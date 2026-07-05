# Math 1 1994 Answers

资料类型：考研数学一答案解析
年份：1994
科目：数学一
范围：试卷 I
来源：D:\百度网盘\高数资料\【02】1987-2022年数学一真题详解答案（PDF）\1994考研数学一真题解析.pdf
校对状态：reviewed（已按原卷题干、答案页图像和现有解析清洗核对）

## 答案速查

| 题号 | 题型 | 答案 |
|---|---|---|
| 1 | 填空题 | $\dfrac{1}{6}$ |
| 2 | 填空题 | $2x+y-4=0$ |
| 3 | 填空题 | $\dfrac{\pi^2}{e^2}$ |
| 4 | 填空题 | $\dfrac{\pi R^4}{4}\left(\dfrac{1}{a^2}+\dfrac{1}{b^2}\right)$ |
| 5 | 填空题 | $3^{\,n-1}A$ |
| 6 | 选择题 | D |
| 7 | 选择题 | D |
| 8 | 选择题 | C |
| 9 | 选择题 | D |
| 10 | 选择题 | C |
| 11 | 解答题 | $\dfrac{dy}{dx}=\sqrt{\dfrac{\pi}{2}},\quad \dfrac{d^2y}{dx^2}=-\dfrac{1}{\sqrt{2\pi}}$ |
| 12 | 解答题 | $\displaystyle \sum_{n=1}^{\infty}\dfrac{x^{4n+1}}{4n+1},\quad \lvert x\rvert<1$ |
| 13 | 解答题 | $\dfrac{1}{8}\left[\ln\lvert1-\cos x\rvert-\ln\lvert1+\cos x\rvert+\dfrac{2}{1+\cos x}\right]+C$ |
| 14 | 解答题 | $\dfrac{\pi^2R}{2}$ |
| 15 | 解答题 | $f(x)=2\cos x+\sin x+x^2-2$，通解为 $\dfrac{1}{2}x^2y^2+2xy+y(\cos x-2\sin x)=C$ |
| 16 | 证明题 | 级数 $\displaystyle\sum_{n=1}^{\infty}f\left(\dfrac{1}{n}\right)$ 绝对收敛 |
| 17 | 解答题 | $\dfrac{2\pi}{3}$ |
| 18 | 解答题 | （I）的基础解系可取 $(0,0,1,0)^T,\ (-1,1,0,1)^T$；非零公共解为 $k(1,-1,-1,-1)^T,\ k\ne0$ |
| 19 | 证明题 | 结论成立，即 $\lvert A\rvert\ne0$ |
| 20 | 填空题 | $P(B)=1-p$ |
| 21 | 填空题 | $P\{Z=0\}=\dfrac{1}{4},\quad P\{Z=1\}=\dfrac{3}{4}$ |
| 22 | 解答题 | $E(Z)=\dfrac{1}{3},\quad D(Z)=3,\quad \rho_{XZ}=0$，且 $X$ 与 $Z$ 相互独立 |

## 详细解析

### 第 1 题

**答案：** $\dfrac{1}{6}$

原式可化为
$$
\cot x\left(\frac{1}{\sin x}-\frac{1}{x}\right)
=\frac{\cos x(x-\sin x)}{x\sin^2x}.
$$

当 $x\to0$ 时，
$$
\cos x\to1,\qquad x-\sin x\sim\frac{x^3}{6},\qquad \sin x\sim x.
$$

因此
$$
\lim_{x\to0}\frac{\cos x(x-\sin x)}{x\sin^2x}
=\frac{1}{6}.
$$

### 第 2 题

**答案：** $2x+y-4=0$

设
$$
F(x,y,z)=z-e^z+2xy-3.
$$

曲面 $F(x,y,z)=0$ 在点 $(1,2,0)$ 处的法向量为
$$
\nabla F(1,2,0)
=\bigl(2y,2x,1-e^z\bigr)\big|_{(1,2,0)}
=(4,2,0).
$$

切平面过点 $(1,2,0)$，故
$$
4(x-1)+2(y-2)=0,
$$
即
$$
2x+y-4=0.
$$

### 第 3 题

**答案：** $\dfrac{\pi^2}{e^2}$

先对 $y$ 求偏导：
$$
u_y=e^{-x}\cos\frac{x}{y}\left(-\frac{x}{y^2}\right).
$$

