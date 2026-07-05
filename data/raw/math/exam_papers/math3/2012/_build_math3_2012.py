from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[6]
YEAR = 2012
YEAR_DIR = ROOT / "data" / "raw" / "math" / "exam_papers" / "math3" / str(YEAR)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def question_id(number: int) -> str:
    return f"kaoyan_math3_{YEAR}_q{number:03d}"


def qtype_label(qtype: str) -> str:
    return {
        "single_choice": "选择题",
        "fill_blank": "填空题",
        "solution": "解答题",
    }[qtype]


def answer_for_table(answer: str) -> str:
    brief = " ".join(answer.replace("\n", " ").split())
    if len(brief) > 56 or "\\begin{" in brief:
        return "见详细解析"
    return brief


@dataclass
class Question:
    number: int
    question_type: str
    score: int
    module: str
    topics: list[str]
    pdf_pages: str
    stem: str
    answer: str
    explanation: str


def q(
    number: int,
    question_type: str,
    score: int,
    module: str,
    topics: list[str],
    pdf_pages: str,
    stem: str,
    answer: str,
    explanation: str,
) -> Question:
    return Question(
        number=number,
        question_type=question_type,
        score=score,
        module=module,
        topics=topics,
        pdf_pages=pdf_pages,
        stem=stem.strip(),
        answer=answer.strip(),
        explanation=explanation.strip(),
    )


