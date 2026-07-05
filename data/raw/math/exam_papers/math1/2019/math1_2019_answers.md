# Math 1 2019 Answers

资料类型：考研数学一真题答案解析
年份：2019
科目：数学一
校对状态：reviewed

## 选择题

| 题号 | 标准答案 |
|---|---|
| 1 | C |
| 2 | B |
| 3 | D |
| 4 | D |
| 5 | C |
| 6 | A |
| 7 | C |
| 8 | A |

## 填空题

| 题号 | 标准答案 |
|---|---|
| 9 | $\dfrac{y}{\cos x}+\dfrac{x}{\cos y}$ |
| 10 | $\sqrt{3e^x-2}$ |
| 11 | $\cos\sqrt{x}$ |
| 12 | $\dfrac{32}{3}$ |
| 13 | $x=k(1,-2,1)^T,\ k\in\mathbb{R}$ |
| 14 | $\dfrac{2}{3}$ |

## 解答题

| 题号 | 标准答案 |
|---|---|
| 15 | 1. $y(x)=xe^{-x^2/2}$<br>2. 凹区间：$(-\infty,-\sqrt{3})\cup(0,\sqrt{3})$；凸区间：$(-\sqrt{3},0)\cup(\sqrt{3},+\infty)$；拐点：$(-\sqrt{3},-\sqrt{3}e^{-3/2})$、$(0,0)$、$(\sqrt{3},\sqrt{3}e^{-3/2})$。 |
| 16 | 1. $a=-1,\ b=-1$<br>2. $S=\dfrac{13\pi}{3}$ |
| 17 | $\dfrac{1}{2}+\dfrac{1}{e^{\pi}-1}$ |
| 18 | 1. $\{a_n\}$ 单调递减，且 $a_n=\dfrac{n-1}{n+2}a_{n-2}\ (n\ge 2)$<br>2. $\displaystyle \lim_{n\to\infty}\frac{a_n}{a_{n-1}}=1$ |
| 19 | $(0,\tfrac{1}{4},\tfrac{1}{4})$ |
| 20 | 1. $a=3,\ b=2,\ c=-2$<br>2. $C=\begin{pmatrix}1&1&0\\-\tfrac{1}{2}&0&1\\\tfrac{1}{2}&0&0\end{pmatrix}$ |
| 21 | 1. $x=3,\ y=-2$<br>2. $P=\begin{pmatrix}-1&-1&-1\\2&1&2\\0&0&4\end{pmatrix}$ |
| 22 | 1. $f_Z(z)=\begin{cases}pe^z,&z<0,\\(1-p)e^{-z},&z\ge 0\end{cases}$<br>2. $p=\dfrac{1}{2}$<br>3. $X$ 与 $Z$ 不独立 |
| 23 | 1. $A=\sqrt{\dfrac{2}{\pi}}$<br>2. $\hat\sigma^2=\dfrac{1}{n}\sum_{i=1}^n(X_i-\mu)^2$ |

## 详细解析

### 第 1 题

#### 标准答案

C

#### 解析

由麦克劳林展开式

$$
\tan x = x + \frac{x^3}{3} + o(x^3)
$$

可得

$$
x - \tan x = -\frac{x^3}{3} + o(x^3),
$$

因此 $x-\tan x$ 与 $x^3$ 是同阶无穷小，故 $k=3$，选 C。

### 第 2 题

#### 标准答案

B

#### 解析

先看 $x=0$ 处的右导数：

$$
f'_+(0)=\lim_{x\to 0^+}\frac{f(x)-f(0)}{x}=\lim_{x\to 0^+}\ln x
$$

该极限不存在，所以 $x=0$ 是不可导点。又因为 $f(0)=0$，且在 $x=0$ 的左右邻域内都有 $f(x)<0$，所以 $x=0$ 是极大值点，故选 B。

### 第 3 题

#### 标准答案

D

#### 解析

取 $u_n=-\dfrac{1}{\ln n}$，则 $\sum \dfrac{u_n}{n}$ 发散，所以 A 错。若 $\sum (-1)^n\dfrac{1}{u_n}$ 收敛，由莱布尼茨判别法应有 $\dfrac{1}{u_n}$ 单调递减趋于零；但题设下 $\{u_n\}$ 是单调增加的有界数列，故 $\dfrac{1}{u_n}$ 不可能满足这一条件，所以 B 错。再取 $u_n=-\dfrac{1}{n}$，则对应级数仍发散，所以 C 错。

