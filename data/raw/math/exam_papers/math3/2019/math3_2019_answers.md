# 2019 年考研数学三答案与解析

## 第 1 题

### 标准答案

C

### 解析

由麦克劳林展开式
$$
\tan x=x+\frac{x^3}{3}+o(x^3),
$$
得
$$
x-\tan x=-\frac{x^3}{3}+o(x^3).
$$
因此 $x-\tan x$ 与 $x^3$ 同阶，故 $k=3$，选 C。

## 第 2 题

### 标准答案

D

### 解析

设 $f(x)=x^5-5x+k$，则
$$
f'(x)=5x^4-5=5(x^2-1)(x^2+1).
$$
故 $f$ 在 $(-\infty,-1)$、$(1,+\infty)$ 上递增，在 $(-1,1)$ 上递减。又
$$
\lim_{x\to -\infty}f(x)=-\infty,\qquad \lim_{x\to +\infty}f(x)=+\infty.
$$
要有三个不同实根，需极大值 $f(-1)>0$ 且极小值 $f(1)<0$，即
$$
-1+5+k>0,\qquad 1-5+k<0,
$$
所以 $-4<k<4$，选 D。

## 第 3 题

### 标准答案

D

### 解析

由齐次方程通解 $(C_1+C_2x)e^{-x}$ 可知，$-1$ 是特征方程
$$
\lambda^2+a\lambda+b=0
$$
的二重根，故
$$
1-a+b=0,\qquad a^2-4b=0.
$$
又 $y=e^x$ 为非齐次方程特解，代入得
$$
1+a+b=c.
$$
解得 $a=2,b=1,c=4$，选 D。

## 第 4 题

### 标准答案

B

### 解析

因为
$$
\frac{|u_nv_n|}{|nu_n|}=\left|\frac{v_n}{n}\right|\to 0,
$$
且 $\sum nu_n$ 绝对收敛，由比较判别法可知 $\sum u_nv_n$ 绝对收敛。

而 $\sum v_n$ 的敛散性不由 $\sum v_n/n$ 条件收敛唯一确定，所以 C、D 不能保证。选 B。

## 第 5 题

### 标准答案

A

### 解析

基础解系含 2 个向量，故
$$
4-r(A)=2,\qquad r(A)=2.
$$
对 4 阶矩阵，当 $r(A)<n-1$ 时，伴随矩阵 $A^*=0$，所以 $r(A^*)=0$，选 A。

## 第 6 题

### 标准答案

C

### 解析

设 $\lambda$ 为 $A$ 的特征值。由 $A^2+A=2E$ 得
$$
\lambda^2+\lambda=2,
$$
故 $\lambda=1$ 或 $\lambda=-2$。又 $A$ 为 3 阶实对称矩阵，且三个特征值乘积为 $|A|=4$，只能为 $1,-2,-2$。正惯性指数为 1，负惯性指数为 2，规范形为
$$
y_1^2-y_2^2-y_3^2.
$$
选 C。

## 第 7 题

### 标准答案

C

### 解析

由
$$
P(A\overline B)=P(A)-P(AB),\qquad P(B\overline A)=P(B)-P(AB),
$$
可知
$$
P(A\overline B)=P(B\overline A)
\Longleftrightarrow P(A)=P(B).
$$
选 C。

## 第 8 题

### 标准答案

A

### 解析

因为 $X,Y$ 独立同分布，
$$
X-Y\sim N(0,2\sigma^2).
$$
所以
$$
P\{|X-Y|<1\}
=P\left\{\frac{|X-Y|}{\sqrt2\sigma}<\frac1{\sqrt2\sigma}\right\}
=2\Phi\left(\frac1{\sqrt2\sigma}\right)-1.
$$
该概率与 $\mu$ 无关，与 $\sigma^2$ 有关，选 A。

## 第 9 题

### 标准答案

$e^{-1}$

### 解析

利用
$$
\frac1{k(k+1)}=\frac1k-\frac1{k+1},
$$
括号内和式为
$$
1-\frac1{n+1}=\frac n{n+1}.
$$
因此
$$
\lim_{n\to\infty}\left(\frac n{n+1}\right)^n
=\lim_{n\to\infty}\left(1-\frac1{n+1}\right)^n=e^{-1}.
$$

## 第 10 题

### 标准答案

$(\pi,-2)$

### 解析

有
$$
y'=x\cos x-\sin x,\qquad y''=-x\sin x.
$$
令 $y''=0$ 得 $x=0$ 或 $x=\pi$。在 $x=0$ 左右 $y''$ 不变号，故不是拐点；在 $x=\pi$ 左右 $y''$ 变号，且
$$
y(\pi)=\pi\sin\pi+2\cos\pi=-2.
$$
所以拐点为 $(\pi,-2)$。

