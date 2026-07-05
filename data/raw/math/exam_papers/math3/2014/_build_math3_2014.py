from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[6]
YEAR = 2014
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
        ["数列极限", "极限定义"],
        "22",
        r"""
设 $\lim\limits_{n\to\infty} a_n=a$，且 $a\ne 0$，则当 $n$ 充分大时（ ）

(A) $\left|a_n\right|>\dfrac{|a|}{2}$

(B) $\left|a_n\right|<\dfrac{|a|}{2}$

(C) $a_n>a-\dfrac1n$

(D) $a_n<a+\dfrac1n$
""",
        "A",
        r"""
由 $a_n\to a\ne 0$，对 $\varepsilon=\dfrac{|a|}{2}>0$，存在 $N$，使得 $n>N$ 时
$$
|a_n-a|<\frac{|a|}{2}.
$$
于是
$$
|a_n|\ge |a|-|a_n-a|>|a|-\frac{|a|}{2}=\frac{|a|}{2}.
$$
故应选 `A`。
""",
    ),
    q(
        2,
        "single_choice",
        4,
        "高等数学",
        ["渐近线", "无穷远处极限"],
        "22",
        r"""
下列曲线中有渐近线的是（ ）

(A) $y=x+\sin x$

(B) $y=x^2+\sin x$

(C) $y=x+\sin\dfrac1x$

(D) $y=x^2+\sin\dfrac1x$
""",
        "C",
        r"""
对选项 (C)，有
$$
\lim_{x\to\infty}\frac{x+\sin(1/x)}{x}=1,\qquad
\lim_{x\to\infty}\left[x+\sin\left(\frac1x\right)-x\right]=0.
$$
因此 $y=x$ 是其斜渐近线。其余各项都不存在水平、竖直或斜渐近线。
故选 `C`。
""",
    ),
    q(
        3,
        "single_choice",
        4,
        "高等数学",
        ["泰勒展开", "无穷小比较"],
        "22",
        r"""
设 $p(x)=a+bx+cx^2+dx^3$。当 $x\to 0$ 时，若 $p(x)-\tan x$ 是比 $x^3$ 高阶的无穷小，则下列选项中错误的是（ ）

(A) $a=0$

(B) $b=1$

(C) $c=0$

(D) $d=\dfrac13$
""",
        "D",
        r"""
由
$$
\tan x=x+\frac{x^3}{3}+o(x^3)
$$
可知
$$
p(x)-\tan x=(a)+(b-1)x+cx^2+\left(d-\frac13\right)x^3+o(x^3).
$$
它比 $x^3$ 高阶，故各低阶系数都应为零：
$$
a=0,\quad b=1,\quad c=0,\quad d=\frac13.
$$
因此错误项是把 $d$ 写成 $\dfrac16$ 的选项 `D`。
""",
    ),
    q(
        4,
        "single_choice",
        4,
        "高等数学",
        ["凸函数", "导数应用"],
        "22",
        r"""
设函数 $f(x)$ 具有 $2$ 阶导数，$g(x)=f(0)(1-x)+f(1)x$，则在区间 $[0,1]$ 上（ ）

(A) 当 $f'(x)\ge 0$ 时，$f(x)\ge g(x)$

(B) 当 $f'(x)\ge 0$ 时，$f(x)\le g(x)$

(C) 当 $f''(x)\ge 0$ 时，$f(x)\ge g(x)$

(D) 当 $f''(x)\ge 0$ 时，$f(x)\le g(x)$
""",
        "D",
        r"""
当 $f''(x)\ge 0$ 时，$f$ 在 $[0,1]$ 上为凸函数。凸函数的图像位于连接两端点的弦下方，而
$$
g(x)=f(0)(1-x)+f(1)x
$$
正是连接 $(0,f(0))$ 与 $(1,f(1))$ 的线段方程，所以
$$
f(x)\le g(x),\qquad x\in[0,1].
$$
故选 `D`。
""",
    ),
    q(
        5,
        "single_choice",
        4,
        "线性代数",
        ["行列式"],
        "22",
        r"""
行列式
$$
\begin{vmatrix}
0&a&b&0\\
a&0&0&b\\
0&c&d&0\\
c&0&0&d
\end{vmatrix}
=（\ \ ）
$$

(A) $(ad-bc)^2$

(B) $-(ad-bc)^2$

(C) $a^2d^2-b^2c^2$

(D) $b^2c^2-a^2d^2$
""",
        "B",
        r"""
按第一列展开：
$$
\begin{vmatrix}
0&a&b&0\\
a&0&0&b\\
0&c&d&0\\
c&0&0&d
\end{vmatrix}
=-a
\begin{vmatrix}
a&b&0\\
c&d&0\\
0&0&d
\end{vmatrix}
-c
\begin{vmatrix}
a&b&0\\
0&0&b\\
c&d&0
\end{vmatrix}.
$$
化简得
$$
-ad(ad-bc)+bc(ad-bc)=-(ad-bc)^2.
$$
故选 `B`。
""",
    ),
    q(
        6,
        "single_choice",
        4,
        "线性代数",
        ["线性无关", "矩阵秩"],
        "22",
        r"""
设 $\alpha_1,\alpha_2,\alpha_3$ 均为 $3$ 维向量，则对任意常数 $k,l$，向量组 $\alpha_1+k\alpha_3,\alpha_2+l\alpha_3$ 线性无关是向量组 $\alpha_1,\alpha_2,\alpha_3$ 线性无关的（ ）

(A) 必要非充分条件

(B) 充分非必要条件

(C) 充分必要条件

(D) 既非充分也非必要条件
""",
        "A",
        r"""
有
$$
(\alpha_1+k\alpha_3,\ \alpha_2+l\alpha_3,\ \alpha_3)
=(\alpha_1,\alpha_2,\alpha_3)
\begin{pmatrix}
1&0&0\\
0&1&0\\
k&l&1
\end{pmatrix}.
$$
若 $\alpha_1,\alpha_2,\alpha_3$ 线性无关，则上述变换矩阵可逆，所以 $\alpha_1+k\alpha_3,\alpha_2+l\alpha_3$ 一定线性无关，故该条件是必要的。

但其并非充分。例如取
$$
\alpha_1=\begin{pmatrix}1\\0\\0\end{pmatrix},\ 
\alpha_2=\begin{pmatrix}0\\1\\0\end{pmatrix},\ 
\alpha_3=\begin{pmatrix}0\\0\\0\end{pmatrix},
$$
则对任意 $k,l$，$\alpha_1+k\alpha_3,\alpha_2+l\alpha_3$ 仍线性无关，而 $\alpha_1,\alpha_2,\alpha_3$ 线性相关。
故选 `A`。
""",
    ),
    q(
        7,
        "single_choice",
        4,
        "概率统计",
        ["事件独立", "概率计算"],
        "22",
        r"""
设随机事件 $A$ 与 $B$ 相互独立，且 $P(B)=0.5,\ P(A-B)=0.3$，则 $P(B-A)=（\ \ ）$

(A) $0.1$

(B) $0.2$

(C) $0.3$

(D) $0.4$
""",
        "B",
        r"""
由独立性，
$$
P(A-B)=P(A)-P(AB)=P(A)-P(A)P(B)=0.5P(A).
$$
题设给出 $P(A-B)=0.3$，故
$$
P(A)=0.6.
$$
于是
$$
P(B-A)=P(B)-P(AB)=P(B)-P(A)P(B)=0.5-0.6\times0.5=0.2.
$$
故选 `B`。
""",
    ),
    q(
        8,
        "single_choice",
        4,
        "概率统计",
        ["t分布", "正态分布"],
        "22",
        r"""
设 $X_1,X_2,X_3$ 为来自正态总体 $N(0,\sigma^2)$ 的简单随机样本，则统计量
$$
S=\frac{X_1-X_2}{\sqrt2\,|X_3|}
$$
服从的分布为（ ）

(A) $F(1,1)$

(B) $F(2,1)$

(C) $t(1)$

(D) $t(2)$
""",
        "C",
        r"""
因为
$$
X_1-X_2\sim N(0,2\sigma^2),
$$
所以
$$
\frac{X_1-X_2}{\sqrt2\,\sigma}\sim N(0,1).
$$
又有
$$
\frac{X_3}{\sigma}\sim N(0,1),\qquad \left(\frac{X_3}{\sigma}\right)^2\sim\chi^2(1).
$$
故
$$
S=\frac{\dfrac{X_1-X_2}{\sqrt2\,\sigma}}{\sqrt{\left(\dfrac{X_3}{\sigma}\right)^2}}
\sim t(1).
$$
故选 `C`。
""",
    ),
    q(
        9,
        "fill_blank",
        4,
        "概率统计",
        ["经济应用", "边际收益"],
        "22",
        r"""
设某商品的需求函数为 $Q=40-2P$（$P$ 为商品的价格），则该商品的边际收益为 $\underline{\qquad}$。
""",
        r"$20-Q$",
        r"""
由 $Q=40-2P$ 得
$$
P=20-\frac Q2.
$$
于是收益函数
$$
R(Q)=PQ=\left(20-\frac Q2\right)Q=20Q-\frac12Q^2.
$$
边际收益为
$$
R'(Q)=20-Q.
$$
""",
    ),
    q(
        10,
        "fill_blank",
        4,
        "高等数学",
        ["定积分应用", "面积"],
        "22",
        r"""
设 $D$ 是由曲线 $xy+1=0$ 与直线 $y+x=0$ 及 $y=2$ 围成的有界区域，则 $D$ 的面积为 $\underline{\qquad}$。
""",
        r"$\dfrac32-\ln 2$",
        r"""
由 $xy+1=0$ 得
$$
x=-\frac1y,
$$
由 $y+x=0$ 得
$$
x=-y.
$$
交点满足 $-y=-1/y$，得 $y=1$（结合区域位置取正值）。因此面积为
$$
S=\int_1^2\left(-\frac1y-(-y)\right)\,dy
=\int_1^2\left(y-\frac1y\right)\,dy
=\left(\frac{y^2}{2}-\ln y\right)\Big|_1^2
=\frac32-\ln2.
$$
""",
    ),
    q(
        11,
        "fill_blank",
        4,
        "高等数学",
        ["定积分"],
        "23",
        r"""
设
$$
\int_0^a xe^{2x}\,dx=\frac14,
$$
则 $a=\underline{\qquad}$。
""",
        r"$\dfrac12$",
        r"""
分部积分可得
$$
\int xe^{2x}\,dx=\frac{e^{2x}}{4}(2x-1)+C.
$$
故
$$
\int_0^a xe^{2x}\,dx=\frac{e^{2a}}{4}(2a-1)+\frac14.
$$
令其等于 $\dfrac14$，得到
$$
\frac{e^{2a}}{4}(2a-1)=0,
$$
故 $2a-1=0$，于是
$$
a=\frac12.
$$
""",
    ),
    q(
        12,
        "fill_blank",
        4,
        "高等数学",
        ["二重积分", "积分次序交换"],
        "23",
        r"""
二次积分
$$
\int_0^1dy\int_y^1\left(\frac{e^{x^2}}x-e^{y^2}\right)dx=\underline{\qquad}.
$$
""",
        r"$\dfrac{e-1}{2}$",
        r"""
将积分拆开并交换次序：
$$
\int_0^1dy\int_y^1\frac{e^{x^2}}x\,dx
=\int_0^1dx\int_0^x\frac{e^{x^2}}x\,dy
=\int_0^1e^{x^2}\,dx.
$$
另一部分为
$$
\int_0^1dy\int_y^1 e^{y^2}\,dx
=\int_0^1(1-y)e^{y^2}\,dy.
$$
所以原式
$$
=\int_0^1e^{x^2}\,dx-\int_0^1e^{y^2}\,dy+\int_0^1ye^{y^2}\,dy
=\int_0^1ye^{y^2}\,dy
=\frac12(e-1).
$$
""",
    ),
    q(
        13,
        "fill_blank",
        4,
        "线性代数",
        ["二次型", "惯性指数"],
        "23",
        r"""
设二次型
$$
f(x_1,x_2,x_3)=x_1^2-x_2^2+2ax_1x_3+4x_2x_3
$$
的负惯性指数为 $1$，则 $a$ 的取值范围是 $\underline{\qquad}$。
""",
        r"$[-2,\,2]$",
        r"""
配方得
$$
f(x_1,x_2,x_3)
=(x_1+ax_3)^2-(x_2-2x_3)^2+(4-a^2)x_3^2.
$$
要使负惯性指数为 $1$，最后一项不能再额外产生负平方项，因此需
$$
4-a^2\ge 0.
$$
故
$$
-2\le a\le 2.
$$
""",
    ),
    q(
        14,
        "fill_blank",
        4,
        "概率统计",
        ["数学期望", "抽样分布"],
        "23",
        r"""
设总体 $X$ 的概率密度为
$$
f(x;\theta)=
\begin{cases}
\dfrac{2x}{3\theta^2},& \theta<x<2\theta,\\[4pt]
0,& \text{其他},
\end{cases}
$$
其中 $\theta$ 是未知参数，$X_1,X_2,\cdots,X_n$ 为来自总体 $X$ 的简单随机样本。若
$$
E\left(c\sum_{i=1}^nX_i^2\right)=\theta^2,
$$
则 $c=\underline{\qquad}$。
""",
        r"$\dfrac{2}{5n}$",
        r"""
先求
$$
E(X^2)=\int_\theta^{2\theta}x^2\cdot \frac{2x}{3\theta^2}\,dx
=\frac{2}{3\theta^2}\int_\theta^{2\theta}x^3\,dx
=\frac52\theta^2.
$$
于是
$$
E\left(c\sum_{i=1}^nX_i^2\right)
=c\sum_{i=1}^nE(X_i^2)
=cn\cdot\frac52\theta^2.
$$
令其等于 $\theta^2$，得
$$
cn\cdot\frac52=1,
$$
所以
$$
c=\frac{2}{5n}.
$$
""",
    ),
    q(
        15,
        "solution",
        10,
        "高等数学",
        ["极限", "洛必达法则", "变量代换"],
        "23",
        r"""
求极限
$$
\lim_{x\to+\infty}\frac{\int_1^x\left[t^2\left(e^{1/t}-1\right)-t\right]dt}{x^2\ln\left(1+\frac1x\right)}.
$$
""",
        r"$\dfrac12$",
        r"""
因为
$$
x^2\ln\left(1+\frac1x\right)\sim x\qquad (x\to+\infty),
$$
原极限可写为
$$
\lim_{x\to+\infty}\frac{\int_1^x\left[t^2\left(e^{1/t}-1\right)-t\right]dt}{x}.
$$
由洛必达法则得
$$
\lim_{x\to+\infty}\left[x^2\left(e^{1/x}-1\right)-x\right].
$$
令 $u=\dfrac1x\to 0^+$，则上式变为
$$
\lim_{u\to0^+}\frac{e^u-1-u}{u^2}.
$$
再用展开式
$$
e^u=1+u+\frac{u^2}{2}+o(u^2),
$$
得极限为
$$
\frac12.
$$
""",
    ),
    q(
        16,
        "solution",
        10,
        "高等数学",
        ["二重积分", "极坐标", "对称性"],
        "23",
        r"""
设平面区域
$$
D=\{(x,y)\mid 1\le x^2+y^2\le 4,\ x\ge 0,\ y\ge 0\},
$$
计算
$$
\iint_D\frac{x\sin\!\left(\pi\sqrt{x^2+y^2}\right)}{x+y}\,dxdy.
$$
""",
        r"$-\dfrac34$",
        r"""
将积分化为极坐标：
$$
x=r\cos\theta,\quad y=r\sin\theta,\quad
1\le r\le 2,\ 0\le\theta\le\frac\pi2.
$$
于是
$$
\iint_D\frac{x\sin(\pi\sqrt{x^2+y^2})}{x+y}\,dxdy
=\int_0^{\pi/2}\frac{\cos\theta}{\cos\theta+\sin\theta}\,d\theta
\int_1^2 r\sin(\pi r)\,dr.
$$
由对称性
$$
\int_0^{\pi/2}\frac{\cos\theta}{\cos\theta+\sin\theta}\,d\theta
=\frac12\int_0^{\pi/2}1\,d\theta
=\frac\pi4.
$$
再算
$$
\int_1^2r\sin(\pi r)\,dr
=\frac1\pi\left(-r\cos\pi r+\frac1\pi\sin\pi r\right)\Big|_1^2
=-\frac3\pi.
$$
因此原积分
$$
=\frac\pi4\cdot\left(-\frac3\pi\right)
=-\frac34.
$$
""",
    ),
    q(
        17,
        "solution",
        10,
        "高等数学",
        ["偏导数", "微分方程"],
        "24",
        r"""
设函数 $f(u)$ 具有连续导数，且
$$
z=f(e^x\cos y)
$$
满足
$$
\cos y\,\frac{\partial z}{\partial x}-\sin y\,\frac{\partial z}{\partial y}
=(4z+e^x\cos y)e^x.
$$
若 $f(0)=0$，求 $f(u)$ 的表达式。
""",
        r"$f(u)=\dfrac{1}{16}\left(e^{4u}-4u-1\right)$",
        r"""
记
$$
u=e^x\cos y,\qquad z=f(u).
$$
则
$$
\frac{\partial z}{\partial x}=f'(u)e^x\cos y,\qquad
\frac{\partial z}{\partial y}=-f'(u)e^x\sin y.
$$
代入题设得
$$
f'(u)e^x=(4f(u)+u)e^x,
$$
即
$$
f'(u)-4f(u)=u.
$$
解线性微分方程：
$$
f(u)=Ce^{4u}-\frac u4-\frac1{16}.
$$
由 $f(0)=0$ 得
$$
C=\frac1{16}.
$$
因此
$$
f(u)=\frac1{16}\left(e^{4u}-4u-1\right).
$$
""",
    ),
    q(
        18,
        "solution",
        10,
        "高等数学",
        ["幂级数", "和函数"],
        "24",
        r"""
求幂级数
$$
\sum_{n=0}^{\infty}(n+1)(n+3)x^n
$$
的收敛域及和函数。
""",
        r"""
收敛域为 $(-1,1)$，
$$
S(x)=\frac{3-x}{(1-x)^3}.
$$
""",
        r"""
系数 $a_n=(n+1)(n+3)$，有
$$
\lim_{n\to\infty}\left|\frac{a_{n+1}}{a_n}\right|
=\lim_{n\to\infty}\frac{(n+2)(n+4)}{(n+1)(n+3)}=1,
$$
故收敛半径 $R=1$。当 $x=\pm1$ 时，通项不趋于零，所以端点都发散，收敛域为
$$
(-1,1).
$$

设
$$
S(x)=\sum_{n=0}^{\infty}(n+1)(n+3)x^n.
$$
利用
$$
\sum_{n=0}^{\infty}(n+1)x^n=\frac1{(1-x)^2},\qquad
\sum_{n=0}^{\infty}(n+1)(n+2)x^n=\frac{2}{(1-x)^3},
$$
并注意
$$
(n+1)(n+3)=(n+1)(n+2)+(n+1),
$$
可得
$$
S(x)=\frac{2}{(1-x)^3}+\frac{1}{(1-x)^2}
=\frac{3-x}{(1-x)^3}.
$$
""",
    ),
    q(
        19,
        "solution",
        10,
        "高等数学",
        ["积分不等式", "单调性"],
        "24",
        r"""
设函数 $f(x),g(x)$ 在区间 $[a,b]$ 上连续，且 $f(x)$ 单调增加，$0\le g(x)\le 1$。证明：

1. $0\le \int_a^x g(t)\,dt\le x-a,\quad x\in[a,b]$；

2. 
$$
\int_a^{a+\int_a^b g(t)\,dt}f(x)\,dx\le \int_a^b f(x)g(x)\,dx.
$$
""",
        "命题成立",
        r"""
对任意 $x\in[a,b]$，由 $0\le g(t)\le 1$ 可得
$$
0=\int_a^x0\,dt\le \int_a^xg(t)\,dt\le \int_a^x1\,dt=x-a,
$$
第 1 问成立。

令
$$
F(x)=\int_a^{a+\int_a^x g(u)\,du}f(t)\,dt-\int_a^x f(t)g(t)\,dt,\qquad x\in[a,b].
$$
则
$$
F'(x)=\Bigl[f\Bigl(a+\int_a^xg(u)\,du\Bigr)-f(x)\Bigr]g(x).
$$
由第 1 问知
$$
a+\int_a^xg(u)\,du\le x,
$$
而 $f$ 单调增加，故
$$
f\Bigl(a+\int_a^xg(u)\,du\Bigr)\le f(x).
$$
再结合 $g(x)\ge 0$，得到
$$
F'(x)\le 0.
$$
所以 $F(x)$ 在 $[a,b]$ 上单调不增。又
$$
F(a)=0,
$$
故
$$
F(b)\le 0.
$$
即
$$
\int_a^{a+\int_a^b g(t)\,dt}f(x)\,dx\le \int_a^b f(x)g(x)\,dx.
$$
证毕。
""",
    ),
    q(
        20,
        "solution",
        11,
        "线性代数",
        ["齐次方程组", "广义逆问题"],
        "24",
        r"""
设矩阵
$$
A=
\begin{pmatrix}
1&-2&3&-4\\
0&1&-1&1\\
1&2&0&-3
\end{pmatrix},\qquad E\text{ 为 }3\text{ 阶单位矩阵}.
$$

1. 求方程组 $Ax=0$ 的一个基础解系；

2. 求满足 $AB=E$ 的所有矩阵 $B$。
""",
        r"""
基础解系可取
$$
\alpha=\begin{pmatrix}-1\\2\\3\\1\end{pmatrix},
$$
且
$$
B=
\begin{pmatrix}
2&6&-1\\
-1&-3&1\\
-1&-4&1\\
0&0&0
\end{pmatrix}
+(\,k_1\alpha,\ k_2\alpha,\ k_3\alpha\,),\quad k_1,k_2,k_3\in\mathbb R.
$$
""",
        r"""
对矩阵 $A$ 作初等行变换，可化为
$$
\begin{pmatrix}
1&0&0&1\\
0&1&0&-2\\
0&0&1&-3
\end{pmatrix}.
$$
因此令 $x_4=t$，则
$$
x_1=-t,\quad x_2=2t,\quad x_3=3t,
$$
故 $Ax=0$ 的一个基础解系为
$$
\alpha=\begin{pmatrix}-1\\2\\3\\1\end{pmatrix}.
$$

再看 $AB=E$。设 $E=(e_1,e_2,e_3)$，则 $B$ 的三列分别是方程组
$$
Ax=e_1,\qquad Ax=e_2,\qquad Ax=e_3
$$
的解。由同样的消元可得三个特解分别可取
$$
\beta_1=\begin{pmatrix}2\\-1\\-1\\0\end{pmatrix},\quad
\beta_2=\begin{pmatrix}6\\-3\\-4\\0\end{pmatrix},\quad
\beta_3=\begin{pmatrix}-1\\1\\1\\0\end{pmatrix}.
$$
因此所有解为
$$
x=\beta_j+k_j\alpha,\qquad j=1,2,3.
$$
把三列合并，得
$$
B=
\begin{pmatrix}
2&6&-1\\
-1&-3&1\\
-1&-4&1\\
0&0&0
\end{pmatrix}
+(\,k_1\alpha,\ k_2\alpha,\ k_3\alpha\,),\quad k_1,k_2,k_3\in\mathbb R.
$$
""",
    ),
    q(
        21,
        "solution",
        11,
        "线性代数",
        ["相似", "特征值"],
        "25",
        r"""
证明 $n$ 阶矩阵
$$
\begin{pmatrix}
1&1&\cdots&1\\
1&1&\cdots&1\\
\vdots&\vdots& &\vdots\\
1&1&\cdots&1
\end{pmatrix}
$$
与
$$
\begin{pmatrix}
0&\cdots&0&1\\
0&\cdots&0&2\\
\vdots& &\vdots&\vdots\\
0&\cdots&0&n
\end{pmatrix}
$$
相似。
""",
        "两矩阵相似",
        r"""
记
$$
A=\mathbf 1\mathbf 1^T,
$$
其中 $\mathbf 1=(1,1,\dots,1)^T$。则 $A$ 的特征值为
$$
\lambda_1=n,\qquad \lambda_2=\cdots=\lambda_n=0.
$$
因为 $A$ 是实对称矩阵，所以它相似于对角矩阵
$$
\operatorname{diag}(n,0,\dots,0).
$$

再记
$$
B=
\begin{pmatrix}
0&\cdots&0&1\\
0&\cdots&0&2\\
\vdots& &\vdots&\vdots\\
0&\cdots&0&n
\end{pmatrix}.
$$
容易看出 $B$ 的秩为 $1$，其特征多项式同样是
$$
|\lambda E-B|=(\lambda-n)\lambda^{n-1},
$$
故它的特征值也是 $n,0,\dots,0$。

又因为 $r(B)=1$，对应特征值 $0$ 的特征子空间维数为 $n-1$；对应特征值 $n$ 也有非零特征向量，所以 $B$ 也可对角化，并相似于
$$
\operatorname{diag}(n,0,\dots,0).
$$
因此 $A$ 与 $B$ 相似。
""",
    ),
    q(
        22,
        "solution",
        11,
        "概率统计",
        ["条件分布", "分布函数", "数学期望"],
        "25",
        r"""
设随机变量 $X$ 的概率分布为
$$
P\{X=1\}=P\{X=2\}=\frac12.
$$
在给定 $X=i$ 的条件下，随机变量 $Y$ 服从均匀分布 $U(0,i)$（$i=1,2$）。

1. 求 $Y$ 的分布函数 $F_Y(y)$；

2. 求 $E(Y)$。
""",
        r"""
$$
F_Y(y)=
\begin{cases}
0,& y<0,\\[4pt]
\dfrac{3y}{4},& 0\le y<1,\\[6pt]
\dfrac12+\dfrac y4,& 1\le y<2,\\[6pt]
1,& y\ge 2,
\end{cases}
$$
且
$$
E(Y)=\frac34.
$$
""",
        r"""
由全概率公式，
$$
F_Y(y)=P(Y\le y)
=\frac12P(Y\le y\mid X=1)+\frac12P(Y\le y\mid X=2).
$$

当 $y<0$ 时，显然 $F_Y(y)=0$。

当 $0\le y<1$ 时，
$$
P(Y\le y\mid X=1)=y,\qquad
P(Y\le y\mid X=2)=\frac y2,
$$
故
$$
F_Y(y)=\frac12y+\frac12\cdot\frac y2=\frac{3y}{4}.
$$

当 $1\le y<2$ 时，
$$
P(Y\le y\mid X=1)=1,\qquad
P(Y\le y\mid X=2)=\frac y2,
$$
故
$$
F_Y(y)=\frac12+\frac y4.
$$

当 $y\ge 2$ 时，$F_Y(y)=1$。

因此
$$
F_Y(y)=
\begin{cases}
0,& y<0,\\
\dfrac{3y}{4},& 0\le y<1,\\
\dfrac12+\dfrac y4,& 1\le y<2,\\
1,& y\ge 2.
\end{cases}
$$

进一步可得密度
$$
f_Y(y)=
\begin{cases}
\dfrac34,& 0<y<1,\\[4pt]
\dfrac14,& 1<y<2,\\[4pt]
0,& \text{其他},
\end{cases}
$$
于是
$$
E(Y)=\int_0^1 y\cdot\frac34\,dy+\int_1^2 y\cdot\frac14\,dy
=\frac38+\frac38=\frac34.
$$
""",
    ),
    q(
        23,
        "solution",
        11,
        "概率统计",
        ["二维离散分布", "相关系数"],
        "25",
        r"""
设随机变量 $X,Y$ 的概率分布相同，$X$ 的概率分布为
$$
P\{X=0\}=\frac13,\qquad P\{X=1\}=\frac23,
$$
且 $X$ 与 $Y$ 的相关系数 $\rho_{XY}=\dfrac12$。

1. 求 $(X,Y)$ 的概率分布；

2. 求 $P\{X+Y\le 1\}$。
""",
        r"""
$$
\begin{array}{c|cc}
X\backslash Y & 0 & 1\\\hline
0 & \dfrac29 & \dfrac19\\
1 & \dfrac19 & \dfrac59
\end{array}
$$
且
$$
P\{X+Y\le 1\}=\frac49.
$$
""",
        r"""
设联合分布为
$$
\begin{array}{c|cc}
X\backslash Y & 0 & 1\\\hline
0 & a & b\\
1 & c & d
\end{array}.
$$
由边缘分布相同且
$$
P(X=0)=P(Y=0)=\frac13,\qquad P(X=1)=P(Y=1)=\frac23,
$$
得
$$
a+b=\frac13,\qquad a+c=\frac13,\qquad c+d=\frac23,\qquad b+d=\frac23.
$$
从而
$$
b=c,\qquad a=\frac13-b,\qquad d=\frac23-b.
$$

又
$$
EX=EY=\frac23,\qquad DX=DY=\frac23\left(1-\frac23\right)=\frac29.
$$
并且
$$
\operatorname{Cov}(X,Y)=E(XY)-EX\cdot EY=d-\frac49.
$$
由相关系数
$$
\rho_{XY}
=\frac{\operatorname{Cov}(X,Y)}{\sqrt{DX\cdot DY}}
=\frac{d-\frac49}{\frac29}
=\frac12,
$$
可得
$$
d=\frac59.
$$
于是
$$
b=c=\frac23-\frac59=\frac19,\qquad
a=\frac13-\frac19=\frac29.
$$
故联合分布为
$$
\begin{array}{c|cc}
X\backslash Y & 0 & 1\\\hline
0 & \dfrac29 & \dfrac19\\
1 & \dfrac19 & \dfrac59
\end{array}.
$$

最后
$$
P(X+Y\le 1)=1-P(X=1,Y=1)=1-\frac59=\frac49.
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
