# Math 1 1996 Answers

资料类型：考研数学一答案解析
年份：1996
科目：数学一
范围：试卷 I
来源：D:\百度网盘\高数资料\【02】1987-2022年数学一真题详解答案（PDF）\1996考研数学一真题解析.pdf
校对状态：已按题干和答案页图像重新清洗，去除 OCR 碎行、串题内容和非本题页脚

## 答案速查

| 题号 | 题型 | 答案 |
|---|---|---|
| 1 | 填空题 | $\ln2$ |
| 2 | 填空题 | $2x+2y-3z=0$ |
| 3 | 填空题 | $y=e^x(C_1\cos x+C_2\sin x+1)$ |
| 4 | 填空题 | $\dfrac{1}{2}$ |
| 5 | 填空题 | $2$ |
| 6 | single_choice | D |
| 7 | single_choice | B |
| 8 | single_choice | A |
| 9 | single_choice | C |
| 10 | single_choice | D |
| 11 | 解答题 | $8a$ |
| 12 | 解答题 | $3$ |
| 13 | 解答题 | $-\dfrac{\pi}{2}$ |
| 14 | 解答题 | $a=3$ |
| 15 | 解答题 | $\dfrac{5}{8}-\dfrac{3}{4}\ln2$ |
| 16 | 解答题 | $f(x)=C_1\ln x+C_2\quad(x>0)$ |
| 17 | 解答题 | 见解析 |
| 18 | 解答题 | 见解析 |
| 19 | 解答题 | $c=3$，特征值为 $0,4,9$；曲面为椭圆柱面 |
| 20 | 填空题 | $\dfrac{3}{7}$ |
| 21 | 填空题 | $\sqrt{\dfrac{2}{\pi}}$ |
| 22 | 解答题 | 见解析；$E(X)=\dfrac{22}{9}$ |

## 详细解析

### 第 1 题

- 答案：$\ln2$

将底数化为
$$
\frac{x+2a}{x-a}=1+\frac{3a}{x-a}.
$$

于是
$$
\lim_{x\to\infty}\left(1+\frac{3a}{x-a}\right)^x
=e^{\lim_{x\to\infty}\frac{3ax}{x-a}}
=e^{3a}.
$$

题设极限为 $8$，故
$$
e^{3a}=8,
$$
从而
$$
a=\frac{1}{3}\ln8=\ln2.
$$


### 第 2 题

- 答案：$2x+2y-3z=0$

所求平面经过原点和点 $M(6,-3,2)$，故向量
$$
\overrightarrow{OM}=(6,-3,2)
$$
在平面内。

已知平面 $4x-y+2z=8$ 的法向量为
$$
\boldsymbol n_0=(4,-1,2).
$$

所求平面与该平面垂直，因此所求平面的法向量应同时垂直于 $\overrightarrow{OM}$ 和 $\boldsymbol n_0$，可取
$$
\boldsymbol n=\overrightarrow{OM}\times\boldsymbol n_0=(-4,-4,6).
$$

化简可取
$$
\boldsymbol n=(2,2,-3).
$$

又平面过原点，所以方程为
$$
2x+2y-3z=0.
$$


### 第 3 题

- 答案：$y=e^x(C_1\cos x+C_2\sin x+1)$

齐次方程
$$
y''-2y'+2y=0
$$
的特征方程为
$$
r^2-2r+2=0,
$$
解得
$$
r=1\pm i.
$$

故齐次通解为
$$
y_h=e^x(C_1\cos x+C_2\sin x).
$$

对非齐次项 $e^x$，设特解 $y_p=Ae^x$。代入原方程得
$$
Ae^x-2Ae^x+2Ae^x=Ae^x=e^x,
$$
所以 $A=1$。

因此通解为
$$
y=e^x(C_1\cos x+C_2\sin x+1).
$$


### 第 4 题

- 答案：$\dfrac{1}{2}$

方向向量
$$
\overrightarrow{AB}=(2,-2,1),
$$
单位方向向量为
$$
\boldsymbol e=\frac{1}{3}(2,-2,1).
$$

