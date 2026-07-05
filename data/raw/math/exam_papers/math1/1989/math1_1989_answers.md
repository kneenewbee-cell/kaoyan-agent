# Math 1 1989 Answers

资料类型：考研数学一答案解析
年份：1989
科目：数学一
范围：试卷 I
来源：D:\百度网盘\高数资料\【02】1987-2022年数学一真题详解答案（PDF）\1989考研数一真题解析.pdf
校对状态：已按题干和答案页图像重新清洗，去除 OCR 碎行、串题内容和非本题知识点页脚

## 答案速查

| 题号 | 题型 | 答案 |
|---|---|---|
| 1 | 填空题 | $-1$ |
| 2 | 填空题 | $f(x)=x-1$ |
| 3 | 填空题 | $\pi$ |
| 4 | 填空题 | $2$ |
| 5 | 填空题 | $\begin{pmatrix}1&0&0\\-\dfrac{1}{2}&\dfrac{1}{2}&0\\0&0&1\end{pmatrix}$ |
| 6 | 选择题 | A |
| 7 | 选择题 | C |
| 8 | 选择题 | D |
| 9 | 选择题 | B |
| 10 | 选择题 | C |
| 11 | 解答题 | $-2f''(2x-y)+g_v(x,xy)+xg_{uv}(x,xy)+xyg_{vv}(x,xy)$ |
| 12 | 解答题 | $\dfrac{1}{2}$ |
| 13 | 解答题 | $\dfrac{\pi}{8}$ |
| 14 | 解答题 | $\displaystyle \frac{\pi}{4}+\sum_{n=0}^{\infty}(-1)^n\frac{x^{2n+1}}{2n+1}$，其中 $-1\le x<1$ |
| 15 | 解答题 | $f(x)=\dfrac{1}{2}\sin x+\dfrac{x}{2}\cos x$ |
| 16 | 解答题 | 证明见解析 |
| 17 | 解答题 | 当 $\lambda=1$ 时有解；通解为 $x_1=1-t,\ x_2=2t-1,\ x_3=t$，其中 $t$ 为任意常数 |
| 18 | 解答题 | 证明见解析 |
| 19 | 解答题 | $R=\dfrac{4a}{3}$ |
| 20 | 填空题 | $0.7$ |
| 21 | 填空题 | $0.75$ |
| 22 | 填空题 | $0.8$ |
| 23 | 解答题 | $f_Z(z)=\dfrac{1}{3\sqrt{2\pi}}\exp\!\left[-\dfrac{(z-5)^2}{18}\right]$ |

## 详细解析

### 第 1 题

- 答案：$-1$

由导数定义，

$$
f'(3)=\lim_{t\to 0}\frac{f(3+t)-f(3)}{t}.
$$

令 $t=-h$，则当 $h\to 0$ 时 $t\to 0$，并且

$$
\lim_{h\to 0}\frac{f(3-h)-f(3)}{2h}
=-\frac{1}{2}\lim_{t\to 0}\frac{f(3+t)-f(3)}{t}
=-\frac{1}{2} f'(3).
$$

已知 $f'(3)=2$，所以所求极限为

$$
-\frac{1}{2}\cdot 2=-1.
$$

### 第 2 题

- 答案：$f(x)=x-1$

设

$$
a=\int_0^1 f(t)\,dt.
$$

由题设得

$$
f(x)=x+2a.
$$

两边在 $[0,1]$ 上积分：

$$
a=\int_0^1 (t+2a)\,dt
=\frac{1}{2}+2a.
$$

因此 $a=-\dfrac{1}{2}$，代回原式，得

$$
f(x)=x+2\left(-\frac{1}{2}\right)=x-1.
$$

### 第 3 题

- 答案：$\pi$

曲线 $L$ 是单位圆的下半圆，因此在 $L$ 上恒有

$$
x^2+y^2=1.
$$

所以

$$
\int_L (x^2+y^2)\,ds
=\int_L 1\,ds.
$$

右端就是下半单位圆弧的长度，故

$$
\int_L (x^2+y^2)\,ds=\pi.
$$

### 第 4 题

- 答案：$2$

原卷中向量场第二分量为 $ye^z$。由散度公式，

$$
\operatorname{div}\boldsymbol{u}
=\frac{\partial}{\partial x}(xy^2)
+\frac{\partial}{\partial y}(ye^z)
+\frac{\partial}{\partial z}\!\left[x\ln(1+z^2)\right].
$$

