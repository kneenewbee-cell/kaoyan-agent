from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from qa.politics_rag import answer_politics_knowledge


OUT_DIR = ROOT / "data/runtime/current_affairs_eval"
OUT_DIR.mkdir(parents=True, exist_ok=True)


RUN_FILES = [
    ROOT / "data/runtime/current_affairs_eval/politics_second_layer_modes_20260625_162910.json",
    ROOT / "data/runtime/current_affairs_eval/politics_mode_paraphrase_20260625_163218.json",
]


SOURCES = {
    "meetings": [
        {
            "title": "中共中央政治局召开会议 分析研究当前经济形势和经济工作",
            "url": "https://www.news.cn/politics/leaders/20260428/002222d43f9e47d2947142a92e84a026/c.html",
            "source_domain": "news.cn",
            "published_at": "2026-04-28",
            "snippet": "中共中央政治局4月28日召开会议，分析研究当前经济形势和经济工作，强调实现“十五五”良好开局。",
            "text_preview": "会议强调坚持稳中求进，完整准确全面贯彻新发展理念，更好统筹国内国际两个大局，统筹发展和安全，推动科技自立自强、产业链自主可控，持续扩大内需、优化供给。",
            "confidence_hint": "high",
        },
        {
            "title": "李强主持召开国务院常务会议 研究推进全国统一大市场建设有关工作",
            "url": "https://credit.fgw.sh.gov.cn/ttxw/20260604/f077cc23c4d64f588ba16af3dfeaba08.html",
            "source_domain": "gov.cn-mirror",
            "published_at": "2026-05-21",
            "snippet": "国务院常务会议研究推进全国统一大市场建设，审议通过《现代化应急体系建设“十五五”规划》。",
            "text_preview": "会议指出建设全国统一大市场是构建新发展格局、推动高质量发展的需要，要完善产权保护、市场准入、公平竞争、社会信用、市场退出等制度，畅通经济循环。",
            "confidence_hint": "medium",
        },
        {
            "title": "习近平对常态化做好东西部协作工作作出重要指示",
            "url": "https://www.news.cn/politics/leaders/20260617/b4e2757ab8d84c2a85a5e0976305fef5/c.html",
            "source_domain": "news.cn",
            "published_at": "2026-06-17",
            "snippet": "习近平强调总结运用闽宁协作等经验，增强区域发展协调性，推动全体人民共同富裕迈出坚实步伐。",
            "text_preview": "要完善协作机制、优化协作方式、拓展协作领域，推动东西部产业互补、人员互动、技术互学、观念互通、作风互鉴，扎实推进乡村全面振兴。",
            "confidence_hint": "high",
        },
        {
            "title": "受权发布丨国家人权行动计划（2026－2030年）",
            "url": "https://www.news.cn/20260611/7c43e4a4e3fe4f419035f0dcdead9059/c.html",
            "source_domain": "news.cn",
            "published_at": "2026-06-11",
            "snippet": "国务院新闻办公室发布国家人权行动计划（2026－2030年）。",
            "text_preview": "行动计划强调全方位推进经济、社会和文化权利保障，并提出以数智技术创造美好生活、促进人的自由全面发展。",
            "confidence_hint": "high",
        },
    ],
    "ecology": [
        {
            "title": "中华人民共和国生态环境法典",
            "url": "https://www.mee.gov.cn/ywgz/fgbz/fl/202603/t20260313_1146496.shtml",
            "source_domain": "mee.gov.cn",
            "published_at": "2026-03-13",
            "snippet": "《中华人民共和国生态环境法典》于2026年3月12日第十四届全国人民代表大会第四次会议通过。",
            "text_preview": "法典包括总则、污染防治、生态保护、绿色低碳发展、法律责任等内容，体现生态环境保护系统化、法治化、规范化。",
            "confidence_hint": "high",
        },
        {
            "title": "关于《中华人民共和国生态环境法典（草案）》的说明（摘要）",
            "url": "https://www.moj.gov.cn/pub/sfbgw/zwgkztzl/2026nianzhuanti/2026qglh0206/lhjj20260206/lhjjyw20260206/202603/t20260306_532347.html",
            "source_domain": "moj.gov.cn",
            "published_at": "2026-03-06",
            "snippet": "说明介绍生态环境法典草案的编纂背景、总体要求和主要制度安排。",
            "text_preview": "草案编纂贯彻习近平生态文明思想，推进人与自然和谐共生的现代化，完善生态环境法律制度体系。",
            "confidence_hint": "high",
        },
        {
            "title": "行政法规制定程序条例",
            "url": "https://xzfg.moj.gov.cn/front/law/detail?LawID=1814",
            "source_domain": "moj.gov.cn",
            "published_at": "2026-05-15",
            "snippet": "《行政法规制定程序条例》2026年5月15日第二次修订。",
            "text_preview": "条例明确制定经济、文化、社会、生态文明等方面重大体制和重大政策调整的重要行政法规，应按规定及时报告党中央。",
            "confidence_hint": "medium",
        },
        {
            "title": "生态环境持续改善 美丽中国建设全面推进",
            "url": "https://www.stats.gov.cn/sj/sjjd/202606/t20260603_1963866.html",
            "source_domain": "stats.gov.cn",
            "published_at": "2026-06-03",
            "snippet": "国家统计局文章总结“十四五”时期生态文明建设成效。",
            "text_preview": "文章提到生态文明制度体系持续完善，协同推进降碳、减污、扩绿、增长，美丽中国建设框架体系逐步完善。",
            "confidence_hint": "medium",
        },
    ],
    "agriculture": [
        {
            "title": "2026年中央一号文件发布 部署扎实推进乡村全面振兴",
            "url": "https://www.spp.gov.cn/spp/tt/202602/t20260203_718061.shtml",
            "source_domain": "news.cn-mirror",
            "published_at": "2026-02-03",
            "snippet": "文件题为《中共中央 国务院关于锚定农业农村现代化 扎实推进乡村全面振兴的意见》。",
            "text_preview": "文件部署提升农业综合生产能力和质量效益、实施常态化精准帮扶、促进农民稳定增收、建设宜居宜业和美乡村、强化体制机制创新等任务。",
            "confidence_hint": "high",
        },
        {
            "title": "农业农村部部署落实中央一号文件重点工作",
            "url": "https://jcs.moa.gov.cn/gzdt/202602/t20260212_6481561.htm",
            "source_domain": "moa.gov.cn",
            "published_at": "2026-02-13",
            "snippet": "农业农村部提出2026年重点抓好八个方面工作。",
            "text_preview": "重点包括保障粮食等重要农产品稳定安全供给、巩固拓展脱贫攻坚成果、农业科技装备支撑、农业绿色转型、乡村富民产业、农村现代生活条件、深化农村改革等。",
            "confidence_hint": "high",
        },
        {
            "title": "国务院关于印发《加快农业农村现代化“十五五”规划》的通知",
            "url": "https://www.mee.gov.cn/zcwj/gwywj/202606/t20260603_1157890.shtml",
            "source_domain": "gov.cn-mirror",
            "published_at": "2026-06-03",
            "snippet": "国务院印发《加快农业农村现代化“十五五”规划》。",
            "text_preview": "规划提出“十五五”时期科学引领未来五年农业农村高质量发展，以加快农业农村现代化更好推进中国式现代化建设。",
            "confidence_hint": "high",
        },
        {
            "title": "习近平对常态化做好东西部协作工作作出重要指示",
            "url": "https://www.news.cn/politics/leaders/20260617/b4e2757ab8d84c2a85a5e0976305fef5/c.html",
            "source_domain": "news.cn",
            "published_at": "2026-06-17",
            "snippet": "习近平强调扎实推进乡村全面振兴，不断增强区域发展协调性。",
            "text_preview": "东西部协作要拓展协作领域，推动产业互补、人员互动、技术互学、观念互通、作风互鉴，推动共同富裕。",
            "confidence_hint": "high",
        },
    ],
    "bri": [
        {
            "title": "“一带一路”国际合作高峰论坛咨询委员会举行视频会议",
            "url": "https://www.mfa.gov.cn/web/wjb_673085/zzjg_673183/gjjjs_674249/xgxw_674251/202601/t20260127_11846213.shtml",
            "source_domain": "mfa.gov.cn",
            "published_at": "2026-01-27",
            "snippet": "会议发布题为《共建“一带一路”倡议——高质量的国际经济合作》的研究报告。",
            "text_preview": "外交部副部长马朝旭表示，共建“一带一路”国家致力于互联互通、共同发展，开展互利互惠国际合作，传递团结、合作、共赢信号。",
            "confidence_hint": "high",
        },
        {
            "title": "中华人民共和国国民经济和社会发展第十五个五年规划纲要",
            "url": "https://www.news.cn/politics/20260313/085af5de5a4b4268aa7d87d90817df2f/c.html",
            "source_domain": "news.cn",
            "published_at": "2026-03-13",
            "snippet": "纲要提出创新“一带一路”合作模式，完善立体互联互通网络布局。",
            "text_preview": "纲要提出深化重要经济走廊和支点港口合作，提升中欧（亚）班列发展水平，高质量建设中吉乌铁路、匈塞铁路等项目，全面提升务实合作质效。",
            "confidence_hint": "high",
        },
        {
            "title": "以高质量共建“一带一路”助推周边命运共同体建设",
            "url": "https://paper.people.com.cn/rmrb/pc/content/202604/08/content_30149816.html",
            "source_domain": "people.com.cn",
            "published_at": "2026-04-08",
            "snippet": "人民日报文章阐释高质量共建“一带一路”与周边命运共同体建设。",
            "text_preview": "文章强调标志性工程和“小而美”民生项目并重，推动硬联通、软联通、心联通，体现正确义利观和合作共赢。",
            "confidence_hint": "medium",
        },
    ],
    "china_us": [
        {
            "title": "2026年6月18日外交部发言人林剑主持例行记者会",
            "url": "https://www.mfa.gov.cn/web/fyrbt_673021/202606/t20260618_11948460.shtml",
            "source_domain": "mfa.gov.cn",
            "published_at": "2026-06-18",
            "snippet": "外交部记者会主要涉及美伊谅解备忘录、中东和平稳定、金砖国家安全事务高级代表会议等内容。",
            "text_preview": "该来源未显示2026年6月18日中美举行重要会谈；涉及中方欢迎美伊签署谅解备忘录，并表示继续为中东和平稳定发挥建设性作用。",
            "confidence_hint": "high",
        },
        {
            "title": "韩正会见美国前运输部长赵小兰",
            "url": "https://www.mfa.gov.cn/wjb_673085/zzjg_673183/xws_674681/xgxw_674683/",
            "source_domain": "mfa.gov.cn",
            "published_at": "2026-06-17",
            "snippet": "外交部相关新闻列表显示韩正会见美国前运输部长赵小兰。",
            "text_preview": "该条是中美人员交往相关信息，但不等同于2026年6月18日中美重要会谈。",
            "confidence_hint": "medium",
        },
        {
            "title": "习近平同美国总统特朗普会谈",
            "url": "https://paper.people.com.cn/rmrb/pc/content/202605/15/content_30156964.html",
            "source_domain": "people.com.cn",
            "published_at": "2026-05-15",
            "snippet": "习近平同美国总统特朗普会谈，双方赞同将构建“中美建设性战略稳定关系”作为中美关系新定位。",
            "text_preview": "来源显示中美元首会谈发生在2026年5月，不是6月18日；可作为用户可能混淆日期时的参照。",
            "confidence_hint": "high",
        },
    ],
    "sco": [
        {
            "title": "上海合作组织峰会",
            "url": "https://www.mfa.gov.cn/web/gjhdq_676201/gjhdqzz_681964/lhg_683094/jbqk_683096/201404/t20140430_9388210.shtml",
            "source_domain": "mfa.gov.cn",
            "published_at": "2026-06-15",
            "snippet": "外交部资料显示，2025年9月1日上合组织成员国元首理事会第二十五次会议在天津举行。",
            "text_preview": "会议批准《上海合作组织未来10年（2026-2030年）发展战略》，通过安全、经济、人文合作和组织建设等成果文件。",
            "confidence_hint": "high",
        },
        {
            "title": "王毅出席上海合作组织成立25周年招待会",
            "url": "https://www.mfa.gov.cn/wjbzhd/202606/t20260615_11946002.shtml",
            "source_domain": "mfa.gov.cn",
            "published_at": "2026-06-15",
            "snippet": "王毅表示天津峰会擘画了上合组织未来10年发展蓝图，今年比什凯克峰会将进一步凝聚各方共识。",
            "text_preview": "王毅强调弘扬“上海精神”，完善全球治理，维护和平安宁，促进可持续发展，增进睦邻友好合作。",
            "confidence_hint": "high",
        },
        {
            "title": "习近平主持上海合作组织成员国元首理事会第二十五次会议并发表重要讲话",
            "url": "https://www.news.cn/20250901/eaa25ef544874a13be39d1a6534008e4/c.html",
            "source_domain": "news.cn",
            "published_at": "2025-09-01",
            "snippet": "习近平主持上合组织天津峰会并发表题为《牢记初心使命 开创美好未来》的重要讲话。",
            "text_preview": "讲话强调弘扬“上海精神”，坚持求同存异、互利共赢、开放包容、公平正义、务实高效。",
            "confidence_hint": "high",
        },
    ],
    "jun18": [
        {
            "title": "新闻背景丨美以伊战事时间线",
            "url": "https://www.news.cn/world/20260618/811efa4644f14fbf9f8c9abaa6313418/c.html",
            "source_domain": "news.cn",
            "published_at": "2026-06-18",
            "snippet": "北京时间6月18日，美国和伊朗宣布远程签署谅解备忘录。",
            "text_preview": "新华社梳理美以伊战事时间线，提到美伊谅解备忘录立即生效，伊朗重新开放霍尔木兹海峡，美国解除海上封锁。",
            "confidence_hint": "high",
        },
        {
            "title": "2026年6月18日外交部发言人林剑主持例行记者会",
            "url": "https://www.mfa.gov.cn/web/fyrbt_673021/202606/t20260618_11948460.shtml",
            "source_domain": "mfa.gov.cn",
            "published_at": "2026-06-18",
            "snippet": "外交部回应美伊签署谅解备忘录及中方促和努力。",
            "text_preview": "发言人表示中方欢迎美伊双方签署谅解备忘录，将继续为实现中东海湾地区长治久安发挥积极和建设性作用。",
            "confidence_hint": "high",
        },
        {
            "title": "为世界政治文明发展进步贡献中国智慧——习近平党建思想引发国际社会热议",
            "url": "https://www.news.cn/politics/leaders/20260619/fa366b6b90184c0fa796d681ff1881d8/c.html",
            "source_domain": "news.cn",
            "published_at": "2026-06-19",
            "snippet": "新华社北京6月18日电，全国党建工作座谈会15日在北京召开，习近平党建思想引发国际社会热议。",
            "text_preview": "该稿围绕习近平党建思想的国际反响，适合归入6月中旬国内政治时政积累。",
            "confidence_hint": "medium",
        },
    ],
    "central_economic_work": [
        {
            "title": "中央经济工作会议在北京举行 习近平发表重要讲话",
            "url": "https://www.news.cn/politics/leaders/20251211/a583f835702d4dc2b8990ddee4644e92/c.html",
            "source_domain": "news.cn",
            "published_at": "2025-12-11",
            "snippet": "中央经济工作会议12月10日至11日在北京举行，习近平总结2025年经济工作，分析当前经济形势，部署2026年经济工作。",
            "text_preview": "会议要求完整准确全面贯彻新发展理念，加快构建新发展格局，推动高质量发展，统筹发展和安全，因地制宜发展新质生产力，纵深推进全国统一大市场建设。",
            "confidence_hint": "high",
        },
        {
            "title": "中央财办有关负责同志详解2025年中央经济工作会议精神",
            "url": "https://www.news.cn/20251216/7721c4193d62414aba876e00024137ee/c.html",
            "source_domain": "news.cn",
            "published_at": "2025-12-16",
            "snippet": "中央财办有关负责同志解读中央经济工作会议精神和2026年经济重点任务。",
            "text_preview": "解读强调稳中求进、提质增效，围绕内需主导、创新驱动、改革攻坚、民生为大等任务推进“十五五”开局。",
            "confidence_hint": "high",
        },
    ],
    "digital_village": [
        {
            "title": "2026年中央一号文件发布 部署扎实推进乡村全面振兴",
            "url": "https://www.spp.gov.cn/spp/tt/202602/t20260203_718061.shtml",
            "source_domain": "news.cn-mirror",
            "published_at": "2026-02-03",
            "snippet": "中央一号文件部署锚定农业农村现代化、扎实推进乡村全面振兴。",
            "text_preview": "文件围绕农业农村现代化、乡村全面振兴和强农惠农富农政策部署，适合支撑数字经济赋能乡村振兴的政策背景。",
            "confidence_hint": "high",
        },
        {
            "title": "国务院关于印发《加快农业农村现代化“十五五”规划》的通知",
            "url": "https://www.mee.gov.cn/zcwj/gwywj/202606/t20260603_1157890.shtml",
            "source_domain": "gov.cn-mirror",
            "published_at": "2026-06-03",
            "snippet": "国务院印发农业农村现代化“十五五”规划。",
            "text_preview": "规划为未来五年农业农村高质量发展提供部署，可作为数字乡村、智慧农业、农村现代化的政策背景。",
            "confidence_hint": "high",
        },
    ],
}


