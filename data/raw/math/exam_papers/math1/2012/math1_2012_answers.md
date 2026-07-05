# Math 1 2012 Answers

资料类型：考研数学一答案解析
年份：2012
科目：数学一
整理状态：已按题干与答案页图像核对并清洗整理

## 答案速查

| 题号 | 题型 | 答案 |
|---|---|---|
| 1 | 选择题 | C |
| 2 | 选择题 | A |
| 3 | 选择题 | B |
| 4 | 选择题 | D |
| 5 | 选择题 | C |
| 6 | 选择题 | B |
| 7 | 选择题 | A |
| 8 | 选择题 | D |
| 9 | 填空题 | $e^x$ |
| 10 | 填空题 | $\displaystyle \frac{\pi}{2}$ |
| 11 | 填空题 | $\mathbf i+\mathbf j+\mathbf k$ |
| 12 | 填空题 | $\displaystyle \frac{\sqrt{3}}{12}$ |
| 13 | 填空题 | $2$ |
| 14 | 填空题 | $\displaystyle \frac{3}{4}$ |
| 15 | 解答题 | 不等式成立，等号当且仅当 $x=0$ 时取到。 |
| 16 | 解答题 | 极大值 $f(1,0)=e^{-1/2}$；极小值 $f(-1,0)=-e^{-1/2}$。 |
| 17 | 解答题 | 收敛域为 $(-1,1)$；和函数为 $\displaystyle S(x)=\frac{1+x^2}{(1-x^2)^2}+\frac{1}{x}\ln\frac{1+x}{1-x}$，其中 $-1<x<1$ 且 $x\ne 0$；$S(0)=3$。 |
| 18 | 解答题 | $\displaystyle f(t)=-\sin t+\ln(\sec t+\tan t)$；所求面积为 $\displaystyle \frac{\pi}{4}$。 |
| 19 | 解答题 | $\displaystyle I=\frac{\pi}{2}-4$。 |
| 20 | 解答题 | $\displaystyle \det A=1-a^4$；当 $a=-1$ 时方程组有无穷多解，通解为 $\displaystyle x=k(1,1,1,1)^T+(0,-1,0,0)^T$，其中 $k\in\mathbb R$。 |
| 21 | 解答题 | $a=-1$；可取 $\displaystyle Q=\begin{pmatrix}-\frac{1}{\sqrt{3}}&-\frac{1}{\sqrt{2}}&\frac{1}{\sqrt{6}}\\-\frac{1}{\sqrt{3}}&\frac{1}{\sqrt{2}}&\frac{1}{\sqrt{6}}\\\frac{1}{\sqrt{3}}&0&\frac{2}{\sqrt{6}}\end{pmatrix}$，此时标准形为 $\displaystyle f=2y_2^2+6y_3^2$。 |
| 22 | 解答题 | $\displaystyle P\{X=2Y\}=\frac{1}{4}$；$\displaystyle \operatorname{Cov}(X-Y,Y)=-\frac{2}{3}$。 |
| 23 | 解答题 | $\displaystyle f(z;\sigma^2)=\frac{1}{\sqrt{6\pi}\,\sigma}e^{-z^2/(6\sigma^2)}$；$\displaystyle \hat\sigma^2=\frac{1}{3n}\sum_{i=1}^n Z_i^2$；且 $E\hat\sigma^2=\sigma^2$，故为无偏估计量。 |

## 详细解析

### 第 1 题

**答案：** C

曲线方程可化为
$$
y=\frac{x^2+x}{x^2-1}=\frac{x}{x-1}\quad (x\ne -1).
$$
原式在 $x=-1$ 处为可去间断点，因为
$$
\lim_{x\to -1}\frac{x(x+1)}{(x+1)(x-1)}=\frac{1}{2},
$$
所以 $x=-1$ 不是渐近线。又
$$
\lim_{x\to 1}\frac{x^2+x}{x^2-1}=\infty,
$$
故 $x=1$ 是垂直渐近线。

