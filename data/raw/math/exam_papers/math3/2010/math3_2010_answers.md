# 2010 年数学三答案解析

资料类型：考研数学三答案解析
年份：2010
科目：数学三
整理状态：按答案页视觉核对后人工清洗整理。

## 选择题

| 题号 | 答案 |
|---|---|
| 1 | C |
| 2 | A |
| 3 | B |
| 4 | C |
| 5 | A |
| 6 | D |
| 7 | C |
| 8 | A |

## 填空题

| 题号 | 答案 |
|---|---|
| 9 | $-1$ |
| 10 | $\dfrac{\pi^2}{4}$ |
| 11 | $p\cdot e^{(p^3-1)/3}$ |
| 12 | $3$ |
| 13 | $3$ |
| 14 | $\sigma^2+\mu^2$ |

## 解答题

| 题号 | 答案 |
|---|---|
| 15 | $e^{-1}$ |
| 16 | $\dfrac{14}{15}$ |
| 17 | $u_{\max}=5\sqrt5,\quad u_{\min}=-5\sqrt5$ |
| 18 | 1. 有 $\int_0^1\lvert\ln t\rvert[\ln(1+t)]^n\,dt<\int_0^1 t^n\lvert\ln t\rvert\,dt$；2. $\lim_{n\to\infty}u_n=0$ |
| 19 | 命题成立 |
| 20 | $\lambda=-1,\quad a=-2$；通解为 $x=k \begin{pmatrix} 1\\0\\1 \end{pmatrix} + \begin{pmatrix} \frac32\\[2pt]-\frac12\\[2pt]0 \end{pmatrix}, \quad k\in\mathbb R$ |
| 21 | $a=-1$；可取 $Q= \begin{pmatrix} \frac1{\sqrt6} & -\frac1{\sqrt2} & \frac1{\sqrt3}\\[6pt] \frac2{\sqrt6} & 0 & -\frac1{\sqrt3}\\[6pt] \frac1{\sqrt6} & \frac1{\sqrt2} & \frac1{\sqrt3} \end{pmatrix}$ |
| 22 | $A=\frac1\pi$ $f_{Y\mid X}(y\mid x)=\frac1{\sqrt\pi}e^{-(y-x)^2},\qquad -\infty<y<+\infty$ |
| 23 | $\begin{array}{cccc} & Y=0 & Y=1 & Y=2\\ \hline X=0 & \frac15 & \frac25 & \frac1{15}\\[6pt] X=1 & \frac15 & \frac2{15} & 0 \end{array}$ $\operatorname{Cov}(X,Y)=-\frac4{45}$ |

## 详细解析

### 第 1 题

- 答案：C

将极限式整理为
$$
\frac1x-\left(\frac1x-a\right)e^x
=\frac{1-e^x}{x}+ae^x.
$$
当 $x\to0$ 时，
$$
\frac{1-e^x}{x}\to-1,\qquad ae^x\to a.
$$
所以原极限为
$$
-1+a=1,
$$
解得 $a=2$。故选 C。

### 第 2 题

- 答案：A

因为 $\lambda y_1-\mu y_2$ 是齐次方程
$$
y'+p(x)y=0
$$
的解，所以
$$
\lambda\bigl[y_1'+p(x)y_1\bigr]-\mu\bigl[y_2'+p(x)y_2\bigr]=0.
$$
而 $y_1,y_2$ 都满足非齐次方程，因此
$$
(\lambda-\mu)q(x)=0.
$$
由题意知方程非齐次，故 $q(x)\ne0$，从而 $\lambda=\mu$。

又因为 $\lambda y_1+\mu y_2$ 也是原方程的解，所以
$$
\lambda\bigl[y_1'+p(x)y_1\bigr]+\mu\bigl[y_2'+p(x)y_2\bigr]=q(x),
$$
即
$$
(\lambda+\mu)q(x)=q(x).
$$
故 $\lambda+\mu=1$。联立得
$$
\lambda=\mu=\frac12.
$$
选 A。

### 第 3 题

- 答案：B

