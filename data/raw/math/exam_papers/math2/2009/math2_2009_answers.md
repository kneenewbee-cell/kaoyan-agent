# Math 2 2009 Answers

资料类型：考研数学二答案解析
年份：2009
科目：数学二
整理状态：依据答案册与题面做清洗整理。

## 答案速查

| 题号 | 题型 | 答案 |
|---|---|---|
| 1 | 选择题 | C |
| 2 | 选择题 | A |
| 3 | 选择题 | D |
| 4 | 选择题 | C |
| 5 | 选择题 | B |
| 6 | 选择题 | D |
| 7 | 选择题 | A |
| 8 | 选择题 | B |
| 9 | 填空题 | $y=2x$ |
| 10 | 填空题 | $-2$ |
| 11 | 填空题 | $0$ |
| 12 | 填空题 | $-3$ |
| 13 | 填空题 | $e^{-2/e}$ |
| 14 | 填空题 | $2$ |
| 15 | 解答题 | $\dfrac14$ |
| 16 | 解答题 | $$
\int \ln\!\left(1+\sqrt{\frac{1+x}{x}}\right)\,dx
=(x+1)\ln\!\left(1+\sqrt{\frac{1+x}{x}}\right)+\sqrt{x(x+1)}+C.
$$ |
| 17 | 解答题 | 记
$$
u=x+y,\quad v=x-y,\quad w=xy,
$$
则
$$
dz=(f_u+f_v+yf_w)\,dx+(f_u-f_v+xf_w)\,dy,
$$
且
$$
z_{xy}=f_{uu}-f_{vv}+(x+y)f_{uw}+(x-y)f_{vw}+xyf_{ww}+f_w.
$$ |
| 18 | 解答题 | $\dfrac{17\pi}{6}$ |
| 19 | 解答题 | $-\dfrac{8}{3}$ |
| 20 | 解答题 | $$
y(x)=
\begin{cases}
\sqrt{\pi^2-x^2}, & -\pi<x<0,\\[2mm]
\pi\cos x+\sin x-x, & 0\le x<\pi.
\end{cases}
$$ |
| 21 | 证明题 | 见解析 |
| 22 | 解答题 | $$
\xi_2=
\begin{pmatrix}
1\\-1\\0
\end{pmatrix}
+k_1
\begin{pmatrix}
1\\1\\0
\end{pmatrix},
\qquad
\xi_3=
\begin{pmatrix}
0\\0\\2
\end{pmatrix}
+k_2
\begin{pmatrix}
1\\1\\0
\end{pmatrix},
\quad k_1,k_2\in\mathbb R.
$$
且任意此类 $\xi_2,\xi_3$ 与 $\xi_1$ 线性无关。 |
| 23 | 解答题 | 特征值为
$$
\lambda_1=a,\qquad \lambda_2=a-2,\qquad \lambda_3=a+1.
$$
当规范形为 $y_1^2+y_2^2$ 时，
$$
a=2.
$$ |

## 详细解析

### 第 1 题

- 答案：C

当 $x$ 取整数时分母为 $0$，函数有无穷多个间断点；但可去间断点要求极限存在。
由
$$
x-x^3=x(1-x^2)=x(1-x)(1+x)
$$
可知只在 $x=0,\pm1$ 处能与 $\sin(\pi x)$ 的零点相消，且这三点的极限都存在，
所以可去间断点共有 $3$ 个。

### 第 2 题

- 答案：A

展开得
$$
x-\sin(ax)=(1-a)x+\frac{a^3}{6}x^3+o(x^3),
$$
而
$$
x^2\ln(1-bx)=-bx^3+o(x^3).
$$
两者等价首先要求一次项消失，所以 $a=1$；再比较三次项系数，
$$
\frac16=-b,
$$
故 $b=-\dfrac16$。

### 第 3 题

- 答案：D

由全微分可知
$$
f_x=x,\qquad f_y=y.
$$
因而
$$
f_{xx}=1,\quad f_{yy}=1,\quad f_{xy}=0.
$$
在 $(0,0)$ 处有驻点，且二次型
$$
d^2f=dx^2+dy^2
$$
正定，所以 $(0,0)$ 是极小值点。

### 第 4 题

- 答案：C

