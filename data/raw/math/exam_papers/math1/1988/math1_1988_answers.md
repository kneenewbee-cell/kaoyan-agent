# Math 1 1988 Answers

资料类型：考研数学一答案解析
年份：1988
科目：数学一
范围：试卷 I
来源：D:\百度网盘\高数资料\【02】1987-2022年数学一真题详解答案（PDF）\1988数学一真题答案解析（试卷一）.pdf
校对状态：已按题干和答案页图像重新清洗，去除 OCR 碎行和串题内容

## 答案速查

| 题号 | 题型 | 答案 |
|---|---|---|
| 1 | 解答题 | $[0,6)$ |
| 2 | 解答题 | $\varphi(x)=\sqrt{\ln(1-x)}$，定义域为 $(-\infty,0]$ |
| 3 | 解答题 | $\dfrac{12\pi}{5}$ |
| 4 | 填空题 | $(2t+1)e^{2t}$ |
| 5 | 填空题 | $\dfrac{3}{2}$ |
| 6 | 填空题 | $\dfrac{1}{12}$ |
| 7 | 填空题 | $40$ |
| 8 | 选择题 | B |
| 9 | 选择题 | A |
| 10 | 选择题 | C |
| 11 | 选择题 | B |
| 12 | 选择题 | D |
| 13 | 解答题 | $0$ |
| 14 | 解答题 | $y=(1-2x)e^x$ |
| 15 | 解答题 | $k\left(1-\dfrac{1}{\sqrt5}\right)$ |
| 16 | 解答题 | $A=\begin{pmatrix}1&0&0\\2&0&0\\6&-1&-1\end{pmatrix}$，且 $A^5=A$ |
| 17 | 解答题 | $x=0,\ y=1$；可取 $P=\begin{pmatrix}1&0&0\\0&1&1\\0&1&-1\end{pmatrix}$ |
| 18 | 解答题 | 见解析 |
| 19 | 填空题 | $\dfrac{1}{3}$ |
| 20 | 填空题 | $\dfrac{17}{25}$ |
| 21 | 填空题 | $0.9876$ |
| 22 | 解答题 | $f_Y(y)=\dfrac{3(1-y)^2}{\pi\left[1+(1-y)^6\right]}$ |

## 详细解析

### 第 1 题

- 答案：$[0,6)$

记

$$
u_n=\frac{(x-3)^n}{n3^n}.
$$

由比值判别法，

$$
\lim_{n\to\infty}\left|\frac{u_{n+1}}{u_n}\right|
=
\lim_{n\to\infty}
\left|
\frac{(x-3)^{n+1}}{(n+1)3^{n+1}}
\cdot
\frac{n3^n}{(x-3)^n}
\right|
=\frac{|x-3|}{3}.
$$

当 $\frac{|x-3|}{3}<1$，即 $0<x<6$ 时，幂级数收敛。

当 $x=0$ 时，原级数为

$$
\sum_{n=1}^{\infty}\frac{(-1)^n}{n},
$$

收敛。

当 $x=6$ 时，原级数为

$$
\sum_{n=1}^{\infty}\frac{1}{n},
$$

发散。

所以收敛域为 $[0,6)$。

### 第 2 题

- 答案：$\varphi(x)=\sqrt{\ln(1-x)}$，定义域为 $(-\infty,0]$

由

$$
f(x)=e^{x^2},\quad f[\varphi(x)]=1-x
$$

得

$$
e^{[\varphi(x)]^2}=1-x.
$$

两边取自然对数：

$$
[\varphi(x)]^2=\ln(1-x).
$$

又 $\varphi(x)\ge 0$，所以

$$
\varphi(x)=\sqrt{\ln(1-x)}.
$$

为使根号内有意义，需

$$
\ln(1-x)\ge 0 \iff 1-x\ge 1 \iff x\le 0.
$$

故定义域为 $(-\infty,0]$。

### 第 3 题

- 答案：$\dfrac{12\pi}{5}$

令 $\Omega$ 为单位球 $x^2+y^2+z^2\le 1$。由高斯公式，

$$
I=\iiint_{\Omega}
\left(
\frac{\partial x^3}{\partial x}
+\frac{\partial y^3}{\partial y}
+\frac{\partial z^3}{\partial z}
\right)\,dv
=3\iiint_{\Omega}(x^2+y^2+z^2)\,dv.
$$

用球坐标计算：

$$
I
=3\int_0^{2\pi}d\theta\int_0^\pi d\varphi\int_0^1
r^2\cdot r^2\sin\varphi\,dr
=3\cdot 2\pi\cdot 2\cdot \frac{1}{5}
=\frac{12\pi}{5}.
$$

