# Math 1 2010 Answers

资料类型：考研数学一答案解析
年份：2010
科目：数学一
校对状态：已按题干截图、答案速查图和答案页图像清洗整理

## 答案速查

| 题号 | 题型 | 答案 |
|---|---|---|
| 1 | 选择题 | C |
| 2 | 选择题 | B |
| 3 | 选择题 | D |
| 4 | 选择题 | D |
| 5 | 选择题 | A |
| 6 | 选择题 | D |
| 7 | 选择题 | C |
| 8 | 选择题 | A |
| 9 | 填空题 | $0$ |
| 10 | 填空题 | $-4\pi$ |
| 11 | 填空题 | $0$ |
| 12 | 填空题 | $\displaystyle \frac{2}{3}$ |
| 13 | 填空题 | $6$ |
| 14 | 填空题 | $2$ |
| 15 | 解答题 | $y=C_1e^x+C_2e^{2x}-(x^2+2x)e^x$，其中 $C_1,C_2$ 为任意常数。 |
| 16 | 解答题 | 单调增加区间为 $(-1,0)$ 和 $(1,+\infty)$；单调减少区间为 $(-\infty,-1)$ 和 $(0,1)$；极小值 $f(\pm1)=0$，极大值 $f(0)=\displaystyle \frac{1}{2}\left(1-\frac{1}{e}\right)$。 |
| 17 | 解答题 | （I）$\displaystyle \int_0^1 \lvert\ln t\rvert[\ln(1+t)]^n\,dt < \int_0^1 t^n\lvert\ln t\rvert\,dt$；（II）$\displaystyle \lim_{n\to\infty}u_n=0$。 |
| 18 | 解答题 | 收敛域为 $[-1,1]$，和函数为 $S(x)=x\arctan x\ (-1\le x\le 1)$。 |
| 19 | 解答题 | 点 $P$ 的轨迹 $C$ 为 $\begin{cases}x^2+y^2+z^2-yz=1,\\ y=2z,\end{cases}$ 等价地 $\begin{cases}x^2+\displaystyle \frac{3}{4}y^2=1,\\ y=2z,\end{cases}$；曲面积分 $I=2\pi$。 |
| 20 | 解答题 | （I）$\lambda=-1,\ a=-2$；（II）通解为 $\boldsymbol{x}=k(1,0,1)^T+\left(\displaystyle \frac{3}{2},-\displaystyle \frac{1}{2},0\right)^T$，其中 $k$ 为任意常数。 |
| 21 | 解答题 | （I）$A=\begin{pmatrix}\displaystyle \frac{1}{2}&0&-\displaystyle \frac{1}{2}\\0&1&0\\-\displaystyle \frac{1}{2}&0&\displaystyle \frac{1}{2}\end{pmatrix}$；（II）$A+E$ 为正定矩阵。 |
| 22 | 解答题 | $A=\displaystyle \frac{1}{\pi}$，$f_{Y\mid X}(y\mid x)=\displaystyle \frac{1}{\sqrt{\pi}}e^{-(y-x)^2}$，$-\infty<y<+\infty$。 |
| 23 | 解答题 | $a_1=0,\ a_2=a_3=\displaystyle \frac{1}{n}$，$D(T)=\displaystyle \frac{\theta(1-\theta)}{n}$。 |

## 详细解析

### 第 1 题

**答案：** C

设
$$
I=\lim_{x\to\infty}\left[\frac{x^2}{(x-a)(x+b)}\right]^x .
$$
这是 $1^\infty$ 型极限，取对数：
$$
\ln I=\lim_{x\to\infty}x\ln\frac{x^2}{(x-a)(x+b)}.
$$
因为
$$
\frac{x^2}{(x-a)(x+b)}-1
=\frac{(a-b)x+ab}{(x-a)(x+b)},
$$
所以
$$
\ln I=\lim_{x\to\infty}x\left(\frac{x^2}{(x-a)(x+b)}-1\right)=a-b.
$$
故 $I=e^{a-b}$，选 C。