逐项求偏导：

$$
\operatorname{div}\boldsymbol{u}
=y^2+e^z+x\frac{2z}{1+z^2}.
$$

在 $P(1,1,0)$ 处，

$$
\operatorname{div}\boldsymbol{u}(1,1,0)
=1+1+0=2.
$$

### 第 5 题

- 答案：$\begin{pmatrix}1&0&0\\-\dfrac{1}{2}&\dfrac{1}{2}&0\\0&0&1\end{pmatrix}$

先计算

$$
A-2E=
\begin{pmatrix}
1&0&0\\
1&2&0\\
0&0&1
\end{pmatrix}.
$$

设其逆矩阵为

$$
B=
\begin{pmatrix}
a&0&0\\
b&c&0\\
0&0&d
\end{pmatrix}.
$$

由 $(A-2E)B=E$ 得

$$
\begin{pmatrix}
1&0&0\\
1&2&0\\
0&0&1
\end{pmatrix}
\begin{pmatrix}
a&0&0\\
b&c&0\\
0&0&d
\end{pmatrix}
=
\begin{pmatrix}
a&0&0\\
a+2b&2c&0\\
0&0&d
\end{pmatrix}
=E.
$$

所以

$$
a=1,\quad a+2b=0,\quad 2c=1,\quad d=1.
$$

于是

$$
(A-2E)^{-1}=
\begin{pmatrix}
1&0&0\\
-\dfrac{1}{2}&\dfrac{1}{2}&0\\
0&0&1
\end{pmatrix}.
$$

### 第 6 题

- 答案：A

当 $x\to+\infty$ 时，

$$
x\sin\frac{1}{x}
=\frac{\sin(1/x)}{1/x}\to 1,
$$

所以曲线有水平渐近线 $y=1$。

当 $x\to 0^+$ 时，

$$
\left|x\sin\frac{1}{x}\right|\le x\to 0,
$$

函数值趋于 $0$，不存在铅直渐近线。因此选 A。

### 第 7 题

- 答案：C

将曲面写为

$$
F(x,y,z)=x^2+y^2+z-4=0.
$$

曲面在点 $P(x,y,z)$ 处的法向量为

$$
\nabla F=(2x,2y,1).
$$

平面 $2x+2y+z-1=0$ 的法向量为 $(2,2,1)$。两平面平行，故

$$
(2x,2y,1)=(2,2,1).
$$

于是 $x=1,\ y=1$。代入曲面方程，

$$
z=4-1^2-1^2=2.
$$

故 $P=(1,1,2)$，选 C。

### 第 8 题

- 答案：D

因为 $y_1,y_2,y_3$ 都是同一个非齐次线性方程的解，所以

$$
y_1-y_3,\quad y_2-y_3
$$

都是对应齐次方程的解。二阶线性方程的通解可写成

$$
y=C_1(y_1-y_3)+C_2(y_2-y_3)+y_3.
$$

整理得

$$
y=C_1y_1+C_2y_2+(1-C_1-C_2)y_3.
$$

因此选 D。

### 第 9 题

- 答案：B

给出的级数是 $f(x)=x^2$ 在 $(0,1)$ 上的正弦级数，因此它对应 $f$ 的奇延拓，并以 $2$ 为周期。

在 $x=\dfrac{1}{2}$ 处函数连续，所以

$$
S\left(\frac{1}{2}\right)=\left(\frac{1}{2}\right)^2=\frac{1}{4}.
$$

又 $S(x)$ 为奇函数，故

$$
S\left(-\frac{1}{2}\right)
=-S\left(\frac{1}{2}\right)
=-\frac{1}{4}.
$$

因此选 B。

### 第 10 题

- 答案：C

由 $|A|=0$ 可知矩阵 $A$ 的列向量组线性相关。

列向量组线性相关意味着存在不全为零的常数 $c_1,\cdots,c_n$，使

$$
c_1\alpha_1+\cdots+c_n\alpha_n=0.
$$

取其中一个非零系数 $c_k$，则

$$
\alpha_k=-\frac{1}{c_k}\sum_{i\ne k}c_i\alpha_i.
$$

即至少有一列向量是其余列向量的线性组合。因此选 C。

### 第 11 题

- 答案：$-2f''(2x-y)+g_v(x,xy)+xg_{uv}(x,xy)+xyg_{vv}(x,xy)$

