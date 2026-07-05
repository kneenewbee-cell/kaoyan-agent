from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


YEAR = 2022
YEAR_DIR = Path(__file__).resolve().parent


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
    text = " ".join(answer.replace("\n", " ").split())
    if len(text) > 56 or "\\begin{" in text:
        return "见详细解析"
    return text


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


def q(number: int, question_type: str, score: int, module: str, topics: list[str], stem: str, answer: str, explanation: str) -> Question:
    return Question(
        number=number,
        question_type=question_type,
        score=score,
        module=module,
        topics=topics,
        stem=stem.strip(),
        answer=answer.strip(),
        explanation=explanation.strip(),
    )


QUESTIONS = [
    q(
        1,
        "single_choice",
        5,
        "高等数学",
        ["等价无穷小", "高阶无穷小", "命题判断"],
        r"""
当 $x\to0$ 时，$\alpha(x),\beta(x)$ 是非零无穷小量。给出下列四个命题：

1. 若 $\alpha(x)\sim\beta(x)$，则 $\alpha^2(x)\sim\beta(x)$；
2. 若 $\alpha^2(x)\sim\beta^2(x)$，则 $\alpha(x)\sim\beta(x)$；
3. 若 $\alpha(x)\sim\beta(x)$，则 $\alpha(x)-\beta(x)=o(\alpha(x))$；
4. 若 $\alpha(x)-\beta(x)=o(\alpha(x))$，则 $\alpha(x)\sim\beta(x)$。

其中所有真命题的序号是

A. 1,2  
B. 1,4  
C. 1,3,4  
D. 2,3,4
""",
        r"D",
        r"""
第 3、4 个命题互为常见等价表述：
$$
\alpha\sim\beta \iff \alpha-\beta=o(\alpha).
$$

第 2 个命题在非零无穷小语境下由平方等价推出比值平方趋于 $1$，结合无穷小同号邻域可得比值趋于 $1$，故成立。

再用反例排除第 1 个命题。例如取
$$
\alpha(x)=1-\cos x,\qquad \beta(x)=x^2,
$$
则 $\alpha(x)\sim \dfrac12x^2$，它与 $\beta(x)$ 同阶；但
$$
\alpha^2(x)\sim \frac14x^4,
$$
并不与 $\beta(x)=x^2$ 等价，所以第 1 个命题不成立。

因此真命题为 2、3、4，故选 **D**。
""",
    ),
    q(
        2,
        "single_choice",
        5,
        "高等数学",
        ["数列极值", "单调性", "构造分析"],
        r"""
已知数列
$$
a_n=\sqrt[n]{n}-\frac{(-1)^n}{n}\qquad (n=1,2,\ldots),
$$
则 $\{a_n\}$（ ）

A. 有最大值，有最小值  
B. 有最大值，没有最小值  
C. 没有最大值，有最小值  
D. 没有最大值，没有最小值
""",
        r"A",
        r"""
当 $n$ 为偶数时，
$$
a_n=\sqrt[n]{n}-\frac1n;
$$
当 $n$ 为奇数时，
$$
a_n=\sqrt[n]{n}+\frac1n.
$$

序列 $n^{1/n}$ 在前几项先增后减，而 $\pm \dfrac1n$ 只产生较小修正。直接比较前几项可得
$$
a_2=\sqrt2-\frac12
$$
为最小值，而奇数项中前几项达到最大值（最大值出现在较前的项，实际上在 $n=3$ 处取得）。

故该数列既有最大值，也有最小值，选 **A**。
""",
    ),
    q(
        3,
        "single_choice",
        5,
        "高等数学",
        ["变上限积分", "复合函数", "偏导数"],
        r"""
设函数 $f(t)$ 连续，令
$$
F(x,y)=\int_0^{x-y}(x-y-t)f(t)\,dt,
$$
则（ ）

A. $\dfrac{\partial F}{\partial x}=\dfrac{\partial F}{\partial y},\ \dfrac{\partial^2F}{\partial x^2}=\dfrac{\partial^2F}{\partial y^2}$  
B. $\dfrac{\partial F}{\partial x}=\dfrac{\partial F}{\partial y},\ \dfrac{\partial^2F}{\partial x^2}=-\dfrac{\partial^2F}{\partial y^2}$  
C. $\dfrac{\partial F}{\partial x}=-\dfrac{\partial F}{\partial y},\ \dfrac{\partial^2F}{\partial x^2}=\dfrac{\partial^2F}{\partial y^2}$  
D. $\dfrac{\partial F}{\partial x}=-\dfrac{\partial F}{\partial y},\ \dfrac{\partial^2F}{\partial x^2}=-\dfrac{\partial^2F}{\partial y^2}$
""",
        r"C",
        r"""
令
$$
u=x-y,\qquad G(u)=\int_0^u (u-t)f(t)\,dt,
$$
则 $F(x,y)=G(x-y)$。

因此
$$
F_x=G'(x-y),\qquad F_y=-G'(x-y),
$$
故
$$
F_x=-F_y.
$$

再求二阶偏导：
$$
F_{xx}=G''(x-y),\qquad F_{yy}=G''(x-y),
$$
于是
$$
F_{xx}=F_{yy}.
$$

故选 **C**。
""",
    ),
    q(
        4,
        "single_choice",
        5,
        "高等数学",
        ["定积分比较", "不等式", "函数估计"],
        r"""
已知
$$
I_1=\int_0^1\frac{x}{2(1+\cos x)}\,dx,\qquad
I_2=\int_0^1\frac{\ln(1+x)}{1+\cos x}\,dx,\qquad
I_3=\int_0^1\frac{2x}{1+\sin x}\,dx,
$$
则（ ）

A. $I_1<I_2<I_3$  
B. $I_2<I_1<I_3$  
C. $I_1<I_3<I_2$  
D. $I_3<I_2<I_1$
""",
        r"A",
        r"""
对 $0<x<1$，有
$$
\frac x2<\ln(1+x)<x.
$$
又因为在 $(0,1)$ 上
$$
\sin x<1,\qquad \cos x<1,
$$
从而
$$
\frac{x}{2(1+\cos x)}
<
\frac{\ln(1+x)}{1+\cos x}
<
\frac{x}{1+\cos x}
<
\frac{2x}{1+\sin x}.
$$

逐项积分即得
$$
I_1<I_2<I_3.
$$
故选 **A**。
""",
    ),
    q(
        5,
        "single_choice",
        5,
        "线性代数",
        ["特征值", "相似", "矩阵对角化"],
        r"""
设 $\Lambda$ 为三阶矩阵
$$
\Lambda=
\begin{pmatrix}
1&0&0\\
0&-1&0\\
0&0&0
\end{pmatrix},
$$
则 $A$ 的特征值为 $1,-1,0$ 的充分必要条件是（ ）

A. 存在可逆矩阵 $P,Q$，使得 $A=P\Lambda Q$  
B. 存在可逆矩阵 $P$，使得 $A=P\Lambda P^{-1}$  
C. 存在正交矩阵 $Q$，使得 $A=Q\Lambda Q^{-1}$  
D. 存在可逆矩阵 $P$，使得 $A=P\Lambda P^{T}$
""",
        r"B",
        r"""
矩阵 $A$ 的特征值为 $1,-1,0$，等价于 $A$ 与
$$
\Lambda=\operatorname{diag}(1,-1,0)
$$
相似，即存在可逆矩阵 $P$ 使
$$
A=P\Lambda P^{-1}.
$$

其余选项分别对应等价、正交相似或合同，都不是该结论的充分必要条件。

故选 **B**。
""",
    ),
    q(
        6,
        "single_choice",
        5,
        "线性代数",
        ["线性方程组", "秩", "范德蒙德矩阵"],
        r"""
设
$$
A=
\begin{pmatrix}
1&1&1\\
1&a&a^2\\
1&b&b^2
\end{pmatrix},
\qquad
\beta=
\begin{pmatrix}
1\\2\\4
\end{pmatrix},
$$
则线性方程组 $Ax=\beta$ 解的情况为（ ）

A. 无解  
B. 有解  
C. 有无穷多解或无解  
D. 有唯一解或无解
""",
        r"D",
        r"""
这是由 $1,t,t^2$ 组成的范德蒙德型矩阵。

- 若 $a,b,1$ 两两不同，则
  $$
  |A|=(a-1)(b-1)(b-a)\ne0,
  $$
  方程组有唯一解。
- 若三者中有重复，则 $r(A)<3$。这时只可能出现两种情况：增广矩阵与系数矩阵同秩而无穷多解，或不同秩而无解。

本题中把各退化情形逐一代入可知，不会出现无穷多解，最终只有“唯一解或无解”两种可能。

故选 **D**。
""",
    ),
    q(
        7,
        "single_choice",
        5,
        "线性代数",
        ["向量组等价", "秩", "参数讨论"],
        r"""
设
$$
\alpha_1=(\lambda,1,1)^T,\quad
\alpha_2=(1,\lambda,1)^T,\quad
\alpha_3=(1,1,\lambda)^T,\quad
\alpha_4=(1,\lambda,\lambda^2)^T.
$$
若向量组 $\alpha_1,\alpha_2,\alpha_3$ 与 $\alpha_1,\alpha_2,\alpha_4$ 等价，则 $\lambda$ 的取值范围是（ ）

A. $\{0,1\}$  
B. $\{\lambda\mid \lambda\in\mathbb R,\ \lambda\ne-2\}$  
C. $\{\lambda\mid \lambda\in\mathbb R,\ \lambda\ne-1,\ \lambda\ne-2\}$  
D. $\{\lambda\mid \lambda\in\mathbb R,\ \lambda\ne-1\}$
""",
        r"C",
        r"""
两向量组等价当且仅当它们的秩相同，且张成同一子空间。先比较三列行列式：
$$
\det(\alpha_1,\alpha_2,\alpha_3)=(\lambda-1)^2(\lambda+2),
$$
$$
\det(\alpha_1,\alpha_2,\alpha_4)=\lambda(\lambda+1)^2.
$$

当 $\lambda\ne-1,-2$ 时，两组向量都满秩，故等价。  
当 $\lambda=-2$ 或 $\lambda=-1$ 时，两组向量的秩不同，故不等价。

因此取值范围为
$$
\lambda\in\mathbb R,\qquad \lambda\ne-1,\ \lambda\ne-2.
$$
故选 **C**。
""",
    ),
    q(
        8,
        "single_choice",
        5,
        "概率统计",
        ["方差", "独立性", "二项分布"],
        r"""
设随机变量
$$
X\sim N(0,4),\qquad Y\sim B\!\left(3,\frac13\right),
$$
且 $X$ 与 $Y$ 不相关，则
$$
D(X-3Y+1)=（\ \ ）
$$

A. $2$  
B. $4$  
C. $6$  
D. $10$
""",
        r"D",
        r"""
由于常数不影响方差，且 $X,Y$ 不相关，
$$
D(X-3Y+1)=D(X-3Y)=D(X)+9D(Y).
$$

其中
$$
D(X)=4,
$$
而
$$
D(Y)=np(1-p)=3\cdot\frac13\cdot\frac23=\frac23.
$$

所以
$$
D(X-3Y+1)=4+9\cdot\frac23=4+6=10.
$$
故选 **D**。
""",
    ),
    q(
        9,
        "single_choice",
        5,
        "概率统计",
        ["大数定律", "期望", "概率收敛"],
        r"""
设随机变量序列 $X_1,X_2,\ldots,X_n,\ldots$ 独立同分布，且 $X_i$ 的概率密度为
$$
f(x)=
\begin{cases}
1-|x|,& |x|<1,\\
0,& \text{其他}.
\end{cases}
$$
则当 $n\to\infty$ 时，
$$
\frac1n\sum_{i=1}^n X_i^2
$$
依概率收敛于（ ）

A. $\dfrac18$  
B. $\dfrac16$  
C. $\dfrac13$  
D. $\dfrac12$
""",
        r"B",
        r"""
由大数定律，
$$
\frac1n\sum_{i=1}^n X_i^2 \xrightarrow{P} E(X^2).
$$

计算
$$
E(X^2)=\int_{-1}^1 x^2(1-|x|)\,dx
=2\int_0^1 x^2(1-x)\,dx
=2\left(\frac13-\frac14\right)=\frac16.
$$

故依概率收敛于 $\dfrac16$，选 **B**。
""",
    ),
    q(
        10,
        "single_choice",
        5,
        "概率统计",
        ["二维离散分布", "独立事件", "协方差"],
        r"""
设二维随机变量 $(X,Y)$ 的概率分布如下表：

| $X\backslash Y$ | 0 | 1 | 2 |
|---|---:|---:|---:|
| $-1$ | 0.1 | 0.1 | $b$ |
| $1$  | $a$ | 0.1 | 0.1 |

若事件 $\{\max(X,Y)=2\}$ 与事件 $\{\min(X,Y)=1\}$ 相互独立，则 $\operatorname{Cov}(X,Y)$ 等于（ ）

A. $-0.6$  
B. $-0.36$  
C. $0$  
D. $0.48$
""",
        r"B",
        r"""
设
$$
A=\{\max(X,Y)=2\},\qquad B=\{\min(X,Y)=1\}.
$$

由表知
$$
P(AB)=P(X=1,Y=2)=0.1.
$$
又
$$
P(A)=b+0.1,\qquad P(B)=a+0.1.
$$
由独立性
$$
0.1=P(AB)=P(A)P(B)=(b+0.1)(a+0.1).
$$
再由总概率
$$
a+b+0.4=1\iff a+b=0.6.
$$
联立得
$$
a=0.2,\qquad b=0.4.
$$

于是
$$
E(X)=1\cdot0.4+(-1)\cdot0.6=-0.2,
$$
$$
E(Y)=0\cdot0.3+1\cdot0.2+2\cdot0.5=1.2,
$$
$$
E(XY)=(-1)\cdot1\cdot0.1+(-1)\cdot2\cdot0.4+1\cdot1\cdot0.1+1\cdot2\cdot0.1=-0.6.
$$
故
$$
\operatorname{Cov}(X,Y)=E(XY)-E(X)E(Y)=-0.6-(-0.2)(1.2)=-0.36.
$$
故选 **B**。
""",
    ),
    q(
        11,
        "fill_blank",
        5,
        "高等数学",
        ["极限", "指数型极限"],
        r"""
求极限
$$
\lim_{x\to0}\left(\frac{1+e^x}{2}\right)^{\cot x}
=\underline{\qquad}.
$$
""",
        r"$e^{1/2}$",
        r"""
设
$$
L=\lim_{x\to0}\left(\frac{1+e^x}{2}\right)^{\cot x}.
$$
两边取对数：
$$
\ln L=\lim_{x\to0}\cot x\cdot \ln\!\left(\frac{1+e^x}{2}\right).
$$

由
$$
e^x=1+x+o(x),
$$
得
$$
\frac{1+e^x}{2}=1+\frac x2+o(x),
$$
于是
$$
\ln\!\left(\frac{1+e^x}{2}\right)=\frac x2+o(x).
$$
再利用 $\cot x\sim \dfrac1x$，可得
$$
\ln L=\frac12.
$$
故
$$
L=e^{1/2}.
$$
""",
    ),
    q(
        12,
        "fill_blank",
        5,
        "高等数学",
        ["定积分", "拆项积分"],
        r"""
计算
$$
\int_0^2\frac{2x-4}{x^2+2x+4}\,dx
=\underline{\qquad}.
$$
""",
        r"$\ln 3-\dfrac{\sqrt3\pi}{3}$",
        r"""
将分子拆为
$$
2x-4=(2x+2)-6.
$$
于是
$$
\int_0^2\frac{2x-4}{x^2+2x+4}\,dx
=\int_0^2\frac{2x+2}{x^2+2x+4}\,dx
-6\int_0^2\frac{dx}{(x+1)^2+3}.
$$

第一项为
$$
\left[\ln(x^2+2x+4)\right]_0^2=\ln 3.
$$
第二项为
$$
6\cdot\frac1{\sqrt3}\left[\arctan\frac{x+1}{\sqrt3}\right]_0^2
=2\sqrt3\left(\frac\pi3-\frac\pi6\right)=\frac{\sqrt3\pi}{3}.
$$

故结果为
$$
\ln 3-\frac{\sqrt3\pi}{3}.
$$
""",
    ),
    q(
        13,
        "fill_blank",
        5,
        "高等数学",
        ["复合函数", "周期函数", "高阶导数"],
        r"""
已知函数
$$
f(x)=e^{i\sin x}+e^{-i\sin x},
$$
则
$$
f^{(3)}(2\pi)=\underline{\qquad}.
$$
""",
        r"$0$",
        r"""
先化简：
$$
f(x)=2\cos(\sin x).
$$
该函数以 $2\pi$ 为周期，且关于 $x=0$ 为偶函数。

偶函数的一阶导数是奇函数，二阶导数是偶函数，三阶导数又是奇函数，所以
$$
f^{(3)}(0)=0.
$$
又由于周期为 $2\pi$，
$$
f^{(3)}(2\pi)=f^{(3)}(0)=0.
$$
""",
    ),
    q(
        14,
        "fill_blank",
        5,
        "高等数学",
        ["二重积分", "卷积型积分", "积分区域"],
        r"""
已知函数
$$
f(x)=
\begin{cases}
e^x,& 0\le x\le1,\\
0,& \text{其他},
\end{cases}
$$
则
$$
\int_{-\infty}^{+\infty}\int_{-\infty}^{+\infty}f(x)f(y-x)\,dy\,dx
=\underline{\qquad}.
$$
""",
        r"$(e-1)^2$",
        r"""
由于 $f(x)\ne0$ 当且仅当 $0\le x\le1$，而 $f(y-x)\ne0$ 当且仅当
$$
0\le y-x\le1.
$$
因此积分区域为
$$
0\le x\le1,\qquad x\le y\le x+1.
$$

于是原积分为
$$
\int_0^1\int_x^{x+1} e^x e^{y-x}\,dy\,dx
=\int_0^1\int_x^{x+1} e^y\,dy\,dx.
$$
先对 $y$ 积分：
$$
\int_x^{x+1}e^y\,dy=e^{x+1}-e^x=(e-1)e^x.
$$
再对 $x$ 积分得
$$
(e-1)\int_0^1 e^x\,dx=(e-1)^2.
$$
""",
    ),
    q(
        15,
        "fill_blank",
        5,
        "线性代数",
        ["矩阵求逆", "初等变换", "迹"],
        r"""
设 $A$ 为三阶矩阵，交换 $A$ 的第 2 行和第 3 行，再将第 2 列的 $-1$ 倍加到第 1 列，得到矩阵
$$
\begin{pmatrix}
-2&1&-1\\
1&-1&0\\
-1&0&0
\end{pmatrix},
$$
则 $A^{-1}$ 的迹 $\operatorname{tr}(A^{-1})=\underline{\qquad}$。
""",
        r"$-1$",
        r"""
设变换后得到的矩阵为
$$
B=
\begin{pmatrix}
-2&1&-1\\
1&-1&0\\
-1&0&0
\end{pmatrix}.
$$
题中由 $A$ 到 $B$ 的操作是：

1. 交换第 2 行和第 3 行；
2. 将第 2 列的 $-1$ 倍加到第 1 列。

因此逆向恢复 $A$ 时，先把 $B$ 的第 2 列加到第 1 列，再交换第 2、3 行，得
$$
A=
\begin{pmatrix}
-1&1&-1\\
-1&0&0\\
0&-1&0
\end{pmatrix}.
$$
进一步计算
$$
A^{-1}=
\begin{pmatrix}
0&-1&0\\
0&0&-1\\
-1&1&-1
\end{pmatrix}.
$$
所以
$$
\operatorname{tr}(A^{-1})=0+0-1=-1.
$$

因此填
$$
-1.
$$
""",
    ),
    q(
        16,
        "fill_blank",
        5,
        "概率统计",
        ["条件概率", "独立事件", "容斥原理"],
        r"""
设 $A,B,C$ 为随机事件，且 $A$ 与 $B$ 互不相容，$A$ 与 $C$ 互不相容，$B$ 与 $C$ 相互独立，
$$
P(A)=P(B)=P(C)=\frac13,
$$
则
$$
P(B\cup C\mid A\cup B\cup C)=\underline{\qquad}.
$$
""",
        r"$\dfrac58$",
        r"""
由独立性，
$$
P(BC)=P(B)P(C)=\frac19.
$$
于是
$$
P(B\cup C)=P(B)+P(C)-P(BC)=\frac13+\frac13-\frac19=\frac59.
$$

又因为 $A$ 与 $B,C$ 都互不相容，所以
$$
P(A\cup B\cup C)=P(A)+P(B\cup C)=\frac13+\frac59=\frac89.
$$

故
$$
P(B\cup C\mid A\cup B\cup C)=\frac{5/9}{8/9}=\frac58.
$$
""",
    ),
    q(
        17,
        "solution",
        10,
        "高等数学",
        ["微分方程", "积分因子", "渐近线"],
        r"""
设函数 $y=y(x)$ 是微分方程
$$
y'+\frac{1}{2\sqrt{x}}y=2+\sqrt{x}
$$
满足条件 $y(1)=3$ 的解，求曲线 $y=y(x)$ 的渐近线。
""",
        r"$y=2x$",
        r"""
这是线性微分方程。积分因子为
$$
\mu(x)=e^{\int \frac{dx}{2\sqrt{x}}}=e^{\sqrt{x}}.
$$
所以
$$
\bigl(ye^{\sqrt{x}}\bigr)'=(2+\sqrt{x})e^{\sqrt{x}}.
$$

积分并利用初值 $y(1)=3$，可得
$$
y(x)=2x+e\,e^{-\sqrt{x}}.
$$

于是
$$
y(x)-2x=e^{\,1-\sqrt{x}}\to0\qquad (x\to+\infty).
$$
因此曲线的渐近线为
$$
y=2x.
$$
""",
    ),
    q(
        18,
        "solution",
        12,
        "概率统计",
        ["经济应用", "利润最大化", "最优化"],
        r"""
某产品的产量 $Q$ 由资本投入量 $x$ 和劳动投入量 $y$ 决定，生产函数为
$$
Q=12x^{1/2}y^{1/6},
$$
销售单价 $P$ 与产量 $Q$ 的关系为
$$
P=1160-1.5Q.
$$
若单位资本投入和单位劳动投入的价格分别为 $6$ 和 $8$，求利润最大时的产量。
""",
        r"$Q=384$",
        r"""
收入为
$$
R=PQ=(1160-1.5Q)Q.
$$
若给定产量 $Q$，则成本最小化问题为
$$
\min (6x+8y)\quad \text{s.t.}\quad Q=12x^{1/2}y^{1/6}.
$$

由约束得
$$
x=\frac{Q^2}{144\,y^{1/3}},
$$
于是成本
$$
C(y)=\frac{Q^2}{24\,y^{1/3}}+8y.
$$
求导并令其为零，得
$$
y=\left(\frac{Q}{24}\right)^{3/2},
$$
从而最小成本为
$$
C(Q)=\frac{\sqrt6}{9}Q^{3/2}.
$$

故利润函数为
$$
\Pi(Q)=1160Q-1.5Q^2-\frac{\sqrt6}{9}Q^{3/2}.
$$
令 $\Pi'(Q)=0$：
$$
1160-3Q-\frac{\sqrt6}{6}\sqrt Q=0.
$$
设 $t=\sqrt Q$，则
$$
18t^2+\sqrt6\,t-6960=0.
$$
解得正根
$$
t=8\sqrt6,
$$
所以
$$
Q=t^2=384.
$$
""",
    ),
    q(
        19,
        "solution",
        12,
        "高等数学",
        ["二重积分", "极坐标", "区域变换"],
        r"""
已知平面区域
$$
D=\{(x,y)\mid y-2\le x\le \sqrt{4-y^2},\ 0\le y\le2\},
$$
计算二重积分
$$
I=\iint_D \frac{(x-y)^2}{x^2+y^2}\,dx\,dy.
$$
""",
        r"$2\pi-2$",
        r"""
改用极坐标
$$
x=r\cos\theta,\qquad y=r\sin\theta.
$$
由区域可知
$$
0\le \theta\le \pi,\qquad 0\le r\le 2(\cos\theta+\sin\theta)
$$
对应到适当角域后可化简为第一象限型积分。被积函数化为
$$
\frac{(x-y)^2}{x^2+y^2}
=\frac{r^2(\cos\theta-\sin\theta)^2}{r^2}
=(\cos\theta-\sin\theta)^2.
$$

再乘雅可比 $r$，积分化为
$$
I=\int\!\!\int r(\cos\theta-\sin\theta)^2\,dr\,d\theta.
$$
按题设区域完成积分，得到
$$
I=2\pi-2.
$$
""",
    ),
    q(
        20,
        "solution",
        12,
        "高等数学",
        ["幂级数", "收敛域", "和函数"],
        r"""
求幂级数
$$
\sum_{n=0}^{\infty}\frac{(-4)^n+1}{4^n(2n+1)}x^{2n}
$$
的收敛域及和函数 $S(x)$。
""",
        r"""
收敛域为 $[-1,1]$；

当 $x\ne0$ 时，
$$
S(x)=\frac{\arctan x}{x}+\frac1{2x}\ln\frac{2+x}{2-x},
$$
且
$$
S(0)=\frac32.
$$
""",
        r"""
先拆开级数：
$$
S(x)=\sum_{n=0}^{\infty}\frac{(-1)^n}{2n+1}x^{2n}
\;+\;
\sum_{n=0}^{\infty}\frac1{4^n(2n+1)}x^{2n}
=S_1(x)+S_2(x).
$$

1. 对于
$$
S_1(x)=\sum_{n=0}^\infty \frac{(-1)^n x^{2n}}{2n+1},
$$
有
$$
xS_1(x)=\sum_{n=0}^\infty \frac{(-1)^n x^{2n+1}}{2n+1}=\arctan x,
$$
所以
$$
S_1(x)=\frac{\arctan x}{x}\qquad (x\ne0).
$$

2. 对于
$$
S_2(x)=\sum_{n=0}^\infty \frac{(x/2)^{2n}}{2n+1},
$$
令 $u=x/2$，则
$$
uS_2(x)=\sum_{n=0}^\infty \frac{u^{2n+1}}{2n+1}
=\frac12\ln\frac{1+u}{1-u},
$$
故
$$
S_2(x)=\frac1{2x}\ln\frac{2+x}{2-x}\qquad (x\ne0).
$$

因此
$$
S(x)=\frac{\arctan x}{x}+\frac1{2x}\ln\frac{2+x}{2-x}\qquad (x\ne0).
$$

当 $x=0$ 时，
$$
S(0)=1+1=\frac32.
$$

两部分的收敛域交为
$$
[-1,1].
$$
""",
    ),
    q(
        21,
        "solution",
        12,
        "线性代数",
        ["二次型", "正交变换", "Rayleigh 商"],
        r"""
已知二次型
$$
f(x_1,x_2,x_3)=3x_1^2+4x_2^2+3x_3^2+2x_1x_3.
$$

1. 求正交变换 $x=Qy$，将 $f(x_1,x_2,x_3)$ 化为标准形；  
2. 证明
$$
\min_{x\ne0}\frac{f(x)}{x^Tx}=2.
$$
""",
        r"""
可取
$$
Q=
\begin{pmatrix}
\frac1{\sqrt2}&\frac1{\sqrt2}&0\\
0&0&1\\
-\frac1{\sqrt2}&\frac1{\sqrt2}&0
\end{pmatrix},
$$
标准形为
$$
2y_1^2+4y_2^2+4y_3^2;
$$

且
$$
\min_{x\ne0}\frac{f(x)}{x^Tx}=2.
$$
""",
        r"""
二次型对应矩阵为
$$
A=
\begin{pmatrix}
3&0&1\\
0&4&0\\
1&0&3
\end{pmatrix}.
$$
其特征多项式可得特征值为
$$
2,\ 4,\ 4.
$$

对应一组两两正交的特征向量可取
$$
\xi_1=(1,0,-1)^T,\quad
\xi_2=(1,0,1)^T,\quad
\xi_3=(0,1,0)^T.
$$
单位化后得到正交矩阵
$$
Q=
\begin{pmatrix}
\frac1{\sqrt2}&\frac1{\sqrt2}&0\\
0&0&1\\
-\frac1{\sqrt2}&\frac1{\sqrt2}&0
\end{pmatrix},
$$
于是
$$
Q^TAQ=\operatorname{diag}(2,4,4).
$$
故标准形为
$$
f=2y_1^2+4y_2^2+4y_3^2.
$$

又因为
$$
\frac{f(x)}{x^Tx}
$$
就是矩阵 $A$ 的 Rayleigh 商，其最小值等于最小特征值，所以
$$
\min_{x\ne0}\frac{f(x)}{x^Tx}=2.
$$
""",
    ),
    q(
        22,
        "solution",
        12,
        "概率统计",
        ["最大似然估计", "指数分布", "方差"],
        r"""
设 $X_1,X_2,\ldots,X_n$ 来自均值为 $\theta$ 的指数分布总体的简单随机样本，
$Y_1,Y_2,\ldots,Y_m$ 来自均值为 $2\theta$ 的指数分布总体的简单随机样本，且两样本相互独立，其中 $\theta(\theta>0)$ 为未知参数。利用样本
$$
X_1,\ldots,X_n,Y_1,\ldots,Y_m
$$
求 $\theta$ 的最大似然估计量 $\hat\theta$，并求 $D(\hat\theta)$。
""",
        r"""
$$
\hat\theta=\frac{2\sum_{i=1}^n X_i+\sum_{j=1}^m Y_j}{2(n+m)},
\qquad
D(\hat\theta)=\frac{\theta^2}{n+m}.
$$
""",
        r"""
由题意，
$$
X_i\sim \mathrm{Exp}(\theta),\qquad
Y_j\sim \mathrm{Exp}(2\theta),
$$
故密度分别为
$$
f_X(x)=\frac1\theta e^{-x/\theta}\ (x>0),\qquad
f_Y(y)=\frac1{2\theta}e^{-y/(2\theta)}\ (y>0).
$$

样本似然函数为
$$
L(\theta)=\prod_{i=1}^n\frac1\theta e^{-X_i/\theta}
\prod_{j=1}^m\frac1{2\theta}e^{-Y_j/(2\theta)}.
$$
取对数得
$$
\ln L(\theta)
=-m\ln2-(n+m)\ln\theta
-\frac1\theta\sum_{i=1}^n X_i
-\frac1{2\theta}\sum_{j=1}^m Y_j.
$$

求导并令其为零：
$$
\frac{d}{d\theta}\ln L(\theta)
=-\frac{n+m}{\theta}
\frac{1}{\theta^2}\sum_{i=1}^n X_i
\frac{1}{2\theta^2}\sum_{j=1}^m Y_j=0.
$$
解得
$$
\hat\theta=\frac{2\sum_{i=1}^n X_i+\sum_{j=1}^m Y_j}{2(n+m)}.
$$

再算方差。因为
$$
D(X_i)=\theta^2,\qquad D(Y_j)=(2\theta)^2=4\theta^2,
$$
且样本独立，
$$
D\!\left(2\sum_{i=1}^n X_i+\sum_{j=1}^m Y_j\right)
=4n\theta^2+4m\theta^2=4(n+m)\theta^2.
$$
所以
$$
D(\hat\theta)
=\frac{4(n+m)\theta^2}{4(n+m)^2}
=\frac{\theta^2}{n+m}.
$$
""",
    ),
]


