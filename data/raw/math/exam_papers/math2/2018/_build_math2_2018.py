from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parent
YEAR = 2018


def md(text: str) -> str:
    return dedent(text).strip()


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def qtype_label(qtype: str) -> str:
    return {
        "single_choice": "选择题",
        "fill_blank": "填空题",
        "solution": "解答题",
        "proof": "证明题",
    }[qtype]


def answer_for_table(answer: str) -> str:
    brief = " ".join(answer.replace("\n", " ").split())
    if len(brief) > 48:
        return "见详解"
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
    assets: list[str]


QUESTIONS = [
    Question(1, "single_choice", 4, "高等数学", ["极限", "指数型极限", "等价无穷小"],
             md(r"""
             若
             $$
             \lim_{x\to0}\left(e^x+ax^2+bx\right)^{1/x^2}=1,
             $$
             则（ ）

             (A) $a=\dfrac12,\ b=-1$

             (B) $a=-\dfrac12,\ b=-1$

             (C) $a=\dfrac12,\ b=1$

             (D) $a=-\dfrac12,\ b=1$
             """),
             "B",
             md(r"""
             设 $u=e^x+ax^2+bx-1$，则原式为 $\lim_{x\to0}(1+u)^{1/x^2}$。要使极限为 $1$，需
             $$
             \lim_{x\to0}\frac{u}{x^2}=0.
             $$
             先由
             $$
             \lim_{x\to0}\frac{e^x+ax^2+bx-1}{x}=1+b=0
             $$
             得 $b=-1$。再代回，
             $$
             \lim_{x\to0}\frac{e^x-x+ax^2-1}{x^2}=\frac12+a=0,
             $$
             故 $a=-\dfrac12$。选 B。
             """), ["images/source_pages/page-1.png"]),
    Question(2, "single_choice", 4, "高等数学", ["导数定义", "可导性", "分段与绝对值函数"],
             md(r"""
             下列函数中，在 $x=0$ 处不可导的是（ ）

             (A) $f(x)=|x|\sin|x|$

             (B) $f(x)=|x|\sin\sqrt{|x|}$

             (C) $f(x)=\cos|x|$

             (D) $f(x)=\cos\sqrt{|x|}$
             """),
             "D",
             md(r"""
             由导数定义逐项判断。
             选项 A、B 有
             $$
             \frac{f(x)-f(0)}{x}\to0.
             $$
             选项 C 中
             $$
             \cos|x|-1\sim-\frac{|x|^2}{2},
             $$
             故商仍趋于 $0$。而 D 中
             $$
             \cos\sqrt{|x|}-1\sim-\frac{|x|}{2},
             $$
             于是
             $$
             \frac{\cos\sqrt{|x|}-1}{x}\sim-\frac{|x|}{2x}
             $$
             左右极限不相等，不可导。选 D。
             """), ["images/source_pages/page-1.png"]),
    Question(3, "single_choice", 4, "高等数学", ["分段函数", "连续性", "参数讨论"],
             md(r"""
             设函数
             $$
             f(x)=
             \begin{cases}
             -1,& x<0,\\
             1,& x\ge 0,
             \end{cases}
             \qquad
             g(x)=
             \begin{cases}
             2-ax,& x\le -1,\\
             x,& -1<x<0,\\
             x-b,& x\ge 0.
             \end{cases}
             $$
             若 $f(x)+g(x)$ 在 $\mathbb R$ 上连续，则（ ）

             (A) $a=3,\ b=1$

             (B) $a=3,\ b=2$

             (C) $a=-3,\ b=1$

             (D) $a=-3,\ b=2$
             """),
             "D",
             md(r"""
             有
             $$
             f(x)+g(x)=
             \begin{cases}
             1-ax,& x\le -1,\\
             x-1,& -1<x<0,\\
             x+1-b,& x\ge 0.
             \end{cases}
             $$
             在 $x=-1$ 处连续给出
             $$
             1+a=-2 \Rightarrow a=-3.
             $$
             在 $x=0$ 处连续给出
             $$
             -1=1-b \Rightarrow b=2.
             $$
             选 D。
             """), ["images/source_pages/page-1.png"]),
    Question(4, "single_choice", 4, "高等数学", ["泰勒公式", "凸函数", "积分不等式"],
             md(r"""
             设函数 $f(x)$ 在 $[0,1]$ 上二阶可导，且
             $$
             \int_0^1 f(x)\,dx=0,
             $$
             则（ ）

             (A) 当 $f'(x)<0$ 时，$f\!\left(\dfrac12\right)<0$

             (B) 当 $f''(x)<0$ 时，$f\!\left(\dfrac12\right)<0$

             (C) 当 $f'(x)>0$ 时，$f\!\left(\dfrac12\right)<0$

             (D) 当 $f''(x)>0$ 时，$f\!\left(\dfrac12\right)<0$
             """),
             "D",
             md(r"""
             取 $f(x)=x-\dfrac12$ 或 $f(x)=\dfrac12-x$ 可排除 A、C。若 $f''(x)>0$，则在 $x=\dfrac12$ 处作泰勒展开：
             $$
             f(x)=f\!\left(\frac12\right)+f'\!\left(\frac12\right)\left(x-\frac12\right)+\frac{f''(\xi)}{2}\left(x-\frac12\right)^2.
             $$
             因为 $f''(\xi)>0$，故
             $$
             f(x)>f\!\left(\frac12\right)+f'\!\left(\frac12\right)\left(x-\frac12\right).
             $$
             两边在 $[0,1]$ 上积分，利用 $\int_0^1 f(x)\,dx=0$ 且 $\int_0^1(x-\frac12)\,dx=0$，得
             $$
             0>f\!\left(\frac12\right).
             $$
             选 D。
             """), ["images/source_pages/page-1.png"]),
    Question(5, "single_choice", 4, "高等数学", ["定积分比较", "奇偶性", "不等式"],
             md(r"""
             设
             $$
             M=\int_{-\pi/2}^{\pi/2}\frac{(1+x)^2}{1+x^2}\,dx,\quad
             N=\int_{-\pi/2}^{\pi/2}\frac{1+x}{e^x}\,dx,\quad
             K=\int_{-\pi/2}^{\pi/2}(1+\sqrt{\cos x})\,dx,
             $$
             则（ ）

             (A) $M>N>K$

             (B) $M>K>N$

             (C) $K>M>N$

             (D) $K>N>M$
             """),
             "C",
             md(r"""
             化简
             $$
             M=\int_{-\pi/2}^{\pi/2}\left(1+\frac{2x}{1+x^2}\right)dx=\int_{-\pi/2}^{\pi/2}1\,dx=\pi.
             $$
             因为 $e^x>1+x$，所以
             $$
             N=\int_{-\pi/2}^{\pi/2}\frac{1+x}{e^x}\,dx<\int_{-\pi/2}^{\pi/2}1\,dx=\pi=M.
             $$
             又因 $1+\sqrt{\cos x}>1$，故
             $$
             K>\int_{-\pi/2}^{\pi/2}1\,dx=\pi=M.
             $$
             所以 $K>M>N$，选 C。
             """), ["images/source_pages/page-1.png"]),
    Question(6, "single_choice", 4, "高等数学", ["二重积分", "区域对称性", "积分计算"],
             md(r"""
             $$
             \int_{-1}^0dx\int_{-x}^{2-x^2}(1-xy)\,dy+\int_0^1dx\int_x^{2-x^2}(1-xy)\,dy=(\ )
             $$

             (A) $\dfrac53$

             (B) $\dfrac56$

             (C) $\dfrac73$

             (D) $\dfrac76$
             """),
             "C",
             md(r"""
             积分区域为
             $$
             D=\{(x,y)\mid -1\le x\le0,\ -x\le y\le2-x^2\}\cup\{(x,y)\mid 0\le x\le1,\ x\le y\le2-x^2\}.
             $$
             其中 $xy$ 关于 $x$ 为奇函数，区域关于 $y$ 轴对称，因此奇部积分为 $0$。原式化为
             $$
             2\int_0^1dx\int_x^{2-x^2}1\,dy
             =2\int_0^1(2-x^2-x)\,dx=\frac73.
             $$
             选 C。
             """), ["images/source_pages/page-1.png"]),
    Question(7, "single_choice", 4, "线性代数", ["矩阵相似", "Jordan块", "相似变换"],
             md(r"""
             下列矩阵中，与矩阵
             $$
             \begin{pmatrix}
             1&1&0\\
             0&1&1\\
             0&0&1
             \end{pmatrix}
             $$
             相似的是（ ）

             (A)
             $$
             \begin{pmatrix}
             1&1&-1\\
             0&1&1\\
             0&0&1
             \end{pmatrix}
             $$

             (B)
             $$
             \begin{pmatrix}
             1&0&-1\\
             0&1&1\\
             0&0&1
             \end{pmatrix}
             $$

             (C)
             $$
             \begin{pmatrix}
             1&1&-1\\
             0&1&0\\
             0&0&1
             \end{pmatrix}
             $$

             (D)
             $$
             \begin{pmatrix}
             1&0&-1\\
             0&1&0\\
             0&0&1
             \end{pmatrix}
             $$
             """),
             "A",
             md(r"""
             取
             $$
             P=\begin{pmatrix}
             1&-1&0\\
             0&1&0\\
             0&0&1
             \end{pmatrix},\qquad
             P^{-1}=\begin{pmatrix}
             1&1&0\\
             0&1&0\\
             0&0&1
             \end{pmatrix}.
             $$
             直接计算得
             $$
             P^{-1}\begin{pmatrix}
             1&1&-1\\
             0&1&1\\
             0&0&1
             \end{pmatrix}P=
             \begin{pmatrix}
             1&1&0\\
             0&1&1\\
             0&0&1
             \end{pmatrix}.
             $$
             故选 A。
             """), ["images/source_pages/page-1.png"]),
    Question(8, "single_choice", 4, "线性代数", ["矩阵秩", "分块矩阵", "反例法"],
             md(r"""
             设 $A,B$ 为 $n$ 阶矩阵，记 $r(X)$ 为矩阵 $X$ 的秩，$(X,Y)$ 表示分块矩阵，则（ ）

             (A) $r(A,AB)=r(A)$

             (B) $r(A,BA)=r(A)$

             (C) $r(A,B)=\max\{r(A),r(B)\}$

             (D) $r(A,B)=r(A^{\mathsf T},B^{\mathsf T})$
             """),
             "A",
             md(r"""
             选项 C 显然不对，秩一般满足的是上、下界而不是恒等于最大值。选项 B、D 均可构造反例否定。对 A，
             $$
             (A,AB)=A(E,B),
             $$
             右乘分块不增加超出 $A$ 列空间的部分，因此
             $$
             r(A,AB)=r(A).
             $$
             故选 A。
             """), ["images/source_pages/page-2.png"]),
    Question(9, "fill_blank", 4, "高等数学", ["极限", "拉格朗日中值定理", "反三角函数"],
             md(r"""
             $$
             \lim_{x\to+\infty}x^2[\arctan(x+1)-\arctan x]=\underline{\qquad}.
             $$
             """),
             "1",
             md(r"""
             由拉格朗日中值定理，存在 $\xi\in(x,x+1)$ 使
             $$
             \arctan(x+1)-\arctan x=\frac{1}{1+\xi^2}.
             $$
             所以
             $$
             x^2[\arctan(x+1)-\arctan x]=\frac{x^2}{1+\xi^2}\to1.
             $$
             """), ["images/source_pages/page-2.png"]),
    Question(10, "fill_blank", 4, "高等数学", ["拐点", "切线方程", "导数应用"],
             md(r"""
             曲线 $y=x^2+2\ln x$ 在其拐点处的切线方程是 $\underline{\qquad}$。
             """),
             r"$y=4x-3$",
             md(r"""
             $$
             y'=2x+\frac{2}{x},\qquad y''=2-\frac{2}{x^2}.
             $$
             令 $y''=0$ 得 $x=1$，对应点为 $(1,1)$。此时斜率
             $$
             y'(1)=4,
             $$
             切线方程为
             $$
             y-1=4(x-1),
             $$
             即 $y=4x-3$。
             """), ["images/source_pages/page-2.png"]),
    Question(11, "fill_blank", 4, "高等数学", ["反常积分", "部分分式"],
             md(r"""
             $$
             \int_5^{+\infty}\frac{1}{x^2-4x+3}\,dx=\underline{\qquad}.
             $$
             """),
             r"$\dfrac12\ln2$",
             md(r"""
             分解
             $$
             \frac{1}{x^2-4x+3}=\frac12\left(\frac{1}{x-3}-\frac{1}{x-1}\right).
             $$
             因而
             $$
             \int_5^{+\infty}\frac{1}{x^2-4x+3}\,dx
             =\frac12\ln\left|\frac{x-3}{x-1}\right|\Bigg|_5^{+\infty}
             =\frac12\ln2.
             $$
             """), ["images/source_pages/page-2.png"]),
    Question(12, "fill_blank", 4, "高等数学", ["参数方程", "曲率"],
             md(r"""
             曲线
             $$
             \begin{cases}
             x=\cos^3 t,\\
             y=\sin^3 t
             \end{cases}
             $$
             在 $t=\dfrac{\pi}{4}$ 对应点处的曲率为 $\underline{\qquad}$。
             """),
             r"$\dfrac23$",
             md(r"""
             先求
             $$
             \frac{dy}{dx}=\frac{dy/dt}{dx/dt}=-\tan t,
             $$
             进而
             $$
             \frac{d^2y}{dx^2}=\frac{1}{3\cos^4 t\sin t}.
             $$
             当 $t=\dfrac{\pi}{4}$ 时，
             $$
             y'=-1,\qquad y''=\frac{4\sqrt2}{3}.
             $$
             曲率
             $$
             k=\frac{|y''|}{[1+(y')^2]^{3/2}}=\frac{2}{3}.
             $$
             """), ["images/source_pages/page-2.png"]),
    Question(13, "fill_blank", 4, "高等数学", ["隐函数求导", "偏导数"],
             md(r"""
             设函数 $z=z(x,y)$ 由方程
             $$
             \ln z+e^{z-1}=xy
             $$
             确定，则
             $$
             \left.\frac{\partial z}{\partial x}\right|_{(2,\frac12)}=\underline{\qquad}.
             $$
             """),
             r"$\dfrac14$",
             md(r"""
             由题设在 $(x,y)=\left(2,\dfrac12\right)$ 时有 $xy=1$，代入可得 $z=1$。令
             $$
             F(x,y,z)=\ln z+e^{z-1}-xy=0.
             $$
             则
             $$
             F_x=-y,\qquad F_z=\frac1z+e^{z-1}.
             $$
             所以
             $$
             \frac{\partial z}{\partial x}=-\frac{F_x}{F_z}
             =\frac{y}{1/z+e^{z-1}}.
             $$
             在 $\left(2,\dfrac12,1\right)$ 处得 $\dfrac14$。
             """), ["images/source_pages/page-2.png"]),
    Question(14, "fill_blank", 4, "线性代数", ["特征值", "线性变换", "基下矩阵"],
             md(r"""
             设 $A$ 为 $3$ 阶矩阵，$\alpha_1,\alpha_2,\alpha_3$ 为线性无关的向量组。若
             $$
             A\alpha_1=2\alpha_1+\alpha_2+\alpha_3,\quad
             A\alpha_2=\alpha_2+2\alpha_3,\quad
             A\alpha_3=-\alpha_2+\alpha_3,
             $$
             则 $|A|=\underline{\qquad}$。
             """),
             "2",
             md(r"""
             在基 $(\alpha_1,\alpha_2,\alpha_3)$ 下，$A$ 的矩阵为
             $$
             \begin{pmatrix}
             2&0&0\\
             1&1&-1\\
             1&2&1
             \end{pmatrix}.
             $$
             行列式与基无关，所以
             $$
             |A|=\begin{vmatrix}
             2&0&0\\
             1&1&-1\\
             1&2&1
             \end{vmatrix}=2.
             $$
             """), ["images/source_pages/page-2.png"]),
    Question(15, "solution", 10, "高等数学", ["不定积分", "分部积分", "换元积分"],
             md(r"""
             求不定积分
             $$
             \int e^{2x}\arctan\sqrt{e^x-1}\,dx.
             $$
             """),
             md(r"""
             $$
             \frac12\left[e^{2x}\arctan\sqrt{e^x-1}-\frac13\left(\sqrt{e^x-1}\right)^3+\sqrt{e^x-1}\right]+C.
             $$
             """),
             md(r"""
             记
             $$
             I=\int e^{2x}\arctan\sqrt{e^x-1}\,dx.
             $$
             分部积分，取
             $$
             u=\arctan\sqrt{e^x-1},\qquad dv=e^{2x}dx,
             $$
             则
             $$
             I=\frac12e^{2x}\arctan\sqrt{e^x-1}-\frac12\int \frac{e^{2x}}{2\sqrt{e^x-1}}\,dx.
             $$
             再令 $t=\sqrt{e^x-1}$，则 $e^x=t^2+1$，可化为有理式积分，算得
             $$
             I=\frac12\left[e^{2x}\arctan\sqrt{e^x-1}-\frac13(\sqrt{e^x-1})^3+\sqrt{e^x-1}\right]+C.
             $$
             """), ["images/source_pages/page-2.png"]),
    Question(16, "solution", 10, "高等数学", ["积分方程", "微积分基本定理", "平均值"],
             md(r"""
             已知连续函数 $f(x)$ 满足
             $$
             \int_0^x f(t)\,dt+\int_0^x t\,f(x-t)\,dt=ax^2.
             $$

             (1) 求 $f(x)$；

             (2) 若 $f(x)$ 在区间 $[0,1]$ 上的平均值为 $1$，求 $a$ 的值。
             """),
             md(r"""
             (1) $f(x)=2a(1-e^{-x})$；

             (2) $a=\dfrac e2$。
             """),
             md(r"""
             将第二项作换元 $u=x-t$，得
             $$
             \int_0^x f(t)\,dt+\int_0^x (x-u)f(u)\,du=ax^2.
             $$
             整理后对 $x$ 求导，可得
             $$
             f(x)+\int_0^x f(u)\,du=2ax.
             $$
             令
             $$
             F(x)=\int_0^x f(u)\,du,
             $$
             则 $F'(x)+F(x)=2ax,\ F(0)=0$。解得
             $$
             F(x)=2ax-2a+2ae^{-x},
             $$
             故
             $$
             f(x)=F'(x)=2a(1-e^{-x}).
             $$
             再由平均值条件
             $$
             \int_0^1 f(x)\,dx=1
             $$
             得
             $$
             2a\int_0^1(1-e^{-x})dx=1 \Rightarrow \frac{2a}{e}=1,
             $$
             所以 $a=\dfrac e2$。
             """), ["images/source_pages/page-2.png"]),
    Question(17, "solution", 10, "高等数学", ["参数曲线围成区域", "二重积分", "换元"],
             md(r"""
             设平面区域 $D$ 由曲线
             $$
             \begin{cases}
             x=t-\sin t,\\
             y=1-\cos t
             \end{cases}
             \qquad (0\le t\le2\pi)
             $$
             与 $x$ 轴围成，计算二重积分
             $$
             \iint_D (x+2y)\,dxdy.
             $$
             """),
             r"$3\pi^2+5\pi$",
             md(r"""
             对竖条积分，设上边界为 $y=\varphi(x)$，则
             $$
             \iint_D(x+2y)\,dxdy=\int_0^{2\pi}[x\varphi(x)+\varphi^2(x)]\,dx.
             $$
             再用参数表示
             $$
             x=t-\sin t,\qquad y=1-\cos t,\qquad dx=(1-\cos t)dt,
             $$
             可得
             $$
             \iint_D(x+2y)\,dxdy
             =\int_0^{2\pi}(t-\sin t)(1-\cos t)^2dt+\int_0^{2\pi}(1-\cos t)^3dt.
             $$
             逐项积分后得到
             $$
             3\pi^2+5\pi.
             $$
             """), ["images/source_pages/page-3.png"]),
    Question(18, "proof", 10, "高等数学", ["函数单调性", "不等式证明", "对数函数"],
             md(r"""
             已知常数 $k\ge \ln2-1$，证明：
             $$
             (x-1)(x-\ln^2x+2k\ln x-1)\ge0,\qquad x>0.
             $$
             """),
             r"结论成立",
             md(r"""
             设
             $$
             f(x)=x-\ln^2x+2k\ln x-1.
             $$
             只需证明 $x<1$ 时 $f(x)\le0$，$x>1$ 时 $f(x)\ge0$。

             对 $0<x<1$，有
             $$
             f'(x)=\frac{x-2\ln x+2k}{x}.
             $$
             再设 $g(x)=x-2\ln x+2k$，则
             $$
             g'(x)=1-\frac2x<0.
             $$
             所以 $g(x)>g(1)=1+2k\ge2\ln2-1>0$，故 $f'(x)>0$，从而 $f(x)\le f(1)=0$。

             对 $x>1$ 同理，$g'(x)=1-\dfrac2x$ 在 $(1,2)$ 上小于零、在 $(2,+\infty)$ 上大于零，故
             $$
             g(x)\ge g(2)=2-2\ln2+2k\ge0.
             $$
             因而 $f'(x)\ge0$，故 $f(x)\ge f(1)=0$。

             于是
             $$
             (x-1)f(x)\ge0,
             $$
             即原不等式成立。
             """), ["images/source_pages/page-3.png"]),
    Question(19, "solution", 10, "高等数学", ["极值问题", "拉格朗日乘子法", "几何应用"],
             md(r"""
             将长为 $2\text{m}$ 的铁丝分成三段，依次围成圆、正方形与正三角形。三个图形的面积和是否存在最小值？若存在，求出最小值。
             """),
             r"$S_{\min}=\dfrac{1}{\pi+4+3\sqrt3}$",
             md(r"""
             设三段长度分别为 $x,y,z$，则
             $$
             x+y+z=2.
             $$
             圆、正三角形、正方形的面积分别为
             $$
             \frac{x^2}{4\pi},\qquad \frac{\sqrt3\,y^2}{36},\qquad \frac{z^2}{16}.
             $$
             故
             $$
             S=\frac{x^2}{4\pi}+\frac{\sqrt3\,y^2}{36}+\frac{z^2}{16}.
             $$
             这是闭有界集合上的连续函数，最小值存在。用拉格朗日乘子法：
             $$
             F=\frac{x^2}{4\pi}+\frac{\sqrt3\,y^2}{36}+\frac{z^2}{16}+\lambda(x+y+z-2).
             $$
             解方程组得
             $$
             x=\frac{4\pi}{2\pi+8+6\sqrt3},\quad
             y=\frac{12\sqrt3}{2\pi+8+6\sqrt3},\quad
             z=\frac{16}{2\pi+8+6\sqrt3}.
             $$
             代回得
             $$
             S_{\min}=\frac{1}{\pi+4+3\sqrt3}.
             $$
             """), ["images/source_pages/page-3.png"]),
    Question(20, "solution", 11, "高等数学", ["相关变化率", "定积分面积", "导数应用"],
             md(r"""
             已知曲线 $L:y=\dfrac49x^2\ (x\ge0)$，点 $O(0,0)$，点 $A(0,1)$。设 $P$ 是 $L$ 上的动点，$S$ 是直线 $OA$ 与直线 $AP$ 及曲线 $L$ 所围图形的面积。若 $P$ 运动到点 $(3,4)$ 时沿 $x$ 轴正向的速度是 $4$，求此时 $S$ 关于时间 $t$ 的变化率。
             """),
             "10",
             md(r"""
             设 $P=(x(t),\frac49x^2(t))$。由图形面积可得
             $$
             S(t)=\frac12\left(1+\frac49x^2(t)\right)x(t)-\int_0^{x(t)}\frac49u^2\,du
             =\frac{x(t)}{2}+\frac{2}{27}x^3(t).
             $$
             所以
             $$
             S'(t)=\frac12x'(t)+\frac29x^2(t)x'(t).
             $$
             当 $x=3,\ x'(t)=4$ 时，
             $$
             S'(t)=\frac12\cdot4+\frac29\cdot9\cdot4=10.
             $$
             """), ["images/source_pages/page-3.png"]),
    Question(21, "proof", 11, "高等数学", ["数列极限", "单调有界", "递推数列"],
             md(r"""
             设数列 $\{x_n\}$ 满足：$x_1>0$，
             $$
             x_ne^{x_{n+1}}=e^{x_n}-1\qquad(n=1,2,\cdots).
             $$
             证明 $\{x_n\}$ 收敛，并求 $\lim\limits_{n\to\infty}x_n$。
             """),
             "数列收敛，且极限为 0",
             md(r"""
             由递推式得
             $$
             x_{n+1}=\ln\frac{e^{x_n}-1}{x_n}.
             $$
             因为 $x_1>0$，且对 $x>0$ 有 $e^x-1>x$，所以归纳可得 $x_n>0$。

             再由中值定理，
             $$
             e^{x_n}-1=e^{\xi_n}x_n\qquad(0<\xi_n<x_n),
             $$
             从而
             $$
             e^{x_{n+1}}=\frac{e^{x_n}-1}{x_n}=e^{\xi_n},
             $$
             即 $x_{n+1}=\xi_n<x_n$。故 $\{x_n\}$ 单调递减且有下界 $0$，从而收敛。

             设极限为 $A\ge0$，对递推式取极限：
             $$
             Ae^A=e^A-1.
             $$
             解得 $A=0$。故
             $$
             \lim_{n\to\infty}x_n=0.
             $$
             """), ["images/source_pages/page-4.png"]),
    Question(22, "solution", 11, "线性代数", ["二次型", "规范形", "秩与特征值"],
             md(r"""
             设实二次型
             $$
             f(x_1,x_2,x_3)=(x_1-x_2+x_3)^2+(x_2+x_3)^2+(x_1+ax_3)^2,
             $$
             其中 $a$ 是参数。

             (1) 求 $f(x_1,x_2,x_3)=0$ 的解；

             (2) 求 $f(x_1,x_2,x_3)$ 的规范形。
             """),
             md(r"""
             (1) 当 $a=2$ 时，$x=k(2,1,-1)^{\mathsf T}\ (k\in\mathbb R)$；当 $a\ne2$ 时，只有零解。

             (2) 当 $a=2$ 时，规范形为 $y_1^2+y_2^2$；当 $a\ne2$ 时，规范形为 $y_1^2+y_2^2+y_3^2$。
             """),
             md(r"""
             由 $f=0$ 可知三个平方项都为零，即
             $$
             \begin{cases}
             x_1-x_2+x_3=0,\\
             x_2+x_3=0,\\
             x_1+ax_3=0.
             \end{cases}
             $$
             其系数矩阵经消元可化为上三角，最后一行给出系数 $a-2$。故当 $a\ne2$ 时秩为 $3$，只有零解；当 $a=2$ 时秩为 $2$，通解为
             $$
             x=k(2,1,-1)^{\mathsf T}.
             $$

             令
             $$
             y_1=x_1-x_2+x_3,\quad y_2=x_2+x_3,\quad y_3=x_1+ax_3,
             $$
             则
             $$
             f=y_1^2+y_2^2+y_3^2.
             $$
             当 $a\ne2$ 时变换矩阵可逆，故规范形为 $y_1^2+y_2^2+y_3^2$。当 $a=2$ 时该变换矩阵秩为 $2$，此时二次型正惯性指数为 $2$、零惯性指数为 $1$，故规范形为 $y_1^2+y_2^2$。
             """), ["images/source_pages/page-4.png"]),
    Question(23, "solution", 11, "线性代数", ["矩阵方程", "初等列变换", "可逆矩阵"],
             md(r"""
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

             (1) 求 $a$；

             (2) 求满足 $AP=B$ 的可逆矩阵 $P$。
             """),
             md(r"""
             (1) $a=2$；

             (2) 可取
             $$
             P=
             \begin{pmatrix}
             -6k_1+3&-6k_2+4&-6k_3+4\\
             2k_1-1&2k_2-1&2k_3-1\\
             k_1&k_2&k_3
             \end{pmatrix},
             $$
             其中 $k_1,k_2,k_3\in\mathbb R$，且 $k_2\ne k_3$。
             """),
             md(r"""
             因为 $A$ 可经初等列变换化为 $B$，故 $r(A)=r(B)$。分别对两矩阵做消元：
             $$
             A\sim
             \begin{pmatrix}
             1&2&a\\
             0&1&-a\\
             0&0&0
             \end{pmatrix},\qquad
             B\sim
             \begin{pmatrix}
             1&a&2\\
             0&1&1\\
             0&0&2-a
             \end{pmatrix}.
             $$
             因秩相等，得 $2-a=0$，即 $a=2$。

             于是求矩阵方程 $AP=B$。把增广矩阵 $(A,B)$ 消元可得通解
             $$
             P=
             \begin{pmatrix}
             -6k_1+3&-6k_2+4&-6k_3+4\\
             2k_1-1&2k_2-1&2k_3-1\\
             k_1&k_2&k_3
             \end{pmatrix}.
             $$
             其可逆条件为 $|P|\ne0$，由结果可化为 $k_2\ne k_3$。故上式即所求。
             """), ["images/source_pages/page-4.png"]),
]


