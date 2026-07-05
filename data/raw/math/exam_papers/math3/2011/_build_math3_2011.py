from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[6]
EXAM_ROOT = ROOT / "data" / "raw" / "math" / "exam_papers"
YEAR = 2011
YEAR_DIR = EXAM_ROOT / "math3" / str(YEAR)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def qtype_label(qtype: str) -> str:
    return {
        "fill_blank": "填空题",
        "single_choice": "选择题",
        "solution": "解答题",
    }[qtype]


def answer_for_table(answer: str) -> str:
    brief = " ".join(answer.replace("\n", " ").split())
    if len(brief) > 56 or "\\begin{" in brief:
        return "见详细解析"
    return brief


def question_id(number: int) -> str:
    return f"kaoyan_math3_{YEAR}_q{number:03d}"


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
        ["等价无穷小", "极限", "三角函数"],
        "34",
        r"""
已知当 $x\to0$ 时，函数
$$
f(x)=3\sin x-\sin 3x
$$
与 $cx^k$ 是等价无穷小，则（ ）  

A. $k=1,\ c=4$  
B. $k=1,\ c=-4$  
C. $k=3,\ c=4$  
D. $k=3,\ c=-4$
""",
        r"C",
        r"""
利用恒等变形
$$
3\sin x-\sin 3x
=3\sin x-\sin x\cos 2x-\cos x\sin 2x
=\sin x\bigl(3-\cos 2x-2\cos^2x\bigr).
$$
再用 $\cos 2x=2\cos^2x-1$，得
$$
3-\cos 2x-2\cos^2x=4-4\cos^2x=4\sin^2x.
$$
因此
$$
3\sin x-\sin 3x\sim 4x^3 \quad (x\to0).
$$
故 $k=3,\ c=4$，选 C。
""",
    ),
    q(
        2,
        "single_choice",
        4,
        "高等数学",
        ["导数定义", "复合极限"],
        "34",
        r"""
设函数 $f(x)$ 在 $x=0$ 处可导，且 $f(0)=0$，则
$$
\lim_{x\to0}\frac{x^2f(x)-2f(x^3)}{x^3}=(\ )
$$

A. $-2f'(0)$  
B. $-f'(0)$  
C. $f'(0)$  
D. $0$
""",
        r"B",
        r"""
因为 $f(0)=0$，
$$
\frac{x^2f(x)-2f(x^3)}{x^3}
=\frac{f(x)-f(0)}{x}-2\cdot\frac{f(x^3)-f(0)}{x^3}.
$$
当 $x\to0$ 时，第一项趋于 $f'(0)$，第二项也趋于 $2f'(0)$，故极限为
$$
f'(0)-2f'(0)=-f'(0).
$$
选 B。
""",
    ),
    q(
        3,
        "single_choice",
        4,
        "高等数学",
        ["无穷级数", "命题判断"],
        "34",
        r"""
设 $\{u_n\}$ 是数列，则下列命题正确的是（ ）

A. 若 $\sum_{n=1}^{\infty}u_n$ 收敛，则 $\sum_{n=1}^{\infty}(u_{2n-1}+u_{2n})$ 收敛。  
B. 若 $\sum_{n=1}^{\infty}(u_{2n-1}+u_{2n})$ 收敛，则 $\sum_{n=1}^{\infty}u_n$ 收敛。  
C. 若 $\sum_{n=1}^{\infty}u_n$ 收敛，则 $\sum_{n=1}^{\infty}(u_{2n-1}-u_{2n})$ 收敛。  
D. 若 $\sum_{n=1}^{\infty}(u_{2n-1}-u_{2n})$ 收敛，则 $\sum_{n=1}^{\infty}u_n$ 收敛。
""",
        r"A",
        r"""
收敛级数任意加括号后仍收敛，因此 A 正确。

B 错：取 $u_n=(-1)^n$，则
$$
u_{2n-1}+u_{2n}=0,
$$
故分组后的级数收敛，但原级数 $\sum (-1)^n$ 发散。

C 错：取 $u_n=\dfrac{(-1)^{n-1}}{n}$，则 $\sum u_n$ 收敛，但
$$
\sum_{n=1}^{\infty}(u_{2n-1}-u_{2n})
=\sum_{n=1}^{\infty}\frac1n
$$
发散。

D 错：取 $u_n=1$，则 $\sum(u_{2n-1}-u_{2n})=0$ 收敛，而 $\sum u_n$ 发散。
""",
    ),
    q(
        4,
        "single_choice",
        4,
        "高等数学",
        ["定积分", "对数函数", "大小比较"],
        "34",
        r"""
设
$$
I=\int_0^{\pi/4}\ln(\sin x)\,dx,\quad
J=\int_0^{\pi/4}\ln(\cot x)\,dx,\quad
K=\int_0^{\pi/4}\ln(\cos x)\,dx,
$$
则 $I,J,K$ 的大小关系为（ ）

A. $I<J<K$  
B. $I<K<J$  
C. $J<I<K$  
D. $K<J<I$
""",
        r"B",
        r"""
当 $0<x<\dfrac{\pi}{4}$ 时，
$$
0<\sin x<\cos x<1<\cot x.
$$
由于 $\ln x$ 单调递增，所以
$$
\ln(\sin x)<\ln(\cos x)<\ln(\cot x).
$$
在同一区间上积分后得到
$$
I<K<J.
$$
故选 B。
""",
    ),
    q(
        5,
        "single_choice",
        4,
        "线性代数",
        ["矩阵初等变换", "逆矩阵"],
        "34",
        r"""
设 $A$ 为 3 阶矩阵，将 $A$ 的第 2 列加到第 1 列得矩阵 $B$，再交换 $B$ 的第 2 行与第 3 行得单位矩阵. 记
$$
P_1=
\begin{pmatrix}
1&0&0\\
1&1&0\\
0&0&1
\end{pmatrix},
\qquad
P_2=
\begin{pmatrix}
1&0&0\\
0&0&1\\
0&1&0
\end{pmatrix},
$$
则 $A=(\ )$

A. $P_1P_2$  
B. $P_1^{-1}P_2$  
C. $P_2P_1$  
D. $P_2P_1^{-1}$
""",
        r"D",
        r"""
将第 2 列加到第 1 列可写成
$$
AP_1=B,
$$
所以
$$
A=BP_1^{-1}.
$$
又由交换 $B$ 的第 2、3 行得到单位矩阵，可写成
$$
P_2B=E,
$$
即
$$
B=P_2^{-1}=P_2.
$$
故
$$
A=P_2P_1^{-1}.
$$
选 D。
""",
    ),
    q(
        6,
        "single_choice",
        4,
        "线性代数",
        ["线性方程组", "基础解系", "通解结构"],
        "34",
        r"""
设 $A$ 为 $4\times3$ 矩阵，$\eta_1,\eta_2,\eta_3$ 是非齐次线性方程组 $Ax=\beta$ 的 3 个线性无关的解，$k_1,k_2$ 为任意常数，则 $Ax=\beta$ 的通解为（ ）

A. $\dfrac{\eta_2+\eta_3}{2}+k_1(\eta_2-\eta_1)$  
B. $\dfrac{\eta_2-\eta_3}{2}+k_1(\eta_2-\eta_1)$  
C. $\dfrac{\eta_2+\eta_3}{2}+k_1(\eta_2-\eta_1)+k_2(\eta_3-\eta_1)$  
D. $\dfrac{\eta_2-\eta_3}{2}+k_1(\eta_2-\eta_1)+k_2(\eta_3-\eta_1)$
""",
        r"C",
        r"""
因为 $\eta_1,\eta_2,\eta_3$ 都是 $Ax=\beta$ 的解，所以
$$
\eta_2-\eta_1,\ \eta_3-\eta_1
$$
都是齐次方程 $Ax=0$ 的解，并且线性无关。故它们构成 $Ax=0$ 的一个基础解系。

又因为
$$
A\left(\frac{\eta_2+\eta_3}{2}\right)=\frac{\beta+\beta}{2}=\beta,
$$
所以 $\dfrac{\eta_2+\eta_3}{2}$ 是一个特解。

因此非齐次方程组的通解为
$$
\frac{\eta_2+\eta_3}{2}+k_1(\eta_2-\eta_1)+k_2(\eta_3-\eta_1).
$$
选 C。
""",
    ),
    q(
        7,
        "single_choice",
        4,
        "概率统计",
        ["分布函数", "概率密度"],
        "34",
        r"""
设 $F_1(x)$ 与 $F_2(x)$ 为两个分布函数，其相应的概率密度 $f_1(x)$ 与 $f_2(x)$ 是连续函数，则必为概率密度的是（ ）

A. $f_1(x)f_2(x)$  
B. $2f_2(x)F_1(x)$  
C. $f_1(x)F_2(x)$  
D. $f_1(x)F_2(x)+f_2(x)F_1(x)$
""",
        r"D",
        r"""
对选项 D，有
$$
\int_{-\infty}^{+\infty}\bigl[f_1(x)F_2(x)+f_2(x)F_1(x)\bigr]\,dx
=\int_{-\infty}^{+\infty}d\bigl(F_1(x)F_2(x)\bigr)=1.
$$
且该函数非负，因此它是概率密度。
故选 D。
""",
    ),
    q(
        8,
        "single_choice",
        4,
        "概率统计",
        ["泊松分布", "数学期望", "方差"],
        "35",
        r"""
设总体 $X$ 服从参数为 $\lambda\ (\lambda>0)$ 的泊松分布，$X_1,X_2,\cdots,X_n\ (n\ge2)$ 为来自该总体的简单随机样本，则对于统计量
$$
T_1=\frac1n\sum_{i=1}^{n}X_i,
\qquad
T_2=\frac1{n-1}\sum_{i=1}^{n-1}X_i+\frac1nX_n,
$$
有（ ）

A. $E(T_1)>E(T_2),\ D(T_1)>D(T_2)$  
B. $E(T_1)>E(T_2),\ D(T_1)<D(T_2)$  
C. $E(T_1)<E(T_2),\ D(T_1)>D(T_2)$  
D. $E(T_1)<E(T_2),\ D(T_1)<D(T_2)$
""",
        r"D",
        r"""
因为 $X_i\sim P(\lambda)$，故
$$
E(X_i)=\lambda,\qquad D(X_i)=\lambda.
$$
于是
$$
E(T_1)=\lambda,
\qquad
E(T_2)=\frac1{n-1}(n-1)\lambda+\frac1n\lambda
=\left(1+\frac1n\right)\lambda,
$$
所以 $E(T_1)<E(T_2)$。

又
$$
D(T_1)=\frac1{n^2}\cdot n\lambda=\frac{\lambda}{n},
$$
$$
D(T_2)=\frac1{(n-1)^2}\cdot(n-1)\lambda+\frac1{n^2}\lambda
=\left(\frac1{n-1}+\frac1{n^2}\right)\lambda.
$$
当 $n\ge2$ 时，
$$
\frac1n<\frac1{n-1}+\frac1{n^2},
$$
故 $D(T_1)<D(T_2)$。选 D。
""",
    ),
    q(
        9,
        "fill_blank",
        4,
        "高等数学",
        ["导数", "指数函数", "极限定义"],
        "35",
        r"""
设
$$
f(x)=\lim_{t\to0}x(1+3t)^{x/t},
$$
则 $f'(x)=\underline{\qquad}$.
""",
        r"$e^{3x}(1+3x)$",
        r"""
由
$$
\lim_{t\to0}(1+3t)^{1/(3t)}=e
$$
可得
$$
f(x)=x\lim_{t\to0}\left[(1+3t)^{1/(3t)}\right]^{3x}=xe^{3x}.
$$
故
$$
f'(x)=e^{3x}+3xe^{3x}=e^{3x}(1+3x).
$$
""",
    ),
    q(
        10,
        "fill_blank",
        4,
        "高等数学",
        ["全微分", "偏导数", "对数求导"],
        "35",
        r"""
设函数
$$
z=\left(1+\frac{x}{y}\right)^{x/y},
$$
则
$$
dz\big|_{(1,1)}=\underline{\qquad}.
$$
""",
        r"$(1+2\ln2)(dx-dy)$",
        r"""
写成
$$
z=\exp\!\left[\frac{x}{y}\ln\!\left(1+\frac{x}{y}\right)\right].
$$
计算偏导并代入 $(1,1)$，得
$$
\left.\frac{\partial z}{\partial x}\right|_{(1,1)}=1+2\ln2,
\qquad
\left.\frac{\partial z}{\partial y}\right|_{(1,1)}=-1-2\ln2.
$$
因此
$$
dz\big|_{(1,1)}=(1+2\ln2)\,dx-(1+2\ln2)\,dy=(1+2\ln2)(dx-dy).
$$
""",
    ),
    q(
        11,
        "fill_blank",
        4,
        "高等数学",
        ["隐函数求导", "切线方程"],
        "35",
        r"""
曲线
$$
\tan\left(x+y+\frac{\pi}{4}\right)=e^y
$$
在点 $(0,0)$ 处的切线方程为 $\underline{\qquad}$.
""",
        r"$y=-2x$",
        r"""
对方程两端对 $x$ 求导：
$$
\sec^2\left(x+y+\frac{\pi}{4}\right)(1+y')=e^y y'.
$$
代入 $(x,y)=(0,0)$，有
$$
\frac{1+y'}{\cos^2(\pi/4)}=y',
$$
即
$$
2(1+y')=y',
$$
解得 $y'=-2$。故切线方程为
$$
y=-2x.
$$
""",
    ),
    q(
        12,
        "fill_blank",
        4,
        "高等数学",
        ["旋转体体积", "定积分"],
        "35",
        r"""
曲线 $y=\sqrt{x^2-1}$、直线 $x=2$ 及 $x$ 轴所围的平面图形绕 $x$ 轴旋转所成的旋转体的体积为 $\underline{\qquad}$.
""",
        r"$\dfrac{4\pi}{3}$",
        r"""
由几何关系可知积分区间为 $x\in[1,2]$，旋转体体积
$$
V=\pi\int_1^2 y^2\,dx
=\pi\int_1^2(x^2-1)\,dx
=\pi\left[\frac{x^3}{3}-x\right]_1^2
=\frac{4\pi}{3}.
$$
""",
    ),
    q(
        13,
        "fill_blank",
        4,
        "线性代数",
        ["二次型", "特征值", "标准形"],
        "35",
        r"""
设二次型
$$
f(x_1,x_2,x_3)=x^TAx
$$
的秩为 1，$A$ 的各行元素之和为 3，则 $f$ 在正交变换 $x=Qy$ 下的标准形为 $\underline{\qquad}$.
""",
        r"$3y_1^2$",
        r"""
由 $A$ 的各行元素之和都等于 3，知
$$
A
\begin{pmatrix}
1\\1\\1
\end{pmatrix}
=3
\begin{pmatrix}
1\\1\\1
\end{pmatrix},
$$
因此 3 是 $A$ 的一个特征值。

又因 $r(A)=1$，所以其余特征值都为 0。正交变换下二次型的标准形系数就是特征值，故标准形为
$$
3y_1^2.
$$
""",
    ),
    q(
        14,
        "fill_blank",
        4,
        "概率统计",
        ["二维正态分布", "独立性", "期望"],
        "35",
        r"""
设二维随机变量 $(X,Y)$ 服从正态分布
$$
N(\mu,\mu;\sigma^2,\sigma^2;0),
$$
则
$$
E(XY^2)=\underline{\qquad}.
$$
""",
        r"$\mu(\mu^2+\sigma^2)$",
        r"""
相关系数为 0，因此在二维正态分布下 $X,Y$ 相互独立。于是
$$
E(XY^2)=E(X)E(Y^2).
$$
又
$$
E(X)=\mu,\qquad E(Y^2)=D(Y)+[E(Y)]^2=\sigma^2+\mu^2.
$$
故
$$
E(XY^2)=\mu(\mu^2+\sigma^2).
$$
""",
    ),
    q(
        15,
        "solution",
        10,
        "高等数学",
        ["极限", "洛必达法则"],
        "35-36",
        r"""
求极限
$$
\lim_{x\to0}\frac{\sqrt{1+2\sin x}-x-1}{x\ln(1+x)}.
$$
""",
        r"$-\dfrac12$",
        r"""
由于
$$
x\ln(1+x)\sim x^2 \quad (x\to0),
$$
原极限可化为
$$
\lim_{x\to0}\frac{\sqrt{1+2\sin x}-x-1}{x^2}.
$$
分子分母同趋于 0，连续使用洛必达法则：
$$
\lim_{x\to0}\frac{\dfrac{\cos x}{\sqrt{1+2\sin x}}-1}{2x}
=\lim_{x\to0}\frac{-\sin x-\dfrac{\cos^2x}{\sqrt{1+2\sin x}}}{2\sqrt{1+2\sin x}}
=-\frac12.
$$
故所求极限为
$$
-\frac12.
$$
""",
    ),
    q(
        16,
        "solution",
        10,
        "高等数学",
        ["复合函数求导", "二阶偏导数"],
        "35",
        r"""
已知函数 $f(u,v)$ 具有二阶连续偏导数，$f(1,1)=2$ 是 $f(u,v)$ 的极值，$z=f(x+y,f(x,y))$。求
$$
\left.\frac{\partial^2 z}{\partial x\,\partial y}\right|_{(1,1)}.
$$
""",
        r"$f_{11}''(2,2)+f_2'(2,2)\,f_{12}''(1,1)$",
        r"""
设
$$
u=x+y,\qquad v=f(x,y),
$$
则
$$
z=f(u,v).
$$
先对 $x$ 求偏导：
$$
\frac{\partial z}{\partial x}=f_1'(u,v)\frac{\partial u}{\partial x}+f_2'(u,v)\frac{\partial v}{\partial x}
=f_1'(u,v)+f_2'(u,v)f_x'(x,y).
$$
再对 $y$ 求偏导，并在 $(1,1)$ 处代入。由于 $f(1,1)=2$ 是极值点，所以
$$
f_1'(1,1)=f_2'(1,1)=0.
$$
于是化简得
$$
\left.\frac{\partial^2 z}{\partial x\,\partial y}\right|_{(1,1)}
=f_{11}''(2,2)+f_2'(2,2)\,f_{12}''(1,1).
$$
""",
    ),
    q(
        17,
        "solution",
        10,
        "高等数学",
        ["不定积分", "换元积分"],
        "36",
        r"""
求不定积分
$$
\int \frac{\arcsin\sqrt{x}+\ln x}{\sqrt{x}}\,dx.
$$
""",
        r"$2\sqrt{x}\arcsin\sqrt{x}+2\sqrt{x}\ln x+2\sqrt{1-x}-4\sqrt{x}+C$",
        r"""
令
$$
t=\sqrt{x},
$$
则 $x=t^2,\ dx=2t\,dt$，原积分化为
$$
2\int(\arcsin t+\ln t^2)\,dt.
$$
分别积分：
$$
2\int \arcsin t\,dt
=2\left(t\arcsin t+\sqrt{1-t^2}\right),
$$
$$
2\int \ln t^2\,dt
=4\int \ln t\,dt
=4(t\ln t-t).
$$
合并并代回 $t=\sqrt{x}$，得
$$
2\sqrt{x}\arcsin\sqrt{x}+2\sqrt{x}\ln x+2\sqrt{1-x}-4\sqrt{x}+C.
$$
""",
    ),
    q(
        18,
        "solution",
        10,
        "高等数学",
        ["函数零点", "单调性", "导数应用"],
        "36",
        r"""
证明方程
$$
4\arctan x-x+\frac{4\pi}{3}-\sqrt{3}=0
$$
恰有两个实根。
""",
        r"方程恰有两个实根",
        r"""
设
$$
f(x)=4\arctan x-x+\frac{4\pi}{3}-\sqrt{3}.
$$
则
$$
f'(x)=\frac{4}{1+x^2}-1=\frac{(\sqrt3-x)(\sqrt3+x)}{1+x^2}.
$$
所以：
$$
f'(x)<0\ (x<-\sqrt3),\quad
f'(x)>0\ (-\sqrt3<x<\sqrt3),\quad
f'(x)<0\ (x>\sqrt3).
$$
故 $f$ 先减后增再减。

又
$$
f(-\sqrt3)=0,
$$
并且
$$
f(\sqrt3)=\frac{8\pi}{3}-2\sqrt3>0,\qquad
\lim_{x\to+\infty}f(x)=-\infty.
$$
因此在 $(-\infty,\sqrt3)$ 上只有一个零点 $x=-\sqrt3$，在 $(\sqrt3,+\infty)$ 上还有且仅有一个零点。
故原方程恰有两个实根。
""",
    ),
    q(
        19,
        "solution",
        10,
        "高等数学",
        ["积分方程", "微分方程"],
        "36",
        r"""
设函数 $f(x)$ 在区间 $[0,1]$ 上具有连续导数，$f(0)=1$，且满足
$$
\iint_{D_t}f'(x+y)\,dxdy=\iint_{D_t}f(t)\,dxdy,
$$
其中
$$
D_t=\{(x,y)\mid 0\le y\le t-x,\ 0\le x\le t\}\quad (0<t\le1).
$$
求 $f(x)$ 的表达式。
""",
        r"$f(x)=\dfrac{4}{(x-2)^2}\ (0\le x\le1)$",
        r"""
先计算右端：
$$
\iint_{D_t}f(t)\,dxdy=\frac12 t^2f(t).
$$
左端有
$$
\iint_{D_t}f'(x+y)\,dxdy
=\int_0^t\int_0^{t-x}f'(x+y)\,dy\,dx
=\int_0^t\bigl(f(t)-f(x)\bigr)\,dx
=tf(t)-\int_0^t f(x)\,dx.
$$
因此
$$
tf(t)-\int_0^t f(x)\,dx=\frac12 t^2f(t).
$$
两边对 $t$ 求导，整理得
$$
(2-t)f'(t)=2f(t).
$$
这是可分离变量方程，解得
$$
f(t)=\frac{C}{(t-2)^2}.
$$
由 $f(0)=1$ 得 $C=4$。故
$$
f(x)=\frac{4}{(x-2)^2},\qquad 0\le x\le1.
$$
""",
    ),
    q(
        20,
        "solution",
        11,
        "线性代数",
        ["向量组", "线性表示", "秩"],
        "36",
        r"""
设向量组
$$
\alpha_1=(1,0,1)^T,\quad
\alpha_2=(0,1,1)^T,\quad
\alpha_3=(1,3,5)^T
$$
不能由向量组
$$
\beta_1=(1,1,1)^T,\quad
\beta_2=(1,2,3)^T,\quad
\beta_3=(3,4,a)^T
$$
线性表示。

1. 求 $a$ 的值；  
2. 将 $\beta_1,\beta_2,\beta_3$ 用 $\alpha_1,\alpha_2,\alpha_3$ 线性表示。
""",
        r"""
(I)\ $a=5$；

(II)\ 
$$
\beta_1=2\alpha_1+4\alpha_2-\alpha_3,\quad
\beta_2=\alpha_1+2\alpha_2,\quad
\beta_3=5\alpha_1+10\alpha_2-2\alpha_3.
$$
""",
        r"""
把两组向量并排写成矩阵并做行变换。由“$\alpha_1,\alpha_2,\alpha_3$ 不能由 $\beta_1,\beta_2,\beta_3$ 线性表示”知，把 $\alpha$ 组并入 $\beta$ 组后秩会增加。

对
$$
(\beta_1,\beta_2,\beta_3,\alpha_1,\alpha_2,\alpha_3)
$$
作初等行变换，可化到含有主元 $a-5$ 的形式，因此只有当
$$
a=5
$$
时，$\alpha$ 组不能由 $\beta$ 组线性表示。

再对
$$
(\alpha_1,\alpha_2,\alpha_3,\beta_1,\beta_2,\beta_3)
$$
作行变换，可读出表示系数：
$$
\beta_1=2\alpha_1+4\alpha_2-\alpha_3,
$$
$$
\beta_2=\alpha_1+2\alpha_2,
$$
$$
\beta_3=5\alpha_1+10\alpha_2-2\alpha_3.
$$
""",
    ),
    q(
        21,
        "solution",
        11,
        "线性代数",
        ["实对称矩阵", "特征值", "正交对角化"],
        "37",
        r"""
设 $A$ 为 3 阶实对称矩阵，$A$ 的秩为 2，且
$$
A
\begin{pmatrix}
1&1\\
0&0\\
-1&1
\end{pmatrix}
=
\begin{pmatrix}
-1&1\\
0&0\\
1&1
\end{pmatrix}.
$$

1. 求 $A$ 的所有特征值与特征向量；  
2. 求矩阵 $A$。
""",
        r"""
特征值为 $-1,1,0$；

对应特征向量可取
$$
(1,0,-1)^T,\ (1,0,1)^T,\ (0,1,0)^T.
$$

并且
$$
A=
\begin{pmatrix}
0&0&1\\
0&0&0\\
1&0&0
\end{pmatrix}.
$$
""",
        r"""
由题设可知
$$
A(1,0,-1)^T=-(1,0,-1)^T,\qquad
A(1,0,1)^T=(1,0,1)^T.
$$
因此 $-1,1$ 是 $A$ 的两个特征值，对应特征向量分别可取
$$
\alpha_1=(1,0,-1)^T,\qquad \alpha_2=(1,0,1)^T.
$$

又因 $r(A)=2$，故第三个特征值为 0。由于 $A$ 是实对称矩阵，不同特征值的特征向量两两正交，所以对应 0 的特征向量可取
$$
\alpha_3=(0,1,0)^T.
$$

单位化后取
$$
\beta_1=\frac1{\sqrt2}(1,0,-1)^T,\quad
\beta_2=\frac1{\sqrt2}(1,0,1)^T,\quad
\beta_3=(0,1,0)^T.
$$
令
$$
Q=(\beta_1,\beta_2,\beta_3),
\qquad
\Lambda=\operatorname{diag}(-1,1,0),
$$
则
$$
A=Q\Lambda Q^T
=
\begin{pmatrix}
0&0&1\\
0&0&0\\
1&0&0
\end{pmatrix}.
$$
""",
    ),
    q(
        22,
        "solution",
        11,
        "概率统计",
        ["联合分布", "随机变量函数分布", "相关系数"],
        "37",
        r"""
设随机变量 $X$ 与 $Y$ 的概率分布分别为

$$
\begin{array}{c|cc}
X & 0 & 1\\ \hline
P & \frac13 & \frac23
\end{array}
\qquad
\begin{array}{c|ccc}
Y & -1 & 0 & 1\\ \hline
P & \frac13 & \frac13 & \frac13
\end{array}
$$

且 $P\{X^2=Y^2\}=1$。

1. 求二维随机变量 $(X,Y)$ 的概率分布；  
2. 求 $Z=XY$ 的概率分布；  
3. 求 $X$ 与 $Y$ 的相关系数 $\rho_{XY}$。
""",
        r"""
$$
\begin{array}{c|ccc}
 & -1 & 0 & 1\\ \hline
X=0 & 0 & \frac13 & 0\\
X=1 & \frac13 & 0 & \frac13
\end{array}
$$

$$
P(Z=-1)=\frac13,\quad P(Z=0)=\frac13,\quad P(Z=1)=\frac13.
$$

$$
\rho_{XY}=0.
$$
""",
        r"""
由
$$
P\{X^2=Y^2\}=1
$$
可知不可能出现
$$
(X,Y)=(0,-1),(0,1),(1,0),
$$
这些情形的概率都为 0。

再由边缘分布得
$$
P(X=0,Y=0)=P(X=0)=\frac13,
$$
$$
P(X=1,Y=-1)=P(Y=-1)=\frac13,
$$
$$
P(X=1,Y=1)=P(Y=1)=\frac13.
$$
因此联合分布如答案所示。

因为 $Z=XY$，故其可能值为 $-1,0,1$，且三者概率都为 $\dfrac13$。

又
$$
E(XY)=(-1)\cdot\frac13+0\cdot\frac13+1\cdot\frac13=0,
$$
$$
E(Y)=(-1)\cdot\frac13+0\cdot\frac13+1\cdot\frac13=0.
$$
所以
$$
\operatorname{Cov}(X,Y)=E(XY)-E(X)E(Y)=0,
$$
从而
$$
\rho_{XY}=0.
$$
""",
    ),
    q(
        23,
        "solution",
        11,
        "概率统计",
        ["二维连续型分布", "边缘密度", "条件密度"],
        "37",
        r"""
设二维随机变量 $(X,Y)$ 服从区域 $G$ 上的均匀分布，其中 $G$ 是由 $x-y=0,\ x+y=2$ 与 $y=0$ 所围成的三角形区域。

1. 求 $X$ 的概率密度 $f_X(x)$；  
2. 求条件概率密度 $f_{X\mid Y}(x\mid y)$。
""",
        r"""
$$
f_X(x)=
\begin{cases}
x, & 0<x<1,\\
2-x, & 1\le x<2,\\
0, & \text{其他}.
\end{cases}
$$

$$
f_{X\mid Y}(x\mid y)=
\begin{cases}
\dfrac1{2-2y}, & y<x<2-y,\ 0<y<1,\\
0, & \text{其他}.
\end{cases}
$$
""",
        r"""
三角形区域
$$
G=\{(x,y)\mid 0<y<1,\ y<x<2-y\}
$$
面积为 1，因此联合密度为
$$
f(x,y)=
\begin{cases}
1, & 0<y<1,\ y<x<2-y,\\
0, & \text{其他}.
\end{cases}
$$

对 $y$ 积分可得边缘密度：
当 $0<x<1$ 时，$0<y<x$，所以
$$
f_X(x)=\int_0^x1\,dy=x.
$$
当 $1\le x<2$ 时，$0<y<2-x$，所以
$$
f_X(x)=\int_0^{2-x}1\,dy=2-x.
$$
其余情形为 0。

再求 $Y$ 的边缘密度：
$$
f_Y(y)=\int_y^{2-y}1\,dx=2-2y,\qquad 0<y<1.
$$
因此条件密度为
$$
f_{X\mid Y}(x\mid y)=\frac{f(x,y)}{f_Y(y)}
=
\begin{cases}
\dfrac1{2-2y}, & y<x<2-y,\ 0<y<1,\\
0, & \text{其他}.
\end{cases}
$$
""",
    ),
]