THEORY_CHUNKS = {
    "dialectics": [
        "唯物辩证法强调联系、发展、矛盾。联系观要求从整体上把握事物之间相互影响、相互制约的关系；发展观要求看到事物由量变到质变、前进性与曲折性的统一；矛盾分析法要求坚持两点论和重点论统一，具体问题具体分析。",
        "矛盾具有普遍性和特殊性。普遍性说明矛盾存在于一切事物发展过程中；特殊性要求具体问题具体分析。主要矛盾和矛盾主要方面要求抓住重点，同时兼顾次要方面。",
    ],
    "marxism": [
        "马克思主义基本原理可从物质与意识、实践与认识、社会存在与社会意识、生产力与生产关系、经济基础与上层建筑、人民群众是历史创造者等角度分析现实材料。",
        "分析题中要避免抽象堆砌原理，应按“材料事实—对应原理—规范表述”组织，把事实中的主体、矛盾、政策目标和实现路径对应到相应原理。",
    ],
    "development": [
        "新发展理念包括创新、协调、绿色、开放、共享，是推动高质量发展的指导原则。高质量发展强调质量变革、效率变革、动力变革，发展新质生产力要以科技创新为核心驱动力。",
        "乡村振兴总要求包括产业兴旺、生态宜居、乡风文明、治理有效、生活富裕。农业农村现代化要坚持农业农村优先发展、城乡融合发展和共同富裕方向。",
    ],
    "politics_exam": [
        "考研政治主观题答法通常按“原理/考点—材料对应—意义/做法”组织。若题干只给抽象材料，应优先调动稳定理论框架；若题干要求结合真实时政，应先核验事实再映射理论。",
        "答题语言要规范，避免只列关键词。每个角度最好写出“为什么相关”和“能怎样写进答案”。",
    ],
}


