# 2021 年数学二答案解析

资料类型：考研数学二答案解析
年份：2021
科目：数学二
整理状态：以答案解析页图为主，并结合题面内容做人工校对与必要补全。

**答案页图 1**

![2021 数学二答案页 1](images/answer_pages/page-1.png)

**答案页图 2**

![2021 数学二答案页 2](images/answer_pages/page-2.png)

**答案页图 3**

![2021 数学二答案页 3](images/answer_pages/page-3.png)

## 答案速查

| 题号 | 题型 | 答案 |
|---|---|---|
| 1 | 选择题 | C |
| 2 | 选择题 | D |
| 3 | 选择题 | C |
| 4 | 选择题 | A |
| 5 | 选择题 | D |
| 6 | 选择题 | C |
| 7 | 选择题 | B |
| 8 | 选择题 | B |
| 9 | 选择题 | D |
| 10 | 选择题 | C |
| 11 | 填空题 | $\dfrac{1}{\ln 3}$ |
| 12 | 填空题 | $\dfrac{2}{3}$ |
| 13 | 填空题 | 1 |
| 14 | 填空题 | $\dfrac{\pi}{2}\cos\dfrac{2}{\pi}$ |
| 15 | 填空题 | $y=C_1e^x+e^{-x/2}\left(C_2\cos\dfrac{\sqrt{3}}{2}x+C_3\sin\dfrac{\sqrt{3}}{2}x\right)$ |
| 16 | 填空题 | -5 |
| 17 | 解答题 | $$\frac{1}{2}$$ |
| 18 | 解答题 | 在 $(-\infty,-1)\cup(0,+\infty)$ 上有 $f''(x)>0$，在 $(-1,0)$ 上有 $f''(x)<0$；垂直渐近线为 $x=-1$；斜渐近线为 $y=x-1$ 和 $y=-x+1$。 |
| 19 | 解答题 | $$S=\frac{22}{3},\qquad A=\frac{425\pi}{9}.$$ |
| 20 | 解答题 | （1）$y(x)=\frac13x^6+1\quad(x>0)$。 （2）当 $I_p$ 最小时，$p=(1,\frac43)$。 |
| 21 | 解答题 | $$\frac{1}{48}$$ |
| 22 | 解答题 | 有两组解： 1. 当 $b=1,\ a=1$ 时， $\Lambda=\operatorname{diag}(1,1,3),\quad P=\begin{pmatrix}-1&0&1\\1&0&1\\0&1&1\end{pmatrix}.$ 2. 当 $b=3,\ a=-1$ 时， $\Lambda=\operatorname{diag}(3,3,1),\quad P=\begin{pmatrix}1&0&-1\\1&0&1\\0&1&1\end{pmatrix}.$ |

## 详细解析

### 第 1 题

- 答案：C

当 \(t\to 0\) 时，\(e^{t^3}-1\sim t^3\)。因此
\[
I(x)\sim \int_0^{x^2} t^3\,dt=\frac{x^8}{4}.
\]
于是
\[
\frac{I(x)}{x^7}\sim \frac{x}{4}\to 0,
\]
故它是 \(x^7\) 的高阶无穷小。

### 第 2 题

- 答案：D

由 \(\lim_{x\to 0}\dfrac{e^x-1}{x}=1\)，知在 \(x=0\) 处连续。又
\[
f'(0)=\lim_{x\to 0}\frac{\frac{e^x-1}{x}-1}{x}
=\lim_{x\to 0}\frac{e^x-1-x}{x^2}=\frac12\ne 0.
\]
所以在 \(x=0\) 处可导且导数不为零。

### 第 3 题

- 答案：C

圆柱体体积 \(V=\pi r^2h\)，故
\[
\frac{dV}{dt}=\pi(2rr'h+r^2h').
\]
代入 \(r=10,h=5,r'=2,h'=-3\) 得
\[
\frac{dV}{dt}=\pi(2\cdot10\cdot2\cdot5+10^2\cdot(-3))=-100\pi.
\]
表面积 \(S=2\pi rh+2\pi r^2\)，故
\[
\frac{dS}{dt}=2\pi(r'h+rh')+4\pi rr'.
\]
代入得
\[
\frac{dS}{dt}=2\pi(2\cdot5+10\cdot(-3))+4\pi\cdot10\cdot2=40\pi.
\]

### 第 4 题

