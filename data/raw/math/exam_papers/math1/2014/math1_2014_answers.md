# Math 1 2014 Answers

资料类型：考研数学一答案解析
年份：2014
科目：数学一
整理状态：已按题干截图与答案页图像核对并清洗整理

## 答案速查

| 题号 | 题型 | 答案 |
|---|---|---|
| 1 | 选择题 | C |
| 2 | 选择题 | D |
| 3 | 选择题 | D |
| 4 | 选择题 | A |
| 5 | 选择题 | B |
| 6 | 选择题 | A |
| 7 | 选择题 | B |
| 8 | 选择题 | D |
| 9 | 填空题 | $2x-y-z-1=0$ |
| 10 | 填空题 | $1$ |
| 11 | 填空题 | $xe^{2x+1}$ |
| 12 | 填空题 | $\pi$ |
| 13 | 填空题 | $[-2,2]$ |
| 14 | 填空题 | $\displaystyle \frac{2}{5n}$ |
| 15 | 解答题 | $\displaystyle \frac{1}{2}$ |
| 16 | 解答题 | 极小值 $f(1)=-2$，无极大值。 |
| 17 | 解答题 | $\displaystyle f(u)=\frac{1}{16}e^{2u}-\frac{1}{16}e^{-2u}-\frac{u}{4}$ |
| 18 | 解答题 | $\displaystyle I=-4\pi$ |
| 19 | 解答题 | 结论成立：$\displaystyle \lim_{n\to\infty}a_n=0$，且 $\displaystyle \sum_{n=1}^{\infty}\frac{a_n}{b_n}$ 收敛。 |
| 20 | 解答题 | （1）基础解系可取 $\displaystyle (-1,2,3,1)^T$；（2）$\displaystyle B=\begin{pmatrix}2-k_1&6-k_2&-1-k_3\\-1+2k_1&-3+2k_2&1+2k_3\\-1+3k_1&-4+3k_2&1+3k_3\\k_1&k_2&k_3\end{pmatrix}$，其中 $k_1,k_2,k_3\in\mathbb R$。 |
| 21 | 解答题 | 两矩阵均相似于 $\operatorname{diag}(n,0,\ldots,0)$，故二者相似。 |
| 22 | 解答题 | （1）$F_Y(y)=0\ (y<0),\ \frac{3y}{4}\ (0\le y<1),\ \frac{1}{2}+\frac{y}{4}\ (1\le y<2),\ 1\ (y\ge2)$；（2）$E(Y)=\frac{3}{4}$。 |
| 23 | 解答题 | （1）$\displaystyle E(X)=\frac{\sqrt{\pi\theta}}{2},\ E(X^2)=\theta$；（2）$\displaystyle \hat\theta_n=\frac{1}{n}\sum_{i=1}^nX_i^2$；（3）存在，$a=\theta$。 |

## 详细解析

### 第 1 题
**答案：** C

$y=x+\sin x$ 与直线 $y=x$ 的差为 $\sin x$，当 $x\to\infty$ 时不趋于 $0$，故没有斜渐近线；$y=x^2+\sin x$ 与 $y=x^2+\sin\frac{1}{x}$ 都不是线性函数的渐近情形。

对 $y=x+\sin\frac{1}{x}$，有
$$
\lim_{x\to\infty}\left(y-x\right)=\lim_{x\to\infty}\sin\frac{1}{x}=0,
$$
因而 $y=x$ 是它的斜渐近线，选 C。

### 第 2 题
**答案：** D

当 $f''(x)\ge0$ 时，$f$ 在 $[0,1]$ 上为凸函数。对任意 $x\in[0,1]$，由凸函数图像位于两端点弦线下方，得
$$
f(x)=f((1-x)\cdot0+x\cdot1)\le(1-x)f(0)+xf(1)=g(x).
$$
因此正确选项为 D。

### 第 3 题
**答案：** D

