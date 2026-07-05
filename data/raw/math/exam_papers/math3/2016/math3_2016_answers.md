# 2016 年考研数学三答案解析

资料类型：考研数学三答案解析
年份：2016
科目：数学三
整理状态：按答案页图人工校对并整理为正式题卡。

## 选择题

| 题号 | 答案 |
|---|---|
| 1 | B |
| 2 | D |
| 3 | B |
| 4 | A |
| 5 | C |
| 6 | C |
| 7 | A |
| 8 | C |

## 填空题

| 题号 | 答案 |
|---|---|
| 9 | $6$ |
| 10 | $\sin1-\cos1$ |
| 11 | $-dx+2dy$ |
| 12 | $\dfrac13-\dfrac2{3e}$ |
| 13 | $\lambda^4+\lambda^3+2\lambda^2+3\lambda+4$ |
| 14 | $\dfrac29$ |

## 解答题

| 题号 | 答案 |
|---|---|
| 15 | $e^{1/3}$ |
| 16 | 1. $Q=1200-10p$；2. 边际收益为 $80$ 万元，表示销售第 $201$ 件商品所增加的收益约为 $80$ 万元。 |
| 17 | $f'(x)= \begin{cases} 4x^2-2x, & 0<x\le1,\\ 2x, & x>1, \end{cases}$；最小值为 $\dfrac14$。 |
| 18 | $f(x)=-\dfrac12(e^x+e^{-x})$ |
| 19 | 收敛域为 $[-1,1]$； $f(x)= \begin{cases} (1+x)\ln(1+x)+(1-x)\ln(1-x), & x\in(-1,1),\\[4pt] 2\ln2, & x=\pm1. \end{cases}$ |
| 20 | $a=0$ $x=\begin{pmatrix}1\\-2\\0\end{pmatrix} +k\begin{pmatrix}0\\-1\\1\end{pmatrix},\quad k\in\mathbb R$ |
| 21 | $A^{99}= \begin{pmatrix} 2^{99}-2&1-2^{99}&2-2^{98}\\ 2^{100}-2&1-2^{100}&2-2^{99}\\ 0&0&0 \end{pmatrix}$ $\beta_1=(2^{99}-2)\alpha_1+(2^{100}-2)\alpha_2$ $\beta_2=(1-2^{99})\alpha_1+(1-2^{100})\alpha_2$ $\beta_3=(2-2^{98})\alpha_1+(2-2^{99})\alpha_2$ |
| 22 | 1. $f(x,y)= \begin{cases} 3,& (x,y)\in D,\\ 0,& \text{其他}; \end{cases}$；2. $U$ 与 $X$ 不独立；3. $F(z)= \begin{cases} 0,& z<0,\\[4pt] \dfrac32z^2-z^3,& 0\le z<1,\\[6pt] \dfrac12+2(z-1)^{3/2}-\dfrac32(z-1)^2,& 1\le z<2,\\[6pt] 1,& z\ge2. \end{cases}$ |
| 23 | 1. $f_T(z)= \begin{cases} \dfrac{9z^8}{\theta^9},& 0<z<\theta,\\ 0,& \text{其他}; \end{cases}$；2. $a=\dfrac{10}{9}$ |

## 详细解析

### 第 1 题

- 标准答案：B

由导函数 $f'(x)$ 的图形可知，$f'(x)=0$ 的点中，只有在 $x=a,\ x=c$ 处导数符号发生改变，因此 $f(x)$ 只有 $2$ 个极值点。

再看 $f'(x)$ 的单调性：在 $x=b$ 附近，$f'(x)$ 先减后增，因此 $f''(x)$ 变号，$(b,f(b))$ 为拐点；类似地，在 $x=e$ 与 $x=d$ 处，$f'(x)$ 的单调性也发生变化，所以对应地还有两个拐点。

因此曲线 $y=f(x)$ 有 $3$ 个拐点，选 B。

### 第 2 题

- 标准答案：D

