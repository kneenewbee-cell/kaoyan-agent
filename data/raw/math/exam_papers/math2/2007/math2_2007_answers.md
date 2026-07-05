# Math 2 2007 Answers

资料类型：考研数学二答案解析
年份：2007
科目：数学二
整理状态：答案与解析依据答案册清洗整理，并与题面同步。

## 答案速查

| 题号 | 题型 | 答案 |
|---|---|---|
| 1 | 选择题 | B |
| 2 | 选择题 | A |
| 3 | 选择题 | C |
| 4 | 选择题 | D |
| 5 | 选择题 | D |
| 6 | 选择题 | D |
| 7 | 选择题 | C |
| 8 | 选择题 | B |
| 9 | 选择题 | A |
| 10 | 选择题 | B |
| 11 | 填空题 | $-\dfrac16$ |
| 12 | 填空题 | $1+\sqrt2$ |
| 13 | 填空题 | $\dfrac{(-1)^n2^n n!}{3^{n+1}}$ |
| 14 | 填空题 | $y=C_1e^x+C_2e^{3x}-2e^{2x}$ |
| 15 | 填空题 | $2\left(-\dfrac{y}{x}f_1'+\dfrac{x}{y}f_2'\right)$ |
| 16 | 填空题 | $1$ |
| 17 | 解答题 | $f(x)=\ln(\sin x+\cos x)$ |
| 18 | 解答题 | （I）$V(a)=\pi\left(\dfrac{a}{\ln a}\right)^2$；（II）$a=e$ 时最小，$V_{\min}=\pi e^2$ |
| 19 | 解答题 | $y=\dfrac23x^{3/2}+\dfrac13$ |
| 20 | 解答题 | $\left.\dfrac{dz}{dx}\right\rvert_{x=0}=0,\quad \left.\dfrac{d^2z}{dx^2}\right\rvert_{x=0}=1$ |
| 21 | 证明题 | 见解析 |
| 22 | 解答题 | $\dfrac13+2\sqrt2\ln(3+2\sqrt2)$ |
| 23 | 解答题 | $a=1$ 或 $a=2$；当 $a=1$ 时公共解为 $k(1,0,-1)^T$，当 $a=2$ 时公共解为 $(0,1,-1)^T$ |
| 24 | 解答题 | （I）$B$ 的特征值为 $-2,1,1$；（II）$B=\begin{pmatrix}0&1&-1\\1&0&1\\-1&1&0\end{pmatrix}$ |

## 详细解析

### 第 1 题

- 答案：B

分别考察各选项：
$$
1-e^{\sqrt{x}}\sim-\sqrt{x},\qquad
\sqrt{1+\sqrt{x}}-1\sim \frac12\sqrt{x},\qquad
1-\cos\sqrt{x}\sim \frac{x}{2}.
$$
而
$$
\ln\frac{1+x}{1-\sqrt{x}}
=\ln\left(1+\frac{x+\sqrt{x}}{1-\sqrt{x}}\right)
\sim \frac{x+\sqrt{x}}{1-\sqrt{x}}\sim \sqrt{x}.
$$
所以选 B。

### 第 2 题

- 答案：A

先找出可能的间断点：$x=0,1,\pm \dfrac{\pi}{2}$。考察 $x=0$ 处左右极限：
$$
\lim_{x\to0^+}f(x)=1,\qquad \lim_{x\to0^-}f(x)=-1.
$$
左右极限都存在但不相等，因此 $x=0$ 是第一类间断点。
其余几个点对应极限发散，为第二类间断点。

### 第 3 题

- 答案：C

