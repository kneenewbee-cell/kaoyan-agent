# Math 2 2010 Answers

资料类型：考研数学二答案解析
年份：2010
科目：数学二
整理状态：答案与解析按清洗后的正式题卡整理。

## 答案速查

| 题号 | 题型 | 答案 |
|---|---|---|
| 1 | choice | B |
| 2 | choice | A |
| 3 | choice | C |
| 4 | choice | D |
| 5 | choice | B |
| 6 | choice | A |
| 7 | choice | A |
| 8 | choice | D |
| 9 | fill_blank | $C_1e^{2x}+e^x\bigl(C_2\cos x+C_3\sin x\bigr)$ |
| 10 | fill_blank | $y=2x$ |
| 11 | fill_blank | $-2^n(n-1)!$ |
| 12 | fill_blank | $\sqrt2\,(e^{\pi}-1)$ |
| 13 | fill_blank | $3\text{ cm/s}$ |
| 14 | fill_blank | $3$ |
| 15 | solution | 单调递减区间为 $(-\infty,-1)\cup(0,1)$，单调递增区间为 $(-1,0)\cup(1,+\infty)$；极大值为 $f(0)=\dfrac{e^{-1}-1}{2}$，极小值为 $f(\pm1)=0$。 |
| 16 | solution | (I) 前者小于后者；(II) $\displaystyle \lim_{n\to\infty}nu_n=0$。 |
| 17 | solution | $\psi(t)=t^3+\dfrac32t^2$ |
| 18 | solution | $M=\rho abl\left(\dfrac{2\pi}{3}+\dfrac{\sqrt3}{4}\right)$ |
| 19 | solution | $a,b$ 为方程 $5r^2+12r+4=0$ 的两个根，即 $a=-2,\ b=-\dfrac25$（或交换次序）。 |
| 20 | solution | $\displaystyle I=\frac13-\frac{\pi}{16}$ |
| 21 | solution | 结论成立。 |
| 22 | solution | $\lambda=-1,\ a=-2$；通解为 $x=\left(\dfrac32+t,-\dfrac12,t\right)^T\ (t\in\mathbb R)$。 |
| 23 | solution | $a=-1$。可取
$$
Q=\begin{pmatrix}
\frac1{\sqrt6} & \frac1{\sqrt2} & \frac1{\sqrt3}\\
\frac2{\sqrt6} & 0 & -\frac1{\sqrt3}\\
\frac1{\sqrt6} & -\frac1{\sqrt2} & \frac1{\sqrt3}
\end{pmatrix}.
$$ |

## 详细解析

### 第 1 题
- 答案：B

函数在 $x=0,\pm1$ 处都有可能出现间断。化简
$$
f(x)=\frac{x}{x+1}\sqrt{1+\frac1{x^2}}\quad(x\ne1).
$$
当 $x\to0$ 时，左右极限分别为 $1$ 与 $-1$，故 $x=0$ 是跳跃间断点；当 $x\to1$ 时极限存在且有限，故 $x=1$ 是可去间断点；当 $x\to-1$ 时分母趋于 $0$ 而分子不为 $0$，故 $x=-1$ 是无穷间断点。因此无穷间断点只有 $1$ 个。

### 第 2 题
- 答案：A

由 $y_1,y_2$ 都满足非齐次方程可知
$$
(\lambda y_1-\mu y_2)'+p(x)(\lambda y_1-\mu y_2)=(\lambda-\mu)q(x).
$$
它是齐次方程的解，因此 $(\lambda-\mu)q(x)=0$，而非齐次方程中 $q(x)\not\equiv0$，故 $\lambda=\mu$。又
$$
(\lambda y_1+\mu y_2)'+p(x)(\lambda y_1+\mu y_2)=(\lambda+\mu)q(x),
$$
要仍为原方程的解，就需 $\lambda+\mu=1$。联立得
$$
\lambda=\mu=\frac12.
$$

### 第 3 题
- 答案：C

设切点为 $(x_0,x_0^2)$，则两曲线在该点既有相同函数值，又有相同导数：
$$
x_0^2=a\ln x_0,\qquad 2x_0=\frac{a}{x_0}.
$$
由第二式得 $a=2x_0^2$。代回第一式：
$$
x_0^2=2x_0^2\ln x_0\Rightarrow \ln x_0=\frac12,
$$
故 $x_0=\sqrt e$，从而
$$
a=2x_0^2=2e.
$$

