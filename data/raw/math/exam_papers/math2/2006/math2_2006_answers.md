# Math 2 2006 Answers

资料类型：考研数学二答案解析
年份：2006
科目：数学二
整理状态：答案与解析依据答案册清洗整理，并与题面同步。

## 答案速查

| 题号 | 题型 | 答案 |
|---|---|---|
| 1 | 填空题 | $y=\dfrac15$ |
| 2 | 填空题 | $\dfrac13$ |
| 3 | 填空题 | $\dfrac12$ |
| 4 | 填空题 | $y=Cxe^{-x}$ |
| 5 | 填空题 | $-e$ |
| 6 | 填空题 | $2$ |
| 7 | 选择题 | A |
| 8 | 选择题 | B |
| 9 | 选择题 | C |
| 10 | 选择题 | D |
| 11 | 选择题 | C |
| 12 | 选择题 | D |
| 13 | 选择题 | A |
| 14 | 选择题 | B |
| 15 | 解答题 | $A=\dfrac13,\ B=-\dfrac23,\ C=\dfrac16$ |
| 16 | 解答题 | $-\dfrac{\arcsin e^x}{e^x}+\dfrac12\ln\left\lvert\dfrac{\sqrt{1-e^{2x}}-1}{\sqrt{1-e^{2x}}+1}\right\rvert+C$ |
| 17 | 解答题 | $\dfrac{\pi}{2}\ln2$ |
| 18 | 解答题 | （I）$\lim\limits_{n\to\infty}x_n=0$；（II）$e^{-1/6}$ |
| 19 | 证明题 | 见解析 |
| 20 | 解答题 | （I）成立；（II）$f(u)=\ln u$ |
| 21 | 解答题 | （I）$t>0$ 时曲线下凹；（II）切点 $(2,3)$，切线 $y=x+1$；（III）面积 $\dfrac73$ |
| 22 | 解答题 | （I）$r(A)=2$；（II）$a=2,\ b=-3$，通解为 $(2,-3,0,0)^T+c_1(-2,1,1,0)^T+c_2(4,-5,0,1)^T$ |
| 23 | 解答题 | （I）特征值为 $3,0,0$；（II）可取 $\Lambda=\operatorname{diag}(3,0,0)$，相应正交矩阵见解析 |

## 详细解析

### 第 1 题

- 答案：$y=\dfrac15$

当 $x\to\infty$ 时，
$$
y=\frac{1+\frac{4\sin x}{x}}{5-\frac{2\cos x}{x}}\to\frac15.
$$
因为 $\dfrac{\sin x}{x},\dfrac{\cos x}{x}\to0$，故水平渐近线为
$$
y=\frac15.
$$

### 第 2 题

- 答案：$\dfrac13$

由连续性需取
$$
a=\lim_{x\to0}\frac{1}{x^3}\int_0^x\sin(t^2)\,dt.
$$
这是 $0/0$ 型，对分子分母求导得
$$
a=\lim_{x\to0}\frac{\sin(x^2)}{3x^2}=\frac13.
$$
也可用等价无穷小 $\sin(x^2)\sim x^2$ 得到同样结论。

### 第 3 题

- 答案：$\dfrac12$

令 $u=1+x^2$，则 $du=2x\,dx$，原式为
$$
\frac12\int_1^{+\infty}\frac{du}{u^2}
=-\frac12\left[\frac1u\right]_1^{+\infty}
=\frac12.
$$

### 第 4 题

- 答案：$y=Cxe^{-x}$

分离变量得
$$
\frac{dy}{y}=\left(\frac1x-1\right)dx.
$$
积分得
$$
\ln|y|=\ln|x|-x+C,
$$
因而
$$
y=Cxe^{-x}.
$$

### 第 5 题

- 答案：$-e$

先令 $x=0$，得 $y(0)=1$。对方程两边求导：
$$
y'=-e^y-xe^y y'.
$$
令 $x=0,y=1$，得
$$
y'(0)=-e.
$$

### 第 6 题

- 答案：$2$

由
$$
BA=B+2E
$$
得
$$
B(A-E)=2E.
$$
两边取行列式：
$$
|B|\cdot|A-E|=|2E|=4.
$$
又
$$
|A-E|=\begin{vmatrix}1&1\\-1&1\end{vmatrix}=2,
$$
所以
$$
|B|=\frac{4}{2}=2.
$$

