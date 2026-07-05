# 2012 年数学三答案解析

资料类型：考研数学三答案解析
年份：2012
科目：数学三
整理状态：按答案页图核对后整理；个别题目解析为依据标准答案补写的清晰版。

## 选择题

| 题号 | 答案 |
|---|---|
| 1 | C |
| 2 | A |
| 3 | B |
| 4 | D |
| 5 | C |
| 6 | B |
| 7 | D |
| 8 | B |

## 填空题

| 题号 | 答案 |
|---|---|
| 9 | $e^{-\sqrt2}$ |
| 10 | $\dfrac1e$ |
| 11 | $2\,dx-dy$ |
| 12 | $4\ln 2$ |
| 13 | $-27$ |
| 14 | $\dfrac34$ |

## 解答题

| 题号 | 答案 |
|---|---|
| 15 | $\dfrac1{12}$ |
| 16 | $\dfrac12$ |
| 17 | $C(x,y)=20x+\frac{x^2}{4}+6y+\frac{y^2}{2}+10000$；总产量为 $50$ 时，最优解为 $x=24,\ y=26$；最小总成本为 $11118$；此时甲产品边际成本为 $32$（万元/件）。 |
| 18 | 命题成立 |
| 19 | $$ f(x)=e^x; $$ 曲线唯一拐点为 $$ (0,0). $$ |
| 20 | $\det A=1-a^4$；方程组有无穷多解当且仅当 $a=-1$；此时通解为 $x= \begin{pmatrix} t\\ t-1\\ t\\ t \end{pmatrix},\qquad t\in\mathbb R$ |
| 21 | $$ a=-1; $$ 标准形可取为 $$ 6y_1^2+2y_2^2. $$ |
| 22 | $P\{X=2Y\}=\frac14$ $\operatorname{Cov}(X-Y,\ Y)=-\frac23$ |
| 23 | $f_V(v)= \begin{cases} 2e^{-2v},& v>0,\\ 0,& v\le 0, \end{cases}$；且 $E(U+V)=2$ |

## 详细解析

### 第 1 题

- 答案：C

因式分解得
$$
\frac{x^2+x}{x^2-1}=\frac{x(x+1)}{(x-1)(x+1)}=\frac{x}{x-1}\qquad (x\ne -1).
$$
因此在 $x=1$ 处有竖直渐近线，
$$
x=1.
$$
又
$$
\lim_{x\to\infty}\frac{x}{x-1}=1,
$$
故有水平渐近线
$$
y=1.
$$
点 $x=-1$ 只是可去间断点，不是渐近线。
所以共有 $2$ 条，选 `C`。

### 第 2 题

- 答案：A

在 $x=0$ 时，第一个因子
$$
e^x-1
$$
为零，其余因子为
$$
e^{kx}-k\Big|_{x=0}=1-k\qquad (k=2,\dots,n).
$$
因此求导时只有对第一个因子求导的项不为零：
$$
f'(0)=e^0\prod_{k=2}^n(1-k)=\prod_{k=2}^n(-(k-1)).
$$
故
$$
f'(0)=(-1)^{n-1}(n-1)!.
$$
选 `A`。

### 第 3 题

- 答案：B

给出的积分本身已经是极坐标形式：
$$
\iint_D f(r^2)\,r\,dr\,d\theta,
$$
其中
$$
0\le \theta\le \frac{\pi}{2},\qquad 2\cos\theta\le r\le 2.
$$
换回直角坐标后，雅可比中的 $r$ 已被吸收进积分元，只剩下
$$
\iint_D f(x^2+y^2)\,dxdy.
$$

边界 $r=2$ 对应
$$
x^2+y^2=4,
$$
边界 $r=2\cos\theta$ 对应
$$
x^2+y^2=2x\iff y^2=2x-x^2.
$$
又在第一象限，所以化为
$$
\int_0^2dx\int_{\sqrt{2x-x^2}}^{\sqrt{4-x^2}}f(x^2+y^2)\,dy.
$$
故选 `B`。

### 第 4 题

- 答案：D

当 $n$ 充分大时，
$$
\sin\frac1{n^\alpha}\sim \frac1{n^\alpha},
$$
故第一组级数绝对值项与
$$
\sum \frac{1}{n^{\alpha-1/2}}
$$
同阶。要绝对收敛，需
$$
\alpha-\frac12>1\iff \alpha>\frac32.
$$

