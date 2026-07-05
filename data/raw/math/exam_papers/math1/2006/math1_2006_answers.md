# Math 1 2006 Answers

资料类型：考研数学一答案解析
年份：2006
科目：数学一
范围：试卷 I
来源：D:\百度网盘\高数资料\【02】1987-2022年数学一真题详解答案（PDF）\2006考研数学一真题解析.pdf
校对状态：已按答案页图像和题干重新整理；第 22 题按原卷题干保留两问，未纳入答案页中与本题题干不对应的协方差段落。

## 答案速查

| 题号 | 题型 | 答案 |
|---|---|---|
| 1 | 填空题 | $2$ |
| 2 | 填空题 | $y=Cxe^{-x}$ |
| 3 | 填空题 | $2\pi$ |
| 4 | 填空题 | $\sqrt{2}$ |
| 5 | 填空题 | $2$ |
| 6 | 填空题 | $\displaystyle \frac{1}{9}$ |
| 7 | 选择题 | A |
| 8 | 选择题 | C |
| 9 | 选择题 | D |
| 10 | 选择题 | D |
| 11 | 选择题 | A |
| 12 | 选择题 | B |
| 13 | 选择题 | C |
| 14 | 选择题 | A |
| 15 | 解答题 | $\displaystyle \frac{\pi}{2}\ln2$ |
| 16 | 解答题 | (I) 极限为 $0$；(II) $\displaystyle e^{-1/6}$。 |
| 17 | 解答题 | $\displaystyle f(x)=\frac{1}{3}\sum_{n=0}^{\infty}\left[(-1)^n+\frac{1}{2^{n+1}}\right]x^{n+1}\quad(|x|<1)$ |
| 18 | 解答题 | $f(u)=\ln u$ |
| 19 | 解答题 | 结论成立。 |
| 20 | 解答题 | $a=2,\ b=-3$；通解为 $(2,-3,0,0)^T+c_1(-2,1,1,0)^T+c_2(4,-5,0,1)^T$。 |
| 21 | 解答题 | 特征值为 $3,0,0$；$\lambda=3$ 的特征向量为 $k(1,1,1)^T$，$\lambda=0$ 的特征向量为 $k_1(-1,2,-1)^T+k_2(0,-1,1)^T$；可取 $Q=\begin{pmatrix}\frac{1}{\sqrt{3}}&0&-\frac{2}{\sqrt{6}}\\ \frac{1}{\sqrt{3}}&-\frac{1}{\sqrt{2}}&\frac{1}{\sqrt{6}}\\ \frac{1}{\sqrt{3}}&\frac{1}{\sqrt{2}}&\frac{1}{\sqrt{6}}\end{pmatrix}$，$\Lambda=\operatorname{diag}(3,0,0)$。 |
| 22 | 解答题 | $f_Y(y)=\dfrac{3}{8\sqrt{y}}\ (0<y<1)$，$f_Y(y)=\dfrac{1}{8\sqrt{y}}\ (1<y<4)$，其他为 $0$；$\displaystyle F\left(-\frac{1}{2},4\right)=\frac{1}{4}$。 |
| 23 | 解答题 | $\displaystyle \hat\theta=\frac{N}{n}$ |

## 详细解析

### 第 1 题

**答案：** $2$

当 $x\to0$ 时，
$$
\ln(1+x)\sim x,\qquad 1-\cos x\sim\frac{x^2}{2}.
$$

因此
$$
\lim_{x\to0}\frac{x\ln(1+x)}{1-\cos x}
=\lim_{x\to0}\frac{x^2}{x^2/2}
=2.
$$

### 第 2 题

**答案：** $y=Cxe^{-x}$

原方程为
$$
\frac{dy}{dx}=\frac{y(1-x)}{x}.
$$
分离变量：
$$
\frac{dy}{y}=\left(\frac{1}{x}-1\right)dx.
$$

两边积分，得
$$
\ln|y|=\ln x-x+C.
$$

于是通解可写为
$$
y=Cxe^{-x}.
$$
其中常数 $C$ 可取任意实数，包含零解。