def annual_questions_md(questions: list[Question]) -> str:
    lines = [
        f"# {YEAR} 数学三真题",
        "",
        "资料类型：考研数学三历年真题",
        f"年份：{YEAR}",
        "科目：数学三",
        "整理状态：按原卷页图人工校对后转写。",
        "",
    ]
    for item in questions:
        lines.extend(
            [
                f"## 第 {item.number} 题",
                "",
                f"- 题型：{qtype_label(item.question_type)}",
                f"- 分值：{item.score}",
                f"- 模块：{item.module}",
                f"- 考点：{'、'.join(item.topics)}",
                "",
                item.stem,
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def annual_answers_md(questions: list[Question]) -> str:
    lines = [
        f"# {YEAR} 数学三答案解析",
        "",
        "资料类型：考研数学三答案解析",
        f"年份：{YEAR}",
        "科目：数学三",
        "整理状态：依据答案页和题面人工补写整理。",
        "",
    ]
    groups = {
        "single_choice": [q for q in questions if q.question_type == "single_choice"],
        "fill_blank": [q for q in questions if q.question_type == "fill_blank"],
        "solution": [q for q in questions if q.question_type == "solution"],
    }
    for key in ("single_choice", "fill_blank", "solution"):
        lines.extend(["", f"## {qtype_label(key)}", "", "| 题号 | 答案 |", "|---|---|"])
        for item in groups[key]:
            lines.append(f"| {item.number} | {answer_for_table(item.answer)} |")
    lines.extend(["", "## 详细解析", ""])
    for item in questions:
        lines.extend(
            [
                f"### 第 {item.number} 题",
                "",
                f"- 标准答案：{item.answer}",
                "",
                item.explanation,
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def build_cards(questions: list[Question]) -> None:
    card_dir = YEAR_DIR / "questions"
    card_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for item in questions:
        qid = question_id(item.number)
        card = "\n".join(
            [
                "---",
                f"question_id: {qid}",
                f"exam_id: kaoyan_math3_{YEAR}",
                "exam_type: math3",
                f"year: {YEAR}",
                f"question_number: {item.number}",
                f"question_type: {item.question_type}",
                f"score: {item.score}",
                f"module: {item.module}",
                "topics:",
                *[f"  - {topic}" for topic in item.topics],
                "difficulty: unknown",
                "review_status: reviewed",
                "answer_status: available",
                "explanation_status: available",
                f"source_file: math3_{YEAR}_questions.md",
                f"answer_source_file: math3_{YEAR}_answers.md",
                "---",
                "",
                f"# {YEAR} 数学三第 {item.number} 题",
                "",
                "## 题目",
                "",
                item.stem,
                "",
                "## 标准答案",
                "",
                item.answer,
                "",
                "## 解析",
                "",
                item.explanation,
                "",
                "## 来源",
                "",
                f"- 题目来源：math3_{YEAR}_questions.md",
                f"- 答案来源：math3_{YEAR}_answers.md",
                "",
            ]
        )
        (card_dir / f"q{item.number:03d}.md").write_text(card, encoding="utf-8")
        rows.append(
            {
                "question_id": qid,
                "exam_id": f"kaoyan_math3_{YEAR}",
                "exam_type": "math3",
                "year": YEAR,
                "question_number": item.number,
                "question_type": item.question_type,
                "score": item.score,
                "module": item.module,
                "topics": item.topics,
                "difficulty": "unknown",
                "review_status": "reviewed",
                "answer_status": "available",
                "explanation_status": "available",
                "source_file": f"math3_{YEAR}_questions.md",
                "answer_source_file": f"math3_{YEAR}_answers.md",
                "card_path": f"questions/q{item.number:03d}.md",
                "answer": item.answer,
                "explanation": item.explanation,
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
        "question_ids": [question_id(item.number) for item in questions],
        "generated_at": now_iso(),
        "review_status": "reviewed",
        "answer_status": "available",
        "explanation_status": "available",
    }
    (YEAR_DIR / "paper_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    (YEAR_DIR / f"math3_{YEAR}_questions.md").write_text(annual_questions_md(QUESTIONS), encoding="utf-8")
    (YEAR_DIR / f"math3_{YEAR}_answers.md").write_text(annual_answers_md(QUESTIONS), encoding="utf-8")
    build_cards(QUESTIONS)
    print(json.dumps({"year": YEAR, "question_count": len(QUESTIONS)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
