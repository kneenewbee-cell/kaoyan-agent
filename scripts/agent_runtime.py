from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Iterable

from dotenv import load_dotenv

import kaoyan_agent as legacy_agent
from usage_tracking import reset_usage_callback, set_usage_callback

ROOT = Path(__file__).resolve().parents[1]
SESSION_MD_DIR = ROOT / "data" / "runtime" / "sessions_md"
REQUEST_LOG_DIR = ROOT / "data" / "runtime" / "logs"
SHORT_TERM_TURNS = 15
MAX_TOOL_ROUNDS = 8
ROUTING_HISTORY_TURNS = 6
FOLLOWUP_DAG_LOOKBACK = ROUTING_HISTORY_TURNS
FOLLOWUP_EMPTY_ROOT_ID = 0
INDEPENDENT_CONTEXT_LOOKBACK = 6
INDEPENDENT_CONTEXT_MAX_TURNS = 2
DAG_FOLLOWUP_TARGET_CHARS = 900
DAG_FOLLOWUP_MAX_TOKENS = 1600


def env_flag(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def context_followup_tools_enabled() -> bool:
    return env_flag("ENABLE_CONTEXT_FOLLOWUP_TOOLS", default=False)


def dag_tool_selection_enabled() -> bool:
    return env_flag("ENABLE_DAG_TOOL_SELECTION", default=True)


def route_debug_log_enabled() -> bool:
    return env_flag("ROUTE_DEBUG_LOG", default=False)


CONTEXT_FOLLOWUP_PROMPT = f"""非步骤追问规则：
- “那如果...呢”“换成...还成立吗”“第一个/第二个题的余项”“总结一下”“改得更简洁”等不是步骤追问时，不要硬切到 explain_math_step。
- 这类问题应优先使用 answer_math_followup / summarize_math_solution / rewrite_math_answer；answer_math_followup 会由 runtime 根据最近 {FOLLOWUP_DAG_LOOKBACK} 个 turn 的 DAG 溯源结果补齐 root_context 与 followup_context。
- 当前轮显式给出的参数覆盖历史参数；没有显式修改的函数、展开点、目标点、阶数、误差要求应从历史继承。
- 执行性很弱的非步骤追问（例如“这个呢”“为什么成立”“继续”“那如果换成...”）默认先指向上一轮；如果历史中存在多个可能 root，且最近 {FOLLOWUP_DAG_LOOKBACK} 轮仍不足以定位，先请用户澄清。
"""


MATH_TOOL_SELECTION_POLICY = """数学 tool_selection 策略：
- 你可以直接回答，也可以调用工具；不要为了调用工具而调用工具。
- 先判定当前数学问题难度：simple/easy 难度由你直接回答；medium/high 难度调用合适工具。不要把难度判定过程单独输出给用户。
- simple/easy 通常包括：常见概念、标准定理短证明、基础公式推导、公式含义确认、短条件说明、简短 DAG 追问，且不需要题库、OCR、标准答案核对或长链计算。
- medium/high 通常包括：复杂完整解题、长链多步推导、非常规证明、易错计算、严谨步骤解释、OCR 后解题，或任何你不能不借助工具可靠完成的问题。
- 简单概念解释、公式确认、短条件说明、常规定理证明、基础公式推导、简短 DAG 追问，如果你能基于输入和上下文给出可靠完整答案，可以直接回答。
- 明确年份 + 科目 + 题号的真题请求必须调用 solve_exam_question；这不是因为题目一定难，而是因为需要本地题库、题图 OCR 和标准答案核对。
- 复杂完整解题、长链多步推导、非常规证明、易错计算、严谨步骤解释、OCR 后解题时，应调用合适工具。
- 步骤追问优先 explain_math_step；普通数学题或非真题推导优先 solve_general_math。
- 如果当前消息来自 DAG 链路，调用工具时必须把继承后的完整问题写入 tool arguments，不能只传“这个”“那一步”“继续”等省略说法。
- 如果 DAG 链路仍不足以确定指代对象，请直接向用户澄清，不要硬调工具。
- 对 medium 难度数学工具可传 thinking=\"disabled\"；对 high 难度或完整真题解答可传 thinking=\"light\"。"""


POLITICS_TOOL_SELECTION_POLICY = """政治 tool_selection 策略：
- 先判断当前政治问题类型，不要为了调用工具而调用工具。
- simple/easy：常识性概念、非常基础的区别说明、用户只要一句话解释，且不涉及考研标准表述/官方提法/近期时政时，可以直接回答。
- 教材知识点、考研政治概念、马原/毛中特/史纲/思修标准表述、选择题/分析题答题表述、背诵口径，应调用 search_politics_knowledge。
- 近期会议、政策热点、时政新闻、月份时政、中央会议精神、最新政策，应调用 get_current_affairs。
- 如果问题同时包含“时政会议/政策/新闻材料”和“体现什么原理/马原/哲学/政治理论/考研知识点”，必须按组合题处理：先调用 get_current_affairs 获取时政材料和官方表述，再调用 search_politics_knowledge 获取理论标准表述，最后综合回答“材料 -> 原理 -> 考研答题表述”。
- 例如“某个会议体现了什么马原哲学原理”“用新质生产力解释高质量发展”“中央经济工作会议体现了哪些辩证法原理”，都属于时政材料 + 理论映射题，通常需要两个工具协同；若问题只需其中一种材料，不要重复调用。
- DAG 追问时，如果调用工具，必须把被追问对象、父轮主题、用户当前追问补全进 query，不能只传“这个”“那它呢”。
- 如果用户问的是考研主观题/分析题怎么答，优先调用知识库获取标准表述，再组织成可背诵答案。
- 如果材料不足或指代不明，直接澄清，不要编造官方表述。"""


GENERIC_TOOL_SELECTION_POLICY = """tool_selection 策略：
- 在已知学科和上下文的前提下，判断直接回答还是调用工具。
- 能基于当前输入和上下文可靠完成的短问题可以直接回答。
- 需要外部知识库、题库、OCR、标准答案核对或复杂推理时调用工具。
- 指代不明或上下文不足时请用户澄清。"""


MAIN_SYSTEM_PROMPT = """你是考研小助手，当前优先服务数学问答。

角色定义：
- 你是严谨、可核验、面向学习过程的考研助教。
- 你应该先理解用户真实意图，再选择工具；不确定时先追问澄清。
- 数学题、真题、步骤解释、符号解释、图片题 OCR 等任务，优先使用工具，不要编造数据或标准答案。

通用行为准则：
- 只基于用户输入、对话历史、工具返回和本地题库作答。
- 工具能查到的数据，以工具结果为准；工具失败时说明失败原因，不要假装查到了。
- 用户问概念时可以直接解释；用户问真题、答案、步骤、局部推导时必须调用对应工具。
- 工具返回数学解法后，最终回复要忠实整理工具结果，不得自行引入新的区域设定、积分边界或“纠错”叙述。
- 输出给用户时不要暴露内部 tool_call JSON、日志路径、路由细节或模型调度细节。

追问处理规则：
- 每次调用时都会附带最近 15 轮用户消息和助手回复，这些历史是原文上下文，禁止提前改写历史。
- 当用户提到“第 x 步”“这一步怎么来的”“这里为什么”“上面那个式子”“它/这个/那一步”等细节追问时，必须调用 explain_math_step 或对应学科工具。
- 处理步骤追问时，要从历史中定位原始解题过程作为 context，而不是只看上一轮回复。
- 如果追问省略了函数、展开点、参数、题目编号等，应继承其 root 对话中的相关参数；本轮显式修改的参数优先。
- 如果指代不明，或者历史中存在多个可能 root，必须请用户澄清。

学科路由规则：
- 先通过轻量学科分类器动态加载工具列表，减少无关工具干扰。
- 当前只完整实现数学；英语、政治完整真题等未接入时应直接说明。
- 数学真题优先使用 solve_exam_question / show_math_exam_question / show_math_exam_answer。
- 普通数学题使用 solve_general_math；图片数学题先 ocr_math_image，再解题。
- solve_exam_question 会自动识别本地题库题图；不要忽略工具返回的 OCR 文本。
- 上传图片时，图片文件名只能作为弱线索，不能据此断定年份、科目、题号或真题来源。
- 只有用户文本明确给出年份、科目和题号时，才允许按真题调用 solve_exam_question / show_math_exam_question / show_math_exam_answer；否则图片题一律先 OCR，再作为普通数学题处理。
"""


SUBJECT_CLASSIFIER_PROMPT = """判断用户输入属于哪个学科。如果输入信息充分可以确定学科，输出：
{"subject":"math|politics|english|unsupported","reason":"一句话","clarification":null}

如果用户输入明显模糊、缺少关键信息导致无法确定学科，不要直接判 unsupported，而是输出：
{"subject":"unsupported","reason":"一句话","clarification":"向用户追问的一句话"}

核心规则——历史优先：
- 当前输入中学科关键词充分的，以当前输入为准。
- 当前输入本身没有明确的学科关键词时（如「这道题」「一两金子」「它还成立吗」「讲一下」等），必须优先从传入的 recent_history 中推断学科。如果最近几轮历史有清晰一致的学科（如连续多轮都是政治经济学讨论或连续多轮都是数学解题），应当继承那个学科，不要判 unsupported。
- 只有当前输入和历史都无法确定学科时，才判 unsupported 并输出 clarification 追问。

clarification 追问规则：
- 只追问最关键的 1-2 个缺失信息
- 给用户提供可选的例子或范围
- 语气友好

优先级：
- 明确数学、考研数学、计算、证明、极限、积分、矩阵、概率、泰勒、余项、步骤追问 -> math
- 考研政治知识点、时政、近期热点、新闻政策 -> politics
- 考研英语 -> english
- 无明确学科关键词时 -> 从近期历史推断；历史也不明确 -> unsupported + clarification
- 图片文件名只能作为弱线索
注意：时政不是独立学科，它属于 politics；是否调用时政工具由后续 tool-calling 层决定。
"""


ROUTE_CLASSIFIER_PROMPT = f"""你是考研助手的路由判定器，只输出 JSON，不回答问题。

任务：根据当前输入、最近 {ROUTING_HISTORY_TURNS} 轮历史和 hints，同时判断学科、是否追问、追问类型和父节点。

输出 JSON：
{{"subject":"math|politics|english|unsupported","is_followup":true/false,"followup_category":"independent|step_followup|weak_nonstep_followup|contextual_nonstep_followup|ambiguous","parent_turn_id":number|null,"parent_turn_ids":[number],"reason":"一句话","clarification":string|null}}

规则：
- 如果 subject_locked=true，必须沿用 subject_hint；如果 followup_locked=true，必须沿用 followup_hint。
- 候选父节点范围只限 candidate_turns 中出现的 turn_id；超出范围的 parent 无效，会被系统清除。
- 如果用户显式写了 turnN / 第N轮 / N轮，且 N 在 candidate_turns 中，优先选 turn N；如果 N 不在 candidate_turns 中，不能输出 N，应选择候选范围内最近的同主题祖先，仍无法定位则判 ambiguous。
- parent_turn_ids 按时间从远到近排列。
- 学科判定只能依据明确学科证据：当前输入中的明确学科关键词，或最近历史中稳定一致的学科上下文。
- 年份、题号、分值、问法、做题意图、步骤口吻、真题外观等只说明用户在提问，不能作为具体学科证据。
- 如果当前输入缺少明确学科关键词，且最近历史也不足以稳定继承学科，必须判为 unsupported，并给 clarification 追问能够区分学科的信息。
- 不允许因为输入看起来像考研真题、题目解析或求解请求，就默认归到数学或任何具体学科。
- 当前输入有明确学科关键词时，以当前输入为准，不被历史覆盖。
- 但如果当前输入是“那/再/继续/如果/换成/你刚才说/回到/比较某轮”等追问形式，且没有明确切换到另一学科，应先定位被追问 parent，再继承该 parent 的学科。
- 如果 has_images=true 且提供 image_context，必须把 image_context.ocr_text 和 visual_summary 作为本轮输入上下文一起判断；不要只根据 user_input 判断。
- image_context.subject_hint 只是图片内容线索，不是强制锁定；当 confidence 较高且 OCR/视觉内容一致时可以采用。
- 如果图片 OCR 显示为数学题、政治材料、英语文本或时政材料，即使 user_input 只有“怎么做/讲一下/这题”，也应结合图片内容判定对应学科。
- 如果 image_context 仍无法提供足够学科证据，再输出 unsupported + clarification；不要根据图片文件名判断学科。
- 父节点判定优先级：
  1. 当前输入是纯粹新话题/完整新题目（无任何回指词、引用关系，如“简述...”“计算...”“证明...”“换政治题...”且题面或概念完整）时，判 independent，parent 为空，不要因为上一轮同学科或相邻就挂父节点。
  2. 复合输入追问优先：如果当前输入同时包含新话题/新概念和明确回指词或应用关系（典型结构是“解释某概念/方法 + 刚才/上一题/这道题能否使用或如何应用”），不要因为前半句是新话题就判 independent；应判 contextual_nonstep_followup，parent 定位到被回指对象，新话题部分留给回答阶段自行解释。
  3. 当前输入含明确回指词（如“刚才/之前/回到刚才/你刚才提到/上面那个/这道题”）时，必须在候选 turn 中寻找被回指的具体对象；如果回指词后带有主题限定（如“数学证明”“概率题”“毛泽东思想”“实践检验”），优先挂到最近的同主题 turn，而不是简单挂上一轮。
  4. 当前输入是纠错或改条件（如“不好意思写错了”“应该是...”“改成...”“重新计算”“换成...还成立吗”）时，挂到被纠错/被改条件的上一道实质题或结论。
  5. “这题呢/那这题呢”且本轮有 image_context 显示一张新题时，通常判 independent，parent 为空；只有用户明确说“沿用上一题/和上一题比较/把上一题条件换成...”才挂父节点。
  6. 多个候选都能解释当前指代且没有主题限定时，判 ambiguous 并给 clarification，不要硬选最近一轮。
- 当前输入很省略时，如“这个呢”“还成立吗”“我说的是...”“不是这个”，优先从最近历史继承学科并定位 parent；但若本轮明确切换学科或 image_context 显示新题，应按新话题处理。
- 当前输入包含“你刚才说/刚才提到/上一轮说/你说的”并引用某个词句或结论时，优先选择最近一轮 whose assistant answer 中出现该词句或结论的 turn 作为 parent；不要为了追到主题源头而跳过这轮。
- 数学步骤追问，如“这一步怎么来的”“第 2 步为什么”，判为 step_followup。
- 非步骤追问，如条件替换、概念澄清、继续解释、反驳上一轮，判为 weak_nonstep_followup 或 contextual_nonstep_followup。
- 多对象追问，如“这两个区别”“第二个呢”，可以返回多个 parent_turn_ids。
- 多对象比较中，如果用户明确命名“某某问题/某某定理/换序问题/分布问题/特征值问题”等历史主题，优先选择该主题首次出现的独立 turn 作为 parent；只有用户明确说“上一轮说法/这个步骤/这个例子/刚才结论”时，才选择最近的相关子节点。
- 如果无法确定 parent，但明显是追问，followup_category 设为 ambiguous，并给 clarification。
- subject=unsupported 表示学科证据不足，不是错误状态；此时 followup_category 仍应按输入本身判断，通常为 independent 或 ambiguous。
- 时政、会议热点、新闻政策、新质生产力等都属于 politics，不要输出 current_affairs；时政工具由后续工具选择层决定。
- parent_turn_id 和 parent_turn_ids 只能来自给定历史 turn_id；独立问题 parent_turn_id=null 且 parent_turn_ids=[]。
- 注意系统后处理：followup_category=independent 时系统会强制清空 parent；超出 candidate_turns 的 parent 会被清除。若需要挂父节点，就不要判 independent。
"""


ROUTE_CLASSIFIER_PROMPT += (
    "\n补充规则：像“六阶呢”“七阶呢”“更高阶呢”“下一项呢”这类是在追问上一轮展开式、近似阶数或余项，"
    "不是在问第六步/第七步，优先判为 weak_nonstep_followup 并定位上一轮 parent。"
)


@dataclass
class RuntimeMetrics:
    request_id: str
    session_id: str
    subject: str = "unsupported"
    started_at: float = field(default_factory=time.perf_counter)
    total_tokens: int = 0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    llm_calls: int = 0
    tool_calls: int = 0
    tool_success: int = 0
    tool_errors: int = 0
    steps: list[dict[str, Any]] = field(default_factory=list)
    llm_usages: list[dict[str, Any]] = field(default_factory=list)
    tool_usages: list[dict[str, Any]] = field(default_factory=list)
    runtime_prompt_tokens: int = 0
    runtime_completion_tokens: int = 0
    runtime_total_tokens: int = 0
    tool_prompt_tokens: int = 0
    tool_completion_tokens: int = 0
    tool_total_tokens: int = 0
    tool_llm_calls: int = 0
    embedding_calls: int = 0
    external_tool_api_calls: int = 0
    progress_callback: Callable[[dict[str, Any]], None] | None = field(default=None, repr=False, compare=False)

    def add_step(self, name: str, started: float, **extra: Any) -> None:
        item = {
            "name": name,
            "latency_ms": round((time.perf_counter() - started) * 1000, 2),
        }
        item.update(extra)
        self.steps.append(item)
        if self.progress_callback:
            try:
                self.progress_callback({
                    "type": "step",
                    "request_id": self.request_id,
                    "session_id": self.session_id,
                    "step": item,
                    "elapsed_ms": round((time.perf_counter() - self.started_at) * 1000, 2),
                })
            except Exception:
                pass

    def add_tool_usage(self, item: dict[str, Any]) -> None:
        normalized = dict(item)
        prompt_tokens = int(normalized.get("prompt_tokens", 0) or 0)
        completion_tokens = int(normalized.get("completion_tokens", 0) or 0)
        total_tokens = int(normalized.get("total_tokens", 0) or 0)
        if not total_tokens:
            total_tokens = prompt_tokens + completion_tokens
            normalized["total_tokens"] = total_tokens
        self.prompt_tokens += prompt_tokens
        self.completion_tokens += completion_tokens
        self.total_tokens += total_tokens
        self.tool_prompt_tokens += prompt_tokens
        self.tool_completion_tokens += completion_tokens
        self.tool_total_tokens += total_tokens
        kind = str(normalized.get("kind") or "")
        if kind == "chat":
            self.llm_calls += 1
            self.tool_llm_calls += 1
        elif kind in {"embedding", "local_embedding"}:
            self.embedding_calls += 1
        elif kind == "external_tool_api":
            self.external_tool_api_calls += 1
        self.tool_usages.append(normalized)

    def as_dict(self) -> dict[str, Any]:
        elapsed_ms = round((time.perf_counter() - self.started_at) * 1000, 2)
        success_rate = self.tool_success / self.tool_calls if self.tool_calls else 1.0
        return {
            "request_id": self.request_id,
            "session_id": self.session_id,
            "subject": self.subject,
            "elapsed_ms": elapsed_ms,
            "llm_calls": self.llm_calls,
            "tool_calls": self.tool_calls,
            "tool_success": self.tool_success,
            "tool_errors": self.tool_errors,
            "tool_success_rate": round(success_rate, 4),
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "total_tokens": self.total_tokens,
            "runtime_prompt_tokens": self.runtime_prompt_tokens,
            "runtime_completion_tokens": self.runtime_completion_tokens,
            "runtime_total_tokens": self.runtime_total_tokens,
            "tool_prompt_tokens": self.tool_prompt_tokens,
            "tool_completion_tokens": self.tool_completion_tokens,
            "tool_total_tokens": self.tool_total_tokens,
            "tool_llm_calls": self.tool_llm_calls,
            "embedding_calls": self.embedding_calls,
            "external_tool_api_calls": self.external_tool_api_calls,
            "llm_usages": self.llm_usages,
            "tool_usages": self.tool_usages,
            "steps": self.steps,
        }


@dataclass
class RuntimeResult:
    answer: str
    subject: str
    messages: list[dict[str, Any]]
    tool_calls: list[dict[str, Any]]
    metrics: dict[str, Any]
    extra_memory: dict[str, Any] | None = None


@dataclass
class RouteDecision:
    subject: str = "unsupported"
    is_followup: bool = False
    followup_category: str = "independent"
    parent_turn_id: int | None = None
    parent_turn_ids: list[int] = field(default_factory=list)
    reason: str = ""
    clarification: str | None = None

    def followup_route(self) -> dict[str, Any]:
        return {
            "category": self.followup_category,
            "parent_turn_id": self.parent_turn_id,
            "parent_turn_ids": self.parent_turn_ids,
            "reason": self.reason,
            "clarification": self.clarification,
        }


@dataclass
class ToolSpec:
    name: str
    description: str
    parameters: dict[str, Any]
    func: Callable[[dict[str, Any]], Any]
    return_mode: str = "synthesize"

    def openai_schema(self) -> dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            },
        }