由图形知 $f$ 为奇函数，因此
$$
F(-x)=\int_0^{-x}f(t)\,dt=\int_0^x f(t)\,dt=F(x),
$$
所以 $F$ 为偶函数。
又
$$
F(2)=\frac{\pi}{2},
$$
因为 $[0,2]$ 上是半径 $1$ 的上半圆面积。
而 $[2,3]$ 上是半径 $\dfrac12$ 的下半圆，故
$$
\int_2^3 f(t)\,dt=-\frac{\pi}{8}.
$$
从而
$$
F(3)=F(2)-\frac{\pi}{8}=\frac{3\pi}{8}=\frac34F(2).
$$
再由偶性得
$$
F(-3)=F(3)=\frac34F(2).
$$
所以选 C。

### 第 4 题

- 答案：D

(A) 中由连续性和
$$
\lim_{x\to0}\frac{f(x)}{x}
$$
存在可得 $f(0)=0$。于是 (C) 中
$$
f'(0)=\lim_{x\to0}\frac{f(x)-f(0)}{x}=\lim_{x\to0}\frac{f(x)}{x}
$$
也成立。
对 (B)，若
$$
\lim_{x\to0}\frac{f(x)+f(-x)}{x}
$$
存在，则由连续性有 $f(x)+f(-x)\to2f(0)$，故必有 $f(0)=0$。
(D) 不成立，例如 $f(x)=|x|$，则
$$
\frac{f(x)-f(-x)}{x}=0
$$
极限存在，但 $f'(0)$ 不存在。

### 第 5 题

- 答案：D

当 $x\to0$ 时，$\dfrac1x\to\infty$，故 $x=0$ 是铅直渐近线。
当 $x\to-\infty$ 时，
$$
\frac1x\to0,\qquad \ln(1+e^x)\to0,
$$
故 $y=0$ 是水平渐近线。
当 $x\to+\infty$ 时，
$$
\ln(1+e^x)=x+\ln(1+e^{-x}),
$$
因而
$$
y-x=\frac1x+\ln(1+e^{-x})\to0,
$$
所以 $y=x$ 是斜渐近线。
共 3 条。

### 第 6 题

- 答案：D

由拉格朗日中值定理，
$$
u_{n+1}-u_n=f(n+1)-f(n)=f'(\xi_n),\qquad n<\xi_n<n+1.
$$
因 $f''(x)>0$，故 $f'(x)$ 严格递增，于是 $f'(\xi_n)$ 严格递增。
若 $u_1<u_2$，则 $f'(\xi_1)=u_2-u_1>0$，从而对所有 $n$ 都有
$$
u_{n+1}-u_n=f'(\xi_n)\ge f'(\xi_1)>0.
$$
因此 $\{u_n\}$ 至少线性增长，必发散。故选 D。

### 第 7 题

- 答案：C

选项 (C) 给出
$$
f(x,y)-f(0,0)=o\!\left(\sqrt{x^2+y^2}\right),
$$
即
$$
f(x,y)-f(0,0)=0\cdot x+0\cdot y+o(\rho),\qquad \rho=\sqrt{x^2+y^2},
$$
这正是可微定义中的一种形式，因此是充分条件。
其余几项都不能单独保证全微分存在。

### 第 8 题

- 答案：B

原积分区域为
$$
\frac{\pi}{2}\le x\le\pi,\qquad \sin x\le y\le1.
$$
固定 $y\in[0,1]$，由 $\sin x\le y$ 且 $x\in[\pi/2,\pi]$ 得
$$
x\in[\pi-\arcsin y,\ \pi].
$$
因而交换次序后为
$$
\int_0^1dy\int_{\pi-\arcsin y}^{\pi}f(x,y)\,dx.
$$
故选 B。

### 第 9 题

- 答案：A

对 (A) 中三向量直接相加：
$$
(\alpha_1-\alpha_2)+(\alpha_2-\alpha_3)+(\alpha_3-\alpha_1)=0.
$$
且系数不全为零，因此该向量组线性相关。
其余三项都可写成原线性无关向量组右乘可逆矩阵的结果，故仍线性无关。

### 第 10 题

- 答案：B

