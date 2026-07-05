# Math 1 2009 Answers

资料类型：考研数学一答案解析
年份：2009
科目：数学一
整理状态：已按题干与答案页图像核对并清洗整理

## 答案速查

| 题号 | 题型 | 答案 |
|---|---|---|
| 1 | 选择题 | A |
| 2 | 选择题 | A |
| 3 | 选择题 | D |
| 4 | 选择题 | C |
| 5 | 选择题 | A |
| 6 | 选择题 | B |
| 7 | 选择题 | C |
| 8 | 选择题 | B |
| 9 | 填空题 | $\displaystyle x f_{12}^{\prime\prime}(x,xy)+f_2^\prime(x,xy)+xy f_{22}^{\prime\prime}(x,xy)$ |
| 10 | 填空题 | $\displaystyle y=-xe^x+x+2$ |
| 11 | 填空题 | $\displaystyle \frac{13}{6}$ |
| 12 | 填空题 | $\displaystyle \frac{4\pi}{15}$ |
| 13 | 填空题 | $2$ |
| 14 | 填空题 | $-1$ |
| 15 | 解答题 | 极小值 $\displaystyle f\left(0,\frac{1}{e}\right)=-\frac{1}{e}$，无极大值。 |
| 16 | 解答题 | $\displaystyle S_1=\frac{1}{2},\quad S_2=1-\ln 2$ |
| 17 | 解答题 | （1）$\displaystyle S_1:\frac{x^2}{4}+\frac{y^2+z^2}{3}=1$，$\displaystyle S_2:y^2+z^2=\frac{(x-4)^2}{4}$；（2）$\displaystyle V=\pi$。 |
| 18 | 解答题 | 证明见解析。 |
| 19 | 解答题 | $\displaystyle I=4\pi$ |
| 20 | 解答题 | $\displaystyle \xi_2=\begin{pmatrix}-\frac{1}{2}+\frac{k}{2}\\ \frac{1}{2}-\frac{k}{2}\\ k\end{pmatrix}$，$\displaystyle \xi_3=\begin{pmatrix}-\frac{1}{2}-s\\ s\\ t\end{pmatrix}$，其中 $k,s,t\in\mathbb{R}$；且任取这样的 $\xi_2,\xi_3$，$\xi_1,\xi_2,\xi_3$ 线性无关。 |
| 21 | 解答题 | （1）特征值为 $a,\ a+1,\ a-2$；（2）$a=2$。 |
| 22 | 解答题 | （1）$\displaystyle P\{X=1\mid Z=0\}=\frac{4}{9}$；（2）记 $p_{ij}=P\{X=i,Y=j\}$，则 $p_{00}=\frac{1}{4},p_{01}=\frac{1}{3},p_{02}=\frac{1}{9},p_{10}=\frac{1}{6},p_{11}=\frac{1}{9},p_{12}=0,p_{20}=\frac{1}{36},p_{21}=0,p_{22}=0$。 |
| 23 | 解答题 | 矩估计量与最大似然估计量均为 $\displaystyle \hat\lambda=\frac{2}{\bar X}$。 |

## 详细解析

### 第 1 题
**答案：** A

由等价无穷小可知
$$
\lim_{x\to 0}\frac{x-\sin(ax)}{x^2\ln(1-bx)}=1.
$$
若 $a\ne 1$，则 $x-\sin(ax)\sim (1-a)x$，而 $x^2\ln(1-bx)\sim -bx^3$，两者阶数不同，不可能等价，所以 $a=1$。此时
$$
x-\sin x\sim \frac{x^3}{6},\qquad x^2\ln(1-bx)\sim -bx^3.
$$
于是 $-b=\frac{1}{6}$，即 $b=-\frac{1}{6}$，选 A。
### 第 2 题
**答案：** A