设 $g_u,g_v$ 分别表示 $g(u,v)$ 对第一、第二个变量的偏导数。

先对 $y$ 求偏导：

$$
\frac{\partial z}{\partial y}
=-f'(2x-y)+xg_v(x,xy).
$$

再对 $x$ 求偏导：

$$
\frac{\partial^2z}{\partial x\partial y}
=-2f''(2x-y)
+\frac{\partial}{\partial x}\left[xg_v(x,xy)\right].
$$

由乘积法则和链式法则，

$$
\frac{\partial}{\partial x}\left[xg_v(x,xy)\right]
=g_v(x,xy)+xg_{uv}(x,xy)+xyg_{vv}(x,xy).
$$

所以

$$
\frac{\partial^2z}{\partial x\partial y}
=-2f''(2x-y)+g_v(x,xy)+xg_{uv}(x,xy)+xyg_{vv}(x,xy).
$$

### 第 12 题

- 答案：$\dfrac{1}{2}$

记

$$
P(x,y)=xy^2,\qquad Q(x,y)=y\varphi(x).
$$

曲线积分与路径无关，故在单连通区域内有

$$
\frac{\partial P}{\partial y}
=\frac{\partial Q}{\partial x}.
$$

于是

$$
2xy=y\varphi'(x).
$$

因此 $\varphi'(x)=2x$。又 $\varphi(0)=0$，所以

$$
\varphi(x)=x^2.
$$

原积分化为

$$
\int_{(0,0)}^{(1,1)}xy^2\,dx+x^2y\,dy.
$$

注意到

$$
xy^2\,dx+x^2y\,dy
=\frac{1}{2}\,d(x^2y^2),
$$

故

$$
\int_{(0,0)}^{(1,1)}xy^2\,dx+x^2y\,dy
=\frac{1}{2}\left[x^2y^2\right]_{(0,0)}^{(1,1)}
=\frac{1}{2}.
$$

### 第 13 题

- 答案：$\dfrac{\pi}{8}$

区域 $\Omega$ 由圆锥面

$$
z=\sqrt{x^2+y^2}
$$

和上半球面

$$
z=\sqrt{1-x^2-y^2}
$$

围成。用球坐标

$$
x=\rho\sin\varphi\cos\theta,\quad
y=\rho\sin\varphi\sin\theta,\quad
z=\rho\cos\varphi
$$

表示时，区域为

$$
0\le \rho\le 1,\quad 0\le \varphi\le \frac{\pi}{4},\quad 0\le \theta\le 2\pi.
$$

由于区域关于 $yz$ 平面对称，$\iiint_\Omega x\,dv=0$。因此

$$
\iiint_\Omega (x+z)\,dv=\iiint_\Omega z\,dv.
$$

计算得

$$
\iiint_\Omega z\,dv
=\int_0^{2\pi}\!\int_0^{\pi/4}\!\int_0^1
\rho\cos\varphi\cdot \rho^2\sin\varphi\,d\rho\,d\varphi\,d\theta.
$$

所以

$$
\iiint_\Omega (x+z)\,dv
=2\pi\cdot \frac{1}{4}\cdot
\int_0^{\pi/4}\sin\varphi\cos\varphi\,d\varphi
=2\pi\cdot \frac{1}{4}\cdot \frac{1}{4}
=\frac{\pi}{8}.
$$

### 第 14 题

- 答案：$\displaystyle \frac{\pi}{4}+\sum_{n=0}^{\infty}(-1)^n\frac{x^{2n+1}}{2n+1}$，其中 $-1\le x<1$

设

$$
f(x)=\arctan\frac{1+x}{1-x}.
$$

先求导。令 $u=\dfrac{1+x}{1-x}$，则

$$
u'=\frac{2}{(1-x)^2},
$$

并且

$$
1+u^2
=1+\left(\frac{1+x}{1-x}\right)^2
=\frac{2(1+x^2)}{(1-x)^2}.
$$

因此

$$
f'(x)=\frac{u'}{1+u^2}
=\frac{1}{1+x^2}.
$$

当 $|x|<1$ 时，

$$
\frac{1}{1+x^2}
=\sum_{n=0}^{\infty}(-1)^n x^{2n}.
$$

又 $f(0)=\arctan 1=\dfrac{\pi}{4}$，逐项积分得

