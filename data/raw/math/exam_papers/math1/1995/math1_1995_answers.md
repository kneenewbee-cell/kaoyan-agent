# Math 1 1995 Answers

资料类型：考研数学一答案解析
年份：1995
科目：数学一
范围：试卷 I
来源：D:\百度网盘\高数资料\【02】1987-2022年数学一真题详解答案（PDF）\1995考研数学一真题解析.pdf
校对状态：已按题干和答案页图像重新清洗，去除 OCR 碎行、串题内容和非本题页脚

## 答案速查

| 题号 | 题型 | 答案 |
|---|---|---|
| 1 | 填空题 | $e^6$ |
| 2 | 填空题 | $\displaystyle \int_{x^2}^{0}\cos(t^2)\,dt-2x^2\cos(x^4)$ |
| 3 | 填空题 | $4$ |
| 4 | 填空题 | $\sqrt3$ |
| 5 | 填空题 | $\begin{pmatrix}3&0&0\\0&2&0\\0&0&1\end{pmatrix}$ |
| 6 | single_choice | C |
| 7 | single_choice | B |
| 8 | single_choice | A |
| 9 | single_choice | C |
| 10 | single_choice | C |
| 11 | 解答题 | $\displaystyle \frac{du}{dx}=f_1+f_2\cos x-\frac{f_3}{\varphi_3}\left(2x\varphi_1+e^y\cos x\,\varphi_2\right)$ |
| 12 | 解答题 | $\dfrac{A^2}{2}$ |
| 13 | 解答题 | $\dfrac{32\sqrt2}{9}$ |
| 14 | 解答题 | $\displaystyle f(x)=-\frac{8}{\pi^2}\sum_{n=1}^{\infty}\frac{\cos\frac{(2n-1)\pi x}{2}}{(2n-1)^2}\quad(0\le x\le2)$ |
| 15 | 解答题 | $y=\sqrt{3x-x^2}\quad(0<x<3)$ |
| 16 | 解答题 | $Q(x,y)=x^2+2y-1$ |
| 17 | 解答题 | 见解析 |
| 18 | 解答题 | $\begin{pmatrix}1&0&0\\0&0&-1\\0&-1&0\end{pmatrix}$ |
| 19 | 解答题 | $0$ |
| 20 | 填空题 | $18.4$ |
| 21 | 填空题 | $\dfrac{5}{7}$ |
| 22 | 解答题 | $f_Y(y)=\begin{cases}\dfrac{1}{y^2},&y>1,\\0,&y\le1.\end{cases}$ |

## 详细解析

### 第 1 题

- 答案：$e^6$

这是 $1^\infty$ 型极限。取对数的指数部分：
$$
\frac{2}{\sin x}\ln(1+3x).
$$

当 $x\to0$ 时，
$$
\ln(1+3x)\sim 3x,\qquad \sin x\sim x,
$$
所以
$$
\lim_{x\to0}\frac{2\ln(1+3x)}{\sin x}=6.
$$

因此
$$
\lim_{x\to0}(1+3x)^{2/\sin x}=e^6.
$$


### 第 2 题

- 答案：$\displaystyle \int_{x^2}^{0}\cos(t^2)\,dt-2x^2\cos(x^4)$

把原式写成
$$
x\int_{x^2}^{0}\cos(t^2)\,dt.
$$

由乘积求导和变上限积分求导公式，
$$
\frac{d}{dx}\left[x\int_{x^2}^{0}\cos(t^2)\,dt\right]
=\int_{x^2}^{0}\cos(t^2)\,dt
x\cdot\left[-\cos\bigl((x^2)^2\bigr)\cdot 2x\right].
$$

故结果为
$$
\int_{x^2}^{0}\cos(t^2)\,dt-2x^2\cos(x^4).
$$


### 第 3 题

- 答案：$4$

利用混合积的线性性：
$$
[(\boldsymbol a+\boldsymbol b)\times(\boldsymbol b+\boldsymbol c)]
\cdot(\boldsymbol c+\boldsymbol a)
$$
$$
=
(\boldsymbol a\times\boldsymbol b)\cdot\boldsymbol c
+(\boldsymbol b\times\boldsymbol c)\cdot\boldsymbol a.
$$

