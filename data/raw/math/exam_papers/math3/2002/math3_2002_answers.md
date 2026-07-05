# 2002 年考研数学三答案与解析

## 2002 数学三第 1 题

### 标准答案

$\displaystyle \frac{1}{1-2a}$

### 解析

注意
$$
\frac{n-2na+1}{n(1-2a)}=1+\frac{1}{n(1-2a)}.
$$
因此原式可写为
$$
\ln\left(1+\frac{1}{n(1-2a)}\right)^n
=n\ln\left(1+\frac{1}{n(1-2a)}\right).
$$
利用极限公式 $\ln(1+t)\sim t\ (t\to0)$，得
$$
\lim_{n\to\infty}n\ln\left(1+\frac{1}{n(1-2a)}\right)
=\lim_{n\to\infty}\frac{n}{n(1-2a)}
=\frac{1}{1-2a}.
$$

## 2002 数学三第 2 题

### 标准答案

$\displaystyle \int_0^{1/2}\!\left(\int_{x^2}^{x} f(x,y)\,dy\right)\,dx$

### 解析

原积分对应的区域由两部分组成：
$$
D_1=\left\{(x,y)\,\middle|\,0\le y\le \frac14,\ y\le x\le \sqrt y\right\},
$$
$$
D_2=\left\{(x,y)\,\middle|\,\frac14\le y\le \frac12,\ y\le x\le \frac12\right\}.
$$
两部分合并后得到
$$
D=\left\{(x,y)\,\middle|\,0\le x\le \frac12,\ x^2\le y\le x\right\}.
$$
因此交换积分次序后，
$$
\iint_D f(x,y)\,d\sigma
=\int_0^{1/2}\!\left(\int_{x^2}^{x} f(x,y)\,dy\right)\,dx.
$$

## 2002 数学三第 3 题

### 标准答案

$-1$

### 解析

先计算
$$
A\alpha
=\begin{pmatrix}
1 & 2 & -2 \\
2 & 1 & 2 \\
3 & 0 & 4
\end{pmatrix}
\begin{pmatrix}
a\\
1\\
1
\end{pmatrix}
=\begin{pmatrix}
a\\
2a+3\\
3a+4
\end{pmatrix}.
$$
因为 $A\alpha$ 与 $\alpha=(a,1,1)^T$ 线性相关，所以存在常数 $k$ 使
$$
\begin{pmatrix}
a\\
2a+3\\
3a+4
\end{pmatrix}
=k
\begin{pmatrix}
a\\
1\\
1
\end{pmatrix}.
$$
比较后两项可得
$$
2a+3=3a+4,
$$
故
$$
a=-1.
$$
代回可验证此时 $A\alpha=\alpha$，条件满足。

## 2002 数学三第 4 题

### 标准答案

$-0.02$

### 解析

由分布表可知
$$
X^2=
\begin{cases}
0,& X=0,\\
1,& X=1,
\end{cases}
\qquad
Y^2=
\begin{cases}
0,& Y=0,\\
1,& Y=\pm1.
\end{cases}
$$
因此
$$
E(X^2)=P(X=1)=0.08+0.32+0.20=0.60,
$$
$$
E(Y^2)=P(Y=\pm1)=0.07+0.08+0.15+0.20=0.50.
$$
又
$$
E(X^2Y^2)=P(X=1,\ Y=\pm1)=0.08+0.20=0.28.
$$
所以
$$
\Cov(X^2,Y^2)=E(X^2Y^2)-E(X^2)E(Y^2)
=0.28-0.60\times0.50
=-0.02.
$$

## 2002 数学三第 5 题

### 标准答案

$\hat\theta=\bar X-1$

### 解析

矩估计法令样本一阶原点矩等于总体一阶原点矩。

先求总体期望：
$$
E(X)=\int_{\theta}^{+\infty}x e^{-(x-\theta)}\,dx.
$$
令 $u=x-\theta$，则
$$
E(X)=\int_0^{+\infty}(u+\theta)e^{-u}\,du
=\theta\int_0^{+\infty}e^{-u}\,du+\int_0^{+\infty}u e^{-u}\,du
=\theta+1.
$$
样本均值为
$$
\bar X=\frac{1}{n}\sum_{i=1}^n X_i.
$$
令
$$
\bar X=E(X)=\theta+1,
$$
即可得到 $\theta$ 的矩估计量
$$
\hat\theta=\bar X-1.
$$

