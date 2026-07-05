# 2013 年数学三答案解析

资料类型：考研数学三答案解析
年份：2013
科目：数学三
整理状态：按答案页图核对后整理；个别题目解析为依据标准答案补写的清晰版。

## 选择题

| 题号 | 答案 |
|---|---|
| 1 | D |
| 2 | C |
| 3 | B |
| 4 | D |
| 5 | B |
| 6 | B |
| 7 | A |
| 8 | C |

## 填空题

| 题号 | 答案 |
|---|---|
| 9 | $-2$ |
| 10 | $2(1-\ln 2)$ |
| 11 | $\ln 2$ |
| 12 | $e^{x/2}(C_1x+C_2)$ |
| 13 | $-1$ |
| 14 | $2e^2$ |

## 解答题

| 题号 | 答案 |
|---|---|
| 15 | $n=2,\ a=7$ |
| 16 | $a=7^{3/2}$ |
| 17 | $\dfrac{416}{3}$ |
| 18 | 边际利润为 $\Pi'(Q)=40-\frac{Q}{500}$；当 $p=50$ 时边际利润为 $20$；利润最大时的定价为 $40$ 元。 |
| 19 | 命题成立 |
| 20 | 存在解当且仅当 $a=-1,\qquad b=0$；此时全部解为 $C= \begin{pmatrix} s+t+1 & -s\\ s & t \end{pmatrix},\qquad s,t\in\mathbb R$ |
| 21 | 对应矩阵为 $2\alpha\alpha^T+\beta\beta^T$；且在条件 $\alpha\perp\beta,\ \lVert\alpha\rVert=\lVert\beta\rVert=1$ 下，标准形为 $2y_1^2+y_2^2$ |
| 22 | $f(x,y)= \begin{cases} 9y^2,& 0<y<x<1,\\ 0,& \text{其他}, \end{cases}$ $f_Y(y)= \begin{cases} 9y^2(1-y),& 0<y<1,\\ 0,& \text{其他}, \end{cases}$；且 $P\{X>2Y\}=\frac{3}{32}$ |
| 23 | 矩估计量为 $\hat\theta_{\text{矩}}=\overline X$；最大似然估计量为 $\hat\theta_{\text{MLE}}=\frac{2n}{\sum_{i=1}^n\frac1{X_i}}$ |

## 详细解析

### 第 1 题

- 答案：D

由高阶无穷小的定义，
$$
o(x)+o(x^2)=o(x),
$$
一般不能保证仍是 $o(x^2)$，所以 `D` 错误。

其余各项都成立：例如 $o(x)\cdot o(x^2)$ 至少是比 $x^3$ 更高阶的无穷小。

### 第 2 题

- 答案：C

函数在可能出现间断的点是 $x=0$ 与 $x=-1$。

当 $x\to 0$ 时，利用
$$
|x|^{|x|}=e^{|x|\ln|x|}=1+|x|\ln|x|+o(|x|\ln|x|),
$$
可知分子与分母同阶，极限存在。

当 $x\to -1$ 时，同样可将分子写为 $e^{|x|\ln|x|}-1$，配合分母中的 $(x+1)\ln|x|$，可算出左右极限存在且相等。

因此可去间断点共有 $2$ 个，选 `C`。

### 第 3 题

- 答案：B

在第二象限中 $x<0,\ y>0$，因此被积函数
$$
y-x=y+|x|>0,
$$
从而
$$
I_2>0.
$$

而第一象限内 $y-x$ 正负皆可能；第三、四象限中又会因为 $x,y$ 的符号变化使积分不恒正。故正确项是 `B`。

### 第 4 题

- 答案：D

若存在 $p>1$ 使 $\lim\limits_{n\to\infty}n^pa_n=L$ 存在，则当 $n$ 足够大时
$$
a_n\sim \frac{L}{n^p}\quad \text{或}\quad a_n=O\!\left(\frac1{n^p}\right).
$$
由 $p$ 级数比较判别法，
$$
\sum a_n
$$
收敛，所以 `D` 正确。

其余三项都可举反例否定，例如交错级数收敛不必意味着单调性严格成立。