两个积分区域分别为
$$
D_1=\{(x,y)\mid 1\le x\le 2,\ x\le y\le 2\},
$$
$$
D_2=\{(x,y)\mid 1\le y\le 2,\ y\le x\le 4-y\}.
$$
合并后可写成
$$
D=\{(x,y)\mid 1\le y\le 2,\ 1\le x\le 4-y\},
$$
所以等于
$$
\int_1^2dy\int_1^{4-y}f(x,y)\,dx.
$$

### 第 5 题

- 答案：B

曲率圆圆心在原点，且过点 $(1,1)$，可得该点切线斜率为 $-1$，并由曲率公式求得
$$
f'(1)=-1,\qquad f''(1)<0.
$$
又 $f''(x)$ 不变号，因此在 $[1,2]$ 上始终有 $f'(x)<0$，函数单调递减，
不会出现极值点。由于 $f(1)=1>0$，而由单调性与曲率信息可知 $f(2)<0$，
由零点定理知在 $(1,2)$ 内有零点。

### 第 6 题

- 答案：D

由积分上限函数的性质，
$$
F'(x)=f(x).
$$
观察题图可知：在 $[-1,0]$ 上 $f(x)=1$，故 $F$ 为斜率为 $1$ 的直线；
在 $(0,1)$ 上 $f(x)<0$，故 $F$ 递减；在 $(1,2)$ 上 $f(x)>0$，故 $F$ 递增；
在 $(2,3)$ 上 $f(x)=0$，故 $F$ 为常数。与这些特征一致的只有 D。

### 第 7 题

- 答案：A

记
$$
M=\begin{pmatrix}O&A\\B&O\end{pmatrix},
$$
则
$$
|M|=|{-AB}|=|A||B|=6\ne0,
$$
因而 $M$ 可逆。利用分块矩阵求逆可得
$$
M^{-1}=
\begin{pmatrix}
O & B^{-1}\\
A^{-1} & O
\end{pmatrix}.
$$
于是
$$
M^*=|M|M^{-1}
=
\begin{pmatrix}
O & 6B^{-1}\\
6A^{-1} & O
\end{pmatrix}
=
\begin{pmatrix}
O & 3B^*\\
2A^* & O
\end{pmatrix}.
$$

### 第 8 题

- 答案：B

令
$$
E=
\begin{pmatrix}
1&0&0\\
1&1&0\\
0&0&1
\end{pmatrix},
$$
则 $Q=PE$。因此
$$
Q^TAQ=E^T(P^TAP)E
=
E^T
\begin{pmatrix}
1&0&0\\
0&1&0\\
0&0&2
\end{pmatrix}
E
=
\begin{pmatrix}
1&1&0\\
1&2&0\\
0&0&2
\end{pmatrix}.
$$

### 第 9 题

- 答案：$y=2x$

对参数方程求导，
$$
\frac{dx}{dt}=-e^{-(1-t)^2},\qquad
\frac{dy}{dt}=2t\ln(2-t^2)-\frac{2t^3}{2-t^2}.
$$
点 $(0,0)$ 对应 $t=1$。代入得
$$
\left.\frac{dx}{dt}\right|_{t=1}=-1,\qquad
\left.\frac{dy}{dt}\right|_{t=1}=-2,
$$
所以
$$
\frac{dy}{dx}=2.
$$
切线过原点，故方程为 $y=2x$。

### 第 10 题

- 答案：$-2$

由于积分收敛，必须有 $k<0$。再由偶函数性，
$$
1=2\int_0^{+\infty}e^{kx}\,dx
=2\cdot\left(-\frac1k\right).
$$
解得 $k=-2$。

### 第 11 题

- 答案：$0$

积分分部或直接计算可得
$$
\int_0^1 e^{-x}\sin(nx)\,dx
=
\frac{n-e^{-1}\bigl(\sin n+n\cos n\bigr)}{1+n^2}.
$$
分子有界且为 $O(n)$，分母为 $n^2+1$，故极限为 $0$。

### 第 12 题

- 答案：$-3$

先由原方程在 $x=0$ 时得 $e^{y(0)}=1$，故 $y(0)=0$。
对方程求导：
$$
y+xy'+e^y y'=1,
$$
代入 $(0,0)$ 得 $y'(0)=1$。再次求导可得
$$
2y'+xy''+e^y\bigl((y')^2+y''\bigr)=0.
$$
再代入 $(0,0)$ 与 $y'(0)=1$，得
$$
2+1+y''(0)=0,
$$
故 $y''(0)=-3$。

### 第 13 题

- 答案：$e^{-2/e}$