## 2002 数学三第 6 题

### 标准答案

B

### 解析

函数在 $(a,b)$ 内可导，必在 $(a,b)$ 内连续，所以对任意 $\xi\in(a,b)$ 都有
$$
\lim_{x\to \xi}[f(x)-f(\xi)]=0.
$$
因此（B）一定成立。

其余三项都需要比题设更强的条件：

- （A）要由端点异号推出零点存在，需要函数在闭区间 $[a,b]$ 上连续；
- （C）罗尔定理要求函数在 $[a,b]$ 上连续；
- （D）拉格朗日中值定理同样要求函数在 $[a,b]$ 上连续。

题设只说明 $f$ 在 $[a,b]$ 上有定义、在 $(a,b)$ 内可导，不能保证端点处连续，所以（A）（C）（D）都不一定成立。

## 2002 数学三第 7 题

### 标准答案

A

### 解析

由 Cauchy-Hadamard 公式，
$$
\limsup_{n\to\infty}|a_n|^{1/n}=\frac{1}{R_a}=\frac{3}{\sqrt5},
\qquad
\limsup_{n\to\infty}|b_n|^{1/n}=\frac{1}{R_b}=3.
$$
于是
$$
\limsup_{n\to\infty}\left|\frac{a_n^2}{b_n^2}\right|^{1/n}
=\frac{\left(\dfrac{3}{\sqrt5}\right)^2}{3^2}
=\frac{1}{5}.
$$
因此幂级数
$$
\sum_{n=1}^{\infty}\frac{a_n^2}{b_n^2}x^n
$$
的收敛半径为
$$
R=\frac{1}{1/5}=5.
$$
故选 A。

## 2002 数学三第 8 题

### 标准答案

D

### 解析

矩阵 $AB$ 是 $m$ 阶方阵，且
$$
r(AB)\le \min\{r(A),r(B)\}\le n.
$$
当 $m>n$ 时，
$$
r(AB)\le n<m.
$$
因此齐次线性方程组
$$
(AB)x=0
$$
的系数矩阵秩小于未知量个数，必有非零解。

所以正确选项是 D。

## 2002 数学三第 9 题

### 标准答案

B

### 解析

设
$$
B=\left(P^{-1}AP\right)^T.
$$
因为 $A$ 为实对称矩阵，所以 $A^T=A$，从而
$$
B=P^TA(P^{-1})^T.
$$
又因为 $A\alpha=\lambda\alpha$，于是
$$
B(P^T\alpha)
=P^TA(P^{-1})^TP^T\alpha
=P^TA\alpha
=\lambda P^T\alpha.
$$
所以 $P^T\alpha$ 是矩阵 $\left(P^{-1}AP\right)^T$ 属于特征值 $\lambda$ 的特征向量。

故选 B。

## 2002 数学三第 10 题

### 标准答案

C

### 解析

若随机变量服从标准正态分布 $N(0,1)$，则其平方服从自由度为 $1$ 的卡方分布，因此
$$
X^2\sim \chi^2(1),\qquad Y^2\sim \chi^2(1).
$$
所以（C）正确。

而（A）（B）（D）都还需要额外的独立性条件：

- $X+Y$ 服从正态分布，一般需要 $(X,Y)$ 联合正态；
- $X^2+Y^2$ 服从卡方分布，需要 $X,Y$ 相互独立且都服从 $N(0,1)$；
- $X^2/Y^2$ 服从 $F$ 分布，也需要 $X^2,Y^2$ 相互独立。

题目只给出了边缘分布，没有给出独立性，因此只有（C）一定成立。

## 2002 数学三第 11 题

### 标准答案

$\displaystyle \frac{\pi}{6}$

### 解析