### 第 2 题

**答案：** B

由方程 $F\left(\frac{y}{x},\frac{z}{x}\right)=0$ 可知 $z/x$ 只由 $y/x$ 决定，因此 $z=z(x,y)$ 是一次齐次函数。由欧拉公式，
$$
x\frac{\partial z}{\partial x}+y\frac{\partial z}{\partial y}=z.
$$
故选 B。

### 第 3 题

**答案：** D

积分可写为
$$
\int_0^1\frac{\left(\ln^2(1-x)\right)^{1/m}}{x^{1/n}}\,dx.
$$
在 $x=0$ 附近，$\ln(1-x)\sim -x$，故被积函数等价于
$$
x^{2/m-1/n}.
$$
因 $2/m-1/n>-1$，所以 $x=0$ 处收敛。

在 $x=1$ 附近，令 $u=1-x$，被积函数只具有 $\lvert\ln u\rvert^{2/m}$ 型奇性，而
$$
\int_0^\varepsilon \lvert\ln u\rvert^{2/m}\,du
$$
收敛。因此不论正整数 $m,n$ 如何取值，原反常积分都收敛，选 D。

### 第 4 题

**答案：** D

将通项整理为
$$
\frac{n}{(n+i)(n^2+j^2)}
=\frac{1}{n^2}\cdot\frac{1}{\left(1+\frac{i}{n}\right)\left(1+\left(\frac{j}{n}\right)^2\right)}.
$$
因此二重和是 $[0,1]\times[0,1]$ 上的二重积分和，极限为
$$
\int_0^1\int_0^1\frac{1}{(1+x)(1+y^2)}\,dy\,dx.
$$
故选 D。

### 第 5 题

**答案：** A

因为 $A$ 为 $m\times n$ 矩阵、$B$ 为 $n\times m$ 矩阵，所以
$$
r(A)\le m,\qquad r(B)\le m.
$$
又 $AB=E_m$，于是
$$
m=r(AB)\le r(A)\le m,
$$
且
$$
m=r(AB)\le r(B)\le m.
$$
故 $r(A)=m,\ r(B)=m$，选 A。

### 第 6 题

**答案：** D

设 $\lambda$ 是 $A$ 的特征值。由 $A^2+A=O$ 得
$$
\lambda^2+\lambda=0,
$$
故 $\lambda=0$ 或 $\lambda=-1$。又 $A$ 是实对称矩阵，必可正交相似对角化；$r(A)=3$ 表明非零特征值有 $3$ 个。因此 $A$ 相似于
$$
\operatorname{diag}(-1,-1,-1,0).
$$
故选 D。

### 第 7 题

**答案：** C

随机变量在 $x=1$ 处的跳跃大小就是 $P\{X=1\}$。因此
$$
P\{X=1\}=F(1)-F(1-0)=\left(1-e^{-1}\right)-\frac{1}{2}=\frac{1}{2}-e^{-1}.
$$
故选 C。

### 第 8 题

**答案：** A

标准正态密度在 $(-\infty,0]$ 上的积分为 $\frac{1}{2}$。$f_2$ 是 $[-1,3]$ 上的均匀分布密度，故
$$
f_2(x)=\frac{1}{4}\quad(-1\le x\le3).
$$
在分段密度中只取 $x>0$ 的部分，所以
$$
\int_0^{+\infty} f_2(x)\,dx=\int_0^3\frac{1}{4}\,dx=\frac{3}{4}.
$$
由总积分为 $1$ 得
$$
\frac{a}{2}+\frac{3b}{4}=1,
$$
即 $2a+3b=4$，选 A。

### 第 9 题

**答案：** $0$

由题设 $x=e^{-t}$，所以 $x'(t)=-e^{-t}$，且
$$
y'(t)=\ln(1+t^2).
$$
于是
$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}=-e^t\ln(1+t^2).
$$
再对 $t$ 求导并除以 $x'(t)$，得
$$
\frac{d^2y}{dx^2}
=e^{2t}\left[\ln(1+t^2)+\frac{2t}{1+t^2}\right].
$$
代入 $t=0$，得
$$
\left.\frac{d^2y}{dx^2}\right|_{t=0}=0.
$$

