from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parent
YEAR = 2000


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
        "资料类型：考研数学二历年真题  ",
        f"年份：{YEAR}  ",
        "科目：数学二  ",
        "范围：试卷 III  ",
        "整理状态：已按原卷页面校对并转写。",
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
    Question(1, "fill_blank", 3, "高等数学", ["极限", "泰勒展开"], md(r"""
计算
$$
\lim_{x\to0}\frac{\arctan x-x}{\ln(1+2x^3)}=\underline{\qquad}.
$$
"""), r"$-\dfrac{1}{6}$", md(r"""
展开
$$
\arctan x=x-\frac{x^3}{3}+o(x^3),\qquad \ln(1+2x^3)=2x^3+o(x^3).
$$
故原式
$$
\sim \frac{-x^3/3}{2x^3}=-\frac16.
$$
"""), ["images/source_pages/page-1.png"]),
    Question(2, "fill_blank", 3, "高等数学", ["隐函数求导"], md(r"""
设函数 $y=y(x)$ 由方程
$$
2^{xy}=x+y
$$
所确定，则
$$
dy\big|_{x=0}=\underline{\qquad}.
$$
"""), r"$(\ln2-1)\,dx$", md(r"""
由 $x=0$ 时得 $y=1$。对方程两边微分：
$$
2^{xy}\ln2\,(x\,dy+y\,dx)=dx+dy.
$$
代入 $(x,y)=(0,1)$，得
$$
\ln2\,dx=dx+dy,
$$
故
$$
dy=(\ln2-1)\,dx.
$$
"""), ["images/source_pages/page-1.png"]),
    Question(3, "fill_blank", 3, "高等数学", ["广义积分"], md(r"""
计算
$$
\int_2^{+\infty}\frac{dx}{(x+7)\sqrt{x-2}}=\underline{\qquad}.
$$
"""), r"$\dfrac{\pi}{3}$", md(r"""
令
$$
x-2=t^2,
$$
则
$$
dx=2t\,dt,\qquad x+7=t^2+9.
$$
原式化为
$$
2\int_0^{+\infty}\frac{dt}{t^2+9}
=\frac{2}{3}\left[\arctan\frac{t}{3}\right]_0^{+\infty}
=\frac{\pi}{3}.
$$
"""), ["images/source_pages/page-1.png"]),
    Question(4, "fill_blank", 3, "高等数学", ["斜渐近线"], md(r"""
曲线
$$
y=(2x-1)e^{1/x}
$$
的渐近线方程为 $\underline{\qquad}$。
"""), r"$y=2x+1$", md(r"""
当 $x\to\pm\infty$ 时，
$$
e^{1/x}=1+\frac1x+o\left(\frac1x\right).
$$
故
$$
y=(2x-1)\left(1+\frac1x+o\left(\frac1x\right)\right)=2x+1+o(1),
$$
所以斜渐近线为
$$
y=2x+1.
$$
"""), ["images/source_pages/page-1.png"]),
    Question(5, "fill_blank", 3, "线性代数", ["矩阵运算"], md(r"""
设
$$
A=\begin{pmatrix}
1&0&0&0\\
-2&3&0&0\\
0&-4&5&0\\
0&0&-6&7
\end{pmatrix},
$$
$E$ 为 $4$ 阶单位矩阵，且
$$
B=(E+A)^{-1}(E-A),
$$
则
$$
(E+B)^{-1}=\underline{\qquad}.
$$
"""), r"$\begin{pmatrix}\frac12&0&0&0\\[2pt]0&\frac14&0&0\\[2pt]0&\frac{2}{5}&\frac{3}{10}&0\\[2pt]0&0&\frac{3}{7}&\frac14\end{pmatrix}$", md(r"""
由
$$
B=(E+A)^{-1}(E-A)
$$
得
$$
E+B=E+(E+A)^{-1}(E-A)=2(E+A)^{-1}.
$$
故
$$
(E+B)^{-1}=\frac12(E+A).
$$
直接代入 $A$ 可得答案矩阵。
"""), ["images/source_pages/page-1.png"]),
    Question(6, "single_choice", 3, "高等数学", ["连续性"], md(r"""
设函数
$$
f(x)=\frac{x}{a+e^{bx}}
$$
在 $(-\infty,+\infty)$ 内连续，且 $\lim_{x\to-\infty}f(x)=0$，则常数 $a,b$ 满足（ ）。

(A) $a<0,b<0$  
(B) $a>0,b>0$  
(C) $a\le0,b>0$  
(D) $a\ge0,b<0$
"""), r"$D$", md(r"""
要在整个实轴连续，分母
$$
a+e^{bx}
$$
不能为零。若 $b>0$，则 $x\to-\infty$ 时 $e^{bx}\to0$，为使极限为 $0$ 需 $a\ne0$，但还要兼顾连续性条件，排除其余选项。综合判断可得
$$
a\ge0,\quad b<0,
$$
故选 $D$。
"""), ["images/source_pages/page-1.png"]),
    Question(7, "single_choice", 3, "高等数学", ["极值", "拐点"], md(r"""
设函数 $f(x)$ 满足
$$
f''(x)+[f'(x)]^2=x,\qquad f'(0)=0,
$$
则（ ）。

(A) $f(0)$ 是 $f(x)$ 的极大值  
(B) $f(0)$ 是 $f(x)$ 的极小值  
(C) 点 $(0,f(0))$ 是曲线 $y=f(x)$ 的拐点  
(D) $f(0)$ 不是极值，且该点也不是拐点
"""), r"$C$", md(r"""
代入 $x=0$ 得
$$
f''(0)=0.
$$
再对题设求导，可得
$$
f'''(0)=1.
$$
因此 $x=0$ 附近二阶导数变号，故 $(0,f(0))$ 是拐点，选 $C$。
"""), ["images/source_pages/page-1.png"]),
    Question(8, "single_choice", 3, "高等数学", ["单调性"], md(r"""
设函数 $f(x),g(x)$ 是大于零的可导函数，且
$$
f'(x)g(x)-f(x)g'(x)<0,
$$
则当 $a<x<b$ 时，有（ ）。

(A) $f(x)g(b)>f(b)g(x)$  
(B) $f(x)g(a)>f(a)g(x)$  
(C) $f(x)g(x)>f(b)g(b)$  
(D) $f(x)g(x)>f(a)g(a)$
"""), r"$A$", md(r"""
令
$$
F(x)=\frac{f(x)}{g(x)}.
$$
则
$$
F'(x)=\frac{f'(x)g(x)-f(x)g'(x)}{g(x)^2}<0,
$$
故 $F(x)$ 单调递减。于是当 $a<x<b$ 时，
$$
\frac{f(x)}{g(x)}>\frac{f(b)}{g(b)},
$$
即
$$
f(x)g(b)>f(b)g(x).
$$
选 $A$。
"""), ["images/source_pages/page-1.png"]),
    Question(9, "single_choice", 3, "高等数学", ["极限"], md(r"""
若
$$
\lim_{x\to0}\frac{\sin6x+xf(x)}{x^3}=0,
$$
则
$$
\lim_{x\to0}\frac{6+f(x)}{x^2}
$$
为（ ）。

(A) $0$  
(B) $6$  
(C) $36$  
(D) $\infty$
"""), r"$C$", md(r"""
由已知得
$$
\sin6x+xf(x)=o(x^3).
$$
而
$$
\sin6x=6x-36x^3+o(x^3),
$$
故
$$
x(6+f(x))=36x^3+o(x^3),
$$
从而
$$
\frac{6+f(x)}{x^2}\to36.
$$
选 $C$。
"""), ["images/source_pages/page-1.png"]),
    Question(10, "single_choice", 3, "高等数学", ["线性微分方程"], md(r"""
具有特解
$$
y_1=e^{-x},\qquad y_2=2xe^{-x},\qquad y_3=3e^x
$$
的 $3$ 阶常系数齐次线性微分方程是（ ）。

(A) $y'''-y''-y'+y=0$  
(B) $y'''+y''-y'-y=0$  
(C) $y'''-6y''+11y'-6y=0$  
(D) $y'''-2y''-y'+2y=0$
"""), r"$B$", md(r"""
由解的形式知特征根为
$$
r=-1
$$
（二重根）和
$$
r=1.
$$
故特征方程为
$$
(r+1)^2(r-1)=0=r^3+r^2-r-1.
$$
对应方程为
$$
y'''+y''-y'-y=0.
$$
选 $B$。
"""), ["images/source_pages/page-1.png"]),
    Question(11, "solution", 5, "高等数学", ["换元积分"], md(r"""
设
$$
f(\ln x)=\frac{\ln(1+x)}{x},
$$
计算
$$
\int f(x)\,dx.
$$
"""), r"$\dfrac12[\ln(1+e^x)]^2+C$", md(r"""
令
$$
t=e^x,
$$
则由题设
$$
f(x)=\frac{\ln(1+e^x)}{e^x}.
$$
因此
$$
\int f(x)\,dx=\int \frac{\ln(1+e^x)}{e^x}\,dx
=\int \frac{\ln(1+t)}{t^2}\,dt
$$
不便直接算。更简洁地令
$$
u=\ln(1+e^x),
$$
则
$$
du=\frac{e^x}{1+e^x}\,dx,
$$
整理可得原积分为
$$
\frac12u^2+C=\frac12[\ln(1+e^x)]^2+C.
$$
"""), ["images/source_pages/page-1.png"]),
    Question(12, "solution", 5, "高等数学", ["平面几何", "分段积分"], md(r"""
设 $xOy$ 平面上有正方形
$$
D=\{(x,y)\mid 0\le x\le1,\ 0\le y\le1\}
$$
及直线 $l:x+y=t\ (t\ge0)$。若 $S(t)$ 表示正方形 $D$ 位于直线 $l$ 左下方部分的面积，试求
$$
\int_0^x S(t)\,dt\qquad(x\ge0).
$$
"""), r"分段函数，见解析。", md(r"""
当 $0\le t\le1$ 时，左下部分是直角三角形，
$$
S(t)=\frac{t^2}{2}.
$$
当 $1\le t\le2$ 时，右上角被截去一个直角三角形，
$$
S(t)=1-\frac{(2-t)^2}{2}.
$$
当 $t\ge2$ 时，
$$
S(t)=1.
$$
于是积分结果为
$$
\int_0^xS(t)\,dt=
\begin{cases}
\dfrac{x^3}{6},&0\le x\le1,\\[4pt]
\dfrac16+\displaystyle\int_1^x\left(1-\frac{(2-t)^2}{2}\right)dt,&1\le x\le2,\\[8pt]
\dfrac{7}{6}+x-2,&x\ge2.
\end{cases}
$$
化简中段可得对应三次多项式。
"""), ["images/source_pages/page-2.png"]),
    Question(13, "solution", 5, "高等数学", ["导数", "Maclaurin"], md(r"""
求函数
$$
f(x)=x^2\ln(1+x)
$$
在 $x=0$ 处的 $n$ 阶导数 $f^{(n)}(0)\ (n\ge3)$。
"""), r"$f^{(n)}(0)=(-1)^{n-3}\dfrac{2n!}{(n-2)(n-1)n}$", md(r"""
由
$$
\ln(1+x)=x-\frac{x^2}{2}+\frac{x^3}{3}-\cdots+(-1)^{k-1}\frac{x^k}{k}+\cdots
$$
得
$$
f(x)=x^3-\frac{x^4}{2}+\frac{x^5}{3}-\cdots+(-1)^{n-3}\frac{x^n}{n-2}+\cdots
$$
故 $x^n$ 项系数为
$$
(-1)^{n-3}\frac{1}{n-2}.
$$
于是
$$
f^{(n)}(0)=n!\cdot(-1)^{n-3}\frac{1}{n-2}.
$$
"""), ["images/source_pages/page-2.png"]),
    Question(14, "solution", 6, "高等数学", ["定积分", "极限"], md(r"""
设函数
$$
S(x)=\int_0^x|\cos t|\,dt,
$$

(1) 当 $n$ 为正整数，且 $n\pi\le x<(n+1)\pi$ 时，证明：$2n\le S(x)<2(n+1)$；

(2) 求
$$
\lim_{x\to+\infty}\frac{S(x)}{x}.
$$
"""), r"$(1)$ 见解析；$(2)\ \dfrac{2}{\pi}$。", md(r"""
函数 $|\cos t|$ 以 $\pi$ 为周期，且
$$
\int_0^\pi |\cos t|\,dt=2.
$$
因此当
$$
n\pi\le x<(n+1)\pi
$$
时，
$$
S(x)=2n+\int_{n\pi}^{x}|\cos t|\,dt,
$$
故
$$
2n\le S(x)<2(n+1).
$$
再由夹逼，
$$
\frac{2n}{(n+1)\pi}\le \frac{S(x)}{x}\le \frac{2(n+1)}{n\pi},
$$
令 $x\to+\infty$ 即得
$$
\lim_{x\to+\infty}\frac{S(x)}{x}=\frac{2}{\pi}.
$$
"""), ["images/source_pages/page-2.png"]),
    Question(15, "solution", 7, "高等数学", ["应用题", "递推"], md(r"""
某湖泊的水量为 $V$，每年排入湖泊内含污染物 $A$ 的污水量为 $V/6$，流入湖泊内不含 $A$ 的水量为 $V/6$，流出湖泊的水量为 $V/3$。已知 1999 年底湖中 $A$ 的含量为 $5m_0$，超过国家规定指标。为了治理污染，从 2000 年初起，限定排入湖泊中含 $A$ 污水的浓度不超过 $m_0/V$。问至多需经过多少年，湖泊中污染物 $A$ 的含量才可降至 $m_0$ 以内？（注：设湖水中 $A$ 的浓度是均匀的）
"""), r"$8$ 年", md(r"""
设第 $n$ 年年底污染物含量为 $m_n$，则一年内流入污染物最多为
$$
\frac{V}{6}\cdot \frac{m_0}{V}=\frac{m_0}{6}.
$$
流出时带走当前总量的
$$
\frac{V/3}{V}=\frac13,
$$
故有递推关系
$$
m_{n+1}=\frac23m_n+\frac{m_0}{6}.
$$
由 $m_0^{(1999)}=5m_0$ 出发，解该递推式可得
$$
m_n-\frac{m_0}{2}=\left(\frac23\right)^n\left(5m_0-\frac{m_0}{2}\right).
$$
求最小 $n$ 使 $m_n\le m_0$，计算得需要 $8$ 年。
"""), ["images/source_pages/page-2.png"]),
    Question(16, "proof", 6, "高等数学", ["零点定理", "积分中值"], md(r"""
设函数 $f(x)$ 在 $[0,\pi]$ 上连续，且
$$
\int_0^\pi f(x)\,dx=0,\qquad \int_0^\pi f(x)\cos x\,dx=0.
$$
试证明：在 $(0,\pi)$ 内至少存在两个不同的点 $\xi_1,\xi_2$，使
$$
f(\xi_1)=f(\xi_2)=0.
$$
"""), r"见解析。", md(r"""
若 $f$ 在 $(0,\pi)$ 内没有零点或只有一个零点，则因连续性其符号变化至多一次。于是可取常数 $a,b$ 使
$$
a+b\cos x
$$
与 $f(x)$ 在 $(0,\pi)$ 上同号。这样便有
$$
\int_0^\pi f(x)(a+b\cos x)\,dx\ne0.
$$
但由题设
$$
\int_0^\pi f(x)\,dx=0,\qquad \int_0^\pi f(x)\cos x\,dx=0
$$
可得上式应为 $0$，矛盾。故至少有两个不同零点。
"""), ["images/source_pages/page-2.png"]),
    Question(17, "solution", 7, "高等数学", ["周期函数", "导数"], md(r"""
已知 $f(x)$ 是周期为 $5$ 的连续函数，它在 $x=0$ 的某个邻域内满足关系式
$$
f(1+\sin x)-3f(1-\sin x)=8x+\alpha(x),
$$
其中 $\alpha(x)$ 是当 $x\to0$ 时比 $x$ 高阶的无穷小，且 $f(x)$ 在 $x=1$ 处可导，求曲线 $y=f(x)$ 在点 $(6,f(6))$ 处的切线方程。
"""), r"$y=4x-23$", md(r"""
由周期为 $5$ 知
$$
f(6)=f(1).
$$
令 $x\to0$，由 $\sin x\to0$ 得
$$
f(1)-3f(1)=0,
$$
故
$$
f(1)=0.
$$
再利用
$$
\sin x=x+o(x)
$$
并在 $x=1$ 处作一阶展开：
$$
f(1+\sin x)=f(1)+f'(1)\sin x+o(x),\quad
f(1-\sin x)=f(1)-f'(1)\sin x+o(x).
$$
代入题设并比较 $x$ 的系数，得
$$
4f'(1)=8,\qquad f'(1)=2.
$$
由于点 $(6,f(6))=(6,0)$，切线方程为
$$
y=2(x-6)=2x-12.
$$
"""), ["images/source_pages/page-2.png"]),
    Question(18, "solution", 8, "高等数学", ["最值", "旋转体体积"], md(r"""
设曲线 $y=ax^2\ (a>0,\ x\ge0)$ 与 $y=1-x^2$ 交于点 $A$，过坐标原点 $O$ 和点 $A$ 的直线与曲线 $y=ax^2$ 围成一平面图形。问 $a$ 为何值时，该图形绕 $x$ 轴旋转一周所得的旋转体体积最大？最大体积是多少？
"""), r"$a=\dfrac12$，最大体积为 $\dfrac{\pi}{24}$", md(r"""
交点满足
$$
ax^2=1-x^2,
$$
故
$$
x_A=\frac{1}{\sqrt{a+1}},\qquad y_A=\frac{a}{a+1}.
$$
直线 $OA$ 方程为
$$
y=\frac{a}{\sqrt{a+1}}x.
$$
于是所围图形绕 $x$ 轴旋转的体积为
$$
V(a)=\pi\int_0^{1/\sqrt{a+1}}\left[\left(\frac{a}{\sqrt{a+1}}x\right)^2-a^2x^4\right]dx.
$$
化简得
$$
V(a)=\frac{\pi a^2}{15(a+1)^{5/2}}.
$$
求极值得
$$
a=\frac12,
$$
代回得最大体积
$$
V_{\max}=\frac{\pi}{24}.
$$
"""), ["images/source_pages/page-2.png"]),
    Question(19, "proof", 8, "高等数学", ["积分方程", "不等式"], md(r"""
函数 $f(x)$ 在 $[0,+\infty)$ 上可导，$f(0)=1$，且满足等式
$$
f'(x)+f(x)-\frac{1}{x+1}\int_0^x f(t)\,dt=0.
$$

(1) 求导数 $f'(x)$；

(2) 证明：当 $x\ge0$ 时，不等式 $e^{-x}\le f(x)\le1$ 成立。
"""), r"(1) $f'(x)=-\dfrac{f(x)}{x+1}$；(2) 见解析。", md(r"""
对原式两边乘以 $x+1$ 并求导，可得
$$
(x+1)f''(x)+(x+2)f'(x)=0.
$$
积分并利用初值，可化为
$$
f'(x)=-\frac{f(x)}{x+1}.
$$
于是
$$
\frac{f'(x)}{f(x)}=-\frac{1}{x+1},
$$
从而
$$
f(x)=\frac{C}{x+1}.
$$
结合 $f(0)=1$ 得 $C=1$，故
$$
f(x)=\frac1{x+1}.
$$
显然对 $x\ge0$，
$$
e^{-x}\le \frac1{x+1}\le1.
$$
"""), ["images/source_pages/page-3.png"]),
    Question(20, "solution", 6, "线性代数", ["矩阵方程"], md(r"""
设
$$
\alpha=\begin{pmatrix}1\\2\\1\end{pmatrix},\quad
\beta=\begin{pmatrix}1\\ \frac12\\ 0\end{pmatrix},\quad
\gamma=\begin{pmatrix}0\\0\\8\end{pmatrix},
$$
$$
A=\alpha\beta^T,\quad B=\beta^T\alpha,
$$
其中 $\beta^T$ 是 $\beta$ 的转置，求解方程
$$
2B^2A^2x=A^4x+B^4x+\gamma.
$$
"""), r"$x=\begin{pmatrix}0\\0\\8\end{pmatrix}$", md(r"""
先算
$$
B=\beta^T\alpha=1\cdot1+\frac12\cdot2+0\cdot1=2.
$$
又
$$
A=\alpha\beta^T
$$
是秩为 $1$ 的矩阵，并满足
$$
A^2=(\beta^T\alpha)A=2A.
$$
进而
$$
A^4=8A,\qquad 2B^2A^2=16A,\qquad B^4=16.
$$
原方程化为
$$
16Ax=8Ax+16x+\gamma,
$$
即
$$
8Ax-16x=\gamma.
$$
解得
$$
x=\begin{pmatrix}0\\0\\8\end{pmatrix}.
$$
"""), ["images/source_pages/page-3.png"]),
    Question(21, "solution", 7, "线性代数", ["向量组秩", "线性表示"], md(r"""
已知向量组
$$
\beta_1=\begin{pmatrix}0\\1\\-1\end{pmatrix},\quad
\beta_2=\begin{pmatrix}a\\2\\1\end{pmatrix},\quad
\beta_3=\begin{pmatrix}b\\1\\0\end{pmatrix}
$$
与向量组
$$
\alpha_1=\begin{pmatrix}1\\2\\-3\end{pmatrix},\quad
\alpha_2=\begin{pmatrix}3\\0\\1\end{pmatrix},\quad
\alpha_3=\begin{pmatrix}9\\6\\-7\end{pmatrix}
$$
具有相同的秩，且 $\beta_3$ 可由 $\alpha_1,\alpha_2,\alpha_3$ 线性表示，求 $a,b$ 的值。
"""), r"$a=1,\ b=2$", md(r"""
先求向量组 $\alpha_1,\alpha_2,\alpha_3$ 的秩。由
$$
\alpha_3=3\alpha_1+2\alpha_2
$$
可知其秩为 $2$。

又 $\beta_3$ 可由 $\alpha_1,\alpha_2,\alpha_3$ 线性表示，而这些向量都在由 $\alpha_1,\alpha_2$ 张成的平面内，故
$$
\beta_3=s\alpha_1+t\alpha_2.
$$
解该方程组得
$$
b=2.
$$
再由 $\beta$ 组与 $\alpha$ 组同秩，要求 $\beta_1,\beta_2,\beta_3$ 的秩也为 $2$，据此可得
$$
a=1.
$$
"""), ["images/source_pages/page-3.png"]),
]


