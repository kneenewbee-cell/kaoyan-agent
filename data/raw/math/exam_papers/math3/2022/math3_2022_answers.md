# 2022 数学三答案解析

资料类型：考研数学三答案解析
年份：2022
科目：数学三
整理状态：依据答案页和题面人工补写整理。


## 选择题

| 题号 | 答案 |
|---|---|
| 1 | C |
| 2 | A |
| 3 | C |
| 4 | A |
| 5 | B |
| 6 | D |
| 7 | C |
| 8 | D |
| 9 | B |
| 10 | B |

## 填空题

| 题号 | 答案 |
|---|---|
| 11 | $e^{1/2}$ |
| 12 | $\ln 3-\dfrac{\sqrt3\pi}{3}$ |
| 13 | $0$ |
| 14 | $(e-1)^2$ |
| 15 | $-1$ |
| 16 | $\dfrac58$ |

## 解答题

| 题号 | 答案 |
|---|---|
| 17 | $y=2x$ |
| 18 | $Q=384$ |
| 19 | $2\pi-2$ |
| 20 | 收敛域为 $[-1,1]$；当 $x\ne0$ 时， $S(x)=\frac{\arctan x}{x}+\frac1{x}\ln\frac{2+x}{2-x}$；且 $S(0)=2$ |
| 21 | 可取 $Q= \begin{pmatrix} \frac1{\sqrt2}&\frac1{\sqrt2}&0\\ 0&0&1\\ -\frac1{\sqrt2}&\frac1{\sqrt2}&0 \end{pmatrix}$；标准形为 $2y_1^2+4y_2^2+4y_3^2$；且 $\min_{x\ne0}\frac{f(x)}{x^Tx}=2$ |
| 22 | $\hat\theta=\frac{2\sum_{i=1}^n X_i+\sum_{j=1}^m Y_j}{2(n+m)}, \qquad D(\hat\theta)=\frac{\theta^2}{n+m}$ |

## 详细解析

### 第 1 题

- 标准答案：C

第 3、4 个命题互为常见等价表述：
$$
\alpha\sim\beta \iff \alpha-\beta=o(\alpha).
$$

第 1 个命题成立。因为 $\alpha\sim\beta$ 意味着
$$
\frac{\alpha}{\beta}\to 1,
$$
于是
$$
\frac{\alpha^2}{\beta^2}\to 1,
$$
即 $\alpha^2\sim\beta^2$。

第 2 个命题不成立。例如取
$$
\alpha(x)=x,\qquad \beta(x)=-x,
$$
则
$$
\alpha^2(x)\sim\beta^2(x),
$$
但 $\alpha(x)/\beta(x)=-1$，故 $\alpha(x)$ 不等价于 $\beta(x)$。

因此真命题为 1、3、4，故选 **C**。

### 第 2 题

- 标准答案：A

当 $n$ 为偶数时，
$$
a_n=\sqrt[n]{n}-\frac1n;
$$
当 $n$ 为奇数时，
$$
a_n=\sqrt[n]{n}+\frac1n.
$$

先比较最大值。$a_1=2$；当奇数 $n\ge3$ 时，$n^{1/n}$ 在 $n\ge3$ 后递减，所以
$$
a_n=n^{1/n}+\frac1n\le 3^{1/3}+\frac13<2.
$$
偶数项满足 $a_n=n^{1/n}-1/n< n^{1/n}\le \sqrt2<2$，故最大值为 $a_1=2$。

再比较最小值。显然
$$
a_2=\sqrt2-\frac12.
$$
当偶数 $n\ge4$ 时，由 $e^u>1+u$ 得
$$
n^{1/n}=e^{(\ln n)/n}>1+\frac{\ln n}{n},
$$
于是
$$
a_n>1+\frac{\ln n-1}{n}>a_2.
$$
而奇数项 $a_n>1>a_2$。因此 $a_2=\sqrt2-\dfrac12$ 为最小值。

故该数列既有最大值，也有最小值，选 **A**。

### 第 3 题

- 标准答案：C

令
$$
u=x-y,\qquad G(u)=\int_0^u (u-t)f(t)\,dt,
$$
则 $F(x,y)=G(x-y)$。

因此
$$
F_x=G'(x-y),\qquad F_y=-G'(x-y),
$$
故
$$
F_x=-F_y.
$$

