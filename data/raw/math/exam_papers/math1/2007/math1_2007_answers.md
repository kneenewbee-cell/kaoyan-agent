# Math 1 2007 Answers

资料类型：考研数学一答案解析
年份：2007
科目：数学一
范围：试卷 I
来源：D:\百度网盘\高数资料\【02】1987-2022年数学一真题详解答案（PDF）\2007考研数学一真题解析.pdf
校对状态：已按答案页图像和原卷题干重新整理；第 11 题按原卷修正为正指数 e^{1/x}。

## 答案速查

| 题号 | 题型 | 答案 |
|---|---|---|
| 1 | 选择题 | B |
| 2 | 选择题 | D |
| 3 | 选择题 | C |
| 4 | 选择题 | D |
| 5 | 选择题 | D |
| 6 | 选择题 | B |
| 7 | 选择题 | A |
| 8 | 选择题 | B |
| 9 | 选择题 | C |
| 10 | 选择题 | A |
| 11 | 填空题 | $\displaystyle \frac{\sqrt{e}}{2}$ |
| 12 | 填空题 | $\displaystyle yx^{y-1}f'_1+y^x\ln y\,f'_2$ |
| 13 | 填空题 | $C_1e^{3x}+C_2e^x-2e^{2x}$ |
| 14 | 填空题 | $\displaystyle \frac{4\sqrt{3}}{3}$ |
| 15 | 填空题 | $1$ |
| 16 | 填空题 | $\displaystyle \frac{3}{4}$ |
| 17 | 解答题 | 最大值为 $8$，最小值为 $0$。 |
| 18 | 解答题 | $\pi$ |
| 19 | 解答题 | 结论成立。 |
| 20 | 解答题 | $\displaystyle y(x)=xe^{x^2}$ |
| 21 | 解答题 | $a=1$ 时，公共解为 $k(-1,0,1)^T$；$a=2$ 时，公共解为 $(0,1,-1)^T$。 |
| 22 | 解答题 | $B$ 的特征值为 $-2,1,1$；$\lambda=-2$ 的特征向量为 $k(1,-1,1)^T$，$\lambda=1$ 的特征向量满足 $x-y+z=0$；$\displaystyle B=\begin{pmatrix}0&1&-1\\1&0&1\\-1&1&0\end{pmatrix}$。 |
| 23 | 解答题 | $\displaystyle P\{X>2Y\}=\frac{7}{24}$；$\displaystyle f_Z(z)=z(2-z)\ (0<z<1)$，$\displaystyle f_Z(z)=(2-z)^2\ (1\le z<2)$，其他为 $0$。 |
| 24 | 解答题 | $\displaystyle \hat\theta=2\overline X-\frac{1}{2}$；$4\overline X^2$ 不是 $\theta^2$ 的无偏估计量。 |

## 详细解析

### 第 1 题

**答案：** B

当 $x\to0^+$ 时，
$$
\ln\frac{1+x}{1-\sqrt{x}}
=\ln\left(1+\frac{x+\sqrt{x}}{1-\sqrt{x}}\right)
\sim\frac{x+\sqrt{x}}{1-\sqrt{x}}\sim\sqrt{x}.
$$
其余选项分别与 $-\sqrt{x}$、$\frac{1}{2}\sqrt{x}$、$\frac{1}{2}x$ 等价，不等价于 $\sqrt{x}$。故选 B。

### 第 2 题

**答案：** D

函数在 $x=0$ 处有间断，且
$$
\lim_{x\to0^\pm}\left(\frac{1}{x}+\ln(1+e^x)\right)=\pm\infty,
$$
故 $x=0$ 是垂直渐近线。

当 $x\to-\infty$ 时，$\frac{1}{x}\to0$，$\ln(1+e^x)\to0$，故有水平渐近线 $y=0$。

