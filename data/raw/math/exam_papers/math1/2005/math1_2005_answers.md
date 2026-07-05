# Math 1 2005 Answers

资料类型：考研数学一答案解析
年份：2005
科目：数学一
范围：试卷 I
来源：D:\百度网盘\高数资料\【02】1987-2022年数学一真题详解答案（PDF）\2005考研数学一真题解析.pdf
校对状态：已按答案页图像和题干重新整理；对原解析省略步骤处补全推导，并更正第 22 题边缘密度区间笔误。

## 答案速查

| 题号 | 题型 | 答案 |
|---|---|---|
| 1 | 填空题 | $\displaystyle y=\frac{1}{2}x-\frac{1}{4}$ |
| 2 | 填空题 | $\displaystyle y=\frac{1}{3}x\ln x-\frac{1}{9}x$ |
| 3 | 填空题 | $\displaystyle \frac{\sqrt{3}}{3}$ |
| 4 | 填空题 | $(2-\sqrt{2})\pi R^3$ |
| 5 | 填空题 | $2$ |
| 6 | 填空题 | $\displaystyle \frac{13}{48}$ |
| 7 | 选择题 | C |
| 8 | 选择题 | A |
| 9 | 选择题 | B |
| 10 | 选择题 | D |
| 11 | 选择题 | B |
| 12 | 选择题 | C |
| 13 | 选择题 | B |
| 14 | 选择题 | D |
| 15 | 解答题 | $\displaystyle \frac{3}{8}$ |
| 16 | 解答题 | 收敛区间为 $(-1,1)$；$\displaystyle f(x)=2x\arctan x-\ln(1+x^2)+\frac{x^2}{1+x^2}$。 |
| 17 | 解答题 | $20$ |
| 18 | 解答题 | 结论成立。 |
| 19 | 解答题 | $\varphi(y)=-y^2$ |
| 20 | 解答题 | $a=0$；可取 $\displaystyle Q=\begin{pmatrix}\frac{1}{\sqrt{2}}&0&-\frac{1}{\sqrt{2}}\\[2pt]\frac{1}{\sqrt{2}}&0&\frac{1}{\sqrt{2}}\\[2pt]0&1&0\end{pmatrix}$，标准形为 $2y_1^2+2y_2^2$；方程通解为 $\boldsymbol{x}=k(-1,1,0)^T$。 |
| 21 | 解答题 | 若 $k\ne9$，通解为 $\boldsymbol{x}=c_1(1,2,3)^T+c_2(3,6,k)^T$。若 $k=9$ 且 $r(A)=2$，通解为 $\boldsymbol{x}=c(1,2,3)^T$；若 $k=9$ 且 $r(A)=1$，通解为所有满足 $ax_1+bx_2+cx_3=0$ 的向量。 |
| 22 | 解答题 | $f_X(x)=2x\ (0<x<1)$，否则为 $0$；$f_Y(y)=1-\dfrac{y}{2}\ (0<y<2)$，否则为 $0$；$f_Z(z)=1-\dfrac{z}{2}\ (0<z<2)$，否则为 $0$。 |
| 23 | 解答题 | $\displaystyle D(Y_i)=\frac{n-1}{n}\ (i=1,2,\ldots,n)$；$\displaystyle \operatorname{Cov}(Y_1,Y_n)=-\frac{1}{n}$。 |

## 详细解析

### 第 1 题

**答案：** $\displaystyle y=\frac{1}{2}x-\frac{1}{4}$

对函数作多项式除法：
$$
\frac{x^2}{2x+1}
=\frac{1}{2}x-\frac{1}{4}+\frac{1}{4(2x+1)}.
$$

当 $x\to\infty$ 时，最后一项趋于 $0$，所以斜渐近线为
$$
y=\frac{1}{2}x-\frac{1}{4}.
$$

### 第 2 题

**答案：** $\displaystyle y=\frac{1}{3}x\ln x-\frac{1}{9}x$

原方程
$$
xy'+2y=x\ln x
$$
在 $x>0$ 时等价于
$$
y'+\frac{2}{x}y=\ln x.
$$

积分因子为
$$
\mu(x)=e^{\int 2/x\,dx}=x^2.
$$
于是
$$
(x^2y)'=x^2\ln x.
$$

