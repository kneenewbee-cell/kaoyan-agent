# 2018 年数学二答案解析

资料类型：考研数学二答案解析
年份：2018
科目：数学二
整理状态：基于答案解析 PDF 页图与题面交叉清洗。

## 答案速查

| 题号 | 题型 | 答案 |
|---|---|---|
| 1 | 选择题 | B |
| 2 | 选择题 | D |
| 3 | 选择题 | D |
| 4 | 选择题 | D |
| 5 | 选择题 | C |
| 6 | 选择题 | C |
| 7 | 选择题 | A |
| 8 | 选择题 | A |
| 9 | 填空题 | 1 |
| 10 | 填空题 | $y=4x-3$ |
| 11 | 填空题 | $\dfrac12\ln2$ |
| 12 | 填空题 | $\dfrac23$ |
| 13 | 填空题 | $\dfrac14$ |
| 14 | 填空题 | 2 |
| 15 | 解答题 | $\frac12\left[e^{2x}\arctan\sqrt{e^x-1}-\frac13\left(\sqrt{e^x-1}\right)^3+\sqrt{e^x-1}\right]+C.$ |
| 16 | 解答题 | (1) $f(x)=2a(1-e^{-x})$； (2) $a=\dfrac e2$。 |
| 17 | 解答题 | $3\pi^2+5\pi$ |
| 18 | 证明题 | 结论成立 |
| 19 | 解答题 | $S_{\min}=\dfrac{1}{\pi+4+3\sqrt3}$ |
| 20 | 解答题 | 10 |
| 21 | 证明题 | 数列收敛，且极限为 0 |
| 22 | 解答题 | (1) 当 $a=2$ 时，$x=k(2,1,-1)^{\mathsf T}\ (k\in\mathbb R)$；当 $a\ne2$ 时，只有零解。 (2) 当 $a=2$ 时，规范形为 $y_1^2+y_2^2$；当 $a\ne2$ 时，规范形为 $y_1^2+y_2^2+y_3^2$。 |
| 23 | 解答题 | (1) $a=2$； (2) 可取 $P= \begin{pmatrix} -6k_1+3&-6k_2+4&-6k_3+4\\ 2k_1-1&2k_2-1&2k_3-1\\ k_1&k_2&k_3 \end{pmatrix},$ 其中 $k_1,k_2,k_3\in\mathbb R$，且 $k_2\ne k_3$。 |

## 详细解析

### 第 1 题

- 答案：B

设 $u=e^x+ax^2+bx-1$，则原式为 $\lim_{x\to0}(1+u)^{1/x^2}$。要使极限为 $1$，需
$$
\lim_{x\to0}\frac{u}{x^2}=0.
$$
先由
$$
\lim_{x\to0}\frac{e^x+ax^2+bx-1}{x}=1+b=0
$$
得 $b=-1$。再代回，
$$
\lim_{x\to0}\frac{e^x-x+ax^2-1}{x^2}=\frac12+a=0,
$$
故 $a=-\dfrac12$。选 B。

### 第 2 题

- 答案：D

由导数定义逐项判断。
选项 A、B 有
$$
\frac{f(x)-f(0)}{x}\to0.
$$
选项 C 中
$$
\cos|x|-1\sim-\frac{|x|^2}{2},
$$
故商仍趋于 $0$。而 D 中
$$
\cos\sqrt{|x|}-1\sim-\frac{|x|}{2},
$$
于是
$$
\frac{\cos\sqrt{|x|}-1}{x}\sim-\frac{|x|}{2x}
$$
左右极限不相等，不可导。选 D。

### 第 3 题

- 答案：D

有
$$
f(x)+g(x)=
\begin{cases}
1-ax,& x\le -1,\\
x-1,& -1<x<0,\\
x+1-b,& x\ge 0.
\end{cases}
$$
在 $x=-1$ 处连续给出
$$
1+a=-2 \Rightarrow a=-3.
$$
在 $x=0$ 处连续给出
$$
-1=1-b \Rightarrow b=2.
$$
选 D。

### 第 4 题

- 答案：D

取 $f(x)=x-\dfrac12$ 或 $f(x)=\dfrac12-x$ 可排除 A、C。若 $f''(x)>0$，则在 $x=\dfrac12$ 处作泰勒展开：
$$
f(x)=f\!\left(\frac12\right)+f'\!\left(\frac12\right)\left(x-\frac12\right)+\frac{f''(\xi)}{2}\left(x-\frac12\right)^2.
$$
因为 $f''(\xi)>0$，故
$$
f(x)>f\!\left(\frac12\right)+f'\!\left(\frac12\right)\left(x-\frac12\right).
$$
两边在 $[0,1]$ 上积分，利用 $\int_0^1 f(x)\,dx=0$ 且 $\int_0^1(x-\frac12)\,dx=0$，得
$$
0>f\!\left(\frac12\right).
$$
选 D。

