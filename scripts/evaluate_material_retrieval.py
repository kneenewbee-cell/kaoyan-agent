#!/usr/bin/env python3
"""Evaluate materials retrieval quality against labeled local PDF fixtures.

This script is intentionally separate from production search code. It monkey
patches search-time constants per configuration, runs the public
``search_user_materials`` entry point, and writes a JSON report for comparison.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import materials.search as material_search
from materials.indexing.query_processor import process_query
from materials.search import search_user_materials


EVAL_USER_ID = "retrieval_eval"


@dataclass(frozen=True)
class QueryCase:
    case_id: str
    query: str
    subject: str
    positive: bool
    expected_terms: tuple[str, ...] = ()
    max_rank: int = 3
    note: str = ""


@dataclass(frozen=True)
class SearchConfig:
    name: str
    vector_min_score: float
    vector_bonus_weight: float
    vector_bonus_cap: float
    title_hit_bonus_cap: float
    text_hit_bonus_cap: float
    specific_table_penalty: float
    specific_overview_table_penalty: float
    overview_table_bonus: float
    display_min_score: float | None
    min_term_matches: int
    min_term_match_ratio: float
    exact_query_heading_bonus: float
    exact_query_text_bonus: float
    fix_overview_regex: bool = True


QUERY_CASES: tuple[QueryCase, ...] = (
    # Math exact and near-exact concepts.
    QueryCase("m01", "事件与概率公式", "math", True, ("事件与概率公式", "概率公式"), 1),
    QueryCase("m02", "两个事件相互独立怎么判断", "math", True, ("相互独立", "独立"), 3),
    QueryCase("m03", "古典概型和几何概型", "math", True, ("古典概型", "几何概型"), 3),
    QueryCase("m04", "全概率公式", "math", True, ("全概率公式",), 1),
    QueryCase("m05", "贝叶斯公式", "math", True, ("贝叶斯公式",), 1),
    QueryCase("m06", "一维随机变量与分布函数", "math", True, ("一维随机变量", "分布函数"), 3),
    QueryCase("m07", "二项分布 泊松分布", "math", True, ("二项分布", "泊松分布"), 3),
    QueryCase("m08", "指数分布 均匀分布 正态分布", "math", True, ("指数分布", "均匀分布", "正态分布"), 3),
    QueryCase("m09", "二维随机变量 联合分布函数", "math", True, ("二维随机变量", "联合分布函数"), 3),
    QueryCase("m10", "边缘分布怎么求", "math", True, ("边缘分布",), 3),
    QueryCase("m11", "随机变量函数的分布", "math", True, ("随机变量函数", "分布"), 3),
    QueryCase("m12", "数学期望的性质", "math", True, ("数学期望",), 3),
    QueryCase("m13", "方差公式", "math", True, ("方差",), 3),
    QueryCase("m14", "协方差和相关系数", "math", True, ("协方差", "相关系数"), 3),
    QueryCase("m15", "切比雪夫不等式", "math", True, ("切比雪夫不等式",), 1),
    QueryCase("m16", "大数定律", "math", True, ("大数定律",), 1),
    QueryCase("m17", "中心极限定理", "math", True, ("中心极限定理",), 1),
    QueryCase("m18", "三大分布", "math", True, ("三大分布",), 2),
    QueryCase("m19", "点估计", "math", True, ("点估计",), 2),
    QueryCase("m20", "假设检验的步骤", "math", True, ("假设检验",), 3),
    QueryCase("m21", "P(A|B) 条件概率", "math", True, ("条件概率", "P ( A | B"), 3),
    QueryCase("m22", "二维连续型随机变量密度", "math", True, ("二维连续型随机变量", "密度"), 3),
    # Politics exact and paraphrase concepts.
    QueryCase("p01", "思想道德和法律的关系", "politics", True, ("思想道德和法律的关系",), 1),
    QueryCase("p02", "人的本质是什么", "politics", True, ("人的本质",), 3),
    QueryCase("p03", "个人与社会的辩证关系", "politics", True, ("个人与社会", "辩证关系"), 3),
    QueryCase("p04", "人生观的主要内容", "politics", True, ("人生观的主要内容",), 1),
    QueryCase("p05", "人生目的回答什么问题", "politics", True, ("人生目的", "为什么活着"), 3),
    QueryCase("p06", "人生价值的评价与实现", "politics", True, ("人生价值", "评价"), 3),
    QueryCase("p07", "理想信念是精神之钙", "politics", True, ("精神之“钙”", "理想信念"), 3),
    QueryCase("p08", "中国精神的丰富内涵", "politics", True, ("中国精神", "丰富内涵"), 3),
    QueryCase("p09", "民族精神与时代精神的辩证统一", "politics", True, ("民族精神", "时代精神"), 3),
    QueryCase("p10", "新时代的爱国主义", "politics", True, ("新时代的爱国主义",), 1),
    QueryCase("p11", "社会主义核心价值观", "politics", True, ("社会主义核心价值观",), 3),
    QueryCase("p12", "道德的功能和作用", "politics", True, ("道德的功能", "道德的作用"), 3),
    QueryCase("p13", "法律的含义", "politics", True, ("法律的含义",), 1),
    QueryCase("p14", "全面依法治国根本遵循", "politics", True, ("全面依法治国", "根本遵循"), 3),
    QueryCase("p15", "习近平法治思想十一个坚持", "politics", True, ("习近平法治思想", "十一个坚持"), 3),
    QueryCase("p16", "宪法的基本原则", "politics", True, ("宪法", "基本原则"), 3),
    # Cross-subject and out-of-corpus negatives.
    QueryCase("n01", "社会主义核心价值观", "math", False, note="politics query inside math scope"),
    QueryCase("n02", "法律的含义", "math", False, note="politics query inside math scope"),
    QueryCase("n03", "全概率公式", "politics", False, note="math query inside politics scope"),
    QueryCase("n04", "正态分布", "politics", False, note="math query inside politics scope"),
    QueryCase("n05", "罗尔定理", "math", False, note="calculus topic outside probability PDF"),
    QueryCase("n06", "线性代数特征值", "math", False, note="linear algebra topic outside probability PDF"),
    QueryCase("n07", "数据库索引优化", "math", False, note="unrelated computer science"),
    QueryCase("n08", "托福阅读长难句", "politics", False, note="unrelated English exam"),
    QueryCase("n09", "化学平衡常数", "politics", False, note="unrelated chemistry"),
    QueryCase("n10", "货币政策和财政政策", "politics", False, note="macro topic outside this ethics/law PDF"),
)


CONFIGS: tuple[SearchConfig, ...] = (
    SearchConfig(
        name="baseline",
        vector_min_score=0.55,
        vector_bonus_weight=0.025,
        vector_bonus_cap=0.03,
        title_hit_bonus_cap=0.07,
        text_hit_bonus_cap=0.025,
        specific_table_penalty=0.015,
        specific_overview_table_penalty=0.045,
        overview_table_bonus=0.025,
        display_min_score=None,
        min_term_matches=0,
        min_term_match_ratio=0.0,
        exact_query_heading_bonus=0.0,
        exact_query_text_bonus=0.0,
        fix_overview_regex=False,
    ),
    SearchConfig(
        name="baseline_display_045",
        vector_min_score=0.55,
        vector_bonus_weight=0.025,
        vector_bonus_cap=0.03,
        title_hit_bonus_cap=0.07,
        text_hit_bonus_cap=0.025,
        specific_table_penalty=0.015,
        specific_overview_table_penalty=0.045,
        overview_table_bonus=0.025,
        display_min_score=0.045,
        min_term_matches=0,
        min_term_match_ratio=0.0,
        exact_query_heading_bonus=0.0,
        exact_query_text_bonus=0.0,
    ),
    SearchConfig(
        name="balanced_v2",
        vector_min_score=0.60,
        vector_bonus_weight=0.020,
        vector_bonus_cap=0.024,
        title_hit_bonus_cap=0.105,
        text_hit_bonus_cap=0.020,
        specific_table_penalty=0.025,
        specific_overview_table_penalty=0.060,
        overview_table_bonus=0.030,
        display_min_score=0.048,
        min_term_matches=0,
        min_term_match_ratio=0.0,
        exact_query_heading_bonus=0.0,
        exact_query_text_bonus=0.0,
    ),
    SearchConfig(
        name="precision_first",
        vector_min_score=0.66,
        vector_bonus_weight=0.014,
        vector_bonus_cap=0.018,
        title_hit_bonus_cap=0.125,
        text_hit_bonus_cap=0.014,
        specific_table_penalty=0.035,
        specific_overview_table_penalty=0.070,
        overview_table_bonus=0.025,
        display_min_score=0.055,
        min_term_matches=0,
        min_term_match_ratio=0.0,
        exact_query_heading_bonus=0.0,
        exact_query_text_bonus=0.0,
    ),
    SearchConfig(
        name="semantic_recall",
        vector_min_score=0.55,
        vector_bonus_weight=0.045,
        vector_bonus_cap=0.050,
        title_hit_bonus_cap=0.075,
        text_hit_bonus_cap=0.032,
        specific_table_penalty=0.012,
        specific_overview_table_penalty=0.035,
        overview_table_bonus=0.030,
        display_min_score=0.040,
        min_term_matches=0,
        min_term_match_ratio=0.0,
        exact_query_heading_bonus=0.0,
        exact_query_text_bonus=0.0,
    ),
    SearchConfig(
        name="balanced_v2_gate",
        vector_min_score=0.60,
        vector_bonus_weight=0.020,
        vector_bonus_cap=0.024,
        title_hit_bonus_cap=0.105,
        text_hit_bonus_cap=0.020,
        specific_table_penalty=0.025,
        specific_overview_table_penalty=0.060,
        overview_table_bonus=0.030,
        display_min_score=0.048,
        min_term_matches=2,
        min_term_match_ratio=0.50,
        exact_query_heading_bonus=0.0,
        exact_query_text_bonus=0.0,
    ),
    SearchConfig(
        name="precision_gate",
        vector_min_score=0.62,
        vector_bonus_weight=0.018,
        vector_bonus_cap=0.022,
        title_hit_bonus_cap=0.115,
        text_hit_bonus_cap=0.018,
        specific_table_penalty=0.030,
        specific_overview_table_penalty=0.065,
        overview_table_bonus=0.028,
        display_min_score=0.048,
        min_term_matches=2,
        min_term_match_ratio=0.50,
        exact_query_heading_bonus=0.0,
        exact_query_text_bonus=0.0,
    ),
    SearchConfig(
        name="balanced_v3_gate_exact",
        vector_min_score=0.60,
        vector_bonus_weight=0.020,
        vector_bonus_cap=0.024,
        title_hit_bonus_cap=0.105,
        text_hit_bonus_cap=0.020,
        specific_table_penalty=0.025,
        specific_overview_table_penalty=0.060,
        overview_table_bonus=0.030,
        display_min_score=0.040,
        min_term_matches=2,
        min_term_match_ratio=0.50,
        exact_query_heading_bonus=0.035,
        exact_query_text_bonus=0.012,
    ),
)


ORIGINALS: dict[str, Any] = {}


def compact(text: str) -> str:
    return "".join(str(text or "").lower().split())


def configure_stdout() -> None:
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")


def capture_originals() -> None:
    if ORIGINALS:
        return
    for name in (
        "VECTOR_SCORE_BONUS_WEIGHT",
        "VECTOR_SCORE_BONUS_CAP",
        "TITLE_HIT_BONUS_CAP",
        "TEXT_HIT_BONUS_CAP",
        "SPECIFIC_TABLE_PENALTY",
        "SPECIFIC_OVERVIEW_TABLE_PENALTY",
        "OVERVIEW_TABLE_BONUS",
        "OVERVIEW_QUERY_RE",
        "OVERVIEW_TABLE_RE",
    ):
        ORIGINALS[name] = getattr(material_search, name)
    ORIGINALS["MATERIALS_VECTOR_MIN_SCORE"] = os.environ.get("MATERIALS_VECTOR_MIN_SCORE")


def restore_originals() -> None:
    for name, value in ORIGINALS.items():
        if name == "MATERIALS_VECTOR_MIN_SCORE":
            if value is None:
                os.environ.pop(name, None)
            else:
                os.environ[name] = value
            continue
        setattr(material_search, name, value)


def apply_config(config: SearchConfig) -> None:
    os.environ["MATERIALS_VECTOR_MIN_SCORE"] = str(config.vector_min_score)
    material_search.VECTOR_SCORE_BONUS_WEIGHT = config.vector_bonus_weight
    material_search.VECTOR_SCORE_BONUS_CAP = config.vector_bonus_cap
    material_search.TITLE_HIT_BONUS_CAP = config.title_hit_bonus_cap
    material_search.TEXT_HIT_BONUS_CAP = config.text_hit_bonus_cap
    material_search.SPECIFIC_TABLE_PENALTY = config.specific_table_penalty
    material_search.SPECIFIC_OVERVIEW_TABLE_PENALTY = config.specific_overview_table_penalty
    material_search.OVERVIEW_TABLE_BONUS = config.overview_table_bonus
    if config.fix_overview_regex:
        material_search.OVERVIEW_QUERY_RE = re.compile(
            r"(考试要求|考试内容|目录|概览|总览|汇总|一览|对比|区别|表格|列表|清单|范围)"
        )
        material_search.OVERVIEW_TABLE_RE = re.compile(
            r"(考试要求|考试内容|目录|概览|总览|汇总|一览|知识清单|知识网络|范围)"
        )


def result_score(result: Any) -> float:
    metadata = dict(getattr(result, "metadata", {}) or {})
    if "rerank_score" in metadata:
        try:
            return float(metadata["rerank_score"])
        except (TypeError, ValueError):
            pass
    try:
        return float(getattr(result, "score", 0.0))
    except (TypeError, ValueError):
        return 0.0


def exact_query_bonus(result: Any, case: QueryCase, config: SearchConfig) -> float:
    if config.exact_query_heading_bonus <= 0 and config.exact_query_text_bonus <= 0:
        return 0.0
    query = compact(case.query)
    if len(query) < 3:
        return 0.0
    heading = compact(
        " ".join([*(getattr(result, "heading_path", []) or []), getattr(result, "section_title", "") or ""])
    )
    body = compact(getattr(result, "text", "") or "")
    if query in heading:
        return config.exact_query_heading_bonus
    if query in body:
        return config.exact_query_text_bonus
    return 0.0


def effective_score(result: Any, case: QueryCase, config: SearchConfig) -> float:
    return result_score(result) + exact_query_bonus(result, case, config)


def result_blob(result: Any) -> str:
    metadata = dict(getattr(result, "metadata", {}) or {})
    return " ".join(
        [
            " ".join(getattr(result, "heading_path", []) or []),
            getattr(result, "section_title", "") or "",
            str(metadata.get("title") or ""),
            getattr(result, "text", "") or "",
        ]
    )


def relevant(result: Any, case: QueryCase) -> bool:
    if not case.expected_terms:
        return False
    blob = compact(result_blob(result))
    return any(compact(term) in blob for term in case.expected_terms if term)


def matched_query_term_count(result: Any, query: str) -> tuple[int, int, list[str]]:
    plan = process_query(query)
    terms = tuple(term for term in (plan.core_terms or plan.phrase_terms or plan.terms) if term)
    if not terms:
        return 0, 0, []
    blob = compact(result_blob(result))
    matched = [term for term in terms if compact(term) in blob]
    return len(matched), len(terms), matched


def passes_display_gate(result: Any, case: QueryCase, config: SearchConfig) -> bool:
    if config.display_min_score is not None and effective_score(result, case, config) < config.display_min_score:
        return False
    if config.min_term_matches <= 0 and config.min_term_match_ratio <= 0:
        return True

    matched_count, total_count, matched = matched_query_term_count(result, case.query)
    if total_count <= 1:
        return True
    required_count = max(config.min_term_matches, int(total_count * config.min_term_match_ratio + 0.999))
    if matched_count >= required_count:
        return True

    # Keep explicit phrase hits even when tokenization over-splits around formulas.
    phrase_terms = tuple(term for term in process_query(case.query).phrase_terms if term)
    blob = compact(result_blob(result))
    if phrase_terms and any(compact(term) in blob for term in phrase_terms):
        return True

    metadata = getattr(result, "metadata", {}) or {}
    metadata["eval_gate"] = {
        "matched_terms": matched,
        "matched_count": matched_count,
        "total_count": total_count,
        "required_count": required_count,
    }
    result.metadata = metadata
    return False


def summarize_result(result: Any) -> dict[str, Any]:
    metadata = dict(getattr(result, "metadata", {}) or {})
    return {
        "rank": getattr(result, "rank", None),
        "score": round(result_score(result), 6),
        "eval_effective_score": metadata.get("eval_effective_score", ""),
        "material_id": getattr(result, "material_id", ""),
        "chunk_id": getattr(result, "chunk_id", ""),
        "section_title": getattr(result, "section_title", "") or "",
        "heading_path": getattr(result, "heading_path", []) or [],
        "matched_by": metadata.get("matched_by", []),
        "search_mode": metadata.get("search_mode", ""),
        "vector_distance": metadata.get("distance", ""),
        "rerank": metadata.get("rerank", {}),
        "llm_rerank": metadata.get("llm_rerank", {}),
        "retrieval_plan": metadata.get("retrieval_plan", {}),
        "snippet": (getattr(result, "text", "") or "")[:220].replace("\n", " "),
    }


def evaluate_case(case: QueryCase, config: SearchConfig, mode: str, top_k: int) -> dict[str, Any]:
    started = time.perf_counter()
    raw_results = search_user_materials(
        EVAL_USER_ID,
        case.query,
        top_k=top_k,
        filters={"subject": case.subject},
        mode=mode,
    )
    elapsed_ms = (time.perf_counter() - started) * 1000.0
    displayed = list(raw_results)
    displayed = [item for item in displayed if passes_display_gate(item, case, config)]
    if mode not in {"llm", "hybrid_llm"}:
        displayed.sort(key=lambda item: effective_score(item, case, config), reverse=True)
    for index, result in enumerate(displayed, start=1):
        metadata = dict(getattr(result, "metadata", {}) or {})
        metadata["eval_effective_score"] = round(effective_score(result, case, config), 6)
        metadata["eval_display_rank"] = index
        result.metadata = metadata

    first_relevant_rank: int | None = None
    for index, result in enumerate(displayed, start=1):
        if relevant(result, case):
            first_relevant_rank = index
            break

    if case.positive:
        passed = first_relevant_rank is not None and first_relevant_rank <= case.max_rank
    else:
        passed = len(displayed) == 0

    return {
        "case_id": case.case_id,
        "query": case.query,
        "subject": case.subject,
        "positive": case.positive,
        "expected_terms": list(case.expected_terms),
        "max_rank": case.max_rank,
        "note": case.note,
        "passed": passed,
        "elapsed_ms": round(elapsed_ms, 2),
        "raw_count": len(raw_results),
        "displayed_count": len(displayed),
        "first_relevant_rank": first_relevant_rank,
        "top_results": [summarize_result(result) for result in displayed[:5]],
        "raw_top_results": [summarize_result(result) for result in raw_results[:5]],
    }


def summarize_config(config: SearchConfig, cases: list[dict[str, Any]]) -> dict[str, Any]:
    positives = [case for case in cases if case["positive"]]
    negatives = [case for case in cases if not case["positive"]]
    positive_passed = sum(1 for case in positives if case["passed"])
    negative_passed = sum(1 for case in negatives if case["passed"])
    top1 = sum(1 for case in positives if case["first_relevant_rank"] == 1)
    top3 = sum(
        1
        for case in positives
        if case["first_relevant_rank"] is not None and case["first_relevant_rank"] <= 3
    )
    reciprocal_ranks = [
        1.0 / case["first_relevant_rank"]
        for case in positives
        if case["first_relevant_rank"]
    ]
    return {
        "name": config.name,
        "config": config.__dict__,
        "case_count": len(cases),
        "positive_count": len(positives),
        "negative_count": len(negatives),
        "passed_count": positive_passed + negative_passed,
        "pass_rate": round((positive_passed + negative_passed) / len(cases), 4) if cases else 0.0,
        "positive_pass_rate": round(positive_passed / len(positives), 4) if positives else 0.0,
        "negative_suppression_rate": round(negative_passed / len(negatives), 4) if negatives else 0.0,
        "positive_top1_rate": round(top1 / len(positives), 4) if positives else 0.0,
        "positive_top3_rate": round(top3 / len(positives), 4) if positives else 0.0,
        "positive_mrr": round(sum(reciprocal_ranks) / len(positives), 4) if positives else 0.0,
        "avg_elapsed_ms": round(sum(case["elapsed_ms"] for case in cases) / len(cases), 2) if cases else 0.0,
        "avg_negative_displayed_count": round(
            sum(case["displayed_count"] for case in negatives) / len(negatives), 3
        ) if negatives else 0.0,
        "failures": [
            {
                "case_id": case["case_id"],
                "query": case["query"],
                "subject": case["subject"],
                "positive": case["positive"],
                "displayed_count": case["displayed_count"],
                "first_relevant_rank": case["first_relevant_rank"],
                "top": case["top_results"][:1],
            }
            for case in cases
            if not case["passed"]
        ],
    }


def run_eval(config_names: set[str], mode: str, top_k: int) -> dict[str, Any]:
    selected_configs = [config for config in CONFIGS if not config_names or config.name in config_names]
    report: dict[str, Any] = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "user_id": EVAL_USER_ID,
        "mode": mode,
        "top_k": top_k,
        "query_count": len(QUERY_CASES),
        "configs": [],
    }

    capture_originals()
    try:
        for config in selected_configs:
            restore_originals()
            apply_config(config)
            cases = [evaluate_case(case, config, mode, top_k) for case in QUERY_CASES]
            report["configs"].append(
                {
                    "summary": summarize_config(config, cases),
                    "cases": cases,
                }
            )
    finally:
        restore_originals()
    return report


def print_table(report: dict[str, Any]) -> None:
    header = (
        "config",
        "pass",
        "pos",
        "neg",
        "top1",
        "mrr",
        "neg_avg",
        "ms",
        "fails",
    )
    print("\t".join(header))
    for config_report in report["configs"]:
        summary = config_report["summary"]
        print(
            "\t".join(
                [
                    summary["name"],
                    f"{summary['pass_rate']:.3f}",
                    f"{summary['positive_pass_rate']:.3f}",
                    f"{summary['negative_suppression_rate']:.3f}",
                    f"{summary['positive_top1_rate']:.3f}",
                    f"{summary['positive_mrr']:.3f}",
                    f"{summary['avg_negative_displayed_count']:.2f}",
                    f"{summary['avg_elapsed_ms']:.0f}",
                    str(len(summary["failures"])),
                ]
            )
        )


def main() -> None:
    configure_stdout()
    parser = argparse.ArgumentParser(description="Evaluate user-material retrieval configurations.")
    parser.add_argument("--mode", choices=["keyword", "vector", "hybrid", "llm", "hybrid_llm"], default="hybrid")
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument(
        "--config",
        action="append",
        default=[],
        help="Config name to run; may be repeated. Defaults to all.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="",
        help="Report path. Defaults to data/runtime/evals/material_retrieval_<timestamp>.json",
    )
    args = parser.parse_args()

    report = run_eval(set(args.config), args.mode, args.top_k)
    if args.output:
        output_path = Path(args.output)
    else:
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = ROOT / "data" / "runtime" / "evals" / f"material_retrieval_{stamp}.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print_table(report)
    print(f"report: {output_path}")


if __name__ == "__main__":
    main()
