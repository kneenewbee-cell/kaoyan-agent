# 2005 年数学三答案解析

资料类型：考研数学三答案解析
年份：2005
科目：数学三
整理状态：按答案页图人工清洗并整理为正式题卡格式


## 填空题

| 题号 | 答案 |
|---|---|
| 1 | $2$ |
| 2 | $xy=2$ |
| 3 | $2e\,dx+(e+2)\,dy$ |
| 4 | $\dfrac12$ |
| 5 | $\dfrac{13}{48}$ |
| 6 | $a=0.4,\ b=0.1$ |

## 选择题

| 题号 | 答案 |
|---|---|
| 7 | B |
| 8 | A |
| 9 | D |
| 10 | B |
| 11 | C |
| 12 | A |
| 13 | D |
| 14 | C |

## 解答题

| 题号 | 答案 |
|---|---|
| 15 | $\dfrac32$ |
| 16 | $\dfrac{2y}{x}f'\!\left(\dfrac{y}{x}\right)$ |
| 17 | $\dfrac{\pi}{4}-\dfrac13$ |
| 18 | $S(x)=\begin{cases}\dfrac{1}{2x}\ln\dfrac{1+x}{1-x}-\dfrac{1}{1-x^2},& \lvert x\rvert<1,\ x\ne0,\\[4pt]0,&x=0\end{cases}$ |
| 19 | 命题成立 |
| 20 | $(a,b,c)=(2,1,2)$ |
| 21 | $P^TDP=\begin{pmatrix}A&0\\0&B-C^TA^{-1}C\end{pmatrix}$，且 $B-C^TA^{-1}C$ 为正定矩阵 |
| 22 | $f_X(x)=2x\ (0<x<1)$，$f_Y(y)=1-\dfrac y2\ (0<y<2)$，$f_Z(z)=1-\dfrac z2\ (0<z<2)$；$P\{Y\le\dfrac12\mid X\le\dfrac12\}=\dfrac34$ |
| 23 | $D(Y_i)=\dfrac{n-1}{n}\sigma^2,\ \operatorname{Cov}(Y_1,Y_n)=-\dfrac1n\sigma^2,\ c=\dfrac{n}{2(n-2)}$ |

## 详细解析

### 第1题

- 答案：$2$

当 $x\to\infty$ 时，
$$
\frac{2x}{x^2+1}\sim \frac{2}{x},
$$
于是
$$
x\sin\frac{2x}{x^2+1}\sim x\cdot \frac{2x}{x^2+1}\to 2.
$$

### 第2题

- 答案：$xy=2$

原方程可写成
$$
(xy)'=0,
$$
积分得 $xy=C$。由初始条件 $y(1)=2$ 得 $C=2$，故特解为
$$
xy=2.
$$

### 第3题

- 答案：$2e\,dx+(e+2)\,dy$

有
$$
\frac{\partial z}{\partial x}=e^{x+y}+xe^{x+y}+\ln(1+y),
\qquad
\frac{\partial z}{\partial y}=xe^{x+y}+\frac{x+1}{1+y}.
$$
在 $(1,0)$ 处，
$$
\frac{\partial z}{\partial x}=2e,\qquad
\frac{\partial z}{\partial y}=e+2.
$$
故
$$
dz\big|_{(1,0)}=2e\,dx+(e+2)\,dy.
$$

### 第4题

- 答案：$\dfrac12$

四个 $4$ 维向量线性相关，其对应行列式应为零：
$$
\begin{vmatrix}
2&1&1&1\\
2&1&a&a\\
3&2&1&a\\
4&3&2&1
\end{vmatrix}
=(a-1)(2a-1)=0.
$$
解得 $a=1$ 或 $a=\dfrac12$。由题设 $a\ne1$，故
$$
a=\frac12.
$$

### 第5题

- 答案：$\dfrac{13}{48}$

按 $X$ 分解：
$$
P\{Y=2\}
=\sum_{k=1}^4 P\{X=k\}P\{Y=2\mid X=k\}.
$$
其中
$$
P\{X=k\}=\frac14,\quad
P\{Y=2\mid X=1\}=0,\ 
P\{Y=2\mid X=2\}=\frac12,\ 
P\{Y=2\mid X=3\}=\frac13,\ 
P\{Y=2\mid X=4\}=\frac14.
$$
所以
$$
P\{Y=2\}
=\frac14\left(0+\frac12+\frac13+\frac14\right)
=\frac{13}{48}.
$$

### 第6题

- 答案：$a=0.4,\ b=0.1$