对 D，利用裂项：

$$
\sum_{n=1}^{\infty}(u_{n+1}^2-u_n^2)
=(u_2^2-u_1^2)+(u_3^2-u_2^2)+\cdots
=\lim_{n\to\infty}(u_{n+1}^2-u_1^2).
$$

因 $\{u_n\}$ 有界且极限存在，上式收敛，故选 D。

### 第 4 题

#### 标准答案

D

#### 解析

曲线积分与路径无关的必要条件是

$$
\frac{\partial P}{\partial y}=\frac{\partial Q}{\partial x}.
$$

由此可先排除 A、B。对 C，在 $x=0$ 处不连续，不满足条件，因此只能选 D。

### 第 5 题

#### 标准答案

C

#### 解析

设 $\lambda$ 是矩阵 $A$ 的特征值。由

$$
A^2+A=2E
$$

得

$$
\lambda^2+\lambda=2,
$$

所以 $\lambda=1$ 或 $\lambda=-2$。又因 $A$ 是 $3$ 阶实对称矩阵，三特征值之积等于 $\det A$，从而 $A$ 的三个特征值为 $1,-2,-2$。因此二次型 $x^TAx$ 的规范形有 $1$ 个正平方项、$2$ 个负平方项，即

$$
y_1^2-y_2^2-y_3^2,
$$

故选 C。

### 第 6 题

#### 标准答案

A

#### 解析

三张平面没有公共交线，说明非齐次方程组 $Ax=b$ 无解，因此

$$
r(A)<r(\overline{A}),
$$

可排除 B、D。又因为三平面两两相交且交线互相平行，所以齐次方程组 $Ax=0$ 只有一个线性无关解，从而

$$
r(A)=2.
$$

故选 A。

### 第 7 题

#### 标准答案

C

#### 解析

由题给关系

$$
P(A\overline{B})=P(B\overline{A})
$$

可得

$$
P(A)-P(AB)=P(B)-P(AB),
$$

从而

$$
P(A)=P(B).
$$

故选 C。

### 第 8 题

#### 标准答案

A

#### 解析

由 $X\sim N(\mu,\sigma^2)$、$Y\sim N(\mu,\sigma^2)$ 且相互独立，得

$$
E(X-Y)=0,\quad D(X-Y)=DX+DY=2\sigma^2.
$$

所以

$$
\frac{X-Y}{\sqrt{2}\sigma}\sim N(0,1).
$$

于是

$$
P(|X-Y|<1)=P\!\left(\left|\frac{X-Y}{\sqrt{2}\sigma}\right|<\frac{1}{\sqrt{2}\sigma}\right)=2\Phi\!\left(\frac{1}{\sqrt{2}\sigma}\right)-1.
$$

该概率与 $\sigma^2$ 有关、与 $\mu$ 无关，故选 A。

### 第 9 题

#### 标准答案

$\dfrac{y}{\cos x}+\dfrac{x}{\cos y}$

#### 解析

由题设关系分别对 $x,y$ 求偏导，可得

$$
\frac{\partial z}{\partial x}=-\cos x\,f'+y,\qquad \frac{\partial z}{\partial y}=\cos y\,f'+x.
$$

因此

$$
\frac{1}{\cos x}\frac{\partial z}{\partial x}+\frac{1}{\cos y}\frac{\partial z}{\partial y}=\frac{y}{\cos x}+\frac{x}{\cos y}.
$$

故应填 $\dfrac{y}{\cos x}+\dfrac{x}{\cos y}$。

### 第 10 题

#### 标准答案

$\sqrt{3e^x-2}$

#### 解析

由方程可整理为

$$
2yy'-y^2-2=0,
$$

于是

$$
\frac{dy}{dx}=\frac{y^2+2}{2y},\qquad \frac{2y}{y^2+2}\,dy=dx.
$$

积分得

$$
y^2+2=ce^x.
$$

再由初值 $y(0)=1$ 得 $c=3$，所以特解为

$$
y=\sqrt{3e^x-2}.
$$

### 第 11 题

#### 标准答案

$\cos\sqrt{x}$

#### 解析

利用余弦级数展开：