当 $x\to\infty$ 时，
$$
\lim_{x\to\infty}y=\lim_{x\to\infty}\frac{x^2+x}{x^2-1}=1,
$$
所以 $y=1$ 是水平渐近线。并且
$$
\lim_{x\to\infty}\frac{y}{x}=0,
$$
无斜渐近线。共有 $2$ 条渐近线，选 C。

### 第 2 题

**答案：** A

设
$$
f(x)=\prod_{k=1}^n(e^{kx}-k).
$$
在 $x=0$ 时，第一因子 $e^x-1=0$，而其余因子不为零。求导后，只有对第一因子求导的那一项在 $x=0$ 处可能非零，因此
$$
f'(0)=e^0\prod_{k=2}^n(1-k)=(-1)^{n-1}(n-1)!.
$$
故选 A。

### 第 3 题

**答案：** B

若
$$
\lim_{(x,y)\to(0,0)}\frac{f(x,y)}{x^2+y^2}=A,
$$
则 $f(x,y)=A(x^2+y^2)+o(x^2+y^2)$。又 $f$ 在 $(0,0)$ 连续，所以 $f(0,0)=0$。于是
$$
\frac{f(x,y)-f(0,0)}{\sqrt{x^2+y^2}}
=A\sqrt{x^2+y^2}+o\left(\sqrt{x^2+y^2}\right)\to 0,
$$
故 $f$ 在 $(0,0)$ 处可微，且微分为 $0$，B 正确。

A 可取 $f(x,y)=|x|+|y|$，此时相应极限存在，但函数在原点不可微。C、D 可取 $f(x,y)=x$，函数在原点可微，但题中两个商的极限均不存在。故选 B。

### 第 4 题

**答案：** D

由
$$
I_2=I_1+\int_\pi^{2\pi}e^{x^2}\sin x\,dx,
$$
且 $\pi<x<2\pi$ 时 $\sin x<0$，可得 $I_2<I_1$。

又
$$
I_3=I_2+\int_{2\pi}^{3\pi}e^{x^2}\sin x\,dx,
$$
且 $2\pi<x<3\pi$ 时 $\sin x>0$，所以 $I_2<I_3$。

比较 $I_3$ 与 $I_1$：
$$
I_3-I_1=\int_\pi^{3\pi}e^{x^2}\sin x\,dx.
$$
将后一段作代换 $x=t+\pi$，得
$$
I_3-I_1=\int_\pi^{2\pi}\left(e^{x^2}-e^{(x+\pi)^2}\right)\sin x\,dx.
$$
在 $(\pi,2\pi)$ 上，$e^{x^2}-e^{(x+\pi)^2}<0$ 且 $\sin x<0$，故 $I_3-I_1>0$。因此
$$
I_2<I_1<I_3,
$$
选 D。

### 第 5 题

**答案：** C

考察向量组 $\alpha_1,\alpha_3,\alpha_4$ 的行列式：
$$
\det(\alpha_1,\alpha_3,\alpha_4)=
\begin{vmatrix}
0&1&-1\\
0&-1&1\\
c_1&c_3&c_4
\end{vmatrix}
=c_1
\begin{vmatrix}
1&-1\\
-1&1
\end{vmatrix}=0.
$$
因此 $\alpha_1,\alpha_3,\alpha_4$ 对任意 $c_1,c_3,c_4$ 都线性相关。其余选项不恒为线性相关，故选 C。

### 第 6 题

**答案：** B

记
$$
D=P^{-1}AP=\operatorname{diag}(1,1,2).
$$
由 $Q=(\alpha_1+\alpha_2,\alpha_2,\alpha_3)$ 可知
$$
Q=P
\begin{pmatrix}
1&0&0\\
1&1&0\\
0&0&1
\end{pmatrix}=PS.
$$
于是
$$
Q^{-1}AQ=S^{-1}DS.
$$
由于 $D$ 的前两个对角元相同，$S$ 只在前两个特征向量张成的子空间内换基，因此
$$
S^{-1}DS=D=\operatorname{diag}(1,1,2).
$$
故选 B。

### 第 7 题

**答案：** A