$$
f(x)=\frac{\pi}{4}
+\sum_{n=0}^{\infty}(-1)^n\frac{x^{2n+1}}{2n+1},
\qquad |x|<1.
$$

当 $x=-1$ 时，右端为

$$
\frac{\pi}{4}-\sum_{n=0}^{\infty}\frac{(-1)^n}{2n+1}
=\frac{\pi}{4}-\frac{\pi}{4}=0=f(-1),
$$

所以展开式可取 $-1\le x<1$。若按左极限延拓到 $x=1$，级数和为 $\dfrac{\pi}{2}$，但原函数在 $x=1$ 处没有定义。

### 第 15 题

- 答案：$f(x)=\dfrac{1}{2}\sin x+\dfrac{x}{2}\cos x$

由

$$
f(x)=\sin x-\int_0^x (x-t)f(t)\,dt
$$

得

$$
f(0)=0.
$$

对两边求导：

$$
f'(x)=\cos x-\int_0^x f(t)\,dt,
$$

所以 $f'(0)=1$。再求导得

$$
f''(x)=-\sin x-f(x),
$$

即

$$
f''(x)+f(x)=-\sin x.
$$

对应齐次方程的通解为

$$
C_1\cos x+C_2\sin x.
$$

由于右端为 $-\sin x$，取特解

$$
f_p(x)=\frac{x}{2}\cos x,
$$

可验证 $f_p''+f_p=-\sin x$。于是

$$
f(x)=C_1\cos x+C_2\sin x+\frac{x}{2}\cos x.
$$

由 $f(0)=0$ 得 $C_1=0$；由 $f'(0)=1$ 得

$$
C_2+\frac{1}{2}=1,
$$

故 $C_2=\dfrac{1}{2}$。因此

$$
f(x)=\frac{1}{2}\sin x+\frac{x}{2}\cos x.
$$

### 第 16 题

- 答案：证明见解析

记

$$
I=\int_0^\pi\sqrt{1-\cos 2t}\,dt.
$$

显然 $I>0$。将原方程移项，令

$$
F(x)=\ln x-\frac{x}{e}+I,\qquad x>0.
$$

则原方程等价于 $F(x)=0$。

求导得

$$
F'(x)=\frac{1}{x}-\frac{1}{e}.
$$

所以 $F'(x)>0$ 当 $0<x<e$，$F'(x)=0$ 当 $x=e$，$F'(x)<0$ 当 $x>e$。因此 $F$ 在 $(0,e)$ 上严格递增，在 $(e,+\infty)$ 上严格递减。

又

$$
\lim_{x\to 0^+}F(x)=-\infty,\qquad
F(e)=1-1+I=I>0,
$$

所以在 $(0,e)$ 内恰有一个零点。

同时

$$
\lim_{x\to+\infty}F(x)=-\infty,
$$

而 $F(e)>0$，故在 $(e,+\infty)$ 内也恰有一个零点。

综上，原方程在 $(0,+\infty)$ 内有且仅有两个不同实根。

### 第 17 题

- 答案：当 $\lambda=1$ 时有解；通解为 $x_1=1-t,\ x_2=2t-1,\ x_3=t$，其中 $t$ 为任意常数

将增广矩阵作初等行变换：

$$
\left[
\begin{array}{ccc|c}
1&0&1&\lambda\\
4&1&2&\lambda+2\\
6&1&4&2\lambda+3
\end{array}
\right]
\longrightarrow
\left[
\begin{array}{ccc|c}
1&0&1&\lambda\\
0&1&-2&-3\lambda+2\\
0&0&0&-\lambda+1
\end{array}
\right].
$$

方程组有解当且仅当最后一行不矛盾，即

$$
-\lambda+1=0.
$$

所以

$$
\lambda=1.
$$

此时方程组化为

$$
\begin{cases}
x_1+x_3=1,\\
x_2-2x_3=-1.
\end{cases}
$$

令 $x_3=t$，其中 $t$ 为任意常数，则

$$
x_1=1-t,\qquad x_2=2t-1,\qquad x_3=t.
$$

### 第 18 题

- 答案：证明见解析

设 $\alpha\ne 0$ 为 $A$ 属于特征值 $\lambda$ 的特征向量，则

$$
A\alpha=\lambda\alpha.
$$

因为 $A$ 可逆，所以 $\lambda\ne 0$。

两边左乘 $A^{-1}$，得

$$
\alpha=\lambda A^{-1}\alpha,
$$

