# Math 1 2004 Answers

资料类型：考研数学一答案解析
年份：2004
科目：数学一
范围：试卷 I
来源：D:\百度网盘\高数资料\【02】1987-2022年数学一真题详解答案（PDF）\2004考研数学一真题解析.pdf
校对状态：已按答案页图像和题干重新整理，去除识别碎行、串题内容和非本题页脚。

## 答案速查

| 题号 | 题型 | 答案 |
|---|---|---|
| 1 | 填空题 | $y=x-1$ |
| 2 | 填空题 | $\displaystyle f(x)=\frac{1}{2}(\ln x)^2$ |
| 3 | 填空题 | $\displaystyle \frac{3\pi}{2}$ |
| 4 | 填空题 | $\displaystyle y=\frac{C_1}{x}+\frac{C_2}{x^2}$ |
| 5 | 填空题 | $\displaystyle \frac{1}{9}$ |
| 6 | 填空题 | $\displaystyle \frac{1}{e}$ |
| 7 | 选择题 | B |
| 8 | 选择题 | C |
| 9 | 选择题 | B |
| 10 | 选择题 | B |
| 11 | 选择题 | D |
| 12 | 选择题 | A |
| 13 | 选择题 | C |
| 14 | 选择题 | A |
| 15 | 解答题 | 结论成立。 |
| 16 | 解答题 | $1.05\,\mathrm{km}$ |
| 17 | 解答题 | $-\pi$ |
| 18 | 解答题 | 方程有唯一正实根；当 $\alpha>1$ 时，$\displaystyle\sum_{n=1}^{\infty}x_n^\alpha$ 收敛。 |
| 19 | 解答题 | 极小值点为 $(9,3)$，极小值为 $3$；极大值点为 $(-9,-3)$，极大值为 $-3$。 |
| 20 | 解答题 | 当 $a=0$ 或 $a=-\dfrac{n(n+1)}{2}$ 时有非零解。若 $a=0$，通解为 $x=k_1\eta_1+\cdots+k_{n-1}\eta_{n-1}$，其中 $\eta_i=(-1,0,\ldots,0,1,0,\ldots,0)^T$，第 $i+1$ 个分量为 $1$；若 $a=-\dfrac{n(n+1)}{2}$，通解为 $x=k(1,2,\ldots,n)^T$。 |
| 21 | 解答题 | $a=-2$ 时，$A$ 可相似对角化；$a=-\dfrac{2}{3}$ 时，$A$ 不可相似对角化。 |
| 22 | 解答题 | $(X,Y)$ 的分布为 $P(0,0)=\dfrac{2}{3}$，$P(0,1)=\dfrac{1}{12}$，$P(1,0)=\dfrac{1}{6}$，$P(1,1)=\dfrac{1}{12}$；$\displaystyle \rho_{XY}=\frac{\sqrt{15}}{15}$。 |
| 23 | 解答题 | 矩估计量 $\displaystyle \hat\beta_M=\frac{\bar X}{\bar X-1}$；最大似然估计量 $\displaystyle \hat\beta=\frac{n}{\sum_{i=1}^n\ln X_i}$。 |

## 详细解析

### 第 1 题

**答案：** $y=x-1$

直线 $x+y=1$ 的斜率为 $-1$，与它垂直的切线斜率应为 $1$。

曲线 $y=\ln x$ 上任一点的导数为
$$
y'=\frac{1}{x}.
$$

令 $\dfrac{1}{x}=1$，得 $x=1$，对应点为 $(1,\ln1)=(1,0)$。因此切线方程为
$$
y-0=1\cdot(x-1),
$$
即
$$
y=x-1.
$$

### 第 2 题

**答案：** $\displaystyle f(x)=\frac{1}{2}(\ln x)^2$

令 $t=e^x$，则 $x=\ln t$，且 $e^{-x}=1/t$。由题设
$$
f'(t)=x e^{-x}=\frac{\ln t}{t}.
$$

于是
$$
f(x)=\int\frac{\ln x}{x}\,dx
=\frac{1}{2}(\ln x)^2+C.
$$

由 $f(1)=0$ 得 $C=0$，所以
$$
f(x)=\frac{1}{2}(\ln x)^2.
$$

### 第 3 题

**答案：** $\displaystyle \frac{3\pi}{2}$

