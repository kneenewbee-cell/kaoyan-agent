# 2000 数学三答案与解析


## 第 1 题
### 标准答案

设
$$
u=xy,\qquad v=\frac{x}{y},
$$
则
$$
\frac{\partial z}{\partial x}
=y\,f_1\left(xy,\frac{x}{y}\right)
+\frac{1}{y}\,f_2\left(xy,\frac{x}{y}\right)
+\frac{1}{y}\,g'\left(\frac{x}{y}\right).
$$

### 解析

记
$$
u=xy,\qquad v=\frac{x}{y},
$$
则
$$
z=f(u,v)+g(v).
$$
由链式法则，
$$
\frac{\partial z}{\partial x}
=f_1(u,v)\frac{\partial u}{\partial x}
+f_2(u,v)\frac{\partial v}{\partial x}
+g'(v)\frac{\partial v}{\partial x}.
$$
又因为
$$
\frac{\partial u}{\partial x}=y,\qquad
\frac{\partial v}{\partial x}=\frac{1}{y},
$$
故
$$
\frac{\partial z}{\partial x}
=y\,f_1\left(xy,\frac{x}{y}\right)
+\frac{1}{y}\,f_2\left(xy,\frac{x}{y}\right)
+\frac{1}{y}\,g'\left(\frac{x}{y}\right).
$$

## 第 2 题
### 标准答案

$$
\frac{\pi}{4e}
$$

### 解析

将分子分母同乘以 $e^x$，得
$$
\int_1^{+\infty}\frac{dx}{e^x+e^{2-x}}
=\int_1^{+\infty}\frac{e^x\,dx}{e^{2x}+e^2}.
$$
令
$$
t=\frac{e^x}{e},
$$
则
$$
dt=\frac{e^x}{e}\,dx=t\,dx,\qquad dx=\frac{dt}{t}.
$$
当 $x=1$ 时，$t=1$；当 $x\to+\infty$ 时，$t\to+\infty$。于是
$$
\int_1^{+\infty}\frac{e^x\,dx}{e^{2x}+e^2}
=\frac{1}{e}\int_1^{+\infty}\frac{dt}{1+t^2}.
$$
因此
$$
\int_1^{+\infty}\frac{dx}{e^x+e^{2-x}}
=\frac{1}{e}\left[\arctan t\right]_1^{+\infty}
=\frac{1}{e}\left(\frac{\pi}{2}-\frac{\pi}{4}\right)
=\frac{\pi}{4e}.
$$

## 第 3 题
### 标准答案

$$
24
$$

### 解析

因为 $A$ 与 $B$ 相似，所以 $A,B$ 有相同的特征值，即
$$
\frac12,\ \frac13,\ \frac14,\ \frac15.
$$
于是 $B^{-1}$ 的特征值分别为
$$
2,\ 3,\ 4,\ 5.
$$
因此 $B^{-1}-E$ 的特征值为
$$
2-1,\ 3-1,\ 4-1,\ 5-1,
$$
即
$$
1,\ 2,\ 3,\ 4.
$$
矩阵的行列式等于全部特征值的乘积，所以
$$
\left|B^{-1}-E\right|=1\cdot2\cdot3\cdot4=24.
$$

## 第 4 题
### 标准答案

$$
[1,3]
$$

### 解析

先计算区间上的概率质量：
$$
P\{0\le X\le1\}=\int_0^1\frac13\,dx=\frac13,
$$
$$
P\{3\le X\le6\}=\int_3^6\frac29\,dx=\frac23.
$$
因此总概率恰好为 $1$。

若 $1\le k\le3$，则
$$
P\{X\ge k\}=P\{3\le X\le6\}=\frac23,
$$
因为区间 $(1,3)$ 上没有概率质量。

若 $k<1$，则
$$
P\{X\ge k\}>P\{X\ge1\}=\frac23;
$$
若 $k>3$，则
$$
P\{X\ge k\}<P\{X\ge3\}=\frac23.
$$
故满足
$$
P\{X\ge k\}=\frac23
$$
的全部 $k$ 为
$$
k\in[1,3].
$$

