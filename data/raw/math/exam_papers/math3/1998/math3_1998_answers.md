# 1998 年考研数学三答案与解析

## 第 1 题

### 标准答案

$\displaystyle \lim_{n\to\infty}f(\xi_n)=\frac1e$

### 解析

曲线 $y=x^n$ 在点 $(1,1)$ 处的导数为
$$
y'=nx^{n-1},\qquad y'\big|_{x=1}=n.
$$
因而该点切线方程为
$$
y-1=n(x-1).
$$
令 $y=0$，得到与 $x$ 轴交点的横坐标
$$
\xi_n=1-\frac1n.
$$
所以
$$
f(\xi_n)=\left(1-\frac1n\right)^n.
$$
由经典极限
$$
\lim_{n\to\infty}\left(1-\frac1n\right)^n=\frac1e,
$$
得
$$
\lim_{n\to\infty}f(\xi_n)=\frac1e.
$$

## 第 2 题

### 标准答案

$\displaystyle \int \frac{\ln x-1}{x^2}\,dx=-\frac{\ln x}{x}+C$

### 解析

注意到
$$
\frac{d}{dx}\left(-\frac{\ln x}{x}\right)
=-\left(\frac{1}{x}\cdot\frac1x+\ln x\cdot\left(-\frac1{x^2}\right)\right)
=\frac{\ln x-1}{x^2}.
$$
因此原不定积分直接为
$$
\int \frac{\ln x-1}{x^2}\,dx=-\frac{\ln x}{x}+C.
$$

## 第 3 题

### 标准答案

$y_t=C(-5)^t+\frac{5}{12}t-\frac{5}{72}$

### 解析

原方程可写为
$$
y_{t+1}+5y_t=\frac52 t.
$$
先解齐次方程
$$
y_{t+1}+5y_t=0,
$$
其通解为
$$
y_t^{(h)}=C(-5)^t.
$$

对非齐次方程设特解为 $y_t^{(p)}=At+B$，则
$$
A(t+1)+B+5(At+B)=\frac52 t.
$$
比较系数得
$$
6A=\frac52,\qquad A+6B=0.
$$
从而
$$
A=\frac{5}{12},\qquad B=-\frac{5}{72}.
$$
所以通解为
$$
y_t=C(-5)^t+\frac{5}{12}t-\frac{5}{72}.
$$

## 第 4 题

### 标准答案

$\displaystyle B=\begin{pmatrix}2&0&0\\0&-4&0\\0&0&2\end{pmatrix}$

### 解析

已知
$$
A=\operatorname{diag}(1,-2,1),\qquad \det A=-2\ne0,
$$
所以 $A$ 可逆。由伴随矩阵公式
$$
A^*=|A|A^{-1}=(-2)A^{-1}=\operatorname{diag}(-2,1,-2).
$$
原式为
$$
A^*BA=2BA-8E.
$$
两边右乘 $A^{-1}$，得
$$
A^*B=2B-8A^{-1}.
$$
代入对角矩阵并整理可得
$$
(A+E)B=4E.
$$
而
$$
A+E=\operatorname{diag}(2,-1,2),
$$
所以
$$
B=4(A+E)^{-1}=4\operatorname{diag}\left(\frac12,-1,\frac12\right)
=\begin{pmatrix}2&0&0\\0&-4&0\\0&0&2\end{pmatrix}.
$$

## 第 5 题

### 标准答案

$a=\frac1{20},\ b=\frac1{100}$，自由度为 $2$

### 解析

因为 $X_1,X_2,X_3,X_4$ 相互独立，且都服从 $N(0,2^2)$，所以
$$
X_1-2X_2\sim N\bigl(0,4+16\bigr)=N(0,20),
$$
$$
3X_3-4X_4\sim N\bigl(0,9\cdot4+16\cdot4\bigr)=N(0,100).
$$
并且这两个线性组合仍相互独立。

因而
$$
\frac{X_1-2X_2}{\sqrt{20}}\sim N(0,1),
\qquad
\frac{3X_3-4X_4}{10}\sim N(0,1).
$$
要使
$$
X=a(X_1-2X_2)^2+b(3X_3-4X_4)^2
$$
服从卡方分布，只需让它成为两个独立标准正态平方和，即
$$
a=\frac1{20},\qquad b=\frac1{100}.
$$
这时
$$
X=\left(\frac{X_1-2X_2}{\sqrt{20}}\right)^2+\left(\frac{3X_3-4X_4}{10}\right)^2\sim\chi^2(2).
$$
所以自由度为 $2$。

