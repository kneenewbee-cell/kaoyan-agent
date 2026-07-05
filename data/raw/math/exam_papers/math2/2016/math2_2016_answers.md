# 2016 年数学二答案解析

资料类型：考研数学二答案解析
年份：2016
科目：数学二
整理状态：结合答案册页图与本地复算整理为精炼版解析。

## 答案速查

| 题号 | 题型 | 答案 |
|---|---|---|
| 1 | 选择题 | B |
| 2 | 选择题 | D |
| 3 | 选择题 | B |
| 4 | 选择题 | B |
| 5 | 选择题 | A |
| 6 | 选择题 | D |
| 7 | 选择题 | C |
| 8 | 选择题 | C |
| 9 | 填空题 | $y=x+\dfrac{\pi}{2}$ |
| 10 | 填空题 | $\sin1-\cos1$ |
| 11 | 填空题 | $y'-y=2x-x^2$ |
| 12 | 填空题 | $5\cdot 2^{n-1}$ |
| 13 | 填空题 | $2\sqrt{2}\,v_0$ |
| 14 | 填空题 | 2 |
| 15 | 解答题 | $e^{1/3}$ |
| 16 | 解答题 | 见详解 |
| 17 | 解答题 | 见详解 |
| 18 | 解答题 | $1-\dfrac{\pi}{2}$ |
| 19 | 解答题 | 见详解 |
| 20 | 解答题 | 见详解 |
| 21 | 解答题 | 见详解 |
| 22 | 解答题 | 见详解 |
| 23 | 解答题 | 见详解 |

## 详细解析

### 第 1 题

- 标准答案：B

由
$\cos\sqrt{x}-1\sim-\dfrac{x}{2}$，
$\ln(1+\sqrt[3]{x})\sim \sqrt[3]{x}$，
$\sqrt[3]{x+1}-1\sim\dfrac{x}{3}$，
得
$$
\alpha_1\sim -\frac{x^2}{2},\qquad
\alpha_2\sim x^{5/6},\qquad
\alpha_3\sim \frac{x}{3}.
$$
比较幂次可知从低阶到高阶为 $\alpha_2,\alpha_3,\alpha_1$，故选 B。

### 第 2 题

- 标准答案：D

分段积分得
$$
F(x)=
\begin{cases}
(x-1)^2+C_1, & x<1,\\
x(\ln x-1)+C_2, & x\ge1.
\end{cases}
$$
原函数应在分界点连续。令 $x\to1^-$ 与 $x\to1^+$，得
$C_1=C_2-1$。选项 D 恰满足这一连续条件，故为所求。

### 第 3 题

- 标准答案：B

令 $u=\dfrac1x$，则
$$
\int \frac1{x^2}e^{1/x}\,dx=-e^{1/x}+C.
$$
对于 ①，
$$
\int_{-\infty}^{0}\frac1{x^2}e^{1/x}\,dx
=\lim_{R\to-\infty,c\to0^-}\left[-e^{1/x}\right]_{R}^{c}=1,
$$
收敛。对于 ②，因 $x\to0^+$ 时 $e^{1/x}\to+\infty$，对应原函数趋于 $-\infty$，故发散。选 B。

### 第 4 题

- 标准答案：B

由 $f'(x)$ 的符号变化判断极值：图中只有两处发生由正到负或由负到正的变化，因此 $f(x)$ 有 2 个极值点。拐点对应 $f'(x)$ 的单调性改变处，包括一处不可导尖点及两处局部极值点，所以共有 3 个拐点。故选 B。

### 第 5 题

- 标准答案：A

