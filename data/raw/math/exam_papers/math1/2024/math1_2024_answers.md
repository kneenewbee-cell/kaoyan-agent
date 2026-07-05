# 2024 数学一答案解析

资料类型：考研数学一答案解析
年份：2024
科目：数学一
整理状态：已根据答案页图像、题图与题干推导清洗

## 答案速查

### 选择题

| 题号 | 答案 |
|---|---|
| 1 | C |
| 2 | A |
| 3 | A |
| 4 | B |
| 5 | B |
| 6 | D |
| 7 | A |
| 8 | B |
| 9 | D |
| 10 | D |

### 填空题

| 题号 | 答案 |
|---|---|
| 11 | $a=6$ |
| 12 | $5$ |
| 13 | $-\dfrac{1}{\pi}$ |
| 14 | $\arctan(x+y)=y+\dfrac{\pi}{4}$ |
| 15 | $a\ge0$ |
| 16 | $p=\dfrac{2}{3}$ |

### 解答题

| 题号 | 答案要点 |
|---|---|
| 17 | $\ln(\sqrt{2}+1)+\sqrt{2}-2$。 |
| 18 | (I) 切平面为 $$ x+y+z=3. $$  (II) 最大值为 $21$，在 $(3,0)$ 与 $(0,3)$ 处取得；最小值为 $\dfrac{17}{27}$，在 $\left(\dfrac{4}{3},\dfrac{4}{3}\right)$ 处取得。 |
| 19 | 证明见解析。 |
| 20 | $\displaystyle \frac{4\sqrt{5}}{25}\pi$。 |
| 21 | 矩阵 $$ A=\begin{pmatrix} -2&0&2\\ 0&-2&-2\\ -6&-3&3 \end{pmatrix}. $$ 当 $n\ge1$ 时， $$ A^n= \begin{pmatrix} (-1)^{n+1}2^n-4&(-1)^{n+1}2^n-2&2\\ (-1)^n2^{n+1}+4&(-1)^n2^{n+1}+2&-2\\ -6&-3&3 \end{pmatrix}, $$ 并且 $$ \begin{pmatrix}x_n\\y_n\\z_n\end{pmatrix} =\begin{pmatrix} (-2)^n+8\\ (-2)^{n+1}-8\\ 12 \end{pmatrix}. $$ |
| 22 | (I) $$ c=\frac{n+1}{n}. $$  (II) 当 $$ c=\frac{n+2}{n+1} $$ 时，$h(c)$ 取得最小值。 |

## 详细解析

### 第 1 题

**答案：** C

$e^{\cos t}$ 是偶函数，所以
$$
f(-x)=\int_0^{-x}e^{\cos t}\,dt=-\int_0^x e^{\cos u}\,du=-f(x),
$$
故 $f$ 为奇函数。

令
$$
F(u)=\int_0^u e^{t^2}\,dt.
$$
因 $e^{t^2}$ 为偶函数，$F$ 为奇函数；又 $\sin x$ 是奇函数，所以
$$
g(-x)=F(\sin(-x))=F(-\sin x)=-F(\sin x)=-g(x).
$$
故 $g$ 也是奇函数，选 C。

### 第 2 题

**答案：** A

对上侧曲面 $z=z(x,y)$，有
$$
dy\,dz=-z_x\,dxdy,\qquad dz\,dx=-z_y\,dxdy.
$$
这里
$$
z_x=-\frac{x}{z},\qquad z_y=-\frac{y}{z}.
$$
因此
$$
\iint_\Sigma P\,dy\,dz+Q\,dz\,dx
=\iint_D\left(P\frac{x}{z}+Q\frac{y}{z}\right)dxdy.
$$
选 A。

### 第 3 题

**答案：** A

在 $x=0$ 附近，
$$
\ln(2+x)=\ln2+\ln\left(1+\frac{x}{2}\right)
=\ln2+\sum_{k=1}^{\infty}(-1)^{k-1}\frac{x^k}{k2^k}.
$$
所以当 $n\ge1$ 时
$$
a_{2n}=-\frac{1}{2n\,2^{2n}}.
$$
于是
$$
\sum_{n=0}^{\infty}n a_{2n}
=\sum_{n=1}^{\infty}n\left(-\frac{1}{2n\,4^n}\right)
=-\frac{1}{2}\sum_{n=1}^{\infty}\frac{1}{4^n}
=-\frac{1}{6}.
$$
选 A。