$$
\sum_{n=0}^{\infty}\frac{(-1)^n}{(2n)!}x^n=\sum_{n=0}^{\infty}\frac{(-1)^n}{(2n)!}(\sqrt{x})^{2n}=\cos\sqrt{x}.
$$

故应填 $\cos\sqrt{x}$。

### 第 12 题

#### 标准答案

$\dfrac{32}{3}$

#### 解析

将曲面方程代入积分表达式，原积分化为

$$
\iint_{\Sigma}|y|\,dx\,dy.
$$

曲面关于 $xOz$ 平面对称，所以

$$
\iint_{\Sigma}|y|\,dx\,dy=2\iint_{D_{xy}}y\,dx\,dy,
$$

其中 $D_{xy}$ 为右半侧在 $xOy$ 平面上的投影。改用极坐标计算：

$$
2\int_0^{\pi}\!d\theta\int_0^2 r^2\sin\theta\,dr=\frac{32}{3}.
$$

故应填 $\dfrac{32}{3}$。

### 第 13 题

#### 标准答案

$x=k(1,-2,1)^T,\ k\in\mathbb{R}$

#### 解析

先求矩阵 $A$ 的秩。由 $\alpha_1,\alpha_2$ 线性无关知 $r(A)\ge 2$；又由

$$
\alpha_3=-\alpha_1+2\alpha_2
$$

知 $r(A)\le 2$，故 $r(A)=2$。因此 $Ax=0$ 的基础解系中只含一个向量。

再由

$$
A\begin{pmatrix}1\\-2\\1\end{pmatrix}=\alpha_1-2\alpha_2+\alpha_3=0,
$$

可知 $\bigl(1,-2,1\bigr)^T$ 就是一个基础解，所以通解为

$$
x=k(1,-2,1)^T,\quad k\in\mathbb{R}.
$$

### 第 14 题

#### 标准答案

$\dfrac{2}{3}$

#### 解析

由概率密度

$$
f(x)=\begin{cases}\dfrac{x}{2},&0<x<2,\\0,&\text{其他},\end{cases}
$$

得分布函数

$$
F(x)=\begin{cases}0,&x<0,\\\dfrac{x^2}{4},&0\le x<2,\\1,&x\ge 2.\end{cases}
$$

并且

$$
EX=\int_0^2 x\cdot\frac{x}{2}\,dx=\frac{4}{3}.
$$

所以

$$
P\{F(X)>EX-1\}=P\left\{\frac{X^2}{4}>\frac{1}{3}\right\}=P\left\{X>\frac{2}{\sqrt{3}}\right\}
$$

$$
=\int_{2/\sqrt{3}}^2\frac{x}{2}\,dx=\frac{2}{3}.
$$

### 第 15 题

#### 标准答案

1. $y(x)=xe^{-x^2/2}$
2. 凹区间：$(-\infty,-\sqrt{3})\cup(0,\sqrt{3})$；凸区间：$(-\sqrt{3},0)\cup(\sqrt{3},+\infty)$；拐点：$(-\sqrt{3},-\sqrt{3}e^{-3/2})$、$(0,0)$、$(\sqrt{3},\sqrt{3}e^{-3/2})$。

#### 解析

这是一个一阶线性微分方程。用公式法得通解

$$
y=e^{-\int x\,dx}\left(\int e^{\int x\,dx}e^{-x^2/2}\,dx+C\right)=(x+C)e^{-x^2/2}.
$$

由 $y(0)=0$ 得 $C=0$，所以

$$
y=xe^{-x^2/2}.
$$

再求导：

$$
y'=(1-x^2)e^{-x^2/2},\qquad y''=x(x^2-3)e^{-x^2/2}.
$$

令 $y''=0$，得 $x=0,\pm\sqrt{3}$。由 $y''$ 的符号变化可知，凹区间为

$$
(-\infty,-\sqrt{3})\cup(0,\sqrt{3}),
$$

凸区间为

$$
(-\sqrt{3},0)\cup(\sqrt{3},+\infty).
$$

对应拐点为

$$
(-\sqrt{3},-\sqrt{3}e^{-3/2}),\quad (0,0),\quad (\sqrt{3},\sqrt{3}e^{-3/2}).
$$

### 第 16 题

#### 标准答案

1. $a=-1,\ b=-1$
2. $S=\dfrac{13\pi}{3}$

#### 解析

由

$$
z=2+ax^2+by^2
$$

