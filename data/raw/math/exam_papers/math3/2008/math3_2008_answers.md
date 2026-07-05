# 2008 年考研数学三答案与解析

## 答案速览

| 题号 | 答案 |
|---:|---|
| 1 | B |
| 2 | C |
| 3 | C |
| 4 | A |
| 5 | C |
| 6 | D |
| 7 | A |
| 8 | D |
| 9 | $1$ |
| 10 | $\dfrac{1}{2}\ln 3$ |
| 11 | $\dfrac{\pi}{4}$ |
| 12 | $\dfrac{1}{x}$ |
| 13 | $3$ |
| 14 | $\dfrac{1}{2e}$ |
| 15 | $-\dfrac{1}{6}$ |
| 16 | （1） $$ dz=\frac{(2x-\varphi')\,dx+(2y-\varphi')\,dy}{1+\varphi'}. $$ （2） $$ \frac{\partial u}{\partial x} =-\frac{2\varphi''(1+2x)}{(1+\varphi')^3}, $$ 其中 $\varphi'$、$\varphi''$ 都是在 $x+y+z(x,y)$ 处取值。 |
| 17 | $\dfrac{19}{4}+\ln 2$ |
| 18 | （1） $$ \int_t^{t+2} f(x)\,dx=\int_0^2 f(x)\,dx. $$ （2）$G(x)$ 是周期为 $2$ 的周期函数。 |
| 19 | 3980 万元 |
| 20 | （1）$\det A=(n+1)a^n$； （2）当 $a\ne 0$ 时方程组有唯一解，且 $$ x_1=\frac{n}{(n+1)a}. $$ （3）当 $a=0$ 时方程组有无穷多解，通解为 $$ \boldsymbol{x} =(0,1,0,\ldots,0)^T+k(1,0,0,\ldots,0)^T. $$ |
| 21 | （1）$\alpha_1,\alpha_2,\alpha_3$ 线性无关； （2） $$ P^{-1}AP= \begin{pmatrix} -1 & 0 & 0 \\ 0 & 1 & 1 \\ 0 & 0 & 1 \end{pmatrix}. $$ |
| 22 | （1）$\dfrac12$； （2） $$ f_Z(z)=\begin{cases} \dfrac13, & -1\le z<2, \\ 0, & 其他。 \end{cases} $$ |
| 23 | （1）$T$ 是 $\mu^2$ 的无偏估计量； （2）当 $\mu=0,\sigma=1$ 时， $$ D(T)=\frac{2}{n(n-1)}. $$ |

## 详细解析

### 第 1 题

#### 标准答案

B

#### 解析

由积分中值定理，对任意 $x\ne 0$，存在介于 $0$ 与 $x$ 之间的点 $\xi_x$，使得
$$
\frac{1}{x}\int_0^x f(t)\,dt=f(\xi_x).
$$
当 $x\to 0$ 时，$\xi_x\to 0$。又因 $f$ 在 $0$ 处连续，
$$
\lim_{x\to 0}g(x)=\lim_{x\to 0}f(\xi_x)=f(0).
$$
所以极限存在且有限，但原式在 $x=0$ 处未定义，因此 $x=0$ 是可去间断点，选 B。

### 第 2 题

#### 标准答案

C

#### 解析

分部积分得
$$
\int_0^a x f'(x)\,dx
=[xf(x)]_0^a-\int_0^a f(x)\,dx
=af(a)-\int_0^a f(x)\,dx.
$$
其中 $af(a)$ 是矩形 $ABOC$ 的面积，$\int_0^a f(x)\,dx$ 是曲边梯形 $ABOD$ 的面积，
二者之差正是曲边三角形 $ACD$ 的面积，所以选 C。

### 第 3 题

#### 标准答案

C

#### 解析

