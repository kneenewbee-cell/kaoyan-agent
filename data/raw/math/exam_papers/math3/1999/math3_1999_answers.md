# 1999 年考研数学三答案与解析

## 第1题
### 标准答案

$-1$

### 解析

由题意，$\dfrac{\sin x}{x}$是$f(x)$的一个原函数，因此
$$
f(x)=\left(\frac{\sin x}{x}\right)'=\frac{x\cos x-\sin x}{x^2}.
$$
所求积分用分部积分：
$$
\int_{\frac{\pi}{2}}^{\pi}x f'(x)\,dx
=\int_{\frac{\pi}{2}}^{\pi}x\,d\bigl(f(x)\bigr)
=\bigl.xf(x)\bigr|_{\frac{\pi}{2}}^{\pi}-\int_{\frac{\pi}{2}}^{\pi}f(x)\,dx.
$$
又因为
$$
\int f(x)\,dx=\frac{\sin x}{x},
$$
所以
$$
\int_{\frac{\pi}{2}}^{\pi}f(x)\,dx=\left.\frac{\sin x}{x}\right|_{\frac{\pi}{2}}^{\pi}=0-\frac{2}{\pi}=-\frac{2}{\pi}.
$$
并且
$$
\pi f(\pi)=\pi\cdot\frac{\pi\cos\pi-\sin\pi}{\pi^2}=-1,
\qquad
\frac{\pi}{2}f\left(\frac{\pi}{2}\right)=\frac{\pi}{2}\cdot\frac{\frac{\pi}{2}\cos\frac{\pi}{2}-\sin\frac{\pi}{2}}{\left(\frac{\pi}{2}\right)^2}=-\frac{2}{\pi}.
$$
因此
$$
\int_{\frac{\pi}{2}}^{\pi}x f'(x)\,dx
=\left(-1+\frac{2}{\pi}\right)-\left(-\frac{2}{\pi}\right)=-1.
$$

## 第2题
### 标准答案

$4$

### 解析

对$|x|<1$，有等比级数
$$
\sum_{n=0}^{\infty}x^n=\frac{1}{1-x}.
$$
两边求导，得
$$
\sum_{n=1}^{\infty}n x^{n-1}=\frac{1}{(1-x)^2}.
$$
令$x=\dfrac12$，便有
$$
\sum_{n=1}^{\infty}n\left(\frac12\right)^{n-1}
=\frac{1}{\left(1-\frac12\right)^2}=4.
$$

## 第3题
### 标准答案

$O$

### 解析

直接计算得
$$
A^2=
\begin{pmatrix}
1 & 0 & 1 \\
0 & 2 & 0 \\
1 & 0 & 1
\end{pmatrix}
\begin{pmatrix}
1 & 0 & 1 \\
0 & 2 & 0 \\
1 & 0 & 1
\end{pmatrix}
=
\begin{pmatrix}
2 & 0 & 2 \\
0 & 4 & 0 \\
2 & 0 & 2
\end{pmatrix}
=2A.
$$
于是
$$
A^n-2A^{n-1}=A^{n-2}(A^2-2A)=A^{n-2}O=O.
$$
故所求为零矩阵$O$。

## 第4题
### 标准答案

$16$

### 解析

设$X_1,\dots,X_n$独立同分布于$N(a,0.2^2)$，则样本均值
$$
\overline{X}_n=\frac{1}{n}\sum_{i=1}^n X_i
$$
仍服从正态分布，且
$$
E\overline{X}_n=a,
\qquad
D\overline{X}_n=\frac{0.2^2}{n}.
$$
因此
$$
\overline{X}_n\sim N\left(a,\frac{0.2^2}{n}\right).
$$
标准化后有
$$
P\left\{\left|\overline{X}_n-a\right|<0.1\right\}
=P\left\{\left|\frac{\overline{X}_n-a}{0.2/\sqrt n}\right|<\frac{0.1\sqrt n}{0.2}\right\}
=P\left\{|U|<\tfrac12\sqrt n\right\},
$$
其中$U\sim N(0,1)$。
要使该概率不小于$0.95$，需满足
$$
\frac12\sqrt n\ge 1.96.
$$
故
$$
\sqrt n\ge 3.92,
\qquad
n\ge 15.3664.
$$
因为$n$取自然数，所以最小值为$16$。

## 第5题
### 标准答案

$0$

### 解析