## 第 11 题

### 标准答案

$\dfrac1{18}(1-2\sqrt2)$

### 解析

分部积分：
$$
\int_0^1x^2f(x)\,dx
=\frac13x^3f(x)\Big|_0^1-\frac13\int_0^1x^3f'(x)\,dx.
$$
由于 $f(1)=0$，$f'(x)=\sqrt{1+x^4}$，故
$$
\int_0^1x^2f(x)\,dx
=-\frac13\int_0^1x^3\sqrt{1+x^4}\,dx.
$$
令 $u=1+x^4$，得
$$
-\frac13\cdot\frac14\int_1^2u^{1/2}\,du
=-\frac1{12}\cdot\frac23(2\sqrt2-1)
=\frac1{18}(1-2\sqrt2).
$$

## 第 12 题

### 标准答案

$0.4$

### 解析

价格弹性公式为
$$
\eta_{AA}=-\frac{P_A}{Q_A}\frac{\partial Q_A}{\partial P_A}.
$$
有
$$
\frac{\partial Q_A}{\partial P_A}=-2P_A-P_B.
$$
代入 $P_A=10,\ P_B=20$：
$$
Q_A=500-100-200+800=1000,\qquad
\frac{\partial Q_A}{\partial P_A}=-40.
$$
所以
$$
\eta_{AA}=-\frac{10}{1000}(-40)=0.4.
$$

## 第 13 题

### 标准答案

$1$

### 解析

对增广矩阵作初等行变换：
$$
\left(\begin{array}{ccc|c}
1&0&-1&0\\
1&1&-1&1\\
0&1&a^2-1&a
\end{array}\right)
\sim
\left(\begin{array}{ccc|c}
1&0&-1&0\\
0&1&0&1\\
0&0&a^2-1&a-1
\end{array}\right).
$$
要有无穷多解，需
$$
a^2-1=0,\qquad a-1=0,
$$
故 $a=1$。

## 第 14 题

### 标准答案

$\dfrac23$

### 解析

当 $0\le x<2$ 时，
$$
F(x)=\int_0^x\frac t2\,dt=\frac{x^2}{4}.
$$
又
$$
E(X)=\int_0^2x\frac x2\,dx=\frac43.
$$
因此
$$
P\{F(X)>E(X)-1\}
=P\left\{\frac{X^2}{4}>\frac13\right\}
=P\left\{X>\frac2{\sqrt3}\right\}.
$$
于是
$$
\int_{2/\sqrt3}^{2}\frac x2\,dx
=\left.\frac{x^2}{4}\right|_{2/\sqrt3}^{2}
=1-\frac13=\frac23.
$$

## 第 15 题

### 标准答案

$f'(0)$ 不存在，
$$
f'(x)=\begin{cases}
2x^{2x}(\ln x+1),&x>0,\\
e^x(x+1),&x<0.
\end{cases}
$$
极小值为 $f(-1)=1-\dfrac1e$ 和 $f(1/e)=e^{-2/e}$，极大值为 $f(0)=1$。

### 解析

当 $x>0$ 时，$x^{2x}=e^{2x\ln x}$，故
$$
f'(x)=2x^{2x}(\ln x+1).
$$
当 $x<0$ 时，
$$
f'(x)=e^x(x+1).
$$
在 $x=0$ 处，
$$
\lim_{x\to0^+}\frac{x^{2x}-1}{x}
=\lim_{x\to0^+}\frac{e^{2x\ln x}-1}{x}
=\lim_{x\to0^+}2\ln x=-\infty,
$$
所以 $f'(0)$ 不存在。

令 $f'(x)=0$，得驻点 $x=-1$、$x=1/e$。符号分析可得：$f$ 在 $(-\infty,-1)$、$(0,1/e)$ 上递减，在 $(-1,0)$、$(1/e,+\infty)$ 上递增；又 $f(0)=1$，且左右附近函数值均小于 1，所以
$$
f(-1)=1-\frac1e,\qquad f(1/e)=e^{-2/e}
$$
为极小值，$f(0)=1$ 为极大值。

## 第 16 题

### 标准答案

$$
1-3f_{uu}(x+y,x-y)-f_{vv}(x+y,x-y).
$$

### 解析

记 $u=x+y,\ v=x-y$。先求一阶偏导：
$$
g_x=y-f_u(u,v)-f_v(u,v),
$$
$$
g_y=x-f_u(u,v)+f_v(u,v).
$$
继续求二阶偏导：
$$
g_{xx}=-f_{uu}-2f_{uv}-f_{vv},
$$
$$
g_{xy}=1-f_{uu}+f_{vv},
$$
$$
g_{yy}=-f_{uu}+2f_{uv}-f_{vv}.
$$
三式相加得
$$
g_{xx}+g_{xy}+g_{yy}
=1-3f_{uu}(x+y,x-y)-f_{vv}(x+y,x-y).
$$