第二组是交错 $p$ 级数
$$
\sum (-1)^n n^{-(2-\alpha)}.
$$
它条件收敛要求
$$
0<2-\alpha\le 1,
$$
即
$$
1\le \alpha<2.
$$

综合得
$$
\frac32<\alpha<2.
$$
选 `D`。

### 第 5 题

- 答案：C

注意到
$$
\alpha_3+\alpha_4=
\begin{pmatrix}
1\\-1\\c_3
\end{pmatrix}
+
\begin{pmatrix}
-1\\1\\c_4
\end{pmatrix}
=
\begin{pmatrix}
0\\0\\c_3+c_4
\end{pmatrix},
$$
它与
$$
\alpha_1=\begin{pmatrix}0\\0\\c_1\end{pmatrix}
$$
同方向，因此 $\alpha_1,\alpha_3,\alpha_4$ 必线性相关。

其余三组在前两维上可以构成独立方向，不必必然相关。
故选 `C`。

### 第 6 题

- 答案：B

因为
$$
Q=P
\begin{pmatrix}
1&0&0\\
1&1&0\\
0&0&1
\end{pmatrix},
$$
即只是在特征值为 $1$ 的二维特征子空间内更换了基。

所以在基 $Q$ 下，矩阵 $A$ 的表示仍然是
$$
\operatorname{diag}(1,1,2).
$$
故
$$
Q^{-1}AQ=
\begin{pmatrix}
1&0&0\\
0&1&0\\
0&0&2
\end{pmatrix},
$$
选 `B`。

### 第 7 题

- 答案：D

$(X,Y)$ 在单位正方形 $(0,1)\times(0,1)$ 上均匀分布。
事件
$$
X^2+Y^2\le 1
$$
对应第一象限内的单位圆四分之一。

所求概率就是该区域面积：
$$
P=\frac{\text{四分之一单位圆面积}}{\text{单位正方形面积}}
=\frac{\pi/4}{1}
=\frac{\pi}{4}.
$$
故选 `D`。

### 第 8 题

- 答案：B

因为
$$
X_1-X_2\sim N(0,2\sigma^2),
$$
所以
$$
\frac{X_1-X_2}{\sqrt2\,\sigma}\sim N(0,1).
$$

又
$$
X_3+X_4-2\sim N(0,2\sigma^2),
$$
所以
$$
\frac{X_3+X_4-2}{\sqrt2\,\sigma}\sim N(0,1).
$$
故原统计量可写为
$$
\frac{\dfrac{X_1-X_2}{\sqrt2\,\sigma}}{\left|\dfrac{X_3+X_4-2}{\sqrt2\,\sigma}\right|},
$$
这是标准正态变量除以独立标准正态变量绝对值，服从 $t(1)$ 分布。
故选 `B`。

### 第 9 题

- 答案：$e^{-\sqrt2}$

设极限为 $L$，取对数：
$$
\ln L=\lim_{x\to\pi/4}\frac{\ln(\tan x)}{\cos x-\sin x}.
$$
这是 $0/0$ 型，应用洛必达法则：
$$
\ln L=
\lim_{x\to\pi/4}
\frac{\dfrac{\sec^2x}{\tan x}}{-\sin x-\cos x}.
$$
又
$$
\frac{\sec^2x}{\tan x}=\frac{1}{\sin x\cos x},
$$
在 $x=\pi/4$ 处取值为 $2$，而
$$
-\sin\frac\pi4-\cos\frac\pi4=-\sqrt2.
$$
故
$$
\ln L=-\sqrt2,
$$
于是
$$
L=e^{-\sqrt2}.
$$

### 第 10 题

- 答案：$\dfrac1e$

先算
$$
f(e)=\ln\sqrt e=\frac12.
$$
由于 $\frac12<1$，所以
$$
f(f(e))=f\left(\frac12\right)=2\cdot\frac12-1=0.
$$

复合函数求导：
$$
y'=f'(f(x))\cdot f'(x).
$$
其中
$$
f'(e)=\frac{d}{dx}\left(\frac12\ln x\right)\Big|_{x=e}=\frac{1}{2e},
$$
且
$$
f'\left(\frac12\right)=2.
$$
故
$$
y'(e)=2\cdot\frac{1}{2e}=\frac1e.
$$

### 第 11 题

- 答案：$2\,dx-dy$