### 第 4 题
- 答案：D

在 $x\to0^+$ 时，$\ln(1-x)\sim -x$，故被积函数与 $x^{\frac1m-\frac1n}$ 同阶。这里 $m,n$ 为正整数，所以指数始终大于 $-1$，在 $0$ 附近总可积。  
在 $x\to1^-$ 时，令 $t=1-x$，则被积函数与 $|\ln t|^{2/m}$ 同阶，而
$$
\int_0^\delta |\ln t|^{2/m}\,dt
$$
总收敛。因此该积分对任意正整数 $m,n$ 都收敛。

### 第 5 题
- 答案：B

由
$$
F\!\left(\frac{y}{x},\frac{z}{x}\right)=0
$$
可知 $\dfrac{z}{x}$ 仅依赖于 $\dfrac{y}{x}$，即存在函数 $\varphi$ 使
$$
z=x\,\varphi\!\left(\frac{y}{x}\right).
$$
因此 $z$ 是关于 $(x,y)$ 的一次齐次函数。由 Euler 齐次函数定理，
$$
xz_x+yz_y=z.
$$

### 第 6 题
- 答案：A

将和式改写为
$$
\sum_{i=1}^n\sum_{j=1}^i \frac{1}{n^2}\cdot\frac{1}{\left(1+\frac{i}{n}\right)\left(1+\left(\frac{j}{n}\right)^2\right)}.
$$
令 $x=\dfrac{i}{n},\ y=\dfrac{j}{n}$，则取样区域满足
$$
0\le y\le x\le1.
$$
故该极限对应的二重积分为
$$
\int_0^1 dx\int_0^x \frac{1}{(1+x)(1+y^2)}\,dy.
$$

### 第 7 题
- 答案：A

向量组 I 可由向量组 II 线性表示，所以
$$
r(\text{I})\le r(\text{II})\le s.
$$
若向量组 I 线性无关，则其秩等于向量个数，即 $r(\text{I})=r$，于是
$$
r\le s.
$$
其余选项都不能由题设必然推出。

### 第 8 题
- 答案：D

由 $A^2+A=O$ 得
$$
A(A+E)=O,
$$
所以任一特征值 $\lambda$ 满足
$$
\lambda^2+\lambda=0\Rightarrow \lambda=0\text{ 或 }-1.
$$
又因 $A$ 为实对称矩阵，必可正交相似对角化。秩为 $3$ 表明恰有三个非零特征值，因此这三个特征值都只能是 $-1$，另一个特征值是 $0$。故
$$
A\sim \operatorname{diag}(-1,-1,-1,0).
$$

### 第 9 题
- 答案：$C_1e^{2x}+e^x\bigl(C_2\cos x+C_3\sin x\bigr)$

特征方程为
$$
r^3-2r^2+r-2=0=(r-2)(r^2+1).
$$
故特征根为 $r=2,\ \pm i$。因此通解为
$$
y=C_1e^{2x}+e^x\bigl(C_2\cos x+C_3\sin x\bigr).
$$

### 第 10 题
- 答案：$y=2x$

作多项式除法：
$$
\frac{2x^3}{x^2+1}=2x-\frac{2x}{x^2+1}.
$$
当 $x\to\pm\infty$ 时，余项趋于 $0$，故斜渐近线为
$$
y=2x.
$$

### 第 11 题
- 答案：$-2^n(n-1)!$

由
$$
\ln(1-2x)=-\sum_{k=1}^{\infty}\frac{(2x)^k}{k}\qquad(|x|<\tfrac12),
$$
可得 $x^n$ 的系数为 $-\dfrac{2^n}{n}$。因此
$$
y^{(n)}(0)=n!\left(-\frac{2^n}{n}\right)=-2^n(n-1)!.
$$

### 第 12 题
- 答案：$\sqrt2\,(e^{\pi}-1)$

极坐标弧长公式为
$$
s=\int_0^{\pi}\sqrt{r^2+\left(\frac{dr}{d\theta}\right)^2}\,d\theta.
$$
这里 $r=e^{\theta}$ 且 $r'=e^{\theta}$，所以
$$
s=\int_0^{\pi}\sqrt{2e^{2\theta}}\,d\theta
=\sqrt2\int_0^{\pi}e^{\theta}\,d\theta
=\sqrt2\,(e^{\pi}-1).
$$

