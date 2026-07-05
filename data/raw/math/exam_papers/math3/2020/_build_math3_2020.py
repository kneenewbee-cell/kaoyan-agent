from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


YEAR = 2020
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
    stem: str
    answer: str
    explanation: str


def q(number: int, question_type: str, score: int, module: str, topics: list[str], stem: str, answer: str, explanation: str) -> Question:
    return Question(number, question_type, score, module, topics, stem.strip(), answer.strip(), explanation.strip())


QUESTIONS = [
    q(1, "single_choice", 4, "高等数学", ["导数定义", "拉格朗日中值定理", "复合函数"], r"""
设
$$
\lim_{x\to a}\frac{f(x)-a}{x-a}=b,
$$
则
$$
\lim_{x\to a}\frac{\sin f(x)-\sin a}{x-a}=(\ \ )
$$

A. $b\sin a$  
B. $b\cos a$  
C. $b\sin f(a)$  
D. $b\cos f(a)$
""", r"B", r"""
由拉格朗日中值定理，
$$
\sin f(x)-\sin a=\cos\xi\,[f(x)-a],
$$
其中 $\xi$ 介于 $f(x)$ 与 $a$ 之间。

因此
$$
\frac{\sin f(x)-\sin a}{x-a}
=\cos\xi\cdot \frac{f(x)-a}{x-a}.
$$
当 $x\to a$ 时，$\xi\to a$，故
$$
\lim_{x\to a}\frac{\sin f(x)-\sin a}{x-a}
=\cos a\cdot b=b\cos a.
$$
故选 **B**。
"""),
    q(2, "single_choice", 4, "高等数学", ["间断点", "极限"], r"""
函数
$$
f(x)=\frac{e^{\frac1{x-1}}\ln|1+x|}{(e^x-1)(x-2)}
$$
的第二类间断点的个数为（ ）

A. 1 个  
B. 2 个  
C. 3 个  
D. 4 个
""", r"C", r"""
可能的间断点来自 $x=-1,0,1,2$。

- 当 $x=-1$ 时，$\ln|1+x|$ 发散，所以是第二类间断点；
- 当 $x=0$ 时，利用
  $$
  \ln(1+x)\sim x,\qquad e^x-1\sim x,
  $$
  可知极限存在，因此是可去间断点；
- 当 $x=1$ 时，$e^{1/(x-1)}$ 发散，为第二类间断点；
- 当 $x=2$ 时，分母为 0 而分子有限非零，也是第二类间断点。

故第二类间断点共有 3 个，选 **C**。
"""),
    q(3, "single_choice", 4, "高等数学", ["奇偶函数", "定积分"], r"""
设奇函数 $f(x)$ 在 $(-\infty,+\infty)$ 上具有连续导数，则（ ）

A.
$$
\int_0^x[\cos f(t)+f'(t)]\,dt
$$
是奇函数  

B.
$$
\int_0^x[\cos f(t)+f'(t)]\,dt
$$
是偶函数  

C.
$$
\int_0^x[\cos f'(t)+f(t)]\,dt
$$
是奇函数  

D.
$$
\int_0^x[\cos f'(t)+f(t)]\,dt
$$
是偶函数
""", r"A", r"""
因为 $f$ 为奇函数，所以 $f'$ 为偶函数；又 $\cos f(t)$ 也是偶函数。
于是
$$
\cos f(t)+f'(t)
$$
是偶函数。

偶函数从 0 到 $x$ 的积分是奇函数，因此
$$
\int_0^x[\cos f(t)+f'(t)]\,dt
$$
是奇函数。

故选 **A**。
"""),
    q(4, "single_choice", 4, "高等数学", ["幂级数", "收敛区间"], r"""
设幂级数
$$
\sum_{n=1}^{\infty} n a_n (x-2)^n
$$
的收敛区间为 $(-2,6)$，则
$$
\sum_{n=1}^{\infty} a_n (x+1)^{2n}
$$
的收敛区间为（ ）

A. $(-2,6)$  
B. $(-3,1)$  
C. $(-5,3)$  
D. $(-17,15)$
""", r"B", r"""
已知级数
$$
\sum n a_n (x-2)^n
$$
的收敛半径为
$$
R=\frac{6-(-2)}2=4.
$$

因此关于变量 $u=(x+1)^2$ 的级数
$$
\sum a_n u^n
$$
的收敛半径为 4，即
$$
|(x+1)^2|<4.
$$
所以
$$
|x+1|<2\iff -3<x<1.
$$
故选 **B**。
"""),
    q(5, "single_choice", 4, "线性代数", ["伴随矩阵", "齐次方程组"], r"""
设 4 阶矩阵 $A=(a_{ij})$ 不可逆，$a_{12}$ 的代数余子式 $A_{12}\ne0$，$\alpha_1,\alpha_2,\alpha_3,\alpha_4$ 为矩阵 $A$ 的列向量组，$A^*$ 为 $A$ 的伴随矩阵，则方程组
$$
A^*x=0
$$
的通解为（ ）

A. $x=k_1\alpha_1+k_2\alpha_2+k_3\alpha_3$  
B. $x=k_1\alpha_1+k_2\alpha_2+k_3\alpha_4$  
C. $x=k_1\alpha_1+k_2\alpha_3+k_3\alpha_4$  
D. $x=k_1\alpha_2+k_2\alpha_3+k_3\alpha_4$
""", r"C", r"""
因为 $A$ 不可逆且 $A_{12}\ne0$，可知 $r(A)=3$，并且去掉第 1 行、第 2 列后的 3 阶子式非零。
这意味着由第 1、3、4 列构成的三个列向量线性无关。

而
$$
A^*A=AA^*=0
$$
且 $r(A^*)=1$，所以齐次方程组 $A^*x=0$ 的解空间维数为 3，它正由 $A$ 的三个线性无关列向量张成。

故通解可写为
$$
x=k_1\alpha_1+k_2\alpha_3+k_3\alpha_4.
$$
选 **C**。
"""),
    q(6, "single_choice", 4, "线性代数", ["相似对角化", "特征向量"], r"""
设 $A$ 为 3 阶矩阵，$\alpha_1,\alpha_2$ 为 $A$ 的属于特征值 1 的线性无关特征向量，$\alpha_3$ 为 $A$ 的属于特征值 $-1$ 的特征向量，则满足
$$
P^{-1}AP=
\begin{pmatrix}
1&0&0\\
0&-1&0\\
0&0&1
\end{pmatrix}
$$
的可逆矩阵 $P$ 可为（ ）

A. $(\alpha_1+\alpha_3,\alpha_2,-\alpha_3)$  
B. $(\alpha_1+\alpha_2,\alpha_2,-\alpha_3)$  
C. $(\alpha_1+\alpha_3,-\alpha_3,\alpha_2)$  
D. $(\alpha_1+\alpha_2,-\alpha_3,\alpha_2)$
""", r"D", r"""
矩阵 $P$ 的列向量必须依次是对应于特征值 $1,-1,1$ 的特征向量。

- $\alpha_1+\alpha_2$ 仍是特征值 1 的特征向量；
- $-\alpha_3$ 是特征值 $-1$ 的特征向量；
- $\alpha_2$ 是特征值 1 的特征向量。

且这三列线性无关，因此
$$
P=(\alpha_1+\alpha_2,-\alpha_3,\alpha_2)
$$
满足要求。

故选 **D**。
"""),
    q(7, "single_choice", 4, "概率统计", ["容斥原理"], r"""
设 $A,B,C$ 为三个随机事件，且
$$
P(A)=P(B)=P(C)=\frac14,\qquad P(AB)=0,\qquad P(AC)=P(BC)=\frac1{12},
$$
则 $A,B,C$ 中恰有一个事件发生的概率为（ ）

A. $\dfrac34$  
B. $\dfrac23$  
C. $\dfrac12$  
D. $\dfrac5{12}$
""", r"D", r"""
恰有一个事件发生的概率为
$$
P(A\cup B\cup C)-P(\text{至少两个发生}).
$$
由于 $P(AB)=0$，故 $P(ABC)=0$。

直接按“只发生 $A$、只发生 $B$、只发生 $C$”计算：
$$
P(\text{只发生 }A)=P(A)-P(AC)=\frac14-\frac1{12}=\frac16,
$$
$$
P(\text{只发生 }B)=P(B)-P(BC)=\frac16,
$$
$$
P(\text{只发生 }C)=P(C)-P(AC)-P(BC)=\frac14-\frac1{12}-\frac1{12}=\frac1{12}.
$$
所以
$$
\frac16+\frac16+\frac1{12}=\frac5{12}.
$$
故选 **D**。
"""),
    q(8, "single_choice", 4, "概率统计", ["二维正态分布", "独立性"], r"""
设随机变量 $(X,Y)$ 服从二维正态分布
$$
N(0,0;1,4;-\tfrac12),
$$
则下列随机变量中服从标准正态分布且与 $X$ 独立的是（ ）

A. $\dfrac{\sqrt5}{5}(X+Y)$  
B. $\dfrac{\sqrt5}{5}(X-Y)$  
C. $\dfrac{\sqrt3}{3}(X+Y)$  
D. $\dfrac{\sqrt3}{3}(X-Y)$
""", r"C", r"""
由题意
$$
D(X)=1,\qquad D(Y)=4,\qquad \rho=-\frac12.
$$
所以
$$
\operatorname{Cov}(X,Y)=\rho\sqrt{D(X)}\sqrt{D(Y)}=-1.
$$

计算
$$
D(X+Y)=1+4+2(-1)=3,
$$
$$
D(X-Y)=1+4-2(-1)=7.
$$
因此
$$
\frac{\sqrt3}{3}(X+Y)
$$
的方差为 1，且其与 $X$ 的协方差
$$
\operatorname{Cov}\!\left(X,\frac{\sqrt3}{3}(X+Y)\right)
=\frac{\sqrt3}{3}(D(X)+\operatorname{Cov}(X,Y))
=0.
$$
二维正态下“不相关即独立”，故选 **C**。
"""),
    q(9, "fill_blank", 4, "高等数学", ["全微分"], r"""
设
$$
z=\arctan[xy+\sin(x+y)],
$$
则
$$
dz\big|_{(0,\pi)}=\underline{\qquad}.
$$
""", r"$(\pi-1)\,dx-dy$", r"""
设
$$
u=xy+\sin(x+y),\qquad z=\arctan u.
$$
则
$$
dz=\frac1{1+u^2}\,du.
$$
在 $(0,\pi)$ 处，
$$
u=0\cdot\pi+\sin\pi=0,
$$
所以
$$
dz=du.
$$

又
$$
u_x=y+\cos(x+y),\qquad u_y=x+\cos(x+y).
$$
代入 $(0,\pi)$ 得
$$
u_x=\pi-1,\qquad u_y=-1.
$$
故
$$
dz=(\pi-1)\,dx-dy.
$$
"""),
    q(10, "fill_blank", 4, "高等数学", ["隐函数求导", "切线"], r"""
曲线
$$
x+y+e^{2xy}=0
$$
在 $(0,-1)$ 处的切线方程为
$$
\underline{\qquad}.
$$
""", r"$y=x-1$", r"""
对方程两边关于 $x$ 求导：
$$
1+y'+e^{2xy}\cdot 2(y+xy')=0.
$$
在点 $(0,-1)$ 处，$e^{2xy}=1$，于是
$$
1+y'+2(-1+0\cdot y')=0
\iff y'=1.
$$
所以切线方程为
$$
y+1=1(x-0),
$$
即
$$
y=x-1.
$$
"""),
    q(11, "fill_blank", 4, "概率统计", ["利润最大化"], r"""
设某厂家某产品的产量为 $Q$，成本
$$
C(Q)=100+13Q,
$$
设产品的单价为 $P$，需求量
$$
Q(P)=\frac{800}{P+3}-2,
$$
则该厂家获得最大利润时的产量为
$$
\underline{\qquad}.
$$
""", r"$8$", r"""
由
$$
Q=\frac{800}{P+3}-2
$$
解得
$$
P=\frac{800}{Q+2}-3.
$$

利润函数为
$$
L(Q)=PQ-C(Q)
=\left(\frac{800}{Q+2}-3\right)Q-(100+13Q)
=\frac{1600}{Q+2}-16Q+700.
$$
求导：
$$
L'(Q)=-\frac{1600}{(Q+2)^2}+16.
$$
令 $L'(Q)=0$，得
$$
\frac{1600}{(Q+2)^2}=16
\iff (Q+2)^2=100
\iff Q=8
$$
（舍去负值）。
故最大利润时产量为 8。
"""),
    q(12, "fill_blank", 4, "高等数学", ["旋转体体积"], r"""
设平面区域
$$
D=\left\{(x,y)\ \middle|\ \frac{x}{2}\le y\le \frac1{1+x^2},\ 0\le x\le1\right\},
$$
则 $D$ 绕 $y$ 轴旋转所成的旋转体的体积为
$$
\underline{\qquad}.
$$
""", r"$\pi\ln2-\dfrac{\pi}{3}$", r"""
绕 $y$ 轴旋转，采用壳层法：
$$
V=2\pi\iint_D x\,d\sigma
=2\pi\int_0^1 x\left(\frac1{1+x^2}-\frac x2\right)\,dx.
$$
所以
$$
V=2\pi\left(\int_0^1\frac{x}{1+x^2}\,dx-\frac12\int_0^1x^2\,dx\right).
$$
计算得
$$
\int_0^1\frac{x}{1+x^2}\,dx=\frac12\ln2,\qquad
\frac12\int_0^1x^2\,dx=\frac16.
$$
因此
$$
V=2\pi\left(\frac12\ln2-\frac16\right)=\pi\ln2-\frac{\pi}{3}.
$$
"""),
    q(13, "fill_blank", 4, "线性代数", ["行列式"], r"""
行列式
$$
\begin{vmatrix}
a&0&-1&1\\
0&a&1&-1\\
-1&1&a&0\\
1&-1&0&a
\end{vmatrix}
=\underline{\qquad}.
$$
""", r"$a^2(a^2-4)$", r"""
对行列式作初等变换化简，例如将第 2 行加到第 1 行、第 3 行加到第 4 行，再对列作相应整理，可化为上三角块形式。

最终得到
$$
\begin{vmatrix}
a&2\\
2&a
\end{vmatrix}
$$
与两个对角元 $a$ 的乘积，因此
$$
|A|=a^2(a^2-4).
$$
"""),
    q(14, "fill_blank", 4, "概率统计", ["离散分布", "数学期望"], r"""
设随机变量 $X$ 的概率分布为
$$
P\{X=k\}=\frac1{2^k},\qquad k=1,2,3,\ldots,
$$
$Y$ 表示 $X$ 被 3 除的余数，则
$$
E(Y)=\underline{\qquad}.
$$
""", r"$\dfrac87$", r"""
按模 3 分类：

- 当 $Y=1$ 时，$X=1,4,7,\ldots$，
  $$
  P(Y=1)=\frac12+\frac1{2^4}+\frac1{2^7}+\cdots=\frac{1/2}{1-1/8}=\frac47;
  $$
- 当 $Y=2$ 时，$X=2,5,8,\ldots$，
  $$
  P(Y=2)=\frac14+\frac1{2^5}+\frac1{2^8}+\cdots=\frac{1/4}{1-1/8}=\frac27;
  $$
- 当 $Y=0$ 时，
  $$
  P(Y=0)=1-\frac47-\frac27=\frac17.
  $$

所以
$$
E(Y)=0\cdot\frac17+1\cdot\frac47+2\cdot\frac27=\frac87.
$$
"""),
    q(15, "solution", 7, "高等数学", ["等价无穷小", "极限"], r"""
已知 $a,b$ 为常数，若
$$
\left(1+\frac1n\right)^n-e
$$
与
$$
\frac{b}{n^a}
$$
在 $n\to+\infty$ 时是等价无穷小，求 $a,b$。
""", r"$a=1,\ b=-\dfrac e2$", r"""
写成
$$
\left(1+\frac1n\right)^n-e
=e\left[e^{n\ln(1+1/n)-1}-1\right].
$$
由于
$$
\ln\left(1+\frac1n\right)=\frac1n-\frac1{2n^2}+o(n^{-2}),
$$
所以
$$
n\ln\left(1+\frac1n\right)-1=-\frac1{2n}+o(n^{-1}).
$$
于是
$$
e^{n\ln(1+1/n)-1}-1\sim -\frac1{2n}.
$$
故
$$
\left(1+\frac1n\right)^n-e\sim -\frac{e}{2n}.
$$

与
$$
\frac{b}{n^a}
$$
等价，故
$$
a=1,\qquad b=-\frac e2.
$$
"""),
    q(16, "solution", 7, "高等数学", ["多元函数极值"], r"""
求函数
$$
f(x,y)=x^3+8y^3-xy
$$
的极值。
""", r"在 $\left(\frac16,\frac1{12}\right)$ 处取极小值 $-\frac1{216}$；原点不是极值点。", r"""
求偏导：
$$
f_x=3x^2-y,\qquad f_y=24y^2-x.
$$
令其为 0，得驻点
$$
(0,0),\qquad \left(\frac16,\frac1{12}\right).
$$

二阶偏导为
$$
f_{xx}=6x,\qquad f_{xy}=-1,\qquad f_{yy}=48y.
$$
判别式
$$
\Delta=f_{xx}f_{yy}-f_{xy}^2=288xy-1.
$$

- 在 $(0,0)$ 处，
  $$
  \Delta=-1<0,
  $$
  不是极值点；
- 在 $\left(\frac16,\frac1{12}\right)$ 处，
  $$
  \Delta=3>0,\qquad f_{xx}=1>0,
  $$
  故为极小值点。

其极小值为
$$
f\left(\frac16,\frac1{12}\right)=\frac1{216}+\frac1{216}-\frac1{72}=-\frac1{216}.
$$
"""),
    q(17, "solution", 7, "高等数学", ["常系数微分方程"], r"""
设函数 $y=f(x)$ 满足
$$
y''+2y'+5y=0,\qquad f(0)=1,\qquad f'(0)=-1.
$$

1. 求 $f(x)$ 的表达式；  
2. 设
$$
a_n=\int_{n\pi}^{+\infty}f(x)\,dx,
$$
求
$$
\sum_{n=1}^{\infty}a_n.
$$
""", r"""
$$
f(x)=e^{-x}\cos 2x;
$$

$$
\sum_{n=1}^{\infty}a_n=\frac{1}{5(e^\pi-1)}.
$$
""", r"""
特征方程
$$
\lambda^2+2\lambda+5=0
$$
有根
$$
\lambda=-1\pm 2i.
$$
因此
$$
f(x)=e^{-x}(C_1\cos2x+C_2\sin2x).
$$
由条件
$$
f(0)=1,\qquad f'(0)=-1
$$
得
$$
C_1=1,\qquad C_2=0.
$$
所以
$$
f(x)=e^{-x}\cos2x.
$$

再求积分：
$$
\int e^{-x}\cos2x\,dx=\frac15(2\sin2x-\cos2x)e^{-x}+C.
$$
因此
$$
a_n=\left[\frac15(2\sin2x-\cos2x)e^{-x}\right]_{n\pi}^{+\infty}
=\frac15e^{-n\pi}.
$$
故
$$
\sum_{n=1}^{\infty}a_n
=\frac15\sum_{n=1}^{\infty}e^{-n\pi}
=\frac15\cdot \frac{e^{-\pi}}{1-e^{-\pi}}
=\frac{1}{5(e^\pi-1)}.
$$
"""),
    q(18, "solution", 7, "高等数学", ["二重积分", "参数"], r"""
设
$$
D=\{(x,y)\mid x^2+y^2\le1,\ y\ge0\},
$$
连续函数 $f(x,y)$ 满足
$$
f(x,y)=y\sqrt{1-x^2}+x\iint_D f(x,y)\,dx\,dy,
$$
求
$$
\iint_D x f(x,y)\,dx\,dy.
$$
""", r"$\dfrac{3\pi^2}{128}$", r"""
设
$$
A=\iint_D f(x,y)\,dx\,dy.
$$
则
$$
f(x,y)=y\sqrt{1-x^2}+Ax.
$$

对两边在 $D$ 上积分：
$$
A=\iint_D y\sqrt{1-x^2}\,dx\,dy+A\iint_D x\,dx\,dy.
$$
由于区域关于 $y$ 轴对称，
$$
\iint_D x\,dx\,dy=0,
$$
所以
$$
A=\iint_D y\sqrt{1-x^2}\,dx\,dy.
$$
计算得
$$
A=2\int_0^1\sqrt{1-x^2}\left(\int_0^{\sqrt{1-x^2}}y\,dy\right)dx
=\int_0^1(1-x^2)^{3/2}\,dx
=\frac{3\pi}{16}.
$$

于是
$$
f(x,y)=y\sqrt{1-x^2}+\frac{3\pi}{16}x.
$$
故
$$
\iint_D x f(x,y)\,dx\,dy
=\iint_D xy\sqrt{1-x^2}\,dx\,dy+\frac{3\pi}{16}\iint_D x^2\,dx\,dy.
$$
第一项由于关于 $y$ 轴奇对称为 0。

因此
$$
\iint_D x f(x,y)\,dx\,dy
=\frac{3\pi}{16}\iint_D x^2\,dx\,dy.
$$
用极坐标计算
$$
\iint_D x^2\,dx\,dy
=\int_0^\pi\int_0^1 r^2\cos^2\theta\cdot r\,dr\,d\theta
=\frac14\cdot \frac\pi2=\frac{\pi}{8}.
$$
所以结果为
$$
\frac{3\pi}{16}\cdot \frac{\pi}{8}=\frac{3\pi^2}{128}.
$$
"""),
    q(19, "solution", 7, "高等数学", ["中值定理", "证明题"], r"""
设函数 $f(x)$ 在区间 $[0,2]$ 上具有连续导数，$f(0)=f(2)=0$，$M=\max\limits_{x\in[0,2]}|f(x)|$。证明：

1. 存在 $\xi\in(0,2)$，使得 $|f'(\xi)|\ge M$；  
2. 若对任意 $x\in(0,2)$，$|f'(x)|\le M$，则 $M=0$。
""", r"命题成立", r"""
1. 取 $c\in[0,2]$ 使
$$
|f(c)|=M.
$$

若 $c\in(0,1]$，由拉格朗日中值定理，存在 $\xi\in(0,c)$ 使
$$
f'(\xi)=\frac{f(c)-f(0)}{c}=\frac{f(c)}{c}.
$$
于是
$$
|f'(\xi)|=\frac{|f(c)|}{c}=\frac{M}{c}\ge M.
$$

若 $c\in(1,2)$，同理存在 $\xi\in(c,2)$ 使
$$
f'(\xi)=\frac{f(2)-f(c)}{2-c}=-\frac{f(c)}{2-c},
$$
从而
$$
|f'(\xi)|=\frac{M}{2-c}\ge M.
$$
故命题 1 成立。

2. 若对任意 $x\in(0,2)$ 有 $|f'(x)|\le M$。仍取 $c$ 使 $|f(c)|=M$。

- 若 $c\in[0,1)$，则
  $$
  M=|f(c)-f(0)|=|f'(\xi)|c\le Mc.
  $$
  因为 $c<1$，只可能 $M=0$；
- 若 $c\in(1,2]$，同理也得 $M=0$；
- 若 $c=1$ 且 $M>0$，则
  $$
  M=|f(1)|=\left|\int_0^1 f'(x)\,dx\right|
  \le \int_0^1|f'(x)|\,dx < M,
  $$
  矛盾。

故必有
$$
M=0.
$$
"""),
    q(20, "solution", 7, "线性代数", ["二次型", "正交变换"], r"""
设二次型
$$
f(x_1,x_2)=x_1^2-4x_1x_2+4x_2^2
$$
经过正交变换
$$
\binom{x_1}{x_2}=Q\binom{y_1}{y_2}
$$
化为二次型
$$
g(y_1,y_2)=ay_1^2+4y_1y_2+by_2^2,
$$
其中 $a\ge b$。

1. 求 $a,b$；  
2. 求正交矩阵 $Q$。
""", r"""
$$
a=4,\quad b=1;
$$

可取
$$
Q=
\begin{pmatrix}
0&1\\
-1&0
\end{pmatrix}.
$$
""", r"""
二次型 $f,g$ 对应矩阵分别为
$$
A=
\begin{pmatrix}
1&-2\\
-2&4
\end{pmatrix},\qquad
B=
\begin{pmatrix}
a&2\\
2&b
\end{pmatrix}.
$$
正交合同保持迹和行列式，所以
$$
a+b=5,\qquad ab-4=0.
$$
解得
$$
a,b=4,1.
$$
又因 $a\ge b$，故
$$
a=4,\quad b=1.
$$

于是
$$
g(y_1,y_2)=4y_1^2+4y_1y_2+y_2^2=(2y_1+y_2)^2.
$$
取变换
$$
x_1=y_2,\qquad x_2=-y_1,
$$
即
$$
\binom{x_1}{x_2}
=
\begin{pmatrix}
0&1\\
-1&0
\end{pmatrix}
\binom{y_1}{y_2}.
$$
代入可验证恰化为所给二次型。
"""),
    q(21, "solution", 7, "线性代数", ["相似变换", "特征值"], r"""
设 $A$ 为 2 阶矩阵，
$$
P=(\alpha,A\alpha),
$$
其中 $\alpha$ 是非零向量且不是 $A$ 的特征向量。

1. 证明 $P$ 为可逆矩阵；  
2. 若
$$
A^2\alpha+A\alpha-6\alpha=0,
$$
求 $P^{-1}AP$，并判断 $A$ 是否相似于对角矩阵。
""", r"""
$$
P^{-1}AP=
\begin{pmatrix}
0&6\\
1&-1
\end{pmatrix};
$$

$A$ 相似于对角矩阵。
""", r"""
1. 若 $P$ 不可逆，则 $\alpha$ 与 $A\alpha$ 线性相关，即存在常数 $k$ 使
$$
A\alpha=k\alpha.
$$
这说明 $\alpha$ 是 $A$ 的特征向量，与题设矛盾。因此 $P$ 可逆。

2. 有
$$
A^2\alpha=6\alpha-A\alpha.
$$
于是
$$
AP=A(\alpha,A\alpha)=(A\alpha,A^2\alpha)=(A\alpha,6\alpha-A\alpha).
$$
写成以 $P$ 为基底的坐标即
$$
AP=(\alpha,A\alpha)
\begin{pmatrix}
0&6\\
1&-1
\end{pmatrix}.
$$
故
$$
P^{-1}AP=
\begin{pmatrix}
0&6\\
1&-1
\end{pmatrix}.
$$

记
$$
B=
\begin{pmatrix}
0&6\\
1&-1
\end{pmatrix},
$$
则其特征多项式为
$$
|\lambda E-B|=\lambda^2+\lambda-6=(\lambda-2)(\lambda+3).
$$
有两个不同特征值，因此 $B$ 可对角化，从而 $A$ 也相似于对角矩阵。
"""),
    q(22, "solution", 7, "概率统计", ["均匀分布", "相关系数"], r"""
设二维随机变量 $(X,Y)$ 在区域
$$
D=\{(x,y)\mid 0<y<\sqrt{1-x^2}\}
$$
上服从均匀分布，令
$$
Z_1=
\begin{cases}
1,& X-Y>0,\\
0,& X-Y\le0,
\end{cases}
\qquad
Z_2=
\begin{cases}
1,& X+Y>0,\\
0,& X+Y\le0.
\end{cases}
$$

1. 求二维随机变量 $(Z_1,Z_2)$ 的概率分布；  
2. 求 $Z_1$ 与 $Z_2$ 的相关系数。
""", r"""
分布为

| $Z_1\backslash Z_2$ | 0 | 1 |
|---|---:|---:|
| 0 | $\dfrac14$ | $\dfrac12$ |
| 1 | $0$ | $\dfrac14$ |

相关系数
$$
\rho_{Z_1,Z_2}=\frac13.
$$
""", r"""
区域 $D$ 是上半圆盘，面积为
$$
|D|=\frac{\pi}{2}.
$$

直线 $x-y=0$ 与 $x+y=0$ 把该半圆分成若干部分。

- 事件 $Z_1=1$ 对应区域 $x>y$，其面积占上半圆的 $\dfrac14$，故
  $$
  P(Z_1=1)=\frac14,\qquad P(Z_1=0)=\frac34;
  $$
- 事件 $Z_2=1$ 对应区域 $x+y>0$，其面积占上半圆的 $\dfrac34$，故
  $$
  P(Z_2=1)=\frac34,\qquad P(Z_2=0)=\frac14.
  $$

又
$$
P(Z_1=1,Z_2=1)=\frac14,
$$
而 $Z_1=1$ 时必有 $Z_2=1$，所以
$$
P(Z_1=1,Z_2=0)=0.
$$
由边际分布得
$$
P(Z_1=0,Z_2=1)=\frac12,\qquad P(Z_1=0,Z_2=0)=\frac14.
$$

因此分布表如答案所示。

再计算：
$$
E(Z_1)=\frac14,\qquad E(Z_2)=\frac34,
$$
$$
D(Z_1)=\frac14\cdot\frac34=\frac3{16},\qquad
D(Z_2)=\frac34\cdot\frac14=\frac3{16}.
$$
且
$$
E(Z_1Z_2)=P(Z_1=1,Z_2=1)=\frac14.
$$
故
$$
\operatorname{Cov}(Z_1,Z_2)=\frac14-\frac14\cdot\frac34=\frac1{16}.
$$
所以
$$
\rho_{Z_1,Z_2}
=\frac{1/16}{\sqrt{3/16}\sqrt{3/16}}
=\frac13.
$$
"""),
    q(23, "solution", 8, "概率统计", ["分布函数", "最大似然估计"], r"""
设某种元件的使用寿命 $T$ 的分布函数为
$$
F(t)=
\begin{cases}
1-e^{-(t/\theta)^m},& t\ge0,\\
0,& \text{其他},
\end{cases}
$$
其中 $\theta,m$ 为参数且均大于 0。

1. 求概率 $P\{T>t\}$ 与 $P\{T>s+t\mid T>s\}$，其中 $s>0,t>0$；  
2. 任取 $n$ 个这种元件做寿命试验，测得它们的寿命分别为 $t_1,t_2,\ldots,t_n$，若 $m$ 已知，求 $\theta$ 的最大似然估计值。
""", r"""
$$
P(T>t)=e^{-(t/\theta)^m},
$$

$$
P(T>s+t\mid T>s)=e^{-((s+t)^m-s^m)/\theta^m},
$$

$$
\hat\theta=\left(\frac1n\sum_{i=1}^n t_i^m\right)^{1/m}.
$$
""", r"""
由分布函数得生存函数
$$
P(T>t)=1-F(t)=e^{-(t/\theta)^m}\qquad (t>0).
$$

因此
$$
P(T>s+t\mid T>s)
=\frac{P(T>s+t)}{P(T>s)}
=\frac{e^{-((s+t)/\theta)^m}}{e^{-(s/\theta)^m}}
=e^{-((s+t)^m-s^m)/\theta^m}.
$$

再求密度函数：
$$
f(t)=F'(t)=\frac{m}{\theta}\left(\frac{t}{\theta}\right)^{m-1}e^{-(t/\theta)^m},\qquad t>0.
$$

样本似然函数为
$$
L(\theta)=\prod_{i=1}^n \frac{m}{\theta}\left(\frac{t_i}{\theta}\right)^{m-1}e^{-(t_i/\theta)^m}.
$$
取对数：
$$
\ln L(\theta)
=n\ln m+(m-1)\sum_{i=1}^n\ln t_i-mn\ln\theta-\sum_{i=1}^n\frac{t_i^m}{\theta^m}.
$$

对 $\theta$ 求导并令其为 0：
$$
\frac{d}{d\theta}\ln L(\theta)
=-\frac{mn}{\theta}+\frac{m}{\theta^{m+1}}\sum_{i=1}^n t_i^m=0.
$$
解得
$$
\theta^m=\frac1n\sum_{i=1}^n t_i^m.
$$
故最大似然估计为
$$
\hat\theta=\left(\frac1n\sum_{i=1}^n t_i^m\right)^{1/m}.
$$
"""),
]