### 第 4 题

**答案：** B

若 $f'(0)=m$，则 $f$ 在 $0$ 处连续。又题设给出 $\lim_{x\to0}f(x)=0$，所以 $f(0)=0$。于是
$$
\lim_{x\to0}\frac{f(x)}{x}
=\lim_{x\to0}\frac{f(x)-f(0)}{x-0}
=f'(0)=m.
$$
故 B 正确。

A 未要求 $f(0)=0$；C 未保证 $f'(0)$ 存在并等于该极限；D 则把一点可导误认为导函数连续，均不一定成立。

### 第 5 题

**答案：** B

由图可知三平面交于同一条直线，但三平面不重合。于是方程组有无穷多解，且解集是一条直线。

因此系数矩阵秩为 $2$，增广矩阵秩也为 $2$：
$$
m=r(\alpha_1,\alpha_2,\alpha_3)=2,\qquad
n=r(\beta_1,\beta_2,\beta_3)=2.
$$
故选 B。

### 第 6 题

**答案：** D

令 $M=(\alpha_1,\alpha_2,\alpha_3)$。题设等价于
$$
r(M)=2
$$
且任意两列线性无关。对 $M$ 作初等行变换可得：若 $a=1$，则 $\alpha_1$ 与 $\alpha_3$ 相关，不合题意。

当 $a\ne1$ 时，进一步化简后，线性相关要求
$$
a+2=0,\qquad -b(a+1)-2=0.
$$
解得
$$
a=-2,\qquad b=2.
$$
此时任意两列均线性无关，故选 D。

### 第 7 题

**答案：** A

由 $A\alpha=0$ 且 $r(A)=2$ 可知 $0$ 是单特征值，$\alpha$ 是其特征向量。

又所有满足 $\beta^T\alpha=0$ 的向量组成一个二维子空间，且在该子空间上 $A\beta=\beta$，故 $1$ 是二重特征值。于是 $A$ 可对角化，相似于
$$
\operatorname{diag}(1,1,0).
$$
因此
$$
\operatorname{tr}(A^3)=1^3+1^3+0^3=2.
$$
选 A。

### 第 8 题

**答案：** B

由独立性，
$$
2X+Y\sim N(-2,10),\qquad X-Y\sim N(2,4).
$$
因此
$$
P\{X>Y\}=P\{X-Y>0\}
=P\left\{\frac{X-Y-2}{2}>-1\right\}
=\Phi(1).
$$
又
$$
P\{2X+Y<a\}=\Phi\left(\frac{a+2}{\sqrt{10}}\right).
$$
故
$$
\frac{a+2}{\sqrt{10}}=1,\qquad a=-2+\sqrt{10}.
$$
选 B。

### 第 9 题

**答案：** D

条件密度为
$$
f_{Y|X}(y|x)=\frac{1}{1-x},\qquad x<y<1.
$$
于是联合密度为
$$
f(x,y)=f_X(x)f_{Y|X}(y|x)=2,\qquad 0<x<y<1.
$$
因此
$$
E(X)=\int_0^1 2x(1-x)\,dx=\frac{1}{3},
$$
$$
E(XY)=\int_0^1\int_x^1 2xy\,dy\,dx=\frac{1}{4}.
$$
边缘密度
$$
f_Y(y)=\int_0^y2\,dx=2y,\qquad 0<y<1,
$$
故
$$
E(Y)=\int_0^1 2y^2\,dy=\frac{2}{3}.
$$
于是
$$
\operatorname{Cov}(X,Y)=E(XY)-E(X)E(Y)=\frac{1}{4}-\frac{2}{9}=\frac{1}{36}.
$$
选 D。

### 第 10 题

**答案：** D

当 $z\ge0$ 时，
$$
F_Z(z)=P\{|X-Y|\le z\}=2P\{0\le X-Y\le z\}.
$$
由联合密度 $\lambda^2e^{-\lambda(x+y)}$ 得
$$
F_Z(z)=2\int_0^\infty\int_y^{y+z}\lambda^2e^{-\lambda(x+y)}\,dx\,dy
=1-e^{-\lambda z}.
$$
这正是参数为 $\lambda$ 的指数分布函数。故 $Z$ 与 $X$ 同分布，选 D。

### 第 11 题

**答案：** $a=6$