令被积函数 $z=y\cos x$。它关于 $y$ 为奇函数，关于 $x$ 为偶函数。区域 $D_2,D_4$ 关于 $x$ 轴对称，因此
$$
I_2=I_4=0.
$$
上方区域 $D_1$ 上 $y\ge 0$，且 $\cos x>0$，所以 $I_1>0$；下方区域 $D_3$ 上 $y\le 0$，所以 $I_3<0$。更具体地，
$$
I_1=2\int_0^1\int_0^y y\cos x\,dx\,dy=2\int_0^1 y\sin y\,dy>0,
$$
而 $I_3<0$。故最大者为 $I_1$，选 A。
### 第 3 题
**答案：** D

由题图可读出：在 $[-1,0)$ 上 $f(x)=1$，在 $[0,2]$ 上记为 $g(x)$，且 $g(0)=-1,g(1)=0,g(2)=2$，在 $(2,3]$ 上 $f(x)=0$。设
$$
F(x)=\int_0^x f(t)\,dt.
$$
当 $-1\le x<0$ 时，
$$
F(x)=\int_0^x f(t)\,dt=-\int_x^0 1\,dt=x<0,
$$
可排除 A、C。又当 $2<x\le 3$ 时，
$$
F(x)=\int_0^2 g(t)\,dt,
$$
由图形面积可知该值为正，并且此后保持常数。符合这些特征的只有 D。
### 第 4 题
**答案：** C

先用反例排除错误选项。取
$$
a_n=b_n=\frac{(-1)^n}{\sqrt{n}},
$$
则 $a_n\to 0$，$\sum b_n$ 收敛，但
$$
\sum a_nb_n=\sum \frac{1}{n}
$$
发散，排除 A；同时 $\sum |b_n|$ 发散，而 $\sum a_n^2b_n^2=\sum \frac{1}{n^2}$ 收敛，排除 D。再取
$$
a_n=b_n=\frac{1}{n},
$$
则 $\sum b_n$ 发散，但 $\sum a_nb_n=\sum \frac{1}{n^2}$ 收敛，排除 B。

若 $\sum |b_n|$ 收敛，则 $b_n\to 0$；又 $a_n\to 0$，所以充分大的 $n$ 有 $a_n^2|b_n|\le 1$，从而
$$
0\le a_n^2b_n^2\le |b_n|.
$$
由比较判别法，$\sum a_n^2b_n^2$ 收敛，故 C 正确。
### 第 5 题
**答案：** A

记
$$
E=(\alpha_1,\alpha_2,\alpha_3),\qquad B=\left(\alpha_1,\frac{1}{2}\alpha_2,\frac{1}{3}\alpha_3\right).
$$
则
$$
B=E\begin{pmatrix}1&0&0\\0&\frac{1}{2}&0\\0&0&\frac{1}{3}\end{pmatrix},
\qquad
E=B\begin{pmatrix}1&0&0\\0&2&0\\0&0&3\end{pmatrix}.
$$
又
$$
(\alpha_1+\alpha_2,\alpha_2+\alpha_3,\alpha_3+\alpha_1)
=E\begin{pmatrix}1&0&1\\1&1&0\\0&1&1\end{pmatrix}.
$$
因此新基在基 $B$ 下的坐标矩阵为
$$
\begin{pmatrix}1&0&0\\0&2&0\\0&0&3\end{pmatrix}
\begin{pmatrix}1&0&1\\1&1&0\\0&1&1\end{pmatrix}
=
\begin{pmatrix}1&0&1\\2&2&0\\0&3&3\end{pmatrix}.
$$
按题目约定，这就是所求过渡矩阵，选 A。
### 第 6 题
**答案：** B

