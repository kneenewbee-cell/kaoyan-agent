from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parent
YEAR = 2016


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
    Question(
        1,
        "single_choice",
        4,
        "高等数学",
        ["无穷小比较", "等价无穷小"],
        md(
            r"""
            设
            $$
            \alpha_1=x(\cos\sqrt{x}-1),\quad
            \alpha_2=\sqrt{x}\ln(1+\sqrt[3]{x}),\quad
            \alpha_3=\sqrt[3]{x+1}-1.
            $$
            当 $x\to0^+$ 时，以上 3 个无穷小量按阶从低到高的排序是（）

            (A) $\alpha_1,\alpha_2,\alpha_3$

            (B) $\alpha_2,\alpha_3,\alpha_1$

            (C) $\alpha_2,\alpha_1,\alpha_3$

            (D) $\alpha_3,\alpha_2,\alpha_1$
            """
        ),
        "B",
        md(
            r"""
            由
            $\cos\sqrt{x}-1\sim-\dfrac{x}{2}$，
            $\ln(1+\sqrt[3]{x})\sim \sqrt[3]{x}$，
            $\sqrt[3]{x+1}-1\sim\dfrac{x}{3}$，
            得
            $$
            \alpha_1\sim -\frac{x^2}{2},\qquad
            \alpha_2\sim x^{5/6},\qquad
            \alpha_3\sim \frac{x}{3}.
            $$
            比较幂次可知从低阶到高阶为 $\alpha_2,\alpha_3,\alpha_1$，故选 B。
            """
        ),
        ["images/source_pages/page-1.png"],
    ),
    Question(
        2,
        "single_choice",
        4,
        "高等数学",
        ["原函数", "分段函数"],
        md(
            r"""
            已知函数
            $$
            f(x)=
            \begin{cases}
            2(x-1), & x<1,\\
            \ln x, & x\ge 1,
            \end{cases}
            $$
            则 $f(x)$ 的一个原函数是（）

            (A)
            $$
            F(x)=
            \begin{cases}
            (x-1)^2, & x<1,\\
            x(\ln x-1), & x\ge 1
            \end{cases}
            $$

            (B)
            $$
            F(x)=
            \begin{cases}
            (x-1)^2, & x<1,\\
            x(\ln x+1)-1, & x\ge 1
            \end{cases}
            $$

            (C)
            $$
            F(x)=
            \begin{cases}
            (x-1)^2, & x<1,\\
            x(\ln x+1)+1, & x\ge 1
            \end{cases}
            $$

            (D)
            $$
            F(x)=
            \begin{cases}
            (x-1)^2, & x<1,\\
            x(\ln x-1)+1, & x\ge 1
            \end{cases}
            $$
            """
        ),
        "D",
        md(
            r"""
            分段积分得
            $$
            F(x)=
            \begin{cases}
            (x-1)^2+C_1, & x<1,\\
            x(\ln x-1)+C_2, & x\ge1.
            \end{cases}
            $$
            原函数应在分界点连续。令 $x\to1^-$ 与 $x\to1^+$，得
            $C_1=C_2-1$。选项 D 恰满足这一连续条件，故为所求。
            """
        ),
        ["images/source_pages/page-1.png"],
    ),
    Question(
        3,
        "single_choice",
        4,
        "高等数学",
        ["反常积分", "敛散性"],
        md(
            r"""
            反常积分
            $$
            \text{① }\int_{-\infty}^{0}\frac{1}{x^2}e^{1/x}\,dx,\qquad
            \text{② }\int_{0}^{+\infty}\frac{1}{x^2}e^{1/x}\,dx
            $$
            的敛散性为（）

            (A) ① 收敛，② 收敛

            (B) ① 收敛，② 发散

            (C) ① 发散，② 收敛

            (D) ① 发散，② 发散
            """
        ),
        "B",
        md(
            r"""
            令 $u=\dfrac1x$，则
            $$
            \int \frac1{x^2}e^{1/x}\,dx=-e^{1/x}+C.
            $$
            对于 ①，
            $$
            \int_{-\infty}^{0}\frac1{x^2}e^{1/x}\,dx
            =\lim_{R\to-\infty,c\to0^-}\left[-e^{1/x}\right]_{R}^{c}=1,
            $$
            收敛。对于 ②，因 $x\to0^+$ 时 $e^{1/x}\to+\infty$，对应原函数趋于 $-\infty$，故发散。选 B。
            """
        ),
        ["images/source_pages/page-1.png"],
    ),
    Question(
        4,
        "single_choice",
        4,
        "高等数学",
        ["导数图像", "极值", "拐点"],
        md(
            r"""
            设函数 $f(x)$ 在 $(-\infty,+\infty)$ 内连续，其导函数的图形如图所示，则（）

            (A) 函数 $f(x)$ 有 2 个极值点，曲线 $y=f(x)$ 有 2 个拐点

            (B) 函数 $f(x)$ 有 2 个极值点，曲线 $y=f(x)$ 有 3 个拐点

            (C) 函数 $f(x)$ 有 3 个极值点，曲线 $y=f(x)$ 有 1 个拐点

            (D) 函数 $f(x)$ 有 3 个极值点，曲线 $y=f(x)$ 有 2 个拐点
            """
        ),
        "B",
        md(
            r"""
            由 $f'(x)$ 的符号变化判断极值：图中只有两处发生由正到负或由负到正的变化，因此 $f(x)$ 有 2 个极值点。拐点对应 $f'(x)$ 的单调性改变处，包括一处不可导尖点及两处局部极值点，所以共有 3 个拐点。故选 B。
            """
        ),
        ["images/source_pages/page-1.png"],
    ),
    Question(
        5,
        "single_choice",
        4,
        "高等数学",
        ["曲率", "凹凸性", "公切线"],
        md(
            r"""
            设函数 $f_i(x)\ (i=1,2)$ 具有二阶连续导数，且 $f_i''(x_0)<0\ (i=1,2)$。若两条曲线 $y=f_i(x)\ (i=1,2)$ 在点 $(x_0,y_0)$ 处具有公切线 $y=g(x)$，且在该点处曲线 $y=f_1(x)$ 的曲率大于曲线 $y=f_2(x)$ 的曲率，则在 $x_0$ 的某个邻域内，有（）

            (A) $f_1(x)\le f_2(x)\le g(x)$

            (B) $f_2(x)\le f_1(x)\le g(x)$

            (C) $f_1(x)\le g(x)\le f_2(x)$

            (D) $f_2(x)\le g(x)\le f_1(x)$
            """
        ),
        "A",
        md(
            r"""
            由 $f_i''(x_0)<0$ 知两曲线在该点附近均为凹曲线，所以公切线位于曲线上方，即
            $f_1(x)\le g(x),\ f_2(x)\le g(x)$。又因曲率
            $$
            K=\frac{|f''(x_0)|}{\left[1+\left(f'(x_0)\right)^2\right]^{3/2}}
            $$
            且公切意味着 $f_1'(x_0)=f_2'(x_0)$，由 $K_1>K_2$ 得 $|f_1''(x_0)|>|f_2''(x_0)|$，结合二者都小于 0 可知 $f_1$ 向下弯得更厉害，因此在切点附近 $f_1(x)\le f_2(x)$。故选 A。
            """
        ),
        ["images/source_pages/page-1.png"],
    ),
    Question(
        6,
        "single_choice",
        4,
        "高等数学",
        ["二元函数", "偏导数"],
        md(
            r"""
            已知函数
            $$
            f(x,y)=\frac{e^x}{x-y},
            $$
            则（）

            (A) $f_x'-f_y'=0$

            (B) $f_x'+f_y'=0$

            (C) $f_x'-f_y'=f$

            (D) $f_x'+f_y'=f$
            """
        ),
        "D",
        md(
            r"""
            计算得
            $$
            f_x'=\frac{e^x(x-y)-e^x}{(x-y)^2},\qquad
            f_y'=\frac{e^x}{(x-y)^2}.
            $$
            因而
            $$
            f_x'+f_y'=\frac{e^x(x-y)}{(x-y)^2}=\frac{e^x}{x-y}=f.
            $$
            故选 D。
            """
        ),
        ["images/source_pages/page-1.png"],
    ),
    Question(
        7,
        "single_choice",
        4,
        "线性代数",
        ["相似矩阵", "逆矩阵", "转置"],
        md(
            r"""
            设 $A,B$ 是可逆矩阵，且 $A$ 与 $B$ 相似，则下列结论错误的是（）

            (A) $A^{\mathsf T}$ 与 $B^{\mathsf T}$ 相似

            (B) $A^{-1}$ 与 $B^{-1}$ 相似

            (C) $A+A^{\mathsf T}$ 与 $B+B^{\mathsf T}$ 相似

            (D) $A+A^{-1}$ 与 $B+B^{-1}$ 相似
            """
        ),
        "C",
        md(
            r"""
            若 $B=P^{-1}AP$，则
            $$
            B^{\mathsf T}=P^{\mathsf T}A^{\mathsf T}(P^{\mathsf T})^{-1},\qquad
            B^{-1}=P^{-1}A^{-1}P,
            $$
            因而 A、B 两项正确。又
            $$
            B+B^{-1}=P^{-1}(A+A^{-1})P,
            $$
            故 D 也正确。对于 $A+A^{\mathsf T}$ 与 $B+B^{\mathsf T}$，相似关系一般不保持，故错误项为 C。
            """
        ),
        ["images/source_pages/page-1.png"],
    ),
    Question(
        8,
        "single_choice",
        4,
        "线性代数",
        ["二次型", "惯性指数"],
        md(
            r"""
            设二次型
            $$
            f(x_1,x_2,x_3)=a(x_1^2+x_2^2+x_3^2)+2x_1x_2+2x_2x_3+2x_1x_3
            $$
            的正、负惯性指数分别为 1、2，则（）

            (A) $a>1$

            (B) $a<-2$

            (C) $-2<a<1$

            (D) $a=1$ 或 $a=-2$
            """
        ),
        "C",
        md(
            r"""
            二次型对应对称矩阵
            $$
            A=\begin{pmatrix}
            a&1&1\\
            1&a&1\\
            1&1&a
            \end{pmatrix}.
            $$
            其特征值为 $a-1,a-1,a+2$。正、负惯性指数分别为 1、2，说明三个特征值中一正两负，于是
            $$
            a+2>0,\qquad a-1<0,
            $$
            即 $-2<a<1$。故选 C。
            """
        ),
        ["images/source_pages/page-1.png"],
    ),
    Question(
        9,
        "fill_blank",
        4,
        "高等数学",
        ["斜渐近线", "反三角函数"],
        md(
            r"""
            曲线
            $$
            y=\frac{x^3}{1+x^2}+\arctan(1+x^2)
            $$
            的斜渐近线方程为 ________。
            """
        ),
        r"$y=x+\dfrac{\pi}{2}$",
        md(
            r"""
            记 $f(x)=\dfrac{x^3}{1+x^2}+\arctan(1+x^2)$。则
            $$
            \lim_{x\to\infty}\frac{f(x)}{x}
            =\lim_{x\to\infty}\left(\frac{x^2}{1+x^2}+\frac{\arctan(1+x^2)}{x}\right)=1.
            $$
            再算截距：
            $$
            \lim_{x\to\infty}[f(x)-x]
            =\lim_{x\to\infty}\left(-\frac{x}{1+x^2}+\arctan(1+x^2)\right)=\frac{\pi}{2}.
            $$
            故斜渐近线为 $y=x+\dfrac{\pi}{2}$。
            """
        ),
        ["images/source_pages/page-2.png"],
    ),
    Question(
        10,
        "fill_blank",
        4,
        "高等数学",
        ["定积分定义", "Riemann和"],
        md(
            r"""
            极限
            $$
            \lim_{n\to\infty}\frac{1}{n^2}\left(\sin\frac1n+2\sin\frac2n+\cdots+n\sin\frac{n}{n}\right)
            =\underline{\qquad\qquad}.
            $$
            """
        ),
        r"$\sin1-\cos1$",
        md(
            r"""
            原式化为
            $$
            \frac1n\sum_{i=1}^{n}\frac{i}{n}\sin\frac{i}{n},
            $$
            是函数 $x\sin x$ 在 $[0,1]$ 上的 Riemann 和，因此极限为
            $$
            \int_0^1x\sin x\,dx
            =\left[-x\cos x+\sin x\right]_0^1
            =\sin1-\cos1.
            $$
            """
        ),
        ["images/source_pages/page-2.png"],
    ),
    Question(
        11,
        "fill_blank",
        4,
        "高等数学",
        ["一阶线性微分方程", "特解"],
        md(
            r"""
            以 $y=x^2-e^x$ 和 $y=x^2$ 为特解的一阶非齐次线性微分方程为 ________。
            """
        ),
        r"$y'-y=2x-x^2$",
        md(
            r"""
            两个特解之差为 $e^x$，它应满足对应齐次方程
            $$
            y'+p(x)y=0.
            $$
            代入 $y=e^x$ 得 $p(x)=-1$。故原方程可写成
            $$
            y'-y=q(x).
            $$
            再将特解 $y=x^2$ 代入，得
            $$
            2x-x^2=q(x).
            $$
            因而所求方程为 $y'-y=2x-x^2$。
            """
        ),
        ["images/source_pages/page-2.png"],
    ),
    Question(
        12,
        "fill_blank",
        4,
        "高等数学",
        ["高阶导数", "积分方程"],
        md(
            r"""
            已知函数 $f(x)$ 在 $(-\infty,+\infty)$ 上连续，且
            $$
            f(x)=(x+1)^2+2\int_0^x f(t)\,dt,
            $$
            则当 $n\ge2$ 时，
            $$
            f^{(n)}(0)=\underline{\qquad\qquad}.
            $$
            """
        ),
        r"$5\cdot 2^{n-1}$",
        md(
            r"""
            对原式求导得
            $$
            f'(x)=2(x+1)+2f(x).
            $$
            再求导得
            $$
            f''(x)=2+2f'(x),\qquad f^{(n)}(x)=2f^{(n-1)}(x)\ (n\ge3).
            $$
            又由原式知 $f(0)=1$，故
            $$
            f'(0)=2+2f(0)=4,\qquad f''(0)=2+2f'(0)=10.
            $$
            因而对 $n\ge2$，
            $$
            f^{(n)}(0)=2^{n-2}f''(0)=10\cdot2^{n-2}=5\cdot 2^{n-1}.
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
        ["相关变化率", "链式法则"],
        md(
            r"""
            已知动点 $P$ 在曲线 $y=x^3$ 上运动，记坐标原点与点 $P$ 间的距离为 $l$。若点 $P$ 的横坐标对时间的变化率为常数 $v_0$，则当点 $P$ 运动到点 $(1,1)$ 时，$l$ 对时间的变化率是 ________。
            """
        ),
        r"$2\sqrt{2}\,v_0$",
        md(
            r"""
            点 $P=(x,x^3)$，故
            $$
            l=\sqrt{x^2+x^6}.
            $$
            由链式法则，
            $$
            \frac{dl}{dt}=\frac{dl}{dx}\frac{dx}{dt}
            =\frac{6x^5+2x}{2\sqrt{x^2+x^6}}\,v_0.
            $$
            在 $x=1$ 处，
            $$
            \frac{dl}{dt}=\frac{8}{2\sqrt2}v_0=2\sqrt2\,v_0.
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
        ["矩阵等价", "矩阵秩"],
        md(
            r"""
            设矩阵
            $$
            \begin{pmatrix}
            a&-1&-1\\
            -1&a&-1\\
            -1&-1&a
            \end{pmatrix}
            $$
            与矩阵
            $$
            \begin{pmatrix}
            1&1&0\\
            0&-1&1\\
            1&0&1
            \end{pmatrix}
            $$
            等价，则 $a=\underline{\qquad}$。
            """
        ),
        "2",
        md(
            r"""
            矩阵等价当且仅当秩相同。右侧矩阵经初等变换可化为秩为 2 的矩阵，所以左侧矩阵也必须满足秩为 2。令
            $$
            A=\begin{pmatrix}
            a&-1&-1\\
            -1&a&-1\\
            -1&-1&a
            \end{pmatrix},
            $$
            则
            $$
            |A|=(a+1)^2(a-2).
            $$
            要使 $r(A)<3$，需 $a=-1$ 或 $a=2$。当 $a=-1$ 时，$r(A)=1$；当 $a=2$ 时，$r(A)=2$，与右侧矩阵秩相同。故 $a=2$。
            """
        ),
        ["images/source_pages/page-2.png"],
    ),
    Question(
        15,
        "solution",
        10,
        "高等数学",
        ["极限", "指数型极限", "Taylor展开"],
        md(
            r"""
            求极限
            $$
            \lim_{x\to0}(\cos2x+2x\sin x)^{1/x^4}.
            $$
            """
        ),
        r"$e^{1/3}$",
        md(
            r"""
            设原极限为 $I$。因底数趋于 1，可取对数：
            $$
            \ln I=\lim_{x\to0}\frac{\ln(\cos2x+2x\sin x)}{x^4}.
            $$
            先展开
            $$
            \cos2x=1-2x^2+\frac{2}{3}x^4+o(x^4),\qquad
            2x\sin x=2x^2-\frac13x^4+o(x^4),
            $$
            所以
            $$
            \cos2x+2x\sin x=1+\frac13x^4+o(x^4).
            $$
            于是
            $$
            \ln I=\lim_{x\to0}\frac{\frac13x^4+o(x^4)}{x^4}=\frac13,
            $$
            故
            $$
            I=e^{1/3}.
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
        ["定积分", "含绝对值函数", "最值"],
        md(
            r"""
            设函数
            $$
            f(x)=\int_0^1|t^2-x^2|\,dt\quad(x>0),
            $$
            求 $f'(x)$，并求 $f(x)$ 的最小值。
            """
        ),
        md(
            r"""
            $$
            f'(x)=
            \begin{cases}
            4x^2-2x, & 0<x<1,\\
            2, & x=1,\\
            2x, & x>1,
            \end{cases}
            \qquad
            f_{\min}=\frac14\ \text{(在 }x=\frac12\text{ 处取得)}.
            $$
            """
        ),
        md(
            r"""
            分情况去绝对值：
            当 $0<x<1$ 时，
            $$
            f(x)=\int_0^x(x^2-t^2)\,dt+\int_x^1(t^2-x^2)\,dt
            =\frac43x^3-x^2+\frac13,
            $$
            故
            $$
            f'(x)=4x^2-2x.
            $$
            当 $x\ge1$ 时，
            $$
            f(x)=\int_0^1(x^2-t^2)\,dt=x^2-\frac13,
            $$
            因而 $f'(x)=2x$（且 $f'(1)=2$）。
            对于 $0<x<1$，令 $f'(x)=0$ 得 $x=\frac12$。比较
            $f\!\left(\frac12\right)=\frac14$，以及 $x\ge1$ 时的函数值均不小于 $\frac23$，故最小值为 $\dfrac14$。
            """
        ),
        ["images/source_pages/page-2.png"],
    ),
    Question(
        17,
        "solution",
        10,
        "高等数学",
        ["隐函数", "多元函数极值"],
        md(
            r"""
            已知函数 $z=z(x,y)$ 由方程
            $$
            (x^2+y^2)z+\ln z+2(x+y+1)=0
            $$
            确定，求 $z=z(x,y)$ 的极值。
            """
        ),
        md(
            r"""
            $$
            z_{\max}=1 \quad\text{(在 }(-1,-1)\text{ 处取得)},
            $$
            无极小值。
            """
        ),
        md(
            r"""
            设
            $$
            F(x,y,z)=(x^2+y^2)z+\ln z+2(x+y+1)=0.
            $$
            由隐函数求导公式，在极值点应有 $z_x=z_y=0$。分别对 $x,y$ 求偏导并令 $z_x=z_y=0$，得
            $$
            2xz+2=0,\qquad 2yz+2=0,
            $$
            即
            $$
            x=y=-\frac1z.
            $$
            代回原方程得
            $$
            \frac{2}{z}+\ln z+2\left(-\frac2z+1\right)=0
            \Longrightarrow \ln z-\frac2z+2=0.
            $$
            易验得 $z=1$ 是解，从而 $x=y=-1$。再由二阶偏导计算可得在该点
            $$
            z_{xx}=z_{yy}=-\frac23,\qquad z_{xy}=0,
            $$
            Hessian 负定，所以此点为极大点，极大值为 1。方程不存在更小的局部极值点，故无极小值。
            """
        ),
        ["images/source_pages/page-2.png"],
    ),
    Question(
        18,
        "solution",
        10,
        "高等数学",
        ["二重积分", "极坐标"],
        md(
            r"""
            设 $D$ 是由直线 $y=1,\ y=x,\ y=-x$ 围成的有界区域，计算二重积分
            $$
            \iint_D \frac{x^2-xy-y^2}{x^2+y^2}\,dx\,dy.
            $$
            """
        ),
        r"$1-\dfrac{\pi}{2}$",
        md(
            r"""
            区域 $D$ 为顶角在原点、上边界为 $y=1$ 的等腰三角形。改用极坐标
            $$
            x=r\cos\theta,\qquad y=r\sin\theta,
            $$
            则
            $$
            \frac{x^2-xy-y^2}{x^2+y^2}
            =\cos^2\theta-\cos\theta\sin\theta-\sin^2\theta.
            $$
            区域对应
            $$
            \frac{\pi}{4}\le\theta\le\frac{3\pi}{4},\qquad 0\le r\le \frac1{\sin\theta}.
            $$
            因此
            $$
            \iint_D \frac{x^2-xy-y^2}{x^2+y^2}\,dx\,dy
            =\int_{\pi/4}^{3\pi/4}\int_0^{1/\sin\theta}
            (\cos^2\theta-\cos\theta\sin\theta-\sin^2\theta)\,r\,dr\,d\theta
            =1-\frac{\pi}{2}.
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
        ["二阶线性微分方程", "降阶法"],
        md(
            r"""
            已知
            $$
            y_1(x)=e^x,\qquad y_2(x)=u(x)e^x
            $$
            是二阶微分方程
            $$
            (2x-1)y''-(2x+1)y'+2y=0
            $$
            的两个解。若 $u(-1)=e,\ u(0)=-1$，求 $u(x)$，并写出该微分方程的通解。
            """
        ),
        md(
            r"""
            $$
            u(x)=-(2x+1)e^{-x},
            \qquad
            y=C_1e^x+C_2(2x+1).
            $$
            """
        ),
        md(
            r"""
            令 $y=u(x)e^x$ 代入原方程。利用已知解 $e^x$ 进行降阶，可化为关于 $v=u'$ 的一阶方程
            $$
            (2x-1)v'+(2x-3)v=0.
            $$
            解得
            $$
            v=u'=C(2x-1)e^{-x}.
            $$
            积分可得
            $$
            u(x)=A(-(2x+1)e^{-x})+B.
            $$
            代入条件 $u(-1)=e,\ u(0)=-1$，解得 $A=1,\ B=0$，故
            $$
            u(x)=-(2x+1)e^{-x}.
            $$
            于是
            $$
            y_2(x)=u(x)e^x=-(2x+1),
            $$
            与 $e^x$ 线性无关，所以通解为
            $$
            y=C_1e^x+C_2(2x+1).
            $$
            """
        ),
        ["images/source_pages/page-3.png"],
    ),
    Question(
        20,
        "solution",
        11,
        "高等数学",
        ["旋转体", "体积", "曲面面积"],
        md(
            r"""
            设 $D$ 是由曲线
            $$
            y=\sqrt{1-x^2}\quad (0\le x\le1)
            $$
            与
            $$
            \begin{cases}
            x=\cos^3 t,\\
            y=\sin^3 t,
            \end{cases}
            \quad 0\le t\le\frac{\pi}{2}
            $$
            围成的平面区域，求 $D$ 绕 $x$ 轴旋转一周所得旋转体的体积和表面积。
            """
        ),
        md(
            r"""
            $$
            V=\frac{18\pi}{35},\qquad S=\frac{16\pi}{5}.
            $$
            """
        ),
        md(
            r"""
            外边界为四分之一单位圆 $y=\sqrt{1-x^2}$，内边界为星形线第一象限弧
            $x^{2/3}+y^{2/3}=1$。体积由垫片法得
            $$
            V=\pi\int_0^1\left[(1-x^2)-\left(1-x^{2/3}\right)^3\right]dx
            =\frac{18\pi}{35}.
            $$
            表面积等于两条母线旋转所得面积之和。圆弧部分
            $$
            S_1=2\pi\int_0^1 y\sqrt{1+(y')^2}\,dx=2\pi.
            $$
            星形线用参数方程计算：
            $$
            x=\cos^3 t,\quad y=\sin^3 t,\quad
            ds=\sqrt{\left(\frac{dx}{dt}\right)^2+\left(\frac{dy}{dt}\right)^2}\,dt
            =3\sin t\cos t\,dt.
            $$
            故
            $$
            S_2=2\pi\int_0^{\pi/2} y\,ds
            =2\pi\int_0^{\pi/2}\sin^3 t\cdot 3\sin t\cos t\,dt
            =\frac{6\pi}{5}.
            $$
            因此
            $$
            S=S_1+S_2=2\pi+\frac{6\pi}{5}=\frac{16\pi}{5}.
            $$
            """
        ),
        ["images/source_pages/page-3.png"],
    ),
    Question(
        21,
        "solution",
        11,
        "高等数学",
        ["原函数", "平均值", "零点唯一性"],
        md(
            r"""
            已知函数 $f(x)$ 在 $\left[0,\dfrac{3\pi}{2}\right]$ 上连续，在 $\left(0,\dfrac{3\pi}{2}\right)$ 内是函数
            $$
            \frac{\cos x}{2x-3\pi}
            $$
            的一个原函数，且 $f(0)=0$。

            (I) 求 $f(x)$ 在区间 $\left[0,\dfrac{3\pi}{2}\right]$ 上的平均值；

            (II) 证明 $f(x)$ 在区间 $\left(0,\dfrac{3\pi}{2}\right)$ 内存在唯一零点。
            """
        ),
        md(
            r"""
            (I) 平均值为
            $$
            \frac{1}{3\pi}.
            $$
            (II) $f(x)$ 在 $\left(0,\dfrac{3\pi}{2}\right)$ 内恰有一个零点。
            """
        ),
        md(
            r"""
            设
            $$
            a=\frac{3\pi}{2}.
            $$
            由分部积分，
            $$
            \int_0^a f(x)\,dx=[xf(x)]_0^a-\int_0^a x f'(x)\,dx.
            $$
            又
            $$
            f'(x)=\frac{\cos x}{2x-3\pi},
            \qquad
            x=\frac12(2x-3\pi)+\frac{3\pi}{2},
            $$
            从而
            $$
            \int_0^a x f'(x)\,dx
            =\frac12\int_0^a \cos x\,dx+\frac{3\pi}{2}\int_0^a f'(x)\,dx
            =-\frac12+\frac{3\pi}{2}(f(a)-f(0)).
            $$
            代回后消去 $f(a)$，得
            $$
            \int_0^a f(x)\,dx=\frac12,
            $$
            所以平均值为
            $$
            \frac{1}{a}\cdot\frac12=\frac1{3\pi}.
            $$

            对于唯一性，注意到
            $$
            f'(x)=\frac{\cos x}{2x-3\pi}.
            $$
            在 $\left(0,\dfrac{\pi}{2}\right)$ 上，$\cos x>0$ 且分母 $<0$，故 $f'(x)<0$；在 $\left(\dfrac{\pi}{2},\dfrac{3\pi}{2}\right)$ 上，$\cos x<0$ 且分母仍 $<0$，故 $f'(x)>0$。因此 $f$ 先减后增。
            又 $f(0)=0$，且平均值为正，所以函数在后半段必须升回到正值，因而至少有一个零点。由于其单调性仅改变一次，故零点只能有一个，遂知在 $\left(0,\dfrac{3\pi}{2}\right)$ 内恰有一个零点。
            """
        ),
        ["images/source_pages/page-4.png"],
    ),
    Question(
        22,
        "solution",
        11,
        "线性代数",
        ["线性方程组", "无解条件", "法方程"],
        md(
            r"""
            设矩阵
            $$
            A=
            \begin{pmatrix}
            1&1&1-a\\
            1&0&a\\
            a+1&1&a+1
            \end{pmatrix},
            \qquad
            \beta=
            \begin{pmatrix}
            0\\
            1\\
            2a-2
            \end{pmatrix},
            $$
            且方程组 $Ax=\beta$ 无解。

            (I) 求 $a$ 的值；

            (II) 求方程组 $A^{\mathsf T}Ax=A^{\mathsf T}\beta$ 的通解。
            """
        ),
        md(
            r"""
            (I) $a=0$；

            (II)
            $$
            x=
            \begin{pmatrix}
            1\\
            -2\\
            0
            \end{pmatrix}
            +t
            \begin{pmatrix}
            0\\
            -1\\
            1
            \end{pmatrix},
            \qquad t\in\mathbb{R}.
            $$
            """
        ),
        md(
            r"""
            要使 $Ax=\beta$ 无解，必须有
            $$
            r(A)<r(A,\beta).
            $$
            先算
            $$
            \det A=a(a-2).
            $$
            当 $a=2$ 时，直接验算增广矩阵秩仍为 2，方程有解；当 $a=0$ 时，$r(A)=2,\ r(A,\beta)=3$，故恰无解，因此 $a=0$。

            取 $a=0$ 后，
            $$
            A=
            \begin{pmatrix}
            1&1&1\\
            1&0&0\\
            1&1&1
            \end{pmatrix},
            \qquad
            \beta=
            \begin{pmatrix}
            0\\
            1\\
            -2
            \end{pmatrix}.
            $$
            法方程
            $A^{\mathsf T}Ax=A^{\mathsf T}\beta$
            的解集等于最小二乘解集。求解可得一个特解
            $$
            x_0=\begin{pmatrix}1\\-2\\0\end{pmatrix},
            $$
            齐次方程 $Ax=0$ 的基础解系可取
            $$
            \begin{pmatrix}0\\-1\\1\end{pmatrix}.
            $$
            因此通解为
            $$
            x=x_0+t\begin{pmatrix}0\\-1\\1\end{pmatrix},\quad t\in\mathbb R.
            $$
            """
        ),
        ["images/source_pages/page-4.png"],
    ),
    Question(
        23,
        "solution",
        11,
        "线性代数",
        ["矩阵幂", "矩阵递推", "列向量表示"],
        md(
            r"""
            已知矩阵
            $$
            A=
            \begin{pmatrix}
            0&-1&1\\
            2&-3&0\\
            0&0&0
            \end{pmatrix}.
            $$

            (I) 求 $A^{99}$；

            (II) 设 3 阶矩阵 $B=(\alpha_1,\alpha_2,\alpha_3)$ 满足 $B^2=BA$。记
            $$
            B^{100}=(\beta_1,\beta_2,\beta_3),
            $$
            将 $\beta_1,\beta_2,\beta_3$ 分别表示为 $\alpha_1,\alpha_2,\alpha_3$ 的线性组合。
            """
        ),
        md(
            r"""
            $$
            A^{99}=
            \begin{pmatrix}
            2^{99}-2 & -(2^{99}-1) & -(2^{98}-2)\\
            2^{100}-2 & -(2^{100}-1) & -(2^{99}-2)\\
            0&0&0
            \end{pmatrix}.
            $$

            因而
            $$
            \beta_1=(2^{99}-2)\alpha_1+(2^{100}-2)\alpha_2,
            $$
            $$
            \beta_2=-(2^{99}-1)\alpha_1-(2^{100}-1)\alpha_2,
            $$
            $$
            \beta_3=-(2^{98}-2)\alpha_1-(2^{99}-2)\alpha_2.
            $$
            """
        ),
        md(
            r"""
            由直接乘法可归纳得到
            $$
            A^n=
            \begin{pmatrix}
            (-1)^{n-1}(2^n-2) & (-1)^n(2^n-1) & (-1)^n(2^{n-1}-2)\\
            (-1)^{n-1}(2^{n+1}-2) & (-1)^n(2^{n+1}-1) & (-1)^n(2^n-2)\\
            0&0&0
            \end{pmatrix}\quad(n\ge1).
            $$
            取 $n=99$ 即得
            $$
            A^{99}=
            \begin{pmatrix}
            2^{99}-2 & -(2^{99}-1) & -(2^{98}-2)\\
            2^{100}-2 & -(2^{100}-1) & -(2^{99}-2)\\
            0&0&0
            \end{pmatrix}.
            $$

            又由 $B^2=BA$，可归纳得
            $$
            B^n=BA^{n-1}\qquad(n\ge2).
            $$
            因此
            $$
            B^{100}=BA^{99}.
            $$
            因 $B=(\alpha_1,\alpha_2,\alpha_3)$，右乘矩阵时各列恰对应 $\alpha_1,\alpha_2,\alpha_3$ 的线性组合，所以 $B^{100}$ 的三列正是 $A^{99}$ 三列作为系数得到的组合。第三行全为 0，故三列都不含 $\alpha_3$ 项，结果如上。
            """
        ),
        ["images/source_pages/page-4.png"],
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
        "整理状态：按原卷页图转写并与答案册交叉核对。",
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
    return "\n".join(lines).rstrip() + "\n"


def annual_answers_md(questions: list[Question]) -> str:
    lines = [
        f"# {YEAR} 年数学二答案解析",
        "",
        "资料类型：考研数学二答案解析",
        f"年份：{YEAR}",
        "科目：数学二",
        "整理状态：结合答案册页图与本地复算整理为精炼版解析。",
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
        lines.extend(
            [
                f"### 第 {q.number} 题",
                "",
                f"- 标准答案：{q.answer}",
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
