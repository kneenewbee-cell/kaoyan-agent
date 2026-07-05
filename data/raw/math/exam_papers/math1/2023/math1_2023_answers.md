# Math 1 2023 Answers

资料类型：考研数学一答案解析
年份：2023
科目：数学一
来源：现有题干与答案速查图 `images/answer_quick.png`，逐题补写解析
校对状态：已按题干、答案速查图和数学推导补齐解析

## 答案速查

| 题号 | 题型 | 答案 |
|---|---|---|
| 1 | 选择题 | B |
| 2 | 选择题 | C |
| 3 | 选择题 | C |
| 4 | 选择题 | A |
| 5 | 选择题 | B |
| 6 | 选择题 | D |
| 7 | 选择题 | D |
| 8 | 选择题 | C |
| 9 | 选择题 | D |
| 10 | 选择题 | A |
| 11 | 填空题 | $-2$ |
| 12 | 填空题 | $x+2y-z=0$ |
| 13 | 填空题 | $0$ |
| 14 | 填空题 | $\displaystyle \frac{1}{2}$ |
| 15 | 填空题 | $\displaystyle \frac{11}{9}$ |
| 16 | 填空题 | $\displaystyle \frac{1}{3}$ |
| 17 | 解答题 | (I) $y=x(2-\ln x)$；(II) 最大值为 $\displaystyle \frac{e^4}{4}-\frac{5}{4}$。 |
| 18 | 解答题 | 极小值为 $\displaystyle f\left(\frac{2}{3},\frac{10}{27}\right)=-\frac{4}{729}$。 |
| 19 | 解答题 | $\displaystyle I=\frac{5\pi}{4}$ |
| 20 | 解答题 | 证明见解析。 |
| 21 | 解答题 | (I) 可取 $\displaystyle P=\begin{pmatrix}1&-1&1\\0&1&0\\0&0&1\end{pmatrix}$；(II) 不存在正交变换。 |
| 22 | 解答题 | (I) $\operatorname{Cov}(X,Y)=0$；(II) 不相互独立；(III) $f_Z(z)=2z,\ 0<z<1$，其他为 $0$。 |

## 详细解析

### 第 1 题

**答案：** B

当 $x\to+\infty$ 时，
$$
\ln\left(e+\frac{1}{x-1}\right)
=1+\ln\left(1+\frac{1}{e(x-1)}\right)
=1+\frac{1}{e(x-1)}+o\left(\frac{1}{x}\right).
$$
故
$$
y=x+\frac{x}{e(x-1)}+o(1)\to x+\frac{1}{e}.
$$
斜渐近线为 $y=x+\frac{1}{e}$，选 B。

### 第 2 题

**答案：** C

方程特征根满足
$$
\lambda^2+a\lambda+b=0.
$$
要使所有解在 $(-\infty,+\infty)$ 上有界，不能有非零实部，也不能有零根导致常数以外的增长项。因此特征根应为一对纯虚根
$$
\lambda=\pm i\sqrt{b},
$$
即
$$
a=0,\qquad b>0.
$$
选 C。

### 第 3 题

**答案：** C

当 $t\ge0$ 时，
$$
x=3t,\qquad y=t\sin t.
$$
当 $t<0$ 时，
$$
x=t,\qquad y=-t\sin t.
$$
两侧均有 $f'(0)=0$，且 $f'(x)\to0$，所以 $f'(x)$ 在 $0$ 处连续。

但二阶导数左右极限不同：右侧 $y\sim t^2=x^2/9$，左侧 $y\sim -x^2$，故 $f''(0)$ 不存在。选 C。

### 第 4 题

**答案：** A

因为 $a_n<b_n$，所以 $c_n=b_n-a_n>0$。又
$$
\sum c_n=\sum b_n-\sum a_n
$$
收敛，故 $\sum c_n$ 绝对收敛。

若 $\sum a_n$ 绝对收敛，则
$$
b_n=a_n+c_n
$$
推出 $\sum b_n$ 绝对收敛。反过来，若 $\sum b_n$ 绝对收敛，则
$$
a_n=b_n-c_n
$$
推出 $\sum a_n$ 绝对收敛。故为充分必要条件，选 A。

### 第 5 题

**答案：** B

由 $ABC=O$，对
$$
M_1=\begin{pmatrix}O&A\\BC&E\end{pmatrix}
$$
用 Schur 补可得
$$
r_1=n+r(-ABC)=n.
$$
类似地
$$
r_2=n+r(AB).
$$
而
$$
M_3=\begin{pmatrix}E&AB\\AB&O\end{pmatrix}
$$
的秩为
$$
r_3=n+r((AB)^2)\le n+r(AB)=r_2.
$$
又 $r_3\ge n=r_1$，故
$$
r_1\le r_3\le r_2.
$$
选 B。

