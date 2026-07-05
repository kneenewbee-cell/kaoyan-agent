from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parent
YEAR = 1996


def md(text: str) -> str:
    return dedent(text).strip()


@dataclass
class Question:
    number: int
    question_type: str
    score: int
    topics: list[str]
    stem: str
    answer: str
    explanation: str
    assets: list[str]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def qtype_label(qtype: str) -> str:
    return {
        "fill_blank": "填空题",
        "single_choice": "选择题",
        "solution": "解答题",
        "proof": "证明题",
    }[qtype]


def build_card(q: Question) -> str:
    qid = f"kaoyan_math2_{YEAR}_q{q.number:03d}"
    topic_lines = [f"  - {topic}" for topic in q.topics]
    asset_lines = [f"  - {asset}" for asset in q.assets]
    image_lines = [f"![题图](../{asset})" for asset in q.assets]
    lines = [
        "---",
        f"question_id: {qid}",
        f"exam_id: kaoyan_math2_{YEAR}",
        "exam_type: math2",
        f"year: {YEAR}",
        f"question_number: {q.number}",
        f"question_type: {q.question_type}",
        f"score: {q.score}",
        "module: 高等数学",
        "topics:",
        *topic_lines,
        "difficulty: unknown",
        "review_status: reviewed",
        "answer_status: available",
        "explanation_status: available",
        f"source_file: math2_{YEAR}_questions.md",
        f"answer_source_file: math2_{YEAR}_answers.md",
        "assets:",
        *asset_lines,
        "---",
        "",
        f"# {YEAR} 数学二第 {q.number} 题",
        "",
        "## 题目",
        "",
        q.stem,
        "",
        *image_lines,
        "",
        "## 标准答案",
        "",
        q.answer,
        "",
        "## 解析",
        "",
        q.explanation,
        "",
        "## 来源",
        "",
        f"- 题目来源：`math2_{YEAR}_questions.md`",
        f"- 答案来源：`math2_{YEAR}_answers.md`",
        "",
    ]
    return "\n".join(lines)


def annual_questions_md(questions: list[Question]) -> str:
    lines = [
        f"# {YEAR} 年数学二真题",
        "",
        "资料类型：考研数学二历年真题  ",
        f"年份：{YEAR}  ",
        "科目：数学二  ",
        "范围：试卷 III  ",
        "整理状态：已按原卷页面图像校对并转写。",
        "",
    ]
    for q in questions:
        lines.extend(
            [
                f"## 第 {q.number} 题",
                f"- 题型：{qtype_label(q.question_type)}",
                f"- 分值：{q.score}",
                "- 模块：高等数学",
                f"- 考点：{'、'.join(q.topics)}",
                "",
                q.stem,
                "",
            ]
        )
        for asset in q.assets:
            lines.extend([f"![{YEAR} 数学二第 {q.number} 题题图]({asset})", ""])
    return "\n".join(lines).rstrip() + "\n"


def annual_answers_md(questions: list[Question]) -> str:
    lines = [
        f"# Math 2 {YEAR} Answers",
        "",
        "资料类型：考研数学二答案解析",
        f"年份：{YEAR}",
        "科目：数学二",
        "范围：试卷 III",
        "校对状态：已按答案页图像清洗并与题面同步。",
        "",
        "## 答案速查",
        "",
        "| 题号 | 题型 | 答案 |",
        "|---|---|---|",
    ]
    for q in questions:
        lines.append(f"| {q.number} | {qtype_label(q.question_type)} | {q.answer.replace('|', '\\|')} |")
    lines.extend(["", "## 详细解析", ""])
    for q in questions:
        lines.extend([f"### 第 {q.number} 题", "", f"- 答案：{q.answer}", "", q.explanation, ""])
    return "\n".join(lines).rstrip() + "\n"


