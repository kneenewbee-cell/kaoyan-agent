from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[6]
EXAM_ROOT = ROOT / "data" / "raw" / "math" / "exam_papers"
YEAR = 2010
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
        "single_choice",
        4,
        "高等数学",
        ["极限", "等价无穷小", "指数函数"],
        "38",
        r"""
若
$$
\lim_{x\to0}\left[\frac1x-\left(\frac1x-a\right)e^x\right]=1,
$$
则 $a$ 等于（ ）

A. $0$  
B. $1$  
C. $2$  
D. $3$
""",
        r"C",
        r"""
将极限式整理为
$$
\frac1x-\left(\frac1x-a\right)e^x
=\frac{1-e^x}{x}+ae^x.
$$
当 $x\to0$ 时，
$$
\frac{1-e^x}{x}\to-1,\qquad ae^x\to a.
$$
所以原极限为
$$
-1+a=1,
$$
解得 $a=2$。故选 C。
""",
    ),
    q(
        2,
        "single_choice",
        4,
        "高等数学",
        ["一阶线性微分方程", "特解与齐次解"],
        "38",
        r"""
设 $y_1,y_2$ 是一阶线性非齐次微分方程
$$
y'+p(x)y=q(x)
$$
的两个特解，若常数 $\lambda,\mu$ 使 $\lambda y_1+\mu y_2$ 是该方程的解，$\lambda y_1-\mu y_2$ 是该方程对应的齐次方程的解，则（ ）

A. $\lambda=\dfrac12,\ \mu=\dfrac12$  
B. $\lambda=-\dfrac12,\ \mu=-\dfrac12$  
C. $\lambda=\dfrac23,\ \mu=\dfrac13$  
D. $\lambda=\dfrac23,\ \mu=\dfrac23$
""",
        r"A",
        r"""
因为 $\lambda y_1-\mu y_2$ 是齐次方程
$$
y'+p(x)y=0
$$
的解，所以
$$
\lambda\bigl[y_1'+p(x)y_1\bigr]-\mu\bigl[y_2'+p(x)y_2\bigr]=0.
$$
而 $y_1,y_2$ 都满足非齐次方程，因此
$$
(\lambda-\mu)q(x)=0.
$$
由题意知方程非齐次，故 $q(x)\ne0$，从而 $\lambda=\mu$。

又因为 $\lambda y_1+\mu y_2$ 也是原方程的解，所以
$$
\lambda\bigl[y_1'+p(x)y_1\bigr]+\mu\bigl[y_2'+p(x)y_2\bigr]=q(x),
$$
即
$$
(\lambda+\mu)q(x)=q(x).
$$
故 $\lambda+\mu=1$。联立得
$$
\lambda=\mu=\frac12.
$$
选 A。
""",
    ),
    q(
        3,
        "single_choice",
        4,
        "高等数学",
        ["复合函数极值", "二阶导数"],
        "38",
        r"""
设函数 $f(x),g(x)$ 具有二阶导数，且 $g''(x)<0$。若 $g(x_0)=a$ 是 $g(x)$ 的极值，则 $f(g(x))$ 在 $x_0$ 处取极大值的一个充分条件是（ ）

A. $f'(a)<0$  
B. $f'(a)>0$  
C. $f''(a)<0$  
D. $f''(a)>0$
""",
        r"B",
        r"""
由复合函数求导，
$$
\{f[g(x)]\}'=f'[g(x)]g'(x),
$$
$$
\{f[g(x)]\}''=f''[g(x)](g'(x))^2+f'[g(x)]g''(x).
$$
由于 $g(x_0)=a$ 是极值点，所以 $g'(x_0)=0$，从而
$$
\{f[g(x_0)]\}''=f'(a)g''(x_0).
$$
又已知 $g''(x_0)<0$，若要使 $f(g(x))$ 在 $x_0$ 处取极大值，只需
$$
\{f[g(x_0)]\}''<0,
$$
因此只需 $f'(a)>0$。选 B。
""",
    ),
    q(
        4,
        "single_choice",
        4,
        "高等数学",
        ["无穷大比较", "洛必达法则"],
        "38",
        r"""
设
$$
f(x)=\ln^{10}x,\quad g(x)=x,\quad h(x)=e^{x/10},
$$
则当 $x$ 充分大时有（ ）

A. $g(x)<h(x)<f(x)$  
B. $h(x)<g(x)<f(x)$  
C. $f(x)<g(x)<h(x)$  
D. $g(x)<f(x)<h(x)$
""",
        r"C",
        r"""
有
$$
\lim_{x\to+\infty}\frac{h(x)}{g(x)}
=\lim_{x\to+\infty}\frac{e^{x/10}}{x}=+\infty,
$$
所以充分大时 $h(x)>g(x)$。

又
$$
\lim_{x\to+\infty}\frac{f(x)}{g(x)}
=\lim_{x\to+\infty}\frac{\ln^{10}x}{x}=0,
$$
因此充分大时 $f(x)<g(x)$。

综上，充分大时
$$
f(x)<g(x)<h(x).
$$
选 C。
""",
    ),
    q(
        5,
        "single_choice",
        4,
        "线性代数",
        ["向量组", "秩", "线性表示"],
        "38",
        r"""
设向量组 I：$\alpha_1,\alpha_2,\cdots,\alpha_r$ 可由向量组 II：$\beta_1,\beta_2,\cdots,\beta_s$ 线性表示。下列命题正确的是（ ）

A. 若向量组 I 线性无关，则 $r\le s$  
B. 若向量组 I 线性相关，则 $r>s$  
C. 若向量组 II 线性无关，则 $r\le s$  
D. 若向量组 II 线性相关，则 $r>s$
""",
        r"A",
        r"""
因为向量组 I 可由向量组 II 线性表示，所以
$$
r(\alpha_1,\cdots,\alpha_r)\le r(\beta_1,\cdots,\beta_s)\le s.
$$
若向量组 I 线性无关，则
$$
r(\alpha_1,\cdots,\alpha_r)=r,
$$
于是
$$
r\le s.
$$
故 A 正确。
""",
    ),
    q(
        6,
        "single_choice",
        4,
        "线性代数",
        ["矩阵相似", "实对称矩阵", "特征值"],
        "38",
        r"""
设 $A$ 为 4 阶实对称矩阵，且
$$
A^2+A=O.
$$
若 $A$ 的秩为 3，则 $A$ 相似于（ ）

A. $\operatorname{diag}(1,1,1,0)$  
B. $\operatorname{diag}(1,1,-1,0)$  
C. $\operatorname{diag}(1,-1,-1,0)$  
D. $\operatorname{diag}(-1,-1,-1,0)$
""",
        r"D",
        r"""
设 $\lambda$ 是 $A$ 的特征值，则由
$$
A^2+A=O
$$
可得
$$
\lambda^2+\lambda=0,
$$
即
$$
\lambda(\lambda+1)=0.
$$
所以特征值只能是 $0$ 或 $-1$。

又 $A$ 为实对称矩阵，必可对角化；且 $r(A)=3$，说明恰有 3 个非零特征值，因此这 3 个非零特征值都只能是 $-1$，另一个是 0。
故 $A$ 相似于
$$
\operatorname{diag}(-1,-1,-1,0).
$$
选 D。
""",
    ),
    q(
        7,
        "single_choice",
        4,
        "概率统计",
        ["分布函数", "点概率"],
        "39",
        r"""
设随机变量 $X$ 的分布函数
$$
F(x)=
\begin{cases}
0, & x<0,\\[4pt]
\dfrac12, & 0\le x<1,\\[4pt]
1-e^{-x}, & x\ge1,
\end{cases}
$$
则 $P\{X=1\}=(\ )$

A. $0$  
B. $\dfrac12$  
C. $\dfrac12-e^{-1}$  
D. $1-e^{-1}$
""",
        r"C",
        r"""
由分布函数的定义，
$$
P\{X=1\}=F(1)-F(1-0).
$$
其中
$$
F(1)=1-e^{-1},\qquad F(1-0)=\frac12.
$$
所以
$$
P\{X=1\}=1-e^{-1}-\frac12=\frac12-e^{-1}.
$$
选 C。
""",
    ),
    q(
        8,
        "single_choice",
        4,
        "概率统计",
        ["概率密度", "标准正态分布", "均匀分布"],
        "39",
        r"""
设 $f_1(x)$ 为标准正态分布的概率密度，$f_2(x)$ 为 $[-1,3]$ 上均匀分布的概率密度，若
$$
f(x)=
\begin{cases}
af_1(x), & x\le0,\\
bf_2(x), & x>0,
\end{cases}
\qquad (a>0,b>0)
$$
为概率密度，则 $a,b$ 应满足（ ）

A. $2a+3b=4$  
B. $3a+2b=4$  
C. $a+b=1$  
D. $a+b=2$
""",
        r"A",
        r"""
由概率密度积分为 1，
$$
\int_{-\infty}^{+\infty}f(x)\,dx
=a\int_{-\infty}^{0}f_1(x)\,dx+b\int_0^{+\infty}f_2(x)\,dx=1.
$$
标准正态分布关于 0 对称，所以
$$
\int_{-\infty}^{0}f_1(x)\,dx=\frac12.
$$
而 $f_2(x)=\dfrac14$ 在 $[-1,3]$ 上，故
$$
\int_0^{+\infty}f_2(x)\,dx=\int_0^3\frac14\,dx=\frac34.
$$
因此
$$
\frac a2+\frac{3b}{4}=1
\iff 2a+3b=4.
$$
选 A。
""",
    ),
    q(
        9,
        "fill_blank",
        4,
        "高等数学",
        ["可导方程", "隐函数求导"],
        "39",
        r"""
设可导函数 $y=y(x)$ 由方程
$$
\int_0^{x+y}e^{-t^2}\,dt=\int_0^x x\sin t^2\,dt
$$
确定，则
$$
\left.\frac{dy}{dx}\right|_{x=0}=\underline{\qquad}.
$$
""",
        r"$-1$",
        r"""
先令 $x=0$，得
$$
\int_0^y e^{-t^2}\,dt=0,
$$
故 $y(0)=0$。

对原方程两边关于 $x$ 求导：
$$
e^{-(x+y)^2}\left(1+\frac{dy}{dx}\right)
=\int_0^x \sin t^2\,dt+x\sin x^2.
$$
代入 $x=0,\ y=0$，得到
$$
1+\left.\frac{dy}{dx}\right|_{x=0}=0,
$$
所以
$$
\left.\frac{dy}{dx}\right|_{x=0}=-1.
$$
""",
    ),
    q(
        10,
        "fill_blank",
        4,
        "高等数学",
        ["旋转体体积", "反常积分"],
        "39",
        r"""
设位于曲线
$$
y=\frac1{\sqrt{x(1+\ln^2x)}}\quad (e\le x<+\infty)
$$
下方、$x$ 轴上方的无界区域为 $G$，则 $G$ 绕 $x$ 轴旋转一周所得空间区域的体积为 $\underline{\qquad}$.
""",
        r"$\dfrac{\pi^2}{4}$",
        r"""
绕 $x$ 轴旋转的体积为
$$
V=\pi\int_e^{+\infty}y^2\,dx
=\pi\int_e^{+\infty}\frac{dx}{x(1+\ln^2x)}.
$$
令 $u=\ln x$，则 $du=\dfrac{dx}{x}$，于是
$$
V=\pi\int_1^{+\infty}\frac{du}{1+u^2}
=\pi\left[\arctan u\right]_1^{+\infty}
=\pi\left(\frac\pi2-\frac\pi4\right)
=\frac{\pi^2}{4}.
$$
""",
    ),
    q(
        11,
        "fill_blank",
        4,
        "概率统计",
        ["收益弹性", "微分方程"],
        "39",
        r"""
设某商品的收益函数为 $R(p)$，收益弹性为 $1+p^3$，其中 $p$ 为价格，且 $R(1)=1$，则 $R(p)=\underline{\qquad}$.
""",
        r"$p\cdot e^{(p^3-1)/3}$",
        r"""
由收益弹性的定义，
$$
\frac{dR}{dp}\cdot\frac{p}{R}=1+p^3.
$$
于是
$$
\frac{dR}{R}=\left(\frac1p+p^2\right)\,dp.
$$
积分得
$$
\ln R=\ln p+\frac13p^3+C.
$$
利用条件 $R(1)=1$，得
$$
0=\frac13+C,
$$
所以 $C=-\dfrac13$。
因此
$$
R(p)=p\cdot e^{(p^3-1)/3}.
$$
""",
    ),
    q(
        12,
        "fill_blank",
        4,
        "高等数学",
        ["拐点", "导数应用"],
        "39",
        r"""
若曲线
$$
y=x^3+ax^2+bx+1
$$
有拐点 $(-1,0)$，则 $b=\underline{\qquad}$.
""",
        r"$3$",
        r"""
有
$$
y'=3x^2+2ax+b,\qquad y''=6x+2a.
$$
由于 $(-1,0)$ 是拐点，故
$$
y''(-1)=0,
$$
从而
$$
-6+2a=0\Rightarrow a=3.
$$
又因为点 $(-1,0)$ 在曲线上，
$$
0=(-1)^3+3(-1)^2-b+1=3-b,
$$
所以
$$
b=3.
$$
""",
    ),
    q(
        13,
        "fill_blank",
        4,
        "线性代数",
        ["行列式", "逆矩阵"],
        "39",
        r"""
设 $A,B$ 为 3 阶矩阵，且 $|A|=3,\ |B|=2,\ |A^{-1}+B|=2$，则
$$
|A+B^{-1}|=\underline{\qquad}.
$$
""",
        r"$3$",
        r"""
注意到
$$
A(A^{-1}+B)B^{-1}=B^{-1}+A.
$$
取行列式得
$$
|A+B^{-1}|=|A||A^{-1}+B||B^{-1}|.
$$
由 $|B|=2$ 可知
$$
|B^{-1}|=\frac12.
$$
于是
$$
|A+B^{-1}|=3\times2\times\frac12=3.
$$
""",
    ),
    q(
        14,
        "fill_blank",
        4,
        "概率统计",
        ["数学期望", "正态总体样本"],
        "39",
        r"""
设 $X_1,X_2,\cdots,X_n$ 是来自总体 $N(\mu,\sigma^2)\ (\sigma>0)$ 的简单随机样本。记统计量
$$
T=\frac1n\sum_{i=1}^nX_i^2,
$$
则
$$
E(T)=\underline{\qquad}.
$$
""",
        r"$\sigma^2+\mu^2$",
        r"""
由期望的线性性，
$$
E(T)=\frac1n\sum_{i=1}^nE(X_i^2)=E(X^2).
$$
而
$$
E(X^2)=D(X)+[E(X)]^2=\sigma^2+\mu^2.
$$
故
$$
E(T)=\sigma^2+\mu^2.
$$
""",
    ),
    q(
        15,
        "solution",
        10,
        "高等数学",
        ["极限", "指数极限", "对数化简"],
        "39",
        r"""
求极限
$$
\lim_{x\to+\infty}\left(x^{1/x}-1\right)^{1/\ln x}.
$$
""",
        r"$e^{-1}$",
        r"""
设
$$
L=\lim_{x\to+\infty}\left(x^{1/x}-1\right)^{1/\ln x}.
$$
两边取对数，
$$
\ln L=\lim_{x\to+\infty}\frac{\ln(x^{1/x}-1)}{\ln x}.
$$
注意到
$$
x^{1/x}=e^{(\ln x)/x}=1+\frac{\ln x}{x}+o\!\left(\frac{\ln x}{x}\right),
$$
因此
$$
x^{1/x}-1\sim \frac{\ln x}{x}.
$$
故
$$
\ln(x^{1/x}-1)\sim \ln\left(\frac{\ln x}{x}\right)=\ln\ln x-\ln x.
$$
于是
$$
\ln L=\lim_{x\to+\infty}\frac{\ln\ln x-\ln x}{\ln x}=-1.
$$
从而
$$
L=e^{-1}.
$$
""",
    ),
    q(
        16,
        "solution",
        10,
        "高等数学",
        ["二重积分", "区域对称性"],
        "40",
        r"""
计算二重积分
$$
\iint_D(x+y)^3\,dxdy,
$$
其中 $D$ 由曲线 $x=\sqrt{1+y^2}$ 与直线 $x+\sqrt2y=0$ 及 $x-\sqrt2y=0$ 围成。
""",
        r"$\dfrac{14}{15}$",
        r"""
区域关于 $x$ 轴对称，可写成
$$
D=D_1\cup D_2,
$$
其中
$$
D_1=\{(x,y)\mid 0\le y\le1,\ \sqrt2y\le x\le\sqrt{1+y^2}\},
$$
$$
D_2=\{(x,y)\mid -1\le y\le0,\ -\sqrt2y\le x\le\sqrt{1+y^2}\}.
$$

展开 integrand：
$$
(x+y)^3=x^3+3x^2y+3xy^2+y^3.
$$
由于区域关于 $x$ 轴对称，且 $3x^2y+y^3$ 关于 $y$ 为奇函数，所以它们在 $D$ 上积分为 0。
故
$$
\iint_D(x+y)^3\,dxdy=\iint_D(x^3+3xy^2)\,dxdy.
$$
再利用对称性，
$$
=2\int_0^1\int_{\sqrt2y}^{\sqrt{1+y^2}}(x^3+3xy^2)\,dx\,dy.
$$
先对 $x$ 积分得
$$
2\int_0^1\left[\frac14x^4+\frac32x^2y^2\right]_{\sqrt2y}^{\sqrt{1+y^2}}dy
=2\int_0^1\left(\frac14+2y^2-\frac94y^4\right)dy
=\frac{14}{15}.
$$
""",
    ),
    q(
        17,
        "solution",
        10,
        "高等数学",
        ["条件极值", "拉格朗日乘数法"],
        "40",
        r"""
求函数
$$
u=xy+2yz
$$
在约束条件
$$
x^2+y^2+z^2=10
$$
下的最大值和最小值。
""",
        r"$u_{\max}=5\sqrt5,\quad u_{\min}=-5\sqrt5$",
        r"""
构造拉格朗日函数
$$
F(x,y,z,\lambda)=xy+2yz+\lambda(x^2+y^2+z^2-10).
$$
由驻点条件得
$$
\begin{cases}
y+2\lambda x=0,\\
x+2z+2\lambda y=0,\\
2y+2\lambda z=0,\\
x^2+y^2+z^2=10.
\end{cases}
$$
解得 6 个驻点：
$$
(1,\sqrt5,2),\ (-1,-\sqrt5,-2),\ (1,-\sqrt5,2),\ (-1,\sqrt5,-2),
$$
$$
(2\sqrt2,0,-\sqrt2),\ (-2\sqrt2,0,\sqrt2).
$$
分别代入
$$
u=xy+2yz
$$
可得
$$
u=5\sqrt5,\ -5\sqrt5,\ -5\sqrt5,\ 5\sqrt5,\ 0,\ 0.
$$
所以
$$
u_{\max}=5\sqrt5,\qquad u_{\min}=-5\sqrt5.
$$
""",
    ),
    q(
        18,
        "solution",
        10,
        "高等数学",
        ["定积分比较", "夹逼定理"],
        "40",
        r"""
1. 比较
$$
\int_0^1|\ln t|[\ln(1+t)]^n\,dt
$$
与
$$
\int_0^1 t^n|\ln t|\,dt\qquad (n=1,2,\cdots)
$$
的大小，并说明理由；

2. 记
$$
u_n=\int_0^1|\ln t|[\ln(1+t)]^n\,dt\qquad (n=1,2,\cdots),
$$
求 $\lim\limits_{n\to\infty}u_n$。
""",
        r"""
1. 有
$$
\int_0^1|\ln t|[\ln(1+t)]^n\,dt<\int_0^1 t^n|\ln t|\,dt;
$$

2. 
$$
\lim_{n\to\infty}u_n=0.
$$
""",
        r"""
对 $0<t<1$，有
$$
0<\ln(1+t)<t.
$$
因此
$$
[\ln(1+t)]^n<t^n.
$$
再乘上非负函数 $|\ln t|$ 并积分，得
$$
\int_0^1|\ln t|[\ln(1+t)]^n\,dt<\int_0^1 t^n|\ln t|\,dt.
$$

又
$$
\int_0^1 t^n|\ln t|\,dt
=-\int_0^1 t^n\ln t\,dt
=\frac1{(n+1)^2}.
$$
所以
$$
0<u_n<\frac1{(n+1)^2}.
$$
由夹逼定理，
$$
\lim_{n\to\infty}u_n=0.
$$
""",
    ),
    q(
        19,
        "solution",
        10,
        "高等数学",
        ["积分中值定理", "罗尔定理", "二阶导数零点"],
        "40",
        r"""
设函数 $f(x)$ 在 $[0,3]$ 上连续，在 $(0,3)$ 内存在二阶导数，且
$$
2f(0)=\int_0^2 f(x)\,dx=f(2)+f(3).
$$

1. 证明存在 $\eta\in(0,2)$，使 $f(\eta)=f(0)$；  
2. 证明存在 $\xi\in(0,3)$，使 $f''(\xi)=0$。
""",
        r"命题成立",
        r"""
由
$$
\int_0^2 f(x)\,dx=2f(0),
$$
结合积分中值定理，存在 $\eta\in(0,2)$，使得
$$
\int_0^2 f(x)\,dx=2f(\eta).
$$
于是
$$
2f(\eta)=2f(0),
$$
故
$$
f(\eta)=f(0).
$$

再由
$$
f(2)+f(3)=2f(0),
$$
知 $\dfrac{f(2)+f(3)}2=f(0)$。由于 $f$ 在 $[2,3]$ 上连续，故存在 $\eta_1\in(2,3)$ 使
$$
f(\eta_1)=f(0).
$$

于是有
$$
f(0)=f(\eta)=f(\eta_1).
$$
由罗尔定理，存在
$$
\xi_1\in(0,\eta),\qquad \xi_2\in(\eta,\eta_1),
$$
使得
$$
f'(\xi_1)=0,\qquad f'(\xi_2)=0.
$$
再在区间 $[\xi_1,\xi_2]$ 上应用罗尔定理，得到存在 $\xi\in(0,3)$ 使
$$
f''(\xi)=0.
$$
""",
    ),
    q(
        20,
        "solution",
        11,
        "线性代数",
        ["线性方程组", "参数讨论", "通解"],
        "41",
        r"""
设
$$
A=
\begin{pmatrix}
\lambda&1&1\\
0&\lambda-1&0\\
1&1&\lambda
\end{pmatrix},
\qquad
b=
\begin{pmatrix}
a\\
1\\
1
\end{pmatrix}.
$$
已知线性方程组 $Ax=b$ 存在两个不同的解。

1. 求 $\lambda,a$；  
2. 求方程组 $Ax=b$ 的通解。
""",
        r"""
$$
\lambda=-1,\quad a=-2;
$$

通解为
$$
x=k
\begin{pmatrix}
1\\0\\1
\end{pmatrix}
+
\begin{pmatrix}
\frac32\\[2pt]-\frac12\\[2pt]0
\end{pmatrix},
\quad k\in\mathbb R.
$$
""",
        r"""
方程组存在两个不同的解，说明它有无穷多解，因此
$$
r(A)=r(\bar A)<3,
$$
从而
$$
|A|=0.
$$
计算得
$$
|A|=(\lambda-1)^2(\lambda+1)=0.
$$
所以 $\lambda=1$ 或 $\lambda=-1$。

若 $\lambda=1$，代入增广矩阵可知
$$
r(A)\ne r(\bar A),
$$
方程组无解，舍去。
故
$$
\lambda=-1.
$$

再代入增广矩阵并行变换，可得必须有
$$
a=-2.
$$

此时方程组化简为
$$
\begin{cases}
x_1-x_3=\dfrac32,\\[4pt]
x_2=-\dfrac12.
\end{cases}
$$
令 $x_3=k$，则
$$
x_1=k+\frac32,\qquad x_2=-\frac12.
$$
故通解为
$$
x=
\begin{pmatrix}
\frac32\\[2pt]-\frac12\\[2pt]0
\end{pmatrix}
+
k
\begin{pmatrix}
1\\0\\1
\end{pmatrix},
\quad k\in\mathbb R.
$$
""",
    ),
    q(
        21,
        "solution",
        11,
        "线性代数",
        ["实对称矩阵", "正交对角化", "特征值特征向量"],
        "41",
        r"""
设
$$
A=
\begin{pmatrix}
0&-1&4\\
-1&3&a\\
4&a&0
\end{pmatrix},
$$
正交矩阵 $Q$ 使 $Q^TAQ$ 为对角矩阵，若 $Q$ 的第 1 列为
$$
\frac1{\sqrt6}(1,2,1)^T,
$$
求 $a,Q$。
""",
        r"""
$$
a=-1;
$$

可取
$$
Q=
\begin{pmatrix}
\frac1{\sqrt6} & -\frac1{\sqrt2} & \frac1{\sqrt3}\\[6pt]
\frac2{\sqrt6} & 0 & -\frac1{\sqrt3}\\[6pt]
\frac1{\sqrt6} & \frac1{\sqrt2} & \frac1{\sqrt3}
\end{pmatrix}.
$$
""",
        r"""
因为 $Q$ 的第 1 列是 $A$ 的一个单位特征向量，设对应特征值为 $\lambda_1$，则
$$
A
\begin{pmatrix}
1\\2\\1
\end{pmatrix}
=\lambda_1
\begin{pmatrix}
1\\2\\1
\end{pmatrix}.
$$
计算左端：
$$
\begin{pmatrix}
0&-1&4\\
-1&3&a\\
4&a&0
\end{pmatrix}
\begin{pmatrix}
1\\2\\1
\end{pmatrix}
=
\begin{pmatrix}
2\\
5+a\\
4+2a
\end{pmatrix}.
$$
与 $\lambda_1(1,2,1)^T$ 对比，得
$$
\lambda_1=2,\qquad 5+a=4,\qquad 4+2a=2,
$$
故
$$
a=-1.
$$

于是
$$
A=
\begin{pmatrix}
0&-1&4\\
-1&3&-1\\
4&-1&0
\end{pmatrix}.
$$
计算特征多项式可得特征值为
$$
2,\ -4,\ 5.
$$
分别可取对应特征向量
$$
\xi_1=(1,2,1)^T,\quad \xi_2=(-1,0,1)^T,\quad \xi_3=(1,-1,1)^T.
$$
单位化后得
$$
\eta_1=\frac1{\sqrt6}(1,2,1)^T,\quad
\eta_2=\frac1{\sqrt2}(-1,0,1)^T,\quad
\eta_3=\frac1{\sqrt3}(1,-1,1)^T.
$$
取
$$
Q=(\eta_1,\eta_2,\eta_3)
$$
即可。
""",
    ),
    q(
        22,
        "solution",
        11,
        "概率统计",
        ["二维正态型密度", "边缘密度", "条件密度"],
        "41",
        r"""
设二维随机变量 $(X,Y)$ 的概率密度为
$$
f(x,y)=Ae^{-2x^2+2xy-y^2},\qquad -\infty<x<+\infty,\ -\infty<y<+\infty,
$$
求常数 $A$ 及条件概率密度 $f_{Y\mid X}(y\mid x)$。
""",
        r"""
$$
A=\frac1\pi;
$$

$$
f_{Y\mid X}(y\mid x)=\frac1{\sqrt\pi}e^{-(y-x)^2},\qquad -\infty<y<+\infty.
$$
""",
        r"""
先把指数配方：
$$
-2x^2+2xy-y^2=-x^2-(y-x)^2.
$$
因此
$$
f(x,y)=Ae^{-x^2}e^{-(y-x)^2}.
$$

求 $X$ 的边缘密度：
$$
f_X(x)=\int_{-\infty}^{+\infty}f(x,y)\,dy
=Ae^{-x^2}\int_{-\infty}^{+\infty}e^{-(y-x)^2}\,dy
=A\sqrt\pi\,e^{-x^2}.
$$
再由概率密度积分为 1，
$$
1=\int_{-\infty}^{+\infty}f_X(x)\,dx
=A\sqrt\pi\int_{-\infty}^{+\infty}e^{-x^2}\,dx
=A\pi.
$$
故
$$
A=\frac1\pi.
$$

于是
$$
f_X(x)=\frac1{\sqrt\pi}e^{-x^2}.
$$
条件密度为
$$
f_{Y\mid X}(y\mid x)=\frac{f(x,y)}{f_X(x)}
=\frac{(1/\pi)e^{-x^2}e^{-(y-x)^2}}{(1/\sqrt\pi)e^{-x^2}}
=\frac1{\sqrt\pi}e^{-(y-x)^2}.
$$
""",
    ),
    q(
        23,
        "solution",
        11,
        "概率统计",
        ["二维离散分布", "协方差", "组合概率"],
        "41",
        r"""
箱中装有 6 个球，其中红、白、黑球的个数分别为 1,2,3 个。现从箱中随机地取出 2 个球，记 $X$ 为取出的红球个数，$Y$ 为取出的白球个数。

1. 求随机变量 $(X,Y)$ 的概率分布；  
2. 求 $\operatorname{Cov}(X,Y)$。
""",
        r"""
$$
\begin{array}{c|ccc}
 & Y=0 & Y=1 & Y=2\\ \hline
X=0 & \frac15 & \frac25 & \frac1{15}\\[6pt]
X=1 & \frac15 & \frac2{15} & 0
\end{array}
$$

$$
\operatorname{Cov}(X,Y)=-\frac4{45}.
$$
""",
        r"""
总取法数为
$$
\binom62=15.
$$

各点概率分别为：
$$
P(X=0,Y=0)=\frac{\binom32}{\binom62}=\frac15,
$$
$$
P(X=0,Y=1)=\frac{\binom21\binom31}{\binom62}=\frac25,
$$
$$
P(X=0,Y=2)=\frac{\binom22}{\binom62}=\frac1{15},
$$
$$
P(X=1,Y=0)=\frac{\binom11\binom31}{\binom62}=\frac15,
$$
$$
P(X=1,Y=1)=\frac{\binom11\binom21}{\binom62}=\frac2{15},
$$
$$
P(X=1,Y=2)=0.
$$

于是
$$
E(XY)=1\cdot1\cdot\frac2{15}=\frac2{15}.
$$
再算边缘期望：
$$
E(X)=0\cdot\frac23+1\cdot\frac13=\frac13,
$$
$$
E(Y)=0\cdot\frac25+1\cdot\frac8{15}+2\cdot\frac1{15}=\frac23.
$$
故
$$
\operatorname{Cov}(X,Y)=E(XY)-E(X)E(Y)=\frac2{15}-\frac13\cdot\frac23=-\frac4{45}.
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
        "整理状态：按原卷页面视觉核对后人工转写并清洗。",
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
                "- 校对状态：已结合原卷页面人工核对",
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
        "整理状态：按答案页视觉核对后人工清洗整理。",
        "",
    ]
    grouped = {
        "single_choice": [qn for qn in questions if qn.question_type == "single_choice"],
        "fill_blank": [qn for qn in questions if qn.question_type == "fill_blank"],
        "solution": [qn for qn in questions if qn.question_type == "solution"],
    }
    section_names = {
        "single_choice": "选择题",
        "fill_blank": "填空题",
        "solution": "解答题",
    }
    for key in ("single_choice", "fill_blank", "solution"):
        lines.extend(
            [
                f"## {section_names[key]}",
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
