# Math 1 2013 Answers

资料类型：考研数学一答案解析
年份：2013
科目：数学一
来源：2013 年数学一真题答案解析页图像与本目录题干截图
校对状态：已按题干截图与答案解析页图像核对，并清洗整理

## 答案速查

| 题号 | 题型 | 答案 |
|---|---|---|
| 1 | 选择题 | D |
| 2 | 选择题 | A |
| 3 | 选择题 | C |
| 4 | 选择题 | D |
| 5 | 选择题 | B |
| 6 | 选择题 | B |
| 7 | 选择题 | A |
| 8 | 选择题 | C |
| 9 | 填空题 | $1$ |
| 10 | 填空题 | $\displaystyle y=C_1e^{3x}+C_2e^x-xe^{2x}$ |
| 11 | 填空题 | $\sqrt{2}$ |
| 12 | 填空题 | $\ln2$ |
| 13 | 填空题 | $-1$ |
| 14 | 填空题 | $\displaystyle 1-\frac{1}{e}$ |
| 15 | 解答题 | $\displaystyle -4\ln2+8-2\pi$ |
| 16 | 解答题 | (1) $S''(x)-S(x)=0$；(2) $\displaystyle S(x)=2e^x+e^{-x}$。 |
| 17 | 解答题 | 极小值 $\displaystyle f\left(1,-\frac{4}{3}\right)=-e^{-\frac{1}{3}}$；无极大值。 |
| 18 | 解答题 | 证明题：存在 $\xi\in(0,1)$ 使 $f'(\xi)=1$，且存在 $\eta\in(-1,1)$ 使 $f''(\eta)+f'(\eta)=1$。 |
| 19 | 解答题 | (1) $x^2+y^2=2z^2-2z+1$；(2) 形心 $\displaystyle \left(0,0,\frac{7}{5}\right)$。 |
| 20 | 解答题 | $a=-1,b=0$；$\displaystyle C=\begin{pmatrix}1+k_1+k_2&-k_2\\k_2&k_1\end{pmatrix}$，$k_1,k_2\in\mathbb{R}$。 |
| 21 | 解答题 | 证明题：对应矩阵 $2\alpha\alpha^T+\beta\beta^T$，正交标准形 $2y_1^2+y_2^2$。 |
| 22 | 解答题 | $F_Y(y)=0\ (y<1)$，$F_Y(y)=\frac{y^3+18}{27}\ (1\le y<2)$，$F_Y(y)=1\ (y\ge2)$；$P\{X\le Y\}=\frac{8}{27}$。 |
| 23 | 解答题 | 矩估计 $\hat\theta=\bar X$；最大似然估计 $\displaystyle \hat\theta=\frac{2n}{\sum_{i=1}^n\frac{1}{X_i}}$。 |

## 详细解析

### 第 1 题

**答案：** D

当 $x\to0$ 时，
$$
\arctan x=x-\frac{x^3}{3}+o(x^3),
$$
所以
$$
x-\arctan x=\frac{x^3}{3}+o(x^3).
$$
若
$$
\lim_{x\to0}\frac{x-\arctan x}{x^k}=c\ne0,
$$
则分子与 $x^k$ 必须同阶，故 $k=3$，并且
$$
c=\frac{1}{3}.
$$
因此选 D。

### 第 2 题

**答案：** A

令
$$
F(x,y,z)=x^2+\cos(xy)+yz+x.
$$
则
$$
F_x=2x-y\sin(xy)+1,\qquad
F_y=-x\sin(xy)+z,\qquad
F_z=y.
$$
在 $(0,1,-1)$ 处，法向量为
$$
(F_x,F_y,F_z)=(1,-1,1).
$$
切平面方程为
$$
1(x-0)-1(y-1)+1(z+1)=0,
$$
即
$$
x-y+z=-2.
$$
因此选 A。

### 第 3 题

**答案：** C

给出的级数是 $f(x)$ 在 $(0,1)$ 上的正弦级数，对应 $f$ 的奇延拓，并以 $2$ 为周期。

因为
$$
-\frac{9}{4}+2=-\frac{1}{4},
$$
且 $-\frac{1}{4}$ 不是延拓函数的间断点，所以
$$
S\left(-\frac{9}{4}\right)=S\left(-\frac{1}{4}\right)
=-f\left(\frac{1}{4}\right)
=-\left|\frac{1}{4}-\frac{1}{2}\right|
=-\frac{1}{4}.
$$
因此选 C。