积分区域为
$$
D=\{(x,y):0\le y\le1,\ -\sqrt{1-y^2}\le x\le1-y\}.
$$
在第一象限部分，边界为直线 $x+y=1$，极坐标下为
$$
0\le\theta\le\frac{\pi}{2},\qquad 0\le r\le\frac{1}{\cos\theta+\sin\theta}.
$$
在第二象限部分，区域由单位圆给出，故
$$
\frac{\pi}{2}\le\theta\le\pi,
\qquad 0\le r\le1.
$$
换元时面积元为 $dx\,dy=r\,dr\,d\theta$，所以应选 D。

### 第 4 题
**答案：** A

记
$$
J(a,b)=\int_{-\pi}^{\pi}(x-a\cos x-b\sin x)^2\,dx.
$$
利用奇偶性，$\int_{-\pi}^{\pi}x\cos x\,dx=0$，$\int_{-\pi}^{\pi}\sin x\cos x\,dx=0$，并且
$$
\int_{-\pi}^{\pi}x\sin x\,dx=2\pi,
\qquad
\int_{-\pi}^{\pi}\sin^2x\,dx=\int_{-\pi}^{\pi}\cos^2x\,dx=\pi.
$$
因此
$$
J(a,b)=\int_{-\pi}^{\pi}x^2\,dx+\pi a^2+\pi b^2-4\pi b.
$$
只需最小化 $a^2+b^2-4b=a^2+(b-2)^2-4$，故 $a_1=0,b_1=2$，答案为 $2\sin x$，选 A。

### 第 5 题
**答案：** B

按第一行展开：
$$
\begin{aligned}
D
&=-a\begin{vmatrix}a&0&b\\0&d&0\\c&0&d\end{vmatrix}
+b\begin{vmatrix}a&0&b\\0&c&0\\c&0&d\end{vmatrix} \\
&=-ad(ad-bc)+bc(ad-bc) \\
&=-(ad-bc)^2.
\end{aligned}
$$
因此选 B。

### 第 6 题
**答案：** A

若 $\alpha_1,\alpha_2,\alpha_3$ 线性无关，且
$$
c_1(\alpha_1+k\alpha_3)+c_2(\alpha_2+l\alpha_3)=0,
$$
则
$$
c_1\alpha_1+c_2\alpha_2+(kc_1+lc_2)\alpha_3=0,
$$
从而 $c_1=c_2=0$。所以三向量线性无关一定推出题中两个向量线性无关。

反过来不成立。例如取 $\alpha_1=(1,0,0)^T,\alpha_2=(0,1,0)^T,\alpha_3=0$，则对任意 $k,l$，$\alpha_1+k\alpha_3, \alpha_2+l\alpha_3$ 仍线性无关，但 $\alpha_1,\alpha_2,\alpha_3$ 线性相关。故题中条件是必要非充分条件，选 A。

### 第 7 题
**答案：** B

由 $A$ 与 $B$ 相互独立，
$$
P(A-B)=P(A\cap B^c)=P(A)P(B^c)=P(A)(1-0.5)=0.3,
$$
所以 $P(A)=0.6$。于是
$$
P(B-A)=P(B\cap A^c)=P(B)P(A^c)=0.5\times0.4=0.2.
$$
因此选 B。

### 第 8 题
**答案：** D

由混合密度可得
$$
E(Y_1)=\frac{1}{2}E(X_1)+\frac{1}{2}E(X_2)=E(Y_2).
$$
记 $\mu_i=E(X_i),\sigma_i^2=D(X_i)$。则
$$
D(Y_1)=\frac{1}{2}(\sigma_1^2+\mu_1^2)+\frac{1}{2}(\sigma_2^2+\mu_2^2)-\left(\frac{\mu_1+\mu_2}{2}\right)^2,
$$
而独立性给出
$$
D(Y_2)=\frac{1}{4}(\sigma_1^2+\sigma_2^2).
$$
两式相减得
$$
D(Y_1)-D(Y_2)=\frac{1}{4}\left[\sigma_1^2+\sigma_2^2+(\mu_1-\mu_2)^2\right]>0.
$$
因而选 D。

### 第 9 题
**答案：** $2x-y-z-1=0$

