# 2001 年考研数学三答案与解析

## 第 1 题

### 标准答案

$-\dfrac{\alpha}{\beta}$

### 解析

由
$$
Q=AL^{\alpha}K^{\beta}=1
$$
得
$$
K=A^{-1/\beta}L^{-\alpha/\beta}.
$$

于是
$$
\frac{dK}{dL}
=-\frac{\alpha}{\beta}A^{-1/\beta}L^{-\alpha/\beta-1}.
$$

按弹性的定义，
$$
E_{K,L}=\frac{dK}{dL}\cdot\frac{L}{K}
=-\frac{\alpha}{\beta}.
$$

## 第 2 题

### 标准答案

$W_t=1.2W_{t-1}+2$

### 解析

由题意，第 $t$ 年工资总额等于第 $t-1$ 年工资总额的 $1.2$ 倍再加上 $2$，因此
$$
W_t=(1+20\%)W_{t-1}+2=1.2W_{t-1}+2.
$$

## 第 3 题

### 标准答案

$-3$

### 解析

记 $J$ 为 $4$ 阶全 $1$ 矩阵，则
$$
A=(k-1)I+J.
$$

矩阵 $J$ 的特征值为 $4,0,0,0$，所以 $A$ 的特征值为
$$
k+3,\quad k-1,\quad k-1,\quad k-1.
$$

由 $r(A)=3$ 知 $A$ 恰有一个特征值为 $0$。  
若 $k-1=0$，则 $A=J$，此时 $r(A)=1$，不合题意。  
因此只能有
$$
k+3=0,
$$
即
$$
k=-3.
$$

## 第 4 题

### 标准答案

$\dfrac{1}{12}$

### 解析

先求 $X+Y$ 的期望与方差：
$$
E(X+Y)=EX+EY=-2+2=0.
$$

又因为
$$
\rho(X,Y)=\frac{\operatorname{Cov}(X,Y)}{\sqrt{D(X)}\sqrt{D(Y)}}=-0.5,
$$
所以
$$
\operatorname{Cov}(X,Y)=(-0.5)\cdot 1\cdot 2=-1.
$$

因而
$$
D(X+Y)=D(X)+2\operatorname{Cov}(X,Y)+D(Y)=1+2(-1)+4=3.
$$

由切比雪夫不等式，
$$
P\{|X+Y|\ge 6\}
=P\{|X+Y-E(X+Y)|\ge 6\}
\le \frac{D(X+Y)}{6^2}
=\frac{3}{36}
=\frac{1}{12}.
$$

## 第 5 题

### 标准答案

$F$ 分布；参数为 $(10,5)$

### 解析

令
$$
Z_i=\frac{X_i}{0.2}\qquad(i=1,2,\ldots,15),
$$
则 $Z_1,\ldots,Z_{15}$ 相互独立，且都服从标准正态分布 $N(0,1)$。

因此
$$
U=\sum_{i=1}^{10}Z_i^2\sim\chi^2(10),\qquad
V=\sum_{i=11}^{15}Z_i^2\sim\chi^2(5),
$$
且 $U,V$ 相互独立。

又因为
$$
Y=\frac{X_1^2+\cdots+X_{10}^2}{2(X_{11}^2+\cdots+X_{15}^2)}
=\frac{U}{2V}
=\frac{U/10}{V/5},
$$
所以
$$
Y\sim F(10,5).
$$

## 第 6 题

### 标准答案

B

### 解析

