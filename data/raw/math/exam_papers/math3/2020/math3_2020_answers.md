# 2020 数学三答案解析

资料类型：考研数学三答案解析
年份：2020
科目：数学三
整理状态：依据答案页和题面人工补写整理。


## 选择题

| 题号 | 答案 |
|---|---|
| 1 | B |
| 2 | C |
| 3 | A |
| 4 | B |
| 5 | C |
| 6 | D |
| 7 | D |
| 8 | C |

## 填空题

| 题号 | 答案 |
|---|---|
| 9 | $(\pi-1)\,dx-dy$ |
| 10 | $y=x-1$ |
| 11 | $8$ |
| 12 | $\pi\ln2-\dfrac{\pi}{3}$ |
| 13 | $a^2(a^2-4)$ |
| 14 | $\dfrac87$ |

## 解答题

| 题号 | 答案 |
|---|---|
| 15 | $a=1,\ b=-\dfrac e2$ |
| 16 | 在 $\left(\frac16,\frac1{12}\right)$ 处取极小值 $-\frac1{216}$；原点不是极值点。 |
| 17 | $f(x)=e^{-x}\cos 2x$ $\sum_{n=1}^{\infty}a_n=\frac{1}{5(e^\pi-1)}$ |
| 18 | $\dfrac{3\pi^2}{128}$ |
| 19 | 命题成立 |
| 20 | $a=4,\quad b=1$；可取 $Q= \begin{pmatrix} 0&1\\ -1&0 \end{pmatrix}$ |
| 21 | $P^{-1}AP= \begin{pmatrix} 0&6\\ 1&-1 \end{pmatrix}$ $A$ 相似于对角矩阵。 |
| 22 | 联合分布为 $\begin{array}{ccc} Z_1\backslash Z_2 & 0 & 1\\ \hline 0 & \dfrac14 & \dfrac12\\ 1 & 0 & \dfrac14 \end{array}$；相关系数 $\rho_{Z_1,Z_2}=\dfrac13$。 |
| 23 | $P(T>t)=e^{-(t/\theta)^m}$ $P(T>s+t\mid T>s)=e^{-((s+t)^m-s^m)/\theta^m}$ $\hat\theta=\left(\frac1n\sum_{i=1}^n t_i^m\right)^{1/m}$ |

## 详细解析

### 第 1 题

- 标准答案：B

由拉格朗日中值定理，
$$
\sin f(x)-\sin a=\cos\xi\,[f(x)-a],
$$
其中 $\xi$ 介于 $f(x)$ 与 $a$ 之间。

因此
$$
\frac{\sin f(x)-\sin a}{x-a}
=\cos\xi\cdot \frac{f(x)-a}{x-a}.
$$
当 $x\to a$ 时，$\xi\to a$，故
$$
\lim_{x\to a}\frac{\sin f(x)-\sin a}{x-a}
=\cos a\cdot b=b\cos a.
$$
故选 **B**。

### 第 2 题

- 标准答案：C

可能的间断点来自 $x=-1,0,1,2$。

- 当 $x=-1$ 时，$\ln|1+x|$ 发散，所以是第二类间断点；
- 当 $x=0$ 时，利用
  $$
  \ln(1+x)\sim x,\qquad e^x-1\sim x,
  $$
  可知极限存在，因此是可去间断点；
- 当 $x=1$ 时，$e^{1/(x-1)}$ 发散，为第二类间断点；
- 当 $x=2$ 时，分母为 0 而分子有限非零，也是第二类间断点。

故第二类间断点共有 3 个，选 **C**。

### 第 3 题

- 标准答案：A

因为 $f$ 为奇函数，所以 $f'$ 为偶函数；又 $\cos f(t)$ 也是偶函数。
于是
$$
\cos f(t)+f'(t)
$$
是偶函数。

