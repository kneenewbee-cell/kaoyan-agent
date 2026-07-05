from __future__ import annotations

import re
import logging
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

try:
    import jieba
except ImportError:  # pragma: no cover - dependency is declared, fallback keeps import safe.
    jieba = None

TOKENIZER_VERSION = "jieba_v7_domain_composite_aliases"
TOKEN_RE = re.compile(r"[A-Za-z0-9_]+|[\u4e00-\u9fff]+")
TOKEN_KEEP_RE = re.compile(r"^[A-Za-z0-9_]+$|^[\u4e00-\u9fff]+$")
STRUCTURED_LABEL_RE = re.compile(
    r"(?:\u8003\u70b9|\u5178\u578b|\u4f8b|\u9898\u578b|\u91cd\u96be\u70b9|\u6613\u9519\u70b9|\u51fa\u9898\u89d2\u5ea6|\u77e5\u8bc6\u7ec4)\s*"
    r"(?:[0-9]+|[\u4e00\u4e8c\u4e09\u56db\u4e94\u516d\u4e03\u516b\u4e5d\u5341\u767e]+)"
)
CONNECTOR_CHAR_RE = re.compile(r"[\u7684\u4e86\u5417\u5462\u554a\u5427\u548c\u4e0e\u53ca\u6216\u5bf9\u628a\u88ab\u4e3a\u4ece]+")
STRUCTURED_LABEL_WORDS = {
    "\u8003\u70b9",
    "\u5178\u578b",
    "\u4f8b",
    "\u9898\u578b",
    "\u91cd\u96be\u70b9",
    "\u6613\u9519\u70b9",
    "\u51fa\u9898\u89d2\u5ea6",
    "\u77e5\u8bc6\u7ec4",
}
QUERY_ALIASES = {
    "\u6cd5\u5236": ("\u6cd5\u5f8b", "\u6cd5\u6cbb"),
    "\u6cd5\u6cbb": ("\u6cd5\u5f8b",),
    "\u6cd5\u5f8b": ("\u6cd5\u6cbb",),
    "\u6b27\u62c9\u578b": ("\u6b27\u62c9\u65b9\u7a0b",),
    "\u975e\u9f50\u6b21\u65b9\u7a0b": ("\u975e\u9f50\u6b21\u7ebf\u6027\u5fae\u5206\u65b9\u7a0b", "\u5e38\u7cfb\u6570\u975e\u9f50\u6b21\u7ebf\u6027\u5fae\u5206\u65b9\u7a0b"),
    "\u53d8\u91cf\u53ef\u5206\u79bb": ("\u53ef\u5206\u79bb\u53d8\u91cf",),
    "\u77db\u76fe\u5206\u6790\u6cd5": ("\u77db\u76fe\u5206\u6790\u65b9\u6cd5", "\u5bf9\u7acb\u7edf\u4e00\u89c4\u5f8b"),
    "\u793e\u4f1a\u4e3b\u4e49\u672c\u8d28": ("\u4ec0\u4e48\u662f\u793e\u4f1a\u4e3b\u4e49", "\u600e\u6837\u5efa\u8bbe\u793e\u4f1a\u4e3b\u4e49"),
}
COMPOSITE_QUERY_ALIASES = (
    (
        ("\u9a6c\u514b\u601d\u4e3b\u4e49", "\u4e2d\u56fd"),
        ("\u9a6c\u514b\u601d\u4e3b\u4e49\u4e2d\u56fd\u5316", "\u9a6c\u514b\u601d\u4e3b\u4e49\u4e2d\u56fd\u5316\u65f6\u4ee3\u5316"),
    ),
    (
        ("\u793e\u4f1a\u4e3b\u4e49", "\u672c\u8d28"),
        ("\u793e\u4f1a\u4e3b\u4e49\u672c\u8d28", "\u4ec0\u4e48\u662f\u793e\u4f1a\u4e3b\u4e49", "\u600e\u6837\u5efa\u8bbe\u793e\u4f1a\u4e3b\u4e49"),
    ),
    (
        ("\u65b0\u6c11\u4e3b\u4e3b\u4e49\u9769\u547d", "\u4e09\u5927\u6cd5\u5b9d"),
        ("\u4e09\u5927\u6cd5\u5b9d", "\u65b0\u6c11\u4e3b\u4e3b\u4e49\u9769\u547d\u4e09\u5927\u6cd5\u5b9d"),
    ),
)
LEXICON_DIR = Path(__file__).resolve().parent / "lexicons"


