# Math 1 2008 Answers

资料类型：考研数学一答案解析
年份：2008
科目：数学一
来源：D:\百度网盘\高数资料\【02】1987-2022年数学一真题详解答案（PDF）\2008考研数一真题解析.pdf
校对状态：已按答案解析 PDF 页面图像与题干核对，并清洗整理

## 答案速查

| 题号 | 题型 | 答案 |
|---|---|---|
| 1 | 选择题 | B |
| 2 | 选择题 | A |
| 3 | 选择题 | D |
| 4 | 选择题 | B |
| 5 | 选择题 | C |
| 6 | 选择题 | B |
| 7 | 选择题 | A |
| 8 | 选择题 | D |
| 9 | 填空题 | $\displaystyle \frac{1}{x}$ |
| 10 | 填空题 | $y=x+1$ |
| 11 | 填空题 | $(1,5]$ |
| 12 | 填空题 | $4\pi$ |
| 13 | 填空题 | $1$ |
| 14 | 填空题 | $\displaystyle \frac{1}{2e}$ |
| 15 | 解答题 | $\displaystyle \frac{1}{6}$ |
| 16 | 解答题 | $\displaystyle -\frac{\pi^2}{2}$ |
| 17 | 解答题 | 最远点为 $(-5,-5,5)$，最近点为 $(1,1,1)$。 |
| 18 | 解答题 | 证明见解析。 |
| 19 | 解答题 | $\displaystyle 1-\frac{\pi^2}{3}+4\sum_{n=1}^{\infty}\frac{(-1)^{n+1}}{n^2}\cos nx$；$\displaystyle \sum_{n=1}^{\infty}\frac{(-1)^{n-1}}{n^2}=\frac{\pi^2}{12}$。 |
| 20 | 解答题 | 证明见解析。 |
| 21 | 解答题 | (I) $\det A=(n+1)a^n$；(II) 当 $a\ne0$ 时有唯一解，$\displaystyle x_1=\frac{n}{(n+1)a}$；(III) 当 $a=0$ 时有无穷多解，$\boldsymbol{x}=(0,1,0,\ldots,0)^T+k(1,0,0,\ldots,0)^T$。 |
| 22 | 解答题 | (I) $\displaystyle \frac{1}{2}$；(II) $\displaystyle f_Z(z)=\begin{cases}\frac{1}{3},&-1\le z<2,\\0,&\text{其他}.\end{cases}$ |
| 23 | 解答题 | $T$ 是 $\mu^2$ 的无偏估计量；当 $\mu=0,\ \sigma=1$ 时，$\displaystyle D(T)=\frac{2}{n(n-1)}$。 |

## 详细解析

### 第 1 题

**答案：** B

由变上限积分求导和链式法则，
$$
f'(x)=\ln(2+x^2)\cdot 2x=2x\ln(2+x^2).
$$
因为 $2+x^2\ge2$，所以 $\ln(2+x^2)>0$ 恒成立，故 $f'(x)=0$ 只可能由 $x=0$ 给出。

因此 $f'(x)$ 只有一个零点，选 B。

### 第 2 题

**答案：** A

对
$$
f(x,y)=\arctan\frac{x}{y}
$$
求偏导：
$$
f_x=\frac{1/y}{1+x^2/y^2}=\frac{y}{x^2+y^2},\qquad
f_y=\frac{-x/y^2}{1+x^2/y^2}=-\frac{x}{x^2+y^2}.
$$
代入 $(0,1)$ 得
$$
f_x(0,1)=1,\qquad f_y(0,1)=0.
$$
所以
$$
\operatorname{grad}f(0,1)=\boldsymbol{i}.
$$
选 A。

### 第 3 题

**答案：** D