$L$ 为第一象限中正向圆弧，可取参数
$$
x=\sqrt{2}\cos\theta,\qquad y=\sqrt{2}\sin\theta,\qquad 0\le\theta\le\frac{\pi}{2}.
$$

于是
$$
dx=-\sqrt{2}\sin\theta\,d\theta,\qquad
dy=\sqrt{2}\cos\theta\,d\theta.
$$

代入曲线积分：
$$
\begin{aligned}
\int_L x\,dy-2y\,dx
&=\int_0^{\pi/2}\left(2\cos^2\theta+4\sin^2\theta\right)d\theta\\
&=\int_0^{\pi/2}\left(2+2\sin^2\theta\right)d\theta\\
&=\pi+\frac{\pi}{2}
=\frac{3\pi}{2}.
\end{aligned}
$$

### 第 4 题

**答案：** $\displaystyle y=\frac{C_1}{x}+\frac{C_2}{x^2}$

这是欧拉方程。令 $x=e^t$，则
$$
x\frac{dy}{dx}=\frac{dy}{dt},\qquad
x^2\frac{d^2y}{dx^2}=\frac{d^2y}{dt^2}-\frac{dy}{dt}.
$$

原方程化为
$$
\frac{d^2y}{dt^2}+3\frac{dy}{dt}+2y=0.
$$

特征方程为
$$
r^2+3r+2=0,
$$
得 $r=-1,-2$。因此
$$
y=C_1e^{-t}+C_2e^{-2t}
=\frac{C_1}{x}+\frac{C_2}{x^2}.
$$

### 第 5 题

**答案：** $\displaystyle \frac{1}{9}$

由
$$
ABA^*=2BA^*+E
$$
得
$$
(A-2E)BA^*=E.
$$

取行列式：
$$
\det(A-2E)\,\det B\,\det(A^*)=1.
$$

对
$$
A=\begin{pmatrix}2&1&0\\1&2&0\\0&0&1\end{pmatrix},
$$
有
$$
\det A=3,\qquad \det(A^*)=(\det A)^{3-1}=9,
$$
并且
$$
A-2E=\begin{pmatrix}0&1&0\\1&0&0\\0&0&-1\end{pmatrix},
\qquad \det(A-2E)=1.
$$

所以
$$
\det B=\frac{1}{\det(A-2E)\det(A^*)}=\frac{1}{9}.
$$

### 第 6 题

**答案：** $\displaystyle \frac{1}{e}$

若 $X$ 服从参数为 $\lambda$ 的指数分布，则
$$
D(X)=\frac{1}{\lambda^2},
\qquad
\sqrt{D(X)}=\frac{1}{\lambda}.
$$

指数分布的尾概率为 $P\{X>x\}=e^{-\lambda x}$，故
$$
P\{X>\sqrt{D(X)}\}
=P\left\{X>\frac{1}{\lambda}\right\}
=e^{-1}.
$$

### 第 7 题

**答案：** B

当 $x\to0^+$ 时，
$$
\alpha=\int_0^x\cos(t^2)\,dt\sim x.
$$

又因为 $\tan\sqrt{t}\sim\sqrt{t}$，所以
$$
\beta=\int_0^{x^2}\tan\sqrt{t}\,dt
\sim\int_0^{x^2}\sqrt{t}\,dt
=\frac{2}{3}x^3.
$$

同理 $\sin(t^3)\sim t^3$，故
$$
\gamma=\int_0^{\sqrt{x}}\sin(t^3)\,dt
\sim\int_0^{\sqrt{x}}t^3\,dt
=\frac{x^2}{4}.
$$

阶数依次为 $x,x^2,x^3$，所以后者为前者高阶无穷小的顺序是
$$
\alpha,\gamma,\beta.
$$
选 B。

### 第 8 题

**答案：** C

由 $f'(0)>0$ 可知存在 $\delta>0$，当 $0<|x|<\delta$ 时，
$$
\frac{f(x)-f(0)}{x}>0.
$$

若 $0<x<\delta$，则 $x>0$，从而
$$
f(x)-f(0)>0,
$$
即 $f(x)>f(0)$。这正是 C。

条件只给出了 $0$ 点处导数的符号，不能推出整个区间内单调，因此 A、B 不能保证。若 $x<0$，由上式反而得到 $f(x)<f(0)$，所以 D 不对。

### 第 9 题

**答案：** B

