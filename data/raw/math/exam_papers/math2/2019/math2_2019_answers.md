# 2019 年数学二答案解析

资料类型：考研数学二答案解析
年份：2019
科目：数学二
整理状态：基于答案解析页图与题面交叉清洗。

## 答案速查

| 题号 | 题型 | 答案 |
|---|---|---|
| 1 | 选择题 | C |
| 2 | 选择题 | B |
| 3 | 选择题 | D |
| 4 | 选择题 | D |
| 5 | 选择题 | A |
| 6 | 选择题 | A |
| 7 | 选择题 | A |
| 8 | 选择题 | C |
| 9 | 填空题 | $4e^2$ |
| 10 | 填空题 | $\dfrac{3\pi}{2}+2$ |
| 11 | 填空题 | $y\,f\!\left(\dfrac{y^2}{x}\right)$ |
| 12 | 填空题 | $\dfrac12\ln3$ |
| 13 | 填空题 | $\dfrac{\cos1-1}{4}$ |
| 14 | 填空题 | -4 |
| 15 | 解答题 | $f'(x)= \begin{cases} x^{2x}(2\ln x+2),& x>0,\\ (x+1)e^x,& x<0, \end{cases}$ 且 $x=0$ 处不可导。 极小值点：$x=-1,\ \dfrac1e$，对应极小值分别为 $1-\dfrac1e,\ \left(\dfrac1e\right)^{2/e}$； 极大值点：$x=0$，极大值为 $1$。 |
| 16 | 解答题 | $$ -2\ln\lvert x-1\rvert-\frac{3}{x-1}+\ln(x^2+x+1)+C. $$ |
| 17 | 解答题 | (1) $y(x)=\sqrt{x}\,e^{x^2/2}$； (2) $V=\dfrac{\pi}{2}(e^4-e)$。 |
| 18 | 解答题 | $\dfrac{43\sqrt2}{120}$ |
| 19 | 解答题 | $S_n=\frac12\left[1+\frac{2e^{-\pi}(1-e^{-n\pi})}{1-e^{-\pi}}-e^{-n\pi}\right], \qquad \lim_{n\to\infty}S_n=\frac12+\frac{1}{e^\pi-1}.$ |
| 20 | 解答题 | $a=-\dfrac34,\quad b=\dfrac34$ |
| 21 | 证明题 | 结论成立 |
| 22 | 解答题 | $a\ne-1$。 当 $a\ne\pm1$ 时， $\beta_3=\alpha_1-\alpha_2+\alpha_3.$ 当 $a=1$ 时，也有 $\beta_3=\alpha_1-\alpha_2+\alpha_3,$ 亦可写成 $\beta_3=(-2k+3)\alpha_1+(k-2)\alpha_2+k\alpha_3\quad (k\in\mathbb R).$ |
| 23 | 解答题 | (I) $x=3,\ y=-2$； (II) 可取 $P= \begin{pmatrix} -1&-1&-1\\ 2&1&2\\ 0&0&4 \end{pmatrix}.$ |

## 详细解析

### 第 1 题

- 答案：C

由
$$
\tan x=x+\frac13x^3+o(x^3)
$$
得
$$
x-\tan x\sim-\frac13x^3.
$$
故与 $x^3$ 同阶，选 C。

### 第 2 题

- 答案：B

$$
y'=x\cos x-\sin x,\qquad y''=-x\sin x.
$$
令 $y''=0$ 得候选点 $x=0,\pi$。在 $(-\frac\pi2,0)$ 与 $(0,\pi)$ 上有 $y''<0$，故 $(0,2)$ 不是拐点；在 $(\pi,\frac{3\pi}{2})$ 上 $y''>0$，所以 $x=\pi$ 为拐点。此时
$$
y(\pi)=\pi\sin\pi+2\cos\pi=-2.
$$
选 B。

### 第 3 题

- 答案：D

前三项分别可直接积分或换元判断收敛：
$$
\int_0^{+\infty}xe^{-x}dx=\Gamma(2)=1,\quad
\int_0^{+\infty}xe^{-x^2}dx=\frac12,
$$
$$
\int_0^{+\infty}\frac{\arctan x}{1+x^2}dx
=\frac12(\arctan x)^2\Big|_0^{+\infty}
=\frac{\pi^2}{8}.
$$
而
$$
\frac{x}{1+x^2}\sim\frac1x\quad (x\to+\infty),
$$
故对应反常积分发散。选 D。

