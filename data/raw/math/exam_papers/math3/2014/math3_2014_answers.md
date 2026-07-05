# 2014 年数学三答案解析

资料类型：考研数学三答案解析
年份：2014
科目：数学三
整理状态：按答案页图核对后整理；个别题目解析为依据标准答案补写的清晰版。

## 选择题

| 题号 | 答案 |
|---|---|
| 1 | A |
| 2 | C |
| 3 | D |
| 4 | D |
| 5 | B |
| 6 | A |
| 7 | B |
| 8 | C |

## 填空题

| 题号 | 答案 |
|---|---|
| 9 | $20-Q$ |
| 10 | $\dfrac32-\ln 2$ |
| 11 | $\dfrac12$ |
| 12 | $\dfrac{e-1}{2}$ |
| 13 | $[-2,\,2]$ |
| 14 | $\dfrac{2}{5n}$ |

## 解答题

| 题号 | 答案 |
|---|---|
| 15 | $\dfrac12$ |
| 16 | $-\dfrac34$ |
| 17 | $f(u)=\dfrac{1}{16}\left(e^{4u}-4u-1\right)$ |
| 18 | 收敛域为 $(-1,1)$， $$ S(x)=\frac{3-x}{(1-x)^3}. $$ |
| 19 | 命题成立 |
| 20 | 基础解系可取 $\alpha=\begin{pmatrix}-1\\2\\3\\1\end{pmatrix}$；且 $B= \begin{pmatrix} 2&6&-1\\ -1&-3&1\\ -1&-4&1\\ 0&0&0 \end{pmatrix} +(\,k_1\alpha,\ k_2\alpha,\ k_3\alpha\,),\quad k_1,k_2,k_3\in\mathbb R$ |
| 21 | 两矩阵相似 |
| 22 | $F_Y(y)= \begin{cases} 0,& y<0,\\[4pt] \dfrac{3y}{4},& 0\le y<1,\\[6pt] \dfrac12+\dfrac y4,& 1\le y<2,\\[6pt] 1,& y\ge 2, \end{cases}$；且 $E(Y)=\frac34$ |
| 23 | $\begin{array}{ccc} X\backslash Y & 0 & 1\\\hline 0 & \dfrac29 & \dfrac19\\ 1 & \dfrac19 & \dfrac59 \end{array}$；且 $P\{X+Y\le 1\}=\frac49$ |

## 详细解析

### 第 1 题

- 答案：A

由 $a_n\to a\ne 0$，对 $\varepsilon=\dfrac{|a|}{2}>0$，存在 $N$，使得 $n>N$ 时
$$
|a_n-a|<\frac{|a|}{2}.
$$
于是
$$
|a_n|\ge |a|-|a_n-a|>|a|-\frac{|a|}{2}=\frac{|a|}{2}.
$$
故应选 `A`。

### 第 2 题

- 答案：C

对选项 (C)，有
$$
\lim_{x\to\infty}\frac{x+\sin(1/x)}{x}=1,\qquad
\lim_{x\to\infty}\left[x+\sin\left(\frac1x\right)-x\right]=0.
$$
因此 $y=x$ 是其斜渐近线。其余各项都不存在水平、竖直或斜渐近线。
故选 `C`。

### 第 3 题

- 答案：D

由
$$
\tan x=x+\frac{x^3}{3}+o(x^3)
$$
可知
$$
p(x)-\tan x=(a)+(b-1)x+cx^2+\left(d-\frac13\right)x^3+o(x^3).
$$
它比 $x^3$ 高阶，故各低阶系数都应为零：
$$
a=0,\quad b=1,\quad c=0,\quad d=\frac13.
$$
因此错误项是把 $d$ 写成 $\dfrac16$ 的选项 `D`。

### 第 4 题

- 答案：D

当 $f''(x)\ge 0$ 时，$f$ 在 $[0,1]$ 上为凸函数。凸函数的图像位于连接两端点的弦下方，而
$$
g(x)=f(0)(1-x)+f(1)x
$$
正是连接 $(0,f(0))$ 与 $(1,f(1))$ 的线段方程，所以
$$
f(x)\le g(x),\qquad x\in[0,1].
$$
故选 `D`。

### 第 5 题

- 答案：B