而混合积循环置换不变，
$$
(\boldsymbol b\times\boldsymbol c)\cdot\boldsymbol a
=(\boldsymbol a\times\boldsymbol b)\cdot\boldsymbol c=2.
$$

因此原式为
$$
2+2=4.
$$


### 第 4 题

- 答案：$\sqrt3$

设
$$
u_n=\frac{n}{2^n+(-3)^n}x^{2n-1}.
$$

用比值判别法：
$$
\left|\frac{u_{n+1}}{u_n}\right|
=|x|^2\frac{n+1}{n}
\left|\frac{2^n+(-3)^n}{2^{n+1}+(-3)^{n+1}}\right|
\longrightarrow \frac{x^2}{3}.
$$

级数收敛需
$$
\frac{x^2}{3}<1,
$$
即
$$
|x|<\sqrt3.
$$

故收敛半径为
$$
R=\sqrt3.
$$


### 第 5 题

- 答案：$\begin{pmatrix}3&0&0\\0&2&0\\0&0&1\end{pmatrix}$

由
$$
A^{-1}BA=6A+BA
$$
两边右乘 $A^{-1}$，得
$$
A^{-1}B=6E+B.
$$

因此
$$
(A^{-1}-E)B=6E.
$$

又
$$
A^{-1}=\begin{pmatrix}3&0&0\\0&4&0\\0&0&7\end{pmatrix},
$$
所以
$$
B=6(A^{-1}-E)^{-1}
=6\begin{pmatrix}2&0&0\\0&3&0\\0&0&6\end{pmatrix}^{-1}
=\begin{pmatrix}3&0&0\\0&2&0\\0&0&1\end{pmatrix}.
$$


### 第 6 题

- 答案：C

直线 $L$ 是两个平面的交线，其方向向量为两个法向量
$$
\boldsymbol n_1=(1,3,2),\qquad \boldsymbol n_2=(2,-1,-10)
$$
的叉积：
$$
\boldsymbol l=\boldsymbol n_1\times\boldsymbol n_2=(-28,14,-7)
=-7(4,-2,1).
$$

平面 $\pi:4x-2y+z-2=0$ 的法向量为
$$
\boldsymbol n=(4,-2,1).
$$

故 $\boldsymbol l\parallel \boldsymbol n$，直线 $L$ 垂直于平面 $\pi$。选 C。


### 第 7 题

- 答案：B

由 $f''(x)>0$ 知 $f'(x)$ 在 $[0,1]$ 上严格单调递增，因此
$$
f'(1)>f'(0).
$$

由微分中值定理，存在 $\xi\in(0,1)$，使
$$
f(1)-f(0)=f'(\xi).
$$

又 $f'$ 严格递增，所以
$$
f'(1)>f'(\xi)>f'(0).
$$

即
$$
f'(1)>f(1)-f(0)>f'(0).
$$

选 B。


### 第 8 题

- 答案：A

因为 $f$ 可导，所以 $f(x)$ 本身在 $0$ 处可导。问题只需考察
$$
f(x)|\sin x|
$$
在 $0$ 处是否可导。

若 $f(0)=0$，则
$$
\lim_{x\to0}\frac{f(x)|\sin x|-f(0)|\sin0|}{x}
=\lim_{x\to0}f(x)\frac{|\sin x|}{x}=0,
$$
故 $F$ 在 $0$ 处可导。

反过来，若 $F$ 在 $0$ 处可导，则 $f(x)|\sin x|$ 在 $0$ 处可导。其左右导数分别为
$$
\lim_{x\to0^-}f(x)\frac{|\sin x|}{x}=-f(0),\qquad
\lim_{x\to0^+}f(x)\frac{|\sin x|}{x}=f(0).
$$

左右导数相等推出 $f(0)=0$。所以这是充分必要条件，选 A。


### 第 9 题

- 答案：C

有
$$
u_n=(-1)^n\ln\left(1+\frac{1}{\sqrt n}\right).
$$

其中
$$
\ln\left(1+\frac{1}{\sqrt n}\right)
$$
单调趋于 $0$，所以 $\sum u_n$ 由莱布尼茨判别法收敛。