### 第 4 题

- 答案：D

齐次方程通解为 $(C_1+C_2x)e^{-x}$，说明特征根为 $-1,-1$，故
$$
\lambda^2+a\lambda+b=(\lambda+1)^2
$$
从而 $a=2,\ b=1$。再代入特解 $y_p=e^x$，
$$
y_p''+ay_p'+by_p=(1+2+1)e^x=4e^x,
$$
所以 $c=4$。选 D。

### 第 5 题

- 答案：A

设 $r=\sqrt{x^2+y^2}$。因 $r\ge0$ 且 $\sin r\le r$，可知 $I_2<I_1$。又
$$
1-\cos r=2\sin^2\frac r2,\qquad
\sin r=2\sin\frac r2\cos\frac r2.
$$
在区域 $D$ 内有 $r\le \dfrac{\pi}{2}$，故 $\dfrac r2\in[0,\dfrac{\pi}{4}]$，从而
$$
\sin\frac r2\le\cos\frac r2.
$$
因此
$$
1-\cos r\le\sin r,
$$
即 $I_3<I_2$。综上 $I_3<I_2<I_1$，选 A。

### 第 6 题

- 答案：A

由极限条件先得
$$
f(a)=g(a),\qquad f'(a)=g'(a),
$$
再对商继续处理可得
$$
f''(a)=g''(a).
$$
因此两曲线在对应点相切且曲率相等，所以它是充分条件。反过来，仅知相切与曲率相等并不能推出上述二阶小量极限一定为 0，故不是必要条件。选 A。

### 第 7 题

- 答案：A

基础解系有 2 个向量，说明
$$
4-r(A)=2 \Rightarrow r(A)=2.
$$
对 4 阶矩阵，当 $r(A)\le n-2$ 时伴随矩阵全为零矩阵，因此
$$
r(A^*)=0.
$$
选 A。

### 第 8 题

- 答案：C

设 $\lambda$ 为 $A$ 的特征值，则
$$
\lambda^2+\lambda-2=0,
$$
故 $\lambda=1$ 或 $\lambda=-2$。又
$$
|A|=\lambda_1\lambda_2\lambda_3=4,
$$
只能是一个特征值为 1、两个特征值为 $-2$。因此实对称矩阵对应二次型经正交变换后有 1 个正平方项、2 个负平方项，规范形为
$$
y_1^2-y_2^2-y_3^2.
$$
选 C。

### 第 9 题

- 答案：$4e^2$

写成
$$
(1+x+2^x-1)^{2/x}.
$$
由指数型极限，
$$
\lim_{x\to0}(1+u)^{2/x}=e^{\lim \frac{2u}{x}},
$$
其中
$$
u=x+2^x-1.
$$
又
$$
\lim_{x\to0}\frac{2(x+2^x-1)}{x}=2(1+\ln2),
$$
故原极限为
$$
e^{2(1+\ln2)}=4e^2.
$$

### 第 10 题

- 答案：$\dfrac{3\pi}{2}+2$

当 $t=\dfrac{3\pi}{2}$ 时，
$$
\left(x,y\right)=\left(\frac{3\pi}{2}+1,1\right).
$$
又
$$
\frac{dy}{dx}=\frac{\sin t}{1-\cos t},
$$
故此时斜率为 $-1$。切线方程
$$
y-1=-\left(x-\frac{3\pi}{2}-1\right).
$$
令 $x=0$ 得截距
$$
y=\frac{3\pi}{2}+2.
$$

### 第 11 题

- 答案：$y\,f\!\left(\dfrac{y^2}{x}\right)$

直接求偏导：
$$
\frac{\partial z}{\partial x}=-\frac{y^3}{x^2}f'\!\left(\frac{y^2}{x}\right),
$$
$$
\frac{\partial z}{\partial y}=f\!\left(\frac{y^2}{x}\right)+\frac{2y^2}{x}f'\!\left(\frac{y^2}{x}\right).
$$
代入可得
$$
2x\frac{\partial z}{\partial x}+y\frac{\partial z}{\partial y}
=-\frac{2y^3}{x}f'+y f+\frac{2y^3}{x}f'
=y f\!\left(\frac{y^2}{x}\right).
$$