QUESTIONS = [
    Question(
        1,
        "fill_blank",
        3,
        ["复合函数求导", "链式法则"],
        md(
            """
            设
            $$
            y=\\left(x+e^{-\\frac{x}{2}}\\right)^{\\frac23},
            $$
            则
            $$
            y'\\big|_{x=0}=\\underline{\\qquad}.
            $$
            """
        ),
        "$\\dfrac{1}{3}$",
        md(
            """
            设
            $$
            u=x+e^{-x/2},
            $$
            则
            $$
            y=u^{2/3},\\qquad y'=\\frac23u^{-1/3}u'.
            $$
            当 $x=0$ 时，
            $$
            u(0)=1,\\qquad u'(0)=1-\\frac12e^0=\\frac12.
            $$
            所以
            $$
            y'(0)=\\frac23\\cdot1^{-1/3}\\cdot\\frac12=\\frac13.
            $$
            """
        ),
        ["images/source_pages/page-1.png"],
    ),
    Question(
        2,
        "fill_blank",
        3,
        ["定积分", "奇偶性"],
        md(
            """
            计算
            $$
            \\int_{-1}^{1}\\left(x+\\sqrt{1-x^2}\\right)^2\\,dx=\\underline{\\qquad}.
            $$
            """
        ),
        "$2$",
        md(
            """
            展开被积式：
            $$
            \\left(x+\\sqrt{1-x^2}\\right)^2=x^2+1-x^2+2x\\sqrt{1-x^2}=1+2x\\sqrt{1-x^2}.
            $$
            其中 $2x\\sqrt{1-x^2}$ 是奇函数，在 $[-1,1]$ 上积分为 $0$，故
            $$
            \\int_{-1}^{1}\\left(x+\\sqrt{1-x^2}\\right)^2dx=\\int_{-1}^{1}1\\,dx=2.
            $$
            """
        ),
        ["images/source_pages/page-1.png"],
    ),
    Question(
        3,
        "fill_blank",
        3,
        ["二阶常系数线性方程"],
        md(
            """
            微分方程
            $$
            y''+2y'+5y=0
            $$
            的通解为 $\\underline{\\qquad}$。
            """
        ),
        "$y=e^{-x}(C_1\\cos2x+C_2\\sin2x)$",
        md(
            """
            特征方程为
            $$
            r^2+2r+5=0,
            $$
            解得
            $$
            r=-1\\pm2i.
            $$
            因而通解为
            $$
            y=e^{-x}(C_1\\cos2x+C_2\\sin2x).
            $$
            """
        ),
        ["images/source_pages/page-1.png"],
    ),
    Question(
        4,
        "fill_blank",
        3,
        ["极限", "等价无穷小"],
        md(
            """
            求极限
            $$
            \\lim_{x\\to\\infty}x\\left[\\sin\\ln\\left(1+\\frac{3}{x}\\right)-\\sin\\ln\\left(1+\\frac{1}{x}\\right)\\right]
            =\\underline{\\qquad}.
            $$
            """
        ),
        "$2$",
        md(
            """
            当 $x\\to\\infty$ 时，
            $$
            \\ln\\left(1+\\frac{k}{x}\\right)\\sim\\frac{k}{x},\\qquad
            \\sin t\\sim t.
            $$
            因此
            $$
            \\sin\\ln\\left(1+\\frac{3}{x}\\right)-\\sin\\ln\\left(1+\\frac{1}{x}\\right)
            \\sim \\frac{3}{x}-\\frac{1}{x}=\\frac{2}{x}.
            $$
            故原极限为
            $$
            \\lim_{x\\to\\infty}x\\cdot\\frac{2}{x}=2.
            $$
            """
        ),
        ["images/source_pages/page-1.png"],
    ),
    Question(
        5,
        "fill_blank",
        3,
        ["平面图形面积", "定积分"],
        md(
            """
            由曲线
            $$
            y=x+\\frac1x,
            $$
            直线 $x=2$ 及 $y=2$ 所围图形的面积
            $$
            S=\\underline{\\qquad}.
            $$
            """
        ),
        "$\\ln2-\\dfrac12$",
        md(
            """
            先求曲线与直线 $y=2$ 的交点：
            $$
            x+\\frac1x=2\\iff (x-1)^2=0,
            $$
            所以交点在 $x=1$。在区间 $[1,2]$ 上曲线位于直线 $y=2$ 上方，故
            $$
            S=\\int_1^2\\left(x+\\frac1x-2\\right)dx
            =\\left[\\frac{x^2}{2}+\\ln x-2x\\right]_1^2
            =\\ln2-\\frac12.
            $$
            """
        ),
        ["images/source_pages/page-1.png"],
    ),
    Question(
        6,
        "single_choice",
        3,
        ["泰勒展开", "高阶无穷小"],
        md(
            """
            设当 $x\\to0$ 时，
            $$
            e^x-(ax^2+bx+1)
            $$
            是比 $x^2$ 高阶的无穷小，则（ ）。

            A. $a=\\dfrac12,b=1$

            B. $a=1,b=1$

            C. $a=-\\dfrac12,b=-1$

            D. $a=-1,b=1$
            """
        ),
        "A",
        md(
            """
            由
            $$
            e^x=1+x+\\frac{x^2}{2}+o(x^2),
            $$
            得
            $$
            e^x-(ax^2+bx+1)=(1-b)x+\\left(\\frac12-a\\right)x^2+o(x^2).
            $$
            因为它是比 $x^2$ 高阶的无穷小，所以一次项和二次项系数都应为 $0$，即
            $$
            1-b=0,\\qquad \\frac12-a=0.
            $$
            故
            $$
            a=\\frac12,\\qquad b=1.
            $$
            选 A。
            """
        ),
        ["images/source_pages/page-1.png"],
    ),
    Question(
        7,
        "single_choice",
        3,
        ["可导定义", "夹逼准则"],
        md(
            """
            设函数 $f(x)$ 在区间 $(-\\delta,\\delta)$ 内有定义，若当 $x\\in(-\\delta,\\delta)$ 时，恒有
            $$
            |f(x)|\\le x^2,
            $$
            则 $x=0$ 必是 $f(x)$ 的（ ）。

            A. 间断点

            B. 连续而不可导的点

            C. 可导的点，且 $f'(0)=0$

            D. 可导的点，且 $f'(0)\\ne0$
            """
        ),
        "C",
        md(
            """
            由 $|f(x)|\\le x^2$，令 $x=0$ 可得 $f(0)=0$。于是
            $$
            \\left|\\frac{f(x)-f(0)}{x}\\right|=\\left|\\frac{f(x)}{x}\\right|\\le |x|\\to0\\quad(x\\to0).
            $$
            因而极限存在且等于 $0$，即
            $$
            f'(0)=\\lim_{x\\to0}\\frac{f(x)-f(0)}{x}=0.
            $$
            所以 $x=0$ 是可导点，且 $f'(0)=0$，选 C。
            """
        ),
        ["images/source_pages/page-1.png"],
    ),
    Question(
        8,
        "single_choice",
        3,
        ["导数与极限", "拉格朗日中值定理"],
        md(
            """
            设 $f(x)$ 处处可导，则（ ）。

            A. 当 $\\lim\\limits_{x\\to-\\infty}f(x)=-\\infty$ 时，必有 $\\lim\\limits_{x\\to-\\infty}f'(x)=-\\infty$

            B. 当 $\\lim\\limits_{x\\to-\\infty}f'(x)=-\\infty$ 时，必有 $\\lim\\limits_{x\\to-\\infty}f(x)=-\\infty$

            C. 当 $\\lim\\limits_{x\\to+\\infty}f(x)=+\\infty$ 时，必有 $\\lim\\limits_{x\\to+\\infty}f'(x)=+\\infty$

            D. 当 $\\lim\\limits_{x\\to+\\infty}f'(x)=+\\infty$ 时，必有 $\\lim\\limits_{x\\to+\\infty}f(x)=+\\infty$
            """
        ),
        "D",
        md(
            """
            A、B、C 都可由反例排除，例如取 $f(x)=x$ 或 $f(x)=e^{-x}$ 等即可。

            对 D，若 $\\lim\\limits_{x\\to+\\infty}f'(x)=+\\infty$，则存在 $X$，当 $x>X$ 时有 $f'(x)>1$。对任意 $x>X$，由拉格朗日中值定理，
            $$
            f(x)-f(X)=f'(\\xi)(x-X)>x-X\\qquad (\\xi\\in(X,x)).
            $$
            因而
            $$
            f(x)>f(X)+x-X\\to+\\infty.
            $$
            所以 D 正确。
            """
        ),
        ["images/source_pages/page-1.png"],
    ),
    Question(
        9,
        "single_choice",
        3,
        ["方程根的个数", "单调性"],
        md(
            """
            在区间 $(-\\infty,+\\infty)$ 内，方程
            $$
            |x|^{\\frac14}+|x|^{\\frac12}-\\cos x=0
            $$
            （ ）。

            A. 无实根

            B. 有且仅有一个实根

            C. 有且仅有两个实根

            D. 有无穷多个实根
            """
        ),
        "C",
        md(
            """
            令
            $$
            F(x)=|x|^{1/4}+|x|^{1/2}-\\cos x.
            $$
            这是偶函数，所以其零点关于原点对称。只需考察 $x\\ge0$。

            当 $x=0$ 时，$F(0)=-1<0$；当 $x=\\dfrac{\\pi}{2}$ 时，
            $$
            F\\left(\\frac\\pi2\\right)=\\left(\\frac\\pi2\\right)^{1/4}+\\left(\\frac\\pi2\\right)^{1/2}>0.
            $$
            故在 $(0,\\pi/2)$ 内至少有一个零点。

            对 $x>0$，
            $$
            F'(x)=\\frac{1}{4x^{3/4}}+\\frac{1}{2x^{1/2}}+\\sin x>0
            $$
            在 $(0,\\pi/2)$ 上成立，所以该区间内零点唯一。又当 $x\\ge\\pi/2$ 时，$\\cos x\\le0$，而前两项非负，故不再有正根。

            因为 $F$ 为偶函数，所以总共有两个实根。选 C。
            """
        ),
        ["images/source_pages/page-1.png"],
    ),
    Question(
        10,
        "single_choice",
        3,
        ["旋转体体积", "定积分"],
        md(
            """
            设 $f(x),g(x)$ 在区间 $[a,b]$ 上连续，且 $g(x)<f(x)<m$（$m$ 为常数），由曲线 $y=g(x)$，$y=f(x)$，$x=a$ 及 $x=b$ 所围平面图形绕直线 $y=m$ 旋转而成的旋转体体积为（ ）。

            A. $\\displaystyle\\int_a^b\\pi[2m-f(x)+g(x)][f(x)-g(x)]dx$

            B. $\\displaystyle\\int_a^b\\pi[2m-f(x)-g(x)][f(x)-g(x)]dx$

            C. $\\displaystyle\\int_a^b\\pi[m-f(x)+g(x)][f(x)-g(x)]dx$

            D. $\\displaystyle\\int_a^b\\pi[m-f(x)-g(x)][f(x)-g(x)]dx$
            """
        ),
        "B",
        md(
            """
            绕直线 $y=m$ 旋转时，外半径为 $m-g(x)$，内半径为 $m-f(x)$。由垫片法，
            $$
            V=\\int_a^b\\pi\\Big[(m-g(x))^2-(m-f(x))^2\\Big]dx.
            $$
            展开得
            $$
            (m-g)^2-(m-f)^2=(f-g)(2m-f-g),
            $$
            所以
            $$
            V=\\int_a^b\\pi[2m-f(x)-g(x)][f(x)-g(x)]dx.
            $$
            选 B。
            """
        ),
        ["images/source_pages/page-1.png"],
    ),
    Question(
        11,
        "solution",
        5,
        ["定积分", "换元积分"],
        md(
            """
            计算
            $$
            \\int_0^{\\ln2}\\sqrt{1-e^{-2x}}\\,dx.
            $$
            """
        ),
        "$\\ln(2+\\sqrt3)-\\dfrac{\\sqrt3}{2}$",
        md(
            """
            令
            $$
            e^{-x}=\\cos t,
            $$
            则
            $$
            e^{-2x}=\\cos^2 t,\\qquad \\sqrt{1-e^{-2x}}=\\sin t.
            $$
            由
            $$
            -e^{-x}dx=-\\sin t\\,dt
            $$
            得
            $$
            dx=\\tan t\\,dt.
            $$
            当 $x=0$ 时，$t=0$；当 $x=\\ln2$ 时，$e^{-x}=\\dfrac12$，故 $t=\\dfrac\\pi3$。于是
            $$
            \\int_0^{\\ln2}\\sqrt{1-e^{-2x}}\\,dx
            =\\int_0^{\\pi/3}\\sin t\\tan t\\,dt
            =\\int_0^{\\pi/3}\\left(\\sec t-\\cos t\\right)dt.
            $$
            因而
            $$
            \\int_0^{\\ln2}\\sqrt{1-e^{-2x}}\\,dx
            =\\left[\\ln(\\sec t+\\tan t)-\\sin t\\right]_0^{\\pi/3}
            =\\ln(2+\\sqrt3)-\\frac{\\sqrt3}{2}.
            $$
            """
        ),
        ["images/source_pages/page-2.png"],
    ),
    Question(
        12,
        "solution",
        5,
        ["不定积分", "三角恒等变形"],
        md(
            """
            求
            $$
            \\int\\frac{dx}{1+\\sin x}.
            $$
            """
        ),
        "$\\tan x-\\sec x+C$",
        md(
            """
            将分母有理化：
            $$
            \\int\\frac{dx}{1+\\sin x}
            =\\int\\frac{1-\\sin x}{(1+\\sin x)(1-\\sin x)}dx
            =\\int\\frac{1-\\sin x}{\\cos^2x}dx.
            $$
            因而
            $$
            \\int\\frac{dx}{1+\\sin x}
            =\\int\\sec^2x\\,dx-\\int\\frac{\\sin x}{\\cos^2x}dx
            =\\tan x-\\sec x+C.
            $$
            """
        ),
        ["images/source_pages/page-2.png"],
    ),
    Question(
        13,
        "solution",
        5,
        ["参数方程", "二阶导数"],
        md(
            """
            设
            $$
            \\begin{cases}
            x=\\int_0^t f(u^2)\\,du,\\\\
            y=[f(t^2)]^2,
            \\end{cases}
            $$
            其中 $f(u)$ 具有二阶导数，且 $f(u)\\ne0$，求 $\\dfrac{d^2y}{dx^2}$。
            """
        ),
        "$\\dfrac{4}{f(t^2)}\\left[f'(t^2)+2t^2f''(t^2)\\right]$",
        md(
            """
            这是由参数方程所确定的函数，其导数为
            $$
            \\frac{dy}{dx}=\\frac{dy/dt}{dx/dt}
            =\\frac{2f(t^2)\\cdot f'(t^2)\\cdot2t}{f(t^2)}
            =4t f'(t^2).
            $$
            所以
            $$
            \\frac{d^2y}{dx^2}
            =\\frac{d}{dt}\\left(\\frac{dy}{dx}\\right)\\cdot\\frac{dt}{dx}
            =\\frac{d}{dt}\\bigl(4tf'(t^2)\\bigr)\\cdot\\frac{1}{f(t^2)}.
            $$
            计算得
            $$
            \\frac{d}{dt}\\bigl(4tf'(t^2)\\bigr)=4f'(t^2)+8t^2f''(t^2),
            $$
            故
            $$
            \\frac{d^2y}{dx^2}
            =\\frac{4}{f(t^2)}\\left[f'(t^2)+2t^2f''(t^2)\\right].
            $$
            """
        ),
        ["images/source_pages/page-2.png"],
    ),
    Question(
        14,
        "solution",
        5,
        ["泰勒公式", "拉格朗日余项"],
        md(
            """
            求函数
            $$
            f(x)=\\frac{1-x}{1+x}
            $$
            在点 $x=0$ 处带拉格朗日型余项的 $n$ 阶泰勒展开式。
            """
        ),
        "$\\dfrac{1-x}{1+x}=1-2x+2x^2+\\cdots+(-1)^n2x^n+(-1)^{n+1}\\dfrac{2x^{n+1}}{(1+\\theta x)^{n+2}}\\ (0<\\theta<1)$",
        md(
            """
            对于函数
            $$
            f(x)=\\frac{1-x}{1+x}=\\frac{2}{1+x}-1,
            $$
            有
            $$
            f^{(n)}(x)=2(-1)^n n!(1+x)^{-(n+1)}\\qquad (n\\ge1),
            $$
            因而
            $$
            f^{(n)}(0)=2(-1)^n n!.
            $$
            由带拉格朗日余项的泰勒公式，
            $$
            f(x)=f(0)+f'(0)x+\\cdots+\\frac{f^{(n)}(0)}{n!}x^n+\\frac{f^{(n+1)}(\\theta x)}{(n+1)!}x^{n+1},
            \\qquad 0<\\theta<1.
            $$
            代入各阶导数得
            $$
            \\frac{1-x}{1+x}
            =1-2x+2x^2+\\cdots+(-1)^n2x^n+(-1)^{n+1}\\frac{2x^{n+1}}{(1+\\theta x)^{n+2}},
            \\qquad 0<\\theta<1.
            $$
            """
        ),
        ["images/source_pages/page-2.png"],
    ),
    Question(
        15,
        "solution",
        5,
        ["二阶线性方程", "待定系数法"],
        md(
            """
            求微分方程
            $$
            y''+y'=x^2
            $$
            的通解。
            """
        ),
        "$y=c_1+c_2e^{-x}+\\dfrac{x^3}{3}-x^2+2x$",
        md(
            """
            对应齐次方程
            $$
            y''+y'=0
            $$
            的特征方程为
            $$
            r^2+r=0,
            $$
            故齐次通解为
            $$
            y_h=c_1+c_2e^{-x}.
            $$
            设非齐次方程的一个特解为
            $$
            y_p=x(ax^2+bx+c),
            $$
            代入原方程比较系数，可得
            $$
            a=\\frac13,\\qquad b=-1,\\qquad c=2.
            $$
            因而
            $$
            y_p=\\frac{x^3}{3}-x^2+2x.
            $$
            所以通解为
            $$
            y=c_1+c_2e^{-x}+\\frac{x^3}{3}-x^2+2x.
            $$
            """
        ),
        ["images/source_pages/page-2.png"],
    ),
    Question(
        16,
        "solution",
        5,
        ["截面法", "体积计算"],
        md(
            """
            设有一正椭圆柱体，其底面的长、短轴分别为 $2a,2b$，用过此柱体底面的短轴且与底面成 $\\alpha$ 角（$0<\\alpha<\\dfrac\\pi2$）的平面截此柱体，得一楔形体（如图），求此楔形体的体积 $V$。
            """
        ),
        "$V=\\dfrac{2}{3}a^2b\\tan\\alpha$",
        md(
            """
            建立坐标系，底面椭圆方程为
            $$
            \\frac{x^2}{a^2}+\\frac{y^2}{b^2}=1.
            $$
            取垂直于 $y$ 轴的平面去截该楔形体，所得截面是直角三角形。其中一条直角边长为
            $$
            x=\\frac{a}{b}\\sqrt{b^2-y^2},
            $$
            另一条直角边长为
            $$
            x\\tan\\alpha=\\frac{a}{b}\\sqrt{b^2-y^2}\\tan\\alpha.
            $$
            所以截面面积为
            $$
            S(y)=\\frac12\\cdot\\frac{a^2}{b^2}(b^2-y^2)\\tan\\alpha.
            $$
            由对称性，
            $$
            V=2\\int_0^b S(y)dy
            =\\frac{a^2}{b^2}\\tan\\alpha\\int_0^b(b^2-y^2)dy
            =\\frac{2}{3}a^2b\\tan\\alpha.
            $$
            """
        ),
        ["images/q016_diagram.png"],
    ),
    Question(
        17,
        "solution",
        8,
        ["不定积分", "分部积分"],
        md(
            """
            计算不定积分
            $$
            \\int\\frac{\\arctan x}{x^2(1+x^2)}\\,dx.
            $$
            """
        ),
        "$-\\dfrac{1}{x}\\arctan x+\\ln|x|-\\dfrac12\\ln(1+x^2)-\\dfrac12\\arctan^2x+C$",
        md(
            """
            将原式拆为
            $$
            \\int\\frac{\\arctan x}{x^2(1+x^2)}dx
            =\\int\\frac{\\arctan x}{x^2}dx-\\int\\frac{\\arctan x}{1+x^2}dx.
            $$
            对第一项作分部积分：
            $$
            u=\\arctan x,\\quad dv=\\frac{dx}{x^2},
            $$
            则
            $$
            du=\\frac{dx}{1+x^2},\\quad v=-\\frac1x.
            $$
            所以
            $$
            \\int\\frac{\\arctan x}{x^2}dx
            =-\\frac{\\arctan x}{x}+\\int\\frac{dx}{x(1+x^2)}.
            $$
            又
            $$
            \\int\\frac{dx}{x(1+x^2)}
            =\\int\\left(\\frac1x-\\frac{x}{1+x^2}\\right)dx
            =\\ln|x|-\\frac12\\ln(1+x^2).
            $$
            第二项令 $t=\\arctan x$，则
            $$
            \\int\\frac{\\arctan x}{1+x^2}dx=\\frac12\\arctan^2x.
            $$
            因而
            $$
            \\int\\frac{\\arctan x}{x^2(1+x^2)}dx
            =-\\frac{1}{x}\\arctan x+\\ln|x|-\\frac12\\ln(1+x^2)-\\frac12\\arctan^2x+C.
            $$
            """
        ),
        ["images/source_pages/page-2.png"],
    ),
    Question(
        18,
        "solution",
        8,
        ["反函数", "连续与可导"],
        md(
            """
            设函数
            $$
            f(x)=
            \\begin{cases}
            1-2x^2, & x<-1,\\\\
            x^3, & -1\\le x\\le2,\\\\
            12x-16, & x>2,
            \\end{cases}
            $$
            (1) 写出 $f(x)$ 的反函数 $g(x)$ 的表达式；

            (2) $g(x)$ 是否有间断点、不可导点，若有，指出这些点。
            """
        ),
        "$g(x)=\\begin{cases}-\\sqrt{\\dfrac{1-x}{2}},&x<-1,\\\\ \\sqrt[3]{x},&-1\\le x\\le8,\\\\ \\dfrac{x+16}{12},&x>8,\\end{cases}$；$g(x)$ 无间断点，在 $x=-1,0$ 处不可导",
        md(
            """
            由各分段单调性可知 $f(x)$ 在 $(-\\infty,+\\infty)$ 上单调递增且连续，因此存在反函数。三段分别求反解得
            $$
            g(x)=
            \\begin{cases}
            -\\sqrt{\\dfrac{1-x}{2}}, & x<-1,\\\\
            \\sqrt[3]{x}, & -1\\le x\\le8,\\\\
            \\dfrac{x+16}{12}, & x>8.
            \\end{cases}
            $$

            因为三段在拼接点处满足
            $$
            g(-1^-)=g(-1^+)=-1,\\qquad g(8^-)=g(8^+)=2,
            $$
            所以 $g(x)$ 在全体实数上连续，没有间断点。

            再考察可导性：$\\sqrt[3]{x}$ 在 $x=0$ 处不可导；在 $x=-1$ 处，
            $$
            g'_-( -1 )=\\frac14,\\qquad g'_+( -1 )=\\frac13,
            $$
            左右导数不相等，故也不可导。至于 $x=8$，左右导数都等于 $\\dfrac{1}{12}$，故可导。

            因此，$g(x)$ 无间断点，仅在 $x=-1,0$ 两点不可导。
            """
        ),
        ["images/source_pages/page-2.png"],
    ),
    Question(
        19,
        "solution",
        8,
        ["隐函数求导", "极值判别"],
        md(
            """
            设函数 $y=y(x)$ 由方程
            $$
            2y^3-2y^2+2xy-x^2=1
            $$
            所确定，试求 $y=y(x)$ 的驻点，并判别它是否为极值点。
            """
        ),
        "$(1,1)$；且在该点取极小值",
        md(
            """
            对方程两边关于 $x$ 求导，得
            $$
            6y^2y'-4yy'+2xy'+2y-2x=0,
            $$
            即
            $$
            (3y^2-2y+x)y'+y-x=0.
            $$
            因而
            $$
            y'=\\frac{x-y}{3y^2-2y+x}.
            $$
            驻点满足 $y'=0$，于是 $x=y$。代回原方程：
            $$
            2x^3-x^2-1=0=(x-1)(2x^2+x+1).
            $$
            只有实根 $x=1$，故唯一驻点为
            $$
            (x,y)=(1,1).
            $$

            再对导数关系求导，或直接利用隐函数二阶导数公式，在点 $(1,1)$ 处代入 $y'=0$ 可得
            $$
            2y''-1=0,
            $$
            即
            $$
            y''\\big|_{x=1}=\\frac12>0.
            $$
            所以点 $(1,1)$ 是极小值点。
            """
        ),
        ["images/source_pages/page-2.png"],
    ),
    Question(
        20,
        "proof",
        8,
        ["零点定理", "罗尔定理"],
        md(
            """
            设 $f(x)$ 在区间 $[a,b]$ 上具有二阶导数，且 $f(a)=f(b)=0$，$f'(a)f'(b)>0$。证明：存在 $\\xi\\in(a,b)$ 和 $\\eta\\in(a,b)$，使 $f(\\xi)=0$ 及 $f''(\\eta)=0$。
            """
        ),
        "见解析",
        md(
            """
            先证存在 $\\xi\\in(a,b)$，使 $f(\\xi)=0$。

            不妨设 $f'(a)>0,f'(b)>0$（若同为负，论证完全类似）。由导数定义与局部保号性，可知在 $a$ 的某个右邻域内有 $f(x)>0$；同理，在 $b$ 的某个左邻域内有 $f(x)<0$。于是存在
            $$
            x_1,x_2\\in(a,b),\\qquad x_1<x_2,
            $$
            使得
            $$
            f(x_1)>0,\\qquad f(x_2)<0.
            $$
            由零点定理，存在
            $$
            \\xi\\in(x_1,x_2)\\subset(a,b)
            $$
            使
            $$
            f(\\xi)=0.
            $$

            再证存在 $\\eta\\in(a,b)$，使 $f''(\\eta)=0$。由于
            $$
            f(a)=f(\\xi)=f(b)=0,
            $$
            根据罗尔定理，在区间 $(a,\\xi)$ 与 $(\\xi,b)$ 内分别存在
            $$
            \\eta_1\\in(a,\\xi),\\qquad \\eta_2\\in(\\xi,b)
            $$
            使
            $$
            f'(\\eta_1)=0,\\qquad f'(\\eta_2)=0.
            $$
            再对函数 $f'(x)$ 在区间 $[\\eta_1,\\eta_2]$ 上应用罗尔定理，得存在
            $$
            \\eta\\in(\\eta_1,\\eta_2)\\subset(a,b)
            $$
            使
            $$
            f''(\\eta)=0.
            $$
            结论得证。
            """
        ),
        ["images/source_pages/page-2.png"],
    ),
    Question(
        21,
        "solution",
        8,
        ["一阶线性方程", "积分估计"],
        md(
            """
            设 $f(x)$ 为连续函数，
            $$
            \\begin{cases}
            y'+ay=f(x),\\\\
            y\\big|_{x=0}=0,
            \\end{cases}
            $$
            其中 $a$ 是正常数；

            (1) 求初值问题的解 $y(x)$；

            (2) 若 $|f(x)|\\le k$（$k$ 为常数），证明：当 $x\\ge0$ 时，有
            $$
            |y(x)|\\le\\frac{k}{a}(1-e^{-ax}).
            $$
            """
        ),
        "$y(x)=e^{-ax}\\int_0^x e^{at}f(t)\\,dt$，且当 $x\\ge0$ 时 $|y(x)|\\le\\dfrac{k}{a}(1-e^{-ax})$",
        md(
            """
            这是一个一阶线性非齐次微分方程。由通解公式，
            $$
            y(x)=e^{-ax}\\left[\\int f(x)e^{ax}dx+C\\right].
            $$
            设 $F(x)$ 是 $f(x)e^{ax}$ 的一个原函数，则
            $$
            y(x)=e^{-ax}[F(x)+C].
            $$
            由初值条件 $y(0)=0$ 得
            $$
            C=-F(0).
            $$
            因而
            $$
            y(x)=e^{-ax}[F(x)-F(0)]
            =e^{-ax}\\int_0^x e^{at}f(t)dt.
            $$

            当 $x\\ge0$ 且 $|f(x)|\\le k$ 时，
            $$
            |y(x)|
            =e^{-ax}\\left|\\int_0^x e^{at}f(t)dt\\right|
            \\le e^{-ax}\\int_0^x e^{at}|f(t)|dt
            \\le ke^{-ax}\\int_0^x e^{at}dt.
            $$
            计算可得
            $$
            |y(x)|\\le ke^{-ax}\\cdot\\frac{e^{ax}-1}{a}
            =\\frac{k}{a}(1-e^{-ax}).
            $$
            证毕。
            """
        ),
        ["images/source_pages/page-2.png"],
    ),
]


