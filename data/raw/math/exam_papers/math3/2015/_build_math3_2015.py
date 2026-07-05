from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[6]
YEAR = 2015
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
        ["数列极限", "子列"],
        "18",
        r"""
设 $\{x_n\}$ 是数列，下列命题中不正确的是（ ）

A. 若 $\lim\limits_{n\to\infty}x_n=a$，则 $\lim\limits_{n\to\infty}x_{2n}=\lim\limits_{n\to\infty}x_{2n+1}=a$  
B. 若 $\lim\limits_{n\to\infty}x_{2n}=\lim\limits_{n\to\infty}x_{2n+1}=a$，则 $\lim\limits_{n\to\infty}x_n=a$  
C. 若 $\lim\limits_{n\to\infty}x_n=a$，则 $\lim\limits_{n\to\infty}x_{3n}=\lim\limits_{n\to\infty}x_{3n+1}=a$  
D. 若 $\lim\limits_{n\to\infty}x_{3n}=\lim\limits_{n\to\infty}x_{3n+1}=a$，则 $\lim\limits_{n\to\infty}x_n=a$
""",
        r"D",
        r"""
命题 A、C 都是“收敛数列的子列仍收敛且极限相同”的直接结论。

命题 B 也正确：若偶数项与奇数项都收敛到同一极限 $a$，则全体项都收敛到 $a$。

命题 D 错，可举反例
$$
x_n=
\begin{cases}
a+\dfrac1n, & n=3m,\\[4pt]
a+\dfrac1n, & n=3m-1,\\[4pt]
n, & n=3m-2.
\end{cases}
$$
则
$$
\lim_{n\to\infty}x_{3n}=\lim_{n\to\infty}x_{3n+1}=a,
$$
但 $\{x_n\}$ 不收敛。故选 D。
""",
    ),
    q(
        2,
        "single_choice",
        4,
        "高等数学",
        ["拐点", "二阶导数图像"],
        "18",
        r"""
设函数 $f(x)$ 在 $(-\infty,+\infty)$ 内连续，其二阶导数 $f''(x)$ 的图形如下图所示，则曲线 $y=f(x)$ 的拐点个数为（ ）

![2015 数学三第 2 题二阶导数图像](../images/question_assets/q002_f2_graph.png)

A. $0$  
B. $1$  
C. $2$  
D. $3$
""",
        r"C",
        r"""
由于 $f(x)$ 连续，拐点只能出现在 $f''(x)=0$ 或 $f''(x)$ 不存在且其符号发生变化的地方。

从图像可看出，在点 $A$ 左右两侧 $f''(x)>0$，故 $A$ 不是拐点对应位置；而在 $x=0$ 与 $x=B$ 附近，$f''(x)$ 的符号发生变化，因此对应两处拐点。

故曲线 $y=f(x)$ 有 $2$ 个拐点，选 C。
""",
    ),
    q(
        3,
        "single_choice",
        4,
        "高等数学",
        ["二重积分", "极坐标变换"],
        "18",
        r"""
设
$$
D=\{(x,y)\mid x^2+y^2\le2x,\ x^2+y^2\le2y\},
$$
函数 $f(x,y)$ 在 $D$ 上连续，则
$$
\iint_D f(x,y)\,dxdy
$$
等于（ ）

![2015 数学三第 3 题积分区域示意图](../images/question_assets/q003_region_diagram.png)

A. $\displaystyle \int_0^{\pi/4}d\theta\int_0^{2\cos\theta}f(r\cos\theta,r\sin\theta)\,rdr+\int_{\pi/4}^{\pi/2}d\theta\int_0^{2\sin\theta}f(r\cos\theta,r\sin\theta)\,rdr$  
B. $\displaystyle \int_0^{\pi/4}d\theta\int_0^{2\sin\theta}f(r\cos\theta,r\sin\theta)\,rdr+\int_{\pi/4}^{\pi/2}d\theta\int_0^{2\cos\theta}f(r\cos\theta,r\sin\theta)\,rdr$  
C. $\displaystyle 2\int_0^1dx\int_{1-\sqrt{1-x^2}}^x f(x,y)\,dy$  
D. $\displaystyle 2\int_0^1dx\int_x^{\sqrt{2x-x^2}} f(x,y)\,dy$
""",
        r"B",
        r"""
圆 $x^2+y^2=2x$ 化为极坐标是
$$
r=2\cos\theta,
$$
圆 $x^2+y^2=2y$ 化为极坐标是
$$
r=2\sin\theta.
$$
因此公共区域在 $0\le\theta\le\pi/2$ 内，其中
$$
0\le\theta\le\frac\pi4
$$
时上界取 $2\sin\theta$，
$$
\frac\pi4\le\theta\le\frac\pi2
$$
时上界取 $2\cos\theta$。

故正确表达式为 B。
""",
    ),
    q(
        4,
        "single_choice",
        4,
        "高等数学",
        ["级数敛散性", "比较判别法"],
        "18",
        r"""
下列级数中发散的是（ ）

A. $\displaystyle \sum_{n=1}^{\infty}\frac{n}{3^n}$  
B. $\displaystyle \sum_{n=1}^{\infty}\frac1{\sqrt n}\ln\left(1+\frac1n\right)$  
C. $\displaystyle \sum_{n=2}^{\infty}\frac{(-1)^n+1}{\ln n}$  
D. $\displaystyle \sum_{n=1}^{\infty}\frac{n!}{n^n}$
""",
        r"C",
        r"""
A 由比值判别法收敛；B 中
$$
\ln\left(1+\frac1n\right)\sim \frac1n,
$$
故通项与 $n^{-3/2}$ 同阶，收敛；D 也可由比值判别法得收敛。

对于 C，
$$
\frac{(-1)^n+1}{\ln n}=
\begin{cases}
\dfrac{2}{\ln n}, & n=2m,\\[4pt]
0, & n=2m+1,
\end{cases}
$$
因此它大于发散的调和型子级数，故发散。选 C。
""",
    ),
    q(
        5,
        "single_choice",
        4,
        "线性代数",
        ["线性方程组", "无穷多解"],
        "18-19",
        r"""
设矩阵
$$
A=\begin{pmatrix}
1&1&1\\
1&2&a\\
1&4&a^2
\end{pmatrix},\qquad
b=\begin{pmatrix}
1\\d\\d^2
\end{pmatrix}.
$$
若集合 $\Omega=\{1,2\}$，则线性方程组 $Ax=b$ 有无穷多解的充分必要条件为（ ）

A. $a\notin\Omega,\ d\notin\Omega$  
B. $a\notin\Omega,\ d\in\Omega$  
C. $a\in\Omega,\ d\notin\Omega$  
D. $a\in\Omega,\ d\in\Omega$
""",
        r"D",
        r"""
有无穷多解要求
$$
r(A)=r(A,b)<3,
$$
首先
$$
|A|=(a-1)(a-2),
$$
故必须有
$$
a=1 \text{ 或 } a=2.
$$
再考察增广矩阵，可得只有在 $d=1$ 或 $d=2$ 时满足
$$
r(A)=r(A,b)<3.
$$
因此充分必要条件是
$$
a\in\Omega,\quad d\in\Omega.
$$
选 D。
""",
    ),
    q(
        6,
        "single_choice",
        4,
        "线性代数",
        ["二次型", "正交变换"],
        "19",
        r"""
设二次型 $f(x_1,x_2,x_3)$ 在正交变换 $x=Py$ 下的标准形为 $2y_1^2+y_2^2-y_3^2$，其中
$$
P=(e_1,e_2,e_3).
$$
若
$$
Q=(e_1,-e_3,e_2),
$$
则 $f(x_1,x_2,x_3)$ 在正交变换 $x=Qy$ 下的标准形为（ ）

A. $2y_1^2-y_2^2+y_3^2$  
B. $2y_1^2+y_2^2-y_3^2$  
C. $2y_1^2-y_2^2-y_3^2$  
D. $2y_1^2+y_2^2+y_3^2$
""",
        r"A",
        r"""
由 $Q=(e_1,-e_3,e_2)$ 可知，相当于在原标准形中交换第二、三坐标，并对新的第二坐标取负号。由于二次型中平方项对符号变化不敏感，只会交换
$$
y_2^2 \text{ 与 } -y_3^2
$$
的位置。

故新标准形为
$$
2y_1^2-y_2^2+y_3^2.
$$
选 A。
""",
    ),
    q(
        7,
        "single_choice",
        4,
        "概率统计",
        ["事件概率", "不等式"],
        "19",
        r"""
若 $A,B$ 为任意两个随机事件，则（ ）

A. $P(AB)\le P(A)P(B)$  
B. $P(AB)\ge P(A)P(B)$  
C. $P(AB)\le \dfrac{P(A)+P(B)}2$  
D. $P(AB)\ge \dfrac{P(A)+P(B)}2$
""",
        r"C",
        r"""
一般情况下，$P(AB)$ 与 $P(A)P(B)$ 没有固定大小关系，所以 A、B 都不对。

又由概率性质
$$
P(A)\ge P(AB),\qquad P(B)\ge P(AB).
$$
两式相加得
$$
P(A)+P(B)\ge2P(AB),
$$
故
$$
P(AB)\le \frac{P(A)+P(B)}2.
$$
选 C。
""",
    ),
    q(
        8,
        "single_choice",
        4,
        "概率统计",
        ["二项分布", "样本方差期望"],
        "19",
        r"""
设总体 $X\sim B(m,\theta)$，$X_1,X_2,\ldots,X_n$ 为来自该总体的简单随机样本，$\overline X$ 为样本均值，则
$$
E\left[\sum_{i=1}^n (X_i-\overline X)^2\right]=（\quad）
$$

A. $(m-1)n\theta(1-\theta)$  
B. $m(n-1)\theta(1-\theta)$  
C. $(m-1)(n-1)\theta(1-\theta)$  
D. $mn\theta(1-\theta)$
""",
        r"B",
        r"""
因为 $X\sim B(m,\theta)$，故
$$
D(X)=m\theta(1-\theta).
$$
记
$$
S^2=\frac1{n-1}\sum_{i=1}^n(X_i-\overline X)^2,
$$
则
$$
E(S^2)=D(X)=m\theta(1-\theta).
$$
因此
$$
E\left[\sum_{i=1}^n(X_i-\overline X)^2\right]
=(n-1)E(S^2)=m(n-1)\theta(1-\theta).
$$
选 B。
""",
    ),
    q(
        9,
        "fill_blank",
        4,
        "高等数学",
        ["极限", "泰勒展开"],
        "19",
        r"""
$$
\lim_{x\to0}\frac{\ln(\cos x)}{x^2}=\underline{\qquad}.
$$
""",
        r"$-\dfrac12$",
        r"""
当 $x\to0$ 时，
$$
\cos x=1-\frac{x^2}{2}+o(x^2).
$$
因此
$$
\ln(\cos x)=\ln\left(1-\frac{x^2}{2}+o(x^2)\right)\sim-\frac{x^2}{2}.
$$
故极限为
$$
-\frac12.
$$
""",
    ),
    q(
        10,
        "fill_blank",
        4,
        "高等数学",
        ["变上限积分", "导数"],
        "19",
        r"""
设函数 $f(x)$ 连续，
$$
\varphi(x)=\int_0^{x^2} x f(t)\,dt.
$$
若 $\varphi(1)=1,\ \varphi'(1)=5$，则 $f(1)=\underline{\qquad}$。
""",
        r"$2$",
        r"""
有
$$
\varphi(1)=\int_0^1 f(t)\,dt=1.
$$
又
$$
\varphi'(x)=\int_0^{x^2}f(t)\,dt+2x^2f(x^2).
$$
故
$$
\varphi'(1)=\int_0^1f(t)\,dt+2f(1)=1+2f(1)=5.
$$
解得
$$
f(1)=2.
$$
""",
    ),
    q(
        11,
        "fill_blank",
        4,
        "高等数学",
        ["隐函数求导", "全微分"],
        "19",
        r"""
若函数 $z=z(x,y)$ 由方程
$$
e^{x+2y+3z}+xyz=1
$$
确定，则
$$
dz\big|_{(0,0)}=\underline{\qquad}.
$$
""",
        r"$-\dfrac13dx-\dfrac23dy$",
        r"""
在 $(0,0)$ 处由方程可得 $z=0$。

对原方程分别关于 $x,y$ 求导并代入 $(0,0,0)$，得
$$
\frac{\partial z}{\partial x}\Big|_{(0,0)}=-\frac13,\qquad
\frac{\partial z}{\partial y}\Big|_{(0,0)}=-\frac23.
$$
因此
$$
dz\big|_{(0,0)}=-\frac13dx-\frac23dy.
$$
""",
    ),
    q(
        12,
        "fill_blank",
        4,
        "高等数学",
        ["微分方程"],
        "19-20",
        r"""
设函数 $y=y(x)$ 是微分方程
$$
y''+y'-2y=0
$$
的解，且在 $x=0$ 处 $y(x)$ 取得极值 $3$，则
$$
y(x)=\underline{\qquad}.
$$
""",
        r"$2e^x+e^{-2x}$",
        r"""
特征方程为
$$
\lambda^2+\lambda-2=0,
$$
解得
$$
\lambda_1=1,\qquad \lambda_2=-2.
$$
故通解
$$
y=C_1e^x+C_2e^{-2x}.
$$
由题意知
$$
y(0)=3,\qquad y'(0)=0,
$$
解得
$$
C_1=2,\qquad C_2=1.
$$
因此
$$
y(x)=2e^x+e^{-2x}.
$$
""",
    ),
    q(
        13,
        "fill_blank",
        4,
        "线性代数",
        ["特征值", "行列式"],
        "20",
        r"""
设 $3$ 阶矩阵 $A$ 的特征值为 $2,-2,1$，$B=A^2-A+E$，其中 $E$ 为 $3$ 阶单位矩阵，则行列式 $|B|=\underline{\qquad}$。
""",
        r"$21$",
        r"""
若 $\lambda$ 是 $A$ 的特征值，则
$$
\lambda^2-\lambda+1
$$
是 $B=A^2-A+E$ 的特征值。

因此 $B$ 的特征值为
$$
3,\ 7,\ 1.
$$
故
$$
|B|=3\cdot7\cdot1=21.
$$
""",
    ),
    q(
        14,
        "fill_blank",
        4,
        "概率统计",
        ["正态分布", "独立性"],
        "20",
        r"""
设二维随机变量 $(X,Y)$ 服从正态分布 $N(1,0;1,1;0)$，则
$$
P\{XY-Y<0\}=\underline{\qquad}.
$$
""",
        r"$\dfrac12$",
        r"""
相关系数为 $0$，故 $X,Y$ 独立，且
$$
X\sim N(1,1),\qquad Y\sim N(0,1).
$$
条件
$$
XY-Y<0
$$
化为
$$
Y(X-1)<0.
$$
于是
$$
P\{Y>0,X<1\}+P\{Y<0,X>1\}
=\frac12\cdot\frac12+\frac12\cdot\frac12=\frac12.
$$
""",
    ),
    q(
        15,
        "solution",
        10,
        "高等数学",
        ["等价无穷小", "泰勒展开"],
        "20",
        r"""
设函数
$$
f(x)=x+a\ln(1+x)+bx\sin x,\qquad g(x)=kx^3.
$$
若 $f(x)$ 与 $g(x)$ 在 $x\to0$ 时是等价无穷小，求 $a,b,k$ 的值。
""",
        r"$a=-1,\ b=-\dfrac12,\ k=-\dfrac13$",
        r"""
若 $f(x)\sim g(x)=kx^3$，则 $f(x)$ 的一、二阶导在 $0$ 处都应为 $0$。

先求
$$
f'(0)=1+a,
$$
故
$$
a=-1.
$$

再求
$$
f''(0)=1+2b,
$$
故
$$
b=-\frac12.
$$

最后比较三阶项，可得
$$
\lim_{x\to0}\frac{f(x)}{x^3}=-\frac13,
$$
于是
$$
k=-\frac13.
$$
""",
    ),
    q(
        16,
        "solution",
        10,
        "高等数学",
        ["二重积分", "区域对称性"],
        "20",
        r"""
计算二重积分
$$
\iint_D x(x+y)\,dxdy,
$$
其中
$$
D=\{(x,y)\mid x^2+y^2\le2,\ y\ge x^2\}.
$$
""",
        r"$\dfrac{\pi}{4}-\dfrac25$",
        r"""
由于区域 $D$ 关于 $y$ 轴对称，
$$
\iint_D xy\,dxdy=0.
$$
故
$$
\iint_D x(x+y)\,dxdy=\iint_D x^2\,dxdy.
$$

按 $x$ 积分，可写成
$$
2\int_0^1dx\int_{x^2}^{\sqrt{2-x^2}}x^2\,dy
=2\int_0^1 x^2\bigl(\sqrt{2-x^2}-x^2\bigr)\,dx.
$$
令 $x=\sqrt2\sin t$ 可算得
$$
2\int_0^1 x^2\sqrt{2-x^2}\,dx=\frac{\pi}{4},
$$
又
$$
2\int_0^1x^4\,dx=\frac25.
$$
故原积分
$$
=\frac{\pi}{4}-\frac25.
$$
""",
    ),
    q(
        17,
        "solution",
        10,
        "高等数学",
        ["经济应用", "需求弹性", "定价模型"],
        "20-21",
        r"""
为了实现利润最大化，厂商需要对某商品确定其定价模型。设 $Q$ 为该商品的需求量，$p$ 为价格，$MC$ 为边际成本，$\eta$ 为需求弹性（$\eta>0$）。

1. 证明定价模型为
$$
p=\frac{MC}{1-\frac1\eta};
$$
2. 若该商品的成本函数为 $C(Q)=1600+Q^2$，需求函数为 $Q=40-p$，试由（1）中的定价模型确定此商品的价格。
""",
        r"价格为 $p=30$",
        r"""
收益函数
$$
R=pQ.
$$
边际收益为
$$
MR=\frac{dR}{dQ}=p+Q\frac{dp}{dQ}
=p\left(1-\frac1\eta\right),
$$
其中利用了
$$
\eta=-\frac{p}{Q}\frac{dQ}{dp}.
$$
利润最大化条件为
$$
MR=MC,
$$
故
$$
p=\frac{MC}{1-\frac1\eta}.
$$

在题设下
$$
MC=C'(Q)=2Q,\qquad \eta=-\frac{p}{Q}\frac{dQ}{dp}=\frac{p}{40-p}.
$$
代入定价模型，
$$
p=\frac{2Q}{1-\frac{40-p}{p}}.
$$
再用 $Q=40-p$ 化简，解得
$$
p=30.
$$
""",
    ),
    q(
        18,
        "solution",
        10,
        "高等数学",
        ["微分方程", "切线", "面积"],
        "21",
        r"""
设函数 $f(x)$ 在定义域 $I$ 上的导数大于零。若对任意的 $x_0\in I$，曲线 $y=f(x)$ 在点 $(x_0,f(x_0))$ 处的切线与直线 $x=x_0$ 及 $x$ 轴所围成区域的面积恒为 $4$，且 $f(0)=2$，求 $f(x)$ 的表达式。
""",
        r"$f(x)=\dfrac{8}{4-x}$",
        r"""
点 $(x_0,f(x_0))$ 处切线方程为
$$
y=f(x_0)+f'(x_0)(x-x_0).
$$
它与 $x$ 轴的交点横坐标为
$$
x_0-\frac{f(x_0)}{f'(x_0)}.
$$
于是题设三角形面积条件给出
$$
\frac12\cdot \left|\frac{f(x_0)}{f'(x_0)}\right|\cdot |f(x_0)|=4.
$$
由于 $f'(x)>0$ 且 $f(0)=2>0$，可取正号，得
$$
y'=\frac18y^2.
$$
解得
$$
y=\frac{8}{C-x}.
$$
由 $f(0)=2$ 得 $C=4$，故
$$
f(x)=\frac{8}{4-x}.
$$
""",
    ),
    q(
        19,
        "solution",
        10,
        "高等数学",
        ["导数定义", "乘积求导法则"],
        "21",
        r"""
1. 设函数 $u(x),v(x)$ 可导，利用导数定义证明
$$
[u(x)v(x)]'=u'(x)v(x)+u(x)v'(x);
$$
2. 设函数 $u_1(x),u_2(x),\ldots,u_n(x)$ 可导，$f(x)=u_1(x)u_2(x)\cdots u_n(x)$，写出 $f(x)$ 的求导公式。
""",
        r"""
$$
[u(x)v(x)]'=u'(x)v(x)+u(x)v'(x),
$$
且
$$
f'(x)=\sum_{k=1}^n\left(\prod_{j\ne k}u_j(x)\right)u_k'(x).
$$
""",
        r"""
由导数定义，
$$
\frac{u(x+\Delta x)v(x+\Delta x)-u(x)v(x)}{\Delta x}
$$
可拆为
$$
\frac{u(x+\Delta x)-u(x)}{\Delta x}v(x+\Delta x)
+u(x)\frac{v(x+\Delta x)-v(x)}{\Delta x}.
$$
令 $\Delta x\to0$，即得
$$
[u(x)v(x)]'=u'(x)v(x)+u(x)v'(x).
$$

对 $n$ 个函数的乘积，反复使用乘积法则可得
$$
f'(x)=u_1'(x)u_2(x)\cdots u_n(x)+u_1(x)u_2'(x)\cdots u_n(x)+\cdots+u_1(x)u_2(x)\cdots u_n'(x),
$$
即
$$
f'(x)=\sum_{k=1}^n\left(\prod_{j\ne k}u_j(x)\right)u_k'(x).
$$
""",
    ),
    q(
        20,
        "solution",
        11,
        "线性代数",
        ["矩阵方程", "幂零矩阵"],
        "21",
        r"""
设矩阵
$$
A=\begin{pmatrix}
a&1&0\\
1&a&-1\\
0&1&a
\end{pmatrix},
$$
且 $A^3=O$。

1. 求 $a$ 的值；  
2. 若矩阵 $X$ 满足
$$
X-XA^2-AX+AXA^2=E,
$$
其中 $E$ 为 $3$ 阶单位矩阵，求 $X$。
""",
        r"""
$$
a=0,
$$
且
$$
X=\begin{pmatrix}
3&1&-2\\
1&1&-1\\
2&1&-1
\end{pmatrix}.
$$
""",
        r"""
由 $A^3=O$ 可知 $A$ 的全部特征值为 $0$，故
$$
|A|=a^3=0,
$$
从而
$$
a=0.
$$

原方程可因式分解为
$$
(E-A)X(E-A^2)=E.
$$
因此
$$
X=(E-A)^{-1}(E-A^2)^{-1}.
$$
当 $a=0$ 时，直接计算可得
$$
X=\begin{pmatrix}
3&1&-2\\
1&1&-1\\
2&1&-1
\end{pmatrix}.
$$
""",
    ),
    q(
        21,
        "solution",
        11,
        "线性代数",
        ["相似矩阵", "对角化"],
        "21-22",
        r"""
设矩阵
$$
A=\begin{pmatrix}
0&2&-3\\
-1&3&-3\\
1&-2&a
\end{pmatrix}
$$
相似于矩阵
$$
B=\begin{pmatrix}
1&-2&0\\
0&b&0\\
0&3&1
\end{pmatrix}.
$$

1. 求 $a,b$ 的值；  
2. 求可逆矩阵 $P$，使 $P^{-1}AP$ 为对角矩阵。
""",
        r"""
$$
a=4,\quad b=5.
$$

可取
$$
P=\begin{pmatrix}
2&-3&1\\
1&0&1\\
0&1&1
\end{pmatrix},
$$
使
$$
P^{-1}AP=\operatorname{diag}(1,1,5).
$$
""",
        r"""
由相似矩阵的性质，
$$
\operatorname{tr}(A)=\operatorname{tr}(B),\qquad |A|=|B|.
$$
由此解得
$$
a=4,\qquad b=5.
$$

于是
$$
|\lambda E-A|=|\lambda E-B|=(\lambda-1)^2(\lambda-5).
$$
所以 $A$ 的特征值为 $1,1,5$。

解特征方程可取对应线性无关特征向量
$$
\xi_1=(2,1,0)^T,\quad
\xi_2=(-3,0,1)^T,\quad
\xi_3=(1,1,1)^T.
$$
令
$$
P=(\xi_1,\xi_2,\xi_3)
=\begin{pmatrix}
2&-3&1\\
1&0&1\\
0&1&1
\end{pmatrix},
$$
则
$$
P^{-1}AP=\operatorname{diag}(1,1,5).
$$
""",
    ),
    q(
        22,
        "solution",
        11,
        "概率统计",
        ["负二项分布", "数学期望"],
        "22",
        r"""
设随机变量 $X$ 的概率密度为
$$
f(x)=
\begin{cases}
2^{-x}\ln2, & x>0,\\
0, & x\le0.
\end{cases}
$$
对 $X$ 进行独立重复的观测，直到第 $2$ 个大于 $3$ 的观测值出现时停止，记 $Y$ 为观测次数。

1. 求 $Y$ 的概率分布；  
2. 求 $E(Y)$。
""",
        r"""
$$
P(Y=n)=(n-1)\left(\frac18\right)^2\left(\frac78\right)^{n-2},\quad n=2,3,\ldots
$$
且
$$
E(Y)=16.
$$
""",
        r"""
先求一次观测“大于 $3$”的概率：
$$
p=P(X>3)=\int_3^{+\infty}2^{-x}\ln2\,dx=2^{-3}=\frac18.
$$
于是 $Y$ 表示独立伯努利试验中“第 $2$ 次成功出现时的试验次数”，故服从参数为 $r=2,p=\frac18$ 的负二项分布：
$$
P(Y=n)=\binom{n-1}{1}p^2(1-p)^{n-2}
=(n-1)\left(\frac18\right)^2\left(\frac78\right)^{n-2},
\quad n\ge2.
$$

其期望为
$$
E(Y)=\frac{r}{p}=\frac{2}{1/8}=16.
$$
""",
    ),
    q(
        23,
        "solution",
        11,
        "概率统计",
        ["矩估计", "极大似然估计", "均匀分布"],
        "22",
        r"""
设总体 $X$ 的概率密度为
$$
f(x;\theta)=
\begin{cases}
\dfrac{1}{1-\theta}, & \theta\le x\le1,\\
0, & \text{其他},
\end{cases}
$$
其中 $\theta$ 为未知参数，$X_1,X_2,\ldots,X_n$ 为来自该总体的简单随机样本。

1. 求 $\theta$ 的矩估计量；  
2. 求 $\theta$ 的最大似然估计量。
""",
        r"""
$$
\hat\theta_{\text{矩}}=2\overline X-1,
$$
$$
\hat\theta_{\text{MLE}}=\min\{X_1,\ldots,X_n\}.
$$
""",
        r"""
该总体服从区间 $[\theta,1]$ 上的均匀分布，因此
$$
EX=\frac{\theta+1}{2}.
$$
令样本均值 $\overline X$ 等于理论均值，得矩估计量
$$
\hat\theta_{\text{矩}}=2\overline X-1.
$$

对样本 $x_1,\ldots,x_n$，似然函数为
$$
L(\theta)=
\begin{cases}
(1-\theta)^{-n}, & \theta\le \min\{x_1,\ldots,x_n\},\\
0, & \text{否则}.
\end{cases}
$$
在允许范围内，$L(\theta)$ 随 $\theta$ 增大而增大，因此最大似然估计取可行域最大值：
$$
\hat\theta_{\text{MLE}}=\min\{X_1,\ldots,X_n\}.
$$
""",
    ),
]


