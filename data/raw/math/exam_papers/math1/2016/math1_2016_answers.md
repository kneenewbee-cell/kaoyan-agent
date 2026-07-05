# 2016 数学一答案解析

资料类型：考研数学一答案解析
年份：2016
科目：数学一
整理状态：已根据答案页图像、题图与题干推导清洗

## 答案速查

### 选择题

| 题号 | 答案 |
|---|---|
| 1 | C |
| 2 | D |
| 3 | A |
| 4 | D |
| 5 | C |
| 6 | B |
| 7 | B |
| 8 | A |

### 填空题

| 题号 | 答案 |
|---|---|
| 9 | $\dfrac{1}{2}$ |
| 10 | $\mathbf j+(y-1)\mathbf k$ |
| 11 | $-dx+2dy$ |
| 12 | $\dfrac{1}{2}$ |
| 13 | $\lambda^4+\lambda^3+2\lambda^2+3\lambda+4$ |
| 14 | $(8.2,10.8)$ |

### 解答题

| 题号 | 答案要点 |
|---|---|
| 15 | $5\pi+\dfrac{32}{3}$ |
| 16 | (I) 证明见解析。  (II) $$ \int_0^{+\infty}y(x)\,dx=\frac{3}{k}. $$ |
| 17 | $$ I(t)=e^{2-t}+t, $$ 且 $I(t)$ 的最小值为 $3$。 |
| 18 | $I=\dfrac{1}{2}$。 |
| 19 | 证明见解析。 |
| 20 | 当 $a=-2$ 时，$AX=B$ 无解；  当 $a=1$ 时，$AX=B$ 有无穷多解，通解可写为 $$ X= \begin{pmatrix} 1&1\\ -1&-1\\ 0&0 \end{pmatrix} + \begin{pmatrix} 0&0\\ -c_1&-c_2\\ c_1&c_2 \end{pmatrix}, \qquad c_1,c_2\in\mathbb R; $$  当 $a\ne-2$ 且 $a\ne1$ 时，$AX=B$ 有唯一解 $$ X= \begin{pmatrix} 1&\dfrac{3a}{a+2}\\ 0&\dfrac{a-4}{a+2}\\ -1&0 \end{pmatrix}. $$ |
| 21 | (I) $$ A^{99}= \begin{pmatrix} 2^{99}-2&1-2^{99}&2-2^{98}\\ 2^{100}-2&1-2^{100}&2-2^{99}\\ 0&0&0 \end{pmatrix}. $$  (II) $$ \beta_1=(2^{99}-2)\alpha_1+(2^{100}-2)\alpha_2, $$ $$ \beta_2=(1-2^{99})\alpha_1+(1-2^{100})\alpha_2, $$ $$ \beta_3=(2-2^{98})\alpha_1+(2-2^{99})\alpha_2. $$ |
| 22 | (I) $$ f_{X,Y}(x,y)= \begin{cases} 3,&0<x<1,\ x^2<y<\sqrt{x},\\ 0,&\text{其他}. \end{cases} $$  (II) $U$ 与 $X$ 不相互独立。  (III) $$ F_Z(z)= \begin{cases} 0,&z<0,\\ \dfrac{3}{2}z^2-z^3,&0\le z<1,\\ 2(z-1)^{3/2}-\dfrac{3}{2}z^2+3z-1,&1\le z<2,\\ 1,&z\ge2. \end{cases} $$ |
| 23 | (I) $$ f_T(t)= \begin{cases} \dfrac{9t^8}{\theta^9},&0<t<\theta,\\ 0,&\text{其他}. \end{cases} $$  (II) $$ a=\frac{10}{9}. $$ |

## 详细解析

### 第 1 题

**答案：** C

当 $x\to0^+$ 时，
$$
\frac{1}{x^a(1+x)^b}\sim x^{-a},
$$
故在 $0$ 附近收敛要求 $a<1$。