### 第 5 题

- 答案：B

由 $C=AB$ 可知，$C$ 的每个列向量都是 $A$ 的列向量组的线性组合，因此 $C$ 的列向量组可由 $A$ 的列向量组线性表示。

又因为 $B$ 可逆，所以
$$
A=CB^{-1},
$$
故 $A$ 的列向量组也可由 $C$ 的列向量组线性表示。

因此矩阵 $C$ 与矩阵 $A$ 的列向量组等价，选 `B`。

### 第 6 题

- 答案：B

设
$$
M=
\begin{pmatrix}
1&a&1\\
a&b&a\\
1&a&1
\end{pmatrix}.
$$
由于第一行与第三行相同，$0$ 是其特征值。若它与对角矩阵 $\operatorname{diag}(2,b,0)$ 相似，则其全部特征值应为 $2,b,0$。

直接计算特征多项式可得
$$
|\lambda E-M|=\lambda\bigl((2-\lambda)(b-\lambda)-2a^2\bigr).
$$
要与
$$
\lambda(2-\lambda)(b-\lambda)
$$
一致，必须有
$$
a=0.
$$
当 $a=0$ 时，矩阵确实具有特征值 $2,b,0$，并且是实对称矩阵，可相似对角化。

故充要条件是 `B`。

### 第 7 题

- 答案：A

对 $X_1\sim N(0,1)$，
$$
p_1=P(|X_1|\le 2)=2\Phi(2)-1.
$$

对 $X_2\sim N(0,4)$，
$$
p_2=P\left(\left|\frac{X_2}{2}\right|\le 1\right)=2\Phi(1)-1.
$$
由于 $\Phi(2)>\Phi(1)$，故 $p_1>p_2$。

对 $X_3\sim N(5,9)$，区间 $[-2,2]$ 整体位于均值 $5$ 左侧，故该概率显著小于前两者，因此
$$
p_1>p_2>p_3.
$$
选 `A`。

### 第 8 题

- 答案：C

由独立性，
$$
P(X+Y=2)=P(X=1,Y=1)+P(X=2,Y=0)+P(X=3,Y=-1).
$$
因此
$$
P(X+Y=2)=\frac14\cdot\frac13+\frac18\cdot\frac13+\frac18\cdot\frac13
=\frac{1}{12}+\frac{1}{24}+\frac{1}{24}
=\frac16.
$$
故选 `C`。

### 第 9 题

- 答案：$-2$

由“公共切线”知
$$
f(1)=0,\qquad f'(1)=\left.(2x-1)\right|_{x=1}=1.
$$
又
$$
\frac{n}{n+2}=1-\frac{2}{n+2}.
$$
故在 $x=1$ 附近作一阶展开：
$$
f\left(\frac{n}{n+2}\right)=f(1)+f'(1)\left(-\frac{2}{n+2}\right)+o\left(\frac1n\right)
=-\frac{2}{n+2}+o\left(\frac1n\right).
$$
于是
$$
\lim_{n\to\infty}n\,f\left(\frac{n}{n+2}\right)=-2.
$$

### 第 10 题

- 答案：$2(1-\ln 2)$

先在点 $(1,2)$ 求出 $z$：
$$
(z+2)^1=1\cdot 2,
$$
所以 $z=0$。

对等式两边取对数：
$$
x\ln(z+y)=\ln x+\ln y.
$$
对 $x$ 求偏导得
$$
\ln(z+y)+x\frac{z_x}{z+y}=\frac1x.
$$
代入 $(x,y,z)=(1,2,0)$，得到
$$
\ln 2+\frac{z_x}{2}=1.
$$
故
$$
z_x=2(1-\ln2).
$$

### 第 11 题

- 答案：$\ln 2$

分部积分，取
$$
u=\ln x,\qquad dv=\frac{dx}{(1+x)^2}.
$$
则
$$
du=\frac{dx}{x},\qquad v=-\frac{1}{1+x}.
$$
故
$$
\int_1^{+\infty}\frac{\ln x}{(1+x)^2}\,dx
=\left.-\frac{\ln x}{1+x}\right|_1^{+\infty}
+\int_1^{+\infty}\frac{1}{x(1+x)}\,dx.
$$
前一项为 $0$，后一项
$$
\int_1^{+\infty}\left(\frac1x-\frac1{1+x}\right)\,dx
=\ln 2.
$$