### 第 12 题

- 答案：$\dfrac12\ln3$

有
$$
y'=-\tan x,
$$
故弧长
$$
s=\int_0^{\pi/6}\sqrt{1+\tan^2x}\,dx=\int_0^{\pi/6}\sec x\,dx.
$$
计算得
$$
s=\ln|\sec x+\tan x|\Big|_0^{\pi/6}
=\ln\sqrt3=\frac12\ln3.
$$

### 第 13 题

- 答案：$\dfrac{\cos1-1}{4}$

写成
$$
\int_0^1 x\left(\int_1^x\frac{\sin t^2}{t}\,dt\right)dx
=\int_0^1\left(\int_1^x\frac{\sin t^2}{t}\,dt\right)d\left(\frac{x^2}{2}\right).
$$
交换处理后化为
$$
-\frac12\int_0^1 x\sin x^2\,dx.
$$
再令 $u=x^2$，得
$$
-\frac14\int_0^1\sin u\,du=\frac{\cos1-1}{4}.
$$

### 第 14 题

- 答案：-4

由第一行按代数余子式展开可知
$$
A_{11}-A_{12}=|A'|,
$$
其中
$$
A'=
\begin{pmatrix}
1&0&0\\
-1&-1&1\\
0&3&4
\end{pmatrix}
$$
等价于相应 3 阶行列式。直接计算得
$$
A_{11}-A_{12}=-4.
$$

### 第 15 题

- 答案：$$
f'(x)=
\begin{cases}
x^{2x}(2\ln x+2),& x>0,\\
(x+1)e^x,& x<0,
\end{cases}
$$
且 $x=0$ 处不可导。

极小值点：$x=-1,\ \dfrac1e$，对应极小值分别为 $1-\dfrac1e,\ \left(\dfrac1e\right)^{2/e}$；

极大值点：$x=0$，极大值为 $1$。

当 $x>0$ 时，
$$
f'(x)=(x^{2x})'=x^{2x}(2\ln x+2).
$$
当 $x<0$ 时，
$$
f'(x)=(xe^x+1)'=(x+1)e^x.
$$
由
$$
\lim_{x\to0^+}\frac{f(x)-f(0)}{x}
=\lim_{x\to0^+}\frac{x^{2x}-1}{x}
=\lim_{x\to0^+}2\ln x=-\infty
$$
知 $x=0$ 处不可导。

临界点与不可导点为 $x=-1,0,\dfrac1e$。结合导数符号：
$$
x<-1:\ f'(x)<0,\quad -1<x<0:\ f'(x)>0,
$$
$$
0<x<\frac1e:\ f'(x)<0,\quad x>\frac1e:\ f'(x)>0.
$$
故 $x=-1,\dfrac1e$ 为极小值点，$x=0$ 为极大值点，代入即可得各极值。

### 第 16 题

- 答案：$$
-2\ln\lvert x-1\rvert-\frac{3}{x-1}+\ln(x^2+x+1)+C.
$$

作部分分式分解：
$$
\frac{3x+6}{(x-1)^2(x^2+x+1)}
=\frac{A}{x-1}+\frac{B}{(x-1)^2}+\frac{Cx+D}{x^2+x+1}.
$$
比较系数得
$$
A=-2,\quad B=3,\quad C=2,\quad D=1.
$$
因而
$$
\int \frac{3x+6}{(x-1)^2(x^2+x+1)}dx
=\int\left[-\frac{2}{x-1}+\frac{3}{(x-1)^2}+\frac{2x+1}{x^2+x+1}\right]dx,
$$
计算后得
$$
-2\ln\lvert x-1\rvert-\frac{3}{x-1}+\ln(x^2+x+1)+C.
$$

### 第 17 题

- 答案：(1) $y(x)=\sqrt{x}\,e^{x^2/2}$；

(2) $V=\dfrac{\pi}{2}(e^4-e)$。

