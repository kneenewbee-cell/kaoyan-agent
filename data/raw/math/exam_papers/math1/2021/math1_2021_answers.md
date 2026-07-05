# Math 1 2021 Answers

资料类型：考研数学一答案解析
年份：2021
科目：数学一
来源：现有题干与答案速查图 `images/answer_quick.png`，逐题补写解析
校对状态：已按题干、答案速查图和数学推导补齐解析

## 答案速查

| 题号 | 题型 | 答案 |
|---|---|---|
| 1 | 选择题 | D |
| 2 | 选择题 | C |
| 3 | 选择题 | A |
| 4 | 选择题 | B |
| 5 | 选择题 | B |
| 6 | 选择题 | A |
| 7 | 选择题 | C |
| 8 | 选择题 | D |
| 9 | 选择题 | C |
| 10 | 选择题 | B |
| 11 | 填空题 | $\displaystyle \frac{\pi}{4}$ |
| 12 | 填空题 | $\displaystyle \frac{2}{3}$ |
| 13 | 填空题 | $x^2$ |
| 14 | 填空题 | $4\pi$ |
| 15 | 填空题 | $\displaystyle \frac{3}{2}$ |
| 16 | 填空题 | $\displaystyle \frac{1}{5}$ |
| 17 | 解答题 | $\displaystyle \frac{1}{2}$ |
| 18 | 解答题 | 收敛域为 $(0,1]$；和函数见解析。 |
| 19 | 解答题 | 最大值为 $66$。 |
| 20 | 解答题 | (I) $I(D_1)=8\pi$；(II) $-\pi$。 |
| 21 | 解答题 | (I) 见解析；(II) $\displaystyle C=\begin{pmatrix}\frac{5}{3}&-\frac{1}{3}&\frac{1}{3}\\-\frac{1}{3}&\frac{5}{3}&\frac{1}{3}\\\frac{1}{3}&\frac{1}{3}&\frac{5}{3}\end{pmatrix}$。 |
| 22 | 解答题 | (I) $f_X(x)=1,\ 0<x<1$；(II) $f_Z(z)=\frac{2}{(z+1)^2},\ z\ge1$；(III) $2\ln2-1$。 |

## 详细解析

### 第 1 题

**答案：** D

当 $x\ne0$ 时，
$$
\frac{e^x-1}{x}=1+\frac{x}{2}+O(x^2).
$$
因此
$$
\lim_{x\to0}\frac{e^x-1}{x}=1=f(0),
$$
函数在 $x=0$ 处连续。并且
$$
f'(0)=\lim_{x\to0}\frac{f(x)-f(0)}{x}
=\lim_{x\to0}\frac{\frac{e^x-1}{x}-1}{x}
=\frac{1}{2}\ne0.
$$
故选 D。

### 第 2 题

**答案：** C

由
$$
f(x+1,e^x)=x(x+1)^2
$$
在 $x=0$ 处求导，得
$$
f_x(1,1)+f_y(1,1)=1.
$$
由
$$
f(x,x^2)=2x^2\ln x
$$
在 $x=1$ 处求导，得
$$
f_x(1,1)+2f_y(1,1)=2.
$$
联立解得
$$
f_x(1,1)=0,\qquad f_y(1,1)=1.
$$
所以
$$
df(1,1)=dy.
$$
故选 C。

### 第 3 题

**答案：** A

在 $x=0$ 附近，
$$
\sin x=x-\frac{x^3}{6}+O(x^5),\qquad
\frac{1}{1+x^2}=1-x^2+O(x^4).
$$
于是
$$
\frac{\sin x}{1+x^2}
=\left(x-\frac{x^3}{6}+O(x^5)\right)(1-x^2+O(x^4))
=x-\frac{7}{6}x^3+O(x^5).
$$
因此
$$
a=1,\qquad b=0,\qquad c=-\frac{7}{6}.
$$
故选 A。

### 第 4 题

**答案：** B

把 $[0,1]$ 分成 $n$ 个等长小区间，每段长度为 $1/n$，第 $k$ 段中点为
$$
\frac{2k-1}{2n}.
$$
由于 $f$ 在 $[0,1]$ 上连续，定积分等于任意取点的黎曼和极限，故
$$
\int_0^1 f(x)\,dx
=\lim_{n\to\infty}\sum_{k=1}^n
f\left(\frac{2k-1}{2n}\right)\frac{1}{n}.
$$
故选 B。