当 $t\to0$ 时，
$$
\arctan(1+t)=\arctan 1+o(1)=\frac{\pi}{4}+o(1).
$$
因此当 $u\to0$ 时，
$$
\int_0^{u^2}\arctan(1+t)\,dt
=\int_0^{u^2}\left(\frac{\pi}{4}+o(1)\right)\,dt
=\frac{\pi}{4}u^2+o(u^2).
$$
再对 $u$ 积分可得
$$
\int_0^x\left[\int_0^{u^2}\arctan(1+t)\,dt\right]du
=\int_0^x\left(\frac{\pi}{4}u^2+o(u^2)\right)du
=\frac{\pi}{12}x^3+o(x^3).
$$
另一方面，
$$
1-\cos x=\frac{x^2}{2}+o(x^2),
$$
所以
$$
x(1-\cos x)=\frac{x^3}{2}+o(x^3).
$$
于是原极限为
$$
\lim_{x\to0}\frac{\frac{\pi}{12}x^3+o(x^3)}{\frac{x^3}{2}+o(x^3)}
=\frac{\pi/12}{1/2}
=\frac{\pi}{6}.
$$

## 2002 数学三第 12 题

### 标准答案

$$
du=
\left(f_x+f_z\frac{e^x(x+1)}{e^z(z+1)}\right)dx
+
\left(f_y-f_z\frac{e^y(y+1)}{e^z(z+1)}\right)dy.
$$

### 解析

由全微分公式，
$$
du=f_x\,dx+f_y\,dy+f_z\,dz.
$$
因此关键是求 $dz$。

由隐函数方程
$$
xe^x-ye^y=ze^z
$$
两边求全微分，得
$$
d(xe^x)-d(ye^y)=d(ze^z).
$$
计算各项：
$$
d(xe^x)=e^x(x+1)\,dx,\qquad
d(ye^y)=e^y(y+1)\,dy,\qquad
d(ze^z)=e^z(z+1)\,dz.
$$
于是
$$
e^x(x+1)\,dx-e^y(y+1)\,dy=e^z(z+1)\,dz,
$$
从而
$$
dz=\frac{e^x(x+1)\,dx-e^y(y+1)\,dy}{e^z(z+1)}.
$$
代回 $du=f_x\,dx+f_y\,dy+f_z\,dz$，整理得
$$
du=
\left(f_x+f_z\frac{e^x(x+1)}{e^z(z+1)}\right)dx
+
\left(f_y-f_z\frac{e^y(y+1)}{e^z(z+1)}\right)dy.
$$

## 2002 数学三第 13 题

### 标准答案

$\displaystyle 2\bigl(\sqrt{x}-\sqrt{1-x}\,\arcsin\sqrt{x}\bigr)+C$

### 解析

先由已知关系求 $f(x)$ 的表达式。令
$$
u=\sin^2 x,
$$
则 $\sin x=\sqrt u$，并且 $x=\arcsin\sqrt u$，所以
$$
f(u)=\frac{x}{\sin x}=\frac{\arcsin\sqrt u}{\sqrt u}.
$$
把自变量再记回 $x$，得到
$$
f(x)=\frac{\arcsin\sqrt x}{\sqrt x}.
$$
于是原积分化为
$$
\int \frac{\sqrt x}{\sqrt{1-x}}f(x)\,dx
=\int \frac{\arcsin\sqrt x}{\sqrt{1-x}}\,dx.
$$
令
$$
\sqrt x=\sin t\quad (x=\sin^2 t),
$$
则
$$
dx=2\sin t\cos t\,dt,\qquad \arcsin\sqrt x=t.
$$
故原积分为
$$
\int \frac{t}{\cos t}\cdot 2\sin t\cos t\,dt
=2\int t\sin t\,dt.
$$
分部积分得
$$
2\int t\sin t\,dt
=2(-t\cos t+\sin t)+C.
$$
再代回 $t=\arcsin\sqrt x$、$\sin t=\sqrt x$、$\cos t=\sqrt{1-x}$，得
$$
\int \frac{\sqrt{x}}{\sqrt{1-x}} f(x)\,dx
=2\bigl(\sqrt{x}-\sqrt{1-x}\,\arcsin\sqrt{x}\bigr)+C.
$$

## 2002 数学三第 14 题

### 标准答案

