# 2015 年考研数学三答案解析

资料类型：考研数学三答案解析
年份：2015
科目：数学三
整理状态：按答案页图人工校对并整理为正式题卡。

## 选择题

| 题号 | 答案 |
|---|---|
| 1 | D |
| 2 | C |
| 3 | B |
| 4 | C |
| 5 | D |
| 6 | A |
| 7 | C |
| 8 | B |

## 填空题

| 题号 | 答案 |
|---|---|
| 9 | $-\dfrac12$ |
| 10 | $2$ |
| 11 | $-\dfrac13dx-\dfrac23dy$ |
| 12 | $2e^x+e^{-2x}$ |
| 13 | $21$ |
| 14 | $\dfrac12$ |

## 解答题

| 题号 | 答案 |
|---|---|
| 15 | $a=-1,\ b=-\dfrac12,\ k=-\dfrac13$ |
| 16 | $\dfrac{\pi}{4}-\dfrac25$ |
| 17 | 价格为 $p=30$ |
| 18 | $f(x)=\dfrac{8}{4-x}$ |
| 19 | $[u(x)v(x)]'=u'(x)v(x)+u(x)v'(x)$；且 $f'(x)=\sum_{k=1}^n\left(\prod_{j\ne k}u_j(x)\right)u_k'(x)$ |
| 20 | $a=0$；且 $X=\begin{pmatrix} 3&1&-2\\ 1&1&-1\\ 2&1&-1 \end{pmatrix}$ |
| 21 | $a=4,\quad b=5$；可取 $P=\begin{pmatrix} 2&-3&1\\ 1&0&1\\ 0&1&1 \end{pmatrix}$；使 $P^{-1}AP=\operatorname{diag}(1,1,5)$ |
| 22 | $P(Y=n)=(n-1)\left(\frac18\right)^2\left(\frac78\right)^{n-2},\quad n=2,3,\ldots$；且 $E(Y)=16$ |
| 23 | $\hat\theta_{\text{矩}}=2\overline X-1$ $\hat\theta_{\text{MLE}}=\min\{X_1,\ldots,X_n\}$ |

## 详细解析

### 第 1 题

- 标准答案：D

命题 A、C 都是“收敛数列的子列仍收敛且极限相同”的直接结论。

命题 B 也正确：若偶数项与奇数项都收敛到同一极限 $a$，则全体项都收敛到 $a$。

命题 D 错，可举反例
$$
x_n=
\begin{cases}
a+\dfrac1n, & n=3m,\\[4pt]
a+\dfrac1n, & n=3m-1,\\[4pt]
n, & n=3m-2.
\end{cases}
$$
则
$$
\lim_{n\to\infty}x_{3n}=\lim_{n\to\infty}x_{3n+1}=a,
$$
但 $\{x_n\}$ 不收敛。故选 D。

### 第 2 题

- 标准答案：C

由于 $f(x)$ 连续，拐点只能出现在 $f''(x)=0$ 或 $f''(x)$ 不存在且其符号发生变化的地方。

从图像可看出，在点 $A$ 左右两侧 $f''(x)>0$，故 $A$ 不是拐点对应位置；而在 $x=0$ 与 $x=B$ 附近，$f''(x)$ 的符号发生变化，因此对应两处拐点。

故曲线 $y=f(x)$ 有 $2$ 个拐点，选 C。

### 第 3 题

- 标准答案：B

圆 $x^2+y^2=2x$ 化为极坐标是
$$
r=2\cos\theta,
$$
圆 $x^2+y^2=2y$ 化为极坐标是
$$
r=2\sin\theta.
$$
因此公共区域在 $0\le\theta\le\pi/2$ 内，其中
$$
0\le\theta\le\frac\pi4
$$
时上界取 $2\sin\theta$，
$$
\frac\pi4\le\theta\le\frac\pi2
$$
时上界取 $2\cos\theta$。

故正确表达式为 B。

### 第 4 题

- 标准答案：C

A 由比值判别法收敛；B 中
$$
\ln\left(1+\frac1n\right)\sim \frac1n,
$$
故通项与 $n^{-3/2}$ 同阶，收敛；D 也可由比值判别法得收敛。

对于 C，
$$
\frac{(-1)^n+1}{\ln n}=
\begin{cases}
\dfrac{2}{\ln n}, & n=2m,\\[4pt]
0, & n=2m+1,
\end{cases}
$$
因此它大于发散的调和型子级数，故发散。选 C。

