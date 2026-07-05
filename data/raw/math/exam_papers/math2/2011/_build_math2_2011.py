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

EXAM_ID = "kaoyan_math2_2011"
YEAR = 2011


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


QUESTIONS = [
    {
        "question_number": 1,
        "question_type": "choice",
        "score": 4,
        "module": "高等数学",
        "topics": ["等价无穷小", "Taylor 展开"],
        "page": "page-1.png",
        "question": """已知当 $x\\to0$ 时，函数
$$
f(x)=3\\sin x-\\sin 3x
$$
与 $cx^k$ 是等价无穷小，则（  ）  
A. $k=1,\\ c=4$  
B. $k=1,\\ c=-4$  
C. $k=3,\\ c=4$  
D. $k=3,\\ c=-4$
""",
        "answer": "C",
        "explanation": """由展开式
$$
\\sin x=x-\\frac{x^3}{6}+o(x^3),\\qquad \\sin3x=3x-\\frac{(3x)^3}{6}+o(x^3)
$$
可得
$$
3\\sin x-\\sin3x
=3\\left(x-\\frac{x^3}{6}\\right)-\\left(3x-\\frac{27x^3}{6}\\right)+o(x^3)
=4x^3+o(x^3).
$$
故 $k=3,\\ c=4$。""",
    },
    {
        "question_number": 2,
        "question_type": "choice",
        "score": 4,
        "module": "高等数学",
        "topics": ["导数定义", "极限"],
        "page": "page-1.png",
        "question": """设函数 $f(x)$ 在 $x=0$ 处可导，且 $f(0)=0$，则
$$
\\lim_{x\\to0}\\frac{x^2f(x)-2f(x^3)}{x^3}=（\\ \\ ）
$$
A. $-2f'(0)$  
B. $-f'(0)$  
C. $f'(0)$  
D. $0$
""",
        "answer": "B",
        "explanation": """因为 $f$ 在 $0$ 处可导，且 $f(0)=0$，所以
$$
f(x)=f'(0)x+o(x),\\qquad f(x^3)=f'(0)x^3+o(x^3).
$$
于是
$$
x^2f(x)-2f(x^3)=f'(0)x^3-2f'(0)x^3+o(x^3)=-f'(0)x^3+o(x^3).
$$
因此极限为 $-f'(0)$。""",
    },
    {
        "question_number": 3,
        "question_type": "choice",
        "score": 4,
        "module": "高等数学",
        "topics": ["驻点", "导数"],
        "page": "page-1.png",
        "question": """函数
$$
f(x)=\\ln\\left|(x-1)(x-2)(x-3)\\right|
$$
的驻点个数为（  ）  
A. $0$  
B. $1$  
C. $2$  
D. $3$
""",
        "answer": "C",
        "explanation": """在定义域内
$$
f'(x)=\\frac{1}{x-1}+\\frac{1}{x-2}+\\frac{1}{x-3}.
$$
令 $f'(x)=0$，化简得
$$
3x^2-12x+11=0.
$$
其判别式为 $12>0$，有两个不等实根，并且都落在函数定义域内，所以驻点有 $2$ 个。""",
    },
    {
        "question_number": 4,
        "question_type": "choice",
        "score": 4,
        "module": "高等数学",
        "topics": ["常系数线性微分方程", "特解形式"],
        "page": "page-1.png",
        "question": """微分方程
$$
y''-\\lambda^2y=e^{\\lambda x}+e^{-\\lambda x}\\qquad(\\lambda>0)
$$
的特解形式为（  ）  
A. $a(e^{\\lambda x}+e^{-\\lambda x})$  
B. $ax(e^{\\lambda x}+e^{-\\lambda x})$  
C. $x(ae^{\\lambda x}+be^{-\\lambda x})$  
D. $x^2(ae^{\\lambda x}+be^{-\\lambda x})$
""",
        "answer": "C",
        "explanation": """对应齐次方程的特征方程为
$$
r^2-\\lambda^2=0,
$$
特征根为 $\\pm\\lambda$。右端 $e^{\\lambda x},e^{-\\lambda x}$ 都与齐次解共振，各需乘以 $x$，故特解应取
$$
y_p=x(ae^{\\lambda x}+be^{-\\lambda x}).
$$""",
    },
    {
        "question_number": 5,
        "question_type": "choice",
        "score": 4,
        "module": "高等数学",
        "topics": ["二元函数极值", "充分条件"],
        "page": "page-1.png",
        "question": """设函数 $f(x),g(x)$ 均有二阶连续导数，满足 $f(0)>0,g(0)<0$，且 $f'(0)=g'(0)=0$，则函数
$$
z=f(x)g(y)
$$
在点 $(0,0)$ 处取得极小值的一个充分条件是（  ）  
A. $f''(0)<0,\\ g''(0)>0$  
B. $f''(0)<0,\\ g''(0)<0$  
C. $f''(0)>0,\\ g''(0)>0$  
D. $f''(0)>0,\\ g''(0)<0$
""",
        "answer": "A",
        "explanation": """在 $(0,0)$ 附近作二阶展开：
$$
z=f(x)g(y)=f(0)g(0)+\\frac12 f''(0)g(0)x^2+\\frac12 f(0)g''(0)y^2+o(x^2+y^2).
$$
要使 $(0,0)$ 成为极小值点，二次项系数应都为正。由于 $f(0)>0,g(0)<0$，故应有
$$
f''(0)g(0)>0\\Rightarrow f''(0)<0,
$$
$$
f(0)g''(0)>0\\Rightarrow g''(0)>0.
$$""",
    },
    {
        "question_number": 6,
        "question_type": "choice",
        "score": 4,
        "module": "高等数学",
        "topics": ["定积分比较", "对数函数"],
        "page": "page-1.png",
        "question": """设
$$
I=\\int_0^{\\pi/4}\\ln(\\sin x)\\,dx,\\qquad
J=\\int_0^{\\pi/4}\\ln(\\cot x)\\,dx,\\qquad
K=\\int_0^{\\pi/4}\\ln(\\cos x)\\,dx,
$$
则 $I,J,K$ 的大小规律为（  ）  
A. $I<J<K$  
B. $I<K<J$  
C. $J<I<K$  
D. $K<J<I$
""",
        "answer": "B",
        "explanation": """在 $0<x<\\dfrac\\pi4$ 上，有
$$
0<\\sin x<\\cos x<1.
$$
取对数后得
$$
\\ln(\\sin x)<\\ln(\\cos x)<0,
$$
积分可知 $I<K<0$。又
$$
J=\\int_0^{\\pi/4}[\\ln(\\cos x)-\\ln(\\sin x)]dx=K-I>0.
$$
故
$$
I<K<J.
$$""",
    },
    {
        "question_number": 7,
        "question_type": "choice",
        "score": 4,
        "module": "线性代数",
        "topics": ["初等变换", "矩阵乘法"],
        "page": "page-1.png",
        "question": """设 $A$ 为 $3$ 阶矩阵，将 $A$ 的第 $2$ 列加到第 $1$ 列得矩阵 $B$，再交换 $B$ 的第 $2$ 行与第 $3$ 行得单位矩阵。记
$$
P_1=\\begin{pmatrix}
1&0&0\\\\
1&1&0\\\\
0&0&1
\\end{pmatrix},
\\qquad
P_2=\\begin{pmatrix}
1&0&0\\\\
0&0&1\\\\
0&1&0
\\end{pmatrix},
$$
则
$$
A=（\\ \\ ）
$$
A. $P_1P_2$  
B. $P_1^{-1}P_2$  
C. $P_2P_1$  
D. $P_2P_1^{-1}$
""",
        "answer": "D",
        "explanation": """将第 $2$ 列加到第 $1$ 列，等价于右乘矩阵 $P_1$，故
$$
B=AP_1.
$$
再交换 $B$ 的第 $2,3$ 行得到单位矩阵，等价于左乘 $P_2$，即
$$
P_2B=I.
$$
代入得
$$
P_2AP_1=I\\Rightarrow A=P_2^{-1}P_1^{-1}=P_2P_1^{-1}.
$$""",
    },
    {
        "question_number": 8,
        "question_type": "choice",
        "score": 4,
        "module": "线性代数",
        "topics": ["伴随矩阵", "零空间"],
        "page": "page-1.png",
        "question": """设 $A=(\\alpha_1,\\alpha_2,\\alpha_3,\\alpha_4)$ 是 $4$ 阶矩阵，$A^*$ 为 $A$ 的伴随矩阵。若 $(1,0,1,0)^T$ 是方程组 $Ax=0$ 的一个基础解系，则 $A^*x=0$ 的基础解系可为（  ）  
A. $\\alpha_1,\\alpha_3$  
B. $\\alpha_1,\\alpha_2$  
C. $\\alpha_1,\\alpha_2,\\alpha_3$  
D. $\\alpha_2,\\alpha_3,\\alpha_4$
""",
        "answer": "D",
        "explanation": """由 $Ax=0$ 的基础解系为 $(1,0,1,0)^T$，知
$$
\\alpha_1+\\alpha_3=0,
$$
故 $r(A)=3$。于是 $r(A^*)=1$，从而 $A^*x=0$ 的解空间维数为 $3$。  
又由恒等式
$$
A^*A=O
$$
知 $A$ 的列向量都属于 $A^*x=0$ 的解空间，因此该解空间就是 $A$ 的列空间。由于 $\\alpha_3=-\\alpha_1$，列空间的一组基可取 $\\alpha_2,\\alpha_3,\\alpha_4$。""",
    },
    {
        "question_number": 9,
        "question_type": "fill_blank",
        "score": 4,
        "module": "高等数学",
        "topics": ["极限", "指数极限"],
        "page": "page-1.png",
        "question": """求极限
$$
\\lim_{x\\to0}\\left(\\frac{1+2^x}{2}\\right)^{1/x}=\\underline{\\qquad}.
$$""",
        "answer": "$\\sqrt2$",
        "explanation": """设极限为 $L$，取对数：
$$
\\ln L=\\lim_{x\\to0}\\frac{1}{x}\\ln\\left(\\frac{1+2^x}{2}\\right).
$$
由 $2^x=e^{x\\ln2}=1+x\\ln2+o(x)$，得
$$
\\frac{1+2^x}{2}=1+\\frac{x\\ln2}{2}+o(x).
$$
因此
$$
\\ln L=\\frac{\\ln2}{2},
$$
从而
$$
L=e^{(\\ln2)/2}=\\sqrt2.
$$""",
    },
    {
        "question_number": 10,
        "question_type": "fill_blank",
        "score": 4,
        "module": "高等数学",
        "topics": ["一阶线性微分方程"],
        "page": "page-1.png",
        "question": """微分方程
$$
y'+y=e^{-x}\\cos x
$$
满足条件 $y(0)=0$ 的解为 $y=\\underline{\\qquad}$。""",
        "answer": "$e^{-x}\\sin x$",
        "explanation": """乘以积分因子 $e^x$，得
$$
(e^xy)'=\\cos x.
$$
积分可得
$$
e^xy=\\sin x+C.
$$
由 $y(0)=0$ 知 $C=0$，故
$$
y=e^{-x}\\sin x.
$$""",
    },
    {
        "question_number": 11,
        "question_type": "fill_blank",
        "score": 4,
        "module": "高等数学",
        "topics": ["弧长", "积分"],
        "page": "page-1.png",
        "question": """曲线
$$
y=\\int_0^x\\tan t\\,dt\\qquad\\left(0\\le x\\le\\frac\\pi4\\right)
$$
的弧长 $s=\\underline{\\qquad}$。""",
        "answer": "$\\ln(1+\\sqrt2)$",
        "explanation": """有
$$
y'=\\tan x,
$$
故弧长
$$
s=\\int_0^{\\pi/4}\\sqrt{1+(y')^2}\\,dx=\\int_0^{\\pi/4}\\sec x\\,dx.
$$
积分得
$$
s=\\left.\\ln|\\sec x+\\tan x|\\right|_0^{\\pi/4}=\\ln(1+\\sqrt2).
$$""",
    },
    {
        "question_number": 12,
        "question_type": "fill_blank",
        "score": 4,
        "module": "高等数学",
        "topics": ["广义积分", "概率密度"],
        "page": "page-1.png",
        "question": """设函数
$$
f(x)=
\\begin{cases}
\\lambda e^{-\\lambda x},&x>0,\\ \\lambda>0,\\\\
0,&x\\le0,
\\end{cases}
$$
则
$$
\\int_{-\\infty}^{+\\infty}xf(x)\\,dx=\\underline{\\qquad}.
$$""",
        "answer": "$\\dfrac{1}{\\lambda}$",
        "explanation": """由定义可知
$$
\\int_{-\\infty}^{+\\infty}xf(x)\\,dx=\\int_0^{+\\infty}x\\lambda e^{-\\lambda x}\\,dx.
$$
分部积分或利用指数分布的期望公式，得
$$
\\int_0^{+\\infty}x\\lambda e^{-\\lambda x}\\,dx=\\frac{1}{\\lambda}.
$$""",
    },
    {
        "question_number": 13,
        "question_type": "fill_blank",
        "score": 4,
        "module": "高等数学",
        "topics": ["二重积分", "平面区域"],
        "page": "page-2.png",
        "question": """设平面区域 $D$ 由直线 $y=x$、圆 $x^2+y^2=2y$ 及 $y$ 轴所围成，则二重积分
$$
\\iint_D xy\\,d\\sigma=\\underline{\\qquad}.
$$""",
        "answer": "$\\dfrac{7}{12}$",
        "explanation": """圆可写成
$$
x^2+(y-1)^2=1.
$$
区域由 $x=0$、$y=x$ 和上半圆弧围成，可取积分次序
$$
0\\le x\\le1,\\qquad x\\le y\\le1+\\sqrt{1-x^2}.
$$
因此
$$
\\iint_D xy\\,d\\sigma
=\\int_0^1\\int_x^{1+\\sqrt{1-x^2}}xy\\,dy\\,dx
=\\int_0^1 x\\left(1+\\sqrt{1-x^2}-x^2\\right)dx
=\\frac14+\\frac13=\\frac{7}{12}.
$$""",
    },
    {
        "question_number": 14,
        "question_type": "fill_blank",
        "score": 4,
        "module": "线性代数",
        "topics": ["二次型", "惯性指数"],
        "page": "page-2.png",
        "question": """二次型
$$
f(x_1,x_2,x_3)=x_1^2+3x_2^2+x_3^2+2x_1x_2+2x_1x_3+2x_2x_3
$$
的正惯性指数为 $\\underline{\\qquad}$。""",
        "answer": "$2$",
        "explanation": """对应矩阵为
$$
A=\\begin{pmatrix}
1&1&1\\\\
1&3&1\\\\
1&1&1
\\end{pmatrix}.
$$
其顺序主子式为
$$
\\Delta_1=1>0,\\qquad \\Delta_2=2>0,\\qquad \\Delta_3=0.
$$
再注意到矩阵秩为 $2$，且非零特征值均为正，因此二次型有两个正平方项、一个零平方项，故正惯性指数为 $2$。""",
    },
    {
        "question_number": 15,
        "question_type": "solution",
        "score": 10,
        "module": "高等数学",
        "topics": ["极限", "定积分函数"],
        "page": "page-2.png",
        "question": """已知函数
$$
F(x)=\\frac{\\int_0^x\\ln(1+t^2)\\,dt}{x^{\\alpha}}.
$$
设
$$
\\lim_{x\\to+\\infty}F(x)=\\lim_{x\\to0^+}F(x)=0,
$$
试求 $\\alpha$ 的取值范围。""",
        "answer": "$1<\\alpha<3$",
        "explanation": """先看 $x\\to0^+$。由
$$
\\ln(1+t^2)\\sim t^2
$$
得
$$
\\int_0^x\\ln(1+t^2)dt\\sim\\int_0^x t^2dt=\\frac{x^3}{3}.
$$
故
$$
F(x)\\sim\\frac{x^3/3}{x^\\alpha}=\\frac13x^{3-\\alpha},
$$
要使极限为 $0$，需
$$
3-\\alpha>0\\Rightarrow \\alpha<3.
$$
再看 $x\\to+\\infty$。当 $t$ 大时，$\\ln(1+t^2)\\sim2\\ln t$，从而
$$
\\int_0^x\\ln(1+t^2)dt\\sim 2x\\ln x.
$$
因此
$$
F(x)\\sim 2x^{1-\\alpha}\\ln x.
$$
要使其趋于 $0$，需
$$
\\alpha>1.
$$
综上
$$
1<\\alpha<3.
$$""",
    },
    {
        "question_number": 16,
        "question_type": "solution",
        "score": 11,
        "module": "高等数学",
        "topics": ["参数方程", "极值", "凹凸性"],
        "page": "page-2.png",
        "question": """设函数 $y=y(x)$ 由参数方程
$$
\\begin{cases}
x=\\dfrac13t^3+t+\\dfrac13,\\\\
y=\\dfrac13t^3-t+\\dfrac13
\\end{cases}
$$
确定，求 $y=y(x)$ 的极值和曲线 $y=y(x)$ 的凹凸区间及拐点。""",
        "answer": "极大值为 $1$（在点 $(-1,1)$ 处），极小值为 $-\\dfrac13$（在点 $\\left(\\dfrac53,-\\dfrac13\\right)$ 处）；当 $x<\\dfrac13$ 时曲线凹向下，当 $x>\\dfrac13$ 时曲线凹向上；拐点为 $\\left(\\dfrac13,\\dfrac13\\right)$。",
        "explanation": """有
$$
\\frac{dx}{dt}=t^2+1>0,
$$
故 $x$ 关于 $t$ 单调增加。于是
$$
\\frac{dy}{dx}=\\frac{dy/dt}{dx/dt}=\\frac{t^2-1}{t^2+1}.
$$
令 $\\dfrac{dy}{dx}=0$，得 $t=\\pm1$。代入参数方程：
$$
t=-1\\Rightarrow (x,y)=(-1,1),
$$
$$
t=1\\Rightarrow \\left(x,y\\right)=\\left(\\frac53,-\\frac13\\right).
$$
又
$$
\\frac{d^2y}{dx^2}=\\frac{\\dfrac{d}{dt}\\left(\\dfrac{t^2-1}{t^2+1}\\right)}{dx/dt}
=\\frac{4t}{(t^2+1)^3}.
$$
故当 $t<0$ 时 $\\dfrac{d^2y}{dx^2}<0$，曲线凹向下；当 $t>0$ 时 $\\dfrac{d^2y}{dx^2}>0$，曲线凹向上。  
由 $t=0$ 时
$$
x=y=\\frac13,
$$
知拐点为 $\\left(\\dfrac13,\\dfrac13\\right)$。""",
    },
    {
        "question_number": 17,
        "question_type": "solution",
        "score": 9,
        "module": "高等数学",
        "topics": ["复合函数", "二阶偏导数"],
        "page": "page-2.png",
        "question": """设函数
$$
z=f(xy,yg(x)),
$$
其中函数 $f$ 具有二阶连续偏导数，函数 $g(x)$ 可导且在 $x=1$ 处取得极值 $g(1)=1$，求
$$
\\left.\\frac{\\partial^2 z}{\\partial x\\partial y}\\right|_{x=1,y=1}.
$$""",
        "answer": "$f_u(1,1)+f_{uu}(1,1)+f_{uv}(1,1)$",
        "explanation": """记
$$
u=xy,\\qquad v=yg(x),
$$
则
$$
z=f(u,v).
$$
先对 $x$ 求偏导：
$$
z_x=f_u\\,u_x+f_v\\,v_x=yf_u+y g'(x)f_v.
$$
再对 $y$ 求偏导：
$$
z_{xy}=f_u+y(xf_{uu}+g(x)f_{uv})+g'(x)f_v+y g'(x)(x f_{uv}+g(x)f_{vv}).
$$
由于 $g$ 在 $x=1$ 处取极值且可导，所以
$$
g(1)=1,\\qquad g'(1)=0.
$$
在 $(x,y)=(1,1)$ 处代入，且此时 $(u,v)=(1,1)$，得到
$$
z_{xy}(1,1)=f_u(1,1)+f_{uu}(1,1)+f_{uv}(1,1).
$$""",
    },
    {
        "question_number": 18,
        "question_type": "solution",
        "score": 10,
        "module": "高等数学",
        "topics": ["微分方程", "切线倾角"],
        "page": "page-3.png",
        "question": """设函数 $y(x)$ 具有二阶导数，且曲线 $l:y=y(x)$ 与直线 $y=x$ 相切于原点。记 $\\alpha$ 为曲线 $l$ 在点 $(x,y)$ 处切线的倾角，若
$$
\\frac{d\\alpha}{dx}=\\frac{dy}{dx},
$$
求 $y(x)$ 的表达式。""",
        "answer": "$\\displaystyle y=\\arcsin\\!\\left(\\frac{e^x}{\\sqrt2}\\right)-\\frac\\pi4$",
        "explanation": """设
$$
p=y'.
$$
因为切线倾角 $\\alpha=\\arctan p$，故
$$
\\frac{d\\alpha}{dx}=\\frac{p'}{1+p^2}.
$$
题设给出
$$
\\frac{p'}{1+p^2}=p,
$$
即
$$
p'=p(1+p^2).
$$
又曲线与直线 $y=x$ 相切于原点，所以
$$
y(0)=0,\\qquad p(0)=1.
$$
分离变量：
$$
\\int\\frac{dp}{p(1+p^2)}=\\int dx.
$$
积分得
$$
\\ln p-\\frac12\\ln(1+p^2)=x+C.
$$
由 $p(0)=1$ 可得 $C=-\\dfrac12\\ln2$，化简得
$$
\\frac{p}{\\sqrt{1+p^2}}=\\frac{e^x}{\\sqrt2}.
$$
故
$$
p=y'=\\frac{e^x}{\\sqrt{2-e^{2x}}}.
$$
于是
$$
y=\\int \\frac{e^x}{\\sqrt{2-e^{2x}}}\\,dx
=\\arcsin\\left(\\frac{e^x}{\\sqrt2}\\right)+C_1.
$$
再由 $y(0)=0$ 得
$$
C_1=-\\frac\\pi4.
$$""",
    },
    {
        "question_number": 19,
        "question_type": "solution",
        "score": 10,
        "module": "高等数学",
        "topics": ["不等式证明", "数列收敛"],
        "page": "page-3.png",
        "question": """(I) 证明：对任意的正整数 $n$，都有
$$
\\frac{1}{n+1}<\\ln\\left(1+\\frac1n\\right)<\\frac1n
$$
成立；  
(II) 设
$$
a_n=1+\\frac12+\\cdots+\\frac1n-\\ln n\\qquad(n=1,2,\\ldots),
$$
证明数列 $\\{a_n\\}$ 收敛。""",
        "answer": "结论成立，数列 $\\{a_n\\}$ 收敛。",
        "explanation": """(I) 由函数 $\\dfrac1x$ 在区间 $[n,n+1]$ 上单调递减，
$$
\\frac1{n+1}<\\int_n^{n+1}\\frac{1}{x}\\,dx<\\frac1n.
$$
而
$$
\\int_n^{n+1}\\frac1x\\,dx=\\ln\\left(1+\\frac1n\\right),
$$
故结论成立。  
(II) 考察差分：
$$
a_{n+1}-a_n=\\frac1{n+1}-\\ln\\left(1+\\frac1n\\right).
$$
由 (I) 知
$$
\\frac1{n+1}-\\ln\\left(1+\\frac1n\\right)<0,
$$
故 $\\{a_n\\}$ 单调递减。又由
$$
\\ln n=\\sum_{k=1}^{n-1}\\ln\\left(1+\\frac1k\\right)<\\sum_{k=1}^{n-1}\\frac1k,
$$
得
$$
a_n=\\left(1+\\frac12+\\cdots+\\frac1{n-1}\\right)-\\ln n+\\frac1n>0.
$$
因此 $\\{a_n\\}$ 有下界且单调递减，所以收敛。""",
    },
    {
        "question_number": 20,
        "question_type": "solution",
        "score": 11,
        "module": "高等数学",
        "topics": ["旋转体", "定积分应用", "做功"],
        "page": "page-3.png",
        "assets_extra": ["images/q020_diagram.png"],
        "question": """一容器的内侧是由图中曲线绕 $y$ 轴旋转一周而成的曲面，该曲线由
$$
x^2+y^2=2y\\quad\\left(y\\ge\\frac12\\right)
$$
与
$$
x^2+y^2=1\\quad\\left(y\\le\\frac12\\right)
$$
连接而成。  
(I) 求容器的容积；  
(II) 若将容器内盛满的水从容器顶部全部抽出，至少需要做多少功？（长度单位：m，重力加速度为 $g\\,\\mathrm{m/s^2}$，水的密度为 $10^3\\,\\mathrm{kg/m^3}$。）""",
        "answer": """(I) $V=\\dfrac{9\\pi}{4}$；  
(II) $W=3375\\pi g$。""",
        "explanation": """旋转半径满足
$$
r^2=
\\begin{cases}
1-y^2,&-1\\le y\\le \\dfrac12,\\\\
2y-y^2,&\\dfrac12\\le y\\le2.
\\end{cases}
$$
(I) 容积
$$
V=\\pi\\int_{-1}^{1/2}(1-y^2)dy+\\pi\\int_{1/2}^{2}(2y-y^2)dy
=\\frac{9\\pi}{4}.
$$
(II) 把高度为 $y$ 处的薄层水抽到顶部 $y=2$，需提升距离 $2-y$。故做功
$$
W=10^3 g\\pi\\int_{-1}^{1/2}(2-y)(1-y^2)dy
+10^3 g\\pi\\int_{1/2}^{2}(2-y)(2y-y^2)dy.
$$
计算得
$$
\\int_{-1}^{1/2}(2-y)(1-y^2)dy+\\int_{1/2}^{2}(2-y)(2y-y^2)dy=\\frac{27}{8},
$$
所以
$$
W=10^3g\\pi\\cdot\\frac{27}{8}=3375\\pi g.
$$""",
    },
    {
        "question_number": 21,
        "question_type": "solution",
        "score": 11,
        "module": "高等数学",
        "topics": ["二重积分", "分部积分"],
        "page": "page-4.png",
        "question": """已知函数 $f(x,y)$ 具有二阶连续偏导数，且 $f(1,y)=f(x,1)=0$，
$$
\\iint_D f(x,y)\\,dxdy=a,
$$
其中
$$
D=\\{(x,y)\\mid0\\le x\\le1,\\ 0\\le y\\le1\\},
$$
计算二重积分
$$
I=\\iint_D xyf''_{xy}(x,y)\\,dxdy.
$$""",
        "answer": "$I=a$",
        "explanation": """对 $x$ 分部积分：
$$
I=\\int_0^1 y\\,dy\\int_0^1 x f_{xy}(x,y)\\,dx
=\\int_0^1 y\\left([xf_y(x,y)]_0^1-\\int_0^1 f_y(x,y)dx\\right)dy.
$$
由于 $f(1,y)=0$，所以 $f_y(1,y)=0$，故
$$
I=-\\int_0^1 y\\,dy\\int_0^1 f_y(x,y)dx.
$$
交换积分次序并对 $y$ 再分部积分：
$$
I=-\\int_0^1 dx\\int_0^1 y f_y(x,y)dy
=-\\int_0^1 dx\\left([yf(x,y)]_0^1-\\int_0^1 f(x,y)dy\\right).
$$
又因 $f(x,1)=0$，于是
$$
I=\\int_0^1dx\\int_0^1 f(x,y)dy=\\iint_D f(x,y)dxdy=a.
$$""",
    },
    {
        "question_number": 22,
        "question_type": "solution",
        "score": 11,
        "module": "线性代数",
        "topics": ["向量组", "线性表示"],
        "page": "page-4.png",
        "question": """设向量组
$$
\\alpha_1=(1,0,1)^T,\\quad \\alpha_2=(0,1,1)^T,\\quad \\alpha_3=(1,3,5)^T
$$
不能由向量组
$$
\\beta_1=(1,1,1)^T,\\quad \\beta_2=(1,2,3)^T,\\quad \\beta_3=(3,4,a)^T
$$
线性表示。  
(I) 求 $a$ 的值；  
(II) 将 $\\beta_1,\\beta_2,\\beta_3$ 用 $\\alpha_1,\\alpha_2,\\alpha_3$ 线性表示。""",
        "answer": """(I) $a=5$；  
(II)
$$
\\beta_1=2\\alpha_1+4\\alpha_2-\\alpha_3,\\qquad
\\beta_2=\\alpha_1+2\\alpha_2,\\qquad
\\beta_3=5\\alpha_1+10\\alpha_2-2\\alpha_3.
$$""",
        "explanation": """(I) 若 $\\beta_1,\\beta_2,\\beta_3$ 线性无关，则它们张成 $\\mathbb R^3$，任意三维向量组都能由它们线性表示，这与题意矛盾。因此
$$
\\det(\\beta_1,\\beta_2,\\beta_3)=0.
$$
计算
$$
\\det
\\begin{pmatrix}
1&1&3\\\\
1&2&4\\\\
1&3&a
\\end{pmatrix}
=a-5,
$$
故
$$
a=5.
$$
(II) 设
$$
(\\alpha_1,\\alpha_2,\\alpha_3)
=
\\begin{pmatrix}
1&0&1\\\\
0&1&3\\\\
1&1&5
\\end{pmatrix}.
$$
分别解线性方程组
$$
c_1\\alpha_1+c_2\\alpha_2+c_3\\alpha_3=\\beta_i
$$
即可得到
$$
\\beta_1=2\\alpha_1+4\\alpha_2-\\alpha_3,
$$
$$
\\beta_2=\\alpha_1+2\\alpha_2,
$$
$$
\\beta_3=5\\alpha_1+10\\alpha_2-2\\alpha_3.
$$""",
    },
    {
        "question_number": 23,
        "question_type": "solution",
        "score": 11,
        "module": "线性代数",
        "topics": ["实对称矩阵", "特征值", "矩阵求解"],
        "page": "page-4.png",
        "question": """设 $A$ 为 $3$ 阶实对称矩阵，$A$ 的秩为 $2$，且
$$
A
\\begin{pmatrix}
1&1\\\\
0&0\\\\
-1&1
\\end{pmatrix}
=
\\begin{pmatrix}
-1&1\\\\
0&0\\\\
1&1
\\end{pmatrix}.
$$
(I) 求 $A$ 的所有特征值与特征向量；  
(II) 求矩阵 $A$。""",
        "answer": """(I) 特征值为 $-1,0,1$，对应特征向量可分别取
$$
(1,0,-1)^T,\\ (0,1,0)^T,\\ (1,0,1)^T.
$$
(II)
$$
A=
\\begin{pmatrix}
0&0&1\\\\
0&0&0\\\\
1&0&0
\\end{pmatrix}.
$$""",
        "explanation": """设
$$
u_1=(1,0,-1)^T,\\qquad u_2=(1,0,1)^T.
$$
由题设矩阵等式知
$$
Au_1=-u_1,\\qquad Au_2=u_2,
$$
故 $-1,1$ 是 $A$ 的两个特征值，特征向量分别为 $u_1,u_2$。  
又因 $r(A)=2$，所以 $0$ 也是特征值。由于 $A$ 为实对称矩阵，不同特征值对应的特征向量互相正交，故与 $u_1,u_2$ 都正交的特征向量可取
$$
u_3=(0,1,0)^T.
$$
于是
$$
A=P\\operatorname{diag}(-1,0,1)P^{-1},
$$
其中 $P$ 的列向量取为 $u_1,u_3,u_2$。也可直接利用谱分解：
$$
A=-\\frac{u_1u_1^T}{u_1^Tu_1}+\\frac{u_2u_2^T}{u_2^Tu_2}.
$$
计算得
$$
A=
\\begin{pmatrix}
0&0&1\\\\
0&0&0\\\\
1&0&0
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
            "source_file: math2_2011_questions.md",
            "answer_source_file: math2_2011_answers.md",
            "assets:",
        ]
    )
    for asset in item["assets"]:
        lines.append(f"  - {asset}")
    lines.append("---")
    return "\n".join(lines)


def question_header(item: dict) -> str:
    return f"# 2011 数学二第 {item['question_number']} 题"


def write_card(item: dict) -> None:
    parts = [
        build_frontmatter(item),
        "",
        question_header(item),
        "",
        "## 题目",
        "",
        item["question"].rstrip(),
        "",
    ]
    if "images/q020_diagram.png" in item["assets"]:
        parts.extend(["![题图](../images/q020_diagram.png)", ""])
    parts.extend(
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
            "- 题目来源：`math2_2011_questions.md`",
            "- 答案来源：`math2_2011_answers.md`",
            "",
        ]
    )
    card_path(item["question_number"]).write_text("\n".join(parts), encoding="utf-8")


def build_questions_markdown(items: list[dict]) -> str:
    out = [
        "# 2011 年数学二真题",
        "",
        "资料类型：考研数学二历年真题",
        "年份：2011",
        "科目：数学二",
        "整理状态：按正式题卡整理并校对。",
        "",
        "**第 1-12 题题图**",
        "",
        "![2011 数学二第 1-12 题题图](images/source_pages/page-1.png)",
        "",
        "**第 13-17 题题图**",
        "",
        "![2011 数学二第 13-17 题题图](images/source_pages/page-2.png)",
        "",
        "**第 18-20 题题图**",
        "",
        "![2011 数学二第 18-20 题题图](images/source_pages/page-3.png)",
        "",
        "**第 21-23 题题图**",
        "",
        "![2011 数学二第 21-23 题题图](images/source_pages/page-4.png)",
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
        if "images/q020_diagram.png" in item["assets"]:
            out.extend(["![第 20 题题图](images/q020_diagram.png)", ""])
    return "\n".join(out).rstrip() + "\n"


def build_answers_markdown(items: list[dict]) -> str:
    out = [
        "# Math 2 2011 Answers",
        "",
        "资料类型：考研数学二答案解析",
        "年份：2011",
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
    crop = image.crop((860, 770, 1215, 1235))
    crop.save(IMAGES / "q020_diagram.png")


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

    (ROOT / "math2_2011_questions.md").write_text(build_questions_markdown(items), encoding="utf-8")
    (ROOT / "math2_2011_answers.md").write_text(build_answers_markdown(items), encoding="utf-8")

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
                "source_file": "math2_2011_questions.md",
                "answer_source_file": "math2_2011_answers.md",
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
            "questions": "math2_2011_questions.md",
            "answers": "math2_2011_answers.md",
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
