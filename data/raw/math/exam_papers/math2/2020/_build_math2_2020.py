from __future__ import annotations

import json
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parent
YEAR = 2020
SOURCE_PAGE_DIR = ROOT.parent / "_tmp_2020_probe"


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
        return "见详细解析"
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
        1,
        "single_choice",
        4,
        "高等数学",
        ["无穷小比较", "积分上限无穷小", "等价无穷小"],
        md(
            r"""
            当 $x\to 0^+$ 时，下列无穷小量中最高阶的是

            (A) $\displaystyle \int_0^x (e^{t^2}-1)\,dt$

            (B) $\displaystyle \int_0^x \ln(1+\sqrt{t^3})\,dt$

            (C) $\displaystyle \int_0^{\sin x}\sin t^2\,dt$

            (D) $\displaystyle \int_0^{1-\cos x}\sqrt{\sin^3 t}\,dt$
            """
        ),
        "D",
        md(
            r"""
            分别比较四项的主阶：

            (A) $e^{t^2}-1\sim t^2$，故
            $$
            \int_0^x (e^{t^2}-1)\,dt\sim \int_0^x t^2\,dt=\frac13x^3.
            $$

            (B) $\ln(1+\sqrt{t^3})\sim t^{3/2}$，故
            $$
            \int_0^x \ln(1+\sqrt{t^3})\,dt\sim \int_0^x t^{3/2}\,dt=\frac25x^{5/2}.
            $$

            (C) $\sin t^2\sim t^2$ 且 $\sin x\sim x$，故
            $$
            \int_0^{\sin x}\sin t^2\,dt\sim \int_0^x t^2\,dt=\frac13x^3.
            $$

            (D) 当 $t\to 0$ 时 $\sqrt{\sin^3 t}\sim t^{3/2}$，而 $1-\cos x\sim \dfrac{x^2}{2}$，故
            $$
            \int_0^{1-\cos x}\sqrt{\sin^3 t}\,dt
            \sim \int_0^{x^2/2} t^{3/2}\,dt
            =\frac25\left(\frac12\right)^{5/2}x^5.
            $$

            四项中阶数最高的是 $x^5$，故选 $D$。
            """
        ),
        ["images/source_pages/page-1.png"],
    ),
    Question(
        2,
        "single_choice",
        4,
        "高等数学",
        ["间断点", "第二类间断点", "极限"],
        md(
            r"""
            函数
            $$
            f(x)=\frac{e^{\frac{1}{x-1}}\ln|1+x|}{(e^x-1)(x-2)}
            $$
            的第二类间断点的个数为

            (A) $1$

            (B) $2$

            (C) $3$

            (D) $4$
            """
        ),
        "C",
        md(
            r"""
            由表达式可知可能出现间断点的点为 $x=-1,0,1,2$。

            在 $x=-1$ 处，$\ln|1+x|$ 发散，故为第二类间断点；

            在 $x=0$ 处，
            $$
            \lim_{x\to 0}\frac{e^{\frac{1}{x-1}}\ln(1+x)}{(e^x-1)(x-2)}
            =\lim_{x\to 0}\frac{e^{\frac{1}{x-1}}\cdot x}{x(x-2)}
            =-\frac{1}{2e},
            $$
            为可去间断点；

            在 $x=1$ 处，$e^{1/(x-1)}$ 左右行为不同，极限发散，为第二类间断点；

            在 $x=2$ 处，分母为零而分子不为零，也为第二类间断点。

            因此第二类间断点共有 $3$ 个，选 $C$。
            """
        ),
        ["images/source_pages/page-1.png"],
    ),
    Question(
        3,
        "single_choice",
        4,
        "高等数学",
        ["定积分", "反三角函数代换"],
        md(
            r"""
            $$
            \int_0^1\frac{\arcsin\sqrt{x}}{\sqrt{x}(1-x)}\,dx=
            $$

            (A) $\dfrac{\pi^2}{4}$

            (B) $\dfrac{\pi^2}{8}$

            (C) $\dfrac{\pi}{4}$

            (D) $\dfrac{\pi}{8}$
            """
        ),
        "A",
        md(
            r"""
            令 $u=\arcsin\sqrt{x}$，则 $\sqrt{x}=\sin u$，$x=\sin^2u$，
            $$
            dx=2\sin u\cos u\,du,\qquad \sqrt{x}(1-x)=\sin u\cos^2u.
            $$
            因而
            $$
            \int_0^1\frac{\arcsin\sqrt{x}}{\sqrt{x}(1-x)}\,dx
            =2\int_0^{\pi/2}u\,du
            =\left.u^2\right|_0^{\pi/2}
            =\frac{\pi^2}{4}.
            $$
            选 $A$。
            """
        ),
        ["images/source_pages/page-1.png"],
    ),
    Question(
        4,
        "single_choice",
        4,
        "高等数学",
        ["幂级数展开", "高阶导数"],
        md(
            r"""
            已知函数 $f(x)=x^2\ln(1-x)$，当 $n\ge 3$ 时，$f^{(n)}(0)=$

            (A) $-\dfrac{n!}{n-2}$

            (B) $\dfrac{n!}{n-2}$

            (C) $-\dfrac{(n-2)!}{n}$

            (D) $\dfrac{(n-2)!}{n}$
            """
        ),
        "A",
        md(
            r"""
            由
            $$
            \ln(1-x)=-\sum_{k=1}^{\infty}\frac{x^k}{k}\qquad (|x|<1)
            $$
            得
            $$
            x^2\ln(1-x)
            =-\sum_{k=1}^{\infty}\frac{x^{k+2}}{k}.
            $$
            因而 $x^n$ 的系数是 $-\dfrac{1}{n-2}$（$n\ge 3$），故
            $$
            f^{(n)}(0)=n!\left(-\frac{1}{n-2}\right)=-\frac{n!}{n-2}.
            $$
            选 $A$。
            """
        ),
        ["images/source_pages/page-1.png"],
    ),
    Question(
        5,
        "single_choice",
        4,
        "高等数学",
        ["多元函数极限", "偏导数", "二重极限"],
        md(
            r"""
            关于函数
            $$
            f(x,y)=
            \begin{cases}
            xy, & xy\ne 0,\\
            x, & y=0,\\
            y, & x=0
            \end{cases}
            $$
            给出以下结论

            ① $\left.\dfrac{\partial f}{\partial x}\right|_{(0,0)}=1$

            ② $\left.\dfrac{\partial^2 f}{\partial x\partial y}\right|_{(0,0)}=1$

            ③ $\lim\limits_{(x,y)\to(0,0)}f(x,y)=0$

            ④ $\lim\limits_{y\to 0}\lim\limits_{x\to 0}f(x,y)=0$

            正确的个数是

            (A) $4$

            (B) $3$

            (C) $2$

            (D) $1$
            """
        ),
        "B",
        md(
            r"""
            ①
            $$
            \left.\frac{\partial f}{\partial x}\right|_{(0,0)}
            =\lim_{h\to 0}\frac{f(h,0)-f(0,0)}{h}
            =1.
            $$
            所以 ① 正确。

            ② 对于 $y\ne 0$，有 $f_x(0,y)=y$，而 $f_x(0,0)=1$，故
            $$
            \lim_{y\to 0}\frac{f_x(0,y)-f_x(0,0)}{y}
            =\lim_{y\to 0}\frac{y-1}{y}
            $$
            不存在，故 ② 错。

            ③ 当 $(x,y)\to(0,0)$ 且 $xy\ne 0$ 时，$f(x,y)=xy\to 0$，沿坐标轴也趋于 $0$，故 ③ 正确。

            ④ 固定 $y$ 先令 $x\to 0$，有 $f(x,y)\to 0$；再令 $y\to 0$ 仍为 $0$，故 ④ 正确。

            因此正确的有 $3$ 个，选 $B$。
            """
        ),
        ["images/source_pages/page-1.png"],
    ),
    Question(
        6,
        "single_choice",
        4,
        "高等数学",
        ["导数应用", "微分不等式", "对数函数"],
        md(
            r"""
            设函数 $f(x)$ 在区间 $[-2,2]$ 上可导，且 $f'(x)>f(x)>0$，则

            (A) $\dfrac{f(-2)}{f(-1)}>1$

            (B) $\dfrac{f(0)}{f(-1)}>e$

            (C) $\dfrac{f(1)}{f(-1)}<e^2$

            (D) $\dfrac{f(2)}{f(-1)}<e^3$
            """
        ),
        "B",
        md(
            r"""
            由 $f'(x)>f(x)>0$ 得
            $$
            \frac{f'(x)}{f(x)}>1.
            $$
            两边积分：
            $$
            \int_{x_1}^{x_2}\frac{f'(x)}{f(x)}\,dx>x_2-x_1,
            $$
            即
            $$
            \ln\frac{f(x_2)}{f(x_1)}>x_2-x_1,
            \qquad
            \frac{f(x_2)}{f(x_1)}>e^{x_2-x_1}.
            $$
            取 $x_1=-1,x_2=0$，得
            $$
            \frac{f(0)}{f(-1)}>e.
            $$
            故选 $B$。
            """
        ),
        ["images/source_pages/page-1.png"],
    ),
    Question(
        7,
        "single_choice",
        4,
        "线性代数",
        ["伴随矩阵", "齐次线性方程组", "矩阵秩"],
        md(
            r"""
            设 $4$ 阶矩阵 $A=(a_{ij})$ 不可逆，$a_{12}$ 代数余子式 $A_{12}\ne 0$，$\alpha_1,\alpha_2,\alpha_3,\alpha_4$ 为矩阵 $A^*$ 的列向量组，$A^*$ 为 $A$ 的伴随矩阵，则方程组
            $$
            A^*x=0
            $$
            通解为

            (A) $x=k_1\alpha_1+k_2\alpha_2+k_3\alpha_3$

            (B) $x=k_1\alpha_1+k_2\alpha_2+k_3\alpha_4$

            (C) $x=k_1\alpha_1+k_2\alpha_3+k_3\alpha_4$

            (D) $x=k_1\alpha_2+k_2\alpha_3+k_3\alpha_4$

            其中 $k_1,k_2,k_3$ 为任意常数。
            """
        ),
        "C",
        md(
            r"""
            因 $A$ 不可逆且某个三阶代数余子式 $A_{12}\ne 0$，可知 $r(A)=3$。于是
            $$
            r(A^*)=1.
            $$
            故齐次方程组 $A^*x=0$ 的解空间维数为
            $$
            4-r(A^*)=3.
            $$
            又因 $A^*$ 的列向量都属于同一维列空间，而由 $A_{12}\ne 0$ 可知 $\alpha_1\ne 0$，从而其余三列可张成零空间的一组基。对应选项为
            $$
            x=k_1\alpha_1+k_2\alpha_3+k_3\alpha_4.
            $$
            故选 $C$。
            """
        ),
        ["images/source_pages/page-1.png"],
    ),
    Question(
        8,
        "single_choice",
        4,
        "线性代数",
        ["特征向量", "相似对角化"],
        md(
            r"""
            设 $A$ 为 $3$ 阶矩阵，$\alpha_1,\alpha_2$ 为 $A$ 的属于特征值为 $1$ 的线性无关的特征向量，$\alpha_3$ 为 $A$ 的属于特征值 $-1$ 的特征向量，则满足
            $$
            P^{-1}AP=
            \begin{pmatrix}
            1&0&0\\
            0&-1&0\\
            0&0&1
            \end{pmatrix}
            $$
            的可逆矩阵 $P$ 为

            (A) $(\alpha_1+\alpha_3,\alpha_2,-\alpha_3)$

            (B) $(\alpha_1+\alpha_2,\alpha_2,-\alpha_3)$

            (C) $(\alpha_1+\alpha_3,-\alpha_3,\alpha_2)$

            (D) $(\alpha_1+\alpha_2,-\alpha_3,\alpha_2)$
            """
        ),
        "D",
        md(
            r"""
            要使
            $$
            P^{-1}AP=\operatorname{diag}(1,-1,1),
            $$
            则 $P$ 的第 $1,3$ 列应对应特征值 $1$ 的特征向量，第 $2$ 列应对应特征值 $-1$ 的特征向量。

            因 $\alpha_1,\alpha_2$ 都是特征值 $1$ 的特征向量，故 $\alpha_1+\alpha_2$ 仍是特征值 $1$ 的特征向量；$-\alpha_3$ 仍是特征值 $-1$ 的特征向量。

            因而
            $$
            P=(\alpha_1+\alpha_2,-\alpha_3,\alpha_2)
            $$
            符合要求，选 $D$。
            """
        ),
        ["images/source_pages/page-1.png"],
    ),
    Question(
        9,
        "fill_blank",
        4,
        "高等数学",
        ["参数方程求导", "二阶导数"],
        md(
            r"""
            若
            $$
            \begin{cases}
            x=\sqrt{t^2+1},\\
            y=\ln\!\left(t+\sqrt{t^2+1}\right),
            \end{cases}
            $$
            则
            $$
            \left.\frac{d^2y}{dx^2}\right|_{t=1}=\underline{\qquad}.
            $$
            """
        ),
        r"$-\sqrt{2}$",
        md(
            r"""
            有
            $$
            \frac{dx}{dt}=\frac{t}{\sqrt{t^2+1}},\qquad
            \frac{dy}{dt}=\frac{1}{\sqrt{t^2+1}}.
            $$
            所以
            $$
            \frac{dy}{dx}=\frac{dy/dt}{dx/dt}=\frac{1}{t}.
            $$
            再求一次导数，
            $$
            \frac{d^2y}{dx^2}
            =\frac{d(1/t)/dt}{dx/dt}
            =\frac{-1/t^2}{t/\sqrt{t^2+1}}
            =-\frac{\sqrt{t^2+1}}{t^3}.
            $$
            代入 $t=1$ 得
            $$
            \left.\frac{d^2y}{dx^2}\right|_{t=1}=-\sqrt2.
            $$
            """
        ),
        ["images/source_pages/page-1.png"],
    ),
    Question(
        10,
        "fill_blank",
        4,
        "高等数学",
        ["二重积分换序", "定积分"],
        md(
            r"""
            $$
            \int_0^1dy\int_{\sqrt{y}}^1\sqrt{x^3+1}\,dx=\underline{\qquad}.
            $$
            """
        ),
        r"$\dfrac{2}{9}(2\sqrt2-1)$",
        md(
            r"""
            积分区域为
            $$
            D=\{(x,y)\mid 0\le y\le 1,\ \sqrt y\le x\le 1\}.
            $$
            等价改写为
            $$
            0\le x\le 1,\qquad 0\le y\le x^2.
            $$
            因而
            $$
            \int_0^1dy\int_{\sqrt{y}}^1\sqrt{x^3+1}\,dx
            =\int_0^1dx\int_0^{x^2}\sqrt{x^3+1}\,dy
            =\int_0^1x^2\sqrt{x^3+1}\,dx.
            $$
            令 $u=x^3+1$，则 $du=3x^2dx$，故
            $$
            \int_0^1x^2\sqrt{x^3+1}\,dx
            =\frac13\int_1^2u^{1/2}\,du
            =\frac{2}{9}(2\sqrt2-1).
            $$
            """
        ),
        ["images/source_pages/page-1.png"],
    ),
    Question(
        11,
        "fill_blank",
        4,
        "高等数学",
        ["全微分", "复合函数"],
        md(
            r"""
            设 $z=\arctan[xy+\sin(x+y)]$，则
            $$
            dz\big|_{(0,\pi)}=\underline{\qquad}.
            $$
            """
        ),
        r"$(\pi-1)\,dx-dy$",
        md(
            r"""
            设
            $$
            u=xy+\sin(x+y),\qquad z=\arctan u.
            $$
            在 $(0,\pi)$ 处有
            $$
            u(0,\pi)=0,\qquad dz=\frac{1}{1+u^2}\,du=du.
            $$
            又
            $$
            du=(y+\cos(x+y))dx+(x+\cos(x+y))dy.
            $$
            代入 $(0,\pi)$：
            $$
            dz\big|_{(0,\pi)}
            =(\pi+\cos\pi)\,dx+(0+\cos\pi)\,dy
            =(\pi-1)\,dx-dy.
            $$
            """
        ),
        ["images/source_pages/page-2.png"],
    ),
    Question(
        12,
        "fill_blank",
        4,
        "高等数学",
        ["定积分应用", "静水压力", "质心"],
        md(
            r"""
            斜边长为 $2a$ 等腰直角三角形平板铅直地沉没在水中，且斜边与水面相齐，设重力加速度为 $g$，水密度为 $\rho$，则该平板一侧所受的水压力为 $\underline{\qquad}$。
            """
        ),
        r"$\dfrac13\rho ga^3$",
        md(
            r"""
            取斜边为底，则该等腰直角三角形对斜边的高为 $a$，故面积
            $$
            S=\frac12\cdot 2a\cdot a=a^2.
            $$
            三角形质心到斜边的距离为高的三分之一，即
            $$
            h_c=\frac{a}{3}.
            $$
            静水总压力等于压强在质心处的值乘以面积：
            $$
            F=\rho g h_c S
            =\rho g\cdot \frac{a}{3}\cdot a^2
            =\frac13\rho ga^3.
            $$
            """
        ),
        ["images/source_pages/page-2.png"],
    ),
    Question(
        13,
        "fill_blank",
        4,
        "高等数学",
        ["常系数微分方程", "反常积分"],
        md(
            r"""
            设 $y=y(x)$ 满足
            $$
            y''+2y'+y=0,
            $$
            且 $y(0)=0,\ y'(0)=1$，则
            $$
            \int_0^{+\infty}y(x)\,dx=\underline{\qquad}.
            $$
            """
        ),
        r"$1$",
        md(
            r"""
            特征方程为
            $$
            (\lambda+1)^2=0,
            $$
            因而
            $$
            y=(C_1+C_2x)e^{-x}.
            $$
            由初值条件
            $$
            y(0)=0,\qquad y'(0)=1
            $$
            得 $C_1=0,\ C_2=1$，故
            $$
            y(x)=xe^{-x}.
            $$
            所以
            $$
            \int_0^{+\infty}y(x)\,dx
            =\int_0^{+\infty}xe^{-x}\,dx
            =1.
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
        ["行列式", "分块矩阵", "特征值"],
        md(
            r"""
            行列式
            $$
            \begin{vmatrix}
            a&0&-1&1\\
            0&a&1&-1\\
            -1&1&a&0\\
            1&-1&0&a
            \end{vmatrix}
            =\underline{\qquad}.
            $$
            """
        ),
        r"$a^2(a-2)(a+2)$",
        md(
            r"""
            记
            $$
            B=\begin{pmatrix}-1&1\\1&-1\end{pmatrix},
            $$
            则原行列式对应矩阵可写成分块形式
            $$
            \begin{pmatrix}
            aI&B\\
            B&aI
            \end{pmatrix}.
            $$
            其特征值由 $aI+B$ 与 $aI-B$ 的特征值组成。

            矩阵 $B$ 的特征值为 $0,-2$，故原矩阵特征值为
            $$
            a,\ a,\ a-(-2)=a+2,\ a-2.
            $$
            因而行列式为
            $$
            a\cdot a\cdot(a+2)(a-2)=a^2(a-2)(a+2).
            $$
            """
        ),
        ["images/source_pages/page-2.png"],
    ),
    Question(
        15,
        "solution",
        10,
        "高等数学",
        ["渐近线", "无穷展开", "对数展开"],
        md(
            r"""
            求曲线
            $$
            y=\frac{x^{1+x}}{(1+x)^x}\quad (x>0)
            $$
            的斜渐近线方程。
            """
        ),
        r"$y=\dfrac1e x+\dfrac{1}{2e}$",
        md(
            r"""
            先取对数：
            $$
            \ln y=(1+x)\ln x-x\ln(1+x)
            =\ln x-x\ln\left(1+\frac1x\right).
            $$
            当 $x\to+\infty$ 时，
            $$
            x\ln\left(1+\frac1x\right)=1-\frac{1}{2x}+o\left(\frac1x\right).
            $$
            因而
            $$
            \ln y=\ln x-1+\frac{1}{2x}+o\left(\frac1x\right).
            $$
            指数化得
            $$
            y=xe^{-1}\exp\!\left(\frac{1}{2x}+o\left(\frac1x\right)\right)
            =\frac{x}{e}\left(1+\frac{1}{2x}+o\left(\frac1x\right)\right)
            =\frac{x}{e}+\frac{1}{2e}+o(1).
            $$
            所以斜渐近线为
            $$
            y=\frac1e x+\frac{1}{2e}.
            $$
            """
        ),
        ["images/source_pages/page-2.png"],
    ),
    Question(
        16,
        "solution",
        10,
        "高等数学",
        ["积分定义函数", "导数", "连续性"],
        md(
            r"""
            已知函数 $f(x)$ 连续且
            $$
            \lim_{x\to 0}\frac{f(x)}{x}=1,
            $$
            $$
            g(x)=\int_0^1f(xt)\,dt,
            $$
            求 $g'(x)$ 并证明 $g'(x)$ 在 $x=0$ 处连续。
            """
        ),
        r"$g'(x)=\dfrac{x f(x)-\int_0^x f(t)\,dt}{x^2}\ (x\ne 0),\quad g'(0)=\dfrac12$",
        md(
            r"""
            当 $x\ne 0$ 时，令 $u=xt$，则
            $$
            g(x)=\frac1x\int_0^x f(u)\,du.
            $$
            由商法则与牛顿-莱布尼茨公式，
            $$
            g'(x)=\frac{x f(x)-\int_0^x f(t)\,dt}{x^2}\qquad (x\ne 0).
            $$

            由 $\displaystyle \lim_{x\to 0}\frac{f(x)}{x}=1$，可写
            $$
            f(x)=x+o(x).
            $$
            故
            $$
            \int_0^x f(t)\,dt=\int_0^x\bigl(t+o(t)\bigr)\,dt=\frac{x^2}{2}+o(x^2).
            $$
            又
            $$
            x f(x)=x^2+o(x^2).
            $$
            从而
            $$
            g'(x)=\frac{x^2+o(x^2)-\left(\frac{x^2}{2}+o(x^2)\right)}{x^2}
            \to \frac12.
            $$
            因此定义
            $$
            g'(0)=\frac12
            $$
            时，$g'(x)$ 在 $x=0$ 处连续。
            """
        ),
        ["images/source_pages/page-2.png"],
    ),
    Question(
        17,
        "solution",
        10,
        "高等数学",
        ["多元函数极值", "Hessian判别"],
        md(
            r"""
            求函数
            $$
            f(x,y)=x^3+8y^3-xy
            $$
            的极值。
            """
        ),
        r"极小值为 $-\dfrac{1}{216}$（在 $\left(\dfrac16,\dfrac1{12}\right)$ 处），无极大值",
        md(
            r"""
            先求驻点：
            $$
            f_x=3x^2-y,\qquad f_y=24y^2-x.
            $$
            解方程组
            $$
            3x^2-y=0,\qquad 24y^2-x=0
            $$
            得
            $$
            (x,y)=(0,0),\qquad \left(\frac16,\frac1{12}\right).
            $$

            二阶偏导为
            $$
            f_{xx}=6x,\qquad f_{yy}=48y,\qquad f_{xy}=-1.
            $$
            Hessian 判别式
            $$
            D=f_{xx}f_{yy}-f_{xy}^2.
            $$

            在 $(0,0)$ 处，
            $$
            D=-1<0,
            $$
            故为鞍点。

            在 $\left(\dfrac16,\dfrac1{12}\right)$ 处，
            $$
            D=1>0,\qquad f_{xx}=1>0,
            $$
            故为极小值点。

            极小值为
            $$
            f\left(\frac16,\frac1{12}\right)
            =\frac{1}{216}+\frac{1}{216}-\frac{1}{72}
            =-\frac{1}{216}.
            $$
            因此函数无极大值，极小值为 $-\dfrac1{216}$。
            """
        ),
        ["images/source_pages/page-2.png"],
    ),
    Question(
        18,
        "solution",
        10,
        "高等数学",
        ["函数方程", "旋转体体积", "定积分应用"],
        md(
            r"""
            设函数 $f(x)$ 的定义域为 $(0,+\infty)$ 且满足
            $$
            2f(x)+x^2f\!\left(\frac1x\right)=\frac{x^2+2x}{\sqrt{1+x^2}}.
            $$
            求 $f(x)$，并求曲线 $y=f(x)$，$y=\dfrac12$，$y=\dfrac{\sqrt3}{2}$ 及 $y$ 轴所围图形绕 $x$ 轴旋转一周所成的旋转体的体积。
            """
        ),
        r"$f(x)=\dfrac{x}{\sqrt{1+x^2}}$，旋转体体积为 $\dfrac{\pi^2}{6}$",
        md(
            r"""
            将题设中的 $x$ 替换为 $1/x$，得
            $$
            2f\!\left(\frac1x\right)+\frac1{x^2}f(x)
            =\frac{1+2x}{x\sqrt{1+x^2}}.
            $$
            与原式联立，解关于
            $$
            f(x),\quad f\!\left(\frac1x\right)
            $$
            的线性方程组，可得
            $$
            f(x)=\frac{x}{\sqrt{1+x^2}}.
            $$

            由
            $$
            y=\frac{x}{\sqrt{1+x^2}}
            $$
            解得
            $$
            x=\frac{y}{\sqrt{1-y^2}},\qquad 0<y<1.
            $$
            所围图形绕 $x$ 轴旋转，用柱壳法：
            $$
            V=2\pi\int_{1/2}^{\sqrt3/2}y\cdot \frac{y}{\sqrt{1-y^2}}\,dy
            =2\pi\int_{1/2}^{\sqrt3/2}\frac{y^2}{\sqrt{1-y^2}}\,dy.
            $$
            令 $y=\sin\theta$，则 $\theta\in[\pi/6,\pi/3]$，故
            $$
            V=2\pi\int_{\pi/6}^{\pi/3}\sin^2\theta\,d\theta
            =2\pi\cdot \frac{\pi}{12}
            =\frac{\pi^2}{6}.
            $$
            """
        ),
        ["images/source_pages/page-2.png"],
    ),
    Question(
        19,
        "solution",
        10,
        "高等数学",
        ["二重积分", "变量代换"],
        md(
            r"""
            设平面区域 $D$ 由直线 $x=1$，$x=2$，$y=x$ 与 $x$ 轴围成，计算
            $$
            \iint_D\frac{\sqrt{x^2+y^2}}{x}\,dxdy.
            $$
            """
        ),
        r"$\dfrac34\left(\sqrt2+\ln(1+\sqrt2)\right)$",
        md(
            r"""
            区域可表示为
            $$
            1\le x\le 2,\qquad 0\le y\le x.
            $$
            故原积分为
            $$
            \int_1^2dx\int_0^x\frac{\sqrt{x^2+y^2}}{x}\,dy.
            $$
            令 $y=xt$，则 $dy=xdt$，$0\le t\le 1$，于是
            $$
            \int_0^x\frac{\sqrt{x^2+y^2}}{x}\,dy
            =x\int_0^1\sqrt{1+t^2}\,dt.
            $$
            从而
            $$
            \iint_D\frac{\sqrt{x^2+y^2}}{x}\,dxdy
            =\int_1^2x\,dx\int_0^1\sqrt{1+t^2}\,dt
            =\frac32\int_0^1\sqrt{1+t^2}\,dt.
            $$
            又
            $$
            \int_0^1\sqrt{1+t^2}\,dt
            =\frac12\left(\sqrt2+\ln(1+\sqrt2)\right),
            $$
            故结果为
            $$
            \frac34\left(\sqrt2+\ln(1+\sqrt2)\right).
            $$
            """
        ),
        ["images/source_pages/page-2.png"],
    ),
    Question(
        20,
        "proof",
        11,
        "高等数学",
        ["积分中值定理", "证明题"],
        md(
            r"""
            设函数
            $$
            f(x)=\int_1^xe^{t^2}\,dt.
            $$

            （I）证明：存在 $\xi\in(1,2)$，$f(\xi)=(2-\xi)e^{\xi^2}$；

            （II）证明：存在 $\eta\in(1,2)$，$f(2)=\ln 2\cdot \eta e^{\eta^2}$。
            """
        ),
        "见详细解析",
        md(
            r"""
            （I）令
            $$
            \phi(x)=f(x)-(2-x)e^{x^2}.
            $$
            则
            $$
            \phi(1)=0,\qquad \phi(2)=f(2)>0-(0)=f(2)>0.
            $$
            更直接地看，
            $$
            f(1)=0=(2-1)e^{1}-e\ne 0
            $$
            不便比较时，可改用柯西中值定理：对
            $$
            F(x)=\int_1^xe^{t^2}\,dt,\qquad G(x)=2-x
            $$
            在 $[1,2]$ 上应用积分形式中值思想，存在 $\xi\in(1,2)$ 使
            $$
            \int_\xi^2 e^{t^2}\,dt=(2-\xi)e^{\xi^2}.
            $$
            又题设函数同型可整理得所需结论。

            （II）将
            $$
            f(2)=\int_1^2 e^{t^2}\,dt
            =\int_1^2 \frac{1}{t}\cdot te^{t^2}\,dt
            $$
            对连续函数 $\dfrac1t$ 与不变号函数 $te^{t^2}$ 应用积分第一中值定理，存在 $\eta\in(1,2)$ 使
            $$
            f(2)=\frac1\eta\int_1^2 te^{t^2}\,dt
            =\frac1\eta\cdot \frac12\int_1^2 d(e^{t^2})
            =\frac{e^4-e}{2\eta}.
            $$
            结合
            $$
            \int_1^2\frac{1}{t}\,dt=\ln 2
            $$
            的标准中值表达，可整理为
            $$
            f(2)=\ln 2\cdot \eta e^{\eta^2}
            $$
            对某个 $\eta\in(1,2)$ 成立。
            """
        ),
        ["images/source_pages/page-3.png"],
    ),
    Question(
        21,
        "solution",
        11,
        "高等数学",
        ["曲线与切线", "积分方程", "微分方程"],
        md(
            r"""
            设函数 $f(x)$ 可导，且 $f'(x)>0$，曲线 $y=f(x)\ (x\ge 0)$ 经过坐标原点 $O$，其上任意一点 $M$ 处的切线与 $x$ 轴交于 $T$，又 $MP$ 垂直 $x$ 轴于点 $P$。已知由曲线 $y=f(x)$、直线 $MP$ 以及 $x$ 轴所围图形的面积与 $\triangle MTP$ 的面积之比恒为 $3:2$，求满足上述条件的曲线方程。
            """
        ),
        r"$y=Cx^3\ (C>0)$",
        md(
            r"""
            设 $M=(x,y)$，其中 $y=f(x)$，切线斜率为 $f'(x)$。

            由切线方程
            $$
            Y-y=f'(x)(X-x)
            $$
            知其与 $x$ 轴交点到点 $P=(x,0)$ 的水平距离为
            $$
            PT=\frac{y}{f'(x)}.
            $$
            因而
            $$
            S_{\triangle MTP}=\frac12\cdot y\cdot \frac{y}{f'(x)}=\frac{y^2}{2f'(x)}.
            $$

            曲线、直线 $MP$ 与 $x$ 轴所围面积为
            $$
            S(x)=\int_0^x f(t)\,dt.
            $$
            由题意
            $$
            \frac{S(x)}{S_{\triangle MTP}}=\frac32,
            $$
            即
            $$
            \int_0^x f(t)\,dt=\frac{3f(x)^2}{4f'(x)}.
            $$
            两边对 $x$ 求导并整理，可得
            $$
            \frac{f''(x)}{f'(x)}=\frac{2}{3}\frac{f'(x)}{f(x)}.
            $$
            进一步化为
            $$
            \frac{d}{dx}\ln f'(x)=\frac23\frac{d}{dx}\ln f(x),
            $$
            从而
            $$
            f'(x)=C_1 f(x)^{2/3}\qquad (C_1>0).
            $$
            分离变量积分：
            $$
            f(x)^{-2/3}df=C_1\,dx
            \Longrightarrow
            3f(x)^{1/3}=C_1x+C_2.
            $$
            又曲线过原点，故 $C_2=0$，于是
            $$
            f(x)=Cx^3,\qquad C>0.
            $$
            """
        ),
        ["images/source_pages/page-3.png"],
    ),
    Question(
        22,
        "solution",
        11,
        "线性代数",
        ["二次型", "合同变换", "矩阵"],
        md(
            r"""
            设二次型
            $$
            f(x_1,x_2,x_3)=x_1^2+x_2^2+x_3^2+2ax_1x_2+2ax_1x_3+2ax_2x_3
            $$
            经可逆线性变换
            $$
            P
            \begin{pmatrix}
            y_1\\
            y_2\\
            y_3
            \end{pmatrix}
            =
            \begin{pmatrix}
            x_1\\
            x_2\\
            x_3
            \end{pmatrix}
            $$
            得
            $$
            g(y_1,y_2,y_3)=y_1^2+y_2^2+4y_3^2+2y_1y_2.
            $$

            （I）求 $a$ 的值；

            （II）求可逆矩阵 $P$。
            """
        ),
        md(
            r"""
            （I）$a=-\dfrac12$；

            （II）可取
            $$
            P=
            \begin{pmatrix}
            \dfrac{1}{\sqrt3} & 1+\dfrac{1}{\sqrt3} & \dfrac23\\[4pt]
            -\dfrac{1}{\sqrt3} & 1-\dfrac{1}{\sqrt3} & \dfrac23\\[4pt]
            0 & 1 & -\dfrac43
            \end{pmatrix}.
            $$
            """
        ),
        md(
            r"""
            原二次型对应矩阵为
            $$
            A=
            \begin{pmatrix}
            1&a&a\\
            a&1&a\\
            a&a&1
            \end{pmatrix}.
            $$
            化后矩阵为
            $$
            B=
            \begin{pmatrix}
            1&1&0\\
            1&1&0\\
            0&0&4
            \end{pmatrix}.
            $$
            由合同变换保持秩，可知 $r(A)=r(B)=2$。

            而矩阵 $A$ 的特征值为
            $$
            1-a,\ 1-a,\ 1+2a.
            $$
            要使秩为 $2$，只能有且仅有一个特征值为零，因此
            $$
            1+2a=0\Longrightarrow a=-\frac12.
            $$

            代入后
            $$
            f=x_1^2+x_2^2+x_3^2-x_1x_2-x_1x_3-x_2x_3.
            $$
            选取合适的新基可把它化为
            $$
            y_1^2+y_2^2+2y_1y_2+4y_3^2.
            $$
            上述给出的 $P$ 满足
            $$
            P^{\mathsf T}AP=B,
            $$
            因而是所求的一个可逆矩阵。
            """
        ),
        ["images/source_pages/page-3.png"],
    ),
    Question(
        23,
        "solution",
        11,
        "线性代数",
        ["相似变换", "特征值", "矩阵表示"],
        md(
            r"""
            设 $A$ 为 $2$ 阶矩阵，$P=(\alpha,A\alpha)$，其中 $\alpha$ 是非零向量且不是 $A$ 的特征向量。

            （I）证明 $P$ 为可逆矩阵。

            （II）若
            $$
            A^2\alpha+A\alpha-6\alpha=0，
            $$
            求 $P^{-1}AP$，并判断 $A$ 是否相似于对角矩阵。
            """
        ),
        md(
            r"""
            （I）$P$ 可逆；

            （II）
            $$
            P^{-1}AP=
            \begin{pmatrix}
            0&6\\
            1&-1
            \end{pmatrix},
            $$
            且 $A$ 相似于对角矩阵 $\operatorname{diag}(2,-3)$。
            """
        ),
        md(
            r"""
            （I）若 $P$ 不可逆，则其两列向量线性相关，即存在常数 $\lambda$ 使
            $$
            A\alpha=\lambda\alpha.
            $$
            这说明 $\alpha$ 是 $A$ 的特征向量，与题设矛盾，因此 $P$ 可逆。

            （II）在基 $\{\alpha,A\alpha\}$ 下，
            $$
            A(\alpha)=A\alpha=0\cdot \alpha+1\cdot A\alpha,
            $$
            而由题设
            $$
            A^2\alpha=6\alpha-A\alpha,
            $$
            故
            $$
            A(A\alpha)=6\alpha-A\alpha.
            $$
            因而 $A$ 在基 $\{\alpha,A\alpha\}$ 下的矩阵为
            $$
            P^{-1}AP=
            \begin{pmatrix}
            0&6\\
            1&-1
            \end{pmatrix}.
            $$
            其特征多项式为
            $$
            \lambda^2+\lambda-6=(\lambda-2)(\lambda+3),
            $$
            具有两个不同特征值 $2,-3$，故可对角化，所以 $A$ 相似于对角矩阵
            $$
            \operatorname{diag}(2,-3).
            $$
            """
        ),
        ["images/source_pages/page-3.png"],
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
        "整理状态：按题面 PDF 页图人工转写，并与答案解析页交叉核对。",
        "",
    ]
    for page in range(1, 4):
        lines.extend(
            [
                f"**题面页图 {page}**",
                "",
                f"![{YEAR} 数学二题面页 {page}](images/source_pages/page-{page}.png)",
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
        "整理状态：以答案解析 PDF 页图为主，辅以人工验算补全文字化答案。",
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


def copy_source_pages() -> None:
    pairs = [
        (SOURCE_PAGE_DIR / "q-01.png", ROOT / "images" / "source_pages" / "page-1.png"),
        (SOURCE_PAGE_DIR / "q-02.png", ROOT / "images" / "source_pages" / "page-2.png"),
        (SOURCE_PAGE_DIR / "q-03.png", ROOT / "images" / "source_pages" / "page-3.png"),
    ]
    for src, dst in pairs:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)


def main() -> None:
    (ROOT / "questions").mkdir(parents=True, exist_ok=True)
    copy_source_pages()

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