而
$$
u_n^2=\ln^2\left(1+\frac{1}{\sqrt n}\right)
\sim \frac{1}{n}.
$$

由于 $\sum 1/n$ 发散，故 $\sum u_n^2$ 发散。选 C。


### 第 10 题

- 答案：C

矩阵 $P_1$ 左乘矩阵时交换第一、二行；矩阵 $P_2$ 左乘矩阵时把第一行加到第三行。

从 $A$ 变到 $B$ 的过程是：先把第一行加到第三行，再交换第一、二行。因此
$$
B=P_1P_2A.
$$

选 C。


### 第 11 题

- 答案：$\displaystyle \frac{du}{dx}=f_1+f_2\cos x-\frac{f_3}{\varphi_3}\left(2x\varphi_1+e^y\cos x\,\varphi_2\right)$

由
$$
\varphi(x^2,e^y,z)=0,\qquad y=\sin x
$$
可把 $z$ 看成 $x$ 的隐函数。

对 $x$ 求导：
$$
2x\varphi_1+e^y\cos x\,\varphi_2+\varphi_3\frac{dz}{dx}=0.
$$

由于 $\varphi_3\ne0$，
$$
\frac{dz}{dx}
=-\frac{2x\varphi_1+e^y\cos x\,\varphi_2}{\varphi_3}.
$$

又
$$
u=f(x,y,z),\qquad y=\sin x,
$$
故
$$
\frac{du}{dx}
=f_1+f_2\cos x+f_3\frac{dz}{dx}.
$$

代入上式得
$$
\frac{du}{dx}
=f_1+f_2\cos x-\frac{f_3}{\varphi_3}
\left(2x\varphi_1+e^y\cos x\,\varphi_2\right).
$$

其中 $f_i$ 在 $(x,y,z)$ 处取值，$\varphi_i$ 在 $(x^2,e^y,z)$ 处取值，且 $y=\sin x$。


### 第 12 题

- 答案：$\dfrac{A^2}{2}$

记
$$
I=\int_0^1 dx\int_x^1 f(x)f(y)\,dy.
$$

积分区域为
$$
D=\{(x,y):0\le x\le y\le1\}.
$$

由于 $f(x)f(y)$ 关于 $x,y$ 对称，正方形 $[0,1]\times[0,1]$ 被直线 $y=x$ 分成两个对称三角形区域，故
$$
2I=\int_0^1\int_0^1 f(x)f(y)\,dy\,dx.
$$

于是
$$
2I=\left(\int_0^1 f(x)\,dx\right)
\left(\int_0^1 f(y)\,dy\right)=A^2.
$$

所以
$$
I=\frac{A^2}{2}.
$$


### 第 13 题

- 答案：$\dfrac{32\sqrt2}{9}$

锥面
$$
z=\sqrt{x^2+y^2}
$$
上有
$$
\sqrt{1+z_x^2+z_y^2}=\sqrt2.
$$

故曲面积分化为投影区域 $D$ 上的二重积分：
$$
\iint_\Sigma z\,dS
=\iint_D \sqrt{x^2+y^2}\,\sqrt2\,dx\,dy.
$$

投影区域由
$$
x^2+y^2\le2x
$$
给出，即
$$
(x-1)^2+y^2\le1.
$$

用极坐标 $x=r\cos\theta,\ y=r\sin\theta$，区域为
$$
-\frac{\pi}{2}\le\theta\le\frac{\pi}{2},\qquad 0\le r\le2\cos\theta.
$$

于是
$$
\iint_\Sigma z\,dS
=\sqrt2\int_{-\pi/2}^{\pi/2}\int_0^{2\cos\theta}r^2\,dr\,d\theta
=\frac{\sqrt2}{3}\int_{-\pi/2}^{\pi/2}8\cos^3\theta\,d\theta.
$$

又
$$
\int_{-\pi/2}^{\pi/2}\cos^3\theta\,d\theta=\frac{4}{3},
$$
故
$$
\iint_\Sigma z\,dS=\frac{32\sqrt2}{9}.
$$


### 第 14 题

- 答案：$\displaystyle f(x)=-\frac{8}{\pi^2}\sum_{n=1}^{\infty}\frac{\cos\frac{(2n-1)\pi x}{2}}{(2n-1)^2}\quad(0\le x\le2)$