积分得
$$
x^2y=\int x^2\ln x\,dx
=\frac{x^3}{3}\ln x-\frac{x^3}{9}+C,
$$
即
$$
y=\frac{1}{3}x\ln x-\frac{1}{9}x+\frac{C}{x^2}.
$$

由 $y(1)=-\dfrac{1}{9}$ 得 $C=0$，所以
$$
y=\frac{1}{3}x\ln x-\frac{1}{9}x.
$$

### 第 3 题

**答案：** $\displaystyle \frac{\sqrt{3}}{3}$

先求梯度：
$$
\nabla u
=\left(\frac{x}{3},\frac{y}{6},\frac{z}{9}\right).
$$

在 $(1,2,3)$ 处，
$$
\nabla u(1,2,3)
=\left(\frac{1}{3},\frac{1}{3},\frac{1}{3}\right).
$$

方向导数为梯度与单位方向向量的点积：
$$
\left.\frac{\partial u}{\partial n}\right|_{(1,2,3)}
=\left(\frac{1}{3},\frac{1}{3},\frac{1}{3}\right)\cdot
\frac{1}{\sqrt{3}}(1,1,1)
=\frac{1}{\sqrt{3}}
=\frac{\sqrt{3}}{3}.
$$

### 第 4 题

**答案：** $(2-\sqrt{2})\pi R^3$

由高斯公式，
$$
\iint_{\Sigma}x\,dy\,dz+y\,dz\,dx+z\,dx\,dy
=\iiint_\Omega
\left(\frac{\partial x}{\partial x}+\frac{\partial y}{\partial y}+\frac{\partial z}{\partial z}\right)dV
=3V(\Omega).
$$

在球坐标中，锥面 $z=\sqrt{x^2+y^2}$ 对应 $\varphi=\pi/4$，上半球对应 $0\le r\le R$。故
$$
V(\Omega)=\int_0^{2\pi}\int_0^{\pi/4}\int_0^R
r^2\sin\varphi\,dr\,d\varphi\,d\theta.
$$

于是
$$
\begin{aligned}
3V(\Omega)
&=3\cdot2\pi\cdot
\left(1-\frac{\sqrt{2}}{2}\right)\cdot\frac{R^3}{3}\\
&=(2-\sqrt{2})\pi R^3.
\end{aligned}
$$

### 第 5 题

**答案：** $2$

由题意，
$$
B=(\boldsymbol{\alpha}_1,\boldsymbol{\alpha}_2,\boldsymbol{\alpha}_3)
\begin{pmatrix}
1&1&1\\
1&2&3\\
1&4&9
\end{pmatrix}
=AC.
$$

因此
$$
\det B=\det A\,\det C.
$$

矩阵 $C$ 是范德蒙德型矩阵，对应 $1,2,3$，所以
$$
\det C=(2-1)(3-1)(3-2)=2.
$$

又 $\det A=1$，故
$$
\det B=2.
$$

### 第 6 题

**答案：** $\displaystyle \frac{13}{48}$

按全概率公式，
$$
P\{Y=2\}
=\sum_{k=1}^4P\{X=k\}P\{Y=2\mid X=k\}.
$$

当 $X=1$ 时不可能取到 $Y=2$；当 $X=2,3,4$ 时，
$$
P\{Y=2\mid X=2\}=\frac{1}{2},\quad
P\{Y=2\mid X=3\}=\frac{1}{3},\quad
P\{Y=2\mid X=4\}=\frac{1}{4}.
$$

又 $P\{X=k\}=\dfrac{1}{4}$，所以
$$
P\{Y=2\}
=\frac{1}{4}\left(0+\frac{1}{2}+\frac{1}{3}+\frac{1}{4}\right)
=\frac{13}{48}.
$$

### 第 7 题

**答案：** C

利用
$$
\lim_{n\to\infty}(a^n+b^n)^{1/n}=\max\{a,b\}\qquad(a,b\ge0),
$$
可得
$$
f(x)=\max\{1,|x|^3\}
=
\begin{cases}
1,& |x|\le1,\\
|x|^3,& |x|>1.
\end{cases}
$$

在 $x=1$ 处，左导数为 $0$，右导数为 $3$；在 $x=-1$ 处，左导数为 $-3$，右导数为 $0$。所以这两点不可导。

其余点处函数由常数函数或光滑函数 $|x|^3$ 给出，均可导。因此恰有两个不可导点，选 C。

