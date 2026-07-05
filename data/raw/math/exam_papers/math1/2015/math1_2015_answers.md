# Math 1 2015 Answers

资料类型：考研数学一答案解析
年份：2015
科目：数学一
校对状态：已按题干截图、答案速查图和答案页图像清洗整理

## 答案速查

| 题号 | 题型 | 答案 |
|---|---|---|
| 1 | 选择题 | C |
| 2 | 选择题 | A |
| 3 | 选择题 | B |
| 4 | 选择题 | B |
| 5 | 选择题 | D |
| 6 | 选择题 | A |
| 7 | 选择题 | C |
| 8 | 选择题 | D |
| 9 | 填空题 | $-\frac{1}{2}$ |
| 10 | 填空题 | $\frac{\pi^2}{4}$ |
| 11 | 填空题 | $-dx$ |
| 12 | 填空题 | $\frac{1}{4}$ |
| 13 | 填空题 | $2^{n+1}-2$ |
| 14 | 填空题 | $\frac{1}{2}$ |
| 15 | 解答题 | $a=-1,\ b=-\frac{1}{2},\ k=-\frac{1}{3}$ |
| 16 | 解答题 | $f(x)=\frac{8}{4-x},\ x\in I$ |
| 17 | 解答题 | $3$ |
| 18 | 解答题 | 第 (I) 问证明乘积求导公式；第 (II) 问 $f'(x)=\sum_{i=1}^{n}u_i'(x)\prod_{j\ne i}u_j(x)$。 |
| 19 | 解答题 | $I=\frac{\sqrt{2}}{2}\pi$ |
| 20 | 解答题 | 第 (I) 问 $\beta_1,\beta_2,\beta_3$ 为 $\mathbb R^3$ 的一个基；第 (II) 问当 $k=0$ 时，所有非零向量为 $\xi=c(\alpha_1-\alpha_3)$，其中 $c\ne0$。 |
| 21 | 解答题 | (I) $a=4,\ b=5$；(II) 可取 $P=\begin{pmatrix}-1&2&-3\\-1&1&0\\1&0&1\end{pmatrix}$，此时 $P^{-1}AP=\operatorname{diag}(5,1,1)$。 |
| 22 | 解答题 | (I) $P\{Y=k\}=\frac{1}{64}(k-1)\left(\frac{7}{8}\right)^{k-2},\ k=2,3,\ldots$；(II) $E(Y)=16$。 |
| 23 | 解答题 | (I) $\hat\theta=2\overline X-1$；(II) $\hat\theta=\min\{X_1,X_2,\ldots,X_n\}$。 |

## 详细解析

### 第 1 题

**答案：** C

由 $f''(x)$ 的图形可知，$f''(x)=0$ 的点有两个，另有 $x=0$ 处 $f''(x)$ 不存在。

曲线 $y=f(x)$ 的拐点对应 $f''(x)$ 在该点两侧变号。两个零点中只有一个零点两侧的二阶导数符号相反，因此给出一个拐点。又 $x=0$ 左侧 $f''(x)>0$，右侧 $f''(x)<0$，虽然 $f''(0)$ 不存在，但 $f(x)$ 连续且凹凸性发生改变，所以 $(0,f(0))$ 也是拐点。

故曲线 $y=f(x)$ 共有 $2$ 个拐点，选 C。

### 第 2 题

**答案：** A

题设给出的特解可分解为齐次方程部分和非齐次特解部分：
$$
y=\frac{1}{2}e^{2x}+\left(x-\frac{1}{3}\right)e^x.
$$
其中 $\frac{1}{2}e^{2x}$ 与 $-\frac{1}{3}e^x$ 对应齐次方程的两个特解，故特征根为 $r_1=2,\ r_2=1$。于是
$$
r^2+ar+b=(r-2)(r-1)=r^2-3r+2,
$$
所以 $a=-3,\ b=2$。

原方程化为
$$
y''-3y'+2y=ce^x.
$$
由于 $r=1$ 是齐次方程特征根，$xe^x$ 是右端为 $ce^x$ 时的特解形式。代入 $y=xe^x$，有
$$
y'=(x+1)e^x,\qquad y''=(x+2)e^x,
$$
从而
$$
y''-3y'+2y=[(x+2)-3(x+1)+2x]e^x=-e^x.
$$
故 $c=-1$，选 A。

### 第 3 题

**答案：** B