设
$$
M=\begin{pmatrix}O&A\\B&O\end{pmatrix}.
$$
由 $\det A=2, \det B=3$ 知 $A,B$ 可逆，且
$$
A^*=\det AA^{-1}=2A^{-1},\qquad B^*=\det BB^{-1}=3B^{-1}.
$$
矩阵 $M$ 的逆矩阵为
$$
M^{-1}=\begin{pmatrix}O&B^{-1}\\A^{-1}&O\end{pmatrix},
$$
并且 $\det M=\det A\det B=6$。所以
$$
M^*=\det MM^{-1}
=\begin{pmatrix}O&6B^{-1}\\6A^{-1}&O\end{pmatrix}
=\begin{pmatrix}O&2B^*\\3A^*&O\end{pmatrix}.
$$
选 B。
### 第 7 题
**答案：** C

由
$$
F(x)=0.3\Phi(x)+0.7\Phi\left(\frac{x-1}{2}\right)
$$
可知 $X$ 可看成以概率 $0.3$ 取标准正态分布 $N(0,1)$，以概率 $0.7$ 取正态分布 $N(1,4)$ 的混合分布。因此
$$
E(X)=0.3\cdot 0+0.7\cdot 1=0.7.
$$
选 C。
### 第 8 题
**答案：** B

因为 $X,Y$ 相互独立，且 $P\{Y=0\}=P\{Y=1\}=\frac{1}{2}$，所以
$$
F_Z(z)=P\{XY\le z\}=\frac{1}{2}P\{0\le z\}+\frac{1}{2}P\{X\le z\}.
$$
当 $z<0$ 时，$P\{0\le z\}=0$，故
$$
F_Z(z)=\frac{1}{2}\Phi(z).
$$
当 $z\ge 0$ 时，$P\{0\le z\}=1$，故
$$
F_Z(z)=\frac{1}{2}\left(1+\Phi(z)\right).
$$
函数只在 $z=0$ 处发生跳跃，因此间断点个数为 $1$，选 B。
### 第 9 题
**答案：** $\displaystyle x f_{12}^{\prime\prime}(x,xy)+f_2^\prime(x,xy)+xy f_{22}^{\prime\prime}(x,xy)$

记 $u=x, v=xy$，且 $f_i, f_{ij}$ 均在 $(x,xy)$ 处取值。先对 $x$ 求偏导：
$$
\frac{\partial z}{\partial x}=f_1+yf_2.
$$
再对 $y$ 求偏导，得
$$
\frac{\partial^2 z}{\partial x\partial y}
=x f_{12}+f_2+xy f_{22}.
$$
因此答案为
$$
x f_{12}^{\prime\prime}(x,xy)+f_2^\prime(x,xy)+xy f_{22}^{\prime\prime}(x,xy).
$$
### 第 10 题
**答案：** $\displaystyle y=-xe^x+x+2$

齐次方程通解为
$$
y=(C_1+C_2x)e^x,
$$
故特征根为二重根 $r=1$，于是 $a=-2,b=1$，非齐次方程为
$$
y''-2y'+y=x.
$$
设特解 $y^*=Ax+B$，代入得
$$
-2A+Ax+B=x,
$$
所以 $A=1,B=2$，即 $y^*=x+2$。通解为
$$
y=(C_1+C_2x)e^x+x+2.
$$
由 $y(0)=2$ 得 $C_1=0$；再由 $y'(0)=0$ 得 $C_2=-1$。因此
$$
y=-xe^x+x+2.
$$
### 第 11 题
**答案：** $\displaystyle \frac{13}{6}$

曲线 $L$ 可参数化为 $x=x, y=x^2, 0\le x\le \sqrt{2}$，于是
$$
ds=\sqrt{1+4x^2}\,dx.
$$
所以
$$
\int_L x\,ds
=\int_0^{\sqrt{2}}x\sqrt{1+4x^2}\,dx
=\frac{1}{8}\int_1^9 u^{\frac{1}{2}}\,du
=\frac{1}{12}\left(9^{\frac{3}{2}}-1\right)
=\frac{13}{6}.
$$
### 第 12 题
**答案：** $\displaystyle \frac{4\pi}{15}$