当 $x\to+\infty$ 时，
$$
\frac{1}{x^a(1+x)^b}\sim x^{-(a+b)},
$$
故在无穷远处收敛要求 $a+b>1$。因此选 C。

### 第 2 题

**答案：** D

在 $x<1$ 时，原函数可取 $(x-1)^2+C_1$；在 $x\ge1$ 时，原函数可取
$$
x\ln x-x+C_2.
$$
原函数在 $x=1$ 处必须连续。取左侧常数为 $0$，左极限为 $0$；右侧在 $x=1$ 的值为 $-1+C_2$，故 $C_2=1$。因此
$$
F(x)=
\begin{cases}
(x-1)^2,&x<1,\\
x(\ln x-1)+1,&x\ge1,
\end{cases}
$$
选 D。

### 第 3 题

**答案：** A

两解之差
$$
y_2-y_1=2\sqrt{1+x^2}
$$
是齐次方程 $y'+p(x)y=0$ 的解，所以
$$
\frac{x}{\sqrt{1+x^2}}+p(x)\sqrt{1+x^2}=0,
\qquad
p(x)=-\frac{x}{1+x^2}.
$$
将
$$
y=(1+x^2)^2+\sqrt{1+x^2}
$$
代入原方程，得
$$
q(x)=y'+p(x)y=3x(1+x^2).
$$
故选 A。

### 第 4 题

**答案：** D

当 $x\to0^-$ 时，$f(x)=x\to0$；当 $x\to0^+$ 时，$x\in(1/(n+1),1/n]$ 且 $n\to\infty$，所以 $f(x)=1/n\to0$。又 $f(0)=0$，故 $f$ 在 $0$ 处连续。

左导数为
$$
\lim_{x\to0^-}\frac{f(x)-f(0)}{x}=1.
$$
右侧若 $1/(n+1)<x\le1/n$，则
$$
1\le\frac{f(x)}{x}=\frac{1/n}{x}<\frac{n+1}{n}\to1.
$$
由夹逼定理右导数也为 $1$。因此 $f$ 在 $0$ 处可导，选 D。

### 第 5 题

**答案：** C

若 $B=P^{-1}AP$，则
$$
B^T=P^TA^T(P^T)^{-1},
$$
所以 A 正确；又
$$
B^{-1}=P^{-1}A^{-1}P,
$$
所以 B 正确；并且
$$
B+B^{-1}=P^{-1}(A+A^{-1})P,
$$
所以 D 正确。

但 $B^T$ 与 $A^T$ 的相似变换矩阵一般不是 $P$，所以不能推出
$$
B+B^T\sim A+A^T.
$$
故错误的是 C。

### 第 6 题

**答案：** B

二次型对应矩阵为
$$
A=\begin{pmatrix}
1&2&2\\
2&1&2\\
2&2&1
\end{pmatrix}.
$$
该矩阵的特征值为 $5,-1,-1$，故经正交变换可化为
$$
5y_1^2-y_2^2-y_3^2=2.
$$
即
$$
\frac{y_1^2}{2/5}-\frac{y_2^2}{2}-\frac{y_3^2}{2}=1,
$$
这是双叶双曲面，选 B。

### 第 7 题

**答案：** B

标准化得
$$
p=P\left\{\frac{X-\mu}{\sigma}\le \frac{\mu+\sigma^2-\mu}{\sigma}\right\}
=P\{Z\le\sigma\}=\Phi(\sigma),
$$
其中 $Z\sim N(0,1)$。因此 $p$ 与 $\mu$ 无关，并随 $\sigma$ 增大而增大，选 B。

### 第 8 题

**答案：** A

$(X,Y)$ 是二项试验次数为 $2$、单次概率 $p_1=p_2=1/3$ 的多项分布中的两个计数。故
$$
D(X)=D(Y)=2\cdot\frac{1}{3}\cdot\frac{2}{3}=\frac{4}{9},
$$
$$
\operatorname{Cov}(X,Y)=-2\cdot\frac{1}{3}\cdot\frac{1}{3}=-\frac{2}{9}.
$$
因此相关系数为
$$
\rho_{XY}=\frac{-2/9}{\sqrt{(4/9)(4/9)}}=-\frac{1}{2}.
$$
选 A。

