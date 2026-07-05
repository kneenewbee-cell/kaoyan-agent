# Math 1 1991 Answers

资料类型：考研数学一答案解析
年份：1991
科目：数学一
范围：试卷 I
来源：D:\百度网盘\高数资料\【02】1987-2022年数学一真题详解答案（PDF）\1991考研数一真题解析.pdf
校对状态：已按题干和答案页图像重新清洗，去除 OCR 碎行、串题内容和非本题知识点页脚

## 答案速查

| 题号 | 题型 | 答案 |
|---|---|---|
| 1 | 填空题 | $\dfrac{\sin t-t\cos t}{4t^3}$ |
| 2 | 填空题 | $dz=dx-\sqrt2\,dy$ |
| 3 | 填空题 | $x-3y+z+2=0$ |
| 4 | 填空题 | $-\dfrac{3}{2}$ |
| 5 | 填空题 | $\begin{pmatrix}1&-2&0&0\\-2&5&0&0\\0&0&\dfrac{1}{3}&\dfrac{2}{3}\\0&0&-\dfrac{1}{3}&\dfrac{1}{3}\end{pmatrix}$ |
| 6 | 选择题 | D |
| 7 | 选择题 | B |
| 8 | 选择题 | C |
| 9 | 选择题 | A |
| 10 | 选择题 | D |
| 11 | 解答题 | $e^{-\pi/2}$ |
| 12 | 解答题 | $\dfrac{11}{7}$ |
| 13 | 解答题 | $\dfrac{256\pi}{3}$ |
| 14 | 解答题 | $y=\sin x,\ 0\le x\le \pi$ |
| 15 | 解答题 | $2+\lvert x\rvert=\dfrac{5}{2}-\dfrac{4}{\pi^2}\sum_{n=1}^{\infty}\dfrac{\cos(2n-1)\pi x}{(2n-1)^2}$；$\displaystyle\sum_{n=1}^{\infty}\dfrac{1}{n^2}=\dfrac{\pi^2}{6}$ |
| 16 | 解答题 | 存在 $c\in(0,1)$，使 $f'(c)=0$。 |
| 17 | 解答题 | 不能表示：$a=-1,\ b\ne0$；唯一表示：$a\ne-1$，且 $\beta=-\dfrac{2b}{a+1}\alpha_1+\dfrac{a+b+1}{a+1}\alpha_2+\dfrac{b}{a+1}\alpha_3$ |
| 18 | 解答题 | 证明见解析。 |
| 19 | 解答题 | $y=\dfrac{1}{2}\left(e^{x-1}+e^{1-x}\right)$ |
| 20 | 填空题 | $0.2$ |
| 21 | 填空题 | $\dfrac{1}{2}+\dfrac{1}{\pi}$ |
| 22 | 解答题 | $F_Z(z)=\begin{cases}0,&z<0,\\1-(1+z)e^{-z},&z\ge0,\end{cases}$ |

## 详细解析

### 第 1 题

- 答案：$\dfrac{\sin t-t\cos t}{4t^3}$

由参数方程

$$
x=1+t^2,\qquad y=\cos t
$$

得

$$
\frac{dy}{dx}
=\frac{dy/dt}{dx/dt}
=\frac{-\sin t}{2t}.
$$

再对 $x$ 求导，即

$$
\frac{d^2y}{dx^2}
=\frac{d}{dt}\left(-\frac{\sin t}{2t}\right)\cdot \frac{dt}{dx}.
$$

因为 $\dfrac{dt}{dx}=\dfrac{1}{2t}$，所以

$$
\frac{d^2y}{dx^2}
=\frac{-2t\cos t+2\sin t}{4t^2}\cdot \frac{1}{2t}
=\frac{\sin t-t\cos t}{4t^3}.
$$

### 第 2 题

- 答案：$dz=dx-\sqrt2\,dy$

对方程

$$
xyz+\sqrt{x^2+y^2+z^2}=\sqrt2
$$

两边求全微分，得

$$
d(xyz)+\frac{x\,dx+y\,dy+z\,dz}{\sqrt{x^2+y^2+z^2}}=0.
$$

即

$$
(yz\,dx+xz\,dy+xy\,dz)
+\frac{x\,dx+y\,dy+z\,dz}{\sqrt{x^2+y^2+z^2}}=0.
$$

在点 $(1,0,-1)$ 处，$\sqrt{x^2+y^2+z^2}=\sqrt2$，代入得

$$
-dy+\frac{dx-dz}{\sqrt2}=0.
$$

所以

$$
dz=dx-\sqrt2\,dy.
$$

### 第 3 题

- 答案：$x-3y+z+2=0$