按第一列展开：
$$
\begin{vmatrix}
0&a&b&0\\
a&0&0&b\\
0&c&d&0\\
c&0&0&d
\end{vmatrix}
=-a
\begin{vmatrix}
a&b&0\\
c&d&0\\
0&0&d
\end{vmatrix}
-c
\begin{vmatrix}
a&b&0\\
0&0&b\\
c&d&0
\end{vmatrix}.
$$
化简得
$$
-ad(ad-bc)+bc(ad-bc)=-(ad-bc)^2.
$$
故选 `B`。

### 第 6 题

- 答案：A

有
$$
(\alpha_1+k\alpha_3,\ \alpha_2+l\alpha_3,\ \alpha_3)
=(\alpha_1,\alpha_2,\alpha_3)
\begin{pmatrix}
1&0&0\\
0&1&0\\
k&l&1
\end{pmatrix}.
$$
若 $\alpha_1,\alpha_2,\alpha_3$ 线性无关，则上述变换矩阵可逆，所以 $\alpha_1+k\alpha_3,\alpha_2+l\alpha_3$ 一定线性无关，故该条件是必要的。

但其并非充分。例如取
$$
\alpha_1=\begin{pmatrix}1\\0\\0\end{pmatrix},\ 
\alpha_2=\begin{pmatrix}0\\1\\0\end{pmatrix},\ 
\alpha_3=\begin{pmatrix}0\\0\\0\end{pmatrix},
$$
则对任意 $k,l$，$\alpha_1+k\alpha_3,\alpha_2+l\alpha_3$ 仍线性无关，而 $\alpha_1,\alpha_2,\alpha_3$ 线性相关。
故选 `A`。

### 第 7 题

- 答案：B

由独立性，
$$
P(A-B)=P(A)-P(AB)=P(A)-P(A)P(B)=0.5P(A).
$$
题设给出 $P(A-B)=0.3$，故
$$
P(A)=0.6.
$$
于是
$$
P(B-A)=P(B)-P(AB)=P(B)-P(A)P(B)=0.5-0.6\times0.5=0.2.
$$
故选 `B`。

### 第 8 题

- 答案：C

因为
$$
X_1-X_2\sim N(0,2\sigma^2),
$$
所以
$$
\frac{X_1-X_2}{\sqrt2\,\sigma}\sim N(0,1).
$$
又有
$$
\frac{X_3}{\sigma}\sim N(0,1),\qquad \left(\frac{X_3}{\sigma}\right)^2\sim\chi^2(1).
$$
故
$$
S=\frac{\dfrac{X_1-X_2}{\sqrt2\,\sigma}}{\sqrt{\left(\dfrac{X_3}{\sigma}\right)^2}}
\sim t(1).
$$
故选 `C`。

### 第 9 题

- 答案：$20-Q$

由 $Q=40-2P$ 得
$$
P=20-\frac Q2.
$$
于是收益函数
$$
R(Q)=PQ=\left(20-\frac Q2\right)Q=20Q-\frac12Q^2.
$$
边际收益为
$$
R'(Q)=20-Q.
$$

### 第 10 题

- 答案：$\dfrac32-\ln 2$

由 $xy+1=0$ 得
$$
x=-\frac1y,
$$
由 $y+x=0$ 得
$$
x=-y.
$$
交点满足 $-y=-1/y$，得 $y=1$（结合区域位置取正值）。因此面积为
$$
S=\int_1^2\left(-\frac1y-(-y)\right)\,dy
=\int_1^2\left(y-\frac1y\right)\,dy
=\left(\frac{y^2}{2}-\ln y\right)\Big|_1^2
=\frac32-\ln2.
$$

### 第 11 题

- 答案：$\dfrac12$

分部积分可得
$$
\int xe^{2x}\,dx=\frac{e^{2x}}{4}(2x-1)+C.
$$
故
$$
\int_0^a xe^{2x}\,dx=\frac{e^{2a}}{4}(2a-1)+\frac14.
$$
令其等于 $\dfrac14$，得到
$$
\frac{e^{2a}}{4}(2a-1)=0,
$$
故 $2a-1=0$，于是
$$
a=\frac12.
$$

### 第 12 题

- 答案：$\dfrac{e-1}{2}$

将积分拆开并交换次序：
$$
\int_0^1dy\int_y^1\frac{e^{x^2}}x\,dx
=\int_0^1dx\int_0^x\frac{e^{x^2}}x\,dy
=\int_0^1e^{x^2}\,dx.
$$
另一部分为
$$
\int_0^1dy\int_y^1 e^{y^2}\,dx
=\int_0^1(1-y)e^{y^2}\,dy.
$$
所以原式
$$
=\int_0^1e^{x^2}\,dx-\int_0^1e^{y^2}\,dy+\int_0^1ye^{y^2}\,dy
=\int_0^1ye^{y^2}\,dy
=\frac12(e-1).
$$