按行列式展开，$Y$是若干项乘积的代数和，每一项都由$n$个互相独立的随机变量相乘得到。
因此每一项的期望都等于各因子期望之积，也就是$2^n$乘以该项的符号。
于是
$$
EY=
\begin{vmatrix}
EX_{11} & EX_{12} & \cdots & EX_{1n} \\
EX_{21} & EX_{22} & \cdots & EX_{2n} \\
\vdots & \vdots & & \vdots \\
EX_{n1} & EX_{n2} & \cdots & EX_{nn}
\end{vmatrix}
=
\begin{vmatrix}
2 & 2 & \cdots & 2 \\
2 & 2 & \cdots & 2 \\
\vdots & \vdots & & \vdots \\
2 & 2 & \cdots & 2
\end{vmatrix}.
$$
该行列式各行相同，所以值为$0$。故$EY=0$。

## 第6题
### 标准答案

（A）

### 解析

取
$$
F(x)=\int_0^x f(t)\,dt + C.
$$
若$f$为奇函数，则
$$
F(-x)=\int_0^{-x}f(t)\,dt + C
=-\int_0^x f(-u)\,du + C
=\int_0^x f(u)\,du + C
=F(x),
$$
所以$F$为偶函数，故（A）正确。

其余各项可举反例说明：

1. （B）不对。取$f(x)=x^2$，则$f$为偶函数，但其一个原函数$F(x)=\dfrac{x^3}{3}+1$不是奇函数。
2. （C）不对。取$f(x)=\cos^2 x$，则$f$是周期函数，但原函数$F(x)=\dfrac{x}{2}+\dfrac{\sin 2x}{4}$不是周期函数。
3. （D）不对。取$f(x)=x$，则$f$在$(-\infty,+\infty)$上单调增，但原函数$F(x)=\dfrac{x^2}{2}$在整个实数轴上并不单调增。

故正确选项为（A）。

## 第7题
### 标准答案

（C）

### 解析

设
$$
a=\iint_D f(u,v)\,du\,dv,
$$
则$a$是常数，原式化为
$$
f(x,y)=xy+a.
$$
于是
$$
a=\iint_D (xy+a)\,dx\,dy.
$$
区域$D$可表示为$0\le x\le1$，$0\le y\le x^2$，故
$$
a=\int_0^1\int_0^{x^2}(xy+a)\,dy\,dx
=\int_0^1\left(\frac{x^5}{2}+ax^2\right)dx
=\frac{1}{12}+\frac{a}{3}.
$$
解得
$$
a=\frac18.
$$
因此
$$
f(x,y)=xy+\frac18,
$$
故选（C）。

## 第8题
### 标准答案

（B）

### 解析

由题意，存在常数$k_1,\dots,k_m$使
$$
\beta=k_1\alpha_1+\cdots+k_m\alpha_m.
$$
又因为$\beta$不能由$\alpha_1,\dots,\alpha_{m-1}$线性表示，所以必有$k_m\ne0$；否则上式右边不含$\alpha_m$，就与题设矛盾。
于是可解出
$$
\alpha_m=\frac1{k_m}\beta-\frac{k_1}{k_m}\alpha_1-\cdots-\frac{k_{m-1}}{k_m}\alpha_{m-1}.
$$
这说明$\alpha_m$可由向量组（II）线性表示。

再看它是否可由向量组（I）线性表示。若可以，则
$$
\alpha_m=c_1\alpha_1+\cdots+c_{m-1}\alpha_{m-1}.
$$
代回$\beta=k_1\alpha_1+\cdots+k_m\alpha_m$，便得到$\beta$也可由$\alpha_1,\dots,\alpha_{m-1}$线性表示，这与题设矛盾。
因此$\alpha_m$不能由（I）线性表示，但可由（II）线性表示，故选（B）。

## 第9题
### 标准答案

（D）

### 解析

由$A$与$B$相似，知存在可逆矩阵$P$使
$$
P^{-1}AP=B.
$$
于是对任意常数$t$，有
$$
P^{-1}(tE-A)P=tP^{-1}EP-P^{-1}AP=tE-B.
$$
故$tE-A$与$tE-B$相似，所以（D）正确。

其余选项不对：

1. （A）若$\lambda E-A=\lambda E-B$，则推出$A=B$，这比“相似”强得多。
2. （B）相似矩阵有相同特征值，但对应特征向量一般不相同。
3. （C）相似矩阵未必都可对角化，例如同一个若尔当块的不同相似表示就都不可对角化。