### 第 10 题

**答案：** $-4\pi$

令 $t=\sqrt{x}$，则 $x=t^2,\ dx=2t\,dt$，积分化为
$$
\int_0^{\pi^2}\sqrt{x}\cos\sqrt{x}\,dx
=2\int_0^\pi t^2\cos t\,dt.
$$
分部积分得
$$
\int_0^\pi t^2\cos t\,dt=-2\pi,
$$
故原积分为
$$
2\cdot(-2\pi)=-4\pi.
$$

### 第 11 题

**答案：** $0$

曲线 $L$ 由 $A(-1,0)$ 到 $B(0,1)$ 再到 $C(1,0)$。补上线段 $CA$，得到闭曲线，所围区域关于 $y$ 轴对称。

取 $P(x,y)=xy,\ Q(x,y)=x^2$。由格林公式，闭曲线上的积分为
$$
\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dx\,dy
=\iint_D x\,dx\,dy=0.
$$
而补上的线段 $CA$ 上有 $y=0,\ dy=0$，其积分也为 $0$。因此原曲线积分为 $0$。

### 第 12 题

**答案：** $\displaystyle \frac{2}{3}$

按高度 $z$ 截取区域 $\Omega$。当 $0\le z\le1$ 时，截面为
$$
x^2+y^2\le z,
$$
面积为 $\pi z$。因此体积为
$$
V=\int_0^1 \pi z\,dz=\frac{\pi}{2},
$$
关于 $xOy$ 平面的静矩为
$$
M_z=\int_0^1 z\cdot \pi z\,dz=\frac{\pi}{3}.
$$
所以形心的竖坐标为
$$
\bar z=\frac{M_z}{V}=\frac{2}{3}.
$$

### 第 13 题

**答案：** $6$

若 $\alpha_1,\alpha_2,\alpha_3$ 生成的向量空间维数为 $2$，则 $\alpha_3$ 可由 $\alpha_1,\alpha_2$ 线性表示。

设
$$
\alpha_3=c_1\alpha_1+c_2\alpha_2.
$$
由前三个分量得
$$
\begin{cases}
c_1+c_2=2,\\
2c_1+c_2=1,\\
-c_1=1.
\end{cases}
$$
解得 $c_1=-1,\ c_2=3$。于是第四个分量应满足
$$
a=0\cdot c_1+2c_2=6.
$$

### 第 14 题

**答案：** $2$

由概率和为 $1$，有
$$
\sum_{k=0}^{\infty}\frac{C}{k!}=Ce=1,
$$
故 $C=e^{-1}$。因此 $X$ 服从参数为 $1$ 的泊松分布。

于是
$$
E(X^2)=D(X)+(EX)^2=1+1=2.
$$

### 第 15 题

**答案：** $y=C_1e^x+C_2e^{2x}-(x^2+2x)e^x$，其中 $C_1,C_2$ 为任意常数。

对应齐次方程的特征方程为
$$
r^2-3r+2=0,
$$
解得 $r=1,2$。所以齐次通解为
$$
y_h=C_1e^x+C_2e^{2x}.
$$
右端为 $2xe^x$，且 $r=1$ 是特征根，设特解
$$
y_p=x(ax+b)e^x.
$$
代入原方程 $y''-3y'+2y=2xe^x$，比较系数得
$$
-2a=2,\qquad 2a-b=0,
$$
故 $a=-1,\ b=-2$。因此
$$
y_p=-x(x+2)e^x.
$$
原方程通解为
$$
y=C_1e^x+C_2e^{2x}-(x^2+2x)e^x.
$$

### 第 16 题

