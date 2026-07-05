# Math 2 1995 Answers

资料类型：考研数学二答案解析
年份：1995
科目：数学二
范围：试卷 III
校对状态：已按答案页图像清洗并与题面同步。

## 答案速查

| 题号 | 题型 | 答案 |
|---|---|---|
| 1 | 填空题 | $-2x\sin(x^2)\sin^2\dfrac{1}{x}-\dfrac{2}{x^2}\cos(x^2)\sin\dfrac{1}{x}\cos\dfrac{1}{x}$ |
| 2 | 填空题 | $y=C_1\cos x+C_2\sin x-2x$ |
| 3 | 填空题 | $y-3x+7=0$ |
| 4 | 填空题 | $\dfrac{1}{2}$ |
| 5 | 填空题 | $y=0$ |
| 6 | 选择题 | D |
| 7 | 选择题 | C |
| 8 | 选择题 | D |
| 9 | 选择题 | B |
| 10 | 选择题 | A |
| 11 | 解答题 | $\dfrac{1}{2}$ |
| 12 | 解答题 | $\dfrac{f''(y)-\bigl(1-f'(y)\bigr)^2}{x^2\bigl(1-f'(y)\bigr)^3}$ |
| 13 | 解答题 | $x+2\ln\lvert x-1\rvert+C$ |
| 14 | 解答题 | $f'(x)$ 在 $x=0$ 处连续 |
| 15 | 解答题 | $8$ |
| 16 | 解答题 | $\xi=x_0-\dfrac{y_0'(1+y_0'^2)}{y_0''},\quad \eta=y_0+\dfrac{1+y_0'^2}{y_0''}$ |
| 17 | 解答题 | $2$ |
| 18 | 证明题 | 见解析 |

## 详细解析

### 第 1 题

- 答案：$-2x\sin(x^2)\sin^2\dfrac{1}{x}-\dfrac{2}{x^2}\cos(x^2)\sin\dfrac{1}{x}\cos\dfrac{1}{x}$

把 $y$ 看成 $\cos(x^2)$ 与 $\sin^2\dfrac{1}{x}$ 的乘积，应用乘积求导法则：
$$
y'=-2x\sin(x^2)\sin^2\frac{1}{x}+\cos(x^2)\cdot2\sin\frac{1}{x}\cos\frac{1}{x}\cdot\left(-\frac{1}{x^2}\right).
$$
整理得
$$
y'=-2x\sin(x^2)\sin^2\frac{1}{x}-\frac{2}{x^2}\cos(x^2)\sin\frac{1}{x}\cos\frac{1}{x}.
$$

### 第 2 题

- 答案：$y=C_1\cos x+C_2\sin x-2x$

对应齐次方程 $y''+y=0$ 的特征方程为 $r^2+1=0$，故齐次通解为
$$
y_h=C_1\cos x+C_2\sin x.
$$
设原方程的一个特解为 $y_p=ax+b$，代入得
$$
0+ax+b=-2x,
$$
比较系数可得 $a=-2,b=0$，所以 $y_p=-2x$。因此通解为
$$
y=C_1\cos x+C_2\sin x-2x.
$$

### 第 3 题

- 答案：$y-3x+7=0$

由参数方程求导，
$$
\frac{dy}{dx}=\frac{dy/dt}{dx/dt}=\frac{3t^2}{2t}=\frac{3t}{2}.
$$
当 $t=2$ 时，斜率为 $3$，且点坐标为
$$
(x,y)=(1+2^2,2^3)=(5,8).
$$
故切线方程为
$$
y-8=3(x-5),
$$
即
$$
y-3x+7=0.
$$

### 第 4 题

- 答案：$\dfrac{1}{2}$

记
$$
a_n=\sum_{k=1}^n\frac{k}{n^2+n+k}.
$$
对每个 $k=1,2,\dots,n$，有
$$
\frac{k}{n^2+2n}\le \frac{k}{n^2+n+k}\le \frac{k}{n^2+n+1}.
$$
求和得
$$
\frac{1+2+\cdots+n}{n^2+2n}\le a_n\le \frac{1+2+\cdots+n}{n^2+n+1}.
$$
即
$$
\frac{n(n+1)}{2(n^2+2n)}\le a_n\le \frac{n(n+1)}{2(n^2+n+1)}.
$$
两端同趋于 $\dfrac{1}{2}$，由夹逼准则得
$$
\lim_{n\to\infty}a_n=\frac{1}{2}.
$$

### 第 5 题

- 答案：$y=0$

函数 $y=x^2e^{-x^2}$ 在全体实数上有定义，不存在竖直渐近线。又由于
$$
\lim_{x\to\pm\infty}x^2e^{-x^2}=0,
$$
所以它只有一条水平渐近线
$$
y=0.
$$

### 第 6 题

- 答案：D

由于 $f(x)$ 连续且处处不为零，所以 $\dfrac{1}{f(x)}$ 也是连续函数。若设 $\dfrac{\varphi(x)}{f(x)}$ 在某点连续，则它与连续函数 $f(x)$ 的乘积
$$
\varphi(x)=f(x)\cdot\frac{\varphi(x)}{f(x)}
$$
也应在该点连续，这与 $\varphi(x)$ 在该点有间断点矛盾。因此 $\dfrac{\varphi(x)}{f(x)}$ 必有间断点，选 D。

其余选项可举反例排除，例如取 $f(x)\equiv1$，$\varphi(x)=\begin{cases}-1,&x<0,\\1,&x\ge0,\end{cases}$ 则 $[\varphi(x)]^2\equiv1$ 连续。

### 第 7 题

- 答案：C

因为
$$
y=x(x-1)(2-x)
$$
在区间 $(0,1)$ 上为负，在区间 $(1,2)$ 上为正，所以所围面积应为两段绝对值面积之和：
$$
S=-\int_0^1x(x-1)(2-x)\,dx+\int_1^2x(x-1)(2-x)\,dx.
$$
故选 C。

### 第 8 题

- 答案：D

题设说明 $f(x)$ 在整个实轴上严格单调增加。若 $x_1>x_2$，则有 $-x_1<-x_2$，从而
$$
f(-x_1)<f(-x_2),
$$
于是
$$
-f(-x_1)>-f(-x_2).
$$
故函数 $-f(-x)$ 单调增加，选 D。

A 不一定成立，例如 $f(x)=x^3$ 单调增加，但在 $x=0$ 处有 $f'(0)=0$。

### 第 9 题

- 答案：B

由 $f''(x)>0$ 可知 $f'(x)$ 在 $[0,1]$ 上严格递增，因此对任意 $x\in(0,1)$ 有
$$
f'(1)>f'(x)>f'(0).
$$
又由拉格朗日中值定理，存在 $\xi\in(0,1)$ 使得
$$
f(1)-f(0)=f'(\xi).
$$
于是
$$
f'(1)>f(1)-f(0)>f'(0).
$$
故选 B。

### 第 10 题

- 答案：A

因为 $f(x)$ 本身可导，所以 $F(x)$ 在 $0$ 处可导当且仅当 $f(x)|\sin x|$ 在 $0$ 处可导。记
$$
p(x)=f(x)|\sin x|.
$$
则右导数为
$$
p'_+(0)=\lim_{x\to0^+}\frac{f(x)\sin x}{x}=f(0),
$$
左导数为
$$
p'_-(0)=\lim_{x\to0^-}\frac{f(x)(-\sin x)}{x}=-f(0).
$$
要使左右导数相等，必须有 $f(0)=-f(0)$，即 $f(0)=0$。故选 A。

### 第 11 题

- 答案：$\dfrac{1}{2}$

将分子有理化：
$$
1-\sqrt{\cos x}=\frac{1-\cos x}{1+\sqrt{\cos x}}.
$$
于是原式等于
$$
\lim_{x\to0^+}\frac{1-\cos x}{x(1-\cos\sqrt{x})(1+\sqrt{\cos x})}.
$$
当 $x\to0^+$ 时，利用等价无穷小
$$
1-\cos x\sim\frac{x^2}{2},\qquad 1-\cos\sqrt{x}\sim\frac{x}{2},\qquad 1+\sqrt{\cos x}\to2,
$$
故原式
$$
\sim\frac{x^2/2}{x\cdot(x/2)\cdot2}=\frac{1}{2}.
$$

### 第 12 题

- 答案：$\dfrac{f''(y)-\bigl(1-f'(y)\bigr)^2}{x^2\bigl(1-f'(y)\bigr)^3}$

对方程两边取对数，得
$$
\ln x+f(y)=y.
$$
两边对 $x$ 求导：
$$
\frac{1}{x}+f'(y)y'=y',
$$
整理得
$$
y'=\frac{1}{x\bigl(1-f'(y)\bigr)}.
$$
再对上式求导。设 $g(y)=1-f'(y)$，则 $y'=(xg)^{-1}$，于是
$$
y''=-\frac{g+xg'}{x^2g^2}=-\frac{g-xf''(y)y'}{x^2g^2}.
$$
代入 $y'=\dfrac{1}{xg}$，得
$$
y''=-\frac{1}{x^2g}+\frac{f''(y)}{x^2g^3}
=\frac{f''(y)-g^2}{x^2g^3}.
$$
因此
$$
\frac{d^2y}{dx^2}=\frac{f''(y)-\bigl(1-f'(y)\bigr)^2}{x^2\bigl(1-f'(y)\bigr)^3}.
$$