### 第 4 题

**答案：** D

由格林公式，若 $L$ 围成区域 $D$，则
$$
I=\iint_D\left[\frac{\partial}{\partial x}\left(2x-\frac{x^3}{3}\right)
-\frac{\partial}{\partial y}\left(y+\frac{y^3}{6}\right)\right]dxdy
=\iint_D\left(1-x^2-\frac{y^2}{2}\right)dxdy.
$$

分别计算四个区域上的二重积分：
$$
I_1=\pi-\frac{\pi}{4}-\frac{\pi}{8}=\frac{5\pi}{8},
$$
$$
I_2=2\pi-\pi-\frac{\pi}{2}=\frac{\pi}{2},
$$
$$
I_3=\pi\sqrt{2}-\frac{\pi\sqrt{2}}{2}-\frac{1}{2}\cdot\frac{\pi\sqrt{2}}{4}
=\frac{3\pi\sqrt{2}}{8},
$$
$$
I_4=\pi\sqrt{2}-\frac{\pi\sqrt{2}}{4}-\frac{1}{2}\cdot\frac{\pi\sqrt{2}}{2}
=\frac{\pi\sqrt{2}}{2}.
$$
显然
$$
|I_4|>|I_1|>|I_3|>|I_2|.
$$
因此最大者为 $I_4$，选 D。

### 第 5 题

**答案：** B

由 $C=AB$ 可知，$C$ 的每一列都是 $A$ 的列向量组的线性组合，所以 $C$ 的列向量组可由 $A$ 的列向量组线性表示。

又因为 $B$ 可逆，
$$
A=CB^{-1},
$$
所以 $A$ 的每一列也可由 $C$ 的列向量组线性表示。

因此矩阵 $C$ 的列向量组与矩阵 $A$ 的列向量组等价，选 B。

### 第 6 题

**答案：** B

记
$$
A=\begin{pmatrix}
1&a&1\\
a&b&a\\
1&a&1
\end{pmatrix}.
$$
因为第一行与第三行相同，所以 $0$ 是 $A$ 的特征值。又
$$
\operatorname{tr}A=2+b,
$$
若 $2$ 是 $A$ 的特征值，则另一个特征值必为 $b$。

计算
$$
\det(2E-A)=
\det\begin{pmatrix}
1&-a&-1\\
-a&2-b&-a\\
-1&-a&1
\end{pmatrix}=-4a^2.
$$
因此 $2$ 是 $A$ 的特征值当且仅当 $a=0$。

当 $a=0$ 时，$A$ 为实对称矩阵，必可正交对角化，其特征值为 $2,b,0$，故与 $\operatorname{diag}(2,b,0)$ 相似。于是充分必要条件为 $a=0$，$b$ 任意，选 B。

### 第 7 题

**答案：** A

标准化得
$$
p_1=P\{-2\le Z\le2\}=\Phi(2)-\Phi(-2),
$$
$$
p_2=P\{-1\le Z\le1\}=\Phi(1)-\Phi(-1),
$$
$$
p_3=P\left\{-\frac{7}{3}\le Z\le-1\right\}=\Phi(-1)-\Phi\left(-\frac{7}{3}\right).
$$
其中 $Z\sim N(0,1)$。显然 $p_1$ 是中心区间 $[-2,2]$ 的概率，$p_2$ 是中心区间 $[-1,1]$ 的概率，故 $p_1>p_2$；而 $p_3$ 位于左侧尾部区间 $[-\frac{7}{3},-1]$，其概率小于中心区间 $[-1,1]$ 的概率，故 $p_2>p_3$。

因此 $p_1>p_2>p_3$，选 A。

### 第 8 题

**答案：** C

若 $X\sim t(n)$，则
$$
X^2\sim F(1,n).
$$
又 $Y\sim F(1,n)$，所以 $Y$ 与 $X^2$ 同分布。由 $0<\alpha<0.5$ 且 $P\{X>c\}=\alpha$ 可知 $c>0$。于是
$$
P\{Y>c^2\}=P\{X^2>c^2\}=P\{|X|>c\}.
$$
$t$ 分布关于 $0$ 对称，故
$$
P\{|X|>c\}=2P\{X>c\}=2\alpha.
$$
因此选 C。

### 第 9 题

**答案：** $1$