### 第 13 题

- 答案：$[-2,\,2]$

配方得
$$
f(x_1,x_2,x_3)
=(x_1+ax_3)^2-(x_2-2x_3)^2+(4-a^2)x_3^2.
$$
要使负惯性指数为 $1$，最后一项不能再额外产生负平方项，因此需
$$
4-a^2\ge 0.
$$
故
$$
-2\le a\le 2.
$$

### 第 14 题

- 答案：$\dfrac{2}{5n}$

先求
$$
E(X^2)=\int_\theta^{2\theta}x^2\cdot \frac{2x}{3\theta^2}\,dx
=\frac{2}{3\theta^2}\int_\theta^{2\theta}x^3\,dx
=\frac52\theta^2.
$$
于是
$$
E\left(c\sum_{i=1}^nX_i^2\right)
=c\sum_{i=1}^nE(X_i^2)
=cn\cdot\frac52\theta^2.
$$
令其等于 $\theta^2$，得
$$
cn\cdot\frac52=1,
$$
所以
$$
c=\frac{2}{5n}.
$$

### 第 15 题

- 答案：$\dfrac12$

因为
$$
x^2\ln\left(1+\frac1x\right)\sim x\qquad (x\to+\infty),
$$
原极限可写为
$$
\lim_{x\to+\infty}\frac{\int_1^x\left[t^2\left(e^{1/t}-1\right)-t\right]dt}{x}.
$$
由洛必达法则得
$$
\lim_{x\to+\infty}\left[x^2\left(e^{1/x}-1\right)-x\right].
$$
令 $u=\dfrac1x\to 0^+$，则上式变为
$$
\lim_{u\to0^+}\frac{e^u-1-u}{u^2}.
$$
再用展开式
$$
e^u=1+u+\frac{u^2}{2}+o(u^2),
$$
得极限为
$$
\frac12.
$$

### 第 16 题

- 答案：$-\dfrac34$

将积分化为极坐标：
$$
x=r\cos\theta,\quad y=r\sin\theta,\quad
1\le r\le 2,\ 0\le\theta\le\frac\pi2.
$$
于是
$$
\iint_D\frac{x\sin(\pi\sqrt{x^2+y^2})}{x+y}\,dxdy
=\int_0^{\pi/2}\frac{\cos\theta}{\cos\theta+\sin\theta}\,d\theta
\int_1^2 r\sin(\pi r)\,dr.
$$
由对称性
$$
\int_0^{\pi/2}\frac{\cos\theta}{\cos\theta+\sin\theta}\,d\theta
=\frac12\int_0^{\pi/2}1\,d\theta
=\frac\pi4.
$$
再算
$$
\int_1^2r\sin(\pi r)\,dr
=\frac1\pi\left(-r\cos\pi r+\frac1\pi\sin\pi r\right)\Big|_1^2
=-\frac3\pi.
$$
因此原积分
$$
=\frac\pi4\cdot\left(-\frac3\pi\right)
=-\frac34.
$$

### 第 17 题

- 答案：$f(u)=\dfrac{1}{16}\left(e^{4u}-4u-1\right)$

记
$$
u=e^x\cos y,\qquad z=f(u).
$$
则
$$
\frac{\partial z}{\partial x}=f'(u)e^x\cos y,\qquad
\frac{\partial z}{\partial y}=-f'(u)e^x\sin y.
$$
代入题设得
$$
f'(u)e^x=(4f(u)+u)e^x,
$$
即
$$
f'(u)-4f(u)=u.
$$
解线性微分方程：
$$
f(u)=Ce^{4u}-\frac u4-\frac1{16}.
$$
由 $f(0)=0$ 得
$$
C=\frac1{16}.
$$
因此
$$
f(u)=\frac1{16}\left(e^{4u}-4u-1\right).
$$

### 第 18 题

- 答案：收敛域为 $(-1,1)$，
$$
S(x)=\frac{3-x}{(1-x)^3}.
$$

系数 $a_n=(n+1)(n+3)$，有
$$
\lim_{n\to\infty}\left|\frac{a_{n+1}}{a_n}\right|
=\lim_{n\to\infty}\frac{(n+2)(n+4)}{(n+1)(n+3)}=1,
$$
故收敛半径 $R=1$。当 $x=\pm1$ 时，通项不趋于零，所以端点都发散，收敛域为
$$
(-1,1).
$$

