# Math 2 1993 Answers

资料类型：考研数学二答案解析
年份：1993
科目：数学二
范围：试卷 III
校对状态：已按答案页图像清洗并与题面同步。

## 答案速查

| 题号 | 题型 | 答案 |
|---|---|---|
| 1 | 填空题 | $0$ |
| 2 | 填空题 | $\dfrac{2xy-y^2-e^x-2x\cos(x^2+y^2)}{2y\cos(x^2+y^2)-2xy}$ |
| 3 | 填空题 | $0<x\le \dfrac{1}{4}$ |
| 4 | 填空题 | $\dfrac{2}{\sqrt{\cos x}}+C$ |
| 5 | 填空题 | $\dfrac{1}{2}(1+x^2)\ln(1+x^2)-\dfrac{1}{2}x^2-\dfrac{1}{2}$ |
| 6 | 选择题 | D |
| 7 | 选择题 | A |
| 8 | 选择题 | D |
| 9 | 选择题 | B |
| 10 | 选择题 | C |
| 11 | 解答题 | $y''=4x^2\cos[f(x^2)]f''(x^2)-4x^2\sin[f(x^2)]\bigl(f'(x^2)\bigr)^2+2\cos[f(x^2)]f'(x^2)$ |
| 12 | 解答题 | $-50$ |
| 13 | 解答题 | $\dfrac{\pi}{8}-\dfrac{1}{4}\ln2$ |
| 14 | 解答题 | $\dfrac{1}{2}$ |
| 15 | 解答题 | $y=\dfrac{1-\sin x}{1-x^2}$ |
| 16 | 解答题 | $\alpha=-3,\ \beta=2,\ \gamma=-1$，通解为 $y=C_1e^x+C_2e^{2x}+e^{2x}+(1+x)e^x$ |
| 17 | 解答题 | $\dfrac{\pi^2}{2}-\dfrac{4\pi}{3}$ |
| 18 | 解答题 | 见解析。 |

## 详细解析

### 第 1 题
- 答案：$0$

把原式化为 $\dfrac{\ln x}{1/x}$，为 $\dfrac{-\infty}{+\infty}$ 型，应用洛必达法则：
$$
\lim_{x\to0^+}\frac{\ln x}{1/x}=\lim_{x\to0^+}\frac{1/x}{-1/x^2}=\lim_{x\to0^+}(-x)=0.
$$

### 第 2 题
- 答案：$\dfrac{2xy-y^2-e^x-2x\cos(x^2+y^2)}{2y\cos(x^2+y^2)-2xy}$

对方程两边关于 $x$ 求导：
$$
\cos(x^2+y^2)(2x+2yy')+e^x-y^2-2xyy'=0.
$$
整理含 $y'$ 的项，得
$$
y'\bigl(2y\cos(x^2+y^2)-2xy\bigr)=y^2-e^x-2x\cos(x^2+y^2),
$$
故
$$
\frac{dy}{dx}=\frac{2xy-y^2-e^x-2x\cos(x^2+y^2)}{2y\cos(x^2+y^2)-2xy}.
$$

### 第 3 题
- 答案：$0<x\le \dfrac{1}{4}$

由变上限积分求导公式，
$$
F'(x)=2-\frac{1}{\sqrt{x}}.
$$
单调减少要求 $F'(x)\le 0$，即
$$
2\le \frac{1}{\sqrt{x}}\iff \sqrt{x}\le \frac{1}{2}\iff 0<x\le \frac{1}{4}.
$$

### 第 4 题
- 答案：$\dfrac{2}{\sqrt{\cos x}}+C$

原式化为
$$
\int \sin x\,(\cos x)^{-3/2}dx.
$$
令 $u=\cos x$，则 $du=-\sin x\,dx$，
$$
\int \frac{\tan x}{\sqrt{\cos x}}dx=-\int u^{-3/2}du=2u^{-1/2}+C=\frac{2}{\sqrt{\cos x}}+C.
$$

### 第 5 题
- 答案：$\dfrac{1}{2}(1+x^2)\ln(1+x^2)-\dfrac{1}{2}x^2-\dfrac{1}{2}$

由题意 $f'(x)=x\ln(1+x^2)$。积分得
$$
f(x)=\int x\ln(1+x^2)dx.
$$
令 $u=1+x^2$，$du=2x\,dx$，则
$$
f(x)=\frac{1}{2}\int \ln u\,du=\frac{1}{2}(u\ln u-u)+C.
$$
代回得
$$
f(x)=\frac{1}{2}(1+x^2)\ln(1+x^2)-\frac{1}{2}(1+x^2)+C.
$$
由 $f(0)=-\dfrac{1}{2}$ 得 $C=0$，故
$$
f(x)=\frac{1}{2}(1+x^2)\ln(1+x^2)-\frac{1}{2}x^2-\frac{1}{2}.
$$

### 第 6 题
- 答案：D

取数列 $x_k=\dfrac{1}{k\pi}$，则 $\sin\dfrac{1}{x_k}=0$，原式等于 $0$；再取 $x_k'=\dfrac{2}{(4k+1)\pi}$，则 $\sin\dfrac{1}{x_k'}=1$，原式为 $\dfrac{1}{{x_k'}^2}\to +\infty$。因此它无界，但并不趋于无穷大，选 D。

### 第 7 题
- 答案：A

当 $x>1$ 时，$|x^2-1|=x^2-1$，故 $f(x)=x+1$；当 $x<1$ 时，$|x^2-1|=1-x^2$，故 $f(x)=-(x+1)$。于是
$$
\lim_{x\to1^-}f(x)=-2,\qquad \lim_{x\to1^+}f(x)=2.
$$
左右极限不相等，因此在 $x=1$ 处不连续，选 A。

### 第 8 题
- 答案：D

当 $0\le x<1$ 时，
$$
F(x)=\int_1^x t^2dt=-\int_x^1 t^2dt=\frac{x^3}{3}-\frac{1}{3}.
$$
当 $1\le x\le2$ 时，
$$
F(x)=\int_1^x 1\,dt=x-1.
$$
故选 D。

### 第 9 题
- 答案：B

求导得
$$
f'(x)=\frac{1}{x}-\frac{1}{e}.
$$
唯一驻点为 $x=e$，且在 $(0,e)$ 上递增，在 $(e,+\infty)$ 上递减，因此 $x=e$ 是最大值点。又
$$
f(e)=1-1+k=k>0,
$$
且当 $x\to0^+$ 或 $x\to+\infty$ 时，$f(x)\to-\infty$。故在 $(0,e)$ 和 $(e,+\infty)$ 内各有一个零点，共 2 个，选 B。

### 第 10 题
- 答案：C

由 $f(-x)=-f(x)$ 知 $f$ 为奇函数。对等式求导得
$$
f'(-x)=f'(x),
$$
所以 $f'$ 为偶函数；再求导得
$$
f''(-x)=-f''(x),
$$
所以 $f''$ 为奇函数。若 $x<0$，则 $-x>0$，因此
$$
f'(x)=f'(-x)>0,\qquad f''(x)=-f''(-x)<0.
$$
故选 C。

### 第 11 题
- 答案：$y''=4x^2\cos[f(x^2)]f''(x^2)-4x^2\sin[f(x^2)]\bigl(f'(x^2)\bigr)^2+2\cos[f(x^2)]f'(x^2)$

先求一阶导数：
$$
y'=\cos[f(x^2)]\cdot f'(x^2)\cdot 2x.
$$
再对其求导，乘积法则与链式法则给出
$$
y''=2\cos[f(x^2)]f'(x^2)+2x\frac{d}{dx}\Bigl(\cos[f(x^2)]f'(x^2)\Bigr).
$$
继续展开得
$$
y''=2\cos[f(x^2)]f'(x^2)+4x^2\cos[f(x^2)]f''(x^2)-4x^2\sin[f(x^2)]\bigl(f'(x^2)\bigr)^2.
$$

### 第 12 题
- 答案：$-50$

将根式有理化：
$$
x(\sqrt{x^2+100}+x)=\frac{100x}{\sqrt{x^2+100}-x}.
$$
因为 $x<0$，有 $\sqrt{x^2+100}=|x|\sqrt{1+100/x^2}=-x\sqrt{1+100/x^2}$，于是
$$
\sqrt{x^2+100}-x\to -2x.
$$
更直接地，将分子分母同除以 $x$，得
$$
\frac{100}{\sqrt{1+100/x^2}-1}\cdot\frac{1}{1}
$$
注意此处 $x<0$，等价写成
$$
\sqrt{x^2+100}+x=\frac{100}{\sqrt{x^2+100}-x}\sim\frac{100}{-2x}=-\frac{50}{x},
$$
所以原极限为 $-50$。

### 第 13 题
- 答案：$\dfrac{\pi}{8}-\dfrac{1}{4}\ln2$

利用恒等式 $1+\cos 2x=2\cos^2x$，原式化为
$$
\frac{1}{2}\int_0^{\pi/4}x\sec^2x\,dx.
$$
分部积分，取 $u=x,\,dv=\sec^2x\,dx$，则 $du=dx,\,v=\tan x$，于是
$$
\frac{1}{2}\left[x\tan x\right]_0^{\pi/4}-\frac{1}{2}\int_0^{\pi/4}\tan x\,dx.
$$
又
$$
\int_0^{\pi/4}\tan x\,dx=-\ln(\cos x)\Big|_0^{\pi/4}=\frac{1}{2}\ln2,
$$
故原积分为
$$
\frac{1}{2}\cdot\frac{\pi}{4}-\frac{1}{2}\cdot\frac{1}{2}\ln2=\frac{\pi}{8}-\frac{1}{4}\ln2.
$$

### 第 14 题
- 答案：$\dfrac{1}{2}$

令 $u=1+x$，则
$$
\int_0^{+\infty}\frac{x}{(1+x)^3}dx=\int_1^{+\infty}\frac{u-1}{u^3}du=\int_1^{+\infty}\left(\frac{1}{u^2}-\frac{1}{u^3}\right)du.
$$
积分得
$$
\left[-\frac{1}{u}+\frac{1}{2u^2}\right]_1^{+\infty}=0-\left(-1+\frac{1}{2}\right)=\frac{1}{2}.
$$

### 第 15 题
- 答案：$y=\dfrac{1-\sin x}{1-x^2}$

方程化为
$$
y'+\frac{2x}{x^2-1}y=\frac{\cos x}{x^2-1}.
$$
积分因子为
$$
\mu(x)=\exp\int\frac{2x}{x^2-1}dx=x^2-1.
$$
因此
$$
\bigl((x^2-1)y\bigr)'=\cos x,
$$
积分得
$$
(x^2-1)y=\sin x+C.
$$
由 $y(0)=1$ 得 $-1=C$，所以
$$
y=\frac{\sin x-1}{x^2-1}=\frac{1-\sin x}{1-x^2}.
$$

### 第 16 题
- 答案：$\alpha=-3,\ \beta=2,\ \gamma=-1$，通解为 $y=C_1e^x+C_2e^{2x}+e^{2x}+(1+x)e^x$

将特解
$$
y_p=e^{2x}+(1+x)e^x
$$
代入原方程。计算得
$$
y_p'=2e^{2x}+(x+2)e^x,\qquad y_p''=4e^{2x}+(x+3)e^x.
$$
代入后比较 $e^{2x}$、$xe^x$、$e^x$ 的系数，得方程组
$$
4+2\alpha+\beta=0,\quad 1+\alpha+\beta=0,\quad 3+2\alpha+\beta=\gamma.
$$
解得
$$
\alpha=-3,\quad \beta=2,\quad \gamma=-1.
$$
齐次方程为
$$
y''-3y'+2y=0,
$$
特征方程 $r^2-3r+2=0$，根为 $1,2$，故齐次通解
$$
y_h=C_1e^x+C_2e^{2x}.
$$
于是原方程通解为
$$
y=y_h+y_p=C_1e^x+C_2e^{2x}+e^{2x}+(1+x)e^x.
$$

### 第 17 题
- 答案：$\dfrac{\pi^2}{2}-\dfrac{4\pi}{3}$

区域满足
$$
(x-1)^2+y^2\le1,\qquad y\ge x.
$$
交点由 $y=x$ 与圆联立得
$$
2x^2-2x=0\Rightarrow x=0,1,
$$
对应 $y=0,1$。取 $y$ 为积分变量，则左、右边界分别为
$$
x=1-\sqrt{1-y^2},\qquad x=y\quad(0\le y\le1).
$$
绕直线 $x=2$ 旋转，用圆环法：外半径
$$
R=2-(1-\sqrt{1-y^2})=1+\sqrt{1-y^2},
$$
内半径
$$
r=2-y.
$$
故体积
$$
V=\pi\int_0^1\bigl(R^2-r^2\bigr)dy.
$$
展开并积分得
$$
V=\pi\int_0^1\left[2+2\sqrt{1-y^2}-y^2-(4-4y+y^2)\right]dy
=\pi\left(-\frac{4}{3}+\frac{\pi}{2}\right)=\frac{\pi^2}{2}-\frac{4\pi}{3}.
$$

### 第 18 题
- 答案：见解析。

两边取自然对数，只需证明
$$
a\ln(a+x)<(a+x)\ln a.
$$
移项后记
$$
\phi(x)=(a+x)\ln a-a\ln(a+x).
$$
则
$$
\phi'(x)=\ln a-\frac{a}{a+x}.
$$
因为 $a>e$，故 $\ln a>1$；又对任意 $x>0$，有 $\dfrac{a}{a+x}<1$，于是
$$
\phi'(x)>0.
$$
所以 $\phi(x)$ 在 $(0,+\infty)$ 上递增，而
$$
\phi(0)=a\ln a-a\ln a=0.
$$
因此 $x>0$ 时 $\phi(x)>0$，即
$$
(a+x)\ln a-a\ln(a+x)>0,
$$
从而
$$
a\ln(a+x)<(a+x)\ln a.
$$
指数化便得
$$
(a+x)^a<a^{a+x}.
$$
