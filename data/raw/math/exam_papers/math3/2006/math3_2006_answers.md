# 2006 年考研数学三答案与解析

## 第 1 题
### 标准答案

$1$

### 解析

设
$$
u_n=\left(1+\frac1n\right)^{(-1)^n}.
$$
当 $n=2k$ 时，
$$
u_{2k}=\left(1+\frac1{2k}\right)\to1;
$$
当 $n=2k-1$ 时，
$$
u_{2k-1}=\left(1+\frac1{2k-1}\right)^{-1}
=\frac{2k-1}{2k}\to1.
$$
奇、偶子列都收敛到 $1$，因此
$$
\lim_{n\to\infty}u_n=1.
$$

## 第 2 题
### 标准答案

$2e^3$

### 解析

由
$$
f'(x)=e^{f(x)}
$$
两边求导，得
$$
f''(x)=e^{f(x)}f'(x)=e^{2f(x)}.
$$
再求导，
$$
f'''(x)=2e^{2f(x)}f'(x)=2e^{3f(x)}.
$$
代入 $f(2)=1$，得到
$$
f'''(2)=2e^3.
$$

## 第 3 题
### 标准答案

$4\,dx-2\,dy$

### 解析

令
$$
u=4x^2-y^2,
$$
则
$$
dz=f'(u)\,du=f'(4x^2-y^2)(8x\,dx-2y\,dy).
$$
在点 $(1,2)$ 处，
$$
u=4\cdot1^2-2^2=0,
$$
因而
$$
dz=f'(0)(8\,dx-4\,dy)=\frac12(8\,dx-4\,dy)=4\,dx-2\,dy.
$$

## 第 4 题
### 标准答案

$2$

### 解析

由题设
$$
BA=B+2E
$$
得
$$
B(A-E)=2E.
$$
两边取行列式：
$$
|B|\cdot|A-E|=|2E|=2^2|E|=4.
$$
又
$$
A-E=\begin{pmatrix}
1 & 1\\
-1 & 1
\end{pmatrix},
\qquad |A-E|=1\cdot1-1\cdot(-1)=2.
$$
因此
$$
|B|=\frac4{|A-E|}=\frac42=2.
$$

## 第 5 题
### 标准答案

$\dfrac19$

### 解析

事件 $\{\max(X,Y)\le1\}$ 等价于 $\{X\le1,\ Y\le1\}$。

因为 $X,Y$ 独立，且都服从 $[0,3]$ 上的均匀分布，所以
$$
P(X\le1)=P(Y\le1)=\frac13.
$$
故
$$
P\{\max(X,Y)\le1\}=P(X\le1)P(Y\le1)=\frac13\cdot\frac13=\frac19.
$$

## 第 6 题
### 标准答案

$2$

### 解析

样本方差 $S^2$ 是总体方差 $D(X)$ 的无偏估计，所以
$$
ES^2=D(X).
$$
由于密度函数 $f(x)$ 为偶函数，故 $E(X)=0$。于是
$$
D(X)=E(X^2)=\int_{-\infty}^{+\infty}x^2\frac12e^{-|x|}\,dx
=\int_0^{+\infty}x^2e^{-x}\,dx.
$$
分部积分两次可得
$$
\int_0^{+\infty}x^2e^{-x}\,dx=2.
$$
因而
$$
ES^2=2.
$$

## 第 7 题
### 标准答案

C

### 解析

由条件概率定义，
$$
P(A\mid B)=\frac{P(A\cap B)}{P(B)}=1.
$$
因为 $P(B)>0$，所以
$$
P(A\cap B)=P(B),
$$
这表明 $B\subset A$（在概率意义下成立）。于是
$$
A\cup B=A,
$$
从而
$$
P(A\cup B)=P(A).
$$
故选 **C**。

## 第 8 题
### 标准答案

C

### 解析

令 $x=h^2$，则当 $h\to0$ 时有 $x\to0^+$，并且
$$
\lim_{x\to0^+}\frac{f(x)}x=1.
$$
因此
$$
\lim_{x\to0^+}f(x)=\lim_{x\to0^+}x\cdot\frac{f(x)}x=0.
$$
又因 $f$ 在 $0$ 处连续，所以
$$
f(0)=0.
$$
再看右导数：
$$
f'_+(0)=\lim_{x\to0^+}\frac{f(x)-f(0)}x
=\lim_{x\to0^+}\frac{f(x)}x=1,
$$
故右导数存在。于是选 **C**。

