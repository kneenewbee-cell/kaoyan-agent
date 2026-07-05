# Math 2 1991 Answers

资料类型：考研数学二答案解析
年份：1991
科目：数学二
范围：试卷 III
校对状态：已按答案页图像清洗并与题面同步。

## 答案速查

| 题号 | 题型 | 答案 |
|---|---|---|
| 1 | 填空题 | $-\dfrac{\ln 3}{1+3^x}\,dx$ |
| 2 | 填空题 | $\left(-\infty,-\dfrac{1}{\sqrt{2}}\right)\cup\left(\dfrac{1}{\sqrt{2}},+\infty\right)$ |
| 3 | 填空题 | $1$ |
| 4 | 填空题 | $\dfrac{1}{2}$ |
| 5 | 填空题 | $-1$ |
| 6 | 选择题 | D |
| 7 | 选择题 | B |
| 8 | 选择题 | B |
| 9 | 选择题 | D |
| 10 | 选择题 | A |
| 11 | 解答题 | $\dfrac{t^2+2-2t\sin t\cos t}{(\cos t-t\sin t)^3}$ |
| 12 | 解答题 | $2\ln\dfrac{4}{3}$ |
| 13 | 解答题 | $\dfrac{1}{6}$ |
| 14 | 解答题 | $\dfrac{x^2}{4}-\dfrac{x\sin2x}{4}-\dfrac{\cos2x}{8}+C$ |
| 15 | 解答题 | $y=\dfrac{(x-1)e^x+1}{x}$ |
| 16 | 证明题 | 见解析。 |
| 17 | 解答题 | $y=C_1\cos x+C_2\sin x+x+\dfrac{1}{2}x\sin x$ |
| 18 | 解答题 | $\dfrac{\pi}{2}$ |
| 19 | 解答题 | $x_B=\dfrac{\ln2}{3}-1,\quad x_C=\dfrac{1+\ln2}{3}$ |
| 20 | 解答题 | $\pi^2-2$ |

## 详细解析

### 第 1 题

- 答案：$-\dfrac{\ln 3}{1+3^x}\,dx$

由链式法则，

$$
y'=\frac{1}{1+3^{-x}}\cdot(-\ln3)3^{-x}=-\frac{\ln3}{1+3^x}.
$$

故 $dy=-\dfrac{\ln3}{1+3^x}dx$。

### 第 2 题

- 答案：$\left(-\infty,-\dfrac{1}{\sqrt{2}}\right)\cup\left(\dfrac{1}{\sqrt{2}},+\infty\right)$

有

$$
y'=-2xe^{-x^2},\qquad y''=(4x^2-2)e^{-x^2}=2(2x^2-1)e^{-x^2}.
$$

因为 $e^{-x^2}>0$，故当 $|x|>\dfrac{1}{\sqrt{2}}$ 时 $y''>0$，曲线为上凸。

### 第 3 题

- 答案：$1$

分部积分，取 $u=\ln x$，$dv=x^{-2}dx$，则

$$
\int_1^{+\infty}\frac{\ln x}{x^2}dx=\left.-\frac{\ln x}{x}\right|_1^{+\infty}+\int_1^{+\infty}\frac{dx}{x^2}=1.
$$

### 第 4 题

- 答案：$\dfrac{1}{2}$

所求路程为

$$
\int_{\sqrt{\pi/2}}^{\sqrt{\pi}}t\sin(t^2)dt.
$$

令 $u=t^2$，则 $du=2t\,dt$，故原积分等于

$$
\frac{1}{2}\int_{\pi/2}^{\pi}\sin u\,du=\frac{1}{2}.
$$

### 第 5 题

- 答案：$-1$

分子分母同时乘以 $e^{-1/x}$，得

$$
\frac{e^{-1/x}-1}{xe^{-1/x}+1}.
$$

当 $x\to0^+$ 时，$e^{-1/x}\to0$，故极限为 $\dfrac{-1}{1}=-1$。

### 第 6 题

- 答案：D

切点在两曲线上，先代入 $x=1,y=-1$ 得 $1+a+b=-1$，即 $a+b=-2$。又两曲线在该点斜率相等：前者斜率 $2x+a$ 在点处为 $2+a$；后者由隐函数求导得在点处斜率为 $1$，故 $2+a=1$，即 $a=-1$，从而 $b=-1$。

### 第 7 题

- 答案：B

当 $0\le x\le1$ 时直接积分得 $F(x)=\dfrac{x^3}{3}$。当 $1<x\le2$ 时，

$$
F(x)=\int_0^1t^2dt+\int_1^x(2-t)dt=\frac{1}{3}+2x-\frac{x^2}{2}-\frac{3}{2}=-\frac{7}{6}+2x-\frac{x^2}{2}.
$$

故选 B。

### 第 8 题

- 答案：B

极大值只是局部性质，A 与 D 都不一定成立。把图像关于原点作中心对称，相当于考察 $y=-f(-x)$，于是 $x_0$ 的极大值点对应为 $-x_0$ 的极小值点，故选 B。

### 第 9 题

- 答案：D