由计算可得 $A$ 的特征值为 $3,3,0$，而 $B$ 的特征值为 $1,1,0$。
因相似矩阵特征值必须完全相同，所以二者不相似。
另一方面，$A,B$ 都是实对称矩阵，且正惯性指数都为 $2$、负惯性指数都为 $0$，
因此按实对称矩阵合同判定准则，二者合同。
故选 B。

### 第 11 题

- 答案：$-\dfrac16$

展开
$$
\arctan x=x-\frac{x^3}{3}+o(x^3),\qquad \sin x=x-\frac{x^3}{6}+o(x^3).
$$
相减得
$$
\arctan x-\sin x=-\frac{x^3}{6}+o(x^3),
$$
故极限为
$$
-\frac16.
$$

### 第 12 题

- 答案：$1+\sqrt2$

有
$$
\frac{dy}{dx}=\frac{dy/dt}{dx/dt}
=\frac{\cos t}{-\sin t-2\sin t\cos t}.
$$
当 $t=\dfrac{\pi}{4}$ 时，
$$
\frac{dy}{dx}=-\frac{1}{1+\sqrt2}.
$$
法线斜率是其负倒数，所以为
$$
1+\sqrt2.
$$

### 第 13 题

- 答案：$\dfrac{(-1)^n2^n n!}{3^{n+1}}$

写成
$$
y=(2x+3)^{-1}.
$$
连续求导可得一般式
$$
y^{(n)}(x)=(-1)^n2^n n!(2x+3)^{-n-1}.
$$
令 $x=0$，即得
$$
y^{(n)}(0)=\frac{(-1)^n2^n n!}{3^{n+1}}.
$$

### 第 14 题

- 答案：$y=C_1e^x+C_2e^{3x}-2e^{2x}$

先解齐次方程
$$
r^2-4r+3=0,
$$
得特征根 $r=1,3$，所以齐次解为
$$
y_h=C_1e^x+C_2e^{3x}.
$$
对非齐次项设特解 $y^*=Ae^{2x}$，代入得
$$
(4A-8A+3A)e^{2x}=2e^{2x},
$$
故 $A=-2$。所以通解为
$$
y=C_1e^x+C_2e^{3x}-2e^{2x}.
$$

### 第 15 题

- 答案：$2\left(-\dfrac{y}{x}f_1'+\dfrac{x}{y}f_2'\right)$

设
$$
u=\frac{y}{x},\qquad v=\frac{x}{y},\qquad z=f(u,v).
$$
由链式法则，
$$
z_x=f_1'u_x+f_2'v_x=f_1'\!\left(-\frac{y}{x^2}\right)+f_2'\frac1y,
$$
$$
z_y=f_1'u_y+f_2'v_y=f_1'\frac1x+f_2'\!\left(-\frac{x}{y^2}\right).
$$
因而
$$
xz_x-yz_y
=2\left(-\frac{y}{x}f_1'+\frac{x}{y}f_2'\right).
$$

### 第 16 题

- 答案：$1$

直接计算可得
$$
A^3=\begin{pmatrix}
0&0&0&1\\
0&0&0&0\\
0&0&0&0\\
0&0&0&0
\end{pmatrix}.
$$
其非零行只有一行，因此
$$
r(A^3)=1.
$$

### 第 17 题

- 答案：$f(x)=\ln(\sin x+\cos x)$

对等式两边关于 $x$ 求导，左边由变上限积分与反函数关系得
$$
f^{-1}(f(x))f'(x)=x f'(x).
$$
右边导数为
$$
\frac{\cos x-\sin x}{\sin x+\cos x}.
$$
因而
$$
x f'(x)=\frac{\cos x-\sin x}{\sin x+\cos x}x,
$$
对 $x\ne0$ 可化为
$$
f'(x)=\frac{\cos x-\sin x}{\sin x+\cos x}.
$$
积分得
$$
f(x)=\ln(\sin x+\cos x)+C.
$$
令 $x=0$ 代回原式，两边都为 $0$，可得 $f(0)=0$，故 $C=0$。
所以
$$
f(x)=\ln(\sin x+\cos x).
$$

