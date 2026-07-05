# Math 1 1997 Answers

资料类型：考研数学一答案解析
年份：1997
科目：数学一
范围：试卷 I
来源：D:\百度网盘\高数资料\【02】1987-2022年数学一真题详解答案（PDF）\1997考研数学一真题解析.pdf
校对状态：已按题干和答案页图像重新清洗，去除 OCR 碎行、串题内容和非本题页脚

## 答案速查

| 题号 | 题型 | 答案 |
|---|---|---|
| 1 | 填空题 | $\dfrac{3}{2}$ |
| 2 | 填空题 | $(-2,4)$ |
| 3 | 填空题 | $x+y=e^{\pi/2}$ |
| 4 | 填空题 | $t=-3$ |
| 5 | 填空题 | $\dfrac{2}{5}$ |
| 6 | 选择题 | C |
| 7 | 选择题 | B |
| 8 | 选择题 | A |
| 9 | 选择题 | D |
| 10 | 选择题 | D |
| 11 | 解答题 | $\dfrac{1024\pi}{3}$ |
| 12 | 解答题 | $-2\pi$ |
| 13 | 解答题 | $\displaystyle x(t)=\frac{Nx_0e^{kNt}}{N-x_0+x_0e^{kNt}}$ |
| 14 | 解答题 | $a=-5,\ b=-2$ |
| 15 | 解答题 | $f(u)=C_1e^u+C_2e^{-u}$ |
| 16 | 解答题 | $\displaystyle \varphi'(x)=\frac{x f(x)-\int_0^x f(u)\,du}{x^2}\ (x\ne0),\quad \varphi'(0)=\dfrac{A}{2}$，且 $\varphi'(x)$ 在 $x=0$ 处连续 |
| 17 | 解答题 | 见解析；极限存在且等于 $1$，所给级数收敛 |
| 18 | 解答题 | $\displaystyle \left\{\frac{1}{\sqrt{15}}(1,1,2,3)^T,\ \frac{1}{\sqrt{39}}(-2,1,5,-3)^T\right\}$ |
| 19 | 解答题 | $a=-3,\ b=0$，对应特征值 $\lambda=-1$；$A$ 不能相似于对角矩阵 |
| 20 | 解答题 | 见解析；$AB^{-1}=E_{ij}$，其中 $E_{ij}$ 为交换第 $i,j$ 行的初等矩阵 |
| 21 | 解答题 | $X\sim B\!\left(3,\dfrac{2}{5}\right)$，且 $E(X)=\dfrac{6}{5}$ |
| 22 | 解答题 | $\displaystyle \hat\theta_M=\frac{2\bar X-1}{1-\bar X},\qquad \hat\theta_{MLE}=-1-\frac{n}{\sum_{i=1}^n\ln X_i}$ |

## 详细解析

### 第 1 题
- 答案：$\dfrac{3}{2}$

分子、分母同除以 $x$，得
$$
\frac{3\sin x+x^2\cos\frac{1}{x}}{(1+\cos x)\ln(1+x)}
=
\frac{3\dfrac{\sin x}{x}+x\cos\frac{1}{x}}
{(1+\cos x)\dfrac{\ln(1+x)}{x}}.
$$

当 $x\to0$ 时，
$$
\frac{\sin x}{x}\to1,\qquad
x\cos\frac{1}{x}\to0,\qquad
1+\cos x\to2,\qquad
\frac{\ln(1+x)}x\to1.
$$

所以原极限为
$$
\frac{3\cdot1+0}{2\cdot1}=\frac{3}{2}.
$$

### 第 2 题
- 答案：$(-2,4)$

设 $t=x-1$，则所给幂级数变为
$$
\sum_{n=1}^{\infty} n a_n t^{\,n+1}
=t^2\sum_{n=1}^{\infty}n a_n t^{\,n-1}.
$$

已知 $\sum a_nx^n$ 的收敛半径为 $3$。逐项求导后，
$$
\sum_{n=1}^{\infty}n a_n t^{\,n-1}
$$
的收敛半径仍为 $3$，乘以 $t^2$ 不改变开区间内的收敛范围。

因此
$$
|t|<3,
$$
即
$$
-3<x-1<3.
$$

所求收敛区间为
$$
(-2,4).
$$

### 第 3 题
- 答案：$x+y=e^{\pi/2}$