设
$$
S(x)=\sum_{n=0}^{\infty}(n+1)(n+3)x^n.
$$
利用
$$
\sum_{n=0}^{\infty}(n+1)x^n=\frac1{(1-x)^2},\qquad
\sum_{n=0}^{\infty}(n+1)(n+2)x^n=\frac{2}{(1-x)^3},
$$
并注意
$$
(n+1)(n+3)=(n+1)(n+2)+(n+1),
$$
可得
$$
S(x)=\frac{2}{(1-x)^3}+\frac{1}{(1-x)^2}
=\frac{3-x}{(1-x)^3}.
$$

### 第 19 题

- 答案：命题成立

对任意 $x\in[a,b]$，由 $0\le g(t)\le 1$ 可得
$$
0=\int_a^x0\,dt\le \int_a^xg(t)\,dt\le \int_a^x1\,dt=x-a,
$$
第 1 问成立。

令
$$
F(x)=\int_a^{a+\int_a^x g(u)\,du}f(t)\,dt-\int_a^x f(t)g(t)\,dt,\qquad x\in[a,b].
$$
则
$$
F'(x)=\Bigl[f\Bigl(a+\int_a^xg(u)\,du\Bigr)-f(x)\Bigr]g(x).
$$
由第 1 问知
$$
a+\int_a^xg(u)\,du\le x,
$$
而 $f$ 单调增加，故
$$
f\Bigl(a+\int_a^xg(u)\,du\Bigr)\le f(x).
$$
再结合 $g(x)\ge 0$，得到
$$
F'(x)\le 0.
$$
所以 $F(x)$ 在 $[a,b]$ 上单调不增。又
$$
F(a)=0,
$$
故
$$
F(b)\le 0.
$$
即
$$
\int_a^{a+\int_a^b g(t)\,dt}f(x)\,dx\le \int_a^b f(x)g(x)\,dx.
$$
证毕。

### 第 20 题

- 答案：基础解系可取
$$
\alpha=\begin{pmatrix}-1\\2\\3\\1\end{pmatrix},
$$
且
$$
B=
\begin{pmatrix}
2&6&-1\\
-1&-3&1\\
-1&-4&1\\
0&0&0
\end{pmatrix}
+(\,k_1\alpha,\ k_2\alpha,\ k_3\alpha\,),\quad k_1,k_2,k_3\in\mathbb R.
$$

对矩阵 $A$ 作初等行变换，可化为
$$
\begin{pmatrix}
1&0&0&1\\
0&1&0&-2\\
0&0&1&-3
\end{pmatrix}.
$$
因此令 $x_4=t$，则
$$
x_1=-t,\quad x_2=2t,\quad x_3=3t,
$$
故 $Ax=0$ 的一个基础解系为
$$
\alpha=\begin{pmatrix}-1\\2\\3\\1\end{pmatrix}.
$$

再看 $AB=E$。设 $E=(e_1,e_2,e_3)$，则 $B$ 的三列分别是方程组
$$
Ax=e_1,\qquad Ax=e_2,\qquad Ax=e_3
$$
的解。由同样的消元可得三个特解分别可取
$$
\beta_1=\begin{pmatrix}2\\-1\\-1\\0\end{pmatrix},\quad
\beta_2=\begin{pmatrix}6\\-3\\-4\\0\end{pmatrix},\quad
\beta_3=\begin{pmatrix}-1\\1\\1\\0\end{pmatrix}.
$$
因此所有解为
$$
x=\beta_j+k_j\alpha,\qquad j=1,2,3.
$$
把三列合并，得
$$
B=
\begin{pmatrix}
2&6&-1\\
-1&-3&1\\
-1&-4&1\\
0&0&0
\end{pmatrix}
+(\,k_1\alpha,\ k_2\alpha,\ k_3\alpha\,),\quad k_1,k_2,k_3\in\mathbb R.
$$

### 第 21 题

- 答案：两矩阵相似

记
$$
A=\mathbf 1\mathbf 1^T,
$$
其中 $\mathbf 1=(1,1,\dots,1)^T$。则 $A$ 的特征值为
$$
\lambda_1=n,\qquad \lambda_2=\cdots=\lambda_n=0.
$$
因为 $A$ 是实对称矩阵，所以它相似于对角矩阵
$$
\operatorname{diag}(n,0,\dots,0).
$$