def now_id() -> str:
    return datetime.now().strftime("%Y%m%d%H%M%S%f")


def safe_session_id(session_id: str) -> str:
    return legacy_agent.safe_session_id(session_id)


def md_session_path(session_id: str) -> Path:
    return SESSION_MD_DIR / f"{safe_session_id(session_id)}.md"


def delete_runtime_session_artifacts(session_id: str) -> None:
    json_path = legacy_agent.session_path(session_id)
    md_path = md_session_path(session_id)
    vector_path = legacy_agent.session_vector_path(session_id)
    for path in (json_path, md_path):
        if path.exists() and path.is_file():
            path.unlink()
    if vector_path.exists():
        if vector_path.is_dir():
            shutil.rmtree(vector_path)
        elif vector_path.is_file():
            vector_path.unlink()


def read_recent_md_messages(session_id: str, max_turns: int = SHORT_TERM_TURNS) -> list[dict[str, str]]:
    path = md_session_path(session_id)
    if path.exists():
        text = path.read_text(encoding="utf-8")
        turns = re.split(r"(?m)^## Turn .*$", text)[1:]
        messages: list[dict[str, str]] = []
        for turn in turns[-max_turns:]:
            user_match = re.search(r"(?s)### User\s*(.*?)\s*### Assistant", turn)
            assistant_match = re.search(r"(?s)### Assistant\s*(.*)$", turn)
            if user_match:
                user_content = user_match.group(1).strip()
                if user_content:
                    messages.append({"role": "user", "content": user_content})
            if assistant_match:
                assistant_content = assistant_match.group(1).strip()
                if assistant_content:
                    messages.append({"role": "assistant", "content": assistant_content})
        if messages:
            return messages

    json_session = legacy_agent.load_session(session_id)
    turns = json_session.get("turns", [])[-max_turns:]
    messages: list[dict[str, str]] = []
    for turn in turns:
        user_query = str(turn.get("user_query") or "")
        assistant_answer = str(turn.get("assistant_answer") or turn.get("assistant_answer_preview") or "")
        if user_query:
            messages.append({"role": "user", "content": user_query})
        if assistant_answer:
            messages.append({"role": "assistant", "content": assistant_answer})
    return messages


def append_md_turn(session_id: str, user_message: str, assistant_answer: str, metadata: dict[str, Any]) -> None:
    path = md_session_path(session_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(f"# Session {safe_session_id(session_id)}\n\n", encoding="utf-8")
    block = [
        f"## Turn {metadata.get('turn_id', '?')} - {datetime.now().isoformat(timespec='seconds')}",
        "",
        "<!-- metadata",
        json.dumps(metadata, ensure_ascii=False, indent=2),
        "-->",
        "",
        "### User",
        user_message.strip(),
        "",
        "### Assistant",
        assistant_answer.strip(),
        "",
    ]
    with path.open("a", encoding="utf-8") as file:
        file.write("\n".join(block))
        file.write("\n")


def append_runtime_turn(session_id: str, user_message: str, result: RuntimeResult) -> None:
    session = legacy_agent.load_session(session_id)
    turns = session.setdefault("turns", [])
    turn_id = (turns[-1].get("turn_id", 0) + 1) if turns else 1
    followup_dag = (result.extra_memory or {}).get("followup_dag")
    for record in result.tool_calls:
        if record.get("name") != "answer_math_followup":
            continue
        arguments = record.get("arguments")
        if isinstance(arguments, dict) and isinstance(arguments.get("_followup_dag"), dict):
            followup_dag = dict(arguments["_followup_dag"])
            break
    if followup_dag is not None:
        followup_dag["current_turn_id"] = turn_id
    route = {
        "subject": result.subject,
        "intent": "tool_loop",
        "need_vl": False,
        "notes": "standard OpenAI tool-calling runtime",
    }
    turn = {
        "turn_id": turn_id,
        "time": datetime.now().isoformat(timespec="seconds"),
        "user_query": user_message,
        "route": route,
        "memory": {
            "topic": user_message[:80],
            "question_brief": user_message[:300],
            "answer_brief": result.answer[:300],
            "context_root_id": result.tool_calls[-1]["name"] if result.tool_calls else "",
        },
        "assistant_answer": result.answer,
        "assistant_answer_preview": result.answer[:500],
        "metrics": result.metrics,
        "tool_calls": result.tool_calls,
    }
    if followup_dag is not None:
        memory = turn["memory"]
        memory["followup_parent_turn_id"] = followup_dag.get("parent_turn_id")
        memory["followup_parent_turn_ids"] = followup_dag.get("parent_turn_ids") or []
        memory["followup_chain_turn_ids"] = followup_dag.get("chain_turn_ids") or []
        memory["followup_dag_reason"] = followup_dag.get("reason") or ""
        memory["followup_dag_lookback"] = followup_dag.get("lookback")
        turn["followup_dag"] = followup_dag
    turns.append(turn)
    legacy_agent.save_session(session_id, session)
    append_md_turn(session_id, user_message, result.answer, {"turn_id": turn_id, **result.metrics})


def json_schema(properties: dict[str, dict[str, Any]], required: list[str] | None = None) -> dict[str, Any]:
    return {
        "type": "object",
        "properties": properties,
        "required": required or [],
        "additionalProperties": False,
    }


def _call_tool(tool: Any, payload: dict[str, Any]) -> Any:
    return tool.invoke(payload) if hasattr(tool, "invoke") else tool(payload)


def compact_text(value: Any, limit: int = 1200) -> str:
    text = str(value or "").strip()
    text = re.sub(r"\s+", " ", text)
    if len(text) <= limit:
        return text
    return f"{text[:limit].rstrip()}..."


def turn_context_block(turn: dict[str, Any], limit: int = 1600) -> str:
    return compact_text(legacy_agent.turn_full_text(turn), limit)


def is_weak_context_followup(user_input: str) -> bool:
    text = user_input.strip()
    if not text:
        return False
    return bool(re.search(
        r"这个|这个呢|这个为什么|为什么成立|怎么成立|继续|接着|那如果|如果.*呢|换成|改成|还成立吗|"
        r"第[一二三四五]个.*呢|(?:\d+|[一二三四五六七八九十]+)阶呢|上一个|上一轮|刚才|刚刚|它|这个式子|这个余项|余项呢|总结一下|简洁",
        text,
    ))


def classify_followup_route_with_llm(
    user_input: str,
    candidates: list[dict[str, Any]],
    client: Any | None,
    metrics: RuntimeMetrics | None = None,
    subject_hint: str | None = None,
) -> dict[str, Any]:
    if not candidates or client is None:
        return {
            "category": "unknown",
            "parent_turn_id": None,
            "parent_turn_ids": [],
            "reason": "no_candidates_or_client",
        }
    history: list[dict[str, str]] = []
    for turn in candidates:
        user_query = str(turn.get("user_query") or "")
        assistant_answer = str(turn.get("assistant_answer") or turn.get("assistant_answer_preview") or "")
        if user_query:
            history.append({"role": "user", "content": user_query})
        if assistant_answer:
            history.append({"role": "assistant", "content": assistant_answer})
    route = route_with_llm(
        user_input,
        history,
        candidates,
        client,
        metrics,
        subject_hint=subject_hint,
        subject_locked=bool(subject_hint),
        followup_hint=classify_followup_heuristic(user_input, history),
        followup_locked=False,
    )
    return route.followup_route()

    candidate_text = "\n\n".join(
        f"[turn {turn.get('turn_id')}]\n{turn_context_block(turn, 700)}"
        for turn in candidates
    )
    prompt = (
        f"请判断当前用户输入相对于最近 {FOLLOWUP_DAG_LOOKBACK} 个 turn 属于哪一类追问或新问题。\n"
        "只输出 JSON："
        '{"category":"independent|step_followup|weak_nonstep_followup|contextual_nonstep_followup|ambiguous",'
        '"parent_turn_id":number|null,"parent_turn_ids":[number],"reason":"一句话"}\n\n'
        "分类规则：\n"
        "- independent：当前输入是完整新问题，不依赖最近对话。\n"
        "- step_followup：追问某个解题步骤、局部变形、某一步为什么成立，应走 explain_math_step。\n"
        "- weak_nonstep_followup：非常省略的非步骤追问，通常默认接上一轮，例如“六阶呢”“为什么”“还成立吗”“继续”“这个呢”。\n"
        f"- contextual_nonstep_followup：非步骤追问，但需要从最近 {FOLLOWUP_DAG_LOOKBACK} 轮定位 parent，例如“第二个题的余项呢”“刚才那个定理换成开区间还成立吗”。\n"
        "- ambiguous：多个 parent 都可能或无法判断，需要澄清。\n"
        "要求：\n"
        "- parent_turn_id 和 parent_turn_ids 只能取候选 turn_id；独立或歧义时 parent_turn_id 为 null 且 parent_turn_ids 为空数组。\n"
        "- 如果只指向一个 parent，同时填写 parent_turn_id 和 parent_turn_ids，例如 2 与 [2]。\n"
        "- 如果用户说“这两个/二者/分别/对比/应用场景各是什么”等多对象追问，可以填写多个 parent_turn_ids，例如 [1,2]，parent_turn_id 可填最近/最主要的一个。\n"
        "- 如果是 weak_nonstep_followup，通常 parent_turn_id 选最近一轮，parent_turn_ids 只含最近一轮。\n"
        "- 不要把“第 x 步怎么来的/这一步为什么”判成非步骤追问。\n\n"
        f"候选 turn：\n{candidate_text}\n\n"
        f"当前用户输入：{user_input}"
    )
    try:
        global_client = make_global_client(client)
        model_name = global_model_name()
        llm_started = time.perf_counter()
        response = global_client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "你是会话追问类型判定器，只输出 JSON。"},
                {"role": "user", "content": prompt},
            ],
            temperature=global_temperature(0),
        )
        if metrics is not None:
            metrics.llm_calls += 1
            record_usage(metrics, response, "followup_route_classifier", model=model_name, started_at=llm_started)
        data = legacy_agent.parse_json_object(response.choices[0].message.content or "{}")
    except Exception as exc:
        return {
            "category": "unknown",
            "parent_turn_id": None,
            "parent_turn_ids": [],
            "reason": f"route_classifier_error:{exc}",
        }

    category = str(data.get("category") or "unknown")
    if category not in {"independent", "step_followup", "weak_nonstep_followup", "contextual_nonstep_followup", "ambiguous"}:
        category = "unknown"
    parent = data.get("parent_turn_id")
    candidate_ids = {int(turn.get("turn_id")) for turn in candidates if turn.get("turn_id") is not None}
    parent_ids: list[int] = []
    raw_parent_ids = data.get("parent_turn_ids")
    if isinstance(raw_parent_ids, list):
        for item in raw_parent_ids:
            try:
                item_id = int(item)
            except (TypeError, ValueError):
                continue
            if item_id in candidate_ids and item_id not in parent_ids:
                parent_ids.append(item_id)
    try:
        parent_id = int(parent)
    except (TypeError, ValueError):
        parent_id = None
    if parent_id not in candidate_ids:
        parent_id = None
    if parent_id is not None and parent_id not in parent_ids:
        parent_ids.append(parent_id)
    parent_ids.sort()
    return {
        "category": category,
        "parent_turn_id": parent_id,
        "parent_turn_ids": parent_ids,
        "reason": str(data.get("reason") or ""),
        "clarification": str(data.get("clarification") or "") or None,
    }


def turn_parent_id(turn: dict[str, Any]) -> int | None:
    memory = turn.get("memory") if isinstance(turn.get("memory"), dict) else {}
    value = memory.get("followup_parent_turn_id")
    if value is None:
        value = turn.get("followup_parent_turn_id")
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def turn_parent_ids(turn: dict[str, Any]) -> list[int]:
    memory = turn.get("memory") if isinstance(turn.get("memory"), dict) else {}
    raw_values = memory.get("followup_parent_turn_ids")
    if raw_values is None:
        raw_values = turn.get("followup_parent_turn_ids")
    values: list[Any]
    if isinstance(raw_values, list):
        values = raw_values
    else:
        parent = turn_parent_id(turn)
        values = [parent] if parent is not None else []
    parent_ids: list[int] = []
    for value in values:
        try:
            parent_id = int(value)
        except (TypeError, ValueError):
            continue
        if parent_id and parent_id not in parent_ids:
            parent_ids.append(parent_id)
    return parent_ids


def route_parent_ids(route_decision: dict[str, Any] | None) -> list[int]:
    if not route_decision:
        return []
    raw_values = route_decision.get("parent_turn_ids")
    values: list[Any] = raw_values if isinstance(raw_values, list) else []
    single = route_decision.get("parent_turn_id")
    if single is not None:
        values = [*values, single]
    parent_ids: list[int] = []
    for value in values:
        try:
            parent_id = int(value)
        except (TypeError, ValueError):
            continue
        if parent_id and parent_id not in parent_ids:
            parent_ids.append(parent_id)
    return parent_ids


def resolve_followup_parent_with_llm(
    user_input: str,
    candidates: list[dict[str, Any]],
    client: Any | None,
    route_decision: dict[str, Any] | None = None,
    metrics: RuntimeMetrics | None = None,
) -> tuple[int, str, str]:
    if not candidates:
        return FOLLOWUP_EMPTY_ROOT_ID, "independent", "no_previous_turns"
    if route_decision:
        category = str(route_decision.get("category") or "")
        parent_ids = route_parent_ids(route_decision)
        parent = route_decision.get("parent_turn_id")
        if parent is None and parent_ids:
            parent = parent_ids[0]
        candidate_ids = {int(turn.get("turn_id")) for turn in candidates if turn.get("turn_id") is not None}
        try:
            parent_id = int(parent)
        except (TypeError, ValueError):
            parent_id = FOLLOWUP_EMPTY_ROOT_ID
        if parent_id in candidate_ids and category in {"weak_nonstep_followup", "contextual_nonstep_followup"}:
            return parent_id, category, str(route_decision.get("reason") or "route_classifier_parent")
        if category in {"independent", "step_followup", "ambiguous"}:
            return FOLLOWUP_EMPTY_ROOT_ID, category, str(route_decision.get("reason") or "route_classifier_no_parent")
    if client is None:
        return int(candidates[-1].get("turn_id", FOLLOWUP_EMPTY_ROOT_ID)), "fallback_previous", "no_resolver_client"

    candidate_text = "\n\n".join(
        f"[turn {turn.get('turn_id')}]\n{turn_context_block(turn, 900)}"
        for turn in candidates
    )
    prompt = (
        f"判断当前用户输入是否是下面最近 {FOLLOWUP_DAG_LOOKBACK} 个 turn 中某一轮的非步骤追问。\n"
        "只输出 JSON："
        '{"parent_turn_id": number|null, "followup_type": "independent|parameter_change|condition_change|remainder_query|compare_roots|continue_explanation|rewrite|summary", "reason": "一句话"}\n\n'
        "规则：\n"
        "- 只能选择给出的 turn_id；如果是独立新问题，parent_turn_id 为 null。\n"
        "- 如果用户说“上一个/这个/刚才/继续”等弱指代，通常选最近一轮。\n"
        f"- 如果用户说“第一个/第二个”，优先在最近 {FOLLOWUP_DAG_LOOKBACK} 轮的局部上下文里找对应对象，不要回到更早历史。\n"
        "- 如果多个候选都合理且无法消歧，parent_turn_id 为 null，followup_type 为 independent，reason 写明需要澄清。\n\n"
        f"候选 turn：\n{candidate_text}\n\n"
        f"当前用户输入：{user_input}"
    )
    try:
        global_client = make_global_client(client)
        model_name = global_model_name()
        llm_started = time.perf_counter()
        response = global_client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": f"你是会话追问溯源节点，只做最近 {FOLLOWUP_DAG_LOOKBACK} 轮内的父节点选择。"},
                {"role": "user", "content": prompt},
            ],
            temperature=global_temperature(0),
        )
        if metrics is not None:
            metrics.llm_calls += 1
            record_usage(metrics, response, "followup_parent_resolver", model=model_name, started_at=llm_started)
        data = legacy_agent.parse_json_object(response.choices[0].message.content or "{}")
    except Exception as exc:
        return int(candidates[-1].get("turn_id", FOLLOWUP_EMPTY_ROOT_ID)), "fallback_previous", f"resolver_error:{exc}"

    parent = data.get("parent_turn_id")
    candidate_ids = {int(turn.get("turn_id")) for turn in candidates if turn.get("turn_id") is not None}
    try:
        parent_id = int(parent)
    except (TypeError, ValueError):
        return FOLLOWUP_EMPTY_ROOT_ID, str(data.get("followup_type") or "independent"), str(data.get("reason") or "resolver_independent")
    if parent_id not in candidate_ids:
        return FOLLOWUP_EMPTY_ROOT_ID, "independent", f"resolver_parent_not_in_recent_{FOLLOWUP_DAG_LOOKBACK}"
    return parent_id, str(data.get("followup_type") or "contextual_followup"), str(data.get("reason") or "")


