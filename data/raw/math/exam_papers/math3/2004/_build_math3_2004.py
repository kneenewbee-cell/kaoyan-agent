from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[6]
EXAM_ROOT = ROOT / "data" / "raw" / "math" / "exam_papers"
YEAR = 2004
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
        ["极限", "等价无穷小", "参数求解"],
        "22",
        r"""
若极限
$$
\lim_{x\to0}\frac{\sin x}{e^x-a}(\cos x-b)=5,
$$
则 $a=\underline{\qquad},\ b=\underline{\qquad}$.
""",
        r"$a=1,\ b=-4$",
        r"""
若极限存在且非零，则分母必须满足
$$
e^x-a\to0 \quad (x\to0),
$$
故 $1-a=0$，即 $a=1$.

于是原极限化为
$$
\lim_{x\to0}\frac{\sin x}{e^x-1}(\cos x-b)
=\lim_{x\to0}\frac{\sin x}{x}\cdot\frac{x}{e^x-1}\cdot(\cos x-b)
=1\cdot1\cdot(1-b).
$$
由题意得 $1-b=5$，所以 $b=-4$.
""",
    ),
    q(
        2,
        "fill_blank",
        4,
        "高等数学",
        ["多元函数", "偏导数", "复合关系"],
        "22",
        r"""
函数 $f(u,v)$ 由关系式
$$
f[xg(y),y]=x+g(y)
$$
确定，其中函数 $g(y)$ 可微，且 $g(y)\ne0$，则
$$
\frac{\partial^2 f}{\partial u\partial v}=\underline{\qquad}.
$$
""",
        r"$-\dfrac{g'(v)}{g(v)^2}$",
        r"""
令
$$
u=xg(y),\qquad v=y,
$$
则
$$
x=\frac{u}{g(v)},
$$
从而
$$
f(u,v)=\frac{u}{g(v)}+g(v).
$$
先对 $u$ 求偏导：
$$
f_u(u,v)=\frac1{g(v)}.
$$
再对 $v$ 求偏导：
$$
f_{uv}(u,v)=\frac{\partial}{\partial v}\!\left(\frac1{g(v)}\right)
=-\frac{g'(v)}{g(v)^2}.
$$
""",
    ),
    q(
        3,
        "fill_blank",
        4,
        "高等数学",
        ["定积分", "分段函数", "换元"],
        "22",
        r"""
设
$$
f(x)=
\begin{cases}
xe^{x^2}, & -\dfrac12\le x<\dfrac12,\\[4pt]
-1, & x\ge \dfrac12,
\end{cases}
$$
则
$$
\int_{1/2}^{2} f(x-1)\,dx=\underline{\qquad}.
$$
""",
        r"$-\dfrac12$",
        r"""
令 $t=x-1$，则
$$
\int_{1/2}^{2} f(x-1)\,dx
=\int_{-1/2}^{1} f(t)\,dt
=\int_{-1/2}^{1/2} te^{t^2}\,dt+\int_{1/2}^{1}(-1)\,dt.
$$
其中 $te^{t^2}$ 为奇函数，所以
$$
\int_{-1/2}^{1/2} te^{t^2}\,dt=0.
$$
故原式为
$$
0-\left(1-\frac12\right)=-\frac12.
$$
""",
    ),
    q(
        4,
        "fill_blank",
        4,
        "线性代数",
        ["二次型", "矩阵秩"],
        "22",
        r"""
二次型
$$
f(x_1,x_2,x_3)=(x_1+x_2)^2+(x_2-x_3)^2+(x_3+x_1)^2
$$
的秩为 $\underline{\qquad}$.
""",
        r"$2$",
        r"""
展开得
$$
f=2x_1^2+2x_2^2+2x_3^2+2x_1x_2-2x_2x_3+2x_1x_3.
$$
对应矩阵为
$$
A=
\begin{pmatrix}
2 & 1 & 1\\
1 & 2 & -1\\
1 & -1 & 2
\end{pmatrix}.
$$
计算行列式可得
$$
|A|=0,
$$
但其二阶主子式
$$
\begin{vmatrix}
2 & 1\\
1 & 2
\end{vmatrix}=3\ne0.
$$
因此 $r(A)=2$，故二次型的秩为 $2$.
""",
    ),
    q(
        5,
        "fill_blank",
        4,
        "概率统计",
        ["指数分布", "方差", "概率计算"],
        "22",
        r"""
设随机变量 $X$ 服从参数为 $\lambda$ 的指数分布，则
$$
P\{X>\sqrt{D(X)}\}=\underline{\qquad}.
$$
""",
        r"$e^{-1}$",
        r"""
指数分布 $X\sim \mathrm{Exp}(\lambda)$ 满足
$$
D(X)=\frac1{\lambda^2},
\qquad \sqrt{D(X)}=\frac1\lambda.
$$
又其尾概率为
$$
P(X>t)=e^{-\lambda t}\quad (t>0),
$$
故
$$
P\!\left(X>\sqrt{D(X)}\right)
=P\!\left(X>\frac1\lambda\right)
=e^{-\lambda\cdot(1/\lambda)}
=e^{-1}.
$$
""",
    ),
    q(
        6,
        "fill_blank",
        4,
        "概率统计",
        ["正态总体", "样本方差", "数学期望"],
        "22",
        r"""
设总体 $X$ 服从正态分布 $N(\mu_1,\sigma^2)$，总体 $Y$ 服从正态分布 $N(\mu_2,\sigma^2)$，$X_1,X_2,\ldots,X_{n_1}$ 和 $Y_1,Y_2,\ldots,Y_{n_2}$ 分别是来自总体 $X$ 和 $Y$ 的简单随机样本，则
$$
E\!\left[
\frac{\sum_{i=1}^{n_1}(X_i-\overline X)^2+\sum_{j=1}^{n_2}(Y_j-\overline Y)^2}{n_1+n_2-2}
\right]
=\underline{\qquad}.
$$
""",
        r"$\sigma^2$",
        r"""
对正态总体有
$$
E\!\left[\sum_{i=1}^{n_1}(X_i-\overline X)^2\right]=(n_1-1)\sigma^2,
$$
以及
$$
E\!\left[\sum_{j=1}^{n_2}(Y_j-\overline Y)^2\right]=(n_2-1)\sigma^2.
$$
两式相加得
$$
E\!\left[\sum_{i=1}^{n_1}(X_i-\overline X)^2+\sum_{j=1}^{n_2}(Y_j-\overline Y)^2\right]
=(n_1+n_2-2)\sigma^2.
$$
再除以 $n_1+n_2-2$ 即得
$$
\sigma^2.
$$
""",
    ),
    q(
        7,
        "single_choice",
        4,
        "高等数学",
        ["函数有界性", "极限"],
        "22",
        r"""
函数
$$
f(x)=\frac{|x|\sin(x-2)}{x(x-1)(x-2)^2}
$$
在下列哪个区间内有界（ ）  

A. $(-1,0)$  
B. $(0,1)$  
C. $(1,2)$  
D. $(2,3)$
""",
        r"A",
        r"""
函数在 $x=1,2$ 处分母为零，因此包含这些点邻域的区间一般会出现无界情形。

在区间 $(-1,0)$ 内，函数连续；并且当 $x\to0^-$ 时，
$$
\frac{|x|\sin(x-2)}{x(x-1)(x-2)^2}
=-\frac{\sin(x-2)}{(x-1)(x-2)^2}
$$
极限存在且有限，所以在 $(-1,0)$ 内有界。

而其余三个区间分别在端点 $1$ 或 $2$ 附近产生无界，因此选 A.
""",
    ),
    q(
        8,
        "single_choice",
        4,
        "高等数学",
        ["分段函数", "连续性", "无穷远极限"],
        "22",
        r"""
设 $f(x)$ 在 $(-\infty,+\infty)$ 内有定义，且
$$
\lim_{x\to\infty}f(x)=a,
$$
定义
$$
g(x)=
\begin{cases}
f\!\left(\dfrac1x\right), & x\ne0,\\[4pt]
0, & x=0.
\end{cases}
$$
则（ ）

A. $x=0$ 必是 $g(x)$ 的第一类间断点  
B. $x=0$ 必是 $g(x)$ 的第二类间断点  
C. $x=0$ 必是 $g(x)$ 的连续点  
D. $g(x)$ 在点 $x=0$ 处的连续性与 $a$ 的取值有关
""",
        r"D",
        r"""
当 $x\to0$ 时，$1/x\to\infty$，所以
$$
\lim_{x\to0}g(x)=\lim_{x\to0}f\!\left(\frac1x\right)=\lim_{t\to\infty}f(t)=a.
$$
而
$$
g(0)=0.
$$
因此：

- 若 $a=0$，则 $\lim_{x\to0}g(x)=g(0)$，函数在 $0$ 点连续；
- 若 $a\ne0$，则 $\lim_{x\to0}g(x)\ne g(0)$，函数在 $0$ 点不连续。

所以连续性与 $a$ 的取值有关，选 D.
""",
    ),
    q(
        9,
        "single_choice",
        4,
        "高等数学",
        ["极值", "拐点", "绝对值函数"],
        "22",
        r"""
设
$$
f(x)=|x(1-x)|,
$$
则（ ）

A. $x=0$ 是 $f(x)$ 的极值点，但 $(0,0)$ 不是曲线 $y=f(x)$ 的拐点  
B. $x=0$ 不是 $f(x)$ 的极值点，但 $(0,0)$ 是曲线 $y=f(x)$ 的拐点  
C. $x=0$ 是 $f(x)$ 的极值点，且 $(0,0)$ 是曲线 $y=f(x)$ 的拐点  
D. $x=0$ 不是 $f(x)$ 的极值点，$(0,0)$ 也不是曲线 $y=f(x)$ 的拐点
""",
        r"C",
        r"""
在 $x=0$ 附近，$f(0)=0$，而当 $x\ne0$ 且充分接近 $0$ 时，
$$
|x(1-x)|>0,
$$
因此 $x=0$ 是极小值点。

又当 $x<0$ 时，
$$
f(x)=-x(1-x),
$$
其二阶导数为 $2>0$；  
当 $0<x<1$ 时，
$$
f(x)=x(1-x),
$$
其二阶导数为 $-2<0$.

可见曲线在 $x=0$ 两侧凹凸性发生改变，所以 $(0,0)$ 是拐点。故选 C.
""",
    ),
    q(
        10,
        "single_choice",
        4,
        "高等数学",
        ["级数", "收敛性", "命题判断"],
        "22",
        r"""
设有以下命题：

1. 若 $\sum_{n=1}^\infty (u_{2n-1}+u_{2n})$ 收敛，则 $\sum_{n=1}^\infty u_n$ 收敛；
2. 若 $\sum_{n=1}^\infty u_n$ 收敛，则 $\sum_{n=1}^\infty u_{n+100}$ 收敛；
3. 若 $\displaystyle\lim_{n\to\infty}\frac{u_{n+1}}{u_n}>1$，则 $\sum_{n=1}^\infty u_n$ 发散；
4. 若 $\sum_{n=1}^\infty (u_n+v_n)$ 收敛，则 $\sum_{n=1}^\infty u_n,\ \sum_{n=1}^\infty v_n$ 都收敛。

则以上命题中正确的是（ ）

A. 1、2  
B. 2、3  
C. 3、4  
D. 1、4
""",
        r"B",
        r"""
命题 1 错：取 $u_n=(-1)^n$，则
$$
u_{2n-1}+u_{2n}=0,
$$
从而 $\sum (u_{2n-1}+u_{2n})$ 收敛，但 $\sum u_n$ 发散。

命题 2 对：去掉级数有限项不改变收敛性。

命题 3 对：若 $\displaystyle\lim_{n\to\infty}\frac{u_{n+1}}{u_n}>1$，则从某项起 $|u_{n+1}|>|u_n|$，故 $u_n$ 不趋于 $0$，级数必发散。

命题 4 错：取 $u_n=1,\ v_n=-1$，则 $\sum (u_n+v_n)=0$ 收敛，但 $\sum u_n,\sum v_n$ 都发散。

故正确的是 2、3，选 B.
""",
    ),
    q(
        11,
        "single_choice",
        4,
        "高等数学",
        ["导数", "介值定理", "命题判断"],
        "23",
        r"""
设 $f'(x)$ 在 $[a,b]$ 上连续，且 $f'(a)>0,\ f'(b)<0$，则下列结论中错误的是（ ）

A. 至少存在一点 $x_0\in(a,b)$，使得 $f(x_0)>f(a)$  
B. 至少存在一点 $x_0\in(a,b)$，使得 $f(x_0)>f(b)$  
C. 至少存在一点 $x_0\in(a,b)$，使得 $f'(x_0)=0$  
D. 至少存在一点 $x_0\in(a,b)$，使得 $f(x_0)=0$
""",
        r"D",
        r"""
由 $f'(x)$ 连续且
$$
f'(a)>0,\qquad f'(b)<0,
$$
根据介值定理，必存在 $x_0\in(a,b)$ 使
$$
f'(x_0)=0,
$$
故 C 正确。

又因为 $f'(a)>0$，所以在 $a$ 的右邻域内 $f$ 递增，从而能找到点使 $f(x)>f(a)$，故 A 正确；同理由 $f'(b)<0$ 可知在 $b$ 的左邻域内有点使 $f(x)>f(b)$，故 B 正确。

至于方程 $f(x)=0$ 是否在 $(a,b)$ 内有解，仅凭导数端点符号无法保证，因此错误项为 D.
""",
    ),
    q(
        12,
        "single_choice",
        4,
        "线性代数",
        ["矩阵等价", "秩", "行列式"],
        "23",
        r"""
设 $n$ 阶矩阵 $A$ 与 $B$ 等价，则必有（ ）

A. 当 $|A|=a\ (a\ne0)$ 时，$|B|=a$  
B. 当 $|A|=a\ (a\ne0)$ 时，$|B|=-a$  
C. 当 $|A|\ne0$ 时，$|B|=0$  
D. 当 $|A|=0$ 时，$|B|=0$
""",
        r"D",
        r"""
矩阵等价的充要条件是
$$
r(A)=r(B).
$$
若 $|A|=0$，则
$$
r(A)<n.
$$
于是 $r(B)<n$，从而
$$
|B|=0.
$$
因此 D 必然成立。

而等价变换并不保持行列式值本身，所以 A、B 不一定成立；C 更明显错误。故选 D.
""",
    ),
    q(
        13,
        "single_choice",
        4,
        "线性代数",
        ["伴随矩阵", "线性方程组", "基础解系"],
        "23",
        r"""
设 $n$ 阶矩阵 $A$ 的伴随矩阵 $A^*\ne0$，若 $\xi_1,\xi_2,\xi_3,\xi_4$ 是非齐次线性方程组 $Ax=b$ 的互不相等的解，则对应的齐次线性方程组 $Ax=0$ 的基础解系（ ）

A. 不存在  
B. 仅含一个非零解向量  
C. 含有两个线性无关的解向量  
D. 含有三个线性无关的解向量
""",
        r"B",
        r"""
由 $A^*\ne0$ 可知
$$
r(A)=n-1 \quad \text{或} \quad r(A)=n.
$$
又因为非齐次方程组 $Ax=b$ 有互不相等的多个解，所以其解不唯一，必有
$$
r(A)<n.
$$
因此只能是
$$
r(A)=n-1.
$$
于是对应齐次方程组 $Ax=0$ 的基础解系所含向量个数为
$$
n-r(A)=1.
$$
故基础解系仅含一个非零解向量，选 B.
""",
    ),
    q(
        14,
        "single_choice",
        4,
        "概率统计",
        ["标准正态分布", "分位数", "概率计算"],
        "23",
        r"""
设随机变量 $X$ 服从正态分布 $N(0,1)$，对给定的 $\alpha\ (0<\alpha<1)$，数 $u_\alpha$ 满足
$$
P\{X>u_\alpha\}=\alpha.
$$
若
$$
P\{|X|<x\}=\alpha,
$$
则 $x$ 等于（ ）

A. $u_{\alpha/2}$  
B. $u_{1-\alpha/2}$  
C. $u_{(1-\alpha)/2}$  
D. $u_{1-\alpha}$
""",
        r"C",
        r"""
由
$$
P(|X|<x)=\alpha
$$
得
$$
P(-x<X<x)=\alpha.
$$
利用标准正态分布关于原点对称，
$$
2\Phi(x)-1=\alpha,
$$
故
$$
\Phi(x)=\frac{1+\alpha}{2}=1-\frac{1-\alpha}{2}.
$$
而 $u_\beta$ 的定义是
$$
P(X>u_\beta)=\beta \iff \Phi(u_\beta)=1-\beta.
$$
因此
$$
x=u_{(1-\alpha)/2}.
$$
选 C.
""",
    ),
    q(
        15,
        "solution",
        8,
        "高等数学",
        ["极限", "泰勒展开", "等价无穷小"],
        "23",
        r"""
求极限
$$
\lim_{x\to0}\left(\frac1{\sin^2 x}-\frac{\cos^2 x}{x^2}\right).
$$
""",
        r"$\dfrac43$",
        r"""
利用展开式
$$
\sin x=x-\frac{x^3}{6}+o(x^3),
\qquad
\cos x=1-\frac{x^2}{2}+o(x^2).
$$
于是
$$
\sin^2x=x^2-\frac{x^4}{3}+o(x^4),
$$
从而
$$
\frac1{\sin^2x}
=\frac1{x^2}\cdot\frac1{1-\frac{x^2}{3}+o(x^2)}
=\frac1{x^2}+\frac13+o(1).
$$
另一方面，
$$
\frac{\cos^2x}{x^2}
=\frac{1-x^2+o(x^2)}{x^2}
=\frac1{x^2}-1+o(1).
$$
两式相减得
$$
\lim_{x\to0}\left(\frac1{\sin^2 x}-\frac{\cos^2 x}{x^2}\right)
=\frac13-(-1)=\frac43.
$$
""",
    ),
    q(
        16,
        "solution",
        8,
        "高等数学",
        ["二重积分", "极坐标", "对称性"],
        "23",
        r"""
求
$$
\iint_D\bigl(\sqrt{x^2+y^2}+y\bigr)\,d\sigma,
$$
其中 $D$ 是由圆 $x^2+y^2=4$ 和 $(x+1)^2+y^2=1$ 所围成的平面区域。
""",
        r"$\dfrac{16}{9}(3\pi-2)$",
        r"""
设
$$
D_1=\{(x,y)\mid x^2+y^2\le4\},\qquad
D_2=\{(x,y)\mid (x+1)^2+y^2\le1\},
$$
则题中区域为
$$
D=D_1\setminus D_2.
$$

由关于 $x$ 轴对称性，
$$
\iint_D y\,d\sigma=0.
$$
故原积分化为
$$
\iint_D \sqrt{x^2+y^2}\,d\sigma
=\iint_{D_1} r\,d\sigma-\iint_{D_2} r\,d\sigma.
$$

对 $D_1$ 用极坐标：
$$
\iint_{D_1} r\,d\sigma
=\int_0^{2\pi}\int_0^2 r^2\,dr\,d\theta
=\frac{16\pi}{3}.
$$

对 $D_2$，其边界满足
$$
(x+1)^2+y^2=1
\iff r^2+2r\cos\theta=0
\iff r=-2\cos\theta,
$$
故对应区域为 $\theta\in\left[\frac\pi2,\frac{3\pi}2\right]$，$0\le r\le -2\cos\theta$。于是
$$
\iint_{D_2} r\,d\sigma
=\int_{\pi/2}^{3\pi/2}\int_0^{-2\cos\theta} r^2\,dr\,d\theta
=\frac{32}{9}.
$$
因此
$$
\iint_D(\sqrt{x^2+y^2}+y)\,d\sigma
=\frac{16\pi}{3}-\frac{32}{9}
=\frac{16}{9}(3\pi-2).
$$
""",
    ),
    q(
        17,
        "solution",
        8,
        "高等数学",
        ["积分不等式", "变限积分", "分部积分"],
        "23",
        r"""
设 $f(x),g(x)$ 在 $[a,b]$ 上连续，且满足
$$
\int_a^x f(t)\,dt\ge\int_a^x g(t)\,dt,\qquad x\in[a,b),
$$
以及
$$
\int_a^b f(t)\,dt=\int_a^b g(t)\,dt.
$$
证明：
$$
\int_a^b xf(x)\,dx\le\int_a^b xg(x)\,dx.
$$
""",
        r"命题成立",
        r"""
令
$$
F(x)=f(x)-g(x),\qquad G(x)=\int_a^x F(t)\,dt.
$$
则由题设可知
$$
G(x)\ge0\quad (x\in[a,b]),
$$
并且
$$
G(a)=0,\qquad G(b)=\int_a^b(f-g)\,dt=0.
$$

现在考察
$$
\int_a^b xF(x)\,dx=\int_a^b xG'(x)\,dx.
$$
分部积分得
$$
\int_a^b xG'(x)\,dx
=\bigl[xG(x)\bigr]_a^b-\int_a^b G(x)\,dx
=-\int_a^b G(x)\,dx\le0.
$$
于是
$$
\int_a^b x(f(x)-g(x))\,dx\le0,
$$
即
$$
\int_a^b xf(x)\,dx\le\int_a^b xg(x)\,dx.
$$
命题得证。
""",
    ),
    q(
        18,
        "solution",
        9,
        "概率统计",
        ["经济应用", "弹性", "导数"],
        "23",
        r"""
设某商品的需求函数为
$$
Q=100-5P,\qquad P\in(0,20),
$$
其中 $Q$ 为需求量。

1. 求需求量对价格的弹性 $E_d\ (E_d>0)$；
2. 推导
$$
\frac{dR}{dP}=Q(1-E_d)
$$
（其中 $R$ 为收益），并用弹性 $E_d$ 说明价格在何范围内变化时，降低价格反而使收益增加。
""",
        r"$E_d=\dfrac{P}{20-P}$，且当 $10<P<20$ 时降低价格会使收益增加",
        r"""
由定义
$$
E_d=-\frac{P}{Q}\frac{dQ}{dP}.
$$
因为
$$
Q=100-5P,\qquad \frac{dQ}{dP}=-5,
$$
所以
$$
E_d=-\frac{P}{100-5P}\cdot(-5)=\frac{P}{20-P}.
$$

又收益
$$
R=PQ,
$$
故
$$
\frac{dR}{dP}=Q+P\frac{dQ}{dP}
=Q\left(1+\frac{P}{Q}\frac{dQ}{dP}\right)
=Q(1-E_d).
$$

若降低价格反而使收益增加，则当 $dP<0$ 时应有 $dR>0$，即
$$
\frac{dR}{dP}<0.
$$
由于 $Q>0$，故需
$$
1-E_d<0 \iff E_d>1.
$$
由
$$
\frac{P}{20-P}>1
$$
解得
$$
P>10.
$$
结合 $P\in(0,20)$，所以当
$$
10<P<20
$$
时，降低价格反而会使收益增加。
""",
    ),
    q(
        19,
        "solution",
        9,
        "高等数学",
        ["幂级数", "微分方程", "求和函数"],
        "24",
        r"""
设级数
$$
\frac{x^4}{2\times4}+\frac{x^6}{2\times4\times6}+\frac{x^8}{2\times4\times6\times8}+\cdots
\qquad (-\infty<x<+\infty)
$$
的和函数为 $S(x)$。求：

1. $S(x)$ 所满足的一阶微分方程；
2. $S(x)$ 的表达式。
""",
        r"$S'(x)=xS(x)+\dfrac{x^3}{2},\ S(0)=0$；$\quad S(x)=-\dfrac{x^2}{2}+e^{x^2/2}-1$",
        r"""
记
$$
S(x)=\frac{x^4}{2\cdot4}+\frac{x^6}{2\cdot4\cdot6}+\frac{x^8}{2\cdot4\cdot6\cdot8}+\cdots.
$$
显然
$$
S(0)=0.
$$

逐项求导得
$$
S'(x)=\frac{x^3}{2}+\frac{x^5}{2\cdot4}+\frac{x^7}{2\cdot4\cdot6}+\cdots
=x\left(\frac{x^2}{2}+S(x)\right).
$$
故 $S(x)$ 满足初值问题
$$
y'=xy+\frac{x^3}{2},\qquad y(0)=0.
$$

解线性微分方程
$$
y'-xy=\frac{x^3}{2}.
$$
取积分因子 $e^{-x^2/2}$，则
$$
\bigl(ye^{-x^2/2}\bigr)'=\frac{x^3}{2}e^{-x^2/2}.
$$
积分可得
$$
y=-\frac{x^2}{2}-1+Ce^{x^2/2}.
$$
由初值 $y(0)=0$，得 $C=1$。因此
$$
S(x)=-\frac{x^2}{2}+e^{x^2/2}-1.
$$
""",
    ),
    q(
        20,
        "solution",
        13,
        "线性代数",
        ["向量组", "线性表示", "方程组讨论"],
        "24",
        r"""
设
$$
\alpha_1=(1,2,0)^T,\quad
\alpha_2=(1,a+2,-3a)^T,\quad
\alpha_3=(-1,-b-2,a+2b)^T,\quad
\beta=(1,3,-3)^T,
$$
试讨论当 $a,b$ 为何值时：

1. $\beta$ 不能由 $\alpha_1,\alpha_2,\alpha_3$ 线性表示；
2. $\beta$ 可由 $\alpha_1,\alpha_2,\alpha_3$ 唯一地线性表示，并求出表示式；
3. $\beta$ 可由 $\alpha_1,\alpha_2,\alpha_3$ 线性表示，但表示式不唯一，并求出表示式。
""",
        r"""
(I) $a=0$；

(II) 当 $a\ne0$ 且 $a\ne b$ 时，
$$
\beta=\left(1-\frac1a\right)\alpha_1+\frac1a\alpha_2;
$$

(III) 当 $a=b\ne0$ 时，
$$
\beta=\left(1-\frac1a\right)\alpha_1+\left(\frac1a+c\right)\alpha_2+c\alpha_3,\quad c\in\mathbb R.
$$
""",
        r"""
设存在 $k_1,k_2,k_3$，使
$$
k_1\alpha_1+k_2\alpha_2+k_3\alpha_3=\beta.
$$
把它写成增广矩阵
$$
(\alpha_1,\alpha_2,\alpha_3,\beta)
=
\begin{pmatrix}
1 & 1 & -1 & 1\\
2 & a+2 & -b-2 & 3\\
0 & -3a & a+2b & -3
\end{pmatrix}.
$$
行变换可化为
$$
\begin{pmatrix}
1 & 1 & -1 & 1\\
0 & a & -b & 1\\
0 & 0 & a-b & 0
\end{pmatrix}.
$$

1. 当 $a=0$ 时，矩阵继续化简后有
$$
r(A)\ne r(A,\beta),
$$
故方程无解，$\beta$ 不能由 $\alpha_1,\alpha_2,\alpha_3$ 线性表示。

2. 当 $a\ne0$ 且 $a\ne b$ 时，
$$
r(A)=r(A,\beta)=3,
$$
故有唯一解。回代得
$$
k_1=1-\frac1a,\qquad k_2=\frac1a,\qquad k_3=0,
$$
所以
$$
\beta=\left(1-\frac1a\right)\alpha_1+\frac1a\alpha_2.
$$

3. 当 $a=b\ne0$ 时，
$$
r(A)=r(A,\beta)=2,
$$
故有无穷多解。令自由参数为 $c$，则
$$
k_1=1-\frac1a,\qquad
k_2=\frac1a+c,\qquad
k_3=c.
$$
因此
$$
\beta=\left(1-\frac1a\right)\alpha_1+\left(\frac1a+c\right)\alpha_2+c\alpha_3,\quad c\in\mathbb R.
$$
""",
    ),
    q(
        21,
        "solution",
        13,
        "线性代数",
        ["特征值", "特征向量", "矩阵对角化"],
        "24",
        r"""
设 $n$ 阶矩阵
$$
A=
\begin{pmatrix}
1 & b & \cdots & b\\
b & 1 & \cdots & b\\
\vdots & \vdots & \ddots & \vdots\\
b & b & \cdots & 1
\end{pmatrix}.
$$

1. 求 $A$ 的特征值和特征向量；
2. 求可逆矩阵 $P$，使得 $P^{-1}AP$ 为对角矩阵。
""",
        r"见详细解析",
        r"""
先讨论 $b\ne0$ 的情形。记
$$
\mathbf 1=(1,1,\ldots,1)^T.
$$
则
$$
A\mathbf 1=\bigl(1+(n-1)b\bigr)\mathbf 1,
$$
故
$$
\lambda_1=1+(n-1)b
$$
是一个特征值，其对应特征向量为任意非零倍数的 $\mathbf 1$。

再看满足各分量和为零的向量 $x$，即
$$
x_1+\cdots+x_n=0.
$$
对这类向量，
$$
Ax=(1-b)x,
$$
所以
$$
\lambda_2=\cdots=\lambda_n=1-b
$$
是重根为 $n-1$ 的特征值，其特征子空间可取一组基为
$$
\xi_2=(1,-1,0,\ldots,0)^T,\ 
\xi_3=(1,0,-1,\ldots,0)^T,\ 
\ldots,\ 
\xi_n=(1,0,\ldots,0,-1)^T.
$$

因此当 $b\ne0$ 时，可取
$$
\xi_1=(1,1,\ldots,1)^T,
$$
并令
$$
P=(\xi_1,\xi_2,\ldots,\xi_n),
$$
则
$$
P^{-1}AP=\operatorname{diag}\bigl(1+(n-1)b,\underbrace{1-b,\ldots,1-b}_{n-1\text{ 个}}\bigr).
$$

当 $b=0$ 时，$A=E$，故全部特征值都等于 $1$，任意非零向量都是特征向量，且对任意可逆矩阵 $P$ 都有
$$
P^{-1}AP=E.
$$
""",
    ),
    q(
        22,
        "solution",
        13,
        "概率统计",
        ["二维离散分布", "相关系数", "随机变量函数分布"],
        "24",
        r"""
设 $A,B$ 为两个随机事件，且
$$
P(A)=\frac14,\qquad P(B\mid A)=\frac13,\qquad P(A\mid B)=\frac12.
$$
令
$$
X=
\begin{cases}
1,& A\text{ 发生},\\
0,& A\text{ 不发生},
\end{cases}
\qquad
Y=
\begin{cases}
1,& B\text{ 发生},\\
0,& B\text{ 不发生}.
\end{cases}
$$
求：

1. 二维随机变量 $(X,Y)$ 的概率分布；
2. $X$ 与 $Y$ 的相关系数 $\rho_{XY}$；
3. $Z=X^2+Y^2$ 的概率分布。
""",
        r"""
$(X,Y)$ 的分布为
$$
P(0,0)=\frac23,\quad P(0,1)=\frac1{12},\quad P(1,0)=\frac16,\quad P(1,1)=\frac1{12};
$$

$$
\rho_{XY}=\frac{\sqrt{15}}{15};
$$

$$
P(Z=0)=\frac23,\quad P(Z=1)=\frac14,\quad P(Z=2)=\frac1{12}.
$$
""",
        r"""
先求
$$
P(AB)=P(A)P(B\mid A)=\frac14\cdot\frac13=\frac1{12}.
$$
又因为
$$
P(A\mid B)=\frac{P(AB)}{P(B)}=\frac12,
$$
故
$$
P(B)=\frac{P(AB)}{P(A\mid B)}=\frac{1/12}{1/2}=\frac16.
$$

于是
$$
P(X=1,Y=1)=P(AB)=\frac1{12},
$$
$$
P(X=1,Y=0)=P(A)-P(AB)=\frac14-\frac1{12}=\frac16,
$$
$$
P(X=0,Y=1)=P(B)-P(AB)=\frac16-\frac1{12}=\frac1{12},
$$
$$
P(X=0,Y=0)=1-\frac1{12}-\frac16-\frac1{12}=\frac23.
$$

再算相关系数。因为
$$
EX=P(A)=\frac14,\qquad EY=P(B)=\frac16,
$$
$$
E(XY)=P(AB)=\frac1{12},
$$
所以
$$
\operatorname{Cov}(X,Y)=E(XY)-EX\cdot EY
=\frac1{12}-\frac14\cdot\frac16
=\frac1{24}.
$$
又
$$
DX=\frac14\left(1-\frac14\right)=\frac3{16},\qquad
DY=\frac16\left(1-\frac16\right)=\frac5{36}.
$$
故
$$
\rho_{XY}
=\frac{\operatorname{Cov}(X,Y)}{\sqrt{DX\cdot DY}}
=\frac{1/24}{\sqrt{(3/16)(5/36)}}
=\frac{\sqrt{15}}{15}.
$$

最后，因 $X,Y$ 仅取 $0,1$，故
$$
Z=X^2+Y^2=X+Y.
$$
于是
$$
P(Z=0)=P(X=0,Y=0)=\frac23,
$$
$$
P(Z=1)=P(X=1,Y=0)+P(X=0,Y=1)=\frac16+\frac1{12}=\frac14,
$$
$$
P(Z=2)=P(X=1,Y=1)=\frac1{12}.
$$
""",
    ),
    q(
        23,
        "solution",
        13,
        "概率统计",
        ["参数估计", "矩估计", "最大似然估计"],
        "24",
        r"""
设随机变量 $X$ 的分布函数为
$$
F(x;\alpha,\beta)=
\begin{cases}
1-\left(\dfrac{\alpha}{x}\right)^\beta, & x>\alpha,\\[6pt]
0, & x\le \alpha,
\end{cases}
$$
其中参数 $\alpha>0,\ \beta>1$。设 $X_1,X_2,\ldots,X_n$ 为来自总体 $X$ 的简单随机样本。

1. 当 $\alpha=1$ 时，求未知参数 $\beta$ 的矩估计量；
2. 当 $\alpha=1$ 时，求未知参数 $\beta$ 的最大似然估计量；
3. 当 $\beta=2$ 时，求未知参数 $\alpha$ 的最大似然估计量。
""",
        r"""
当 $\alpha=1$ 时，
$$
\hat\beta_{\text{矩}}=\frac{\overline X}{\overline X-1},\qquad
\hat\beta_{\text{MLE}}=\frac{n}{\sum_{i=1}^n\ln X_i};
$$

当 $\beta=2$ 时，
$$
\hat\alpha_{\text{MLE}}=\min\{X_1,X_2,\ldots,X_n\}.
$$
""",
        r"""
先由分布函数求密度函数。

当 $\alpha=1$ 时，
$$
F(x;1,\beta)=
\begin{cases}
1-x^{-\beta}, & x>1,\\
0, & x\le1,
\end{cases}
$$
故密度为
$$
f(x;\beta)=
\begin{cases}
\dfrac{\beta}{x^{\beta+1}}, & x>1,\\[4pt]
0, & x\le1.
\end{cases}
$$

1. 矩估计：
$$
EX=\int_1^\infty x\cdot \frac{\beta}{x^{\beta+1}}\,dx=\frac{\beta}{\beta-1}.
$$
令
$$
\overline X=\frac{\beta}{\beta-1},
$$
解得
$$
\hat\beta_{\text{矩}}=\frac{\overline X}{\overline X-1}.
$$

2. 最大似然估计：
样本似然函数为
$$
L(\beta)=\prod_{i=1}^n\frac{\beta}{x_i^{\beta+1}}
=\beta^n\prod_{i=1}^n x_i^{-(\beta+1)}\qquad (x_i>1).
$$
取对数得
$$
\ln L(\beta)=n\ln\beta-(\beta+1)\sum_{i=1}^n\ln x_i.
$$
求导并令其为零：
$$
\frac{d}{d\beta}\ln L(\beta)=\frac{n}{\beta}-\sum_{i=1}^n\ln x_i=0.
$$
故
$$
\hat\beta_{\text{MLE}}=\frac{n}{\sum_{i=1}^n\ln X_i}.
$$

3. 当 $\beta=2$ 时，
$$
f(x;\alpha)=
\begin{cases}
\dfrac{2\alpha^2}{x^3}, & x>\alpha,\\[4pt]
0, & x\le\alpha.
\end{cases}
$$
于是
$$
L(\alpha)=\prod_{i=1}^n \frac{2\alpha^2}{x_i^3},
$$
其成立条件是 $\alpha< x_i$ 对所有 $i$ 都成立，即
$$
\alpha\le \min\{x_1,\ldots,x_n\}.
$$
在该条件下，$L(\alpha)$ 随 $\alpha$ 增大而增大，所以最大似然估计取可行域最大值：
$$
\hat\alpha_{\text{MLE}}=\min\{X_1,X_2,\ldots,X_n\}.
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