### 第 5 题

- 标准答案：D

有无穷多解要求
$$
r(A)=r(A,b)<3,
$$
首先
$$
|A|=(a-1)(a-2),
$$
故必须有
$$
a=1 \text{ 或 } a=2.
$$
再考察增广矩阵，可得只有在 $d=1$ 或 $d=2$ 时满足
$$
r(A)=r(A,b)<3.
$$
因此充分必要条件是
$$
a\in\Omega,\quad d\in\Omega.
$$
选 D。

### 第 6 题

- 标准答案：A

由 $Q=(e_1,-e_3,e_2)$ 可知，相当于在原标准形中交换第二、三坐标，并对新的第二坐标取负号。由于二次型中平方项对符号变化不敏感，只会交换
$$
y_2^2 \text{ 与 } -y_3^2
$$
的位置。

故新标准形为
$$
2y_1^2-y_2^2+y_3^2.
$$
选 A。

### 第 7 题

- 标准答案：C

一般情况下，$P(AB)$ 与 $P(A)P(B)$ 没有固定大小关系，所以 A、B 都不对。

又由概率性质
$$
P(A)\ge P(AB),\qquad P(B)\ge P(AB).
$$
两式相加得
$$
P(A)+P(B)\ge2P(AB),
$$
故
$$
P(AB)\le \frac{P(A)+P(B)}2.
$$
选 C。

### 第 8 题

- 标准答案：B

因为 $X\sim B(m,\theta)$，故
$$
D(X)=m\theta(1-\theta).
$$
记
$$
S^2=\frac1{n-1}\sum_{i=1}^n(X_i-\overline X)^2,
$$
则
$$
E(S^2)=D(X)=m\theta(1-\theta).
$$
因此
$$
E\left[\sum_{i=1}^n(X_i-\overline X)^2\right]
=(n-1)E(S^2)=m(n-1)\theta(1-\theta).
$$
选 B。

### 第 9 题

- 标准答案：$-\dfrac12$

当 $x\to0$ 时，
$$
\cos x=1-\frac{x^2}{2}+o(x^2).
$$
因此
$$
\ln(\cos x)=\ln\left(1-\frac{x^2}{2}+o(x^2)\right)\sim-\frac{x^2}{2}.
$$
故极限为
$$
-\frac12.
$$

### 第 10 题

- 标准答案：$2$

有
$$
\varphi(1)=\int_0^1 f(t)\,dt=1.
$$
又
$$
\varphi'(x)=\int_0^{x^2}f(t)\,dt+2x^2f(x^2).
$$
故
$$
\varphi'(1)=\int_0^1f(t)\,dt+2f(1)=1+2f(1)=5.
$$
解得
$$
f(1)=2.
$$

### 第 11 题

- 标准答案：$-\dfrac13dx-\dfrac23dy$

在 $(0,0)$ 处由方程可得 $z=0$。

对原方程分别关于 $x,y$ 求导并代入 $(0,0,0)$，得
$$
\frac{\partial z}{\partial x}\Big|_{(0,0)}=-\frac13,\qquad
\frac{\partial z}{\partial y}\Big|_{(0,0)}=-\frac23.
$$
因此
$$
dz\big|_{(0,0)}=-\frac13dx-\frac23dy.
$$

### 第 12 题

- 标准答案：$2e^x+e^{-2x}$

特征方程为
$$
\lambda^2+\lambda-2=0,
$$
解得
$$
\lambda_1=1,\qquad \lambda_2=-2.
$$
故通解
$$
y=C_1e^x+C_2e^{-2x}.
$$
由题意知
$$
y(0)=3,\qquad y'(0)=0,
$$
解得
$$
C_1=2,\qquad C_2=1.
$$
因此
$$
y(x)=2e^x+e^{-2x}.
$$

### 第 13 题

- 标准答案：$21$

若 $\lambda$ 是 $A$ 的特征值，则
$$
\lambda^2-\lambda+1
$$
是 $B=A^2-A+E$ 的特征值。

因此 $B$ 的特征值为
$$
3,\ 7,\ 1.
$$
故
$$
|B|=3\cdot7\cdot1=21.
$$

### 第 14 题

- 标准答案：$\dfrac12$

