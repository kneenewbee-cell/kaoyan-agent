# 2003 年考研数学三答案与解析

## 第 1 题

### 标准答案

$\lambda>2$

### 解析

先求 $f'(0)$。由定义
$$
f'(0)=\lim_{x\to 0}\frac{f(x)-f(0)}{x}
=\lim_{x\to 0}x^{\lambda-1}\cos\frac{1}{x}.
$$
要使该极限存在，必须有 $\lambda>1$，且此时 $f'(0)=0$。

当 $x\ne 0$ 时，
$$
f'(x)=\lambda x^{\lambda-1}\cos\frac{1}{x}+x^{\lambda-2}\sin\frac{1}{x}.
$$
要使 $f'(x)$ 在 $x=0$ 处连续，需要
$$
\lim_{x\to 0}f'(x)=f'(0)=0.
$$
前一项在 $\lambda>1$ 时趋于 $0$，后一项趋于 $0$ 的条件是 $\lambda>2$。因此 $\lambda$ 的取值范围为
$$
\lambda>2.
$$

## 第 2 题

### 标准答案

$4a^6$

### 解析

设切点为 $x_0$。因为曲线与 $x$ 轴相切，所以
$$
y'(x_0)=0,\qquad y(x_0)=0.
$$
由
$$
y=x^3-3a^2x+b
$$
得
$$
y'=3x^2-3a^2,
$$
故
$$
3x_0^2-3a^2=0\quad\Longrightarrow\quad x_0^2=a^2.
$$
又
$$
x_0^3-3a^2x_0+b=0
\quad\Longrightarrow\quad
b=2a^2x_0.
$$
于是
$$
b^2=4a^4x_0^2=4a^4\cdot a^2=4a^6.
$$

## 第 3 题

### 标准答案

$a^2$

### 解析

由题意，
$$
f(x)g(y-x)=a^2
$$
当且仅当
$$
0\le x\le 1,\qquad 0\le y-x\le 1.
$$
这等价于
$$
0\le x\le 1,\qquad x\le y\le x+1.
$$
因此
$$
I=\iint_D f(x)g(y-x)\,dx\,dy
=a^2\int_0^1\int_x^{x+1}dy\,dx
=a^2\int_0^1 1\,dx
=a^2.
$$

## 第 4 题

### 标准答案

$-1$

### 解析

由 $A^{-1}=B$ 可知 $AB=E$。于是
$$
\begin{aligned}
AB
&=(E-\alpha\alpha^T)\left(E+\frac{1}{a}\alpha\alpha^T\right)\\
&=E+\left(\frac{1}{a}-1\right)\alpha\alpha^T-\frac{1}{a}\alpha\alpha^T\alpha\alpha^T.
\end{aligned}
$$
又
$$
\alpha^T\alpha=a^2+a^2=2a^2,
$$
所以
$$
\alpha\alpha^T\alpha\alpha^T
=\alpha(\alpha^T\alpha)\alpha^T
=2a^2\alpha\alpha^T.
$$
故
$$
AB=E+\left(\frac{1}{a}-1-2a\right)\alpha\alpha^T.
$$
由 $AB=E$ 得
$$
\frac{1}{a}-1-2a=0
\quad\Longrightarrow\quad
2a^2+a-1=0.
$$
解得
$$
a=\frac{1}{2}\quad\text{或}\quad a=-1.
$$
又因 $a<0$，所以
$$
a=-1.
$$

## 第 5 题

### 标准答案

$0.9$

### 解析

因为
$$
Z=X-0.4,
$$
所以平移不改变方差与协方差：
$$
\operatorname{cov}(Y,Z)=\operatorname{cov}(Y,X-0.4)=\operatorname{cov}(Y,X),
$$
且
$$
D(Z)=D(X).
$$
于是
$$
\rho_{YZ}
=\frac{\operatorname{cov}(Y,Z)}{\sqrt{D(Y)}\sqrt{D(Z)}}
=\frac{\operatorname{cov}(Y,X)}{\sqrt{D(Y)}\sqrt{D(X)}}
=\rho_{YX}
=0.9.
$$

## 第 6 题

### 标准答案

$\dfrac{1}{2}$

### 解析

