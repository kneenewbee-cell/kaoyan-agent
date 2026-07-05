# Math 1 2002 Answers

资料类型：考研数学一答案解析
年份：2002
科目：数学一
范围：试卷 I
来源：D:\百度网盘\高数资料\【02】1987-2022年数学一真题详解答案（PDF）\2002考研数学一真题解析.pdf
校对状态：已按答案页图像和题干重新整理，去除识别碎行、串题内容和非本题页脚。

## 答案速查

| 题号 | 题型 | 答案 |
|---|---|---|
| 1 | 填空题 | $1$ |
| 2 | 填空题 | $-2$ |
| 3 | 填空题 | $y=\sqrt{x+1}$ |
| 4 | 填空题 | $2$ |
| 5 | 填空题 | $4$ |
| 6 | 选择题 | A |
| 7 | 选择题 | C |
| 8 | 选择题 | B |
| 9 | 选择题 | B |
| 10 | 选择题 | D |
| 11 | 解答题 | $a=2,\ b=-1$ |
| 12 | 解答题 | 切线方程为 $y=x$；极限为 $2$ |
| 13 | 解答题 | $e-1$ |
| 14 | 解答题 | 曲线积分与路径无关；当 $ab=cd$ 时，$I=\dfrac{c}{d}-\dfrac{a}{b}$ |
| 15 | 解答题 | $y''+y'+y=e^x$；$\displaystyle \sum_{n=0}^{\infty}\frac{x^{3n}}{(3n)!}=\frac{1}{3}e^x+\frac{2}{3}e^{-x/2}\cos\frac{\sqrt{3} x}{2}$ |
| 16 | 解答题 | 最大方向导数为 $\sqrt{(y_0-2x_0)^2+(x_0-2y_0)^2}$；攀登起点可取 $(5,-5)$ 或 $(-5,5)$ |
| 17 | 解答题 | $x=(1,1,1,1)^T+k(1,-2,1,0)^T,\ k\in\mathbb R$ |
| 18 | 解答题 | (1) 成立；(2) 逆命题一般不成立；(3) 对实对称矩阵逆命题成立 |
| 19 | 解答题 | $5$ |
| 20 | 解答题 | 矩估计为 $\hat\theta=\dfrac{1}{4}$；最大似然估计为 $\hat\theta=\dfrac{7-\sqrt{13}}{12}$ |

## 详细解析

### 第 1 题
- 答案：$1$

作广义积分极限：
$$
\int_e^{+\infty}\frac{dx}{x\ln^2x}
=\lim_{b\to+\infty}\int_e^b\frac{dx}{x\ln^2x}.
$$

令 $u=\ln x$，则 $du=dx/x$，所以
$$
\int_e^b\frac{dx}{x\ln^2x}
=\int_1^{\ln b}\frac{du}{u^2}
=\left[-\frac{1}{u}\right]_1^{\ln b}
=1-\frac{1}{\ln b}.
$$

令 $b\to+\infty$，得原积分为
$$
1.
$$

### 第 2 题
- 答案：$-2$

由
$$
e^y+6xy+x^2-1=0
$$
代入 $x=0$，得 $e^{y(0)}-1=0$，故 $y(0)=0$。

两边对 $x$ 求导：
$$
e^y y'+6y+6xy'+2x=0.
$$

代入 $x=0,y(0)=0$，得 $y'(0)=0$。