### 第 9 题

**答案：** $\dfrac{1}{2}$

当 $t\to0$ 时，
$$
\ln(1+t\sin t)\sim t\sin t\sim t^2,
$$
所以
$$
t\ln(1+t\sin t)\sim t^3,
\qquad
\int_0^x t\ln(1+t\sin t)\,dt\sim\frac{x^4}{4}.
$$
又
$$
1-\cos x^2\sim\frac{x^4}{2}.
$$
故极限为
$$
\frac{x^4/4}{x^4/2}=\frac{1}{2}.
$$

### 第 10 题

**答案：** $\mathbf j+(y-1)\mathbf k$

设
$$
P=x+y+z,\qquad Q=xy,\qquad R=z.
$$
则
$$
\operatorname{rot}\mathbf A
=\left(R_y-Q_z,\ P_z-R_x,\ Q_x-P_y\right)
=(0,\ 1,\ y-1).
$$
因此
$$
\operatorname{rot}\mathbf A=\mathbf j+(y-1)\mathbf k.
$$

### 第 11 题

**答案：** $-dx+2dy$

在 $(x,y)=(0,1)$ 处，方程给出
$$
z-1=0,\qquad z=1.
$$
令
$$
F(x,y,z)=(x+1)z-y^2-x^2f(x-z,y).
$$
在 $(0,1,1)$ 处，
$$
F_x=1,\qquad F_y=-2,\qquad F_z=1.
$$
由 $dF=0$，
$$
F_xdx+F_ydy+F_zdz=0,
$$
故
$$
dz=-dx+2dy.
$$

### 第 12 题

**答案：** $\dfrac{1}{2}$