def annual_questions_md(questions: list[Question]) -> str:
    lines = [f"# {YEAR} 数学三真题", "", "资料类型：考研数学三历年真题", f"年份：{YEAR}", "科目：数学三", "整理状态：按原卷页图人工校对后转写。", ""]
    for item in questions:
        lines.extend([f"## 第 {item.number} 题", "", f"- 题型：{qtype_label(item.question_type)}", f"- 分值：{item.score}", f"- 模块：{item.module}", f"- 考点：{'、'.join(item.topics)}", "", item.stem, ""])
    return "\n".join(lines).rstrip() + "\n"


def annual_answers_md(questions: list[Question]) -> str:
    lines = [f"# {YEAR} 数学三答案解析", "", "资料类型：考研数学三答案解析", f"年份：{YEAR}", "科目：数学三", "整理状态：依据答案页和题面人工补写整理。", ""]
    groups = {k: [q for q in questions if q.question_type == k] for k in ("single_choice", "fill_blank", "solution")}
    for key in ("single_choice", "fill_blank", "solution"):
        lines.extend(["", f"## {qtype_label(key)}", "", "| 题号 | 答案 |", "|---|---|"])
        for item in groups[key]:
            lines.append(f"| {item.number} | {answer_for_table(item.answer)} |")
    lines.extend(["", "## 详细解析", ""])
    for item in questions:
        lines.extend([f"### 第 {item.number} 题", "", f"- 标准答案：{item.answer}", "", item.explanation, ""])
    return "\n".join(lines).rstrip() + "\n"