### 第 12 题

- 答案：$e^{x/2}(C_1x+C_2)$

特征方程为
$$
r^2-r+\frac14=0,
$$
即
$$
\left(r-\frac12\right)^2=0.
$$
有二重根 $r=\dfrac12$，故通解为
$$
y=e^{x/2}(C_1x+C_2).
$$

### 第 13 题

- 答案：$-1$

由条件
$$
a_{ij}+A_{ij}=0
$$
可知
$$
A^*=-A.
$$
又由伴随矩阵恒等式
$$
AA^*=|A|E
$$
得
$$
A(-A)=|A|E.
$$
两边取行列式，并注意 $A\ne 0$，可推出
$$
|A|=-1.
$$

### 第 14 题

- 答案：$2e^2$

标准正态分布的矩母函数为
$$
M_X(t)=E(e^{tX})=e^{t^2/2}.
$$
于是
$$
E(Xe^{tX})=M_X'(t)=te^{t^2/2}.
$$
取 $t=2$，得
$$
E(Xe^{2X})=2e^2.
$$

### 第 15 题

- 答案：$n=2,\ a=7$

利用
$$
\cos(kx)=1-\frac{k^2x^2}{2}+o(x^2)\qquad (k=1,2,3),
$$
有
$$
\cos x\cos 2x\cos 3x
=\left(1-\frac{x^2}{2}\right)\left(1-2x^2\right)\left(1-\frac{9x^2}{2}\right)+o(x^2).
$$
只保留二次项，得
$$
\cos x\cos 2x\cos 3x
=1-\left(\frac12+2+\frac92\right)x^2+o(x^2)
=1-7x^2+o(x^2).
$$
因此
$$
1-\cos x\cos 2x\cos 3x=7x^2+o(x^2).
$$
所以
$$
n=2,\qquad a=7.
$$

### 第 16 题

- 答案：$a=7^{3/2}$

区域为
$$
0\le x\le a,\qquad 0\le y\le x^{1/3}.
$$
绕 $x$ 轴旋转：
$$
V_x=\pi\int_0^a \left(x^{1/3}\right)^2dx
=\pi\int_0^a x^{2/3}dx
=\frac{3\pi}{5}a^{5/3}.
$$

绕 $y$ 轴旋转：
$$
V_y=2\pi\int_0^a x\cdot x^{1/3}dx
=2\pi\int_0^a x^{4/3}dx
=\frac{6\pi}{7}a^{7/3}.
$$
由 $V_y=10V_x$，得
$$
\frac{6\pi}{7}a^{7/3}=10\cdot \frac{3\pi}{5}a^{5/3}=6\pi a^{5/3}.
$$
约去公共因子后有
$$
a^{2/3}=7,
$$
故
$$
a=7^{3/2}.
$$

### 第 17 题

- 答案：$\dfrac{416}{3}$

三条直线围成三角形，顶点为
$$
(0,0),\quad (2,6),\quad (6,2).
$$
按 $x$ 分段：

当 $0\le x\le 2$ 时，
$$
\frac{x}{3}\le y\le 3x.
$$

当 $2\le x\le 6$ 时，
$$
\frac{x}{3}\le y\le 8-x.
$$

故
$$
\iint_Dx^2\,dxdy
=\int_0^2x^2\left(3x-\frac{x}{3}\right)dx
+\int_2^6x^2\left((8-x)-\frac{x}{3}\right)dx.
$$
即
$$
=\int_0^2\frac{8}{3}x^3dx+\int_2^6\left(8x^2-\frac{4}{3}x^3\right)dx
=\frac{32}{3}+128
=\frac{416}{3}.
$$

### 第 18 题

- 答案：边际利润为
$$
\Pi'(Q)=40-\frac{Q}{500};
$$
当 $p=50$ 时边际利润为 $20$；
利润最大时的定价为 $40$ 元。

