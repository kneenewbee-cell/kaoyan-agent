# 2011 年数学三答案解析

资料类型：考研数学三答案解析
年份：2011
科目：数学三
整理状态：按答案页视觉核对后人工清洗整理。

## 选择题

| 题号 | 答案 |
|---|---|
| 1 | C |
| 2 | B |
| 3 | A |
| 4 | B |
| 5 | D |
| 6 | C |
| 7 | D |
| 8 | D |

## 填空题

| 题号 | 答案 |
|---|---|
| 9 | $e^{3x}(1+3x)$ |
| 10 | $(1+2\ln2)(dx-dy)$ |
| 11 | $y=-2x$ |
| 12 | $\dfrac{4\pi}{3}$ |
| 13 | $3y_1^2$ |
| 14 | $\mu(\mu^2+\sigma^2)$ |

## 解答题

| 题号 | 答案 |
|---|---|
| 15 | $-\dfrac12$ |
| 16 | $f_{11}''(2,2)+f_2'(2,2)\,f_{12}''(1,1)$ |
| 17 | $2\sqrt{x}\arcsin\sqrt{x}+2\sqrt{x}\ln x+2\sqrt{1-x}-4\sqrt{x}+C$ |
| 18 | 方程恰有两个实根 |
| 19 | $f(x)=\dfrac{4}{(x-2)^2}\ (0\le x\le1)$ |
| 20 | (I)\ $a=5$；(II)\ $\beta_1=2\alpha_1+4\alpha_2-\alpha_3,\quad \beta_2=\alpha_1+2\alpha_2,\quad \beta_3=5\alpha_1+10\alpha_2-2\alpha_3$ |
| 21 | 特征值为 $-1,1,0$；对应特征向量可取 $(1,0,-1)^T,\ (1,0,1)^T,\ (0,1,0)^T$；并且 $A= \begin{pmatrix} 0&0&1\\ 0&0&0\\ 1&0&0 \end{pmatrix}$ |
| 22 | $\begin{array}{cccc} & -1 & 0 & 1\\ \hline X=0 & 0 & \frac13 & 0\\ X=1 & \frac13 & 0 & \frac13 \end{array}$ $P(Z=-1)=\frac13,\quad P(Z=0)=\frac13,\quad P(Z=1)=\frac13$ $\rho_{XY}=0$ |
| 23 | $f_X(x)= \begin{cases} x, & 0<x<1,\\ 2-x, & 1\le x<2,\\ 0, & \text{其他}. \end{cases}$ $f_{X\mid Y}(x\mid y)= \begin{cases} \dfrac1{2-2y}, & y<x<2-y,\ 0<y<1,\\ 0, & \text{其他}. \end{cases}$ |

## 详细解析

### 第 1 题

- 答案：C

利用恒等变形
$$
3\sin x-\sin 3x
=3\sin x-\sin x\cos 2x-\cos x\sin 2x
=\sin x\bigl(3-\cos 2x-2\cos^2x\bigr).
$$
再用 $\cos 2x=2\cos^2x-1$，得
$$
3-\cos 2x-2\cos^2x=4-4\cos^2x=4\sin^2x.
$$
因此
$$
3\sin x-\sin 3x\sim 4x^3 \quad (x\to0).
$$
故 $k=3,\ c=4$，选 C。

### 第 2 题

- 答案：B

因为 $f(0)=0$，
$$
\frac{x^2f(x)-2f(x^3)}{x^3}
=\frac{f(x)-f(0)}{x}-2\cdot\frac{f(x^3)-f(0)}{x^3}.
$$
当 $x\to0$ 时，第一项趋于 $f'(0)$，第二项也趋于 $2f'(0)$，故极限为
$$
f'(0)-2f'(0)=-f'(0).
$$
选 B。

### 第 3 题

- 答案：A

收敛级数任意加括号后仍收敛，因此 A 正确。

B 错：取 $u_n=(-1)^n$，则
$$
u_{2n-1}+u_{2n}=0,
$$
故分组后的级数收敛，但原级数 $\sum (-1)^n$ 发散。

