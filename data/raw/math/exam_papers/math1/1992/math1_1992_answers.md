# Math 1 1992 Answers

资料类型：考研数学一答案解析
年份：1992
科目：数学一
范围：试卷 I
来源：D:\百度网盘\高数资料\【02】1987-2022年数学一真题详解答案（PDF）\1992考研数一真题解析.pdf
校对状态：已按题干和答案页图像重新清洗，去除 OCR 碎行、串题内容和非本题知识点页脚

## 答案速查

| 题号 | 题型 | 答案 |
|---|---|---|
| 1 | 填空题 | $-\dfrac{e^{x+y}-y\sin(xy)}{e^{x+y}-x\sin(xy)}$ |
| 2 | 填空题 | $\dfrac{2}{9}\{1,2,-2\}$ |
| 3 | 填空题 | $\dfrac{\pi^2}{2}$ |
| 4 | 填空题 | $y=x\cos x+C\cos x$，其中 $C$ 为任意常数 |
| 5 | 填空题 | $1$ |
| 6 | 选择题 | D |
| 7 | 选择题 | C |
| 8 | 选择题 | B |
| 9 | 选择题 | C |
| 10 | 选择题 | A |
| 11 | 解答题 | $1$ |
| 12 | 解答题 | $f_{11}''e^{2x}\sin y\cos y+2f_{12}''e^x(y\sin y+x\cos y)+4xyf_{22}''+f_1'e^x\cos y$ |
| 13 | 解答题 | $\dfrac{7}{3}-\dfrac{1}{e}$ |
| 14 | 解答题 | $y=C_1e^x+C_2e^{-3x}-\dfrac{x}{4}e^{-3x}$ |
| 15 | 解答题 | $\dfrac{29}{20}\pi a^5$ |
| 16 | 解答题 | 所证不等式成立。 |
| 17 | 解答题 | $\xi=\dfrac{a}{\sqrt3},\ \eta=\dfrac{b}{\sqrt3},\ \zeta=\dfrac{c}{\sqrt3}$；$W_{\max}=\dfrac{\sqrt3}{9}abc$ |
| 18 | 解答题 | $\alpha_1$ 能由 $\alpha_2,\alpha_3$ 线性表示；$\alpha_4$ 不能由 $\alpha_1,\alpha_2,\alpha_3$ 线性表示 |
| 19 | 解答题 | $\beta=2\xi_1-2\xi_2+\xi_3$；$A^n\beta=\begin{pmatrix}2-2^{n+1}+3^n\\2-2^{n+2}+3^{n+1}\\2-2^{n+3}+3^{n+2}\end{pmatrix}$ |
| 20 | 填空题 | $\dfrac{3}{8}$ |
| 21 | 填空题 | $\dfrac{4}{3}$ |
| 22 | 解答题 | $f_Z(z)=\dfrac{1}{2\pi}\left[\Phi\!\left(\dfrac{z-\mu+\pi}{\sigma}\right)-\Phi\!\left(\dfrac{z-\mu-\pi}{\sigma}\right)\right]$ |

## 详细解析

### 第 1 题

- 答案：$-\dfrac{e^{x+y}-y\sin(xy)}{e^{x+y}-x\sin(xy)}$

由
$$
e^{x+y}+\cos(xy)=0
$$
两边对 $x$ 求导，并把 $y$ 看作 $x$ 的函数，得
$$
e^{x+y}(1+y')-\sin(xy)(y+xy')=0.
$$

整理含 $y'$ 的项：
$$
\bigl(e^{x+y}-x\sin(xy)\bigr)y'
+e^{x+y}-y\sin(xy)=0.
$$

因此
$$
\frac{dy}{dx}
=y'
=-\frac{e^{x+y}-y\sin(xy)}
{e^{x+y}-x\sin(xy)}.
$$

### 第 2 题

- 答案：$\dfrac{2}{9}\{1,2,-2\}$

对
$$
u=\ln(x^2+y^2+z^2)
$$
分别求偏导：
$$
u_x=\frac{2x}{x^2+y^2+z^2},\quad
u_y=\frac{2y}{x^2+y^2+z^2},\quad
u_z=\frac{2z}{x^2+y^2+z^2}.
$$

在 $M(1,2,-2)$ 处，
$$
x^2+y^2+z^2=1+4+4=9.
$$