## 第 9 题
### 标准答案

D

### 解析

设
$$
b_n=\frac{a_n+a_{n+1}}2.
$$
则其前 $N$ 项部分和为
$$
\sum_{n=1}^N b_n
=\frac12\sum_{n=1}^N a_n+\frac12\sum_{n=1}^N a_{n+1}
=\frac12S_N+\frac12(S_{N+1}-a_1),
$$
其中 $S_N=\sum_{n=1}^N a_n$。

由于 $\sum a_n$ 收敛，所以 $S_N\to S$，且 $a_{N+1}\to0$，从而
$$
\sum_{n=1}^N b_n\to S-\frac{a_1}{2}.
$$
因此 $\sum b_n$ 必收敛，即选 **D**。

## 第 10 题
### 标准答案

B

### 解析

非齐次线性方程两个解的差满足对应的齐次方程。因为 $y_1,y_2$ 都满足
$$
y'+P(x)y=Q(x),
$$
所以
$$
(y_1-y_2)'+P(x)(y_1-y_2)=0.
$$
因而齐次方程的通解可写成
$$
C\bigl(y_1(x)-y_2(x)\bigr).
$$
再加上非齐次方程的一个特解 $y_1(x)$，得到原方程通解
$$
y=y_1(x)+C\bigl(y_1(x)-y_2(x)\bigr).
$$
故选 **B**。

## 第 11 题
### 标准答案

D

### 解析

由拉格朗日乘子法，在极值点处存在 $\lambda$ 使
$$
\begin{cases}
f_x'(x_0,y_0)+\lambda\varphi_x'(x_0,y_0)=0,\\
f_y'(x_0,y_0)+\lambda\varphi_y'(x_0,y_0)=0.
\end{cases}
$$
若 $f_x'(x_0,y_0)\ne0$，则第一式说明 $\lambda\ne0$。
又由题设 $\varphi_y'(x_0,y_0)\ne0$，第二式便推出
$$
f_y'(x_0,y_0)=-\lambda\varphi_y'(x_0,y_0)\ne0.
$$
因此选 **D**。

## 第 12 题
### 标准答案

A

### 解析

若 $a_1,a_2,\dots,a_s$ 线性相关，则存在不全为零的常数 $k_1,\dots,k_s$，使
$$
k_1a_1+k_2a_2+\cdots+k_sa_s=0.
$$
两边左乘矩阵 $A$，得到
$$
k_1Aa_1+k_2Aa_2+\cdots+k_sAa_s=0.
$$
系数 $k_1,\dots,k_s$ 仍然不全为零，因此 $Aa_1,Aa_2,\dots,Aa_s$ 线性相关。故选 **A**。

## 第 13 题
### 标准答案

B

### 解析

将 $A$ 的第 $2$ 行加到第 $1$ 行，相当于左乘初等矩阵 $P$，所以
$$
B=PA.
$$
再将 $B$ 的第 $1$ 列的 $-1$ 倍加到第 $2$ 列，相当于右乘矩阵
$$
Q=\begin{pmatrix}
1 & -1 & 0\\
0 & 1 & 0\\
0 & 0 & 1
\end{pmatrix}.
$$
注意到
$$
PQ=QP=E,
$$
故 $Q=P^{-1}$。于是
$$
C=BQ=PA\,P^{-1}.
$$
所以选 **B**。

## 第 14 题
### 标准答案

A

### 解析

标准化后，
$$
\frac{X-\mu_1}{\sigma_1}\sim N(0,1),\qquad
\frac{Y-\mu_2}{\sigma_2}\sim N(0,1).
$$
因此
$$
P\{|X-\mu_1|<1\}
=P\left\{\left|\frac{X-\mu_1}{\sigma_1}\right|<\frac1{\sigma_1}\right\}
=2\Phi\!\left(\frac1{\sigma_1}\right)-1,
$$
同理
$$
P\{|Y-\mu_2|<1\}=2\Phi\!\left(\frac1{\sigma_2}\right)-1.
$$
由于标准正态分布函数 $\Phi$ 单调递增，而题设给出前者大于后者，所以
$$
\frac1{\sigma_1}>\frac1{\sigma_2},
$$
从而
$$
\sigma_1<\sigma_2.
$$
故选 **A**。

