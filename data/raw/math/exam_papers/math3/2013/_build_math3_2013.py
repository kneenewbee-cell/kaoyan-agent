from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[6]
YEAR = 2013
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
        ["无穷小", "高阶无穷小"],
        "26",
        r"""
当 $x\to 0$ 时，用 $o(x)$ 表示比 $x$ 高阶的无穷小量，则下列式子中错误的是（ ）

(A) $x\cdot o(x^2)=o(x^3)$

(B) $o(x)\cdot o(x^2)=o(x^3)$

(C) $o(x^2)+o(x^2)=o(x^2)$

(D) $o(x)+o(x^2)=o(x^2)$
""",
        "D",
        r"""
由高阶无穷小的定义，
$$
o(x)+o(x^2)=o(x),
$$
一般不能保证仍是 $o(x^2)$，所以 `D` 错误。

其余各项都成立：例如 $o(x)\cdot o(x^2)$ 至少是比 $x^3$ 更高阶的无穷小。
""",
    ),
    q(
        2,
        "single_choice",
        4,
        "高等数学",
        ["间断点", "可去间断点"],
        "26",
        r"""
函数
$$
f(x)=\frac{|x|^{|x|}-1}{x(x+1)\ln|x|}
$$
的可去间断点的个数为（ ）

(A) $0$

(B) $1$

(C) $2$

(D) $3$
""",
        "C",
        r"""
函数在可能出现间断的点是 $x=0$ 与 $x=-1$。

当 $x\to 0$ 时，利用
$$
|x|^{|x|}=e^{|x|\ln|x|}=1+|x|\ln|x|+o(|x|\ln|x|),
$$
可知分子与分母同阶，极限存在。

当 $x\to -1$ 时，同样可将分子写为 $e^{|x|\ln|x|}-1$，配合分母中的 $(x+1)\ln|x|$，可算出左右极限存在且相等。

因此可去间断点共有 $2$ 个，选 `C`。
""",
    ),
    q(
        3,
        "single_choice",
        4,
        "高等数学",
        ["二重积分", "极坐标", "象限对称性"],
        "26",
        r"""
设 $D_k$ 是圆域
$$
D=\{(x,y)\mid x^2+y^2\le 1\}
$$
位于第 $k$ 象限的部分。记
$$
I_k=\iint_{D_k}(y-x)\,dxdy\qquad (k=1,2,3,4),
$$
则（ ）

(A) $I_1>0$

(B) $I_2>0$

(C) $I_3>0$

(D) $I_4>0$
""",
        "B",
        r"""
在第二象限中 $x<0,\ y>0$，因此被积函数
$$
y-x=y+|x|>0,
$$
从而
$$
I_2>0.
$$

而第一象限内 $y-x$ 正负皆可能；第三、四象限中又会因为 $x,y$ 的符号变化使积分不恒正。故正确项是 `B`。
""",
    ),
    q(
        4,
        "single_choice",
        4,
        "高等数学",
        ["正项级数", "比较判别法"],
        "26",
        r"""
设 $\{a_n\}$ 为正项数列，下列选项正确的是（ ）

(A) 若 $a_n>a_{n+1}$，则 $\sum\limits_{n=1}^{\infty}(-1)^{n-1}a_n$ 收敛

(B) 若 $\sum\limits_{n=1}^{\infty}(-1)^{n-1}a_n$ 收敛，则 $a_n>a_{n+1}$

(C) 若 $\sum\limits_{n=1}^{\infty}a_n$ 收敛，则存在常数 $p>1$，使 $\lim\limits_{n\to\infty}n^pa_n$ 存在

(D) 若存在常数 $p>1$，使 $\lim\limits_{n\to\infty}n^pa_n$ 存在，则 $\sum\limits_{n=1}^{\infty}a_n$ 收敛
""",
        "D",
        r"""
若存在 $p>1$ 使 $\lim\limits_{n\to\infty}n^pa_n=L$ 存在，则当 $n$ 足够大时
$$
a_n\sim \frac{L}{n^p}\quad \text{或}\quad a_n=O\!\left(\frac1{n^p}\right).
$$
由 $p$ 级数比较判别法，
$$
\sum a_n
$$
收敛，所以 `D` 正确。

其余三项都可举反例否定，例如交错级数收敛不必意味着单调性严格成立。
""",
    ),
    q(
        5,
        "single_choice",
        4,
        "线性代数",
        ["向量组等价", "可逆矩阵"],
        "26-27",
        r"""
设 $A,B,C$ 均为 $n$ 阶矩阵。若 $AB=C$，且 $B$ 可逆，则（ ）

(A) 矩阵 $C$ 的行向量组与矩阵 $A$ 的行向量组等价

(B) 矩阵 $C$ 的列向量组与矩阵 $A$ 的列向量组等价

(C) 矩阵 $C$ 的行向量组与矩阵 $B$ 的行向量组等价

(D) 矩阵 $C$ 的列向量组与矩阵 $B$ 的列向量组等价
""",
        "B",
        r"""
由 $C=AB$ 可知，$C$ 的每个列向量都是 $A$ 的列向量组的线性组合，因此 $C$ 的列向量组可由 $A$ 的列向量组线性表示。

又因为 $B$ 可逆，所以
$$
A=CB^{-1},
$$
故 $A$ 的列向量组也可由 $C$ 的列向量组线性表示。

因此矩阵 $C$ 与矩阵 $A$ 的列向量组等价，选 `B`。
""",
    ),
    q(
        6,
        "single_choice",
        4,
        "线性代数",
        ["矩阵相似", "特征值"],
        "27",
        r"""
矩阵
$$
\begin{pmatrix}
1&a&1\\
a&b&a\\
1&a&1
\end{pmatrix}
$$
与
$$
\begin{pmatrix}
2&0&0\\
0&b&0\\
0&0&0
\end{pmatrix}
$$
相似的充分必要条件为（ ）

(A) $a=0,\ b=2$

(B) $a=0,\ b$ 为任意常数

(C) $a=2,\ b=0$

(D) $a=2,\ b$ 为任意常数
""",
        "B",
        r"""
设
$$
M=
\begin{pmatrix}
1&a&1\\
a&b&a\\
1&a&1
\end{pmatrix}.
$$
由于第一行与第三行相同，$0$ 是其特征值。若它与对角矩阵 $\operatorname{diag}(2,b,0)$ 相似，则其全部特征值应为 $2,b,0$。

直接计算特征多项式可得
$$
|\lambda E-M|=\lambda\bigl((2-\lambda)(b-\lambda)-2a^2\bigr).
$$
要与
$$
\lambda(2-\lambda)(b-\lambda)
$$
一致，必须有
$$
a=0.
$$
当 $a=0$ 时，矩阵确实具有特征值 $2,b,0$，并且是实对称矩阵，可相似对角化。

故充要条件是 `B`。
""",
    ),
    q(
        7,
        "single_choice",
        4,
        "概率统计",
        ["正态分布", "区间概率比较"],
        "27",
        r"""
设 $X_1,X_2,X_3$ 是随机变量，且
$$
X_1\sim N(0,1),\qquad X_2\sim N(0,2^2),\qquad X_3\sim N(5,3^2),
$$
记
$$
p_i=P\{-2\le X_i\le 2\}\qquad (i=1,2,3),
$$
则（ ）

(A) $p_1>p_2>p_3$

(B) $p_2>p_1>p_3$

(C) $p_3>p_1>p_2$

(D) $p_1>p_3>p_2$
""",
        "A",
        r"""
对 $X_1\sim N(0,1)$，
$$
p_1=P(|X_1|\le 2)=2\Phi(2)-1.
$$

对 $X_2\sim N(0,4)$，
$$
p_2=P\left(\left|\frac{X_2}{2}\right|\le 1\right)=2\Phi(1)-1.
$$
由于 $\Phi(2)>\Phi(1)$，故 $p_1>p_2$。

对 $X_3\sim N(5,9)$，区间 $[-2,2]$ 整体位于均值 $5$ 左侧，故该概率显著小于前两者，因此
$$
p_1>p_2>p_3.
$$
选 `A`。
""",
    ),
    q(
        8,
        "single_choice",
        4,
        "概率统计",
        ["离散分布", "独立性"],
        "27",
        r"""
设随机变量 $X$ 和 $Y$ 相互独立，且 $X$ 和 $Y$ 的概率分布分别为

| $X$ | $0$ | $1$ | $2$ | $3$ |
|---|---:|---:|---:|---:|
| $P$ | $\dfrac12$ | $\dfrac14$ | $\dfrac18$ | $\dfrac18$ |

| $Y$ | $-1$ | $0$ | $1$ |
|---|---:|---:|---:|
| $P$ | $\dfrac13$ | $\dfrac13$ | $\dfrac13$ |

则 $P\{X+Y=2\}=（\ \ ）$

(A) $\dfrac1{12}$

(B) $\dfrac18$

(C) $\dfrac16$

(D) $\dfrac12$
""",
        "C",
        r"""
由独立性，
$$
P(X+Y=2)=P(X=1,Y=1)+P(X=2,Y=0)+P(X=3,Y=-1).
$$
因此
$$
P(X+Y=2)=\frac14\cdot\frac13+\frac18\cdot\frac13+\frac18\cdot\frac13
=\frac{1}{12}+\frac{1}{24}+\frac{1}{24}
=\frac16.
$$
故选 `C`。
""",
    ),
    q(
        9,
        "fill_blank",
        4,
        "高等数学",
        ["极限", "导数几何意义"],
        "27",
        r"""
设曲线 $y=f(x)$ 与 $y=x^2-x$ 在点 $(1,0)$ 处有公共切线，则
$$
\lim_{n\to\infty}n\,f\left(\frac{n}{n+2}\right)=\underline{\qquad}.
$$
""",
        r"$-2$",
        r"""
由“公共切线”知
$$
f(1)=0,\qquad f'(1)=\left.(2x-1)\right|_{x=1}=1.
$$
又
$$
\frac{n}{n+2}=1-\frac{2}{n+2}.
$$
故在 $x=1$ 附近作一阶展开：
$$
f\left(\frac{n}{n+2}\right)=f(1)+f'(1)\left(-\frac{2}{n+2}\right)+o\left(\frac1n\right)
=-\frac{2}{n+2}+o\left(\frac1n\right).
$$
于是
$$
\lim_{n\to\infty}n\,f\left(\frac{n}{n+2}\right)=-2.
$$
""",
    ),
    q(
        10,
        "fill_blank",
        4,
        "高等数学",
        ["隐函数求导"],
        "27",
        r"""
设函数 $z=z(x,y)$ 由方程
$$
(z+y)^x=xy
$$
确定，则
$$
\left.\frac{\partial z}{\partial x}\right|_{(1,2)}=\underline{\qquad}.
$$
""",
        r"$2(1-\ln 2)$",
        r"""
先在点 $(1,2)$ 求出 $z$：
$$
(z+2)^1=1\cdot 2,
$$
所以 $z=0$。

对等式两边取对数：
$$
x\ln(z+y)=\ln x+\ln y.
$$
对 $x$ 求偏导得
$$
\ln(z+y)+x\frac{z_x}{z+y}=\frac1x.
$$
代入 $(x,y,z)=(1,2,0)$，得到
$$
\ln 2+\frac{z_x}{2}=1.
$$
故
$$
z_x=2(1-\ln2).
$$
""",
    ),
    q(
        11,
        "fill_blank",
        4,
        "高等数学",
        ["反常积分", "分部积分"],
        "27",
        r"""
$$
\int_1^{+\infty}\frac{\ln x}{(1+x)^2}\,dx=\underline{\qquad}.
$$
""",
        r"$\ln 2$",
        r"""
分部积分，取
$$
u=\ln x,\qquad dv=\frac{dx}{(1+x)^2}.
$$
则
$$
du=\frac{dx}{x},\qquad v=-\frac{1}{1+x}.
$$
故
$$
\int_1^{+\infty}\frac{\ln x}{(1+x)^2}\,dx
=\left.-\frac{\ln x}{1+x}\right|_1^{+\infty}
+\int_1^{+\infty}\frac{1}{x(1+x)}\,dx.
$$
前一项为 $0$，后一项
$$
\int_1^{+\infty}\left(\frac1x-\frac1{1+x}\right)\,dx
=\ln 2.
$$
""",
    ),
    q(
        12,
        "fill_blank",
        4,
        "高等数学",
        ["常系数线性微分方程"],
        "27",
        r"""
微分方程
$$
y''-y'+\frac14y=0
$$
的通解为 $y=\underline{\qquad}$。
""",
        r"$e^{x/2}(C_1x+C_2)$",
        r"""
特征方程为
$$
r^2-r+\frac14=0,
$$
即
$$
\left(r-\frac12\right)^2=0.
$$
有二重根 $r=\dfrac12$，故通解为
$$
y=e^{x/2}(C_1x+C_2).
$$
""",
    ),
    q(
        13,
        "fill_blank",
        4,
        "线性代数",
        ["行列式", "伴随矩阵"],
        "27",
        r"""
设 $A=(a_{ij})$ 是 $3$ 阶非零矩阵，$|A|$ 为 $A$ 的行列式，$A_{ij}$ 为 $a_{ij}$ 的代数余子式。若
$$
a_{ij}+A_{ij}=0\qquad (i,j=1,2,3),
$$
则 $|A|=\underline{\qquad}$。
""",
        r"$-1$",
        r"""
由条件
$$
a_{ij}+A_{ij}=0
$$
可知
$$
A^*=-A.
$$
又由伴随矩阵恒等式
$$
AA^*=|A|E
$$
得
$$
A(-A)=|A|E.
$$
两边取行列式，并注意 $A\ne 0$，可推出
$$
|A|=-1.
$$
""",
    ),
    q(
        14,
        "fill_blank",
        4,
        "概率统计",
        ["正态分布", "矩母函数"],
        "27",
        r"""
设随机变量 $X$ 服从标准正态分布 $N(0,1)$，则
$$
E(Xe^{2X})=\underline{\qquad}.
$$
""",
        r"$2e^2$",
        r"""
标准正态分布的矩母函数为
$$
M_X(t)=E(e^{tX})=e^{t^2/2}.
$$
于是
$$
E(Xe^{tX})=M_X'(t)=te^{t^2/2}.
$$
取 $t=2$，得
$$
E(Xe^{2X})=2e^2.
$$
""",
    ),
    q(
        15,
        "solution",
        10,
        "高等数学",
        ["等价无穷小", "泰勒展开"],
        "27-28",
        r"""
当 $x\to 0$ 时，$1-\cos x\cdot\cos 2x\cdot\cos 3x$ 与 $ax^n$ 为等价无穷小，求 $n$ 与 $a$ 的值。
""",
        r"$n=2,\ a=7$",
        r"""
利用
$$
\cos(kx)=1-\frac{k^2x^2}{2}+o(x^2)\qquad (k=1,2,3),
$$
有
$$
\cos x\cos 2x\cos 3x
=\left(1-\frac{x^2}{2}\right)\left(1-2x^2\right)\left(1-\frac{9x^2}{2}\right)+o(x^2).
$$
只保留二次项，得
$$
\cos x\cos 2x\cos 3x
=1-\left(\frac12+2+\frac92\right)x^2+o(x^2)
=1-7x^2+o(x^2).
$$
因此
$$
1-\cos x\cos 2x\cos 3x=7x^2+o(x^2).
$$
所以
$$
n=2,\qquad a=7.
$$
""",
    ),
    q(
        16,
        "solution",
        10,
        "高等数学",
        ["定积分应用", "旋转体体积"],
        "27-28",
        r"""
设 $D$ 是由曲线 $y=x^{1/3}$、直线 $x=a$（$a>0$）及 $x$ 轴所围成的平面图形，$V_x,\ V_y$ 分别是 $D$ 绕 $x$ 轴、$y$ 轴旋转一周所得旋转体的体积。若 $V_y=10V_x$，求 $a$ 的值。
""",
        r"$a=7^{3/2}$",
        r"""
区域为
$$
0\le x\le a,\qquad 0\le y\le x^{1/3}.
$$
绕 $x$ 轴旋转：
$$
V_x=\pi\int_0^a \left(x^{1/3}\right)^2dx
=\pi\int_0^a x^{2/3}dx
=\frac{3\pi}{5}a^{5/3}.
$$

绕 $y$ 轴旋转：
$$
V_y=2\pi\int_0^a x\cdot x^{1/3}dx
=2\pi\int_0^a x^{4/3}dx
=\frac{6\pi}{7}a^{7/3}.
$$
由 $V_y=10V_x$，得
$$
\frac{6\pi}{7}a^{7/3}=10\cdot \frac{3\pi}{5}a^{5/3}=6\pi a^{5/3}.
$$
约去公共因子后有
$$
a^{2/3}=7,
$$
故
$$
a=7^{3/2}.
$$
""",
    ),
    q(
        17,
        "solution",
        10,
        "高等数学",
        ["二重积分", "区域划分"],
        "28",
        r"""
设平面区域 $D$ 由直线 $x=3y,\ y=3x$ 及 $x+y=8$ 围成，计算
$$
\iint_D x^2\,dxdy.
$$
""",
        r"$\dfrac{416}{3}$",
        r"""
三条直线围成三角形，顶点为
$$
(0,0),\quad (2,6),\quad (6,2).
$$
按 $x$ 分段：

当 $0\le x\le 2$ 时，
$$
\frac{x}{3}\le y\le 3x.
$$

当 $2\le x\le 6$ 时，
$$
\frac{x}{3}\le y\le 8-x.
$$

故
$$
\iint_Dx^2\,dxdy
=\int_0^2x^2\left(3x-\frac{x}{3}\right)dx
+\int_2^6x^2\left((8-x)-\frac{x}{3}\right)dx.
$$
即
$$
=\int_0^2\frac{8}{3}x^3dx+\int_2^6\left(8x^2-\frac{4}{3}x^3\right)dx
=\frac{32}{3}+128
=\frac{416}{3}.
$$
""",
    ),
    q(
        18,
        "solution",
        10,
        "概率统计",
        ["经济应用", "利润函数"],
        "28",
        r"""
设生产某商品的固定成本为 $60\,000$ 元，可变成本为 $20$ 元/件，价格函数为
$$
p=60-\frac{Q}{1000}
$$
（$p$ 是单价，单位：元；$Q$ 是销量，单位：件）。已知产销平衡，求：

1. 该商品的边际利润；

2. 当 $p=50$ 时的边际利润，并解释其经济意义；

3. 使得利润最大的定价 $p$。
""",
        r"""
边际利润为
$$
\Pi'(Q)=40-\frac{Q}{500};
$$
当 $p=50$ 时边际利润为 $20$；
利润最大时的定价为 $40$ 元。
""",
        r"""
利润函数为
$$
\Pi(Q)=pQ-(60000+20Q)
=\left(60-\frac{Q}{1000}\right)Q-60000-20Q
=40Q-\frac{Q^2}{1000}-60000.
$$
故边际利润
$$
\Pi'(Q)=40-\frac{Q}{500}.
$$

当 $p=50$ 时，由
$$
50=60-\frac{Q}{1000}
$$
得
$$
Q=10000.
$$
于是
$$
\Pi'(10000)=40-\frac{10000}{500}=20.
$$
其经济意义是：当价格为 $50$ 元、销量处于对应平衡点时，销量每增加 $1$ 件，利润约增加 $20$ 元。

要使利润最大，令
$$
\Pi'(Q)=0,
$$
得
$$
Q=20000.
$$
代回价格函数：
$$
p=60-\frac{20000}{1000}=40.
$$
""",
    ),
    q(
        19,
        "solution",
        10,
        "高等数学",
        ["连续函数", "拉格朗日中值定理"],
        "28",
        r"""
设函数 $f(x)$ 在 $[0,+\infty)$ 上可导，$f(0)=0$ 且 $\lim\limits_{x\to+\infty}f(x)=2$。证明：

1. 存在 $a>0$，使得 $f(a)=1$；

2. 对（1）中的 $a$，存在 $\xi\in(0,a)$，使得 $f'(\xi)=\dfrac1a$。
""",
        "命题成立",
        r"""
因为
$$
\lim_{x\to+\infty}f(x)=2,
$$
所以存在 $X>0$，使得当 $x>X$ 时，
$$
f(x)>1.
$$
函数 $f$ 在 $[0,X]$ 上连续，又
$$
f(0)=0<1,\qquad f(X)>1,
$$
由介值定理知，存在
$$
a\in(0,X)
$$
使得
$$
f(a)=1.
$$

再看区间 $[0,a]$。函数 $f$ 在其上连续、在其内可导，故由拉格朗日中值定理，存在
$$
\xi\in(0,a)
$$
使得
$$
f'(\xi)=\frac{f(a)-f(0)}{a-0}=\frac{1-0}{a}=\frac1a.
$$
证毕。
""",
    ),
    q(
        20,
        "solution",
        11,
        "线性代数",
        ["矩阵方程", "线性方程组"],
        "28",
        r"""
设
$$
A=
\begin{pmatrix}
1&a\\
1&0
\end{pmatrix},\qquad
B=
\begin{pmatrix}
0&1\\
1&b
\end{pmatrix}.
$$
当 $a,b$ 为何值时，存在矩阵 $C$ 使得
$$
AC-CA=B,
$$
并求所有矩阵 $C$。
""",
        r"""
存在解当且仅当
$$
a=-1,\qquad b=0.
$$
此时全部解为
$$
C=
\begin{pmatrix}
s+t+1 & -s\\
s & t
\end{pmatrix},\qquad s,t\in\mathbb R.
$$
""",
        r"""
设
$$
C=
\begin{pmatrix}
x_1&x_2\\
x_3&x_4
\end{pmatrix}.
$$
则
$$
AC=
\begin{pmatrix}
x_1+ax_3 & x_2+ax_4\\
x_1 & x_2
\end{pmatrix},
\qquad
CA=
\begin{pmatrix}
x_1+x_2 & ax_1\\
x_3+x_4 & ax_3
\end{pmatrix}.
$$
因此
$$
AC-CA=
\begin{pmatrix}
ax_3-x_2 & -ax_1+x_2+ax_4\\
x_1-x_3-x_4 & x_2-ax_3
\end{pmatrix}
=
\begin{pmatrix}
0&1\\
1&b
\end{pmatrix}.
$$
得到方程组
$$
\begin{cases}
ax_3-x_2=0,\\
-ax_1+x_2+ax_4=1,\\
x_1-x_3-x_4=1,\\
x_2-ax_3=b.
\end{cases}
$$
由第一式与第四式立刻得到
$$
b=0.
$$
再由第一式 $x_2=ax_3$ 代入第二式，结合第三式
$$
x_1-x_3-x_4=1
$$
可得
$$
a(-x_1+x_3+x_4)=1.
$$
而第三式等价于
$$
-x_1+x_3+x_4=-1,
$$
所以
$$
-a=1,\qquad a=-1.
$$

当 $a=-1,\ b=0$ 时，令
$$
x_3=s,\qquad x_4=t,
$$
则
$$
x_2=-s,\qquad x_1=s+t+1.
$$
故全部解为
$$
C=
\begin{pmatrix}
s+t+1 & -s\\
s & t
\end{pmatrix},\qquad s,t\in\mathbb R.
$$
""",
    ),
    q(
        21,
        "solution",
        11,
        "线性代数",
        ["二次型", "正交变换"],
        "29",
        r"""
设二次型
$$
f(x_1,x_2,x_3)=2(a_1x_1+a_2x_2+a_3x_3)^2+(b_1x_1+b_2x_2+b_3x_3)^2,
$$
记
$$
\alpha=\begin{pmatrix}a_1\\a_2\\a_3\end{pmatrix},\qquad
\beta=\begin{pmatrix}b_1\\b_2\\b_3\end{pmatrix}.
$$

1. 证明二次型 $f$ 对应的矩阵为 $2\alpha\alpha^T+\beta\beta^T$；

2. 若 $\alpha,\beta$ 正交且均为单位向量，证明 $f$ 在正交变换下的标准形为 $2y_1^2+y_2^2$。
""",
        r"""
对应矩阵为
$$
2\alpha\alpha^T+\beta\beta^T,
$$
且在条件 $\alpha\perp\beta,\ \|\alpha\|=\|\beta\|=1$ 下，标准形为
$$
2y_1^2+y_2^2.
$$
""",
        r"""
先将二次型写成矩阵形式：
$$
f(x)=2(\alpha^Tx)^2+(\beta^Tx)^2
=2x^T\alpha\alpha^Tx+x^T\beta\beta^Tx
=x^T(2\alpha\alpha^T+\beta\beta^T)x.
$$
故对应矩阵就是
$$
A=2\alpha\alpha^T+\beta\beta^T.
$$

若 $\alpha,\beta$ 正交且均为单位向量，则
$$
A\alpha=2\alpha,\qquad A\beta=\beta.
$$
因此 $2$ 与 $1$ 是 $A$ 的特征值，对应特征向量分别为 $\alpha,\beta$。

又因为
$$
r(A)\le r(2\alpha\alpha^T)+r(\beta\beta^T)\le 2,
$$
故第三个特征值必为 $0$。

矩阵 $A$ 为实对称矩阵，所以存在正交矩阵使其对角化为
$$
\operatorname{diag}(2,1,0).
$$
于是二次型在正交变换下的标准形为
$$
2y_1^2+y_2^2.
$$
""",
    ),
    q(
        22,
        "solution",
        11,
        "概率统计",
        ["二维连续分布", "边缘密度", "条件密度"],
        "29",
        r"""
设 $(X,Y)$ 是二维随机变量，$X$ 的边缘概率密度为
$$
f_X(x)=
\begin{cases}
3x^2,& 0<x<1,\\
0,& \text{其他},
\end{cases}
$$
在给定 $X=x$（$0<x<1$）的条件下，$Y$ 的条件概率密度为
$$
f_{Y\mid X}(y\mid x)=
\begin{cases}
\dfrac{3y^2}{x^3},& 0<y<x,\\
0,& \text{其他}.
\end{cases}
$$

1. 求 $(X,Y)$ 的概率密度 $f(x,y)$；

2. 求 $Y$ 的边缘概率密度 $f_Y(y)$；

3. 求 $P\{X>2Y\}$。
""",
        r"""
$$
f(x,y)=
\begin{cases}
9y^2,& 0<y<x<1,\\
0,& \text{其他},
\end{cases}
$$
$$
f_Y(y)=
\begin{cases}
9y^2(1-y),& 0<y<1,\\
0,& \text{其他},
\end{cases}
$$
且
$$
P\{X>2Y\}=\frac{3}{32}.
$$
""",
        r"""
由联合密度与条件密度关系
$$
f(x,y)=f_{Y\mid X}(y\mid x)f_X(x),
$$
得
$$
f(x,y)=
\begin{cases}
\dfrac{3y^2}{x^3}\cdot 3x^2=9y^2,& 0<y<x<1,\\
0,& \text{其他}.
\end{cases}
$$

于是
$$
f_Y(y)=\int_y^1 9y^2\,dx
=9y^2(1-y),\qquad 0<y<1.
$$
其余处为 $0$。

最后，
$$
P(X>2Y)=\iint_{x>2y}f(x,y)\,dxdy.
$$
由约束 $0<y<x<1$ 与 $x>2y$，可知
$$
0<y<\frac12,\qquad 2y<x<1.
$$
故
$$
P(X>2Y)=\int_0^{1/2}\int_{2y}^1 9y^2\,dxdy
=\int_0^{1/2}9y^2(1-2y)\,dy
=\frac{3}{32}.
$$
""",
    ),
    q(
        23,
        "solution",
        11,
        "概率统计",
        ["参数估计", "矩估计", "最大似然估计"],
        "29",
        r"""
设总体 $X$ 的概率密度为
$$
f(x;\theta)=
\begin{cases}
\dfrac{\theta^2}{x^3}e^{-\theta/x},& x>0,\\
0,& \text{其他},
\end{cases}
$$
其中 $\theta$ 为未知参数且大于零，$X_1,X_2,\cdots,X_n$ 为来自总体 $X$ 的简单随机样本。

1. 求 $\theta$ 的矩估计量；

2. 求 $\theta$ 的最大似然估计量。
""",
        r"""
矩估计量为
$$
\hat\theta_{\text{矩}}=\overline X;
$$
最大似然估计量为
$$
\hat\theta_{\text{MLE}}=\frac{2n}{\sum_{i=1}^n\frac1{X_i}}.
$$
""",
        r"""
先求总体期望：
$$
E(X)=\int_0^\infty x\cdot \frac{\theta^2}{x^3}e^{-\theta/x}\,dx
=\int_0^\infty \frac{\theta^2}{x^2}e^{-\theta/x}\,dx.
$$
令
$$
u=\frac{\theta}{x},\qquad x=\frac{\theta}{u},\qquad dx=-\frac{\theta}{u^2}\,du,
$$
则
$$
E(X)=\theta\int_0^\infty e^{-u}\,du=\theta.
$$
因此矩估计由
$$
\overline X=E(X)=\theta
$$
得到
$$
\hat\theta_{\text{矩}}=\overline X.
$$

再求最大似然估计。样本似然函数为
$$
L(\theta)=\prod_{i=1}^n\frac{\theta^2}{X_i^3}e^{-\theta/X_i}
=\theta^{2n}\left(\prod_{i=1}^nX_i^{-3}\right)\exp\left(-\theta\sum_{i=1}^n\frac1{X_i}\right).
$$
取对数得
$$
\ln L(\theta)=2n\ln\theta-3\sum_{i=1}^n\ln X_i-\theta\sum_{i=1}^n\frac1{X_i}.
$$
求导并令其为零：
$$
\frac{d}{d\theta}\ln L(\theta)=\frac{2n}{\theta}-\sum_{i=1}^n\frac1{X_i}=0.
$$
解得
$$
\hat\theta_{\text{MLE}}=\frac{2n}{\sum_{i=1}^n\frac1{X_i}}.
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