偶函数从 0 到 $x$ 的积分是奇函数，因此
$$
\int_0^x[\cos f(t)+f'(t)]\,dt
$$
是奇函数。

故选 **A**。

### 第 4 题

- 标准答案：B

已知级数
$$
\sum n a_n (x-2)^n
$$
的收敛半径为
$$
R=\frac{6-(-2)}2=4.
$$

因此关于变量 $u=(x+1)^2$ 的级数
$$
\sum a_n u^n
$$
的收敛半径为 4，即
$$
|(x+1)^2|<4.
$$
所以
$$
|x+1|<2\iff -3<x<1.
$$
故选 **B**。

### 第 5 题

- 标准答案：C

因为 $A$ 不可逆且 $A_{12}\ne0$，可知 $r(A)=3$，并且去掉第 1 行、第 2 列后的 3 阶子式非零。
这意味着由第 1、3、4 列构成的三个列向量线性无关。

而
$$
A^*A=AA^*=0
$$
且 $r(A^*)=1$，所以齐次方程组 $A^*x=0$ 的解空间维数为 3，它正由 $A$ 的三个线性无关列向量张成。

故通解可写为
$$
x=k_1\alpha_1+k_2\alpha_3+k_3\alpha_4.
$$
选 **C**。

### 第 6 题

- 标准答案：D

矩阵 $P$ 的列向量必须依次是对应于特征值 $1,-1,1$ 的特征向量。

- $\alpha_1+\alpha_2$ 仍是特征值 1 的特征向量；
- $-\alpha_3$ 是特征值 $-1$ 的特征向量；
- $\alpha_2$ 是特征值 1 的特征向量。

且这三列线性无关，因此
$$
P=(\alpha_1+\alpha_2,-\alpha_3,\alpha_2)
$$
满足要求。

故选 **D**。

### 第 7 题

- 标准答案：D

恰有一个事件发生的概率为
$$
P(A\cup B\cup C)-P(\text{至少两个发生}).
$$
由于 $P(AB)=0$，故 $P(ABC)=0$。

直接按“只发生 $A$、只发生 $B$、只发生 $C$”计算：
$$
P(\text{只发生 }A)=P(A)-P(AC)=\frac14-\frac1{12}=\frac16,
$$
$$
P(\text{只发生 }B)=P(B)-P(BC)=\frac16,
$$
$$
P(\text{只发生 }C)=P(C)-P(AC)-P(BC)=\frac14-\frac1{12}-\frac1{12}=\frac1{12}.
$$
所以
$$
\frac16+\frac16+\frac1{12}=\frac5{12}.
$$
故选 **D**。

### 第 8 题

- 标准答案：C

由题意
$$
D(X)=1,\qquad D(Y)=4,\qquad \rho=-\frac12.
$$
所以
$$
\operatorname{Cov}(X,Y)=\rho\sqrt{D(X)}\sqrt{D(Y)}=-1.
$$

计算
$$
D(X+Y)=1+4+2(-1)=3,
$$
$$
D(X-Y)=1+4-2(-1)=7.
$$
因此
$$
\frac{\sqrt3}{3}(X+Y)
$$
的方差为 1，且其与 $X$ 的协方差
$$
\operatorname{Cov}\!\left(X,\frac{\sqrt3}{3}(X+Y)\right)
=\frac{\sqrt3}{3}(D(X)+\operatorname{Cov}(X,Y))
=0.
$$
二维正态下“不相关即独立”，故选 **C**。

### 第 9 题

- 标准答案：$(\pi-1)\,dx-dy$

设
$$
u=xy+\sin(x+y),\qquad z=\arctan u.
$$
则
$$
dz=\frac1{1+u^2}\,du.
$$
在 $(0,\pi)$ 处，
$$
u=0\cdot\pi+\sin\pi=0,
$$
所以
$$
dz=du.
$$

又
$$
u_x=y+\cos(x+y),\qquad u_y=x+\cos(x+y).
$$
代入 $(0,\pi)$ 得
$$
u_x=\pi-1,\qquad u_y=-1.
$$
故
$$
dz=(\pi-1)\,dx-dy.
$$

### 第 10 题

- 标准答案：$y=x-1$

对方程两边关于 $x$ 求导：
$$
1+y'+e^{2xy}\cdot 2(y+xy')=0.
$$
在点 $(0,-1)$ 处，$e^{2xy}=1$，于是
$$
1+y'+2(-1+0\cdot y')=0
\iff y'=1.
$$
所以切线方程为
$$
y+1=1(x-0),
$$
即
$$
y=x-1.
$$

