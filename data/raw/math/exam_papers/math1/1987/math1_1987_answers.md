# 1987 数学一答案解析

资料类型：考研数学一答案解析
年份：1987
科目：数学一
解析来源：原答案解析目录未含 1987 年文件；本文件依据题面独立推导补写。
整理状态：已补齐答案与解析

## 答案速查

| 题号 | 题型 | 答案 |
|---|---|---|
| 1 | 填空题 | $x-y+z=0$ |
| 2 | 填空题 | $x=\dfrac{1}{e}$ |
| 3 | 填空题 | $\dfrac{3}{2}$ |
| 4 | 填空题 | $-18\pi$ |
| 5 | 填空题 | $(1,1,-1)$ |
| 6 | 解答题 | $a=4,\ b=1$ |
| 7 | 解答题 | $\bigl[f_1(x,xy)+y f_2(x,xy)\bigr](1+y)g'(x+xy)$ |
| 8 | 解答题 | $B=\begin{pmatrix}5&-2&-2\\4&-3&-2\\-2&2&3\end{pmatrix}$ |
| 9 | 解答题 | $y=C_0+e^{-3x}(C_1\cos ax+C_2\sin ax)+\dfrac{x}{a^2+9}$ |
| 10 | 选择题 | C |
| 11 | 选择题 | D |
| 12 | 选择题 | B |
| 13 | 选择题 | C |
| 14 | 解答题 | 收敛域为 $[-2,2)$；和函数 $S(x)=-\dfrac{1}{x}\ln\left(1-\dfrac{x}{2}\right)$（$x\ne0$），且 $S(0)=\dfrac{1}{2}$ |
| 15 | 解答题 | $34\pi$ |
| 16 | 解答题 | 见解析 |
| 17 | 解答题 | $a\ne1$ 时有唯一解；$a=1,b\ne-1$ 时无解；$a=1,b=-1$ 时有无穷多解，通解为 $(-1+s+t,\ 1-2s-2t,\ s,\ t)$ |
| 18 | 填空题 | $1-(1-p)^n$；$(1-p)^n+np(1-p)^{n-1}$ |
| 19 | 填空题 | $\dfrac{53}{120}$；$\dfrac{20}{53}$ |
| 20 | 填空题 | $E(X)=1$；$D(X)=\dfrac{1}{2}$ |
| 21 | 解答题 | $f_Z(z)=\begin{cases}0,&z\le0,\\\dfrac{1}{2}(1-e^{-z}),&0<z\le2,\\\dfrac{1}{2}(e^2-1)e^{-z},&z>2.\end{cases}$ |

## 详细解析

### 第 1 题

- 答案：$x-y+z=0$

第一条直线的方向向量为

$$
\boldsymbol v_1=(0,1,1),
$$

第二条直线的方向向量为

$$
\boldsymbol v_2=(1,2,1).
$$

所求平面与两直线都平行，因此平面内含有这两个方向。其法向量可取

$$
\boldsymbol n=\boldsymbol v_1\times \boldsymbol v_2=(-1,1,-1).
$$

又平面过原点，所以

$$
-x+y-z=0,
$$

即

$$
x-y+z=0.
$$

### 第 2 题

- 答案：$x=\dfrac{1}{e}$

当 $x>0$ 时，

$$
y=x^{2x},\qquad \ln y=2x\ln x.
$$

两边求导得

$$
\frac{y'}{y}=2(\ln x+1).
$$

令 $y'=0$，得

$$
\ln x+1=0,\qquad x=e^{-1}.
$$

当 $x<e^{-1}$ 时 $y'<0$，当 $x>e^{-1}$ 时 $y'>0$，故函数在

$$
x=\frac{1}{e}
$$

处取得极小值。

### 第 3 题

- 答案：$\dfrac{3}{2}$

曲线 $y=\ln x$ 与 $y=0$ 交于 $x=1$；直线 $y=e+1-x$ 与 $y=0$ 交于 $x=e+1$；曲线与直线交于 $x=e$，此时 $y=1$。

因此所围面积为

$$
S=\int_1^e \ln x\,dx+\int_e^{e+1}(e+1-x)\,dx.
$$

计算得

$$
\int_1^e \ln x\,dx=\bigl(x\ln x-x\bigr)\big|_1^e=1,
$$

且

$$
\int_e^{e+1}(e+1-x)\,dx=\frac{1}{2}.
$$

故

$$
S=\frac{3}{2}.
$$

### 第 4 题

- 答案：$-18\pi$

记

$$
P=2xy-2y,\qquad Q=x^2-4x.
$$

由格林公式，

$$
\oint_L P\,dx+Q\,dy
=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dxdy,
$$

其中 $D:x^2+y^2\le 9$。又

$$
\frac{\partial Q}{\partial x}=2x-4,\qquad
\frac{\partial P}{\partial y}=2x-2,
$$

故

$$
\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}=-2.
$$

