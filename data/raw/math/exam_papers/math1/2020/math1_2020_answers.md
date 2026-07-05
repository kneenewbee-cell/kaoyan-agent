# Math 1 2020 Answers

资料类型：考研数学一答案解析
年份：2020
科目：数学一
校对状态：已根据本年份题目卡、答案速查图和答案页图片逐题清洗补全

## 答案速查

| 题号 | 题型 | 答案 |
|---|---|---|
| 1 | 选择题 | D |
| 2 | 选择题 | C |
| 3 | 选择题 | A |
| 4 | 选择题 | A |
| 5 | 选择题 | B |
| 6 | 选择题 | C |
| 7 | 选择题 | D |
| 8 | 选择题 | B |
| 9 | 填空题 | $-1$ |
| 10 | 填空题 | $-\sqrt{2}$ |
| 11 | 填空题 | $n+am$ |
| 12 | 填空题 | $4e$ |
| 13 | 填空题 | $a^2(a^2-4)$ |
| 14 | 填空题 | $\dfrac{2}{\pi}$ |
| 15 | 解答题 | 极小值 $f\left(\dfrac{1}{6},\dfrac{1}{12}\right)=-\dfrac{1}{216}$ |
| 16 | 解答题 | $I=\pi$ |
| 17 | 解答题 | 幂级数在 $\lvert x\rvert<1$ 时收敛，且 $S(x)=\dfrac{2}{\sqrt{1-x}}-2$ |
| 18 | 解答题 | $I=\dfrac{14\pi}{3}$ |
| 19 | 解答题 | 存在 $\xi\in(0,2)$ 使 $\lvert f'(\xi)\rvert\ge M$；若对任意 $x\in(0,2)$ 有 $\lvert f'(x)\rvert<M$，则 $M=0$ |
| 20 | 解答题 | (I) $a=4,\ b=1$；(II) 可取 $Q=\begin{pmatrix}0&1\\-1&0\end{pmatrix}$ |
| 21 | 解答题 | (I) $P$ 可逆；(II) $P^{-1}AP=\begin{pmatrix}0&6\\1&-1\end{pmatrix}$，且 $A$ 相似于 $\operatorname{diag}(2,-3)$ |
| 22 | 解答题 | (I) $ F(x,y)= \begin{cases} \dfrac{1}{2}\Phi(x)\bigl[\Phi(y)+1\bigr], & x\le y,\\ \dfrac{1}{2}\Phi(y)\bigl[\Phi(x)+1\bigr], & x>y, \end{cases} $ ；(II) $Y\sim N(0,1)$ |
| 23 | 解答题 | (I) $P\{T>t\}=e^{-(t/\theta)^m}$，$P\{T>s+t\mid T>s\}=e^{\frac{s^m-(s+t)^m}{\theta^m}}$；(II) $\hat\theta=\sqrt[m]{\dfrac{1}{n}\sum_{i=1}^n t_i^m}$ |

## 详细解析

### 第 1 题

**标准答案：** D

设

$$
I(x)=\int_0^{\varphi(x)} f(t)\,dt.
$$

若 $f(t)\sim t^m$，$\varphi(x)\sim x^n$，则 $I(x)$ 与 $x^{n(m+1)}$ 同阶。

对四个选项分别估阶：

$$
\text{A}:\ e^{t^2}-1\sim t^2\Rightarrow \int_0^x (e^{t^2}-1)\,dt\sim \int_0^x t^2\,dt\sim x^3;
$$

$$
\text{B}:\ \ln(1+\sqrt{t^3})\sim t^{3/2}\Rightarrow \int_0^x \ln(1+\sqrt{t^3})\,dt\sim x^{5/2};
$$

$$
\text{C}:\ \sin(t^2)\sim t^2,\ \sin x\sim x\Rightarrow \int_0^{\sin x}\sin(t^2)\,dt\sim x^3;
$$

$$
\text{D}:\ \sqrt{\sin^3 t}\sim t^{3/2},\ 1-\cos x\sim \frac{x^2}{2}
\Rightarrow \int_0^{1-\cos x}\sqrt{\sin^3 t}\,dt\sim x^5.
$$

无穷小阶数最高的是 D。

### 第 2 题

**标准答案：** C

若 $f(x)$ 在 $x=0$ 处可导，则 $f$ 在 $0$ 处连续，且