计算偏导数：
$$
f'_x=\frac{e^x(x-y)-e^x}{(x-y)^2},\qquad
f'_y=\frac{e^x}{(x-y)^2}.
$$
故
$$
f'_x+f'_y=\frac{e^x(x-y)-e^x+e^x}{(x-y)^2}
=\frac{e^x}{x-y}=f.
$$
所以选 D。

### 第 3 题

- 标准答案：B

记
$$
D_4=\{(x,y)\mid 0\le x\le1,\ \sqrt x\le y\le1\},\qquad
D_5=\{(x,y)\mid 0\le x\le1,\ 0\le y\le x^2\},
$$
则
$$
D_2=D_1-D_4,\qquad D_3=D_1-D_5.
$$

因为 $D_1$ 关于直线 $y=x$ 对称，而
$$
\sqrt[3]{x-y}
$$
关于交换 $x,y$ 变号，所以
$$
J_1=0.
$$

在 $D_4$ 上有 $x-y<0$，故被积函数为负，从而
$$
J_2=J_1-\iint_{D_4}\sqrt[3]{x-y}\,dxdy>0.
$$
在 $D_5$ 上有 $x-y>0$，故
$$
J_3=J_1-\iint_{D_5}\sqrt[3]{x-y}\,dxdy<0.
$$
所以
$$
J_3<J_1<J_2.
$$
选 B。

### 第 4 题

- 标准答案：A

因为
$$
\left|\left(\frac1{\sqrt n}-\frac1{\sqrt{n+1}}\right)\sin(n+k)\right|
\le \frac1{\sqrt n}-\frac1{\sqrt{n+1}}.
$$
而正项级数
$$
\sum_{n=1}^{\infty}\left(\frac1{\sqrt n}-\frac1{\sqrt{n+1}}\right)
$$
为裂项级数，其部分和为
$$
1-\frac1{\sqrt{n+1}},
$$
故收敛。

由比较判别法，原级数绝对收敛。选 A。

### 第 5 题

- 标准答案：C

若
$$
P^{-1}AP=B,
$$
则有
$$
P^TA^T(P^T)^{-1}=B^T,
$$
故 A 正确。

又
$$
B^{-1}=P^{-1}A^{-1}P,
$$
故 B 正确。

并且
$$
P^{-1}(A+A^{-1})P=B+B^{-1},
$$
故 D 正确。

但一般并不能推出
$$
A+A^T \sim B+B^T,
$$
故错误的是 C。

### 第 6 题

- 标准答案：C

对应矩阵为
$$
A=\begin{pmatrix}
a&1&1\\
1&a&1\\
1&1&a
\end{pmatrix}.
$$
其特征值为
$$
a+2,\qquad a-1\ (\text{二重}).
$$

正、负惯性指数分别为 $1,2$，说明一个特征值为正，两个特征值为负，因此
$$
a+2>0,\qquad a-1<0.
$$
解得
$$
-2<a<1.
$$
故选 C。

### 第 7 题

- 标准答案：A

由
$$
P(A\mid B)=1
$$
得
$$
P(AB)=P(B),
$$
即 $B\subseteq A$（概率意义下）。

于是
$$
P(A\cup B)=P(A),
$$
从而
$$
P(\overline B\mid \overline A)
=\frac{P(\overline B\,\overline A)}{P(\overline A)}
=\frac{1-P(A\cup B)}{1-P(A)}
=1.
$$
故选 A。

### 第 8 题

- 标准答案：C

由独立性，
$$
D(XY)=E(X^2Y^2)-[E(XY)]^2=E(X^2)E(Y^2)-[E(X)E(Y)]^2.
$$
又
$$
E(X^2)=D(X)+[E(X)]^2=2+1=3,
$$
$$
E(Y^2)=D(Y)+[E(Y)]^2=4+1=5.
$$
故
$$
D(XY)=3\cdot5-1^2=14.
$$
选 C。

### 第 9 题

- 标准答案：$6$

