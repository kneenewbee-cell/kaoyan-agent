# Math 2 2012 Answers

资料类型：考研数学二答案解析
年份：2012
科目：数学二
整理状态：答案与解析按答案册清洗，并与题面同步。

## 答案速查

| 题号 | 题型 | 答案 |
|---|---|---|
| 1 | 选择题 | C |
| 2 | 选择题 | C |
| 3 | 选择题 | B |
| 4 | 选择题 | A |
| 5 | 选择题 | D |
| 6 | 选择题 | D |
| 7 | 选择题 | C |
| 8 | 选择题 | B |
| 9 | 填空题 | $1$ |
| 10 | 填空题 | $\dfrac{\pi}{4}$ |
| 11 | 填空题 | $0$ |
| 12 | 填空题 | $y=\sqrt{x}$ |
| 13 | 填空题 | $(-1,0)$ |
| 14 | 填空题 | $-27$ |
| 15 | 解答题 | $a=1,\ k=2$ |
| 16 | 解答题 | 极大值为 $\dfrac1{\sqrt e}$（在 $(1,0)$ 处），极小值为 $-\dfrac1{\sqrt e}$（在 $(-1,0)$ 处） |
| 17 | 解答题 | 面积为 $2$，体积为 $\dfrac{8\pi}{3}$ |
| 18 | 解答题 | $\dfrac{15}{16}$ |
| 19 | 解答题 | $f(x)=e^x$；拐点为 $(0,0)$ |
| 20 | 证明题 | 见解析 |
| 21 | 证明题 | 在 $\left(\dfrac12,1\right)$ 内有唯一实根；且 $\displaystyle\lim_{n\to\infty}x_n=\frac12$ |
| 22 | 解答题 | $\lvert A\rvert=1-a^4$；当 $a=-1$ 时有无穷多解，通解为 $\begin{pmatrix}t\\ t-1\\ t\\ t\end{pmatrix}$ |
| 23 | 解答题 | $a=-1$；可化为标准形 $2y_1^2+6y_2^2$（另一个特征值为 $0$） |

## 详细解析

### 第 1 题

- 答案：C

当 $x\to 1$ 时，分母趋于 $0$ 而分子不为 $0$，故有一条竖直渐近线 $x=1$；当 $x\to\infty$ 时，
$$
\frac{x^2+x}{x^2-1}\to 1,
$$
故有一条水平渐近线 $y=1$。又因 $x=-1$ 时分子分母同为 $0$，化简后是可去间断点，不再产生渐近线，所以共有两条。

### 第 2 题

- 答案：C

在 $x=0$ 处，只有第一因子 $e^x-1$ 为 $0$，其导数为 $1$；其余因子在 $x=0$ 的值分别为
$$
e^{2\cdot 0}-2=-1,\ \ldots,\ e^{n\cdot 0}-n=1-n.
$$
因而
$$
f'(0)=1\cdot(-1)\cdot(-2)\cdots (1-n)=(-1)^{n-1}(n-1)! \cdot n = (-1)^{n-1}n!.
$$

### 第 3 题

- 答案：B

由 $a_n>0$ 可知 $\{S_n\}$ 单调递增。若 $\{S_n\}$ 有界，则级数 $\sum a_n$ 收敛，从而必有 $a_n\to 0$，所以它是充分条件。
但反过来 $a_n\to 0$ 不保证 $\sum a_n$ 收敛，例如 $a_n=\frac1n$，故不是必要条件。

### 第 4 题

- 答案：A

把
$$
I(k)=\int_0^k e^{x^2}\sin x\,dx
$$
看作关于上限 $k$ 的函数，则
$$
I'(k)=e^{k^2}\sin k.
$$
因为 $1,2,3\in(0,\pi)$，且在 $(0,\pi)$ 上有 $\sin k>0$，所以 $I(k)$ 在该区间单调递增，从而
$$
I_1<I_2<I_3.
$$

### 第 5 题

- 答案：D

条件说明 $f$ 关于 $x$ 单调递增，关于 $y$ 单调递减。若 $x_1<x_2$ 且 $y_1>y_2$，则由 $x$ 增大使函数值增大，由 $y$ 减小也使函数值增大，因此
$$
f(x_1,y_1)<f(x_2,y_2).
$$

### 第 6 题

- 答案：D

