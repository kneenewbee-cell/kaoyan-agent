from __future__ import annotations

import json
from pathlib import Path


YEAR = 2019
EXAM_TYPE = "math3"
EXAM_ID = f"kaoyan_{EXAM_TYPE}_{YEAR}"
ROOT = Path(__file__).resolve().parent


QUESTIONS = [
    {
        "number": 1,
        "type": "choice",
        "score": 4,
        "module": "高等数学",
        "topics": ["无穷小比较"],
        "stem": r"""当 $x\\to 0$ 时，若 $x-\\tan x$ 与 $x^k$ 是同阶无穷小，则 $k=\\underline{\\qquad}$。

（A）1.  （B）2.  （C）3.  （D）4.""",
        "answer": "C",
        "explanation": r"""由麦克劳林展开式
$$
\\tan x=x+\\frac{x^3}{3}+o(x^3),
$$
得
$$
x-\\tan x=-\\frac{x^3}{3}+o(x^3).
$$
因此 $x-\\tan x$ 与 $x^3$ 同阶，故 $k=3$，选 C。""",
    },
    {
        "number": 2,
        "type": "choice",
        "score": 4,
        "module": "高等数学",
        "topics": ["函数零点"],
        "stem": r"""已知方程
$$
x^5-5x+k=0
$$
有 3 个不同的实根，则 $k$ 的取值范围是（  ）。

（A）$(-\\infty,-4)$。  （B）$(4,+\\infty)$。  （C）$\\{-4,4\\}$。  （D）$(-4,4)$。""",
        "answer": "D",
        "explanation": r"""设 $f(x)=x^5-5x+k$，则
$$
f'(x)=5x^4-5=5(x^2-1)(x^2+1).
$$
故 $f$ 在 $(-\\infty,-1)$、$(1,+\\infty)$ 上递增，在 $(-1,1)$ 上递减。又
$$
\\lim_{x\\to -\\infty}f(x)=-\\infty,\qquad \\lim_{x\\to +\\infty}f(x)=+\\infty.
$$
要有三个不同实根，需极大值 $f(-1)>0$ 且极小值 $f(1)<0$，即
$$
-1+5+k>0,\qquad 1-5+k<0,
$$
所以 $-4<k<4$，选 D。""",
    },
    {
        "number": 3,
        "type": "choice",
        "score": 4,
        "module": "高等数学",
        "topics": ["常系数微分方程"],
        "stem": r"""已知微分方程
$$
y''+ay'+by=ce^x
$$
的通解为
$$
y=(C_1+C_2x)e^{-x}+e^x,
$$
则 $a,b,c$ 依次为（  ）。

（A）$1,0,1$。  （B）$1,0,2$。  （C）$2,1,3$。  （D）$2,1,4$。""",
        "answer": "D",
        "explanation": r"""由齐次方程通解 $(C_1+C_2x)e^{-x}$ 可知，$-1$ 是特征方程
$$
\\lambda^2+a\\lambda+b=0
$$
的二重根，故
$$
1-a+b=0,\qquad a^2-4b=0.
$$
又 $y=e^x$ 为非齐次方程特解，代入得
$$
1+a+b=c.
$$
解得 $a=2,b=1,c=4$，选 D。""",
    },
    {
        "number": 4,
        "type": "choice",
        "score": 4,
        "module": "高等数学",
        "topics": ["级数敛散性"],
        "stem": r"""若 $\\sum_{n=1}^{\\infty}nu_n$ 绝对收敛，$\\sum_{n=1}^{\\infty}\\dfrac{v_n}{n}$ 条件收敛，则（  ）。

（A）$\\sum_{n=1}^{\\infty}u_nv_n$ 条件收敛。

（B）$\\sum_{n=1}^{\\infty}u_nv_n$ 绝对收敛。

（C）$\\sum_{n=1}^{\\infty}(u_n+v_n)$ 收敛。

（D）$\\sum_{n=1}^{\\infty}(u_n+v_n)$ 发散。""",
        "answer": "B",
        "explanation": r"""因为
$$
\\frac{|u_nv_n|}{|nu_n|}=\\left|\\frac{v_n}{n}\\right|\\to 0,
$$
且 $\\sum nu_n$ 绝对收敛，由比较判别法可知 $\\sum u_nv_n$ 绝对收敛。

而 $\\sum v_n$ 的敛散性不由 $\\sum v_n/n$ 条件收敛唯一确定，所以 C、D 不能保证。选 B。""",
    },
    {
        "number": 5,
        "type": "choice",
        "score": 4,
        "module": "线性代数",
        "topics": ["伴随矩阵", "秩"],
        "stem": r"""设 $A$ 是 4 阶矩阵，$A^*$ 是 $A$ 的伴随矩阵。若线性方程组 $Ax=0$ 的基础解系中只有 2 个向量，则
$$
r(A^*)=\\underline{\\qquad}.
$$

（A）0.  （B）1.  （C）2.  （D）3.""",
        "answer": "A",
        "explanation": r"""基础解系含 2 个向量，故
$$
4-r(A)=2,\qquad r(A)=2.
$$
对 4 阶矩阵，当 $r(A)<n-1$ 时，伴随矩阵 $A^*=0$，所以 $r(A^*)=0$，选 A。""",
    },
    {
        "number": 6,
        "type": "choice",
        "score": 4,
        "module": "线性代数",
        "topics": ["实对称矩阵", "二次型"],
        "stem": r"""设 $A$ 是 3 阶实对称矩阵，$E$ 是 3 阶单位矩阵。若
$$
A^2+A=2E,\qquad |A|=4,
$$
则二次型 $x^TAx$ 的规范形为（  ）。

（A）$y_1^2+y_2^2+y_3^2$。
（B）$y_1^2+y_2^2-y_3^2$。
（C）$y_1^2-y_2^2-y_3^2$。
（D）$-y_1^2-y_2^2-y_3^2$。""",
        "answer": "C",
        "explanation": r"""设 $\\lambda$ 为 $A$ 的特征值。由 $A^2+A=2E$ 得
$$
\\lambda^2+\\lambda=2,
$$
故 $\\lambda=1$ 或 $\\lambda=-2$。又 $A$ 为 3 阶实对称矩阵，且三个特征值乘积为 $|A|=4$，只能为 $1,-2,-2$。正惯性指数为 1，负惯性指数为 2，规范形为
$$
y_1^2-y_2^2-y_3^2.
$$
选 C。""",
    },
    {
        "number": 7,
        "type": "choice",
        "score": 4,
        "module": "概率统计",
        "topics": ["概率运算"],
        "stem": r"""设 $A,B$ 为随机事件，则 $P(A)=P(B)$ 的充分必要条件是（  ）。

（A）$P(A\\cup B)=P(A)+P(B)$。

（B）$P(AB)=P(A)P(B)$。

（C）$P(A\\overline B)=P(B\\overline A)$。

（D）$P(AB)=P(A B)$。""",
        "answer": "C",
        "explanation": r"""由
$$
P(A\\overline B)=P(A)-P(AB),\qquad P(B\\overline A)=P(B)-P(AB),
$$
可知
$$
P(A\\overline B)=P(B\\overline A)
\\Longleftrightarrow P(A)=P(B).
$$
选 C。""",
    },
    {
        "number": 8,
        "type": "choice",
        "score": 4,
        "module": "概率统计",
        "topics": ["正态分布"],
        "stem": r"""设随机变量 $X$ 与 $Y$ 相互独立，且都服从正态分布 $N(\\mu,\\sigma^2)$，则
$$
P\\{|X-Y|<1\\}
$$
（  ）。

（A）与 $\\mu$ 无关，而与 $\\sigma^2$ 有关。
（B）与 $\\mu$ 有关，而与 $\\sigma^2$ 无关。
（C）与 $\\mu,\\sigma^2$ 都有关。
（D）与 $\\mu,\\sigma^2$ 都无关。""",
        "answer": "A",
        "explanation": r"""因为 $X,Y$ 独立同分布，
$$
X-Y\\sim N(0,2\\sigma^2).
$$
所以
$$
P\\{|X-Y|<1\\}
=P\\left\\{\\frac{|X-Y|}{\\sqrt2\\sigma}<\\frac1{\\sqrt2\\sigma}\\right\\}
=2\\Phi\\left(\\frac1{\\sqrt2\\sigma}\\right)-1.
$$
该概率与 $\\mu$ 无关，与 $\\sigma^2$ 有关，选 A。""",
    },
    {
        "number": 9,
        "type": "fill_blank",
        "score": 4,
        "module": "高等数学",
        "topics": ["极限"],
        "stem": r"""求极限
$$
\\lim_{n\\to\\infty}\\left[\\frac1{1\\cdot2}+\\frac1{2\\cdot3}+\\cdots+\\frac1{n(n+1)}\\right]^n.
$$""",
        "answer": "$e^{-1}$",
        "explanation": r"""利用
$$
\\frac1{k(k+1)}=\\frac1k-\\frac1{k+1},
$$
括号内和式为
$$
1-\\frac1{n+1}=\\frac n{n+1}.
$$
因此
$$
\\lim_{n\\to\\infty}\\left(\\frac n{n+1}\\right)^n
=\\lim_{n\\to\\infty}\\left(1-\\frac1{n+1}\\right)^n=e^{-1}.
$$""",
    },
    {
        "number": 10,
        "type": "fill_blank",
        "score": 4,
        "module": "高等数学",
        "topics": ["拐点"],
        "stem": r"""曲线
$$
y=x\\sin x+2\\cos x\\qquad \\left(-\\frac\\pi2<x<\\frac{3\\pi}2\\right)
$$
的拐点坐标为 $\\underline{\\qquad}$。""",
        "answer": "$(\\pi,-2)$",
        "explanation": r"""有
$$
y'=x\\cos x-\\sin x,\qquad y''=-x\\sin x.
$$
令 $y''=0$ 得 $x=0$ 或 $x=\\pi$。在 $x=0$ 左右 $y''$ 不变号，故不是拐点；在 $x=\\pi$ 左右 $y''$ 变号，且
$$
y(\\pi)=\\pi\\sin\\pi+2\\cos\\pi=-2.
$$
所以拐点为 $(\\pi,-2)$。""",
    },
    {
        "number": 11,
        "type": "fill_blank",
        "score": 4,
        "module": "高等数学",
        "topics": ["定积分"],
        "stem": r"""已知函数
$$
f(x)=\\int_1^x\\sqrt{1+t^4}\\,dt,
$$
则
$$
\\int_0^1x^2f(x)\\,dx=\\underline{\\qquad}.
$$""",
        "answer": "$\\dfrac1{18}(1-2\\sqrt2)$",
        "explanation": r"""分部积分：
$$
\\int_0^1x^2f(x)\\,dx
=\\frac13x^3f(x)\\Big|_0^1-\\frac13\\int_0^1x^3f'(x)\\,dx.
$$
由于 $f(1)=0$，$f'(x)=\\sqrt{1+x^4}$，故
$$
\\int_0^1x^2f(x)\\,dx
=-\\frac13\\int_0^1x^3\\sqrt{1+x^4}\\,dx.
$$
令 $u=1+x^4$，得
$$
-\\frac13\\cdot\\frac14\\int_1^2u^{1/2}\\,du
=-\\frac1{12}\\cdot\\frac23(2\\sqrt2-1)
=\\frac1{18}(1-2\\sqrt2).
$$""",
    },
    {
        "number": 12,
        "type": "fill_blank",
        "score": 4,
        "module": "概率统计",
        "topics": ["弹性"],
        "stem": r"""以 $P_A,P_B$ 分别表示 $A,B$ 两个商品的价格，设商品 $A$ 的需求函数
$$
Q_A=500-P_A^2-P_AP_B+2P_B^2,
$$
则当 $P_A=10,\ P_B=20$ 时，商品 $A$ 的需求量对自身价格的弹性 $\\eta_{AA}\\ (\\eta_{AA}>0)$ 为 $\\underline{\\qquad}$。""",
        "answer": "$0.4$",
        "explanation": r"""价格弹性公式为
$$
\\eta_{AA}=-\\frac{P_A}{Q_A}\\frac{\\partial Q_A}{\\partial P_A}.
$$
有
$$
\\frac{\\partial Q_A}{\\partial P_A}=-2P_A-P_B.
$$
代入 $P_A=10,\ P_B=20$：
$$
Q_A=500-100-200+800=1000,\qquad
\\frac{\\partial Q_A}{\\partial P_A}=-40.
$$
所以
$$
\\eta_{AA}=-\\frac{10}{1000}(-40)=0.4.
$$""",
    },
    {
        "number": 13,
        "type": "fill_blank",
        "score": 4,
        "module": "线性代数",
        "topics": ["线性方程组"],
        "stem": r"""已知
$$
A=\\begin{pmatrix}
1&0&-1\\\\
1&1&-1\\\\
0&1&a^2-1
\\end{pmatrix},\qquad
b=\\begin{pmatrix}0\\\\1\\\\a\\end{pmatrix}.
$$
若线性方程组 $Ax=b$ 有无穷多解，则 $a=\\underline{\\qquad}$。""",
        "answer": "$1$",
        "explanation": r"""对增广矩阵作初等行变换：
$$
\\left(\\begin{array}{ccc|c}
1&0&-1&0\\\\
1&1&-1&1\\\\
0&1&a^2-1&a
\\end{array}\\right)
\\sim
\\left(\\begin{array}{ccc|c}
1&0&-1&0\\\\
0&1&0&1\\\\
0&0&a^2-1&a-1
\\end{array}\\right).
$$
要有无穷多解，需
$$
a^2-1=0,\qquad a-1=0,
$$
故 $a=1$。""",
    },
    {
        "number": 14,
        "type": "fill_blank",
        "score": 4,
        "module": "概率统计",
        "topics": ["分布函数"],
        "stem": r"""设随机变量 $X$ 的概率密度为
$$
f(x)=\\begin{cases}
\\dfrac{x}{2},&0<x<2,\\\\
0,&\\text{其他},
\\end{cases}
$$
$F(x)$ 为 $X$ 的分布函数，$E(X)$ 为 $X$ 的数学期望，则
$$
P\\{F(X)>E(X)-1\\}=\\underline{\\qquad}.
$$""",
        "answer": "$\\dfrac23$",
        "explanation": r"""当 $0\\le x<2$ 时，
$$
F(x)=\\int_0^x\\frac t2\\,dt=\\frac{x^2}{4}.
$$
又
$$
E(X)=\\int_0^2x\\frac x2\\,dx=\\frac43.
$$
因此
$$
P\\{F(X)>E(X)-1\\}
=P\\left\\{\\frac{X^2}{4}>\\frac13\\right\\}
=P\\left\\{X>\\frac2{\\sqrt3}\\right\\}.
$$
于是
$$
\\int_{2/\\sqrt3}^{2}\\frac x2\\,dx
=\\left.\\frac{x^2}{4}\\right|_{2/\\sqrt3}^{2}
=1-\\frac13=\\frac23.
$$""",
    },
    {
        "number": 15,
        "type": "solution",
        "score": 10,
        "module": "高等数学",
        "topics": ["分段函数", "极值"],
        "stem": r"""已知函数
$$
f(x)=\\begin{cases}
x^{2x},&x>0,\\\\
xe^x+1,&x\\le 0.
\\end{cases}
$$
求 $f'(x)$，并求 $f(x)$ 的极值。""",
        "answer": r"""$f'(0)$ 不存在，
$$
f'(x)=\\begin{cases}
2x^{2x}(\\ln x+1),&x>0,\\\\
e^x(x+1),&x<0.
\\end{cases}
$$
极小值为 $f(-1)=1-\\dfrac1e$ 和 $f(1/e)=e^{-2/e}$，极大值为 $f(0)=1$。""",
        "explanation": r"""当 $x>0$ 时，$x^{2x}=e^{2x\\ln x}$，故
$$
f'(x)=2x^{2x}(\\ln x+1).
$$
当 $x<0$ 时，
$$
f'(x)=e^x(x+1).
$$
在 $x=0$ 处，
$$
\\lim_{x\\to0^+}\\frac{x^{2x}-1}{x}
=\\lim_{x\\to0^+}\\frac{e^{2x\\ln x}-1}{x}
=\\lim_{x\\to0^+}2\\ln x=-\\infty,
$$
所以 $f'(0)$ 不存在。

令 $f'(x)=0$，得驻点 $x=-1$、$x=1/e$。符号分析可得：$f$ 在 $(-\\infty,-1)$、$(0,1/e)$ 上递减，在 $(-1,0)$、$(1/e,+\\infty)$ 上递增；又 $f(0)=1$，且左右附近函数值均小于 1，所以
$$
f(-1)=1-\\frac1e,\qquad f(1/e)=e^{-2/e}
$$
为极小值，$f(0)=1$ 为极大值。""",
    },
    {
        "number": 16,
        "type": "solution",
        "score": 10,
        "module": "高等数学",
        "topics": ["多元复合函数求导"],
        "stem": r"""设函数 $f(u,v)$ 具有 2 阶连续偏导数，函数
$$
g(x,y)=xy-f(x+y,x-y).
$$
求
$$
\\frac{\\partial^2g}{\\partial x^2}
+\\frac{\\partial^2g}{\\partial x\\partial y}
+\\frac{\\partial^2g}{\\partial y^2}.
$$""",
        "answer": r"""$$
1-3f_{uu}(x+y,x-y)-f_{vv}(x+y,x-y).
$$""",
        "explanation": r"""记 $u=x+y,\ v=x-y$。先求一阶偏导：
$$
g_x=y-f_u(u,v)-f_v(u,v),
$$
$$
g_y=x-f_u(u,v)+f_v(u,v).
$$
继续求二阶偏导：
$$
g_{xx}=-f_{uu}-2f_{uv}-f_{vv},
$$
$$
g_{xy}=1-f_{uu}+f_{vv},
$$
$$
g_{yy}=-f_{uu}+2f_{uv}-f_{vv}.
$$
三式相加得
$$
g_{xx}+g_{xy}+g_{yy}
=1-3f_{uu}(x+y,x-y)-f_{vv}(x+y,x-y).
$$""",
    },
    {
        "number": 17,
        "type": "solution",
        "score": 10,
        "module": "高等数学",
        "topics": ["微分方程", "旋转体体积"],
        "stem": r"""设函数 $y(x)$ 是微分方程
$$
y'-xy=\\frac1{2\\sqrt x}e^{x^2/2}
$$
满足条件 $y(1)=\\sqrt e$ 的特解。

（I）求 $y(x)$；

（II）设平面区域
$$
D=\\{(x,y)\\mid 1\\le x\\le2,\ 0\\le y\\le y(x)\\},
$$
求 $D$ 绕 $x$ 轴旋转所得旋转体的体积。""",
        "answer": r"""$$
y(x)=\\sqrt x\,e^{x^2/2},\qquad
V=\\frac\\pi2(e^4-e).
$$""",
        "explanation": r"""原方程为一阶线性方程。积分因子为 $e^{-x^2/2}$，于是
$$
\\left(ye^{-x^2/2}\\right)'=\\frac1{2\\sqrt x}.
$$
积分得
$$
ye^{-x^2/2}=\\sqrt x+C.
$$
由 $y(1)=\\sqrt e$ 得 $C=0$，故
$$
y(x)=\\sqrt x\,e^{x^2/2}.
$$

旋转体体积为
$$
V=\\pi\\int_1^2y^2(x)\,dx
=\\pi\\int_1^2x e^{x^2}\,dx
=\\frac\\pi2e^{x^2}\\Big|_1^2
=\\frac\\pi2(e^4-e).
$$""",
    },
    {
        "number": 18,
        "type": "solution",
        "score": 10,
        "module": "高等数学",
        "topics": ["定积分", "无穷级数"],
        "stem": r"""求曲线
$$
y=e^{-x}\\sin x\qquad (x\\ge0)
$$
与 $x$ 轴之间图形的面积。""",
        "answer": r"""$$
\\frac{e^{\\pi}+1}{2(e^{\\pi}-1)}.
$$""",
        "explanation": r"""所求面积为
$$
S=\\int_0^{+\\infty}e^{-x}|\\sin x|\,dx
=\\sum_{n=0}^{\\infty}(-1)^n\\int_{n\\pi}^{(n+1)\\pi}e^{-x}\\sin x\,dx.
$$
计算
$$
\\int_{n\\pi}^{(n+1)\\pi}e^{-x}\\sin x\,dx
=\\frac{(-1)^n}{2}\\left(e^{-n\\pi}+e^{-(n+1)\\pi}\\right).
$$
故
$$
S=\\frac12\\sum_{n=0}^{\\infty}\\left(e^{-n\\pi}+e^{-(n+1)\\pi}\\right)
=\\frac12(1+e^{-\\pi})\\sum_{n=0}^{\\infty}e^{-n\\pi}
=\\frac{e^{\\pi}+1}{2(e^{\\pi}-1)}.
$$""",
    },
    {
        "number": 19,
        "type": "solution",
        "score": 10,
        "module": "高等数学",
        "topics": ["定积分递推", "数列极限"],
        "stem": r"""设
$$
a_n=\\int_0^1x^n\\sqrt{1-x^2}\\,dx\\qquad(n=0,1,2,\\cdots).
$$

（I）证明数列 $\\{a_n\\}$ 单调递减，且
$$
a_n=\\frac{n-1}{n+2}a_{n-2}\qquad(n=2,3,\\cdots);
$$

（II）求
$$
\\lim_{n\\to\\infty}\\frac{a_n}{a_{n-1}}.
$$""",
        "answer": "$1$",
        "explanation": r"""有
$$
a_{n+1}-a_n=\\int_0^1x^n(x-1)\\sqrt{1-x^2}\\,dx<0,
$$
故 $\\{a_n\\}$ 单调递减。

当 $n\\ge2$ 时分部积分：
$$
a_n=\\int_0^1x^n\\sqrt{1-x^2}\\,dx
=-\\frac13x^{n-1}(1-x^2)^{3/2}\\Big|_0^1
+\\frac{n-1}{3}\\int_0^1x^{n-2}(1-x^2)^{3/2}\,dx.
$$
又
$$
\\int_0^1x^{n-2}(1-x^2)^{3/2}\,dx
=a_{n-2}-a_n,
$$
所以
$$
a_n=\\frac{n-1}{3}(a_{n-2}-a_n),
$$
即
$$
a_n=\\frac{n-1}{n+2}a_{n-2}.
$$

由递推式
$$
\\frac{a_n}{a_{n-1}}
=\\frac{n-1}{n+2}\\frac{a_{n-2}}{a_{n-1}}.
$$
因 $a_n>0$ 且单调递减，得
$$
\\frac{n-1}{n+2}<\\frac{a_n}{a_{n-1}}<1.
$$
夹逼得
$$
\\lim_{n\\to\\infty}\\frac{a_n}{a_{n-1}}=1.
$$""",
    },
    {
        "number": 20,
        "type": "solution",
        "score": 11,
        "module": "线性代数",
        "topics": ["向量组等价"],
        "stem": r"""已知向量组 I：
$$
\\alpha_1=\\begin{pmatrix}1\\\\1\\\\4\\end{pmatrix},\quad
\\alpha_2=\\begin{pmatrix}1\\\\0\\\\4\\end{pmatrix},\quad
\\alpha_3=\\begin{pmatrix}1\\\\2\\\\a^2+3\\end{pmatrix},
$$
与 II：
$$
\\beta_1=\\begin{pmatrix}1\\\\1\\\\a+3\\end{pmatrix},\quad
\\beta_2=\\begin{pmatrix}0\\\\2\\\\1-a\\end{pmatrix},\quad
\\beta_3=\\begin{pmatrix}1\\\\3\\\\a^2+3\\end{pmatrix}.
$$
若向量组 I 与 II 等价，求 $a$ 的取值，并将 $\\beta_3$ 用 $\\alpha_1,\\alpha_2,\\alpha_3$ 线性表示。""",
        "answer": r"""$a\\ne-1$。当 $a\\ne1$ 且 $a\\ne-1$ 时，
$$
\\beta_3=\\alpha_1-\\alpha_2+\\alpha_3.
$$
当 $a=1$ 时，
$$
\\beta_3=(3-2k)\\alpha_1+(k-2)\\alpha_2+k\\alpha_3,\qquad k\\in\\mathbb R.
$$""",
        "explanation": r"""由向量组等价定义，两组向量应能相互线性表示。分别比较
$$
r(\\alpha_1,\\alpha_2,\\alpha_3)
$$
与加入 $\\beta_1,\beta_2,\beta_3$ 后的秩，可得当 $a=-1$ 时不等价；当 $a=1$ 或 $a\\ne1,-1$ 时，$\\beta_1,\beta_2,\beta_3$ 均可由 $\\alpha_1,\alpha_2,\alpha_3$ 线性表示。再反向检验可知等价条件为
$$
a\\ne-1.
$$

设
$$
x_1\\alpha_1+x_2\\alpha_2+x_3\\alpha_3=\\beta_3.
$$
当 $a\\ne1,-1$ 时，解得
$$
x_1=1,\quad x_2=-1,\quad x_3=1,
$$
故
$$
\\beta_3=\\alpha_1-\\alpha_2+\alpha_3.
$$
当 $a=1$ 时，线性方程组有无穷多解，可取
$$
x_1=3-2k,\quad x_2=k-2,\quad x_3=k,
$$
故
$$
\\beta_3=(3-2k)\\alpha_1+(k-2)\\alpha_2+k\\alpha_3.
$$""",
    },
    {
        "number": 21,
        "type": "solution",
        "score": 11,
        "module": "线性代数",
        "topics": ["矩阵相似"],
        "stem": r"""已知矩阵
$$
A=\\begin{pmatrix}
-2&-2&1\\\\
2&x&-2\\\\
0&0&-2
\\end{pmatrix}
$$
与
$$
B=\\begin{pmatrix}
2&1&0\\\\
0&-1&0\\\\
0&0&y
\\end{pmatrix}
$$
相似。

（I）求 $x,y$；

（II）求可逆矩阵 $P$，使得 $P^{-1}AP=B$。""",
        "answer": r"""$$
x=3,\qquad y=-2,
$$
可取
$$
P=\\begin{pmatrix}
1&1&1\\\\
-2&-1&-2\\\\
0&0&-4
\\end{pmatrix}.
$$""",
        "explanation": r"""相似矩阵有相同迹和行列式，故
$$
\\operatorname{tr}(A)=\\operatorname{tr}(B),\qquad |A|=|B|.
$$
于是
$$
x-4=y+1,\qquad 4x-8=-2y,
$$
解得
$$
x=3,\qquad y=-2.
$$

此时 $B$ 的特征值为 $2,-1,-2$。矩阵 $A$ 对应特征值 $2,-1,-2$ 的特征向量可取
$$
\\xi_1=(1,-2,0)^T,\quad
\\xi_2=(-2,1,0)^T,\quad
\\xi_3=(1,-2,-4)^T.
$$
矩阵 $B$ 对应特征向量可取
$$
\\eta_1=(1,0,0)^T,\quad
\\eta_2=(1,-3,0)^T,\quad
\\eta_3=(0,0,1)^T.
$$
令 $P_1=(\\xi_1,\xi_2,\xi_3)$，$P_2=(\\eta_1,\eta_2,\eta_3)$，则
$$
P=P_1P_2^{-1}
=\\begin{pmatrix}
1&1&1\\\\
-2&-1&-2\\\\
0&0&-4
\\end{pmatrix}.
$$
于是 $P^{-1}AP=B$。""",
    },
    {
        "number": 22,
        "type": "solution",
        "score": 11,
        "module": "概率统计",
        "topics": ["指数分布", "相关性", "独立性"],
        "stem": r"""设随机变量 $X$ 与 $Y$ 相互独立，$X$ 服从参数为 1 的指数分布，$Y$ 的概率分布为
$$
P\\{Y=-1\\}=p,\qquad P\\{Y=1\\}=1-p,\qquad 0<p<1.
$$
令 $Z=XY$。

（I）求 $Z$ 的概率密度；

（II）$p$ 为何值时，$X$ 与 $Z$ 不相关；

（III）$X$ 与 $Z$ 是否相互独立？""",
        "answer": r"""$$
f_Z(z)=\\begin{cases}
pe^z,&z<0,\\\\
(1-p)e^{-z},&z\\ge0.
\\end{cases}
$$
当 $p=\\dfrac12$ 时 $X$ 与 $Z$ 不相关；$X$ 与 $Z$ 不相互独立。""",
        "explanation": r"""由全概率公式，
$$
F_Z(z)=P(XY\\le z)
=pP(-X\\le z)+(1-p)P(X\\le z).
$$
当 $z<0$ 时，
$$
F_Z(z)=pP(X\ge -z)=pe^z;
$$
当 $z\ge0$ 时，
$$
F_Z(z)=p+(1-p)(1-e^{-z})=1-(1-p)e^{-z}.
$$
故
$$
f_Z(z)=\\begin{cases}
pe^z,&z<0,\\\\
(1-p)e^{-z},&z\\ge0.
\\end{cases}
$$

又 $E(X)=1,\ D(X)=1,\ E(Y)=1-2p$，且 $X,Y$ 独立，因此
$$
\\operatorname{Cov}(X,Z)
=\\operatorname{Cov}(X,XY)
=E(X^2)E(Y)-E(X)E(X)E(Y)
=D(X)E(Y)=1-2p.
$$
令协方差为 0，得 $p=1/2$。

但例如
$$
P\\{X\\le1,\ Z\\le-1\\}=0,
$$
而 $P\\{X\\le1\\}>0$ 且 $P\\{Z\\le-1\\}>0$，故不满足独立性，$X$ 与 $Z$ 不相互独立。""",
    },
    {
        "number": 23,
        "type": "solution",
        "score": 11,
        "module": "概率统计",
        "topics": ["最大似然估计"],
        "stem": r"""设总体 $X$ 的概率密度为
$$
f(x;\\sigma^2)=\\begin{cases}
\\dfrac A\\sigma e^{-\\frac{(x-\\mu)^2}{2\\sigma^2}},&x\\ge\\mu,\\\\
0,&x<\\mu,
\\end{cases}
$$
其中 $\\mu$ 是已知参数，$\\sigma>0$ 是未知参数，$A$ 是常数。$X_1,X_2,\\cdots,X_n$ 是来自总体 $X$ 的简单随机样本。

（I）求 $A$；

（II）求 $\\sigma^2$ 的最大似然估计量。""",
        "answer": r"""$$
A=\\sqrt{\\frac2\\pi},\qquad
\\widehat{\\sigma^2}=\\frac1n\\sum_{i=1}^n(X_i-\\mu)^2.
$$""",
        "explanation": r"""由密度积分为 1，
$$
1=\\int_\\mu^{+\\infty}\\frac A\\sigma e^{-\\frac{(x-\\mu)^2}{2\\sigma^2}}\,dx.
$$
令 $t=(x-\mu)/\sigma$，得
$$
1=A\\int_0^{+\infty}e^{-t^2/2}\,dt
=A\\frac{\\sqrt{2\\pi}}2,
$$
所以
$$
A=\\sqrt{\\frac2\\pi}.
$$

设样本观测值为 $x_1,\ldots,x_n$。当 $x_i\\ge\mu$ 全部成立时，似然函数为
$$
L(\\sigma^2)=\\left(\\frac2\\pi\\right)^{n/2}(\\sigma^2)^{-n/2}
\\exp\\left\\{-\\frac1{2\\sigma^2}\\sum_{i=1}^n(x_i-\mu)^2\\right\\}.
$$
对数似然为
$$
\\ln L(\\sigma^2)=\\frac n2\\ln\\frac2\\pi-\\frac n2\\ln\\sigma^2
-\\frac1{2\\sigma^2}\\sum_{i=1}^n(x_i-\mu)^2.
$$
令关于 $\\sigma^2$ 的导数为 0：
$$
-\\frac n{2\\sigma^2}
+\\frac1{2\\sigma^4}\\sum_{i=1}^n(x_i-\mu)^2=0,
$$
得
$$
\\widehat{\\sigma^2}=\\frac1n\\sum_{i=1}^n(X_i-\mu)^2.
$$""",
    },
]