对
$$
u=\ln\left(x+\sqrt{y^2+z^2}\right)
$$
求梯度：
$$
u_x=\frac{1}{x+\sqrt{y^2+z^2}},
$$
$$
u_y=\frac{y}{(x+\sqrt{y^2+z^2})\sqrt{y^2+z^2}},
\qquad
u_z=\frac{z}{(x+\sqrt{y^2+z^2})\sqrt{y^2+z^2}}.
$$

在 $A(1,0,1)$ 处，
$$
\nabla u(A)=\left(\frac{1}{2},0,\frac{1}{2}\right).
$$

方向导数为
$$
\nabla u(A)\cdot\boldsymbol e
=\frac{1}{2}\cdot\frac{2}{3}+0\cdot\left(-\frac{2}{3}\right)
+\frac{1}{2}\cdot\frac{1}{3}
=\frac{1}{2}.
$$


### 第 5 题

- 答案：$2$

计算
$$
|B|=
\begin{vmatrix}
1&0&2\\
0&2&0\\
-1&0&3
\end{vmatrix}
=10\ne0.
$$

所以 $B$ 可逆。右乘可逆矩阵不改变矩阵的秩，因此
$$
r(AB)=r(A)=2.
$$


### 第 6 题

- 答案：D

设
$$
M=\frac{x+ay}{(x+y)^2},\qquad N=\frac{y}{(x+y)^2}.
$$

该微分式为全微分的条件是
$$
\frac{\partial M}{\partial y}=\frac{\partial N}{\partial x}.
$$

计算得
$$
\frac{\partial M}{\partial y}
=\frac{(a-2)x-ay}{(x+y)^3},
$$
而
$$
\frac{\partial N}{\partial x}
=-\frac{2y}{(x+y)^3}.
$$

比较分子：
$$
(a-2)x-ay=-2y.
$$

故
$$
a=2.
$$

选 D。


### 第 7 题

- 答案：B

由
$$
\lim_{x\to0}\frac{f''(x)}{|x|}=1>0
$$
可知，在 $0$ 的某去心邻域内有
$$
f''(x)>0.
$$

因此 $f'(x)$ 在该邻域内单调递增。又 $f'(0)=0$，故当 $x<0$ 且充分接近 $0$ 时 $f'(x)<0$，当 $x>0$ 且充分接近 $0$ 时 $f'(x)>0$。

于是 $f(x)$ 在 $x=0$ 处取得极小值，选 B。


### 第 8 题

- 答案：A

因为 $\sum a_n$ 为正项收敛级数，所以其子级数
$$
\sum a_{2n}
$$
也收敛。

又
$$
\lim_{n\to\infty}n\tan\frac{\lambda}{n}=\lambda>0.
$$

因此正项级数
$$
\sum \left(n\tan\frac{\lambda}{n}\right)a_{2n}
$$
与 $\sum a_{2n}$ 同敛散，故收敛。

原级数的绝对值级数收敛，所以原级数绝对收敛，选 A。


### 第 9 题

- 答案：C

先写成
$$
F(x)=x^2\int_0^x f(t)\,dt-\int_0^x t^2f(t)\,dt.
$$

求导得
$$
F'(x)=2x\int_0^x f(t)\,dt.
$$

因为 $f(0)=0,\ f'(0)\ne0$，所以
$$
f(t)\sim f'(0)t\qquad(t\to0).
$$

于是
$$
\int_0^x f(t)\,dt\sim \frac{1}{2} f'(0)x^2.
$$

因此
$$
F'(x)\sim f'(0)x^3.
$$

所以 $F'(x)$ 是 $x$ 的三阶无穷小，选 C。


### 第 10 题

- 答案：D

按第一行展开并继续化简，可得
$$
\begin{vmatrix}
a_1&0&0&b_1\\
0&a_2&b_2&0\\
0&b_3&a_3&0\\
b_4&0&0&a_4
\end{vmatrix}
=a_1a_4
\begin{vmatrix}
a_2&b_2\\
b_3&a_3
\end{vmatrix}
-b_1b_4
\begin{vmatrix}
a_2&b_2\\
b_3&a_3
\end{vmatrix}.
$$

故
$$
D=(a_2a_3-b_2b_3)(a_1a_4-b_1b_4).
$$

选 D。


### 第 11 题

- 答案：$8a$