$$
V_1=\frac{4\pi}{5}(32-a^5),\qquad
V_2=\pi a^4;
$$
$$
a=1,\qquad \max(V_1+V_2)=\frac{129\pi}{5}.
$$

### 解析

对 $D_1$ 绕 $x$ 轴旋转，用圆盘法：
$$
V_1=\pi\int_a^2 (2x^2)^2\,dx
=4\pi\int_a^2 x^4\,dx
=\frac{4\pi}{5}(32-a^5).
$$

对 $D_2$ 绕 $y$ 轴旋转，用柱壳法：
$$
V_2=2\pi\int_0^a x\cdot 2x^2\,dx
=4\pi\int_0^a x^3\,dx
=\pi a^4.
$$

因此
$$
V(a)=V_1+V_2=\frac{4\pi}{5}(32-a^5)+\pi a^4.
$$
求导得
$$
V'(a)=-4\pi a^4+4\pi a^3
=4\pi a^3(1-a).
$$
由 $0<a<2$ 可知，驻点只有 $a=1$。

并且
$$
V'(a)>0\quad (0<a<1),\qquad
V'(a)<0\quad (1<a<2),
$$
所以 $a=1$ 时取得最大值。

最大值为
$$
V(1)=\frac{4\pi}{5}(32-1)+\pi
=\frac{124\pi}{5}+\frac{5\pi}{5}
=\frac{129\pi}{5}.
$$

## 2002 数学三第 15 题

### 标准答案

C

### 解析

记
$$
b_n=\frac{1}{u_n}.
$$
则所给级数的前 $N$ 项和为
$$
S_N=\sum_{n=1}^N(-1)^{n+1}(b_n+b_{n+1}).
$$
展开后可见它是错位相消的：
$$
S_N=(b_1+b_2)-(b_2+b_3)+(b_3+b_4)-\cdots+(-1)^{N+1}(b_N+b_{N+1}),
$$
于是
$$
S_N=b_1+(-1)^{N+1}b_{N+1}.
$$
又因为
$$
\lim_{n\to\infty}\frac{n}{u_n}=1,
$$
所以
$$
\lim_{n\to\infty}b_n=\lim_{n\to\infty}\frac{1}{u_n}=0.
$$
故
$$
\lim_{N\to\infty}S_N=b_1=\frac{1}{u_1},
$$
级数收敛。

再考察绝对收敛性。由 $\dfrac{n}{u_n}\to1$ 得
$$
\frac{1}{u_n}\sim\frac{1}{n},\qquad
\frac{1}{u_{n+1}}\sim\frac{1}{n+1},
$$
从而
$$
\left|\frac{1}{u_n}+\frac{1}{u_{n+1}}\right|
\sim \frac{1}{n}+\frac{1}{n+1}
\sim \frac{2}{n}.
$$
因此绝对值级数与调和级数同阶，发散。

所以该级数是条件收敛，选 C。

## 2002 数学三第 16 题

### 标准答案

存在 $\xi\in[a,b]$，使
$$
\int_a^b f(x)g(x)\,dx=f(\xi)\int_a^b g(x)\,dx.
$$

### 解析

因为 $f$ 在闭区间 $[a,b]$ 上连续，所以它能取到最大值与最小值。设
$$
m=\min_{x\in[a,b]}f(x),\qquad M=\max_{x\in[a,b]}f(x).
$$
则对任意 $x\in[a,b]$ 都有
$$
m\le f(x)\le M.
$$
又由于 $g(x)>0$，两边同乘 $g(x)$ 得
$$
mg(x)\le f(x)g(x)\le Mg(x).
$$
对区间 $[a,b]$ 积分，得
$$
m\int_a^b g(x)\,dx
\le
\int_a^b f(x)g(x)\,dx
\le
M\int_a^b g(x)\,dx.
$$
由于 $g(x)>0$ 且连续，故
$$
\int_a^b g(x)\,dx>0.
$$
于是可将上式同除以 $\int_a^b g(x)\,dx$，得到
$$
m\le \frac{\int_a^b f(x)g(x)\,dx}{\int_a^b g(x)\,dx}\le M.
$$
而 $f$ 在 $[a,b]$ 上连续，所以由介值定理，存在 $\xi\in[a,b]$ 使
$$
f(\xi)=\frac{\int_a^b f(x)g(x)\,dx}{\int_a^b g(x)\,dx}.
$$
移项即得
$$
\int_a^b f(x)g(x)\,dx=f(\xi)\int_a^b g(x)\,dx.
$$