C 错：取 $u_n=\dfrac{(-1)^{n-1}}{n}$，则 $\sum u_n$ 收敛，但
$$
\sum_{n=1}^{\infty}(u_{2n-1}-u_{2n})
=\sum_{n=1}^{\infty}\frac1n
$$
发散。

D 错：取 $u_n=1$，则 $\sum(u_{2n-1}-u_{2n})=0$ 收敛，而 $\sum u_n$ 发散。

### 第 4 题

- 答案：B

当 $0<x<\dfrac{\pi}{4}$ 时，
$$
0<\sin x<\cos x<1<\cot x.
$$
由于 $\ln x$ 单调递增，所以
$$
\ln(\sin x)<\ln(\cos x)<\ln(\cot x).
$$
在同一区间上积分后得到
$$
I<K<J.
$$
故选 B。

### 第 5 题

- 答案：D

将第 2 列加到第 1 列可写成
$$
AP_1=B,
$$
所以
$$
A=BP_1^{-1}.
$$
又由交换 $B$ 的第 2、3 行得到单位矩阵，可写成
$$
P_2B=E,
$$
即
$$
B=P_2^{-1}=P_2.
$$
故
$$
A=P_2P_1^{-1}.
$$
选 D。

### 第 6 题

- 答案：C

因为 $\eta_1,\eta_2,\eta_3$ 都是 $Ax=\beta$ 的解，所以
$$
\eta_2-\eta_1,\ \eta_3-\eta_1
$$
都是齐次方程 $Ax=0$ 的解，并且线性无关。故它们构成 $Ax=0$ 的一个基础解系。

又因为
$$
A\left(\frac{\eta_2+\eta_3}{2}\right)=\frac{\beta+\beta}{2}=\beta,
$$
所以 $\dfrac{\eta_2+\eta_3}{2}$ 是一个特解。

因此非齐次方程组的通解为
$$
\frac{\eta_2+\eta_3}{2}+k_1(\eta_2-\eta_1)+k_2(\eta_3-\eta_1).
$$
选 C。

### 第 7 题

- 答案：D

对选项 D，有
$$
\int_{-\infty}^{+\infty}\bigl[f_1(x)F_2(x)+f_2(x)F_1(x)\bigr]\,dx
=\int_{-\infty}^{+\infty}d\bigl(F_1(x)F_2(x)\bigr)=1.
$$
且该函数非负，因此它是概率密度。
故选 D。

### 第 8 题

- 答案：D

因为 $X_i\sim P(\lambda)$，故
$$
E(X_i)=\lambda,\qquad D(X_i)=\lambda.
$$
于是
$$
E(T_1)=\lambda,
\qquad
E(T_2)=\frac1{n-1}(n-1)\lambda+\frac1n\lambda
=\left(1+\frac1n\right)\lambda,
$$
所以 $E(T_1)<E(T_2)$。

又
$$
D(T_1)=\frac1{n^2}\cdot n\lambda=\frac{\lambda}{n},
$$
$$
D(T_2)=\frac1{(n-1)^2}\cdot(n-1)\lambda+\frac1{n^2}\lambda
=\left(\frac1{n-1}+\frac1{n^2}\right)\lambda.
$$
当 $n\ge2$ 时，
$$
\frac1n<\frac1{n-1}+\frac1{n^2},
$$
故 $D(T_1)<D(T_2)$。选 D。

### 第 9 题

- 答案：$e^{3x}(1+3x)$

由
$$
\lim_{t\to0}(1+3t)^{1/(3t)}=e
$$
可得
$$
f(x)=x\lim_{t\to0}\left[(1+3t)^{1/(3t)}\right]^{3x}=xe^{3x}.
$$
故
$$
f'(x)=e^{3x}+3xe^{3x}=e^{3x}(1+3x).
$$

### 第 10 题

- 答案：$(1+2\ln2)(dx-dy)$

写成
$$
z=\exp\!\left[\frac{x}{y}\ln\!\left(1+\frac{x}{y}\right)\right].
$$
计算偏导并代入 $(1,1)$，得
$$
\left.\frac{\partial z}{\partial x}\right|_{(1,1)}=1+2\ln2,
\qquad
\left.\frac{\partial z}{\partial y}\right|_{(1,1)}=-1-2\ln2.
$$
因此
$$
dz\big|_{(1,1)}=(1+2\ln2)\,dx-(1+2\ln2)\,dy=(1+2\ln2)(dx-dy).
$$