### 第 11 题

- 标准答案：$8$

由
$$
Q=\frac{800}{P+3}-2
$$
解得
$$
P=\frac{800}{Q+2}-3.
$$

利润函数为
$$
L(Q)=PQ-C(Q)
=\left(\frac{800}{Q+2}-3\right)Q-(100+13Q)
=\frac{1600}{Q+2}-16Q+700.
$$
求导：
$$
L'(Q)=-\frac{1600}{(Q+2)^2}+16.
$$
令 $L'(Q)=0$，得
$$
\frac{1600}{(Q+2)^2}=16
\iff (Q+2)^2=100
\iff Q=8
$$
（舍去负值）。
故最大利润时产量为 8。

### 第 12 题

- 标准答案：$\pi\ln2-\dfrac{\pi}{3}$

绕 $y$ 轴旋转，采用壳层法：
$$
V=2\pi\iint_D x\,d\sigma
=2\pi\int_0^1 x\left(\frac1{1+x^2}-\frac x2\right)\,dx.
$$
所以
$$
V=2\pi\left(\int_0^1\frac{x}{1+x^2}\,dx-\frac12\int_0^1x^2\,dx\right).
$$
计算得
$$
\int_0^1\frac{x}{1+x^2}\,dx=\frac12\ln2,\qquad
\frac12\int_0^1x^2\,dx=\frac16.
$$
因此
$$
V=2\pi\left(\frac12\ln2-\frac16\right)=\pi\ln2-\frac{\pi}{3}.
$$

### 第 13 题

- 标准答案：$a^2(a^2-4)$

对行列式作初等变换化简，例如将第 2 行加到第 1 行、第 3 行加到第 4 行，再对列作相应整理，可化为上三角块形式。

最终得到
$$
\begin{vmatrix}
a&2\\
2&a
\end{vmatrix}
$$
与两个对角元 $a$ 的乘积，因此
$$
|A|=a^2(a^2-4).
$$

### 第 14 题

- 标准答案：$\dfrac87$

按模 3 分类：

- 当 $Y=1$ 时，$X=1,4,7,\ldots$，
  $$
  P(Y=1)=\frac12+\frac1{2^4}+\frac1{2^7}+\cdots=\frac{1/2}{1-1/8}=\frac47;
  $$
- 当 $Y=2$ 时，$X=2,5,8,\ldots$，
  $$
  P(Y=2)=\frac14+\frac1{2^5}+\frac1{2^8}+\cdots=\frac{1/4}{1-1/8}=\frac27;
  $$
- 当 $Y=0$ 时，
  $$
  P(Y=0)=1-\frac47-\frac27=\frac17.
  $$

所以
$$
E(Y)=0\cdot\frac17+1\cdot\frac47+2\cdot\frac27=\frac87.
$$

### 第 15 题

- 标准答案：$a=1,\ b=-\dfrac e2$

写成
$$
\left(1+\frac1n\right)^n-e
=e\left[e^{n\ln(1+1/n)-1}-1\right].
$$
由于
$$
\ln\left(1+\frac1n\right)=\frac1n-\frac1{2n^2}+o(n^{-2}),
$$
所以
$$
n\ln\left(1+\frac1n\right)-1=-\frac1{2n}+o(n^{-1}).
$$
于是
$$
e^{n\ln(1+1/n)-1}-1\sim -\frac1{2n}.
$$
故
$$
\left(1+\frac1n\right)^n-e\sim -\frac{e}{2n}.
$$

与
$$
\frac{b}{n^a}
$$
等价，故
$$
a=1,\qquad b=-\frac e2.
$$

### 第 16 题

- 标准答案：在 $\left(\frac16,\frac1{12}\right)$ 处取极小值 $-\frac1{216}$；原点不是极值点。