这是线性微分方程。乘积分因子 $e^{-x^2/2}$，得
$$
\left(ye^{-x^2/2}\right)'=\frac{1}{2\sqrt{x}}.
$$
积分后
$$
ye^{-x^2/2}=\sqrt{x}+C,
$$
即
$$
y=(\sqrt{x}+C)e^{x^2/2}.
$$
由 $y(1)=\sqrt e$ 得 $C=0$，故
$$
y(x)=\sqrt{x}\,e^{x^2/2}.
$$

旋转体体积
$$
V=\pi\int_1^2 y^2\,dx
=\pi\int_1^2 xe^{x^2}\,dx
=\frac{\pi}{2}e^{x^2}\Big|_1^2
=\frac{\pi}{2}(e^4-e).
$$

### 第 18 题

- 答案：$\dfrac{43\sqrt2}{120}$

由对称性，含 $x$ 的奇部积分为 $0$，原式化为
$$
\iint_D \frac{y}{\sqrt{x^2+y^2}}\,dxdy.
$$
取极坐标
$$
x=r\cos\theta,\qquad y=r\sin\theta.
$$
条件 $|x|\le y$ 化为
$$
\frac{\pi}{4}\le\theta\le\frac{3\pi}{4},
$$
而
$$
(x^2+y^2)^3\le y^4
$$
化为
$$
0\le r\le \sin^2\theta.
$$
所以
$$
\iint_D \frac{x+y}{\sqrt{x^2+y^2}}\,dxdy
=\int_{\pi/4}^{3\pi/4}\int_0^{\sin^2\theta} \sin\theta \cdot r\,dr\,d\theta
=\frac12\int_{\pi/4}^{3\pi/4}\sin^5\theta\,d\theta
=\frac{43\sqrt2}{120}.
$$

### 第 19 题

- 答案：$$
S_n=\frac12\left[1+\frac{2e^{-\pi}(1-e^{-n\pi})}{1-e^{-\pi}}-e^{-n\pi}\right],
\qquad
\lim_{n\to\infty}S_n=\frac12+\frac{1}{e^\pi-1}.
$$

面积按每段正负交替求和：
$$
S_n=\sum_{k=0}^{n-1}(-1)^k\int_{k\pi}^{(k+1)\pi}e^{-x}\sin x\,dx.
$$
原函数可取
$$
\int e^{-x}\sin x\,dx=-\frac12e^{-x}(\sin x+\cos x).
$$
代入端点并整理等比和，得到
$$
S_n=\frac12\left[1+2\sum_{k=1}^{n-1}e^{-k\pi}-e^{-n\pi}\right]
=\frac12\left[1+\frac{2e^{-\pi}(1-e^{-n\pi})}{1-e^{-\pi}}-e^{-n\pi}\right].
$$
令 $n\to\infty$ 即得
$$
\lim_{n\to\infty}S_n=\frac12+\frac{1}{e^\pi-1}.
$$

### 第 20 题

- 答案：$a=-\dfrac34,\quad b=\dfrac34$

将
$$
u=v e^{ax+by}
$$
代入，计算偏导后可得关于 $v$ 的方程：
$$
2v_{xx}-2v_{yy}+(4a+3)v_x+(3-4b)v_y+(2a^2-2b^2+3a+3b)v=0.
$$
要消去一阶偏导项，只需
$$
4a+3=0,\qquad 3-4b=0.
$$
解得
$$
a=-\frac34,\qquad b=\frac34.
$$

### 第 21 题

- 答案：结论成立

设
$$
F(x)=\int_0^x f(t)\,dt,
$$
则 $F'(x)=f(x)$。由积分中值定理，存在 $c\in(0,1)$ 使
$$
\int_0^1f(x)\,dx=f(c)(1-0),
$$
即 $f(c)=1$。而已知 $f(1)=1$，故由罗尔定理，存在 $\xi\in(c,1)\subset(0,1)$ 使
$$
f'(\xi)=0.
$$

