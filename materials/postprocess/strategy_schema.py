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


class CleaningStrategy(StrictModel):
    version: str = "1.0"
    document_profile: DocumentProfile = Field(default_factory=DocumentProfile)
    main_section_rule: MainSectionRule = Field(default_factory=MainSectionRule)
    subsection_rules: list[SubsectionRule] = Field(default_factory=list)
    heading_rules: list[HeadingRule] = Field(default_factory=list, max_length=24)
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
