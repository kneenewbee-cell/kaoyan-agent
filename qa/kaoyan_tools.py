from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable


@dataclass
class LocalTool:
    """Small fallback with a LangChain-like invoke interface."""

    name: str
    description: str
    func: Callable[..., Any]
    args_schema: type | None = None
    return_direct: bool = False

    def invoke(self, tool_input: dict[str, Any]) -> Any:
        return self.func(**tool_input)


def _make_tool(
    *,
    name: str,
    description: str,
    func: Callable[..., Any],
    args_schema: type | None = None,
    return_direct: bool = False,
) -> Any:
    try:
        from langchain_core.tools import StructuredTool

        return StructuredTool.from_function(
            name=name,
            description=description,
            func=func,
            args_schema=args_schema,
            return_direct=return_direct,
        )
    except Exception:
        return LocalTool(
            name=name,
            description=description,
            func=func,
            args_schema=args_schema,
            return_direct=return_direct,
        )


try:
    from pydantic import BaseModel, Field
except Exception:
    BaseModel = object  # type: ignore[assignment]

    def Field(default: Any = None, description: str = "") -> Any:  # type: ignore[misc]
        return default


class SearchMathExamInput(BaseModel):
    exam_type: str = Field(default="math1", description="考试类型：math1、math2、math3")
    year: int = Field(description="考研数学真题年份，例如 2022")
    question_number: int = Field(description="题号，例如 11")


class OCRMathImageInput(BaseModel):
    image_paths: list[str] = Field(description="本地数学题图片路径列表")
    user_query: str = Field(description="用户文字描述或补充")


class SolveMathExamInput(BaseModel):
    exam_type: str = Field(default="math1", description="考试类型：math1、math2、math3")
    year: int = Field(description="考研数学真题年份")
    question_number: int = Field(description="题号")
    user_query: str = Field(description="用户原始问题")
    vl_text: str | None = Field(default=None, description="可选：Qwen-VL 图片识别文本")
    output_format: str = Field(default="ui", description="ui 或 terminal")
    feedback: str | None = Field(default=None, description="可选：答案核对反馈")
    thinking: str | None = Field(default=None, description="可选：disabled/light/max；高难度完整解题建议 light")


class ShowMathExamInput(BaseModel):
    exam_type: str = Field(default="math1", description="考试类型：math1、math2、math3")
    year: int = Field(description="考研数学真题年份")
    question_number: int = Field(description="题号")


class ClarifyMathSymbolInput(BaseModel):
    exam_type: str = Field(default="math1", description="考试类型：math1、math2、math3")
    year: int = Field(description="考研数学真题年份")
    question_number: int = Field(description="题号")
    target: str = Field(description="需要解释的符号或对象，例如 E、alpha")
    user_query: str = Field(default="", description="用户原始追问")


class ExplainMathStepInput(BaseModel):
    exam_type: str = Field(default="math1", description="考试类型：math1、math2、math3")
    year: int = Field(description="考研数学真题年份")
    question_number: int = Field(description="题号")
    user_query: str = Field(description="用户关于某一步的追问")
    previous_context: str = Field(default="", description="可选：上一轮解答或会话上下文")
    output_format: str = Field(default="ui", description="ui 或 terminal")
    thinking: str | None = Field(default=None, description="可选：disabled/light/max")


class RewriteMathAnswerInput(BaseModel):
    user_query: str = Field(description="用户改写要求")
    previous_context: str = Field(description="上一轮回答或会话上下文")
    output_format: str = Field(default="ui", description="ui 或 terminal")


class SummarizeMathSolutionInput(BaseModel):
    user_query: str = Field(description="用户总结要求")
    previous_context: str = Field(description="上一轮回答或会话上下文")
    output_format: str = Field(default="ui", description="ui 或 terminal")


class SolveGeneralMathInput(BaseModel):
    user_query: str = Field(description="用户数学题或问题")
    vl_text: str | None = Field(default=None, description="可选：Qwen-VL 图片识别文本")
    output_format: str = Field(default="ui", description="ui 或 terminal")
    thinking: str | None = Field(default=None, description="可选：disabled/light/max；复杂推导可传 light")