### 第 13 题
- 答案：$3\text{ cm/s}$

设对角线长为 $s$，则
$$
s^2=l^2+w^2.
$$
两边对时间求导：
$$
2s\frac{ds}{dt}=2l\frac{dl}{dt}+2w\frac{dw}{dt}.
$$
当 $l=12,w=5$ 时，$s=13$，故
$$
\frac{ds}{dt}=\frac{12\cdot2+5\cdot3}{13}=3\text{ cm/s}.
$$

### 第 14 题
- 答案：$3$

由
$$
A^{-1}+B=A^{-1}(E+AB)
$$
得
$$
|A^{-1}+B|=|A|^{-1}|E+AB|=2.
$$
代入 $|A|=3$，可得
$$
|E+AB|=6.
$$
又
$$
A+B^{-1}=B^{-1}(AB+E),
$$
故
$$
|A+B^{-1}|=|B|^{-1}|AB+E|=\frac{1}{2}\cdot6=3.
$$

### 第 15 题
- 答案：单调递减区间为 $(-\infty,-1)\cup(0,1)$，单调递增区间为 $(-1,0)\cup(1,+\infty)$；极大值为 $f(0)=\dfrac{e^{-1}-1}{2}$，极小值为 $f(\pm1)=0$。

将积分拆开：
$$
f(x)=x^2\int_1^{x^2}e^{-t^2}\,dt-\int_1^{x^2}te^{-t^2}\,dt.
$$
求导得
$$
f'(x)=2x\int_1^{x^2}e^{-t^2}\,dt.
$$
令 $f'(x)=0$，得驻点 $x=0,\pm1$。再求二阶导数
$$
f''(x)=2\int_1^{x^2}e^{-t^2}\,dt+4x^2e^{-x^4}.
$$
由 $f''(0)=2\int_1^0e^{-t^2}dt<0$，知 $x=0$ 为极大值点；而 $f''(\pm1)=4e^{-1}>0$，知 $x=\pm1$ 为极小值点。结合
$$
\int_1^{x^2}e^{-t^2}\,dt
$$
在 $x^2<1$ 时为负、在 $x^2>1$ 时为正，可得单调性结论。又
$$
f(0)=\int_1^0(-t)e^{-t^2}\,dt=\frac{e^{-1}-1}{2},\qquad f(\pm1)=0.
$$

### 第 16 题
- 答案：(I) 前者小于后者；(II) $\displaystyle \lim_{n\to\infty}nu_n=0$。

对 $0<t<1$，有
$$
0<\ln(1+t)<t.
$$
因此
$$
0<|\ln t|\,[\ln(1+t)]^n<t^n|\ln t|,
$$
从而
$$
\int_0^1 |\ln t|\,[\ln(1+t)]^n\,dt<\int_0^1 t^n|\ln t|\,dt.
$$
又
$$
\int_0^1 t^n|\ln t|\,dt=\frac{1}{(n+1)^2},
$$
故
$$
0<nu_n<\frac{n}{(n+1)^2}\to0.
$$
由夹逼定理，
$$
\lim_{n\to\infty}nu_n=0.
$$

### 第 17 题
- 答案：$\psi(t)=t^3+\dfrac32t^2$