### 第 8 题

**答案：** A

若 $F(x)$ 为偶函数，则
$$
F(-x)=F(x).
$$
两边对 $x$ 求导，得
$$
-F'(-x)=F'(x),
$$
即
$$
f(-x)=-f(x),
$$
所以 $f(x)$ 为奇函数。

反过来，若 $f(x)$ 为奇函数，则
$$
\int_0^x f(t)\,dt
$$
为偶函数，而 $F(x)$ 与它只差一个常数；偶函数加常数仍为偶函数。因此 $F(x)$ 为偶函数。

所以必有
$$
F(x)\text{ 为偶函数}\Longleftrightarrow f(x)\text{ 为奇函数}.
$$
选 A。

### 第 9 题

**答案：** B

分别求偏导：
$$
u_x=\varphi'(x+y)+\varphi'(x-y)+\psi(x+y)-\psi(x-y),
$$
$$
u_y=\varphi'(x+y)-\varphi'(x-y)+\psi(x+y)+\psi(x-y).
$$

继续求二阶偏导：
$$
u_{xx}
=\varphi''(x+y)+\varphi''(x-y)+\psi'(x+y)-\psi'(x-y),
$$
$$
u_{yy}
=\varphi''(x+y)+\varphi''(x-y)+\psi'(x+y)-\psi'(x-y).
$$

因此
$$
\frac{\partial^2u}{\partial x^2}
=\frac{\partial^2u}{\partial y^2}.
$$
选 B。

### 第 10 题

**答案：** D

设
$$
F(x,y,z)=xy-z\ln y+e^{xz}-1.
$$
显然 $F(0,1,1)=0$。计算偏导：
$$
F_x=y+ze^{xz},\qquad
F_y=x-\frac{z}{y},\qquad
F_z=-\ln y+xe^{xz}.
$$

在 $(0,1,1)$ 处，
$$
F_x(0,1,1)=2\ne0,\qquad
F_y(0,1,1)=-1\ne0,\qquad
F_z(0,1,1)=0.
$$

由隐函数存在定理，能确定以 $x$ 为因变量的隐函数 $x=x(y,z)$，也能确定以 $y$ 为因变量的隐函数 $y=y(x,z)$；但不能由该定理确定 $z=z(x,y)$。选 D。

### 第 11 题

**答案：** B

因为 $\lambda_1,\lambda_2$ 是不同特征值，所以对应特征向量 $\boldsymbol{\alpha}_1,\boldsymbol{\alpha}_2$ 线性无关。

有
$$
A(\boldsymbol{\alpha}_1+\boldsymbol{\alpha}_2)
=\lambda_1\boldsymbol{\alpha}_1+\lambda_2\boldsymbol{\alpha}_2.
$$

若
$$
k_1\boldsymbol{\alpha}_1
+k_2A(\boldsymbol{\alpha}_1+\boldsymbol{\alpha}_2)=0,
$$
则
$$
(k_1+k_2\lambda_1)\boldsymbol{\alpha}_1
+k_2\lambda_2\boldsymbol{\alpha}_2=0.
$$

由线性无关性，必须有
$$
k_1+k_2\lambda_1=0,\qquad k_2\lambda_2=0.
$$
因此只有当 $\lambda_2\ne0$ 时，必有 $k_2=0$，进而 $k_1=0$，两向量线性无关。选 B。

### 第 12 题

**答案：** C

设交换第 $1$ 行与第 $2$ 行的初等矩阵为 $P$，则
$$
B=PA.
$$

因为 $P^{-1}=P$ 且 $\det P=-1$，所以
$$
B^*=\det(B)B^{-1}
=\det(PA)(PA)^{-1}
=-\det(A)A^{-1}P
=-A^*P.
$$

右乘 $P$ 表示交换列，因此 $A^*P$ 正是交换 $A^*$ 的第 $1$ 列与第 $2$ 列所得矩阵。由
$$
A^*P=-B^*
$$
知，交换 $A^*$ 的第 $1$ 列与第 $2$ 列得到 $-B^*$。选 C。

### 第 13 题

**答案：** D

由概率分布总和为 $1$，得
$$
0.4+a+b+0.1=1,
$$
即
$$
a+b=0.5.
$$