## 第 6 题

### 标准答案

(D)

### 解析

由导数定义，令 $h=-x$，则题设极限可化为
$$
\lim_{x\to0}\frac{f(1)-f(1-x)}{2x}
=\lim_{h\to0}\frac{f(1+h)-f(1)}{2h}
=\frac12 f'(1).
$$
已知该极限等于 $-1$，因此
$$
\frac12 f'(1)=-1\quad\Rightarrow\quad f'(1)=-2.
$$
由于 $f(x)$ 的周期为 $4$，所以导函数 $f'(x)$ 的周期也为 $4$，于是
$$
f'(5)=f'(1+4)=f'(1)=-2.
$$
故切线斜率为 $-2$，选 $(D)$。

## 第 7 题

### 标准答案

(B)

### 解析

先求函数的分段表达式。

当 $|x|<1$ 时，$x^{2n}\to0$，故
$$
f(x)=\lim_{n\to\infty}\frac{1+x}{1+x^{2n}}=1+x.
$$
当 $x=1$ 时，
$$
f(1)=\lim_{n\to\infty}\frac{2}{2}=1.
$$
当 $x=-1$ 时，
$$
f(-1)=\lim_{n\to\infty}\frac{0}{2}=0.
$$
当 $|x|>1$ 时，$x^{2n}\to\infty$，故
$$
f(x)=0.
$$
因而
$$
f(x)=\begin{cases}
1+x,&|x|<1,\\
0,&x=-1\text{ 或 }|x|>1,\\
1,&x=1.
\end{cases}
$$

在 $x=-1$ 处，左右极限都为 $0$，且 $f(-1)=0$，连续；
在 $x=1$ 处，左极限为 $2$，右极限为 $0$，不相等，所以 $x=1$ 是间断点。
故选 $(B)$。

## 第 8 题

### 标准答案

(C)

### 解析

由 $AB=0$ 且 $B\ne0$ 可知齐次方程组 $Ax=0$ 有非零解，因此
$$
\det A=0.
$$
直接计算
$$
A=\begin{pmatrix}
\lambda&1&\lambda^2\\
1&\lambda&1\\
1&1&\lambda
\end{pmatrix},
\qquad
\det A=(\lambda-1)^2.
$$
所以必须有 $\lambda=1$。

当 $\lambda=1$ 时，
$$
A=\begin{pmatrix}1&1&1\\1&1&1\\1&1&1\end{pmatrix},
$$
其秩为 $1$，于是由秩不等式
$$
r(A)+r(B)\le3
$$
得 $r(B)\le2$，所以 $B$ 不可能可逆，从而
$$
|B|=0.
$$
故选 $(C)$。

## 第 9 题

### 标准答案

(B)

### 解析

设 $J$ 为全 $1$ 矩阵，则
$$
A=(1-a)E+aJ.
$$
已知 $J$ 的特征值为 $n$ 和 $0$（后者重数为 $n-1$），因此 $A$ 的特征值为
$$
1+(n-1)a,
\qquad
1-a\ \text{（重数 }n-1\text{）}.
$$
若 $r(A)=n-1$，则恰有一个特征值为 $0$，其余特征值非零。

若 $1-a=0$，则 $a=1$，此时矩阵秩为 $1$，不符合题意。
因此只能是
$$
1+(n-1)a=0,
$$
即
$$
a=\frac{1}{1-n}.
$$
故选 $(B)$。

## 第 10 题

### 标准答案

(A)

### 解析

一个分布函数必须满足
$$
\lim_{x\to+\infty}F(x)=1.
$$
由题设
$$
F(x)=aF_1(x)-bF_2(x),
$$
所以
$$
1=\lim_{x\to+\infty}F(x)=a-b.
$$
在四个选项中，只有 $(A)$ 满足
$$
\frac35-\left(-\frac25\right)=1.
$$
并且此时
$$
F(x)=\frac35F_1(x)+\frac25F_2(x),
$$
是两个分布函数的凸组合，仍是分布函数。
故选 $(A)$。

## 第 11 题

### 标准答案

$\displaystyle dz=e^{-\arctan(y/x)}\bigl[(2x+y)\,dx+(2y-x)\,dy\bigr]$，且 $\displaystyle \frac{\partial^2 z}{\partial x\partial y}=e^{-\arctan(y/x)}\frac{y^2-xy-x^2}{x^2+y^2}$