当 $x\to+\infty$ 时，
$$
\lim_{x\to+\infty}\frac{y}{x}=1,\qquad
\lim_{x\to+\infty}(y-x)=0,
$$
故有斜渐近线 $y=x$。共 $3$ 条，选 D。

### 第 3 题

**答案：** C

由图形可知 $f(x)$ 为奇函数，所以
$$
F(x)=\int_0^x f(t)\,dt
$$
为偶函数。

在 $[0,2]$ 上是直径为 $2$ 的上半圆，面积为 $\pi/2$，故
$$
F(2)=\frac{\pi}{2}.
$$
在 $[2,3]$ 上是直径为 $1$ 的下半圆，面积为 $-\pi/8$，故
$$
F(3)=\frac{\pi}{2}-\frac{\pi}{8}=\frac{3\pi}{8}.
$$
于是
$$
F(-3)=F(3)=\frac{3\pi}{8}
=\frac{3}{4}F(2).
$$
选 C。

### 第 4 题

**答案：** D

A 中若 $\lim_{x\to0}f(x)/x$ 存在，则 $f(x)\to0$，由连续性得 $f(0)=0$。B 中若 $\lim_{x\to0}[f(x)+f(-x)]/x$ 存在，则分子极限必须为 $0$，即 $2f(0)=0$。C 中由 A 得 $f(0)=0$，所以
$$
f'(0)=\lim_{x\to0}\frac{f(x)-f(0)}{x}
=\lim_{x\to0}\frac{f(x)}{x}
$$
存在。

D 错。例如 $f(x)=|x|$ 在 $0$ 处连续，且
$$
\frac{f(x)-f(-x)}{x}=0
$$
极限存在，但 $f'(0)$ 不存在。故选 D。

### 第 5 题

**答案：** D

由 $f''(x)>0$ 知 $f'(x)$ 在 $(0,+\infty)$ 上严格递增。

若 $u_1<u_2$，则 $f(1)<f(2)$。由拉格朗日中值定理，存在 $\xi\in(1,2)$ 使 $f'(\xi)>0$。由于 $f'$ 递增，$x>\xi$ 时 $f'(x)>f'(\xi)>0$，故 $f(x)\to+\infty$，从而 $\{f(n)\}$ 发散。

若 $u_1>u_2$，既可能收敛，如 $f(x)=1/x$；也可能发散，如 $f(x)=1/x-x$。故只有 D 必然正确。

### 第 6 题

**答案：** B

在曲线 $L:f(x,y)=1$ 上，沿弧 $\Gamma$ 有 $f(x,y)=1$。设 $M=(x_M,y_M)$ 在第二象限，$N=(x_N,y_N)$ 在第四象限，则
$$
x_N-x_M>0,\qquad y_N-y_M<0.
$$
所以
$$
\int_\Gamma f\,dx=\int_\Gamma dx=x_N-x_M>0,
$$
$$
\int_\Gamma f\,dy=\int_\Gamma dy=y_N-y_M<0.
$$
又 $\int_\Gamma f\,ds$ 为弧长，正；而沿等值曲线 $f=1$ 有 $df=f_xdx+f_ydy=0$。故小于零的是 B。

### 第 7 题

**答案：** A

因为
$$
(\boldsymbol{\alpha}_1-\boldsymbol{\alpha}_2)
+(\boldsymbol{\alpha}_2-\boldsymbol{\alpha}_3)
+(\boldsymbol{\alpha}_3-\boldsymbol{\alpha}_1)=0,
$$
所以 A 中三个向量线性相关。故选 A。

### 第 8 题

**答案：** B

矩阵
$$
A=\begin{pmatrix}2&-1&-1\\-1&2&-1\\-1&-1&2\end{pmatrix}
$$
的特征值为 $3,3,0$，而 $B$ 的特征值为 $1,1,0$，故二者不相似。

但二者都是实对称矩阵，且正惯性指数均为 $2$、负惯性指数均为 $0$、零特征值个数均为 $1$。由实二次型合同判别，二者合同。因此选 B。