由大数定律，
$$
Y_n=\frac{1}{n}\sum_{i=1}^n X_i^2 \xrightarrow{P} E(X^2).
$$
对参数为 $2$ 的指数分布，有
$$
E(X)=\frac{1}{2},\qquad D(X)=\frac{1}{4}.
$$
因此
$$
E(X^2)=D(X)+[E(X)]^2=\frac{1}{4}+\frac{1}{4}=\frac{1}{2}.
$$
故
$$
Y_n\xrightarrow{P}\frac{1}{2}.
$$

## 第 7 题

### 标准答案

（D）

### 解析

因为 $f(x)$ 是奇函数，所以
$$
f(0)=0.
$$
对 $x\ne 0$，
$$
g(x)=\frac{f(x)}{x}=\frac{f(x)-f(0)}{x-0}.
$$
由 $f'(0)$ 存在可得
$$
\lim_{x\to 0}g(x)=\lim_{x\to 0}\frac{f(x)-f(0)}{x-0}=f'(0).
$$
故 $g(x)$ 在 $x=0$ 附近的左右极限都存在且相等，但题目中的 $g(0)$ 未定义，因此 $x=0$ 是可去间断点。

所以选
$$
\text{（D）}.
$$

## 第 8 题

### 标准答案

（A）

### 解析

令
$$
\varphi(y)=f(x_0,y).
$$
因为 $f(x,y)$ 在点 $(x_0,y_0)$ 取得极小值，所以单变量函数 $\varphi(y)$ 在 $y=y_0$ 处也取得极小值。

又由于 $f$ 可微，故 $\varphi$ 在 $y_0$ 处可导，于是由单变量函数取极值的必要条件可知
$$
\varphi'(y_0)=0.
$$
而
$$
\varphi'(y_0)=\frac{\partial f}{\partial y}(x_0,y_0),
$$
即 $f(x_0,y)$ 在 $y=y_0$ 处的导数等于零。

因此正确选项为
$$
\text{（A）}.
$$

## 第 9 题

### 标准答案

（B）

### 解析

由定义，
$$
p_n=\frac{a_n+\lvert a_n\rvert}{2},\qquad q_n=\frac{a_n-\lvert a_n\rvert}{2}.
$$
若 $\sum_{n=1}^{\infty}a_n$ 绝对收敛，则
$$
\sum_{n=1}^{\infty}\lvert a_n\rvert
$$
也收敛。于是
$$
\sum_{n=1}^{\infty}p_n
=\frac{1}{2}\sum_{n=1}^{\infty}a_n+\frac{1}{2}\sum_{n=1}^{\infty}\lvert a_n\rvert,
$$
$$
\sum_{n=1}^{\infty}q_n
=\frac{1}{2}\sum_{n=1}^{\infty}a_n-\frac{1}{2}\sum_{n=1}^{\infty}\lvert a_n\rvert
$$
都收敛。

因此正确选项为
$$
\text{（B）}.
$$

## 第 10 题

### 标准答案

（C）

### 解析

已知 $A$ 的伴随矩阵秩为 $1$，对三阶矩阵来说这等价于
$$
r(A)=2.
$$
先求行列式：
$$
\det(A)=
\begin{vmatrix}
a & b & b\\
b & a & b\\
b & b & a
\end{vmatrix}
=(a-b)^2(a+2b).
$$
由于 $r(A)=2$，必有
$$
\det(A)=0,
$$
即
$$
(a-b)^2(a+2b)=0.
$$
所以
$$
a=b\quad\text{或}\quad a+2b=0.
$$
但若 $a=b$，则
$$
A=\begin{pmatrix}
a & a & a\\
a & a & a\\
a & a & a
\end{pmatrix}
$$
三行完全相同，秩至多为 $1$，与 $r(A)=2$ 矛盾。

因此必有
$$
a\ne b,\qquad a+2b=0,
$$
故选
$$
\text{（C）}.
$$

## 第 11 题

### 标准答案

（B）

### 解析

若向量组 $\alpha_1,\alpha_2,\cdots,\alpha_s$ 线性相关，只能推出存在一组不全为零的数 $k_1,k_2,\cdots,k_s$，使得
$$
k_1\alpha_1+k_2\alpha_2+\cdots+k_s\alpha_s=0.
$$
并不能推出“对于任意一组不全为零的数”都成立。因此（B）错误。

