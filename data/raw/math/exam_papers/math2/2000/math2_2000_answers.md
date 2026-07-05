# Math 2 2000 Answers

资料类型：考研数学二答案解析
年份：2000
科目：数学二
范围：试卷 III
校对状态：已按答案页图像清洗并与题面同步。

## 答案速查

| 题号 | 题型 | 答案 |
|---|---|---|
| 1 | 填空题 | $-\dfrac{1}{6}$ |
| 2 | 填空题 | $(\ln2-1)\,dx$ |
| 3 | 填空题 | $\dfrac{\pi}{3}$ |
| 4 | 填空题 | $y=2x+1$ |
| 5 | 填空题 | $\begin{pmatrix}\frac12&0&0&0\\[2pt]0&\frac14&0&0\\[2pt]0&\frac{2}{5}&\frac{3}{10}&0\\[2pt]0&0&\frac{3}{7}&\frac14\end{pmatrix}$ |
| 6 | 选择题 | $D$ |
| 7 | 选择题 | $C$ |
| 8 | 选择题 | $A$ |
| 9 | 选择题 | $C$ |
| 10 | 选择题 | $B$ |
| 11 | 解答题 | $\dfrac12[\ln(1+e^x)]^2+C$ |
| 12 | 解答题 | 分段函数，见解析。 |
| 13 | 解答题 | $f^{(n)}(0)=(-1)^{n-3}\dfrac{2n!}{(n-2)(n-1)n}$ |
| 14 | 解答题 | $(1)$ 见解析；$(2)\ \dfrac{2}{\pi}$。 |
| 15 | 解答题 | $8$ 年 |
| 16 | 证明题 | 见解析。 |
| 17 | 解答题 | $y=4x-23$ |
| 18 | 解答题 | $a=\dfrac12$，最大体积为 $\dfrac{\pi}{24}$ |
| 19 | 证明题 | (1) $f'(x)=-\dfrac{f(x)}{x+1}$；(2) 见解析。 |
| 20 | 解答题 | $x=\begin{pmatrix}0\\0\\8\end{pmatrix}$ |
| 21 | 解答题 | $a=1,\ b=2$ |

## 详细解析

### 第 1 题

- 答案：$-\dfrac{1}{6}$

展开
$$
\arctan x=x-\frac{x^3}{3}+o(x^3),\qquad \ln(1+2x^3)=2x^3+o(x^3).
$$
故原式
$$
\sim \frac{-x^3/3}{2x^3}=-\frac16.
$$

### 第 2 题

- 答案：$(\ln2-1)\,dx$

由 $x=0$ 时得 $y=1$。对方程两边微分：
$$
2^{xy}\ln2\,(x\,dy+y\,dx)=dx+dy.
$$
代入 $(x,y)=(0,1)$，得
$$
\ln2\,dx=dx+dy,
$$
故
$$
dy=(\ln2-1)\,dx.
$$

### 第 3 题

- 答案：$\dfrac{\pi}{3}$

令
$$
x-2=t^2,
$$
则
$$
dx=2t\,dt,\qquad x+7=t^2+9.
$$
原式化为
$$
2\int_0^{+\infty}\frac{dt}{t^2+9}
=\frac{2}{3}\left[\arctan\frac{t}{3}\right]_0^{+\infty}
=\frac{\pi}{3}.
$$

### 第 4 题

- 答案：$y=2x+1$

当 $x\to\pm\infty$ 时，
$$
e^{1/x}=1+\frac1x+o\left(\frac1x\right).
$$
故
$$
y=(2x-1)\left(1+\frac1x+o\left(\frac1x\right)\right)=2x+1+o(1),
$$
所以斜渐近线为
$$
y=2x+1.
$$

### 第 5 题

- 答案：$\begin{pmatrix}\frac12&0&0&0\\[2pt]0&\frac14&0&0\\[2pt]0&\frac{2}{5}&\frac{3}{10}&0\\[2pt]0&0&\frac{3}{7}&\frac14\end{pmatrix}$

由
$$
B=(E+A)^{-1}(E-A)
$$
得
$$
E+B=E+(E+A)^{-1}(E-A)=2(E+A)^{-1}.
$$
故
$$
(E+B)^{-1}=\frac12(E+A).
$$
直接代入 $A$ 可得答案矩阵。

### 第 6 题

- 答案：$D$

要在整个实轴连续，分母
$$
a+e^{bx}
$$
不能为零。若 $b>0$，则 $x\to-\infty$ 时 $e^{bx}\to0$，为使极限为 $0$ 需 $a\ne0$，但还要兼顾连续性条件，排除其余选项。综合判断可得
$$
a\ge0,\quad b<0,
$$
故选 $D$。

### 第 7 题

- 答案：$C$