极坐标曲线 $\rho=e^\theta$ 的直角坐标参数式为
$$
x=\rho\cos\theta=e^\theta\cos\theta,\qquad
y=\rho\sin\theta=e^\theta\sin\theta.
$$

求导得
$$
\frac{dx}{d\theta}=e^\theta(\cos\theta-\sin\theta),\qquad
\frac{dy}{d\theta}=e^\theta(\sin\theta+\cos\theta).
$$

当 $\theta=\dfrac{\pi}{2}$ 时，切点为
$$
(x_0,y_0)=\left(0,e^{\pi/2}\right),
$$
且
$$
\left.\frac{dy}{dx}\right|_{\theta=\pi/2}
=\frac{e^{\pi/2}}{-e^{\pi/2}}=-1.
$$

切线方程为
$$
y-e^{\pi/2}=-(x-0),
$$
即
$$
x+y=e^{\pi/2}.
$$

### 第 4 题
- 答案：$t=-3$

存在非零矩阵 $B$ 使 $AB=O$，说明线性方程组
$$
A\boldsymbol{x}=0
$$
有非零解，因此
$$
\det A=0.
$$

计算
$$
\det A=
\begin{vmatrix}
1&2&-2\\
4&t&3\\
3&-1&1
\end{vmatrix}.
$$

按第一行展开：
$$
\det A
=1(t+3)-2(4-9)-2(-4-3t)
=t+3-2(-5)-2(-4-3t).
$$

化简得
$$
\det A=7t+21=7(t+3).
$$

由 $\det A=0$，得
$$
t=-3.
$$

### 第 5 题
- 答案：$\dfrac{2}{5}$

第二个人取到黄球的概率可以按第一个人的取球结果分解：
$$
P=\frac{20}{50}\cdot\frac{19}{49}
+\frac{30}{50}\cdot\frac{20}{49}.
$$

整理得
$$
P=\frac{20\cdot19+30\cdot20}{50\cdot49}
=\frac{20(19+30)}{50\cdot49}
=\frac{20}{50}
=\frac{2}{5}.
$$

也可以理解为随机排列中任一固定位置为黄球的概率都等于总体黄球比例。

### 第 6 题
- 答案：C

沿直线 $y=x$ 趋近原点时，
$$
f(x,x)=\frac{x^2}{2x^2}=\frac{1}{2},
$$
而沿坐标轴趋近原点时，
$$
f(x,0)=0,\qquad f(0,y)=0.
$$

极限与趋近路径有关，所以 $f$ 在 $(0,0)$ 不连续。

再看偏导数：
$$
f_x(0,0)=\lim_{h\to0}\frac{f(h,0)-f(0,0)}h=0,
$$
$$
f_y(0,0)=\lim_{h\to0}\frac{f(0,h)-f(0,0)}h=0.
$$

故偏导数存在但函数不连续，选 C。

### 第 7 题
- 答案：B

因为 $f'(x)<0$，所以 $f$ 在 $[a,b]$ 上单调递减。于是对任意 $x\in[a,b]$ 有
$$
f(b)\le f(x)\le f(a),
$$
从而
$$
S_2=f(b)(b-a)<\int_a^b f(x)\,dx=S_1.
$$

又因为 $f''(x)>0$，曲线 $y=f(x)$ 是下凸的，割线位于曲线之上，即
$$
f(x)\le
\frac{b-x}{b-a}f(a)+\frac{x-a}{b-a}f(b).
$$

两边在 $[a,b]$ 上积分得
$$
S_1<\frac{1}{2}[f(a)+f(b)](b-a)=S_3.
$$

因此
$$
S_2<S_1<S_3,
$$
选 B。

### 第 8 题
- 答案：A

由于被积函数 $e^{\sin t}\sin t$ 的周期为 $2\pi$，所以
$$
F(x)=\int_x^{x+2\pi}e^{\sin t}\sin t\,dt
$$
与 $x$ 无关，是常数。

只需判断该常数符号。取一整个周期积分：
$$
F=\int_0^{2\pi}e^{\sin t}\sin t\,dt.
$$

将区间分为 $[0,\pi]$ 与 $[\pi,2\pi]$，后半段令 $u=t-\pi$，得
$$
\int_\pi^{2\pi}e^{\sin t}\sin t\,dt
=-\int_0^\pi e^{-\sin u}\sin u\,du.
$$