再求二阶偏导：
$$
F_{xx}=G''(x-y),\qquad F_{yy}=G''(x-y),
$$
于是
$$
F_{xx}=F_{yy}.
$$

故选 **C**。

### 第 4 题

- 标准答案：A

对 $0<x<1$，有
$$
\frac x2<\ln(1+x)<x.
$$
又因为在 $(0,1)$ 上
$$
\sin x<1,\qquad \cos x<1,
$$
从而
$$
\frac{x}{2(1+\cos x)}
<
\frac{\ln(1+x)}{1+\cos x}
<
\frac{x}{1+\cos x}
<
\frac{2x}{1+\sin x}.
$$

逐项积分即得
$$
I_1<I_2<I_3.
$$
故选 **A**。

### 第 5 题

- 标准答案：B

矩阵 $A$ 的特征值为 $1,-1,0$，等价于 $A$ 与
$$
\Lambda=\operatorname{diag}(1,-1,0)
$$
相似，即存在可逆矩阵 $P$ 使
$$
A=P\Lambda P^{-1}.
$$

其余选项分别对应等价、正交相似或合同，都不是该结论的充分必要条件。

故选 **B**。

### 第 6 题

- 标准答案：D

这是由 $1,t,t^2$ 组成的范德蒙德型矩阵。

- 若 $a,b,1$ 两两不同，则
  $$
  |A|=(a-1)(b-1)(b-a)\ne0,
  $$
  方程组有唯一解。
- 若三者中有重复，则 $r(A)<3$。这时只可能出现两种情况：增广矩阵与系数矩阵同秩而无穷多解，或不同秩而无解。

本题中把各退化情形逐一代入可知，不会出现无穷多解，最终只有“唯一解或无解”两种可能。

故选 **D**。

### 第 7 题

- 标准答案：C

两向量组等价当且仅当它们的秩相同，且张成同一子空间。先比较三列行列式：
$$
\det(\alpha_1,\alpha_2,\alpha_3)=(\lambda-1)^2(\lambda+2),
$$
$$
\det(\alpha_1,\alpha_2,\alpha_4)=\lambda(\lambda+1)^2.
$$

当 $\lambda\ne-1,-2$ 时，两组向量都满秩，故等价。  
当 $\lambda=-2$ 或 $\lambda=-1$ 时，两组向量的秩不同，故不等价。

因此取值范围为
$$
\lambda\in\mathbb R,\qquad \lambda\ne-1,\ \lambda\ne-2.
$$
故选 **C**。

### 第 8 题

- 标准答案：D

由于常数不影响方差，且 $X,Y$ 不相关，
$$
D(X-3Y+1)=D(X-3Y)=D(X)+9D(Y).
$$

其中
$$
D(X)=4,
$$
而
$$
D(Y)=np(1-p)=3\cdot\frac13\cdot\frac23=\frac23.
$$

所以
$$
D(X-3Y+1)=4+9\cdot\frac23=4+6=10.
$$
故选 **D**。

### 第 9 题

- 标准答案：B

由大数定律，
$$
\frac1n\sum_{i=1}^n X_i^2 \xrightarrow{P} E(X^2).
$$

计算
$$
E(X^2)=\int_{-1}^1 x^2(1-|x|)\,dx
=2\int_0^1 x^2(1-x)\,dx
=2\left(\frac13-\frac14\right)=\frac16.
$$

故依概率收敛于 $\dfrac16$，选 **B**。

### 第 10 题

- 标准答案：B

设
$$
A=\{\max(X,Y)=2\},\qquad B=\{\min(X,Y)=1\}.
$$

由表知
$$
P(AB)=P(X=1,Y=2)=0.1.
$$
又
$$
P(A)=b+0.1,\qquad P(B)=a+0.1.
$$
由独立性
$$
0.1=P(AB)=P(A)P(B)=(b+0.1)(a+0.1).
$$
再由总概率
$$
a+b+0.4=1\iff a+b=0.6.
$$
联立得
$$
a=0.2,\qquad b=0.4.
$$