### 第 7 题

- 答案：A

由 $f'(x_0)>0$ 且 $\Delta x>0$，有
$$
dy=f'(x_0)\Delta x>0.
$$
再由拉格朗日中值定理，
$$
\Delta y-dy=f''(\eta)\frac{(\Delta x)^2}{2}>0.
$$
因而
$$
0<dy<\Delta y.
$$

### 第 8 题

- 答案：B

设
$$
F(x)=\int_0^x f(t)\,dt.
$$
因为 $f$ 在任意有限区间上可积，所以 $F$ 处处连续。又
$$
F(-x)=\int_0^{-x}f(t)\,dt
=-\int_0^x f(-u)\,du
=\int_0^x f(u)\,du
=F(x),
$$
所以 $F$ 为连续的偶函数。

### 第 9 题

- 答案：C

对
$$
h(x)=e^{1+g(x)}
$$
求导得
$$
h'(x)=g'(x)e^{1+g(x)}.
$$
代入 $x=1$：
$$
1=2e^{1+g(1)}.
$$
故
$$
e^{1+g(1)}=\frac12,\qquad g(1)=\ln\frac12-1=-\ln2-1.
$$

### 第 10 题

- 答案：D

齐次部分对应特征根为 $1,-2$，故齐次方程为
$$
y''+y'-2y=0.
$$
再把特解 $y^*=xe^x$ 代入左边：
$$
(y^*)''+(y^*)'-2y^*=3e^x.
$$
因而所求方程为
$$
y''+y'-2y=3e^x.
$$

### 第 11 题

- 答案：C

积分区域满足
$$
0\le r\le1,\qquad 0\le\theta\le\frac{\pi}{4},
$$
即第一象限内圆 $x^2+y^2\le1$ 且位于直线 $y\le x$ 之下的部分。改写为直角坐标：
$$
0\le y\le \frac{\sqrt2}{2},\qquad y\le x\le\sqrt{1-y^2}.
$$
故选
$$
\int_0^{\sqrt2/2}dy\int_y^{\sqrt{1-y^2}}f(x,y)\,dx.
$$

### 第 12 题

- 答案：D