得

$$
\frac{\partial z}{\partial x}=2ax,\qquad \frac{\partial z}{\partial y}=2by.
$$

在点 $(3,4)$ 处，梯度方向为 $(6a,8b)$。题设说沿方向 $l=-3\mathbf{i}-4\mathbf{j}$ 的方向导数最大，所以梯度与 $(-3,-4)$ 同向，故

$$
\frac{6a}{-3}=\frac{8b}{-4},
$$

从而 $a=b$，且因方向向量指向第三象限，得 $a<0,b<0$。又最大方向导数为 $10$，故

$$
6a\left(-\frac{3}{5}\right)+8b\left(-\frac{4}{5}\right)=10,
$$

解得 $a=b=-1$。

于是曲面为

$$
z=2-x^2-y^2\quad(z\ge 0).
$$

其面积为第一类曲面积分：

$$
S=\iint_D\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}\,dxdy
=\iint_D\sqrt{1+4x^2+4y^2}\,dxdy,
$$

其中 $D=\{(x,y)\mid x^2+y^2\le 2\}$。化为极坐标：

$$
S=\int_0^{2\pi}d\theta\int_0^{\sqrt{2}}r\sqrt{1+4r^2}\,dr=\frac{13\pi}{3}.
$$

### 第 17 题

#### 标准答案

$\dfrac{1}{2}+\dfrac{1}{e^{\pi}-1}$

#### 解析

所求面积为

$$
S=\int_0^{+\infty}e^{-x}|\sin x|\,dx=\sum_{n=0}^{\infty}(-1)^n\int_{n\pi}^{(n+1)\pi}e^{-x}\sin x\,dx.
$$

而

$$
\int e^{-x}\sin x\,dx=-\frac{1}{2}e^{-x}(\sin x+\cos x),
$$

故

$$
\int_{n\pi}^{(n+1)\pi}e^{-x}\sin x\,dx=\frac{(-1)^n}{2}\bigl[e^{-n\pi}+e^{-(n+1)\pi}\bigr].
$$

代回求和得

$$
S=\frac{1}{2}\sum_{n=0}^{\infty}\bigl[e^{-n\pi}+e^{-(n+1)\pi}\bigr]
=\frac{e^{\pi}+1}{2(e^{\pi}-1)}
=\frac{1}{2}+\frac{1}{e^{\pi}-1}.
$$

### 第 18 题

#### 标准答案

1. $\{a_n\}$ 单调递减，且 $a_n=\dfrac{n-1}{n+2}a_{n-2}\ (n\ge 2)$
2. $\displaystyle \lim_{n\to\infty}\frac{a_n}{a_{n-1}}=1$

#### 解析

由

$$
a_{n+1}-a_n=\int_0^1 x^n(x-1)\sqrt{1-x^2}\,dx
$$

可知在区间 $[0,1]$ 上 integrand 恒不大于零且不恒为零，因此 $a_{n+1}-a_n<0$，故 $\{a_n\}$ 单调递减。

当 $n\ge 2$ 时，对

$$
a_n=\int_0^1 x^n\sqrt{1-x^2}\,dx
$$

作分部积分，得

$$
a_n=\frac{n-1}{3}\int_0^1 x^{n-2}(1-x^2)^{3/2}\,dx
=\frac{n-1}{3}a_{n-2}-\frac{n-1}{3}a_n,
$$

从而

$$
a_n=\frac{n-1}{n+2}a_{n-2}.
$$

于是

$$
\frac{a_n}{a_{n-1}}=\frac{n-1}{n+2}\cdot\frac{a_{n-2}}{a_{n-1}}.
$$

因为 $\{a_n\}$ 单调递减且 $a_n>0$，所以

$$
\frac{n-1}{n+2}<\frac{a_n}{a_{n-1}}<1.
$$

由夹逼定理得

$$
\lim_{n\to\infty}\frac{a_n}{a_{n-1}}=1.
$$

### 第 19 题

#### 标准答案

$(0,\tfrac{1}{4},\tfrac{1}{4})$

#### 解析

设形心坐标为 $(\bar x,\bar y,\bar z)$。由于区域 $\Omega$ 关于 $yOz$ 平面对称，所以

$$
\bar x=0.
$$

再用先二后一法计算体积：

