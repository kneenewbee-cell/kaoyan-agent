from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Callable
from unittest.mock import patch

from qa import agent_runtime

ROOT = Path(__file__).resolve().parent
CASES_DIR = ROOT / "cases"
PROJECT_ROOT = ROOT.parents[1]
SESSION_REPLAY_IDS = ("4", "default", "user_25_dag_parent_eval_v5")


@dataclass
class EvalResult:
    suite: str
    case_id: str
    ok: bool
    detail: str


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows = []
    with path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_number}: {exc}") from exc
    return rows


def turn_history_to_messages(turns: list[dict[str, Any]]) -> list[dict[str, str]]:
    messages: list[dict[str, str]] = []
    for turn in turns:
        user_query = str(turn.get("user_query") or turn.get("user") or "")
        assistant_answer = str(turn.get("assistant_answer") or turn.get("assistant") or "")
        if user_query:
            messages.append({"role": "user", "content": user_query})
        if assistant_answer:
            messages.append({"role": "assistant", "content": assistant_answer})
    return messages


def assert_equal(actual: Any, expected: Any, label: str) -> tuple[bool, str]:
    if actual == expected:
        return True, f"{label}={actual!r}"
    return False, f"{label}: expected {expected!r}, got {actual!r}"


def fake_response(content: str = "", tool_calls: list[dict[str, Any]] | None = None) -> SimpleNamespace:
    calls = []
    for item in tool_calls or []:
        calls.append(
            SimpleNamespace(
                id=item.get("id", f"call_{len(calls) + 1}"),
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
        self.calls: list[dict[str, Any]] = []

    def create(self, **kwargs: Any) -> SimpleNamespace:
        self.calls.append(kwargs)
        if not self.responses:
            raise AssertionError("No fake route response left")
        return self.responses.pop(0)


class FakeClient:
    def __init__(self, responses: list[SimpleNamespace]) -> None:
        self.chat = SimpleNamespace(completions=FakeCompletions(responses))


def eval_subject_cases() -> list[EvalResult]:
    rows = read_jsonl(CASES_DIR / "politics_subject_cases.jsonl")
    results: list[EvalResult] = []
    for row in rows:
        history = turn_history_to_messages(row.get("history") or [])
        actual = agent_runtime.classify_subject_heuristic(
            str(row["user_input"]),
            history=history,
        )
        expected = row["expected"]["subject"]
        ok, detail = assert_equal(actual, expected, "subject")
        results.append(EvalResult("subject_heuristic", row["id"], ok, detail))
    return results


def eval_followup_cases() -> list[EvalResult]:
    rows = [
        *read_jsonl(CASES_DIR / "politics_followup_cases.jsonl"),
        *read_jsonl(CASES_DIR / "math_followup_cases.jsonl"),
    ]
    results: list[EvalResult] = []
    for row in rows:
        history = turn_history_to_messages(row.get("history") or [])
        actual = agent_runtime.classify_followup_heuristic(str(row["user_input"]), history) or "independent"
        expected = row["expected"]["followup_category"]
        ok, detail = assert_equal(actual, expected, "followup_category")
        results.append(EvalResult("followup_heuristic", row["id"], ok, detail))
    return results


def combined_route_case_rows() -> list[dict[str, Any]]:
    return [
        *read_jsonl(CASES_DIR / "math_combined_route_cases.jsonl"),
        *read_jsonl(CASES_DIR / "politics_combined_route_cases.jsonl"),
    ]


def eval_combined_route_cases() -> list[EvalResult]:
    rows = combined_route_case_rows()
    results: list[EvalResult] = []
    for row in rows:
        history = turn_history_to_messages(row.get("history") or [])
        recent_turns = list(row.get("recent_turns") or row.get("history") or [])
        client = FakeClient([fake_response(json.dumps(row["llm_response"], ensure_ascii=False))])
        metrics = agent_runtime.RuntimeMetrics(f"eval_{row['id']}", "eval")
        route = agent_runtime.build_route_decision(
            str(row["user_input"]),
            history,
            recent_turns,
            False,
            client,
            metrics,
        )
        expected = row["expected"]
        checks = [
            assert_equal(route.subject, expected.get("subject"), "subject"),
            assert_equal(route.followup_category, expected.get("followup_category"), "followup_category"),
            assert_equal(route.parent_turn_ids, expected.get("parent_turn_ids") or [], "parent_turn_ids"),
        ]
        failed = [detail for ok, detail in checks if not ok]
        ok = not failed
        detail = (
            f"route={{subject:{route.subject!r}, category:{route.followup_category!r}, "
            f"parents:{route.parent_turn_ids!r}}}"
        )
        if failed:
            detail += "; " + "; ".join(failed)
        results.append(EvalResult("combined_route", row["id"], ok, detail))
    return results


def eval_real_route_cases() -> list[EvalResult]:
    rows = combined_route_case_rows()
    results: list[EvalResult] = []
    client = agent_runtime.make_client()
    for row in rows:
        history = turn_history_to_messages(row.get("history") or [])
        recent_turns = list(row.get("recent_turns") or row.get("history") or [])
        metrics = agent_runtime.RuntimeMetrics(f"real_eval_{row['id']}", "real_eval")
        route = agent_runtime.build_route_decision(
            str(row["user_input"]),
            history,
            recent_turns,
            False,
            client,
            metrics,
        )
        expected = row["expected"]
        checks = [
            assert_equal(route.subject, expected.get("subject"), "subject"),
            assert_equal(route.followup_category, expected.get("followup_category"), "followup_category"),
        ]
        if expected.get("parent_turn_ids"):
            checks.append(assert_equal(route.parent_turn_ids, expected.get("parent_turn_ids"), "parent_turn_ids"))
        failed = [detail for ok, detail in checks if not ok]
        ok = not failed
        detail = (
            f"route={{subject:{route.subject!r}, category:{route.followup_category!r}, "
            f"parents:{route.parent_turn_ids!r}}}"
        )
        if failed:
            detail += "; " + "; ".join(failed)
        results.append(EvalResult("real_route", row["id"], ok, detail))
    return results


def eval_tool_registry_cases() -> list[EvalResult]:
    rows = read_jsonl(CASES_DIR / "politics_tool_registry_cases.jsonl")
    results: list[EvalResult] = []
    for row in rows:
        tools = agent_runtime.select_tools(str(row["subject"]))
        names = set(tools)
        expected = set(row.get("expected_tools") or [])
        forbidden = set(row.get("forbidden_tools") or [])
        missing = sorted(expected - names)
        unexpected = sorted(forbidden & names)
        ok = not missing and not unexpected
        detail = f"tools={sorted(names)}"
        if missing:
            detail += f"; missing={missing}"
        if unexpected:
            detail += f"; forbidden_present={unexpected}"
        results.append(EvalResult("tool_registry", row["id"], ok, detail))
    return results


def eval_policy_cases() -> list[EvalResult]:
    rows = read_jsonl(CASES_DIR / "politics_policy_cases.jsonl")
    results: list[EvalResult] = []
    policy = agent_runtime.POLITICS_TOOL_SELECTION_POLICY
    route_prompt = agent_runtime.ROUTE_CLASSIFIER_PROMPT
    prompt_map = {
        "politics_tool_selection_policy": policy,
        "route_classifier_prompt": route_prompt,
    }
    for row in rows:
        text = prompt_map[str(row["prompt"])]
        required = [str(item) for item in row.get("required_contains") or []]
        missing = [item for item in required if item not in text]
        ok = not missing
        detail = "all required text present" if ok else f"missing={missing}"
        results.append(EvalResult("prompt_policy", row["id"], ok, detail))
    return results


def eval_answer_rubric_cases() -> list[EvalResult]:
    rows = read_jsonl(CASES_DIR / "politics_answer_rubric_cases.jsonl")
    results: list[EvalResult] = []
    for row in rows:
        answer = str(row.get("answer") or "")
        required = [str(item) for item in row.get("required_contains") or []]
        forbidden = [str(item) for item in row.get("forbidden_contains") or []]
        missing = [item for item in required if item not in answer]
        present_forbidden = [item for item in forbidden if item in answer]
        ok = not missing and not present_forbidden
        detail = "rubric satisfied"
        if missing:
            detail += f"; missing={missing}"
        if present_forbidden:
            detail += f"; forbidden_present={present_forbidden}"
        results.append(EvalResult("answer_rubric", row["id"], ok, detail))
    return results


def eval_session_replay_cases() -> list[EvalResult]:
    results: list[EvalResult] = []
    politics_markers = [
        "政治 tool_selection 策略",
        "近期会议、政策热点、时政新闻",
        "先调用 get_current_affairs",
        "再调用 search_politics_knowledge",
    ]
    forbidden_in_math = [
        "政治 tool_selection 策略",
        "近期会议、政策热点、时政新闻",
        "先调用 get_current_affairs",
        "answer_politics_knowledge",
    ]
    for session_id in SESSION_REPLAY_IDS:
        path = PROJECT_ROOT / "data" / "runtime" / "sessions" / f"{session_id}.json"
        if not path.exists():
            results.append(EvalResult("session_replay", f"{session_id}:missing", False, f"missing {path}"))
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        turns = list(data.get("turns") or [])
        for index, turn in enumerate(turns):
            subject = agent_runtime.normalize_subject((turn.get("route") or {}).get("subject"))
            if subject not in {"math", "politics"}:
                continue
            history = turn_history_to_messages(turns[:index])
            messages = agent_runtime.build_tool_selection_messages(
                str(turn.get("user_query") or ""),
                history,
                "ui",
                subject=subject,
                recent_turns=turns[:index],
            )
            joined = "\n".join(str(item.get("content") or "") for item in messages)
            case_id = f"{session_id}:turn{turn.get('turn_id')}:{subject}"
            if subject == "math":
                unexpected = [marker for marker in forbidden_in_math if marker in joined]
                ok = not unexpected
                detail = "math prompt isolated from politics flow" if ok else f"unexpected_politics_markers={unexpected}"
            else:
                missing = [marker for marker in politics_markers if marker not in joined]
                ok = not missing
                detail = "politics flow prompt present" if ok else f"missing_politics_markers={missing}"
            results.append(EvalResult("session_replay", case_id, ok, detail))

    math_tools = set(agent_runtime.select_tools("math"))
    politics_tools = set(agent_runtime.select_tools("politics"))
    results.append(EvalResult(
        "session_replay",
        "tool_pool:math_isolation",
        not {"search_politics_knowledge", "get_current_affairs", "answer_politics_knowledge"} & math_tools,
        f"math_tools={sorted(math_tools)}",
    ))
    required_politics = {"search_politics_knowledge", "get_current_affairs", "answer_politics_knowledge"}
    results.append(EvalResult(
        "session_replay",
        "tool_pool:politics_flow_tools",
        required_politics <= politics_tools,
        f"politics_tools={sorted(politics_tools)}",
    ))
    return results


def eval_politics_flow_cases() -> list[EvalResult]:
    results: list[EvalResult] = []

    def run_case(
        case_id: str,
        responses: list[SimpleNamespace],
        tools: dict[str, agent_runtime.ToolSpec],
        expected_answer: str,
        expected_tools: list[str],
    ) -> EvalResult:
        client = FakeClient(responses)
        with patch("qa.agent_runtime.classify_subject", return_value="politics"), patch(
            "qa.agent_runtime.select_tools",
            return_value=tools,
        ):
            result = agent_runtime.run_standard_message_loop(
                f"eval {case_id}",
                session_id=f"eval_{case_id}",
                client=client,
                persist=False,
            )
        actual_tools = [item.get("name") for item in result.tool_calls]
        step_names = [step.get("name") for step in result.metrics.get("steps", [])]
        checks = [
            assert_equal(result.answer, expected_answer, "answer"),
            assert_equal(actual_tools, expected_tools, "tool_sequence"),
            assert_equal(step_names[-1] if step_names else "", "direct_tool_return", "last_step"),
        ]
        failed = [detail for ok, detail in checks if not ok]
        detail = f"answer={result.answer!r}; tools={actual_tools}; steps={step_names}"
        if failed:
            detail += "; " + "; ".join(failed)
        return EvalResult("politics_flow", case_id, not failed, detail)

    search_tool = agent_runtime.ToolSpec(
        "search_politics_knowledge",
        "politics evidence",
        agent_runtime.json_schema({}),
        lambda args: '[{"content":"主要矛盾标准表述。"}]',
        return_mode="evidence",
    )
    current_affairs_tool = agent_runtime.ToolSpec(
        "get_current_affairs",
        "current affairs",
        agent_runtime.json_schema({}),
        lambda args: "时政材料：新质生产力相关表述。",
        return_mode="synthesize",
    )
    answer_tool = agent_runtime.ToolSpec(
        "answer_politics_knowledge",
        "politics final answer",
        agent_runtime.json_schema({}),
        lambda args: str(args.get("final") or "政治最终答案"),
        return_mode="direct",
    )

    results.append(run_case(
        "knowledge_rag_answer",
        [
            fake_response(tool_calls=[{"name": "search_politics_knowledge", "arguments": {"query": "主要矛盾"}}]),
            fake_response(tool_calls=[{"name": "answer_politics_knowledge", "arguments": {"final": "知识库成文答案"}}]),
        ],
        {"search_politics_knowledge": search_tool, "answer_politics_knowledge": answer_tool},
        "知识库成文答案",
        ["search_politics_knowledge", "answer_politics_knowledge"],
    ))
    results.append(run_case(
        "current_affairs_theory_answer",
        [
            fake_response(tool_calls=[{"name": "get_current_affairs", "arguments": {"query": "新质生产力"}}]),
            fake_response(tool_calls=[{"name": "search_politics_knowledge", "arguments": {"query": "新质生产力 马原 原理"}}]),
            fake_response(tool_calls=[{"name": "answer_politics_knowledge", "arguments": {"final": "时政映射理论答案"}}]),
        ],
        {
            "get_current_affairs": current_affairs_tool,
            "search_politics_knowledge": search_tool,
            "answer_politics_knowledge": answer_tool,
        },
        "时政映射理论答案",
        ["get_current_affairs", "search_politics_knowledge", "answer_politics_knowledge"],
    ))
    return results


EVALUATORS: dict[str, Callable[[], list[EvalResult]]] = {
    "subject": eval_subject_cases,
    "followup": eval_followup_cases,
    "combined_route": eval_combined_route_cases,
    "tools": eval_tool_registry_cases,
    "policy": eval_policy_cases,
    "rubric": eval_answer_rubric_cases,
    "session_replay": eval_session_replay_cases,
    "politics_flow": eval_politics_flow_cases,
}


def run_all(selected: list[str] | None = None) -> list[EvalResult]:
    names = selected or list(EVALUATORS)
    results: list[EvalResult] = []
    for name in names:
        results.extend(EVALUATORS[name]())
    return results


def print_report(results: list[EvalResult]) -> None:
    passed = sum(1 for item in results if item.ok)
    failed = len(results) - passed
    print(f"QA evaluation summary: total={len(results)} passed={passed} failed={failed}")
    by_suite: dict[str, list[EvalResult]] = {}
    for item in results:
        by_suite.setdefault(item.suite, []).append(item)
    for suite, items in by_suite.items():
        suite_passed = sum(1 for item in items if item.ok)
        print(f"\n[{suite}] {suite_passed}/{len(items)} passed")
        for item in items:
            status = "PASS" if item.ok else "FAIL"
            print(f"  {status} {item.case_id}: {item.detail}")


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run offline QA evaluation cases.")
    parser.add_argument(
        "--suite",
        action="append",
        choices=sorted(EVALUATORS),
        help="Suite to run. Can be passed more than once. Defaults to all suites.",
    )
    parser.add_argument(
        "--real-route",
        action="store_true",
        help="Also run route cases against the configured real LLM. This may call external APIs.",
    )
    parser.add_argument("--strict", action="store_true", help="Exit with code 1 when any case fails.")
    return parser


def main() -> None:
    args = build_arg_parser().parse_args()
    results = run_all(args.suite)
    if args.real_route:
        results.extend(eval_real_route_cases())
    print_report(results)
    if args.strict and any(not item.ok for item in results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