## 第 5 题
### 标准答案

$$
\frac{8}{9}
$$

### 解析

因为 $X$ 在区间 $[-1,2]$ 上服从均匀分布，所以
$$
P\{X<0\}=\frac{0-(-1)}{2-(-1)}=\frac13,\qquad
P\{X>0\}=\frac{2-0}{2-(-1)}=\frac23,
$$
且
$$
P\{X=0\}=0.
$$
于是随机变量 $Y$ 的分布为
$$
P\{Y=-1\}=\frac13,\qquad P\{Y=1\}=\frac23.
$$
故
$$
E(Y)=(-1)\cdot\frac13+1\cdot\frac23=\frac13,
$$
$$
E(Y^2)=(-1)^2\cdot\frac13+1^2\cdot\frac23=1.
$$
因此
$$
D(Y)=E(Y^2)-[E(Y)]^2
=1-\left(\frac13\right)^2
=\frac89.
$$

## 第 6 题
### 标准答案

（D）

### 解析

由题设只知道
$$
\varphi(x)\le f(x)\le g(x),\qquad g(x)-\varphi(x)\to0\quad(x\to\infty),
$$
但不能推出 $f(x)$ 的极限一定存在。

先举一个极限存在的例子：取
$$
\varphi(x)=1,\qquad g(x)=1+\frac{1}{x},\qquad f(x)=1+\frac{1}{2x}.
$$
则显然
$$
\varphi(x)\le f(x)\le g(x),\qquad g(x)-\varphi(x)=\frac1x\to0,
$$
并且
$$
\lim_{x\to\infty}f(x)=1.
$$
所以极限存在时也不一定等于 $0$，排除（A）、（B）。

再举一个极限不存在的例子：取
$$
\varphi(x)=\sin x-\frac{1}{x^2},\qquad
g(x)=\sin x+\frac{1}{x^2},\qquad
f(x)=\sin x.
$$
则有
$$
\varphi(x)\le f(x)\le g(x),\qquad g(x)-\varphi(x)=\frac{2}{x^2}\to0,
$$
但
$$
\lim_{x\to\infty}\sin x
$$
不存在。

因此
$$
\lim_{x\to\infty}f(x)
$$
不一定存在，故选（D）。

## 第 7 题
### 标准答案

（B）

### 解析

若 $f(a)=0$ 且 $f'(a)\ne0$，则
$$
\lim_{x\to a}\frac{f(x)-f(a)}{x-a}=f'(a)\ne0.
$$
因此在 $a$ 的邻域内，$f(x)$ 在 $a$ 的两侧异号，故 $|f(x)|$ 在 $x=a$ 处会出现尖点。

更具体地说，由 $f(a)=0$ 可得
$$
|f(x)|=
\begin{cases}
 f(x), & x>a\ \text{且充分接近 }a,\\
-f(x), & x<a\ \text{且充分接近 }a,
\end{cases}
$$
或者左右两侧情况相反。于是
$$
\lim_{x\to a^+}\frac{|f(x)|-|f(a)|}{x-a}=f'(a),
$$
$$
\lim_{x\to a^-}\frac{|f(x)|-|f(a)|}{x-a}=-f'(a).
$$
由于 $f'(a)\ne0$，左右导数不相等，所以 $|f(x)|$ 在 $x=a$ 处不可导。

故充分条件是
$$
f(a)=0,\qquad f'(a)\ne0,
$$
即选（B）。

## 第 8 题
### 标准答案

（C）

### 解析

因为 $\alpha_1,\alpha_2,\alpha_3$ 都是非齐次方程组 $AX=b$ 的解，所以
$$
A\alpha_1=A\alpha_2=A\alpha_3=b.
$$
于是 $\alpha_1$ 是一个特解。