于是

$$
\oint_L P\,dx+Q\,dy=-2\cdot \pi\cdot 3^2=-18\pi.
$$

### 第 5 题

- 答案：$(1,1,-1)$

设 $u=c_1\alpha_1+c_2\alpha_2+c_3\alpha_3$。由

$$
c_1(1,1,0)+c_2(1,0,1)+c_3(0,1,1)=(2,0,0)
$$

得方程组

$$
\begin{cases}
c_1+c_2=2,\\
c_1+c_3=0,\\
c_2+c_3=0.
\end{cases}
$$

解得

$$
c_1=1,\qquad c_2=1,\qquad c_3=-1.
$$

故坐标为

$$
(1,1,-1).
$$

### 第 6 题

- 答案：$a=4,\ b=1$

当 $x\to0$ 时，

$$
\int_0^x\frac{t^2}{\sqrt{a+t^2}}\,dt
\sim \int_0^x\frac{t^2}{\sqrt{a}}\,dt
=\frac{x^3}{3\sqrt{a}}.
$$

又

$$
bx-\sin x=(b-1)x+\frac{x^3}{6}+o(x^3).
$$

要使极限为有限非零值，必须先有

$$
b=1.
$$

此时分母等价于 $x^3/6$，故

$$
\lim_{x\to0}\frac{\dfrac{x^3}{3\sqrt{a}}}{\dfrac{x^3}{6}}
=\frac{2}{\sqrt{a}}=1.
$$

因此

$$
\sqrt{a}=2,\qquad a=4.
$$

### 第 7 题

- 答案：$\bigl[f_1(x,xy)+y f_2(x,xy)\bigr](1+y)g'(x+xy)$

设 $f_1,f_2$ 分别表示 $f$ 对第一、第二个变量的偏导数。由复合函数求导法则，

$$
\frac{\partial u}{\partial x}
=f_1(x,xy)+y f_2(x,xy).
$$

又

$$
v=g(x+xy)=g\bigl(x(1+y)\bigr),
$$

故

$$
\frac{\partial v}{\partial x}=(1+y)g'(x+xy).
$$

于是

$$
\frac{\partial u}{\partial x}\cdot\frac{\partial v}{\partial x}
=\bigl[f_1(x,xy)+y f_2(x,xy)\bigr](1+y)g'(x+xy).
$$

### 第 8 题

- 答案：$B=\begin{pmatrix}5&-2&-2\\4&-3&-2\\-2&2&3\end{pmatrix}$

由

$$
AB=A+2B
$$

得

$$
(A-2E)B=A.
$$

由于

$$
A-2E=
\begin{pmatrix}
1&0&1\\
1&-1&0\\
0&1&2
\end{pmatrix},
$$

且 $|A-2E|\ne0$，故

$$
B=(A-2E)^{-1}A.
$$

计算得

$$
B=
\begin{pmatrix}
5&-2&-2\\
4&-3&-2\\
-2&2&3
\end{pmatrix}.
$$

### 第 9 题

- 答案：$y=C_0+e^{-3x}(C_1\cos ax+C_2\sin ax)+\dfrac{x}{a^2+9}$

令 $u=y'$，原方程化为

$$
u''+6u'+(9+a^2)u=1.
$$

对应齐次方程的特征方程为

$$
\lambda^2+6\lambda+9+a^2=0,
$$

即

$$
(\lambda+3)^2+a^2=0.
$$

故

$$
u_h=e^{-3x}(A\cos ax+B\sin ax).
$$

取常数特解

$$
u_p=\frac{1}{9+a^2}.
$$

于是

$$
y'=e^{-3x}(A\cos ax+B\sin ax)+\frac{1}{9+a^2}.
$$

积分后仍可把指数三角项的常数重新记为 $C_1,C_2$，得通解

$$
y=C_0+e^{-3x}(C_1\cos ax+C_2\sin ax)+\frac{x}{a^2+9}.
$$

### 第 10 题

- 答案：C

原级数可写为

$$
\sum_{n=1}^{\infty}(-1)^n\left(\frac{1}{n}+\frac{k}{n^2}\right).
$$

其中 $\sum (-1)^n/n$ 收敛但不绝对收敛，$\sum (-1)^n k/n^2$ 绝对收敛，所以原级数收敛。

但

$$
\sum_{n=1}^{\infty}\left|\frac{k+n}{n^2}\right|
\sim \sum_{n=1}^{\infty}\frac{1}{n}
$$

发散，因此原级数为条件收敛。选 C。

### 第 11 题

- 答案：D

令 $u=tx$，则 $du=t\,dx$。于是

$$
I=t\int_0^{s/t}f(tx)\,dx
=t\int_0^s f(u)\frac{du}{t}
=\int_0^s f(u)\,du.
$$