### 第 9 题

**答案：** C

第 $4$ 次射击恰好第 $2$ 次命中，表示前 $3$ 次中恰有 $1$ 次命中，且第 $4$ 次命中。因此概率为
$$
\binom{3}{1}p(1-p)^2\cdot p=3p^2(1-p)^2.
$$
选 C。

### 第 10 题

**答案：** A

二维正态分布中，不相关等价于相互独立。因此
$$
f_{X,Y}(x,y)=f_X(x)f_Y(y).
$$
条件密度为
$$
f_{X\mid Y}(x\mid y)=\frac{f_{X,Y}(x,y)}{f_Y(y)}
=f_X(x).
$$
选 A。

### 第 11 题

**答案：** $\displaystyle \frac{\sqrt{e}}{2}$

原卷题目为
$$
\int_1^2\frac{1}{x^3}e^{1/x}\,dx.
$$
令 $t=1/x$，则 $dx=-dt/t^2$，$x^{-3}=t^3$。积分化为
$$
\int_{1/2}^{1}t e^t\,dt.
$$
因为
$$
\int t e^t\,dt=(t-1)e^t,
$$
所以
$$
\int_{1/2}^{1}t e^t\,dt
=\left.(t-1)e^t\right|_{1/2}^{1}
=\frac{\sqrt{e}}{2}.
$$

### 第 12 题

**答案：** $\displaystyle yx^{y-1}f'_1+y^x\ln y\,f'_2$

令
$$
u=x^y,\qquad v=y^x.
$$
由链式法则，
$$
\frac{\partial z}{\partial x}
=f'_1(u,v)\frac{\partial u}{\partial x}
+f'_2(u,v)\frac{\partial v}{\partial x}.
$$
又
$$
\frac{\partial}{\partial x}x^y=yx^{y-1},\qquad
\frac{\partial}{\partial x}y^x=y^x\ln y,
$$
故
$$
\frac{\partial z}{\partial x}
=yx^{y-1}f'_1+y^x\ln y\,f'_2.
$$

### 第 13 题

**答案：** $C_1e^{3x}+C_2e^x-2e^{2x}$

对应齐次方程的特征方程为
$$
\lambda^2-4\lambda+3=0,
$$
得 $\lambda=1,3$。齐次通解为
$$
y_h=C_1e^{3x}+C_2e^x.
$$

设特解 $y^*=Ae^{2x}$。代入原方程：
$$
(4A-8A+3A)e^{2x}=2e^{2x},
$$
故 $A=-2$。因此
$$
y=C_1e^{3x}+C_2e^x-2e^{2x}.
$$

### 第 14 题

**答案：** $\displaystyle \frac{4\sqrt{3}}{3}$

曲面
$$
|x|+|y|+|z|=1
$$
关于坐标平面对称，所以
$$
\iint_\Sigma x\,dS=0.
$$
又由对称性，
$$
\iint_\Sigma |x|\,dS
=\iint_\Sigma |y|\,dS
=\iint_\Sigma |z|\,dS.
$$
在曲面上 $|x|+|y|+|z|=1$，故
$$
\iint_\Sigma |y|\,dS
=\frac{1}{3}\iint_\Sigma 1\,dS.
$$
第一卦限内的三角形面积为 $\sqrt{3}/2$，全曲面共有 $8$ 个全等三角形，面积为 $4\sqrt{3}$。因此
$$
\iint_\Sigma(x+|y|)\,dS
=\frac{1}{3}\cdot4\sqrt{3}
=\frac{4\sqrt{3}}{3}.
$$

### 第 15 题

**答案：** $1$

矩阵 $A$ 是四阶 nilpotent Jordan 型上移矩阵。直接计算得
$$
A^3=
\begin{pmatrix}
0&0&0&1\\
0&0&0&0\\
0&0&0&0\\
0&0&0&0
\end{pmatrix}.
$$
因此
$$
r(A^3)=1.
$$

