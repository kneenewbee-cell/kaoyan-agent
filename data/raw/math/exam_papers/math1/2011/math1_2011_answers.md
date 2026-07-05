# Math 1 2011 Answers

资料类型：考研数学一答案解析
年份：2011
科目：数学一
整理状态：已按题干与答案页图像核对并清洗整理

## 答案速查

| 题号 | 题型 | 答案 |
|---|---|---|
| 1 | 选择题 | C |
| 2 | 选择题 | C |
| 3 | 选择题 | A |
| 4 | 选择题 | B |
| 5 | 选择题 | D |
| 6 | 选择题 | D |
| 7 | 选择题 | D |
| 8 | 选择题 | B |
| 9 | 填空题 | $\ln(1+\sqrt{2})$ |
| 10 | 填空题 | $e^{-x}\sin x$ |
| 11 | 填空题 | $4$ |
| 12 | 填空题 | $\pi$ |
| 13 | 填空题 | $1$ |
| 14 | 填空题 | $\mu\sigma^2+\mu^3$ |
| 15 | 解答题 | $e^{-1/2}$ |
| 16 | 解答题 | $f_1^\prime(1,1)+f_{11}^{\prime\prime}(1,1)+f_{12}^{\prime\prime}(1,1)$ |
| 17 | 解答题 | 当 $k\le 1$ 时，方程只有 $1$ 个实根；当 $k>1$ 时，方程有 $3$ 个不同实根。 |
| 18 | 解答题 | （1）不等式成立；（2）数列收敛。 |
| 19 | 解答题 | $I=a$ |
| 20 | 解答题 | （1）$a=5$；（2）$\beta_1=2\alpha_1+4\alpha_2-\alpha_3$，$\beta_2=\alpha_1+2\alpha_2$，$\beta_3=5\alpha_1+10\alpha_2-2\alpha_3$。 |
| 21 | 解答题 | （1）特征值为 $-1,1,0$；对应特征向量可分别取 $k_1(1,0,-1)^T$、$k_2(1,0,1)^T$、$k_3(0,1,0)^T$，其中 $k_i\ne0$；（2）$A=\begin{pmatrix}0&0&1\\0&0&0\\1&0&0\end{pmatrix}$。 |
| 22 | 解答题 | （1）$P\{X=0,Y=0\}=P\{X=1,Y=-1\}=P\{X=1,Y=1\}=\frac{1}{3}$，其余为 $0$；（2）$P\{Z=-1\}=P\{Z=0\}=P\{Z=1\}=\frac{1}{3}$；（3）$\rho_{XY}=0$。 |
| 23 | 解答题 | （1）$\hat\sigma^2=\frac{1}{n}\sum_{i=1}^n (X_i-\mu_0)^2$；（2）$E(\hat\sigma^2)=\sigma^2$，$D(\hat\sigma^2)=\frac{2\sigma^4}{n}$。 |

## 详细解析

### 第 1 题 **答案：** C

令
$$
y=(x-1)(x-2)^2(x-3)^3(x-4)^4.
$$
拐点要求二阶导数在该点两侧变号。对零点的重数作局部判断：$x=1$ 为一重零点、$x=2$ 为二重零点，均不能使 $y''$ 在该点为零；$x=3$ 为三重零点，$x=4$ 为四重零点，是需要进一步判断的候选点。

在 $x=3$ 附近，
$$
y=2(x-3)^3+o((x-3)^3),
$$
故
$$
y''=12(x-3)+o(x-3),
$$
二阶导数在 $x=3$ 两侧变号，所以 $(3,0)$ 是拐点。在 $x=4$ 附近，
$$
y=12(x-4)^4+o((x-4)^4),
$$
故 $y''$ 在两侧同号，不是拐点。故选 C。

### 第 2 题 **答案：** C

幂级数
$$
\sum_{n=1}^{\infty}a_n(x-1)^n
$$
的收敛区间关于中心 $x=1$ 对称，端点需单独判断。由于 $a_n\to0$，当 $|x-1|<1$ 时级数绝对收敛。