所以
$$
F=\int_0^\pi \bigl(e^{\sin u}-e^{-\sin u}\bigr)\sin u\,du>0,
$$
因为在 $(0,\pi)$ 上 $\sin u>0$。

故 $F(x)$ 为正常数，选 A。

### 第 9 题
- 答案：D

三条直线交于一点，等价于线性方程组
$$
\begin{cases}
a_1x+b_1y=-c_1,\\
a_2x+b_2y=-c_2,\\
a_3x+b_3y=-c_3
\end{cases}
$$
有唯一解。

系数矩阵的两列分别为 $\boldsymbol{\alpha}_1,\boldsymbol{\alpha}_2$，增广矩阵还包含 $\boldsymbol{\alpha}_3$。唯一解要求
$$
r(\boldsymbol{\alpha}_1,\boldsymbol{\alpha}_2)
=r(\boldsymbol{\alpha}_1,\boldsymbol{\alpha}_2,\boldsymbol{\alpha}_3)=2.
$$

这就是说 $\boldsymbol{\alpha}_1,\boldsymbol{\alpha}_2$ 线性无关，而三个三维列向量
$$
\boldsymbol{\alpha}_1,\boldsymbol{\alpha}_2,\boldsymbol{\alpha}_3
$$
整体线性相关。故选 D。

### 第 10 题
- 答案：D

因为 $X,Y$ 相互独立，
$$
D(3X-2Y)=3^2D(X)+(-2)^2D(Y).
$$

代入 $D(X)=4,\ D(Y)=2$：
$$
D(3X-2Y)=9\cdot4+4\cdot2=36+8=44.
$$

故选 D。

### 第 11 题
- 答案：$\dfrac{1024\pi}{3}$

曲线
$$
y^2=2z,\qquad x=0
$$
绕 $z$ 轴旋转得到曲面
$$
x^2+y^2=2z.
$$

用柱坐标 $x=r\cos\theta,\ y=r\sin\theta$，区域为
$$
0\le z\le8,\qquad 0\le r\le\sqrt{2z},\qquad 0\le\theta\le2\pi.
$$

于是
$$
I=\int_0^{2\pi}\int_0^8\int_0^{\sqrt{2z}} r^2\cdot r\,dr\,dz\,d\theta.
$$

计算得
$$
I=2\pi\int_0^8\frac{1}{4}(2z)^2\,dz
=2\pi\int_0^8 z^2\,dz
=2\pi\cdot\frac{8^3}{3}
=\frac{1024\pi}{3}.
$$

### 第 12 题
- 答案：$-2\pi$

设
$$
P=z-y,\qquad Q=x-z,\qquad R=x-y.
$$

由 Stokes 公式，
$$
\oint_C P\,dx+Q\,dy+R\,dz
=\iint_S(\nabla\times\boldsymbol F)\cdot\boldsymbol n\,dS.
$$

计算旋度：
$$
\nabla\times\boldsymbol F
=
\begin{vmatrix}
\boldsymbol i&\boldsymbol j&\boldsymbol k\\
\partial_x&\partial_y&\partial_z\\
z-y&x-z&x-y
\end{vmatrix}
=(0,0,2).
$$

曲面取平面
$$
z=2-x+y.
$$

题给方向为从 $z$ 轴正向往负向看是顺时针，因此取法向量的 $z$ 分量为负。对应有
$$
\boldsymbol n\,dS=(z_x,z_y,-1)\,dx\,dy=(-1,1,-1)\,dx\,dy.
$$

投影区域为
$$
D:x^2+y^2\le1.
$$

故
$$
I=\iint_D(0,0,2)\cdot(-1,1,-1)\,dx\,dy
=\iint_D(-2)\,dx\,dy
=-2\pi.
$$

### 第 13 题
- 答案：$\displaystyle x(t)=\frac{Nx_0e^{kNt}}{N-x_0+x_0e^{kNt}}$

由题意，变化率与已掌握人数 $x$ 和未掌握人数 $N-x$ 的乘积成正比：
$$
\frac{dx}{dt}=kx(N-x),\qquad k>0.
$$

分离变量：
$$
\frac{dx}{x(N-x)}=k\,dt.
$$

利用
$$
\frac{1}{x(N-x)}=\frac{1}{N}\left(\frac{1}{x}+\frac{1}{N-x}\right),
$$
积分得
$$
\frac{1}{N}\ln\frac{x}{N-x}=kt+C.
$$

于是
$$
\frac{x}{N-x}=Ce^{kNt}.
$$

