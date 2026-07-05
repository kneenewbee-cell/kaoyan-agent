from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parent
YEAR = 2007


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
    topic_lines = [f"  - {topic}" for topic in q.topics]
    asset_lines = [f"  - {asset}" for asset in q.assets]
    image_lines = [f"![题图](../{asset})" for asset in q.assets]
    return "\n".join(
        [
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
    )


def annual_questions_md(questions: list[Question]) -> str:
    lines = [
        f"# {YEAR} 年数学二真题",
        "",
        "资料类型：考研数学二历年真题",
        f"年份：{YEAR}",
        "科目：数学二",
        "整理状态：按原卷页图转写并校对。",
        "",
        "**第 1 页题面页图**",
        "",
        f"![{YEAR} 数学二第 1 页题面](images/source_pages/page-1.png)",
        "",
        "**第 2 页题面页图**",
        "",
        f"![{YEAR} 数学二第 2 页题面](images/source_pages/page-2.png)",
        "",
        "**第 3 页题面页图**",
        "",
        f"![{YEAR} 数学二第 3 页题面](images/source_pages/page-3.png)",
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
    return "\n".join(lines).rstrip() + "\n"


def annual_answers_md(questions: list[Question]) -> str:
    lines = [
        f"# Math 2 {YEAR} Answers",
        "",
        "资料类型：考研数学二答案解析",
        f"年份：{YEAR}",
        "科目：数学二",
        "整理状态：答案与解析依据答案册清洗整理，并与题面同步。",
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
    Question(1, "single_choice", 4, "高等数学", ["等价无穷小", "极限"],
        md(r"""
        当 $x\to0^+$ 时，与 $\sqrt{x}$ 等价的无穷小量是（  ）  
        (A) $1-e^{\sqrt{x}}$  
        (B) $\ln\dfrac{1+x}{1-\sqrt{x}}$  
        (C) $\sqrt{1+\sqrt{x}}-1$  
        (D) $1-\cos\sqrt{x}$
        """),
        "B",
        md(r"""
        分别考察各选项：
        $$
        1-e^{\sqrt{x}}\sim-\sqrt{x},\qquad
        \sqrt{1+\sqrt{x}}-1\sim \frac12\sqrt{x},\qquad
        1-\cos\sqrt{x}\sim \frac{x}{2}.
        $$
        而
        $$
        \ln\frac{1+x}{1-\sqrt{x}}
        =\ln\left(1+\frac{x+\sqrt{x}}{1-\sqrt{x}}\right)
        \sim \frac{x+\sqrt{x}}{1-\sqrt{x}}\sim \sqrt{x}.
        $$
        所以选 B。
        """),
        ["images/source_pages/page-1.png"]),
    Question(2, "single_choice", 4, "高等数学", ["间断点", "极限"],
        md(r"""
        函数
        $$
        f(x)=\frac{(e^{1/x}+e)\tan x}{x(e^{1/x}-e)}
        $$
        在 $[-\pi,\pi]$ 上的第一类间断点是 $x=$（  ）  
        (A) $0$  
        (B) $1$  
        (C) $-\dfrac{\pi}{2}$  
        (D) $\dfrac{\pi}{2}$
        """),
        "A",
        md(r"""
        先找出可能的间断点：$x=0,1,\pm \dfrac{\pi}{2}$。考察 $x=0$ 处左右极限：
        $$
        \lim_{x\to0^+}f(x)=1,\qquad \lim_{x\to0^-}f(x)=-1.
        $$
        左右极限都存在但不相等，因此 $x=0$ 是第一类间断点。
        其余几个点对应极限发散，为第二类间断点。
        """),
        ["images/source_pages/page-1.png"]),
    Question(3, "single_choice", 4, "高等数学", ["定积分应用", "奇偶性", "图像面积"],
        md(r"""
        如图，连续函数 $y=f(x)$ 在区间 $[-3,-2]$、$[2,3]$ 上的图形分别是直径为 $1$ 的上、下半圆弧，
        在区间 $[-2,0]$、$[0,2]$ 上的图形分别是直径为 $2$ 的下、上半圆弧。设
        $$
        F(x)=\int_0^x f(t)\,dt,
        $$
        则下列结论正确的是（  ）  
        (A) $F(3)=-\dfrac34F(-2)$  
        (B) $F(3)=\dfrac54F(2)$  
        (C) $F(-3)=\dfrac34F(2)$  
        (D) $F(-3)=-\dfrac54F(-2)$
        """),
        "C",
        md(r"""
        由图形知 $f$ 为奇函数，因此
        $$
        F(-x)=\int_0^{-x}f(t)\,dt=\int_0^x f(t)\,dt=F(x),
        $$
        所以 $F$ 为偶函数。
        又
        $$
        F(2)=\frac{\pi}{2},
        $$
        因为 $[0,2]$ 上是半径 $1$ 的上半圆面积。
        而 $[2,3]$ 上是半径 $\dfrac12$ 的下半圆，故
        $$
        \int_2^3 f(t)\,dt=-\frac{\pi}{8}.
        $$
        从而
        $$
        F(3)=F(2)-\frac{\pi}{8}=\frac{3\pi}{8}=\frac34F(2).
        $$
        再由偶性得
        $$
        F(-3)=F(3)=\frac34F(2).
        $$
        所以选 C。
        """),
        ["images/q003_diagram.png"]),
    Question(4, "single_choice", 4, "高等数学", ["连续", "可导", "命题判断"],
        md(r"""
        设函数 $f(x)$ 在 $x=0$ 处连续，下列命题错误的是（  ）  
        (A) 若 $\lim\limits_{x\to0}\dfrac{f(x)}{x}$ 存在，则 $f(0)=0$  
        (B) 若 $\lim\limits_{x\to0}\dfrac{f(x)+f(-x)}{x}$ 存在，则 $f(0)=0$  
        (C) 若 $\lim\limits_{x\to0}\dfrac{f(x)}{x}$ 存在，则 $f'(0)$ 存在  
        (D) 若 $\lim\limits_{x\to0}\dfrac{f(x)-f(-x)}{x}$ 存在，则 $f'(0)$ 存在
        """),
        "D",
        md(r"""
        (A) 中由连续性和
        $$
        \lim_{x\to0}\frac{f(x)}{x}
        $$
        存在可得 $f(0)=0$。于是 (C) 中
        $$
        f'(0)=\lim_{x\to0}\frac{f(x)-f(0)}{x}=\lim_{x\to0}\frac{f(x)}{x}
        $$
        也成立。
        对 (B)，若
        $$
        \lim_{x\to0}\frac{f(x)+f(-x)}{x}
        $$
        存在，则由连续性有 $f(x)+f(-x)\to2f(0)$，故必有 $f(0)=0$。
        (D) 不成立，例如 $f(x)=|x|$，则
        $$
        \frac{f(x)-f(-x)}{x}=0
        $$
        极限存在，但 $f'(0)$ 不存在。
        """),
        ["images/source_pages/page-1.png"]),
    Question(5, "single_choice", 4, "高等数学", ["渐近线"],
        md(r"""
        曲线
        $$
        y=\frac1x+\ln(1+e^x)
        $$
        渐近线的条数为（  ）  
        (A) $0$  
        (B) $1$  
        (C) $2$  
        (D) $3$
        """),
        "D",
        md(r"""
        当 $x\to0$ 时，$\dfrac1x\to\infty$，故 $x=0$ 是铅直渐近线。
        当 $x\to-\infty$ 时，
        $$
        \frac1x\to0,\qquad \ln(1+e^x)\to0,
        $$
        故 $y=0$ 是水平渐近线。
        当 $x\to+\infty$ 时，
        $$
        \ln(1+e^x)=x+\ln(1+e^{-x}),
        $$
        因而
        $$
        y-x=\frac1x+\ln(1+e^{-x})\to0,
        $$
        所以 $y=x$ 是斜渐近线。
        共 3 条。
        """),
        ["images/source_pages/page-1.png"]),
    Question(6, "single_choice", 4, "高等数学", ["数列", "拉格朗日中值定理"],
        md(r"""
        设函数 $f(x)$ 在 $(0,+\infty)$ 内具有二阶导数，且 $f''(x)>0$，令 $u_n=f(n)\ (n=1,2,\cdots)$，
        则下列结论正确的是（  ）  
        (A) 若 $u_1>u_2$，则 $\{u_n\}$ 必收敛  
        (B) 若 $u_1>u_2$，则 $\{u_n\}$ 必发散  
        (C) 若 $u_1<u_2$，则 $\{u_n\}$ 必收敛  
        (D) 若 $u_1<u_2$，则 $\{u_n\}$ 必发散
        """),
        "D",
        md(r"""
        由拉格朗日中值定理，
        $$
        u_{n+1}-u_n=f(n+1)-f(n)=f'(\xi_n),\qquad n<\xi_n<n+1.
        $$
        因 $f''(x)>0$，故 $f'(x)$ 严格递增，于是 $f'(\xi_n)$ 严格递增。
        若 $u_1<u_2$，则 $f'(\xi_1)=u_2-u_1>0$，从而对所有 $n$ 都有
        $$
        u_{n+1}-u_n=f'(\xi_n)\ge f'(\xi_1)>0.
        $$
        因此 $\{u_n\}$ 至少线性增长，必发散。故选 D。
        """),
        ["images/source_pages/page-1.png"]),
    Question(7, "single_choice", 4, "高等数学", ["可微", "充分条件"],
        md(r"""
        二元函数 $f(x,y)$ 在点 $(0,0)$ 处可微的一个充分条件是（  ）  
        (A) $\lim\limits_{(x,y)\to(0,0)}[f(x,y)-f(0,0)]=0$  
        (B) $\lim\limits_{x\to0}\dfrac{f(x,0)-f(0,0)}{x}=0$，且 $\lim\limits_{y\to0}\dfrac{f(0,y)-f(0,0)}{y}=0$  
        (C) $\lim\limits_{(x,y)\to(0,0)}\dfrac{f(x,y)-f(0,0)}{\sqrt{x^2+y^2}}=0$  
        (D) $\lim\limits_{x\to0}[f_x'(x,0)-f_x'(0,0)]=0$，且 $\lim\limits_{y\to0}[f_y'(0,y)-f_y'(0,0)]=0$
        """),
        "C",
        md(r"""
        选项 (C) 给出
        $$
        f(x,y)-f(0,0)=o\!\left(\sqrt{x^2+y^2}\right),
        $$
        即
        $$
        f(x,y)-f(0,0)=0\cdot x+0\cdot y+o(\rho),\qquad \rho=\sqrt{x^2+y^2},
        $$
        这正是可微定义中的一种形式，因此是充分条件。
        其余几项都不能单独保证全微分存在。
        """),
        ["images/source_pages/page-1.png"]),
    Question(8, "single_choice", 4, "高等数学", ["二重积分", "积分次序交换"],
        md(r"""
        设函数 $f(x,y)$ 连续，则二次积分
        $$
        \int_{\pi/2}^{\pi}dx\int_{\sin x}^{1}f(x,y)\,dy
        $$
        等于（  ）  
        (A) $\displaystyle\int_0^1dy\int_{\pi+\arcsin y}^{\pi}f(x,y)\,dx$  
        (B) $\displaystyle\int_0^1dy\int_{\pi-\arcsin y}^{\pi}f(x,y)\,dx$  
        (C) $\displaystyle\int_0^1dy\int_{\pi/2}^{\pi+\arcsin y}f(x,y)\,dx$  
        (D) $\displaystyle\int_0^1dy\int_{\pi/2}^{\pi-\arcsin y}f(x,y)\,dx$
        """),
        "B",
        md(r"""
        原积分区域为
        $$
        \frac{\pi}{2}\le x\le\pi,\qquad \sin x\le y\le1.
        $$
        固定 $y\in[0,1]$，由 $\sin x\le y$ 且 $x\in[\pi/2,\pi]$ 得
        $$
        x\in[\pi-\arcsin y,\ \pi].
        $$
        因而交换次序后为
        $$
        \int_0^1dy\int_{\pi-\arcsin y}^{\pi}f(x,y)\,dx.
        $$
        故选 B。
        """),
        ["images/source_pages/page-2.png"]),
    Question(9, "single_choice", 4, "线性代数", ["线性相关"],
        md(r"""
        设向量组 $\alpha_1,\alpha_2,\alpha_3$ 线性无关，则下列向量组线性相关的是（  ）  
        (A) $\alpha_1-\alpha_2,\ \alpha_2-\alpha_3,\ \alpha_3-\alpha_1$  
        (B) $\alpha_1+\alpha_2,\ \alpha_2+\alpha_3,\ \alpha_3+\alpha_1$  
        (C) $\alpha_1-2\alpha_2,\ \alpha_2-2\alpha_3,\ \alpha_3-2\alpha_1$  
        (D) $\alpha_1+2\alpha_2,\ \alpha_2+2\alpha_3,\ \alpha_3+2\alpha_1$
        """),
        "A",
        md(r"""
        对 (A) 中三向量直接相加：
        $$
        (\alpha_1-\alpha_2)+(\alpha_2-\alpha_3)+(\alpha_3-\alpha_1)=0.
        $$
        且系数不全为零，因此该向量组线性相关。
        其余三项都可写成原线性无关向量组右乘可逆矩阵的结果，故仍线性无关。
        """),
        ["images/source_pages/page-2.png"]),
    Question(10, "single_choice", 4, "线性代数", ["合同", "相似", "特征值"],
        md(r"""
        设矩阵
        $$
        A=\begin{pmatrix}
        2&-1&-1\\
        -1&2&-1\\
        -1&-1&2
        \end{pmatrix},\qquad
        B=\begin{pmatrix}
        1&0&0\\
        0&1&0\\
        0&0&0
        \end{pmatrix},
        $$
        则 $A$ 与 $B$（  ）  
        (A) 合同且相似  
        (B) 合同，但不相似  
        (C) 不合同，但相似  
        (D) 既不合同，也不相似
        """),
        "B",
        md(r"""
        由计算可得 $A$ 的特征值为 $3,3,0$，而 $B$ 的特征值为 $1,1,0$。
        因相似矩阵特征值必须完全相同，所以二者不相似。
        另一方面，$A,B$ 都是实对称矩阵，且正惯性指数都为 $2$、负惯性指数都为 $0$，
        因此按实对称矩阵合同判定准则，二者合同。
        故选 B。
        """),
        ["images/source_pages/page-2.png"]),
    Question(11, "fill_blank", 4, "高等数学", ["洛必达法则", "等价无穷小"],
        md(r"""
        $$
        \lim_{x\to0}\frac{\arctan x-\sin x}{x^3}=\underline{\qquad}.
        $$
        """),
        r"$-\dfrac16$",
        md(r"""
        展开
        $$
        \arctan x=x-\frac{x^3}{3}+o(x^3),\qquad \sin x=x-\frac{x^3}{6}+o(x^3).
        $$
        相减得
        $$
        \arctan x-\sin x=-\frac{x^3}{6}+o(x^3),
        $$
        故极限为
        $$
        -\frac16.
        $$
        """),
        ["images/source_pages/page-2.png"]),
    Question(12, "fill_blank", 4, "高等数学", ["参数方程", "法线"],
        md(r"""
        曲线
        $$
        \begin{cases}
        x=\cos t+\cos^2 t,\\
        y=1+\sin t
        \end{cases}
        $$
        上对应于 $t=\dfrac{\pi}{4}$ 的点处的法线斜率为 $\underline{\qquad}$。
        """),
        r"$1+\sqrt2$",
        md(r"""
        有
        $$
        \frac{dy}{dx}=\frac{dy/dt}{dx/dt}
        =\frac{\cos t}{-\sin t-2\sin t\cos t}.
        $$
        当 $t=\dfrac{\pi}{4}$ 时，
        $$
        \frac{dy}{dx}=-\frac{1}{1+\sqrt2}.
        $$
        法线斜率是其负倒数，所以为
        $$
        1+\sqrt2.
        $$
        """),
        ["images/source_pages/page-2.png"]),
    Question(13, "fill_blank", 4, "高等数学", ["高阶导数", "求导公式"],
        md(r"""
        设函数
        $$
        y=\frac{1}{2x+3},
        $$
        则 $y^{(n)}(0)=\underline{\qquad}$。
        """),
        r"$\dfrac{(-1)^n2^n n!}{3^{n+1}}$",
        md(r"""
        写成
        $$
        y=(2x+3)^{-1}.
        $$
        连续求导可得一般式
        $$
        y^{(n)}(x)=(-1)^n2^n n!(2x+3)^{-n-1}.
        $$
        令 $x=0$，即得
        $$
        y^{(n)}(0)=\frac{(-1)^n2^n n!}{3^{n+1}}.
        $$
        """),
        ["images/source_pages/page-2.png"]),
    Question(14, "fill_blank", 4, "高等数学", ["常系数微分方程"],
        md(r"""
        二阶常系数非齐次线性微分方程
        $$
        y''-4y'+3y=2e^{2x}
        $$
        的通解为 $\underline{\qquad}$。
        """),
        r"$y=C_1e^x+C_2e^{3x}-2e^{2x}$",
        md(r"""
        先解齐次方程
        $$
        r^2-4r+3=0,
        $$
        得特征根 $r=1,3$，所以齐次解为
        $$
        y_h=C_1e^x+C_2e^{3x}.
        $$
        对非齐次项设特解 $y^*=Ae^{2x}$，代入得
        $$
        (4A-8A+3A)e^{2x}=2e^{2x},
        $$
        故 $A=-2$。所以通解为
        $$
        y=C_1e^x+C_2e^{3x}-2e^{2x}.
        $$
        """),
        ["images/source_pages/page-2.png"]),
    Question(15, "fill_blank", 4, "高等数学", ["多元复合函数求导"],
        md(r"""
        设 $f(u,v)$ 是二元可微函数，$z=f\!\left(\dfrac{y}{x},\dfrac{x}{y}\right)$，则
        $$
        x\frac{\partial z}{\partial x}-y\frac{\partial z}{\partial y}=\underline{\qquad}.
        $$
        """),
        r"$2\left(-\dfrac{y}{x}f_1'+\dfrac{x}{y}f_2'\right)$",
        md(r"""
        设
        $$
        u=\frac{y}{x},\qquad v=\frac{x}{y},\qquad z=f(u,v).
        $$
        由链式法则，
        $$
        z_x=f_1'u_x+f_2'v_x=f_1'\!\left(-\frac{y}{x^2}\right)+f_2'\frac1y,
        $$
        $$
        z_y=f_1'u_y+f_2'v_y=f_1'\frac1x+f_2'\!\left(-\frac{x}{y^2}\right).
        $$
        因而
        $$
        xz_x-yz_y
        =2\left(-\frac{y}{x}f_1'+\frac{x}{y}f_2'\right).
        $$
        """),
        ["images/source_pages/page-2.png"]),
    Question(16, "fill_blank", 4, "线性代数", ["矩阵的秩", "幂矩阵"],
        md(r"""
        设矩阵
        $$
        A=\begin{pmatrix}
        0&1&0&0\\
        0&0&1&0\\
        0&0&0&1\\
        0&0&0&0
        \end{pmatrix},
        $$
        则 $A^3$ 的秩为 $\underline{\qquad}$。
        """),
        r"$1$",
        md(r"""
        直接计算可得
        $$
        A^3=\begin{pmatrix}
        0&0&0&1\\
        0&0&0&0\\
        0&0&0&0\\
        0&0&0&0
        \end{pmatrix}.
        $$
        其非零行只有一行，因此
        $$
        r(A^3)=1.
        $$
        """),
        ["images/source_pages/page-2.png"]),
    Question(17, "solution", 10, "高等数学", ["反函数", "积分方程", "微分方程"],
        md(r"""
        设 $f(x)$ 是区间 $\left[0,\dfrac{\pi}{4}\right]$ 上的单调、可导函数，且满足
        $$
        \int_0^{f(x)}f^{-1}(t)\,dt=\int_0^x \frac{\cos t-\sin t}{\sin t+\cos t}\,dt,
        $$
        其中 $f^{-1}$ 是 $f$ 的反函数，求 $f(x)$。
        """),
        r"$f(x)=\ln(\sin x+\cos x)$",
        md(r"""
        对等式两边关于 $x$ 求导，左边由变上限积分与反函数关系得
        $$
        f^{-1}(f(x))f'(x)=x f'(x).
        $$
        右边导数为
        $$
        \frac{\cos x-\sin x}{\sin x+\cos x}.
        $$
        因而
        $$
        x f'(x)=\frac{\cos x-\sin x}{\sin x+\cos x}x,
        $$
        对 $x\ne0$ 可化为
        $$
        f'(x)=\frac{\cos x-\sin x}{\sin x+\cos x}.
        $$
        积分得
        $$
        f(x)=\ln(\sin x+\cos x)+C.
        $$
        令 $x=0$ 代回原式，两边都为 $0$，可得 $f(0)=0$，故 $C=0$。
        所以
        $$
        f(x)=\ln(\sin x+\cos x).
        $$
        """),
        ["images/source_pages/page-2.png"]),
    Question(18, "solution", 11, "高等数学", ["旋转体体积", "参数最值"],
        md(r"""
        设 $D$ 是位于曲线
        $$
        y=\sqrt{x}\,a^{-x/(2a)}\qquad(a>1,\ 0\le x<+\infty)
        $$
        下方、$x$ 轴上方的无界区域。  
        （I）求区域 $D$ 绕 $x$ 轴旋转一周所成旋转体的体积 $V(a)$；  
        （II）当 $a$ 为何值时，$V(a)$ 最小？并求此最小值。
        """),
        r"（I）$V(a)=\pi\left(\dfrac{a}{\ln a}\right)^2$；（II）$a=e$ 时最小，$V_{\min}=\pi e^2$",
        md(r"""
        由旋转体体积公式，
        $$
        V(a)=\pi\int_0^{+\infty}y^2\,dx
        =\pi\int_0^{+\infty}x\,a^{-x/a}\,dx.
        $$
        利用分部积分或指数积分公式可得
        $$
        V(a)=\pi\left(\frac{a}{\ln a}\right)^2.
        $$
        对其求导：
        $$
        V'(a)=2\pi\frac{a(\ln a-1)}{(\ln a)^3}.
        $$
        因此在 $a=e$ 时取极小值，且
        $$
        V_{\min}=V(e)=\pi e^2.
        $$
        """),
        ["images/source_pages/page-2.png"]),
    Question(19, "solution", 10, "高等数学", ["微分方程", "降阶"],
        md(r"""
        求微分方程
        $$
        y''(x+y'^2)=y'
        $$
        满足初始条件 $y(1)=y'(1)=1$ 的特解。
        """),
        r"$y=\dfrac23x^{3/2}+\dfrac13$",
        md(r"""
        令 $p=y'$，则 $y''=\dfrac{dp}{dx}$，原方程化为
        $$
        p'(x+p^2)=p.
        $$
        将 $x$ 看作 $p$ 的函数，有
        $$
        \frac{dx}{dp}-\frac1p x=p.
        $$
        这是关于 $x(p)$ 的一阶线性方程，解得
        $$
        x=p^2+Cp.
        $$
        由初值 $x=1,p=1$ 得 $C=0$，故
        $$
        p=\sqrt{x}.
        $$
        即
        $$
        y'=\sqrt{x}.
        $$
        再积分并用 $y(1)=1$，得
        $$
        y=\frac23x^{3/2}+\frac13.
        $$
        """),
        ["images/source_pages/page-3.png"]),
    Question(20, "solution", 11, "高等数学", ["隐函数", "复合函数求导"],
        md(r"""
        已知函数 $f(u)$ 具有二阶导数，且 $f'(0)=1$，函数 $y=y(x)$ 由方程
        $$
        y-xe^{y-1}=1
        $$
        所确定。设
        $$
        z=f(\ln y-\sin x),
        $$
        求
        $$
        \left.\frac{dz}{dx}\right|_{x=0},\qquad
        \left.\frac{d^2z}{dx^2}\right|_{x=0}.
        $$
        """),
        r"$\left.\dfrac{dz}{dx}\right|_{x=0}=0,\quad \left.\dfrac{d^2z}{dx^2}\right|_{x=0}=1$",
        md(r"""
        先由方程在 $x=0$ 时得
        $$
        y(0)=1.
        $$
        对
        $$
        y-xe^{y-1}=1
        $$
        求导，可得
        $$
        (2-y)y'=e^{y-1}.
        $$
        代入 $x=0,y=1$ 得
        $$
        y'(0)=1.
        $$
        再求一次导数，可得 $y''(0)=2$。
        设
        $$
        u=\ln y-\sin x,\qquad z=f(u).
        $$
        则
        $$
        \frac{dz}{dx}=f'(u)\left(\frac{y'}{y}-\cos x\right).
        $$
        在 $x=0$ 处，由 $u(0)=0,\ f'(0)=1,\ y(0)=1,\ y'(0)=1$ 得
        $$
        \left.\frac{dz}{dx}\right|_{x=0}=1\cdot(1-1)=0.
        $$
        再求导：
        $$
        \frac{d^2z}{dx^2}=f''(u)(u')^2+f'(u)u''.
        $$
        因 $u'(0)=0$，故第一项为 $0$；而
        $$
        u''(0)=\left(\frac{y''}{y}-\frac{(y')^2}{y^2}+\sin x\right)_{x=0}=2-1=1.
        $$
        所以
        $$
        \left.\frac{d^2z}{dx^2}\right|_{x=0}=f'(0)\cdot1=1.
        $$
        """),
        ["images/source_pages/page-3.png"]),
    Question(21, "proof", 11, "高等数学", ["罗尔定理", "存在性证明"],
        md(r"""
        设函数 $f(x),g(x)$ 在 $[a,b]$ 上连续，在 $(a,b)$ 内具有二阶导数且存在相等的最大值，
        $f(a)=g(a),\ f(b)=g(b)$，证明：存在 $\xi\in(a,b)$，使得
        $$
        f''(\xi)=g''(\xi).
        $$
        """),
        "见解析",
        md(r"""
        令
        $$
        \varphi(x)=f(x)-g(x).
        $$
        由题设，$f,g$ 在 $(a,b)$ 内分别取得相等的最大值，所以存在某个 $\eta\in(a,b)$ 使得
        $$
        \varphi(\eta)=0.
        $$
        又因
        $$
        \varphi(a)=f(a)-g(a)=0,\qquad \varphi(b)=f(b)-g(b)=0,
        $$
        故 $\varphi$ 在区间 $[a,\eta]$ 与 $[\eta,b]$ 上分别满足罗尔定理，于是存在
        $$
        \xi_1\in(a,\eta),\qquad \xi_2\in(\eta,b)
        $$
        使得
        $$
        \varphi'(\xi_1)=\varphi'(\xi_2)=0.
        $$
        再对 $\varphi'$ 在 $[\xi_1,\xi_2]$ 上应用罗尔定理，存在 $\xi\in(\xi_1,\xi_2)\subset(a,b)$ 使
        $$
        \varphi''(\xi)=0.
        $$
        即
        $$
        f''(\xi)=g''(\xi).
        $$
        """),
        ["images/source_pages/page-3.png"]),
    Question(22, "solution", 11, "高等数学", ["二重积分", "分区域积分", "极坐标"],
        md(r"""
        设二元函数
        $$
        f(x,y)=
        \begin{cases}
        x^2, & |x|+|y|\le1,\\[2mm]
        \dfrac{1}{\sqrt{x^2+y^2}}, & 1<|x|+|y|\le2,
        \end{cases}
        $$
        计算二重积分
        $$
        \iint_D f(x,y)\,d\sigma,
        $$
        其中
        $$
        D=\{(x,y)\mid |x|+|y|\le2\}.
        $$
        """),
        r"$\dfrac13+2\sqrt2\ln(3+2\sqrt2)$",
        md(r"""
        将区域分成
        $$
        D_1=\{|x|+|y|\le1\},\qquad D_2=\{1<|x|+|y|\le2\}.
        $$
        则
        $$
        \iint_D f(x,y)\,d\sigma=\iint_{D_1}x^2\,d\sigma+\iint_{D_2}\frac{1}{\sqrt{x^2+y^2}}\,d\sigma.
        $$
        第一部分利用关于坐标轴的对称性：
        $$
        \iint_{D_1}x^2\,d\sigma
        =4\int_0^1dx\int_0^{1-x}x^2\,dy
        =4\int_0^1x^2(1-x)\,dx=\frac13.
        $$
        第二部分在第一象限用极坐标，边界 $x+y=1,2$ 分别对应
        $$
        r=\frac{1}{\cos\theta+\sin\theta},\qquad
        r=\frac{2}{\cos\theta+\sin\theta},\qquad 0\le\theta\le\frac{\pi}{2}.
        $$
        因而
        $$
        \iint_{D_2}\frac{1}{\sqrt{x^2+y^2}}\,d\sigma
        =4\int_0^{\pi/2}\int_{1/(\cos\theta+\sin\theta)}^{2/(\cos\theta+\sin\theta)}dr\,d\theta
        =2\sqrt2\ln(3+2\sqrt2).
        $$
        所以结果为
        $$
        \frac13+2\sqrt2\ln(3+2\sqrt2).
        $$
        """),
        ["images/source_pages/page-3.png"]),
    Question(23, "solution", 11, "线性代数", ["线性方程组", "参数讨论"],
        md(r"""
        设线性方程组
        $$
        \begin{cases}
        x_1+x_2+x_3=0,\\
        x_1+2x_2+ax_3=0,\\
        x_1+4x_2+a^2x_3=0,
        \end{cases}
        $$
        与方程
        $$
        x_1+2x_2+x_3=a-1
        $$
        有公共解，求 $a$ 的值及所有公共解。
        """),
        r"$a=1$ 或 $a=2$；当 $a=1$ 时公共解为 $k(1,0,-1)^T$，当 $a=2$ 时公共解为 $(0,1,-1)^T$",
        md(r"""
        把附加方程并入原线性方程组，组成增广矩阵并作消元，可得可解条件
        $$
        (a-1)(a-2)=0.
        $$
        因而
        $$
        a=1\quad\text{或}\quad a=2.
        $$
        当 $a=1$ 时，方程组化为
        $$
        \begin{cases}
        x_1+x_2+x_3=0,\\
        x_2=0,
        \end{cases}
        $$
        所有公共解为
        $$
        k(1,0,-1)^T.
        $$
        当 $a=2$ 时，联立后解得
        $$
        x_2=1,\qquad x_3=-1,\qquad x_1=0,
        $$
        因而公共解为
        $$
        (0,1,-1)^T.
        $$
        """),
        ["images/source_pages/page-3.png"]),
    Question(24, "solution", 11, "线性代数", ["特征值", "特征向量", "矩阵多项式"],
        md(r"""
        设 $3$ 阶实对称矩阵 $A$ 的特征值为 $\lambda_1=1,\lambda_2=2,\lambda_3=-2$，
        $\alpha_1=(1,-1,1)^T$ 是 $A$ 的属于 $\lambda_1$ 的一个特征向量。记
        $$
        B=A^5-4A^3+E,
        $$
        其中 $E$ 为 $3$ 阶单位矩阵。  
        （I）验证 $\alpha_1$ 是矩阵 $B$ 的特征向量，并求 $B$ 的全部特征值与特征向量；  
        （II）求矩阵 $B$。
        """),
        r"（I）$B$ 的特征值为 $-2,1,1$；（II）$B=\begin{pmatrix}0&1&-1\\1&0&1\\-1&1&0\end{pmatrix}$",
        md(r"""
        设
        $$
        p(\lambda)=\lambda^5-4\lambda^3+1.
        $$
        因为 $\alpha_1$ 是 $A$ 的属于特征值 $1$ 的特征向量，所以
        $$
        B\alpha_1=p(A)\alpha_1=p(1)\alpha_1=-2\alpha_1,
        $$
        故 $\alpha_1$ 是 $B$ 的特征向量，属于特征值 $-2$。
        又由矩阵多项式的特征值映射性质，
        $$
        p(1)=-2,\qquad p(2)=1,\qquad p(-2)=1.
        $$
        所以 $B$ 的特征值为
        $$
        -2,1,1.
        $$
        由于 $B$ 为实对称矩阵，不同特征值对应特征向量正交。设属于特征值 $1$ 的向量为 $(x_1,x_2,x_3)^T$，
        则需满足与 $\alpha_1=(1,-1,1)^T$ 正交，即
        $$
        x_1-x_2+x_3=0.
        $$
        可取一组基
        $$
        \alpha_2=(-1,0,1)^T,\qquad \alpha_3=(1,1,0)^T.
        $$
        令 $P=(\alpha_1,\alpha_2,\alpha_3)$，则
        $$
        P^{-1}BP=\operatorname{diag}(-2,1,1).
        $$
        由此计算得
        $$
        B=\begin{pmatrix}
        0&1&-1\\
        1&0&1\\
        -1&1&0
        \end{pmatrix}.
        $$
        """),
        ["images/source_pages/page-3.png"]),
]


def main() -> None:
    (ROOT / "questions").mkdir(parents=True, exist_ok=True)

    for q in QUESTIONS:
        (ROOT / "questions" / f"q{q.number:03d}.md").write_text(build_card(q), encoding="utf-8")

    (ROOT / f"math2_{YEAR}_questions.md").write_text(annual_questions_md(QUESTIONS), encoding="utf-8")
    (ROOT / f"math2_{YEAR}_answers.md").write_text(annual_answers_md(QUESTIONS), encoding="utf-8")

    jsonl_lines = []
    question_ids = []
    for q in QUESTIONS:
        qid = f"kaoyan_math2_{YEAR}_q{q.number:03d}"
        question_ids.append(qid)
        jsonl_lines.append(
            json.dumps(
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
                    "card_path": f"questions/q{q.number:03d}.md",
                    "assets": q.assets,
                    "answer": q.answer,
                    "explanation": q.explanation,
                },
                ensure_ascii=False,
            )
        )
    (ROOT / "questions.jsonl").write_text("\n".join(jsonl_lines) + "\n", encoding="utf-8")

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
        "question_ids": question_ids,
        "generated_at": now_iso(),
        "paper_scope": "full paper",
        "review_status": "reviewed",
        "answer_status": "available",
        "explanation_status": "available",
    }
    (ROOT / "paper_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