端点 $x=0$ 时，级数为
$$
\sum_{n=1}^{\infty}(-1)^n a_n,
$$
因 $\{a_n\}$ 单调趋于 $0$，由莱布尼茨判别法知其收敛。端点 $x=2$ 时，级数为
$$
\sum_{n=1}^{\infty}a_n,
$$
其前 $n$ 项和 $S_n$ 无界，故发散。因此收敛域为 $[0,2)$，选 C。

### 第 3 题 **答案：** A

设
$$
z=f(x)\ln f(y).
$$
由 $f'(0)=0$ 且 $f(0)>0$，有
$$
z_x(0,0)=f'(0)\ln f(0)=0,
\qquad
z_y(0,0)=f(0)\frac{f'(0)}{f(0)}=0.
$$
再看 Hessian 矩阵。在 $(0,0)$ 处，
$$
z_{xx}=f''(0)\ln f(0),\qquad z_{xy}=0,
\qquad z_{yy}=f''(0).
$$
若 $f(0)>1$ 且 $f''(0)>0$，则 $z_{xx}>0,z_{yy}>0$，Hessian 正定，所以 $z$ 在 $(0,0)$ 处取得极小值。故选 A。

### 第 4 题 **答案：** B

当 $0<x<\frac{\pi}{4}$ 时，
$$
0<\sin x<\cos x<\cot x,
$$
于是
$$
\ln(\sin x)<\ln(\cos x)<\ln(\cot x).
$$
在同一区间积分得
$$
I<K<J.
$$
故选 B。

### 第 5 题 **答案：** D

将 $A$ 的第 $2$ 列加到第 $1$ 列等价于右乘 $P_1$，故
$$
AP_1=B.
$$
交换 $B$ 的第 $2$ 行与第 $3$ 行等价于左乘 $P_2$，且结果为单位矩阵，故
$$
P_2B=E.
$$
由于 $P_2^{-1}=P_2$，所以 $B=P_2$。于是
$$
AP_1=P_2,
\qquad
A=P_2P_1^{-1}.
$$
故选 D。

### 第 6 题 **答案：** D

方程组 $Ax=0$ 的基础解系只含一个线性无关解向量，故 $A$ 的零度为 $1$，从而
$$
r(A)=3.
$$
因此伴随矩阵满足 $r(A^*)=1$，齐次方程组 $A^*x=0$ 的基础解系应含 $3$ 个线性无关解向量，排除 A、B。

又 $A^*A=\det AE=0$，所以 $A$ 的列向量均为 $A^*x=0$ 的解。由 $(1,0,1,0)^T$ 是 $Ax=0$ 的基础解系，得
$$
\alpha_1+\alpha_3=0.
$$
故 $\alpha_1,\alpha_2,\alpha_3$ 线性相关，而 $\alpha_2,\alpha_3,\alpha_4$ 可作为 $A^*x=0$ 的基础解系。故选 D。

### 第 7 题 **答案：** D

候选函数
$$
g(x)=f_1(x)F_2(x)+f_2(x)F_1(x)
$$
非负，因为 $f_1,f_2\ge0$ 且 $F_1,F_2\ge0$。又
$$
g(x)=\frac{d}{dx}\bigl(F_1(x)F_2(x)\bigr),
$$
因此
$$
\int_{-\infty}^{+\infty}g(x)\,dx
=F_1(+\infty)F_2(+\infty)-F_1(-\infty)F_2(-\infty)=1.
$$
所以 $g(x)$ 必为概率密度。故选 D。

### 第 8 题 **答案：** B

无论 $X\ge Y$ 还是 $X<Y$，都有
$$
UV=\max\{X,Y\}\min\{X,Y\}=XY.
$$
因此
$$
E(UV)=E(XY).
$$
又 $X$ 与 $Y$ 相互独立，且 $E(X),E(Y)$ 存在，所以
$$
E(XY)=E(X)E(Y).
$$
故选 B。

### 第 9 题 **答案：** $\ln(1+\sqrt{2})$

由题设
$$
y'=\tan x.
$$
弧长为
$$
s=\int_0^{\pi/4}\sqrt{1+(y')^2}\,dx
=\int_0^{\pi/4}\sqrt{1+\tan^2x}\,dx
=\int_0^{\pi/4}\sec x\,dx.
$$
于是
$$
s=\left.\ln|\sec x+\tan x|\right|_0^{\pi/4}
=\ln(1+\sqrt{2}).
$$

### 第 10 题 **答案：** $e^{-x}\sin x$

方程
$$
y'+y=e^{-x}\cos x
$$
的积分因子为 $e^x$，故
$$
(e^x y)'=\cos x.
$$
积分得
$$
e^x y=\sin x+C,
\qquad
 y=e^{-x}(\sin x+C).
$$
由 $y(0)=0$ 得 $C=0$，所以
$$
y=e^{-x}\sin x.
$$

### 第 11 题 **答案：** $4$

由
$$
F(x,y)=\int_0^{xy}\frac{\sin t}{1+t^2}\,dt
$$
可得
$$
F_x=\frac{y\sin(xy)}{1+x^2y^2}.
$$
继续对 $x$ 求偏导，
$$
F_{xx}=y^2\frac{(1+x^2y^2)\cos(xy)-2xy\sin(xy)}{(1+x^2y^2)^2}.
$$
代入 $x=0,y=2$，得
$$
\left.F_{xx}\right|_{x=0,y=2}=4.
$$

### 第 12 题 **答案：** $\pi$

记
$$
P=xz,
\qquad Q=x,
\qquad R=\frac{y^2}{2}.
$$
按题设方向取曲面 $\Sigma:z=x+y$ 的上侧，由斯托克斯公式，
$$
\oint_L P\,dx+Q\,dy+R\,dz
=\iint_\Sigma
\left(\frac{\partial R}{\partial y}-\frac{\partial Q}{\partial z}\right)dy\,dz
+\left(\frac{\partial P}{\partial z}-\frac{\partial R}{\partial x}\right)dz\,dx
+\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)dx\,dy.
$$
即
$$
\oint_L xz\,dx+x\,dy+\frac{y^2}{2}\,dz
=\iint_\Sigma y\,dy\,dz+x\,dz\,dx+dx\,dy.
$$
其中 $\Sigma$ 在 $xOy$ 平面上的投影为单位圆盘 $D:x^2+y^2\le1$。前两项因关于圆盘对称积分为 $0$，第三项为投影面积，故
$$
\oint_L xz\,dx+x\,dy+\frac{y^2}{2}\,dz=\iint_D1\,dx\,dy=\pi.
$$

### 第 13 题 **答案：** $1$

二次型矩阵为
$$
A=\begin{pmatrix}1&a&1\\a&3&1\\1&1&1\end{pmatrix}.
$$
经正交变换化为 $y_1^2+4z_1^2=4$，说明 $A$ 的特征值为 $0,1,4$。因此
$$
\det A=0.
$$
直接计算
$$
\det A=-(a-1)^2,
$$
故
$$
a=1.
$$

### 第 14 题 **答案：** $\mu\sigma^2+\mu^3$

由 $(X,Y)\sim N(\mu,\mu;\sigma^2,\sigma^2;0)$ 可知 $X,Y$ 相互独立，且
$$
X\sim N(\mu,\sigma^2),\qquad Y\sim N(\mu,\sigma^2).
$$
于是
$$
E(XY^2)=E(X)E(Y^2)=\mu\bigl(D(Y)+[E(Y)]^2\bigr)
=\mu(\sigma^2+\mu^2)=\mu\sigma^2+\mu^3.
$$

### 第 15 题 **答案：** $e^{-1/2}$

令
$$
y=\left(\frac{\ln(1+x)}{x}\right)^{\frac{1}{e^x-1}}.
$$
当 $x\to0$ 时，
$$
\frac{\ln(1+x)}{x}=1-\frac{x}{2}+O(x^2),
$$
因此
$$
\ln\left(\frac{\ln(1+x)}{x}\right)=-\frac{x}{2}+O(x^2).
$$
又
$$
e^x-1=x+O(x^2),
$$
所以
$$
\ln y=\frac{\ln\left(\frac{\ln(1+x)}{x}\right)}{e^x-1}\to -\frac{1}{2}.
$$
故原极限为
$$
e^{-1/2}.
$$

### 第 16 题 **答案：** $f_1^\prime(1,1)+f_{11}^{\prime\prime}(1,1)+f_{12}^{\prime\prime}(1,1)$

记
$$
u=xy,
\qquad v=yg(x),
\qquad z=f(u,v).
$$
由 $g(x)$ 在 $x=1$ 处取得极值且可导，得
$$
g'(1)=0,
\qquad g(1)=1.
$$
先对 $x$ 求偏导：
$$
z_x=yf_1^\prime+yg'(x)f_2^\prime.
$$
再对 $y$ 求偏导，得
$$
z_{xy}=f_1^\prime+xy f_{11}^{\prime\prime}+y f_{12}^{\prime\prime}\bigl(g(x)+xg'(x)\bigr)
+g'(x)f_2^\prime+yg(x)g'(x)f_{22}^{\prime\prime}.
$$
将 $x=1,y=1,g(1)=1,g'(1)=0$ 代入，得到
$$
\left.z_{xy}\right|_{x=1,y=1}
=f_1^\prime(1,1)+f_{11}^{\prime\prime}(1,1)+f_{12}^{\prime\prime}(1,1).
$$

### 第 17 题 **答案：** 当 $k\le 1$ 时，方程只有 $1$ 个实根；当 $k>1$ 时，方程有 $3$ 个不同实根。

令
$$
f(x)=k\arctan x-x.
$$
则
$$
f'(x)=\frac{k}{1+x^2}-1=\frac{k-1-x^2}{1+x^2}.
$$

当 $k\le1$ 时，$f'(x)\le0$，故 $f(x)$ 单调不增。又 $f(0)=0$，所以方程只有一个实根 $x=0$。

当 $k>1$ 时，令 $a=\sqrt{k-1}$，则 $f'(x)$ 在 $(-\infty,-a)$ 与 $(a,+\infty)$ 上为负，在 $(-a,a)$ 上为正。因此 $x=-a$ 为极小值点，$x=a$ 为极大值点。又 $f$ 为奇函数，且
$$
f(a)=k\arctan a-a=(1+a^2)\arctan a-a>0,
$$
其中不等式可由 $h(a)=(1+a^2)\arctan a-a$ 满足 $h(0)=0,h'(a)=2a\arctan a>0$ 得到。于是 $f(-a)<0$。再结合
$$
\lim_{x\to-\infty}f(x)=+\infty,
\qquad
\lim_{x\to+\infty}f(x)=-\infty,
\qquad
f(0)=0,
$$
可知方程有三个不同实根。

### 第 18 题 **答案：** （1）不等式成立；（2）数列收敛。

（1）令 $f(x)=\ln(1+x)$。在区间 $[0,1/n]$ 上用拉格朗日中值定理，存在 $\xi\in(0,1/n)$，使
$$
\ln\left(1+\frac{1}{n}\right)-\ln1=f'(\xi)\frac{1}{n}=\frac{1}{n(1+\xi)}.
$$
因为 $0<\xi<\frac{1}{n}$，所以
$$
\frac{1}{n+1}<\frac{1}{n(1+\xi)}<\frac{1}{n}.
$$
即
$$
\frac{1}{n+1}<\ln\left(1+\frac{1}{n}\right)<\frac{1}{n}.
$$

（2）由（1）知
$$
\ln(n+1)-\ln n=\ln\left(1+\frac{1}{n}\right)<\frac{1}{n}.
$$
令 $n=1,2,\ldots,m$ 并相加，得
$$
\ln(m+1)<1+\frac{1}{2}+\cdots+\frac{1}{m}.
$$
于是
$$
a_{m+1}=1+\frac{1}{2}+\cdots+\frac{1}{m}+\frac{1}{m+1}-\ln(m+1)>\frac{1}{m+1}>0,
$$
所以 $\{a_n\}$ 有下界。

另一方面，
$$
a_n-a_{n+1}=\ln\left(1+\frac{1}{n}\right)-\frac{1}{n+1}>0,
$$
故 $\{a_n\}$ 单调下降。单调有界数列必收敛，因此 $\{a_n\}$ 收敛。

### 第 19 题 **答案：** $I=a$

积分区域为
$$
D=\{(x,y)\mid 0\le x\le1,
0\le y\le1\}.
$$
于是
$$
I=\int_0^1 x\,dx\int_0^1 y f_{xy}(x,y)\,dy.
$$
先对内层关于 $y$ 分部积分：
$$
\int_0^1 y f_{xy}(x,y)\,dy
=\left.yf_x(x,y)\right|_0^1-\int_0^1 f_x(x,y)\,dy
=f_x(x,1)-\int_0^1 f_x(x,y)\,dy.
$$
故
$$
I=\int_0^1 x f_x(x,1)\,dx-
\int_0^1\int_0^1 x f_x(x,y)\,dy\,dx.
$$
第一项中 $f(x,1)=0$，所以
$$
\int_0^1 x f_x(x,1)\,dx
=\left.xf(x,1)\right|_0^1-\int_0^1 f(x,1)\,dx=0.
$$
第二项交换积分次序并对 $x$ 分部积分：
$$
\int_0^1\int_0^1 x f_x(x,y)\,dx\,dy
=\int_0^1\left(\left.xf(x,y)\right|_0^1-\int_0^1f(x,y)\,dx\right)dy.
$$
由 $f(1,y)=0$，上式等于
$$
-\iint_D f(x,y)\,dx\,dy=-a.
$$
因此
$$
I=0-(-a)=a.
$$

### 第 20 题 **答案：** （1）$a=5$；（2）$\beta_1=2\alpha_1+4\alpha_2-\alpha_3$，$\beta_2=\alpha_1+2\alpha_2$，$\beta_3=5\alpha_1+10\alpha_2-2\alpha_3$。

先看向量组 $\alpha_1,\alpha_2,\alpha_3$。其矩阵
$$
(\alpha_1,\alpha_2,\alpha_3)=
\begin{pmatrix}1&0&1\\0&1&3\\1&1&5\end{pmatrix}
$$
的行列式为 $1$，所以它张成三维空间。若 $\beta_1,\beta_2,\beta_3$ 也张成三维空间，则 $\alpha_1,\alpha_2,\alpha_3$ 都可由它们线性表示，与题设矛盾。因此
$$
|\beta_1,\beta_2,\beta_3|=0.
$$
即
$$
\begin{vmatrix}1&1&3\\1&2&4\\1&3&a\end{vmatrix}=a-5=0,
$$
故
$$
a=5.
$$

设
$$
(\beta_1,\beta_2,\beta_3)=(\alpha_1,\alpha_2,\alpha_3)C.
$$
当 $a=5$ 时，
$$
C=(\alpha_1,\alpha_2,\alpha_3)^{-1}(\beta_1,\beta_2,\beta_3)
=\begin{pmatrix}2&1&5\\4&2&10\\-1&0&-2\end{pmatrix}.
$$
因此
$$
\beta_1=2\alpha_1+4\alpha_2-\alpha_3,
\qquad
\beta_2=\alpha_1+2\alpha_2,
\qquad
\beta_3=5\alpha_1+10\alpha_2-2\alpha_3.
$$

### 第 21 题 **答案：** （1）特征值为 $-1,1,0$；对应特征向量可分别取 $k_1(1,0,-1)^T$、$k_2(1,0,1)^T$、$k_3(0,1,0)^T$，其中 $k_i\ne0$；（2）$A=\begin{pmatrix}0&0&1\\0&0&0\\1&0&0\end{pmatrix}$。

记
$$
\alpha_1=(1,0,-1)^T,
\qquad
\alpha_2=(1,0,1)^T.
$$
由题设矩阵等式可知
$$
A\alpha_1=-\alpha_1,
\qquad
A\alpha_2=\alpha_2.
$$
故 $-1$ 与 $1$ 是 $A$ 的特征值，对应特征向量分别为 $\alpha_1,\alpha_2$。又 $r(A)=2$，所以 $\det A=0$，另一特征值为 $0$。

设 $0$ 对应的特征向量为 $\alpha_3=(x_1,x_2,x_3)^T$。由于 $A$ 为实对称矩阵，不同特征值对应的特征向量正交，故
$$
\alpha_1^T\alpha_3=0,
\qquad
\alpha_2^T\alpha_3=0.
$$
即
$$
x_1-x_3=0,
\qquad
x_1+x_3=0,
$$
解得可取 $\alpha_3=(0,1,0)^T$。所以三个特征值 $-1,1,0$ 的特征向量可分别写为
$$
k_1(1,0,-1)^T,
\quad
k_2(1,0,1)^T,
\quad
k_3(0,1,0)^T,
\qquad k_i\ne0.
$$

将单位特征向量组成正交矩阵，或直接用谱分解，得
$$
A=-\frac{\alpha_1\alpha_1^T}{\alpha_1^T\alpha_1}
+\frac{\alpha_2\alpha_2^T}{\alpha_2^T\alpha_2}
=\begin{pmatrix}0&0&1\\0&0&0\\1&0&0\end{pmatrix}.
$$

### 第 22 题 **答案：** （1）$P\{X=0,Y=0\}=P\{X=1,Y=-1\}=P\{X=1,Y=1\}=\frac{1}{3}$，其余为 $0$；（2）$P\{Z=-1\}=P\{Z=0\}=P\{Z=1\}=\frac{1}{3}$；（3）$\rho_{XY}=0$。

由 $P\{X^2=Y^2\}=1$ 可知，只可能出现满足 $X^2=Y^2$ 的取值组合。结合 $X$ 的取值为 $0,1$，$Y$ 的取值为 $-1,0,1$，可知可能组合只有
$$
(0,0),\quad (1,-1),\quad (1,1).
$$
由边缘分布得
$$
P\{X=0,Y=0\}=P\{X=0\}=\frac{1}{3},
$$
且
$$
P\{X=1,Y=-1\}=P\{Y=-1\}=\frac{1}{3},
\qquad
P\{X=1,Y=1\}=P\{Y=1\}=\frac{1}{3}.
$$
因此二维分布为

| $X\backslash Y$ | $-1$ | $0$ | $1$ |
|---|---:|---:|---:|
| $0$ | $0$ | $\frac{1}{3}$ | $0$ |
| $1$ | $\frac{1}{3}$ | $0$ | $\frac{1}{3}$ |

令 $Z=XY$，则 $Z$ 的可能取值为 $-1,0,1$，并且
$$
P\{Z=-1\}=P\{X=1,Y=-1\}=\frac{1}{3},
$$
$$
P\{Z=0\}=P\{X=0,Y=0\}=\frac{1}{3},
$$
$$
P\{Z=1\}=P\{X=1,Y=1\}=\frac{1}{3}.
$$
故 $Z$ 的分布为

| $Z$ | $-1$ | $0$ | $1$ |
|---|---:|---:|---:|
| $P$ | $\frac{1}{3}$ | $\frac{1}{3}$ | $\frac{1}{3}$ |

最后，
$$
E(X)=\frac{2}{3},
\qquad
E(Y)=0,
\qquad
E(XY)=0.
$$
所以
$$
\operatorname{Cov}(X,Y)=E(XY)-E(X)E(Y)=0.
$$
由于 $D(X)>0,D(Y)>0$，得到
$$
\rho_{XY}=0.
$$

### 第 23 题 **答案：** （1）$\hat\sigma^2=\frac{1}{n}\sum_{i=1}^n (X_i-\mu_0)^2$；（2）$E(\hat\sigma^2)=\sigma^2$，$D(\hat\sigma^2)=\frac{2\sigma^4}{n}$。

设样本观测值为 $x_1,x_2,\ldots,x_n$。因为 $\mu_0$ 已知，似然函数为
$$
L(\sigma^2)=\prod_{i=1}^n\frac{1}{\sqrt{2\pi}\sigma}
\exp\left\{-\frac{(x_i-\mu_0)^2}{2\sigma^2}\right\}.
$$
取对数，得
$$
\ln L(\sigma^2)=-\frac{n}{2}\ln(2\pi)-\frac{n}{2}\ln\sigma^2-
\frac{1}{2\sigma^2}\sum_{i=1}^n(x_i-\mu_0)^2.
$$
对 $\sigma^2$ 求导并令其为 $0$，得到
$$
\hat\sigma^2=\frac{1}{n}\sum_{i=1}^n(X_i-\mu_0)^2.
$$

又
$$
\frac{1}{\sigma^2}\sum_{i=1}^n(X_i-\mu_0)^2\sim\chi^2(n).
$$
因此
$$
E(\hat\sigma^2)=\frac{\sigma^2}{n}\cdot n=\sigma^2,
$$
并且
$$
D(\hat\sigma^2)=\frac{\sigma^4}{n^2}\cdot 2n=\frac{2\sigma^4}{n}.
$$
