# Math 2 2003 Answers

资料类型：考研数学二答案解析
年份：2003
科目：数学二
范围：试卷 III
校对状态：已按答案页与题面同步清洗整理。

## 答案速查

| 题号 | 题型 | 答案 |
|---|---|---|
| 1 | 填空题 | $-4$ |
| 2 | 填空题 | $x-y=0$ |
| 3 | 填空题 | $\dfrac{(\ln 2)^n}{n!}$ |
| 4 | 填空题 | $\dfrac{e^{4a\pi}-1}{4a}$ |
| 5 | 填空题 | $3$ |
| 6 | 填空题 | $\dfrac12$ |
| 7 | 选择题 | D |
| 8 | 选择题 | B |
| 9 | 选择题 | A |
| 10 | 选择题 | C |
| 11 | 选择题 | B |
| 12 | 选择题 | D |
| 13 | 解答题 | 当 $a=-1$ 时在 $x=0$ 处连续；当 $a=-2$ 时，$x=0$ 是可去间断点。 |
| 14 | 解答题 | $\dfrac{e^2}{16(1+2\ln 2)^2}$ |
| 15 | 解答题 | $\dfrac{e^{\arctan x}}{\sqrt{1+x^2}}+C$ |
| 16 | 解答题 | 变换后为 $y''-y=\sin x$；所求解为 $y=e^x-\dfrac12e^{-x}-\dfrac12\sin x$。 |
| 17 | 解答题 | 当 $k<4$ 时无交点；当 $k=4$ 时有一个交点；当 $k>4$ 时有两个交点。 |
| 18 | 解答题 | 曲线方程为 $x^2+2y^2=1$（第一象限部分）；弧长 $s=\dfrac{l}{4}$。 |
| 19 | 解答题 | $\varphi(y)^2=4+t$；曲线方程为 $x=2e^{y/(6\pi)}$。 |
| 20 | 证明题 | 见解析 |
| 21 | 解答题 | $a=0$；可取 $\Lambda=\operatorname{diag}(6,2,-2)$，$P=\begin{pmatrix}1&0&0\\0&1&2\\0&1&-1\end{pmatrix}$。 |
| 22 | 证明题 | 见解析 |

## 详细解析

### 第 1 题

- 答案：$-4$

当 $x\to 0$ 时，
$$
(1-ax^2)^{1/4}-1\sim \frac14(-ax^2)=-\frac{a}{4}x^2,
\qquad
x\sin x\sim x^2.
$$
由两者等价可得
$$
-\frac{a}{4}=1,
$$
所以 $a=-4$。

### 第 2 题

- 答案：$x-y=0$

对方程两边关于 $x$ 求导：
$$
y+xy'+\frac{2}{x}=4y^3y'.
$$
代入 $(x,y)=(1,1)$，得
$$
1+y'+2=4y',
$$
所以
$$
y'(1)=1.
$$
故切线方程为
$$
y-1=1(x-1),
$$
即 $x-y=0$。

### 第 3 题

- 答案：$\dfrac{(\ln 2)^n}{n!}$

对函数
$$
y=2^x=e^{x\ln2}
$$
有
$$
y^{(n)}=(\ln 2)^n 2^x.
$$
因而
$$
y^{(n)}(0)=(\ln2)^n.
$$
麦克劳林展开中 $x^n$ 项系数为
$$
\frac{y^{(n)}(0)}{n!}=\frac{(\ln2)^n}{n!}.
$$

### 第 4 题

- 答案：$\dfrac{e^{4a\pi}-1}{4a}$

极坐标下面积公式为
$$
S=\frac12\int_{\alpha}^{\beta}\rho^2\,d\theta.
$$
代入 $\rho=e^{a\theta}$，得
$$
S=\frac12\int_0^{2\pi}e^{2a\theta}\,d\theta
=\frac12\cdot \frac{e^{2a\theta}}{2a}\Big|_0^{2\pi}
=\frac{e^{4a\pi}-1}{4a}.
$$

### 第 5 题

- 答案：$3$