## 第 17 题

### 标准答案

$$
y(x)=\sqrt x\,e^{x^2/2},\qquad
V=\frac\pi2(e^4-e).
$$

### 解析

原方程为一阶线性方程。积分因子为 $e^{-x^2/2}$，于是
$$
\left(ye^{-x^2/2}\right)'=\frac1{2\sqrt x}.
$$
积分得
$$
ye^{-x^2/2}=\sqrt x+C.
$$
由 $y(1)=\sqrt e$ 得 $C=0$，故
$$
y(x)=\sqrt x\,e^{x^2/2}.
$$

旋转体体积为
$$
V=\pi\int_1^2y^2(x)\,dx
=\pi\int_1^2x e^{x^2}\,dx
=\frac\pi2e^{x^2}\Big|_1^2
=\frac\pi2(e^4-e).
$$

## 第 18 题

### 标准答案

$$
\frac{e^{\pi}+1}{2(e^{\pi}-1)}.
$$

### 解析

所求面积为
$$
S=\int_0^{+\infty}e^{-x}|\sin x|\,dx
=\sum_{n=0}^{\infty}(-1)^n\int_{n\pi}^{(n+1)\pi}e^{-x}\sin x\,dx.
$$
计算
$$
\int_{n\pi}^{(n+1)\pi}e^{-x}\sin x\,dx
=\frac{(-1)^n}{2}\left(e^{-n\pi}+e^{-(n+1)\pi}\right).
$$
故
$$
S=\frac12\sum_{n=0}^{\infty}\left(e^{-n\pi}+e^{-(n+1)\pi}\right)
=\frac12(1+e^{-\pi})\sum_{n=0}^{\infty}e^{-n\pi}
=\frac{e^{\pi}+1}{2(e^{\pi}-1)}.
$$

## 第 19 题

### 标准答案

$1$

### 解析

有
$$
a_{n+1}-a_n=\int_0^1x^n(x-1)\sqrt{1-x^2}\,dx<0,
$$
故 $\{a_n\}$ 单调递减。

当 $n\ge2$ 时分部积分：
$$
a_n=\int_0^1x^n\sqrt{1-x^2}\,dx
=-\frac13x^{n-1}(1-x^2)^{3/2}\Big|_0^1
+\frac{n-1}{3}\int_0^1x^{n-2}(1-x^2)^{3/2}\,dx.
$$
又
$$
\int_0^1x^{n-2}(1-x^2)^{3/2}\,dx
=a_{n-2}-a_n,
$$
所以
$$
a_n=\frac{n-1}{3}(a_{n-2}-a_n),
$$
即
$$
a_n=\frac{n-1}{n+2}a_{n-2}.
$$

由递推式
$$
\frac{a_n}{a_{n-1}}
=\frac{n-1}{n+2}\frac{a_{n-2}}{a_{n-1}}.
$$
因 $a_n>0$ 且单调递减，得
$$
\frac{n-1}{n+2}<\frac{a_n}{a_{n-1}}<1.
$$
夹逼得
$$
\lim_{n\to\infty}\frac{a_n}{a_{n-1}}=1.
$$

## 第 20 题

### 标准答案

$a\ne-1$。当 $a\ne1$ 且 $a\ne-1$ 时，
$$
\beta_3=\alpha_1-\alpha_2+\alpha_3.
$$
当 $a=1$ 时，
$$
\beta_3=(3-2k)\alpha_1+(k-2)\alpha_2+k\alpha_3,\qquad k\in\mathbb R.
$$

### 解析

由向量组等价定义，两组向量应能相互线性表示。分别比较
$$
r(\alpha_1,\alpha_2,\alpha_3)
$$
与加入 $\beta_1,\beta_2,\beta_3$ 后的秩，可得当 $a=-1$ 时不等价；当 $a=1$ 或 $a\ne1,-1$ 时，$\beta_1,\beta_2,\beta_3$ 均可由 $\alpha_1,\alpha_2,\alpha_3$ 线性表示。再反向检验可知等价条件为
$$
a\ne-1.
$$

设
$$
x_1\alpha_1+x_2\alpha_2+x_3\alpha_3=\beta_3.
$$
当 $a\ne1,-1$ 时，解得
$$
x_1=1,\quad x_2=-1,\quad x_3=1,
$$
故
$$
\beta_3=\alpha_1-\alpha_2+\alpha_3.
$$
当 $a=1$ 时，线性方程组有无穷多解，可取
$$
x_1=3-2k,\quad x_2=k-2,\quad x_3=k,
$$
故
$$
\beta_3=(3-2k)\alpha_1+(k-2)\alpha_2+k\alpha_3.
$$