利润函数为
$$
\Pi(Q)=pQ-(60000+20Q)
=\left(60-\frac{Q}{1000}\right)Q-60000-20Q
=40Q-\frac{Q^2}{1000}-60000.
$$
故边际利润
$$
\Pi'(Q)=40-\frac{Q}{500}.
$$

当 $p=50$ 时，由
$$
50=60-\frac{Q}{1000}
$$
得
$$
Q=10000.
$$
于是
$$
\Pi'(10000)=40-\frac{10000}{500}=20.
$$
其经济意义是：当价格为 $50$ 元、销量处于对应平衡点时，销量每增加 $1$ 件，利润约增加 $20$ 元。

要使利润最大，令
$$
\Pi'(Q)=0,
$$
得
$$
Q=20000.
$$
代回价格函数：
$$
p=60-\frac{20000}{1000}=40.
$$

### 第 19 题

- 答案：命题成立

因为
$$
\lim_{x\to+\infty}f(x)=2,
$$
所以存在 $X>0$，使得当 $x>X$ 时，
$$
f(x)>1.
$$
函数 $f$ 在 $[0,X]$ 上连续，又
$$
f(0)=0<1,\qquad f(X)>1,
$$
由介值定理知，存在
$$
a\in(0,X)
$$
使得
$$
f(a)=1.
$$

再看区间 $[0,a]$。函数 $f$ 在其上连续、在其内可导，故由拉格朗日中值定理，存在
$$
\xi\in(0,a)
$$
使得
$$
f'(\xi)=\frac{f(a)-f(0)}{a-0}=\frac{1-0}{a}=\frac1a.
$$
证毕。

### 第 20 题

- 答案：存在解当且仅当
$$
a=-1,\qquad b=0.
$$
此时全部解为
$$
C=
\begin{pmatrix}
s+t+1 & -s\\
s & t
\end{pmatrix},\qquad s,t\in\mathbb R.
$$

设
$$
C=
\begin{pmatrix}
x_1&x_2\\
x_3&x_4
\end{pmatrix}.
$$
则
$$
AC=
\begin{pmatrix}
x_1+ax_3 & x_2+ax_4\\
x_1 & x_2
\end{pmatrix},
\qquad
CA=
\begin{pmatrix}
x_1+x_2 & ax_1\\
x_3+x_4 & ax_3
\end{pmatrix}.
$$
因此
$$
AC-CA=
\begin{pmatrix}
ax_3-x_2 & -ax_1+x_2+ax_4\\
x_1-x_3-x_4 & x_2-ax_3
\end{pmatrix}
=
\begin{pmatrix}
0&1\\
1&b
\end{pmatrix}.
$$
得到方程组
$$
\begin{cases}
ax_3-x_2=0,\\
-ax_1+x_2+ax_4=1,\\
x_1-x_3-x_4=1,\\
x_2-ax_3=b.
\end{cases}
$$
由第一式与第四式立刻得到
$$
b=0.
$$
再由第一式 $x_2=ax_3$ 代入第二式，结合第三式
$$
x_1-x_3-x_4=1
$$
可得
$$
a(-x_1+x_3+x_4)=1.
$$
而第三式等价于
$$
-x_1+x_3+x_4=-1,
$$
所以
$$
-a=1,\qquad a=-1.
$$

当 $a=-1,\ b=0$ 时，令
$$
x_3=s,\qquad x_4=t,
$$
则
$$
x_2=-s,\qquad x_1=s+t+1.
$$
故全部解为
$$
C=
\begin{pmatrix}
s+t+1 & -s\\
s & t
\end{pmatrix},\qquad s,t\in\mathbb R.
$$

### 第 21 题

- 答案：对应矩阵为
$$
2\alpha\alpha^T+\beta\beta^T,
$$
且在条件 $\alpha\perp\beta,\ \|\alpha\|=\|\beta\|=1$ 下，标准形为
$$
2y_1^2+y_2^2.
$$