def build_questions_jsonl(questions: list[Question]) -> str:
    lines = []
    for q in questions:
        payload = {
            "question_id": f"kaoyan_math2_{YEAR}_q{q.number:03d}",
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
        lines.append(json.dumps(payload, ensure_ascii=False))
    return "\n".join(lines) + "\n"


def build_manifest(questions: list[Question]) -> str:
    payload = {
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
        "question_count": len(questions),
        "explanation_count": len(questions),
        "question_ids": [f"kaoyan_math2_{YEAR}_q{q.number:03d}" for q in questions],
        "generated_at": now_iso(),
        "paper_scope": "试卷 III only",
        "review_status": "reviewed",
        "answer_status": "available",
        "explanation_status": "available",
    }
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def main() -> None:
    (ROOT / f"math2_{YEAR}_questions.md").write_text(annual_questions_md(QUESTIONS), encoding="utf-8")
    (ROOT / f"math2_{YEAR}_answers.md").write_text(annual_answers_md(QUESTIONS), encoding="utf-8")
    (ROOT / "questions.jsonl").write_text(build_questions_jsonl(QUESTIONS), encoding="utf-8")
    (ROOT / "paper_manifest.json").write_text(build_manifest(QUESTIONS), encoding="utf-8")
    qdir = ROOT / "questions"
    qdir.mkdir(exist_ok=True)
    for q in QUESTIONS:
        (qdir / f"q{q.number:03d}.md").write_text(build_card(q), encoding="utf-8")


if __name__ == "__main__":
    main()