def load_cases() -> list[dict]:
    cases: list[dict] = []
    for path in RUN_FILES:
        cases.extend(json.loads(path.read_text(encoding="utf-8")))
    return cases


def select_source_keys(question: str, query: str) -> list[str]:
    text = f"{question} {query}"
    keys: list[str] = []
    if "中央经济工作会议" in text:
        keys.append("central_economic_work")
    if any(word in text for word in ["中美", "美国", "会谈", "接触"]):
        keys.append("china_us")
    if any(word in text for word in ["上合", "上海合作组织"]):
        keys.append("sco")
    if any(word in text for word in ["一带一路"]):
        keys.append("bri")
    if any(word in text for word in ["生态", "环保", "环境法典", "法案", "法典"]):
        keys.append("ecology")
    if any(word in text for word in ["农业", "农村", "乡村", "三农", "数字经济"]):
        keys.append("agriculture")
    if any(word in text for word in ["数字经济", "数字乡村", "乡村振兴"]):
        keys.append("digital_village")
    if any(word in text for word in ["6月18", "6月 18", "六月十八", "中旬"]):
        keys.append("jun18")
    if any(word in text for word in ["会议", "大事", "时政", "五六月", "最近两月", "过去两个月", "国家层面"]):
        keys.append("meetings")
    if not keys:
        keys.append("meetings")
    return list(dict.fromkeys(keys))