QUESTIONS = [
    q(
        1,
        "single_choice",
        4,
        "高等数学",
        ["渐近线", "有理函数"],
        "30",
        r"""
曲线
$$
y=\frac{x^2+x}{x^2-1}
$$
的渐近线的条数为（ ）

(A) $0$

(B) $1$

(C) $2$

(D) $3$
""",
        "C",
        r"""
因式分解得
$$
\frac{x^2+x}{x^2-1}=\frac{x(x+1)}{(x-1)(x+1)}=\frac{x}{x-1}\qquad (x\ne -1).
$$
因此在 $x=1$ 处有竖直渐近线，
$$
x=1.
$$
又
$$
\lim_{x\to\infty}\frac{x}{x-1}=1,
$$
故有水平渐近线
$$
y=1.
$$
点 $x=-1$ 只是可去间断点，不是渐近线。
所以共有 $2$ 条，选 `C`。
""",
    ),
    q(
        2,
        "single_choice",
        4,
        "高等数学",
        ["导数", "乘积求导"],
        "30",
        r"""
设函数
$$
f(x)=(e^x-1)(e^{2x}-2)\cdots(e^{nx}-n),
$$
其中 $n$ 为正整数，则 $f'(0)=（\ \ ）$

(A) $(-1)^{n-1}(n-1)!$

(B) $(-1)^n(n-1)!$

(C) $(-1)^{n-1}n!$

(D) $(-1)^n n!$
""",
        "A",
        r"""
在 $x=0$ 时，第一个因子
$$
e^x-1
$$
为零，其余因子为
$$
e^{kx}-k\Big|_{x=0}=1-k\qquad (k=2,\dots,n).
$$
因此求导时只有对第一个因子求导的项不为零：
$$
f'(0)=e^0\prod_{k=2}^n(1-k)=\prod_{k=2}^n(-(k-1)).
$$
故
$$
f'(0)=(-1)^{n-1}(n-1)!.
$$
选 `A`。
""",
    ),
    q(
        3,
        "single_choice",
        4,
        "高等数学",
        ["二重积分", "极坐标换元"],
        "30",
        r"""
设函数 $f(t)$ 连续，则二次积分
$$
\int_0^{\pi/2}d\theta\int_{2\cos\theta}^{2}f(r^2)r\,dr
$$
等于（ ）

(A)
$$
\int_0^2dx\int_{\sqrt{2x-x^2}}^{\sqrt{4-x^2}}\sqrt{x^2+y^2}\,f(x^2+y^2)\,dy
$$

(B)
$$
\int_0^2dx\int_{\sqrt{2x-x^2}}^{\sqrt{4-x^2}}f(x^2+y^2)\,dy
$$

(C)
$$
\int_0^2dy\int_{1+\sqrt{1-y^2}}^{\sqrt{4-y^2}}\sqrt{x^2+y^2}\,f(x^2+y^2)\,dx
$$

(D)
$$
\int_0^2dy\int_{1+\sqrt{1-y^2}}^{\sqrt{4-y^2}}f(x^2+y^2)\,dx
$$
""",
        "B",
        r"""
给出的积分本身已经是极坐标形式：
$$
\iint_D f(r^2)\,r\,dr\,d\theta,
$$
其中
$$
0\le \theta\le \frac{\pi}{2},\qquad 2\cos\theta\le r\le 2.
$$
换回直角坐标后，雅可比中的 $r$ 已被吸收进积分元，只剩下
$$
\iint_D f(x^2+y^2)\,dxdy.
$$

边界 $r=2$ 对应
$$
x^2+y^2=4,
$$
边界 $r=2\cos\theta$ 对应
$$
x^2+y^2=2x\iff y^2=2x-x^2.
$$
又在第一象限，所以化为
$$
\int_0^2dx\int_{\sqrt{2x-x^2}}^{\sqrt{4-x^2}}f(x^2+y^2)\,dy.
$$
故选 `B`。
""",
    ),
    q(
        4,
        "single_choice",
        4,
        "高等数学",
        ["级数敛散性", "绝对收敛", "条件收敛"],
        "30",
        r"""
已知级数
$$
\sum_{n=1}^{\infty}(-1)^n\sqrt n\sin\frac1{n^\alpha}
$$
绝对收敛，级数
$$
\sum_{n=1}^{\infty}\frac{(-1)^n}{n^{2-\alpha}}
$$
条件收敛，则（ ）

(A) $0<\alpha\le \dfrac12$

(B) $\dfrac12<\alpha\le 1$

(C) $1<\alpha\le \dfrac32$

(D) $\dfrac32<\alpha<2$
""",
        "D",
        r"""
当 $n$ 充分大时，
$$
\sin\frac1{n^\alpha}\sim \frac1{n^\alpha},
$$
故第一组级数绝对值项与
$$
\sum \frac{1}{n^{\alpha-1/2}}
$$
同阶。要绝对收敛，需
$$
\alpha-\frac12>1\iff \alpha>\frac32.
$$

第二组是交错 $p$ 级数
$$
\sum (-1)^n n^{-(2-\alpha)}.
$$
它条件收敛要求
$$
0<2-\alpha\le 1,
$$
即
$$
1\le \alpha<2.
$$

综合得
$$
\frac32<\alpha<2.
$$
选 `D`。
""",
    ),
    q(
        5,
        "single_choice",
        4,
        "线性代数",
        ["线性相关", "行列式判别"],
        "30",
        r"""
设
$$
\alpha_1=\begin{pmatrix}0\\0\\c_1\end{pmatrix},\quad
\alpha_2=\begin{pmatrix}0\\1\\c_2\end{pmatrix},\quad
\alpha_3=\begin{pmatrix}1\\-1\\c_3\end{pmatrix},\quad
\alpha_4=\begin{pmatrix}-1\\1\\c_4\end{pmatrix},
$$
其中 $c_1,c_2,c_3,c_4$ 为任意常数，则下列向量组线性相关的是（ ）

(A) $\alpha_1,\alpha_2,\alpha_3$

(B) $\alpha_1,\alpha_2,\alpha_4$

(C) $\alpha_1,\alpha_3,\alpha_4$

(D) $\alpha_2,\alpha_3,\alpha_4$
""",
        "C",
        r"""
注意到
$$
\alpha_3+\alpha_4=
\begin{pmatrix}
1\\-1\\c_3
\end{pmatrix}
+
\begin{pmatrix}
-1\\1\\c_4
\end{pmatrix}
=
\begin{pmatrix}
0\\0\\c_3+c_4
\end{pmatrix},
$$
它与
$$
\alpha_1=\begin{pmatrix}0\\0\\c_1\end{pmatrix}
$$
同方向，因此 $\alpha_1,\alpha_3,\alpha_4$ 必线性相关。

其余三组在前两维上可以构成独立方向，不必必然相关。
故选 `C`。
""",
    ),
    q(
        6,
        "single_choice",
        4,
        "线性代数",
        ["相似对角化", "基变换"],
        "30",
        r"""
设 $A$ 为 $3$ 阶矩阵，$P$ 为 $3$ 阶可逆矩阵，且
$$
P^{-1}AP=
\begin{pmatrix}
1&0&0\\
0&1&0\\
0&0&2
\end{pmatrix}.
$$
若
$$
P=(\alpha_1,\alpha_2,\alpha_3),\qquad
Q=(\alpha_1+\alpha_2,\alpha_2,\alpha_3),
$$
则 $Q^{-1}AQ=（\ \ ）$

(A)
$$
\begin{pmatrix}
1&0&0\\
0&2&0\\
0&0&1
\end{pmatrix}
$$

(B)
$$
\begin{pmatrix}
1&0&0\\
0&1&0\\
0&0&2
\end{pmatrix}
$$

(C)
$$
\begin{pmatrix}
2&0&0\\
0&1&0\\
0&0&1
\end{pmatrix}
$$

(D)
$$
\begin{pmatrix}
2&0&0\\
0&2&0\\
0&0&1
\end{pmatrix}
$$
""",
        "B",
        r"""
因为
$$
Q=P
\begin{pmatrix}
1&0&0\\
1&1&0\\
0&0&1
\end{pmatrix},
$$
即只是在特征值为 $1$ 的二维特征子空间内更换了基。

所以在基 $Q$ 下，矩阵 $A$ 的表示仍然是
$$
\operatorname{diag}(1,1,2).
$$
故
$$
Q^{-1}AQ=
\begin{pmatrix}
1&0&0\\
0&1&0\\
0&0&2
\end{pmatrix},
$$
选 `B`。
""",
    ),
    q(
        7,
        "single_choice",
        4,
        "概率统计",
        ["几何概率", "均匀分布"],
        "30",
        r"""
设随机变量 $X$ 与 $Y$ 相互独立，且都服从区间 $(0,1)$ 上的均匀分布，则
$$
P\{X^2+Y^2\le 1\}=（\ \ ）
$$

(A) $\dfrac14$

(B) $\dfrac12$

(C) $\dfrac{\pi}{8}$

(D) $\dfrac{\pi}{4}$
""",
        "D",
        r"""
$(X,Y)$ 在单位正方形 $(0,1)\times(0,1)$ 上均匀分布。
事件
$$
X^2+Y^2\le 1
$$
对应第一象限内的单位圆四分之一。

所求概率就是该区域面积：
$$
P=\frac{\text{四分之一单位圆面积}}{\text{单位正方形面积}}
=\frac{\pi/4}{1}
=\frac{\pi}{4}.
$$
故选 `D`。
""",
    ),
    q(
        8,
        "single_choice",
        4,
        "概率统计",
        ["t分布", "正态抽样"],
        "31",
        r"""
设 $X_1,X_2,X_3,X_4$ 是来自总体 $N(1,\sigma^2)$（$\sigma>0$）的简单随机样本，则统计量
$$
\frac{X_1-X_2}{|X_3+X_4-2|}
$$
的分布为（ ）

(A) $N(0,1)$

(B) $t(1)$

(C) $\chi^2(1)$

(D) $F(1,1)$
""",
        "B",
        r"""
因为
$$
X_1-X_2\sim N(0,2\sigma^2),
$$
所以
$$
\frac{X_1-X_2}{\sqrt2\,\sigma}\sim N(0,1).
$$

又
$$
X_3+X_4-2\sim N(0,2\sigma^2),
$$
所以
$$
\frac{X_3+X_4-2}{\sqrt2\,\sigma}\sim N(0,1).
$$
故原统计量可写为
$$
\frac{\dfrac{X_1-X_2}{\sqrt2\,\sigma}}{\left|\dfrac{X_3+X_4-2}{\sqrt2\,\sigma}\right|},
$$
这是标准正态变量除以独立标准正态变量绝对值，服从 $t(1)$ 分布。
故选 `B`。
""",
    ),
    q(
        9,
        "fill_blank",
        4,
        "高等数学",
        ["重要极限", "指数极限"],
        "31",
        r"""
$$
\lim_{x\to \pi/4}(\tan x)^{\frac1{\cos x-\sin x}}=\underline{\qquad}.
$$
""",
        r"$e^{-\sqrt2}$",
        r"""
设极限为 $L$，取对数：
$$
\ln L=\lim_{x\to\pi/4}\frac{\ln(\tan x)}{\cos x-\sin x}.
$$
这是 $0/0$ 型，应用洛必达法则：
$$
\ln L=
\lim_{x\to\pi/4}
\frac{\dfrac{\sec^2x}{\tan x}}{-\sin x-\cos x}.
$$
又
$$
\frac{\sec^2x}{\tan x}=\frac{1}{\sin x\cos x},
$$
在 $x=\pi/4$ 处取值为 $2$，而
$$
-\sin\frac\pi4-\cos\frac\pi4=-\sqrt2.
$$
故
$$
\ln L=-\sqrt2,
$$
于是
$$
L=e^{-\sqrt2}.
$$
""",
    ),
    q(
        10,
        "fill_blank",
        4,
        "高等数学",
        ["复合函数求导", "分段函数"],
        "31",
        r"""
设函数
$$
f(x)=
\begin{cases}
\ln\sqrt{x},& x\ge 1,\\
2x-1,& x<1,
\end{cases}
$$
且
$$
y=f(f(x)),
$$
则
$$
\left.\frac{dy}{dx}\right|_{x=e}=\underline{\qquad}.
$$
""",
        r"$\dfrac1e$",
        r"""
先算
$$
f(e)=\ln\sqrt e=\frac12.
$$
由于 $\frac12<1$，所以
$$
f(f(e))=f\left(\frac12\right)=2\cdot\frac12-1=0.
$$

复合函数求导：
$$
y'=f'(f(x))\cdot f'(x).
$$
其中
$$
f'(e)=\frac{d}{dx}\left(\frac12\ln x\right)\Big|_{x=e}=\frac{1}{2e},
$$
且
$$
f'\left(\frac12\right)=2.
$$
故
$$
y'(e)=2\cdot\frac{1}{2e}=\frac1e.
$$
""",
    ),
    q(
        11,
        "fill_blank",
        4,
        "高等数学",
        ["全微分", "可微定义"],
        "31",
        r"""
设连续函数 $z=f(x,y)$ 满足
$$
\lim_{\substack{x\to 0\\ y\to 1}}
\frac{f(x,y)-2x+y-2}{\sqrt{x^2+(y-1)^2}}=0,
$$
则
$$
dz\big|_{(0,1)}=\underline{\qquad}.
$$
""",
        r"$2\,dx-dy$",
        r"""
由题设极限为零可知
$$
f(x,y)=2x-y+2+o\!\left(\sqrt{x^2+(y-1)^2}\right)\qquad ((x,y)\to(0,1)).
$$
这正是可微展开式，因此
$$
f_x(0,1)=2,\qquad f_y(0,1)=-1.
$$
故
$$
dz\big|_{(0,1)}=f_x(0,1)\,dx+f_y(0,1)\,dy=2\,dx-dy.
$$
""",
    ),
    q(
        12,
        "fill_blank",
        4,
        "高等数学",
        ["面积", "定积分应用"],
        "31",
        r"""
由曲线
$$
y=\frac4x
$$
和直线 $y=x$ 及 $y=4x$ 在第一象限中围成的平面图形的面积为 $\underline{\qquad}$。
""",
        r"$4\ln 2$",
        r"""
三条曲线围成的区域可按 $x$ 分段。

与双曲线的交点分别为：
$$
y=4x \text{ 与 } y=\frac4x \Rightarrow x=1;
$$
$$
y=x \text{ 与 } y=\frac4x \Rightarrow x=2.
$$

所以面积为
$$
S=\int_0^1(4x-x)\,dx+\int_1^2\left(\frac4x-x\right)\,dx.
$$
计算得
$$
S=\frac32+\left(4\ln2-\frac32\right)=4\ln2.
$$
""",
    ),
    q(
        13,
        "fill_blank",
        4,
        "线性代数",
        ["伴随矩阵", "行列式"],
        "31",
        r"""
设 $A$ 为 $3$ 阶矩阵，$|A|=3$，$A^*$ 为 $A$ 的伴随矩阵，若交换 $A$ 的第 $1$ 行与第 $2$ 行得矩阵 $B$，则
$$
|BA^*|=\underline{\qquad}.
$$
""",
        r"$-27$",
        r"""
交换两行会使行列式变号，因此
$$
|B|=-|A|=-3.
$$
又因为 $A$ 为三阶矩阵，
$$
|A^*|=|A|^{3-1}=|A|^2=9.
$$
所以
$$
|BA^*|=|B|\cdot|A^*|=(-3)\cdot 9=-27.
$$
""",
    ),
    q(
        14,
        "fill_blank",
        4,
        "概率统计",
        ["条件概率", "互斥事件"],
        "31",
        r"""
设 $A,B,C$ 是随机事件，$A$ 与 $C$ 互不相容，$P(AB)=\dfrac12,\ P(C)=\dfrac13$，则
$$
P(AB\mid \overline C)=\underline{\qquad}.
$$
""",
        r"$\dfrac34$",
        r"""
因为 $A$ 与 $C$ 互不相容，所以
$$
AB\subset A
$$
也与 $C$ 互不相容，即
$$
P(AB\cap \overline C)=P(AB)=\frac12.
$$
又
$$
P(\overline C)=1-\frac13=\frac23.
$$
因此
$$
P(AB\mid \overline C)=\frac{P(AB\cap \overline C)}{P(\overline C)}
=\frac{1/2}{2/3}=\frac34.
$$
""",
    ),
    q(
        15,
        "solution",
        10,
        "高等数学",
        ["极限", "泰勒展开"],
        "31-32",
        r"""
求极限
$$
\lim_{x\to 0}\frac{e^{x^2}-e^{2-2\cos x}}{x^4}.
$$
""",
        r"$\dfrac1{12}$",
        r"""
利用展开式
$$
2-2\cos x=x^2-\frac{x^4}{12}+o(x^4).
$$
于是
$$
e^{2-2\cos x}
=e^{x^2-\frac{x^4}{12}+o(x^4)}
=e^{x^2}\cdot e^{-\frac{x^4}{12}+o(x^4)}
=e^{x^2}\left(1-\frac{x^4}{12}+o(x^4)\right).
$$
故分子
$$
e^{x^2}-e^{2-2\cos x}
=e^{x^2}\left[\frac{x^4}{12}+o(x^4)\right].
$$
因此
$$
\lim_{x\to 0}\frac{e^{x^2}-e^{2-2\cos x}}{x^4}
=\lim_{x\to 0}e^{x^2}\left(\frac1{12}+o(1)\right)
=\frac1{12}.
$$
""",
    ),
    q(
        16,
        "solution",
        10,
        "高等数学",
        ["二重积分", "交换积分次序"],
        "31-32",
        r"""
计算二重积分
$$
\iint_D e^x y\,dxdy,
$$
其中 $D$ 是以曲线 $y=\sqrt x,\ y=\dfrac1{\sqrt x}$ 及 $y$ 轴为边界的无界区域。
""",
        r"$\dfrac12$",
        r"""
由边界关系可知区域可表示为
$$
0\le x\le 1,\qquad \sqrt x\le y\le \frac1{\sqrt x}.
$$
因此
$$
\iint_D e^x y\,dxdy
=\int_0^1 e^x\left(\int_{\sqrt x}^{1/\sqrt x}y\,dy\right)dx.
$$
内层积分为
$$
\int_{\sqrt x}^{1/\sqrt x}y\,dy
=\frac12\left(\frac1x-x\right).
$$
所以
$$
\iint_D e^x y\,dxdy
=\frac12\int_0^1 e^x(1-x^2)\,dx.
$$
注意到
$$
\frac{d}{dx}\Bigl[e^x(-x^2+2x-1)\Bigr]=e^x(1-x^2),
$$
故
$$
\int_0^1 e^x(1-x^2)\,dx
=e^x(-x^2+2x-1)\Big|_0^1=1.
$$
因此原积分为
$$
\frac12.
$$
""",
    ),
    q(
        17,
        "solution",
        10,
        "概率统计",
        ["多元成本函数", "条件极值"],
        "31-32",
        r"""
某企业为生产甲、乙两种型号的产品投入的固定成本为 $10000$（万元）。设该企业生产甲、乙两种产品的产量分别为 $x$（件）和 $y$（件），且这两种产品的边际成本分别为
$$
20+\frac{x}{2}\quad (\text{万元/件}),\qquad 6+y\quad (\text{万元/件}).
$$

1. 求生产甲、乙两种产品的总成本函数 $C(x,y)$（万元）；

2. 当总产量为 $50$ 件时，甲、乙两种产品的产量各为多少时可使总成本最小？求最小总成本；

3. 求总产量为 $50$ 件且总成本最小时甲产品的边际成本，并解释其经济意义。
""",
        r"""
$$
C(x,y)=20x+\frac{x^2}{4}+6y+\frac{y^2}{2}+10000;
$$
总产量为 $50$ 时，最优解为
$$
x=24,\ y=26,
$$
最小总成本为
$$
11118;
$$
此时甲产品边际成本为 $32$（万元/件）。
""",
        r"""
由边际成本定义，
$$
\frac{\partial C}{\partial x}=20+\frac{x}{2},\qquad
\frac{\partial C}{\partial y}=6+y.
$$
先对 $x,y$ 分别积分，得
$$
C(x,y)=20x+\frac{x^2}{4}+6y+\frac{y^2}{2}+K.
$$
由固定成本 $C(0,0)=10000$，可得 $K=10000$，所以
$$
C(x,y)=20x+\frac{x^2}{4}+6y+\frac{y^2}{2}+10000.
$$

当总产量为 $50$ 件时，约束为
$$
x+y=50,\qquad y=50-x.
$$
代入成本函数：
$$
\phi(x)=20x+\frac{x^2}{4}+6(50-x)+\frac{(50-x)^2}{2}+10000
=\frac34x^2-36x+11550.
$$
令
$$
\phi'(x)=\frac32x-36=0,
$$
得
$$
x=24,\qquad y=26.
$$
此时最小总成本
$$
C(24,26)=11118.
$$

最优点处甲产品边际成本为
$$
\frac{\partial C}{\partial x}(24,26)=20+\frac{24}{2}=32.
$$
其经济意义是：在总产量为 $50$ 件且成本最小时，甲产品产量若再增加 $1$ 件，成本约增加 $32$ 万元。
""",
    ),
    q(
        18,
        "solution",
        10,
        "高等数学",
        ["不等式证明", "导数法"],
        "32",
        r"""
证明
$$
x\ln\frac{1+x}{1-x}+\cos x\ge 1+\frac{x^2}{2}\qquad (-1<x<1).
$$
""",
        "命题成立",
        r"""
设
$$
F(x)=x\ln\frac{1+x}{1-x}+\cos x-1-\frac{x^2}{2}.
$$
则
$$
F(0)=0.
$$
对其求导：
$$
F'(x)=\ln\frac{1+x}{1-x}+\frac{2x}{1-x^2}-\sin x-x.
$$
进一步整理可知
$$
F'(x)=\left(\ln\frac{1+x}{1-x}-2x\right)+\left(\frac{2x}{1-x^2}-x\right)+(x-\sin x).
$$

在 $(-1,1)$ 上有经典不等式
$$
\ln\frac{1+x}{1-x}\ge 2x,\qquad x-\sin x\ge 0,
$$
且
$$
\frac{2x}{1-x^2}-x=\frac{x(1+x^2)}{1-x^2}
$$
与 $x$ 同号。
综合可得 $F'(x)$ 与 $x$ 同号，因此 $x=0$ 是 $F$ 的最小点。

于是对一切 $-1<x<1$，有
$$
F(x)\ge F(0)=0,
$$
即
$$
x\ln\frac{1+x}{1-x}+\cos x\ge 1+\frac{x^2}{2}.
$$
""",
    ),
    q(
        19,
        "solution",
        10,
        "高等数学",
        ["微分方程", "拐点"],
        "32",
        r"""
已知函数 $f(x)$ 满足方程
$$
f''(x)+f'(x)-2f(x)=0
$$
及
$$
f''(x)+f(x)=2e^x.
$$

1. 求 $f(x)$ 的表达式；

2. 求曲线
$$
y=f(x^2)\int_0^x f(-t^2)\,dt
$$
的拐点。
""",
        r"""
$$
f(x)=e^x;
$$
曲线唯一拐点为
$$
(0,0).
$$
""",
        r"""
将两式相减，得
$$
f'(x)-3f(x)=-2e^x.
$$
解此一阶线性微分方程：
$$
f(x)=e^x+Ce^{3x}.
$$
代回
$$
f''(x)+f(x)=2e^x
$$
可得 $C=0$，故
$$
f(x)=e^x.
$$

于是曲线方程为
$$
y=e^{x^2}\int_0^x e^{-t^2}\,dt.
$$
记
$$
I(x)=\int_0^x e^{-t^2}\,dt.
$$
则
$$
y'=2xe^{x^2}I(x)+1.
$$
再求导得
$$
y''=2(1+2x^2)e^{x^2}I(x)+2x.
$$
由于 $I(x)$ 与 $x$ 同号，所以当 $x>0$ 时，$y''>0$；当 $x<0$ 时，$y''<0$。
故曲线在 $x=0$ 两侧凹凸性相反，且
$$
y(0)=0.
$$
因此唯一拐点是
$$
(0,0).
$$
""",
    ),
    q(
        20,
        "solution",
        11,
        "线性代数",
        ["行列式", "线性方程组"],
        "32-33",
        r"""
设
$$
A=
\begin{pmatrix}
1&a&0&0\\
0&1&a&0\\
0&0&1&a\\
a&0&0&1
\end{pmatrix},\qquad
\beta=
\begin{pmatrix}
1\\
-1\\
0\\
0
\end{pmatrix}.
$$

1. 计算行列式 $|A|$；

2. 当实数 $a$ 为何值时，方程组 $Ax=\beta$ 有无穷多解，并求其通解。
""",
        r"""
$$
|A|=1-a^4;
$$
方程组有无穷多解当且仅当
$$
a=-1,
$$
此时通解为
$$
x=
\begin{pmatrix}
t\\
t-1\\
t\\
t
\end{pmatrix},\qquad t\in\mathbb R.
$$
""",
        r"""
矩阵 $A$ 只有两类非零置换项：恒等置换给出 $1$，四循环 $(1\,2\,3\,4)$ 给出 $-a^4$，故
$$
|A|=1-a^4.
$$

要使方程组有无穷多解，必须先有
$$
|A|=0\iff a^4=1\iff a=\pm 1.
$$

分别讨论：

当 $a=1$ 时，方程组为
$$
\begin{cases}
x_1+x_2=1,\\
x_2+x_3=-1,\\
x_3+x_4=0,\\
x_1+x_4=0.
\end{cases}
$$
由后两式得 $x_4=-x_3,\ x_1=x_3$，再代入第一式与第二式矛盾，所以无解。

当 $a=-1$ 时，方程组化为
$$
\begin{cases}
x_1-x_2=1,\\
x_2-x_3=-1,\\
x_3-x_4=0,\\
-x_1+x_4=0.
\end{cases}
$$
由后两式得
$$
x_4=x_1,\qquad x_3=x_4=x_1.
$$
再由第二式得
$$
x_2=x_1-1.
$$
令 $x_1=t$，则
$$
x=
\begin{pmatrix}
t\\
t-1\\
t\\
t
\end{pmatrix},\qquad t\in\mathbb R.
$$
故方程组有无穷多解当且仅当 $a=-1$。
""",
    ),
    q(
        21,
        "solution",
        11,
        "线性代数",
        ["二次型", "正交对角化"],
        "33",
        r"""
已知
$$
A=
\begin{pmatrix}
1&0&1\\
0&1&1\\
-1&0&a\\
0&a&-1
\end{pmatrix},
$$
二次型
$$
f(x_1,x_2,x_3)=x^T(A^TA)x
$$
的秩为 $2$。

1. 求实数 $a$ 的值；

2. 求正交变换 $x=Qy$ 将 $f$ 化为标准形。
""",
        r"""
$$
a=-1;
$$
标准形可取为
$$
6y_1^2+2y_2^2.
$$
""",
        r"""
因为
$$
r(A^TA)=r(A)=2,
$$
故矩阵 $A$ 的列向量线性相关。设其三列分别为
$$
c_1=\begin{pmatrix}1\\0\\-1\\0\end{pmatrix},\quad
c_2=\begin{pmatrix}0\\1\\0\\a\end{pmatrix},\quad
c_3=\begin{pmatrix}1\\1\\a\\-1\end{pmatrix}.
$$
要使秩为 $2$，必须有 $c_3$ 可由 $c_1,c_2$ 线性表示。观察到若
$$
a=-1,
$$
则
$$
c_3=c_1+c_2.
$$
因此 $a=-1$。

此时
$$
A^TA=
\begin{pmatrix}
2&0&2\\
0&2&2\\
2&2&4
\end{pmatrix}.
$$
求其特征值与特征向量，可得特征值为
$$
6,\quad 2,\quad 0,
$$
对应一组两两正交的特征向量可取
$$
v_1=(1,1,2)^T,\qquad
v_2=(1,-1,0)^T,\qquad
v_3=(-1,-1,1)^T.
$$
将其单位化：
$$
\eta_1=\frac{1}{\sqrt6}(1,1,2)^T,\quad
\eta_2=\frac{1}{\sqrt2}(1,-1,0)^T,\quad
\eta_3=\frac{1}{\sqrt3}(-1,-1,1)^T.
$$
取正交矩阵
$$
Q=(\eta_1,\eta_2,\eta_3),
$$
则
$$
Q^T(A^TA)Q=\operatorname{diag}(6,2,0).
$$
故在正交变换 $x=Qy$ 下，
$$
f=6y_1^2+2y_2^2.
$$
""",
    ),
    q(
        22,
        "solution",
        11,
        "概率统计",
        ["二维离散分布", "协方差"],
        "33",
        r"""
设二维离散型随机变量 $(X,Y)$ 的概率分布为

| $X\backslash Y$ | $0$ | $1$ | $2$ |
|---|---:|---:|---:|
| $0$ | $\dfrac14$ | $0$ | $\dfrac14$ |
| $1$ | $0$ | $\dfrac13$ | $0$ |
| $2$ | $\dfrac1{12}$ | $0$ | $\dfrac1{12}$ |

1. 求 $P\{X=2Y\}$；

2. 求 $\operatorname{Cov}(X-Y,\ Y)$。
""",
        r"""
$$
P\{X=2Y\}=\frac14;
$$
$$
\operatorname{Cov}(X-Y,\ Y)=-\frac23.
$$
""",
        r"""
由表可知事件 $X=2Y$ 只在 $(X,Y)=(0,0)$ 处发生，因此
$$
P\{X=2Y\}=P(X=0,Y=0)=\frac14.
$$

再求协方差。先求边缘分布：
$$
P(Y=0)=P(Y=1)=P(Y=2)=\frac13,
$$
故
$$
EY=1,\qquad EY^2=\frac{0^2+1^2+2^2}{3}=\frac53,
$$
所以
$$
DY=EY^2-(EY)^2=\frac53-1=\frac23.
$$

又
$$
EX=0\cdot \frac12+1\cdot\frac13+2\cdot\frac16=\frac23.
$$
并且
$$
EXY=1\cdot1\cdot\frac13+2\cdot2\cdot\frac1{12}=\frac13+\frac13=\frac23.
$$
于是
$$
\operatorname{Cov}(X,Y)=EXY-EX\cdot EY=\frac23-\frac23\cdot 1=0.
$$
故
$$
\operatorname{Cov}(X-Y,Y)=\operatorname{Cov}(X,Y)-\operatorname{Cov}(Y,Y)=0-DY=-\frac23.
$$
""",
    ),
    q(
        23,
        "solution",
        11,
        "概率统计",
        ["指数分布", "顺序统计量"],
        "33",
        r"""
设随机变量 $X$ 与 $Y$ 相互独立，且都服从参数为 $1$ 的指数分布。记
$$
U=\max\{X,Y\},\qquad V=\min\{X,Y\}.
$$

1. 求 $V$ 的概率密度 $f_V(v)$；

2. 求 $E(U+V)$。
""",
        r"""
$$
f_V(v)=
\begin{cases}
2e^{-2v},& v>0,\\
0,& v\le 0,
\end{cases}
$$
且
$$
E(U+V)=2.
$$
""",
        r"""
因为
$$
V=\min(X,Y),
$$
所以对 $v>0$，
$$
P(V>v)=P(X>v,\ Y>v)=e^{-v}\cdot e^{-v}=e^{-2v}.
$$
因此分布函数为
$$
F_V(v)=1-e^{-2v}\qquad (v>0),
$$
从而密度
$$
f_V(v)=F_V'(v)=2e^{-2v},\qquad v>0.
$$

又因为
$$
U+V=X+Y,
$$
故
$$
E(U+V)=E(X)+E(Y)=1+1=2.
$$
""",
    ),
]