### 解析

记
$$
\phi=\arctan\frac{y}{x},\qquad z=(x^2+y^2)e^{-\phi}.
$$
则
$$
dz=e^{-\phi}d(x^2+y^2)+(x^2+y^2)d(e^{-\phi}).
$$
由
$$
d\phi=d\left(\arctan\frac{y}{x}\right)=\frac{x\,dy-y\,dx}{x^2+y^2},
$$
得
$$
dz=e^{-\phi}\left(2x\,dx+2y\,dy-(x^2+y^2)\frac{x\,dy-y\,dx}{x^2+y^2}\right)
=e^{-\phi}\bigl[(2x+y)dx+(2y-x)dy\bigr].
$$
因而
$$
z_x=(2x+y)e^{-\phi}.
$$
再对 $y$ 求偏导，注意
$$
\phi_y=\frac{1}{1+(y/x)^2}\cdot\frac1x=\frac{x}{x^2+y^2},
$$
所以
$$
z_{xy}=e^{-\phi}-(2x+y)e^{-\phi}\frac{x}{x^2+y^2}
=e^{-\phi}\frac{y^2-xy-x^2}{x^2+y^2}.
$$

## 第 12 题

### 标准答案

$\displaystyle \iint_D\sqrt{x}\,dx\,dy=\frac{8}{15}$

### 解析

区域
$$
D=\{(x,y)\mid x^2+y^2\le x\}
$$
在极坐标下化为
$$
r^2\le r\cos\theta
\quad\Rightarrow\quad
0\le r\le \cos\theta,
\qquad -\frac\pi2\le\theta\le\frac\pi2.
$$
又因为 $x=r\cos\theta$，故
$$
\sqrt{x}=\sqrt{r\cos\theta}.
$$
于是
$$
\iint_D\sqrt{x}\,dxdy
=\int_{-\pi/2}^{\pi/2}\int_0^{\cos\theta}\sqrt{r\cos\theta}\,r\,dr\,d\theta.
$$
先对 $r$ 积分：
$$
\int_0^{\cos\theta}r^{3/2}\,dr=\frac25(\cos\theta)^{5/2}.
$$
所以原积分为
$$
\frac25\int_{-\pi/2}^{\pi/2}\cos^3\theta\,d\theta
=\frac45\int_0^{\pi/2}\cos^3\theta\,d\theta
=\frac45\cdot\frac23
=\frac{8}{15}.
$$

## 第 13 题

### 标准答案

现值在 $\displaystyle t=\frac1{25r^2}$ 年时最大；当 $r=0.06$ 时，$\displaystyle t=\frac{100}{9}$ 年。

### 解析

若把酒窖藏 $t$ 年后卖出，则总收入现值为
$$
V(t)=R_0e^{\frac25\sqrt{t}}e^{-rt}=R_0e^{\frac25\sqrt{t}-rt}.
$$
由于 $R_0>0$，只需最大化指数部分
$$
\varphi(t)=\frac25\sqrt{t}-rt\qquad (t\ge0).
$$
求导得
$$
\varphi'(t)=\frac{1}{5\sqrt{t}}-r.
$$
令 $\varphi'(t)=0$，得到
$$
\sqrt{t}=\frac{1}{5r},
\qquad
t=\frac1{25r^2}.
$$
且
$$
\varphi''(t)=-\frac{1}{10t^{3/2}}<0,
$$
所以该点取得最大值。

当 $r=0.06=\frac{3}{50}$ 时，
$$
t=\frac1{25\left(\frac{3}{50}\right)^2}=\frac{100}{9}.
$$

## 第 14 题

### 标准答案

结论成立：存在 $\xi,\eta\in(a,b)$，使 $\displaystyle \frac{f'(\xi)}{f'(\eta)}=\frac{e^b-e^a}{b-a}e^{-\eta}$。

### 解析

先对函数 $f$ 在区间 $[a,b]$ 上应用拉格朗日中值定理，可得存在 $\xi\in(a,b)$，使
$$
f'(\xi)=\frac{f(b)-f(a)}{b-a}.
$$