## 第 15 题
### 标准答案

1. $g(x)=\dfrac1x-\dfrac{1-\pi x}{\arctan x}$；
2. $\displaystyle \lim_{x\to0^+}g(x)=\pi$。

### 解析

固定 $x>0$，先求 $g(x)$。

由
$$
\frac{y}{1+xy}=\frac1{x+\frac1y}\to\frac1x
$$
以及
$$
y\sin\frac{\pi x}{y}
=\pi x\cdot\frac{\sin(\pi x/y)}{\pi x/y}\to\pi x,
$$
可得
$$
g(x)=\lim_{y\to+\infty}f(x,y)
=\frac1x-\frac{1-\pi x}{\arctan x}.
$$

再求第二问。将其通分为
$$
g(x)=\frac{\arctan x-x+\pi x^2}{x\arctan x}.
$$
当 $x\to0^+$ 时分子、分母同时趋于 $0$，应用洛必达法则：
$$
\lim_{x\to0^+}g(x)
=\lim_{x\to0^+}\frac{\frac1{1+x^2}-1+2\pi x}{\arctan x+\frac{x}{1+x^2}}
=\lim_{x\to0^+}\frac{-\frac{2x}{(1+x^2)^2}+2\pi}{\frac1{1+x^2}+\frac1{(1+x^2)^2}}
=\pi.
$$

## 第 16 题
### 标准答案

$\dfrac29$

### 解析

区域 $D$ 可表示为
$$
D=\{(x,y)\mid 0\le y\le1,\ 0\le x\le y\}.
$$
因而
$$
\iint_D \sqrt{y^2-xy}\,dx\,dy
=\int_0^1\!\int_0^y \sqrt{y(y-x)}\,dx\,dy.
$$
对内层积分作代换 $u=y-x$，则 $du=-dx$，得到
$$
\int_0^y \sqrt{y(y-x)}\,dx
=\sqrt y\int_0^y \sqrt{y-x}\,dx
=\sqrt y\int_0^y \sqrt u\,du
=\frac23y^2.
$$
所以
$$
\iint_D \sqrt{y^2-xy}\,dx\,dy
=\int_0^1 \frac23y^2\,dy
=\frac23\cdot\frac13
=\frac29.
$$

## 第 17 题
### 标准答案

命题成立

### 解析

设
$$
F(x)=x\sin x+2\cos x+\pi x,\qquad 0<x<\pi.
$$
则
$$
F'(x)=\sin x+x\cos x-2\sin x+\pi=x\cos x-\sin x+\pi,
$$
$$
F''(x)=\cos x-\cos x-x\sin x=-x\sin x<0\qquad(0<x<\pi).
$$
因此 $F'(x)$ 在 $(0,\pi)$ 上严格递减。

又
$$
F'(\pi)=\pi\cos\pi-\sin\pi+\pi=-\pi+0+\pi=0,
$$
所以对任意 $0<x<\pi$，都有 $F'(x)>F'(\pi)=0$。故 $F(x)$ 在 $(0,\pi)$ 上严格递增。

由 $0<a<b<\pi$ 可知
$$
F(b)>F(a),
$$
即
$$
b\sin b+2\cos b+\pi b>a\sin a+2\cos a+\pi a.
$$
命题得证。

## 第 18 题
### 标准答案

1. $L:\ y=ax(x-1)$；
2. $a=2$。

### 解析

设曲线方程为 $y=y(x)$。题意给出
$$
y'-\frac yx=ax,\qquad y(1)=0.
$$
这是线性微分方程。其积分因子为
$$
\mu(x)=e^{\int -\frac1x\,dx}=\frac1x\qquad(x>0),
$$
因而
$$
\left(\frac yx\right)'=a.
$$
积分得
$$
\frac yx=ax+C,
\qquad
y=ax^2+Cx.
$$
由 $y(1)=0$ 得 $a+C=0$，所以 $C=-a$，从而
$$
y=ax(x-1).
$$