### 第 6 题

**答案：** D

A 的特征值 $1,2,3$ 互异，可对角化；B 为实对称矩阵，可正交对角化；C 对特征值 $2$ 的几何重数为 $2$，也可对角化。

D 的特征值为 $1,2,2$。对 $\lambda=2$，
$$
A-2E=
\begin{pmatrix}
-1&1&a\\
0&0&2\\
0&0&0
\end{pmatrix},
$$
其零空间维数为 $1$，小于特征值 $2$ 的代数重数 $2$，故不能相似于对角矩阵。选 D。

### 第 7 题

**答案：** D

设
$$
\gamma=s\alpha_1+t\alpha_2=u\beta_1+v\beta_2.
$$
即
$$
s(1,2,3)^T+t(2,1,1)^T
=u(2,5,9)^T+v(1,0,1)^T.
$$
解该齐次交集条件，得公共向量空间由
$$
(1,5,8)^T
$$
张成。因此
$$
\gamma=k(1,5,8)^T,\quad k\in\mathbb R.
$$
选 D。

### 第 8 题

**答案：** C

若 $X\sim P(1)$，则 $E(X)=1$。于是
$$
E|X-1|
=P(X=0)+\sum_{k=2}^{\infty}(k-1)P(X=k).
$$
又由 $E(X-1)=0$ 得
$$
\sum_{k=2}^{\infty}(k-1)P(X=k)=P(X=0)=e^{-1}.
$$
所以
$$
E|X-E(X)|=\frac{2}{e}.
$$
选 C。

### 第 9 题

**答案：** D

有
$$
\frac{(n-1)S_1^2}{\sigma^2}\sim\chi^2(n-1),\qquad
\frac{(m-1)S_2^2}{2\sigma^2}\sim\chi^2(m-1),
$$
且相互独立。因此
$$
\frac{S_1^2}{S_2^2/2}
=\frac{2S_1^2}{S_2^2}
\sim F(n-1,m-1).
$$
选 D。

### 第 10 题

**答案：** A

因为
$$
X_1-X_2\sim N(0,2\sigma^2),
$$
若 $Z\sim N(0,\tau^2)$，则
$$
E|Z|=\tau\sqrt{\frac{2}{\pi}}.
$$
故
$$
E|X_1-X_2|=\sqrt{2}\sigma\sqrt{\frac{2}{\pi}}
=\frac{2\sigma}{\sqrt{\pi}}.
$$
要使 $a|X_1-X_2|$ 无偏估计 $\sigma$，需
$$
a\cdot\frac{2}{\sqrt{\pi}}=1,
$$
即
$$
a=\frac{\sqrt{\pi}}{2}.
$$
选 A。

### 第 11 题

**答案：** $-2$

展开得
$$
f(x)=ax+bx^2+\ln(1+x)
=(a+1)x+\left(b-\frac{1}{2}\right)x^2+O(x^3).
$$
又
$$
g(x)=e^{x^2}-\cos x
=\left(1+x^2+O(x^4)\right)-\left(1-\frac{x^2}{2}+O(x^4)\right)
=\frac{3}{2}x^2+O(x^4).
$$
二者等价，故一次项为 $0$，二次项系数相同：
$$
a+1=0,\qquad b-\frac{1}{2}=\frac{3}{2}.
$$
所以
$$
a=-1,\qquad b=2,\qquad ab=-2.
$$

### 第 12 题

**答案：** $x+2y-z=0$

设
$$
z=x+2y+\ln(1+x^2+y^2).
$$
在 $(0,0)$ 处，
$$
z_x=1+\frac{2x}{1+x^2+y^2}=1,\qquad
z_y=2+\frac{2y}{1+x^2+y^2}=2.
$$
故切平面为
$$
z=0+1\cdot x+2\cdot y,
$$
即
$$
x+2y-z=0.
$$

### 第 13 题

**答案：** $0$

这是 $[0,1]$ 上的余弦展开，系数为
$$
a_n=2\int_0^1(1-x)\cos(n\pi x)\,dx.
$$
分部积分或直接计算可得
$$
a_n=\frac{2[1-(-1)^n]}{n^2\pi^2}.
$$
当 $n$ 为偶数时，$a_n=0$。因此
$$
\sum_{n=1}^{\infty}a_{2n}=0.
$$

### 第 14 题

**答案：** $\displaystyle \frac{1}{2}$