所以
$$
\operatorname{grad}u\big|_M
=\left\{\frac{2}{9},\frac{4}{9},-\frac{4}{9}\right\}
=\frac{2}{9}\{1,2,-2\}.
$$

### 第 3 题

- 答案：$\dfrac{\pi^2}{2}$

题设函数在 $[-\pi,\pi]$ 上按 $2\pi$ 周期展开。点 $x=\pi$ 是端点，傅里叶级数在该点收敛到周期延拓函数左右极限的平均值：
$$
\frac{f(\pi-0)+f(-\pi+0)}{2}.
$$

由题意
$$
f(\pi-0)=1+\pi^2,\qquad f(-\pi+0)=-1.
$$

故收敛值为
$$
\frac{(1+\pi^2)+(-1)}{2}
=\frac{\pi^2}{2}.
$$

### 第 4 题

- 答案：$y=x\cos x+C\cos x$，其中 $C$ 为任意常数

方程
$$
y'+y\tan x=\cos x
$$
是一阶线性微分方程。在不跨越 $\cos x=0$ 的区间上取积分因子
$$
\mu(x)=e^{\int \tan x\,dx}=\frac{1}{\cos x}.
$$

两边同乘 $\mu(x)$，得
$$
\left(\frac{y}{\cos x}\right)'=1.
$$

积分得
$$
\frac{y}{\cos x}=x+C,
$$
所以通解为
$$
y=x\cos x+C\cos x.
$$

### 第 5 题

- 答案：$1$

矩阵 $A$ 的第 $i$ 行为
$$
a_i(b_1,b_2,\ldots,b_n).
$$

因为每个 $a_i\ne0$，所以所有行都与同一个非零行向量 $(b_1,b_2,\ldots,b_n)$ 成比例，故行秩不超过 $1$。

又因为 $a_i\ne0,\ b_i\ne0$，至少有元素 $a_1b_1\ne0$，矩阵不是零矩阵，故秩至少为 $1$。

因此
$$
r(A)=1.
$$

### 第 6 题

- 答案：D

原式可化为
$$
\frac{x^2-1}{x-1}e^{1/(x-1)}
=(x+1)e^{1/(x-1)}.
$$

当 $x\to1^-$ 时，$1/(x-1)\to-\infty$，故
$$
(x+1)e^{1/(x-1)}\to0.
$$

当 $x\to1^+$ 时，$1/(x-1)\to+\infty$，故
$$
(x+1)e^{1/(x-1)}\to+\infty.
$$

左右极限不同，所以极限不存在；又不是两侧同时趋于无穷大，故选 D。

### 第 7 题

- 答案：C

考察绝对值级数：
$$
\sum_{n=1}^{\infty}\left|(-1)^n\left(1-\cos\frac{\alpha}{n}\right)\right|
=\sum_{n=1}^{\infty}\left(1-\cos\frac{\alpha}{n}\right).
$$

当 $n\to\infty$ 时，
$$
1-\cos\frac{\alpha}{n}
\sim \frac{\alpha^2}{2n^2}.
$$

由于
$$
\sum_{n=1}^{\infty}\frac{1}{n^2}
$$
收敛，比较判别法知原级数绝对收敛，故选 C。

### 第 8 题

- 答案：B

曲线
$$
x=t,\quad y=-t^2,\quad z=t^3
$$
在参数 $t$ 处的切向量为
$$
\tau=(1,-2t,3t^2).
$$

平面 $x+2y+z=4$ 的法向量为
$$
n=(1,2,1).
$$

切线与该平面平行，当且仅当 $\tau\cdot n=0$，即
$$
1-4t+3t^2=0.
$$

解得
$$
t=1,\qquad t=\frac{1}{3}.
$$

因此满足条件的切线共有 2 条，故选 B。

### 第 9 题

- 答案：C

将
$$
x^2|x|=
\begin{cases}
-x^3,&x<0,\\
x^3,&x\ge0
\end{cases}
$$
写成分段形式。由于 $3x^3$ 在任意阶都可导，只需考察 $x^2|x|$ 在 $0$ 处的可导阶数。

设
$$
\varphi(x)=x^2|x|.
$$
则
$$
\varphi'(x)=
\begin{cases}
-3x^2,&x<0,\\
3x^2,&x>0,
\end{cases}
\qquad \varphi'(0)=0,
$$
并且
$$
\varphi''(x)=
\begin{cases}
-6x,&x<0,\\
6x,&x>0,
\end{cases}
\qquad \varphi''(0)=0.
$$