def followup_chain_for_parent(session: dict[str, Any], parent_turn_id: int) -> list[dict[str, Any]]:
    if parent_turn_id == FOLLOWUP_EMPTY_ROOT_ID:
        return []
    turns_by_id = {
        int(turn.get("turn_id")): turn
        for turn in session.get("turns", [])
        if isinstance(turn.get("turn_id"), int)
    }
    chain: list[dict[str, Any]] = []
    seen: set[int] = set()
    current_id = parent_turn_id
    while current_id and current_id not in seen and current_id in turns_by_id:
        seen.add(current_id)
        turn = turns_by_id[current_id]
        chain.append(turn)
        parents = turn_parent_ids(turn)
        if not parents:
            break
        current_id = parents[0]
    return list(reversed(chain))


def followup_subgraph_for_parents(session: dict[str, Any], parent_turn_ids: list[int]) -> list[dict[str, Any]]:
    turns_by_id = {
        int(turn.get("turn_id")): turn
        for turn in session.get("turns", [])
        if isinstance(turn.get("turn_id"), int)
    }
    collected: dict[int, dict[str, Any]] = {}
    seen: set[int] = set()

    def visit(turn_id: int) -> None:
        if not turn_id or turn_id in seen or turn_id not in turns_by_id:
            return
        seen.add(turn_id)
        turn = turns_by_id[turn_id]
        for parent_id in turn_parent_ids(turn):
            visit(parent_id)
        collected[turn_id] = turn

    for parent_id in parent_turn_ids:
        visit(parent_id)
    return [collected[turn_id] for turn_id in sorted(collected)]


def format_followup_dag_context(
    session_id: str,
    user_input: str,
    output_format: str,
    client: Any | None,
    route_decision: dict[str, Any] | None = None,
    metrics: RuntimeMetrics | None = None,
) -> dict[str, Any]:
    session = legacy_agent.load_session(session_id)
    candidates = session.get("turns", [])[-FOLLOWUP_DAG_LOOKBACK:]
    parent_id, followup_type, reason = resolve_followup_parent_with_llm(
        user_input,
        candidates,
        client,
        route_decision,
        metrics,
    )
    parent_ids = route_parent_ids(route_decision)
    candidate_ids = {int(turn.get("turn_id")) for turn in candidates if turn.get("turn_id") is not None}
    parent_ids = [item for item in parent_ids if item in candidate_ids]
    if not parent_ids and parent_id != FOLLOWUP_EMPTY_ROOT_ID:
        parent_ids = [parent_id]
    chain = followup_subgraph_for_parents(session, parent_ids)
    root_context = "\n\n".join(
        f"[root turn {turn.get('turn_id')}]\n{turn_context_block(turn, 1200)}"
        for turn in chain
        if not turn_parent_ids(turn)
    ) if chain else ""
    chain_lines = []
    if chain:
        edge_ids = [str(turn.get("turn_id")) for turn in chain]
        label = "DAG 链路" if len(parent_ids) <= 1 else "DAG 子图"
        chain_lines.append(f"{label}：EMPTY({FOLLOWUP_EMPTY_ROOT_ID}) -> " + " -> ".join(f"turn {item}" for item in edge_ids) + " -> current")
        if len(parent_ids) > 1:
            chain_lines.append("当前节点父节点：" + ", ".join(f"turn {item}" for item in parent_ids))
        for turn in chain:
            chain_lines.append(f"\n[turn {turn.get('turn_id')}]\n{turn_context_block(turn, 1800)}")
    else:
        chain_lines.append(f"DAG 链路：EMPTY({FOLLOWUP_EMPTY_ROOT_ID}) -> current")
        chain_lines.append(f"最近 {FOLLOWUP_DAG_LOOKBACK} 轮内未确定父节点；如当前问题指代不明，应请用户澄清。")
    chain_lines.append(f"\n[current]\n{compact_text(user_input, 800)}")

    return {
        "user_query": user_input,
        "root_context": root_context,
        "followup_context": "\n".join(chain_lines),
        "followup_type": followup_type,
        "output_format": output_format,
        "followup_dag": {
            "lookback": FOLLOWUP_DAG_LOOKBACK,
            "parent_turn_id": parent_id,
            "parent_turn_ids": parent_ids,
            "chain_turn_ids": [turn.get("turn_id") for turn in chain],
            "reason": reason,
            "empty_root_id": FOLLOWUP_EMPTY_ROOT_ID,
        },
    }


def build_math_tools(
    metrics: RuntimeMetrics | None = None,
    followup_context_resolver: Callable[[dict[str, Any]], dict[str, Any]] | None = None,
) -> dict[str, ToolSpec]:
    toolkit = legacy_agent.get_toolkit()

    def timed_skill_call(step_name: str, tool: Any, payload: dict[str, Any], **extra: Any) -> Any:
        started = time.perf_counter()
        try:
            value = _call_tool(tool, payload)
        except Exception as exc:
            if metrics is not None:
                metrics.add_step(f"skill:solve_exam_question:{step_name}", started, ok=False, error=str(exc), **extra)
            raise
        if metrics is not None:
            metrics.add_step(f"skill:solve_exam_question:{step_name}", started, ok=True, **extra)
        return value

    def solve_exam_question(args: dict[str, Any]) -> str:
        exam_type = args.get("exam_type") or "math1"
        year = int(args["year"])
        question_number = int(args["question_number"])
        user_query = str(args.get("user_query") or "")
        image_paths = [Path(item) for item in args.get("image_paths") or []]
        output_format = str(args.get("output_format") or "ui")
        thinking = str(args.get("thinking") or "light")
        problem = legacy_agent.math_problem_from_tool_payload(
            timed_skill_call("search_math_exam", toolkit.search_math_exam, {
                "exam_type": exam_type,
                "year": year,
                "question_number": question_number,
            }, year=year, question_number=question_number, exam_type=exam_type)
        )
        vl_text = None
        image_started = time.perf_counter()
        database_image_paths = legacy_agent.problem_image_paths(problem)
        ocr_image_paths: list[Path] = []
        seen_paths: set[str] = set()
        for path in [*database_image_paths, *image_paths]:
            key = str(path.resolve() if path.exists() else path).lower()
            if key in seen_paths:
                continue
            seen_paths.add(key)
            ocr_image_paths.append(path)
        if metrics is not None:
            metrics.add_step(
                "skill:solve_exam_question:collect_images",
                image_started,
                database_images=len(database_image_paths),
                user_images=len(image_paths),
                ocr_images=len(ocr_image_paths),
            )
        if ocr_image_paths:
            ocr_query = (
                f"{user_query}\n\n"
                f"题库定位：{problem.year} 年{legacy_agent.exam_label(problem.exam_type)}第 {problem.question_number} 题。\n"
                "请识别题库图片和用户上传图片中的题干、公式、坐标轴、图形区域、选项图形等关键信息，不要解题。"
                "对区域标号、阴影或选项小图，必须按实际边界、曲线、端点、刻度和相对位置描述；能读出不等式或参数范围就列出，读不出则标注不确定。"
            )
            vl_text = timed_skill_call("ocr_math_image", toolkit.ocr_math_image, {
                "image_paths": [str(path) for path in ocr_image_paths],
                "user_query": ocr_query,
            }, image_count=len(ocr_image_paths))
        feedback = None
        last_solution = ""
        last_judgement: dict[str, Any] = {}
        for attempt in range(1, 4):
            last_solution = timed_skill_call("solve_math_exam", toolkit.solve_math_exam, {
                "exam_type": problem.exam_type,
                "year": problem.year,
                "question_number": problem.question_number,
                "user_query": user_query,
                "vl_text": vl_text,
                "output_format": output_format,
                "feedback": feedback,
                "thinking": thinking,
            }, attempt=attempt)
            last_judgement = timed_skill_call("judge_math_answer", toolkit.judge_math_answer, {
                "exam_type": problem.exam_type,
                "year": problem.year,
                "question_number": problem.question_number,
                "solution": last_solution,
            }, attempt=attempt)
            if last_judgement.get("match"):
                return last_solution
            feedback = (
                "上一次答案与标准答案不一致。"
                f"标准答案: {last_judgement.get('expected') or problem.answer_text}; "
                f"你的答案: {last_judgement.get('actual')}; "
                f"原因: {last_judgement.get('reason')}"
            )
        if problem.answer_text:
            fallback_started = time.perf_counter()
            try:
                fallback_answer = legacy_agent.render_standard_answer_with_explanation(problem, user_query, vl_text, output_format, thinking)
            except Exception as exc:
                if metrics is not None:
                    metrics.add_step("skill:solve_exam_question:fallback_explanation", fallback_started, ok=False, error=str(exc))
                raise
            if metrics is not None:
                metrics.add_step("skill:solve_exam_question:fallback_explanation", fallback_started, ok=True)
            return fallback_answer
        return last_solution or json.dumps(last_judgement, ensure_ascii=False)

    def answer_context_followup(args: dict[str, Any]) -> str:
        payload = dict(args)
        if followup_context_resolver is not None:
            resolved = followup_context_resolver(payload)
            for key in ("user_query", "root_context", "followup_context", "followup_type", "output_format"):
                if key in resolved:
                    payload[key] = resolved[key]
            args.update(payload)
            args["_followup_dag"] = resolved.get("followup_dag")
        return legacy_agent.explain_math_followup_with_qwenmath(
            str(payload.get("user_query") or ""),
            str(payload.get("root_context") or ""),
            str(payload.get("followup_context") or ""),
            str(payload.get("followup_type") or "contextual_followup"),
            str(payload.get("output_format") or "ui"),
        )

    common_exam_props = {
        "exam_type": {"type": "string", "enum": ["math1", "math2", "math3"], "description": "考试类型：math1 数学一，math2 数学二，math3 数学三"},
        "year": {"type": "integer", "description": "真题年份，如 2021"},
        "question_number": {"type": "integer", "description": "题号，如 9"},
    }
    tools = {
        "solve_exam_question": ToolSpec(
            "solve_exam_question",
            "组合 skill：搜索考研数学真题，若题库题块或用户本轮包含图片则先用 Qwen-VL OCR，再调用数学解题并与本地标准答案核对。仅当用户文本明确给出年份、科目和题号时使用，例如“2021 数一第 9 题怎么做”。不要根据图片文件名推断真题。边界：未知来源图片题用 ocr_math_image 后接 solve_general_math；只看题目用 show_math_exam_question，只要标准答案用 show_math_exam_answer，局部追问用 explain_math_step。",
            json_schema({
                **common_exam_props,
                "user_query": {"type": "string", "description": "用户原始问题，保留追问措辞"},
                "image_paths": {"type": "array", "items": {"type": "string"}, "description": "可选的本地图片路径列表"},
                "output_format": {"type": "string", "enum": ["ui", "terminal"], "description": "输出格式"},
                "thinking": {"type": "string", "enum": ["disabled", "light", "max"], "description": "数学解题模型思考强度。完整真题或高难题建议 light；普通题可 disabled"},
            }, ["exam_type", "year", "question_number", "user_query"]),
            solve_exam_question,
            return_mode="direct",
        ),
        "show_math_exam_question": ToolSpec(
            "show_math_exam_question",
            "展示考研数学真题题面，不解题、不展示答案。仅当用户文本明确给出年份、科目和题号时使用。典型问法：“2024 数一第 5 题题目是什么”“给我原题”。不要根据图片文件名推断真题；图片未知来源时先 OCR。",
            json_schema(common_exam_props, ["exam_type", "year", "question_number"]),
            lambda args: _call_tool(toolkit.show_math_exam_question, args),
            return_mode="direct",
        ),
        "show_math_exam_answer": ToolSpec(
            "show_math_exam_answer",
            "展示本地标准答案速查，不重新解题。仅当用户文本明确给出年份、科目和题号时使用。典型问法：“2024 数一第 5 题答案是什么”“选什么”。不要根据图片文件名推断真题；用户要过程时用 solve_exam_question。",
            json_schema(common_exam_props, ["exam_type", "year", "question_number"]),
            lambda args: _call_tool(toolkit.show_math_exam_answer, args),
            return_mode="direct",
        ),
        "explain_math_step": ToolSpec(
            "explain_math_step",
            "解释已有解题过程中的某一步或局部结论。典型问法：“第 2 步怎么来的”“这里为什么可以这样变形”“这一步是不是用了中值定理”。必须传入从历史定位出的 original_context。边界：不完整重做整题。",
            json_schema({
                **common_exam_props,
                "user_query": {"type": "string", "description": "用户当前追问"},
                "previous_context": {"type": "string", "description": "最近 15 轮中定位到的原始解题过程或 root 上下文，必须原样保留关键步骤"},
                "output_format": {"type": "string", "enum": ["ui", "terminal"]},
                "thinking": {"type": "string", "enum": ["disabled", "light", "max"], "description": "数学解释模型思考强度，默认 disabled；复杂步骤可 light"},
            }, ["exam_type", "year", "question_number", "user_query", "previous_context"]),
            lambda args: _call_tool(toolkit.explain_math_step, args),
            return_mode="direct",
        ),
        "solve_general_math": ToolSpec(
            "solve_general_math",
            "解答普通数学题、概念解释、定理说明、非真题计算或证明。典型问法：“第一积分中值定理是什么”“求 lim...”。边界：明确年份题号的考研真题用 solve_exam_question。",
            json_schema({
                "user_query": {"type": "string", "description": "完整数学问题"},
                "vl_text": {"type": ["string", "null"], "description": "可选 OCR 结果"},
                "output_format": {"type": "string", "enum": ["ui", "terminal"]},
                "thinking": {"type": "string", "enum": ["disabled", "light", "max"], "description": "数学解题模型思考强度，默认 disabled；复杂推导可 light"},
            }, ["user_query"]),
            lambda args: _call_tool(toolkit.solve_general_math, args),
            return_mode="direct",
        ),
        "ocr_math_image": ToolSpec(
            "ocr_math_image",
            "识别数学题图片，只做 OCR、公式识别和图形条件说明，不解题；既可用于用户上传图片，也可由 solve_exam_question 内部识别本地题库题图。典型问法：“看这张图题面是什么”。图片文件名不能作为真题定位依据。边界：OCR 后解题通常调用 solve_general_math；只有用户文本明确给出年份、科目、题号时才可接 solve_exam_question。",
            json_schema({
                "image_paths": {"type": "array", "items": {"type": "string"}, "description": "本地图片路径列表"},
                "user_query": {"type": "string", "description": "用户文字补充"},
            }, ["image_paths", "user_query"]),
            lambda args: _call_tool(toolkit.ocr_math_image, args),
            return_mode="evidence",
        ),
    }
    if context_followup_tools_enabled():
        tools.update({
            "answer_math_followup": ToolSpec(
                "answer_math_followup",
                "回答非步骤型数学上下文追问，例如参数改动、条件替换、余项/误差追问、多个前序题之间用“第一个/第二个”定位、继续说明上一个结论等。不要用于“第 x 步怎么来的”这类局部步骤解释；步骤解释仍用 explain_math_step。必须传入最近历史中定位到的 root_context 和 followup_context。",
                json_schema({
                    "user_query": {"type": "string", "description": "用户当前非步骤追问"},
                    "root_context": {"type": "string", "description": "被追问的根话题、原题或原始解法。多个候选时应包含足够定位信息"},
                    "followup_context": {"type": "string", "description": "从根话题到当前追问的相关对话链路，原样保留函数、参数、展开点、阶数、误差要求等"},
                    "followup_type": {"type": "string", "description": "追问类型，如 parameter_change / condition_change / remainder_query / compare_roots / continue_explanation"},
                    "output_format": {"type": "string", "enum": ["ui", "terminal"]},
                }, ["user_query", "root_context", "followup_context"]),
                answer_context_followup,
                return_mode="direct",
            ),
            "rewrite_math_answer": ToolSpec(
                "rewrite_math_answer",
                "按用户要求改写已有数学回答，例如更简洁、口语化、适合笔记、保留若干位小数等；不重新解题。必须传入 previous_context。",
                json_schema({
                    "user_query": {"type": "string", "description": "用户当前改写要求"},
                    "previous_context": {"type": "string", "description": "需要被改写的上一轮或相关历史回答"},
                    "output_format": {"type": "string", "enum": ["ui", "terminal"]},
                }, ["user_query", "previous_context"]),
                lambda args: _call_tool(toolkit.rewrite_math_answer, args),
                return_mode="direct",
            ),
            "summarize_math_solution": ToolSpec(
                "summarize_math_solution",
                "总结已有数学解法、知识点或对话链路；不重新解题。适用于“总结一下”“提炼思路”“帮我整理成笔记”等非步骤追问。必须传入 previous_context。",
                json_schema({
                    "user_query": {"type": "string", "description": "用户当前总结要求"},
                    "previous_context": {"type": "string", "description": "需要被总结的上一轮或相关历史回答"},
                    "output_format": {"type": "string", "enum": ["ui", "terminal"]},
                }, ["user_query", "previous_context"]),
                lambda args: _call_tool(toolkit.summarize_math_solution, args),
                return_mode="direct",
            ),
        })
    return tools