### 第 4 题

- 答案：$(2t+1)e^{2t}$

由

$$
\lim_{x\to\infty}\left(1+\frac{1}{x}\right)^{2tx}=e^{2t},
$$

得

$$
f(t)=t e^{2t}.
$$

因此

$$
f'(t)=e^{2t}+2t e^{2t}=(2t+1)e^{2t}.
$$

### 第 5 题

- 答案：$\dfrac{3}{2}$

答案页写作 $\dfrac{2}{3}$，但这与题干和傅里叶级数收敛定理不一致。按题干推导如下。

该函数以 $2$ 为周期。傅里叶级数在跳跃间断点处收敛于左右极限的平均值。

在 $x=1$ 处，

$$
f(1-0)=1^3=1.
$$

由周期性，

$$
f(1+0)=f(-1+0)=2.
$$

所以傅里叶级数在 $x=1$ 处收敛于

$$
\frac{f(1-0)+f(1+0)}{2}
=\frac{1+2}{2}
=\frac{3}{2}.
$$

因此，按当前题干，傅里叶级数在 $x=1$ 处的收敛值应为 $\dfrac{3}{2}$。源答案页的 $\dfrac{2}{3}$ 与上述步骤不符，按排印或答案页录入错误处理。

### 第 6 题

- 答案：$\dfrac{1}{12}$

对等式

$$
\int_0^{x^3-1}f(t)\,dt=x
$$

两边关于 $x$ 求导，得

$$
f(x^3-1)\cdot 3x^2=1.
$$

要求 $f(7)$，令 $x^3-1=7$，得 $x=2$。于是

$$
f(7)=\frac{1}{3\cdot 2^2}=\frac{1}{12}.
$$

### 第 7 题

- 答案：$40$

因为

$$
A+B=(\alpha+\beta,\ 2\gamma_2,\ 2\gamma_3,\ 2\gamma_4),
$$

由行列式关于列的线性性，

$$
|A+B|
=8|\alpha+\beta,\gamma_2,\gamma_3,\gamma_4|
=8\left(|A|+|B|\right)
=8(4+1)=40.
$$

### 第 8 题

- 答案：B

函数在 $x=x_0$ 处的微分为

$$
dy=f'(x_0)\Delta x=\frac{1}{2}\Delta x.
$$

当 $\Delta x\to 0$ 时，$dy$ 与 $\Delta x$ 同阶；但二者之比趋于 $\frac{1}{2}$，不是 $1$，所以不是等价无穷小。

故选 B。

### 第 9 题

- 答案：A

由微分方程

$$
y''-2y'+4y=0
$$

得

$$
f''(x_0)=2f'(x_0)-4f(x_0).
$$

已知 $f'(x_0)=0,\ f(x_0)>0$，所以

$$
f''(x_0)=-4f(x_0)<0.
$$

因此 $f(x)$ 在 $x_0$ 处取得极大值。

故选 A。

### 第 10 题

- 答案：C

$\Omega_1$ 是上半球，$\Omega_2$ 是第一卦限内的八分之一球。

对被积函数 $z$，在上半球内关于 $x,y$ 对称，且 $\Omega_1$ 可以按 $x,y$ 的符号分成 $4$ 个与 $\Omega_2$ 对称的部分，所以

$$
\iiint_{\Omega_1}z\,dv
=4\iiint_{\Omega_2}z\,dv.
$$

而 $x,y,xyz$ 在相关对称区域中会出现正负抵消或符号不一致，不能得到对应选项的等式。

故选 C。

### 第 11 题

- 答案：B

设

$$
b_n=a_n(-2)^n.
$$

已知级数在 $x=-1$ 处收敛，即 $\sum b_n$ 收敛，因此 $b_n\to 0$，从而 $\{b_n\}$ 有界。设 $|b_n|\le M$。

当 $x=2$ 时，原级数为

$$
\sum_{n=1}^{\infty}a_n.
$$

又

$$
|a_n|=\frac{|b_n|}{2^n}\le \frac{M}{2^n},
$$

故 $\sum |a_n|$ 收敛，所以在 $x=2$ 处绝对收敛。

故选 B。

### 第 12 题

- 答案：D

向量组线性无关的等价刻画是：其中任意一个向量都不能由其余向量线性表示。

选项 A 只说明存在某个非零线性组合不为零，这对线性相关向量组也可能成立，不充分。

选项 B 只要求任意两个向量线性无关，不能排除三个或更多向量之间的线性相关。

选项 C 只要求存在一个向量不能由其余向量表示，也不足以推出整个向量组线性无关。