于是
$$
\frac{\partial^2u}{\partial x\,\partial y}
=\frac{\partial}{\partial x}
\left[-\frac{x}{y^2}e^{-x}\cos\frac{x}{y}\right].
$$

在点 $\left(2,\dfrac{1}{\pi}\right)$ 处，有 $\cos(2\pi)=1,\ \sin(2\pi)=0$，所以
$$
\frac{\partial^2u}{\partial x\,\partial y}\bigg|_{\left(2,\frac{1}{\pi}\right)}
=\pi^2e^{-2}(2-1)
=\frac{\pi^2}{e^2}.
$$

### 第 4 题

**答案：** $\dfrac{\pi R^4}{4}\left(\dfrac{1}{a^2}+\dfrac{1}{b^2}\right)$

在极坐标下，$x=r\cos\theta,\ y=r\sin\theta$，$0\le r\le R,\ 0\le\theta\le2\pi$。原积分为
$$
\int_0^{2\pi}\int_0^R
r^2\left(\frac{\cos^2\theta}{a^2}+\frac{\sin^2\theta}{b^2}\right)r\,dr\,d\theta.
$$

又
$$
\int_0^R r^3\,dr=\frac{R^4}{4},\qquad
\int_0^{2\pi}\cos^2\theta\,d\theta
=\int_0^{2\pi}\sin^2\theta\,d\theta=\pi.
$$

故
$$
\iint_D\left(\frac{x^2}{a^2}+\frac{y^2}{b^2}\right)\,dx\,dy
=\frac{\pi R^4}{4}\left(\frac{1}{a^2}+\frac{1}{b^2}\right).
$$

### 第 5 题

**答案：** $3^{\,n-1}A$

记
$$
\alpha=(1,2,3),\qquad \beta=\left(1,\frac{1}{2},\frac{1}{3}\right),
$$
则
$$
A=\alpha^T\beta.
$$

由矩阵乘法结合律，
$$
\beta\alpha^T=1+1+1=3,
$$
因此
$$
A^2=(\alpha^T\beta)(\alpha^T\beta)
=\alpha^T(\beta\alpha^T)\beta=3A.
$$

归纳可得
$$
A^n=3^{\,n-1}A\qquad(n=1,2,\ldots).
$$

即
$$
A^n=3^{\,n-1}
\begin{pmatrix}
1&\frac{1}{2}&\frac{1}{3}\\
2&1&\frac{2}{3}\\
3&\frac{3}{2}&1
\end{pmatrix}.
$$

### 第 6 题

**答案：** D

三个积分的积分区间均关于原点对称。$M$ 的被积函数
$$
\frac{\sin x}{1+x^2}\cos^4x
$$
是奇函数，故
$$
M=0.
$$

对 $N$，$\sin^3x$ 为奇函数，$\cos^4x$ 为非负偶函数，且不恒为零，所以
$$
N=\int_{-\pi/2}^{\pi/2}\cos^4x\,dx>0.
$$

对 $P$，$x^2\sin^3x$ 为奇函数，于是
$$
P=-\int_{-\pi/2}^{\pi/2}\cos^4x\,dx<0.
$$

因此
$$
P<M<N.
$$

故选 D。

### 第 7 题

**答案：** D

偏导数存在不能推出函数连续。例如定义
$$
f(x,y)=
\begin{cases}
\dfrac{xy}{x^2+y^2},&(x,y)\ne(0,0),\\
0,&(x,y)=(0,0),
\end{cases}
$$
则 $f_x(0,0)$ 与 $f_y(0,0)$ 都存在，但 $f(x,y)$ 沿 $y=x$ 趋于 $\dfrac{1}{2}$，故在原点不连续。

反过来，函数连续也不能推出偏导数存在。例如
$$
f(x,y)=\sqrt{x^2+y^2}
$$
在 $(0,0)$ 连续，但 $f_x(0,0)$ 不存在。

所以偏导数存在既非连续的充分条件，也非必要条件，选 D。

### 第 8 题

**答案：** C

考察绝对值级数
$$
\sum_{n=1}^{\infty}\frac{|a_n|}{\sqrt{n^2+\lambda}}.
$$

由柯西不等式，
$$
\sum_{n=1}^{\infty}\frac{|a_n|}{\sqrt{n^2+\lambda}}
\le
\left(\sum_{n=1}^{\infty}a_n^2\right)^{1/2}
\left(\sum_{n=1}^{\infty}\frac{1}{n^2+\lambda}\right)^{1/2}.
$$

