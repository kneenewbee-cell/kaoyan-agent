# 2017 年考研数学三答案解析

资料类型：考研数学三答案解析
年份：2017
科目：数学三
整理状态：按答案页图人工校对并整理为正式题卡。

## 选择题

| 题号 | 答案 |
|---|---|
| 1 | A |
| 2 | D |
| 3 | C |
| 4 | C |
| 5 | A |
| 6 | B |
| 7 | C |
| 8 | B |

## 填空题

| 题号 | 答案 |
|---|---|
| 9 | $\dfrac{\pi^3}{2}$ |
| 10 | $A2^t+t2^{t-1}$ |
| 11 | $1+(1-Q)e^{-Q}$ |
| 12 | $xye^y$ |
| 13 | $2$ |
| 14 | $\dfrac92$ |

## 解答题

| 题号 | 答案 |
|---|---|
| 15 | $\dfrac23$ |
| 16 | $\dfrac{2-\sqrt2}{16}\pi$ |
| 17 | $\dfrac14$ |
| 18 | $\left(\dfrac1{\ln2}-1,\dfrac12\right)$ |
| 19 | 1. 收敛半径 $R\ge1$；2. $S(x)=\frac{e^{-x}}{1-x}\quad (\lvert x\rvert<1)$ |
| 20 | 1. $r(A)=2$；2. $x=\begin{pmatrix}1\\1\\1\end{pmatrix} +k\begin{pmatrix}1\\2\\-1\end{pmatrix}, \quad k\in\mathbb R$ |
| 21 | $a=2$；可取 $Q= \begin{pmatrix} \dfrac1{\sqrt3} & -\dfrac1{\sqrt2} & \dfrac1{\sqrt6}\\[6pt] -\dfrac1{\sqrt3} & 0 & \dfrac2{\sqrt6}\\[6pt] \dfrac1{\sqrt3} & \dfrac1{\sqrt2} & \dfrac1{\sqrt6} \end{pmatrix}$ |
| 22 | $P\{Y\le E(Y)\}=\frac49$ $f_Z(z)= \begin{cases} z, & 0<z<1,\\ z-2, & 2<z<3,\\ 0, & \text{其他}. \end{cases}$ |
| 23 | 1. $f_{Z_1}(z)= \begin{cases} \dfrac{2}{\sqrt{2\pi}\sigma}e^{-z^2/(2\sigma^2)}, & z\ge0,\\ 0, & z<0; \end{cases}$；2. $\hat\sigma_{\text{矩}}=\frac{\sqrt{2\pi}}{2}\,\overline Z$；3. $\hat\sigma_{\text{MLE}}=\sqrt{\frac1n\sum_{i=1}^n Z_i^2}$ |

## 详细解析

### 第 1 题

- 标准答案：A

由连续性知
$$
\lim_{x\to0^+}f(x)=b.
$$
而
$$
\lim_{x\to0^+}\frac{1-\cos\sqrt{x}}{ax}
=\lim_{x\to0^+}\frac{x/2}{ax}
=\frac1{2a}.
$$
故
$$
b=\frac1{2a},
$$
从而
$$
ab=\frac12.
$$
故选 A。

### 第 2 题

- 标准答案：D

计算偏导数
$$
z_x=3y-2xy-y^2,\qquad z_y=3x-2xy-x^2.
$$
联立 $z_x=z_y=0$ 得驻点
$$
(0,0),\ (1,1),\ (0,3),\ (3,0).
$$

再算二阶偏导
$$
z_{xx}=-2y,\qquad z_{yy}=-2x,\qquad z_{xy}=3-2x-2y.
$$
在 $(1,1)$ 处，
$$
z_{xx}z_{yy}-z_{xy}^2=(-2)(-2)-(-1)^2=3>0,
$$
且 $z_{xx}<0$，故 $(1,1)$ 是极大值点。

其余三点对应判别式小于零，不是极值点。故选 D。

### 第 3 题

- 标准答案：C

由
$$
f(x)f'(x)>0
$$
可得
$$
[f^2(x)]'=2f(x)f'(x)>0.
$$
因此 $f^2(x)$ 严格单调增加，从而
$$
f^2(1)>f^2(-1),
$$
即
$$
|f(1)|>|f(-1)|.
$$
故选 C。

### 第 4 题

- 标准答案：C

当 $n\to\infty$ 时，
$$
\sin\frac1n=\frac1n+o\!\left(\frac1n\right),
$$
且
$$
\ln\left(1-\frac1n\right)=-\frac1n-\frac1{2n^2}+o\!\left(\frac1{n^2}\right).
$$
于是通项
$$
\sin\frac1n-k\ln\left(1-\frac1n\right)
=\frac{1+k}{n}+o\!\left(\frac1n\right).
$$
要使级数收敛，必须有 $1+k=0$，故
$$
k=-1.
$$
故选 C。

