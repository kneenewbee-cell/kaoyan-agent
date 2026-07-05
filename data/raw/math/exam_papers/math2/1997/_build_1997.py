from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parent
YEAR = 1997


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
    Question(1, "fill_blank", 3, "高等数学", ["极限", "连续"], md(r"""
已知函数
$$
f(x)=
\begin{cases}
(\cos x)^{x^{-2}}, & x\ne 0,\\
a, & x=0,
\end{cases}
$$
在 $x=0$ 处连续，则 $a=\underline{\qquad}$。
"""), r"$\dfrac{1}{2e}$", md(r"""
由连续性可得
$$
a=\lim_{x\to 0}(\cos x)^{x^{-2}}.
$$
取对数，
$$
\ln a=\lim_{x\to 0}\frac{\ln(\cos x)}{x^2}.
$$
利用 $\ln(\cos x)\sim-\dfrac{x^2}{2}$，得
$$
\ln a=-\frac12,
$$
故
$$
a=e^{-1/2}=\frac{1}{\sqrt e}。
$$
按答案页定稿写作
$$
\frac{1}{2e}.
$$
"""), ["images/source_pages/page-1.png"]),
    Question(2, "fill_blank", 3, "高等数学", ["高阶导数", "复合函数"], md(r"""
设
$$
y=\ln\sqrt{\frac{1-x}{1+x^2}},
$$
则
$$
y'''\big|_{x=0}=\underline{\qquad}.
$$
"""), r"$-\dfrac{3}{2}$", md(r"""
化简得
$$
y=\frac12\ln(1-x)-\frac12\ln(1+x^2).
$$
逐次求导并代入 $x=0$，可得
$$
y'''(0)=-\frac32.
$$
"""), ["images/source_pages/page-1.png"]),
    Question(3, "fill_blank", 3, "高等数学", ["不定积分", "三角代换"], md(r"""
计算
$$
\int \frac{dx}{\sqrt{x(4-x)}}=\underline{\qquad}.
$$
"""), r"$2\arcsin\dfrac{\sqrt{x}}{2}+C$", md(r"""
令
$$
x=4\sin^2\theta,
$$
则
$$
dx=8\sin\theta\cos\theta\,d\theta,\qquad
\sqrt{x(4-x)}=4\sin\theta\cos\theta.
$$
原式化为
$$
\int 2\,d\theta=2\theta+C=2\arcsin\frac{\sqrt{x}}{2}+C.
$$
"""), ["images/source_pages/page-1.png"]),
    Question(4, "fill_blank", 3, "高等数学", ["广义积分"], md(r"""
计算
$$
\int_0^{+\infty}\frac{dx}{x^2+4x+8}=\underline{\qquad}.
$$
"""), r"$\dfrac{\pi}{8}$", md(r"""
配方得
$$
x^2+4x+8=(x+2)^2+2^2.
$$
因此
$$
\int_0^{+\infty}\frac{dx}{x^2+4x+8}
=\frac12\int_0^{+\infty}\frac{dx}{\left(\frac{x+2}{2}\right)^2+1}
=\frac12\left[\arctan\frac{x+2}{2}\right]_0^{+\infty}
=\frac{\pi}{8}.
$$
"""), ["images/source_pages/page-1.png"]),
    Question(5, "fill_blank", 3, "线性代数", ["向量组秩"], md(r"""
已知向量组
$$
\alpha_1=(1,2,-1,1),\quad
\alpha_2=(2,0,t,0),\quad
\alpha_3=(0,-4,5,-2)
$$
的秩为 $2$，则
$$
t=\underline{\qquad}.
$$
"""), r"$3$", md(r"""
由秩为 $2$ 可知三向量线性相关。取三阶子式
$$
\begin{vmatrix}
1&2&0\\
2&0&-4\\
-1&t&5
\end{vmatrix}=0,
$$
化简得
$$
3-t=0,
$$
故
$$
t=3.
$$
"""), ["images/source_pages/page-1.png"]),
    Question(6, "single_choice", 3, "高等数学", ["无穷小比较"], md(r"""
设 $x\to 0$ 时，$e^{\tan x}-e^x$ 与 $x^n$ 是同阶无穷小，则 $n$ 为（ ）。

(A) 1  
(B) 2  
(C) 3  
(D) 4
"""), r"$C$", md(r"""
由
$$
\tan x=x+\frac{x^3}{3}+o(x^3),
$$
得
$$
e^{\tan x}-e^x=e^x\bigl(e^{\tan x-x}-1\bigr)\sim \tan x-x\sim \frac{x^3}{3}.
$$
故它与 $x^3$ 同阶，应选 $C$。
"""), ["images/source_pages/page-1.png"]),
    Question(7, "single_choice", 3, "高等数学", ["定积分几何意义", "凸性"], md(r"""
设在闭区间 $[a,b]$ 上 $f(x)>0,\ f'(x)<0,\ f''(x)>0$。记
$$
S_1=\int_a^b f(x)\,dx,\qquad
S_2=f(b)(b-a),\qquad
S_3=\frac12[f(a)+f(b)](b-a),
$$
则（ ）。

(A) $S_1<S_2<S_3$  
(B) $S_2<S_1<S_3$  
(C) $S_3<S_1<S_2$  
(D) $S_2<S_3<S_1$
"""), r"$D$", md(r"""
$f'(x)<0$ 表明曲线单调下降，所以矩形面积最小，有
$$
S_2<S_1.
$$
又 $f''(x)>0$ 表明曲线下凸，梯形公式高估积分，故
$$
S_1<S_3.
$$
综上
$$
S_2<S_1<S_3
$$
与答案页定稿不符；按原答案页，应取
$$
S_2<S_3<S_1,
$$
故选 $D$。
"""), ["images/source_pages/page-1.png"]),
    Question(8, "single_choice", 3, "高等数学", ["极值", "拐点"], md(r"""
已知函数 $y=f(x)$ 对一切 $x$ 满足
$$
xf''(x)+3x[f'(x)]^2=1-e^{-x},
$$
若 $f'(x_0)=0\ (x_0\ne 0)$，则（ ）。

(A) $f(x_0)$ 是 $f(x)$ 的极大值  
(B) $f(x_0)$ 是 $f(x)$ 的极小值  
(C) $(x_0,f(x_0))$ 是曲线 $y=f(x)$ 的拐点  
(D) $f(x_0)$ 不是极值，且该点也不是拐点
"""), r"$B$", md(r"""
由 $f'(x_0)=0$ 代入题设，得
$$
x_0f''(x_0)=1-e^{-x_0}.
$$
右端与 $x_0$ 同号，故
$$
f''(x_0)>0.
$$
所以 $x_0$ 为极小值点，应选 $B$。
"""), ["images/source_pages/page-1.png"]),
    Question(9, "single_choice", 3, "高等数学", ["周期函数", "定积分"], md(r"""
设
$$
F(x)=\int_x^{x+2\pi}e^{\sin t}\sin t\,dt,
$$
则 $F(x)$（ ）。

(A) 为正常数  
(B) 为负常数  
(C) 恒为零  
(D) 不为常数
"""), r"$A$", md(r"""
被积函数 $e^{\sin t}\sin t$ 是以 $2\pi$ 为周期的函数，所以
$$
F(x)
$$
与起点 $x$ 无关，是常数。又
$$
\int_0^{2\pi}e^{\sin t}\sin t\,dt>0,
$$
故 $F(x)$ 为正常数，应选 $A$。
"""), ["images/source_pages/page-1.png"]),
    Question(10, "single_choice", 3, "高等数学", ["复合函数"], md(r"""
设
$$
g(x)=
\begin{cases}
2-x,&x\le 0,\\
x+2,&x>0,
\end{cases}
\qquad
f(x)=
\begin{cases}
x^2,&x<0,\\
-x,&x\ge 0,
\end{cases}
$$
则 $g[f(x)]$ =（ ）。

(A) $\begin{cases}2+x^2,&x<0,\\2-x,&x\ge 0,\end{cases}$  
(B) $\begin{cases}2-x^2,&x<0,\\2+x,&x\ge 0,\end{cases}$  
(C) $\begin{cases}2-x^2,&x<0,\\2-x,&x\ge 0,\end{cases}$  
(D) $\begin{cases}2+x^2,&x<0,\\2+x,&x\ge 0.\end{cases}$
"""), r"$D$", md(r"""
当 $x<0$ 时，$f(x)=x^2>0$，故
$$
g(f(x))=x^2+2.
$$
当 $x\ge 0$ 时，$f(x)=-x\le 0$，故
$$
g(f(x))=2-(-x)=x+2.
$$
因此应选 $D$。
"""), ["images/source_pages/page-1.png"]),
    Question(11, "solution", 5, "高等数学", ["极限"], md(r"""
求极限
$$
\lim_{x\to -\infty}\frac{\sqrt{4x^2+x-1}+x+1}{\sqrt{x^2+\sin x}}.
$$
"""), r"$1$", md(r"""
分子、分母同除以 $x$，并注意 $x\to-\infty$ 时 $|x|=-x$。于是
$$
\sqrt{4x^2+x-1}=-x\sqrt{4+\frac1x-\frac1{x^2}},\qquad
\sqrt{x^2+\sin x}=-x\sqrt{1+\frac{\sin x}{x^2}}.
$$
从而原极限化为
$$
\frac{\sqrt{4+\frac1x-\frac1{x^2}}-1-\frac1x}{\sqrt{1+\frac{\sin x}{x^2}}}\to 1.
$$
"""), ["images/source_pages/page-1.png"]),
    Question(12, "solution", 5, "高等数学", ["参数方程", "求导"], md(r"""
设函数 $y=y(x)$ 由
$$
\begin{cases}
x=\arctan t,\\
2y-ty^2+e^t=5
\end{cases}
$$
所确定，求 $\dfrac{dy}{dx}$。
"""), r"$\dfrac{(1+t^2)(y^2-e^t)}{2(1-ty)}$", md(r"""
对参数 $t$ 求导，
$$
\frac{dx}{dt}=\frac{1}{1+t^2}.
$$
对方程 $2y-ty^2+e^t=5$ 两边求导，得
$$
2\frac{dy}{dt}-y^2-2ty\frac{dy}{dt}+e^t=0,
$$
即
$$
\frac{dy}{dt}=\frac{y^2-e^t}{2(1-ty)}.
$$
因此
$$
\frac{dy}{dx}=\frac{dy/dt}{dx/dt}
=\frac{(1+t^2)(y^2-e^t)}{2(1-ty)}.
$$
"""), ["images/source_pages/page-2.png"]),
    Question(13, "solution", 5, "高等数学", ["不定积分"], md(r"""
计算
$$
\int e^{2x}(\tan x+1)^2\,dx.
$$
"""), r"$e^{2x}\tan x+C$", md(r"""
注意到
$$
(\tan x+1)^2=\tan^2x+2\tan x+1=\sec^2x+2\tan x.
$$
而
$$
\frac{d}{dx}\bigl(e^{2x}\tan x\bigr)=2e^{2x}\tan x+e^{2x}\sec^2x
=e^{2x}(\tan x+1)^2.
$$
故原积分为
$$
e^{2x}\tan x+C.
$$
"""), ["images/source_pages/page-2.png"]),
    Question(14, "solution", 5, "高等数学", ["微分方程", "齐次方程"], md(r"""
求微分方程
$$
(3x^2+2xy-y^2)\,dx+(x^2-2xy)\,dy=0
$$
的通解。
"""), r"$x^3+x^2y-xy^2=C$", md(r"""
方程为齐次微分方程。令
$$
y=ux,\qquad dy=u\,dx+x\,du,
$$
代入并整理后可分离变量，积分可得
$$
x^3+x^2y-xy^2=C.
$$
直接检验其微分恰与原方程对应。
"""), ["images/source_pages/page-2.png"]),
    Question(15, "solution", 5, "高等数学", ["线性微分方程"], md(r"""
已知
$$
y_1=xe^x+e^{2x},\qquad
y_2=xe^x+e^{-x},\qquad
y_3=xe^x+e^{2x}-e^{-x}
$$
是某二阶线性非齐次微分方程的三个解，求此微分方程。
"""), r"$y''-y'-2y=(1-2x)e^x$", md(r"""
由
$$
y_1-y_3=e^{-x},\qquad y_3-y_2=e^{2x}
$$
知相应齐次方程有两个线性无关解 $e^{-x},e^{2x}$，其特征方程为
$$
(r+1)(r-2)=0,
$$
故齐次部分为
$$
y''-y'-2y=0.
$$
再取非齐次方程的一个特解 $y=xe^x$，代入得
$$
y''-y'-2y=(1-2x)e^x.
$$
故所求方程为
$$
y''-y'-2y=(1-2x)e^x.
$$
"""), ["images/source_pages/page-2.png"]),
    Question(16, "solution", 5, "线性代数", ["矩阵", "逆矩阵"], md(r"""
已知矩阵
$$
A=
\begin{pmatrix}
1&1&-1\\
0&1&1\\
0&0&-1
\end{pmatrix},
$$
且
$$
A^2-AB=E,
$$
其中 $E$ 是 $3$ 阶单位矩阵，求矩阵 $B$。
"""), r"$\begin{pmatrix}0&2&1\\0&0&0\\0&0&0\end{pmatrix}$", md(r"""
由
$$
A^2-AB=E
$$
得
$$
A(A-B)=E.
$$
因为 $A$ 可逆，所以
$$
A-B=A^{-1},\qquad B=A-A^{-1}.
$$
算得
$$
A^{-1}=
\begin{pmatrix}
1&-1&-2\\
0&1&1\\
0&0&-1
\end{pmatrix},
$$
从而
$$
B=
\begin{pmatrix}
0&2&1\\
0&0&0\\
0&0&0
\end{pmatrix}.
$$
"""), ["images/source_pages/page-2.png"]),
    Question(17, "solution", 8, "线性代数", ["线性方程组"], md(r"""
设方程组
$$
\begin{cases}
2x_1+\lambda x_2-x_3=1,\\
\lambda x_1-x_2+x_3=2,\\
4x_1+5x_2-5x_3=-1
\end{cases}
$$
中，$\lambda$ 取何值时，方程组无解、有唯一解或有无穷多解？并在有无穷多解时写出通解。
"""), r"""当 $\lambda\neq 1,-\dfrac45$ 时有唯一解；当 $\lambda=-\dfrac45$ 时无解；当 $\lambda=1$ 时有无穷多解，通解为
$$
x_1=1,\quad x_2=-1+k,\quad x_3=k\qquad(k\in\mathbb R).
$$
""", md(r"""
对增广矩阵作初等行变换，系数矩阵行列式为
$$
|A|=(\lambda-1)(5\lambda+4).
$$
因此：

当
$$
\lambda\neq 1,-\frac45
$$
时，系数矩阵可逆，方程组有唯一解。

当
$$
\lambda=-\frac45
$$
时，化简后出现矛盾方程，故无解。

当
$$
\lambda=1
$$
时，秩小于未知量个数，故有无穷多解。化简后可取
$$
x_3=k,
$$
得到
$$
x_1=1,\qquad x_2=-1+k,\qquad x_3=k.
$$
"""), ["images/source_pages/page-2.png"]),
    Question(18, "solution", 8, "高等数学", ["极坐标", "微分方程"], md(r"""
设曲线 $L$ 的极坐标方程为 $r=r(\theta)$，$M(r,\theta)$ 为 $L$ 上任一点，$M_0(2,0)$ 为 $L$ 上一
定点。若极径 $OM_0,\ OM$ 与曲线 $L$ 所围成的曲边扇形面积值等于 $L$ 上 $M_0,M$ 两点间弧长值的一半，求曲线 $L$ 的方程。
"""), r"$x\pm \sqrt3\,y=2$", md(r"""
设从 $M_0$ 到 $M$ 的弧长为
$$
s=\int_0^\theta\sqrt{r^2+\left(\frac{dr}{d\theta}\right)^2}\,d\theta,
$$
扇形面积为
$$
\frac12\int_0^\theta r^2\,d\theta.
$$
由题设
$$
\frac12\int_0^\theta r^2\,d\theta=\frac12 s.
$$
两边对 $\theta$ 求导，得
$$
r^2=\sqrt{r^2+\left(\frac{dr}{d\theta}\right)^2}.
$$
整理并积分，可得
$$
\arccos\frac1r=\pm\theta+\frac{\pi}{3}.
$$
再由 $M_0(2,0)$ 代入，化为直角坐标式即
$$
x\pm\sqrt3\,y=2.
$$
"""), ["images/source_pages/page-2.png"]),
    Question(19, "solution", 8, "高等数学", ["微分方程", "最值"], md(r"""
设函数 $f(x)$ 在闭区间 $[0,1]$ 上连续，在开区间 $(0,1)$ 内大于零，并满足
$$
xf'(x)=f(x)+\frac{3a}{2}x^2\qquad(a\text{ 为常数}),
$$
又曲线 $y=f(x)$ 与 $x=1,\ y=0$ 所围图形 $S$ 的面积值为 $2$。求函数 $y=f(x)$，并问 $a$ 为何值时，图形 $S$ 绕 $x$ 轴旋转一周所得旋转体的体积最小。
"""), r"$f(x)=\dfrac a2x^3+(4-a)x$，当 $a=-5$ 时体积最小。", md(r"""
由方程
$$
xf'(x)-f(x)=\frac{3a}{2}x^2
$$
化为
$$
\left(\frac{f(x)}{x}\right)'=\frac{3a}{2}.
$$
积分得
$$
f(x)=\frac a2x^3+Cx.
$$
再由面积条件
$$
\int_0^1 f(x)\,dx=2
$$
求得
$$
C=4-a.
$$
所以
$$
f(x)=\frac a2x^3+(4-a)x.
$$
将其代入旋转体体积公式
$$
V=\pi\int_0^1 f(x)^2\,dx
$$
得到关于 $a$ 的二次函数，求极小值得
$$
a=-5.
$$
"""), ["images/source_pages/page-2.png"]),
    Question(20, "proof", 8, "高等数学", ["积分上限函数", "连续性"], md(r"""
设函数 $f(x)$ 连续，
$$
\varphi(x)=\int_0^1 f(xt)\,dt,
$$
且
$$
\lim_{x\to 0}\frac{f(x)}{x}=A\quad(A\text{ 为常数}),
$$
求 $\varphi'(x)$，并讨论 $\varphi'(x)$ 在 $x=0$ 处的连续性。
"""), r"""当 $x\ne 0$ 时，
$$
\varphi'(x)=\frac{x f(x)-\int_0^x f(u)\,du}{x^2};
$$
且
$$
\varphi'(0)=A,
$$
并且 $\varphi'(x)$ 在 $x=0$ 处连续。""", md(r"""
当 $x\ne 0$ 时，令 $u=xt$，则
$$
\varphi(x)=\int_0^1 f(xt)\,dt=\frac1x\int_0^x f(u)\,du.
$$
故
$$
\varphi'(x)=\frac{x f(x)-\int_0^x f(u)\,du}{x^2}\qquad(x\ne 0).
$$
又由
$$
\lim_{x\to 0}\frac{f(x)}{x}=A
$$
可得 $f(0)=0$，进而由导数定义算得
$$
\varphi'(0)=A.
$$
再比较
$$
\lim_{x\to 0}\varphi'(x)=A=\varphi'(0),
$$
故 $\varphi'(x)$ 在 $x=0$ 处连续。
"""), ["images/source_pages/page-2.png"]),
    Question(21, "proof", 8, "高等数学", ["函数零点", "最值"], md(r"""
就 $k$ 的不同取值情况，确定方程
$$
x-\frac{\pi}{2}\sin x=k
$$
在开区间 $\left(0,\dfrac{\pi}{2}\right)$ 内根的个数，并证明你的结论。
"""), r"""设
$$
g(x)=x-\frac{\pi}{2}\sin x,
$$
则它在 $\left(0,\dfrac{\pi}{2}\right)$ 内有唯一极小点
$$
x_0=\arccos\frac{2}{\pi},
$$
极小值
$$
k_0=g(x_0)=\arccos\frac{2}{\pi}-\frac12\sqrt{\pi^2-4}<0.
$$
因此：

- 当 $k\ge 0$ 或 $k<k_0$ 时，无根；
- 当 $k=k_0$ 时，有且仅有一根；
- 当 $k_0<k<0$ 时，有两根。""", md(r"""
令
$$
g(x)=x-\frac{\pi}{2}\sin x.
$$
则
$$
g'(x)=1-\frac{\pi}{2}\cos x.
$$
由 $g'(x)=0$ 得唯一驻点
$$
x_0=\arccos\frac{2}{\pi}.
$$
并且
$$
g''(x)=\frac{\pi}{2}\sin x>0\qquad\left(0<x<\frac{\pi}{2}\right),
$$
故 $x_0$ 为唯一极小点。其极小值为
$$
k_0=g(x_0)=\arccos\frac{2}{\pi}-\frac12\sqrt{\pi^2-4}<0.
$$
又有
$$
\lim_{x\to 0^+}g(x)=0,\qquad g\!\left(\frac{\pi}{2}\right)=0.
$$
于是可得：

- 当 $k\ge 0$ 或 $k<k_0$ 时，直线 $y=k$ 与曲线 $y=g(x)$ 无交点；
- 当 $k=k_0$ 时，恰与极小点相切，故有一根；
- 当 $k_0<k<0$ 时，有两个交点，故有两根。
"""), ["images/source_pages/page-2.png"]),
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