于是
$$
E(X)=1\cdot0.4+(-1)\cdot0.6=-0.2,
$$
$$
E(Y)=0\cdot0.3+1\cdot0.2+2\cdot0.5=1.2,
$$
$$
E(XY)=(-1)\cdot1\cdot0.1+(-1)\cdot2\cdot0.4+1\cdot1\cdot0.1+1\cdot2\cdot0.1=-0.6.
$$
故
$$
\operatorname{Cov}(X,Y)=E(XY)-E(X)E(Y)=-0.6-(-0.2)(1.2)=-0.36.
$$
故选 **B**。

### 第 11 题

- 标准答案：$e^{1/2}$

设
$$
L=\lim_{x\to0}\left(\frac{1+e^x}{2}\right)^{\cot x}.
$$
两边取对数：
$$
\ln L=\lim_{x\to0}\cot x\cdot \ln\!\left(\frac{1+e^x}{2}\right).
$$

由
$$
e^x=1+x+o(x),
$$
得
$$
\frac{1+e^x}{2}=1+\frac x2+o(x),
$$
于是
$$
\ln\!\left(\frac{1+e^x}{2}\right)=\frac x2+o(x).
$$
再利用 $\cot x\sim \dfrac1x$，可得
$$
\ln L=\frac12.
$$
故
$$
L=e^{1/2}.
$$

### 第 12 题

- 标准答案：$\ln 3-\dfrac{\sqrt3\pi}{3}$

将分子拆为
$$
2x-4=(2x+2)-6.
$$
于是
$$
\int_0^2\frac{2x-4}{x^2+2x+4}\,dx
=\int_0^2\frac{2x+2}{x^2+2x+4}\,dx
-6\int_0^2\frac{dx}{(x+1)^2+3}.
$$

第一项为
$$
\left[\ln(x^2+2x+4)\right]_0^2=\ln 3.
$$
第二项为
$$
6\cdot\frac1{\sqrt3}\left[\arctan\frac{x+1}{\sqrt3}\right]_0^2
=2\sqrt3\left(\frac\pi3-\frac\pi6\right)=\frac{\sqrt3\pi}{3}.
$$

故结果为
$$
\ln 3-\frac{\sqrt3\pi}{3}.
$$

### 第 13 题

- 标准答案：$0$

先化简：
$$
f(x)=2\cos(\sin x).
$$
该函数以 $2\pi$ 为周期，且关于 $x=0$ 为偶函数。

偶函数的一阶导数是奇函数，二阶导数是偶函数，三阶导数又是奇函数，所以
$$
f^{(3)}(0)=0.
$$
又由于周期为 $2\pi$，
$$
f^{(3)}(2\pi)=f^{(3)}(0)=0.
$$

### 第 14 题

- 标准答案：$(e-1)^2$

由于 $f(x)\ne0$ 当且仅当 $0\le x\le1$，而 $f(y-x)\ne0$ 当且仅当
$$
0\le y-x\le1.
$$
因此积分区域为
$$
0\le x\le1,\qquad x\le y\le x+1.
$$

于是原积分为
$$
\int_0^1\int_x^{x+1} e^x e^{y-x}\,dy\,dx
=\int_0^1\int_x^{x+1} e^y\,dy\,dx.
$$
先对 $y$ 积分：
$$
\int_x^{x+1}e^y\,dy=e^{x+1}-e^x=(e-1)e^x.
$$
再对 $x$ 积分得
$$
(e-1)\int_0^1 e^x\,dx=(e-1)^2.
$$

### 第 15 题

- 标准答案：$-1$

设变换后得到的矩阵为
$$
B=
\begin{pmatrix}
-2&1&-1\\
1&-1&0\\
-1&0&0
\end{pmatrix}.
$$
题中由 $A$ 到 $B$ 的操作是：

1. 交换第 2 行和第 3 行；
2. 将第 2 列的 $-1$ 倍加到第 1 列。

因此逆向恢复 $A$ 时，先把 $B$ 的第 2 列加到第 1 列，再交换第 2、3 行，得
$$
A=
\begin{pmatrix}
-1&1&-1\\
-1&0&0\\
0&-1&0
\end{pmatrix}.
$$
进一步计算
$$
A^{-1}=
\begin{pmatrix}
0&-1&0\\
0&0&-1\\
-1&1&-1
\end{pmatrix}.
$$
所以
$$
\operatorname{tr}(A^{-1})=0+0-1=-1.
$$

因此填
$$
-1.
$$

### 第 16 题

- 标准答案：$\dfrac58$

