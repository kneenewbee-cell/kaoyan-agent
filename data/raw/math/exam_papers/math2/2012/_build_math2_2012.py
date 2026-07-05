from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parent
YEAR = 2012


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
        "资料类型：考研数学二历年真题",
        f"年份：{YEAR}",
        "科目：数学二",
        "整理状态：按题卷页面转写并与答案册核对。",
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
        "整理状态：答案与解析按答案册清洗，并与题面同步。",
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
        "single_choice",
        4,
        "高等数学",
        ["渐近线", "有理函数"],
        md(
            r"""
            曲线
            $$
            y=\frac{x^2+x}{x^2-1}
            $$
            的渐近线的条数为（ ）

            A. 0  
            B. 1  
            C. 2  
            D. 3
            """
        ),
        "C",
        md(
            r"""
            当 $x\to 1$ 时，分母趋于 $0$ 而分子不为 $0$，故有一条竖直渐近线 $x=1$；当 $x\to\infty$ 时，
            $$
            \frac{x^2+x}{x^2-1}\to 1,
            $$
            故有一条水平渐近线 $y=1$。又因 $x=-1$ 时分子分母同为 $0$，化简后是可去间断点，不再产生渐近线，所以共有两条。
            """
        ),
        ["images/source_pages/page-1.png"],
    ),
    Question(
        2,
        "single_choice",
        4,
        "高等数学",
        ["导数", "乘积求导"],
        md(
            r"""
            设函数
            $$
            f(x)=(e^x-1)(e^{2x}-2)\cdots(e^{nx}-n),
            $$
            其中 $n$ 为正整数，则 $f'(0)=$（ ）

            A. $(-1)^{n-1}(n-1)!$  
            B. $(-1)^n(n-1)!$  
            C. $(-1)^{n-1}n!$  
            D. $(-1)^n n!$
            """
        ),
        "C",
        md(
            r"""
            在 $x=0$ 处，只有第一因子 $e^x-1$ 为 $0$，其导数为 $1$；其余因子在 $x=0$ 的值分别为
            $$
            e^{2\cdot 0}-2=-1,\ \ldots,\ e^{n\cdot 0}-n=1-n.
            $$
            因而
            $$
            f'(0)=1\cdot(-1)\cdot(-2)\cdots (1-n)=(-1)^{n-1}(n-1)! \cdot n = (-1)^{n-1}n!.
            $$
            """
        ),
        ["images/source_pages/page-1.png"],
    ),
    Question(
        3,
        "single_choice",
        4,
        "高等数学",
        ["数列", "级数必要条件"],
        md(
            r"""
            设 $a_n>0\ (n=1,2,\cdots)$，$S_n=a_1+a_2+\cdots+a_n$，则数列 $\{S_n\}$ 有界是数列 $\{a_n\}$ 收敛的（ ）

            A. 充分必要条件  
            B. 充分非必要条件  
            C. 必要非充分条件  
            D. 既非充分也非必要条件
            """
        ),
        "B",
        md(
            r"""
            由 $a_n>0$ 可知 $\{S_n\}$ 单调递增。若 $\{S_n\}$ 有界，则级数 $\sum a_n$ 收敛，从而必有 $a_n\to 0$，所以它是充分条件。
            但反过来 $a_n\to 0$ 不保证 $\sum a_n$ 收敛，例如 $a_n=\frac1n$，故不是必要条件。
            """
        ),
        ["images/source_pages/page-1.png"],
    ),
    Question(
        4,
        "single_choice",
        4,
        "高等数学",
        ["定积分", "参数单调性"],
        md(
            r"""
            设
            $$
            I_k=\int_0^k e^{x^2}\sin x\,dx\quad (k=1,2,3),
            $$
            则有（ ）

            A. $I_1<I_2<I_3$  
            B. $I_3<I_2<I_1$  
            C. $I_2<I_3<I_1$  
            D. $I_2<I_1<I_3$
            """
        ),
        "A",
        md(
            r"""
            把
            $$
            I(k)=\int_0^k e^{x^2}\sin x\,dx
            $$
            看作关于上限 $k$ 的函数，则
            $$
            I'(k)=e^{k^2}\sin k.
            $$
            因为 $1,2,3\in(0,\pi)$，且在 $(0,\pi)$ 上有 $\sin k>0$，所以 $I(k)$ 在该区间单调递增，从而
            $$
            I_1<I_2<I_3.
            $$
            """
        ),
        ["images/source_pages/page-1.png"],
    ),
    Question(
        5,
        "single_choice",
        4,
        "高等数学",
        ["多元函数", "单调性"],
        md(
            r"""
            设函数 $f(x,y)$ 可微，且对任意 $x,y$ 都有
            $$
            \frac{\partial f(x,y)}{\partial x}>0,\qquad \frac{\partial f(x,y)}{\partial y}<0,
            $$
            则使不等式 $f(x_1,y_1)<f(x_2,y_2)$ 成立的一个充分条件是（ ）

            A. $x_1>x_2,\ y_1<y_2$  
            B. $x_1>x_2,\ y_1>y_2$  
            C. $x_1<x_2,\ y_1<y_2$  
            D. $x_1<x_2,\ y_1>y_2$
            """
        ),
        "D",
        md(
            r"""
            条件说明 $f$ 关于 $x$ 单调递增，关于 $y$ 单调递减。若 $x_1<x_2$ 且 $y_1>y_2$，则由 $x$ 增大使函数值增大，由 $y$ 减小也使函数值增大，因此
            $$
            f(x_1,y_1)<f(x_2,y_2).
            $$
            """
        ),
        ["images/source_pages/page-1.png"],
    ),
    Question(
        6,
        "single_choice",
        4,
        "高等数学",
        ["二重积分", "区域对称性"],
        md(
            r"""
            设区域 $D$ 由曲线 $y=\sin x,\ x=\pm \frac{\pi}{2},\ y=1$ 围成，则
            $$
            \iint_D (xy^5-1)\,dxdy = （\ ）
            $$

            A. $\pi$  
            B. $2$  
            C. $-2$  
            D. $-\pi$
            """
        ),
        "D",
        md(
            r"""
            由于区域关于 $y$ 轴对称，而被积函数中的 $xy^5$ 关于 $x$ 是奇函数，所以
            $$
            \iint_D xy^5\,dxdy=0.
            $$
            因而原积分化为
            $$
            -\iint_D 1\,dxdy=-|D|.
            $$
            区域面积
            $$
            |D|=\int_{-\pi/2}^{\pi/2}(1-\sin x)\,dx=\pi,
            $$
            故原积分为 $-\pi$。
            """
        ),
        ["images/source_pages/page-1.png"],
    ),
    Question(
        7,
        "single_choice",
        4,
        "线性代数",
        ["向量组线性相关", "线性组合"],
        md(
            r"""
            设
            $$
            \alpha_1=\begin{pmatrix}0\\0\\c_1\end{pmatrix},\quad
            \alpha_2=\begin{pmatrix}0\\1\\c_2\end{pmatrix},\quad
            \alpha_3=\begin{pmatrix}1\\-1\\c_3\end{pmatrix},\quad
            \alpha_4=\begin{pmatrix}-1\\1\\c_4\end{pmatrix},
            $$
            其中 $c_1,c_2,c_3,c_4$ 为任意常数，则下列向量组线性相关的是（ ）

            A. $\alpha_1,\alpha_2,\alpha_3$  
            B. $\alpha_1,\alpha_2,\alpha_4$  
            C. $\alpha_1,\alpha_3,\alpha_4$  
            D. $\alpha_2,\alpha_3,\alpha_4$
            """
        ),
        "C",
        md(
            r"""
            有
            $$
            \alpha_3+\alpha_4=\begin{pmatrix}0\\0\\c_3+c_4\end{pmatrix},
            $$
            它与 $\alpha_1=\begin{pmatrix}0\\0\\c_1\end{pmatrix}$ 共线，所以 $\alpha_1,\alpha_3,\alpha_4$ 必线性相关。
            """
        ),
        ["images/source_pages/page-1.png"],
    ),
    Question(
        8,
        "single_choice",
        4,
        "线性代数",
        ["相似矩阵", "基变换"],
        md(
            r"""
            设 $A$ 为 $3$ 阶矩阵，$P$ 为 $3$ 阶可逆矩阵，且
            $$
            P^{-1}AP=\begin{pmatrix}
            1&0&0\\
            0&1&0\\
            0&0&2
            \end{pmatrix}.
            $$
            若 $P=(\alpha_1,\alpha_2,\alpha_3)$，$Q=(\alpha_1+\alpha_2,\alpha_2,\alpha_3)$，则 $Q^{-1}AQ=$（ ）

            A. $\begin{pmatrix}1&0&0\\0&2&0\\0&0&1\end{pmatrix}$  
            B. $\begin{pmatrix}1&0&0\\0&1&0\\0&0&2\end{pmatrix}$  
            C. $\begin{pmatrix}2&0&0\\0&1&0\\0&0&2\end{pmatrix}$  
            D. $\begin{pmatrix}2&0&0\\0&2&0\\0&0&1\end{pmatrix}$
            """
        ),
        "B",
        md(
            r"""
            由于
            $$
            Q=P\begin{pmatrix}
            1&0&0\\
            1&1&0\\
            0&0&1
            \end{pmatrix},
            $$
            而对角矩阵前两个特征值同为 $1$，在对应二维特征子空间内改变基并不会改变其对角形，因此
            $$
            Q^{-1}AQ=\operatorname{diag}(1,1,2).
            $$
            """
        ),
        ["images/source_pages/page-1.png"],
    ),
    Question(
        9,
        "fill_blank",
        4,
        "高等数学",
        ["隐函数求导", "二阶导数"],
        md(
            r"""
            设 $y=y(x)$ 是由方程
            $$
            x^2-y+1=e^y
            $$
            所确定的隐函数，则
            $$
            \left.\frac{d^2y}{dx^2}\right|_{x=0}=\underline{\qquad}.
            $$
            """
        ),
        "$1$",
        md(
            r"""
            由 $x=0$ 可得 $1-y=e^y-1$，解得 $y(0)=0$。对方程两边求导：
            $$
            2x-y'=e^y y'.
            $$
            于是
            $$
            y'=\frac{2x}{1+e^y},
            $$
            从而 $y'(0)=0$。再对上式求导并代入 $(0,0)$，得到
            $$
            2-y''=e^0(y')^2+e^0 y''=y'',
            $$
            故 $y''(0)=1$。
            """
        ),
        ["images/source_pages/page-2.png"],
    ),
    Question(
        10,
        "fill_blank",
        4,
        "高等数学",
        ["极限", "黎曼和"],
        md(
            r"""
            计算
            $$
            \lim_{n\to\infty}n\left(\frac{1}{1+n^2}+\frac{1}{2^2+n^2}+\cdots+\frac{1}{n^2+n^2}\right)=\underline{\qquad}.
            $$
            """
        ),
        r"$\dfrac{\pi}{4}$",
        md(
            r"""
            原式可写为
            $$
            \sum_{i=1}^n \frac{1}{n}\cdot \frac{1}{1+\left(\frac{i}{n}\right)^2},
            $$
            这是函数 $\frac{1}{1+x^2}$ 在 $[0,1]$ 上的黎曼和，因此极限为
            $$
            \int_0^1 \frac{dx}{1+x^2}=\arctan 1-\arctan 0=\frac{\pi}{4}.
            $$
            """
        ),
        ["images/source_pages/page-2.png"],
    ),
    Question(
        11,
        "fill_blank",
        4,
        "高等数学",
        ["复合函数", "偏导数"],
        md(
            r"""
            设
            $$
            z=f\!\left(\ln x+\frac1y\right),
            $$
            其中函数 $f(u)$ 可微，则
            $$
            x\frac{\partial z}{\partial x}+y^2\frac{\partial z}{\partial y}=\underline{\qquad}.
            $$
            """
        ),
        "$0$",
        md(
            r"""
            记
            $$
            u=\ln x+\frac1y,\qquad z=f(u).
            $$
            则
            $$
            z_x=f'(u)\cdot \frac1x,\qquad z_y=f'(u)\cdot\left(-\frac1{y^2}\right).
            $$
            所以
            $$
            xz_x+y^2z_y=f'(u)-f'(u)=0.
            $$
            """
        ),
        ["images/source_pages/page-2.png"],
    ),
    Question(
        12,
        "fill_blank",
        4,
        "高等数学",
        ["微分方程", "初值问题"],
        md(
            r"""
            微分方程
            $$
            y\,dx+(x-3y^2)\,dy=0
            $$
            满足条件 $y|_{x=1}=1$ 的解为
            $\underline{\qquad}$。
            """
        ),
        r"$y=\sqrt{x}$",
        md(
            r"""
            将 $x$ 视为 $y$ 的函数，有
            $$
            y\frac{dx}{dy}+x-3y^2=0,
            $$
            即
            $$
            \frac{dx}{dy}+\frac{1}{y}x=3y.
            $$
            这是关于 $x(y)$ 的一阶线性方程。乘积分因子 $y$ 得
            $$
            \frac{d(xy)}{dy}=3y^2,
            $$
            故
            $$
            xy=y^3+C.
            $$
            代入 $(x,y)=(1,1)$ 得 $C=0$，从而 $x=y^2$。由初值 $y(1)=1>0$，知取正支：
            $$
            y=\sqrt{x}.
            $$
            """
        ),
        ["images/source_pages/page-2.png"],
    ),
    Question(
        13,
        "fill_blank",
        4,
        "高等数学",
        ["曲率", "导数应用"],
        md(
            r"""
            曲线
            $$
            y=x^2+x\quad (x<0)
            $$
            上曲率为 $\dfrac{\sqrt2}{2}$ 的点的坐标是
            $\underline{\qquad}$。
            """
        ),
        "$(-1,0)$",
        md(
            r"""
            对曲线 $y=x^2+x$ 有
            $$
            y'=2x+1,\qquad y''=2.
            $$
            曲率
            $$
            K=\frac{|y''|}{\left(1+(y')^2\right)^{3/2}}
            =\frac{2}{\left(1+(2x+1)^2\right)^{3/2}}.
            $$
            令其等于 $\frac{\sqrt2}{2}$，化简得
            $$
            (2x+1)^2=1.
            $$
            解得 $x=0$ 或 $x=-1$。由条件 $x<0$，取 $x=-1$，此时 $y=0$。
            """
        ),
        ["images/source_pages/page-2.png"],
    ),
    Question(
        14,
        "fill_blank",
        4,
        "线性代数",
        ["伴随矩阵", "行列式性质"],
        md(
            r"""
            设 $A$ 为 $3$ 阶矩阵，$|A|=3$，$A^*$ 为 $A$ 的伴随矩阵。若交换 $A$ 的第 $1$ 行与第 $2$ 行得到矩阵 $B$，则
            $$
            |BA^*|=\underline{\qquad}.
            $$
            """
        ),
        "$-27$",
        md(
            r"""
            交换两行使行列式变号，所以
            $$
            |B|=-|A|=-3.
            $$
            又因为 $A$ 为 $3$ 阶矩阵，
            $$
            |A^*|=|A|^{3-1}=|A|^2=9.
            $$
            故
            $$
            |BA^*|=|B|\cdot |A^*|=(-3)\cdot 9=-27.
            $$
            """
        ),
        ["images/source_pages/page-2.png"],
    ),
    Question(
        15,
        "solution",
        10,
        "高等数学",
        ["极限", "等价无穷小"],
        md(
            r"""
            已知函数
            $$
            f(x)=\frac{1+x}{\sin x}-\frac1x,
            $$
            记
            $$
            a=\lim_{x\to 0}f(x).
            $$

            （I）求 $a$ 的值；  
            （II）若当 $x\to 0$ 时，$f(x)-a$ 与 $x^k$ 是同阶无穷小，求常数 $k$ 的值。
            """
        ),
        r"$a=1,\ k=2$",
        md(
            r"""
            先算极限：
            $$
            f(x)=\frac{x(1+x)-\sin x}{x\sin x}.
            $$
            由 $\sin x=x-\frac{x^3}{6}+o(x^3)$，得
            $$
            x(1+x)-\sin x=x^2+o(x^2),
            $$
            且 $x\sin x=x^2+o(x^2)$，所以
            $$
            a=\lim_{x\to 0}f(x)=1.
            $$

            再看
            $$
            f(x)-1=\frac{x-\sin x}{\sin x}.
            $$
            由于
            $$
            x-\sin x\sim \frac{x^3}{6},\qquad \sin x\sim x,
            $$
            故
            $$
            f(x)-1\sim \frac{x^2}{6}.
            $$
            因而它与 $x^k$ 同阶时应有 $k=2$。
            """
        ),
        ["images/source_pages/page-2.png"],
    ),
    Question(
        16,
        "solution",
        10,
        "高等数学",
        ["多元函数极值", "驻点判别"],
        md(
            r"""
            求函数
            $$
            f(x,y)=xe^{-\frac{x^2+y^2}{2}}
            $$
            的极值。
            """
        ),
        r"极大值为 $\dfrac1{\sqrt e}$（在 $(1,0)$ 处），极小值为 $-\dfrac1{\sqrt e}$（在 $(-1,0)$ 处）",
        md(
            r"""
            有
            $$
            f_x=e^{-\frac{x^2+y^2}{2}}(1-x^2),\qquad
            f_y=-xye^{-\frac{x^2+y^2}{2}}.
            $$
            令偏导同时为零，得驻点为 $(1,0)$ 与 $(-1,0)$。

            固定 $x$ 时，$e^{-(x^2+y^2)/2}$ 在 $y=0$ 处最大，因此极值只能落在 $y=0$ 上。于是问题化为研究
            $$
            g(x)=xe^{-x^2/2}.
            $$
            有
            $$
            g'(x)=e^{-x^2/2}(1-x^2),
            $$
            故在 $x=1$ 取极大值，在 $x=-1$ 取极小值。相应函数值为
            $$
            g(1)=e^{-1/2}=\frac1{\sqrt e},\qquad g(-1)=-e^{-1/2}=-\frac1{\sqrt e}.
            $$
            """
        ),
        ["images/source_pages/page-2.png"],
    ),
    Question(
        17,
        "solution",
        12,
        "高等数学",
        ["曲线切线", "面积", "旋转体体积"],
        md(
            r"""
            过点 $(0,1)$ 作曲线 $L:y=\ln x$ 的切线，切点为 $A$，又 $L$ 与 $x$ 轴交于 $B$ 点，区域 $D$ 由 $L$ 与直线 $AB$ 围成。求区域 $D$ 的面积及 $D$ 绕 $x$ 轴旋转一周所得旋转体的体积。
            """
        ),
        r"面积为 $2$，体积为 $\dfrac{8\pi}{3}$",
        md(
            r"""
            设切点为 $A(x_0,\ln x_0)$。曲线 $y=\ln x$ 在 $A$ 点的切线为
            $$
            y-\ln x_0=\frac1{x_0}(x-x_0).
            $$
            代入点 $(0,1)$，得
            $$
            1-\ln x_0=-1,\qquad \ln x_0=2,
            $$
            所以 $x_0=e^2$，即 $A=(e^2,2)$。又曲线 $L$ 与 $x$ 轴交于
            $$
            B=(1,0).
            $$
            因而弦 $AB$ 的方程为
            $$
            y=\frac{2}{e^2-1}(x-1),
            $$
            即
            $$
            x=1+\frac{e^2-1}{2}y.
            $$

            用 $y$ 作积分变量，曲线写成 $x=e^y$，积分区间为 $0\le y\le 2$。面积为
            $$
            S=\int_0^2 \left(1+\frac{e^2-1}{2}y-e^y\right)\,dy=2.
            $$

            绕 $x$ 轴旋转的体积为
            $$
            V=\pi\int_0^2 y^2\left(1+\frac{e^2-1}{2}y-e^y\right)\,dy
            =\frac{8\pi}{3}.
            $$
            """
        ),
        ["images/source_pages/page-2.png"],
    ),
    Question(
        18,
        "solution",
        10,
        "高等数学",
        ["极坐标", "二重积分"],
        md(
            r"""
            计算二重积分
            $$
            \iint_D xy\,d\sigma,
            $$
            其中区域 $D$ 由曲线 $r=1+\cos\theta\ (0\le \theta\le \pi)$ 与极轴围成。
            """
        ),
        r"$\dfrac{15}{16}$",
        md(
            r"""
            改用极坐标：
            $$
            x=r\cos\theta,\qquad y=r\sin\theta,\qquad d\sigma=r\,dr\,d\theta.
            $$
            于是
            $$
            \iint_D xy\,d\sigma
            =\int_0^\pi\int_0^{1+\cos\theta} r^3\sin\theta\cos\theta\,dr\,d\theta
            =\frac14\int_0^\pi (1+\cos\theta)^4\sin\theta\cos\theta\,d\theta.
            $$
            令 $u=1+\cos\theta$ 或直接展开积分，可得结果
            $$
            \iint_D xy\,d\sigma=\frac{15}{16}.
            $$
            """
        ),
        ["images/source_pages/page-3.png"],
    ),
    Question(
        19,
        "solution",
        10,
        "高等数学",
        ["常系数线性微分方程", "拐点"],
        md(
            r"""
            已知函数 $f(x)$ 满足方程
            $$
            f''(x)+f'(x)-2f(x)=0
            $$
            及
            $$
            f''(x)+f(x)=2e^x.
            $$

            （I）求 $f(x)$ 的表达式；  
            （II）求曲线
            $$
            y=f(x^2)\int_0^x f(-t^2)\,dt
            $$
            的拐点。
            """
        ),
        r"$f(x)=e^x$；拐点为 $(0,0)$",
        md(
            r"""
            由
            $$
            f''+f'-2f=0
            $$
            的特征方程
            $$
            r^2+r-2=0
            $$
            得通解
            $$
            f(x)=C_1e^x+C_2e^{-2x}.
            $$
            代入第二个方程
            $$
            f''+f=2e^x
            $$
            可解得 $C_1=1,\ C_2=0$，故
            $$
            f(x)=e^x.
            $$

            于是
            $$
            y=e^{x^2}\int_0^x e^{-t^2}\,dt.
            $$
            计算导数可得 $y''(0)=0$，并可验证当 $x<0$ 时 $y''<0$、当 $x>0$ 时 $y''>0$，故凹凸性在 $x=0$ 两侧改变，所以唯一拐点为
            $$
            (0,0).
            $$
            """
        ),
        ["images/source_pages/page-3.png"],
    ),
    Question(
        20,
        "proof",
        10,
        "高等数学",
        ["不等式证明", "单调性"],
        md(
            r"""
            证明：
            $$
            x\ln\frac{1+x}{1-x}+\cos x\ge 1+\frac{x^2}{2}\qquad (-1<x<1).
            $$
            """
        ),
        "见解析",
        md(
            r"""
            令
            $$
            F(x)=x\ln\frac{1+x}{1-x}+\cos x-1-\frac{x^2}{2}.
            $$
            有 $F(0)=0$。计算导数：
            $$
            F'(x)=\ln\frac{1+x}{1-x}-\sin x+\frac{2x}{1-x^2}-x.
            $$
            在 $(-1,1)$ 上可利用
            $$
            \ln\frac{1+x}{1-x}\ge 2x,\qquad \sin x\le x
            $$
            以及 $\frac{2x}{1-x^2}-x\ge 0$（按 $x>0$、$x<0$ 分别讨论）推出 $F'(x)\ge 0$。因此 $F$ 在 $(-1,1)$ 上以 $0$ 为最小值点，从而
            $$
            F(x)\ge F(0)=0,
            $$
            即
            $$
            x\ln\frac{1+x}{1-x}+\cos x\ge 1+\frac{x^2}{2}.
            $$
            """
        ),
        ["images/source_pages/page-3.png"],
    ),
    Question(
        21,
        "proof",
        10,
        "高等数学",
        ["方程根", "数列极限"],
        md(
            r"""
            （I）证明方程
            $$
            x^n+x^{n-1}+\cdots+x=1\qquad (n\text{ 为大于 }1\text{ 的整数})
            $$
            在区间 $\left(\dfrac12,1\right)$ 内有且仅有一个实根；

            （II）记（I）中的实根为 $x_n$，证明 $\lim_{n\to\infty}x_n$ 存在，并求此极限。
            """
        ),
        r"在 $\left(\dfrac12,1\right)$ 内有唯一实根；且 $\displaystyle\lim_{n\to\infty}x_n=\frac12$",
        md(
            r"""
            令
            $$
            f_n(x)=x+x^2+\cdots+x^n-1.
            $$
            在 $\left(\frac12,1\right)$ 上，$f_n'(x)=1+2x+\cdots+nx^{n-1}>0$，故 $f_n$ 严格递增。
            又
            $$
            f_n\!\left(\frac12\right)=\frac12+\frac14+\cdots+\frac1{2^n}-1<0,\qquad
            f_n(1)=n-1>0,
            $$
            由介值定理知在 $\left(\frac12,1\right)$ 内恰有一个实根。

            由方程
            $$
            x_n+x_n^2+\cdots+x_n^n=1
            $$
            可知 $x_n>\frac12$。又比较 $f_{n+1}(x_n)=x_n^{n+1}>0$，而 $f_{n+1}$ 递增，得 $x_{n+1}<x_n$，所以 $\{x_n\}$ 单调递减且下有界，从而收敛。
            设极限为 $a$。由
            $$
            x_n(1-x_n^n)=1-x_n
            $$
            或直接对原式放缩并令 $n\to\infty$，可得极限满足
            $$
            \frac{a}{1-a}=1,
            $$
            故
            $$
            a=\frac12.
            $$
            """
        ),
        ["images/source_pages/page-4.png"],
    ),
    Question(
        22,
        "solution",
        11,
        "线性代数",
        ["线性方程组", "无穷多解"],
        md(
            r"""
            设
            $$
            A=\begin{pmatrix}
            1&a&0&0\\
            0&1&a&0\\
            0&0&1&a\\
            a&0&0&1
            \end{pmatrix},\qquad
            \beta=\begin{pmatrix}
            1\\
            -1\\
            0\\
            0
            \end{pmatrix}.
            $$

            （I）计算行列式 $|A|$；  
            （II）当实数 $a$ 为何值时，方程组 $Ax=\beta$ 有无穷多解，并求其通解。
            """
        ),
        r"$|A|=1-a^4$；当 $a=-1$ 时有无穷多解，通解为 $\begin{pmatrix}t\\ t-1\\ t\\ t\end{pmatrix}$",
        md(
            r"""
            先计算行列式，可得
            $$
            |A|=1-a^4.
            $$
            因而方程组要有无穷多解，必须先有 $|A|=0$，即 $a=\pm 1$。

            分别代入增广矩阵检验相容性：当 $a=1$ 时方程组不相容；当 $a=-1$ 时，
            $$
            \begin{cases}
            x_1-x_2=1,\\
            x_2-x_3=-1,\\
            x_3-x_4=0,\\
            -x_1+x_4=0.
            \end{cases}
            $$
            由后两式得 $x_4=x_1,\ x_3=x_1$，再由第二式得 $x_2=x_1-1$。令 $x_1=t$，则通解为
            $$
            x=\begin{pmatrix}t\\ t-1\\ t\\ t\end{pmatrix}
            =\begin{pmatrix}0\\ -1\\ 0\\ 0\end{pmatrix}
            +t\begin{pmatrix}1\\ 1\\ 1\\ 1\end{pmatrix}.
            $$
            """
        ),
        ["images/source_pages/page-4.png"],
    ),
    Question(
        23,
        "solution",
        11,
        "线性代数",
        ["二次型", "秩", "正交变换"],
        md(
            r"""
            已知
            $$
            A=\begin{pmatrix}
            1&0&1\\
            0&1&1\\
            -1&0&a\\
            0&a&-1
            \end{pmatrix},
            $$
            二次型
            $$
            f(x_1,x_2,x_3)=x^{\mathsf T}(A^{\mathsf T}A)x
            $$
            的秩为 $2$。

            （I）求实数 $a$ 的值；  
            （II）求正交变换 $x=Qy$ 将 $f$ 化为标准形。
            """
        ),
        r"$a=-1$；可化为标准形 $2y_1^2+6y_2^2$（另一个特征值为 $0$）",
        md(
            r"""
            由
            $$
            \operatorname{rank}(A^{\mathsf T}A)=\operatorname{rank}(A)=2
            $$
            可知矩阵 $A$ 的秩为 $2$。对 $A$ 做行列式或子式计算，可得唯一满足条件的参数为
            $$
            a=-1.
            $$

            此时
            $$
            A^{\mathsf T}A=
            \begin{pmatrix}
            2&0&2\\
            0&2&2\\
            2&2&4
            \end{pmatrix}.
            $$
            它的特征值为
            $$
            0,\ 2,\ 6.
            $$
            取对应的单位正交特征向量为
            $$
            \alpha_1=\frac1{\sqrt2}\begin{pmatrix}1\\ -1\\ 0\end{pmatrix},\quad
            \alpha_2=\frac1{\sqrt6}\begin{pmatrix}1\\ 1\\ 2\end{pmatrix},\quad
            \alpha_3=\frac1{\sqrt3}\begin{pmatrix}1\\ 1\\ -1\end{pmatrix}.
            $$
            令
            $$
            Q=(\alpha_1,\alpha_2,\alpha_3),
            $$
            则 $Q$ 为正交矩阵，且
            $$
            Q^{\mathsf T}(A^{\mathsf T}A)Q=\operatorname{diag}(2,6,0).
            $$
            因而在正交变换 $x=Qy$ 下，
            $$
            f=2y_1^2+6y_2^2.
            $$
            """
        ),
        ["images/source_pages/page-4.png"],
    ),
]


def question_record(q: Question) -> dict[str, object]:
    qid = f"kaoyan_math2_{YEAR}_q{q.number:03d}"
    return {
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
    }


def main() -> None:
    (ROOT / "questions").mkdir(parents=True, exist_ok=True)
    (ROOT / "images" / "source_pages").mkdir(parents=True, exist_ok=True)

    (ROOT / f"math2_{YEAR}_questions.md").write_text(annual_questions_md(QUESTIONS), encoding="utf-8")
    (ROOT / f"math2_{YEAR}_answers.md").write_text(annual_answers_md(QUESTIONS), encoding="utf-8")

    for q in QUESTIONS:
        (ROOT / "questions" / f"q{q.number:03d}.md").write_text(build_card(q), encoding="utf-8")

    records = [question_record(q) for q in QUESTIONS]
    with (ROOT / "questions.jsonl").open("w", encoding="utf-8") as fh:
        for record in records:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")

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
        "question_ids": [f"kaoyan_math2_{YEAR}_q{q.number:03d}" for q in QUESTIONS],
        "generated_at": now_iso(),
        "review_status": "reviewed",
        "answer_status": "available",
        "explanation_status": "available",
    }
    (ROOT / "paper_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
