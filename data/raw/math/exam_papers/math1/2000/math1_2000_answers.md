# Math 1 2000 Answers

资料类型：考研数学一答案解析
年份：2000
科目：数学一
范围：试卷 I
来源：D:\百度网盘\高数资料\【02】1987-2022年数学一真题详解答案（PDF）\2000考研数学一真题解析.pdf
校对状态：已按答案页图像和题干重新整理，去除识别碎行、串题内容和非本题页脚。

## 答案速查

| 题号 | 题型 | 答案 |
|---|---|---|
| 1 | 填空题 | $\dfrac{\pi}{4}$ |
| 2 | 填空题 | $\displaystyle \frac{x-1}{2}=\frac{y+2}{-8}=\frac{z-2}{12}$ |
| 3 | 填空题 | $y=\dfrac{C_1}{x^2}+C_2$ |
| 4 | 填空题 | $-1$ |
| 5 | 填空题 | $\dfrac{2}{3}$ |
| 6 | 选择题 | A |
| 7 | 选择题 | C |
| 8 | 选择题 | D |
| 9 | 选择题 | D |
| 10 | 选择题 | B |
| 11 | 解答题 | $1$ |
| 12 | 解答题 | $f_1-\dfrac{1}{y^2}f_2+xy f_{11}-\dfrac{x}{y^3}f_{22}-\dfrac{1}{x^2}g'-\dfrac{y}{x^3}g''$ |
| 13 | 解答题 | $\pi$ |
| 14 | 解答题 | $\displaystyle f(x)=\frac{e^x(e^x-1)}{x}$ |
| 15 | 解答题 | 收敛区间为 $[-3,3)$；在 $x=-3$ 处收敛，在 $x=3$ 处发散 |
| 16 | 解答题 | 重心在直径 $OP_0$ 的反向延长线上，距球心 $O$ 为 $\dfrac{R}{4}$；若取 $OP_0$ 为正 $x$ 轴，则重心为 $\left(-\dfrac{R}{4},0,0\right)$ |
| 17 | 解答题 | 在 $(0,\pi)$ 内至少有两个不同的零点 |
| 18 | 解答题 | $\displaystyle B=\begin{pmatrix}6&0&0&0\\0&6&0&0\\6&0&6&0\\0&3&0&-1\end{pmatrix}$ |
| 19 | 解答题 | $(1)\ A=\begin{pmatrix}\frac{9}{10}&\frac{2}{5}\\[2pt]\frac{1}{10}&\frac{3}{5}\end{pmatrix}$；$(2)\ \lambda_1=1,\ \lambda_2=\frac{1}{2}$；$(3)\ \displaystyle \begin{pmatrix}x_{n+1}\\y_{n+1}\end{pmatrix}=\frac{1}{10}\begin{pmatrix}8-3\left(\frac{1}{2}\right)^n\\2+3\left(\frac{1}{2}\right)^n\end{pmatrix}$ |
| 20 | 解答题 | $E(X)=\dfrac{1}{p},\quad D(X)=\dfrac{1-p}{p^2}$ |
| 21 | 解答题 | $\hat\theta=\min\{x_1,x_2,\ldots,x_n\}$ |

## 详细解析

### 第 1 题
- 答案：$\dfrac{\pi}{4}$

因为
$$
2x-x^2=1-(x-1)^2,
$$
所以
$$
\int_0^1\sqrt{2x-x^2}\,dx
=\int_0^1\sqrt{1-(x-1)^2}\,dx.
$$

令 $t=x-1$，则积分化为
$$
\int_{-1}^{0}\sqrt{1-t^2}\,dt.
$$

这是单位圆左下四分之一圆的面积，故
$$
\int_{-1}^{0}\sqrt{1-t^2}\,dt=\frac{\pi}{4}.
$$

### 第 2 题
- 答案：$\displaystyle \frac{x-1}{2}=\frac{y+2}{-8}=\frac{z-2}{12}$

设
$$
F(x,y,z)=x^2+2y^2+3z^2-21.
$$

曲面在点 $(1,-2,2)$ 处的法向量为
$$
\nabla F(1,-2,2)
=(2x,4y,6z)\big|_{(1,-2,2)}
=(2,-8,12).
$$