由题设极限为零可知
$$
f(x,y)=2x-y+2+o\!\left(\sqrt{x^2+(y-1)^2}\right)\qquad ((x,y)\to(0,1)).
$$
这正是可微展开式，因此
$$
f_x(0,1)=2,\qquad f_y(0,1)=-1.
$$
故
$$
dz\big|_{(0,1)}=f_x(0,1)\,dx+f_y(0,1)\,dy=2\,dx-dy.
$$

### 第 12 题

- 答案：$4\ln 2$

三条曲线围成的区域可按 $x$ 分段。

与双曲线的交点分别为：
$$
y=4x \text{ 与 } y=\frac4x \Rightarrow x=1;
$$
$$
y=x \text{ 与 } y=\frac4x \Rightarrow x=2.
$$

所以面积为
$$
S=\int_0^1(4x-x)\,dx+\int_1^2\left(\frac4x-x\right)\,dx.
$$
计算得
$$
S=\frac32+\left(4\ln2-\frac32\right)=4\ln2.
$$

### 第 13 题

- 答案：$-27$

交换两行会使行列式变号，因此
$$
|B|=-|A|=-3.
$$
又因为 $A$ 为三阶矩阵，
$$
|A^*|=|A|^{3-1}=|A|^2=9.
$$
所以
$$
|BA^*|=|B|\cdot|A^*|=(-3)\cdot 9=-27.
$$

### 第 14 题

- 答案：$\dfrac34$

因为 $A$ 与 $C$ 互不相容，所以
$$
AB\subset A
$$
也与 $C$ 互不相容，即
$$
P(AB\cap \overline C)=P(AB)=\frac12.
$$
又
$$
P(\overline C)=1-\frac13=\frac23.
$$
因此
$$
P(AB\mid \overline C)=\frac{P(AB\cap \overline C)}{P(\overline C)}
=\frac{1/2}{2/3}=\frac34.
$$

### 第 15 题

- 答案：$\dfrac1{12}$

利用展开式
$$
2-2\cos x=x^2-\frac{x^4}{12}+o(x^4).
$$
于是
$$
e^{2-2\cos x}
=e^{x^2-\frac{x^4}{12}+o(x^4)}
=e^{x^2}\cdot e^{-\frac{x^4}{12}+o(x^4)}
=e^{x^2}\left(1-\frac{x^4}{12}+o(x^4)\right).
$$
故分子
$$
e^{x^2}-e^{2-2\cos x}
=e^{x^2}\left[\frac{x^4}{12}+o(x^4)\right].
$$
因此
$$
\lim_{x\to 0}\frac{e^{x^2}-e^{2-2\cos x}}{x^4}
=\lim_{x\to 0}e^{x^2}\left(\frac1{12}+o(1)\right)
=\frac1{12}.
$$

### 第 16 题

- 答案：$\dfrac12$

由边界关系可知区域可表示为
$$
0\le x\le 1,\qquad \sqrt x\le y\le \frac1{\sqrt x}.
$$
因此
$$
\iint_D e^x y\,dxdy
=\int_0^1 e^x\left(\int_{\sqrt x}^{1/\sqrt x}y\,dy\right)dx.
$$
内层积分为
$$
\int_{\sqrt x}^{1/\sqrt x}y\,dy
=\frac12\left(\frac1x-x\right).
$$
所以
$$
\iint_D e^x y\,dxdy
=\frac12\int_0^1 e^x(1-x^2)\,dx.
$$
注意到
$$
\frac{d}{dx}\Bigl[e^x(-x^2+2x-1)\Bigr]=e^x(1-x^2),
$$
故
$$
\int_0^1 e^x(1-x^2)\,dx
=e^x(-x^2+2x-1)\Big|_0^1=1.
$$
因此原积分为
$$
\frac12.
$$

### 第 17 题

- 答案：$$
C(x,y)=20x+\frac{x^2}{4}+6y+\frac{y^2}{2}+10000;
$$
总产量为 $50$ 时，最优解为
$$
x=24,\ y=26,
$$
最小总成本为
$$
11118;
$$
此时甲产品边际成本为 $32$（万元/件）。

由边际成本定义，
$$
\frac{\partial C}{\partial x}=20+\frac{x}{2},\qquad
\frac{\partial C}{\partial y}=6+y.
$$
先对 $x,y$ 分别积分，得
$$
C(x,y)=20x+\frac{x^2}{4}+6y+\frac{y^2}{2}+K.
$$
由固定成本 $C(0,0)=10000$，可得 $K=10000$，所以
$$
C(x,y)=20x+\frac{x^2}{4}+6y+\frac{y^2}{2}+10000.
$$