- 答案：A

令 \(c=\dfrac{b}{a}\)，则零点满足
\[
x-c\ln x=0 \quad (x>0).
\]
设 \(g(x)=x-c\ln x\)，则
\[
g'(x)=1-\frac{c}{x}=\frac{x-c}{x}.
\]
故 \(x=c\) 为极小值点，且
\[
g(c)=c-c\ln c=c(1-\ln c).
\]
要有 2 个零点，需极小值小于 0，即
\[
1-\ln c<0 \iff c>e.
\]
所以 \(\dfrac{b}{a}\in(e,+\infty)\)。

### 第 5 题

- 答案：D

由展开式
\[
\cos x=1-\frac{x^2}{2}+o(x^2),
\]
可得
\[
\sec x=\frac{1}{\cos x}=1+\frac{x^2}{2}+o(x^2).
\]
故 2 次泰勒多项式为 \(1+\dfrac{x^2}{2}\)，所以 \(a=0,b=\dfrac12\)。

### 第 6 题

- 答案：C

设 \(f_u(1,1)=A,\ f_v(1,1)=B\)。
由 \(u=x+1,v=e^x\) 在 \(x=0\) 时经过点 \((1,1)\)，两边求导得
\[
A\cdot 1+B\cdot 1=\left[x(x+1)^2\right]'_{x=0}=1.
\]
由 \(u=x,v=x^2\) 在 \(x=1\) 时也经过点 \((1,1)\)，两边求导得
\[
A\cdot 1+B\cdot 2=\left[2x^2\ln x\right]'_{x=1}=2.
\]
联立解得 \(A=0,B=1\)。故
\[
df(1,1)=A\,dx+B\,dy=dy.
\]

### 第 7 题

- 答案：B

区间 \([0,1]\) 等分为 \(n\) 份，每份长度为 \(\Delta x=\dfrac1n\)，第 \(k\) 个小区间中点为 \(\dfrac{2k-1}{2n}\)。因此积分的黎曼和表示为
\[
\int_0^1 f(x)\,dx=
\lim_{n\to\infty}\sum_{k=1}^{n} f\!\left(\frac{2k-1}{2n}\right)\frac1n.
\]
故选 B。

### 第 8 题

- 答案：B

展开得
\[
f=2x_2^2+2x_1x_2+2x_2x_3+2x_1x_3.
\]
对应对称矩阵为
\[
A=\begin{pmatrix}
0&1&1\\
1&2&1\\
1&1&0
\end{pmatrix}.
\]
求特征值可得 \(\lambda=3,-1,0\)。因此正特征值、负特征值、零特征值各一个，所以正惯性指数与负惯性指数分别为 \((1,1)\)。

### 第 9 题

- 答案：D

由题意存在矩阵 $C$，使 $A=BC$。于是 $A^T=C^TB^T$。若 $B^Tx=0$，则 $A^Tx=C^TB^Tx=0$，故 $B^Tx=0$ 的解必为 $A^Tx=0$ 的解，选 D。

### 第 10 题

- 答案：C

这是用初等行变换与初等列变换把矩阵同时化为对角形的问题。检验可知，取选项 C 中的下三角可逆矩阵 $P$ 与上三角可逆矩阵 $Q$ 时，$PAQ$ 恰为对角矩阵，因此选 C。

### 第 11 题

- 答案：$\dfrac{1}{\ln 3}$

被积函数为偶函数，原积分等于 $2\int_0^{\infty}x\,3^{-x^2}dx$。令 $u=x^2$，则 $du=2x\,dx$，得积分为 $\int_0^{\infty}3^{-u}du=\int_0^{\infty}e^{-u\ln3}du=\dfrac{1}{\ln3}$。

### 第 12 题

- 答案：$\dfrac{2}{3}$

由参数方程有 $\dfrac{dy}{dx}=\dfrac{dy/dt}{dx/dt}$。先求 $x'(t)=2e^t+1$，$y'(t)=4te^t+2t$，故 $\dfrac{dy}{dx}=\dfrac{4te^t+2t}{2e^t+1}$。再用 $\dfrac{d^2y}{dx^2}=\dfrac{d}{dt}(dy/dx)\big/\dfrac{dx}{dt}$，代入 $t=0$ 可得 $\dfrac{2}{3}$。

### 第 13 题

- 答案：1