再求面积。直线 $y=ax$ 与曲线 $y=ax(x-1)$ 的交点满足
$$
ax=ax(x-1)\iff x(x-2)=0,
$$
即交于 $(0,0)$ 与 $(2,2a)$。所围面积为
$$
S=\int_0^2\bigl[ax-ax(x-1)\bigr]\,dx
=a\int_0^2(2x-x^2)\,dx
=a\left[x^2-\frac{x^3}{3}\right]_0^2
=\frac{4a}{3}.
$$
由 $S=\dfrac83$ 得
$$
\frac{4a}{3}=\frac83,
$$
故
$$
a=2.
$$

## 第 19 题
### 标准答案

收敛域为 $[-1,1]$，且
$$
S(x)=2x^2\arctan x-x\ln(1+x^2),\qquad -1\le x\le1.
$$

### 解析

先求收敛域。设
$$
u_n=\frac{(-1)^{n-1}x^{2n+1}}{n(2n-1)}.
$$
由比值判别法，
$$
\lim_{n\to\infty}\left|\frac{u_{n+1}}{u_n}\right|
=|x|^2.
$$
因而收敛半径为 $R=1$。

当 $x=\pm1$ 时，
$$
\left|u_n\right|=\frac1{n(2n-1)}\sim\frac1{2n^2},
$$
故级数绝对收敛。所以收敛域为
$$
[-1,1].
$$

再求和函数。利用分解
$$
\frac1{n(2n-1)}=-\frac1n+\frac2{2n-1},
$$
得
$$
S(x)
=-x\sum_{n=1}^{\infty}\frac{(-1)^{n-1}x^{2n}}n
+2x^2\sum_{n=1}^{\infty}\frac{(-1)^{n-1}x^{2n-1}}{2n-1}.
$$
在 $|x|\le1$ 上，
$$
\sum_{n=1}^{\infty}\frac{(-1)^{n-1}x^{2n}}n=\ln(1+x^2),
\qquad
\sum_{n=1}^{\infty}\frac{(-1)^{n-1}x^{2n-1}}{2n-1}=\arctan x.
$$
因而
$$
S(x)=2x^2\arctan x-x\ln(1+x^2),\qquad -1\le x\le1.
$$

## 第 20 题
### 标准答案

$\alpha_1,\alpha_2,\alpha_3,\alpha_4$ 线性相关当且仅当
$$
a=0\quad\text{或}\quad a=-10.
$$

- 当 $a=0$ 时，可取极大线性无关组 $\{\alpha_1\}$，且
  $$
  \alpha_2=2\alpha_1,\qquad \alpha_3=3\alpha_1,\qquad \alpha_4=4\alpha_1.
  $$
- 当 $a=-10$ 时，可取极大线性无关组 $\{\alpha_2,\alpha_3,\alpha_4\}$，且
  $$
  \alpha_1=-\alpha_2-\alpha_3-\alpha_4.
  $$

### 解析

设
$$
A=(\alpha_1,\alpha_2,\alpha_3,\alpha_4)
=\begin{pmatrix}
1+a & 2 & 3 & 4\\
1 & 2+a & 3 & 4\\
1 & 2 & 3+a & 4\\
1 & 2 & 3 & 4+a
\end{pmatrix}.
$$
四个向量线性相关当且仅当 $|A|=0$。

将后 3 列分别加到第 1 列，可得
$$
|A|
=(10+a)
\begin{vmatrix}
1 & 2 & 3 & 4\\
1 & 2+a & 3 & 4\\
1 & 2 & 3+a & 4\\
1 & 2 & 3 & 4+a
\end{vmatrix}.
$$
再用第 1 行分别消去后 3 行的第 1 列，得到
$$
|A|=(10+a)
\begin{vmatrix}
1 & 2 & 3 & 4\\
0 & a & 0 & 0\\
0 & 0 & a & 0\\
0 & 0 & 0 & a
\end{vmatrix}
=(10+a)a^3.
$$
因而线性相关当且仅当
$$
(10+a)a^3=0,
$$
即
$$
a=0\quad\text{或}\quad a=-10.
$$