周期为 $4$ 的余弦级数对应在 $[0,2]$ 上作偶延拓，半区间长度为 $l=2$。

余弦系数为
$$
a_n=\frac{2}{l}\int_0^l f(x)\cos\frac{n\pi x}{l}\,dx
=\int_0^2(x-1)\cos\frac{n\pi x}{2}\,dx.
$$

分部积分得
$$
a_n=\frac{4}{n^2\pi^2}\bigl((-1)^n-1\bigr).
$$

所以当 $n=2k$ 时 $a_n=0$；当 $n=2k-1$ 时
$$
a_{2k-1}=-\frac{8}{(2k-1)^2\pi^2}.
$$

又
$$
a_0=\int_0^2(x-1)\,dx=0.
$$

因此
$$
f(x)=-\frac{8}{\pi^2}\sum_{k=1}^{\infty}
\frac{\cos\frac{(2k-1)\pi x}{2}}{(2k-1)^2},
\qquad 0\le x\le2.
$$


### 第 15 题

- 答案：$y=\sqrt{3x-x^2}\quad(0<x<3)$

设曲线上点 $M$ 的坐标为 $(x,y)$。该点处切线为
$$
Y-y=y'(X-x).
$$

令 $X=0$，得切线与 $y$ 轴交点
$$
A=(0,y-xy').
$$

由 $|\overline{MA}|=|\overline{OA}|$，
$$
\sqrt{x^2+(xy')^2}=|y-xy'|.
$$

两边平方并化简：
$$
2xyy'-y^2=-x^2,
$$
即
$$
(y^2)'-\frac{1}{x} y^2=-x.
$$

令 $z=y^2$，得
$$
z'-\frac{1}{x}z=-x.
$$

解得
$$
z=x(C-x),
$$
即
$$
y^2=Cx-x^2.
$$

曲线过 $\left(\frac{3}{2},\frac{3}{2}\right)$，代入得 $C=3$。第一象限内 $y>0$，故
$$
y=\sqrt{3x-x^2},\qquad 0<x<3.
$$


### 第 16 题

- 答案：$Q(x,y)=x^2+2y-1$

曲线积分与路径无关，且 $P=2xy$、$Q$ 有连续偏导数，所以
$$
\frac{\partial Q}{\partial x}=\frac{\partial P}{\partial y}=2x.
$$

对 $x$ 积分得
$$
Q(x,y)=x^2+\varphi(y).
$$

此时
$$
2xy\,dx+Q(x,y)\,dy
=2xy\,dx+\bigl(x^2+\varphi(y)\bigr)\,dy
=d\left(x^2y+\int_0^y\varphi(s)\,ds\right).
$$

题设给出对任意 $t$，
$$
\left[x^2y+\int_0^y\varphi(s)\,ds\right]_{(0,0)}^{(t,1)}
=
\left[x^2y+\int_0^y\varphi(s)\,ds\right]_{(0,0)}^{(1,t)}.
$$

故
$$
t^2+\int_0^1\varphi(s)\,ds
=t+\int_0^t\varphi(s)\,ds.
$$

对 $t$ 求导：
$$
2t=1+\varphi(t),
$$
所以
$$
\varphi(t)=2t-1.
$$

因此
$$
Q(x,y)=x^2+2y-1.
$$


### 第 17 题

- 答案：见解析

先证第一问。若存在 $c\in(a,b)$ 使 $g(c)=0$，则由
$$
g(a)=g(c)=g(b)=0
$$
和罗尔定理，分别存在
$$
\xi_1\in(a,c),\qquad \xi_2\in(c,b),
$$
使
$$
g'(\xi_1)=g'(\xi_2)=0.
$$

再对 $g'$ 在 $[\xi_1,\xi_2]$ 上用罗尔定理，存在 $\eta\in(\xi_1,\xi_2)$，使
$$
g''(\eta)=0,
$$
这与 $g''(x)\ne0$ 矛盾。故 $g(x)$ 在 $(a,b)$ 内不为零。

再证第二问。令
$$
\Phi(x)=f(x)g'(x)-f'(x)g(x).
$$

由端点条件 $f(a)=f(b)=g(a)=g(b)=0$，得
$$
\Phi(a)=\Phi(b)=0.
$$

由罗尔定理，存在 $\xi\in(a,b)$，使
$$
\Phi'(\xi)=0.
$$

而
$$
\Phi'(x)=f(x)g''(x)-f''(x)g(x).
$$

所以
$$
f(\xi)g''(\xi)-f''(\xi)g(\xi)=0.
$$

由第一问 $g(\xi)\ne0$，且题设 $g''(\xi)\ne0$，故
$$
\frac{f(\xi)}{g(\xi)}=\frac{f''(\xi)}{g''(\xi)}.
$$


### 第 18 题

- 答案：$\begin{pmatrix}1&0&0\\0&0&-1\\0&-1&0\end{pmatrix}$

由于 $A$ 为实对称矩阵，不同特征值对应的特征向量正交。

对应 $\lambda_1=-1$ 的单位特征向量可取
$$
u=\frac{1}{\sqrt2}(0,1,1)^T.
$$

而 $\lambda_2=\lambda_3=1$ 对应的是与 $u$ 正交的二维子空间。因此 $A$ 在 $u$ 方向上取相反数，在正交补上保持不变，即
$$
A=I-2uu^T.
$$

计算
$$
uu^T=\frac{1}{2}
\begin{pmatrix}
0&0&0\\
0&1&1\\
0&1&1
\end{pmatrix}.
$$

故
$$
A=
\begin{pmatrix}
1&0&0\\
0&0&-1\\
0&-1&0
\end{pmatrix}.
$$


### 第 19 题

- 答案：$0$

由
$$
AA^T=E
$$
知 $A$ 为正交矩阵，因此
$$
\det(A)^2=1.
$$

又题设 $\det A<0$，所以
$$
\det A=-1.
$$

利用 $AA^T=E$，
$$
\det(A+E)=\det(A+AA^T)=\det\!\bigl(A(E+A^T)\bigr)
=\det A\,\det(E+A^T).
$$

而
$$
\det(E+A^T)=\det(E+A)=\det(A+E).
$$

所以
$$
\det(A+E)=-\det(A+E),
$$
从而
$$
\det(A+E)=0.
$$


### 第 20 题

- 答案：$18.4$

由题意
$$
X\sim B(10,0.4).
$$

因此
$$
E(X)=np=10\cdot0.4=4,
$$
$$
D(X)=np(1-p)=10\cdot0.4\cdot0.6=2.4.
$$

由
$$
D(X)=E(X^2)-[E(X)]^2
$$
得
$$
E(X^2)=D(X)+[E(X)]^2=2.4+16=18.4.
$$


### 第 21 题

- 答案：$\dfrac{5}{7}$

事件
$$
\{\max(X,Y)\ge0\}
$$
等价于
$$
\{X\ge0\}\cup\{Y\ge0\}.
$$

由加法公式，
$$
P\{\max(X,Y)\ge0\}
=P\{X\ge0\}+P\{Y\ge0\}-P\{X\ge0,Y\ge0\}.
$$

代入题给数据：
$$
P\{\max(X,Y)\ge0\}
=\frac{4}{7}+\frac{4}{7}-\frac{3}{7}
=\frac{5}{7}.
$$


### 第 22 题

- 答案：$f_Y(y)=\begin{cases}\dfrac{1}{y^2},&y>1,\\0,&y\le1.\end{cases}$

因为
$$
Y=e^X,\qquad X\ge0,
$$
所以
$$
Y\ge1.
$$

当 $y\le1$ 时，
$$
F_Y(y)=0.
$$

当 $y>1$ 时，
$$
F_Y(y)=P(Y\le y)=P(e^X\le y)=P(X\le\ln y)
=\int_0^{\ln y}e^{-x}\,dx.
$$

计算得
$$
F_Y(y)=1-\frac{1}{y},\qquad y>1.
$$

对 $y$ 求导，
$$
f_Y(y)=F_Y'(y)=\frac{1}{y^2},\qquad y>1.
$$

故
$$
f_Y(y)=
\begin{cases}
\dfrac{1}{y^2},&y>1,\\
0,&y\le1.
\end{cases}
$$