再对上式求导：
$$
e^y(y')^2+e^y y''+12y'+6xy''+2=0.
$$

代入 $x=0,y(0)=0,y'(0)=0$，得
$$
y''(0)+2=0,
$$
故
$$
y''(0)=-2.
$$

### 第 3 题
- 答案：$y=\sqrt{x+1}$

原方程可写成
$$
yy''+(y')^2=(yy')'=0.
$$

因此 $yy'=C$。由初始条件 $y(0)=1,\ y'(0)=\frac{1}{2}$，得
$$
C=1\cdot\frac{1}{2}=\frac{1}{2}.
$$

于是
$$
yy'=\frac{1}{2},
\qquad
(y^2)'=2yy'=1.
$$

积分得
$$
y^2=x+C_1.
$$

由 $y(0)=1$ 得 $C_1=1$。又初值处 $y>0$，取正支：
$$
y=\sqrt{x+1}.
$$

### 第 4 题
- 答案：$2$

二次型对应的实对称矩阵为
$$
A=\begin{pmatrix}
a&2&2\\
2&a&2\\
2&2&a
\end{pmatrix}.
$$

经正交变换化为标准形
$$
6y_1^2
$$
说明 $A$ 的特征值为 $6,0,0$。

矩阵的迹等于特征值之和，因此
$$
\operatorname{tr}A=3a=6+0+0=6.
$$

所以
$$
a=2.
$$

### 第 5 题
- 答案：$4$

二次方程
$$
y^2+4y+X=0
$$
没有实根，当且仅当判别式小于 $0$：
$$
16-4X<0,
$$
即
$$
X>4.
$$

题设给出该事件概率为
$$
P\{X>4\}=\frac{1}{2}.
$$

正态分布 $N(\mu,\sigma^2)$ 的密度关于 $x=\mu$ 对称，且
$$
P\{X>\mu\}=\frac{1}{2}.
$$

因此
$$
\mu=4.
$$

### 第 6 题
- 答案：A

多元函数在一点附近有如下常用推出关系：
$$
\text{偏导数连续}\ \Longrightarrow\ \text{可微}
\ \Longrightarrow\ \text{连续}.
$$

但连续不一定可微，可微也不要求偏导数在该点邻域连续；偏导数存在也不一定推出连续或可微。

所以题中必然成立的命题是 A。

### 第 7 题
- 答案：C

设
$$
S_n=\sum_{k=1}^n(-1)^{k+1}\left(\frac{1}{u_k}+\frac{1}{u_{k+1}}\right).
$$

部分和可望远镜化为
$$
S_n=\frac{1}{u_1}+(-1)^{n+1}\frac{1}{u_{n+1}}.
$$

由
$$
\lim_{n\to\infty}\frac{n}{u_n}=1
$$
知 $u_n\to+\infty$，故
$$
S_n\to\frac{1}{u_1},
$$
原级数收敛。

再看绝对值级数：
$$
\sum_{n=1}^{\infty}\left(\frac{1}{u_n}+\frac{1}{u_{n+1}}\right).
$$

因为 $u_n\sim n$，所以
$$
\frac{1}{u_n}+\frac{1}{u_{n+1}}\sim \frac{1}{n}+\frac{1}{n+1},
$$
与调和级数同阶，故发散。

因此原级数条件收敛，选 C。

### 第 8 题
- 答案：B

先证 B。若
$$
\lim_{x\to+\infty}f'(x)=A
$$
存在，若 $A>0$，则充分大的 $x$ 上有 $f'(x)>A/2$。由拉格朗日中值定理可知 $f(x)$ 将随 $x$ 至少线性增长，与 $f$ 在 $(0,+\infty)$ 内有界矛盾。

若 $A<0$，同理会推出 $f(x)$ 向负无穷方向无界，也矛盾。因此只能
$$
A=0.
$$

其余选项可用反例排除。令
$$
f(x)=\frac{\sin x^2}{x},
$$
则 $f$ 有界且 $f(x)\to0\ (x\to+\infty)$，但
$$
f'(x)=2\cos x^2-\frac{\sin x^2}{x^2}
$$
极限不存在，故 A 不成立。

令
$$
f(x)=\frac{x}{1+x},
$$
则 $f$ 在 $(0,+\infty)$ 内有界，且 $f(x)\to0\ (x\to0^+)$，但
$$
f'(x)=\frac{1}{(1+x)^2}\to1,
$$
所以 C、D 均不成立。

故选 B。

### 第 9 题
- 答案：B

三张平面有无公共点，可转化为三元线性方程组是否有解。

题设给出系数矩阵与增广矩阵的秩均为 $2$，且未知量个数为 $3$，因此
$$
r(A)=r(\bar A)=2<3.
$$

所以方程组有无穷多解。几何上，三个平面有无穷多个公共点，通常表现为相交于一条直线。

与四个图形选项比较，应选 B。

### 第 10 题
- 答案：D

若令
$$
X=\max(X_1,X_2),
$$
则 $X$ 也是随机变量。由于 $X_1,X_2$ 相互独立，
$$
P\{X\le x\}
=P\{X_1\le x,\ X_2\le x\}
=P\{X_1\le x\}P\{X_2\le x\}
=F_1(x)F_2(x).
$$

因此 $F_1(x)F_2(x)$ 一定是某个随机变量的分布函数。

另一方面，密度函数相加的积分为 $2$，不可能仍是密度；密度函数相乘不一定积分为 $1$；两个分布函数相加在 $+\infty$ 的极限为 $2$，也不可能是分布函数。

故选 D。

### 第 11 题
- 答案：$a=2,\ b=-1$

因为
$$
af(h)+bf(2h)-f(0)=o(h),
$$
特别有其极限为 $0$。令 $h\to0$，得
$$
(a+b-1)f(0)=0.
$$

又 $f(0)\ne0$，故
$$
a+b-1=0.
$$

将 $f(h),f(2h)$ 在 $h=0$ 处展开到一阶：
$$
f(h)=f(0)+f'(0)h+o(h),
$$
$$
f(2h)=f(0)+2f'(0)h+o(h).
$$

于是
$$
af(h)+bf(2h)-f(0)
=(a+b-1)f(0)+(a+2b)f'(0)h+o(h).
$$

要使其为比 $h$ 高阶的无穷小，还需
$$
(a+2b)f'(0)=0.
$$

由于 $f'(0)\ne0$，得
$$
a+2b=0.
$$

联立
$$
\begin{cases}
a+b=1,\\
a+2b=0,
\end{cases}
$$
解得
$$
a=2,\qquad b=-1.
$$

### 第 12 题
- 答案：切线方程为 $y=x$；极限为 $2$

设
$$
y=\int_0^{\arctan x}e^{-t^2}\,dt.
$$

则 $y(0)=0$，且由变上限积分求导公式，
$$
y'=e^{-(\arctan x)^2}\cdot\frac{1}{1+x^2}.
$$

代入 $x=0$，得
$$
y'(0)=1.
$$

所以该曲线在 $(0,0)$ 处的切线为
$$
y=x.
$$

题设函数 $y=f(x)$ 在 $(0,0)$ 处与上述曲线有相同切线，因此
$$
f(0)=0,\qquad f'(0)=1.
$$

于是
$$
\lim_{n\to\infty}n f\left(\frac{2}{n}\right)
=\lim_{n\to\infty}2\cdot
\frac{f(2/n)-f(0)}{2/n}
=2f'(0)=2.
$$

### 第 13 题
- 答案：$e-1$

在单位正方形
$$
D=\{(x,y)\mid 0\le x\le1,\ 0\le y\le1\}
$$
中，按 $y=x$ 分成两部分：
$$
D_1=\{0\le y\le x\le1\},\qquad
D_2=\{0\le x\le y\le1\}.
$$

在 $D_1$ 上有 $\max\{x^2,y^2\}=x^2$；在 $D_2$ 上有 $\max\{x^2,y^2\}=y^2$。故
$$
\iint_D e^{\max\{x^2,y^2\}}\,d\sigma
=\int_0^1\int_0^x e^{x^2}\,dy\,dx
+\int_0^1\int_0^y e^{y^2}\,dx\,dy.
$$

计算得
$$
\int_0^1 xe^{x^2}\,dx+\int_0^1 ye^{y^2}\,dy
=2\int_0^1 xe^{x^2}\,dx
=\int_0^1 e^{u}\,du
=e-1.
$$

### 第 14 题
- 答案：曲线积分与路径无关；当 $ab=cd$ 时，$I=\dfrac{c}{d}-\dfrac{a}{b}$

记
$$
P(x,y)=\frac{1}{y}\bigl[1+y^2f(xy)\bigr]
=\frac{1}{y}+yf(xy),
$$
$$
Q(x,y)=\frac{x}{y^2}\bigl[y^2f(xy)-1\bigr]
=xf(xy)-\frac{x}{y^2}.
$$

在上半平面 $y>0$ 内，
$$
\frac{\partial P}{\partial y}
=-\frac{1}{y^2}+f(xy)+xyf'(xy),
$$
$$
\frac{\partial Q}{\partial x}
=f(xy)+xyf'(xy)-\frac{1}{y^2}.
$$

两者相等，因此该曲线积分在上半平面内与路径无关。

进一步观察微分形式：
$$
P\,dx+Q\,dy
=\left(\frac{1}{y}\,dx-\frac{x}{y^2}\,dy\right)
+f(xy)(y\,dx+x\,dy).
$$

即
$$
P\,dx+Q\,dy
=d\left(\frac{x}{y}\right)+f(xy)\,d(xy).
$$

设 $F'(u)=f(u)$，则原函数为
$$
\frac{x}{y}+F(xy).
$$

从 $(a,b)$ 到 $(c,d)$ 的积分为
$$
I=\left[\frac{x}{y}+F(xy)\right]_{(a,b)}^{(c,d)}
=\frac{c}{d}-\frac{a}{b}+F(cd)-F(ab).
$$

若 $ab=cd$，则 $F(cd)-F(ab)=0$，故
$$
I=\frac{c}{d}-\frac{a}{b}.
$$

### 第 15 题
- 答案：$y''+y'+y=e^x$；$\displaystyle \sum_{n=0}^{\infty}\frac{x^{3n}}{(3n)!}=\frac{1}{3}e^x+\frac{2}{3}e^{-x/2}\cos\frac{\sqrt{3} x}{2}$

设
$$
y(x)=\sum_{n=0}^{\infty}\frac{x^{3n}}{(3n)!}.
$$

该幂级数收敛半径为 $+\infty$，可逐项求导：
$$
y'(x)=\sum_{n=1}^{\infty}\frac{x^{3n-1}}{(3n-1)!},
$$
$$
y''(x)=\sum_{n=1}^{\infty}\frac{x^{3n-2}}{(3n-2)!}.
$$

于是
$$
y''+y'+y
=\sum_{n=1}^{\infty}\frac{x^{3n-2}}{(3n-2)!}
+\sum_{n=1}^{\infty}\frac{x^{3n-1}}{(3n-1)!}
+\sum_{n=0}^{\infty}\frac{x^{3n}}{(3n)!}
=\sum_{m=0}^{\infty}\frac{x^m}{m!}
=e^x.
$$

同时
$$
y(0)=1,\qquad y'(0)=0.
$$

求微分方程
$$
y''+y'+y=e^x
$$
满足上述初值的解。齐次方程特征根为
$$
\lambda=\frac{-1\pm i\sqrt{3}}{2},
$$
故齐次通解为
$$
e^{-x/2}\left(C_1\cos\frac{\sqrt{3}x}{2}
+C_2\sin\frac{\sqrt{3}x}{2}\right).
$$

取特解 $y_p=ce^x$，代入得 $3c e^x=e^x$，所以 $c=\frac{1}{3}$。

因此
$$
y=e^{-x/2}\left(C_1\cos\frac{\sqrt{3}x}{2}
+C_2\sin\frac{\sqrt{3}x}{2}\right)+\frac{1}{3}e^x.
$$

由 $y(0)=1,\ y'(0)=0$ 解得
$$
C_1=\frac{2}{3},\qquad C_2=0.
$$

所以
$$
\sum_{n=0}^{\infty}\frac{x^{3n}}{(3n)!}
=\frac{2}{3}e^{-x/2}\cos\frac{\sqrt{3}x}{2}
+\frac{1}{3}e^x.
$$

### 第 16 题
- 答案：最大方向导数为 $\sqrt{(y_0-2x_0)^2+(x_0-2y_0)^2}$；攀登起点可取 $(5,-5)$ 或 $(-5,5)$

高度函数为
$$
h(x,y)=75-x^2-y^2+xy.
$$

其梯度为
$$
\nabla h(x,y)=(y-2x,\ x-2y).
$$

在点 $(x_0,y_0)$ 处方向导数的最大值等于梯度的模：
$$
\max\frac{\partial h}{\partial \ell}
=\|\nabla h(x_0,y_0)\|
=\sqrt{(y_0-2x_0)^2+(x_0-2y_0)^2}.
$$

在山脚线上
$$
h(x,y)=0,
$$
即
$$
x^2+y^2-xy=75.
$$

要使最大方向导数最大，只需在该约束下最大化
$$
g(x,y)=(y-2x)^2+(x-2y)^2
=5x^2+5y^2-8xy.
$$

用拉格朗日乘数法，令
$$
F=5x^2+5y^2-8xy+\lambda(75-x^2-y^2+xy).
$$

驻点方程给出两类可能：
$$
y=x
\quad\text{或}\quad
y=-x.
$$

当 $y=x$ 时，由约束得
$$
(x,y)=(5\sqrt{3},5\sqrt{3}),\ (-5\sqrt{3},-5\sqrt{3}),
$$
此时 $g=150$。

当 $y=-x$ 时，由约束得
$$
(x,y)=(5,-5),\ (-5,5),
$$
此时 $g=450$。

因此最大攀升起点可取
$$
(5,-5)\quad\text{或}\quad(-5,5).
$$

### 第 17 题
- 答案：$x=(1,1,1,1)^T+k(1,-2,1,0)^T,\ k\in\mathbb R$

记
$$
A=(\alpha_1,\alpha_2,\alpha_3,\alpha_4).
$$

由
$$
\alpha_1=2\alpha_2-\alpha_3
$$
可得
$$
\alpha_1-2\alpha_2+\alpha_3=0.
$$

因此
$$
\xi=(1,-2,1,0)^T
$$
是齐次方程 $Ax=0$ 的一个非零解。

又 $\alpha_2,\alpha_3,\alpha_4$ 线性无关，所以 $r(A)=3$，齐次方程基础解系只含一个解向量，故 $\xi$ 即可作为基础解系。

另一方面，
$$
\beta=\alpha_1+\alpha_2+\alpha_3+\alpha_4
=A(1,1,1,1)^T.
$$

所以
$$
\eta=(1,1,1,1)^T
$$
是非齐次方程 $Ax=\beta$ 的一个特解。

由非齐次线性方程组通解结构，
$$
x=\eta+k\xi
=(1,1,1,1)^T+k(1,-2,1,0)^T,\qquad k\in\mathbb R.
$$

### 第 18 题
- 答案：(1) 成立；(2) 逆命题一般不成立；(3) 对实对称矩阵逆命题成立

(1) 若 $A$ 与 $B$ 相似，则存在可逆矩阵 $P$，使
$$
B=P^{-1}AP.
$$

于是
$$
\det(\lambda E-B)
=\det(\lambda E-P^{-1}AP)
=\det(P^{-1}(\lambda E-A)P)
=\det(P^{-1})\det(\lambda E-A)\det(P)
=\det(\lambda E-A).
$$

故 $A,B$ 有相同的特征多项式。

(2) 逆命题一般不成立。取
$$
A=\begin{pmatrix}0&0\\0&0\end{pmatrix},
\qquad
B=\begin{pmatrix}0&1\\0&0\end{pmatrix}.
$$

两者特征多项式均为
$$
\lambda^2,
$$
但 $A$ 只能与零矩阵相似，而 $B\ne0$，所以 $A$ 与 $B$ 不相似。

(3) 若 $A,B$ 都是实对称矩阵，则它们都可正交相似于实对角矩阵。若二者特征多项式相同，则特征值及其重数完全相同，故 $A,B$ 都相似于同一个对角矩阵
$$
\operatorname{diag}(\lambda_1,\lambda_2,\ldots,\lambda_n).
$$

由相似关系的传递性，得到
$$
A\sim B.
$$

因此在实对称矩阵范围内，(1) 的逆命题成立。

### 第 19 题
- 答案：$5$

令一次观测成功事件为
$$
X>\frac{\pi}{3}.
$$

则
$$
p=P\left\{X>\frac{\pi}{3}\right\}
=\int_{\pi/3}^{\pi}\frac{1}{2}\cos\frac{x}{2}\,dx
=\left[\sin\frac{x}{2}\right]_{\pi/3}^{\pi}
=1-\frac{1}{2}=\frac{1}{2}.
$$

重复独立观察 $4$ 次，$Y$ 为成功次数，所以
$$
Y\sim B\left(4,\frac{1}{2}\right).
$$

于是
$$
E(Y)=np=2,
\qquad
D(Y)=np(1-p)=1.
$$

由
$$
E(Y^2)=D(Y)+[E(Y)]^2
$$
得
$$
E(Y^2)=1+2^2=5.
$$

### 第 20 题
- 答案：矩估计为 $\hat\theta=\dfrac{1}{4}$；最大似然估计为 $\hat\theta=\dfrac{7-\sqrt{13}}{12}$

先求总体均值：
$$
E(X)=0\cdot\theta^2+1\cdot2\theta(1-\theta)+2\theta^2+3(1-2\theta)
=3-4\theta.
$$

样本为
$$
3,1,3,0,3,1,2,3,
$$
其均值为
$$
\bar X=\frac{3+1+3+0+3+1+2+3}{8}=2.
$$

矩估计令 $E(X)=\bar X$，得
$$
3-4\theta=2,
$$
所以
$$
\hat\theta=\frac{1}{4}.
$$

再求最大似然估计。样本中 $0,1,2,3$ 出现次数分别为 $1,2,1,4$，故似然函数为
$$
L(\theta)=\theta^2[2\theta(1-\theta)]^2\theta^2(1-2\theta)^4
=4\theta^6(1-\theta)^2(1-2\theta)^4.
$$

取对数：
$$
\ln L(\theta)=\ln4+6\ln\theta+2\ln(1-\theta)+4\ln(1-2\theta).
$$

令导数为 $0$：
$$
\frac{d}{d\theta}\ln L(\theta)
=\frac{6}{\theta}-\frac{2}{1-\theta}-\frac{8}{1-2\theta}=0.
$$

化简得
$$
12\theta^2-14\theta+3=0,
$$
所以
$$
\theta=\frac{7\pm\sqrt{13}}{12}.
$$

由参数范围 $0<\theta<\frac{1}{2}$，只取
$$
\hat\theta=\frac{7-\sqrt{13}}{12}.
$$
