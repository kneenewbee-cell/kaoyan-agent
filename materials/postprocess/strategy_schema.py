from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


SubjectName = Literal["math", "politics", "english", "cs408", "408", "unknown"]
DocumentType = Literal["knowledge_notes", "exercise_notes", "outline", "table_like", "mixed", "unknown"]
LanguageName = Literal["zh", "en", "mixed"]
MarkerType = Literal[
    "label_ordinal",
    "chinese_outline",
    "arabic_outline",
    "decimal_outline",
    "chapter",
    "existing_markdown",
    "none",
]
SubsectionType = Literal["fixed_label"]
FallbackAction = Literal["keep_original_structure", "basic_cleanup_only", "use_default_strategy"]
ChunkBy = Literal["heading", "paragraph", "length"]
HeadingFamilyKind = Literal["strong_boundary", "major_section", "block", "item", "outline"]
HeadingFamilyOrdinalStyle = Literal[
    "chinese",
    "arabic",
    "alpha",
    "decimal",
    "circled",
    "paren_chinese",
    "paren_arabic",
]
AnchorPosition = Literal["line_start", "exact"]
RelationType = Literal["direct_parent"]
RelationCertainty = Literal["strong"]
FrontMatterZoneType = Literal[
    "preface_or_overview",
    "catalog_or_navigation",
    "cover_or_metadata",
    "front_matter",
]
FrontMatterAction = Literal["preserve_unprocessed"]
FrontMatterChunkPolicy = Literal["exclude", "single_catalog_chunk"]

RESERVED_NON_HEADING_ANCHORS = {
    "答案",
    "答",
    "分析",
    "解析",
    "点拨",
    "点评",
    "提示",
    "说明",
    "注",
    "解",
    "方法",
    "证明",
    "评注",
}