故选 D。

### 第 13 题

- 答案：$0$

由

$$
u=yf\left(\frac{x}{y}\right)+xg\left(\frac{y}{x}\right)
$$

可得

$$
\frac{\partial u}{\partial x}
=f'\left(\frac{x}{y}\right)
+g\left(\frac{y}{x}\right)
-\frac{y}{x}g'\left(\frac{y}{x}\right).
$$

继续求导：

$$
\frac{\partial^2u}{\partial x^2}
=\frac{1}{y} f''\left(\frac{x}{y}\right)
+\frac{y^2}{x^3}g''\left(\frac{y}{x}\right),
$$

$$
\frac{\partial^2u}{\partial x\partial y}
=-\frac{x}{y^2}f''\left(\frac{x}{y}\right)
-\frac{y}{x^2}g''\left(\frac{y}{x}\right).
$$

因此

$$
x\frac{\partial^2u}{\partial x^2}
+y\frac{\partial^2u}{\partial x\partial y}
=0.
$$

### 第 14 题

- 答案：$y=(1-2x)e^x$

对应齐次方程

$$
y''-3y'+2y=0
$$

的特征根为 $1,2$，故齐次通解为

$$
Y=C_1e^x+C_2e^{2x}.
$$

由于右端为 $2e^x$，取特解

$$
y^*=Axe^x.
$$

代入原方程得 $A=-2$，所以

$$
y=C_1e^x+C_2e^{2x}-2xe^x.
$$

曲线 $y=x^2-x+1$ 在 $(0,1)$ 处的切线斜率为 $-1$，因此

$$
y(0)=1,\quad y'(0)=-1.
$$

代入通解：

$$
\begin{cases}
C_1+C_2=1,\\
C_1+2C_2=1,
\end{cases}
$$

解得 $C_1=1,\ C_2=0$。

故

$$
y=(1-2x)e^x.
$$

### 第 15 题

- 答案：$k\left(1-\dfrac{1}{\sqrt5}\right)$

设质点 $M$ 的坐标为 $(x,y)$。由 $A(0,1)$ 指向 $M(x,y)$ 的距离为

$$
r=\sqrt{x^2+(1-y)^2}.
$$

引力方向与 $\overrightarrow{MA}=\{-x,1-y\}$ 一致，故力为

$$
\vec F=\frac{k}{r^3}\{-x,1-y\}.
$$

所作功为

$$
W=\int_{\widehat{BO}}\frac{k}{r^3}\left[-x\,dx+(1-y)\,dy\right].
$$

由于

$$
d\left(\frac{1}{r}\right)
=\frac{-x\,dx+(1-y)\,dy}{r^3},
$$

所以

$$
W=k\left[\frac{1}{r}\right]_B^O.
$$

在 $O(0,0)$ 处 $r=1$，在 $B(2,0)$ 处 $r=\sqrt5$，故

$$
W=k\left(1-\frac{1}{\sqrt5}\right).
$$

### 第 16 题

- 答案：$A=\begin{pmatrix}1&0&0\\2&0&0\\6&-1&-1\end{pmatrix}$，且 $A^5=A$

由

$$
P=
\begin{pmatrix}
1&0&0\\
2&-1&0\\
2&1&1
\end{pmatrix}
$$

可求得

$$
P^{-1}=
\begin{pmatrix}
1&0&0\\
2&-1&0\\
-4&1&1
\end{pmatrix}.
$$

由 $AP=PB$，得

$$
A=PBP^{-1}.
$$

因此

$$
A=
\begin{pmatrix}
1&0&0\\
2&0&0\\
6&-1&-1
\end{pmatrix}.
$$

又因

$$
B^5=B,
$$

所以

$$
A^5=(PBP^{-1})^5=PB^5P^{-1}=PBP^{-1}=A.
$$

### 第 17 题

- 答案：$x=0,\ y=1$；可取 $P=\begin{pmatrix}1&0&0\\0&1&1\\0&1&-1\end{pmatrix}$

因为 $A$ 与 $B$ 相似，所以二者特征多项式相同：

$$
|\lambda E-A|=|\lambda E-B|.
$$

即

$$
(\lambda-2)(\lambda^2-x\lambda-1)
=
(\lambda-2)(\lambda^2+(1-y)\lambda-y).
$$

比较系数得

$$
x=0,\quad y=1.
$$

此时

$$
A=
\begin{pmatrix}
2&0&0\\
0&0&1\\
0&1&0
\end{pmatrix},
\quad
B=
\begin{pmatrix}
2&0&0\\
0&1&0\\
0&0&-1
\end{pmatrix}.
$$

