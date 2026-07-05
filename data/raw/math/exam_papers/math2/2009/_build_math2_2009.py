from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from textwrap import dedent

from PIL import Image


ROOT = Path(__file__).resolve().parent
YEAR = 2009
EXAM_ID = f"kaoyan_math2_{YEAR}"
PDF_PATH = Path(r"D:\百度网盘\高数资料\【01】1987-2022年考研数学二真题（PDF）\2009考研数学二真题.pdf")
PDFTOPPM = Path(
    r"C:\Users\idapro\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdftoppm.exe"
)


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
        1,
        "single_choice",
        4,
        "高等数学",
        ["可去间断点", "极限"],
        md(
            r"""
            函数
            $$
            f(x)=\frac{x-x^3}{\sin \pi x}
            $$
            的可去间断点的个数为（ ）

            A. $1$
            B. $2$
            C. $3$
            D. 无穷多个
            """
        ),
        "C",
        md(
            r"""
            当 $x$ 取整数时分母为 $0$，函数有无穷多个间断点；但可去间断点要求极限存在。
            由
            $$
            x-x^3=x(1-x^2)=x(1-x)(1+x)
            $$
            可知只在 $x=0,\pm1$ 处能与 $\sin(\pi x)$ 的零点相消，且这三点的极限都存在，
            所以可去间断点共有 $3$ 个。
            """
        ),
        ["images/source_pages/page-1.png"],
    ),
    Question(
        2,
        "single_choice",
        4,
        "高等数学",
        ["等价无穷小", "Taylor 展开"],
        md(
            r"""
            当 $x\to 0$ 时，
            $$
            f(x)=x-\sin ax,\qquad g(x)=x^2\ln(1-bx)
            $$
            是等价无穷小量，则（ ）

            A. $a=1,\ b=-\dfrac16$
            B. $a=1,\ b=\dfrac16$
            C. $a=-1,\ b=-\dfrac16$
            D. $a=-1,\ b=\dfrac16$
            """
        ),
        "A",
        md(
            r"""
            展开得
            $$
            x-\sin(ax)=(1-a)x+\frac{a^3}{6}x^3+o(x^3),
            $$
            而
            $$
            x^2\ln(1-bx)=-bx^3+o(x^3).
            $$
            两者等价首先要求一次项消失，所以 $a=1$；再比较三次项系数，
            $$
            \frac16=-b,
            $$
            故 $b=-\dfrac16$。
            """
        ),
        ["images/source_pages/page-1.png"],
    ),
    Question(
        3,
        "single_choice",
        4,
        "高等数学",
        ["全微分", "多元函数极值"],
        md(
            r"""
            设函数 $z=f(x,y)$ 的全微分为
            $$
            dz=x\,dx+y\,dy,
            $$
            则点 $(0,0)$（ ）

            A. 不是 $f(x,y)$ 的连续点
            B. 不是 $f(x,y)$ 的极值点
            C. 是 $f(x,y)$ 的极大值点
            D. 是 $f(x,y)$ 的极小值点
            """
        ),
        "D",
        md(
            r"""
            由全微分可知
            $$
            f_x=x,\qquad f_y=y.
            $$
            因而
            $$
            f_{xx}=1,\quad f_{yy}=1,\quad f_{xy}=0.
            $$
            在 $(0,0)$ 处有驻点，且二次型
            $$
            d^2f=dx^2+dy^2
            $$
            正定，所以 $(0,0)$ 是极小值点。
            """
        ),
        ["images/source_pages/page-1.png"],
    ),
    Question(
        4,
        "single_choice",
        4,
        "高等数学",
        ["二重积分", "积分区域化简"],
        md(
            r"""
            设函数 $f(x,y)$ 连续，则
            $$
            \int_1^2 dx\int_x^2 f(x,y)\,dy+\int_1^2 dy\int_y^{4-y} f(x,y)\,dx
            =(\ \ )
            $$

            A. $\int_1^2 dx\int_1^{4-x} f(x,y)\,dy$

            B. $\int_1^2 dx\int_x^{4-x} f(x,y)\,dy$

            C. $\int_1^2 dy\int_1^{4-y} f(x,y)\,dx$

            D. $\int_1^2 dy\int_y^2 f(x,y)\,dx$
            """
        ),
        "C",
        md(
            r"""
            两个积分区域分别为
            $$
            D_1=\{(x,y)\mid 1\le x\le 2,\ x\le y\le 2\},
            $$
            $$
            D_2=\{(x,y)\mid 1\le y\le 2,\ y\le x\le 4-y\}.
            $$
            合并后可写成
            $$
            D=\{(x,y)\mid 1\le y\le 2,\ 1\le x\le 4-y\},
            $$
            所以等于
            $$
            \int_1^2dy\int_1^{4-y}f(x,y)\,dx.
            $$
            """
        ),
        ["images/source_pages/page-1.png"],
    ),
    Question(
        5,
        "single_choice",
        4,
        "高等数学",
        ["曲率", "单调性与零点"],
        md(
            r"""
            若 $f''(x)$ 不变号，且曲线 $y=f(x)$ 在点 $(1,1)$ 处的曲率圆为
            $$
            x^2+y^2=2,
            $$
            则函数 $f(x)$ 在区间 $(1,2)$ 内（ ）

            A. 有极值点，无零点
            B. 无极值点，有零点
            C. 有极值点，有零点
            D. 无极值点，无零点
            """
        ),
        "B",
        md(
            r"""
            曲率圆圆心在原点，且过点 $(1,1)$，可得该点切线斜率为 $-1$，并由曲率公式求得
            $$
            f'(1)=-1,\qquad f''(1)<0.
            $$
            又 $f''(x)$ 不变号，因此在 $[1,2]$ 上始终有 $f'(x)<0$，函数单调递减，
            不会出现极值点。由于 $f(1)=1>0$，而由单调性与曲率信息可知 $f(2)<0$，
            由零点定理知在 $(1,2)$ 内有零点。
            """
        ),
        ["images/source_pages/page-1.png"],
    ),
    Question(
        6,
        "single_choice",
        4,
        "高等数学",
        ["积分上限函数", "函数图像"],
        md(
            r"""
            设函数 $y=f(x)$ 在区间 $[-1,3]$ 上的图形如图所示，则函数
            $$
            F(x)=\int_0^x f(t)\,dt
            $$
            的图形为（ ）

            题图见下方裁图；四个选项图见原始试卷页图。
            """
        ),
        "D",
        md(
            r"""
            由积分上限函数的性质，
            $$
            F'(x)=f(x).
            $$
            观察题图可知：在 $[-1,0]$ 上 $f(x)=1$，故 $F$ 为斜率为 $1$ 的直线；
            在 $(0,1)$ 上 $f(x)<0$，故 $F$ 递减；在 $(1,2)$ 上 $f(x)>0$，故 $F$ 递增；
            在 $(2,3)$ 上 $f(x)=0$，故 $F$ 为常数。与这些特征一致的只有 D。
            """
        ),
        [
            "images/source_pages/page-1.png",
            "images/source_pages/page-2.png",
            "images/q006_diagram.png",
        ],
    ),
    Question(
        7,
        "single_choice",
        4,
        "线性代数",
        ["伴随矩阵", "分块矩阵"],
        md(
            r"""
            设 $A,B$ 均为 $2$ 阶方阵，$A^*,B^*$ 分别为 $A,B$ 的伴随矩阵。若 $|A|=2,\ |B|=3$，
            则分块矩阵
            $$
            \begin{pmatrix}
            O & A\\
            B & O
            \end{pmatrix}
            $$
            的伴随矩阵为（ ）

            A. $\begin{pmatrix}O & 3B^*\\ 2A^* & O\end{pmatrix}$

            B. $\begin{pmatrix}O & 2B^*\\ 3A^* & O\end{pmatrix}$

            C. $\begin{pmatrix}O & 3A^*\\ 2B^* & O\end{pmatrix}$

            D. $\begin{pmatrix}O & 2A^*\\ 3B^* & O\end{pmatrix}$
            """
        ),
        "A",
        md(
            r"""
            记
            $$
            M=\begin{pmatrix}O&A\\B&O\end{pmatrix},
            $$
            则
            $$
            |M|=|{-AB}|=|A||B|=6\ne0,
            $$
            因而 $M$ 可逆。利用分块矩阵求逆可得
            $$
            M^{-1}=
            \begin{pmatrix}
            O & B^{-1}\\
            A^{-1} & O
            \end{pmatrix}.
            $$
            于是
            $$
            M^*=|M|M^{-1}
            =
            \begin{pmatrix}
            O & 6B^{-1}\\
            6A^{-1} & O
            \end{pmatrix}
            =
            \begin{pmatrix}
            O & 3B^*\\
            2A^* & O
            \end{pmatrix}.
            $$
            """
        ),
        ["images/source_pages/page-2.png"],
    ),
    Question(
        8,
        "single_choice",
        4,
        "线性代数",
        ["二次型", "合同变换"],
        md(
            r"""
            设 $A,P$ 均为 $3$ 阶矩阵，$P^T$ 为 $P$ 的转置矩阵，且
            $$
            P^TAP=
            \begin{pmatrix}
            1&0&0\\
            0&1&0\\
            0&0&2
            \end{pmatrix}.
            $$
            若 $P=(\alpha_1,\alpha_2,\alpha_3)$，
            $$
            Q=(\alpha_1+\alpha_2,\alpha_2,\alpha_3),
            $$
            则 $Q^TAQ$ 为（ ）

            A. $\begin{pmatrix}2&1&0\\1&1&0\\0&0&2\end{pmatrix}$

            B. $\begin{pmatrix}1&1&0\\1&2&0\\0&0&2\end{pmatrix}$

            C. $\begin{pmatrix}2&0&0\\0&1&0\\0&0&2\end{pmatrix}$

            D. $\begin{pmatrix}1&0&0\\0&2&0\\0&0&2\end{pmatrix}$
            """
        ),
        "B",
        md(
            r"""
            令
            $$
            E=
            \begin{pmatrix}
            1&0&0\\
            1&1&0\\
            0&0&1
            \end{pmatrix},
            $$
            则 $Q=PE$。因此
            $$
            Q^TAQ=E^T(P^TAP)E
            =
            E^T
            \begin{pmatrix}
            1&0&0\\
            0&1&0\\
            0&0&2
            \end{pmatrix}
            E
            =
            \begin{pmatrix}
            1&1&0\\
            1&2&0\\
            0&0&2
            \end{pmatrix}.
            $$
            """
        ),
        ["images/source_pages/page-2.png"],
    ),
    Question(
        9,
        "fill_blank",
        4,
        "高等数学",
        ["参数方程", "切线方程"],
        md(
            r"""
            曲线
            $$
            \begin{cases}
            x=\int_0^{1-t} e^{-u^2}\,du,\\
            y=t^2\ln(2-t^2)
            \end{cases}
            $$
            在点 $(0,0)$ 处的切线方程为 ________。
            """
        ),
        "$y=2x$",
        md(
            r"""
            对参数方程求导，
            $$
            \frac{dx}{dt}=-e^{-(1-t)^2},\qquad
            \frac{dy}{dt}=2t\ln(2-t^2)-\frac{2t^3}{2-t^2}.
            $$
            点 $(0,0)$ 对应 $t=1$。代入得
            $$
            \left.\frac{dx}{dt}\right|_{t=1}=-1,\qquad
            \left.\frac{dy}{dt}\right|_{t=1}=-2,
            $$
            所以
            $$
            \frac{dy}{dx}=2.
            $$
            切线过原点，故方程为 $y=2x$。
            """
        ),
        ["images/source_pages/page-2.png"],
    ),
    Question(
        10,
        "fill_blank",
        4,
        "高等数学",
        ["反常积分", "偶函数"],
        md(
            r"""
            已知
            $$
            \int_{-\infty}^{+\infty} e^{k|x|}\,dx=1,
            $$
            则 $k=$ ________。
            """
        ),
        "$-2$",
        md(
            r"""
            由于积分收敛，必须有 $k<0$。再由偶函数性，
            $$
            1=2\int_0^{+\infty}e^{kx}\,dx
            =2\cdot\left(-\frac1k\right).
            $$
            解得 $k=-2$。
            """
        ),
        ["images/source_pages/page-2.png"],
    ),
    Question(
        11,
        "fill_blank",
        4,
        "高等数学",
        ["定积分极限", "分部积分"],
        md(
            r"""
            $$
            \lim_{n\to\infty}\int_0^1 e^{-x}\sin(nx)\,dx
            =\underline{\qquad}.
            $$
            """
        ),
        "$0$",
        md(
            r"""
            积分分部或直接计算可得
            $$
            \int_0^1 e^{-x}\sin(nx)\,dx
            =
            \frac{n-e^{-1}\bigl(\sin n+n\cos n\bigr)}{1+n^2}.
            $$
            分子有界且为 $O(n)$，分母为 $n^2+1$，故极限为 $0$。
            """
        ),
        ["images/source_pages/page-2.png"],
    ),
    Question(
        12,
        "fill_blank",
        4,
        "高等数学",
        ["隐函数求导", "二阶导数"],
        md(
            r"""
            设 $y=y(x)$ 是由方程
            $$
            xy+e^y=x+1
            $$
            确定的隐函数，则
            $$
            \left.\frac{d^2y}{dx^2}\right|_{x=0}
            =\underline{\qquad}.
            $$
            """
        ),
        "$-3$",
        md(
            r"""
            先由原方程在 $x=0$ 时得 $e^{y(0)}=1$，故 $y(0)=0$。
            对方程求导：
            $$
            y+xy'+e^y y'=1,
            $$
            代入 $(0,0)$ 得 $y'(0)=1$。再次求导可得
            $$
            2y'+xy''+e^y\bigl((y')^2+y''\bigr)=0.
            $$
            再代入 $(0,0)$ 与 $y'(0)=1$，得
            $$
            2+1+y''(0)=0,
            $$
            故 $y''(0)=-3$。
            """
        ),
        ["images/source_pages/page-2.png"],
    ),
    Question(
        13,
        "fill_blank",
        4,
        "高等数学",
        ["最值", "对数求导"],
        md(
            r"""
            函数
            $$
            y=x^{2x}
            $$
            在区间 $(0,1]$ 上的最小值为 ________。
            """
        ),
        "$e^{-2/e}$",
        md(
            r"""
            取对数，
            $$
            \ln y=2x\ln x.
            $$
            设 $\phi(x)=2x\ln x$，则
            $$
            \phi'(x)=2(\ln x+1).
            $$
            令 $\phi'(x)=0$ 得 $x=e^{-1}$。此时
            $$
            \phi(e^{-1})=-\frac{2}{e},
            $$
            从而
            $$
            y_{\min}=e^{-2/e}.
            $$
            """
        ),
        ["images/source_pages/page-2.png"],
    ),
    Question(
        14,
        "fill_blank",
        4,
        "线性代数",
        ["矩阵相似", "迹"],
        md(
            r"""
            设 $\alpha,\beta$ 为 $3$ 维列向量，$\beta^T$ 为 $\beta$ 的转置。若矩阵 $\alpha\beta^T$
            相似于
            $$
            \begin{pmatrix}
            2&0&0\\
            0&0&0\\
            0&0&0
            \end{pmatrix},
            $$
            则 $\beta^T\alpha=$ ________。
            """
        ),
        "$2$",
        md(
            r"""
            相似矩阵有相同的迹，而
            $$
            \operatorname{tr}(\alpha\beta^T)=\beta^T\alpha.
            $$
            已知相似矩阵的迹为 $2$，故
            $$
            \beta^T\alpha=2.
            $$
            """
        ),
        ["images/source_pages/page-2.png"],
    ),
    Question(
        15,
        "solution",
        9,
        "高等数学",
        ["极限", "无穷小展开"],
        md(
            r"""
            求极限
            $$
            \lim_{x\to 0}\frac{(1-\cos x)\,[x-\ln(1+\tan x)]}{\sin^4 x}.
            $$
            """
        ),
        r"$\dfrac14$",
        md(
            r"""
            利用展开式
            $$
            1-\cos x=\frac{x^2}{2}+O(x^4),\qquad \tan x=x+\frac{x^3}{3}+O(x^5),
            $$
            以及
            $$
            \ln(1+\tan x)=x-\frac{x^2}{2}+\frac{2x^3}{3}+O(x^4).
            $$
            因而
            $$
            x-\ln(1+\tan x)=\frac{x^2}{2}+O(x^3),
            $$
            所以分子为
            $$
            \left(\frac{x^2}{2}+O(x^4)\right)\left(\frac{x^2}{2}+O(x^3)\right)=\frac{x^4}{4}+o(x^4).
            $$
            又 $\sin^4x=x^4+o(x^4)$，故极限为 $\dfrac14$。
            """
        ),
        ["images/source_pages/page-2.png"],
    ),
    Question(
        16,
        "solution",
        10,
        "高等数学",
        ["不定积分", "换元积分"],
        md(
            r"""
            计算不定积分
            $$
            \int \ln\!\left(1+\sqrt{\frac{1+x}{x}}\right)\,dx\qquad (x>0).
            $$
            """
        ),
        md(
            r"""
            $$
            \int \ln\!\left(1+\sqrt{\frac{1+x}{x}}\right)\,dx
            =(x+1)\ln\!\left(1+\sqrt{\frac{1+x}{x}}\right)+\sqrt{x(x+1)}+C.
            $$
            """
        ),
        md(
            r"""
            令
            $$
            t=\sqrt{\frac{1+x}{x}},
            $$
            则可化为关于 $t$ 的有理函数积分。整理后做分部积分，或直接对结果求导核对，
            可得一个原函数为
            $$
            F(x)=(x+1)\ln\!\left(1+\sqrt{\frac{1+x}{x}}\right)+\sqrt{x(x+1)}.
            $$
            验证 $F'(x)$ 即为被积函数，因此答案成立。
            """
        ),
        ["images/source_pages/page-2.png"],
    ),
    Question(
        17,
        "solution",
        10,
        "高等数学",
        ["多元复合函数", "链式法则"],
        md(
            r"""
            设
            $$
            z=f(x+y,\ x-y,\ xy),
            $$
            其中 $f$ 具有二阶连续偏导数，求 $dz$ 与
            $$
            \frac{\partial^2 z}{\partial x\,\partial y}.
            $$
            """
        ),
        md(
            r"""
            记
            $$
            u=x+y,\quad v=x-y,\quad w=xy,
            $$
            则
            $$
            dz=(f_u+f_v+yf_w)\,dx+(f_u-f_v+xf_w)\,dy,
            $$
            且
            $$
            z_{xy}=f_{uu}-f_{vv}+(x+y)f_{uw}+(x-y)f_{vw}+xyf_{ww}+f_w.
            $$
            """
        ),
        md(
            r"""
            设 $u=x+y,\ v=x-y,\ w=xy$，则 $z=f(u,v,w)$。
            由链式法则，
            $$
            z_x=f_u u_x+f_v v_x+f_w w_x=f_u+f_v+yf_w,
            $$
            $$
            z_y=f_u u_y+f_v v_y+f_w w_y=f_u-f_v+xf_w.
            $$
            因而
            $$
            dz=z_x\,dx+z_y\,dy.
            $$
            再对 $z_x$ 关于 $y$ 求偏导，继续应用链式法则即可得到所示的 $z_{xy}$ 公式。
            """
        ),
        ["images/source_pages/page-3.png"],
    ),
    Question(
        18,
        "solution",
        10,
        "高等数学",
        ["微分方程", "旋转体体积"],
        md(
            r"""
            设非负函数 $y=y(x)\ (x\ge 0)$ 满足微分方程
            $$
            xy''-y'+2=0.
            $$
            当曲线 $y=y(x)$ 过原点时，其与直线 $x=1$ 及 $y=0$ 围成平面区域 $D$ 的面积为 $2$，
            求 $D$ 绕 $y$ 轴旋转所得旋转体体积。
            """
        ),
        r"$\dfrac{17\pi}{6}$",
        md(
            r"""
            方程可写为
            $$
            \left(\frac{y'}x\right)'=-\frac{2}{x^2},
            $$
            积分得通解
            $$
            y=x^2+C_1x+C_2.
            $$
            又因曲线过原点，故 $C_2=0$。由面积条件
            $$
            \int_0^1 y(x)\,dx=2
            $$
            求得 $C_1=\dfrac32$，所以
            $$
            y=x^2+\frac32x.
            $$
            反解为
            $$
            x=\frac{-3+\sqrt{9+16y}}{4},
            $$
            用壳层法或圆盘法计算绕 $y$ 轴旋转体积，可得
            $$
            V=2\pi\int_0^1 x\,y(x)\,dx=\frac{17\pi}{6}.
            $$
            """
        ),
        ["images/source_pages/page-3.png"],
    ),
    Question(
        19,
        "solution",
        10,
        "高等数学",
        ["二重积分", "极坐标"],
        md(
            r"""
            计算二重积分
            $$
            \iint_D (x-y)\,dx\,dy,
            $$
            其中
            $$
            D=\{(x,y)\mid (x-1)^2+(y-1)^2\le 2,\ y\ge x\}.
            $$
            """
        ),
        r"$-\dfrac{8}{3}$",
        md(
            r"""
            作平移
            $$
            u=x-1,\quad v=y-1,
            $$
            则区域化为半圆盘
            $$
            u^2+v^2\le 2,\quad v\ge u,
            $$
            而被积函数变为 $u-v$。再改用极坐标即可：
            $$
            u=r\cos\theta,\quad v=r\sin\theta,\quad
            0\le r\le \sqrt2,\quad \frac{\pi}{4}\le\theta\le\frac{5\pi}{4}.
            $$
            因而
            $$
            \iint_D(x-y)\,dx\,dy
            =\int_{\pi/4}^{5\pi/4}\int_0^{\sqrt2}r^2(\cos\theta-\sin\theta)\,dr\,d\theta
            =-\frac83.
            $$
            """
        ),
        ["images/source_pages/page-3.png"],
    ),
    Question(
        20,
        "solution",
        12,
        "高等数学",
        ["微分方程", "分段函数"],
        md(
            r"""
            设 $y=y(x)$ 是区间 $(-\pi,\pi)$ 内过点
            $$
            \left(-\frac{\pi}{\sqrt2},\ \frac{\pi}{\sqrt2}\right)
            $$
            的光滑曲线。当 $-\pi<x<0$ 时，曲线上任一点处的法线都过原点；
            当 $0\le x<\pi$ 时，函数 $y(x)$ 满足
            $$
            y''+y+x=0.
            $$
            求 $y(x)$ 的表达式。
            """
        ),
        md(
            r"""
            $$
            y(x)=
            \begin{cases}
            \sqrt{\pi^2-x^2}, & -\pi<x<0,\\[2mm]
            \pi\cos x+\sin x-x, & 0\le x<\pi.
            \end{cases}
            $$
            """
        ),
        md(
            r"""
            当 $-\pi<x<0$ 时，法线过原点意味着切线斜率满足
            $$
            y'=-\frac{x}{y},
            $$
            从而
            $$
            y\,dy=-x\,dx,\qquad x^2+y^2=C.
            $$
            代入已知点得 $C=\pi^2$，又 $y>0$，故
            $$
            y=\sqrt{\pi^2-x^2}.
            $$
            当 $0\le x<\pi$ 时，方程通解为
            $$
            y=c_1\cos x+c_2\sin x-x.
            $$
            由曲线在 $x=0$ 处连续且可导，联立
            $$
            y(0^-)=y(0^+)=\pi,\qquad y'(0^-)=y'(0^+)=0
            $$
            得 $c_1=\pi,\ c_2=1$，从而得到所求分段表达式。
            """
        ),
        ["images/source_pages/page-3.png"],
    ),
    Question(
        21,
        "proof",
        11,
        "高等数学",
        ["拉格朗日中值定理", "导数定义"],
        md(
            r"""
            （Ⅰ）证明拉格朗日中值定理：若函数 $f(x)$ 在 $[a,b]$ 上连续，在 $(a,b)$ 内可导，
            则存在点 $\xi\in(a,b)$，使得
            $$
            f(b)-f(a)=f'(\xi)(b-a).
            $$

            （Ⅱ）证明：若函数 $f(x)$ 在 $x=0$ 处连续，在 $(0,\delta)\ (\delta>0)$ 内可导，
            且
            $$
            \lim_{x\to0^+}f'(x)=A,
            $$
            则 $f_+'(0)$ 存在，且 $f_+'(0)=A$。
            """
        ),
        "见解析",
        md(
            r"""
            （Ⅰ）构造辅助函数
            $$
            \phi(x)=f(x)-f(a)-\frac{f(b)-f(a)}{b-a}(x-a).
            $$
            则 $\phi(a)=\phi(b)=0$，由罗尔定理知存在 $\xi\in(a,b)$ 使
            $$
            \phi'(\xi)=0,
            $$
            即
            $$
            f'(\xi)=\frac{f(b)-f(a)}{b-a}.
            $$

            （Ⅱ）对任意 $x\in(0,\delta)$，把拉格朗日中值定理应用到 $[0,x]$ 上，
            存在 $\xi_x\in(0,x)$ 使
            $$
            \frac{f(x)-f(0)}x=f'(\xi_x).
            $$
            当 $x\to0^+$ 时，$\xi_x\to0^+$，故右端趋于 $A$，于是
            $$
            \lim_{x\to0^+}\frac{f(x)-f(0)}x=A.
            $$
            这正是 $f_+'(0)$ 存在且等于 $A$。
            """
        ),
        ["images/source_pages/page-3.png"],
    ),
    Question(
        22,
        "solution",
        11,
        "线性代数",
        ["线性方程组", "线性无关"],
        md(
            r"""
            设
            $$
            A=
            \begin{pmatrix}
            1&-1&-1\\
            -1&1&1\\
            0&-4&-2
            \end{pmatrix},
            \qquad
            \xi_1=
            \begin{pmatrix}
            -1\\
            1\\
            -2
            \end{pmatrix}.
            $$

            （Ⅰ）求满足
            $$
            A\xi_2=\xi_1,\qquad A^2\xi_3=\xi_1
            $$
            的所有向量 $\xi_2,\xi_3$；

            （Ⅱ）对（Ⅰ）中的任意向量 $\xi_2,\xi_3$，证明 $\xi_1,\xi_2,\xi_3$ 线性无关。
            """
        ),
        md(
            r"""
            $$
            \xi_2=
            \begin{pmatrix}
            1\\-1\\0
            \end{pmatrix}
            +k_1
            \begin{pmatrix}
            1\\1\\0
            \end{pmatrix},
            \qquad
            \xi_3=
            \begin{pmatrix}
            0\\0\\2
            \end{pmatrix}
            +k_2
            \begin{pmatrix}
            1\\1\\0
            \end{pmatrix},
            \quad k_1,k_2\in\mathbb R.
            $$
            且任意此类 $\xi_2,\xi_3$ 与 $\xi_1$ 线性无关。
            """
        ),
        md(
            r"""
            解线性方程组 $A\xi_2=\xi_1$，可得其通解为
            $$
            \xi_2=
            \begin{pmatrix}
            1\\-1\\0
            \end{pmatrix}
            +k_1
            \begin{pmatrix}
            1\\1\\0
            \end{pmatrix}.
            $$
            再解 $A^2\xi_3=\xi_1$，可先写成 $A(A\xi_3)=\xi_1$，得到
            $$
            \xi_3=
            \begin{pmatrix}
            0\\0\\2
            \end{pmatrix}
            +k_2
            \begin{pmatrix}
            1\\1\\0
            \end{pmatrix}.
            $$
            对任意 $k_1,k_2$，计算三向量构成的行列式可得
            $$
            \det(\xi_1,\xi_2,\xi_3)=2\ne0,
            $$
            因而 $\xi_1,\xi_2,\xi_3$ 线性无关。
            """
        ),
        ["images/source_pages/page-3.png"],
    ),
    Question(
        23,
        "solution",
        11,
        "线性代数",
        ["二次型", "特征值"],
        md(
            r"""
            设二次型
            $$
            f(x_1,x_2,x_3)=ax_1^2+ax_2^2+(a-1)x_3^2+2x_1x_3-2x_2x_3.
            $$

            （Ⅰ）求二次型 $f$ 的矩阵的所有特征值；

            （Ⅱ）若二次型 $f$ 的规范形为
            $$
            y_1^2+y_2^2,
            $$
            求 $a$ 的值。
            """
        ),
        md(
            r"""
            特征值为
            $$
            \lambda_1=a,\qquad \lambda_2=a-2,\qquad \lambda_3=a+1.
            $$
            当规范形为 $y_1^2+y_2^2$ 时，
            $$
            a=2.
            $$
            """
        ),
        md(
            r"""
            二次型对应矩阵为
            $$
            A=
            \begin{pmatrix}
            a&0&1\\
            0&a&-1\\
            1&-1&a-1
            \end{pmatrix}.
            $$
            计算特征多项式
            $$
            |A-\lambda E|
            $$
            可分解为
            $$
            (a-\lambda)(a-\lambda-2)(a-\lambda+1),
            $$
            因而特征值分别为 $a,\ a-2,\ a+1$。
            若规范形为 $y_1^2+y_2^2$，则应有两个正特征值、一个零特征值。
            逐一检验三者为零的情形，只有
            $$
            a-2=0
            $$
            时得到特征值组 $(2,0,3)$，满足要求，故 $a=2$。
            """
        ),
        ["images/source_pages/page-3.png"],
    ),
]


