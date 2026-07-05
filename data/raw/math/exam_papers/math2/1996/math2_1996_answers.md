# Math 2 1996 Answers

资料类型：考研数学二答案解析
年份：1996
科目：数学二
范围：试卷 III
校对状态：已按答案页图像清洗并与题面同步。

## 答案速查

| 题号 | 题型 | 答案 |
|---|---|---|
| 1 | 填空题 | $\dfrac{1}{3}$ |
| 2 | 填空题 | $2$ |
| 3 | 填空题 | $y=e^{-x}(C_1\cos2x+C_2\sin2x)$ |
| 4 | 填空题 | $2$ |
| 5 | 填空题 | $\ln2-\dfrac12$ |
| 6 | 选择题 | A |
| 7 | 选择题 | C |
| 8 | 选择题 | D |
| 9 | 选择题 | C |
| 10 | 选择题 | B |
| 11 | 解答题 | $\dfrac{4}{f(t^2)}\left[f'(t^2)+2t^2f''(t^2)\right]$ |
| 12 | 解答题 | $\tan x-\sec x+C$ |
| 13 | 解答题 | $\dfrac{1-x}{1+x}=1-2x+2x^2+\cdots+(-1)^n2x^n+(-1)^{n+1}\dfrac{2x^{n+1}}{(1+\theta x)^{n+2}}\ (0<\theta<1)$ |
| 14 | 解答题 | $y=c_1+c_2e^{-x}+\dfrac{x^3}{3}-x^2+2x$ |
| 15 | 解答题 | $-\dfrac{\arctan x}{x}+\ln\lvert x\rvert-\dfrac12\ln(1+x^2)-\dfrac12\arctan^2x+C$ |
| 16 | 解答题 | $V=\dfrac{2}{3}a^2b\tan\alpha$ |
| 17 | 解答题 | $-\dfrac{1}{x}\arctan x+\ln\lvert x\rvert-\dfrac12\ln(1+x^2)-\dfrac12\arctan^2x+C$ |
| 18 | 解答题 | $g(x)=\begin{cases}-\sqrt{\dfrac{1-x}{2}},&x<-1,\\ \sqrt[3]{x},&-1\le x\le8,\\ \dfrac{x+16}{12},&x>8,\end{cases}$；$g(x)$ 无间断点，在 $x=-1,0$ 处不可导 |
| 19 | 解答题 | $(1,1)$；且在该点取极小值 |
| 20 | 证明题 | 见解析 |
| 21 | 解答题 | $y(x)=e^{-ax}\int_0^x e^{at}f(t)\,dt$，且当 $x\ge0$ 时 $\lvert y(x)\rvert\le\dfrac{k}{a}(1-e^{-ax})$ |

## 详细解析

### 第 1 题

- 答案：$\dfrac{1}{3}$

设
$$
u=x+e^{-x/2},
$$
则
$$
y=u^{2/3},\qquad y'=\frac23u^{-1/3}u'.
$$
当 $x=0$ 时，
$$
u(0)=1,\qquad u'(0)=1-\frac12e^0=\frac12.
$$
所以
$$
y'(0)=\frac23\cdot1^{-1/3}\cdot\frac12=\frac13.
$$

### 第 2 题

- 答案：$2$

展开被积式：
$$
\left(x+\sqrt{1-x^2}\right)^2=x^2+1-x^2+2x\sqrt{1-x^2}=1+2x\sqrt{1-x^2}.
$$
其中 $2x\sqrt{1-x^2}$ 是奇函数，在 $[-1,1]$ 上积分为 $0$，故
$$
\int_{-1}^{1}\left(x+\sqrt{1-x^2}\right)^2dx=\int_{-1}^{1}1\,dx=2.
$$

### 第 3 题

- 答案：$y=e^{-x}(C_1\cos2x+C_2\sin2x)$

特征方程为
$$
r^2+2r+5=0,
$$
解得
$$
r=-1\pm2i.
$$
因而通解为
$$
y=e^{-x}(C_1\cos2x+C_2\sin2x).
$$

### 第 4 题

- 答案：$2$

当 $x\to\infty$ 时，
$$
\ln\left(1+\frac{k}{x}\right)\sim\frac{k}{x},\qquad
\sin t\sim t.
$$
因此
$$
\sin\ln\left(1+\frac{3}{x}\right)-\sin\ln\left(1+\frac{1}{x}\right)
\sim \frac{3}{x}-\frac{1}{x}=\frac{2}{x}.
$$
故原极限为
$$
\lim_{x\to\infty}x\cdot\frac{2}{x}=2.
$$

### 第 5 题

- 答案：$\ln2-\dfrac12$

先求曲线与直线 $y=2$ 的交点：
$$
x+\frac1x=2\iff (x-1)^2=0,
$$
所以交点在 $x=1$。在区间 $[1,2]$ 上曲线位于直线 $y=2$ 上方，故
$$
S=\int_1^2\left(x+\frac1x-2\right)dx
=\left[\frac{x^2}{2}+\ln x-2x\right]_1^2
=\ln2-\frac12.
$$

### 第 6 题

- 答案：A

由
$$
e^x=1+x+\frac{x^2}{2}+o(x^2),
$$
得
$$
e^x-(ax^2+bx+1)=(1-b)x+\left(\frac12-a\right)x^2+o(x^2).
$$
因为它是比 $x^2$ 高阶的无穷小，所以一次项和二次项系数都应为 $0$，即
$$
1-b=0,\qquad \frac12-a=0.
$$
故
$$
a=\frac12,\qquad b=1.
$$
选 A。

### 第 7 题

- 答案：C

由 $|f(x)|\le x^2$，令 $x=0$ 可得 $f(0)=0$。于是
$$
\left|\frac{f(x)-f(0)}{x}\right|=\left|\frac{f(x)}{x}\right|\le |x|\to0\quad(x\to0).
$$
因而极限存在且等于 $0$，即
$$
f'(0)=\lim_{x\to0}\frac{f(x)-f(0)}{x}=0.
$$
所以 $x=0$ 是可导点，且 $f'(0)=0$，选 C。

### 第 8 题

- 答案：D

A、B、C 都可由反例排除，例如取 $f(x)=x$ 或 $f(x)=e^{-x}$ 等即可。

对 D，若 $\lim\limits_{x\to+\infty}f'(x)=+\infty$，则存在 $X$，当 $x>X$ 时有 $f'(x)>1$。对任意 $x>X$，由拉格朗日中值定理，
$$
f(x)-f(X)=f'(\xi)(x-X)>x-X\qquad (\xi\in(X,x)).
$$
因而
$$
f(x)>f(X)+x-X\to+\infty.
$$
所以 D 正确。

### 第 9 题

- 答案：C

令
$$
F(x)=|x|^{1/4}+|x|^{1/2}-\cos x.
$$
这是偶函数，所以其零点关于原点对称。只需考察 $x\ge0$。

当 $x=0$ 时，$F(0)=-1<0$；当 $x=\dfrac{\pi}{2}$ 时，
$$
F\left(\frac\pi2\right)=\left(\frac\pi2\right)^{1/4}+\left(\frac\pi2\right)^{1/2}>0.
$$
故在 $(0,\pi/2)$ 内至少有一个零点。

对 $x>0$，
$$
F'(x)=\frac{1}{4x^{3/4}}+\frac{1}{2x^{1/2}}+\sin x>0
$$
在 $(0,\pi/2)$ 上成立，所以该区间内零点唯一。又当 $x\ge\pi/2$ 时，$\cos x\le0$，而前两项非负，故不再有正根。

因为 $F$ 为偶函数，所以总共有两个实根。选 C。

### 第 10 题

- 答案：B

绕直线 $y=m$ 旋转时，外半径为 $m-g(x)$，内半径为 $m-f(x)$。由垫片法，
$$
V=\int_a^b\pi\Big[(m-g(x))^2-(m-f(x))^2\Big]dx.
$$
展开得
$$
(m-g)^2-(m-f)^2=(f-g)(2m-f-g),
$$
所以
$$
V=\int_a^b\pi[2m-f(x)-g(x)][f(x)-g(x)]dx.
$$
选 B。

### 第 11 题

- 答案：$\dfrac{4}{f(t^2)}\left[f'(t^2)+2t^2f''(t^2)\right]$

这是由参数方程所确定的函数，其导数为
$$
\frac{dy}{dx}=\frac{dy/dt}{dx/dt}
=\frac{2f(t^2)\cdot f'(t^2)\cdot2t}{f(t^2)}
=4t f'(t^2).
$$
所以
$$
\frac{d^2y}{dx^2}
=\frac{d}{dt}\left(\frac{dy}{dx}\right)\cdot\frac{dt}{dx}
=\frac{d}{dt}\bigl(4tf'(t^2)\bigr)\cdot\frac{1}{f(t^2)}.
$$
计算得
$$
\frac{d}{dt}\bigl(4tf'(t^2)\bigr)=4f'(t^2)+8t^2f''(t^2),
$$
故
$$
\frac{d^2y}{dx^2}
=\frac{4}{f(t^2)}\left[f'(t^2)+2t^2f''(t^2)\right].
$$

### 第 12 题

- 答案：$\tan x-\sec x+C$

将分母有理化：
$$
\int\frac{dx}{1+\sin x}
=\int\frac{1-\sin x}{(1+\sin x)(1-\sin x)}dx
=\int\frac{1-\sin x}{\cos^2x}dx.
$$
因而
$$
\int\frac{dx}{1+\sin x}
=\int\sec^2x\,dx-\int\frac{\sin x}{\cos^2x}dx
=\tan x-\sec x+C.
$$

### 第 13 题

- 答案：$\dfrac{1-x}{1+x}=1-2x+2x^2+\cdots+(-1)^n2x^n+(-1)^{n+1}\dfrac{2x^{n+1}}{(1+\theta x)^{n+2}}\ (0<\theta<1)$

对于函数
$$
f(x)=\frac{1-x}{1+x}=\frac{2}{1+x}-1,
$$
有
$$
f^{(n)}(x)=2(-1)^n n!(1+x)^{-(n+1)}\qquad (n\ge1),
$$
因而
$$
f^{(n)}(0)=2(-1)^n n!.
$$
由带拉格朗日余项的泰勒公式，
$$
f(x)=f(0)+f'(0)x+\cdots+\frac{f^{(n)}(0)}{n!}x^n+\frac{f^{(n+1)}(\theta x)}{(n+1)!}x^{n+1},
\qquad 0<\theta<1.
$$
代入各阶导数得
$$
\frac{1-x}{1+x}
=1-2x+2x^2+\cdots+(-1)^n2x^n+(-1)^{n+1}\frac{2x^{n+1}}{(1+\theta x)^{n+2}},
\qquad 0<\theta<1.
$$

### 第 14 题

- 答案：$y=c_1+c_2e^{-x}+\dfrac{x^3}{3}-x^2+2x$

对应齐次方程
$$
y''+y'=0
$$
的特征方程为
$$
r^2+r=0,
$$
故齐次通解为
$$
y_h=c_1+c_2e^{-x}.
$$
设非齐次方程的一个特解为
$$
y_p=x(ax^2+bx+c),
$$
代入原方程比较系数，可得
$$
a=\frac13,\qquad b=-1,\qquad c=2.
$$
因而
$$
y_p=\frac{x^3}{3}-x^2+2x.
$$
所以通解为
$$
y=c_1+c_2e^{-x}+\frac{x^3}{3}-x^2+2x.
$$

### 第 15 题

- 答案：$-\dfrac{\arctan x}{x}+\ln\lvert x\rvert-\dfrac12\ln(1+x^2)-\dfrac12\arctan^2x+C$

先拆分为
$$
\int\frac{\arctan x}{x^2(1+x^2)}dx
=\int\frac{\arctan x}{x^2}dx-\int\frac{\arctan x}{1+x^2}dx.
$$
第一项分部积分，取
$$
u=\arctan x,\qquad dv=\frac{dx}{x^2},
$$
则
$$
du=\frac{dx}{1+x^2},\qquad v=-\frac1x.
$$
因而
$$
\int\frac{\arctan x}{x^2}dx
=-\frac{\arctan x}{x}+\int\frac{dx}{x(1+x^2)}.
$$
又
$$
\int\frac{dx}{x(1+x^2)}=\int\left(\frac1x-\frac{x}{1+x^2}\right)dx
=\ln\lvert x\rvert-\frac12\ln(1+x^2).
$$
第二项由 $t=\arctan x$ 得
$$
\int\frac{\arctan x}{1+x^2}dx=\frac12\arctan^2x.
$$
综上，
$$
\int\frac{\arctan x}{x^2(1+x^2)}dx
=-\frac{\arctan x}{x}+\ln\lvert x\rvert-\frac12\ln(1+x^2)-\frac12\arctan^2x+C.
$$

### 第 16 题

- 答案：$V=\dfrac{2}{3}a^2b\tan\alpha$

建立坐标系，底面椭圆方程为
$$
\frac{x^2}{a^2}+\frac{y^2}{b^2}=1.
$$
取垂直于 $y$ 轴的平面去截该楔形体，所得截面是直角三角形。其中一条直角边长为
$$
x=\frac{a}{b}\sqrt{b^2-y^2},
$$
另一条直角边长为
$$
x\tan\alpha=\frac{a}{b}\sqrt{b^2-y^2}\tan\alpha.
$$
所以截面面积为
$$
S(y)=\frac12\cdot\frac{a^2}{b^2}(b^2-y^2)\tan\alpha.
$$
由对称性，
$$
V=2\int_0^b S(y)dy
=\frac{a^2}{b^2}\tan\alpha\int_0^b(b^2-y^2)dy
=\frac{2}{3}a^2b\tan\alpha.
$$

### 第 17 题

- 答案：$-\dfrac{1}{x}\arctan x+\ln\lvert x\rvert-\dfrac12\ln(1+x^2)-\dfrac12\arctan^2x+C$

将原式拆为
$$
\int\frac{\arctan x}{x^2(1+x^2)}dx
=\int\frac{\arctan x}{x^2}dx-\int\frac{\arctan x}{1+x^2}dx.
$$
对第一项作分部积分：
$$
u=\arctan x,\quad dv=\frac{dx}{x^2},
$$
则
$$
du=\frac{dx}{1+x^2},\quad v=-\frac1x.
$$
所以
$$
\int\frac{\arctan x}{x^2}dx
=-\frac{\arctan x}{x}+\int\frac{dx}{x(1+x^2)}.
$$
又
$$
\int\frac{dx}{x(1+x^2)}
=\int\left(\frac1x-\frac{x}{1+x^2}\right)dx
=\ln\lvert x\rvert-\frac12\ln(1+x^2).
$$
第二项令 $t=\arctan x$，则
$$
\int\frac{\arctan x}{1+x^2}dx=\frac12\arctan^2x.
$$
因而
$$
\int\frac{\arctan x}{x^2(1+x^2)}dx
=-\frac{1}{x}\arctan x+\ln\lvert x\rvert-\frac12\ln(1+x^2)-\frac12\arctan^2x+C.
$$

### 第 18 题

- 答案：$g(x)=\begin{cases}-\sqrt{\dfrac{1-x}{2}},&x<-1,\\ \sqrt[3]{x},&-1\le x\le8,\\ \dfrac{x+16}{12},&x>8,\end{cases}$；$g(x)$ 无间断点，在 $x=-1,0$ 处不可导

由各分段单调性可知 $f(x)$ 在 $(-\infty,+\infty)$ 上单调递增且连续，因此存在反函数。三段分别求反解得
$$
g(x)=
\begin{cases}
-\sqrt{\dfrac{1-x}{2}}, & x<-1,\\
\sqrt[3]{x}, & -1\le x\le8,\\
\dfrac{x+16}{12}, & x>8.
\end{cases}
$$

因为三段在拼接点处满足
$$
g(-1^-)=g(-1^+)=-1,\qquad g(8^-)=g(8^+)=2,
$$
所以 $g(x)$ 在全体实数上连续，没有间断点。

再考察可导性：$\sqrt[3]{x}$ 在 $x=0$ 处不可导；在 $x=-1$ 处，
$$
g'_-( -1 )=\frac14,\qquad g'_+( -1 )=\frac13,
$$
左右导数不相等，故也不可导。至于 $x=8$，左右导数都等于 $\dfrac{1}{12}$，故可导。

因此，$g(x)$ 无间断点，仅在 $x=-1,0$ 两点不可导。

### 第 19 题

- 答案：$(1,1)$；且在该点取极小值

对方程两边关于 $x$ 求导，得
$$
6y^2y'-4yy'+2xy'+2y-2x=0,
$$
即
$$
(3y^2-2y+x)y'+y-x=0.
$$
因而
$$
y'=\frac{x-y}{3y^2-2y+x}.
$$
驻点满足 $y'=0$，于是 $x=y$。代回原方程：
$$
2x^3-x^2-1=0=(x-1)(2x^2+x+1).
$$
只有实根 $x=1$，故唯一驻点为
$$
(x,y)=(1,1).
$$

再对导数关系求导，或直接利用隐函数二阶导数公式，在点 $(1,1)$ 处代入 $y'=0$ 可得
$$
2y''-1=0,
$$
即
$$
y''\big|_{x=1}=\frac12>0.
$$
所以点 $(1,1)$ 是极小值点。

### 第 20 题

- 答案：见解析

先证存在 $\xi\in(a,b)$，使 $f(\xi)=0$。

不妨设 $f'(a)>0,f'(b)>0$（若同为负，论证完全类似）。由导数定义与局部保号性，可知在 $a$ 的某个右邻域内有 $f(x)>0$；同理，在 $b$ 的某个左邻域内有 $f(x)<0$。于是存在
$$
x_1,x_2\in(a,b),\qquad x_1<x_2,
$$
使得
$$
f(x_1)>0,\qquad f(x_2)<0.
$$
由零点定理，存在
$$
\xi\in(x_1,x_2)\subset(a,b)
$$
使
$$
f(\xi)=0.
$$

再证存在 $\eta\in(a,b)$，使 $f''(\eta)=0$。由于
$$
f(a)=f(\xi)=f(b)=0,
$$
根据罗尔定理，在区间 $(a,\xi)$ 与 $(\xi,b)$ 内分别存在
$$
\eta_1\in(a,\xi),\qquad \eta_2\in(\xi,b)
$$
使
$$
f'(\eta_1)=0,\qquad f'(\eta_2)=0.
$$
再对函数 $f'(x)$ 在区间 $[\eta_1,\eta_2]$ 上应用罗尔定理，得存在
$$
\eta\in(\eta_1,\eta_2)\subset(a,b)
$$
使
$$
f''(\eta)=0.
$$
结论得证。

### 第 21 题

- 答案：$y(x)=e^{-ax}\int_0^x e^{at}f(t)\,dt$，且当 $x\ge0$ 时 $\lvert y(x)\rvert\le\dfrac{k}{a}(1-e^{-ax})$

这是一个一阶线性非齐次微分方程。由通解公式，
$$
y(x)=e^{-ax}\left[\int f(x)e^{ax}dx+C\right].
$$
设 $F(x)$ 是 $f(x)e^{ax}$ 的一个原函数，则
$$
y(x)=e^{-ax}[F(x)+C].
$$
由初值条件 $y(0)=0$ 得
$$
C=-F(0).
$$
因而
$$
y(x)=e^{-ax}[F(x)-F(0)]
=e^{-ax}\int_0^x e^{at}f(t)dt.
$$

当 $x\ge0$ 且 $|f(x)|\le k$ 时，
$$
\lvert y(x)\rvert
=e^{-ax}\left|\int_0^x e^{at}f(t)dt\right|
\le e^{-ax}\int_0^x e^{at}|f(t)|dt
\le ke^{-ax}\int_0^x e^{at}dt.
$$
计算可得
$$
\lvert y(x)\rvert\le ke^{-ax}\cdot\frac{e^{ax}-1}{a}
=\frac{k}{a}(1-e^{-ax}).
$$
证毕。
