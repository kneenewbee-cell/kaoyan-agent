# 2021 数学三答案解析

资料类型：考研数学三答案解析
年份：2021
科目：数学三
整理状态：依据答案页和题面人工补写整理。


## 选择题

| 题号 | 答案 |
|---|---|
| 1 | C |
| 2 | D |
| 3 | A |
| 4 | C |
| 5 | B |
| 6 | D |
| 7 | C |
| 8 | D |
| 9 | B |
| 10 | A |

## 填空题

| 题号 | 答案 |
|---|---|
| 11 | $\dfrac{\sin e^{-1}}{2e}$ |
| 12 | $6$ |
| 13 | $\dfrac{\pi}{4}$ |
| 14 | $\dfrac12 t^2-\dfrac12 t+c$ |
| 15 | $-5$ |
| 16 | $\dfrac15$ |

## 解答题

| 题号 | 答案 |
|---|---|
| 17 | $a=\dfrac{e^{-1}-e}{\pi}$ |
| 18 | 极小值点为 $(-1,0)$ 与 $\left(\dfrac12,0\right)$；对应极小值分别为 $f(-1,0)=2,\qquad f\!\left(\frac12,0\right)=\frac12-2\ln2$ |
| 19 | $\dfrac18(e-1)^2$ |
| 20 | $y_n(x)=\frac{x^{n+1}}{n(n+1)}$；收敛域为 $[-1,1]$；和函数为 $S(x)= \begin{cases} x+(1-x)\ln(1-x),& -1\le x<1,\\ 1,& x=1. \end{cases}$ |
| 21 | 两种情形：1. $b=1,\ a=1$，可取 $P= \begin{pmatrix} -1&0&1\\ 1&0&1\\ 0&1&1 \end{pmatrix}, \quad \Lambda=\operatorname{diag}(1,1,3)$；2. $b=3,\ a=-1$，可取 $P= \begin{pmatrix} -1&1&0\\ 1&1&0\\ 1&0&1 \end{pmatrix}, \quad \Lambda=\operatorname{diag}(1,3,3)$ |
| 22 | $f_X(x)= \begin{cases} 1,& 0<x<1,\\ 0,& \text{其他}, \end{cases}$ $f_Z(z)= \begin{cases} \dfrac{2}{(z+1)^2},& z>1,\\ 0,& \text{其他}, \end{cases}$ $E\!\left(\frac{X}{Y}\right)=2\ln2-1$ |

## 详细解析

### 第 1 题

- 标准答案：C

当 $t\to0$ 时，
$$
e^{t^3}-1\sim t^3.
$$
因此
$$
\int_0^{x^2}(e^{t^3}-1)\,dt
\sim \int_0^{x^2} t^3\,dt
=\frac{x^8}{4}.
$$
所以它与 $x^7$ 相比满足
$$
\frac{x^8/4}{x^7}=\frac x4\to0,
$$
故它是 $x^7$ 的高阶无穷小，选 **C**。

### 第 2 题

- 标准答案：D

先看连续性：
$$
\lim_{x\to0}\frac{e^x-1}{x}=1=f(0),
$$
所以连续。

再求导数。由展开
$$
e^x-1=x+\frac{x^2}{2}+o(x^2),
$$
得
$$
\frac{e^x-1}{x}=1+\frac x2+o(x).
$$
因此
$$
f'(0)=\lim_{x\to0}\frac{f(x)-f(0)}x=\frac12\ne0.
$$
故选 **D**。

### 第 3 题

- 标准答案：A

令
$$
f'(x)=a-\frac bx.
$$
若有两个零点，则函数先降后升，故必须有唯一极小值点
$$
x_0=\frac ba>0.
$$

在该点
$$
f(x_0)=a\cdot \frac ba-b\ln\frac ba
=b\left(1-\ln\frac ba\right).
$$
要有两个零点，极小值必须小于 0，即
$$
1-\ln\frac ba<0
\iff \ln\frac ba>1
\iff \frac ba>e.
$$
故选 **A**。

### 第 4 题

- 标准答案：C

由
$$
u=x+1,\quad v=e^x
$$
当 $x=0$ 时对应 $(u,v)=(1,1)$。

设
$$
g(x)=f(x+1,e^x)=x(x+1)^2,
$$
则
$$
g'(0)=f_u(1,1)\cdot1+f_v(1,1)\cdot1=1.
$$