### 第 5 题

- 标准答案：A

因为 $\alpha$ 是单位列向量，所以
$$
\alpha^T\alpha=1.
$$
矩阵 $\alpha\alpha^T$ 为秩一矩阵，其特征值为 $1,0,\ldots,0$。
因此
$$
E-\alpha\alpha^T
$$
的特征值为
$$
0,1,\ldots,1,
$$
故其不可逆。选 A。

### 第 6 题

- 标准答案：B

三个矩阵的特征值都为 $1,2,2$。要判断是否与对角矩阵 $C$ 相似，只需看特征值 $2$ 的线性无关特征向量个数。

对 $A$，
$$
3-r(2E-A)=3-1=2,
$$
故特征值 $2$ 有两个线性无关特征向量，可以对角化，所以 $A$ 与 $C$ 相似。

对 $B$，
$$
3-r(2E-B)=3-2=1,
$$
故特征值 $2$ 只有一个线性无关特征向量，不能对角化，因此 $B$ 与 $C$ 不相似。

故选 B。

### 第 7 题

- 标准答案：C

由 $A$ 与 $C$ 独立、$B$ 与 $C$ 独立，有
$$
P(AC)=P(A)P(C),\qquad P(BC)=P(B)P(C).
$$
又
$$
P[(A\cup B)C]=P(AC\cup BC)=P(AC)+P(BC)-P(ABC).
$$
而
$$
P(A\cup B)P(C)=[P(A)+P(B)-P(AB)]P(C).
$$
比较二者可知
$$
A\cup B \text{ 与 } C \text{ 独立}
\iff P(ABC)=P(AB)P(C),
$$
即
$$
AB \text{ 与 } C \text{ 独立}.
$$
故选 C。

### 第 8 题

- 标准答案：B

因为 $X_i\sim N(\mu,1)$，所以
$$
X_i-\mu\sim N(0,1),
$$
故 A 正确。

又
$$
\sum_{i=1}^n(X_i-\overline X)^2\sim\chi^2(n-1),
$$
因此 C 正确。

且
$$
\overline X\sim N\!\left(\mu,\frac1n\right),
$$
所以
$$
n(\overline X-\mu)^2\sim\chi^2(1),
$$
D 正确。

对于 B，$X_n-X_1\sim N(0,2)$，故
$$
\frac{(X_n-X_1)^2}{2}\sim\chi^2(1),
$$
而不是 $2(X_n-X_1)^2$。故选 B。

### 第 9 题

- 标准答案：$\dfrac{\pi^3}{2}$

因为 $\sin^3x$ 是奇函数，所以
$$
\int_{-\pi}^{\pi}\sin^3x\,dx=0.
$$
而 $\sqrt{\pi^2-x^2}$ 是偶函数，
$$
\int_{-\pi}^{\pi}\sqrt{\pi^2-x^2}\,dx
=2\int_0^\pi \sqrt{\pi^2-x^2}\,dx.
$$
后者表示半径为 $\pi$ 的四分之一圆面积，因此
$$
\int_0^\pi \sqrt{\pi^2-x^2}\,dx=\frac14\pi^3.
$$
故原积分为
$$
2\cdot\frac14\pi^3=\frac{\pi^3}{2}.
$$

### 第 10 题

- 标准答案：$A2^t+t2^{t-1}$

对应齐次方程
$$
y_{t+1}-2y_t=0
$$
的通解为
$$
Y_t=A2^t.
$$
设特解为 $y_t^*=kt2^t$，代入原方程得
$$
k(t+1)2^{t+1}-2kt2^t=2^t,
$$
解得
$$
k=\frac12.
$$
因此特解为
$$
y_t^*=t2^{t-1}.
$$
故通解
$$
y_t=A2^t+t2^{t-1}.
$$

### 第 11 题

- 标准答案：$1+(1-Q)e^{-Q}$

总成本为
$$
C(Q)=Q\overline C(Q)=Q+Qe^{-Q}.
$$
故边际成本
$$
C'(Q)=1+e^{-Q}-Qe^{-Q}=1+(1-Q)e^{-Q}.
$$

### 第 12 题

- 标准答案：$xye^y$