$X$ 与 $Y$ 独立，且 $X\sim\operatorname{Exp}(1)$，$Y\sim\operatorname{Exp}(4)$。因此
$$
P\{X<Y\}=\int_0^{+\infty}P\{Y>x\}f_X(x)\,dx
=\int_0^{+\infty}e^{-4x}e^{-x}\,dx
=\frac{1}{5}.
$$
故选 A。

### 第 8 题

**答案：** D

设两段木棒长度为 $X,Y$，则
$$
X+Y=1,
$$
即 $Y=1-X$。两者满足斜率为负的严格线性关系，因此相关系数为
$$
\rho_{XY}=-1.
$$
故选 D。

### 第 9 题

**答案：** $e^x$

由
$$
f''(x)+f(x)=2e^x
$$
得 $f''(x)=2e^x-f(x)$。代入
$$
f''(x)+f'(x)-2f(x)=0,
$$
可得
$$
f'(x)-3f(x)=-2e^x.
$$
两边乘以积分因子 $e^{-3x}$：
$$
\left(e^{-3x}f(x)\right)'=-2e^{-2x}.
$$
积分得
$$
e^{-3x}f(x)=e^{-2x}+C,
$$
即
$$
f(x)=e^x+Ce^{3x}.
$$
代回 $f''(x)+f(x)=2e^x$，得 $C=0$，所以
$$
f(x)=e^x.
$$

### 第 10 题

**答案：** $\displaystyle \frac{\pi}{2}$

令 $t=x-1$，则 $x=t+1$，积分化为
$$
\int_0^2x\sqrt{2x-x^2}\,dx
=\int_{-1}^{1}(t+1)\sqrt{1-t^2}\,dt.
$$
其中
$$
\int_{-1}^{1}t\sqrt{1-t^2}\,dt=0
$$
为奇函数在对称区间上的积分，而
$$
\int_{-1}^{1}\sqrt{1-t^2}\,dt=\frac{\pi}{2}
$$
是单位圆上半圆面积。故原积分为
$$
\frac{\pi}{2}.
$$

### 第 11 题

**答案：** $\mathbf i+\mathbf j+\mathbf k$

令
$$
u(x,y,z)=xy+\frac{z}{y}.
$$
则
$$
\nabla u=\left(y,\ x-\frac{z}{y^2},\ \frac{1}{y}\right).
$$
代入 $(2,1,1)$，得
$$
\nabla u\big|_{(2,1,1)}=(1,1,1)=\mathbf i+\mathbf j+\mathbf k.
$$

### 第 12 题

**答案：** $\displaystyle \frac{\sqrt{3}}{12}$

由平面方程得 $z=1-x-y$，其在 $xy$ 平面上的投影区域为
$$
D=\{(x,y):x\ge 0,\ y\ge 0,\ x+y\le 1\}.
$$
又
$$
dS=\sqrt{1+z_x^2+z_y^2}\,dxdy=\sqrt{3}\,dxdy.
$$
因此
$$
\iint_\Sigma y^2\,dS
=\sqrt{3}\int_0^1\int_0^{1-x}y^2\,dy\,dx
=\sqrt{3}\int_0^1\frac{(1-x)^3}{3}\,dx
=\frac{\sqrt{3}}{12}.
$$

### 第 13 题

**答案：** $2$

因为 $\alpha$ 是三维单位列向量，矩阵 $\alpha\alpha^T$ 是到 $\alpha$ 张成直线上的正交投影矩阵，其特征值为 $1,0,0$。于是
$$
E-\alpha\alpha^T
$$
的特征值为 $0,1,1$，故其秩为 $2$。

### 第 14 题

**答案：** $\displaystyle \frac{3}{4}$

因为 $A$ 与 $C$ 互不相容，所以 $AB$ 与 $C$ 也互不相容，故
$$
P(AB\cap\overline C)=P(AB).
$$
于是
$$
P(AB\mid\overline C)=\frac{P(AB\cap\overline C)}{P(\overline C)}
=\frac{P(AB)}{1-P(C)}
=\frac{\frac{1}{2}}{1-\frac{1}{3}}
=\frac{3}{4}.
$$

### 第 15 题