再由
$$
h(x)=f(x,x^2)=2x^2\ln x,
$$
当 $x=1$ 时也对应 $(1,1)$。有
$$
h'(1)=f_u(1,1)+2f_v(1,1)=2.
$$

联立
$$
\begin{cases}
f_u+f_v=1,\\
f_u+2f_v=2,
\end{cases}
$$
解得
$$
f_u(1,1)=0,\qquad f_v(1,1)=1.
$$
所以
$$
df(1,1)=f_u\,dx+f_v\,dy=dy.
$$
故选 **C**。

### 第 5 题

- 标准答案：B

展开得
$$
f=2x_2^2+2x_1x_2+2x_2x_3+2x_1x_3.
$$
对应对称矩阵为
$$
A=
\begin{pmatrix}
0&1&1\\
1&2&1\\
1&1&0
\end{pmatrix}.
$$

计算其特征值可得
$$
\lambda_1=3,\qquad \lambda_2=-1,\qquad \lambda_3=0.
$$
因此正惯性指数为 1，负惯性指数为 1，故选 **B**。

### 第 6 题

- 标准答案：D

因为 $A$ 为正交矩阵，列向量 $\alpha_i$ 构成标准正交基，且
$$
B x=
\begin{pmatrix}
\alpha_1^Tx\\
\alpha_2^Tx\\
\alpha_3^Tx
\end{pmatrix}
=
\begin{pmatrix}
1\\1\\1
\end{pmatrix}.
$$
所以
$$
\alpha_1^Tx=\alpha_2^Tx=\alpha_3^Tx=1.
$$

将 $x$ 在正交基下展开：
$$
x=c_1\alpha_1+c_2\alpha_2+c_3\alpha_3+c_4\alpha_4.
$$
则立刻得到
$$
c_1=c_2=c_3=1,\qquad c_4=k.
$$
故
$$
x=\alpha_1+\alpha_2+\alpha_3+k\alpha_4.
$$
选 **D**。

### 第 7 题

- 标准答案：C

对矩阵 $A$ 做行初等变换与列初等变换，使之化为对角矩阵。对应地，左乘下三角可逆矩阵 $P$，右乘上三角可逆矩阵 $Q$。

按原题给出的四组选项逐一代入检查，可发现只有 **C** 所给的 $P,Q$ 能把 $A$ 化为对角矩阵。

因此选 **C**。

### 第 8 题

- 标准答案：D

A：由全概率公式
$$
P(A)=P(A|B)P(B)+P(A|\bar B)P(\bar B)
$$
可知成立。  

B：由
$$
P(\bar A|B)=1-P(A|B),\qquad P(\bar A)=1-P(A)
$$
可知与题设矛盾方向相反，因此仍成立。  

C：若
$$
P(A|B)>P(A|\bar B),
$$
则
$$
P(A)=P(A|B)P(B)+P(A|\bar B)P(\bar B)
$$
是两者的加权平均，故必有 $P(A|B)>P(A)$。  

D 不一定成立，构造反例即可否定，所以假命题为 **D**。

### 第 9 题

- 标准答案：B

显然
$$
E(\bar X)=\mu_1,\qquad E(\bar Y)=\mu_2,
$$
所以
$$
E(\hat\theta)=E(\bar X-\bar Y)=\mu_1-\mu_2=\theta.
$$

又
$$
D(\bar X)=\frac{\sigma_1^2}{n},\qquad
D(\bar Y)=\frac{\sigma_2^2}{n},\qquad
\operatorname{Cov}(\bar X,\bar Y)=\frac{\rho\sigma_1\sigma_2}{n}.
$$
因此
$$
D(\hat\theta)=D(\bar X-\bar Y)
=\frac{\sigma_1^2+\sigma_2^2-2\rho\sigma_1\sigma_2}{n}.
$$
故选 **B**。

### 第 10 题

- 标准答案：A

样本中取值 1 出现 3 次，取值 2 或 3 共出现 5 次。

似然函数为
$$
L(\theta)=\left(\frac{1-\theta}{2}\right)^3\left(\frac{1+\theta}{4}\right)^5.
$$
取对数：
$$
\ln L(\theta)=3\ln(1-\theta)+5\ln(1+\theta)+C.
$$
求导并令其为零：
$$
\frac{-3}{1-\theta}+\frac{5}{1+\theta}=0.
$$
解得
$$
5(1-\theta)=3(1+\theta)\iff 2=8\theta\iff \theta=\frac14.
$$
故选 **A**。

### 第 11 题

- 标准答案：$\dfrac{\sin e^{-1}}{2e}$