因此 $I$ 只依赖于 $s$，不依赖于 $t$。选 D。

### 第 12 题

- 答案：B

由题设

$$
\frac{f(x)-f(a)}{(x-a)^2}\to -1
$$

可知，当 $x$ 充分接近 $a$ 且 $x\ne a$ 时，

$$
f(x)-f(a)<0.
$$

因此 $f(a)$ 是局部最大值。并且

$$
\frac{f(x)-f(a)}{x-a}
=\frac{f(x)-f(a)}{(x-a)^2}(x-a)\to0,
$$

所以 $f'(a)=0$。选 B。

### 第 13 题

- 答案：C

当 $|A|=a\ne0$ 时，

$$
A^*=|A|A^{-1}.
$$

两边取行列式得

$$
|A^*|=||A|A^{-1}|=|A|^n|A^{-1}|
=a^n\cdot \frac{1}{a}=a^{n-1}.
$$

选 C。

### 第 14 题

- 答案：收敛域为 $[-2,2)$；和函数 $S(x)=-\dfrac{1}{x}\ln\left(1-\dfrac{x}{2}\right)$（$x\ne0$），且 $S(0)=\dfrac{1}{2}$

原级数为

$$
S(x)=\sum_{n=1}^{\infty}\frac{x^{n-1}}{n2^n}.
$$

令 $u=x/2$，则

$$
S(x)=\frac{1}{x}\sum_{n=1}^{\infty}\frac{x^n}{n2^n}
=\frac{1}{x}\sum_{n=1}^{\infty}\frac{u^n}{n}.
$$

当 $|u|<1$，即 $|x|<2$ 时，

$$
\sum_{n=1}^{\infty}\frac{u^n}{n}=-\ln(1-u),
$$

故

$$
S(x)=-\frac{1}{x}\ln\left(1-\frac{x}{2}\right)\quad (x\ne0).
$$

当 $x=0$ 时，原级数只剩首项的极限形式，或由上式取极限，得

$$
S(0)=\frac{1}{2}.
$$

端点处，$x=2$ 时级数为 $\sum 1/(2n)$ 发散；$x=-2$ 时为 $\sum (-1)^{n-1}/(2n)$ 收敛。故收敛域为

$$
[-2,2).
$$

### 第 15 题

- 答案：$34\pi$

旋转曲面满足

$$
y=1+x^2+z^2,\qquad x^2+z^2\le2.
$$

按题意，法向量与 $y$ 轴正向夹角大于 $\pi/2$，故取参数化

$$
\boldsymbol r(x,z)=(x,1+x^2+z^2,z),
$$

并取有向面积向量

$$
\boldsymbol r_z\times\boldsymbol r_x=(2x,-1,2z).
$$

记

$$
P=x(8y+1),\quad Q=2(1-y^2),\quad R=-4yz.
$$

则

$$
I=\iint_D\bigl(2xP-Q+2zR\bigr)\,dxdz,
$$

其中 $D:x^2+z^2\le2$，$y=1+x^2+z^2$。令 $x=r\cos\theta,z=r\sin\theta$，则角向积分后被积函数化为

$$
\int_0^{2\pi}\bigl(2xP-Q+2zR\bigr)\,d\theta
=\pi(18r^2+12r^4).
$$

因此

$$
I=\pi\int_0^{\sqrt{2}}(18r^3+12r^5)\,dr
=\pi\left(\frac{9}{2}r^4+2r^6\right)\Big|_0^{\sqrt{2}}
=34\pi.
$$

### 第 16 题

- 答案：见解析

令

$$
g(x)=f(x)-x.
$$

由于 $f(x)$ 在 $[0,1]$ 上取值恒在 $(0,1)$ 内，所以

$$
g(0)=f(0)>0,\qquad g(1)=f(1)-1<0.
$$

由连续函数介值定理，存在 $\xi\in(0,1)$，使

$$
g(\xi)=0,
$$

即

$$
f(\xi)=\xi.
$$

再证唯一性。若存在 $0<x_1<x_2<1$，使

$$
f(x_1)=x_1,\qquad f(x_2)=x_2,
$$

则

$$
g(x_1)=g(x_2)=0.
$$

由罗尔定理，存在 $\eta\in(x_1,x_2)$，使

$$
g'(\eta)=0.
$$

但

$$
g'(x)=f'(x)-1,
$$

于是 $g'(\eta)=0$ 意味着 $f'(\eta)=1$，与题设 $f'(x)\ne1$ 矛盾。因此这样的点唯一。

### 第 17 题

- 答案：$a\ne1$ 时有唯一解；$a=1,b\ne-1$ 时无解；$a=1,b=-1$ 时有无穷多解，通解为 $(-1+s+t,\ 1-2s-2t,\ s,\ t)$