先由 $(x,y)=(0,2)$ 代入原方程得 $z+2\ln z=1$，解得 $z=1$。设 $F(x,y,z)=(x+1)z+y\ln z-\arctan(2xy)-1=0$，则 $z_x=-\dfrac{F_x}{F_z}$。计算得 $F_x=z-\dfrac{2y}{1+4x^2y^2}$，$F_z=x+1+\dfrac{y}{z}$。代入 $(0,2,1)$，有 $F_x=-3$，$F_z=3$，故 $z_x=1$。

### 第 14 题

- 答案：$\dfrac{\pi}{2}\cos\dfrac{2}{\pi}$

积分区域可改写为 $1\le y\le t,\ 1\le x\le y^2$，故
$f(t)=\int_1^t dy\int_1^{y^2}\sin\left(\dfrac{x}{y}\right)dx=\int_1^t y\bigl(\cos\tfrac{1}{y}-\cos y\bigr)dy$。
由变上限积分求导得 $f'(t)=t\bigl(\cos\tfrac{1}{t}-\cos t\bigr)$，代入 $t=\dfrac{\pi}{2}$ 即得 $\dfrac{\pi}{2}\cos\dfrac{2}{\pi}$。

### 第 15 题

- 答案：$y=C_1e^x+e^{-x/2}\left(C_2\cos\dfrac{\sqrt{3}}{2}x+C_3\sin\dfrac{\sqrt{3}}{2}x\right)$

特征方程为 $r^3-1=0$，根为 $r=1,\ -\dfrac12\pm\dfrac{\sqrt3}{2}i$。因此通解为实指数项与共轭复根对应振荡项之和，即 $y=C_1e^x+e^{-x/2}\left(C_2\cos\dfrac{\sqrt3}{2}x+C_3\sin\dfrac{\sqrt3}{2}x\right)$。

### 第 16 题

- 答案：-5

按第一行展开并整理：
$M_{11}=x^3-4x-3$，$M_{12}=x^2-2x+1$，$M_{13}=-2x^2+3x+5$，$M_{14}=2x^2-x-7$。
故
$f(x)=xM_{11}-xM_{12}+M_{13}-2xM_{14}=x^4-5x^3-2x^2+13x+5$，所以 $x^3$ 项系数为 $-5$。

### 第 17 题

- 答案：$$\frac{1}{2}$$

通分得
$$\lim_{x\to 0}\frac{\left(1+\int_0^x e^{t^2}\,dt\right)\sin x-e^x+1}{(e^x-1)\sin x}.$$ 再拆成两部分，并用展开式 $\sin x=x+o(x)$、$e^x=1+x+\frac12x^2+o(x^2)$、$\int_0^x e^{t^2}\,dt=x+o(x)$，可得第一部分极限为 $-\frac12$，第二部分极限为 $1$，故原极限为 $\frac12$。

### 第 18 题

- 答案：在 $(-\infty,-1)\cup(0,+\infty)$ 上有 $f''(x)>0$，在 $(-1,0)$ 上有 $f''(x)<0$；垂直渐近线为 $x=-1$；斜渐近线为 $y=x-1$ 和 $y=-x+1$。

分段写成：$x>0$ 时 $f(x)=\dfrac{x^2}{1+x}$，$x<0$ 时 $f(x)=-\dfrac{x^2}{1+x}$。求导可得
$$f''(x)=\begin{cases}-\dfrac{2}{(1+x)^3},&x<0,\\[4pt]\dfrac{2}{(1+x)^3},&x>0.\end{cases}$$
于是 $(-\infty,-1)$ 与 $(0,+\infty)$ 上 $f''>0$，$(-1,0)$ 上 $f''<0$。又因 $x\to -1$ 时函数发散，故有垂直渐近线 $x=-1$。当 $x\to +\infty$ 时，$f(x)-x\to -1$，得斜渐近线 $y=x-1$；当 $x\to -\infty$ 时，$f(x)+x\to 1$，得斜渐近线 $y=-x+1$。

### 第 19 题

- 答案：$$S=\frac{22}{3},\qquad A=\frac{425\pi}{9}.$$