### 第 16 题

**答案：** $\displaystyle \frac{3}{4}$

设两数为 $X,Y$，则样本点在单位正方形
$$
0<X<1,\qquad 0<Y<1
$$
内均匀分布。事件为
$$
|X-Y|<\frac{1}{2}.
$$
在单位正方形中，去掉两块直角三角形：
$$
Y-X\ge\frac{1}{2},\qquad X-Y\ge\frac{1}{2}.
$$
每块面积为 $\frac{1}{2}\cdot\frac{1}{2}\cdot\frac{1}{2}=\frac{1}{8}$，两块合计 $\frac{1}{4}$。故所求概率为
$$
1-\frac{1}{4}=\frac{3}{4}.
$$

### 第 17 题

**答案：** 最大值为 $8$，最小值为 $0$。

先求区域内部驻点：
$$
f_x=2x-2xy^2=2x(1-y^2),\qquad
f_y=4y-2x^2y=2y(2-x^2).
$$
在 $D$ 内得驻点 $(\pm\sqrt{2},1)$，函数值为 $2$。

边界 $y=0$ 上，
$$
f(x,0)=x^2,\qquad -2\le x\le2,
$$
故最小值 $0$，最大值 $4$。

边界 $x^2+y^2=4,\ y\ge0$ 上，令 $y=\sqrt{4-x^2}$，则
$$
h(x)=f(x,\sqrt{4-x^2})=x^4-5x^2+8,\qquad -2\le x\le2.
$$
由
$$
h'(x)=4x^3-10x=2x(2x^2-5)
$$
知需考察 $x=0,\ \pm\sqrt{5/2}$ 及端点。对应函数值为
$$
h(0)=8,\qquad h(\pm\sqrt{5/2})=\frac{7}{4},\qquad h(\pm2)=4.
$$

综合内部和边界，最大值为 $8$，最小值为 $0$。

### 第 18 题

**答案：** $\pi$

用椭圆盘
$$
\Sigma_1:\ z=0,\quad x^2+\frac{y^2}{4}\le1
$$
补成闭曲面。设
$$
P=xz,\qquad Q=2zy,\qquad R=3xy.
$$
则
$$
P_x+Q_y+R_z=z+2z+0=3z.
$$
由高斯公式，闭曲面积分为
$$
\iiint_\Omega 3z\,dV.
$$
截面 $z=\text{常数}$ 时，
$$
x^2+\frac{y^2}{4}\le1-z,
$$
面积为 $2\pi(1-z)$。故
$$
\iiint_\Omega 3z\,dV
=\int_0^1 3z\cdot2\pi(1-z)\,dz
=\pi.
$$
在补面 $\Sigma_1$ 上，$z=0$ 且 $R=3xy$ 关于区域积分为 $0$，所以补面积分为 $0$。原曲面取上侧，与闭曲面方向一致，故
$$
I=\pi.
$$

### 第 19 题

**答案：** 结论成立。

令
$$
h(x)=f(x)-g(x).
$$
则
$$
h(a)=h(b)=0.
$$
设 $f,g$ 在 $(a,b)$ 内的相同最大值为 $M$，分别在 $\alpha,\beta\in(a,b)$ 处取得。

若 $\alpha=\beta$，则
$$
h(\alpha)=f(\alpha)-g(\alpha)=0.
$$
若 $\alpha\ne\beta$，则
$$
h(\alpha)=M-g(\alpha)\ge0,\qquad
h(\beta)=f(\beta)-M\le0.
$$
由介值定理，$\alpha,\beta$ 之间存在 $\eta$ 使 $h(\eta)=0$。