由概率和为 $1$，得
$$
a+b=0.5.
$$
又
$$
P(X=0)=0.4+a,\qquad P(X+Y=1)=a+b.
$$
而
$$
P(X=0,\ X+Y=1)=P(X=0,Y=1)=a.
$$
由独立性，
$$
a=P(X=0)\,P(X+Y=1)=(0.4+a)(a+b).
$$
再结合 $a+b=0.5$，解得
$$
a=0.4,\qquad b=0.1.
$$

### 第7题

- 答案：B

有
$$
f'(x)=6x^2-18x+12=6(x-1)(x-2),
$$
故可能极值点为 $x=1,2$。计算得
$$
f(1)=5-a,\qquad f(2)=4-a.
$$
恰有两个不同零点时，需要有一个极值恰好为 $0$，由此得 $a=4$，故选 `B`。

### 第8题

- 答案：A

在区域 $D$ 上有
$$
0\le (x^2+y^2)^2 \le x^2+y^2 \le \sqrt{x^2+y^2}\le 1<\frac{\pi}{2}.
$$
由于 $\cos t$ 在 $\left(0,\frac{\pi}{2}\right)$ 上单调递减，所以
$$
\cos\sqrt{x^2+y^2}\le \cos(x^2+y^2)\le \cos(x^2+y^2)^2.
$$
对区域 $D$ 积分可得
$$
I_1<I_2<I_3,
$$
故选 `A`。

### 第9题

- 答案：D

取反例 $a_n=\dfrac1n$。则
$$
\sum a_n
$$
发散，而
$$
\sum (-1)^{n-1}a_n
$$
收敛。此时奇项级数和偶项级数都发散，所以 `A`、`B` 错；并且
$$
\sum (a_{2n-1}+a_{2n})
$$
仍发散，故 `C` 错。  
另一方面，
$$
\sum (a_{2n-1}-a_{2n})
$$
正是交错级数的分组形式，收敛，故选 `D`。

### 第10题

- 答案：B

有
$$
f'(x)=x\cos x,
$$
故 $f'(0)=0,\ f'\left(\dfrac{\pi}{2}\right)=0$。再算
$$
f''(x)=\cos x-x\sin x.
$$
于是
$$
f''(0)=1>0,\qquad
f''\left(\frac{\pi}{2}\right)=-\frac{\pi}{2}<0.
$$
所以 $f(0)$ 为极小值，$f\left(\dfrac{\pi}{2}\right)$ 为极大值，选 `B`。

### 第11题

- 答案：C

`A`、`B` 不对，例如 $f(x)=\dfrac1x$ 在 $(0,1)$ 内连续，且 $f'(x)=-\dfrac1{x^2}$ 也连续，但 $f(x)$ 无界。  
`D` 不对，例如 $f(x)=\sqrt x$ 在 $(0,1)$ 内有界，但
$$
f'(x)=\frac{1}{2\sqrt x}
$$
无界。  
若 $f'(x)$ 在 $(0,1)$ 内有界，则 $f$ 满足 Lipschitz 型估计，从而在该区间内不能发散，故 `C` 正确。

### 第12题

- 答案：A

由
$$
AA^*=|A|E
$$
及 $A^*=A^T$ 得
$$
AA^T=|A|E.
$$
从而 $|A|^2=|A|^3$，又因 $a_{11},a_{12},a_{13}$ 为相等正数，不可能有 $|A|=0$，故 $|A|=1$。  
设 $a_{11}=a_{12}=a_{13}=t>0$，则第一行与对应代数余子式关系给出
$$
3t^2=1,
$$
故
$$
t=\frac{\sqrt3}{3}.
$$
选 `A`。

### 第13题

- 答案：D

有
$$
A(\alpha_1+\alpha_2)=\lambda_1\alpha_1+\lambda_2\alpha_2.
$$
在基 $\{\alpha_1,\alpha_2\}$ 下，向量组
$$
\alpha_1,\ A(\alpha_1+\alpha_2)
$$
的系数矩阵为
$$
\begin{pmatrix}
1 & \lambda_1\\
0 & \lambda_2
\end{pmatrix}.
$$
其行列式为 $\lambda_2$，故线性无关当且仅当 $\lambda_2\ne 0$。选 `D`。

### 第14题

- 答案：C

总体方差未知，故用统计量
$$
\frac{\bar X-\mu}{S/\sqrt n}\sim t(n-1).
$$
这里 $n=16$，自由度为 $15$，置信度 $0.90$ 对应双侧临界值 $t_{0.05}(15)$。  
又
$$
\frac{S}{\sqrt n}=\frac14,
$$
所以区间为
$$
\left(20-\frac14 t_{0.05}(15),\,20+\frac14 t_{0.05}(15)\right).
$$
故选 `C`。

### 第15题

- 答案：$\dfrac32$