由独立性，
$$
P(BC)=P(B)P(C)=\frac19.
$$
于是
$$
P(B\cup C)=P(B)+P(C)-P(BC)=\frac13+\frac13-\frac19=\frac59.
$$

又因为 $A$ 与 $B,C$ 都互不相容，所以
$$
P(A\cup B\cup C)=P(A)+P(B\cup C)=\frac13+\frac59=\frac89.
$$

故
$$
P(B\cup C\mid A\cup B\cup C)=\frac{5/9}{8/9}=\frac58.
$$

### 第 17 题

- 标准答案：$y=2x$

这是线性微分方程。积分因子为
$$
\mu(x)=e^{\int \frac{dx}{2\sqrt{x}}}=e^{\sqrt{x}}.
$$
所以
$$
\bigl(ye^{\sqrt{x}}\bigr)'=(2+\sqrt{x})e^{\sqrt{x}}.
$$

积分并利用初值 $y(1)=3$，可得
$$
y(x)=2x+e\,e^{-\sqrt{x}}.
$$

于是
$$
y(x)-2x=e^{\,1-\sqrt{x}}\to0\qquad (x\to+\infty).
$$
因此曲线的渐近线为
$$
y=2x.
$$

### 第 18 题

- 标准答案：$Q=384$

收入为
$$
R=PQ=(1160-1.5Q)Q.
$$
若给定产量 $Q$，则成本最小化问题为
$$
\min (6x+8y)\quad \text{s.t.}\quad Q=12x^{1/2}y^{1/6}.
$$

由约束得
$$
x=\frac{Q^2}{144\,y^{1/3}},
$$
于是成本
$$
C(y)=\frac{Q^2}{24\,y^{1/3}}+8y.
$$
求导并令其为零，得
$$
y=\left(\frac{Q}{24}\right)^{3/2},
$$
从而最小成本为
$$
C(Q)=\frac{\sqrt6}{9}Q^{3/2}.
$$

故利润函数为
$$
\Pi(Q)=1160Q-1.5Q^2-\frac{\sqrt6}{9}Q^{3/2}.
$$
令 $\Pi'(Q)=0$：
$$
1160-3Q-\frac{\sqrt6}{6}\sqrt Q=0.
$$
设 $t=\sqrt Q$，则
$$
18t^2+\sqrt6\,t-6960=0.
$$
解得正根
$$
t=8\sqrt6,
$$
所以
$$
Q=t^2=384.
$$

### 第 19 题

- 标准答案：$2\pi-2$

改用极坐标
$$
x=r\cos\theta,\qquad y=r\sin\theta.
$$
由区域可知
$$
0\le \theta\le \pi,\qquad 0\le r\le 2(\cos\theta+\sin\theta)
$$
对应到适当角域后可化简为第一象限型积分。被积函数化为
$$
\frac{(x-y)^2}{x^2+y^2}
=\frac{r^2(\cos\theta-\sin\theta)^2}{r^2}
=(\cos\theta-\sin\theta)^2.
$$

再乘雅可比 $r$，积分化为
$$
I=\int\!\!\int r(\cos\theta-\sin\theta)^2\,dr\,d\theta.
$$
按题设区域完成积分，得到
$$
I=2\pi-2.
$$

### 第 20 题

- 标准答案：收敛域为 $[-1,1]$；

当 $x\ne0$ 时，
$$
S(x)=\frac{\arctan x}{x}+\frac1{x}\ln\frac{2+x}{2-x},
$$
且
$$
S(0)=2.
$$

先拆开级数：
$$
S(x)=\sum_{n=0}^{\infty}\frac{(-1)^n}{2n+1}x^{2n}
\;+\;
\sum_{n=0}^{\infty}\frac1{4^n(2n+1)}x^{2n}
=S_1(x)+S_2(x).
$$

1. 对于
$$
S_1(x)=\sum_{n=0}^\infty \frac{(-1)^n x^{2n}}{2n+1},
$$
有
$$
xS_1(x)=\sum_{n=0}^\infty \frac{(-1)^n x^{2n+1}}{2n+1}=\arctan x,
$$
所以
$$
S_1(x)=\frac{\arctan x}{x}\qquad (x\ne0).
$$