def build_cards(questions: list[Question]) -> None:
    card_dir = YEAR_DIR / "questions"
    card_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for item in questions:
        qid = question_id(item.number)
        card = "\n".join([
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
            *[f"  - {t}" for t in item.topics],
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
        ])
        (card_dir / f"q{item.number:03d}.md").write_text(card, encoding="utf-8")
        rows.append({
            "question_id": qid, "exam_id": f"kaoyan_math3_{YEAR}", "exam_type": "math3", "year": YEAR,
            "question_number": item.number, "question_type": item.question_type, "score": item.score,
            "module": item.module, "topics": item.topics, "difficulty": "unknown", "review_status": "reviewed",
            "answer_status": "available", "explanation_status": "available", "source_file": f"math3_{YEAR}_questions.md",
            "answer_source_file": f"math3_{YEAR}_answers.md", "card_path": f"questions/q{item.number:03d}.md",
            "answer": item.answer, "explanation": item.explanation,
        })
    with (YEAR_DIR / "questions.jsonl").open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    manifest = {
        "exam_id": f"kaoyan_math3_{YEAR}", "exam_type": "math3", "exam_label": "数学三", "year": YEAR,
        "source_files": {"questions": f"math3_{YEAR}_questions.md", "answers": f"math3_{YEAR}_answers.md"},
        "card_dir": "questions", "index_file": "questions.jsonl", "question_count": len(questions), "explanation_count": len(questions),
        "question_ids": [question_id(item.number) for item in questions], "generated_at": now_iso(),
        "review_status": "reviewed", "answer_status": "available", "explanation_status": "available",
    }
    (YEAR_DIR / "paper_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    (YEAR_DIR / f"math3_{YEAR}_questions.md").write_text(annual_questions_md(QUESTIONS), encoding="utf-8")
    (YEAR_DIR / f"math3_{YEAR}_answers.md").write_text(annual_answers_md(QUESTIONS), encoding="utf-8")
    build_cards(QUESTIONS)
    print(json.dumps({"year": YEAR, "question_count": len(QUESTIONS)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