当 $x\to0$ 时，
$$
(1+ax^2)^{\sin x}
=\exp\left(\sin x\ln(1+ax^2)\right).
$$
又
$$
\sin x\ln(1+ax^2)\sim x\cdot ax^2=ax^3,
$$
所以
$$
(1+ax^2)^{\sin x}-1\sim ax^3.
$$
由极限等于 $6$ 得 $a=6$。

### 第 12 题

**答案：** $5$

由 $df|_{(1,1)}=3\,du+4\,dv$ 得
$$
f_u(1,1)=3,\qquad f_v(1,1)=4.
$$
记 $u=\cos x,\ v=1+x^2$。当 $x=0$ 时，$u=1,v=1$，且
$$
u'(0)=0,\quad v'(0)=0,\quad u''(0)=-1,\quad v''(0)=2.
$$
由于一阶导数在 $0$ 处为零，二阶链式法则中只留下
$$
y''(0)=f_u(1,1)u''(0)+f_v(1,1)v''(0)
=3(-1)+4\cdot2=5.
$$

### 第 13 题

**答案：** $-\dfrac{1}{\pi}$

余弦系数为
$$
a_n=\frac{2}{\pi}\int_0^\pi (x+1)\cos nx\,dx
=\frac{2}{n^2\pi}\left((-1)^n-1\right).
$$
当 $n$ 为奇数时，
$$
a_n=-\frac{4}{n^2\pi}.
$$
故
$$
a_{2n-1}=-\frac{4}{(2n-1)^2\pi}.
$$
由于 $a_{2n-1}\to0$，$\sin a_{2n-1}\sim a_{2n-1}$，于是
$$
\lim_{n\to\infty}n^2\sin a_{2n-1}
=\lim_{n\to\infty}n^2\left[-\frac{4}{(2n-1)^2\pi}\right]
=-\frac{1}{\pi}.
$$

### 第 14 题

**答案：** $\arctan(x+y)=y+\dfrac{\pi}{4}$

将 $x$ 看作 $y$ 的函数，则
$$
\frac{dx}{dy}=(x+y)^2.
$$
令 $u=x+y$，则
$$
\frac{du}{dy}=\frac{dx}{dy}+1=u^2+1.
$$
于是
$$
\int\frac{du}{1+u^2}=\int dy,
\qquad
\arctan u=y+C.
$$
由 $y(1)=0$ 得 $u=1$，故 $C=\pi/4$。因此
$$
\arctan(x+y)=y+\frac{\pi}{4}.
$$

### 第 15 题

**答案：** $a\ge0$

矩阵 $A$ 为实对称矩阵。题中不等式要对任意 $\alpha,\beta$ 成立，等价于双线性型
$$
(\alpha,\beta)_A=\alpha^TA\beta
$$
满足 Cauchy-Schwarz 不等式，因此 $A$ 应为半正定矩阵。

对二阶实对称矩阵
$$
A=\begin{pmatrix}a+1&a\\a&a\end{pmatrix},
$$
半正定条件为
$$
a+1\ge0,\qquad \det A=(a+1)a-a^2=a\ge0.
$$
后一条件已推出前一条件，故
$$
a\ge0.
$$

### 第 16 题

**答案：** $p=\dfrac{2}{3}$

设事件 $A$ 为“三次全部成功”，事件 $B$ 为“至少成功一次”。则
$$
P(A|B)=\frac{P(A)}{P(B)}
=\frac{p^3}{1-(1-p)^3}=\frac{4}{13}.
$$
整理得
$$
13p^3=4-4(1-p)^3,
$$
即
$$
p(3p-2)(3p+6)=0.
$$
因 $0<p<1$，故
$$
p=\frac{2}{3}.
$$

### 第 17 题

**答案：** $\ln(\sqrt{2}+1)+\sqrt{2}-2$。

对固定的 $y$，直接对 $x$ 积分：
$$
\int_{\sqrt{1-y^2}}^1\frac{x}{\sqrt{x^2+y^2}}\,dx
=\left.\sqrt{x^2+y^2}\right|_{\sqrt{1-y^2}}^1
=\sqrt{1+y^2}-1.
$$
因此
$$
I=\int_{-1}^1(\sqrt{1+y^2}-1)\,dy
=2\int_0^1(\sqrt{1+y^2}-1)\,dy.
$$
又
$$
\int\sqrt{1+y^2}\,dy
=\frac{1}{2}\left(y\sqrt{1+y^2}+\ln(y+\sqrt{1+y^2})\right),
$$
故
$$
I=\left[y\sqrt{1+y^2}+\ln(y+\sqrt{1+y^2})\right]_0^1-2
=\sqrt{2}+\ln(\sqrt{2}+1)-2.
$$
所以答案为
$$
\ln(\sqrt{2}+1)+\sqrt{2}-2.
$$

