from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


YEAR = 2021
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
        ["无穷小比较", "定积分", "Taylor 展开"],
        r"""
当 $x\to0$ 时，
$$
\int_0^{x^2}(e^{t^3}-1)\,dt
$$
是 $x^7$ 的（ ）

A. 低阶无穷小  
B. 等价无穷小  
C. 高阶无穷小  
D. 同阶但非等价无穷小
""",
        r"C",
        r"""
当 $t\to0$ 时，
$$
e^{t^3}-1\sim t^3.
$$
因此
$$
\int_0^{x^2}(e^{t^3}-1)\,dt
\sim \int_0^{x^2} t^3\,dt
=\frac{x^8}{4}.
$$
所以它与 $x^7$ 相比满足
$$
\frac{x^8/4}{x^7}=\frac x4\to0,
$$
故它是 $x^7$ 的高阶无穷小，选 **C**。
""",
    ),
    q(
        2,
        "single_choice",
        5,
        "高等数学",
        ["连续", "可导", "极值"],
        r"""
设
$$
f(x)=
\begin{cases}
\dfrac{e^x-1}{x},& x\ne0,\\[4pt]
1,& x=0,
\end{cases}
$$
则 $f(x)$ 在 $x=0$ 处（ ）

A. 连续且取得极大值  
B. 连续且取得极小值  
C. 可导且导数为零  
D. 可导且导数不为零
""",
        r"D",
        r"""
先看连续性：
$$
\lim_{x\to0}\frac{e^x-1}{x}=1=f(0),
$$
所以连续。

再求导数。由展开
$$
e^x-1=x+\frac{x^2}{2}+o(x^2),
$$
得
$$
\frac{e^x-1}{x}=1+\frac x2+o(x).
$$
因此
$$
f'(0)=\lim_{x\to0}\frac{f(x)-f(0)}x=\frac12\ne0.
$$
故选 **D**。
""",
    ),
    q(
        3,
        "single_choice",
        5,
        "高等数学",
        ["函数零点", "极值", "参数范围"],
        r"""
函数
$$
f(x)=ax-b\ln x\qquad (a>0)
$$
有 2 个零点，则 $\dfrac ba$ 的取值范围是（ ）

A. $(e,+\infty)$  
B. $(0,e)$  
C. $\left(0,\dfrac1e\right)$  
D. $\left(\dfrac1e,+\infty\right)$
""",
        r"A",
        r"""
令
$$
f'(x)=a-\frac bx.
$$
若有两个零点，则函数先降后升，故必须有唯一极小值点
$$
x_0=\frac ba>0.
$$

在该点
$$
f(x_0)=a\cdot \frac ba-b\ln\frac ba
=b\left(1-\ln\frac ba\right).
$$
要有两个零点，极小值必须小于 0，即
$$
1-\ln\frac ba<0
\iff \ln\frac ba>1
\iff \frac ba>e.
$$
故选 **A**。
""",
    ),
    q(
        4,
        "single_choice",
        5,
        "高等数学",
        ["全微分", "复合函数", "偏导数"],
        r"""
设函数 $f(u,v)$ 可微，且
$$
f(x+1,e^x)=x(x+1)^2,\qquad f(x,x^2)=2x^2\ln x,
$$
则 $df(1,1)=$（ ）

A. $dx+dy$  
B. $dx-dy$  
C. $dy$  
D. $-dy$
""",
        r"C",
        r"""
由
$$
u=x+1,\quad v=e^x
$$
当 $x=0$ 时对应 $(u,v)=(1,1)$。

设
$$
g(x)=f(x+1,e^x)=x(x+1)^2,
$$
则
$$
g'(0)=f_u(1,1)\cdot1+f_v(1,1)\cdot1=1.
$$

再由
$$
h(x)=f(x,x^2)=2x^2\ln x,
$$
当 $x=1$ 时也对应 $(1,1)$。有
$$
h'(1)=f_u(1,1)+2f_v(1,1)=2.
$$

联立
$$
\begin{cases}
f_u+f_v=1,\\
f_u+2f_v=2,
\end{cases}
$$
解得
$$
f_u(1,1)=0,\qquad f_v(1,1)=1.
$$
所以
$$
df(1,1)=f_u\,dx+f_v\,dy=dy.
$$
故选 **C**。
""",
    ),
    q(
        5,
        "single_choice",
        5,
        "线性代数",
        ["二次型", "惯性指数"],
        r"""
二次型
$$
f(x_1,x_2,x_3)=(x_1+x_2)^2+(x_2+x_3)^2-(x_3-x_1)^2
$$
的正惯性指数和负惯性指数分别为（ ）

A. $2,0$  
B. $1,1$  
C. $2,1$  
D. $1,2$
""",
        r"B",
        r"""
展开得
$$
f=2x_2^2+2x_1x_2+2x_2x_3+2x_1x_3.
$$
对应对称矩阵为
$$
A=
\begin{pmatrix}
0&1&1\\
1&2&1\\
1&1&0
\end{pmatrix}.
$$

计算其特征值可得
$$
\lambda_1=3,\qquad \lambda_2=-1,\qquad \lambda_3=0.
$$
因此正惯性指数为 1，负惯性指数为 1，故选 **B**。
""",
    ),
    q(
        6,
        "single_choice",
        5,
        "线性代数",
        ["正交矩阵", "线性方程组"],
        r"""
设 $A=(\alpha_1,\alpha_2,\alpha_3,\alpha_4)$ 为 4 阶正交矩阵，若
$$
B=
\begin{pmatrix}
\alpha_1^T\\
\alpha_2^T\\
\alpha_3^T
\end{pmatrix},\qquad
\beta=
\begin{pmatrix}
1\\1\\1
\end{pmatrix},
$$
$k$ 表示任意常数，则线性方程组 $Ax=\beta$ 的通解为（ ）

A. $\alpha_2+\alpha_3+\alpha_4+k\alpha_1$  
B. $\alpha_1+\alpha_3+\alpha_4+k\alpha_2$  
C. $\alpha_1+\alpha_2+\alpha_4+k\alpha_3$  
D. $\alpha_1+\alpha_2+\alpha_3+k\alpha_4$
""",
        r"D",
        r"""
因为 $A$ 为正交矩阵，列向量 $\alpha_i$ 构成标准正交基，且
$$
B x=
\begin{pmatrix}
\alpha_1^Tx\\
\alpha_2^Tx\\
\alpha_3^Tx
\end{pmatrix}
=
\begin{pmatrix}
1\\1\\1
\end{pmatrix}.
$$
所以
$$
\alpha_1^Tx=\alpha_2^Tx=\alpha_3^Tx=1.
$$

将 $x$ 在正交基下展开：
$$
x=c_1\alpha_1+c_2\alpha_2+c_3\alpha_3+c_4\alpha_4.
$$
则立刻得到
$$
c_1=c_2=c_3=1,\qquad c_4=k.
$$
故
$$
x=\alpha_1+\alpha_2+\alpha_3+k\alpha_4.
$$
选 **D**。
""",
    ),
    q(
        7,
        "single_choice",
        5,
        "线性代数",
        ["矩阵分解", "初等变换"],
        r"""
已知
$$
A=
\begin{pmatrix}
1&0&1\\
2&-1&1\\
-1&2&-5
\end{pmatrix},
$$
若三角可逆矩阵 $P$ 和上三角可逆矩阵 $Q$ 使得 $PAQ$ 为对角矩阵，则 $P,Q$ 分别取（ ）

A.
$$
P=
\begin{pmatrix}
1&0&0\\
0&1&0\\
0&0&1
\end{pmatrix},
\quad
Q=
\begin{pmatrix}
1&0&1\\
0&1&3\\
0&0&1
\end{pmatrix}
$$

B.
$$
P=
\begin{pmatrix}
1&0&0\\
2&-1&0\\
-3&2&1
\end{pmatrix},
\quad
Q=
\begin{pmatrix}
1&0&0\\
0&1&0\\
0&0&1
\end{pmatrix}
$$

C.
$$
P=
\begin{pmatrix}
1&0&0\\
2&-1&0\\
-3&2&1
\end{pmatrix},
\quad
Q=
\begin{pmatrix}
1&0&1\\
0&1&3\\
0&0&1
\end{pmatrix}
$$

D.
$$
P=
\begin{pmatrix}
1&0&0\\
0&1&0\\
1&3&1
\end{pmatrix},
\quad
Q=
\begin{pmatrix}
1&2&-3\\
0&-1&2\\
0&0&1
\end{pmatrix}
$$
""",
        r"C",
        r"""
对矩阵 $A$ 做行初等变换与列初等变换，使之化为对角矩阵。对应地，左乘下三角可逆矩阵 $P$，右乘上三角可逆矩阵 $Q$。

按原题给出的四组选项逐一代入检查，可发现只有 **C** 所给的 $P,Q$ 能把 $A$ 化为对角矩阵。

因此选 **C**。
""",
    ),
    q(
        8,
        "single_choice",
        5,
        "概率统计",
        ["条件概率", "命题判断"],
        r"""
设 $A,B$ 为随机事件，且 $0<P(B)<1$，下列命题中为假命题的是（ ）

A. 若 $P(A\mid B)=P(A)$，则 $P(A\mid \bar B)=P(A)$  
B. 若 $P(A\mid B)>P(A)$，则 $P(\bar A\mid B)>P(\bar A)$  
C. 若 $P(A\mid B)>P(A\mid \bar B)$，则 $P(A\mid B)>P(A)$  
D. 若 $P(A\mid A\cup B)>P(\bar A\mid A\cup B)$，则 $P(A)>P(B)$
""",
        r"D",
        r"""
A：由全概率公式
$$
P(A)=P(A|B)P(B)+P(A|\bar B)P(\bar B)
$$
可知成立。  

B：由
$$
P(\bar A|B)=1-P(A|B),\qquad P(\bar A)=1-P(A)
$$
可知与题设矛盾方向相反，因此仍成立。  

C：若
$$
P(A|B)>P(A|\bar B),
$$
则
$$
P(A)=P(A|B)P(B)+P(A|\bar B)P(\bar B)
$$
是两者的加权平均，故必有 $P(A|B)>P(A)$。  

D 不一定成立，构造反例即可否定，所以假命题为 **D**。
""",
    ),
    q(
        9,
        "single_choice",
        5,
        "概率统计",
        ["点估计", "均值方差", "协方差"],
        r"""
设 $(X_1,Y_1),(X_2,Y_2),\ldots,(X_n,Y_n)$ 为来自总体
$$
N(\mu_1,\mu_2;\sigma_1^2,\sigma_2^2;\rho)
$$
的简单随机样本。令
$$
\theta=\mu_1-\mu_2,\qquad
\bar X=\frac1n\sum_{i=1}^nX_i,\qquad
\bar Y=\frac1n\sum_{i=1}^nY_i,\qquad
\hat\theta=\bar X-\bar Y,
$$
则（ ）

A. $E(\hat\theta)=\theta,\ D(\hat\theta)=\dfrac{\sigma_1^2+\sigma_2^2}{n}$  
B. $E(\hat\theta)=\theta,\ D(\hat\theta)=\dfrac{\sigma_1^2+\sigma_2^2-2\rho\sigma_1\sigma_2}{n}$  
C. $E(\hat\theta)\ne\theta,\ D(\hat\theta)=\dfrac{\sigma_1^2+\sigma_2^2}{n}$  
D. $E(\hat\theta)\ne\theta,\ D(\hat\theta)=\dfrac{\sigma_1^2+\sigma_2^2-2\rho\sigma_1\sigma_2}{n}$
""",
        r"B",
        r"""
显然
$$
E(\bar X)=\mu_1,\qquad E(\bar Y)=\mu_2,
$$
所以
$$
E(\hat\theta)=E(\bar X-\bar Y)=\mu_1-\mu_2=\theta.
$$

又
$$
D(\bar X)=\frac{\sigma_1^2}{n},\qquad
D(\bar Y)=\frac{\sigma_2^2}{n},\qquad
\operatorname{Cov}(\bar X,\bar Y)=\frac{\rho\sigma_1\sigma_2}{n}.
$$
因此
$$
D(\hat\theta)=D(\bar X-\bar Y)
=\frac{\sigma_1^2+\sigma_2^2-2\rho\sigma_1\sigma_2}{n}.
$$
故选 **B**。
""",
    ),
    q(
        10,
        "single_choice",
        5,
        "概率统计",
        ["最大似然估计", "离散分布"],
        r"""
总体 $X$ 的概率分布为
$$
P\{X=1\}=\frac{1-\theta}{2},\qquad
P\{X=2\}=P\{X=3\}=\frac{1+\theta}{4}.
$$
利用来自总体 $X$ 的样本观察值
$$
1,3,2,2,1,3,1,2
$$
可得 $\theta$ 的最大似然估计值为（ ）

A. $\dfrac14$  
B. $\dfrac38$  
C. $\dfrac12$  
D. $\dfrac58$
""",
        r"A",
        r"""
样本中取值 1 出现 3 次，取值 2 或 3 共出现 5 次。

似然函数为
$$
L(\theta)=\left(\frac{1-\theta}{2}\right)^3\left(\frac{1+\theta}{4}\right)^5.
$$
取对数：
$$
\ln L(\theta)=3\ln(1-\theta)+5\ln(1+\theta)+C.
$$
求导并令其为零：
$$
\frac{-3}{1-\theta}+\frac{5}{1+\theta}=0.
$$
解得
$$
5(1-\theta)=3(1+\theta)\iff 2=8\theta\iff \theta=\frac14.
$$
故选 **A**。
""",
    ),
    q(
        11,
        "fill_blank",
        5,
        "高等数学",
        ["导数", "链式法则"],
        r"""
若
$$
y=\cos e^{-\sqrt x},
$$
则
$$
\left.\frac{dy}{dx}\right|_{x=1}=\underline{\qquad}.
$$
""",
        r"$\dfrac{\sin e^{-1}}{2e}$",
        r"""
设
$$
u=e^{-\sqrt x},
$$
则
$$
y=\cos u,\qquad \frac{dy}{dx}=-\sin u\cdot \frac{du}{dx}.
$$
又
$$
\frac{du}{dx}=e^{-\sqrt x}\cdot\left(-\frac1{2\sqrt x}\right).
$$
所以
$$
\frac{dy}{dx}=\sin(e^{-\sqrt x})\frac{e^{-\sqrt x}}{2\sqrt x}.
$$
代入 $x=1$ 得
$$
\left.\frac{dy}{dx}\right|_{x=1}=\frac{\sin e^{-1}}{2e}.
$$
""",
    ),
    q(
        12,
        "fill_blank",
        5,
        "高等数学",
        ["定积分", "换元"],
        r"""
计算
$$
\int_{\sqrt5}^{5}\frac{x}{\sqrt{|x^2-9|}}\,dx=\underline{\qquad}.
$$
""",
        r"$6$",
        r"""
因为积分区间分成 $(\sqrt5,3)$ 与 $(3,5)$ 两段，分别有
$$
|x^2-9|=
\begin{cases}
9-x^2,& \sqrt5\le x<3,\\
x^2-9,& 3<x\le5.
\end{cases}
$$

因此
$$
\int_{\sqrt5}^{5}\frac{x}{\sqrt{|x^2-9|}}\,dx
=\int_{\sqrt5}^{3}\frac{x}{\sqrt{9-x^2}}\,dx+\int_{3}^{5}\frac{x}{\sqrt{x^2-9}}\,dx.
$$
两项都用换元 $u=9-x^2$ 或 $u=x^2-9$ 即可，分别得到 2 与 4，总和为
$$
6.
$$
""",
    ),
    q(
        13,
        "fill_blank",
        5,
        "高等数学",
        ["旋转体体积", "定积分"],
        r"""
设 $D$ 由
$$
y=\sqrt x\sin\pi x\qquad (0\le x\le1)
$$
与 $x$ 轴围成，则 $D$ 绕 $x$ 轴旋转的旋转体体积为
$$
\underline{\qquad}.
$$
""",
        r"$\dfrac{\pi}{4}$",
        r"""
旋转体体积公式：
$$
V=\pi\int_0^1 y^2\,dx.
$$
代入
$$
y=\sqrt x\sin\pi x
$$
得
$$
V=\pi\int_0^1 x\sin^2(\pi x)\,dx.
$$
利用
$$
\sin^2(\pi x)=\frac{1-\cos 2\pi x}{2},
$$
可算得
$$
\int_0^1 x\sin^2(\pi x)\,dx=\frac14.
$$
故
$$
V=\frac{\pi}{4}.
$$
""",
    ),
    q(
        14,
        "fill_blank",
        5,
        "高等数学",
        ["差分方程"],
        r"""
差分方程
$$
\Delta y_t=t
$$
的通解为
$$
\underline{\qquad}.
$$
""",
        r"$\dfrac12 t^2-\dfrac12 t+c$",
        r"""
由
$$
\Delta y_t=y_{t+1}-y_t=t.
$$
设通解为二次多项式
$$
y_t=At^2+Bt+C.
$$
则
$$
y_{t+1}-y_t=A[(t+1)^2-t^2]+B[(t+1)-t]=2At+A+B.
$$
与 $t$ 对比系数得
$$
2A=1,\qquad A+B=0.
$$
故
$$
A=\frac12,\qquad B=-\frac12.
$$
所以通解为
$$
y_t=\frac12 t^2-\frac12 t+c.
$$
""",
    ),
    q(
        15,
        "fill_blank",
        5,
        "线性代数",
        ["行列式", "多项式系数"],
        r"""
多项式
$$
f(x)=
\begin{vmatrix}
x&x&1&2x\\
1&x&2&-1\\
2&1&x&1\\
2&-1&1&x
\end{vmatrix}
$$
的 $x^3$ 项的系数为
$$
\underline{\qquad}.
$$
""",
        r"$-5$",
        r"""
行列式按关于 $x$ 的多项式展开。$x^3$ 项来自从四行四列中恰好取三个含 $x$ 的元素、另一个取常数项的情形。

直接按行列式多线性展开，或借助按列分拆后收集三次项，可得该系数为
$$
-5.
$$
""",
    ),
    q(
        16,
        "fill_blank",
        5,
        "概率统计",
        ["相关系数", "条件分布"],
        r"""
甲乙中各装 2 红 2 白球，从甲盆中任取一球，观察颜色放入乙盆，再从乙盆中任取一球。令 $X,Y$ 分别为从甲乙两盆中取得红球的个数，则
$$
\rho_{XY}=\underline{\qquad}.
$$
""",
        r"$\dfrac15$",
        r"""
$X$ 只取 0 或 1，且
$$
P(X=1)=P(X=0)=\frac12.
$$

若 $X=1$，则乙盆变成 3 红 2 白，所以
$$
P(Y=1\mid X=1)=\frac35;
$$
若 $X=0$，则乙盆变成 2 红 3 白，所以
$$
P(Y=1\mid X=0)=\frac25.
$$

由此算得
$$
E(X)=E(Y)=\frac12,\qquad E(XY)=\frac12\cdot\frac35=\frac3{10}.
$$
所以
$$
\operatorname{Cov}(X,Y)=E(XY)-E(X)E(Y)=\frac3{10}-\frac14=\frac1{20}.
$$

又
$$
D(X)=D(Y)=\frac14,
$$
故
$$
\rho_{XY}=\frac{1/20}{\sqrt{(1/4)(1/4)}}=\frac15.
$$
""",
    ),
    q(
        17,
        "solution",
        10,
        "高等数学",
        ["极限", "左右极限", "参数求值"],
        r"""
已知
$$
\lim_{x\to0}\left[a\arctan\frac1x+(1+|x|)^{1/x}\right]
$$
存在，求 $a$ 的值。
""",
        r"$a=\dfrac{e^{-1}-e}{\pi}$",
        r"""
分别考察左右极限。

当 $x\to0^+$ 时，
$$
\arctan\frac1x\to\frac\pi2,\qquad (1+x)^{1/x}\to e,
$$
所以
$$
\lim_{x\to0^+}\left[a\arctan\frac1x+(1+|x|)^{1/x}\right]=\frac\pi2 a+e.
$$

当 $x\to0^-$ 时，
$$
\arctan\frac1x\to-\frac\pi2,\qquad (1-|x|)^{1/x}=(1-x)^{-1/x}\to e^{-1},
$$
所以
$$
\lim_{x\to0^-}\left[a\arctan\frac1x+(1+|x|)^{1/x}\right]=-\frac\pi2 a+e^{-1}.
$$

极限存在需左右极限相等：
$$
\frac\pi2 a+e=-\frac\pi2 a+e^{-1}.
$$
解得
$$
a=\frac{e^{-1}-e}{\pi}.
$$
""",
    ),
    q(
        18,
        "solution",
        12,
        "高等数学",
        ["多元函数极值"],
        r"""
求函数
$$
f(x,y)=2\ln|x|+\frac{(x-1)^2+y^2}{2x^2}
$$
的极值。
""",
        r"""
极小值点为 $(-1,0)$ 与 $\left(\dfrac12,0\right)$；

对应极小值分别为
$$
f(-1,0)=2,\qquad f\!\left(\frac12,0\right)=\frac12-2\ln2.
$$
""",
        r"""
先求一阶偏导：
$$
f_x(x,y)=\frac{2x^2+x-1-y^2}{x^3},\qquad
f_y(x,y)=\frac{y}{x^2}.
$$
令其为 0，得
$$
y=0,\qquad 2x^2+x-1=0.
$$
解得驻点
$$
(-1,0),\qquad \left(\frac12,0\right).
$$

再求二阶偏导：
$$
f_{xx}=\frac{-2x^2-2x+3+3y^2}{x^4},\qquad
f_{xy}=-\frac{2y}{x^3},\qquad
f_{yy}=\frac1{x^2}.
$$

在 $(-1,0)$ 处，
$$
A=f_{xx}=3,\quad B=f_{xy}=0,\quad C=f_{yy}=1,
$$
有
$$
A>0,\quad AC-B^2>0,
$$
故为极小值点，且
$$
f(-1,0)=2.
$$

在 $\left(\frac12,0\right)$ 处，
$$
A=24,\quad B=0,\quad C=4,
$$
同样满足
$$
A>0,\quad AC-B^2>0,
$$
故也为极小值点，且
$$
f\!\left(\frac12,0\right)=\frac12-2\ln2.
$$
""",
    ),
    q(
        19,
        "solution",
        12,
        "高等数学",
        ["二重积分", "极坐标"],
        r"""
设有界区域 $D$ 是圆 $x^2+y^2=1$ 和直线 $y=x$ 以及 $x$ 轴在第一象限围成的部分，计算二重积分
$$
\iint_D e^{(x+y)^2}(x^2-y^2)\,dx\,dy.
$$
""",
        r"$\dfrac18(e-1)^2$",
        r"""
区域 $D$ 在极坐标下为
$$
0\le r\le1,\qquad 0\le \theta\le\frac\pi4.
$$

又
$$
x=r\cos\theta,\qquad y=r\sin\theta,
$$
所以
$$
(x+y)^2=r^2(\cos\theta+\sin\theta)^2=r^2(1+\sin2\theta),
$$
且
$$
x^2-y^2=r^2(\cos^2\theta-\sin^2\theta)=r^2\cos2\theta.
$$

因此原积分化为
$$
\int_0^{\pi/4}\int_0^1 e^{r^2(1+\sin2\theta)}r^3\cos2\theta\,dr\,d\theta.
$$
交换积分次序并对 $\theta$ 积分，可得
$$
\int_0^1 \frac r2\int_0^{\pi/4} e^{r^2(1+\sin2\theta)}\,d(\sin2\theta)\,dr
=\frac12\int_0^1 r(e^{2r^2}-e^{r^2})\,dr.
$$

再积分得
$$
\frac12\left[\frac14e^{2r^2}-\frac12e^{r^2}\right]_0^1
=\frac18(e-1)^2.
$$
""",
    ),
    q(
        20,
        "solution",
        12,
        "高等数学",
        ["微分方程", "幂级数"],
        r"""
设 $n$ 为正整数，$y=y_n(x)$ 是微分方程
$$
xy'-(n+1)y=0
$$
满足条件
$$
y_n(1)=\frac1{n(n+1)}
$$
的解。

1. 求 $y_n(x)$；  
2. 求级数
$$
\sum_{n=1}^{\infty}y_n(x)
$$
的收敛域及和函数。
""",
        r"""
$$
y_n(x)=\frac{x^{n+1}}{n(n+1)};
$$

收敛域为 $[-1,1]$；

和函数为
$$
S(x)=
\begin{cases}
x+(1-x)\ln(1-x),& -1\le x<1,\\
1,& x=1.
\end{cases}
$$
""",
        r"""
1. 由方程
$$
xy'-(n+1)y=0
$$
得
$$
\frac{y'}y=\frac{n+1}{x}.
$$
积分得
$$
\ln|y|=(n+1)\ln|x|+C,
$$
即
$$
y=Cx^{n+1}.
$$
利用条件
$$
y_n(1)=\frac1{n(n+1)}
$$
得
$$
C=\frac1{n(n+1)}.
$$
所以
$$
y_n(x)=\frac{x^{n+1}}{n(n+1)}.
$$

2. 于是
$$
\sum_{n=1}^{\infty}y_n(x)=\sum_{n=1}^{\infty}\frac{x^{n+1}}{n(n+1)}.
$$
比值法知收敛半径为 1。端点上：
$$
x=1:\ \sum\frac1{n(n+1)} \text{ 收敛},\qquad
x=-1:\ \sum\frac{(-1)^{n+1}}{n(n+1)} \text{ 收敛}.
$$
故收敛域为
$$
[-1,1].
$$

设和函数为 $S(x)$，则
$$
S(x)=\sum_{n=1}^{\infty}\left(\frac1n-\frac1{n+1}\right)x^{n+1}
=x\sum_{n=1}^{\infty}\frac{x^n}{n}-\sum_{n=1}^{\infty}\frac{x^{n+1}}{n+1}.
$$
利用
$$
\sum_{n=1}^{\infty}\frac{x^n}{n}=-\ln(1-x)\qquad (|x|<1),
$$
化简得
$$
S(x)=x+(1-x)\ln(1-x)\qquad (-1\le x<1).
$$
再由
$$
S(1)=\sum_{n=1}^{\infty}\frac1{n(n+1)}=1,
$$
得到
$$
S(x)=
\begin{cases}
x+(1-x)\ln(1-x),& -1\le x<1,\\
1,& x=1.
\end{cases}
$$
""",
    ),
    q(
        21,
        "solution",
        12,
        "线性代数",
        ["特征值", "相似对角化"],
        r"""
设矩阵
$$
A=
\begin{pmatrix}
2&1&0\\
1&2&0\\
1&a&b
\end{pmatrix}
$$
仅有两个不同特征值，若 $A$ 相似于对角矩阵，求 $a,b$；并求逆矩阵 $P$，使得
$$
P^{-1}AP=\Lambda.
$$
""",
        r"""
两种情形：

1. $b=1,\ a=1$，可取
$$
P=
\begin{pmatrix}
-1&0&1\\
1&0&1\\
0&1&1
\end{pmatrix},
\quad
\Lambda=\operatorname{diag}(1,1,3).
$$

2. $b=3,\ a=-1$，可取
$$
P=
\begin{pmatrix}
-1&1&0\\
1&1&0\\
1&0&1
\end{pmatrix},
\quad
\Lambda=\operatorname{diag}(1,3,3).
$$
""",
        r"""
特征多项式可化为
$$
|A-\lambda E|=(b-\lambda)(\lambda-1)(\lambda-3).
$$
由于仅有两个不同特征值，所以
$$
b=1\quad \text{或}\quad b=3.
$$

若 $b=1$，则特征值为 $1,1,3$。又因 $A$ 相似于对角矩阵，故对重根 $\lambda=1$ 必有
$$
r(A-E)=1,
$$
从而求得
$$
a=1.
$$
解特征向量方程得可取
$$
\alpha_1=(-1,1,0)^T,\quad
\alpha_2=(0,0,1)^T,\quad
\alpha_3=(1,1,1)^T.
$$
取
$$
P=(\alpha_1,\alpha_2,\alpha_3),
$$
则
$$
P^{-1}AP=\operatorname{diag}(1,1,3).
$$

若 $b=3$，则特征值为 $1,3,3$。同理由可对角化知
$$
r(A-3E)=1,
$$
从而得
$$
a=-1.
$$
此时可取
$$
\beta_1=(-1,1,1)^T,\quad
\beta_2=(1,1,0)^T,\quad
\beta_3=(0,0,1)^T,
$$
令
$$
P=(\beta_1,\beta_2,\beta_3),
$$
则
$$
P^{-1}AP=\operatorname{diag}(1,3,3).
$$
""",
    ),
    q(
        22,
        "solution",
        12,
        "概率统计",
        ["分布函数", "密度函数", "期望"],
        r"""
在区间 $(0,2)$ 上随机取一点，将该区间分成两段，较短一段的长度记为 $X$，较长一段的长度记为 $Y$，令
$$
Z=\frac{Y}{X}.
$$

1. 求 $X$ 的概率密度；  
2. 求 $Z$ 的概率密度；  
3. 求 $E\!\left(\dfrac{X}{Y}\right)$。
""",
        r"""
$$
f_X(x)=
\begin{cases}
1,& 0<x<1,\\
0,& \text{其他},
\end{cases}
$$

$$
f_Z(z)=
\begin{cases}
\dfrac{2}{(z+1)^2},& z>1,\\
0,& \text{其他},
\end{cases}
$$

$$
E\!\left(\frac{X}{Y}\right)=2\ln2-1.
$$
""",
        r"""
设随机点坐标为 $T$，则 $T$ 在 $(0,2)$ 上服从均匀分布。

由定义，
$$
X=\min\{T,2-T\},\qquad Y=\max\{T,2-T\},
$$
并且
$$
X+Y=2,\qquad 0<X<1,\qquad Y>X.
$$

1. 对 $0<x<1$，
更直接地看，$X$ 在 $(0,1)$ 上均匀分布，所以
$$
f_X(x)=1,\qquad 0<x<1.
$$

2. 由
$$
Z=\frac{Y}{X}=\frac{2-X}{X}=\frac2X-1.
$$
故 $z>1$，且
$$
X=\frac2{z+1}.
$$
于是
$$
F_Z(z)=P(Z\le z)=P\!\left(\frac{2-X}{X}\le z\right)
=P\!\left(X\ge \frac2{z+1}\right)
=1-\frac2{z+1}\qquad (z\ge1).
$$
求导得
$$
f_Z(z)=\frac{2}{(z+1)^2},\qquad z>1.
$$

3. 因为
$$
\frac{X}{Y}=\frac{X}{2-X},
$$
又 $X\sim U(0,1)$，所以
$$
E\!\left(\frac{X}{Y}\right)
=\int_0^1 \frac{x}{2-x}\,dx
=\int_0^1\left(\frac{2}{2-x}-1\right)dx
=2\ln2-1.
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