**答案：** 单调增加区间为 $(-1,0)$ 和 $(1,+\infty)$；单调减少区间为 $(-\infty,-1)$ 和 $(0,1)$；极小值 $f(\pm1)=0$，极大值 $f(0)=\displaystyle \frac{1}{2}\left(1-\frac{1}{e}\right)$。

将函数写成
$$
f(x)=x^2\int_1^{x^2}e^{-t^2}\,dt-\int_1^{x^2}t e^{-t^2}\,dt.
$$
求导得
$$
f'(x)=2x\int_1^{x^2}e^{-t^2}\,dt.
$$
由于 $e^{-t^2}>0$，$\int_1^{x^2}e^{-t^2}\,dt$ 在 $|x|>1$ 时为正，在 $|x|<1$ 时为负。于是 $f'(x)$ 的符号为：
$$
\begin{array}{c|cccc}
x&(-\infty,-1)&(-1,0)&(0,1)&(1,+\infty)\\
\hline
f'(x)&-&+&-&+
\end{array}
$$
故单调增加区间为 $(-1,0)$ 和 $(1,+\infty)$，单调减少区间为 $(-\infty,-1)$ 和 $(0,1)$。

又
$$
f(\pm1)=0,
$$
且
$$
f(0)=\int_1^0(-t)e^{-t^2}\,dt=\int_0^1t e^{-t^2}\,dt=\frac{1}{2}\left(1-\frac{1}{e}\right).
$$
因此 $f(\pm1)=0$ 为极小值，$f(0)=\frac{1}{2}\left(1-\frac{1}{e}\right)$ 为极大值。

### 第 17 题

**答案：** （I）$\displaystyle \int_0^1 \lvert\ln t\rvert[\ln(1+t)]^n\,dt < \int_0^1 t^n\lvert\ln t\rvert\,dt$；（II）$\displaystyle \lim_{n\to\infty}u_n=0$。

当 $0<t\le1$ 时，
$$
0<\ln(1+t)<t.
$$
因此对任意正整数 $n$，有
$$
[\ln(1+t)]^n<t^n.
$$
两边同乘正函数 $\lvert\ln t\rvert$ 并积分，得
$$
\int_0^1 \lvert\ln t\rvert[\ln(1+t)]^n\,dt
<\int_0^1 t^n\lvert\ln t\rvert\,dt.
$$

记左端为 $u_n$。由上式和非负性可得
$$
0\le u_n<\int_0^1 t^n\lvert\ln t\rvert\,dt.
$$
分部积分或利用参数积分可得
$$
\int_0^1 t^n\lvert\ln t\rvert\,dt=\frac{1}{(n+1)^2}.
$$
因为 $\frac{1}{(n+1)^2}\to0$，由夹逼准则得
$$
\lim_{n\to\infty}u_n=0.
$$

### 第 18 题

**答案：** 收敛域为 $[-1,1]$，和函数为 $S(x)=x\arctan x\ (-1\le x\le 1)$。

设
$$
S(x)=\sum_{n=1}^{\infty}\frac{(-1)^{n-1}}{2n-1}x^{2n}.
$$
由比值法，收敛半径为 $1$；当 $x=\pm1$ 时，级数化为交错级数
$$
\sum_{n=1}^{\infty}\frac{(-1)^{n-1}}{2n-1},
$$
仍收敛。因此收敛域为 $[-1,1]$。

对 $|x|<1$，有
$$
S(x)=x\sum_{n=1}^{\infty}\frac{(-1)^{n-1}}{2n-1}x^{2n-1}.
$$
而
$$
\arctan x=\sum_{n=1}^{\infty}\frac{(-1)^{n-1}}{2n-1}x^{2n-1},
$$
所以
$$
S(x)=x\arctan x.
$$
在端点 $x=\pm1$ 处该表达式与级数和一致，故和函数为
$$
S(x)=x\arctan x,
\qquad -1\le x\le1.
$$

### 第 19 题

**答案：** 点 $P$ 的轨迹 $C$ 为 $\begin{cases}x^2+y^2+z^2-yz=1,\\ y=2z,\end{cases}$ 等价地 $\begin{cases}x^2+\displaystyle \frac{3}{4}y^2=1,\\ y=2z,\end{cases}$；曲面积分 $I=2\pi$。

