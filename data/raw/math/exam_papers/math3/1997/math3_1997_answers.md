# 1997 年考研数学三答案与解析

## 答案速览

| 题 | 答案 |
|---:|---|
| 1 | $dy=e^{f(x)}\left(\frac{f'(\ln x)}{x}+f(\ln x)f'(x)\right)\,dx$ |
| 2 | $\displaystyle \int_0^1 f(x)\,dx=\frac{\pi}{4-\pi}$ |
| 3 | $y_t=C+(t-2)2^t$ |
| 4 | $-\sqrt{2}<t<\sqrt{2}$ |
| 5 | $U\sim t(9)$ |
| 6 | (B) |
| 7 | (C) |
| 8 | (C) |
| 9 | (D) |
| 10 | (A) |
| 11 | $\displaystyle \lim_{x\to0}Q(x)=AK^\delta L^{1-\delta}$ |
| 12 | $\displaystyle \frac{du}{dx}=f_x+\frac{y^2}{1-xy}f_y+\frac{(x-1)e^x}{x^2}f_z$ |
| 13 | （1）最大利润时的销售量为 $x=\max\left\{10-\frac{5}{2}t,\,0\right\}$；若按通常情形 $0\le t<4$，则 $x=10-\frac{5}{2}t$。 （2）当 $t=2$ 时政府税收总额最大。 |
| 14 | $F(x)$ 在 $[0,+\infty)$ 上连续且单调不减。 |
| 15 | （1）$\overline{OP_n}=2^{1-n}$；（2）$\displaystyle \sum_{n=1}^{\infty}\overline{Q_nP_n}=\frac43$。 |
| 16 | $f(t)=(1+4\pi t^2)e^{4\pi t^2}$ |
| 17 | $\displaystyle PQ=\begin{pmatrix}A&\alpha\\0&|A|\bigl(b-\alpha^TA^{-1}\alpha\bigr)\end{pmatrix}$，且 $Q$ 可逆当且仅当 $\alpha^TA^{-1}\alpha\ne b$。 |
| 18 | （1）属于特征值 $3$ 的特征向量可取 $\alpha_3=(1,0,1)^T$；（2）$\displaystyle A=\begin{pmatrix}\frac{13}{6}&-\frac13&\frac56\\-\frac13&\frac53&\frac13\\\frac56&\frac13&\frac{13}{6}\end{pmatrix}$。 |
| 19 | $\displaystyle F(x)=\begin{cases}0,&x<-1,\\\frac{5x+7}{16},&-1\le x<1,\\1,&x\ge1.\end{cases}$ |
| 20 | $\displaystyle E(Y)=\frac{35}{3}\text{ 分钟}$ |
| 21 | $\displaystyle f_T(t)=\begin{cases}25te^{-5t},&t>0,\\0,&t\le0,\end{cases}\qquad E(T)=\frac25,\qquad D(T)=\frac{2}{25}$ |

## 详细解析

### 第1题

- 答案：$dy=e^{f(x)}\left(\frac{f'(\ln x)}{x}+f(\ln x)f'(x)\right)\,dx$

由乘积求导与链式法则，
$$
y=f(\ln x)e^{f(x)}
$$
的微分为
$$
dy=e^{f(x)}\,d\bigl(f(\ln x)\bigr)+f(\ln x)\,d\bigl(e^{f(x)}\bigr).
$$
其中
$$
d\bigl(f(\ln x)\bigr)=f'(\ln x)\,d(\ln x)=\frac{f'(\ln x)}{x}\,dx,
$$
$$
d\bigl(e^{f(x)}\bigr)=e^{f(x)}f'(x)\,dx.
$$
代回即可得到
$$
dy=e^{f(x)}\left(\frac{f'(\ln x)}{x}+f(\ln x)f'(x)\right)dx.
$$

### 第2题

- 答案：$\displaystyle \int_0^1 f(x)\,dx=\frac{\pi}{4-\pi}$

设
$$
A=\int_0^1 f(x)\,dx.
$$
由题设可写成
$$
f(x)=\frac{1}{1+x^2}+A\sqrt{1-x^2}.
$$
两边在 $[0,1]$ 上积分，得
$$
A=\int_0^1\frac{1}{1+x^2}\,dx+A\int_0^1\sqrt{1-x^2}\,dx.
$$
其中
$$
\int_0^1\frac{1}{1+x^2}\,dx=\frac{\pi}{4},\qquad
\int_0^1\sqrt{1-x^2}\,dx=\frac{\pi}{4}.
$$
因而
$$
A=\frac{\pi}{4}+\frac{\pi}{4}A,
$$
解得
$$
A=\frac{\pi}{4-\pi}.
$$

### 第3题

- 答案：$y_t=C+(t-2)2^t$

先解对应齐次方程
$$
y_{t+1}-y_t=0,
$$
其通解为 $y_t^{(h)}=C$。

对非齐次方程设一个特解为
$$
y_t^{(p)}=(At+B)2^t.
$$
则
$$
y_{t+1}^{(p)}-y_t^{(p)}=\bigl[A(t+1)+B\bigr]2^{t+1}-(At+B)2^t
=(At+2A+B)2^t.
$$
与右端 $t2^t$ 对比，得到
$$
At+2A+B=t,
$$
所以 $A=1,\ B=-2$。

因而通解为
$$
y_t=y_t^{(h)}+y_t^{(p)}=C+(t-2)2^t.
$$

### 第4题

- 答案：$-\sqrt{2}<t<\sqrt{2}$

该二次型对应的对称矩阵为
$$
A=\begin{pmatrix}
2 & 1 & 0\\
1 & 1 & \frac t2\\
0 & \frac t2 & 1
\end{pmatrix}.
$$
由 Sylvester 判别法，二次型正定当且仅当顺序主子式全大于零。
$$
\Delta_1=2>0,
$$
$$
\Delta_2=\begin{vmatrix}2&1\\1&1\end{vmatrix}=1>0,
$$
$$
\Delta_3=\det A
=2\left(1-\frac{t^2}{4}\right)-1
=1-\frac{t^2}{2}>0.
$$
因此
$$
t^2<2,
$$
即
$$
-\sqrt2<t<\sqrt2.
$$

### 第5题

- 答案：$U\sim t(9)$

由于 $X_1,\dots,X_9$ 独立同分布于 $N(0,3^2)$，故
$$
X_1+\cdots+X_9\sim N(0,9\cdot 3^2)=N(0,9^2).
$$
因而
$$
\frac{X_1+\cdots+X_9}{9}\sim N(0,1).
$$

又因为 $Y_1,\dots,Y_9$ 独立同分布于 $N(0,3^2)$，所以
$$
\sum_{i=1}^9\left(\frac{Y_i}{3}\right)^2\sim \chi^2(9),
$$
即
$$
\frac{Y_1^2+\cdots+Y_9^2}{9}\sim \chi^2(9).
$$

从而
$$
U=\frac{X_1+\cdots+X_9}{\sqrt{Y_1^2+\cdots+Y_9^2}}
=\frac{\dfrac{X_1+\cdots+X_9}{9}}{\sqrt{\dfrac{Y_1^2+\cdots+Y_9^2}{9}/9}},
$$
按 $t$ 分布定义可知
$$
U\sim t(9).
$$

### 第6题

- 答案：(B)

由变上限积分求导公式，
$$
f'(x)=\sin\bigl((1-\cos x)^2\bigr)\cdot \sin x.
$$
当 $x\to0$ 时，$1-\cos x\sim \dfrac{x^2}{2}$，故
$$
\sin\bigl((1-\cos x)^2\bigr)\sim (1-\cos x)^2\sim \frac{x^4}{4},
\qquad \sin x\sim x.
$$
因而
$$
f'(x)\sim \frac{x^5}{4}.
$$
又 $f(0)=0$，所以 $f(x)$ 的阶至少为 $x^6$。

而
$$
g(x)=\frac{x^5}{5}+\frac{x^6}{6}\sim \frac{x^5}{5}.
$$
所以
$$
\lim_{x\to0}\frac{f(x)}{g(x)}=0,
$$
即 $f(x)$ 是 $g(x)$ 的高阶无穷小，选 $(B)$。

### 第7题

- 答案：(C)

因为 $f(-x)=f(x)$，所以 $f$ 是偶函数，从而
$$
f'(-x)=-f'(x),\qquad f''(-x)=f''(x).
$$
已知当 $x<0$ 时，$f'(x)>0$ 且 $f''(x)<0$。

令 $x>0$，则 $-x<0$，于是
$$
f'(-x)>0\Rightarrow -f'(x)>0\Rightarrow f'(x)<0,
$$
$$
f''(-x)<0\Rightarrow f''(x)<0.
$$
所以在 $(0,+\infty)$ 内有 $f'(x)<0$ 且 $f''(x)<0$，应选 $(C)$。

### 第8题

- 答案：(C)

把各组选项中的向量都写成基底 $\alpha_1,\alpha_2,\alpha_3$ 下的坐标。

对于 $(C)$，三向量对应的坐标列分别为
$$
(1,2,0)^T,\quad (0,2,3)^T,\quad (1,0,3)^T.
$$
其系数矩阵为
$$
C=\begin{pmatrix}
1&0&1\\
2&2&0\\
0&3&3
\end{pmatrix},
$$
且
$$
\det C=4\ne0.
$$
因而这组三向量线性无关。

其余各组都可以直接构造出非零线性关系，例如 $(A)$ 中
$$
(\alpha_1+\alpha_2)-(\alpha_2+\alpha_3)+(\alpha_3-\alpha_1)=0,
$$
所以不线性无关。故选 $(C)$。

### 第9题

- 答案：(D)

对任意同阶可逆矩阵 $A,B$，取
$$
P=I,\qquad Q=A^{-1}B,
$$
则 $Q$ 也是可逆矩阵，并且
$$
PAQ=A(A^{-1}B)=B.
$$
因而选项 $(D)$ 总成立。

其余选项都不一定成立。例如一般可逆矩阵并不必满足 $AB=BA$，也不必相似，更不必合同。

### 第10题

- 答案：(A)

由于 $X,Y$ 独立且都只取 $\pm1$，并且各自两点概率都为 $\dfrac12$，四种组合
$$
(-1,-1),\ (-1,1),\ (1,-1),\ (1,1)
$$
的概率都等于 $\dfrac14$。

因而
$$
P\{X=Y\}=P\{(-1,-1)\}+P\{(1,1)\}=\frac14+\frac14=\frac12.
$$
所以 $(A)$ 成立。

同时 $P\{X+Y=0\}=\dfrac12$，$P\{XY=1\}=\dfrac12$，故其余选项不对。

### 第11题

- 答案：$\displaystyle \lim_{x\to0}Q(x)=AK^\delta L^{1-\delta}$

设
$$
Q(x)=A\bigl[\delta K^{-x}+(1-\delta)L^{-x}\bigr]^{-1/x}.
$$
取对数，记
$$
\ln\frac{Q(x)}{A}=-\frac1x\ln\bigl(\delta K^{-x}+(1-\delta)L^{-x}\bigr).
$$
又
$$
K^{-x}=e^{-x\ln K}=1-x\ln K+o(x),
\qquad
L^{-x}=e^{-x\ln L}=1-x\ln L+o(x).
$$
因而
$$
\delta K^{-x}+(1-\delta)L^{-x}
=1-x\bigl(\delta\ln K+(1-\delta)\ln L\bigr)+o(x).
$$
再利用 $\ln(1+u)=u+o(u)$，得到
$$
\ln\bigl(\delta K^{-x}+(1-\delta)L^{-x}\bigr)
=-x\bigl(\delta\ln K+(1-\delta)\ln L\bigr)+o(x).
$$
所以
$$
\lim_{x\to0}\ln\frac{Q(x)}{A}
=\delta\ln K+(1-\delta)\ln L.
$$
两边取指数即得
$$
\lim_{x\to0}Q(x)=A\exp\bigl(\delta\ln K+(1-\delta)\ln L\bigr)=AK^\delta L^{1-\delta}.
$$

### 第12题

- 答案：$\displaystyle \frac{du}{dx}=f_x+\frac{y^2}{1-xy}f_y+\frac{(x-1)e^x}{x^2}f_z$

由复合函数求导公式，
$$
\frac{du}{dx}=f_x+f_y\frac{dy}{dx}+f_z\frac{dz}{dx}.
$$
只需求出 $y'(x),z'(x)$。

由
$$
e^{xy}-y=0
$$
两边对 $x$ 求导，得
$$
e^{xy}(xy'+y)-y'=0.
$$
又由原方程知 $e^{xy}=y$，所以
$$
y(xy-1)+y^2=0,
$$
从而
$$
y'=\frac{y^2}{1-xy}.
$$

再由
$$
e^x-xz=0
$$
对 $x$ 求导，得
$$
e^x-z-xz'=0.
$$
由原式 $z=\dfrac{e^x}{x}$，于是
$$
z'=\frac{e^x-z}{x}=\frac{(x-1)e^x}{x^2}.
$$
代回即可得到
$$
\frac{du}{dx}=f_x+\frac{y^2}{1-xy}f_y+\frac{(x-1)e^x}{x^2}f_z.
$$

### 第13题

- 答案：（1）最大利润时的销售量为 $x=\max\left\{10-\frac{5}{2}t,\,0\right\}$；若按通常情形 $0\le t<4$，则 $x=10-\frac{5}{2}t$。  
（2）当 $t=2$ 时政府税收总额最大。

利润函数为
$$
\Pi(x)=x(7-0.2x)-(3x+1)-tx=-0.2x^2+(4-t)x-1,\qquad x\ge0.
$$
这是开口向下的二次函数。若只看顶点，其顶点横坐标为
$$
x=\frac{4-t}{0.4}=10-\frac52 t.
$$
考虑销售量约束 $x\ge0$，故最大利润对应的销售量为
$$
x=\max\left\{10-\frac52 t,\,0\right\}.
$$
在通常经济情形 $0\le t<4$ 下，可直接写成
$$
x=10-\frac52 t.
$$

政府税收总额为
$$
T(t)=tx=t\left(10-\frac52 t\right)=10t-\frac52 t^2.
$$
这也是开口向下的二次函数，故最大值在顶点处取得：
$$
t=\frac{10}{5}=2.
$$

### 第14题

- 答案：$F(x)$ 在 $[0,+\infty)$ 上连续且单调不减。

当 $x>0$ 时，$F(x)=\dfrac1x\int_0^x t^n f(t)\,dt$ 显然连续，只需考察 $x=0$ 处。
因为 $f$ 在 $[0,+\infty)$ 上单调不减且 $f(0)\ge0$，所以对 $x>0$ 有 $f(t)\le f(x)$，从而
$$
0\le F(x)\le \frac{f(x)}{x}\int_0^x t^n\,dt=\frac{f(x)x^n}{n+1}.
$$
当 $x\to0^+$ 时，右端趋于 $0$，故
$$
\lim_{x\to0^+}F(x)=0=F(0).
$$
所以 $F$ 在 $[0,+\infty)$ 上连续。

对 $x>0$ 求导：
$$
F'(x)=\frac{x^{n+1}f(x)-\int_0^x t^n f(t)\,dt}{x^2}.
$$
由单调性知 $f(t)\le f(x)$，故
$$
\int_0^x t^n f(t)\,dt\le f(x)\int_0^x t^n\,dt=\frac{x^{n+1}}{n+1}f(x).
$$
因而
$$
x^{n+1}f(x)-\int_0^x t^n f(t)\,dt\ge \frac{n}{n+1}x^{n+1}f(x)\ge0,
$$
即 $F'(x)\ge0$。所以 $F$ 在 $[0,+\infty)$ 上单调不减。

### 第15题

- 答案：（1）$\overline{OP_n}=2^{1-n}$；（2）$\displaystyle \sum_{n=1}^{\infty}\overline{Q_nP_n}=\frac43$。

设 $P_n=(p_n,0)$，则 $Q_n=(p_n,p_n^2)$，并且 $p_1=1$。

抛物线 $y=x^2$ 在点 $(p_n,p_n^2)$ 处的切线方程为
$$
y-p_n^2=2p_n(x-p_n).
$$
令 $y=0$，得到它与 $x$ 轴的交点横坐标
$$
x=\frac{p_n}{2}.
$$
因而
$$
p_{n+1}=\frac{p_n}{2},\qquad p_1=1.
$$
解得
$$
p_n=2^{1-n}.
$$
所以
$$
\overline{OP_n}=p_n=2^{1-n}.
$$

又因为 $Q_nP_n$ 是竖直线段，所以
$$
\overline{Q_nP_n}=p_n^2=4^{1-n}.
$$
于是
$$
\sum_{n=1}^{\infty}\overline{Q_nP_n}
=\sum_{n=1}^{\infty}4^{1-n}
=\frac{1}{1-\frac14}=\frac43.
$$

### 第16题

- 答案：$f(t)=(1+4\pi t^2)e^{4\pi t^2}$

将积分项化为极坐标。由
$$
x=r\cos\theta,\qquad y=r\sin\theta,
$$
得
$$
\iint_{x^2+y^2\le4t^2}f\left(\frac12\sqrt{x^2+y^2}\right)dxdy
=\int_0^{2\pi}\int_0^{2t}f\left(\frac r2\right)r\,dr\,d\theta.
$$
令 $u=\frac r2$，则上式等于
$$
8\pi\int_0^t u f(u)\,du.
$$
所以原方程化为
$$
f(t)=e^{4\pi t^2}+8\pi\int_0^t u f(u)\,du.
$$
对 $t$ 求导，得
$$
f'(t)=8\pi t e^{4\pi t^2}+8\pi t f(t).
$$
即
$$
f'(t)-8\pi t f(t)=8\pi t e^{4\pi t^2}.
$$
两边乘以积分因子 $e^{-4\pi t^2}$，有
$$
\bigl(e^{-4\pi t^2}f(t)\bigr)'=8\pi t.
$$
积分得
$$
e^{-4\pi t^2}f(t)=4\pi t^2+C.
$$
又由原方程取 $t=0$ 得 $f(0)=1$，故 $C=1$。
因而
$$
f(t)=(1+4\pi t^2)e^{4\pi t^2}.
$$

### 第17题

- 答案：$\displaystyle PQ=\begin{pmatrix}A&\alpha\\0&|A|\bigl(b-\alpha^TA^{-1}\alpha\bigr)\end{pmatrix}$，且 $Q$ 可逆当且仅当 $\alpha^TA^{-1}\alpha\ne b$。

直接做分块矩阵乘法：
$$
PQ=
\begin{pmatrix}
E&0\\
-\alpha^TA^*&|A|
\end{pmatrix}
\begin{pmatrix}
A&\alpha\\
\alpha^T&b
\end{pmatrix}
=
\begin{pmatrix}
A&\alpha\\
-\alpha^TA^*A+|A|\alpha^T&-\alpha^TA^*\alpha+|A|b
\end{pmatrix}.
$$
因为 $A$ 非奇异，且 $A^*=|A|A^{-1}$，又有 $A^*A=|A|E$，所以
$$
-\alpha^TA^*A+|A|\alpha^T=0,
$$
$$
-\alpha^TA^*\alpha+|A|b=|A|\bigl(b-\alpha^TA^{-1}\alpha\bigr).
$$
因而
$$
PQ=\begin{pmatrix}
A&\alpha\\
0&|A|\bigl(b-\alpha^TA^{-1}\alpha\bigr)
\end{pmatrix}.
$$

又因为
$$
\det P=|A|\ne0,
$$
所以 $P$ 可逆，从而 $Q$ 可逆当且仅当 $PQ$ 可逆。由于 $PQ$ 是分块上三角矩阵，
$$
\det(PQ)=|A|\cdot |A|\bigl(b-\alpha^TA^{-1}\alpha\bigr).
$$
因为 $|A|\ne0$，故
$$
Q\text{ 可逆}\iff b-\alpha^TA^{-1}\alpha\ne0
\iff \alpha^TA^{-1}\alpha\ne b.
$$

### 第18题

- 答案：（1）属于特征值 $3$ 的特征向量可取 $\alpha_3=(1,0,1)^T$；（2）$\displaystyle A=\begin{pmatrix}\frac{13}{6}&-\frac13&\frac56\\-\frac13&\frac53&\frac13\\\frac56&\frac13&\frac{13}{6}\end{pmatrix}$。

因为 $A$ 是实对称矩阵，属于不同特征值的特征向量彼此正交。已知
$$
\alpha_1=(-1,-1,1)^T,\qquad \alpha_2=(1,-2,-1)^T,
$$
所以属于特征值 $3$ 的特征向量可取同时与它们都正交的向量。解方程
$$
\alpha_1^T\alpha_3=0,\qquad \alpha_2^T\alpha_3=0
$$
可取
$$
\alpha_3=(1,0,1)^T.
$$

由于 $\alpha_1,\alpha_2,\alpha_3$ 两两正交，可用谱分解
$$
A=\sum_{i=1}^3 \lambda_i\frac{\alpha_i\alpha_i^T}{\alpha_i^T\alpha_i},
\qquad \lambda_1=1,\ \lambda_2=2,\ \lambda_3=3.
$$
计算
$$
\alpha_1^T\alpha_1=3,\qquad \alpha_2^T\alpha_2=6,\qquad \alpha_3^T\alpha_3=2,
$$
于是
$$
A=
\frac13\alpha_1\alpha_1^T+\frac13\alpha_2\alpha_2^T+\frac32\alpha_3\alpha_3^T
=\begin{pmatrix}
\frac{13}{6} & -\frac13 & \frac56\\
-\frac13 & \frac53 & \frac13\\
\frac56 & \frac13 & \frac{13}{6}
\end{pmatrix}.
$$

### 第19题

- 答案：$\displaystyle F(x)=\begin{cases}0,&x<-1,\\\frac{5x+7}{16},&-1\le x<1,\\1,&x\ge1.\end{cases}$

已知
$$
P\{X=-1\}=\frac18,\qquad P\{X=1\}=\frac14,
$$
因而落在区间 $(-1,1)$ 内的概率为
$$
1-\frac18-\frac14=\frac58.
$$
又题设说明在条件事件 $\{-1<X<1\}$ 下，$X$ 在 $(-1,1)$ 上按长度成比例取值，所以条件分布是区间 $(-1,1)$ 上的均匀分布。
因此在 $(-1,1)$ 上的无条件密度为
$$
\frac58\cdot \frac12=\frac{5}{16}.
$$

于是分布函数分段为：
当 $x<-1$ 时，$F(x)=0$；
当 $-1\le x<1$ 时，
$$
F(x)=P\{X=-1\}+\int_{-1}^x\frac{5}{16}\,dt
=\frac18+\frac{5(x+1)}{16}
=\frac{5x+7}{16};
$$
当 $x\ge1$ 时，$F(x)=1$。

### 第20题

- 答案：$\displaystyle E(Y)=\frac{35}{3}\text{ 分钟}$

设游客到达时刻为 $X\sim U[0,60]$，等候时间记为 $Y$。根据电梯发车时刻，
$$
Y=\begin{cases}
5-X,&0\le X\le5,\\
25-X,&5<X\le25,\\
55-X,&25<X\le55,\\
65-X,&55<X\le60.
\end{cases}
$$
因为 $X$ 在 $[0,60]$ 上均匀分布，故
$$
E(Y)=\frac1{60}\left(\int_0^5(5-x)dx+\int_5^{25}(25-x)dx+\int_{25}^{55}(55-x)dx+\int_{55}^{60}(65-x)dx\right).
$$
分别计算得
$$
\int_0^5(5-x)dx=\frac{25}{2},\quad
\int_5^{25}(25-x)dx=200,
$$
$$
\int_{25}^{55}(55-x)dx=450,\quad
\int_{55}^{60}(65-x)dx=\frac{75}{2}.
$$
因而
$$
E(Y)=\frac{\frac{25}{2}+200+450+\frac{75}{2}}{60}
=\frac{700}{60}=\frac{35}{3}.
$$

### 第21题

- 答案：$\displaystyle f_T(t)=\begin{cases}25te^{-5t},&t>0,\\0,&t\le0,\end{cases}\qquad E(T)=\frac25,\qquad D(T)=\frac{2}{25}$

设两台记录仪各自无故障工作的时间分别为 $X_1,X_2$，则它们独立且都服从参数为 $5$ 的指数分布，密度为
$$
f_X(x)=\begin{cases}5e^{-5x},&x>0,\\0,&x\le0.\end{cases}
$$
总工作时间
$$
T=X_1+X_2.
$$
由卷积公式，当 $t>0$ 时，
$$
f_T(t)=\int_0^t 5e^{-5x}\cdot 5e^{-5(t-x)}\,dx
=25e^{-5t}\int_0^t dx
=25te^{-5t}.
$$
当 $t\le0$ 时显然 $f_T(t)=0$。

又因为指数分布的期望和方差分别为
$$
E(X_i)=\frac15,\qquad D(X_i)=\frac1{25},
$$
且 $X_1,X_2$ 独立，所以
$$
E(T)=E(X_1)+E(X_2)=\frac25,
$$
$$
D(T)=D(X_1)+D(X_2)=\frac{2}{25}.
$$