def annual_questions_md(questions: list[Question]) -> str:
    lines = [
        f"# {YEAR} 年考研数学三真题",
        "",
        "资料类型：考研数学三历年真题",
        f"年份：{YEAR}",
        "科目：数学三",
        "整理状态：按试卷页图人工校对并清洗为正式题卡。",
        "",
    ]
    for item in questions:
        lines.extend(
            [
                f"### 第 {item.number} 题",
                f"- 题型：{qtype_label(item.question_type)}",
                f"- 分值：{item.score}",
                f"- 模块：{item.module}",
                f"- 考点：{'、'.join(item.topics)}",
                f"- PDF 页码：{item.pdf_pages}",
                "",
                item.stem,
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def annual_answers_md(questions: list[Question]) -> str:
    lines = [
        f"# {YEAR} 年考研数学三答案解析",
        "",
        "资料类型：考研数学三答案解析",
        f"年份：{YEAR}",
        "科目：数学三",
        "整理状态：按答案页图人工校对并整理为正式题卡。",
        "",
    ]
    groups = {
        "single_choice": [q for q in questions if q.question_type == "single_choice"],
        "fill_blank": [q for q in questions if q.question_type == "fill_blank"],
        "solution": [q for q in questions if q.question_type == "solution"],
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
        for item in groups[key]:
            lines.append(f"| {item.number} | {answer_for_table(item.answer)} |")
        lines.append("")
    lines.extend(["## 详细解析", ""])
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
                f"- 题目来源：`math3_{YEAR}_questions.md`",
                f"- 答案来源：`math3_{YEAR}_answers.md`",
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
    with (YEAR_DIR / "questions.jsonl").open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
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
    (YEAR_DIR / "paper_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def main() -> None:
    YEAR_DIR.mkdir(parents=True, exist_ok=True)
    (YEAR_DIR / f"math3_{YEAR}_questions.md").write_text(
        annual_questions_md(QUESTIONS),
        encoding="utf-8",
    )
    (YEAR_DIR / f"math3_{YEAR}_answers.md").write_text(
        annual_answers_md(QUESTIONS),
        encoding="utf-8",
    )
    build_cards(QUESTIONS)
    print(json.dumps({"year": YEAR, "question_count": len(QUESTIONS), "generated_at": now_iso()}, ensure_ascii=False))


if __name__ == "__main__":
    main()