令 $x=0$，由方程得 $f(0)=1$。对
$$
f(x)-x=e^{x(1-f(x))}
$$
两边关于 $x$ 求导，得
$$
f'(x)-1=e^{x(1-f(x))}\left[1-f(x)-xf'(x)\right].
$$
代入 $x=0$，并用 $f(0)=1$，有
$$
f'(0)-1=1\cdot(1-1)=0,
$$
故 $f'(0)=1$。

于是
$$
\lim_{n\to\infty}n\left[f\left(\frac{1}{n}\right)-1\right]
=\lim_{x\to0}\frac{f(x)-f(0)}{x}=f'(0)=1.
$$

### 第 10 题

**答案：** $\displaystyle y=C_1e^{3x}+C_2e^x-xe^{2x}$

非齐次线性方程任意两个解之差是对应齐次方程的解。由题意，
$$
y_1-y_3=e^{3x},\qquad y_2-y_3=e^x.
$$
因此对应齐次方程的通解为
$$
y_h=C_1e^{3x}+C_2e^x.
$$
取非齐次方程的一个特解 $y_3=-xe^{2x}$，得原方程通解
$$
y=C_1e^{3x}+C_2e^x-xe^{2x}.
$$

### 第 11 题

**答案：** $\sqrt{2}$

由参数方程，
$$
\frac{dx}{dt}=\cos t,
$$
$$
\frac{dy}{dt}=\sin t+t\cos t-\sin t=t\cos t.
$$
故
$$
\frac{dy}{dx}=\frac{dy/dt}{dx/dt}=t.
$$
于是
$$
\frac{d^2y}{dx^2}=\frac{d}{dx}\left(\frac{dy}{dx}\right)
=\frac{dt}{dx}=\frac{1}{\cos t}.
$$
代入 $t=\frac{\pi}{4}$，得
$$
\left.\frac{d^2y}{dx^2}\right|_{t=\frac{\pi}{4}}=\frac{1}{\cos\frac{\pi}{4}}=\sqrt{2}.
$$

### 第 12 题

**答案：** $\ln2$

分部积分，取
$$
u=\ln x,
\qquad
 dv=\frac{dx}{(1+x)^2},
$$
则
$$
du=\frac{dx}{x},
\qquad
v=-\frac{1}{1+x}.
$$
边界项
$$
\left.-\frac{\ln x}{1+x}\right|_1^{+\infty}=0.
$$
所以
$$
\int_1^{+\infty}\frac{\ln x}{(1+x)^2}\,dx
=\int_1^{+\infty}\frac{1}{x(1+x)}\,dx
=\int_1^{+\infty}\left(\frac{1}{x}-\frac{1}{1+x}\right)dx
=\ln2.
$$

### 第 13 题

**答案：** $-1$

设 $C=(A_{ij})$ 为代数余子式矩阵，则题设给出
$$
C=-A.
$$
而伴随矩阵为 $A^*=C^T$，故
$$
A^*=-A^T.
$$
两边取行列式，因 $A$ 为 $3$ 阶矩阵，有
$$
|A^*|=\det A^2,
\qquad
\det(-A^T)=-\det A,
$$
所以
$$
\det A^2=-\det A,
$$
即 $\det A=0$ 或 $\det A=-1$。

若 $\det A=0$，则 $r(A)<3$。当 $r(A)=2$ 时，$r(A^*)=1$；当 $r(A)\le1$ 时，$A^*=O$。这都与 $A^*=-A^T$ 且 $A$ 非零矛盾。因此 $\det A\ne0$，只能有
$$
\det A=-1.
$$

### 第 14 题

**答案：** $\displaystyle 1-\frac{1}{e}$

由指数分布的无记忆性，
$$
P\{Y\le a+1\mid Y>a\}=P\{Y-a\le1\mid Y>a\}=P\{Y\le1\}.
$$
参数为 $1$ 的指数分布满足 $F_Y(y)=1-e^{-y}$，$y\ge0$。故
$$
P\{Y\le1\}=1-e^{-1}=1-\frac{1}{e}.
$$

### 第 15 题

**答案：** $\displaystyle -4\ln2+8-2\pi$

