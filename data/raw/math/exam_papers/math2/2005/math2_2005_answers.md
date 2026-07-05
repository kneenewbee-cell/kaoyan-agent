# Math 2 2005 Answers

资料类型：考研数学二答案解析
年份：2005
科目：数学二
范围：试卷 III
校对状态：已按答案页与题面同步清洗整理。

## 答案速查

| 题号 | 题型 | 答案 |
|---|---|---|
| 1 | 填空题 | $-\pi\,dx$ |
| 2 | 填空题 | $y=x+\dfrac{3}{2}$ |
| 3 | 填空题 | $\dfrac{\pi}{4}$ |
| 4 | 填空题 | $y=\dfrac13x\ln x-\dfrac19x$ |
| 5 | 填空题 | $\dfrac34$ |
| 6 | 填空题 | $2$ |
| 7 | 选择题 | C |
| 8 | 选择题 | A |
| 9 | 选择题 | A |
| 10 | 选择题 | D |
| 11 | 选择题 | B |
| 12 | 选择题 | D |
| 13 | 选择题 | B |
| 14 | 选择题 | C |
| 15 | 解答题 | $\dfrac12$ |
| 16 | 解答题 | $x=\varphi(y)=\ln y-\dfrac12+\dfrac{1}{2y}$ |
| 17 | 解答题 | $20$ |
| 18 | 解答题 | $y=2x+\sqrt{1-x^2}\quad(-1<x<1)$ |
| 19 | 证明题 | 见解析 |
| 20 | 解答题 | 最大值为 $3$，最小值为 $-2$ |
| 21 | 解答题 | $\dfrac{\pi}{4}-\dfrac13$ |
| 22 | 解答题 | $a=1$ |
| 23 | 解答题 | 当 $k\ne9$ 时，$x=s(1,2,3)^\mathrm{T}+t(3,6,k)^\mathrm{T}$；当 $k=9$ 时，若 $r(A)=2$，则 $x=s(1,2,3)^\mathrm{T}$；若 $r(A)=1$，则通解为 $x=s\left(-\dfrac ba,1,0\right)^\mathrm{T}+t\left(-\dfrac ca,0,1\right)^\mathrm{T}$（$a\ne0$）。 |

## 详细解析

### 第 1 题

- 答案：$-\pi\,dx$

先求导数：
$$
y'=(1+\sin x)^x\left[\ln(1+\sin x)+\frac{x\cos x}{1+\sin x}\right].
$$
当 $x=\pi$ 时，$\sin\pi=0,\cos\pi=-1$，故
$$
y'(\pi)=\ln 1+\pi\cdot(-1)=-\pi.
$$
因此
$$
dy\vert_{x=\pi}=y'(\pi)\,dx=-\pi\,dx.
$$

### 第 2 题

- 答案：$y=x+\dfrac{3}{2}$

利用斜渐近线公式 $y=ax+b$，其中
$$
a=\lim_{x\to+\infty}\frac{f(x)}{x},\qquad b=\lim_{x\to+\infty}[f(x)-ax].
$$
对 $f(x)=\dfrac{(1+x)^{3/2}}{\sqrt{x}}$，有
$$
a=\lim_{x\to+\infty}\frac{(1+x)^{3/2}}{x\sqrt{x}}=1.
$$
再算
$$
b=\lim_{x\to+\infty}\left(\frac{(1+x)^{3/2}}{\sqrt{x}}-x\right)=\frac{3}{2}.
$$
故斜渐近线为
$$
y=x+\frac{3}{2}.
$$

### 第 3 题

- 答案：$\dfrac{\pi}{4}$

令 $x=\sin t\ (0<t<\tfrac\pi2)$，则 $dx=\cos t\,dt$，原积分化为
$$
\int_0^{\pi/2}\frac{\sin t}{2-\sin^2 t}\,dt.
$$
再令 $u=\cos t$，则 $du=-\sin t\,dt$，得
$$
\int_0^{\pi/2}\frac{\sin t}{2-\sin^2 t}\,dt=\int_1^0\frac{-du}{1+u^2}=\int_0^1\frac{du}{1+u^2}=\arctan 1=\frac{\pi}{4}.
$$

### 第 4 题