def build_current_affairs_tools() -> dict[str, ToolSpec]:
    toolkit = legacy_agent.get_toolkit()
    return {
        "get_current_affairs": ToolSpec(
            "get_current_affairs",
            "调用 Coze 时政智能体整理近期时政、政策、新闻热点。典型问法：“2026 年 5 月考研政治时政热点”。边界：数学题不要使用。",
            json_schema({"query": {"type": "string", "description": "时政查询或整理请求"}}, ["query"]),
            lambda args: _call_tool(toolkit.get_current_affairs, args),
        )
    }

def build_politics_tools() -> dict[str, ToolSpec]:
    """政治知识点 RAG 工具。"""
    try:
        from politics_rag import retrieve_politics, answer_with_qwen
    except Exception:
        return {}
    return {
        "search_politics_knowledge": ToolSpec(
            "search_politics_knowledge",
            "从考研政治知识库（马原、毛中特、史纲、思修）中检索相关知识点。典型问法：「马克思主义基本原理有哪些章节」「主要矛盾和矛盾的主要方面有什么区别」。",
            json_schema({"query": {"type": "string", "description": "政治知识查询"}}, ["query"]),
            lambda args: json.dumps(retrieve_politics(str(args["query"]), top_k=3), ensure_ascii=False, default=str),
            return_mode="evidence",
        ),
    }



MATH_STRONG_KEYWORDS = (
    # 基础与极限
    "考研数学", "数学一", "数学二", "数学三", "数一", "数二", "数三", "math1", "math2", "math3",
    "初等函数", "基本初等函数", "复合函数", "反函数", "分段函数", "隐函数", "参数方程",
    "函数定义域", "函数值域", "函数奇偶性", "函数周期性", "函数单调性", "单调区间",
    "数列极限", "函数极限", "极限定义", "ε-N定义", "ε-δ定义", "epsilon-delta", "epsilon-N",
    "去心邻域", "左极限", "右极限", "单侧极限", "双侧极限", "极限存在", "极限不存在",
    "极限唯一性", "极限保号性", "极限局部有界性", "极限四则运算法则", "左右极限相等",
    "无穷小量", "无穷大量", "等价无穷小", "高阶无穷小", "低阶无穷小", "同阶无穷小",
    "无穷小替换", "等价替换", "无穷小比较", "无穷大比较", "等价无穷大", "o符号", "O符号",
    "未定式", "洛必达法则", "L'Hospital法则", "泰勒展开求极限", "重要极限", "两个重要极限",
    "第一重要极限", "第二重要极限", "华里士公式", "Wallis公式", "斯特林公式", "Stirling公式",
    "夹逼准则", "夹挤准则", "迫敛性", "三明治定理", "Squeeze theorem", "单调有界准则",
    "单调有界收敛准则", "递推数列极限",
    "可去间断点", "跳跃间断点", "无穷间断点", "振荡间断点", "间断点",
    "渐近线", "水平渐近线", "垂直渐近线", "斜渐近线",
    # 导数、微分、中值定理
    "导数定义", "左导数", "右导数", "导函数", "导数几何意义", "瞬时变化率", "切线斜率",
    "可微定义", "全增量", "线性主部", "一阶微分", "高阶微分", "微分形式",
    "复合函数求导", "隐函数求导", "参数方程求导", "反函数求导", "对数求导法",
    "高阶导数", "n阶导数", "莱布尼茨公式", "链式法则", "基本求导公式",
    "切线方程", "法线方程", "法向量", "切向量", "驻点", "临界点", "极大值", "极小值",
    "极值判别", "导数符号表", "凹凸性", "凹函数", "凸函数", "拐点", "二阶导数判别",
    "曲率", "曲率半径", "零点定理", "介值定理", "最值定理", "根的存在性", "根的唯一性",
    "罗尔定理", "Rolle定理", "拉格朗日中值定理", "Lagrange中值定理", "有限增量公式",
    "柯西中值定理", "Cauchy中值定理", "泰勒公式", "泰勒中值定理", "Taylor公式",
    "麦克劳林公式", "Maclaurin公式", "皮亚诺余项", "拉格朗日余项", "积分余项",
    "泰勒展开", "麦克劳林展开", "常用泰勒展开式", "数学证明", "数学归纳法", "归纳假设", "归纳步骤",
    # 积分、多元、级数、微分方程
    "不定积分", "原函数", "积分常数", "基本积分公式", "换元积分法", "分部积分法", "有理函数积分",
    "定积分", "黎曼和", "积分上限", "积分下限", "黎曼可积", "牛顿-莱布尼茨公式",
    "牛顿莱布尼茨公式", "微积分基本定理", "积分中值定理", "变限积分", "变上限积分",
    "积分上限函数", "莱布尼茨积分求导法则", "反常积分", "广义积分", "瑕积分", "瑕点", "p积分",
    "反常积分收敛", "反常积分发散", "无界函数反常积分", "无穷区间反常积分", "比较判别法", "极限比较判别法", "平面图形面积",
    "旋转体体积", "旋转体侧面积", "旋转侧面积", "曲线弧长", "极坐标面积", "截面面积法",
    "截面法", "变力做功", "液体压力", "弧长微分",
    "多元函数", "二元函数极限", "累次极限", "重极限", "偏导数", "全微分", "方向导数", "梯度",
    "偏导连续", "可微条件", "一阶偏导数", "二阶偏导数", "混合偏导数", "雅可比矩阵",
    "Jacobian矩阵", "雅可比行列式", "偏微分方程", "拉普拉斯方程", "条件极值", "无条件极值",
    "拉格朗日乘数法", "拉格朗日乘子法", "Hessian矩阵", "海塞矩阵",
    "二重积分", "三重积分", "积分区域", "极坐标", "柱坐标", "球坐标", "积分换序", "换序积分", "二重积分换序",
    "交换积分次序", "X型区域", "Y型区域", "极坐标变换", "柱坐标变换", "球坐标变换",
    "曲线积分", "第一类曲线积分", "第二类曲线积分", "对弧长的曲线积分", "对坐标的曲线积分",
    "曲面积分", "第一类曲面积分", "第二类曲面积分", "对面积的曲面积分", "对坐标的曲面积分",
    "向量场", "数量场", "梯度场", "保守场", "势函数", "通量", "环流量", "散度", "旋度",
    "散度定理", "旋度定理", "格林公式", "高斯公式", "斯托克斯公式", "Gauss公式", "Green公式",
    "Stokes公式", "奥斯特罗格拉德斯基公式", "无旋场", "有旋场", "无源场", "有源场",
    "无穷级数", "数项级数", "正项级数", "交错级数", "任意项级数", "变号级数", "级数收敛", "级数发散",
    "部分和", "敛散性", "绝对收敛", "条件收敛", "比值判别法", "根值判别法", "积分判别法",
    "莱布尼茨判别法", "莱布尼茨型级数", "幂级数", "幂级数展开式", "收敛半径", "收敛区间", "收敛域", "阿贝尔定理",
    "泰勒级数", "傅里叶级数", "间接展开法", "微分方程", "常微分方程", "一阶微分方程", "可分离变量方程",
    "一阶线性微分方程", "一阶线性", "伯努利方程", "全微分方程", "积分因子", "二阶微分方程",
    "二阶常系数线性微分方程", "二阶常系数", "可降阶", "缺x型", "缺y型", "齐次通解", "非齐次特解",
    "通解", "特解", "待定系数法", "欧拉方程", "初值问题", "初值条件",
    # 线性代数
    "线性代数", "线代", "行列式", "n阶行列式", "范德蒙德行列式", "余子式", "代数余子式",
    "克拉默法则", "Cramer法则", "拉普拉斯展开定理", "单位矩阵", "零矩阵", "对角矩阵",
    "数量矩阵", "上三角矩阵", "下三角矩阵", "对称矩阵", "反对称矩阵", "转置矩阵",
    "逆矩阵", "伴随矩阵", "可逆矩阵", "分块矩阵", "矩阵加法", "矩阵数乘", "矩阵乘法",
    "矩阵乘积", "矩阵幂", "矩阵高阶幂", "矩阵多项式", "初等变换", "行初等变换", "列初等变换",
    "初等矩阵", "矩阵等价", "行阶梯形矩阵", "行最简形矩阵", "行最简形", "阶梯形", "矩阵的秩", "矩阵秩",
    "行秩", "列秩", "满秩矩阵", "最高阶非零子式", "矩阵方程", "矩阵A", "矩阵B",
    "向量组", "线性组合", "线性表示", "线性相关", "线性无关", "极大线性无关组",
    "向量组的秩", "齐次线性方程组", "非齐次线性方程组", "系数矩阵", "增广矩阵",
    "基础解系", "自由变量", "主元变量", "同解方程组", "公共解", "特征值", "特征向量",
    "特征多项式", "特征方程", "特征子空间", "代数重数", "几何重数", "矩阵相似", "相似矩阵",
    "对角化", "相似对角化", "可对角化", "相似变换矩阵", "P逆AP", "P^{-1}AP", "实对称矩阵正交对角化",
    "正交矩阵", "正交变换", "正交化", "正交对角化", "正交相似", "二次型", "二次型矩阵", "二次型标准形", "二次型规范形",
    "合同矩阵", "矩阵合同", "合同变换", "惯性定理", "惯性指数", "正惯性指数", "负惯性指数",
    "正定二次型", "正定矩阵", "负定矩阵", "顺序主子式", "正定判别法", "施密特正交化",
    "正交基", "标准正交基", "正交向量组", "单位正交向量组", "幂等矩阵", "幂零矩阵", "秩1矩阵",
    "向量空间", "子空间", "零空间", "列空间", "行空间", "解空间", "主元列", "主元行",
    # 概率统计
    "概率论", "随机试验", "样本空间", "样本点", "随机事件", "基本事件", "必然事件", "不可能事件",
    "互斥事件", "对立事件", "条件概率", "概率加法公式", "概率乘法公式", "全概率公式",
    "贝叶斯公式", "Bayes公式", "完备事件组", "古典概型", "几何概型", "伯努利概型",
    "独立重复试验", "事件独立", "相互独立", "两两独立", "随机变量", "一维随机变量",
    "二维随机变量", "多维随机变量", "分布函数", "分布律", "概率密度", "概率密度函数",
    "联合分布", "联合分布函数", "联合概率密度", "边缘分布", "边缘密度", "条件分布", "条件密度",
    "随机变量函数的分布", "Y=g(X)", "Z=g(X,Y)", "卷积公式", "变量变换法", "0-1分布",
    "两点分布", "伯努利分布", "二项分布", "泊松分布", "几何分布", "超几何分布", "均匀分布",
    "指数分布", "正态分布", "标准正态分布", "二维正态分布", "数学期望", "期望公式",
    "随机变量期望", "方差公式", "标准差", "协方差", "协方差公式", "协方差矩阵", "相关系数",
    "Pearson相关系数", "不相关", "独立同分布", "i.i.d.", "原点矩", "中心矩", "矩母函数",
    "切比雪夫不等式", "Chebyshev不等式", "大数定律", "切比雪夫大数定律", "伯努利大数定律",
    "辛钦大数定律", "中心极限定理", "独立同分布中心极限定理", "林德伯格-列维中心极限定理",
    "棣莫弗-拉普拉斯定理", "正态近似", "简单随机样本", "统计量", "样本均值", "样本方差",
    "样本标准差", "样本矩", "抽样分布", "三大分布", "卡方分布", "χ²分布", "t分布", "F分布",
    "正态总体抽样分布", "点估计", "参数估计", "估计量", "估计值", "矩估计", "矩估计法",
    "最大似然估计", "极大似然估计", "似然函数", "对数似然函数", "似然方程", "MLE",
    "无偏估计", "有效估计", "一致估计", "相合估计", "均方误差", "区间估计", "置信区间",
    "置信水平", "置信度", "单侧置信区间", "双侧置信区间", "假设检验", "原假设", "零假设",
    "备择假设", "显著性水平", "拒绝域", "接受域", "检验统计量", "单侧检验", "双侧检验",
    "第一类错误", "第二类错误", "P值", "p-value", "分位数", "上α分位数", "上alpha分位数", "α分位数",
    "矩估计量", "最大似然估计量", "极大似然估计量", "无偏性", "有效性", "一致性", "相合性",
    "泊松过程", "更新过程", "随机游走", "检验临界值", "置信上限", "置信下限",
)


def keyword_regex(keywords: Iterable[str]) -> str:
    return "|".join(re.escape(keyword) for keyword in sorted(set(keywords), key=len, reverse=True))


