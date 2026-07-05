# Math 2 2014 Answers

资料类型：考研数学二答案解析
年份：2014
科目：数学二
整理状态：按答案册清洗并与题面同步。

## 答案速查

| 题号 | 题型 | 答案 |
|---|---|---|
| 1 | 选择题 | B |
| 2 | 选择题 | C |
| 3 | 选择题 | D |
| 4 | 选择题 | C |
| 5 | 选择题 | D |
| 6 | 选择题 | A |
| 7 | 选择题 | B |
| 8 | 选择题 | A |
| 9 | 填空题 | $\dfrac{3\pi}{8}$ |
| 10 | 填空题 | $1$ |
| 11 | 填空题 | $-\dfrac12(dx+dy)$ |
| 12 | 填空题 | $y=-\dfrac{2}{\pi}x+\dfrac{\pi}{2}$ |
| 13 | 填空题 | $\dfrac{11}{20}$ |
| 14 | 填空题 | $[-2,2]$ |
| 15 | 解答题 | $\dfrac12$ |
| 16 | 解答题 | 极大值为 $1$，极小值为 $0$ |
| 17 | 解答题 | $-\dfrac34$ |
| 18 | 解答题 | $f(u)=\dfrac{1}{16}e^{2u}-\dfrac{1}{16}e^{-2u}-\dfrac14u$ |
| 19 | 证明题 | 见解析 |
| 20 | 解答题 | $1$ |
| 21 | 解答题 | $\pi\left(2\ln2-\dfrac54\right)$ |
| 22 | 解答题 | (I) 基础解系可取 $\left\{\begin{pmatrix}-1\\2\\3\\1\end{pmatrix}\right\}$；  
(II) 所有满足 $AB=E$ 的矩阵为
$$
B=
\begin{pmatrix}
-c_1+2&-c_2+6&-c_3-1\\
2c_1-1&2c_2-3&2c_3+1\\
3c_1-1&3c_2-4&3c_3+1\\
c_1&c_2&c_3
\end{pmatrix},
\quad c_1,c_2,c_3\in\mathbb R.
$$ |
| 23 | 证明题 | 见解析 |

## 详细解析

### 第 1 题

- 答案：B

要使 $\ln^\alpha(1+2x)=o(x)$，由 $\ln(1+2x)\sim 2x$ 得
$$
\frac{\ln^\alpha(1+2x)}{x}\sim 2^\alpha x^{\alpha-1}\to 0,
$$
故 $\alpha>1$。
又因 $1-\cos x\sim \dfrac{x^2}{2}$，要使 $(1-\cos x)^{1/\alpha}=o(x)$，需
$$
\frac{(1-\cos x)^{1/\alpha}}{x}\sim \left(\frac12\right)^{1/\alpha}x^{2/\alpha-1}\to0,
$$
即 $\dfrac{2}{\alpha}-1>0$，所以 $\alpha<2$。综合得 $\alpha\in(1,2)$。

### 第 2 题

- 答案：C

对 $y=x+\sin\dfrac1x$，当 $x\to\infty$ 时，
$$
\frac{y}{x}=1+\frac{\sin(1/x)}{x}\to 1,\qquad
y-x=\sin\frac1x\to 0.
$$
因此它有斜渐近线 $y=x$。其余选项分别因振荡项不趋零或主项为二次项，不满足渐近线条件。

### 第 3 题

- 答案：D

$g(x)$ 是连接 $(0,f(0))$ 与 $(1,f(1))$ 的弦。若 $f''(x)\ge 0$，则 $f$ 在 $[0,1]$ 上为凸函数，凸函数图像位于任意弦的下方，因此
$$
f(x)\le g(x),\qquad x\in[0,1].
$$
所以选 D。

### 第 4 题

- 答案：C