$$
\iiint_{\Omega}dV=\int_0^1dz\iint_{x^2+(y-z)^2\le (1-z)^2}dxdy=\pi\int_0^1(1-z)^2\,dz=\frac{\pi}{3}.
$$

对 $z$ 的矩：

$$
\iiint_{\Omega}z\,dV=\int_0^1dz\iint_{x^2+(y-z)^2\le (1-z)^2}z\,dxdy=\frac{\pi}{12},
$$

故

$$
\bar z=\frac{\iiint_{\Omega}z\,dV}{\iiint_{\Omega}dV}=\frac{1}{4}.
$$

对 $y$ 的矩，令 $u=y-z$，则

$$
\iint y\,dxdy=\iint (u+z)\,dxdu=\iint z\,dxdu=\pi z(1-z)^2,
$$

从而

$$
\iiint_{\Omega}y\,dV=\int_0^1\pi z(1-z)^2\,dz=\frac{\pi}{12}.
$$

所以

$$
\bar y=\frac{\iiint_{\Omega}y\,dV}{\iiint_{\Omega}dV}=\frac{1}{4}.
$$

故形心为

$$
(0,\tfrac{1}{4},\tfrac{1}{4}).
$$

### 第 20 题

#### 标准答案

1. $a=3,\ b=2,\ c=-2$
2. $C=\begin{pmatrix}1&1&0\\-\tfrac{1}{2}&0&1\\\tfrac{1}{2}&0&0\end{pmatrix}$

#### 解析

由题意

$$
\beta=b\alpha_1+c\alpha_2+\alpha_3,
$$

代入坐标得

$$
\begin{cases}
b+c+1=1,\\
2b+3c+a=1,\\
b+2c+3=1,
\end{cases}
$$

解得

$$
a=3,\quad b=2,\quad c=-2.
$$

再看向量组 $\alpha_2,\alpha_3,\beta$：

$$
|\alpha_2,\alpha_3,\beta|=
\begin{vmatrix}
1&1&1\\
3&3&1\\
2&3&1
\end{vmatrix}=2\ne 0,
$$

因此它们线性无关，构成 $\mathbb{R}^3$ 的一组基。

设过渡矩阵为 $C$，则

$$
(\alpha_1,\alpha_2,\alpha_3)=(\alpha_2,\alpha_3,\beta)C.
$$

于是

$$
C=(\alpha_2,\alpha_3,\beta)^{-1}(\alpha_1,\alpha_2,\alpha_3)
=\frac{1}{2}
\begin{pmatrix}
2&2&0\\
-1&0&2\\
1&0&0
\end{pmatrix}
=
\begin{pmatrix}
1&1&0\\
-\tfrac{1}{2}&0&1\\
\tfrac{1}{2}&0&0
\end{pmatrix}.
$$

### 第 21 题

#### 标准答案

1. $x=3,\ y=-2$
2. $P=\begin{pmatrix}-1&-1&-1\\2&1&2\\0&0&4\end{pmatrix}$

#### 解析

因为矩阵 $A$ 与 $B$ 相似，所以

$$
\operatorname{tr}(A)=\operatorname{tr}(B),\qquad \det A=\det B.
$$

由此得到

$$
\begin{cases}
x-4=y+1,\\
4x-8=-2y,
\end{cases}
$$

解得

$$
x=3,\qquad y=-2.
$$

此时矩阵 $B$ 的特征多项式为

$$
\det(\lambda E-B)=(\lambda-2)(\lambda+1)(\lambda+2),
$$

所以特征值为 $2,-1,-2$。相似矩阵特征值相同，故 $A$ 的特征值也为 $2,-1,-2$。

分别求得 $A$ 的对应特征向量可取

$$
\xi_1=(1,-2,0)^T,\quad \xi_2=(-2,1,0)^T,\quad \xi_3=(1,-2,-4)^T.
$$

因此

$$
P_1=(\xi_1,\xi_2,\xi_3),\qquad P_1^{-1}AP_1=\operatorname{diag}(2,-1,-2).
$$

同理，$B$ 的对应特征向量可取

$$
\eta_1=(1,0,0)^T,\quad \eta_2=(1,-3,0)^T,\quad \eta_3=(0,0,1)^T,
$$

于是

$$
P_2=(\eta_1,\eta_2,\eta_3),\qquad P_2^{-1}BP_2=\operatorname{diag}(2,-1,-2).
$$