当 $x\to0$ 时，
$$
\sqrt{1+f(x)\sin2x}-1\sim \frac12f(x)\sin2x,
$$
且
$$
\sin2x\sim2x,\qquad e^{3x}-1\sim3x.
$$
因此
$$
\lim_{x\to0}\frac{\frac12f(x)\sin2x}{3x}=2,
$$
即
$$
\lim_{x\to0}\frac{f(x)}3=2.
$$
故
$$
\lim_{x\to0}f(x)=6.
$$

### 第 10 题

- 标准答案：$\sin1-\cos1$

原式可写成
$$
\lim_{n\to\infty}\frac1n\left(\frac1n\sin\frac1n+\frac2n\sin\frac2n+\cdots+\frac nn\sin\frac nn\right),
$$
它是函数 $x\sin x$ 在 $[0,1]$ 上的黎曼和，因此极限等于
$$
\int_0^1 x\sin x\,dx.
$$
分部积分得
$$
\int_0^1 x\sin x\,dx
=-\int_0^1 x\,d(\cos x)
=-x\cos x\Big|_0^1+\int_0^1\cos x\,dx
=\sin1-\cos1.
$$

### 第 11 题

- 标准答案：$-dx+2dy$

对等式
$$
(x+1)z-y^2=x^2f(x-z,y)
$$
分别关于 $x,y$ 求偏导，可得
$$
z+(x+1)z_x'=2xf(x-z,y)+x^2f_1'(x-z,y)(1-z_x'),
$$
$$
(x+1)z_y'-2y=x^2\left[f_1'(x-z,y)(-z_y')+f_2'(x-z,y)\right].
$$
先由原方程在 $(x,y)=(0,1)$ 处得 $z=1$。再代入上两式得
$$
z_x'=-1,\qquad z_y'=2.
$$
因此
$$
dz\big|_{(0,1)}=z_x'dx+z_y'dy=-dx+2dy.
$$

### 第 12 题

- 标准答案：$\dfrac13-\dfrac2{3e}$

区域 $D$ 关于 $y$ 轴对称，记
$$
D_1=\{(x,y)\mid 0\le x\le1,\ x\le y\le1\}.
$$
则
$$
\iint_D x^2e^{-y^2}\,dxdy
=2\iint_{D_1}x^2e^{-y^2}\,dxdy
=2\int_0^1dy\int_0^y x^2e^{-y^2}\,dx.
$$
化简得
$$
=\frac23\int_0^1 y^3e^{-y^2}\,dy.
$$
令 $t=y^2$，则
$$
\frac23\int_0^1 y^3e^{-y^2}\,dy
=\frac13\int_0^1 te^{-t}\,dt
=\frac13-\frac2{3e}.
$$

### 第 13 题

- 标准答案：$\lambda^4+\lambda^3+2\lambda^2+3\lambda+4$

按最后一行展开：
$$
\begin{vmatrix}
\lambda-1&0&0&0\\
0&\lambda&-1&0\\
0&0&\lambda&-1\\
4&3&2&\lambda+1
\end{vmatrix}
$$
等于四个三阶行列式之和。逐项计算后可得
$$
\lambda^4+\lambda^3+2\lambda^2+3\lambda+4.
$$

### 第 14 题

- 标准答案：$\dfrac29$

取球次数恰好为 $4$，说明前 $3$ 次只取到了两种颜色，第 $4$ 次取到第三种颜色。

先选出前 $3$ 次出现的两种颜色，有
$$
\binom32=3
$$
种；在这两种颜色中排成长度为 $3$ 的序列且两种颜色都出现，有
$$
2^3-2=6
$$
种；第 $4$ 次只能取剩下那一种颜色。

故所求概率为
$$
\frac{3\times6}{3^4}=\frac29.
$$

### 第 15 题

- 标准答案：$e^{1/3}$

设极限为 $L$，则
$$
\ln L=\lim_{x\to0}\frac{\ln(\cos2x+2x\sin x)}{x^4}.
$$
这是 $0/0$ 型，可反复应用洛必达法则。按官方推导整理后可得
$$
\lim_{x\to0}\frac{\ln(\cos2x+2x\sin x)}{x^4}=\frac13.
$$
因此
$$
L=e^{1/3}.
$$

### 第 16 题

- 标准答案：1.
$$
Q=1200-10p;
$$
2. 边际收益为 $80$ 万元，表示销售第 $201$ 件商品所增加的收益约为 $80$ 万元。

由需求弹性的定义
$$
\eta=-\frac{p}{Q}\frac{dQ}{dp},
$$
以及题设
$$
\eta=\frac{p}{120-p},
$$
可得
$$
\frac{dQ}{Q}=-\frac{dp}{120-p}.
$$
积分得
$$
\ln Q=\ln(120-p)+C,
$$
即
$$
Q=C(120-p).
$$
又最大需求量为 $1200$，故 $C=10$，于是
$$
Q=1200-10p.
$$

销售收益
$$
R=pQ=p(1200-10p)=120Q-\frac1{10}Q^2.
$$
所以边际收益
$$
R'(Q)=120-\frac15Q.
$$
当 $p=100$ 时，
$$
Q=1200-10\times100=200,
$$
从而
$$
R'(200)=120-\frac15\cdot200=80.
$$
其经济意义是：在该点附近，销售再增加一件商品，收益约增加 $80$ 万元。

### 第 17 题

- 标准答案：$$
f'(x)=
\begin{cases}
4x^2-2x, & 0<x\le1,\\
2x, & x>1,
\end{cases}
$$
最小值为 $\dfrac14$。

当 $0<x\le1$ 时，
$$
f(x)=\int_0^x(x^2-t^2)\,dt+\int_x^1(t^2-x^2)\,dt
=\frac43x^3-x^2+\frac13.
$$

当 $x>1$ 时，
$$
f(x)=\int_0^1(x^2-t^2)\,dt=x^2-\frac13.
$$

因此
$$
f(x)=
\begin{cases}
\dfrac43x^3-x^2+\dfrac13, & 0<x\le1,\\[6pt]
x^2-\dfrac13, & x>1.
\end{cases}
$$
进而
$$
f'(x)=
\begin{cases}
4x^2-2x, & 0<x\le1,\\
2x, & x>1.
\end{cases}
$$

解 $f'(x)=0$ 得驻点 $x=\dfrac12$。比较可知它给出最小值，
$$
f\!\left(\frac12\right)=\frac14.
$$

### 第 18 题

- 标准答案：$f(x)=-\dfrac12(e^x+e^{-x})$

令
$$
u=x-t,
$$
则
$$
\int_0^x f(x-t)\,dt=\int_0^x f(u)\,du.
$$
题设化为
$$
\int_0^x f(u)\,du=x\int_0^x f(t)\,dt-\int_0^x tf(t)\,dt+e^{-x}-1.
$$
对 $x$ 求导，整理得
$$
f(x)=\int_0^x f(t)\,dt-e^{-x}.
$$
再对 $x$ 求导，得
$$
f'(x)-f(x)=e^{-x}.
$$
并由原式在 $x=0$ 处得
$$
f(0)=-1.
$$

解线性微分方程
$$
f'(x)-f(x)=e^{-x}
$$
得
$$
f(x)=Ce^x-\frac12e^{-x}.
$$
代入 $f(0)=-1$ 得 $C=-\dfrac12$，故
$$
f(x)=-\frac12(e^x+e^{-x}).
$$

### 第 19 题

- 标准答案：收敛域为 $[-1,1]$；

$$
f(x)=
\begin{cases}
(1+x)\ln(1+x)+(1-x)\ln(1-x), & x\in(-1,1),\\[4pt]
2\ln2, & x=\pm1.
\end{cases}
$$

用比值判别法，
$$
\lim_{n\to\infty}\left|\frac{x^{2n+4}}{(n+2)(2n+3)}\cdot\frac{(n+1)(2n+1)}{x^{2n+2}}\right|=x^2.
$$
故当 $|x|<1$ 时绝对收敛，当 $|x|>1$ 时发散。
又在 $x=\pm1$ 时，级数化为常数项正级数，也收敛，所以收敛域为
$$
[-1,1].
$$

设
$$
f(x)=\sum_{n=0}^{\infty}\frac{x^{2n+2}}{(n+1)(2n+1)}.
$$
逐项求导两次，得
$$
f''(x)=2\sum_{n=0}^{\infty}x^{2n}=\frac{2}{1-x^2}\qquad (|x|<1).
$$
又由 $f(0)=0,\ f'(0)=0$，积分可得
$$
f'(x)=\ln(1+x)-\ln(1-x),
$$
再积分得
$$
f(x)=(1+x)\ln(1+x)+(1-x)\ln(1-x).
$$
最后取端点极限可得
$$
f(1)=f(-1)=2\ln2.
$$

### 第 20 题

- 标准答案：$$
a=0;
$$

$$
x=\begin{pmatrix}1\\-2\\0\end{pmatrix}
+k\begin{pmatrix}0\\-1\\1\end{pmatrix},\quad k\in\mathbb R.
$$

对增广矩阵 $(A\mid\beta)$ 作初等行变换，可化为
$$
\begin{pmatrix}
1&1&1-a&0\\
1&0&a&1\\
a+1&1&a+1&2a-2
\end{pmatrix}
\to
\begin{pmatrix}
1&1&1-a&0\\
0&-1&2a-1&1\\
0&0&-a^2+2a&a-2
\end{pmatrix}.
$$
因 $Ax=\beta$ 无解，必须有
$$
-a^2+2a=0,\qquad a-2\ne0.
$$
解得
$$
a=0.
$$

此时
$$
A^TA=
\begin{pmatrix}
3&2&2\\
2&2&2\\
2&2&2
\end{pmatrix},\qquad
A^T\beta=
\begin{pmatrix}
-1\\-2\\-2
\end{pmatrix}.
$$
对增广矩阵 $(A^TA\mid A^T\beta)$ 化简，得
$$
\begin{pmatrix}
1&0&0&1\\
0&1&1&-2\\
0&0&0&0
\end{pmatrix}.
$$
故通解为
$$
x=\begin{pmatrix}1\\-2\\0\end{pmatrix}
+k\begin{pmatrix}0\\-1\\1\end{pmatrix},\quad k\in\mathbb R.
$$

### 第 21 题

- 标准答案：$$
A^{99}=
\begin{pmatrix}
2^{99}-2&1-2^{99}&2-2^{98}\\
2^{100}-2&1-2^{100}&2-2^{99}\\
0&0&0
\end{pmatrix};
$$

$$
\beta_1=(2^{99}-2)\alpha_1+(2^{100}-2)\alpha_2,
$$
$$
\beta_2=(1-2^{99})\alpha_1+(1-2^{100})\alpha_2,
$$
$$
\beta_3=(2-2^{98})\alpha_1+(2-2^{99})\alpha_2.
$$

先求特征多项式：
$$
|\lambda E-A|
=\begin{vmatrix}
\lambda&1&-1\\
-2&\lambda+3&0\\
0&0&\lambda
\end{vmatrix}
=\lambda(\lambda+1)(\lambda+2).
$$
故特征值为 $-1,-2,0$。

对应特征向量可取
$$
\xi_1=(1,1,0)^T,\quad
\xi_2=(1,2,0)^T,\quad
\xi_3=(3,2,2)^T.
$$
令
$$
P=(\xi_1,\xi_2,\xi_3),
$$
则
$$
P^{-1}AP=\operatorname{diag}(-1,-2,0).
$$
从而
$$
A^{99}=P\operatorname{diag}\bigl((-1)^{99},(-2)^{99},0\bigr)P^{-1},
$$
计算即得
$$
A^{99}=
\begin{pmatrix}
2^{99}-2&1-2^{99}&2-2^{98}\\
2^{100}-2&1-2^{100}&2-2^{99}\\
0&0&0
\end{pmatrix}.
$$

又由
$$
B^2=BA
$$
可反复推出
$$
B^{100}=BA^{99}.
$$
若记
$$
B=(\alpha_1,\alpha_2,\alpha_3),
$$
则
$$
B^{100}=(\alpha_1,\alpha_2,\alpha_3)A^{99}.
$$
因此读取矩阵 $A^{99}$ 的各列即可得到
$$
\beta_1=(2^{99}-2)\alpha_1+(2^{100}-2)\alpha_2,
$$
$$
\beta_2=(1-2^{99})\alpha_1+(1-2^{100})\alpha_2,
$$
$$
\beta_3=(2-2^{98})\alpha_1+(2-2^{99})\alpha_2.
$$

### 第 22 题

- 标准答案：1.
$$
f(x,y)=
\begin{cases}
3,& (x,y)\in D,\\
0,& \text{其他};
\end{cases}
$$
2. $U$ 与 $X$ 不独立；  
3.
$$
F(z)=
\begin{cases}
0,& z<0,\\[4pt]
\dfrac32z^2-z^3,& 0\le z<1,\\[6pt]
\dfrac12+2(z-1)^{3/2}-\dfrac32(z-1)^2,& 1\le z<2,\\[6pt]
1,& z\ge2.
\end{cases}
$$

先求区域面积：
$$
|D|=\int_0^1(\sqrt x-x^2)\,dx=\frac13,
$$
故均匀分布密度为常数 $3$。

对任意 $0<t<1$，
$$
P(U=0,X\le t)=P(X>Y,\ X\le t)=\int_0^t dx\int_{x^2}^x 3\,dy=\frac32t^2-t^3.
$$
而
$$
P(U=0)=P(X>Y)=\frac12,
$$
$$
P(X\le t)=\int_0^t dx\int_{x^2}^{\sqrt x}3\,dy=2t^{3/2}-t^3.
$$
一般有
$$
P(U=0,X\le t)\ne P(U=0)P(X\le t),
$$
故 $U$ 与 $X$ 不独立。

下面求 $Z=U+X$ 的分布函数。

当 $z<0$ 时，$F(z)=0$。

当 $0\le z<1$ 时，必有 $U=0$，所以
$$
F(z)=P(U+X\le z)=P(U=0,X\le z)=\frac32z^2-z^3.
$$

当 $1\le z<2$ 时，
$$
F(z)=P(U=0,X\le z)+P(U=1,X\le z-1).
$$
其中
$$
P(U=0,X\le z)=P(U=0)=\frac12,
$$
且
$$
P(U=1,X\le z-1)=\int_0^{z-1}dx\int_x^{\sqrt x}3\,dy
=2(z-1)^{3/2}-\frac32(z-1)^2.
$$
故
$$
F(z)=\frac12+2(z-1)^{3/2}-\frac32(z-1)^2.
$$

当 $z\ge2$ 时，$F(z)=1$。

### 第 23 题

- 标准答案：1.
$$
f_T(z)=
\begin{cases}
\dfrac{9z^8}{\theta^9},& 0<z<\theta,\\
0,& \text{其他};
\end{cases}
$$
2.
$$
a=\dfrac{10}{9}.
$$

先求总体分布函数：
$$
F(x)=
\begin{cases}
0,& x<0,\\[4pt]
\dfrac{x^3}{\theta^3},& 0\le x<\theta,\\[6pt]
1,& x\ge\theta.
\end{cases}
$$
于是
$$
F_T(z)=P(T\le z)=[F(z)]^3
=
\begin{cases}
0,& z<0,\\[4pt]
\dfrac{z^9}{\theta^9},& 0\le z<\theta,\\[6pt]
1,& z\ge\theta.
\end{cases}
$$
故密度为
$$
f_T(z)=
\begin{cases}
\dfrac{9z^8}{\theta^9},& 0<z<\theta,\\
0,& \text{其他}.
\end{cases}
$$

进一步
$$
E(T)=\int_0^\theta z\cdot \frac{9z^8}{\theta^9}\,dz
=\frac{9}{10}\theta.
$$
若要
$$
E(aT)=\theta,
$$
则需
$$
a\cdot\frac{9}{10}\theta=\theta,
$$
故
$$
a=\frac{10}{9}.
$$