MATH_EXPLICIT_RE = re.compile(
    keyword_regex(MATH_STRONG_KEYWORDS)
    + r"|(?:20\d{2}|0?[9]|1\d|2\d)\s*年\s*(?:数[一二三]|数学[一二三]|math[123])\s*第\s*(?:\d{1,2}|[一二三四五六七八九十]{1,3})\s*[题问]"
    + r"|\\lim|\blim\b|x\s*→\s*x0|n\s*→\s*∞|ε-δ|ε-N|1\^∞型|1\^\\infty型|[A-Z]\s*~\s*N\s*\(|P\s*\("
)
MATH_FOLLOWUP_RE = re.compile(
    r"第\s*\d+\s*步|这一步|上一步|这里为什么|怎么来的|为什么成立|"
    r"上面.*式子|这个式子|那个式子|这个余项|余项呢|展开点|"
    r"这个积分|那个积分|这个矩阵|这个函数"
)
MATH_HISTORY_RE = re.compile(
    rf"{MATH_EXPLICIT_RE.pattern}|\\int|\\lim|lim_|题号|解法|推导|化简|代入"
)
POLITICS_STRONG_KEYWORDS = (
    '马克思主义基本原理', '马克思主义哲学', '哲学基本问题', '思维和存在的关系问题', '物质和意识的关系问题', '唯物主义', '唯心主义', '可知论',
    '不可知论', '辩证法', '形而上学', '马克思主义物质观', '马克思主义实践观', '世界的物质统一性', '主观能动性', '客观规律性',
    '规律的客观性', '意识的能动作用', '实践观点', '实践的基本形式', '实践的主体', '实践的客体', '实践的中介', '人与自然',
    '自然界和人类社会', '世界物质统一性', '意识起源', '意识本质', '意识作用', '主观能动性和客观规律性', '尊重客观规律', '发挥主观能动性',
    '唯物辩证法', '普遍联系', '永恒发展', '矛盾分析法', '矛盾同一性', '矛盾斗争性', '矛盾普遍性', '矛盾特殊性',
    '主要矛盾', '次要矛盾', '矛盾主要方面', '矛盾次要方面', '两点论', '重点论', '两点论和重点论统一', '质量互变规律',
    '关节点', '否定之否定规律', '辩证否定观', '扬弃', '事物发展的前进性和曲折性', '对立统一规律', '联系和发展的基本环节', '原因和结果',
    '必然和偶然', '可能和现实', '现象和本质', '内容和形式', '认识论', '实践和认识', '认识的本质', '认识的主体',
    '认识的客体', '感性认识', '理性认识', '感性认识到理性认识', '理性认识到实践', '认识运动的反复性', '认识运动的无限性', '客观真理',
    '绝对真理', '相对真理', '真理的绝对性', '真理的相对性', '真理和谬误', '真理标准', '实践是检验真理的唯一标准', '价值评价',
    '真理和价值的统一', '认识世界', '改造世界', '历史唯物主义', '社会存在', '社会意识', '社会存在决定社会意识', '社会意识相对独立性',
    '生产力', '生产关系', '经济基础', '上层建筑', '生产力和生产关系矛盾运动', '经济基础和上层建筑矛盾运动', '社会基本矛盾', '社会主要矛盾',
    '阶级斗争', '社会革命', '科学技术', '人民群众', '人民群众是历史的创造者', '群众观点', '群众路线', '杰出人物',
    '历史人物', '人的本质', '人的自由全面发展', '社会形态', '社会形态更替', '社会发展动力', '商品经济', '使用价值',
    '交换价值', '具体劳动', '抽象劳动', '私人劳动', '社会劳动', '价值量', '社会必要劳动时间', '劳动生产率',
    '价值规律', '货币职能', '商品拜物教', '劳动力商品', '剩余价值', '剩余价值率', '必要劳动时间', '剩余劳动时间',
    '不变资本', '可变资本', '绝对剩余价值', '相对剩余价值', '超额剩余价值', '资本积累', '资本有机构成', '资本原始积累',
    '资本积累的一般规律', '资本循环', '资本周转', '固定资本', '流动资本', '社会总资本再生产', '简单再生产', '扩大再生产',
    '产业资本', '商业资本', '借贷资本', '银行资本', '利润率', '平均利润', '平均利润率', '生产价格',
    '平均利润率下降规律', '资本拜物教', '经济危机', '资本主义经济危机', '生产相对过剩', '资本主义基本矛盾', '金融资本', '国家垄断资本主义',
    '经济全球化', '科学社会主义', '空想社会主义', '社会主义从空想到科学', '两个必然', '两个决不会', '资本主义灭亡', '社会主义胜利',
    '无产阶级', '无产阶级政党', '无产阶级革命', '无产阶级专政', '社会主义民主', '共产主义', '共产主义社会', '各尽所能按需分配',
    '自由人联合体', '马克思主义中国化', '马克思主义时代化', '马克思主义中国化时代化', '两个结合', '把马克思主义基本原理同中国具体实际相结合', '把马克思主义基本原理同中华优秀传统文化相结合', '理论创新',
    '实践创新', '中国化时代化的马克思主义', '毛泽东思想', '中国特色社会主义理论体系', '习近平新时代中国特色社会主义思想', '毛泽东思想活的灵魂', '实事求是', '新民主主义革命理论',
    '社会主义革命理论', '社会主义建设理论', '党的建设理论', '政策和策略理论', '思想政治工作', '统一战线', '武装斗争', '党的建设',
    '三大法宝', '新民主主义革命', '新民主主义革命总路线', '无产阶级领导权', '人民大众', '反帝反封建反官僚资本主义', '新民主主义革命对象', '新民主主义革命动力',
    '新民主主义革命领导力量', '新民主主义革命性质', '新民主主义革命前途', '新民主主义基本纲领', '新民主主义政治纲领', '新民主主义经济纲领', '新民主主义文化纲领', '农村包围城市',
    '武装夺取政权', '工农武装割据', '土地革命', '过渡时期总路线', '一化三改', '社会主义工业化', '农业社会主义改造', '手工业社会主义改造',
    '资本主义工商业社会主义改造', '和平赎买', '国家资本主义', '社会主义基本制度确立', '三大改造', '社会主义改造完成', '社会主义建设道路初步探索', '十大关系',
    '正确处理人民内部矛盾', '人民内部矛盾', '敌我矛盾', '社会主义社会基本矛盾', '调动一切积极因素', '独立完整工业体系', '国民经济体系', '四个现代化',
    '邓小平理论', '社会主义本质', '解放生产力', '发展生产力', '消灭剥削', '消除两极分化', '共同富裕', '社会主义初级阶段',
    '党的基本路线', '一个中心两个基本点', '改革开放', '社会主义市场经济', '两手抓两手都要硬', '一国两制', '三个代表重要思想', '始终代表中国先进生产力的发展要求',
    '始终代表中国先进文化的前进方向', '始终代表中国最广大人民的根本利益', '科学发展观', '第一要义是发展', '核心立场是以人为本', '基本要求是全面协调可持续', '根本方法是统筹兼顾', '新时代',
    '中国特色社会主义新时代', '社会主要矛盾变化', '人民日益增长的美好生活需要', '不平衡不充分的发展', '中华民族伟大复兴', '中国梦', '强国建设', '民族复兴',
    '两个确立', '两个维护', '四个意识', '四个自信', '四个伟大', '伟大斗争', '伟大工程', '伟大事业',
    '伟大梦想', '十个明确', '十四个坚持', '十三个方面成就', '六个必须坚持', '人民至上', '自信自立', '守正创新',
    '问题导向', '系统观念', '胸怀天下', '中国式现代化', '人口规模巨大的现代化', '全体人民共同富裕的现代化', '物质文明和精神文明相协调的现代化', '人与自然和谐共生的现代化',
    '走和平发展道路的现代化', '中国式现代化本质要求', '高质量发展', '全过程人民民主', '丰富人民精神世界', '人与自然和谐共生', '人类命运共同体', '创造人类文明新形态',
    '两步走战略安排', '全面建成社会主义现代化强国', '基本实现社会主义现代化', '社会主义现代化强国', '全面建设社会主义现代化国家', '新发展阶段', '新发展理念', '新发展格局',
    '创新发展', '协调发展', '绿色发展', '开放发展', '共享发展', '供给侧结构性改革', '扩大内需', '乡村振兴',
    '区域协调发展', '社会主义基本经济制度', '公有制为主体', '多种所有制经济共同发展', '按劳分配为主体', '多种分配方式并存', '社会主义市场经济体制', '有效市场',
    '有为政府', '现代化经济体系', '创新驱动发展战略', '实体经济', '数字经济', '新质生产力', '乡村振兴战略', '区域协调发展战略',
    '党的领导', '人民当家作主', '依法治国有机统一', '人民民主专政', '人民代表大会制度', '中国共产党领导的多党合作和政治协商制度', '民族区域自治制度', '基层群众自治制度',
    '协商民主', '选举民主', '民主集中制', '爱国统一战线', '社会主义法治国家', '全面依法治国', '社会主义先进文化', '文化自信',
    '意识形态工作', '马克思主义在意识形态领域指导地位', '社会主义核心价值观', '中华优秀传统文化', '革命文化', '文化强国', '精神文明建设', '网络强国',
    '讲好中国故事', '增强中华文明传播力影响力', '以人民为中心', '保障和改善民生', '收入分配', '就业优先', '教育强国', '健康中国',
    '社会保障体系', '基层治理', '社会治理共同体', '共建共治共享', '人民生活品质', '全过程人民民主基层实践', '生态文明', '生态文明建设',
    '绿水青山就是金山银山', '美丽中国', '生态环境保护', '碳达峰', '碳中和', '山水林田湖草沙一体化保护和系统治理', '最严格生态环境保护制度', '全面深化改革',
    '国家治理体系和治理能力现代化', '完善和发展中国特色社会主义制度', '改革系统集成', '顶层设计', '摸着石头过河', '全面深化改革总目标', '进一步全面深化改革', '习近平法治思想',
    '中国特色社会主义法治道路', '法治中国', '法治国家', '法治政府', '法治社会', '依宪治国', '依宪执政', '科学立法',
    '严格执法', '公正司法', '全民守法', '建设中国特色社会主义法治体系', '建设社会主义法治国家', '全面从严治党', '党的自我革命', '新时代党的建设总要求',
    '政治建设', '思想建设', '组织建设', '作风建设', '纪律建设', '制度建设', '反腐败斗争', '中央八项规定',
    '四风', '党的群众路线教育实践活动', '不忘初心牢记使命主题教育', '党史学习教育', '党纪学习教育', '三严三实', '两学一做', '依规治党',
    '党内法规', '总体国家安全观', '国家安全体系', '国家安全能力', '政治安全', '经济安全', '文化安全', '社会安全',
    '网络安全', '生态安全', '军事安全', '海外利益安全', '平安中国', '强军思想', '党对人民军队绝对领导', '听党指挥',
    '能打胜仗', '作风优良', '世界一流军队', '港人治港', '澳人治澳', '高度自治', '九二共识', '一个中国原则',
    '祖国完全统一', '中国特色大国外交', '全人类共同价值', '一带一路', '全球发展倡议', '全球安全倡议', '全球文明倡议', '中国近现代史纲要',
    '鸦片战争', '第一次鸦片战争', '第二次鸦片战争', '南京条约', '天津条约', '北京条约', '马关条约', '辛丑条约',
    '半殖民地半封建社会', '近代中国社会主要矛盾', '近代中国两大历史任务', '反帝反封建', '太平天国运动', '天朝田亩制度', '资政新篇', '洋务运动',
    '中体西用', '师夷长技以制夷', '戊戌维新运动', '百日维新', '辛亥革命', '三民主义', '民族主义', '民权主义',
    '民生主义', '中华民国', '临时约法', '旧民主主义革命', '新文化运动', '民主与科学', '五四运动', '五四精神',
    '马克思主义传播', '李大钊', '陈独秀', '中国早期马克思主义思想运动', '工人阶级登上政治舞台', '新民主主义革命开端', '中国共产党成立', '中共一大',
    '中共二大', '中共三大', '中共四大', '民主革命纲领', '国共合作', '第一次国共合作', '革命统一战线', '国民革命',
    '大革命', '北伐战争', '四一二反革命政变', '七一五反革命政变', '大革命失败', '南昌起义', '八七会议', '秋收起义',
    '广州起义', '井冈山革命根据地', '古田会议', '中华苏维埃共和国', '遵义会议', '长征', '长征精神', '瓦窑堡会议',
    '抗日民族统一战线', '九一八事变', '华北事变', '一二九运动', '西安事变', '七七事变', '卢沟桥事变', '第二次国共合作',
    '全面抗战路线', '片面抗战路线', '洛川会议', '持久战', '论持久战', '敌后战场', '正面战场', '百团大战',
    '延安整风运动', '六届六中全会', '中共七大', '毛泽东思想写入党章', '抗日战争胜利', '重庆谈判', '双十协定', '内战爆发',
    '人民解放战争', '土地改革', '中国土地法大纲', '三大战役', '辽沈战役', '淮海战役', '平津战役', '七届二中全会',
    '两个务必', '渡江战役', '南京解放', '中国人民政治协商会议', '共同纲领', '中华人民共和国成立', '新中国成立', '抗美援朝',
    '土地改革运动', '镇压反革命', '三反五反运动', '中共八大', '社会主义建设总路线', '大跃进', '人民公社化运动', '七千人大会',
    '四清运动', '文化大革命', '二月抗争', '四五运动', '粉碎四人帮', '真理标准问题讨论', '十一届三中全会', '家庭联产承包责任制',
    '经济特区', '南方谈话', '中共十二大', '中共十三大', '中共十四大', '中共十五大', '中共十六大', '中共十七大',
    '中共十八大', '中共十九大', '中共二十大', '全面建成小康社会', '脱贫攻坚', '十二月会议', '义和团运动', '抗日战争',
    '解放战争', '思想道德与法治', '人生观', '世界观', '价值观', '人生目的', '人生态度', '人生价值',
    '自我价值', '社会价值', '人生价值评价', '人生价值实现', '服务人民', '奉献社会', '个人与社会', '个人理想与社会理想',
    '理想信念', '马克思主义信仰', '中国特色社会主义共同理想', '共产主义远大理想', '个人理想', '社会理想', '理想信念是精神之钙', '立大志',
    '明大德', '成大才', '担大任', '中国精神', '民族精神', '时代精神', '爱国主义', '改革创新',
    '伟大创造精神', '伟大奋斗精神', '伟大团结精神', '伟大梦想精神', '爱国爱党爱社会主义相统一', '国家安全意识', '核心价值观', '价值准则',
    '价值目标', '价值取向', '价值规范', '道德本质', '道德功能', '道德作用', '中华传统美德', '中国革命道德',
    '社会主义道德', '为人民服务', '集体主义', '社会公德', '职业道德', '家庭美德', '个人品德', '网络道德',
    '诚信道德', '志愿服务', '见义勇为', '法治思维', '法治观念', '社会主义法治观念', '社会主义法治道路', '法律权威',
    '尊法学法守法用法', '法律面前人人平等', '权利义务相统一', '依法行使权利', '依法履行义务', '宪法', '宪法法律至上', '宪法权威',
    '宪法宣誓制度', '国家宪法日', '基本权利', '基本义务', '国家机构', '公民权利', '公民义务', '民法典',
    '民事权利', '民事义务', '民事责任', '民事法律行为', '违约责任', '侵权责任', '缔约过失责任', '不可抗力',
    '人格权', '知识产权', '继承权', '刑法', '刑事责任', '正当防卫', '紧急避险', '行政法',
    '行政行为', '行政处罚', '行政复议', '行政诉讼', '民事诉讼', '刑事诉讼', '法律援助', '司法救助',
    '程序正义', '实体正义', '肖秀荣', '腿姐', '徐涛', '陆寓丰', '米鹏', '肖四',
    '肖八', '1000题', '精讲精练', '核心考案', '冲刺背诵手册', '背诵手册', '腿四', '徐六',
    '米三', '米六', '政治选择题', '政治单选题', '政治多选题', '政治大题', '政治分析题', '马原大题',
    '毛中特大题', '史纲大题', '思修大题', '当代大题', '政治背诵', '政治刷题', '政治错题', '政治押题',
    '政治主观题', '政治客观题', '考研政治', '政治题', '马原', '马克思主义', '毛中特', '史纲',
    '思修', '思想道德', '思想道德修养与法律基础', '思修法基', '实践是检验真理', '逻辑证明', '实践检验', '新民主主义',
    '官僚资本主义', '混合所有制', '反对本本主义',
)
CURRENT_AFFAIRS_STRONG_KEYWORDS = (
    '时政', '时事', '时事政治', '新闻热点', '热点新闻', '本月时政', '会议精神', '政策解读',
    '形势与政策', '中央经济工作会议', '中央农村工作会议', '全国两会', '政府工作报告', '高质量发展', '新质生产力', '现代化产业体系',
    '共同富裕', '乡村振兴', '区域协调发展', '扩大内需', '科技自立自强', '教育强国', '人才强国', '健康中国',
    '数字中国', '美丽中国', '双碳', '碳达峰', '碳中和', '党的二十大', '二十届一中全会', '二十届二中全会',
    '二十届三中全会', '中国式现代化', '全面深化改革', '党纪学习教育', '全面从严治党', '党的自我革命', '反腐败斗争', '中央八项规定',
    '中国特色大国外交', '人类命运共同体', '全人类共同价值', '一带一路', '全球发展倡议', '全球安全倡议', '全球文明倡议', '多边主义',
    '经济全球化', '全球治理', '国际秩序', '国际格局', '百年未有之大变局', '中美关系', '中俄关系', '中欧关系',
    '周边外交', '大国关系', '南南合作', '联合国', '金砖国家', '上合组织', '亚太经合组织', '新型举国体制',
)
CURRENT_AFFAIRS_EXPLICIT_RE = re.compile(keyword_regex(CURRENT_AFFAIRS_STRONG_KEYWORDS) + r"|近期.*(?:新闻|政策|热点)")
POLITICS_EXPLICIT_RE = re.compile(keyword_regex(POLITICS_STRONG_KEYWORDS))
ENGLISH_EXPLICIT_RE = re.compile(r"考研英语|英语[一二]?|阅读理解|英语作文|小作文|大作文|完形填空|新题型|考研翻译")

# 模糊真题引用的局部模式
_FUZZY_EXAM_YEAR_RE = re.compile(r"(?:20\d{2}|0?[9]|1\d|2\d)\s*年")
_FUZZY_EXAM_QUESTION_RE = re.compile(r"(?:第\s*)?(?:\d{1,2}|[一二三四五六七八九十]{1,3})\s*(?:题|问|[大个]题)")
_FUZZY_EXAM_SUBJECT_RE = re.compile(r"数学[一二三]|数[一二三]|math[123]")
_FUZZY_EXAM_VAGUE_RE = re.compile(r"真题|历年真题|考题|考研题|这道题|那道题|第\s*[几多少]\s*题|第[一二三四五六七八九十]\s*[个大题问]")


def analyze_missing_info(user_input: str, history: list[dict[str, str]] | None = None) -> dict[str, Any]:
    text = user_input.strip()
    result: dict[str, Any] = {
        "has_subject_hint": False,
        "has_year": False,
        "has_question_number": False,
        "has_exam_type": False,
        "likely_math": False,
        "likely_kaoyan": bool(re.search(r"考研|真题|考题|数[一二三]|数学", text)),
        "missing": [],
    }
    result["has_year"] = bool(_FUZZY_EXAM_YEAR_RE.search(text))
    result["has_question_number"] = bool(_FUZZY_EXAM_QUESTION_RE.search(text))
    result["has_exam_type"] = bool(_FUZZY_EXAM_SUBJECT_RE.search(text))
    result["has_subject_hint"] = bool(CURRENT_AFFAIRS_EXPLICIT_RE.search(text) or
                                      POLITICS_EXPLICIT_RE.search(text) or
                                      ENGLISH_EXPLICIT_RE.search(text) or
                                      MATH_EXPLICIT_RE.search(text))
    if not result["has_subject_hint"]:
        if history_suggests_math(history):
            result["likely_math"] = True
    missing = result["missing"]
    if result["has_year"] and result["has_question_number"] and not result["has_exam_type"]:
        missing.append("exam_type")
    elif not result["has_year"] and result["has_question_number"]:
        missing.append("year")
    elif result["has_year"] and not result["has_question_number"]:
        missing.append("question_number")
    elif not result["has_subject_hint"] and not result["has_year"] and not result["has_question_number"]:
        if _FUZZY_EXAM_VAGUE_RE.search(text):
            missing.append("exam_specifics")
        elif not result["likely_math"]:
            missing.append("subject")
    return result


def build_ambiguous_clarification(user_input: str, history: list[dict[str, str]]) -> str:
    info = analyze_missing_info(user_input, history)
    missing = info["missing"]
    hard_rules: list[tuple[list[str], str]] = [
        (["exam_type"], "请问您指的是数学一、数学二还是数学三的题？"),
        (["year"], "请问是哪一年的题？比如 2020、2021。"),
        (["question_number"], "请问是第几题？请提供具体题号。"),
        (["exam_specifics"], "请提供更具体的信息，比如哪一年、哪一科的哪道真题？例如 2021 年数一第 9 题怎么做。"),
        (["subject"], "请问您想咨询什么内容？我可以帮您解答数学题、查询考研时政热点。"),
    ]
    for triggers, answer in hard_rules:
        if sorted(missing) == sorted(triggers):
            return answer
    if info["has_year"] and info["has_question_number"] and not info["has_exam_type"]:
        return "请问您指的是数学一、数学二还是数学三的题？"
    if info["likely_math"]:
        return "能否提供更具体的信息？比如年份、科目（数一/数二/数三）和题号。"
    return "请问您想咨询什么内容？我可以帮您解答数学题（如 2021 年数一第 9 题）、查询考研时政热点。"


def history_suggests_math(history: list[dict[str, str]] | None) -> bool:
    if not history:
        return False
    recent_text = "\n".join(str(item.get("content", "")) for item in history[-8:])
    return bool(MATH_HISTORY_RE.search(recent_text))


def classify_subject_heuristic(
    user_input: str,
    has_images: bool = False,
    history: list[dict[str, str]] | None = None,
) -> str | None:
    if MATH_FOLLOWUP_RE.search(user_input) and history_suggests_math(history):
        return "math"
    if MATH_EXPLICIT_RE.search(user_input):
        return "math"
    if CURRENT_AFFAIRS_EXPLICIT_RE.search(user_input):
        return "politics"
    if POLITICS_EXPLICIT_RE.search(user_input):
        return "politics"
    if ENGLISH_EXPLICIT_RE.search(user_input):
        return "english"
    return None