def annual_questions_md(questions: list[Question]) -> str:
    lines = [
        f"# {YEAR} 年数学三真题",
        "",
        "资料类型：考研数学三历年真题",
        f"年份：{YEAR}",
        "科目：数学三",
        "整理状态：按原卷页面视觉核对后人工转写并清洗。",
        "",
    ]
    for qn in questions:
        lines.extend(
            [
                f"### 第 {qn.number} 题",
                f"- 题型：{qtype_label(qn.question_type)}",
                f"- 题号：{qn.number}",
                f"- 分值：{qn.score}",
                f"- 模块：{qn.module}",
                f"- 考点：{'、'.join(qn.topics)}",
                f"- PDF 页码：{qn.pdf_pages}",
                "- 校对状态：已结合原卷页面人工核对",
                "",
                qn.stem,
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def annual_answers_md(questions: list[Question]) -> str:
    lines = [
        f"# {YEAR} 年数学三答案解析",
        "",
        "资料类型：考研数学三答案解析",
        f"年份：{YEAR}",
        "科目：数学三",
        "整理状态：按答案页视觉核对后人工清洗整理。",
        "",
    ]
    grouped = {
        "single_choice": [qn for qn in questions if qn.question_type == "single_choice"],
        "fill_blank": [qn for qn in questions if qn.question_type == "fill_blank"],
        "solution": [qn for qn in questions if qn.question_type == "solution"],
    }
    section_names = {
        "single_choice": "选择题",
        "fill_blank": "填空题",
        "solution": "解答题",
    }
    for key in ("single_choice", "fill_blank", "solution"):
        lines.extend(
            [
                f"## {section_names[key]}",
                "",
                "| 题号 | 答案 |",
                "|---|---|",
            ]
        )
        for qn in grouped[key]:
            lines.append(f"| {qn.number} | {answer_for_table(qn.answer)} |")
        lines.append("")
    lines.extend(["## 详细解析", ""])
    for qn in questions:
        lines.extend(
            [
                f"### 第 {qn.number} 题",
                "",
                f"- 答案：{qn.answer}",
                "",
                qn.explanation,
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def build_cards(questions: list[Question]) -> None:
    card_dir = YEAR_DIR / "questions"
    card_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for qn in questions:
        qid = question_id(qn.number)
        card = "\n".join(
            [
                "---",
                f"question_id: {qid}",
                f"exam_id: kaoyan_math3_{YEAR}",
                "exam_type: math3",
                f"year: {YEAR}",
                f"question_number: {qn.number}",
                f"question_type: {qn.question_type}",
                f"score: {qn.score}",
                f"module: {qn.module}",
                "topics:",
                *[f"  - {topic}" for topic in qn.topics],
                "difficulty: unknown",
                "review_status: reviewed",
                "answer_status: available",
                "explanation_status: available",
                f"source_file: math3_{YEAR}_questions.md",
                f"answer_source_file: math3_{YEAR}_answers.md",
                "---",
                "",
                f"# {YEAR} 数学三第 {qn.number} 题",
                "",
                "## 题目",
                "",
                qn.stem,
                "",
                "## 标准答案",
                "",
                qn.answer,
                "",
                "## 解析",
                "",
                qn.explanation,
                "",
                "## 来源",
                "",
                f"- 题目来源：`math3_{YEAR}_questions.md`",
                f"- 答案来源：`math3_{YEAR}_answers.md`",
                "",
            ]
        )
        (card_dir / f"q{qn.number:03d}.md").write_text(card, encoding="utf-8")
        rows.append(
            {
                "question_id": qid,
                "exam_id": f"kaoyan_math3_{YEAR}",
                "exam_type": "math3",
                "year": YEAR,
                "question_number": qn.number,
                "question_type": qn.question_type,
                "score": qn.score,
                "module": qn.module,
                "topics": qn.topics,
                "difficulty": "unknown",
                "review_status": "reviewed",
                "answer_status": "available",
                "explanation_status": "available",
                "source_file": f"math3_{YEAR}_questions.md",
                "answer_source_file": f"math3_{YEAR}_answers.md",
                "card_path": f"questions/q{qn.number:03d}.md",
                "answer": qn.answer,
                "explanation": qn.explanation,
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
        "question_ids": [question_id(qn.number) for qn in questions],
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