令
$$
F(x,y,z)=x^2+y^2+z^2-yz-1.
$$
椭球面在点 $P(x,y,z)$ 处的法向量为
$$
\nabla F=(2x,2y-z,2z-y).
$$
若切平面与 $xOy$ 面垂直，则两个平面的法向量互相垂直，即
$$
(2x,2y-z,2z-y)\cdot(0,0,1)=0.
$$
故 $2z-y=0$，即 $y=2z$。再与椭球面方程联立，得轨迹
$$
C:\begin{cases}
x^2+y^2+z^2-yz=1,\\
y=2z.
\end{cases}
$$
代入 $z=\frac{y}{2}$，也可写为
$$
C:\begin{cases}
x^2+\frac{3}{4}y^2=1,\\
y=2z.
\end{cases}
$$

曲面 $\Sigma$ 位于平面 $y=2z$ 上方，即在 $\Sigma$ 上 $y\le2z$，所以
$$
\lvert y-2z\rvert=2z-y.
$$
将椭球面看作 $z=z(x,y)$，由隐函数求导得
$$
z_x=\frac{2x}{y-2z},\qquad z_y=\frac{2y-z}{y-2z}.
$$
于是
$$
dS=\frac{\sqrt{4+y^2+z^2-4yz}}{2z-y}\,dx\,dy.
$$
投影区域为
$$
D_{xy}:\quad x^2+\frac{3}{4}y^2\le1.
$$
因此
$$
\begin{aligned}
I
&=\iint_{\Sigma}\frac{(x+\sqrt{3})(2z-y)}{\sqrt{4+y^2+z^2-4yz}}\,dS\\
&=\iint_{D_{xy}}(x+\sqrt{3})\,dx\,dy.
\end{aligned}
$$
区域 $D_{xy}$ 关于 $y$ 轴对称，故 $\iint_{D_{xy}}x\,dx\,dy=0$。其面积为
$$
\pi\cdot1\cdot\frac{2}{\sqrt{3}}=\frac{2\pi}{\sqrt{3}}.
$$
所以
$$
I=\sqrt{3}\cdot\frac{2\pi}{\sqrt{3}}=2\pi.
$$

### 第 20 题

**答案：** （I）$\lambda=-1,\ a=-2$；（II）通解为 $\boldsymbol{x}=k(1,0,1)^T+\left(\displaystyle \frac{3}{2},-\displaystyle \frac{1}{2},0\right)^T$，其中 $k$ 为任意常数。

因为方程组 $A\boldsymbol{x}=\boldsymbol{b}$ 存在两个不同的解，所以有无穷多解，必须满足
$$
r(A)=r(A:\boldsymbol{b})<3.
$$
先令 $\det A=0$：
$$
\det A=(\lambda-1)^2(\lambda+1)=0,
$$
故 $\lambda=1$ 或 $\lambda=-1$。

当 $\lambda=1$ 时，$A$ 的第二行为零行，但 $\boldsymbol{b}$ 的第二个分量为 $1$，方程组无解。因此 $\lambda=-1$。

代入 $\lambda=-1$，由增广矩阵相容条件可得 $a=-2$。此时
$$
(A:\boldsymbol{b})
\sim
\begin{pmatrix}
1&0&-1&\vline&\displaystyle \frac{3}{2}\\
0&1&0&\vline&-\displaystyle \frac{1}{2}\\
0&0&0&\vline&0
\end{pmatrix}.
$$
故
$$
x_1=\frac{3}{2}+x_3,
\qquad x_2=-\frac{1}{2}.
$$
令 $x_3=k$，得通解
$$
\boldsymbol{x}=k(1,0,1)^T+
\left(\frac{3}{2},-\frac{1}{2},0\right)^T,
$$
其中 $k$ 为任意常数。

### 第 21 题