### 第 3 题

**答案：** $2\pi$

设
$$
P=x,\qquad Q=2y,\qquad R=3(z-1).
$$
则
$$
\frac{\partial P}{\partial x}+\frac{\partial Q}{\partial y}+\frac{\partial R}{\partial z}
=1+2+3=6.
$$

用平面 $z=1$ 补上圆盘 $\Sigma_1$，与锥面 $\Sigma$ 围成圆锥体
$$
\Omega:\ 0\le r\le z\le1.
$$
锥面取下侧，正好是该圆锥体的外侧方向。由高斯公式，
$$
\iint_{\Sigma+\Sigma_1}P\,dy\,dz+Q\,dz\,dx+R\,dx\,dy
=\iiint_\Omega 6\,dV.
$$

在补上的圆盘 $\Sigma_1$ 上，$z=1$ 且 $dz=0$，故补面上的积分为 $0$。因此原积分等于
$$
6V(\Omega).
$$

圆锥体体积为
$$
V(\Omega)=\int_0^1\pi z^2\,dz=\frac{\pi}{3}.
$$
所以积分值为
$$
6\cdot\frac{\pi}{3}=2\pi.
$$

### 第 4 题

**答案：** $\sqrt{2}$

点 $(x_0,y_0,z_0)$ 到平面 $Ax+By+Cz+D=0$ 的距离为
$$
d=\frac{|Ax_0+By_0+Cz_0+D|}{\sqrt{A^2+B^2+C^2}}.
$$

代入点 $(2,1,0)$ 与平面 $3x+4y+5z=0$，得
$$
d=\frac{|3\cdot2+4\cdot1+5\cdot0|}{\sqrt{3^2+4^2+5^2}}
=\frac{10}{\sqrt{50}}
=\sqrt{2}.
$$

### 第 5 题

**答案：** $2$

由
$$
BA=B+2E
$$
得
$$
B(A-E)=2E.
$$

两边取行列式：
$$
\det B\,\det(A-E)=\det(2E).
$$

这里
$$
A-E=
\begin{pmatrix}
1&1\\
-1&1
\end{pmatrix},
\qquad \det(A-E)=2,
$$
且 $\det(2E)=2^2\det E=4$。因此
$$
\det B=\frac{4}{2}=2.
$$

### 第 6 题

**答案：** $\displaystyle \frac{1}{9}$

事件
$$
\{\max\{X,Y\}\le1\}
$$
等价于
$$
\{X\le1,\ Y\le1\}.
$$

因为 $X,Y$ 独立，且都服从 $[0,3]$ 上的均匀分布，
$$
P\{X\le1\}=\frac{1}{3},\qquad P\{Y\le1\}=\frac{1}{3}.
$$

所以
$$
P\{\max\{X,Y\}\le1\}
=P\{X\le1\}P\{Y\le1\}
=\frac{1}{9}.
$$

### 第 7 题

**答案：** A

由 $f'(x)>0$ 与 $\Delta x>0$ 可知
$$
dy=f'(x_0)\Delta x>0.
$$

又由泰勒公式，
$$
\Delta y=f(x_0+\Delta x)-f(x_0)
=f'(x_0)\Delta x+\frac{1}{2} f''(\xi)(\Delta x)^2
$$
其中 $\xi$ 位于 $x_0$ 与 $x_0+\Delta x$ 之间。由于 $f''(\xi)>0$，
$$
\Delta y-dy=\frac{1}{2} f''(\xi)(\Delta x)^2>0.
$$

因此
$$
0<dy<\Delta y.
$$
选 A。

### 第 8 题

**答案：** C

给定极坐标区域
$$
0\le r\le1,\qquad 0\le\theta\le\frac{\pi}{4}.
$$
这是单位圆第一象限中位于直线 $y=x$ 下方的扇形区域，即
$$
x^2+y^2\le1,\qquad 0\le y\le x.
$$

若按先 $y$ 后 $x$ 的次序积分，则
$$
0\le y\le\frac{\sqrt{2}}{2},
\qquad
y\le x\le\sqrt{1-y^2}.
$$

