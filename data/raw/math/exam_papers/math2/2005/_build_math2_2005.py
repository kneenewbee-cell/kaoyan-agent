from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent
YEAR = 2005


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
        "范围：试卷 III  ",
        "整理状态：已按原卷页面图像校对并转录。",
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
        "范围：试卷 III",
        "校对状态：已按答案页与题面同步清洗整理。",
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
        4,
        "高等数学",
        ["微分", "复合函数求导"],
        "设\n$$\ny=(1+\\sin x)^x,\n$$\n则 $dy\\vert_{x=\\pi}=\\underline{\\qquad}$。",
        "$-\\pi\\,dx$",
        "先求导数：\n$$\ny'=(1+\\sin x)^x\\left[\\ln(1+\\sin x)+\\frac{x\\cos x}{1+\\sin x}\\right].\n$$\n当 $x=\\pi$ 时，$\\sin\\pi=0,\\cos\\pi=-1$，故\n$$\ny'(\\pi)=\\ln 1+\\pi\\cdot(-1)=-\\pi.\n$$\n因此\n$$\ndy\\vert_{x=\\pi}=y'(\\pi)\\,dx=-\\pi\\,dx.\n$$",
        ["images/source_pages/page-1.png"],
    ),
    Question(
        2,
        "fill_blank",
        4,
        "高等数学",
        ["斜渐近线", "极限"],
        "曲线\n$$\ny=\\frac{(1+x)^{3/2}}{\\sqrt{x}}\n$$\n的斜渐近线方程为 $\\underline{\\qquad}$。",
        "$y=x+\\dfrac{3}{2}$",
        "利用斜渐近线公式 $y=ax+b$，其中\n$$\na=\\lim_{x\\to+\\infty}\\frac{f(x)}{x},\\qquad b=\\lim_{x\\to+\\infty}[f(x)-ax].\n$$\n对 $f(x)=\\dfrac{(1+x)^{3/2}}{\\sqrt{x}}$，有\n$$\na=\\lim_{x\\to+\\infty}\\frac{(1+x)^{3/2}}{x\\sqrt{x}}=1.\n$$\n再算\n$$\nb=\\lim_{x\\to+\\infty}\\left(\\frac{(1+x)^{3/2}}{\\sqrt{x}}-x\\right)=\\frac{3}{2}.\n$$\n故斜渐近线为\n$$\ny=x+\\frac{3}{2}.\n$$",
        ["images/source_pages/page-1.png"],
    ),
    Question(
        3,
        "fill_blank",
        4,
        "高等数学",
        ["定积分", "三角换元"],
        "计算\n$$\n\\int_0^1\\frac{x\\,dx}{(2-x^2)\\sqrt{1-x^2}}=\\underline{\\qquad}。\n$$",
        "$\\dfrac{\\pi}{4}$",
        "令 $x=\\sin t\\ (0<t<\\tfrac\\pi2)$，则 $dx=\\cos t\\,dt$，原积分化为\n$$\n\\int_0^{\\pi/2}\\frac{\\sin t}{2-\\sin^2 t}\\,dt.\n$$\n再令 $u=\\cos t$，则 $du=-\\sin t\\,dt$，得\n$$\n\\int_0^{\\pi/2}\\frac{\\sin t}{2-\\sin^2 t}\\,dt=\\int_1^0\\frac{-du}{1+u^2}=\\int_0^1\\frac{du}{1+u^2}=\\arctan 1=\\frac{\\pi}{4}.\n$$",
        ["images/source_pages/page-1.png"],
    ),
    Question(
        4,
        "fill_blank",
        4,
        "高等数学",
        ["一阶线性微分方程", "积分因子"],
        "微分方程\n$$\nxy'+2y=x\\ln x\n$$\n满足 $y(1)=-\\dfrac19$ 的解为 $\\underline{\\qquad}$。",
        "$y=\\dfrac13x\\ln x-\\dfrac19x$",
        "将方程写成\n$$\ny'+\\frac{2}{x}y=\\ln x\\qquad (x>0).\n$$\n积分因子为 $\\mu(x)=x^2$，故\n$$\n(x^2y)'=x^2\\ln x.\n$$\n积分得\n$$\nx^2y=\\int x^2\\ln x\\,dx=\\frac{x^3}{3}\\ln x-\\frac{x^3}{9}+C,\n$$\n即\n$$\ny=\\frac13x\\ln x-\\frac19x+\\frac{C}{x^2}.\n$$\n由 $y(1)=-\\dfrac19$ 得 $C=0$，所以\n$$\ny=\\frac13x\\ln x-\\frac19x.\n$$",
        ["images/source_pages/page-1.png"],
    ),
    Question(
        5,
        "fill_blank",
        4,
        "高等数学",
        ["等价无穷小", "极限"],
        "当 $x\\to0$ 时，$\\alpha(x)=kx^2$ 与 $\\beta(x)=\\sqrt{1+x\\arcsin x}-\\sqrt{\\cos x}$ 是等价无穷小量，则 $k=\\underline{\\qquad}$。",
        "$\\dfrac34$",
        "由题意有\n$$\n\\lim_{x\\to0}\\frac{\\beta(x)}{\\alpha(x)}=1.\n$$\n对 $\\beta(x)$ 有\n$$\n\\beta(x)=\\frac{x\\arcsin x+1-\\cos x}{\\sqrt{1+x\\arcsin x}+\\sqrt{\\cos x}}.\n$$\n又当 $x\\to0$ 时，\n$$\n\\arcsin x\\sim x,\\qquad 1-\\cos x\\sim \\frac{x^2}{2},\n$$\n故\n$$\n\\beta(x)\\sim \\frac{x^2+\\frac{x^2}{2}}{2}=\\frac34x^2.\n$$\n于是 $kx^2\\sim\\beta(x)\\sim\\dfrac34x^2$，从而\n$$\nk=\\frac34.\n$$",
        ["images/source_pages/page-1.png"],
    ),
    Question(
        6,
        "fill_blank",
        4,
        "线性代数",
        ["行列式", "矩阵列变换"],
        "设 $\\alpha_1,\\alpha_2,\\alpha_3$ 均为 3 维列向量，记矩阵\n$$\nA=(\\alpha_1,\\alpha_2,\\alpha_3),\\quad B=(\\alpha_1+\\alpha_2+\\alpha_3,\\alpha_1+2\\alpha_2+4\\alpha_3,\\alpha_1+3\\alpha_2+9\\alpha_3).\n$$\n如果 $|A|=1$，那么 $|B|=\\underline{\\qquad}$。",
        "$2$",
        "可写成\n$$\nB=A\\begin{pmatrix}1&1&1\\\\1&2&3\\\\1&4&9\\end{pmatrix}.\n$$\n故\n$$\n|B|=|A|\\cdot\\begin{vmatrix}1&1&1\\\\1&2&3\\\\1&4&9\\end{vmatrix}.\n$$\n由 $|A|=1$，且范德蒙德行列式\n$$\n\\begin{vmatrix}1&1&1\\\\1&2&3\\\\1&4&9\\end{vmatrix}=(2-1)(3-1)(3-2)=2,\n$$\n所以\n$$\n|B|=2.\n$$",
        ["images/source_pages/page-1.png"],
    ),
    Question(
        7,
        "single_choice",
        4,
        "高等数学",
        ["函数极限", "可导性"],
        "设函数\n$$\nf(x)=\\lim_{n\\to\\infty}\\sqrt[n]{1+|x|^{3n}},\n$$\n则 $f(x)$ 在 $(-\\infty,+\\infty)$ 内（  ）\n\nA. 处处可导\n\nB. 恰有一个不可导点\n\nC. 恰有两个不可导点\n\nD. 至少有三个不可导点",
        "C",
        "分段求极限：\n$$\nf(x)=\\begin{cases}1,&|x|<1,\\\\|x|^3,&|x|\\ge1.\\end{cases}\n$$\n因此在 $x=\\pm1$ 处，左右导数不相等，函数不可导；其余各点都可导。故恰有两个不可导点，选 C。",
        ["images/source_pages/page-1.png"],
    ),
    Question(
        8,
        "single_choice",
        4,
        "高等数学",
        ["原函数", "奇偶性"],
        "设 $F(x)$ 是连续函数 $f(x)$ 的一个原函数，“$M\\Leftrightarrow N$”表示“$M$ 的充分必要条件是 $N$”，则必有（  ）\n\nA. $F(x)$ 是偶函数 $\\Leftrightarrow f(x)$ 是奇函数\n\nB. $F(x)$ 是奇函数 $\\Leftrightarrow f(x)$ 是偶函数\n\nC. $F(x)$ 是周期函数 $\\Leftrightarrow f(x)$ 是周期函数\n\nD. $F(x)$ 是单调函数 $\\Leftrightarrow f(x)$ 是单调函数",
        "A",
        "若 $F$ 是偶函数，则对两边求导得\n$$\nF'(-x)(-1)=F'(x),\n$$\n即\n$$\nf(-x)=-f(x),\n$$\n所以 $f$ 为奇函数。反之若 $f$ 为奇函数，取\n$$\nF(x)=\\int_0^x f(t)\\,dt+C,\n$$\n则由换元可得 $F(-x)=F(x)$，故 $F$ 为偶函数。A 必然成立。",
        ["images/source_pages/page-1.png"],
    ),
    Question(
        9,
        "single_choice",
        4,
        "高等数学",
        ["参数方程", "法线方程"],
        "设函数 $y=y(x)$ 由参数方程\n$$\n\\begin{cases}\nx=t^2+2t,\\\\\ny=\\ln(1+t)\n\\end{cases}\n$$\n确定，则曲线 $y=y(x)$ 在 $x=3$ 处的法线与 $x$ 轴交点的横坐标是（  ）\n\nA. $\\dfrac18\\ln2+3$\n\nB. $-\\dfrac18\\ln2+3$\n\nC. $-8\\ln2+3$\n\nD. $8\\ln2+3$",
        "A",
        "由 $x=3$ 得 $t^2+2t=3$，解得 $t=1$ 或 $-3$，而 $t>-1$，故取 $t=1$。此时点为 $(3,\\ln2)$。\n$$\n\\frac{dy}{dx}=\\frac{dy/dt}{dx/dt}=\\frac{1/(1+t)}{2t+2}.\n$$\n在 $t=1$ 处，切线斜率为 $\\dfrac18$，故法线斜率为 $-8$。法线方程为\n$$\ny-\\ln2=-8(x-3).\n$$\n令 $y=0$ 得\n$$\nx=3+\\frac18\\ln2.\n$$\n故选 A。",
        ["images/source_pages/page-1.png"],
    ),
    Question(
        10,
        "single_choice",
        4,
        "高等数学",
        ["曲线积分", "对称性"],
        "设区域 $D=\\{(x,y)\\mid x^2+y^2\\le4,\\ x\\ge0,\\ y\\ge0\\}$，$f(x)$ 为 $D$ 上的正值连续函数，$a,b$ 为常数，则\n$$\n\\iint_D\\frac{a\\sqrt{f(x)}+b\\sqrt{f(y)}}{\\sqrt{f(x)}+\\sqrt{f(y)}}\\,d\\sigma=(\\ \\ )\n$$\n\nA. $ab\\pi$\n\nB. $\\dfrac{ab}{2}\\pi$\n\nC. $(a+b)\\pi$\n\nD. $\\dfrac{a+b}{2}\\pi$",
        "D",
        "设\n$$\nI=\\iint_D\\frac{a\\sqrt{f(x)}+b\\sqrt{f(y)}}{\\sqrt{f(x)}+\\sqrt{f(y)}}\\,d\\sigma.\n$$\n交换 $x,y$ 后，由区域关于直线 $y=x$ 对称，得\n$$\nI=\\iint_D\\frac{a\\sqrt{f(y)}+b\\sqrt{f(x)}}{\\sqrt{f(x)}+\\sqrt{f(y)}}\\,d\\sigma.\n$$\n两式相加：\n$$\n2I=(a+b)\\iint_D1\\,d\\sigma.\n$$\n而 $D$ 是半径 2 的四分之一圆盘，面积为 $\\pi$，所以\n$$\nI=\\frac{a+b}{2}\\pi.\n$$\n故选 D。",
        ["images/source_pages/page-1.png"],
    ),
    Question(
        11,
        "single_choice",
        4,
        "高等数学",
        ["偏导数", "二阶偏导"],
        "设函数\n$$\nu(x,y)=\\varphi(x+y)+\\varphi(x-y)+\\int_{x-y}^{x+y}\\psi(t)\\,dt,\n$$\n其中函数 $\\varphi$ 具有二阶导数，$\\psi$ 具有一阶导数，则必有（  ）\n\nA. $\\dfrac{\\partial^2u}{\\partial x^2}=-\\dfrac{\\partial^2u}{\\partial y^2}$\n\nB. $\\dfrac{\\partial^2u}{\\partial x^2}=\\dfrac{\\partial^2u}{\\partial y^2}$\n\nC. $\\dfrac{\\partial^2u}{\\partial x\\partial y}=\\dfrac{\\partial^2u}{\\partial y^2}$\n\nD. $\\dfrac{\\partial^2u}{\\partial x\\partial y}=\\dfrac{\\partial^2u}{\\partial x^2}$",
        "B",
        "直接求偏导：\n$$\nu_x=\\varphi'(x+y)+\\varphi'(x-y)+\\psi(x+y)-\\psi(x-y),\n$$\n$$\nu_y=\\varphi'(x+y)-\\varphi'(x-y)+\\psi(x+y)+\\psi(x-y).\n$$\n再求二阶偏导，得\n$$\nu_{xx}=\\varphi''(x+y)+\\varphi''(x-y)+\\psi'(x+y)-\\psi'(x-y),\n$$\n$$\nu_{yy}=\\varphi''(x+y)+\\varphi''(x-y)+\\psi'(x+y)-\\psi'(x-y).\n$$\n故必有 $u_{xx}=u_{yy}$，选 B。",
        ["images/source_pages/page-1.png", "images/source_pages/page-2.png"],
    ),
    Question(
        12,
        "single_choice",
        4,
        "高等数学",
        ["间断点", "函数极限"],
        "设函数\n$$\nf(x)=\\frac{1}{e^{x/(x-1)}-1},\n$$\n则（  ）\n\nA. $x=0,x=1$ 都是 $f(x)$ 的第一类间断点\n\nB. $x=0,x=1$ 都是 $f(x)$ 的第二类间断点\n\nC. $x=0$ 是 $f(x)$ 的第一类间断点，$x=1$ 是 $f(x)$ 的第二类间断点\n\nD. $x=0$ 是 $f(x)$ 的第二类间断点，$x=1$ 是 $f(x)$ 的第一类间断点",
        "D",
        "当 $x\\to0$ 时，指数 $\\dfrac{x}{x-1}\\to0$，并且\n$$\ne^{x/(x-1)}-1\\sim \\frac{x}{x-1}\\sim -x,\n$$\n故 $f(x)\\sim-\\dfrac1x$，极限发散，所以 $x=0$ 是第二类间断点。\n\n当 $x\\to1^-$ 时，$\\dfrac{x}{x-1}\\to-\\infty$，故 $f(x)\\to-1$；当 $x\\to1^+$ 时，$\\dfrac{x}{x-1}\\to+\\infty$，故 $f(x)\\to0$。左右极限都存在但不相等，所以 $x=1$ 是第一类间断点。故选 D。",
        ["images/source_pages/page-2.png"],
    ),
    Question(
        13,
        "single_choice",
        4,
        "线性代数",
        ["特征值", "特征向量"],
        "设 $\\lambda_1,\\lambda_2$ 是矩阵 $A$ 的两个不同的特征值，对应的特征向量分别为 $\\alpha_1,\\alpha_2$，则 $\\alpha_1, A(\\alpha_1+\\alpha_2)$ 线性无关的充要条件是（  ）\n\nA. $\\lambda_1\\ne0$\n\nB. $\\lambda_2\\ne0$\n\nC. $\\lambda_1=0$\n\nD. $\\lambda_2=0$",
        "B",
        "因为\n$$\nA(\\alpha_1+\\alpha_2)=\\lambda_1\\alpha_1+\\lambda_2\\alpha_2.\n$$\n又 $\\lambda_1\\ne\\lambda_2$，故 $\\alpha_1,\\alpha_2$ 线性无关。于是 $\\alpha_1$ 与 $A(\\alpha_1+\\alpha_2)$ 线性无关，当且仅当后者中 $\\alpha_2$ 的系数不为零，即\n$$\n\\lambda_2\\ne0.\n$$\n故选 B。",
        ["images/source_pages/page-2.png"],
    ),
    Question(
        14,
        "single_choice",
        4,
        "线性代数",
        ["伴随矩阵", "初等矩阵"],
        "设 $A$ 为 $n(n\\ge2)$ 阶可逆矩阵，交换 $A$ 的第 1 行与第 2 行得矩阵 $B$，$A^*,B^*$ 分别为 $A,B$ 的伴随矩阵，则（  ）\n\nA. 交换 $A^*$ 的第 1 列与第 2 列得 $B^*$\n\nB. 交换 $A^*$ 的第 1 行与第 2 行得 $B^*$\n\nC. 交换 $A^*$ 的第 1 列与第 2 列得 $-B^*$\n\nD. 交换 $A^*$ 的第 1 行与第 2 行得 $-B^*$",
        "C",
        "设 $E_{12}$ 为交换第 1、2 行的初等矩阵，则 $B=E_{12}A$。于是\n$$\nB^*=|B|B^{-1}=(-|A|)A^{-1}E_{12}=-A^*E_{12}.\n$$\n右乘 $E_{12}$ 表示交换列，因此 $B^*$ 等于把 $A^*$ 的第 1、2 列交换后再乘以 $-1$。故选 C。",
        ["images/source_pages/page-2.png"],
    ),
    Question(
        15,
        "solution",
        11,
        "高等数学",
        ["极限", "积分变量替换"],
        "设函数 $f(x)$ 连续，且 $f(0)\\ne0$，求极限\n$$\n\\lim_{x\\to0}\\frac{\\int_0^x(x-t)f(t)\\,dt}{x\\int_0^xf(x-t)\\,dt}。\n$$",
        "$\\dfrac12$",
        "对分母中的积分作变量替换 $u=x-t$，得\n$$\n\\int_0^xf(x-t)\\,dt=\\int_0^xf(u)\\,du.\n$$\n于是原式为\n$$\n\\lim_{x\\to0}\\frac{\\int_0^x(x-t)f(t)\\,dt}{x\\int_0^xf(t)\\,dt}.\n$$\n分子分母同趋于 0，可用洛必达法则：\n$$\n\\lim_{x\\to0}\\frac{\\int_0^xf(t)\\,dt}{\\int_0^xf(t)\\,dt+xf(x)}.\n$$\n再将上下同除以 $x$，并利用连续性\n$$\n\\lim_{x\\to0}\\frac{\\frac1x\\int_0^xf(t)\\,dt}{\\frac1x\\int_0^xf(t)\\,dt+f(x)}=\frac{f(0)}{f(0)+f(0)}=\\frac12.\n$$",
        ["images/source_pages/page-2.png"],
    ),
    Question(
        16,
        "solution",
        11,
        "高等数学",
        ["定积分应用", "函数方程"],
        "如图，$C_1$ 和 $C_2$ 分别是 $y=\\dfrac12(1+e^x)$ 和 $y=e^x$ 的图像，过点 $(0,1)$ 的曲线 $C_3$ 是一单调增函数的图像，过 $C_2$ 上任一点 $M(x,y)$ 分别作垂直于 $x$ 轴和 $y$ 轴的直线 $l_x$ 和 $l_y$。记 $C_1,C_2$ 与 $l_x$ 所围图形的面积为 $S_1(x)$；$C_2,C_3$ 与 $l_y$ 所围图形的面积为 $S_2(y)$。如果总有 $S_1(x)=S_2(y)$，求曲线 $C_3$ 的方程 $x=\\varphi(y)$。",
        "$x=\\varphi(y)=\\ln y-\\dfrac12+\\dfrac{1}{2y}$",
        "由面积公式，\n$$\nS_1(x)=\\int_0^x\\left[e^t-\\frac12(1+e^t)\\right]dt=\\frac12(e^x-x-1).\n$$\n又由图形关系\n$$\nS_2(y)=\\int_1^y\\bigl(\\ln t-\\varphi(t)\\bigr)dt.\n$$\n题设给出 $S_1(x)=S_2(y)$，且点 $M(x,y)$ 在 $C_2$ 上，所以 $y=e^x$，即 $x=\\ln y$。代入得\n$$\n\\int_1^y\\bigl(\\ln t-\\varphi(t)\\bigr)dt=\\frac12(y-\\ln y-1).\n$$\n两边对 $y$ 求导：\n$$\n\\ln y-\\varphi(y)=\\frac12\\left(1-\\frac1y\\right).\n$$\n故\n$$\n\\varphi(y)=\\ln y-\\frac12+\\frac{1}{2y}.\n$$",
        ["images/q016_diagram.png"],
    ),
    Question(
        17,
        "solution",
        11,
        "高等数学",
        ["分部积分", "导数几何意义"],
        "如图，曲线 $C$ 的方程为 $y=f(x)$，点 $(3,2)$ 是它的一个拐点，直线 $l_1$ 与 $l_2$ 分别是曲线 $C$ 在点 $(0,0)$ 与 $(3,2)$ 处的切线，其交点为 $(2,4)$。设函数 $f(x)$ 具有三阶连续导数，计算定积分\n$$\n\\int_0^3(x^2+x)f'''(x)\\,dx。\n$$",
        "$20$",
        "由几何条件，直线 $l_1$ 过 $(0,0)$ 与 $(2,4)$，故其斜率为 2，于是\n$$\nf'(0)=2.\n$$\n同理直线 $l_2$ 过 $(3,2)$ 与 $(2,4)$，斜率为 $-2$，故\n$$\nf'(3)=-2.\n$$\n又 $(3,2)$ 是拐点，所以\n$$\nf''(3)=0.\n$$\n对积分作分部积分：\n$$\n\\int_0^3(x^2+x)f'''(x)dx=\\bigl[(x^2+x)f''(x)\\bigr]_0^3-\\int_0^3(2x+1)f''(x)dx.\n$$\n再分部积分一次：\n$$\n\\int_0^3(2x+1)f''(x)dx=\\bigl[(2x+1)f'(x)\\bigr]_0^3-2\\int_0^3f'(x)dx.\n$$\n代入已知条件与 $f(0)=0,f(3)=2$，得\n$$\n\\int_0^3(x^2+x)f'''(x)dx=0-\\bigl[7f'(3)-f'(0)-2(f(3)-f(0))\\bigr]=20.\n$$",
        ["images/q017_diagram.png"],
    ),
    Question(
        18,
        "solution",
        12,
        "高等数学",
        ["变量代换", "二阶常系数微分方程"],
        "用变量代换 $x=\\cos t\\ (0<t<\\pi)$ 化简微分方程\n$$\n(1-x^2)y''-xy'+y=0,\n$$\n并求其满足 $y\\vert_{x=0}=1$，$y'\\vert_{x=0}=2$ 的特解。",
        "$y=2x+\\sqrt{1-x^2}\\quad(-1<x<1)$",
        "令 $x=\\cos t$，则 $dx=-\\sin t\\,dt$。把 $y$ 看作 $t$ 的函数，利用链式法则可化原方程为\n$$\n\\frac{d^2y}{dt^2}+y=0.\n$$\n其通解为\n$$\ny=C_1\\cos t+C_2\\sin t.\n$$\n再换回 $x$：因 $0<t<\\pi$，故 $\\sin t=\\sqrt{1-x^2}$，从而\n$$\ny=C_1x+C_2\\sqrt{1-x^2}.\n$$\n由 $y(0)=1$ 得 $C_2=1$。又\n$$\ny'=C_1-\\frac{C_2x}{\\sqrt{1-x^2}},\n$$\n代入 $y'(0)=2$ 得 $C_1=2$。故所求特解为\n$$\ny=2x+\\sqrt{1-x^2},\\qquad -1<x<1.\n$$",
        ["images/source_pages/page-3.png"],
    ),
    Question(
        19,
        "proof",
        12,
        "高等数学",
        ["中值定理", "证明题"],
        "已知函数 $f(x)$ 在 $[0,1]$ 上连续，在 $(0,1)$ 内可导，且 $f(0)=0,\\ f(1)=1$。证明：\n\n（I）存在 $\\xi\\in(0,1)$，使得 $f(\\xi)=1-\\xi$；\n\n（II）存在两个不同的点 $\\eta,\\zeta\\in(0,1)$，使得 $f'(\\eta)f'(\\zeta)=1$。",
        "见解析",
        "（I）令\n$$\nF(x)=f(x)+x-1.\n$$\n则 $F$ 在 $[0,1]$ 上连续，且\n$$\nF(0)=-1<0,\\qquad F(1)=1>0.\n$$\n由介值定理，存在 $\\xi\\in(0,1)$，使得 $F(\\xi)=0$，即\n$$\nf(\\xi)=1-\\xi.\n$$\n\n（II）在区间 $[0,\\xi]$ 与 $[\\xi,1]$ 上分别应用拉格朗日中值定理，存在\n$$\n\\eta\\in(0,\\xi),\\qquad \\zeta\\in(\\xi,1)\n$$\n使得\n$$\nf'(\\eta)=\\frac{f(\\xi)-f(0)}{\\xi-0}=\\frac{1-\\xi}{\\xi},\n$$\n$$\nf'(\\zeta)=\\frac{f(1)-f(\\xi)}{1-\\xi}=\\frac{\\xi}{1-\\xi}.\n$$\n因此\n$$\nf'(\\eta)f'(\\zeta)=1.\n$$",
        ["images/source_pages/page-3.png"],
    ),
    Question(
        20,
        "solution",
        10,
        "高等数学",
        ["全微分", "条件极值"],
        "已知函数 $z=f(x,y)$ 的全微分\n$$\ndz=2x\\,dx-2y\\,dy,\n$$\n并且 $f(1,1)=2$。求 $f(x,y)$ 在椭圆域\n$$\nD=\\left\\{(x,y)\\mid x^2+\\frac{y^2}{4}\\le1\\right\\}\n$$\n上的最大值和最小值。",
        "最大值为 $3$，最小值为 $-2$",
        "由全微分得\n$$\nf_x=2x,\\qquad f_y=-2y.\n$$\n积分可得\n$$\nf(x,y)=x^2-y^2+C.\n$$\n由 $f(1,1)=2$ 得 $C=2$，故\n$$\nf(x,y)=x^2-y^2+2.\n$$\n内部驻点满足 $f_x=f_y=0$，即 $(0,0)$，对应函数值为 2。\n\n在边界 $x^2+\\dfrac{y^2}{4}=1$ 上，令 $y^2=4(1-x^2)$，则\n$$\nf(x,y)=x^2-4(1-x^2)+2=5x^2-2,\\qquad -1\\le x\\le1.\n$$\n于是最大值在 $x=\\pm1,y=0$ 处取得，为\n$$\nf_{\\max}=3;\n$$\n最小值在 $x=0,y=\\pm2$ 处取得，为\n$$\nf_{\\min}=-2.\n$$",
        ["images/source_pages/page-3.png"],
    ),
    Question(
        21,
        "solution",
        9,
        "高等数学",
        ["二重积分", "分区域积分"],
        "计算二重积分\n$$\n\\iint_D|x^2+y^2-1|\\,d\\sigma,\n$$\n其中 $D=\\{(x,y)\\mid 0\\le x\\le1,\\ 0\\le y\\le1\\}$。",
        "$\\dfrac{\\pi}{4}-\\dfrac13$",
        "将区域 $D$ 按圆弧 $x^2+y^2=1$ 分成两部分：\n$$\nD_1=\\{(x,y)\\in D\\mid x^2+y^2\\le1\\},\\qquad D_2=D\\setminus D_1.\n$$\n于是\n$$\n\\iint_D|x^2+y^2-1|d\\sigma=\\iint_{D_1}(1-x^2-y^2)d\\sigma+\\iint_{D_2}(x^2+y^2-1)d\\sigma.\n$$\n第一部分用极坐标：\n$$\n\\iint_{D_1}(1-r^2)d\\sigma=\\int_0^{\\pi/2}\\int_0^1(1-r^2)r\\,dr\\,d\\theta=\\frac{\\pi}{8}.\n$$\n第二部分可用补区域计算，整理后得\n$$\n\\iint_{D_2}(x^2+y^2-1)d\\sigma=\\frac{\\pi}{8}-\\frac13.\n$$\n故原积分为\n$$\n\\frac{\\pi}{8}+\\left(\\frac{\\pi}{8}-\\frac13\\right)=\\frac{\\pi}{4}-\\frac13.\n$$",
        ["images/source_pages/page-3.png"],
    ),
    Question(
        22,
        "solution",
        9,
        "线性代数",
        ["向量组线性表示", "秩"],
        "确定常数 $a$，使向量组\n$$\n\\alpha_1=(1,1,a)^\\mathrm{T},\\quad \\alpha_2=(1,a,1)^\\mathrm{T},\\quad \\alpha_3=(a,1,1)^\\mathrm{T}\n$$\n可由向量组\n$$\n\\beta_1=(1,1,a)^\\mathrm{T},\\quad \\beta_2=(-2,a,4)^\\mathrm{T},\\quad \\beta_3=(-2,a,a)^\\mathrm{T}\n$$\n线性表示，但向量组 $\\beta_1,\\beta_2,\\beta_3$ 不能由向量组 $\\alpha_1,\\alpha_2,\\alpha_3$ 线性表示。",
        "$a=1$",
        "设\n$$\nA=(\\alpha_1,\\alpha_2,\\alpha_3),\\qquad B=(\\beta_1,\\beta_2,\\beta_3).\n$$\n由“$\\beta$ 不能由 $\\alpha$ 线性表示”可知 $r(A)<3$，于是\n$$\n|A|=\\begin{vmatrix}1&1&a\\\\1&a&1\\\\a&1&1\\end{vmatrix}=-(a-1)^2(a+2)=0.\n$$\n故只可能有\n$$\na=1\\quad\\text{或}\\quad a=-2.\n$$\n\n当 $a=1$ 时，\n$$\n\\alpha_1=\\alpha_2=\\alpha_3=(1,1,1)^\\mathrm{T},\n$$\n显然 $\\alpha_1,\\alpha_2,\\alpha_3$ 可由 $\\beta_1,\\beta_2,\\beta_3$ 表出；另一方面 $\\beta_2=(-2,1,4)^\\mathrm{T}$ 不能由 $(1,1,1)^\\mathrm{T}$ 的倍数表示，所以 $\\beta$ 不能由 $\\alpha$ 表示，满足题意。\n\n当 $a=-2$ 时，检验可知 $\\alpha$ 也不能由 $\\beta$ 线性表示，与题意矛盾。\n\n因此唯一可取\n$$\na=1.\n$$",
        ["images/source_pages/page-3.png"],
    ),
    Question(
        23,
        "solution",
        9,
        "线性代数",
        ["齐次线性方程组", "秩"],
        "已知 3 阶矩阵 $A$ 的第一行是 $(a,b,c)$，$a,b,c$ 不全为零，矩阵\n$$\nB=\\begin{pmatrix}\n1&2&3\\\\\n2&4&6\\\\\n3&6&k\n\\end{pmatrix}\\quad (k\\text{ 为常数}),\n$$\n且 $AB=O$。求线性方程组 $Ax=0$ 的通解。",
        "当 $k\\ne9$ 时，$x=s(1,2,3)^\\mathrm{T}+t(3,6,k)^\\mathrm{T}$；当 $k=9$ 时，若 $r(A)=2$，则 $x=s(1,2,3)^\\mathrm{T}$；若 $r(A)=1$，则通解为 $x=s\\left(-\\dfrac ba,1,0\\right)^\\mathrm{T}+t\\left(-\\dfrac ca,0,1\\right)^\\mathrm{T}$（$a\\ne0$）。",
        "由 $AB=O$ 知，矩阵 $B$ 的每一列都是齐次方程组 $Ax=0$ 的解。\n\n当 $k\\ne9$ 时，\n$$\n\\beta_1=(1,2,3)^\\mathrm{T},\\quad \\beta_2=(2,4,6)^\\mathrm{T}=2\\beta_1,\quad \\beta_3=(3,6,k)^\\mathrm{T}\n$$\n中，$\\beta_1$ 与 $\\beta_3$ 线性无关，因此 $Ax=0$ 至少有两个线性无关解。又因 $A$ 的第一行不全为零，故 $r(A)\\ge1$；而解空间维数为 $3-r(A)$，只能等于 2，所以 $r(A)=1$。于是 $\\beta_1,\\beta_3$ 可作为基础解系，通解为\n$$\nx=s\\begin{pmatrix}1\\\\2\\\\3\\end{pmatrix}+t\\begin{pmatrix}3\\\\6\\\\k\\end{pmatrix},\\qquad s,t\\in\\mathbb{R}.\n$$\n\n当 $k=9$ 时，三列向量都与 $(1,2,3)^\\mathrm{T}$ 成比例。若 $r(A)=2$，则解空间维数为 1，基础解系可取 $(1,2,3)^\\mathrm{T}$，通解为\n$$\nx=s\\begin{pmatrix}1\\\\2\\\\3\\end{pmatrix}.\n$$\n若 $r(A)=1$，则 $A$ 的三行成比例，而第一行 $(a,b,c)$ 不全为零，可设 $a\\ne0$，则 $Ax=0$ 与一元方程\n$$\nax_1+bx_2+cx_3=0\n$$\n同解。取 $x_2,x_3$ 为自由变量，可得通解\n$$\nx=s\\begin{pmatrix}-\\dfrac ba\\\\1\\\\0\\end{pmatrix}+t\\begin{pmatrix}-\\dfrac ca\\\\0\\\\1\\end{pmatrix},\\qquad s,t\\in\\mathbb{R}.\n$$",
        ["images/source_pages/page-3.png"],
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

    (ROOT / f"math2_{YEAR}_questions.md").write_text(annual_questions_md(QUESTIONS), encoding="utf-8", newline="\n")
    (ROOT / f"math2_{YEAR}_answers.md").write_text(annual_answers_md(QUESTIONS), encoding="utf-8", newline="\n")

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
    (ROOT / "paper_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