def main() -> None:
    (ROOT / "questions").mkdir(parents=True, exist_ok=True)
    rows = []
    qids = []
    for q in QUESTIONS:
        qid = f"kaoyan_math2_{YEAR}_q{q.number:03d}"
        qids.append(qid)
        card_rel = f"questions/q{q.number:03d}.md"
        (ROOT / card_rel).write_text(build_card(q), encoding="utf-8", newline="\n")
        rows.append(
            {
                "question_id": qid,
                "exam_id": f"kaoyan_math2_{YEAR}",
                "exam_type": "math2",
                "year": YEAR,
                "question_number": q.number,
                "question_type": q.question_type,
                "score": q.score,
                "module": "高等数学",
                "topics": q.topics,
                "difficulty": "unknown",
                "review_status": "reviewed",
                "answer_status": "available",
                "explanation_status": "available",
                "source_file": f"math2_{YEAR}_questions.md",
                "answer_source_file": f"math2_{YEAR}_answers.md",
                "card_path": card_rel,
                "assets": q.assets,
                "answer": q.answer,
                "explanation": q.explanation,
            }
        )

    (ROOT / f"math2_{YEAR}_questions.md").write_text(
        annual_questions_md(QUESTIONS), encoding="utf-8", newline="\n"
    )
    (ROOT / f"math2_{YEAR}_answers.md").write_text(
        annual_answers_md(QUESTIONS), encoding="utf-8", newline="\n"
    )
    with (ROOT / "questions.jsonl").open("w", encoding="utf-8", newline="\n") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    manifest = {
        "exam_id": f"kaoyan_math2_{YEAR}",
        "exam_type": "math2",
        "exam_label": "数学二",
        "year": YEAR,
        "source_files": {
            "questions": f"math2_{YEAR}_questions.md",
            "answers": f"math2_{YEAR}_answers.md",
        },
        "card_dir": "questions",
        "index_file": "questions.jsonl",
        "question_count": len(QUESTIONS),
        "explanation_count": len(QUESTIONS),
        "question_ids": qids,
        "generated_at": now_iso(),
        "paper_scope": "试卷 III only",
        "review_status": "reviewed",
        "answer_status": "available",
        "explanation_status": "available",
    }
    (ROOT / "paper_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


if __name__ == "__main__":
    main()
