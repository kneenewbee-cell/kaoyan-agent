# Math 1 1993 Answers

资料类型：考研数学一答案解析
年份：1993
科目：数学一
范围：试卷 I
来源：D:\百度网盘\高数资料\【02】1987-2022年数学一真题详解答案（PDF）\1993考研数一真题解析.pdf
校对状态：已按题干和答案页图像重新清洗，去除 OCR 碎行、串题内容和非本题知识点页脚

## 答案速查

| 题号 | 题型 | 答案 |
|---|---|---|
| 1 | 填空题 | $0<x\le\dfrac{1}{4}$ |
| 2 | 填空题 | $\dfrac{1}{\sqrt5}\{0,\sqrt2,\sqrt3\}$ |
| 3 | 填空题 | $\dfrac{2\pi}{3}$ |
| 4 | 填空题 | $\dfrac{1}{x^2+y^2+z^2}$ |
| 5 | 填空题 | $k(1,1,\ldots,1)^T$，其中 $k$ 为任意常数 |
| 6 | 选择题 | B |
| 7 | 选择题 | A |
| 8 | 选择题 | C |
| 9 | 选择题 | B |
| 10 | 选择题 | C |
| 11 | 解答题 | $e^2$ |
| 12 | 解答题 | $2x\sqrt{e^x-1}-4\sqrt{e^x-1}+4\arctan\sqrt{e^x-1}+C$ |
| 13 | 解答题 | $y=\dfrac{2x}{1+x^2}$ |
| 14 | 解答题 | $\dfrac{\pi}{2}$ |
| 15 | 解答题 | $\dfrac{22}{27}$ |
| 16 | 解答题 | 在 $(0,+\infty)$ 内有且仅有一个零点。 |
| 17 | 解答题 | $a^b>b^a$。 |
| 18 | 解答题 | $a=2$，可取 $x=Py$，其中 $P=\begin{pmatrix}0&1&0\\\dfrac{1}{\sqrt2}&0&\dfrac{1}{\sqrt2}\\-\dfrac{1}{\sqrt2}&0&\dfrac{1}{\sqrt2}\end{pmatrix}$ |
| 19 | 解答题 | $B$ 的列向量组线性无关。 |
| 20 | 解答题 | $2xy''+\sqrt{1+(y')^2}=0$，初始条件 $y(-1)=0,\ y'(-1)=1$ |
| 21 | 填空题 | $\dfrac{1}{6}$ |
| 22 | 填空题 | $f_Y(y)=\begin{cases}\dfrac{1}{4\sqrt y},&0<y<4,\\0,&\text{其他},\end{cases}$ |
| 23 | 解答题 | $E(X)=0,\ D(X)=2$；$\operatorname{Cov}(X,\lvert X\rvert)=0$，故 $X$ 与 $\lvert X\rvert$ 不相关；但二者不相互独立 |

## 详细解析

### 第 1 题

- 答案：$0<x\le\dfrac{1}{4}$

由变上限积分求导公式，
$$
F'(x)=2-\frac{1}{\sqrt{x}}.
$$

函数 $F(x)$ 单调减少当且仅当
$$
F'(x)\le0.
$$

于是
$$
2-\frac{1}{\sqrt{x}}\le0
\quad\Longleftrightarrow\quad
\sqrt{x}\le\frac{1}{2}
\quad\Longleftrightarrow\quad
0<x\le\frac{1}{4}.
$$

所以单调减少区间为
$$
0<x\le\frac{1}{4}.
$$

### 第 2 题

- 答案：$\dfrac{1}{\sqrt5}\{0,\sqrt2,\sqrt3\}$

曲线
$$
3x^2+2y^2=12,\qquad z=0
$$
绕 $y$ 轴旋转后，旋转面方程为
$$
3(x^2+z^2)+2y^2=12.
$$

令
$$
F(x,y,z)=3(x^2+z^2)+2y^2-12.
$$
则法向量可取
$$
\nabla F=(6x,4y,6z).
$$

在点 $(0,\sqrt3,\sqrt2)$ 处，
$$
\nabla F=(0,4\sqrt3,6\sqrt2).
$$

它指向外侧，单位化得
$$
\frac{(0,4\sqrt3,6\sqrt2)}
\sqrt{(4\sqrt3)^2+(6\sqrt2)^2}}
=\frac{1}{\sqrt5}\{0,\sqrt2,\sqrt3\}.
$$

### 第 3 题

- 答案：$\dfrac{2\pi}{3}$

傅里叶系数
$$
b_n=\frac{1}{\pi}\int_{-\pi}^{\pi}f(x)\sin nx\,dx.
$$

因此
$$
b_3=\frac{1}{\pi}\int_{-\pi}^{\pi}(\pi x+x^2)\sin3x\,dx.
$$

其中 $x^2\sin3x$ 为奇函数，在对称区间上积分为 $0$。所以
$$
b_3=\int_{-\pi}^{\pi}x\sin3x\,dx
=2\int_0^\pi x\sin3x\,dx.
$$

分部积分：
$$
\int_0^\pi x\sin3x\,dx
=\left[-\frac{x\cos3x}{3}\right]_0^\pi
+\frac{1}{3}\int_0^\pi\cos3x\,dx
=\frac{\pi}{3}.
$$

故
$$
b_3=\frac{2\pi}{3}.
$$

### 第 4 题

- 答案：$\dfrac{1}{x^2+y^2+z^2}$

设
$$
r^2=x^2+y^2+z^2.
$$
题中
$$
u=\ln\sqrt{x^2+y^2+z^2}=\ln r.
$$

先求一阶偏导：
$$
u_x=\frac{x}{r^2},\qquad
u_y=\frac{y}{r^2},\qquad
u_z=\frac{z}{r^2}.
$$

再求二阶偏导：
$$
u_{xx}=\frac{r^2-2x^2}{r^4},\quad
u_{yy}=\frac{r^2-2y^2}{r^4},\quad
u_{zz}=\frac{r^2-2z^2}{r^4}.
$$

于是
$$
\operatorname{div}(\operatorname{grad}u)
=u_{xx}+u_{yy}+u_{zz}
=\frac{3r^2-2r^2}{r^4}
=\frac{1}{r^2}.
$$

即
$$
\operatorname{div}(\operatorname{grad}u)
=\frac{1}{x^2+y^2+z^2}.
$$

### 第 5 题

- 答案：$k(1,1,\ldots,1)^T$，其中 $k$ 为任意常数

因为 $A$ 的各行元素之和均为零，所以
$$
A(1,1,\ldots,1)^T=0.
$$

又因为
$$
r(A)=n-1,
$$
齐次方程组 $Ax=0$ 的解空间维数为
$$
n-r(A)=1.
$$

因此 $(1,1,\ldots,1)^T$ 可作为基础解系，通解为
$$
x=k(1,1,\ldots,1)^T,
$$
其中 $k$ 为任意常数。

### 第 6 题

- 答案：B

当 $x\to0$ 时，
$$
\sin(t^2)\sim t^2.
$$
因此
$$
f(x)=\int_0^{\sin x}\sin(t^2)\,dt
\sim \int_0^{\sin x}t^2\,dt
=\frac{(\sin x)^3}{3}
\sim \frac{x^3}{3}.
$$

又
$$
g(x)=x^3+x^4\sim x^3.
$$

故
$$
\lim_{x\to0}\frac{f(x)}{g(x)}=\frac{1}{3}.
$$

比值极限为非零常数但不等于 $1$，所以 $f(x)$ 是 $g(x)$ 的同阶但非等价无穷小，选 B。

### 第 7 题

- 答案：A

双纽线
$$
(x^2+y^2)^2=x^2-y^2
$$
化为极坐标方程：
$$
r^4=r^2\cos2\theta,
$$
即
$$
r^2=\cos2\theta.
$$

第一象限一瓣对应
$$
0\le\theta\le\frac{\pi}{4}.
$$
该部分面积为
$$
S_1=\frac{1}{2}\int_0^{\pi/4}r^2\,d\theta
=\frac{1}{2}\int_0^{\pi/4}\cos2\theta\,d\theta.
$$

由对称性，总面积为
$$
S=4S_1
=2\int_0^{\pi/4}\cos2\theta\,d\theta.
$$

故选 A。

### 第 8 题

- 答案：C

直线 $L_1$ 的方向向量为
$$
l_1=(1,-2,1).
$$

直线 $L_2$ 是两个平面的交线。两个平面的法向量分别为
$$
n_1=(1,-1,0),\qquad n_2=(0,2,1).
$$
故 $L_2$ 的方向向量可取
$$
l_2=n_1\times n_2=(-1,-1,2).
$$

两直线夹角 $\varphi$ 满足
$$
\cos\varphi
=\frac{|l_1\cdot l_2|}{|l_1||l_2|}
=\frac{|-1+2+2|}{\sqrt6\sqrt6}
=\frac{1}{2}.
$$

所以
$$
\varphi=\frac{\pi}{3}.
$$

故选 C。

### 第 9 题

- 答案：B

记
$$
P=[f(x)-e^x]\sin y,\qquad Q=-f(x)\cos y.
$$

曲线积分与路径无关的条件为
$$
\frac{\partial P}{\partial y}=\frac{\partial Q}{\partial x}.
$$

于是
$$
[f(x)-e^x]\cos y=-f'(x)\cos y.
$$

化简得
$$
f'(x)+f(x)=e^x.
$$

两边同乘积分因子 $e^x$：
$$
\bigl(e^x f(x)\bigr)'=e^{2x}.
$$

积分得
$$
e^x f(x)=\frac{1}{2}e^{2x}+C.
$$

由 $f(0)=0$ 得
$$
C=-\frac{1}{2}.
$$

所以
$$
f(x)=\frac{1}{2}(e^x-e^{-x}).
$$

故选 B。

### 第 10 题

- 答案：C

矩阵
$$
Q=
\begin{pmatrix}
1&2&3\\
2&4&t\\
3&6&9
\end{pmatrix}
$$
的第三行恒为第一行的 $3$ 倍。

当 $t=6$ 时，第二行也是第一行的 $2$ 倍，所以
$$
r(Q)=1.
$$
由 $PQ=O$ 只能推出
$$
r(P)+r(Q)\le3,
$$
即 $r(P)\le2$。又 $P\ne O$，故 $r(P)$ 可能为 $1$，也可能为 $2$，A、B 都不必成立。

当 $t\ne6$ 时，第一行与第二行不成比例，所以
$$
r(Q)=2.
$$
于是
$$
r(P)+r(Q)\le3
$$
推出
$$
r(P)\le1.
$$
又 $P$ 非零，故
$$
r(P)=1.
$$

因此选 C。

### 第 11 题

- 答案：$e^2$

令
$$
t=\frac{1}{x}.
$$
当 $x\to\infty$ 时，$t\to0^+$，原极限为
$$
\lim_{t\to0^+}(\sin2t+\cos t)^{1/t}.
$$

这是 $1^\infty$ 型。取对数：
$$
\ln L=\lim_{t\to0^+}\frac{\ln(\sin2t+\cos t)}{t}.
$$

因为 $\sin2t+\cos t\to1$，且
$$
\ln(\sin2t+\cos t)
\sim \sin2t+\cos t-1.
$$

所以
$$
\ln L
=\lim_{t\to0^+}\frac{\sin2t+\cos t-1}{t}.
$$

用洛必达法则：
$$
\lim_{t\to0^+}\frac{\sin2t+\cos t-1}{t}
=\lim_{t\to0^+}(2\cos2t-\sin t)=2.
$$

故
$$
L=e^2.
$$

### 第 12 题

- 答案：$2x\sqrt{e^x-1}-4\sqrt{e^x-1}+4\arctan\sqrt{e^x-1}+C$

先作分部积分。因为
$$
d\sqrt{e^x-1}
=\frac{e^x}{2\sqrt{e^x-1}}\,dx,
$$
所以
$$
\frac{e^x}{\sqrt{e^x-1}}\,dx
=2\,d\sqrt{e^x-1}.
$$

于是
$$
\int\frac{xe^x}{\sqrt{e^x-1}}\,dx
=2x\sqrt{e^x-1}-2\int\sqrt{e^x-1}\,dx.
$$

令
$$
t=\sqrt{e^x-1},
$$
则
$$
e^x=t^2+1,\qquad dx=\frac{2t}{t^2+1}\,dt.
$$

所以
$$
\int\sqrt{e^x-1}\,dx
=\int t\frac{2t}{t^2+1}\,dt
=2\int\frac{t^2}{t^2+1}\,dt
=2t-2\arctan t+C.
$$

代回得
$$
\int\frac{xe^x}{\sqrt{e^x-1}}\,dx
=2x\sqrt{e^x-1}
-4\sqrt{e^x-1}
+4\arctan\sqrt{e^x-1}+C.
$$

### 第 13 题

- 答案：$y=\dfrac{2x}{1+x^2}$

原方程
$$
x^2y'+xy=y^2
$$
两边除以 $y^2$，得
$$
x^2y^{-2}y'+xy^{-1}=1.
$$

令
$$
z=y^{-1}.
$$
则
$$
z'=-y^{-2}y'.
$$

方程化为
$$
-x^2z'+xz=1,
$$
即
$$
z'-\frac{1}{x} z=-\frac{1}{x^2}.
$$

注意
$$
\left(\frac{z}{x}\right)'
=\frac{xz'-z}{x^2}.
$$
由方程得
$$
xz'-z=-\frac{1}{x},
$$
故
$$
\left(\frac{z}{x}\right)'=-\frac{1}{x^3}.
$$

积分：
$$
\frac{z}{x}=\frac{1}{2x^2}+C.
$$
于是
$$
\frac{1}{xy}=\frac{1}{2x^2}+C.
$$

整理得
$$
y=\frac{2x}{1+2Cx^2}.
$$

由 $y(1)=1$ 得 $C=\frac{1}{2}$，所以特解为
$$
y=\frac{2x}{1+x^2}.
$$

### 第 14 题

- 答案：$\dfrac{\pi}{2}$

记
$$
P=2xz,\qquad Q=yz,\qquad R=-z^2.
$$
则
$$
\frac{\partial P}{\partial x}
+\frac{\partial Q}{\partial y}
+\frac{\partial R}{\partial z}
=2z+z-2z=z.
$$

$\Sigma$ 是所围立体的闭合边界且取外侧，故由高斯公式
$$
I=\iint_{\Sigma}P\,dy\,dz+Q\,dz\,dx+R\,dx\,dy
=\iiint_{\Omega}z\,dV.
$$

两曲面为
$$
z=\sqrt{x^2+y^2}
$$
与
$$
z=\sqrt{2-x^2-y^2}.
$$
在球坐标中分别对应
$$
\varphi=\frac{\pi}{4},\qquad \rho=\sqrt2.
$$

因此区域为
$$
0\le\theta\le2\pi,\quad
0\le\varphi\le\frac{\pi}{4},\quad
0\le\rho\le\sqrt2.
$$

又 $z=\rho\cos\varphi$，$dV=\rho^2\sin\varphi\,d\rho\,d\varphi\,d\theta$，故
$$
\begin{aligned}
I
&=\int_0^{2\pi}d\theta
\int_0^{\pi/4}\sin\varphi\cos\varphi\,d\varphi
\int_0^{\sqrt2}\rho^3\,d\rho\\
&=2\pi\cdot\frac{1}{4}\cdot1
=\frac{\pi}{2}.
\end{aligned}
$$

### 第 15 题

- 答案：$\dfrac{22}{27}$

将级数拆成两部分：
$$
\sum_{n=0}^{\infty}\frac{(-1)^n(n^2-n+1)}{2^n}
=
\sum_{n=0}^{\infty}n(n-1)\left(-\frac{1}{2}\right)^n
+
\sum_{n=0}^{\infty}\left(-\frac{1}{2}\right)^n.
$$

第二项为等比级数：
$$
\sum_{n=0}^{\infty}\left(-\frac{1}{2}\right)^n
=\frac{1}{1+\frac{1}{2}}
=\frac{2}{3}.
$$

又由
$$
\sum_{n=0}^{\infty}x^n=\frac{1}{1-x}
$$
两次求导得
$$
\sum_{n=0}^{\infty}n(n-1)x^n=\frac{2x^2}{(1-x)^3}.
$$

令 $x=-\frac{1}{2}$，有
$$
\sum_{n=0}^{\infty}n(n-1)\left(-\frac{1}{2}\right)^n
=\frac{2\cdot\frac{1}{4}}{(1+\frac{1}{2})^3}
=\frac{4}{27}.
$$

因此原级数和为
$$
\frac{4}{27}+\frac{2}{3}
=\frac{22}{27}.
$$

### 第 16 题

- 答案：在 $(0,+\infty)$ 内有且仅有一个零点。

由条件 $f'(x)\ge k>0$，对任意 $x>0$ 有
$$
f(x)=f(0)+\int_0^x f'(t)\,dt
\ge f(0)+kx.
$$

当 $x\to+\infty$ 时，右端趋于 $+\infty$，因此存在充分大的 $x_0>0$ 使
$$
f(x_0)>0.
$$

又 $f(0)<0$，且 $f$ 连续，所以由介值定理，$f$ 在 $(0,x_0)$ 内至少有一个零点。

另一方面，因为
$$
f'(x)\ge k>0,
$$
所以 $f(x)$ 在 $[0,+\infty)$ 上严格单调增加。严格单调函数至多有一个零点。

综上，$f(x)$ 在 $(0,+\infty)$ 内有且仅有一个零点。

### 第 17 题

- 答案：$a^b>b^a$。

因为 $a,b>0$，要证
$$
a^b>b^a,
$$
等价于证明
$$
b\ln a>a\ln b,
$$
即
$$
\frac{\ln a}{a}>\frac{\ln b}{b}.
$$

设
$$
g(x)=\frac{\ln x}{x}\qquad (x>e).
$$
则
$$
g'(x)=\frac{1-\ln x}{x^2}<0\qquad (x>e).
$$

所以 $g(x)$ 在 $(e,+\infty)$ 上严格单调减少。由 $b>a>e$ 得
$$
g(a)>g(b),
$$
即
$$
\frac{\ln a}{a}>\frac{\ln b}{b}.
$$

故
$$
a^b>b^a.
$$

### 第 18 题

- 答案：$a=2$，可取 $x=Py$，其中 $P=\begin{pmatrix}0&1&0\\\dfrac{1}{\sqrt2}&0&\dfrac{1}{\sqrt2}\\-\dfrac{1}{\sqrt2}&0&\dfrac{1}{\sqrt2}\end{pmatrix}$

二次型矩阵为
$$
A=
\begin{pmatrix}
2&0&0\\
0&3&a\\
0&a&3
\end{pmatrix}.
$$

特征方程为
$$
|\lambda E-A|
=(\lambda-2)\bigl((\lambda-3)^2-a^2\bigr)=0.
$$

正交变换后的标准形为
$$
y_1^2+2y_2^2+5y_3^2,
$$
所以矩阵 $A$ 的特征值为 $1,2,5$。由于 $a>0$，由 $3-a=1$ 得
$$
a=2.
$$

此时
$$
A=
\begin{pmatrix}
2&0&0\\
0&3&2\\
0&2&3
\end{pmatrix}.
$$

对应特征值 $\lambda_1=1,\lambda_2=2,\lambda_3=5$ 的特征向量可分别取
$$
X_1=(0,1,-1)^T,\quad
X_2=(1,0,0)^T,\quad
X_3=(0,1,1)^T.
$$

单位化得
$$
\gamma_1=\frac{1}{\sqrt2}(0,1,-1)^T,\quad
\gamma_2=(1,0,0)^T,\quad
\gamma_3=\frac{1}{\sqrt2}(0,1,1)^T.
$$

取
$$
P=(\gamma_1,\gamma_2,\gamma_3)
=
\begin{pmatrix}
0&1&0\\
\dfrac{1}{\sqrt2}&0&\dfrac{1}{\sqrt2}\\
-\dfrac{1}{\sqrt2}&0&\dfrac{1}{\sqrt2}
\end{pmatrix}.
$$

则
$$
P^TAP=\operatorname{diag}(1,2,5),
$$
即令 $x=Py$ 可将二次型化为所给标准形。

### 第 19 题

- 答案：$B$ 的列向量组线性无关。

设 $B$ 的列向量为
$$
\beta_1,\beta_2,\ldots,\beta_n,
$$
即
$$
B=(\beta_1,\beta_2,\ldots,\beta_n).
$$

若有
$$
k_1\beta_1+k_2\beta_2+\cdots+k_n\beta_n=0,
$$
记
$$
k=(k_1,k_2,\ldots,k_n)^T,
$$
则
$$
Bk=0.
$$

两边左乘 $A$，得
$$
ABk=0.
$$

由 $AB=E$，有
$$
Ek=0,
$$
即
$$
k=0.
$$

所以只有零线性组合能得到零向量，故 $B$ 的列向量组线性无关。

### 第 20 题

- 答案：$2xy''+\sqrt{1+(y')^2}=0$，初始条件 $y(-1)=0,\ y'(-1)=1$

设某时刻物体 $A$ 位于
$$
(0,Y),
$$
物体 $B$ 位于
$$
(x,y).
$$

由于 $B$ 的速度方向始终指向 $A$，轨迹切线方向就是从 $B$ 指向 $A$ 的方向，因此
$$
y'=\frac{y-Y}{x-0}.
$$
即
$$
Y=y-xy'. \tag{1}
$$

又 $A$ 的速度大小为 $v$，沿 $y$ 轴正向运动，所以
$$
\frac{dY}{dt}=v.
$$
物体 $B$ 的速度大小为 $2v$，故
$$
\sqrt{\left(\frac{dx}{dt}\right)^2+\left(\frac{dy}{dt}\right)^2}
=2\frac{dY}{dt}.
$$

因 $B$ 从 $x=-1$ 向 $y$ 轴方向运动，可取 $\frac{dx}{dt}>0$，于是
$$
\sqrt{1+(y')^2}=2\frac{dY}{dx}. \tag{2}
$$

由 (1) 对 $x$ 求导：
$$
\frac{dY}{dx}=y'-(y'+xy'')=-xy''.
$$

代入 (2)，得
$$
\sqrt{1+(y')^2}=-2xy''.
$$

因此轨迹满足微分方程
$$
2xy''+\sqrt{1+(y')^2}=0.
$$

初始时 $B$ 位于 $(-1,0)$，所以
$$
y(-1)=0.
$$
此时 $A$ 位于 $(0,1)$，从 $B$ 指向 $A$ 的方向向量为 $(1,1)$，故初始切线斜率为
$$
y'(-1)=1.
$$

### 第 21 题

- 答案：$\dfrac{1}{6}$

设第二次抽出次品为事件 $B_2$，第一次抽出次品为 $B_1$。由全概率公式，
$$
P(B_2)=P(B_1)P(B_2\mid B_1)+P(\overline{B_1})P(B_2\mid \overline{B_1}).
$$

题中共有 $12$ 个产品，其中 $2$ 个次品，所以
$$
P(B_1)=\frac{2}{12},\qquad P(\overline{B_1})=\frac{10}{12}.
$$

若第一次抽出次品，则剩余 $11$ 个中有 $1$ 个次品：
$$
P(B_2\mid B_1)=\frac{1}{11}.
$$

若第一次抽出正品，则剩余 $11$ 个中有 $2$ 个次品：
$$
P(B_2\mid \overline{B_1})=\frac{2}{11}.
$$

因此
$$
P(B_2)=\frac{2}{12}\cdot\frac{1}{11}
+\frac{10}{12}\cdot\frac{2}{11}
=\frac{1}{6}.
$$

### 第 22 题

- 答案：$f_Y(y)=\begin{cases}\dfrac{1}{4\sqrt y},&0<y<4,\\0,&\text{其他},\end{cases}$

因为 $X$ 在 $(0,2)$ 上均匀分布，所以
$$
f_X(x)=
\begin{cases}
\dfrac{1}{2},&0<x<2,\\
0,&\text{其他}.
\end{cases}
$$

令
$$
Y=X^2.
$$
当 $0<y<4$ 时，
$$
F_Y(y)=P(Y\le y)=P(X^2\le y)=P(0<X\le\sqrt y).
$$

所以
$$
F_Y(y)=\int_0^{\sqrt y}\frac{1}{2}\,dx
=\frac{\sqrt y}{2}.
$$

对 $y$ 求导得
$$
f_Y(y)=F_Y'(y)=\frac{1}{4\sqrt y},\qquad 0<y<4.
$$

因此
$$
f_Y(y)=
\begin{cases}
\dfrac{1}{4\sqrt y},&0<y<4,\\
0,&\text{其他}.
\end{cases}
$$

### 第 23 题

- 答案：$E(X)=0,\ D(X)=2$；$\operatorname{Cov}(X,\lvert X\rvert)=0$，故 $X$ 与 $\lvert X\rvert$ 不相关；但二者不相互独立

密度
$$
f(x)=\frac{1}{2}e^{-|x|}
$$
是偶函数。

1. 由于 $xf(x)$ 是奇函数，故
$$
E(X)=\int_{-\infty}^{+\infty}xf(x)\,dx=0.
$$

又
$$
D(X)=E(X^2)-[E(X)]^2=E(X^2).
$$
因此
$$
\begin{aligned}
D(X)
&=\int_{-\infty}^{+\infty}x^2\frac{1}{2}e^{-|x|}\,dx\\
&=\int_0^{+\infty}x^2e^{-x}\,dx
=2.
\end{aligned}
$$

2. 协方差为
$$
\operatorname{Cov}(X,|X|)
=E(X|X|)-E(X)E(|X|).
$$

其中 $E(X)=0$，且 $x|x|f(x)$ 是奇函数，所以
$$
E(X|X|)=\int_{-\infty}^{+\infty}x|x|f(x)\,dx=0.
$$

故
$$
\operatorname{Cov}(X,|X|)=0.
$$
因此 $X$ 与 $|X|$ 不相关。

3. $X$ 与 $|X|$ 不相互独立。取事件
$$
A=\{X\le1\},\qquad B=\{|X|\le1\}.
$$
则
$$
P(A)=1-\frac{1}{2e},
$$
而
$$
P(B)=P(-1\le X\le1)=1-\frac{1}{e}.
$$

又 $B\subset A$，所以
$$
P(A\cap B)=P(B)=1-\frac{1}{e}.
$$

但
$$
P(A)P(B)=\left(1-\frac{1}{2e}\right)\left(1-\frac{1}{e}\right)
\ne 1-\frac{1}{e}.
$$

因此 $A$ 与 $B$ 不独立，从而 $X$ 与 $|X|$ 不相互独立。
