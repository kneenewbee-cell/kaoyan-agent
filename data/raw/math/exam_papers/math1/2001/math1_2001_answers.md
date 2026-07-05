# Math 1 2001 Answers

资料类型：考研数学一答案解析
年份：2001
科目：数学一
范围：试卷 I
来源：D:\百度网盘\高数资料\【02】1987-2022年数学一真题详解答案（PDF）\2001考研数学一真题解析.pdf
校对状态：已按答案页图像和题干重新整理，去除识别碎行、串题内容和非本题页脚。

## 答案速查

| 题号 | 题型 | 答案 |
|---|---|---|
| 1 | 填空题 | $y''-2y'+2y=0$ |
| 2 | 填空题 | $\dfrac{2}{3}$ |
| 3 | 填空题 | $\displaystyle \int_1^2 dx\int_0^{1-x} f(x,y)\,dy$ |
| 4 | 填空题 | $\dfrac{1}{2}(A+2E)$ |
| 5 | 填空题 | $\dfrac{1}{2}$ |
| 6 | 选择题 | D |
| 7 | 选择题 | C |
| 8 | 选择题 | B |
| 9 | 选择题 | A |
| 10 | 选择题 | A |
| 11 | 解答题 | $-\dfrac{1}{2}\left(e^{-2x}\arctan e^x+e^{-x}+\arctan e^x\right)+C$ |
| 12 | 解答题 | $51$ |
| 13 | 解答题 | $\displaystyle f(x)=1+\sum_{n=1}^{\infty}\frac{2(-1)^n}{1-4n^2}x^{2n}\ (-1\le x\le1)$；$\displaystyle \sum_{n=1}^{\infty}\frac{(-1)^n}{1-4n^2}=\frac{\pi}{4}-\frac{1}{2}$ |
| 14 | 解答题 | $-24$ |
| 15 | 解答题 | (1) 存在且唯一；(2) $\displaystyle \lim_{x\to0}\theta(x)=\frac{1}{2}$ |
| 16 | 解答题 | $100$ 小时 |
| 17 | 解答题 | $t_1^s+(-1)^{s+1}t_2^s\ne0$；等价地，$s$ 为偶数时 $t_1\ne\pm t_2$，$s$ 为奇数时 $t_1\ne -t_2$ |
| 18 | 解答题 | $(1)\ \displaystyle B=\begin{pmatrix}0&0&0\\1&0&3\\0&1&-2\end{pmatrix}$；$(2)\ \det(A+E)=-4$ |
| 19 | 解答题 | $(1)\ \displaystyle P\{Y=m\mid X=n\}=\binom{n}{m} p^m(1-p)^{n-m}$；$(2)\ \displaystyle P\{X=n,Y=m\}=\binom{n}{m} p^m(1-p)^{n-m}\frac{\lambda^n}{n!}e^{-\lambda}$，$0\le m\le n$ |
| 20 | 解答题 | $2(n-1)\sigma^2$ |

## 详细解析

### 第 1 题
- 答案：$y''-2y'+2y=0$

通解
$$
y=e^x(C_1\sin x+C_2\cos x)
$$
对应的特征根为
$$
\lambda_{1,2}=1\pm i.
$$

因此特征方程为
$$
(\lambda-1-i)(\lambda-1+i)=0,
$$
即
$$
\lambda^2-2\lambda+2=0.
$$

所以二阶常系数齐次线性微分方程为
$$
y''-2y'+2y=0.
$$

### 第 2 题
- 答案：$\dfrac{2}{3}$

记
$$
r=\sqrt{x^2+y^2+z^2}.
$$

在三维空间中
$$
\operatorname{div}(\operatorname{grad}r)
=\Delta r
=\frac{\partial^2 r}{\partial x^2}
+\frac{\partial^2 r}{\partial y^2}
+\frac{\partial^2 r}{\partial z^2}.
$$

因为
$$
\frac{\partial r}{\partial x}=\frac{x}{r},
\qquad
\frac{\partial^2 r}{\partial x^2}=\frac{r^2-x^2}{r^3},
$$
类似地
$$
\frac{\partial^2 r}{\partial y^2}=\frac{r^2-y^2}{r^3},\qquad
\frac{\partial^2 r}{\partial z^2}=\frac{r^2-z^2}{r^3}.
$$