def _dedupe_strings(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        item = value.strip()
        if item and item not in seen:
            seen.add(item)
            result.append(item)
    return result


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class DocumentProfile(StrictModel):
    subject: SubjectName = "unknown"
    document_type: DocumentType = "unknown"
    language: LanguageName = "zh"
    confidence: float = Field(0.3, ge=0.0, le=1.0)


class MainSectionRule(StrictModel):
    enabled: bool = False
    target_level: int = Field(2, ge=1, le=6)
    marker_type: MarkerType = "none"
    aliases: list[str] = Field(default_factory=list)
    number_styles: list[str] = Field(default_factory=list)
    requires_line_start: bool = True
    requires_colon: bool = False
    min_repeats: int = Field(2, ge=1, le=20)
    examples: list[str] = Field(default_factory=list)

    @field_validator("aliases", "number_styles", "examples")
    @classmethod
    def dedupe(cls, values: list[str]) -> list[str]:
        return _dedupe_strings(values)


class SubsectionRule(StrictModel):
    enabled: bool = True
    target_level: int = Field(3, ge=1, le=6)
    type: SubsectionType = "fixed_label"
    aliases: list[str] = Field(default_factory=list)
    requires_line_start: bool = True
    min_repeats: int = Field(1, ge=1, le=20)

    @field_validator("aliases")
    @classmethod
    def dedupe_aliases(cls, values: list[str]) -> list[str]:
        return _dedupe_strings(values)


class HeadingFamily(StrictModel):
    id: str = Field(min_length=1, max_length=48)
    enabled: bool = True
    kind: HeadingFamilyKind = "block"
    anchors: list[str] = Field(default_factory=list, max_length=12)
    anchor_position: AnchorPosition = "line_start"
    ordinal_styles: list[HeadingFamilyOrdinalStyle] = Field(default_factory=list, max_length=6)
    ordinal_required: bool = False
    units: list[str] = Field(default_factory=list, max_length=8)
    separators: list[str] = Field(default_factory=lambda: ["", " ", "、", ".", "．", "|", "：", ":"], max_length=12)
    title_required: bool = True
    parent_hints: list[str] = Field(default_factory=list, max_length=8)
    min_repeats: int = Field(1, ge=1, le=20)
    examples: list[str] = Field(default_factory=list, max_length=8)

    @field_validator("id")
    @classmethod
    def strip_id(cls, value: str) -> str:
        return value.strip()

    @field_validator("anchors", "ordinal_styles", "units", "separators", "parent_hints", "examples")
    @classmethod
    def dedupe_values(cls, values: list[str]) -> list[str]:
        return _dedupe_strings(values)

    @model_validator(mode="after")
    def validate_family_shape(self) -> "HeadingFamily":
        if not self.anchors and not self.ordinal_styles and not self.units:
            raise ValueError("heading family requires anchors, ordinal_styles, or units")
        if self.kind == "strong_boundary" and not self.units:
            raise ValueError("strong_boundary family requires units")
        if self.ordinal_required and not self.ordinal_styles:
            raise ValueError("ordinal_required requires ordinal_styles")
        if not self.anchors and self.kind not in {"outline", "strong_boundary"} and not self.ordinal_styles:
            raise ValueError("non-outline heading family requires anchors or ordinal_styles")
        return self


class RelationScoreBreakdown(StrictModel):
    interval_structure: int = Field(0, ge=0, le=25)
    coverage_density: int = Field(0, ge=0, le=25)
    numbering_anchor: int = Field(0, ge=0, le=20)
    sample_evidence: int = Field(0, ge=0, le=20)
    counter_evidence: int = Field(0, ge=-50, le=0)


class RelationHint(StrictModel):
    relation_type: RelationType = "direct_parent"
    parent: str = Field(min_length=1, max_length=48)
    child: str = Field(min_length=1, max_length=48)
    score: int = Field(ge=85, le=100)
    certainty: RelationCertainty = "strong"
    score_breakdown: RelationScoreBreakdown = Field(default_factory=RelationScoreBreakdown)
    evidence: list[str] = Field(default_factory=list, max_length=8)
    scope: Literal["body", "unknown"] = "body"

    @field_validator("parent", "child")
    @classmethod
    def strip_family_id(cls, value: str) -> str:
        return value.strip()

    @field_validator("evidence")
    @classmethod
    def dedupe_evidence(cls, values: list[str]) -> list[str]:
        return _dedupe_strings(values)

    @model_validator(mode="after")
    def validate_direct_relation(self) -> "RelationHint":
        if self.parent == self.child:
            raise ValueError("relation parent and child must differ")
        return self


class MetadataRules(StrictModel):
    recognize_bracket_fields: bool = True
    fields: list[str] = Field(default_factory=lambda: ["考频", "难度", "题型", "来源", "备注"])

    @field_validator("fields")
    @classmethod
    def dedupe_fields(cls, values: list[str]) -> list[str]:
        return _dedupe_strings(values)


class CleanupRules(StrictModel):
    normalize_blank_lines: bool = True
    strip_trailing_spaces: bool = True
    remove_control_chars: bool = True
    preserve_tables: bool = True
    preserve_code_blocks: bool = True
    preserve_formulas: bool = True
    preserve_images: bool = True


class FallbackPolicy(StrictModel):
    if_main_sections_less_than: int = Field(2, ge=1, le=20)
    action: FallbackAction = "keep_original_structure"
    chunk_by: ChunkBy = "length"
    reason: str = "未获得可信结构策略"


class SafetyRules(StrictModel):
    do_not_rewrite_content: bool = True
    do_not_summarize: bool = True
    do_not_translate: bool = True
    do_not_delete_unknown_lines: bool = True


class FrontMatterZone(StrictModel):
    type: FrontMatterZoneType
    start_line: int = Field(ge=1)
    end_line: int = Field(ge=1)
    title: str = Field(default="", max_length=40)
    action: FrontMatterAction = "preserve_unprocessed"
    chunk_policy: FrontMatterChunkPolicy = "exclude"
    confidence: float = Field(0.0, ge=0.0, le=1.0)
    signals: list[str] = Field(default_factory=list, max_length=12)

    @model_validator(mode="before")
    @classmethod
    def default_chunk_policy_for_type(cls, data: object) -> object:
        if isinstance(data, dict) and "chunk_policy" not in data:
            if data.get("type") == "catalog_or_navigation":
                data = {**data, "chunk_policy": "single_catalog_chunk"}
            else:
                data = {**data, "chunk_policy": "exclude"}
        return data

    @field_validator("title")
    @classmethod
    def strip_title(cls, value: str) -> str:
        return value.strip()

    @field_validator("signals")
    @classmethod
    def dedupe_signals(cls, values: list[str]) -> list[str]:
        return _dedupe_strings(values)

    @model_validator(mode="after")
    def validate_range(self) -> "FrontMatterZone":
        if self.end_line < self.start_line:
            raise ValueError("front matter zone end_line cannot be before start_line")
        if self.type == "catalog_or_navigation" and self.chunk_policy == "exclude":
            raise ValueError("catalog_or_navigation should use single_catalog_chunk")
        if self.type != "catalog_or_navigation" and self.chunk_policy == "single_catalog_chunk":
            raise ValueError("single_catalog_chunk is only allowed for catalog_or_navigation")
        return self


class DocumentZones(StrictModel):
    front_matter_zones: list[FrontMatterZone] = Field(default_factory=list, max_length=8)
    body_start_line: int | None = Field(default=None, ge=1)
    confidence: float = Field(0.0, ge=0.0, le=1.0)


class CleaningStrategy(StrictModel):
    version: str = "1.0"
    document_profile: DocumentProfile = Field(default_factory=DocumentProfile)
    main_section_rule: MainSectionRule = Field(default_factory=MainSectionRule)
    subsection_rules: list[SubsectionRule] = Field(default_factory=list)
    heading_families: list[HeadingFamily] = Field(default_factory=list, max_length=32)
    relation_hints: list[RelationHint] = Field(default_factory=list, max_length=32)
    metadata_rules: MetadataRules = Field(default_factory=MetadataRules)
    cleanup_rules: CleanupRules = Field(default_factory=CleanupRules)
    fallback_policy: FallbackPolicy = Field(default_factory=FallbackPolicy)
    safety_rules: SafetyRules = Field(default_factory=SafetyRules)
    strategy_source: Literal["qwen", "local", "default"] = "default"

    @model_validator(mode="after")
    def validate_heading_family_graph(self) -> "CleaningStrategy":
        family_ids = [family.id for family in self.heading_families]
        if len(family_ids) != len(set(family_ids)):
            raise ValueError("heading family ids must be unique")
        family_id_set = set(family_ids)
        relation_edges = [(hint.parent, hint.child) for hint in self.relation_hints]
        for parent, child in relation_edges:
            if parent not in family_id_set:
                raise ValueError(f"unknown relation parent family: {parent}")
            if child not in family_id_set:
                raise ValueError(f"unknown relation child family: {child}")
        if len(relation_edges) != len(set(relation_edges)):
            raise ValueError("relation hints must be unique")
        graph: dict[str, list[str]] = {}
        for parent, child in relation_edges:
            graph.setdefault(parent, []).append(child)

        def has_path(start: str, target: str, *, skip_edge: tuple[str, str] | None = None) -> bool:
            stack = [start]
            seen: set[str] = set()
            while stack:
                node = stack.pop()
                if node in seen:
                    continue
                seen.add(node)
                for next_node in graph.get(node, []):
                    if skip_edge == (node, next_node):
                        continue
                    if next_node == target:
                        return True
                    stack.append(next_node)
            return False

        for parent, child in relation_edges:
            if has_path(child, parent):
                raise ValueError("relation hints must not contain cycles")
            if has_path(parent, child, skip_edge=(parent, child)):
                raise ValueError("relation hints must be direct parent-child edges, not transitive edges")
        return self

    def to_dict(self) -> dict:
        return self.model_dump(mode="json")