又因为 $r(A)=3$，未知量个数为 $4$，所以对应齐次方程组 $AX=0$ 的基础解系只含 $1$ 个向量。

由
$$
A\bigl(2\alpha_1-(\alpha_2+\alpha_3)\bigr)
=2b-b=0,
$$
可知
$$
2\alpha_1-(\alpha_2+\alpha_3)
$$
是齐次方程组的一个非零解，从而可作为基础解系。计算得
$$
2\alpha_1-(\alpha_2+\alpha_3)
=2\begin{pmatrix}1\\2\\3\\4\end{pmatrix}
-\begin{pmatrix}0\\1\\2\\3\end{pmatrix}
=\begin{pmatrix}2\\3\\4\\5\end{pmatrix}.
$$
因此原非齐次方程组的通解为
$$
X=\alpha_1+c\begin{pmatrix}2\\3\\4\\5\end{pmatrix}
=\begin{pmatrix}1\\2\\3\\4\end{pmatrix}
+c\begin{pmatrix}2\\3\\4\\5\end{pmatrix}.
$$
故选（C）。

## 第 9 题
### 标准答案

（A）

### 解析

若 $X$ 是方程组（Ⅰ）
$$
AX=0
$$
的解，则左乘 $A^T$ 得
$$
A^TAX=0,
$$
所以 $X$ 也是方程组（Ⅱ）的解。

反过来，若 $X$ 是方程组（Ⅱ）
$$
A^TAX=0
$$
的解，则左乘 $X^T$，得
$$
X^TA^TAX=(AX)^T(AX)=0.
$$
而
$$
(AX)^T(AX)=\|AX\|^2\ge0,
$$
只有当
$$
AX=0
$$
时才等于 $0$。因此 $X$ 也是方程组（Ⅰ）的解。

故两个方程组的解集相同，选（A）。

## 第 10 题
### 标准答案

（C）

### 解析

按题意，事件 $E$ 表示“至少有两个温控器显示温度不低于 $t_0$”。

把四个显示值按从小到大排列为
$$
T_{(1)}\le T_{(2)}\le T_{(3)}\le T_{(4)}.
$$
若至少有两个温控器显示值不低于 $t_0$，那么最大的两个显示值中较小的那个也必满足
$$
T_{(3)}\ge t_0.
$$

反过来，若
$$
T_{(3)}\ge t_0,
$$
则 $T_{(3)},T_{(4)}$ 都不低于 $t_0$，从而确有两个温控器满足条件，电炉断电。

所以
$$
E=\{T_{(3)}\ge t_0\}.
$$
故选（C）。

## 第 11 题
### 标准答案

$$
y=\frac{(1+2x)e^{2x}-1}{4}
$$

### 解析

原方程可写为
$$
y''-2y'=e^{2x}.
$$

先解对应齐次方程
$$
y''-2y'=0.
$$
其特征方程为
$$
r^2-2r=0,
$$
特征根为 $r=0,2$，故齐次方程通解为
$$
y_h=C_1+C_2e^{2x}.
$$

因为右端是 $e^{2x}$，而 $2$ 是特征根的单根，所以设特解为
$$
y_p=Ax e^{2x}.
$$
则
$$
y_p'=Ae^{2x}+2Axe^{2x},\qquad
y_p''=4Ae^{2x}+4Axe^{2x}.
$$
代入原方程，得
$$
y_p''-2y_p'=2Ae^{2x}=e^{2x},
$$
故
$$
A=\frac12.
$$
于是
$$
y_p=\frac12 xe^{2x}.
$$

所以原方程通解为
$$
y=C_1+C_2e^{2x}+\frac12 xe^{2x}.
$$
再由初始条件 $y(0)=0,\ y'(0)=1$，得
$$
C_1+C_2=0,
$$
$$
2C_2+\frac12=1.
$$
解得
$$
C_2=\frac14,\qquad C_1=-\frac14.
$$
因此所求解为
$$
y=-\frac14+\frac14e^{2x}+\frac12xe^{2x}
=\frac{(1+2x)e^{2x}-1}{4}.
$$