求偏导：
$$
f_x=3x^2-y,\qquad f_y=24y^2-x.
$$
令其为 0，得驻点
$$
(0,0),\qquad \left(\frac16,\frac1{12}\right).
$$

二阶偏导为
$$
f_{xx}=6x,\qquad f_{xy}=-1,\qquad f_{yy}=48y.
$$
判别式
$$
\Delta=f_{xx}f_{yy}-f_{xy}^2=288xy-1.
$$

- 在 $(0,0)$ 处，
  $$
  \Delta=-1<0,
  $$
  不是极值点；
- 在 $\left(\frac16,\frac1{12}\right)$ 处，
  $$
  \Delta=3>0,\qquad f_{xx}=1>0,
  $$
  故为极小值点。

其极小值为
$$
f\left(\frac16,\frac1{12}\right)=\frac1{216}+\frac1{216}-\frac1{72}=-\frac1{216}.
$$

### 第 17 题

- 标准答案：$$
f(x)=e^{-x}\cos 2x;
$$

$$
\sum_{n=1}^{\infty}a_n=\frac{1}{5(e^\pi-1)}.
$$

特征方程
$$
\lambda^2+2\lambda+5=0
$$
有根
$$
\lambda=-1\pm 2i.
$$
因此
$$
f(x)=e^{-x}(C_1\cos2x+C_2\sin2x).
$$
由条件
$$
f(0)=1,\qquad f'(0)=-1
$$
得
$$
C_1=1,\qquad C_2=0.
$$
所以
$$
f(x)=e^{-x}\cos2x.
$$

再求积分：
$$
\int e^{-x}\cos2x\,dx=\frac15(2\sin2x-\cos2x)e^{-x}+C.
$$
因此
$$
a_n=\left[\frac15(2\sin2x-\cos2x)e^{-x}\right]_{n\pi}^{+\infty}
=\frac15e^{-n\pi}.
$$
故
$$
\sum_{n=1}^{\infty}a_n
=\frac15\sum_{n=1}^{\infty}e^{-n\pi}
=\frac15\cdot \frac{e^{-\pi}}{1-e^{-\pi}}
=\frac{1}{5(e^\pi-1)}.
$$

### 第 18 题

- 标准答案：$\dfrac{3\pi^2}{128}$

设
$$
A=\iint_D f(x,y)\,dx\,dy.
$$
则
$$
f(x,y)=y\sqrt{1-x^2}+Ax.
$$

对两边在 $D$ 上积分：
$$
A=\iint_D y\sqrt{1-x^2}\,dx\,dy+A\iint_D x\,dx\,dy.
$$
由于区域关于 $y$ 轴对称，
$$
\iint_D x\,dx\,dy=0,
$$
所以
$$
A=\iint_D y\sqrt{1-x^2}\,dx\,dy.
$$
计算得
$$
A=2\int_0^1\sqrt{1-x^2}\left(\int_0^{\sqrt{1-x^2}}y\,dy\right)dx
=\int_0^1(1-x^2)^{3/2}\,dx
=\frac{3\pi}{16}.
$$

于是
$$
f(x,y)=y\sqrt{1-x^2}+\frac{3\pi}{16}x.
$$
故
$$
\iint_D x f(x,y)\,dx\,dy
=\iint_D xy\sqrt{1-x^2}\,dx\,dy+\frac{3\pi}{16}\iint_D x^2\,dx\,dy.
$$
第一项由于关于 $y$ 轴奇对称为 0。

因此
$$
\iint_D x f(x,y)\,dx\,dy
=\frac{3\pi}{16}\iint_D x^2\,dx\,dy.
$$
用极坐标计算
$$
\iint_D x^2\,dx\,dy
=\int_0^\pi\int_0^1 r^2\cos^2\theta\cdot r\,dr\,d\theta
=\frac14\cdot \frac\pi2=\frac{\pi}{8}.
$$
所以结果为
$$
\frac{3\pi}{16}\cdot \frac{\pi}{8}=\frac{3\pi^2}{128}.
$$

