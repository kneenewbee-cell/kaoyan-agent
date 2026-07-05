from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from textwrap import dedent

from PIL import Image


ROOT = Path(__file__).resolve().parent
YEAR = 2008
EXAM_ID = f"kaoyan_math2_{YEAR}"
PDF_PATH = Path(r"D:\百度网盘\高数资料\【01】1987-2022年考研数学二真题（PDF）\【合集打印】1987-2009考研数学二真题【共58页】.pdf")
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
    Question(1, "single_choice", 4, "高等数学", ["罗尔定理", "导数零点"],
        md(r"""
        设函数
        $$
        f(x)=x^2(x-1)(x-2),
        $$
        则 $f'(x)$ 的零点个数为（ ）

        A. $0$  B. $1$  C. $2$  D. $3$
        """),
        "D",
        md(r"""
        由 $f(0)=f(1)=f(2)=0$，在区间 $(0,1)$、$(1,2)$ 内各由罗尔定理得到一个零点。
        又 $f'(x)$ 是三次多项式，不可能恰有两个实零点，因此只能有三个实零点，选 D。
        """),
        ["images/source_pages/page-1.png"]),
    Question(2, "single_choice", 4, "高等数学", ["定积分几何意义", "分部积分"],
        md(r"""
        如图，曲线段的方程为 $y=f(x)$，函数 $f(x)$ 在区间 $[0,a]$ 上有连续的导数，则
        $$
        \int_0^a xf'(x)\,dx
        $$
        等于（ ）

        A. 曲边梯形 $ABOD$ 的面积
        B. 梯形 $ABOD$ 的面积
        C. 曲边三角形 $ACD$ 的面积
        D. 三角形 $ACD$ 的面积
        """),
        "C",
        md(r"""
        分部积分得
        $$
        \int_0^a xf'(x)\,dx=af(a)-\int_0^a f(x)\,dx.
        $$
        其中 $af(a)$ 是矩形 $ABOC$ 的面积，$\int_0^a f(x)\,dx$ 是曲边梯形 $ABOD$ 的面积，
        二者之差正是曲边三角形 $ACD$ 的面积，故选 C。
        """),
        ["images/source_pages/page-1.png", "images/q002_diagram.png"]),
    Question(3, "single_choice", 4, "高等数学", ["常系数线性微分方程", "特征方程"],
        md(r"""
        在下列微分方程中，以
        $$
        y=C_1e^x+C_2\cos2x+C_3\sin2x
        $$
        为通解的是（ ）

        A. $y'''+y''-4y'-4y=0$
        B. $y'''+y''+4y'+4y=0$
        C. $y'''-y''-4y'+4y=0$
        D. $y'''-y''+4y'-4y=0$
        """),
        "D",
        md(r"""
        通解对应特征根为 $1,\pm2i$，故特征方程为
        $$
        (r-1)(r^2+4)=r^3-r^2+4r-4=0.
        $$
        因而对应微分方程为 $y'''-y''+4y'-4y=0$，选 D。
        """),
        ["images/source_pages/page-1.png"]),
    Question(4, "single_choice", 4, "高等数学", ["间断点", "极限"],
        md(r"""
        设函数
        $$
        f(x)=\frac{\ln|x|}{|x-1|}\sin x,
        $$
        则 $f(x)$ 有（ ）

        A. $1$ 个可去间断点，$1$ 个跳跃间断点
        B. $1$ 个可去间断点，$1$ 个无穷间断点
        C. $2$ 个跳跃间断点
        D. $2$ 个无穷间断点
        """),
        "A",
        md(r"""
        在 $x=0,1$ 处函数无定义。由
        $$
        \lim_{x\to0}\ln|x|\sin x=0
        $$
        可知 $x=0$ 是可去间断点；而 $x\to1^\pm$ 时左右极限存在但不相等，所以 $x=1$ 是跳跃间断点，选 A。
        """),
        ["images/source_pages/page-1.png"]),
    Question(5, "single_choice", 4, "高等数学", ["单调有界函数", "数列极限"],
        md(r"""
        设函数 $f(x)$ 在 $(-\infty,+\infty)$ 内单调有界，$\{x_n\}$ 为数列，下列命题正确的是（ ）

        A. 若 $\{x_n\}$ 收敛，则 $\{f(x_n)\}$ 收敛
        B. 若 $\{x_n\}$ 单调，则 $\{f(x_n)\}$ 收敛
        C. 若 $\{f(x_n)\}$ 收敛，则 $\{x_n\}$ 收敛
        D. 若 $\{f(x_n)\}$ 单调，则 $\{x_n\}$ 收敛
        """),
        "B",
        md(r"""
        若 $\{x_n\}$ 单调，则由 $f$ 单调知 $\{f(x_n)\}$ 也单调；又因为 $f$ 有界，故 $\{f(x_n)\}$ 单调有界，
        必收敛，因此 B 正确。
        """),
        ["images/source_pages/page-1.png"]),
    Question(6, "single_choice", 4, "高等数学", ["二重积分", "变上限积分"],
        md(r"""
        设函数 $f$ 连续。若
        $$
        F(u,v)=\iint_{D_{uv}}\frac{f(x^2+y^2)}{\sqrt{x^2+y^2}}\,dx\,dy,
        $$
        其中区域 $D_{uv}$ 为图中阴影部分，则
        $$
        \frac{\partial F}{\partial u}=(\ \ )
        $$

        A. $vf(u^2)$
        B. $\dfrac{v}{u}f(u^2)$
        C. $v f(u)$
        D. $\dfrac{v}{u}f(u)$
        """),
        "A",
        md(r"""
        改用极坐标，区域为 $1\le r\le u,\ 0\le\theta\le v$，故
        $$
        F(u,v)=\int_0^v\int_1^u f(r^2)\,dr\,d\theta
        =v\int_1^u f(r^2)\,dr.
        $$
        对 $u$ 求导即得
        $$
        \frac{\partial F}{\partial u}=vf(u^2).
        $$
        """),
        ["images/source_pages/page-1.png", "images/q006_diagram.png"]),
    Question(7, "single_choice", 4, "线性代数", ["矩阵可逆", "幂零矩阵"],
        md(r"""
        设 $A$ 为 $n$ 阶非零矩阵，$E$ 为 $n$ 阶单位阵。若 $A^3=O$，则（ ）

        A. $E-A$ 不可逆，$E+A$ 不可逆
        B. $E-A$ 不可逆，$E+A$ 可逆
        C. $E-A$ 可逆，$E+A$ 可逆
        D. $E-A$ 可逆，$E+A$ 不可逆
        """),
        "C",
        md(r"""
        因为 $A^3=O$，有
        $$
        (E-A)(E+A+A^2)=E-A^3=E,
        $$
        $$
        (E+A)(E-A+A^2)=E+A^3=E.
        $$
        所以 $E-A$、$E+A$ 都可逆，选 C。
        """),
        ["images/source_pages/page-1.png"]),
    Question(8, "single_choice", 4, "线性代数", ["矩阵合同", "实对称矩阵"],
        md(r"""
        设
        $$
        A=\begin{pmatrix}1&2\\2&1\end{pmatrix},
        $$
        则在实数域上与 $A$ 合同的矩阵为（ ）

        A. $\begin{pmatrix}-2&1\\1&-2\end{pmatrix}$
        B. $\begin{pmatrix}2&-1\\-1&2\end{pmatrix}$
        C. $\begin{pmatrix}2&1\\1&2\end{pmatrix}$
        D. $\begin{pmatrix}1&-2\\-2&1\end{pmatrix}$
        """),
        "D",
        md(r"""
        $A$ 为实对称矩阵，其特征值为 $3,-1$，惯性指标为 $(1,1)$。四个选项中只有 D 的特征值也为 $3,-1$，
        与 $A$ 有相同惯性指标，因此在实数域上与 $A$ 合同，选 D。
        """),
        ["images/source_pages/page-1.png"]),
    Question(9, "fill_blank", 4, "高等数学", ["极限", "连续性"],
        md(r"""
        已知函数 $f(x)$ 连续，且
        $$
        \lim_{x\to0}\frac{1-\cos[xf(x)]}{(e^{x^2}-1)f(x)}=1,
        $$
        则 $f(0)=$ ________。
        """),
        "$2$",
        md(r"""
        由 $1-\cos t\sim \dfrac{t^2}{2}$，$e^{x^2}-1\sim x^2$，得
        $$
        \lim_{x\to0}\frac{\frac12x^2f^2(x)}{x^2f(x)}=\lim_{x\to0}\frac{f(x)}2=1.
        $$
        由连续性可知 $f(0)=2$。
        """),
        ["images/source_pages/page-2.png"]),
    Question(10, "fill_blank", 4, "高等数学", ["一阶微分方程", "线性方程"],
        md(r"""
        微分方程
        $$
        (y+x^2e^{-x})\,dx-x\,dy=0
        $$
        的通解是 $y=$ ________。
        """),
        r"$y=(x-1)e^{-x}+Cx$",
        md(r"""
        方程化为
        $$
        y'-\frac1x y=xe^{-x}.
        $$
        线性方程积分因子为 $x^{-1}$，故
        $$
        \left(\frac yx\right)'=e^{-x}.
        $$
        积分得
        $$
        \frac yx=-(x+1)\frac{e^{-x}}x + C,
        $$
        整理可得
        $$
        y=(x-1)e^{-x}+Cx.
        $$
        """),
        ["images/source_pages/page-2.png"]),
    Question(11, "fill_blank", 4, "高等数学", ["隐函数", "切线方程"],
        md(r"""
        曲线
        $$
        \sin(xy)+\ln(y-x)=x
        $$
        在点 $(0,1)$ 处的切线方程是 ________。
        """),
        r"$y=x+1$",
        md(r"""
        设
        $$
        F(x,y)=\sin(xy)+\ln(y-x)-x.
        $$
        由隐函数求导得
        $$
        F_x+F_y y'=0.
        $$
        在 $(0,1)$ 处代入可得 $y'(0)=1$，故切线方程为
        $$
        y-1=1(x-0),
        $$
        即 $y=x+1$。
        """),
        ["images/source_pages/page-2.png"]),
    Question(12, "fill_blank", 4, "高等数学", ["拐点", "导数"],
        md(r"""
        曲线
        $$
        y=(x-5)x^{2/3}
        $$
        的拐点坐标为 ________。
        """),
        "$(-1,-6)$",
        md(r"""
        计算二阶导数并考察符号变化。可得 $x=-1$ 时 $y''=0$ 且两侧异号，$x=0$ 虽不可导但两侧同号，
        故真正的拐点在 $x=-1$。代入原式得 $y=-6$，故拐点为 $(-1,-6)$。
        """),
        ["images/source_pages/page-2.png"]),
    Question(13, "fill_blank", 4, "高等数学", ["多元复合函数", "偏导数"],
        md(r"""
        设
        $$
        z=\left(\frac yx\right)^{x/y},
        $$
        则
        $$
        \left.\frac{\partial z}{\partial x}\right|_{(1,2)}
        =\underline{\qquad}.
        $$
        """),
        r"$2(\ln 2-1)$",
        md(r"""
        令 $u=\dfrac yx,\ v=\dfrac xy$，则 $z=u^v$。先取对数
        $$
        \ln z=\frac xy\ln\frac yx,
        $$
        再对 $x$ 求偏导并在 $(1,2)$ 处代入，可得
        $$
        \frac{\partial z}{\partial x}=2(\ln2-1).
        $$
        """),
        ["images/source_pages/page-2.png"]),
    Question(14, "fill_blank", 4, "线性代数", ["特征值", "行列式"],
        md(r"""
        设 $3$ 阶矩阵 $A$ 的特征值为 $2,3,\lambda$。若行列式 $|2A|=-48$，则 $\lambda=$ ________。
        """),
        "$-1$",
        md(r"""
        由特征值性质，
        $$
        |A|=2\cdot3\cdot\lambda=6\lambda.
        $$
        又
        $$
        |2A|=2^3|A|=8\cdot6\lambda=48\lambda=-48,
        $$
        故 $\lambda=-1$。
        """),
        ["images/source_pages/page-2.png"]),
    Question(15, "solution", 9, "高等数学", ["极限", "Taylor 展开"],
        md(r"""
        求极限
        $$
        \lim_{x\to0}\frac{[\sin x-\sin(\sin x)]\sin x}{x^4}.
        $$
        """),
        r"$\dfrac16$",
        md(r"""
        由
        $$
        \sin x=x-\frac{x^3}{6}+o(x^3),\qquad
        \sin(\sin x)=\sin x-\frac{\sin^3x}{6}+o(x^3),
        $$
        得
        $$
        \sin x-\sin(\sin x)=\frac{x^3}{6}+o(x^3).
        $$
        再乘以 $\sin x\sim x$，所以原式极限为 $\dfrac16$。
        """),
        ["images/source_pages/page-2.png"]),
    Question(16, "solution", 10, "高等数学", ["参数方程", "二阶导数"],
        md(r"""
        设函数 $y=y(x)$ 由参数方程
        $$
        \begin{cases}
        x=x(t),\\
        y=\int_0^{t^2}\ln(1+u)\,du
        \end{cases}
        $$
        确定，其中 $x(t)$ 是初值问题
        $$
        \begin{cases}
        \dfrac{dx}{dt}-2te^{-x}=0,\\
        x|_{t=0}=0
        \end{cases}
        $$
        的解，求 $\dfrac{d^2y}{dx^2}$。
        """),
        r"$\dfrac{d^2y}{dx^2}=(1+t^2)\bigl[\ln(1+t^2)+1\bigr]$",
        md(r"""
        由微分方程得
        $$
        xe^x=t^2,\qquad x=\ln(1+t^2).
        $$
        又
        $$
        \frac{dy}{dt}=2t\ln(1+t^2),\qquad
        \frac{dx}{dt}=\frac{2t}{1+t^2}.
        $$
        因而
        $$
        \frac{dy}{dx}=(1+t^2)\ln(1+t^2).
        $$
        再对 $t$ 求导并除以 $\dfrac{dx}{dt}$，得
        $$
        \frac{d^2y}{dx^2}=(1+t^2)\bigl[\ln(1+t^2)+1\bigr].
        $$
        """),
        ["images/source_pages/page-2.png"]),
    Question(17, "solution", 9, "高等数学", ["反常积分", "换元积分"],
        md(r"""
        计算
        $$
        \int_0^1\frac{x^2\arcsin x}{\sqrt{1-x^2}}\,dx.
        $$
        """),
        r"$\dfrac{\pi^2}{16}+\dfrac14$",
        md(r"""
        令 $t=\arcsin x$，则 $x=\sin t,\ dx=\cos t\,dt,\ t\in[0,\pi/2]$，
        原积分化为
        $$
        \int_0^{\pi/2} t\sin^2 t\,dt
        =\frac12\int_0^{\pi/2}t\,dt-\frac12\int_0^{\pi/2}t\cos2t\,dt.
        $$
        计算得结果为
        $$
        \frac{\pi^2}{16}+\frac14.
        $$
        """),
        ["images/source_pages/page-2.png"]),
    Question(18, "solution", 11, "高等数学", ["二重积分", "分区域积分"],
        md(r"""
        计算
        $$
        \iint_D \max\{xy,1\}\,dx\,dy,
        $$
        其中
        $$
        D=\{(x,y)\mid 0\le x\le2,\ 0\le y\le2\}.
        $$
        """),
        r"$\dfrac{19}{4}+\ln2$",
        md(r"""
        曲线 $xy=1$ 将正方形区域分成两部分：一部分取值为 $1$，另一部分取值为 $xy$。
        按 $xy\le1$ 与 $xy\ge1$ 分区积分，整理可得
        $$
        \iint_D\max\{xy,1\}\,dx\,dy=\frac{19}{4}+\ln2.
        $$
        """),
        ["images/source_pages/page-2.png"]),
    Question(19, "solution", 11, "高等数学", ["微分方程", "旋转体侧面积"],
        md(r"""
        设 $f(x)$ 是区间 $[0,+\infty)$ 上具有连续导数的单调增加函数，且 $f(0)=1$。
        对任意 $t\in[0,+\infty)$，直线 $x=0,\ x=t$，曲线 $y=f(x)$ 以及 $x$ 轴所围成的曲边梯形绕 $x$ 轴旋转一周生成一旋转体。
        若该旋转体的侧面积在数值上等于其体积的 $2$ 倍，求函数 $f(x)$ 的表达式。
        """),
        r"$f(x)=\dfrac12\left(e^x+e^{-x}\right)$",
        md(r"""
        体积与侧面积分别为
        $$
        V(t)=\pi\int_0^t f^2(x)\,dx,\qquad
        S(t)=2\pi\int_0^t f(x)\sqrt{1+f'^2(x)}\,dx.
        $$
        由题设 $S(t)=2V(t)$，对 $t$ 求导得
        $$
        f\sqrt{1+f'^2}=f^2.
        $$
        因为 $f>0$，故
        $$
        1+f'^2=f^2.
        $$
        解得
        $$
        f(x)=\frac12\left(e^x+e^{-x}\right),
        $$
        再由 $f(0)=1$ 选定常数。
        """),
        ["images/source_pages/page-2.png"]),
    Question(20, "proof", 11, "高等数学", ["积分中值定理", "拉格朗日中值定理"],
        md(r"""
        （Ⅰ）证明积分中值定理：若函数 $f(x)$ 在闭区间 $[a,b]$ 上连续，则至少存在一点 $\eta\in[a,b]$，使
        $$
        \int_a^b f(x)\,dx=f(\eta)(b-a).
        $$

        （Ⅱ）若函数 $\varphi(x)$ 具有二阶导数，且满足 $\varphi(2)>\varphi(1),\ \varphi(2)>\int_2^3\varphi(x)\,dx$，
        则至少存在一点 $\xi\in(1,3)$，使得 $\varphi''(\xi)<0$。
        """),
        "见解析",
        md(r"""
        （Ⅰ）由连续函数在闭区间上有界，设最小值为 $m$、最大值为 $M$，则
        $$
        m(b-a)\le\int_a^b f(x)\,dx\le M(b-a).
        $$
        再由介值定理即可得存在 $\eta$ 满足结论。

        （Ⅱ）先由（Ⅰ）得存在 $\eta\in[2,3]$ 使
        $$
        \int_2^3\varphi(x)\,dx=\varphi(\eta).
        $$
        结合题设可得 $\eta>2$。随后分别在 $[1,2]$ 与 $[2,\eta]$ 上使用拉格朗日中值定理，
        得到一处导数为正、一处导数为负，再在两点之间对 $\varphi'$ 应用拉格朗日中值定理，即得某点 $\xi$ 使 $\varphi''(\xi)<0$。
        """),
        ["images/source_pages/page-2.png"]),
    Question(21, "solution", 11, "高等数学", ["条件极值", "拉格朗日乘数法"],
        md(r"""
        求函数
        $$
        u=x^2+y^2+z^2
        $$
        在约束条件
        $$
        z=x^2+y^2,\qquad x+y+z=4
        $$
        下的最大值与最小值。
        """),
        "最小值为 $6$，最大值为 $72$",
        md(r"""
        将约束化为平面与抛物面的交线上的最值问题，可用拉格朗日乘数法，
        也可先代入 $z=x^2+y^2$ 后化成二元函数求条件极值。求得临界点为
        $$
        (1,1,2),\qquad (-2,-2,8),
        $$
        对应
        $$
        u=6,\qquad u=72.
        $$
        故最小值为 $6$，最大值为 $72$。
        """),
        ["images/source_pages/page-2.png"]),
    Question(22, "solution", 12, "线性代数", ["行列式", "线性方程组"],
        md(r"""
        设 $n$ 元线性方程组 $Ax=b$，其中
        $$
        A=
        \begin{pmatrix}
        2a&1\\
        a^2&2a&1\\
        &a^2&2a&1\\
        &&\ddots&\ddots&\ddots\\
        &&&a^2&2a&1\\
        &&&&a^2&2a
        \end{pmatrix},
        \qquad
        b=
        \begin{pmatrix}
        1\\0\\ \vdots\\0
        \end{pmatrix}.
        $$

        （Ⅰ）证明行列式 $|A|=(n+1)a^n$；

        （Ⅱ）当 $a$ 为何值时，该方程组有唯一解，并求 $x_1$；

        （Ⅲ）当 $a$ 为何值时，该方程组有无穷多解，并求通解。
        """),
        "见解析",
        md(r"""
        记 $D_n=|A|$，按第一列或用递推可证
        $$
        D_n=(n+1)a^n.
        $$
        因而当且仅当 $a\ne0$ 时，$D_n\ne0$，方程组有唯一解。由克拉默法则可得
        $$
        x_1=\frac{n}{(n+1)a}.
        $$
        当 $a=0$ 时，系数矩阵与增广矩阵秩同为 $n-1$，故有无穷多解；通解可写成
        $$
        x_1=1,\ x_2=t,\ x_3=-t,\ \ldots
        $$
        的等价参数形式，其中保留一个自由参数。
        """),
        ["images/source_pages/page-3.png"]),
    Question(23, "solution", 10, "线性代数", ["特征向量", "Jordan 标准形"],
        md(r"""
        设 $A$ 为 $3$ 阶矩阵，$\alpha_1,\alpha_2$ 为 $A$ 的分别属于特征值 $-1,1$ 的特征向量，向量 $\alpha_3$ 满足
        $$
        A\alpha_3=\alpha_2+\alpha_3.
        $$

        （Ⅰ）证明 $\alpha_1,\alpha_2,\alpha_3$ 线性无关；

        （Ⅱ）令 $P=(\alpha_1,\alpha_2,\alpha_3)$，求 $P^{-1}AP$。
        """),
        r"$P^{-1}AP=\begin{pmatrix}-1&0&0\\0&1&1\\0&0&1\end{pmatrix}$",
        md(r"""
        因为 $\alpha_1,\alpha_2$ 分属不同特征值，先知它们线性无关。若 $\alpha_3$ 能由前两者线性表示，
        代入
        $$
        A\alpha_3=\alpha_2+\alpha_3
        $$
        后比较系数会与 $\alpha_1,\alpha_2$ 的线性无关性矛盾，因此三向量线性无关。
        以这组三向量为基，$A$ 的作用为
        $$
        A\alpha_1=-\alpha_1,\qquad A\alpha_2=\alpha_2,\qquad A\alpha_3=\alpha_2+\alpha_3,
        $$
        所以
        $$
        P^{-1}AP=
        \begin{pmatrix}
        -1&0&0\\
        0&1&1\\
        0&0&1
        \end{pmatrix}.
        $$
        """),
        ["images/source_pages/page-3.png"]),
]


