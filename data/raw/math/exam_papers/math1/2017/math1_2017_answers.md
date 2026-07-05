# Math 1 2017 Answers

资料类型：考研数学一答案解析
年份：2017
科目：数学一
校对状态：reviewed

## 选择题

| 题号 | 标准答案 |
|---|---|
| 1 | A |
| 2 | C |
| 3 | D |
| 4 | C |
| 5 | A |
| 6 | B |
| 7 | A |
| 8 | B |

## 填空题

| 题号 | 标准答案 |
|---|---|
| 9 | $0$ |
| 10 | $e^{-x}(C_1\cos\sqrt{2}x+C_2\sin\sqrt{2}x)$ |
| 11 | $-1$ |
| 12 | $\dfrac{1}{(1+x)^2}$ |
| 13 | $2$ |
| 14 | $2$ |

## 解答题

| 题号 | 标准答案 |
|---|---|
| 15 | （1）$\left.\dfrac{dy}{dx}\right\rvert_{x=0}=f_u(1,1)$；（2）$\left.\dfrac{d^2y}{dx^2}\right\rvert_{x=0}=f_u(1,1)+f_{uu}(1,1)-f_v(1,1)$ |
| 16 | $\dfrac{1}{4}$ |
| 17 | 极大值为 $y(1)=1$，极小值为 $y(-1)=0$ |
| 18 | （1）方程 $f(x)=0$ 在区间 $(0,1)$ 内至少有一个实根；（2）方程 $f(x)f''(x)+[f'(x)]^2=0$ 在区间 $(0,1)$ 内至少有两个不同实根 |
| 19 | （1）投影曲线为 $x^2+y^2=2x,\ z=0$；（2）质量 $M=64$ |
| 20 | （1）$r(A)=2$；（2）$Ax=\beta$ 的通解为 $x=\begin{pmatrix}1\\1\\1\end{pmatrix}+k\begin{pmatrix}1\\2\\-1\end{pmatrix}$ |
| 21 | （1）$a=2$；（2）可取 $Q=\begin{pmatrix} \frac{1}{\sqrt{3}} & -\frac{1}{\sqrt{2}} & \frac{1}{\sqrt{6}} \\ -\frac{1}{\sqrt{3}} & 0 & \frac{2}{\sqrt{6}} \\ \frac{1}{\sqrt{3}} & \frac{1}{\sqrt{2}} & \frac{1}{\sqrt{6}} \end{pmatrix}$，标准形为 $f=-3y_1^2+6y_2^2$ |
| 22 | （1）$P\{Y\le E(Y)\}=\dfrac{4}{9}$；（2）$f_Z(z)=\begin{cases} z, & 0<z<1, \\ z-2, & 2<z<3, \\ 0, & \text{其他}. \end{cases}$ |
| 23 | （1）$f_Z(z)=\begin{cases}\sqrt{\dfrac{2}{\pi}}\dfrac{1}{\sigma}e^{-z^2/(2\sigma^2)}, & z\ge 0,\\ 0, & z<0;\end{cases}$ （2）矩估计为 $\hat\sigma=\sqrt{\dfrac{\pi}{2}}\,\overline{Z}$；（3）最大似然估计为 $\hat\sigma=\sqrt{\dfrac{1}{n}\sum_{i=1}^n Z_i^2}$ |

## 详细解析

### 第 1 题

#### 标准答案

A

#### 解析

由题意，函数在 $x=0$ 处连续，因此

$$
b=\lim_{x\to 0^+}\frac{1-\cos\sqrt{x}}{ax}.
$$

令 $t=\sqrt{x}$，则 $x=t^2$，上式化为

$$
b=\lim_{t\to 0^+}\frac{1-\cos t}{at^2}=\frac{1}{a}\lim_{t\to 0^+}\frac{1-\cos t}{t^2}=\frac{1}{2a}.
$$

所以 $ab=\frac{1}{2}$，故选 A。

### 第 2 题

#### 标准答案

C

#### 解析

由 $f(x)f'(x)>0$ 可得

$$
2f(x)f'(x)>0,
$$

即

$$
\left[f^2(x)\right]'>0.
$$

因此 $f^2(x)$ 严格单增，从而 $|f(x)|$ 也严格单增，所以

$$
|f(1)|>|f(-1)|.
$$

故选 C。

### 第 3 题

#### 标准答案

D

#### 解析

向量 $n=(1,2,2)$ 的方向余弦为

$$
\cos\alpha=\frac{1}{3},\quad \cos\beta=\frac{2}{3},\quad \cos\gamma=\frac{2}{3}.
$$

函数 $f(x,y,z)=x^2y+z^2$ 在点 $(1,2,0)$ 处的偏导数为

$$
f_x(1,2,0)=4,\quad f_y(1,2,0)=1,\quad f_z(1,2,0)=0.
$$

故沿向量 $n$ 的方向导数为

$$
\frac{\partial f}{\partial n}=f_x\cos\alpha+f_y\cos\beta+f_z\cos\gamma
=4\cdot\frac{1}{3}+1\cdot\frac{2}{3}+0\cdot\frac{2}{3}=2.
$$

故选 D。

### 第 4 题

#### 标准答案

C

#### 解析

设 $s_1(t),s_2(t)$ 分别表示甲、乙两人的路程。计时开始时甲在乙前方 $10$ m，要在 $t_0$ 时刻追上甲，应满足

$$
s_1(t_0)-s_2(t_0)=-10.
$$

由图中阴影面积可知：

$$
\int_0^{10}[v_1(t)-v_2(t)]\,dt=10,
$$

所以 $t=10$ 时有 $s_1(10)-s_2(10)=10$。

当 $15<t<20$ 时，

$$
s_1(t)-s_2(t)=10+\int_{10}^{t}[v_1(t)-v_2(t)]\,dt
>10+\int_{10}^{25}[v_1(t)-v_2(t)]\,dt=10-20=-10.
$$

当 $t=25$ 时，

$$
s_1(25)-s_2(25)=\int_0^{25}[v_1(t)-v_2(t)]\,dt=10-20=-10.
$$

而当 $t>25$ 时，

$$
s_1(t)-s_2(t)=\int_0^{25}[v_1(t)-v_2(t)]\,dt+\int_{25}^{t}[v_1(t)-v_2(t)]\,dt
=-10+\int_{25}^{t}[v_1(t)-v_2(t)]\,dt>-10.
$$

因此恰在 $t_0=25$ 时乙追上甲，故选 C。

### 第 5 题

#### 标准答案

A

#### 解析

因为 $\alpha$ 为 3 维单位列向量，所以

$$
\alpha^T\alpha=1=\operatorname{tr}(\alpha\alpha^T).
$$

于是矩阵 $\alpha\alpha^T$ 的特征值为 $1,0,0$。因此

$$
|E-\alpha\alpha^T|=0,
$$

说明矩阵 $E-\alpha\alpha^T$ 不可逆，故选 A。

### 第 6 题

#### 标准答案

B

#### 解析

矩阵 $A,B$ 都是上三角矩阵，所以它们的特征值都是 $1,2,2$。

要判断能否与对角矩阵 $C$ 相似，只需看对应特征值 $2$ 的线性无关特征向量个数。

对于 $A$，

$$
\dim V_{\lambda=2}=3-r(2E-A)=3-1=2,
$$

所以 $A$ 可相似对角化。

对于 $B$，

$$
\dim V_{\lambda=2}=3-r(2E-B)=3-2=1,
$$

所以 $B$ 不能相似对角化。

故 $A$ 与 $C$ 相似而 $B$ 与 $C$ 不相似，选 B。

### 第 7 题

#### 标准答案

A

#### 解析

由题设

$$
P(A\mid B)>P(A\mid \overline{B}),
$$

即

$$
\frac{P(AB)}{P(B)}>\frac{P(A)-P(AB)}{1-P(B)}.
$$

整理得

$$
P(AB)>P(A)P(B).
$$

于是

$$
P(B\mid A)=\frac{P(AB)}{P(A)}>P(B),
$$

且

$$
P(B\mid \overline{A})=\frac{P(B)-P(AB)}{1-P(A)}
<\frac{P(B)-P(A)P(B)}{1-P(A)}=P(B).
$$

所以

$$
P(B\mid A)>P(B\mid \overline{A}).
$$

故选 A。

### 第 8 题

#### 标准答案

B

#### 解析

因为 $X_i\sim N(\mu,1)$，所以

$$
X_i-\mu\sim N(0,1),
$$

从而

$$
\sum_{i=1}^n (X_i-\mu)^2\sim \chi^2(n),
$$

故 A 正确。

又因为

$$
\frac{\sum_{i=1}^n (X_i-\overline{X})^2}{1}=(n-1)S^2\sim \chi^2(n-1),
$$

故 C 正确。

并且 $\overline{X}\sim N\left(\mu,\frac{1}{n}\right)$，所以

$$
n(\overline{X}-\mu)^2\sim \chi^2(1),
$$

故 D 正确。

对 B 而言，$X_n-X_1\sim N(0,2)$，因此

$$
\frac{X_n-X_1}{\sqrt{2}}\sim N(0,1),
$$

应有

$$
\left(\frac{X_n-X_1}{\sqrt{2}}\right)^2\sim \chi^2(1),
$$

而不是 $2(X_n-X_1)^2\sim \chi^2$。故 B 错误。

### 第 9 题

#### 标准答案

$0$

#### 解析

根据

$$
f(x)=\frac{1}{1+x^2}=\sum_{n=0}^{\infty}(-1)^n x^{2n}\quad (|x|<1),
$$

又有麦克劳林展开

$$
f(x)=\sum_{n=0}^{\infty}\frac{f^{(n)}(0)}{n!}x^n.
$$

比较系数可知

$$
f^{(n)}(0)=
\begin{cases}
(-1)^{n/2}n!, & n\text{ 为偶数},\\
0, & n\text{ 为奇数}.
\end{cases}
$$

因此 $f^{(3)}(0)=0$。

### 第 10 题

#### 标准答案

$e^{-x}(C_1\cos\sqrt{2}x+C_2\sin\sqrt{2}x)$

#### 解析

微分方程的特征方程为

$$
r^2+2r+3=0.
$$

其特征根为

$$
r_{1,2}=-1\pm \sqrt{2}i.
$$

故原方程通解为

$$
y=e^{-x}(C_1\cos\sqrt{2}x+C_2\sin\sqrt{2}x).
$$

### 第 11 题

#### 标准答案

$-1$

#### 解析

设

$$
P(x,y)=\frac{x}{x^2+y^2-1},\qquad Q(x,y)=\frac{-ay}{x^2+y^2-1}.
$$

曲线积分在区域 $D=\{(x,y)\mid x^2+y^2<1\}$ 内与路径无关的条件是

$$
\frac{\partial P}{\partial y}=\frac{\partial Q}{\partial x}.
$$

计算得

$$
\frac{\partial P}{\partial y}=\frac{-2xy}{(x^2+y^2-1)^2},\qquad
\frac{\partial Q}{\partial x}=\frac{2axy}{(x^2+y^2-1)^2}.
$$

两者恒等相等时有 $a=-1$。

### 第 12 题

#### 标准答案

$\dfrac{1}{(1+x)^2}$

#### 解析

令

$$
S(x)=\sum_{n=1}^{\infty}(-1)^{n-1}nx^{n-1},\quad x\in(-1,1).
$$

则

$$
\int_0^x S(t)\,dt
=\sum_{n=1}^{\infty}(-1)^{n-1}\int_0^x nt^{n-1}\,dt
=\sum_{n=1}^{\infty}(-1)^{n-1}x^n
=\frac{x}{1+x}.
$$

因此

$$
S(x)=\left(\frac{x}{1+x}\right)'=\frac{1}{(1+x)^2}.
$$

### 第 13 题

#### 标准答案

$2$

#### 解析

有

$$
(A\alpha_1,A\alpha_2,A\alpha_3)=A(\alpha_1,\alpha_2,\alpha_3).
$$

因为 $\alpha_1,\alpha_2,\alpha_3$ 线性无关，所以矩阵 $(\alpha_1,\alpha_2,\alpha_3)$ 可逆，于是

$$
r(A\alpha_1,A\alpha_2,A\alpha_3)=r(A).
$$

由矩阵

$$
A=
\begin{pmatrix}
1&0&1\\
1&1&2\\
0&1&1
\end{pmatrix}
$$

可知第三列等于前两列之和，因此 $r(A)=2$。故所求秩为 $2$。

### 第 14 题

#### 标准答案

$2$

#### 解析

由分布函数可得随机变量 $X$ 的密度为

$$
f(x)=F'(x)=0.5\varphi(x)+0.25\varphi\left(\frac{x-4}{2}\right).
$$

因此

$$
EX=\int_{-\infty}^{+\infty}xf(x)\,dx
=0.5\int_{-\infty}^{+\infty}x\varphi(x)\,dx
+0.25\int_{-\infty}^{+\infty}x\varphi\left(\frac{x-4}{2}\right)dx.
$$

令 $t=\dfrac{x-4}{2}$，则 $x=2t+4,dx=2dt$，于是

$$
EX=0+0.5\int_{-\infty}^{+\infty}(2t+4)\varphi(t)dt
=0.5\left[2\int_{-\infty}^{+\infty}t\varphi(t)dt+4\int_{-\infty}^{+\infty}\varphi(t)dt\right]=2.
$$

### 第 15 题

#### 标准答案

（1）$\left.\dfrac{dy}{dx}\right\rvert_{x=0}=f_u(1,1)$；（2）$\left.\dfrac{d^2y}{dx^2}\right\rvert_{x=0}=f_u(1,1)+f_{uu}(1,1)-f_v(1,1)$

#### 解析

因为

$$
y=f(e^x,\cos x),
$$

设 $u=e^x,v=\cos x$，由链式法则得

$$
\frac{dy}{dx}=f_u(u,v)\frac{du}{dx}+f_v(u,v)\frac{dv}{dx}
=f_u(u,v)e^x-f_v(u,v)\sin x.
$$

再对 $x$ 求导，

$$
\frac{d^2y}{dx^2}
=f_u(u,v)e^x+\left(f_{uu}(u,v)e^x-f_{uv}(u,v)\sin x\right)e^x
-f_v(u,v)\cos x
-\left(f_{uv}(u,v)e^x-f_{vv}(u,v)\sin x\right)\sin x.
$$

当 $x=0$ 时，

$$
u=e^0=1,\qquad v=\cos 0=1,\qquad \sin 0=0,\qquad \cos 0=1.
$$

所以

$$
\left.\frac{dy}{dx}\right\rvert_{x=0}=f_u(1,1),
$$

$$
\left.\frac{d^2y}{dx^2}\right\rvert_{x=0}=f_u(1,1)+f_{uu}(1,1)-f_v(1,1).
$$

### 第 16 题

#### 标准答案

$\dfrac{1}{4}$

#### 解析

将极限写成定积分的黎曼和：

$$
\lim_{n\to\infty}\sum_{k=1}^n\frac{k}{n^2}\ln\left(1+\frac{k}{n}\right)
=\lim_{n\to\infty}\sum_{k=1}^n\left(\frac{k}{n}\ln\left(1+\frac{k}{n}\right)\right)\frac{1}{n}
=\int_0^1 x\ln(1+x)\,dx.
$$

分部积分得

$$
\int_0^1 x\ln(1+x)\,dx
=\left.\frac{x^2}{2}\ln(1+x)\right|_0^1-\frac{1}{2}\int_0^1\frac{x^2}{1+x}\,dx.
$$

又

$$
\frac{x^2}{1+x}=x-1+\frac{1}{1+x},
$$

故

$$
\int_0^1 x\ln(1+x)\,dx
=\frac{1}{2}\ln 2-\frac{1}{2}\int_0^1\left(x-1+\frac{1}{1+x}\right)dx
=\frac{1}{2}\ln 2-\frac{1}{2}\left(\frac{1}{2}-1+\ln 2\right)
=\frac{1}{4}.
$$

### 第 17 题

#### 标准答案

极大值为 $y(1)=1$，极小值为 $y(-1)=0$

#### 解析

由方程

$$
x^3+y^3-3x+3y-2=0
$$

对 $x$ 求导，得

$$
3x^2+3y^2y'-3+3y'=0. \tag{1}
$$

再求导，得

$$
6x+6y(y')^2+3y^2y''+3y''=0. \tag{2}
$$

在式 (1) 中令 $y'=0$，得到 $x=-1$ 或 $x=1$。

当 $x=-1$ 时，由原方程得 $y(-1)=0$；当 $x=1$ 时，由原方程得 $y(1)=1$。

将 $x=-1,y(-1)=0,y'(-1)=0$ 代入式 (2)，得

$$
y''(-1)=2>0,
$$

所以 $y(-1)=0$ 是极小值。

将 $x=1,y(1)=1,y'(1)=0$ 代入式 (2)，得

$$
y''(1)=-1<0,
$$

所以 $y(1)=1$ 是极大值。

### 第 18 题

#### 标准答案

（1）方程 $f(x)=0$ 在区间 $(0,1)$ 内至少有一个实根；（2）方程 $f(x)f''(x)+[f'(x)]^2=0$ 在区间 $(0,1)$ 内至少有两个不同实根

#### 解析

先证第（1）问。由题设 $f(x)$ 在 $[0,1]$ 上连续，且

$$
\lim_{x\to 0^+}\frac{f(x)}{x}<0.
$$

因为该极限存在，所以 $f(0)=0$。又由极限的保号性，存在 $a\in(0,1)$，使得

$$
\frac{f(a)}{a}<0,
$$

即 $f(a)<0$。而 $f(1)>0$，由介值定理可知存在 $b\in(a,1)\subset(0,1)$，使得

$$
f(b)=0.
$$

故方程 $f(x)=0$ 在 $(0,1)$ 内至少有一个实根。

再证第（2）问。由上面结论知 $f(0)=f(b)=0$，根据罗尔定理，存在 $c\in(0,b)\subset(0,1)$ 使得

$$
f'(c)=0.
$$

令

$$
F(x)=f(x)f'(x),
$$

则 $F(x)$ 在 $[0,b]$ 上可导，且

$$
F(0)=0,\qquad F(c)=0,\qquad F(b)=0.
$$

分别在区间 $(0,c)$ 与 $(c,b)$ 上应用罗尔定理，存在 $\xi\in(0,c),\eta\in(c,b)$，使得

$$
F'(\xi)=0,\qquad F'(\eta)=0.
$$

而

$$
F'(x)=f(x)f''(x)+[f'(x)]^2,
$$

故 $\xi,\eta$ 是方程

$$
f(x)f''(x)+[f'(x)]^2=0
$$

在区间 $(0,1)$ 内的两个不同实根。

### 第 19 题

#### 标准答案

（1）投影曲线为 $x^2+y^2=2x,\ z=0$；（2）质量 $M=64$

#### 解析

圆锥面与柱面交线 $C$ 满足

$$
z=\sqrt{x^2+y^2},\qquad z^2=2x.
$$

消去 $z$ 得到其在 $xOy$ 平面上的投影曲线为

$$
x^2+y^2=2x,\qquad z=0.
$$

再求曲面片 $S$ 的质量。因为密度

$$
\mu(x,y,z)=9\sqrt{x^2+y^2+z^2},
$$

故

$$
M=\iint_S 9\sqrt{x^2+y^2+z^2}\,dS.
$$

在圆锥面 $z=\sqrt{x^2+y^2}$ 上，

$$
z_x=\frac{x}{\sqrt{x^2+y^2}},\qquad z_y=\frac{y}{\sqrt{x^2+y^2}},
$$

所以

$$
\sqrt{1+z_x^2+z_y^2}=\sqrt{2},
$$

且

$$
\sqrt{x^2+y^2+z^2}=\sqrt{2(x^2+y^2)}.
$$

于是

$$
M=9\iint_D \sqrt{2(x^2+y^2)}\cdot \sqrt{2}\,dxdy
=18\iint_D \sqrt{x^2+y^2}\,dxdy,
$$

其中投影区域

$$
D=\{(x,y)\mid x^2+y^2\le 2x\}.
$$

改用极坐标：$x=r\cos\theta,y=r\sin\theta$，则区域为

$$
-\frac{\pi}{2}\le \theta\le \frac{\pi}{2},\qquad 0\le r\le 2\cos\theta.
$$

因此

$$
M=18\int_{-\pi/2}^{\pi/2}\int_0^{2\cos\theta} r\cdot r\,drd\theta
=48\int_{-\pi/2}^{\pi/2}\cos^3\theta\,d\theta
=64.
$$

### 第 20 题

#### 标准答案

（1）$r(A)=2$；（2）$Ax=\beta$ 的通解为 $x=\begin{pmatrix}1\\1\\1\end{pmatrix}+k\begin{pmatrix}1\\2\\-1\end{pmatrix}$

#### 解析

由 $\alpha_3=\alpha_1+2\alpha_2$ 可知 $\alpha_1,\alpha_2,\alpha_3$ 线性相关，因此

$$
r(A)\le 2.
$$

又因为 $A$ 有 3 个不同的特征值，所以至少有 2 个非零特征值，从而

$$
r(A)\ge 2.
$$

故

$$
r(A)=2.
$$

再由

$$
\alpha_1+2\alpha_2-\alpha_3=0
$$

知

$$
A\begin{pmatrix}1\\2\\-1\end{pmatrix}=0,
$$

所以

$$
\begin{pmatrix}1\\2\\-1\end{pmatrix}
$$

是齐次方程 $Ax=0$ 的一个解。由于 $r(A)=2$，其基础解系恰可取为

$$
\begin{pmatrix}1\\2\\-1\end{pmatrix}.
$$

又因为

$$
\beta=\alpha_1+\alpha_2+\alpha_3=A\begin{pmatrix}1\\1\\1\end{pmatrix},
$$

所以

$$
\begin{pmatrix}1\\1\\1\end{pmatrix}
$$

是方程组 $Ax=\beta$ 的一个特解。

因此通解为

$$
x=\begin{pmatrix}1\\1\\1\end{pmatrix}
+k\begin{pmatrix}1\\2\\-1\end{pmatrix},\qquad k\in\mathbb{R}.
$$

### 第 21 题

#### 标准答案

（1）$a=2$；（2）可取 $Q=\begin{pmatrix} \frac{1}{\sqrt{3}} & -\frac{1}{\sqrt{2}} & \frac{1}{\sqrt{6}} \\ -\frac{1}{\sqrt{3}} & 0 & \frac{2}{\sqrt{6}} \\ \frac{1}{\sqrt{3}} & \frac{1}{\sqrt{2}} & \frac{1}{\sqrt{6}} \end{pmatrix}$，标准形为 $f=-3y_1^2+6y_2^2$

#### 解析

二次型对应矩阵为

$$
A=
\begin{pmatrix}
2&1&-4\\
1&-1&1\\
-4&1&a
\end{pmatrix}.
$$

题设说在正交变换下标准形为 $\lambda_1y_1^2+\lambda_2y_2^2$，说明 $\det A=0$。计算

$$
\det A=6-3a,
$$

所以

$$
a=2.
$$

此时矩阵 $A$ 的特征多项式为

$$
\det(\lambda E-A)=\lambda(\lambda+3)(\lambda-6),
$$

故特征值为 $-3,6,0$。

可分别取对应的单位特征向量为

$$
\beta_1=\frac{1}{\sqrt{3}}(1,-1,1)^T,
\quad
\beta_2=\frac{1}{\sqrt{2}}(-1,0,1)^T,
\quad
\beta_3=\frac{1}{\sqrt{6}}(1,2,1)^T.
$$

于是可取正交矩阵

$$
Q=(\beta_1,\beta_2,\beta_3)
=
\begin{pmatrix}
\frac{1}{\sqrt{3}} & -\frac{1}{\sqrt{2}} & \frac{1}{\sqrt{6}} \\
-\frac{1}{\sqrt{3}} & 0 & \frac{2}{\sqrt{6}} \\
\frac{1}{\sqrt{3}} & \frac{1}{\sqrt{2}} & \frac{1}{\sqrt{6}}
\end{pmatrix}.
$$

在该变换下标准形为

$$
f=-3y_1^2+6y_2^2.
$$

若交换前两个特征向量，得到的 $Q$ 与标准形次序不同，但也是等价正确答案。

### 第 22 题

#### 标准答案

（1）$P\{Y\le E(Y)\}=\dfrac{4}{9}$；（2）$f_Z(z)=\begin{cases} z, & 0<z<1, \\ z-2, & 2<z<3, \\ 0, & \text{其他}. \end{cases}$

#### 解析

由密度函数

$$
f_Y(y)=
\begin{cases}
2y, & 0<y<1,\\
0, & \text{其他}
\end{cases}
$$

先求期望：

$$
EY=\int_0^1 2y^2\,dy=\frac{2}{3}.
$$

因此

$$
P\{Y\le E(Y)\}=P\left\{Y\le \frac{2}{3}\right\}
=\int_0^{2/3}2y\,dy=\frac{4}{9}.
$$

再求 $Z=X+Y$ 的密度。记分布函数为 $F_Z(z)$，则

$$
F_Z(z)=P\{X+Y\le z\}
=P\{X=0\}P\{Y\le z\}+P\{X=2\}P\{Y\le z-2\}.
$$

由于 $P\{X=0\}=P\{X=2\}=\frac{1}{2}$，于是：

当 $z<0$ 时，$F_Z(z)=0$；

当 $0\le z<1$ 时，

$$
F_Z(z)=\frac{1}{2}P\{Y\le z\}=\frac{z^2}{2};
$$

当 $1\le z<2$ 时，

$$
F_Z(z)=\frac{1}{2};
$$

当 $2\le z<3$ 时，

$$
F_Z(z)=\frac{1}{2}+\frac{1}{2}P\{Y\le z-2\}
=\frac{1}{2}+\frac{1}{2}(z-2)^2;
$$

当 $z\ge 3$ 时，$F_Z(z)=1$。

对分布函数分段求导得

$$
f_Z(z)=
\begin{cases}
z, & 0<z<1,\\
z-2, & 2<z<3,\\
0, & \text{其他}.
\end{cases}
$$

### 第 23 题

#### 标准答案

（1）$f_Z(z)=\begin{cases}\sqrt{\dfrac{2}{\pi}}\dfrac{1}{\sigma}e^{-z^2/(2\sigma^2)}, & z\ge 0,\\ 0, & z<0;\end{cases}$ （2）矩估计为 $\hat\sigma=\sqrt{\dfrac{\pi}{2}}\,\overline{Z}$；（3）最大似然估计为 $\hat\sigma=\sqrt{\dfrac{1}{n}\sum_{i=1}^n Z_i^2}$

#### 解析

设 $Z=|X-\mu|$，其中 $X\sim N(\mu,\sigma^2)$。

先求分布函数。当 $z<0$ 时，显然 $F_Z(z)=0$；当 $z\ge 0$ 时，

$$
F_Z(z)=P\{|X-\mu|\le z\}
=P\left\{\left|\frac{X-\mu}{\sigma}\right|\le \frac{z}{\sigma}\right\}
=2\Phi\left(\frac{z}{\sigma}\right)-1.
$$

因此密度函数为

$$
f_Z(z)=
\begin{cases}
\sqrt{\dfrac{2}{\pi}}\dfrac{1}{\sigma}e^{-z^2/(2\sigma^2)}, & z\ge 0,\\
0, & z<0.
\end{cases}
$$

接着求矩估计。由密度可得

$$
EZ=\int_0^{\infty}z\sqrt{\frac{2}{\pi}}\frac{1}{\sigma}e^{-z^2/(2\sigma^2)}dz
=\sqrt{\frac{2}{\pi}}\sigma.
$$

于是

$$
\sigma=\sqrt{\frac{\pi}{2}}EZ.
$$

令

$$
\overline{Z}=\frac{1}{n}\sum_{i=1}^n Z_i,
$$

得到 $\sigma$ 的矩估计量为

$$
\hat\sigma=\sqrt{\frac{\pi}{2}}\,\overline{Z}.
$$

最后求最大似然估计。设样本观测值为 $z_1,z_2,\dots,z_n$，则似然函数

$$
L(\sigma)=\prod_{i=1}^n f(z_i)
=\left(\sqrt{\frac{2}{\pi}}\right)^n\sigma^{-n}
\exp\left(-\frac{1}{2\sigma^2}\sum_{i=1}^n z_i^2\right).
$$

取对数得

$$
\ln L(\sigma)=n\ln\sqrt{\frac{2}{\pi}}-n\ln\sigma-\frac{1}{2\sigma^2}\sum_{i=1}^n z_i^2.
$$

求导并令其为零：

$$
\frac{d\ln L(\sigma)}{d\sigma}
=-\frac{n}{\sigma}+\frac{1}{\sigma^3}\sum_{i=1}^n z_i^2=0.
$$

解得

$$
\hat\sigma=\sqrt{\frac{1}{n}\sum_{i=1}^n z_i^2}.
$$