在 $x=0$ 附近，
$$
\arctan x=x-\frac{x^3}{3}+O(x^5),
$$
$$
\frac{x}{1+ax^2}=x-ax^3+O(x^5).
$$
因此
$$
f(x)=\left(a-\frac{1}{3}\right)x^3+O(x^5).
$$
故
$$
f'''(0)=6\left(a-\frac{1}{3}\right)=1,
$$
解得
$$
a=\frac{1}{2}.
$$

### 第 13 题

**答案：** $\lambda^4+\lambda^3+2\lambda^2+3\lambda+4$

按第一行展开并继续计算，得
$$
\begin{aligned}
D&=(\lambda-1)
\begin{vmatrix}
\lambda&-1&0\\
0&\lambda&-1\\
3&2&\lambda+1
\end{vmatrix}\\
&=(\lambda-1)\left[\lambda^2(\lambda+1)+2\lambda+3\right]+4\\
&=\lambda^4+\lambda^3+2\lambda^2+3\lambda+4.
\end{aligned}
$$

### 第 14 题

**答案：** $(8.2,10.8)$

正态总体均值的双侧置信区间以样本均值 $\overline X$ 为中心。已知中心为 $9.5$，上限为 $10.8$，故半长为
$$
10.8-9.5=1.3.
$$
因此下限为
$$
9.5-1.3=8.2.
$$
所求置信区间为
$$
(8.2,10.8).
$$

### 第 15 题

**答案：** $5\pi+\dfrac{32}{3}$

在极坐标下，$x=r\cos\theta$，$dxdy=r\,drd\theta$。因此
$$
\iint_Dx\,dxdy
=\int_{-\pi/2}^{\pi/2}\int_2^{2(1+\cos\theta)}
r^2\cos\theta\,drd\theta.
$$
即
$$
\frac{8}{3}\int_{-\pi/2}^{\pi/2}\cos\theta\left[(1+\cos\theta)^3-1\right]d\theta.
$$
展开后为
$$
\frac{8}{3}\int_{-\pi/2}^{\pi/2}\left(3\cos^2\theta+3\cos^3\theta+\cos^4\theta\right)d\theta.
$$
利用
$$
\int_{-\pi/2}^{\pi/2}\cos^2\theta\,d\theta=\frac{\pi}{2},\quad
\int_{-\pi/2}^{\pi/2}\cos^3\theta\,d\theta=\frac{4}{3},\quad
\int_{-\pi/2}^{\pi/2}\cos^4\theta\,d\theta=\frac{3\pi}{8},
$$
得
$$
\iint_Dx\,dxdy=5\pi+\frac{32}{3}.
$$

### 第 16 题

**答案：** (I) 证明见解析。

(II)
$$
\int_0^{+\infty}y(x)\,dx=\frac{3}{k}.
$$

特征方程为
$$
r^2+2r+k=0,
$$
其根为
$$
r_1=-1+\sqrt{1-k},\qquad r_2=-1-\sqrt{1-k}.
$$
由于 $0<k<1$，有 $r_1<0,r_2<0$。因此
$$
y(x)=C_1e^{r_1x}+C_2e^{r_2x},
$$
两个指数项在 $[0,+\infty)$ 上均可积，故反常积分收敛。

对微分方程在 $[0,+\infty)$ 上积分：
$$
\int_0^{+\infty}y''\,dx+2\int_0^{+\infty}y'\,dx
+k\int_0^{+\infty}y\,dx=0.
$$
由 $r_1,r_2<0$ 可知 $y(x)\to0,\ y'(x)\to0$。代入 $y(0)=1,\ y'(0)=1$，得
$$
(0-1)+2(0-1)+k\int_0^{+\infty}y(x)\,dx=0.
$$
故
$$
\int_0^{+\infty}y(x)\,dx=\frac{3}{k}.
$$

### 第 17 题

**答案：**
$$
I(t)=e^{2-t}+t,
$$
且 $I(t)$ 的最小值为 $3$。

因为被积表达式是全微分 $df$，所以曲线积分与路径无关，
$$
I(t)=f(1,t)-f(0,0).
$$
由
$$
f_x=(2x+1)e^{2x-y}
$$
对 $x$ 积分，得
$$
f(x,y)=xe^{2x-y}+C(y).
$$
又 $f(0,y)=y+1$，故 $C(y)=y+1$，于是
$$
f(x,y)=xe^{2x-y}+y+1.
$$
因此
$$
I(t)=f(1,t)-f(0,0)=e^{2-t}+t.
$$
令
$$
I'(t)=-e^{2-t}+1=0,
$$
得 $t=2$。且 $I''(t)=e^{2-t}>0$，故最小值为
$$
I(2)=3.
$$

### 第 18 题

**答案：** $I=\dfrac{1}{2}$。

由 Gauss 公式，令
$$
P=x^2+1,\qquad Q=-2y,\qquad R=3z.
$$
则
$$
P_x+Q_y+R_z=2x-2+3=2x+1.
$$
区域 $\Omega$ 是由坐标平面和截距为 $1,2,1$ 的平面围成的四面体，体积
$$
V=\frac{1\cdot2\cdot1}{6}=\frac{1}{3}.
$$
四面体质心的 $x$ 坐标为 $1/4$，所以
$$
\iiint_\Omega x\,dV=\frac{1}{4}\cdot\frac{1}{3}=\frac{1}{12}.
$$
因此
$$
I=\iiint_\Omega(2x+1)\,dV
=2\cdot\frac{1}{12}+\frac{1}{3}
=\frac{1}{2}.
$$

### 第 19 题

**答案：** 证明见解析。

由中值定理，
$$
|x_{n+1}-x_n|
=|f(x_n)-f(x_{n-1})|
=|f'(\xi_n)||x_n-x_{n-1}|
<\frac{1}{2}|x_n-x_{n-1}|.
$$
递推得
$$
|x_{n+1}-x_n|<\left(\frac{1}{2}\right)^{n-1}|x_2-x_1|.
$$
故
$$
\sum_{n=1}^{\infty}|x_{n+1}-x_n|
$$
由几何级数比较判别法收敛，即 (I) 成立。

由 (I) 可知 $\{x_n\}$ 为 Cauchy 数列，所以极限存在，记为 $L$。令 $n\to\infty$，由 $x_{n+1}=f(x_n)$ 得
$$
L=f(L).
$$
设 $F(x)=f(x)-x$，则
$$
F'(x)=f'(x)-1<-\frac{1}{2},
$$
故 $F$ 严格递减。又
$$
F(0)=1>0,
$$
并且由 $0<f'(x)<1/2$ 得
$$
f(2)<f(0)+1=2,
$$
所以 $F(2)=f(2)-2<0$。因此方程 $F(x)=0$ 的根位于 $(0,2)$，即
$$
0<L<2.
$$

### 第 20 题

**答案：** 当 $a=-2$ 时，$AX=B$ 无解；

当 $a=1$ 时，$AX=B$ 有无穷多解，通解可写为
$$
X=
\begin{pmatrix}
1&1\\
-1&-1\\
0&0
\end{pmatrix}
+
\begin{pmatrix}
0&0\\
-c_1&-c_2\\
c_1&c_2
\end{pmatrix},
\qquad c_1,c_2\in\mathbb R;
$$

当 $a\ne-2$ 且 $a\ne1$ 时，$AX=B$ 有唯一解
$$
X=
\begin{pmatrix}
1&\dfrac{3a}{a+2}\\
0&\dfrac{a-4}{a+2}\\
-1&0
\end{pmatrix}.
$$

计算行列式可得
$$
\det A=(a-1)(a+2).
$$
因此当 $a\ne1,-2$ 时，$A$ 可逆，方程有唯一解，直接计算
$$
X=A^{-1}B=
\begin{pmatrix}
1&\dfrac{3a}{a+2}\\
0&\dfrac{a-4}{a+2}\\
-1&0
\end{pmatrix}.
$$

当 $a=-2$ 时，对增广矩阵作初等行变换可知
$$
r(A)<r(A,B),
$$
故方程无解。

当 $a=1$ 时，
$$
r(A)=r(A,B)<3,
$$
故方程有无穷多解。分别解两列右端方程，通解可写为
$$
X=
\begin{pmatrix}
1&1\\
-1&-1\\
0&0
\end{pmatrix}
+
\begin{pmatrix}
0&0\\
-c_1&-c_2\\
c_1&c_2
\end{pmatrix},
\qquad c_1,c_2\in\mathbb R.
$$

### 第 21 题

**答案：** (I)
$$
A^{99}=
\begin{pmatrix}
2^{99}-2&1-2^{99}&2-2^{98}\\
2^{100}-2&1-2^{100}&2-2^{99}\\
0&0&0
\end{pmatrix}.
$$

(II)
$$
\beta_1=(2^{99}-2)\alpha_1+(2^{100}-2)\alpha_2,
$$
$$
\beta_2=(1-2^{99})\alpha_1+(1-2^{100})\alpha_2,
$$
$$
\beta_3=(2-2^{98})\alpha_1+(2-2^{99})\alpha_2.
$$

由计算可得
$$
A^n=
\begin{pmatrix}
2^n-2&1-2^n&2-2^{n-1}\\
2^{n+1}-2&1-2^{n+1}&2-2^n\\
0&0&0
\end{pmatrix}\qquad(n\ge1).
$$
取 $n=99$ 即得
$$
A^{99}=
\begin{pmatrix}
2^{99}-2&1-2^{99}&2-2^{98}\\
2^{100}-2&1-2^{100}&2-2^{99}\\
0&0&0
\end{pmatrix}.
$$

由 $B^2=BA$，反复相乘得
$$
B^{100}=BA^{99}.
$$
若 $B=(\alpha_1,\alpha_2,\alpha_3)$，则 $BA^{99}$ 的各列就是 $A^{99}$ 对应列系数下 $\alpha_1,\alpha_2,\alpha_3$ 的线性组合。由于 $A^{99}$ 第三行均为 $0$，得到
$$
\beta_1=(2^{99}-2)\alpha_1+(2^{100}-2)\alpha_2,
$$
$$
\beta_2=(1-2^{99})\alpha_1+(1-2^{100})\alpha_2,
$$
$$
\beta_3=(2-2^{98})\alpha_1+(2-2^{99})\alpha_2.
$$

### 第 22 题

**答案：** (I)
$$
f_{X,Y}(x,y)=
\begin{cases}
3,&0<x<1,\ x^2<y<\sqrt{x},\\
0,&\text{其他}.
\end{cases}
$$

(II) $U$ 与 $X$ 不相互独立。

(III)
$$
F_Z(z)=
\begin{cases}
0,&z<0,\\
\dfrac{3}{2}z^2-z^3,&0\le z<1,\\
2(z-1)^{3/2}-\dfrac{3}{2}z^2+3z-1,&1\le z<2,\\
1,&z\ge2.
\end{cases}
$$

区域面积为
$$
|D|=\int_0^1(\sqrt{x}-x^2)\,dx=\frac{2}{3}-\frac{1}{3}=\frac{1}{3}.
$$
故均匀分布密度为
$$
f_{X,Y}(x,y)=3,\qquad 0<x<1,\ x^2<y<\sqrt{x}.
$$

给定 $X=x$ 时，$Y$ 在 $(x^2,\sqrt{x})$ 上均匀。由于 $x^2<x<\sqrt{x}$，
$$
P(U=1\mid X=x)=P(Y\ge x\mid X=x)
=\frac{\sqrt{x}-x}{\sqrt{x}-x^2},
$$
该值依赖于 $x$，所以 $U$ 与 $X$ 不独立。

当 $0\le z<1$ 时，$Z\le z$ 只能来自 $U=0$ 且 $X\le z$，即
$$
F_Z(z)=3\int_0^z\int_{x^2}^{x}dy\,dx
=3\int_0^z(x-x^2)\,dx
=\frac{3}{2}z^2-z^3.
$$
当 $1\le z<2$ 时，
$$
F_Z(z)=P(U=0)+P(U=1,\ X\le z-1).
$$
其中
$$
P(U=0)=3\int_0^1(x-x^2)\,dx=\frac{1}{2},
$$
且
$$
P(U=1,\ X\le z-1)
=3\int_0^{z-1}(\sqrt{x}-x)\,dx.
$$
化简得
$$
F_Z(z)=2(z-1)^{3/2}-\frac{3}{2}z^2+3z-1.
$$
再结合端点情形，得到题中分段表达式。

### 第 23 题

**答案：** (I)
$$
f_T(t)=
\begin{cases}
\dfrac{9t^8}{\theta^9},&0<t<\theta,\\
0,&\text{其他}.
\end{cases}
$$

(II)
$$
a=\frac{10}{9}.
$$

总体分布函数为
$$
F(x)=\left(\frac{x}{\theta}\right)^3,\qquad 0<x<\theta.
$$
因此样本最大值 $T$ 的分布函数为
$$
F_T(t)=P(T\le t)=\left[F(t)\right]^3
=\left(\frac{t}{\theta}\right)^9,\qquad 0<t<\theta.
$$
求导得
$$
f_T(t)=\frac{9t^8}{\theta^9},\qquad 0<t<\theta.
$$
于是
$$
E(T)=\int_0^\theta t\frac{9t^8}{\theta^9}\,dt
=\frac{9}{10}\theta.
$$
要使 $aT$ 为 $\theta$ 的无偏估计，需要
$$
aE(T)=\theta,
$$
故
$$
a=\frac{10}{9}.
$$