- 答案：$y=\dfrac13x\ln x-\dfrac19x$

将方程写成
$$
y'+\frac{2}{x}y=\ln x\qquad (x>0).
$$
积分因子为 $\mu(x)=x^2$，故
$$
(x^2y)'=x^2\ln x.
$$
积分得
$$
x^2y=\int x^2\ln x\,dx=\frac{x^3}{3}\ln x-\frac{x^3}{9}+C,
$$
即
$$
y=\frac13x\ln x-\frac19x+\frac{C}{x^2}.
$$
由 $y(1)=-\dfrac19$ 得 $C=0$，所以
$$
y=\frac13x\ln x-\frac19x.
$$

### 第 5 题

- 答案：$\dfrac34$

由题意有
$$
\lim_{x\to0}\frac{\beta(x)}{\alpha(x)}=1.
$$
对 $\beta(x)$ 有
$$
\beta(x)=\frac{x\arcsin x+1-\cos x}{\sqrt{1+x\arcsin x}+\sqrt{\cos x}}.
$$
又当 $x\to0$ 时，
$$
\arcsin x\sim x,\qquad 1-\cos x\sim \frac{x^2}{2},
$$
故
$$
\beta(x)\sim \frac{x^2+\frac{x^2}{2}}{2}=\frac34x^2.
$$
于是 $kx^2\sim\beta(x)\sim\dfrac34x^2$，从而
$$
k=\frac34.
$$

### 第 6 题

- 答案：$2$

可写成
$$
B=A\begin{pmatrix}1&1&1\\1&2&3\\1&4&9\end{pmatrix}.
$$
故
$$
|B|=|A|\cdot\begin{vmatrix}1&1&1\\1&2&3\\1&4&9\end{vmatrix}.
$$
由 $|A|=1$，且范德蒙德行列式
$$
\begin{vmatrix}1&1&1\\1&2&3\\1&4&9\end{vmatrix}=(2-1)(3-1)(3-2)=2,
$$
所以
$$
|B|=2.
$$

### 第 7 题

- 答案：C

分段求极限：
$$
f(x)=\begin{cases}1,&|x|<1,\\|x|^3,&|x|\ge1.\end{cases}
$$
因此在 $x=\pm1$ 处，左右导数不相等，函数不可导；其余各点都可导。故恰有两个不可导点，选 C。

### 第 8 题

- 答案：A

若 $F$ 是偶函数，则对两边求导得
$$
F'(-x)(-1)=F'(x),
$$
即
$$
f(-x)=-f(x),
$$
所以 $f$ 为奇函数。反之若 $f$ 为奇函数，取
$$
F(x)=\int_0^x f(t)\,dt+C,
$$
则由换元可得 $F(-x)=F(x)$，故 $F$ 为偶函数。A 必然成立。

### 第 9 题

- 答案：A

由 $x=3$ 得 $t^2+2t=3$，解得 $t=1$ 或 $-3$，而 $t>-1$，故取 $t=1$。此时点为 $(3,\ln2)$。
$$
\frac{dy}{dx}=\frac{dy/dt}{dx/dt}=\frac{1/(1+t)}{2t+2}.
$$
在 $t=1$ 处，切线斜率为 $\dfrac18$，故法线斜率为 $-8$。法线方程为
$$
y-\ln2=-8(x-3).
$$
令 $y=0$ 得
$$
x=3+\frac18\ln2.
$$
故选 A。

### 第 10 题

- 答案：D

设
$$
I=\iint_D\frac{a\sqrt{f(x)}+b\sqrt{f(y)}}{\sqrt{f(x)}+\sqrt{f(y)}}\,d\sigma.
$$
交换 $x,y$ 后，由区域关于直线 $y=x$ 对称，得
$$
I=\iint_D\frac{a\sqrt{f(y)}+b\sqrt{f(x)}}{\sqrt{f(x)}+\sqrt{f(y)}}\,d\sigma.
$$
两式相加：
$$
2I=(a+b)\iint_D1\,d\sigma.
$$
而 $D$ 是半径 2 的四分之一圆盘，面积为 $\pi$，所以
$$
I=\frac{a+b}{2}\pi.
$$
故选 D。

### 第 11 题

- 答案：B