因此法线方程为
$$
\frac{x-1}{2}=\frac{y+2}{-8}=\frac{z-2}{12}.
$$

也可同除以 $2$ 写成
$$
\frac{x-1}{1}=\frac{y+2}{-4}=\frac{z-2}{6}.
$$

### 第 3 题
- 答案：$y=\dfrac{C_1}{x^2}+C_2$

令
$$
p=y',
$$
则原方程化为
$$
xp'+3p=0.
$$

分离变量得
$$
\frac{dp}{p}=-3\frac{dx}{x},
$$
故
$$
p=Cx^{-3}.
$$

即
$$
y'=Cx^{-3}.
$$

再积分可得
$$
y=C_1x^{-2}+C_2
=\frac{C_1}{x^2}+C_2.
$$

### 第 4 题
- 答案：$-1$

系数矩阵行列式为
$$
\begin{vmatrix}
1&2&1\\
2&3&a+2\\
1&a&-2
\end{vmatrix}
=-(a-3)(a+1).
$$

当 $a\ne -1,3$ 时，系数矩阵可逆，方程组有唯一解，因此不可能无解。

当 $a=-1$ 时，增广矩阵作初等行变换。用第 $2$ 行减去第 $1$ 行的 $2$ 倍、用第 $3$ 行减去第 $1$ 行，得到
$$
\begin{pmatrix}
1&2&1&1\\
0&-1&-1&1\\
0&-3&-3&-1
\end{pmatrix}.
$$
后两行左端成比例，但右端不成比例，所以系数矩阵的秩小于增广矩阵的秩，方程组无解。

当 $a=3$ 时，系数矩阵与增广矩阵秩相同且小于未知量个数，方程组有无穷多解。

故无解时
$$
a=-1.
$$

### 第 5 题
- 答案：$\dfrac{2}{3}$

设
$$
P(A)=p,\qquad P(B)=q.
$$

由 $A,B$ 相互独立，有
$$
P(\overline A\overline B)=(1-p)(1-q)=\frac{1}{9}.
$$

又
$$
P(A\overline B)=P(\overline A B),
$$
即
$$
p(1-q)=(1-p)q.
$$
化简得
$$
p=q.
$$

于是
$$
(1-p)^2=\frac{1}{9}.
$$
因 $0\le p\le1$，所以 $1-p=\dfrac{1}{3}$，从而
$$
P(A)=p=\frac{2}{3}.
$$

### 第 6 题
- 答案：A

由
$$
f'(x)g(x)-f(x)g'(x)<0
$$
且 $g(x)>0$，得
$$
\left(\frac{f(x)}{g(x)}\right)'
=\frac{f'(x)g(x)-f(x)g'(x)}{g^2(x)}<0.
$$

所以 $\dfrac{f(x)}{g(x)}$ 在区间内单调递减。若 $a<x<b$，则
$$
\frac{f(x)}{g(x)}>\frac{f(b)}{g(b)}.
$$

两边同乘正数 $g(x)g(b)$，得
$$
f(x)g(b)>f(b)g(x).
$$

故选 A。

### 第 7 题
- 答案：C

曲面 $S$ 是上半球面。因 $S$ 关于 $yoz$ 平面与 $xoz$ 平面对称，且 $z$ 关于 $x,y$ 都为偶函数，所以
$$
\iint_S z\,dS
=4\iint_{S_1} z\,dS.
$$

在第一卦限球面 $S_1$ 上，区域对 $x,y,z$ 的轮换对称，曲面面积元也保持不变，因此
$$
\iint_{S_1}z\,dS=\iint_{S_1}x\,dS.
$$

于是
$$
\iint_S z\,dS
=4\iint_{S_1}x\,dS.
$$

故选 C。

### 第 8 题
- 答案：D

若
$$
\sum_{n=1}^{\infty}u_n
$$
收敛，则移位后的级数
$$
\sum_{n=1}^{\infty}u_{n+1}
=\sum_{n=2}^{\infty}u_n
$$
也收敛。

因此
$$
\sum_{n=1}^{\infty}(u_n+u_{n+1})
=\sum_{n=1}^{\infty}u_n+\sum_{n=1}^{\infty}u_{n+1}
$$
为两个收敛级数之和，必收敛。