### 第 19 题

- 标准答案：命题成立

1. 取 $c\in[0,2]$ 使
$$
|f(c)|=M.
$$

若 $c\in(0,1]$，由拉格朗日中值定理，存在 $\xi\in(0,c)$ 使
$$
f'(\xi)=\frac{f(c)-f(0)}{c}=\frac{f(c)}{c}.
$$
于是
$$
|f'(\xi)|=\frac{|f(c)|}{c}=\frac{M}{c}\ge M.
$$

若 $c\in(1,2)$，同理存在 $\xi\in(c,2)$ 使
$$
f'(\xi)=\frac{f(2)-f(c)}{2-c}=-\frac{f(c)}{2-c},
$$
从而
$$
|f'(\xi)|=\frac{M}{2-c}\ge M.
$$
故命题 1 成立。

2. 若对任意 $x\in(0,2)$ 有 $|f'(x)|\le M$。仍取 $c$ 使 $|f(c)|=M$。

- 若 $c\in[0,1)$，则
  $$
  M=|f(c)-f(0)|=|f'(\xi)|c\le Mc.
  $$
  因为 $c<1$，只可能 $M=0$；
- 若 $c\in(1,2]$，同理也得 $M=0$；
- 若 $c=1$ 且 $M>0$，则
  $$
  M=|f(1)|=\left|\int_0^1 f'(x)\,dx\right|
  \le \int_0^1|f'(x)|\,dx < M,
  $$
  矛盾。

故必有
$$
M=0.
$$

### 第 20 题

- 标准答案：$$
a=4,\quad b=1;
$$

可取
$$
Q=
\begin{pmatrix}
0&1\\
-1&0
\end{pmatrix}.
$$

二次型 $f,g$ 对应矩阵分别为
$$
A=
\begin{pmatrix}
1&-2\\
-2&4
\end{pmatrix},\qquad
B=
\begin{pmatrix}
a&2\\
2&b
\end{pmatrix}.
$$
正交合同保持迹和行列式，所以
$$
a+b=5,\qquad ab-4=0.
$$
解得
$$
a,b=4,1.
$$
又因 $a\ge b$，故
$$
a=4,\quad b=1.
$$

于是
$$
g(y_1,y_2)=4y_1^2+4y_1y_2+y_2^2=(2y_1+y_2)^2.
$$
取变换
$$
x_1=y_2,\qquad x_2=-y_1,
$$
即
$$
\binom{x_1}{x_2}
=
\begin{pmatrix}
0&1\\
-1&0
\end{pmatrix}
\binom{y_1}{y_2}.
$$
代入可验证恰化为所给二次型。

### 第 21 题

- 标准答案：$$
P^{-1}AP=
\begin{pmatrix}
0&6\\
1&-1
\end{pmatrix};
$$

$A$ 相似于对角矩阵。

1. 若 $P$ 不可逆，则 $\alpha$ 与 $A\alpha$ 线性相关，即存在常数 $k$ 使
$$
A\alpha=k\alpha.
$$
这说明 $\alpha$ 是 $A$ 的特征向量，与题设矛盾。因此 $P$ 可逆。

2. 有
$$
A^2\alpha=6\alpha-A\alpha.
$$
于是
$$
AP=A(\alpha,A\alpha)=(A\alpha,A^2\alpha)=(A\alpha,6\alpha-A\alpha).
$$
写成以 $P$ 为基底的坐标即
$$
AP=(\alpha,A\alpha)
\begin{pmatrix}
0&6\\
1&-1
\end{pmatrix}.
$$
故
$$
P^{-1}AP=
\begin{pmatrix}
0&6\\
1&-1
\end{pmatrix}.
$$

记
$$
B=
\begin{pmatrix}
0&6\\
1&-1
\end{pmatrix},
$$
则其特征多项式为
$$
|\lambda E-B|=\lambda^2+\lambda-6=(\lambda-2)(\lambda+3).
$$
有两个不同特征值，因此 $B$ 可对角化，从而 $A$ 也相似于对角矩阵。