## 第 12 题
### 标准答案

$$
\iint_D \frac{\sqrt{x^2+y^2}}{\sqrt{4a^2-x^2-y^2}}\,d\sigma
=a^2\left(\frac{\pi^2}{16}-\frac12\right)
$$

### 解析

将曲线
$$
y=-a+\sqrt{a^2-x^2}
$$
化为
$$
x^2+(y+a)^2=a^2,\qquad y\ge -a.
$$
改用极坐标 $x=r\cos\theta,\ y=r\sin\theta$，则该圆弧方程为
$$
r=-2a\sin\theta\qquad\left(-\pi\le\theta\le0\right).
$$
直线 $y=-x$ 对应 $\theta=-\dfrac{\pi}{4}$，因此积分区域为
$$
-\frac{\pi}{4}\le\theta\le0,\qquad 0\le r\le -2a\sin\theta.
$$

于是
$$
I=\iint_D \frac{\sqrt{x^2+y^2}}{\sqrt{4a^2-x^2-y^2}}\,d\sigma
=\int_{-\pi/4}^0\int_0^{-2a\sin\theta}\frac{r^2}{\sqrt{4a^2-r^2}}\,dr\,d\theta.
$$

对内层积分令
$$
r=2a\sin t\quad (0\le t\le -\theta),
$$
则
$$
dr=2a\cos t\,dt,
$$
从而
$$
\frac{r^2}{\sqrt{4a^2-r^2}}\,dr
=\frac{4a^2\sin^2 t}{2a\cos t}\cdot 2a\cos t\,dt
=4a^2\sin^2 t\,dt.
$$
故
$$
I=\int_{-\pi/4}^0\int_0^{-\theta}4a^2\sin^2 t\,dt\,d\theta
=4a^2\int_{-\pi/4}^0\left(\frac{-\theta}{2}+\frac{\sin 2\theta}{4}\right)d\theta.
$$
即
$$
I=a^2\int_{-\pi/4}^0\bigl(-2\theta+\sin 2\theta\bigr)\,d\theta.
$$
计算得
$$
I=a^2\left[-\theta^2-\frac12\cos 2\theta\right]_{-\pi/4}^0
=a^2\left(\frac{\pi^2}{16}-\frac12\right).
$$

## 第 13 题
### 标准答案

（A）价格差别时，
$$
Q_1=8,\quad Q_2=5,\quad P_1=10,\quad P_2=7,
$$
最大利润为 $84$ 万元。

（B）价格无差别时，
$$
Q_1=\frac{19}{2},\quad Q_2=\frac{7}{2},\quad P=\frac{17}{2},
$$
最大利润为 $\dfrac{159}{2}$ 万元。

故价格差别策略下的最大利润更大。

### 解析

设总利润为 $L$。

由
$$
P_1=18-Q_1,\qquad P_2=12-Q_2,
$$
以及总成本
$$
C=2(Q_1+Q_2)+5,
$$
可得利润函数
$$
\begin{aligned}
L&=P_1Q_1+P_2Q_2-C\\
&=(18-Q_1)Q_1+(12-Q_2)Q_2-2(Q_1+Q_2)-5\\
&=-Q_1^2-Q_2^2+16Q_1+10Q_2-5.
\end{aligned}
$$

### （A）价格差别策略

此时 $Q_1,Q_2$ 可分别独立选取，令偏导数为零：
$$
\frac{\partial L}{\partial Q_1}=-2Q_1+16=0,\qquad
\frac{\partial L}{\partial Q_2}=-2Q_2+10=0.
$$
解得
$$
Q_1=8,\qquad Q_2=5.
$$
相应价格为
$$
P_1=18-8=10,\qquad P_2=12-5=7.
$$
最大利润为
$$
L_{\max}=10\cdot8+7\cdot5-2(8+5)-5=84\ \text{万元}.
$$