### 第 5 题

**答案：** B

展开二次型：
$$
\begin{aligned}
f&=(x_1+x_2)^2+(x_2+x_3)^2-(x_3-x_1)^2\\
&=2x_2^2+2x_1x_2+2x_2x_3+2x_1x_3.
\end{aligned}
$$
对应矩阵为
$$
A=\begin{pmatrix}
0&1&1\\
1&2&1\\
1&1&0
\end{pmatrix}.
$$
有 $\det A=0$，且二阶主子式
$$
\begin{vmatrix}0&1\\1&2\end{vmatrix}=-1<0,
$$
说明非零惯性指数中正、负各有一个。故正惯性指数为 $1$，负惯性指数为 $1$。

故选 B。

### 第 6 题

**答案：** A

由 $\boldsymbol{\beta}_2=\boldsymbol{\alpha}_2-k\boldsymbol{\beta}_1$ 与 $\boldsymbol{\beta}_1$ 正交，
$$
(\boldsymbol{\alpha}_2-k\boldsymbol{\alpha}_1,\boldsymbol{\alpha}_1)=0.
$$
因为
$$
(\boldsymbol{\alpha}_2,\boldsymbol{\alpha}_1)=2,\qquad
(\boldsymbol{\alpha}_1,\boldsymbol{\alpha}_1)=2,
$$
得 $k=1$，于是
$$
\boldsymbol{\beta}_2=(0,2,0)^T.
$$
再由
$$
\boldsymbol{\beta}_3=\boldsymbol{\alpha}_3-l_1\boldsymbol{\beta}_1-l_2\boldsymbol{\beta}_2
$$
分别与 $\boldsymbol{\beta}_1,\boldsymbol{\beta}_2$ 正交，得
$$
l_1=\frac{(\boldsymbol{\alpha}_3,\boldsymbol{\beta}_1)}{(\boldsymbol{\beta}_1,\boldsymbol{\beta}_1)}
=\frac{5}{2},
\qquad
l_2=\frac{(\boldsymbol{\alpha}_3,\boldsymbol{\beta}_2)}{(\boldsymbol{\beta}_2,\boldsymbol{\beta}_2)}
=\frac{1}{2}.
$$
故选 A。

### 第 7 题

**答案：** C

A、B、D 都可由初等分块变换或 $r(A^TA)=r(A)$ 得到秩为 $2r(A)$。C 不恒成立。

举反例：
$$
A=\begin{pmatrix}1&1\\0&0\end{pmatrix},\qquad
B=\begin{pmatrix}1&1\\1&1\end{pmatrix}.
$$
则 $r(A)=1$，但
$$
\begin{pmatrix}
A&BA\\
O&AA^T
\end{pmatrix}
=
\begin{pmatrix}
1&1&1&1\\
0&0&1&1\\
0&0&2&0\\
0&0&0&0
\end{pmatrix}
$$
的秩为 $3$，不等于 $2r(A)=2$。故 C 不成立。

### 第 8 题

**答案：** D

D 不恒成立。取 $A\subset B$，且
$$
P(A)=0.4,\qquad P(B)=0.6.
$$
则 $A\cup B=B$，所以
$$
P(A\mid A\cup B)=P(A\mid B)=\frac{2}{3},
$$
而
$$
P(\overline A\mid A\cup B)=\frac{1}{3}.
$$
于是
$$
P(A\mid A\cup B)>P(\overline A\mid A\cup B),
$$
但 $P(A)<P(B)$。故 D 为假命题。

### 第 9 题

**答案：** C

有
$$
E(\overline X-\overline Y)=\mu_1-\mu_2=\theta,
$$
所以 $\widehat\theta$ 是 $\theta$ 的无偏估计。

又每组 $(X_i,Y_i)$ 中
$$
\operatorname{Cov}(X_i,Y_i)=\rho\sigma_1\sigma_2,
$$
不同样本之间相互独立，故
$$
D(\overline X-\overline Y)
=D(\overline X)+D(\overline Y)-2\operatorname{Cov}(\overline X,\overline Y)
=\frac{\sigma_1^2+\sigma_2^2-2\rho\sigma_1\sigma_2}{n}.
$$
故选 C。

### 第 10 题

**答案：** B