由不定积分两边求导得
$$\frac{f(x)}{\sqrt{x}}=\frac13x-1,$$
故
$$f(x)=\frac13x^{3/2}-x^{1/2},\qquad f'(x)=\frac12x^{1/2}-\frac12x^{-1/2}.$$ 
于是
$$\sqrt{1+[f'(x)]^2}=\frac12x^{1/2}+\frac12x^{-1/2}.$$ 
弧长
$$S=\int_4^9\sqrt{1+[f'(x)]^2}\,dx=\int_4^9\left(\frac12x^{1/2}+\frac12x^{-1/2}\right)dx=\frac{22}{3}.$$ 
旋转曲面面积
$$A=\int_4^9 2\pi f(x)\sqrt{1+[f'(x)]^2}\,dx=\pi\int_4^9\left(\frac13x^2-\frac23x+1\right)dx=\frac{425\pi}{9}.$$

### 第 20 题

- 答案：（1）$y(x)=\frac13x^6+1\quad(x>0)$。

（2）当 $I_p$ 最小时，$p=(1,\frac43)$。

方程化为
$$y'-\frac6x y=-\frac6x.$$ 
解线性微分方程得通解
$$y=Cx^6+1.$$ 代入 $y(\sqrt3)=10$，得 $C=\frac13$，故
$$y(x)=\frac13x^6+1.$$ 
设 $p=(x,y)$，则 $y'(x)=2x^5$，法线斜率为 $-\frac1{2x^5}$。法线方程为
$$Y-y=-\frac1{2x^5}(X-x).$$ 
令 $X=0$，得在 $y$ 轴上的截距
$$I_p=y+\frac1{2x^4}=\frac13x^6+1+\frac1{2x^4}.$$ 
求导：
$$I_p' = 2x^5-\frac2{x^5}.$$ 
令 $I_p'=0$ 得 $x=1$，此时取得最小值，故
$$y=\frac13+1=\frac43,$$
所以 $p=(1,\frac43)$。

### 第 21 题

- 答案：$$\frac{1}{48}$$

改用极坐标 $x=r\cos\theta,\ y=r\sin\theta$，则边界方程化为
$$r^4=r^2\cos 2\theta,$$
即
$$r^2=\cos 2\theta.$$ 
在第一象限内有 $0\le \theta\le \frac\pi4$，$0\le r\le \sqrt{\cos 2\theta}$。因此
$$\iint_D xy\,dxdy=\int_0^{\pi/4}\int_0^{\sqrt{\cos 2\theta}}(r\cos\theta)(r\sin\theta)r\,drd\theta.$$ 
先对 $r$ 积分，再对 $\theta$ 积分，得
$$\iint_D xy\,dxdy=\frac18\int_0^{\pi/4}\sin 2\theta\,\cos^2 2\theta\,d\theta=\frac1{48}.$$

### 第 22 题

- 答案：有两组解：

1. 当 $b=1,\ a=1$ 时，
$$
\Lambda=\operatorname{diag}(1,1,3),\quad
P=\begin{pmatrix}-1&0&1\\1&0&1\\0&1&1\end{pmatrix}.
$$

2. 当 $b=3,\ a=-1$ 时，
$$
\Lambda=\operatorname{diag}(3,3,1),\quad
P=\begin{pmatrix}1&0&-1\\1&0&1\\0&1&1\end{pmatrix}.
$$

特征多项式为
$$
\lvert\lambda E-A\rvert
=\begin{vmatrix}\lambda-2&-1&0\\-1&\lambda-2&0\\-1&-a&\lambda-b\end{vmatrix}
=(\lambda-b)\big((\lambda-2)^2-1\big)
=(\lambda-b)(\lambda-3)(\lambda-1).
$$
因仅有两个不同特征值，所以 $b=1$ 或 $b=3$。

当 $b=1$ 时，为使矩阵可对角化，特征值 $1$ 的几何重数需为 $2$，由 $r(E-A)=1$ 得 $a=1$。此时可取特征向量
$$\alpha_1=(-1,1,0)^T,\ \alpha_2=(0,0,1)^T,\ \alpha_3=(1,1,1)^T,$$
组成
$$P=(\alpha_1,\alpha_2,\alpha_3).$$

当 $b=3$ 时，同理需特征值 $3$ 的几何重数为 $2$，由 $r(3E-A)=1$ 得 $a=-1$。此时可取特征向量
$$\beta_1=(1,1,0)^T,\ \beta_2=(0,0,1)^T,\ \beta_3=(-1,1,1)^T,$$
组成
$$P=(\beta_1,\beta_2,\beta_3).$$
