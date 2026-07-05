# Math 2 1994 Answers

资料类型：考研数学二答案解析
年份：1994
科目：数学二
范围：试卷 III
校对状态：已按答案页图像清洗并与题面同步。

## 答案速查

| 题号 | 题型 | 答案 |
|---|---|---|
| 1 | 填空题 | $-2$ |
| 2 | 填空题 | $\dfrac{(t+1)(6t+5)}{t}$ |
| 3 | 填空题 | $-3\sin 3x\,f(\cos 3x)$ |
| 4 | 填空题 | $\dfrac{1}{2}(x^2-1)e^{x^2}+C$ |
| 5 | 填空题 | $(x-4)y^4=Cx$ |
| 6 | 选择题 | A |
| 7 | 选择题 | B |
| 8 | 选择题 | C |
| 9 | 选择题 | B |
| 10 | 选择题 | D |
| 11 | 解答题 | $y''=\dfrac{f''}{(1-f')^3}$ |
| 12 | 解答题 | $\dfrac{3\pi}{32}$ |
| 13 | 解答题 | $e^4$ |
| 14 | 解答题 | $\dfrac{1}{8}\left[\ln(1-\cos x)-\ln(1+\cos x)+\dfrac{2}{1+\cos x}\right]+C$ |
| 15 | 解答题 | 见解析。 |
| 16 | 解答题 | $k\le0$ 或 $k=\dfrac{2\sqrt{3}}{9}$ |
| 17 | 解答题 | 函数在 $(-\infty,0)\cup(2,+\infty)$ 上单调增加，在 $(0,2)$ 上单调减少；在 $x=2$ 处取极小值 $3$；在 $(-\infty,0)\cup(0,+\infty)$ 上均为凹，无拐点；渐近线为 $x=0$ 与 $y=x$。 |
| 18 | 解答题 | $\begin{cases}y=C_1\cos ax+C_2\sin ax+\dfrac{\sin x}{a^2-1},&a\ne1,\\[4pt]y=C_1\cos x+C_2\sin x-\dfrac{x}{2}\cos x,&a=1.\end{cases}$ |
| 19 | 解答题 | 见解析。 |
| 20 | 解答题 | $\dfrac{448\pi}{15}$ |

## 详细解析

### 第 1 题

- 答案：$-2$

要使 $f(x)$ 在 $x=0$ 处连续，需有
$$
a=\lim_{x\to 0}\frac{\sin 2x+e^{2ax}-1}{x}.
$$
由 $\sin 2x\sim 2x$，$e^{2ax}-1\sim 2ax$，得
$$
a=2+2a,
$$
故 $a=-2$。

### 第 2 题

- 答案：$\dfrac{(t+1)(6t+5)}{t}$

先求
$$
\frac{dy}{dx}=\frac{dy/dt}{dx/dt}=\frac{3t^2+2t}{1-\frac{1}{1+t}}=3t^2+5t+2.
$$
再对 $t$ 求导，得
$$
\frac{d^2y}{dx^2}=\frac{6t+5}{1-\frac{1}{1+t}}=\frac{(t+1)(6t+5)}{t}.
$$

### 第 3 题

- 答案：$-3\sin 3x\,f(\cos 3x)$

由变上限积分求导公式与链式法则，
$$
\frac{d}{dx}\left(\int_0^{\cos 3x}f(t)\,dt\right)=f(\cos 3x)\cdot(\cos 3x)'=-3\sin 3x\,f(\cos 3x).
$$

### 第 4 题

- 答案：$\dfrac{1}{2}(x^2-1)e^{x^2}+C$

写成
$$
\int x^3e^{x^2}\,dx=\frac{1}{2}\int x^2\,d(e^{x^2}).
$$
作分部积分得
$$
\frac{1}{2}\int x^2\,d(e^{x^2})=\frac{1}{2}\left[x^2e^{x^2}-\int e^{x^2}\,d(x^2)\right]=\frac{1}{2}(x^2-1)e^{x^2}+C.
$$

### 第 5 题

- 答案：$(x-4)y^4=Cx$

原方程可写成
$$
\frac{dx}{x(x-4)}+\frac{dy}{y}=0.
$$
积分得
$$
\frac{1}{4}\ln\left|\frac{x-4}{x}\right|+\ln|y|=C_1.
$$
化简为
$$
\frac{x-4}{x}y^4=C,
$$
即
$$
(x-4)y^4=Cx.
$$

### 第 6 题

- 答案：A

由 $\ln(1+x)=x-\dfrac{x^2}{2}+o(x^2)$，得
$$
\ln(1+x)-(ax+bx^2)=(1-a)x-\left(\frac{1}{2}+b\right)x^2+o(x^2).
$$
由题设应有
$$
1-a=0,\qquad -\left(\frac{1}{2}+b\right)=2.
$$
故 $a=1,b=-\dfrac{5}{2}$，选 A。

### 第 7 题

- 答案：B

左侧函数可导，且
$$
f'_-(1)=\left(\frac{2}{3}x^3\right)'\bigg|_{x=1}=2.
$$
又有
$$
f(1)=\frac{2}{3},\qquad \lim_{x\to1^+}f(x)=1\ne f(1),
$$
故 $f$ 在 $x=1$ 右侧不连续，从而右导数不存在，选 B。

### 第 8 题

- 答案：C

在 $x=x_0$ 处有
$$
f''(x_0)+f'(x_0)=e^{\sin x_0}.
$$
由 $f'(x_0)=0$ 得
$$
f''(x_0)=e^{\sin x_0}>0.
$$
故 $x_0$ 是极小值点，选 C。

### 第 9 题

- 答案：B

当 $x\to\pm\infty$ 时，$e^{1/x^2}\to1$，且
$$
\frac{x^2+x+1}{(x-1)(x+2)}\to1,
$$
故有水平渐近线 $y=\arctan1=\dfrac{\pi}{4}$。当 $x\to0$ 时，
$$
\arctan\frac{x^2+x+1}{(x-1)(x+2)}\to\arctan\left(-\frac{1}{2}\right)<0,
$$
而 $e^{1/x^2}\to+\infty$，故 $y\to-\infty$，所以 $x=0$ 是铅直渐近线。$x=1,-2$ 处函数值有界，不是渐近线。故共 2 条，选 B。

### 第 10 题

- 答案：D

被积函数 $\dfrac{\sin x}{1+x^2}\cos^4x$ 为奇函数，故 $M=0$。又
$$
N=\int_{-\pi/2}^{\pi/2}\sin^3x\,dx+\int_{-\pi/2}^{\pi/2}\cos^4x\,dx=2\int_0^{\pi/2}\cos^4x\,dx>0,
$$
$$
P=\int_{-\pi/2}^{\pi/2}x^2\sin^3x\,dx-\int_{-\pi/2}^{\pi/2}\cos^4x\,dx=-N<0.
$$
故 $P<M<N$，选 D。

### 第 11 题

- 答案：$y''=\dfrac{f''}{(1-f')^3}$

对方程 $y=f(x+y)$ 两边对 $x$ 求导，得
$$
y'=f'(1+y').
$$
故
$$
y'=\frac{f'}{1-f'}.
$$
再求导，有
$$
y''=f''(1+y')^2+f'y''.
$$
移项得
$$
(1-f')y''=f''(1+y')^2.
$$
而
$$
1+y'=1+\frac{f'}{1-f'}=\frac{1}{1-f'},
$$
所以
$$
y''=\frac{f''}{(1-f')^3}.
$$

### 第 12 题

- 答案：$\dfrac{3\pi}{32}$

令 $x^2=\sin t$，则 $2x\,dx=\cos t\,dt$。当 $x=0$ 时 $t=0$，当 $x=1$ 时 $t=\dfrac{\pi}{2}$，故
$$
\int_0^1x(1-x^4)^{3/2}dx=\frac{1}{2}\int_0^{\pi/2}\cos^4t\,dt.
$$
又
$$
\int_0^{\pi/2}\cos^4t\,dt=\frac{3\pi}{16},
$$
故原积分为
$$
\frac{1}{2}\cdot\frac{3\pi}{16}=\frac{3\pi}{32}.
$$

### 第 13 题

- 答案：$e^4$

利用
$$
\tan\left(\frac{\pi}{4}+u\right)=\frac{1+\tan u}{1-\tan u},
$$
取 $u=\dfrac{2}{n}$，得
$$
\tan^n\left(\frac{\pi}{4}+\frac{2}{n}\right)=\left(1+\frac{2\tan(2/n)}{1-\tan(2/n)}\right)^n.
$$
由 $\tan(2/n)\sim 2/n$ 可知
$$
n\cdot\frac{2\tan(2/n)}{1-\tan(2/n)}\to4,
$$
于是由重要极限得原极限为 $e^4$。

### 第 14 题

- 答案：$\dfrac{1}{8}\left[\ln(1-\cos x)-\ln(1+\cos x)+\dfrac{2}{1+\cos x}\right]+C$

先化简分母：
$$
\sin2x+2\sin x=2\sin x(1+\cos x).
$$
令 $u=\cos x$，则 $du=-\sin x\,dx$，原式化为
$$
-\frac{1}{2}\int\frac{du}{(1-u)(1+u)^2}.
$$
将被积函数分解为
$$
\frac{1}{(1-u)(1+u)^2}=\frac{1}{4}\cdot\frac{1}{1-u}+\frac{1}{4}\cdot\frac{1}{1+u}+\frac{1}{2}\cdot\frac{1}{(1+u)^2}.
$$
逐项积分后得
$$
\int\frac{dx}{\sin2x+2\sin x}=\frac{1}{8}\left[\ln(1-u)-\ln(1+u)+\frac{2}{1+u}\right]+C.
$$
代回 $u=\cos x$ 即得。

### 第 15 题

- 答案：见解析。

由图可知 $C=(0,\tfrac{1}{2})$，$B=(a,a^2+\tfrac{1}{2})$。故梯形面积
$$
D=\frac{\frac{1}{2}+\left(a^2+\frac{1}{2}\right)}{2}\cdot a=\frac{a(1+a^2)}{2}.
$$
曲边梯形面积
$$
D_1=\int_0^a\left(x^2+\frac{1}{2}\right)dx=\frac{a^3}{3}+\frac{a}{2}=\frac{a(3+2a^2)}{6}.
$$
于是
$$
\frac{D}{D_1}=\frac{3(1+a^2)}{3+2a^2}=\frac{3}{2}\cdot\frac{1+a^2}{\frac{3}{2}+a^2}<\frac{3}{2}.
$$

### 第 16 题

- 答案：$k\le0$ 或 $k=\dfrac{2\sqrt{3}}{9}$

方程可化为
$$
kx^3-x^2+1=0.
$$
记 $\varphi(x)=kx^3-x^2+1$。则
$$
\varphi'(x)=3kx^2-2x=x(3kx-2).
$$
当 $k\le0$ 时，对一切 $x>0$ 有 $\varphi'(x)<0$，故 $\varphi$ 单调减少，且 $\varphi(0)=1>0$，在 $x>0$ 上恰有一个零点。
当 $k>0$ 时，$\varphi$ 先减后增，极小值在 $x=\dfrac{2}{3k}$ 处取得。要使正根唯一，必须有极小值为零，即
$$
\varphi\left(\frac{2}{3k}\right)=1-\frac{4}{27k^2}=0.
$$
解得
$$
k=\frac{2\sqrt{3}}{9}.
$$
综上，
$$
k\le0\quad\text{或}\quad k=\frac{2\sqrt{3}}{9}.
$$

### 第 17 题

- 答案：函数在 $(-\infty,0)\cup(2,+\infty)$ 上单调增加，在 $(0,2)$ 上单调减少；在 $x=2$ 处取极小值 $3$；在 $(-\infty,0)\cup(0,+\infty)$ 上均为凹，无拐点；渐近线为 $x=0$ 与 $y=x$。

函数可化为
$$
y=x+\frac{4}{x^2},\qquad x\ne0.
$$
故
$$
y'=1-\frac{8}{x^3},\qquad y''=\frac{24}{x^4}>0.
$$
由 $y'=0$ 得驻点 $x=2$。于是函数在 $(-\infty,0)$、$(2,+\infty)$ 上单调增加，在 $(0,2)$ 上单调减少，且
$$
y(2)=2+\frac{4}{4}=3,
$$
所以在 $x=2$ 处取极小值 $3$。由于 $y''>0$ 对一切 $x\ne0$ 成立，所以在 $(-\infty,0)$ 与 $(0,+\infty)$ 上均为凹，不存在拐点。
又
$$
\lim_{x\to0}y=+\infty,
$$
故 $x=0$ 为铅直渐近线；并且
$$
\lim_{x\to\pm\infty}\frac{y}{x}=1,\qquad \lim_{x\to\pm\infty}(y-x)=0,
$$
故斜渐近线为 $y=x$。据此可作出图形。

### 第 18 题

- 答案：$\begin{cases}y=C_1\cos ax+C_2\sin ax+\dfrac{\sin x}{a^2-1},&a\ne1,\\[4pt]y=C_1\cos x+C_2\sin x-\dfrac{x}{2}\cos x,&a=1.\end{cases}$

对应齐次方程 $y''+a^2y=0$ 的通解为
$$
y_h=C_1\cos ax+C_2\sin ax.
$$
当 $a\ne1$ 时，设特解为 $y_p=A\sin x+B\cos x$，代入得
$$
(a^2-1)A=1,\qquad (a^2-1)B=0,
$$
故
$$
y_p=\frac{\sin x}{a^2-1}.
$$
当 $a=1$ 时发生共振，设特解为
$$
y_p=x(A\sin x+B\cos x).
$$
代入方程得 $A=0,B=-\dfrac{1}{2}$，于是
$$
y_p=-\frac{x}{2}\cos x.
$$
故所求通解即为题中所示。

### 第 19 题

- 答案：见解析。

作代换 $x=\lambda t$，则
$$
\int_0^\lambda f(x)\,dx=\lambda\int_0^1f(\lambda t)\,dt.
$$
因此
$$
\int_0^\lambda f(x)\,dx-\lambda\int_0^1f(x)\,dx=\lambda\int_0^1\bigl[f(\lambda t)-f(t)\bigr]dt.
$$
由于 $0<\lambda<1$，对任意 $t\in[0,1]$ 都有 $\lambda t\le t$，又 $f$ 递减，故
$$
f(\lambda t)\ge f(t).
$$
于是右端非负，从而
$$
\int_0^\lambda f(x)\,dx\ge \lambda\int_0^1f(x)\,dx.
$$

### 第 20 题

- 答案：$\dfrac{448\pi}{15}$

曲线关于 $y$ 轴对称，且与 $x$ 轴交于 $(-2,0)$、$(2,0)$。只算右半边即可。对 $0\le x\le2$，有
$$
3-y=|x^2-1|.
$$
以竖条作体积微元，得
$$
dV=\pi\left[3^2-(3-y)^2\right]dx=\pi\left[9-(x^2-1)^2\right]dx=\pi(8+2x^2-x^4)dx.
$$
故总体积
$$
V=2\pi\int_0^2(8+2x^2-x^4)dx
=2\pi\left[8x+\frac{2}{3}x^3-\frac{1}{5}x^5\right]_0^2
=\frac{448\pi}{15}.
$$