### 第 13 题

- 答案：$x+2\ln\lvert x-1\rvert+C$

先求出 $f$ 的表达式。令 $t=x^2-1$，则 $x^2=t+1$，从而
$$
f(t)=\ln\frac{t+1}{t-1}.
$$
由题设 $f[\varphi(x)]=\ln x$，得
$$
\ln\frac{\varphi(x)+1}{\varphi(x)-1}=\ln x.
$$
因此
$$
\frac{\varphi(x)+1}{\varphi(x)-1}=x.
$$
解得
$$
\varphi(x)=\frac{x+1}{x-1}=1+\frac{2}{x-1}.
$$
故
$$
\int\varphi(x)\,dx=\int\left(1+\frac{2}{x-1}\right)dx=x+2\ln\lvert x-1\rvert+C.
$$

### 第 14 题

- 答案：$f'(x)$ 在 $x=0$ 处连续

当 $x\ne0$ 时，
$$
f'(x)=\arctan\frac{1}{x^2}+x\cdot\frac{1}{1+1/x^4}\cdot\left(-\frac{2}{x^3}\right)
=\arctan\frac{1}{x^2}-\frac{2x^2}{1+x^4}.
$$
又因为
$$
f'(0)=\lim_{x\to0}\frac{f(x)-f(0)}{x}=\lim_{x\to0}\arctan\frac{1}{x^2}=\frac{\pi}{2}.
$$
而当 $x\to0$ 时，
$$
\arctan\frac{1}{x^2}\to\frac{\pi}{2},\qquad \frac{2x^2}{1+x^4}\to0,
$$
所以
$$
\lim_{x\to0}f'(x)=\frac{\pi}{2}=f'(0).
$$
故 $f'(x)$ 在 $x=0$ 处连续。