当 $\mu=11.5$ 时，
$$
\overline X\sim N\left(11.5,\frac{4}{16}\right),
$$
即标准差为 $1/2$。第二类错误为备择为真时未拒绝原假设：
$$
P_{\mu=11.5}\{\overline X\le 11\}
=P\left\{Z\le \frac{11-11.5}{1/2}\right\}
=P\{Z\le -1\}
=1-\Phi(1).
$$
故选 B。

### 第 11 题

**答案：** $\displaystyle \frac{\pi}{4}$

因为
$$
x^2+2x+2=(x+1)^2+1,
$$
所以
$$
\int_0^{+\infty}\frac{dx}{x^2+2x+2}
=\left.\arctan(x+1)\right|_0^{+\infty}
=\frac{\pi}{2}-\frac{\pi}{4}
=\frac{\pi}{4}.
$$

### 第 12 题

**答案：** $\displaystyle \frac{2}{3}$

由参数方程
$$
x=2e^t+t+1,\qquad y=4(t-1)e^t+t^2
$$
得
$$
x'=2e^t+1,\qquad y'=4te^t+2t.
$$
因此在 $t=0$ 时，
$$
x'(0)=3,\qquad y'(0)=0.
$$
又
$$
y''=4e^t+4te^t+2,
$$
故 $y''(0)=6$。于是
$$
\frac{dy}{dx}=\frac{y'}{x'},\qquad
\frac{d^2y}{dx^2}
=\frac{d}{dt}\left(\frac{dy}{dx}\right)\frac{1}{x'}.
$$
代入 $t=0$ 得
$$
\left.\frac{d^2y}{dx^2}\right|_{t=0}
=\frac{6/3}{3}
=\frac{2}{3}.
$$

### 第 13 题

**答案：** $x^2$

欧拉方程令 $y=x^m$，得
$$
m(m-1)+m-4=m^2-4=0.
$$
所以 $m=2,-2$，通解为
$$
y=C_1x^2+C_2x^{-2}.
$$
由
$$
y(1)=C_1+C_2=1,\qquad
y'(1)=2C_1-2C_2=2
$$
解得
$$
C_1=1,\qquad C_2=0.
$$
故
$$
y=x^2.
$$

### 第 14 题

**答案：** $4\pi$

由高斯公式，令
$$
P=x^2,\qquad Q=y^2,\qquad R=z,
$$
则
$$
\frac{\partial P}{\partial x}
+\frac{\partial Q}{\partial y}
+\frac{\partial R}{\partial z}
=2x+2y+1.
$$
区域关于 $x$、$y$ 对称，故 $2x$、$2y$ 的积分为 $0$。所求积分等于该柱体体积。

底面为
$$
x^2+4y^2\le4,
$$
半轴分别为 $2$ 和 $1$，面积为 $2\pi$；高为 $2$。因此体积为
$$
2\pi\cdot2=4\pi.
$$

### 第 15 题

**答案：** $\displaystyle \frac{3}{2}$

设
$$
\boldsymbol{e}=(1,1,1)^T.
$$
每行元素之和均为 $2$，即
$$
A\boldsymbol{e}=2\boldsymbol{e}.
$$
由于 $\det A=3\ne0$，$A$ 可逆，于是
$$
A^{-1}\boldsymbol{e}=\frac{1}{2}\boldsymbol{e}.
$$
两边乘以 $\det A$，得
$$
\operatorname{adj}(A)\boldsymbol{e}
=\frac{3}{2}\boldsymbol{e}.
$$
而 $\operatorname{adj}(A)$ 第一行与 $\boldsymbol{e}$ 的乘积为
$$
A_{11}+A_{21}+A_{31}.
$$
所以
$$
A_{11}+A_{21}+A_{31}=\frac{3}{2}.
$$

### 第 16 题

**答案：** $\displaystyle \frac{1}{5}$

令 $X,Y$ 分别为两次取球中取到红球的示性变量。显然
$$
P(X=1)=\frac{1}{2}.
$$
若 $X=1$，则乙盒中变为 $3$ 红 $2$ 白，故
$$
P(Y=1\mid X=1)=\frac{3}{5}.
$$
若 $X=0$，则乙盒中变为 $2$ 红 $3$ 白，故
$$
P(Y=1\mid X=0)=\frac{2}{5}.
$$
于是
$$
P(Y=1)=\frac{1}{2}\cdot\frac{3}{5}
+\frac{1}{2}\cdot\frac{2}{5}
=\frac{1}{2}.
$$
并且
$$
E(XY)=P(X=1,Y=1)=\frac{1}{2}\cdot\frac{3}{5}=\frac{3}{10}.
$$
故
$$
\operatorname{Cov}(X,Y)=\frac{3}{10}-\frac{1}{2}\cdot\frac{1}{2}
=\frac{1}{20}.
$$
又 $D(X)=D(Y)=1/4$，所以相关系数
$$
\rho_{XY}=\frac{\operatorname{Cov}(X,Y)}{\sqrt{D(X)D(Y)}}
=\frac{1/20}{1/4}
=\frac{1}{5}.
$$

### 第 17 题

**答案：** $\displaystyle \frac{1}{2}$

记
$$
A(x)=\int_0^x e^{t^2}\,dt.
$$
当 $x\to0$ 时，
$$
A(x)=x+\frac{x^3}{3}+O(x^5),
\qquad
e^x-1=x+\frac{x^2}{2}+\frac{x^3}{6}+O(x^4).
$$
因此
$$
\frac{1+A(x)}{e^x-1}
=\frac{1+x+O(x^3)}{x\left(1+\frac{x}{2}+O(x^2)\right)}
=\frac{1}{x}+\frac{1}{2}+O(x).
$$
又
$$
\frac{1}{\sin x}=\frac{1}{x}+O(x).
$$
所以
$$
\lim_{x\to0}\left[
\frac{1+\int_0^x e^{t^2}\,dt}{e^x-1}
-\frac{1}{\sin x}
\right]
=\frac{1}{2}.
$$

### 第 18 题

**答案：** 收敛域为 $(0,1]$；和函数见解析。

级数可分为
$$
\sum_{n=1}^{\infty}e^{-nx}
+\sum_{n=1}^{\infty}\frac{x^{n+1}}{n(n+1)}.
$$
第一项是等比级数，收敛当且仅当 $e^{-x}<1$，即 $x>0$。

第二项为幂级数，收敛半径为 $1$；在 $x=1$ 时
$$
\sum_{n=1}^{\infty}\frac{1}{n(n+1)}
$$
收敛。因此总级数收敛域为
$$
(0,1].
$$
当 $0<x<1$ 时，
$$
\sum_{n=1}^{\infty}e^{-nx}=\frac{1}{e^x-1}.
$$
又
$$
\frac{1}{n(n+1)}=\frac{1}{n}-\frac{1}{n+1},
$$
所以
$$
\begin{aligned}
\sum_{n=1}^{\infty}\frac{x^{n+1}}{n(n+1)}
&=x\sum_{n=1}^{\infty}\frac{x^n}{n}
-\sum_{n=1}^{\infty}\frac{x^{n+1}}{n+1}\\
&=-x\ln(1-x)-[-\ln(1-x)-x]\\
&=(1-x)\ln(1-x)+x.
\end{aligned}
$$
故
$$
s(x)=\frac{1}{e^x-1}+(1-x)\ln(1-x)+x,\qquad 0<x<1.
$$
当 $x=1$ 时，第二项级数和为 $1$，第一项为 $1/(e-1)$，故
$$
s(1)=\frac{1}{e-1}+1.
$$

### 第 19 题

**答案：** 最大值为 $66$。

由曲线方程
$$
z=x^2+2y^2-6,\qquad z=30-4x-2y
$$
消去 $z$，得
$$
x^2+2y^2+4x+2y-36=0.
$$
配方：
$$
(x+2)^2+2\left(y+\frac{1}{2}\right)^2=\frac{81}{2}.
$$
令
$$
u=x+2,\qquad v=y+\frac{1}{2},
$$
则
$$
z=30-4x-2y=39-4u-2v.
$$
在约束
$$
u^2+2v^2=\frac{81}{2}
$$
下，线性函数 $-4u-2v$ 的最大值为
$$
\sqrt{\frac{81}{2}\left(16+\frac{(-2)^2}{2}\right)}
=\sqrt{\frac{81}{2}\cdot18}
=27.
$$
因此
$$
z_{\max}=39+27=66.
$$
曲线上 $z$ 的最小值为 $39-27=12>0$，所以到 $xOy$ 面距离的最大值就是 $z$ 的最大值，即 $66$。

### 第 20 题

**答案：** (I) $I(D_1)=8\pi$；(II) $-\pi$。

(I) 被积函数
$$
4-x^2-y^2
$$
在圆盘 $x^2+y^2<4$ 内为正，在外部为负。要使积分最大，应取
$$
D_1=\{(x,y):x^2+y^2\le4\}.
$$
于是
$$
I(D_1)=\int_0^{2\pi}\int_0^2(4-r^2)r\,dr\,d\theta=8\pi.
$$

(II) 记 $s=x^2+4y^2$。积分中的微分形式可分为
$$
\frac{e^s}{s}(x\,dx+4y\,dy)+\frac{y\,dx-x\,dy}{x^2+4y^2}.
$$
第一项是全微分在闭曲线上的积分，贡献为 $0$。因此只需计算
$$
\oint_{\partial D_1}\frac{y\,dx-x\,dy}{x^2+4y^2}.
$$
取正向参数
$$
x=2\cos t,\qquad y=2\sin t,\qquad 0\le t\le2\pi.
$$
则
$$
y\,dx-x\,dy=-4\,dt,
$$
且
$$
x^2+4y^2=4(\cos^2 t+4\sin^2 t).
$$
故积分为
$$
-\int_0^{2\pi}\frac{dt}{\cos^2t+4\sin^2t}
=-\pi.
$$

### 第 21 题

**答案：** (I) 见解析；(II) $\displaystyle C=\begin{pmatrix}\frac{5}{3}&-\frac{1}{3}&\frac{1}{3}\\-\frac{1}{3}&\frac{5}{3}&\frac{1}{3}\\\frac{1}{3}&\frac{1}{3}&\frac{5}{3}\end{pmatrix}$。

(I) 取
$$
P=
\begin{pmatrix}
-\frac{1}{\sqrt{2}}&\frac{1}{\sqrt{6}}&-\frac{1}{\sqrt{3}}\\
\frac{1}{\sqrt{2}}&\frac{1}{\sqrt{6}}&-\frac{1}{\sqrt{3}}\\
0&\frac{2}{\sqrt{6}}&\frac{1}{\sqrt{3}}
\end{pmatrix}.
$$
其三列两两正交且均为单位向量，因此 $P$ 为正交矩阵。直接计算得
$$
P^TAP=
\begin{pmatrix}
a-1&0&0\\
0&a-1&0\\
0&0&a+2
\end{pmatrix}.
$$

(II) 由上式可知，$(a+3)E-A$ 的特征值为
$$
4,\quad 4,\quad 1.
$$
其正定平方根为
$$
C=P
\begin{pmatrix}
2&0&0\\
0&2&0\\
0&0&1
\end{pmatrix}
P^T.
$$
计算得
$$
C=
\begin{pmatrix}
\frac{5}{3}&-\frac{1}{3}&\frac{1}{3}\\
-\frac{1}{3}&\frac{5}{3}&\frac{1}{3}\\
\frac{1}{3}&\frac{1}{3}&\frac{5}{3}
\end{pmatrix}.
$$

### 第 22 题

**答案：** (I) $f_X(x)=1,\ 0<x<1$；(II) $f_Z(z)=\frac{2}{(z+1)^2},\ z\ge1$；(III) $2\ln2-1$。

设随机点到左端点的距离为 $U$，则 $U\sim U(0,2)$，且
$$
X=\min\{U,2-U\},\qquad Y=2-X.
$$

(I) 对 $0<x<1$，
$$
P(X>x)=P(x<U<2-x)=\frac{2-2x}{2}=1-x.
$$
故
$$
F_X(x)=x,\qquad 0<x<1,
$$
从而
$$
f_X(x)=
\begin{cases}
1,&0<x<1,\\
0,&\text{其他}.
\end{cases}
$$

(II) 由
$$
Z=\frac{Y}{X}=\frac{2-X}{X}=\frac{2}{X}-1
$$
可知 $z\ge1$，且
$$
x=\frac{2}{z+1}.
$$
于是
$$
f_Z(z)=f_X\left(\frac{2}{z+1}\right)
\left|\frac{d}{dz}\frac{2}{z+1}\right|
=\frac{2}{(z+1)^2},\qquad z\ge1.
$$
当 $z<1$ 时，$f_Z(z)=0$。

(III)
$$
E\left(\frac{X}{Y}\right)
=\int_0^1\frac{x}{2-x}\,dx.
$$
由于
$$
\frac{x}{2-x}=\frac{2}{2-x}-1,
$$
故
$$
E\left(\frac{X}{Y}\right)
=\left[-2\ln(2-x)-x\right]_0^1
=2\ln2-1.
$$