### 第 18 题

- 答案：（I）$V(a)=\pi\left(\dfrac{a}{\ln a}\right)^2$；（II）$a=e$ 时最小，$V_{\min}=\pi e^2$

由旋转体体积公式，
$$
V(a)=\pi\int_0^{+\infty}y^2\,dx
=\pi\int_0^{+\infty}x\,a^{-x/a}\,dx.
$$
利用分部积分或指数积分公式可得
$$
V(a)=\pi\left(\frac{a}{\ln a}\right)^2.
$$
对其求导：
$$
V'(a)=2\pi\frac{a(\ln a-1)}{(\ln a)^3}.
$$
因此在 $a=e$ 时取极小值，且
$$
V_{\min}=V(e)=\pi e^2.
$$

### 第 19 题

- 答案：$y=\dfrac23x^{3/2}+\dfrac13$

令 $p=y'$，则 $y''=\dfrac{dp}{dx}$，原方程化为
$$
p'(x+p^2)=p.
$$
将 $x$ 看作 $p$ 的函数，有
$$
\frac{dx}{dp}-\frac1p x=p.
$$
这是关于 $x(p)$ 的一阶线性方程，解得
$$
x=p^2+Cp.
$$
由初值 $x=1,p=1$ 得 $C=0$，故
$$
p=\sqrt{x}.
$$
即
$$
y'=\sqrt{x}.
$$
再积分并用 $y(1)=1$，得
$$
y=\frac23x^{3/2}+\frac13.
$$

### 第 20 题

- 答案：$\left.\dfrac{dz}{dx}\right\rvert_{x=0}=0,\quad \left.\dfrac{d^2z}{dx^2}\right\rvert_{x=0}=1$