题设给出 $\sum a_n^2$ 收敛；又 $\lambda>0$，故
$$
0<\frac{1}{n^2+\lambda}<\frac{1}{n^2},
$$
从而 $\sum\dfrac{1}{n^2+\lambda}$ 收敛。于是原级数绝对收敛，选 C。

### 第 9 题

**答案：** D

当 $x\to0$ 时，
$$
\tan x\sim x,\qquad 1-\cos x\sim\frac{x^2}{2},
$$
且
$$
\ln(1-2x)\sim -2x,\qquad 1-e^{-x^2}\sim x^2.
$$

若 $c=0$，由 $a^2+c^2\ne0$ 得 $a\ne0$，分母为二阶无穷小而分子有一阶主项，极限不可能为 $2$；若 $a=0$ 且 $c\ne0$，极限为 $0$。故必须由一阶主项决定极限：
$$
\lim_{x\to0}\frac{a\tan x+b(1-\cos x)}
{c\ln(1-2x)+d(1-e^{-x^2})}
=\frac{a}{-2c}=2.
$$

所以
$$
a=-4c.
$$

故选 D。

### 第 10 题

**答案：** C

由于 $\alpha_1,\alpha_2,\alpha_3,\alpha_4$ 线性无关，变换后的向量组是否线性无关，只需看相对于原向量组的系数矩阵是否可逆。

选项 C 对应的系数矩阵可写为
$$
\begin{pmatrix}
1&0&0&-1\\
1&1&0&0\\
0&1&1&0\\
0&0&1&1
\end{pmatrix},
$$
其行列式为
$$
\begin{vmatrix}
1&0&0&-1\\
1&1&0&0\\
0&1&1&0\\
0&0&1&1
\end{vmatrix}=2\ne0.
$$

因此 C 中向量组线性无关。其余选项可分别写出非平凡线性关系，例如 A 中
$$
(\alpha_1+\alpha_2)-(\alpha_2+\alpha_3)+(\alpha_3+\alpha_4)-(\alpha_4+\alpha_1)=0,
$$
B、D 也类似线性相关。故选 C。

### 第 11 题

**答案：** $\dfrac{dy}{dx}=\sqrt{\dfrac{\pi}{2}},\quad \dfrac{d^2y}{dx^2}=-\dfrac{1}{\sqrt{2\pi}}$

由
$$
x=\cos(t^2)
$$
得
$$
\frac{dx}{dt}=-2t\sin(t^2).
$$

再对
$$
y=t\cos(t^2)-\int_1^{t^2}\frac{1}{2\sqrt u}\cos u\,du
$$
求导。由于 $t>0$，
$$
\frac{d}{dt}\int_1^{t^2}\frac{1}{2\sqrt u}\cos u\,du
=\frac{1}{2t}\cos(t^2)\cdot2t
=\cos(t^2).
$$

所以
$$
\frac{dy}{dt}
=\cos(t^2)-2t^2\sin(t^2)-\cos(t^2)
=-2t^2\sin(t^2).
$$

于是
$$
\frac{dy}{dx}
=\frac{dy/dt}{dx/dt}=t.
$$

在 $t=\sqrt{\dfrac{\pi}{2}}$ 时，
$$
\frac{dy}{dx}=\sqrt{\frac{\pi}{2}}.
$$

二阶导数为
$$
\frac{d^2y}{dx^2}
=\frac{d}{dt}\left(\frac{dy}{dx}\right)\bigg/\frac{dx}{dt}
=\frac{1}{-2t\sin(t^2)}.
$$

代入 $t=\sqrt{\dfrac{\pi}{2}}$，有 $\sin(t^2)=\sin\dfrac{\pi}{2}=1$，故
$$
\frac{d^2y}{dx^2}
=-\frac{1}{2\sqrt{\pi/2}}
=-\frac{1}{\sqrt{2\pi}}.
$$

### 第 12 题

**答案：** $\displaystyle \sum_{n=1}^{\infty}\dfrac{x^{4n+1}}{4n+1},\quad \lvert x\rvert<1$

先求导：
$$
f'(x)=\frac{1}{2(1-x^2)}+\frac{1}{2(1+x^2)}-1
=\frac{1}{1-x^4}-1
=\frac{x^4}{1-x^4}.
$$