WEAK_FOLLOWUP_HINT_RE = re.compile(
    r"这个|那个|它|这里|上面|刚才|上一|继续|详细|展开|"
    r"为什么|咋来的|怎么来的|还成立|可以吗|对吗|"
    r"我说的是|我的意思|不是这个|换成|那如果|这个呢|那个呢"
)
MULTI_PARENT_FOLLOWUP_HINT_RE = re.compile(
    r"第[一二三四五六七八九十\d]+个|第[一二三四五六七八九十\d]+题|"
    r"这两个|那两个|二者|两者|分别|对比|区别|联系|另一个|前一个|后一个"
)
CONTEXTUAL_FOLLOWUP_ANCHOR_RE = re.compile(
    r"这道题|那道题|这题|那题|上一题|上一道|刚才.*题|之前.*题|"
    r"重新计算|重新算|写错|改错|应该是|更正|改成|换成|"
    r"能不能.*解决这道题|能否.*解决这道题"
)
COMPOSITE_FOLLOWUP_NEW_TOPIC_RE = re.compile(
    r"什么是|是什么|讲一下|解释一下|介绍一下|总结一下|怎么理解|如何理解|"
    r"定义|概念|定理|公式|方法|原理|规则"
)
COMPOSITE_FOLLOWUP_APPLICATION_RE = re.compile(
    r"能不能|能否|能用吗|能不能用|能否用|可以用吗|可不可以|是否可以|"
    r"能不能使用|能否使用|是否能使用|适合.*吗|"
    r"用.*(?:证明|解决|求解|计算|解释|处理|分析)"
)
INDEPENDENT_COMMAND_RE = re.compile(
    r"^(?:讲一下|解释一下|总结一下|帮我|请问|什么是|如何|怎么做|求|证明)"
)


def is_composite_followup_input(text: str, has_history: bool) -> bool:
    if not has_history or not CONTEXTUAL_FOLLOWUP_ANCHOR_RE.search(text):
        return False
    return bool(
        COMPOSITE_FOLLOWUP_NEW_TOPIC_RE.search(text)
        or COMPOSITE_FOLLOWUP_APPLICATION_RE.search(text)
    )


def classify_followup_heuristic(user_input: str, history: list[dict[str, str]] | None = None) -> str | None:
    text = user_input.strip()
    if not text:
        return None
    has_history = bool(history)
    if re.search(r"(?:20\d{2}|0?[9]|1\d|2\d).*(?:math[123]|数学[一二三]|数[一二三]).*(?:question|第\s*\d+|题)", text, flags=re.I):
        return "independent"
    if MATH_FOLLOWUP_RE.search(text) and history_suggests_math(history):
        return "step_followup"
    if MULTI_PARENT_FOLLOWUP_HINT_RE.search(text):
        return "contextual_nonstep_followup"
    if is_composite_followup_input(text, has_history):
        return "contextual_nonstep_followup"
    if CONTEXTUAL_FOLLOWUP_ANCHOR_RE.search(text):
        return "contextual_nonstep_followup"
    if WEAK_FOLLOWUP_HINT_RE.search(text):
        return "weak_nonstep_followup"
    if re.search(r"^(那|再|继续|如果|你刚|刚才|回到|比较\s*turn\d+)", text, flags=re.I) and has_history:
        return None
    if not has_history and (classify_subject_heuristic(text, history=history) or INDEPENDENT_COMMAND_RE.search(text)):
        return "independent"
    return None


def normalize_subject(value: Any, fallback: str = "unsupported") -> str:
    subject = str(value or fallback)
    if subject == "current_affairs":
        return "politics"
    if subject not in {"math", "politics", "english", "unsupported", ""}:
        return fallback
    return subject


def subject_keywords(subject: str) -> tuple[str, ...]:
    normalized = normalize_subject(subject, fallback="")
    if normalized == "math":
        return MATH_STRONG_KEYWORDS
    if normalized == "politics":
        return (*POLITICS_STRONG_KEYWORDS, *CURRENT_AFFAIRS_STRONG_KEYWORDS)
    return ()


def matched_subject_keywords(text: str, subject: str) -> set[str]:
    if not text:
        return set()
    lowered = text.lower()
    return {
        keyword
        for keyword in subject_keywords(subject)
        if keyword and keyword.lower() in lowered
    }


def normalize_followup_category(value: Any, fallback: str = "independent") -> str:
    category = str(value or fallback)
    if category not in {"independent", "step_followup", "weak_nonstep_followup", "contextual_nonstep_followup", "ambiguous"}:
        return fallback
    return category


def candidate_turn_ids(candidates: list[dict[str, Any]]) -> set[int]:
    ids: set[int] = set()
    for turn in candidates:
        try:
            ids.add(int(turn.get("turn_id")))
        except (TypeError, ValueError):
            continue
    return ids


def normalize_parent_ids(data: dict[str, Any], candidates: list[dict[str, Any]]) -> tuple[int | None, list[int]]:
    valid_ids = candidate_turn_ids(candidates)
    values: list[Any] = []
    raw_values = data.get("parent_turn_ids")
    if isinstance(raw_values, list):
        values.extend(raw_values)
    if data.get("parent_turn_id") is not None:
        values.append(data.get("parent_turn_id"))
    parent_ids: list[int] = []
    for value in values:
        try:
            parent_id = int(value)
        except (TypeError, ValueError):
            continue
        if parent_id in valid_ids and parent_id not in parent_ids:
            parent_ids.append(parent_id)
    parent_ids.sort()
    parent_turn_id = None
    try:
        raw_parent = int(data.get("parent_turn_id"))
    except (TypeError, ValueError):
        raw_parent = None
    if raw_parent in valid_ids:
        parent_turn_id = raw_parent
    elif parent_ids:
        parent_turn_id = parent_ids[-1]
    return parent_turn_id, parent_ids


def route_with_llm(
    user_input: str,
    history: list[dict[str, str]],
    candidates: list[dict[str, Any]],
    client: Any,
    metrics: RuntimeMetrics | None = None,
    subject_hint: str | None = None,
    subject_locked: bool = False,
    followup_hint: str | None = None,
    followup_locked: bool = False,
    has_images: bool = False,
    image_context: dict[str, Any] | None = None,
) -> RouteDecision:
    candidate_text = "\n\n".join(
        f"[turn {turn.get('turn_id')}]\n{turn_context_block(turn, 900)}"
        for turn in candidates
    )
    payload = {
        "user_input": user_input,
        "recent_history": history[-ROUTING_HISTORY_TURNS * 2:],
        "candidate_turns": candidate_text,
        "has_images": has_images,
        "subject_hint": subject_hint,
        "subject_locked": subject_locked,
        "followup_hint": followup_hint,
        "followup_locked": followup_locked,
    }
    if has_images and image_context:
        payload["image_context"] = image_context
    global_client = make_global_client(client)
    model_name = global_model_name()
    llm_started = time.perf_counter()
    response = global_client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": ROUTE_CLASSIFIER_PROMPT},
            {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
        ],
        temperature=global_temperature(0),
    )
    raw_content = str(response.choices[0].message.content or "")
    if metrics is not None:
        metrics.llm_calls += 1
        usage = record_usage(metrics, response, "route_classifier", model=model_name, started_at=llm_started)
        usage["raw_content_chars"] = len(raw_content)
    parse_error = None
    try:
        data = legacy_agent.parse_json_object(raw_content or "{}")
    except Exception as exc:
        parse_error = str(exc)
        data = {}
    log_route_debug(
        metrics,
        user_input=user_input,
        model=model_name,
        raw_content=raw_content,
        parsed=data,
        parse_error=parse_error,
    )
    subject = normalize_subject(subject_hint if subject_locked else data.get("subject"), subject_hint or "unsupported")
    category = normalize_followup_category(
        followup_hint if followup_locked else data.get("followup_category", data.get("category")),
        followup_hint or "independent",
    )
    parent_id, parent_ids = normalize_parent_ids(data, candidates)
    if category in {"independent", "ambiguous"}:
        parent_id = None
        parent_ids = []
    reason = str(data.get("reason") or "")
    parent_subject = infer_subject_from_parent_turns(candidates, parent_ids, subject)
    if category != "independent" and parent_subject:
        if subject != parent_subject:
            reason = f"{reason}；追问学科继承父节点 {parent_subject}。".strip("；")
        subject = parent_subject
    clarification = data.get("clarification")
    return RouteDecision(
        subject=subject,
        is_followup=bool(data.get("is_followup")) if not followup_locked else category != "independent",
        followup_category=category,
        parent_turn_id=parent_id,
        parent_turn_ids=parent_ids,
        reason=reason,
        clarification=clarification.strip() if isinstance(clarification, str) and clarification.strip() else None,
    )


_last_clarification: str | None = None


def classify_subject(
    user_input: str,
    history: list[dict[str, str]],
    has_images: bool = False,
    client: Any | None = None,
    metrics: RuntimeMetrics | None = None,
    image_context: dict[str, Any] | None = None,
) -> str:
    heuristic = classify_subject_heuristic(user_input, has_images, history)
    if heuristic:
        return heuristic
    if client is None:
        return "unsupported"
    route = route_with_llm(
        user_input,
        history,
        [],
        client,
        metrics,
        followup_hint=classify_followup_heuristic(user_input, history),
        has_images=has_images,
        image_context=image_context,
    )
    if route.clarification:
        global _last_clarification
        _last_clarification = route.clarification
    if not subject_has_routing_evidence(route.subject, user_input, history, [], has_images, image_context):
        _last_clarification = build_ambiguous_clarification(user_input, history)
        return "unsupported"
    return route.subject


def should_use_unified_route(has_images: bool, recent_turns: list[dict[str, Any]]) -> bool:
    return context_followup_tools_enabled() and bool(recent_turns)


def turns_to_messages(turns: list[dict[str, Any]]) -> list[dict[str, str]]:
    messages: list[dict[str, str]] = []
    for turn in turns:
        user_query = str(turn.get("user_query") or "")
        assistant_answer = str(turn.get("assistant_answer") or turn.get("assistant_answer_preview") or "")
        if user_query:
            messages.append({"role": "user", "content": user_query})
        if assistant_answer:
            messages.append({"role": "assistant", "content": assistant_answer})
    return messages


def infer_subject_from_turns(turns: list[dict[str, Any]]) -> str | None:
    text = "\n".join(turn_context_block(turn, 600) for turn in turns)
    if not text.strip():
        return None
    if POLITICS_EXPLICIT_RE.search(text):
        return "politics"
    if CURRENT_AFFAIRS_EXPLICIT_RE.search(text):
        return "politics"
    if ENGLISH_EXPLICIT_RE.search(text):
        return "english"
    if MATH_HISTORY_RE.search(text) or re.search(
        r"cosh|sinh|Taylor|泰勒|积分|导数|函数|定理|连续|可导|矩阵|概率|"
        r"\b(?:lim|sin|cos|tan|ln|log|det)\b|[a-zA-Z]\s*\(|\^",
        text,
        flags=re.I,
    ):
        return "math"
    for turn in reversed(turns):
        route = turn.get("route")
        if isinstance(route, dict):
            subject = normalize_subject(route.get("subject"), fallback="")
            if subject:
                return subject
    return None


def infer_subject_from_parent_turns(
    recent_turns: list[dict[str, Any]],
    parent_turn_ids: list[int],
    current_subject: str | None = None,
) -> str | None:
    if not parent_turn_ids:
        return None
    turns_by_id: dict[int, dict[str, Any]] = {}
    for turn in recent_turns:
        try:
            turns_by_id[int(turn.get("turn_id"))] = turn
        except (TypeError, ValueError):
            continue
    subjects: list[str] = []
    for parent_id in parent_turn_ids:
        turn = turns_by_id.get(parent_id)
        if not turn:
            continue
        subject: str | None = None
        route = turn.get("route")
        if isinstance(route, dict):
            subject = normalize_subject(route.get("subject"), fallback="")
        if not subject:
            subject = classify_subject_heuristic(turn_context_block(turn, 600))
        if subject and subject != "unsupported" and subject not in subjects:
            subjects.append(subject)
    if not subjects:
        return None
    if len(subjects) == 1:
        return subjects[0]
    normalized_current = normalize_subject(current_subject, fallback="")
    if normalized_current in subjects:
        return normalized_current
    return subjects[-1]


def turn_subject(turn: dict[str, Any]) -> str | None:
    route = turn.get("route")
    if isinstance(route, dict):
        subject = normalize_subject(route.get("subject"), fallback="")
        if subject:
            return subject
    return classify_subject_heuristic(turn_context_block(turn, 600))


def subject_hint_from_image_context(image_context: dict[str, Any] | None) -> str | None:
    if not image_context:
        return None
    subject = normalize_subject(image_context.get("subject_hint"), fallback="")
    if not subject or subject == "unsupported":
        return None
    try:
        confidence = float(image_context.get("confidence", 0.0) or 0.0)
    except (TypeError, ValueError):
        confidence = 0.0
    if confidence < 0.7:
        return None
    image_text = "\n".join([
        str(image_context.get("ocr_text") or ""),
        str(image_context.get("visual_summary") or ""),
    ])
    if classify_subject_heuristic(image_text) == subject:
        return subject
    return subject


def route_subject_hint(
    user_input: str,
    recent_turns: list[dict[str, Any]],
    has_images: bool = False,
    image_context: dict[str, Any] | None = None,
) -> tuple[str | None, bool]:
    current_hint = classify_subject_heuristic(user_input, has_images=False, history=None)
    if current_hint:
        return current_hint, True
    image_hint = subject_hint_from_image_context(image_context) if has_images else None
    if image_hint:
        return image_hint, True
    return infer_subject_from_turns(recent_turns), False


IMAGE_NEW_PROBLEM_RE = re.compile(
    r"^\s*(?:这道题|这题|那这题|这个题|这个|这张图|图片)?\s*"
    r"(?:怎么做|如何做|求解|解一下|看一下|帮我看看|呢)?[？?。！!\s]*$"
)
IMAGE_CONTEXT_LINK_RE = re.compile(r"上一|刚才|之前|沿用|比较|对比|区别|换成|改成|继续|同样|类似")


def image_context_is_new_problem(
    user_input: str,
    recent_turns: list[dict[str, Any]],
    image_context: dict[str, Any] | None,
) -> bool:
    image_subject = subject_hint_from_image_context(image_context)
    if not image_subject:
        return False
    if IMAGE_CONTEXT_LINK_RE.search(user_input):
        return False
    if not IMAGE_NEW_PROBLEM_RE.search(user_input):
        return False
    recent_subject = infer_subject_from_turns(recent_turns)
    return recent_subject is None or recent_subject != image_subject


def subject_has_routing_evidence(
    subject: str,
    user_input: str,
    history: list[dict[str, str]],
    recent_turns: list[dict[str, Any]],
    has_images: bool = False,
    image_context: dict[str, Any] | None = None,
) -> bool:
    if subject == "unsupported":
        return True
    if has_images and image_context:
        image_subject = normalize_subject(image_context.get("subject_hint"), fallback="")
        try:
            confidence = float(image_context.get("confidence", 0.0) or 0.0)
        except (TypeError, ValueError):
            confidence = 0.0
        image_text = "\n".join([
            str(image_context.get("ocr_text") or ""),
            str(image_context.get("visual_summary") or ""),
        ])
        if image_subject == subject and confidence >= 0.55:
            return True
        if classify_subject_heuristic(image_text) == subject:
            return True
    route_history = [*history, *turns_to_messages(recent_turns)]
    heuristic = classify_subject_heuristic(user_input, has_images=has_images, history=route_history)
    if heuristic == subject:
        return True
    return infer_subject_from_turns(recent_turns) == subject


def build_route_decision(
    user_input: str,
    history: list[dict[str, str]],
    recent_turns: list[dict[str, Any]],
    has_images: bool,
    client: Any,
    metrics: RuntimeMetrics,
    image_context: dict[str, Any] | None = None,
) -> RouteDecision:
    route_history = [*history, *turns_to_messages(recent_turns)]
    subject_hint, subject_locked = route_subject_hint(user_input, recent_turns, has_images, image_context)
    followup_hint = classify_followup_heuristic(user_input, route_history)
    route = route_with_llm(
        user_input,
        route_history,
        recent_turns,
        client,
        metrics,
        subject_hint=subject_hint,
        subject_locked=subject_locked,
        followup_hint=followup_hint,
        followup_locked=followup_hint == "independent",
        has_images=has_images,
        image_context=image_context,
    )
    if has_images and image_context_is_new_problem(user_input, recent_turns, image_context):
        image_subject = subject_hint_from_image_context(image_context)
        if image_subject:
            route.subject = image_subject
        route.is_followup = False
        route.followup_category = "independent"
        route.parent_turn_id = None
        route.parent_turn_ids = []
        route.reason = f"{route.reason}；本轮图片 OCR 显示为新题，按独立图片题处理。".strip("；")
    parent_subject = infer_subject_from_parent_turns(recent_turns, route.parent_turn_ids, route.subject)
    if route.is_followup and parent_subject:
        if route.subject != parent_subject:
            route.reason = f"{route.reason}；追问学科继承父节点 {parent_subject}。".strip("；")
        route.subject = parent_subject
    has_parent_context = route.is_followup and bool(route.parent_turn_ids)
    if not has_parent_context and not subject_has_routing_evidence(route.subject, user_input, history, recent_turns, has_images, image_context):
        route.subject = "unsupported"
        route.clarification = build_ambiguous_clarification(user_input, history)
        route.parent_turn_id = None
        route.parent_turn_ids = []
    return route


def pop_last_clarification() -> str | None:
    global _last_clarification
    text = _last_clarification
    _last_clarification = None
    return text