因此总存在 $\eta\in(a,b)$，使
$$
h(a)=h(\eta)=h(b)=0.
$$
对 $h$ 在 $[a,\eta]$ 和 $[\eta,b]$ 上分别用罗尔定理，存在 $\xi_1\in(a,\eta)$、$\xi_2\in(\eta,b)$，使
$$
h'(\xi_1)=h'(\xi_2)=0.
$$
再对 $h'$ 在 $[\xi_1,\xi_2]$ 上用罗尔定理，存在 $\xi\in(\xi_1,\xi_2)\subset(a,b)$，使
$$
h''(\xi)=0.
$$
即
$$
f''(\xi)=g''(\xi).
$$

### 第 20 题

**答案：** $\displaystyle y(x)=xe^{x^2}$

设
$$
y=\sum_{n=0}^{\infty}a_nx^n.
$$
则
$$
y'=\sum_{n=1}^{\infty}na_nx^{n-1},\qquad
y''=\sum_{n=2}^{\infty}n(n-1)a_nx^{n-2}.
$$
代入
$$
y''-2xy'-4y=0
$$
并整理同次幂，得
$$
2a_2-4a_0=0,
$$
以及
$$
(n+1)(n+2)a_{n+2}-2(n+2)a_n=0,\qquad n=1,2,\ldots.
$$
因此
$$
a_{n+2}=\frac{2}{n+1}a_n,\qquad n=1,2,\ldots.
$$

由初值条件 $y(0)=0,\ y'(0)=1$，得
$$
a_0=0,\qquad a_1=1.
$$
于是所有偶数项为 $0$，且
$$
a_{2n+1}=\frac{1}{n!}\qquad(n=0,1,2,\ldots).
$$
所以
$$
y=\sum_{n=0}^{\infty}\frac{x^{2n+1}}{n!}
=x\sum_{n=0}^{\infty}\frac{(x^2)^n}{n!}
=xe^{x^2}.
$$

### 第 21 题

**答案：** $a=1$ 时，公共解为 $k(-1,0,1)^T$；$a=2$ 时，公共解为 $(0,1,-1)^T$。

公共解就是联立方程组
$$
\begin{cases}
x_1+x_2+x_3=0,\\
x_1+2x_2+ax_3=0,\\
x_1+4x_2+a^2x_3=0,\\
x_1+2x_2+x_3=a-1
\end{cases}
$$
的解。

对增广矩阵作初等行变换，可化为
$$
\begin{pmatrix}
1&0&1&|&1-a\\
0&1&0&|&a-1\\
0&0&a-1&|&1-a\\
0&0&0&|&(a-1)(a-2)
\end{pmatrix}.
$$
有解必须满足
$$
(a-1)(a-2)=0,
$$
故
$$
a=1\quad\text{或}\quad a=2.
$$

当 $a=1$ 时，同解方程组为
$$
x_1+x_3=0,\qquad x_2=0,
$$
故公共解为
$$
\boldsymbol{x}=k(-1,0,1)^T.
$$

当 $a=2$ 时，化简得
$$
x_1=0,\qquad x_2=1,\qquad x_3=-1,
$$
故公共解为
$$
\boldsymbol{x}=(0,1,-1)^T.
$$

### 第 22 题

**答案：** $B$ 的特征值为 $-2,1,1$；$\lambda=-2$ 的特征向量为 $k(1,-1,1)^T$，$\lambda=1$ 的特征向量满足 $x-y+z=0$；$\displaystyle B=\begin{pmatrix}0&1&-1\\1&0&1\\-1&1&0\end{pmatrix}$。

设
$$
p(\lambda)=\lambda^5-4\lambda^3+1.
$$
因为 $B=p(A)$，若 $A\boldsymbol{\alpha}=\lambda\boldsymbol{\alpha}$，则
$$
B\boldsymbol{\alpha}=p(\lambda)\boldsymbol{\alpha}.
$$

对 $\lambda_1=1$，
$$
p(1)=1-4+1=-2.
$$
所以
$$
B\boldsymbol{\alpha}_1=-2\boldsymbol{\alpha}_1,
$$
即 $\boldsymbol{\alpha}_1=(1,-1,1)^T$ 是 $B$ 的特征向量，对应特征值 $-2$。