若存在非零常数 $\lambda$ 使
$$
\lim_{n\to\infty}n a_n=\lambda,
$$
则
$$
a_n\sim\frac{\lambda}{n}.
$$

因为 $\sum\dfrac{1}{n}$ 发散，所以正项级数 $\sum a_n$ 也发散。故 B 正确。

A 不能保证，例如 $a_n=1/(n\ln n)$ 从 $n\ge2$ 起有 $n a_n\to0$，但级数发散。C 也不成立，例如 $a_n=1/n^2$ 时级数收敛而 $n^2a_n=1$。D 显然不能由发散推出该极限存在。

### 第 10 题

**答案：** B

积分区域为
$$
1\le y\le t,\qquad y\le x\le t.
$$

交换积分次序，得
$$
F(t)=\int_1^t\int_1^x f(x)\,dy\,dx
=\int_1^t (x-1)f(x)\,dx.
$$

因此
$$
F'(t)=(t-1)f(t),
$$
从而
$$
F'(2)=f(2).
$$
选 B。

### 第 11 题

**答案：** D

右乘矩阵表示对列作初等变换。

先交换 $A$ 的第 $1$、第 $2$ 列，对应右乘
$$
P=\begin{pmatrix}
0&1&0\\
1&0&0\\
0&0&1
\end{pmatrix}.
$$

此时 $B=AP$。再把 $B$ 的第 $2$ 列加到第 $3$ 列，对应右乘
$$
R=\begin{pmatrix}
1&0&0\\
0&1&1\\
0&0&1
\end{pmatrix}.
$$

于是
$$
C=APR=AQ,
$$
其中
$$
Q=PR=
\begin{pmatrix}
0&1&1\\
1&0&0\\
0&0&1
\end{pmatrix}.
$$
选 D。

### 第 12 题

**答案：** A

设 $A$ 为 $m\times n$ 矩阵，$B$ 为 $n\times s$ 矩阵。由 $AB=O$ 和秩不等式得
$$
r(A)+r(B)\le n.
$$

因为 $B$ 为非零矩阵，$r(B)>0$，所以 $r(A)<n$，即 $A$ 的列向量组线性相关。

又因为 $A$ 为非零矩阵，$r(A)>0$，所以 $r(B)<n$。矩阵 $B$ 有 $n$ 个行向量，而其秩小于 $n$，故 $B$ 的行向量组线性相关。

因此必然成立的是 A。

### 第 13 题

**答案：** C

标准正态分布关于 $0$ 对称。若
$$
P\{|X|<x\}=\alpha,
$$
则两侧尾概率之和为 $1-\alpha$，每一侧尾概率为
$$
\frac{1-\alpha}{2}.
$$

题中 $u_\alpha$ 的定义为
$$
P\{X>u_\alpha\}=\alpha,
$$
所以
$$
x=u_{\frac{1-\alpha}{2}}.
$$
选 C。

### 第 14 题

**答案：** A

由
$$
Y=\frac{1}{n}\sum_{i=1}^n X_i
$$
及独立同分布可得
$$
\operatorname{Cov}(X_1,Y)
=\frac{1}{n}\sum_{i=1}^n\operatorname{Cov}(X_1,X_i)
=\frac{1}{n}D(X_1)
=\frac{\sigma^2}{n}.
$$

故 A 正确。顺便核对方差：
$$
D(Y)=\frac{\sigma^2}{n},
\qquad
\operatorname{Cov}(X_1,Y)=\frac{\sigma^2}{n}.
$$

于是
$$
D(X_1+Y)
=\sigma^2+\frac{\sigma^2}{n}+2\frac{\sigma^2}{n}
=\frac{n+3}{n}\sigma^2,
$$
$$
D(X_1-Y)
=\sigma^2+\frac{\sigma^2}{n}-2\frac{\sigma^2}{n}
=\frac{n-1}{n}\sigma^2.
$$
所以 C、D 的数值也不对。

### 第 15 题

**答案：** 结论成立。

令
$$
\varphi(x)=\ln^2 x.
$$

由拉格朗日中值定理，存在 $\xi\in(a,b)$，使得
$$
\ln^2 b-\ln^2 a=\varphi'(\xi)(b-a)
=\frac{2\ln\xi}{\xi}(b-a).
$$

因为 $e<a<\xi<b<e^2$，且函数
$$
g(x)=\frac{\ln x}{x}
$$
在 $(e,+\infty)$ 上递减，所以
$$
\frac{\ln\xi}{\xi}>\frac{\ln e^2}{e^2}=\frac{2}{e^2}.
$$