取对数，
$$
\ln y=2x\ln x.
$$
设 $\phi(x)=2x\ln x$，则
$$
\phi'(x)=2(\ln x+1).
$$
令 $\phi'(x)=0$ 得 $x=e^{-1}$。此时
$$
\phi(e^{-1})=-\frac{2}{e},
$$
从而
$$
y_{\min}=e^{-2/e}.
$$

### 第 14 题

- 答案：$2$

相似矩阵有相同的迹，而
$$
\operatorname{tr}(\alpha\beta^T)=\beta^T\alpha.
$$
已知相似矩阵的迹为 $2$，故
$$
\beta^T\alpha=2.
$$

### 第 15 题

- 答案：$\dfrac14$

利用展开式
$$
1-\cos x=\frac{x^2}{2}+O(x^4),\qquad \tan x=x+\frac{x^3}{3}+O(x^5),
$$
以及
$$
\ln(1+\tan x)=x-\frac{x^2}{2}+\frac{2x^3}{3}+O(x^4).
$$
因而
$$
x-\ln(1+\tan x)=\frac{x^2}{2}+O(x^3),
$$
所以分子为
$$
\left(\frac{x^2}{2}+O(x^4)\right)\left(\frac{x^2}{2}+O(x^3)\right)=\frac{x^4}{4}+o(x^4).
$$
又 $\sin^4x=x^4+o(x^4)$，故极限为 $\dfrac14$。

### 第 16 题

- 答案：$$
\int \ln\!\left(1+\sqrt{\frac{1+x}{x}}\right)\,dx
=(x+1)\ln\!\left(1+\sqrt{\frac{1+x}{x}}\right)+\sqrt{x(x+1)}+C.
$$

令
$$
t=\sqrt{\frac{1+x}{x}},
$$
则可化为关于 $t$ 的有理函数积分。整理后做分部积分，或直接对结果求导核对，
可得一个原函数为
$$
F(x)=(x+1)\ln\!\left(1+\sqrt{\frac{1+x}{x}}\right)+\sqrt{x(x+1)}.
$$
验证 $F'(x)$ 即为被积函数，因此答案成立。

### 第 17 题

- 答案：记
$$
u=x+y,\quad v=x-y,\quad w=xy,
$$
则
$$
dz=(f_u+f_v+yf_w)\,dx+(f_u-f_v+xf_w)\,dy,
$$
且
$$
z_{xy}=f_{uu}-f_{vv}+(x+y)f_{uw}+(x-y)f_{vw}+xyf_{ww}+f_w.
$$

设 $u=x+y,\ v=x-y,\ w=xy$，则 $z=f(u,v,w)$。
由链式法则，
$$
z_x=f_u u_x+f_v v_x+f_w w_x=f_u+f_v+yf_w,
$$
$$
z_y=f_u u_y+f_v v_y+f_w w_y=f_u-f_v+xf_w.
$$
因而
$$
dz=z_x\,dx+z_y\,dy.
$$
再对 $z_x$ 关于 $y$ 求偏导，继续应用链式法则即可得到所示的 $z_{xy}$ 公式。

### 第 18 题

- 答案：$\dfrac{17\pi}{6}$