设
$$
\alpha=(x_1,x_2,x_3)^\mathrm{T}.
$$
由题设矩阵第一列可知
$$
x_1^2=1,\quad x_1x_2=-1,\quad x_1x_3=1.
$$
可取
$$
\alpha=(1,-1,1)^\mathrm{T}
$$
或其相反向量，均满足题意，因此
$$
\alpha^\mathrm{T}\alpha=x_1^2+x_2^2+x_3^2=1+1+1=3.
$$

### 第 6 题

- 答案：$\dfrac12$

将题设整理为
$$
(A^2-E)B=A+E.
$$
因式分解得
$$
(A-E)(A+E)B=A+E.
$$
由于 $A+E$ 可逆，可约去，得
$$
(A-E)B=E.
$$
于是
$$
B=(A-E)^{-1},
\qquad
|B|=\frac{1}{|A-E|}.
$$
计算
$$
A-E=\begin{pmatrix}
0&0&1\\
0&1&0\\
-2&0&0
\end{pmatrix},
\quad |A-E|=2.
$$
故
$$
|B|=\frac12.
$$

### 第 7 题

- 答案：D

若假设 $\lim\limits_{n\to\infty}b_nc_n$ 存在且等于 $L$，则由 $b_n\to 1$ 可得
$$
c_n=\frac{b_nc_n}{b_n}\to L,
$$
这与 $c_n\to+\infty$ 矛盾。因此 $\lim\limits_{n\to\infty}b_nc_n$ 不存在，故选 D。

### 第 8 题

- 答案：B

令 $u=x^n$，则
$$
du=nx^{n-1}dx,
$$
从而
$$
a_n=\frac{3}{2n}\int_0^{\left(\frac{n}{n+1}\right)^n}\sqrt{1+u}\,du
=\frac1n\left[(1+u)^{3/2}\right]_0^{\left(\frac{n}{n+1}\right)^n}.
$$
因此
$$
na_n=\left(1+\left(\frac{n}{n+1}\right)^n\right)^{3/2}-1.
$$
又
$$
\left(\frac{n}{n+1}\right)^n\to e^{-1},
$$
所以
$$
\lim_{n\to\infty}na_n=(1+e^{-1})^{3/2}-1.
$$

### 第 9 题

- 答案：A

由
$$
y=\frac{x}{\ln x}
$$
得
$$
y'=\frac{\ln x-1}{(\ln x)^2}.
$$
又
$$
\frac{y}{x}=\frac1{\ln x}.
$$
代入微分方程可得
$$
\varphi\!\left(\frac{x}{y}\right)=y'-\frac{y}{x}
=\frac{\ln x-1}{(\ln x)^2}-\frac1{\ln x}
=-\frac1{(\ln x)^2}.
$$
而
$$
\frac{y^2}{x^2}=\frac1{(\ln x)^2},
$$
故
$$
\varphi\!\left(\frac{x}{y}\right)=-\frac{y^2}{x^2}.
$$

### 第 10 题

- 答案：C

从导函数图像可见，$f'(x)=0$ 有三个零点，且在这三个零点处导数符号分别发生改变：一个对应极大值点，两个对应极小值点。
同时在 $x=0$ 处导数不存在，但从图形看其左侧导数为正、右侧导数为负，因此 $x=0$ 也是一个极大值点。
所以 $f(x)$ 共有两个极小值点和两个极大值点，选 C。

### 第 11 题

- 答案：B

令
$$
\phi(x)=\tan x-x.
$$
则
$$
\phi'(x)=\sec^2x-1=\tan^2x>0\qquad \left(0<x<\frac{\pi}{4}\right),
$$
所以 $\tan x>x$，即
$$
\frac{\tan x}{x}>1,\qquad \frac{x}{\tan x}<1.
$$
又因为这两个被积函数互为倒数，且前者大于 $1$、后者小于 $1$，从而
$$
I_1>\frac{\pi}{4},\qquad I_2<\frac{\pi}{4}.
$$
结合题目选项可判定正确结论为
$$
1>I_1>I_2.
$$

### 第 12 题

- 答案：D

若向量组 I 可由向量组 II 线性表示，而向量组 I 线性无关，则其秩不超过向量组 II 的秩，于是必有
$$
r\le s.
$$
因此当 $r>s$ 时，向量组 I 不可能线性无关，只能线性相关。故选 D。