**答案：** 不等式成立，等号当且仅当 $x=0$ 时取到。

令
$$
F(x)=x\ln\frac{1+x}{1-x}+\cos x-1-\frac{x^2}{2},\qquad -1<x<1.
$$
显然 $F(x)$ 为偶函数，所以只需证明 $0\le x<1$ 时 $F(x)\ge 0$。

有
$$
F'(x)=\ln\frac{1+x}{1-x}+\frac{2x}{1-x^2}-\sin x-x,
$$
且
$$
F''(x)=\frac{2}{1-x^2}+\frac{2(1+x^2)}{(1-x^2)^2}-\cos x-1.
$$
当 $0<x<1$ 时，$\frac{2}{1-x^2}>2$，$\frac{2(1+x^2)}{(1-x^2)^2}>2$，且 $\cos x<1$，所以 $F''(x)>0$。

又 $F'(0)=0$，故 $F'(x)>0$，从而 $F(x)$ 在 $[0,1)$ 上递增。由于 $F(0)=0$，故 $F(x)\ge 0$。由偶性可知对 $-1<x<1$ 均成立，即
$$
x\ln\frac{1+x}{1-x}+\cos x\ge 1+\frac{x^2}{2}.
$$

### 第 16 题

**答案：** 极大值 $f(1,0)=e^{-1/2}$；极小值 $f(-1,0)=-e^{-1/2}$。

函数
$$
f(x,y)=xe^{-(x^2+y^2)/2}.
$$
先求驻点：
$$
f_x=(1-x^2)e^{-(x^2+y^2)/2},\qquad
f_y=-xye^{-(x^2+y^2)/2}.
$$
由 $f_x=f_y=0$ 得驻点为 $(1,0)$ 与 $(-1,0)$。

二阶偏导为
$$
f_{xx}=(x^3-3x)e^{-(x^2+y^2)/2},
$$
$$
f_{xy}=(x^2-1)ye^{-(x^2+y^2)/2},
$$
$$
f_{yy}=x(y^2-1)e^{-(x^2+y^2)/2}.
$$
在 $(1,0)$ 处，
$$
A=-2e^{-1/2},\quad B=0,\quad C=-e^{-1/2},
$$
所以 $AC-B^2=2e^{-1}>0$ 且 $A<0$，故 $(1,0)$ 为极大值点，极大值为
$$
f(1,0)=e^{-1/2}.
$$
在 $(-1,0)$ 处，
$$
A=2e^{-1/2},\quad B=0,\quad C=e^{-1/2},
$$
所以 $AC-B^2=2e^{-1}>0$ 且 $A>0$，故 $(-1,0)$ 为极小值点，极小值为
$$
f(-1,0)=-e^{-1/2}.
$$

### 第 17 题

**答案：** 收敛域为 $(-1,1)$；和函数为 $\displaystyle S(x)=\frac{1+x^2}{(1-x^2)^2}+\frac{1}{x}\ln\frac{1+x}{1-x}$，其中 $-1<x<1$ 且 $x\ne 0$；$S(0)=3$。

记通项
$$
u_n(x)=\frac{4n^2+4n+3}{2n+1}x^{2n}.
$$
由比值判别法，
$$
\lim_{n\to\infty}\left|\frac{u_{n+1}(x)}{u_n(x)}\right|=x^2.
$$
故 $|x|<1$ 时收敛，$|x|>1$ 时发散。当 $x=\pm1$ 时，通项
$$
\frac{4n^2+4n+3}{2n+1}
$$
不趋于 $0$，级数发散。因此收敛域为 $(-1,1)$。