由初值 $x(0)=x_0$ 得
$$
C=\frac{x_0}{N-x_0}.
$$

解出 $x(t)$：
$$
x(t)=\frac{Nx_0e^{kNt}}{N-x_0+x_0e^{kNt}}.
$$

### 第 14 题
- 答案：$a=-5,\ b=-2$

曲面
$$
z=x^2+y^2
$$
在点 $(1,-2,5)$ 处的切平面为
$$
z-5=2(x-1)-4(y+2),
$$
即
$$
2x-4y-z-5=0.
$$

直线
$$
l:\begin{cases}
x+y+b=0,\\
x+ay-z-3=0
\end{cases}
$$
在该切平面内，所以直线上任意点都满足切平面方程。

由第一式得
$$
y=-x-b.
$$

由第二式得
$$
z=x+ay-3=(1-a)x-ab-3.
$$

代入切平面方程：
$$
2x-4(-x-b)-[(1-a)x-ab-3]-5=0.
$$

整理为
$$
(5+a)x+4b+ab-2=0.
$$

该式对直线上的任意 $x$ 恒成立，故
$$
5+a=0,\qquad 4b+ab-2=0.
$$

解得
$$
a=-5,\qquad b=-2.
$$

### 第 15 题
- 答案：$f(u)=C_1e^u+C_2e^{-u}$

记
$$
u=e^x\sin y,\qquad z=f(u).
$$

先求一阶偏导：
$$
z_x=f'(u)e^x\sin y=f'(u)u,
$$
$$
z_y=f'(u)e^x\cos y.
$$

继续求二阶偏导：
$$
z_{xx}=f''(u)u^2+f'(u)u,
$$
$$
z_{yy}=f''(u)e^{2x}\cos^2y-f'(u)e^x\sin y.
$$

两式相加时一阶项抵消：
$$
z_{xx}+z_{yy}
=f''(u)e^{2x}(\sin^2y+\cos^2y)
=e^{2x}f''(u).
$$

题设要求
$$
z_{xx}+z_{yy}=e^{2x}z=e^{2x}f(u),
$$
因此
$$
f''(u)=f(u).
$$

解常微分方程得
$$
f(u)=C_1e^u+C_2e^{-u}.
$$

### 第 16 题
- 答案：$\displaystyle \varphi'(x)=\frac{x f(x)-\int_0^x f(u)\,du}{x^2}\ (x\ne0),\quad \varphi'(0)=\dfrac{A}{2}$，且 $\varphi'(x)$ 在 $x=0$ 处连续

当 $x\ne0$ 时，令 $u=xt$，有
$$
\varphi(x)=\int_0^1 f(xt)\,dt
=\frac{1}{x}\int_0^x f(u)\,du.
$$

求导得
$$
\varphi'(x)
=\frac{x f(x)-\int_0^x f(u)\,du}{x^2},
\qquad x\ne0.
$$

当 $x=0$ 时，由
$$
\lim_{x\to0}\frac{f(x)}x=A
$$
知 $f(0)=0$，且
$$
\varphi(0)=0.
$$

于是
$$
\varphi'(0)
=\lim_{x\to0}\frac{\varphi(x)-\varphi(0)}x
=\lim_{x\to0}\int_0^1\frac{f(xt)}x\,dt.
$$

写成
$$
\frac{f(xt)}x
=t\cdot\frac{f(xt)}{xt},
$$
由极限条件可得
$$
\varphi'(0)=\int_0^1 At\,dt=\frac{A}{2}.
$$

再证连续性。对 $x\ne0$，
$$
\varphi'(x)
=\frac{1}{x^2}\int_0^x [f(x)-f(u)]\,du.
$$
利用 $f(u)\sim Au$，
$$
x f(x)-\int_0^x f(u)\,du
\sim Ax^2-\frac{1}{2}Ax^2=\frac{1}{2}Ax^2.
$$

所以
$$
\lim_{x\to0}\varphi'(x)=\frac{A}{2}=\varphi'(0).
$$

故 $\varphi'(x)$ 在 $x=0$ 处连续。

### 第 17 题
- 答案：见解析；极限存在且等于 $1$，所给级数收敛

先证明数列极限存在。由 $a_1=2>0$ 且
$$
a_{n+1}=\frac{1}{2}\left(a_n+\frac{1}{a_n}\right)
$$
可知 $a_n>0$。