当总产量为 $50$ 件时，约束为
$$
x+y=50,\qquad y=50-x.
$$
代入成本函数：
$$
\phi(x)=20x+\frac{x^2}{4}+6(50-x)+\frac{(50-x)^2}{2}+10000
=\frac34x^2-36x+11550.
$$
令
$$
\phi'(x)=\frac32x-36=0,
$$
得
$$
x=24,\qquad y=26.
$$
此时最小总成本
$$
C(24,26)=11118.
$$

最优点处甲产品边际成本为
$$
\frac{\partial C}{\partial x}(24,26)=20+\frac{24}{2}=32.
$$
其经济意义是：在总产量为 $50$ 件且成本最小时，甲产品产量若再增加 $1$ 件，成本约增加 $32$ 万元。

### 第 18 题

- 答案：命题成立

设
$$
F(x)=x\ln\frac{1+x}{1-x}+\cos x-1-\frac{x^2}{2}.
$$
则
$$
F(0)=0.
$$
对其求导：
$$
F'(x)=\ln\frac{1+x}{1-x}+\frac{2x}{1-x^2}-\sin x-x.
$$
进一步整理可知
$$
F'(x)=\left(\ln\frac{1+x}{1-x}-2x\right)+\left(\frac{2x}{1-x^2}-x\right)+(x-\sin x).
$$

在 $(-1,1)$ 上有经典不等式
$$
\ln\frac{1+x}{1-x}\ge 2x,\qquad x-\sin x\ge 0,
$$
且
$$
\frac{2x}{1-x^2}-x=\frac{x(1+x^2)}{1-x^2}
$$
与 $x$ 同号。
综合可得 $F'(x)$ 与 $x$ 同号，因此 $x=0$ 是 $F$ 的最小点。

于是对一切 $-1<x<1$，有
$$
F(x)\ge F(0)=0,
$$
即
$$
x\ln\frac{1+x}{1-x}+\cos x\ge 1+\frac{x^2}{2}.
$$

### 第 19 题

- 答案：$$
f(x)=e^x;
$$
曲线唯一拐点为
$$
(0,0).
$$

将两式相减，得
$$
f'(x)-3f(x)=-2e^x.
$$
解此一阶线性微分方程：
$$
f(x)=e^x+Ce^{3x}.
$$
代回
$$
f''(x)+f(x)=2e^x
$$
可得 $C=0$，故
$$
f(x)=e^x.
$$

于是曲线方程为
$$
y=e^{x^2}\int_0^x e^{-t^2}\,dt.
$$
记
$$
I(x)=\int_0^x e^{-t^2}\,dt.
$$
则
$$
y'=2xe^{x^2}I(x)+1.
$$
再求导得
$$
y''=2(1+2x^2)e^{x^2}I(x)+2x.
$$
由于 $I(x)$ 与 $x$ 同号，所以当 $x>0$ 时，$y''>0$；当 $x<0$ 时，$y''<0$。
故曲线在 $x=0$ 两侧凹凸性相反，且
$$
y(0)=0.
$$
因此唯一拐点是
$$
(0,0).
$$

### 第 20 题

- 答案：$$
|A|=1-a^4;
$$
方程组有无穷多解当且仅当
$$
a=-1,
$$
此时通解为
$$
x=
\begin{pmatrix}
t\\
t-1\\
t\\
t
\end{pmatrix},\qquad t\in\mathbb R.
$$

矩阵 $A$ 只有两类非零置换项：恒等置换给出 $1$，四循环 $(1\,2\,3\,4)$ 给出 $-a^4$，故
$$
|A|=1-a^4.
$$

要使方程组有无穷多解，必须先有
$$
|A|=0\iff a^4=1\iff a=\pm 1.
$$

分别讨论：

当 $a=1$ 时，方程组为
$$
\begin{cases}
x_1+x_2=1,\\
x_2+x_3=-1,\\
x_3+x_4=0,\\
x_1+x_4=0.
\end{cases}
$$
由后两式得 $x_4=-x_3,\ x_1=x_3$，再代入第一式与第二式矛盾，所以无解。

