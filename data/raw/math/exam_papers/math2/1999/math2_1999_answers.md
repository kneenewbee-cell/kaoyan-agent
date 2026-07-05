# Math 2 1999 Answers

资料类型：考研数学二答案解析
年份：1999
科目：数学二
校对状态：已按答案骨架与题面重新清洗整理。

## 答案速查

| 题号 | 题型 | 答案 |
|---|---|---|
| 1 | 填空题 | $2x+y-1=0$ |
| 2 | 填空题 | $1$ |
| 3 | 填空题 | $\dfrac12\ln(x^2-6x+13)+4\arctan\dfrac{x-3}{2}+C$ |
| 4 | 填空题 | $\dfrac{(1+\sqrt3)\pi}{12}$ |
| 5 | 填空题 | $y=C_1e^{2x}+C_2e^{-2x}+\dfrac14xe^{2x}$ |
| 6 | 选择题 | D |
| 7 | 选择题 | C |
| 8 | 选择题 | A |
| 9 | 选择题 | C |
| 10 | 选择题 | B |
| 11 | 解答题 | $-\dfrac12$ |
| 12 | 解答题 | $\dfrac{\pi}{4}+\dfrac12\ln 2$ |
| 13 | 解答题 | $y=\dfrac{x^2-1}{2}$ |
| 14 | 解答题 | $91500\text{ J}$ |
| 15 | 解答题 | 单调增区间为 $(-\infty,1)$ 与 $(3,+\infty)$，单调减区间为 $(1,3)$；在 $x=3$ 处取极小值 $\dfrac{27}{4}$；凹区间为 $(-\infty,0)$，凸区间为 $(0,1)$ 与 $(1,+\infty)$，拐点为 $(0,0)$；渐近线为 $x=1$ 与 $y=x+2$。 |
| 16 | 证明题 | 见解析。 |
| 17 | 解答题 | $y=e^x$ |
| 18 | 证明题 | 见解析。 |
| 19 | 解答题 | $X=\dfrac14\begin{pmatrix}1&1&0\\0&1&1\\1&0&1\end{pmatrix}$ |
| 20 | 解答题 | 当 $p\ne2$ 时，向量组线性无关，且
$$
\alpha=2\alpha_1+\frac{3p-4}{p-2}\alpha_2+\alpha_3-\frac{p-1}{p-2}\alpha_4.
$$
当 $p=2$ 时，向量组线性相关，秩为 $3$，可取一个极大线性无关组为 $\{\alpha_1,\alpha_2,\alpha_3\}$。 |

## 详细解析

### 第 1 题

- 答案：$2x+y-1=0$

点 $(0,1)$ 对应 $t=0$。由参数方程求导得
$$
\frac{dx}{dt}=e^t(\sin 2t+2\cos 2t),\qquad
\frac{dy}{dt}=e^t(\cos t-\sin t).
$$
当 $t=0$ 时，
$$
\left.\frac{dx}{dt}\right|_{t=0}=2,\qquad
\left.\frac{dy}{dt}\right|_{t=0}=1,
$$
故切线斜率为
$$
\frac{dy}{dx}=\frac{dy/dt}{dx/dt}=\frac12.
$$
于是法线斜率为 $-2$，过点 $(0,1)$ 的法线方程为
$$
y-1=-2x,
$$
即
$$
2x+y-1=0.
$$

### 第 2 题

- 答案：$1$