代入 $x=0$ 得
$$
f''(0)=0.
$$
再对题设求导，可得
$$
f'''(0)=1.
$$
因此 $x=0$ 附近二阶导数变号，故 $(0,f(0))$ 是拐点，选 $C$。

### 第 8 题

- 答案：$A$

令
$$
F(x)=\frac{f(x)}{g(x)}.
$$
则
$$
F'(x)=\frac{f'(x)g(x)-f(x)g'(x)}{g(x)^2}<0,
$$
故 $F(x)$ 单调递减。于是当 $a<x<b$ 时，
$$
\frac{f(x)}{g(x)}>\frac{f(b)}{g(b)},
$$
即
$$
f(x)g(b)>f(b)g(x).
$$
选 $A$。

### 第 9 题

- 答案：$C$

由已知得
$$
\sin6x+xf(x)=o(x^3).
$$
而
$$
\sin6x=6x-36x^3+o(x^3),
$$
故
$$
x(6+f(x))=36x^3+o(x^3),
$$
从而
$$
\frac{6+f(x)}{x^2}\to36.
$$
选 $C$。

### 第 10 题

- 答案：$B$

由解的形式知特征根为
$$
r=-1
$$
（二重根）和
$$
r=1.
$$
故特征方程为
$$
(r+1)^2(r-1)=0=r^3+r^2-r-1.
$$
对应方程为
$$
y'''+y''-y'-y=0.
$$
选 $B$。

### 第 11 题

- 答案：$\dfrac12[\ln(1+e^x)]^2+C$

令
$$
t=e^x,
$$
则由题设
$$
f(x)=\frac{\ln(1+e^x)}{e^x}.
$$
因此
$$
\int f(x)\,dx=\int \frac{\ln(1+e^x)}{e^x}\,dx
=\int \frac{\ln(1+t)}{t^2}\,dt
$$
不便直接算。更简洁地令
$$
u=\ln(1+e^x),
$$
则
$$
du=\frac{e^x}{1+e^x}\,dx,
$$
整理可得原积分为
$$
\frac12u^2+C=\frac12[\ln(1+e^x)]^2+C.
$$

### 第 12 题

- 答案：分段函数，见解析。

当 $0\le t\le1$ 时，左下部分是直角三角形，
$$
S(t)=\frac{t^2}{2}.
$$
当 $1\le t\le2$ 时，右上角被截去一个直角三角形，
$$
S(t)=1-\frac{(2-t)^2}{2}.
$$
当 $t\ge2$ 时，
$$
S(t)=1.
$$
于是积分结果为
$$
\int_0^xS(t)\,dt=
\begin{cases}
\dfrac{x^3}{6},&0\le x\le1,\\[4pt]
\dfrac16+\displaystyle\int_1^x\left(1-\frac{(2-t)^2}{2}\right)dt,&1\le x\le2,\\[8pt]
\dfrac{7}{6}+x-2,&x\ge2.
\end{cases}
$$
化简中段可得对应三次多项式。

### 第 13 题

- 答案：$f^{(n)}(0)=(-1)^{n-3}\dfrac{2n!}{(n-2)(n-1)n}$

由
$$
\ln(1+x)=x-\frac{x^2}{2}+\frac{x^3}{3}-\cdots+(-1)^{k-1}\frac{x^k}{k}+\cdots
$$
得
$$
f(x)=x^3-\frac{x^4}{2}+\frac{x^5}{3}-\cdots+(-1)^{n-3}\frac{x^n}{n-2}+\cdots
$$
故 $x^n$ 项系数为
$$
(-1)^{n-3}\frac{1}{n-2}.
$$
于是
$$
f^{(n)}(0)=n!\cdot(-1)^{n-3}\frac{1}{n-2}.
$$

### 第 14 题

- 答案：$(1)$ 见解析；$(2)\ \dfrac{2}{\pi}$。

函数 $|\cos t|$ 以 $\pi$ 为周期，且
$$
\int_0^\pi |\cos t|\,dt=2.
$$
因此当
$$
n\pi\le x<(n+1)\pi
$$
时，
$$
S(x)=2n+\int_{n\pi}^{x}|\cos t|\,dt,
$$
故
$$
2n\le S(x)<2(n+1).
$$
再由夹逼，
$$
\frac{2n}{(n+1)\pi}\le \frac{S(x)}{x}\le \frac{2(n+1)}{n\pi},
$$
令 $x\to+\infty$ 即得
$$
\lim_{x\to+\infty}\frac{S(x)}{x}=\frac{2}{\pi}.
$$

### 第 15 题

- 答案：$8$ 年

设第 $n$ 年年底污染物含量为 $m_n$，则一年内流入污染物最多为
$$
\frac{V}{6}\cdot \frac{m_0}{V}=\frac{m_0}{6}.
$$
流出时带走当前总量的
$$
\frac{V/3}{V}=\frac13,
$$
故有递推关系
$$
m_{n+1}=\frac23m_n+\frac{m_0}{6}.
$$
由 $m_0^{(1999)}=5m_0$ 出发，解该递推式可得
$$
m_n-\frac{m_0}{2}=\left(\frac23\right)^n\left(5m_0-\frac{m_0}{2}\right).
$$
求最小 $n$ 使 $m_n\le m_0$，计算得需要 $8$ 年。