## 第 21 题

### 标准答案

$$
x=3,\qquad y=-2,
$$
可取
$$
P=\begin{pmatrix}
1&1&1\\
-2&-1&-2\\
0&0&-4
\end{pmatrix}.
$$

### 解析

相似矩阵有相同迹和行列式，故
$$
\operatorname{tr}(A)=\operatorname{tr}(B),\qquad |A|=|B|.
$$
于是
$$
x-4=y+1,\qquad 4x-8=-2y,
$$
解得
$$
x=3,\qquad y=-2.
$$

此时 $B$ 的特征值为 $2,-1,-2$。矩阵 $A$ 对应特征值 $2,-1,-2$ 的特征向量可取
$$
\xi_1=(1,-2,0)^T,\quad
\xi_2=(-2,1,0)^T,\quad
\xi_3=(1,-2,-4)^T.
$$
矩阵 $B$ 对应特征向量可取
$$
\eta_1=(1,0,0)^T,\quad
\eta_2=(1,-3,0)^T,\quad
\eta_3=(0,0,1)^T.
$$
令 $P_1=(\xi_1,\xi_2,\xi_3)$，$P_2=(\eta_1,\eta_2,\eta_3)$，则
$$
P=P_1P_2^{-1}
=\begin{pmatrix}
1&1&1\\
-2&-1&-2\\
0&0&-4
\end{pmatrix}.
$$
于是 $P^{-1}AP=B$。

## 第 22 题

### 标准答案

$$
f_Z(z)=\begin{cases}
pe^z,&z<0,\\
(1-p)e^{-z},&z\ge0.
\end{cases}
$$
当 $p=\dfrac12$ 时 $X$ 与 $Z$ 不相关；$X$ 与 $Z$ 不相互独立。

### 解析

由全概率公式，
$$
F_Z(z)=P(XY\le z)
=pP(-X\le z)+(1-p)P(X\le z).
$$
当 $z<0$ 时，
$$
F_Z(z)=pP(X\ge -z)=pe^z;
$$
当 $z\ge0$ 时，
$$
F_Z(z)=p+(1-p)(1-e^{-z})=1-(1-p)e^{-z}.
$$
故
$$
f_Z(z)=\begin{cases}
pe^z,&z<0,\\
(1-p)e^{-z},&z\ge0.
\end{cases}
$$

又 $E(X)=1,\ D(X)=1,\ E(Y)=1-2p$，且 $X,Y$ 独立，因此
$$
\operatorname{Cov}(X,Z)
=\operatorname{Cov}(X,XY)
=E(X^2)E(Y)-E(X)E(X)E(Y)
=D(X)E(Y)=1-2p.
$$
令协方差为 0，得 $p=1/2$。

但例如
$$
P\{X\le1,\ Z\le-1\}=0,
$$
而 $P\{X\le1\}>0$ 且 $P\{Z\le-1\}>0$，故不满足独立性，$X$ 与 $Z$ 不相互独立。

## 第 23 题

### 标准答案

$$
A=\sqrt{\frac2\pi},\qquad
\widehat{\sigma^2}=\frac1n\sum_{i=1}^n(X_i-\mu)^2.
$$

### 解析

由密度积分为 1，
$$
1=\int_\mu^{+\infty}\frac A\sigma e^{-\frac{(x-\mu)^2}{2\sigma^2}}\,dx.
$$
令 $t=(x-\mu)/\sigma$，得
$$
1=A\int_0^{+\infty}e^{-t^2/2}\,dt
=A\frac{\sqrt{2\pi}}2,
$$
所以
$$
A=\sqrt{\frac2\pi}.
$$

设样本观测值为 $x_1,\ldots,x_n$。当 $x_i\ge\mu$ 全部成立时，似然函数为
$$
L(\sigma^2)=\left(\frac2\pi\right)^{n/2}(\sigma^2)^{-n/2}
\exp\left\{-\frac1{2\sigma^2}\sum_{i=1}^n(x_i-\mu)^2\right\}.
$$
对数似然为
$$
\ln L(\sigma^2)=\frac n2\ln\frac2\pi-\frac n2\ln\sigma^2
-\frac1{2\sigma^2}\sum_{i=1}^n(x_i-\mu)^2.
$$
令关于 $\sigma^2$ 的导数为 0：
$$
-\frac n{2\sigma^2}
+\frac1{2\sigma^4}\sum_{i=1}^n(x_i-\mu)^2=0,
$$
得
$$
\widehat{\sigma^2}=\frac1n\sum_{i=1}^n(X_i-\mu)^2.
$$