事件 $\{X=0\}$ 与 $\{X+Y=1\}$ 独立。注意
$$
P\{X=0\}=0.4+a,\qquad
P\{X+Y=1\}=a+b=0.5,
$$
且
$$
P\{X=0,\ X+Y=1\}=P\{X=0,Y=1\}=a.
$$

独立性给出
$$
a=(0.4+a)\cdot0.5,
$$
故
$$
a=0.4,\qquad b=0.1.
$$
选 B。

### 第 14 题

**答案：** D

因为样本来自 $N(0,1)$，所以
$$
X_1^2\sim\chi^2(1),
\qquad
\sum_{i=2}^n X_i^2\sim\chi^2(n-1),
$$
且两者相互独立。

于是
$$
\frac{X_1^2/1}{\left(\sum_{i=2}^nX_i^2\right)/(n-1)}
=\frac{(n-1)X_1^2}{\sum_{i=2}^nX_i^2}
\sim F(1,n-1).
$$

故 D 正确。其他选项中，$n\overline X$ 的方差不是 $1$；样本方差满足 $(n-1)S^2\sim\chi^2(n-1)$；构造 $t$ 分布时应出现 $\sqrt{n}\,\overline X/S$，不是 $(n-1)\overline X/S$。

### 第 15 题

**答案：** $\displaystyle \frac{3}{8}$

在极坐标下，
$$
x=r\cos\theta,\qquad y=r\sin\theta,
$$
区域 $D$ 为
$$
0\le\theta\le\frac{\pi}{2},\qquad
0\le r\le \sqrt[4]{2}.
$$

又
$$
[1+x^2+y^2]=[1+r^2].
$$
当 $0\le r<1$ 时，$[1+r^2]=1$；当 $1\le r\le\sqrt[4]{2}$ 时，$[1+r^2]=2$。端点不影响积分。

于是
$$
\begin{aligned}
\iint_D xy[1+x^2+y^2]\,dx\,dy
&=\int_0^{\pi/2}\sin\theta\cos\theta\,d\theta
\left(\int_0^1r^3\,dr+\int_1^{\sqrt[4]{2}}2r^3\,dr\right)\\
&=\frac{1}{2}\left(\frac{1}{4}+\frac{1}{2}\right)\\
&=\frac{3}{8}.
\end{aligned}
$$

### 第 16 题

**答案：** 收敛区间为 $(-1,1)$；$\displaystyle f(x)=2x\arctan x-\ln(1+x^2)+\frac{x^2}{1+x^2}$。

设
$$
a_n=\left[1+\frac{1}{n(2n-1)}\right]x^{2n}.
$$
由根值判别可知收敛半径满足 $|x|<1$。当 $x=\pm1$ 时，通项
$$
(-1)^{n-1}\left[1+\frac{1}{n(2n-1)}\right]
$$
不趋于 $0$，故两端点均发散。因此收敛区间为
$$
(-1,1).
$$

在 $|x|<1$ 内，将原级数拆为
$$
f(x)=\sum_{n=1}^{\infty}(-1)^{n-1}x^{2n}
+\sum_{n=1}^{\infty}\frac{(-1)^{n-1}}{n(2n-1)}x^{2n}.
$$

第一部分为
$$
\sum_{n=1}^{\infty}(-1)^{n-1}x^{2n}
=\frac{x^2}{1+x^2}.
$$

记
$$
S(x)=\sum_{n=1}^{\infty}\frac{(-1)^{n-1}}{2n(2n-1)}x^{2n}.
$$
则
$$
S''(x)=\sum_{n=1}^{\infty}(-1)^{n-1}x^{2n-2}
=\frac{1}{1+x^2}.
$$
又 $S(0)=S'(0)=0$，故
$$
S'(x)=\int_0^x\frac{dt}{1+t^2}=\arctan x,
$$
$$
S(x)=\int_0^x\arctan t\,dt
=x\arctan x-\frac{1}{2}\ln(1+x^2).
$$

原级数第二部分等于 $2S(x)$，所以
$$
f(x)
=\frac{x^2}{1+x^2}+2S(x)
=2x\arctan x-\ln(1+x^2)+\frac{x^2}{1+x^2}.
$$

### 第 17 题

**答案：** $20$

由图可读出切线信息。切线 $l_1$ 过 $(0,0)$ 与 $(2,4)$，故
$$
f'(0)=2.
$$
切线 $l_2$ 过 $(3,2)$ 与 $(2,4)$，故
$$
f'(3)=\frac{4-2}{2-3}=-2.
$$
又 $(3,2)$ 是拐点，且 $f$ 具有三阶连续导数，所以
$$
f''(3)=0.
$$