由题设，
$$
f(1)=0,
\qquad
f'(x)=\frac{\ln(x+1)}{x}.
$$
记
$$
I=\int_0^1\frac{f(x)}{\sqrt{x}}\,dx.
$$
对 $I$ 分部积分，取 $u=f(x)$，$dv=x^{-1/2}dx$，则 $v=2\sqrt{x}$，边界项为 $0$，所以
$$
I=-2\int_0^1\sqrt{x}\,f'(x)\,dx
=-2\int_0^1\frac{\ln(1+x)}{\sqrt{x}}\,dx.
$$
令 $x=t^2$，则 $dx=2t\,dt$，得
$$
I=-4\int_0^1\ln(1+t^2)\,dt.
$$
又
$$
\int\ln(1+t^2)\,dt
=t\ln(1+t^2)-2t+2\arctan t,
$$
故
$$
\int_0^1\ln(1+t^2)\,dt=\ln2-2+\frac{\pi}{2}.
$$
因此
$$
I=-4\left(\ln2-2+\frac{\pi}{2}\right)
=-4\ln2+8-2\pi.
$$

### 第 16 题

**答案：** (1) $S''(x)-S(x)=0$；(2) $\displaystyle S(x)=2e^x+e^{-x}$。

由幂级数逐项求导，
$$
S''(x)=\sum_{n=2}^{\infty}n(n-1)a_nx^{n-2}.
$$
根据递推关系 $n(n-1)a_n=a_{n-2}$，得
$$
S''(x)=\sum_{n=2}^{\infty}a_{n-2}x^{n-2}
=\sum_{m=0}^{\infty}a_mx^m
=S(x).
$$
所以
$$
S''(x)-S(x)=0.
$$

微分方程 $S''-S=0$ 的通解为
$$
S(x)=C_1e^x+C_2e^{-x}.
$$
又
$$
S(0)=a_0=3,
\qquad
S'(0)=a_1=1,
$$
所以
$$
C_1+C_2=3,
\qquad
C_1-C_2=1.
$$
解得 $C_1=2,\ C_2=1$。因此
$$
S(x)=2e^x+e^{-x}.
$$

### 第 17 题

**答案：** 函数仅有极小值，极小值点为 $\left(1,-\frac{4}{3}\right)$，极小值为 $\displaystyle -e^{-\frac{1}{3}}$。

令
$$
g(x,y)=y+\frac{x^3}{3},
\qquad
f(x,y)=g(x,y)e^{x+y}.
$$
一阶偏导为
$$
f_x=e^{x+y}\left(x^2+y+\frac{x^3}{3}\right),
\qquad
f_y=e^{x+y}\left(y+\frac{x^3}{3}+1\right).
$$
令 $f_x=f_y=0$，得
$$
\begin{cases}
x^2+y+\frac{x^3}{3}=0,\\
y+\frac{x^3}{3}+1=0,
\end{cases}
$$
相减得 $x^2-1=0$，故驻点为
$$
\left(-1,-\frac{2}{3}\right),
\qquad
\left(1,-\frac{4}{3}\right).
$$

在驻点处，
$$
f_{xx}=e^{x+y}(2x+x^2),
\qquad
f_{xy}=e^{x+y},
\qquad
f_{yy}=e^{x+y}.
$$
在 $\left(-1,-\frac{2}{3}\right)$ 处，判别式
$$
D=f_{xx}f_{yy}-f_{xy}^2<0,
$$
故不是极值点。

在 $\left(1,-\frac{4}{3}\right)$ 处，
$$
f_{xx}=3e^{-1/3},
\qquad
f_{xy}=e^{-1/3},
\qquad
f_{yy}=e^{-1/3},
$$
所以
$$
D=3e^{-2/3}-e^{-2/3}=2e^{-2/3}>0,
\qquad
f_{xx}>0.
$$
该点为极小值点，极小值为
$$
f\left(1,-\frac{4}{3}\right)
=\left(-\frac{4}{3}+\frac{1}{3}\right)e^{-1/3}
=-e^{-1/3}.
$$
因此函数无极大值，只有上述极小值。

### 第 18 题

**答案：** 两个存在性结论均成立。

(1) 因为 $f(x)$ 为奇函数，所以 $f(0)=0$。令
$$
F(x)=f(x)-x,
\qquad x\in[0,1].
$$
则
$$
F(0)=f(0)-0=0,
\qquad
F(1)=f(1)-1=0.
$$
由罗尔定理，存在 $\xi\in(0,1)$，使得
$$
F'(\xi)=0,
$$
即
$$
f'(\xi)=1.
$$