但三阶导数在 $0$ 左右极限分别为 $-6$ 与 $6$，不相等。因此 $f^{(n)}(0)$ 存在的最高阶数为 $2$，故选 C。

### 第 10 题

- 答案：A

若 $\xi_1,\xi_2$ 都是齐次方程组 $Ax=0$ 的解，则 $A\xi_1=0$ 且 $A\xi_2=0$。

两向量
$$
\xi_1=(1,0,2)^T,\qquad \xi_2=(0,1,-1)^T
$$
线性无关，因此零空间维数至少为 $2$。三元齐次方程组满足
$$
\dim N(A)=3-r(A),
$$
故
$$
r(A)\le1.
$$

四个选项中，只有 A 是秩为 $1$ 的行矩阵，且
$$
(-2,1,1)\xi_1=-2+2=0,\qquad
(-2,1,1)\xi_2=1-1=0.
$$

因此选 A。

### 第 11 题

- 答案：$1$

当 $x\to0$ 时，
$$
1-\sqrt{1-x^2}\sim \frac{x^2}{2}.
$$

原极限化为
$$
\lim_{x\to0}
\frac{e^x-\sin x-1}{1-\sqrt{1-x^2}}.
$$
分子、分母均趋于 $0$，连续使用两次洛必达法则：
$$
\lim_{x\to0}
\frac{e^x-\cos x}{x/\sqrt{1-x^2}}
=
\lim_{x\to0}
\frac{e^x+\sin x}{(1-x^2)^{-3/2}}
=1.
$$

因此原极限为
$$
1.
$$

### 第 12 题

- 答案：$f_{11}''e^{2x}\sin y\cos y+2f_{12}''e^x(y\sin y+x\cos y)+4xyf_{22}''+f_1'e^x\cos y$

记
$$
u=e^x\sin y,\qquad v=x^2+y^2,\qquad z=f(u,v).
$$
以下 $f_1',f_2',f_{ij}''$ 均在点 $(u,v)=(e^x\sin y,x^2+y^2)$ 处取值。

先对 $x$ 求偏导：
$$
\frac{\partial z}{\partial x}
=f_1'e^x\sin y+2xf_2'.
$$

再对 $y$ 求偏导：
$$
\frac{\partial^2z}{\partial x\partial y}
=\frac{\partial}{\partial y}\left(f_1'e^x\sin y+2xf_2'\right).
$$