由复合函数求导，
$$
\{f[g(x)]\}'=f'[g(x)]g'(x),
$$
$$
\{f[g(x)]\}''=f''[g(x)](g'(x))^2+f'[g(x)]g''(x).
$$
由于 $g(x_0)=a$ 是极值点，所以 $g'(x_0)=0$，从而
$$
\{f[g(x_0)]\}''=f'(a)g''(x_0).
$$
又已知 $g''(x_0)<0$，若要使 $f(g(x))$ 在 $x_0$ 处取极大值，只需
$$
\{f[g(x_0)]\}''<0,
$$
因此只需 $f'(a)>0$。选 B。

### 第 4 题

- 答案：C

有
$$
\lim_{x\to+\infty}\frac{h(x)}{g(x)}
=\lim_{x\to+\infty}\frac{e^{x/10}}{x}=+\infty,
$$
所以充分大时 $h(x)>g(x)$。

又
$$
\lim_{x\to+\infty}\frac{f(x)}{g(x)}
=\lim_{x\to+\infty}\frac{\ln^{10}x}{x}=0,
$$
因此充分大时 $f(x)<g(x)$。

综上，充分大时
$$
f(x)<g(x)<h(x).
$$
选 C。

### 第 5 题

- 答案：A

因为向量组 I 可由向量组 II 线性表示，所以
$$
r(\alpha_1,\cdots,\alpha_r)\le r(\beta_1,\cdots,\beta_s)\le s.
$$
若向量组 I 线性无关，则
$$
r(\alpha_1,\cdots,\alpha_r)=r,
$$
于是
$$
r\le s.
$$
故 A 正确。

### 第 6 题

- 答案：D

设 $\lambda$ 是 $A$ 的特征值，则由
$$
A^2+A=O
$$
可得
$$
\lambda^2+\lambda=0,
$$
即
$$
\lambda(\lambda+1)=0.
$$
所以特征值只能是 $0$ 或 $-1$。

又 $A$ 为实对称矩阵，必可对角化；且 $r(A)=3$，说明恰有 3 个非零特征值，因此这 3 个非零特征值都只能是 $-1$，另一个是 0。
故 $A$ 相似于
$$
\operatorname{diag}(-1,-1,-1,0).
$$
选 D。

### 第 7 题

- 答案：C

由分布函数的定义，
$$
P\{X=1\}=F(1)-F(1-0).
$$
其中
$$
F(1)=1-e^{-1},\qquad F(1-0)=\frac12.
$$
所以
$$
P\{X=1\}=1-e^{-1}-\frac12=\frac12-e^{-1}.
$$
选 C。

### 第 8 题

- 答案：A

由概率密度积分为 1，
$$
\int_{-\infty}^{+\infty}f(x)\,dx
=a\int_{-\infty}^{0}f_1(x)\,dx+b\int_0^{+\infty}f_2(x)\,dx=1.
$$
标准正态分布关于 0 对称，所以
$$
\int_{-\infty}^{0}f_1(x)\,dx=\frac12.
$$
而 $f_2(x)=\dfrac14$ 在 $[-1,3]$ 上，故
$$
\int_0^{+\infty}f_2(x)\,dx=\int_0^3\frac14\,dx=\frac34.
$$
因此
$$
\frac a2+\frac{3b}{4}=1
\iff 2a+3b=4.
$$
选 A。

### 第 9 题

- 答案：$-1$

先令 $x=0$，得
$$
\int_0^y e^{-t^2}\,dt=0,
$$
故 $y(0)=0$。

对原方程两边关于 $x$ 求导：
$$
e^{-(x+y)^2}\left(1+\frac{dy}{dx}\right)
=\int_0^x \sin t^2\,dt+x\sin x^2.
$$
代入 $x=0,\ y=0$，得到
$$
1+\left.\frac{dy}{dx}\right|_{x=0}=0,
$$
所以
$$
\left.\frac{dy}{dx}\right|_{x=0}=-1.
$$

### 第 10 题

- 答案：$\dfrac{\pi^2}{4}$

绕 $x$ 轴旋转的体积为
$$
V=\pi\int_e^{+\infty}y^2\,dx
=\pi\int_e^{+\infty}\frac{dx}{x(1+\ln^2x)}.
$$
令 $u=\ln x$，则 $du=\dfrac{dx}{x}$，于是
$$
V=\pi\int_1^{+\infty}\frac{du}{1+u^2}
=\pi\left[\arctan u\right]_1^{+\infty}
=\pi\left(\frac\pi2-\frac\pi4\right)
=\frac{\pi^2}{4}.
$$

### 第 11 题

- 答案：$p\cdot e^{(p^3-1)/3}$

由收益弹性的定义，
$$
\frac{dR}{dp}\cdot\frac{p}{R}=1+p^3.
$$
于是
$$
\frac{dR}{R}=\left(\frac1p+p^2\right)\,dp.
$$
积分得
$$
\ln R=\ln p+\frac13p^3+C.
$$
利用条件 $R(1)=1$，得
$$
0=\frac13+C,
$$
所以 $C=-\dfrac13$。
因此
$$
R(p)=p\cdot e^{(p^3-1)/3}.
$$

### 第 12 题

- 答案：$3$

有
$$
y'=3x^2+2ax+b,\qquad y''=6x+2a.
$$
由于 $(-1,0)$ 是拐点，故
$$
y''(-1)=0,
$$
从而
$$
-6+2a=0\Rightarrow a=3.
$$
又因为点 $(-1,0)$ 在曲线上，
$$
0=(-1)^3+3(-1)^2-b+1=3-b,
$$
所以
$$
b=3.
$$

### 第 13 题

- 答案：$3$

注意到
$$
A(A^{-1}+B)B^{-1}=B^{-1}+A.
$$
取行列式得
$$
|A+B^{-1}|=|A||A^{-1}+B||B^{-1}|.
$$
由 $|B|=2$ 可知
$$
|B^{-1}|=\frac12.
$$
于是
$$
|A+B^{-1}|=3\times2\times\frac12=3.
$$

### 第 14 题

- 答案：$\sigma^2+\mu^2$

由期望的线性性，
$$
E(T)=\frac1n\sum_{i=1}^nE(X_i^2)=E(X^2).
$$
而
$$
E(X^2)=D(X)+[E(X)]^2=\sigma^2+\mu^2.
$$
故
$$
E(T)=\sigma^2+\mu^2.
$$

### 第 15 题

- 答案：$e^{-1}$

设
$$
L=\lim_{x\to+\infty}\left(x^{1/x}-1\right)^{1/\ln x}.
$$
两边取对数，
$$
\ln L=\lim_{x\to+\infty}\frac{\ln(x^{1/x}-1)}{\ln x}.
$$
注意到
$$
x^{1/x}=e^{(\ln x)/x}=1+\frac{\ln x}{x}+o\!\left(\frac{\ln x}{x}\right),
$$
因此
$$
x^{1/x}-1\sim \frac{\ln x}{x}.
$$
故
$$
\ln(x^{1/x}-1)\sim \ln\left(\frac{\ln x}{x}\right)=\ln\ln x-\ln x.
$$
于是
$$
\ln L=\lim_{x\to+\infty}\frac{\ln\ln x-\ln x}{\ln x}=-1.
$$
从而
$$
L=e^{-1}.
$$

### 第 16 题

- 答案：$\dfrac{14}{15}$

区域关于 $x$ 轴对称，可写成
$$
D=D_1\cup D_2,
$$
其中
$$
D_1=\{(x,y)\mid 0\le y\le1,\ \sqrt2y\le x\le\sqrt{1+y^2}\},
$$
$$
D_2=\{(x,y)\mid -1\le y\le0,\ -\sqrt2y\le x\le\sqrt{1+y^2}\}.
$$

展开 integrand：
$$
(x+y)^3=x^3+3x^2y+3xy^2+y^3.
$$
由于区域关于 $x$ 轴对称，且 $3x^2y+y^3$ 关于 $y$ 为奇函数，所以它们在 $D$ 上积分为 0。
故
$$
\iint_D(x+y)^3\,dxdy=\iint_D(x^3+3xy^2)\,dxdy.
$$
再利用对称性，
$$
=2\int_0^1\int_{\sqrt2y}^{\sqrt{1+y^2}}(x^3+3xy^2)\,dx\,dy.
$$
先对 $x$ 积分得
$$
2\int_0^1\left[\frac14x^4+\frac32x^2y^2\right]_{\sqrt2y}^{\sqrt{1+y^2}}dy
=2\int_0^1\left(\frac14+2y^2-\frac94y^4\right)dy
=\frac{14}{15}.
$$

### 第 17 题

- 答案：$u_{\max}=5\sqrt5,\quad u_{\min}=-5\sqrt5$

构造拉格朗日函数
$$
F(x,y,z,\lambda)=xy+2yz+\lambda(x^2+y^2+z^2-10).
$$
由驻点条件得
$$
\begin{cases}
y+2\lambda x=0,\\
x+2z+2\lambda y=0,\\
2y+2\lambda z=0,\\
x^2+y^2+z^2=10.
\end{cases}
$$
解得 6 个驻点：
$$
(1,\sqrt5,2),\ (-1,-\sqrt5,-2),\ (1,-\sqrt5,2),\ (-1,\sqrt5,-2),
$$
$$
(2\sqrt2,0,-\sqrt2),\ (-2\sqrt2,0,\sqrt2).
$$
分别代入
$$
u=xy+2yz
$$
可得
$$
u=5\sqrt5,\ -5\sqrt5,\ -5\sqrt5,\ 5\sqrt5,\ 0,\ 0.
$$
所以
$$
u_{\max}=5\sqrt5,\qquad u_{\min}=-5\sqrt5.
$$

### 第 18 题

- 答案：1. 有
$$
\int_0^1|\ln t|[\ln(1+t)]^n\,dt<\int_0^1 t^n|\ln t|\,dt;
$$

2. 
$$
\lim_{n\to\infty}u_n=0.
$$

对 $0<t<1$，有
$$
0<\ln(1+t)<t.
$$
因此
$$
[\ln(1+t)]^n<t^n.
$$
再乘上非负函数 $|\ln t|$ 并积分，得
$$
\int_0^1|\ln t|[\ln(1+t)]^n\,dt<\int_0^1 t^n|\ln t|\,dt.
$$

又
$$
\int_0^1 t^n|\ln t|\,dt
=-\int_0^1 t^n\ln t\,dt
=\frac1{(n+1)^2}.
$$
所以
$$
0<u_n<\frac1{(n+1)^2}.
$$
由夹逼定理，
$$
\lim_{n\to\infty}u_n=0.
$$

### 第 19 题

- 答案：命题成立

由
$$
\int_0^2 f(x)\,dx=2f(0),
$$
结合积分中值定理，存在 $\eta\in(0,2)$，使得
$$
\int_0^2 f(x)\,dx=2f(\eta).
$$
于是
$$
2f(\eta)=2f(0),
$$
故
$$
f(\eta)=f(0).
$$

再由
$$
f(2)+f(3)=2f(0),
$$
知 $\dfrac{f(2)+f(3)}2=f(0)$。由于 $f$ 在 $[2,3]$ 上连续，故存在 $\eta_1\in(2,3)$ 使
$$
f(\eta_1)=f(0).
$$

于是有
$$
f(0)=f(\eta)=f(\eta_1).
$$
由罗尔定理，存在
$$
\xi_1\in(0,\eta),\qquad \xi_2\in(\eta,\eta_1),
$$
使得
$$
f'(\xi_1)=0,\qquad f'(\xi_2)=0.
$$
再在区间 $[\xi_1,\xi_2]$ 上应用罗尔定理，得到存在 $\xi\in(0,3)$ 使
$$
f''(\xi)=0.
$$

### 第 20 题

- 答案：$$
\lambda=-1,\quad a=-2;
$$

通解为
$$
x=k
\begin{pmatrix}
1\\0\\1
\end{pmatrix}
+
\begin{pmatrix}
\frac32\\[2pt]-\frac12\\[2pt]0
\end{pmatrix},
\quad k\in\mathbb R.
$$

方程组存在两个不同的解，说明它有无穷多解，因此
$$
r(A)=r(\bar A)<3,
$$
从而
$$
|A|=0.
$$
计算得
$$
|A|=(\lambda-1)^2(\lambda+1)=0.
$$
所以 $\lambda=1$ 或 $\lambda=-1$。

若 $\lambda=1$，代入增广矩阵可知
$$
r(A)\ne r(\bar A),
$$
方程组无解，舍去。
故
$$
\lambda=-1.
$$

再代入增广矩阵并行变换，可得必须有
$$
a=-2.
$$

此时方程组化简为
$$
\begin{cases}
x_1-x_3=\dfrac32,\\[4pt]
x_2=-\dfrac12.
\end{cases}
$$
令 $x_3=k$，则
$$
x_1=k+\frac32,\qquad x_2=-\frac12.
$$
故通解为
$$
x=
\begin{pmatrix}
\frac32\\[2pt]-\frac12\\[2pt]0
\end{pmatrix}
+
k
\begin{pmatrix}
1\\0\\1
\end{pmatrix},
\quad k\in\mathbb R.
$$

### 第 21 题

- 答案：$$
a=-1;
$$

可取
$$
Q=
\begin{pmatrix}
\frac1{\sqrt6} & -\frac1{\sqrt2} & \frac1{\sqrt3}\\[6pt]
\frac2{\sqrt6} & 0 & -\frac1{\sqrt3}\\[6pt]
\frac1{\sqrt6} & \frac1{\sqrt2} & \frac1{\sqrt3}
\end{pmatrix}.
$$

因为 $Q$ 的第 1 列是 $A$ 的一个单位特征向量，设对应特征值为 $\lambda_1$，则
$$
A
\begin{pmatrix}
1\\2\\1
\end{pmatrix}
=\lambda_1
\begin{pmatrix}
1\\2\\1
\end{pmatrix}.
$$
计算左端：
$$
\begin{pmatrix}
0&-1&4\\
-1&3&a\\
4&a&0
\end{pmatrix}
\begin{pmatrix}
1\\2\\1
\end{pmatrix}
=
\begin{pmatrix}
2\\
5+a\\
4+2a
\end{pmatrix}.
$$
与 $\lambda_1(1,2,1)^T$ 对比，得
$$
\lambda_1=2,\qquad 5+a=4,\qquad 4+2a=2,
$$
故
$$
a=-1.
$$

于是
$$
A=
\begin{pmatrix}
0&-1&4\\
-1&3&-1\\
4&-1&0
\end{pmatrix}.
$$
计算特征多项式可得特征值为
$$
2,\ -4,\ 5.
$$
分别可取对应特征向量
$$
\xi_1=(1,2,1)^T,\quad \xi_2=(-1,0,1)^T,\quad \xi_3=(1,-1,1)^T.
$$
单位化后得
$$
\eta_1=\frac1{\sqrt6}(1,2,1)^T,\quad
\eta_2=\frac1{\sqrt2}(-1,0,1)^T,\quad
\eta_3=\frac1{\sqrt3}(1,-1,1)^T.
$$
取
$$
Q=(\eta_1,\eta_2,\eta_3)
$$
即可。

### 第 22 题

- 答案：$$
A=\frac1\pi;
$$

$$
f_{Y\mid X}(y\mid x)=\frac1{\sqrt\pi}e^{-(y-x)^2},\qquad -\infty<y<+\infty.
$$

先把指数配方：
$$
-2x^2+2xy-y^2=-x^2-(y-x)^2.
$$
因此
$$
f(x,y)=Ae^{-x^2}e^{-(y-x)^2}.
$$

求 $X$ 的边缘密度：
$$
f_X(x)=\int_{-\infty}^{+\infty}f(x,y)\,dy
=Ae^{-x^2}\int_{-\infty}^{+\infty}e^{-(y-x)^2}\,dy
=A\sqrt\pi\,e^{-x^2}.
$$
再由概率密度积分为 1，
$$
1=\int_{-\infty}^{+\infty}f_X(x)\,dx
=A\sqrt\pi\int_{-\infty}^{+\infty}e^{-x^2}\,dx
=A\pi.
$$
故
$$
A=\frac1\pi.
$$

于是
$$
f_X(x)=\frac1{\sqrt\pi}e^{-x^2}.
$$
条件密度为
$$
f_{Y\mid X}(y\mid x)=\frac{f(x,y)}{f_X(x)}
=\frac{(1/\pi)e^{-x^2}e^{-(y-x)^2}}{(1/\sqrt\pi)e^{-x^2}}
=\frac1{\sqrt\pi}e^{-(y-x)^2}.
$$

### 第 23 题

- 答案：$$
\begin{array}{c|ccc}
 & Y=0 & Y=1 & Y=2\\ \hline
X=0 & \frac15 & \frac25 & \frac1{15}\\[6pt]
X=1 & \frac15 & \frac2{15} & 0
\end{array}
$$

$$
\operatorname{Cov}(X,Y)=-\frac4{45}.
$$

总取法数为
$$
\binom62=15.
$$

各点概率分别为：
$$
P(X=0,Y=0)=\frac{\binom32}{\binom62}=\frac15,
$$
$$
P(X=0,Y=1)=\frac{\binom21\binom31}{\binom62}=\frac25,
$$
$$
P(X=0,Y=2)=\frac{\binom22}{\binom62}=\frac1{15},
$$
$$
P(X=1,Y=0)=\frac{\binom11\binom31}{\binom62}=\frac15,
$$
$$
P(X=1,Y=1)=\frac{\binom11\binom21}{\binom62}=\frac2{15},
$$
$$
P(X=1,Y=2)=0.
$$

于是
$$
E(XY)=1\cdot1\cdot\frac2{15}=\frac2{15}.
$$
再算边缘期望：
$$
E(X)=0\cdot\frac23+1\cdot\frac13=\frac13,
$$
$$
E(Y)=0\cdot\frac25+1\cdot\frac8{15}+2\cdot\frac1{15}=\frac23.
$$
故
$$
\operatorname{Cov}(X,Y)=E(XY)-E(X)E(Y)=\frac2{15}-\frac13\cdot\frac23=-\frac4{45}.
$$