由全微分可知
$$
f_x'(x,y)=ye^y,\qquad f_y'(x,y)=x(1+y)e^y.
$$
对 $x$ 积分，
$$
f(x,y)=\int ye^y\,dx=xye^y+C(y).
$$
再对 $y$ 求偏导，
$$
f_y'(x,y)=x(1+y)e^y+C'(y).
$$
与已知比较得
$$
C'(y)=0,
$$
故 $C(y)=C$ 为常数。由 $f(0,0)=0$ 得 $C=0$，于是
$$
f(x,y)=xye^y.
$$

### 第 13 题

- 标准答案：$2$

因为
$$
(A\alpha_1,A\alpha_2,A\alpha_3)=A(\alpha_1,\alpha_2,\alpha_3),
$$
且 $(\alpha_1,\alpha_2,\alpha_3)$ 可逆，所以
$$
r(A\alpha_1,A\alpha_2,A\alpha_3)=r(A).
$$
计算可得
$$
r(A)=2.
$$
因此所求秩为 $2$。

### 第 14 题

- 标准答案：$\dfrac92$

由概率和为 $1$，
$$
\frac12+a+b=1.
$$
又由
$$
E(X)=-2\cdot\frac12+a+3b=0,
$$
解得
$$
a=b=\frac14.
$$
于是
$$
E(X^2)=(-2)^2\cdot\frac12+1^2\cdot\frac14+3^2\cdot\frac14=\frac92.
$$
由于 $E(X)=0$，
$$
D(X)=E(X^2)-[E(X)]^2=\frac92.
$$

### 第 15 题

- 标准答案：$\dfrac23$

令
$$
u=x-t,
$$
则 $t=x-u,\ dt=-du$，原式分子化为
$$
\int_0^x \sqrt{u}\,e^{x-u}\,du
=e^x\int_0^x \sqrt{u}e^{-u}\,du.
$$
因此原极限等于
$$
\lim_{x\to0^+}\frac{\int_0^x \sqrt{u}e^{-u}\,du}{x^{3/2}}.
$$
这是 $0/0$ 型，应用洛必达法则：
$$
\lim_{x\to0^+}\frac{\sqrt{x}e^{-x}}{\frac32\sqrt{x}}
=\frac23.
$$

### 第 16 题

- 标准答案：$\dfrac{2-\sqrt2}{16}\pi$

区域 $D$ 可表示为
$$
0\le x<+\infty,\qquad 0\le y\le \sqrt{x}.
$$
故
$$
\iint_D \frac{y^3}{(1+x^2+y^4)^2}\,dx\,dy
=\int_0^{+\infty}\!\!dx\int_0^{\sqrt{x}} \frac{y^3}{(1+x^2+y^4)^2}\,dy.
$$
对内层积分令
$$
v=1+x^2+y^4,\qquad dv=4y^3\,dy,
$$
得
$$
\int_0^{\sqrt{x}} \frac{y^3}{(1+x^2+y^4)^2}\,dy
=\frac14\left(\frac1{1+x^2}-\frac1{1+2x^2}\right).
$$
故原式为
$$
\frac14\int_0^{+\infty}\left(\frac1{1+x^2}-\frac1{1+2x^2}\right)\,dx
=\frac14\left(\frac\pi2-\frac{\sqrt2}{2}\cdot\frac\pi2\right)
=\frac{2-\sqrt2}{16}\pi.
$$

### 第 17 题

- 标准答案：$\dfrac14$

将和式写成
$$
\sum_{k=1}^n \frac{k}{n}\ln\left(1+\frac{k}{n}\right)\cdot\frac1n.
$$
它是函数
$$
f(x)=x\ln(1+x)
$$
在 $[0,1]$ 上的黎曼和，因此极限为
$$
\int_0^1 x\ln(1+x)\,dx.
$$
分部积分得
$$
\int_0^1 x\ln(1+x)\,dx
=\frac12x^2\ln(1+x)\Big|_0^1-\frac12\int_0^1 \frac{x^2}{1+x}\,dx.
$$
再将
$$
\frac{x^2}{1+x}=x-1+\frac1{1+x}
$$
代入并计算，得
$$
\int_0^1 x\ln(1+x)\,dx=\frac14.
$$
故极限为 $\dfrac14$。

### 第 18 题

- 标准答案：$\left(\dfrac1{\ln2}-1,\dfrac12\right)$

设
$$
f(x)=\frac1{\ln(1+x)}-\frac1x-k,\qquad x\in(0,1).
$$
先研究
$$
g(x)=(1+x)\ln^2(1+x)-x^2.
$$
由计算可得
$$
f'(x)=\frac{(1+x)\ln^2(1+x)-x^2}{x^2(1+x)\ln^2(1+x)}
=\frac{g(x)}{x^2(1+x)\ln^2(1+x)}.
$$
进一步有
$$
g''(x)=\frac{2[\ln(1+x)-x]}{1+x}<0\qquad (0<x\le1),
$$
故 $g'(x)<g'(0)=0$，从而 $g(x)<g(0)=0$，于是 $f'(x)<0$，即 $f$ 在 $(0,1)$ 上严格递减。