设
$$
z=x^2(1-\sin y)+y^2(1-\sin x).
$$
则
$$
z_x=2x(1-\sin y)-y^2\cos x,
\qquad
z_y=-x^2\cos y+2y(1-\sin x).
$$
在 $(1,0)$ 处，$z_x=2,z_y=-1$。切平面方程为
$$
z-1=2(x-1)-y,
$$
即
$$
2x-y-z-1=0.
$$

### 第 10 题
**答案：** $1$

在 $[0,2]$ 上积分得
$$
f(x)=\int 2(x-1)\,dx=x^2-2x+C.
$$
因 $f$ 为奇函数，$f(0)=0$，故 $C=0$。又 $f$ 的周期为 4，
$$
f(7)=f(7-8)=f(-1)=-f(1).
$$
而 $f(1)=1-2=-1$，所以 $f(7)=1$。

### 第 11 题
**答案：** $xe^{2x+1}$

令 $u=\frac{y}{x}$，即 $y=ux$，则 $y'=u+xu'$。代入原方程得
$$
x(u+xu')+ux\bigl(\ln x-\ln(ux)\bigr)=0,
$$
化简为
$$
xu'=u(\ln u-1).
$$
分离变量：
$$
\frac{du}{u(\ln u-1)}=\frac{dx}{x}.
$$
积分得
$$
\ln|\ln u-1|=\ln x+C,
$$
因而 $\ln u-1=Cx$。由 $y(1)=e^3$ 得 $u(1)=e^3$，所以 $C=2$。于是
$$
\ln\frac{y}{x}=1+2x,
\qquad
y=xe^{2x+1}.
$$

### 第 12 题
**答案：** $\pi$

由平面 $y+z=0$ 得 $z=-y$。按题设方向取参数
$$
x=\cos t,\qquad y=\sin t,\qquad z=-\sin t,
\qquad 0\le t\le2\pi.
$$
此时从 $z$ 轴正向看去，投影沿单位圆逆时针运行。于是
$$
dx=-\sin t\,dt,
\qquad
dz=-\cos t\,dt.
$$
因此
$$
\oint_L z\,dx+y\,dz
=\int_0^{2\pi}\left(\sin^2t-\sin t\cos t\right)dt
=\pi.
$$

### 第 13 题
**答案：** $[-2,2]$

配方得
$$
\begin{aligned}
f&=x_1^2-x_2^2+2ax_1x_3+4x_2x_3 \\
&=(x_1+ax_3)^2-(x_2-2x_3)^2+(4-a^2)x_3^2.
\end{aligned}
$$
若 $4-a^2\ge0$，规范形中负平方项只有一个；若 $4-a^2<0$，则会有两个负平方项。故负惯性指数为 1 当且仅当
$$
4-a^2\ge0,
$$
即 $a\in[-2,2]$。

### 第 14 题
**答案：** $\displaystyle \frac{2}{5n}$

先计算
$$
E(X^2)=\int_\theta^{2\theta}x^2\frac{2x}{3\theta^2}\,dx
=\frac{2}{3\theta^2}\cdot\frac{x^4}{4}\bigg|_\theta^{2\theta}
=\frac{5}{2}\theta^2.
$$
因此
$$
E\left(c\sum_{i=1}^nX_i^2\right)
=cnE(X^2)=cn\cdot\frac{5}{2}\theta^2.
$$
它为 $\theta^2$ 的无偏估计，故
$$
cn\cdot\frac{5}{2}=1,
\qquad
c=\frac{2}{5n}.
$$

### 第 15 题
**答案：** $\displaystyle \frac{1}{2}$

令
$$
A(x)=\int_1^x\left[t^2\left(e^{\frac{1}{t}}-1\right)-t\right]dt,
\qquad
B(x)=x^2\ln\left(1+\frac{1}{x}\right).
$$
当 $x\to+\infty$ 时，$A(x),B(x)\to+\infty$，可用洛必达法则。由微积分基本定理，
$$
A'(x)=x^2\left(e^{\frac{1}{x}}-1\right)-x.
$$
又
$$
B'(x)=2x\ln\left(1+\frac{1}{x}\right)-\frac{x}{x+1}.
$$
利用展开式 $e^{1/x}=1+\frac{1}{x}+\frac{1}{2x^2}+o(x^{-2})$ 与 $\ln(1+\frac{1}{x})=\frac{1}{x}-\frac{1}{2x^2}+o(x^{-2})$，得
$$
A'(x)\to\frac{1}{2},
\qquad
B'(x)\to1.
$$
因此原极限为
$$
\frac{1}{2}.
$$

### 第 16 题
**答案：** 极小值 $f(1)=-2$，无极大值。

设
$$
F(x,y)=y^3+xy^2+x^2y+6.
$$
由 $F(x,f(x))=0$ 得
$$
y'=-\frac{F_x}{F_y}
=-\frac{y^2+2xy}{3y^2+2xy+x^2}.
$$
极值点需满足 $y'=0$，即 $y(y+2x)=0$。其中 $y=0$ 不满足原方程，故 $y=-2x$。代入原方程得
$$
-8x^3+4x^3-2x^3+6=0,
$$
所以 $x=1,y=-2$。

在该点，$F_y=9\ne0$，且
$$
y''=-\frac{F_{xx}}{F_y}\bigg|_{(1,-2)}=-\frac{2y}{3y^2+2xy+x^2}\bigg|_{(1,-2)}=\frac{4}{9}>0.
$$
因此 $x=1$ 为极小值点，极小值为 $f(1)=-2$，无极大值。

### 第 17 题
**答案：** $\displaystyle f(u)=\frac{1}{16}e^{2u}-\frac{1}{16}e^{-2u}-\frac{u}{4}$

令 $u=e^x\cos y$，则 $z=f(u)$。有
$$
z_{xx}=f''(u)u^2+f'(u)u,
$$
且
$$
z_{yy}=f''(u)e^{2x}\sin^2y-f'(u)u.
$$
相加得
$$
z_{xx}+z_{yy}=e^{2x}f''(u).
$$
题设方程化为
$$
e^{2x}f''(u)=\left(4f(u)+u\right)e^{2x},
$$
即
$$
f''(u)-4f(u)=u.
$$
其通解为
$$
f(u)=C_1e^{2u}+C_2e^{-2u}-\frac{u}{4}.
$$
由 $f(0)=0$ 得 $C_1+C_2=0$；由 $f'(0)=0$ 得 $2C_1-2C_2-\frac{1}{4}=0$。解得
$$
C_1=\frac{1}{16},\qquad C_2=-\frac{1}{16}.
$$
因此
$$
f(u)=\frac{1}{16}e^{2u}-\frac{1}{16}e^{-2u}-\frac{u}{4}.
$$

### 第 18 题
**答案：** $\displaystyle I=-4\pi$

设
$$
\boldsymbol F=((x-1)^3,(y-1)^3,z-1).
$$
令 $\Omega=\{(x,y,z):x^2+y^2\le z\le1\}$，用平面圆盘 $\Sigma_0:z=1, x^2+y^2\le1$ 封闭曲面。$\Omega$ 的外法向在抛物面部分为下侧，而题目要求上侧，故抛物面外向通量为 $-I$。圆盘上 $z-1=0$，所以圆盘通量为 $0$。

由高斯公式，
$$
-I=\iiint_\Omega \operatorname{div}\boldsymbol F\,dV.
$$
又
$$
\operatorname{div}\boldsymbol F=3(x-1)^2+3(y-1)^2+1.
$$
在柱坐标中，奇函数项积分为 $0$，于是
$$
\begin{aligned}
\iiint_\Omega \operatorname{div}\boldsymbol F\,dV
&=\int_0^{2\pi}\int_0^1(3r^2+7)(1-r^2)r\,dr\,d\theta \\
&=4\pi.
\end{aligned}
$$
因此
$$
I=-4\pi.
$$

### 第 19 题
**答案：** 结论成立：$\displaystyle \lim_{n\to\infty}a_n=0$，且 $\displaystyle \sum_{n=1}^{\infty}\frac{a_n}{b_n}$ 收敛。

（1）因 $\sum_{n=1}^{\infty}b_n$ 收敛且 $b_n>0$，故 $b_n\to0$。于是 $\cos b_n\to1$。由
$$
\cos a_n-a_n=\cos b_n
$$
得 $\cos a_n-a_n\to1$。函数 $h(x)=\cos x-x$ 在 $[0,\frac{\pi}{2})$ 上严格递减，且 $h(0)=1$，所以
$$
a_n\to0.
$$

（2）由等式变形得
$$
a_n=\cos a_n-\cos b_n=(1-\cos b_n)-(1-\cos a_n).
$$
又 $0<a_n<b_n$ 可由 $a_n<1-\cos b_n<\frac{b_n^2}{2}$ 推出，故 $\frac{a_n}{b_n}\to0$。于是
$$
\lim_{n\to\infty}\frac{a_n}{b_n^2}
=\lim_{n\to\infty}\left[\frac{1-\cos b_n}{b_n^2}-\frac{1-\cos a_n}{a_n^2}\left(\frac{a_n}{b_n}\right)^2\right]
=\frac{1}{2}.
$$
因而
$$
\frac{a_n/b_n}{b_n}=\frac{a_n}{b_n^2}\to\frac{1}{2}.
$$
由正项级数比较判别法，既然 $\sum b_n$ 收敛，级数 $\sum \frac{a_n}{b_n}$ 也收敛。

### 第 20 题
**答案：** （1）基础解系可取 $\displaystyle (-1,2,3,1)^T$；（2）$\displaystyle B=\begin{pmatrix}2-k_1&6-k_2&-1-k_3\\-1+2k_1&-3+2k_2&1+2k_3\\-1+3k_1&-4+3k_2&1+3k_3\\k_1&k_2&k_3\end{pmatrix}$，其中 $k_1,k_2,k_3\in\mathbb R$。

（1）对 $A$ 作初等行变换可得
$$
A\sim
\begin{pmatrix}
1&0&0&1\\
0&1&0&-2\\
0&0&1&-3
\end{pmatrix}.
$$
因此齐次方程 $Ax=0$ 的通解为
$$
x=t(-1,2,3,1)^T,
$$
一个基础解系可取
$$
\alpha=(-1,2,3,1)^T.
$$

（2）设 $B=(\beta_1,\beta_2,\beta_3)$，则 $AB=E$ 等价于
$$
A\beta_1=e_1,
\qquad
A\beta_2=e_2,
\qquad
A\beta_3=e_3.
$$
三个方程的通解分别可写为
$$
\beta_1=\begin{pmatrix}2\\-1\\-1\\0\end{pmatrix}+k_1\alpha,
\quad
\beta_2=\begin{pmatrix}6\\-3\\-4\\0\end{pmatrix}+k_2\alpha,
\quad
\beta_3=\begin{pmatrix}-1\\1\\1\\0\end{pmatrix}+k_3\alpha.
$$
所以
$$
B=\begin{pmatrix}
2-k_1&6-k_2&-1-k_3\\
-1+2k_1&-3+2k_2&1+2k_3\\
-1+3k_1&-4+3k_2&1+3k_3\\
k_1&k_2&k_3
\end{pmatrix},
\qquad k_1,k_2,k_3\in\mathbb R.
$$

### 第 21 题
**答案：** 两矩阵均相似于 $\operatorname{diag}(n,0,\ldots,0)$，故二者相似。

记左边全 1 矩阵为 $A$，右边矩阵为 $B$。显然 $r(A)=r(B)=1$，且
$$
\operatorname{tr}A=\operatorname{tr}B=n.
$$
对全 1 矩阵，有 $A^2=nA$。对矩阵 $B$，它只有最后一列非零，且最后一列为 $(1,2,\ldots,n)^T$，故同样有
$$
B^2=nB.
$$
因而二者的最小多项式都整除 $\lambda(\lambda-n)$，且均有特征值 $n$ 与 $0$。由于该多项式无重根，$A,B$ 都可对角化。

又 $r(A)=r(B)=1$，所以特征值 $0$ 的几何重数均为 $n-1$，从而
$$
A\sim\operatorname{diag}(n,0,\ldots,0),
\qquad
B\sim\operatorname{diag}(n,0,\ldots,0).
$$
因此 $A$ 与 $B$ 相似。

### 第 22 题
**答案：** （1）$F_Y(y)=0\ (y<0),\ \frac{3y}{4}\ (0\le y<1),\ \frac{1}{2}+\frac{y}{4}\ (1\le y<2),\ 1\ (y\ge2)$；（2）$E(Y)=\frac{3}{4}$。

（1）由全概率公式，
$$
F_Y(y)=\frac{1}{2}P\{Y\le y\mid X=1\}+\frac{1}{2}P\{Y\le y\mid X=2\}.
$$
当 $y<0$ 时，$F_Y(y)=0$；当 $0\le y<1$ 时，
$$
F_Y(y)=\frac{1}{2}y+\frac{1}{2}\cdot\frac{y}{2}=\frac{3y}{4};
$$
当 $1\le y<2$ 时，
$$
F_Y(y)=\frac{1}{2}+\frac{1}{2}\cdot\frac{y}{2}=\frac{1}{2}+\frac{y}{4};
$$
当 $y\ge2$ 时，$F_Y(y)=1$。故
$$
F_Y(y)=
\begin{cases}
0,&y<0,\\
\frac{3y}{4},&0\le y<1,\\
\frac{1}{2}+\frac{y}{4},&1\le y<2,\\
1,&y\ge2.
\end{cases}
$$

（2）由条件期望公式，
$$
E(Y)=E\{E(Y\mid X)\}=\frac{1}{2}E(X)=\frac{1}{2}\cdot\frac{1+2}{2}=\frac{3}{4}.
$$

### 第 23 题
**答案：** （1）$\displaystyle E(X)=\frac{\sqrt{\pi\theta}}{2},\ E(X^2)=\theta$；（2）$\displaystyle \hat\theta_n=\frac{1}{n}\sum_{i=1}^nX_i^2$；（3）存在，$a=\theta$。

（1）由分布函数求导，密度为
$$
f(x;\theta)=\frac{2x}{\theta}e^{-\frac{x^2}{\theta}},\qquad x\ge0.
$$
令 $u=\frac{x^2}{\theta}$，则
$$
E(X)=\int_0^\infty x\frac{2x}{\theta}e^{-\frac{x^2}{\theta}}\,dx
=\sqrt{\theta}\int_0^\infty u^{\frac{1}{2}}e^{-u}\,du
=\frac{\sqrt{\pi\theta}}{2},
$$
且
$$
E(X^2)=\int_0^\infty x^2\frac{2x}{\theta}e^{-\frac{x^2}{\theta}}\,dx
=\theta\int_0^\infty ue^{-u}\,du
=\theta.
$$

（2）设样本观测值 $x_1,x_2,\ldots,x_n$ 均非负，似然函数为
$$
L(\theta)=\prod_{i=1}^n\frac{2x_i}{\theta}e^{-\frac{x_i^2}{\theta}}.
$$
去掉与 $\theta$ 无关的因子，
$$
\ln L(\theta)=C-n\ln\theta-\frac{1}{\theta}\sum_{i=1}^nx_i^2.
$$
求导并令其为零：
$$
-\frac{n}{\theta}+\frac{1}{\theta^2}\sum_{i=1}^nx_i^2=0,
$$
得
$$
\hat\theta_n=\frac{1}{n}\sum_{i=1}^nX_i^2.
$$

（3）因为 $E(X^2)=\theta<\infty$，由辛钦大数定律，
$$
\hat\theta_n=\frac{1}{n}\sum_{i=1}^nX_i^2\xrightarrow{P}\theta.
$$
因此存在这样的实数 $a$，取 $a=\theta$ 即可。
