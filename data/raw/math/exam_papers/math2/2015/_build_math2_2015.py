from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from textwrap import dedent

from PIL import Image


ROOT = Path(__file__).resolve().parent
YEAR = 2015


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
    if len(brief) > 48 or "\\begin{pmatrix}" in brief:
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
    Question(
        number=1,
        question_type="single_choice",
        score=4,
        module="高等数学",
        topics=["反常积分", "广义积分敛散性", "分部积分"],
        stem=md(
            r"""
            下列反常积分收敛的是（ ）

            (A) $\displaystyle \int_2^{+\infty}\frac{1}{\sqrt{x}}\,dx$

            (B) $\displaystyle \int_2^{+\infty}\frac{\ln x}{x}\,dx$

            (C) $\displaystyle \int_2^{+\infty}\frac{1}{x\ln x}\,dx$

            (D) $\displaystyle \int_2^{+\infty}\frac{x}{e^x}\,dx$
            """
        ),
        answer="D",
        explanation=md(
            r"""
            对 (D)，有
            $$
            \int xe^{-x}\,dx=-(x+1)e^{-x}+C,
            $$
            因此
            $$
            \int_2^{+\infty}\frac{x}{e^x}\,dx
            =\left[-(x+1)e^{-x}\right]_2^{+\infty}
            =3e^{-2},
            $$
            所以收敛。

            其余三项分别与
            $\int x^{-1/2}\,dx$、
            $\int \dfrac{\ln x}{x}\,dx$、
            $\int \dfrac{1}{x\ln x}\,dx$
            同型，均发散。
            """
        ),
        assets=["images/source_pages/page-1.png"],
    ),
    Question(
        number=2,
        question_type="single_choice",
        score=4,
        module="高等数学",
        topics=["函数极限", "重要极限", "间断点类型", "指数型极限"],
        stem=md(
            r"""
            函数
            $$
            f(x)=\lim_{t\to 0}\left(1+\frac{\sin t}{x}\right)^{\frac{x^2}{t}}
            $$
            在 $(-\infty,+\infty)$ 内（ ）

            (A) 连续

            (B) 有可去间断点

            (C) 有跳跃间断点

            (D) 有无穷间断点
            """
        ),
        answer="B",
        explanation=md(
            r"""
            当 $x\ne 0$ 时，
            $$
            f(x)=\exp\!\left(\lim_{t\to 0}\frac{\sin t}{x}\cdot \frac{x^2}{t}\right)
            =e^x.
            $$
            因而 $x=0$ 是唯一可能的间断点。

            又
            $$
            \lim_{x\to 0}f(x)=\lim_{x\to 0}e^x=1,
            $$
            只需补定义 $f(0)=1$ 就可使其连续，所以它在 $x=0$ 处有可去间断点。
            """
        ),
        assets=["images/source_pages/page-1.png"],
    ),
    Question(
        number=3,
        question_type="single_choice",
        score=4,
        module="高等数学",
        topics=["导数连续性", "分段函数", "振荡函数极限", "参数范围判定"],
        stem=md(
            r"""
            设函数
            $$
            f(x)=
            \begin{cases}
            x^\alpha\cos\!\left(\dfrac{1}{x^\beta}\right), & x>0,\\
            0, & x\le 0,
            \end{cases}
            \qquad (\alpha>0,\ \beta>0),
            $$
            若 $f'(x)$ 在 $x=0$ 处连续，则（ ）

            (A) $\alpha-\beta>0$

            (B) $0<\alpha-\beta\le 1$

            (C) $\alpha-\beta>2$

            (D) $0<\alpha-\beta\le 2$
            """
        ),
        answer="A",
        explanation=md(
            r"""
            对 $x<0$，有 $f'(x)=0$，故 $f'_-(0)=0$。

            对 $x>0$，
            $$
            f'(x)=\alpha x^{\alpha-1}\cos\!\left(\frac{1}{x^\beta}\right)
            +\beta x^{\alpha-\beta-1}\sin\!\left(\frac{1}{x^\beta}\right).
            $$
            要使 $f'(x)$ 在 $x=0$ 处连续，需 $\lim\limits_{x\to 0^+}f'(x)=0$，
            从而必须有
            $$
            \alpha-1>0,\qquad \alpha-\beta-1>0.
            $$
            尤其有 $\alpha-\beta>0$，故选 A。
            """
        ),
        assets=["images/source_pages/page-1.png"],
    ),
    Question(
        number=4,
        question_type="single_choice",
        score=4,
        module="高等数学",
        topics=["二阶导数", "曲线拐点", "图像判定"],
        stem=md(
            r"""
            设函数 $f(x)$ 在 $(-\infty,+\infty)$ 内连续，其中二阶导数 $f''(x)$ 的图形如图所示，则曲线
            $$
            y=f(x)
            $$
            的拐点个数为（ ）

            (A) $0$

            (B) $1$

            (C) $2$

            (D) $3$
            """
        ),
        answer="C",
        explanation=md(
            r"""
            拐点对应于 $f''(x)$ 变号的点。由图像可见，$f''(x)$ 恰有两处变号，
            因此曲线 $y=f(x)$ 有两个拐点，故选 C。
            """
        ),
        assets=["images/q004_diagram.png"],
    ),
    Question(
        number=5,
        question_type="single_choice",
        score=4,
        module="高等数学",
        topics=["二元函数", "偏导数", "变量代换", "复合函数"],
        stem=md(
            r"""
            设函数 $f(u,v)$ 满足
            $$
            f\!\left(x+y,\frac{y}{x}\right)=x^2-y^2,
            $$
            则
            $$
            \left.\frac{\partial f}{\partial u}\right|_{(1,1)}
            \quad\text{与}\quad
            \left.\frac{\partial f}{\partial v}\right|_{(1,1)}
            $$
            依次是（ ）

            (A) $\left(\dfrac12,0\right)$

            (B) $\left(0,\dfrac12\right)$

            (C) $\left(-\dfrac12,0\right)$

            (D) $\left(0,-\dfrac12\right)$
            """
        ),
        answer="D",
        explanation=md(
            r"""
            令
            $$
            u=x+y,\qquad v=\frac{y}{x},
            $$
            解得
            $$
            x=\frac{u}{1+v},\qquad y=\frac{uv}{1+v}.
            $$
            于是
            $$
            f(u,v)=x^2-y^2
            =\left(\frac{u}{1+v}\right)^2-\left(\frac{uv}{1+v}\right)^2
            =\frac{u^2(1-v)}{1+v}.
            $$
            因而
            $$
            \frac{\partial f}{\partial u}=\frac{2u(1-v)}{1+v},\qquad
            \frac{\partial f}{\partial v}=-\frac{2u^2}{(1+v)^2}.
            $$
            在 $(u,v)=(1,1)$ 处有
            $$
            \left.\frac{\partial f}{\partial u}\right|_{(1,1)}=0,\qquad
            \left.\frac{\partial f}{\partial v}\right|_{(1,1)}=-\frac12.
            $$
            故选 D。
            """
        ),
        assets=["images/source_pages/page-1.png"],
    ),
    Question(
        number=6,
        question_type="single_choice",
        score=4,
        module="高等数学",
        topics=["二重积分", "极坐标变换", "积分区域表示", "第一象限曲边区域"],
        stem=md(
            r"""
            设 $D$ 是第一象限内由曲线 $2xy=1$、$4xy=1$ 与直线 $y=x$、$y=\sqrt3\,x$ 围成的平面区域，
            函数 $f(x,y)$ 在 $D$ 上连续，则
            $$
            \iint_D f(x,y)\,dxdy
            $$
            等于（ ）

            (A) $\displaystyle \int_{\pi/4}^{\pi/3}d\theta\int_{\frac{1}{2\sin2\theta}}^{\frac{1}{\sin2\theta}}f(r\cos\theta,r\sin\theta)\,dr$

            (B) $\displaystyle \int_{\pi/4}^{\pi/3}d\theta\int_{\frac{1}{\sqrt{2\sin2\theta}}}^{\frac{1}{\sqrt{\sin2\theta}}}f(r\cos\theta,r\sin\theta)\,r\,dr$

            (C) $\displaystyle \int_{\pi/4}^{\pi/3}d\theta\int_{\frac{1}{2\sin2\theta}}^{\frac{1}{\sin2\theta}}f(r\cos\theta,r\sin\theta)\,r\,dr$

            (D) $\displaystyle \int_{\pi/4}^{\pi/3}d\theta\int_{\frac{1}{\sqrt{2\sin2\theta}}}^{\frac{1}{\sqrt{\sin2\theta}}}f(r\cos\theta,r\sin\theta)\,dr$
            """
        ),
        answer="B",
        explanation=md(
            r"""
            改用极坐标
            $$
            x=r\cos\theta,\qquad y=r\sin\theta.
            $$
            由直线边界得
            $$
            \theta=\frac{\pi}{4},\qquad \theta=\frac{\pi}{3}.
            $$
            由双曲线边界
            $$
            2xy=1,\qquad 4xy=1
            $$
            分别得到
            $$
            r=\frac{1}{\sqrt{\sin2\theta}},\qquad
            r=\frac{1}{\sqrt{2\sin2\theta}}.
            $$
            因而
            $$
            D=\left\{(r,\theta)\ \middle|\ \frac{\pi}{4}\le\theta\le\frac{\pi}{3},
            \ \frac{1}{\sqrt{2\sin2\theta}}\le r\le\frac{1}{\sqrt{\sin2\theta}}\right\}.
            $$
            再乘雅可比 $r$，故选 B。
            """
        ),
        assets=["images/source_pages/page-1.png"],
    ),
    Question(
        number=7,
        question_type="single_choice",
        score=4,
        module="线性代数",
        topics=["线性方程组", "增广矩阵", "无穷多解", "秩"],
        stem=md(
            r"""
            设矩阵
            $$
            A=\begin{pmatrix}
            1&1&1\\
            1&2&a\\
            1&4&a^2
            \end{pmatrix},
            \qquad
            b=\begin{pmatrix}
            1\\ d\\ d^2
            \end{pmatrix}.
            $$
            若集合 $\Omega=\{1,2\}$，则线性方程组 $Ax=b$ 有无穷多解的充分必要条件为（ ）

            (A) $a\notin\Omega,\ d\notin\Omega$

            (B) $a\notin\Omega,\ d\in\Omega$

            (C) $a\in\Omega,\ d\notin\Omega$

            (D) $a\in\Omega,\ d\in\Omega$
            """
        ),
        answer="D",
        explanation=md(
            r"""
            对增广矩阵作初等变换：
            $$
            (A,b)\sim
            \begin{pmatrix}
            1&1&1&1\\
            0&1&a-1&d-1\\
            0&0&(a-1)(a-2)&(d-1)(d-2)
            \end{pmatrix}.
            $$
            要使方程组有无穷多解，必须满足
            $$
            r(A)=r(A,b)<3.
            $$
            这等价于
            $$
            (a-1)(a-2)=0,\qquad (d-1)(d-2)=0,
            $$
            即 $a\in\{1,2\}$ 且 $d\in\{1,2\}$。
            故选 D。
            """
        ),
        assets=["images/source_pages/page-2.png"],
    ),
    Question(
        number=8,
        question_type="single_choice",
        score=4,
        module="线性代数",
        topics=["二次型", "正交变换", "标准形"],
        stem=md(
            r"""
            设二次型 $f(x_1,x_2,x_3)$ 在正交变换 $x=Py$ 下的标准形为
            $$
            2y_1^2+y_2^2-y_3^2,
            $$
            其中 $P=(e_1,e_2,e_3)$。若
            $$
            Q=(e_1,-e_3,e_2),
            $$
            则 $f(x_1,x_2,x_3)$ 在正交变换 $x=Qy$ 下的标准形为（ ）

            (A) $2y_1^2-y_2^2+y_3^2$

            (B) $2y_1^2+y_2^2-y_3^2$

            (C) $2y_1^2-y_2^2-y_3^2$

            (D) $2y_1^2+y_2^2+y_3^2$
            """
        ),
        answer="A",
        explanation=md(
            r"""
            由 $x=Py$，可知
            $$
            f=x^{\mathsf T}Ax=y^{\mathsf T}(P^{\mathsf T}AP)y
            =2y_1^2+y_2^2-y_3^2,
            $$
            因而
            $$
            P^{\mathsf T}AP=
            \begin{pmatrix}
            2&0&0\\
            0&1&0\\
            0&0&-1
            \end{pmatrix}.
            $$
            又
            $$
            Q=PC,\qquad
            C=
            \begin{pmatrix}
            1&0&0\\
            0&0&1\\
            0&-1&0
            \end{pmatrix},
            $$
            所以
            $$
            Q^{\mathsf T}AQ=C^{\mathsf T}(P^{\mathsf T}AP)C=
            \begin{pmatrix}
            2&0&0\\
            0&-1&0\\
            0&0&1
            \end{pmatrix}.
            $$
            因此新标准形为
            $$
            2y_1^2-y_2^2+y_3^2,
            $$
            故选 A。
            """
        ),
        assets=["images/source_pages/page-2.png"],
    ),
    Question(
        number=9,
        question_type="fill_blank",
        score=4,
        module="高等数学",
        topics=["参数方程求导", "二阶导数"],
        stem=md(
            r"""
            设
            $$
            \begin{cases}
            x=\arctan t,\\
            y=3t+t^3,
            \end{cases}
            $$
            则
            $$
            \left.\frac{d^2y}{dx^2}\right|_{t=1}=\underline{\qquad}.
            $$
            """
        ),
        answer="48",
        explanation=md(
            r"""
            由参数方程求导，
            $$
            \frac{dy}{dx}=\frac{dy/dt}{dx/dt}
            =\frac{3+3t^2}{1/(1+t^2)}=3(1+t^2)^2.
            $$
            再对 $x$ 求导：
            $$
            \frac{d^2y}{dx^2}
            =\frac{d[3(1+t^2)^2]/dt}{dx/dt}
            =\frac{12t(1+t^2)}{1/(1+t^2)}
            =12t(1+t^2)^2.
            $$
            代入 $t=1$，得
            $$
            \left.\frac{d^2y}{dx^2}\right|_{t=1}=48.
            $$
            """
        ),
        assets=["images/source_pages/page-2.png"],
    ),
    Question(
        number=10,
        question_type="fill_blank",
        score=4,
        module="高等数学",
        topics=["高阶导数", "莱布尼茨公式", "指数函数"],
        stem=md(
            r"""
            函数
            $$
            f(x)=x^2\cdot 2^x
            $$
            在 $x=0$ 处的 $n$ 阶导数
            $$
            f^{(n)}(0)=\underline{\qquad}.
            $$
            """
        ),
        answer=r"$n(n-1)(\ln 2)^{n-2}$",
        explanation=md(
            r"""
            由莱布尼茨公式，
            $$
            f^{(n)}(0)=\sum_{k=0}^n\binom{n}{k}(x^2)^{(k)}(2^x)^{(n-k)}\Big|_{x=0}.
            $$
            只有 $k=2$ 项不为零，因此
            $$
            f^{(n)}(0)=\binom{n}{2}\cdot 2\cdot (\ln 2)^{n-2}
            =n(n-1)(\ln 2)^{n-2}.
            $$
            """
        ),
        assets=["images/source_pages/page-2.png"],
    ),
    Question(
        number=11,
        question_type="fill_blank",
        score=4,
        module="高等数学",
        topics=["积分上限函数", "乘积求导", "牛顿-莱布尼茨公式"],
        stem=md(
            r"""
            设 $f(x)$ 连续，
            $$
            \varphi(x)=\int_0^{x^2}x f(t)\,dt.
            $$
            若 $\varphi(1)=1,\ \varphi'(1)=5$，则
            $$
            f(1)=\underline{\qquad}.
            $$
            """
        ),
        answer="2",
        explanation=md(
            r"""
            将 $x$ 看作积分号外的因子，有
            $$
            \varphi(x)=x\int_0^{x^2}f(t)\,dt.
            $$
            故
            $$
            \varphi'(x)=\int_0^{x^2}f(t)\,dt+2x^2f(x^2).
            $$
            代入 $x=1$，得
            $$
            \varphi(1)=\int_0^1f(t)\,dt=1,
            $$
            又
            $$
            \varphi'(1)=1+2f(1)=5,
            $$
            所以 $f(1)=2$。
            """
        ),
        assets=["images/source_pages/page-2.png"],
    ),
    Question(
        number=12,
        question_type="fill_blank",
        score=4,
        module="高等数学",
        topics=["二阶常系数线性微分方程", "特征方程", "初值条件"],
        stem=md(
            r"""
            设函数 $y=y(x)$ 是微分方程
            $$
            y''+y'-2y=0
            $$
            的解，且在 $x=0$ 处 $y(x)$ 取得极值 $3$，则
            $$
            y(x)=\underline{\qquad}.
            $$
            """
        ),
        answer=r"$e^{-2x}+2e^x$",
        explanation=md(
            r"""
            由题意知
            $$
            y(0)=3,\qquad y'(0)=0.
            $$
            特征方程为
            $$
            \lambda^2+\lambda-2=0,
            $$
            解得 $\lambda_1=1,\ \lambda_2=-2$。
            因而通解为
            $$
            y=C_1e^x+C_2e^{-2x}.
            $$
            代入初值条件
            $$
            C_1+C_2=3,\qquad C_1-2C_2=0,
            $$
            解得 $C_1=2,\ C_2=1$，所以
            $$
            y=2e^x+e^{-2x}.
            $$
            """
        ),
        assets=["images/source_pages/page-2.png"],
    ),
    Question(
        number=13,
        question_type="fill_blank",
        score=4,
        module="高等数学",
        topics=["隐函数微分", "全微分", "指数函数"],
        stem=md(
            r"""
            若函数 $Z=z(x,y)$ 由方程
            $$
            e^{x+2y+3z}+xyz=1
            $$
            确定，则
            $$
            dz\big|_{(0,0)}=\underline{\qquad}.
            $$
            """
        ),
        answer=r"$-\dfrac13(dx+2dy)$",
        explanation=md(
            r"""
            当 $x=0,\ y=0$ 时，由
            $$
            e^{x+2y+3z}+xyz=1
            $$
            得 $z=0$。

            对原式分别对 $x,y$ 求偏导，得到
            $$
            (3e^{x+2y+3z}+xy)\frac{\partial z}{\partial x}=-yz-e^{x+2y+3z},
            $$
            $$
            (3e^{x+2y+3z}+xy)\frac{\partial z}{\partial y}=-xz-2e^{x+2y+3z}.
            $$
            代入 $(0,0,0)$，得
            $$
            \left.\frac{\partial z}{\partial x}\right|_{(0,0)}=-\frac13,\qquad
            \left.\frac{\partial z}{\partial y}\right|_{(0,0)}=-\frac23.
            $$
            因而
            $$
            dz\big|_{(0,0)}=-\frac13\,dx-\frac23\,dy
            =-\frac13(dx+2dy).
            $$
            """
        ),
        assets=["images/source_pages/page-2.png"],
    ),
    Question(
        number=14,
        question_type="fill_blank",
        score=4,
        module="线性代数",
        topics=["特征值", "矩阵多项式", "行列式"],
        stem=md(
            r"""
            若 $3$ 阶矩阵 $A$ 的特征值为 $2,-2,1$，
            $$
            B=A^2-A+E,
            $$
            其中 $E$ 为 $3$ 阶单位阵，则
            $$
            |B|=\underline{\qquad}.
            $$
            """
        ),
        answer="21",
        explanation=md(
            r"""
            由矩阵多项式的特征值对应关系，$A$ 的特征值 $2,-2,1$
            经变换 $\lambda^2-\lambda+1$ 后，
            $B$ 的特征值分别为
            $$
            2^2-2+1=3,\qquad (-2)^2-(-2)+1=7,\qquad 1^2-1+1=1.
            $$
            故
            $$
            |B|=3\cdot 7\cdot 1=21.
            $$
            """
        ),
        assets=["images/source_pages/page-2.png"],
    ),
    Question(
        number=15,
        question_type="solution",
        score=10,
        module="高等数学",
        topics=["等价无穷小", "泰勒展开", "参数求值"],
        stem=md(
            r"""
            设函数
            $$
            f(x)=x+a\ln(1+x)+bx\sin x,\qquad g(x)=kx^3.
            $$
            若 $f(x)$ 与 $g(x)$ 在 $x\to 0$ 时是等价无穷小，求 $a,b,k$ 的值。
            """
        ),
        answer=r"$a=-1,\ b=-\dfrac12,\ k=-\dfrac13$",
        explanation=md(
            r"""
            由
            $$
            \ln(1+x)=x-\frac{x^2}{2}+\frac{x^3}{3}+o(x^3),\qquad
            \sin x=x-\frac{x^3}{6}+o(x^3),
            $$
            得
            $$
            f(x)=x+a\left(x-\frac{x^2}{2}+\frac{x^3}{3}\right)+bx\left(x-\frac{x^3}{6}\right)+o(x^3).
            $$
            整理为
            $$
            f(x)=(1+a)x+\left(b-\frac{a}{2}\right)x^2+\frac{a}{3}x^3+o(x^3).
            $$
            因 $f(x)\sim g(x)=kx^3$，必须满足
            $$
            1+a=0,\qquad b-\frac{a}{2}=0,\qquad \frac{a}{3}=k.
            $$
            解得
            $$
            a=-1,\qquad b=-\frac12,\qquad k=-\frac13.
            $$
            """
        ),
        assets=["images/source_pages/page-3.png"],
    ),
    Question(
        number=16,
        question_type="solution",
        score=10,
        module="高等数学",
        topics=["定积分应用", "旋转体体积", "柱壳法"],
        stem=md(
            r"""
            设 $A>0$，$D$ 是由曲线段
            $$
            y=A\sin x\qquad \left(0\le x\le \frac{\pi}{2}\right)
            $$
            及直线 $y=0$、$x=\dfrac{\pi}{2}$ 所围成的平面区域。$V_1,V_2$ 分别表示 $D$ 绕 $x$ 轴与绕 $y$ 轴旋转成旋转体的体积，若 $V_1=V_2$，求 $A$ 的值。
            """
        ),
        answer=r"$A=\dfrac{8}{\pi}$",
        explanation=md(
            r"""
            绕 $x$ 轴旋转时，
            $$
            V_1=\pi\int_0^{\pi/2}(A\sin x)^2\,dx
            =\pi A^2\int_0^{\pi/2}\sin^2x\,dx
            =\pi A^2\cdot \frac{\pi}{4}
            =\frac{\pi^2A^2}{4}.
            $$
            绕 $y$ 轴旋转时，用柱壳法：
            $$
            V_2=2\pi\int_0^{\pi/2}x(A\sin x)\,dx.
            $$
            分部积分可得
            $$
            \int_0^{\pi/2}x\sin x\,dx=1,
            $$
            因而
            $$
            V_2=2\pi A.
            $$
            由 $V_1=V_2$ 得
            $$
            \frac{\pi^2A^2}{4}=2\pi A.
            $$
            因 $A>0$，解得
            $$
            A=\frac{8}{\pi}.
            $$
            """
        ),
        assets=["images/source_pages/page-3.png"],
    ),
    Question(
        number=17,
        question_type="solution",
        score=11,
        module="高等数学",
        topics=["多元函数微分学", "二元函数极值", "偏导与积分还原函数"],
        stem=md(
            r"""
            已知函数 $f(x,y)$ 满足
            $$
            f''_{xy}(x,y)=2(y+1)e^x,\qquad
            f'_x(x,0)=(x+1)e^x,\qquad
            f(0,y)=y^2+2y,
            $$
            求 $f(x,y)$ 的极值。
            """
        ),
        answer=r"极小值为 $-1$，在点 $(0,-1)$ 处取得",
        explanation=md(
            r"""
            先由
            $$
            f''_{xy}(x,y)=2(y+1)e^x
            $$
            对 $y$ 积分，得
            $$
            f'_x(x,y)=(y^2+2y)e^x+\varphi(x).
            $$
            再由 $f'_x(x,0)=(x+1)e^x$，得
            $$
            \varphi(x)=(x+1)e^x.
            $$
            因而
            $$
            f'_x(x,y)=(y^2+2y)e^x+(x+1)e^x.
            $$
            再对 $x$ 积分，
            $$
            f(x,y)=(y^2+2y)e^x+xe^x+C(y).
            $$
            由 $f(0,y)=y^2+2y$ 得 $C(y)=0$，所以
            $$
            f(x,y)=e^x(x+y^2+2y).
            $$

            求驻点：由
            $$
            f_x=e^x(x+y^2+2y+1),\qquad
            f_y=2(y+1)e^x,
            $$
            得 $y=-1$，代回得 $x=0$，故唯一驻点为 $(0,-1)$。

            再求二阶偏导：
            $$
            f_{xx}=e^x(x+y^2+2y+2),\quad
            f_{xy}=2(y+1)e^x,\quad
            f_{yy}=2e^x.
            $$
            在 $(0,-1)$ 处有
            $$
            f_{xx}=1,\qquad f_{xy}=0,\qquad f_{yy}=2.
            $$
            因而
            $$
            f_{xx}f_{yy}-f_{xy}^2=2>0,\qquad f_{xx}>0,
            $$
            所以 $(0,-1)$ 是极小点。

            极小值为
            $$
            f(0,-1)=-1.
            $$
            """
        ),
        assets=["images/source_pages/page-3.png"],
    ),
    Question(
        number=18,
        question_type="solution",
        score=10,
        module="高等数学",
        topics=["二重积分", "对称性", "积分区域", "三角代换"],
        stem=md(
            r"""
            计算二重积分
            $$
            \iint_D x(x+y)\,dxdy,
            $$
            其中
            $$
            D=\{(x,y)\mid x^2+y^2\le 2,\ y\ge x^2\}.
            $$
            """
        ),
        answer=r"$\dfrac{\pi}{4}-\dfrac{2}{5}$",
        explanation=md(
            r"""
            由积分区域关于 $y$ 轴对称，且 $xy$ 关于 $y$ 轴为奇函数，
            所以
            $$
            \iint_D xy\,dxdy=0.
            $$
            因而原积分化为
            $$
            \iint_D x^2\,dxdy.
            $$
            可写成
            $$
            2\int_0^1\int_{x^2}^{\sqrt{2-x^2}}x^2\,dydx
            =2\int_0^1x^2\bigl(\sqrt{2-x^2}-x^2\bigr)\,dx.
            $$
            即
            $$
            2\int_0^1x^2\sqrt{2-x^2}\,dx-\frac{2}{5}.
            $$
            令 $x=\sqrt2\sin t$，则
            $$
            2\int_0^1x^2\sqrt{2-x^2}\,dx
            =2\int_0^{\pi/4}2\sin^2t\cdot \sqrt2\cos t\cdot \sqrt2\cos t\,dt
            =4\int_0^{\pi/4}\sin^2t\cos^2t\,dt.
            $$
            又
            $$
            4\sin^2t\cos^2t=\sin^22t,
            $$
            因而
            $$
            4\int_0^{\pi/4}\sin^2t\cos^2t\,dt
            =\int_0^{\pi/4}\sin^22t\,dt
            =\frac12\int_0^{\pi/2}\sin^2u\,du
            =\frac{\pi}{4}.
            $$
            所以原积分为
            $$
            \frac{\pi}{4}-\frac{2}{5}.
            $$
            """
        ),
        assets=["images/source_pages/page-3.png"],
    ),
    Question(
        number=19,
        question_type="solution",
        score=11,
        module="高等数学",
        topics=["积分函数", "单调性", "零点个数"],
        stem=md(
            r"""
            已知函数
            $$
            f(x)=\int_x^1\sqrt{1+t^2}\,dt+\int_1^{x^2}\sqrt{1+t}\,dt,
            $$
            求 $f(x)$ 零点的个数。
            """
        ),
        answer="2 个",
        explanation=md(
            r"""
            由变上限积分求导，
            $$
            f'(x)=-\sqrt{1+x^2}+2x\sqrt{1+x^2}
            =\sqrt{1+x^2}(2x-1).
            $$
            因此驻点为 $x=\dfrac12$，且
            $$
            f(x)\text{ 在 }(-\infty,\tfrac12)\text{ 上单调递减，在 }(\tfrac12,+\infty)\text{ 上单调递增。}
            $$
            所以 $f\!\left(\dfrac12\right)$ 是唯一极小值。

            计算
            $$
            f\!\left(\frac12\right)
            =\int_{1/2}^1\sqrt{1+t^2}\,dt+\int_1^{1/4}\sqrt{1+t}\,dt
            =\int_{1/2}^1\sqrt{1+t^2}\,dt-\int_{1/4}^1\sqrt{1+t}\,dt.
            $$
            分拆为
            $$
            \int_{1/2}^1\sqrt{1+t^2}\,dt-\int_{1/2}^1\sqrt{1+t}\,dt-\int_{1/4}^{1/2}\sqrt{1+t}\,dt.
            $$
            在 $(1/2,1)$ 上有 $\sqrt{1+t^2}<\sqrt{1+t}$，故上式小于 $0$，所以
            $$
            f\!\left(\frac12\right)<0.
            $$

            另一方面，
            $$
            \lim_{x\to-\infty}f(x)=+\infty,
            $$
            且
            $$
            \lim_{x\to+\infty}f(x)=+\infty.
            $$
            因为函数在极小值点取负值，所以它在
            $$
            (-\infty,\tfrac12)\quad\text{和}\quad(\tfrac12,+\infty)
            $$
            上各有一个零点。

            故零点个数为 $2$。
            """
        ),
        assets=["images/source_pages/page-3.png"],
    ),
    Question(
        number=20,
        question_type="solution",
        score=10,
        module="高等数学",
        topics=["一阶微分方程", "牛顿冷却定律", "实际应用"],
        stem=md(
            r"""
            已知高温物体置于低温介质中，任一时刻该物体温度对时间的变化率与该时刻物体和介质的温差成正比。
            现将一初始温度为 $120^\circ\mathrm{C}$ 的物体在 $20^\circ\mathrm{C}$ 的恒温介质中冷却，$30\text{ min}$ 后该物体降至 $30^\circ\mathrm{C}$。
            若要将该物体的温度继续降至 $21^\circ\mathrm{C}$，还需冷却多长时间？
            """
        ),
        answer="30 min",
        explanation=md(
            r"""
            设 $t$ 时刻物体温度为 $x(t)$，由牛顿冷却定律，
            $$
            \frac{dx}{dt}=-k(x-20)\qquad (k>0).
            $$
            解得
            $$
            x(t)=Ce^{-kt}+20.
            $$
            由 $x(0)=120$ 得 $C=100$，故
            $$
            x(t)=100e^{-kt}+20.
            $$
            又由 $x(1/2)=30$，得
            $$
            100e^{-k/2}+20=30
            \quad\Longrightarrow\quad
            e^{-k/2}=\frac{1}{10}
            \quad\Longrightarrow\quad
            k=2\ln 10.
            $$
            令 $x(t)=21$，则
            $$
            100e^{-2t\ln 10}+20=21
            \quad\Longrightarrow\quad
            e^{-2t\ln 10}=\frac{1}{100}
            \quad\Longrightarrow\quad
            t=1\text{ h}.
            $$
            因此从 $30\text{ min}$ 冷却到 $21^\circ\mathrm{C}$ 还需
            $$
            1\text{ h}-30\text{ min}=30\text{ min}.
            $$
            """
        ),
        assets=["images/source_pages/page-3.png"],
    ),
    Question(
        number=21,
        question_type="proof",
        score=10,
        module="高等数学",
        topics=["导数应用", "切线", "拉格朗日中值定理", "函数单调性"],
        stem=md(
            r"""
            已知函数 $f(x)$ 在区间 $[a,+\infty)$ 上具有二阶导数，$f(a)=0$，$f'(x)>0$，$f''(x)>0$。
            设 $b>a$，曲线 $y=f(x)$ 在点 $(b,f(b))$ 处的切线与 $x$ 轴的交点是 $(x_0,0)$，证明
            $$
            a<x_0<b.
            $$
            """
        ),
        answer=r"$a<x_0<b$",
        explanation=md(
            r"""
            点 $(b,f(b))$ 处的切线方程为
            $$
            y-f(b)=f'(b)(x-b).
            $$
            令 $y=0$，得
            $$
            x_0=b-\frac{f(b)}{f'(b)}.
            $$

            因为 $f'(x)>0$，故 $f(x)$ 单调递增；又 $f(a)=0$ 且 $b>a$，所以
            $$
            f(b)>0.
            $$
            再由 $f'(b)>0$，立得
            $$
            x_0=b-\frac{f(b)}{f'(b)}<b.
            $$

            下证 $x_0>a$。由拉格朗日中值定理，存在 $\xi\in(a,b)$，使
            $$
            \frac{f(b)-f(a)}{b-a}=f'(\xi),
            $$
            即
            $$
            \frac{f(b)}{b-a}=f'(\xi).
            $$
            因而
            $$
            x_0-a=b-a-\frac{f(b)}{f'(b)}
            =\frac{f(b)}{f'(\xi)}-\frac{f(b)}{f'(b)}
            =f(b)\frac{f'(b)-f'(\xi)}{f'(b)f'(\xi)}.
            $$
            由 $f''(x)>0$，知 $f'(x)$ 单调递增，于是
            $$
            f'(b)>f'(\xi),
            $$
            从而
            $$
            x_0-a>0.
            $$
            即 $x_0>a$。

            综上，
            $$
            a<x_0<b.
            $$
            """
        ),
        assets=["images/source_pages/page-4.png"],
    ),
    Question(
        number=22,
        question_type="solution",
        score=11,
        module="线性代数",
        topics=["矩阵方程", "幂零矩阵", "逆矩阵", "行列式"],
        stem=md(
            r"""
            设矩阵
            $$
            A=\begin{pmatrix}
            a&1&0\\
            1&a&-1\\
            0&1&a
            \end{pmatrix},
            \qquad A^3=O.
            $$
            (1) 求 $a$ 的值；

            (2) 若矩阵 $X$ 满足
            $$
            X-XA^2-AX+AXA^2=E,
            $$
            其中 $E$ 为 $3$ 阶单位阵，求 $X$。
            """
        ),
        answer=md(
            r"""
            (1) $a=0$；

            (2) $X=\begin{pmatrix}
            3&1&-2\\
            1&1&-1\\
            2&1&-1
            \end{pmatrix}$。
            """
        ),
        explanation=md(
            r"""
            由 $A^3=O$ 可知 $A$ 为幂零矩阵，因此
            $$
            |A|=0.
            $$
            计算
            $$
            |A|=a^3,
            $$
            所以
            $$
            a=0.
            $$

            代入后，原方程化为
            $$
            X(E-A^2)-AX(E-A^2)=E,
            $$
            即
            $$
            (E-A)X(E-A^2)=E.
            $$
            因为 $A^3=O$，所以 $E-A$ 与 $E-A^2$ 都可逆，从而
            $$
            X=(E-A)^{-1}(E-A^2)^{-1}
            =\bigl[(E-A^2)(E-A)\bigr]^{-1}
            =(E-A^2-A)^{-1}.
            $$
            当 $a=0$ 时，
            $$
            A=\begin{pmatrix}
            0&1&0\\
            1&0&-1\\
            0&1&0
            \end{pmatrix},
            \qquad
            E-A^2-A=
            \begin{pmatrix}
            0&-1&1\\
            -1&1&1\\
            -1&-1&2
            \end{pmatrix}.
            $$
            直接求逆得
            $$
            X=
            \begin{pmatrix}
            3&1&-2\\
            1&1&-1\\
            2&1&-1
            \end{pmatrix}.
            $$

            说明：答案册首页给出的 $X$ 与后续推导不一致。这里采用推导结果，并已直接代回
            $X-XA^2-AX+AXA^2=E$
            验证无误。
            """
        ),
        assets=["images/source_pages/page-4.png"],
    ),
    Question(
        number=23,
        question_type="solution",
        score=11,
        module="线性代数",
        topics=["矩阵相似", "特征值", "特征向量", "矩阵对角化"],
        stem=md(
            r"""
            设矩阵
            $$
            A=\begin{pmatrix}
            0&2&-3\\
            -1&3&-3\\
            1&-2&a
            \end{pmatrix}
            $$
            相似于矩阵
            $$
            B=\begin{pmatrix}
            1&-2&0\\
            0&b&0\\
            0&3&1
            \end{pmatrix}.
            $$
            (1) 求 $a,b$ 的值；

            (2) 求可逆矩阵 $P$，使 $P^{-1}AP$ 为对角阵。
            """
        ),
        answer=md(
            r"""
            (1) $a=4,\ b=5$；

            (2) 可取
            $$
            P=\begin{pmatrix}
            2&-3&-1\\
            1&0&-1\\
            0&1&1
            \end{pmatrix},
            $$
            此时
            $$
            P^{-1}AP=\operatorname{diag}(1,1,5).
            $$
            """
        ),
        explanation=md(
            r"""
            因为 $A\sim B$，故相似矩阵的迹、行列式相等。

            由迹相等，
            $$
            \operatorname{tr}(A)=3+a,\qquad \operatorname{tr}(B)=1+b+1=b+2,
            $$
            得
            $$
            a-b=-1.
            $$
            再由行列式相等可解得
            $$
            a=4,\qquad b=5.
            $$

            将 $a=4$ 代入，记
            $$
            A=E+C,\qquad
            C=\begin{pmatrix}
            -1&2&-3\\
            -1&2&-3\\
            1&-2&3
            \end{pmatrix}
            =
            \begin{pmatrix}
            -1\\ -1\\ 1
            \end{pmatrix}
            (1,-2,3).
            $$
            因而 $C$ 的特征值为 $0,0,4$，从而 $A$ 的特征值为
            $$
            1,\ 1,\ 5.
            $$

            对应 $\lambda=1$，可取两个线性无关特征向量
            $$
            \xi_1=(2,1,0)^{\mathsf T},\qquad
            \xi_2=(-3,0,1)^{\mathsf T}.
            $$
            对应 $\lambda=5$，可取特征向量
            $$
            \xi_3=(-1,-1,1)^{\mathsf T}.
            $$
            以它们为列向量组成
            $$
            P=\begin{pmatrix}
            2&-3&-1\\
            1&0&-1\\
            0&1&1
            \end{pmatrix},
            $$
            则
            $$
            P^{-1}AP=\operatorname{diag}(1,1,5).
            $$
            """
        ),
        assets=["images/source_pages/page-4.png"],
    ),
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
    lines.extend(
        [
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
        ]
    )
    return "\n".join(lines)


