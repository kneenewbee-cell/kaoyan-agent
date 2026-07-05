# 2004 年数学三答案解析

资料类型：考研数学三答案解析
年份：2004
科目：数学三
整理状态：按答案页图人工清洗并整理为正式题卡格式


## 填空题

| 题号 | 答案 |
|---|---|
| 1 | $a=1,\ b=-4$ |
| 2 | $-\dfrac{g'(v)}{g(v)^2}$ |
| 3 | $-\dfrac12$ |
| 4 | $2$ |
| 5 | $e^{-1}$ |
| 6 | $\sigma^2$ |

## 选择题

| 题号 | 答案 |
|---|---|
| 7 | A |
| 8 | D |
| 9 | C |
| 10 | B |
| 11 | D |
| 12 | D |
| 13 | B |
| 14 | C |

## 解答题

| 题号 | 答案 |
|---|---|
| 15 | $\dfrac43$ |
| 16 | $\dfrac{16}{9}(3\pi-2)$ |
| 17 | 命题成立 |
| 18 | $E_d=\dfrac{P}{20-P}$，且当 $10<P<20$ 时降低价格会使收益增加 |
| 19 | $S'(x)=xS(x)+\dfrac{x^3}{2},\ S(0)=0$；$S(x)=-\dfrac{x^2}{2}+e^{x^2/2}-1$ |
| 20 | (I) $a=0$；(II) $a\ne0,\ a\ne b$ 时，$\beta=\left(1-\dfrac1a\right)\alpha_1+\dfrac1a\alpha_2$；(III) $a=b\ne0$ 时，$\beta=\left(1-\dfrac1a\right)\alpha_1+\left(\dfrac1a+c\right)\alpha_2+c\alpha_3,\ c\in\mathbb R$ |
| 21 | 特征值为 $\lambda_1=1+(n-1)b,\ \lambda_2=\cdots=\lambda_n=1-b$；可取 $P=(\xi_1,\xi_2,\ldots,\xi_n)$，其中 $\xi_1=(1,\ldots,1)^T,\ \xi_k=e_1-e_k\ (k=2,\ldots,n)$；当 $b=0$ 时 $A=E$，任意可逆 $P$ 均可 |
| 22 | $P(0,0)=\dfrac23,\ P(0,1)=\dfrac1{12},\ P(1,0)=\dfrac16,\ P(1,1)=\dfrac1{12}$；$\rho_{XY}=\dfrac{\sqrt{15}}{15}$；$P(Z=0)=\dfrac23,\ P(Z=1)=\dfrac14,\ P(Z=2)=\dfrac1{12}$ |
| 23 | 当 $\alpha=1$ 时，$\hat\beta_{\text{矩}}=\dfrac{\overline X}{\overline X-1},\ \hat\beta_{\text{MLE}}=\dfrac{n}{\sum_{i=1}^n\ln X_i}$；当 $\beta=2$ 时，$\hat\alpha_{\text{MLE}}=\min\{X_1,\ldots,X_n\}$ |

## 详细解析

### 第1题

- 答案：$a=1,\ b=-4$

若极限存在且非零，则分母必须满足
$$
e^x-a\to0 \quad (x\to0),
$$
故 $1-a=0$，即 $a=1$.

于是原极限化为
$$
\lim_{x\to0}\frac{\sin x}{e^x-1}(\cos x-b)
=\lim_{x\to0}\frac{\sin x}{x}\cdot\frac{x}{e^x-1}\cdot(\cos x-b)
=1\cdot1\cdot(1-b).
$$
由题意得 $1-b=5$，所以 $b=-4$.

### 第2题

- 答案：$-\dfrac{g'(v)}{g(v)^2}$

令
$$
u=xg(y),\qquad v=y,
$$
则
$$
x=\frac{u}{g(v)},
$$
从而
$$
f(u,v)=\frac{u}{g(v)}+g(v).
$$
先对 $u$ 求偏导：
$$
f_u(u,v)=\frac1{g(v)}.
$$
再对 $v$ 求偏导：
$$
f_{uv}(u,v)=\frac{\partial}{\partial v}\!\left(\frac1{g(v)}\right)
=-\frac{g'(v)}{g(v)^2}.
$$

### 第3题

- 答案：$-\dfrac12$

令 $t=x-1$，则
$$
\int_{1/2}^{2} f(x-1)\,dx
=\int_{-1/2}^{1} f(t)\,dt
=\int_{-1/2}^{1/2} te^{t^2}\,dt+\int_{1/2}^{1}(-1)\,dt.
$$
其中 $te^{t^2}$ 为奇函数，所以
$$
\int_{-1/2}^{1/2} te^{t^2}\,dt=0.
$$
故原式为
$$
0-\left(1-\frac12\right)=-\frac12.
$$

### 第4题

- 答案：$2$

展开得
$$
f=2x_1^2+2x_2^2+2x_3^2+2x_1x_2-2x_2x_3+2x_1x_3.
$$
对应矩阵为
$$
A=
\begin{pmatrix}
2 & 1 & 1\\
1 & 2 & -1\\
1 & -1 & 2
\end{pmatrix}.
$$
计算行列式可得
$$
|A|=0,
$$
但其二阶主子式
$$
\begin{vmatrix}
2 & 1\\
1 & 2
\end{vmatrix}=3\ne0.
$$
因此 $r(A)=2$，故二次型的秩为 $2$.

### 第5题

- 答案：$e^{-1}$

指数分布 $X\sim \mathrm{Exp}(\lambda)$ 满足
$$
D(X)=\frac1{\lambda^2},
\qquad \sqrt{D(X)}=\frac1\lambda.
$$
又其尾概率为
$$
P(X>t)=e^{-\lambda t}\quad (t>0),
$$
故
$$
P\!\left(X>\sqrt{D(X)}\right)
=P\!\left(X>\frac1\lambda\right)
=e^{-\lambda\cdot(1/\lambda)}
=e^{-1}.
$$

### 第6题

- 答案：$\sigma^2$

对正态总体有
$$
E\!\left[\sum_{i=1}^{n_1}(X_i-\overline X)^2\right]=(n_1-1)\sigma^2,
$$
以及
$$
E\!\left[\sum_{j=1}^{n_2}(Y_j-\overline Y)^2\right]=(n_2-1)\sigma^2.
$$
两式相加得
$$
E\!\left[\sum_{i=1}^{n_1}(X_i-\overline X)^2+\sum_{j=1}^{n_2}(Y_j-\overline Y)^2\right]
=(n_1+n_2-2)\sigma^2.
$$
再除以 $n_1+n_2-2$ 即得
$$
\sigma^2.
$$

### 第7题

- 答案：A

函数在 $x=1,2$ 处分母为零，因此包含这些点邻域的区间一般会出现无界情形。

在区间 $(-1,0)$ 内，函数连续；并且当 $x\to0^-$ 时，
$$
\frac{|x|\sin(x-2)}{x(x-1)(x-2)^2}
=-\frac{\sin(x-2)}{(x-1)(x-2)^2}
$$
极限存在且有限，所以在 $(-1,0)$ 内有界。

而其余三个区间分别在端点 $1$ 或 $2$ 附近产生无界，因此选 A.

### 第8题

- 答案：D

当 $x\to0$ 时，$1/x\to\infty$，所以
$$
\lim_{x\to0}g(x)=\lim_{x\to0}f\!\left(\frac1x\right)=\lim_{t\to\infty}f(t)=a.
$$
而
$$
g(0)=0.
$$
因此：

- 若 $a=0$，则 $\lim_{x\to0}g(x)=g(0)$，函数在 $0$ 点连续；
- 若 $a\ne0$，则 $\lim_{x\to0}g(x)\ne g(0)$，函数在 $0$ 点不连续。

所以连续性与 $a$ 的取值有关，选 D.

### 第9题

- 答案：C

在 $x=0$ 附近，$f(0)=0$，而当 $x\ne0$ 且充分接近 $0$ 时，
$$
|x(1-x)|>0,
$$
因此 $x=0$ 是极小值点。

又当 $x<0$ 时，
$$
f(x)=-x(1-x),
$$
其二阶导数为 $2>0$；  
当 $0<x<1$ 时，
$$
f(x)=x(1-x),
$$
其二阶导数为 $-2<0$.

可见曲线在 $x=0$ 两侧凹凸性发生改变，所以 $(0,0)$ 是拐点。故选 C.

### 第10题

- 答案：B

命题 1 错：取 $u_n=(-1)^n$，则
$$
u_{2n-1}+u_{2n}=0,
$$
从而 $\sum (u_{2n-1}+u_{2n})$ 收敛，但 $\sum u_n$ 发散。

命题 2 对：去掉级数有限项不改变收敛性。

命题 3 对：若 $\displaystyle\lim_{n\to\infty}\frac{u_{n+1}}{u_n}>1$，则从某项起 $|u_{n+1}|>|u_n|$，故 $u_n$ 不趋于 $0$，级数必发散。

命题 4 错：取 $u_n=1,\ v_n=-1$，则 $\sum (u_n+v_n)=0$ 收敛，但 $\sum u_n,\sum v_n$ 都发散。

故正确的是 2、3，选 B.

### 第11题

- 答案：D

由 $f'(x)$ 连续且
$$
f'(a)>0,\qquad f'(b)<0,
$$
根据介值定理，必存在 $x_0\in(a,b)$ 使
$$
f'(x_0)=0,
$$
故 C 正确。

又因为 $f'(a)>0$，所以在 $a$ 的右邻域内 $f$ 递增，从而能找到点使 $f(x)>f(a)$，故 A 正确；同理由 $f'(b)<0$ 可知在 $b$ 的左邻域内有点使 $f(x)>f(b)$，故 B 正确。

至于方程 $f(x)=0$ 是否在 $(a,b)$ 内有解，仅凭导数端点符号无法保证，因此错误项为 D.

### 第12题

- 答案：D

矩阵等价的充要条件是
$$
r(A)=r(B).
$$
若 $|A|=0$，则
$$
r(A)<n.
$$
于是 $r(B)<n$，从而
$$
|B|=0.
$$
因此 D 必然成立。

而等价变换并不保持行列式值本身，所以 A、B 不一定成立；C 更明显错误。故选 D.

### 第13题

- 答案：B

由 $A^*\ne0$ 可知
$$
r(A)=n-1 \quad \text{或} \quad r(A)=n.
$$
又因为非齐次方程组 $Ax=b$ 有互不相等的多个解，所以其解不唯一，必有
$$
r(A)<n.
$$
因此只能是
$$
r(A)=n-1.
$$
于是对应齐次方程组 $Ax=0$ 的基础解系所含向量个数为
$$
n-r(A)=1.
$$
故基础解系仅含一个非零解向量，选 B.

### 第14题

- 答案：C

由
$$
P(|X|<x)=\alpha
$$
得
$$
P(-x<X<x)=\alpha.
$$
利用标准正态分布关于原点对称，
$$
2\Phi(x)-1=\alpha,
$$
故
$$
\Phi(x)=\frac{1+\alpha}{2}=1-\frac{1-\alpha}{2}.
$$
而 $u_\beta$ 的定义是
$$
P(X>u_\beta)=\beta \iff \Phi(u_\beta)=1-\beta.
$$
因此
$$
x=u_{(1-\alpha)/2}.
$$
选 C.

### 第15题

- 答案：$\dfrac43$

利用展开式
$$
\sin x=x-\frac{x^3}{6}+o(x^3),
\qquad
\cos x=1-\frac{x^2}{2}+o(x^2).
$$
于是
$$
\sin^2x=x^2-\frac{x^4}{3}+o(x^4),
$$
从而
$$
\frac1{\sin^2x}
=\frac1{x^2}\cdot\frac1{1-\frac{x^2}{3}+o(x^2)}
=\frac1{x^2}+\frac13+o(1).
$$
另一方面，
$$
\frac{\cos^2x}{x^2}
=\frac{1-x^2+o(x^2)}{x^2}
=\frac1{x^2}-1+o(1).
$$
两式相减得
$$
\lim_{x\to0}\left(\frac1{\sin^2 x}-\frac{\cos^2 x}{x^2}\right)
=\frac13-(-1)=\frac43.
$$

### 第16题

- 答案：$\dfrac{16}{9}(3\pi-2)$

设
$$
D_1=\{(x,y)\mid x^2+y^2\le4\},\qquad
D_2=\{(x,y)\mid (x+1)^2+y^2\le1\},
$$
则题中区域为
$$
D=D_1\setminus D_2.
$$

由关于 $x$ 轴对称性，
$$
\iint_D y\,d\sigma=0.
$$
故原积分化为
$$
\iint_D \sqrt{x^2+y^2}\,d\sigma
=\iint_{D_1} r\,d\sigma-\iint_{D_2} r\,d\sigma.
$$

对 $D_1$ 用极坐标：
$$
\iint_{D_1} r\,d\sigma
=\int_0^{2\pi}\int_0^2 r^2\,dr\,d\theta
=\frac{16\pi}{3}.
$$

对 $D_2$，其边界满足
$$
(x+1)^2+y^2=1
\iff r^2+2r\cos\theta=0
\iff r=-2\cos\theta,
$$
故对应区域为 $\theta\in\left[\frac\pi2,\frac{3\pi}2\right]$，$0\le r\le -2\cos\theta$。于是
$$
\iint_{D_2} r\,d\sigma
=\int_{\pi/2}^{3\pi/2}\int_0^{-2\cos\theta} r^2\,dr\,d\theta
=\frac{32}{9}.
$$
因此
$$
\iint_D(\sqrt{x^2+y^2}+y)\,d\sigma
=\frac{16\pi}{3}-\frac{32}{9}
=\frac{16}{9}(3\pi-2).
$$

### 第17题

- 答案：命题成立

令
$$
F(x)=f(x)-g(x),\qquad G(x)=\int_a^x F(t)\,dt.
$$
则由题设可知
$$
G(x)\ge0\quad (x\in[a,b]),
$$
并且
$$
G(a)=0,\qquad G(b)=\int_a^b(f-g)\,dt=0.
$$

现在考察
$$
\int_a^b xF(x)\,dx=\int_a^b xG'(x)\,dx.
$$
分部积分得
$$
\int_a^b xG'(x)\,dx
=\bigl[xG(x)\bigr]_a^b-\int_a^b G(x)\,dx
=-\int_a^b G(x)\,dx\le0.
$$
于是
$$
\int_a^b x(f(x)-g(x))\,dx\le0,
$$
即
$$
\int_a^b xf(x)\,dx\le\int_a^b xg(x)\,dx.
$$
命题得证。

### 第18题

- 答案：$E_d=\dfrac{P}{20-P}$，且当 $10<P<20$ 时降低价格会使收益增加

由定义
$$
E_d=-\frac{P}{Q}\frac{dQ}{dP}.
$$
因为
$$
Q=100-5P,\qquad \frac{dQ}{dP}=-5,
$$
所以
$$
E_d=-\frac{P}{100-5P}\cdot(-5)=\frac{P}{20-P}.
$$

又收益
$$
R=PQ,
$$
故
$$
\frac{dR}{dP}=Q+P\frac{dQ}{dP}
=Q\left(1+\frac{P}{Q}\frac{dQ}{dP}\right)
=Q(1-E_d).
$$

若降低价格反而使收益增加，则当 $dP<0$ 时应有 $dR>0$，即
$$
\frac{dR}{dP}<0.
$$
由于 $Q>0$，故需
$$
1-E_d<0 \iff E_d>1.
$$
由
$$
\frac{P}{20-P}>1
$$
解得
$$
P>10.
$$
结合 $P\in(0,20)$，所以当
$$
10<P<20
$$
时，降低价格反而会使收益增加。

### 第19题

- 答案：$S'(x)=xS(x)+\dfrac{x^3}{2},\ S(0)=0$；$\quad S(x)=-\dfrac{x^2}{2}+e^{x^2/2}-1$

记
$$
S(x)=\frac{x^4}{2\cdot4}+\frac{x^6}{2\cdot4\cdot6}+\frac{x^8}{2\cdot4\cdot6\cdot8}+\cdots.
$$
显然
$$
S(0)=0.
$$

逐项求导得
$$
S'(x)=\frac{x^3}{2}+\frac{x^5}{2\cdot4}+\frac{x^7}{2\cdot4\cdot6}+\cdots
=x\left(\frac{x^2}{2}+S(x)\right).
$$
故 $S(x)$ 满足初值问题
$$
y'=xy+\frac{x^3}{2},\qquad y(0)=0.
$$

解线性微分方程
$$
y'-xy=\frac{x^3}{2}.
$$
取积分因子 $e^{-x^2/2}$，则
$$
\bigl(ye^{-x^2/2}\bigr)'=\frac{x^3}{2}e^{-x^2/2}.
$$
积分可得
$$
y=-\frac{x^2}{2}-1+Ce^{x^2/2}.
$$
由初值 $y(0)=0$，得 $C=1$。因此
$$
S(x)=-\frac{x^2}{2}+e^{x^2/2}-1.
$$

### 第20题

- 答案：(I) $a=0$；

(II) 当 $a\ne0$ 且 $a\ne b$ 时，
$$
\beta=\left(1-\frac1a\right)\alpha_1+\frac1a\alpha_2;
$$

(III) 当 $a=b\ne0$ 时，
$$
\beta=\left(1-\frac1a\right)\alpha_1+\left(\frac1a+c\right)\alpha_2+c\alpha_3,\quad c\in\mathbb R.
$$

设存在 $k_1,k_2,k_3$，使
$$
k_1\alpha_1+k_2\alpha_2+k_3\alpha_3=\beta.
$$
把它写成增广矩阵
$$
(\alpha_1,\alpha_2,\alpha_3,\beta)
=
\begin{pmatrix}
1 & 1 & -1 & 1\\
2 & a+2 & -b-2 & 3\\
0 & -3a & a+2b & -3
\end{pmatrix}.
$$
行变换可化为
$$
\begin{pmatrix}
1 & 1 & -1 & 1\\
0 & a & -b & 1\\
0 & 0 & a-b & 0
\end{pmatrix}.
$$

1. 当 $a=0$ 时，矩阵继续化简后有
$$
r(A)\ne r(A,\beta),
$$
故方程无解，$\beta$ 不能由 $\alpha_1,\alpha_2,\alpha_3$ 线性表示。

2. 当 $a\ne0$ 且 $a\ne b$ 时，
$$
r(A)=r(A,\beta)=3,
$$
故有唯一解。回代得
$$
k_1=1-\frac1a,\qquad k_2=\frac1a,\qquad k_3=0,
$$
所以
$$
\beta=\left(1-\frac1a\right)\alpha_1+\frac1a\alpha_2.
$$

3. 当 $a=b\ne0$ 时，
$$
r(A)=r(A,\beta)=2,
$$
故有无穷多解。令自由参数为 $c$，则
$$
k_1=1-\frac1a,\qquad
k_2=\frac1a+c,\qquad
k_3=c.
$$
因此
$$
\beta=\left(1-\frac1a\right)\alpha_1+\left(\frac1a+c\right)\alpha_2+c\alpha_3,\quad c\in\mathbb R.
$$

### 第21题

- 答案：特征值为
$$
\lambda_1=1+(n-1)b,\qquad \lambda_2=\cdots=\lambda_n=1-b.
$$
$\lambda_1$ 的特征向量为任意非零倍数的 $(1,1,\ldots,1)^T$；$\lambda_2$ 对应的特征子空间为 $x_1+\cdots+x_n=0$。可取
$$
\xi_1=(1,1,\ldots,1)^T,\quad
\xi_k=e_1-e_k\quad(k=2,\ldots,n),
$$
令 $P=(\xi_1,\xi_2,\ldots,\xi_n)$，则
$$
P^{-1}AP=\operatorname{diag}\bigl(1+(n-1)b,\underbrace{1-b,\ldots,1-b}_{n-1\text{ 个}}\bigr).
$$
特别地，当 $b=0$ 时，$A=E$，唯一特征值为 $1$，任意非零向量都是特征向量，且任意可逆矩阵 $P$ 都满足 $P^{-1}AP=E$。

先讨论 $b\ne0$ 的情形。记
$$
\mathbf 1=(1,1,\ldots,1)^T.
$$
则
$$
A\mathbf 1=\bigl(1+(n-1)b\bigr)\mathbf 1,
$$
故
$$
\lambda_1=1+(n-1)b
$$
是一个特征值，其对应特征向量为任意非零倍数的 $\mathbf 1$。

再看满足各分量和为零的向量 $x$，即
$$
x_1+\cdots+x_n=0.
$$
对这类向量，
$$
Ax=(1-b)x,
$$
所以
$$
\lambda_2=\cdots=\lambda_n=1-b
$$
是重根为 $n-1$ 的特征值，其特征子空间可取一组基为
$$
\xi_2=(1,-1,0,\ldots,0)^T,\ 
\xi_3=(1,0,-1,\ldots,0)^T,\ 
\ldots,\ 
\xi_n=(1,0,\ldots,0,-1)^T.
$$

因此当 $b\ne0$ 时，可取
$$
\xi_1=(1,1,\ldots,1)^T,
$$
并令
$$
P=(\xi_1,\xi_2,\ldots,\xi_n),
$$
则
$$
P^{-1}AP=\operatorname{diag}\bigl(1+(n-1)b,\underbrace{1-b,\ldots,1-b}_{n-1\text{ 个}}\bigr).
$$

当 $b=0$ 时，$A=E$，故全部特征值都等于 $1$，任意非零向量都是特征向量，且对任意可逆矩阵 $P$ 都有
$$
P^{-1}AP=E.
$$

### 第22题

- 答案：$(X,Y)$ 的分布为
$$
P(0,0)=\frac23,\quad P(0,1)=\frac1{12},\quad P(1,0)=\frac16,\quad P(1,1)=\frac1{12};
$$

$$
\rho_{XY}=\frac{\sqrt{15}}{15};
$$

$$
P(Z=0)=\frac23,\quad P(Z=1)=\frac14,\quad P(Z=2)=\frac1{12}.
$$

先求
$$
P(AB)=P(A)P(B\mid A)=\frac14\cdot\frac13=\frac1{12}.
$$
又因为
$$
P(A\mid B)=\frac{P(AB)}{P(B)}=\frac12,
$$
故
$$
P(B)=\frac{P(AB)}{P(A\mid B)}=\frac{1/12}{1/2}=\frac16.
$$

于是
$$
P(X=1,Y=1)=P(AB)=\frac1{12},
$$
$$
P(X=1,Y=0)=P(A)-P(AB)=\frac14-\frac1{12}=\frac16,
$$
$$
P(X=0,Y=1)=P(B)-P(AB)=\frac16-\frac1{12}=\frac1{12},
$$
$$
P(X=0,Y=0)=1-\frac1{12}-\frac16-\frac1{12}=\frac23.
$$

再算相关系数。因为
$$
EX=P(A)=\frac14,\qquad EY=P(B)=\frac16,
$$
$$
E(XY)=P(AB)=\frac1{12},
$$
所以
$$
\operatorname{Cov}(X,Y)=E(XY)-EX\cdot EY
=\frac1{12}-\frac14\cdot\frac16
=\frac1{24}.
$$
又
$$
DX=\frac14\left(1-\frac14\right)=\frac3{16},\qquad
DY=\frac16\left(1-\frac16\right)=\frac5{36}.
$$
故
$$
\rho_{XY}
=\frac{\operatorname{Cov}(X,Y)}{\sqrt{DX\cdot DY}}
=\frac{1/24}{\sqrt{(3/16)(5/36)}}
=\frac{\sqrt{15}}{15}.
$$

最后，因 $X,Y$ 仅取 $0,1$，故
$$
Z=X^2+Y^2=X+Y.
$$
于是
$$
P(Z=0)=P(X=0,Y=0)=\frac23,
$$
$$
P(Z=1)=P(X=1,Y=0)+P(X=0,Y=1)=\frac16+\frac1{12}=\frac14,
$$
$$
P(Z=2)=P(X=1,Y=1)=\frac1{12}.
$$

### 第23题

- 答案：当 $\alpha=1$ 时，
$$
\hat\beta_{\text{矩}}=\frac{\overline X}{\overline X-1},\qquad
\hat\beta_{\text{MLE}}=\frac{n}{\sum_{i=1}^n\ln X_i};
$$

当 $\beta=2$ 时，
$$
\hat\alpha_{\text{MLE}}=\min\{X_1,X_2,\ldots,X_n\}.
$$

先由分布函数求密度函数。

当 $\alpha=1$ 时，
$$
F(x;1,\beta)=
\begin{cases}
1-x^{-\beta}, & x>1,\\
0, & x\le1,
\end{cases}
$$
故密度为
$$
f(x;\beta)=
\begin{cases}
\dfrac{\beta}{x^{\beta+1}}, & x>1,\\[4pt]
0, & x\le1.
\end{cases}
$$

1. 矩估计：
$$
EX=\int_1^\infty x\cdot \frac{\beta}{x^{\beta+1}}\,dx=\frac{\beta}{\beta-1}.
$$
令
$$
\overline X=\frac{\beta}{\beta-1},
$$
解得
$$
\hat\beta_{\text{矩}}=\frac{\overline X}{\overline X-1}.
$$

2. 最大似然估计：
样本似然函数为
$$
L(\beta)=\prod_{i=1}^n\frac{\beta}{x_i^{\beta+1}}
=\beta^n\prod_{i=1}^n x_i^{-(\beta+1)}\qquad (x_i>1).
$$
取对数得
$$
\ln L(\beta)=n\ln\beta-(\beta+1)\sum_{i=1}^n\ln x_i.
$$
求导并令其为零：
$$
\frac{d}{d\beta}\ln L(\beta)=\frac{n}{\beta}-\sum_{i=1}^n\ln x_i=0.
$$
故
$$
\hat\beta_{\text{MLE}}=\frac{n}{\sum_{i=1}^n\ln X_i}.
$$

3. 当 $\beta=2$ 时，
$$
f(x;\alpha)=
\begin{cases}
\dfrac{2\alpha^2}{x^3}, & x>\alpha,\\[4pt]
0, & x\le\alpha.
\end{cases}
$$
于是
$$
L(\alpha)=\prod_{i=1}^n \frac{2\alpha^2}{x_i^3},
$$
其成立条件是 $\alpha< x_i$ 对所有 $i$ 都成立，即
$$
\alpha\le \min\{x_1,\ldots,x_n\}.
$$
在该条件下，$L(\alpha)$ 随 $\alpha$ 增大而增大，所以最大似然估计取可行域最大值：
$$
\hat\alpha_{\text{MLE}}=\min\{X_1,X_2,\ldots,X_n\}.
$$