故应选（D）。

## 第10题
### 标准答案

（A）

### 解析

由$P\{X_1X_2=0\}=1$知，只要$X_1$与$X_2$同时非零，联合概率就必须为$0$。
因此
$$
P\{X_1=-1,X_2=-1\}=P\{X_1=-1,X_2=1\}=P\{X_1=1,X_2=-1\}=P\{X_1=1,X_2=1\}=0.
$$
又因为$P\{X_1=-1\}=\dfrac14$，故必有
$$
P\{X_1=-1,X_2=0\}=\frac14.
$$
同理
$$
P\{X_1=1,X_2=0\}=\frac14.
$$
而$P\{X_2=0\}=\dfrac12$，所以
$$
P\{X_1=0,X_2=0\}=\frac12-\frac14-\frac14=0.
$$
于是
$$
P\{X_1=X_2\}=P\{X_1=-1,X_2=-1\}+P\{X_1=0,X_2=0\}+P\{X_1=1,X_2=1\}=0.
$$
故选（A）。

## 第11题
### 标准答案

切线方程为
$$
y-\frac1{\sqrt a}=-\frac1{2a^{3/2}}(x-a).
$$
所围图形面积为
$$
S=\frac94\sqrt a.
$$
当$a\to+\infty$时，$S\to+\infty$；当$a\to0^+$时，$S\to0$。

### 解析

曲线
$$
y=x^{-1/2}
$$
在点$\left(a,\dfrac1{\sqrt a}\right)$处的导数为
$$
y'=-\frac{1}{2x^{3/2}},
\qquad
y'\big|_{x=a}=-\frac{1}{2a^{3/2}}.
$$
故切线方程为
$$
y-\frac1{\sqrt a}=-\frac1{2a^{3/2}}(x-a).
$$
令$x=0$，得切线与$y$轴交点为
$$
\left(0,\frac1{\sqrt a}+\frac{1}{2\sqrt a}\right)=\left(0,\frac{3}{2\sqrt a}\right).
$$
令$y=0$，得切线与$x$轴交点为
$$
(3a,0).
$$
因此该图形是一直角三角形，其面积为
$$
S=\frac12\cdot 3a\cdot \frac{3}{2\sqrt a}=\frac94\sqrt a.
$$
由此可知：
$$
a\to+\infty \Rightarrow S=\frac94\sqrt a\to+\infty,
$$
$$
a\to0^+ \Rightarrow S=\frac94\sqrt a\to0.
$$
所以当切点沿曲线向右远去时，面积趋于无穷大；当切点沿曲线向上远去时，面积趋于$0$。

## 第12题
### 标准答案

$4-\dfrac{\pi}{2}$

### 解析

由题意可将区域写成
$$
D=\{(x,y)\mid 0\le y\le 2,\ -2\le x\le -\sqrt{2y-y^2}\}.
$$
因此
$$
\iint_D y\,dx\,dy
=\int_0^2\int_{-2}^{-\sqrt{2y-y^2}} y\,dx\,dy
=\int_0^2 y\left(2-\sqrt{2y-y^2}\right)dy.
$$
即
$$
\iint_D y\,dx\,dy
=2\int_0^2 y\,dy-\int_0^2 y\sqrt{2y-y^2}\,dy
=4-\int_0^2 y\sqrt{1-(y-1)^2}\,dy.
$$
令$y-1=\sin t$，则$dy=\cos t\,dt$，当$y=0$时$t=-\dfrac\pi2$，当$y=2$时$t=\dfrac\pi2$。于是
$$
\int_0^2 y\sqrt{1-(y-1)^2}\,dy
=\int_{-\pi/2}^{\pi/2}(1+\sin t)\cos^2 t\,dt.
$$
其中$\sin t\cos^2 t$为奇函数，在对称区间上积分为$0$，故
$$
\int_{-\pi/2}^{\pi/2}(1+\sin t)\cos^2 t\,dt
=\int_{-\pi/2}^{\pi/2}\cos^2 t\,dt
=\frac\pi2.
$$
因此
$$
\iint_D y\,dx\,dy=4-\frac\pi2.
$$

## 第13题
### 标准答案

最优投入为
$$
x_1=6\left(\frac{\alpha p_2}{\beta p_1}\right)^\beta,
\qquad
x_2=6\left(\frac{\beta p_1}{\alpha p_2}\right)^\alpha.
$$

### 解析