于是
$$
\ln^2 b-\ln^2 a
=\frac{2\ln\xi}{\xi}(b-a)
>\frac{4}{e^2}(b-a).
$$
命题得证。

### 第 16 题

**答案：** $1.05\,\mathrm{km}$

设飞机着陆后水平速度为 $v(t)$。阻力与速度成正比且方向相反，因此
$$
m\frac{dv}{dt}=-kv.
$$

解得
$$
v(t)=v_0e^{-kt/m}.
$$

飞机从着陆到停止的最大滑行距离为
$$
s=\int_0^{+\infty}v(t)\,dt
=\int_0^{+\infty}v_0e^{-kt/m}\,dt
=\frac{m v_0}{k}.
$$

代入 $m=9000$，$v_0=700\,\mathrm{km/h}$，$k=6.0\times10^6$，得
$$
s=\frac{9000\times700}{6.0\times10^6}
=1.05\,\mathrm{km}.
$$

### 第 17 题

**答案：** $-\pi$

曲面为
$$
z=1-x^2-y^2,\qquad z\ge0,
$$
其在 $xy$ 平面的投影为
$$
D:\ x^2+y^2\le1.
$$

曲面取上侧时，对第二类曲面积分可化为
$$
I=\iint_D\left[-Pz_x-Qz_y+R\right]\,dx\,dy,
$$
其中
$$
P=2x^3,\qquad Q=2y^3,\qquad R=3(z^2-1).
$$

由 $z_x=-2x,\ z_y=-2y$，得
$$
\begin{aligned}
I
&=\iint_D\left[4x^4+4y^4+3(1-x^2-y^2)^2-3\right]dx\,dy.
\end{aligned}
$$

改用极坐标 $x=r\cos\theta,\ y=r\sin\theta$，则
$$
\begin{aligned}
I
&=\int_0^{2\pi}\int_0^1
\left[4r^4(\cos^4\theta+\sin^4\theta)+3(1-r^2)^2-3\right]r\,dr\,d\theta\\
&=-\pi.
\end{aligned}
$$

所以曲面积分的值为
$$
I=-\pi.
$$

### 第 18 题

**答案：** 方程有唯一正实根；当 $\alpha>1$ 时，$\displaystyle\sum_{n=1}^{\infty}x_n^\alpha$ 收敛。

令
$$
f_n(x)=x^n+nx-1.
$$

有
$$
f_n(0)=-1,\qquad f_n(1)=n>0,
$$
因此在 $(0,1)$ 内至少有一个正根。

又
$$
f_n'(x)=n x^{n-1}+n>0\qquad(x>0),
$$
故 $f_n(x)$ 在 $(0,+\infty)$ 上严格递增，所以正根唯一，记为 $x_n$。

由方程
$$
x_n^n+n x_n-1=0
$$
得
$$
x_n=\frac{1-x_n^n}{n}<\frac{1}{n}.
$$

当 $\alpha>1$ 时，
$$
0<x_n^\alpha<\frac{1}{n^\alpha}.
$$
而 $\sum_{n=1}^{\infty}\dfrac{1}{n^\alpha}$ 收敛，所以由比较判别法，
$$
\sum_{n=1}^{\infty}x_n^\alpha
$$
收敛。

### 第 19 题

**答案：** 极小值点为 $(9,3)$，极小值为 $3$；极大值点为 $(-9,-3)$，极大值为 $-3$。

设
$$
F(x,y,z)=x^2-6xy+10y^2-2yz-z^2+18.
$$

由 $F(x,y,z(x,y))=0$ 对 $x,y$ 求偏导：
$$
2x-6y-2y z_x-2z z_x=0,
$$
$$
-6x+20y-2z-2y z_y-2z z_y=0.
$$

极值点处 $z_x=z_y=0$，因此
$$
x-3y=0,\qquad -3x+10y-z=0.
$$
由此得
$$
x=3y,\qquad z=y.
$$
代入原方程：
$$
-2y^2+18=0,
$$
故
$$
(x,y,z)=(9,3,3)\quad\text{或}\quad(-9,-3,-3).
$$

