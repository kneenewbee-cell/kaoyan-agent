# Math 1 1999 Answers

资料类型：考研数学一答案解析
年份：1999
科目：数学一
范围：试卷 I
来源：D:\百度网盘\高数资料\【02】1987-2022年数学一真题详解答案（PDF）\1999考研数学一真题解析.pdf
校对状态：已按题干和答案页图像重新清洗，去除 OCR 碎行、串题内容和非本题页脚

## 答案速查

| 题号 | 题型 | 答案 |
|---|---|---|
| 1 | 填空题 | $\dfrac{1}{3}$ |
| 2 | 填空题 | $\sin x^2$ |
| 3 | 填空题 | $y=C_1e^{-2x}+\left(C_2+\dfrac{1}{4}x\right)e^{2x}$ |
| 4 | 填空题 | $n$，$0$（$0$ 为 $n-1$ 重特征值） |
| 5 | 填空题 | $\dfrac{1}{4}$ |
| 6 | 选择题 | A |
| 7 | 选择题 | D |
| 8 | 选择题 | C |
| 9 | 选择题 | B |
| 10 | 选择题 | B |
| 11 | 解答题 | $\displaystyle \frac{dz}{dx}=\frac{(f+xf')F_y-xf'F_x}{F_y+xf'F_z}$ |
| 12 | 解答题 | $\left(\dfrac{\pi}{2}+2\right)a^2b-\dfrac{\pi}{2}a^3$ |
| 13 | 解答题 | $y=e^x$ |
| 14 | 解答题 | 见解析 |
| 15 | 解答题 | $91500\,\mathrm{J}$ |
| 16 | 解答题 | $\dfrac{3\pi}{2}$ |
| 17 | 解答题 | (1) $1$；(2) 对任意 $\lambda>0$ 均收敛 |
| 18 | 解答题 | $a=2,\ b=-3,\ c=2,\ \lambda_0=1$ |
| 19 | 解答题 | 见解析 |
| 20 | 解答题 | $\begin{array}{c\|ccc\|c}  &y_1&y_2&y_3&p_{i\cdot}\\ \hline x_1&\frac{1}{24}&\frac{1}{8}&\frac{1}{12}&\frac{1}{4}\\ x_2&\frac{1}{8}&\frac{3}{8}&\frac{1}{4}&\frac{3}{4}\\ \hline p_{\cdot j}&\frac{1}{6}&\frac{1}{2}&\frac{1}{3}&1 \end{array}$ |
| 21 | 解答题 | $\hat\theta=2\overline X,\qquad D(\hat\theta)=\dfrac{\theta^2}{5n}$ |

## 详细解析

### 第 1 题
- 答案：$\dfrac{1}{3}$

原式化为
$$
\frac{1}{x^2}-\frac{1}{x\tan x}
=\frac{\tan x-x}{x^2\tan x}.
$$

当 $x\to0$ 时，$\tan x\sim x$，且
$$
\tan x-x\sim \frac{x^3}{3}.
$$

因此
$$
\lim_{x\to0}\frac{\tan x-x}{x^2\tan x}
=\lim_{x\to0}\frac{x^3/3}{x^3}
=\frac{1}{3}.
$$

### 第 2 题
- 答案：$\sin x^2$

令
$$
u=x-t,
$$
则 $dt=-du$。当 $t=0$ 时 $u=x$，当 $t=x$ 时 $u=0$，所以
$$
\int_0^x\sin\bigl((x-t)^2\bigr)\,dt
=\int_0^x\sin u^2\,du.
$$

由变上限积分求导公式，
$$
\frac{d}{dx}\int_0^x\sin u^2\,du=\sin x^2.
$$

这里平方在正弦函数的自变量内，即答案为 $\sin(x^2)$。

### 第 3 题
- 答案：$y=C_1e^{-2x}+\left(C_2+\dfrac{1}{4}x\right)e^{2x}$

齐次方程
$$
y''-4y=0
$$
的特征方程为
$$
r^2-4=0,
$$
故齐次通解为
$$
y_h=C_1e^{-2x}+C_2e^{2x}.
$$

右端 $e^{2x}$ 与齐次解中的 $e^{2x}$ 重合，设特解
$$
y_p=Axe^{2x}.
$$

代入 $y''-4y=e^{2x}$ 得
$$
4Ae^{2x}=e^{2x},
$$
故 $A=\dfrac{1}{4}$。

因此通解为
$$
y=C_1e^{-2x}+\left(C_2+\frac{1}{4}x\right)e^{2x}.
$$

### 第 4 题
- 答案：$n$，$0$（$0$ 为 $n-1$ 重特征值）

矩阵 $A$ 的每个元素都是 $1$。记
$$
\boldsymbol e=(1,1,\ldots,1)^T,
$$
则
$$
A\boldsymbol e=n\boldsymbol e,
$$
所以 $n$ 是一个特征值。

若向量 $\boldsymbol x$ 满足各分量之和为 $0$，则
$$
A\boldsymbol x=\boldsymbol 0.
$$
这样的向量空间维数为 $n-1$，所以 $0$ 是 $n-1$ 重特征值。

故 $A$ 的 $n$ 个特征值为
$$
n,\ 0,\ldots,0.
$$

### 第 5 题
- 答案：$\dfrac{1}{4}$

设
$$
P(A)=P(B)=P(C)=p.
$$

三事件两两相互独立，且 $ABC=\varnothing$，故
$$
P(AB)=P(AC)=P(BC)=p^2,\qquad P(ABC)=0.
$$

由加法公式，
$$
P(A\cup B\cup C)
=3p-3p^2.
$$

题设给出
$$
3p-3p^2=\frac{9}{16}.
$$

化简得
$$
p^2-p+\frac{3}{16}=0,
$$
解得
$$
p=\frac{3}{4}\quad\text{或}\quad p=\frac{1}{4}.
$$

又 $p<\dfrac{1}{2}$，所以
$$
P(A)=p=\frac{1}{4}.
$$

### 第 6 题
- 答案：A

若 $f$ 为奇函数，取
$$
F(x)=\int_0^x f(t)\,dt+C.
$$

则
$$
F(-x)=\int_0^{-x}f(t)\,dt+C
=\int_0^x f(-u)\,du+C
=\int_0^x f(u)\,du+C=F(x).
$$
所以原函数可为偶函数，且任一原函数只差常数，仍为偶函数。

其余选项可举反例：偶函数 $f(x)=x^2$ 的原函数不必为奇函数；周期函数的原函数不必周期；单调增函数 $f(x)=x$ 的原函数 $\frac{1}{2}x^2+C$ 不在全轴单调增。

选 A。

### 第 7 题
- 答案：D

先看连续性。右侧
$$
\frac{1-\cos x}{\sqrt x}\sim\frac{x^2/2}{\sqrt x}=\frac{1}{2}x^{3/2}\to0,
\qquad x\to0^+.
$$

左侧 $x^2g(x)\to0$，因为 $g(x)$ 有界。因此 $f(0)=0$ 且函数在 $0$ 处连续。

再看导数：
$$
f'_+(0)=\lim_{x\to0^+}\frac{(1-\cos x)/\sqrt x}{x}
=\lim_{x\to0^+}\frac{1-\cos x}{x\sqrt x}=0,
$$
$$
f'_-(0)=\lim_{x\to0^-}\frac{x^2g(x)}x
=\lim_{x\to0^-}xg(x)=0.
$$

左右导数相等，所以 $f$ 在 $x=0$ 处可导，选 D。

### 第 8 题
- 答案：C

该余弦级数对应把 $f$ 从 $[0,1]$ 作偶延拓，再作周期为 $2$ 的周期延拓。

所以
$$
S\left(-\frac{5}{2}\right)=S\left(-\frac{1}{2}\right)=S\left(\frac{1}{2}\right).
$$

在 $x=\dfrac{1}{2}$ 处，原函数有跳跃间断。傅里叶级数取左右极限的平均值：
$$
S\left(\frac{1}{2}\right)
=\frac{f(1/2-0)+f(1/2+0)}2
=\frac{\frac{1}{2}+1}{2}
=\frac{3}{4}.
$$

选 C。

### 第 9 题
- 答案：B

$AB$ 是 $m$ 阶方阵，且
$$
r(AB)\le\min\{r(A),r(B)\}\le\min\{m,n\}.
$$

当 $m>n$ 时，
$$
r(AB)\le n<m.
$$
因此 $AB$ 的秩小于阶数，行列式必为零：
$$
\det(AB)=0.
$$

选 B。

### 第 10 题
- 答案：B

独立正态随机变量的线性组合仍服从正态分布。

由 $X\sim N(0,1),\ Y\sim N(1,1)$ 且独立，
$$
X+Y\sim N(1,2),
$$
$$
X-Y\sim N(-1,2).
$$

正态分布关于均值对称，所以
$$
P\{X+Y\le1\}=\frac{1}{2}.
$$

其余选项的临界点不是对应分布的均值，故不等于 $1/2$。选 B。

### 第 11 题
- 答案：$\displaystyle \frac{dz}{dx}=\frac{(f+xf')F_y-xf'F_x}{F_y+xf'F_z}$

以下记
$$
f=f(x+y),\qquad f'=f'(x+y),
$$
并将 $F_x,F_y,F_z$ 理解为 $F(x,y,z)$ 在当前点的偏导数。

对
$$
z=xf(x+y)
$$
两边对 $x$ 求导，得
$$
\frac{dz}{dx}=f+x f'\left(1+\frac{dy}{dx}\right).
$$

整理为
$$
-xf'\frac{dy}{dx}+\frac{dz}{dx}=f+xf'.
$$

对
$$
F(x,y,z)=0
$$
求导，得
$$
F_x+F_y\frac{dy}{dx}+F_z\frac{dz}{dx}=0,
$$
即
$$
F_y\frac{dy}{dx}+F_z\frac{dz}{dx}=-F_x.
$$

解这两个关于 $\dfrac{dy}{dx}$、$\dfrac{dz}{dx}$ 的线性方程，得
$$
\frac{dz}{dx}
=\frac{(f+xf')F_y-xf'F_x}{F_y+xf'F_z}.
$$

### 第 12 题
- 答案：$\left(\dfrac{\pi}{2}+2\right)a^2b-\dfrac{\pi}{2}a^3$

记
$$
P=e^x\sin y-b(x+y),\qquad Q=e^x\cos y-ax.
$$

曲线 $L$ 是上半圆
$$
(x-a)^2+y^2=a^2
$$
从 $A(2a,0)$ 到 $O(0,0)$ 的弧。补上从 $O$ 到 $A$ 的线段 $L_1$，形成正向闭曲线。

由 Green 公式，
$$
\oint_{L+L_1}P\,dx+Q\,dy
=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)dx\,dy.
$$

计算
$$
\frac{\partial Q}{\partial x}=e^x\cos y-a,\qquad
\frac{\partial P}{\partial y}=e^x\cos y-b,
$$
所以差为 $b-a$。半圆面积为 $\dfrac{1}{2}\pi a^2$，故
$$
\oint_{L+L_1}P\,dx+Q\,dy
=\frac{\pi}{2}a^2(b-a).
$$

在线段 $L_1:y=0,\ 0\le x\le2a$ 上，
$$
\int_{L_1}P\,dx+Q\,dy
=\int_0^{2a}[-bx]\,dx=-2a^2b.
$$

因此
$$
I=\int_LP\,dx+Q\,dy
=\frac{\pi}{2}a^2(b-a)-(-2a^2b)
=\left(\frac{\pi}{2}+2\right)a^2b-\frac{\pi}{2}a^3.
$$

### 第 13 题
- 答案：$y=e^x$

曲线在点 $(x,y)$ 处的切线为
$$
Y-y=y'(X-x).
$$

切线与 $x$ 轴交于
$$
\left(x-\frac{y}{y'},0\right).
$$

题设 $y'(x)>0$ 且 $y(0)=1$，故 $y>0$。三角形面积为
$$
S_1=\frac{1}{2} y\left|x-\left(x-\frac{y}{y'}\right)\right|
=\frac{y^2}{2y'}.
$$

曲边梯形面积为
$$
S_2=\int_0^x y(t)\,dt.
$$

由 $2S_1-S_2=1$ 得
$$
\frac{y^2}{y'}-\int_0^x y(t)\,dt=1.
$$

两边对 $x$ 求导，化简得
$$
yy''=(y')^2.
$$

令 $p=y'$，则
$$
y''=\frac{dp}{dx}=\frac{dp}{dy}\frac{dy}{dx}=p\frac{dp}{dy}.
$$
代入得
$$
y p\frac{dp}{dy}=p^2.
$$
因 $p>0$，故
$$
\frac{dp}{p}=\frac{dy}{y},
$$
从而
$$
p=C_1y,\qquad \frac{dy}{dx}=C_1y.
$$

由原面积式在 $x=0$ 处得 $y'(0)=1$，又 $y(0)=1$，故 $C_1=1$。
解得
$$
y=e^x.
$$

### 第 14 题
- 答案：见解析

令
$$
F(x)=(x^2-1)\ln x-(x-1)^2,\qquad x>0.
$$

显然
$$
F(1)=0.
$$

求导：
$$
F'(x)=2x\ln x-x+2-\frac{1}{x},
$$
$$
F''(x)=2\ln x+1+\frac{1}{x^2}.
$$

再求导得
$$
F'''(x)=\frac{2(x^2-1)}{x^3}.
$$

当 $0<x<1$ 时 $F'''(x)<0$，当 $x>1$ 时 $F'''(x)>0$，所以 $F''(x)$ 在 $x=1$ 处取最小值。
又
$$
F''(1)=2>0,
$$
故
$$
F''(x)>0\qquad(x>0).
$$

于是 $F'(x)$ 单调递增，且 $F'(1)=0$。因此当 $0<x<1$ 时 $F'(x)<0$，当 $x>1$ 时 $F'(x)>0$。

所以 $F(x)$ 在 $x=1$ 处取得最小值，
$$
F(x)\ge F(1)=0.
$$

即
$$
(x^2-1)\ln x\ge (x-1)^2,\qquad x>0.
$$

### 第 15 题
- 答案：$91500\,\mathrm{J}$

把总功分为三部分：抓斗自重、绳重、污泥重。

抓斗自重做功为
$$
W_1=400\times30=12000\ \mathrm J.
$$

当抓斗已提升 $x$ 米时，仍在井内的绳长为 $30-x$ 米，绳重对应的微元功为
$$
dW_2=50(30-x)\,dx.
$$
故
$$
W_2=\int_0^{30}50(30-x)\,dx=22500\ \mathrm J.
$$

提升速度为 $3\,\mathrm{m/s}$，提升 $30$ 米需
$$
10\ \mathrm s.
$$
污泥以 $20\,\mathrm{N/s}$ 漏掉，故时刻 $t$ 的污泥重量为 $2000-20t$。微元时间内提升高度为 $3\,dt$，所以
$$
W_3=\int_0^{10}3(2000-20t)\,dt=57000\ \mathrm J.
$$

因此总功为
$$
W=W_1+W_2+W_3
=12000+22500+57000
=91500\ \mathrm J.
$$

### 第 16 题
- 答案：$\dfrac{3\pi}{2}$

椭球面可写为
$$
\frac{x^2}{2}+\frac{y^2}{2}+z^2=1,\qquad z\ge0.
$$

在点 $P(x,y,z)$ 处的切平面为
$$
\frac{x}{2}X+\frac{y}{2}Y+zZ=1.
$$

原点到该平面的距离为
$$
\rho=\frac{1}{\sqrt{x^2/4+y^2/4+z^2}}.
$$

所以
$$
\frac{z}{\rho}=z\sqrt{\frac{x^2}{4}+\frac{y^2}{4}+z^2}.
$$

把上半椭球投影到 $xOy$ 平面，投影区域为
$$
D:x^2+y^2\le2,
$$
且
$$
z=\sqrt{1-\frac{x^2+y^2}{2}}.
$$

由图形曲面面积元公式，代入化简可得
$$
\iint_S\frac{z}{\rho}\,dS
=\frac{1}{4}\iint_D(4-x^2-y^2)\,dx\,dy.
$$

用极坐标计算：
$$
\frac{1}{4}\int_0^{2\pi}\int_0^{\sqrt2}(4-r^2)r\,dr\,d\theta
=\frac{3\pi}{2}.
$$

### 第 17 题
- 答案：(1) $1$；(2) 对任意 $\lambda>0$ 均收敛

(1) 由定义
$$
a_n+a_{n+2}
=\int_0^{\pi/4}\tan^n x(1+\tan^2x)\,dx
=\int_0^{\pi/4}\tan^n x\sec^2x\,dx.
$$

令 $t=\tan x$，则 $t$ 从 $0$ 到 $1$，得
$$
a_n+a_{n+2}=\int_0^1t^n\,dt=\frac{1}{n+1}.
$$

因此
$$
\sum_{n=1}^{\infty}\frac{1}{n}(a_n+a_{n+2})
=\sum_{n=1}^{\infty}\frac{1}{n(n+1)}
=1.
$$

(2) 同样令 $t=\tan x$，有
$$
a_n=\int_0^1\frac{t^n}{1+t^2}\,dt
<\int_0^1t^n\,dt
=\frac{1}{n+1}.
$$

于是
$$
0<\frac{a_n}{n^\lambda}
<\frac{1}{n^\lambda(n+1)}
<\frac{1}{n^{\lambda+1}}.
$$

由于 $\lambda>0$，级数
$$
\sum_{n=1}^{\infty}\frac{1}{n^{\lambda+1}}
$$
收敛，由比较判别法，
$$
\sum_{n=1}^{\infty}\frac{a_n}{n^\lambda}
$$
收敛。

### 第 18 题
- 答案：$a=2,\ b=-3,\ c=2,\ \lambda_0=1$

由 $\det A=-1$，有
$$
AA^*=(\det A)E=-E.
$$

又 $A^*$ 有特征值 $\lambda_0$，对应特征向量
$$
\boldsymbol\alpha=(-1,-1,1)^T,
$$
即
$$
A^*\boldsymbol\alpha=\lambda_0\boldsymbol\alpha.
$$

两边左乘 $A$：
$$
AA^*\boldsymbol\alpha=\lambda_0A\boldsymbol\alpha.
$$
因此
$$
-\boldsymbol\alpha=\lambda_0A\boldsymbol\alpha.
$$

计算
$$
A\boldsymbol\alpha=
\begin{pmatrix}
-a+1+c\\
-5-b+3\\
-(1-c)-a
\end{pmatrix}.
$$

于是
$$
\lambda_0(-a+1+c)=1,
$$
$$
\lambda_0(-5-b+3)=1,
$$
$$
\lambda_0(-1+c-a)=-1.
$$

由于 $\det A\ne0$，所以 $\lambda_0\ne0$。由第一、三式相除得
$$
a=c.
$$

代回第一式可得 $\lambda_0=1$，再由第二式得
$$
b=-3.
$$

又由 $\det A=-1$、$a=c$、$b=-3$，可算得
$$
\det A=a-3.
$$

所以
$$
a-3=-1,\qquad a=2.
$$
因此
$$
a=2,\quad b=-3,\quad c=2,\quad \lambda_0=1.
$$

### 第 19 题
- 答案：见解析

先证必要性。若 $B^TAB$ 正定，则对任意非零 $\boldsymbol x\in\mathbb R^n$，
$$
\boldsymbol x^TB^TAB\boldsymbol x>0.
$$

即
$$
(B\boldsymbol x)^TA(B\boldsymbol x)>0.
$$

由于 $A$ 正定，若 $B\boldsymbol x=0$，则上式为 $0$，矛盾。因此
$$
B\boldsymbol x=0
$$
只有零解，故
$$
r(B)=n.
$$

再证充分性。若 $r(B)=n$，则对任意非零 $\boldsymbol x\in\mathbb R^n$，有
$$
B\boldsymbol x\ne0.
$$

因为 $A$ 正定，
$$
(B\boldsymbol x)^TA(B\boldsymbol x)>0.
$$

而
$$
(B\boldsymbol x)^TA(B\boldsymbol x)
=\boldsymbol x^TB^TAB\boldsymbol x.
$$

故对任意非零 $\boldsymbol x$，
$$
\boldsymbol x^TB^TAB\boldsymbol x>0.
$$

所以 $B^TAB$ 正定。

### 第 20 题
- 答案：$\begin{array}{c|ccc|c}
 &y_1&y_2&y_3&p_{i\cdot}\\ \hline
x_1&\frac{1}{24}&\frac{1}{8}&\frac{1}{12}&\frac{1}{4}\\
x_2&\frac{1}{8}&\frac{3}{8}&\frac{1}{4}&\frac{3}{4}\\ \hline
p_{\cdot j}&\frac{1}{6}&\frac{1}{2}&\frac{1}{3}&1
\end{array}$

由边缘分布定义，
$$
P(Y=y_1)=P(X=x_1,Y=y_1)+P(X=x_2,Y=y_1).
$$

已知 $P(Y=y_1)=\dfrac{1}{6}$，且
$$
P(X=x_2,Y=y_1)=\frac{1}{8},
$$
所以
$$
P(X=x_1,Y=y_1)=\frac{1}{6}-\frac{1}{8}=\frac{1}{24}.
$$

又由独立性，
$$
P(X=x_1,Y=y_1)=P(X=x_1)P(Y=y_1),
$$
故
$$
P(X=x_1)=\frac{1/24}{1/6}=\frac{1}{4}.
$$

于是
$$
P(X=x_1,Y=y_3)
=P(X=x_1)-P(X=x_1,Y=y_1)-P(X=x_1,Y=y_2)
=\frac{1}{4}-\frac{1}{24}-\frac{1}{8}=\frac{1}{12}.
$$

再由独立性，
$$
P(Y=y_3)=\frac{P(X=x_1,Y=y_3)}{P(X=x_1)}
=\frac{1/12}{1/4}=\frac{1}{3}.
$$

所以
$$
P(X=x_2,Y=y_3)=P(Y=y_3)-P(X=x_1,Y=y_3)
=\frac{1}{3}-\frac{1}{12}=\frac{1}{4}.
$$

又
$$
P(X=x_2)=1-P(X=x_1)=\frac{3}{4},
$$
从而
$$
P(X=x_2,Y=y_2)
=\frac{3}{4}-\frac{1}{8}-\frac{1}{4}=\frac{3}{8}.
$$

最后
$$
P(Y=y_2)=1-\frac{1}{6}-\frac{1}{3}=\frac{1}{2}.
$$

因此完整表为
$$
\begin{array}{c|ccc|c}
 &y_1&y_2&y_3&p_{i\cdot}\\ \hline
x_1&\frac{1}{24}&\frac{1}{8}&\frac{1}{12}&\frac{1}{4}\\
x_2&\frac{1}{8}&\frac{3}{8}&\frac{1}{4}&\frac{3}{4}\\ \hline
p_{\cdot j}&\frac{1}{6}&\frac{1}{2}&\frac{1}{3}&1
\end{array}.
$$

### 第 21 题
- 答案：$\hat\theta=2\overline X,\qquad D(\hat\theta)=\dfrac{\theta^2}{5n}$

先求总体均值：
$$
E(X)=\int_0^\theta x\frac{6x}{\theta^3}(\theta-x)\,dx.
$$

即
$$
E(X)=\int_0^\theta\left(\frac{6x^2}{\theta^2}-\frac{6x^3}{\theta^3}\right)dx
=2\theta-\frac{3}{2}\theta
=\frac{\theta}{2}.
$$

令样本均值等于总体均值：
$$
\overline X=\frac{\theta}{2}.
$$

故矩估计量为
$$
\hat\theta=2\overline X.
$$

再求方差。先算二阶矩：
$$
E(X^2)=\int_0^\theta x^2\frac{6x}{\theta^3}(\theta-x)\,dx
=\frac{6\theta^2}{20}.
$$

所以
$$
D(X)=E(X^2)-[E(X)]^2
=\frac{6\theta^2}{20}-\left(\frac{\theta}{2}\right)^2
=\frac{\theta^2}{20}.
$$

由于
$$
D(\overline X)=\frac{1}{n}D(X),
$$
因此
$$
D(\hat\theta)=D(2\overline X)
=4D(\overline X)
=\frac{4}{n}D(X)
=\frac{\theta^2}{5n}.
$$