由隐函数定理可在邻域内把约束写成 $y=y(x)$。极值点满足
$$
\frac{d}{dx}f(x,y(x))\Big|_{x=x_0}=0,
$$
即
$$
f'_x(x_0,y_0)+f'_y(x_0,y_0)\,y'(x_0)=0.
$$
又
$$
y'(x_0)=-\frac{\varphi'_x(x_0,y_0)}{\varphi'_y(x_0,y_0)}
$$
且 $\varphi'_y(x_0,y_0)\ne0$。若 $f'_x(x_0,y_0)\ne0$，则必有 $f'_y(x_0,y_0)\ne0$，故选 D。

### 第 13 题

- 答案：A

若 $\alpha_1,\dots,\alpha_s$ 线性相关，则存在不全为零的 $k_1,\dots,k_s$ 使
$$
k_1\alpha_1+\cdots+k_s\alpha_s=0.
$$
左乘 $A$ 得
$$
k_1A\alpha_1+\cdots+k_sA\alpha_s=0.
$$
因而 $A\alpha_1,\dots,A\alpha_s$ 必线性相关，故选 A。

### 第 14 题

- 答案：B

把第 $2$ 行加到第 $1$ 行相当于左乘 $P$，故
$$
B=PA.
$$
再将第 $1$ 列的 $-1$ 倍加到第 $2$ 列，相当于右乘
$$
Q=\begin{pmatrix}
1&-1&0\\
0&1&0\\
0&0&1
\end{pmatrix}=P^{-1}.
$$
所以
$$
C=BQ=PAP^{-1}.
$$

### 第 15 题

- 答案：$A=\dfrac13,\ B=-\dfrac23,\ C=\dfrac16$

展开
$$
e^x=1+x+\frac{x^2}{2}+\frac{x^3}{6}+o(x^3).
$$
与 $1+Bx+Cx^2$ 相乘后比较各阶系数，得
$$
\begin{cases}
1+B-A=0,\\
1+2B+2C=0,\\
1+3B+6C=0.
\end{cases}
$$
解得
$$
A=\frac13,\qquad B=-\frac23,\qquad C=\frac16.
$$

### 第 16 题

- 答案：$-\dfrac{\arcsin e^x}{e^x}+\dfrac12\ln\left\lvert\dfrac{\sqrt{1-e^{2x}}-1}{\sqrt{1-e^{2x}}+1}\right\rvert+C$

令 $t=e^x$，则 $dt=e^x\,dx$，原式化为
$$
\int \frac{\arcsin t}{t^2}\,dt.
$$
分部积分：
$$
\int \frac{\arcsin t}{t^2}\,dt
=-\frac{\arcsin t}{t}+\int \frac{dt}{t\sqrt{1-t^2}}.
$$
再令 $u=\sqrt{1-t^2}$，可得
$$
\int \frac{dt}{t\sqrt{1-t^2}}
=\frac12\ln\left|\frac{u-1}{u+1}\right|+C.
$$
还原 $t=e^x,\ u=\sqrt{1-e^{2x}}$ 即得
$$
\int \frac{\arcsin e^x}{e^x}\,dx
=-\frac{\arcsin e^x}{e^x}
+\frac12\ln\left|\frac{\sqrt{1-e^{2x}}-1}{\sqrt{1-e^{2x}}+1}\right|+C.
$$

### 第 17 题

- 答案：$\dfrac{\pi}{2}\ln2$

将被积函数拆成
$$
\frac{1}{1+x^2+y^2}+\frac{xy}{1+x^2+y^2}.
$$
区域 $D$ 关于 $x$ 轴对称，而 $\dfrac{xy}{1+x^2+y^2}$ 对 $y$ 是奇函数，因此该部分积分为 $0$。
故
$$
I=\iint_D\frac{1}{1+x^2+y^2}\,dxdy.
$$
用极坐标：$0\le r\le1,\ -\dfrac{\pi}{2}\le\theta\le\dfrac{\pi}{2}$，
$$
I=\int_{-\pi/2}^{\pi/2}\!\!d\theta\int_0^1\frac{r}{1+r^2}\,dr
=\pi\cdot\frac12\ln(1+r^2)\Big|_0^1
=\frac{\pi}{2}\ln2.
$$

### 第 18 题

- 答案：（I）$\lim\limits_{n\to\infty}x_n=0$；（II）$e^{-1/6}$

因为 $0<x_n<\pi$ 时有
$$
0<\sin x_n<x_n,
$$
所以 $\{x_n\}$ 单调递减且有下界 $0$，故极限存在。设极限为 $A$，则
$$
A=\sin A.
$$
在 $[0,\pi)$ 上仅有解 $A=0$，故
$$
\lim_{n\to\infty}x_n=0.
$$
对第二问，用
$$
\sin x=x-\frac{x^3}{6}+o(x^3),
$$
得
$$
\frac{x_{n+1}}{x_n}=\frac{\sin x_n}{x_n}=1-\frac{x_n^2}{6}+o(x_n^2).
$$
因而
$$
\left(\frac{x_{n+1}}{x_n}\right)^{1/x_n^2}\to e^{-1/6}.
$$

### 第 19 题

- 答案：见解析

设
$$
f(x)=x\sin x+2\cos x+\pi x.
$$
则
$$
f'(x)=x\cos x-\sin x+\pi,\qquad
f''(x)=-x\sin x<0\quad(0<x<\pi).
$$
所以 $f'(x)$ 在 $(0,\pi)$ 上严格递减。又
$$
f'(\pi)=\pi\cos\pi-\sin\pi+\pi=0,
$$
因而对任意 $0<x<\pi$，都有 $f'(x)>0$，即 $f$ 在 $(0,\pi)$ 上严格递增。由 $a<b$ 得
$$
f(b)>f(a),
$$
即原不等式成立。

### 第 20 题

- 答案：（I）成立；（II）$f(u)=\ln u$

设 $u=\sqrt{x^2+y^2}$，则
$$
z_x=f'(u)\frac{x}{u},\qquad z_y=f'(u)\frac{y}{u}.
$$
继续求二阶偏导并相加，可得
$$
z_{xx}+z_{yy}=f''(u)+\frac{f'(u)}{u}.
$$
由题设 $z_{xx}+z_{yy}=0$，故
$$
f''(u)+\frac{f'(u)}{u}=0.
$$
令 $p=f'(u)$，则
$$
p'+\frac{1}{u}p=0,
$$
解得
$$
p=\frac{C}{u}.
$$
由 $f'(1)=1$ 得 $C=1$，故
$$
f'(u)=\frac1u.
$$
积分得
$$
f(u)=\ln u+C_1.
$$
再由 $f(1)=0$ 得 $C_1=0$，所以
$$
f(u)=\ln u.
$$

### 第 21 题

- 答案：（I）$t>0$ 时曲线下凹；（II）切点 $(2,3)$，切线 $y=x+1$；（III）面积 $\dfrac73$

由参数方程得
$$
\frac{dy}{dx}=\frac{4-2t}{2t}=\frac2t-1,
$$
进一步
$$
\frac{d^2y}{dx^2}
=\frac{d}{dt}\!\left(\frac2t-1\right)\Big/\frac{dx}{dt}
=-\frac1{t^3}<0\quad(t>0),
$$
故曲线在 $t>0$ 时下凹。
设切点对应参数为 $t_0$，切线过 $(-1,0)$，则
$$
0-(4t_0-t_0^2)=\left(\frac2{t_0}-1\right)(-1-(t_0^2+1)).
$$
化简得 $(t_0-1)(t_0+2)=0$，由 $t_0\ge0$ 得 $t_0=1$。所以
$$
(x_0,y_0)=(2,3),\qquad y=x+1.
$$
对应 $x\le2$ 的曲线部分与直线及 $x$ 轴围成面积，计算可得
$$
S=\frac73.
$$

### 第 22 题

- 答案：（I）$r(A)=2$；（II）$a=2,\ b=-3$，通解为 $(2,-3,0,0)^T+c_1(-2,1,1,0)^T+c_2(4,-5,0,1)^T$

非齐次方程组有三个线性无关解，则任意两解之差是对应齐次方程的解，且可得到两个线性无关的齐次解。
因而
$$
4-r(A)\ge2,
$$
即 $r(A)\le2$。又原矩阵前两行线性无关，所以 $r(A)\ge2$，从而
$$
r(A)=2.
$$
对增广矩阵作初等变换，可由 $r(A)=2$ 推出
$$
4-2a=0,\qquad 4a+b-5=0,
$$
故
$$
a=2,\qquad b=-3.
$$
此时化简方程组得
$$
\begin{cases}
x_1=2-2x_3+4x_4,\\
x_2=-3+x_3-5x_4.
\end{cases}
$$
令 $x_3=c_1,\ x_4=c_2$，则通解为
$$
(2,-3,0,0)^T+c_1(-2,1,1,0)^T+c_2(4,-5,0,1)^T.
$$

### 第 23 题

- 答案：（I）特征值为 $3,0,0$；（II）可取 $\Lambda=\operatorname{diag}(3,0,0)$，相应正交矩阵见解析

因为 $A\alpha_1=0,\ A\alpha_2=0$，所以 $\alpha_1,\alpha_2$ 都是特征值 $0$ 的特征向量，且二者线性无关，
因而 $0$ 至少是二重特征值。
又各行元素和为 $3$，所以
$$
A(1,1,1)^T=(3,3,3)^T=3(1,1,1)^T,
$$
故 $(1,1,1)^T$ 是特征值 $3$ 的特征向量。
因此
$$
\lambda_1=3,\qquad \lambda_2=\lambda_3=0.
$$
取
$$
\eta_3=\frac1{\sqrt3}(1,1,1)^T,
$$
再对 $\alpha_1,\alpha_2$ 在特征值 $0$ 的子空间内作施密特正交化，可取
$$
\eta_1=\left(0,-\frac{\sqrt2}{2},\frac{\sqrt2}{2}\right)^T,\qquad
\eta_2=\left(-\frac{\sqrt6}{3},\frac{\sqrt6}{6},\frac{\sqrt6}{6}\right)^T.
$$
令
$$
Q=(\eta_1,\eta_2,\eta_3),
$$
则 $Q$ 为正交矩阵，且
$$
Q^TAQ=\operatorname{diag}(0,0,3).
$$
若按特征值顺序写成 $\operatorname{diag}(3,0,0)$，只需调整列向量次序即可。