因为 $\sum a_n$ 条件收敛，所以 $a_n\to0$ 且 $\sum |a_n|$ 发散。对幂级数 $\sum a_nt^n$，由 $a_n\to0$ 可知收敛半径 $R\ge1$；若 $R>1$，则在 $t=1$ 处绝对收敛，与 $\sum a_n$ 条件收敛矛盾。因此 $R=1$。

题中级数可写成
$$
\sum_{n=1}^{\infty}na_n(x-1)^n.
$$
乘以 $n$ 不改变幂级数的收敛半径，所以它关于 $t=x-1$ 的收敛半径仍为 $1$。

当 $x=\sqrt{3}$ 时，$|x-1|=\sqrt{3}-1<1$，故该幂级数收敛；当 $x=3$ 时，$|x-1|=2>1$，故该幂级数发散。选 B。

### 第 4 题

**答案：** B

在第一象限作极坐标变换
$$
x=r\cos\theta,\qquad y=r\sin\theta.
$$
由 $y=x$ 与 $y=\sqrt{3}x$ 得
$$
\frac{\pi}{4}\le \theta\le \frac{\pi}{3}.
$$
又
$$
xy=\frac{1}{2}r^2\sin2\theta.
$$
曲线 $4xy=1$ 给出
$$
r=\frac{1}{\sqrt{2\sin2\theta}},
$$
曲线 $2xy=1$ 给出
$$
r=\frac{1}{\sqrt{\sin2\theta}}.
$$
因此
$$
\iint_D f(x,y)\,dxdy
=\int_{\pi/4}^{\pi/3}\!d\theta
\int_{1/\sqrt{2\sin2\theta}}^{1/\sqrt{\sin2\theta}}
 f(r\cos\theta,r\sin\theta)r\,dr.
$$
选 B。

### 第 5 题

**答案：** D

系数矩阵
$$
A=\begin{pmatrix}
1&1&1\\
1&2&a\\
1&4&a^2
\end{pmatrix}
$$
是 Vandermonde 型矩阵，故
$$
\det A=(2-1)(a-1)(a-2)=(a-1)(a-2).
$$
线性方程组有无穷多解，必须有 $\det A=0$，即 $a=1$ 或 $a=2$。

当 $a=1$ 时，对增广矩阵作初等行变换可化为
$$
(A,b)\sim
\begin{pmatrix}
1&1&1&1\\
0&1&0&d-1\\
0&0&0&(d-1)(d-2)
\end{pmatrix}.
$$
要有 $r(A)=r(A,b)<3$，需 $d=1$ 或 $d=2$。

当 $a=2$ 时同理也得到 $d=1$ 或 $d=2$。因此 $a\in\Omega$ 且 $d\in\Omega$，选 D。

### 第 6 题

**答案：** A

在正交变换 $x=Py$ 下，二次型标准形为
$$
2y_1^2+y_2^2-y_3^2,
$$
即
$$
P^TAP=\operatorname{diag}(2,1,-1).
$$
又 $Q=(e_1,-e_3,e_2)$，相当于在原标准正交基中交换第二、第三个方向，并把第三个方向取负。取负不改变平方项系数，交换后系数顺序变为
$$
2,\ -1,\ 1.
$$
故在 $x=Qy$ 下的标准形为
$$
2y_1^2-y_2^2+y_3^2.
$$
选 A。

### 第 7 题

**答案：** C

对任意事件 $A,B$，总有
$$
P(AB)\le P(A),\qquad P(AB)\le P(B).
$$
两式相加得
$$
2P(AB)\le P(A)+P(B),
$$
即
$$
P(AB)\le \frac{P(A)+P(B)}2.
$$

选项 A、B 只有在附加独立性等条件下才可能判断；选项 D 与上式相反。故选 C。

### 第 8 题

**答案：** D

由于 $X,Y$ 不相关，
$$
\operatorname{Cov}(X,Y)=0,
$$
所以
$$
E(XY)=E(X)E(Y)=2\cdot1=2.
$$
又
$$
E(X^2)=D(X)+[E(X)]^2=3+2^2=7.
$$
因此
$$
E[X(X+Y-2)]=E(X^2+XY-2X)=7+2-4=5.
$$
选 D。

### 第 9 题

**答案：** $-\frac{1}{2}$