先由原方程求点值。令 $x=0$，得
$$
\ln y=0,
$$
故 $y(0)=1$。对
$$
\ln(x^2+y)=x^3y+\sin x
$$
两边关于 $x$ 求导，得
$$
\frac{2x+y'}{x^2+y}=3x^2y+x^3y'+\cos x.
$$
再代入 $x=0,\ y=1$，得到
$$
y'(0)=1.
$$

### 第 3 题

- 答案：$\dfrac12\ln(x^2-6x+13)+4\arctan\dfrac{x-3}{2}+C$

先配方：
$$
x^2-6x+13=(x-3)^2+4.
$$
又有
$$
x+5=\frac12(2x-6)+8.
$$
所以原积分化为
$$
\frac12\int\frac{2x-6}{x^2-6x+13}\,dx+8\int\frac{dx}{(x-3)^2+4}.
$$
第一项为
$$
\frac12\ln(x^2-6x+13).
$$
第二项为
$$
8\cdot \frac12\arctan\frac{x-3}{2}=4\arctan\frac{x-3}{2}.
$$
故结果为
$$
\frac12\ln(x^2-6x+13)+4\arctan\frac{x-3}{2}+C.
$$

### 第 4 题

- 答案：$\dfrac{(1+\sqrt3)\pi}{12}$

平均值公式为
$$
\bar y=\frac{1}{b-a}\int_a^b \frac{x^2}{\sqrt{1-x^2}}\,dx,
$$
其中
$$
a=\frac12,\qquad b=\frac{\sqrt3}{2}.
$$
令 $x=\sin t$，则 $dx=\cos t\,dt$，且
$$
t: \frac\pi6 \to \frac\pi3.
$$
原积分化为
$$
\int_{\pi/6}^{\pi/3} \sin^2 t\,dt
=\left[\frac t2-\frac{\sin 2t}{4}\right]_{\pi/6}^{\pi/3}
=\frac{\pi}{12}.
$$
又
$$
b-a=\frac{\sqrt3-1}{2},
$$
故平均值为
$$
\bar y=\frac{\pi/12}{(\sqrt3-1)/2}=\frac{(1+\sqrt3)\pi}{12}.
$$

### 第 5 题

- 答案：$y=C_1e^{2x}+C_2e^{-2x}+\dfrac14xe^{2x}$

对应齐次方程
$$
y''-4y=0
$$
的特征方程为
$$
r^2-4=0,
$$
解得 $r=\pm2$，故齐次通解为
$$
y_h=C_1e^{2x}+C_2e^{-2x}.
$$
由于右端为 $e^{2x}$，且与齐次解重复，设特解为
$$
y_p=Axe^{2x}.
$$
代入原方程可得 $4A=1$，于是 $A=\dfrac14$。所以通解为
$$
y=C_1e^{2x}+C_2e^{-2x}+\frac14xe^{2x}.
$$

### 第 6 题

- 答案：D

先看连续性。因为 $g(x)$ 有界，所以当 $x\to0^-$ 时，$x^2g(x)\to0$。又
$$
1-\cos x\sim \frac{x^2}{2},
$$
故当 $x\to0^+$ 时，
$$
\frac{1-\cos x}{\sqrt x}\sim \frac{x^2/2}{\sqrt x}=\frac12x^{3/2}\to0.
$$
于是 $f(0)=0$，且 $f$ 在 $0$ 处连续。再看导数：
$$
\lim_{x\to0^+}\frac{f(x)-f(0)}{x}
=\lim_{x\to0^+}\frac{1-\cos x}{x\sqrt x}=0.
$$
左侧有
$$
\lim_{x\to0^-}\frac{x^2g(x)-0}{x}
=\lim_{x\to0^-}xg(x)=0.
$$
左右导数都存在且相等，因此 $f$ 在 $0$ 处可导。

### 第 7 题

- 答案：C

当 $t\to0$ 时，
$$
\frac{\sin t}{t}\to1,\qquad (1+t)^{1/t}\to e.
$$
因此
$$
\alpha(x)\sim \int_0^{5x}1\,dt=5x,
$$
而
$$
\beta(x)\sim \int_0^{\sin x}e\,dt=e\sin x\sim ex.
$$
于是
$$
\frac{\alpha(x)}{\beta(x)}\to \frac{5}{e},
$$
该极限为非零常数，但不等于 $1$，所以二者同阶但不等价。

### 第 8 题

- 答案：A

若 $f$ 为奇函数，取
$$
F(x)=\int_0^x f(t)\,dt+C.
$$
则
$$
F(-x)=\int_0^{-x}f(t)\,dt+C
=-\int_0^x f(-u)\,du+C
=\int_0^x f(u)\,du+C
=F(x),
$$
故 $F$ 为偶函数，所以 A 正确。其余选项都可举反例否定：例如 $f(x)=x^2$ 为偶函数，但原函数 $\dfrac{x^3}{3}+1$ 不是奇函数；$f(x)=\cos x$ 是周期函数，但原函数未必仍为周期函数；单调性也不能直接由原函数继承。

### 第 9 题

- 答案：C

若 $x_n\to a$，则对任意 $\varepsilon\in(0,1)$，当然存在 $N$ 使 $|x_n-a|<\varepsilon<2\varepsilon$，所以它是必要条件。反过来，若题设条件成立，任取任意 $\eta>0$，取
$$
\varepsilon=\min\left\{\frac{\eta}{2},\frac12\right\},
$$
则 $\varepsilon\in(0,1)$，从而当 $n\ge N$ 时有
$$
|x_n-a|\le 2\varepsilon\le \eta.
$$
这正是 $x_n\to a$ 的定义，因此它也是充分条件。

### 第 10 题

- 答案：B

对行列式作初等变换可把它化简为一个二次多项式。计算后得到
$$
f(x)=5x(x-1).
$$
因此方程 $f(x)=0$ 的实根为
$$
x=0,\qquad x=1,
$$
共有 $2$ 个根，所以选 B。

### 第 11 题

- 答案：$-\dfrac12$

先化分子：
$$
\sqrt{1+\tan x}-\sqrt{1+\sin x}
=\frac{\tan x-\sin x}{\sqrt{1+\tan x}+\sqrt{1+\sin x}}.
$$
当 $x\to0$ 时，分母趋于 $2$，而
$$
\tan x=x+\frac{x^3}{3}+o(x^3),\qquad
\sin x=x-\frac{x^3}{6}+o(x^3),
$$
故
$$
\tan x-\sin x=\frac{x^3}{2}+o(x^3).
$$
于是分子为
$$
\frac{1}{2}\left(\frac{x^3}{2}+o(x^3)\right)=\frac{x^3}{4}+o(x^3).
$$
再看分母：
$$
\ln(1+x)=x-\frac{x^2}{2}+o(x^2),
$$
所以
$$
x\ln(1+x)-x^2
=x\left(x-\frac{x^2}{2}+o(x^2)\right)-x^2
=-\frac{x^3}{2}+o(x^3).
$$
因此原极限为
$$
\lim_{x\to0}\frac{x^3/4+o(x^3)}{-x^3/2+o(x^3)}=-\frac12.
$$

### 第 12 题

- 答案：$\dfrac{\pi}{4}+\dfrac12\ln 2$

用分部积分，取
$$
u=\arctan x,\qquad dv=\frac{dx}{x^2}.
$$
则
$$
du=\frac{dx}{1+x^2},\qquad v=-\frac1x.
$$
故原积分为
$$
\left.-\frac{\arctan x}{x}\right|_1^{+\infty}
+\int_1^{+\infty}\frac{1}{x(1+x^2)}\,dx.
$$
第一项等于
$$
0-\left(-\frac{\pi}{4}\right)=\frac{\pi}{4}.
$$
对第二项作部分分式分解：
$$
\frac{1}{x(1+x^2)}=\frac1x-\frac{x}{1+x^2}.
$$
因此
$$
\int_1^{+\infty}\frac{1}{x(1+x^2)}\,dx
=\left[\ln x-\frac12\ln(1+x^2)\right]_1^{+\infty}
=\frac12\ln2.
$$
综上
$$
\int_1^{+\infty}\frac{\arctan x}{x^2}\,dx
=\frac{\pi}{4}+\frac12\ln2.
$$

### 第 13 题

- 答案：$y=\dfrac{x^2-1}{2}$

将方程改写为
$$
x\frac{dy}{dx}=y+\sqrt{x^2+y^2}.
$$
由于 $x>0$，令
$$
y=ux,
$$
则
$$
\frac{dy}{dx}=u+x\frac{du}{dx},\qquad
\sqrt{x^2+y^2}=x\sqrt{1+u^2}.
$$
代入得
$$
x\left(u+x\frac{du}{dx}\right)=ux+x\sqrt{1+u^2},
$$
从而
$$
x\frac{du}{dx}=\sqrt{1+u^2}.
$$
分离变量积分：
$$
\int\frac{du}{\sqrt{1+u^2}}=\int\frac{dx}{x},
$$
即
$$
\operatorname{arsinh}u=\ln x+C.
$$
等价写成
$$
u+\sqrt{1+u^2}=Cx.
$$
由初值 $x=1,y=0$ 知 $u=0$，故 $C=1$，于是
$$
u+\sqrt{1+u^2}=x.
$$
解得
$$
u=\frac{x^2-1}{2x}.
$$
所以
$$
y=ux=\frac{x^2-1}{2}.
$$

### 第 14 题

- 答案：$91500\text{ J}$

把总功分成三部分：抓斗自重、缆绳重力、污泥重力。

1. 抓斗自重做功
$$
W_1=400\times30=12000\text{ J}.
$$

2. 缆绳做功。设抓斗已上升 $x$ 米，则井中尚有 $30-x$ 米缆绳，其重量为 $50(30-x)$ N，因此
$$
W_2=\int_0^{30}50(30-x)\,dx=22500\text{ J}.
$$

3. 污泥做功。提升速度为 $3\text{ m/s}$，故总提升时间为
$$
T=\frac{30}{3}=10\text{ s}.
$$
设经过 $t$ 秒时，污泥重量为
$$
2000-20t.
$$
此时位移微元为 $dx=3dt$，故污泥做功
$$
W_3=\int_0^{10}(2000-20t)\cdot3\,dt=57000\text{ J}.
$$
于是总功为
$$
W=W_1+W_2+W_3=12000+22500+57000=91500\text{ J}.
$$

### 第 15 题

- 答案：单调增区间为 $(-\infty,1)$ 与 $(3,+\infty)$，单调减区间为 $(1,3)$；在 $x=3$ 处取极小值 $\dfrac{27}{4}$；凹区间为 $(-\infty,0)$，凸区间为 $(0,1)$ 与 $(1,+\infty)$，拐点为 $(0,0)$；渐近线为 $x=1$ 与 $y=x+2$。

定义域为 $(-\infty,1)\cup(1,+\infty)$。先求导：
$$
y'=\frac{x^2(x-3)}{(x-1)^3}.
$$
据此讨论符号：在 $(-\infty,1)$ 上 $y'>0$，在 $(1,3)$ 上 $y'<0$，在 $(3,+\infty)$ 上 $y'>0$，所以函数在 $(-\infty,1)$、$(3,+\infty)$ 单调增加，在 $(1,3)$ 单调减少。故 $x=3$ 处取极小值
$$
y(3)=\frac{27}{4}.
$$
再求二阶导数：
$$
y''=\frac{6x}{(x-1)^4}.
$$
因为 $(x-1)^4>0$，故 $y''$ 的符号由 $x$ 决定，于是在 $(-\infty,0)$ 上凹，在 $(0,1)$ 与 $(1,+\infty)$ 上凸，拐点为
$$
(0,0).
$$
最后求渐近线。显然当 $x\to1$ 时，$y\to+\infty$，故有垂直渐近线 $x=1$。又作多项式除法：
$$
\frac{x^3}{(x-1)^2}=x+2+\frac{3x-2}{(x-1)^2},
$$
故当 $x\to\pm\infty$ 时
$$
y-(x+2)\to0,
$$
所以斜渐近线为
$$
y=x+2.
$$

### 第 16 题

- 答案：见解析。

在 $x=0$ 处分别对 $f(1)$ 与 $f(-1)$ 使用带拉格朗日余项的泰勒公式。存在 $\xi_1\in(0,1)$、$\xi_2\in(-1,0)$，使得
$$
f(1)=f(0)+f'(0)+\frac{f''(0)}{2}+\frac{f'''(\xi_1)}{6},
$$
$$
f(-1)=f(0)-f'(0)+\frac{f''(0)}{2}-\frac{f'''(\xi_2)}{6}.
$$
由题设 $f(-1)=0$，$f(1)=1$，$f'(0)=0$，化为
$$
1=f(0)+\frac{f''(0)}{2}+\frac{f'''(\xi_1)}{6},
$$
$$
0=f(0)+\frac{f''(0)}{2}-\frac{f'''(\xi_2)}{6}.
$$
两式相减得
$$
1=\frac{f'''(\xi_1)+f'''(\xi_2)}{6}.
$$
于是
$$
\frac{f'''(\xi_1)+f'''(\xi_2)}{2}=3.
$$
由于 $f'''$ 在区间 $[\xi_2,\xi_1]\subset(-1,1)$ 上连续，所以由介值定理知，存在 $\xi\in(\xi_2,\xi_1)\subset(-1,1)$，使得
$$
f'''(\xi)=3.
$$
证毕。

