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
PatternTokenType = Literal["literal", "ordinal", "separator", "whitespace", "title_text"]
OrdinalStyle = Literal["chinese", "arabic", "decimal"]
HeadingRole = Literal["main", "subsection"]
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


class PatternToken(StrictModel):
    type: PatternTokenType
    values: list[str] = Field(default_factory=list, max_length=20)
    styles: list[OrdinalStyle] = Field(default_factory=list, max_length=3)
    optional: bool = False
    min_chars: int = Field(1, ge=1, le=120)
    max_chars: int = Field(80, ge=1, le=120)

    @field_validator("values")
    @classmethod
    def validate_values(cls, values: list[str]) -> list[str]:
        result = _dedupe_strings(values)
        if any(len(value) > 24 for value in result):
            raise ValueError("pattern token value is too long")
        return result

    @field_validator("styles")
    @classmethod
    def dedupe_styles(cls, values: list[OrdinalStyle]) -> list[OrdinalStyle]:
        return list(dict.fromkeys(values))

    @model_validator(mode="after")
    def validate_token_shape(self) -> "PatternToken":
        if self.type in {"literal", "separator"} and not self.values:
            raise ValueError(f"{self.type} token requires values")
        if self.type == "ordinal" and not self.styles:
            raise ValueError("ordinal token requires styles")
        if self.min_chars > self.max_chars:
            raise ValueError("min_chars cannot exceed max_chars")
        return self


class HeadingRule(StrictModel):
    id: str = Field(min_length=1, max_length=48)
    enabled: bool = True
    role: HeadingRole = "main"
    target_level: int = Field(2, ge=1, le=6)
    parent_rule: str | None = Field(default=None, max_length=48)
    priority: int = Field(50, ge=0, le=100)
    min_repeats: int = Field(2, ge=1, le=20)
    pattern: list[PatternToken] = Field(min_length=1, max_length=10)
    examples: list[str] = Field(default_factory=list, max_length=8)

    @field_validator("id", "parent_rule")
    @classmethod
    def strip_identifier(cls, value: str | None) -> str | None:
        return value.strip() if value is not None else None

    @field_validator("examples")
    @classmethod
    def dedupe_examples(cls, values: list[str]) -> list[str]:
        return _dedupe_strings(values)

    @model_validator(mode="after")
    def validate_pattern(self) -> "HeadingRule":
        title_indexes = [index for index, token in enumerate(self.pattern) if token.type == "title_text"]
        if len(title_indexes) > 1 or (title_indexes and title_indexes[0] != len(self.pattern) - 1):
            raise ValueError("title_text may appear once and must be the final token")
        return self


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
    heading_rules: list[HeadingRule] = Field(default_factory=list, max_length=24)
    heading_families: list[HeadingFamily] = Field(default_factory=list, max_length=32)
    metadata_rules: MetadataRules = Field(default_factory=MetadataRules)
    cleanup_rules: CleanupRules = Field(default_factory=CleanupRules)
    fallback_policy: FallbackPolicy = Field(default_factory=FallbackPolicy)
    safety_rules: SafetyRules = Field(default_factory=SafetyRules)
    strategy_source: Literal["qwen", "local", "default"] = "default"

    @model_validator(mode="after")
    def validate_heading_rule_graph(self) -> "CleaningStrategy":
        ids = [rule.id for rule in self.heading_rules]
        if len(ids) != len(set(ids)):
            raise ValueError("heading rule ids must be unique")
        family_ids = [family.id for family in self.heading_families]
        if len(family_ids) != len(set(family_ids)):
            raise ValueError("heading family ids must be unique")
        rules_by_id = {rule.id: rule for rule in self.heading_rules}
        for rule in self.heading_rules:
            if rule.parent_rule is None:
                continue
            parent = rules_by_id.get(rule.parent_rule)
            if parent is None:
                raise ValueError(f"unknown parent_rule: {rule.parent_rule}")
            if parent.target_level >= rule.target_level:
                raise ValueError("parent rule target level must be above child level")
        return self

    def to_dict(self) -> dict:
        return self.model_dump(mode="json")