直接求偏导：
$$
u_x=\varphi'(x+y)+\varphi'(x-y)+\psi(x+y)-\psi(x-y),
$$
$$
u_y=\varphi'(x+y)-\varphi'(x-y)+\psi(x+y)+\psi(x-y).
$$
再求二阶偏导，得
$$
u_{xx}=\varphi''(x+y)+\varphi''(x-y)+\psi'(x+y)-\psi'(x-y),
$$
$$
u_{yy}=\varphi''(x+y)+\varphi''(x-y)+\psi'(x+y)-\psi'(x-y).
$$
故必有 $u_{xx}=u_{yy}$，选 B。

### 第 12 题

- 答案：D

当 $x\to0$ 时，指数 $\dfrac{x}{x-1}\to0$，并且
$$
e^{x/(x-1)}-1\sim \frac{x}{x-1}\sim -x,
$$
故 $f(x)\sim-\dfrac1x$，极限发散，所以 $x=0$ 是第二类间断点。

当 $x\to1^-$ 时，$\dfrac{x}{x-1}\to-\infty$，故 $f(x)\to-1$；当 $x\to1^+$ 时，$\dfrac{x}{x-1}\to+\infty$，故 $f(x)\to0$。左右极限都存在但不相等，所以 $x=1$ 是第一类间断点。故选 D。

### 第 13 题

- 答案：B

因为
$$
A(\alpha_1+\alpha_2)=\lambda_1\alpha_1+\lambda_2\alpha_2.
$$
又 $\lambda_1\ne\lambda_2$，故 $\alpha_1,\alpha_2$ 线性无关。于是 $\alpha_1$ 与 $A(\alpha_1+\alpha_2)$ 线性无关，当且仅当后者中 $\alpha_2$ 的系数不为零，即
$$
\lambda_2\ne0.
$$
故选 B。

### 第 14 题

- 答案：C

设 $E_{12}$ 为交换第 1、2 行的初等矩阵，则 $B=E_{12}A$。于是
$$
B^*=|B|B^{-1}=(-|A|)A^{-1}E_{12}=-A^*E_{12}.
$$
右乘 $E_{12}$ 表示交换列，因此 $B^*$ 等于把 $A^*$ 的第 1、2 列交换后再乘以 $-1$。故选 C。

### 第 15 题

- 答案：$\dfrac12$

对分母中的积分作变量替换 $u=x-t$，得
$$
\int_0^xf(x-t)\,dt=\int_0^xf(u)\,du.
$$
于是原式为
$$
\lim_{x\to0}\frac{\int_0^x(x-t)f(t)\,dt}{x\int_0^xf(t)\,dt}.
$$
分子分母同趋于 0，可用洛必达法则：
$$
\lim_{x\to0}\frac{\int_0^xf(t)\,dt}{\int_0^xf(t)\,dt+xf(x)}.
$$
再将上下同除以 $x$，并利用连续性
$$
\lim_{x\to0}\frac{\frac1x\int_0^xf(t)\,dt}{\frac1x\int_0^xf(t)\,dt+f(x)}=\frac{f(0)}{f(0)+f(0)}=\frac12.
$$

### 第 16 题

- 答案：$x=\varphi(y)=\ln y-\dfrac12+\dfrac{1}{2y}$

由面积公式，
$$
S_1(x)=\int_0^x\left[e^t-\frac12(1+e^t)\right]dt=\frac12(e^x-x-1).
$$
又由图形关系
$$
S_2(y)=\int_1^y\bigl(\ln t-\varphi(t)\bigr)dt.
$$
题设给出 $S_1(x)=S_2(y)$，且点 $M(x,y)$ 在 $C_2$ 上，所以 $y=e^x$，即 $x=\ln y$。代入得
$$
\int_1^y\bigl(\ln t-\varphi(t)\bigr)dt=\frac12(y-\ln y-1).
$$
两边对 $y$ 求导：
$$
\ln y-\varphi(y)=\frac12\left(1-\frac1y\right).
$$
故
$$
\varphi(y)=\ln y-\frac12+\frac{1}{2y}.
$$

### 第 17 题

- 答案：$20$

