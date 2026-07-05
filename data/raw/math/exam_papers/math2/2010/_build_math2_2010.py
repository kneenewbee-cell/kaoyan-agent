from __future__ import annotations

import json
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parent
IMAGES = ROOT / "images"
SOURCE_PAGES = IMAGES / "source_pages"
QUESTIONS_DIR = ROOT / "questions"

EXAM_ID = "kaoyan_math2_2010"
YEAR = 2010


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


QUESTIONS = [
    {
        "question_number": 1,
        "question_type": "choice",
        "score": 4,
        "module": "高等数学",
        "topics": ["间断点", "极限"],
        "page": "page-1.png",
        "question": """函数
$$
f(x)=\\frac{x^2-x}{x^2-1}\\sqrt{1+\\frac{1}{x^2}}
$$
的无穷间断点的个数为（  ）  
A. $0$  
B. $1$  
C. $2$  
D. $3$
""",
        "answer": "B",
        "explanation": """函数在 $x=0,\\pm1$ 处都有可能出现间断。化简
$$
f(x)=\\frac{x}{x+1}\\sqrt{1+\\frac1{x^2}}\\quad(x\\ne1).
$$
当 $x\\to0$ 时，左右极限分别为 $1$ 与 $-1$，故 $x=0$ 是跳跃间断点；当 $x\\to1$ 时极限存在且有限，故 $x=1$ 是可去间断点；当 $x\\to-1$ 时分母趋于 $0$ 而分子不为 $0$，故 $x=-1$ 是无穷间断点。因此无穷间断点只有 $1$ 个。""",
    },
    {
        "question_number": 2,
        "question_type": "choice",
        "score": 4,
        "module": "高等数学",
        "topics": ["一阶线性微分方程", "非齐次方程"],
        "page": "page-1.png",
        "question": """设 $y_1,y_2$ 是一阶线性非齐次微分方程
$$
y'+p(x)y=q(x)
$$
的两个特解，若常数 $\\lambda,\\mu$ 使 $\\lambda y_1+\\mu y_2$ 是该方程的解，$\\lambda y_1-\\mu y_2$ 是该方程对应齐次方程的解，则（  ）  
A. $\\lambda=\\dfrac12,\\ \\mu=\\dfrac12$  
B. $\\lambda=-\\dfrac12,\\ \\mu=-\\dfrac12$  
C. $\\lambda=\\dfrac23,\\ \\mu=\\dfrac13$  
D. $\\lambda=\\dfrac23,\\ \\mu=\\dfrac23$
""",
        "answer": "A",
        "explanation": """由 $y_1,y_2$ 都满足非齐次方程可知
$$
(\\lambda y_1-\\mu y_2)'+p(x)(\\lambda y_1-\\mu y_2)=(\\lambda-\\mu)q(x).
$$
它是齐次方程的解，因此 $(\\lambda-\\mu)q(x)=0$，而非齐次方程中 $q(x)\\not\\equiv0$，故 $\\lambda=\\mu$。又
$$
(\\lambda y_1+\\mu y_2)'+p(x)(\\lambda y_1+\\mu y_2)=(\\lambda+\\mu)q(x),
$$
要仍为原方程的解，就需 $\\lambda+\\mu=1$。联立得
$$
\\lambda=\\mu=\\frac12.
$$""",
    },
    {
        "question_number": 3,
        "question_type": "choice",
        "score": 4,
        "module": "高等数学",
        "topics": ["曲线相切", "导数"],
        "page": "page-1.png",
        "question": """曲线 $y=x^2$ 与曲线 $y=a\\ln x\\ (a\\ne0)$ 相切，则
$$
a=（\\ \\ ）
$$
A. $4e$  
B. $3e$  
C. $2e$  
D. $e$
""",
        "answer": "C",
        "explanation": """设切点为 $(x_0,x_0^2)$，则两曲线在该点既有相同函数值，又有相同导数：
$$
x_0^2=a\\ln x_0,\\qquad 2x_0=\\frac{a}{x_0}.
$$
由第二式得 $a=2x_0^2$。代回第一式：
$$
x_0^2=2x_0^2\\ln x_0\\Rightarrow \\ln x_0=\\frac12,
$$
故 $x_0=\\sqrt e$，从而
$$
a=2x_0^2=2e.
$$""",
    },
    {
        "question_number": 4,
        "question_type": "choice",
        "score": 4,
        "module": "高等数学",
        "topics": ["反常积分", "比较判别法"],
        "page": "page-1.png",
        "question": """设 $m,n$ 均是正整数，则反常积分
$$
\\int_0^1 \\frac{\\sqrt[m]{\\ln^2(1-x)}}{\\sqrt[n]{x}}\\,dx
$$
的收敛性（  ）  
A. 仅与 $m$ 的取值有关  
B. 仅与 $n$ 的取值有关  
C. 与 $m,n$ 的取值都有关  
D. 与 $m,n$ 的取值都无关
""",
        "answer": "D",
        "explanation": """在 $x\\to0^+$ 时，$\\ln(1-x)\\sim -x$，故被积函数与 $x^{\\frac1m-\\frac1n}$ 同阶。这里 $m,n$ 为正整数，所以指数始终大于 $-1$，在 $0$ 附近总可积。  
在 $x\\to1^-$ 时，令 $t=1-x$，则被积函数与 $|\\ln t|^{2/m}$ 同阶，而
$$
\\int_0^\\delta |\\ln t|^{2/m}\\,dt
$$
总收敛。因此该积分对任意正整数 $m,n$ 都收敛。""",
    },
    {
        "question_number": 5,
        "question_type": "choice",
        "score": 4,
        "module": "高等数学",
        "topics": ["隐函数", "齐次函数"],
        "page": "page-1.png",
        "question": """设函数 $z=z(x,y)$ 由方程
$$
F\\!\\left(\\frac{y}{x},\\frac{z}{x}\\right)=0
$$
确定，其中 $F$ 为可微函数，且 $F_2'\\ne0$，则
$$
x\\frac{\\partial z}{\\partial x}+y\\frac{\\partial z}{\\partial y}=（\\ \\ ）
$$
A. $x$  
B. $z$  
C. $-x$  
D. $-z$
""",
        "answer": "B",
        "explanation": """由
$$
F\\!\\left(\\frac{y}{x},\\frac{z}{x}\\right)=0
$$
可知 $\\dfrac{z}{x}$ 仅依赖于 $\\dfrac{y}{x}$，即存在函数 $\\varphi$ 使
$$
z=x\\,\\varphi\\!\\left(\\frac{y}{x}\\right).
$$
因此 $z$ 是关于 $(x,y)$ 的一次齐次函数。由 Euler 齐次函数定理，
$$
xz_x+yz_y=z.
$$""",
    },
    {
        "question_number": 6,
        "question_type": "choice",
        "score": 4,
        "module": "高等数学",
        "topics": ["二重积分", "Riemann 和"],
        "page": "page-1.png",
        "question": """求极限
$$
\\lim_{n\\to\\infty}\\sum_{i=1}^n\\sum_{j=1}^i\\frac{n}{(n+i)(n^2+j^2)}=（\\ \\ ）
$$
A. $\\displaystyle \\int_0^1 dx\\int_0^x \\frac{1}{(1+x)(1+y^2)}\\,dy$  
B. $\\displaystyle \\int_0^1 dx\\int_0^x \\frac{1}{(1+x)(1+y)}\\,dy$  
C. $\\displaystyle \\int_0^1 dx\\int_0^1 \\frac{1}{(1+x)(1+y)}\\,dy$  
D. $\\displaystyle \\int_0^1 dx\\int_0^1 \\frac{1}{(1+x)(1+y^2)}\\,dy$
""",
        "answer": "A",
        "explanation": """将和式改写为
$$
\\sum_{i=1}^n\\sum_{j=1}^i \\frac{1}{n^2}\\cdot\\frac{1}{\\left(1+\\frac{i}{n}\\right)\\left(1+\\left(\\frac{j}{n}\\right)^2\\right)}.
$$
令 $x=\\dfrac{i}{n},\\ y=\\dfrac{j}{n}$，则取样区域满足
$$
0\\le y\\le x\\le1.
$$
故该极限对应的二重积分为
$$
\\int_0^1 dx\\int_0^x \\frac{1}{(1+x)(1+y^2)}\\,dy.
$$""",
    },
    {
        "question_number": 7,
        "question_type": "choice",
        "score": 4,
        "module": "线性代数",
        "topics": ["向量组", "秩"],
        "page": "page-1.png",
        "question": """设向量组 I：$\\alpha_1,\\alpha_2,\\ldots,\\alpha_r$ 可由向量组 II：$\\beta_1,\\beta_2,\\ldots,\\beta_s$ 线性表示。下列命题正确的是（  ）  
A. 若向量组 I 线性无关，则 $r\\le s$  
B. 若向量组 I 线性相关，则 $r>s$  
C. 若向量组 II 线性无关，则 $r\\le s$  
D. 若向量组 II 线性相关，则 $r>s$
""",
        "answer": "A",
        "explanation": """向量组 I 可由向量组 II 线性表示，所以
$$
r(\\text{I})\\le r(\\text{II})\\le s.
$$
若向量组 I 线性无关，则其秩等于向量个数，即 $r(\\text{I})=r$，于是
$$
r\\le s.
$$
其余选项都不能由题设必然推出。""",
    },
    {
        "question_number": 8,
        "question_type": "choice",
        "score": 4,
        "module": "线性代数",
        "topics": ["特征值", "实对称矩阵"],
        "page": "page-1.png",
        "question": """设 $A$ 为 $4$ 阶实对称矩阵，且
$$
A^2+A=O.
$$
若 $A$ 的秩为 $3$，则 $A$ 相似于（  ）  
A. $\\operatorname{diag}(1,1,1,0)$  
B. $\\operatorname{diag}(1,1,-1,0)$  
C. $\\operatorname{diag}(1,-1,-1,0)$  
D. $\\operatorname{diag}(-1,-1,-1,0)$
""",
        "answer": "D",
        "explanation": """由 $A^2+A=O$ 得
$$
A(A+E)=O,
$$
所以任一特征值 $\\lambda$ 满足
$$
\\lambda^2+\\lambda=0\\Rightarrow \\lambda=0\\text{ 或 }-1.
$$
又因 $A$ 为实对称矩阵，必可正交相似对角化。秩为 $3$ 表明恰有三个非零特征值，因此这三个特征值都只能是 $-1$，另一个特征值是 $0$。故
$$
A\\sim \\operatorname{diag}(-1,-1,-1,0).
$$""",
    },
    {
        "question_number": 9,
        "question_type": "fill_blank",
        "score": 4,
        "module": "高等数学",
        "topics": ["常系数线性微分方程"],
        "page": "page-2.png",
        "question": """$3$ 阶常系数线性齐次微分方程
$$
y'''-2y''+y'-2y=0
$$
的通解为 $y=\\underline{\\qquad}$。""",
        "answer": "$C_1e^{2x}+e^x\\bigl(C_2\\cos x+C_3\\sin x\\bigr)$",
        "explanation": """特征方程为
$$
r^3-2r^2+r-2=0=(r-2)(r^2+1).
$$
故特征根为 $r=2,\\ \\pm i$。因此通解为
$$
y=C_1e^{2x}+e^x\\bigl(C_2\\cos x+C_3\\sin x\\bigr).
$$""",
    },
    {
        "question_number": 10,
        "question_type": "fill_blank",
        "score": 4,
        "module": "高等数学",
        "topics": ["渐近线"],
        "page": "page-2.png",
        "question": """曲线
$$
y=\\frac{2x^3}{x^2+1}
$$
的渐近线方程为 $\\underline{\\qquad}$。""",
        "answer": "$y=2x$",
        "explanation": """作多项式除法：
$$
\\frac{2x^3}{x^2+1}=2x-\\frac{2x}{x^2+1}.
$$
当 $x\\to\\pm\\infty$ 时，余项趋于 $0$，故斜渐近线为
$$
y=2x.
$$""",
    },
    {
        "question_number": 11,
        "question_type": "fill_blank",
        "score": 4,
        "module": "高等数学",
        "topics": ["高阶导数", "幂级数"],
        "page": "page-2.png",
        "question": """函数
$$
y=\\ln(1-2x)
$$
在 $x=0$ 处的 $n$ 阶导数 $y^{(n)}(0)=\\underline{\\qquad}$。""",
        "answer": "$-2^n(n-1)!$",
        "explanation": """由
$$
\\ln(1-2x)=-\\sum_{k=1}^{\\infty}\\frac{(2x)^k}{k}\\qquad(|x|<\\tfrac12),
$$
可得 $x^n$ 的系数为 $-\\dfrac{2^n}{n}$。因此
$$
y^{(n)}(0)=n!\\left(-\\frac{2^n}{n}\\right)=-2^n(n-1)!.
$$""",
    },
    {
        "question_number": 12,
        "question_type": "fill_blank",
        "score": 4,
        "module": "高等数学",
        "topics": ["极坐标曲线", "弧长"],
        "page": "page-2.png",
        "question": """当 $0\\le\\theta\\le\\pi$ 时，对数螺线
$$
r=e^{\\theta}
$$
的弧长为 $\\underline{\\qquad}$。""",
        "answer": "$\\sqrt2\\,(e^{\\pi}-1)$",
        "explanation": """极坐标弧长公式为
$$
s=\\int_0^{\\pi}\\sqrt{r^2+\\left(\\frac{dr}{d\\theta}\\right)^2}\\,d\\theta.
$$
这里 $r=e^{\\theta}$ 且 $r'=e^{\\theta}$，所以
$$
s=\\int_0^{\\pi}\\sqrt{2e^{2\\theta}}\\,d\\theta
=\\sqrt2\\int_0^{\\pi}e^{\\theta}\\,d\\theta
=\\sqrt2\\,(e^{\\pi}-1).
$$""",
    },
    {
        "question_number": 13,
        "question_type": "fill_blank",
        "score": 4,
        "module": "高等数学",
        "topics": ["相关变化率"],
        "page": "page-2.png",
        "question": """已知一个长方形的长 $l$ 以 $2\\text{ cm/s}$ 的速率增加，宽 $w$ 以 $3\\text{ cm/s}$ 的速率增加，则当 $l=12\\text{ cm},\\ w=5\\text{ cm}$ 时，它的对角线增加的速率为 $\\underline{\\qquad}$。""",
        "answer": "$3\\text{ cm/s}$",
        "explanation": """设对角线长为 $s$，则
$$
s^2=l^2+w^2.
$$
两边对时间求导：
$$
2s\\frac{ds}{dt}=2l\\frac{dl}{dt}+2w\\frac{dw}{dt}.
$$
当 $l=12,w=5$ 时，$s=13$，故
$$
\\frac{ds}{dt}=\\frac{12\\cdot2+5\\cdot3}{13}=3\\text{ cm/s}.
$$""",
    },
    {
        "question_number": 14,
        "question_type": "fill_blank",
        "score": 4,
        "module": "线性代数",
        "topics": ["行列式", "矩阵运算"],
        "page": "page-2.png",
        "question": """设 $A,B$ 为 $3$ 阶矩阵，且 $|A|=3,\\ |B|=2,\\ |A^{-1}+B|=2$，则
$$
|A+B^{-1}|=\\underline{\\qquad}.
$$""",
        "answer": "$3$",
        "explanation": """由
$$
A^{-1}+B=A^{-1}(E+AB)
$$
得
$$
|A^{-1}+B|=|A|^{-1}|E+AB|=2.
$$
代入 $|A|=3$，可得
$$
|E+AB|=6.
$$
又
$$
A+B^{-1}=B^{-1}(AB+E),
$$
故
$$
|A+B^{-1}|=|B|^{-1}|AB+E|=\\frac{1}{2}\\cdot6=3.
$$""",
    },
    {
        "question_number": 15,
        "question_type": "solution",
        "score": 10,
        "module": "高等数学",
        "topics": ["定积分函数", "单调性", "极值"],
        "page": "page-2.png",
        "question": """求函数
$$
f(x)=\\int_1^{x^2}(x^2-t)e^{-t^2}\\,dt
$$
的单调区间与极值。""",
        "answer": "单调递减区间为 $(-\\infty,-1)\\cup(0,1)$，单调递增区间为 $(-1,0)\\cup(1,+\\infty)$；极大值为 $f(0)=\\dfrac{e^{-1}-1}{2}$，极小值为 $f(\\pm1)=0$。",
        "explanation": """将积分拆开：
$$
f(x)=x^2\\int_1^{x^2}e^{-t^2}\\,dt-\\int_1^{x^2}te^{-t^2}\\,dt.
$$
求导得
$$
f'(x)=2x\\int_1^{x^2}e^{-t^2}\\,dt.
$$
令 $f'(x)=0$，得驻点 $x=0,\\pm1$。再求二阶导数
$$
f''(x)=2\\int_1^{x^2}e^{-t^2}\\,dt+4x^2e^{-x^4}.
$$
由 $f''(0)=2\\int_1^0e^{-t^2}dt<0$，知 $x=0$ 为极大值点；而 $f''(\\pm1)=4e^{-1}>0$，知 $x=\\pm1$ 为极小值点。结合
$$
\\int_1^{x^2}e^{-t^2}\\,dt
$$
在 $x^2<1$ 时为负、在 $x^2>1$ 时为正，可得单调性结论。又
$$
f(0)=\\int_1^0(-t)e^{-t^2}\\,dt=\\frac{e^{-1}-1}{2},\\qquad f(\\pm1)=0.
$$""",
    },
    {
        "question_number": 16,
        "question_type": "solution",
        "score": 10,
        "module": "高等数学",
        "topics": ["定积分估计", "极限"],
        "page": "page-2.png",
        "question": """(I) 比较
$$
\\int_0^1 |\\ln t|\\,[\\ln(1+t)]^n\\,dt
$$
与
$$
\\int_0^1 t^n|\\ln t|\\,dt\\qquad(n=1,2,\\ldots)
$$
的大小，并说明理由；  
(II) 记
$$
u_n=\\int_0^1 |\\ln t|\\,[\\ln(1+t)]^n\\,dt\\qquad(n=1,2,\\ldots),
$$
求极限 $\\displaystyle \\lim_{n\\to\\infty}nu_n$。""",
        "answer": "(I) 前者小于后者；(II) $\\displaystyle \\lim_{n\\to\\infty}nu_n=0$。",
        "explanation": """对 $0<t<1$，有
$$
0<\\ln(1+t)<t.
$$
因此
$$
0<|\\ln t|\\,[\\ln(1+t)]^n<t^n|\\ln t|,
$$
从而
$$
\\int_0^1 |\\ln t|\\,[\\ln(1+t)]^n\\,dt<\\int_0^1 t^n|\\ln t|\\,dt.
$$
又
$$
\\int_0^1 t^n|\\ln t|\\,dt=\\frac{1}{(n+1)^2},
$$
故
$$
0<nu_n<\\frac{n}{(n+1)^2}\\to0.
$$
由夹逼定理，
$$
\\lim_{n\\to\\infty}nu_n=0.
$$""",
    },
    {
        "question_number": 17,
        "question_type": "solution",
        "score": 10,
        "module": "高等数学",
        "topics": ["参数方程", "二阶导数"],
        "page": "page-3.png",
        "question": """设函数 $y=f(x)$ 由参数方程
$$
\\begin{cases}
x=2t+t^2,\\quad t>-1,\\\\
y=\\psi(t)
\\end{cases}
$$
所确定，其中 $\\psi(t)$ 具有 $2$ 阶导数，且 $\\psi(1)=\\dfrac52,\\ \\psi'(1)=6$。已知
$$
\\frac{d^2y}{dx^2}=\\frac{3}{4(1+t)},
$$
求函数 $\\psi(t)$。""",
        "answer": "$\\psi(t)=t^3+\\dfrac32t^2$",
        "explanation": """先求
$$
\\frac{dx}{dt}=2+2t=2(1+t),\\qquad \\frac{dy}{dx}=\\frac{\\psi'(t)}{2(1+t)}.
$$
于是
$$
\\frac{d^2y}{dx^2}
=\\frac{\\dfrac{d}{dt}\\left(\\dfrac{\\psi'(t)}{2(1+t)}\\right)}{2(1+t)}
=\\frac{(1+t)\\psi''(t)-\\psi'(t)}{4(1+t)^3}.
$$
与题设比较得
$$
(1+t)\\psi''(t)-\\psi'(t)=3(1+t)^2.
$$
令 $v=\\psi'(t)$，则
$$
(1+t)v'-v=3(1+t)^2.
$$
解得
$$
v=3(1+t)^2+C(1+t).
$$
由 $\\psi'(1)=6$ 得 $12+2C=6$，故 $C=-3$，于是
$$
\\psi'(t)=3t(t+1).
$$
积分得
$$
\\psi(t)=t^3+\\frac32t^2+C_1.
$$
再由 $\\psi(1)=\\dfrac52$，得 $C_1=0$。""",
    },
    {
        "question_number": 18,
        "question_type": "solution",
        "score": 10,
        "module": "高等数学",
        "topics": ["定积分应用", "平面图形面积"],
        "page": "page-3.png",
        "assets_extra": ["images/q018_diagram.png"],
        "question": """一个高为 $l$ 的柱体形贮油罐，底面是长轴为 $2a$、短轴为 $2b$ 的椭圆。现将贮油罐平放，当油罐中油面高度为 $\\dfrac{3b}{2}$ 时（如图），计算油的质量。（长度单位为 m，质量单位为 kg，油的密度为常量 $\\rho\\,\\mathrm{kg/m^3}$。）""",
        "answer": "$M=\\rho abl\\left(\\dfrac{2\\pi}{3}+\\dfrac{\\sqrt3}{4}\\right)$",
        "explanation": """椭圆截面方程可写为
$$
\\frac{x^2}{a^2}+\\frac{y^2}{b^2}=1.
$$
油面高度为 $\\dfrac{3b}{2}$，说明顶部尚有一段高度为 $\\dfrac{b}{2}$ 的空缺弓形。  
整个椭圆面积为 $\\pi ab$。顶部弓形面积为
$$
S_0=2\\int_{b/2}^{b} a\\sqrt{1-\\frac{y^2}{b^2}}\\,dy
=2ab\\int_{1/2}^{1}\\sqrt{1-u^2}\\,du
=ab\\left(\\frac{\\pi}{3}-\\frac{\\sqrt3}{4}\\right).
$$
因此油的截面积
$$
S=\\pi ab-S_0
=ab\\left(\\frac{2\\pi}{3}+\\frac{\\sqrt3}{4}\\right).
$$
体积 $V=Sl$，故油的质量为
$$
M=\\rho V=\\rho abl\\left(\\frac{2\\pi}{3}+\\frac{\\sqrt3}{4}\\right).
$$""",
    },
    {
        "question_number": 19,
        "question_type": "solution",
        "score": 11,
        "module": "高等数学",
        "topics": ["偏微分方程", "变量代换"],
        "page": "page-3.png",
        "question": """设函数 $u=f(x,y)$ 具有二阶连续偏导数，且满足等式
$$
4u_{xx}+12u_{xy}+5u_{yy}=0,
$$
确定 $a,b$ 的值，使等式在变换
$$
\\xi=x+ay,\\qquad \\eta=x+by
$$
下化简为
$$
u_{\\xi\\eta}=0.
$$""",
        "answer": "$a,b$ 为方程 $5r^2+12r+4=0$ 的两个根，即 $a=-2,\\ b=-\\dfrac25$（或交换次序）。",
        "explanation": """由链式法则，
$$
u_x=u_\\xi+u_\\eta,\\qquad u_y=au_\\xi+bu_\\eta.
$$
进一步可得
$$
u_{xx}=u_{\\xi\\xi}+2u_{\\xi\\eta}+u_{\\eta\\eta},
$$
$$
u_{xy}=a u_{\\xi\\xi}+(a+b)u_{\\xi\\eta}+b u_{\\eta\\eta},
$$
$$
u_{yy}=a^2u_{\\xi\\xi}+2abu_{\\xi\\eta}+b^2u_{\\eta\\eta}.
$$
代入原式后，若要化为 $u_{\\xi\\eta}=0$，就必须令 $u_{\\xi\\xi}$ 与 $u_{\\eta\\eta}$ 的系数同时为零，即
$$
4+12a+5a^2=0,\\qquad 4+12b+5b^2=0.
$$
解得
$$
5r^2+12r+4=0\\Rightarrow r=-2,\\ -\\frac25.
$$
故可取
$$
(a,b)=\\left(-2,-\\frac25\\right)
$$
或交换次序。""",
    },
    {
        "question_number": 20,
        "question_type": "solution",
        "score": 10,
        "module": "高等数学",
        "topics": ["二重积分", "极坐标变换"],
        "page": "page-3.png",
        "question": """计算二重积分
$$
I=\\iint_D r^2\\sin\\theta\\sqrt{1-r^2\\cos2\\theta}\\,drd\\theta,
$$
其中
$$
D=\\{(r,\\theta)\\mid 0\\le r\\le\\sec\\theta,\\ 0\\le\\theta\\le\\tfrac\\pi4\\}.
$$""",
        "answer": "$\\displaystyle I=\\frac13-\\frac{\\pi}{16}$",
        "explanation": """改用直角坐标。由
$$
x=r\\cos\\theta,\\qquad y=r\\sin\\theta
$$
知区域 $D$ 对应为
$$
0\\le y\\le x\\le1.
$$
又
$$
r^2\\cos2\\theta=x^2-y^2,\\qquad r^2\\sin\\theta\\,drd\\theta = y\\,dxdy.
$$
因此
$$
I=\\int_0^1dx\\int_0^x y\\sqrt{1-x^2+y^2}\\,dy.
$$
对内层积分令 $u=1-x^2+y^2$，得
$$
\\int_0^x y\\sqrt{1-x^2+y^2}\\,dy
=\\frac13\\left[1-(1-x^2)^{3/2}\\right].
$$
于是
$$
I=\\frac13\\int_0^1\\left[1-(1-x^2)^{3/2}\\right]dx
=\\frac13-\\frac13\\int_0^1(1-x^2)^{3/2}dx.
$$
令 $x=\\sin t$，则
$$
\\int_0^1(1-x^2)^{3/2}dx=\\int_0^{\\pi/2}\\cos^4 t\\,dt=\\frac{3\\pi}{16}.
$$
故
$$
I=\\frac13-\\frac{\\pi}{16}.
$$""",
    },
    {
        "question_number": 21,
        "question_type": "solution",
        "score": 10,
        "module": "高等数学",
        "topics": ["微分中值定理", "构造函数"],
        "page": "page-4.png",
        "question": """设函数 $f(x)$ 在闭区间 $[0,1]$ 上连续，在开区间 $(0,1)$ 内可导，且 $f(0)=0,\\ f(1)=\\dfrac13$。证明：存在 $\\xi\\in\\left(0,\\dfrac12\\right),\\ \\eta\\in\\left(\\dfrac12,1\\right)$，使得
$$
f'(\\xi)+f'(\\eta)=\\xi^2+\\eta^2.
$$""",
        "answer": "结论成立。",
        "explanation": """构造函数
$$
H(x)=f(x)-\\frac{x^3}{3}.
$$
则
$$
H(0)=f(0)=0,\\qquad H(1)=f(1)-\\frac13=0.
$$
分两种情形。  
若 $H\\!\\left(\\dfrac12\\right)=0$，则由 Rolle 定理分别在区间 $\\left[0,\\dfrac12\\right]$ 和 $\\left[\\dfrac12,1\\right]$ 上可得存在
$$
\\xi\\in\\left(0,\\frac12\\right),\\quad \\eta\\in\\left(\\frac12,1\\right)
$$
使
$$
H'(\\xi)=0,\\qquad H'(\\eta)=0.
$$
即
$$
f'(\\xi)=\\xi^2,\\qquad f'(\\eta)=\\eta^2.
$$
于是结论成立。  
若 $H\\!\\left(\\dfrac12\\right)\\ne0$，则由拉格朗日中值定理，在 $\\left[0,\\dfrac12\\right]$ 上存在 $\\xi\\in\\left(0,\\dfrac12\\right)$ 使
$$
H'(\\xi)=\\frac{H(1/2)-H(0)}{1/2}=2H\\!\\left(\\frac12\\right),
$$
在 $\\left[\\dfrac12,1\\right]$ 上存在 $\\eta\\in\\left(\\dfrac12,1\\right)$ 使
$$
H'(\\eta)=\\frac{H(1)-H(1/2)}{1/2}=-2H\\!\\left(\\frac12\\right).
$$
故
$$
H'(\\xi)+H'(\\eta)=0.
$$
又 $H'(x)=f'(x)-x^2$，所以
$$
f'(\\xi)+f'(\\eta)=\\xi^2+\\eta^2.
$$
结论得证。""",
    },
    {
        "question_number": 22,
        "question_type": "solution",
        "score": 11,
        "module": "线性代数",
        "topics": ["线性方程组", "秩"],
        "page": "page-4.png",
        "question": """设
$$
A=\\begin{pmatrix}
\\lambda & 1 & 1\\\\
0 & \\lambda-1 & 0\\\\
1 & 1 & \\lambda
\\end{pmatrix},
\\qquad
b=\\begin{pmatrix}
a\\\\
1\\\\
1
\\end{pmatrix},
$$
已知线性方程组 $Ax=b$ 存在两个不同的解。  
(I) 求 $\\lambda,a$；  
(II) 求方程组 $Ax=b$ 的通解。""",
        "answer": "$\\lambda=-1,\\ a=-2$；通解为 $x=\\left(\\dfrac32+t,-\\dfrac12,t\\right)^T\\ (t\\in\\mathbb R)$。",
        "explanation": """“存在两个不同的解”说明该方程组有无穷多解，因此
$$
\\det A=0
$$
且增广矩阵与系数矩阵同秩。计算
$$
\\det A=(\\lambda-1)^2(\\lambda+1).
$$
若 $\\lambda=1$，第二行变成 $0=1$，方程组无解，故只能取
$$
\\lambda=-1.
$$
此时方程组为
$$
\\begin{cases}
-x_1+x_2+x_3=a,\\\\
-2x_2=1,\\\\
x_1+x_2-x_3=1.
\\end{cases}
$$
由第二式得 $x_2=-\\dfrac12$。代入第一、三式得
$$
-x_1+x_3=a+\\frac12,\\qquad x_1-x_3=\\frac32.
$$
两式相容需满足
$$
a+\\frac12=-\\frac32,
$$
故
$$
a=-2.
$$
设 $x_3=t$，则
$$
x_1=\\frac32+t,\\qquad x_2=-\\frac12.
$$
故通解为
$$
x=\\begin{pmatrix}\\frac32+t\\\\-\\frac12\\\\t\\end{pmatrix},\\quad t\\in\\mathbb R.
$$""",
    },
    {
        "question_number": 23,
        "question_type": "solution",
        "score": 11,
        "module": "线性代数",
        "topics": ["实对称矩阵", "正交对角化"],
        "page": "page-4.png",
        "question": """设
$$
A=\\begin{pmatrix}
0 & -1 & 4\\\\
-1 & 3 & a\\\\
4 & a & 0
\\end{pmatrix},
$$
正交矩阵 $Q$ 使 $Q^TAQ$ 为对角矩阵，若 $Q$ 的第 $1$ 列为
$$
\\frac{1}{\\sqrt6}(1,2,1)^T,
$$
求 $a,Q$。""",
        "answer": """$a=-1$。可取
$$
Q=\\begin{pmatrix}
\\frac1{\\sqrt6} & \\frac1{\\sqrt2} & \\frac1{\\sqrt3}\\\\
\\frac2{\\sqrt6} & 0 & -\\frac1{\\sqrt3}\\\\
\\frac1{\\sqrt6} & -\\frac1{\\sqrt2} & \\frac1{\\sqrt3}
\\end{pmatrix}.
$$""",
        "explanation": """记
$$
q_1=\\frac1{\\sqrt6}(1,2,1)^T.
$$
由于 $Q^TAQ$ 为对角矩阵，$q_1$ 必是 $A$ 的特征向量。故存在特征值 $\\lambda$ 使
$$
A(1,2,1)^T=\\lambda(1,2,1)^T.
$$
直接计算得
$$
A(1,2,1)^T=(2,5+a,4+2a)^T.
$$
故
$$
2=\\lambda,\\qquad 5+a=2\\lambda,\\qquad 4+2a=\\lambda,
$$
解得
$$
a=-1,\\qquad \\lambda=2.
$$
此时
$$
A=\\begin{pmatrix}
0 & -1 & 4\\\\
-1 & 3 & -1\\\\
4 & -1 & 0
\\end{pmatrix}.
$$
再求与 $q_1$ 正交的两个单位特征向量，可取
$$
q_2=\\frac1{\\sqrt2}(1,0,-1)^T,\\qquad q_3=\\frac1{\\sqrt3}(1,-1,1)^T.
$$
它们分别对应特征值 $-4,5$，且与 $q_1$ 两两正交。于是可取
$$
Q=(q_1,q_2,q_3)
=\\begin{pmatrix}
\\frac1{\\sqrt6} & \\frac1{\\sqrt2} & \\frac1{\\sqrt3}\\\\
\\frac2{\\sqrt6} & 0 & -\\frac1{\\sqrt3}\\\\
\\frac1{\\sqrt6} & -\\frac1{\\sqrt2} & \\frac1{\\sqrt3}
\\end{pmatrix}.
$$""",
    },
]