@dataclass(frozen=True)
class QueryPlan:
    terms: tuple[str, ...]
    term_weights: dict[str, float]
    phrase_terms: tuple[str, ...]
    core_terms: tuple[str, ...]


def _read_lexicon(path: Path) -> tuple[str, ...]:
    if not path.exists():
        return ()
    terms: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        item = line.strip()
        if not item or item.startswith("#"):
            continue
        terms.append(item.lower())
    return tuple(dict.fromkeys(terms))


@lru_cache(maxsize=1)
def stopwords() -> tuple[str, ...]:
    return _read_lexicon(LEXICON_DIR / "stopwords_zh.txt")


@lru_cache(maxsize=1)
def domain_terms() -> tuple[str, ...]:
    terms = [
        *_read_lexicon(LEXICON_DIR / "domain_terms_math.txt"),
        *_read_lexicon(LEXICON_DIR / "domain_terms_politics.txt"),
    ]
    return tuple(sorted(dict.fromkeys(terms), key=len, reverse=True))


def _is_cjk(text: str) -> bool:
    return bool(re.fullmatch(r"[\u4e00-\u9fff]+", text or ""))


def _domain_terms_in_text(text: str) -> list[str]:
    lowered = (text or "").lower()
    selected: list[str] = []
    occupied_spans: list[tuple[int, int]] = []

    for term in domain_terms():
        if not term:
            continue
        start = 0
        while True:
            index = lowered.find(term, start)
            if index < 0:
                break
            span = (index, index + len(term))
            overlaps = any(max(span[0], used[0]) < min(span[1], used[1]) for used in occupied_spans)
            if not overlaps:
                selected.append(term)
                occupied_spans.append(span)
                break
            start = index + 1

    return selected


def _structured_label_terms_in_text(text: str) -> list[str]:
    terms: list[str] = []
    for match in STRUCTURED_LABEL_RE.finditer(text or ""):
        term = re.sub(r"\s+", "", match.group(0).lower())
        if term:
            terms.append(term)
    return list(dict.fromkeys(terms))


def _remove_stopword_phrases(text: str) -> str:
    cleaned = str(text or "")
    for phrase in sorted((item for item in stopwords() if len(item) > 1), key=len, reverse=True):
        cleaned = cleaned.replace(phrase, " ")
    return cleaned


def _drop_stopwords(tokens: list[str]) -> list[str]:
    stopword_set = set(stopwords())
    return [token for token in tokens if token not in stopword_set]


@lru_cache(maxsize=1)
def _configure_jieba() -> bool:
    if jieba is None:
        return False
    jieba.setLogLevel(logging.WARN)
    for term in [*domain_terms(), *STRUCTURED_LABEL_WORDS]:
        if term and _is_cjk(term):
            jieba.add_word(term, freq=2_000_000)
    return True


def _fallback_tokenize_raw(text: str) -> list[str]:
    tokens: list[str] = []
    for token in TOKEN_RE.findall(text or ""):
        token = token.strip().lower()
        if not token:
            continue
        if _is_cjk(token):
            for segment in CONNECTOR_CHAR_RE.split(token):
                if segment:
                    tokens.append(segment)
        else:
            tokens.append(token)
    return tokens


def _tokenize_raw(text: str) -> list[str]:
    if not _configure_jieba():
        return _fallback_tokenize_raw(text)

    tokens: list[str] = []
    for piece in jieba.cut(text or "", HMM=True):
        piece = piece.strip().lower()
        if not piece:
            continue
        if TOKEN_KEEP_RE.fullmatch(piece):
            tokens.append(piece)
            continue
        tokens.extend(match.group(0).lower() for match in TOKEN_RE.finditer(piece))
    return tokens