### 第 5 题

- 答案：C

化简
$$
M=\int_{-\pi/2}^{\pi/2}\left(1+\frac{2x}{1+x^2}\right)dx=\int_{-\pi/2}^{\pi/2}1\,dx=\pi.
$$
因为 $e^x>1+x$，所以
$$
N=\int_{-\pi/2}^{\pi/2}\frac{1+x}{e^x}\,dx<\int_{-\pi/2}^{\pi/2}1\,dx=\pi=M.
$$
又因 $1+\sqrt{\cos x}>1$，故
$$
K>\int_{-\pi/2}^{\pi/2}1\,dx=\pi=M.
$$
所以 $K>M>N$，选 C。

### 第 6 题

- 答案：C

积分区域为
$$
D=\{(x,y)\mid -1\le x\le0,\ -x\le y\le2-x^2\}\cup\{(x,y)\mid 0\le x\le1,\ x\le y\le2-x^2\}.
$$
其中 $xy$ 关于 $x$ 为奇函数，区域关于 $y$ 轴对称，因此奇部积分为 $0$。原式化为
$$
2\int_0^1dx\int_x^{2-x^2}1\,dy
=2\int_0^1(2-x^2-x)\,dx=\frac73.
$$
选 C。

### 第 7 题

- 答案：A

取
$$
P=\begin{pmatrix}
1&-1&0\\
0&1&0\\
0&0&1
\end{pmatrix},\qquad
P^{-1}=\begin{pmatrix}
1&1&0\\
0&1&0\\
0&0&1
\end{pmatrix}.
$$
直接计算得
$$
P^{-1}\begin{pmatrix}
1&1&-1\\
0&1&1\\
0&0&1
\end{pmatrix}P=
\begin{pmatrix}
1&1&0\\
0&1&1\\
0&0&1
\end{pmatrix}.
$$
故选 A。

### 第 8 题

- 答案：A

选项 C 显然不对，秩一般满足的是上、下界而不是恒等于最大值。选项 B、D 均可构造反例否定。对 A，
$$
(A,AB)=A(E,B),
$$
右乘分块不增加超出 $A$ 列空间的部分，因此
$$
r(A,AB)=r(A).
$$
故选 A。

### 第 9 题

- 答案：1

由拉格朗日中值定理，存在 $\xi\in(x,x+1)$ 使
$$
\arctan(x+1)-\arctan x=\frac{1}{1+\xi^2}.
$$
所以
$$
x^2[\arctan(x+1)-\arctan x]=\frac{x^2}{1+\xi^2}\to1.
$$

### 第 10 题

- 答案：$y=4x-3$

$$
y'=2x+\frac{2}{x},\qquad y''=2-\frac{2}{x^2}.
$$
令 $y''=0$ 得 $x=1$，对应点为 $(1,1)$。此时斜率
$$
y'(1)=4,
$$
切线方程为
$$
y-1=4(x-1),
$$
即 $y=4x-3$。

### 第 11 题

- 答案：$\dfrac12\ln2$

分解
$$
\frac{1}{x^2-4x+3}=\frac12\left(\frac{1}{x-3}-\frac{1}{x-1}\right).
$$
因而
$$
\int_5^{+\infty}\frac{1}{x^2-4x+3}\,dx
=\frac12\ln\left|\frac{x-3}{x-1}\right|\Bigg|_5^{+\infty}
=\frac12\ln2.
$$

### 第 12 题

- 答案：$\dfrac23$