def card_path(question_number: int) -> Path:
    return QUESTIONS_DIR / f"q{question_number:03d}.md"


def build_frontmatter(item: dict) -> str:
    lines = [
        "---",
        f"question_id: {item['question_id']}",
        f"exam_id: {EXAM_ID}",
        "exam_type: math2",
        f"year: {YEAR}",
        f"question_number: {item['question_number']}",
        f"question_type: {item['question_type']}",
        f"score: {item['score']}",
        f"module: {item['module']}",
        "topics:",
    ]
    for topic in item["topics"]:
        lines.append(f"  - {topic}")
    lines.extend(
        [
            "difficulty: unknown",
            "review_status: reviewed",
            "answer_status: available",
            "explanation_status: available",
            "source_file: math2_2010_questions.md",
            "answer_source_file: math2_2010_answers.md",
            "assets:",
        ]
    )
    for asset in item["assets"]:
        lines.append(f"  - {asset}")
    lines.append("---")
    return "\n".join(lines)


def question_header(item: dict) -> str:
    return f"# 2010 数学二第 {item['question_number']} 题"


def write_card(item: dict) -> None:
    body = [
        build_frontmatter(item),
        "",
        question_header(item),
        "",
        "## 题目",
        "",
        item["question"].rstrip(),
        "",
    ]
    if "images/q018_diagram.png" in item["assets"]:
        body.extend(["![题图](../images/q018_diagram.png)", ""])
    body.extend(
        [
            "## 标准答案",
            "",
            item["answer"],
            "",
            "## 解析",
            "",
            item["explanation"].rstrip(),
            "",
            "## 来源",
            "",
            "- 题目来源：`math2_2010_questions.md`",
            "- 答案来源：`math2_2010_answers.md`",
            "",
        ]
    )
    card_path(item["question_number"]).write_text("\n".join(body), encoding="utf-8")


