from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[6]
YEAR = 2018
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
        ["导数", "可导性", "左右导数"],
        "6",
        r"""
下列函数中，在 $x=0$ 处不可导的是（ ）

A. $f(x)=|x|\sin|x|$  
B. $f(x)=|x|\sin\sqrt{|x|}$  
C. $f(x)=\cos|x|$  
D. $f(x)=\cos\sqrt{|x|}$
""",
        r"D",
        r"""
对于 D 选项，$f(x)=\cos\sqrt{|x|}$。

由右导数
$$
f'_+(0)=\lim_{x\to0^+}\frac{f(x)-f(0)}{x}
=\lim_{x\to0^+}\frac{\cos\sqrt{x}-1}{x}
=-\frac12,
$$
左导数
$$
f'_-(0)=\lim_{x\to0^-}\frac{f(x)-f(0)}{x}
=\lim_{x\to0^-}\frac{\cos\sqrt{|x|}-1}{x}
=\frac12.
$$
因此 $f'_+(0)\ne f'_-(0)$，故 $f(x)$ 在 $x=0$ 处不可导，选 D。
""",
    ),
    q(
        2,
        "single_choice",
        4,
        "高等数学",
        ["积分中值", "凹凸性", "函数性质"],
        "6",
        r"""
设函数 $f(x)$ 在 $[0,1]$ 上二阶可导，且
$$
\int_0^1 f(x)\,dx=0,
$$
则（ ）

A. 当 $f'(x)<0$ 时，$f\!\left(\dfrac12\right)<0$  
B. 当 $f''(x)<0$ 时，$f\!\left(\dfrac12\right)<0$  
C. 当 $f'(x)>0$ 时，$f\!\left(\dfrac12\right)<0$  
D. 当 $f''(x)>0$ 时，$f\!\left(\dfrac12\right)<0$
""",
        r"D",
        r"""
当 $f(x)=x-\dfrac12$ 时，满足
$$
\int_0^1 f(x)\,dx=0,\qquad f\!\left(\frac12\right)=0,
$$
可排除 A、C。

当 $f(x)=\sqrt{x}-\dfrac23$ 时，也满足
$$
\int_0^1 f(x)\,dx=0,\qquad f''(x)<0,
$$
而
$$
f\!\left(\frac12\right)=\sqrt{\frac12}-\frac23>0,
$$
可排除 B。

因此只有 D 正确。
""",
    ),
    q(
        3,
        "single_choice",
        4,
        "高等数学",
        ["定积分", "对称性", "估值比较"],
        "6",
        r"""
设
$$
M=\int_{-\pi/2}^{\pi/2}\frac{(1+x)^2}{1+x^2}\,dx,\quad
N=\int_{-\pi/2}^{\pi/2}\frac{1+x}{e^x}\,dx,\quad
K=\int_{-\pi/2}^{\pi/2}\bigl(1+\sqrt{\cos x}\bigr)\,dx,
$$
则（ ）

A. $M>N>K$  
B. $M>K>N$  
C. $K>M>N$  
D. $K>N>M$
""",
        r"C",
        r"""
利用对称性可得
$$
M=\int_{-\pi/2}^{\pi/2}\frac{(1+x)^2}{1+x^2}\,dx
=\int_{-\pi/2}^{\pi/2}\left(1+\frac{2x}{1+x^2}\right)\,dx
=\pi.
$$

又容易判断 $K>\pi$，而 $N<\pi$，故
$$
K>M>N.
$$
因此选 C。
""",
    ),
    q(
        4,
        "single_choice",
        4,
        "高等数学",
        ["导数应用", "平均成本", "极值"],
        "6",
        r"""
设某产品的成本函数 $C(Q)$ 可导，其中 $Q$ 为产量。若产量为 $Q_0$ 时平均成本最小，则（ ）

A. $C'(Q_0)=0$  
B. $C'(Q_0)=C(Q_0)$  
C. $C'(Q_0)=Q_0C(Q_0)$  
D. $Q_0C'(Q_0)=C(Q_0)$
""",
        r"D",
        r"""
平均成本为
$$
\frac{C(Q)}{Q}.
$$
其在 $Q_0$ 处取最小值，因此
$$
\left(\frac{C(Q)}{Q}\right)'_{Q=Q_0}=0.
$$
化简得
$$
\frac{Q_0C'(Q_0)-C(Q_0)}{Q_0^2}=0,
$$
所以
$$
Q_0C'(Q_0)=C(Q_0).
$$
故选 D。
""",
    ),
    q(
        5,
        "single_choice",
        4,
        "线性代数",
        ["相似矩阵", "Jordan 形", "矩阵的秩"],
        "6",
        r"""
下列矩阵中，与矩阵
$$
\begin{pmatrix}
1&1&0\\
0&1&1\\
0&0&1
\end{pmatrix}
$$
相似的是（ ）

A. $\begin{pmatrix}1&1&-1\\0&1&1\\0&0&1\end{pmatrix}$  
B. $\begin{pmatrix}1&0&-1\\0&1&1\\0&0&1\end{pmatrix}$  
C. $\begin{pmatrix}1&1&-1\\0&1&0\\0&0&1\end{pmatrix}$  
D. $\begin{pmatrix}1&0&-1\\0&1&0\\0&0&1\end{pmatrix}$
""",
        r"A",
        r"""
题中矩阵的特征值均为 $1$，且是三重特征值。若两矩阵相似，则对应的
$$
E-A
$$
与
$$
E-B
$$
的秩必须相同。

对 A 选项有
$$
E-
\begin{pmatrix}
1&1&-1\\
0&1&1\\
0&0&1
\end{pmatrix}
=
\begin{pmatrix}
0&-1&1\\
0&0&-1\\
0&0&0
\end{pmatrix},
$$
其秩与原矩阵对应的 $E-A$ 相同，故 A 正确。
""",
    ),
    q(
        6,
        "single_choice",
        4,
        "线性代数",
        ["矩阵的秩", "分块矩阵"],
        "6",
        r"""
设 $A,B$ 为 $n$ 阶矩阵，记 $r(X)$ 为矩阵 $X$ 的秩，$(X,Y)$ 表示分块矩阵，则（ ）

A. $r(A,AB)=r(A)$  
B. $r(A,BA)=r(A)$  
C. $r(A,B)=\max\{r(A),r(B)\}$  
D. $r(A,B)=r(A^T,B^T)$
""",
        r"A",
        r"""
对 B 选项，可举反例
$$
A=\begin{pmatrix}1&0\\0&0\end{pmatrix},\quad
B=\begin{pmatrix}1&0\\1&1\end{pmatrix},
$$
则 $r(A,BA)=2\ne r(A)$，故 B 错。

对 C 选项，也可取反例使 $r(A,B)=2\ne\max\{r(A),r(B)\}$。

对 D 选项，同样可取反例说明一般不成立。

而
$$
(A,AB)=A(I,B),
$$
其列空间不超过在 $A$ 的列空间之外增加新秩，因此结论 A 成立，故选 A。
""",
    ),
    q(
        7,
        "single_choice",
        4,
        "概率统计",
        ["概率密度", "对称性", "积分"],
        "6",
        r"""
设随机变量 $X$ 的概率密度 $f(x)$ 满足 $f(1+x)=f(1-x)$，且
$$
\int_0^2 f(x)\,dx=0.6,
$$
则 $P\{X<0\}=$（ ）

A. $0.2$  
B. $0.3$  
C. $0.4$  
D. $0.5$
""",
        r"A",
        r"""
由 $f(1+x)=f(1-x)$ 可知 $f(x)$ 关于 $x=1$ 对称，所以
$$
\int_{-\infty}^1 f(x)\,dx=\int_1^{+\infty} f(x)\,dx=0.5.
$$
又已知
$$
\int_0^2 f(x)\,dx=0.6,
$$
由对称性可得
$$
\int_0^1 f(x)\,dx=\int_1^2 f(x)\,dx=0.3.
$$
因此
$$
P(X<0)=\int_{-\infty}^0 f(x)\,dx
=\int_{-\infty}^1 f(x)\,dx-\int_0^1 f(x)\,dx
=0.5-0.3=0.2.
$$
故选 A。
""",
    ),
    q(
        8,
        "single_choice",
        4,
        "概率统计",
        ["正态总体", "t分布", "统计量分布"],
        "6",
        r"""
设 $X_1,X_2,\ldots,X_n\ (n\ge2)$ 为来自总体 $N(\mu,\sigma^2)\ (\sigma>0)$ 的简单随机样本。令
$$
\overline X=\frac1n\sum_{i=1}^n X_i,\quad
S=\sqrt{\frac1{n-1}\sum_{i=1}^n (X_i-\overline X)^2},\quad
S^*=\sqrt{\frac1n\sum_{i=1}^n (X_i-\mu)^2},
$$
则下列结论中正确的是（ ）

A. $\dfrac{\sqrt n(\overline X-\mu)}{S}\sim t(n)$  
B. $\dfrac{\sqrt n(\overline X-\mu)}{S}\sim t(n-1)$  
C. $\dfrac{\sqrt n(\overline X-\mu)}{S^*}\sim t(n)$  
D. $\dfrac{\sqrt n(\overline X-\mu)}{S^*}\sim t(n-1)$
""",
        r"B",
        r"""
由正态总体抽样理论，
$$
\overline X\sim N\!\left(\mu,\frac{\sigma^2}{n}\right),
$$
且
$$
\frac{(n-1)S^2}{\sigma^2}\sim\chi^2(n-1),
$$
并与 $\overline X$ 独立。

因此
$$
\frac{\sqrt n(\overline X-\mu)}{S}\sim t(n-1).
$$
故选 B。
""",
    ),
    q(
        9,
        "fill_blank",
        4,
        "高等数学",
        ["曲线方程", "拐点", "切线"],
        "7",
        r"""
曲线 $y=x^2+2\ln x$ 在其拐点处的切线方程是 $\underline{\qquad}$。
""",
        r"$y=4x-3$",
        r"""
有
$$
y'=2x+\frac2x,\qquad y''=2-\frac2{x^2}.
$$
令 $y''=0$ 得拐点横坐标 $x=1$（定义域内只取正值），代入得拐点为 $(1,1)$。

此时切线斜率
$$
y'(1)=2+\frac21=4.
$$
因此切线方程为
$$
y-1=4(x-1),
$$
即
$$
y=4x-3.
$$
""",
    ),
    q(
        10,
        "fill_blank",
        4,
        "高等数学",
        ["不定积分", "换元积分"],
        "7",
        r"""
$$
\int e^x\arcsin\sqrt{1-e^{2x}}\,dx=\underline{\qquad}.
$$
""",
        r"$e^x\arcsin\sqrt{1-e^{2x}}-\sqrt{1-e^{2x}}+C$",
        r"""
令
$$
\arcsin\sqrt{1-e^{2x}}=t,
$$
则
$$
e^x=|\cos t|=\cos t
$$
（在积分区间对应情形下取正值），原式可化为
$$
-\int t\sin t\,dt
=t\cos t-\int \cos t\,dt
=t\cos t-\sin t+C.
$$
再代回
$$
t=\arcsin\sqrt{1-e^{2x}},\qquad \sin t=\sqrt{1-e^{2x}},\qquad \cos t=e^x,
$$
得
$$
\int e^x\arcsin\sqrt{1-e^{2x}}\,dx
=e^x\arcsin\sqrt{1-e^{2x}}-\sqrt{1-e^{2x}}+C.
$$
""",
    ),
    q(
        11,
        "fill_blank",
        4,
        "高等数学",
        ["差分方程", "递推数列"],
        "7",
        r"""
差分方程 $\Delta^2 y_x-y_x=5$ 的通解为 $\underline{\qquad}$。
""",
        r"$C2^x-5$",
        r"""
由二阶差分定义，
$$
\Delta^2 y_x=\Delta y_{x+1}-\Delta y_x=(y_{x+2}-y_{x+1})-(y_{x+1}-y_x)
=y_{x+2}-2y_{x+1}+y_x.
$$
原方程化为
$$
y_{x+2}-2y_{x+1}=5.
$$

对应齐次方程的特征方程为
$$
\lambda^2-2\lambda=0,
$$
其非零特征根为 $\lambda=2$，故齐次解为 $C2^x$。

设特解为常数 $A$，代入得 $-A=5$，故 $A=-5$。
于是通解为
$$
y_x=C2^x-5.
$$
""",
    ),
    q(
        12,
        "fill_blank",
        4,
        "高等数学",
        ["导数定义", "微分方程"],
        "7",
        r"""
设函数 $f(x)$ 满足
$$
f(x+\Delta x)-f(x)=2xf(x)\Delta x+o(\Delta x)\quad (\Delta x\to0),
$$
且 $f(0)=2$，则 $f(1)=\underline{\qquad}$。
""",
        r"$2e$",
        r"""
移项并同除以 $\Delta x$，得
$$
\frac{f(x+\Delta x)-f(x)}{\Delta x}-2xf(x)=\frac{o(\Delta x)}{\Delta x}.
$$
令 $\Delta x\to0$，可得
$$
f'(x)=2xf(x).
$$
解微分方程
$$
\frac{f'(x)}{f(x)}=2x
$$
得
$$
f(x)=Ce^{x^2}.
$$
由 $f(0)=2$ 得 $C=2$，故
$$
f(1)=2e.
$$
""",
    ),
    q(
        13,
        "fill_blank",
        4,
        "线性代数",
        ["行列式", "线性变换"],
        "7",
        r"""
设 $A$ 为 $3$ 阶矩阵，$\alpha_1,\alpha_2,\alpha_3$ 是线性无关的向量组。若
$$
A\alpha_1=\alpha_1+\alpha_2,\quad
A\alpha_2=\alpha_2+\alpha_3,\quad
A\alpha_3=\alpha_1+\alpha_3,
$$
则 $|A|=\underline{\qquad}$。
""",
        r"$2$",
        r"""
以向量组 $(\alpha_1,\alpha_2,\alpha_3)$ 为基，线性变换 $A$ 的矩阵为
$$
\begin{pmatrix}
1&0&1\\
1&1&0\\
0&1&1
\end{pmatrix}.
$$
由于 $\alpha_1,\alpha_2,\alpha_3$ 线性无关，这个表示矩阵与 $A$ 相似，故行列式相同。

因此
$$
|A|=\begin{vmatrix}
1&0&1\\
1&1&0\\
0&1&1
\end{vmatrix}=2.
$$
""",
    ),
    q(
        14,
        "fill_blank",
        4,
        "概率统计",
        ["条件概率", "相互独立"],
        "7",
        r"""
随机事件 $A,B,C$ 相互独立，且
$$
P(A)=P(B)=P(C)=\frac12,
$$
则
$$
P(AC\mid A\cup B)=\underline{\qquad}.
$$
""",
        r"$\dfrac13$",
        r"""
由条件概率公式，
$$
P(AC\mid A\cup B)=\frac{P\bigl(AC\cap(A\cup B)\bigr)}{P(A\cup B)}.
$$
注意到
$$
AC\cap(A\cup B)=AC,
$$
所以分子为
$$
P(AC)=P(A)P(C)=\frac14.
$$
又
$$
P(A\cup B)=P(A)+P(B)-P(AB)=\frac12+\frac12-\frac14=\frac34.
$$
因此
$$
P(AC\mid A\cup B)=\frac{1/4}{3/4}=\frac13.
$$
""",
    ),
    q(
        15,
        "solution",
        10,
        "高等数学",
        ["极限", "等价无穷小", "参数求值"],
        "7-8",
        r"""
已知实数 $a,b$ 满足
$$
\lim_{x\to+\infty}\left[\left(ax+b\right)e^{1/x}-x\right]=2,
$$
求 $a,b$。
""",
        r"$a=1,\ b=1$",
        r"""
令
$$
t=\frac1x,
$$
则当 $x\to+\infty$ 时，$t\to0^+$，原极限化为
$$
\lim_{t\to0^+}\frac{(a+bt)e^t-1}{t}=2.
$$

若极限存在，需有
$$
\lim_{t\to0^+}\bigl[(a+bt)e^t-1\bigr]=0,
$$
即
$$
a-1=0,
$$
故 $a=1$。

于是
$$
\lim_{t\to0^+}\frac{(1+bt)e^t-1}{t}
=\lim_{t\to0^+}\left(be^t+\frac{e^t-1}{t}\right)
=b+1.
$$
由题设得 $b+1=2$，所以 $b=1$。
""",
    ),
    q(
        16,
        "solution",
        10,
        "高等数学",
        ["二重积分", "积分区域", "换元"],
        "7",
        r"""
设平面区域 $D$ 由曲线 $y=\sqrt3(1-x^2)$ 与直线 $y=\sqrt3\,x$ 及 $y$ 轴围成。计算二重积分
$$
\iint_D x^2\,dx\,dy.
$$
""",
        r"$\dfrac{\sqrt3}{16}\left(\dfrac{\pi}{2}-1\right)$",
        r"""
由区域边界可知
$$
0\le x\le \frac1{\sqrt2},\qquad \sqrt3\,x\le y\le \sqrt3(1-x^2).
$$
因此
$$
\iint_D x^2\,dx\,dy
=\int_0^{1/\sqrt2}\!\!dx\int_{\sqrt3 x}^{\sqrt3(1-x^2)} x^2\,dy
=\sqrt3\int_0^{1/\sqrt2}x^2(\sqrt{1-x^2}-x)\,dx.
$$

分成两项：
$$
\int_0^{1/\sqrt2}x^2\sqrt{1-x^2}\,dx.
$$
令 $x=\sin t$，则 $t\in[0,\pi/4]$，上式化为
$$
\int_0^{\pi/4}\sin^2 t\cos^2 t\,dt
=\frac18\int_0^{\pi/4}(1-\cos4t)\,dt
=\frac{\pi}{32}.
$$
又
$$
\int_0^{1/\sqrt2}x^3\,dx=\frac1{16}.
$$
故
$$
\iint_D x^2\,dx\,dy
=\sqrt3\left(\frac{\pi}{32}-\frac1{16}\right)
=\frac{\sqrt3}{16}\left(\frac{\pi}{2}-1\right).
$$
""",
    ),
    q(
        17,
        "solution",
        10,
        "高等数学",
        ["条件极值", "拉格朗日乘数法"],
        "8",
        r"""
将长为 $2\text{m}$ 的铁丝分成三段，依次围成圆、正方形与正三角形。三个图形的面积之和是否存在最小值？若存在，求出最小值。
""",
        r"存在，最小值为 $\dfrac1{\pi+4+3\sqrt3}$",
        r"""
设圆的半径为 $x$，正方形边长为 $y$，正三角形边长为 $z$，则问题化为求
$$
f(x,y,z)=\pi x^2+y^2+\frac{\sqrt3}{4}z^2
$$
在约束
$$
2\pi x+4y+3z=2,\qquad x>0,\ y>0,\ z>0
$$
下是否有最小值。

令
$$
L(x,y,z,\lambda)=\pi x^2+y^2+\frac{\sqrt3}{4}z^2+\lambda(2\pi x+4y+3z-2).
$$
由拉格朗日方程组
$$
\frac{\partial L}{\partial x}=2\pi x+2\pi\lambda=0,\quad
\frac{\partial L}{\partial y}=2y+4\lambda=0,\quad
\frac{\partial L}{\partial z}=\frac{\sqrt3}{2}z+3\lambda=0,
$$
可解得
$$
x_0=\frac1{\pi+4+3\sqrt3},\quad
y_0=\frac2{\pi+4+3\sqrt3},\quad
z_0=\frac{2\sqrt3}{\pi+4+3\sqrt3}.
$$
此时
$$
f(x_0,y_0,z_0)=\frac1{\pi+4+3\sqrt3}.
$$

再比较边界情形 $xyz=0$，可得最小值更大，因此原问题的最小值存在，且为
$$
\frac1{\pi+4+3\sqrt3}.
$$
""",
    ),
    q(
        18,
        "solution",
        10,
        "高等数学",
        ["幂级数展开", "泰勒展开"],
        "8-9",
        r"""
已知
$$
\cos2x-\frac1{(1+x)^2}=\sum_{n=0}^{\infty}a_nx^n\quad (-1<x<1),
$$
求 $a_n$。
""",
        r"""
$$
a_{2n}=\frac{(-1)^n4^n}{(2n)!}-2n-1,\qquad
a_{2n+1}=2n+2\quad (n=0,1,2,\ldots).
$$
""",
        r"""
先展开
$$
\cos2x=\sum_{n=0}^{\infty}\frac{(-1)^n(2x)^{2n}}{(2n)!}
=\sum_{n=0}^{\infty}\frac{(-1)^n4^n}{(2n)!}x^{2n}.
$$

又
$$
\frac1{(1+x)^2}=\left(-\frac1{1+x}\right)'
=-\left(\sum_{n=0}^{\infty}(-1)^n x^n\right)'
=\sum_{n=0}^{\infty}(-1)^n(n+1)x^n.
$$
故
$$
\cos2x-\frac1{(1+x)^2}
=\sum_{n=0}^{\infty}\frac{(-1)^n4^n}{(2n)!}x^{2n}
+\sum_{n=0}^{\infty}(-1)^{n+1}(n+1)x^n.
$$

于是偶次项与奇次项系数分别为
$$
a_{2n}=\frac{(-1)^n4^n}{(2n)!}-2n-1,
$$
$$
a_{2n+1}=2n+2\qquad (n=0,1,2,\ldots).
$$
""",
    ),
    q(
        19,
        "solution",
        10,
        "高等数学",
        ["数列极限", "单调有界", "中值定理"],
        "8-9",
        r"""
设数列 $\{x_n\}$ 满足：$x_1>0$，
$$
x_ne^{x_{n+1}}=e^{x_n}-1\quad (n=1,2,\ldots).
$$
证明 $\{x_n\}$ 收敛，并求 $\lim\limits_{n\to\infty}x_n$。
""",
        r"$\lim\limits_{n\to\infty}x_n=0$",
        r"""
由题设
$$
e^{x_{n+1}}=\frac{e^{x_n}-1}{x_n}.
$$
由微分中值定理，存在 $\xi_n\in(0,x_n)$，使得
$$
\frac{e^{x_n}-1}{x_n}=e^{\xi_n}.
$$
所以
$$
e^{x_{n+1}}=e^{\xi_n},
$$
从而
$$
0<x_{n+1}<x_n.
$$
故 $\{x_n\}$ 单调递减且有下界 $0$，因此收敛。设
$$
\lim_{n\to\infty}x_n=a\ge0.
$$
将极限代入原关系得
$$
ae^a=e^a-1.
$$

令
$$
f(x)=xe^x-e^x+1,
$$
则
$$
f'(x)=xe^x.
$$
当 $x>0$ 时，$f'(x)>0$，所以 $f(x)$ 在 $[0,+\infty)$ 上单调增加。又 $f(0)=0$，故方程在 $[0,+\infty)$ 上唯一解为 $a=0$。

因此
$$
\lim_{n\to\infty}x_n=0.
$$
""",
    ),
    q(
        20,
        "solution",
        11,
        "线性代数",
        ["二次型", "正定性", "规范形"],
        "8-9",
        r"""
设实二次型
$$
f(x_1,x_2,x_3)=(x_1-x_2+x_3)^2+(x_2+x_3)^2+(x_1+ax_3)^2,
$$
其中 $a$ 是参数。

1. 求 $f(x_1,x_2,x_3)=0$ 的解；  
2. 求 $f(x_1,x_2,x_3)$ 的规范形。
""",
        r"""
1. 当 $a\ne2$ 时，解只有 $x=0$；当 $a=2$ 时，解为
$$
x=k(-2,-1,1)^T,\quad k\in\mathbb R.
$$
2. 当 $a\ne2$ 时，规范形为
$$
y_1^2+y_2^2+y_3^2;
$$
当 $a=2$ 时，规范形为
$$
y_1^2+y_2^2.
$$
""",
        r"""
由 $f(x_1,x_2,x_3)=0$ 可知三个平方项都为零，因此
$$
\begin{cases}
x_1-x_2+x_3=0,\\
x_2+x_3=0,\\
x_1+ax_3=0.
\end{cases}
$$
其系数矩阵经初等行变换化为
$$
\begin{pmatrix}
1&-1&1\\
0&1&1\\
1&0&a
\end{pmatrix}
\to
\begin{pmatrix}
1&0&2\\
0&1&1\\
0&0&a-2
\end{pmatrix}.
$$
当 $a\ne2$ 时，只有零解；当 $a=2$ 时，有无穷多解，
$$
x=k(-2,-1,1)^T,\quad k\in\mathbb R.
$$

由此知，当 $a\ne2$ 时，二次型正定，故规范形为
$$
y_1^2+y_2^2+y_3^2.
$$

当 $a=2$ 时，
$$
f(x_1,x_2,x_3)=2x_1^2+2x_2^2+6x_3^2-2x_1x_2+6x_1x_3
=2\left(x_1-\frac12x_2+\frac32x_3\right)^2+\frac32(x_2+x_3)^2,
$$
所以规范形为
$$
y_1^2+y_2^2.
$$
""",
    ),
    q(
        21,
        "solution",
        11,
        "线性代数",
        ["初等变换", "矩阵方程", "可逆矩阵"],
        "9",
        r"""
已知 $a$ 是常数，且矩阵
$$
A=
\begin{pmatrix}
1&2&a\\
1&3&0\\
2&7&-a
\end{pmatrix}
$$
可经初等列变换化为矩阵
$$
B=
\begin{pmatrix}
1&a&2\\
0&1&1\\
-1&1&1
\end{pmatrix}.
$$

1. 求 $a$；  
2. 求满足 $AP=B$ 的可逆矩阵 $P$。
""",
        r"""
$$
a=2.
$$

满足 $AP=B$ 的可逆矩阵为
$$
P=
\begin{pmatrix}
3-6k_1&4-6k_2&4-6k_3\\
-1+2k_1&-1+2k_2&-1+2k_3\\
k_1&k_2&k_3
\end{pmatrix},
\quad k_2\ne k_3.
$$
""",
        r"""
先分别对矩阵 $A,B$ 作初等行变换：
$$
A=
\begin{pmatrix}
1&2&a\\
1&3&0\\
2&7&-a
\end{pmatrix}
\to
\begin{pmatrix}
1&0&3a\\
0&1&-a\\
0&0&0
\end{pmatrix},
$$
$$
B=
\begin{pmatrix}
1&a&2\\
0&1&1\\
-1&1&1
\end{pmatrix}
\to
\begin{pmatrix}
1&0&0\\
0&1&1\\
0&0&2-a
\end{pmatrix}.
$$
由于 $A,B$ 可经初等列变换互化，故秩相同，从而
$$
2-a=0,\qquad a=2.
$$

当 $a=2$ 时，对增广矩阵 $(A\mid B)$ 进行初等行变换，得
$$
(A\mid B)\to
\begin{pmatrix}
1&0&6&3&4&4\\
0&1&-2&-1&-1&-1\\
0&0&0&0&0&0
\end{pmatrix}.
$$
设 $B=(\beta_1,\beta_2,\beta_3)$，则通解为
$$
X=
\begin{pmatrix}
3-6k_1&4-6k_2&4-6k_3\\
-1+2k_1&-1+2k_2&-1+2k_3\\
k_1&k_2&k_3
\end{pmatrix}.
$$
又
$$
|X|=k_3-k_2,
$$
故当且仅当 $k_2\ne k_3$ 时，$X$ 可逆。于是所求可逆矩阵 $P$ 即为上式。
""",
    ),
    q(
        22,
        "solution",
        11,
        "概率统计",
        ["协方差", "泊松分布", "离散分布"],
        "9",
        r"""
设随机变量 $X$ 与 $Y$ 相互独立，$X$ 的概率分布为
$$
P\{X=1\}=P\{X=-1\}=\frac12,
$$
$Y$ 服从参数为 $\lambda$ 的泊松分布。令 $Z=XY$。

1. 求 $\operatorname{Cov}(X,Z)$；  
2. 求 $Z$ 的概率分布。
""",
        r"""
$$
\operatorname{Cov}(X,Z)=\lambda.
$$

$$
P\{Z=0\}=e^{-\lambda},
$$
且对 $n=\pm1,\pm2,\ldots$，
$$
P\{Z=n\}=e^{-\lambda}\frac{\lambda^{|n|}}{2|n|!}.
$$
""",
        r"""
由 $Z=XY$ 与独立性，
$$
EX=(-1)\cdot\frac12+1\cdot\frac12=0,
$$
$$
E(XZ)=E(X^2Y)=EX^2\cdot EY=\lambda.
$$
所以
$$
\operatorname{Cov}(X,Z)=E(XZ)-EX\cdot EZ=\lambda.
$$

又因为 $X=\pm1$，故 $Z$ 可能取所有整数值。

当 $Z=0$ 时，只能是 $Y=0$，因此
$$
P\{Z=0\}=P\{Y=0\}=e^{-\lambda}.
$$

对 $n=\pm1,\pm2,\ldots$，
$$
P\{Z=n\}=P\{XY=n\}
=P\left\{X=\frac{n}{|n|},\,Y=|n|\right\}
=P\left\{X=\frac{n}{|n|}\right\}P\{Y=|n|\}.
$$
于是
$$
P\{Z=n\}=\frac12\cdot e^{-\lambda}\frac{\lambda^{|n|}}{|n|!}
=e^{-\lambda}\frac{\lambda^{|n|}}{2|n|!}.
$$
""",
    ),
    q(
        23,
        "solution",
        11,
        "概率统计",
        ["极大似然估计", "数学期望", "方差"],
        "9",
        r"""
设总体 $X$ 的概率密度为
$$
f(x;\sigma)=\frac1{2\sigma}e^{-\frac{|x|}{\sigma}},\quad -\infty<x<+\infty,
$$
其中 $\sigma\in(0,+\infty)$ 为未知参数，$X_1,X_2,\ldots,X_n$ 为来自总体 $X$ 的简单随机样本。记 $\sigma$ 的最大似然估计量为 $\hat\sigma$。

1. 求 $\hat\sigma$；  
2. 求 $E(\hat\sigma),D(\hat\sigma)$。
""",
        r"""
$$
\hat\sigma=\frac1n\sum_{i=1}^n|X_i|.
$$

$$
E(\hat\sigma)=\sigma,\qquad D(\hat\sigma)=\frac{\sigma^2}{n}.
$$
""",
        r"""
样本似然函数为
$$
L(\sigma)=\prod_{i=1}^n\frac1{2\sigma}e^{-\frac{|x_i|}{\sigma}}
=\frac1{2^n\sigma^n}e^{-\frac1\sigma\sum_{i=1}^n|x_i|}.
$$
取对数得
$$
\ln L(\sigma)=-n\ln2-n\ln\sigma-\frac1\sigma\sum_{i=1}^n|x_i|.
$$
求导并令其为零：
$$
\frac{d\ln L(\sigma)}{d\sigma}
=-\frac n\sigma+\frac1{\sigma^2}\sum_{i=1}^n|x_i|=0,
$$
解得
$$
\hat\sigma=\frac1n\sum_{i=1}^n|X_i|.
$$

又因为
$$
E|X|=\int_{-\infty}^{+\infty}|x|f(x;\sigma)\,dx=\sigma,
$$
所以
$$
E(\hat\sigma)=\frac1n\sum_{i=1}^nE|X_i|=\sigma.
$$

再由
$$
E(|X|^2)=\int_{-\infty}^{+\infty}x^2f(x;\sigma)\,dx=2\sigma^2,
$$
得
$$
D(|X|)=E(|X|^2)-[E|X|]^2=2\sigma^2-\sigma^2=\sigma^2.
$$
因此
$$
D(\hat\sigma)=\frac1{n^2}\sum_{i=1}^nD(|X_i|)=\frac{\sigma^2}{n}.
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