先求
$$
\frac{dx}{dt}=2+2t=2(1+t),\qquad \frac{dy}{dx}=\frac{\psi'(t)}{2(1+t)}.
$$
于是
$$
\frac{d^2y}{dx^2}
=\frac{\dfrac{d}{dt}\left(\dfrac{\psi'(t)}{2(1+t)}\right)}{2(1+t)}
=\frac{(1+t)\psi''(t)-\psi'(t)}{4(1+t)^3}.
$$
与题设比较得
$$
(1+t)\psi''(t)-\psi'(t)=3(1+t)^2.
$$
令 $v=\psi'(t)$，则
$$
(1+t)v'-v=3(1+t)^2.
$$
解得
$$
v=3(1+t)^2+C(1+t).
$$
由 $\psi'(1)=6$ 得 $12+2C=6$，故 $C=-3$，于是
$$
\psi'(t)=3t(t+1).
$$
积分得
$$
\psi(t)=t^3+\frac32t^2+C_1.
$$
再由 $\psi(1)=\dfrac52$，得 $C_1=0$。

### 第 18 题
- 答案：$M=\rho abl\left(\dfrac{2\pi}{3}+\dfrac{\sqrt3}{4}\right)$

椭圆截面方程可写为
$$
\frac{x^2}{a^2}+\frac{y^2}{b^2}=1.
$$
油面高度为 $\dfrac{3b}{2}$，说明顶部尚有一段高度为 $\dfrac{b}{2}$ 的空缺弓形。  
整个椭圆面积为 $\pi ab$。顶部弓形面积为
$$
S_0=2\int_{b/2}^{b} a\sqrt{1-\frac{y^2}{b^2}}\,dy
=2ab\int_{1/2}^{1}\sqrt{1-u^2}\,du
=ab\left(\frac{\pi}{3}-\frac{\sqrt3}{4}\right).
$$
因此油的截面积
$$
S=\pi ab-S_0
=ab\left(\frac{2\pi}{3}+\frac{\sqrt3}{4}\right).
$$
体积 $V=Sl$，故油的质量为
$$
M=\rho V=\rho abl\left(\frac{2\pi}{3}+\frac{\sqrt3}{4}\right).
$$

### 第 19 题
- 答案：$a,b$ 为方程 $5r^2+12r+4=0$ 的两个根，即 $a=-2,\ b=-\dfrac25$（或交换次序）。

由链式法则，
$$
u_x=u_\xi+u_\eta,\qquad u_y=au_\xi+bu_\eta.
$$
进一步可得
$$
u_{xx}=u_{\xi\xi}+2u_{\xi\eta}+u_{\eta\eta},
$$
$$
u_{xy}=a u_{\xi\xi}+(a+b)u_{\xi\eta}+b u_{\eta\eta},
$$
$$
u_{yy}=a^2u_{\xi\xi}+2abu_{\xi\eta}+b^2u_{\eta\eta}.
$$
代入原式后，若要化为 $u_{\xi\eta}=0$，就必须令 $u_{\xi\xi}$ 与 $u_{\eta\eta}$ 的系数同时为零，即
$$
4+12a+5a^2=0,\qquad 4+12b+5b^2=0.
$$
解得
$$
5r^2+12r+4=0\Rightarrow r=-2,\ -\frac25.
$$
故可取
$$
(a,b)=\left(-2,-\frac25\right)
$$
或交换次序。

### 第 20 题
- 答案：$\displaystyle I=\frac13-\frac{\pi}{16}$

改用直角坐标。由
$$
x=r\cos\theta,\qquad y=r\sin\theta
$$
知区域 $D$ 对应为
$$
0\le y\le x\le1.
$$
又
$$
r^2\cos2\theta=x^2-y^2,\qquad r^2\sin\theta\,drd\theta = y\,dxdy.
$$
因此
$$
I=\int_0^1dx\int_0^x y\sqrt{1-x^2+y^2}\,dy.
$$
对内层积分令 $u=1-x^2+y^2$，得
$$
\int_0^x y\sqrt{1-x^2+y^2}\,dy
=\frac13\left[1-(1-x^2)^{3/2}\right].
$$
于是
$$
I=\frac13\int_0^1\left[1-(1-x^2)^{3/2}\right]dx
=\frac13-\frac13\int_0^1(1-x^2)^{3/2}dx.
$$
令 $x=\sin t$，则
$$
\int_0^1(1-x^2)^{3/2}dx=\int_0^{\pi/2}\cos^4 t\,dt=\frac{3\pi}{16}.
$$
故
$$
I=\frac13-\frac{\pi}{16}.
$$

### 第 21 题
- 答案：结论成立。

构造函数
$$
H(x)=f(x)-\frac{x^3}{3}.
$$
则
$$
H(0)=f(0)=0,\qquad H(1)=f(1)-\frac13=0.
$$
分两种情形。  
若 $H\!\left(\dfrac12\right)=0$，则由 Rolle 定理分别在区间 $\left[0,\dfrac12\right]$ 和 $\left[\dfrac12,1\right]$ 上可得存在
$$
\xi\in\left(0,\frac12\right),\quad \eta\in\left(\frac12,1\right)
$$
使
$$
H'(\xi)=0,\qquad H'(\eta)=0.
$$
即
$$
f'(\xi)=\xi^2,\qquad f'(\eta)=\eta^2.
$$
于是结论成立。  
若 $H\!\left(\dfrac12\right)\ne0$，则由拉格朗日中值定理，在 $\left[0,\dfrac12\right]$ 上存在 $\xi\in\left(0,\dfrac12\right)$ 使
$$
H'(\xi)=\frac{H(1/2)-H(0)}{1/2}=2H\!\left(\frac12\right),
$$
在 $\left[\dfrac12,1\right]$ 上存在 $\eta\in\left(\dfrac12,1\right)$ 使
$$
H'(\eta)=\frac{H(1)-H(1/2)}{1/2}=-2H\!\left(\frac12\right).
$$
故
$$
H'(\xi)+H'(\eta)=0.
$$
又 $H'(x)=f'(x)-x^2$，所以
$$
f'(\xi)+f'(\eta)=\xi^2+\eta^2.
$$
结论得证。

### 第 22 题
- 答案：$\lambda=-1,\ a=-2$；通解为 $x=\left(\dfrac32+t,-\dfrac12,t\right)^T\ (t\in\mathbb R)$。

“存在两个不同的解”说明该方程组有无穷多解，因此
$$
\det A=0
$$
且增广矩阵与系数矩阵同秩。计算
$$
\det A=(\lambda-1)^2(\lambda+1).
$$
若 $\lambda=1$，第二行变成 $0=1$，方程组无解，故只能取
$$
\lambda=-1.
$$
此时方程组为
$$
\begin{cases}
-x_1+x_2+x_3=a,\\
-2x_2=1,\\
x_1+x_2-x_3=1.
\end{cases}
$$
由第二式得 $x_2=-\dfrac12$。代入第一、三式得
$$
-x_1+x_3=a+\frac12,\qquad x_1-x_3=\frac32.
$$
两式相容需满足
$$
a+\frac12=-\frac32,
$$
故
$$
a=-2.
$$
设 $x_3=t$，则
$$
x_1=\frac32+t,\qquad x_2=-\frac12.
$$
故通解为
$$
x=\begin{pmatrix}\frac32+t\\-\frac12\\t\end{pmatrix},\quad t\in\mathbb R.
$$

### 第 23 题
- 答案：$a=-1$。可取
$$
Q=\begin{pmatrix}
\frac1{\sqrt6} & \frac1{\sqrt2} & \frac1{\sqrt3}\\
\frac2{\sqrt6} & 0 & -\frac1{\sqrt3}\\
\frac1{\sqrt6} & -\frac1{\sqrt2} & \frac1{\sqrt3}
\end{pmatrix}.
$$

记
$$
q_1=\frac1{\sqrt6}(1,2,1)^T.
$$
由于 $Q^TAQ$ 为对角矩阵，$q_1$ 必是 $A$ 的特征向量。故存在特征值 $\lambda$ 使
$$
A(1,2,1)^T=\lambda(1,2,1)^T.
$$
直接计算得
$$
A(1,2,1)^T=(2,5+a,4+2a)^T.
$$
故
$$
2=\lambda,\qquad 5+a=2\lambda,\qquad 4+2a=\lambda,
$$
解得
$$
a=-1,\qquad \lambda=2.
$$
此时
$$
A=\begin{pmatrix}
0 & -1 & 4\\
-1 & 3 & -1\\
4 & -1 & 0
\end{pmatrix}.
$$
再求与 $q_1$ 正交的两个单位特征向量，可取
$$
q_2=\frac1{\sqrt2}(1,0,-1)^T,\qquad q_3=\frac1{\sqrt3}(1,-1,1)^T.
$$
它们分别对应特征值 $-4,5$，且与 $q_1$ 两两正交。于是可取
$$
Q=(q_1,q_2,q_3)
=\begin{pmatrix}
\frac1{\sqrt6} & \frac1{\sqrt2} & \frac1{\sqrt3}\\
\frac2{\sqrt6} & 0 & -\frac1{\sqrt3}\\
\frac1{\sqrt6} & -\frac1{\sqrt2} & \frac1{\sqrt3}
\end{pmatrix}.
$$