由
$$
f(x+2)=f(x)+x
$$
得
$$
\int_1^3f(x)\,dx
=\int_1^2f(x)\,dx+\int_2^3f(x)\,dx.
$$
令 $x=u+2$，则
$$
\int_2^3f(x)\,dx=\int_0^1 f(u+2)\,du
=\int_0^1[f(u)+u]\,du.
$$
所以
$$
\int_1^3f(x)\,dx
=\int_0^2 f(x)\,dx+\int_0^1u\,du
=0+\frac{1}{2}
=\frac{1}{2}.
$$

### 第 15 题

**答案：** $\displaystyle \frac{11}{9}$

由条件
$$
\gamma^T\alpha_i=\beta^T\alpha_i\quad(i=1,2,3)
$$
且 $\gamma=k_1\alpha_1+k_2\alpha_2+k_3\alpha_3$，可得
$$
Gk=b,
$$
其中
$$
G=(\alpha_i^T\alpha_j)=3E,\qquad
b=(\beta^T\alpha_1,\beta^T\alpha_2,\beta^T\alpha_3)^T=(1,-3,-1)^T.
$$
所以
$$
k=\left(\frac{1}{3},-1,-\frac{1}{3}\right)^T.
$$
因此
$$
k_1^2+k_2^2+k_3^2
=\frac{1}{9}+1+\frac{1}{9}
=\frac{11}{9}.
$$

### 第 16 题

**答案：** $\displaystyle \frac{1}{3}$

$X\sim B(1,1/3)$，$Y\sim B(2,1/2)$，且相互独立。因此
$$
P\{X=Y\}=P(X=0,Y=0)+P(X=1,Y=1).
$$
计算得
$$
P(X=0,Y=0)=\frac{2}{3}\cdot\frac{1}{4}=\frac{1}{6},
$$
$$
P(X=1,Y=1)=\frac{1}{3}\cdot\frac{1}{2}=\frac{1}{6}.
$$
故
$$
P\{X=Y\}=\frac{1}{3}.
$$

### 第 17 题

**答案：** (I) $y=x(2-\ln x)$；(II) 最大值为 $\displaystyle \frac{e^4}{4}-\frac{5}{4}$。

切线在 $y$ 轴上的截距为
$$
y-xy'.
$$
点 $P(x,y)$ 到 $y$ 轴的距离为 $x$，故
$$
y-xy'=x.
$$
即
$$
y'-\frac{1}{x}y=-1.
$$
令 $y=xu$，则 $y'=u+xu'$，代入得
$$
xu'=-1.
$$
所以
$$
u=-\ln x+C,
$$
由 $y(1)=2$ 得 $C=2$，故
$$
y=x(2-\ln x).
$$

设
$$
f(x)=\int_1^x t(2-\ln t)\,dt.
$$
则 $f'(x)=x(2-\ln x)$。在 $(0,e^2)$ 上 $f'(x)>0$，在 $(e^2,+\infty)$ 上 $f'(x)<0$，故最大值在 $x=e^2$ 处取得。

原函数为
$$
\int x(2-\ln x)\,dx=\frac{5}{4}x^2-\frac{1}{2}x^2\ln x.
$$
因此最大值为
$$
f(e^2)=\frac{e^4}{4}-\frac{5}{4}.
$$

### 第 18 题

**答案：** 极小值为 $\displaystyle f\left(\frac{2}{3},\frac{10}{27}\right)=-\frac{4}{729}$。

设
$$
f(x,y)=(y-x^2)(y-x^3).
$$
求偏导：
$$
f_y=2y-x^2-x^3,
$$
$$
f_x=-(2x+3x^2)y+5x^4.
$$
由 $f_y=0$ 得
$$
y=\frac{x^2+x^3}{2}.
$$
代入 $f_x=0$，得
$$
x^3(3x-2)(x-1)=0.
$$
驻点为
$$
(0,0),\quad \left(\frac{2}{3},\frac{10}{27}\right),\quad (1,1).
$$
其中 $(0,0)$ 与 $(1,1)$ 不是极值点；在
$$
\left(\frac{2}{3},\frac{10}{27}\right)
$$
处，
$$
y-x^2=-\frac{2}{27},\qquad y-x^3=\frac{2}{27},
$$
故
$$
f\left(\frac{2}{3},\frac{10}{27}\right)
=-\frac{4}{729}.
$$
该点为极小值点，所以极小值为 $-\frac{4}{729}$。

### 第 19 题

**答案：** $\displaystyle I=\frac{5\pi}{4}$