直线 $L_1$ 的方向向量为

$$
\boldsymbol{v}_1=(1,0,-1),
$$

且 $L_1$ 过点 $(1,2,3)$。直线 $L_2$ 的方向向量为

$$
\boldsymbol{v}_2=(2,1,1).
$$

所求平面过 $L_1$ 且平行于 $L_2$，因此平面内含有方向向量 $\boldsymbol{v}_1,\boldsymbol{v}_2$。平面方程可写为

$$
\begin{vmatrix}
x-1&y-2&z-3\\
1&0&-1\\
2&1&1
\end{vmatrix}=0.
$$

展开并整理得

$$
x-3y+z+2=0.
$$

### 第 4 题

- 答案：$-\dfrac{3}{2}$

当 $x\to0$ 时，

$$
(1+ax^2)^{1/3}-1\sim \frac{1}{3} ax^2,
$$

而

$$
\cos x-1\sim -\frac{1}{2}x^2.
$$

两者为等价无穷小，所以

$$
\frac{1}{3}a=-\frac{1}{2}.
$$

故

$$
a=-\frac{3}{2}.
$$

### 第 5 题

- 答案：$\begin{pmatrix}1&-2&0&0\\-2&5&0&0\\0&0&\dfrac{1}{3}&\dfrac{2}{3}\\0&0&-\dfrac{1}{3}&\dfrac{1}{3}\end{pmatrix}$

矩阵 $A$ 是分块对角矩阵：

$$
A=
\begin{pmatrix}
B_1&0\\
0&B_2
\end{pmatrix},
\quad
B_1=
\begin{pmatrix}
5&2\\
2&1
\end{pmatrix},
\quad
B_2=
\begin{pmatrix}
1&-2\\
1&1
\end{pmatrix}.
$$

分别求逆：

$$
B_1^{-1}=
\begin{pmatrix}
1&-2\\
-2&5
\end{pmatrix},
\qquad
B_2^{-1}
=\frac{1}{3}
\begin{pmatrix}
1&2\\
-1&1
\end{pmatrix}.
$$

因此

$$
A^{-1}=
\begin{pmatrix}
1&-2&0&0\\
-2&5&0&0\\
0&0&\dfrac{1}{3}&\dfrac{2}{3}\\
0&0&-\dfrac{1}{3}&\dfrac{1}{3}
\end{pmatrix}.
$$

### 第 6 题

- 答案：D

函数在 $x=0$ 处分母为 $0$，且

$$
\lim_{x\to0}\frac{1+e^{-x^2}}{1-e^{-x^2}}=+\infty,
$$

所以 $x=0$ 是铅直渐近线。

当 $x\to\pm\infty$ 时，$e^{-x^2}\to0$，于是

$$
\lim_{x\to\pm\infty}\frac{1+e^{-x^2}}{1-e^{-x^2}}=1.
$$

所以 $y=1$ 是水平渐近线。故选 D。

### 第 7 题

- 答案：B

令 $u=t/2$，则 $t=2u,\ dt=2du$。题设化为

$$
f(x)=2\int_0^x f(u)\,du+\ln2.
$$

两边对 $x$ 求导：

$$
f'(x)=2f(x).
$$

故

$$
f(x)=Ce^{2x}.
$$

令 $x=0$，由原式得

$$
f(0)=\ln2.
$$

所以 $C=\ln2$，即

$$
f(x)=e^{2x}\ln2.
$$

故选 B。

### 第 8 题

- 答案：C

由

$$
\sum_{n=1}^{\infty}(-1)^{n-1}a_n
=\sum_{n=1}^{\infty}a_{2n-1}
-\sum_{n=1}^{\infty}a_{2n}=2
$$

和

$$
\sum_{n=1}^{\infty}a_{2n-1}=5
$$

可得

$$
\sum_{n=1}^{\infty}a_{2n}=5-2=3.
$$

因此

$$
\sum_{n=1}^{\infty}a_n
=\sum_{n=1}^{\infty}a_{2n-1}
+\sum_{n=1}^{\infty}a_{2n}
=5+3=8.
$$

故选 C。

### 第 9 题

- 答案：A

区域 $D$ 可分成关于坐标轴对称配对的若干部分。函数 $xy$ 关于 $x$、$y$ 都是奇函数，因此在这些对称区域上的积分相互抵消：

$$
\iint_D xy\,dx\,dy=0.
$$

函数 $\cos x\sin y$ 关于 $x$ 是偶函数，关于 $y$ 是奇函数。结合题中三角形区域的对称分割，负半平面部分抵消后，只留下第一象限部分的两倍：