即

$$
A^{-1}\alpha=\frac{1}{\lambda}\alpha.
$$

所以 $\dfrac{1}{\lambda}$ 是 $A^{-1}$ 的特征值。

又因为

$$
A^{-1}=\frac{A^*}{|A|},
$$

于是

$$
\frac{A^*}{|A|}\alpha=\frac{1}{\lambda}\alpha.
$$

两边同乘 $|A|$，得

$$
A^*\alpha=\frac{|A|}{\lambda}\alpha.
$$

由于 $\alpha\ne 0$，故 $\dfrac{|A|}{\lambda}$ 是伴随矩阵 $A^*$ 的特征值。

### 第 19 题

- 答案：$R=\dfrac{4a}{3}$

由对称性，不妨设球面 $\Sigma$ 的球心为 $(0,0,a)$，其方程为

$$
x^2+y^2+(z-a)^2=R^2.
$$

定球面为

$$
x^2+y^2+z^2=a^2.
$$

两球面相交时，将两式相减，得交线所在平面

$$
z=a-\frac{R^2}{2a}.
$$

球面 $\Sigma$ 位于定球面内部的部分是球面 $\Sigma$ 上靠近原点的一侧球冠。该球冠的高为

$$
h=R-\frac{R^2}{2a}.
$$

因此面积为

$$
S(R)=2\pi Rh
=2\pi R\left(R-\frac{R^2}{2a}\right)
=2\pi R^2-\frac{\pi R^3}{a}.
$$

其中 $0<R<2a$。求导：

$$
S'(R)=4\pi R-\frac{3\pi R^2}{a}
=\pi R\left(4-\frac{3R}{a}\right).
$$

当

$$
R=\frac{4a}{3}
$$

时，$S'(R)$ 由正变负，故 $S(R)$ 取得最大值。

因此，当 $R=\dfrac{4a}{3}$ 时，球面 $\Sigma$ 在定球面内部的那部分面积最大。

### 第 20 题

- 答案：$0.7$

由条件概率公式，

$$
P(AB)=P(A)P(B\mid A)=0.5\times 0.8=0.4.
$$

所以

$$
P(A\cup B)
=P(A)+P(B)-P(AB)
=0.5+0.6-0.4=0.7.
$$

### 第 21 题

- 答案：$0.75$

设事件 $A$ 表示“甲命中”，事件 $B$ 表示“乙命中”。已知

$$
P(A)=0.6,\qquad P(B)=0.5,
$$

且 $A,B$ 独立，所以

$$
P(AB)=0.6\times 0.5=0.3.
$$

目标被命中即事件 $A\cup B$，其概率为

$$
P(A\cup B)=P(A)+P(B)-P(AB)
=0.6+0.5-0.3=0.8.
$$

所求概率为

$$
P(A\mid A\cup B)
=\frac{P(A)}{P(A\cup B)}
=\frac{0.6}{0.8}=0.75.
$$

### 第 22 题

- 答案：$0.8$

方程

$$
x^2+\xi x+1=0
$$

有实根的充要条件是判别式非负：

$$
\Delta=\xi^2-4\ge 0.
$$

因为 $\xi$ 在 $(1,6)$ 上取值，所以 $\xi>0$，从而

$$
\xi^2-4\ge 0 \iff \xi\ge 2.
$$

又 $\xi\sim U(1,6)$，故

$$
P(\xi\ge 2)
=\frac{6-2}{6-1}
=\frac{4}{5}=0.8.
$$

### 第 23 题

- 答案：$f_Z(z)=\dfrac{1}{3\sqrt{2\pi}}\exp\!\left[-\dfrac{(z-5)^2}{18}\right]$

由题意

$$
X\sim N(1,2),\qquad Y\sim N(0,1),
$$

且 $X,Y$ 独立。独立正态随机变量的线性组合仍服从正态分布。

令

$$
Z=2X-Y+3.
$$

则

$$
E(Z)=2E(X)-E(Y)+3=2\cdot 1-0+3=5,
$$

并且

$$
D(Z)=4D(X)+D(Y)=4\cdot 2+1=9.
$$

所以

$$
Z\sim N(5,9).
$$

代入正态分布密度公式，得

$$
f_Z(z)=\frac{1}{3\sqrt{2\pi}}
\exp\left[-\frac{(z-5)^2}{18}\right],
\qquad -\infty<z<+\infty.
$$