def build_questions_markdown(items: list[dict]) -> str:
    out = [
        "# 2010 年数学二真题",
        "",
        "资料类型：考研数学二历年真题",
        "年份：2010",
        "科目：数学二",
        "整理状态：按正式题卡整理并校对。",
        "",
        "**第 1-8 题题图**",
        "",
        "![2010 数学二第 1-8 题题图](images/source_pages/page-1.png)",
        "",
        "**第 9-16 题题图**",
        "",
        "![2010 数学二第 9-16 题题图](images/source_pages/page-2.png)",
        "",
        "**第 17-20 题题图**",
        "",
        "![2010 数学二第 17-20 题题图](images/source_pages/page-3.png)",
        "",
        "**第 21-23 题题图**",
        "",
        "![2010 数学二第 21-23 题题图](images/source_pages/page-4.png)",
        "",
    ]
    for item in items:
        out.extend(
            [
                f"## 第 {item['question_number']} 题",
                f"- 题型：{item['question_type']}",
                f"- 分值：{item['score']}",
                f"- 模块：{item['module']}",
                f"- 考点：{'、'.join(item['topics'])}",
                "",
                item["question"].rstrip(),
                "",
            ]
        )
        if "images/q018_diagram.png" in item["assets"]:
            out.extend(["![第 18 题题图](images/q018_diagram.png)", ""])
    return "\n".join(out).rstrip() + "\n"