又
$$
\lim_{x\to0^+}f(x)=\frac12-k,\qquad
f(1)=\frac1{\ln2}-1-k.
$$
因为 $f$ 单调递减，方程在 $(0,1)$ 内有实根当且仅当
$$
\frac12-k>0,\qquad \frac1{\ln2}-1-k<0.
$$
故
$$
k\in\left(\frac1{\ln2}-1,\frac12\right).
$$

### 第 19 题

- 标准答案：1. 收敛半径 $R\ge1$；  
2.
$$
S(x)=\frac{e^{-x}}{1-x}\quad (|x|<1).
$$

由递推式及初值可归纳得
$$
0\le a_n\le1\qquad (n\ge0).
$$
因此当 $|x|<1$ 时，
$$
|a_nx^n|\le |x|^n,
$$
而几何级数 $\sum |x|^n$ 收敛，所以原幂级数绝对收敛，故收敛半径满足 $R\ge1$。

由
$$
S(x)=\sum_{n=0}^{\infty}a_nx^n
$$
可得
$$
S'(x)=\sum_{n=1}^{\infty}na_nx^{n-1}
=\sum_{n=0}^{\infty}(n+1)a_{n+1}x^n.
$$
于是
$$
(1-x)S'(x)-xS(x)
=a_1+\sum_{n=1}^{\infty}\bigl[(n+1)a_{n+1}-na_n-a_{n-1}\bigr]x^n
=0,
$$
因为递推式恰好使每一项系数为零。