$$
\iint_D \cos x\sin y\,dx\,dy
=2\iint_{D_1}\cos x\sin y\,dx\,dy.
$$

所以

$$
\iint_D (xy+\cos x\sin y)\,dx\,dy
=2\iint_{D_1}\cos x\sin y\,dx\,dy.
$$

故选 A。

### 第 10 题

- 答案：D

由

$$
ABC=E
$$

可知 $A,B,C$ 均可逆。左乘 $A^{-1}$ 得

$$
BC=A^{-1}.
$$

两边右乘 $A$，得

$$
BCA=E.
$$

故选 D。

### 第 11 题

- 答案：$e^{-\pi/2}$

设

$$
L=\lim_{x\to0^+}(\cos\sqrt{x})^{\pi/x}.
$$

取对数：

$$
\ln L=\lim_{x\to0^+}\frac{\pi}{x}\ln(\cos\sqrt{x}).
$$

当 $x\to0^+$ 时，

$$
\cos\sqrt{x}-1\sim -\frac{x}{2},
\qquad
\ln(\cos\sqrt{x})\sim \cos\sqrt{x}-1\sim -\frac{x}{2}.
$$

所以

$$
\ln L=\lim_{x\to0^+}\frac{\pi}{x}\left(-\frac{x}{2}\right)
=-\frac{\pi}{2}.
$$

因此

$$
L=e^{-\pi/2}.
$$

### 第 12 题

- 答案：$\dfrac{11}{7}$

曲面

$$
2x^2+3y^2+z^2=6
$$

在 $P(1,1,1)$ 处的外法向量与梯度

$$
(4x,6y,2z)\big|_{(1,1,1)}=(4,6,2)
$$

同向，所以单位外法向量为

$$
\boldsymbol{e}_n=\frac{1}{\sqrt{14}}(2,3,1).
$$

对

$$
u=\frac{\sqrt{6x^2+8y^2}}{z}
$$

求梯度，在 $P$ 处有

$$
u_x=\frac{6}{\sqrt{14}},\qquad
u_y=\frac{8}{\sqrt{14}},\qquad
u_z=-\sqrt{14}.
$$

方向导数为

$$
D_{\boldsymbol{e}_n}u
=\nabla u(P)\cdot \boldsymbol{e}_n
=\frac{6}{\sqrt{14}}\frac{2}{\sqrt{14}}
+\frac{8}{\sqrt{14}}\frac{3}{\sqrt{14}}
-\sqrt{14}\frac{1}{\sqrt{14}}
=\frac{11}{7}.
$$

### 第 13 题

- 答案：$\dfrac{256\pi}{3}$

曲线

$$
y^2=2z,\quad x=0
$$

绕 $z$ 轴旋转所得曲面为

$$
x^2+y^2=2z.
$$

用柱坐标，区域为

$$
0\le \theta\le 2\pi,\quad 0\le z\le 4,\quad 0\le r\le \sqrt{2z}.
$$

积分变为

$$
\iiint_\Omega (x^2+y^2+z)\,dV
=\int_0^4\int_0^{2\pi}\int_0^{\sqrt{2z}}
(r^2+z)r\,dr\,d\theta\,dz.
$$

先对 $r$ 积分：

$$
\int_0^{\sqrt{2z}}(r^2+z)r\,dr
=\left(\frac{r^4}{4}+\frac{zr^2}{2}\right)_0^{\sqrt{2z}}
=2z^2.
$$

故

$$
\iiint_\Omega (x^2+y^2+z)\,dV
=2\pi\int_0^4 2z^2\,dz
=\frac{256\pi}{3}.
$$

### 第 14 题

- 答案：$y=\sin x,\ 0\le x\le \pi$

曲线族为

$$
y=a\sin x,\qquad a>0,\quad 0\le x\le\pi.
$$

于是

$$
dy=a\cos x\,dx.
$$

沿该曲线的积分为

$$
\begin{aligned}
I(a)
&=\int_0^\pi\left[1+(a\sin x)^3+(2x+a\sin x)a\cos x\right]\,dx\\
&=\pi+\frac{4}{3}a^3-4a.
\end{aligned}
$$

求导：

$$
I'(a)=4a^2-4.
$$

因 $a>0$，临界点为 $a=1$。并且 $I'(a)<0$ 当 $0<a<1$，$I'(a)>0$ 当 $a>1$，所以 $a=1$ 处取最小值。

故所求曲线为

$$
y=\sin x,\qquad 0\le x\le\pi.
$$

### 第 15 题