由几何条件，直线 $l_1$ 过 $(0,0)$ 与 $(2,4)$，故其斜率为 2，于是
$$
f'(0)=2.
$$
同理直线 $l_2$ 过 $(3,2)$ 与 $(2,4)$，斜率为 $-2$，故
$$
f'(3)=-2.
$$
又 $(3,2)$ 是拐点，所以
$$
f''(3)=0.
$$
对积分作分部积分：
$$
\int_0^3(x^2+x)f'''(x)dx=\bigl[(x^2+x)f''(x)\bigr]_0^3-\int_0^3(2x+1)f''(x)dx.
$$
再分部积分一次：
$$
\int_0^3(2x+1)f''(x)dx=\bigl[(2x+1)f'(x)\bigr]_0^3-2\int_0^3f'(x)dx.
$$
代入已知条件与 $f(0)=0,f(3)=2$，得
$$
\int_0^3(x^2+x)f'''(x)dx=0-\bigl[7f'(3)-f'(0)-2(f(3)-f(0))\bigr]=20.
$$

### 第 18 题

- 答案：$y=2x+\sqrt{1-x^2}\quad(-1<x<1)$

令 $x=\cos t$，则 $dx=-\sin t\,dt$。把 $y$ 看作 $t$ 的函数，利用链式法则可化原方程为
$$
\frac{d^2y}{dt^2}+y=0.
$$
其通解为
$$
y=C_1\cos t+C_2\sin t.
$$
再换回 $x$：因 $0<t<\pi$，故 $\sin t=\sqrt{1-x^2}$，从而
$$
y=C_1x+C_2\sqrt{1-x^2}.
$$
由 $y(0)=1$ 得 $C_2=1$。又
$$
y'=C_1-\frac{C_2x}{\sqrt{1-x^2}},
$$
代入 $y'(0)=2$ 得 $C_1=2$。故所求特解为
$$
y=2x+\sqrt{1-x^2},\qquad -1<x<1.
$$

### 第 19 题

- 答案：见解析

（I）令
$$
F(x)=f(x)+x-1.
$$
则 $F$ 在 $[0,1]$ 上连续，且
$$
F(0)=-1<0,\qquad F(1)=1>0.
$$
由介值定理，存在 $\xi\in(0,1)$，使得 $F(\xi)=0$，即
$$
f(\xi)=1-\xi.
$$

（II）在区间 $[0,\xi]$ 与 $[\xi,1]$ 上分别应用拉格朗日中值定理，存在
$$
\eta\in(0,\xi),\qquad \zeta\in(\xi,1)
$$
使得
$$
f'(\eta)=\frac{f(\xi)-f(0)}{\xi-0}=\frac{1-\xi}{\xi},
$$
$$
f'(\zeta)=\frac{f(1)-f(\xi)}{1-\xi}=\frac{\xi}{1-\xi}.
$$
因此
$$
f'(\eta)f'(\zeta)=1.
$$

### 第 20 题

- 答案：最大值为 $3$，最小值为 $-2$

由全微分得
$$
f_x=2x,\qquad f_y=-2y.
$$
积分可得
$$
f(x,y)=x^2-y^2+C.
$$
由 $f(1,1)=2$ 得 $C=2$，故
$$
f(x,y)=x^2-y^2+2.
$$
内部驻点满足 $f_x=f_y=0$，即 $(0,0)$，对应函数值为 2。

在边界 $x^2+\dfrac{y^2}{4}=1$ 上，令 $y^2=4(1-x^2)$，则
$$
f(x,y)=x^2-4(1-x^2)+2=5x^2-2,\qquad -1\le x\le1.
$$
于是最大值在 $x=\pm1,y=0$ 处取得，为
$$
f_{\max}=3;
$$
最小值在 $x=0,y=\pm2$ 处取得，为
$$
f_{\min}=-2.
$$

### 第 21 题

- 答案：$\dfrac{\pi}{4}-\dfrac13$