由
$$
\lim_{x\to a}\frac{f'(x)}{x-a}=-1
$$
可得
$$
\lim_{x\to a}f'(x)
=\lim_{x\to a}\left(\frac{f'(x)}{x-a}\cdot(x-a)\right)=0.
$$

因为 $f'(x)$ 在 $x=a$ 处连续，所以
$$
f'(a)=0.
$$

于是
$$
f''(a)=\lim_{x\to a}\frac{f'(x)-f'(a)}{x-a}
=\lim_{x\to a}\frac{f'(x)}{x-a}
=-1<0.
$$

故 $x=a$ 是 $f(x)$ 的极大值点，选
$$
\boxed{B}.
$$

## 第 7 题

### 标准答案

D

### 解析

函数 $f$ 在 $[0,2]$ 上分段连续，因此变上限积分
$$
g(x)=\int_0^x f(u)\,du
$$
在整个区间 $[0,2]$ 上连续，特别地在 $(0,2)$ 内连续。

所以正确选项为
$$
\boxed{D}.
$$

## 第 8 题

### 标准答案

C

### 解析

将 $A$ 的第 $2,3$ 列互换，再将第 $1,4$ 列互换，便得到 $B$。因此
$$
B=AP_2P_1.
$$

由 $P_1^{-1}=P_1,\ P_2^{-1}=P_2$，得
$$
B^{-1}=(AP_2P_1)^{-1}=P_1^{-1}P_2^{-1}A^{-1}=P_1P_2A^{-1}.
$$

故选
$$
\boxed{C}.
$$

## 第 9 题

### 标准答案

D

### 解析

记
$$
M=\begin{pmatrix}
A & \alpha \\
\alpha^T & 0
\end{pmatrix}.
$$

题设给出
$$
r(M)=r(A)\le n<n+1.
$$

但 $M$ 是 $(n+1)$ 阶矩阵，所以 $M$ 不满秩。  
因而齐次线性方程组
$$
M\begin{pmatrix}X\\y\end{pmatrix}=0
$$
必有非零解。

故选
$$
\boxed{D}.
$$

## 第 10 题

### 标准答案

A

### 解析

每次掷硬币不是正面就是反面，因此
$$
X+Y=n,
$$
即
$$
Y=n-X.
$$

于是
$$
D(Y)=D(n-X)=D(X),
$$
且
$$
\operatorname{Cov}(X,Y)
=\operatorname{Cov}(X,n-X)
=-\operatorname{Cov}(X,X)
=-D(X).
$$

所以相关系数
$$
\rho_{XY}
=\frac{\operatorname{Cov}(X,Y)}{\sqrt{D(X)}\sqrt{D(Y)}}
=\frac{-D(X)}{D(X)}
=-1.
$$

故选
$$
\boxed{A}.
$$

## 第 11 题

### 标准答案

$\displaystyle \frac{du}{dx}=\frac{\partial f}{\partial x}-\frac{y}{x}\frac{\partial f}{\partial y}+\left(1-\frac{e^x(x-z)}{\sin(x-z)}\right)\frac{\partial f}{\partial z}$

### 解析

由复合函数求导法则，
$$
\frac{du}{dx}
=\frac{\partial f}{\partial x}
+\frac{\partial f}{\partial y}\frac{dy}{dx}
+\frac{\partial f}{\partial z}\frac{dz}{dx}.
$$

先对
$$
e^{xy}-xy=2
$$
两边对 $x$ 求导，得
$$
(e^{xy}-1)\left(y+x\frac{dy}{dx}\right)=0.
$$
由原方程知 $e^{xy}\ne 1$，故
$$
y+x\frac{dy}{dx}=0,
\qquad
\frac{dy}{dx}=-\frac{y}{x}.
$$

再对
$$
e^x=\int_0^{x-z}\frac{\sin t}{t}\,dt
$$
两边求导，由变上限积分求导公式得
$$
e^x=\frac{\sin(x-z)}{x-z}\left(1-\frac{dz}{dx}\right),
$$
从而
$$
\frac{dz}{dx}=1-\frac{e^x(x-z)}{\sin(x-z)}.
$$

代回即可得
$$
\frac{du}{dx}
=\frac{\partial f}{\partial x}
-\frac{y}{x}\frac{\partial f}{\partial y}
+\left(1-\frac{e^x(x-z)}{\sin(x-z)}\right)\frac{\partial f}{\partial z}.
$$

## 第 12 题

### 标准答案

$\dfrac12$

### 解析

先计算
$$
\lim_{x\to\infty}\left(\frac{x+c}{x-c}\right)^x
=\lim_{x\to\infty}\left(1+\frac{2c}{x-c}\right)^x.
$$
因为
$$
\frac{x}{x-c}\to 1,
$$
所以
$$
\lim_{x\to\infty}\left(1+\frac{2c}{x-c}\right)^x=e^{2c}.
$$

另一方面，由拉格朗日中值定理，对每个充分大的 $x$，存在 $\xi_x\in(x-1,x)$，使得
$$
f(x)-f(x-1)=f'(\xi_x).
$$
当 $x\to\infty$ 时，$\xi_x\to\infty$，故
$$
\lim_{x\to\infty}[f(x)-f(x-1)]
=\lim_{x\to\infty}f'(\xi_x)
=e.
$$

由题设两极限相等，得
$$
e^{2c}=e,
$$
因而
$$
2c=1,
\qquad
c=\frac12.
$$

## 第 13 题

### 标准答案

$-\dfrac23$

### 解析

区域
$$
D=\{(x,y)\mid -1\le y\le 1,\ y\le x\le 1\}.
$$

因此原积分可写为
$$
\int_{-1}^{1}\int_y^1 y\left[1+xe^{\frac12(x^2+y^2)}\right]\,dx\,dy
=I_1+I_2.
$$

其中
$$
I_1=\int_{-1}^{1}\int_y^1 y\,dx\,dy
=\int_{-1}^{1}y(1-y)\,dy
=-\frac23.
$$

对第二项，先对 $x$ 积分：
$$
I_2=\int_{-1}^{1}y\left[\int_y^1 xe^{\frac12(x^2+y^2)}\,dx\right]dy.
$$
令 $s=\dfrac12(x^2+y^2)$，则 $ds=x\,dx$，从而
$$
\int_y^1 xe^{\frac12(x^2+y^2)}\,dx
=e^{\frac12(1+y^2)}-e^{y^2}.
$$
所以
$$
I_2=\int_{-1}^{1}y\left(e^{\frac12(1+y^2)}-e^{y^2}\right)dy=0,
$$
因为被积函数关于 $y$ 是奇函数。

故原积分
$$
I=I_1+I_2=-\frac23.
$$

## 第 14 题

### 标准答案

（1）$p=-\dfrac45,\ q=3$；（2）$S_{\max}=\dfrac{225}{32}$

### 解析

抛物线与 $x$ 轴交于 $x=0$ 与 $x=-\dfrac{q}{p}$，故面积
$$
S=\int_0^{-q/p}(px^2+qx)\,dx
=-\frac{q^3}{6p^2}.
$$

又因为直线 $x+y=5$ 与抛物线相切，联立
$$
y=px^2+qx,
\qquad
y=5-x,
$$
得
$$
px^2+(q+1)x-5=0.
$$
相切意味着判别式为零：
$$
(q+1)^2+20p=0,
$$
即
$$
p=-\frac{(q+1)^2}{20}.
$$

代入面积公式，
$$
S(q)=\frac{200q^3}{3(q+1)^4}\qquad(q>0).
$$
求导得
$$
S'(q)=\frac{200q^2(3-q)}{3(q+1)^5}.
$$
因而 $S$ 在 $q=3$ 时达到最大值。

此时
$$
p=-\frac{(3+1)^2}{20}=-\frac45,
$$
且
$$
S_{\max}=S(3)=\frac{200\cdot 27}{3\cdot 4^4}
=\frac{225}{32}.
$$

## 第 15 题

### 标准答案

令 $F(x)=xe^{-x}f(x)$，则存在 $\xi\in(0,1)$ 使 $F'(\xi)=0$，从而 $f'(\xi)=\left(1-\xi^{-1}\right)f(\xi)$。

### 解析

令
$$
F(x)=xe^{-x}f(x).
$$
则
$$
xe^{1-x}f(x)=eF(x),
$$
所以题设可写为
$$
f(1)=ek\int_0^{1/k}F(x)\,dx.
$$

由积分中值定理，存在 $\eta\in[0,1/k]$，使得
$$
\int_0^{1/k}F(x)\,dx=\frac1kF(\eta).
$$
因而
$$
f(1)=eF(\eta)=\eta e^{1-\eta}f(\eta).
$$
两边同乘以 $e^{-1}$，得
$$
F(1)=F(\eta).
$$

由于 $F$ 在 $[\eta,1]$ 上连续、在 $(\eta,1)$ 上可导，由罗尔定理可知，存在 $\xi\in(\eta,1)\subset(0,1)$，使得
$$
F'(\xi)=0.
$$

而
$$
F'(x)=e^{-x}\bigl[xf'(x)+(1-x)f(x)\bigr].
$$
所以
$$
0=F'(\xi)=e^{-\xi}\bigl[\xi f'(\xi)+(1-\xi)f(\xi)\bigr].
$$
由此得到
$$
\xi f'(\xi)+(1-\xi)f(\xi)=0,
$$
即
$$
f'(\xi)=\left(1-\xi^{-1}\right)f(\xi).
$$

## 第 16 题

### 标准答案

$\displaystyle \sum_{n=1}^{\infty}f_n(x)=-e^x\ln(1-x),\qquad x\in[-1,1)$

### 解析

原方程可写为
$$
f_n'(x)-f_n(x)=x^{n-1}e^x.
$$
两边同乘以积分因子 $e^{-x}$，得
$$
\bigl(e^{-x}f_n(x)\bigr)'=x^{n-1}.
$$

积分可得
$$
e^{-x}f_n(x)=\frac{x^n}{n}+C.
$$
利用条件 $f_n(1)=\dfrac{e}{n}$，得到
$$
\frac1n+C=\frac1n,
$$
因而 $C=0$。故
$$
f_n(x)=e^x\frac{x^n}{n}.
$$

所以
$$
\sum_{n=1}^{\infty}f_n(x)
=e^x\sum_{n=1}^{\infty}\frac{x^n}{n}.
$$
当 $|x|<1$ 时，
$$
\sum_{n=1}^{\infty}\frac{x^n}{n}=-\ln(1-x),
$$
因而
$$
\sum_{n=1}^{\infty}f_n(x)=-e^x\ln(1-x).
$$

当 $x=-1$ 时，
$$
\sum_{n=1}^{\infty}\frac{(-1)^n}{n}=-\ln 2,
$$
仍与右端一致，因此和函数的定义域可扩充为
$$
x\in[-1,1).
$$

## 第 17 题

### 标准答案

（1）$a=-2$。  
（2）可取
$$
Q=\begin{pmatrix}
\frac1{\sqrt3} & \frac1{\sqrt2} & -\frac1{\sqrt6}\\[4pt]
\frac1{\sqrt3} & 0 & \frac2{\sqrt6}\\[4pt]
\frac1{\sqrt3} & -\frac1{\sqrt2} & -\frac1{\sqrt6}
\end{pmatrix},
$$
则
$$
Q^TAQ=\operatorname{diag}(0,3,-3).
$$

### 解析

（1）因为方程组 $AX=\beta$ 有解但不唯一，所以 $\det A=0$，且与增广矩阵同秩。

对矩阵 $A$ 直接求特征值更方便：向量 $(1,1,1)^T$ 对应特征值 $a+2$，而与它正交的二维子空间上对应特征值均为 $1-a$，因此
$$
\det A=(a+2)(a-1)^2.
$$
所以 $a=1$ 或 $a=-2$。

若 $a=1$，则
$$
A=\begin{pmatrix}
1&1&1\\
1&1&1\\
1&1&1
\end{pmatrix},
$$
方程组变为
$$
x_1+x_2+x_3=1,\qquad
x_1+x_2+x_3=1,\qquad
x_1+x_2+x_3=-2,
$$
矛盾，因此 $a=1$ 不可能。

故
$$
a=-2.
$$

（2）此时
$$
A=\begin{pmatrix}
1&1&-2\\
1&-2&1\\
-2&1&1
\end{pmatrix}.
$$

易验得三个互相正交的特征向量可取为
$$
\xi_1=(1,1,1)^T,\qquad
\xi_2=(1,0,-1)^T,\qquad
\xi_3=(-1,2,-1)^T,
$$
对应特征值分别为
$$
0,\quad 3,\quad -3.
$$

将它们单位化：
$$
\eta_1=\frac1{\sqrt3}(1,1,1)^T,\quad
\eta_2=\frac1{\sqrt2}(1,0,-1)^T,\quad
\eta_3=\frac1{\sqrt6}(-1,2,-1)^T.
$$

以 $\eta_1,\eta_2,\eta_3$ 为列向量组成正交矩阵
$$
Q=(\eta_1,\eta_2,\eta_3),
$$
则
$$
Q^TAQ=\operatorname{diag}(0,3,-3).
$$

## 第 18 题

### 标准答案

（1）$f(X)=X^TA^{-1}X$，因此其矩阵为 $A^{-1}$。  
（2）规范形相同。

### 解析

因为
$$
A^{-1}=\frac1{|A|}A^*,
$$
而伴随矩阵 $A^*$ 的第 $(j,i)$ 个元素正是 $A_{ij}$。又由于 $A$ 是实对称矩阵，故其代数余子式矩阵也对称，从而
$$
\frac{A_{ij}}{|A|}
$$
正好是 $A^{-1}$ 的第 $(i,j)$ 个元素。

因此
$$
f(X)=\sum_{i=1}^n\sum_{j=1}^n\frac{A_{ij}}{|A|}x_ix_j
=X^TA^{-1}X.
$$
所以二次型 $f(X)$ 的矩阵就是 $A^{-1}$。

再看规范形。因为 $A$ 可逆且为实对称矩阵，它的特征值全为非零实数。设这些特征值为
$$
\lambda_1,\lambda_2,\ldots,\lambda_n.
$$
那么 $A^{-1}$ 的特征值为
$$
\lambda_1^{-1},\lambda_2^{-1},\ldots,\lambda_n^{-1}.
$$
取倒数不会改变特征值的正负号，因此 $A$ 与 $A^{-1}$ 具有相同的正惯性指数和负惯性指数。

由实对称二次型的惯性定理可知，$g(X)=X^TAX$ 与 $f(X)=X^TA^{-1}X$ 的规范形相同。

## 第 19 题

### 标准答案

最多装 $98$ 箱。

### 解析

设第 $i$ 箱重量为 $X_i$（单位：千克），则
$$
E(X_i)=50,\qquad D(X_i)=25.
$$
若装 $n$ 箱，则总重量
$$
S_n=X_1+X_2+\cdots+X_n.
$$
因而
$$
E(S_n)=50n,\qquad D(S_n)=25n.
$$

由中心极限定理，当 $n$ 较大时，
$$
S_n\approx N(50n,25n).
$$
要求不超载的概率大于 $0.977$，即
$$
P(S_n\le 5000)>0.977=\Phi(2).
$$
标准化后得到
$$
\Phi\!\left(\frac{5000-50n}{5\sqrt n}\right)>\Phi(2).
$$
由于 $\Phi$ 单调递增，因此
$$
\frac{5000-50n}{5\sqrt n}>2.
$$

检查相邻整数即可：
$$
n=98\ \Rightarrow\ \frac{5000-4900}{5\sqrt{98}}\approx 2.02>2,
$$
而
$$
n=99\ \Rightarrow\ \frac{5000-4950}{5\sqrt{99}}\approx 1.01<2.
$$

因此每辆车最多可以装
$$
\boxed{98}
$$
箱。

## 第 20 题

### 标准答案

$$
p(u)=
\begin{cases}
\dfrac{2-u}{2}, & 0<u<2,\\[4pt]
0, & \text{其他}.
\end{cases}
$$

### 解析

因为 $(X,Y)$ 在边长为 $2$ 的正方形 $G$ 上均匀分布，所以联合密度为
$$
f_{X,Y}(x,y)=
\begin{cases}
\dfrac14, & (x,y)\in G,\\[4pt]
0, & \text{其他}.
\end{cases}
$$

设 $F(u)=P(U\le u)$。

当 $u<0$ 时，显然
$$
F(u)=0.
$$

当 $u\ge 2$ 时，因为在正方形 $G$ 内总有 $|X-Y|\le 2$，所以
$$
F(u)=1.
$$

当 $0\le u<2$ 时，条件 $|X-Y|\le u$ 表示正方形中两条直线
$$
y=x+u,\qquad y=x-u
$$
之间的带状区域。去掉的是两个直角边长都为 $2-u$ 的角三角形，所以
$$
F(u)=1-\frac{2\cdot \frac12(2-u)^2}{4}
=1-\frac{(2-u)^2}{4}.
$$

对 $u$ 求导，得到密度函数
$$
p(u)=F'(u)=\frac{2-u}{2}\qquad(0<u<2).
$$

因此
$$
p(u)=
\begin{cases}
\dfrac{2-u}{2}, & 0<u<2,\\[4pt]
0, & \text{其他}.
\end{cases}
$$
