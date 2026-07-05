# Math 1 2018 Answers

资料类型：考研数学一答案解析
年份：2018
科目：数学一
校对状态：已依据本年份题目卡片与 `images/answer_pages/` 页面图片人工清洗并补全

## 选择题

| 题号 | 标准答案 |
|---|---|
| 1 | D |
| 2 | B |
| 3 | B |
| 4 | C |
| 5 | A |
| 6 | A |
| 7 | A |
| 8 | D |

## 填空题

| 题号 | 标准答案 |
|---|---|
| 9 | $-2$ |
| 10 | $2(\ln 2-1)$ |
| 11 | $i-k$ |
| 12 | $-\pi/3$ |
| 13 | $-1$ |
| 14 | $1/4$ |

## 解答题

| 题号 | 标准答案 |
|---|---|
| 15 | $\frac{1}{2} e^{2x}\arctan\sqrt{e^x-1}-\frac{1}{6}(e^x+2)\sqrt{e^x-1}+C$ |
| 16 | $\dfrac{1}{\pi+4+3\sqrt{3}}$ |
| 17 | $I=\dfrac{14\pi}{45}$ |
| 18 | （1）$y=x-1+Ce^{-x}$；（2）方程存在唯一的以 $T$ 为周期的解。 |
| 19 | 数列收敛，且 $\lim_{n\to\infty}x_n=0$。 |
| 20 | （1）当 $a\ne 2$ 时仅有零解；当 $a=2$ 时，解为 $x=k(-2,-1,1)^T$。 （2）当 $a\ne 2$ 时规范形为 $y_1^2+y_2^2+y_3^2$；当 $a=2$ 时规范形为 $y_1^2+y_2^2$。 |
| 21 | （1）$a=2$。 （2）可取 $P=\begin{pmatrix}3&-2&4\\-1&1&-1\\0&1&0\end{pmatrix}$；更一般地，$P=\begin{pmatrix}3-6k_1&4-6k_2&4-6k_3\\-1+2k_1&-1+2k_2&-1+2k_3\\k_1&k_2&k_3\end{pmatrix}$，其中 $k_2\ne k_3$。 |
| 22 | （1）$\operatorname{Cov}(X,Z)=\lambda$。 （2）对任意整数 $i$，$P(Z=0)=e^{-\lambda}$；当 $i>0$ 时，$P(Z=i)=\dfrac{1}{2}\dfrac{\lambda^i e^{-\lambda}}{i!}$；当 $i<0$ 时，$P(Z=i)=\dfrac{1}{2}\dfrac{\lambda^{-i} e^{-\lambda}}{(-i)!}$。 |
| 23 | （1）$\hat\sigma=\dfrac{1}{n}\sum_{i=1}^n \lvert X_i\rvert$。 （2）$E(\hat\sigma)=\sigma$，$D(\hat\sigma)=\dfrac{\sigma^2}{n}$。 |

## 详细解析

### 第 1 题

**标准答案：** D

对于 D 选项，$f(x)=\cos\sqrt{|x|}$。

当 $x\to 0^+$ 时，
$$
f'_+(0)=\lim_{x\to 0^+}\frac{\cos\sqrt{x}-1}{x}
=\lim_{x\to 0^+}\frac{-\tfrac{1}{2} x+o(x)}{x}
=-\frac{1}{2}.
$$

当 $x\to 0^-$ 时，
$$
f'_-(0)=\lim_{x\to 0^-}\frac{\cos\sqrt{-x}-1}{x}
=\lim_{x\to 0^-}\frac{\tfrac{1}{2} x+o(x)}{x}
=\frac{1}{2}.
$$

左右导数不相等，所以在 $x=0$ 处不可导，故选 D。

### 第 2 题

**标准答案：** B

平面过点 $(1,0,0)$、$(0,1,0)$，故平面内有方向向量 $(1,-1,0)$。曲面 $z=x^2+y^2$ 在点 $(x,y,z)$ 处的切平面法向量为 $(2x,2y,-1)$。

由于该方向向量在切平面内，应与法向量垂直，于是
$$
(1,-1,0)\cdot(2x,2y,-1)=2x-2y=0,
$$
故 $x=y$，选 B。

### 第 3 题

**标准答案：** B

原式可写成
$$
\sum_{n=0}^{\infty}\frac{(-1)^n}{(2n)!}
+2\sum_{n=0}^{\infty}\frac{(-1)^n}{(2n+1)!}.
$$