设
$$
u=e^{-\sqrt x},
$$
则
$$
y=\cos u,\qquad \frac{dy}{dx}=-\sin u\cdot \frac{du}{dx}.
$$
又
$$
\frac{du}{dx}=e^{-\sqrt x}\cdot\left(-\frac1{2\sqrt x}\right).
$$
所以
$$
\frac{dy}{dx}=\sin(e^{-\sqrt x})\frac{e^{-\sqrt x}}{2\sqrt x}.
$$
代入 $x=1$ 得
$$
\left.\frac{dy}{dx}\right|_{x=1}=\frac{\sin e^{-1}}{2e}.
$$

### 第 12 题

- 标准答案：$6$

因为积分区间分成 $(\sqrt5,3)$ 与 $(3,5)$ 两段，分别有
$$
|x^2-9|=
\begin{cases}
9-x^2,& \sqrt5\le x<3,\\
x^2-9,& 3<x\le5.
\end{cases}
$$

因此
$$
\int_{\sqrt5}^{5}\frac{x}{\sqrt{|x^2-9|}}\,dx
=\int_{\sqrt5}^{3}\frac{x}{\sqrt{9-x^2}}\,dx+\int_{3}^{5}\frac{x}{\sqrt{x^2-9}}\,dx.
$$
两项都用换元 $u=9-x^2$ 或 $u=x^2-9$ 即可，分别得到 2 与 4，总和为
$$
6.
$$

### 第 13 题

- 标准答案：$\dfrac{\pi}{4}$

旋转体体积公式：
$$
V=\pi\int_0^1 y^2\,dx.
$$
代入
$$
y=\sqrt x\sin\pi x
$$
得
$$
V=\pi\int_0^1 x\sin^2(\pi x)\,dx.
$$
利用
$$
\sin^2(\pi x)=\frac{1-\cos 2\pi x}{2},
$$
可算得
$$
\int_0^1 x\sin^2(\pi x)\,dx=\frac14.
$$
故
$$
V=\frac{\pi}{4}.
$$

### 第 14 题

- 标准答案：$\dfrac12 t^2-\dfrac12 t+c$

由
$$
\Delta y_t=y_{t+1}-y_t=t.
$$
设通解为二次多项式
$$
y_t=At^2+Bt+C.
$$
则
$$
y_{t+1}-y_t=A[(t+1)^2-t^2]+B[(t+1)-t]=2At+A+B.
$$
与 $t$ 对比系数得
$$
2A=1,\qquad A+B=0.
$$
故
$$
A=\frac12,\qquad B=-\frac12.
$$
所以通解为
$$
y_t=\frac12 t^2-\frac12 t+c.
$$

### 第 15 题

- 标准答案：$-5$

行列式按关于 $x$ 的多项式展开。$x^3$ 项来自从四行四列中恰好取三个含 $x$ 的元素、另一个取常数项的情形。

直接按行列式多线性展开，或借助按列分拆后收集三次项，可得该系数为
$$
-5.
$$

### 第 16 题

- 标准答案：$\dfrac15$

$X$ 只取 0 或 1，且
$$
P(X=1)=P(X=0)=\frac12.
$$

若 $X=1$，则乙盆变成 3 红 2 白，所以
$$
P(Y=1\mid X=1)=\frac35;
$$
若 $X=0$，则乙盆变成 2 红 3 白，所以
$$
P(Y=1\mid X=0)=\frac25.
$$

由此算得
$$
E(X)=E(Y)=\frac12,\qquad E(XY)=\frac12\cdot\frac35=\frac3{10}.
$$
所以
$$
\operatorname{Cov}(X,Y)=E(XY)-E(X)E(Y)=\frac3{10}-\frac14=\frac1{20}.
$$

又
$$
D(X)=D(Y)=\frac14,
$$
故
$$
\rho_{XY}=\frac{1/20}{\sqrt{(1/4)(1/4)}}=\frac15.
$$

### 第 17 题

- 标准答案：$a=\dfrac{e^{-1}-e}{\pi}$

分别考察左右极限。

当 $x\to0^+$ 时，
$$
\arctan\frac1x\to\frac\pi2,\qquad (1+x)^{1/x}\to e,
$$
所以
$$
\lim_{x\to0^+}\left[a\arctan\frac1x+(1+|x|)^{1/x}\right]=\frac\pi2 a+e.
$$