故原积分等于
$$
\int_0^{\sqrt{2}/2}dy\int_y^{\sqrt{1-y^2}}f(x,y)\,dx.
$$
选 C。

### 第 9 题

**答案：** D

若 $\sum a_n$ 收敛，则去掉有限项或平移指标后，$\sum a_{n+1}$ 也收敛。因此
$$
\sum_{n=1}^{\infty}(a_n+a_{n+1})
$$
收敛，从而
$$
\sum_{n=1}^{\infty}\frac{a_n+a_{n+1}}{2}
$$
收敛。故 D 正确。

A 不一定成立，例如交错调和级数收敛但不绝对收敛。B 不一定成立，因为改变符号后不保留一般收敛性。C 也不一定成立，例如取 $a_n=(-1)^n/\sqrt{n}$，则 $\sum a_n$ 收敛，但
$$
a_n a_{n+1}=-\frac{1}{\sqrt{n(n+1)}},
$$
相应级数发散。

### 第 10 题

**答案：** D

由于 $\varphi_y'(x,y)\ne0$，约束方程 $\varphi(x,y)=0$ 在 $(x_0,y_0)$ 附近可确定隐函数 $y=y(x)$。约束极值可化为一元函数
$$
z=f(x,y(x))
$$
在 $x=x_0$ 处的极值。