(2) 奇函数的导函数 $f'(x)$ 为偶函数，因此 $f'(-1)=f'(1)$。令
$$
G(x)=f'(x)+f(x)-x,
\qquad x\in[-1,1].
$$
则
$$
G(1)=f'(1)+f(1)-1=f'(1),
$$
而 $f(-1)=-f(1)=-1$，所以
$$
G(-1)=f'(-1)+f(-1)+1=f'(1).
$$
故 $G(-1)=G(1)$。由罗尔定理，存在 $\eta\in(-1,1)$，使得
$$
G'(\eta)=0.
$$
又
$$
G'(x)=f''(x)+f'(x)-1,
$$
所以
$$
f''(\eta)+f'(\eta)=1.
$$

### 第 19 题

**答案：** (1) $\Sigma:x^2+y^2=2z^2-2z+1$；(2) $\Omega$ 的形心为 $\displaystyle \left(0,0,\frac{7}{5}\right)$。

直线 $L$ 可参数化为
$$
(x,y,z)=(1-t,t,t),
$$
即取 $z=t$ 时，直线上对应点为
$$
(x_0,y_0,z)=(1-z,z,z).
$$
绕 $z$ 轴旋转后，同一高度 $z$ 处的半径平方为
$$
x^2+y^2=x_0^2+y_0^2=(1-z)^2+z^2=2z^2-2z+1.
$$
故曲面方程为
$$
\Sigma:x^2+y^2=2z^2-2z+1.
$$

由旋转对称性，形心满足 $\bar x=\bar y=0$。在高度 $z$ 处，截面面积为
$$
A(z)=\pi(2z^2-2z+1),\qquad 0\le z\le2.
$$
体积
$$
V=\int_0^2 A(z)\,dz
=\pi\int_0^2(2z^2-2z+1)\,dz
=\frac{10\pi}{3}.
$$
于是
$$
\bar z=\frac{1}{V}\int_0^2 zA(z)\,dz
=\frac{\pi}{V}\int_0^2(2z^3-2z^2+z)\,dz
=\frac{\pi\cdot\frac{14}{3}}{\frac{10\pi}{3}}
=\frac{7}{5}.
$$
所以 $\Omega$ 的形心为
$$
\left(0,0,\frac{7}{5}\right).
$$

### 第 20 题

**答案：** 当且仅当 $a=-1,b=0$ 时存在矩阵 $C$。此时 $\displaystyle C=\begin{pmatrix}1+k_1+k_2&-k_2\\k_2&k_1\end{pmatrix}$，其中 $k_1,k_2\in\mathbb{R}$。

设
$$
C=\begin{pmatrix}x_1&x_2\\x_3&x_4\end{pmatrix}.
$$
直接计算
$$
AC-CA=
\begin{pmatrix}
ax_3-x_2&-ax_1+x_2+ax_4\\
x_1-x_3-x_4&x_2-ax_3
\end{pmatrix}.
$$
令其等于
$$
B=\begin{pmatrix}0&1\\1&b\end{pmatrix},
$$
得到方程组
$$
\begin{cases}
ax_3-x_2=0,\\
-ax_1+x_2+ax_4=1,\\
x_1-x_3-x_4=1,\\
x_2-ax_3=b.
\end{cases}
$$
由第一式 $x_2=ax_3$，代入第四式得 $b=0$。再结合第三式
$$
-x_1+x_3+x_4=-1,
$$
代入第二式得
$$
a(-x_1+x_3+x_4)=1,
$$
故 $-a=1$，即 $a=-1$。

当 $a=-1,b=0$ 时，方程组化为
$$
x_2=-x_3,
\qquad
x_1=1+x_3+x_4.
$$
令 $x_4=k_1,\ x_3=k_2$，得全部解
$$
C=\begin{pmatrix}
1+k_1+k_2&-k_2\\
k_2&k_1
\end{pmatrix},
\qquad k_1,k_2\in\mathbb{R}.
$$
因此当且仅当 $a=-1,b=0$ 时存在满足条件的矩阵 $C$。

### 第 21 题

**答案：** (1) 对应矩阵为 $2\alpha\alpha^T+\beta\beta^T$；(2) 在给定条件下正交标准形为 $2y_1^2+y_2^2$。

记
$$
x=(x_1,x_2,x_3)^T.
$$
则
$$
a_1x_1+a_2x_2+a_3x_3=\alpha^Tx,
\qquad
b_1x_1+b_2x_2+b_3x_3=\beta^Tx.
$$
因此
$$
f=2(\alpha^Tx)^2+(\beta^Tx)^2
=2x^T\alpha\alpha^Tx+x^T\beta\beta^Tx
=x^T(2\alpha\alpha^T+\beta\beta^T)x.
$$
又 $2\alpha\alpha^T+\beta\beta^T$ 为对称矩阵，所以它就是二次型对应的矩阵。