1. 当 $a=0$ 时，
   $$
   \alpha_1=(1,1,1,1)^T,\ 
   \alpha_2=2\alpha_1,\ 
   \alpha_3=3\alpha_1,\ 
   \alpha_4=4\alpha_1.
   $$
   所以可取极大线性无关组 $\{\alpha_1\}$。

2. 当 $a=-10$ 时，
   $$
   \alpha_1=(-9,1,1,1)^T,\ 
   \alpha_2=(2,-8,2,2)^T,\ 
   \alpha_3=(3,3,-7,3)^T,\ 
   \alpha_4=(4,4,4,-6)^T.
   $$
   直接验证
   $$
   \alpha_1+\alpha_2+\alpha_3+\alpha_4=0,
   $$
   即
   $$
   \alpha_1=-\alpha_2-\alpha_3-\alpha_4.
   $$
   又 $\alpha_2,\alpha_3,\alpha_4$ 线性无关，因此可取极大线性无关组
   $$
   \{\alpha_2,\alpha_3,\alpha_4\}.
   $$

## 第 21 题
### 标准答案

1. 特征值为 $3,0,0$。其中
   $$
   \lambda=3 \text{ 的特征向量可取 } (1,1,1)^T,
   $$
   $$
   \lambda=0 \text{ 的特征向量空间为 } \operatorname{span}\{(-1,2,-1)^T,(0,-1,1)^T\}.
   $$
2. 可取
   $$
   Q=\begin{pmatrix}
   \frac1{\sqrt3} & 0 & -\frac2{\sqrt6}\\[4pt]
   \frac1{\sqrt3} & -\frac1{\sqrt2} & \frac1{\sqrt6}\\[4pt]
   \frac1{\sqrt3} & \frac1{\sqrt2} & \frac1{\sqrt6}
   \end{pmatrix},
   \qquad
   \Lambda=\operatorname{diag}(3,0,0).
   $$
3.
   $$
   A=\begin{pmatrix}
   1 & 1 & 1\\
   1 & 1 & 1\\
   1 & 1 & 1
   \end{pmatrix},
   \qquad
   \left(A-\frac32E\right)^6=\left(\frac32\right)^6E=\frac{729}{64}E.
   $$

### 解析

因为 $A\alpha_1=0,\ A\alpha_2=0$，所以 $\alpha_1,\alpha_2$ 都是 $A$ 对应于特征值 $0$ 的特征向量。
且它们线性无关，因此 $\lambda=0$ 至少是二重特征值。

又由于 $A$ 的每行元素之和都等于 $3$，所以
$$
A(1,1,1)^T=(3,3,3)^T=3(1,1,1)^T.
$$
因而 $(1,1,1)^T$ 是对应于特征值 $3$ 的特征向量。由于 $A$ 是 $3$ 阶矩阵，所以全部特征值为
$$
3,0,0.
$$

取单位特征向量
$$
\eta_1=\frac1{\sqrt3}(1,1,1)^T,\qquad
\eta_2=\frac1{\sqrt2}(0,-1,1)^T,\qquad
\eta_3=\frac1{\sqrt6}(-2,1,1)^T.
$$
三个向量两两正交，分别对应特征值 $3,0,0$。令
$$
Q=(\eta_1,\eta_2,\eta_3),
\qquad
\Lambda=\operatorname{diag}(3,0,0),
$$
则 $Q$ 为正交矩阵，且
$$
Q^TAQ=\Lambda.
$$

于是
$$
A=Q\Lambda Q^T
=3\eta_1\eta_1^T
=3\cdot\frac13
\begin{pmatrix}
1 & 1 & 1\\
1 & 1 & 1\\
1 & 1 & 1
\end{pmatrix}
=
\begin{pmatrix}
1 & 1 & 1\\
1 & 1 & 1\\
1 & 1 & 1
\end{pmatrix}.
$$

再看
$$
A-\frac32E
=Q\left(\Lambda-\frac32E\right)Q^T,
$$
其中 $\Lambda-\dfrac32E$ 的对角元为
$$
\frac32,\ -\frac32,\ -\frac32.
$$
六次方后都变成 $\left(\dfrac32\right)^6$，故
$$
\left(A-\frac32E\right)^6
=Q\operatorname{diag}\left[\left(\frac32\right)^6,\left(\frac32\right)^6,\left(\frac32\right)^6\right]Q^T
=\left(\frac32\right)^6E
=\frac{729}{64}E.
$$