设总成本为
$$
P=p_1x_1+p_2x_2.
$$
题目要求在约束
$$
2x_1^{\alpha}x_2^{\beta}=12
\quad\Longleftrightarrow\quad
x_1^{\alpha}x_2^{\beta}=6
$$
下，使$P$最小。
用拉格朗日乘数法，取
$$
L(x_1,x_2,\lambda)=p_1x_1+p_2x_2+\lambda\bigl(2x_1^{\alpha}x_2^{\beta}-12\bigr).
$$
由驻点条件
$$
\frac{\partial L}{\partial x_1}=p_1+2\lambda\alpha x_1^{\alpha-1}x_2^{\beta}=0,
$$
$$
\frac{\partial L}{\partial x_2}=p_2+2\lambda\beta x_1^{\alpha}x_2^{\beta-1}=0,
$$
$$
\frac{\partial L}{\partial \lambda}=2x_1^{\alpha}x_2^{\beta}-12=0.
$$
前两式相除，得
$$
\frac{p_1}{p_2}=\frac{\alpha x_2}{\beta x_1},
$$
即
$$
p_1x_1\beta=p_2x_2\alpha,
\qquad
x_2=\frac{\beta p_1}{\alpha p_2}x_1.
$$
代回约束条件：
$$
x_1^{\alpha}\left(\frac{\beta p_1}{\alpha p_2}x_1\right)^\beta=6.
$$
利用$\alpha+\beta=1$，得
$$
x_1\left(\frac{\beta p_1}{\alpha p_2}\right)^\beta=6,
$$
所以
$$
x_1=6\left(\frac{\alpha p_2}{\beta p_1}\right)^\beta.
$$
再由$x_2=\dfrac{\beta p_1}{\alpha p_2}x_1$，得到
$$
x_2=6\left(\frac{\beta p_1}{\alpha p_2}\right)^\alpha.
$$
故最小成本时的投入量如上。

## 第14题
### 标准答案

所求函数为
$$
y(x)=\begin{cases}
e^{2x}-1, & x\le 1, \\
(1-e^{-2})e^{2x}, & x>1.
\end{cases}
$$

### 解析

在区间$x<1$上，方程为
$$
y'-2y=2.
$$
其通解为
$$
y=C_1e^{2x}-1.
$$
在区间$x>1$上，方程为
$$
y'-2y=0,
$$
其通解为
$$
y=C_2e^{2x}.
$$
由条件$y(0)=0$，且$0<1$，代入左段解得
$$
0=C_1-1,
$$
故$C_1=1$，从而
$$
y=e^{2x}-1\qquad (x<1).
$$
又由于$y$在$(-\infty,+\infty)$上连续，故在$x=1$处满足
$$
\lim_{x\to1^-}y(x)=\lim_{x\to1^+}y(x).
$$
即
$$
e^2-1=C_2e^2,
$$
所以
$$
C_2=1-e^{-2}.
$$
因此
$$
y(x)=\begin{cases}
e^{2x}-1, & x\le 1, \\
(1-e^{-2})e^{2x}, & x>1.
\end{cases}
$$
该函数在两侧分别满足原方程，并在全实数范围内连续。

## 第15题
### 标准答案

$\displaystyle \int_1^2 f(x)\,dx=\frac34$

### 解析

对积分作代换$u=2x-t$，则$t=2x-u$，$dt=-du$，得
$$
\int_0^x t f(2x-t)\,dt
=\int_x^{2x}(2x-u)f(u)\,du
=2x\int_x^{2x}f(u)\,du-\int_x^{2x}u f(u)\,du.
$$
于是
$$
2x\int_x^{2x}f(u)\,du-\int_x^{2x}u f(u)\,du=\frac12\arctan x^2.
$$
两边对$x$求导。设
$$
A(x)=\int_x^{2x}f(u)\,du,
\qquad
B(x)=\int_x^{2x}u f(u)\,du.
$$
则由莱布尼茨公式，
$$
A'(x)=2f(2x)-f(x),
\qquad
B'(x)=4x f(2x)-x f(x).
$$
因此
$$
\frac{d}{dx}\bigl(2xA(x)-B(x)\bigr)
=2A(x)+2xA'(x)-B'(x)
=2\int_x^{2x}f(u)\,du-xf(x).
$$
而右边导数为
$$
\frac{d}{dx}\left(\frac12\arctan x^2\right)=\frac{x}{1+x^4}.
$$
故有
$$
2\int_x^{2x}f(u)\,du-xf(x)=\frac{x}{1+x^4}.
$$
令$x=1$，并用$f(1)=1$，得
$$
2\int_1^2 f(u)\,du-1=\frac12.
$$
所以
$$
\int_1^2 f(x)\,dx=\frac34.
$$

