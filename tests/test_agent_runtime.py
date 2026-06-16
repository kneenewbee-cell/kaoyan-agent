from __future__ import annotations

import json
import os
import shutil
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from typing import Any
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import agent_runtime
import kaoyan_agent


TEST_SESSION_PREFIXES = ("unit", "real_api_smoke")


def is_test_session_id(session_id: str) -> bool:
    return session_id.startswith(TEST_SESSION_PREFIXES)


def cleanup_test_sessions() -> None:
    for directory, suffix in (
        (kaoyan_agent.SESSION_DIR, ".json"),
        (agent_runtime.SESSION_MD_DIR, ".md"),
    ):
        if not directory.exists():
            continue
        for path in directory.iterdir():
            if path.is_file() and path.suffix == suffix and is_test_session_id(path.stem):
                path.unlink()

    vector_dir = kaoyan_agent.SESSION_VECTOR_DIR
    if not vector_dir.exists():
        return
    for path in vector_dir.iterdir():
        if not is_test_session_id(path.name):
            continue
        if path.is_dir():
            shutil.rmtree(path)
        elif path.is_file():
            path.unlink()


def fake_response(content: str = "", tool_calls: list[dict] | None = None) -> SimpleNamespace:
    calls = []
    for item in tool_calls or []:
        calls.append(
            SimpleNamespace(
                id=item.get("id", "call_1"),
                function=SimpleNamespace(
                    name=item["name"],
                    arguments=json.dumps(item.get("arguments", {}), ensure_ascii=False),
                ),
            )
        )
    message = SimpleNamespace(content=content, tool_calls=calls)
    usage = SimpleNamespace(prompt_tokens=10, completion_tokens=5, total_tokens=15)
    return SimpleNamespace(choices=[SimpleNamespace(message=message)], usage=usage)


class FakeCompletions:
    def __init__(self, responses: list[SimpleNamespace]) -> None:
        self.responses = responses
        self.calls: list[dict] = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        if not self.responses:
            raise AssertionError("No fake response left")
        return self.responses.pop(0)


class FakeClient:
    def __init__(self, responses: list[SimpleNamespace]) -> None:
        self.chat = SimpleNamespace(completions=FakeCompletions(responses))


