# 2018 年考研数学三答案解析

资料类型：考研数学三答案解析
年份：2018
科目：数学三
整理状态：按答案页图人工校对并整理为正式题卡。

## 选择题

| 题号 | 答案 |
|---|---|
| 1 | D |
| 2 | D |
| 3 | C |
| 4 | D |
| 5 | A |
| 6 | A |
| 7 | A |
| 8 | B |

## 填空题

| 题号 | 答案 |
|---|---|
| 9 | $y=4x-3$ |
| 10 | $e^x\arcsin\sqrt{1-e^{2x}}-\sqrt{1-e^{2x}}+C$ |
| 11 | $C2^x-5$ |
| 12 | $2e$ |
| 13 | $2$ |
| 14 | $\dfrac13$ |

## 解答题

| 题号 | 答案 |
|---|---|
| 15 | $a=1,\ b=1$ |
| 16 | $\dfrac{\sqrt3}{16}\left(\dfrac{\pi}{2}-1\right)$ |
| 17 | 存在，最小值为 $\dfrac1{\pi+4+3\sqrt3}$ |
| 18 | $a_{2n}=\frac{(-1)^n4^n}{(2n)!}-2n-1,\qquad a_{2n+1}=2n+2\quad (n=0,1,2,\ldots)$ |
| 19 | $\lim\limits_{n\to\infty}x_n=0$ |
| 20 | 1. 当 $a\ne2$ 时，解只有 $x=0$；当 $a=2$ 时，解为 $x=k(-2,-1,1)^T,\quad k\in\mathbb R$；2. 当 $a\ne2$ 时，规范形为 $y_1^2+y_2^2+y_3^2$；当 $a=2$ 时，规范形为 $y_1^2+y_2^2$ |
| 21 | $a=2$；满足 $AP=B$ 的可逆矩阵为 $P= \begin{pmatrix} 3-6k_1&4-6k_2&4-6k_3\\ -1+2k_1&-1+2k_2&-1+2k_3\\ k_1&k_2&k_3 \end{pmatrix}, \quad k_2\ne k_3$ |
| 22 | $\operatorname{Cov}(X,Z)=\lambda$ $P\{Z=0\}=e^{-\lambda}$；且对 $n=\pm1,\pm2,\ldots$， $P\{Z=n\}=e^{-\lambda}\frac{\lambda^{\lvert n\rvert}}{2\lvert n\rvert!}$ |
| 23 | $\hat\sigma=\frac1n\sum_{i=1}^n\lvert X_i\rvert$ $E(\hat\sigma)=\sigma,\qquad D(\hat\sigma)=\frac{\sigma^2}{n}$ |

## 详细解析

### 第 1 题

- 标准答案：D

对于 D 选项，$f(x)=\cos\sqrt{|x|}$。

由右导数
$$
f'_+(0)=\lim_{x\to0^+}\frac{f(x)-f(0)}{x}
=\lim_{x\to0^+}\frac{\cos\sqrt{x}-1}{x}
=-\frac12,
$$
左导数
$$
f'_-(0)=\lim_{x\to0^-}\frac{f(x)-f(0)}{x}
=\lim_{x\to0^-}\frac{\cos\sqrt{|x|}-1}{x}
=\frac12.
$$
因此 $f'_+(0)\ne f'_-(0)$，故 $f(x)$ 在 $x=0$ 处不可导，选 D。

### 第 2 题

- 标准答案：D

当 $f(x)=x-\dfrac12$ 时，满足
$$
\int_0^1 f(x)\,dx=0,\qquad f\!\left(\frac12\right)=0,
$$
可排除 A、C。

当 $f(x)=\sqrt{x}-\dfrac23$ 时，也满足
$$
\int_0^1 f(x)\,dx=0,\qquad f''(x)<0,
$$
而
$$
f\!\left(\frac12\right)=\sqrt{\frac12}-\frac23>0,
$$
可排除 B。

因此只有 D 正确。

### 第 3 题

- 标准答案：C