当 $x\to0^-$ 时，
$$
\arctan\frac1x\to-\frac\pi2,\qquad (1-|x|)^{1/x}=(1-x)^{-1/x}\to e^{-1},
$$
所以
$$
\lim_{x\to0^-}\left[a\arctan\frac1x+(1+|x|)^{1/x}\right]=-\frac\pi2 a+e^{-1}.
$$

极限存在需左右极限相等：
$$
\frac\pi2 a+e=-\frac\pi2 a+e^{-1}.
$$
解得
$$
a=\frac{e^{-1}-e}{\pi}.
$$

### 第 18 题

- 标准答案：极小值点为 $(-1,0)$ 与 $\left(\dfrac12,0\right)$；

对应极小值分别为
$$
f(-1,0)=2,\qquad f\!\left(\frac12,0\right)=\frac12-2\ln2.
$$

先求一阶偏导：
$$
f_x(x,y)=\frac{2x^2+x-1-y^2}{x^3},\qquad
f_y(x,y)=\frac{y}{x^2}.
$$
令其为 0，得
$$
y=0,\qquad 2x^2+x-1=0.
$$
解得驻点
$$
(-1,0),\qquad \left(\frac12,0\right).
$$

再求二阶偏导：
$$
f_{xx}=\frac{-2x^2-2x+3+3y^2}{x^4},\qquad
f_{xy}=-\frac{2y}{x^3},\qquad
f_{yy}=\frac1{x^2}.
$$

在 $(-1,0)$ 处，
$$
A=f_{xx}=3,\quad B=f_{xy}=0,\quad C=f_{yy}=1,
$$
有
$$
A>0,\quad AC-B^2>0,
$$
故为极小值点，且
$$
f(-1,0)=2.
$$

在 $\left(\frac12,0\right)$ 处，
$$
A=24,\quad B=0,\quad C=4,
$$
同样满足
$$
A>0,\quad AC-B^2>0,
$$
故也为极小值点，且
$$
f\!\left(\frac12,0\right)=\frac12-2\ln2.
$$

### 第 19 题

- 标准答案：$\dfrac18(e-1)^2$

区域 $D$ 在极坐标下为
$$
0\le r\le1,\qquad 0\le \theta\le\frac\pi4.
$$

又
$$
x=r\cos\theta,\qquad y=r\sin\theta,
$$
所以
$$
(x+y)^2=r^2(\cos\theta+\sin\theta)^2=r^2(1+\sin2\theta),
$$
且
$$
x^2-y^2=r^2(\cos^2\theta-\sin^2\theta)=r^2\cos2\theta.
$$

因此原积分化为
$$
\int_0^{\pi/4}\int_0^1 e^{r^2(1+\sin2\theta)}r^3\cos2\theta\,dr\,d\theta.
$$
交换积分次序并对 $\theta$ 积分，可得
$$
\int_0^1 \frac r2\int_0^{\pi/4} e^{r^2(1+\sin2\theta)}\,d(\sin2\theta)\,dr
=\frac12\int_0^1 r(e^{2r^2}-e^{r^2})\,dr.
$$

再积分得
$$
\frac12\left[\frac14e^{2r^2}-\frac12e^{r^2}\right]_0^1
=\frac18(e-1)^2.
$$

### 第 20 题

- 标准答案：$$
y_n(x)=\frac{x^{n+1}}{n(n+1)};
$$

收敛域为 $[-1,1]$；

和函数为
$$
S(x)=
\begin{cases}
x+(1-x)\ln(1-x),& -1\le x<1,\\
1,& x=1.
\end{cases}
$$