利用展开式
$$
\cos x=\sum_{n=0}^{\infty}\frac{(-1)^n x^{2n}}{(2n)!},\qquad
\sin x=\sum_{n=0}^{\infty}\frac{(-1)^n x^{2n+1}}{(2n+1)!},
$$
令 $x=1$，得原式为 $\cos 1+2\sin 1$，故选 B。

### 第 4 题

**标准答案：** C

由题中定义
$$
M=\int_{-\pi/2}^{\pi/2}\frac{(1+x)^2}{1+x^2}\,dx
=\int_{-\pi/2}^{\pi/2}\left(1+\frac{2x}{1+x^2}\right)dx.
$$

其中 $\dfrac{2x}{1+x^2}$ 为奇函数，在对称区间上积分为 $0$，所以
$$
M=\int_{-\pi/2}^{\pi/2}1\,dx=\pi.
$$

再由题中对 $K,N$ 的比较可得 $K>\pi>N$，因此 $K>M>N$，选 C。

### 第 5 题

**标准答案：** A

记原矩阵为
$$
J=\begin{pmatrix}
1&1&0\\
0&1&1\\
0&0&1
\end{pmatrix}.
$$
矩阵 $J$ 只有特征值 $1$，且
$$
r(J-E)=2,
\qquad
(J-E)^2\ne O,
\qquad
(J-E)^3=O.
$$
因此 $J$ 对应特征值 $1$ 的 Jordan 块大小为 $3$。

逐项考察 $M-E$ 的秩与幂零阶。A 选项满足
$$
r(M-E)=2,
\qquad
(M-E)^2\ne O,
\qquad
(M-E)^3=O,
$$
与 $J$ 有相同的 Jordan 结构；而 B、C、D 选项均有 $r(M-E)=1$，Jordan 结构不同。

所以与原矩阵相似的是 A。

### 第 6 题

**标准答案：** A

A 正确。$AB$ 的每一列都是 $A$ 的列向量的线性组合，因此
$$
\operatorname{col}(AB)\subseteq \operatorname{col}(A),
$$
从而
$$
r(A,AB)=r(A).
$$

下面用反例排除其余选项。取
$$
A=\begin{pmatrix}1&0\\0&0\end{pmatrix},
\qquad
B=\begin{pmatrix}0&0\\1&0\end{pmatrix}.
$$
则 $r(A)=r(B)=1$，且
$$
BA=\begin{pmatrix}0&0\\1&0\end{pmatrix},
\qquad
(A,BA)=
\begin{pmatrix}1&0&0&0\\0&0&1&0\end{pmatrix},
$$
所以 $r(A,BA)=2\ne r(A)$，B 错误。

又
$$
(A,B)=
\begin{pmatrix}1&0&0&0\\0&0&1&0\end{pmatrix},
$$
故 $r(A,B)=2\ne\max\{r(A),r(B)\}$，C 错误。

同时
$$
(A^T,B^T)=
\begin{pmatrix}1&0&0&1\\0&0&0&0\end{pmatrix},
$$
所以 $r(A^T,B^T)=1\ne r(A,B)$，D 错误。

综上，正确选项为 A。

### 第 7 题

**标准答案：** A

由 $f(1+x)=f(1-x)$ 可知，$f(x)$ 关于 $x=1$ 对称，所以
$$
\int_{-\infty}^{1}f(x)\,dx=\int_{1}^{+\infty}f(x)\,dx=\frac{1}{2}.
$$

又已知
$$
\int_0^2 f(x)\,dx=0.6,
$$
由对称性知
$$
\int_0^1 f(x)\,dx=\int_1^2 f(x)\,dx=0.3.
$$

于是
$$
P(X<0)=\int_{-\infty}^0 f(x)\,dx
=\int_{-\infty}^1 f(x)\,dx-\int_0^1 f(x)\,dx
=0.5-0.3=0.2.
$$
故选 A。

### 第 8 题

**标准答案：** D

显著性水平 $\alpha=0.05$ 时接受 $H_0$，说明双侧检验统计量满足
$$
|Z|\le u_{0.025}.
$$

而标准正态分布分位点满足 $u_{0.025}<u_{0.005}$，故必有
$$
|Z|\le u_{0.005}.
$$

因此正确选项为 D。

### 第 9 题

**标准答案：** $-2$

由题设极限等于 $e$，可化为
$$
\lim_{x\to 0}\frac{\dfrac{1-\tan x}{1+\tan x}-1}{\sin kx}=1.
$$