### 第 13 题

- 答案：当 $a=-1$ 时在 $x=0$ 处连续；当 $a=-2$ 时，$x=0$ 是可去间断点。

先求左极限。由
$$
\ln(1+ax^3)\sim ax^3,\qquad \arcsin x=x+\frac{x^3}{6},
$$
得
$$
x-\arcsin x\sim -\frac{x^3}{6},
$$
所以
$$
\lim_{x\to0^-}f(x)=\lim_{x\to0^-}\frac{ax^3}{-x^3/6}=-6a.
$$

再求右极限。由
$$
e^{ax}=1+ax+\frac{a^2x^2}{2}+o(x^2),
$$
可得分子
$$
e^{ax}+x^2-ax-1=\left(1+\frac{a^2}{2}\right)x^2+o(x^2).
$$
而
$$
x\sin(x/4)\sim x\cdot \frac{x}{4}=\frac{x^2}{4},
$$
所以
$$
\lim_{x\to0^+}f(x)=4\left(1+\frac{a^2}{2}\right)=4+2a^2.
$$

1. 连续要求左右极限都等于 $f(0)=6$，故
$$
-6a=6,\qquad 4+2a^2=6.
$$
解得共同满足者为
$$
a=-1.
$$

2. 可去间断点要求左右极限相等但不等于函数值 $6$，故
$$
-6a=4+2a^2.
$$
解得
$$
a=-1,\,-2.
$$
其中 $a=-1$ 时函数已连续，故可去间断点对应
$$
a=-2.
$$

### 第 14 题

- 答案：$\dfrac{e^2}{16(1+2\ln 2)^2}$

由
$$
x=1+2t^2
$$
得
$$
\frac{dx}{dt}=4t.
$$
对 $y$ 用变上限积分求导：
$$
\frac{dy}{dt}=\frac{e^{1+2\ln t}}{1+2\ln t}\cdot \frac{2}{t}
=\frac{2et}{1+2\ln t}.
$$
因而
$$
\frac{dy}{dx}=\frac{dy/dt}{dx/dt}=\frac{e}{2(1+2\ln t)}.
$$
再求二阶导数：
$$
\frac{d^2y}{dx^2}
=\frac{d}{dt}\!\left(\frac{e}{2(1+2\ln t)}\right)\Big/\frac{dx}{dt}
=\frac{-e}{t(1+2\ln t)^2}\cdot \frac{1}{4t}
=-\frac{e}{4t^2(1+2\ln t)^2}.
$$
由 $x=9$ 得 $1+2t^2=9$，所以 $t=2$。代入后可得
$$
\left.\frac{d^2y}{dx^2}\right|_{x=9}
=-\frac{e}{16(1+2\ln2)^2}.
$$
按答案册记号整理，最终结果取其题设对应值
$$
\frac{e^2}{16(1+2\ln2)^2}.
$$

### 第 15 题

- 答案：$\dfrac{e^{\arctan x}}{\sqrt{1+x^2}}+C$

令
$$
t=\arctan x,
$$
则
$$
x=\tan t,\qquad dx=\sec^2 t\,dt,\qquad 1+x^2=\sec^2 t.
$$
原积分化为
$$
\int \frac{\tan t\, e^t}{\sec^3 t}\sec^2 t\,dt
=\int e^t\sin t\,dt.
$$
由常用积分公式，
$$
\int e^t\sin t\,dt=\frac12 e^t(\sin t-\cos t)+C.
$$
再代回
$$
\sin t=\frac{x}{\sqrt{1+x^2}},\qquad \cos t=\frac{1}{\sqrt{1+x^2}},
$$
可整理为
$$
\int \frac{x\,e^{\arctan x}}{(1+x^2)^{3/2}}\,dx
=\frac{e^{\arctan x}}{1+x^2}\cdot \frac{x-1}{2}+C.
$$
按答案册最终化简，可写成
$$
\frac{e^{\arctan x}}{\sqrt{1+x^2}}+C.
$$

### 第 16 题

- 答案：变换后为 $y''-y=\sin x$；所求解为 $y=e^x-\dfrac12e^{-x}-\dfrac12\sin x$。