其余选项不能保证。比如取
$$
u_n=\frac{(-1)^n}{\sqrt n},
$$
则 $\sum u_n$ 收敛，但 $\sum u_n^2=\sum\dfrac{1}{n}$ 发散；取
$$
u_n=\frac{(-1)^{n-1}}{n},
$$
则
$$
u_{2n-1}-u_{2n}=\frac{1}{2n-1}+\frac{1}{2n}\sim\frac{1}{n},
$$
对应级数发散。

故选 D。

### 第 9 题
- 答案：D

记
$$
A=(\boldsymbol{\alpha}_1,\cdots,\boldsymbol{\alpha}_m),\qquad
B=(\boldsymbol{\beta}_1,\cdots,\boldsymbol{\beta}_m).
$$

题设 $\boldsymbol{\alpha}_1,\cdots,\boldsymbol{\alpha}_m$ 线性无关，所以
$$
r(A)=m.
$$

矩阵等价的充要条件是秩相等。选项 D 表示 $A$ 与 $B$ 等价，即
$$
r(B)=r(A)=m.
$$

而 $B$ 的列向量正是 $\boldsymbol{\beta}_1,\cdots,\boldsymbol{\beta}_m$，所以
$$
r(B)=m
$$
等价于该向量组线性无关。

故选 D。

### 第 10 题
- 答案：B

随机变量 $\xi$ 与 $\eta$ 不相关的充要条件为
$$
\operatorname{Cov}(\xi,\eta)=0.
$$

由 $\xi=X+Y,\ \eta=X-Y$，得
$$
\operatorname{Cov}(\xi,\eta)
=\operatorname{Cov}(X+Y,X-Y).
$$

利用协方差的双线性性：
$$
\operatorname{Cov}(X+Y,X-Y)
=\operatorname{Cov}(X,X)-\operatorname{Cov}(X,Y)
+\operatorname{Cov}(Y,X)-\operatorname{Cov}(Y,Y).
$$

由于 $\operatorname{Cov}(X,Y)=\operatorname{Cov}(Y,X)$，上式化为
$$
\operatorname{Cov}(\xi,\eta)=D(X)-D(Y).
$$

所以不相关当且仅当
$$
D(X)=D(Y),
$$
即
$$
E(X^2)-[E(X)]^2=E(Y^2)-[E(Y)]^2.
$$

故选 B。

### 第 11 题
- 答案：$1$

分别求左右极限。

当 $x\to0^+$ 时，
$$
\frac{2+e^{1/x}}{1+e^{4/x}}
=\frac{2e^{-4/x}+e^{-3/x}}{e^{-4/x}+1}\to0,
$$
且
$$
\frac{\sin x}{|x|}=\frac{\sin x}{x}\to1.
$$
故右极限为 $1$。

当 $x\to0^-$ 时，
$$
e^{1/x}\to0,\qquad e^{4/x}\to0,
$$
所以
$$
\frac{2+e^{1/x}}{1+e^{4/x}}\to2.
$$
同时
$$
\frac{\sin x}{|x|}
=-\frac{\sin x}{x}\to-1.
$$
故左极限为 $2-1=1$。

左右极限相等，因此原极限为
$$
1.
$$

### 第 12 题
- 答案：$f_1-\dfrac{1}{y^2}f_2+xy f_{11}-\dfrac{x}{y^3}f_{22}-\dfrac{1}{x^2}g'-\dfrac{y}{x^3}g''$

以下记
$$
u=xy,\qquad v=\frac{x}{y},\qquad w=\frac{y}{x}.
$$
其中 $f_i,f_{ij}$ 均表示 $f(u,v)$ 对相应变量的偏导数，$g',g''$ 均在 $w=\dfrac{y}{x}$ 处取值。

先对 $x$ 求偏导：
$$
\frac{\partial z}{\partial x}
=y f_1+\frac{1}{y} f_2-\frac{y}{x^2}g'.
$$

再对 $y$ 求偏导。第一项给出
$$
\frac{\partial}{\partial y}(y f_1)
=f_1+y\left(xf_{11}-\frac{x}{y^2}f_{12}\right).
$$