将区域 $D$ 按圆弧 $x^2+y^2=1$ 分成两部分：
$$
D_1=\{(x,y)\in D\mid x^2+y^2\le1\},\qquad D_2=D\setminus D_1.
$$
于是
$$
\iint_D|x^2+y^2-1|d\sigma=\iint_{D_1}(1-x^2-y^2)d\sigma+\iint_{D_2}(x^2+y^2-1)d\sigma.
$$
第一部分用极坐标：
$$
\iint_{D_1}(1-r^2)d\sigma=\int_0^{\pi/2}\int_0^1(1-r^2)r\,dr\,d\theta=\frac{\pi}{8}.
$$
第二部分可用补区域计算，整理后得
$$
\iint_{D_2}(x^2+y^2-1)d\sigma=\frac{\pi}{8}-\frac13.
$$
故原积分为
$$
\frac{\pi}{8}+\left(\frac{\pi}{8}-\frac13\right)=\frac{\pi}{4}-\frac13.
$$

### 第 22 题

- 答案：$a=1$

设
$$
A=(\alpha_1,\alpha_2,\alpha_3),\qquad B=(\beta_1,\beta_2,\beta_3).
$$
由“$\beta$ 不能由 $\alpha$ 线性表示”可知 $r(A)<3$，于是
$$
|A|=\begin{vmatrix}1&1&a\\1&a&1\\a&1&1\end{vmatrix}=-(a-1)^2(a+2)=0.
$$
故只可能有
$$
a=1\quad\text{或}\quad a=-2.
$$

当 $a=1$ 时，
$$
\alpha_1=\alpha_2=\alpha_3=(1,1,1)^\mathrm{T},
$$
显然 $\alpha_1,\alpha_2,\alpha_3$ 可由 $\beta_1,\beta_2,\beta_3$ 表出；另一方面 $\beta_2=(-2,1,4)^\mathrm{T}$ 不能由 $(1,1,1)^\mathrm{T}$ 的倍数表示，所以 $\beta$ 不能由 $\alpha$ 表示，满足题意。

当 $a=-2$ 时，检验可知 $\alpha$ 也不能由 $\beta$ 线性表示，与题意矛盾。

因此唯一可取
$$
a=1.
$$

### 第 23 题

- 答案：当 $k\ne9$ 时，$x=s(1,2,3)^\mathrm{T}+t(3,6,k)^\mathrm{T}$；当 $k=9$ 时，若 $r(A)=2$，则 $x=s(1,2,3)^\mathrm{T}$；若 $r(A)=1$，则通解为 $x=s\left(-\dfrac ba,1,0\right)^\mathrm{T}+t\left(-\dfrac ca,0,1\right)^\mathrm{T}$（$a\ne0$）。

由 $AB=O$ 知，矩阵 $B$ 的每一列都是齐次方程组 $Ax=0$ 的解。

当 $k\ne9$ 时，
$$
\beta_1=(1,2,3)^\mathrm{T},\quad \beta_2=(2,4,6)^\mathrm{T}=2\beta_1,\quad \beta_3=(3,6,k)^\mathrm{T}
$$
中，$\beta_1$ 与 $\beta_3$ 线性无关，因此 $Ax=0$ 至少有两个线性无关解。又因 $A$ 的第一行不全为零，故 $r(A)\ge1$；而解空间维数为 $3-r(A)$，只能等于 2，所以 $r(A)=1$。于是 $\beta_1,\beta_3$ 可作为基础解系，通解为
$$
x=s\begin{pmatrix}1\\2\\3\end{pmatrix}+t\begin{pmatrix}3\\6\\k\end{pmatrix},\qquad s,t\in\mathbb{R}.
$$

当 $k=9$ 时，三列向量都与 $(1,2,3)^\mathrm{T}$ 成比例。若 $r(A)=2$，则解空间维数为 1，基础解系可取 $(1,2,3)^\mathrm{T}$，通解为
$$
x=s\begin{pmatrix}1\\2\\3\end{pmatrix}.
$$
若 $r(A)=1$，则 $A$ 的三行成比例，而第一行 $(a,b,c)$ 不全为零，可设 $a\ne0$，则 $Ax=0$ 与一元方程
$$
ax_1+bx_2+cx_3=0
$$
同解。取 $x_2,x_3$ 为自由变量，可得通解
$$
x=s\begin{pmatrix}-\dfrac ba\\1\\0\end{pmatrix}+t\begin{pmatrix}-\dfrac ca\\0\\1\end{pmatrix},\qquad s,t\in\mathbb{R}.
$$