方程可写为
$$
\left(\frac{y'}x\right)'=-\frac{2}{x^2},
$$
积分得通解
$$
y=x^2+C_1x+C_2.
$$
又因曲线过原点，故 $C_2=0$。由面积条件
$$
\int_0^1 y(x)\,dx=2
$$
求得 $C_1=\dfrac32$，所以
$$
y=x^2+\frac32x.
$$
反解为
$$
x=\frac{-3+\sqrt{9+16y}}{4},
$$
用壳层法或圆盘法计算绕 $y$ 轴旋转体积，可得
$$
V=2\pi\int_0^1 x\,y(x)\,dx=\frac{17\pi}{6}.
$$

### 第 19 题

- 答案：$-\dfrac{8}{3}$

作平移
$$
u=x-1,\quad v=y-1,
$$
则区域化为半圆盘
$$
u^2+v^2\le 2,\quad v\ge u,
$$
而被积函数变为 $u-v$。再改用极坐标即可：
$$
u=r\cos\theta,\quad v=r\sin\theta,\quad
0\le r\le \sqrt2,\quad \frac{\pi}{4}\le\theta\le\frac{5\pi}{4}.
$$
因而
$$
\iint_D(x-y)\,dx\,dy
=\int_{\pi/4}^{5\pi/4}\int_0^{\sqrt2}r^2(\cos\theta-\sin\theta)\,dr\,d\theta
=-\frac83.
$$

### 第 20 题

- 答案：$$
y(x)=
\begin{cases}
\sqrt{\pi^2-x^2}, & -\pi<x<0,\\[2mm]
\pi\cos x+\sin x-x, & 0\le x<\pi.
\end{cases}
$$

当 $-\pi<x<0$ 时，法线过原点意味着切线斜率满足
$$
y'=-\frac{x}{y},
$$
从而
$$
y\,dy=-x\,dx,\qquad x^2+y^2=C.
$$
代入已知点得 $C=\pi^2$，又 $y>0$，故
$$
y=\sqrt{\pi^2-x^2}.
$$
当 $0\le x<\pi$ 时，方程通解为
$$
y=c_1\cos x+c_2\sin x-x.
$$
由曲线在 $x=0$ 处连续且可导，联立
$$
y(0^-)=y(0^+)=\pi,\qquad y'(0^-)=y'(0^+)=0
$$
得 $c_1=\pi,\ c_2=1$，从而得到所求分段表达式。

### 第 21 题

- 答案：见解析

（Ⅰ）构造辅助函数
$$
\phi(x)=f(x)-f(a)-\frac{f(b)-f(a)}{b-a}(x-a).
$$
则 $\phi(a)=\phi(b)=0$，由罗尔定理知存在 $\xi\in(a,b)$ 使
$$
\phi'(\xi)=0,
$$
即
$$
f'(\xi)=\frac{f(b)-f(a)}{b-a}.
$$

（Ⅱ）对任意 $x\in(0,\delta)$，把拉格朗日中值定理应用到 $[0,x]$ 上，
存在 $\xi_x\in(0,x)$ 使
$$
\frac{f(x)-f(0)}x=f'(\xi_x).
$$
当 $x\to0^+$ 时，$\xi_x\to0^+$，故右端趋于 $A$，于是
$$
\lim_{x\to0^+}\frac{f(x)-f(0)}x=A.
$$
这正是 $f_+'(0)$ 存在且等于 $A$。

### 第 22 题

- 答案：$$
\xi_2=
\begin{pmatrix}
1\\-1\\0
\end{pmatrix}
+k_1
\begin{pmatrix}
1\\1\\0
\end{pmatrix},
\qquad
\xi_3=
\begin{pmatrix}
0\\0\\2
\end{pmatrix}
+k_2
\begin{pmatrix}
1\\1\\0
\end{pmatrix},
\quad k_1,k_2\in\mathbb R.
$$
且任意此类 $\xi_2,\xi_3$ 与 $\xi_1$ 线性无关。

解线性方程组 $A\xi_2=\xi_1$，可得其通解为
$$
\xi_2=
\begin{pmatrix}
1\\-1\\0
\end{pmatrix}
+k_1
\begin{pmatrix}
1\\1\\0
\end{pmatrix}.
$$
再解 $A^2\xi_3=\xi_1$，可先写成 $A(A\xi_3)=\xi_1$，得到
$$
\xi_3=
\begin{pmatrix}
0\\0\\2
\end{pmatrix}
+k_2
\begin{pmatrix}
1\\1\\0
\end{pmatrix}.
$$
对任意 $k_1,k_2$，计算三向量构成的行列式可得
$$
\det(\xi_1,\xi_2,\xi_3)=2\ne0,
$$
因而 $\xi_1,\xi_2,\xi_3$ 线性无关。

### 第 23 题

- 答案：特征值为
$$
\lambda_1=a,\qquad \lambda_2=a-2,\qquad \lambda_3=a+1.
$$
当规范形为 $y_1^2+y_2^2$ 时，
$$
a=2.
$$

二次型对应矩阵为
$$
A=
\begin{pmatrix}
a&0&1\\
0&a&-1\\
1&-1&a-1
\end{pmatrix}.
$$
计算特征多项式
$$
|A-\lambda E|
$$
可分解为
$$
(a-\lambda)(a-\lambda-2)(a-\lambda+1),
$$
因而特征值分别为 $a,\ a-2,\ a+1$。
若规范形为 $y_1^2+y_2^2$，则应有两个正特征值、一个零特征值。
逐一检验三者为零的情形，只有
$$
a-2=0
$$
时得到特征值组 $(2,0,3)$，满足要求，故 $a=2$。
