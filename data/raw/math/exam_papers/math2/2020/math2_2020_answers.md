# 2020 年数学二答案解析

资料类型：考研数学二答案解析
年份：2020
科目：数学二
整理状态：以答案解析 PDF 页图为主，辅以人工验算补全文字化答案。

## 答案速查

| 题号 | 题型 | 答案 |
|---|---|---|
| 1 | 选择题 | D |
| 2 | 选择题 | C |
| 3 | 选择题 | A |
| 4 | 选择题 | A |
| 5 | 选择题 | B |
| 6 | 选择题 | B |
| 7 | 选择题 | C |
| 8 | 选择题 | D |
| 9 | 填空题 | $-\sqrt{2}$ |
| 10 | 填空题 | $\dfrac{2}{9}(2\sqrt2-1)$ |
| 11 | 填空题 | $(\pi-1)\,dx-dy$ |
| 12 | 填空题 | $\dfrac13\rho ga^3$ |
| 13 | 填空题 | $1$ |
| 14 | 填空题 | $a^2(a-2)(a+2)$ |
| 15 | 解答题 | $y=\dfrac1e x+\dfrac{1}{2e}$ |
| 16 | 解答题 | $g'(x)=\dfrac{x f(x)-\int_0^x f(t)\,dt}{x^2}\ (x\ne 0),\quad g'(0)=\dfrac12$ |
| 17 | 解答题 | 极小值为 $-\dfrac{1}{216}$（在 $\left(\dfrac16,\dfrac1{12}\right)$ 处），无极大值 |
| 18 | 解答题 | $f(x)=\dfrac{x}{\sqrt{1+x^2}}$，旋转体体积为 $\dfrac{\pi^2}{6}$ |
| 19 | 解答题 | $\dfrac34\left(\sqrt2+\ln(1+\sqrt2)\right)$ |
| 20 | 证明题 | （I）存在 $\xi\in(1,2)$，使 $f(\xi)=(2-\xi)e^{\xi^2}$。 （II）存在 $\eta\in(1,2)$，使 $f(2)=\ln 2\cdot \eta e^{\eta^2}$。 |
| 21 | 解答题 | $y=Cx^3\ (C>0)$ |
| 22 | 解答题 | （I）$a=-\dfrac12$； （II）可取 $P= \begin{pmatrix} \dfrac{1}{\sqrt3} & 1+\dfrac{1}{\sqrt3} & \dfrac23\\[4pt] -\dfrac{1}{\sqrt3} & 1-\dfrac{1}{\sqrt3} & \dfrac23\\[4pt] 0 & 1 & -\dfrac43 \end{pmatrix}.$ |
| 23 | 解答题 | （I）$P$ 可逆； （II） $P^{-1}AP= \begin{pmatrix} 0&6\\ 1&-1 \end{pmatrix},$ 且 $A$ 相似于对角矩阵 $\operatorname{diag}(2,-3)$。 |

## 详细解析

### 第 1 题

- 答案：D

分别比较四项的主阶：

(A) $e^{t^2}-1\sim t^2$，故
$$
\int_0^x (e^{t^2}-1)\,dt\sim \int_0^x t^2\,dt=\frac13x^3.
$$

(B) $\ln(1+\sqrt{t^3})\sim t^{3/2}$，故
$$
\int_0^x \ln(1+\sqrt{t^3})\,dt\sim \int_0^x t^{3/2}\,dt=\frac25x^{5/2}.
$$

(C) $\sin t^2\sim t^2$ 且 $\sin x\sim x$，故
$$
\int_0^{\sin x}\sin t^2\,dt\sim \int_0^x t^2\,dt=\frac13x^3.
$$

(D) 当 $t\to 0$ 时 $\sqrt{\sin^3 t}\sim t^{3/2}$，而 $1-\cos x\sim \dfrac{x^2}{2}$，故
$$
\int_0^{1-\cos x}\sqrt{\sin^3 t}\,dt
\sim \int_0^{x^2/2} t^{3/2}\,dt
=\frac25\left(\frac12\right)^{5/2}x^5.
$$

四项中阶数最高的是 $x^5$，故选 $D$。

### 第 2 题