对 $x$ 的偏导数，
$$
f'_x(0,0)=\lim_{h\to 0}\frac{f(h,0)-f(0,0)}{h}
=\lim_{h\to 0}\frac{e^{|h|}-1}{h}.
$$
当 $h\to 0^+$ 时，上式趋于 $1$；当 $h\to 0^-$ 时，上式趋于 $-1$，故 $f'_x(0,0)$ 不存在。

对 $y$ 的偏导数，
$$
f'_y(0,0)=\lim_{h\to 0}\frac{f(0,h)-f(0,0)}{h}
=\lim_{h\to 0}\frac{e^{h^2}-1}{h}.
$$
由于 $e^{h^2}-1\sim h^2$，所以
$$
\lim_{h\to 0}\frac{e^{h^2}-1}{h}=0.
$$
因此 $f'_y(0,0)$ 存在，而 $f'_x(0,0)$ 不存在，选 C。

### 第 4 题

#### 标准答案

A

#### 解析

将积分区域改写为极坐标：$1\le r\le u$，$0\le \theta \le v$。此时
$$
x^2+y^2=r^2,\qquad dx\,dy=r\,dr\,d\theta,
$$
所以
$$
F(u,v)=\int_0^v\int_1^u f(r^2)\,dr\,d\theta
=v\int_1^u f(r^2)\,dr.
$$
对 $u$ 求偏导得
$$
\frac{\partial F}{\partial u}=vf(u^2).
$$
故选 A。

### 第 5 题

#### 标准答案

C

#### 解析

由 $A^3=O$，
$$
(E-A)(E+A+A^2)=E-A^3=E,
$$
因此 $E-A$ 可逆，且其逆为 $E+A+A^2$。

同理，
$$
(E+A)(E-A+A^2)=E+A^3=E,
$$
所以 $E+A$ 也可逆。故选 C。

### 第 6 题

#### 标准答案

D

#### 解析

实对称矩阵在实数域上的合同由惯性定理决定。矩阵
$$
A=\begin{pmatrix}
1 & 2 \\
2 & 1
\end{pmatrix}
$$
的特征值为 $3$ 和 $-1$，故其正、负惯性指数分别为 $1,1$。

选项 D 的矩阵
$$
\begin{pmatrix}
1 & -2 \\
-2 & 1
\end{pmatrix}
$$
的特征值同样是 $3$ 和 $-1$，惯性指数也为 $(1,1)$，因此与 $A$ 合同。故选 D。

### 第 7 题

#### 标准答案

A

#### 解析

设 $F_Z(x)$ 为 $Z$ 的分布函数，则
$$
F_Z(x)=P(Z\le x)=P(max\left{X,Y\right}\le x)=P(X\le x,\,Y\le x).
$$
由于 $X,Y$ 独立同分布，
$$
F_Z(x)=P(X\le x)P(Y\le x)=F(x)^2.
$$
所以选 A。

### 第 8 题

#### 标准答案

D

#### 解析

由 $\rho_{XY}=1$ 可知 $X,Y$ 几乎处处满足正线性关系，可设
$$
Y=aX+b,\qquad a>0.
$$
由方差关系得
$$
a=\frac{\sigma_Y}{\sigma_X}=\frac{2}{1}=2.
$$
再由期望关系
$$
EY=aEX+b
$$
得
$$
1=2\cdot0+b,
$$
故 $b=1$。于是
$$
P\{Y=2X+1\}=1.
$$
所以选 D。

### 第 9 题

#### 标准答案

$1$

#### 解析

由于定义式中出现 $|x|$，所以 $c\ge 0$。要使 $f(x)$ 在整个实数轴上连续，只需在 $x=±c$ 处连续。

在 $x=c$ 处连续给出
$$
c^2+1=\frac{2}{c},
$$
即
$$
c^3+c-2=0=(c-1)(c^2+c+2).
$$
又因为 $c^2+c+2>0$，故唯一可取的实根为
$$
c=1.
$$

### 第 10 题

#### 标准答案

$\dfrac{1}{2}\ln 3$

#### 解析

