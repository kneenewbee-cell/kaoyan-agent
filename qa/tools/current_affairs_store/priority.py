from __future__ import annotations


P0_OFFICIAL = {
    "gov.cn",
    "npc.gov.cn",
    "cppcc.gov.cn",
    "mfa.gov.cn",
    "moa.gov.cn",
    "moj.gov.cn",
    "ndrc.gov.cn",
    "mee.gov.cn",
    "mofcom.gov.cn",
    "moe.gov.cn",
    "miit.gov.cn",
    "mps.gov.cn",
    "chinacourt.gov.cn",
    "spp.gov.cn",
    "weforum.org",
}

P1_AUTHORITATIVE_MEDIA = {
    "news.cn",
    "xinhuanet.com",
    "people.com.cn",
    "paper.people.com.cn",
    "cctv.com",
    "cctv.cn",
    "cntv.cn",
    "china.com.cn",
}

P4_CLUE_ONLY = {
    "chinanews.com",
    "thepaper.cn",
    "caixin.com",
    "yicai.com",
}


def clean_domain(domain: str) -> str:
    return str(domain or "").strip().lower().removeprefix("www.")


def source_priority(domain: str, category: str | None = None) -> int:
    clean = clean_domain(domain)
    category = str(category or "").strip()
    if clean in P0_OFFICIAL:
        return 100 + category_boost(clean, category)
    if clean in P1_AUTHORITATIVE_MEDIA:
        return 80 + category_boost(clean, category)
    if clean.endswith(".gov.cn"):
        return 70
    if any(clean.endswith("." + item) for item in P1_AUTHORITATIVE_MEDIA):
        return 65
    if clean in P4_CLUE_ONLY:
        return 40
    return 20


def category_boost(domain: str, category: str) -> int:
    if category == "law_or_draft" and domain in {"npc.gov.cn", "moj.gov.cn"}:
        return 12
    if category == "policy_document" and domain == "gov.cn":
        return 12
    if category == "international_event" and domain in {"mfa.gov.cn", "weforum.org"}:
        return 12
    if category == "agriculture_rural" and domain == "moa.gov.cn":
        return 12
    return 0