由均值不等式，
$$
a_{n+1}=\frac{1}{2}\left(a_n+\frac{1}{a_n}\right)\ge1.
$$

当 $a_n\ge1$ 时，
$$
a_{n+1}-a_n
=\frac{1}{2}\left(\frac{1}{a_n}-a_n\right)\le0.
$$
因此从 $a_1$ 起，$\{a_n\}$ 单调不增且有下界 $1$，故极限存在。

设极限为 $L$，则 $L\ge1$，并由递推式得
$$
L=\frac{1}{2}\left(L+\frac{1}{L}\right),
$$
所以
$$
L^2=1.
$$
结合 $L\ge1$，得
$$
L=1.
$$

再证级数收敛。因为 $a_{n+1}\ge1$，
$$
0\le \frac{a_n}{a_{n+1}}-1
=\frac{a_n-a_{n+1}}{a_{n+1}}
\le a_n-a_{n+1}.
$$

而
$$
\sum_{n=1}^{m}(a_n-a_{n+1})=a_1-a_{m+1}
$$
有界并收敛到 $a_1-1$。由比较判别法，
$$
\sum_{n=1}^{\infty}\left(\frac{a_n}{a_{n+1}}-1\right)
$$
收敛。

### 第 18 题
- 答案：$\displaystyle \left\{\frac{1}{\sqrt{15}}(1,1,2,3)^T,\ \frac{1}{\sqrt{39}}(-2,1,5,-3)^T\right\}$

因为 $B$ 是 $5\times4$ 矩阵且 $r(B)=2$，所以齐次方程组
$$
B\boldsymbol{x}=0
$$
的解空间维数为
$$
4-r(B)=2.
$$

题给
$$
\boldsymbol{\alpha}_1=(1,1,2,3)^T,\quad
\boldsymbol{\alpha}_2=(-1,1,4,-1)^T,\quad
\boldsymbol{\alpha}_3=(5,-1,-8,9)^T
$$
均为解向量，且
$$
\boldsymbol{\alpha}_3=2\boldsymbol{\alpha}_1-3\boldsymbol{\alpha}_2.
$$
所以可取 $\boldsymbol{\alpha}_1,\boldsymbol{\alpha}_2$ 作为解空间的一组基。

对其作 Gram-Schmidt 正交化。令
$$
\boldsymbol{\beta}_1=\boldsymbol{\alpha}_1=(1,1,2,3)^T.
$$

又
$$
\boldsymbol{\alpha}_1^T\boldsymbol{\alpha}_2=5,\qquad
\boldsymbol{\alpha}_1^T\boldsymbol{\alpha}_1=15,
$$
故
$$
\boldsymbol{\beta}_2
=\boldsymbol{\alpha}_2-\frac{5}{15}\boldsymbol{\alpha}_1
=\frac{2}{3}(-2,1,5,-3)^T.
$$

单位化得
$$
\boldsymbol{\eta}_1=\frac{1}{\sqrt{15}}(1,1,2,3)^T,
$$
$$
\boldsymbol{\eta}_2=\frac{1}{\sqrt{39}}(-2,1,5,-3)^T.
$$

因此所求标准正交基为
$$
\left\{
\frac{1}{\sqrt{15}}(1,1,2,3)^T,\ 
\frac{1}{\sqrt{39}}(-2,1,5,-3)^T
\right\}.
$$

### 第 19 题
- 答案：$a=-3,\ b=0$，对应特征值 $\lambda=-1$；$A$ 不能相似于对角矩阵

由 $\boldsymbol{\xi}=(1,1,-1)^T$ 是特征向量，设对应特征值为 $\lambda$，则
$$
A\boldsymbol{\xi}=\lambda\boldsymbol{\xi}.
$$

计算
$$
A\boldsymbol{\xi}
=
\begin{pmatrix}
2&-1&2\\
5&a&3\\
-1&b&-2
\end{pmatrix}
\begin{pmatrix}
1\\1\\-1
\end{pmatrix}
=
\begin{pmatrix}
-1\\
a+2\\
b+1
\end{pmatrix}.
$$

又
$$
\lambda\boldsymbol{\xi}=(\lambda,\lambda,-\lambda)^T.
$$

比较分量得
$$
\lambda=-1,\qquad a+2=-1,\qquad b+1=1.
$$

所以
$$
a=-3,\qquad b=0.
$$