对增广矩阵作初等行变换。先用第 4 行减去第 1 行的 3 倍，系数矩阵的行列式等于

$$
\begin{vmatrix}
1&2&2\\
-1&a-3&-2\\
-1&-2&a-3
\end{vmatrix}
=(a-1)^2.
$$

因此当 $a\ne1$ 时，系数矩阵可逆，方程组有唯一解。

当 $a=1$ 时，后 3 个方程的系数部分满足

$$
\begin{pmatrix}
1&2&2\\
-1&-2&-2\\
-1&-2&-2
\end{pmatrix}.
$$

此时第二个方程给出

$$
x_2+2x_3+2x_4=1.
$$

第三个方程左端为其相反数，故相容要求

$$
b=-1.
$$

第四个方程也给出相同条件。于是：

$$
a=1,\ b\ne-1
$$

时无解；

$$
a=1,\ b=-1
$$

时有无穷多解。令 $x_3=s,\ x_4=t$，由

$$
x_2+2x_3+2x_4=1
$$

得

$$
x_2=1-2s-2t.
$$

再由

$$
x_1+x_2+x_3+x_4=0
$$

得

$$
x_1=-1+s+t.
$$

故通解为

$$
(x_1,x_2,x_3,x_4)=(-1+s+t,\ 1-2s-2t,\ s,\ t),
\quad s,t\in\mathbb R.
$$

### 第 18 题

- 答案：$1-(1-p)^n$；$(1-p)^n+np(1-p)^{n-1}$

$n$ 次独立试验中，事件 $A$ 一次也不发生的概率为 $(1-p)^n$。因此至少发生一次的概率为

$$
1-(1-p)^n.
$$

至多发生一次包括发生 $0$ 次和发生 $1$ 次两种情形，所以概率为

$$
(1-p)^n+\binom n1p(1-p)^{n-1}
=(1-p)^n+np(1-p)^{n-1}.
$$

### 第 19 题

- 答案：$\dfrac{53}{120}$；$\dfrac{20}{53}$

设 $W$ 表示取出白球。由全概率公式，

$$
P(W)=\frac{1}{3}\left(\frac{1}{5}+\frac{3}{6}+\frac{5}{8}\right)
=\frac{1}{3}\left(\frac{1}{5}+\frac{1}{2}+\frac{5}{8}\right)
=\frac{53}{120}.
$$

由贝叶斯公式，已知取出白球时它来自第二个箱子的概率为

$$
P(B_2\mid W)
=\frac{P(B_2)P(W\mid B_2)}{P(W)}
=\frac{\frac{1}{3}\cdot\frac{1}{2}}{\frac{53}{120}}
=\frac{20}{53}.
$$

### 第 20 题

- 答案：$E(X)=1$；$D(X)=\dfrac{1}{2}$

密度函数可写为

$$
f(x)=\frac{1}{\sqrt\pi}e^{-(x-1)^2}.
$$

与正态分布密度

$$
\frac{1}{\sqrt{2\pi}\sigma}\exp\left[-\frac{(x-\mu)^2}{2\sigma^2}\right]
$$

比较，得

$$
\mu=1,\qquad 2\sigma^2=1.
$$

故

$$
E(X)=1,\qquad D(X)=\sigma^2=\frac{1}{2}.
$$

### 第 21 题

- 答案：$f_Z(z)=\begin{cases}0,&z\le0,\\\dfrac{1}{2}(1-e^{-z}),&0<z\le2,\\\dfrac{1}{2}(e^2-1)e^{-z},&z>2.\end{cases}$

令

$$
W=2X.
$$

由于 $X\sim U(0,1)$，故

$$
f_W(w)=
\begin{cases}
\dfrac{1}{2},&0\le w\le2,\\
0,&\text{其他}.
\end{cases}
$$

又 $Z=W+Y$，且 $W,Y$ 独立，所以由卷积公式

$$
f_Z(z)=\int_{-\infty}^{\infty} f_W(w)f_Y(z-w)\,dw.
$$

只有当 $0\le w\le2$ 且 $z-w>0$ 时 integrand 非零。因此：

当 $z\le0$ 时，

$$
f_Z(z)=0.
$$

当 $0<z\le2$ 时，

$$
f_Z(z)=\int_0^z \frac{1}{2} e^{-(z-w)}\,dw
=\frac{1}{2}(1-e^{-z}).
$$

当 $z>2$ 时，

$$
f_Z(z)=\int_0^2 \frac{1}{2} e^{-(z-w)}\,dw
=\frac{1}{2}(e^2-1)e^{-z}.
$$

综上，

$$
f_Z(z)=
\begin{cases}
0,&z\le0,\\
\dfrac{1}{2}(1-e^{-z}),&0<z\le2,\\
\dfrac{1}{2}(e^2-1)e^{-z},&z>2.
\end{cases}
$$