- 答案：$2+\lvert x\rvert=\dfrac{5}{2}-\dfrac{4}{\pi^2}\sum_{n=1}^{\infty}\dfrac{\cos(2n-1)\pi x}{(2n-1)^2}$；$\displaystyle\sum_{n=1}^{\infty}\dfrac{1}{n^2}=\dfrac{\pi^2}{6}$

函数 $f(x)=2+|x|$ 为偶函数，周期为 $2$，故只含余弦项。

在 $[-1,1]$ 上，

$$
a_0=2\int_0^1(2+x)\,dx=5,
$$

且

$$
a_n=2\int_0^1(2+x)\cos n\pi x\,dx
=\frac{2(\cos n\pi-1)}{n^2\pi^2},\qquad b_n=0.
$$

当 $n$ 为偶数时 $a_n=0$；当 $n=2k-1$ 为奇数时，

$$
a_{2k-1}=-\frac{4}{(2k-1)^2\pi^2}.
$$

所以

$$
2+|x|
=\frac{5}{2}-\frac{4}{\pi^2}\sum_{k=1}^{\infty}
\frac{\cos(2k-1)\pi x}{(2k-1)^2}.
$$

令 $x=0$，得

$$
2=\frac{5}{2}-\frac{4}{\pi^2}\sum_{k=1}^{\infty}\frac{1}{(2k-1)^2},
$$

故

$$
\sum_{k=1}^{\infty}\frac{1}{(2k-1)^2}=\frac{\pi^2}{8}.
$$

又

$$
\sum_{n=1}^{\infty}\frac{1}{n^2}
=\sum_{k=1}^{\infty}\frac{1}{(2k-1)^2}
+\sum_{k=1}^{\infty}\frac{1}{(2k)^2}
=\frac{\pi^2}{8}+\frac{1}{4}\sum_{n=1}^{\infty}\frac{1}{n^2}.
$$

因此

$$
\sum_{n=1}^{\infty}\frac{1}{n^2}=\frac{\pi^2}{6}.
$$

### 第 16 题

- 答案：存在 $c\in(0,1)$，使 $f'(c)=0$。

由积分中值定理，存在 $\xi\in\left(\dfrac{2}{3},1\right)$，使

$$
\int_{2/3}^{1}f(x)\,dx
=f(\xi)\left(1-\frac{2}{3}\right)
=\frac{1}{3} f(\xi).
$$

题设给出

$$
3\int_{2/3}^{1}f(x)\,dx=f(0),
$$

因此

$$
f(\xi)=f(0).
$$

函数 $f$ 在 $[0,\xi]$ 上连续，在 $(0,\xi)$ 内可导，由罗尔定理，存在

$$
c\in(0,\xi)\subset(0,1),
$$

使

$$
f'(c)=0.
$$

### 第 17 题

- 答案：不能表示：$a=-1,\ b\ne0$；唯一表示：$a\ne-1$，且 $\beta=-\dfrac{2b}{a+1}\alpha_1+\dfrac{a+b+1}{a+1}\alpha_2+\dfrac{b}{a+1}\alpha_3$

设

$$
x_1\alpha_1+x_2\alpha_2+x_3\alpha_3+x_4\alpha_4=\beta.
$$

写成增广矩阵并作初等行变换，可化为

$$
\left[
\begin{array}{cccc|c}
1&1&1&1&1\\
0&1&-1&2&1\\
0&0&a+1&0&b\\
0&0&0&a+1&0
\end{array}
\right].
$$

当 $a=-1$ 时，第三行变为

$$
0=b.
$$

所以若 $a=-1,\ b\ne0$，方程组无解，即 $\beta$ 不能表示成 $\alpha_1,\alpha_2,\alpha_3,\alpha_4$ 的线性组合。

当 $a\ne-1$ 时，系数矩阵满秩，方程组有唯一解。由阶梯形方程组得

$$
x_3=\frac{b}{a+1},\qquad x_4=0,
$$

$$
x_2=1+x_3=\frac{a+b+1}{a+1},
$$

$$
x_1=1-x_2-x_3=-\frac{2b}{a+1}.
$$

因此当 $a\ne-1$ 时，

$$
\beta=-\frac{2b}{a+1}\alpha_1
+\frac{a+b+1}{a+1}\alpha_2
+\frac{b}{a+1}\alpha_3.
$$

### 第 18 题

- 答案：证明见解析。

因为 $A$ 是 $n$ 阶正定阵，所以 $A$ 的特征值

$$
\lambda_1,\lambda_2,\cdots,\lambda_n
$$

全为正数。

若 $\lambda_i$ 是 $A$ 的特征值，则 $\lambda_i+1$ 是 $A+E$ 的特征值。于是