又
$$
\frac{4n^2+4n+3}{2n+1}=2n+1+\frac{2}{2n+1}.
$$
设
$$
S(x)=\sum_{n=0}^{\infty}\frac{4n^2+4n+3}{2n+1}x^{2n}=S_1(x)+S_2(x),
$$
其中
$$
S_1(x)=\sum_{n=0}^{\infty}(2n+1)x^{2n}
=\left(\sum_{n=0}^{\infty}x^{2n+1}\right)'
=\left(\frac{x}{1-x^2}\right)'
=\frac{1+x^2}{(1-x^2)^2}.
$$
并且
$$
S_2(x)=\sum_{n=0}^{\infty}\frac{2}{2n+1}x^{2n}.
$$
当 $x\ne0$ 时，
$$
xS_2(x)=2\sum_{n=0}^{\infty}\frac{x^{2n+1}}{2n+1}
=\ln\frac{1+x}{1-x},
$$
所以
$$
S_2(x)=\frac{1}{x}\ln\frac{1+x}{1-x}.
$$
综上，
$$
S(x)=\frac{1+x^2}{(1-x^2)^2}+\frac{1}{x}\ln\frac{1+x}{1-x},\qquad -1<x<1,\ x\ne0.
$$
当 $x=0$ 时，原级数仅首项保留，$S(0)=3$。

### 第 18 题

**答案：** $\displaystyle f(t)=-\sin t+\ln(\sec t+\tan t)$；所求面积为 $\displaystyle \frac{\pi}{4}$。