## 2002 数学三第 17 题

### 标准答案

设 $A$ 为系数矩阵，则
$$
A=(a-b)I_n+bJ_n,
$$
其中 $J_n$ 为全 $1$ 矩阵。故 $A$ 的特征值为
$$
a-b\quad(\text{重数 }n-1),\qquad a+(n-1)b\quad(\text{重数 }1).
$$

因此：

1. 当 $a\ne b$ 且 $a\ne -(n-1)b$ 时，方程组仅有零解；
2. 当 $a=b$ 时，方程组有无穷多组解，解满足
   $$
   x_1+x_2+\cdots+x_n=0;
   $$
   一组基础解系可取
   $$
   \xi_1=(-1,1,0,\ldots,0)^T,\ 
   \xi_2=(-1,0,1,\ldots,0)^T,\ \ldots,\ 
   \xi_{n-1}=(-1,0,\ldots,0,1)^T.
   $$
3. 当 $a=-(n-1)b$ 时，方程组有无穷多组解，解满足
   $$
   x_1=x_2=\cdots=x_n;
   $$
   一组基础解系可取
   $$
   \xi=(1,1,\ldots,1)^T.
   $$

### 解析

系数矩阵可写成
$$
A=(a-b)I_n+bJ_n,
$$
其中 $J_n$ 是全 $1$ 矩阵。

已知 $J_n$ 的特征值为：

- $n$，对应特征向量 $(1,1,\ldots,1)^T$；
- $0$，重数为 $n-1$，对应所有满足各分量和为 $0$ 的向量。

所以 $A=(a-b)I_n+bJ_n$ 的特征值为
$$
a-b\quad(\text{重数 }n-1),\qquad a-b+bn=a+(n-1)b\quad(\text{重数 }1).
$$
齐次线性方程组 $AX=0$：

- 仅有零解，当且仅当 $0$ 不是 $A$ 的特征值，即
  $$
  a-b\ne0,\qquad a+(n-1)b\ne0.
  $$
  也就是
  $$
  a\ne b,\qquad a\ne -(n-1)b.
  $$

- 有无穷多组解，当且仅当上面两式之一成立。

下面分别写出解集。

当 $a=b$ 时，
$$
A=bJ_n,
$$
方程组化为
$$
x_1+x_2+\cdots+x_n=0.
$$
取 $x_2,\ldots,x_n$ 为自由变量，就得到一组基础解系
$$
\xi_1=(-1,1,0,\ldots,0)^T,\ 
\xi_2=(-1,0,1,\ldots,0)^T,\ \ldots,\ 
\xi_{n-1}=(-1,0,\ldots,0,1)^T.
$$
全部解为
$$
X=k_1\xi_1+k_2\xi_2+\cdots+k_{n-1}\xi_{n-1}.
$$

当 $a=-(n-1)b$ 时，零特征值对应的特征向量就是
$$
\xi=(1,1,\ldots,1)^T.
$$
所以全部解为
$$
X=k\xi,\qquad k\in\mathbb R.
$$

## 2002 数学三第 18 题

### 标准答案

$A$ 的全部特征值为 $-2,-2,0$；当且仅当 $k>2$ 时，$A+kE$ 为正定矩阵。

### 解析

设 $\lambda$ 是 $A$ 的任一特征值，$\alpha\ne0$ 是对应特征向量，则
$$
A\alpha=\lambda\alpha.
$$
两边再左乘 $A$，得
$$
A^2\alpha=\lambda^2\alpha.
$$
由条件 $A^2+2A=0$，可得
$$
(A^2+2A)\alpha=0
\Longrightarrow
(\lambda^2+2\lambda)\alpha=0.
$$
因为 $\alpha\ne0$，所以
$$
\lambda^2+2\lambda=0,
$$
即
$$
\lambda=0\quad \text{或}\quad \lambda=-2.
$$