通解
$$
y=C_1e^x+C_2\cos 2x+C_3\sin 2x
$$
对应的特征根为
$$
\lambda_1=1,\qquad \lambda_{2,3}=\pm 2i.
$$
故特征方程为
$$
(\lambda-1)(\lambda+2i)(\lambda-2i)
=(\lambda-1)(\lambda^2+4)
=\lambda^3-\lambda^2+4\lambda-4=0.
$$
对应微分方程为
$$
y'''-y''+4y'-4y=0.
$$
选 D。

### 第 4 题

**答案：** B

若 $\{x_n\}$ 单调，且 $f(x)$ 在全实轴上单调，则 $\{f(x_n)\}$ 也是单调数列。又因为 $f$ 有界，所以 $\{f(x_n)\}$ 有界。

单调有界数列必收敛，因此 B 正确。

### 第 5 题

**答案：** C

由 $A^3=O$，有
$$
(E-A)(E+A+A^2)=E-A^3=E,
$$
所以 $E-A$ 可逆；同理
$$
(E+A)(E-A+A^2)=E+A^3=E,
$$
所以 $E+A$ 也可逆。

故选 C。

### 第 6 题

**答案：** B

图中标准形是沿 $x'$ 轴分成两支的旋转双叶双曲面，其标准方程可写成
$$
\frac{x'^2}{a^2}-\frac{y'^2+z'^2}{c^2}=1.
$$
标准形中只有一个正平方项，因此实对称矩阵 $A$ 的正特征值个数为 $1$。

选 B。

### 第 7 题

**答案：** A

设 $Z$ 的分布函数为 $F_Z(x)$，则
$$
F_Z(x)=P(Z\le x)=P(\max\{X,Y\}\le x)=P(X\le x,\ Y\le x).
$$
由于 $X,Y$ 独立同分布，
$$
F_Z(x)=P(X\le x)P(Y\le x)=F(x)^2.
$$
选 A。

### 第 8 题

**答案：** D

相关系数 $\rho_{XY}=1$ 时，$X,Y$ 几乎处处满足正线性关系。设
$$
Y=aX+b,\qquad a>0.
$$
由 $X\sim N(0,1)$，$Y\sim N(1,4)$，得
$$
a=\frac{\sigma_Y}{\sigma_X}=2,\qquad
b=EY-aEX=1.
$$
所以
$$
P\{Y=2X+1\}=1.
$$
选 D。

### 第 9 题

**答案：** $\displaystyle \frac{1}{x}$

原方程
$$
xy'+y=0
$$
等价于
$$
(xy)'=xy'+y=0.
$$
所以 $xy=C$。由 $y(1)=1$ 得 $C=1$，故
$$
y=\frac{1}{x}.
$$

### 第 10 题

**答案：** $y=x+1$

设
$$
F(x,y)=\sin(xy)+\ln(y-x)-x.
$$
曲线由 $F(x,y)=0$ 给出，故切线斜率
$$
y'=-\frac{F_x}{F_y}.
$$
其中
$$
F_x=y\cos(xy)-\frac{1}{y-x}-1,\qquad
F_y=x\cos(xy)+\frac{1}{y-x}.
$$
代入 $(0,1)$ 得
$$
F_x(0,1)=-1,\qquad F_y(0,1)=1,
$$
所以 $y'(0)=1$。切线方程为
$$
y-1=x,
$$
即
$$
y=x+1.
$$

### 第 11 题

**答案：** $(1,5]$

设 $t=x+2$。已知
$$
\sum_{n=0}^{\infty}a_n(x+2)^n
$$
在 $x=0$ 即 $t=2$ 处收敛，在 $x=-4$ 即 $t=-2$ 处发散，因此其收敛半径为 $2$，且右端点收敛、左端点发散。

所以
$$
\sum_{n=0}^{\infty}a_n t^n
$$
的收敛域为 $(-2,2]$。对
$$
\sum_{n=0}^{\infty}a_n(x-3)^n
$$
令 $t=x-3$，得
$$
-2<x-3\le2,
$$
故收敛域为
$$
(1,5].
$$

### 第 12 题

**答案：** $4\pi$

记
$$
P=xy,\qquad Q=x,\qquad R=x^2.
$$
令 $\Omega$ 为上半球体 $x^2+y^2+z^2\le4,\ z\ge0$，用底面圆盘 $D$ 与 $\Sigma$ 围成闭曲面。由高斯公式，
$$
\iint_{\partial\Omega}P\,dy\,dz+Q\,dz\,dx+R\,dx\,dy
=\iiint_\Omega\left(\frac{\partial P}{\partial x}
+\frac{\partial Q}{\partial y}
+\frac{\partial R}{\partial z}\right)dV
=\iiint_\Omega y\,dV=0.
$$
底面外法向为负 $z$ 方向，因此底面对闭曲面的贡献为 $-\iint_D x^2\,dA$。于是原积分
$$
I=\iint_\Sigma xy\,dy\,dz+x\,dz\,dx+x^2\,dx\,dy
=\iint_D x^2\,dA.
$$
在半径为 $2$ 的圆盘上，
$$
\iint_D x^2\,dA
=\int_0^{2\pi}\int_0^2 r^2\cos^2\theta\cdot r\,dr\,d\theta
=\left(\int_0^{2\pi}\cos^2\theta\,d\theta\right)
\left(\int_0^2 r^3\,dr\right)
=\pi\cdot4=4\pi.
$$

### 第 13 题

**答案：** $1$

由题设
$$
A[\boldsymbol{\alpha}_1,\boldsymbol{\alpha}_2]
=[A\boldsymbol{\alpha}_1,A\boldsymbol{\alpha}_2]
=[0,2\boldsymbol{\alpha}_1+\boldsymbol{\alpha}_2]
=[\boldsymbol{\alpha}_1,\boldsymbol{\alpha}_2]
\begin{pmatrix}
0&2\\
0&1
\end{pmatrix}.
$$
记 $P=[\boldsymbol{\alpha}_1,\boldsymbol{\alpha}_2]$。由于 $\boldsymbol{\alpha}_1,\boldsymbol{\alpha}_2$ 线性无关，$P$ 可逆，因此 $A$ 与
$$
B=\begin{pmatrix}0&2\\0&1\end{pmatrix}
$$
相似。于是 $A$ 与 $B$ 有相同特征值。

因为
$$
\det(\lambda E-B)=
\begin{vmatrix}
\lambda&-2\\
0&\lambda-1
\end{vmatrix}
=\lambda(\lambda-1),
$$
所以非零特征值为 $1$。

### 第 14 题

**答案：** $\displaystyle \frac{1}{2e}$

若 $X\sim P(1)$，则
$$
EX=1,\qquad DX=1.
$$
由
$$
DX=E(X^2)-(EX)^2
$$
得
$$
E(X^2)=DX+(EX)^2=2.
$$
因此
$$
P\{X=E(X^2)\}=P\{X=2\}
=e^{-1}\frac{1^2}{2!}
=\frac{1}{2e}.
$$

### 第 15 题

**答案：** $\displaystyle \frac{1}{6}$

当 $x\to0$ 时，
$$
\sin(\sin x)
=\sin x-\frac{(\sin x)^3}{6}+O(x^5).
$$
所以
$$
\sin x-\sin(\sin x)
=\frac{(\sin x)^3}{6}+O(x^5)
=\frac{x^3}{6}+O(x^5).
$$
又 $\sin x=x+O(x^3)$，故
$$
[\sin x-\sin(\sin x)]\sin x
=\left(\frac{x^3}{6}+O(x^5)\right)(x+O(x^3))
=\frac{x^4}{6}+O(x^6).
$$
因此
$$
\lim_{x\to0}\frac{[\sin x-\sin(\sin x)]\sin x}{x^4}
=\frac{1}{6}.
$$

### 第 16 题

**答案：** $\displaystyle -\frac{\pi^2}{2}$

沿曲线 $L$ 取参数
$$
y=\sin x,\qquad 0\le x\le\pi,
$$
则
$$
dy=\cos x\,dx.
$$
原积分为
$$
\int_0^\pi\left[\sin2x+2(x^2-1)\sin x\cos x\right]dx.
$$
由于 $2\sin x\cos x=\sin2x$，上式化为
$$
\int_0^\pi x^2\sin2x\,dx.
$$
分部积分得
$$
\int_0^\pi x^2\sin2x\,dx
=-\left.\frac{x^2}{2}\cos2x\right|_0^\pi
+\int_0^\pi x\cos2x\,dx.
$$
而
$$
\int_0^\pi x\cos2x\,dx=0,
$$
故
$$
\int_L \sin2x\,dx+2(x^2-1)y\,dy
=-\frac{\pi^2}{2}.
$$

### 第 17 题

**答案：** 最远点为 $(-5,-5,5)$，最近点为 $(1,1,1)$。

点 $(x,y,z)$ 到 $xOy$ 面的距离为 $|z|$。在曲线 $C$ 上求最远点和最近点，等价于在约束
$$
x^2+y^2-2z^2=0,\qquad x+y+3z=5
$$
下求 $H=z^2$ 的最大值和最小值。

构造拉格朗日函数
$$
L=z^2+\lambda(x^2+y^2-2z^2)+\mu(x+y+3z-5).
$$
由
$$
\begin{cases}
2\lambda x+\mu=0,\\
2\lambda y+\mu=0,\\
2z-4\lambda z+3\mu=0,\\
x^2+y^2-2z^2=0,\\
x+y+3z=5
\end{cases}
$$
得 $x=y$。于是
$$
\begin{cases}
2x^2-2z^2=0,\\
2x+3z=5.
\end{cases}
$$
解得两组点：
$$
(-5,-5,5),\qquad (1,1,1).
$$
对应距离分别为 $5$ 与 $1$，故最远点为 $(-5,-5,5)$，最近点为 $(1,1,1)$。

### 第 18 题

**答案：** 证明见解析。

(I) 对任意 $x$，考察差商。若 $h\ne0$，则
$$
\frac{F(x+h)-F(x)}{h}
=\frac{1}{h}\int_x^{x+h}f(t)\,dt.
$$
由积分中值定理，存在 $\xi_h$ 介于 $x$ 与 $x+h$ 之间，使得
$$
\frac{1}{h}\int_x^{x+h}f(t)\,dt=f(\xi_h).
$$
当 $h\to0$ 时，$\xi_h\to x$。由于 $f$ 连续，
$$
\lim_{h\to0}f(\xi_h)=f(x).
$$
因此 $F$ 在 $x$ 处可导，且
$$
F'(x)=f(x).
$$

(II) 只需证明 $G(x+2)=G(x)$。由定义，
$$
G(x+2)-G(x)
=2\int_x^{x+2}f(t)\,dt-2\int_0^2f(t)\,dt.
$$
因为 $f$ 以 $2$ 为周期，任意长度为 $2$ 的区间上的积分相同，即
$$
\int_x^{x+2}f(t)\,dt=\int_0^2f(t)\,dt.
$$
故
$$
G(x+2)-G(x)=0.
$$
所以 $G(x)$ 也是以 $2$ 为周期的周期函数。

### 第 19 题

**答案：** $\displaystyle 1-\frac{\pi^2}{3}+4\sum_{n=1}^{\infty}\frac{(-1)^{n+1}}{n^2}\cos nx$；$\displaystyle \sum_{n=1}^{\infty}\frac{(-1)^{n-1}}{n^2}=\frac{\pi^2}{12}$。

余弦级数系数为
$$
a_0=\frac{2}{\pi}\int_0^\pi(1-x^2)\,dx
=2-\frac{2\pi^2}{3},
$$
且当 $n\ge1$ 时，
$$
a_n=\frac{2}{\pi}\int_0^\pi(1-x^2)\cos nx\,dx.
$$
分部积分可得
$$
\int_0^\pi x^2\cos nx\,dx=\frac{2\pi(-1)^n}{n^2},
$$
因此
$$
a_n=-\frac{2}{\pi}\cdot \frac{2\pi(-1)^n}{n^2}
=\frac{4(-1)^{n+1}}{n^2}.
$$
所以
$$
f(x)=1-\frac{\pi^2}{3}
+4\sum_{n=1}^{\infty}\frac{(-1)^{n+1}}{n^2}\cos nx,
\qquad 0\le x\le\pi.
$$
令 $x=0$，有 $f(0)=1$，于是
$$
1=1-\frac{\pi^2}{3}
+4\sum_{n=1}^{\infty}\frac{(-1)^{n+1}}{n^2}.
$$
故
$$
\sum_{n=1}^{\infty}\frac{(-1)^{n-1}}{n^2}
=\frac{\pi^2}{12}.
$$

### 第 20 题

**答案：** 证明见解析。

(I) 由矩阵秩的不等式，
$$
r(A)=r(\boldsymbol{\alpha}\boldsymbol{\alpha}^T+\boldsymbol{\beta}\boldsymbol{\beta}^T)
\le r(\boldsymbol{\alpha}\boldsymbol{\alpha}^T)
+r(\boldsymbol{\beta}\boldsymbol{\beta}^T).
$$
而 $\boldsymbol{\alpha}\boldsymbol{\alpha}^T$ 的列向量均为 $\boldsymbol{\alpha}$ 的倍数，故其秩不超过 $1$；同理
$$
r(\boldsymbol{\beta}\boldsymbol{\beta}^T)\le1.
$$
因此
$$
r(A)\le2.
$$

(II) 若 $\boldsymbol{\alpha},\boldsymbol{\beta}$ 线性相关，不妨设
$$
\boldsymbol{\alpha}=k\boldsymbol{\beta}.
$$
则
$$
A=k^2\boldsymbol{\beta}\boldsymbol{\beta}^T+\boldsymbol{\beta}\boldsymbol{\beta}^T
=(1+k^2)\boldsymbol{\beta}\boldsymbol{\beta}^T.
$$
所以
$$
r(A)\le r(\boldsymbol{\beta}\boldsymbol{\beta}^T)\le1<2.
$$
结论成立。

### 第 21 题

**答案：** (I) $\det A=(n+1)a^n$；(II) 当 $a\ne0$ 时有唯一解，$\displaystyle x_1=\frac{n}{(n+1)a}$；(III) 当 $a=0$ 时有无穷多解，$\boldsymbol{x}=(0,1,0,\ldots,0)^T+k(1,0,0,\ldots,0)^T$。

(I) 记 $D_n=\det A$。显然
$$
D_1=2a,\qquad
D_2=
\begin{vmatrix}
2a&1\\
a^2&2a
\end{vmatrix}
=3a^2.
$$
对 $n\ge3$，按第一行展开可得递推式
$$
D_n=2aD_{n-1}-a^2D_{n-2}.
$$
若 $D_{n-1}=n a^{n-1}$、$D_{n-2}=(n-1)a^{n-2}$，则
$$
D_n=2a\cdot n a^{n-1}-a^2\cdot (n-1)a^{n-2}
=(n+1)a^n.
$$
故由归纳法得
$$
\det A=D_n=(n+1)a^n.
$$

(II) 方程组有唯一解当且仅当 $\det A\ne0$，即
$$
a\ne0.
$$
此时由克拉默法则，将 $D_n$ 第一列替换为 $\boldsymbol{b}$ 得
$$
D_n^{(1)}=D_{n-1}=n a^{n-1}.
$$
所以
$$
x_1=\frac{D_n^{(1)}}{D_n}
=\frac{n a^{n-1}}{(n+1)a^n}
=\frac{n}{(n+1)a}.
$$

(III) 当 $a=0$ 时，方程组为
$$
\begin{cases}
x_2=1,\\
x_3=0,\\
\cdots\\
x_n=0,\\
0=0.
\end{cases}
$$
此时 $x_1$ 为自由变量，方程组有无穷多解，通解为
$$
\boldsymbol{x}=(0,1,0,\ldots,0)^T+k(1,0,0,\ldots,0)^T,
$$
其中 $k$ 为任意常数。

### 第 22 题

**答案：** (I) $\displaystyle \frac{1}{2}$；(II) $\displaystyle f_Z(z)=\begin{cases}\frac{1}{3},&-1\le z<2,\\0,&\text{其他}.\end{cases}$

(I) 当 $X=0$ 时，$Z=X+Y=Y$，因此
$$
P\left\{Z\le\frac{1}{2}\mid X=0\right\}
=P\left\{Y\le\frac{1}{2}\right\}
=\int_0^{1/2}1\,dy
=\frac{1}{2}.
$$

(II) 设 $F_Y$ 为 $Y$ 的分布函数。因为 $X$ 只取 $-1,0,1$，且与 $Y$ 独立，
$$
F_Z(z)=P(X+Y\le z)
=\frac{1}{3}\left[F_Y(z+1)+F_Y(z)+F_Y(z-1)\right].
$$
两边求导得
$$
f_Z(z)=\frac{1}{3}\left[f_Y(z+1)+f_Y(z)+f_Y(z-1)\right].
$$
由于
$$
f_Y(y)=
\begin{cases}
1,&0\le y<1,\\
0,&\text{其他},
\end{cases}
$$
可知三个平移后的区间分别为
$$
-1\le z<0,\qquad 0\le z<1,\qquad 1\le z<2.
$$
它们首尾相接，故
$$
f_Z(z)=
\begin{cases}
\dfrac{1}{3},&-1\le z<2,\\
0,&\text{其他}.
\end{cases}
$$

### 第 23 题

**答案：** $T$ 是 $\mu^2$ 的无偏估计量；当 $\mu=0,\ \sigma=1$ 时，$\displaystyle D(T)=\frac{2}{n(n-1)}$。

(I) 因为
$$
T=\overline X^{\,2}-\frac{1}{n}S^2,
$$
且
$$
E(\overline X^{\,2})=D(\overline X)+(E\overline X)^2
=\frac{\sigma^2}{n}+\mu^2,\qquad
E(S^2)=\sigma^2,
$$
所以
$$
ET=\left(\frac{\sigma^2}{n}+\mu^2\right)-\frac{1}{n}\sigma^2
=\mu^2.
$$
故 $T$ 是 $\mu^2$ 的无偏估计量。

(II) 当 $\mu=0,\ \sigma=1$ 时，$\overline X$ 与 $S^2$ 独立，且
$$
\sqrt{n}\,\overline X\sim N(0,1),\qquad (n-1)S^2\sim\chi^2(n-1).
$$
于是
$$
D(\overline X^{\,2})
=D\left(\frac{(\sqrt{n}\,\overline X)^2}{n}\right)
=\frac{1}{n^2}D(\chi_1^2)
=\frac{2}{n^2},
$$
并且
$$
D(S^2)
=D\left(\frac{\chi^2_{n-1}}{n-1}\right)
=\frac{1}{(n-1)^2}\cdot2(n-1)
=\frac{2}{n-1}.
$$
由独立性，
$$
D(T)=D(\overline X^{\,2})+\frac{1}{n^2}D(S^2)
=\frac{2}{n^2}+\frac{2}{n^2(n-1)}
=\frac{2}{n(n-1)}.
$$