曲线在参数 $t$ 对应的切点为 $A(f(t),\cos t)$。因
$$
\frac{dy}{dx}=\frac{-\sin t}{f'(t)},
$$
切线方程为
$$
y=\cos t-\frac{\sin t}{f'(t)}\,[x-f(t)].
$$
令 $y=0$，得切线与 $x$ 轴交点
$$
B\left(f(t)+\frac{\cos t\,f'(t)}{\sin t},0\right).
$$
于是
$$
AB=\sqrt{\left(\frac{\cos t\,f'(t)}{\sin t}\right)^2+\cos^2t}=1.
$$
化简并结合 $f'(t)>0$，得
$$
f'(t)=\frac{\sin^2t}{\cos t}=\sec t-\cos t.
$$
由 $f(0)=0$，
$$
f(t)=\int_0^t(\sec u-\cos u)\,du
=\ln(\sec t+\tan t)-\sin t.
$$

因 $t\to\frac{\pi}{2}-0$ 时 $f(t)\to+\infty$，曲线可写成 $y=g(x)$，所求面积为
$$
S=\int_0^{+\infty}g(x)\,dx
=\int_0^{\pi/2}\cos t\,df(t)
=\int_0^{\pi/2}\cos t\,f'(t)\,dt.
$$
代入 $f'(t)=\frac{\sin^2t}{\cos t}$，得
$$
S=\int_0^{\pi/2}\sin^2t\,dt=\frac{\pi}{4}.
$$

### 第 19 题

**答案：** $\displaystyle I=\frac{\pi}{2}-4$。

记
$$
P(x,y)=3x^2y,\qquad Q(x,y)=x^3+x-2y.
$$
则
$$
\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}=3x^2+1-3x^2=1.
$$
曲线 $L$ 不封闭，添加辅助线 $L_1$：沿 $y$ 轴从 $B(0,2)$ 到 $O(0,0)$。则 $L+L_1$ 围成的区域 $D$ 为第一象限内大圆 $x^2+y^2=4$ 的四分之一圆去掉小圆 $x^2+y^2=2x$ 的上半圆，所以
$$
\iint_D1\,d\sigma=\frac{1}{4}\pi\cdot2^2-\frac{1}{2}\pi\cdot1^2=\frac{\pi}{2}.
$$
由格林公式，
$$
\int_{L+L_1}P\,dx+Q\,dy=\frac{\pi}{2}.
$$
在 $L_1$ 上 $x=0$，$dx=0$，且方向为 $y:2\to0$，因此
$$
\int_{L_1}P\,dx+Q\,dy=\int_2^0(-2y)\,dy=4.
$$
所以
$$
I=\int_LP\,dx+Q\,dy=\frac{\pi}{2}-4.
$$

### 第 20 题

**答案：** $\displaystyle \det A=1-a^4$；当 $a=-1$ 时方程组有无穷多解，通解为 $\displaystyle x=k(1,1,1,1)^T+(0,-1,0,0)^T$，其中 $k\in\mathbb R$。

按第一列展开行列式，得
$$
\det A=1\cdot
\begin{vmatrix}
1&a&0\\
0&1&a\\
0&0&1
\end{vmatrix}
-a
\begin{vmatrix}
a&0&0\\
1&a&0\\
0&1&a
\end{vmatrix}
=1-a^4.
$$
若方程组有无穷多解，必须 $\det A=0$，故 $a=1$ 或 $a=-1$。

当 $a=1$ 时，增广矩阵可化为
$$
\begin{pmatrix}
1&1&0&0&1\\
0&1&1&0&-1\\
0&0&1&1&0\\
0&0&0&0&-2
\end{pmatrix},
$$
出现矛盾方程，故无解。

当 $a=-1$ 时，增广矩阵可化为
$$
\begin{pmatrix}
1&0&0&-1&0\\
0&1&0&-1&-1\\
0&0&1&-1&0\\
0&0&0&0&0
\end{pmatrix}.
$$
令 $x_4=k$，则
$$
x_1=k,\quad x_2=k-1,\quad x_3=k,\quad x_4=k.
$$
故通解为
$$
x=k(1,1,1,1)^T+(0,-1,0,0)^T,\qquad k\in\mathbb R.
$$

### 第 21 题

**答案：** $a=-1$；可取 $\displaystyle Q=\begin{pmatrix}-\frac{1}{\sqrt{3}}&-\frac{1}{\sqrt{2}}&\frac{1}{\sqrt{6}}\\-\frac{1}{\sqrt{3}}&\frac{1}{\sqrt{2}}&\frac{1}{\sqrt{6}}\\\frac{1}{\sqrt{3}}&0&\frac{2}{\sqrt{6}}\end{pmatrix}$，此时标准形为 $\displaystyle f=2y_2^2+6y_3^2$。

先计算
$$
A^TA=
\begin{pmatrix}
2&0&1-a\\
0&1+a^2&1-a\\
1-a&1-a&3+a^2
\end{pmatrix}.
$$
其中二阶子式
$$
\begin{vmatrix}
2&0\\
0&1+a^2
\end{vmatrix}=2(1+a^2)\ne0.
$$
若二次型秩为 $2$，则必须
$$
\det(A^TA)=0.
$$
直接计算得
$$
\det(A^TA)=(a+1)^2(a^2+3),
$$
故实数解为
$$
a=-1.
$$

当 $a=-1$ 时，
$$
A^TA=\begin{pmatrix}
2&0&2\\
0&2&2\\
2&2&4
\end{pmatrix}.
$$
其特征多项式为
$$
\det(\lambda E-A^TA)=\lambda(\lambda-2)(\lambda-6),
$$
特征值为 $0,2,6$。对应单位特征向量可取
$$
\gamma_1=\frac{1}{\sqrt{3}}(-1,-1,1)^T,
$$
$$
\gamma_2=\frac{1}{\sqrt{2}}(-1,1,0)^T,
$$
$$
\gamma_3=\frac{1}{\sqrt{6}}(1,1,2)^T.
$$
令 $Q=(\gamma_1,\gamma_2,\gamma_3)$，即
$$
Q=\begin{pmatrix}
-\frac{1}{\sqrt{3}}&-\frac{1}{\sqrt{2}}&\frac{1}{\sqrt{6}}\\
-\frac{1}{\sqrt{3}}&\frac{1}{\sqrt{2}}&\frac{1}{\sqrt{6}}\\
\frac{1}{\sqrt{3}}&0&\frac{2}{\sqrt{6}}
\end{pmatrix},
$$
则正交变换 $x=Qy$ 下
$$
f=x^T(A^TA)x=y^TQ^T(A^TA)Qy=2y_2^2+6y_3^2.
$$

### 第 22 题

**答案：** $\displaystyle P\{X=2Y\}=\frac{1}{4}$；$\displaystyle \operatorname{Cov}(X-Y,Y)=-\frac{2}{3}$。

由分布表，满足 $X=2Y$ 的可能点为 $(0,0)$ 与 $(2,1)$，其中
$$
P\{X=2Y\}=P\{X=0,Y=0\}+P\{X=2,Y=1\}=\frac{1}{4}+0=\frac{1}{4}.
$$

先求边缘分布与必要矩：
$$
P_X(0)=\frac{1}{2},\quad P_X(1)=\frac{1}{3},\quad P_X(2)=\frac{1}{6},
$$
$$
P_Y(0)=P_Y(1)=P_Y(2)=\frac{1}{3}.
$$
因此
$$
EX=0\cdot\frac{1}{2}+1\cdot\frac{1}{3}+2\cdot\frac{1}{6}=\frac{2}{3},
$$
$$
EY=0\cdot\frac{1}{3}+1\cdot\frac{1}{3}+2\cdot\frac{1}{3}=1,
$$
$$
EY^2=0^2\cdot\frac{1}{3}+1^2\cdot\frac{1}{3}+2^2\cdot\frac{1}{3}=\frac{5}{3}.
$$
又
$$
EXY=1\cdot\frac{1}{3}+4\cdot\frac{1}{12}=\frac{2}{3}.
$$
于是
$$
DY=EY^2-(EY)^2=\frac{5}{3}-1=\frac{2}{3},
$$
并且
$$
\operatorname{Cov}(X,Y)=EXY-EX\,EY=\frac{2}{3}-\frac{2}{3}\cdot1=0.
$$
故
$$
\operatorname{Cov}(X-Y,Y)=\operatorname{Cov}(X,Y)-D(Y)=0-\frac{2}{3}=-\frac{2}{3}.
$$

### 第 23 题

**答案：** $\displaystyle f(z;\sigma^2)=\frac{1}{\sqrt{6\pi}\,\sigma}e^{-z^2/(6\sigma^2)}$；$\displaystyle \hat\sigma^2=\frac{1}{3n}\sum_{i=1}^n Z_i^2$；且 $E\hat\sigma^2=\sigma^2$，故为无偏估计量。

因为 $X$ 与 $Y$ 相互独立，且
$$
X\sim N(\mu,\sigma^2),\qquad Y\sim N(\mu,2\sigma^2),
$$
所以
$$
Z=X-Y\sim N(0,3\sigma^2).
$$
故 $Z$ 的概率密度为
$$
f(z;\sigma^2)=\frac{1}{\sqrt{2\pi}\sqrt{3\sigma^2}}\exp\left(-\frac{z^2}{2\cdot3\sigma^2}\right)
=\frac{1}{\sqrt{6\pi}\,\sigma}e^{-z^2/(6\sigma^2)},\quad -\infty<z<+\infty.
$$

令 $\theta=\sigma^2$。样本 $Z_1,Z_2,\ldots,Z_n$ 的似然函数为
$$
L(\theta)=\prod_{i=1}^n\frac{1}{\sqrt{6\pi\theta}}\exp\left(-\frac{Z_i^2}{6\theta}\right)
=(6\pi\theta)^{-n/2}\exp\left(-\frac{1}{6\theta}\sum_{i=1}^nZ_i^2\right).
$$
取对数：
$$
\ln L(\theta)=-\frac{n}{2}\ln(6\pi)-\frac{n}{2}\ln\theta-\frac{1}{6\theta}\sum_{i=1}^nZ_i^2.
$$
令导数为零，
$$
\frac{d}{d\theta}\ln L(\theta)=-\frac{n}{2\theta}+\frac{1}{6\theta^2}\sum_{i=1}^nZ_i^2=0,
$$
得
$$
\hat\sigma^2=\hat\theta=\frac{1}{3n}\sum_{i=1}^nZ_i^2.
$$

又 $EZ=0$，$DZ=3\sigma^2$，故
$$
E(Z_i^2)=DZ+(EZ)^2=3\sigma^2.
$$
于是
$$
E\hat\sigma^2=E\left(\frac{1}{3n}\sum_{i=1}^nZ_i^2\right)
=\frac{1}{3n}\sum_{i=1}^nE(Z_i^2)
=\frac{1}{3n}\cdot n\cdot3\sigma^2
=\sigma^2.
$$
因此 $\hat\sigma^2$ 是 $\sigma^2$ 的无偏估计量。