由单位球的对称性，
$$
\iiint_\Omega x^2\,dV=\iiint_\Omega y^2\,dV=\iiint_\Omega z^2\,dV.
$$
因此
$$
\iiint_\Omega z^2\,dV
=\frac{1}{3}\iiint_\Omega (x^2+y^2+z^2)\,dV.
$$
在球坐标下，
$$
\iiint_\Omega (x^2+y^2+z^2)\,dV
=\int_0^{2\pi}\int_0^\pi\int_0^1 r^4\sin\varphi\,dr\,d\varphi\,d\theta
=\frac{4\pi}{5}.
$$
故所求积分为
$$
\frac{1}{3}\cdot\frac{4\pi}{5}=\frac{4\pi}{15}.
$$
### 第 13 题
**答案：** $2$

设 $\lambda$ 是矩阵 $\beta\alpha^T$ 的非零特征值，$\eta$ 是对应特征向量，则
$$
\beta\alpha^T\eta=\lambda\eta.
$$
因为 $\lambda\ne0$，所以 $\alpha^T\eta\ne0$，并且 $\eta$ 必与 $\beta$ 同方向。设 $\eta=c\beta$，则
$$
\beta\alpha^T(c\beta)=c(\alpha^T\beta)\beta=2c\beta.
$$
因此非零特征值为 $2$。
### 第 14 题
**答案：** $-1$

因为 $\bar X+kS^2$ 是 $np^2$ 的无偏估计量，所以
$$
E(\bar X+kS^2)=np^2.
$$
对总体 $B(n,p)$，有
$$
E\bar X=EX=np,
\qquad
E(S^2)=DX=np(1-p),
$$
其中 $S^2$ 为样本方差。因此
$$
np+k\,np(1-p)=np^2.
$$
化简得 $k(1-p)=p-1$，故
$$
k=-1.
$$
### 第 15 题
**答案：** 极小值 $\displaystyle f\left(0,\frac{1}{e}\right)=-\frac{1}{e}$，无极大值。

函数定义域为 $y>0$。先求一阶偏导：
$$
f_x=2x(2+y^2),
\qquad
f_y=2x^2y+\ln y+1.
$$
令 $f_x=f_y=0$，由 $f_x=0$ 得 $x=0$，再由 $\ln y+1=0$ 得 $y=\frac{1}{e}$，故唯一驻点为
$$
\left(0,\frac{1}{e}\right).
$$
二阶偏导为
$$
f_{xx}=2(2+y^2),\qquad f_{xy}=4xy,
\qquad f_{yy}=2x^2+\frac{1}{y}.
$$
在驻点处，
$$
A=2\left(2+\frac{1}{e^2}\right)>0,
\qquad B=0,
\qquad C=e>0.
$$
于是 $B^2-AC<0$ 且 $A>0$，所以该点为极小值点。极小值为
$$
f\left(0,\frac{1}{e}\right)=\frac{1}{e}\ln\frac{1}{e}=-\frac{1}{e}.
$$
因此函数有极小值 $-\frac{1}{e}$，无极大值。
### 第 16 题
**答案：** $\displaystyle S_1=\frac{1}{2},\quad S_2=1-\ln 2$

两曲线 $y=x^n$ 与 $y=x^{n+1}$ 在 $(0,0)$ 与 $(1,1)$ 相交，且在 $0<x<1$ 上 $x^n>x^{n+1}$，所以
$$
a_n=\int_0^1(x^n-x^{n+1})\,dx
=\frac{1}{n+1}-\frac{1}{n+2}.
$$
于是
$$
S_1=\sum_{n=1}^{\infty}\left(\frac{1}{n+1}-\frac{1}{n+2}\right)=\frac{1}{2}.
$$
又
$$
a_{2n-1}=\frac{1}{2n}-\frac{1}{2n+1},
$$
从而
$$
S_2=\sum_{n=1}^{\infty}\left(\frac{1}{2n}-\frac{1}{2n+1}\right)
=\frac{1}{2}-\frac{1}{3}+\frac{1}{4}-\frac{1}{5}+\cdots.
$$
由
$$
\ln2=1-\frac{1}{2}+\frac{1}{3}-\frac{1}{4}+\cdots,
$$
得
$$
S_2=1-\ln2.
$$
### 第 17 题
**答案：** （1）$\displaystyle S_1:\frac{x^2}{4}+\frac{y^2+z^2}{3}=1$，$\displaystyle S_2:y^2+z^2=\frac{(x-4)^2}{4}$；（2）$\displaystyle V=\pi$。