def _expand_query_aliases(tokens: list[str]) -> list[str]:
    expanded: list[str] = []
    seen: set[str] = set()
    for token in tokens:
        if token not in seen:
            expanded.append(token)
            seen.add(token)
        for alias in QUERY_ALIASES.get(token, ()):
            if alias not in seen:
                expanded.append(alias)
                seen.add(alias)
    return expanded


def _composite_alias_terms(text: str) -> tuple[str, ...]:
    compact = "".join((text or "").lower().split())
    aliases: list[str] = []
    for triggers, replacements in COMPOSITE_QUERY_ALIASES:
        if all(trigger in compact for trigger in triggers):
            aliases.extend(replacements)
    return tuple(dict.fromkeys(aliases))


def tokenize_document(text: str, *, drop_function_words: bool = True) -> list[str]:
    tokens = _tokenize_raw(text)
    if drop_function_words:
        tokens = _drop_stopwords(tokens)
    existing = set(tokens)
    for term in [*_structured_label_terms_in_text(text), *_domain_terms_in_text(text)]:
        if term not in existing:
            tokens.append(term)
            existing.add(term)
    return tokens


def _base_weight(term: str) -> float:
    if not term:
        return 0.0
    if term in stopwords():
        return 0.0
    if STRUCTURED_LABEL_RE.fullmatch(term):
        return 1.8
    if term in domain_terms():
        length = len(term)
        if length <= 3:
            return 1.25
        if length <= 6:
            return 1.55
        return 1.8
    if _is_cjk(term):
        length = len(term)
        if length == 1:
            return 0.15
        if length == 2:
            return 0.8
        if length == 3:
            return 1.0
        if length == 4:
            return 1.1
        return 1.0
    return 1.0


def process_query(query: str) -> QueryPlan:
    cleaned = _remove_stopword_phrases(query)
    raw_terms = _expand_query_aliases(_drop_stopwords(_tokenize_raw(cleaned)))
    structured_terms = tuple(_structured_label_terms_in_text(cleaned))
    composite_terms = _composite_alias_terms(cleaned)
    domain_term_set = set(domain_terms())
    phrase_terms = tuple(
        dict.fromkeys([
            *structured_terms,
            *composite_terms,
            *(term for term in _domain_terms_in_text(cleaned) if term not in stopwords()),
            *(term for term in raw_terms if term in domain_term_set and term not in stopwords()),
        ])
    )

    ordered_terms: list[str] = []
    term_weights: dict[str, float] = {}
    for term in [*phrase_terms, *raw_terms]:
        weight = _base_weight(term)
        if weight <= 0:
            continue
        if term not in term_weights:
            ordered_terms.append(term)
            term_weights[term] = weight
        else:
            term_weights[term] = max(term_weights[term], weight)

    if structured_terms:
        ordered_terms = [
            term
            for term in ordered_terms
            if not (term.isdigit() or term in STRUCTURED_LABEL_WORDS)
        ]
        term_weights = {term: weight for term, weight in term_weights.items() if term in ordered_terms}

    if any(_is_cjk(term) and len(term) > 1 for term in ordered_terms):
        ordered_terms = [term for term in ordered_terms if not (_is_cjk(term) and len(term) == 1)]
        term_weights = {term: weight for term, weight in term_weights.items() if term in ordered_terms}

    phrase_set = set(phrase_terms)
    core_terms = tuple(
        term
        for term in ordered_terms
        if term in phrase_set or (term_weights.get(term, 0.0) >= 1.0 and not (len(term) == 1 and _is_cjk(term)))
    )
    if not core_terms:
        core_terms = tuple(term for term in ordered_terms if not (len(term) == 1 and _is_cjk(term)))
    return QueryPlan(
        terms=tuple(ordered_terms),
        term_weights=term_weights,
        phrase_terms=phrase_terms,
        core_terms=core_terms,
    )


def tokenize_query(query: str) -> list[str]:
    return list(process_query(query).terms)