先将二次型写成矩阵形式：
$$
f(x)=2(\alpha^Tx)^2+(\beta^Tx)^2
=2x^T\alpha\alpha^Tx+x^T\beta\beta^Tx
=x^T(2\alpha\alpha^T+\beta\beta^T)x.
$$
故对应矩阵就是
$$
A=2\alpha\alpha^T+\beta\beta^T.
$$

若 $\alpha,\beta$ 正交且均为单位向量，则
$$
A\alpha=2\alpha,\qquad A\beta=\beta.
$$
因此 $2$ 与 $1$ 是 $A$ 的特征值，对应特征向量分别为 $\alpha,\beta$。

又因为
$$
r(A)\le r(2\alpha\alpha^T)+r(\beta\beta^T)\le 2,
$$
故第三个特征值必为 $0$。

矩阵 $A$ 为实对称矩阵，所以存在正交矩阵使其对角化为
$$
\operatorname{diag}(2,1,0).
$$
于是二次型在正交变换下的标准形为
$$
2y_1^2+y_2^2.
$$

### 第 22 题

- 答案：$$
f(x,y)=
\begin{cases}
9y^2,& 0<y<x<1,\\
0,& \text{其他},
\end{cases}
$$
$$
f_Y(y)=
\begin{cases}
9y^2(1-y),& 0<y<1,\\
0,& \text{其他},
\end{cases}
$$
且
$$
P\{X>2Y\}=\frac{3}{32}.
$$

由联合密度与条件密度关系
$$
f(x,y)=f_{Y\mid X}(y\mid x)f_X(x),
$$
得
$$
f(x,y)=
\begin{cases}
\dfrac{3y^2}{x^3}\cdot 3x^2=9y^2,& 0<y<x<1,\\
0,& \text{其他}.
\end{cases}
$$

于是
$$
f_Y(y)=\int_y^1 9y^2\,dx
=9y^2(1-y),\qquad 0<y<1.
$$
其余处为 $0$。

最后，
$$
P(X>2Y)=\iint_{x>2y}f(x,y)\,dxdy.
$$
由约束 $0<y<x<1$ 与 $x>2y$，可知
$$
0<y<\frac12,\qquad 2y<x<1.
$$
故
$$
P(X>2Y)=\int_0^{1/2}\int_{2y}^1 9y^2\,dxdy
=\int_0^{1/2}9y^2(1-2y)\,dy
=\frac{3}{32}.
$$

### 第 23 题

- 答案：矩估计量为
$$
\hat\theta_{\text{矩}}=\overline X;
$$
最大似然估计量为
$$
\hat\theta_{\text{MLE}}=\frac{2n}{\sum_{i=1}^n\frac1{X_i}}.
$$

先求总体期望：
$$
E(X)=\int_0^\infty x\cdot \frac{\theta^2}{x^3}e^{-\theta/x}\,dx
=\int_0^\infty \frac{\theta^2}{x^2}e^{-\theta/x}\,dx.
$$
令
$$
u=\frac{\theta}{x},\qquad x=\frac{\theta}{u},\qquad dx=-\frac{\theta}{u^2}\,du,
$$
则
$$
E(X)=\theta\int_0^\infty e^{-u}\,du=\theta.
$$
因此矩估计由
$$
\overline X=E(X)=\theta
$$
得到
$$
\hat\theta_{\text{矩}}=\overline X.
$$

再求最大似然估计。样本似然函数为
$$
L(\theta)=\prod_{i=1}^n\frac{\theta^2}{X_i^3}e^{-\theta/X_i}
=\theta^{2n}\left(\prod_{i=1}^nX_i^{-3}\right)\exp\left(-\theta\sum_{i=1}^n\frac1{X_i}\right).
$$
取对数得
$$
\ln L(\theta)=2n\ln\theta-3\sum_{i=1}^n\ln X_i-\theta\sum_{i=1}^n\frac1{X_i}.
$$
求导并令其为零：
$$
\frac{d}{d\theta}\ln L(\theta)=\frac{2n}{\theta}-\sum_{i=1}^n\frac1{X_i}=0.
$$
解得
$$
\hat\theta_{\text{MLE}}=\frac{2n}{\sum_{i=1}^n\frac1{X_i}}.
$$