椭圆
$$
\frac{x^2}{4}+\frac{y^2}{3}=1
$$
绕 $x$ 轴旋转，得到椭球面
$$
S_1:\quad \frac{x^2}{4}+\frac{y^2+z^2}{3}=1.
$$
设过点 $(4,0)$ 的切线与椭圆相切于 $(x_0,y_0)$。椭圆在该点的切线为
$$
\frac{x_0x}{4}+\frac{y_0y}{3}=1.
$$
代入 $(4,0)$ 得 $x_0=1$，再由椭圆方程得 $y_0=\pm\frac{3}{2}$。因此切线为
$$
\frac{x}{4}\pm\frac{y}{2}=1.
$$
绕 $x$ 轴旋转，得到圆锥面
$$
S_2:\quad y^2+z^2=\frac{(x-4)^2}{4}.
$$
两曲面之间的体积可看成底面半径 $\frac{3}{2}$、高 $3$ 的圆锥体积，减去椭球在 $1\le x\le2$ 的部分体积。圆锥体积为
$$
\frac{1}{3}\pi\left(\frac{3}{2}\right)^2\cdot3=\frac{9\pi}{4}.
$$
椭球截面半径平方为 $3\left(1-\frac{x^2}{4}\right)$，所以该部分体积为
$$
\int_1^2 \pi\cdot3\left(1-\frac{x^2}{4}\right)\,dx
=\frac{3\pi}{4}\int_1^2(4-x^2)\,dx
=\frac{5\pi}{4}.
$$
故所求体积为
$$
\frac{9\pi}{4}-\frac{5\pi}{4}=\pi.
$$
### 第 18 题
**答案：** 证明见解析。

（1）构造辅助函数
$$
F(x)=f(x)-\frac{f(b)-f(a)}{b-a}(x-a).
$$
由题设可知 $F(x)$ 在 $[a,b]$ 上连续，在 $(a,b)$ 内可导，且
$$
F(a)=f(a),\qquad F(b)=f(b)-\frac{f(b)-f(a)}{b-a}(b-a)=f(a).
$$
由罗尔定理，存在 $\xi\in(a,b)$，使 $F'(\xi)=0$。于是
$$
f'(\xi)-\frac{f(b)-f(a)}{b-a}=0,
$$
即
$$
f(b)-f(a)=f'(\xi)(b-a).
$$

（2）任取 $t\in(0,\delta)$。由 $f$ 在 $x=0$ 处连续、在 $(0,\delta)$ 内可导，知 $f$ 在 $[0,t]$ 上连续、在 $(0,t)$ 内可导。由拉格朗日中值定理，存在 $\xi_t\in(0,t)$，使
$$
\frac{f(t)-f(0)}{t}=f'(\xi_t).
$$
当 $t\to0^+$ 时，$\xi_t\to0^+$。又 $\lim_{x\to0^+}f'(x)=A$，故
$$
f'_+(0)=\lim_{t\to0^+}\frac{f(t)-f(0)}{t}=\lim_{t\to0^+}f'(\xi_t)=A.
$$
所以 $f'_+(0)$ 存在且等于 $A$。
### 第 19 题
**答案：** $\displaystyle I=4\pi$

