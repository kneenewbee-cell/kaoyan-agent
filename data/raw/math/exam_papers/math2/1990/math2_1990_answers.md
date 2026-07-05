# Math 2 1990 Answers

资料类型：考研数学二答案解析
年份：1990
科目：数学二
范围：试卷 III
校对状态：已按答案页图像清洗并与题面同步。

## 答案速查

| 题号 | 题型 | 答案 |
|---|---|---|
| 1 | 填空题 | $y-\dfrac{1}{8}=3\left(x-\dfrac{3\sqrt{3}}{8}\right)$ |
| 2 | 填空题 | $e^{\tan\frac{1}{x}}\left(\sec^2\frac{1}{x}\sin\frac{1}{x}+\cos\frac{1}{x}\right)\left(-\dfrac{1}{x^2}\right)dx$ |
| 3 | 填空题 | $\dfrac{4}{15}$ |
| 4 | 填空题 | $>$ |
| 5 | 填空题 | $1$ |
| 6 | 选择题 | C |
| 7 | 选择题 | B |
| 8 | 选择题 | A |
| 9 | 选择题 | A |
| 10 | 选择题 | B |
| 11 | 解答题 | $a=\ln 3$ |
| 12 | 解答题 | $dy=\dfrac{3+\ln(x-y)}{2+\ln(x-y)}\,dx$ |
| 13 | 解答题 | $\left(\dfrac{1}{\sqrt{3}},\dfrac{3}{4}\right)$ |
| 14 | 解答题 | $\ln x+\ln\lvert 1-x\rvert-\dfrac{\ln x}{1-x}+C$ |
| 15 | 解答题 | $y=\dfrac{1+\ln^2 x}{2\ln x}$ |
| 16 | 解答题 | $P=\left(\dfrac{a}{\sqrt{2}},\dfrac{b}{\sqrt{2}}\right)$ |
| 17 | 证明题 | 见解析。 |
| 18 | 解答题 | $\dfrac{1}{2}\ln^2 x$ |
| 19 | 解答题 | $6\pi$ |
| 20 | 解答题 | 当 $a\ne-2$ 时，$y=(C_1+C_2x)e^{-2x}+\dfrac{e^{ax}}{(a+2)^2}$；当 $a=-2$ 时，$y=(C_1+C_2x)e^{-2x}+\dfrac{1}{2}x^2e^{-2x}$。 |

## 详细解析

### 第 1 题

- 答案：$y-\dfrac{1}{8}=3\left(x-\dfrac{3\sqrt{3}}{8}\right)$

当 $t=\dfrac{\pi}{6}$ 时，点为 $\left(\dfrac{3\sqrt{3}}{8},\dfrac{1}{8}\right)$。由

$$
\frac{dy}{dx}=\frac{dy/dt}{dx/dt}=\frac{3\sin^2 t\cos t}{-3\cos^2 t\sin t}=-\tan t
$$

得切线斜率为 $-\dfrac{1}{\sqrt{3}}$，故法线斜率为 $\sqrt{3}=3\cdot\dfrac{1}{\sqrt{3}}$，整理得所求方程。

### 第 2 题

- 答案：$e^{\tan\frac{1}{x}}\left(\sec^2\frac{1}{x}\sin\frac{1}{x}+\cos\frac{1}{x}\right)\left(-\dfrac{1}{x^2}\right)dx$

把 $y$ 看成两函数乘积，先求导再乘 $dx$：

$$
y'=e^{\tan\frac{1}{x}}\left(\tan\frac{1}{x}\right)'\sin\frac{1}{x}+e^{\tan\frac{1}{x}}\left(\sin\frac{1}{x}\right)'.
$$

两项都含 $-\dfrac{1}{x^2}$，提取后即可得到所求微分。

### 第 3 题

- 答案：$\dfrac{4}{15}$

令 $u=1-x$，则 $x=1-u$，原积分化为