由链式法则，
$$
\frac{\partial f_1'}{\partial y}
=f_{11}''e^x\cos y+2yf_{12}'',
\qquad
\frac{\partial f_2'}{\partial y}
=f_{21}''e^x\cos y+2yf_{22}''.
$$

因此
$$
\begin{aligned}
\frac{\partial^2z}{\partial x\partial y}
&=(f_{11}''e^x\cos y+2yf_{12}'')e^x\sin y
+f_1'e^x\cos y \\
&\quad +2x(f_{21}''e^x\cos y+2yf_{22}'').
\end{aligned}
$$

因 $f$ 具有二阶连续偏导数，$f_{12}''=f_{21}''$，故
$$
\frac{\partial^2z}{\partial x\partial y}
=f_{11}''e^{2x}\sin y\cos y
+2f_{12}''e^x(y\sin y+x\cos y)
+4xyf_{22}''
+f_1'e^x\cos y.
$$

### 第 13 题

- 答案：$\dfrac{7}{3}-\dfrac{1}{e}$

令
$$
t=x-2,\qquad dx=dt.
$$
当 $x=1$ 时，$t=-1$；当 $x=3$ 时，$t=1$。故
$$
\int_1^3 f(x-2)\,dx=\int_{-1}^{1}f(t)\,dt.
$$

由分段定义，
$$
\int_{-1}^{1}f(t)\,dt
=\int_{-1}^{0}(1+t^2)\,dt+\int_0^1 e^{-t}\,dt.
$$

计算得
$$
\int_{-1}^{0}(1+t^2)\,dt=\left(t+\frac{t^3}{3}\right)\bigg|_{-1}^{0}
=\frac{4}{3},
$$
且
$$
\int_0^1 e^{-t}\,dt=1-\frac{1}{e}.
$$

因此
$$
\int_1^3 f(x-2)\,dx
=\frac{4}{3}+1-\frac{1}{e}
=\frac{7}{3}-\frac{1}{e}.
$$

### 第 14 题

- 答案：$y=C_1e^x+C_2e^{-3x}-\dfrac{x}{4}e^{-3x}$

齐次方程
$$
y''+2y'-3y=0
$$
的特征方程为
$$
r^2+2r-3=0,
$$
即
$$
(r-1)(r+3)=0.
$$
故齐次通解为
$$
y_h=C_1e^x+C_2e^{-3x}.
$$

非齐次项 $e^{-3x}$ 对应的指数 $-3$ 是特征根，设特解为
$$
y_p=Axe^{-3x}.
$$
代入原方程得
$$
-4Ae^{-3x}=e^{-3x},
$$
所以
$$
A=-\frac{1}{4}.
$$

因此通解为
$$
y=C_1e^x+C_2e^{-3x}-\frac{x}{4}e^{-3x}.
$$

### 第 15 题

- 答案：$\dfrac{29}{20}\pi a^5$

记
$$
P=x^3+az^2,\quad Q=y^3+ax^2,\quad R=z^3+ay^2.
$$
则
$$
\frac{\partial P}{\partial x}
+\frac{\partial Q}{\partial y}
+\frac{\partial R}{\partial z}
=3(x^2+y^2+z^2).
$$

曲面 $\Sigma$ 是上半球面，不封闭。补上圆盘
$$
S:\ z=0,\quad x^2+y^2\le a^2,
$$
取向向下，使 $S$ 与 $\Sigma$ 围成上半球区域 $\Omega$ 的外侧边界。由高斯公式，
$$
I+I_S
=3\iiint_{\Omega}(x^2+y^2+z^2)\,dV.
$$

右端用球坐标计算：
$$
3\iiint_{\Omega}(x^2+y^2+z^2)\,dV
=3\int_0^{2\pi}d\theta\int_0^{\pi/2}\sin\varphi\,d\varphi
\int_0^a \rho^4\,d\rho
=\frac{6}{5}\pi a^5.
$$

在辅助圆盘 $S$ 上，$z=0$，且向下取向。只有 $R\,dx\,dy$ 项有贡献，并因取向向下得到
$$
I_S
=-\iint_{x^2+y^2\le a^2} ay^2\,dx\,dy.
$$

用极坐标计算：
$$
I_S
=-a\int_0^{2\pi}\sin^2\theta\,d\theta\int_0^a r^3\,dr
=-\frac{\pi}{4}a^5.
$$

因此
$$
I=\frac{6}{5}\pi a^5-I_S
=\frac{6}{5}\pi a^5+\frac{\pi}{4}a^5
=\frac{29}{20}\pi a^5.
$$

### 第 16 题

- 答案：所证不等式成立。

固定 $x_1>0$，对 $x>0$ 构造函数
$$
\varphi(x)=f(x_1)+f(x)-f(x_1+x).
$$

因为 $f''(x)<0$，所以 $f'(x)$ 严格单调递减。于是当 $x>0$ 时，
$$
x<x_1+x,
$$
从而
$$
f'(x)>f'(x_1+x).
$$

因此
$$
\varphi'(x)=f'(x)-f'(x_1+x)>0.
$$

又由 $f(0)=0$，
$$
\varphi(0)=f(x_1)+f(0)-f(x_1)=0.
$$

所以对任意 $x_2>0$，有
$$
\varphi(x_2)>0.
$$

即
$$
f(x_1)+f(x_2)-f(x_1+x_2)>0,
$$
故
$$
f(x_1+x_2)<f(x_1)+f(x_2).
$$

### 第 17 题

- 答案：$\xi=\dfrac{a}{\sqrt3},\ \eta=\dfrac{b}{\sqrt3},\ \zeta=\dfrac{c}{\sqrt3}$；$W_{\max}=\dfrac{\sqrt3}{9}abc$

设从原点到
$$
M(\xi,\eta,\zeta)
$$
的直线段参数方程为
$$
x=\xi t,\qquad y=\eta t,\qquad z=\zeta t,\qquad 0\le t\le1.
$$

则
$$
dx=\xi\,dt,\quad dy=\eta\,dt,\quad dz=\zeta\,dt.
$$

功为
$$
\begin{aligned}
W
&=\int_L yz\,dx+zx\,dy+xy\,dz\\
&=\int_0^1
\bigl(\eta\zeta t^2\xi+\zeta\xi t^2\eta+\xi\eta t^2\zeta\bigr)\,dt\\
&=3\xi\eta\zeta\int_0^1t^2\,dt
=\xi\eta\zeta.
\end{aligned}
$$

因此问题化为在约束
$$
\frac{\xi^2}{a^2}+\frac{\eta^2}{b^2}+\frac{\zeta^2}{c^2}=1,\qquad
\xi,\eta,\zeta\ge0
$$
下求 $\xi\eta\zeta$ 的最大值。

作拉格朗日函数
$$
L=\xi\eta\zeta+\lambda\left(
\frac{\xi^2}{a^2}+\frac{\eta^2}{b^2}+\frac{\zeta^2}{c^2}-1
\right).
$$

对 $\xi,\eta,\zeta$ 求偏导并令其为零。内点最大值满足
$$
\frac{\xi^2}{a^2}
=\frac{\eta^2}{b^2}
=\frac{\zeta^2}{c^2}.
$$

代回约束得
$$
\xi=\frac{a}{\sqrt3},\qquad
\eta=\frac{b}{\sqrt3},\qquad
\zeta=\frac{c}{\sqrt3}.
$$

边界上至少有一个变量为 $0$，此时 $W=0$；内点取值为正，故最大值在上述点取得：
$$
W_{\max}
=\frac{a}{\sqrt3}\frac{b}{\sqrt3}\frac{c}{\sqrt3}
=\frac{\sqrt3}{9}abc.
$$

### 第 18 题

- 答案：$\alpha_1$ 能由 $\alpha_2,\alpha_3$ 线性表示；$\alpha_4$ 不能由 $\alpha_1,\alpha_2,\alpha_3$ 线性表示

因为向量组
$$
\alpha_2,\alpha_3,\alpha_4
$$
线性无关，所以其任意子组也线性无关，特别地，$\alpha_2,\alpha_3$ 线性无关。

又已知
$$
\alpha_1,\alpha_2,\alpha_3
$$
线性相关，故存在不全为零的数 $k_1,k_2,k_3$，使
$$
k_1\alpha_1+k_2\alpha_2+k_3\alpha_3=0.
$$

若 $k_1=0$，则
$$
k_2\alpha_2+k_3\alpha_3=0,
$$
这会推出 $\alpha_2,\alpha_3$ 线性相关，矛盾。因此 $k_1\ne0$，从而
$$
\alpha_1=-\frac{k_2}{k_1}\alpha_2-\frac{k_3}{k_1}\alpha_3.
$$
所以 $\alpha_1$ 能由 $\alpha_2,\alpha_3$ 线性表示。

下面证明 $\alpha_4$ 不能由 $\alpha_1,\alpha_2,\alpha_3$ 线性表示。若能表示，设
$$
\alpha_4=l_1\alpha_1+l_2\alpha_2+l_3\alpha_3.
$$

由于上面已证 $\alpha_1$ 可由 $\alpha_2,\alpha_3$ 线性表示，代入后可得 $\alpha_4$ 也能由 $\alpha_2,\alpha_3$ 线性表示。于是
$$
\alpha_2,\alpha_3,\alpha_4
$$
线性相关，这与已知矛盾。

因此 $\alpha_4$ 不能由 $\alpha_1,\alpha_2,\alpha_3$ 线性表示。

### 第 19 题

- 答案：$\beta=2\xi_1-2\xi_2+\xi_3$；$A^n\beta=\begin{pmatrix}2-2^{n+1}+3^n\\2-2^{n+2}+3^{n+1}\\2-2^{n+3}+3^{n+2}\end{pmatrix}$

设
$$
\beta=x_1\xi_1+x_2\xi_2+x_3\xi_3.
$$
即
$$
x_1
\begin{pmatrix}1\\1\\1\end{pmatrix}
+x_2
\begin{pmatrix}1\\2\\4\end{pmatrix}
+x_3
\begin{pmatrix}1\\3\\9\end{pmatrix}
=
\begin{pmatrix}1\\1\\3\end{pmatrix}.
$$

解此方程组得
$$
x_1=2,\qquad x_2=-2,\qquad x_3=1.
$$
所以
$$
\beta=2\xi_1-2\xi_2+\xi_3.
$$

因为
$$
A\xi_i=\lambda_i\xi_i\quad (i=1,2,3),
$$
所以
$$
A^n\xi_i=\lambda_i^n\xi_i.
$$

于是
$$
\begin{aligned}
A^n\beta
&=2A^n\xi_1-2A^n\xi_2+A^n\xi_3\\
&=2\cdot1^n\xi_1-2\cdot2^n\xi_2+3^n\xi_3.
\end{aligned}
$$

代入三个特征向量，得
$$
A^n\beta
=
\begin{pmatrix}
2-2^{n+1}+3^n\\
2-2^{n+2}+3^{n+1}\\
2-2^{n+3}+3^{n+2}
\end{pmatrix}.
$$

### 第 20 题

- 答案：$\dfrac{3}{8}$

由 $P(AB)=0$ 可知
$$
P(ABC)=0.
$$

利用容斥公式：
$$
\begin{aligned}
P(A\cup B\cup C)
&=P(A)+P(B)+P(C)-P(AB)-P(AC)-P(BC)+P(ABC)\\
&=\frac{1}{4}+\frac{1}{4}+\frac{1}{4}-0-\frac{1}{16}-\frac{1}{16}+0\\
&=\frac{5}{8}.
\end{aligned}
$$

事件 $A,B,C$ 全不发生，即
$$
\overline{A}\,\overline{B}\,\overline{C}
=\overline{A\cup B\cup C}.
$$

因此
$$
P(\overline{A}\,\overline{B}\,\overline{C})
=1-\frac{5}{8}
=\frac{3}{8}.
$$

### 第 21 题

- 答案：$\dfrac{4}{3}$

参数为 $1$ 的指数分布密度为
$$
f_X(x)=
\begin{cases}
e^{-x},&x>0,\\
0,&x\le0.
\end{cases}
$$

所以
$$
E(X+e^{-2X})
=\int_0^\infty (x+e^{-2x})e^{-x}\,dx.
$$

分开计算：
$$
\int_0^\infty xe^{-x}\,dx=1,
\qquad
\int_0^\infty e^{-3x}\,dx=\frac{1}{3}.
$$

因此
$$
E(X+e^{-2X})=1+\frac{1}{3}=\frac{4}{3}.
$$

### 第 22 题

- 答案：$f_Z(z)=\dfrac{1}{2\pi}\left[\Phi\!\left(\dfrac{z-\mu+\pi}{\sigma}\right)-\Phi\!\left(\dfrac{z-\mu-\pi}{\sigma}\right)\right]$

由于 $X$ 与 $Y$ 独立，且 $Y$ 在 $[-\pi,\pi]$ 上均匀分布，
$$
f_Y(y)=
\begin{cases}
\dfrac{1}{2\pi},&-\pi\le y\le\pi,\\
0,&\text{其他}.
\end{cases}
$$

又
$$
X\sim N(\mu,\sigma^2),
$$
故
$$
f_X(x)=\frac{1}{\sigma}\varphi\left(\frac{x-\mu}{\sigma}\right),
$$
其中
$$
\varphi(t)=\frac{1}{\sqrt{2\pi}}e^{-t^2/2}
$$
为标准正态密度。

由独立随机变量和的卷积公式，
$$
f_Z(z)=\int_{-\infty}^{\infty}f_X(z-y)f_Y(y)\,dy
=\frac{1}{2\pi}\int_{-\pi}^{\pi}
\frac{1}{\sigma}\varphi\left(\frac{z-y-\mu}{\sigma}\right)\,dy.
$$

令
$$
t=\frac{z-y-\mu}{\sigma},
$$
则 $dy=-\sigma\,dt$。当 $y=-\pi$ 时，
$$
t=\frac{z+\pi-\mu}{\sigma};
$$
当 $y=\pi$ 时，
$$
t=\frac{z-\pi-\mu}{\sigma}.
$$

因此
$$
\begin{aligned}
f_Z(z)
&=\frac{1}{2\pi}
\int_{(z-\pi-\mu)/\sigma}^{(z+\pi-\mu)/\sigma}\varphi(t)\,dt\\
&=\frac{1}{2\pi}
\left[
\Phi\left(\frac{z-\mu+\pi}{\sigma}\right)
-\Phi\left(\frac{z-\mu-\pi}{\sigma}\right)
\right].
\end{aligned}
$$
