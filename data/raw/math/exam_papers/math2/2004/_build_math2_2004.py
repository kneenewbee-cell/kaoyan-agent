from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parent
YEAR = 2004


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
    Question(1, "fill_blank", 4, "高等数学", ["极限", "间断点"],
        md(r"""
        设
        $$
        f(x)=\lim_{n\to\infty}\frac{(n-1)x}{nx^2+1},
        $$
        则 $f(x)$ 的间断点为 $x=\underline{\qquad}$。
        """),
        "$0$",
        md(r"""
        当 $x=0$ 时，显然 $f(0)=0$。当 $x\neq 0$ 时，
        $$
        f(x)=\lim_{n\to\infty}\frac{(n-1)x}{nx^2+1}
        =\lim_{n\to\infty}\frac{1-\frac1n}{x+\frac{1}{nx}}=\frac1x.
        $$
        因而
        $$
        f(x)=\begin{cases}
        0,&x=0,\\[2mm]
        \dfrac1x,&x\ne 0.
        \end{cases}
        $$
        由 $\lim_{x\to 0}f(x)$ 不存在可知，$x=0$ 是间断点。
        """),
        ["images/source_pages/page-1.png"]),
    Question(2, "fill_blank", 4, "高等数学", ["参数方程", "曲线凹凸性"],
        md(r"""
        设函数 $y=y(x)$ 由参数方程
        $$
        \begin{cases}
        x=t^3+3t+1,\\
        y=t^3-3t+1
        \end{cases}
        $$
        确定，则曲线 $y=y(x)$ 向上凸的 $x$ 的取值范围为 $\underline{\qquad}$。
        """),
        "$(-\infty,1)$",
        md(r"""
        由参数方程可得
        $$
        \frac{dy}{dx}=\frac{dy/dt}{dx/dt}=\frac{3t^2-3}{3t^2+3}=\frac{t^2-1}{t^2+1}.
        $$
        再求二阶导数：
        $$
        \frac{d^2y}{dx^2}
        =\frac{d}{dt}\!\left(\frac{t^2-1}{t^2+1}\right)\Big/\frac{dx}{dt}
        =\frac{4t}{3(t^2+1)^3}.
        $$
        向上凸对应 $\dfrac{d^2y}{dx^2}<0$，故 $t<0$。又
        $$
        x=t^3+3t+1
        $$
        单调递增，且 $t=0$ 时 $x=1$，所以 $t<0$ 等价于 $x<1$。
        """),
        ["images/source_pages/page-1.png"]),
    Question(3, "fill_blank", 4, "高等数学", ["广义积分", "变量代换"],
        md(r"""
        计算
        $$
        \int_1^{+\infty}\frac{dx}{x\sqrt{x^2-1}}=\underline{\qquad}.
        $$
        """),
        "$\dfrac{\pi}{2}$",
        md(r"""
        令 $x=\sec t$，则
        $$
        dx=\sec t\tan t\,dt,\qquad \sqrt{x^2-1}=\tan t.
        $$
        当 $x=1$ 时 $t=0$，当 $x\to+\infty$ 时 $t\to \dfrac{\pi}{2}$，故
        $$
        \int_1^{+\infty}\frac{dx}{x\sqrt{x^2-1}}
        =\int_0^{\pi/2}dt
        =\frac{\pi}{2}.
        $$
        """),
        ["images/source_pages/page-1.png"]),
    Question(4, "fill_blank", 4, "高等数学", ["隐函数", "偏导数"],
        md(r"""
        设函数 $z=z(x,y)$ 由方程
        $$
        z=e^{2x-3z}+2y
        $$
        确定，则
        $$
        3\frac{\partial z}{\partial x}+\frac{\partial z}{\partial y}=\underline{\qquad}.
        $$
        """),
        "$2$",
        md(r"""
        设
        $$
        F(x,y,z)=z-e^{2x-3z}-2y=0.
        $$
        则
        $$
        F_x=-2e^{2x-3z},\quad F_y=-2,\quad F_z=1+3e^{2x-3z}.
        $$
        因此
        $$
        z_x=-\frac{F_x}{F_z}=\frac{2e^{2x-3z}}{1+3e^{2x-3z}},\qquad
        z_y=-\frac{F_y}{F_z}=\frac{2}{1+3e^{2x-3z}}.
        $$
        从而
        $$
        3z_x+z_y=\frac{6e^{2x-3z}+2}{1+3e^{2x-3z}}=2.
        $$
        """),
        ["images/source_pages/page-1.png"]),
    Question(5, "fill_blank", 4, "高等数学", ["一阶微分方程", "初值问题"],
        md(r"""
        微分方程
        $$
        (y+x^3)\,dx-2x\,dy=0
        $$
        满足 $y\vert_{x=1}=\dfrac65$ 的特解为 $\underline{\qquad}$。
        """),
        "$y=x^3+\dfrac15\sqrt{x}$",
        md(r"""
        原方程可化为
        $$
        \frac{dy}{dx}-\frac{1}{2x}y=\frac{x^2}{2}.
        $$
        先求齐次方程，得
        $$
        y_h=C\sqrt{x}.
        $$
        设特解为 $y_p=ax^3$，代入得 $a=1$，故通解为
        $$
        y=x^3+C\sqrt{x}.
        $$
        由条件 $y(1)=\dfrac65$ 可得 $C=\dfrac15$，故特解为
        $$
        y=x^3+\frac15\sqrt{x}.
        $$
        """),
        ["images/source_pages/page-1.png"]),
    Question(6, "fill_blank", 4, "线性代数", ["伴随矩阵", "行列式"],
        md(r"""
        设矩阵
        $$
        A=\begin{pmatrix}
        2&1&0\\
        1&2&0\\
        0&0&1
        \end{pmatrix},
        $$
        矩阵 $B$ 满足 $ABA^*=2BA^*+E$，其中 $A^*$ 为 $A$ 的伴随矩阵，$E$ 是单位矩阵，则 $|B|=\underline{\qquad}$。
        """),
        "$\dfrac19$",
        md(r"""
        设 $C=BA^*$，则题设化为
        $$
        AC=2C+E,
        $$
        即
        $$
        (A-2E)C=E.
        $$
        由于
        $$
        A-2E=\begin{pmatrix}
        0&1&0\\
        1&0&0\\
        0&0&-1
        \end{pmatrix}
        $$
        可逆，且其行列式为 $1$，故 $|C|=1$。又
        $$
        C=BA^* \quad\Rightarrow\quad |C|=|B|\cdot|A^*|.
        $$
        由 $|A|=3$ 且 $A$ 为 $3$ 阶矩阵，知
        $$
        |A^*|=|A|^{2}=9.
        $$
        因而
        $$
        |B|=\frac{|C|}{|A^*|}=\frac19.
        $$
        """),
        ["images/source_pages/page-1.png"]),
    Question(7, "single_choice", 4, "高等数学", ["无穷小比较", "定积分估计"],
        md(r"""
        把 $x\to 0^+$ 时的无穷小量
        $$
        \alpha=\int_0^x\cos(t^2)\,dt,\quad
        \beta=\int_0^{x^2}\tan\sqrt{t}\,dt,\quad
        \gamma=\int_0^{\sqrt{x}}\sin(t^3)\,dt
        $$
        排列起来，使排在后面的是前一个的高阶无穷小，则正确的排列次序是（ ）。

        A. $\alpha,\beta,\gamma$

        B. $\alpha,\gamma,\beta$

        C. $\beta,\alpha,\gamma$

        D. $\beta,\gamma,\alpha$
        """),
        "B",
        md(r"""
        当 $x\to 0^+$ 时，
        $$
        \alpha\sim\int_0^x1\,dt=x.
        $$
        对 $\beta$ 令 $u=\sqrt t$，得
        $$
        \beta=2\int_0^x u\tan u\,du\sim 2\int_0^x u^2\,du=\frac23x^3.
        $$
        而
        $$
        \gamma\sim\int_0^{\sqrt x}t^3\,dt=\frac14x^2.
        $$
        所以
        $$
        \alpha\gg \gamma\gg \beta,
        $$
        即排列为 $\alpha,\gamma,\beta$。
        """),
        ["images/source_pages/page-1.png"]),
    Question(8, "single_choice", 4, "高等数学", ["极值", "拐点"],
        md(r"""
        设
        $$
        f(x)=|x(1-x)|,
        $$
        则（ ）。

        A. $x=0$ 是 $f(x)$ 的极值点，但 $(0,0)$ 不是曲线 $y=f(x)$ 的拐点

        B. $x=0$ 不是 $f(x)$ 的极值点，但 $(0,0)$ 是曲线 $y=f(x)$ 的拐点

        C. $x=0$ 是 $f(x)$ 的极值点，且 $(0,0)$ 是曲线 $y=f(x)$ 的拐点

        D. $x=0$ 不是 $f(x)$ 的极值点，$(0,0)$ 也不是曲线 $y=f(x)$ 的拐点
        """),
        "C",
        md(r"""
        在 $x<0$ 时，
        $$
        f(x)=x^2-x;
        $$
        在 $0\le x\le 1$ 时，
        $$
        f(x)=x-x^2.
        $$
        因为 $f(0)=0$ 且其邻域内 $f(x)\ge 0$，所以 $x=0$ 为极小值点。又
        $$
        f''(x)=\begin{cases}
        2,&x<0,\\
        -2,&0<x<1,
        \end{cases}
        $$
        凹凸性在 $x=0$ 左右发生改变，因此 $(0,0)$ 是拐点。
        """),
        ["images/source_pages/page-1.png"]),
    Question(9, "single_choice", 4, "高等数学", ["定积分", "黎曼和极限"],
        md(r"""
        $$
        \lim_{n\to\infty}\ln\sqrt[n]{\left(1+\frac1n\right)^2\left(1+\frac2n\right)^2\cdots\left(1+\frac nn\right)^2}
        $$
        等于（ ）。

        A. $\displaystyle\int_1^2\ln^2x\,dx$

        B. $\displaystyle 2\int_1^2\ln x\,dx$

        C. $\displaystyle 2\int_1^2\ln(1+x)\,dx$

        D. $\displaystyle \int_1^2\ln^2(1+x)\,dx$
        """),
        "B",
        md(r"""
        设所求极限为 $L$，则
        $$
        L=\lim_{n\to\infty}\frac{2}{n}\sum_{k=1}^n\ln\left(1+\frac{k}{n}\right).
        $$
        这是函数 $\ln(1+x)$ 在 $[0,1]$ 上的黎曼和，因此
        $$
        L=2\int_0^1\ln(1+x)\,dx
        =2\int_1^2\ln x\,dx.
        $$
        故选 B。
        """),
        ["images/source_pages/page-1.png"]),
    Question(10, "single_choice", 4, "高等数学", ["导数定义", "局部单调性"],
        md(r"""
        设函数 $f(x)$ 连续，且 $f'(0)>0$，则存在 $\delta>0$，使得（ ）。

        A. $f(x)$ 在 $(0,\delta)$ 内单调增加

        B. $f(x)$ 在 $(-\delta,0)$ 内单调减少

        C. 对任意的 $x\in(0,\delta)$ 有 $f(x)>f(0)$

        D. 对任意的 $x\in(-\delta,0)$ 有 $f(x)>f(0)$
        """),
        "C",
        md(r"""
        由 $f'(0)>0$，根据导数定义，存在 $\delta>0$，当 $0<|x|<\delta$ 时有
        $$
        \frac{f(x)-f(0)}{x}>0.
        $$
        因而对 $x\in(0,\delta)$，有 $f(x)-f(0)>0$，即 $f(x)>f(0)$。故 C 正确。
        """),
        ["images/source_pages/page-1.png"]),
    Question(11, "single_choice", 4, "高等数学", ["常系数微分方程", "待定系数法"],
        md(r"""
        微分方程
        $$
        y''+y=x^2+1+\sin x
        $$
        的特解形式可设为（ ）。

        A. $y^*=ax^2+bx+c+x(A\sin x+B\cos x)$

        B. $y^*=x(ax^2+bx+c+A\sin x+B\cos x)$

        C. $y^*=ax^2+bx+c+A\sin x$

        D. $y^*=ax^2+bx+c+A\cos x$
        """),
        "A",
        md(r"""
        对多项式项 $x^2+1$，特解可设为 $ax^2+bx+c$。齐次方程
        $$
        y''+y=0
        $$
        的解为 $\sin x,\cos x$，右端含有共振项 $\sin x$，故对应特解应补乘 $x$，设为
        $$
        x(A\sin x+B\cos x).
        $$
        合并得应选 A。
        """),
        ["images/source_pages/page-2.png"]),
    Question(12, "single_choice", 4, "高等数学", ["二重积分", "极坐标变换"],
        md(r"""
        设函数 $f(u)$ 连续，区域
        $$
        D=\{(x,y)\mid x^2+y^2\le 2y\},
        $$
        则
        $$
        \iint_Df(xy)\,dxdy
        $$
        等于（ ）。

        A. $\displaystyle \int_{-1}^{1}dx\int_{-\sqrt{1-x^2}}^{\sqrt{1-x^2}}f(xy)\,dy$

        B. $\displaystyle 2\int_0^2dy\int_0^{\sqrt{2y-y^2}}f(xy)\,dx$

        C. $\displaystyle \int_0^\pi d\theta\int_0^{2\sin\theta}f(r^2\sin\theta\cos\theta)\,dr$

        D. $\displaystyle \int_0^\pi d\theta\int_0^{2\sin\theta}f(r^2\sin\theta\cos\theta)\,rdr$
        """),
        "D",
        md(r"""
        由
        $$
        x^2+y^2\le 2y
        $$
        可知该区域是圆 $x^2+(y-1)^2\le 1$。在极坐标下，
        $$
        r^2\le 2r\sin\theta \quad\Rightarrow\quad 0\le r\le 2\sin\theta,\quad 0\le \theta\le \pi.
        $$
        又
        $$
        xy=r^2\sin\theta\cos\theta,\qquad dxdy=r\,dr\,d\theta.
        $$
        因此应选 D。
        """),
        ["images/source_pages/page-2.png"]),
    Question(13, "single_choice", 4, "线性代数", ["初等矩阵", "列变换"],
        md(r"""
        设 $A$ 是 $3$ 阶方阵，将 $A$ 的第 $1$ 列与第 $2$ 列交换得 $B$，再把 $B$ 的第 $2$ 列加到第 $3$ 列得 $C$，则满足 $AQ=C$ 的可逆矩阵 $Q$ 为（ ）。

        A. $\begin{pmatrix}0&1&0\\1&0&0\\1&0&1\end{pmatrix}$

        B. $\begin{pmatrix}0&1&0\\1&0&1\\0&0&1\end{pmatrix}$

        C. $\begin{pmatrix}0&1&0\\1&0&0\\0&1&1\end{pmatrix}$

        D. $\begin{pmatrix}0&1&1\\1&0&0\\0&0&1\end{pmatrix}$
        """),
        "D",
        md(r"""
        交换第 $1$、$2$ 列相当于右乘
        $$
        S=\begin{pmatrix}
        0&1&0\\
        1&0&0\\
        0&0&1
        \end{pmatrix}.
        $$
        再把第 $2$ 列加到第 $3$ 列，相当于右乘
        $$
        T=\begin{pmatrix}
        1&0&0\\
        0&1&1\\
        0&0&1
        \end{pmatrix}.
        $$
        所以
        $$
        C=AST=A(ST),
        $$
        从而
        $$
        Q=ST=\begin{pmatrix}
        0&1&1\\
        1&0&0\\
        0&0&1
        \end{pmatrix}.
        $$
        """),
        ["images/source_pages/page-2.png"]),
    Question(14, "single_choice", 4, "线性代数", ["矩阵乘积", "线性相关"],
        md(r"""
        设 $A,B$ 为满足 $AB=0$ 的任意两个非零矩阵，则必有（ ）。

        A. $A$ 的列向量组线性相关，$B$ 的行向量组线性相关

        B. $A$ 的列向量组线性相关，$B$ 的列向量组线性相关

        C. $A$ 的行向量组线性相关，$B$ 的行向量组线性相关

        D. $A$ 的行向量组线性相关，$B$ 的列向量组线性相关
        """),
        "A",
        md(r"""
        由 $AB=0$ 且 $B\ne 0$，知 $B$ 至少有一个非零列向量 $\beta$ 满足
        $$
        A\beta=0.
        $$
        于是齐次方程组 $Ax=0$ 有非零解，故 $A$ 的列向量组线性相关。

        另一方面，由 $A\ne 0$，取 $A$ 的一个非零行向量组合作为系数，可得
        $$
        \alpha^\mathrm{T}B=0
        $$
        有非零系数解，因此 $B$ 的行向量组线性相关。故选 A。
        """),
        ["images/source_pages/page-2.png"]),
    Question(15, "solution", 10, "高等数学", ["极限", "洛必达法则"],
        md(r"""
        求极限
        $$
        \lim_{x\to 0}\frac{1}{x^3}\left[\left(\frac{2+\cos x}{3}\right)^x-1\right].
        $$
        """),
        "$-\dfrac16$",
        md(r"""
        设
        $$
        L=\lim_{x\to0}\frac{\left(\frac{2+\cos x}{3}\right)^x-1}{x^3}.
        $$
        先取对数化简指数：
        $$
        \left(\frac{2+\cos x}{3}\right)^x
        =\exp\!\left(x\ln\frac{2+\cos x}{3}\right).
        $$
        因此关键在于求
        $$
        \lim_{x\to0}\frac{1}{x^2}\ln\frac{2+\cos x}{3}.
        $$
        由 $\cos x=1-\dfrac{x^2}{2}+o(x^2)$，得
        $$
        \frac{2+\cos x}{3}=1-\frac{x^2}{6}+o(x^2),
        $$
        从而
        $$
        \ln\frac{2+\cos x}{3}=-\frac{x^2}{6}+o(x^2).
        $$
        所以
        $$
        x\ln\frac{2+\cos x}{3}=-\frac{x^3}{6}+o(x^3),
        $$
        进而
        $$
        \left(\frac{2+\cos x}{3}\right)^x-1=-\frac{x^3}{6}+o(x^3).
        $$
        故
        $$
        L=-\frac16.
        $$
        """),
        ["images/source_pages/page-2.png"]),
    Question(16, "solution", 10, "高等数学", ["函数递推定义", "可导性"],
        md(r"""
        设函数 $f(x)$ 在 $(-\infty,+\infty)$ 内有定义，在区间 $[0,2]$ 上
        $$
        f(x)=x(x^2-4),
        $$
        若对任意的 $x$ 都满足
        $$
        f(x)=k f(x+2),
        $$
        其中 $k$ 为常数。

        (I) 写出 $f(x)$ 在 $[-2,0)$ 上的表达式；

        (II) 问 $k$ 为何值时，$f(x)$ 在 $x=0$ 处可导。
        """),
        "在 $[-2,0)$ 上，$f(x)=k(x+2)x(x+4)$；且当 $k=-\dfrac12$ 时，$f(x)$ 在 $x=0$ 处可导。",
        md(r"""
        因为当 $-2\le x<0$ 时，$x+2\in[0,2)$，由题设递推关系
        $$
        f(x)=kf(x+2)=k(x+2)\bigl((x+2)^2-4\bigr)
        =k(x+2)x(x+4).
        $$
        这就得到
        $$
        f(x)=k(x+2)x(x+4),\qquad -2\le x<0.
        $$

        再讨论 $x=0$ 处可导性。右导数为
        $$
        f'_+(0)=\left[x(x^2-4)\right]'_{x=0}=-4.
        $$
        左导数由上式得
        $$
        f'_-(0)=\left[k(x+2)x(x+4)\right]'_{x=0}=8k.
        $$
        可导要求左右导数相等，故
        $$
        8k=-4\quad\Rightarrow\quad k=-\frac12.
        $$
        """),
        ["images/source_pages/page-2.png"]),
    Question(17, "solution", 11, "高等数学", ["变限积分", "周期函数"],
        md(r"""
        设
        $$
        f(x)=\int_x^{x+\frac{\pi}{2}}|\sin t|\,dt.
        $$

        (I) 证明 $f(x)$ 是以 $\pi$ 为周期的周期函数；

        (II) 求 $f(x)$ 的值域。
        """),
        "周期为 $\pi$；值域为 $\left[2-\sqrt2,\sqrt2\right]$。",
        md(r"""
        由 $|\sin(t+\pi)|=|\sin t|$，有
        $$
        f(x+\pi)=\int_{x+\pi}^{x+\frac{3\pi}{2}}|\sin t|\,dt.
        $$
        令 $u=t-\pi$，则
        $$
        f(x+\pi)=\int_x^{x+\frac{\pi}{2}}|\sin(u+\pi)|\,du
        =\int_x^{x+\frac{\pi}{2}}|\sin u|\,du=f(x),
        $$
        故 $f(x)$ 以 $\pi$ 为周期。

        只需在 $[0,\pi]$ 上求值域。由变上限积分求导公式，
        $$
        f'(x)=\left|\sin\left(x+\frac{\pi}{2}\right)\right|-|\sin x|
        =|\cos x|-|\sin x|.
        $$
        在 $[0,\pi]$ 上可解得驻点 $x=\dfrac{\pi}{4},\dfrac{3\pi}{4}$。
        分别计算：
        $$
        f\!\left(\frac{\pi}{4}\right)=\sqrt2,\qquad
        f\!\left(\frac{3\pi}{4}\right)=2-\sqrt2,
        $$
        且
        $$
        f(0)=f(\pi)=1.
        $$
        因而最大值为 $\sqrt2$，最小值为 $2-\sqrt2$，值域为
        $$
        \left[2-\sqrt2,\sqrt2\right].
        $$
        """),
        ["images/source_pages/page-2.png"]),
    Question(18, "solution", 12, "高等数学", ["旋转体", "极限"],
        md(r"""
        曲线
        $$
        y=\frac{e^x+e^{-x}}{2}
        $$
        与直线 $x=0,\ x=t\ (t>0)$ 及 $y=0$ 围成一曲边梯形。该曲边梯形绕 $x$ 轴旋转一周得一旋转体，其体积为 $V(t)$，侧面积为 $S(t)$，在 $x=t$ 处的底面积为 $F(t)$。

        (I) 求 $\dfrac{S(t)}{V(t)}$ 的值；

        (II) 计算极限 $\displaystyle\lim_{t\to+\infty}\dfrac{S(t)}{F(t)}$。
        """),
        "$\dfrac{S(t)}{V(t)}=2$；$\displaystyle\lim_{t\to+\infty}\dfrac{S(t)}{F(t)}=1$。",
        md(r"""
        记
        $$
        y=\frac{e^x+e^{-x}}{2}=\cosh x.
        $$
        则
        $$
        y'=\sinh x,\qquad 1+(y')^2=\cosh^2x=y^2.
        $$
        因而侧面积
        $$
        S(t)=2\pi\int_0^t y\sqrt{1+(y')^2}\,dx
        =2\pi\int_0^t y^2\,dx.
        $$
        体积
        $$
        V(t)=\pi\int_0^t y^2\,dx.
        $$
        所以
        $$
        \frac{S(t)}{V(t)}=2.
        $$

        又底面积为
        $$
        F(t)=\pi y(t)^2=\pi\cosh^2 t.
        $$
        因而
        $$
        \frac{S(t)}{F(t)}
        =\frac{2\int_0^t \cosh^2x\,dx}{\cosh^2 t}.
        $$
        当 $t\to+\infty$ 时，用主项估计 $\cosh^2x\sim \dfrac14e^{2x}$，于是
        $$
        2\int_0^t\cosh^2x\,dx\sim \frac14e^{2t},\qquad
        \cosh^2t\sim \frac14e^{2t},
        $$
        故
        $$
        \lim_{t\to+\infty}\frac{S(t)}{F(t)}=1.
        $$
        """),
        ["images/source_pages/page-3.png"]),
    Question(19, "proof", 12, "高等数学", ["中值定理", "函数不等式"],
        md(r"""
        设 $e<a<b<e^2$，证明
        $$
        \ln^2b-\ln^2a>\frac{4}{e^2}(b-a).
        $$
        """),
        "见解析",
        md(r"""
        设
        $$
        g(x)=\ln^2x.
        $$
        因为 $g$ 在 $[a,b]$ 上连续、在 $(a,b)$ 内可导，由拉格朗日中值定理，存在 $\xi\in(a,b)$，使
        $$
        \ln^2b-\ln^2a=g'(\xi)(b-a)=\frac{2\ln\xi}{\xi}(b-a).
        $$
        于是只需证明
        $$
        \frac{2\ln\xi}{\xi}>\frac4{e^2}.
        $$
        令
        $$
        h(x)=\frac{2\ln x}{x}.
        $$
        则
        $$
        h'(x)=\frac{2(1-\ln x)}{x^2}.
        $$
        在区间 $(e,e^2)$ 上有 $1<\ln x<2$，所以 $h'(x)<0$，即 $h$ 在 $(e,e^2)$ 上单调递减。
        又由于 $\xi\in(a,b)\subset(e,e^2)$，故
        $$
        h(\xi)>h(e^2)=\frac{2\ln(e^2)}{e^2}=\frac4{e^2}.
        $$
        从而
        $$
        \ln^2b-\ln^2a=\frac{2\ln\xi}{\xi}(b-a)>\frac4{e^2}(b-a).
        $$
        证毕。
        """),
        ["images/source_pages/page-3.png"]),
    Question(20, "solution", 11, "高等数学", ["微分方程应用", "牛顿第二定律"],
        md(r"""
        某种飞机在机场降落时，为了减少滑行距离，在触地的瞬间，飞机尾部张开减速伞，以增大阻力，使飞机迅速减速并停下。

        现有一质量为 $9000\text{kg}$ 的飞机，着陆时的水平速度为 $700\text{km/h}$。经测试，减速伞打开后，飞机所受的总阻力与飞机的速度成正比（比例系数为 $k=6.0\times 10^6$，单位按题意匹配）。问从着陆点算起，飞机滑行的最长距离是多少？
        """),
        "$1.05\text{ km}$",
        md(r"""
        设飞机速度为 $v(t)$，位移为 $x(t)$。由牛顿第二定律，
        $$
        m\frac{dv}{dt}=-kv.
        $$
        分离变量并积分，得
        $$
        v(t)=v_0e^{-kt/m},
        $$
        其中 $m=9000,\ v_0=700\text{ km/h}$。

        又
        $$
        \frac{dx}{dt}=v(t),
        $$
        所以从着陆到最终停下的总滑行距离为
        $$
        x_{\max}=\int_0^{+\infty}v_0e^{-kt/m}\,dt=\frac{mv_0}{k}.
        $$
        代入数据可得
        $$
        x_{\max}=1.05\text{ km}.
        $$
        """),
        ["images/source_pages/page-3.png"]),
    Question(21, "solution", 10, "高等数学", ["复合函数", "偏导数"],
        md(r"""
        设
        $$
        z=f(x^2-y^2,e^{xy}),
        $$
        其中 $f$ 具有连续二阶偏导数，求 $\dfrac{\partial z}{\partial x}$，$\dfrac{\partial z}{\partial y}$，$\dfrac{\partial^2 z}{\partial x\partial y}$。
        """),
        md(r"""
        设 $u=x^2-y^2,\ v=e^{xy}$，则
        $$
        z=f(u,v).
        $$
        有
        $$
        z_x=2x\,f_u+y e^{xy}f_v,
        \qquad
        z_y=-2y\,f_u+x e^{xy}f_v.
        $$
        进一步，
        $$
        z_{xy}
        =-4xy\,f_{uu}+2x^2e^{xy}f_{uv}-2y^2e^{xy}f_{uv}+e^{xy}f_v+xye^{xy}f_v+x y e^{2xy}f_{vv}.
        $$
        （其中 $f_u,f_v,f_{uu},f_{uv},f_{vv}$ 均取在 $(u,v)=(x^2-y^2,e^{xy})$ 处。）
        """),
        md(r"""
        设
        $$
        u=x^2-y^2,\qquad v=e^{xy},
        $$
        则
        $$
        u_x=2x,\ u_y=-2y,\ v_x=ye^{xy},\ v_y=xe^{xy}.
        $$
        因而
        $$
        z_x=f_u u_x+f_v v_x=2x\,f_u+y e^{xy}f_v,
        $$
        $$
        z_y=f_u u_y+f_v v_y=-2y\,f_u+x e^{xy}f_v.
        $$
        再对 $z_x$ 关于 $y$ 求导，得
        $$
        z_{xy}
        =2x(f_{uu}u_y+f_{uv}v_y)+e^{xy}f_v+y\!\left(f_{vu}u_y+f_{vv}v_y\right)e^{xy}+xy e^{xy}f_v.
        $$
        利用 $f_{uv}=f_{vu}$ 并代入各偏导，可整理为
        $$
        z_{xy}
        =-4xy\,f_{uu}+(2x^2-2y^2)e^{xy}f_{uv}+(1+xy)e^{xy}f_v+xye^{2xy}f_{vv}.
        $$
        """),
        ["images/source_pages/page-3.png"]),
    Question(22, "solution", 9, "线性代数", ["齐次线性方程组", "参数讨论"],
        md(r"""
        设有齐次线性方程组
        $$
        \begin{cases}
        (1+a)x_1+x_2+x_3+x_4=0,\\
        2x_1+(2+a)x_2+2x_3+2x_4=0,\\
        3x_1+3x_2+(3+a)x_3+3x_4=0,\\
        4x_1+4x_2+4x_3+(4+a)x_4=0,
        \end{cases}
        $$
        试问 $a$ 取何值时，该方程组有非零解，并求出其通解。
        """),
        "$a=0$ 或 $a=-10$；对应通解见解析。",
        md(r"""
        将方程组写成矩阵形式 $Ax=0$。注意到系数矩阵可写为
        $$
        A=aI+\begin{pmatrix}1\\2\\3\\4\end{pmatrix}(1,1,1,1).
        $$
        若记 $s=x_1+x_2+x_3+x_4$，则各方程统一写成
        $$
        ax_i+i\,s=0,\qquad i=1,2,3,4.
        $$

        要有非零解，必须使系数矩阵奇异。由矩阵行列式引理，
        $$
        \det A=a^4\left(1+\frac{1+2+3+4}{a}\right)=a^3(a+10).
        $$
        因而有非零解当且仅当
        $$
        a=0\quad\text{或}\quad a=-10.
        $$

        1. 当 $a=0$ 时，四个方程都化为
        $$
        x_1+x_2+x_3+x_4=0.
        $$
        取 $x_2,x_3,x_4$ 为自由变量，则
        $$
        x_1=-x_2-x_3-x_4.
        $$
        通解为
        $$
        x=c_1(-1,1,0,0)^\mathrm{T}+c_2(-1,0,1,0)^\mathrm{T}+c_3(-1,0,0,1)^\mathrm{T}.
        $$

        2. 当 $a=-10$ 时，由 $-10x_i+i\,s=0$ 得
        $$
        x_i=\frac{i}{10}s.
        $$
        于是
        $$
        x_1:x_2:x_3:x_4=1:2:3:4,
        $$
        通解为
        $$
        x=t(1,2,3,4)^\mathrm{T}.
        $$
        """),
        ["images/source_pages/page-3.png"]),
    Question(23, "solution", 9, "线性代数", ["特征值", "相似对角化"],
        md(r"""
        设矩阵
        $$
        A=\begin{pmatrix}
        1&2&-3\\
        -1&4&-3\\
        1&a&5
        \end{pmatrix}
        $$
        的特征方程有一个二重根，求 $a$ 的值，并讨论 $A$ 是否可相似对角化。
        """),
        "$a=-2$ 或 $a=-\dfrac23$；当 $a=-2$ 时可相似对角化，当 $a=-\dfrac23$ 时不可相似对角化。",
        md(r"""
        计算特征多项式：
        $$
        \det(\lambda E-A)=\lambda^3-10\lambda^2+(34+3a)\lambda-(36+6a).
        $$
        若其有二重根 $\lambda_0$，则 $\lambda_0$ 既满足特征方程，也满足导方程
        $$
        3\lambda^2-20\lambda+(34+3a)=0.
        $$
        消去 $a$ 后可得
        $$
        (\lambda_0-2)^2(\lambda_0-4)=0.
        $$
        因而二重根只能是 $\lambda_0=2$ 或 $\lambda_0=4$。

        1. 当 $\lambda_0=2$ 时，代回得
        $$
        a=-2.
        $$
        此时
        $$
        \chi_A(\lambda)=(\lambda-2)^2(\lambda-6).
        $$
        又
        $$
        A-2E=\begin{pmatrix}
        -1&2&-3\\
        -1&2&-3\\
        1&-2&3
        \end{pmatrix}
        $$
        的秩为 $1$，故特征值 $2$ 的特征子空间维数为 $2$，等于其代数重数，所以 $A$ 可相似对角化。

        2. 当 $\lambda_0=4$ 时，代回得
        $$
        a=-\frac23.
        $$
        此时
        $$
        \chi_A(\lambda)=(\lambda-4)^2(\lambda-2).
        $$
        检查 $A-4E$ 可知特征值 $4$ 只对应一个线性无关特征向量，其几何重数为 $1$，小于代数重数 $2$，因此 $A$ 不可相似对角化。
        """),
        ["images/source_pages/page-3.png"]),
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