由高斯公式，
$$
I=\iiint_{\Omega}
\left[
\frac{\partial(2xz)}{\partial x}
+\frac{\partial(xz\cos y)}{\partial y}
+\frac{\partial(3yz\sin x)}{\partial z}
\right]dV.
$$
即
$$
I=\iiint_{\Omega}\left(2z-xz\sin y+3y\sin x\right)dV.
$$
区域为
$$
x^2+y^2\le1,\qquad 0\le z\le1-x.
$$
由于关于 $y$ 对称，含 $\sin y$ 或因子 $y$ 的两项积分为 $0$。故
$$
I=\iint_{x^2+y^2\le1}\int_0^{1-x}2z\,dz\,dxdy
=\iint_{x^2+y^2\le1}(1-x)^2\,dxdy.
$$
于是
$$
I=\iint_D(1-2x+x^2)\,dA
=\pi+\frac{\pi}{4}
=\frac{5\pi}{4}.
$$

### 第 20 题

**答案：** 证明见解析。

(I) 构造二次插值余项。设
$$
F(x)=f(x)-\frac{f(a)+f(-a)}{2a^2}x^2.
$$
由 $f(0)=0$，有
$$
F(a)+F(-a)=f(a)+f(-a)-[f(a)+f(-a)]=0.
$$
又 $F$ 在 $[-a,a]$ 上二阶连续，由两次应用中值定理，可知存在 $\xi\in(-a,a)$ 使
$$
F''(\xi)=0.
$$
因此
$$
f''(\xi)=\frac{f(a)+f(-a)}{a^2}.
$$

(II) 若 $f$ 在 $(-a,a)$ 内取得极值，设极值点为 $x_0$，则 $f'(x_0)=0$。由拉格朗日中值定理，
$$
f(a)-f(x_0)=f'(\xi_1)(a-x_0),
$$
$$
f(x_0)-f(-a)=f'(\xi_2)(x_0+a)
$$
对某些 $\xi_1,\xi_2\in(-a,a)$ 成立。再由 $f'(x_0)=0$，对 $f'$ 应用中值定理，可得存在 $\eta\in(-a,a)$，使
$$
|f''(\eta)|\ge
\frac{|f(a)-f(-a)|}{2a^2}.
$$
即结论成立。

### 第 21 题

**答案：** (I) 可取 $\displaystyle P=\begin{pmatrix}1&-1&1\\0&1&0\\0&0&1\end{pmatrix}$；(II) 不存在正交变换。

二次型 $f$ 的矩阵为
$$
A=\begin{pmatrix}
1&1&-1\\
1&2&0\\
-1&0&2
\end{pmatrix},
$$
$g$ 的矩阵为
$$
B=\begin{pmatrix}
1&0&0\\
0&1&1\\
0&1&1
\end{pmatrix}.
$$
取
$$
P=\begin{pmatrix}
1&-1&1\\
0&1&0\\
0&0&1
\end{pmatrix},
$$
直接计算得
$$
P^TAP=B.
$$
因此可逆变换 $x=Py$ 可将 $f$ 化为 $g$。

若存在正交变换 $x=Qy$，则应有
$$
Q^TAQ=B,
$$
这意味着 $A$ 与 $B$ 正交相似，从而特征值相同。但
$$
A
$$
的特征值为 $0,2,3$，而 $B$ 的特征值为 $0,1,2$，二者不同。因此不存在这样的正交变换。

### 第 22 题

**答案：** (I) $\operatorname{Cov}(X,Y)=0$；(II) 不相互独立；(III) $f_Z(z)=2z,\ 0<z<1$，其他为 $0$。

(I) 密度只依赖于 $x^2+y^2$，且区域关于坐标轴对称。因此
$$
EX=EY=0,\qquad E(XY)=0.
$$
故
$$
\operatorname{Cov}(X,Y)=E(XY)-EX\,EY=0.
$$

(II) $X,Y$ 的联合密度支撑集为单位圆盘，不是直积区域；例如当 $X$ 接近 $1$ 时，$Y$ 只能接近 $0$。因此 $X$ 与 $Y$ 不相互独立。

(III) 令
$$
Z=X^2+Y^2=r^2.
$$
在极坐标下
$$
f_{X,Y}(x,y)=\frac{2}{\pi}r^2,
$$
且 $dxdy=r\,dr\,d\theta=\frac{1}{2}\,dz\,d\theta$。于是当 $0<z<1$ 时，
$$
f_Z(z)=\int_0^{2\pi}\frac{2}{\pi}z\cdot\frac{1}{2}\,d\theta=2z.
$$
其他处为 $0$。
