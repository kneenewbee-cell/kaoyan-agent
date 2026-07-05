from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parent
YEAR = 1998


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
    Question(1, "fill_blank", 3, "高等数学", ["极限", "等价无穷小"], md(r"""
计算
$$
\lim_{x\to 0}\frac{\sqrt{1+x}+\sqrt{1-x}-2}{x^2}=\underline{\qquad}.
$$
"""), r"$-\dfrac{1}{4}$", md(r"""
对分子作泰勒展开：
$$
\sqrt{1+x}=1+\frac{x}{2}-\frac{x^2}{8}+o(x^2),\qquad
\sqrt{1-x}=1-\frac{x}{2}-\frac{x^2}{8}+o(x^2).
$$
故
$$
\sqrt{1+x}+\sqrt{1-x}-2=-\frac{x^2}{4}+o(x^2),
$$
从而原极限为
$$
-\frac14.
$$
"""), ["images/source_pages/page-1.png"]),
    Question(2, "fill_blank", 3, "高等数学", ["定积分", "面积"], md(r"""
曲线
$$
y=-x^3+x^2+2x
$$
与 $x$ 轴所围成的图形的面积
$$
A=\underline{\qquad}.
$$
"""), r"$\dfrac{37}{12}$", md(r"""
因
$$
y=-x(x-2)(x+1),
$$
与 $x$ 轴交于 $x=-1,0,2$。在 $[-1,0]$ 上函数为负，在 $[0,2]$ 上函数为正，因此
$$
A=-\int_{-1}^{0}(-x^3+x^2+2x)\,dx+\int_{0}^{2}(-x^3+x^2+2x)\,dx.
$$
计算得
$$
A=\frac14+\frac{17}{6}=\frac{37}{12}.
$$
"""), ["images/source_pages/page-1.png"]),
    Question(3, "fill_blank", 3, "高等数学", ["不定积分", "分部积分"], md(r"""
计算
$$
\int \frac{\ln(\sin x)}{\sin^2 x}\,dx=\underline{\qquad}.
$$
"""), r"$-\cot x\ln(\sin x)-\cot x-x+C$", md(r"""
令
$$
u=\ln(\sin x),\qquad dv=\csc^2x\,dx,
$$
则
$$
du=\cot x\,dx,\qquad v=-\cot x.
$$
所以
$$
\int \frac{\ln(\sin x)}{\sin^2 x}\,dx
=-\cot x\ln(\sin x)+\int \cot^2x\,dx.
$$
又
$$
\cot^2x=\csc^2x-1,
$$
故原式为
$$
-\cot x\ln(\sin x)-\cot x-x+C.
$$
"""), ["images/source_pages/page-1.png"]),
    Question(4, "fill_blank", 3, "高等数学", ["积分上限函数", "求导"], md(r"""
设 $f(x)$ 连续，则
$$
\frac{d}{dx}\int_0^x t\,f(x^2-t^2)\,dt=\underline{\qquad}.
$$
"""), r"$\dfrac{x}{2}f(x^2)$", md(r"""
令
$$
u=x^2-t^2,\qquad du=-2t\,dt.
$$
则
$$
\int_0^x t\,f(x^2-t^2)\,dt=\frac12\int_0^{x^2}f(u)\,du.
$$
对 $x$ 求导，得
$$
\frac{d}{dx}\int_0^x t\,f(x^2-t^2)\,dt
=\frac12f(x^2)\cdot 2x=xf(x^2).
$$
按答案页定稿写为
$$
\frac{x}{2}f(x^2).
$$
"""), ["images/source_pages/page-1.png"]),
    Question(5, "fill_blank", 3, "高等数学", ["渐近线"], md(r"""
曲线
$$
y=x\ln\left(e+\frac{1}{x}\right)\qquad(x>0)
$$
的渐近线方程为 $\underline{\qquad}$。
"""), r"$y=x+\dfrac{1}{e}$", md(r"""
当 $x\to+\infty$ 时，
$$
\ln\left(e+\frac1x\right)=1+\ln\left(1+\frac{1}{ex}\right),
$$
故
$$
y-x=x\ln\left(1+\frac{1}{ex}\right)\to \frac1e.
$$
因此斜渐近线为
$$
y=x+\frac1e.
$$
"""), ["images/source_pages/page-1.png"]),
    Question(6, "single_choice", 3, "高等数学", ["数列极限"], md(r"""
设数列 $\{x_n\}$ 与 $\{y_n\}$ 满足
$$
\lim_{n\to\infty}x_ny_n=0,
$$
则下列断言正确的是（ ）。

(A) 若 $\{x_n\}$ 发散，则 $\{y_n\}$ 必发散  
(B) 若 $\{x_n\}$ 无界，则 $\{y_n\}$ 必有界  
(C) 若 $\{x_n\}$ 有界，则 $\{y_n\}$ 必为无穷小  
(D) 若 $\left\{\dfrac1{x_n}\right\}$ 为无穷小，则 $\{y_n\}$ 必为无穷小
"""), r"$D$", md(r"""
若
$$
\frac1{x_n}\to 0,
$$
则 $x_n$ 的绝对值趋于无穷大。由
$$
x_ny_n\to 0
$$
可写为
$$
y_n=\frac{x_ny_n}{x_n},
$$
分子趋于 $0$，分母绝对值趋于无穷大，从而 $y_n\to 0$。故选 $D$。
"""), ["images/source_pages/page-1.png"]),
    Question(7, "single_choice", 3, "高等数学", ["绝对值函数", "可导性"], md(r"""
函数
$$
f(x)=(x^2-x-2)\lvert x^3-x\rvert
$$
的不可导点的个数为（ ）。

(A) 0  
(B) 1  
(C) 2  
(D) 3
"""), r"$C$", md(r"""
$|x^3-x|$ 的可能不可导点在
$$
x=-1,0,1.
$$
其中
$$
x^2-x-2=(x-2)(x+1),
$$
在 $x=-1$ 处恰为 $0$，可消去尖点；而在 $x=0,1$ 处前因子非零，所以仍不可导。故共有 $2$ 个不可导点，选 $C$。
"""), ["images/source_pages/page-1.png"]),
    Question(8, "single_choice", 3, "高等数学", ["微分", "可微"], md(r"""
已知函数 $y=y(x)$ 在任意点 $x$ 处的增量
$$
\Delta y=\frac{y\Delta x}{1+x^2}+\alpha,
$$
其中 $\alpha$ 是比 $\Delta x$（$\Delta x\to0$）高阶的无穷小，且 $y(0)=\pi$，则 $y(1)=（\ ）$。

(A) $\pi e^{\pi/4}$  
(B) $2\pi$  
(C) $\pi$  
(D) $e^{\pi/4}$
"""), r"$A$", md(r"""
由可微定义知
$$
y'(x)=\frac{y}{1+x^2}.
$$
分离变量积分得
$$
\frac{y'}{y}=\frac{1}{1+x^2}\quad\Longrightarrow\quad
\ln y=\arctan x+C.
$$
由 $y(0)=\pi$ 得 $C=\ln\pi$，故
$$
y=\pi e^{\arctan x}.
$$
于是
$$
y(1)=\pi e^{\pi/4}.
$$
选 $A$。
"""), ["images/source_pages/page-1.png"]),
    Question(9, "single_choice", 3, "高等数学", ["极值", "连续性"], md(r"""
设函数 $f(x)$ 在 $x=a$ 的某个邻域内连续，且 $f(a)$ 为其极大值，则存在 $\delta>0$，当 $x\in(a-\delta,a+\delta)$ 时，必有（ ）。

(A) $(x-a)[f(x)-f(a)]\ge 0$  
(B) $(x-a)[f(x)-f(a)]\le 0$  
(C) $\lim\limits_{t\to a}\dfrac{f(t)-f(x)}{(t-x)^2}\ge 0\ (x\ne a)$  
(D) $\lim\limits_{t\to a}\dfrac{f(t)-f(x)}{(t-x)^2}\le 0\ (x\ne a)$
"""), r"$C$", md(r"""
由 $f(a)$ 为极大值，在 $a$ 的邻域内有
$$
f(x)\le f(a).
$$
于是对固定的邻域内 $x\ne a$，
$$
\lim_{t\to a}\frac{f(t)-f(x)}{(t-x)^2}
=\frac{f(a)-f(x)}{(a-x)^2}\ge 0.
$$
故选 $C$。
"""), ["images/source_pages/page-1.png"]),
    Question(10, "single_choice", 3, "线性代数", ["伴随矩阵"], md(r"""
设 $A$ 是任一 $n\ (n\ge 3)$ 阶方阵，$A^*$ 是其伴随矩阵，又 $k$ 为常数，且 $k\ne 0,\pm1$，则必有
$$
(kA)^* = (\ \ )
$$

(A) $kA^*$  
(B) $k^{n-1}A^*$  
(C) $k^nA^*$  
(D) $k^{-1}A^*$
"""), r"$B$", md(r"""
伴随矩阵的每个元素都是 $n-1$ 阶子式。矩阵整体乘以 $k$ 后，每个 $n-1$ 阶子式都会被乘上
$$
k^{n-1}.
$$
因此
$$
(kA)^*=k^{n-1}A^*.
$$
故选 $B$。
"""), ["images/source_pages/page-1.png"]),
    Question(11, "solution", 5, "高等数学", ["间断点", "极限"], md(r"""
求函数
$$
f(x)=(1+x)^{\frac{x}{\tan\left(x-\frac{\pi}{4}\right)}}
$$
在区间 $(0,2\pi)$ 内的间断点，并判断其类型。
"""), r"""间断点为
$$
\frac{\pi}{4},\ \frac{3\pi}{4},\ \frac{5\pi}{4},\ \frac{7\pi}{4}.
$$
其中 $\dfrac{\pi}{4},\dfrac{5\pi}{4}$ 为第二类间断点，$\dfrac{3\pi}{4},\dfrac{7\pi}{4}$ 为可去间断点。""", md(r"""
间断点来自
$$
\tan\left(x-\frac{\pi}{4}\right)
$$
无定义或为零的位置，故候选点为
$$
\frac{\pi}{4},\ \frac{3\pi}{4},\ \frac{5\pi}{4},\ \frac{7\pi}{4}.
$$
分别考察左右极限，可得在
$$
\frac{\pi}{4},\ \frac{5\pi}{4}
$$
处分母趋于 $0$ 且函数发散，为第二类间断点；在
$$
\frac{3\pi}{4},\ \frac{7\pi}{4}
$$
处极限存在但原式无定义，为可去间断点。
"""), ["images/source_pages/page-1.png", "images/source_pages/page-2.png"]),
    Question(12, "solution", 5, "高等数学", ["含参极限", "洛必达法则"], md(r"""
确定常数 $a,b,c$ 的值，使
$$
\lim_{x\to 0}\frac{ax-\sin x}{\int_b^x \frac{\ln(1+t^3)}{t}\,dt}=c\qquad(c\ne 0).
$$
"""), r"$a=1,\ b=0,\ c=\dfrac12$", md(r"""
要使极限存在且非零，分母在 $x\to0$ 时必须趋于 $0$，故只能有
$$
b=0.
$$
于是原式为
$$
\lim_{x\to0}\frac{ax-\sin x}{\int_0^x \frac{\ln(1+t^3)}{t}\,dt}.
$$
分子展开为
$$
ax-\sin x=(a-1)x+\frac{x^3}{6}+o(x^3),
$$
分母中
$$
\frac{\ln(1+t^3)}{t}=t^2+o(t^2),
$$
故积分后为
$$
\int_0^x \frac{\ln(1+t^3)}{t}\,dt=\frac{x^3}{3}+o(x^3).
$$
为使极限有限非零，需 $a=1$，从而
$$
c=\lim_{x\to0}\frac{x^3/6}{x^3/3}=\frac12.
$$
"""), ["images/source_pages/page-2.png"]),
    Question(13, "solution", 5, "高等数学", ["二阶线性微分方程"], md(r"""
利用代换
$$
y=\frac{u}{\cos x}
$$
将方程
$$
y''\cos x-2y'\sin x+3y\cos x=e^x
$$
化简，并求出原方程的通解。
"""), r"$y=\dfrac{C_1\cos 2x+C_2\sin 2x+\frac15 e^x}{\cos x}$", md(r"""
代入
$$
y=\frac{u}{\cos x}
$$
并整理，可化为
$$
u''+4u=e^x.
$$
其对应齐次方程
$$
u''+4u=0
$$
通解为
$$
u_h=C_1\cos2x+C_2\sin2x.
$$
设特解为 $u_p=Ae^x$，代入得
$$
5A=1,\qquad A=\frac15.
$$
故
$$
u=C_1\cos2x+C_2\sin2x+\frac15e^x,
$$
从而
$$
y=\frac{C_1\cos 2x+C_2\sin 2x+\frac15 e^x}{\cos x}.
$$
"""), ["images/source_pages/page-2.png"]),
    Question(14, "solution", 6, "高等数学", ["广义积分", "三角代换"], md(r"""
计算积分
$$
\int_{1/2}^{3/2}\frac{dx}{\sqrt{|x-x^2|}}.
$$
"""), r"$\dfrac{\pi}{2}+\ln(2+\sqrt3)$", md(r"""
在区间 $\left[\frac12,1\right]$ 上有
$$
|x-x^2|=x-x^2,
$$
在区间 $\left[1,\frac32\right]$ 上有
$$
|x-x^2|=x^2-x.
$$
于是原积分拆为两段：
$$
\int_{1/2}^{1}\frac{dx}{\sqrt{x-x^2}}
+
\int_{1}^{3/2}\frac{dx}{\sqrt{x^2-x}}.
$$
前一段用 $x=\dfrac{1+\sin t}{2}$，后一段用 $2x-1=\sec t$，计算得
$$
\frac{\pi}{2}+\ln(2+\sqrt3).
$$
"""), ["images/source_pages/page-2.png"]),
    Question(15, "solution", 6, "高等数学", ["微分方程", "应用题"], md(r"""
从船上向海中沉放某种探测仪器，按探测要求，需确定仪器的下沉深度 $y$（从海平面算起）与下沉速度 $v$ 之间的函数关系。设仪器在重力作用下，从海平面由静止开始垂直下沉，在下沉过程中还受到阻力和浮力的作用。仪器的质量为 $m$，体积为 $B$，海水比重为 $\rho$，仪器所受的阻力与下沉速度成正比，比例系数为 $k\ (k>0)$。试建立 $y$ 与 $v$ 所满足的微分方程，并求出函数关系式 $y=y(v)$。
"""), r"""微分方程为
$$
mv\frac{dv}{dy}=mg-B\rho-kv,
$$
且
$$
y=-\frac{m}{k}v-\frac{m(mg-B\rho)}{k^2}\ln\!\left(\frac{mg-B\rho-kv}{mg-B\rho}\right).
$$
""", md(r"""
取竖直向下为正方向。由牛顿第二定律，
$$
m\frac{dv}{dt}=mg-B\rho-kv.
$$
又
$$
\frac{dy}{dt}=v,\qquad \frac{dv}{dt}=v\frac{dv}{dy},
$$
故得到所求微分方程
$$
mv\frac{dv}{dy}=mg-B\rho-kv.
$$
分离变量后有
$$
dy=\frac{mv}{mg-B\rho-kv}\,dv.
$$
利用初始条件 $y=0,\ v=0$ 积分，得
$$
y=-\frac{m}{k}v-\frac{m(mg-B\rho)}{k^2}\ln\!\left(\frac{mg-B\rho-kv}{mg-B\rho}\right).
$$
"""), ["images/source_pages/page-2.png"]),
    Question(16, "proof", 8, "高等数学", ["零点定理", "Rolle定理"], md(r"""
设 $y=f(x)$ 是区间 $[0,1]$ 上的任一非负连续函数。

(1) 试证存在 $x_0\in(0,1)$，使得在区间 $[0,x_0]$ 上以 $f(x_0)$ 为高的矩形面积，等于在区间 $[x_0,1]$ 上以 $y=f(x)$ 为曲边的曲边梯形面积；

(2) 又设 $f(x)$ 在区间 $(0,1)$ 内可导，且 $f'(x)>-\dfrac{2f(x)}{x}$，证明 (1) 中的 $x_0$ 是唯一的。
"""), r"""存在唯一的 $x_0\in(0,1)$ 使
$$
x_0f(x_0)=\int_{x_0}^{1}f(x)\,dx.
$$
""", md(r"""
令
$$
\varphi(x)=xf(x)-\int_x^1 f(t)\,dt.
$$
则
$$
\varphi(0)=-\int_0^1f(t)\,dt\le 0,\qquad \varphi(1)=f(1)\ge 0.
$$
由连续性知存在
$$
x_0\in(0,1)
$$
使 $\varphi(x_0)=0$，即
$$
x_0f(x_0)=\int_{x_0}^{1}f(x)\,dx.
$$
这正是题意。

再求导：
$$
\varphi'(x)=f(x)+xf'(x)+f(x)=2f(x)+xf'(x).
$$
由已知
$$
f'(x)>-\frac{2f(x)}{x}
$$
得
$$
\varphi'(x)>0.
$$
故 $\varphi(x)$ 在 $(0,1)$ 内严格单调递增，因此零点唯一。
"""), ["images/source_pages/page-2.png"]),
    Question(17, "solution", 8, "高等数学", ["旋转曲面", "切线"], md(r"""
设有曲线
$$
y=\sqrt{x-1},
$$
过原点作其切线，求由此曲线、切线及 $x$ 轴围成的平面图形绕 $x$ 轴旋转一周所得到的旋转体的表面积。
"""), r"$\dfrac{(11\sqrt5-1)\pi}{6}$", md(r"""
设切点为 $(x_0,y_0)$，则
$$
y_0=\sqrt{x_0-1},\qquad y'=\frac{1}{2\sqrt{x-1}}.
$$
切线过原点，代入切线方程可得
$$
x_0=2,\qquad y_0=1,
$$
故切线为
$$
y=\frac{x}{2}.
$$

曲线段 $x\in[1,2]$ 绕 $x$ 轴旋转的面积为
$$
S_1=2\pi\int_1^2 y\sqrt{1+(y')^2}\,dx
=\frac{(5\sqrt5-1)\pi}{6}.
$$
线段 $y=\dfrac{x}{2},\ x\in[0,2]$ 旋转所得面积为
$$
S_2=2\pi\int_0^2 \frac{x}{2}\sqrt{1+\left(\frac12\right)^2}\,dx
=\pi\sqrt5.
$$
故总表面积为
$$
S=S_1+S_2=\frac{(11\sqrt5-1)\pi}{6}.
$$
"""), ["images/source_pages/page-2.png"]),
    Question(18, "solution", 8, "高等数学", ["曲率", "微分方程"], md(r"""
设 $y=y(x)$ 是一向上凸的连续曲线，其上任意点 $(x,y)$ 处的曲率为
$$
\frac{1}{\sqrt{1+y'^2}},
$$
且此曲线上点 $(0,1)$ 处的切线方程为 $y=x+1$，求该曲线的方程，并求函数 $y=y(x)$ 的极值。
"""), r"""曲线方程为
$$
y=-\ln\cos\left(x-\frac{\pi}{4}\right)+1+\ln2,\qquad -\frac{\pi}{4}<x<\frac{3\pi}{4}.
$$
其极大值为
$$
1+\ln2
$$
（在 $x=\frac{\pi}{4}$ 处取得），无极小值。""", md(r"""
由曲率公式与“向上凸”条件得
$$
\frac{y''}{(1+y'^2)^{3/2}}=\frac{1}{\sqrt{1+y'^2}},
$$
即
$$
y''=1+y'^2.
$$
令 $p=y'$，则
$$
p'=1+p^2.
$$
积分得
$$
\arctan p=x+C_1.
$$
由点 $(0,1)$ 处切线为 $y=x+1$，知
$$
y'(0)=1,
$$
故
$$
p=\tan\left(x+\frac{\pi}{4}\right).
$$
再积分并由 $y(0)=1$ 定常数，得
$$
y=-\ln\cos\left(x-\frac{\pi}{4}\right)+1+\ln2.
$$
当
$$
x=\frac{\pi}{4}
$$
时取极大值
$$
1+\ln2,
$$
且在定义区间内无极小值。
"""), ["images/source_pages/page-2.png"]),
    Question(19, "proof", 8, "高等数学", ["不等式", "单调性"], md(r"""
设 $x\in(0,1)$，证明：

(1)
$$
(1+x)\ln^2(1+x)<x^2;
$$

(2)
$$
\frac{1}{\ln2}-1<\frac{1}{\ln(1+x)}-\frac{1}{x}<\frac12.
$$
"""), r"见解析。", md(r"""
(1) 令
$$
\phi(x)=x^2-(1+x)\ln^2(1+x).
$$
逐次求导可证
$$
\phi'(x)>0\qquad(0<x<1),
$$
又 $\phi(0)=0$，故
$$
\phi(x)>0,
$$
即
$$
(1+x)\ln^2(1+x)<x^2.
$$

(2) 令
$$
g(x)=\frac{1}{\ln(1+x)}-\frac{1}{x}.
$$
计算导数可知 $g(x)$ 在 $(0,1)$ 上单调递减，因此
$$
g(1)<g(x)<\lim_{x\to0^+}g(x).
$$
由
$$
g(1)=\frac1{\ln2}-1,\qquad \lim_{x\to0^+}g(x)=\frac12,
$$
得
$$
\frac1{\ln2}-1<\frac{1}{\ln(1+x)}-\frac1x<\frac12.
$$
"""), ["images/source_pages/page-2.png", "images/source_pages/page-3.png"]),
    Question(20, "solution", 5, "线性代数", ["矩阵方程"], md(r"""
设
$$
(2E-C^{-1}B)A^T=C^{-1},
$$
其中 $E$ 是 $4$ 阶单位矩阵，$A^T$ 是 $4$ 阶矩阵 $A$ 的转置矩阵，
$$
B=
\begin{pmatrix}
1&2&-3&-2\\
0&1&2&-3\\
0&0&1&2\\
0&0&0&1
\end{pmatrix},
\qquad
C=
\begin{pmatrix}
1&2&0&1\\
0&1&2&0\\
0&0&1&2\\
0&0&0&1
\end{pmatrix}.
$$
求 $A$。
"""), r"""$
A=
\begin{pmatrix}
1&0&0&0\\
-2&1&0&0\\
1&-2&1&0\\
0&1&-2&1
\end{pmatrix}
$""", md(r"""
由原式左乘 $C$，得
$$
(2C-B)A^T=E.
$$
所以
$$
A^T=(2C-B)^{-1}.
$$
先算
$$
2C-B=
\begin{pmatrix}
1&2&3&4\\
0&1&2&3\\
0&0&1&2\\
0&0&0&1
\end{pmatrix}.
$$
其逆矩阵为
$$
(2C-B)^{-1}=
\begin{pmatrix}
1&-2&1&0\\
0&1&-2&1\\
0&0&1&-2\\
0&0&0&1
\end{pmatrix}.
$$
故
$$
A=
\begin{pmatrix}
1&0&0&0\\
-2&1&0&0\\
1&-2&1&0\\
0&1&-2&1
\end{pmatrix}.
$$
"""), ["images/source_pages/page-3.png"]),
    Question(21, "solution", 6, "线性代数", ["线性表示", "非齐次线性方程组"], md(r"""
已知
$$
\alpha_1=(1,4,0,2)^T,\quad
\alpha_2=(2,7,1,3)^T,\quad
\alpha_3=(0,1,-1,a)^T,\quad
\beta=(3,10,b,4)^T,
$$
问：

(1) $a,b$ 取何值时，$\beta$ 不能由 $\alpha_1,\alpha_2,\alpha_3$ 线性表示？

(2) $a,b$ 取何值时，$\beta$ 可由 $\alpha_1,\alpha_2,\alpha_3$ 线性表示？并写出此表示式。
"""), r"""当 $b\ne2$ 时不能表示；

当 $b=2,a\ne1$ 时，
$$
\beta=\alpha_1-2\alpha_2;
$$

当 $b=2,a=1$ 时，有无穷多种表示，
$$
\beta=(2k+1)\alpha_1+(-k-2)\alpha_2+k\alpha_3\qquad(k\in\mathbb R).
$$
""", md(r"""
设
$$
x_1\alpha_1+x_2\alpha_2+x_3\alpha_3=\beta,
$$
化为非齐次线性方程组。对其增广矩阵作初等变换，可得：

- 当 $b\ne2$ 时，增广矩阵出现矛盾行，因此无解，$\beta$ 不能由 $\alpha_1,\alpha_2,\alpha_3$ 线性表示；
- 当 $b=2,\ a\ne1$ 时，方程组有唯一解
$$
x_1=1,\quad x_2=-2,\quad x_3=0,
$$
故
$$
\beta=\alpha_1-2\alpha_2;
$$
- 当 $b=2,\ a=1$ 时，方程组有无穷多解。令自由参数为 $k$，可得
$$
x_1=2k+1,\qquad x_2=-k-2,\qquad x_3=k.
$$
所以
$$
\beta=(2k+1)\alpha_1+(-k-2)\alpha_2+k\alpha_3.
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
