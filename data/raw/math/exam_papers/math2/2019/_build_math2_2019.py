from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parent
YEAR = 2019


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
    Question(1, "single_choice", 4, "高等数学", ["无穷小比较", "泰勒展开", "极限"],
             md(r"""
             当 $x\to0$ 时，若 $x-\tan x$ 与 $x^k$ 是同阶无穷小，则 $k=（\ ）$

             (A) 1

             (B) 2

             (C) 3

             (D) 4
             """),
             "C",
             md(r"""
             由
             $$
             \tan x=x+\frac13x^3+o(x^3)
             $$
             得
             $$
             x-\tan x\sim-\frac13x^3.
             $$
             故与 $x^3$ 同阶，选 C。
             """), ["images/source_pages/page-1.png"]),
    Question(2, "single_choice", 4, "高等数学", ["拐点", "导数应用", "函数图像"],
             md(r"""
             曲线
             $$
             y=x\sin x+2\cos x\qquad \left(-\frac{\pi}{2}<x<2\pi\right)
             $$
             的拐点坐标为（ ）

             (A) $(0,2)$

             (B) $(\pi,-2)$

             (C) $\left(\dfrac{\pi}{2},\dfrac{\pi}{2}\right)$

             (D) $\left(\dfrac{3\pi}{2},-\dfrac{3\pi}{2}\right)$
             """),
             "B",
             md(r"""
             $$
             y'=x\cos x-\sin x,\qquad y''=-x\sin x.
             $$
             令 $y''=0$ 得候选点 $x=0,\pi$。在 $(-\frac\pi2,0)$ 与 $(0,\pi)$ 上有 $y''<0$，故 $(0,2)$ 不是拐点；在 $(\pi,\frac{3\pi}{2})$ 上 $y''>0$，所以 $x=\pi$ 为拐点。此时
             $$
             y(\pi)=\pi\sin\pi+2\cos\pi=-2.
             $$
             选 B。
             """), ["images/source_pages/page-1.png"]),
    Question(3, "single_choice", 4, "高等数学", ["反常积分", "收敛散敛"],
             md(r"""
             下列反常积分发散的是（ ）

             (A) $\displaystyle \int_0^{+\infty} xe^{-x}\,dx$

             (B) $\displaystyle \int_0^{+\infty} xe^{-x^2}\,dx$

             (C) $\displaystyle \int_0^{+\infty}\frac{\arctan x}{1+x^2}\,dx$

             (D) $\displaystyle \int_0^{+\infty}\frac{x}{1+x^2}\,dx$
             """),
             "D",
             md(r"""
             前三项分别可直接积分或换元判断收敛：
             $$
             \int_0^{+\infty}xe^{-x}dx=\Gamma(2)=1,\quad
             \int_0^{+\infty}xe^{-x^2}dx=\frac12,
             $$
             $$
             \int_0^{+\infty}\frac{\arctan x}{1+x^2}dx
             =\frac12(\arctan x)^2\Big|_0^{+\infty}
             =\frac{\pi^2}{8}.
             $$
             而
             $$
             \frac{x}{1+x^2}\sim\frac1x\quad (x\to+\infty),
             $$
             故对应反常积分发散。选 D。
             """), ["images/source_pages/page-1.png"]),
    Question(4, "single_choice", 4, "高等数学", ["线性微分方程", "特征方程", "特解"],
             md(r"""
             已知微分方程
             $$
             y''+ay'+by=ce^x
             $$
             的通解为
             $$
             y=(C_1+C_2x)e^{-x}+e^x,
             $$
             则 $a,b,c$ 依次为（ ）

             (A) $1,0,1$

             (B) $1,0,2$

             (C) $2,1,3$

             (D) $2,1,4$
             """),
             "D",
             md(r"""
             齐次方程通解为 $(C_1+C_2x)e^{-x}$，说明特征根为 $-1,-1$，故
             $$
             \lambda^2+a\lambda+b=(\lambda+1)^2
             $$
             从而 $a=2,\ b=1$。再代入特解 $y_p=e^x$，
             $$
             y_p''+ay_p'+by_p=(1+2+1)e^x=4e^x,
             $$
             所以 $c=4$。选 D。
             """), ["images/source_pages/page-1.png"]),
    Question(5, "single_choice", 4, "高等数学", ["二重积分比较", "不等式", "极坐标"],
             md(r"""
             已知平面区域
             $$
             D=\left\{(x,y)\mid |x|+|y|\le\frac{\pi}{2}\right\},
             $$
             $$
             I_1=\iint_D\sqrt{x^2+y^2}\,dxdy,\quad
             I_2=\iint_D\sin\sqrt{x^2+y^2}\,dxdy,\quad
             I_3=\iint_D(1-\cos\sqrt{x^2+y^2})\,dxdy,
             $$
             则（ ）

             (A) $I_3<I_2<I_1$

             (B) $I_2<I_1<I_3$

             (C) $I_1<I_2<I_3$

             (D) $I_2<I_3<I_1$
             """),
             "A",
             md(r"""
             设 $r=\sqrt{x^2+y^2}$。因 $r\ge0$ 且 $\sin r\le r$，可知 $I_2<I_1$。又
             $$
             1-\cos r=2\sin^2\frac r2,\qquad
             \sin r=2\sin\frac r2\cos\frac r2.
             $$
             在区域 $D$ 内有 $r\le \dfrac{\pi}{2}$，故 $\dfrac r2\in[0,\dfrac{\pi}{4}]$，从而
             $$
             \sin\frac r2\le\cos\frac r2.
             $$
             因此
             $$
             1-\cos r\le\sin r,
             $$
             即 $I_3<I_2$。综上 $I_3<I_2<I_1$，选 A。
             """), ["images/source_pages/page-1.png"]),
    Question(6, "single_choice", 4, "高等数学", ["曲线相切", "曲率", "极限判定"],
             md(r"""
             已知 $f(x),g(x)$ 2 阶可导且 2 阶导函数在 $x=a$ 处连续，则
             $$
             \lim_{x\to a}\frac{f(x)-g(x)}{(x-a)^2}=0
             $$
             是曲线 $y=f(x)$ 和 $y=g(x)$ 在 $x=a$ 对应点处相切且曲率相等的（ ）

             (A) 充分非必要条件

             (B) 充分必要条件

             (C) 必要非充分条件

             (D) 既非充分又非必要条件
             """),
             "A",
             md(r"""
             由极限条件先得
             $$
             f(a)=g(a),\qquad f'(a)=g'(a),
             $$
             再对商继续处理可得
             $$
             f''(a)=g''(a).
             $$
             因此两曲线在对应点相切且曲率相等，所以它是充分条件。反过来，仅知相切与曲率相等并不能推出上述二阶小量极限一定为 0，故不是必要条件。选 A。
             """), ["images/source_pages/page-1.png"]),
    Question(7, "single_choice", 4, "线性代数", ["伴随矩阵", "秩", "齐次方程组"],
             md(r"""
             设 $A$ 是 4 阶矩阵，$A^*$ 是 $A$ 的伴随矩阵，若线性方程组 $Ax=0$ 的基础解系中只有 2 个向量，则 $r(A^*)=（\ ）$

             (A) 0

             (B) 1

             (C) 2

             (D) 3
             """),
             "A",
             md(r"""
             基础解系有 2 个向量，说明
             $$
             4-r(A)=2 \Rightarrow r(A)=2.
             $$
             对 4 阶矩阵，当 $r(A)\le n-2$ 时伴随矩阵全为零矩阵，因此
             $$
             r(A^*)=0.
             $$
             选 A。
             """), ["images/source_pages/page-1.png"]),
    Question(8, "single_choice", 4, "线性代数", ["实对称矩阵", "特征值", "规范形"],
             md(r"""
             设 $A$ 是 3 阶实对称矩阵，$E$ 是 3 阶单位矩阵。若 $A^2+A=2E$，且 $|A|=4$，则二次型 $x^{\mathsf T}Ax$ 的规范形为（ ）

             (A) $y_1^2+y_2^2+y_3^2$

             (B) $y_1^2+y_2^2-y_3^2$

             (C) $y_1^2-y_2^2-y_3^2$

             (D) $-y_1^2-y_2^2-y_3^2$
             """),
             "C",
             md(r"""
             设 $\lambda$ 为 $A$ 的特征值，则
             $$
             \lambda^2+\lambda-2=0,
             $$
             故 $\lambda=1$ 或 $\lambda=-2$。又
             $$
             |A|=\lambda_1\lambda_2\lambda_3=4,
             $$
             只能是一个特征值为 1、两个特征值为 $-2$。因此实对称矩阵对应二次型经正交变换后有 1 个正平方项、2 个负平方项，规范形为
             $$
             y_1^2-y_2^2-y_3^2.
             $$
             选 C。
             """), ["images/source_pages/page-1.png"]),
    Question(9, "fill_blank", 4, "高等数学", ["指数型极限", "重要极限"],
             md(r"""
             $$
             \lim_{x\to0}(x+2^x)^{2/x}=\underline{\qquad}.
             $$
             """),
             r"$4e^2$",
             md(r"""
             写成
             $$
             (1+x+2^x-1)^{2/x}.
             $$
             由指数型极限，
             $$
             \lim_{x\to0}(1+u)^{2/x}=e^{\lim \frac{2u}{x}},
             $$
             其中
             $$
             u=x+2^x-1.
             $$
             又
             $$
             \lim_{x\to0}\frac{2(x+2^x-1)}{x}=2(1+\ln2),
             $$
             故原极限为
             $$
             e^{2(1+\ln2)}=4e^2.
             $$
             """), ["images/source_pages/page-1.png"]),
    Question(10, "fill_blank", 4, "高等数学", ["参数方程", "切线方程"],
             md(r"""
             曲线
             $$
             \begin{cases}
             x=t-\sin t,\\
             y=1-\cos t
             \end{cases}
             $$
             在 $t=\dfrac{3\pi}{2}$ 对应点处的切线在 $y$ 轴上的截距为 $\underline{\qquad}$。
             """),
             r"$\dfrac{3\pi}{2}+2$",
             md(r"""
             当 $t=\dfrac{3\pi}{2}$ 时，
             $$
             \left(x,y\right)=\left(\frac{3\pi}{2}+1,1\right).
             $$
             又
             $$
             \frac{dy}{dx}=\frac{\sin t}{1-\cos t},
             $$
             故此时斜率为 $-1$。切线方程
             $$
             y-1=-\left(x-\frac{3\pi}{2}-1\right).
             $$
             令 $x=0$ 得截距
             $$
             y=\frac{3\pi}{2}+2.
             $$
             """), ["images/source_pages/page-1.png"]),
    Question(11, "fill_blank", 4, "高等数学", ["复合函数", "偏导数", "齐次性质"],
             md(r"""
             设函数 $f(u)$ 可导，
             $$
             z=yf\!\left(\frac{y^2}{x}\right),
             $$
             则
             $$
             2x\frac{\partial z}{\partial x}+y\frac{\partial z}{\partial y}=\underline{\qquad}.
             $$
             """),
             r"$y\,f\!\left(\dfrac{y^2}{x}\right)$",
             md(r"""
             直接求偏导：
             $$
             \frac{\partial z}{\partial x}=-\frac{y^3}{x^2}f'\!\left(\frac{y^2}{x}\right),
             $$
             $$
             \frac{\partial z}{\partial y}=f\!\left(\frac{y^2}{x}\right)+\frac{2y^2}{x}f'\!\left(\frac{y^2}{x}\right).
             $$
             代入可得
             $$
             2x\frac{\partial z}{\partial x}+y\frac{\partial z}{\partial y}
             =-\frac{2y^3}{x}f'+y f+\frac{2y^3}{x}f'
             =y f\!\left(\frac{y^2}{x}\right).
             $$
             """), ["images/source_pages/page-2.png"]),
    Question(12, "fill_blank", 4, "高等数学", ["弧长", "对数函数"],
             md(r"""
             曲线 $y=\ln\cos x\ (0\le x\le \frac{\pi}{6})$ 的弧长为 $\underline{\qquad}$。
             """),
             r"$\dfrac12\ln3$",
             md(r"""
             有
             $$
             y'=-\tan x,
             $$
             故弧长
             $$
             s=\int_0^{\pi/6}\sqrt{1+\tan^2x}\,dx=\int_0^{\pi/6}\sec x\,dx.
             $$
             计算得
             $$
             s=\ln|\sec x+\tan x|\Big|_0^{\pi/6}
             =\ln\sqrt3=\frac12\ln3.
             $$
             """), ["images/source_pages/page-2.png"]),
    Question(13, "fill_blank", 4, "高等数学", ["定积分", "交换积分次序", "分部积分"],
             md(r"""
             已知函数
             $$
             f(x)=x\int_1^x\frac{\sin t^2}{t}\,dt,
             $$
             则
             $$
             \int_0^1 f(x)\,dx=\underline{\qquad}.
             $$
             """),
             r"$\dfrac{\cos1-1}{4}$",
             md(r"""
             写成
             $$
             \int_0^1 x\left(\int_1^x\frac{\sin t^2}{t}\,dt\right)dx
             =\int_0^1\left(\int_1^x\frac{\sin t^2}{t}\,dt\right)d\left(\frac{x^2}{2}\right).
             $$
             交换处理后化为
             $$
             -\frac12\int_0^1 x\sin x^2\,dx.
             $$
             再令 $u=x^2$，得
             $$
             -\frac14\int_0^1\sin u\,du=\frac{\cos1-1}{4}.
             $$
             """), ["images/source_pages/page-2.png"]),
    Question(14, "fill_blank", 4, "线性代数", ["代数余子式", "行列式展开"],
             md(r"""
             已知矩阵
             $$
             A=
             \begin{pmatrix}
             1&-1&0&0\\
             -2&1&-1&1\\
             3&-2&2&-1\\
             0&0&3&4
             \end{pmatrix},
             $$
             $A_{ij}$ 表示 $|A|$ 中 $(i,j)$ 元的代数余子式，则 $A_{11}-A_{12}=\underline{\qquad}$。
             """),
             "-4",
             md(r"""
             由第一行按代数余子式展开可知
             $$
             A_{11}-A_{12}=|A'|,
             $$
             其中
             $$
             A'=
             \begin{pmatrix}
             1&0&0\\
             -1&-1&1\\
             0&3&4
             \end{pmatrix}
             $$
             等价于相应 3 阶行列式。直接计算得
             $$
             A_{11}-A_{12}=-4.
             $$
             """), ["images/source_pages/page-2.png"]),
    Question(15, "solution", 10, "高等数学", ["分段函数", "导数", "极值"],
             md(r"""
             已知函数
             $$
             f(x)=
             \begin{cases}
             x^{2x},& x>0,\\
             xe^x+1,& x\le 0,
             \end{cases}
             $$
             求 $f'(x)$，并求 $f(x)$ 的极值。
             """),
             md(r"""
             $$
             f'(x)=
             \begin{cases}
             x^{2x}(2\ln x+2),& x>0,\\
             (x+1)e^x,& x<0,
             \end{cases}
             $$
             且 $x=0$ 处不可导。

             极小值点：$x=-1,\ \dfrac1e$，对应极小值分别为 $1-\dfrac1e,\ \left(\dfrac1e\right)^{2/e}$；

             极大值点：$x=0$，极大值为 $1$。
             """),
             md(r"""
             当 $x>0$ 时，
             $$
             f'(x)=(x^{2x})'=x^{2x}(2\ln x+2).
             $$
             当 $x<0$ 时，
             $$
             f'(x)=(xe^x+1)'=(x+1)e^x.
             $$
             由
             $$
             \lim_{x\to0^+}\frac{f(x)-f(0)}{x}
             =\lim_{x\to0^+}\frac{x^{2x}-1}{x}
             =\lim_{x\to0^+}2\ln x=-\infty
             $$
             知 $x=0$ 处不可导。

             临界点与不可导点为 $x=-1,0,\dfrac1e$。结合导数符号：
             $$
             x<-1:\ f'(x)<0,\quad -1<x<0:\ f'(x)>0,
             $$
             $$
             0<x<\frac1e:\ f'(x)<0,\quad x>\frac1e:\ f'(x)>0.
             $$
             故 $x=-1,\dfrac1e$ 为极小值点，$x=0$ 为极大值点，代入即可得各极值。
             """), ["images/source_pages/page-2.png"]),
    Question(16, "solution", 10, "高等数学", ["不定积分", "部分分式"],
             md(r"""
             求不定积分
             $$
             \int \frac{3x+6}{(x-1)^2(x^2+x+1)}\,dx.
             $$
             """),
             md(r"""
             $$
             -2\ln|x-1|-\frac{3}{x-1}+\ln(x^2+x+1)+C.
             $$
             """),
             md(r"""
             作部分分式分解：
             $$
             \frac{3x+6}{(x-1)^2(x^2+x+1)}
             =\frac{A}{x-1}+\frac{B}{(x-1)^2}+\frac{Cx+D}{x^2+x+1}.
             $$
             比较系数得
             $$
             A=-2,\quad B=3,\quad C=2,\quad D=1.
             $$
             因而
             $$
             \int \frac{3x+6}{(x-1)^2(x^2+x+1)}dx
             =\int\left[-\frac{2}{x-1}+\frac{3}{(x-1)^2}+\frac{2x+1}{x^2+x+1}\right]dx,
             $$
             计算后得
             $$
             -2\ln|x-1|-\frac{3}{x-1}+\ln(x^2+x+1)+C.
             $$
             """), ["images/source_pages/page-2.png"]),
    Question(17, "solution", 10, "高等数学", ["一阶线性微分方程", "旋转体体积"],
             md(r"""
             设函数 $y(x)$ 是微分方程
             $$
             y'-xy=\frac{1}{2\sqrt{x}}e^{x^2/2}
             $$
             满足条件 $y(1)=\sqrt e$ 的特解。

             (1) 求 $y(x)$；

             (2) 设平面区域
             $$
             D=\{(x,y)\mid 1\le x\le2,\ 0\le y\le y(x)\},
             $$
             求 $D$ 绕 $x$ 轴旋转所得旋转体的体积。
             """),
             md(r"""
             (1) $y(x)=\sqrt{x}\,e^{x^2/2}$；

             (2) $V=\dfrac{\pi}{2}(e^4-e)$。
             """),
             md(r"""
             这是线性微分方程。乘积分因子 $e^{-x^2/2}$，得
             $$
             \left(ye^{-x^2/2}\right)'=\frac{1}{2\sqrt{x}}.
             $$
             积分后
             $$
             ye^{-x^2/2}=\sqrt{x}+C,
             $$
             即
             $$
             y=(\sqrt{x}+C)e^{x^2/2}.
             $$
             由 $y(1)=\sqrt e$ 得 $C=0$，故
             $$
             y(x)=\sqrt{x}\,e^{x^2/2}.
             $$

             旋转体体积
             $$
             V=\pi\int_1^2 y^2\,dx
             =\pi\int_1^2 xe^{x^2}\,dx
             =\frac{\pi}{2}e^{x^2}\Big|_1^2
             =\frac{\pi}{2}(e^4-e).
             $$
             """), ["images/source_pages/page-2.png"]),
    Question(18, "solution", 10, "高等数学", ["二重积分", "极坐标变换", "对称性"],
             md(r"""
             已知平面区域
             $$
             D=\{(x,y)\mid |x|\le y,\ (x^2+y^2)^3\le y^4\},
             $$
             计算二重积分
             $$
             \iint_D \frac{x+y}{\sqrt{x^2+y^2}}\,dxdy.
             $$
             """),
             r"$\dfrac{43\sqrt2}{120}$",
             md(r"""
             由对称性，含 $x$ 的奇部积分为 $0$，原式化为
             $$
             \iint_D \frac{y}{\sqrt{x^2+y^2}}\,dxdy.
             $$
             取极坐标
             $$
             x=r\cos\theta,\qquad y=r\sin\theta.
             $$
             条件 $|x|\le y$ 化为
             $$
             \frac{\pi}{4}\le\theta\le\frac{3\pi}{4},
             $$
             而
             $$
             (x^2+y^2)^3\le y^4
             $$
             化为
             $$
             0\le r\le \sin^2\theta.
             $$
             所以
             $$
             \iint_D \frac{x+y}{\sqrt{x^2+y^2}}\,dxdy
             =\int_{\pi/4}^{3\pi/4}\int_0^{\sin^2\theta} \sin\theta \cdot r\,dr\,d\theta
             =\frac12\int_{\pi/4}^{3\pi/4}\sin^5\theta\,d\theta
             =\frac{43\sqrt2}{120}.
             $$
             """), ["images/source_pages/page-3.png"]),
    Question(19, "solution", 10, "高等数学", ["定积分", "数列极限", "级数型求和"],
             md(r"""
             设 $n$ 为正整数，记 $S_n$ 为曲线
             $$
             y=e^{-x}\sin x\qquad (0\le x\le n\pi)
             $$
             与 $x$ 轴所围图形的面积，求 $S_n$，并求 $\lim\limits_{n\to\infty}S_n$。
             """),
             md(r"""
             $$
             S_n=\frac12\left[1+\frac{2e^{-\pi}(1-e^{-n\pi})}{1-e^{-\pi}}-e^{-n\pi}\right],
             \qquad
             \lim_{n\to\infty}S_n=\frac12+\frac{1}{e^\pi-1}.
             $$
             """),
             md(r"""
             面积按每段正负交替求和：
             $$
             S_n=\sum_{k=0}^{n-1}(-1)^k\int_{k\pi}^{(k+1)\pi}e^{-x}\sin x\,dx.
             $$
             原函数可取
             $$
             \int e^{-x}\sin x\,dx=-\frac12e^{-x}(\sin x+\cos x).
             $$
             代入端点并整理等比和，得到
             $$
             S_n=\frac12\left[1+2\sum_{k=1}^{n-1}e^{-k\pi}-e^{-n\pi}\right]
             =\frac12\left[1+\frac{2e^{-\pi}(1-e^{-n\pi})}{1-e^{-\pi}}-e^{-n\pi}\right].
             $$
             令 $n\to\infty$ 即得
             $$
             \lim_{n\to\infty}S_n=\frac12+\frac{1}{e^\pi-1}.
             $$
             """), ["images/source_pages/page-3.png"]),
    Question(20, "solution", 11, "高等数学", ["偏微分方程", "变量代换", "消一阶项"],
             md(r"""
             已知函数 $u(x,y)$ 满足
             $$
             2\frac{\partial^2u}{\partial x^2}-2\frac{\partial^2u}{\partial y^2}+3\frac{\partial u}{\partial x}+3\frac{\partial u}{\partial y}=0,
             $$
             求 $a,b$ 的值，使得在变换
             $$
             u(x,y)=v(x,y)e^{ax+by}
             $$
             下，上述等式可化为 $v(x,y)$ 不含一阶偏导数的等式。
             """),
             md(r"$a=-\dfrac34,\quad b=\dfrac34$"),
             md(r"""
             将
             $$
             u=v e^{ax+by}
             $$
             代入，计算偏导后可得关于 $v$ 的方程：
             $$
             2v_{xx}-2v_{yy}+(4a+3)v_x+(3-4b)v_y+(2a^2-2b^2+3a+3b)v=0.
             $$
             要消去一阶偏导项，只需
             $$
             4a+3=0,\qquad 3-4b=0.
             $$
             解得
             $$
             a=-\frac34,\qquad b=\frac34.
             $$
             """), ["images/source_pages/page-3.png"]),
    Question(21, "proof", 11, "高等数学", ["积分中值定理", "罗尔定理", "拉格朗日中值定理"],
             md(r"""
             已知函数 $f(x)$ 在 $[0,1]$ 上具有 2 阶导数，且
             $$
             f(0)=0,\qquad f(1)=1,\qquad \int_0^1f(x)\,dx=1,
             $$
             证明：

             (I) 存在 $\xi\in(0,1)$，使得 $f'(\xi)=0$；

             (II) 存在 $\eta\in(0,1)$，使得 $f''(\eta)<-2$。
             """),
             "结论成立",
             md(r"""
             设
             $$
             F(x)=\int_0^x f(t)\,dt,
             $$
             则 $F'(x)=f(x)$。由积分中值定理，存在 $c\in(0,1)$ 使
             $$
             \int_0^1f(x)\,dx=f(c)(1-0),
             $$
             即 $f(c)=1$。而已知 $f(1)=1$，故由罗尔定理，存在 $\xi\in(c,1)\subset(0,1)$ 使
             $$
             f'(\xi)=0.
             $$

             再设
             $$
             \varphi(x)=f(x)+x^2.
             $$
             则
             $$
             \varphi(0)=0,\qquad \varphi(c)=1+c^2,\qquad \varphi(1)=2.
             $$
             由拉格朗日中值定理，存在 $\eta_1\in(0,c),\ \eta_2\in(c,1)$ 使
             $$
             \varphi'(\eta_1)=\frac{1+c^2}{c}=c+\frac1c,\qquad
             \varphi'(\eta_2)=\frac{2-(1+c^2)}{1-c}=1+c.
             $$
             再对 $\varphi'$ 用拉格朗日中值定理，存在 $\eta\in(\eta_1,\eta_2)$ 使
             $$
             \varphi''(\eta)=\frac{\varphi'(\eta_2)-\varphi'(\eta_1)}{\eta_2-\eta_1}
             =\frac{1-\frac1c}{\eta_2-\eta_1}<0.
             $$
             又 $\varphi''=f''+2$，故
             $$
             f''(\eta)+2<0 \Rightarrow f''(\eta)<-2.
             $$
             """), ["images/source_pages/page-4.png"]),
    Question(22, "solution", 11, "线性代数", ["向量组等价", "秩", "线性表示"],
             md(r"""
             已知向量组 I：
             $$
             \alpha_1=\begin{pmatrix}1\\1\\4\end{pmatrix},\quad
             \alpha_2=\begin{pmatrix}1\\0\\4\end{pmatrix},\quad
             \alpha_3=\begin{pmatrix}1\\2\\a^2+3\end{pmatrix}
             $$
             与 II：
             $$
             \beta_1=\begin{pmatrix}1\\1\\a+3\end{pmatrix},\quad
             \beta_2=\begin{pmatrix}0\\2\\1-a\end{pmatrix},\quad
             \beta_3=\begin{pmatrix}1\\3\\a^2+3\end{pmatrix}.
             $$
             若向量组 I 与 II 等价，求 $a$ 的取值，并将 $\beta_3$ 用 $\alpha_1,\alpha_2,\alpha_3$ 线性表示。
             """),
             md(r"""
             $a\ne-1$。

             当 $a\ne\pm1$ 时，
             $$
             \beta_3=\alpha_1-\alpha_2+\alpha_3.
             $$

             当 $a=1$ 时，也有
             $$
             \beta_3=\alpha_1-\alpha_2+\alpha_3,
             $$
             亦可写成
             $$
             \beta_3=(-2k+3)\alpha_1+(k-2)\alpha_2+k\alpha_3\quad (k\in\mathbb R).
             $$
             """),
             md(r"""
             先算两组向量的秩。对
             $$
             (\alpha_1,\alpha_2,\alpha_3)
             $$
             作消元，可得其秩在 $a=-1$ 时为 $2$，在 $a\ne-1$ 时不小于 $2$。再对
             $$
             (\beta_1,\beta_2,\beta_3)
             $$
             以及联合向量组
             $$
             (\alpha_1,\alpha_2,\alpha_3,\beta_1,\beta_2,\beta_3)
             $$
             消元比较。

             当 $a=-1$ 时，两组与联合组秩不一致，因此不等价。

             当 $a=1$ 时，两组及联合组秩都为 $2$，故等价。解方程
             $$
             x_1\alpha_1+x_2\alpha_2+x_3\alpha_3=\beta_3
             $$
             可得一族表示
             $$
             \beta_3=(-2k+3)\alpha_1+(k-2)\alpha_2+k\alpha_3.
             $$

             当 $a\ne\pm1$ 时，两组与联合组秩都为 $3$，故等价，并且表示唯一。解线性方程组得
             $$
             \beta_3=\alpha_1-\alpha_2+\alpha_3.
             $$
             综上，等价所需且所求为 $a\ne-1$。
             """), ["images/source_pages/page-4.png"]),
    Question(23, "solution", 11, "线性代数", ["矩阵相似", "特征值", "对角化"],
             md(r"""
             已知矩阵
             $$
             A=
             \begin{pmatrix}
             -2&-2&1\\
             2&x&-2\\
             0&0&-2
             \end{pmatrix}
             $$
             与
             $$
             B=
             \begin{pmatrix}
             2&1&0\\
             0&-1&0\\
             0&0&y
             \end{pmatrix}
             $$
             相似。

             (I) 求 $x,y$；

             (II) 求可逆矩阵 $P$，使得 $P^{-1}AP=B$。
             """),
             md(r"""
             (I) $x=3,\ y=-2$；

             (II) 可取
             $$
             P=
             \begin{pmatrix}
             -1&-1&-1\\
             2&1&2\\
             0&0&4
             \end{pmatrix}.
             $$
             """),
             md(r"""
             因为 $A\sim B$，所以迹与行列式分别相等。
             $$
             \operatorname{tr}(A)=x-4,\qquad \operatorname{tr}(B)=y+1,
             $$
             故
             $$
             y=x-5.
             $$
             又
             $$
             |A|=-2(-2x+4),\qquad |B|=-2y,
             $$
             所以
             $$
             y=-2x+4.
             $$
             联立得
             $$
             x=3,\qquad y=-2.
             $$

             于是
             $$
             A=
             \begin{pmatrix}
             -2&-2&1\\
             2&3&-2\\
             0&0&-2
             \end{pmatrix},\qquad
             B=
             \begin{pmatrix}
             2&1&0\\
             0&-1&0\\
             0&0&-2
             \end{pmatrix}.
             $$
             求得 $A$ 属于特征值 $-2,-1,2$ 的线性无关特征向量可分别取
             $$
             \alpha_1=\begin{pmatrix}-1\\2\\4\end{pmatrix},\quad
             \alpha_2=\begin{pmatrix}-2\\1\\0\end{pmatrix},\quad
             \alpha_3=\begin{pmatrix}-1\\2\\0\end{pmatrix}.
             $$
             于是
             $$
             P_1=(\alpha_1,\alpha_2,\alpha_3),\qquad
             P_1^{-1}AP_1=\operatorname{diag}(-2,-1,2).
             $$
             同理取 $B$ 的相应特征向量组构成 $P_2$，可使
             $$
             P_2^{-1}BP_2=\operatorname{diag}(-2,-1,2).
             $$
             因而
             $$
             P=P_1P_2^{-1}
             $$
             即可。按答案页给出的一个可取值为
             $$
             P=
             \begin{pmatrix}
             -1&-1&-1\\
             2&1&2\\
             0&0&4
             \end{pmatrix}.
             $$
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
        "整理状态：按真题 PDF 与答案解析页图交叉校对整理。",
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
        "整理状态：基于答案解析页图与题面交叉清洗。",
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