故
$$
\Delta r=\frac{3r^2-(x^2+y^2+z^2)}{r^3}
=\frac{2r^2}{r^3}
=\frac{2}{r}.
$$

在点 $(1,-2,2)$ 处，
$$
r=\sqrt{1+4+4}=3,
$$
所以
$$
\operatorname{div}(\operatorname{grad} r)\big|_{(1,-2,2)}
=\frac{2}{3}.
$$

### 第 3 题
- 答案：$\displaystyle \int_1^2 dx\int_0^{1-x} f(x,y)\,dy$

原积分内层上限小于下限，先改写方向：
$$
\int_{-1}^{0}dy\int_2^{1-y}f(x,y)\,dx
=-\int_{-1}^{0}dy\int_{1-y}^{2}f(x,y)\,dx.
$$

对应区域为
$$
D=\{(x,y):-1\le y\le0,\ 1-y\le x\le2\}.
$$

换用 $x$ 作外层变量。由 $x\ge1-y$ 得 $y\ge1-x$，故
$$
1\le x\le2,\qquad 1-x\le y\le0.
$$

因此
$$
-\int_{-1}^{0}dy\int_{1-y}^{2}f(x,y)\,dx
=-\int_1^2dx\int_{1-x}^{0}f(x,y)\,dy.
$$

再把内层积分方向反过来，得
$$
\int_1^2 dx\int_0^{1-x} f(x,y)\,dy.
$$

### 第 4 题
- 答案：$\dfrac{1}{2}(A+2E)$

由
$$
A^2+A-4E=O
$$
可得
$$
A^2+A=4E.
$$

计算
$$
(A-E)(A+2E)=A^2+A-2E=2E.
$$

于是
$$
(A-E)\cdot \frac{1}{2}(A+2E)=E,
$$
所以
$$
(A-E)^{-1}=\frac{1}{2}(A+2E).
$$

### 第 5 题
- 答案：$\dfrac{1}{2}$

切比雪夫不等式为
$$
P\{|X-E(X)|\ge\varepsilon\}
\le \frac{D(X)}{\varepsilon^2}.
$$

题中 $D(X)=2$，取 $\varepsilon=2$，得
$$
P\{|X-E(X)|\ge2\}
\le \frac{2}{2^2}
=\frac{1}{2}.
$$

### 第 6 题
- 答案：D

从题图看，$y=f(x)$ 在 $y$ 轴左侧严格单调增加，因此当 $x<0$ 时有
$$
f'(x)>0.
$$
导函数图像在这一段应位于 $x$ 轴上方，可排除 A、C。

又在 $y$ 轴右侧靠近 $y$ 轴的一段，原函数图像仍是单调增加的，所以导函数在这一段也应为正，可进一步排除 B。

故选 D。

### 第 7 题
- 答案：C

题目只给出 $f_x'(0,0)$ 与 $f_y'(0,0)$ 存在，未说明 $f$ 在 $(0,0)$ 可微，因此不能直接写全微分，A 不一定成立。

若写曲面为
$$
F(x,y,z)=z-f(x,y)=0,
$$
则在该点的一个法向量应为
$$
(-f_x'(0,0),-f_y'(0,0),1)=(-3,-1,1),
$$
而不是 $(3,1,1)$，故 B 不对。