再设
$$
\varphi(x)=f(x)+x^2.
$$
则
$$
\varphi(0)=0,\qquad \varphi(c)=1+c^2,\qquad \varphi(1)=2.
$$
由拉格朗日中值定理，存在 $\eta_1\in(0,c),\ \eta_2\in(c,1)$ 使
$$
\varphi'(\eta_1)=\frac{1+c^2}{c}=c+\frac1c,\qquad
\varphi'(\eta_2)=\frac{2-(1+c^2)}{1-c}=1+c.
$$
再对 $\varphi'$ 用拉格朗日中值定理，存在 $\eta\in(\eta_1,\eta_2)$ 使
$$
\varphi''(\eta)=\frac{\varphi'(\eta_2)-\varphi'(\eta_1)}{\eta_2-\eta_1}
=\frac{1-\frac1c}{\eta_2-\eta_1}<0.
$$
又 $\varphi''=f''+2$，故
$$
f''(\eta)+2<0 \Rightarrow f''(\eta)<-2.
$$

### 第 22 题

- 答案：$a\ne-1$。

当 $a\ne\pm1$ 时，
$$
\beta_3=\alpha_1-\alpha_2+\alpha_3.
$$

当 $a=1$ 时，也有
$$
\beta_3=\alpha_1-\alpha_2+\alpha_3,
$$
亦可写成
$$
\beta_3=(-2k+3)\alpha_1+(k-2)\alpha_2+k\alpha_3\quad (k\in\mathbb R).
$$

先算两组向量的秩。对
$$
(\alpha_1,\alpha_2,\alpha_3)
$$
作消元，可得其秩在 $a=-1$ 时为 $2$，在 $a\ne-1$ 时不小于 $2$。再对
$$
(\beta_1,\beta_2,\beta_3)
$$
以及联合向量组
$$
(\alpha_1,\alpha_2,\alpha_3,\beta_1,\beta_2,\beta_3)
$$
消元比较。

当 $a=-1$ 时，两组与联合组秩不一致，因此不等价。

当 $a=1$ 时，两组及联合组秩都为 $2$，故等价。解方程
$$
x_1\alpha_1+x_2\alpha_2+x_3\alpha_3=\beta_3
$$
可得一族表示
$$
\beta_3=(-2k+3)\alpha_1+(k-2)\alpha_2+k\alpha_3.
$$

当 $a\ne\pm1$ 时，两组与联合组秩都为 $3$，故等价，并且表示唯一。解线性方程组得
$$
\beta_3=\alpha_1-\alpha_2+\alpha_3.
$$
综上，等价所需且所求为 $a\ne-1$。

### 第 23 题

- 答案：(I) $x=3,\ y=-2$；

(II) 可取
$$
P=
\begin{pmatrix}
-1&-1&-1\\
2&1&2\\
0&0&4
\end{pmatrix}.
$$

因为 $A\sim B$，所以迹与行列式分别相等。
$$
\operatorname{tr}(A)=x-4,\qquad \operatorname{tr}(B)=y+1,
$$
故
$$
y=x-5.
$$
又
$$
|A|=-2(-2x+4),\qquad |B|=-2y,
$$
所以
$$
y=-2x+4.
$$
联立得
$$
x=3,\qquad y=-2.
$$

于是
$$
A=
\begin{pmatrix}
-2&-2&1\\
2&3&-2\\
0&0&-2
\end{pmatrix},\qquad
B=
\begin{pmatrix}
2&1&0\\
0&-1&0\\
0&0&-2
\end{pmatrix}.
$$
求得 $A$ 属于特征值 $-2,-1,2$ 的线性无关特征向量可分别取
$$
\alpha_1=\begin{pmatrix}-1\\2\\4\end{pmatrix},\quad
\alpha_2=\begin{pmatrix}-2\\1\\0\end{pmatrix},\quad
\alpha_3=\begin{pmatrix}-1\\2\\0\end{pmatrix}.
$$
于是
$$
P_1=(\alpha_1,\alpha_2,\alpha_3),\qquad
P_1^{-1}AP_1=\operatorname{diag}(-2,-1,2).
$$
同理取 $B$ 的相应特征向量组构成 $P_2$，可使
$$
P_2^{-1}BP_2=\operatorname{diag}(-2,-1,2).
$$
因而
$$
P=P_1P_2^{-1}
$$
即可。可取
$$
P=
\begin{pmatrix}
-1&-1&-1\\
2&1&2\\
0&0&4
\end{pmatrix}.
$$