先由方程在 $x=0$ 时得
$$
y(0)=1.
$$
对
$$
y-xe^{y-1}=1
$$
求导，可得
$$
(2-y)y'=e^{y-1}.
$$
代入 $x=0,y=1$ 得
$$
y'(0)=1.
$$
再求一次导数，可得 $y''(0)=2$。
设
$$
u=\ln y-\sin x,\qquad z=f(u).
$$
则
$$
\frac{dz}{dx}=f'(u)\left(\frac{y'}{y}-\cos x\right).
$$
在 $x=0$ 处，由 $u(0)=0,\ f'(0)=1,\ y(0)=1,\ y'(0)=1$ 得
$$
\left.\frac{dz}{dx}\right|_{x=0}=1\cdot(1-1)=0.
$$
再求导：
$$
\frac{d^2z}{dx^2}=f''(u)(u')^2+f'(u)u''.
$$
因 $u'(0)=0$，故第一项为 $0$；而
$$
u''(0)=\left(\frac{y''}{y}-\frac{(y')^2}{y^2}+\sin x\right)_{x=0}=2-1=1.
$$
所以
$$
\left.\frac{d^2z}{dx^2}\right|_{x=0}=f'(0)\cdot1=1.
$$

### 第 21 题

- 答案：见解析

令
$$
\varphi(x)=f(x)-g(x).
$$
由题设，$f,g$ 在 $(a,b)$ 内分别取得相等的最大值，所以存在某个 $\eta\in(a,b)$ 使得
$$
\varphi(\eta)=0.
$$
又因
$$
\varphi(a)=f(a)-g(a)=0,\qquad \varphi(b)=f(b)-g(b)=0,
$$
故 $\varphi$ 在区间 $[a,\eta]$ 与 $[\eta,b]$ 上分别满足罗尔定理，于是存在
$$
\xi_1\in(a,\eta),\qquad \xi_2\in(\eta,b)
$$
使得
$$
\varphi'(\xi_1)=\varphi'(\xi_2)=0.
$$
再对 $\varphi'$ 在 $[\xi_1,\xi_2]$ 上应用罗尔定理，存在 $\xi\in(\xi_1,\xi_2)\subset(a,b)$ 使
$$
\varphi''(\xi)=0.
$$
即
$$
f''(\xi)=g''(\xi).
$$

### 第 22 题

- 答案：$\dfrac13+2\sqrt2\ln(3+2\sqrt2)$

将区域分成
$$
D_1=\{|x|+|y|\le1\},\qquad D_2=\{1<|x|+|y|\le2\}.
$$
则
$$
\iint_D f(x,y)\,d\sigma=\iint_{D_1}x^2\,d\sigma+\iint_{D_2}\frac{1}{\sqrt{x^2+y^2}}\,d\sigma.
$$
第一部分利用关于坐标轴的对称性：
$$
\iint_{D_1}x^2\,d\sigma
=4\int_0^1dx\int_0^{1-x}x^2\,dy
=4\int_0^1x^2(1-x)\,dx=\frac13.
$$
第二部分在第一象限用极坐标，边界 $x+y=1,2$ 分别对应
$$
r=\frac{1}{\cos\theta+\sin\theta},\qquad
r=\frac{2}{\cos\theta+\sin\theta},\qquad 0\le\theta\le\frac{\pi}{2}.
$$
因而
$$
\iint_{D_2}\frac{1}{\sqrt{x^2+y^2}}\,d\sigma
=4\int_0^{\pi/2}\int_{1/(\cos\theta+\sin\theta)}^{2/(\cos\theta+\sin\theta)}dr\,d\theta
=2\sqrt2\ln(3+2\sqrt2).
$$
所以结果为
$$
\frac13+2\sqrt2\ln(3+2\sqrt2).
$$

### 第 23 题

- 答案：$a=1$ 或 $a=2$；当 $a=1$ 时公共解为 $k(1,0,-1)^T$，当 $a=2$ 时公共解为 $(0,1,-1)^T$

把附加方程并入原线性方程组，组成增广矩阵并作消元，可得可解条件
$$
(a-1)(a-2)=0.
$$
因而
$$
a=1\quad\text{或}\quad a=2.
$$
当 $a=1$ 时，方程组化为
$$
\begin{cases}
x_1+x_2+x_3=0,\\
x_2=0,
\end{cases}
$$
所有公共解为
$$
k(1,0,-1)^T.
$$
当 $a=2$ 时，联立后解得
$$
x_2=1,\qquad x_3=-1,\qquad x_1=0,
$$
因而公共解为
$$
(0,1,-1)^T.
$$

### 第 24 题

- 答案：（I）$B$ 的特征值为 $-2,1,1$；（II）$B=\begin{pmatrix}0&1&-1\\1&0&1\\-1&1&0\end{pmatrix}$

设
$$
p(\lambda)=\lambda^5-4\lambda^3+1.
$$
因为 $\alpha_1$ 是 $A$ 的属于特征值 $1$ 的特征向量，所以
$$
B\alpha_1=p(A)\alpha_1=p(1)\alpha_1=-2\alpha_1,
$$
故 $\alpha_1$ 是 $B$ 的特征向量，属于特征值 $-2$。
又由矩阵多项式的特征值映射性质，
$$
p(1)=-2,\qquad p(2)=1,\qquad p(-2)=1.
$$
所以 $B$ 的特征值为
$$
-2,1,1.
$$
由于 $B$ 为实对称矩阵，不同特征值对应特征向量正交。设属于特征值 $1$ 的向量为 $(x_1,x_2,x_3)^T$，
则需满足与 $\alpha_1=(1,-1,1)^T$ 正交，即
$$
x_1-x_2+x_3=0.
$$
可取一组基
$$
\alpha_2=(-1,0,1)^T,\qquad \alpha_3=(1,1,0)^T.
$$
令 $P=(\alpha_1,\alpha_2,\alpha_3)$，则
$$
P^{-1}BP=\operatorname{diag}(-2,1,1).
$$
由此计算得
$$
B=\begin{pmatrix}
0&1&-1\\
1&0&1\\
-1&1&0
\end{pmatrix}.
$$