所以
$$
(1-x)S'(x)-xS(x)=0,
$$
解该微分方程得
$$
\frac{S'(x)}{S(x)}=\frac{x}{1-x},
$$
从而
$$
S(x)=\frac{Ce^{-x}}{1-x}.
$$
再由 $S(0)=a_0=1$ 得 $C=1$，故
$$
S(x)=\frac{e^{-x}}{1-x}.
$$

### 第 20 题

- 标准答案：1. $r(A)=2$；  
2.
$$
x=\begin{pmatrix}1\\1\\1\end{pmatrix}
+k\begin{pmatrix}1\\2\\-1\end{pmatrix},
\quad k\in\mathbb R.
$$

由 $\alpha_3=\alpha_1+2\alpha_2$ 知列向量线性相关，所以
$$
r(A)\le2.
$$
又因为 $A$ 有三个不同特征值，所以至少有两个非零特征值，从而
$$
r(A)\ge2.
$$
故
$$
r(A)=2.
$$

由关系
$$
\alpha_1+2\alpha_2-\alpha_3=0
$$
知
$$
A\begin{pmatrix}1\\2\\-1\end{pmatrix}=0,
$$
所以 $\begin{pmatrix}1\\2\\-1\end{pmatrix}$ 是齐次方程 $Ax=0$ 的基础解系。

又
$$
\beta=\alpha_1+\alpha_2+\alpha_3
=A\begin{pmatrix}1\\1\\1\end{pmatrix},
$$
故
$$
\begin{pmatrix}1\\1\\1\end{pmatrix}
$$
是非齐次方程 $Ax=\beta$ 的一个特解。

因此通解为
$$
x=\begin{pmatrix}1\\1\\1\end{pmatrix}
+k\begin{pmatrix}1\\2\\-1\end{pmatrix},\quad k\in\mathbb R.
$$

### 第 21 题

- 标准答案：$$
a=2,
$$
可取
$$
Q=
\begin{pmatrix}
\dfrac1{\sqrt3} & -\dfrac1{\sqrt2} & \dfrac1{\sqrt6}\\[6pt]
-\dfrac1{\sqrt3} & 0 & \dfrac2{\sqrt6}\\[6pt]
\dfrac1{\sqrt3} & \dfrac1{\sqrt2} & \dfrac1{\sqrt6}
\end{pmatrix}.
$$

二次型对应的对称矩阵为
$$
A=
\begin{pmatrix}
2&1&-4\\
1&-1&1\\
-4&1&a
\end{pmatrix}.
$$
题设标准形只有两个平方项，故有一个特征值为 $0$，即
$$
|A|=0.
$$
计算得
$$
|A|=6-3a,
$$
因此
$$
a=2.
$$

此时特征多项式可分解为
$$
|\lambda E-A|=\lambda(\lambda+3)(\lambda-6),
$$
故特征值为 $-3,6,0$。

对应单位特征向量可取
$$
\beta_1=\frac1{\sqrt3}(1,-1,1)^T,\quad
\beta_2=\frac1{\sqrt2}(-1,0,1)^T,\quad
\beta_3=\frac1{\sqrt6}(1,2,1)^T.
$$
于是取
$$
Q=(\beta_1,\beta_2,\beta_3)
$$
即可得到所求正交变换。

### 第 22 题

- 标准答案：$$
P\{Y\le E(Y)\}=\frac49.
$$

$$
f_Z(z)=
\begin{cases}
z, & 0<z<1,\\
z-2, & 2<z<3,\\
0, & \text{其他}.
\end{cases}
$$

先求
$$
E(Y)=\int_0^1 y\cdot 2y\,dy=\frac23.
$$
因此
$$
P\{Y\le E(Y)\}=P\left\{Y\le\frac23\right\}
=\int_0^{2/3}2y\,dy=\frac49.
$$

设 $F_Z(z)=P(Z\le z)$，则由全概率公式
$$
F_Z(z)=\frac12P(Y\le z)+\frac12P(Y\le z-2).
$$
分段计算：

当 $z<0$ 时，$F_Z(z)=0$；

当 $0\le z<1$ 时，
$$
F_Z(z)=\frac12\int_0^z 2y\,dy=\frac{z^2}{2};
$$

当 $1\le z<2$ 时，$F_Z(z)=\dfrac12$；

当 $2\le z<3$ 时，
$$
F_Z(z)=\frac12+\frac12\int_0^{z-2}2y\,dy
=\frac12+\frac{(z-2)^2}{2};
$$

当 $z\ge3$ 时，$F_Z(z)=1$。

对各段求导，得
$$
f_Z(z)=
\begin{cases}
z, & 0<z<1,\\
z-2, & 2<z<3,\\
0, & \text{其他}.
\end{cases}
$$

### 第 23 题

- 标准答案：1.
$$
f_{Z_1}(z)=
\begin{cases}
\dfrac{2}{\sqrt{2\pi}\sigma}e^{-z^2/(2\sigma^2)}, & z\ge0,\\
0, & z<0;
\end{cases}
$$
2.
$$
\hat\sigma_{\text{矩}}=\frac{\sqrt{2\pi}}{2}\,\overline Z;
$$
3.
$$
\hat\sigma_{\text{MLE}}=\sqrt{\frac1n\sum_{i=1}^n Z_i^2}.
$$

因为
$$
X_1-\mu\sim N(0,\sigma^2),
$$
故
$$
Z_1=|X_1-\mu|
$$
服从半正态分布，其分布函数为
$$
F(z)=P(Z_1\le z)=P(|X_1-\mu|\le z)
=
\begin{cases}
2\Phi\!\left(\dfrac z\sigma\right)-1, & z\ge0,\\[6pt]
0, & z<0.
\end{cases}
$$
故概率密度为
$$
f_{Z_1}(z)=
\begin{cases}
\dfrac{2}{\sqrt{2\pi}\sigma}e^{-z^2/(2\sigma^2)}, & z\ge0,\\
0, & z<0.
\end{cases}
$$

又
$$
EZ_1=\int_0^{+\infty} z\cdot \frac{2}{\sqrt{2\pi}\sigma}e^{-z^2/(2\sigma^2)}\,dz
=\frac{2}{\sqrt{2\pi}}\sigma.
$$
令样本一阶矩
$$
\overline Z=\frac1n\sum_{i=1}^n Z_i
$$
等于理论一阶矩，可得矩估计
$$
\hat\sigma_{\text{矩}}=\frac{\sqrt{2\pi}}{2}\,\overline Z.
$$

对观测值 $z_1,\ldots,z_n$，似然函数为
$$
L(\sigma)=\prod_{i=1}^n \frac{2}{\sqrt{2\pi}\sigma}e^{-z_i^2/(2\sigma^2)}
=\left(\frac{2}{\sqrt{2\pi}}\right)^n \sigma^{-n}
e^{-\frac1{2\sigma^2}\sum_{i=1}^n z_i^2}.
$$
其对数似然为
$$
\ln L(\sigma)=n\ln\frac{2}{\sqrt{2\pi}}-n\ln\sigma-\frac1{2\sigma^2}\sum_{i=1}^n z_i^2.
$$
求导并令其为零：
$$
-\frac n\sigma+\frac1{\sigma^3}\sum_{i=1}^n z_i^2=0.
$$
解得
$$
\hat\sigma_{\text{MLE}}=\sqrt{\frac1n\sum_{i=1}^n Z_i^2}.
$$