### 第 15 题

- 答案：$8$

由弧长公式，
$$
S=\int_0^{2\pi}\sqrt{\left(\frac{dx}{dt}\right)^2+\left(\frac{dy}{dt}\right)^2}\,dt.
$$
其中
$$
\frac{dx}{dt}=\sin t,\qquad \frac{dy}{dt}=1-\cos t.
$$
故
$$
\sqrt{\sin^2 t+(1-\cos t)^2}=\sqrt{2-2\cos t}=2\sin\frac{t}{2}
$$
（在 $0\le t\le2\pi$ 上取非负值）。于是
$$
S=\int_0^{2\pi}2\sin\frac{t}{2}\,dt=\left[-4\cos\frac{t}{2}\right]_0^{2\pi}=8.
$$

### 第 16 题

- 答案：$\xi=x_0-\dfrac{y_0'(1+y_0'^2)}{y_0''},\quad \eta=y_0+\dfrac{1+y_0'^2}{y_0''}$

点 $M(x_0,y_0)$ 处切线斜率为 $y_0'$，故法线方向向量可取
$$
(-y_0',1).
$$
它的长度为 $\sqrt{1+y_0'^2}$，所以法线方向上的单位向量可取
$$
\left(\frac{-y_0'}{\sqrt{1+y_0'^2}},\frac{1}{\sqrt{1+y_0'^2}}\right).
$$
又已知
$$
|MP|=\frac{(1+y_0'^2)^{3/2}}{y_0''}.
$$
由于 $y_0''>0$，图中点 $P$ 位于法线向上的一侧，因此
$$
\overrightarrow{MP}=\frac{(1+y_0'^2)^{3/2}}{y_0''}\left(\frac{-y_0'}{\sqrt{1+y_0'^2}},\frac{1}{\sqrt{1+y_0'^2}}\right)
=\left(-\frac{y_0'(1+y_0'^2)}{y_0''},\frac{1+y_0'^2}{y_0''}\right).
$$
于是
$$
\xi=x_0-\frac{y_0'(1+y_0'^2)}{y_0''},\qquad
\eta=y_0+\frac{1+y_0'^2}{y_0''}.
$$

### 第 17 题

- 答案：$2$

把二重积分区域写出来：
$$
\int_0^{\pi}f(x)\,dx=\int_0^{\pi}\left(\int_0^x\frac{\sin t}{\pi-t}\,dt\right)dx.
$$
对应区域为
$$
D=\{(x,t)\mid 0\le t\le x\le\pi\}.
$$
交换积分次序后得
$$
\int_0^{\pi}f(x)\,dx=\int_0^{\pi}\left(\int_t^{\pi}dx\right)\frac{\sin t}{\pi-t}\,dt
=\int_0^{\pi}\frac{\pi-t}{\pi-t}\sin t\,dt.
$$
因此
$$
\int_0^{\pi}f(x)\,dx=\int_0^{\pi}\sin t\,dt=2.
$$

### 第 18 题

- 答案：见解析

由
$$
\lim_{x\to0}\frac{f(x)}{x}=1
$$
可知 $f(0)=0$，并且
$$
f'(0)=\lim_{x\to0}\frac{f(x)-f(0)}{x-0}=\lim_{x\to0}\frac{f(x)}{x}=1.
$$
令
$$
p(x)=f(x)-x.
$$
则
$$
p(0)=0,\qquad p'(0)=f'(0)-1=0,\qquad p''(x)=f''(x)>0.
$$
所以 $p(x)$ 是严格凸函数，且在 $x=0$ 处导数为零，因此 $x=0$ 是 $p(x)$ 的极小点。于是对一切 $x$ 都有
$$
p(x)\ge p(0)=0.
$$
即
$$
f(x)-x\ge0.
$$
故
$$
f(x)\ge x.
$$