def current_affairs_evidence(question: str, query: str) -> dict:
    items: list[dict] = []
    for key in select_source_keys(question, query):
        for item in SOURCES[key]:
            if item["url"] not in {existing["url"] for existing in items}:
                item_copy = dict(item)
                item_copy["query"] = query
                items.append(item_copy)
    return {
        "type": "current_affairs_evidence",
        "query": query,
        "items": items[:6],
        "warnings": [],
        "manual_search_role": True,
        "manual_search_note": "本次评测为节省项目新闻搜索 API，由 Codex 根据权威域名检索结果临时构造 evidence。",
    }


def theory_evidence(query: str) -> list[dict]:
    text = query
    buckets: list[str] = []
    if any(word in text for word in ["辩证", "矛盾", "联系", "发展", "马原", "哲学"]):
        buckets.extend(["dialectics", "marxism"])
    if any(word in text for word in ["乡村", "农业", "数字经济", "新质", "高质量", "一带一路", "经济", "生态"]):
        buckets.extend(["development", "politics_exam"])
    if not buckets:
        buckets.extend(["marxism", "politics_exam"])
    chunks = []
    for bucket in dict.fromkeys(buckets):
        for content in THEORY_CHUNKS[bucket]:
            chunks.append({
                "content": content,
                "heading_path": ["考研政治", bucket],
                "score": 9.0,
                "query": query,
            })
    return chunks[:5]