当 $x\to0$ 时分母趋于 $0$ 而分子趋于 $2$，所以 $x=0$ 是铅直渐近线；当 $x\to\pm\infty$ 时 $e^{-x^2}\to0$，故 $y\to1$，所以 $y=1$ 是水平渐近线。

### 第 10 题

- 答案：A

以杆右端为原点，杆位于区间 $[-l,0]$。长度元 $dx$ 的质量为 $\mu dx$，与质点的距离为 $a-x$，故微元引力为

$$
dF=\frac{k m\mu}{(a-x)^2}dx.
$$

沿整根细杆积分即可，故选 A。

### 第 11 题

- 答案：$\dfrac{t^2+2-2t\sin t\cos t}{(\cos t-t\sin t)^3}$

先求

$$
\frac{dy}{dx}=\frac{\sin t+t\cos t}{\cos t-t\sin t}.
$$

再对 $t$ 求导并除以 $dx/dt=\cos t-t\sin t$，整理得

$$
\frac{d^2y}{dx^2}=\frac{t^2+2-2t\sin t\cos t}{(\cos t-t\sin t)^3}.
$$

### 第 12 题

- 答案：$2\ln\dfrac{4}{3}$

令 $t=\sqrt{x}$，则 $x=t^2,dx=2t\,dt$，原积分化为

$$
2\int_1^2\frac{dt}{t(1+t)}=2\int_1^2\left(\frac{1}{t}-\frac{1}{1+t}\right)dt=2\ln\frac{4}{3}.
$$

### 第 13 题

- 答案：$\dfrac{1}{6}$

当 $x\to0$ 时，

$$
x-\sin x\sim\frac{x^3}{6},\qquad e^x-1\sim x.
$$

所以原式

$$
\sim\frac{x^3/6}{x^2\cdot x}=\frac{1}{6}.
$$

### 第 14 题

- 答案：$\dfrac{x^2}{4}-\dfrac{x\sin2x}{4}-\dfrac{\cos2x}{8}+C$

用恒等式 $\sin^2x=\dfrac{1-\cos2x}{2}$，则

$$
\int x\sin^2x\,dx=\frac{1}{2}\int x\,dx-\frac{1}{2}\int x\cos2x\,dx.
$$

第二项作分部积分，整理得所求结果。

### 第 15 题

- 答案：$y=\dfrac{(x-1)e^x+1}{x}$

方程可写成 $(xy)'=xe^x$。积分得

$$
xy=\int xe^x dx=(x-1)e^x+C.
$$

由 $y(1)=1$ 得 $C=1$，故

$$
y=\frac{(x-1)e^x+1}{x}.
$$

### 第 16 题

- 答案：见解析。

令

$$
f(x)=(1+x)\ln(1+x)-x\ln x.
$$

则命题等价于 $f(x)>0$（$x>1$）。求导得

$$
f'(x)=\ln\frac{1+x}{x}>0,
$$

所以 $f$ 在 $(1,+\infty)$ 上递增，而 $f(1)=2\ln2>0$，故对一切 $x>1$ 都有 $f(x)>0$，命题成立。

### 第 17 题

- 答案：$y=C_1\cos x+C_2\sin x+x+\dfrac{1}{2}x\sin x$

对应齐次方程通解为 $C_1\cos x+C_2\sin x$。对右端的 $x$ 可取特解 $y_{p1}=x$；对共振项 $\cos x$ 取特解 $y_{p2}=Ax\sin x$，代入得 $A=\dfrac{1}{2}$。故通解为

$$
y=C_1\cos x+C_2\sin x+x+\frac{1}{2}x\sin x.
$$

### 第 18 题

- 答案：$\dfrac{\pi}{2}$

区域位于 $x\in[1,2]$，且曲线在该区间下方。用柱壳法：

$$
V=2\pi\int_1^2x\bigl(-(x-1)(x-2)\bigr)dx=2\pi\int_1^2(-x^3+3x^2-2x)dx=\frac{\pi}{2}.
$$

### 第 19 题

- 答案：$x_B=\dfrac{\ln2}{3}-1,\quad x_C=\dfrac{1+\ln2}{3}$

设 $C$ 的横坐标为 $x>0$，则由 $e^{x_B}=2e^{-2x}$ 得 $x_B=\ln2-2x$。梯形面积可表示为

$$
S(x)=\frac{e^{-2x}+2e^{-2x}}2\,(x-x_B)=\frac{3}{2}e^{-2x}(3x-\ln2).
$$

求导得唯一极大点 $x=\dfrac{1+\ln2}{3}$，于是

$$
x_B=\ln2-2x=\frac{\ln2}{3}-1.
$$

### 第 20 题

- 答案：$\pi^2-2$

当 $x\in[\pi,2\pi)$ 时，

$$
f(x)=x-\pi+\sin x;
$$

当 $x\in[2\pi,3\pi)$ 时，再递推一次得 $f(x)=x-2\pi$。故

$$
\int_\pi^{3\pi}f(x)dx=\int_\pi^{2\pi}(x-\pi+\sin x)dx+\int_{2\pi}^{3\pi}(x-2\pi)dx=\pi^2-2.
$$