由于区域关于 $y$ 轴对称，而被积函数中的 $xy^5$ 关于 $x$ 是奇函数，所以
$$
\iint_D xy^5\,dxdy=0.
$$
因而原积分化为
$$
-\iint_D 1\,dxdy=-|D|.
$$
区域面积
$$
|D|=\int_{-\pi/2}^{\pi/2}(1-\sin x)\,dx=\pi,
$$
故原积分为 $-\pi$。

### 第 7 题

- 答案：C

有
$$
\alpha_3+\alpha_4=\begin{pmatrix}0\\0\\c_3+c_4\end{pmatrix},
$$
它与 $\alpha_1=\begin{pmatrix}0\\0\\c_1\end{pmatrix}$ 共线，所以 $\alpha_1,\alpha_3,\alpha_4$ 必线性相关。

### 第 8 题

- 答案：B

由于
$$
Q=P\begin{pmatrix}
1&0&0\\
1&1&0\\
0&0&1
\end{pmatrix},
$$
而对角矩阵前两个特征值同为 $1$，在对应二维特征子空间内改变基并不会改变其对角形，因此
$$
Q^{-1}AQ=\operatorname{diag}(1,1,2).
$$

### 第 9 题

- 答案：$1$

由 $x=0$ 可得 $1-y=e^y-1$，解得 $y(0)=0$。对方程两边求导：
$$
2x-y'=e^y y'.
$$
于是
$$
y'=\frac{2x}{1+e^y},
$$
从而 $y'(0)=0$。再对上式求导并代入 $(0,0)$，得到
$$
2-y''=e^0(y')^2+e^0 y''=y'',
$$
故 $y''(0)=1$。

### 第 10 题

- 答案：$\dfrac{\pi}{4}$

原式可写为
$$
\sum_{i=1}^n \frac{1}{n}\cdot \frac{1}{1+\left(\frac{i}{n}\right)^2},
$$
这是函数 $\frac{1}{1+x^2}$ 在 $[0,1]$ 上的黎曼和，因此极限为
$$
\int_0^1 \frac{dx}{1+x^2}=\arctan 1-\arctan 0=\frac{\pi}{4}.
$$

### 第 11 题

- 答案：$0$

记
$$
u=\ln x+\frac1y,\qquad z=f(u).
$$
则
$$
z_x=f'(u)\cdot \frac1x,\qquad z_y=f'(u)\cdot\left(-\frac1{y^2}\right).
$$
所以
$$
xz_x+y^2z_y=f'(u)-f'(u)=0.
$$

### 第 12 题

- 答案：$y=\sqrt{x}$

将 $x$ 视为 $y$ 的函数，有
$$
y\frac{dx}{dy}+x-3y^2=0,
$$
即
$$
\frac{dx}{dy}+\frac{1}{y}x=3y.
$$
这是关于 $x(y)$ 的一阶线性方程。乘积分因子 $y$ 得
$$
\frac{d(xy)}{dy}=3y^2,
$$
故
$$
xy=y^3+C.
$$
代入 $(x,y)=(1,1)$ 得 $C=0$，从而 $x=y^2$。由初值 $y(1)=1>0$，知取正支：
$$
y=\sqrt{x}.
$$

### 第 13 题

- 答案：$(-1,0)$

对曲线 $y=x^2+x$ 有
$$
y'=2x+1,\qquad y''=2.
$$
曲率
$$
K=\frac{|y''|}{\left(1+(y')^2\right)^{3/2}}
=\frac{2}{\left(1+(2x+1)^2\right)^{3/2}}.
$$
令其等于 $\frac{\sqrt2}{2}$，化简得
$$
(2x+1)^2=1.
$$
解得 $x=0$ 或 $x=-1$。由条件 $x<0$，取 $x=-1$，此时 $y=0$。

### 第 14 题

- 答案：$-27$

交换两行使行列式变号，所以
$$
|B|=-|A|=-3.
$$
又因为 $A$ 为 $3$ 阶矩阵，
$$
|A^*|=|A|^{3-1}=|A|^2=9.
$$
故
$$
|BA^*|=|B|\cdot |A^*|=(-3)\cdot 9=-27.
$$

### 第 15 题

- 答案：$a=1,\ k=2$

先算极限：
$$
f(x)=\frac{x(1+x)-\sin x}{x\sin x}.
$$
由 $\sin x=x-\frac{x^3}{6}+o(x^3)$，得
$$
x(1+x)-\sin x=x^2+o(x^2),
$$
且 $x\sin x=x^2+o(x^2)$，所以
$$
a=\lim_{x\to 0}f(x)=1.
$$

再看
$$
f(x)-1=\frac{x-\sin x}{\sin x}.
$$
由于
$$
x-\sin x\sim \frac{x^3}{6},\qquad \sin x\sim x,
$$
故
$$
f(x)-1\sim \frac{x^2}{6}.
$$
因而它与 $x^k$ 同阶时应有 $k=2$。

### 第 16 题

- 答案：极大值为 $\dfrac1{\sqrt e}$（在 $(1,0)$ 处），极小值为 $-\dfrac1{\sqrt e}$（在 $(-1,0)$ 处）

有
$$
f_x=e^{-\frac{x^2+y^2}{2}}(1-x^2),\qquad
f_y=-xye^{-\frac{x^2+y^2}{2}}.
$$
令偏导同时为零，得驻点为 $(1,0)$ 与 $(-1,0)$。

固定 $x$ 时，$e^{-(x^2+y^2)/2}$ 在 $y=0$ 处最大，因此极值只能落在 $y=0$ 上。于是问题化为研究
$$
g(x)=xe^{-x^2/2}.
$$
有
$$
g'(x)=e^{-x^2/2}(1-x^2),
$$
故在 $x=1$ 取极大值，在 $x=-1$ 取极小值。相应函数值为
$$
g(1)=e^{-1/2}=\frac1{\sqrt e},\qquad g(-1)=-e^{-1/2}=-\frac1{\sqrt e}.
$$

### 第 17 题

- 答案：面积为 $2$，体积为 $\dfrac{8\pi}{3}$

设切点为 $A(x_0,\ln x_0)$。曲线 $y=\ln x$ 在 $A$ 点的切线为
$$
y-\ln x_0=\frac1{x_0}(x-x_0).
$$
代入点 $(0,1)$，得
$$
1-\ln x_0=-1,\qquad \ln x_0=2,
$$
所以 $x_0=e^2$，即 $A=(e^2,2)$。又曲线 $L$ 与 $x$ 轴交于
$$
B=(1,0).
$$
因而弦 $AB$ 的方程为
$$
y=\frac{2}{e^2-1}(x-1),
$$
即
$$
x=1+\frac{e^2-1}{2}y.
$$

用 $y$ 作积分变量，曲线写成 $x=e^y$，积分区间为 $0\le y\le 2$。面积为
$$
S=\int_0^2 \left(1+\frac{e^2-1}{2}y-e^y\right)\,dy=2.
$$

绕 $x$ 轴旋转的体积为
$$
V=\pi\int_0^2 y^2\left(1+\frac{e^2-1}{2}y-e^y\right)\,dy
=\frac{8\pi}{3}.
$$

### 第 18 题

- 答案：$\dfrac{15}{16}$

改用极坐标：
$$
x=r\cos\theta,\qquad y=r\sin\theta,\qquad d\sigma=r\,dr\,d\theta.
$$
于是
$$
\iint_D xy\,d\sigma
=\int_0^\pi\int_0^{1+\cos\theta} r^3\sin\theta\cos\theta\,dr\,d\theta
=\frac14\int_0^\pi (1+\cos\theta)^4\sin\theta\cos\theta\,d\theta.
$$
令 $u=1+\cos\theta$ 或直接展开积分，可得结果
$$
\iint_D xy\,d\sigma=\frac{15}{16}.
$$

### 第 19 题

- 答案：$f(x)=e^x$；拐点为 $(0,0)$

由
$$
f''+f'-2f=0
$$
的特征方程
$$
r^2+r-2=0
$$
得通解
$$
f(x)=C_1e^x+C_2e^{-2x}.
$$
代入第二个方程
$$
f''+f=2e^x
$$
可解得 $C_1=1,\ C_2=0$，故
$$
f(x)=e^x.
$$

于是
$$
y=e^{x^2}\int_0^x e^{-t^2}\,dt.
$$
计算导数可得 $y''(0)=0$，并可验证当 $x<0$ 时 $y''<0$、当 $x>0$ 时 $y''>0$，故凹凸性在 $x=0$ 两侧改变，所以唯一拐点为
$$
(0,0).
$$

### 第 20 题

- 答案：见解析

令
$$
F(x)=x\ln\frac{1+x}{1-x}+\cos x-1-\frac{x^2}{2}.
$$
有 $F(0)=0$。计算导数：
$$
F'(x)=\ln\frac{1+x}{1-x}-\sin x+\frac{2x}{1-x^2}-x.
$$
在 $(-1,1)$ 上可利用
$$
\ln\frac{1+x}{1-x}\ge 2x,\qquad \sin x\le x
$$
以及 $\frac{2x}{1-x^2}-x\ge 0$（按 $x>0$、$x<0$ 分别讨论）推出 $F'(x)\ge 0$。因此 $F$ 在 $(-1,1)$ 上以 $0$ 为最小值点，从而
$$
F(x)\ge F(0)=0,
$$
即
$$
x\ln\frac{1+x}{1-x}+\cos x\ge 1+\frac{x^2}{2}.
$$

### 第 21 题

- 答案：在 $\left(\dfrac12,1\right)$ 内有唯一实根；且 $\displaystyle\lim_{n\to\infty}x_n=\frac12$

令
$$
f_n(x)=x+x^2+\cdots+x^n-1.
$$
在 $\left(\frac12,1\right)$ 上，$f_n'(x)=1+2x+\cdots+nx^{n-1}>0$，故 $f_n$ 严格递增。
又
$$
f_n\!\left(\frac12\right)=\frac12+\frac14+\cdots+\frac1{2^n}-1<0,\qquad
f_n(1)=n-1>0,
$$
由介值定理知在 $\left(\frac12,1\right)$ 内恰有一个实根。

由方程
$$
x_n+x_n^2+\cdots+x_n^n=1
$$
可知 $x_n>\frac12$。又比较 $f_{n+1}(x_n)=x_n^{n+1}>0$，而 $f_{n+1}$ 递增，得 $x_{n+1}<x_n$，所以 $\{x_n\}$ 单调递减且下有界，从而收敛。
设极限为 $a$。由
$$
x_n(1-x_n^n)=1-x_n
$$
或直接对原式放缩并令 $n\to\infty$，可得极限满足
$$
\frac{a}{1-a}=1,
$$
故
$$
a=\frac12.
$$

### 第 22 题

- 答案：$\lvert A\rvert=1-a^4$；当 $a=-1$ 时有无穷多解，通解为 $\begin{pmatrix}t\\ t-1\\ t\\ t\end{pmatrix}$

先计算行列式，可得
$$
\lvert A\rvert=1-a^4.
$$
因而方程组要有无穷多解，必须先有 $\lvert A\rvert=0$，即 $a=\pm 1$。

分别代入增广矩阵检验相容性：当 $a=1$ 时方程组不相容；当 $a=-1$ 时，
$$
\begin{cases}
x_1-x_2=1,\\
x_2-x_3=-1,\\
x_3-x_4=0,\\
-x_1+x_4=0.
\end{cases}
$$
由后两式得 $x_4=x_1,\ x_3=x_1$，再由第二式得 $x_2=x_1-1$。令 $x_1=t$，则通解为
$$
x=\begin{pmatrix}t\\ t-1\\ t\\ t\end{pmatrix}
=\begin{pmatrix}0\\ -1\\ 0\\ 0\end{pmatrix}
+t\begin{pmatrix}1\\ 1\\ 1\\ 1\end{pmatrix}.
$$

### 第 23 题

- 答案：$a=-1$；可化为标准形 $2y_1^2+6y_2^2$（另一个特征值为 $0$）

由
$$
\operatorname{rank}(A^{\mathsf T}A)=\operatorname{rank}(A)=2
$$
可知矩阵 $A$ 的秩为 $2$。对 $A$ 做行列式或子式计算，可得唯一满足条件的参数为
$$
a=-1.
$$

此时
$$
A^{\mathsf T}A=
\begin{pmatrix}
2&0&2\\
0&2&2\\
2&2&4
\end{pmatrix}.
$$
它的特征值为
$$
0,\ 2,\ 6.
$$
取对应的单位正交特征向量为
$$
\alpha_1=\frac1{\sqrt2}\begin{pmatrix}1\\ -1\\ 0\end{pmatrix},\quad
\alpha_2=\frac1{\sqrt6}\begin{pmatrix}1\\ 1\\ 2\end{pmatrix},\quad
\alpha_3=\frac1{\sqrt3}\begin{pmatrix}1\\ 1\\ -1\end{pmatrix}.
$$
令
$$
Q=(\alpha_1,\alpha_2,\alpha_3),
$$
则 $Q$ 为正交矩阵，且
$$
Q^{\mathsf T}(A^{\mathsf T}A)Q=\operatorname{diag}(2,6,0).
$$
因而在正交变换 $x=Qy$ 下，
$$
f=2y_1^2+6y_2^2.
$$