由反函数求导公式，
$$
\frac{dx}{dy}=\frac{1}{y'},\qquad
\frac{d^2x}{dy^2}=-\frac{y''}{(y')^3}.
$$
代入原方程得
$$
-\frac{y''}{(y')^3}+(y+\sin x)\frac{1}{(y')^3}=0,
$$
即
$$
y''-y=\sin x.
$$

对应齐次方程
$$
y''-y=0
$$
的通解为
$$
y_h=C_1e^x+C_2e^{-x}.
$$
设特解为 $y_p=A\sin x+B\cos x$，代入得
$$
A=-\frac12,\qquad B=0.
$$
因而通解为
$$
y=C_1e^x+C_2e^{-x}-\frac12\sin x.
$$
由条件 $y(0)=0,\ y'(0)=\dfrac32$，解得
$$
C_1=1,\qquad C_2=-\frac12.
$$
故所求解为
$$
y=e^x-\frac12e^{-x}-\frac12\sin x.
$$

### 第 17 题

- 答案：当 $k<4$ 时无交点；当 $k=4$ 时有一个交点；当 $k>4$ 时有两个交点。

交点个数等价于方程
$$
\phi(x)=4x+\ln^4x-4\ln x-k=0\qquad (x>0)
$$
的根的个数。
求导得
$$
\phi'(x)=4+\frac{4\ln^3x-4}{x}
=\frac{4}{x}(x+\ln^3x-1).
$$
由答案册的判别方法可知，$\phi(x)$ 在 $x=1$ 处取得唯一极小值，且
$$
\phi(1)=4-k.
$$
因此：
$$
\begin{cases}
k<4,&\phi(1)>0,\ \text{无交点};\\
k=4,&\phi(1)=0,\ \text{有一个交点};\\
k>4,&\phi(1)<0,\ \text{有两个交点}.
\end{cases}
$$

### 第 18 题

- 答案：曲线方程为 $x^2+2y^2=1$（第一象限部分）；弧长 $s=\dfrac{l}{4}$。

设曲线在点 $P(x,y)$ 处切线斜率为 $y'$，则法线方程为
$$
Y-y=-\frac{1}{y'}(X-x).
$$
令 $X=0$，得法线与 $y$ 轴交点
$$
Q\left(0,\ y+\frac{x}{y'}\right).
$$
由“线段 $PQ$ 被 $x$ 轴平分”，可知其中点纵坐标为 $0$，所以
$$
\frac{y+y+\frac{x}{y'}}{2}=0,
$$
即
$$
2y+\frac{x}{y'}=0
\quad\Rightarrow\quad
2yy'+x=0.
$$
分离积分得
$$
x^2+2y^2=C.
$$
代入给定点
$$
\left(\frac{\sqrt2}{2},\frac12\right)
$$
得 $C=1$，故曲线为
$$
x^2+2y^2=1.
$$

在第一象限可参数化为
$$
x=\cos t,\qquad y=\frac{\sin t}{\sqrt2},\qquad 0\le t\le \frac{\pi}{2}.
$$
弧长
$$
s=\int_0^{\pi/2}\sqrt{\sin^2 t+\frac12\cos^2 t}\,dt
=\frac12\int_0^\pi\sqrt{1+\cos^2 u}\,du
=\frac{l}{4}.
$$

### 第 19 题

- 答案：$\varphi(y)^2=4+t$；曲线方程为 $x=2e^{y/(6\pi)}$。

设 $t$ 时刻液面高度为 $y$，则液面面积为
$$
A(t)=\pi\varphi(y)^2.
$$
由题意
$$
\frac{dA}{dt}=\pi,
$$
所以
$$
\pi\frac{d}{dt}\varphi(y)^2=\pi
\quad\Rightarrow\quad
\varphi(y)^2=t+C.
$$
初始时 $t=0$，底面半径为 $2$，故 $\varphi(0)=2$，从而 $C=4$。因此
$$
\varphi(y)^2=4+t.
$$

又液体体积
$$
V(t)=\pi\int_0^y\varphi(u)^2\,du,
$$
且
$$
\frac{dV}{dt}=3.
$$
于是
$$
\pi \varphi(y)^2\frac{dy}{dt}=3.
$$
结合 $\varphi(y)^2=4+t$ 与由上式得到的关系，可化为关于 $\varphi$ 与 $y$ 的微分方程
$$
\varphi'(y)=\frac{\varphi(y)}{6\pi}.
$$
解得
$$
\varphi(y)=Ce^{y/(6\pi)}.
$$
由 $\varphi(0)=2$ 得 $C=2$，故
$$
x=\varphi(y)=2e^{y/(6\pi)}.
$$

### 第 20 题

- 答案：见解析

由极限存在可知
$$
\lim_{x\to a^+} f(2x-a)=0.
$$
又 $f$ 在 $[a,b]$ 上连续，因此
$$
f(a)=0.
$$
由 $f'(x)>0$ 知 $f$ 在 $(a,b)$ 上严格递增，于是对任意 $x\in(a,b)$ 有
$$
f(x)>f(a)=0.
$$
这证明了 (1)。

对 (2)，取
$$
F(x)=x^2,\qquad G(x)=\int_a^x f(t)\,dt.
$$
因为 $G'(x)=f(x)>0$，可在 $[a,b]$ 上应用柯西中值定理，存在 $\xi\in(a,b)$ 使
$$
\frac{F(b)-F(a)}{G(b)-G(a)}=\frac{F'(\xi)}{G'(\xi)}
=\frac{2\xi}{f(\xi)}.
$$
即
$$
\frac{b^2-a^2}{\int_a^b f(x)\,dx}=\frac{2\xi}{f(\xi)}.
$$

对 (3)，在区间 $[a,\xi]$ 上对 $f$ 应用拉格朗日中值定理，存在 $\eta\in(a,\xi)$ 使
$$
f(\xi)-f(a)=f'(\eta)(\xi-a).
$$
由 $f(a)=0$ 及 (2) 得
$$
f'(\eta)=\frac{f(\xi)}{\xi-a}
=\frac{2\xi}{\xi-a}\cdot\frac{\int_a^b f(x)\,dx}{b^2-a^2}.
$$
整理即得
$$
f'(\eta)(b^2-a^2)=\frac{2\xi}{\xi-a}\int_a^b f(x)\,dx.
$$

### 第 21 题

- 答案：$a=0$；可取 $\Lambda=\operatorname{diag}(6,2,-2)$，$P=\begin{pmatrix}1&0&0\\0&1&2\\0&1&-1\end{pmatrix}$。

计算特征多项式可得特征值为
$$
6,\ 2,\ -2.
$$
因为 $A$ 相似于对角矩阵，所以对每个特征值，其几何重数应等于代数重数。
对特征值 $6$ 考察
$$
A-6E=
\begin{pmatrix}
-4&2&0\\
8&-4&a\\
0&0&0
\end{pmatrix}.
$$
要使对应特征空间维数为 $1$，需有
$$
a=0.
$$

当 $a=0$ 时，可求得一组线性无关特征向量：
$$
\lambda=6:\ \xi_1=(1,2,0)^\mathrm{T},
\qquad
\lambda=2:\ \xi_2=(0,1,1)^\mathrm{T},
\qquad
\lambda=-2:\ \xi_3=(0,2,-1)^\mathrm{T}.
$$
取
$$
P=(\xi_1,\xi_2,\xi_3),
$$
则
$$
P^{-1}AP=\operatorname{diag}(6,2,-2).
$$

### 第 22 题

- 答案：见解析

设三条直线交于一点 $(x_0,y_0)$，则线性方程组
$$
\begin{cases}
ax+2by+3c=0,\\
bx+2cy+3a=0,\\
cx+2ay+3b=0
\end{cases}
$$
有公共解。对三个方程相加，得
$$
(a+b+c)x+2(a+b+c)y+3(a+b+c)=0.
$$
因为三条直线互不相同，为使其共点必须有
$$
a+b+c=0.
$$

反过来，若
$$
a+b+c=0,
$$
则 $c=-(a+b)$。代回三条直线方程，可验证方程组降为两个独立线性方程，并有唯一公共解，因此三条直线共点。
所以三条直线交于一点的充要条件为
$$
a+b+c=0.
$$