又因为 $A$ 为三阶实对称矩阵，所以它可对角化；并且 $r(A)=2$，说明恰有两个非零特征值和一个零特征值。故 $A$ 的全部特征值为
$$
-2,\ -2,\ 0.
$$

对于矩阵 $A+kE$，若 $\lambda$ 是 $A$ 的特征值，则 $\lambda+k$ 是 $A+kE$ 的特征值，因此 $A+kE$ 的特征值为
$$
k-2,\ k-2,\ k.
$$
实对称矩阵正定，当且仅当全部特征值都大于零，所以需满足
$$
k-2>0,\qquad k>0.
$$
综合得
$$
k>2.
$$

## 2002 数学三第 19 题

### 标准答案

$$
\begin{array}{c|cc}
X\backslash Y & -1 & 1 \\
\hline
-1 & \frac14 & 0 \\
1 & \frac12 & \frac14
\end{array}
$$
$$
D(X+Y)=2.
$$

### 解析

因为 $U\sim U[-2,2]$，区间长度为 $4$。

先求联合分布：

- 当 $X=-1,\ Y=-1$ 时，必须有 $U\le -1$，故
  $$
  P(X=-1,Y=-1)=P(U\le -1)=\frac{1}{4};
  $$
- 当 $X=-1,\ Y=1$ 时，需要同时满足 $U\le -1$ 与 $U>1$，这是不可能事件，故
  $$
  P(X=-1,Y=1)=0;
  $$
- 当 $X=1,\ Y=-1$ 时，对应 $-1<U\le1$，故
  $$
  P(X=1,Y=-1)=\frac{2}{4}=\frac12;
  $$
- 当 $X=1,\ Y=1$ 时，对应 $U>1$，故
  $$
  P(X=1,Y=1)=\frac{1}{4}.
  $$

于是得到联合分布表
$$
\begin{array}{c|cc}
X\backslash Y & -1 & 1 \\
\hline
-1 & \frac14 & 0 \\
1 & \frac12 & \frac14
\end{array}
$$

再求 $D(X+Y)$。由上表知
$$
X+Y=
\begin{cases}
-2,& P=\frac14,\\
0,& P=\frac12,\\
2,& P=\frac14.
\end{cases}
$$
因此
$$
E(X+Y)=(-2)\cdot\frac14+0\cdot\frac12+2\cdot\frac14=0,
$$
$$
E[(X+Y)^2]=(-2)^2\cdot\frac14+0^2\cdot\frac12+2^2\cdot\frac14=2.
$$
所以
$$
D(X+Y)=E[(X+Y)^2]-[E(X+Y)]^2=2-0=2.
$$

## 2002 数学三第 20 题

### 标准答案

$$
F_Y(y)=
\begin{cases}
0, & y<0, \\
1-e^{-y/5}, & 0\le y<2, \\
1, & y\ge 2.
\end{cases}
$$

### 解析

由题意，设备每次实际无故障工作时间为
$$
Y=\min(X,2).
$$
又因为 $X$ 服从指数分布，且
$$
E(X)=\frac{1}{\lambda}=5,
$$
所以
$$
\lambda=\frac15.
$$
于是
$$
F_X(x)=
\begin{cases}
0, & x<0,\\
1-e^{-x/5}, & x\ge0.
\end{cases}
$$

下面分段讨论 $F_Y(y)=P(Y\le y)$：

1. 当 $y<0$ 时，$Y\ge0$，故
   $$
   F_Y(y)=0.
   $$

2. 当 $0\le y<2$ 时，
   $$
   \{Y\le y\}=\{\min(X,2)\le y\}=\{X\le y\},
   $$
   因而
   $$
   F_Y(y)=P(X\le y)=1-e^{-y/5}.
   $$

3. 当 $y\ge2$ 时，由于 $Y=\min(X,2)\le2$ 恒成立，所以
   $$
   F_Y(y)=1.
   $$

综上，
$$
F_Y(y)=
\begin{cases}
0, & y<0, \\
1-e^{-y/5}, & 0\le y<2, \\
1, & y\ge 2.
\end{cases}
$$
其中在 $y=2$ 处有跳跃，跳跃大小为
$$
P(Y=2)=P(X\ge2)=e^{-2/5}.
$$