通分得
$$
\frac{1+x}{1-e^{-x}}-\frac1x
=\frac{x+x^2-1+e^{-x}}{x(1-e^{-x})}.
$$
这是 $0/0$ 型，应用洛必达法则：
$$
\lim_{x\to0}\frac{x+x^2-1+e^{-x}}{x(1-e^{-x})}
=\lim_{x\to0}\frac{1+2x-e^{-x}}{1-e^{-x}+xe^{-x}}
=\lim_{x\to0}\frac{2+e^{-x}}{2e^{-x}}
=\frac32.
$$

### 第16题

- 答案：$\dfrac{2y}{x}f'\!\left(\dfrac{y}{x}\right)$

先求偏导：
$$
\frac{\partial g}{\partial x}
=-\frac{y}{x^2}f'\!\left(\frac{y}{x}\right)+f'\!\left(\frac{x}{y}\right),
$$
$$
\frac{\partial g}{\partial y}
=\frac1x f'\!\left(\frac{y}{x}\right)+f\!\left(\frac{x}{y}\right)-\frac{x}{y}f'\!\left(\frac{x}{y}\right).
$$
继续求二阶偏导并整理，可得
$$
x^2\frac{\partial^2 g}{\partial x^2}-y^2\frac{\partial^2 g}{\partial y^2}
=\frac{2y}{x}f'\!\left(\frac{y}{x}\right).
$$

### 第17题

- 答案：$\dfrac{\pi}{4}-\dfrac13$

在正方形区域 $D$ 内，曲线 $x^2+y^2=1$ 将区域分成两部分。记
$$
D_1=\{(x,y)\in D\mid x^2+y^2\le 1\},\qquad
D_2=\{(x,y)\in D\mid x^2+y^2>1\}.
$$
则
$$
\iint_D |x^2+y^2-1|\,d\sigma
=-\iint_{D_1}(x^2+y^2-1)\,d\sigma+\iint_{D_2}(x^2+y^2-1)\,d\sigma.
$$
计算后得
$$
\iint_D |x^2+y^2-1|\,d\sigma
=\frac{\pi}{4}-\frac13.
$$

### 第18题

- 答案：$$
S(x)=
\begin{cases}
\dfrac{1}{2x}\ln\dfrac{1+x}{1-x}-\dfrac{1}{1-x^2}, & |x|<1,\ x\ne 0,\\[6pt]
0, & x=0.
\end{cases}
$$

设
$$
S(x)=\sum_{n=1}^{\infty}\left(\frac{1}{2n+1}-1\right)x^{2n}
=S_1(x)-S_2(x),
$$
其中
$$
S_1(x)=\sum_{n=1}^{\infty}\frac{x^{2n}}{2n+1},\qquad
S_2(x)=\sum_{n=1}^{\infty}x^{2n}=\frac{x^2}{1-x^2}.
$$
对 $xS_1(x)$ 求导，
$$
(xS_1(x))'=\sum_{n=1}^{\infty}x^{2n}=\frac{x^2}{1-x^2}.
$$
积分并利用 $S_1(0)=0$，得
$$
S_1(x)=
\begin{cases}
-1+\dfrac{1}{2x}\ln\dfrac{1+x}{1-x}, & x\ne 0,\\[6pt]
0, & x=0.
\end{cases}
$$
于是
$$
S(x)=
\begin{cases}
\dfrac{1}{2x}\ln\dfrac{1+x}{1-x}-\dfrac{1}{1-x^2}, & |x|<1,\ x\ne 0,\\[6pt]
0, & x=0.
\end{cases}
$$

### 第19题

- 答案：命题成立

设
$$
F(x)=\int_0^x g(t)f'(t)\,dt+\int_0^1 f(t)g'(t)\,dt-f(x)g(1).
$$
则
$$
F'(x)=g(x)f'(x)-f'(x)g(1)=f'(x)\,[g(x)-g(1)]\le 0,
$$
因为 $f'(x)\ge 0$，且 $g(x)\le g(1)$。故 $F(x)$ 在 $[0,1]$ 上单调递减。  
另一方面，
$$
F(1)=\int_0^1 g(t)f'(t)\,dt+\int_0^1 f(t)g'(t)\,dt-f(1)g(1)=0
$$
（由分部积分可得）。于是对任意 $a\in[0,1]$，
$$
F(a)\ge F(1)=0,
$$
即
$$
\int_0^a g(x)f'(x)\,dx+\int_0^1 f(x)g'(x)\,dx\ge f(a)g(1).
$$

### 第20题

- 答案：$(a,b,c)=(2,1,2)$