其余选项都正确：

- （A）正是线性无关定义的等价表述；
- （C）向量组线性无关当且仅当该向量组的秩等于向量个数 $s$；
- （D）若向量组线性无关，则任意部分组也线性无关，特别地任意两个向量线性无关。

所以不正确的结论是
$$
\text{（B）}.
$$

## 第 12 题

### 标准答案

（C）

### 解析

样本空间为
$$
\{HH,HT,TH,TT\},
$$
每个样本点概率都为 $\dfrac{1}{4}$。因此
$$
P(A_1)=P(A_2)=P(A_3)=\frac{1}{2},\qquad P(A_4)=\frac{1}{4}.
$$

又有
$$
P(A_1A_2)=P(\{HH\})=\frac{1}{4}=P(A_1)P(A_2),
$$
$$
P(A_1A_3)=P(\{HT\})=\frac{1}{4}=P(A_1)P(A_3),
$$
$$
P(A_2A_3)=P(\{TH\})=\frac{1}{4}=P(A_2)P(A_3).
$$
所以 $A_1,A_2,A_3$ 两两独立。

但
$$
A_1A_2A_3=\varnothing,
$$
故
$$
P(A_1A_2A_3)=0\ne \frac{1}{8}=P(A_1)P(A_2)P(A_3).
$$
因此它们不相互独立。

所以正确选项为
$$
\text{（C）}.
$$

## 第 13 题

### 标准答案

$f(1)=\dfrac{1}{\pi}$

### 解析

要使 $f(x)$ 在 $\left[\dfrac{1}{2},1\right]$ 上连续，只需令
$$
f(1)=\lim_{x\to 1^-}\left(\frac{1}{\pi x}+\frac{1}{\sin \pi x}-\frac{1}{\pi(1-x)}\right).
$$
注意到
$$
\sin \pi x \sim \pi(1-x)\qquad (x\to 1^-),
$$
故
$$
\frac{1}{\sin \pi x}-\frac{1}{\pi(1-x)}\to 0.
$$
同时
$$
\frac{1}{\pi x}\to \frac{1}{\pi}.
$$
因此
$$
\lim_{x\to 1^-}f(x)=\frac{1}{\pi}.
$$
所以应定义
$$
f(1)=\frac{1}{\pi}.
$$

## 第 14 题

### 标准答案

$x^2+y^2$

### 解析

设
$$
u=xy,\qquad v=\frac{x^2-y^2}{2},
$$
则
$$
g(x,y)=f(u,v).
$$
由链式法则，
$$
g_x=f_u u_x+f_v v_x=yf_u+xf_v,
$$
$$
g_y=f_u u_y+f_v v_y=xf_u-yf_v.
$$
再求二阶偏导：
$$
g_{xx}=y^2f_{uu}+2xyf_{uv}+x^2f_{vv}+f_v,
$$
$$
g_{yy}=x^2f_{uu}-2xyf_{uv}+y^2f_{vv}-f_v.
$$
两式相加得
$$
g_{xx}+g_{yy}
=(x^2+y^2)(f_{uu}+f_{vv}).
$$
又已知
$$
f_{uu}+f_{vv}=1,
$$
故
$$
g_{xx}+g_{yy}=x^2+y^2.
$$

## 第 15 题

### 标准答案

$\dfrac{\pi}{2}(1+e^\pi)$

### 解析

将积分化为极坐标：
$$
x=r\cos\theta,\qquad y=r\sin\theta,
$$
其中
$$
0\le r\le \sqrt{\pi},\qquad 0\le \theta\le 2\pi.
$$
于是
$$
\begin{aligned}
I
&=\iint_D e^{-(x^2+y^2-\pi)}\sin(x^2+y^2)\,dx\,dy\\
&=e^\pi\int_0^{2\pi}\int_0^{\sqrt{\pi}} e^{-r^2}\sin(r^2)\,r\,dr\,d\theta\\
&=2\pi e^\pi\int_0^{\sqrt{\pi}} e^{-r^2}\sin(r^2)\,r\,dr.
\end{aligned}
$$
令 $t=r^2$，则 $dt=2r\,dr$，得
$$
I=\pi e^\pi\int_0^\pi e^{-t}\sin t\,dt.
$$
又
$$
\int e^{-t}\sin t\,dt=-\frac{1}{2}e^{-t}(\sin t+\cos t)+C,
$$
所以
$$
\int_0^\pi e^{-t}\sin t\,dt
=\frac{1+e^{-\pi}}{2}.
$$
因此
$$
I=\pi e^\pi\cdot \frac{1+e^{-\pi}}{2}
=\frac{\pi}{2}(1+e^\pi).
$$