### 第 17 题

- 答案：$y=e^x$

点 $P(x,y)$ 处的切线方程为
$$
Y-y=y'(x)(X-x).
$$
令 $Y=0$，得切线与 $x$ 轴交点的横坐标为
$$
X=x-\frac{y}{y'}.
$$
故三角形面积
$$
S_1=\frac12\cdot y\cdot\frac{y}{y'}=\frac{y^2}{2y'}.
$$
又
$$
S_2=\int_0^x y(t)\,dt.
$$
由题设
$$
2S_1-S_2=1
$$
得
$$
\frac{y^2}{y'}-\int_0^x y(t)\,dt=1.
$$
对 $x$ 求导并化简，得
$$
y'^2=yy''.
$$
令 $p=y'$，视 $p$ 为 $y$ 的函数，则
$$
y''=p\frac{dp}{dy}.
$$
代入可得
$$
p^2=yp\frac{dp}{dy}.
$$
由于 $p=y'>0$，可约去 $p$，得
$$
\frac{dp}{p}=\frac{dy}{y}.
$$
积分后有
$$
p=Cy,
$$
即
$$
y'=Cy.
$$
把 $x=0$ 代入题设关系：此时 $S_2=0$，且 $2S_1=1$，于是 $S_1=\dfrac12$。又 $y(0)=1$，故
$$
\frac{1}{2y'(0)}=\frac12,
$$
从而 $y'(0)=1$，所以 $C=1$。于是
$$
y'=y,\qquad y(0)=1,
$$
解得
$$
y=e^x.
$$

### 第 18 题

- 答案：见解析。

先求相邻两项之差：
$$
a_{n+1}-a_n=f(n+1)-\int_n^{n+1}f(x)\,dx.
$$
由于 $f$ 在 $[0,+\infty)$ 上单调减少，对任意 $x\in[n,n+1]$ 有
$$
f(n+1)\le f(x)\le f(n).
$$
积分得
$$
f(n+1)\le \int_n^{n+1}f(x)\,dx\le f(n).
$$
于是
$$
a_{n+1}-a_n\le0,
$$
故 $\{a_n\}$ 单调减少。另一方面，由
$$
\int_1^n f(x)\,dx\le \sum_{k=1}^{n-1}f(k)
$$
可得
$$
a_n=\sum_{k=1}^n f(k)-\int_1^n f(x)\,dx\ge f(n)\ge0.
$$
因此 $\{a_n\}$ 有下界 $0$。数列单调减少且有下界，所以极限存在。

### 第 19 题

- 答案：$X=\dfrac14\begin{pmatrix}1&1&0\\0&1&1\\1&0&1\end{pmatrix}$

先求 $|A|$。计算得
$$
|A|=4.
$$
因此
$$
A^*=|A|A^{-1}=4A^{-1}.
$$
代入题设：
$$
4A^{-1}X=A^{-1}+2X.
$$
两边左乘 $A$，得到
$$
4X=E+2AX,
$$
即
$$
2(2E-A)X=E.
$$
所以
$$
X=\frac12(2E-A)^{-1}.
$$
而
$$
2E-A=\begin{pmatrix}
1&-1&1\\
1&1&-1\\
-1&1&1
\end{pmatrix},
$$
其逆矩阵为
$$
(2E-A)^{-1}
=\begin{pmatrix}
\frac12&\frac12&0\\
0&\frac12&\frac12\\
\frac12&0&\frac12
\end{pmatrix}.
$$
故
$$
X=\frac14\begin{pmatrix}
1&1&0\\
0&1&1\\
1&0&1
\end{pmatrix}.
$$

### 第 20 题

- 答案：当 $p\ne2$ 时，向量组线性无关，且
$$
\alpha=2\alpha_1+\frac{3p-4}{p-2}\alpha_2+\alpha_3-\frac{p-1}{p-2}\alpha_4.
$$
当 $p=2$ 时，向量组线性相关，秩为 $3$，可取一个极大线性无关组为 $\{\alpha_1,\alpha_2,\alpha_3\}$。

注意到
$$
\alpha_4-2\alpha_2=(0,0,0,p-2)^T.
$$
因此当 $p=2$ 时，$\alpha_4=2\alpha_2$，向量组线性相关；当 $p\ne2$ 时，第四个向量不能由前三个向量线性表示，从而向量组线性无关。

下面求 $\alpha$ 的表示。设
$$
\alpha=x_1\alpha_1+x_2\alpha_2+x_3\alpha_3+x_4\alpha_4.
$$
按分量列方程组：
$$
\begin{cases}
x_1-x_2+3x_3-2x_4=4,\\
x_1-3x_2+2x_3-6x_4=1,\\
x_1+5x_2-x_3+10x_4=6,\\
3x_1+x_2+(p+2)x_3+px_4=10.
\end{cases}
$$
由前三式可先解得
$$
x_1=2,\qquad x_3=1,\qquad x_2=1-2x_4.
$$
代入第四式，得到
$$
(p-2)x_4=1-p,
$$
故当 $p\ne2$ 时
$$
x_4=-\frac{p-1}{p-2},\qquad
x_2=\frac{3p-4}{p-2}.
$$
于是
$$
\alpha=2\alpha_1+\frac{3p-4}{p-2}\alpha_2+\alpha_3-\frac{p-1}{p-2}\alpha_4.
$$
当 $p=2$ 时，已有 $\alpha_4=2\alpha_2$，所以向量组秩至多为 $3$；而 $\alpha_1,\alpha_2,\alpha_3$ 线性无关，因此秩恰为 $3$，一个极大线性无关组可取
$$
\{\alpha_1,\alpha_2,\alpha_3\}.
$$