由 $f_i''(x_0)<0$ 知两曲线在该点附近均为凹曲线，所以公切线位于曲线上方，即
$f_1(x)\le g(x),\ f_2(x)\le g(x)$。又因曲率
$$
K=\frac{|f''(x_0)|}{\left[1+\left(f'(x_0)\right)^2\right]^{3/2}}
$$
且公切意味着 $f_1'(x_0)=f_2'(x_0)$，由 $K_1>K_2$ 得 $|f_1''(x_0)|>|f_2''(x_0)|$，结合二者都小于 0 可知 $f_1$ 向下弯得更厉害，因此在切点附近 $f_1(x)\le f_2(x)$。故选 A。

### 第 6 题

- 标准答案：D

计算得
$$
f_x'=\frac{e^x(x-y)-e^x}{(x-y)^2},\qquad
f_y'=\frac{e^x}{(x-y)^2}.
$$
因而
$$
f_x'+f_y'=\frac{e^x(x-y)}{(x-y)^2}=\frac{e^x}{x-y}=f.
$$
故选 D。

### 第 7 题

- 标准答案：C

若 $B=P^{-1}AP$，则
$$
B^{\mathsf T}=P^{\mathsf T}A^{\mathsf T}(P^{\mathsf T})^{-1},\qquad
B^{-1}=P^{-1}A^{-1}P,
$$
因而 A、B 两项正确。又
$$
B+B^{-1}=P^{-1}(A+A^{-1})P,
$$
故 D 也正确。对于 $A+A^{\mathsf T}$ 与 $B+B^{\mathsf T}$，相似关系一般不保持，故错误项为 C。

### 第 8 题

- 标准答案：C

二次型对应对称矩阵
$$
A=\begin{pmatrix}
a&1&1\\
1&a&1\\
1&1&a
\end{pmatrix}.
$$
其特征值为 $a-1,a-1,a+2$。正、负惯性指数分别为 1、2，说明三个特征值中一正两负，于是
$$
a+2>0,\qquad a-1<0,
$$
即 $-2<a<1$。故选 C。

### 第 9 题

- 标准答案：$y=x+\dfrac{\pi}{2}$

记 $f(x)=\dfrac{x^3}{1+x^2}+\arctan(1+x^2)$。则
$$
\lim_{x\to\infty}\frac{f(x)}{x}
=\lim_{x\to\infty}\left(\frac{x^2}{1+x^2}+\frac{\arctan(1+x^2)}{x}\right)=1.
$$
再算截距：
$$
\lim_{x\to\infty}[f(x)-x]
=\lim_{x\to\infty}\left(-\frac{x}{1+x^2}+\arctan(1+x^2)\right)=\frac{\pi}{2}.
$$
故斜渐近线为 $y=x+\dfrac{\pi}{2}$。

### 第 10 题

- 标准答案：$\sin1-\cos1$

原式化为
$$
\frac1n\sum_{i=1}^{n}\frac{i}{n}\sin\frac{i}{n},
$$
是函数 $x\sin x$ 在 $[0,1]$ 上的 Riemann 和，因此极限为
$$
\int_0^1x\sin x\,dx
=\left[-x\cos x+\sin x\right]_0^1
=\sin1-\cos1.
$$

### 第 11 题

- 标准答案：$y'-y=2x-x^2$

两个特解之差为 $e^x$，它应满足对应齐次方程
$$
y'+p(x)y=0.
$$
代入 $y=e^x$ 得 $p(x)=-1$。故原方程可写成
$$
y'-y=q(x).
$$
再将特解 $y=x^2$ 代入，得
$$
2x-x^2=q(x).
$$
因而所求方程为 $y'-y=2x-x^2$。

### 第 12 题

- 标准答案：$5\cdot 2^{n-1}$

对原式求导得
$$
f'(x)=2(x+1)+2f(x).
$$
再求导得
$$
f''(x)=2+2f'(x),\qquad f^{(n)}(x)=2f^{(n-1)}(x)\ (n\ge3).
$$
又由原式知 $f(0)=1$，故
$$
f'(0)=2+2f(0)=4,\qquad f''(0)=2+2f'(0)=10.
$$
因而对 $n\ge2$，
$$
f^{(n)}(0)=2^{n-2}f''(0)=10\cdot2^{n-2}=5\cdot 2^{n-1}.
$$

### 第 13 题

- 标准答案：$2\sqrt{2}\,v_0$

点 $P=(x,x^3)$，故
$$
l=\sqrt{x^2+x^6}.
$$
由链式法则，
$$
\frac{dl}{dt}=\frac{dl}{dx}\frac{dx}{dt}
=\frac{6x^5+2x}{2\sqrt{x^2+x^6}}\,v_0.
$$
在 $x=1$ 处，
$$
\frac{dl}{dt}=\frac{8}{2\sqrt2}v_0=2\sqrt2\,v_0.
$$

### 第 14 题

- 标准答案：2

矩阵等价当且仅当秩相同。右侧矩阵经初等变换可化为秩为 2 的矩阵，所以左侧矩阵也必须满足秩为 2。令
$$
A=\begin{pmatrix}
a&-1&-1\\
-1&a&-1\\
-1&-1&a
\end{pmatrix},
$$
则
$$
|A|=(a+1)^2(a-2).
$$
要使 $r(A)<3$，需 $a=-1$ 或 $a=2$。当 $a=-1$ 时，$r(A)=1$；当 $a=2$ 时，$r(A)=2$，与右侧矩阵秩相同。故 $a=2$。

### 第 15 题

- 标准答案：$e^{1/3}$

设原极限为 $I$。因底数趋于 1，可取对数：
$$
\ln I=\lim_{x\to0}\frac{\ln(\cos2x+2x\sin x)}{x^4}.
$$
先展开
$$
\cos2x=1-2x^2+\frac{2}{3}x^4+o(x^4),\qquad
2x\sin x=2x^2-\frac13x^4+o(x^4),
$$
所以
$$
\cos2x+2x\sin x=1+\frac13x^4+o(x^4).
$$
于是
$$
\ln I=\lim_{x\to0}\frac{\frac13x^4+o(x^4)}{x^4}=\frac13,
$$
故
$$
I=e^{1/3}.
$$

### 第 16 题

- 标准答案：$$
f'(x)=
\begin{cases}
4x^2-2x, & 0<x<1,\\
2, & x=1,\\
2x, & x>1,
\end{cases}
\qquad
f_{\min}=\frac14\ \text{(在 }x=\frac12\text{ 处取得)}.
$$

分情况去绝对值：
当 $0<x<1$ 时，
$$
f(x)=\int_0^x(x^2-t^2)\,dt+\int_x^1(t^2-x^2)\,dt
=\frac43x^3-x^2+\frac13,
$$
故
$$
f'(x)=4x^2-2x.
$$
当 $x\ge1$ 时，
$$
f(x)=\int_0^1(x^2-t^2)\,dt=x^2-\frac13,
$$
因而 $f'(x)=2x$（且 $f'(1)=2$）。
对于 $0<x<1$，令 $f'(x)=0$ 得 $x=\frac12$。比较
$f\!\left(\frac12\right)=\frac14$，以及 $x\ge1$ 时的函数值均不小于 $\frac23$，故最小值为 $\dfrac14$。

### 第 17 题

- 标准答案：$$
z_{\max}=1 \quad\text{(在 }(-1,-1)\text{ 处取得)},
$$
无极小值。

设
$$
F(x,y,z)=(x^2+y^2)z+\ln z+2(x+y+1)=0.
$$
由隐函数求导公式，在极值点应有 $z_x=z_y=0$。分别对 $x,y$ 求偏导并令 $z_x=z_y=0$，得
$$
2xz+2=0,\qquad 2yz+2=0,
$$
即
$$
x=y=-\frac1z.
$$
代回原方程得
$$
\frac{2}{z}+\ln z+2\left(-\frac2z+1\right)=0
\Longrightarrow \ln z-\frac2z+2=0.
$$
易验得 $z=1$ 是解，从而 $x=y=-1$。再由二阶偏导计算可得在该点
$$
z_{xx}=z_{yy}=-\frac23,\qquad z_{xy}=0,
$$
Hessian 负定，所以此点为极大点，极大值为 1。方程不存在更小的局部极值点，故无极小值。

### 第 18 题

- 标准答案：$1-\dfrac{\pi}{2}$

区域 $D$ 为顶角在原点、上边界为 $y=1$ 的等腰三角形。改用极坐标
$$
x=r\cos\theta,\qquad y=r\sin\theta,
$$
则
$$
\frac{x^2-xy-y^2}{x^2+y^2}
=\cos^2\theta-\cos\theta\sin\theta-\sin^2\theta.
$$
区域对应
$$
\frac{\pi}{4}\le\theta\le\frac{3\pi}{4},\qquad 0\le r\le \frac1{\sin\theta}.
$$
因此
$$
\iint_D \frac{x^2-xy-y^2}{x^2+y^2}\,dx\,dy
=\int_{\pi/4}^{3\pi/4}\int_0^{1/\sin\theta}
(\cos^2\theta-\cos\theta\sin\theta-\sin^2\theta)\,r\,dr\,d\theta
=1-\frac{\pi}{2}.
$$

### 第 19 题

- 标准答案：$$
u(x)=-(2x+1)e^{-x},
\qquad
y=C_1e^x+C_2(2x+1).
$$

令 $y=u(x)e^x$ 代入原方程。利用已知解 $e^x$ 进行降阶，可化为关于 $v=u'$ 的一阶方程
$$
(2x-1)v'+(2x-3)v=0.
$$
解得
$$
v=u'=C(2x-1)e^{-x}.
$$
积分可得
$$
u(x)=A(-(2x+1)e^{-x})+B.
$$
代入条件 $u(-1)=e,\ u(0)=-1$，解得 $A=1,\ B=0$，故
$$
u(x)=-(2x+1)e^{-x}.
$$
于是
$$
y_2(x)=u(x)e^x=-(2x+1),
$$
与 $e^x$ 线性无关，所以通解为
$$
y=C_1e^x+C_2(2x+1).
$$

### 第 20 题

- 标准答案：$$
V=\frac{18\pi}{35},\qquad S=\frac{16\pi}{5}.
$$

外边界为四分之一单位圆 $y=\sqrt{1-x^2}$，内边界为星形线第一象限弧
$x^{2/3}+y^{2/3}=1$。体积由垫片法得
$$
V=\pi\int_0^1\left[(1-x^2)-\left(1-x^{2/3}\right)^3\right]dx
=\frac{18\pi}{35}.
$$
表面积等于两条母线旋转所得面积之和。圆弧部分
$$
S_1=2\pi\int_0^1 y\sqrt{1+(y')^2}\,dx=2\pi.
$$
星形线用参数方程计算：
$$
x=\cos^3 t,\quad y=\sin^3 t,\quad
ds=\sqrt{\left(\frac{dx}{dt}\right)^2+\left(\frac{dy}{dt}\right)^2}\,dt
=3\sin t\cos t\,dt.
$$
故
$$
S_2=2\pi\int_0^{\pi/2} y\,ds
=2\pi\int_0^{\pi/2}\sin^3 t\cdot 3\sin t\cos t\,dt
=\frac{6\pi}{5}.
$$
因此
$$
S=S_1+S_2=2\pi+\frac{6\pi}{5}=\frac{16\pi}{5}.
$$

### 第 21 题

- 标准答案：(I) 平均值为
$$
\frac{1}{3\pi}.
$$
(II) $f(x)$ 在 $\left(0,\dfrac{3\pi}{2}\right)$ 内恰有一个零点。

设
$$
a=\frac{3\pi}{2}.
$$
由分部积分，
$$
\int_0^a f(x)\,dx=[xf(x)]_0^a-\int_0^a x f'(x)\,dx.
$$
又
$$
f'(x)=\frac{\cos x}{2x-3\pi},
\qquad
x=\frac12(2x-3\pi)+\frac{3\pi}{2},
$$
从而
$$
\int_0^a x f'(x)\,dx
=\frac12\int_0^a \cos x\,dx+\frac{3\pi}{2}\int_0^a f'(x)\,dx
=-\frac12+\frac{3\pi}{2}(f(a)-f(0)).
$$
代回后消去 $f(a)$，得
$$
\int_0^a f(x)\,dx=\frac12,
$$
所以平均值为
$$
\frac{1}{a}\cdot\frac12=\frac1{3\pi}.
$$

对于唯一性，注意到
$$
f'(x)=\frac{\cos x}{2x-3\pi}.
$$
在 $\left(0,\dfrac{\pi}{2}\right)$ 上，$\cos x>0$ 且分母 $<0$，故 $f'(x)<0$；在 $\left(\dfrac{\pi}{2},\dfrac{3\pi}{2}\right)$ 上，$\cos x<0$ 且分母仍 $<0$，故 $f'(x)>0$。因此 $f$ 先减后增。
又 $f(0)=0$，且平均值为正，所以函数在后半段必须升回到正值，因而至少有一个零点。由于其单调性仅改变一次，故零点只能有一个，遂知在 $\left(0,\dfrac{3\pi}{2}\right)$ 内恰有一个零点。

### 第 22 题

- 标准答案：(I) $a=0$；

(II)
$$
x=
\begin{pmatrix}
1\\
-2\\
0
\end{pmatrix}
+t
\begin{pmatrix}
0\\
-1\\
1
\end{pmatrix},
\qquad t\in\mathbb{R}.
$$

要使 $Ax=\beta$ 无解，必须有
$$
r(A)<r(A,\beta).
$$
先算
$$
\det A=a(a-2).
$$
当 $a=2$ 时，直接验算增广矩阵秩仍为 2，方程有解；当 $a=0$ 时，$r(A)=2,\ r(A,\beta)=3$，故恰无解，因此 $a=0$。

取 $a=0$ 后，
$$
A=
\begin{pmatrix}
1&1&1\\
1&0&0\\
1&1&1
\end{pmatrix},
\qquad
\beta=
\begin{pmatrix}
0\\
1\\
-2
\end{pmatrix}.
$$
法方程
$A^{\mathsf T}Ax=A^{\mathsf T}\beta$
的解集等于最小二乘解集。求解可得一个特解
$$
x_0=\begin{pmatrix}1\\-2\\0\end{pmatrix},
$$
齐次方程 $Ax=0$ 的基础解系可取
$$
\begin{pmatrix}0\\-1\\1\end{pmatrix}.
$$
因此通解为
$$
x=x_0+t\begin{pmatrix}0\\-1\\1\end{pmatrix},\quad t\in\mathbb R.
$$

### 第 23 题

- 标准答案：$$
A^{99}=
\begin{pmatrix}
2^{99}-2 & -(2^{99}-1) & -(2^{98}-2)\\
2^{100}-2 & -(2^{100}-1) & -(2^{99}-2)\\
0&0&0
\end{pmatrix}.
$$

因而
$$
\beta_1=(2^{99}-2)\alpha_1+(2^{100}-2)\alpha_2,
$$
$$
\beta_2=-(2^{99}-1)\alpha_1-(2^{100}-1)\alpha_2,
$$
$$
\beta_3=-(2^{98}-2)\alpha_1-(2^{99}-2)\alpha_2.
$$

由直接乘法可归纳得到
$$
A^n=
\begin{pmatrix}
(-1)^{n-1}(2^n-2) & (-1)^n(2^n-1) & (-1)^n(2^{n-1}-2)\\
(-1)^{n-1}(2^{n+1}-2) & (-1)^n(2^{n+1}-1) & (-1)^n(2^n-2)\\
0&0&0
\end{pmatrix}\quad(n\ge1).
$$
取 $n=99$ 即得
$$
A^{99}=
\begin{pmatrix}
2^{99}-2 & -(2^{99}-1) & -(2^{98}-2)\\
2^{100}-2 & -(2^{100}-1) & -(2^{99}-2)\\
0&0&0
\end{pmatrix}.
$$

又由 $B^2=BA$，可归纳得
$$
B^n=BA^{n-1}\qquad(n\ge2).
$$
因此
$$
B^{100}=BA^{99}.
$$
因 $B=(\alpha_1,\alpha_2,\alpha_3)$，右乘矩阵时各列恰对应 $\alpha_1,\alpha_2,\alpha_3$ 的线性组合，所以 $B^{100}$ 的三列正是 $A^{99}$ 三列作为系数得到的组合。第三行全为 0，故三列都不含 $\alpha_3$ 项，结果如上。