当 $a=-1$ 时，方程组化为
$$
\begin{cases}
x_1-x_2=1,\\
x_2-x_3=-1,\\
x_3-x_4=0,\\
-x_1+x_4=0.
\end{cases}
$$
由后两式得
$$
x_4=x_1,\qquad x_3=x_4=x_1.
$$
再由第二式得
$$
x_2=x_1-1.
$$
令 $x_1=t$，则
$$
x=
\begin{pmatrix}
t\\
t-1\\
t\\
t
\end{pmatrix},\qquad t\in\mathbb R.
$$
故方程组有无穷多解当且仅当 $a=-1$。

### 第 21 题

- 答案：$$
a=-1;
$$
标准形可取为
$$
6y_1^2+2y_2^2.
$$

因为
$$
r(A^TA)=r(A)=2,
$$
故矩阵 $A$ 的列向量线性相关。设其三列分别为
$$
c_1=\begin{pmatrix}1\\0\\-1\\0\end{pmatrix},\quad
c_2=\begin{pmatrix}0\\1\\0\\a\end{pmatrix},\quad
c_3=\begin{pmatrix}1\\1\\a\\-1\end{pmatrix}.
$$
要使秩为 $2$，必须有 $c_3$ 可由 $c_1,c_2$ 线性表示。观察到若
$$
a=-1,
$$
则
$$
c_3=c_1+c_2.
$$
因此 $a=-1$。

此时
$$
A^TA=
\begin{pmatrix}
2&0&2\\
0&2&2\\
2&2&4
\end{pmatrix}.
$$
求其特征值与特征向量，可得特征值为
$$
6,\quad 2,\quad 0,
$$
对应一组两两正交的特征向量可取
$$
v_1=(1,1,2)^T,\qquad
v_2=(1,-1,0)^T,\qquad
v_3=(-1,-1,1)^T.
$$
将其单位化：
$$
\eta_1=\frac{1}{\sqrt6}(1,1,2)^T,\quad
\eta_2=\frac{1}{\sqrt2}(1,-1,0)^T,\quad
\eta_3=\frac{1}{\sqrt3}(-1,-1,1)^T.
$$
取正交矩阵
$$
Q=(\eta_1,\eta_2,\eta_3),
$$
则
$$
Q^T(A^TA)Q=\operatorname{diag}(6,2,0).
$$
故在正交变换 $x=Qy$ 下，
$$
f=6y_1^2+2y_2^2.
$$

### 第 22 题

- 答案：$$
P\{X=2Y\}=\frac14;
$$
$$
\operatorname{Cov}(X-Y,\ Y)=-\frac23.
$$

由表可知事件 $X=2Y$ 只在 $(X,Y)=(0,0)$ 处发生，因此
$$
P\{X=2Y\}=P(X=0,Y=0)=\frac14.
$$

再求协方差。先求边缘分布：
$$
P(Y=0)=P(Y=1)=P(Y=2)=\frac13,
$$
故
$$
EY=1,\qquad EY^2=\frac{0^2+1^2+2^2}{3}=\frac53,
$$
所以
$$
DY=EY^2-(EY)^2=\frac53-1=\frac23.
$$

又
$$
EX=0\cdot \frac12+1\cdot\frac13+2\cdot\frac16=\frac23.
$$
并且
$$
EXY=1\cdot1\cdot\frac13+2\cdot2\cdot\frac1{12}=\frac13+\frac13=\frac23.
$$
于是
$$
\operatorname{Cov}(X,Y)=EXY-EX\cdot EY=\frac23-\frac23\cdot 1=0.
$$
故
$$
\operatorname{Cov}(X-Y,Y)=\operatorname{Cov}(X,Y)-\operatorname{Cov}(Y,Y)=0-DY=-\frac23.
$$

### 第 23 题

- 答案：$$
f_V(v)=
\begin{cases}
2e^{-2v},& v>0,\\
0,& v\le 0,
\end{cases}
$$
且
$$
E(U+V)=2.
$$

因为
$$
V=\min(X,Y),
$$
所以对 $v>0$，
$$
P(V>v)=P(X>v,\ Y>v)=e^{-v}\cdot e^{-v}=e^{-2v}.
$$
因此分布函数为
$$
F_V(v)=1-e^{-2v}\qquad (v>0),
$$
从而密度
$$
f_V(v)=F_V'(v)=2e^{-2v},\qquad v>0.
$$

又因为
$$
U+V=X+Y,
$$
故
$$
E(U+V)=E(X)+E(Y)=1+1=2.
$$