再对函数 $f(x)$ 与 $e^x$ 在 $[a,b]$ 上应用柯西中值定理，可得存在 $\eta\in(a,b)$，使
$$
\frac{f(b)-f(a)}{e^b-e^a}=\frac{f'(\eta)}{e^{\eta}}.
$$
即
$$
f'(\eta)=\frac{f(b)-f(a)}{e^b-e^a}e^{\eta}.
$$

将这两个式子相除，得到
$$
\frac{f'(\xi)}{f'(\eta)}
=\frac{\dfrac{f(b)-f(a)}{b-a}}{\dfrac{f(b)-f(a)}{e^b-e^a}e^{\eta}}
=\frac{e^b-e^a}{b-a}e^{-\eta}.
$$
因而结论成立。

## 第 15 题

### 标准答案

$\displaystyle a_n=\frac1{\sqrt{n(n+1)}},\quad S_n=\frac{4}{3[n(n+1)]^{3/2}},\quad \sum_{n=1}^{\infty}\frac{S_n}{a_n}=\frac43$

### 解析

两条抛物线交点满足
$$
nx^2+\frac1n=(n+1)x^2+\frac1{n+1}.
$$
整理得
$$
x^2=\frac1{n(n+1)}.
$$
因而
$$
a_n=\frac1{\sqrt{n(n+1)}}.
$$

两曲线围成图形的面积为
$$
S_n=\int_{-a_n}^{a_n}\left(nx^2+\frac1n-(n+1)x^2-\frac1{n+1}\right)dx
=\int_{-a_n}^{a_n}(a_n^2-x^2)dx.
$$
计算得
$$
S_n=\frac{4}{3}a_n^3=\frac{4}{3[n(n+1)]^{3/2}}.
$$

于是
$$
\frac{S_n}{a_n}=\frac{4}{3n(n+1)}.
$$
所以
$$
\sum_{n=1}^{\infty}\frac{S_n}{a_n}
=\frac43\sum_{n=1}^{\infty}\frac1{n(n+1)}
=\frac43\sum_{n=1}^{\infty}\left(\frac1n-\frac1{n+1}\right)
=\frac43.
$$

## 第 16 题

### 标准答案

所求微分方程为 $\displaystyle x^2y'+2xy-3y^2=0$，满足 $\displaystyle y\big|_{x=2}=\frac29$ 的解为 $\displaystyle y=\frac{x}{1+x^3}$。

### 解析

由旋转体体积公式，
$$
V(t)=\pi\int_1^t f^2(x)\,dx.
$$
又题设给出
$$
V(t)=\frac\pi3\bigl[t^2f(t)-f(1)\bigr].
$$
两边对 $t$ 求导：
$$
\pi f^2(t)=\frac\pi3\bigl(2tf(t)+t^2f'(t)\bigr).
$$
令 $y=f(t)$，再把自变量记回 $x$，便得
$$
x^2y'+2xy-3y^2=0.
$$

解该微分方程。令 $u=1/y$，则 $y=1/u$，$y'=-u'/u^2$，代入得
$$
-u'+\frac{2}{x}u=\frac{3}{x^2}.
$$
即
$$
u'-\frac{2}{x}u=-\frac{3}{x^2}.
$$
乘以积分因子 $x^{-2}$，有
$$
(ux^{-2})'=-3x^{-4}.
$$
积分得
$$
ux^{-2}=x^{-3}+C,
$$
即
$$
u=\frac1x+Cx^2.
$$
因而
$$
y=\frac1u=\frac{x}{1+Cx^3}.
$$
利用条件 $y(2)=\dfrac29$，得到
$$
\frac{2}{1+8C}=\frac29\quad\Rightarrow\quad C=1.
$$
所以所求解为
$$
y=\frac{x}{1+x^3}.
$$

## 第 17 题

### 标准答案

$A^2=0$；矩阵 $A$ 的全部特征值都是 $0$，其特征向量为一切满足 $\beta^Tx=0$ 的非零向量。

### 解析

由 $A=\alpha\beta^T$ 可得
$$
A^2=\alpha\beta^T\alpha\beta^T=\alpha(\beta^T\alpha)\beta^T.
$$
又由题设 $\alpha^T\beta=0$，而标量转置不变，所以
$$
\beta^T\alpha=0.
$$
因此
$$
A^2=0.
$$

设 $\lambda$ 是 $A$ 的特征值，对应特征向量为 $x\ne0$。由 $A^2=0$ 得
$$
0=A^2x=\lambda^2x.
$$
因为 $x\ne0$，故 $\lambda=0$。所以 $A$ 的全部特征值都是 $0$。

对应的特征向量满足
$$
Ax=0
\iff \alpha\beta^T x=0.
$$
由于 $\alpha\ne0$，故上式等价于
$$
\beta^T x=0.
$$
因而所有满足 $\beta^T x=0$ 的非零向量都是 $A$ 属于特征值 $0$ 的特征向量。

## 第 18 题

### 标准答案

$\displaystyle \Lambda=\operatorname{diag}(k^2,(k+2)^2,(k+2)^2)$，且当且仅当 $k\ne0,-2$ 时，$B$ 为正定矩阵。

### 解析

先求矩阵
$$
A=\begin{pmatrix}
1&0&1\\
0&2&0\\
1&0&1
\end{pmatrix}
$$
的特征值。容易验证
$$
A(1,0,-1)^T=0,
$$
$$
A(1,0,1)^T=2(1,0,1)^T,
\qquad
A(0,1,0)^T=2(0,1,0)^T.
$$
所以 $A$ 的特征值为 $0,2,2$。

因而 $kE+A$ 的特征值为 $k,k+2,k+2$，于是
$$
B=(kE+A)^2
$$
的特征值为
$$
k^2,(k+2)^2,(k+2)^2.
$$
所以 $B$ 与对角矩阵
$$
\Lambda=\operatorname{diag}(k^2,(k+2)^2,(k+2)^2)
$$
相似。

又因为 $B$ 是实对称矩阵，所以它正定当且仅当全部特征值都大于 $0$。于是
$$
k^2>0,\qquad (k+2)^2>0,
$$
即
$$
k\ne0,-2.
$$

## 第 19 题

### 标准答案

$\displaystyle E(\text{利润})=\frac{42500}{3}\text{ 元}$

### 解析

设每周利润为 $L$。当需求量 $Y\le X$ 时，全部由本店库存满足，利润为
$$
L=1000Y.
$$
当需求量 $Y>X$ 时，超出部分从别店调剂，每单位利润变为 $500$ 元，因此
$$
L=1000X+500(Y-X)=500(X+Y).
$$
于是可统一写成
$$
L=500Y+500\min(X,Y).
$$
故
$$
E(L)=500E(Y)+500E\bigl(\min(X,Y)\bigr).
$$
因为 $Y\sim U[10,20]$，所以
$$
E(Y)=15.
$$
再设 $X=10+U_1,\ Y=10+U_2$，其中 $U_1,U_2\sim U[0,10]$ 独立，则
$$
\min(X,Y)=10+\min(U_1,U_2).
$$
对两个独立 $U[0,10]$ 随机变量，有
$$
E\bigl(\min(U_1,U_2)\bigr)=\frac{10}{3},
$$
从而
$$
E\bigl(\min(X,Y)\bigr)=10+\frac{10}{3}=\frac{40}{3}.
$$
最终
$$
E(L)=500\cdot15+500\cdot\frac{40}{3}=\frac{42500}{3}\text{ 元}.
$$

## 第 20 题

### 标准答案

$\displaystyle p=\frac{29}{90},\qquad q=\frac{20}{61}$

### 解析

三个地区被等概率选中，各地区女生表占比分别为
$$
\frac{3}{10},\quad \frac{7}{15},\quad \frac{5}{25}.
$$
因而先抽到女生表的概率为
$$
p=\frac13\left(\frac{3}{10}+\frac{7}{15}+\frac{5}{25}\right)=\frac{29}{90}.
$$

下面求
$$
q=P(\text{先抽到女生表}\mid \text{后抽到男生表}).
$$
记事件 $A$ 为“先抽到女生表”，事件 $B$ 为“后抽到男生表”。

对三个地区分别计算：
$$
P(A\cap B)=\frac13\left(\frac{3}{10}\cdot\frac{7}{9}+\frac{7}{15}\cdot\frac{8}{14}+\frac{5}{25}\cdot\frac{20}{24}\right)=\frac{2}{9}.
$$
又
$$
P(B)=\frac13\left(\frac{7}{10}+\frac{8}{15}+\frac{20}{25}\right)=\frac{61}{90}.
$$
所以由贝叶斯公式
$$
q=P(A\mid B)=\frac{P(A\cap B)}{P(B)}=\frac{\frac29}{\frac{61}{90}}=\frac{20}{61}.
$$