当 $x\to0$ 时，
$$
\cos x-1\sim -\frac{x^2}{2},
$$
且 $\ln(1+t)\sim t$。因此
$$
\ln(\cos x)=\ln[1+(\cos x-1)]\sim \cos x-1\sim -\frac{x^2}{2}.
$$
所以
$$
\lim_{x\to0}\frac{\ln(\cos x)}{x^2}=-\frac{1}{2}.
$$

### 第 10 题

**答案：** $\frac{\pi^2}{4}$

由于
$$
\frac{\sin x}{1+\cos x}=\tan\frac{x}{2}
$$
是奇函数，$|x|$ 是偶函数，且积分区间 $[-\frac{\pi}{2},\frac{\pi}{2}]$ 关于原点对称，所以
$$
\int_{-\pi/2}^{\pi/2}\frac{\sin x}{1+\cos x}\,dx=0.
$$
于是
$$
\int_{-\pi/2}^{\pi/2}\left(\frac{\sin x}{1+\cos x}+|x|\right)dx
=2\int_0^{\pi/2}x\,dx
=\frac{\pi^2}{4}.
$$

### 第 11 题

**答案：** $-dx$

令
$$
F(x,y,z)=e^z+xyz+x+
\cos x-2.
$$
由 $F(0,1,z)=0$ 得 $e^z=1$，故 $z=0$。又
$$
F_x=yz+1-\sin x,\qquad F_y=xz,\qquad F_z=e^z+xy.
$$
由隐函数求导公式，
$$
z_x=-\frac{F_x}{F_z},\qquad z_y=-\frac{F_y}{F_z}.
$$
代入 $(x,y,z)=(0,1,0)$ 得
$$
z_x(0,1)=-1,
\qquad z_y(0,1)=0.
$$
因此
$$
dz\big|_{(0,1)}=z_x(0,1)dx+z_y(0,1)dy=-dx.
$$

### 第 12 题

**答案：** $\frac{1}{4}$

区域 $\Omega$ 是由 $x,y,z\ge0$ 与 $x+y+z\le1$ 围成的四面体。由轮换对称性，
$$
\iiint_\Omega x\,dV=\iiint_\Omega y\,dV=\iiint_\Omega z\,dV.
$$
因此
$$
\iiint_\Omega (x+2y+3z)\,dV
=6\iiint_\Omega x\,dV.
$$
直接积分：
$$
\iiint_\Omega x\,dV
=\int_0^1\int_0^{1-x}\int_0^{1-x-y}x\,dz\,dy\,dx
=\int_0^1\int_0^{1-x}x(1-x-y)\,dy\,dx
=\frac{1}{24}.
$$
故所求积分为
$$
6\cdot\frac{1}{24}=\frac{1}{4}.
$$

### 第 13 题

**答案：** $2^{n+1}-2$

记该 $n$ 阶行列式为 $D_n$。从第 $1$ 行开始，依次将第 $i$ 行的 $\frac{1}{2}$ 倍加到第 $i+1$ 行，$i=1,2,\ldots,n-1$。这些初等行变换不改变行列式的值，并把主对角线下方的 $-1$ 消去。

变换后矩阵成为上三角型，前 $n-1$ 个对角元均为 $2$，最后一个对角元为
$$
2\left[1+\frac{1}{2}+\left(\frac{1}{2}\right)^2+\cdots+\left(\frac{1}{2}\right)^{n-1}\right]
=4\left(1-2^{-n}\right).
$$
因此
$$
D_n=2^{n-1}\cdot4\left(1-2^{-n}\right)=2^{n+1}-2.
$$

### 第 14 题

**答案：** $\frac{1}{2}$

由题意，$X,Y$ 服从二维正态分布，且相关系数为 $0$，所以 $X$ 与 $Y$ 相互独立。其中
$$
X\sim N(1,1),\qquad Y\sim N(0,1),
$$
故 $X-1$ 与 $Y$ 是相互独立的标准正态随机变量。

因为
$$
XY-Y=(X-1)Y,
$$
所以
$$
\begin{aligned}
P\{XY-Y<0\}
&=P\{(X-1)Y<0\}\\
&=P\{X-1<0,Y>0\}+P\{X-1>0,Y<0\}\\
&=\frac{1}{2}\cdot\frac{1}{2}+\frac{1}{2}\cdot\frac{1}{2}=\frac{1}{2}.
\end{aligned}
$$

### 第 15 题

**答案：** $a=-1,\ b=-\frac{1}{2},\ k=-\frac{1}{3}$