def build_card(q: Question) -> str:
    qid = f"{EXAM_ID}_q{q.number:03d}"
    front_matter = [
        "---",
        f"question_id: {qid}",
        f"exam_id: {EXAM_ID}",
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
    ]
    body = [
        f"# {YEAR} 数学二第 {q.number} 题",
        "",
        "## 题目",
        "",
        q.stem,
        "",
        *[f"![题图](../{asset})\n" for asset in q.assets if asset.endswith(".png")],
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
    return "\n".join(front_matter + body)


def build_questions_md() -> str:
    lines = [
        f"# {YEAR} 年考研数学二真题",
        "",
        "资料类型：考研数学二历年真题",
        f"年份：{YEAR}",
        "科目：数学二",
        "整理状态：按试卷页图校对并统一转写。",
        "",
    ]
    for q in QUESTIONS:
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
        if any(asset.endswith("q006_diagram.png") for asset in q.assets):
            lines.extend(["![第 6 题题图](images/q006_diagram.png)", ""])
    return "\n".join(lines).rstrip() + "\n"


def build_answers_md() -> str:
    lines = [
        f"# Math 2 {YEAR} Answers",
        "",
        "资料类型：考研数学二答案解析",
        f"年份：{YEAR}",
        "科目：数学二",
        "整理状态：依据答案册与题面做清洗整理。",
        "",
        "## 答案速查",
        "",
        "| 题号 | 题型 | 答案 |",
        "|---|---|---|",
    ]
    for q in QUESTIONS:
        lines.append(f"| {q.number} | {qtype_label(q.question_type)} | {q.answer.replace('|', '\\|')} |")
    lines.extend(["", "## 详细解析", ""])
    for q in QUESTIONS:
        lines.extend([f"### 第 {q.number} 题", "", f"- 答案：{q.answer}", "", q.explanation, ""])
    return "\n".join(lines).rstrip() + "\n"


def build_questions_jsonl() -> str:
    rows = []
    for q in QUESTIONS:
        rows.append(
            json.dumps(
                {
                    "question_id": f"{EXAM_ID}_q{q.number:03d}",
                    "exam_id": EXAM_ID,
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
                },
                ensure_ascii=False,
            )
        )
    return "\n".join(rows) + "\n"


def build_manifest() -> str:
    return json.dumps(
        {
            "exam_id": EXAM_ID,
            "exam_type": "math2",
            "exam_label": "数学二",
            "year": YEAR,
            "source_files": {
                "questions": f"math2_{YEAR}_questions.md",
                "answers": f"math2_{YEAR}_answers.md",
            },
            "card_dir": "questions",
            "index_file": "questions.jsonl",
            "question_count": len(QUESTIONS),
            "explanation_count": len(QUESTIONS),
            "question_ids": [f"{EXAM_ID}_q{q.number:03d}" for q in QUESTIONS],
            "generated_at": now_iso(),
            "review_status": "reviewed",
            "answer_status": "available",
            "explanation_status": "available",
        },
        ensure_ascii=False,
        indent=2,
    ) + "\n"


def ensure_dirs() -> None:
    (ROOT / "questions").mkdir(parents=True, exist_ok=True)
    (ROOT / "images" / "source_pages").mkdir(parents=True, exist_ok=True)


def render_source_pages() -> None:
    expected = [ROOT / "images" / "source_pages" / f"page-{i}.png" for i in range(1, 4)]
    if all(path.exists() for path in expected):
        return
    tmp_prefix = ROOT / "images" / "source_pages" / "tmp_page"
    subprocess.run(
        [
            str(PDFTOPPM),
            "-f",
            "1",
            "-l",
            "3",
            "-png",
            str(PDF_PATH),
            str(tmp_prefix),
        ],
        check=True,
    )
    for i in range(1, 4):
        src = ROOT / "images" / "source_pages" / f"tmp_page-{i}.png"
        dst = ROOT / "images" / "source_pages" / f"page-{i}.png"
        src.replace(dst)


def crop_diagram() -> None:
    output = ROOT / "images" / "q006_diagram.png"
    source = ROOT / "images" / "source_pages" / "page-1.png"
    with Image.open(source) as img:
        crop = img.crop((470, 1000, 840, 1535))
        crop.save(output)


def write_outputs() -> None:
    (ROOT / f"math2_{YEAR}_questions.md").write_text(build_questions_md(), encoding="utf-8", newline="\n")
    (ROOT / f"math2_{YEAR}_answers.md").write_text(build_answers_md(), encoding="utf-8", newline="\n")
    (ROOT / "questions.jsonl").write_text(build_questions_jsonl(), encoding="utf-8", newline="\n")
    (ROOT / "paper_manifest.json").write_text(build_manifest(), encoding="utf-8", newline="\n")
    for q in QUESTIONS:
        (ROOT / "questions" / f"q{q.number:03d}.md").write_text(
            build_card(q),
            encoding="utf-8",
            newline="\n",
        )


def main() -> None:
    ensure_dirs()
    render_source_pages()
    crop_diagram()
    write_outputs()


if __name__ == "__main__":
    main()