def select_tools(
    subject: str,
    metrics: RuntimeMetrics | None = None,
    followup_context_resolver: Callable[[dict[str, Any]], dict[str, Any]] | None = None,
) -> dict[str, ToolSpec]:
    subject = normalize_subject(subject)
    if subject == "math":
        return build_math_tools(metrics, followup_context_resolver)
    if subject == "politics":
        return {**build_politics_tools(), **build_current_affairs_tools()}
    return {}


def has_explicit_exam_reference(text: str) -> bool:
    has_year = bool(re.search(r"(20\d{2}|0[9]|1[0-9]|2[0-9])\s*年", text))
    has_exam = bool(re.search(r"数学一|数一|math1|数学二|数二|math2|数学三|数三|math3", text, flags=re.I))
    has_question = bool(re.search(r"第\s*(?:\d{1,2}|[一二三四五六七八九十]{1,3})\s*[题問问]|(?<!\d)\d{1,2}\s*[题問问]", text))
    return has_year and has_exam and has_question


def filter_tools_for_request(tools: dict[str, ToolSpec], user_input: str, has_images: bool) -> dict[str, ToolSpec]:
    if not has_images:
        return tools
    if has_explicit_exam_reference(user_input):
        return tools
    blocked = {"solve_exam_question", "show_math_exam_question", "show_math_exam_answer"}
    return {name: spec for name, spec in tools.items() if name not in blocked}


def build_image_context_text(image_context: dict[str, Any] | None) -> str:
    if not image_context:
        return ""
    parts = [
        "本轮图片预识别结果（供路由和作答参考，不是用户原话）：",
        f"- 学科线索：{image_context.get('subject_hint') or 'unknown'}",
        f"- 置信度：{image_context.get('confidence', 0.0)}",
    ]
    reason = str(image_context.get("reason") or "").strip()
    if reason:
        parts.append(f"- 判断依据：{reason}")
    visual_summary = str(image_context.get("visual_summary") or "").strip()
    if visual_summary:
        parts.append(f"- 视觉概述：{visual_summary}")
    ocr_text = str(image_context.get("ocr_text") or "").strip()
    if ocr_text:
        parts.append(f"- OCR 文本：\n{ocr_text}")
    return "\n".join(parts)


def recognize_image_context(
    image_paths: list[Path],
    user_input: str,
    client: Any,
    metrics: RuntimeMetrics,
) -> dict[str, Any] | None:
    if not image_paths:
        return None
    started = time.perf_counter()
    usage_token = set_usage_callback(
        lambda item: metrics.add_tool_usage({
            **item,
            "tool_call_name": "image_routing_ocr",
        })
    )
    try:
        image_context = legacy_agent.recognize_images_for_routing(image_paths, user_input, client=client)
    except Exception as exc:
        metrics.add_step("image_routing_ocr", started, ok=False, error=str(exc), image_count=len(image_paths))
        return {
            "ocr_text": "",
            "visual_summary": "",
            "subject_hint": "unknown",
            "confidence": 0.0,
            "reason": f"image_routing_ocr_error:{exc}",
        }
    finally:
        reset_usage_callback(usage_token)
    metrics.add_step(
        "image_routing_ocr",
        started,
        ok=True,
        image_count=len(image_paths),
        subject_hint=image_context.get("subject_hint"),
        confidence=image_context.get("confidence"),
    )
    return image_context


def make_client() -> Any:
    return legacy_agent.make_client()


def global_model_name() -> str:
    load_dotenv(ROOT / ".env", encoding="utf-8-sig")
    return os.getenv("ROUTER_MODEL") or legacy_agent.load_settings().global_model


def global_temperature(default: float | None = None) -> float | None:
    load_dotenv(ROOT / ".env", encoding="utf-8-sig")
    value = os.getenv("ROUTER_TEMPERATURE")
    if value is None or not value.strip():
        return default
    try:
        return float(value)
    except ValueError:
        return default


def log_route_debug(
    metrics: RuntimeMetrics | None,
    *,
    user_input: str,
    model: str,
    raw_content: str,
    parsed: dict[str, Any] | None,
    parse_error: str | None = None,
) -> None:
    if not route_debug_log_enabled():
        return
    REQUEST_LOG_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "time": datetime.now().isoformat(timespec="seconds"),
        "session_id": metrics.session_id if metrics else None,
        "request_id": metrics.request_id if metrics else None,
        "user_input": user_input,
        "model": model,
        "raw_content_chars": len(raw_content),
        "raw_content": raw_content,
        "parsed": parsed,
        "parse_error": parse_error,
    }
    path = REQUEST_LOG_DIR / f"route_debug_{datetime.now().date().isoformat()}.jsonl"
    with path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(payload, ensure_ascii=False, default=str) + "\n")


def make_global_client(default_client: Any | None = None) -> Any:
    load_dotenv(ROOT / ".env", encoding="utf-8-sig")
    router_model = os.getenv("ROUTER_MODEL")
    router_api_key = os.getenv("ROUTER_API_KEY") or os.getenv("DEEPSEEK_API_KEY")
    router_base_url = os.getenv("ROUTER_BASE_URL") or os.getenv("DEEPSEEK_BASE_URL")
    if default_client is not None and not str(default_client.__class__.__module__).startswith("openai"):
        return default_client
    if not router_model or not router_api_key or not router_base_url:
        return default_client or make_client()
    from openai import OpenAI

    return OpenAI(api_key=router_api_key, base_url=router_base_url)


def normalize_message(message: Any) -> dict[str, Any]:
    data: dict[str, Any] = {"role": "assistant", "content": getattr(message, "content", None) or ""}
    tool_calls = getattr(message, "tool_calls", None)
    if tool_calls:
        data["tool_calls"] = []
        for call in tool_calls:
            function = getattr(call, "function", None)
            data["tool_calls"].append({
                "id": getattr(call, "id", ""),
                "type": "function",
                "function": {
                    "name": getattr(function, "name", ""),
                    "arguments": getattr(function, "arguments", "{}"),
                },
            })
    return data


def record_usage(
    metrics: RuntimeMetrics,
    response: Any,
    name: str | None = None,
    *,
    model: str | None = None,
    started_at: float | None = None,
) -> dict[str, Any]:
    usage = getattr(response, "usage", None)
    if not usage:
        return {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
    prompt_tokens = int(getattr(usage, "prompt_tokens", 0) or 0)
    completion_tokens = int(getattr(usage, "completion_tokens", 0) or 0)
    total_tokens = int(getattr(usage, "total_tokens", 0) or 0)
    if not total_tokens:
        total_tokens = prompt_tokens + completion_tokens
    metrics.prompt_tokens += prompt_tokens
    metrics.completion_tokens += completion_tokens
    metrics.total_tokens += total_tokens
    metrics.runtime_prompt_tokens += prompt_tokens
    metrics.runtime_completion_tokens += completion_tokens
    metrics.runtime_total_tokens += total_tokens
    item = {
        "name": name or "llm",
        "kind": "chat",
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": total_tokens,
    }
    if model:
        item["model"] = model
    if started_at is not None:
        latency_ms = round((time.perf_counter() - started_at) * 1000, 2)
        elapsed_seconds = latency_ms / 1000 if latency_ms else 0.0
        item["latency_ms"] = latency_ms
        item["tokens_per_second"] = round(total_tokens / elapsed_seconds, 2) if elapsed_seconds and total_tokens else 0.0
        item["completion_tokens_per_second"] = (
            round(completion_tokens / elapsed_seconds, 2) if elapsed_seconds and completion_tokens else 0.0
        )
    metrics.llm_usages.append(item)
    return item


def format_model_error(exc: Exception) -> str:
    text = str(exc)
    if "Arrearage" in text or "overdue-payment" in text or "Access denied" in text:
        return (
            "模型接口调用失败：DashScope 账户当前不可用，返回了 Arrearage/欠费状态。"
            "请检查阿里云百炼/DashScope 账户余额、套餐或 API Key 所属账号状态后再试。"
        )
    return f"模型接口调用失败：{exc}"


def execute_tool_call(tool_call: dict[str, Any], tools: dict[str, ToolSpec], metrics: RuntimeMetrics) -> tuple[dict[str, Any], dict[str, Any]]:
    started = time.perf_counter()
    name = tool_call.get("function", {}).get("name", "")
    raw_arguments = tool_call.get("function", {}).get("arguments", "{}")
    metrics.tool_calls += 1
    try:
        arguments = json.loads(raw_arguments or "{}")
    except json.JSONDecodeError as exc:
        metrics.tool_errors += 1
        result = {"ok": False, "error": f"Invalid JSON arguments: {exc}", "raw_arguments": raw_arguments}
        metrics.add_step(f"tool:{name}", started, ok=False, error=result["error"])
        return result, {"name": name, "arguments": raw_arguments, "ok": False, "error": result["error"]}
    spec = tools.get(name)
    if spec is None:
        metrics.tool_errors += 1
        result = {"ok": False, "error": f"Unknown tool: {name}", "available_tools": sorted(tools)}
        metrics.add_step(f"tool:{name}", started, ok=False, error=result["error"])
        return result, {"name": name, "arguments": arguments, "ok": False, "error": result["error"]}
    usage_token = set_usage_callback(
        lambda item: metrics.add_tool_usage({
            **item,
            "tool_call_name": name,
        })
    )
    try:
        value = spec.func(arguments)
        metrics.tool_success += 1
        result = {"ok": True, "result": value}
        metrics.add_step(f"tool:{name}", started, ok=True)
        return result, {"name": name, "arguments": arguments, "ok": True}
    except Exception as exc:
        metrics.tool_errors += 1
        result = {"ok": False, "error": str(exc)}
        metrics.add_step(f"tool:{name}", started, ok=False, error=str(exc))
        return result, {"name": name, "arguments": arguments, "ok": False, "error": str(exc)}
    finally:
        reset_usage_callback(usage_token)


def direct_tool_answer(
    tool_call_records: list[dict[str, Any]],
    tools: dict[str, ToolSpec],
    latest_tool_result: dict[str, Any],
    current_round_tool_count: int,
) -> tuple[str, str] | None:
    if current_round_tool_count != 1 or len(tool_call_records) != 1:
        return None
    record = tool_call_records[0]
    if not record.get("ok") or not latest_tool_result.get("ok"):
        return None
    spec = tools.get(str(record.get("name") or ""))
    if spec is None or spec.return_mode != "direct":
        return None
    value = latest_tool_result.get("result")
    if not isinstance(value, str):
        return None
    answer = value.strip()
    if not answer:
        return None
    return answer, spec.name


def log_runtime(result: RuntimeResult) -> None:
    REQUEST_LOG_DIR.mkdir(parents=True, exist_ok=True)
    path = REQUEST_LOG_DIR / f"{datetime.now().date().isoformat()}.jsonl"
    payload = {
        "time": datetime.now().isoformat(timespec="seconds"),
        "subject": result.subject,
        "metrics": result.metrics,
        "tool_calls": result.tool_calls,
        "messages": result.messages,
    }
    with path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(payload, ensure_ascii=False) + "\n")
    for item in result.tool_calls:
        if not item.get("ok"):
            case_path = REQUEST_LOG_DIR / "tool_misuse_cases.jsonl"
            with case_path.open("a", encoding="utf-8") as file:
                file.write(json.dumps(payload, ensure_ascii=False) + "\n")
            break


def split_context_paragraphs(text: str) -> list[str]:
    paragraphs = [part.strip() for part in re.split(r"\n\s*\n", str(text or "")) if part.strip()]
    if paragraphs:
        return paragraphs
    return [line.strip() for line in str(text or "").splitlines() if line.strip()]


def selected_answer_paragraphs(answer: str, keywords: set[str]) -> str:
    paragraphs = split_context_paragraphs(answer)
    if not paragraphs:
        return ""
    selected_indexes: list[int] = []
    for index in (0, len(paragraphs) - 1):
        if index not in selected_indexes:
            selected_indexes.append(index)
    lowered_keywords = {keyword.lower() for keyword in keywords if keyword}
    for index, paragraph in enumerate(paragraphs):
        lowered = paragraph.lower()
        if any(keyword in lowered for keyword in lowered_keywords) and index not in selected_indexes:
            selected_indexes.append(index)
    selected_indexes.sort()
    return "\n\n".join(paragraphs[index] for index in selected_indexes)


def select_independent_context_turns(
    user_input: str,
    recent_turns: list[dict[str, Any]],
    subject: str,
    lookback: int = INDEPENDENT_CONTEXT_LOOKBACK,
    max_turns: int = INDEPENDENT_CONTEXT_MAX_TURNS,
) -> list[dict[str, Any]]:
    normalized_subject = normalize_subject(subject, fallback="")
    if not normalized_subject or normalized_subject == "unsupported":
        return []
    current_keywords = matched_subject_keywords(user_input, normalized_subject)
    if not current_keywords:
        return []
    selected: list[dict[str, Any]] = []
    for turn in reversed(recent_turns[-lookback:]):
        if turn_subject(turn) != normalized_subject:
            continue
        turn_text = turn_context_block(turn, 2400)
        turn_keywords = matched_subject_keywords(turn_text, normalized_subject)
        overlap = current_keywords & turn_keywords
        if not overlap:
            continue
        enriched = dict(turn)
        enriched["_independent_context_keywords"] = sorted(overlap, key=len, reverse=True)
        selected.append(enriched)
        if len(selected) >= max_turns:
            break
    return list(reversed(selected))


def format_independent_context_message(
    user_input: str,
    recent_turns: list[dict[str, Any]],
    subject: str,
) -> dict[str, str] | None:
    selected_turns = select_independent_context_turns(user_input, recent_turns, subject)
    if not selected_turns:
        return None
    blocks = [
        "当前问题已判定为独立问题。下面仅提供最近 6 轮内同学科且关键词匹配的参考片段；",
        "不要把当前问题强行挂到这些历史，只在确有帮助时参考术语、口径或已讲过的结论。",
    ]
    for turn in selected_turns:
        keywords = set(str(item) for item in turn.get("_independent_context_keywords") or [])
        answer = str(turn.get("assistant_answer") or turn.get("assistant_answer_preview") or "")
        selected_answer = selected_answer_paragraphs(answer, keywords)
        blocks.append(
            "\n".join([
                f"\n[turn {turn.get('turn_id')}]",
                f"匹配关键词：{', '.join(sorted(keywords, key=len, reverse=True))}",
                f"User: {str(turn.get('user_query') or '').strip()}",
                "Assistant 参考片段:",
                selected_answer or str((turn.get("memory") or {}).get("answer_brief") or "").strip(),
            ]).strip()
        )
    return {"role": "user", "content": "\n\n".join(blocks)}


def build_messages(
    user_input: str,
    history: list[dict[str, str]],
    output_format: str,
    subject: str | None = None,
    recent_turns: list[dict[str, Any]] | None = None,
    use_independent_context: bool = False,
) -> list[dict[str, Any]]:
    format_hint = "输出适合网页 UI，保留 Markdown 和 LaTeX。" if output_format == "ui" else "输出适合 PowerShell 终端阅读，少用复杂 Markdown 表格。"
    system_prompt = MAIN_SYSTEM_PROMPT
    if context_followup_tools_enabled():
        system_prompt = f"{system_prompt}\n\n{CONTEXT_FOLLOWUP_PROMPT}"
    selected_context = (
        format_independent_context_message(user_input, recent_turns or [], subject or "")
        if use_independent_context
        else None
    )
    history_messages = [] if use_independent_context else history[-SHORT_TERM_TURNS * 2:]
    return [
        {"role": "system", "content": f"{system_prompt}\n\n{format_hint}"},
        *history_messages,
        *([selected_context] if selected_context else []),
        {"role": "user", "content": user_input},
    ]


def tool_selection_policy_for_subject(subject: str | None) -> str:
    if subject == "math":
        return MATH_TOOL_SELECTION_POLICY
    if subject == "politics":
        return POLITICS_TOOL_SELECTION_POLICY
    return GENERIC_TOOL_SELECTION_POLICY


def append_tool_selection_policy(messages: list[dict[str, Any]], subject: str | None, context_mode: str) -> list[dict[str, Any]]:
    if not messages:
        return messages
    updated = [dict(item) for item in messages]
    policy = tool_selection_policy_for_subject(subject)
    updated[0]["content"] = (
        f"{updated[0].get('content') or ''}\n\n"
        f"当前第二层上下文模式：{context_mode}。\n"
        f"{policy}"
    )
    return updated


def build_dag_tool_selection_messages(
    user_input: str,
    dag_context: dict[str, Any],
    output_format: str,
    subject: str | None,
) -> list[dict[str, Any]]:
    format_hint = "输出适合网页 UI，保留 Markdown 和 LaTeX。" if output_format == "ui" else "输出适合 PowerShell 终端阅读，少用复杂 Markdown 表格。"
    system_prompt = (
        f"{MAIN_SYSTEM_PROMPT}\n\n{CONTEXT_FOLLOWUP_PROMPT}\n\n"
        "当前轮已经由 runtime 定位到 DAG 追问链路；下面的 DAG 链路记忆替代最近 15 轮平铺历史。"
        "你是第二层 tool_selection + 可直接回答节点。"
        "先判断当前问题能否基于 DAG 链路可靠直接回答；如果不能，调用合适工具。"
        "回答或调用工具都只能沿这条链继承对象、参数、条件、阶数和上一轮结论；不要虚构链路外的历史。"
        "如果选择调用工具，必须在 tool arguments 中显式写出继承后的完整问题和必要上下文。"
        "如果链路不足以确定指代对象，请直接提出澄清问题，不要调用工具。"
        "如果选择直接回答，认真解决当前输入的核心问题，但不要主动延伸、不要主动举例、不要主动构造反例、不要展开无关背景。"
        "如果用户只问是否成立/是否一样/换成某条件如何，先给明确结论，再给必要理由；"
        "除非用户明确要求详细讲解，否则不要把回答扩展成完整专题。"
        "如果选择直接回答，应按问题复杂度控制篇幅：短确认用简短结论，概念/条件说明给必要解释，比较或推导题给关键步骤。"
        "不要为了显得完整而主动扩展成专题；除非用户要求详细展开，否则避免大段背景、长表格和无关例子。"
        "回答必须完整收尾；若内容变长，优先保留结论、关键理由和必要公式。"
    )
    content = (
        "DAG 追问链路记忆：\n"
        f"{dag_context.get('followup_context') or ''}\n\n"
        "根节点上下文：\n"
        f"{dag_context.get('root_context') or ''}\n\n"
        "当前用户输入：\n"
        f"{user_input}"
    )
    return [
        {
            "role": "system",
            "content": (
                f"{system_prompt}\n\n{format_hint}\n\n"
                f"当前第二层上下文模式：dag。\n"
                f"{tool_selection_policy_for_subject(subject)}"
            ),
        },
        {"role": "user", "content": content},
    ]