$$
\int_0^1 (1-u)u^{1/2}\,du=\int_0^1 \left(u^{1/2}-u^{3/2}\right)du,
$$

直接积分得 $\dfrac{2}{3}-\dfrac{2}{5}=\dfrac{4}{15}$。

### 第 4 题

- 答案：$>$

在区间 $[-2,-1]$ 上有 $-x^3>x^3$，指数函数单调递增，所以 $e^{-x^3}>e^{x^3}$。在同一区间积分后不等号方向保持不变。

### 第 5 题

- 答案：$1$

若 $|x|\le1$，则 $f(x)=1$，于是 $f[f(x)]=f(1)=1$；若 $|x|>1$，则 $f(x)=0$，于是 $f[f(x)]=f(0)=1$。故恒有 $f[f(x)]=1$。

### 第 6 题

- 答案：C

将

$$
\frac{x^2}{x+1}=x-1+\frac{1}{x+1}
$$

代入原式，得 $(1-a)x+(-1-b)+\dfrac{1}{x+1}$。极限为零要求一次项与常数项都为零，所以 $a=1,b=-1$。

### 第 7 题

- 答案：B

设 $F'(x)=f(x)$，则 $\int f(x)dx=F(x)+C$。两边取微分得 $d[\int f(x)dx]=dF(x)=F'(x)dx=f(x)dx$。

### 第 8 题

- 答案：A

记 $y=f(x)$。由 $y'=y^2$ 得 $y''=2y^3$，$y'''=3!y^4$。归纳可得 $y^{(n)}=n!y^{n+1}$，故选 A。

### 第 9 题

- 答案：A

用变上限积分求导公式：

$$
F'(x)=f(e^{-x})(e^{-x})'-f(x)\cdot 1=-e^{-x}f(e^{-x})-f(x).
$$

### 第 10 题

- 答案：B

当 $x\to0$ 时，

$$
\frac{f(x)}x\to f'(0)\ne0,
$$

而 $F(0)=f(0)=0$。极限存在但不等于函数值，所以 $x=0$ 是第一类（可去）间断点。

### 第 11 题

- 答案：$a=\ln 3$

由

$$
\frac{x+a}{x-a}=1+\frac{2a}{x-a}
$$

得

$$
\left(\frac{x+a}{x-a}\right)^x\to e^{2a}=9.
$$

于是 $2a=\ln9$，故 $a=\ln3$。

### 第 12 题

- 答案：$dy=\dfrac{3+\ln(x-y)}{2+\ln(x-y)}\,dx$

对方程两边求微分：

$$
2dy-dx=\ln(x-y)(dx-dy)+(x-y)\frac{dx-dy}{x-y}.
$$

整理得

$$
(2+\ln(x-y))dy=(3+\ln(x-y))dx.
$$

故 $dy=\dfrac{3+\ln(x-y)}{2+\ln(x-y)}dx$。

### 第 13 题

- 答案：$\left(\dfrac{1}{\sqrt{3}},\dfrac{3}{4}\right)$

先求二阶导数：

$$
y'=-\frac{2x}{(1+x^2)^2},\qquad y''=\frac{2(3x^2-1)}{(1+x^2)^3}.
$$

令 $y''=0$ 得 $x=\dfrac{1}{\sqrt{3}}$。此点两侧 $y''$ 变号，所以拐点为

$$
\left(\frac{1}{\sqrt{3}},\frac{1}{1+\frac{1}{3}}\right)=\left(\frac{1}{\sqrt{3}},\frac{3}{4}\right).
$$

### 第 14 题

- 答案：$\ln x+\ln\lvert 1-x\rvert-\dfrac{\ln x}{1-x}+C$

注意

$$
\frac{dx}{(1-x)^2}=d\left(\frac{1}{1-x}\right).
$$

分部积分得

$$
\int\frac{\ln x}{(1-x)^2}dx=\frac{\ln x}{1-x}-\int\frac{dx}{x(1-x)}.
$$