当 $\lvert x\rvert<1$ 时，
$$
\frac{x^4}{1-x^4}=\sum_{n=1}^{\infty}x^{4n}.
$$

又 $f(0)=0$，逐项积分得
$$
f(x)=\int_0^x\sum_{n=1}^{\infty}t^{4n}\,dt
=\sum_{n=1}^{\infty}\frac{x^{4n+1}}{4n+1}.
$$

因此
$$
f(x)=\sum_{n=1}^{\infty}\frac{x^{4n+1}}{4n+1},\qquad \lvert x\rvert<1.
$$

### 第 13 题

**答案：** $\dfrac{1}{8}\left[\ln\lvert1-\cos x\rvert-\ln\lvert1+\cos x\rvert+\dfrac{2}{1+\cos x}\right]+C$

由
$$
\sin2x+2\sin x=2\sin x(1+\cos x)
$$
可得
$$
\int\frac{dx}{\sin2x+2\sin x}
=\int\frac{dx}{2\sin x(1+\cos x)}.
$$

令 $u=\cos x$，则 $du=-\sin x\,dx$，且 $\sin^2x=1-u^2$。于是
$$
\int\frac{dx}{2\sin x(1+\cos x)}
=-\frac{1}{2}\int\frac{du}{(1-u^2)(1+u)}
=-\frac{1}{2}\int\frac{du}{(1-u)(1+u)^2}.
$$

作部分分式分解：
$$
\frac{1}{(1-u)(1+u)^2}
=\frac{1}{4}\frac{1}{1-u}
+\frac{1}{4}\frac{1}{1+u}
+\frac{1}{2}\frac{1}{(1+u)^2}.
$$

积分并代回 $u=\cos x$，得
$$
\frac{1}{8}\left[
\ln\lvert1-\cos x\rvert-\ln\lvert1+\cos x\rvert
+\frac{2}{1+\cos x}
\right]+C.
$$

### 第 14 题

**答案：** $\dfrac{\pi^2R}{2}$

记
$$
I=\iint_S \frac{x\,dy\,dz+z^2\,dx\,dy}{x^2+y^2+z^2}.
$$

上下底面关于 $xy$ 平面对称，$z^2\,dx\,dy$ 项在上下底面取相反方向而相互抵消；圆柱侧面上 $dx\,dy=0$。因此只需计算圆柱侧面的
$$
\iint_S \frac{x}{x^2+y^2+z^2}\,dy\,dz.
$$

圆柱侧面取参数
$$
x=R\cos\theta,\qquad y=R\sin\theta,\qquad -R\le z\le R,\quad 0\le\theta\le2\pi.
$$

按外侧取向，
$$
dy\,dz=R\cos\theta\,d\theta\,dz,
$$
且 $x^2+y^2=R^2$，所以
$$
\begin{aligned}
I
&=\int_{-R}^{R}\int_0^{2\pi}
\frac{R\cos\theta}{R^2+z^2}\,R\cos\theta\,d\theta\,dz\\
&=R^2\int_{-R}^{R}\frac{dz}{R^2+z^2}
\int_0^{2\pi}\cos^2\theta\,d\theta\\
&=\pi R^2\int_{-R}^{R}\frac{dz}{R^2+z^2}\\
&=\pi R^2\cdot\frac{1}{R}\left[\arctan\frac{z}{R}\right]_{-R}^{R}\\
&=\frac{\pi^2R}{2}.
\end{aligned}
$$

### 第 15 题

**答案：** $f(x)=2\cos x+\sin x+x^2-2$，通解为 $\dfrac{1}{2}x^2y^2+2xy+y(\cos x-2\sin x)=C$

记
$$
M(x,y)=xy(x+y)-f(x)y,\qquad N(x,y)=f'(x)+x^2y.
$$

方程为全微分方程，故
$$
\frac{\partial M}{\partial y}=\frac{\partial N}{\partial x}.
$$

计算得
$$
\frac{\partial M}{\partial y}=x^2+2xy-f(x),\qquad
\frac{\partial N}{\partial x}=f''(x)+2xy.
$$

于是
$$
f''(x)+f(x)=x^2.
$$

结合 $f(0)=0,\ f'(0)=1$，解初值问题
$$
\begin{cases}
f''+f=x^2,\\
f(0)=0,\quad f'(0)=1,
\end{cases}
$$
得
$$
f(x)=2\cos x+\sin x+x^2-2.
$$