曲线
$$
\begin{cases}
z=f(x,y),\\
y=0
\end{cases}
$$
可参数化为
$$
x=x,\qquad y=0,\qquad z=f(x,0).
$$
在 $x=0$ 处的切向量为
$$
(1,0,f_x'(0,0))=(1,0,3).
$$

故选 C。

### 第 8 题
- 答案：B

若 $f$ 在 $0$ 处可导且 $f(0)=0$，则
$$
\lim_{x\to0}\frac{f(x)}{x}=f'(0).
$$

对选项 B，令
$$
x=1-e^h.
$$
当 $h\to0$ 时，$x\to0$，且
$$
1-e^h\sim -h.
$$
于是
$$
\frac{1}{h} f(1-e^h)
=\frac{f(x)}{x}\cdot\frac{x}{h}
\to f'(0)\cdot(-1),
$$
极限存在。

反过来，$x=1-e^h$ 在 $0$ 附近可反解为 $h=\ln(1-x)$，且 $\ln(1-x)\sim -x$。若
$$
\lim_{h\to0}\frac{1}{h} f(1-e^h)
$$
存在，则
$$
\frac{f(x)}{x}
=\frac{f(x)}{\ln(1-x)}\cdot\frac{\ln(1-x)}{x}
$$
也有极限，因此 $f'(0)$ 存在。

所以 B 是充分必要条件。

### 第 9 题
- 答案：A

矩阵 $A$ 是实对称矩阵，且所有元素均为 $1$。其特征值为
$$
4,\ 0,\ 0,\ 0.
$$

矩阵 $B$ 的特征值同样为
$$
4,\ 0,\ 0,\ 0.
$$

实对称矩阵可正交相似于对角矩阵，因此 $A$ 与 $B$ 都相似于
$$
\operatorname{diag}(4,0,0,0),
$$
从而二者相似。

又实对称矩阵合同的判别可用惯性指数。$A$ 与 $B$ 都只有一个正特征值、无负特征值、秩为 $1$，惯性指数相同，所以二者也合同。

故选 A。

### 第 10 题
- 答案：A

每次掷硬币不是正面就是反面，因此
$$
X+Y=n,
$$
即
$$
Y=n-X.
$$

于是
$$
D(Y)=D(n-X)=D(X),
$$
且
$$
\operatorname{Cov}(X,Y)
=\operatorname{Cov}(X,n-X)
=-\operatorname{Cov}(X,X)
=-D(X).
$$

相关系数为
$$
\rho_{XY}
=\frac{\operatorname{Cov}(X,Y)}{\sqrt{D(X)}\sqrt{D(Y)}}
=\frac{-D(X)}{D(X)}
=-1.
$$

故选 A。

### 第 11 题
- 答案：$-\dfrac{1}{2}\left(e^{-2x}\arctan e^x+e^{-x}+\arctan e^x\right)+C$

原积分为
$$
\int e^{-2x}\arctan e^x\,dx.
$$

分部积分，取
$$
u=\arctan e^x,\qquad dv=e^{-2x}\,dx.
$$
则
$$
du=\frac{e^x}{1+e^{2x}}\,dx,\qquad
v=-\frac{1}{2}e^{-2x}.
$$

所以
$$
\int e^{-2x}\arctan e^x\,dx
=-\frac{1}{2}e^{-2x}\arctan e^x
+\frac{1}{2}\int\frac{e^{-x}}{1+e^{2x}}\,dx.
$$

令 $u=e^x$，则后一个积分可写为
$$
\int\frac{e^{-x}}{1+e^{2x}}\,dx
=\int \frac{1}{u^2(1+u^2)}\,du
=\int\left(\frac{1}{u^2}-\frac{1}{1+u^2}\right)\,du.
$$

因此
$$
\int\frac{e^{-x}}{1+e^{2x}}\,dx
=-e^{-x}-\arctan e^x.
$$

代回得
$$
\int \frac{\arctan e^x}{e^{2x}}\,dx
=-\frac{1}{2}\left(e^{-2x}\arctan e^x+e^{-x}+\arctan e^x\right)+C.
$$

### 第 12 题
- 答案：$51$

设
$$
\varphi(x)=f(x,f(x,x)).
$$

由链式法则，
$$
\varphi'(x)
=f_1'(x,f(x,x))
+f_2'(x,f(x,x))\cdot \frac{d}{dx}f(x,x).
$$

而
$$
\frac{d}{dx}f(x,x)=f_1'(x,x)+f_2'(x,x).
$$

在 $x=1$ 处，题设给出
$$
f(1,1)=1,\qquad f_1'(1,1)=2,\qquad f_2'(1,1)=3.
$$
所以
$$
\varphi'(1)=2+3(2+3)=17.
$$

又
$$
\varphi(1)=f(1,f(1,1))=f(1,1)=1.
$$

因此
$$
\left.\frac{d}{dx}\varphi^3(x)\right|_{x=1}
=3\varphi^2(1)\varphi'(1)
=3\cdot1^2\cdot17
=51.
$$

### 第 13 题
- 答案：$\displaystyle f(x)=1+\sum_{n=1}^{\infty}\frac{2(-1)^n}{1-4n^2}x^{2n}\ (-1\le x\le1)$；$\displaystyle \sum_{n=1}^{\infty}\frac{(-1)^n}{1-4n^2}=\frac{\pi}{4}-\frac{1}{2}$

先展开
$$
\arctan x=\sum_{n=0}^{\infty}\frac{(-1)^n}{2n+1}x^{2n+1},
\qquad |x|<1.
$$

当 $x\ne0$ 时，
$$
f(x)=\frac{1+x^2}{x}\arctan x
=(1+x^2)\sum_{n=0}^{\infty}\frac{(-1)^n}{2n+1}x^{2n}.
$$

整理同次幂项，得
$$
f(x)
=1+\sum_{n=1}^{\infty}(-1)^n
\left(\frac{1}{2n+1}-\frac{1}{2n-1}\right)x^{2n}.
$$

即
$$
f(x)=1+\sum_{n=1}^{\infty}
\frac{2(-1)^n}{1-4n^2}x^{2n}.
$$

端点 $x=\pm1$ 处该级数也收敛，并与 $f$ 的相应单侧极限一致，因此展开可取
$$
-1\le x\le1.
$$

令 $x=1$，由于
$$
f(1)=2\arctan1=\frac{\pi}{2},
$$
得到
$$
\frac{\pi}{2}
=1+2\sum_{n=1}^{\infty}\frac{(-1)^n}{1-4n^2}.
$$

故
$$
\sum_{n=1}^{\infty}\frac{(-1)^n}{1-4n^2}
=\frac{\pi}{4}-\frac{1}{2}.
$$

### 第 14 题
- 答案：$-24$

记
$$
P=y^2-z^2,\quad Q=2z^2-x^2,\quad R=3x^2-y^2.
$$

由斯托克斯公式，
$$
I=\iint_S (\nabla\times(P,Q,R))\cdot\boldsymbol n\,dS,
$$
其中 $S$ 取平面 $x+y+z=2$ 上由 $L$ 围成的部分。题中从 $z$ 轴正向看去为逆时针，故取向上法向量。

计算旋度：
$$
\nabla\times(P,Q,R)
=(-2y-4z,\,-2z-6x,\,-2x-2y).
$$

平面写成
$$
z=2-x-y,
$$
向上的向量面积元为
$$
(-z_x,-z_y,1)\,dx\,dy=(1,1,1)\,dx\,dy.
$$

投影区域为
$$
D:\ |x|+|y|\le1.
$$

因此
$$
I=\iint_D[(-2y-4z)+(-2z-6x)+(-2x-2y)]\,dx\,dy.
$$

代入 $z=2-x-y$，化为
$$
I=-2\iint_D(x-y+6)\,dx\,dy.
$$

区域 $D$ 关于 $x$ 轴、$y$ 轴对称，故
$$
\iint_D x\,dx\,dy=\iint_D y\,dx\,dy=0.
$$
又 $D$ 是对角线长均为 $2$ 的菱形，面积为 $2$。所以
$$
I=-12\cdot2=-24.
$$

### 第 15 题
- 答案：(1) 存在且唯一；(2) $\displaystyle \lim_{x\to0}\theta(x)=\frac{1}{2}$

(1) 对任意 $x\in(-1,1)$ 且 $x\ne0$，在区间端点 $0$ 与 $x$ 之间对 $f$ 使用拉格朗日中值定理，存在 $\xi$ 介于 $0$ 与 $x$ 之间，使
$$
f(x)-f(0)=f'(\xi)x.
$$

令
$$
\xi=\theta(x)x.
$$
因 $\xi$ 介于 $0$ 与 $x$ 之间，故
$$
0<\theta(x)<1,
$$
于是
$$
f(x)=f(0)+xf'(\theta(x)x).
$$

由于 $f''(x)$ 在 $(-1,1)$ 内连续且处处不为 $0$，由介值性知 $f''$ 在该区间不变号，所以 $f'$ 严格单调。因此满足上式的 $\theta(x)$ 唯一。

(2) 由
$$
xf'(\theta(x)x)=f(x)-f(0)
$$
得
$$
f'(\theta(x)x)=\frac{f(x)-f(0)}{x}.
$$

两边减去 $f'(0)$，再除以 $x$：
$$
\frac{f'(\theta(x)x)-f'(0)}{x}
=\frac{f(x)-f(0)-f'(0)x}{x^2}.
$$

左边可写为
$$
\frac{f'(\theta(x)x)-f'(0)}{\theta(x)x}\,\theta(x).
$$
当 $x\to0$ 时，该式趋于
$$
f''(0)\lim_{x\to0}\theta(x).
$$

右边由洛必达法则或泰勒公式可得
$$
\lim_{x\to0}\frac{f(x)-f(0)-f'(0)x}{x^2}
=\frac{1}{2}f''(0).
$$

因为 $f''(0)\ne0$，所以
$$
\lim_{x\to0}\theta(x)=\frac{1}{2}.
$$

### 第 16 题
- 答案：$100$ 小时

侧面方程为
$$
z=h(t)-\frac{2(x^2+y^2)}{h(t)}.
$$
由 $z\ge0$ 得投影区域
$$
D:\ x^2+y^2\le\frac{1}{2}h^2(t).
$$

雪堆体积为
$$
V=\iint_D z\,dx\,dy.
$$
用极坐标计算：
$$
V=2\pi\int_0^{h/\sqrt{2}}\left(h-\frac{2r^2}{h}\right)r\,dr
=\frac{\pi}{4}h^3.
$$

侧面积为
$$
S=\iint_D\sqrt{1+z_x^2+z_y^2}\,dx\,dy.
$$
由于
$$
z_x=-\frac{4x}{h},\qquad z_y=-\frac{4y}{h},
$$
故
$$
S=2\pi\int_0^{h/\sqrt{2}}\sqrt{1+\frac{16r^2}{h^2}}\,r\,dr
=\frac{13\pi}{12}h^2.
$$

题设体积减少速率与侧面积成正比，比例系数为 $0.9$，所以
$$
\frac{dV}{dt}=-0.9S.
$$

代入 $V=\frac{\pi}{4}h^3$ 与 $S=\frac{13\pi}{12}h^2$，得
$$
\frac{3\pi}{4}h^2\frac{dh}{dt}
=-0.9\cdot\frac{13\pi}{12}h^2.
$$

因此
$$
\frac{dh}{dt}=-\frac{13}{10}.
$$

若 $h(0)=130$，则
$$
h(t)=130-\frac{13}{10}t.
$$
令 $h(t)=0$，得
$$
t=100.
$$

所以全部融化需要 $100$ 小时。

### 第 17 题
- 答案：$t_1^s+(-1)^{s+1}t_2^s\ne0$；等价地，$s$ 为偶数时 $t_1\ne\pm t_2$，$s$ 为奇数时 $t_1\ne -t_2$

因为每个 $\boldsymbol\beta_i$ 都是基础解系
$$
\boldsymbol\alpha_1,\ldots,\boldsymbol\alpha_s
$$
的线性组合，所以 $\boldsymbol\beta_1,\ldots,\boldsymbol\beta_s$ 都是方程组 $A\boldsymbol x=0$ 的解。

要使它们也构成基础解系，只需它们线性无关。

设
$$
k_1\boldsymbol\beta_1+\cdots+k_s\boldsymbol\beta_s=\boldsymbol0.
$$
代入 $\boldsymbol\beta_i$ 的表达式并按 $\boldsymbol\alpha_i$ 合并，得线性方程组
$$
\begin{cases}
t_1k_1+t_2k_s=0,\\
t_2k_1+t_1k_2=0,\\
\quad\vdots\\
t_2k_{s-1}+t_1k_s=0.
\end{cases}
$$

其系数矩阵是循环型矩阵
$$
\begin{pmatrix}
t_1&0&\cdots&0&t_2\\
t_2&t_1&\cdots&0&0\\
0&t_2&\ddots&0&0\\
\vdots&\vdots&\ddots&t_1&0\\
0&0&\cdots&t_2&t_1
\end{pmatrix},
$$
其行列式为
$$
t_1^s+(-1)^{s+1}t_2^s.
$$

因此 $\boldsymbol\beta_1,\ldots,\boldsymbol\beta_s$ 线性无关的充要条件为
$$
t_1^s+(-1)^{s+1}t_2^s\ne0.
$$

若 $s$ 为偶数，该条件等价于
$$
t_1^s-t_2^s\ne0,
$$
即 $t_1\ne\pm t_2$；若 $s$ 为奇数，该条件等价于
$$
t_1^s+t_2^s\ne0,
$$
即 $t_1\ne -t_2$。这与统一条件 $t_1^s+(-1)^{s+1}t_2^s\ne0$ 一致。

### 第 18 题
- 答案：$(1)\ \displaystyle B=\begin{pmatrix}0&0&0\\1&0&3\\0&1&-2\end{pmatrix}$；$(2)\ \det(A+E)=-4$

(1) 记
$$
P=(\boldsymbol x,A\boldsymbol x,A^2\boldsymbol x).
$$
题设向量组线性无关，故 $P$ 可逆。

有
$$
AP=(A\boldsymbol x,A^2\boldsymbol x,A^3\boldsymbol x).
$$
又题设
$$
A^3\boldsymbol x=3A\boldsymbol x-2A^2\boldsymbol x.
$$

所以在基
$$
(\boldsymbol x,A\boldsymbol x,A^2\boldsymbol x)
$$
下，$A\boldsymbol x,A^2\boldsymbol x,A^3\boldsymbol x$ 的坐标列分别为
$$
\begin{pmatrix}0\\1\\0\end{pmatrix},
\quad
\begin{pmatrix}0\\0\\1\end{pmatrix},
\quad
\begin{pmatrix}0\\3\\-2\end{pmatrix}.
$$

因此
$$
B=\begin{pmatrix}
0&0&0\\
1&0&3\\
0&1&-2
\end{pmatrix},
$$
并且
$$
AP=PB,\qquad A=PBP^{-1}.
$$

(2) 相似矩阵行列式相同，故
$$
\det(A+E)=\det(B+E).
$$

计算
$$
B+E=
\begin{pmatrix}
1&0&0\\
1&1&3\\
0&1&-1
\end{pmatrix}.
$$

于是
$$
\det(A+E)=\det(B+E)
=1\cdot
\begin{vmatrix}
1&3\\
1&-1
\end{vmatrix}
=-4.
$$

### 第 19 题
- 答案：$(1)\ \displaystyle P\{Y=m\mid X=n\}=\binom{n}{m} p^m(1-p)^{n-m}$；$(2)\ \displaystyle P\{X=n,Y=m\}=\binom{n}{m} p^m(1-p)^{n-m}\frac{\lambda^n}{n!}e^{-\lambda}$，$0\le m\le n$

(1) 在发车时有 $n$ 个乘客的条件下，每位乘客是否中途下车相互独立，且下车概率均为 $p$。因此 $Y\mid X=n$ 服从二项分布：
$$
P\{Y=m\mid X=n\}
=\binom{n}{m} p^m(1-p)^{n-m},
\qquad m=0,1,\ldots,n.
$$

(2) 由乘法公式，
$$
P\{X=n,Y=m\}
=P\{Y=m\mid X=n\}P\{X=n\}.
$$

又 $X$ 服从参数为 $\lambda$ 的泊松分布：
$$
P\{X=n\}=\frac{\lambda^n}{n!}e^{-\lambda},
\qquad n=0,1,2,\ldots.
$$

因此
$$
P\{X=n,Y=m\}
=\binom{n}{m} p^m(1-p)^{n-m}
\frac{\lambda^n}{n!}e^{-\lambda},
$$
其中
$$
n=0,1,2,\ldots,\qquad m=0,1,\ldots,n.
$$
其余情形概率为 $0$。

### 第 20 题
- 答案：$2(n-1)\sigma^2$

记
$$
\overline X_1=\frac{1}{n}\sum_{i=1}^n X_i,\qquad
\overline X_2=\frac{1}{n}\sum_{i=1}^n X_{n+i}.
$$
则
$$
\overline X=\frac{1}{2}(\overline X_1+\overline X_2).
$$

于是
$$
X_i+X_{n+i}-2\overline X
=(X_i-\overline X_1)+(X_{n+i}-\overline X_2).
$$

所以
$$
Y=\sum_{i=1}^n
\left[(X_i-\overline X_1)+(X_{n+i}-\overline X_2)\right]^2.
$$

展开后，
$$
E(Y)
=E\sum_{i=1}^n(X_i-\overline X_1)^2
+E\sum_{i=1}^n(X_{n+i}-\overline X_2)^2
+2E\sum_{i=1}^n(X_i-\overline X_1)(X_{n+i}-\overline X_2).
$$

前后两组样本相互独立，且中心化项期望为 $0$，因此交叉项期望为 $0$。

又样本方差
$$
S_1^2=\frac{1}{n-1}\sum_{i=1}^n(X_i-\overline X_1)^2
$$
是 $\sigma^2$ 的无偏估计，故
$$
E\sum_{i=1}^n(X_i-\overline X_1)^2=(n-1)\sigma^2.
$$
第二组同理。

因此
$$
E(Y)=2(n-1)\sigma^2.
$$
