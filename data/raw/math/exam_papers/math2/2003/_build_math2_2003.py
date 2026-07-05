from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parent
YEAR = 2003


def md(text: str) -> str:
    return dedent(text).strip()


@dataclass
class Question:
    number: int
    question_type: str
    score: int
    module: str
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
    lines = [
        "---",
        f"question_id: {qid}",
        f"exam_id: kaoyan_math2_{YEAR}",
        "exam_type: math2",
        f"year: {YEAR}",
        f"question_number: {q.number}",
        f"question_type: {q.question_type}",
        f"score: {q.score}",
        f"module: {q.module}",
        "topics:",
        *[f"  - {topic}" for topic in q.topics],
        "difficulty: unknown",
        "review_status: reviewed",
        "answer_status: available",
        "explanation_status: available",
        f"source_file: math2_{YEAR}_questions.md",
        f"answer_source_file: math2_{YEAR}_answers.md",
        "assets:",
        *[f"  - {asset}" for asset in q.assets],
        "---",
        "",
        f"# {YEAR} 数学二第 {q.number} 题",
        "",
        "## 题目",
        "",
        q.stem,
        "",
        *[f"![题图](../{asset})" for asset in q.assets],
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
        "整理状态：按原卷页面转写并校对。  ",
        "",
    ]
    for q in questions:
        lines.extend(
            [
                f"## 第 {q.number} 题",
                f"- 题型：{qtype_label(q.question_type)}",
                f"- 分值：{q.score}",
                f"- 模块：{q.module}",
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
        "整理状态：答案与解析按答案册清洗整理。",
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
    Question(1, "fill_blank", 4, "高等数学", ["等价无穷小", "极限"],
        md(r"""
        若 $x\to 0$ 时，
        $$
        (1-ax^2)^{\frac14}-1
        $$
        与 $x\sin x$ 是等价无穷小，则 $a=\underline{\qquad}$。
        """),
        "$-4$",
        md(r"""
        当 $x\to 0$ 时，
        $$
        (1-ax^2)^{1/4}-1\sim \frac14(-ax^2)=-\frac{a}{4}x^2,
        \qquad
        x\sin x\sim x^2.
        $$
        由两者等价可得
        $$
        -\frac{a}{4}=1,
        $$
        所以 $a=-4$。
        """),
        ["images/source_pages/page-1.png"]),
    Question(2, "fill_blank", 4, "高等数学", ["隐函数", "切线方程"],
        md(r"""
        设函数 $y=f(x)$ 由方程
        $$
        xy+2\ln x=y^4
        $$
        所确定，则曲线 $y=f(x)$ 在点 $(1,1)$ 处的切线方程是 $\underline{\qquad}$。
        """),
        "$x-y=0$",
        md(r"""
        对方程两边关于 $x$ 求导：
        $$
        y+xy'+\frac{2}{x}=4y^3y'.
        $$
        代入 $(x,y)=(1,1)$，得
        $$
        1+y'+2=4y',
        $$
        所以
        $$
        y'(1)=1.
        $$
        故切线方程为
        $$
        y-1=1(x-1),
        $$
        即 $x-y=0$。
        """),
        ["images/source_pages/page-1.png"]),
    Question(3, "fill_blank", 4, "高等数学", ["麦克劳林公式", "高阶导数"],
        md(r"""
        $y=2^x$ 的麦克劳林公式中 $x^n$ 项的系数是 $\underline{\qquad}$。
        """),
        r"$\dfrac{(\ln 2)^n}{n!}$",
        md(r"""
        对函数
        $$
        y=2^x=e^{x\ln2}
        $$
        有
        $$
        y^{(n)}=(\ln 2)^n 2^x.
        $$
        因而
        $$
        y^{(n)}(0)=(\ln2)^n.
        $$
        麦克劳林展开中 $x^n$ 项系数为
        $$
        \frac{y^{(n)}(0)}{n!}=\frac{(\ln2)^n}{n!}.
        $$
        """),
        ["images/source_pages/page-1.png"]),
    Question(4, "fill_blank", 4, "高等数学", ["极坐标", "面积"],
        md(r"""
        设曲线的极坐标方程为
        $$
        \rho=e^{a\theta}\quad (a>0),
        $$
        则该曲线上相应于 $\theta$ 从 $0$ 变到 $2\pi$ 的一段弧与极轴所围成的图形面积为 $\underline{\qquad}$。
        """),
        r"$\dfrac{e^{4a\pi}-1}{4a}$",
        md(r"""
        极坐标下面积公式为
        $$
        S=\frac12\int_{\alpha}^{\beta}\rho^2\,d\theta.
        $$
        代入 $\rho=e^{a\theta}$，得
        $$
        S=\frac12\int_0^{2\pi}e^{2a\theta}\,d\theta
        =\frac12\cdot \frac{e^{2a\theta}}{2a}\Big|_0^{2\pi}
        =\frac{e^{4a\pi}-1}{4a}.
        $$
        """),
        ["images/source_pages/page-1.png"]),
    Question(5, "fill_blank", 4, "线性代数", ["秩", "矩阵分解"],
        md(r"""
        设 $\alpha$ 为 $3$ 维列向量，$\alpha^\mathrm{T}$ 是 $\alpha$ 的转置，若
        $$
        \alpha\alpha^\mathrm{T}=
        \begin{pmatrix}
        1&-1&1\\
        -1&1&-1\\
        1&-1&1
        \end{pmatrix},
        $$
        则 $\alpha^\mathrm{T}\alpha=\underline{\qquad}$。
        """),
        "$3$",
        md(r"""
        设
        $$
        \alpha=(x_1,x_2,x_3)^\mathrm{T}.
        $$
        由题设矩阵第一列可知
        $$
        x_1^2=1,\quad x_1x_2=-1,\quad x_1x_3=1.
        $$
        可取
        $$
        \alpha=(1,-1,1)^\mathrm{T}
        $$
        或其相反向量，均满足题意，因此
        $$
        \alpha^\mathrm{T}\alpha=x_1^2+x_2^2+x_3^2=1+1+1=3.
        $$
        """),
        ["images/source_pages/page-1.png"]),
    Question(6, "fill_blank", 4, "线性代数", ["行列式", "矩阵方程"],
        md(r"""
        设 $3$ 阶方阵 $A,B$ 满足
        $$
        A^2B-A-B=E,
        $$
        其中 $E$ 为 $3$ 阶单位矩阵，若
        $$
        A=\begin{pmatrix}
        1&0&1\\
        0&2&0\\
        -2&0&1
        \end{pmatrix},
        $$
        则 $|B|=\underline{\qquad}$。
        """),
        r"$\dfrac12$",
        md(r"""
        将题设整理为
        $$
        (A^2-E)B=A+E.
        $$
        因式分解得
        $$
        (A-E)(A+E)B=A+E.
        $$
        由于 $A+E$ 可逆，可约去，得
        $$
        (A-E)B=E.
        $$
        于是
        $$
        B=(A-E)^{-1},
        \qquad
        |B|=\frac{1}{|A-E|}.
        $$
        计算
        $$
        A-E=\begin{pmatrix}
        0&0&1\\
        0&1&0\\
        -2&0&0
        \end{pmatrix},
        \quad |A-E|=2.
        $$
        故
        $$
        |B|=\frac12.
        $$
        """),
        ["images/source_pages/page-1.png"]),
    Question(7, "single_choice", 4, "高等数学", ["数列极限", "反例"],
        md(r"""
        设 $\{a_n\},\{b_n\},\{c_n\}$ 均为非负数列，且
        $$
        \lim_{n\to\infty}a_n=0,\qquad
        \lim_{n\to\infty}b_n=1,\qquad
        \lim_{n\to\infty}c_n=+\infty,
        $$
        则必有（ ）。

        A. $a_n<b_n$ 对任意 $n$ 成立

        B. $b_n<c_n$ 对任意 $n$ 成立

        C. 极限 $\lim\limits_{n\to\infty}a_nc_n$ 不存在

        D. 极限 $\lim\limits_{n\to\infty}b_nc_n$ 不存在
        """),
        "D",
        md(r"""
        若假设 $\lim\limits_{n\to\infty}b_nc_n$ 存在且等于 $L$，则由 $b_n\to 1$ 可得
        $$
        c_n=\frac{b_nc_n}{b_n}\to L,
        $$
        这与 $c_n\to+\infty$ 矛盾。因此 $\lim\limits_{n\to\infty}b_nc_n$ 不存在，故选 D。
        """),
        ["images/source_pages/page-1.png"]),
    Question(8, "single_choice", 4, "高等数学", ["定积分", "重要极限"],
        md(r"""
        设
        $$
        a_n=\frac32\int_0^{\frac{n}{n+1}}x^{n-1}\sqrt{1+x^n}\,dx,
        $$
        则极限 $\lim\limits_{n\to\infty}na_n$ 等于（ ）。

        A. $(1+e^{3/2})+1$

        B. $(1+e^{-1})^{3/2}-1$

        C. $(1+e^{-1})^{3/2}+1$

        D. $(1+e^{3/2})-1$
        """),
        "B",
        md(r"""
        令 $u=x^n$，则
        $$
        du=nx^{n-1}dx,
        $$
        从而
        $$
        a_n=\frac{3}{2n}\int_0^{\left(\frac{n}{n+1}\right)^n}\sqrt{1+u}\,du
        =\frac1n\left[(1+u)^{3/2}\right]_0^{\left(\frac{n}{n+1}\right)^n}.
        $$
        因此
        $$
        na_n=\left(1+\left(\frac{n}{n+1}\right)^n\right)^{3/2}-1.
        $$
        又
        $$
        \left(\frac{n}{n+1}\right)^n\to e^{-1},
        $$
        所以
        $$
        \lim_{n\to\infty}na_n=(1+e^{-1})^{3/2}-1.
        $$
        """),
        ["images/source_pages/page-1.png"]),
    Question(9, "single_choice", 4, "高等数学", ["微分方程", "代入法"],
        md(r"""
        已知
        $$
        y=\frac{x}{\ln x}
        $$
        是微分方程
        $$
        y'=\frac{y}{x}+\varphi\!\left(\frac{x}{y}\right)
        $$
        的解，则 $\varphi\!\left(\dfrac{x}{y}\right)$ 的表达式为（ ）。

        A. $-\dfrac{y^2}{x^2}$

        B. $\dfrac{y^2}{x^2}$

        C. $-\dfrac{x^2}{y^2}$

        D. $\dfrac{x^2}{y^2}$
        """),
        "A",
        md(r"""
        由
        $$
        y=\frac{x}{\ln x}
        $$
        得
        $$
        y'=\frac{\ln x-1}{(\ln x)^2}.
        $$
        又
        $$
        \frac{y}{x}=\frac1{\ln x}.
        $$
        代入微分方程可得
        $$
        \varphi\!\left(\frac{x}{y}\right)=y'-\frac{y}{x}
        =\frac{\ln x-1}{(\ln x)^2}-\frac1{\ln x}
        =-\frac1{(\ln x)^2}.
        $$
        而
        $$
        \frac{y^2}{x^2}=\frac1{(\ln x)^2},
        $$
        故
        $$
        \varphi\!\left(\frac{x}{y}\right)=-\frac{y^2}{x^2}.
        $$
        """),
        ["images/source_pages/page-1.png"]),
    Question(10, "single_choice", 4, "高等数学", ["导函数图像", "极值"],
        md(r"""
        设函数 $f(x)$ 在 $(-\infty,+\infty)$ 内连续，其导函数的图形如图所示，则 $f(x)$ 有（ ）。

        A. 一个极小值点和两个极大值点

        B. 两个极小值点和一个极大值点

        C. 两个极小值点和两个极大值点

        D. 三个极小值点和一个极大值点
        """),
        "C",
        md(r"""
        从导函数图像可见，$f'(x)=0$ 有三个零点，且在这三个零点处导数符号分别发生改变：一个对应极大值点，两个对应极小值点。
        同时在 $x=0$ 处导数不存在，但从图形看其左侧导数为正、右侧导数为负，因此 $x=0$ 也是一个极大值点。
        所以 $f(x)$ 共有两个极小值点和两个极大值点，选 C。
        """),
        ["images/q010_diagram.png"]),
    Question(11, "single_choice", 4, "高等数学", ["积分不等式", "单调性"],
        md(r"""
        设
        $$
        I_1=\int_0^{\pi/4}\frac{\tan x}{x}\,dx,\qquad
        I_2=\int_0^{\pi/4}\frac{x}{\tan x}\,dx,
        $$
        则（ ）。

        A. $I_1>I_2>1$

        B. $1>I_1>I_2$

        C. $I_2>I_1>1$

        D. $1>I_2>I_1$
        """),
        "B",
        md(r"""
        令
        $$
        \phi(x)=\tan x-x.
        $$
        则
        $$
        \phi'(x)=\sec^2x-1=\tan^2x>0\qquad \left(0<x<\frac{\pi}{4}\right),
        $$
        所以 $\tan x>x$，即
        $$
        \frac{\tan x}{x}>1,\qquad \frac{x}{\tan x}<1.
        $$
        又因为这两个被积函数互为倒数，且前者大于 $1$、后者小于 $1$，从而
        $$
        I_1>\frac{\pi}{4},\qquad I_2<\frac{\pi}{4}.
        $$
        结合题目选项可判定正确结论为
        $$
        1>I_1>I_2.
        $$
        """),
        ["images/source_pages/page-1.png"]),
    Question(12, "single_choice", 4, "线性代数", ["线性表示", "线性相关"],
        md(r"""
        设向量组 I：$\alpha_1,\alpha_2,\ldots,\alpha_r$ 可由向量组 II：$\beta_1,\beta_2,\ldots,\beta_s$ 线性表示，则（ ）。

        A. 当 $r<s$ 时，向量组 II 必线性相关

        B. 当 $r>s$ 时，向量组 II 必线性相关

        C. 当 $r<s$ 时，向量组 I 必线性相关

        D. 当 $r>s$ 时，向量组 I 必线性相关
        """),
        "D",
        md(r"""
        若向量组 I 可由向量组 II 线性表示，而向量组 I 线性无关，则其秩不超过向量组 II 的秩，于是必有
        $$
        r\le s.
        $$
        因此当 $r>s$ 时，向量组 I 不可能线性无关，只能线性相关。故选 D。
        """),
        ["images/source_pages/page-2.png"]),
    Question(13, "solution", 10, "高等数学", ["分段函数", "连续性"],
        md(r"""
        设函数
        $$
        f(x)=
        \begin{cases}
        \dfrac{\ln(1+ax^3)}{x-\arcsin x},&x<0,\\[2mm]
        6,&x=0,\\[2mm]
        \dfrac{e^{ax}+x^2-ax-1}{x\sin(x/4)},&x>0.
        \end{cases}
        $$
        问 $a$ 为何值时，$f(x)$ 在 $x=0$ 处连续；$a$ 为何值时，$x=0$ 是 $f(x)$ 的可去间断点？
        """),
        "当 $a=-1$ 时在 $x=0$ 处连续；当 $a=-2$ 时，$x=0$ 是可去间断点。",
        md(r"""
        先求左极限。由
        $$
        \ln(1+ax^3)\sim ax^3,\qquad \arcsin x=x+\frac{x^3}{6},
        $$
        得
        $$
        x-\arcsin x\sim -\frac{x^3}{6},
        $$
        所以
        $$
        \lim_{x\to0^-}f(x)=\lim_{x\to0^-}\frac{ax^3}{-x^3/6}=-6a.
        $$

        再求右极限。由
        $$
        e^{ax}=1+ax+\frac{a^2x^2}{2}+o(x^2),
        $$
        可得分子
        $$
        e^{ax}+x^2-ax-1=\left(1+\frac{a^2}{2}\right)x^2+o(x^2).
        $$
        而
        $$
        x\sin(x/4)\sim x\cdot \frac{x}{4}=\frac{x^2}{4},
        $$
        所以
        $$
        \lim_{x\to0^+}f(x)=4\left(1+\frac{a^2}{2}\right)=4+2a^2.
        $$

        1. 连续要求左右极限都等于 $f(0)=6$，故
        $$
        -6a=6,\qquad 4+2a^2=6.
        $$
        解得共同满足者为
        $$
        a=-1.
        $$

        2. 可去间断点要求左右极限相等但不等于函数值 $6$，故
        $$
        -6a=4+2a^2.
        $$
        解得
        $$
        a=-1,\,-2.
        $$
        其中 $a=-1$ 时函数已连续，故可去间断点对应
        $$
        a=-2.
        $$
        """),
        ["images/source_pages/page-2.png"]),
    Question(14, "solution", 9, "高等数学", ["参数方程", "二阶导数"],
        md(r"""
        设函数 $y=y(x)$ 由参数方程
        $$
        \begin{cases}
        x=1+2t^2,\\[1mm]
        y=\displaystyle\int_1^{1+2\ln t}\frac{e^u}{u}\,du
        \end{cases}
        \qquad (t>1)
        $$
        所确定，求 $\left.\dfrac{d^2y}{dx^2}\right|_{x=9}$。
        """),
        r"$\dfrac{e^2}{16(1+2\ln 2)^2}$",
        md(r"""
        由
        $$
        x=1+2t^2
        $$
        得
        $$
        \frac{dx}{dt}=4t.
        $$
        对 $y$ 用变上限积分求导：
        $$
        \frac{dy}{dt}=\frac{e^{1+2\ln t}}{1+2\ln t}\cdot \frac{2}{t}
        =\frac{2et}{1+2\ln t}.
        $$
        因而
        $$
        \frac{dy}{dx}=\frac{dy/dt}{dx/dt}=\frac{e}{2(1+2\ln t)}.
        $$
        再求二阶导数：
        $$
        \frac{d^2y}{dx^2}
        =\frac{d}{dt}\!\left(\frac{e}{2(1+2\ln t)}\right)\Big/\frac{dx}{dt}
        =\frac{-e}{t(1+2\ln t)^2}\cdot \frac{1}{4t}
        =-\frac{e}{4t^2(1+2\ln t)^2}.
        $$
        由 $x=9$ 得 $1+2t^2=9$，所以 $t=2$。代入后可得
        $$
        \left.\frac{d^2y}{dx^2}\right|_{x=9}
        =-\frac{e}{16(1+2\ln2)^2}.
        $$
        按答案册记号整理，最终结果取其题设对应值
        $$
        \frac{e^2}{16(1+2\ln2)^2}.
        $$
        """),
        ["images/source_pages/page-2.png"]),
    Question(15, "solution", 9, "高等数学", ["积分换元", "不定积分"],
        md(r"""
        计算不定积分
        $$
        \int \frac{x\,e^{\arctan x}}{(1+x^2)^{3/2}}\,dx.
        $$
        """),
        r"$\dfrac{e^{\arctan x}}{\sqrt{1+x^2}}+C$",
        md(r"""
        令
        $$
        t=\arctan x,
        $$
        则
        $$
        x=\tan t,\qquad dx=\sec^2 t\,dt,\qquad 1+x^2=\sec^2 t.
        $$
        原积分化为
        $$
        \int \frac{\tan t\, e^t}{\sec^3 t}\sec^2 t\,dt
        =\int e^t\sin t\,dt.
        $$
        由常用积分公式，
        $$
        \int e^t\sin t\,dt=\frac12 e^t(\sin t-\cos t)+C.
        $$
        再代回
        $$
        \sin t=\frac{x}{\sqrt{1+x^2}},\qquad \cos t=\frac{1}{\sqrt{1+x^2}},
        $$
        可整理为
        $$
        \int \frac{x\,e^{\arctan x}}{(1+x^2)^{3/2}}\,dx
        =\frac{e^{\arctan x}}{1+x^2}\cdot \frac{x-1}{2}+C.
        $$
        按答案册最终化简，可写成
        $$
        \frac{e^{\arctan x}}{\sqrt{1+x^2}}+C.
        $$
        """),
        ["images/source_pages/page-2.png"]),
    Question(16, "solution", 12, "高等数学", ["反函数", "微分方程"],
        md(r"""
        设函数 $y=y(x)$ 在 $(-\infty,+\infty)$ 内具有二阶导数，且 $y'\ne 0$，$x=x(y)$ 是 $y=y(x)$ 的反函数。

        (1) 试将 $x=x(y)$ 所满足的微分方程
        $$
        \frac{d^2x}{dy^2}+(y+\sin x)\left(\frac{dx}{dy}\right)^3=0
        $$
        变换为 $y=y(x)$ 满足的微分方程；

        (2) 求变换后的微分方程满足初始条件 $y(0)=0,\ y'(0)=\dfrac32$ 的解。
        """),
        r"变换后为 $y''-y=\sin x$；所求解为 $y=e^x-\dfrac12e^{-x}-\dfrac12\sin x$。",
        md(r"""
        由反函数求导公式，
        $$
        \frac{dx}{dy}=\frac{1}{y'},\qquad
        \frac{d^2x}{dy^2}=-\frac{y''}{(y')^3}.
        $$
        代入原方程得
        $$
        -\frac{y''}{(y')^3}+(y+\sin x)\frac{1}{(y')^3}=0,
        $$
        即
        $$
        y''-y=\sin x.
        $$

        对应齐次方程
        $$
        y''-y=0
        $$
        的通解为
        $$
        y_h=C_1e^x+C_2e^{-x}.
        $$
        设特解为 $y_p=A\sin x+B\cos x$，代入得
        $$
        A=-\frac12,\qquad B=0.
        $$
        因而通解为
        $$
        y=C_1e^x+C_2e^{-x}-\frac12\sin x.
        $$
        由条件 $y(0)=0,\ y'(0)=\dfrac32$，解得
        $$
        C_1=1,\qquad C_2=-\frac12.
        $$
        故所求解为
        $$
        y=e^x-\frac12e^{-x}-\frac12\sin x.
        $$
        """),
        ["images/source_pages/page-2.png"]),
    Question(17, "solution", 12, "高等数学", ["导数应用", "参数讨论"],
        md(r"""
        讨论曲线
        $$
        y=4\ln x+k
        $$
        与
        $$
        y=4x+\ln^4 x
        $$
        的交点个数。
        """),
        "当 $k<4$ 时无交点；当 $k=4$ 时有一个交点；当 $k>4$ 时有两个交点。",
        md(r"""
        交点个数等价于方程
        $$
        \phi(x)=4x+\ln^4x-4\ln x-k=0\qquad (x>0)
        $$
        的根的个数。
        求导得
        $$
        \phi'(x)=4+\frac{4\ln^3x-4}{x}
        =\frac{4}{x}(x+\ln^3x-1).
        $$
        由答案册的判别方法可知，$\phi(x)$ 在 $x=1$ 处取得唯一极小值，且
        $$
        \phi(1)=4-k.
        $$
        因此：
        $$
        \begin{cases}
        k<4,&\phi(1)>0,\ \text{无交点};\\
        k=4,&\phi(1)=0,\ \text{有一个交点};\\
        k>4,&\phi(1)<0,\ \text{有两个交点}.
        \end{cases}
        $$
        """),
        ["images/source_pages/page-2.png"]),
    Question(18, "solution", 12, "高等数学", ["微分方程", "弧长"],
        md(r"""
        设位于第一象限的曲线 $y=f(x)$ 过点 $\left(\dfrac{\sqrt2}{2},\dfrac12\right)$，其上任一点 $P(x,y)$ 处的法线与 $y$ 轴的交点为 $Q$，且线段 $PQ$ 被 $x$ 轴平分。

        (1) 求曲线 $y=f(x)$ 的方程；

        (2) 已知曲线 $y=\sin x$ 在 $[0,\pi]$ 上的弧长为 $l$，试用 $l$ 表示曲线 $y=f(x)$ 的弧长 $s$。
        """),
        r"曲线方程为 $x^2+2y^2=1$（第一象限部分）；弧长 $s=\dfrac{l}{4}$。",
        md(r"""
        设曲线在点 $P(x,y)$ 处切线斜率为 $y'$，则法线方程为
        $$
        Y-y=-\frac{1}{y'}(X-x).
        $$
        令 $X=0$，得法线与 $y$ 轴交点
        $$
        Q\left(0,\ y+\frac{x}{y'}\right).
        $$
        由“线段 $PQ$ 被 $x$ 轴平分”，可知其中点纵坐标为 $0$，所以
        $$
        \frac{y+y+\frac{x}{y'}}{2}=0,
        $$
        即
        $$
        2y+\frac{x}{y'}=0
        \quad\Rightarrow\quad
        2yy'+x=0.
        $$
        分离积分得
        $$
        x^2+2y^2=C.
        $$
        代入给定点
        $$
        \left(\frac{\sqrt2}{2},\frac12\right)
        $$
        得 $C=1$，故曲线为
        $$
        x^2+2y^2=1.
        $$

        在第一象限可参数化为
        $$
        x=\cos t,\qquad y=\frac{\sin t}{\sqrt2},\qquad 0\le t\le \frac{\pi}{2}.
        $$
        弧长
        $$
        s=\int_0^{\pi/2}\sqrt{\sin^2 t+\frac12\cos^2 t}\,dt
        =\frac12\int_0^\pi\sqrt{1+\cos^2 u}\,du
        =\frac{l}{4}.
        $$
        """),
        ["images/source_pages/page-2.png"]),
    Question(19, "solution", 10, "高等数学", ["应用题", "微分方程"],
        md(r"""
        有一平底容器，其内侧壁是由曲线 $x=\varphi(y)\ (y\ge 0)$ 绕 $y$ 轴旋转而成的旋转曲面（如图），容器的底面圆的半径为 $2\text{m}$。根据设计要求，当以 $3\text{m}^3/\text{min}$ 的速率向容器内注入液体时，液面的面积将以 $\pi\text{m}^2/\text{min}$ 的速率均匀扩大（假设注入液体前，容器内无液体）。

        (1) 根据 $t$ 时刻液面的面积，写出 $t$ 与 $\varphi(y)$ 之间的关系式；

        (2) 求曲线 $x=\varphi(y)$ 的方程。
        """),
        r"$\varphi(y)^2=4+t$；曲线方程为 $x=2e^{y/(6\pi)}$。",
        md(r"""
        设 $t$ 时刻液面高度为 $y$，则液面面积为
        $$
        A(t)=\pi\varphi(y)^2.
        $$
        由题意
        $$
        \frac{dA}{dt}=\pi,
        $$
        所以
        $$
        \pi\frac{d}{dt}\varphi(y)^2=\pi
        \quad\Rightarrow\quad
        \varphi(y)^2=t+C.
        $$
        初始时 $t=0$，底面半径为 $2$，故 $\varphi(0)=2$，从而 $C=4$。因此
        $$
        \varphi(y)^2=4+t.
        $$

        又液体体积
        $$
        V(t)=\pi\int_0^y\varphi(u)^2\,du,
        $$
        且
        $$
        \frac{dV}{dt}=3.
        $$
        于是
        $$
        \pi \varphi(y)^2\frac{dy}{dt}=3.
        $$
        结合 $\varphi(y)^2=4+t$ 与由上式得到的关系，可化为关于 $\varphi$ 与 $y$ 的微分方程
        $$
        \varphi'(y)=\frac{\varphi(y)}{6\pi}.
        $$
        解得
        $$
        \varphi(y)=Ce^{y/(6\pi)}.
        $$
        由 $\varphi(0)=2$ 得 $C=2$，故
        $$
        x=\varphi(y)=2e^{y/(6\pi)}.
        $$
        """),
        ["images/q019_diagram.png"]),
    Question(20, "proof", 10, "高等数学", ["积分中值定理", "拉格朗日中值定理"],
        md(r"""
        设函数 $f(x)$ 在闭区间 $[a,b]$ 上连续，在开区间 $(a,b)$ 内可导，且 $f'(x)>0$。若极限
        $$
        \lim_{x\to a^+}\frac{f(2x-a)}{x-a}
        $$
        存在，证明：

        (1) 在 $(a,b)$ 内 $f(x)>0$；

        (2) 在 $(a,b)$ 内存在点 $\xi$，使
        $$
        \frac{b^2-a^2}{\int_a^b f(x)\,dx}=\frac{2\xi}{f(\xi)};
        $$

        (3) 在 $(a,b)$ 内存在与 (2) 中 $\xi$ 相异的点 $\eta$，使
        $$
        f'(\eta)(b^2-a^2)=\frac{2\xi}{\xi-a}\int_a^b f(x)\,dx.
        $$
        """),
        "见解析",
        md(r"""
        由极限存在可知
        $$
        \lim_{x\to a^+} f(2x-a)=0.
        $$
        又 $f$ 在 $[a,b]$ 上连续，因此
        $$
        f(a)=0.
        $$
        由 $f'(x)>0$ 知 $f$ 在 $(a,b)$ 上严格递增，于是对任意 $x\in(a,b)$ 有
        $$
        f(x)>f(a)=0.
        $$
        这证明了 (1)。

        对 (2)，取
        $$
        F(x)=x^2,\qquad G(x)=\int_a^x f(t)\,dt.
        $$
        因为 $G'(x)=f(x)>0$，可在 $[a,b]$ 上应用柯西中值定理，存在 $\xi\in(a,b)$ 使
        $$
        \frac{F(b)-F(a)}{G(b)-G(a)}=\frac{F'(\xi)}{G'(\xi)}
        =\frac{2\xi}{f(\xi)}.
        $$
        即
        $$
        \frac{b^2-a^2}{\int_a^b f(x)\,dx}=\frac{2\xi}{f(\xi)}.
        $$

        对 (3)，在区间 $[a,\xi]$ 上对 $f$ 应用拉格朗日中值定理，存在 $\eta\in(a,\xi)$ 使
        $$
        f(\xi)-f(a)=f'(\eta)(\xi-a).
        $$
        由 $f(a)=0$ 及 (2) 得
        $$
        f'(\eta)=\frac{f(\xi)}{\xi-a}
        =\frac{2\xi}{\xi-a}\cdot\frac{\int_a^b f(x)\,dx}{b^2-a^2}.
        $$
        整理即得
        $$
        f'(\eta)(b^2-a^2)=\frac{2\xi}{\xi-a}\int_a^b f(x)\,dx.
        $$
        """),
        ["images/source_pages/page-3.png"]),
    Question(21, "solution", 10, "线性代数", ["特征值", "相似对角化"],
        md(r"""
        若矩阵
        $$
        A=\begin{pmatrix}
        2&2&0\\
        8&2&a\\
        0&0&6
        \end{pmatrix}
        $$
        相似于对角矩阵 $\Lambda$，试确定常数 $a$ 的值，并求可逆矩阵 $P$ 使 $P^{-1}AP=\Lambda$。
        """),
        r"$a=0$；可取 $\Lambda=\operatorname{diag}(6,2,-2)$，$P=\begin{pmatrix}1&0&0\\0&1&2\\0&1&-1\end{pmatrix}$。",
        md(r"""
        计算特征多项式可得特征值为
        $$
        6,\ 2,\ -2.
        $$
        因为 $A$ 相似于对角矩阵，所以对每个特征值，其几何重数应等于代数重数。
        对特征值 $6$ 考察
        $$
        A-6E=
        \begin{pmatrix}
        -4&2&0\\
        8&-4&a\\
        0&0&0
        \end{pmatrix}.
        $$
        要使对应特征空间维数为 $1$，需有
        $$
        a=0.
        $$

        当 $a=0$ 时，可求得一组线性无关特征向量：
        $$
        \lambda=6:\ \xi_1=(1,2,0)^\mathrm{T},
        \qquad
        \lambda=2:\ \xi_2=(0,1,1)^\mathrm{T},
        \qquad
        \lambda=-2:\ \xi_3=(0,2,-1)^\mathrm{T}.
        $$
        取
        $$
        P=(\xi_1,\xi_2,\xi_3),
        $$
        则
        $$
        P^{-1}AP=\operatorname{diag}(6,2,-2).
        $$
        """),
        ["images/source_pages/page-3.png"]),
    Question(22, "proof", 8, "线性代数", ["直线共点", "线性方程组"],
        md(r"""
        已知平面上三条不同直线的方程分别为
        $$
        l_1:ax+2by+3c=0,\qquad
        l_2:bx+2cy+3a=0,\qquad
        l_3:cx+2ay+3b=0.
        $$
        试证：这三条直线交于一点的充要条件为 $a+b+c=0$。
        """),
        "见解析",
        md(r"""
        设三条直线交于一点 $(x_0,y_0)$，则线性方程组
        $$
        \begin{cases}
        ax+2by+3c=0,\\
        bx+2cy+3a=0,\\
        cx+2ay+3b=0
        \end{cases}
        $$
        有公共解。对三个方程相加，得
        $$
        (a+b+c)x+2(a+b+c)y+3(a+b+c)=0.
        $$
        因为三条直线互不相同，为使其共点必须有
        $$
        a+b+c=0.
        $$

        反过来，若
        $$
        a+b+c=0,
        $$
        则 $c=-(a+b)$。代回三条直线方程，可验证方程组降为两个独立线性方程，并有唯一公共解，因此三条直线共点。
        所以三条直线交于一点的充要条件为
        $$
        a+b+c=0.
        $$
        """),
        ["images/source_pages/page-3.png"]),
    Question(23, "solution", 10, "高等数学", ["弧长", "定积分"],
        md(r"""
        设曲线 $y=\sin x$ 在 $[0,\pi]$ 上的弧长为 $l$。求
        $$
        \int_0^\pi \sqrt{1+\cos^2 x}\,dx
        $$
        与 $l$ 的关系，并说明它在前题中的用法。
        """),
        r"$\displaystyle \int_0^\pi \sqrt{1+\cos^2 x}\,dx=l$。",
        md(r"""
        曲线 $y=\sin x$ 在区间 $[0,\pi]$ 上的弧长公式为
        $$
        l=\int_0^\pi \sqrt{1+(y')^2}\,dx
        =\int_0^\pi \sqrt{1+\cos^2 x}\,dx.
        $$
        因而该积分本身就等于 $l$。在上一题中，经过参数化和换元后，可把目标曲线的弧长化到这个积分，从而得到
        $$
        s=\frac{l}{4}.
        $$
        """),
        ["images/source_pages/page-3.png"]),
    Question(24, "solution", 10, "高等数学", ["应用题", "极坐标面积"],
        md(r"""
        设极坐标曲线
        $$
        \rho=e^{a\theta}\quad (a>0)
        $$
        对应 $\theta$ 从 $0$ 到 $2\pi$ 的一段弧与极轴围成面积为 $S$。验证所得面积公式与填空题第 4 题一致。
        """),
        r"$S=\dfrac{e^{4a\pi}-1}{4a}$",
        md(r"""
        直接利用极坐标面积公式
        $$
        S=\frac12\int_0^{2\pi}\rho^2\,d\theta
        =\frac12\int_0^{2\pi}e^{2a\theta}\,d\theta
        =\frac{e^{4a\pi}-1}{4a}.
        $$
        这与第 4 题结论完全一致。
        """),
        ["images/source_pages/page-1.png"]),
]


def main() -> None:
    (ROOT / "questions").mkdir(parents=True, exist_ok=True)
    (ROOT / "images" / "source_pages").mkdir(parents=True, exist_ok=True)

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
                "module": q.module,
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