## 第 16 题

### 标准答案

$$
f(x)=1-\frac{1}{2}\ln(1+x^2)\qquad (|x|<1),
$$
并且 $f(x)$ 在 $x=0$ 处取得极大值 $1$，无极小值。

### 解析

设
$$
f(x)=1+\sum_{n=1}^{\infty}(-1)^n\frac{x^{2n}}{2n}\qquad (|x|<1).
$$
逐项求导得
$$
f'(x)=\sum_{n=1}^{\infty}(-1)^n x^{2n-1}
=-x\sum_{n=0}^{\infty}(-x^2)^n
=-\frac{x}{1+x^2}.
$$
由 $f(0)=1$，对上式从 $0$ 到 $x$ 积分：
$$
f(x)-1=-\int_0^x \frac{t}{1+t^2}\,dt
=-\frac{1}{2}\ln(1+x^2).
$$
故
$$
f(x)=1-\frac{1}{2}\ln(1+x^2)\qquad (|x|<1).
$$

再由
$$
f'(x)=-\frac{x}{1+x^2}
$$
知唯一驻点为 $x=0$。当 $x<0$ 时，$f'(x)>0$；当 $x>0$ 时，$f'(x)<0$，所以 $f(x)$ 在 $x=0$ 处取得极大值
$$
f(0)=1.
$$
由于定义域是开区间 $(-1,1)$，且 $f(x)$ 在两侧单调下降，不取得极小值。

## 第 17 题

### 标准答案

（A）$F'(x)+2F(x)=4e^{2x}$；

（B）$F(x)=e^{2x}-e^{-2x}$。

### 解析

由 $F(x)=f(x)g(x)$ 得
$$
F'(x)=f'(x)g(x)+f(x)g'(x)=g^2(x)+f^2(x).
$$
又因为
$$
f(x)+g(x)=2e^x,
$$
所以
$$
f^2(x)+g^2(x)=[f(x)+g(x)]^2-2f(x)g(x)=4e^{2x}-2F(x).
$$
故
$$
F'(x)+2F(x)=4e^{2x}.
$$
这就是所求的一阶线性微分方程。

再解方程：
$$
F'(x)+2F(x)=4e^{2x}.
$$
其通解为
$$
F(x)=e^{-2x}\left(\int 4e^{4x}\,dx+C\right)=e^{2x}+Ce^{-2x}.
$$
由 $f(0)=0$ 且 $f(0)+g(0)=2$ 得 $g(0)=2$，所以
$$
F(0)=f(0)g(0)=0.
$$
代入得
$$
0=1+C\quad\Longrightarrow\quad C=-1.
$$
故
$$
F(x)=e^{2x}-e^{-2x}.
$$

## 第 18 题

### 标准答案

必存在 $\xi\in(0,3)$，使 $f'(\xi)=0$。

### 解析

因为 $f(x)$ 在 $[0,2]$ 上连续，所以在 $[0,2]$ 上能取到最大值 $M$ 和最小值 $m$。于是
$$
m\le f(0),\quad m\le f(1),\quad m\le f(2),
$$
$$
f(0)\le M,\quad f(1)\le M,\quad f(2)\le M.
$$
从而
$$
m\le \frac{f(0)+f(1)+f(2)}{3}\le M.
$$
由题设 $f(0)+f(1)+f(2)=3$，得
$$
\frac{f(0)+f(1)+f(2)}{3}=1.
$$
于是
$$
m\le 1\le M.
$$
由介值定理，存在 $c\in[0,2]$，使
$$
f(c)=1.
$$
又已知
$$
f(3)=1,
$$
故
$$
f(c)=f(3).
$$
由于 $f(x)$ 在 $[c,3]$ 上连续、在 $(c,3)$ 内可导，根据罗尔定理，存在
$$
\xi\in(c,3)\subset(0,3)
$$
使得
$$
f'(\xi)=0.
$$