class JudgeMathAnswerInput(BaseModel):
    exam_type: str = Field(default="math1", description="考试类型：math1、math2、math3")
    year: int = Field(description="考研数学真题年份")
    question_number: int = Field(description="题号")
    solution: str = Field(description="模型解答")


class CurrentAffairsInput(BaseModel):
    query: str = Field(description="时政查询或整理请求")


@dataclass
class KaoyanToolkit:
    search_math_exam: Any
    show_math_exam_question: Any
    show_math_exam_answer: Any
    clarify_math_symbol: Any
    explain_math_step: Any
    rewrite_math_answer: Any
    summarize_math_solution: Any
    ocr_math_image: Any
    solve_math_exam: Any
    solve_general_math: Any
    judge_math_answer: Any
    get_current_affairs: Any

    def as_list(self) -> list[Any]:
        return [
            self.search_math_exam,
            self.show_math_exam_question,
            self.show_math_exam_answer,
            self.clarify_math_symbol,
            self.explain_math_step,
            self.rewrite_math_answer,
            self.summarize_math_solution,
            self.ocr_math_image,
            self.solve_math_exam,
            self.solve_general_math,
            self.judge_math_answer,
            self.get_current_affairs,
        ]


def create_kaoyan_toolkit(agent_module: Any) -> KaoyanToolkit:
    """Build LangChain-style tools around the existing project functions."""

    def search_math_exam(year: int, question_number: int, exam_type: str = "math1") -> dict[str, Any]:
        problem = agent_module.load_problem(year, question_number, exam_type)
        return {
            "exam_type": problem.exam_type,
            "year": problem.year,
            "question_number": problem.question_number,
            "question_text": problem.question_text,
            "answer_text": problem.answer_text,
            "question_source": str(problem.question_source),
            "answer_source": str(problem.answer_source) if problem.answer_source else None,
        }

    def ocr_math_image(image_paths: list[str], user_query: str) -> str:
        return agent_module.ocr_images_with_qwenvl([Path(item) for item in image_paths], user_query)

    def show_math_exam_question(year: int, question_number: int, exam_type: str = "math1") -> str:
        problem = agent_module.load_problem(year, question_number, exam_type)
        return agent_module.render_question_for_user(problem)

    def show_math_exam_answer(year: int, question_number: int, exam_type: str = "math1") -> str:
        problem = agent_module.load_problem(year, question_number, exam_type)
        if problem.answer_text:
            return agent_module.render_answer_only(problem.answer_text)
        return "这道题的本地答案速查暂未录入。"

    def clarify_math_symbol(
        year: int,
        question_number: int,
        target: str,
        user_query: str = "",
        exam_type: str = "math1",
    ) -> str:
        problem = agent_module.load_problem(year, question_number, exam_type)
        answer = agent_module.clarify_symbol_from_question(target, problem.question_text)
        if answer:
            return answer
        return agent_module.clarify_symbol_with_qwen(target, problem)

    def explain_math_step(
        year: int,
        question_number: int,
        user_query: str,
        previous_context: str = "",
        output_format: str = "ui",
        exam_type: str = "math1",
        thinking: str | None = None,
    ) -> str:
        problem = agent_module.load_problem(year, question_number, exam_type)
        return agent_module.explain_math_step_with_qwenmath(problem, user_query, previous_context, output_format, thinking)

    def rewrite_math_answer(user_query: str, previous_context: str, output_format: str = "ui") -> str:
        return agent_module.rewrite_math_answer_with_qwen(user_query, previous_context, output_format)

    def summarize_math_solution(user_query: str, previous_context: str, output_format: str = "ui") -> str:
        return agent_module.summarize_math_solution_with_qwen(user_query, previous_context, output_format)

    def solve_math_exam(
        year: int,
        question_number: int,
        user_query: str,
        vl_text: str | None = None,
        output_format: str = "ui",
        feedback: str | None = None,
        exam_type: str = "math1",
        thinking: str | None = None,
    ) -> str:
        problem = agent_module.load_problem(year, question_number, exam_type)
        return agent_module.solve_with_qwenmath(problem, user_query, vl_text, output_format, feedback, thinking)

    def solve_general_math(
        user_query: str,
        vl_text: str | None = None,
        output_format: str = "ui",
        thinking: str | None = None,
    ) -> str:
        return agent_module.solve_general_math_with_qwenmath(user_query, vl_text, output_format, thinking)

    def judge_math_answer(year: int, question_number: int, solution: str, exam_type: str = "math1") -> dict[str, Any]:
        problem = agent_module.load_problem(year, question_number, exam_type)
        return agent_module.judge_answer(problem, solution)

    def get_current_affairs(query: str) -> str:
        return agent_module.call_current_affairs_search(query)

    return KaoyanToolkit(
        search_math_exam=_make_tool(
            name="search_math_exam",
            description="查询考研数学一/二/三历年真题。适用于用户询问某年某卷第几题，返回题干、题图 Markdown 链接和标准答案速查。",
            func=search_math_exam,
            args_schema=SearchMathExamInput,
        ),
        show_math_exam_question=_make_tool(
            name="show_math_exam_question",
            description="展示考研数学一/二/三真题题目，不解题。",
            func=show_math_exam_question,
            args_schema=ShowMathExamInput,
        ),
        show_math_exam_answer=_make_tool(
            name="show_math_exam_answer",
            description="展示考研数学一/二/三真题本地标准答案速查，不解题。",
            func=show_math_exam_answer,
            args_schema=ShowMathExamInput,
        ),
        clarify_math_symbol=_make_tool(
            name="clarify_math_symbol",
            description="解释考研数学真题题干中的符号或对象含义，例如 E、alpha；不重做整题。",
            func=clarify_math_symbol,
            args_schema=ClarifyMathSymbolInput,
        ),
        explain_math_step=_make_tool(
            name="explain_math_step",
            description="解释考研数学真题解答中的某一步或局部结论；只解释局部，不完整重做。",
            func=explain_math_step,
            args_schema=ExplainMathStepInput,
        ),
        rewrite_math_answer=_make_tool(
            name="rewrite_math_answer",
            description="按用户要求改写上一轮数学回答，例如更简洁、口语化、适合笔记；不重新解题。",
            func=rewrite_math_answer,
            args_schema=RewriteMathAnswerInput,
        ),
        summarize_math_solution=_make_tool(
            name="summarize_math_solution",
            description="总结上一轮数学解法或本题思路；不重新解题。",
            func=summarize_math_solution,
            args_schema=SummarizeMathSolutionInput,
        ),
        ocr_math_image=_make_tool(
            name="ocr_math_image",
            description="识别数学题图片，将图片中的文字、公式、选项和图形条件转成文本；可用于用户上传图片和本地题库题图；只做 OCR，不解题。",
            func=ocr_math_image,
            args_schema=OCRMathImageInput,
        ),
        solve_math_exam=_make_tool(
            name="solve_math_exam",
            description="解答考研数学一/二/三真题。输入考试类型、年份、题号、用户问题和可选 OCR 结果，返回解题过程和最终答案。",
            func=solve_math_exam,
            args_schema=SolveMathExamInput,
        ),
        solve_general_math=_make_tool(
            name="solve_general_math",
            description="解答普通数学题或图片 OCR 后的数学题，不查本地真题库。",
            func=solve_general_math,
            args_schema=SolveGeneralMathInput,
        ),
        judge_math_answer=_make_tool(
            name="judge_math_answer",
            description="将考研数学真题的模型解答与资料库标准答案速查进行核心答案核对。",
            func=judge_math_answer,
            args_schema=JudgeMathAnswerInput,
        ),
        get_current_affairs=_make_tool(
            name="get_current_affairs",
            description="调用自研新闻搜索链路，按权威来源检索并整理考研政治时政信息。",
            func=get_current_affairs,
            args_schema=CurrentAffairsInput,
            return_direct=True,
        ),
    )