### （B）价格无差别策略

若两个市场实行统一价格 $P$，则
$$
P=P_1=P_2,
$$
所以
$$
18-Q_1=12-Q_2,
$$
即
$$
Q_1-Q_2=6.
$$
令
$$
Q_1=Q_2+6,
$$
代入利润函数得
$$
\begin{aligned}
L&=-(Q_2+6)^2-Q_2^2+16(Q_2+6)+10Q_2-5\\
&=-2Q_2^2+14Q_2+55.
\end{aligned}
$$
令导数为零：
$$
\frac{dL}{dQ_2}=-4Q_2+14=0,
$$
得
$$
Q_2=\frac72,\qquad Q_1=\frac{19}{2}.
$$
统一价格为
$$
P=18-Q_1=12-Q_2=\frac{17}{2}.
$$
此时最大利润为
$$
L_{\max}
=\frac{17}{2}\left(\frac{19}{2}+\frac72\right)-2\cdot13-5
=\frac{159}{2}\ \text{万元}.
$$

因为
$$
84>\frac{159}{2}=79.5,
$$
故价格差别策略下的总利润更大。

## 第 14 题
### 标准答案

单调递增区间为
$$
(-\infty,-1)\cup(0,+\infty),
$$
单调递减区间为
$$
(-1,0).
$$

极大值为
$$
y(-1)=-2e^{\pi/4},
$$
极小值为
$$
y(0)=-e^{\pi/2}.
$$

渐近线为
$$
y=x-2,\qquad y=e^\pi x-2e^\pi.
$$

### 解析

设
$$
y=(x-1)e^{\frac{\pi}{2}+\arctan x}.
$$
对 $x$ 求导：
$$
\begin{aligned}
y'
&=e^{\frac{\pi}{2}+\arctan x}
+(x-1)e^{\frac{\pi}{2}+\arctan x}\cdot\frac{1}{1+x^2}\\
&=e^{\frac{\pi}{2}+\arctan x}\left(1+\frac{x-1}{1+x^2}\right)\\
&=e^{\frac{\pi}{2}+\arctan x}\cdot\frac{x^2+x}{1+x^2}\\
&=e^{\frac{\pi}{2}+\arctan x}\cdot\frac{x(x+1)}{1+x^2}.
\end{aligned}
$$
由于指数因子始终为正，故 $y'$ 的符号由 $x(x+1)$ 决定：

- 当 $x<-1$ 时，$y'>0$；
- 当 $-1<x<0$ 时，$y'<0$；
- 当 $x>0$ 时，$y'>0$。

因此函数在
$$
(-\infty,-1),\quad (0,+\infty)
$$
上单调递增，在
$$
(-1,0)
$$
上单调递减。

计算驻点函数值：
$$
y(-1)=(-2)e^{\frac{\pi}{2}-\frac{\pi}{4}}=-2e^{\pi/4},
$$
$$
y(0)=(-1)e^{\pi/2}=-e^{\pi/2}.
$$
所以 $x=-1$ 处取得极大值 $-2e^{\pi/4}$，$x=0$ 处取得极小值 $-e^{\pi/2}$。

下面求渐近线。

当 $x\to+\infty$ 时，
$$
\arctan x=\frac{\pi}{2}-\frac{1}{x}+o\!\left(\frac1x\right),
$$
故
$$
e^{\frac{\pi}{2}+\arctan x}
=e^\pi\left(1-\frac1x+o\!\left(\frac1x\right)\right).
$$
于是
$$
y=(x-1)e^\pi\left(1-\frac1x+o\!\left(\frac1x\right)\right)
=e^\pi x-2e^\pi+o(1).
$$
故当 $x\to+\infty$ 时的斜渐近线为
$$
y=e^\pi x-2e^\pi.
$$