$$
|A+E|=\prod_{i=1}^n(\lambda_i+1).
$$

由于每个 $\lambda_i>0$，所以每个 $\lambda_i+1>1$。因此

$$
|A+E|=\prod_{i=1}^n(\lambda_i+1)>1.
$$

### 第 19 题

- 答案：$y=\dfrac{1}{2}\left(e^{x-1}+e^{1-x}\right)$

设曲线为 $y=y(x)$。其曲率为

$$
K=\frac{y''}{(1+y'^2)^{3/2}},
$$

因为曲线向上凹，取 $y''>0$。

曲线在 $P(x,y)$ 处的法线与 $x$ 轴交于 $Q$，可得法线段长度

$$
|PQ|=y\sqrt{1+y'^2}.
$$

题设给出

$$
\frac{y''}{(1+y'^2)^{3/2}}
=\frac{1}{y\sqrt{1+y'^2}},
$$

即

$$
yy''=1+y'^2.
$$

令 $p=y'$，把 $p$ 看作 $y$ 的函数，则 $y''=p\dfrac{dp}{dy}$，所以

$$
yp\frac{dp}{dy}=1+p^2.
$$

分离变量并积分：

$$
\frac{1}{2}\ln(1+p^2)=\ln y+C,
$$

即

$$
y=C\sqrt{1+p^2}.
$$

曲线在 $(1,1)$ 处切线与 $x$ 轴平行，故 $p(1)=0$，且 $y(1)=1$，得 $C=1$。于是

$$
y=\sqrt{1+y'^2},
$$

即

$$
y'=\pm\sqrt{y^2-1}.
$$

积分得

$$
\ln\left(y+\sqrt{y^2-1}\right)=\pm x+C.
$$

结合 $y(1)=1$，得到

$$
y=\frac{1}{2}\left(e^{x-1}+e^{1-x}\right).
$$

### 第 20 题

- 答案：$0.2$

设

$$
X\sim N(2,\sigma^2),
$$

则

$$
\frac{X-2}{\sigma}\sim N(0,1).
$$

由题设

$$
P\{2<X<4\}=0.3
$$

可得

$$
\Phi\left(\frac{2}{\sigma}\right)-\Phi(0)=0.3.
$$

因为 $\Phi(0)=0.5$，所以

$$
\Phi\left(\frac{2}{\sigma}\right)=0.8.
$$

所求概率为

$$
P\{X<0\}
=\Phi\left(\frac{0-2}{\sigma}\right)
=\Phi\left(-\frac{2}{\sigma}\right)
=1-\Phi\left(\frac{2}{\sigma}\right)
=0.2.
$$

### 第 21 题

- 答案：$\dfrac{1}{2}+\dfrac{1}{\pi}$

半圆

$$
0<y<\sqrt{2ax-x^2}
$$

可写为

$$
(x-a)^2+y^2<a^2,\qquad y>0.
$$

其面积为

$$
S_{\text{半圆}}=\frac{1}{2}\pi a^2.
$$

夹角小于 $\dfrac{\pi}{4}$ 等价于点在直线 $y=x$ 下方。直线 $y=x$ 与半圆交于 $(0,0)$ 和 $(a,a)$。

所求区域面积由三角形面积和四分之一圆面积组成：

$$
S=\frac{1}{2}a^2+\frac{1}{4}\pi a^2.
$$

因此概率为

$$
P=\frac{S}{S_{\text{半圆}}}
=\frac{\frac{1}{2}a^2+\frac{1}{4}\pi a^2}{\frac{1}{2}\pi a^2}
=\frac{1}{2}+\frac{1}{\pi}.
$$

### 第 22 题

- 答案：$F_Z(z)=\begin{cases}0,&z<0,\\1-(1+z)e^{-z},&z\ge0,\end{cases}$

由密度可知 $x>0,\ y>0$，因此

$$
Z=X+2Y\ge0.
$$

所以当 $z<0$ 时，

$$
F_Z(z)=0.
$$

当 $z\ge0$ 时，

$$
F_Z(z)=P(X+2Y\le z)
=\int_0^z\int_0^{(z-x)/2}2e^{-(x+2y)}\,dy\,dx.
$$

先对 $y$ 积分：

$$
\int_0^{(z-x)/2}2e^{-(x+2y)}\,dy
=e^{-x}-e^{-z}.
$$

于是

$$
F_Z(z)=\int_0^z(e^{-x}-e^{-z})\,dx
=1-e^{-z}-ze^{-z}.
$$

即

$$
F_Z(z)=
\begin{cases}
0,&z<0,\\
1-(1+z)e^{-z},&z\ge0.
\end{cases}
$$