在极值点处继续求二阶偏导。记
$$
A=z_{xx},\qquad B=z_{xy},\qquad C=z_{yy}.
$$
在 $(9,3,3)$ 处，
$$
A=\frac{1}{6},\qquad B=-\frac{1}{2},\qquad C=\frac{5}{3},
$$
故
$$
AC-B^2=\frac{1}{36}>0,\qquad A>0,
$$
所以 $(9,3)$ 为极小值点，极小值为 $z(9,3)=3$。

在 $(-9,-3,-3)$ 处，
$$
A=-\frac{1}{6},\qquad B=\frac{1}{2},\qquad C=-\frac{5}{3},
$$
仍有
$$
AC-B^2=\frac{1}{36}>0,\qquad A<0,
$$
所以 $(-9,-3)$ 为极大值点，极大值为 $z(-9,-3)=-3$。

### 第 20 题

**答案：** 当 $a=0$ 或 $a=-\dfrac{n(n+1)}{2}$ 时有非零解。若 $a=0$，通解为 $x=k_1\eta_1+\cdots+k_{n-1}\eta_{n-1}$，其中 $\eta_i=(-1,0,\ldots,0,1,0,\ldots,0)^T$，第 $i+1$ 个分量为 $1$；若 $a=-\dfrac{n(n+1)}{2}$，通解为 $x=k(1,2,\ldots,n)^T$。

系数矩阵可写为
$$
A=aE+Q,
$$
其中
$$
Q=\begin{pmatrix}
1&1&\cdots&1\\
2&2&\cdots&2\\
\vdots&\vdots&&\vdots\\
n&n&\cdots&n
\end{pmatrix}.
$$

矩阵 $Q$ 的特征值为
$$
0,\ldots,0,\frac{n(n+1)}{2}.
$$
因此
$$
\det A=a^{\,n-1}\left(a+\frac{n(n+1)}{2}\right).
$$

齐次线性方程组有非零解的充要条件为 $\det A=0$，故
$$
a=0
\quad\text{或}\quad
a=-\frac{n(n+1)}{2}.
$$

当 $a=0$ 时，方程组化为
$$
x_1+x_2+\cdots+x_n=0.
$$
取 $x_2,\ldots,x_n$ 为自由未知量，基础解系可取
$$
\eta_1=(-1,1,0,\ldots,0)^T,\quad
\eta_2=(-1,0,1,\ldots,0)^T,\quad\ldots,\quad
\eta_{n-1}=(-1,0,\ldots,0,1)^T.
$$
通解为
$$
x=k_1\eta_1+\cdots+k_{n-1}\eta_{n-1}.
$$

当
$$
a=-\frac{n(n+1)}{2}
$$
时，同解方程组可化为
$$
-2x_1+x_2=0,\quad -3x_1+x_3=0,\quad\ldots,\quad -n x_1+x_n=0.
$$
所以基础解系可取
$$
\eta=(1,2,\ldots,n)^T,
$$
通解为
$$
x=k\eta=k(1,2,\ldots,n)^T.
$$

### 第 21 题

**答案：** $a=-2$ 时，$A$ 可相似对角化；$a=-\dfrac{2}{3}$ 时，$A$ 不可相似对角化。

计算特征多项式：
$$
\begin{aligned}
\det(\lambda E-A)
&=(\lambda-2)\left(\lambda^2-8\lambda+18+3a\right).
\end{aligned}
$$

题设特征方程有一个二重根，分两种情况。

第一种，$\lambda=2$ 为二重根。令
$$
2^2-8\cdot2+18+3a=0,
$$
得
$$
a=-2.
$$
此时
$$
\det(\lambda E-A)=(\lambda-2)^2(\lambda-6),
$$
特征值为 $2,2,6$。又
$$
r(2E-A)=1,
$$
故 $\lambda=2$ 对应的线性无关特征向量个数为
$$
3-r(2E-A)=2,
$$
等于其代数重数，所以 $A$ 可相似对角化。

第二种，$\lambda=2$ 不是二重根，则
$$
\lambda^2-8\lambda+18+3a
$$
为完全平方。由判别式为零，
$$
64-4(18+3a)=0,
$$
得
$$
a=-\frac{2}{3}.
$$
此时
$$
\det(\lambda E-A)=(\lambda-2)(\lambda-4)^2,
$$
特征值为 $2,4,4$。又
$$
r(4E-A)=2,
$$
故 $\lambda=4$ 对应的线性无关特征向量个数为
$$
3-r(4E-A)=1,
$$
小于其代数重数 $2$，所以 $A$ 不可相似对角化。