此时
$$
A=
\begin{pmatrix}
2&-1&2\\
5&-3&3\\
-1&0&-2
\end{pmatrix}.
$$

其特征多项式为
$$
\det(\lambda E-A)=(\lambda+1)^3.
$$

唯一特征值为 $-1$，代数重数为 $3$。但
$$
r(-E-A)=2,
$$
所以对应特征子空间维数为
$$
3-r(-E-A)=1.
$$

几何重数小于代数重数，因此 $A$ 不能相似于对角矩阵。

### 第 20 题
- 答案：见解析；$AB^{-1}=E_{ij}$，其中 $E_{ij}$ 为交换第 $i,j$ 行的初等矩阵

设 $E_{ij}$ 表示交换第 $i$ 行和第 $j$ 行的初等矩阵。将 $A$ 的第 $i$ 行和第 $j$ 行对换，等价于左乘 $E_{ij}$，故
$$
B=E_{ij}A.
$$

因为 $A$ 可逆，且 $E_{ij}$ 也是可逆矩阵，所以
$$
B=E_{ij}A
$$
可逆。也可由行列式说明：
$$
\det B=\det(E_{ij})\det A=-\det A\ne0.
$$

又由于交换同两行两次即回到原矩阵，
$$
E_{ij}^{-1}=E_{ij}.
$$

于是
$$
B^{-1}=(E_{ij}A)^{-1}=A^{-1}E_{ij}^{-1}=A^{-1}E_{ij}.
$$

所以
$$
AB^{-1}=AA^{-1}E_{ij}=E_{ij}.
$$

### 第 21 题
- 答案：$X\sim B\!\left(3,\dfrac{2}{5}\right)$，且 $E(X)=\dfrac{6}{5}$

三个交通岗是否遇到红灯相互独立，且每个交通岗遇到红灯的概率为 $2/5$，所以
$$
X\sim B\left(3,\frac{2}{5}\right).
$$

因此
$$
P\{X=k\}=\binom3k\left(\frac{2}{5}\right)^k
\left(\frac{3}{5}\right)^{3-k},\qquad k=0,1,2,3.
$$

具体为
$$
\begin{array}{c|cccc}
k&0&1&2&3\\ \hline
P\{X=k\}&\dfrac{27}{125}&\dfrac{54}{125}&\dfrac{36}{125}&\dfrac{8}{125}
\end{array}
$$

分布函数为
$$
F(x)=
\begin{cases}
0,&x<0,\\
\dfrac{27}{125},&0\le x<1,\\
\dfrac{81}{125},&1\le x<2,\\
\dfrac{117}{125},&2\le x<3,\\
1,&x\ge3.
\end{cases}
$$

数学期望为
$$
E(X)=np=3\cdot\frac{2}{5}=\frac{6}{5}.
$$

### 第 22 题
- 答案：$\displaystyle \hat\theta_M=\frac{2\bar X-1}{1-\bar X},\qquad \hat\theta_{MLE}=-1-\frac{n}{\sum_{i=1}^n\ln X_i}$

先求矩估计。总体密度为
$$
f(x)=(\theta+1)x^\theta,\qquad 0<x<1,\quad \theta>-1.
$$

总体一阶矩为
$$
E(X)=\int_0^1 x(\theta+1)x^\theta\,dx
=(\theta+1)\int_0^1x^{\theta+1}\,dx
=\frac{\theta+1}{\theta+2}.
$$

令 $E(X)=\bar X$，即
$$
\frac{\theta+1}{\theta+2}=\bar X.
$$

解得矩估计量
$$
\hat\theta_M=\frac{2\bar X-1}{1-\bar X}.
$$

再求极大似然估计。样本似然函数为
$$
L(\theta)=\prod_{i=1}^n(\theta+1)X_i^\theta
=(\theta+1)^n\prod_{i=1}^nX_i^\theta.
$$

对数似然函数为
$$
\ell(\theta)=n\ln(\theta+1)+\theta\sum_{i=1}^n\ln X_i.
$$

求导：
$$
\ell'(\theta)=\frac{n}{\theta+1}+\sum_{i=1}^n\ln X_i.
$$

令 $\ell'(\theta)=0$，得
$$
\theta+1=-\frac{n}{\sum_{i=1}^n\ln X_i}.
$$

所以极大似然估计量为
$$
\hat\theta_{MLE}=-1-\frac{n}{\sum_{i=1}^n\ln X_i}.
$$