def build_card(q: Question) -> str:
    qid = f"kaoyan_math2_{YEAR}_q{q.number:03d}"
    lines = [
        "---",
        f"question_id: {qid}",
        f"exam_id: kaoyan_math2_{YEAR}",
        "exam_type: math2",
        f"year: {YEAR}",
        f"question_number: {q.number}",
        f"question_type: {q.question_type}",
        f"score: {q.score}",
        f"module: {q.module}",
        "topics:",
        *[f"  - {topic}" for topic in q.topics],
        "difficulty: unknown",
        "review_status: reviewed",
        "answer_status: available",
        "explanation_status: available",
        f"source_file: math2_{YEAR}_questions.md",
        f"answer_source_file: math2_{YEAR}_answers.md",
        "assets:",
        *[f"  - {asset}" for asset in q.assets],
        "---",
        "",
        f"# {YEAR} 数学二第 {q.number} 题",
        "",
        "## 题目",
        "",
        q.stem,
        "",
    ]
    for asset in q.assets:
        lines.append(f"![题图](../{asset})")
    lines.extend([
        "",
        "## 标准答案",
        "",
        q.answer,
        "",
        "## 解析",
        "",
        q.explanation,
        "",
        "## 来源",
        "",
        f"- 题目来源：`math2_{YEAR}_questions.md`",
        f"- 答案来源：`math2_{YEAR}_answers.md`",
        "",
    ])
    return "\n".join(lines)


