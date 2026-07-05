from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[6]
YEAR = 2017
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
        ["连续性", "极限", "参数条件"],
        "10",
        r"""
若函数
$$
f(x)=
\begin{cases}
\dfrac{1-\cos\sqrt{x}}{ax}, & x>0,\\[4pt]
b, & x\le 0,
\end{cases}
$$
在 $x=0$ 处连续，则（ ）

A. $ab=\dfrac12$  
B. $ab=-\dfrac12$  
C. $ab=0$  
D. $ab=2$
""",
        r"A",
        r"""
由连续性知
$$
\lim_{x\to0^+}f(x)=b.
$$
而
$$
\lim_{x\to0^+}\frac{1-\cos\sqrt{x}}{ax}
=\lim_{x\to0^+}\frac{x/2}{ax}
=\frac1{2a}.
$$
故
$$
b=\frac1{2a},
$$
从而
$$
ab=\frac12.
$$
故选 A。
""",
    ),
    q(
        2,
        "single_choice",
        4,
        "高等数学",
        ["多元函数", "极值点", "Hessian 判别"],
        "10",
        r"""
二元函数
$$
z=xy(3-x-y)
$$
的极值点是（ ）

A. $(0,0)$  
B. $(0,3)$  
C. $(3,0)$  
D. $(1,1)$
""",
        r"D",
        r"""
计算偏导数
$$
z_x=3y-2xy-y^2,\qquad z_y=3x-2xy-x^2.
$$
联立 $z_x=z_y=0$ 得驻点
$$
(0,0),\ (1,1),\ (0,3),\ (3,0).
$$

再算二阶偏导
$$
z_{xx}=-2y,\qquad z_{yy}=-2x,\qquad z_{xy}=3-2x-2y.
$$
在 $(1,1)$ 处，
$$
z_{xx}z_{yy}-z_{xy}^2=(-2)(-2)-(-1)^2=3>0,
$$
且 $z_{xx}<0$，故 $(1,1)$ 是极大值点。

其余三点对应判别式小于零，不是极值点。故选 D。
""",
    ),
    q(
        3,
        "single_choice",
        4,
        "高等数学",
        ["导数", "单调性", "函数符号"],
        "10",
        r"""
设函数 $f(x)$ 可导，且 $f(x)f'(x)>0$，则（ ）

A. $f(1)>f(-1)$  
B. $f(1)<f(-1)$  
C. $|f(1)|>|f(-1)|$  
D. $|f(1)|<|f(-1)|$
""",
        r"C",
        r"""
由
$$
f(x)f'(x)>0
$$
可得
$$
[f^2(x)]'=2f(x)f'(x)>0.
$$
因此 $f^2(x)$ 严格单调增加，从而
$$
f^2(1)>f^2(-1),
$$
即
$$
|f(1)|>|f(-1)|.
$$
故选 C。
""",
    ),
    q(
        4,
        "single_choice",
        4,
        "高等数学",
        ["级数敛散性", "等价无穷小"],
        "10",
        r"""
若级数
$$
\sum_{n=2}^{\infty}\left[\sin\frac1n-k\ln\left(1-\frac1n\right)\right]
$$
收敛，则 $k=$（ ）

A. $1$  
B. $2$  
C. $-1$  
D. $-2$
""",
        r"C",
        r"""
当 $n\to\infty$ 时，
$$
\sin\frac1n=\frac1n+o\!\left(\frac1n\right),
$$
且
$$
\ln\left(1-\frac1n\right)=-\frac1n-\frac1{2n^2}+o\!\left(\frac1{n^2}\right).
$$
于是通项
$$
\sin\frac1n-k\ln\left(1-\frac1n\right)
=\frac{1+k}{n}+o\!\left(\frac1n\right).
$$
要使级数收敛，必须有 $1+k=0$，故
$$
k=-1.
$$
故选 C。
""",
    ),
    q(
        5,
        "single_choice",
        4,
        "线性代数",
        ["矩阵可逆", "秩一矩阵", "特征值"],
        "10",
        r"""
设 $\alpha$ 为 $n$ 维单位列向量，$E$ 为 $n$ 阶单位矩阵，则（ ）

A. $E-\alpha\alpha^T$ 不可逆  
B. $E+\alpha\alpha^T$ 不可逆  
C. $E+2\alpha\alpha^T$ 不可逆  
D. $E-2\alpha\alpha^T$ 不可逆
""",
        r"A",
        r"""
因为 $\alpha$ 是单位列向量，所以
$$
\alpha^T\alpha=1.
$$
矩阵 $\alpha\alpha^T$ 为秩一矩阵，其特征值为 $1,0,\ldots,0$。
因此
$$
E-\alpha\alpha^T
$$
的特征值为
$$
0,1,\ldots,1,
$$
故其不可逆。选 A。
""",
    ),
    q(
        6,
        "single_choice",
        4,
        "线性代数",
        ["相似", "Jordan 形", "特征向量个数"],
        "10-11",
        r"""
已知矩阵
$$
A=\begin{pmatrix}2&0&0\\0&2&1\\0&0&1\end{pmatrix},\quad
B=\begin{pmatrix}2&1&0\\0&2&0\\0&0&1\end{pmatrix},\quad
C=\begin{pmatrix}1&0&0\\0&2&0\\0&0&2\end{pmatrix},
$$
则（ ）

A. $A$ 与 $C$ 相似，$B$ 与 $C$ 相似  
B. $A$ 与 $C$ 相似，$B$ 与 $C$ 不相似  
C. $A$ 与 $C$ 不相似，$B$ 与 $C$ 相似  
D. $A$ 与 $C$ 不相似，$B$ 与 $C$ 不相似
""",
        r"B",
        r"""
三个矩阵的特征值都为 $1,2,2$。要判断是否与对角矩阵 $C$ 相似，只需看特征值 $2$ 的线性无关特征向量个数。

对 $A$，
$$
3-r(2E-A)=3-1=2,
$$
故特征值 $2$ 有两个线性无关特征向量，可以对角化，所以 $A$ 与 $C$ 相似。

对 $B$，
$$
3-r(2E-B)=3-2=1,
$$
故特征值 $2$ 只有一个线性无关特征向量，不能对角化，因此 $B$ 与 $C$ 不相似。

故选 B。
""",
    ),
    q(
        7,
        "single_choice",
        4,
        "概率统计",
        ["事件独立", "并事件"],
        "10-11",
        r"""
设 $A,B,C$ 为三个随机事件，且 $A$ 与 $C$ 相互独立，$B$ 与 $C$ 相互独立，则 $A\cup B$ 与 $C$ 相互独立的充分必要条件是（ ）

A. $A$ 与 $B$ 相互独立  
B. $A$ 与 $B$ 互不相容  
C. $AB$ 与 $C$ 相互独立  
D. $AB$ 与 $C$ 互不相容
""",
        r"C",
        r"""
由 $A$ 与 $C$ 独立、$B$ 与 $C$ 独立，有
$$
P(AC)=P(A)P(C),\qquad P(BC)=P(B)P(C).
$$
又
$$
P[(A\cup B)C]=P(AC\cup BC)=P(AC)+P(BC)-P(ABC).
$$
而
$$
P(A\cup B)P(C)=[P(A)+P(B)-P(AB)]P(C).
$$
比较二者可知
$$
A\cup B \text{ 与 } C \text{ 独立}
\iff P(ABC)=P(AB)P(C),
$$
即
$$
AB \text{ 与 } C \text{ 独立}.
$$
故选 C。
""",
    ),
    q(
        8,
        "single_choice",
        4,
        "概率统计",
        ["正态分布", "卡方分布"],
        "10-11",
        r"""
设 $X_1,X_2,\ldots,X_n\ (n\ge2)$ 为来自总体 $N(\mu,1)$ 的简单随机样本，记
$$
\overline X=\frac1n\sum_{i=1}^n X_i,
$$
则下列结论中不正确的是（ ）

A. $\sum_{i=1}^n(X_i-\mu)^2$ 服从 $\chi^2(n)$ 分布  
B. $2(X_n-X_1)^2$ 服从 $\chi^2$ 分布  
C. $\sum_{i=1}^n(X_i-\overline X)^2$ 服从 $\chi^2(n-1)$ 分布  
D. $n(\overline X-\mu)^2$ 服从 $\chi^2(1)$ 分布
""",
        r"B",
        r"""
因为 $X_i\sim N(\mu,1)$，所以
$$
X_i-\mu\sim N(0,1),
$$
故 A 正确。

又
$$
\sum_{i=1}^n(X_i-\overline X)^2\sim\chi^2(n-1),
$$
因此 C 正确。

且
$$
\overline X\sim N\!\left(\mu,\frac1n\right),
$$
所以
$$
n(\overline X-\mu)^2\sim\chi^2(1),
$$
D 正确。

对于 B，$X_n-X_1\sim N(0,2)$，故
$$
\frac{(X_n-X_1)^2}{2}\sim\chi^2(1),
$$
而不是 $2(X_n-X_1)^2$。故选 B。
""",
    ),
    q(
        9,
        "fill_blank",
        4,
        "高等数学",
        ["定积分", "奇偶性", "面积"],
        "11",
        r"""
$$
\int_{-\pi}^{\pi}\left(\sin^3x+\sqrt{\pi^2-x^2}\right)\,dx=\underline{\qquad}.
$$
""",
        r"$\dfrac{\pi^3}{2}$",
        r"""
因为 $\sin^3x$ 是奇函数，所以
$$
\int_{-\pi}^{\pi}\sin^3x\,dx=0.
$$
而 $\sqrt{\pi^2-x^2}$ 是偶函数，
$$
\int_{-\pi}^{\pi}\sqrt{\pi^2-x^2}\,dx
=2\int_0^\pi \sqrt{\pi^2-x^2}\,dx.
$$
后者表示半径为 $\pi$ 的四分之一圆面积，因此
$$
\int_0^\pi \sqrt{\pi^2-x^2}\,dx=\frac14\pi^3.
$$
故原积分为
$$
2\cdot\frac14\pi^3=\frac{\pi^3}{2}.
$$
""",
    ),
    q(
        10,
        "fill_blank",
        4,
        "高等数学",
        ["差分方程"],
        "11",
        r"""
差分方程 $y_{t+1}-2y_t=2^t$ 的通解为 $y_t=\underline{\qquad}$。
""",
        r"$A2^t+t2^{t-1}$",
        r"""
对应齐次方程
$$
y_{t+1}-2y_t=0
$$
的通解为
$$
Y_t=A2^t.
$$
设特解为 $y_t^*=kt2^t$，代入原方程得
$$
k(t+1)2^{t+1}-2kt2^t=2^t,
$$
解得
$$
k=\frac12.
$$
因此特解为
$$
y_t^*=t2^{t-1}.
$$
故通解
$$
y_t=A2^t+t2^{t-1}.
$$
""",
    ),
    q(
        11,
        "fill_blank",
        4,
        "高等数学",
        ["导数应用", "平均成本"],
        "11",
        r"""
设生产某产品的平均成本为 $\overline C(Q)=1+e^{-Q}$，其中产量为 $Q$，则边际成本为 $\underline{\qquad}$。
""",
        r"$1+(1-Q)e^{-Q}$",
        r"""
总成本为
$$
C(Q)=Q\overline C(Q)=Q+Qe^{-Q}.
$$
故边际成本
$$
C'(Q)=1+e^{-Q}-Qe^{-Q}=1+(1-Q)e^{-Q}.
$$
""",
    ),
    q(
        12,
        "fill_blank",
        4,
        "高等数学",
        ["全微分", "偏积分"],
        "11",
        r"""
设函数 $f(x,y)$ 具有一阶连续偏导数，且
$$
df(x,y)=ye^y\,dx+x(1+y)e^y\,dy,\qquad f(0,0)=0,
$$
则
$$
f(x,y)=\underline{\qquad}.
$$
""",
        r"$xye^y$",
        r"""
由全微分可知
$$
f_x'(x,y)=ye^y,\qquad f_y'(x,y)=x(1+y)e^y.
$$
对 $x$ 积分，
$$
f(x,y)=\int ye^y\,dx=xye^y+C(y).
$$
再对 $y$ 求偏导，
$$
f_y'(x,y)=x(1+y)e^y+C'(y).
$$
与已知比较得
$$
C'(y)=0,
$$
故 $C(y)=C$ 为常数。由 $f(0,0)=0$ 得 $C=0$，于是
$$
f(x,y)=xye^y.
$$
""",
    ),
    q(
        13,
        "fill_blank",
        4,
        "线性代数",
        ["矩阵秩", "线性变换"],
        "11",
        r"""
设矩阵
$$
A=\begin{pmatrix}
1&0&1\\
1&1&2\\
0&1&1
\end{pmatrix},
$$
$\alpha_1,\alpha_2,\alpha_3$ 为线性无关的 $3$ 维列向量组，则向量组 $A\alpha_1,A\alpha_2,A\alpha_3$ 的秩为 $\underline{\qquad}$。
""",
        r"$2$",
        r"""
因为
$$
(A\alpha_1,A\alpha_2,A\alpha_3)=A(\alpha_1,\alpha_2,\alpha_3),
$$
且 $(\alpha_1,\alpha_2,\alpha_3)$ 可逆，所以
$$
r(A\alpha_1,A\alpha_2,A\alpha_3)=r(A).
$$
计算可得
$$
r(A)=2.
$$
因此所求秩为 $2$。
""",
    ),
    q(
        14,
        "fill_blank",
        4,
        "概率统计",
        ["离散分布", "数学期望", "方差"],
        "11",
        r"""
设随机变量 $X$ 的概率分布为
$$
P\{X=-2\}=\frac12,\quad P\{X=1\}=a,\quad P\{X=3\}=b,
$$
若 $E(X)=0$，则 $D(X)=\underline{\qquad}$。
""",
        r"$\dfrac92$",
        r"""
由概率和为 $1$，
$$
\frac12+a+b=1.
$$
又由
$$
E(X)=-2\cdot\frac12+a+3b=0,
$$
解得
$$
a=b=\frac14.
$$
于是
$$
E(X^2)=(-2)^2\cdot\frac12+1^2\cdot\frac14+3^2\cdot\frac14=\frac92.
$$
由于 $E(X)=0$，
$$
D(X)=E(X^2)-[E(X)]^2=\frac92.
$$
""",
    ),
    q(
        15,
        "solution",
        10,
        "高等数学",
        ["极限", "积分换元", "洛必达"],
        "11-12",
        r"""
求极限
$$
\lim_{x\to0^+}\frac{\int_0^x \sqrt{x-t}\,e^t\,dt}{\sqrt{x^3}}.
$$
""",
        r"$\dfrac23$",
        r"""
令
$$
u=x-t,
$$
则 $t=x-u,\ dt=-du$，原式分子化为
$$
\int_0^x \sqrt{u}\,e^{x-u}\,du
=e^x\int_0^x \sqrt{u}e^{-u}\,du.
$$
因此原极限等于
$$
\lim_{x\to0^+}\frac{\int_0^x \sqrt{u}e^{-u}\,du}{x^{3/2}}.
$$
这是 $0/0$ 型，应用洛必达法则：
$$
\lim_{x\to0^+}\frac{\sqrt{x}e^{-x}}{\frac32\sqrt{x}}
=\frac23.
$$
""",
    ),
    q(
        16,
        "solution",
        10,
        "高等数学",
        ["二重积分", "广义积分"],
        "11-12",
        r"""
计算积分
$$
\iint_D \frac{y^3}{(1+x^2+y^4)^2}\,dx\,dy,
$$
其中 $D$ 是第一象限中以曲线 $y=\sqrt{x}$ 与 $x$ 轴为边界的无界区域。
""",
        r"$\dfrac{2-\sqrt2}{16}\pi$",
        r"""
区域 $D$ 可表示为
$$
0\le x<+\infty,\qquad 0\le y\le \sqrt{x}.
$$
故
$$
\iint_D \frac{y^3}{(1+x^2+y^4)^2}\,dx\,dy
=\int_0^{+\infty}\!\!dx\int_0^{\sqrt{x}} \frac{y^3}{(1+x^2+y^4)^2}\,dy.
$$
对内层积分令
$$
v=1+x^2+y^4,\qquad dv=4y^3\,dy,
$$
得
$$
\int_0^{\sqrt{x}} \frac{y^3}{(1+x^2+y^4)^2}\,dy
=\frac14\left(\frac1{1+x^2}-\frac1{1+2x^2}\right).
$$
故原式为
$$
\frac14\int_0^{+\infty}\left(\frac1{1+x^2}-\frac1{1+2x^2}\right)\,dx
=\frac14\left(\frac\pi2-\frac{\sqrt2}{2}\cdot\frac\pi2\right)
=\frac{2-\sqrt2}{16}\pi.
$$
""",
    ),
    q(
        17,
        "solution",
        10,
        "高等数学",
        ["定积分", "黎曼和极限"],
        "12",
        r"""
求极限
$$
\lim_{n\to\infty}\sum_{k=1}^n \frac{k}{n^2}\ln\left(1+\frac{k}{n}\right).
$$
""",
        r"$\dfrac14$",
        r"""
将和式写成
$$
\sum_{k=1}^n \frac{k}{n}\ln\left(1+\frac{k}{n}\right)\cdot\frac1n.
$$
它是函数
$$
f(x)=x\ln(1+x)
$$
在 $[0,1]$ 上的黎曼和，因此极限为
$$
\int_0^1 x\ln(1+x)\,dx.
$$
分部积分得
$$
\int_0^1 x\ln(1+x)\,dx
=\frac12x^2\ln(1+x)\Big|_0^1-\frac12\int_0^1 \frac{x^2}{1+x}\,dx.
$$
再将
$$
\frac{x^2}{1+x}=x-1+\frac1{1+x}
$$
代入并计算，得
$$
\int_0^1 x\ln(1+x)\,dx=\frac14.
$$
故极限为 $\dfrac14$。
""",
    ),
    q(
        18,
        "solution",
        10,
        "高等数学",
        ["函数零点", "单调性"],
        "12-13",
        r"""
已知方程
$$
\frac1{\ln(1+x)}-\frac1x=k
$$
在区间 $(0,1)$ 内有实根，确定常数 $k$ 的取值范围。
""",
        r"$\left(\dfrac1{\ln2}-1,\dfrac12\right)$",
        r"""
设
$$
f(x)=\frac1{\ln(1+x)}-\frac1x-k,\qquad x\in(0,1).
$$
先研究
$$
g(x)=(1+x)\ln^2(1+x)-x^2.
$$
由计算可得
$$
f'(x)=\frac{(1+x)\ln^2(1+x)-x^2}{x^2(1+x)\ln^2(1+x)}
=\frac{g(x)}{x^2(1+x)\ln^2(1+x)}.
$$
进一步有
$$
g''(x)=\frac{2[\ln(1+x)-x]}{1+x}<0\qquad (0<x\le1),
$$
故 $g'(x)<g'(0)=0$，从而 $g(x)<g(0)=0$，于是 $f'(x)<0$，即 $f$ 在 $(0,1)$ 上严格递减。

又
$$
\lim_{x\to0^+}f(x)=\frac12-k,\qquad
f(1)=\frac1{\ln2}-1-k.
$$
因为 $f$ 单调递减，方程在 $(0,1)$ 内有实根当且仅当
$$
\frac12-k>0,\qquad \frac1{\ln2}-1-k<0.
$$
故
$$
k\in\left(\frac1{\ln2}-1,\frac12\right).
$$
""",
    ),
    q(
        19,
        "solution",
        10,
        "高等数学",
        ["幂级数", "微分方程", "收敛半径"],
        "12-13",
        r"""
若 $a_0=1,\ a_1=0$，
$$
a_{n+1}=\frac1{n+1}(na_n+a_{n-1})\quad (n=1,2,3,\ldots),
$$
$S(x)$ 为幂级数 $\sum_{n=0}^{\infty}a_nx^n$ 的和函数。

1. 证明 $\sum_{n=0}^{\infty}a_nx^n$ 的收敛半径不小于 $1$；  
2. 证明 $(1-x)S'(x)-xS(x)=0\ (x\in(-1,1))$，并求 $S(x)$ 的表达式。
""",
        r"""
1. 收敛半径 $R\ge1$；  
2.
$$
S(x)=\frac{e^{-x}}{1-x}\quad (|x|<1).
$$
""",
        r"""
由递推式及初值可归纳得
$$
0\le a_n\le1\qquad (n\ge0).
$$
因此当 $|x|<1$ 时，
$$
|a_nx^n|\le |x|^n,
$$
而几何级数 $\sum |x|^n$ 收敛，所以原幂级数绝对收敛，故收敛半径满足 $R\ge1$。

由
$$
S(x)=\sum_{n=0}^{\infty}a_nx^n
$$
可得
$$
S'(x)=\sum_{n=1}^{\infty}na_nx^{n-1}
=\sum_{n=0}^{\infty}(n+1)a_{n+1}x^n.
$$
于是
$$
(1-x)S'(x)-xS(x)
=a_1+\sum_{n=1}^{\infty}\bigl[(n+1)a_{n+1}-na_n-a_{n-1}\bigr]x^n
=0,
$$
因为递推式恰好使每一项系数为零。

所以
$$
(1-x)S'(x)-xS(x)=0,
$$
解该微分方程得
$$
\frac{S'(x)}{S(x)}=\frac{x}{1-x},
$$
从而
$$
S(x)=\frac{Ce^{-x}}{1-x}.
$$
再由 $S(0)=a_0=1$ 得 $C=1$，故
$$
S(x)=\frac{e^{-x}}{1-x}.
$$
""",
    ),
    q(
        20,
        "solution",
        11,
        "线性代数",
        ["矩阵秩", "特征值", "线性方程组"],
        "12-13",
        r"""
设 $3$ 阶矩阵 $A=(\alpha_1,\alpha_2,\alpha_3)$ 有 $3$ 个不同的特征值，且 $\alpha_3=\alpha_1+2\alpha_2$。

1. 证明 $r(A)=2$；  
2. 若 $\beta=\alpha_1+\alpha_2+\alpha_3$，求方程组 $Ax=\beta$ 的通解。
""",
        r"""
1. $r(A)=2$；  
2.
$$
x=\begin{pmatrix}1\\1\\1\end{pmatrix}
+k\begin{pmatrix}1\\2\\-1\end{pmatrix},
\quad k\in\mathbb R.
$$
""",
        r"""
由 $\alpha_3=\alpha_1+2\alpha_2$ 知列向量线性相关，所以
$$
r(A)\le2.
$$
又因为 $A$ 有三个不同特征值，所以至少有两个非零特征值，从而
$$
r(A)\ge2.
$$
故
$$
r(A)=2.
$$

由关系
$$
\alpha_1+2\alpha_2-\alpha_3=0
$$
知
$$
A\begin{pmatrix}1\\2\\-1\end{pmatrix}=0,
$$
所以 $\begin{pmatrix}1\\2\\-1\end{pmatrix}$ 是齐次方程 $Ax=0$ 的基础解系。

又
$$
\beta=\alpha_1+\alpha_2+\alpha_3
=A\begin{pmatrix}1\\1\\1\end{pmatrix},
$$
故
$$
\begin{pmatrix}1\\1\\1\end{pmatrix}
$$
是非齐次方程 $Ax=\beta$ 的一个特解。

因此通解为
$$
x=\begin{pmatrix}1\\1\\1\end{pmatrix}
+k\begin{pmatrix}1\\2\\-1\end{pmatrix},\quad k\in\mathbb R.
$$
""",
    ),
    q(
        21,
        "solution",
        11,
        "线性代数",
        ["二次型", "正交变换", "特征值分解"],
        "13",
        r"""
设二次型
$$
f(x_1,x_2,x_3)=2x_1^2-x_2^2+ax_3^2+2x_1x_2-8x_1x_3+2x_2x_3
$$
在正交变换 $x=Qy$ 下的标准形为
$$
\lambda_1y_1^2+\lambda_2y_2^2,
$$
求 $a$ 的值及一个正交矩阵 $Q$。
""",
        r"""
$$
a=2,
$$
可取
$$
Q=
\begin{pmatrix}
\dfrac1{\sqrt3} & -\dfrac1{\sqrt2} & \dfrac1{\sqrt6}\\[6pt]
-\dfrac1{\sqrt3} & 0 & \dfrac2{\sqrt6}\\[6pt]
\dfrac1{\sqrt3} & \dfrac1{\sqrt2} & \dfrac1{\sqrt6}
\end{pmatrix}.
$$
""",
        r"""
二次型对应的对称矩阵为
$$
A=
\begin{pmatrix}
2&1&-4\\
1&-1&1\\
-4&1&a
\end{pmatrix}.
$$
题设标准形只有两个平方项，故有一个特征值为 $0$，即
$$
|A|=0.
$$
计算得
$$
|A|=6-3a,
$$
因此
$$
a=2.
$$

此时特征多项式可分解为
$$
|\lambda E-A|=\lambda(\lambda+3)(\lambda-6),
$$
故特征值为 $-3,6,0$。

对应单位特征向量可取
$$
\beta_1=\frac1{\sqrt3}(1,-1,1)^T,\quad
\beta_2=\frac1{\sqrt2}(-1,0,1)^T,\quad
\beta_3=\frac1{\sqrt6}(1,2,1)^T.
$$
于是取
$$
Q=(\beta_1,\beta_2,\beta_3)
$$
即可得到所求正交变换。
""",
    ),
    q(
        22,
        "solution",
        11,
        "概率统计",
        ["连续型随机变量", "卷积"],
        "13-14",
        r"""
设随机变量 $X,Y$ 相互独立，且 $X$ 的概率分布为
$$
P\{X=0\}=P\{X=2\}=\frac12,
$$
$Y$ 的概率密度为
$$
f(y)=
\begin{cases}
2y, & 0<y<1,\\
0, & \text{其他}.
\end{cases}
$$

1. 求 $P\{Y\le E(Y)\}$；  
2. 求 $Z=X+Y$ 的概率密度。
""",
        r"""
$$
P\{Y\le E(Y)\}=\frac49.
$$

$$
f_Z(z)=
\begin{cases}
z, & 0<z<1,\\
z-2, & 2<z<3,\\
0, & \text{其他}.
\end{cases}
$$
""",
        r"""
先求
$$
E(Y)=\int_0^1 y\cdot 2y\,dy=\frac23.
$$
因此
$$
P\{Y\le E(Y)\}=P\left\{Y\le\frac23\right\}
=\int_0^{2/3}2y\,dy=\frac49.
$$

设 $F_Z(z)=P(Z\le z)$，则由全概率公式
$$
F_Z(z)=\frac12P(Y\le z)+\frac12P(Y\le z-2).
$$
分段计算：

当 $z<0$ 时，$F_Z(z)=0$；

当 $0\le z<1$ 时，
$$
F_Z(z)=\frac12\int_0^z 2y\,dy=\frac{z^2}{2};
$$

当 $1\le z<2$ 时，$F_Z(z)=\dfrac12$；

当 $2\le z<3$ 时，
$$
F_Z(z)=\frac12+\frac12\int_0^{z-2}2y\,dy
=\frac12+\frac{(z-2)^2}{2};
$$

当 $z\ge3$ 时，$F_Z(z)=1$。

对各段求导，得
$$
f_Z(z)=
\begin{cases}
z, & 0<z<1,\\
z-2, & 2<z<3,\\
0, & \text{其他}.
\end{cases}
$$
""",
    ),
    q(
        23,
        "solution",
        11,
        "概率统计",
        ["正态分布", "矩估计", "极大似然估计"],
        "13-14",
        r"""
某工程师为了了解一台天平的精度，用该天平对一物体的质量做 $n$ 次测量，该物体的质量 $\mu$ 是已知的，设 $n$ 次测量结果 $X_1,X_2,\ldots,X_n$ 相互独立且均服从正态分布 $N(\mu,\sigma^2)$。该工程师记录的是 $n$ 次测量的绝对误差
$$
Z_i=|X_i-\mu|\quad (i=1,2,\ldots,n),
$$
利用 $Z_1,Z_2,\ldots,Z_n$ 估计 $\sigma$。

1. 求 $Z_1$ 的概率密度；  
2. 利用一阶矩求 $\sigma$ 的矩估计量；  
3. 求 $\sigma$ 的最大似然估计量。
""",
        r"""
1.
$$
f_{Z_1}(z)=
\begin{cases}
\dfrac{2}{\sqrt{2\pi}\sigma}e^{-z^2/(2\sigma^2)}, & z\ge0,\\
0, & z<0;
\end{cases}
$$
2.
$$
\hat\sigma_{\text{矩}}=\frac{\sqrt{2\pi}}{2}\,\overline Z;
$$
3.
$$
\hat\sigma_{\text{MLE}}=\sqrt{\frac1n\sum_{i=1}^n Z_i^2}.
$$
""",
        r"""
因为
$$
X_1-\mu\sim N(0,\sigma^2),
$$
故
$$
Z_1=|X_1-\mu|
$$
服从半正态分布，其分布函数为
$$
F(z)=P(Z_1\le z)=P(|X_1-\mu|\le z)
=
\begin{cases}
2\Phi\!\left(\dfrac z\sigma\right)-1, & z\ge0,\\[6pt]
0, & z<0.
\end{cases}
$$
故概率密度为
$$
f_{Z_1}(z)=
\begin{cases}
\dfrac{2}{\sqrt{2\pi}\sigma}e^{-z^2/(2\sigma^2)}, & z\ge0,\\
0, & z<0.
\end{cases}
$$

又
$$
EZ_1=\int_0^{+\infty} z\cdot \frac{2}{\sqrt{2\pi}\sigma}e^{-z^2/(2\sigma^2)}\,dz
=\frac{2}{\sqrt{2\pi}}\sigma.
$$
令样本一阶矩
$$
\overline Z=\frac1n\sum_{i=1}^n Z_i
$$
等于理论一阶矩，可得矩估计
$$
\hat\sigma_{\text{矩}}=\frac{\sqrt{2\pi}}{2}\,\overline Z.
$$

对观测值 $z_1,\ldots,z_n$，似然函数为
$$
L(\sigma)=\prod_{i=1}^n \frac{2}{\sqrt{2\pi}\sigma}e^{-z_i^2/(2\sigma^2)}
=\left(\frac{2}{\sqrt{2\pi}}\right)^n \sigma^{-n}
e^{-\frac1{2\sigma^2}\sum_{i=1}^n z_i^2}.
$$
其对数似然为
$$
\ln L(\sigma)=n\ln\frac{2}{\sqrt{2\pi}}-n\ln\sigma-\frac1{2\sigma^2}\sum_{i=1}^n z_i^2.
$$
求导并令其为零：
$$
-\frac n\sigma+\frac1{\sigma^3}\sum_{i=1}^n z_i^2=0.
$$
解得
$$
\hat\sigma_{\text{MLE}}=\sqrt{\frac1n\sum_{i=1}^n Z_i^2}.
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