分子整理得
$$
\frac{1-\tan x}{1+\tan x}-1=\frac{-2\tan x}{1+\tan x},
$$
于是
$$
\lim_{x\to 0}\frac{-2\tan x}{(1+\tan x)\sin kx}
=\lim_{x\to 0}\frac{-2x}{kx}=1.
$$

故 $k=-2$。

### 第 10 题

**标准答案：** $2(\ln 2-1)$

由 $y=f(x)$ 过点 $(0,0)$，得 $f(0)=0$。又曲线 $y=f(x)$ 与 $y=2^x$ 在点 $(1,2)$ 相切，所以
$$
f(1)=2,\qquad f'(1)=2\ln 2.
$$

由分部积分，
$$
\int_0^1 x f''(x)\,dx=\bigl[x f'(x)\bigr]_0^1-\int_0^1 f'(x)\,dx
=f'(1)-\bigl(f(1)-f(0)\bigr).
$$

故
$$
\int_0^1 x f''(x)\,dx=2\ln 2-2=2(\ln 2-1).
$$

### 第 11 题

**标准答案：** $i-k$

由旋度定义，
$$
\operatorname{rot}F=
\begin{vmatrix}
i & j & k \\
\partial/\partial x & \partial/\partial y & \partial/\partial z \\
xy & -yz & xz
\end{vmatrix}
=(y,-z,-x).
$$

再与题中向量 $(1,1,0)$ 作叉乘，可得
$$
(y,-z,-x)\perp(1,1,0),\qquad
\operatorname{rot}F=(1,0,-1)=i-k.
$$

故应填 $i-k$。

### 第 12 题

**标准答案：** $-\pi/3$

曲线 $L$ 为
$$
\begin{cases}
x^2+y^2+z^2=1,\\
x+y+z=0.
\end{cases}
$$

由平面方程得
$$
z=-(x+y),
$$
代入球面方程可化简出
$$
xy=\frac{1}{2}-(x^2+y^2).
$$

由于 $L$ 是该平面与单位球的交圆，圆上平均有
$$
x^2+y^2=\frac{2}{3}.
$$

因此
$$
\oint_L xy\,ds
=\oint_L\left(\frac{1}{2}-(x^2+y^2)\right)ds
=\oint_L\left(\frac{1}{2}-\frac{2}{3}\right)ds
=-\frac{1}{6}\cdot 2\pi
=-\frac{\pi}{3}.
$$

### 第 13 题

**标准答案：** $-1$

设矩阵 $A$ 的两个特征值为 $\lambda_1,\lambda_2$，对应特征向量分别为 $\alpha_1,\alpha_2$。

由题设可推出
$$
A(\alpha_1+\alpha_2)=\lambda_1\alpha_1+\lambda_2\alpha_2,
$$
且
$$
A^2(\alpha_1+\alpha_2)=\lambda_1^2\alpha_1+\lambda_2^2\alpha_2=\alpha_1+\alpha_2.
$$

故
$$
\lambda_1^2=1,\qquad \lambda_2^2=1,
$$
即 $\lambda_1,\lambda_2\in\{1,-1\}$。又因 $\lambda_1\ne\lambda_2$，所以
$$
\det A=\lambda_1\lambda_2=-1.
$$

故应填 $-1$。

### 第 14 题

**标准答案：** $1/4$

由条件概率公式，
$$
P(AC\mid AB\cup C)\cdot P(AB\cup C)=P(AC).
$$

把题设数值代入，
$$
\frac{1}{4}\left(\frac{1}{4}+P(C)\right)=\frac{1}{2} P(C).
$$

整理得
$$
P(C)=\frac{1}{4}.
$$

故应填 $\dfrac{1}{4}$。

### 第 15 题

**标准答案：** $\frac{1}{2} e^{2x}\arctan\sqrt{e^x-1}-\frac{1}{6}(e^x+2)\sqrt{e^x-1}+C$

设
$$
I=\int e^{2x}\arctan\sqrt{e^x-1}\,dx.
$$

分部积分，取
$$
u=\arctan\sqrt{e^x-1},\qquad dv=e^{2x}dx,
$$
则
$$
I=\frac{1}{2} e^{2x}\arctan\sqrt{e^x-1}-\frac{1}{4}\int \frac{e^{2x}}{\sqrt{e^x-1}}\,dx.
$$

再令 $t=e^x$，则
$$
\int \frac{e^{2x}}{\sqrt{e^x-1}}\,dx
=\int \frac{t}{\sqrt{t-1}}\,dt
=\int \sqrt{t-1}\,dt+\int \frac{1}{\sqrt{t-1}}\,dt
=\frac{2}{3}(t-1)^{3/2}+2\sqrt{t-1}.
$$

代回得
$$
I=\frac{1}{2} e^{2x}\arctan\sqrt{e^x-1}-\frac{1}{6}(e^x+2)\sqrt{e^x-1}+C.
$$

### 第 16 题

**标准答案：** $\dfrac{1}{\pi+4+3\sqrt{3}}$

设圆半径为 $x$，正方形边长为 $y$，正三角形边长为 $z$，则总长度约束为
$$
2\pi x+4y+3z=2,\qquad x>0,\ y>0,\ z>0.
$$

总面积为
$$
f(x,y,z)=\pi x^2+y^2+\frac{\sqrt{3}}{4}z^2.
$$

作拉格朗日函数
$$
L=\pi x^2+y^2+\frac{\sqrt{3}}{4}z^2+\lambda(2\pi x+4y+3z-2),
$$
解方程组得驻点
$$
x_0=\frac{1}{\pi+4+3\sqrt{3}},\quad
y_0=\frac{2}{\pi+4+3\sqrt{3}},\quad
z_0=\frac{2\sqrt{3}}{\pi+4+3\sqrt{3}}.
$$

此时
$$
f(x_0,y_0,z_0)=\frac{1}{\pi+4+3\sqrt{3}}.
$$

再检查边界 $xyz=0$ 的情形，可得边界最小值为
$$
\frac{1}{4+3\sqrt{3}},
$$
大于内部驻点处的值。因此最小值存在，且为
$$
\frac{1}{\pi+4+3\sqrt{3}}.
$$

### 第 17 题

**标准答案：** $I=\dfrac{14\pi}{45}$

设 $\Sigma_1$ 为平面 $x=0$ 上由
$$
3y^2+3z^2\le 1
$$
围成部分的后侧，$\Omega$ 为 $\Sigma$ 与 $\Sigma_1$ 围成的立体。

由高斯公式，
$$
\iint_{\Sigma+\Sigma_1}x\,dy\,dz+(y^3+2)\,dz\,dx+z^3\,dx\,dy
=\iiint_\Omega (1+3y^2+3z^2)\,dx\,dy\,dz.
$$

对右端取极坐标 $y=r\cos\theta,\ z=r\sin\theta$，得
$$
\iiint_\Omega (1+3y^2+3z^2)\,dx\,dy\,dz
=2\pi\int_0^{\sqrt{3}/3} r(1+3r^2)\sqrt{1-3r^2}\,dr
=\frac{14\pi}{45}.
$$

而在底面 $\Sigma_1$ 上有 $x=0$，故
$$
\iint_{\Sigma_1}x\,dy\,dz+(y^3+2)\,dz\,dx+z^3\,dx\,dy=0.
$$

因此
$$
I=\frac{14\pi}{45}.
$$

### 第 18 题

**标准答案：** （1）$y=x-1+Ce^{-x}$；（2）方程存在唯一的以 $T$ 为周期的解。

（1）当 $f(x)=x$ 时，方程
$$
y'+y=x
$$
的通解为
$$
y=e^{-x}\left(C+\int xe^x\,dx\right)=Ce^{-x}+x-1.
$$

（2）一般地，方程 $y'+y=f(x)$ 的通解为
$$
y(x)=e^{-x}\left(C+\int_0^x e^t f(t)\,dt\right).
$$

于是
$$
y(x+T)-y(x)
=e^{-x}\left[\left(\frac{1}{e^T}-1\right)C+\frac{1}{e^T}\int_0^T e^t f(t)\,dt\right].
$$

要使 $y$ 为 $T$ 周期解，只需且只需对一切 $x$ 有 $y(x+T)-y(x)=0$，故常数 $C$ 必须满足
$$
C=\frac{1}{e^T-1}\int_0^T e^t f(t)\,dt.
$$

该常数唯一确定，所以方程存在唯一的以 $T$ 为周期的解。

### 第 19 题

**标准答案：** 数列收敛，且 $\lim_{n\to\infty}x_n=0$。

由递推关系
$$
x_n e^{x_{n+1}}=e^{x_n}-1
$$
可得
$$
e^{x_{n+1}}=\frac{e^{x_n}-1}{x_n}.
$$

由微分中值定理，存在 $\xi_n\in(0,x_n)$，使得
$$
\frac{e^{x_n}-1}{x_n}=e^{\xi_n}.
$$

因此
$$
e^{x_{n+1}}=e^{\xi_n},
$$
从而 $0<x_{n+1}<x_n$。故 $\{x_n\}$ 单调递减且有下界 $0$，所以收敛。

设 $\lim\limits_{n\to\infty}x_n=a\ge 0$，则由递推式取极限得
$$
ae^a=e^a-1.
$$

令
$$
\varphi(x)=xe^x-e^x+1,
$$
则
$$
\varphi'(x)=xe^x>0\quad (x>0),
$$
故 $\varphi$ 在 $[0,+\infty)$ 上单调递增，而 $\varphi(0)=0$，所以方程在 $[0,+\infty)$ 上唯一解为 $a=0$。

于是
$$
\lim_{n\to\infty}x_n=0.
$$

### 第 20 题

**标准答案：** （1）当 $a\ne 2$ 时仅有零解；当 $a=2$ 时，解为 $x=k(-2,-1,1)^T$。 （2）当 $a\ne 2$ 时规范形为 $y_1^2+y_2^2+y_3^2$；当 $a=2$ 时规范形为 $y_1^2+y_2^2$。

（1）由 $f(x_1,x_2,x_3)=0$ 当且仅当
$$
\begin{cases}
x_1-x_2+x_3=0,\\
x_2+x_3=0,\\
x_1+ax_3=0.
\end{cases}
$$

其系数矩阵经初等行变换化为
$$
\begin{pmatrix}
1 & -1 & 1 \\
0 & 1 & 1 \\
1 & 0 & a
\end{pmatrix}
\sim
\begin{pmatrix}
1 & 0 & 2 \\
0 & 1 & 1 \\
0 & 0 & a-2
\end{pmatrix}.
$$

所以：

- 当 $a\ne 2$ 时，方程组只有零解；
- 当 $a=2$ 时，通解为
  $$
  x=k(-2,-1,1)^T.
  $$

（2）当 $a\ne 2$ 时，由上式知二次型正定，故其规范形为
$$
y_1^2+y_2^2+y_3^2.
$$

当 $a=2$ 时，
$$
f(x_1,x_2,x_3)=2x_1^2+2x_2^2+6x_3^2-2x_1x_2+6x_1x_3
$$
可配方为
$$
f=2\left(x_1-\frac{1}{2}x_2+\frac{3}{2}x_3\right)^2+\frac{3}{2}(x_2+x_3)^2.
$$

因此规范形为
$$
y_1^2+y_2^2.
$$

### 第 21 题

**标准答案：** （1）$a=2$。 （2）可取 $P=\begin{pmatrix}3&-2&4\\-1&1&-1\\0&1&0\end{pmatrix}$；更一般地，$P=\begin{pmatrix}3-6k_1&4-6k_2&4-6k_3\\-1+2k_1&-1+2k_2&-1+2k_3\\k_1&k_2&k_3\end{pmatrix}$，其中 $k_2\ne k_3$。

（1）对矩阵 $A,B$ 分别作初等行变换，可得
$$
A\sim
\begin{pmatrix}
1 & 0 & 3a \\
0 & 1 & -a \\
0 & 0 & 0
\end{pmatrix},\qquad
B\sim
\begin{pmatrix}
1 & 0 & 0 \\
0 & 1 & 1 \\
0 & 0 & 2-a
\end{pmatrix}.
$$

题设说二者可经初等行变换互化，因此秩相同，故 $2-a=0$，即
$$
a=2.
$$

（2）取 $a=2$ 后，对增广矩阵 $(A\mid B)$ 作行变换，得到
$$
(A\mid B)\sim
\begin{pmatrix}
1 & 0 & 6 & 3 & 4 & 4 \\
0 & 1 & -2 & -1 & -1 & -1 \\
0 & 0 & 0 & 0 & 0 & 0
\end{pmatrix}.
$$

记 $B=(\beta_1,\beta_2,\beta_3)$，可解得
$$
AX=B
$$
的一般解为
$$
X=
\begin{pmatrix}
3-6k_1 & 4-6k_2 & 4-6k_3 \\
-1+2k_1 & -1+2k_2 & -1+2k_3 \\
k_1 & k_2 & k_3
\end{pmatrix}.
$$

又
$$
|X|=k_3-k_2,
$$
所以当且仅当 $k_2\ne k_3$ 时，$X$ 可逆。于是满足 $AP=B$ 的可逆矩阵全体为
$$
P=
\begin{pmatrix}
3-6k_1 & 4-6k_2 & 4-6k_3 \\
-1+2k_1 & -1+2k_2 & -1+2k_3 \\
k_1 & k_2 & k_3
\end{pmatrix},
\qquad k_2\ne k_3.
$$

例如取 $(k_1,k_2,k_3)=(0,1,0)$，得到
$$
P=
\begin{pmatrix}
3 & -2 & 4 \\
-1 & 1 & -1 \\
0 & 1 & 0
\end{pmatrix}.
$$

### 第 22 题

**标准答案：** （1）$\operatorname{Cov}(X,Z)=\lambda$。 （2）对任意整数 $i$，$P(Z=0)=e^{-\lambda}$；当 $i>0$ 时，$P(Z=i)=\dfrac{1}{2}\dfrac{\lambda^i e^{-\lambda}}{i!}$；当 $i<0$ 时，$P(Z=i)=\dfrac{1}{2}\dfrac{\lambda^{-i} e^{-\lambda}}{(-i)!}$。

（1）由题设，
$$
E(X)=(-1)\cdot\frac{1}{2}+1\cdot\frac{1}{2}=0.
$$

又因 $Z=XY$，且 $X,Y$ 独立，有
$$
E(XZ)=E(X^2Y)=E(X^2)E(Y)=1\cdot\lambda=\lambda.
$$

因此
$$
\operatorname{Cov}(X,Z)=E(XZ)-E(X)E(Z)=\lambda.
$$

（2）随机变量 $Z$ 的所有可能取值是全体整数。

- 当 $i=0$ 时，$Z=0$ 等价于 $Y=0$，故
  $$
  P(Z=0)=P(Y=0)=e^{-\lambda}.
  $$

- 当 $i>0$ 时，只有 $X=1,\ Y=i$ 才能使 $Z=i$，故
  $$
  P(Z=i)=P(X=1)P(Y=i)=\frac{1}{2}\cdot\frac{\lambda^i e^{-\lambda}}{i!}.
  $$

- 当 $i<0$ 时，只有 $X=-1,\ Y=-i$ 才能使 $Z=i$，故
  $$
  P(Z=i)=P(X=-1)P(Y=-i)=\frac{1}{2}\cdot\frac{\lambda^{-i} e^{-\lambda}}{(-i)!}.
  $$

这就是 $Z$ 的分布律。

### 第 23 题

**标准答案：** （1）$\hat\sigma=\dfrac{1}{n}\sum_{i=1}^n \lvert X_i\rvert$。 （2）$E(\hat\sigma)=\sigma$，$D(\hat\sigma)=\dfrac{\sigma^2}{n}$。

（1）样本观测值为 $x_1,\dots,x_n$ 时，似然函数为
$$
L(\sigma)=\prod_{i=1}^n \frac{1}{2\sigma}e^{-|x_i|/\sigma}
=\frac{1}{2^n\sigma^n}e^{-\frac{1}{\sigma}\sum_{i=1}^n |x_i|}.
$$

于是
$$
\ln L(\sigma)=-n\ln 2-n\ln\sigma-\frac{1}{\sigma}\sum_{i=1}^n |x_i|.
$$

求导并令其为零：
$$
\frac{d\ln L(\sigma)}{d\sigma}
=-\frac{n}{\sigma}+\frac{1}{\sigma^2}\sum_{i=1}^n |x_i|=0,
$$
解得
$$
\hat\sigma=\frac{1}{n}\sum_{i=1}^n \lvert X_i\rvert.
$$

（2）先计算单个样本的矩：
$$
E\lvert X\rvert
=\int_{-\infty}^{+\infty}|x|\frac{1}{2\sigma}e^{-|x|/\sigma}\,dx
=\frac{1}{\sigma}\int_0^{+\infty}xe^{-x/\sigma}\,dx
=\sigma,
$$
故
$$
E(\hat\sigma)=\frac{1}{n}\sum_{i=1}^n E\lvert X_i\rvert=\sigma.
$$

又
$$
E\lvert X\rvert^2=EX^2
=\int_{-\infty}^{+\infty}x^2\frac{1}{2\sigma}e^{-|x|/\sigma}\,dx
=\frac{1}{\sigma}\int_0^{+\infty}x^2e^{-x/\sigma}\,dx
=2\sigma^2,
$$
所以
$$
D(|X|)=E\lvert X\rvert^2-(E\lvert X\rvert)^2=\sigma^2.
$$

由样本独立性，
$$
D(\hat\sigma)=\frac{1}{n^2}\sum_{i=1}^n D(\lvert X_i\rvert)
=\frac{\sigma^2}{n}.
$$
