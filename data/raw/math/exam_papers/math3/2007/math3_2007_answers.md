# 2007 年考研数学三答案与解析

## 第 1 题

### 标准答案

$B$

### 解析

利用常见等价无穷小可直接判断：

$$
e^{\sqrt{x}}-1\sim \sqrt{x},\qquad
\ln(1+\sqrt{x})\sim \sqrt{x},
$$
$$
\sqrt{1+\sqrt{x}}-1\sim \frac{1}{2}\sqrt{x},\qquad
1-\cos\sqrt{x}\sim \frac{x}{2}.
$$

因此

$$
1-e^{\sqrt{x}}\sim-\sqrt{x},
$$

与 $\sqrt{x}$ 等价的只有

$$
\ln(1+\sqrt{x})\sim \sqrt{x}.
$$

故选 $B$。

## 第 2 题

### 标准答案

D

### 解析

A 中若 $\lim_{x\to0}f(x)/x$ 存在，则 $f(x)\to0$，由连续性得 $f(0)=0$。B 中若 $\lim_{x\to0}[f(x)+f(-x)]/x$ 存在，则分子极限必须为 $0$，即 $2f(0)=0$。C 中由 A 得 $f(0)=0$，所以
$$
f'(0)=\lim_{x\to0}\frac{f(x)-f(0)}{x}
=\lim_{x\to0}\frac{f(x)}{x}
$$
存在。

D 错。例如 $f(x)=|x|$ 在 $0$ 处连续，且
$$
\frac{f(x)-f(-x)}{x}=0
$$
极限存在，但 $f'(0)$ 不存在。故选 D。

## 第 3 题

### 标准答案

C

### 解析

由图形可知 $f(x)$ 为奇函数，所以
$$
F(x)=\int_0^x f(t)\,dt
$$
为偶函数。

在 $[0,2]$ 上是直径为 $2$ 的上半圆，面积为 $\pi/2$，故
$$
F(2)=\frac{\pi}{2}.
$$
在 $[2,3]$ 上是直径为 $1$ 的下半圆，面积为 $-\pi/8$，故
$$
F(3)=\frac{\pi}{2}-\frac{\pi}{8}=\frac{3\pi}{8}.
$$
于是
$$
F(-3)=F(3)=\frac{3\pi}{8}
=\frac{3}{4}F(2).
$$
选 C。

## 第 4 题

### 标准答案

B

### 解析

原积分区域为
$$
\frac{\pi}{2}\le x\le\pi,\qquad \sin x\le y\le1.
$$
固定 $y\in[0,1]$，由 $\sin x\le y$ 且 $x\in[\pi/2,\pi]$ 得
$$
x\in[\pi-\arcsin y,\ \pi].
$$
因而交换次序后为
$$
\int_0^1dy\int_{\pi-\arcsin y}^{\pi}f(x,y)\,dx.
$$
故选 B。

## 第 5 题

### 标准答案

$D$

### 解析

需求弹性的绝对值为