### 第 18 题

**答案：** (I) 切平面为
$$
x+y+z=3.
$$

(II) 最大值为 $21$，在 $(3,0)$ 与 $(0,3)$ 处取得；最小值为 $\dfrac{17}{27}$，在 $\left(\dfrac{4}{3},\dfrac{4}{3}\right)$ 处取得。

令
$$
F(x,y,z)=x^3+y^3-(x+y)^2+3-z.
$$
则
$$
F_x=3x^2-2(x+y),\quad F_y=3y^2-2(x+y),\quad F_z=-1.
$$
在点 $(1,1,1)$ 处，
$$
F_x=F_y=F_z=-1.
$$
故切平面法向量可取 $(1,1,1)$，切平面为
$$
x+y+z=3.
$$

它与坐标平面围成的区域在 $xOy$ 平面上的投影为
$$
D=\{(x,y)\mid x\ge0,\ y\ge0,\ x+y\le3\}.
$$
在 $D$ 内部，驻点满足
$$
3x^2-2(x+y)=0,\qquad 3y^2-2(x+y)=0,
$$
解得唯一内部驻点
$$
\left(\frac{4}{3},\frac{4}{3}\right).
$$
边界上分别考察 $x=0$、$y=0$、$x+y=3$，候选点包括
$$
(0,0),\ (3,0),\ (0,3),\ \left(\frac{2}{3},0\right),\ \left(0,\frac{2}{3}\right),\ \left(\frac{3}{2},\frac{3}{2}\right).
$$
代入比较可得
$$
f(3,0)=f(0,3)=21,\qquad
f\left(\frac{4}{3},\frac{4}{3}\right)=\frac{17}{27},
$$
且其余候选值介于二者之间。因此最大值为 $21$，最小值为 $17/27$。

### 第 19 题

**答案：** 证明见解析。

由 Taylor 公式，存在 $\xi_1\in(0,x)$、$\xi_2\in(x,1)$，使
$$
f(x)=f(0)+f'(0)x+\frac{f''(\xi_1)}2x^2,
$$
$$
f(x)=f(1)+f'(1)(x-1)+\frac{f''(\xi_2)}2(x-1)^2.
$$
用 $(1-x)$ 乘第一式、用 $x$ 乘第二式后相加，并利用 $f'(0)=f'(1)$，可得
$$
f(x)-f(0)(1-x)-f(1)x
=\frac{f''(\xi_1)}2x^2(1-x)
+\frac{f''(\xi_2)}2x(x-1)^2.
$$
由 $|f''|\le1$，
$$
\left|f(x)-f(0)(1-x)-f(1)x\right|
\le\frac{1}{2}x^2(1-x)+\frac{1}{2}x(1-x)^2
=\frac{x(1-x)}2.
$$
这证明了 (I)。

对 (I) 在 $[0,1]$ 上积分，得
$$
\left|\int_0^1\left[f(x)-f(0)(1-x)-f(1)x\right]dx\right|
\le\int_0^1\frac{x(1-x)}2\,dx=\frac{1}{12}.
$$
又
$$
\int_0^1[f(0)(1-x)+f(1)x]\,dx=\frac{f(0)+f(1)}2,
$$
故 (II) 成立。

### 第 20 题

**答案：** $\displaystyle \frac{4\sqrt{5}}{25}\pi$。

在平面 $2x-z-1=0$ 上有 $z=2x-1$，$dz=2\,dx$。曲线在 $xOy$ 平面上的投影满足
$$
x^2+y^2+(2x-1)^2=2x,
$$
即
$$
5x^2-6x+y^2+1=0.
$$
化为标准形：
$$
\frac{(x-\frac{3}{5})^2}{(\frac{2}{5})^2}+\frac{y^2}{(\frac{2}{\sqrt{5}})^2}=1.
$$