class AgentRuntimeTest(unittest.TestCase):
    def setUp(self) -> None:
        cleanup_test_sessions()
        self.addCleanup(cleanup_test_sessions)

    def test_subject_classifier_heuristic_math_followup(self) -> None:
        self.assertIsNone(agent_runtime.classify_subject_heuristic("这一步怎么来的？"))
        history = [{"role": "assistant", "content": "考研数学解法：先求极限，再估计余项。"}]
        self.assertEqual(agent_runtime.classify_subject_heuristic("这一步怎么来的？", history=history), "math")
        self.assertEqual(agent_runtime.classify_subject_heuristic("2021 年数一第 9 题怎么做"), "math")
        self.assertEqual(agent_runtime.classify_subject_heuristic("09年数一第二题怎么做"), "math")
        self.assertIsNone(agent_runtime.classify_subject_heuristic("这张图怎么看？", has_images=True))

    def test_current_affairs_is_politics_subject_with_current_affairs_tool(self) -> None:
        self.assertEqual(agent_runtime.classify_subject_heuristic("二十届三中全会的新质生产力是什么？"), "politics")
        tools = agent_runtime.select_tools("politics")
        self.assertIn("search_politics_knowledge", tools)
        self.assertIn("get_current_affairs", tools)
        self.assertEqual(agent_runtime.normalize_subject("current_affairs"), "politics")

    def test_subject_classifier_heuristic_math_linear_algebra_probability(self) -> None:
        examples = [
            "向量组线性相关怎么判断？",
            "这个矩阵可以对角化吗？",
            "齐次线性方程组的基础解系怎么求？",
            "随机变量的分布函数怎么写？",
            "条件概率和全概率公式怎么区分？",
            "正态分布的数学期望和方差是多少？",
            "斯托克斯公式",
            "格林公式",
            "高斯公式",
            "曲面积分怎么计算？",
            "牛顿-莱布尼茨公式",
            "隐函数求导怎么做？",
            "比值判别法和根值判别法怎么选？",
            "施密特正交化步骤",
            "最大似然估计量怎么求？",
            "置信区间和假设检验",
        ]
        for text in examples:
            with self.subTest(text=text):
                self.assertEqual(agent_runtime.classify_subject_heuristic(text), "math")

    def test_subject_classifier_heuristic_ignores_weak_math_words_alone(self) -> None:
        examples = [
            "这个函数是什么？",
            "连续推进改革",
            "总体要求是什么",
            "相关政策有哪些",
            "独立自主是什么意思",
            "这个条件有什么关系",
        ]
        for text in examples:
            with self.subTest(text=text):
                self.assertIsNone(agent_runtime.classify_subject_heuristic(text))

    def test_subject_classifier_requires_evidence_for_ambiguous_input(self) -> None:
        client = FakeClient([fake_response(content='{"subject":"english","reason":"用户问题本身模糊，需要按历史判断"}')])
        subject = agent_runtime.classify_subject("这道题怎么做？", [], client=client)
        self.assertEqual(subject, "unsupported")
        self.assertIsNotNone(agent_runtime.pop_last_clarification())
        self.assertEqual(len(client.chat.completions.calls), 1)

    def test_route_payload_includes_image_context_only_for_image_input(self) -> None:
        image_context = {
            "ocr_text": "设函数 f(x)=x^2，求导数。",
            "visual_summary": "图片是一道含函数公式的题目。",
            "subject_hint": "math",
            "confidence": 0.9,
            "reason": "包含函数和求导要求",
        }
        client = FakeClient([fake_response(content='{"subject":"math","is_followup":false,"followup_category":"independent","parent_turn_id":null,"parent_turn_ids":[],"reason":"OCR显示为数学题","clarification":null}')])
        route = agent_runtime.route_with_llm("怎么做？", [], [], client, has_images=True, image_context=image_context)
        payload = json.loads(client.chat.completions.calls[0]["messages"][1]["content"])
        self.assertEqual(route.subject, "math")
        self.assertEqual(payload["image_context"]["ocr_text"], image_context["ocr_text"])

        plain_client = FakeClient([fake_response(content='{"subject":"unsupported","is_followup":false,"followup_category":"independent","parent_turn_id":null,"parent_turn_ids":[],"reason":"无图片","clarification":null}')])
        agent_runtime.route_with_llm("怎么做？", [], [], plain_client, has_images=False)
        plain_payload = json.loads(plain_client.chat.completions.calls[0]["messages"][1]["content"])
        self.assertNotIn("image_context", plain_payload)

    def test_route_uses_router_model_when_configured(self) -> None:
        client = FakeClient([fake_response(content='{"subject":"math","is_followup":false,"followup_category":"independent","parent_turn_id":null,"parent_turn_ids":[],"reason":"router model","clarification":null}')])
        with patch.dict(os.environ, {"ROUTER_MODEL": "deepseek-v4-flash", "ROUTER_TEMPERATURE": "0"}, clear=False):
            route = agent_runtime.route_with_llm("格林公式", [], [], client)
        self.assertEqual(route.subject, "math")
        self.assertEqual(client.chat.completions.calls[0]["model"], "deepseek-v4-flash")
        self.assertEqual(client.chat.completions.calls[0]["temperature"], 0.0)

    def test_image_context_counts_as_subject_routing_evidence(self) -> None:
        image_context = {
            "ocr_text": "计算极限 lim x->0 sin x / x",
            "visual_summary": "图片包含数学公式。",
            "subject_hint": "math",
            "confidence": 0.88,
            "reason": "包含极限公式",
        }
        self.assertTrue(
            agent_runtime.subject_has_routing_evidence(
                "math",
                "怎么做？",
                [],
                [],
                has_images=True,
                image_context=image_context,
            )
        )

    def test_image_subject_hint_overrides_recent_history_for_route(self) -> None:
        image_context = {
            "ocr_text": "帮我用数学归纳法证明：1² + 2² + ... + n² = n(n+1)(2n+1)/6。",
            "visual_summary": "图片包含数学归纳法证明题。",
            "subject_hint": "math",
            "confidence": 0.95,
            "reason": "包含数学公式和归纳法证明要求",
        }
        recent_turns = [
            {"turn_id": 1, "user_query": "量变和质变的辩证关系是什么？", "assistant_answer": "这是政治马原内容。", "route": {"subject": "politics"}},
        ]
        subject_hint, subject_locked = agent_runtime.route_subject_hint("这道题怎么做？", recent_turns, True, image_context)
        self.assertEqual(subject_hint, "math")
        self.assertTrue(subject_locked)

        client = FakeClient([fake_response(content='{"subject":"politics","is_followup":false,"followup_category":"independent","parent_turn_id":null,"parent_turn_ids":[],"reason":"tries to inherit history","clarification":null}')])
        route = agent_runtime.build_route_decision("这道题怎么做？", [], recent_turns, True, client, agent_runtime.RuntimeMetrics("r", "s"), image_context)
        payload = json.loads(client.chat.completions.calls[0]["messages"][1]["content"])
        self.assertEqual(route.subject, "math")
        self.assertEqual(payload["subject_hint"], "math")
        self.assertTrue(payload["subject_locked"])

    def test_current_explicit_subject_overrides_previous_topic_for_route(self) -> None:
        recent_turns = [
            {"turn_id": 15, "user_query": "数学归纳法证明平方和公式", "assistant_answer": "已完成数学证明。", "route": {"subject": "math"}},
            {"turn_id": 16, "user_query": "量变和质变的辩证关系是什么？", "assistant_answer": "政治题回答。", "route": {"subject": "politics"}},
        ]
        subject_hint, subject_locked = agent_runtime.route_subject_hint(
            "回到刚才的数学证明，在归纳假设步，n=1 验证过吗？",
            recent_turns,
        )
        self.assertEqual(subject_hint, "math")
        self.assertTrue(subject_locked)

    def test_followup_subject_inherits_single_parent_subject(self) -> None:
        recent_turns = [
            {
                "turn_id": 9,
                "user_query": "中央经济工作会议提出的“稳中求进”工作总基调是什么？",
                "assistant_answer": "这是时政中的工作总基调。",
                "route": {"subject": "current_affairs"},
            },
        ]
        client = FakeClient([fake_response(content='{"subject":"politics","is_followup":true,"followup_category":"weak_nonstep_followup","parent_turn_id":9,"parent_turn_ids":[9],"reason":"当前句有辩证关系","clarification":null}')])
        route = agent_runtime.build_route_decision(
            "那“稳”和“进”的辩证关系是什么？",
            [],
            recent_turns,
            False,
            client,
            agent_runtime.RuntimeMetrics("r", "s"),
        )
        self.assertEqual(route.subject, "politics")
        self.assertEqual(route.parent_turn_ids, [9])

    def test_followup_subject_keeps_current_subject_for_mixed_parents(self) -> None:
        recent_turns = [
            {
                "turn_id": 8,
                "user_query": "两点论和重点论有什么联系？",
                "assistant_answer": "政治马原内容。",
                "route": {"subject": "politics"},
            },
            {
                "turn_id": 10,
                "user_query": "稳中求进的工作总基调是什么？",
                "assistant_answer": "时政内容。",
                "route": {"subject": "current_affairs"},
            },
        ]
        client = FakeClient([fake_response(content='{"subject":"politics","is_followup":true,"followup_category":"contextual_nonstep_followup","parent_turn_id":10,"parent_turn_ids":[8,10],"reason":"混合父节点比较","clarification":null}')])
        route = agent_runtime.build_route_decision(
            "比较一下两点论和稳中求进，它们是否相通？",
            [],
            recent_turns,
            False,
            client,
            agent_runtime.RuntimeMetrics("r", "s"),
        )
        self.assertEqual(route.subject, "politics")
        self.assertEqual(route.parent_turn_ids, [8, 10])

    def test_ambiguous_route_clears_parent_ids(self) -> None:
        recent_turns = [
            {
                "turn_id": 16,
                "user_query": "比较一下两个政治概念。",
                "assistant_answer": "这是一个比较题。",
                "route": {"subject": "politics"},
            },
        ]
        client = FakeClient([fake_response(content='{"subject":"politics","is_followup":true,"followup_category":"ambiguous","parent_turn_id":16,"parent_turn_ids":[16],"reason":"比较对象缺失","clarification":"你指哪一个比较题？"}')])
        route = agent_runtime.route_with_llm(
            "那这个和之前那个哪个更难？",
            [],
            recent_turns,
            client,
        )
        self.assertEqual(route.followup_category, "ambiguous")
        self.assertIsNone(route.parent_turn_id)
        self.assertEqual(route.parent_turn_ids, [])

    def test_contextual_anchor_inputs_are_not_locked_independent(self) -> None:
        history = [{"role": "assistant", "content": "上一题是矩阵特征值计算。"}]
        self.assertEqual(
            agent_runtime.classify_followup_heuristic("不好意思，我写错了矩阵，请重新计算", history),
            "contextual_nonstep_followup",
        )
        self.assertEqual(
            agent_runtime.classify_followup_heuristic("能不能使用洛必达解决这道题呢", history),
            "contextual_nonstep_followup",
        )
        composite_examples = [
            "讲一下积分中值定理，刚才那道题能用吗",
            "这个方法是什么，上一题能不能用它证明",
            "这个政策工具是什么，上一题可以用它分析吗",
        ]
        for text in composite_examples:
            with self.subTest(text=text):
                self.assertTrue(agent_runtime.is_composite_followup_input(text, has_history=True))
                self.assertEqual(
                    agent_runtime.classify_followup_heuristic(text, history),
                    "contextual_nonstep_followup",
                )

    def test_image_new_problem_clears_parent_from_route(self) -> None:
        image_context = {
            "ocr_text": "帮我用数学归纳法证明：1² + 2² + ... + n² = n(n+1)(2n+1)/6。",
            "visual_summary": "图片包含数学归纳法证明题。",
            "subject_hint": "math",
            "confidence": 0.95,
            "reason": "包含数学公式和归纳法证明要求",
        }
        recent_turns = [
            {"turn_id": 16, "user_query": "量变和质变的辩证关系是什么？", "assistant_answer": "政治题回答。", "route": {"subject": "politics"}},
        ]
        client = FakeClient([fake_response(content='{"subject":"math","is_followup":true,"followup_category":"weak_nonstep_followup","parent_turn_id":16,"parent_turn_ids":[16],"reason":"tries to attach latest","clarification":null}')])
        route = agent_runtime.build_route_decision("这道题怎么做？", [], recent_turns, True, client, agent_runtime.RuntimeMetrics("r", "s"), image_context)
        self.assertEqual(route.subject, "math")
        self.assertEqual(route.followup_category, "independent")
        self.assertIsNone(route.parent_turn_id)
        self.assertEqual(route.parent_turn_ids, [])

    def test_route_classifier_prompt_documents_parent_priority_rules(self) -> None:
        prompt = agent_runtime.ROUTE_CLASSIFIER_PROMPT
        self.assertIn("父节点判定优先级", prompt)
        self.assertIn("纯粹新话题", prompt)
        self.assertIn("复合输入追问优先", prompt)
        self.assertIn("解释某概念/方法", prompt)
        self.assertIn("能否使用或如何应用", prompt)
        self.assertIn("完整新题目", prompt)
        self.assertIn("回到刚才", prompt)
        self.assertIn("纠错或改条件", prompt)
        self.assertIn("本轮有 image_context 显示一张新题", prompt)

    def test_dag_followup_prompt_uses_soft_answer_budget(self) -> None:
        messages = agent_runtime.build_dag_followup_messages(
            "那这个条件下还成立吗？",
            {
                "followup_context": "[turn 1]\nUser: 原题\nAssistant: 原回答",
                "root_context": "[root turn 1]\nUser: 原题\nAssistant: 原回答",
            },
            "ui",
        )
        system_prompt = messages[0]["content"]
        self.assertIn(f"{agent_runtime.DAG_FOLLOWUP_TARGET_CHARS} 个汉字以内", system_prompt)
        self.assertIn("必须完整收尾", system_prompt)
        self.assertIn("优先删减例子、背景、表格和延伸内容", system_prompt)
        self.assertGreater(agent_runtime.DAG_FOLLOWUP_MAX_TOKENS, agent_runtime.DAG_FOLLOWUP_TARGET_CHARS)

    def test_image_context_flows_into_runtime_messages(self) -> None:
        image_context = {
            "ocr_text": "设函数 f(x)=x^2，求 f'(x)。",
            "visual_summary": "图片是一道求导题。",
            "subject_hint": "math",
            "confidence": 0.92,
            "reason": "包含函数和导数符号",
        }
        client = FakeClient([
            fake_response(content='{"subject":"math","is_followup":false,"followup_category":"independent","parent_turn_id":null,"parent_turn_ids":[],"reason":"OCR显示为数学题","clarification":null}'),
            fake_response(tool_calls=[{"name": "direct_math_tool", "arguments": {"x": 1}}]),
        ])
        direct_tool = agent_runtime.ToolSpec(
            name="direct_math_tool",
            description="direct",
            parameters=agent_runtime.json_schema({"x": {"type": "integer"}}, ["x"]),
            func=lambda args: "direct answer",
            return_mode="direct",
        )
        with patch("agent_runtime.legacy_agent.recognize_images_for_routing", return_value=image_context), patch(
            "agent_runtime.select_tools",
            return_value={"direct_math_tool": direct_tool},
        ):
            result = agent_runtime.run_standard_message_loop(
                "怎么做？",
                session_id="unit_image_context_flow",
                image_paths=[Path("missing.png")],
                client=client,
                persist=False,
            )

        route_payload = json.loads(client.chat.completions.calls[0]["messages"][1]["content"])
        tool_loop_user_text = "\n".join(
            str(message.get("content") or "")
            for message in client.chat.completions.calls[1]["messages"]
            if message.get("role") == "user"
        )
        self.assertEqual(route_payload["image_context"]["ocr_text"], image_context["ocr_text"])
        self.assertIn("本轮图片预识别结果", tool_loop_user_text)
        self.assertIn(image_context["ocr_text"], tool_loop_user_text)
        self.assertEqual(result.answer, "direct answer")

    def test_image_only_input_uses_image_context_for_routing(self) -> None:
        image_context = {
            "ocr_text": "计算不定积分 \\int x dx。",
            "visual_summary": "图片只有一道积分题，没有额外用户文字。",
            "subject_hint": "math",
            "confidence": 0.93,
            "reason": "包含积分公式",
        }
        client = FakeClient([
            fake_response(content='{"subject":"math","is_followup":false,"followup_category":"independent","parent_turn_id":null,"parent_turn_ids":[],"reason":"图片OCR显示为数学积分题","clarification":null}'),
            fake_response(tool_calls=[{"name": "direct_math_tool", "arguments": {"x": 1}}]),
        ])
        direct_tool = agent_runtime.ToolSpec(
            name="direct_math_tool",
            description="direct",
            parameters=agent_runtime.json_schema({"x": {"type": "integer"}}, ["x"]),
            func=lambda args: "direct answer",
            return_mode="direct",
        )
        with patch("agent_runtime.legacy_agent.recognize_images_for_routing", return_value=image_context), patch(
            "agent_runtime.select_tools",
            return_value={"direct_math_tool": direct_tool},
        ):
            result = agent_runtime.run_standard_message_loop(
                "",
                session_id="unit_image_only_context_flow",
                image_paths=[Path("missing.png")],
                client=client,
                persist=False,
            )

        route_payload = json.loads(client.chat.completions.calls[0]["messages"][1]["content"])
        self.assertEqual(route_payload["user_input"], "")
        self.assertEqual(route_payload["image_context"]["ocr_text"], image_context["ocr_text"])
        self.assertEqual(result.subject, "math")
        self.assertEqual(result.answer, "direct answer")

    def test_math_tool_registry_has_composite_skill_and_precise_boundary(self) -> None:
        tools = agent_runtime.build_math_tools()
        self.assertIn("solve_exam_question", tools)
        self.assertEqual(tools["solve_exam_question"].return_mode, "direct")
        self.assertEqual(tools["solve_general_math"].return_mode, "direct")
        self.assertEqual(tools["explain_math_step"].return_mode, "direct")
        self.assertEqual(tools["ocr_math_image"].return_mode, "evidence")
        self.assertIn("组合 skill", tools["solve_exam_question"].description)
        self.assertIn("局部追问用 explain_math_step", tools["solve_exam_question"].description)
        self.assertIn("previous_context", tools["explain_math_step"].parameters["properties"])

    def test_context_followup_tools_are_env_gated(self) -> None:
        with patch.dict(os.environ, {"ENABLE_CONTEXT_FOLLOWUP_TOOLS": "0"}):
            tools = agent_runtime.build_math_tools()
            messages = agent_runtime.build_messages("总结一下", [], "ui")
        self.assertNotIn("answer_math_followup", tools)
        self.assertNotIn("非步骤追问规则", messages[0]["content"])

        with patch.dict(os.environ, {"ENABLE_CONTEXT_FOLLOWUP_TOOLS": "1"}):
            tools = agent_runtime.build_math_tools()
            messages = agent_runtime.build_messages("总结一下", [], "ui")
        self.assertIn("answer_math_followup", tools)
        self.assertIn("rewrite_math_answer", tools)
        self.assertIn("summarize_math_solution", tools)
        self.assertIn("非步骤追问规则", messages[0]["content"])

    def test_independent_context_uses_recent_same_subject_keyword_paragraphs(self) -> None:
        recent_turns = [
            {
                "turn_id": 1,
                "user_query": "等价无穷小定义",
                "assistant_answer": "turn1 old matching answer",
                "route": {"subject": "math"},
            },
            {
                "turn_id": 2,
                "user_query": "等价无穷小替换条件",
                "assistant_answer": "turn2 开头\n\n等价无穷小只能在乘除中替换。\n\nturn2 结尾",
                "route": {"subject": "math"},
            },
            {
                "turn_id": 3,
                "user_query": "新质生产力是什么",
                "assistant_answer": "政治里也可能出现等价无穷小这个字样，但学科不一致。",
                "route": {"subject": "politics"},
            },
            {
                "turn_id": 4,
                "user_query": "等价无穷小例题",
                "assistant_answer": (
                    "turn4 开头\n\n"
                    "等价无穷小第一处命中。\n\n"
                    "无关段落不应进入。\n\n"
                    "等价无穷小第二处命中。\n\n"
                    "turn4 结尾"
                ),
                "route": {"subject": "math"},
            },
        ]

        message = agent_runtime.format_independent_context_message("等价无穷小怎么用？", recent_turns, "math")

        self.assertIsNotNone(message)
        content = message["content"] if message else ""
        self.assertIn("turn 2", content)
        self.assertIn("turn 4", content)
        self.assertNotIn("turn 1", content)
        self.assertNotIn("turn 3", content)
        self.assertLess(content.index("turn 2"), content.index("turn 4"))
        self.assertIn("等价无穷小第一处命中", content)
        self.assertIn("等价无穷小第二处命中", content)
        self.assertIn("turn4 开头", content)
        self.assertIn("turn4 结尾", content)
        self.assertNotIn("无关段落不应进入", content)

    def test_independent_build_messages_does_not_fallback_to_flat_history(self) -> None:
        messages = agent_runtime.build_messages(
            "一个没有关键词的新问题",
            [
                {"role": "user", "content": "old flat user"},
                {"role": "assistant", "content": "old flat assistant"},
            ],
            "ui",
            subject="math",
            recent_turns=[],
            use_independent_context=True,
        )
        joined = "\n".join(str(item.get("content", "")) for item in messages)
        self.assertNotIn("old flat user", joined)
        self.assertNotIn("old flat assistant", joined)
        self.assertIn("一个没有关键词的新问题", joined)

    def test_followup_dag_context_uses_previous_turn_for_weak_followup(self) -> None:
        session_id = "unit2_followup_dag"
        kaoyan_agent.save_session(session_id, {
            "session_id": session_id,
            "turns": [
                {
                    "turn_id": 1,
                    "user_query": "求 f(x) 的泰勒展开",
                    "assistant_answer": "根问题：在 x=0 展开，保留 Peano 余项。",
                },
                {
                    "turn_id": 2,
                    "user_query": "第二个题的余项呢？",
                    "assistant_answer": "第二个题的余项是 o(x^3)。",
                    "memory": {"followup_parent_turn_id": 1},
                },
            ],
        })

        payload = agent_runtime.format_followup_dag_context(session_id, "这个为什么成立？", "ui", None)

        self.assertEqual(payload["followup_dag"]["parent_turn_id"], 2)
        self.assertEqual(payload["followup_dag"]["chain_turn_ids"], [1, 2])
        self.assertIn("DAG 链路", payload["followup_context"])
        self.assertIn("turn 1", payload["followup_context"])
        self.assertIn("turn 2", payload["followup_context"])
        self.assertIn("根问题", payload["root_context"])

    def test_answer_math_followup_receives_dag_memory_and_records_trace(self) -> None:
        captured: dict[str, str] = {}

        def fake_followup(user_query: str, root_context: str, followup_context: str, followup_type: str, output_format: str) -> str:
            captured.update({
                "user_query": user_query,
                "root_context": root_context,
                "followup_context": followup_context,
                "followup_type": followup_type,
                "output_format": output_format,
            })
            return "DAG followup answer"

        def resolver(args: dict[str, Any]) -> dict[str, Any]:
            return {
                "user_query": args["user_query"],
                "root_context": "root turn memory",
                "followup_context": "DAG 链路：EMPTY(0) -> turn 1 -> turn 2",
                "followup_type": "weak_followup_previous",
                "output_format": "ui",
                "followup_dag": {
                    "lookback": 5,
                    "parent_turn_id": 2,
                    "chain_turn_ids": [1, 2],
                    "reason": "weak_context_default_previous",
                    "empty_root_id": 0,
                },
            }

        with patch.dict(os.environ, {"ENABLE_CONTEXT_FOLLOWUP_TOOLS": "1"}), patch(
            "agent_runtime.legacy_agent.explain_math_followup_with_qwenmath",
            side_effect=fake_followup,
        ):
            tools = agent_runtime.build_math_tools(followup_context_resolver=resolver)
            args = {"user_query": "这个为什么成立？", "root_context": "", "followup_context": ""}
            answer = tools["answer_math_followup"].func(args)

        self.assertEqual(answer, "DAG followup answer")
        self.assertEqual(captured["root_context"], "root turn memory")
        self.assertIn("DAG 链路", captured["followup_context"])
        self.assertEqual(args["_followup_dag"]["parent_turn_id"], 2)

    def test_llm_classified_weak_followup_uses_dag_memory_for_controller(self) -> None:
        session_id = "unit2_forced_weak_followup"
        kaoyan_agent.save_session(session_id, {
            "session_id": session_id,
            "turns": [
                {
                    "turn_id": 1,
                    "user_query": "e的x次方加上e的-x次方整体除以2的泰勒展开，以及x=0.1的5阶泰勒展开的估值是",
                    "assistant_answer": "f(x)=cosh x，5阶近似为 1+x^2/2+x^4/24，x=0.1 时约 1.0050041667。",
                },
            ],
        })
        client = FakeClient([
            fake_response(content='{"category":"weak_nonstep_followup","parent_turn_id":1,"reason":"当前只问六阶，默认追问上一轮泰勒估值"}'),
            fake_response(content="六阶近似加入 x^6/720。"),
        ])
        with patch.dict(os.environ, {"ENABLE_CONTEXT_FOLLOWUP_TOOLS": "1"}), patch(
            "agent_runtime.classify_subject",
            return_value="math",
        ):
            result = agent_runtime.run_standard_message_loop(
                "六阶呢",
                session_id=session_id,
                client=client,
                persist=False,
            )

        self.assertEqual(result.answer, "六阶近似加入 x^6/720。")
        self.assertEqual(len(client.chat.completions.calls), 2)
        self.assertEqual(result.tool_calls, [])
        self.assertEqual(result.extra_memory["followup_dag"]["parent_turn_id"], 1)
        self.assertEqual(result.extra_memory["followup_dag"]["reason"], "当前只问六阶，默认追问上一轮泰勒估值")
        final_messages = client.chat.completions.calls[1]["messages"]
        final_joined = "\n".join(str(item.get("content", "")) for item in final_messages)
        self.assertIn("DAG 追问链路记忆", final_joined)
        self.assertIn("turn 1", final_joined)
        self.assertIn("cosh", final_joined)
        self.assertEqual(len(final_messages), 2)

    def test_context_followup_uses_single_unified_route_before_answer(self) -> None:
        session_id = "unit2_unified_route"
        kaoyan_agent.save_session(session_id, {
            "session_id": session_id,
            "turns": [
                {
                    "turn_id": 1,
                    "user_query": "expand cosh(x)",
                    "assistant_answer": "cosh(x)=1+x^2/2+x^4/24+...",
                },
            ],
        })
        client = FakeClient([
            fake_response(content='{"category":"weak_nonstep_followup","parent_turn_id":1,"reason":"continues the previous expansion"}'),
            fake_response(content="add the x^6/720 term"),
        ])
        with patch.dict(os.environ, {"ENABLE_CONTEXT_FOLLOWUP_TOOLS": "1"}), patch(
            "agent_runtime.classify_subject",
            side_effect=AssertionError("subject classification should be part of unified route"),
        ):
            result = agent_runtime.run_standard_message_loop(
                "sixth order?",
                session_id=session_id,
                client=client,
                persist=False,
            )

        self.assertEqual(result.subject, "math")
        self.assertEqual(result.answer, "add the x^6/720 term")
        self.assertEqual(len(client.chat.completions.calls), 2)
        step_names = [step["name"] for step in result.metrics["steps"]]
        self.assertIn("route_classifier", step_names)
        self.assertNotIn("followup_route_classifier", step_names)

    def test_independent_runtime_uses_selected_context_not_flat_history(self) -> None:
        session_id = "unit2_independent_selected_context"
        kaoyan_agent.save_session(session_id, {
            "session_id": session_id,
            "turns": [
                {
                    "turn_id": 1,
                    "user_query": "特征值与特征向量的几何意义是什么？",
                    "assistant_answer": "特征值开头\n\n特征值表示线性变换中的伸缩倍数。\n\n特征值结尾",
                    "route": {"subject": "math"},
                },
                {
                    "turn_id": 2,
                    "user_query": "等价无穷小是什么？",
                    "assistant_answer": "不应进入当前独立问题。",
                    "route": {"subject": "math"},
                },
            ],
        })
        appendable_result = agent_runtime.RuntimeResult(
            "old md answer not selected",
            "math",
            [],
            [],
            {"request_id": "seed", "session_id": session_id},
        )
        agent_runtime.append_md_turn(session_id, "old md user not selected", appendable_result.answer, {"turn_id": 99})
        client = FakeClient([
            fake_response(content='{"subject":"math","is_followup":false,"followup_category":"independent","parent_turn_id":null,"parent_turn_ids":[],"reason":"new independent linear algebra question","clarification":null}'),
            fake_response(content="final independent answer"),
        ])

        with patch.dict(os.environ, {"ENABLE_CONTEXT_FOLLOWUP_TOOLS": "1"}):
            result = agent_runtime.run_standard_message_loop(
                "特征值怎么计算？",
                session_id=session_id,
                client=client,
                persist=False,
            )

        joined = "\n".join(str(item.get("content", "")) for item in result.messages)
        self.assertEqual(result.answer, "final independent answer")
        self.assertIn("当前问题已判定为独立问题", joined)
        self.assertIn("特征值表示线性变换中的伸缩倍数", joined)
        self.assertNotIn("old md user not selected", joined)
        self.assertNotIn("old md answer not selected", joined)
        self.assertNotIn("不应进入当前独立问题", joined)

    def test_explicit_new_exam_request_is_not_remounted_as_followup(self) -> None:
        session_id = "unit2_explicit_exam_independent"
        kaoyan_agent.save_session(session_id, {
            "session_id": session_id,
            "turns": [
                {
                    "turn_id": 1,
                    "user_query": "17 year question 1",
                    "assistant_answer": "Please clarify the subject.",
                },
            ],
        })
        client = FakeClient([
            fake_response(content='{"subject":"math","is_followup":true,"followup_category":"contextual_nonstep_followup","parent_turn_id":1,"parent_turn_ids":[1],"reason":"tries to continue history"}'),
            fake_response(tool_calls=[{
                "name": "direct_math_tool",
                "arguments": {"x": 1},
            }]),
        ])
        direct_tool = agent_runtime.ToolSpec(
            name="direct_math_tool",
            description="direct",
            parameters=agent_runtime.json_schema({"x": {"type": "integer"}}, ["x"]),
            func=lambda args: "direct answer",
            return_mode="direct",
        )
        with patch.dict(os.environ, {"ENABLE_CONTEXT_FOLLOWUP_TOOLS": "1"}), patch(
            "agent_runtime.select_tools",
            return_value={"direct_math_tool": direct_tool},
        ):
            result = agent_runtime.run_standard_message_loop(
                "2018 math1 question 3",
                session_id=session_id,
                client=client,
                persist=False,
            )

        self.assertEqual(result.answer, "direct answer")
        self.assertEqual(result.tool_calls[0]["name"], "direct_math_tool")
        self.assertNotIn("llm_dag_followup_final", [step["name"] for step in result.metrics["steps"]])

    def test_llm_classified_step_followup_is_not_forced_to_answer_math_followup(self) -> None:
        session_id = "unit2_step_followup_not_forced"
        kaoyan_agent.save_session(session_id, {
            "session_id": session_id,
            "turns": [
                {
                    "turn_id": 1,
                    "user_query": "求一道题的完整解法",
                    "assistant_answer": "第一步化简，第二步代入。",
                },
            ],
        })
        direct_tool = agent_runtime.ToolSpec(
            name="direct_math_tool",
            description="direct",
            parameters=agent_runtime.json_schema({}),
            func=lambda args: "普通总控工具路径",
            return_mode="direct",
        )
        client = FakeClient([
            fake_response(content='{"category":"step_followup","parent_turn_id":1,"reason":"用户追问第二步"}'),
            fake_response(tool_calls=[{"name": "direct_math_tool", "arguments": {}}]),
        ])
        with patch.dict(os.environ, {"ENABLE_CONTEXT_FOLLOWUP_TOOLS": "1"}), patch(
            "agent_runtime.classify_subject",
            return_value="math",
        ), patch(
            "agent_runtime.select_tools",
            return_value={
                "answer_math_followup": agent_runtime.ToolSpec(
                    name="answer_math_followup",
                    description="followup",
                    parameters=agent_runtime.json_schema({}),
                    func=lambda args: "不应调用",
                    return_mode="direct",
                ),
                "direct_math_tool": direct_tool,
            },
        ):
            result = agent_runtime.run_standard_message_loop(
                "第二步为什么这样做",
                session_id=session_id,
                client=client,
                persist=False,
            )

        self.assertEqual(result.answer, "普通总控工具路径")
        self.assertEqual(result.tool_calls[0]["name"], "direct_math_tool")
        self.assertEqual(len(client.chat.completions.calls), 2)

    def test_contextual_nonstep_followup_with_parent_uses_dag_memory_for_controller(self) -> None:
        session_id = "unit2_contextual_followup_dag"
        kaoyan_agent.save_session(session_id, {
            "session_id": session_id,
            "turns": [
                {"turn_id": 1, "user_query": "第一个函数的泰勒展开", "assistant_answer": "第一个是 e^x。"},
                {"turn_id": 2, "user_query": "第二个函数的泰勒展开", "assistant_answer": "第二个是 cosh x。"},
            ],
        })
        client = FakeClient([
            fake_response(content='{"category":"contextual_nonstep_followup","parent_turn_id":2,"reason":"用户追问第二个函数的余项"}'),
            fake_response(content="第二个函数的余项应沿 cosh x 的偶次展开判断。"),
        ])
        with patch.dict(os.environ, {"ENABLE_CONTEXT_FOLLOWUP_TOOLS": "1"}), patch(
            "agent_runtime.classify_subject",
            return_value="math",
        ):
            result = agent_runtime.run_standard_message_loop(
                "第二个函数的余项呢",
                session_id=session_id,
                client=client,
                persist=False,
            )

        self.assertEqual(result.answer, "第二个函数的余项应沿 cosh x 的偶次展开判断。")
        self.assertEqual(result.tool_calls, [])
        self.assertEqual(result.extra_memory["followup_dag"]["parent_turn_id"], 2)
        final_joined = "\n".join(str(item.get("content", "")) for item in client.chat.completions.calls[1]["messages"])
        self.assertIn("DAG 追问链路记忆", final_joined)
        self.assertIn("turn 2", final_joined)
        self.assertIn("cosh x", final_joined)

    def test_contextual_nonstep_followup_can_use_multiple_parents(self) -> None:
        session_id = "unit2_multi_parent_followup_dag"
        kaoyan_agent.save_session(session_id, {
            "session_id": session_id,
            "turns": [
                {"turn_id": 1, "user_query": "积分第一中值定理", "assistant_answer": "积分第一中值定理用于积分平均值。"},
                {"turn_id": 2, "user_query": "泰勒中值定理", "assistant_answer": "泰勒中值定理用于函数局部多项式逼近和余项估计。"},
            ],
        })
        client = FakeClient([
            fake_response(content='{"category":"contextual_nonstep_followup","parent_turn_id":2,"parent_turn_ids":[1,2],"reason":"用户问这两个定理的应用场景"}'),
            fake_response(content="积分第一中值定理偏积分估计，泰勒中值定理偏局部近似。"),
        ])
        with patch.dict(os.environ, {"ENABLE_CONTEXT_FOLLOWUP_TOOLS": "1"}), patch(
            "agent_runtime.classify_subject",
            return_value="math",
        ):
            result = agent_runtime.run_standard_message_loop(
                "这两个应用场景分别是什么",
                session_id=session_id,
                client=client,
                persist=False,
            )

        dag = result.extra_memory["followup_dag"]
        self.assertEqual(dag["parent_turn_id"], 2)
        self.assertEqual(dag["parent_turn_ids"], [1, 2])
        self.assertEqual(dag["chain_turn_ids"], [1, 2])
        final_joined = "\n".join(str(item.get("content", "")) for item in client.chat.completions.calls[1]["messages"])
        self.assertIn("DAG 子图", final_joined)
        self.assertIn("当前节点父节点：turn 1, turn 2", final_joined)
        self.assertIn("积分第一中值定理", final_joined)
        self.assertIn("泰勒中值定理", final_joined)
        self.assertEqual(result.metrics["llm_calls"], 2)
        self.assertEqual(result.metrics["prompt_tokens"], 20)
        self.assertEqual(result.metrics["completion_tokens"], 10)

    def test_ambiguous_nonstep_followup_asks_clarification_with_recent_5(self) -> None:
        session_id = "unit2_ambiguous_followup"
        kaoyan_agent.save_session(session_id, {
            "session_id": session_id,
            "turns": [
                {"turn_id": 1, "user_query": "罗尔定理", "assistant_answer": "罗尔定理要求闭区间连续、开区间可导。"},
                {"turn_id": 2, "user_query": "积分第一中值定理", "assistant_answer": "积分第一中值定理要求闭区间连续。"},
            ],
        })
        client = FakeClient([
            fake_response(content='{"category":"ambiguous","parent_turn_id":null,"reason":"这个可能指两个定理"}'),
            fake_response(content="你这里的“这个”是指罗尔定理，还是积分第一中值定理？"),
        ])
        with patch.dict(os.environ, {"ENABLE_CONTEXT_FOLLOWUP_TOOLS": "1"}), patch(
            "agent_runtime.classify_subject",
            return_value="math",
        ):
            result = agent_runtime.run_standard_message_loop(
                "这个还成立吗",
                session_id=session_id,
                client=client,
                persist=False,
            )

        self.assertIn("罗尔定理", result.answer)
        self.assertEqual(result.tool_calls, [])
        self.assertIsNone(result.extra_memory)
        final_messages = client.chat.completions.calls[1]["messages"]
        final_joined = "\n".join(str(item.get("content", "")) for item in final_messages)
        self.assertIn("最近 6 轮候选", final_joined)
        self.assertIn("turn 1", final_joined)
        self.assertIn("turn 2", final_joined)
        self.assertEqual(len(final_messages), 2)

    def test_politics_contextual_followup_can_use_dag_memory(self) -> None:
        session_id = "unit_politics_followup_dag"
        kaoyan_agent.save_session(session_id, {
            "session_id": session_id,
            "turns": [
                {
                    "turn_id": 1,
                    "user_query": "politics money question",
                    "assistant_answer": "root context about worn gold coin and circulation.",
                },
            ],
        })
        politics_tool = agent_runtime.ToolSpec(
            name="search_politics_knowledge",
            description="politics",
            parameters=agent_runtime.json_schema({"query": {"type": "string"}}, ["query"]),
            func=lambda args: "politics evidence",
            return_mode="evidence",
        )
        client = FakeClient([
            fake_response(content='{"subject":"politics","is_followup":true,"followup_category":"contextual_nonstep_followup","parent_turn_id":1,"parent_turn_ids":[1],"reason":"clarifies previous politics turn"}'),
            fake_response(content="politics followup answer"),
        ])
        with patch.dict(os.environ, {"ENABLE_CONTEXT_FOLLOWUP_TOOLS": "1"}), patch(
            "agent_runtime.classify_subject",
            return_value="politics",
        ), patch(
            "agent_runtime.select_tools",
            return_value={"search_politics_knowledge": politics_tool},
        ):
            result = agent_runtime.run_standard_message_loop(
                "I mean the worn gold coin case",
                session_id=session_id,
                client=client,
                persist=False,
            )

        self.assertEqual(result.subject, "politics")
        self.assertEqual(result.answer, "politics followup answer")
        self.assertEqual(result.tool_calls, [])
        self.assertEqual(result.extra_memory["followup_dag"]["parent_turn_id"], 1)

    def test_visual_prompts_use_generic_region_rules(self) -> None:
        self.assertIn("实际边界", kaoyan_agent.QWEN_VL_OCR_PROMPT)
        self.assertIn("不等式或参数范围", kaoyan_agent.QWEN_VL_OCR_PROMPT)
        self.assertNotIn("正方形被两条对角线", kaoyan_agent.QWEN_VL_OCR_PROMPT)
        self.assertNotIn("上、左、下、右", kaoyan_agent.QWEN_VL_OCR_PROMPT)

    def test_image_without_explicit_exam_reference_hides_exam_tools(self) -> None:
        tools = agent_runtime.filter_tools_for_request(agent_runtime.build_math_tools(), "这张图片的分段函数怎么处理？", True)
        self.assertNotIn("solve_exam_question", tools)
        self.assertNotIn("show_math_exam_question", tools)
        self.assertIn("ocr_math_image", tools)
        self.assertIn("solve_general_math", tools)

    def test_image_with_explicit_exam_reference_keeps_exam_tools(self) -> None:
        tools = agent_runtime.filter_tools_for_request(agent_runtime.build_math_tools(), "2009 年数一第 3 题这张图怎么做？", True)
        self.assertIn("solve_exam_question", tools)
        cn_number_tools = agent_runtime.filter_tools_for_request(agent_runtime.build_math_tools(), "09年数一第二题这张图怎么做？", True)
        self.assertIn("solve_exam_question", cn_number_tools)

    def test_load_normalized_math1_2009_question(self) -> None:
        problem = kaoyan_agent.load_problem(2009, 2, "math1")
        self.assertIn("### 第 2 题", problem.question_text)
        self.assertIn("- 题号：2", problem.question_text)
        self.assertIn("D_1` 为上方三角形", problem.question_text)
        self.assertIn("-1 <= y <= 1, -1 <= x <= -|y|", problem.question_text)
        self.assertIn("max { I_k | 1 <= k <= 4 }", problem.question_text)
        self.assertNotIn("- 题号：3", problem.question_text)
        self.assertEqual(problem.answer_text, "A")

    def test_problem_image_paths_resolve_database_diagram(self) -> None:
        problem = kaoyan_agent.load_problem(2009, 2, "math1")
        paths = kaoyan_agent.problem_image_paths(problem)
        self.assertTrue(paths)
        self.assertEqual(paths[0].name, "q02_diagram.png")
        self.assertTrue(paths[0].exists())

    def test_solve_exam_question_ocr_database_images_before_math(self) -> None:
        problem = kaoyan_agent.load_problem(2009, 2, "math1")
        calls: dict[str, list[dict]] = {"ocr": [], "solve": []}

        def problem_payload() -> dict:
            return {
                "exam_type": problem.exam_type,
                "year": problem.year,
                "question_number": problem.question_number,
                "question_text": problem.question_text,
                "answer_text": problem.answer_text,
                "question_source": str(problem.question_source),
                "answer_source": str(problem.answer_source) if problem.answer_source else None,
            }

        fake_toolkit = SimpleNamespace(
            search_math_exam=lambda args: problem_payload(),
            ocr_math_image=lambda args: calls["ocr"].append(args) or "OCR：识别到四个区域 D1-D4。",
            solve_math_exam=lambda args: calls["solve"].append(args) or "最终答案：A",
            judge_math_answer=lambda args: {"match": True},
        )
        with patch("agent_runtime.legacy_agent.get_toolkit", return_value=fake_toolkit):
            tools = agent_runtime.build_math_tools()
            answer = tools["solve_exam_question"].func({
                "exam_type": "math1",
                "year": 2009,
                "question_number": 2,
                "user_query": "09 年数一第二题怎么做",
                "output_format": "ui",
            })

        self.assertEqual(answer, "最终答案：A")
        self.assertEqual(len(calls["ocr"]), 1)
        self.assertIn("q02_diagram.png", calls["ocr"][0]["image_paths"][0])
        self.assertEqual(calls["solve"][0]["vl_text"], "OCR：识别到四个区域 D1-D4。")

    def test_standard_tool_loop_executes_tool_and_returns_final_answer(self) -> None:
        dummy_tool = agent_runtime.ToolSpec(
            name="dummy_math_tool",
            description="dummy",
            parameters=agent_runtime.json_schema({"x": {"type": "integer"}}, ["x"]),
            func=lambda args: {"value": args["x"] + 1},
        )
        client = FakeClient([
            fake_response(tool_calls=[{"name": "dummy_math_tool", "arguments": {"x": 2}}]),
            fake_response(content="最终答案：3"),
        ])
        with patch("agent_runtime.classify_subject", return_value="math"), patch("agent_runtime.select_tools", return_value={"dummy_math_tool": dummy_tool}):
            result = agent_runtime.run_standard_message_loop(
                "算一下",
                session_id="unit2_loop",
                client=client,
                persist=False,
            )
        self.assertEqual(result.answer, "最终答案：3")
        self.assertEqual(result.tool_calls[0]["name"], "dummy_math_tool")
        self.assertTrue(result.tool_calls[0]["ok"])
        self.assertEqual(result.metrics["tool_success_rate"], 1.0)
        self.assertEqual(len(client.chat.completions.calls), 2)
        tool_message = result.messages[-2]
        self.assertEqual(tool_message["role"], "tool")
        self.assertIn('"value": 3', tool_message["content"])

    def test_single_direct_tool_returns_without_final_llm(self) -> None:
        direct_tool = agent_runtime.ToolSpec(
            name="direct_math_tool",
            description="direct",
            parameters=agent_runtime.json_schema({"x": {"type": "integer"}}, ["x"]),
            func=lambda args: f"直接答案：{args['x'] + 1}",
            return_mode="direct",
        )
        client = FakeClient([
            fake_response(tool_calls=[{"name": "direct_math_tool", "arguments": {"x": 2}}]),
        ])
        with patch("agent_runtime.classify_subject", return_value="math"), patch("agent_runtime.select_tools", return_value={"direct_math_tool": direct_tool}):
            result = agent_runtime.run_standard_message_loop(
                "算一下",
                session_id="unit2_direct",
                client=client,
                persist=False,
            )
        self.assertEqual(result.answer, "直接答案：3")
        self.assertEqual(len(client.chat.completions.calls), 1)
        self.assertTrue(any(step["name"] == "direct_tool_return" for step in result.metrics["steps"]))

    def test_multiple_tools_keep_final_llm_summary(self) -> None:
        evidence_tool = agent_runtime.ToolSpec(
            name="evidence_tool",
            description="evidence",
            parameters=agent_runtime.json_schema({}),
            func=lambda args: "OCR 结果",
            return_mode="evidence",
        )
        direct_tool = agent_runtime.ToolSpec(
            name="direct_math_tool",
            description="direct",
            parameters=agent_runtime.json_schema({}),
            func=lambda args: "完整解答",
            return_mode="direct",
        )
        client = FakeClient([
            fake_response(tool_calls=[{"name": "evidence_tool", "arguments": {}}]),
            fake_response(tool_calls=[{"name": "direct_math_tool", "arguments": {}}]),
            fake_response(content="总控总结后的答案"),
        ])
        with patch("agent_runtime.classify_subject", return_value="math"), patch(
            "agent_runtime.select_tools",
            return_value={"evidence_tool": evidence_tool, "direct_math_tool": direct_tool},
        ):
            result = agent_runtime.run_standard_message_loop(
                "看图解题",
                session_id="unit2_multi_tool",
                client=client,
                persist=False,
            )
        self.assertEqual(result.answer, "总控总结后的答案")
        self.assertEqual(len(client.chat.completions.calls), 3)
        self.assertFalse(any(step["name"] == "direct_tool_return" for step in result.metrics["steps"]))

    def test_tool_error_is_logged_in_result(self) -> None:
        broken_tool = agent_runtime.ToolSpec(
            name="broken_tool",
            description="broken",
            parameters=agent_runtime.json_schema({}),
            func=lambda args: (_ for _ in ()).throw(ValueError("bad args")),
        )
        client = FakeClient([
            fake_response(tool_calls=[{"name": "broken_tool", "arguments": {}}]),
            fake_response(content="工具失败，需要澄清。"),
        ])
        with patch("agent_runtime.classify_subject", return_value="math"), patch("agent_runtime.select_tools", return_value={"broken_tool": broken_tool}):
            result = agent_runtime.run_standard_message_loop(
                "测试异常",
                session_id="unit2_error",
                client=client,
                persist=False,
            )
        self.assertFalse(result.tool_calls[0]["ok"])
        self.assertIn("bad args", result.tool_calls[0]["error"])
        self.assertEqual(result.metrics["tool_errors"], 1)

    def test_recent_15_turn_history_is_passed_verbatim_for_deep_followup(self) -> None:
        session_id = "unit2_history"
        turns = []
        for index in range(1, 18):
            turns.append({
                "turn_id": index,
                "time": "2026-05-29T00:00:00",
                "user_query": f"考研数学 root question {index}",
                "assistant_answer": f"数学解法 root solution {index}: step A -> step B",
            })
        kaoyan_agent.save_session(session_id, {"session_id": session_id, "turns": turns})
        dummy_tool = agent_runtime.ToolSpec(
            name="explain_math_step",
            description="dummy explain",
            parameters=agent_runtime.json_schema({
                "previous_context": {"type": "string"},
                "user_query": {"type": "string"},
            }, ["previous_context", "user_query"]),
            func=lambda args: f"解释：{args['previous_context'][:20]}",
        )
        client = FakeClient([
            fake_response(content='{"category":"step_followup","parent_turn_id":17,"reason":"追问第 2 步"}'),
            fake_response(tool_calls=[{
                "name": "explain_math_step",
                "arguments": {
                    "previous_context": "root solution 17: step A -> step B",
                    "user_query": "第 2 步怎么来的？",
                },
            }]),
            fake_response(content="第 2 步来自前面的变形。"),
        ])
        with patch("agent_runtime.select_tools", return_value={"explain_math_step": dummy_tool}):
            result = agent_runtime.run_standard_message_loop(
                "第 2 步怎么来的？",
                session_id=session_id,
                client=client,
                persist=False,
            )
        first_call_messages = client.chat.completions.calls[1]["messages"]
        joined = "\n".join(str(item.get("content", "")) for item in first_call_messages)
        self.assertNotIn("root question 2", joined)
        self.assertIn("root question 3", joined)
        self.assertIn("root solution 17: step A -> step B", joined)
        self.assertEqual(result.answer, "第 2 步来自前面的变形。")


class AgentRuntimeRealApiSmokeTest(unittest.TestCase):
    @unittest.skipUnless(
        (ROOT / ".env").exists() and __import__("os").environ.get("RUN_REAL_API_TESTS") == "1",
        "set RUN_REAL_API_TESTS=1 to run the real API smoke test",
    )
    def test_real_api_math_general_smoke(self) -> None:
        result = agent_runtime.run_standard_message_loop(
            "求极限 lim_{x->0} sin(x)/x，只给最终答案。",
            session_id="real_api_smoke",
            output_format="terminal",
            persist=False,
        )
        self.assertTrue(result.answer.strip())
        self.assertEqual(result.subject, "math")
        self.assertGreaterEqual(result.metrics["llm_calls"], 1)


if __name__ == "__main__":
    unittest.main()