方程组 (ii) 只有两行，显然有无穷多解，因此方程组 (i) 也应有无穷多解，其系数矩阵秩小于 $3$。  
对 (i) 的系数矩阵作初等变换，可得第三行变为
$$
(0,0,a-2),
$$
故
$$
a=2.
$$
此时 (i) 的基础解系可取为
$$
(-1,-1,1)^T.
$$
将其代入 (ii) 得
$$
b=1,\ c=2
$$
或 $b=0,\ c=1$。再检验与 (i) 是否同解，只有
$$
(b,c)=(1,2)
$$
成立。  
故
$$
(a,b,c)=(2,1,2).
$$

### 第21题

- 答案：$$
P^TDP=
\begin{pmatrix}
A & 0\\
0 & B-C^TA^{-1}C
\end{pmatrix},
\qquad
B-C^TA^{-1}C\ \text{为正定矩阵}.
$$

先算
$$
P^T=
\begin{pmatrix}
E_m & O\\
-C^TA^{-1} & E_n
\end{pmatrix}.
$$
直接做分块矩阵乘法得
$$
P^TDP=
\begin{pmatrix}
A & 0\\
0 & B-C^TA^{-1}C
\end{pmatrix}.
$$
由于 $D$ 正定，且 $P$ 可逆，故 $P^TDP$ 与 $D$ 合同，因此也正定。  
而 $P^TDP$ 是分块对角矩阵，所以对任意非零 $Y\in\mathbb R^n$，
$$
\begin{pmatrix}0\\Y\end{pmatrix}^T
\begin{pmatrix}
A & 0\\
0 & B-C^TA^{-1}C
\end{pmatrix}
\begin{pmatrix}0\\Y\end{pmatrix}
=Y^T(B-C^TA^{-1}C)Y>0.
$$
故
$$
B-C^TA^{-1}C
$$
是正定矩阵。

### 第22题

- 答案：$$
f_X(x)=
\begin{cases}
2x, & 0<x<1,\\
0, & \text{其他},
\end{cases}
\qquad
f_Y(y)=
\begin{cases}
1-\dfrac y2, & 0<y<2,\\
0, & \text{其他},
\end{cases}
$$
$$
f_Z(z)=
\begin{cases}
1-\dfrac z2, & 0<z<2,\\
0, & \text{其他},
\end{cases}
\qquad
P\left\{Y\le \dfrac12\mid X\le \dfrac12\right\}=\frac34.
$$

由定义，
$$
f_X(x)=\int_{-\infty}^{+\infty}f(x,y)\,dy=
\begin{cases}
\int_0^{2x}1\,dy=2x, & 0<x<1,\\
0, & \text{其他},
\end{cases}
$$
$$
f_Y(y)=\int_{-\infty}^{+\infty}f(x,y)\,dx=
\begin{cases}
\int_{y/2}^{1}1\,dx=1-\dfrac y2, & 0<y<2,\\
0, & \text{其他}.
\end{cases}
$$
令 $F_Z(z)=P(Z\le z)=P(2X-Y\le z)$。分段计算可得
$$
F_Z(z)=
\begin{cases}
0, & z<0,\\
z-\dfrac14 z^2, & 0\le z<2,\\
1, & z\ge 2.
\end{cases}
$$
故
$$
f_Z(z)=F_Z'(z)=
\begin{cases}
1-\dfrac z2, & 0<z<2,\\
0, & \text{其他}.
\end{cases}
$$
最后，
$$
P\left\{Y\le \frac12\mid X\le \frac12\right\}
=\frac{P\left\{X\le \frac12,\ Y\le \frac12\right\}}{P\left\{X\le \frac12\right\}}
=\frac{3/16}{1/4}
=\frac34.
$$

### 第23题

- 答案：$$
D(Y_i)=\frac{n-1}{n}\sigma^2,\qquad
\operatorname{Cov}(Y_1,Y_n)=-\frac1n\sigma^2,\qquad
c=\frac{n}{2(n-2)}.
$$

由 $E(X_i)=0,\ D(X_i)=\sigma^2$，且样本独立，知
$$
Y_i=X_i-\overline X.
$$
于是
$$
D(Y_i)=D(X_i-\overline X)=\frac{n-1}{n}\sigma^2.
$$
再由协方差定义展开，
$$
\operatorname{Cov}(Y_1,Y_n)
=E[(X_1-\overline X)(X_n-\overline X)]
=-\frac1n\sigma^2.
$$
最后
$$
E[c(Y_1+Y_n)^2]=c\,D(Y_1+Y_n)
=c\,[D(Y_1)+D(Y_n)+2\operatorname{Cov}(Y_1,Y_n)].
$$
代入前两问结果得
$$
E[c(Y_1+Y_n)^2]
=c\cdot \frac{2(n-2)}{n}\sigma^2.
$$
令其等于 $\sigma^2$，解得
$$
c=\frac{n}{2(n-2)}.
$$