利用对称性可得
$$
M=\int_{-\pi/2}^{\pi/2}\frac{(1+x)^2}{1+x^2}\,dx
=\int_{-\pi/2}^{\pi/2}\left(1+\frac{2x}{1+x^2}\right)\,dx
=\pi.
$$

又容易判断 $K>\pi$，而 $N<\pi$，故
$$
K>M>N.
$$
因此选 C。

### 第 4 题

- 标准答案：D

平均成本为
$$
\frac{C(Q)}{Q}.
$$
其在 $Q_0$ 处取最小值，因此
$$
\left(\frac{C(Q)}{Q}\right)'_{Q=Q_0}=0.
$$
化简得
$$
\frac{Q_0C'(Q_0)-C(Q_0)}{Q_0^2}=0,
$$
所以
$$
Q_0C'(Q_0)=C(Q_0).
$$
故选 D。

### 第 5 题

- 标准答案：A

题中矩阵的特征值均为 $1$，且是三重特征值。若两矩阵相似，则对应的
$$
E-A
$$
与
$$
E-B
$$
的秩必须相同。

对 A 选项有
$$
E-
\begin{pmatrix}
1&1&-1\\
0&1&1\\
0&0&1
\end{pmatrix}
=
\begin{pmatrix}
0&-1&1\\
0&0&-1\\
0&0&0
\end{pmatrix},
$$
其秩与原矩阵对应的 $E-A$ 相同，故 A 正确。

### 第 6 题

- 标准答案：A

对 B 选项，可举反例
$$
A=\begin{pmatrix}1&0\\0&0\end{pmatrix},\quad
B=\begin{pmatrix}1&0\\1&1\end{pmatrix},
$$
则 $r(A,BA)=2\ne r(A)$，故 B 错。

对 C 选项，也可取反例使 $r(A,B)=2\ne\max\{r(A),r(B)\}$。

对 D 选项，同样可取反例说明一般不成立。

而
$$
(A,AB)=A(I,B),
$$
其列空间不超过在 $A$ 的列空间之外增加新秩，因此结论 A 成立，故选 A。

### 第 7 题

- 标准答案：A

由 $f(1+x)=f(1-x)$ 可知 $f(x)$ 关于 $x=1$ 对称，所以
$$
\int_{-\infty}^1 f(x)\,dx=\int_1^{+\infty} f(x)\,dx=0.5.
$$
又已知
$$
\int_0^2 f(x)\,dx=0.6,
$$
由对称性可得
$$
\int_0^1 f(x)\,dx=\int_1^2 f(x)\,dx=0.3.
$$
因此
$$
P(X<0)=\int_{-\infty}^0 f(x)\,dx
=\int_{-\infty}^1 f(x)\,dx-\int_0^1 f(x)\,dx
=0.5-0.3=0.2.
$$
故选 A。

### 第 8 题

- 标准答案：B

由正态总体抽样理论，
$$
\overline X\sim N\!\left(\mu,\frac{\sigma^2}{n}\right),
$$
且
$$
\frac{(n-1)S^2}{\sigma^2}\sim\chi^2(n-1),
$$
并与 $\overline X$ 独立。

因此
$$
\frac{\sqrt n(\overline X-\mu)}{S}\sim t(n-1).
$$
故选 B。

### 第 9 题

- 标准答案：$y=4x-3$

有
$$
y'=2x+\frac2x,\qquad y''=2-\frac2{x^2}.
$$
令 $y''=0$ 得拐点横坐标 $x=1$（定义域内只取正值），代入得拐点为 $(1,1)$。

此时切线斜率
$$
y'(1)=2+\frac21=4.
$$
因此切线方程为
$$
y-1=4(x-1),
$$
即
$$
y=4x-3.
$$

### 第 10 题

- 标准答案：$e^x\arcsin\sqrt{1-e^{2x}}-\sqrt{1-e^{2x}}+C$

令
$$
\arcsin\sqrt{1-e^{2x}}=t,
$$
则
$$
e^x=|\cos t|=\cos t
$$
（在积分区间对应情形下取正值），原式可化为
$$
-\int t\sin t\,dt
=t\cos t-\int \cos t\,dt
=t\cos t-\sin t+C.
$$
再代回
$$
t=\arcsin\sqrt{1-e^{2x}},\qquad \sin t=\sqrt{1-e^{2x}},\qquad \cos t=e^x,
$$
得
$$
\int e^x\arcsin\sqrt{1-e^{2x}}\,dx
=e^x\arcsin\sqrt{1-e^{2x}}-\sqrt{1-e^{2x}}+C.
$$

### 第 11 题

- 标准答案：$C2^x-5$

由二阶差分定义，
$$
\Delta^2 y_x=\Delta y_{x+1}-\Delta y_x=(y_{x+2}-y_{x+1})-(y_{x+1}-y_x)
=y_{x+2}-2y_{x+1}+y_x.
$$
原方程化为
$$
y_{x+2}-2y_{x+1}=5.
$$

对应齐次方程的特征方程为
$$
\lambda^2-2\lambda=0,
$$
其非零特征根为 $\lambda=2$，故齐次解为 $C2^x$。

设特解为常数 $A$，代入得 $-A=5$，故 $A=-5$。
于是通解为
$$
y_x=C2^x-5.
$$

### 第 12 题

- 标准答案：$2e$

移项并同除以 $\Delta x$，得
$$
\frac{f(x+\Delta x)-f(x)}{\Delta x}-2xf(x)=\frac{o(\Delta x)}{\Delta x}.
$$
令 $\Delta x\to0$，可得
$$
f'(x)=2xf(x).
$$
解微分方程
$$
\frac{f'(x)}{f(x)}=2x
$$
得
$$
f(x)=Ce^{x^2}.
$$
由 $f(0)=2$ 得 $C=2$，故
$$
f(1)=2e.
$$

### 第 13 题

- 标准答案：$2$

以向量组 $(\alpha_1,\alpha_2,\alpha_3)$ 为基，线性变换 $A$ 的矩阵为
$$
\begin{pmatrix}
1&0&1\\
1&1&0\\
0&1&1
\end{pmatrix}.
$$
由于 $\alpha_1,\alpha_2,\alpha_3$ 线性无关，这个表示矩阵与 $A$ 相似，故行列式相同。

因此
$$
|A|=\begin{vmatrix}
1&0&1\\
1&1&0\\
0&1&1
\end{vmatrix}=2.
$$

### 第 14 题

- 标准答案：$\dfrac13$

由条件概率公式，
$$
P(AC\mid A\cup B)=\frac{P\bigl(AC\cap(A\cup B)\bigr)}{P(A\cup B)}.
$$
注意到
$$
AC\cap(A\cup B)=AC,
$$
所以分子为
$$
P(AC)=P(A)P(C)=\frac14.
$$
又
$$
P(A\cup B)=P(A)+P(B)-P(AB)=\frac12+\frac12-\frac14=\frac34.
$$
因此
$$
P(AC\mid A\cup B)=\frac{1/4}{3/4}=\frac13.
$$

### 第 15 题

- 标准答案：$a=1,\ b=1$

令
$$
t=\frac1x,
$$
则当 $x\to+\infty$ 时，$t\to0^+$，原极限化为
$$
\lim_{t\to0^+}\frac{(a+bt)e^t-1}{t}=2.
$$

若极限存在，需有
$$
\lim_{t\to0^+}\bigl[(a+bt)e^t-1\bigr]=0,
$$
即
$$
a-1=0,
$$
故 $a=1$。

于是
$$
\lim_{t\to0^+}\frac{(1+bt)e^t-1}{t}
=\lim_{t\to0^+}\left(be^t+\frac{e^t-1}{t}\right)
=b+1.
$$
由题设得 $b+1=2$，所以 $b=1$。

### 第 16 题

- 标准答案：$\dfrac{\sqrt3}{16}\left(\dfrac{\pi}{2}-1\right)$

由区域边界可知
$$
0\le x\le \frac1{\sqrt2},\qquad \sqrt3\,x\le y\le \sqrt3(1-x^2).
$$
因此
$$
\iint_D x^2\,dx\,dy
=\int_0^{1/\sqrt2}\!\!dx\int_{\sqrt3 x}^{\sqrt3(1-x^2)} x^2\,dy
=\sqrt3\int_0^{1/\sqrt2}x^2(\sqrt{1-x^2}-x)\,dx.
$$

分成两项：
$$
\int_0^{1/\sqrt2}x^2\sqrt{1-x^2}\,dx.
$$
令 $x=\sin t$，则 $t\in[0,\pi/4]$，上式化为
$$
\int_0^{\pi/4}\sin^2 t\cos^2 t\,dt
=\frac18\int_0^{\pi/4}(1-\cos4t)\,dt
=\frac{\pi}{32}.
$$
又
$$
\int_0^{1/\sqrt2}x^3\,dx=\frac1{16}.
$$
故
$$
\iint_D x^2\,dx\,dy
=\sqrt3\left(\frac{\pi}{32}-\frac1{16}\right)
=\frac{\sqrt3}{16}\left(\frac{\pi}{2}-1\right).
$$

### 第 17 题

- 标准答案：存在，最小值为 $\dfrac1{\pi+4+3\sqrt3}$

设圆的半径为 $x$，正方形边长为 $y$，正三角形边长为 $z$，则问题化为求
$$
f(x,y,z)=\pi x^2+y^2+\frac{\sqrt3}{4}z^2
$$
在约束
$$
2\pi x+4y+3z=2,\qquad x>0,\ y>0,\ z>0
$$
下是否有最小值。

令
$$
L(x,y,z,\lambda)=\pi x^2+y^2+\frac{\sqrt3}{4}z^2+\lambda(2\pi x+4y+3z-2).
$$
由拉格朗日方程组
$$
\frac{\partial L}{\partial x}=2\pi x+2\pi\lambda=0,\quad
\frac{\partial L}{\partial y}=2y+4\lambda=0,\quad
\frac{\partial L}{\partial z}=\frac{\sqrt3}{2}z+3\lambda=0,
$$
可解得
$$
x_0=\frac1{\pi+4+3\sqrt3},\quad
y_0=\frac2{\pi+4+3\sqrt3},\quad
z_0=\frac{2\sqrt3}{\pi+4+3\sqrt3}.
$$
此时
$$
f(x_0,y_0,z_0)=\frac1{\pi+4+3\sqrt3}.
$$

再比较边界情形 $xyz=0$，可得最小值更大，因此原问题的最小值存在，且为
$$
\frac1{\pi+4+3\sqrt3}.
$$

### 第 18 题

- 标准答案：$$
a_{2n}=\frac{(-1)^n4^n}{(2n)!}-2n-1,\qquad
a_{2n+1}=2n+2\quad (n=0,1,2,\ldots).
$$

先展开
$$
\cos2x=\sum_{n=0}^{\infty}\frac{(-1)^n(2x)^{2n}}{(2n)!}
=\sum_{n=0}^{\infty}\frac{(-1)^n4^n}{(2n)!}x^{2n}.
$$

又
$$
\frac1{(1+x)^2}=\left(-\frac1{1+x}\right)'
=-\left(\sum_{n=0}^{\infty}(-1)^n x^n\right)'
=\sum_{n=0}^{\infty}(-1)^n(n+1)x^n.
$$
故
$$
\cos2x-\frac1{(1+x)^2}
=\sum_{n=0}^{\infty}\frac{(-1)^n4^n}{(2n)!}x^{2n}
+\sum_{n=0}^{\infty}(-1)^{n+1}(n+1)x^n.
$$

于是偶次项与奇次项系数分别为
$$
a_{2n}=\frac{(-1)^n4^n}{(2n)!}-2n-1,
$$
$$
a_{2n+1}=2n+2\qquad (n=0,1,2,\ldots).
$$

### 第 19 题

- 标准答案：$\lim\limits_{n\to\infty}x_n=0$

由题设
$$
e^{x_{n+1}}=\frac{e^{x_n}-1}{x_n}.
$$
由微分中值定理，存在 $\xi_n\in(0,x_n)$，使得
$$
\frac{e^{x_n}-1}{x_n}=e^{\xi_n}.
$$
所以
$$
e^{x_{n+1}}=e^{\xi_n},
$$
从而
$$
0<x_{n+1}<x_n.
$$
故 $\{x_n\}$ 单调递减且有下界 $0$，因此收敛。设
$$
\lim_{n\to\infty}x_n=a\ge0.
$$
将极限代入原关系得
$$
ae^a=e^a-1.
$$

令
$$
f(x)=xe^x-e^x+1,
$$
则
$$
f'(x)=xe^x.
$$
当 $x>0$ 时，$f'(x)>0$，所以 $f(x)$ 在 $[0,+\infty)$ 上单调增加。又 $f(0)=0$，故方程在 $[0,+\infty)$ 上唯一解为 $a=0$。

因此
$$
\lim_{n\to\infty}x_n=0.
$$

### 第 20 题

- 标准答案：1. 当 $a\ne2$ 时，解只有 $x=0$；当 $a=2$ 时，解为
$$
x=k(-2,-1,1)^T,\quad k\in\mathbb R.
$$
2. 当 $a\ne2$ 时，规范形为
$$
y_1^2+y_2^2+y_3^2;
$$
当 $a=2$ 时，规范形为
$$
y_1^2+y_2^2.
$$

由 $f(x_1,x_2,x_3)=0$ 可知三个平方项都为零，因此
$$
\begin{cases}
x_1-x_2+x_3=0,\\
x_2+x_3=0,\\
x_1+ax_3=0.
\end{cases}
$$
其系数矩阵经初等行变换化为
$$
\begin{pmatrix}
1&-1&1\\
0&1&1\\
1&0&a
\end{pmatrix}
\to
\begin{pmatrix}
1&0&2\\
0&1&1\\
0&0&a-2
\end{pmatrix}.
$$
当 $a\ne2$ 时，只有零解；当 $a=2$ 时，有无穷多解，
$$
x=k(-2,-1,1)^T,\quad k\in\mathbb R.
$$

由此知，当 $a\ne2$ 时，二次型正定，故规范形为
$$
y_1^2+y_2^2+y_3^2.
$$

当 $a=2$ 时，
$$
f(x_1,x_2,x_3)=2x_1^2+2x_2^2+6x_3^2-2x_1x_2+6x_1x_3
=2\left(x_1-\frac12x_2+\frac32x_3\right)^2+\frac32(x_2+x_3)^2,
$$
所以规范形为
$$
y_1^2+y_2^2.
$$

### 第 21 题

- 标准答案：$$
a=2.
$$

满足 $AP=B$ 的可逆矩阵为
$$
P=
\begin{pmatrix}
3-6k_1&4-6k_2&4-6k_3\\
-1+2k_1&-1+2k_2&-1+2k_3\\
k_1&k_2&k_3
\end{pmatrix},
\quad k_2\ne k_3.
$$

先分别对矩阵 $A,B$ 作初等行变换：
$$
A=
\begin{pmatrix}
1&2&a\\
1&3&0\\
2&7&-a
\end{pmatrix}
\to
\begin{pmatrix}
1&0&3a\\
0&1&-a\\
0&0&0
\end{pmatrix},
$$
$$
B=
\begin{pmatrix}
1&a&2\\
0&1&1\\
-1&1&1
\end{pmatrix}
\to
\begin{pmatrix}
1&0&0\\
0&1&1\\
0&0&2-a
\end{pmatrix}.
$$
由于 $A,B$ 可经初等列变换互化，故秩相同，从而
$$
2-a=0,\qquad a=2.
$$

当 $a=2$ 时，对增广矩阵 $(A\mid B)$ 进行初等行变换，得
$$
(A\mid B)\to
\begin{pmatrix}
1&0&6&3&4&4\\
0&1&-2&-1&-1&-1\\
0&0&0&0&0&0
\end{pmatrix}.
$$
设 $B=(\beta_1,\beta_2,\beta_3)$，则通解为
$$
X=
\begin{pmatrix}
3-6k_1&4-6k_2&4-6k_3\\
-1+2k_1&-1+2k_2&-1+2k_3\\
k_1&k_2&k_3
\end{pmatrix}.
$$
又
$$
|X|=k_3-k_2,
$$
故当且仅当 $k_2\ne k_3$ 时，$X$ 可逆。于是所求可逆矩阵 $P$ 即为上式。

### 第 22 题

- 标准答案：$$
\operatorname{Cov}(X,Z)=\lambda.
$$

$$
P\{Z=0\}=e^{-\lambda},
$$
且对 $n=\pm1,\pm2,\ldots$，
$$
P\{Z=n\}=e^{-\lambda}\frac{\lambda^{|n|}}{2|n|!}.
$$

由 $Z=XY$ 与独立性，
$$
EX=(-1)\cdot\frac12+1\cdot\frac12=0,
$$
$$
E(XZ)=E(X^2Y)=EX^2\cdot EY=\lambda.
$$
所以
$$
\operatorname{Cov}(X,Z)=E(XZ)-EX\cdot EZ=\lambda.
$$

又因为 $X=\pm1$，故 $Z$ 可能取所有整数值。

当 $Z=0$ 时，只能是 $Y=0$，因此
$$
P\{Z=0\}=P\{Y=0\}=e^{-\lambda}.
$$

对 $n=\pm1,\pm2,\ldots$，
$$
P\{Z=n\}=P\{XY=n\}
=P\left\{X=\frac{n}{|n|},\,Y=|n|\right\}
=P\left\{X=\frac{n}{|n|}\right\}P\{Y=|n|\}.
$$
于是
$$
P\{Z=n\}=\frac12\cdot e^{-\lambda}\frac{\lambda^{|n|}}{|n|!}
=e^{-\lambda}\frac{\lambda^{|n|}}{2|n|!}.
$$

### 第 23 题

- 标准答案：$$
\hat\sigma=\frac1n\sum_{i=1}^n|X_i|.
$$

$$
E(\hat\sigma)=\sigma,\qquad D(\hat\sigma)=\frac{\sigma^2}{n}.
$$

样本似然函数为
$$
L(\sigma)=\prod_{i=1}^n\frac1{2\sigma}e^{-\frac{|x_i|}{\sigma}}
=\frac1{2^n\sigma^n}e^{-\frac1\sigma\sum_{i=1}^n|x_i|}.
$$
取对数得
$$
\ln L(\sigma)=-n\ln2-n\ln\sigma-\frac1\sigma\sum_{i=1}^n|x_i|.
$$
求导并令其为零：
$$
\frac{d\ln L(\sigma)}{d\sigma}
=-\frac n\sigma+\frac1{\sigma^2}\sum_{i=1}^n|x_i|=0,
$$
解得
$$
\hat\sigma=\frac1n\sum_{i=1}^n|X_i|.
$$

又因为
$$
E|X|=\int_{-\infty}^{+\infty}|x|f(x;\sigma)\,dx=\sigma,
$$
所以
$$
E(\hat\sigma)=\frac1n\sum_{i=1}^nE|X_i|=\sigma.
$$

再由
$$
E(|X|^2)=\int_{-\infty}^{+\infty}x^2f(x;\sigma)\,dx=2\sigma^2,
$$
得
$$
D(|X|)=E(|X|^2)-[E|X|]^2=2\sigma^2-\sigma^2=\sigma^2.
$$
因此
$$
D(\hat\sigma)=\frac1{n^2}\sum_{i=1}^nD(|X_i|)=\frac{\sigma^2}{n}.
$$