1. 由方程
$$
xy'-(n+1)y=0
$$
得
$$
\frac{y'}y=\frac{n+1}{x}.
$$
积分得
$$
\ln|y|=(n+1)\ln|x|+C,
$$
即
$$
y=Cx^{n+1}.
$$
利用条件
$$
y_n(1)=\frac1{n(n+1)}
$$
得
$$
C=\frac1{n(n+1)}.
$$
所以
$$
y_n(x)=\frac{x^{n+1}}{n(n+1)}.
$$

2. 于是
$$
\sum_{n=1}^{\infty}y_n(x)=\sum_{n=1}^{\infty}\frac{x^{n+1}}{n(n+1)}.
$$
比值法知收敛半径为 1。端点上：
$$
x=1:\ \sum\frac1{n(n+1)} \text{ 收敛},\qquad
x=-1:\ \sum\frac{(-1)^{n+1}}{n(n+1)} \text{ 收敛}.
$$
故收敛域为
$$
[-1,1].
$$

设和函数为 $S(x)$，则
$$
S(x)=\sum_{n=1}^{\infty}\left(\frac1n-\frac1{n+1}\right)x^{n+1}
=x\sum_{n=1}^{\infty}\frac{x^n}{n}-\sum_{n=1}^{\infty}\frac{x^{n+1}}{n+1}.
$$
利用
$$
\sum_{n=1}^{\infty}\frac{x^n}{n}=-\ln(1-x)\qquad (|x|<1),
$$
化简得
$$
S(x)=x+(1-x)\ln(1-x)\qquad (-1\le x<1).
$$
再由
$$
S(1)=\sum_{n=1}^{\infty}\frac1{n(n+1)}=1,
$$
得到
$$
S(x)=
\begin{cases}
x+(1-x)\ln(1-x),& -1\le x<1,\\
1,& x=1.
\end{cases}
$$

### 第 21 题

- 标准答案：两种情形：

1. $b=1,\ a=1$，可取
$$
P=
\begin{pmatrix}
-1&0&1\\
1&0&1\\
0&1&1
\end{pmatrix},
\quad
\Lambda=\operatorname{diag}(1,1,3).
$$

2. $b=3,\ a=-1$，可取
$$
P=
\begin{pmatrix}
-1&1&0\\
1&1&0\\
1&0&1
\end{pmatrix},
\quad
\Lambda=\operatorname{diag}(1,3,3).
$$

特征多项式可化为
$$
|A-\lambda E|=(b-\lambda)(\lambda-1)(\lambda-3).
$$
由于仅有两个不同特征值，所以
$$
b=1\quad \text{或}\quad b=3.
$$

若 $b=1$，则特征值为 $1,1,3$。又因 $A$ 相似于对角矩阵，故对重根 $\lambda=1$ 必有
$$
r(A-E)=1,
$$
从而求得
$$
a=1.
$$
解特征向量方程得可取
$$
\alpha_1=(-1,1,0)^T,\quad
\alpha_2=(0,0,1)^T,\quad
\alpha_3=(1,1,1)^T.
$$
取
$$
P=(\alpha_1,\alpha_2,\alpha_3),
$$
则
$$
P^{-1}AP=\operatorname{diag}(1,1,3).
$$

若 $b=3$，则特征值为 $1,3,3$。同理由可对角化知
$$
r(A-3E)=1,
$$
从而得
$$
a=-1.
$$
此时可取
$$
\beta_1=(-1,1,1)^T,\quad
\beta_2=(1,1,0)^T,\quad
\beta_3=(0,0,1)^T,
$$
令
$$
P=(\beta_1,\beta_2,\beta_3),
$$
则
$$
P^{-1}AP=\operatorname{diag}(1,3,3).
$$

### 第 22 题

- 标准答案：$$
f_X(x)=
\begin{cases}
1,& 0<x<1,\\
0,& \text{其他},
\end{cases}
$$

$$
f_Z(z)=
\begin{cases}
\dfrac{2}{(z+1)^2},& z>1,\\
0,& \text{其他},
\end{cases}
$$

$$
E\!\left(\frac{X}{Y}\right)=2\ln2-1.
$$

设随机点坐标为 $T$，则 $T$ 在 $(0,2)$ 上服从均匀分布。

由定义，
$$
X=\min\{T,2-T\},\qquad Y=\max\{T,2-T\},
$$
并且
$$
X+Y=2,\qquad 0<X<1,\qquad Y>X.
$$

1. 对 $0<x<1$，
更直接地看，$X$ 在 $(0,1)$ 上均匀分布，所以
$$
f_X(x)=1,\qquad 0<x<1.
$$

2. 由
$$
Z=\frac{Y}{X}=\frac{2-X}{X}=\frac2X-1.
$$
故 $z>1$，且
$$
X=\frac2{z+1}.
$$
于是
$$
F_Z(z)=P(Z\le z)=P\!\left(\frac{2-X}{X}\le z\right)
=P\!\left(X\ge \frac2{z+1}\right)
=1-\frac2{z+1}\qquad (z\ge1).
$$
求导得
$$
f_Z(z)=\frac{2}{(z+1)^2},\qquad z>1.
$$

3. 因为
$$
\frac{X}{Y}=\frac{X}{2-X},
$$
又 $X\sim U(0,1)$，所以
$$
E\!\left(\frac{X}{Y}\right)
=\int_0^1 \frac{x}{2-x}\,dx
=\int_0^1\left(\frac{2}{2-x}-1\right)dx
=2\ln2-1.
$$