def build_tool_outputs(case: dict) -> tuple[list[dict], list[str]]:
    outputs: list[dict] = []
    source_urls: list[str] = []
    question = case["question"]
    for record in case.get("executed_records") or []:
        name = record.get("name")
        query = str(record.get("query") or question)
        if name == "get_current_affairs":
            evidence = current_affairs_evidence(question, query)
            source_urls.extend(item["url"] for item in evidence["items"])
            outputs.append({"tool": name, "content": json.dumps(evidence, ensure_ascii=False)})
        elif name == "search_politics_knowledge":
            outputs.append({"tool": name, "content": json.dumps(theory_evidence(query), ensure_ascii=False)})
    return outputs, list(dict.fromkeys(source_urls))


def answer_mode(case: dict) -> str:
    for record in case.get("executed_records") or []:
        if record.get("name") == "answer_politics_knowledge":
            return str(record.get("mode") or case.get("second_layer_mode") or "auto")
    return str(case.get("second_layer_mode") or "auto")


def main() -> None:
    cases = load_cases()
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results = []
    for index, case in enumerate(cases, start=1):
        mode = answer_mode(case)
        tool_outputs, source_urls = build_tool_outputs(case)
        answer = ""
        for attempt in range(2):
            answer = answer_politics_knowledge(
                question=case["question"],
                tool_outputs=json.dumps(tool_outputs, ensure_ascii=False),
                mode=mode,
                output_format="ui",
            )
            if answer.strip():
                break
        result = {
            "index": index,
            "case_id": case["case_id"],
            "case_type": case["case_type"],
            "question": case["question"],
            "expected_mode": case["expected_mode"],
            "second_layer_mode": case.get("second_layer_mode"),
            "answer_mode": mode,
            "executed_records": case.get("executed_records") or [],
            "source_urls": source_urls,
            "answer": answer,
        }
        results.append(result)
        print(f"[{index:02d}/{len(cases)}] {case['case_id']} mode={mode} answer_chars={len(answer)}")

    json_path = OUT_DIR / f"politics_answer_32_manual_news_{stamp}.json"
    json_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")

    md_lines = [
        "# Politics Answer 32 Manual News Eval",
        "",
        f"- generated_at: {datetime.now().isoformat(timespec='seconds')}",
        "- current_affairs: manual Codex web evidence, not project news API",
        "- answer_llm: qa.politics_rag.answer_politics_knowledge",
        "",
    ]
    for result in results:
        md_lines.extend([
            f"## {result['index']:02d}. {result['case_id']}",
            "",
            f"- question: {result['question']}",
            f"- expected_mode: {result['expected_mode']}",
            f"- second_layer_mode: {result['second_layer_mode']}",
            f"- answer_mode: {result['answer_mode']}",
            "- tools: "
            + " -> ".join(record.get("name", "") for record in result["executed_records"]),
            "- sources: "
            + ("; ".join(result["source_urls"]) if result["source_urls"] else "none"),
            "",
            result["answer"].strip(),
            "",
        ])
    md_path = OUT_DIR / f"politics_answer_32_manual_news_{stamp}.md"
    md_path.write_text("\n".join(md_lines), encoding="utf-8")
    print(f"SAVED_JSON {json_path}")
    print(f"SAVED_MD {md_path}")


if __name__ == "__main__":
    main()