必要条件为
$$
\left.\frac{dz}{dx}\right|_{x=x_0}
=f_x'(x_0,y_0)+f_y'(x_0,y_0)y'(x_0)=0.
$$
又
$$
y'(x_0)=-\frac{\varphi_x'(x_0,y_0)}{\varphi_y'(x_0,y_0)}.
$$
所以
$$
f_x'(x_0,y_0)
-f_y'(x_0,y_0)\frac{\varphi_x'(x_0,y_0)}{\varphi_y'(x_0,y_0)}
=0.
$$

若 $f_x'(x_0,y_0)\ne0$ 而 $f_y'(x_0,y_0)=0$，上式不可能成立。因此
$$
f_x'(x_0,y_0)\ne0\quad\Rightarrow\quad f_y'(x_0,y_0)\ne0.
$$
选 D。

### 第 11 题

**答案：** A

若
$$
\boldsymbol{\alpha}_1,\ldots,\boldsymbol{\alpha}_s
$$
线性相关，则存在不全为零的常数 $k_1,\ldots,k_s$，使
$$
k_1\boldsymbol{\alpha}_1+\cdots+k_s\boldsymbol{\alpha}_s=0.
$$

左乘矩阵 $A$，得到
$$
k_1A\boldsymbol{\alpha}_1+\cdots+k_sA\boldsymbol{\alpha}_s=0.
$$

这说明
$$
A\boldsymbol{\alpha}_1,\ldots,A\boldsymbol{\alpha}_s
$$
线性相关。选 A。

### 第 12 题

**答案：** B

左乘初等矩阵表示行变换。将 $A$ 的第 $2$ 行加到第 $1$ 行，正是左乘
$$
P=\begin{pmatrix}
1&1&0\\
0&1&0\\
0&0&1
\end{pmatrix},
$$
所以
$$
B=PA.
$$

右乘初等矩阵表示列变换。将 $B$ 的第 $1$ 列的 $-1$ 倍加到第 $2$ 列，对应右乘
$$
P^{-1}=
\begin{pmatrix}
1&-1&0\\
0&1&0\\
0&0&1
\end{pmatrix}.
$$

因此
$$
C=BP^{-1}=PAP^{-1}.
$$
选 B。

### 第 13 题

**答案：** C

由条件概率定义，
$$
P(A\mid B)=\frac{P(AB)}{P(B)}=1.
$$
因为 $P(B)>0$，得
$$
P(AB)=P(B).
$$
这表示 $B$ 几乎包含于 $A$。

由加法公式，
$$
P(A\cup B)=P(A)+P(B)-P(AB)=P(A).
$$
选 C。

### 第 14 题

**答案：** A

标准化后，
$$
\frac{X-\mu_1}{\sigma_1}\sim N(0,1),\qquad
\frac{Y-\mu_2}{\sigma_2}\sim N(0,1).
$$

因此
$$
P\{|X-\mu_1|<1\}
=P\left\{\left|\frac{X-\mu_1}{\sigma_1}\right|<\frac{1}{\sigma_1}\right\}
=2\Phi\left(\frac{1}{\sigma_1}\right)-1.
$$
同理
$$
P\{|Y-\mu_2|<1\}
=2\Phi\left(\frac{1}{\sigma_2}\right)-1.
$$

标准正态分布函数 $\Phi(x)$ 单调递增。题设左边概率更大，故
$$
\frac{1}{\sigma_1}>\frac{1}{\sigma_2},
$$
于是
$$
\sigma_1<\sigma_2.
$$
选 A。

### 第 15 题

**答案：** $\displaystyle \frac{\pi}{2}\ln2$

区域
$$
D=\{(x,y)\mid x^2+y^2\le1,\ x\ge0\}
$$
关于 $x$ 轴对称，而
$$
\frac{xy}{1+x^2+y^2}
$$
关于 $y$ 为奇函数。因此
$$
\iint_D\frac{xy}{1+x^2+y^2}\,dx\,dy=0.
$$

所以
$$
I=\iint_D\frac{1}{1+x^2+y^2}\,dx\,dy.
$$

用极坐标，$D$ 对应
$$
-\frac{\pi}{2}\le\theta\le\frac{\pi}{2},\qquad 0\le r\le1.
$$
于是
$$
\begin{aligned}
I
&=\int_{-\pi/2}^{\pi/2}\int_0^1\frac{r}{1+r^2}\,dr\,d\theta\\
&=\pi\cdot\frac{1}{2}\ln(1+r^2)\Big|_0^1\\
&=\frac{\pi}{2}\ln2.
\end{aligned}
$$

### 第 16 题

**答案：** (I) 极限为 $0$；(II) $\displaystyle e^{-1/6}$。

(I) 因为 $0<x_1<\pi$，且 $x_{n+1}=\sin x_n$，从第二项起有
$$
0<x_n<\pi,\qquad 0<\sin x_n<x_n.
$$
所以 $\{x_n\}$ 单调递减且有下界 $0$，极限存在。设
$$
\lim_{n\to\infty}x_n=A.
$$
递推式两边取极限，得
$$
A=\sin A.
$$
在 $[0,\pi]$ 上该方程唯一解为 $A=0$，故
$$
\lim_{n\to\infty}x_n=0.
$$

(II) 由于 $x_{n+1}=\sin x_n$ 且 $x_n\to0$，所求极限为
$$
\lim_{n\to\infty}\left(\frac{\sin x_n}{x_n}\right)^{1/x_n^2}
=\lim_{t\to0}\left(\frac{\sin t}{t}\right)^{1/t^2}.
$$

设此极限为 $L$。取对数：
$$
\ln L=\lim_{t\to0}\frac{\ln(\sin t/t)}{t^2}.
$$
利用展开
$$
\frac{\sin t}{t}=1-\frac{t^2}{6}+o(t^2),
$$
得
$$
\ln\left(\frac{\sin t}{t}\right)=-\frac{t^2}{6}+o(t^2).
$$
因此
$$
\ln L=-\frac{1}{6},
$$
从而
$$
L=e^{-1/6}.
$$

### 第 17 题

**答案：** $\displaystyle f(x)=\frac{1}{3}\sum_{n=0}^{\infty}\left[(-1)^n+\frac{1}{2^{n+1}}\right]x^{n+1}\quad(|x|<1)$

先分解：
$$
\frac{1}{2+x-x^2}
=\frac{1}{(1+x)(2-x)}
=\frac{1}{3}\left(\frac{1}{1+x}+\frac{1}{2-x}\right).
$$

又
$$
\frac{1}{1+x}=\sum_{n=0}^{\infty}(-1)^n x^n,\qquad |x|<1,
$$
并且
$$
\frac{1}{2-x}
=\frac{1}{2}\cdot\frac{1}{1-x/2}
=\sum_{n=0}^{\infty}\frac{x^n}{2^{n+1}},\qquad |x|<2.
$$

两者共同收敛范围为 $|x|<1$。因此
$$
\frac{1}{2+x-x^2}
=\frac{1}{3}\sum_{n=0}^{\infty}
\left[(-1)^n+\frac{1}{2^{n+1}}\right]x^n.
$$

乘以 $x$，得
$$
f(x)=\frac{x}{2+x-x^2}
=\frac{1}{3}\sum_{n=0}^{\infty}
\left[(-1)^n+\frac{1}{2^{n+1}}\right]x^{n+1},
\qquad |x|<1.
$$

### 第 18 题

**答案：** $f(u)=\ln u$

令
$$
u=\sqrt{x^2+y^2}.
$$
则
$$
z=f(u).
$$
径向函数在平面上的拉普拉斯算子为
$$
z_{xx}+z_{yy}=f''(u)+\frac{1}{u}f'(u).
$$
也可直接求偏导验证：代入题设
$$
z_{xx}+z_{yy}=0
$$
即得
$$
f''(u)+\frac{f'(u)}{u}=0.
$$

令
$$
p=f'(u).
$$
则方程化为
$$
p'+\frac{p}{u}=0,
$$
即
$$
\frac{dp}{p}=-\frac{du}{u}.
$$
积分得
$$
p=\frac{C}{u}.
$$

由 $f'(1)=1$ 得 $C=1$，所以
$$
f'(u)=\frac{1}{u}.
$$
再积分：
$$
f(u)=\ln u+C_2.
$$
由 $f(1)=0$ 得 $C_2=0$，因此
$$
f(u)=\ln u.
$$

### 第 19 题

**答案：** 结论成立。

由题设
$$
f(tx,ty)=t^{-2}f(x,y)\qquad(t>0)
$$
对 $t$ 求导，得
$$
x f_x(tx,ty)+y f_y(tx,ty)=-2t^{-3}f(x,y).
$$
令 $t=1$，得到欧拉齐次函数关系
$$
x f_x(x,y)+y f_y(x,y)=-2f(x,y).
$$

记
$$
P(x,y)=y f(x,y),\qquad Q(x,y)=-x f(x,y).
$$
则
$$
\frac{\partial Q}{\partial x}
=-f(x,y)-x f_x(x,y),
$$
$$
\frac{\partial P}{\partial y}
=f(x,y)+y f_y(x,y).
$$

由
$$
x f_x+y f_y=-2f
$$
可得
$$
-f-xf_x=f+yf_y,
$$
即
$$
\frac{\partial Q}{\partial x}
=\frac{\partial P}{\partial y}.
$$

上半平面 $D=\{(x,y)\mid y>0\}$ 是单连通区域，且 $P,Q$ 有连续偏导。由格林公式，对 $D$ 内任意分段光滑有向简单闭曲线 $L$，
$$
\oint_L P\,dx+Q\,dy
=\iint_{\operatorname{int}L}
\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)dx\,dy
=0.
$$

即
$$
\oint_L yf(x,y)\,dx-xf(x,y)\,dy=0.
$$

### 第 20 题

**答案：** $a=2,\ b=-3$；通解为 $(2,-3,0,0)^T+c_1(-2,1,1,0)^T+c_2(4,-5,0,1)^T$。

(I) 设非齐次方程组的三个线性无关解为
$$
\boldsymbol{\alpha}_1,\boldsymbol{\alpha}_2,\boldsymbol{\alpha}_3.
$$
则
$$
\boldsymbol{\alpha}_2-\boldsymbol{\alpha}_1,\qquad
\boldsymbol{\alpha}_3-\boldsymbol{\alpha}_1
$$
是对应齐次方程组 $A\boldsymbol{x}=0$ 的两个线性无关解。

未知量个数为 $4$，故齐次解空间维数至少为 $2$：
$$
4-r(A)\ge2.
$$
于是 $r(A)\le2$。另一方面，系数矩阵前两行
$$
(1,1,1,1),\qquad (4,3,5,-1)
$$
线性无关，所以 $r(A)\ge2$。因此
$$
r(A)=2.
$$

(II) 对增广矩阵作初等行变换：
$$
\left[
\begin{array}{rrrr|r}
1&1&1&1&-1\\
4&3&5&-1&-1\\
a&1&3&b&1
\end{array}
\right]
\sim
\left[
\begin{array}{rrrr|r}
1&1&1&1&-1\\
0&-1&1&-5&3\\
0&0&4-2a&4a+b-5&4-2a
\end{array}
\right].
$$

由 $r(A)=2$，第三行系数应为零，故
$$
4-2a=0,\qquad 4a+b-5=0.
$$
解得
$$
a=2,\qquad b=-3.
$$

此时方程组同解为
$$
\begin{cases}
x_1=2-2x_3+4x_4,\\
x_2=-3+x_3-5x_4.
\end{cases}
$$
令 $x_3,x_4$ 为自由未知量，得一个特解
$$
(2,-3,0,0)^T,
$$
齐次方程组的基础解系为
$$
(-2,1,1,0)^T,\qquad (4,-5,0,1)^T.
$$
因此通解为
$$
\boldsymbol{x}
=(2,-3,0,0)^T
c_1(-2,1,1,0)^T
c_2(4,-5,0,1)^T.
$$

### 第 21 题

**答案：** 特征值为 $3,0,0$；$\lambda=3$ 的特征向量为 $k(1,1,1)^T$，$\lambda=0$ 的特征向量为 $k_1(-1,2,-1)^T+k_2(0,-1,1)^T$；可取 $Q=\begin{pmatrix}\frac{1}{\sqrt{3}}&0&-\frac{2}{\sqrt{6}}\\ \frac{1}{\sqrt{3}}&-\frac{1}{\sqrt{2}}&\frac{1}{\sqrt{6}}\\ \frac{1}{\sqrt{3}}&\frac{1}{\sqrt{2}}&\frac{1}{\sqrt{6}}\end{pmatrix}$，$\Lambda=\operatorname{diag}(3,0,0)$。

因为 $A\boldsymbol{\alpha}_1=0$，$A\boldsymbol{\alpha}_2=0$，且
$$
\boldsymbol{\alpha}_1=(-1,2,-1)^T,\qquad
\boldsymbol{\alpha}_2=(0,-1,1)^T
$$
线性无关，所以 $\lambda=0$ 至少有两个线性无关特征向量。

又 $A$ 的各行元素之和均为 $3$，故
$$
A(1,1,1)^T=(3,3,3)^T=3(1,1,1)^T.
$$
因此 $(1,1,1)^T$ 是对应特征值 $3$ 的特征向量。

由于 $A$ 为 $3$ 阶实对称矩阵，且已经得到三个线性无关的特征向量，所以特征值为
$$
3,0,0.
$$
对应特征向量可写为
$$
\lambda=3:\quad k(1,1,1)^T,
$$
$$
\lambda=0:\quad k_1(-1,2,-1)^T+k_2(0,-1,1)^T.
$$

为作正交对角化，取单位正交特征向量
$$
e_1=\frac{1}{\sqrt{3}}(1,1,1)^T,
$$
$$
e_2=\frac{1}{\sqrt{2}}(0,-1,1)^T,
$$
$$
e_3=\frac{1}{\sqrt{6}}(-2,1,1)^T.
$$
令
$$
Q=(e_1,e_2,e_3)
=\begin{pmatrix}
\frac{1}{\sqrt{3}}&0&-\frac{2}{\sqrt{6}}\\
\frac{1}{\sqrt{3}}&-\frac{1}{\sqrt{2}}&\frac{1}{\sqrt{6}}\\
\frac{1}{\sqrt{3}}&\frac{1}{\sqrt{2}}&\frac{1}{\sqrt{6}}
\end{pmatrix}.
$$
则 $Q$ 为正交矩阵，并且
$$
Q^TAQ=
\begin{pmatrix}
3&0&0\\
0&0&0\\
0&0&0
\end{pmatrix}
=\Lambda.
$$

### 第 22 题

**答案：** $f_Y(y)=\dfrac{3}{8\sqrt{y}}\ (0<y<1)$，$f_Y(y)=\dfrac{1}{8\sqrt{y}}\ (1<y<4)$，其他为 $0$；$\displaystyle F\left(-\frac{1}{2},4\right)=\frac{1}{4}$。

(I) 因为 $Y=X^2$，先求分布函数
$$
F_Y(y)=P\{Y\le y\}=P\{X^2\le y\}.
$$

当 $y<0$ 时，$F_Y(y)=0$。

当 $0\le y<1$ 时，
$$
-\sqrt{y}\le X\le\sqrt{y}
$$
同时落在 $(-1,0)$ 与 $[0,2)$ 两段密度区间内，因此
$$
F_Y(y)=\int_{-\sqrt{y}}^{0}\frac{1}{2}\,dx+\int_0^{\sqrt{y}}\frac{1}{4}\,dx
=\frac{3}{4}\sqrt{y}.
$$

当 $1\le y<4$ 时，负半轴部分已经覆盖 $(-1,0)$，正半轴覆盖 $[0,\sqrt{y}]$，故
$$
F_Y(y)=\int_{-1}^{0}\frac{1}{2}\,dx+\int_0^{\sqrt{y}}\frac{1}{4}\,dx
=\frac{1}{2}+\frac{1}{4}\sqrt{y}.
$$

当 $y\ge4$ 时，$F_Y(y)=1$。所以
$$
F_Y(y)=
\begin{cases}
0,&y<0,\\
\dfrac{3}{4}\sqrt{y},&0\le y<1,\\
\dfrac{1}{2}+\dfrac{1}{4}\sqrt{y},&1\le y<4,\\
1,&y\ge4.
\end{cases}
$$

对 $y$ 求导，得
$$
f_Y(y)=
\begin{cases}
\dfrac{3}{8\sqrt{y}},&0<y<1,\\
\dfrac{1}{8\sqrt{y}},&1<y<4,\\
0,&\text{其他}.
\end{cases}
$$

(II) 按二维分布函数定义，
$$
F\left(-\frac{1}{2},4\right)
=P\left\{X\le-\frac{1}{2},\ Y\le4\right\}
=P\left\{X\le-\frac{1}{2},\ X^2\le4\right\}.
$$
在 $X$ 的支持区间 $(-1,2)$ 上，条件 $X^2\le4$ 恒成立，因此
$$
F\left(-\frac{1}{2},4\right)
=P\left\{-1<X\le-\frac{1}{2}\right\}
=\int_{-1}^{-1/2}\frac{1}{2}\,dx
=\frac{1}{4}.
$$

### 第 23 题

**答案：** $\displaystyle \hat\theta=\frac{N}{n}$

样本中小于 $1$ 的观测值有 $N$ 个，其密度因子为 $\theta$；其余 $n-N$ 个观测值位于 $[1,2)$，密度因子为 $1-\theta$。因此似然函数为
$$
L(\theta)=\theta^N(1-\theta)^{n-N},\qquad 0<\theta<1.
$$

当 $0<N<n$ 时，取对数：
$$
\ln L(\theta)=N\ln\theta+(n-N)\ln(1-\theta).
$$
求导并令其为零：
$$
\frac{d}{d\theta}\ln L(\theta)
=\frac{N}{\theta}-\frac{n-N}{1-\theta}=0.
$$
解得
$$
\hat\theta=\frac{N}{n}.
$$

通常将最大似然估计写为
$$
\hat\theta=\frac{N}{n}.
$$
若严格坚持参数空间为开区间 $0<\theta<1$，则当 $N=0$ 或 $N=n$ 时最大值只在边界极限处取得；按常规估计量仍记为 $N/n$。