曲面积分可看成向量场
$$
\boldsymbol F=\frac{(x,y,z)}{(x^2+y^2+z^2)^{\frac{3}{2}}}
$$
通过闭曲面 $\Sigma$ 外侧的通量。该向量场在原点外散度为 $0$。取单位球面 $\Sigma_1:x^2+y^2+z^2=1$ 的外侧，考虑 $\Sigma$ 与 $\Sigma_1$ 之间的区域，由高斯公式可知两闭曲面的外向通量相等。

在单位球面上，$x^2+y^2+z^2=1$，故
$$
\iint_{\Sigma_1}\frac{x\,dy\,dz+y\,dz\,dx+z\,dx\,dy}{(x^2+y^2+z^2)^{\frac{3}{2}}}
=\iint_{\Sigma_1}x\,dy\,dz+y\,dz\,dx+z\,dx\,dy.
$$
再用高斯公式，
$$
\iint_{\Sigma_1}x\,dy\,dz+y\,dz\,dx+z\,dx\,dy
=\iiint_{x^2+y^2+z^2\le1}3\,dV=3\cdot\frac{4\pi}{3}=4\pi.
$$
因此
$$
I=4\pi.
$$
### 第 20 题
**答案：** $\displaystyle \xi_2=\begin{pmatrix}-\frac{1}{2}+\frac{k}{2}\\ \frac{1}{2}-\frac{k}{2}\\ k\end{pmatrix}$，$\displaystyle \xi_3=\begin{pmatrix}-\frac{1}{2}-s\\ s\\ t\end{pmatrix}$，其中 $k,s,t\in\mathbb{R}$；且任取这样的 $\xi_2,\xi_3$，$\xi_1,\xi_2,\xi_3$ 线性无关。

记
$$
A=\begin{pmatrix}1&-1&-1\\-1&1&1\\0&-4&-2\end{pmatrix},
\qquad
\xi_1=\begin{pmatrix}-1\\1\\-2\end{pmatrix}.
$$
对增广矩阵 $(A:\xi_1)$ 作初等行变换，可化为
$$
\left(\begin{array}{ccc:c}
1&0&-\frac{1}{2}&-\frac{1}{2}\\
0&1&\frac{1}{2}&\frac{1}{2}\\
0&0&0&0
\end{array}\right).
$$
故
$$
\xi_2=\begin{pmatrix}-\frac{1}{2}+\frac{k}{2}\\ \frac{1}{2}-\frac{k}{2}\\ k\end{pmatrix},
\qquad k\in\mathbb R.
$$
又
$$
A^2=\begin{pmatrix}2&2&0\\-2&-2&0\\4&4&0\end{pmatrix}.
$$
对 $(A^2:\xi_1)$ 作初等行变换，可得方程 $x_1+x_2=-\frac{1}{2}$，所以
$$
\xi_3=\begin{pmatrix}-\frac{1}{2}-s\\s\\t\end{pmatrix},
\qquad s,t\in\mathbb R.
$$

下面证明线性无关。由 $A\xi_1=0$、$A\xi_2=\xi_1$、$A^2\xi_3=\xi_1$。若
$$
c_1\xi_1+c_2\xi_2+c_3\xi_3=0,
$$
两边左乘 $A$ 得
$$
c_2\xi_1+c_3A\xi_3=0.
$$
再左乘 $A$ 得
$$
c_3A^2\xi_3=c_3\xi_1=0.
$$
由于 $\xi_1\ne0$，所以 $c_3=0$。代回得 $c_2\xi_1=0$，故 $c_2=0$；再代回原式得 $c_1\xi_1=0$，故 $c_1=0$。因此 $\xi_1,\xi_2,\xi_3$ 线性无关。
### 第 21 题
**答案：** （1）特征值为 $a,\ a+1,\ a-2$；（2）$a=2$。