极坐标曲线弧长公式为
$$
s=\int \sqrt{r^2(\theta)+[r'(\theta)]^2}\,d\theta.
$$

对
$$
r=a(1+\cos\theta)
$$
有
$$
r'=-a\sin\theta.
$$

于是
$$
\sqrt{r^2+(r')^2}
=a\sqrt{(1+\cos\theta)^2+\sin^2\theta}
=a\sqrt{2(1+\cos\theta)}
=2a\left|\cos\frac{\theta}{2}\right|.
$$

该心形线关于极轴对称，取 $\theta\in[0,\pi]$ 后加倍：
$$
s=2\int_0^\pi 2a\cos\frac{\theta}{2}\,d\theta
=4a\cdot2\sin\frac{\theta}{2}\bigg|_0^\pi
=8a.
$$


### 第 12 题

- 答案：$3$

由 $x_1=10>0$ 和递推式知 $x_n>0$。

先证单调递减。由于
$$
x_2=\sqrt{6+10}=4<10=x_1.
$$
若 $x_n<x_{n-1}$，则
$$
x_{n+1}=\sqrt{6+x_n}<\sqrt{6+x_{n-1}}=x_n.
$$
由归纳法，$\{x_n\}$ 单调递减。

又 $x_n>0$，所以该数列有下界。由单调有界准则，极限存在。

设
$$
\lim_{n\to\infty}x_n=L\quad(L\ge0).
$$
在
$$
x_{n+1}=\sqrt{6+x_n}
$$
两边取极限，得
$$
L=\sqrt{6+L}.
$$

解得
$$
L=3\quad\text{或}\quad L=-2.
$$

因 $L\ge0$，故
$$
\lim_{n\to\infty}x_n=3.
$$


### 第 13 题

- 答案：$-\dfrac{\pi}{2}$

曲面为
$$
S:\ z=x^2+y^2,\qquad 0\le z\le1,
$$
且法向量与 $z$ 轴正向夹角为锐角，即取上侧。

对上侧曲面，有
$$
dy\,dz=-z_x\,dx\,dy,\qquad dx\,dy=dx\,dy.
$$

其中
$$
z_x=2x,\qquad z=x^2+y^2,
$$
投影区域为
$$
D:x^2+y^2\le1.
$$

因此
$$
I=\iint_D\left[(2x+z)(-z_x)+z\right]dx\,dy.
$$

代入得
$$
I=\iint_D\left[-2x(2x+x^2+y^2)+(x^2+y^2)\right]dx\,dy.
$$

由圆域对称性，
$$
\iint_D2x(x^2+y^2)\,dx\,dy=0,
$$
且
$$
\iint_D4x^2\,dx\,dy=2\iint_D(x^2+y^2)\,dx\,dy.
$$

于是
$$
I=-\iint_D(x^2+y^2)\,dx\,dy.
$$

极坐标下
$$
I=-\int_0^{2\pi}\int_0^1 r^2\cdot r\,dr\,d\theta
=-\frac{\pi}{2}.
$$


### 第 14 题

- 答案：$a=3$

由
$$
u=x-2y,\qquad v=x+ay
$$
得
$$
z_x=z_u+z_v,\qquad z_y=-2z_u+az_v.
$$

继续求二阶偏导：
$$
z_{xx}=z_{uu}+2z_{uv}+z_{vv},
$$
$$
z_{xy}=-2z_{uu}+(a-2)z_{uv}+az_{vv},
$$
$$
z_{yy}=4z_{uu}-4az_{uv}+a^2z_{vv}.
$$

代入
$$
6z_{xx}+z_{xy}-z_{yy}=0,
$$
整理得
$$
(10+5a)z_{uv}+(6+a-a^2)z_{vv}=0.
$$

要化为
$$
z_{uv}=0,
$$
需
$$
6+a-a^2=0
$$
且
$$
10+5a\ne0.
$$

由 $6+a-a^2=0$ 得 $a=3$ 或 $a=-2$。当 $a=-2$ 时，$10+5a=0$，不合题意；故
$$
a=3.
$$


### 第 15 题

- 答案：$\dfrac{5}{8}-\dfrac{3}{4}\ln2$

先作部分分式分解：
$$
\frac{1}{n^2-1}
=\frac{1}{2}\left(\frac{1}{n-1}-\frac{1}{n+1}\right).
$$

所以
$$
\sum_{n=2}^{\infty}\frac{1}{(n^2-1)2^n}
=\sum_{n=2}^{\infty}\frac{1}{2^{n+1}}
\left(\frac{1}{n-1}-\frac{1}{n+1}\right).
$$

把两部分错位整理：
$$
A=\sum_{n=1}^{\infty}\frac{1}{2^{n+2}n}
-\sum_{n=3}^{\infty}\frac{1}{2^n n}.
$$

利用
$$
-\ln(1-x)=\sum_{n=1}^{\infty}\frac{x^n}{n}\quad(|x|<1)
$$
取 $x=\frac{1}{2}$，可得
$$
\sum_{n=1}^{\infty}\frac{1}{2^n n}=\ln2.
$$

于是
$$
\sum_{n=1}^{\infty}\frac{1}{2^{n+2}n}=\frac{1}{4}\ln2,
$$
而
$$
\sum_{n=3}^{\infty}\frac{1}{2^n n}
=\ln2-\frac{1}{2}-\frac{1}{8}.
$$

故
$$
A=\frac{1}{4}\ln2-\left(\ln2-\frac{5}{8}\right)
=\frac{5}{8}-\frac{3}{4}\ln2.
$$


### 第 16 题

- 答案：$f(x)=C_1\ln x+C_2\quad(x>0)$

曲线 $y=f(x)$ 在点 $(x,f(x))$ 处的切线为
$$
Y-f(x)=f'(x)(X-x).
$$

令 $X=0$，得 $y$ 轴截距
$$
Y=f(x)-xf'(x).
$$

由题意，
$$
f(x)-xf'(x)=\frac{1}{x}\int_0^x f(t)\,dt.
$$

两边乘以 $x$：
$$
xf(x)-x^2f'(x)=\int_0^x f(t)\,dt.
$$

对 $x$ 求导：
$$
f(x)=f(x)+xf'(x)-2xf'(x)-x^2f''(x),
$$
即
$$
xy''+y'=0.
$$

因此
$$
(xy')'=0,
$$
所以
$$
xy'=C_1.
$$

由于 $x>0$，
$$
y'= \frac{C_1}{x}.
$$

积分得
$$
f(x)=C_1\ln x+C_2.
$$


### 第 17 题

- 答案：见解析

(1) 对任意 $c,x\in[0,1]$，在点 $c$ 处带拉格朗日型余项的一阶泰勒公式为
$$
f(x)=f(c)+f'(c)(x-c)+\frac{1}{2}f''(\xi)(x-c)^2,
$$
其中 $\xi$ 介于 $c$ 与 $x$ 之间。

(2) 固定任意 $c\in[0,1]$。分别令上式中的 $x=0$ 与 $x=1$，得
$$
f(0)=f(c)-cf'(c)+\frac{1}{2}f''(\xi_0)c^2,
$$
$$
f(1)=f(c)+(1-c)f'(c)+\frac{1}{2}f''(\xi_1)(1-c)^2.
$$

两式相减：
$$
f(1)-f(0)=f'(c)+\frac{1}{2}\left[f''(\xi_1)(1-c)^2-f''(\xi_0)c^2\right].
$$

所以
$$
|f'(c)|
\le |f(1)|+|f(0)|
+\frac{1}{2}|f''(\xi_1)|(1-c)^2
+\frac{1}{2}|f''(\xi_0)|c^2.
$$

由题设 $|f(x)|\le a,\ |f''(x)|\le b$，
$$
|f'(c)|\le2a+\frac{b}{2}\bigl[(1-c)^2+c^2\bigr].
$$

由于 $0\le c\le1$ 时
$$
(1-c)^2+c^2\le1,
$$
故
$$
|f'(c)|\le2a+\frac{b}{2}.
$$

因 $c$ 任意，结论成立。


### 第 18 题

- 答案：见解析

(1) 由
$$
A=E-\xi\xi^T
$$
得
$$
A^2=(E-\xi\xi^T)^2
=E-2\xi\xi^T+\xi(\xi^T\xi)\xi^T
=E-(2-\xi^T\xi)\xi\xi^T.
$$

因此
$$
A^2=A
$$
等价于
$$
E-(2-\xi^T\xi)\xi\xi^T=E-\xi\xi^T,
$$
即
$$
(\xi^T\xi-1)\xi\xi^T=0.
$$

由于 $\xi$ 为非零列向量，$\xi\xi^T\ne0$，故
$$
A^2=A
\quad\Longleftrightarrow\quad
\xi^T\xi=1.
$$

(2) 当 $\xi^T\xi=1$ 时，
$$
A\xi=(E-\xi\xi^T)\xi
=\xi-\xi(\xi^T\xi)=0.
$$

而 $\xi\ne0$，所以 $A$ 有非零零向量，故 $A$ 不可逆。


### 第 19 题

- 答案：$c=3$，特征值为 $0,4,9$；曲面为椭圆柱面

二次型对应的对称矩阵为
$$
A=\begin{pmatrix}
5&-1&3\\
-1&5&-3\\
3&-3&c
\end{pmatrix}.
$$

题设二次型秩为 $2$，即 $r(A)=2$。由行列式为零并结合二阶子式不全为零，可得
$$
c=3.
$$

此时
$$
A=\begin{pmatrix}
5&-1&3\\
-1&5&-3\\
3&-3&3
\end{pmatrix}.
$$

其特征多项式为
$$
|\lambda E-A|=\lambda(\lambda-4)(\lambda-9).
$$

所以特征值为
$$
0,\ 4,\ 9.
$$

经正交变换，二次型可化为
$$
4y_2^2+9y_3^2.
$$

因此方程
$$
f(x_1,x_2,x_3)=1
$$
化为
$$
4y_2^2+9y_3^2=1,
$$
它表示椭圆柱面。


### 第 20 题

- 答案：$\dfrac{3}{7}$

设事件 $C$ 表示“抽到次品”，事件 $A$ 表示“产品来自 A 厂”。

题给
$$
P(A)=0.6,\qquad P(\bar A)=0.4,
$$
$$
P(C\mid A)=0.01,\qquad P(C\mid\bar A)=0.02.
$$

由贝叶斯公式，
$$
P(A\mid C)
=\frac{P(A)P(C\mid A)}
{P(A)P(C\mid A)+P(\bar A)P(C\mid\bar A)}.
$$

代入数据：
$$
P(A\mid C)
=\frac{0.6\cdot0.01}{0.6\cdot0.01+0.4\cdot0.02}
=\frac{3}{7}.
$$


### 第 21 题

- 答案：$\sqrt{\dfrac{2}{\pi}}$

令
$$
U=\xi-\eta.
$$

由于 $\xi,\eta$ 相互独立，且
$$
\xi,\eta\sim N\left(0,\frac{1}{2}\right),
$$
所以
$$
E(U)=0,
$$
$$
D(U)=D(\xi)+D(\eta)=\frac{1}{2}+\frac{1}{2}=1.
$$

因此
$$
U\sim N(0,1).
$$

于是
$$
E|\xi-\eta|=E|U|
=2\int_0^\infty u\frac{1}{\sqrt{2\pi}}e^{-u^2/2}\,du.
$$

计算得
$$
E|U|=\sqrt{\frac{2}{\pi}}.
$$


### 第 22 题

- 答案：见解析；$E(X)=\dfrac{22}{9}$

由
$$
X=\max\{\xi,\eta\},\qquad Y=\min\{\xi,\eta\},
$$
必有 $Y\le X$。又 $\xi,\eta$ 独立且均在 $1,2,3$ 上等概率取值。

按题干表头 $Y\backslash X$，即“行是 $Y$，列是 $X$”，联合分布律为
$$
\begin{array}{c|ccc}
Y\backslash X&1&2&3\\ \hline
1&\frac{1}{9}&\frac{2}{9}&\frac{2}{9}\\
2&0&\frac{1}{9}&\frac{2}{9}\\
3&0&0&\frac{1}{9}
\end{array}
$$

例如
$$
P\{X=2,Y=1\}=P\{(\xi,\eta)=(2,1)\ \text{或}\ (1,2)\}=\frac{2}{9}.
$$

由上表求 $X$ 的边缘分布：
$$
P\{X=1\}=\frac{1}{9},\qquad
P\{X=2\}=\frac{3}{9},\qquad
P\{X=3\}=\frac{5}{9}.
$$

所以
$$
E(X)=1\cdot\frac{1}{9}+2\cdot\frac{3}{9}+3\cdot\frac{5}{9}
=\frac{22}{9}.
$$