又
$$
p(2)=1,\qquad p(-2)=1,
$$
故 $B$ 的全部特征值为 $-2,1,1$。由于 $A$ 为实对称矩阵，$B=p(A)$ 也为实对称矩阵，不同特征值的特征向量正交。因此属于 $\lambda=1$ 的特征向量均与 $\boldsymbol{\alpha}_1$ 正交：
$$
x-y+z=0.
$$
可取基础向量
$$
(1,1,0)^T,\qquad (-1,0,1)^T.
$$

求矩阵 $B$ 时，用单位向量
$$
u=\frac{1}{\sqrt{3}}(1,-1,1)^T.
$$
$B$ 在 $u$ 方向上的特征值为 $-2$，在其正交平面上的特征值为 $1$，故
$$
B=I+(-2-1)uu^T=I-3uu^T.
$$
又
$$
3uu^T=
\begin{pmatrix}
1&-1&1\\
-1&1&-1\\
1&-1&1
\end{pmatrix},
$$
所以
$$
B=
\begin{pmatrix}
0&1&-1\\
1&0&1\\
-1&1&0
\end{pmatrix}.
$$

### 第 23 题

**答案：** $\displaystyle P\{X>2Y\}=\frac{7}{24}$；$\displaystyle f_Z(z)=z(2-z)\ (0<z<1)$，$\displaystyle f_Z(z)=(2-z)^2\ (1\le z<2)$，其他为 $0$。

(I) 事件 $X>2Y$ 在单位正方形内对应
$$
0<x<1,\qquad 0<y<\frac{x}{2}.
$$
因此
$$
\begin{aligned}
P\{X>2Y\}
&=\int_0^1\int_0^{x/2}(2-x-y)\,dy\,dx\\
&=\int_0^1\left(x-\frac{5}{8}x^2\right)dx\\
&=\frac{7}{24}.
\end{aligned}
$$

(II) 令 $Z=X+Y$。由卷积公式，
$$
f_Z(z)=\int_{-\infty}^{+\infty}f(x,z-x)\,dx.
$$
在支持区域内
$$
f(x,z-x)=2-x-(z-x)=2-z.
$$

当 $0<z<1$ 时，$0<x<z$，故
$$
f_Z(z)=\int_0^z(2-z)\,dx=z(2-z).
$$

当 $1\le z<2$ 时，$z-1<x<1$，故
$$
f_Z(z)=\int_{z-1}^1(2-z)\,dx=(2-z)^2.
$$

其他 $z$ 处密度为 $0$。

### 第 24 题

**答案：** $\displaystyle \hat\theta=2\overline X-\frac{1}{2}$；$4\overline X^2$ 不是 $\theta^2$ 的无偏估计量。

(I) 先求总体均值：
$$
EX=\int_0^\theta x\frac{1}{2\theta}\,dx
+\int_\theta^1x\frac{1}{2(1-\theta)}\,dx
=\frac{1}{4}+\frac{\theta}{2}.
$$
令样本均值等于总体均值：
$$
\overline X=\frac{1}{4}+\frac{\theta}{2},
$$
解得矩估计量
$$
\hat\theta=2\overline X-\frac{1}{2}.
$$

(II) 有
$$
E(4\overline X^2)=4\left[D(\overline X)+(E\overline X)^2\right]
=4\left[\frac{DX}{n}+\left(\frac{1}{4}+\frac{\theta}{2}\right)^2\right].
$$
即
$$
E(4\overline X^2)
=\frac{4}{n}DX+\frac{1}{4}+\theta+\theta^2.
$$
由于 $DX\ge0$ 且 $0<\theta<1$，可知
$$
E(4\overline X^2)\ne\theta^2.
$$
因此 $4\overline X^2$ 不是 $\theta^2$ 的无偏估计量。