再分解

$$
\frac{1}{x(1-x)}=\frac{1}{x}+\frac{1}{1-x},
$$

整理即得答案。

### 第 15 题

- 答案：$y=\dfrac{1+\ln^2 x}{2\ln x}$

方程化为

$$
y'+\frac{1}{x\ln x}y=\frac{1}{x}.
$$

积分因子为 $\mu(x)=\ln x$，所以

$$
(\ln x\cdot y)'=\frac{\ln x}{x}.
$$

积分得 $y\ln x=\dfrac{1}{2}(\ln x)^2+C$。由 $y(e)=1$ 得 $C=\dfrac{1}{2}$，故

$$
y=\frac{1+\ln^2 x}{2\ln x}.
$$

### 第 16 题

- 答案：$P=\left(\dfrac{a}{\sqrt{2}},\dfrac{b}{\sqrt{2}}\right)$

设切点为 $(x,y)$。椭圆在该点的切线可写成

$$
\frac{xX}{a^2}+\frac{yY}{b^2}=1。
$$

它在坐标轴上的截距分别为 $\dfrac{a^2}{x}$ 与 $\dfrac{b^2}{y}$，所围梯形面积等于常数倍 $\dfrac{1}{xy}$，因此只需使 $xy$ 最大。由椭圆约束可得 $xy$ 在第一象限最大时 $x^2/a^2=y^2/b^2=\dfrac{1}{2}$，故

$$
P=\left(\frac{a}{\sqrt{2}},\frac{b}{\sqrt{2}}\right).
$$

### 第 17 题

- 答案：见解析。

令

$$
f(x)=\arctan x+\frac{1}{x}-\frac{\pi}{2}.
$$

则

$$
f'(x)=\frac{1}{1+x^2}-\frac{1}{x^2}=-\frac{1}{x^2(1+x^2)}<0,\quad x>0.
$$

所以 $f(x)$ 在 $(0,+\infty)$ 上单调递减。而

$$
\lim_{x\to+\infty}f(x)=0.
$$

于是对任意 $x>0$，都有 $f(x)>0$，命题得证。

### 第 18 题

- 答案：$\dfrac{1}{2}\ln^2 x$

把 $f\left(\dfrac{1}{x}\right)$ 中积分作代换 $t=\dfrac{1}{u}$，得

$$
f\left(\frac{1}{x}\right)=\int_x^1\frac{\ln u}{u(1+u)}du.
$$

与 $f(x)$ 相加后，可合并为

$$
\int_1^x\frac{\ln t}{t}\,dt=\frac{1}{2}\ln^2 x.
$$

### 第 19 题

- 答案：$6\pi$

设切点为 $(x_0,\sqrt{x_0-2})$。由切线过 $(1,0)$ 可求得 $x_0=3$，切线为 $y=\dfrac{1}{2}x-\dfrac{1}{2}$。所求体积为曲线与直线对应旋转体体积之差：

$$
V=\pi\int_1^3\left(\frac{x-1}{2}\right)^2dx-\pi\int_2^3(x-2)dx=6\pi.
$$

### 第 20 题

- 答案：

$$
\begin{cases}
y=(C_1+C_2x)e^{-2x}+\dfrac{e^{ax}}{(a+2)^2},&a\ne-2,\\[4pt]
y=(C_1+C_2x)e^{-2x}+\dfrac{1}{2}x^2e^{-2x},&a=-2.
\end{cases}
$$

对应齐次方程特征根为二重根 $r=-2$，所以齐次通解为 $(C_1+C_2x)e^{-2x}$。当 $a\ne-2$ 时取特解 $y_p=Ae^{ax}$，代入得 $A=\dfrac{1}{(a+2)^2}$。当 $a=-2$ 时右端与齐次解共振，取特解 $y_p=Ax^2e^{-2x}$，代入得 $A=\dfrac{1}{2}$。