def annual_questions_md(questions: list[Question]) -> str:
    lines = [
        f"# {YEAR} 年数学三真题",
        "",
        "资料类型：考研数学三历年真题",
        f"年份：{YEAR}",
        "科目：数学三",
        "整理状态：按题面页图人工核对后整理成题卡格式。",
        "",
    ]
    for qn in questions:
        lines.extend(
            [
                f"### 第 {qn.number} 题",
                f"- 题型：{qtype_label(qn.question_type)}",
                f"- 题号：{qn.number}",
                f"- 分值：{qn.score}",
                f"- 模块：{qn.module}",
                f"- 考点：{'、'.join(qn.topics)}",
                f"- PDF 页码：{qn.pdf_pages}",
                "- 校对状态：已校对",
                "",
                qn.stem,
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def annual_answers_md(questions: list[Question]) -> str:
    lines = [
        f"# {YEAR} 年数学三答案解析",
        "",
        "资料类型：考研数学三答案解析",
        f"年份：{YEAR}",
        "科目：数学三",
        "整理状态：按答案页图核对后整理；个别题目解析为依据标准答案补写的清晰版。",
        "",
    ]
    grouped = {
        "single_choice": [qn for qn in questions if qn.question_type == "single_choice"],
        "fill_blank": [qn for qn in questions if qn.question_type == "fill_blank"],
        "solution": [qn for qn in questions if qn.question_type == "solution"],
    }
    for key in ("single_choice", "fill_blank", "solution"):
        lines.extend(
            [
                f"## {qtype_label(key)}",
                "",
                "| 题号 | 答案 |",
                "|---|---|",
            ]
        )
        for qn in grouped[key]:
            lines.append(f"| {qn.number} | {answer_for_table(qn.answer)} |")
        lines.append("")
    lines.extend(["## 详细解析", ""])
    for qn in questions:
        lines.extend(
            [
                f"### 第 {qn.number} 题",
                "",
                f"- 答案：{qn.answer}",
                "",
                qn.explanation,
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def build_cards(questions: list[Question]) -> None:
    card_dir = YEAR_DIR / "questions"
    card_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for qn in questions:
        qid = question_id(qn.number)
        card = "\n".join(
            [
                "---",
                f"question_id: {qid}",
                f"exam_id: kaoyan_math3_{YEAR}",
                "exam_type: math3",
                f"year: {YEAR}",
                f"question_number: {qn.number}",
                f"question_type: {qn.question_type}",
                f"score: {qn.score}",
                f"module: {qn.module}",
                "topics:",
                *[f"  - {topic}" for topic in qn.topics],
                "difficulty: unknown",
                "review_status: reviewed",
                "answer_status: available",
                "explanation_status: available",
                f"source_file: math3_{YEAR}_questions.md",
                f"answer_source_file: math3_{YEAR}_answers.md",
                "---",
                "",
                f"# {YEAR} 数学三第 {qn.number} 题",
                "",
                "## 题目",
                "",
                qn.stem,
                "",
                "## 标准答案",
                "",
                qn.answer,
                "",
                "## 解析",
                "",
                qn.explanation,
                "",
                "## 来源",
                "",
                f"- 题目来源：`math3_{YEAR}_questions.md`",
                f"- 答案来源：`math3_{YEAR}_answers.md`",
                "",
            ]
        )
        (card_dir / f"q{qn.number:03d}.md").write_text(card, encoding="utf-8")
        rows.append(
            {
                "question_id": qid,
                "exam_id": f"kaoyan_math3_{YEAR}",
                "exam_type": "math3",
                "year": YEAR,
                "question_number": qn.number,
                "question_type": qn.question_type,
                "score": qn.score,
                "module": qn.module,
                "topics": qn.topics,
                "difficulty": "unknown",
                "review_status": "reviewed",
                "answer_status": "available",
                "explanation_status": "available",
                "source_file": f"math3_{YEAR}_questions.md",
                "answer_source_file": f"math3_{YEAR}_answers.md",
                "card_path": f"questions/q{qn.number:03d}.md",
                "answer": qn.answer,
                "explanation": qn.explanation,
            }
        )

    with (YEAR_DIR / "questions.jsonl").open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    manifest = {
        "exam_id": f"kaoyan_math3_{YEAR}",
        "exam_type": "math3",
        "exam_label": "数学三",
        "year": YEAR,
        "source_files": {
            "questions": f"math3_{YEAR}_questions.md",
            "answers": f"math3_{YEAR}_answers.md",
        },
        "card_dir": "questions",
        "index_file": "questions.jsonl",
        "question_count": len(questions),
        "explanation_count": len(questions),
        "question_ids": [question_id(qn.number) for qn in questions],
        "generated_at": now_iso(),
        "review_status": "reviewed",
        "answer_status": "available",
        "explanation_status": "available",
    }
    (YEAR_DIR / "paper_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def main() -> None:
    YEAR_DIR.mkdir(parents=True, exist_ok=True)
    (YEAR_DIR / f"math3_{YEAR}_questions.md").write_text(annual_questions_md(QUESTIONS), encoding="utf-8")
    (YEAR_DIR / f"math3_{YEAR}_answers.md").write_text(annual_answers_md(QUESTIONS), encoding="utf-8")
    build_cards(QUESTIONS)
    print(json.dumps({"year": YEAR, "question_count": len(QUESTIONS), "generated_at": now_iso()}, ensure_ascii=False))


if __name__ == "__main__":
    main()