def question_id(number: int) -> str:
    return f"kaoyan_{EXAM_TYPE}_{YEAR}_q{number:03d}"


def yaml_list(items: list[str]) -> str:
    return "\n".join(f"  - {item}" for item in items)


def latex_text(text: str) -> str:
    return text.replace("\\\\", "\\")


def card_markdown(q: dict) -> str:
    qid = question_id(q["number"])
    n = q["number"]
    return f"""---
question_id: {qid}
exam_id: {EXAM_ID}
exam_type: {EXAM_TYPE}
year: {YEAR}
question_number: {n}
question_type: {q["type"]}
score: {q["score"]}
module: {q["module"]}
topics:
{yaml_list(q["topics"])}
difficulty: unknown
review_status: reviewed
answer_status: available
explanation_status: available
source_file: math3_{YEAR}_questions.md
answer_source_file: math3_{YEAR}_answers.md
---

# {YEAR} 数学三第 {n} 题

## 题目

{latex_text(q["stem"])}

## 标准答案

{latex_text(q["answer"])}

## 解析

{latex_text(q["explanation"])}

## 来源

- 题目来源：math3_{YEAR}_questions.md
- 答案解析来源：math3_{YEAR}_answers.md
"""


def main() -> None:
    questions_dir = ROOT / "questions"
    questions_dir.mkdir(exist_ok=True)

    for q in QUESTIONS:
        (questions_dir / f"q{q['number']:03d}.md").write_text(card_markdown(q), encoding="utf-8", newline="\n")

    questions_md = [f"# {YEAR} 年考研数学三真题\n"]
    answers_md = [f"# {YEAR} 年考研数学三答案与解析\n"]
    jsonl_rows = []

    for q in QUESTIONS:
        n = q["number"]
        qid = question_id(n)
        stem = latex_text(q["stem"])
        answer = latex_text(q["answer"])
        explanation = latex_text(q["explanation"])
        questions_md.append(f"## 第 {n} 题\n\n{stem}\n")
        answers_md.append(f"## 第 {n} 题\n\n### 标准答案\n\n{answer}\n\n### 解析\n\n{explanation}\n")
        jsonl_rows.append(
            {
                "question_id": qid,
                "exam_id": EXAM_ID,
                "exam_type": EXAM_TYPE,
                "year": YEAR,
                "question_number": n,
                "question_type": q["type"],
                "score": q["score"],
                "module": q["module"],
                "topics": q["topics"],
                "difficulty": "unknown",
                "review_status": "reviewed",
                "answer_status": "available",
                "explanation_status": "available",
                "question_file": f"questions/q{n:03d}.md",
                "card_path": f"questions/q{n:03d}.md",
                "source_file": f"math3_{YEAR}_questions.md",
                "answer_source_file": f"math3_{YEAR}_answers.md",
                "stem": stem,
                "answer": answer,
                "explanation": explanation,
            }
        )

    (ROOT / f"math3_{YEAR}_questions.md").write_text("\n".join(questions_md).rstrip() + "\n", encoding="utf-8", newline="\n")
    (ROOT / f"math3_{YEAR}_answers.md").write_text("\n".join(answers_md).rstrip() + "\n", encoding="utf-8", newline="\n")
    (ROOT / "questions.jsonl").write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in jsonl_rows),
        encoding="utf-8",
        newline="\n",
    )

    manifest = {
        "exam_id": EXAM_ID,
        "exam_type": EXAM_TYPE,
        "year": YEAR,
        "question_count": len(QUESTIONS),
        "source_files": [
            f"math3_{YEAR}_questions.md",
            f"math3_{YEAR}_answers.md",
        ],
        "questions_jsonl": "questions.jsonl",
        "questions_dir": "questions",
        "status": "reviewed",
        "notes": [
            "2019 年原 OCR 中间文件存在中文乱码，本脚本按源页图与答案页图重建题干、答案和解析。",
            "公式统一使用 LaTeX 块或行内公式，不使用 text code fence 表示数学公式。",
        ],
    }
    (ROOT / "paper_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"year": YEAR, "question_count": len(QUESTIONS)}, ensure_ascii=False))


if __name__ == "__main__":
    main()