由参数方程得
$$
\frac{dy}{dx}=\frac{dy/dt}{dx/dt}=\frac{2t+4}{2t},\qquad \left.\frac{dy}{dx}\right|_{t=1}=3.
$$
再求
$$
\frac{d^2y}{dx^2}
=\frac{d}{dt}\left(\frac{2t+4}{2t}\right)\Big/\frac{dx}{dt}
=-\frac{8}{(2t)^3},
$$
所以 $\left.\dfrac{d^2y}{dx^2}\right|_{t=1}=-1$。曲率
$$
k=\frac{|y''|}{(1+y'^2)^{3/2}}=\frac{1}{(1+3^2)^{3/2}}.
$$
因此曲率半径
$$
R=\frac1k=(1+3^2)^{3/2}=10\sqrt{10}.
$$

### 第 5 题

- 答案：D

由题设
$$
\frac{f(x)}{x}=\frac{\arctan x}{x}=\frac{1}{1+\xi^2},
$$
整理得
$$
\xi^2=\frac{x-\arctan x}{\arctan x}.
$$
于是
$$
\frac{\xi^2}{x^2}=\frac{x-\arctan x}{x^2\arctan x}\sim \frac{x-\arctan x}{x^3}.
$$
再用洛必达法则或展开 $\arctan x=x-\dfrac{x^3}{3}+o(x^3)$，得极限为 $\dfrac13$。

### 第 6 题

- 答案：A

由
$$
u_{xx}+u_{yy}=0
$$
且 $u_{xy}\ne 0$，可知若在内部点取极值，则 Hessian 行列式
$$
u_{xx}u_{yy}-u_{xy}^2<0,
$$
与内部极值点的必要条件矛盾，因此内部没有极值点。又因函数在有界闭区域上连续，最大值和最小值存在，只能在边界上取得。

### 第 7 题

- 答案：B

按第一列展开并继续化简，可得原行列式等于
$$
(bc-ad)\begin{vmatrix} a&b\\ c&d \end{vmatrix}
=-(ad-bc)^2.
$$
因而选 B。

### 第 8 题

- 答案：A

若 $\alpha_1,\alpha_2,\alpha_3$ 线性无关，则
$$
\lambda_1(\alpha_1+k\alpha_3)+\lambda_2(\alpha_2+l\alpha_3)=0
$$
推出
$$
\lambda_1\alpha_1+\lambda_2\alpha_2+(k\lambda_1+l\lambda_2)\alpha_3=0,
$$
从而 $\lambda_1=\lambda_2=0$，故前两向量必线性无关，所以这是必要条件。
但反过来不成立，例如取 $\alpha_3=0$ 而 $\alpha_1,\alpha_2$ 无关时，$\alpha_1+k\alpha_3,\alpha_2+l\alpha_3$ 仍无关。故为必要非充分条件。

### 第 9 题

- 答案：$\dfrac{3\pi}{8}$

配方得
$$
x^2+2x+5=(x+1)^2+4.
$$
因此
$$
\int_{-\infty}^{1}\frac{dx}{x^2+2x+5}
=\int_{-\infty}^{1}\frac{dx}{(x+1)^2+4}
=\frac12\arctan\frac{x+1}{2}\Big|_{-\infty}^{1}
=\frac12\left(\frac{\pi}{4}+\frac{\pi}{2}\right)
=\frac{3\pi}{8}.
$$

### 第 10 题

- 答案：$1$

由 $f'(x)=2(x-1)$ 得
$$
f(x)=x^2-2x+c,\qquad x\in[0,2].
$$
又 $f$ 为奇函数，故 $f(0)=0$，从而 $c=0$，即
$$
f(x)=x^2-2x,\qquad x\in[0,2].
$$
利用周期 4 与奇函数性质，
$$
f(7)=f(3)=f(-1)=-f(1)=-(1-2)=1.
$$

### 第 11 题

- 答案：$-\dfrac12(dx+dy)$

先由方程在 $\left(\dfrac12,\dfrac12\right)$ 处求对应的 $z$。代入得
$$
e^{z/2}+z+ \frac34=\frac74,
$$
易知 $z=0$。
对原方程分别对 $x,y$ 求偏导：
$$
e^{2yz}(2y z_x)+1+z_x=0,\qquad e^{2yz}(2z+2y z_y)+2y+z_y=0.
$$
在 $\left(x,y,z\right)=\left(\dfrac12,\dfrac12,0\right)$ 处有
$$
z_x=-\frac12,\qquad z_y=-\frac12.
$$
所以
$$
dz=z_x\,dx+z_y\,dy=-\frac12(dx+dy).
$$

### 第 12 题

- 答案：$y=-\dfrac{2}{\pi}x+\dfrac{\pi}{2}$

化为参数方程
$$
x=\theta\cos\theta,\qquad y=\theta\sin\theta.
$$
则
$$
\frac{dy}{dx}=\frac{dy/d\theta}{dx/d\theta}
=\frac{\sin\theta+\theta\cos\theta}{\cos\theta-\theta\sin\theta}.
$$
当 $\theta=\dfrac{\pi}{2}$ 时，
$$
\frac{dy}{dx}=-\frac{2}{\pi},\qquad (x,y)=\left(0,\frac{\pi}{2}\right).
$$
故切线方程为
$$
y-\frac{\pi}{2}=-\frac{2}{\pi}(x-0),
$$
即
$$
y=-\frac{2}{\pi}x+\frac{\pi}{2}.
$$

### 第 13 题

- 答案：$\dfrac{11}{20}$

质心横坐标
$$
\bar x=\frac{\int_0^1 x\rho(x)\,dx}{\int_0^1\rho(x)\,dx}
=\frac{\int_0^1 x(-x^2+2x+1)\,dx}{\int_0^1(-x^2+2x+1)\,dx}.
$$
计算得
$$
\int_0^1 x(-x^2+2x+1)\,dx=\frac{11}{12},\qquad
\int_0^1(-x^2+2x+1)\,dx=\frac53.
$$
因而
$$
\bar x=\frac{11/12}{5/3}=\frac{11}{20}.
$$

### 第 14 题

- 答案：$[-2,2]$

配方可写为
$$
f=(x_1+ax_3)^2-(x_2-2x_3)^2+(4-a^2)x_3^2.
$$
要使负惯性指数恰为 1，除了 $-(x_2-2x_3)^2$ 这一项外，其余部分不能再贡献负平方项，因此需
$$
4-a^2\ge 0.
$$
解得
$$
-2\le a\le 2.
$$

### 第 15 题

- 答案：$\dfrac12$

分子分母同趋于无穷大，可用洛必达法则：
$$
\lim_{x\to+\infty}\frac{\int_1^x\left[t^2\left(e^{1/t}-1\right)-t\right]dt}{x^2\ln\left(1+\frac1x\right)}
=
\lim_{x\to+\infty}\frac{x^2(e^{1/x}-1)-x}{x^2\cdot \frac1x}.
$$
进一步化为
$$
\lim_{x\to+\infty}x\left[x\left(e^{1/x}-1\right)-1\right].
$$
令 $u=\dfrac1x\to 0^+$，由
$$
e^u=1+u+\frac{u^2}{2}+O(u^3)
$$
得
$$
x\left(e^{1/x}-1\right)-1=\frac{1}{2x}+o\left(\frac1x\right),
$$
因而极限为 $\dfrac12$。

### 第 16 题

- 答案：极大值为 $1$，极小值为 $0$

由方程得
$$
y'=\frac{1-x^2}{y^2+1}.
$$
令 $y'=0$，得驻点满足 $x=\pm 1$。再由
$$
y''=\frac{-2x(y^2+1)-(1-x^2)\cdot 2yy'}{(y^2+1)^2}
$$
可知
$$
y''(1)=-\frac{2}{y^2(1)+1}<0,\qquad y''(-1)=\frac{2}{y^2(-1)+1}>0,
$$
所以 $x=1$ 处取极大值，$x=-1$ 处取极小值。
又因
$$
(y^2+1)dy=(1-x^2)dx,
$$
积分得
$$
\frac13y^3+y=x-\frac13x^3+C.
$$
利用 $y(2)=0$ 得 $C=\dfrac23$，故
$$
\frac13y^3+y=x-\frac13x^3+\frac23.
$$
代入 $x=1$ 得 $y(1)=1$；代入 $x=-1$ 得 $y(-1)=0$。故极大值为 $1$，极小值为 $0$。

### 第 17 题

- 答案：$-\dfrac34$

区域 $D$ 关于直线 $y=x$ 对称，因此
$$
\iint_D \frac{x\sin(\pi\sqrt{x^2+y^2})}{x+y}\,dxdy
=
\iint_D \frac{y\sin(\pi\sqrt{x^2+y^2})}{x+y}\,dxdy.
$$
两式相加后除以 2，得原积分
$$
I=\frac12\iint_D \sin(\pi\sqrt{x^2+y^2})\,dxdy.
$$
改用极坐标：
$$
I=\frac12\int_0^{\pi/2}\!\!d\theta\int_1^2 \sin(\pi r)\,r\,dr
=\frac{\pi}{4\pi}\int_1^2 r\sin(\pi r)\,dr.
$$
分部积分可得
$$
I=-\frac34.
$$

### 第 18 题

- 答案：$f(u)=\dfrac{1}{16}e^{2u}-\dfrac{1}{16}e^{-2u}-\dfrac14u$

设 $u=e^x\cos y$，则
$$
z=f(u),\quad z_x=f'(u)e^x\cos y,\quad z_y=-f'(u)e^x\sin y.
$$
继续求二阶偏导并相加，得到
$$
z_{xx}+z_{yy}=f''(u)e^{2x}.
$$
与题设比较可知
$$
f''(u)=4f(u)+u.
$$
即 $f$ 满足常系数方程
$$
f''-4f=u.
$$
其通解为
$$
f(u)=C_1e^{2u}+C_2e^{-2u}-\frac14u.
$$
由 $f(0)=0,\ f'(0)=0$ 得
$$
C_1+C_2=0,\qquad 2C_1-2C_2-\frac14=0,
$$
解得
$$
C_1=\frac1{16},\qquad C_2=-\frac1{16}.
$$
因而
$$
f(u)=\frac{1}{16}e^{2u}-\frac{1}{16}e^{-2u}-\frac14u.
$$

### 第 19 题

- 答案：见解析

设
$$
h_1(x)=\int_a^x g(t)\,dt,\qquad h_2(x)=\int_a^x g(t)\,dt-x+a.
$$
则
$$
h_1'(x)=g(x)\ge 0,\qquad h_2'(x)=g(x)-1\le 0.
$$
又 $h_1(a)=h_2(a)=0$，因此
$$
h_1(x)\ge 0,\qquad h_2(x)\le 0,
$$
即得
$$
0\le \int_a^x g(t)\,dt\le x-a.
$$

再设
$$
p(x)=\int_a^x f(u)g(u)\,du-\int_a^{a+\int_a^x g(t)\,dt} f(u)\,du.
$$
由链式法则，
$$
p'(x)=\left[f(x)-f\!\left(a+\int_a^x g(t)\,dt\right)\right]g(x).
$$
由 (I) 知
$$
a+\int_a^x g(t)\,dt\le x,
$$
又 $f$ 单调增加，故
$$
f(x)\ge f\!\left(a+\int_a^x g(t)\,dt\right),
$$
从而 $p'(x)\ge 0$。且 $p(a)=0$，所以 $p(b)\ge 0$，即
$$
\int_a^{a+\int_a^b g(t)\,dt} f(x)\,dx\le \int_a^b f(x)g(x)\,dx.
$$

### 第 20 题

- 答案：$1$

先计算前几项：
$$
f_1(x)=\frac{x}{1+x},\qquad
f_2(x)=\frac{x}{1+2x},\qquad
f_3(x)=\frac{x}{1+3x}.
$$
由归纳法可得
$$
f_n(x)=\frac{x}{1+nx},\qquad x\in[0,1].
$$
因而
$$
S_n=\int_0^1 \frac{x}{1+nx}\,dx
=\frac1n\int_0^1\left(1-\frac{1}{1+nx}\right)dx
=\frac1n-\frac{1}{n^2}\ln(1+n).
$$
所以
$$
nS_n=1-\frac{\ln(1+n)}{n}\to 1.
$$

### 第 21 题

- 答案：$\pi\left(2\ln2-\dfrac54\right)$

由
$$
\frac{\partial f}{\partial y}=2(y+1)
$$
对 $y$ 积分得
$$
f(x,y)=y^2+2y+\varphi(x).
$$
再由条件
$$
f(y,y)=(y+1)^2-(2-y)\ln y
$$
得
$$
y^2+2y+\varphi(y)=(y+1)^2-(2-y)\ln y,
$$
所以
$$
\varphi(y)=1-(2-y)\ln y.
$$
故
$$
f(x,y)=(y+1)^2-(2-x)\ln x.
$$
于是边界曲线满足
$$
(y+1)^2=(2-x)\ln x.
$$
右端非负时 $1\le x\le 2$。旋转体体积为
$$
V=\pi\int_1^2(2-x)\ln x\,dx
=\pi\left(2\ln2-\frac54\right).
$$

### 第 22 题

- 答案：(I) 基础解系可取 $\left\{\begin{pmatrix}-1\\2\\3\\1\end{pmatrix}\right\}$；  
(II) 所有满足 $AB=E$ 的矩阵为
$$
B=
\begin{pmatrix}
-c_1+2&-c_2+6&-c_3-1\\
2c_1-1&2c_2-3&2c_3+1\\
3c_1-1&3c_2-4&3c_3+1\\
c_1&c_2&c_3
\end{pmatrix},
\quad c_1,c_2,c_3\in\mathbb R.
$$

对 $A$ 作行变换可化为
$$
\begin{pmatrix}
1&0&0&1\\
0&1&0&-2\\
0&0&1&-3
\end{pmatrix}.
$$
因而齐次方程组 $Ax=0$ 满足
$$
x_1=-x_4,\qquad x_2=2x_4,\qquad x_3=3x_4,
$$
所以基础解系可取
$$
\left\{\begin{pmatrix}-1\\2\\3\\1\end{pmatrix}\right\}.
$$

设
$$
B=(\beta_1,\beta_2,\beta_3),
$$
则 $AB=E$ 等价于分别解
$$
A\beta_1=e_1,\quad A\beta_2=e_2,\quad A\beta_3=e_3.
$$
每个非齐次方程的通解都等于一个特解加上齐次解，整理可得
$$
\beta_1=\begin{pmatrix}2\\-1\\-1\\0\end{pmatrix}+c_1\begin{pmatrix}-1\\2\\3\\1\end{pmatrix},
\quad
\beta_2=\begin{pmatrix}6\\-3\\-4\\0\end{pmatrix}+c_2\begin{pmatrix}-1\\2\\3\\1\end{pmatrix},
\quad
\beta_3=\begin{pmatrix}-1\\1\\1\\0\end{pmatrix}+c_3\begin{pmatrix}-1\\2\\3\\1\end{pmatrix},
$$
从而得到题述全部矩阵 $B$。

### 第 23 题

- 答案：见解析

先求 $A$ 的特征多项式。注意到 $A$ 的秩为 1，且向量 $(1,1,\dots,1)^\mathrm T$ 是其特征向量，对应特征值 $n$；其余与该向量正交的 $n-1$ 维子空间上均对应特征值 $0$。因此
$$
A\sim \operatorname{diag}(n,0,\dots,0).
$$

对矩阵 $B$，其特征多项式同样为
$$
\lambda^{\,n-1}(\lambda-n),
$$
即特征值也是 $n,0,\dots,0$。又由 $r(B)=1$，可知零特征值对应有 $n-1$ 个线性无关特征向量，因此 $B$ 也可相似对角化，且
$$
B\sim \operatorname{diag}(n,0,\dots,0).
$$
二者都与同一对角矩阵相似，所以 $A$ 与 $B$ 相似。