def build_answers_markdown(items: list[dict]) -> str:
    out = [
        "# Math 2 2010 Answers",
        "",
        "资料类型：考研数学二答案解析",
        "年份：2010",
        "科目：数学二",
        "整理状态：答案与解析按清洗后的正式题卡整理。",
        "",
        "## 答案速查",
        "",
        "| 题号 | 题型 | 答案 |",
        "|---|---|---|",
    ]
    for item in items:
        out.append(f"| {item['question_number']} | {item['question_type']} | {item['answer'].replace('|', '\\|')} |")
    out.extend(["", "## 详细解析", ""])
    for item in items:
        out.extend(
            [
                f"### 第 {item['question_number']} 题",
                f"- 答案：{item['answer']}",
                "",
                item["explanation"].rstrip(),
                "",
            ]
        )
    return "\n".join(out).rstrip() + "\n"


def crop_diagram() -> None:
    image = Image.open(SOURCE_PAGES / "page-3.png")
    # Tight crop around the tank diagram in Q18.
    crop = image.crop((820, 410, 1215, 760))
    crop.save(IMAGES / "q018_diagram.png")


def main() -> None:
    QUESTIONS_DIR.mkdir(parents=True, exist_ok=True)
    crop_diagram()

    items: list[dict] = []
    for raw in QUESTIONS:
        item = deepcopy(raw)
        qn = item["question_number"]
        item["question_id"] = f"{EXAM_ID}_q{qn:03d}"
        item["card_path"] = f"questions/q{qn:03d}.md"
        assets = [f"images/source_pages/{item.pop('page')}"]
        assets.extend(item.pop("assets_extra", []))
        item["assets"] = assets
        write_card(item)
        items.append(item)

    (ROOT / "math2_2010_questions.md").write_text(build_questions_markdown(items), encoding="utf-8")
    (ROOT / "math2_2010_answers.md").write_text(build_answers_markdown(items), encoding="utf-8")

    with (ROOT / "questions.jsonl").open("w", encoding="utf-8") as f:
        for item in items:
            record = {
                "question_id": item["question_id"],
                "exam_id": EXAM_ID,
                "exam_type": "math2",
                "year": YEAR,
                "question_number": item["question_number"],
                "question_type": item["question_type"],
                "score": item["score"],
                "module": item["module"],
                "topics": item["topics"],
                "difficulty": "unknown",
                "review_status": "reviewed",
                "answer_status": "available",
                "explanation_status": "available",
                "source_file": "math2_2010_questions.md",
                "answer_source_file": "math2_2010_answers.md",
                "card_path": item["card_path"],
                "assets": item["assets"],
                "answer": item["answer"],
                "explanation": item["explanation"],
            }
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    manifest = {
        "exam_id": EXAM_ID,
        "exam_type": "math2",
        "exam_label": "数学二",
        "year": YEAR,
        "source_files": {
            "questions": "math2_2010_questions.md",
            "answers": "math2_2010_answers.md",
        },
        "card_dir": "questions",
        "index_file": "questions.jsonl",
        "question_count": len(items),
        "explanation_count": len(items),
        "question_ids": [item["question_id"] for item in items],
        "generated_at": ts(),
        "review_status": "reviewed",
        "answer_status": "available",
        "explanation_status": "available",
    }
    (ROOT / "paper_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