二次型矩阵为
$$
A=\begin{pmatrix}a&0&1\\0&a&-1\\1&-1&a-1\end{pmatrix}.
$$
其特征多项式为
$$
\begin{aligned}
\det(\lambda E-A)
&=\begin{vmatrix}\lambda-a&0&-1\\0&\lambda-a&1\\-1&1&\lambda-a+1\end{vmatrix} \\
&=(\lambda-a)(\lambda-(a+1))(\lambda-(a-2)).
\end{aligned}
$$
所以特征值为
$$
a,\qquad a+1,\qquad a-2.
$$
若规范形为 $y_1^2+y_2^2$，则矩阵秩为 $2$，故
$$
a(a+1)(a-2)=0,
$$
即 $a=0,-1,2$。逐一判断惯性指数：

当 $a=0$ 时，特征值为 $0,1,-2$，规范形含一正一负；当 $a=-1$ 时，特征值为 $-1,0,-3$，规范形含两个负平方项；当 $a=2$ 时，特征值为 $2,3,0$，规范形为两个正平方项。故
$$
a=2.
$$
### 第 22 题
**答案：** （1）$\displaystyle P\{X=1\mid Z=0\}=\frac{4}{9}$；（2）记 $p_{ij}=P\{X=i,Y=j\}$，则 $p_{00}=\frac{1}{4},p_{01}=\frac{1}{3},p_{02}=\frac{1}{9},p_{10}=\frac{1}{6},p_{11}=\frac{1}{9},p_{12}=0,p_{20}=\frac{1}{36},p_{21}=0,p_{22}=0$。

每次取到红、黑、白球的概率分别为
$$
\frac{1}{6},\qquad \frac{1}{3},\qquad \frac{1}{2}.
$$
（1）$Z=0$ 表示两次都没有取到白球，其概率为
$$
P\{Z=0\}=\left(\frac{1}{2}\right)^2=\frac{1}{4}.
$$
同时 $X=1,Z=0$ 表示两次中一次红球、一次黑球，故
$$
P\{X=1,Z=0\}=2\cdot\frac{1}{6}\cdot\frac{1}{3}=\frac{1}{9}.
$$
因此
$$
P\{X=1\mid Z=0\}=\frac{\frac{1}{9}}{\frac{1}{4}}=\frac{4}{9}.
$$

（2）$X,Y$ 的可能取值均为 $0,1,2$，且 $x+y\le2$。概率分布为：

| $X\backslash Y$ | $0$ | $1$ | $2$ |
|---|---:|---:|---:|
| $0$ | $\frac{1}{4}$ | $\frac{1}{3}$ | $\frac{1}{9}$ |
| $1$ | $\frac{1}{6}$ | $\frac{1}{9}$ | $0$ |
| $2$ | $\frac{1}{36}$ | $0$ | $0$ |
### 第 23 题
**答案：** 矩估计量与最大似然估计量均为 $\displaystyle \hat\lambda=\frac{2}{\bar X}$。

总体密度为
$$
f(x)=\lambda^2xe^{-\lambda x},\qquad x>0,
$$
这是形状参数为 $2$、率参数为 $\lambda$ 的 Gamma 分布，故
$$
EX=\int_0^{+\infty}x\lambda^2xe^{-\lambda x}\,dx=\frac{2}{\lambda}.
$$
令 $\bar X=EX$，得矩估计量
$$
\hat\lambda_1=\frac{2}{\bar X}.
$$

设样本观测值为 $x_1,x_2,\ldots,x_n$，其中 $x_i>0$。似然函数为
$$
L(\lambda)=\prod_{i=1}^n \lambda^2x_i e^{-\lambda x_i}
=\lambda^{2n}e^{-\lambda\sum_{i=1}^n x_i}\prod_{i=1}^n x_i.
$$
取对数，
$$
\ln L=2n\ln\lambda-\lambda\sum_{i=1}^n x_i+\sum_{i=1}^n\ln x_i.
$$
令
$$
\frac{d\ln L}{d\lambda}=\frac{2n}{\lambda}-\sum_{i=1}^n x_i=0,
$$
得最大似然估计量
$$
\hat\lambda_2=\frac{2n}{\sum_{i=1}^n x_i}=\frac{2}{\bar X}.
$$