$A$ 的三个特征值为 $2,1,-1$。可分别取特征向量

$$
p_1=\begin{pmatrix}1\\0\\0\end{pmatrix},\quad
p_2=\begin{pmatrix}0\\1\\1\end{pmatrix},\quad
p_3=\begin{pmatrix}0\\1\\-1\end{pmatrix}.
$$

令

$$
P=(p_1,p_2,p_3)
=
\begin{pmatrix}
1&0&0\\
0&1&1\\
0&1&-1
\end{pmatrix},
$$

则 $P$ 可逆，且

$$
P^{-1}AP=B.
$$

### 第 18 题

- 答案：见解析

对 $t\in[a,b]$，令

$$
F(t)=
\int_a^t [f(t)-f(x)]\,dx
-3\int_t^b [f(x)-f(t)]\,dx.
$$

则 $F(t)$ 在 $[a,b]$ 上连续。

因为 $f'(x)>0$，所以 $f(x)$ 在 $[a,b]$ 上单调增加。取 $c\in(a,b)$，则

$$
F(a)
=-3\int_a^b[f(x)-f(a)]\,dx
<0,
$$

且

$$
F(b)
=\int_a^b[f(b)-f(x)]\,dx
>0.
$$

由介值定理，存在 $\xi\in(a,b)$，使 $F(\xi)=0$。这正表示

$$
S_1=3S_2.
$$

下面证唯一性。对 $F(t)$ 求导：

$$
F'(t)=f'(t)\big[(t-a)+3(b-t)\big].
$$

由于 $f'(t)>0$，且

$$
(t-a)+3(b-t)>0,
$$

故 $F'(t)>0$。因此 $F(t)$ 在 $(a,b)$ 内严格单调增加，零点唯一。

所以在 $(a,b)$ 内存在唯一的 $\xi$，使 $S_1=3S_2$。

### 第 19 题

- 答案：$\dfrac{1}{3}$

设事件 $A$ 在一次试验中出现的概率为 $p$。由题意，

$$
1-(1-p)^3=\frac{19}{27}.
$$

因此

$$
(1-p)^3=\frac{8}{27},
$$

得

$$
1-p=\frac{2}{3},\quad p=\frac{1}{3}.
$$

### 第 20 题

- 答案：$\dfrac{17}{25}$

设随机取到的两个数为 $X,Y$，则样本空间为单位正方形

$$
0<X<1,\quad 0<Y<1.
$$

要求事件

$$
X+Y<\frac{6}{5}.
$$

其补事件为 $X+Y\ge \frac{6}{5}$。在单位正方形中，补事件对应右上角直角三角形，两条直角边长度均为

$$
1-\frac{1}{5}=\frac{4}{5}.
$$

故补事件面积为

$$
\frac{1}{2}\cdot \frac{4}{5}\cdot \frac{4}{5}=\frac{8}{25}.
$$

所求概率为

$$
1-\frac{8}{25}=\frac{17}{25}.
$$

### 第 21 题

- 答案：$0.9876$

由题意，$X$ 服从均值 $10$、标准差 $0.02$ 的正态分布。于是

$$
P(9.95<X<10.05)
=P\left(\frac{9.95-10}{0.02}<Z<\frac{10.05-10}{0.02}\right),
$$

即

$$
P(-2.5<Z<2.5)=2\Phi(2.5)-1.
$$

代入 $\Phi(2.5)=0.9938$，得

$$
2\times 0.9938-1=0.9876.
$$

### 第 22 题

- 答案：

$$
f_Y(y)=\frac{3(1-y)^2}{\pi\left[1+(1-y)^6\right]}.
$$

这里的关键是变量变换时要乘上反函数导数的绝对值。

由

$$
Y=1-\sqrt[3]{X}
$$

得

$$
X=(1-Y)^3.
$$

先求分布函数：

$$
F_Y(y)=P(Y<y)
=P\left(1-\sqrt[3]{X}<y\right)
=P\left(X>(1-y)^3\right).
$$

因此

$$
F_Y(y)
=\int_{(1-y)^3}^{+\infty}\frac{dx}{\pi(1+x^2)}
=\frac{1}{\pi}\left[\frac{\pi}{2}-\arctan(1-y)^3\right].
$$

对 $y$ 求导，得

$$
f_Y(y)
=\frac{d}{dy}F_Y(y)
=\frac{3(1-y)^2}{\pi\left[1+(1-y)^6\right]}.
$$

其中

$$
\left|\frac{d}{dy}(1-y)^3\right|=3(1-y)^2,
$$

这正是变量变换时需要乘上的反函数导数绝对值。