对积分分部积分：
$$
\begin{aligned}
\int_0^3(x^2+x)f'''(x)\,dx
&=\left.(x^2+x)f''(x)\right|_0^3-\int_0^3(2x+1)f''(x)\,dx\\
&=-\left.(2x+1)f'(x)\right|_0^3+2\int_0^3f'(x)\,dx.
\end{aligned}
$$

代入 $f'(0)=2,\ f'(3)=-2,\ f(3)=2,\ f(0)=0$：
$$
\begin{aligned}
\int_0^3(x^2+x)f'''(x)\,dx
&=-\bigl[7f'(3)-f'(0)\bigr]+2[f(3)-f(0)]\\
&=-[7(-2)-2]+2(2-0)\\
&=16+4\\
&=20.
\end{aligned}
$$

### 第 18 题

**答案：** 结论成立。

(I) 令
$$
g(x)=f(x)+x-1.
$$
则 $g(x)$ 在 $[0,1]$ 上连续，并且
$$
g(0)=-1<0,\qquad g(1)=1>0.
$$
由介值定理，存在 $\xi\in(0,1)$，使
$$
g(\xi)=0,
$$
即
$$
f(\xi)=1-\xi.
$$

(II) 由拉格朗日中值定理，在区间 $(0,\xi)$ 内存在 $\eta$，使
$$
f'(\eta)=\frac{f(\xi)-f(0)}{\xi-0}
=\frac{1-\xi}{\xi}.
$$
在区间 $(\xi,1)$ 内存在 $\zeta$，使
$$
f'(\zeta)=\frac{f(1)-f(\xi)}{1-\xi}
=\frac{1-(1-\xi)}{1-\xi}
=\frac{\xi}{1-\xi}.
$$

因为 $\eta\in(0,\xi)$，$\zeta\in(\xi,1)$，两点不同。且
$$
f'(\eta)f'(\zeta)
=\frac{1-\xi}{\xi}\cdot\frac{\xi}{1-\xi}
=1.
$$

### 第 19 题

**答案：** $\varphi(y)=-y^2$

记
$$
P(x,y)=\frac{\varphi(y)}{2x^2+y^4},\qquad
Q(x,y)=\frac{2xy}{2x^2+y^4}.
$$

(I) 题设说明，凡围绕原点的分段光滑简单闭曲线，其积分值都相同。若 $C$ 位于右半平面 $x>0$ 内，可把 $C$ 与一条围绕原点的辅助闭曲线组合成两条同向围绕原点的闭曲线；这两条曲线的积分值相同，相减后正好得到
$$
\oint_C P\,dx+Q\,dy=0.
$$
因此对右半平面 $x>0$ 内任意分段光滑简单闭曲线 $C$，有
$$
\oint_C\frac{\varphi(y)\,dx+2xy\,dy}{2x^2+y^4}=0.
$$

(II) 右半平面为单连通区域，且上式对任意闭曲线成立，所以在 $x>0$ 内有
$$
\frac{\partial Q}{\partial x}=\frac{\partial P}{\partial y}.
$$

分别计算：
$$
\frac{\partial Q}{\partial x}
=\frac{-4x^2y+2y^5}{(2x^2+y^4)^2},
$$
$$
\frac{\partial P}{\partial y}
=\frac{2x^2\varphi'(y)+y^4\varphi'(y)-4y^3\varphi(y)}
{(2x^2+y^4)^2}.
$$

比较分子中关于 $x^2$ 的系数，得
$$
2\varphi'(y)=-4y,
$$
即
$$
\varphi'(y)=-2y.
$$
故
$$
\varphi(y)=-y^2+C.
$$

再比较不含 $x^2$ 的项：
$$
y^4\varphi'(y)-4y^3\varphi(y)=2y^5.
$$
代入 $\varphi'(y)=-2y$ 与 $\varphi(y)=-y^2+C$，得
$$
-2y^5-4y^3(-y^2+C)=2y^5,
$$
从而 $C=0$。因此
$$
\varphi(y)=-y^2.
$$

### 第 20 题