## 第 22 题
### 标准答案

1.
   $$
   f_Y(y)=
   \begin{cases}
   \dfrac{3}{8\sqrt y}, & 0<y<1,\\[6pt]
   \dfrac{1}{8\sqrt y}, & 1<y<4,\\[6pt]
   0, & \text{其他}.
   \end{cases}
   $$
2.
   $$
   \operatorname{Cov}(X,Y)=\frac23.
   $$
3.
   $$
   F\!\left(-\frac12,4\right)=\frac14.
   $$

### 解析

先求 $Y=X^2$ 的分布函数。

当 $y<0$ 时，显然 $F_Y(y)=0$。

当 $0\le y<1$ 时，
$$
F_Y(y)=P(X^2\le y)=P(-\sqrt y\le X\le \sqrt y)
=\int_{-\sqrt y}^0\frac12\,dx+\int_0^{\sqrt y}\frac14\,dx
=\frac34\sqrt y.
$$

当 $1\le y<4$ 时，
$$
F_Y(y)=P(-1<X<0)+P(0\le X\le \sqrt y)
=\frac12+\frac14\sqrt y.
$$

当 $y\ge4$ 时，$F_Y(y)=1$。

因此
$$
f_Y(y)=F_Y'(y)=
\begin{cases}
\dfrac{3}{8\sqrt y}, & 0<y<1,\\[6pt]
\dfrac{1}{8\sqrt y}, & 1<y<4,\\[6pt]
0, & \text{其他}.
\end{cases}
$$

再求协方差。因为 $Y=X^2$，所以
$$
\operatorname{Cov}(X,Y)=\operatorname{Cov}(X,X^2)=E(X^3)-E(X)E(X^2).
$$
分别计算：
$$
E(X)=\int_{-1}^0 \frac{x}{2}\,dx+\int_0^2 \frac{x}{4}\,dx
=-\frac14+\frac12=\frac14,
$$
$$
E(X^2)=\int_{-1}^0 \frac{x^2}{2}\,dx+\int_0^2 \frac{x^2}{4}\,dx
=\frac16+\frac23=\frac56,
$$
$$
E(X^3)=\int_{-1}^0 \frac{x^3}{2}\,dx+\int_0^2 \frac{x^3}{4}\,dx
=-\frac18+1=\frac78.
$$
故
$$
\operatorname{Cov}(X,Y)
=\frac78-\frac14\cdot\frac56
=\frac{21-5}{24}
=\frac23.
$$

最后，
$$
F\!\left(-\frac12,4\right)
=P\left(X\le-\frac12,\ Y\le4\right).
$$
在 $X$ 的支持集 $(-1,2)$ 上恒有 $Y=X^2\le4$，因此
$$
F\!\left(-\frac12,4\right)
=P\left(-1<X\le-\frac12\right)
=\int_{-1}^{-1/2}\frac12\,dx
=\frac14.
$$

## 第 23 题
### 标准答案

$$
\hat\theta_{\text{矩}}=\frac32-\overline X,\qquad
\hat\theta_{\text{MLE}}=\frac Nn.
$$

### 解析

先求总体的一阶原点矩：
$$
E(X)=\int_0^1 x\theta\,dx+\int_1^2 x(1-\theta)\,dx
=\frac{\theta}{2}+\frac{3(1-\theta)}{2}
=\frac32-\theta.
$$
用样本均值 $\overline X$ 估计 $E(X)$，得到矩估计方程
$$
\overline X=\frac32-\theta,
$$
所以
$$
\hat\theta_{\text{矩}}=\frac32-\overline X.
$$

再求最大似然估计。若样本中有 $N$ 个落在 $(0,1)$，其余 $n-N$ 个落在 $[1,2)$，则似然函数为
$$
L(\theta)=\theta^N(1-\theta)^{n-N}.
$$
取对数得
$$
\ell(\theta)=N\ln\theta+(n-N)\ln(1-\theta).
$$
求导并令其为零：
$$
\ell'(\theta)=\frac{N}{\theta}-\frac{n-N}{1-\theta}=0.
$$
解得
$$
\hat\theta_{\text{MLE}}=\frac Nn.
$$