2. 对于
$$
S_2(x)=\sum_{n=0}^\infty \frac{(x/2)^{2n}}{2n+1},
$$
令 $u=x/2$，则
$$
uS_2(x)=\sum_{n=0}^\infty \frac{u^{2n+1}}{2n+1}
=\frac12\ln\frac{1+u}{1-u},
$$
故
$$
S_2(x)=\frac1{x}\ln\frac{2+x}{2-x}\qquad (x\ne0).
$$

因此
$$
S(x)=\frac{\arctan x}{x}+\frac1{x}\ln\frac{2+x}{2-x}\qquad (x\ne0).
$$

当 $x=0$ 时，
$$
S(0)=1+1=2.
$$

两部分的收敛域交为
$$
[-1,1].
$$

### 第 21 题

- 标准答案：可取
$$
Q=
\begin{pmatrix}
\frac1{\sqrt2}&\frac1{\sqrt2}&0\\
0&0&1\\
-\frac1{\sqrt2}&\frac1{\sqrt2}&0
\end{pmatrix},
$$
标准形为
$$
2y_1^2+4y_2^2+4y_3^2;
$$

且
$$
\min_{x\ne0}\frac{f(x)}{x^Tx}=2.
$$

二次型对应矩阵为
$$
A=
\begin{pmatrix}
3&0&1\\
0&4&0\\
1&0&3
\end{pmatrix}.
$$
其特征多项式可得特征值为
$$
2,\ 4,\ 4.
$$

对应一组两两正交的特征向量可取
$$
\xi_1=(1,0,-1)^T,\quad
\xi_2=(1,0,1)^T,\quad
\xi_3=(0,1,0)^T.
$$
单位化后得到正交矩阵
$$
Q=
\begin{pmatrix}
\frac1{\sqrt2}&\frac1{\sqrt2}&0\\
0&0&1\\
-\frac1{\sqrt2}&\frac1{\sqrt2}&0
\end{pmatrix},
$$
于是
$$
Q^TAQ=\operatorname{diag}(2,4,4).
$$
故标准形为
$$
f=2y_1^2+4y_2^2+4y_3^2.
$$

又因为
$$
\frac{f(x)}{x^Tx}
$$
就是矩阵 $A$ 的 Rayleigh 商，其最小值等于最小特征值，所以
$$
\min_{x\ne0}\frac{f(x)}{x^Tx}=2.
$$

### 第 22 题

- 标准答案：$$
\hat\theta=\frac{2\sum_{i=1}^n X_i+\sum_{j=1}^m Y_j}{2(n+m)},
\qquad
D(\hat\theta)=\frac{\theta^2}{n+m}.
$$

由题意，
$$
X_i\sim \mathrm{Exp}(\theta),\qquad
Y_j\sim \mathrm{Exp}(2\theta),
$$
故密度分别为
$$
f_X(x)=\frac1\theta e^{-x/\theta}\ (x>0),\qquad
f_Y(y)=\frac1{2\theta}e^{-y/(2\theta)}\ (y>0).
$$

样本似然函数为
$$
L(\theta)=\prod_{i=1}^n\frac1\theta e^{-X_i/\theta}
\prod_{j=1}^m\frac1{2\theta}e^{-Y_j/(2\theta)}.
$$
取对数得
$$
\ln L(\theta)
=-m\ln2-(n+m)\ln\theta
-\frac1\theta\sum_{i=1}^n X_i
-\frac1{2\theta}\sum_{j=1}^m Y_j.
$$

求导并令其为零：
$$
\frac{d}{d\theta}\ln L(\theta)
=-\frac{n+m}{\theta}
\frac{1}{\theta^2}\sum_{i=1}^n X_i
\frac{1}{2\theta^2}\sum_{j=1}^m Y_j=0.
$$
解得
$$
\hat\theta=\frac{2\sum_{i=1}^n X_i+\sum_{j=1}^m Y_j}{2(n+m)}.
$$

再算方差。因为
$$
D(X_i)=\theta^2,\qquad D(Y_j)=(2\theta)^2=4\theta^2,
$$
且样本独立，
$$
D\!\left(2\sum_{i=1}^n X_i+\sum_{j=1}^m Y_j\right)
=4n\theta^2+4m\theta^2=4(n+m)\theta^2.
$$
所以
$$
D(\hat\theta)
=\frac{4(n+m)\theta^2}{4(n+m)^2}
=\frac{\theta^2}{n+m}.
$$