将 $z=2x-1$ 代入原积分，并按题设方向转化为投影曲线的正向积分，得
$$
\int_{L_1}(12x^2-4x-1)y\,dx+(4x^3-2x^2)\,dy.
$$
由 Green 公式，
$$
\iint_D\left[(12x^2-4x)-(12x^2-4x-1)\right]\,dA
=\iint_D1\,dA=S_D.
$$
投影区域 $D$ 是半轴长分别为 $2/5$ 与 $2/\sqrt{5}$ 的椭圆，故
$$
S_D=\pi\cdot\frac{2}{5}\cdot\frac{2}{\sqrt{5}}
=\frac{4\sqrt{5}}{25}\pi.
$$

### 第 21 题

**答案：** 矩阵
$$
A=\begin{pmatrix}
-2&0&2\\
0&-2&-2\\
-6&-3&3
\end{pmatrix}.
$$
当 $n\ge1$ 时，
$$
A^n=
\begin{pmatrix}
(-1)^{n+1}2^n-4&(-1)^{n+1}2^n-2&2\\
(-1)^n2^{n+1}+4&(-1)^n2^{n+1}+2&-2\\
-6&-3&3
\end{pmatrix},
$$
并且
$$
\begin{pmatrix}x_n\\y_n\\z_n\end{pmatrix}
=\begin{pmatrix}
(-2)^n+8\\
(-2)^{n+1}-8\\
12
\end{pmatrix}.
$$

由递推式直接读出
$$
A=\begin{pmatrix}
-2&0&2\\
0&-2&-2\\
-6&-3&3
\end{pmatrix}.
$$
其特征多项式为
$$
\det(\lambda E-A)=\lambda(\lambda-1)(\lambda+2),
$$
故特征值为 $0,1,-2$。对应可取特征向量
$$
\xi_1=(1,-1,1)^T,\quad
\xi_2=(-2,2,-3)^T,\quad
\xi_3=(1,-2,0)^T.
$$
令
$$
P=(\xi_1,\xi_2,\xi_3)=
\begin{pmatrix}
1&-2&1\\
-1&2&-2\\
1&-3&0
\end{pmatrix},
\qquad
\Lambda=\operatorname{diag}(0,1,-2).
$$
则
$$
A=P\Lambda P^{-1},\qquad A^n=P\Lambda^nP^{-1}.
$$
计算得，当 $n\ge1$ 时，
$$
A^n=
\begin{pmatrix}
(-1)^{n+1}2^n-4&(-1)^{n+1}2^n-2&2\\
(-1)^n2^{n+1}+4&(-1)^n2^{n+1}+2&-2\\
-6&-3&3
\end{pmatrix}.
$$
又
$$
\alpha_n=A^n\alpha_0,\qquad \alpha_0=(-1,0,2)^T,
$$
所以
$$
\alpha_n=
\begin{pmatrix}
(-2)^n+8\\
(-2)^{n+1}-8\\
12
\end{pmatrix}.
$$

### 第 22 题

**答案：** (I)
$$
c=\frac{n+1}{n}.
$$

(II) 当
$$
c=\frac{n+2}{n+1}
$$
时，$h(c)$ 取得最小值。

样本最大值的分布函数为
$$
F_{X_{(n)}}(x)=
\begin{cases}
0,&x<0,\\
\left(\dfrac{x}{\theta}\right)^n,&0\le x<\theta,\\
1,&x\ge\theta.
\end{cases}
$$
故密度为
$$
f_{X_{(n)}}(x)=\frac{n}{\theta^n}x^{n-1},\qquad 0<x<\theta.
$$
于是
$$
E[X_{(n)}]=\int_0^\theta x\frac{n}{\theta^n}x^{n-1}\,dx
=\frac{n}{n+1}\theta.
$$
若 $T_c=cX_{(n)}$ 无偏，则
$$
c\frac{n}{n+1}\theta=\theta,
$$
所以
$$
c=\frac{n+1}{n}.
$$

再算
$$
E[X_{(n)}^2]=\int_0^\theta x^2\frac{n}{\theta^n}x^{n-1}\,dx
=\frac{n}{n+2}\theta^2.
$$
因此
$$
h(c)=E(cX_{(n)}-\theta)^2
=c^2E[X_{(n)}^2]-2c\theta E[X_{(n)}]+\theta^2
$$
$$
=\left(\frac{n}{n+2}c^2-\frac{2n}{n+1}c+1\right)\theta^2.
$$
这是关于 $c$ 的二次函数，令导数为 $0$，得
$$
\frac{2n}{n+2}c-\frac{2n}{n+1}=0,
$$
所以
$$
c=\frac{n+2}{n+1}.
$$