由 $P_1^{-1}AP_1=P_2^{-1}BP_2$ 知

$$
(P_1P_2^{-1})^{-1}A(P_1P_2^{-1})=B.
$$

计算得

$$
P=P_1P_2^{-1}=
\begin{pmatrix}
1 & 1 & 1 \\
-2 & -1 & -2 \\
0 & 0 & -4
\end{pmatrix}.
$$

把矩阵整体乘以 $-1$ 仍可作为相似变换矩阵，所以也可写成题卡中的等价形式。

### 第 22 题

#### 标准答案

1. $f_Z(z)=\begin{cases}pe^z,&z<0,\\(1-p)e^{-z},&z\ge 0\end{cases}$
2. $p=\dfrac{1}{2}$
3. $X$ 与 $Z$ 不独立

#### 解析

先求 $Z=XY$ 的分布函数：

$$
F_Z(z)=P(Z\le z)=P(XY\le z\mid Y=-1)P(Y=-1)+P(XY\le z\mid Y=1)P(Y=1).
$$

由 $X$ 服从参数为 $1$ 的指数分布，分类讨论可得：

当 $z<0$ 时，

$$
F_Z(z)=pP(-X\le z)=pe^z;
$$

当 $z\ge 0$ 时，

$$
F_Z(z)=p\cdot 1+(1-p)P(X\le z)=1-(1-p)e^{-z}.
$$

故密度函数为

$$
f_Z(z)=F_Z'(z)=\begin{cases}pe^z,&z<0,\\(1-p)e^{-z},&z\ge 0.\end{cases}
$$

再算协方差：

$$
\operatorname{Cov}(X,Z)=E(XZ)-EX\,EZ=E(X^2Y)-EX\,E(XY).
$$

由独立性可化为

$$
\operatorname{Cov}(X,Z)=E(X^2)E(Y)-(EX)^2E(Y)=DX\cdot E(Y)=1-2p.
$$

所以 $\operatorname{Cov}(X,Z)=0$ 当且仅当 $p=\dfrac{1}{2}$。

最后判断独立性。注意

$$
P(X\le 1,Z\le -1)=P(X\le 1,XY\le -1)=0,
$$

但 $P(X\le 1)>0$ 且 $P(Z\le -1)>0$，因此

$$
P(X\le 1,Z\le -1)\ne P(X\le 1)P(Z\le -1),
$$

故 $X$ 与 $Z$ 不独立。

### 第 23 题

#### 标准答案

1. $A=\sqrt{\dfrac{2}{\pi}}$
2. $\hat\sigma^2=\dfrac{1}{n}\sum_{i=1}^n(X_i-\mu)^2$

#### 解析

由密度函数归一化条件

$$
\int_{-\infty}^{+\infty}f(x;\sigma^2)\,dx=1
$$

得

$$
1=\int_{\mu}^{+\infty}\frac{A}{\sigma}e^{-\frac{(x-\mu)^2}{2\sigma^2}}dx.
$$

令 $t=\dfrac{x-\mu}{\sigma}$，则

$$
1=A\int_0^{+\infty}e^{-t^2/2}dt=A\cdot\frac{\sqrt{2\pi}}{2},
$$

所以

$$
A=\sqrt{\frac{2}{\pi}}.
$$

设样本观测值为 $x_1,\dots,x_n$，则似然函数为

$$
L(\sigma^2)=\prod_{i=1}^n f(x_i;\sigma^2)
=\left(\frac{2}{\pi}\right)^{n/2}(\sigma^2)^{-n/2}\exp\left(-\frac{\sum_{i=1}^n(x_i-\mu)^2}{2\sigma^2}\right),
$$

其对数似然函数为

$$
\ln L(\sigma^2)=\frac{n}{2}\ln\frac{2}{\pi}-\frac{n}{2}\ln\sigma^2-\frac{1}{2\sigma^2}\sum_{i=1}^n(x_i-\mu)^2.
$$

求导并令其为零：

$$
\frac{d\ln L(\sigma^2)}{d\sigma^2}=-\frac{n}{2\sigma^2}+\frac{1}{2\sigma^4}\sum_{i=1}^n(x_i-\mu)^2=0.
$$

解得最大似然估计为

$$
\hat\sigma^2=\frac{1}{n}\sum_{i=1}^n(X_i-\mu)^2.
$$