先求
$$
\frac{dy}{dx}=\frac{dy/dt}{dx/dt}=-\tan t,
$$
进而
$$
\frac{d^2y}{dx^2}=\frac{1}{3\cos^4 t\sin t}.
$$
当 $t=\dfrac{\pi}{4}$ 时，
$$
y'=-1,\qquad y''=\frac{4\sqrt2}{3}.
$$
曲率
$$
k=\frac{|y''|}{[1+(y')^2]^{3/2}}=\frac{2}{3}.
$$

### 第 13 题

- 答案：$\dfrac14$

由题设在 $(x,y)=\left(2,\dfrac12\right)$ 时有 $xy=1$，代入可得 $z=1$。令
$$
F(x,y,z)=\ln z+e^{z-1}-xy=0.
$$
则
$$
F_x=-y,\qquad F_z=\frac1z+e^{z-1}.
$$
所以
$$
\frac{\partial z}{\partial x}=-\frac{F_x}{F_z}
=\frac{y}{1/z+e^{z-1}}.
$$
在 $\left(2,\dfrac12,1\right)$ 处得 $\dfrac14$。

### 第 14 题

- 答案：2

在基 $(\alpha_1,\alpha_2,\alpha_3)$ 下，$A$ 的矩阵为
$$
\begin{pmatrix}
2&0&0\\
1&1&-1\\
1&2&1
\end{pmatrix}.
$$
行列式与基无关，所以
$$
|A|=\begin{vmatrix}
2&0&0\\
1&1&-1\\
1&2&1
\end{vmatrix}=2.
$$

### 第 15 题

- 答案：$$
\frac12\left[e^{2x}\arctan\sqrt{e^x-1}-\frac13\left(\sqrt{e^x-1}\right)^3+\sqrt{e^x-1}\right]+C.
$$

记
$$
I=\int e^{2x}\arctan\sqrt{e^x-1}\,dx.
$$
分部积分，取
$$
u=\arctan\sqrt{e^x-1},\qquad dv=e^{2x}dx,
$$
则
$$
I=\frac12e^{2x}\arctan\sqrt{e^x-1}-\frac12\int \frac{e^{2x}}{2\sqrt{e^x-1}}\,dx.
$$
再令 $t=\sqrt{e^x-1}$，则 $e^x=t^2+1$，可化为有理式积分，算得
$$
I=\frac12\left[e^{2x}\arctan\sqrt{e^x-1}-\frac13(\sqrt{e^x-1})^3+\sqrt{e^x-1}\right]+C.
$$

### 第 16 题

- 答案：(1) $f(x)=2a(1-e^{-x})$；

(2) $a=\dfrac e2$。

将第二项作换元 $u=x-t$，得
$$
\int_0^x f(t)\,dt+\int_0^x (x-u)f(u)\,du=ax^2.
$$
整理后对 $x$ 求导，可得
$$
f(x)+\int_0^x f(u)\,du=2ax.
$$
令
$$
F(x)=\int_0^x f(u)\,du,
$$
则 $F'(x)+F(x)=2ax,\ F(0)=0$。解得
$$
F(x)=2ax-2a+2ae^{-x},
$$
故
$$
f(x)=F'(x)=2a(1-e^{-x}).
$$
再由平均值条件
$$
\int_0^1 f(x)\,dx=1
$$
得
$$
2a\int_0^1(1-e^{-x})dx=1 \Rightarrow \frac{2a}{e}=1,
$$
所以 $a=\dfrac e2$。

### 第 17 题

- 答案：$3\pi^2+5\pi$

对竖条积分，设上边界为 $y=\varphi(x)$，则
$$
\iint_D(x+2y)\,dxdy=\int_0^{2\pi}[x\varphi(x)+\varphi^2(x)]\,dx.
$$
再用参数表示
$$
x=t-\sin t,\qquad y=1-\cos t,\qquad dx=(1-\cos t)dt,
$$
可得
$$
\iint_D(x+2y)\,dxdy
=\int_0^{2\pi}(t-\sin t)(1-\cos t)^2dt+\int_0^{2\pi}(1-\cos t)^3dt.
$$
逐项积分后得到
$$
3\pi^2+5\pi.
$$

### 第 18 题

- 答案：结论成立

设
$$
f(x)=x-\ln^2x+2k\ln x-1.
$$
只需证明 $x<1$ 时 $f(x)\le0$，$x>1$ 时 $f(x)\ge0$。

对 $0<x<1$，有
$$
f'(x)=\frac{x-2\ln x+2k}{x}.
$$
再设 $g(x)=x-2\ln x+2k$，则
$$
g'(x)=1-\frac2x<0.
$$
所以 $g(x)>g(1)=1+2k\ge2\ln2-1>0$，故 $f'(x)>0$，从而 $f(x)\le f(1)=0$。

对 $x>1$ 同理，$g'(x)=1-\dfrac2x$ 在 $(1,2)$ 上小于零、在 $(2,+\infty)$ 上大于零，故
$$
g(x)\ge g(2)=2-2\ln2+2k\ge0.
$$
因而 $f'(x)\ge0$，故 $f(x)\ge f(1)=0$。

于是
$$
(x-1)f(x)\ge0,
$$
即原不等式成立。

### 第 19 题

- 答案：$S_{\min}=\dfrac{1}{\pi+4+3\sqrt3}$

设三段长度分别为 $x,y,z$，则
$$
x+y+z=2.
$$
圆、正三角形、正方形的面积分别为
$$
\frac{x^2}{4\pi},\qquad \frac{\sqrt3\,y^2}{36},\qquad \frac{z^2}{16}.
$$
故
$$
S=\frac{x^2}{4\pi}+\frac{\sqrt3\,y^2}{36}+\frac{z^2}{16}.
$$
这是闭有界集合上的连续函数，最小值存在。用拉格朗日乘子法：
$$
F=\frac{x^2}{4\pi}+\frac{\sqrt3\,y^2}{36}+\frac{z^2}{16}+\lambda(x+y+z-2).
$$
解方程组得
$$
x=\frac{4\pi}{2\pi+8+6\sqrt3},\quad
y=\frac{12\sqrt3}{2\pi+8+6\sqrt3},\quad
z=\frac{16}{2\pi+8+6\sqrt3}.
$$
代回得
$$
S_{\min}=\frac{1}{\pi+4+3\sqrt3}.
$$

### 第 20 题

- 答案：10

设 $P=(x(t),\frac49x^2(t))$。由图形面积可得
$$
S(t)=\frac12\left(1+\frac49x^2(t)\right)x(t)-\int_0^{x(t)}\frac49u^2\,du
=\frac{x(t)}{2}+\frac{2}{27}x^3(t).
$$
所以
$$
S'(t)=\frac12x'(t)+\frac29x^2(t)x'(t).
$$
当 $x=3,\ x'(t)=4$ 时，
$$
S'(t)=\frac12\cdot4+\frac29\cdot9\cdot4=10.
$$

### 第 21 题

- 答案：数列收敛，且极限为 0

由递推式得
$$
x_{n+1}=\ln\frac{e^{x_n}-1}{x_n}.
$$
因为 $x_1>0$，且对 $x>0$ 有 $e^x-1>x$，所以归纳可得 $x_n>0$。

再由中值定理，
$$
e^{x_n}-1=e^{\xi_n}x_n\qquad(0<\xi_n<x_n),
$$
从而
$$
e^{x_{n+1}}=\frac{e^{x_n}-1}{x_n}=e^{\xi_n},
$$
即 $x_{n+1}=\xi_n<x_n$。故 $\{x_n\}$ 单调递减且有下界 $0$，从而收敛。

设极限为 $A\ge0$，对递推式取极限：
$$
Ae^A=e^A-1.
$$
解得 $A=0$。故
$$
\lim_{n\to\infty}x_n=0.
$$

### 第 22 题

- 答案：(1) 当 $a=2$ 时，$x=k(2,1,-1)^{\mathsf T}\ (k\in\mathbb R)$；当 $a\ne2$ 时，只有零解。

(2) 当 $a=2$ 时，规范形为 $y_1^2+y_2^2$；当 $a\ne2$ 时，规范形为 $y_1^2+y_2^2+y_3^2$。

由 $f=0$ 可知三个平方项都为零，即
$$
\begin{cases}
x_1-x_2+x_3=0,\\
x_2+x_3=0,\\
x_1+ax_3=0.
\end{cases}
$$
其系数矩阵经消元可化为上三角，最后一行给出系数 $a-2$。故当 $a\ne2$ 时秩为 $3$，只有零解；当 $a=2$ 时秩为 $2$，通解为
$$
x=k(2,1,-1)^{\mathsf T}.
$$

令
$$
y_1=x_1-x_2+x_3,\quad y_2=x_2+x_3,\quad y_3=x_1+ax_3,
$$
则
$$
f=y_1^2+y_2^2+y_3^2.
$$
当 $a\ne2$ 时变换矩阵可逆，故规范形为 $y_1^2+y_2^2+y_3^2$。当 $a=2$ 时该变换矩阵秩为 $2$，此时二次型正惯性指数为 $2$、零惯性指数为 $1$，故规范形为 $y_1^2+y_2^2$。

### 第 23 题

- 答案：(1) $a=2$；

(2) 可取
$$
P=
\begin{pmatrix}
-6k_1+3&-6k_2+4&-6k_3+4\\
2k_1-1&2k_2-1&2k_3-1\\
k_1&k_2&k_3
\end{pmatrix},
$$
其中 $k_1,k_2,k_3\in\mathbb R$，且 $k_2\ne k_3$。

因为 $A$ 可经初等列变换化为 $B$，故 $r(A)=r(B)$。分别对两矩阵做消元：
$$
A\sim
\begin{pmatrix}
1&2&a\\
0&1&-a\\
0&0&0
\end{pmatrix},\qquad
B\sim
\begin{pmatrix}
1&a&2\\
0&1&1\\
0&0&2-a
\end{pmatrix}.
$$
因秩相等，得 $2-a=0$，即 $a=2$。

于是求矩阵方程 $AP=B$。把增广矩阵 $(A,B)$ 消元可得通解
$$
P=
\begin{pmatrix}
-6k_1+3&-6k_2+4&-6k_3+4\\
2k_1-1&2k_2-1&2k_3-1\\
k_1&k_2&k_3
\end{pmatrix}.
$$
其可逆条件为 $|P|\ne0$，由结果可化为 $k_2\ne k_3$。故上式即所求。