第二项给出
$$
\frac{\partial}{\partial y}\left(\frac{1}{y} f_2\right)
=-\frac{1}{y^2}f_2+\frac{1}{y}\left(xf_{21}-\frac{x}{y^2}f_{22}\right).
$$

由于 $f$ 具有二阶连续偏导数，$f_{12}=f_{21}$，交叉项相消。第三项给出
$$
\frac{\partial}{\partial y}\left(-\frac{y}{x^2}g'\right)
=-\frac{1}{x^2}g'-\frac{y}{x^3}g''.
$$

合并得
$$
\frac{\partial^2 z}{\partial x\partial y}
=f_1-\frac{1}{y^2}f_2+xy f_{11}-\frac{x}{y^3}f_{22}
-\frac{1}{x^2}g'-\frac{y}{x^3}g''.
$$

### 第 13 题
- 答案：$\pi$

记
$$
P(x,y)=\frac{-y}{4x^2+y^2},\qquad
Q(x,y)=\frac{x}{4x^2+y^2}.
$$

在 $(x,y)\ne(0,0)$ 处有
$$
\frac{\partial P}{\partial x}
=\frac{8xy}{(4x^2+y^2)^2}
=\frac{\partial Q}{\partial y}.
$$

由于圆周 $L$ 包含原点，不能直接在整个圆域内用格林公式。取足够小的椭圆
$$
L_1:\quad x=\frac{\varepsilon}{2}\cos t,\quad y=\varepsilon\sin t,\quad 0\le t\le2\pi,
$$
逆时针方向。$L$ 与 $L_1$ 围成的环域内被积函数满足格林公式条件，因此原积分等于沿 $L_1$ 的积分。

沿 $L_1$，
$$
dx=-\frac{\varepsilon}{2}\sin t\,dt,\qquad
dy=\varepsilon\cos t\,dt,
$$
且
$$
4x^2+y^2=\varepsilon^2.
$$

于是
$$
I=\int_0^{2\pi}
\frac{(\varepsilon/2\cos t)(\varepsilon\cos t)
-(\varepsilon\sin t)(-\varepsilon/2\sin t)}
{\varepsilon^2}\,dt
=\int_0^{2\pi}\frac{1}{2}\,dt
=\pi.
$$

### 第 14 题
- 答案：$\displaystyle f(x)=\frac{e^x(e^x-1)}{x}$

把曲面积分写成高斯公式的形式：
$$
\oiint_S P\,dy\,dz+Q\,dz\,dx+R\,dx\,dy=0,
$$
其中
$$
P=xf(x),\qquad Q=-xyf(x),\qquad R=-e^{2x}z.
$$

由高斯公式，对半空间 $x>0$ 内任意光滑封闭曲面都有
$$
\iiint_\Omega
\left(\frac{\partial P}{\partial x}
+\frac{\partial Q}{\partial y}
+\frac{\partial R}{\partial z}\right)\,dV=0.
$$

曲面任意，故散度恒为 $0$：
$$
xf'(x)+f(x)-xf(x)-e^{2x}=0,\qquad x>0.
$$

化为一阶线性微分方程
$$
f'(x)+\left(\frac{1}{x}-1\right)f(x)=\frac{1}{x} e^{2x}.
$$

积分因子为
$$
\mu(x)=e^{\int(1/x-1)\,dx}=xe^{-x}.
$$

于是
$$
\bigl(xe^{-x}f(x)\bigr)'=e^x.
$$

积分得
$$
xe^{-x}f(x)=e^x+C,
$$
即
$$
f(x)=\frac{e^{2x}+Ce^x}{x}.
$$

又
$$
\lim_{x\to0^+}f(x)=1
$$
要求分子在 $x=0$ 的零阶项为 $0$，故 $1+C=0$，即 $C=-1$。因此
$$
f(x)=\frac{e^{2x}-e^x}{x}
=\frac{e^x(e^x-1)}{x}.
$$

### 第 15 题
- 答案：收敛区间为 $[-3,3)$；在 $x=-3$ 处收敛，在 $x=3$ 处发散

记幂级数系数为
$$
a_n=\frac{1}{n\bigl(3^n+(-2)^n\bigr)}.
$$

由相邻项比值可知
$$
\lim_{n\to\infty}\left|\frac{a_{n+1}}{a_n}\right|
=\frac{1}{3},
$$
故收敛半径为
$$
R=3.
$$

当 $x=3$ 时，级数为
$$
\sum_{n=1}^{\infty}
\frac{3^n}{n\bigl(3^n+(-2)^n\bigr)}
=\sum_{n=1}^{\infty}
\frac{1}{n\left(1+(-2/3)^n\right)}.
$$
其通项与 $\dfrac{1}{n}$ 等价，故发散。

当 $x=-3$ 时，
$$
\frac{(-3)^n}{n\bigl(3^n+(-2)^n\bigr)}
=\frac{(-1)^n}{n}
-\frac{(2/3)^n}{n\left(1+(-2/3)^n\right)}.
$$

第一部分为交错调和级数，收敛；第二部分由几何级数控制，绝对收敛。因此 $x=-3$ 处收敛。

综上，收敛区间为
$$
[-3,3).
$$

### 第 16 题
- 答案：重心在直径 $OP_0$ 的反向延长线上，距球心 $O$ 为 $\dfrac{R}{4}$；若取 $OP_0$ 为正 $x$ 轴，则重心为 $\left(-\dfrac{R}{4},0,0\right)$

以球心 $O$ 为原点，取射线 $OP_0$ 为正 $x$ 轴，则球体为
$$
x^2+y^2+z^2\le R^2,
$$
且
$$
P_0=(R,0,0).
$$

球内点 $(x,y,z)$ 到 $P_0$ 的距离平方为
$$
(x-R)^2+y^2+z^2,
$$
所以密度可写为
$$
\mu=k\bigl((x-R)^2+y^2+z^2\bigr)
=k(x^2+y^2+z^2+R^2-2Rx).
$$

由对称性，
$$
\bar y=\bar z=0.
$$

质量为
$$
M=\iiint_\Omega \mu\,dV
=k\iiint_\Omega (x^2+y^2+z^2+R^2)\,dV,
$$
因为 $\iiint_\Omega x\,dV=0$。又
$$
\iiint_\Omega (x^2+y^2+z^2)\,dV=\frac{4\pi R^5}{5},
\qquad
\iiint_\Omega R^2\,dV=\frac{4\pi R^5}{3}.
$$
故
$$
M=k\left(\frac{4\pi R^5}{5}+\frac{4\pi R^5}{3}\right)
=\frac{32k\pi R^5}{15}.
$$

关于 $yz$ 平面的矩为
$$
\iiint_\Omega x\mu\,dV
=k\iiint_\Omega x(x^2+y^2+z^2+R^2)\,dV
-2kR\iiint_\Omega x^2\,dV.
$$
第一项为奇函数积分，等于 $0$。并且
$$
\iiint_\Omega x^2\,dV
=\frac{1}{3}\iiint_\Omega (x^2+y^2+z^2)\,dV
=\frac{4\pi R^5}{15}.
$$
故
$$
\iiint_\Omega x\mu\,dV
=-\frac{8k\pi R^6}{15}.
$$

于是
$$
\bar x
=\frac{-8k\pi R^6/15}{32k\pi R^5/15}
=-\frac{R}{4}.
$$

所以重心坐标为
$$
\left(-\frac{R}{4},0,0\right).
$$

### 第 17 题
- 答案：在 $(0,\pi)$ 内至少有两个不同的零点

令
$$
F(x)=\int_0^x f(t)\,dt,\qquad 0\le x\le\pi.
$$

由题设
$$
\int_0^\pi f(x)\,dx=0
$$
得
$$
F(0)=F(\pi)=0.
$$

又由
$$
\int_0^\pi f(x)\cos x\,dx=0,
$$
分部积分得
$$
0=\int_0^\pi \cos x\,dF(x)
=F(x)\cos x\big|_0^\pi+\int_0^\pi F(x)\sin x\,dx.
$$
由于 $F(0)=F(\pi)=0$，故
$$
\int_0^\pi F(x)\sin x\,dx=0.
$$

在 $(0,\pi)$ 内 $\sin x>0$。由积分中值定理，存在 $\xi\in(0,\pi)$，使
$$
F(\xi)=0.
$$

于是 $F$ 在 $[0,\xi]$ 上满足 $F(0)=F(\xi)=0$，由罗尔定理，存在
$$
\xi_1\in(0,\xi)
$$
使
$$
F'(\xi_1)=f(\xi_1)=0.
$$

同理，$F$ 在 $[\xi,\pi]$ 上满足 $F(\xi)=F(\pi)=0$，存在
$$
\xi_2\in(\xi,\pi)
$$
使
$$
F'(\xi_2)=f(\xi_2)=0.
$$

因此 $f(x)$ 在 $(0,\pi)$ 内至少有两个不同的零点。

### 第 18 题
- 答案：$\displaystyle B=\begin{pmatrix}6&0&0&0\\0&6&0&0\\6&0&6&0\\0&3&0&-1\end{pmatrix}$

由伴随矩阵性质
$$
AA^*=A^*A=(\det A)E.
$$

由于 $A$ 为 $4$ 阶矩阵，且
$$
\det(A^*)=(\det A)^{3}.
$$
由题中 $A^*$ 可得 $\det(A^*)=8$，故
$$
\det A=2.
$$

题设
$$
ABA^{-1}=BA^{-1}+3E.
$$
两边右乘 $A$，得
$$
AB=B+3A.
$$
两边左乘 $A^*$，得
$$
A^*AB=A^*B+3A^*A.
$$

利用 $A^*A=2E$，化简为
$$
2B=A^*B+6E,
$$
即
$$
(2E-A^*)B=6E.
$$

因此
$$
B=6(2E-A^*)^{-1}.
$$

而
$$
2E-A^*
=\begin{pmatrix}
1&0&0&0\\
0&1&0&0\\
-1&0&1&0\\
0&3&0&-6
\end{pmatrix},
$$
其逆矩阵为
$$
(2E-A^*)^{-1}
=\begin{pmatrix}
1&0&0&0\\
0&1&0&0\\
1&0&1&0\\
0&\frac{1}{2}&0&-\frac{1}{6}
\end{pmatrix}.
$$

故
$$
B=6(2E-A^*)^{-1}
=\begin{pmatrix}
6&0&0&0\\
0&6&0&0\\
6&0&6&0\\
0&3&0&-1
\end{pmatrix}.
$$

### 第 19 题
- 答案：$(1)\ A=\begin{pmatrix}\frac{9}{10}&\frac{2}{5}\\[2pt]\frac{1}{10}&\frac{3}{5}\end{pmatrix}$；$(2)\ \lambda_1=1,\ \lambda_2=\frac{1}{2}$；$(3)\ \displaystyle \begin{pmatrix}x_{n+1}\\y_{n+1}\end{pmatrix}=\frac{1}{10}\begin{pmatrix}8-3\left(\frac{1}{2}\right)^n\\2+3\left(\frac{1}{2}\right)^n\end{pmatrix}$

(1) 第 $n$ 年一月份熟练工比例为 $x_n$，非熟练工比例为 $y_n$。年初支援后留下的熟练工为
$$
\frac{5}{6}x_n.
$$
年内非熟练工共有
$$
\frac{1}{6}x_n+y_n,
$$
其中 $\dfrac{2}{5}$ 转为熟练工，$\dfrac{3}{5}$ 仍为非熟练工。

所以
$$
x_{n+1}=\frac{5}{6}x_n+\frac{2}{5}\left(\frac{1}{6}x_n+y_n\right)
=\frac{9}{10}x_n+\frac{2}{5}y_n,
$$
$$
y_{n+1}=\frac{3}{5}\left(\frac{1}{6}x_n+y_n\right)
=\frac{1}{10}x_n+\frac{3}{5}y_n.
$$

因此
$$
\begin{pmatrix}
x_{n+1}\\y_{n+1}
\end{pmatrix}
=
\begin{pmatrix}
\frac{9}{10}&\frac{2}{5}\\
\frac{1}{10}&\frac{3}{5}
\end{pmatrix}
\begin{pmatrix}
x_n\\y_n
\end{pmatrix}.
$$

(2) 记
$$
A=\begin{pmatrix}
\frac{9}{10}&\frac{2}{5}\\
\frac{1}{10}&\frac{3}{5}
\end{pmatrix}.
$$

直接计算：
$$
A\begin{pmatrix}4\\1\end{pmatrix}
=\begin{pmatrix}4\\1\end{pmatrix},
$$
所以 $\boldsymbol\eta_1=(4,1)^T$ 对应特征值
$$
\lambda_1=1.
$$

又
$$
A\begin{pmatrix}-1\\1\end{pmatrix}
=\begin{pmatrix}-\frac{1}{2}\\\frac{1}{2}\end{pmatrix}
=\frac{1}{2}\begin{pmatrix}-1\\1\end{pmatrix},
$$
所以 $\boldsymbol\eta_2=(-1,1)^T$ 对应特征值
$$
\lambda_2=\frac{1}{2}.
$$

并且
$$
\det\begin{pmatrix}4&-1\\1&1\end{pmatrix}=5\ne0,
$$
故两个特征向量线性无关。

(3) 令
$$
P=(\boldsymbol\eta_1,\boldsymbol\eta_2)
=\begin{pmatrix}4&-1\\1&1\end{pmatrix}.
$$

则
$$
A=P
\begin{pmatrix}
1&0\\0&\frac{1}{2}
\end{pmatrix}
P^{-1}.
$$
于是
$$
A^n
=\frac{1}{5}
\begin{pmatrix}
4+\left(\frac{1}{2}\right)^n&4-4\left(\frac{1}{2}\right)^n\\
1-\left(\frac{1}{2}\right)^n&1+4\left(\frac{1}{2}\right)^n
\end{pmatrix}.
$$

由
$$
\begin{pmatrix}x_1\\y_1\end{pmatrix}
=\begin{pmatrix}\frac{1}{2}\\\frac{1}{2}\end{pmatrix}
$$
得
$$
\begin{pmatrix}x_{n+1}\\y_{n+1}\end{pmatrix}
=A^n\begin{pmatrix}\frac{1}{2}\\\frac{1}{2}\end{pmatrix}
=\frac{1}{10}
\begin{pmatrix}
8-3\left(\frac{1}{2}\right)^n\\
2+3\left(\frac{1}{2}\right)^n
\end{pmatrix}.
$$

### 第 20 题
- 答案：$E(X)=\dfrac{1}{p},\quad D(X)=\dfrac{1-p}{p^2}$

设
$$
q=1-p.
$$

$X=k$ 表示前 $k-1$ 个产品均合格，第 $k$ 个产品不合格。因此
$$
P\{X=k\}=q^{k-1}p,\qquad k=1,2,\ldots
$$
这就是参数为 $p$、取值从 $1$ 开始的几何分布。

数学期望为
$$
E(X)=\sum_{k=1}^{\infty}kq^{k-1}p
=p\sum_{k=1}^{\infty}kq^{k-1}.
$$
由
$$
\sum_{k=1}^{\infty}kq^{k-1}=\frac{1}{(1-q)^2}
$$
得
$$
E(X)=p\cdot\frac{1}{p^2}=\frac{1}{p}.
$$

同理，
$$
E(X^2)=\sum_{k=1}^{\infty}k^2q^{k-1}p
=\frac{2-p}{p^2}.
$$

所以
$$
D(X)=E(X^2)-[E(X)]^2
=\frac{2-p}{p^2}-\frac{1}{p^2}
=\frac{1-p}{p^2}.
$$

### 第 21 题
- 答案：$\hat\theta=\min\{x_1,x_2,\ldots,x_n\}$

样本观测值为 $x_1,\ldots,x_n$。似然函数为
$$
L(\theta)
=\prod_{i=1}^n f(x_i;\theta).
$$

当且仅当
$$
\theta\le x_i,\qquad i=1,2,\ldots,n
$$
时，似然函数非零。此时
$$
L(\theta)
=\prod_{i=1}^n 2e^{-2(x_i-\theta)}
=2^n e^{-2\sum_{i=1}^n(x_i-\theta)}.
$$

取对数：
$$
\ln L(\theta)
=n\ln2-2\sum_{i=1}^n x_i+2n\theta.
$$

在允许范围
$$
\theta\le \min\{x_1,\ldots,x_n\}
$$
内，$\ln L(\theta)$ 关于 $\theta$ 单调递增，因此取允许的最大值时似然函数最大。

所以
$$
\hat\theta=\min\{x_1,x_2,\ldots,x_n\}.
$$