相关系数为 $0$，故 $X,Y$ 独立，且
$$
X\sim N(1,1),\qquad Y\sim N(0,1).
$$
条件
$$
XY-Y<0
$$
化为
$$
Y(X-1)<0.
$$
于是
$$
P\{Y>0,X<1\}+P\{Y<0,X>1\}
=\frac12\cdot\frac12+\frac12\cdot\frac12=\frac12.
$$

### 第 15 题

- 标准答案：$a=-1,\ b=-\dfrac12,\ k=-\dfrac13$

若 $f(x)\sim g(x)=kx^3$，则 $f(x)$ 的一、二阶导在 $0$ 处都应为 $0$。

先求
$$
f'(0)=1+a,
$$
故
$$
a=-1.
$$

再求
$$
f''(0)=1+2b,
$$
故
$$
b=-\frac12.
$$

最后比较三阶项，可得
$$
\lim_{x\to0}\frac{f(x)}{x^3}=-\frac13,
$$
于是
$$
k=-\frac13.
$$

### 第 16 题

- 标准答案：$\dfrac{\pi}{4}-\dfrac25$

由于区域 $D$ 关于 $y$ 轴对称，
$$
\iint_D xy\,dxdy=0.
$$
故
$$
\iint_D x(x+y)\,dxdy=\iint_D x^2\,dxdy.
$$

按 $x$ 积分，可写成
$$
2\int_0^1dx\int_{x^2}^{\sqrt{2-x^2}}x^2\,dy
=2\int_0^1 x^2\bigl(\sqrt{2-x^2}-x^2\bigr)\,dx.
$$
令 $x=\sqrt2\sin t$ 可算得
$$
2\int_0^1 x^2\sqrt{2-x^2}\,dx=\frac{\pi}{4},
$$
又
$$
2\int_0^1x^4\,dx=\frac25.
$$
故原积分
$$
=\frac{\pi}{4}-\frac25.
$$

### 第 17 题

- 标准答案：价格为 $p=30$

收益函数
$$
R=pQ.
$$
边际收益为
$$
MR=\frac{dR}{dQ}=p+Q\frac{dp}{dQ}
=p\left(1-\frac1\eta\right),
$$
其中利用了
$$
\eta=-\frac{p}{Q}\frac{dQ}{dp}.
$$
利润最大化条件为
$$
MR=MC,
$$
故
$$
p=\frac{MC}{1-\frac1\eta}.
$$

在题设下
$$
MC=C'(Q)=2Q,\qquad \eta=-\frac{p}{Q}\frac{dQ}{dp}=\frac{p}{40-p}.
$$
代入定价模型，
$$
p=\frac{2Q}{1-\frac{40-p}{p}}.
$$
再用 $Q=40-p$ 化简，解得
$$
p=30.
$$

### 第 18 题

- 标准答案：$f(x)=\dfrac{8}{4-x}$