$$
f(0)=\lim_{x\to 0} f(x)=0.
$$

于是

$$
\lim_{x\to 0}\frac{f(x)}{\sqrt{|x|}}
=\lim_{x\to 0}\frac{f(x)}{x}\cdot \frac{x}{\sqrt{|x|}}
=f'(0)\cdot 0=0.
$$

因此 C 必然成立。

A、B 不一定成立。举例：

$$
f(x)=
\begin{cases}
x^3, & x\ne 0,\\
1, & x=0,
\end{cases}
$$

则 $\lim\limits_{x\to 0}\dfrac{f(x)}{\sqrt{|x|}}=0$ 且 $\lim\limits_{x\to 0}\dfrac{f(x)}{x^2}=0$，但 $f$ 在 0 处不连续，更不可导。

D 也不一定成立。取 $f(x)=x$，则 $f$ 在 0 处可导，但

$$
\lim_{x\to 0}\frac{f(x)}{x^2}
=\lim_{x\to 0}\frac{1}{x}
$$

不存在。故选 C。

### 第 3 题

**标准答案：** A

函数 $z=f(x,y)$ 在 $(0,0)$ 处可微时，

$$
\lim_{(x,y)\to (0,0)}
\frac{f(x,y)-f(0,0)-f_x(0,0)x-f_y(0,0)y}{\sqrt{x^2+y^2}}=0.
$$

曲面 $z=f(x,y)$ 在点 $(x,y,f(x,y))$ 处的切平面法向量可写为

$$
n(x,y,f(x,y))=
\bigl(f_x(0,0),\,f_y(0,0),\,-1\bigr)
\cdot
\bigl(x,\,y,\,f(x,y)-f(0,0)\bigr),
$$

它本质上就是上式分子对应的线性余项，因此

$$
\lim_{(x,y)\to (0,0)}
\frac{\left|n\cdot (x,y,f(x,y))\right|}{\sqrt{x^2+y^2}}=0.
$$

故正确选项为 A。

### 第 4 题

**标准答案：** A

若幂级数

$$
\sum_{n=1}^{\infty} a_n x^n
$$

的收敛半径为 $R$，则当 $|r|<R$ 时级数

$$
\sum_{n=1}^{\infty} a_n r^n
$$

收敛。于是其子级数

$$
\sum_{n=1}^{\infty} a_{2n} r^{2n}
$$

也必收敛。

题设给出

$$
\sum_{n=1}^{\infty} a_{2n} r^{2n}
$$

发散，因此只能有 $|r|\ge R$。故选 A。

### 第 5 题

**标准答案：** B

矩阵 $A$ 经过一系列初等列变换得到 $B$，故存在初等矩阵 $P_1,P_2,\dots,P_t$ 使

$$
AP_1P_2\cdots P_t=B.
$$

每个初等矩阵都可逆，于是

$$
A=B(P_1P_2\cdots P_t)^{-1}.
$$

记

$$
P=(P_1P_2\cdots P_t)^{-1},
$$

则 $P$ 可逆，且 $A=BP$。因此选 B。

### 第 6 题

**标准答案：** C

设直线 $L_1,L_2$ 的方向向量分别为

$$
\alpha_1=(a_1,b_1,c_1)^T,\qquad
\alpha_2=(a_2,b_2,c_2)^T.
$$

它们分别经过点

$$
A(a_2,b_2,c_2),\qquad B(a_3,b_3,c_3).
$$

两直线相交的充要条件是：方向向量不平行，且连接向量 $\overrightarrow{AB}=\alpha_3-\alpha_2$ 与 $\alpha_1,\alpha_2$ 共面，即

$$
\det(\alpha_1,\alpha_2,\alpha_3-\alpha_2)=0.
$$

于是

$$
\det(\alpha_1,\alpha_2,\alpha_3)=0.
$$

这说明 $\alpha_1,\alpha_2,\alpha_3$ 线性相关；又因两直线不平行，$\alpha_1,\alpha_2$ 线性无关，所以 $\alpha_3$ 必可由 $\alpha_1,\alpha_2$ 线性表示。故选 C。

### 第 7 题

**标准答案：** D

由题意，$A,B,C$ 中恰有一个发生，故事件可写为

$$
(A\cup B\cup C)\setminus (AB\cup AC\cup BC).
$$