令
$$
t=x+\frac{1}{x}\qquad (x>0),
$$
则
$$
t^2-2=x^2+\frac{1}{x^2}=\frac{x^4+1}{x^2}.
$$
因而
$$
\frac{t}{t^2-2}
=\frac{\frac{x^2+1}{x}}{\frac{x^4+1}{x^2}}
=\frac{x+x^3}{1+x^4}.
$$
所以
$$
f(t)=\frac{t}{t^2-2},
$$
从而
$$
\int_2^{2\sqrt{2}} f(x)\,dx
=\int_2^{2\sqrt{2}} \frac{x}{x^2-2}\,dx
=\frac12\ln(x^2-2)\Big|_2^{2\sqrt2}
=\frac12\ln 3.
$$

### 第 11 题

#### 标准答案

$\dfrac{\pi}{4}$

#### 解析

区域 $D$ 关于 $x$ 轴对称，所以奇函数部分积分为零：
$$
\iint_D y\,dx\,dy=0.
$$
因此
$$
\iint_D (x^2-y)\,dx\,dy=\iint_D x^2\,dx\,dy.
$$
又由于区域关于坐标轴完全对称，
$$
\iint_D x^2\,dx\,dy=\iint_D y^2\,dx\,dy
=\frac12\iint_D (x^2+y^2)\,dx\,dy.
$$
改用极坐标，
$$
\iint_D (x^2+y^2)\,dx\,dy
=\int_0^{2\pi}\int_0^1 r^2\cdotr\,dr\,d\theta
=2\pi\cdot\frac14
=\frac{\pi}{2}.
$$
故
$$
\iint_D (x^2-y)\,dx\,dy
=\frac12\cdot\frac{\pi}{2}
=\frac{\pi}{4}.
$$

### 第 12 题

#### 标准答案

$\dfrac{1}{x}$

#### 解析

原方程可写成
$$
(xy)'=xy'+y=0.
$$
因而
$$
xy=C.
$$
由初始条件 $y(1)=1$ 得 $C=1$，所以
$$
y=\frac{1}{x}.
$$

### 第 13 题

#### 标准答案

$3$

#### 解析

由矩阵特征值的性质可知，$A^{-1}$ 的特征值为
$$
1,\quad \frac12,\quad \frac12.
$$
因而 $4A^{-1}-E$ 的特征值为
$$
4\cdot1-1=3,\qquad 4\cdot\frac12-1=1,\qquad 4\cdot\frac12-1=1.
$$
所以
$$
\left|4A^{-1}-E\right|=3\cdot1\cdot1=3.
$$

### 第 14 题

#### 标准答案

$\dfrac{1}{2e}$

#### 解析

若 $X\sim P(1)$，则
$$
EX=1,\qquad DX=1.
$$
由方差公式
$$
DX=E(X^2)-(EX)^2
$$
得
$$
E(X^2)=DX+(EX)^2=1+1=2.
$$
因此
$$
P\left\{X=EX^2\right\}=P\{X=2\}
=e^{-1}\frac{1^2}{2!}
=\frac{1}{2e}.
$$

### 第 15 题

#### 标准答案

$-\dfrac{1}{6}$

#### 解析

当 $x\to 0$ 时，
$$
\frac{\sin x}{x}=1-\frac{x^2}{6}+o(x^2).
$$
因而
$$
\ln\frac{\sin x}{x}
=\ln\left(1-\frac{x^2}{6}+o(x^2)\right)
=-\frac{x^2}{6}+o(x^2).
$$
所以
$$
\lim_{x\to 0}\frac{1}{x^2}\ln\frac{\sin x}{x}
=-\frac16.
$$

### 第 16 题

#### 标准答案