**答案：** $a=0$；可取 $\displaystyle Q=\begin{pmatrix}\frac{1}{\sqrt{2}}&0&-\frac{1}{\sqrt{2}}\\[2pt]\frac{1}{\sqrt{2}}&0&\frac{1}{\sqrt{2}}\\[2pt]0&1&0\end{pmatrix}$，标准形为 $2y_1^2+2y_2^2$；方程通解为 $\boldsymbol{x}=k(-1,1,0)^T$。

二次型对应的对称矩阵为
$$
A=\begin{pmatrix}
1-a&1+a&0\\
1+a&1-a&0\\
0&0&2
\end{pmatrix}.
$$

(I) 已知二次型的秩为 $2$。由于第三个对角块 $2$ 非零，只需令左上 $2$ 阶块秩为 $1$：
$$
\begin{vmatrix}
1-a&1+a\\
1+a&1-a
\end{vmatrix}
=(1-a)^2-(1+a)^2=-4a=0.
$$
故
$$
a=0.
$$

(II) 当 $a=0$ 时，
$$
A=\begin{pmatrix}
1&1&0\\
1&1&0\\
0&0&2
\end{pmatrix}.
$$
其特征值为
$$
2,2,0.
$$
可取对应的两两正交单位特征向量
$$
e_1=\frac{1}{\sqrt{2}}(1,1,0)^T,\qquad
e_2=(0,0,1)^T,\qquad
e_3=\frac{1}{\sqrt{2}}(-1,1,0)^T.
$$
令
$$
Q=(e_1,e_2,e_3)
=\begin{pmatrix}
\frac{1}{\sqrt{2}}&0&-\frac{1}{\sqrt{2}}\\
\frac{1}{\sqrt{2}}&0&\frac{1}{\sqrt{2}}\\
0&1&0
\end{pmatrix}.
$$
则 $Q$ 为正交矩阵。在正交变换 $\boldsymbol{x}=Q\boldsymbol{y}$ 下，
$$
f=2y_1^2+2y_2^2.
$$

(III) 方程 $f=0$ 化为
$$
2y_1^2+2y_2^2=0,
$$
故
$$
y_1=0,\qquad y_2=0.
$$
于是
$$
\boldsymbol{x}=y_3e_3=k(-1,1,0)^T,
$$
其中 $k$ 为任意常数。

也可直接由
$$
f=(x_1+x_2)^2+2x_3^2=0
$$
得到 $x_1+x_2=0,\ x_3=0$，同样推出上述通解。

### 第 21 题

**答案：** 若 $k\ne9$，通解为 $\boldsymbol{x}=c_1(1,2,3)^T+c_2(3,6,k)^T$。若 $k=9$ 且 $r(A)=2$，通解为 $\boldsymbol{x}=c(1,2,3)^T$；若 $k=9$ 且 $r(A)=1$，通解为所有满足 $ax_1+bx_2+cx_3=0$ 的向量。

由 $AB=O$ 及秩不等式，
$$
r(A)+r(B)\le3.
$$
又因为 $A$ 的第一行 $(a,b,c)$ 不全为零，所以
$$
r(A)\ge1.
$$

矩阵
$$
B=\begin{pmatrix}
1&2&3\\
2&4&6\\
3&6&k
\end{pmatrix}
$$
的前两列线性相关，且当 $k\ne9$ 时，
$$
(1,2,3)^T,\quad (3,6,k)^T
$$
线性无关，所以 $r(B)=2$。此时 $r(A)=1$，方程组 $A\boldsymbol{x}=0$ 的解空间维数为 $2$。由 $AB=O$ 知 $B$ 的列向量均为 $A\boldsymbol{x}=0$ 的解，因此
$$
(1,2,3)^T,\quad (3,6,k)^T
$$
构成基础解系，通解为
$$
\boldsymbol{x}=c_1(1,2,3)^T+c_2(3,6,k)^T.
$$

当 $k=9$ 时，$r(B)=1$，且 $B$ 的列空间由
$$
(1,2,3)^T
$$
张成，因此
$$
A(1,2,3)^T=0.
$$
此时由 $r(A)+r(B)\le3$ 知 $r(A)=1$ 或 $r(A)=2$。

若 $r(A)=2$，则 $A\boldsymbol{x}=0$ 的解空间维数为 $1$，故
$$
\boldsymbol{x}=c(1,2,3)^T.
$$