### 第 22 题

**答案：** $(X,Y)$ 的分布为 $P(0,0)=\dfrac{2}{3}$，$P(0,1)=\dfrac{1}{12}$，$P(1,0)=\dfrac{1}{6}$，$P(1,1)=\dfrac{1}{12}$；$\displaystyle \rho_{XY}=\frac{\sqrt{15}}{15}$。

由
$$
P(A)=\frac{1}{4},\qquad P(B\mid A)=\frac{1}{3}
$$
得
$$
P(AB)=P(A)P(B\mid A)=\frac{1}{12}.
$$

又由 $P(A\mid B)=\dfrac{1}{2}$，得
$$
P(B)=\frac{P(AB)}{P(A\mid B)}
=\frac{1/12}{1/2}
=\frac{1}{6}.
$$

于是
$$
P\{X=1,Y=1\}=P(AB)=\frac{1}{12},
$$
$$
P\{X=1,Y=0\}=P(A)-P(AB)=\frac{1}{4}-\frac{1}{12}=\frac{1}{6},
$$
$$
P\{X=0,Y=1\}=P(B)-P(AB)=\frac{1}{6}-\frac{1}{12}=\frac{1}{12},
$$
$$
P\{X=0,Y=0\}=1-P(A)-P(B)+P(AB)=\frac{2}{3}.
$$

因此联合分布为
$$
\begin{array}{c|cc}
X\backslash Y&0&1\\ \hline
0&\dfrac{2}{3}&\dfrac{1}{12}\\
1&\dfrac{1}{6}&\dfrac{1}{12}
\end{array}
$$

边缘分布给出
$$
EX=\frac{1}{4},\qquad EY=\frac{1}{6},
$$
$$
DX=\frac{1}{4}\cdot\frac{3}{4}=\frac{3}{16},\qquad
DY=\frac{1}{6}\cdot\frac{5}{6}=\frac{5}{36}.
$$

又
$$
E(XY)=P\{X=1,Y=1\}=\frac{1}{12}.
$$
所以
$$
\operatorname{Cov}(X,Y)
=E(XY)-EX\,EY
=\frac{1}{12}-\frac{1}{24}
=\frac{1}{24}.
$$

相关系数为
$$
\rho_{XY}
=\frac{\operatorname{Cov}(X,Y)}{\sqrt{DX}\sqrt{DY}}
=\frac{1/24}{\sqrt{3/16}\sqrt{5/36}}
=\frac{1}{\sqrt{15}}
=\frac{\sqrt{15}}{15}.
$$

### 第 23 题

**答案：** 矩估计量 $\displaystyle \hat\beta_M=\frac{\bar X}{\bar X-1}$；最大似然估计量 $\displaystyle \hat\beta=\frac{n}{\sum_{i=1}^n\ln X_i}$。

由分布函数
$$
F(x;\beta)=1-\frac{1}{x^\beta}\qquad(x>1)
$$
可得密度函数
$$
f(x;\beta)=
\begin{cases}
\dfrac{\beta}{x^{\beta+1}},&x>1,\\
0,&x\le1.
\end{cases}
$$

首先求矩估计。因 $\beta>1$，
$$
EX=\int_1^{+\infty}x\frac{\beta}{x^{\beta+1}}\,dx
=\frac{\beta}{\beta-1}.
$$
令 $EX=\bar X$，得到
$$
\frac{\beta}{\beta-1}=\bar X,
$$
解得矩估计量
$$
\hat\beta_M=\frac{\bar X}{\bar X-1},
\qquad
\bar X=\frac{1}{n}\sum_{i=1}^n X_i.
$$

再求最大似然估计。样本观测值均大于 $1$ 时，似然函数为
$$
L(\beta)=\prod_{i=1}^n \frac{\beta}{x_i^{\beta+1}}
=\frac{\beta^n}{(x_1x_2\cdots x_n)^{\beta+1}}.
$$

取对数：
$$
\ln L(\beta)
=n\ln\beta-(\beta+1)\sum_{i=1}^n\ln x_i.
$$

求导并令其为零：
$$
\frac{d}{d\beta}\ln L(\beta)
=\frac{n}{\beta}-\sum_{i=1}^n\ln x_i=0.
$$

于是最大似然估计量为
$$
\hat\beta=\frac{n}{\sum_{i=1}^n\ln X_i}.
$$