（1）
$$
dz=\frac{(2x-\varphi')\,dx+(2y-\varphi')\,dy}{1+\varphi'}.
$$

（2）
$$
\frac{\partial u}{\partial x}
=-\frac{2\varphi''(1+2x)}{(1+\varphi')^3},
$$
其中 $\varphi'$、$\varphi''$ 都是在 $x+y+z(x,y)$ 处取值。

#### 解析

记
$$
s=x+y+z(x,y).
$$
对方程
$$
x^2+y^2-z=\varphi(s)
$$
两边求全微分，得
$$
2x\,dx+2y\,dy-dz=\varphi'(s)(dx+dy+dz).
$$
整理可得
$$
(1+\varphi')dz=(2x-\varphi')\,dx+(2y-\varphi')\,dy,
$$
因而
$$
dz=\frac{(2x-\varphi')\,dx+(2y-\varphi')\,dy}{1+\varphi'}.
$$

由此得到
$$
z_x=\frac{2x-\varphi'}{1+\varphi'},\qquad
z_y=\frac{2y-\varphi'}{1+\varphi'}.
$$
所以
$$
u(x,y)=\frac{1}{x-y}(z_x-z_y)=\frac{2}{1+\varphi'}.
$$
对 $x$ 求偏导，
$$
\frac{\partial u}{\partial x}
=-\frac{2\varphi''}{(1+\varphi')^2}\cdot\frac{\partial s}{\partial x}.
$$
而
$$
\frac{\partial s}{\partial x}=1+z_x
=1+\frac{2x-\varphi'}{1+\varphi'}
=\frac{1+2x}{1+\varphi'}.
$$
于是
$$
\frac{\partial u}{\partial x}
=-\frac{2\varphi''(1+2x)}{(1+\varphi')^3}.
$$

### 第 17 题

#### 标准答案

$\dfrac{19}{4}+\ln 2$

#### 解析

曲线 $xy=1$ 将正方形区域 $D$ 分成三部分：

1. 当 $0\le x\le \frac12$ 时，恒有 $xy\le 1$，故被积函数等于 $1$；
2. 当 $\frac12\le x\le 2$ 且 $0\le y\le \frac1x$ 时，被积函数也等于 $1$；
3. 当 $\frac12\le x\le 2$ 且 $\frac1x\le y\le 2$ 时，被积函数等于 $xy$。

因此
$$
\iint_D max\left{xy,1\right}\,dx\,dy
=\int_0^{1/2}\int_0^2 1\,dy\,dx
+\int_{1/2}^2\int_0^{1/x}1\,dy\,dx
+\int_{1/2}^2\int_{1/x}^2 xy\,dy\,dx.
$$
逐项计算：
$$
\int_0^{1/2}\int_0^2 1\,dy\,dx=1,
$$
$$
\int_{1/2}^2\int_0^{1/x}1\,dy\,dx=\int_{1/2}^2 \frac{1}{x}\,dx=2\ln 2,
$$
$$
\int_{1/2}^2\int_{1/x}^2 xy\,dy\,dx
=\int_{1/2}^2 x\cdot\frac12\left(4-\frac{1}{x^2}\right)\,dx
=\frac{15}{4}-\ln 2.
$$
所以
$$
\iint_D max\left{xy,1\right}\,dx\,dy
=1+2\ln 2+\frac{15}{4}-\ln 2
=\frac{19}{4}+\ln 2.
$$

### 第 18 题

#### 标准答案

（1）
$$
\int_t^{t+2} f(x)\,dx=\int_0^2 f(x)\,dx.
$$

（2）$G(x)$ 是周期为 $2$ 的周期函数。

#### 解析

设
$$
F(t)=\int_t^{t+2}f(x)\,dx.
$$
由微积分基本定理，
$$
F'(t)=f(t+2)-f(t)=0,
$$
因为 $f$ 的周期为 $2$。所以 $F(t)$ 是常数，故
$$
\int_t^{t+2}f(x)\,dx=F(t)=F(0)=\int_0^2f(x)\,dx.
$$

记
$$
a=\int_0^2f(x)\,dx.
$$
由第（1）问可知，对任意 $t$ 都有
$$
\int_t^{t+2}f(s)\,ds=a.
$$
因而
$$
G(x)=\int_0^x [2f(t)-a]\,dt.
$$
于是
$$
G(x+2)-G(x)=\int_x^{x+2}[2f(t)-a]\,dt
=2\int_x^{x+2}f(t)\,dt-2a
=2a-2a=0.
$$
所以 $G(x+2)=G(x)$，即 $G(x)$ 是周期为 $2$ 的周期函数。

### 第 19 题

#### 标准答案

3980 万元

#### 解析

把第 $n$ 年提取的 $(10+9n)$ 万元折现到现在，其现值为
$$
\frac{10+9n}{(1.05)^n}.
$$
因此初始存款至少应等于全部现值之和：
$$
A=\sum_{n=1}^{\infty}\frac{10+9n}{1.05^n}.
$$
令
$$
x=\frac{1}{1.05}=\frac{20}{21},
$$
则
$$
A=10\sum_{n=1}^{\infty}x^n+9\sum_{n=1}^{\infty}nx^n.
$$
又因为
$$
\sum_{n=1}^{\infty}x^n=\frac{x}{1-x}=20,
$$
$$
\sum_{n=1}^{\infty}nx^n=\frac{x}{(1-x)^2}=420,
$$
所以
$$
A=10\cdot20+9\cdot420=200+3780=3980.
$$
故至少应存入 $3980$ 万元。

### 第 20 题

#### 标准答案

（1）$\det A=(n+1)a^n$；

（2）当 $a\ne 0$ 时方程组有唯一解，且
$$
x_1=\frac{n}{(n+1)a}.
$$

（3）当 $a=0$ 时方程组有无穷多解，通解为
$$
\boldsymbol{x}
=(0,1,0,\ldots,0)^T+k(1,0,0,\ldots,0)^T.
$$

#### 解析

记 $D_n=\det A$。按第一行展开可得递推关系
$$
D_n=2aD_{n-1}-a^2D_{n-2}\qquad (n\ge 3),
$$
且
$$
D_1=2a,\qquad D_2=
\begin{vmatrix}
2a & 1 \\
a^2 & 2a
\end{vmatrix}
=3a^2.
$$
用数学归纳法可得
$$
D_n=(n+1)a^n.
$$
这就证明了
$$
\det A=(n+1)a^n.
$$

方程组有唯一解当且仅当 $\det A\ne 0$，故
$$
a\ne 0.
$$
此时用克莱姆法则求 $x_1$。把 $D_n$ 的第一列换成 $b$，得
$$
D_n^{(1)}=D_{n-1}=na^{n-1}.
$$
因而
$$
x_1=\frac{D_n^{(1)}}{D_n}=\frac{na^{n-1}}{(n+1)a^n}=\frac{n}{(n+1)a}.
$$

当 $a=0$ 时，方程组化为
$$
\begin{cases}
x_2=1,\\
x_3=0,\\
\cdots\\
x_n=0,\\
0=0.
\end{cases}
$$
此时 $x_1$ 为自由变量，故有无穷多解。设 $x_1=k$，则通解为
$$
\boldsymbol{x}
=(0,1,0,\ldots,0)^T+k(1,0,0,\ldots,0)^T.
$$

### 第 21 题

#### 标准答案

（1）$\alpha_1,\alpha_2,\alpha_3$ 线性无关；

（2）
$$
P^{-1}AP=
\begin{pmatrix}
-1 & 0 & 0 \\
 0 & 1 & 1 \\
 0 & 0 & 1
\end{pmatrix}.
$$

#### 解析

因为 $\alpha_1,\alpha_2$ 分别属于不同特征值，所以它们线性无关。

若 $\alpha_3$ 可由 $\alpha_1,\alpha_2$ 线性表示，不妨设
$$
\alpha_3=l_1\alpha_1+l_2\alpha_2.
$$
由题设
$$
A\alpha_3=\alpha_2+\alpha_3
$$
以及
$$
A\alpha_1=-\alpha_1,\qquad A\alpha_2=\alpha_2
$$
得
$$
-l_1\alpha_1+l_2\alpha_2
=A\alpha_3
=\alpha_2+l_1\alpha_1+l_2\alpha_2.
$$
整理后得到
$$
2l_1\alpha_1+\alpha_2=0,
$$
这与 $\alpha_1,\alpha_2$ 线性无关矛盾。故 $\alpha_3$ 不能由前两者线性表示，于是
$$
\alpha_1,\alpha_2,\alpha_3
$$
线性无关。

取这组三向量为基，
$$
A\alpha_1=-\alpha_1,\qquad
A\alpha_2=\alpha_2,\qquad
A\alpha_3=\alpha_2+\alpha_3.
$$
因此在基 $P=(\alpha_1,\alpha_2,\alpha_3)$ 下，矩阵表示为
$$
P^{-1}AP=
\begin{pmatrix}
-1 & 0 & 0 \\
 0 & 1 & 1 \\
 0 & 0 & 1
\end{pmatrix}.
$$

### 第 22 题

#### 标准答案

（1）$\dfrac12$；

（2）
$$
f_Z(z)=\begin{cases}
\dfrac13, & -1\le z<2, \\
0, & 其他。
\end{cases}
$$

#### 解析

当 $X=0$ 时，$Z=X+Y=Y$，故
$$
P\left\{Z\le \frac12 \middle| X=0\right\}
=P\left\{Y\le \frac12\right\}
=\int_0^{1/2}1\,dy
=\frac12.
$$

再求 $Z$ 的分布。设 $F_Y$ 为 $Y$ 的分布函数，则
$$
F_Z(z)=P(X+Y\le z).
$$
由于 $X$ 只取 $-1,0,1$ 且与 $Y$ 独立，
$$
F_Z(z)
=\frac13[F_Y(z+1)+F_Y(z)+F_Y(z-1)].
$$
两边对 $z$ 求导，得
$$
f_Z(z)=\frac13[f_Y(z+1)+f_Y(z)+f_Y(z-1)].
$$
其中 $f_Y$ 在区间 $[0,1]$ 上恒等于 $1$，其三个平移区间分别是
$$
[-1,0),\qquad [0,1),\qquad [1,2).
$$
它们首尾相接，因此
$$
f_Z(z)=\begin{cases}
\dfrac13, & -1\le z<2, \\
0, & 其他。
\end{cases}
$$

### 第 23 题

#### 标准答案

（1）$T$ 是 $\mu^2$ 的无偏估计量；

（2）当 $\mu=0,\sigma=1$ 时，
$$
D(T)=\frac{2}{n(n-1)}.
$$

#### 解析

因为总体服从正态分布，所以
$$
E(\overline X)=\mu,\qquad D(\overline X)=\frac{\sigma^2}{n},
$$
并且样本方差满足
$$
E(S^2)=\sigma^2.
$$
于是
$$
E(T)=E(\overline X^2)-\frac1nE(S^2)
=D(\overline X)+[E(\overline X)]^2-\frac{\sigma^2}{n}
=\frac{\sigma^2}{n}+\mu^2-\frac{\sigma^2}{n}
=\mu^2.
$$
所以 $T$ 是 $\mu^2$ 的无偏估计量。

当 $\mu=0,\sigma=1$ 时，$\overline X$ 与 $S^2$ 相互独立，且
$$
\sqrt n\,\overline X\sim N(0,1),\qquad (n-1)S^2\sim \chi^2(n-1).
$$
因此
$$
D(\overline X^2)=\frac{1}{n^2}D(\chi_1^2)=\frac{2}{n^2},
$$
以及
$$
D(S^2)=\frac{1}{(n-1)^2}D(\chi_{n-1}^2)=\frac{1}{(n-1)^2}\cdot2(n-1)=\frac{2}{n-1}.
$$
由独立性，
$$
D(T)=D(\overline X^2)+\frac{1}{n^2}D(S^2)
=\frac{2}{n^2}+\frac{2}{n^2(n-1)}
=\frac{2}{n(n-1)}.
$$