设
$$
A=2\alpha\alpha^T+\beta\beta^T.
$$
若 $\alpha,\beta$ 正交且均为单位向量，则
$$
A\alpha=2\alpha(\alpha^T\alpha)+\beta(\beta^T\alpha)=2\alpha,
$$
$$
A\beta=2\alpha(\alpha^T\beta)+\beta(\beta^T\beta)=\beta.
$$
再取单位向量 $\gamma$ 与 $\alpha,\beta$ 都正交，则
$$
A\gamma=0.
$$
于是 $A$ 在正交基 $\alpha,\beta,\gamma$ 下的对角矩阵为
$$
\operatorname{diag}(2,1,0).
$$
所以二次型在正交变换下的标准形为
$$
2y_1^2+y_2^2.
$$

### 第 22 题

**答案：**

(1)
$$
F_Y(y)=\begin{cases}
0,&y<1,\\
\frac{y^3+18}{27},&1\le y<2,\\
1,&y\ge2;
\end{cases}
$$
(2) $\displaystyle P\{X\le Y\}=\frac{8}{27}$。

由定义，$Y=1$ 对应 $X\ge2$，$Y=2$ 对应 $X\le1$，而当 $1<X<2$ 时 $Y=X$。

当 $y<1$ 时，显然
$$
F_Y(y)=0.
$$
当 $1\le y<2$ 时，
$$
F_Y(y)=P\{Y\le y\}=P\{X\ge2\}+P\{1<X\le y\}.
$$
其中
$$
P\{X\ge2\}=\int_2^3\frac{x^2}{9}\,dx=\frac{19}{27},
$$
$$
P\{1<X\le y\}=\int_1^y\frac{x^2}{9}\,dx=\frac{y^3-1}{27}.
$$
故
$$
F_Y(y)=\frac{19}{27}+\frac{y^3-1}{27}
=\frac{y^3+18}{27},\qquad 1\le y<2.
$$
当 $y\ge2$ 时，$F_Y(y)=1$。因此
$$
F_Y(y)=\begin{cases}
0,&y<1,\\
\frac{y^3+18}{27},&1\le y<2,\\
1,&y\ge2.
\end{cases}
$$

再求 $P\{X\le Y\}$。若 $X\le1$，则 $Y=2$，事件成立；若 $1<X<2$，则 $Y=X$，事件也成立；若 $X\ge2$，则 $Y=1$，事件不成立。故
$$
P\{X\le Y\}=P\{X<2\}
=\int_0^2\frac{x^2}{9}\,dx
=\frac{8}{27}.
$$

### 第 23 题

**答案：** (1) 矩估计量 $\displaystyle \hat\theta=\bar X$；(2) 最大似然估计量 $\displaystyle \hat\theta=\frac{2n}{\sum_{i=1}^n\frac{1}{X_i}}$。

先求数学期望：
$$
E(X)=\int_0^{\infty}x\frac{\theta^2}{x^3}e^{-\theta/x}\,dx
=\int_0^{\infty}\frac{\theta^2}{x^2}e^{-\theta/x}\,dx.
$$
令 $u=\frac{\theta}{x}$，则 $x=\frac{\theta}{u}$，$dx=-\frac{\theta}{u^2}du$，所以
$$
E(X)=\theta\int_0^{\infty}e^{-u}\,du=\theta.
$$
由矩估计法，令样本均值等于总体均值，得
$$
\hat\theta=\bar X.
$$

设样本观测值均大于 $0$。似然函数为
$$
L(\theta)=\prod_{i=1}^n\frac{\theta^2}{x_i^3}e^{-\theta/x_i}
=\theta^{2n}\left(\prod_{i=1}^n x_i^{-3}\right)
\exp\left(-\theta\sum_{i=1}^n\frac{1}{x_i}\right).
$$
对数似然为
$$
\ln L(\theta)=2n\ln\theta-3\sum_{i=1}^n\ln x_i
-\theta\sum_{i=1}^n\frac{1}{x_i}.
$$
求导得
$$
\frac{d}{d\theta}\ln L(\theta)=\frac{2n}{\theta}-\sum_{i=1}^n\frac{1}{x_i}.
$$
令其为 $0$，得
$$
\hat\theta=\frac{2n}{\sum_{i=1}^n\frac{1}{X_i}}.
$$
且二阶导数 $-\frac{2n}{\theta^2}<0$，故该值为最大似然估计量。