### 第 11 题

- 答案：$y=-2x$

对方程两端对 $x$ 求导：
$$
\sec^2\left(x+y+\frac{\pi}{4}\right)(1+y')=e^y y'.
$$
代入 $(x,y)=(0,0)$，有
$$
\frac{1+y'}{\cos^2(\pi/4)}=y',
$$
即
$$
2(1+y')=y',
$$
解得 $y'=-2$。故切线方程为
$$
y=-2x.
$$

### 第 12 题

- 答案：$\dfrac{4\pi}{3}$

由几何关系可知积分区间为 $x\in[1,2]$，旋转体体积
$$
V=\pi\int_1^2 y^2\,dx
=\pi\int_1^2(x^2-1)\,dx
=\pi\left[\frac{x^3}{3}-x\right]_1^2
=\frac{4\pi}{3}.
$$

### 第 13 题

- 答案：$3y_1^2$

由 $A$ 的各行元素之和都等于 3，知
$$
A
\begin{pmatrix}
1\\1\\1
\end{pmatrix}
=3
\begin{pmatrix}
1\\1\\1
\end{pmatrix},
$$
因此 3 是 $A$ 的一个特征值。

又因 $r(A)=1$，所以其余特征值都为 0。正交变换下二次型的标准形系数就是特征值，故标准形为
$$
3y_1^2.
$$

### 第 14 题

- 答案：$\mu(\mu^2+\sigma^2)$

相关系数为 0，因此在二维正态分布下 $X,Y$ 相互独立。于是
$$
E(XY^2)=E(X)E(Y^2).
$$
又
$$
E(X)=\mu,\qquad E(Y^2)=D(Y)+[E(Y)]^2=\sigma^2+\mu^2.
$$
故
$$
E(XY^2)=\mu(\mu^2+\sigma^2).
$$

### 第 15 题

- 答案：$-\dfrac12$

由于
$$
x\ln(1+x)\sim x^2 \quad (x\to0),
$$
原极限可化为
$$
\lim_{x\to0}\frac{\sqrt{1+2\sin x}-x-1}{x^2}.
$$
分子分母同趋于 0，连续使用洛必达法则：
$$
\lim_{x\to0}\frac{\dfrac{\cos x}{\sqrt{1+2\sin x}}-1}{2x}
=\lim_{x\to0}\frac{-\sin x-\dfrac{\cos^2x}{\sqrt{1+2\sin x}}}{2\sqrt{1+2\sin x}}
=-\frac12.
$$
故所求极限为
$$
-\frac12.
$$

### 第 16 题

- 答案：$f_{11}''(2,2)+f_2'(2,2)\,f_{12}''(1,1)$

设
$$
u=x+y,\qquad v=f(x,y),
$$
则
$$
z=f(u,v).
$$
先对 $x$ 求偏导：
$$
\frac{\partial z}{\partial x}=f_1'(u,v)\frac{\partial u}{\partial x}+f_2'(u,v)\frac{\partial v}{\partial x}
=f_1'(u,v)+f_2'(u,v)f_x'(x,y).
$$
再对 $y$ 求偏导，并在 $(1,1)$ 处代入。由于 $f(1,1)=2$ 是极值点，所以
$$
f_1'(1,1)=f_2'(1,1)=0.
$$
于是化简得
$$
\left.\frac{\partial^2 z}{\partial x\,\partial y}\right|_{(1,1)}
=f_{11}''(2,2)+f_2'(2,2)\,f_{12}''(1,1).
$$

### 第 17 题

- 答案：$2\sqrt{x}\arcsin\sqrt{x}+2\sqrt{x}\ln x+2\sqrt{1-x}-4\sqrt{x}+C$

令
$$
t=\sqrt{x},
$$
则 $x=t^2,\ dx=2t\,dt$，原积分化为
$$
2\int(\arcsin t+\ln t^2)\,dt.
$$
分别积分：
$$
2\int \arcsin t\,dt
=2\left(t\arcsin t+\sqrt{1-t^2}\right),
$$
$$
2\int \ln t^2\,dt
=4\int \ln t\,dt
=4(t\ln t-t).
$$
合并并代回 $t=\sqrt{x}$，得
$$
2\sqrt{x}\arcsin\sqrt{x}+2\sqrt{x}\ln x+2\sqrt{1-x}-4\sqrt{x}+C.
$$

### 第 18 题

- 答案：方程恰有两个实根

设
$$
f(x)=4\arctan x-x+\frac{4\pi}{3}-\sqrt{3}.
$$
则
$$
f'(x)=\frac{4}{1+x^2}-1=\frac{(\sqrt3-x)(\sqrt3+x)}{1+x^2}.
$$
所以：
$$
f'(x)<0\ (x<-\sqrt3),\quad
f'(x)>0\ (-\sqrt3<x<\sqrt3),\quad
f'(x)<0\ (x>\sqrt3).
$$
故 $f$ 先减后增再减。

又
$$
f(-\sqrt3)=0,
$$
并且
$$
f(\sqrt3)=\frac{8\pi}{3}-2\sqrt3>0,\qquad
\lim_{x\to+\infty}f(x)=-\infty.
$$
因此在 $(-\infty,\sqrt3)$ 上只有一个零点 $x=-\sqrt3$，在 $(\sqrt3,+\infty)$ 上还有且仅有一个零点。
故原方程恰有两个实根。

### 第 19 题

- 答案：$f(x)=\dfrac{4}{(x-2)^2}\ (0\le x\le1)$

先计算右端：
$$
\iint_{D_t}f(t)\,dxdy=\frac12 t^2f(t).
$$
左端有
$$
\iint_{D_t}f'(x+y)\,dxdy
=\int_0^t\int_0^{t-x}f'(x+y)\,dy\,dx
=\int_0^t\bigl(f(t)-f(x)\bigr)\,dx
=tf(t)-\int_0^t f(x)\,dx.
$$
因此
$$
tf(t)-\int_0^t f(x)\,dx=\frac12 t^2f(t).
$$
两边对 $t$ 求导，整理得
$$
(2-t)f'(t)=2f(t).
$$
这是可分离变量方程，解得
$$
f(t)=\frac{C}{(t-2)^2}.
$$
由 $f(0)=1$ 得 $C=4$。故
$$
f(x)=\frac{4}{(x-2)^2},\qquad 0\le x\le1.
$$

### 第 20 题

- 答案：(I)\ $a=5$；

(II)\ 
$$
\beta_1=2\alpha_1+4\alpha_2-\alpha_3,\quad
\beta_2=\alpha_1+2\alpha_2,\quad
\beta_3=5\alpha_1+10\alpha_2-2\alpha_3.
$$

把两组向量并排写成矩阵并做行变换。由“$\alpha_1,\alpha_2,\alpha_3$ 不能由 $\beta_1,\beta_2,\beta_3$ 线性表示”知，把 $\alpha$ 组并入 $\beta$ 组后秩会增加。

对
$$
(\beta_1,\beta_2,\beta_3,\alpha_1,\alpha_2,\alpha_3)
$$
作初等行变换，可化到含有主元 $a-5$ 的形式，因此只有当
$$
a=5
$$
时，$\alpha$ 组不能由 $\beta$ 组线性表示。

再对
$$
(\alpha_1,\alpha_2,\alpha_3,\beta_1,\beta_2,\beta_3)
$$
作行变换，可读出表示系数：
$$
\beta_1=2\alpha_1+4\alpha_2-\alpha_3,
$$
$$
\beta_2=\alpha_1+2\alpha_2,
$$
$$
\beta_3=5\alpha_1+10\alpha_2-2\alpha_3.
$$

### 第 21 题

- 答案：特征值为 $-1,1,0$；

对应特征向量可取
$$
(1,0,-1)^T,\ (1,0,1)^T,\ (0,1,0)^T.
$$

并且
$$
A=
\begin{pmatrix}
0&0&1\\
0&0&0\\
1&0&0
\end{pmatrix}.
$$

由题设可知
$$
A(1,0,-1)^T=-(1,0,-1)^T,\qquad
A(1,0,1)^T=(1,0,1)^T.
$$
因此 $-1,1$ 是 $A$ 的两个特征值，对应特征向量分别可取
$$
\alpha_1=(1,0,-1)^T,\qquad \alpha_2=(1,0,1)^T.
$$

又因 $r(A)=2$，故第三个特征值为 0。由于 $A$ 是实对称矩阵，不同特征值的特征向量两两正交，所以对应 0 的特征向量可取
$$
\alpha_3=(0,1,0)^T.
$$

单位化后取
$$
\beta_1=\frac1{\sqrt2}(1,0,-1)^T,\quad
\beta_2=\frac1{\sqrt2}(1,0,1)^T,\quad
\beta_3=(0,1,0)^T.
$$
令
$$
Q=(\beta_1,\beta_2,\beta_3),
\qquad
\Lambda=\operatorname{diag}(-1,1,0),
$$
则
$$
A=Q\Lambda Q^T
=
\begin{pmatrix}
0&0&1\\
0&0&0\\
1&0&0
\end{pmatrix}.
$$

### 第 22 题

- 答案：$$
\begin{array}{c|ccc}
 & -1 & 0 & 1\\ \hline
X=0 & 0 & \frac13 & 0\\
X=1 & \frac13 & 0 & \frac13
\end{array}
$$

$$
P(Z=-1)=\frac13,\quad P(Z=0)=\frac13,\quad P(Z=1)=\frac13.
$$

$$
\rho_{XY}=0.
$$

由
$$
P\{X^2=Y^2\}=1
$$
可知不可能出现
$$
(X,Y)=(0,-1),(0,1),(1,0),
$$
这些情形的概率都为 0。

再由边缘分布得
$$
P(X=0,Y=0)=P(X=0)=\frac13,
$$
$$
P(X=1,Y=-1)=P(Y=-1)=\frac13,
$$
$$
P(X=1,Y=1)=P(Y=1)=\frac13.
$$
因此联合分布如答案所示。

因为 $Z=XY$，故其可能值为 $-1,0,1$，且三者概率都为 $\dfrac13$。

又
$$
E(XY)=(-1)\cdot\frac13+0\cdot\frac13+1\cdot\frac13=0,
$$
$$
E(Y)=(-1)\cdot\frac13+0\cdot\frac13+1\cdot\frac13=0.
$$
所以
$$
\operatorname{Cov}(X,Y)=E(XY)-E(X)E(Y)=0,
$$
从而
$$
\rho_{XY}=0.
$$

### 第 23 题

- 答案：$$
f_X(x)=
\begin{cases}
x, & 0<x<1,\\
2-x, & 1\le x<2,\\
0, & \text{其他}.
\end{cases}
$$

$$
f_{X\mid Y}(x\mid y)=
\begin{cases}
\dfrac1{2-2y}, & y<x<2-y,\ 0<y<1,\\
0, & \text{其他}.
\end{cases}
$$

三角形区域
$$
G=\{(x,y)\mid 0<y<1,\ y<x<2-y\}
$$
面积为 1，因此联合密度为
$$
f(x,y)=
\begin{cases}
1, & 0<y<1,\ y<x<2-y,\\
0, & \text{其他}.
\end{cases}
$$

对 $y$ 积分可得边缘密度：
当 $0<x<1$ 时，$0<y<x$，所以
$$
f_X(x)=\int_0^x1\,dy=x.
$$
当 $1\le x<2$ 时，$0<y<2-x$，所以
$$
f_X(x)=\int_0^{2-x}1\,dy=2-x.
$$
其余情形为 0。

再求 $Y$ 的边缘密度：
$$
f_Y(y)=\int_y^{2-y}1\,dx=2-2y,\qquad 0<y<1.
$$
因此条件密度为
$$
f_{X\mid Y}(x\mid y)=\frac{f(x,y)}{f_Y(y)}
=
\begin{cases}
\dfrac1{2-2y}, & y<x<2-y,\ 0<y<1,\\
0, & \text{其他}.
\end{cases}
$$