又已知 $P(AB)=0$，于是三者同时发生的概率也为 0，可直接计算

$$
P\bigl((A\cup B\cup C)\setminus (BC\cup AC)\bigr)
=P(A)+P(B)+P(C)-P(BC)-P(AC)-P(BC)-P(AC).
$$

代入题给数据得

$$
\frac{1}{4}+\frac{1}{4}+\frac{1}{4}-\frac{1}{12}-\frac{1}{12}-\frac{1}{12}-\frac{1}{12}
=\frac{5}{12}.
$$

故选 D。

### 第 8 题

**标准答案：** B

设 $X_1,\dots,X_{100}$ 独立同分布，且

$$
P(X_i=1)=P(X_i=0)=\frac{1}{2}.
$$

则

$$
E(X_i)=\frac{1}{2},\qquad D(X_i)=\frac{1}{4}.
$$

因此

$$
\sum_{i=1}^{100}X_i
$$

的均值和方差分别为

$$
100\cdot \frac{1}{2}=50,\qquad 100\cdot \frac{1}{4}=25.
$$

由中心极限定理，

$$
\sum_{i=1}^{100}X_i \approx N(50,25).
$$

于是

$$
P\left\{\sum_{i=1}^{100}X_i\le 55\right\}
=P\left\{\frac{\sum_{i=1}^{100}X_i-50}{5}\le 1\right\}
\approx \Phi(1).
$$

故选 B。

### 第 9 题

**标准答案：** $-1$

通分后有

$$
\frac{1}{e^x-1}-\frac{1}{\ln(1+x)}
=\frac{\ln(1+x)-(e^x-1)}{(e^x-1)\ln(1+x)}.
$$

当 $x\to 0$ 时分子分母都趋于 0，用两次洛必达法则：

$$
\lim_{x\to 0}
\frac{\ln(1+x)-(e^x-1)}{(e^x-1)\ln(1+x)}
=
\lim_{x\to 0}
\frac{\frac{1}{1+x}-e^x}{e^x\ln(1+x)+\frac{e^x-1}{1+x}}.
$$

再对分子分母求导并代入 $x=0$，得

$$
\lim_{x\to 0}
\left[\frac{1}{e^x-1}-\frac{1}{\ln(1+x)}\right]
=-1.
$$

### 第 10 题

**标准答案：** $-\sqrt{2}$

由参数方程

$$
x=\sqrt{1+t^2},\qquad y=\ln t
$$

可得

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}
=\frac{1/t}{t/\sqrt{1+t^2}}
=\frac{\sqrt{1+t^2}}{t^2}.
$$

进一步，

$$
\frac{d^2y}{dx^2}
=\frac{d}{dt}\left(\frac{\sqrt{1+t^2}}{t^2}\right)\Big/\frac{dx}{dt}
=-\frac{\sqrt{1+t^2}}{t^3}.
$$

当 $t=1$ 时，

$$
\frac{d^2y}{dx^2}\Big|_{t=1}=-\sqrt{2}.
$$

### 第 11 题

**标准答案：** $n+am$

由微分方程

$$
f''(x)+af'(x)+f(x)=0
$$

可得