代回后，
$$
M\,dx+N\,dy
=d\left[\frac{1}{2}x^2y^2+2xy+y(\cos x-2\sin x)\right].
$$

因此通解为
$$
\frac{1}{2}x^2y^2+2xy+y(\cos x-2\sin x)=C,
$$
其中 $C$ 为任意常数。

### 第 16 题

**答案：** 级数 $\displaystyle\sum_{n=1}^{\infty}f\left(\dfrac{1}{n}\right)$ 绝对收敛。

由
$$
\lim_{x\to0}\frac{f(x)}{x}=0
$$
且 $f$ 在 $0$ 的邻域内二阶连续可导，先得
$$
f(0)=0,\qquad f'(0)=\lim_{x\to0}\frac{f(x)-f(0)}{x}=0.
$$

取 $\delta>0$，使 $f''$ 在 $[-\delta,\delta]$ 上连续有界。于是存在 $M>0$，使
$$
\lvert f''(x)\rvert\le M,\qquad x\in[-\delta,\delta].
$$

当 $\lvert x\rvert\le\delta$ 时，由泰勒公式
$$
f(x)=f(0)+f'(0)x+\frac{1}{2}f''(\xi)x^2
=\frac{1}{2}f''(\xi)x^2,
$$
其中 $\xi$ 介于 $0$ 与 $x$ 之间。因此
$$
\lvert f(x)\rvert\le\frac{M}{2}x^2.
$$

当 $n$ 充分大时，$1/n<\delta$，从而
$$
\left|f\left(\frac{1}{n}\right)\right|
\le\frac{M}{2}\frac{1}{n^2}.
$$

由于 $\sum_{n=1}^{\infty}\dfrac{1}{n^2}$ 收敛，故由比较判别法，
$$
\sum_{n=1}^{\infty}\left|f\left(\frac{1}{n}\right)\right|
$$
收敛，即原级数绝对收敛。

### 第 17 题

**答案：** $\dfrac{2\pi}{3}$

线段 $AB$ 的方向向量为
$$
(0-1,1-0,1-0)=(-1,1,1).
$$

以 $z$ 为参数，线段 $AB$ 可写为
$$
x=1-z,\qquad y=z,\qquad 0\le z\le1.
$$

绕 $z$ 轴旋转后，高度为 $z$ 的截面是圆盘，其半径平方为
$$
r^2=x^2+y^2=(1-z)^2+z^2.
$$

故截面积为
$$
S(z)=\pi\bigl[(1-z)^2+z^2\bigr].
$$

体积
$$
\begin{aligned}
V
&=\int_0^1 S(z)\,dz\\
&=\pi\int_0^1\bigl[(1-z)^2+z^2\bigr]\,dz\\
&=\pi\int_0^1(1-2z+2z^2)\,dz\\
&=\pi\left[z-z^2+\frac{2}{3}z^3\right]_0^1\\
&=\frac{2\pi}{3}.
\end{aligned}
$$

### 第 18 题

**答案：** （I）的基础解系可取 $(0,0,1,0)^T,\ (-1,1,0,1)^T$；非零公共解为 $k(1,-1,-1,-1)^T,\ k\ne0$。

方程组（I）为
$$
x_1+x_2=0,\qquad x_2-x_4=0.
$$

令 $x_3,x_4$ 为自由变量，则
$$
x_2=x_4,\qquad x_1=-x_4.
$$

取 $(x_3,x_4)=(1,0),(0,1)$，得（I）的基础解系可取
$$
(0,0,1,0)^T,\qquad (-1,1,0,1)^T.
$$

方程组（II）的通解为
$$
x=k_1(0,1,1,0)^T+k_2(-1,2,2,1)^T,
$$
即
$$
x_1=-k_2,\quad x_2=k_1+2k_2,\quad x_3=k_1+2k_2,\quad x_4=k_2.
$$

代入方程组（I），两个方程都化为
$$
k_1+k_2=0,
$$
即 $k_1=-k_2$。因此存在非零公共解，且全部非零公共解为
$$
x=k(1,-1,-1,-1)^T,\qquad k\ne0.
$$

### 第 19 题

**答案：** 结论成立，即 $\lvert A\rvert\ne0$。