## 第 19 题

### 标准答案

（A）方程组仅有零解，当且仅当
$$
b\ne 0,\qquad b+\sum_{i=1}^n a_i\ne 0.
$$

（B）方程组有非零解，当且仅当
$$
b=0
\quad\text{或}\quad
b=-\sum_{i=1}^n a_i.
$$

当 $b=0$ 时，方程组等价于
$$
a_1x_1+a_2x_2+\cdots+a_nx_n=0.
$$
若不妨设 $a_1\ne 0$，则一个基础解系可取
$$
\alpha_1=\left(-\frac{a_2}{a_1},1,0,\cdots,0\right)^T,
\alpha_2=\left(-\frac{a_3}{a_1},0,1,\cdots,0\right)^T,
\cdots,
\alpha_{n-1}=\left(-\frac{a_n}{a_1},0,0,\cdots,1\right)^T.
$$

当
$$
b=-\sum_{i=1}^n a_i
$$
时，一个基础解系可取
$$
\alpha=(1,1,\cdots,1)^T.
$$

### 解析

该方程组的系数矩阵为
$$
A=
\begin{pmatrix}
a_1+b & a_2 & a_3 & \cdots & a_n\\
a_1 & a_2+b & a_3 & \cdots & a_n\\
a_1 & a_2 & a_3+b & \cdots & a_n\\
\vdots & \vdots & \vdots & \ddots & \vdots\\
a_1 & a_2 & a_3 & \cdots & a_n+b
\end{pmatrix}.
$$
它可写成
$$
A=bI+\mathbf{1}(a_1,a_2,\cdots,a_n),
$$
其中 $\mathbf{1}=(1,1,\cdots,1)^T$。由行列式公式可得
$$
\det(A)=b^{\,n-1}\left(b+\sum_{i=1}^n a_i\right).
$$

因此：

1. 当
   $$
   b\ne 0,\qquad b+\sum_{i=1}^n a_i\ne 0
   $$
   时，$\det(A)\ne 0$，故方程组仅有零解。

2. 当 $b=0$ 时，所有方程相同，化为
   $$
   a_1x_1+a_2x_2+\cdots+a_nx_n=0.
   $$
   因为 $\sum_{i=1}^n a_i\ne 0$，所以 $a_1,\cdots,a_n$ 不全为零，方程组有非零解。若不妨设 $a_1\ne 0$，即可写出上面的基础解系。

3. 当
   $$
   b=-\sum_{i=1}^n a_i
   $$
   时，
   $$
   A(1,1,\cdots,1)^T=0,
   $$
   所以方程组有非零解。又此时 $\det(A)=0$ 且 $b\ne 0$，矩阵秩为 $n-1$，故解空间维数为 $1$，基础解系可取
   $$
   \{(1,1,\cdots,1)^T\}.
   $$

综上得到题目所要求的全部结论。

## 第 20 题

### 标准答案

（A）
$$
a=1,\qquad b=2.
$$

（B）在正交变换 $X=QY$ 下，可化为标准形
$$
f=2y_1^2+2y_2^2-3y_3^2,
$$
其中可取
$$
Q=
\begin{pmatrix}
\dfrac{2}{\sqrt{5}} & 0 & \dfrac{1}{\sqrt{5}}\\[4pt]
0 & 1 & 0\\[4pt]
\dfrac{1}{\sqrt{5}} & 0 & -\dfrac{2}{\sqrt{5}}
\end{pmatrix}.
$$

### 解析

二次型矩阵为
$$
A=
\begin{pmatrix}
a & 0 & b\\
0 & 2 & 0\\
b & 0 & -2
\end{pmatrix}.
$$

由特征值之和等于迹，得
$$
a+2+(-2)=1,
$$
所以
$$
a=1.
$$

又由特征值之积等于行列式，得
$$
\det(A)=
\begin{vmatrix}
1 & 0 & b\\
0 & 2 & 0\\
b & 0 & -2
\end{vmatrix}
=-4-2b^2=-12.
$$
因此
$$
b^2=4.
$$
又因 $b>0$，故
$$
b=2.
$$