def annual_questions_md(questions: list[Question]) -> str:
    lines = [
        f"# {YEAR} 年数学二真题",
        "",
        "资料类型：考研数学二历年真题",
        f"年份：{YEAR}",
        "科目：数学二",
        "整理状态：按真题 PDF 与答案解析 PDF 交叉校对整理。",
        "",
    ]
    for page in range(1, 5):
        lines.extend([
            f"**第 {page} 页题面页图**",
            "",
            f"![{YEAR} 数学二第 {page} 页题面](images/source_pages/page-{page}.png)",
            "",
        ])
    for q in questions:
        lines.extend([
            f"## 第 {q.number} 题",
            f"- 题型：{qtype_label(q.question_type)}",
            f"- 分值：{q.score}",
            f"- 模块：{q.module}",
            f"- 考点：{'、'.join(q.topics)}",
            "",
            q.stem,
            "",
        ])
    return "\n".join(lines).rstrip() + "\n"


def annual_answers_md(questions: list[Question]) -> str:
    lines = [
        f"# {YEAR} 年数学二答案解析",
        "",
        "资料类型：考研数学二答案解析",
        f"年份：{YEAR}",
        "科目：数学二",
        "整理状态：基于答案解析 PDF 页图与题面交叉清洗。",
        "",
        "## 答案速查",
        "",
        "| 题号 | 题型 | 答案 |",
        "|---|---|---|",
    ]
    for q in questions:
        lines.append(f"| {q.number} | {qtype_label(q.question_type)} | {answer_for_table(q.answer).replace('|', '\\|')} |")
    lines.extend(["", "## 详细解析", ""])
    for q in questions:
        lines.extend([
            f"### 第 {q.number} 题",
            "",
            f"- 答案：{q.answer}",
            "",
            q.explanation,
            "",
        ])
    return "\n".join(lines).rstrip() + "\n"