当 $x\to0$ 时，
$$
\ln(1+x)=x-\frac{x^2}{2}+\frac{x^3}{3}+o(x^3),
\qquad
\sin x=x-\frac{x^3}{6}+o(x^3).
$$
于是
$$
\begin{aligned}
f(x)
&=x+a\ln(1+x)+bx\sin x\\
&=x+a\left(x-\frac{x^2}{2}+\frac{x^3}{3}\right)+bx^2+o(x^3)\\
&=(1+a)x+\left(b-\frac{a}{2}\right)x^2+\frac{a}{3}x^3+o(x^3).
\end{aligned}
$$

因为 $f(x)$ 与 $g(x)=kx^3$ 在 $x\to0$ 时为等价无穷小，必须有
$$
1+a=0,
\qquad b-\frac{a}{2}=0,
\qquad k=\frac{a}{3}.
$$
解得
$$
a=-1,
\qquad b=-\frac{1}{2},
\qquad k=-\frac{1}{3}.
$$

### 第 16 题

**答案：** $f(x)=\frac{8}{4-x},\ x\in I$

曲线 $y=f(x)$ 在点 $(x_0,f(x_0))$ 处的切线为
$$
y=f'(x_0)(x-x_0)+f(x_0).
$$
它与 $x$ 轴的交点为
$$
\left(x_0-\frac{f(x_0)}{f'(x_0)},0\right).
$$
由 $f'(x)>0$，所围三角形面积为
$$
\frac{1}{2}\left|\frac{f(x_0)}{f'(x_0)}\right|\cdot |f(x_0)|=4.
$$
因此
$$
[f(x_0)]^2=8f'(x_0).
$$
即函数满足微分方程
$$
y'=\frac{1}{8}y^2.
$$
分离变量得
$$
-\frac{1}{y}=\frac{x}{8}+C,
$$
所以
$$
y=-\frac{8}{x+8C}.
$$
由 $f(0)=2$ 得 $C=-\frac{1}{2}$，故
$$
f(x)=\frac{8}{4-x},\qquad x\in I.
$$

### 第 17 题

**答案：** $3$

函数在某点的最大方向导数等于该点梯度向量的模。由
$$
f(x,y)=x+y+xy
$$
得
$$
\nabla f(x,y)=(1+y,1+x),
\qquad
|\nabla f(x,y)|=\sqrt{(1+x)^2+(1+y)^2}.
$$
因此问题转化为在约束
$$
x^2+y^2+xy=3
$$
下求 $(1+x)^2+(1+y)^2$ 的最大值。

构造
$$
F(x,y,\lambda)=(1+x)^2+(1+y)^2+\lambda(x^2+y^2+xy-3).
$$
由
$$
\begin{cases}
2(1+x)+\lambda(2x+y)=0,\\
2(1+y)+\lambda(2y+x)=0,\\
x^2+y^2+xy=3
\end{cases}
$$
解得候选点
$$
(1,1),\quad (-1,-1),\quad (2,-1),\quad (-1,2).
$$
对应梯度模分别为
$$
2\sqrt{2},
\quad 0,
\quad 3,
\quad 3.
$$
所以最大方向导数为 $3$。

### 第 18 题

**答案：** 第 (I) 问证明乘积求导公式；第 (II) 问 $f'(x)=\sum_{i=1}^{n}u_i'(x)\prod_{j\ne i}u_j(x)$。

(I) 由导数定义，
$$
[u(x)v(x)]'
=\lim_{\Delta x\to0}\frac{u(x+\Delta x)v(x+\Delta x)-u(x)v(x)}{\Delta x}.
$$
将分子拆成两部分：
$$
\begin{aligned}
&u(x+\Delta x)v(x+\Delta x)-u(x)v(x)\\
&=[u(x+\Delta x)-u(x)]v(x+\Delta x)+u(x)[v(x+\Delta x)-v(x)].
\end{aligned}
$$
于是
$$
\begin{aligned}
[u(x)v(x)]'
&=\lim_{\Delta x\to0}\frac{u(x+\Delta x)-u(x)}{\Delta x}v(x+\Delta x)\\
&\quad +u(x)\lim_{\Delta x\to0}\frac{v(x+\Delta x)-v(x)}{\Delta x}\\
&=u'(x)v(x)+u(x)v'(x).
\end{aligned}
$$

(II) 对 $f(x)=u_1(x)u_2(x)\cdots u_n(x)$，逐次使用乘积求导法则，得
$$
f'(x)=\sum_{i=1}^{n}u_i'(x)\prod_{\substack{1\le j\le n\\ j\ne i}}u_j(x).
$$

### 第 19 题

**答案：** $I=\frac{\sqrt{2}}{2}\pi$

设 $L_1$ 为从 $B(0,-\sqrt{2},0)$ 到 $A(0,\sqrt{2},0)$ 的直线段。曲线 $L$ 与 $L_1$ 围成平面 $z=x$ 上的半圆面 $\Sigma$，取与边界方向相容的法向量
$$
\boldsymbol n=\left(\frac{1}{\sqrt{2}},0,-\frac{1}{\sqrt{2}}\right).
$$
记
$$
P=y+z,
\qquad Q=z^2-x^2+y,
\qquad R=x^2y^2.
$$
由 Stokes 公式，
$$
\oint_{L+L_1}P\,dx+Q\,dy+R\,dz
=\iint_\Sigma (\nabla\times(P,Q,R))\cdot\boldsymbol n\,dS.
$$
计算得在平面 $z=x$ 上
$$
(\nabla\times(P,Q,R))\cdot\boldsymbol n
=\frac{1}{\sqrt{2}}(2x^2y+1).
$$
半圆面 $\Sigma$ 关于 $xOz$ 平面对称，故
$$
\iint_\Sigma 2x^2y\,dS=0.
$$
又该半圆面的半径为 $\sqrt{2}$，面积为 $\pi$，所以
$$
\oint_{L+L_1}P\,dx+Q\,dy+R\,dz
=\frac{1}{\sqrt{2}}\pi.
$$

在线段 $L_1$ 上，$x=0,\ z=0$，且 $y$ 从 $-\sqrt{2}$ 到 $\sqrt{2}$，故
$$
\int_{L_1}P\,dx+Q\,dy+R\,dz=\int_{-\sqrt{2}}^{\sqrt{2}}y\,dy=0.
$$
因此
$$
I=\int_LP\,dx+Q\,dy+R\,dz=\frac{\sqrt{2}}{2}\pi.
$$

### 第 20 题

**答案：** 第 (I) 问 $\beta_1,\beta_2,\beta_3$ 为 $\mathbb R^3$ 的一个基；第 (II) 问当 $k=0$ 时，所有非零向量为 $\xi=c(\alpha_1-\alpha_3)$，其中 $c\ne0$。

(I) 由题设，
$$
(\beta_1,\beta_2,\beta_3)=(\alpha_1,\alpha_2,\alpha_3)P,
$$
其中
$$
P=\begin{pmatrix}
2&0&1\\
0&2&0\\
2k&0&k+1
\end{pmatrix}.
$$
计算行列式得
$$
\det P=4\ne0.
$$
因为 $\alpha_1,\alpha_2,\alpha_3$ 是 $\mathbb R^3$ 的一个基，且 $P$ 可逆，所以 $\beta_1,\beta_2,\beta_3$ 也是 $\mathbb R^3$ 的一个基。

(II) 设同一个非零向量 $\xi$ 在两组基下的坐标向量都为 $x$，则
$$
\xi=(\alpha_1,\alpha_2,\alpha_3)x=(\beta_1,\beta_2,\beta_3)x=(\alpha_1,\alpha_2,\alpha_3)Px.
$$
由于 $(\alpha_1,\alpha_2,\alpha_3)$ 可逆，需有
$$
(P-E)x=0.
$$
而
$$
P-E=\begin{pmatrix}
1&0&1\\
0&1&0\\
2k&0&k
\end{pmatrix}
\sim
\begin{pmatrix}
1&0&1\\
0&1&0\\
0&0&-k
\end{pmatrix}.
$$
该齐次方程组有非零解当且仅当 $k=0$。此时
$$
x=c\begin{pmatrix}1\\0\\-1\end{pmatrix},\qquad c\ne0.
$$
故所有满足条件的非零向量为
$$
\xi=(\alpha_1,\alpha_2,\alpha_3)x=c(\alpha_1-\alpha_3),\qquad c\ne0.
$$

### 第 21 题

**答案：** (I) $a=4,\ b=5$；(II) 可取 $P=\begin{pmatrix}-1&2&-3\\-1&1&0\\1&0&1\end{pmatrix}$，此时 $P^{-1}AP=\operatorname{diag}(5,1,1)$。

(I) 相似矩阵有相同的迹和行列式。由
$$
\operatorname{tr}(A)=\operatorname{tr}(B),
\qquad \det A=\det B
$$
得
$$
3+a=2+b,
\qquad 2a-3=b.
$$
解得
$$
a=4,
\qquad b=5.
$$

(II) 此时
$$
A=\begin{pmatrix}
0&2&-3\\
-1&3&-3\\
1&-2&4
\end{pmatrix},
\qquad
B=\begin{pmatrix}
1&-2&0\\
0&5&0\\
0&3&1
\end{pmatrix}.
$$
由于 $A$ 与 $B$ 相似，且 $B$ 的特征多项式为
$$
(\lambda-1)^2(\lambda-5),
$$
所以 $A$ 的特征值为 $5,1,1$。

对 $\lambda=5$，可取特征向量
$$
\xi_1=(-1,-1,1)^T.
$$
对 $\lambda=1$，可取两个线性无关的特征向量
$$
\xi_2=(2,1,0)^T,
\qquad
\xi_3=(-3,0,1)^T.
$$
令
$$
P=(\xi_1,\xi_2,\xi_3)=
\begin{pmatrix}
-1&2&-3\\
-1&1&0\\
1&0&1
\end{pmatrix}.
$$
则 $P$ 可逆，并且
$$
P^{-1}AP=
\begin{pmatrix}
5&0&0\\
0&1&0\\
0&0&1
\end{pmatrix}.
$$

### 第 22 题

**答案：** (I) $P\{Y=k\}=\frac{1}{64}(k-1)\left(\frac{7}{8}\right)^{k-2},\ k=2,3,\ldots$；(II) $E(Y)=16$。

每次观测中，观测值大于 $3$ 的概率为
$$
p=P\{X>3\}=\int_3^{+\infty}2^{-x}\ln2\,dx=2^{-3}=\frac{1}{8}.
$$

(I) $Y$ 表示第 $2$ 个“大于 $3$”的观测值出现时的观测次数。因此当 $Y=k$ 时，前 $k-1$ 次观测中恰有 $1$ 次大于 $3$，且第 $k$ 次大于 $3$。于是
$$
P\{Y=k\}=\binom{k-1}{1}p^2(1-p)^{k-2}
=(k-1)\left(\frac{1}{8}\right)^2\left(\frac{7}{8}\right)^{k-2},
\qquad k=2,3,\ldots.
$$
即
$$
P\{Y=k\}=\frac{1}{64}(k-1)\left(\frac{7}{8}\right)^{k-2},
\qquad k=2,3,\ldots.
$$

(II) 这是等待第 $2$ 次成功的负二项分布，故
$$
E(Y)=\frac{2}{p}=\frac{2}{1/8}=16.
$$

### 第 23 题

**答案：** (I) $\hat\theta=2\overline X-1$；(II) $\hat\theta=\min\{X_1,X_2,\ldots,X_n\}$。

(I) 总体 $X$ 在区间 $[\theta,1]$ 上服从均匀分布，因此
$$
E(X)=\frac{1+\theta}{2}.
$$
令 $E(X)$ 等于样本均值 $\overline X$，得
$$
\frac{1+\theta}{2}=\overline X.
$$
所以 $\theta$ 的矩估计量为
$$
\hat\theta=2\overline X-1.
$$

(II) 设样本观测值为 $x_1,x_2,\ldots,x_n$。似然函数为
$$
L(\theta)=\prod_{i=1}^n f(x_i;\theta)
=\begin{cases}
\dfrac{1}{(1-\theta)^n},& \theta\le x_i\le1\ (i=1,2,\ldots,n),\\
0,&\text{其他}.
\end{cases}
$$
也即
$$
L(\theta)=\begin{cases}
\dfrac{1}{(1-\theta)^n},& \theta\le \min\{x_1,x_2,\ldots,x_n\},\\
0,&\text{其他}.
\end{cases}
$$
在允许范围内，$\frac{1}{(1-\theta)^n}$ 随 $\theta$ 增大而增大，因此似然函数在
$$
\theta=\min\{x_1,x_2,\ldots,x_n\}
$$
处达到最大。故最大似然估计量为
$$
\hat\theta=\min\{X_1,X_2,\ldots,X_n\}.
$$