若 $r(A)=1$，则 $A$ 的各行都与第一行成比例，方程组等价于
$$
ax_1+bx_2+cx_3=0.
$$
因此通解就是该平面上的全部向量。若需要给出一组具体基础解系，并且 $a\ne0$，可取
$$
(-b,a,0)^T,\qquad (-c,0,a)^T,
$$
于是
$$
\boldsymbol{x}=c_1(-b,a,0)^T+c_2(-c,0,a)^T.
$$
当 $a=0$ 时，可按 $b$ 或 $c$ 的非零情况类似选取两组独立解。

### 第 22 题

**答案：** $f_X(x)=2x\ (0<x<1)$，否则为 $0$；$f_Y(y)=1-\dfrac{y}{2}\ (0<y<2)$，否则为 $0$；$f_Z(z)=1-\dfrac{z}{2}\ (0<z<2)$，否则为 $0$。

(I) 对 $X$ 的边缘密度，
$$
f_X(x)=\int_{-\infty}^{+\infty}f(x,y)\,dy.
$$
当 $0<x<1$ 时，$0<y<2x$，故
$$
f_X(x)=\int_0^{2x}1\,dy=2x.
$$
其他 $x$ 处为 $0$。因此
$$
f_X(x)=
\begin{cases}
2x,&0<x<1,\\
0,&\text{其他}.
\end{cases}
$$

对 $Y$ 的边缘密度，给定 $y$ 后需满足
$$
0<x<1,\qquad 0<y<2x,
$$
即
$$
\frac{y}{2}<x<1.
$$
这要求 $0<y<2$。所以
$$
f_Y(y)=\int_{y/2}^{1}1\,dx=1-\frac{y}{2}\qquad(0<y<2),
$$
即
$$
f_Y(y)=
\begin{cases}
1-\dfrac{y}{2},&0<y<2,\\
0,&\text{其他}.
\end{cases}
$$

(II) 令
$$
Z=2X-Y.
$$
在原支持区域 $0<y<2x,\ 0<x<1$ 内，有 $0<z<2$。作变量代换
$$
z=2x-y,\qquad y=2x-z,
$$
雅可比绝对值为 $1$。当给定 $0<z<2$ 时，条件 $0<2x-z$ 与 $x<1$ 给出
$$
\frac{z}{2}<x<1.
$$
因此
$$
f_Z(z)=\int_{z/2}^{1}1\,dx=1-\frac{z}{2}\qquad(0<z<2).
$$

所以
$$
f_Z(z)=
\begin{cases}
1-\dfrac{z}{2},&0<z<2,\\
0,&\text{其他}.
\end{cases}
$$

### 第 23 题

**答案：** $\displaystyle D(Y_i)=\frac{n-1}{n}\ (i=1,2,\ldots,n)$；$\displaystyle \operatorname{Cov}(Y_1,Y_n)=-\frac{1}{n}$。

因为 $X_1,\ldots,X_n$ 独立同分布于 $N(0,1)$，所以
$$
D(X_i)=1,\qquad D(\overline X)=\frac{1}{n},
$$
且
$$
\operatorname{Cov}(X_i,\overline X)
=\operatorname{Cov}\left(X_i,\frac{1}{n}\sum_{j=1}^nX_j\right)
=\frac{1}{n}.
$$

(I) 由 $Y_i=X_i-\overline X$，
$$
\begin{aligned}
D(Y_i)
&=D(X_i-\overline X)\\
&=D(X_i)+D(\overline X)-2\operatorname{Cov}(X_i,\overline X)\\
&=1+\frac{1}{n}-2\cdot\frac{1}{n}\\
&=\frac{n-1}{n}.
\end{aligned}
$$

(II) 当 $1\ne n$ 时，$X_1$ 与 $X_n$ 独立，故 $\operatorname{Cov}(X_1,X_n)=0$。于是
$$
\begin{aligned}
\operatorname{Cov}(Y_1,Y_n)
&=\operatorname{Cov}(X_1-\overline X,\ X_n-\overline X)\\
&=\operatorname{Cov}(X_1,X_n)
-\operatorname{Cov}(X_1,\overline X)
-\operatorname{Cov}(\overline X,X_n)
+D(\overline X)\\
&=0-\frac{1}{n}-\frac{1}{n}+\frac{1}{n}\\
&=-\frac{1}{n}.
\end{aligned}
$$