def annual_questions_md(questions: list[Question]) -> str:
    lines = [
        f"# {YEAR} 年数学二真题",
        "",
        "资料类型：考研数学二历年真题",
        f"年份：{YEAR}",
        "科目：数学二",
        "整理状态：按原卷页图转写并校对。",
        "",
    ]
    for page in range(1, 5):
        lines.extend(
            [
                f"**第 {page} 页题面页图**",
                "",
                f"![{YEAR} 数学二第 {page} 页题面](images/source_pages/page-{page}.png)",
                "",
            ]
        )
    for q in questions:
        lines.extend(
            [
                f"## 第 {q.number} 题",
                f"- 题型：{qtype_label(q.question_type)}",
                f"- 分值：{q.score}",
                f"- 模块：{q.module}",
                f"- 考点：{'、'.join(q.topics)}",
                "",
                q.stem,
                "",
            ]
        )
        for asset in q.assets:
            lines.extend([f"![{YEAR} 数学二第 {q.number} 题题图]({asset})", ""])
    return "\n".join(lines).rstrip() + "\n"


def annual_answers_md(questions: list[Question]) -> str:
    lines = [
        f"# {YEAR} 年数学二答案解析",
        "",
        "资料类型：考研数学二答案解析",
        f"年份：{YEAR}",
        "科目：数学二",
        "整理状态：答案与解析按答案册清洗，并与题面同步。",
        "",
        "## 答案速查",
        "",
        "| 题号 | 题型 | 答案 |",
        "|---|---|---|",
    ]
    for q in questions:
        lines.append(f"| {q.number} | {qtype_label(q.question_type)} | {answer_for_table(q.answer)} |")
    lines.extend(["", "## 详细解析", ""])
    for q in questions:
        lines.extend(
            [
                f"### 第 {q.number} 题",
                "",
                f"- 答案：{q.answer}",
                "",
                q.explanation,
                "",
            ]
        )
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


def crop_q004_diagram() -> None:
    src = ROOT / "images" / "answer_pages" / "page-02.png"
    dst = ROOT / "images" / "q004_diagram.png"
    img = Image.open(src)
    # 手工裁出第 4 题图像本体，尽量不带题面文字。
    crop = img.crop((930, 560, 1230, 1080))
    crop.save(dst)


def main() -> None:
    (ROOT / "questions").mkdir(exist_ok=True)
    crop_q004_diagram()

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