### 第 22 题

- 标准答案：分布为

| $Z_1\backslash Z_2$ | 0 | 1 |
|---|---:|---:|
| 0 | $\dfrac14$ | $\dfrac12$ |
| 1 | $0$ | $\dfrac14$ |

相关系数
$$
\rho_{Z_1,Z_2}=\frac13.
$$

区域 $D$ 是上半圆盘，面积为
$$
|D|=\frac{\pi}{2}.
$$

直线 $x-y=0$ 与 $x+y=0$ 把该半圆分成若干部分。

- 事件 $Z_1=1$ 对应区域 $x>y$，其面积占上半圆的 $\dfrac14$，故
  $$
  P(Z_1=1)=\frac14,\qquad P(Z_1=0)=\frac34;
  $$
- 事件 $Z_2=1$ 对应区域 $x+y>0$，其面积占上半圆的 $\dfrac34$，故
  $$
  P(Z_2=1)=\frac34,\qquad P(Z_2=0)=\frac14.
  $$

又
$$
P(Z_1=1,Z_2=1)=\frac14,
$$
而 $Z_1=1$ 时必有 $Z_2=1$，所以
$$
P(Z_1=1,Z_2=0)=0.
$$
由边际分布得
$$
P(Z_1=0,Z_2=1)=\frac12,\qquad P(Z_1=0,Z_2=0)=\frac14.
$$

因此分布表如答案所示。

再计算：
$$
E(Z_1)=\frac14,\qquad E(Z_2)=\frac34,
$$
$$
D(Z_1)=\frac14\cdot\frac34=\frac3{16},\qquad
D(Z_2)=\frac34\cdot\frac14=\frac3{16}.
$$
且
$$
E(Z_1Z_2)=P(Z_1=1,Z_2=1)=\frac14.
$$
故
$$
\operatorname{Cov}(Z_1,Z_2)=\frac14-\frac14\cdot\frac34=\frac1{16}.
$$
所以
$$
\rho_{Z_1,Z_2}
=\frac{1/16}{\sqrt{3/16}\sqrt{3/16}}
=\frac13.
$$

### 第 23 题

- 标准答案：$$
P(T>t)=e^{-(t/\theta)^m},
$$

$$
P(T>s+t\mid T>s)=e^{-((s+t)^m-s^m)/\theta^m},
$$

$$
\hat\theta=\left(\frac1n\sum_{i=1}^n t_i^m\right)^{1/m}.
$$

由分布函数得生存函数
$$
P(T>t)=1-F(t)=e^{-(t/\theta)^m}\qquad (t>0).
$$

因此
$$
P(T>s+t\mid T>s)
=\frac{P(T>s+t)}{P(T>s)}
=\frac{e^{-((s+t)/\theta)^m}}{e^{-(s/\theta)^m}}
=e^{-((s+t)^m-s^m)/\theta^m}.
$$

再求密度函数：
$$
f(t)=F'(t)=\frac{m}{\theta}\left(\frac{t}{\theta}\right)^{m-1}e^{-(t/\theta)^m},\qquad t>0.
$$

样本似然函数为
$$
L(\theta)=\prod_{i=1}^n \frac{m}{\theta}\left(\frac{t_i}{\theta}\right)^{m-1}e^{-(t_i/\theta)^m}.
$$
取对数：
$$
\ln L(\theta)
=n\ln m+(m-1)\sum_{i=1}^n\ln t_i-mn\ln\theta-\sum_{i=1}^n\frac{t_i^m}{\theta^m}.
$$

对 $\theta$ 求导并令其为 0：
$$
\frac{d}{d\theta}\ln L(\theta)
=-\frac{mn}{\theta}+\frac{m}{\theta^{m+1}}\sum_{i=1}^n t_i^m=0.
$$
解得
$$
\theta^m=\frac1n\sum_{i=1}^n t_i^m.
$$
故最大似然估计为
$$
\hat\theta=\left(\frac1n\sum_{i=1}^n t_i^m\right)^{1/m}.
$$