$$
f(x)=-\bigl(f''(x)+af'(x)\bigr).
$$

因此

$$
\int_0^{+\infty} f(x)\,dx
=-\int_0^{+\infty}\bigl(f''(x)+af'(x)\bigr)\,dx
=-f'(+\infty)+f'(0)-a\bigl(f(+\infty)-f(0)\bigr).
$$

特征方程为

$$
\lambda^2+a\lambda+1=0.
$$

由于 $a>0$，其对应解无论是两负实根、重根还是共轭复根，都会满足

$$
f(+\infty)=0,\qquad f'(+\infty)=0.
$$

于是

$$
\int_0^{+\infty} f(x)\,dx
=f'(0)+af(0)=n+am.
$$

### 第 12 题

**标准答案：** $4e$

因 $f(x,y)$ 有二阶连续偏导数，故混合偏导可交换：

$$
\frac{\partial^2 f}{\partial x\partial y}
=\frac{\partial^2 f}{\partial y\partial x}.
$$

由题设先求

$$
\frac{\partial f}{\partial y}
=x e^{x^3y^2}\cdot 2x^2y
=2x^3y e^{x^3y^2}.
$$

再对 $x$ 求偏导：

$$
\frac{\partial^2 f}{\partial y\partial x}
=6x^2y e^{x^3y^2}+6x^5y^3 e^{x^3y^2}.
$$

代入 $(1,1)$ 得

$$
\frac{\partial^2 f}{\partial x\partial y}(1,1)
=\frac{\partial^2 f}{\partial y\partial x}(1,1)
=6e-2e=4e.
$$

### 第 13 题

**标准答案：** $a^2(a^2-4)$

对行列式作不改变值的初等变换：把第 2 行加到第 1 行，第 3 行加到第 4 行；再把第 1 列的 $-1$ 倍加到第 2 列，把第 4 列的 $-1$ 倍加到第 3 列。可化为

$$
\begin{vmatrix}
a&0&0&0\\
0&a&2&-1\\
-1&2&a&0\\
0&0&0&a
\end{vmatrix}.
$$

按第 1 行和第 4 行展开，得

$$
D=a^2
\begin{vmatrix}
a&2\\
2&a
\end{vmatrix}
=a^2(a^2-4).
$$

### 第 14 题

**标准答案：** $\dfrac{2}{\pi}$

设 $X\sim U\left(-\dfrac{\pi}{2},\dfrac{\pi}{2}\right)$，$Y=\sin X$。则

$$
E(X)=0,\qquad E(Y)=E(\sin X)=0.
$$

因此

$$
\operatorname{Cov}(X,Y)=E(XY)=E(X\sin X).
$$

由均匀分布密度可得

$$
E(X\sin X)
=\frac{1}{\pi}\int_{-\pi/2}^{\pi/2} x\sin x\,dx
=\frac{2}{\pi}\int_0^{\pi/2} x\sin x\,dx.
$$

分部积分：

$$
\int_0^{\pi/2} x\sin x\,dx
=\bigl[-x\cos x+\sin x\bigr]_0^{\pi/2}=1.
$$

故

$$
\operatorname{Cov}(X,Y)=\frac{2}{\pi}.
$$

### 第 15 题

**标准答案：** 极小值 $f\left(\dfrac{1}{6},\dfrac{1}{12}\right)=-\dfrac{1}{216}$

先求驻点：

$$
f_x=3x^2-y=0,\qquad f_y=24y^2-x=0.
$$

联立得驻点

$$
(0,0),\qquad \left(\frac{1}{6},\frac{1}{12}\right).
$$

再求二阶偏导：

$$
A=f_{xx}=6x,\qquad B=f_{xy}=-1,\qquad C=f_{yy}=48y.
$$

判别式

$$
\Delta=AC-B^2=288xy-1.
$$

在 $(0,0)$ 处，

$$
\Delta=-1<0,
$$

不是极值点。

在 $\left(\dfrac{1}{6},\dfrac{1}{12}\right)$ 处，

$$
\Delta=288\cdot \frac{1}{6}\cdot\frac{1}{12}-1=3>0,
\qquad
A=1>0,
$$

故该点为极小值点。代入原函数：

$$
f\left(\frac{1}{6},\frac{1}{12}\right)
=\left(\frac{1}{6}\right)^3+8\left(\frac{1}{12}\right)^3-\frac{1}{6}\cdot\frac{1}{12}
=-\frac{1}{216}.
$$

### 第 16 题

**标准答案：** $I=\pi$

由 $L:x^2+y^2=2$ 且方向为逆时针方向，令

$$
x=\sqrt{2}\cos t,\qquad y=\sqrt{2}\sin t,\qquad 0\le t\le 2\pi.
$$

则

$$
dx=-\sqrt{2}\sin t\,dt,\qquad dy=\sqrt{2}\cos t\,dt,
$$

且

$$
4x^2+y^2=2(4\cos^2t+\sin^2t)=2(1+3\cos^2t).
$$

代入曲线积分的被积表达式：

$$
\begin{aligned}
\frac{4x-y}{4x^2+y^2}\,dx+\frac{x+y}{4x^2+y^2}\,dy
&=\frac{(4\sqrt{2}\cos t-\sqrt{2}\sin t)(-\sqrt{2}\sin t)
+(\sqrt{2}\cos t+\sqrt{2}\sin t)(\sqrt{2}\cos t)}
{2(1+3\cos^2t)}\,dt\\
&=\frac{1-3\sin t\cos t}{1+3\cos^2t}\,dt.
\end{aligned}
$$

因此

$$
I=\int_0^{2\pi}\frac{dt}{1+3\cos^2t}
-3\int_0^{2\pi}\frac{\sin t\cos t}{1+3\cos^2t}\,dt.
$$

第二个积分在 $[0,2\pi]$ 上为 $0$。又由

$$
\int_0^{2\pi}\frac{dt}{a+b\cos^2t}=\frac{2\pi}{\sqrt{a(a+b)}}\quad(a>0,\ a+b>0),
$$

取 $a=1,b=3$，得

$$
\int_0^{2\pi}\frac{dt}{1+3\cos^2t}=\frac{2\pi}{\sqrt{1\cdot4}}=\pi.
$$

故

$$
I=\pi.
$$

### 第 17 题

**标准答案：** 幂级数在 $\lvert x\rvert<1$ 时收敛，且 $S(x)=\dfrac{2}{\sqrt{1-x}}-2$

由递推式

$$
(n+1)a_{n+1}=\left(n+\frac{1}{2}\right)a_n
$$

得

$$
\frac{a_{n+1}}{a_n}=\frac{n+\frac{1}{2}}{n+1}\xrightarrow[n\to\infty]{}1.
$$

因此幂级数

$$
S(x)=\sum_{n=1}^{\infty} a_n x^n
$$

的收敛半径为 $R=1$，故当 $\lvert x\rvert<1$ 时收敛。

对 $S(x)$ 求导：

$$
S'(x)=\sum_{n=1}^{\infty} n a_n x^{n-1}
=\sum_{n=1}^{\infty} (n+1)a_{n+1}x^n+a_1.
$$

利用递推式，

$$
S'(x)=\sum_{n=1}^{\infty}\left(n+\frac{1}{2}\right)a_n x^n+1
=xS'(x)+\frac{1}{2} S(x)+1.
$$

故

$$
(1-x)S'(x)=\frac{1}{2} S(x)+1,
$$

即

$$
\frac{S'(x)}{S(x)+2}=\frac{1}{2(1-x)}.
$$

积分得

$$
\ln|S(x)+2|=-\frac{1}{2}\ln(1-x)+C,
$$

所以

$$
S(x)+2=\frac{C_1}{\sqrt{1-x}}.
$$

又因 $S(0)=0$，得 $C_1=2$，故

$$
S(x)=\frac{2}{\sqrt{1-x}}-2.
$$

### 第 18 题

**标准答案：** $I=\dfrac{14\pi}{3}$

曲面为

$$
z=\sqrt{x^2+y^2},\qquad 1\le x^2+y^2\le 4,
$$

取下侧时，可用投影到 $xy$ 平面的方法。记

$$
P=x f(xy)+2x-y,\quad
Q=y f(xy)+2y+x,\quad
R=z f(xy)+z.
$$

则下侧法向对应

$$
I=\iint_D \bigl(Pz_x+Qz_y-R\bigr)\,dxdy,
$$

其中

$$
z_x=\frac{x}{\sqrt{x^2+y^2}},\qquad
z_y=\frac{y}{\sqrt{x^2+y^2}},\qquad
D=\{(x,y)\mid 1\le x^2+y^2\le 4\}.
$$

代入并利用 $z=\sqrt{x^2+y^2}$ 化简，含 $f(xy)$ 的项全部抵消，得到

$$
I=\iint_D \sqrt{x^2+y^2}\,dxdy.
$$

改用极坐标：

$$
I=\int_0^{2\pi}\int_1^2 r\cdot r\,dr\,d\theta
=2\pi\int_1^2 r^2\,dr
=2\pi\cdot \frac{8-1}{3}
=\frac{14\pi}{3}.
$$

### 第 19 题

**标准答案：** 存在 $\xi\in(0,2)$ 使 $\lvert f'(\xi)\rvert\ge M$；若对任意 $x\in(0,2)$ 有 $\lvert f'(x)\rvert<M$，则 $M=0$

设 $c\in[0,2]$ 满足

$$
\lvert f(c)\rvert=M.
$$

1. 若 $c\in(0,1]$，由拉格朗日中值定理，存在 $\xi\in(0,c)$ 使

$$
f'(\xi)=\frac{f(c)-f(0)}{c}=\frac{f(c)}{c},
$$

故

$$
\lvert f'(\xi)\rvert=\frac{\lvert f(c)\rvert}{c}=\frac{M}{c}\ge M.
$$

若 $c\in(1,2)$，同理在区间 $[c,2]$ 上存在 $\xi\in(c,2)$ 使

$$
f'(\xi)=\frac{f(2)-f(c)}{2-c}=-\frac{f(c)}{2-c},
$$

于是

$$
\lvert f'(\xi)\rvert=\frac{M}{2-c}\ge M.
$$

若 $c=1$，上述任一侧都可得到结论。因此存在 $\xi\in(0,2)$ 使 $\lvert f'(\xi)\rvert\ge M$。

2. 若对任意 $x\in(0,2)$ 都有 $\lvert f'(x)\rvert<M$，分情形讨论。

若 $c\in[0,1)$，则

$$
M=\lvert f(c)-f(0)\rvert\le c\max_{(0,1)}\lvert f'(x)\rvert<cM\le M,
$$

只能推出 $M=0$。

若 $c\in(1,2]$，同理也有 $M=0$。

若 $c=1$ 且 $M>0$，则

$$
M=|f(1)-f(0)|
=\left|\int_0^1 f'(x)\,dx\right|
\le \int_0^1 \lvert f'(x)\rvert\,dx
<\int_0^1 M\,dx=M,
$$

矛盾。

故必有

$$
M=0.
$$

### 第 20 题

**标准答案：** (I) $a=4,\ b=1$；(II) 可取 $Q=\begin{pmatrix}0&1\\-1&0\end{pmatrix}$

设二次型 $f,g$ 的矩阵分别为

$$
A=\begin{pmatrix}1&-2\\-2&4\end{pmatrix},\qquad
B=\begin{pmatrix}a&2\\2&b\end{pmatrix}.
$$

因 $f$ 经正交变换化为 $g$，故 $A,B$ 相似，从而迹与行列式分别相等：

$$
a+b=\operatorname{tr}(B)=\operatorname{tr}(A)=5,
$$

$$
ab-4=\det B=\det A=0.
$$

故

$$
ab=4.
$$

联立并结合 $a\ge b$ 得

$$
a=4,\qquad b=1.
$$

再看

$$
f(x_1,x_2)=x_1^2-4x_1x_2+4x_2^2,
$$

若取

$$
x_1=y_2,\qquad x_2=-y_1,
$$

即

$$
\begin{pmatrix}x_1\\x_2\end{pmatrix}
=
\begin{pmatrix}0&1\\-1&0\end{pmatrix}
\begin{pmatrix}y_1\\y_2\end{pmatrix},
$$

则

$$
f(x_1,x_2)=4y_1^2+4y_1y_2+y_2^2.
$$

故所求正交矩阵可取

$$
Q=\begin{pmatrix}0&1\\-1&0\end{pmatrix}.
$$

### 第 21 题

**标准答案：** (I) $P$ 可逆；(II) $P^{-1}AP=\begin{pmatrix}0&6\\1&-1\end{pmatrix}$，且 $A$ 相似于 $\operatorname{diag}(2,-3)$

因为 $\alpha\ne 0$ 且 $\alpha$ 不是 $A$ 的特征向量，所以

$$
A\alpha\neq k\alpha
$$

对任意常数 $k$ 都成立，从而向量 $\alpha$ 与 $A\alpha$ 不共线，线性无关。故

$$
P=(\alpha, A\alpha)
$$

可逆。

又由条件

$$
A^2\alpha+A\alpha-6\alpha=0
$$

可得

$$
A^2\alpha=6\alpha-A\alpha.
$$

因此

$$
AP=A(\alpha,A\alpha)=(A\alpha,A^2\alpha)
=(\alpha,A\alpha)
\begin{pmatrix}
0&6\\
1&-1
\end{pmatrix}.
$$

两边左乘 $P^{-1}$，得

$$
P^{-1}AP=
\begin{pmatrix}
0&6\\
1&-1
\end{pmatrix}.
$$

该矩阵的特征多项式为

$$
\lambda^2+\lambda-6=(\lambda-2)(\lambda+3),
$$

有两个不同特征值 $2,-3$，故它可对角化，从而 $A$ 也可对角化，并且

$$
A\sim \operatorname{diag}(2,-3).
$$

### 第 22 题

**标准答案：** (I)
$$
F(x,y)=
\begin{cases}
\dfrac{1}{2}\Phi(x)\bigl[\Phi(y)+1\bigr], & x\le y,\\
\dfrac{1}{2}\Phi(y)\bigl[\Phi(x)+1\bigr], & x>y,
\end{cases}
$$
；(II) $Y\sim N(0,1)$

由

$$
Y=X_3X_1+(1-X_3)X_2
$$

且

$$
P(X_3=0)=P(X_3=1)=\frac{1}{2}
$$

可分情形计算。

1. 二维分布函数

$$
F(x,y)=P(X_1\le x, Y\le y).
$$

按 $X_3$ 分类：

$$
\begin{aligned}
F(x,y)
&=\frac{1}{2} P(X_1\le x, X_2\le y)+\frac{1}{2} P(X_1\le x, X_1\le y)\\
&=\frac{1}{2} \Phi(x)\Phi(y)+\frac{1}{2} \Phi(\min\{x,y\}).
\end{aligned}
$$

故

$$
F(x,y)=
\begin{cases}
\dfrac{1}{2}\Phi(x)\Phi(y)+\dfrac{1}{2}\Phi(x)
=\dfrac{1}{2}\Phi(x)[\Phi(y)+1], & x\le y,\\
\dfrac{1}{2}\Phi(x)\Phi(y)+\dfrac{1}{2}\Phi(y)
=\dfrac{1}{2}\Phi(y)[\Phi(x)+1], & x>y.
\end{cases}
$$

2. 求 $Y$ 的分布函数：

$$
\begin{aligned}
F_Y(y)
&=P(Y\le y)\\
&=\frac{1}{2} P(X_2\le y)+\frac{1}{2} P(X_1\le y)\\
&=\frac{1}{2}\Phi(y)+\frac{1}{2}\Phi(y)=\Phi(y).
\end{aligned}
$$

而 $\Phi(y)$ 正是标准正态分布函数，因此

$$
Y\sim N(0,1).
$$

### 第 23 题

**标准答案：** (I) $P\{T>t\}=e^{-(t/\theta)^m}$，$P\{T>s+t\mid T>s\}=e^{\frac{s^m-(s+t)^m}{\theta^m}}$；(II) $\hat\theta=\sqrt[m]{\dfrac{1}{n}\sum_{i=1}^n t_i^m}$

由分布函数

$$
F(t)=
\begin{cases}
1-e^{-(t/\theta)^m}, & t\ge 0,\\
0, & t<0
\end{cases}
$$

知

$$
P(T>t)=1-F(t)=e^{-(t/\theta)^m}\quad (t>0).
$$

于是

$$
P(T>s+t\mid T>s)
=\frac{P(T>s+t)}{P(T>s)}
=e^{-\frac{(s+t)^m}{\theta^m}+\frac{s^m}{\theta^m}}
=e^{\frac{s^m-(s+t)^m}{\theta^m}}.
$$

再求极大似然估计。密度函数为

$$
f(t)=F'(t)=
\begin{cases}
\dfrac{m}{\theta}\left(\dfrac{t}{\theta}\right)^{m-1}e^{-(t/\theta)^m}, & t\ge 0,\\
0, & t<0.
\end{cases}
$$

对样本 $t_1,\dots,t_n$，

$$
L(\theta)=\prod_{i=1}^n f(t_i)
=m^n\prod_{i=1}^n t_i^{m-1}\cdot \theta^{-mn}
\exp\left(-\sum_{i=1}^n \frac{t_i^m}{\theta^m}\right).
$$

取对数得

$$
\ln L(\theta)
=n\ln m+(m-1)\sum_{i=1}^n \ln t_i-mn\ln\theta-\sum_{i=1}^n \frac{t_i^m}{\theta^m}.
$$

求导并令其为 0：

$$
\frac{d\ln L}{d\theta}
=-\frac{mn}{\theta}+m\sum_{i=1}^n \frac{t_i^m}{\theta^{m+1}}=0.
$$

化简得

$$
\theta^m=\frac{1}{n}\sum_{i=1}^n t_i^m.
$$

故

$$
\hat\theta=\sqrt[m]{\frac{1}{n}\sum_{i=1}^n t_i^m}.
$$