def build_tool_selection_messages(
    user_input: str,
    history: list[dict[str, str]],
    output_format: str,
    *,
    subject: str | None = None,
    recent_turns: list[dict[str, Any]] | None = None,
    followup_route_decision: dict[str, Any] | None = None,
    dag_context: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    if dag_context is not None:
        return build_dag_tool_selection_messages(user_input, dag_context, output_format, subject)
    context_mode = "plain"
    if (followup_route_decision or {}).get("category") == "independent":
        context_mode = "independent"
    messages = build_messages(
        user_input,
        history,
        output_format,
        subject=subject,
        recent_turns=recent_turns,
        use_independent_context=(followup_route_decision or {}).get("category") == "independent",
    )
    return append_tool_selection_policy(messages, subject, context_mode)


def build_dag_followup_messages(user_input: str, dag_context: dict[str, Any], output_format: str) -> list[dict[str, Any]]:
    format_hint = "输出适合网页 UI，保留 Markdown 和 LaTeX。" if output_format == "ui" else "输出适合 PowerShell 终端阅读，少用复杂 Markdown 表格。"
    system_prompt = (
        f"{MAIN_SYSTEM_PROMPT}\n\n{CONTEXT_FOLLOWUP_PROMPT}\n\n"
        "当前轮已经由 runtime 判定为非步骤追问；下面的 DAG 链路记忆替代最近 15 轮平铺历史。"
        "回答时只沿这条链继承对象、参数、条件、阶数和上一轮结论；不要虚构链路外的历史。"
        "认真解决当前输入的核心问题，但不要主动延伸、不要主动举例、不要主动构造反例、不要展开无关背景。"
        "如果用户只问是否成立/是否一样/换成某条件如何，先给明确结论，再给必要理由；"
        "除非用户明确要求详细讲解，否则不要把回答扩展成完整专题。"
        "回答时应按问题复杂度控制篇幅：短确认用简短结论，概念/条件说明给必要解释，比较或推导题给关键步骤。"
        "不要为了显得完整而主动扩展成专题；除非用户要求详细展开，否则避免大段背景、长表格和无关例子。"
        "回答必须完整收尾；若内容变长，优先保留结论、关键理由和必要公式。"
        "只有当用户明确要求“详细讲”“细说”“展开”“举例”“完整推导”等时，才允许超过默认字数，但仍要优先保证结尾完整，不要停在列表或公式中途。"
    )
    content = (
        "DAG 追问链路记忆：\n"
        f"{dag_context.get('followup_context') or ''}\n\n"
        "根节点上下文：\n"
        f"{dag_context.get('root_context') or ''}\n\n"
        "当前用户输入：\n"
        f"{user_input}"
    )
    return [
        {"role": "system", "content": f"{system_prompt}\n\n{format_hint}"},
        {"role": "user", "content": content},
    ]


def build_followup_clarification_messages(
    user_input: str,
    recent_turns: list[dict[str, Any]],
    route_decision: dict[str, Any],
    output_format: str,
) -> list[dict[str, Any]]:
    format_hint = "输出适合网页 UI，保留 Markdown 和 LaTeX。" if output_format == "ui" else "输出适合 PowerShell 终端阅读，少用复杂 Markdown 表格。"
    recent_context = "\n\n".join(
        f"[turn {turn.get('turn_id')}]\n{turn_context_block(turn, 900)}"
        for turn in recent_turns
    )
    system_prompt = (
        f"{MAIN_SYSTEM_PROMPT}\n\n{CONTEXT_FOLLOWUP_PROMPT}\n\n"
        "当前轮被判定为非步骤追问但 parent 不明确。不要直接解题；"
        f"请基于最近 {FOLLOWUP_DAG_LOOKBACK} 轮候选，向用户提出一个简短澄清问题，让用户确认要追问哪一轮或哪个对象。"
    )
    content = (
        f"判定结果：{json.dumps(route_decision, ensure_ascii=False)}\n\n"
        f"最近 {FOLLOWUP_DAG_LOOKBACK} 轮候选：\n{recent_context}\n\n"
        f"当前用户输入：\n{user_input}"
    )
    return [
        {"role": "system", "content": f"{system_prompt}\n\n{format_hint}"},
        {"role": "user", "content": content},
    ]


def run_tool_selection_loop(
    *,
    user_input: str,
    session_id: str,
    subject: str,
    messages: list[dict[str, Any]],
    tools: dict[str, ToolSpec],
    client: Any,
    metrics: RuntimeMetrics,
    persist: bool,
    extra_memory: dict[str, Any] | None = None,
    max_tokens: int | None = None,
) -> RuntimeResult:
    openai_tools = [tool.openai_schema() for tool in tools.values()]
    tool_call_records: list[dict[str, Any]] = []

    for round_index in range(MAX_TOOL_ROUNDS):
        llm_started = time.perf_counter()
        try:
            global_client = make_global_client(client)
            model_name = global_model_name()
            payload: dict[str, Any] = {
                "model": model_name,
                "messages": messages,
                "tools": openai_tools,
                "tool_choice": "auto",
                "temperature": global_temperature(legacy_agent.load_settings().temperature),
            }
            if max_tokens is not None:
                payload["max_tokens"] = max_tokens
            response = global_client.chat.completions.create(**payload)
        except Exception as exc:
            metrics.add_step("llm_tool_selection", llm_started, round=round_index + 1, ok=False, error=str(exc))
            result = RuntimeResult(format_model_error(exc), subject, messages, tool_call_records, metrics.as_dict(), extra_memory=extra_memory)
            log_runtime(result)
            if persist:
                append_runtime_turn(session_id, user_input, result)
            return result
        metrics.llm_calls += 1
        message = response.choices[0].message
        assistant_message = normalize_message(message)
        messages.append(assistant_message)
        tool_calls = assistant_message.get("tool_calls") or []
        record_usage(
            metrics,
            response,
            "llm_tool_selection" if tool_calls else "llm_final",
            model=model_name,
            started_at=llm_started,
        )
        metrics.add_step("llm_tool_selection" if tool_calls else "llm_final", llm_started, round=round_index + 1, tool_calls=len(tool_calls))
        if not tool_calls:
            answer = str(assistant_message.get("content") or "").strip()
            result = RuntimeResult(answer, subject, messages, tool_call_records, metrics.as_dict(), extra_memory=extra_memory)
            log_runtime(result)
            if persist:
                append_runtime_turn(session_id, user_input, result)
            return result
        latest_tool_result: dict[str, Any] | None = None
        for tool_call in tool_calls:
            tool_result, record = execute_tool_call(tool_call, tools, metrics)
            latest_tool_result = tool_result
            tool_call_records.append(record)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call["id"],
                "name": tool_call["function"]["name"],
                "content": json.dumps(tool_result, ensure_ascii=False, default=str),
            })
        direct = direct_tool_answer(tool_call_records, tools, latest_tool_result or {}, len(tool_calls))
        if direct is not None:
            answer, tool_name = direct
            direct_started = time.perf_counter()
            metrics.add_step("direct_tool_return", direct_started, tool=tool_name)
            result = RuntimeResult(answer, subject, messages, tool_call_records, metrics.as_dict(), extra_memory=extra_memory)
            log_runtime(result)
            if persist:
                append_runtime_turn(session_id, user_input, result)
            return result

    answer = "工具调用轮次过多，我先停止本轮处理。请把问题拆小一点，或明确要解释哪一步。"
    result = RuntimeResult(answer, subject, messages, tool_call_records, metrics.as_dict(), extra_memory=extra_memory)
    log_runtime(result)
    if persist:
        append_runtime_turn(session_id, user_input, result)
    return result


def run_standard_message_loop(
    user_input: str,
    session_id: str = "default",
    image_paths: list[Path] | None = None,
    output_format: str = "ui",
    client: Any | None = None,
    persist: bool = True,
    progress_callback: Callable[[dict[str, Any]], None] | None = None,
) -> RuntimeResult:
    load_dotenv(ROOT / ".env")
    image_paths = image_paths or []
    request_id = now_id()
    metrics = RuntimeMetrics(
        request_id=request_id,
        session_id=safe_session_id(session_id),
        progress_callback=progress_callback,
    )
    client = client or make_client()

    history = read_recent_md_messages(session_id)
    recent_turns = legacy_agent.load_session(session_id).get("turns", [])[-FOLLOWUP_DAG_LOOKBACK:]
    image_context = recognize_image_context(image_paths, user_input, client, metrics) if image_paths else None
    followup_route_decision: dict[str, Any] | None = None
    route_decision: RouteDecision | None = None
    step_started = time.perf_counter()
    try:
        if should_use_unified_route(bool(image_paths), recent_turns):
            route_decision = build_route_decision(
                user_input,
                history,
                recent_turns,
                bool(image_paths),
                client,
                metrics,
                image_context=image_context,
            )
            subject = route_decision.subject
            followup_route_decision = route_decision.followup_route()
        else:
            subject = classify_subject(
                user_input,
                history,
                has_images=bool(image_paths),
                client=client,
                metrics=metrics,
                image_context=image_context,
            )
    except Exception as exc:
        metrics.add_step("route_classifier", step_started, subject="error", error=str(exc))
        result = RuntimeResult(
            format_model_error(exc),
            "unsupported",
            build_messages(user_input, history, output_format),
            [],
            metrics.as_dict(),
        )
        log_runtime(result)
        if persist:
            append_runtime_turn(session_id, user_input, result)
        return result
    metrics.subject = subject
    metrics.add_step(
        "route_classifier" if route_decision is not None else "subject_classifier",
        step_started,
        subject=subject,
        category=(followup_route_decision or {}).get("category"),
        parent_turn_id=(followup_route_decision or {}).get("parent_turn_id"),
        parent_turn_ids=(followup_route_decision or {}).get("parent_turn_ids") or [],
    )

    def followup_context_resolver(args: dict[str, Any]) -> dict[str, Any]:
        return format_followup_dag_context(
            session_id=session_id,
            user_input=str(args.get("user_query") or user_input),
            output_format=str(args.get("output_format") or output_format),
            client=client,
            route_decision=followup_route_decision,
            metrics=metrics,
        )

    tools = filter_tools_for_request(
        select_tools(subject, metrics, followup_context_resolver),
        user_input,
        bool(image_paths),
    )
    if not tools:
        clarification = (route_decision.clarification if route_decision else None) or pop_last_clarification()
        if not clarification:
            if subject == "politics":
                clarification = "当前主要支持数学问答和时政查询，政治知识点功能正在开发中。您可以试试数学题（如「2021 年数一第 9 题怎么做」），或者查询近期的时政热点。"
            elif subject == "english":
                clarification = "当前主要支持数学问答和时政查询，英语相关功能正在开发中。您有数学题需要解答吗？"
            else:
                clarification = build_ambiguous_clarification(user_input, history)
        answer = clarification
        result = RuntimeResult(answer, subject, build_messages(user_input, history, output_format), [], metrics.as_dict())
        log_runtime(result)
        if persist:
            append_runtime_turn(session_id, user_input, result)
        return result

    if image_paths:
        image_context_text = build_image_context_text(image_context)
        image_parts = [user_input]
        if image_context_text:
            image_parts.append(image_context_text)
        image_parts.append(f"本轮上传图片路径：{json.dumps([str(path) for path in image_paths], ensure_ascii=False)}")
        user_input = "\n\n".join(part for part in image_parts if part)

    if (
        context_followup_tools_enabled()
        and not image_paths
        and subject in {"math", "politics"}
        and followup_route_decision is None
    ):
        followup_hint = classify_followup_heuristic(user_input, history)
        if followup_hint == "independent":
            followup_route_decision = {
                "category": "independent",
                "parent_turn_id": None,
                "parent_turn_ids": [],
                "reason": "heuristic_independent",
            }
        else:
            route_started = time.perf_counter()
            followup_route_decision = classify_followup_route_with_llm(user_input, recent_turns, client, metrics, subject_hint=subject)
            metrics.add_step(
                "followup_route_classifier",
                route_started,
                category=followup_route_decision.get("category"),
                parent_turn_id=followup_route_decision.get("parent_turn_id"),
                parent_turn_ids=followup_route_decision.get("parent_turn_ids") or [],
            )

    dag_context_for_tool_selection: dict[str, Any] | None = None

    if (
        context_followup_tools_enabled()
        and not image_paths
        and followup_route_decision is not None
        and followup_route_decision.get("category") in {"weak_nonstep_followup", "contextual_nonstep_followup"}
        and route_parent_ids(followup_route_decision)
    ):
        dag_context = followup_context_resolver({
            "user_query": user_input,
            "output_format": output_format,
        })
        if dag_tool_selection_enabled():
            dag_context_for_tool_selection = dag_context
        else:
            messages = build_dag_followup_messages(user_input, dag_context, output_format)
            llm_started = time.perf_counter()
            try:
                global_client = make_global_client(client)
                model_name = global_model_name()
                response = global_client.chat.completions.create(
                    model=model_name,
                    messages=messages,
                    temperature=global_temperature(legacy_agent.load_settings().temperature),
                    max_tokens=DAG_FOLLOWUP_MAX_TOKENS,
                )
                metrics.llm_calls += 1
                record_usage(metrics, response, "llm_dag_followup_final", model=model_name, started_at=llm_started)
                answer = str(response.choices[0].message.content or "").strip()
                metrics.add_step(
                    "llm_dag_followup_final",
                    llm_started,
                    category=followup_route_decision.get("category"),
                    parent_turn_id=followup_route_decision.get("parent_turn_id"),
                    parent_turn_ids=followup_route_decision.get("parent_turn_ids") or [],
                )
                result = RuntimeResult(
                    answer,
                    subject,
                    messages,
                    [],
                    metrics.as_dict(),
                    extra_memory={"followup_dag": dag_context.get("followup_dag")},
                )
            except Exception as exc:
                metrics.add_step("llm_dag_followup_final", llm_started, ok=False, error=str(exc))
                result = RuntimeResult(format_model_error(exc), subject, messages, [], metrics.as_dict())
            log_runtime(result)
            if persist:
                append_runtime_turn(session_id, user_input, result)
            return result

    if (
        context_followup_tools_enabled()
        and not image_paths
        and followup_route_decision is not None
        and followup_route_decision.get("category") in {"contextual_nonstep_followup", "ambiguous"}
        and not route_parent_ids(followup_route_decision)
    ):
        recent_turns = legacy_agent.load_session(session_id).get("turns", [])[-FOLLOWUP_DAG_LOOKBACK:]
        messages = build_followup_clarification_messages(user_input, recent_turns, followup_route_decision, output_format)
        llm_started = time.perf_counter()
        try:
            global_client = make_global_client(client)
            model_name = global_model_name()
            response = global_client.chat.completions.create(
                model=model_name,
                messages=messages,
                temperature=global_temperature(legacy_agent.load_settings().temperature),
            )
            metrics.llm_calls += 1
            record_usage(metrics, response, "llm_followup_clarification", model=model_name, started_at=llm_started)
            answer = str(response.choices[0].message.content or "").strip()
            metrics.add_step(
                "llm_followup_clarification",
                llm_started,
                category=followup_route_decision.get("category"),
            )
            result = RuntimeResult(answer, subject, messages, [], metrics.as_dict())
        except Exception as exc:
            metrics.add_step("llm_followup_clarification", llm_started, ok=False, error=str(exc))
            result = RuntimeResult(format_model_error(exc), subject, messages, [], metrics.as_dict())
        log_runtime(result)
        if persist:
            append_runtime_turn(session_id, user_input, result)
        return result

    messages = build_tool_selection_messages(
        user_input,
        history,
        output_format,
        subject=subject,
        recent_turns=recent_turns,
        followup_route_decision=followup_route_decision,
        dag_context=dag_context_for_tool_selection,
    )
    return run_tool_selection_loop(
        user_input=user_input,
        session_id=session_id,
        subject=subject,
        messages=messages,
        tools=tools,
        client=client,
        metrics=metrics,
        persist=persist,
        extra_memory=(
            {"followup_dag": dag_context_for_tool_selection.get("followup_dag")}
            if dag_context_for_tool_selection is not None
            else None
        ),
    )


def iter_text_chunks(text: str, chunk_size: int = 24) -> Iterable[str]:
    for index in range(0, len(text), chunk_size):
        yield text[index:index + chunk_size]


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the standard tool-calling kaoyan assistant.")
    parser.add_argument("query", nargs="+", help="用户问题")
    parser.add_argument("--session", default="default", help="会话 ID")
    parser.add_argument("--image", "-i", action="append", default=[], help="本地图片路径，可传多次")
    parser.add_argument("--format", choices=["ui", "terminal"], default="terminal")
    parser.add_argument("--no-memory", action="store_true", help="不写入短期会话")
    parser.add_argument("--debug", action="store_true", help="输出 runtime metrics")
    return parser


def configure_cli_output_encoding() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if not callable(reconfigure):
            continue
        try:
            reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def main() -> None:
    configure_cli_output_encoding()
    parser = build_arg_parser()
    args = parser.parse_args()
    result = run_standard_message_loop(
        " ".join(args.query),
        session_id=args.session,
        image_paths=[Path(item) for item in args.image],
        output_format=args.format,
        persist=not args.no_memory,
    )
    print(result.answer)
    if args.debug:
        print("\n[metrics]")
        print(json.dumps(result.metrics, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