设 $A=(a_{ij})$，$A_{ij}$ 为元素 $a_{ij}$ 的代数余子式。伴随矩阵 $A^*$ 的 $(i,j)$ 元为 $A_{ji}$。

由
$$
A^*=A^T
$$
可得
$$
A_{ji}=a_{ji}\qquad(i,j=1,2,\ldots,n),
$$
也即
$$
A_{ij}=a_{ij}.
$$

因为 $A$ 为非零矩阵，存在某个 $a_{ij}\ne0$。沿第 $i$ 行展开行列式，得
$$
\lvert A\rvert
=\sum_{k=1}^n a_{ik}A_{ik}
=\sum_{k=1}^n a_{ik}^2.
$$

右端至少有一项 $a_{ij}^2>0$，故
$$
\lvert A\rvert>0.
$$

因此
$$
\lvert A\rvert\ne0.
$$

### 第 20 题

**答案：** $P(B)=1-p$

由概率加法公式，
$$
P(\overline A\,\overline B)
=P\bigl(\overline{A\cup B}\bigr)
=1-P(A\cup B)
=1-\bigl[P(A)+P(B)-P(AB)\bigr].
$$

题设给出
$$
P(AB)=P(\overline A\,\overline B),
$$
故
$$
P(AB)=1-P(A)-P(B)+P(AB).
$$

于是
$$
P(A)+P(B)=1.
$$

又 $P(A)=p$，所以
$$
P(B)=1-p.
$$

### 第 21 题

**答案：** $P\{Z=0\}=\dfrac{1}{4},\quad P\{Z=1\}=\dfrac{3}{4}$

因为 $Z=\max\{X,Y\}$，且 $X,Y$ 只取 $0,1$ 两个值，所以 $Z$ 也只取 $0,1$。

有
$$
P\{Z=0\}=P\{X=0,Y=0\}
=P\{X=0\}P\{Y=0\}
=\frac{1}{2}\cdot\frac{1}{2}
=\frac{1}{4}.
$$

于是
$$
P\{Z=1\}=1-P\{Z=0\}=\frac{3}{4}.
$$

故分布律为
$$
\begin{array}{c|cc}
Z&0&1\\ \hline
P&\frac{1}{4}&\frac{3}{4}
\end{array}
$$

### 第 22 题

**答案：** $E(Z)=\dfrac{1}{3},\quad D(Z)=3,\quad \rho_{XZ}=0$，且 $X$ 与 $Z$ 相互独立。

已知
$$
X\sim N(1,3^2),\qquad Y\sim N(0,4^2),\qquad \rho_{XY}=-\frac{1}{2}.
$$

因此
$$
E(X)=1,\quad D(X)=9,\quad E(Y)=0,\quad D(Y)=16.
$$

又
$$
\operatorname{Cov}(X,Y)
=\rho_{XY}\sqrt{D(X)}\sqrt{D(Y)}
=-\frac{1}{2}\cdot3\cdot4=-6.
$$

由
$$
Z=\frac{1}{3}X+\frac{1}{2}Y
$$
得
$$
E(Z)=\frac{1}{3}E(X)+\frac{1}{2}E(Y)=\frac{1}{3}.
$$

方差为
$$
\begin{aligned}
D(Z)
&=\frac{1}{9}D(X)+\frac{1}{4}D(Y)
+\frac{1}{3}\operatorname{Cov}(X,Y)\\
&=\frac{1}{9}\cdot9+\frac{1}{4}\cdot16+\frac{1}{3}(-6)\\
&=3.
\end{aligned}
$$

再算协方差：
$$
\begin{aligned}
\operatorname{Cov}(X,Z)
&=\operatorname{Cov}\left(X,\frac{1}{3}X+\frac{1}{2}Y\right)\\
&=\frac{1}{3}D(X)+\frac{1}{2}\operatorname{Cov}(X,Y)\\
&=3-3=0.
\end{aligned}
$$

所以
$$
\rho_{XZ}=\frac{\operatorname{Cov}(X,Z)}{\sqrt{D(X)}\sqrt{D(Z)}}=0.
$$

由于 $(X,Y)$ 服从二维正态分布，而 $X$ 与 $Z$ 都是 $X,Y$ 的线性组合，所以 $(X,Z)$ 也服从二维正态分布。二维正态分布中零相关推出相互独立，故 $X$ 与 $Z$ 相互独立。