**答案：** （I）$A=\begin{pmatrix}\displaystyle \frac{1}{2}&0&-\displaystyle \frac{1}{2}\\0&1&0\\-\displaystyle \frac{1}{2}&0&\displaystyle \frac{1}{2}\end{pmatrix}$；（II）$A+E$ 为正定矩阵。

正交变换下标准形为 $y_1^2+y_2^2$，说明 $A$ 的特征值为
$$
\lambda_1=\lambda_2=1,
\qquad \lambda_3=0.
$$
又 $Q$ 的第三列
$$
\alpha_3=\left(\frac{\sqrt{2}}{2},0,\frac{\sqrt{2}}{2}\right)^T
$$
是 $\lambda_3=0$ 的单位特征向量。由于 $A$ 为实对称矩阵，$A$ 就是在 $\alpha_3^\perp$ 上特征值为 $1$、在 $\alpha_3$ 方向上特征值为 $0$ 的正交投影矩阵，即
$$
A=E-\alpha_3\alpha_3^T.
$$
计算得
$$
A=\begin{pmatrix}
\displaystyle \frac{1}{2}&0&-\displaystyle \frac{1}{2}\\
0&1&0\\
-\displaystyle \frac{1}{2}&0&\displaystyle \frac{1}{2}
\end{pmatrix}.
$$

$A+E$ 的特征值为
$$
2,\ 2,\ 1,
$$
均大于 $0$，因此 $A+E$ 为正定矩阵。

### 第 22 题

**答案：** $A=\displaystyle \frac{1}{\pi}$，$f_{Y\mid X}(y\mid x)=\displaystyle \frac{1}{\sqrt{\pi}}e^{-(y-x)^2}$，$-\infty<y<+\infty$。

将指数配方：
$$
-2x^2+2xy-y^2=-x^2-(y-x)^2.
$$
所以
$$
f(x,y)=Ae^{-x^2}e^{-(y-x)^2}.
$$
由密度积分为 $1$，得
$$
1=A\int_{-\infty}^{+\infty}e^{-x^2}\,dx
\int_{-\infty}^{+\infty}e^{-(y-x)^2}\,dy
=A\pi,
$$
故
$$
A=\frac{1}{\pi}.
$$

边缘密度为
$$
f_X(x)=\int_{-\infty}^{+\infty}f(x,y)\,dy
=\frac{1}{\sqrt{\pi}}e^{-x^2}.
$$
于是条件密度
$$
f_{Y\mid X}(y\mid x)=\frac{f(x,y)}{f_X(x)}
=\frac{1}{\sqrt{\pi}}e^{-(y-x)^2},
\qquad -\infty<y<+\infty.
$$

### 第 23 题

**答案：** $a_1=0,\ a_2=a_3=\displaystyle \frac{1}{n}$，$D(T)=\displaystyle \frac{\theta(1-\theta)}{n}$。

由题意，
$$
N_1\sim B(n,1-\theta),\qquad
N_2\sim B(n,\theta-\theta^2),\qquad
N_3\sim B(n,\theta^2).
$$
因此
$$
\begin{aligned}
E(T)
&=a_1E(N_1)+a_2E(N_2)+a_3E(N_3)\\
&=n a_1+n(a_2-a_1)\theta+n(a_3-a_2)\theta^2.
\end{aligned}
$$
要使 $T$ 为 $\theta$ 的无偏估计量，需对任意 $\theta$ 有 $E(T)=\theta$，故
$$
na_1=0,
\qquad n(a_2-a_1)=1,
\qquad n(a_3-a_2)=0.
$$
解得
$$
a_1=0,
\qquad a_2=a_3=\frac{1}{n}.
$$
此时
$$
T=\frac{N_2+N_3}{n}=\frac{n-N_1}{n}.
$$
又 $N_1\sim B(n,1-\theta)$，所以
$$
D(T)=\frac{1}{n^2}D(N_1)
=\frac{1}{n^2}n(1-\theta)\theta
=\frac{\theta(1-\theta)}{n}.
$$