def build_card(q: Question) -> str:
    qid = f"{EXAM_ID}_q{q.number:03d}"
    lines = [
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
        f"# {YEAR} 数学二第 {q.number} 题",
        "",
        "## 题目",
        "",
        q.stem,
        "",
        *[f"![题图](../{asset})\n" for asset in q.assets if asset.endswith('.png')],
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
    return "\n".join(lines)


def build_questions_md() -> str:
    lines = [
        f"# {YEAR} 年考研数学二真题",
        "",
        "资料类型：考研数学二历年真题",
        f"年份：{YEAR}",
        "科目：数学二",
        "整理状态：按合集卷页图校对并统一转写。",
        "",
        "**第 1-8 题题图**",
        "",
        "![2008 数学二第 1-8 题题图](images/source_pages/page-1.png)",
        "",
        "**第 9-21 题题图**",
        "",
        "![2008 数学二第 9-21 题题图](images/source_pages/page-2.png)",
        "",
        "**第 22-23 题题图**",
        "",
        "![2008 数学二第 22-23 题题图](images/source_pages/page-3.png)",
        "",
    ]
    for q in QUESTIONS:
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
        for asset in q.assets:
            if asset.endswith("q002_diagram.png") or asset.endswith("q006_diagram.png"):
                lines.extend([f"![第 {q.number} 题题图]({asset})", ""])
    return "\n".join(lines).rstrip() + "\n"


def build_answers_md() -> str:
    lines = [
        f"# Math 2 {YEAR} Answers",
        "",
        "资料类型：考研数学二答案解析",
        f"年份：{YEAR}",
        "科目：数学二",
        "整理状态：依据答案册并结合题面做清洗整理。",
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
        rows.append(json.dumps({
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
        }, ensure_ascii=False))
    return "\n".join(rows) + "\n"


def build_manifest() -> str:
    return json.dumps({
        "exam_id": EXAM_ID,
        "exam_type": "math2",
        "exam_label": "数学二",
        "year": YEAR,
        "source_files": {"questions": f"math2_{YEAR}_questions.md", "answers": f"math2_{YEAR}_answers.md"},
        "card_dir": "questions",
        "index_file": "questions.jsonl",
        "question_count": len(QUESTIONS),
        "explanation_count": len(QUESTIONS),
        "question_ids": [f"{EXAM_ID}_q{q.number:03d}" for q in QUESTIONS],
        "generated_at": now_iso(),
        "review_status": "reviewed",
        "answer_status": "available",
        "explanation_status": "available",
    }, ensure_ascii=False, indent=2) + "\n"


def ensure_dirs() -> None:
    (ROOT / "questions").mkdir(parents=True, exist_ok=True)
    (ROOT / "images" / "source_pages").mkdir(parents=True, exist_ok=True)


def render_source_pages() -> None:
    tmp_prefix = ROOT / "images" / "source_pages" / "tmp_page"
    subprocess.run([str(PDFTOPPM), "-f", "53", "-l", "55", "-png", str(PDF_PATH), str(tmp_prefix)], check=True)
    for src_no, dst_no in zip(range(53, 56), range(1, 4)):
        src = ROOT / "images" / "source_pages" / f"tmp_page-{src_no}.png"
        dst = ROOT / "images" / "source_pages" / f"page-{dst_no}.png"
        if dst.exists():
            dst.unlink()
        src.replace(dst)


def crop_diagrams() -> None:
    with Image.open(ROOT / "images" / "source_pages" / "page-1.png") as img:
        img.crop((780, 350, 1180, 870)).save(ROOT / "images" / "q002_diagram.png")
        img.crop((770, 880, 1180, 1440)).save(ROOT / "images" / "q006_diagram.png")


def write_outputs() -> None:
    (ROOT / f"math2_{YEAR}_questions.md").write_text(build_questions_md(), encoding="utf-8", newline="\n")
    (ROOT / f"math2_{YEAR}_answers.md").write_text(build_answers_md(), encoding="utf-8", newline="\n")
    (ROOT / "questions.jsonl").write_text(build_questions_jsonl(), encoding="utf-8", newline="\n")
    (ROOT / "paper_manifest.json").write_text(build_manifest(), encoding="utf-8", newline="\n")
    for q in QUESTIONS:
        (ROOT / "questions" / f"q{q.number:03d}.md").write_text(build_card(q), encoding="utf-8", newline="\n")


def main() -> None:
    ensure_dirs()
    render_source_pages()
    crop_diagrams()
    write_outputs()


if __name__ == "__main__":
    main()