点 $(x_0,f(x_0))$ 处切线方程为
$$
y=f(x_0)+f'(x_0)(x-x_0).
$$
它与 $x$ 轴的交点横坐标为
$$
x_0-\frac{f(x_0)}{f'(x_0)}.
$$
于是题设三角形面积条件给出
$$
\frac12\cdot \left|\frac{f(x_0)}{f'(x_0)}\right|\cdot |f(x_0)|=4.
$$
由于 $f'(x)>0$ 且 $f(0)=2>0$，可取正号，得
$$
y'=\frac18y^2.
$$
解得
$$
y=\frac{8}{C-x}.
$$
由 $f(0)=2$ 得 $C=4$，故
$$
f(x)=\frac{8}{4-x}.
$$

### 第 19 题

- 标准答案：$$
[u(x)v(x)]'=u'(x)v(x)+u(x)v'(x),
$$
且
$$
f'(x)=\sum_{k=1}^n\left(\prod_{j\ne k}u_j(x)\right)u_k'(x).
$$

由导数定义，
$$
\frac{u(x+\Delta x)v(x+\Delta x)-u(x)v(x)}{\Delta x}
$$
可拆为
$$
\frac{u(x+\Delta x)-u(x)}{\Delta x}v(x+\Delta x)
+u(x)\frac{v(x+\Delta x)-v(x)}{\Delta x}.
$$
令 $\Delta x\to0$，即得
$$
[u(x)v(x)]'=u'(x)v(x)+u(x)v'(x).
$$

对 $n$ 个函数的乘积，反复使用乘积法则可得
$$
f'(x)=u_1'(x)u_2(x)\cdots u_n(x)+u_1(x)u_2'(x)\cdots u_n(x)+\cdots+u_1(x)u_2(x)\cdots u_n'(x),
$$
即
$$
f'(x)=\sum_{k=1}^n\left(\prod_{j\ne k}u_j(x)\right)u_k'(x).
$$

### 第 20 题

- 标准答案：$$
a=0,
$$
且
$$
X=\begin{pmatrix}
3&1&-2\\
1&1&-1\\
2&1&-1
\end{pmatrix}.
$$

由 $A^3=O$ 可知 $A$ 的全部特征值为 $0$，故
$$
|A|=a^3=0,
$$
从而
$$
a=0.
$$

原方程可因式分解为
$$
(E-A)X(E-A^2)=E.
$$
因此
$$
X=(E-A)^{-1}(E-A^2)^{-1}.
$$
当 $a=0$ 时，直接计算可得
$$
X=\begin{pmatrix}
3&1&-2\\
1&1&-1\\
2&1&-1
\end{pmatrix}.
$$

### 第 21 题

- 标准答案：$$
a=4,\quad b=5.
$$

可取
$$
P=\begin{pmatrix}
2&-3&1\\
1&0&1\\
0&1&1
\end{pmatrix},
$$
使
$$
P^{-1}AP=\operatorname{diag}(1,1,5).
$$

由相似矩阵的性质，
$$
\operatorname{tr}(A)=\operatorname{tr}(B),\qquad |A|=|B|.
$$
由此解得
$$
a=4,\qquad b=5.
$$

于是
$$
|\lambda E-A|=|\lambda E-B|=(\lambda-1)^2(\lambda-5).
$$
所以 $A$ 的特征值为 $1,1,5$。

解特征方程可取对应线性无关特征向量
$$
\xi_1=(2,1,0)^T,\quad
\xi_2=(-3,0,1)^T,\quad
\xi_3=(1,1,1)^T.
$$
令
$$
P=(\xi_1,\xi_2,\xi_3)
=\begin{pmatrix}
2&-3&1\\
1&0&1\\
0&1&1
\end{pmatrix},
$$
则
$$
P^{-1}AP=\operatorname{diag}(1,1,5).
$$

### 第 22 题

- 标准答案：$$
P(Y=n)=(n-1)\left(\frac18\right)^2\left(\frac78\right)^{n-2},\quad n=2,3,\ldots
$$
且
$$
E(Y)=16.
$$

先求一次观测“大于 $3$”的概率：
$$
p=P(X>3)=\int_3^{+\infty}2^{-x}\ln2\,dx=2^{-3}=\frac18.
$$
于是 $Y$ 表示独立伯努利试验中“第 $2$ 次成功出现时的试验次数”，故服从参数为 $r=2,p=\frac18$ 的负二项分布：
$$
P(Y=n)=\binom{n-1}{1}p^2(1-p)^{n-2}
=(n-1)\left(\frac18\right)^2\left(\frac78\right)^{n-2},
\quad n\ge2.
$$

其期望为
$$
E(Y)=\frac{r}{p}=\frac{2}{1/8}=16.
$$

### 第 23 题

- 标准答案：$$
\hat\theta_{\text{矩}}=2\overline X-1,
$$
$$
\hat\theta_{\text{MLE}}=\min\{X_1,\ldots,X_n\}.
$$

该总体服从区间 $[\theta,1]$ 上的均匀分布，因此
$$
EX=\frac{\theta+1}{2}.
$$
令样本均值 $\overline X$ 等于理论均值，得矩估计量
$$
\hat\theta_{\text{矩}}=2\overline X-1.
$$

对样本 $x_1,\ldots,x_n$，似然函数为
$$
L(\theta)=
\begin{cases}
(1-\theta)^{-n}, & \theta\le \min\{x_1,\ldots,x_n\},\\
0, & \text{否则}.
\end{cases}
$$
在允许范围内，$L(\theta)$ 随 $\theta$ 增大而增大，因此最大似然估计取可行域最大值：
$$
\hat\theta_{\text{MLE}}=\min\{X_1,\ldots,X_n\}.
$$