def card_record(q: Question) -> dict:
    return {
        "question_id": f"kaoyan_math2_{YEAR}_q{q.number:03d}",
        "exam_id": f"kaoyan_math2_{YEAR}",
        "exam_type": "math2",
        "year": YEAR,
        "question_number": q.number,
        "question_type": q.question_type,
        "score": q.score,
        "module": q.module,
        "topics": q.topics,
        "difficulty": "unknown",
        "review_status": "reviewed",
        "answer_status": "available",
        "explanation_status": "available",
        "source_file": f"math2_{YEAR}_questions.md",
        "answer_source_file": f"math2_{YEAR}_answers.md",
        "card_path": f"questions/q{q.number:03d}.md",
        "assets": q.assets,
        "answer": q.answer,
        "explanation": q.explanation,
    }


def write_manifest(questions: list[Question]) -> None:
    manifest = {
        "exam_id": f"kaoyan_math2_{YEAR}",
        "exam_type": "math2",
        "exam_label": "数学二",
        "year": YEAR,
        "source_files": {
            "questions": f"math2_{YEAR}_questions.md",
            "answers": f"math2_{YEAR}_answers.md",
        },
        "card_dir": "questions",
        "index_file": "questions.jsonl",
        "question_count": len(questions),
        "explanation_count": len(questions),
        "question_ids": [f"kaoyan_math2_{YEAR}_q{q.number:03d}" for q in questions],
        "generated_at": now_iso(),
        "review_status": "reviewed",
        "answer_status": "available",
        "explanation_status": "available",
    }
    (ROOT / "paper_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    (ROOT / "questions").mkdir(exist_ok=True)

    (ROOT / f"math2_{YEAR}_questions.md").write_text(
        annual_questions_md(QUESTIONS),
        encoding="utf-8",
    )
    (ROOT / f"math2_{YEAR}_answers.md").write_text(
        annual_answers_md(QUESTIONS),
        encoding="utf-8",
    )

    with (ROOT / "questions.jsonl").open("w", encoding="utf-8") as fh:
        for q in QUESTIONS:
            card_path = ROOT / "questions" / f"q{q.number:03d}.md"
            card_path.write_text(build_card(q), encoding="utf-8")
            fh.write(json.dumps(card_record(q), ensure_ascii=False) + "\n")

    write_manifest(QUESTIONS)


if __name__ == "__main__":
    main()