- 答案：C

由表达式可知可能出现间断点的点为 $x=-1,0,1,2$。

在 $x=-1$ 处，$\ln|1+x|$ 发散，故为第二类间断点；

在 $x=0$ 处，
$$
\lim_{x\to 0}\frac{e^{\frac{1}{x-1}}\ln(1+x)}{(e^x-1)(x-2)}
=\lim_{x\to 0}\frac{e^{\frac{1}{x-1}}\cdot x}{x(x-2)}
=-\frac{1}{2e},
$$
为可去间断点；

在 $x=1$ 处，$e^{1/(x-1)}$ 左右行为不同，极限发散，为第二类间断点；

在 $x=2$ 处，分母为零而分子不为零，也为第二类间断点。

因此第二类间断点共有 $3$ 个，选 $C$。

### 第 3 题

- 答案：A

令 $u=\arcsin\sqrt{x}$，则 $\sqrt{x}=\sin u$，$x=\sin^2u$，
$$
dx=2\sin u\cos u\,du,\qquad \sqrt{x}(1-x)=\sin u\cos^2u.
$$
因而
$$
\int_0^1\frac{\arcsin\sqrt{x}}{\sqrt{x}(1-x)}\,dx
=2\int_0^{\pi/2}u\,du
=\left.u^2\right|_0^{\pi/2}
=\frac{\pi^2}{4}.
$$
选 $A$。

### 第 4 题

- 答案：A

由
$$
\ln(1-x)=-\sum_{k=1}^{\infty}\frac{x^k}{k}\qquad (|x|<1)
$$
得
$$
x^2\ln(1-x)
=-\sum_{k=1}^{\infty}\frac{x^{k+2}}{k}.
$$
因而 $x^n$ 的系数是 $-\dfrac{1}{n-2}$（$n\ge 3$），故
$$
f^{(n)}(0)=n!\left(-\frac{1}{n-2}\right)=-\frac{n!}{n-2}.
$$
选 $A$。

### 第 5 题

- 答案：B

①
$$
\left.\frac{\partial f}{\partial x}\right|_{(0,0)}
=\lim_{h\to 0}\frac{f(h,0)-f(0,0)}{h}
=1.
$$
所以 ① 正确。

② 对于 $y\ne 0$，有 $f_x(0,y)=y$，而 $f_x(0,0)=1$，故
$$
\lim_{y\to 0}\frac{f_x(0,y)-f_x(0,0)}{y}
=\lim_{y\to 0}\frac{y-1}{y}
$$
不存在，故 ② 错。

③ 当 $(x,y)\to(0,0)$ 且 $xy\ne 0$ 时，$f(x,y)=xy\to 0$，沿坐标轴也趋于 $0$，故 ③ 正确。

④ 固定 $y$ 先令 $x\to 0$，有 $f(x,y)\to 0$；再令 $y\to 0$ 仍为 $0$，故 ④ 正确。

因此正确的有 $3$ 个，选 $B$。

### 第 6 题

- 答案：B