### 第 16 题

- 答案：见解析。

若 $f$ 在 $(0,\pi)$ 内没有零点或只有一个零点，则因连续性其符号变化至多一次。于是可取常数 $a,b$ 使
$$
a+b\cos x
$$
与 $f(x)$ 在 $(0,\pi)$ 上同号。这样便有
$$
\int_0^\pi f(x)(a+b\cos x)\,dx\ne0.
$$
但由题设
$$
\int_0^\pi f(x)\,dx=0,\qquad \int_0^\pi f(x)\cos x\,dx=0
$$
可得上式应为 $0$，矛盾。故至少有两个不同零点。

### 第 17 题

- 答案：$y=4x-23$

由周期为 $5$ 知
$$
f(6)=f(1).
$$
令 $x\to0$，由 $\sin x\to0$ 得
$$
f(1)-3f(1)=0,
$$
故
$$
f(1)=0.
$$
再利用
$$
\sin x=x+o(x)
$$
并在 $x=1$ 处作一阶展开：
$$
f(1+\sin x)=f(1)+f'(1)\sin x+o(x),\quad
f(1-\sin x)=f(1)-f'(1)\sin x+o(x).
$$
代入题设并比较 $x$ 的系数，得
$$
4f'(1)=8,\qquad f'(1)=2.
$$
由于点 $(6,f(6))=(6,0)$，切线方程为
$$
y=2(x-6)=2x-12.
$$

### 第 18 题

- 答案：$a=\dfrac12$，最大体积为 $\dfrac{\pi}{24}$

交点满足
$$
ax^2=1-x^2,
$$
故
$$
x_A=\frac{1}{\sqrt{a+1}},\qquad y_A=\frac{a}{a+1}.
$$
直线 $OA$ 方程为
$$
y=\frac{a}{\sqrt{a+1}}x.
$$
于是所围图形绕 $x$ 轴旋转的体积为
$$
V(a)=\pi\int_0^{1/\sqrt{a+1}}\left[\left(\frac{a}{\sqrt{a+1}}x\right)^2-a^2x^4\right]dx.
$$
化简得
$$
V(a)=\frac{\pi a^2}{15(a+1)^{5/2}}.
$$
求极值得
$$
a=\frac12,
$$
代回得最大体积
$$
V_{\max}=\frac{\pi}{24}.
$$

### 第 19 题

- 答案：(1) $f'(x)=-\dfrac{f(x)}{x+1}$；(2) 见解析。

对原式两边乘以 $x+1$ 并求导，可得
$$
(x+1)f''(x)+(x+2)f'(x)=0.
$$
积分并利用初值，可化为
$$
f'(x)=-\frac{f(x)}{x+1}.
$$
于是
$$
\frac{f'(x)}{f(x)}=-\frac{1}{x+1},
$$
从而
$$
f(x)=\frac{C}{x+1}.
$$
结合 $f(0)=1$ 得 $C=1$，故
$$
f(x)=\frac1{x+1}.
$$
显然对 $x\ge0$，
$$
e^{-x}\le \frac1{x+1}\le1.
$$

### 第 20 题

- 答案：$x=\begin{pmatrix}0\\0\\8\end{pmatrix}$

先算
$$
B=\beta^T\alpha=1\cdot1+\frac12\cdot2+0\cdot1=2.
$$
又
$$
A=\alpha\beta^T
$$
是秩为 $1$ 的矩阵，并满足
$$
A^2=(\beta^T\alpha)A=2A.
$$
进而
$$
A^4=8A,\qquad 2B^2A^2=16A,\qquad B^4=16.
$$
原方程化为
$$
16Ax=8Ax+16x+\gamma,
$$
即
$$
8Ax-16x=\gamma.
$$
解得
$$
x=\begin{pmatrix}0\\0\\8\end{pmatrix}.
$$

### 第 21 题

- 答案：$a=1,\ b=2$

先求向量组 $\alpha_1,\alpha_2,\alpha_3$ 的秩。由
$$
\alpha_3=3\alpha_1+2\alpha_2
$$
可知其秩为 $2$。

又 $\beta_3$ 可由 $\alpha_1,\alpha_2,\alpha_3$ 线性表示，而这些向量都在由 $\alpha_1,\alpha_2$ 张成的平面内，故
$$
\beta_3=s\alpha_1+t\alpha_2.
$$
解该方程组得
$$
b=2.
$$
再由 $\beta$ 组与 $\alpha$ 组同秩，要求 $\beta_1,\beta_2,\beta_3$ 的秩也为 $2$，据此可得
$$
a=1.
$$