再记
$$
B=
\begin{pmatrix}
0&\cdots&0&1\\
0&\cdots&0&2\\
\vdots& &\vdots&\vdots\\
0&\cdots&0&n
\end{pmatrix}.
$$
容易看出 $B$ 的秩为 $1$，其特征多项式同样是
$$
|\lambda E-B|=(\lambda-n)\lambda^{n-1},
$$
故它的特征值也是 $n,0,\dots,0$。

又因为 $r(B)=1$，对应特征值 $0$ 的特征子空间维数为 $n-1$；对应特征值 $n$ 也有非零特征向量，所以 $B$ 也可对角化，并相似于
$$
\operatorname{diag}(n,0,\dots,0).
$$
因此 $A$ 与 $B$ 相似。

### 第 22 题

- 答案：$$
F_Y(y)=
\begin{cases}
0,& y<0,\\[4pt]
\dfrac{3y}{4},& 0\le y<1,\\[6pt]
\dfrac12+\dfrac y4,& 1\le y<2,\\[6pt]
1,& y\ge 2,
\end{cases}
$$
且
$$
E(Y)=\frac34.
$$

由全概率公式，
$$
F_Y(y)=P(Y\le y)
=\frac12P(Y\le y\mid X=1)+\frac12P(Y\le y\mid X=2).
$$

当 $y<0$ 时，显然 $F_Y(y)=0$。

当 $0\le y<1$ 时，
$$
P(Y\le y\mid X=1)=y,\qquad
P(Y\le y\mid X=2)=\frac y2,
$$
故
$$
F_Y(y)=\frac12y+\frac12\cdot\frac y2=\frac{3y}{4}.
$$

当 $1\le y<2$ 时，
$$
P(Y\le y\mid X=1)=1,\qquad
P(Y\le y\mid X=2)=\frac y2,
$$
故
$$
F_Y(y)=\frac12+\frac y4.
$$

当 $y\ge 2$ 时，$F_Y(y)=1$。

因此
$$
F_Y(y)=
\begin{cases}
0,& y<0,\\
\dfrac{3y}{4},& 0\le y<1,\\
\dfrac12+\dfrac y4,& 1\le y<2,\\
1,& y\ge 2.
\end{cases}
$$

进一步可得密度
$$
f_Y(y)=
\begin{cases}
\dfrac34,& 0<y<1,\\[4pt]
\dfrac14,& 1<y<2,\\[4pt]
0,& \text{其他},
\end{cases}
$$
于是
$$
E(Y)=\int_0^1 y\cdot\frac34\,dy+\int_1^2 y\cdot\frac14\,dy
=\frac38+\frac38=\frac34.
$$

### 第 23 题

- 答案：$$
\begin{array}{c|cc}
X\backslash Y & 0 & 1\\\hline
0 & \dfrac29 & \dfrac19\\
1 & \dfrac19 & \dfrac59
\end{array}
$$
且
$$
P\{X+Y\le 1\}=\frac49.
$$

设联合分布为
$$
\begin{array}{c|cc}
X\backslash Y & 0 & 1\\\hline
0 & a & b\\
1 & c & d
\end{array}.
$$
由边缘分布相同且
$$
P(X=0)=P(Y=0)=\frac13,\qquad P(X=1)=P(Y=1)=\frac23,
$$
得
$$
a+b=\frac13,\qquad a+c=\frac13,\qquad c+d=\frac23,\qquad b+d=\frac23.
$$
从而
$$
b=c,\qquad a=\frac13-b,\qquad d=\frac23-b.
$$

又
$$
EX=EY=\frac23,\qquad DX=DY=\frac23\left(1-\frac23\right)=\frac29.
$$
并且
$$
\operatorname{Cov}(X,Y)=E(XY)-EX\cdot EY=d-\frac49.
$$
由相关系数
$$
\rho_{XY}
=\frac{\operatorname{Cov}(X,Y)}{\sqrt{DX\cdot DY}}
=\frac{d-\frac49}{\frac29}
=\frac12,
$$
可得
$$
d=\frac59.
$$
于是
$$
b=c=\frac23-\frac59=\frac19,\qquad
a=\frac13-\frac19=\frac29.
$$
故联合分布为
$$
\begin{array}{c|cc}
X\backslash Y & 0 & 1\\\hline
0 & \dfrac29 & \dfrac19\\
1 & \dfrac19 & \dfrac59
\end{array}.
$$

最后
$$
P(X+Y\le 1)=1-P(X=1,Y=1)=1-\frac59=\frac49.
$$
