"""LLM-assisted postprocess patches for residual render errors.

The LLM is never allowed to rewrite the whole document. It receives only
verified formula occurrences and returns replacement proposals. Local code
validates and applies those proposals.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any, Callable, Protocol

from .formula_extractor import (
    FormulaOccurrence,
    extract_formula_candidates,
    extract_formula_occurrences,
    validate_formula_boundary,
)
from .katex_validator import validate_latex_with_katex_batch


RenderValidator = Callable[[str], bool]
FormulaRenderChecker = Callable[[str, str], bool | tuple[bool, str | None]]


class FormulaRepairClient(Protocol):
    def repair_formula_variants(self, payload: dict[str, Any]) -> dict[str, Any]:
        ...


class HeadingReviewClient(Protocol):
    def review_headings(self, payload: dict[str, Any]) -> dict[str, Any]:
        ...
@dataclass
class LLMCleanResult:
    cleaned_markdown: str
    report: dict[str, Any]
    patches: list[dict[str, Any]]
    warnings: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "enabled": self.report.get("enabled", False),
            "report": self.report,
            "patches": self.patches,
            "warnings": self.warnings,
        }


def _default_render_validator(latex: str) -> bool:
    if not latex or not latex.strip():
        return False
    if "\\kern - delimiterspace" in latex:
        return False
    katex_results, katex_metadata = validate_latex_with_katex_batch([(latex, True)])
    if katex_metadata.get("available") and katex_results:
        return bool(katex_results[0].get("ok"))
    return not validate_formula_boundary(latex)


def _display_mode_for_container(container: str) -> bool:
    return container != "inline_math"


def _normalize_render_check(result: bool | tuple[bool, str | None]) -> tuple[bool, str | None]:
    if isinstance(result, tuple):
        ok, error = result
        return bool(ok), error
    return bool(result), None


def _unsafe_formula_boundary_for_llm(occurrence: FormulaOccurrence) -> bool:
    errors = set(occurrence.completeness_errors)
    return bool(errors.intersection({"starts_with_closing_braces", "brace_underflow"}))


def _render_failure_occurrences_from_checker(
    markdown: str,
    checker: FormulaRenderChecker,
) -> tuple[list[FormulaOccurrence], dict[str, Any]]:
    candidates = extract_formula_candidates(markdown)
    failures: list[FormulaOccurrence] = []
    for candidate in candidates:
        ok, error = _normalize_render_check(checker(candidate.formula, candidate.container))
        if ok:
            continue
        failures.append(
            replace(
                candidate,
                issue=error or "render_failed",
            )
        )
    return failures, {
        "candidate_source": "render_checker",
        "scan_count": len(candidates),
        "render_engine": "custom",
    }


def _render_failure_occurrences_from_katex(markdown: str) -> tuple[list[FormulaOccurrence], dict[str, Any]]:
    candidates = extract_formula_candidates(markdown)
    katex_results, katex_metadata = validate_latex_with_katex_batch(
        [
            (candidate.formula, _display_mode_for_container(candidate.container))
            for candidate in candidates
        ]
    )
    failures: list[FormulaOccurrence] = []
    if katex_metadata.get("available"):
        for candidate, result in zip(candidates, katex_results):
            if result.get("ok"):
                continue
            failures.append(
                replace(
                    candidate,
                    issue=str(result.get("error") or "katex_render_failed"),
                )
            )
    return failures, {
        "candidate_source": "katex" if katex_metadata.get("available") else "pattern_fallback",
        "scan_count": len(candidates),
        "render_engine": katex_metadata.get("engine", "katex"),
        "render_engine_available": bool(katex_metadata.get("available")),
        "render_engine_version": katex_metadata.get("version"),
        "render_engine_error": katex_metadata.get("error"),
    }


def build_heading_review_context(markdown: str) -> dict[str, Any]:
    """Build a compact heading tree from the local dynamic heading stack."""

    roots: list[dict[str, Any]] = []
    stack: list[dict[str, Any]] = []
    events: list[dict[str, Any]] = []
    previous_level: int | None = None

    for line_no, line in enumerate(markdown.splitlines(), start=1):
        stripped = line.strip()
        if not stripped.startswith("#"):
            continue
        hashes = len(stripped) - len(stripped.lstrip("#"))
        if hashes < 1 or hashes > 6:
            continue
        if len(stripped) <= hashes or stripped[hashes] != " ":
            continue
        title = stripped[hashes:].strip()
        if previous_level is not None and hashes > previous_level + 1:
            events.append(
                {
                    "event": "heading_level_jump",
                    "line": line_no,
                    "from_level": previous_level,
                    "to_level": hashes,
                    "title": title,
                }
            )
        while stack and int(stack[-1]["level"]) >= hashes:
            stack.pop()
        node = {
            "line": line_no,
            "level": hashes,
            "title": title,
            "children": [],
        }
        if stack:
            stack[-1]["children"].append(node)
        else:
            roots.append(node)
        stack.append(node)
        previous_level = hashes

    return {
        "heading_tree": roots,
        "heading_events": events,
        "heading_count": _count_heading_nodes(roots),
    }


def _count_heading_nodes(nodes: list[dict[str, Any]]) -> int:
    total = 0
    pending = list(nodes)
    while pending:
        node = pending.pop()
        total += 1
        pending.extend(list(node.get("children", [])))
    return total


def _proposal_confidence(proposal: dict[str, Any]) -> float:
    try:
        return float(proposal.get("confidence", 0.0))
    except (TypeError, ValueError):
        return 0.0


def _clean_report_payload(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _clean_report_payload(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_clean_report_payload(item) for item in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)


def _nearby_context(markdown: str, occurrence: FormulaOccurrence, *, window: int = 2) -> dict[str, Any]:
    lines = markdown.splitlines()
    line_index = max(0, occurrence.line_start - 1)
    start = max(0, line_index - window)
    end = min(len(lines), occurrence.line_end + window)
    return {
        "before": [
            {"line": index + 1, "text": lines[index]}
            for index in range(start, line_index)
        ],
        "after": [
            {"line": index + 1, "text": lines[index]}
            for index in range(occurrence.line_end, end)
        ],
    }


def _make_formula_payload(
    occurrence: FormulaOccurrence,
    heading_context: dict[str, Any],
    *,
    markdown: str,
) -> dict[str, Any]:
    return {
        "formula_id": occurrence.occurrence_id,
        "formula": occurrence.formula,
        "container": occurrence.container,
        "markdown_line": occurrence.markdown_line,
        "line_start": occurrence.line_start,
        "line_end": occurrence.line_end,
        "heading_path": list(occurrence.heading_path),
        "extract_confidence": occurrence.extract_confidence,
        "completeness_errors": list(occurrence.completeness_errors),
        "render_issue": occurrence.issue,
        "nearby_context": _nearby_context(markdown, occurrence),
        "heading_context_summary": {
            "heading_count": heading_context.get("heading_count", 0),
            "heading_events": list(heading_context.get("heading_events", []))[:20],
        },
        "instruction": (
            "Return JSON only. Produce direct replacement LaTeX candidates for only this formula span. "
            "Do not include Markdown delimiters and do not rewrite surrounding Markdown."
        ),
    }


def _make_direct_variants_payload(
    occurrence: FormulaOccurrence,
    heading_context: dict[str, Any],
    *,
    markdown: str,
) -> dict[str, Any]:
    payload = _make_formula_payload(occurrence, heading_context, markdown=markdown)
    payload["instruction"] = (
        "Return three direct replacement LaTeX formulas for only this formula span. "
        "Do not include Markdown delimiters. Prefer candidates that preserve the original math meaning, "
        "but every candidate must be valid KaTeX/MathJax LaTeX. Return JSON with variants only."
    )
    return payload


def _make_heading_review_payload(heading_context: dict[str, Any]) -> dict[str, Any]:
    return {
        "heading_context": heading_context,
        "instruction": (
            "Review whether this cleaned Markdown heading tree is structurally plausible. "
            "Return JSON only. Do not rewrite the full document. Report suspicious heading "
            "level jumps, body text misrecognized as headings, repeated headings, and empty "
            "sections. If no issue is clear, return quality='ok'."
        ),
    }


def _variant_formula(variant: dict[str, Any]) -> str:
    return str(variant.get("formula") or variant.get("replacement_formula") or "").strip()


def _ranked_variants(response: dict[str, Any]) -> list[dict[str, Any]]:
    raw_variants = response.get("variants", [])
    if not isinstance(raw_variants, list):
        return []
    variants = [variant for variant in raw_variants if isinstance(variant, dict)]
    return sorted(variants, key=_proposal_confidence, reverse=True)


def _select_direct_variant(
    response: dict[str, Any],
    *,
    min_confidence: float,
    render_validator: RenderValidator,
) -> tuple[str | None, dict[str, Any] | None, list[dict[str, Any]], str | None]:
    variants_report: list[dict[str, Any]] = []
    selected_formula: str | None = None
    selected_record: dict[str, Any] | None = None
    for variant in _ranked_variants(response):
        formula = _variant_formula(variant)
        confidence = _proposal_confidence(variant)
        render_ok = bool(formula) and render_validator(formula)
        record = {
            **_clean_report_payload(variant),
            "formula": formula,
            "confidence": confidence,
            "render_ok": render_ok,
        }
        if not formula:
            record["rejection"] = "empty_formula"
        elif bool(variant.get("needs_human_review")):
            record["rejection"] = "needs_human_review"
        elif confidence < min_confidence:
            record["rejection"] = "low_confidence"
        elif not render_ok:
            record["rejection"] = "replacement_failed_render_validation"
        variants_report.append(record)
        if "rejection" not in record and selected_formula is None:
            selected_formula = formula
            selected_record = record
    if not variants_report:
        return None, None, variants_report, "no_variants"
    if selected_formula is not None and selected_record is not None:
        return selected_formula, selected_record, variants_report, None
    return None, None, variants_report, "no_valid_variant"


def clean_markdown_with_llm_patches(
    markdown: str,
    *,
    formula_repair_client: FormulaRepairClient | None = None,
    heading_review_client: HeadingReviewClient | None = None,
    render_issue_patterns: list[str] | tuple[str, ...] | None = None,
    formula_render_checker: FormulaRenderChecker | None = None,
    render_validator: RenderValidator | None = None,
    min_confidence: float = 0.8,
) -> LLMCleanResult:
    heading_context = build_heading_review_context(markdown)
    candidate_metadata: dict[str, Any]
    if render_issue_patterns is not None:
        occurrences = extract_formula_occurrences(markdown, issue_patterns=render_issue_patterns)
        candidate_metadata = {
            "candidate_source": "pattern",
            "scan_count": len(occurrences),
            "render_engine": None,
        }
    elif formula_render_checker is not None:
        occurrences, candidate_metadata = _render_failure_occurrences_from_checker(markdown, formula_render_checker)
    else:
        occurrences, candidate_metadata = _render_failure_occurrences_from_katex(markdown)
        if candidate_metadata.get("candidate_source") == "pattern_fallback":
            occurrences = extract_formula_occurrences(markdown)
    validator = render_validator or _default_render_validator
    warnings: list[str] = []
    patches: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []

    if formula_repair_client is not None:
        for occurrence in occurrences:
            if _unsafe_formula_boundary_for_llm(occurrence):
                skipped.append(
                    {
                        "formula_id": occurrence.occurrence_id,
                        "line": occurrence.line_start,
                        "reason": "unsafe_formula_boundary",
                        "completeness_errors": occurrence.completeness_errors,
                    }
                )
                continue
            try:
                variants_response = formula_repair_client.repair_formula_variants(
                    _make_direct_variants_payload(
                        occurrence,
                        heading_context,
                        markdown=markdown,
                    )
                )
                direct_replacement, selected_variant, variants_report, variant_rejection = _select_direct_variant(
                    variants_response,
                    min_confidence=min_confidence,
                    render_validator=validator,
                )
            except Exception as exc:  # pragma: no cover - defensive against real API clients.
                warnings.append(f"llm_formula_variants_error:{exc.__class__.__name__}")
                skipped.append(
                    {
                        "formula_id": occurrence.occurrence_id,
                        "line": occurrence.line_start,
                        "reason": "client_error",
                        "error_type": exc.__class__.__name__,
                    }
                )
                continue
            if direct_replacement is None or selected_variant is None:
                skipped.append(
                    {
                        "formula_id": occurrence.occurrence_id,
                        "line": occurrence.line_start,
                        "reason": variant_rejection or "no_valid_variant",
                        "direct_variants": variants_report,
                    }
                )
                continue
            patches.append(
                {
                    "type": "formula_render_fix",
                    "source": "direct_variant",
                    "formula_id": occurrence.occurrence_id,
                    "line": occurrence.line_start,
                    "start_offset": occurrence.start_offset,
                    "end_offset": occurrence.end_offset,
                    "original_formula": occurrence.formula,
                    "replacement_formula": direct_replacement,
                    "confidence": selected_variant.get("confidence", 0.0),
                    "reason": selected_variant.get("reason", ""),
                    "variants": variants_report,
                }
            )
    elif occurrences:
        warnings.append("llm_formula_repair_client_unavailable")

    heading_review_report: dict[str, Any] = {
        "enabled": False,
        "context": heading_context,
    }
    if heading_review_client is not None:
        try:
            heading_review_report = {
                "enabled": True,
                "context": heading_context,
                "review": heading_review_client.review_headings(_make_heading_review_payload(heading_context)),
            }
        except Exception as exc:  # pragma: no cover - defensive against real API clients.
            warnings.append(f"llm_heading_review_error:{exc.__class__.__name__}")
            heading_review_report = {
                "enabled": True,
                "context": heading_context,
                "review": None,
                "error_type": exc.__class__.__name__,
            }

    cleaned = markdown
    applied: list[dict[str, Any]] = []
    for patch in sorted(patches, key=lambda item: int(item["start_offset"]), reverse=True):
        start = int(patch["start_offset"])
        end = int(patch["end_offset"])
        if cleaned[start:end] != patch["original_formula"]:
            skipped.append(
                {
                    "formula_id": patch["formula_id"],
                    "line": patch["line"],
                    "reason": "source_span_mismatch",
                }
            )
            continue
        cleaned = cleaned[:start] + str(patch["replacement_formula"]) + cleaned[end:]
        applied.append(patch)

    applied.reverse()
    report = {
        "enabled": formula_repair_client is not None,
        "formula_repair": {
            **candidate_metadata,
            "candidate_count": len(occurrences),
            "applied_count": len(applied),
            "skipped_count": len(skipped),
            "skipped": skipped,
            "applied": applied,
        },
        "heading_review": heading_review_report,
    }
    return LLMCleanResult(
        cleaned_markdown=cleaned,
        report=report,
        patches=applied,
        warnings=warnings,
    )


def repair_render_error_formulas(
    markdown: str,
    *,
    formula_repair_client: FormulaRepairClient,
    heading_review_client: HeadingReviewClient | None = None,
    render_issue_patterns: list[str] | tuple[str, ...] | None = None,
    formula_render_checker: FormulaRenderChecker | None = None,
    render_validator: RenderValidator | None = None,
    min_confidence: float = 0.8,
) -> LLMCleanResult:
    """Public focused entry point for formula-only LLM repair."""

    return clean_markdown_with_llm_patches(
        markdown,
        formula_repair_client=formula_repair_client,
        heading_review_client=heading_review_client,
        render_issue_patterns=render_issue_patterns,
        formula_render_checker=formula_render_checker,
        render_validator=render_validator,
        min_confidence=min_confidence,
    )