当 $x\to-\infty$ 时，
$$
\arctan x=-\frac{\pi}{2}-\frac{1}{x}+o\!\left(\frac1x\right),
$$
从而
$$
e^{\frac{\pi}{2}+\arctan x}
=1-\frac1x+o\!\left(\frac1x\right).
$$
因此
$$
y=(x-1)\left(1-\frac1x+o\!\left(\frac1x\right)\right)
=x-2+o(1).
$$
故当 $x\to-\infty$ 时的斜渐近线为
$$
y=x-2.
$$

## 第 15 题
### 标准答案

$$
\sum_{n=0}^{\infty}I_n=\ln(2+\sqrt2)
$$

### 解析

由换元 $u=\sin x$，得
$$
du=\cos x\,dx,
$$
所以
$$
I_n=\int_0^{\pi/4}\sin^n x\cos x\,dx
=\int_0^{\sqrt2/2}u^n\,du
=\frac{(\sqrt2/2)^{n+1}}{n+1}.
$$

于是
$$
\sum_{n=0}^{\infty}I_n
=\sum_{n=0}^{\infty}\frac{(\sqrt2/2)^{n+1}}{n+1}.
$$
记
$$
S(x)=\sum_{n=0}^{\infty}\frac{x^{n+1}}{n+1}\qquad (|x|<1).
$$
则
$$
S'(x)=\sum_{n=0}^{\infty}x^n=\frac{1}{1-x}.
$$
又因为 $S(0)=0$，故
$$
S(x)=\int_0^x\frac{dt}{1-t}=-\ln(1-x).
$$

取
$$
x=\frac{\sqrt2}{2},
$$
便得
$$
\sum_{n=0}^{\infty}I_n
=-\ln\left(1-\frac{\sqrt2}{2}\right).
$$
而
$$
\frac{1}{1-\frac{\sqrt2}{2}}=2+\sqrt2,
$$
所以
$$
\sum_{n=0}^{\infty}I_n=\ln(2+\sqrt2).
$$

## 第 16 题
### 标准答案

（D）

### 解析

记
$$
A=\left(\alpha_1,\cdots,\alpha_m\right),\qquad
B=\left(\beta_1,\cdots,\beta_m\right).
$$

因为向量组 $\alpha_1,\cdots,\alpha_m$ 线性无关，所以
$$
r(A)=m.
$$

若矩阵 $A$ 与矩阵 $B$ 等价，则等价矩阵秩相同，从而
$$
r(B)=r(A)=m.
$$
而 $B$ 有 $m$ 个列向量，故 $\beta_1,\cdots,\beta_m$ 线性无关。

反过来，若向量组 $\beta_1,\cdots,\beta_m$ 线性无关，则
$$
r(B)=m=r(A).
$$
同型矩阵秩相同当且仅当它们等价，因此 $A$ 与 $B$ 等价。

所以，$\beta_1,\cdots,\beta_m$ 线性无关的充分必要条件是矩阵 $A$ 与矩阵 $B$ 等价，故选 **（D）**。

## 第 17 题
### 标准答案

（A）当且仅当
$$
a\ne -4.
$$

（B）当且仅当
$$
a=-4,\qquad c\ne 3b-1.
$$

（C）当且仅当
$$
a=-4,\qquad c=3b-1.
$$
此时
$$
\beta=k\alpha_1-(b+1+2k)\alpha_2+(2b+1)\alpha_3,\qquad k\in\mathbb{R}.
$$

### 解析

设
$$
x_1\alpha_1+x_2\alpha_2+x_3\alpha_3=\beta,
$$
则系数满足线性方程组
$$
\begin{pmatrix}
a & -2 & -1\\
2 & 1 & 1\\
10 & 5 & 4
\end{pmatrix}
\begin{pmatrix}
x_1\\
x_2\\
x_3
\end{pmatrix}
=
\begin{pmatrix}
1\\
b\\
c
\end{pmatrix}.
$$

先看系数矩阵的行列式：
$$
\left|
\begin{matrix}
a & -2 & -1\\
2 & 1 & 1\\
10 & 5 & 4
\end{matrix}
\right|
=-(a+4).
$$

