from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[6]
EXAM_ROOT = ROOT / "data" / "raw" / "math" / "exam_papers"
YEAR = 2005
YEAR_DIR = EXAM_ROOT / "math3" / str(YEAR)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def qtype_label(qtype: str) -> str:
    return {
        "fill_blank": "填空题",
        "single_choice": "选择题",
        "solution": "解答题",
    }[qtype]


def answer_for_table(answer: str) -> str:
    brief = " ".join(answer.replace("\n", " ").split())
    if len(brief) > 56 or "\\begin{" in brief:
        return "见详细解析"
    return brief


def question_id(number: int) -> str:
    return f"kaoyan_math3_{YEAR}_q{number:03d}"


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
        "fill_blank",
        4,
        "高等数学",
        ["极限", "等价无穷小"],
        "25",
        r"""
极限
$$
\lim_{x\to\infty} x\sin\frac{2x}{x^2+1} = \underline{\qquad}.
$$
""",
        r"$2$",
        r"""
当 $x\to\infty$ 时，
$$
\frac{2x}{x^2+1}\sim \frac{2}{x},
$$
于是
$$
x\sin\frac{2x}{x^2+1}\sim x\cdot \frac{2x}{x^2+1}\to 2.
$$
""",
    ),
    q(
        2,
        "fill_blank",
        4,
        "高等数学",
        ["微分方程", "一阶线性方程"],
        "25",
        r"""
微分方程
$$
xy' + y = 0
$$
满足初始条件 $y(1)=2$ 的特解为 $\underline{\qquad}$。
""",
        r"$xy=2$",
        r"""
原方程可写成
$$
(xy)'=0,
$$
积分得 $xy=C$。由初始条件 $y(1)=2$ 得 $C=2$，故特解为
$$
xy=2.
$$
""",
    ),
    q(
        3,
        "fill_blank",
        4,
        "高等数学",
        ["全微分", "偏导数"],
        "25",
        r"""
设二元函数
$$
z=xe^{x+y}+(x+1)\ln(1+y),
$$
则
$$
dz\big|_{(1,0)}=\underline{\qquad}.
$$
""",
        r"$2e\,dx+(e+2)\,dy$",
        r"""
有
$$
\frac{\partial z}{\partial x}=e^{x+y}+xe^{x+y}+\ln(1+y),
\qquad
\frac{\partial z}{\partial y}=xe^{x+y}+\frac{x+1}{1+y}.
$$
在 $(1,0)$ 处，
$$
\frac{\partial z}{\partial x}=2e,\qquad
\frac{\partial z}{\partial y}=e+2.
$$
故
$$
dz\big|_{(1,0)}=2e\,dx+(e+2)\,dy.
$$
""",
    ),
    q(
        4,
        "fill_blank",
        4,
        "线性代数",
        ["行列式", "线性相关"],
        "25",
        r"""
设行向量组
$$
(2,1,1,1),\ (2,1,a,a),\ (3,2,1,a),\ (4,3,2,1)
$$
线性相关，且 $a\ne 1$，则
$$
a=\underline{\qquad}.
$$
""",
        r"$\dfrac12$",
        r"""
四个 $4$ 维向量线性相关，其对应行列式应为零：
$$
\begin{vmatrix}
2&1&1&1\\
2&1&a&a\\
3&2&1&a\\
4&3&2&1
\end{vmatrix}
=(a-1)(2a-1)=0.
$$
解得 $a=1$ 或 $a=\dfrac12$。由题设 $a\ne1$，故
$$
a=\frac12.
$$
""",
    ),
    q(
        5,
        "fill_blank",
        4,
        "概率统计",
        ["全概率公式", "离散型随机变量"],
        "25",
        r"""
从数 $1,2,3,4$ 中任取一个数，记为 $X$，再从 $1,\cdots,X$ 中任取一个数，记为 $Y$，则
$$
P\{Y=2\}=\underline{\qquad}.
$$
""",
        r"$\dfrac{13}{48}$",
        r"""
按 $X$ 分解：
$$
P\{Y=2\}
=\sum_{k=1}^4 P\{X=k\}P\{Y=2\mid X=k\}.
$$
其中
$$
P\{X=k\}=\frac14,\quad
P\{Y=2\mid X=1\}=0,\ 
P\{Y=2\mid X=2\}=\frac12,\ 
P\{Y=2\mid X=3\}=\frac13,\ 
P\{Y=2\mid X=4\}=\frac14.
$$
所以
$$
P\{Y=2\}
=\frac14\left(0+\frac12+\frac13+\frac14\right)
=\frac{13}{48}.
$$
""",
    ),
    q(
        6,
        "fill_blank",
        4,
        "概率统计",
        ["二维离散分布", "独立性"],
        "25",
        r"""
设二维随机变量 $(X,Y)$ 的概率分布为

| $X\backslash Y$ | $0$ | $1$ |
|---|---:|---:|
| $0$ | $0.4$ | $a$ |
| $1$ | $b$ | $0.1$ |

若随机事件 $\{X=0\}$ 与 $\{X+Y=1\}$ 相互独立，则
$$
a=\underline{\qquad},\qquad b=\underline{\qquad}.
$$
""",
        r"$a=0.4,\ b=0.1$",
        r"""
由概率和为 $1$，得
$$
a+b=0.5.
$$
又
$$
P(X=0)=0.4+a,\qquad P(X+Y=1)=a+b.
$$
而
$$
P(X=0,\ X+Y=1)=P(X=0,Y=1)=a.
$$
由独立性，
$$
a=P(X=0)\,P(X+Y=1)=(0.4+a)(a+b).
$$
再结合 $a+b=0.5$，解得
$$
a=0.4,\qquad b=0.1.
$$
""",
    ),
    q(
        7,
        "single_choice",
        4,
        "高等数学",
        ["函数零点", "导数与极值"],
        "25",
        r"""
当 $a$ 取下列哪个值时，函数
$$
f(x)=2x^3-9x^2+12x-a
$$
恰有两个不同的零点。（ ）

(A) $2$  
(B) $4$  
(C) $6$  
(D) $8$
""",
        "B",
        r"""
有
$$
f'(x)=6x^2-18x+12=6(x-1)(x-2),
$$
故可能极值点为 $x=1,2$。计算得
$$
f(1)=5-a,\qquad f(2)=4-a.
$$
恰有两个不同零点时，需要有一个极值恰好为 $0$，由此得 $a=4$，故选 `B`。
""",
    ),
    q(
        8,
        "single_choice",
        4,
        "高等数学",
        ["二重积分", "单调性比较"],
        "25",
        r"""
设
$$
I_1=\iint_D \cos\sqrt{x^2+y^2}\,d\sigma,\quad
I_2=\iint_D \cos(x^2+y^2)\,d\sigma,\quad
I_3=\iint_D \cos(x^2+y^2)^2\,d\sigma,
$$
其中
$$
D=\{(x,y)\mid x^2+y^2\le 1\},
$$
则（ ）

(A) $I_3>I_2>I_1$  
(B) $I_1>I_2>I_3$  
(C) $I_2>I_1>I_3$  
(D) $I_3>I_1>I_2$
""",
        "A",
        r"""
在区域 $D$ 上有
$$
0\le (x^2+y^2)^2 \le x^2+y^2 \le \sqrt{x^2+y^2}\le 1<\frac{\pi}{2}.
$$
由于 $\cos t$ 在 $\left(0,\frac{\pi}{2}\right)$ 上单调递减，所以
$$
\cos\sqrt{x^2+y^2}\le \cos(x^2+y^2)\le \cos(x^2+y^2)^2.
$$
对区域 $D$ 积分可得
$$
I_1<I_2<I_3,
$$
故选 `A`。
""",
    ),
    q(
        9,
        "single_choice",
        4,
        "高等数学",
        ["数项级数", "反例"],
        "25",
        r"""
设 $a_n>0,\ n=1,2,\cdots$。若
$$
\sum_{n=1}^{\infty} a_n
$$
发散，
$$
\sum_{n=1}^{\infty}(-1)^{n-1}a_n
$$
收敛，则下列结论正确的是（ ）

(A) $\displaystyle\sum_{n=1}^{\infty} a_{2n-1}$ 收敛，$\displaystyle\sum_{n=1}^{\infty} a_{2n}$ 发散  
(B) $\displaystyle\sum_{n=1}^{\infty} a_{2n}$ 收敛，$\displaystyle\sum_{n=1}^{\infty} a_{2n-1}$ 发散  
(C) $\displaystyle\sum_{n=1}^{\infty}(a_{2n-1}+a_{2n})$ 收敛  
(D) $\displaystyle\sum_{n=1}^{\infty}(a_{2n-1}-a_{2n})$ 收敛
""",
        "D",
        r"""
取反例 $a_n=\dfrac1n$。则
$$
\sum a_n
$$
发散，而
$$
\sum (-1)^{n-1}a_n
$$
收敛。此时奇项级数和偶项级数都发散，所以 `A`、`B` 错；并且
$$
\sum (a_{2n-1}+a_{2n})
$$
仍发散，故 `C` 错。  
另一方面，
$$
\sum (a_{2n-1}-a_{2n})
$$
正是交错级数的分组形式，收敛，故选 `D`。
""",
    ),
    q(
        10,
        "single_choice",
        4,
        "高等数学",
        ["极值", "二阶导数判别法"],
        "25",
        r"""
设
$$
f(x)=x\sin x+\cos x,
$$
下列命题中正确的是（ ）

(A) $f(0)$ 是极大值，$f\left(\dfrac{\pi}{2}\right)$ 是极小值  
(B) $f(0)$ 是极小值，$f\left(\dfrac{\pi}{2}\right)$ 是极大值  
(C) $f(0)$ 是极大值，$f\left(\dfrac{\pi}{2}\right)$ 也是极大值  
(D) $f(0)$ 是极小值，$f\left(\dfrac{\pi}{2}\right)$ 也是极小值
""",
        "B",
        r"""
有
$$
f'(x)=x\cos x,
$$
故 $f'(0)=0,\ f'\left(\dfrac{\pi}{2}\right)=0$。再算
$$
f''(x)=\cos x-x\sin x.
$$
于是
$$
f''(0)=1>0,\qquad
f''\left(\frac{\pi}{2}\right)=-\frac{\pi}{2}<0.
$$
所以 $f(0)$ 为极小值，$f\left(\dfrac{\pi}{2}\right)$ 为极大值，选 `B`。
""",
    ),
    q(
        11,
        "single_choice",
        4,
        "高等数学",
        ["有界性", "反例"],
        "26",
        r"""
以下四个命题中，正确的是（ ）

(A) 若 $f'(x)$ 在 $(0,1)$ 内连续，则 $f(x)$ 在 $(0,1)$ 内有界。  
(B) 若 $f(x)$ 在 $(0,1)$ 内连续，则 $f(x)$ 在 $(0,1)$ 内有界。  
(C) 若 $f'(x)$ 在 $(0,1)$ 内有界，则 $f(x)$ 在 $(0,1)$ 内有界。  
(D) 若 $f(x)$ 在 $(0,1)$ 内有界，则 $f'(x)$ 在 $(0,1)$ 内有界。
""",
        "C",
        r"""
`A`、`B` 不对，例如 $f(x)=\dfrac1x$ 在 $(0,1)$ 内连续，且 $f'(x)=-\dfrac1{x^2}$ 也连续，但 $f(x)$ 无界。  
`D` 不对，例如 $f(x)=\sqrt x$ 在 $(0,1)$ 内有界，但
$$
f'(x)=\frac{1}{2\sqrt x}
$$
无界。  
若 $f'(x)$ 在 $(0,1)$ 内有界，则 $f$ 满足 Lipschitz 型估计，从而在该区间内不能发散，故 `C` 正确。
""",
    ),
    q(
        12,
        "single_choice",
        4,
        "线性代数",
        ["伴随矩阵", "行列式"],
        "26",
        r"""
设矩阵 $A=(a_{ij})_{3\times 3}$ 满足
$$
A^*=A^T,
$$
其中 $A^*$ 为 $A$ 的伴随矩阵，$A^T$ 为 $A$ 的转置矩阵。若 $a_{11},a_{12},a_{13}$ 为三个相等的正数，则 $a_{11}$ 为（ ）

(A) $\dfrac{\sqrt3}{3}$  
(B) $3$  
(C) $\dfrac13$  
(D) $\sqrt3$
""",
        "A",
        r"""
由
$$
AA^*=|A|E
$$
及 $A^*=A^T$ 得
$$
AA^T=|A|E.
$$
从而 $|A|^2=|A|^3$，又因 $a_{11},a_{12},a_{13}$ 为相等正数，不可能有 $|A|=0$，故 $|A|=1$。  
设 $a_{11}=a_{12}=a_{13}=t>0$，则第一行与对应代数余子式关系给出
$$
3t^2=1,
$$
故
$$
t=\frac{\sqrt3}{3}.
$$
选 `A`。
""",
    ),
    q(
        13,
        "single_choice",
        4,
        "线性代数",
        ["特征值", "线性无关"],
        "26",
        r"""
设 $\lambda_1,\lambda_2$ 是矩阵 $A$ 的两个不同的特征值，对应的特征向量分别为 $\alpha_1,\alpha_2$，则 $\alpha_1,\ A(\alpha_1+\alpha_2)$ 线性无关的充分必要条件是（ ）

(A) $\lambda_1=0$  
(B) $\lambda_2=0$  
(C) $\lambda_1\ne 0$  
(D) $\lambda_2\ne 0$
""",
        "D",
        r"""
有
$$
A(\alpha_1+\alpha_2)=\lambda_1\alpha_1+\lambda_2\alpha_2.
$$
在基 $\{\alpha_1,\alpha_2\}$ 下，向量组
$$
\alpha_1,\ A(\alpha_1+\alpha_2)
$$
的系数矩阵为
$$
\begin{pmatrix}
1 & \lambda_1\\
0 & \lambda_2
\end{pmatrix}.
$$
其行列式为 $\lambda_2$，故线性无关当且仅当 $\lambda_2\ne 0$。选 `D`。
""",
    ),
    q(
        14,
        "single_choice",
        4,
        "概率统计",
        ["置信区间", "t分布"],
        "26",
        r"""
（超纲题）设一批零件的长度服从正态分布 $N(\mu,\sigma^2)$，其中 $\mu,\sigma^2$ 均未知。现从中随机抽取 $16$ 个零件，测得样本均值 $\bar x=20(\mathrm{cm})$，样本标准差 $S=1(\mathrm{cm})$，则 $\mu$ 的置信度为 $0.90$ 的置信区间是（ ）

(A) $\left(20-\dfrac14 t_{0.05}(16),\,20+\dfrac14 t_{0.05}(16)\right)$  
(B) $\left(20-\dfrac14 t_{0.1}(16),\,20+\dfrac14 t_{0.1}(16)\right)$  
(C) $\left(20-\dfrac14 t_{0.05}(15),\,20+\dfrac14 t_{0.05}(15)\right)$  
(D) $\left(20-\dfrac14 t_{0.1}(15),\,20+\dfrac14 t_{0.1}(15)\right)$
""",
        "C",
        r"""
总体方差未知，故用统计量
$$
\frac{\bar X-\mu}{S/\sqrt n}\sim t(n-1).
$$
这里 $n=16$，自由度为 $15$，置信度 $0.90$ 对应双侧临界值 $t_{0.05}(15)$。  
又
$$
\frac{S}{\sqrt n}=\frac14,
$$
所以区间为
$$
\left(20-\frac14 t_{0.05}(15),\,20+\frac14 t_{0.05}(15)\right).
$$
故选 `C`。
""",
    ),
    q(
        15,
        "solution",
        8,
        "高等数学",
        ["极限", "洛必达法则"],
        "26",
        r"""
求极限
$$
\lim_{x\to 0}\left(\frac{1+x}{1-e^{-x}}-\frac1x\right).
$$
""",
        r"$\dfrac32$",
        r"""
通分得
$$
\frac{1+x}{1-e^{-x}}-\frac1x
=\frac{x+x^2-1+e^{-x}}{x(1-e^{-x})}.
$$
这是 $0/0$ 型，应用洛必达法则：
$$
\lim_{x\to0}\frac{x+x^2-1+e^{-x}}{x(1-e^{-x})}
=\lim_{x\to0}\frac{1+2x-e^{-x}}{1-e^{-x}+xe^{-x}}
=\lim_{x\to0}\frac{2+e^{-x}}{2e^{-x}}
=\frac32.
$$
""",
    ),
    q(
        16,
        "solution",
        8,
        "高等数学",
        ["偏导数", "复合函数"],
        "26",
        r"""
设 $f(u)$ 具有二阶连续导数，且
$$
g(x,y)=f\left(\frac{y}{x}\right)+yf\left(\frac{x}{y}\right),
$$
求
$$
x^2\frac{\partial^2 g}{\partial x^2}-y^2\frac{\partial^2 g}{\partial y^2}.
$$
""",
        r"$\dfrac{2y}{x}f'\!\left(\dfrac{y}{x}\right)$",
        r"""
先求偏导：
$$
\frac{\partial g}{\partial x}
=-\frac{y}{x^2}f'\!\left(\frac{y}{x}\right)+f'\!\left(\frac{x}{y}\right),
$$
$$
\frac{\partial g}{\partial y}
=\frac1x f'\!\left(\frac{y}{x}\right)+f\!\left(\frac{x}{y}\right)-\frac{x}{y}f'\!\left(\frac{x}{y}\right).
$$
继续求二阶偏导并整理，可得
$$
x^2\frac{\partial^2 g}{\partial x^2}-y^2\frac{\partial^2 g}{\partial y^2}
=\frac{2y}{x}f'\!\left(\frac{y}{x}\right).
$$
""",
    ),
    q(
        17,
        "solution",
        9,
        "高等数学",
        ["二重积分", "区域分割"],
        "26",
        r"""
计算二重积分
$$
\iint_D |x^2+y^2-1|\,d\sigma,
\qquad
D=\{(x,y)\mid 0\le x\le 1,\ 0\le y\le 1\}.
$$
""",
        r"$\dfrac{\pi}{4}-\dfrac13$",
        r"""
在正方形区域 $D$ 内，曲线 $x^2+y^2=1$ 将区域分成两部分。记
$$
D_1=\{(x,y)\in D\mid x^2+y^2\le 1\},\qquad
D_2=\{(x,y)\in D\mid x^2+y^2>1\}.
$$
则
$$
\iint_D |x^2+y^2-1|\,d\sigma
=-\iint_{D_1}(x^2+y^2-1)\,d\sigma+\iint_{D_2}(x^2+y^2-1)\,d\sigma.
$$
计算后得
$$
\iint_D |x^2+y^2-1|\,d\sigma
=\frac{\pi}{4}-\frac13.
$$
""",
    ),
    q(
        18,
        "solution",
        9,
        "高等数学",
        ["幂级数", "和函数"],
        "26",
        r"""
求幂级数
$$
\sum_{n=1}^{\infty}\left(\frac{1}{2n+1}-1\right)x^{2n}
$$
在区间 $(-1,1)$ 内的和函数 $S(x)$。
""",
        r"""
$$
S(x)=
\begin{cases}
\dfrac{1}{2x}\ln\dfrac{1+x}{1-x}-\dfrac{1}{1-x^2}, & |x|<1,\ x\ne 0,\\[6pt]
0, & x=0.
\end{cases}
$$
""",
        r"""
设
$$
S(x)=\sum_{n=1}^{\infty}\left(\frac{1}{2n+1}-1\right)x^{2n}
=S_1(x)-S_2(x),
$$
其中
$$
S_1(x)=\sum_{n=1}^{\infty}\frac{x^{2n}}{2n+1},\qquad
S_2(x)=\sum_{n=1}^{\infty}x^{2n}=\frac{x^2}{1-x^2}.
$$
对 $xS_1(x)$ 求导，
$$
(xS_1(x))'=\sum_{n=1}^{\infty}x^{2n}=\frac{x^2}{1-x^2}.
$$
积分并利用 $S_1(0)=0$，得
$$
S_1(x)=
\begin{cases}
-1+\dfrac{1}{2x}\ln\dfrac{1+x}{1-x}, & x\ne 0,\\[6pt]
0, & x=0.
\end{cases}
$$
于是
$$
S(x)=
\begin{cases}
\dfrac{1}{2x}\ln\dfrac{1+x}{1-x}-\dfrac{1}{1-x^2}, & |x|<1,\ x\ne 0,\\[6pt]
0, & x=0.
\end{cases}
$$
""",
    ),
    q(
        19,
        "solution",
        8,
        "高等数学",
        ["积分不等式", "分部积分"],
        "26",
        r"""
设 $f(x),g(x)$ 在 $[0,1]$ 上的导数连续，且 $f(0)=0,\ f'(x)\ge 0,\ g'(x)\ge 0$。证明：对任何 $a\in[0,1]$，有
$$
\int_0^a g(x)f'(x)\,dx+\int_0^1 f(x)g'(x)\,dx\ge f(a)g(1).
$$
""",
        "命题成立",
        r"""
设
$$
F(x)=\int_0^x g(t)f'(t)\,dt+\int_0^1 f(t)g'(t)\,dt-f(x)g(1).
$$
则
$$
F'(x)=g(x)f'(x)-f'(x)g(1)=f'(x)\,[g(x)-g(1)]\le 0,
$$
因为 $f'(x)\ge 0$，且 $g(x)\le g(1)$。故 $F(x)$ 在 $[0,1]$ 上单调递减。  
另一方面，
$$
F(1)=\int_0^1 g(t)f'(t)\,dt+\int_0^1 f(t)g'(t)\,dt-f(1)g(1)=0
$$
（由分部积分可得）。于是对任意 $a\in[0,1]$，
$$
F(a)\ge F(1)=0,
$$
即
$$
\int_0^a g(x)f'(x)\,dx+\int_0^1 f(x)g'(x)\,dx\ge f(a)g(1).
$$
""",
    ),
    q(
        20,
        "solution",
        13,
        "线性代数",
        ["齐次线性方程组", "同解"],
        "26-27",
        r"""
已知齐次线性方程组
$$
\text{(i)}
\begin{cases}
x_1+2x_2+3x_3=0,\\
2x_1+3x_2+5x_3=0,\\
x_1+x_2+ax_3=0,
\end{cases}
$$
和
$$
\text{(ii)}
\begin{cases}
x_1+bx_2+cx_3=0,\\
2x_1+b^2x_2+(c+1)x_3=0
\end{cases}
$$
同解，求 $a,b,c$ 的值。
""",
        r"$(a,b,c)=(2,1,2)$",
        r"""
方程组 (ii) 只有两行，显然有无穷多解，因此方程组 (i) 也应有无穷多解，其系数矩阵秩小于 $3$。  
对 (i) 的系数矩阵作初等变换，可得第三行变为
$$
(0,0,a-2),
$$
故
$$
a=2.
$$
此时 (i) 的基础解系可取为
$$
(-1,-1,1)^T.
$$
将其代入 (ii) 得
$$
b=1,\ c=2
$$
或 $b=0,\ c=1$。再检验与 (i) 是否同解，只有
$$
(b,c)=(1,2)
$$
成立。  
故
$$
(a,b,c)=(2,1,2).
$$
""",
    ),
    q(
        21,
        "solution",
        13,
        "线性代数",
        ["正定矩阵", "分块矩阵"],
        "27",
        r"""
设
$$
D=
\begin{pmatrix}
A & C\\
C^T & B
\end{pmatrix}
$$
为正定矩阵，其中 $A,B$ 分别为 $m$ 阶、$n$ 阶对称矩阵，$C$ 为 $m\times n$ 矩阵。

1. 计算 $P^TDP$，其中
$$
P=
\begin{pmatrix}
E_m & -A^{-1}C\\
O & E_n
\end{pmatrix}.
$$
2. 利用 1 的结果判断矩阵 $B-C^TA^{-1}C$ 是否为正定矩阵，并证明你的结论。
""",
        r"""
$$
P^TDP=
\begin{pmatrix}
A & 0\\
0 & B-C^TA^{-1}C
\end{pmatrix},
\qquad
B-C^TA^{-1}C\ \text{为正定矩阵}.
$$
""",
        r"""
先算
$$
P^T=
\begin{pmatrix}
E_m & O\\
-C^TA^{-1} & E_n
\end{pmatrix}.
$$
直接做分块矩阵乘法得
$$
P^TDP=
\begin{pmatrix}
A & 0\\
0 & B-C^TA^{-1}C
\end{pmatrix}.
$$
由于 $D$ 正定，且 $P$ 可逆，故 $P^TDP$ 与 $D$ 合同，因此也正定。  
而 $P^TDP$ 是分块对角矩阵，所以对任意非零 $Y\in\mathbb R^n$，
$$
\begin{pmatrix}0\\Y\end{pmatrix}^T
\begin{pmatrix}
A & 0\\
0 & B-C^TA^{-1}C
\end{pmatrix}
\begin{pmatrix}0\\Y\end{pmatrix}
=Y^T(B-C^TA^{-1}C)Y>0.
$$
故
$$
B-C^TA^{-1}C
$$
是正定矩阵。
""",
    ),
    q(
        22,
        "solution",
        13,
        "概率统计",
        ["连续型二维分布", "边缘密度", "条件概率"],
        "27",
        r"""
设二维随机变量 $(X,Y)$ 的概率密度为
$$
f(x,y)=
\begin{cases}
1, & 0<x<1,\ 0<y<2x,\\
0, & \text{其他}.
\end{cases}
$$
求：

1. $(X,Y)$ 的边缘概率密度 $f_X(x),f_Y(y)$；
2. $Z=2X-Y$ 的概率密度 $f_Z(z)$；
3. $P\left\{Y\le \dfrac12\mid X\le \dfrac12\right\}$。
""",
        r"""
$$
f_X(x)=
\begin{cases}
2x, & 0<x<1,\\
0, & \text{其他},
\end{cases}
\qquad
f_Y(y)=
\begin{cases}
1-\dfrac y2, & 0<y<2,\\
0, & \text{其他},
\end{cases}
$$
$$
f_Z(z)=
\begin{cases}
1-\dfrac z2, & 0<z<2,\\
0, & \text{其他},
\end{cases}
\qquad
P\left\{Y\le \dfrac12\mid X\le \dfrac12\right\}=\frac34.
$$
""",
        r"""
由定义，
$$
f_X(x)=\int_{-\infty}^{+\infty}f(x,y)\,dy=
\begin{cases}
\int_0^{2x}1\,dy=2x, & 0<x<1,\\
0, & \text{其他},
\end{cases}
$$
$$
f_Y(y)=\int_{-\infty}^{+\infty}f(x,y)\,dx=
\begin{cases}
\int_{y/2}^{1}1\,dx=1-\dfrac y2, & 0<y<2,\\
0, & \text{其他}.
\end{cases}
$$
令 $F_Z(z)=P(Z\le z)=P(2X-Y\le z)$。分段计算可得
$$
F_Z(z)=
\begin{cases}
0, & z<0,\\
z-\dfrac14 z^2, & 0\le z<2,\\
1, & z\ge 2.
\end{cases}
$$
故
$$
f_Z(z)=F_Z'(z)=
\begin{cases}
1-\dfrac z2, & 0<z<2,\\
0, & \text{其他}.
\end{cases}
$$
最后，
$$
P\left\{Y\le \frac12\mid X\le \frac12\right\}
=\frac{P\left\{X\le \frac12,\ Y\le \frac12\right\}}{P\left\{X\le \frac12\right\}}
=\frac{3/16}{1/4}
=\frac34.
$$
""",
    ),
    q(
        23,
        "solution",
        13,
        "概率统计",
        ["抽样分布", "方差", "协方差", "无偏估计"],
        "27",
        r"""
设 $X_1,X_2,\cdots,X_n\ (n>2)$ 为来自总体 $N(0,\sigma^2)$ 的简单随机样本，其样本均值为 $\overline X$。记
$$
Y_i=X_i-\overline X,\qquad i=1,2,\cdots,n.
$$
求：

1. $Y_i$ 的方差 $D(Y_i),\ i=1,2,\cdots,n$；
2. $Y_1$ 与 $Y_n$ 的协方差 $\operatorname{Cov}(Y_1,Y_n)$；
3. 若 $c(Y_1+Y_n)^2$ 是 $\sigma^2$ 的无偏估计量，求常数 $c$。
""",
        r"""
$$
D(Y_i)=\frac{n-1}{n}\sigma^2,\qquad
\operatorname{Cov}(Y_1,Y_n)=-\frac1n\sigma^2,\qquad
c=\frac{n}{2(n-2)}.
$$
""",
        r"""
由 $E(X_i)=0,\ D(X_i)=\sigma^2$，且样本独立，知
$$
Y_i=X_i-\overline X.
$$
于是
$$
D(Y_i)=D(X_i-\overline X)=\frac{n-1}{n}\sigma^2.
$$
再由协方差定义展开，
$$
\operatorname{Cov}(Y_1,Y_n)
=E[(X_1-\overline X)(X_n-\overline X)]
=-\frac1n\sigma^2.
$$
最后
$$
E[c(Y_1+Y_n)^2]=c\,D(Y_1+Y_n)
=c\,[D(Y_1)+D(Y_n)+2\operatorname{Cov}(Y_1,Y_n)].
$$
代入前两问结果得
$$
E[c(Y_1+Y_n)^2]
=c\cdot \frac{2(n-2)}{n}\sigma^2.
$$
令其等于 $\sigma^2$，解得
$$
c=\frac{n}{2(n-2)}.
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
        "整理状态：按题面页图人工清洗并转写为正式题卡格式",
        "",
    ]
    for qn in questions:
        lines.extend(
            [
                f"### 第{qn.number}题",
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
        "整理状态：按答案页图人工清洗并整理为正式题卡格式",
        "",
    ]
    grouped = {
        "fill_blank": [qn for qn in questions if qn.question_type == "fill_blank"],
        "single_choice": [qn for qn in questions if qn.question_type == "single_choice"],
        "solution": [qn for qn in questions if qn.question_type == "solution"],
    }
    section_names = {
        "fill_blank": "填空题",
        "single_choice": "选择题",
        "solution": "解答题",
    }
    for key in ("fill_blank", "single_choice", "solution"):
        lines.extend(
            [
                "",
                f"## {section_names[key]}",
                "",
                "| 题号 | 答案 |",
                "|---|---|",
            ]
        )
        for qn in grouped[key]:
            lines.append(f"| {qn.number} | {answer_for_table(qn.answer)} |")
    lines.extend(["", "## 详细解析", ""])
    for qn in questions:
        lines.extend(
            [
                f"### 第{qn.number}题",
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
    (YEAR_DIR / "paper_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    YEAR_DIR.mkdir(parents=True, exist_ok=True)
    (YEAR_DIR / f"math3_{YEAR}_questions.md").write_text(annual_questions_md(QUESTIONS), encoding="utf-8")
    (YEAR_DIR / f"math3_{YEAR}_answers.md").write_text(annual_answers_md(QUESTIONS), encoding="utf-8")
    build_cards(QUESTIONS)
    print(json.dumps({"year": YEAR, "question_count": len(QUESTIONS), "generated_at": now_iso()}, ensure_ascii=False))


if __name__ == "__main__":
    main()