由 $f'(x)>f(x)>0$ 得
$$
\frac{f'(x)}{f(x)}>1.
$$
两边积分：
$$
\int_{x_1}^{x_2}\frac{f'(x)}{f(x)}\,dx>x_2-x_1,
$$
即
$$
\ln\frac{f(x_2)}{f(x_1)}>x_2-x_1,
\qquad
\frac{f(x_2)}{f(x_1)}>e^{x_2-x_1}.
$$
取 $x_1=-1,x_2=0$，得
$$
\frac{f(0)}{f(-1)}>e.
$$
故选 $B$。

### 第 7 题

- 答案：C

因 $A$ 不可逆且某个三阶代数余子式 $A_{12}\ne 0$，可知 $r(A)=3$。于是
$$
r(A^*)=1.
$$
故齐次方程组 $A^*x=0$ 的解空间维数为
$$
4-r(A^*)=3.
$$
又因 $A^*$ 的列向量都属于同一维列空间，而由 $A_{12}\ne 0$ 可知 $\alpha_1\ne 0$，从而其余三列可张成零空间的一组基。对应选项为
$$
x=k_1\alpha_1+k_2\alpha_3+k_3\alpha_4.
$$
故选 $C$。

### 第 8 题

- 答案：D

要使
$$
P^{-1}AP=\operatorname{diag}(1,-1,1),
$$
则 $P$ 的第 $1,3$ 列应对应特征值 $1$ 的特征向量，第 $2$ 列应对应特征值 $-1$ 的特征向量。

因 $\alpha_1,\alpha_2$ 都是特征值 $1$ 的特征向量，故 $\alpha_1+\alpha_2$ 仍是特征值 $1$ 的特征向量；$-\alpha_3$ 仍是特征值 $-1$ 的特征向量。

因而
$$
P=(\alpha_1+\alpha_2,-\alpha_3,\alpha_2)
$$
符合要求，选 $D$。

### 第 9 题

- 答案：$-\sqrt{2}$

有
$$
\frac{dx}{dt}=\frac{t}{\sqrt{t^2+1}},\qquad
\frac{dy}{dt}=\frac{1}{\sqrt{t^2+1}}.
$$
所以
$$
\frac{dy}{dx}=\frac{dy/dt}{dx/dt}=\frac{1}{t}.
$$
再求一次导数，
$$
\frac{d^2y}{dx^2}
=\frac{d(1/t)/dt}{dx/dt}
=\frac{-1/t^2}{t/\sqrt{t^2+1}}
=-\frac{\sqrt{t^2+1}}{t^3}.
$$
代入 $t=1$ 得
$$
\left.\frac{d^2y}{dx^2}\right|_{t=1}=-\sqrt2.
$$

### 第 10 题

- 答案：$\dfrac{2}{9}(2\sqrt2-1)$

积分区域为
$$
D=\{(x,y)\mid 0\le y\le 1,\ \sqrt y\le x\le 1\}.
$$
等价改写为
$$
0\le x\le 1,\qquad 0\le y\le x^2.
$$
因而
$$
\int_0^1dy\int_{\sqrt{y}}^1\sqrt{x^3+1}\,dx
=\int_0^1dx\int_0^{x^2}\sqrt{x^3+1}\,dy
=\int_0^1x^2\sqrt{x^3+1}\,dx.
$$
令 $u=x^3+1$，则 $du=3x^2dx$，故
$$
\int_0^1x^2\sqrt{x^3+1}\,dx
=\frac13\int_1^2u^{1/2}\,du
=\frac{2}{9}(2\sqrt2-1).
$$

### 第 11 题

- 答案：$(\pi-1)\,dx-dy$

设
$$
u=xy+\sin(x+y),\qquad z=\arctan u.
$$
在 $(0,\pi)$ 处有
$$
u(0,\pi)=0,\qquad dz=\frac{1}{1+u^2}\,du=du.
$$
又
$$
du=(y+\cos(x+y))dx+(x+\cos(x+y))dy.
$$
代入 $(0,\pi)$：
$$
dz\big|_{(0,\pi)}
=(\pi+\cos\pi)\,dx+(0+\cos\pi)\,dy
=(\pi-1)\,dx-dy.
$$

### 第 12 题

- 答案：$\dfrac13\rho ga^3$

取斜边为底，则该等腰直角三角形对斜边的高为 $a$，故面积
$$
S=\frac12\cdot 2a\cdot a=a^2.
$$
三角形质心到斜边的距离为高的三分之一，即
$$
h_c=\frac{a}{3}.
$$
静水总压力等于压强在质心处的值乘以面积：
$$
F=\rho g h_c S
=\rho g\cdot \frac{a}{3}\cdot a^2
=\frac13\rho ga^3.
$$

### 第 13 题

- 答案：$1$

特征方程为
$$
(\lambda+1)^2=0,
$$
因而
$$
y=(C_1+C_2x)e^{-x}.
$$
由初值条件
$$
y(0)=0,\qquad y'(0)=1
$$
得 $C_1=0,\ C_2=1$，故
$$
y(x)=xe^{-x}.
$$
所以
$$
\int_0^{+\infty}y(x)\,dx
=\int_0^{+\infty}xe^{-x}\,dx
=1.
$$

### 第 14 题

- 答案：$a^2(a-2)(a+2)$

记
$$
B=\begin{pmatrix}-1&1\\1&-1\end{pmatrix},
$$
则原行列式对应矩阵可写成分块形式
$$
\begin{pmatrix}
aI&B\\
B&aI
\end{pmatrix}.
$$
其特征值由 $aI+B$ 与 $aI-B$ 的特征值组成。

矩阵 $B$ 的特征值为 $0,-2$，故原矩阵特征值为
$$
a,\ a,\ a-(-2)=a+2,\ a-2.
$$
因而行列式为
$$
a\cdot a\cdot(a+2)(a-2)=a^2(a-2)(a+2).
$$

### 第 15 题

- 答案：$y=\dfrac1e x+\dfrac{1}{2e}$

先取对数：
$$
\ln y=(1+x)\ln x-x\ln(1+x)
=\ln x-x\ln\left(1+\frac1x\right).
$$
当 $x\to+\infty$ 时，
$$
x\ln\left(1+\frac1x\right)=1-\frac{1}{2x}+o\left(\frac1x\right).
$$
因而
$$
\ln y=\ln x-1+\frac{1}{2x}+o\left(\frac1x\right).
$$
指数化得
$$
y=xe^{-1}\exp\!\left(\frac{1}{2x}+o\left(\frac1x\right)\right)
=\frac{x}{e}\left(1+\frac{1}{2x}+o\left(\frac1x\right)\right)
=\frac{x}{e}+\frac{1}{2e}+o(1).
$$
所以斜渐近线为
$$
y=\frac1e x+\frac{1}{2e}.
$$

### 第 16 题

- 答案：$g'(x)=\dfrac{x f(x)-\int_0^x f(t)\,dt}{x^2}\ (x\ne 0),\quad g'(0)=\dfrac12$

当 $x\ne 0$ 时，令 $u=xt$，则
$$
g(x)=\frac1x\int_0^x f(u)\,du.
$$
由商法则与牛顿-莱布尼茨公式，
$$
g'(x)=\frac{x f(x)-\int_0^x f(t)\,dt}{x^2}\qquad (x\ne 0).
$$

由 $\displaystyle \lim_{x\to 0}\frac{f(x)}{x}=1$，可写
$$
f(x)=x+o(x).
$$
故
$$
\int_0^x f(t)\,dt=\int_0^x\bigl(t+o(t)\bigr)\,dt=\frac{x^2}{2}+o(x^2).
$$
又
$$
x f(x)=x^2+o(x^2).
$$
从而
$$
g'(x)=\frac{x^2+o(x^2)-\left(\frac{x^2}{2}+o(x^2)\right)}{x^2}
\to \frac12.
$$
因此定义
$$
g'(0)=\frac12
$$
时，$g'(x)$ 在 $x=0$ 处连续。

### 第 17 题

- 答案：极小值为 $-\dfrac{1}{216}$（在 $\left(\dfrac16,\dfrac1{12}\right)$ 处），无极大值

先求驻点：
$$
f_x=3x^2-y,\qquad f_y=24y^2-x.
$$
解方程组
$$
3x^2-y=0,\qquad 24y^2-x=0
$$
得
$$
(x,y)=(0,0),\qquad \left(\frac16,\frac1{12}\right).
$$

二阶偏导为
$$
f_{xx}=6x,\qquad f_{yy}=48y,\qquad f_{xy}=-1.
$$
Hessian 判别式
$$
D=f_{xx}f_{yy}-f_{xy}^2.
$$

在 $(0,0)$ 处，
$$
D=-1<0,
$$
故为鞍点。

在 $\left(\dfrac16,\dfrac1{12}\right)$ 处，
$$
D=1>0,\qquad f_{xx}=1>0,
$$
故为极小值点。

极小值为
$$
f\left(\frac16,\frac1{12}\right)
=\frac{1}{216}+\frac{1}{216}-\frac{1}{72}
=-\frac{1}{216}.
$$
因此函数无极大值，极小值为 $-\dfrac1{216}$。

### 第 18 题

- 答案：$f(x)=\dfrac{x}{\sqrt{1+x^2}}$，旋转体体积为 $\dfrac{\pi^2}{6}$

将题设中的 $x$ 替换为 $1/x$，得
$$
2f\!\left(\frac1x\right)+\frac1{x^2}f(x)
=\frac{1+2x}{x\sqrt{1+x^2}}.
$$
与原式联立，解关于
$$
f(x),\quad f\!\left(\frac1x\right)
$$
的线性方程组，可得
$$
f(x)=\frac{x}{\sqrt{1+x^2}}.
$$

由
$$
y=\frac{x}{\sqrt{1+x^2}}
$$
解得
$$
x=\frac{y}{\sqrt{1-y^2}},\qquad 0<y<1.
$$
所围图形绕 $x$ 轴旋转，用柱壳法：
$$
V=2\pi\int_{1/2}^{\sqrt3/2}y\cdot \frac{y}{\sqrt{1-y^2}}\,dy
=2\pi\int_{1/2}^{\sqrt3/2}\frac{y^2}{\sqrt{1-y^2}}\,dy.
$$
令 $y=\sin\theta$，则 $\theta\in[\pi/6,\pi/3]$，故
$$
V=2\pi\int_{\pi/6}^{\pi/3}\sin^2\theta\,d\theta
=2\pi\cdot \frac{\pi}{12}
=\frac{\pi^2}{6}.
$$

### 第 19 题

- 答案：$\dfrac34\left(\sqrt2+\ln(1+\sqrt2)\right)$

区域可表示为
$$
1\le x\le 2,\qquad 0\le y\le x.
$$
故原积分为
$$
\int_1^2dx\int_0^x\frac{\sqrt{x^2+y^2}}{x}\,dy.
$$
令 $y=xt$，则 $dy=xdt$，$0\le t\le 1$，于是
$$
\int_0^x\frac{\sqrt{x^2+y^2}}{x}\,dy
=x\int_0^1\sqrt{1+t^2}\,dt.
$$
从而
$$
\iint_D\frac{\sqrt{x^2+y^2}}{x}\,dxdy
=\int_1^2x\,dx\int_0^1\sqrt{1+t^2}\,dt
=\frac32\int_0^1\sqrt{1+t^2}\,dt.
$$
又
$$
\int_0^1\sqrt{1+t^2}\,dt
=\frac12\left(\sqrt2+\ln(1+\sqrt2)\right),
$$
故结果为
$$
\frac34\left(\sqrt2+\ln(1+\sqrt2)\right).
$$

### 第 20 题

- 答案：（I）存在 $\xi\in(1,2)$，使 $f(\xi)=(2-\xi)e^{\xi^2}$。

（II）存在 $\eta\in(1,2)$，使 $f(2)=\ln 2\cdot \eta e^{\eta^2}$。

（I）令
$$
\phi(x)=f(x)-(2-x)e^{x^2}.
$$
则 $\phi(x)$ 在 $[1,2]$ 上连续，且
$$
\phi(1)=f(1)-e=-e<0,\qquad \phi(2)=f(2)>0.
$$
由介值定理，存在 $\xi\in(1,2)$，使 $\phi(\xi)=0$，即
$$
f(\xi)=(2-\xi)e^{\xi^2}.
$$

（II）将
$$
f(2)=\int_1^2 e^{t^2}\,dt
=\int_1^2 \frac{1}{t}\cdot te^{t^2}\,dt
$$
看作以 $\dfrac1t$ 为正权函数的积分。函数 $h(t)=te^{t^2}$ 在 $[1,2]$ 上连续，且 $\dfrac1t>0$，由积分第一中值定理，存在 $\eta\in(1,2)$，使
$$
f(2)=\eta e^{\eta^2}\int_1^2\frac{1}{t}\,dt.
$$
又
$$
\int_1^2\frac{1}{t}\,dt=\ln 2
$$
所以
$$
f(2)=\ln 2\cdot \eta e^{\eta^2}
$$
成立。

### 第 21 题

- 答案：$y=Cx^3\ (C>0)$

设 $M=(x,y)$，其中 $y=f(x)$，切线斜率为 $f'(x)$。

由切线方程
$$
Y-y=f'(x)(X-x)
$$
知其与 $x$ 轴交点到点 $P=(x,0)$ 的水平距离为
$$
PT=\frac{y}{f'(x)}.
$$
因而
$$
S_{\triangle MTP}=\frac12\cdot y\cdot \frac{y}{f'(x)}=\frac{y^2}{2f'(x)}.
$$

曲线、直线 $MP$ 与 $x$ 轴所围面积为
$$
S(x)=\int_0^x f(t)\,dt.
$$
由题意
$$
\frac{S(x)}{S_{\triangle MTP}}=\frac32,
$$
即
$$
\int_0^x f(t)\,dt=\frac{3f(x)^2}{4f'(x)}.
$$
两边对 $x$ 求导并整理，可得
$$
\frac{f''(x)}{f'(x)}=\frac{2}{3}\frac{f'(x)}{f(x)}.
$$
进一步化为
$$
\frac{d}{dx}\ln f'(x)=\frac23\frac{d}{dx}\ln f(x),
$$
从而
$$
f'(x)=C_1 f(x)^{2/3}\qquad (C_1>0).
$$
分离变量积分：
$$
f(x)^{-2/3}df=C_1\,dx
\Longrightarrow
3f(x)^{1/3}=C_1x+C_2.
$$
又曲线过原点，故 $C_2=0$，于是
$$
f(x)=Cx^3,\qquad C>0.
$$

### 第 22 题

- 答案：（I）$a=-\dfrac12$；

（II）可取
$$
P=
\begin{pmatrix}
\dfrac{1}{\sqrt3} & 1+\dfrac{1}{\sqrt3} & \dfrac23\\[4pt]
-\dfrac{1}{\sqrt3} & 1-\dfrac{1}{\sqrt3} & \dfrac23\\[4pt]
0 & 1 & -\dfrac43
\end{pmatrix}.
$$

原二次型对应矩阵为
$$
A=
\begin{pmatrix}
1&a&a\\
a&1&a\\
a&a&1
\end{pmatrix}.
$$
化后矩阵为
$$
B=
\begin{pmatrix}
1&1&0\\
1&1&0\\
0&0&4
\end{pmatrix}.
$$
由合同变换保持秩，可知 $r(A)=r(B)=2$。

而矩阵 $A$ 的特征值为
$$
1-a,\ 1-a,\ 1+2a.
$$
要使秩为 $2$，只能有且仅有一个特征值为零，因此
$$
1+2a=0\Longrightarrow a=-\frac12.
$$

代入后
$$
f=x_1^2+x_2^2+x_3^2-x_1x_2-x_1x_3-x_2x_3.
$$
选取合适的新基可把它化为
$$
y_1^2+y_2^2+2y_1y_2+4y_3^2.
$$
上述给出的 $P$ 满足
$$
P^{\mathsf T}AP=B,
$$
因而是所求的一个可逆矩阵。

### 第 23 题

- 答案：（I）$P$ 可逆；

（II）
$$
P^{-1}AP=
\begin{pmatrix}
0&6\\
1&-1
\end{pmatrix},
$$
且 $A$ 相似于对角矩阵 $\operatorname{diag}(2,-3)$。

（I）若 $P$ 不可逆，则其两列向量线性相关，即存在常数 $\lambda$ 使
$$
A\alpha=\lambda\alpha.
$$
这说明 $\alpha$ 是 $A$ 的特征向量，与题设矛盾，因此 $P$ 可逆。

（II）在基 $\{\alpha,A\alpha\}$ 下，
$$
A(\alpha)=A\alpha=0\cdot \alpha+1\cdot A\alpha,
$$
而由题设
$$
A^2\alpha=6\alpha-A\alpha,
$$
故
$$
A(A\alpha)=6\alpha-A\alpha.
$$
因而 $A$ 在基 $\{\alpha,A\alpha\}$ 下的矩阵为
$$
P^{-1}AP=
\begin{pmatrix}
0&6\\
1&-1
\end{pmatrix}.
$$
其特征多项式为
$$
\lambda^2+\lambda-6=(\lambda-2)(\lambda+3),
$$
具有两个不同特征值 $2,-3$，故可对角化，所以 $A$ 相似于对角矩阵
$$
\operatorname{diag}(2,-3).
$$