因此：

1. 当 $a\ne -4$ 时，系数行列式不为零，方程组有唯一解，所以 $\beta$ 可由 $\alpha_1,\alpha_2,\alpha_3$ 唯一表示。

2. 当 $a=-4$ 时，方程组化为
$$
\begin{cases}
-4x_1-2x_2-x_3=1,\\
2x_1+x_2+x_3=b,\\
10x_1+5x_2+4x_3=c.
\end{cases}
$$
由前两式可得
$$
x_3=2b+1,
$$
再由第二式得
$$
2x_1+x_2=-b-1.
$$
把它代入第三式：
$$
10x_1+5x_2+4x_3=5(2x_1+x_2)+4x_3
=-5(b+1)+4(2b+1)=3b-1.
$$
故方程组有解的充要条件是
$$
c=3b-1.
$$

于是：

1. 若 $a=-4$ 且 $c\ne 3b-1$，则方程组无解，$\beta$ 不能由 $\alpha_1,\alpha_2,\alpha_3$ 线性表示。

2. 若 $a=-4$ 且 $c=3b-1$，则方程组有无穷多解。令
$$
x_1=k\in\mathbb{R},
$$
则
$$
x_2=-b-1-2k,\qquad x_3=2b+1.
$$
所以
$$
\beta=k\alpha_1-(b+1+2k)\alpha_2+(2b+1)\alpha_3,\qquad k\in\mathbb{R}.
$$

综上即得三问结论。

## 第 18 题
### 标准答案

当且仅当
$$
a_1a_2\cdots a_n\ne (-1)^n.
$$

### 解析

由题设，
$$
f(x_1,x_2,\cdots,x_n)
=(x_1+a_1x_2)^2+\cdots+(x_n+a_nx_1)^2\ge 0,
$$
因此它总是半正定的。

要使它成为正定二次型，必须且只需对任意非零向量
$$
X=(x_1,x_2,\cdots,x_n)^T\ne 0
$$
都有
$$
f(X)>0.
$$
这等价于
$$
f(X)=0
$$
时只能有零解。

而
$$
f(X)=0
$$
当且仅当每一项平方都为零，即
$$
\begin{cases}
x_1+a_1x_2=0,\\
x_2+a_2x_3=0,\\
\qquad\vdots\\
x_{n-1}+a_{n-1}x_n=0,\\
x_n+a_nx_1=0.
\end{cases}
$$

记其系数矩阵为
$$
B=
\begin{pmatrix}
1 & a_1 & 0 & \cdots & 0\\
0 & 1 & a_2 & \cdots & 0\\
\vdots & \vdots & \vdots & \ddots & \vdots\\
0 & 0 & 0 & \cdots & a_{n-1}\\
a_n & 0 & 0 & \cdots & 1
\end{pmatrix}.
$$
则上述方程组只有零解的充要条件是
$$
\det B\ne 0.
$$

对这个循环矩阵直接展开可得
$$
\det B=1+(-1)^{n+1}a_1a_2\cdots a_n.
$$
因此
$$
\det B\ne 0
\iff 1+(-1)^{n+1}a_1a_2\cdots a_n\ne 0
\iff a_1a_2\cdots a_n\ne (-1)^n.
$$

故二次型 $f(x_1,x_2,\cdots,x_n)$ 为正定二次型的充分必要条件是
$$
a_1a_2\cdots a_n\ne (-1)^n.
$$

## 第 19 题
### 标准答案

（A）
$$
b=EX=e^{\mu+\frac12}.
$$

（B）$\mu$ 的 $0.95$ 置信区间为
$$
(-0.98,\,0.98).
$$

（C）$b$ 的 $0.95$ 置信区间为
$$
\left(e^{-0.48},\,e^{1.48}\right).
$$

### 解析

因为
$$
Y=\ln X\sim N(\mu,1),
$$
所以 $X=e^Y$ 服从对数正态分布。

### （A）求 $b=EX$