此时
$$
A=
\begin{pmatrix}
1 & 0 & 2\\
0 & 2 & 0\\
2 & 0 & -2
\end{pmatrix}.
$$
其特征多项式为
$$
\det(\lambda E-A)
=(\lambda-2)^2(\lambda+3).
$$
故特征值为
$$
\lambda_1=2,\qquad \lambda_2=2,\qquad \lambda_3=-3.
$$

对 $\lambda=2$，解
$$
(2E-A)x=0
$$
可得两个线性无关特征向量
$$
\xi_1=(2,0,1)^T,\qquad \xi_2=(0,1,0)^T.
$$
对 $\lambda=-3$，解
$$
(-3E-A)x=0
$$
可得特征向量
$$
\xi_3=(1,0,-2)^T.
$$
将它们单位化：
$$
\eta_1=\left(\frac{2}{\sqrt{5}},0,\frac{1}{\sqrt{5}}\right)^T,\qquad
\eta_2=(0,1,0)^T,\qquad
\eta_3=\left(\frac{1}{\sqrt{5}},0,-\frac{2}{\sqrt{5}}\right)^T.
$$
取正交矩阵
$$
Q=[\eta_1,\eta_2,\eta_3]
=
\begin{pmatrix}
\dfrac{2}{\sqrt{5}} & 0 & \dfrac{1}{\sqrt{5}}\\[4pt]
0 & 1 & 0\\[4pt]
\dfrac{1}{\sqrt{5}} & 0 & -\dfrac{2}{\sqrt{5}}
\end{pmatrix},
$$
则
$$
Q^TAQ=
\begin{pmatrix}
2 & 0 & 0\\
0 & 2 & 0\\
0 & 0 & -3
\end{pmatrix}.
$$
因此在正交变换 $X=QY$ 下，
$$
f=2y_1^2+2y_2^2-3y_3^2.
$$

## 第 21 题

### 标准答案

随机变量 $Y=F(X)$ 的分布函数为
$$
G(y)=
\begin{cases}
0, & y<0,\\
y, & 0\le y<1,\\
1, & y\ge 1.
\end{cases}
$$

### 解析

先求 $X$ 的分布函数。由密度
$$
f(x)=\frac{1}{3\sqrt[3]{x^2}}=\frac{1}{3x^{2/3}}\qquad (x\in[1,8])
$$
可得：

- 当 $x<1$ 时，$F(x)=0$；
- 当 $1\le x\le 8$ 时，
  $$
  F(x)=\int_1^x \frac{1}{3t^{2/3}}\,dt
  =\left[t^{1/3}\right]_1^x
  =x^{1/3}-1;
  $$
- 当 $x>8$ 时，$F(x)=1$。

设 $G(y)$ 为 $Y=F(X)$ 的分布函数。显然
$$
G(y)=0\quad (y<0),\qquad G(y)=1\quad (y\ge 1).
$$

当 $0\le y<1$ 时，
$$
\begin{aligned}
G(y)
&=P(Y\le y)=P(F(X)\le y)\\
&=P(X^{1/3}-1\le y)\\
&=P(X\le (y+1)^3)\\
&=F((y+1)^3)\\
&=(y+1)-1=y.
\end{aligned}
$$
故
$$
G(y)=
\begin{cases}
0, & y<0,\\
y, & 0\le y<1,\\
1, & y\ge 1.
\end{cases}
$$

## 第 22 题

### 标准答案

$$
g(u)=0.3\,f(u-1)+0.7\,f(u-2).
$$

### 解析

设 $F(y)$ 是随机变量 $Y$ 的分布函数，则由全概率公式，
$$
\begin{aligned}
G(u)
&=P(U\le u)\\
&=P(X+Y\le u)\\
&=0.3\,P(X+Y\le u\mid X=1)+0.7\,P(X+Y\le u\mid X=2).
\end{aligned}
$$
由于 $X$ 与 $Y$ 独立，
$$
P(X+Y\le u\mid X=1)=P(Y\le u-1)=F(u-1),
$$
$$
P(X+Y\le u\mid X=2)=P(Y\le u-2)=F(u-2).
$$
因此
$$
G(u)=0.3\,F(u-1)+0.7\,F(u-2).
$$
对 $u$ 求导即可得到 $U$ 的概率密度：
$$
g(u)=G'(u)=0.3\,f(u-1)+0.7\,f(u-2).
$$