$$
\left|\frac{pQ'(p)}{Q(p)}\right|
=\left|\frac{p\cdot(-2)}{160-2p}\right|
=\left|\frac{p}{80-p}\right|.
$$

由题意，

$$
\left|\frac{p}{80-p}\right|=1.
$$

在需求量为正的情形下，$160-2p>0$，即 $0<p<80$，于是

$$
\frac{p}{80-p}=1.
$$

解得

$$
p=40.
$$

故选 $D$。

## 第 6 题

### 标准答案

D

### 解析

函数在 $x=0$ 处有间断，且
$$
\lim_{x\to0^\pm}\left(\frac{1}{x}+\ln(1+e^x)\right)=\pm\infty,
$$
故 $x=0$ 是垂直渐近线。

当 $x\to-\infty$ 时，$\frac{1}{x}\to0$，$\ln(1+e^x)\to0$，故有水平渐近线 $y=0$。

当 $x\to+\infty$ 时，
$$
\lim_{x\to+\infty}\frac{y}{x}=1,\qquad
\lim_{x\to+\infty}(y-x)=0,
$$
故有斜渐近线 $y=x$。共 $3$ 条，选 D。

## 第 7 题

### 标准答案

A

### 解析

因为
$$
(\boldsymbol{\alpha}_1-\boldsymbol{\alpha}_2)
+(\boldsymbol{\alpha}_2-\boldsymbol{\alpha}_3)
+(\boldsymbol{\alpha}_3-\boldsymbol{\alpha}_1)=0,
$$
所以 A 中三个向量线性相关。故选 A。

## 第 8 题

### 标准答案

B

### 解析

矩阵
$$
A=\begin{pmatrix}2&-1&-1\\-1&2&-1\\-1&-1&2\end{pmatrix}
$$
的特征值为 $3,3,0$，而 $B$ 的特征值为 $1,1,0$，故二者不相似。

但二者都是实对称矩阵，且正惯性指数均为 $2$、负惯性指数均为 $0$、零特征值个数均为 $1$。由实二次型合同判别，二者合同。因此选 B。

## 第 9 题

### 标准答案

C

### 解析

第 $4$ 次射击恰好第 $2$ 次命中，表示前 $3$ 次中恰有 $1$ 次命中，且第 $4$ 次命中。因此概率为
$$
\binom{3}{1}p(1-p)^2\cdot p=3p^2(1-p)^2.
$$
选 C。

## 第 10 题

### 标准答案

A

### 解析

二维正态分布中，不相关等价于相互独立。因此
$$
f_{X,Y}(x,y)=f_X(x)f_Y(y).
$$
条件密度为
$$
f_{X\mid Y}(x\mid y)=\frac{f_{X,Y}(x,y)}{f_Y(y)}
=f_X(x).
$$
选 A。

## 第 11 题

### 标准答案

$0$

### 解析

因为

$$
0\le \frac{x^3+x^2+1}{2^x+x^3}\le \frac{x^3+x^2+1}{2^x},
$$

而指数函数增长快于多项式，所以

$$
\lim_{x\to+\infty}\frac{x^3+x^2+1}{2^x+x^3}=0.
$$

又由于

$$
|\sin x+\cos x|\le \sqrt{2},
$$

故 $(\sin x+\cos x)$ 是有界量。无穷小与有界量之积仍为无穷小，因此

$$
\lim_{x\to+\infty}\frac{x^3+x^2+1}{2^x+x^3}(\sin x+\cos x)=0.
$$

## 第 12 题

### 标准答案

$\dfrac{(-1)^n2^n n!}{3^{n+1}}$

### 解析

写成
$$
y=(2x+3)^{-1}.
$$
连续求导可得一般式
$$
y^{(n)}(x)=(-1)^n2^n n!(2x+3)^{-n-1}.
$$
令 $x=0$，即得
$$
y^{(n)}(0)=\frac{(-1)^n2^n n!}{3^{n+1}}.
$$

## 第 13 题

### 标准答案

$2\left(-\dfrac{y}{x}f_1'+\dfrac{x}{y}f_2'\right)$

### 解析

设
$$
u=\frac{y}{x},\qquad v=\frac{x}{y},\qquad z=f(u,v).
$$
由链式法则，
$$
z_x=f_1'u_x+f_2'v_x=f_1'\!\left(-\frac{y}{x^2}\right)+f_2'\frac1y,
$$
$$
z_y=f_1'u_y+f_2'v_y=f_1'\frac1x+f_2'\!\left(-\frac{x}{y^2}\right).
$$
因而
$$
xz_x-yz_y
=2\left(-\frac{y}{x}f_1'+\frac{x}{y}f_2'\right).
$$

## 第 14 题

### 标准答案

$$
\frac{x}{\sqrt{1+\ln x}}
$$

### 解析

令

$$
u=\frac{y}{x},
$$

则 $y=ux$，从而

$$
\frac{dy}{dx}=u+x\frac{du}{dx}.
$$

代入原方程得

$$
u+x\frac{du}{dx}=u-\frac12u^3,
$$

即

$$
x\frac{du}{dx}=-\frac12u^3.
$$

分离变量：

$$
\frac{du}{u^3}=-\frac12\frac{dx}{x}.
$$

积分得

$$
-\frac{1}{2u^2}=-\frac12\ln x+C,
$$

即

$$
\frac{1}{u^2}=\ln x+C_1.
$$

由 $u=\dfrac{y}{x}$ 可得

$$
\frac{x^2}{y^2}=\ln x+C_1.
$$

再由初始条件 $y(1)=1$，得 $C_1=1$，于是

$$
y^2=\frac{x^2}{1+\ln x}.
$$

又因 $y(1)=1>0$，取正支，故所求特解为

$$
y=\frac{x}{\sqrt{1+\ln x}}.
$$

## 第 15 题

### 标准答案

$1$

### 解析

矩阵 $A$ 是四阶 nilpotent Jordan 型上移矩阵。直接计算得
$$
A^3=
\begin{pmatrix}
0&0&0&1\\
0&0&0&0\\
0&0&0&0\\
0&0&0&0
\end{pmatrix}.
$$
因此
$$
r(A^3)=1.
$$

## 第 16 题

### 标准答案

$\displaystyle \frac{3}{4}$

### 解析

设两数为 $X,Y$，则样本点在单位正方形
$$
0<X<1,\qquad 0<Y<1
$$
内均匀分布。事件为
$$
|X-Y|<\frac{1}{2}.
$$
在单位正方形中，去掉两块直角三角形：
$$
Y-X\ge\frac{1}{2},\qquad X-Y\ge\frac{1}{2}.
$$
每块面积为 $\frac{1}{2}\cdot\frac{1}{2}\cdot\frac{1}{2}=\frac{1}{8}$，两块合计 $\frac{1}{4}$。故所求概率为
$$
1-\frac{1}{4}=\frac{3}{4}.
$$

## 第 17 题

### 标准答案

在点 $(1,1)$ 附近，曲线满足 $y''<0$，故曲线向下凹。

### 解析

由隐函数方程

$$
y\ln y-x+y=0
$$

两边对 $x$ 求导，得

$$
y'\ln y+y\cdot\frac{1}{y}y'-1+y'=0,
$$

即

$$
y'(\ln y+2)=1,
$$

所以

$$
y'=\frac{1}{\ln y+2}.
$$

再对上式求导：

$$
y''=-\frac{1}{(\ln y+2)^2}\cdot\frac{1}{y}y'
=-\frac{1}{y(\ln y+2)^3}.
$$

在点 $(1,1)$ 处，

$$
y''(1)=-\frac{1}{1\cdot(2+\ln1)^3}=-\frac18<0.
$$

由于 $y''$ 在 $(1,1)$ 附近连续，因此在该点附近仍有 $y''<0$。故曲线在点 $(1,1)$ 附近向下凹。

## 第 18 题

### 标准答案

$\dfrac13+2\sqrt2\ln(3+2\sqrt2)$

### 解析

将区域分成
$$
D_1=\{|x|+|y|\le1\},\qquad D_2=\{1<|x|+|y|\le2\}.
$$
则
$$
\iint_D f(x,y)\,d\sigma=\iint_{D_1}x^2\,d\sigma+\iint_{D_2}\frac{1}{\sqrt{x^2+y^2}}\,d\sigma.
$$
第一部分利用关于坐标轴的对称性：
$$
\iint_{D_1}x^2\,d\sigma
=4\int_0^1dx\int_0^{1-x}x^2\,dy
=4\int_0^1x^2(1-x)\,dx=\frac13.
$$
第二部分在第一象限用极坐标，边界 $x+y=1,2$ 分别对应
$$
r=\frac{1}{\cos\theta+\sin\theta},\qquad
r=\frac{2}{\cos\theta+\sin\theta},\qquad 0\le\theta\le\frac{\pi}{2}.
$$
因而
$$
\iint_{D_2}\frac{1}{\sqrt{x^2+y^2}}\,d\sigma
=4\int_0^{\pi/2}\int_{1/(\cos\theta+\sin\theta)}^{2/(\cos\theta+\sin\theta)}dr\,d\theta
=2\sqrt2\ln(3+2\sqrt2).
$$
所以结果为
$$
\frac13+2\sqrt2\ln(3+2\sqrt2).
$$

## 第 19 题

### 标准答案

结论成立：存在 $\eta\in(a,b)$ 使 $f(\eta)=g(\eta)$，并存在 $\xi\in(a,b)$ 使 $f''(\xi)=g''(\xi)$。

### 解析

设

$$
h(x)=f(x)-g(x).
$$

记 $f,g$ 在 $(a,b)$ 内的相等最大值为 $M$。则存在 $\alpha,\beta\in(a,b)$，使得

$$
f(\alpha)=M,\qquad g(\beta)=M.
$$

不妨设 $\alpha\le\beta$。

若 $\alpha=\beta$，则取 $\eta=\alpha$，立得

$$
f(\eta)=g(\eta).
$$

若 $\alpha<\beta$，则

$$
h(\alpha)=f(\alpha)-g(\alpha)=M-g(\alpha)\ge0,
$$
$$
h(\beta)=f(\beta)-g(\beta)=f(\beta)-M\le0.
$$

由连续性和介值定理，存在 $\eta\in[\alpha,\beta]\subset(a,b)$，使得

$$
h(\eta)=0,
$$

即

$$
f(\eta)=g(\eta).
$$

这证明了（A）。

又因为

$$
h(a)=f(a)-g(a)=0,\qquad h(\eta)=0,\qquad h(b)=f(b)-g(b)=0,
$$

由罗尔定理，存在 $\xi_1\in(a,\eta)$、$\xi_2\in(\eta,b)$，使得

$$
h'(\xi_1)=0,\qquad h'(\xi_2)=0.
$$

再对 $h'$ 在区间 $[\xi_1,\xi_2]$ 上应用罗尔定理，得到存在 $\xi\in(\xi_1,\xi_2)\subset(a,b)$，使得

$$
h''(\xi)=0.
$$

于是

$$
f''(\xi)=g''(\xi).
$$

这证明了（B）。

## 第 20 题

### 标准答案

$$
\frac{1}{x^2-3x-4}
=-\frac15\sum_{n=0}^{\infty}\left(\frac{1}{3^{n+1}}+\frac{(-1)^n}{2^{n+1}}\right)(x-1)^n,
\quad -1<x<3.
$$

### 解析

先作部分分式分解：

$$
\frac{1}{x^2-3x-4}
=\frac{1}{(x-4)(x+1)}
=\frac15\left(\frac{1}{x-4}-\frac{1}{x+1}\right).
$$

令 $t=x-1$，则

$$
x-4=t-3,\qquad x+1=t+2,
$$

所以

$$
\frac{1}{x^2-3x-4}
=\frac15\left(\frac{1}{t-3}-\frac{1}{t+2}\right).
$$

对第一项，

$$
\frac{1}{t-3}
=-\frac13\cdot\frac{1}{1-\frac{t}{3}}
=-\sum_{n=0}^{\infty}\frac{t^n}{3^{n+1}},
\qquad |t|<3.
$$

对第二项，

$$
\frac{1}{t+2}
=\frac12\cdot\frac{1}{1+\frac{t}{2}}
=\sum_{n=0}^{\infty}\frac{(-1)^n}{2^{n+1}}t^n,
\qquad |t|<2.
$$

代回并整理，得

$$
\frac{1}{x^2-3x-4}
=-\frac15\sum_{n=0}^{\infty}\left(\frac{1}{3^{n+1}}+\frac{(-1)^n}{2^{n+1}}\right)t^n.
$$

再将 $t=x-1$ 代回，得到

$$
\frac{1}{x^2-3x-4}
=-\frac15\sum_{n=0}^{\infty}\left(\frac{1}{3^{n+1}}+\frac{(-1)^n}{2^{n+1}}\right)(x-1)^n.
$$

收敛条件取两部分的交集：

$$
|x-1|<2,
$$

故收敛区间为

$$
(-1,3).
$$

## 第 21 题

### 标准答案

$a=1$ 时，公共解为 $k(-1,0,1)^T$；$a=2$ 时，公共解为 $(0,1,-1)^T$。

### 解析

公共解就是联立方程组
$$
\begin{cases}
x_1+x_2+x_3=0,\\
x_1+2x_2+ax_3=0,\\
x_1+4x_2+a^2x_3=0,\\
x_1+2x_2+x_3=a-1
\end{cases}
$$
的解。

对增广矩阵作初等行变换，可化为
$$
\begin{pmatrix}
1&0&1&|&1-a\\
0&1&0&|&a-1\\
0&0&a-1&|&1-a\\
0&0&0&|&(a-1)(a-2)
\end{pmatrix}.
$$
有解必须满足
$$
(a-1)(a-2)=0,
$$
故
$$
a=1\quad\text{或}\quad a=2.
$$

当 $a=1$ 时，同解方程组为
$$
x_1+x_3=0,\qquad x_2=0,
$$
故公共解为
$$
\boldsymbol{x}=k(-1,0,1)^T.
$$

当 $a=2$ 时，化简得
$$
x_1=0,\qquad x_2=1,\qquad x_3=-1,
$$
故公共解为
$$
\boldsymbol{x}=(0,1,-1)^T.
$$

## 第 22 题

### 标准答案

$B$ 的特征值为 $-2,1,1$；$\lambda=-2$ 的特征向量为 $k(1,-1,1)^T$，$\lambda=1$ 的特征向量满足 $x-y+z=0$；$\displaystyle B=\begin{pmatrix}0&1&-1\\1&0&1\\-1&1&0\end{pmatrix}$。

### 解析

设
$$
p(\lambda)=\lambda^5-4\lambda^3+1.
$$
因为 $B=p(A)$，若 $A\boldsymbol{\alpha}=\lambda\boldsymbol{\alpha}$，则
$$
B\boldsymbol{\alpha}=p(\lambda)\boldsymbol{\alpha}.
$$

对 $\lambda_1=1$，
$$
p(1)=1-4+1=-2.
$$
所以
$$
B\boldsymbol{\alpha}_1=-2\boldsymbol{\alpha}_1,
$$
即 $\boldsymbol{\alpha}_1=(1,-1,1)^T$ 是 $B$ 的特征向量，对应特征值 $-2$。

又
$$
p(2)=1,\qquad p(-2)=1,
$$
故 $B$ 的全部特征值为 $-2,1,1$。由于 $A$ 为实对称矩阵，$B=p(A)$ 也为实对称矩阵，不同特征值的特征向量正交。因此属于 $\lambda=1$ 的特征向量均与 $\boldsymbol{\alpha}_1$ 正交：
$$
x-y+z=0.
$$
可取基础向量
$$
(1,1,0)^T,\qquad (-1,0,1)^T.
$$

求矩阵 $B$ 时，用单位向量
$$
u=\frac{1}{\sqrt{3}}(1,-1,1)^T.
$$
$B$ 在 $u$ 方向上的特征值为 $-2$，在其正交平面上的特征值为 $1$，故
$$
B=I+(-2-1)uu^T=I-3uu^T.
$$
又
$$
3uu^T=
\begin{pmatrix}
1&-1&1\\
-1&1&-1\\
1&-1&1
\end{pmatrix},
$$
所以
$$
B=
\begin{pmatrix}
0&1&-1\\
1&0&1\\
-1&1&0
\end{pmatrix}.
$$

## 第 23 题

### 标准答案

$\displaystyle P\{X>2Y\}=\frac{7}{24}$；$\displaystyle f_Z(z)=z(2-z)\ (0<z<1)$，$\displaystyle f_Z(z)=(2-z)^2\ (1\le z<2)$，其他为 $0$。

### 解析

(I) 事件 $X>2Y$ 在单位正方形内对应
$$
0<x<1,\qquad 0<y<\frac{x}{2}.
$$
因此
$$
\begin{aligned}
P\{X>2Y\}
&=\int_0^1\int_0^{x/2}(2-x-y)\,dy\,dx\\
&=\int_0^1\left(x-\frac{5}{8}x^2\right)dx\\
&=\frac{7}{24}.
\end{aligned}
$$

(II) 令 $Z=X+Y$。由卷积公式，
$$
f_Z(z)=\int_{-\infty}^{+\infty}f(x,z-x)\,dx.
$$
在支持区域内
$$
f(x,z-x)=2-x-(z-x)=2-z.
$$

当 $0<z<1$ 时，$0<x<z$，故
$$
f_Z(z)=\int_0^z(2-z)\,dx=z(2-z).
$$

当 $1\le z<2$ 时，$z-1<x<1$，故
$$
f_Z(z)=\int_{z-1}^1(2-z)\,dx=(2-z)^2.
$$

其他 $z$ 处密度为 $0$。

## 第 24 题

### 标准答案

$\displaystyle \hat\theta=2\overline X-\frac{1}{2}$；$4\overline X^2$ 不是 $\theta^2$ 的无偏估计量。

### 解析

(I) 先求总体均值：
$$
EX=\int_0^\theta x\frac{1}{2\theta}\,dx
+\int_\theta^1x\frac{1}{2(1-\theta)}\,dx
=\frac{1}{4}+\frac{\theta}{2}.
$$
令样本均值等于总体均值：
$$
\overline X=\frac{1}{4}+\frac{\theta}{2},
$$
解得矩估计量
$$
\hat\theta=2\overline X-\frac{1}{2}.
$$

(II) 有
$$
E(4\overline X^2)=4\left[D(\overline X)+(E\overline X)^2\right]
=4\left[\frac{DX}{n}+\left(\frac{1}{4}+\frac{\theta}{2}\right)^2\right].
$$
即
$$
E(4\overline X^2)
=\frac{4}{n}DX+\frac{1}{4}+\theta+\theta^2.
$$
由于 $DX\ge0$ 且 $0<\theta<1$，可知
$$
E(4\overline X^2)\ne\theta^2.
$$
因此 $4\overline X^2$ 不是 $\theta^2$ 的无偏估计量。