## 第16题
### 标准答案

（A）存在$\eta\in\left(\dfrac12,1\right)$使$f(\eta)=\eta$；

（B）对任意$\lambda\in\mathbb R$，存在$\xi\in(0,\eta)$使
$$
f'(\xi)-\lambda\bigl[f(\xi)-\xi\bigr]=1.
$$

### 解析

先证（A）。令
$$
F(x)=f(x)-x.
$$
则$F$在$[0,1]$上连续，在$(0,1)$内可导，且
$$
F\left(\frac12\right)=f\left(\frac12\right)-\frac12=\frac12>0,
\qquad
F(1)=f(1)-1=-1<0.
$$
由介值定理知，存在
$$
\eta\in\left(\frac12,1\right)
$$
使得$F(\eta)=0$，即
$$
f(\eta)=\eta.
$$
故（A）成立。

再证（B）。对任意给定的实数$\lambda$，令
$$
G(x)=e^{-\lambda x}\bigl(f(x)-x\bigr).
$$
由$f(0)=0$及$f(\eta)=\eta$可得
$$
G(0)=e^0(f(0)-0)=0,
\qquad
G(\eta)=e^{-\lambda\eta}\bigl(f(\eta)-\eta\bigr)=0.
$$
由于$G$在$[0,\eta]$上连续、在$(0,\eta)$内可导，故由罗尔定理知，存在$\xi\in(0,\eta)$使
$$
G'(\xi)=0.
$$
而
$$
G'(x)=e^{-\lambda x}\Bigl(f'(x)-1-\lambda\bigl(f(x)-x\bigr)\Bigr).
$$
故在$x=\xi$处有
$$
e^{-\lambda \xi}\Bigl(f'(\xi)-1-\lambda\bigl(f(\xi)-\xi\bigr)\Bigr)=0.
$$
指数因子不为零，因此
$$
f'(\xi)-\lambda\bigl(f(\xi)-\xi\bigr)=1.
$$
故（B）得证。

## 第17题
### 标准答案

（B）

### 解析

因为$X\sim N(0,1)$，$Y\sim N(1,1)$，且二者独立，所以
$$
X+Y\sim N(1,2),
\qquad
X-Y\sim N(-1,2).
$$
对正态分布，概率等于$\dfrac12$恰好对应于随机变量不超过其均值。

1. 对$X+Y\sim N(1,2)$，有
$$
P\{X+Y\le1\}=\frac12.
$$
因此（B）正确。
2. 因为$0\ne1$，所以
$$
P\{X+Y\le0\}\ne\frac12,
$$
故（A）错误。
3. 因为$X-Y\sim N(-1,2)$，其均值为$-1$，而不是$0$或$1$，故
$$
P\{X-Y\le0\}\ne\frac12,
\qquad
P\{X-Y\le1\}\ne\frac12.
$$
所以（C）、（D）也都错误。

故应选（B）。

## 第18题
### 标准答案

当$\lambda>0$时，矩阵$B=\lambda E+A^TA$为正定矩阵。

### 解析

先证$B$是实对称矩阵：
$$
B^T=(\lambda E+A^TA)^T=\lambda E+(A^TA)^T=\lambda E+A^TA=B.
$$
再对任意非零向量$x\in\mathbb R^n$，考察二次型：
$$
x^TBx=x^T(\lambda E+A^TA)x=\lambda x^Tx+x^TA^TAx.
$$
注意到
$$
x^TA^TAx=(Ax)^T(Ax)\ge0,
$$
而当$x\ne0$时，
$$
x^Tx>0.
$$
又因为$\lambda>0$，所以
$$
\lambda x^Tx>0.
$$
于是对任意$x\ne0$，都有
$$
x^TBx=\lambda x^Tx+(Ax)^T(Ax)>0.
$$
这正是正定矩阵的定义，因此$B$为正定矩阵。

## 第19题
### 标准答案

联合分布为
$$
P\{U=0,V=0\}=\frac14,\quad P\{U=0,V=1\}=0,\quad P\{U=1,V=0\}=\frac14,\quad P\{U=1,V=1\}=\frac12.
$$
相关系数为
$$
r=\frac{\sqrt3}{3}.
$$

### 解析

由于$(X,Y)$在矩形$G$上均匀分布，总面积为$2$，故任一事件的概率等于对应区域面积除以$2$。

由直线$x=y$与$x=2y$把矩形分成三部分：

1. 区域$\{X\le Y\}$的面积为
$$
\int_0^1 y\,dy=\frac12,
$$
故
$$
P\{X\le Y\}=\frac{1/2}{2}=\frac14.
$$
2. 区域$\{X>2Y\}$的面积为
$$
\int_0^1 (2-2y)\,dy=1,
$$
故
$$
P\{X>2Y\}=\frac{1}{2}.
$$
3. 区域$\{Y<X\le2Y\}$的概率为
$$
1-\frac14-\frac12=\frac14.
$$
因此联合分布为
$$
P\{U=0,V=0\}=P\{X\le Y\}=\frac14,
$$
$$
P\{U=0,V=1\}=0,
$$
$$
P\{U=1,V=0\}=P\{Y<X\le2Y\}=\frac14,
$$
$$
P\{U=1,V=1\}=P\{X>2Y\}=\frac12.
$$

下面求相关系数。由上式得边缘分布：
$$
P\{U=1\}=\frac34,
\qquad
P\{V=1\}=\frac12.
$$
所以
$$
EU=\frac34,
\qquad
EV=\frac12,
\qquad
EUV=P\{U=1,V=1\}=\frac12.
$$
故协方差为
$$
\operatorname{cov}(U,V)=EUV-EU\cdot EV
=\frac12-\frac34\cdot\frac12=\frac18.
$$
又因为$U,V$都是$0$-$1$变量，
$$
DU=EU-EU^2=\frac34-\left(\frac34\right)^2=\frac{3}{16},
$$
$$
DV=EV-EV^2=\frac12-\left(\frac12\right)^2=\frac14.
$$
于是
$$
r=\frac{\operatorname{cov}(U,V)}{\sqrt{DU}\,\sqrt{DV}}
=\frac{1/8}{\sqrt{3/16}\cdot\sqrt{1/4}}
=\frac{1}{\sqrt3}
=\frac{\sqrt3}{3}.
$$

## 第20题
### 标准答案

$Z\sim t(2)$

### 解析

设总体$X\sim N(\mu,\sigma^2)$。由于$X_1,\dots,X_9$是简单随机样本，所以它们相互独立且都服从$N(\mu,\sigma^2)$。

首先看$Y_1,Y_2$的分布：
$$
Y_1=\frac16\sum_{i=1}^6 X_i \sim N\left(\mu,\frac{\sigma^2}{6}\right),
$$
$$
Y_2=\frac13\sum_{i=7}^9 X_i \sim N\left(\mu,\frac{\sigma^2}{3}\right).
$$
因为$Y_1$只由$X_1,\dots,X_6$决定，而$Y_2,S^2$只由$X_7,X_8,X_9$决定，所以$Y_1$与$(Y_2,S^2)$独立。
又由正态总体样本均值与样本方差独立可知，$Y_2$与$S^2$独立，因此$Y_1-Y_2$与$S^2$独立。

再看$Y_1-Y_2$：
$$
E(Y_1-Y_2)=0,
$$
$$
D(Y_1-Y_2)=DY_1+DY_2=\frac{\sigma^2}{6}+\frac{\sigma^2}{3}=\frac{\sigma^2}{2}.
$$
故
$$
Y_1-Y_2\sim N\left(0,\frac{\sigma^2}{2}\right).
$$
于是
$$
U=\frac{Y_1-Y_2}{\sigma/\sqrt2}\sim N(0,1).
$$

另一方面，$S^2$正是样本$X_7,X_8,X_9$的样本方差，因此
$$
\frac{(3-1)S^2}{\sigma^2}=\frac{2S^2}{\sigma^2}\sim \chi^2(2).
$$
结合独立性，$U$与$\dfrac{2S^2}{\sigma^2}$独立。
于是按照$t$分布的定义，
$$
\frac{U}{\sqrt{\left(\dfrac{2S^2}{\sigma^2}\right)/2}}\sim t(2).
$$
而上式恰好化为
$$
\frac{\dfrac{Y_1-Y_2}{\sigma/\sqrt2}}{S/\sigma}
=\frac{\sqrt2\,(Y_1-Y_2)}{S}
=Z.
$$
故
$$
Z\sim t(2).
$$