设 $Y=\mu+Z$，其中 $Z\sim N(0,1)$，则
$$
b=EX=E(e^Y)=E(e^{\mu+Z})=e^\mu E(e^Z).
$$
而标准正态变量满足
$$
E(e^Z)=e^{1/2},
$$
故
$$
b=e^{\mu+\frac12}.
$$

### （B）求 $\mu$ 的 $0.95$ 置信区间

先把样本取对数：
$$
\ln 0.50+\ln 1.25+\ln 0.80+\ln 2.00
=\ln(0.50\times 1.25\times 0.80\times 2.00)=\ln 1=0.
$$
因此样本均值为
$$
\bar Y=0.
$$

由于 $Y\sim N(\mu,1)$，总体方差已知为 $1$，样本容量 $n=4$，故
$$
\frac{\bar Y-\mu}{1/\sqrt{4}}\sim N(0,1).
$$
取 $z_{0.975}=1.96$，于是
$$
P\left(-1.96\le \frac{\bar Y-\mu}{1/2}\le 1.96\right)=0.95.
$$
从而
$$
P\left(\bar Y-\frac{1.96}{2}\le \mu\le \bar Y+\frac{1.96}{2}\right)=0.95.
$$
代入 $\bar Y=0$，得到 $\mu$ 的 $0.95$ 置信区间为
$$
(-0.98,\,0.98).
$$

### （C）求 $b$ 的 $0.95$ 置信区间

由（A）知
$$
b=e^{\mu+\frac12}.
$$
因为指数函数严格单调递增，所以可将 $\mu$ 的置信区间整体平移 $\frac12$ 后再指数化：
$$
\mu\in(-0.98,0.98)
\iff
\mu+\frac12\in(-0.48,1.48).
$$
于是
$$
b=e^{\mu+\frac12}\in\left(e^{-0.48},e^{1.48}\right).
$$

故 $b$ 的 $0.95$ 置信区间为
$$
\left(e^{-0.48},\,e^{1.48}\right).
$$

## 第 20 题
### 标准答案

随机变量 $X$ 和 $Y$ 不相关的充分必要条件是
$$
P(AB)=P(A)P(B),
$$
即事件 $A$ 与 $B$ 相互独立。

### 解析

先求数学期望：
$$
E(X)=1\cdot P(A)+(-1)\cdot P(A^c)=2P(A)-1,
$$
同理
$$
E(Y)=2P(B)-1.
$$

再求 $E(XY)$。注意到 $XY=1$ 当且仅当 $A,B$ 同时发生或同时不发生，即
$$
\{XY=1\}=AB\cup A^cB^c,
$$
所以
$$
P(XY=1)=P(AB)+P(A^cB^c).
$$
而
$$
P(A^cB^c)=1-P(A\cup B)=1-P(A)-P(B)+P(AB),
$$
故
$$
P(XY=1)=1-P(A)-P(B)+2P(AB).
$$

同理，$XY=-1$ 当且仅当恰有一个事件发生，因此
$$
P(XY=-1)=P(AB^c)+P(A^cB)=P(A)+P(B)-2P(AB).
$$
于是
$$
E(XY)=1\cdot P(XY=1)-1\cdot P(XY=-1)
=4P(AB)-2P(A)-2P(B)+1.
$$

从而协方差为
$$
\operatorname{Cov}(X,Y)=E(XY)-E(X)E(Y).
$$
代入上式得
$$
\operatorname{Cov}(X,Y)
=4P(AB)-2P(A)-2P(B)+1-\bigl(2P(A)-1\bigr)\bigl(2P(B)-1\bigr)
=4\bigl(P(AB)-P(A)P(B)\bigr).
$$

因此
$$
\operatorname{Cov}(X,Y)=0
\iff P(AB)=P(A)P(B).
$$
也就是说，随机变量 $X$ 和 $Y$ 不相关的充分必要条件正是事件 $A$ 与 $B$ 相互独立。
