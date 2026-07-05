# 2022 数学一答案解析

资料类型：考研数学一答案解析
年份：2022
科目：数学一
整理状态：已根据答案页图像、题图与题干推导清洗

## 答案速查

### 选择题

| 题号 | 答案 |
|---|---|
| 1 | B |
| 2 | B |
| 3 | D |
| 4 | A |
| 5 | A |
| 6 | C |
| 7 | C |
| 8 | C |
| 9 | A |
| 10 | D |

### 填空题

| 题号 | 答案 |
|---|---|
| 11 | $4$ |
| 12 | $4$ |
| 13 | $[4e^{-2},+\infty)$ |
| 14 | $-1$ |
| 15 | $-E$ |
| 16 | $\dfrac{5}{8}$ |

### 解答题

| 题号 | 答案要点 |
|---|---|
| 17 | $y=2x$ 是曲线 $y=y(x)$ 的唯一斜渐近线。 |
| 18 | $I=2\pi-2$。 |
| 19 | $I=0$。 |
| 20 | 证明见解析。 |
| 21 | (I) $$ A=\begin{pmatrix} 1&2&3\\ 2&4&6\\ 3&6&9 \end{pmatrix}. $$  (II) 可取 $$ Q=\begin{pmatrix} \frac{1}{\sqrt{14}}&-\frac{2}{\sqrt{5}}&-\frac{3}{\sqrt{70}}\\ \frac{2}{\sqrt{14}}& \frac{1}{\sqrt{5}}&-\frac{6}{\sqrt{70}}\\ \frac{3}{\sqrt{14}}&0&\frac{5}{\sqrt{70}} \end{pmatrix}, $$ 标准形为 $$ 14y_1^2. $$  (III) $$ x=k_1(-2,1,0)^T+k_2(-3,-6,5)^T,\qquad k_1,k_2\in\mathbb R. $$ |
| 22 | 最大似然估计量为 $$ \hat\theta=\frac{2\sum_{i=1}^nX_i+\sum_{j=1}^mY_j}{2(n+m)}. $$ 且 $$ D(\hat\theta)=\frac{\theta^2}{n+m}. $$ |

## 详细解析

### 第 1 题

**答案：** B

因为 $\ln x\to0$ 且
$$
\frac{f(x)}{\ln x}\to1,
$$
所以
$$
f(x)=\ln x\cdot\frac{f(x)}{\ln x}\to0.
$$
题设没有说明 $f(1)$ 的取值，也不能推出 $f'(1)$ 或 $f'(x)$ 的极限，故选 B。

### 第 2 题

**答案：** B

令 $u=y/x$，则
$$
z=x^2u f(u)
$$
是关于 $(x,y)$ 的二次齐次结构。直接求 Euler 导数得
$$
xz_x+yz_y=2xy f(u).
$$
又
$$
y^2(\ln y-\ln x)=y^2\ln\frac{y}{x}=x^2u^2\ln u,
$$
所以
$$
2x^2u f(u)=x^2u^2\ln u,\qquad
f(u)=\frac{1}{2}u\ln u.
$$
于是
$$
f(1)=0,\qquad f'(u)=\frac{1}{2}(\ln u+1),\qquad f'(1)=\frac{1}{2}.
$$
故选 B。

### 第 3 题

**答案：** D

因为 $\cos x_n\in[0,1]$，而 $\sin t$ 在 $[0,1]$ 上严格单调，所以 $\sin(\cos x_n)$ 收敛可推出 $\cos x_n$ 收敛。

但 $\cos x_n$ 收敛不能推出 $x_n$ 收敛。例如 $x_n=(-1)^na$，其中 $0<a<\pi/2$，则 $\cos x_n=\cos a$ 恒定，而 $x_n$ 不收敛。

另一方面，$\cos t$ 在 $[-1,1]$ 上不是一一对应，$\cos(\sin x_n)$ 收敛不能保证 $\sin x_n$ 收敛。故选 D。

### 第 4 题

**答案：** A

当 $0<x<1$ 时，
$$
\ln(1+x)>\frac{x}{1+x}>\frac{x}{2},
$$
且 $1+\cos x>0$，故 $I_1<I_2$。

又 $\ln(1+x)<x$，并且在 $0<x<1$ 上
$$
1+\sin x<2(1+\cos x).
$$
于是
$$
\frac{\ln(1+x)}{1+\cos x}
<\frac{x}{1+\cos x}
<\frac{2x}{1+\sin x}.
$$
因此 $I_2<I_3$，故
$$
I_1<I_2<I_3.
$$
选 A。

### 第 5 题

**答案：** A

$n$ 阶矩阵可对角化的充要条件是有 $n$ 个线性无关的特征向量，因此 B 是充要条件，不是“充分但不必要”。

若 $3$ 阶矩阵有 $3$ 个互不相同的特征值，则对应特征向量线性无关，矩阵可对角化，所以 A 充分。可对角化矩阵也可能有重特征值，例如单位矩阵，所以 A 不必要。

C 中“两两线性无关”不能保证三向量整体线性无关；D 不是一般矩阵可对角化的充分条件。故选 A。

### 第 6 题

**答案：** C

设未知向量 $y=(u^T,v^T)^T$。对选项 C 的第一个方程组，
$$
Au+Bv=0,\qquad Bv=0.
$$
因 $Ax=0$ 与 $Bx=0$ 同解，由 $Bv=0$ 得 $Av=0$；再由 $Au+Bv=0$ 得 $Au=0$，从而 $Bu=0$。因此
$$
Bu+Av=0,\qquad Av=0,
$$
即满足选项 C 的第二个方程组。

反向推理完全相同，所以两方程组同解，选 C。

### 第 7 题

**答案：** C

记
$$
M_3=(\alpha_1,\alpha_2,\alpha_3),\qquad
M_4=(\alpha_1,\alpha_2,\alpha_4).
$$
计算得
$$
\det M_3=(\lambda-1)^2(\lambda+2),\qquad
\det M_4=(\lambda-1)^2(\lambda+1)^2.
$$
当 $\lambda\ne1,-1,-2$ 时，两矩阵均满秩，两个向量组都张成 $\mathbb R^3$，故等价。

当 $\lambda=1$ 时，四个向量均为 $(1,1,1)^T$，两个向量组仍等价。

当 $\lambda=-2$ 时，$M_3$ 不满秩而 $M_4$ 满秩；当 $\lambda=-1$ 时，$M_3$ 满秩而 $M_4$ 不满秩，均不等价。故选 C。

### 第 8 题

**答案：** C

有
$$
D(X)=\frac{(3-0)^2}{12}=\frac{3}{4},\qquad D(Y)=2,\qquad \operatorname{Cov}(X,Y)=-1.
$$
因此
$$
\begin{aligned}
D(2X-Y+1)
&=4D(X)+D(Y)-4\operatorname{Cov}(X,Y)\\
&=4\cdot\frac{3}{4}+2-4(-1)\\
&=9.
\end{aligned}
$$
故选 C。

### 第 9 题

**答案：** A

令 $Z_i=X_i^2$，则
$$
E(Z_i)=\mu_2,\qquad D(Z_i)=E(X_i^4)-[E(X_i^2)]^2=\mu_4-\mu_2^2.
$$
由于 $Z_i$ 独立同分布，
$$
D\left(\frac{1}{n}\sum_{i=1}^nZ_i\right)=\frac{\mu_4-\mu_2^2}{n}.
$$
由切比雪夫不等式得
$$
P\left\{\left|\frac{1}{n}\sum_{i=1}^nX_i^2-\mu_2\right|\ge\varepsilon\right\}
\le\frac{\mu_4-\mu_2^2}{n\varepsilon^2}.
$$
故选 A。

### 第 10 题

**答案：** D

由条件分布可知
$$
E(Y\mid X)=X,\qquad D(Y\mid X)=1.
$$
因此
$$
E(Y)=E[E(Y\mid X)]=0,
$$
$$
D(Y)=D[E(Y\mid X)]+E[D(Y\mid X)]=D(X)+1=2.
$$
又
$$
\operatorname{Cov}(X,Y)=\operatorname{Cov}(X,E(Y\mid X))=\operatorname{Cov}(X,X)=1.
$$
故相关系数为
$$
\rho_{XY}=\frac{1}{\sqrt{D(X)D(Y)}}=\frac{1}{\sqrt{2}}=\frac{\sqrt{2}}{2}.
$$
选 D。

### 第 11 题

**答案：** $4$

函数在一点的最大方向导数等于梯度的模。因为
$$
\nabla f=(2x,4y),
$$
所以
$$
\nabla f(0,1)=(0,4),\qquad |\nabla f(0,1)|=4.
$$
故答案为 $4$。

### 第 12 题

**答案：** $4$

令 $x=t^2$，则 $dx=2t\,dt$，$\sqrt{x}=t$。上下限由 $x=1,e^2$ 变为 $t=1,e$，故
$$
\int_1^{e^2}\frac{\ln x}{\sqrt{x}}\,dx
=\int_1^e\frac{2\ln t}{t}\cdot 2t\,dt
=4\int_1^e\ln t\,dt.
$$
于是
$$
4\int_1^e\ln t\,dt
=4[t\ln t-t]_1^e=4.
$$

### 第 13 题

**答案：** $[4e^{-2},+\infty)$

题设等价于
$$
k\ge (x^2+y^2)e^{-(x+y)}
$$
对所有 $x,y\ge0$ 成立。因此只需求
$$
F(x,y)=(x^2+y^2)e^{-(x+y)}
$$
在第一象限闭区域上的最大值。

内点驻点满足
$$
\frac{2x}{x^2+y^2}=1,\qquad
\frac{2y}{x^2+y^2}=1,
$$
得 $x=y=1$，此时 $F=2e^{-2}$。

边界 $x=0$ 时，$F=y^2e^{-y}$，最大值在 $y=2$ 处取得，为 $4e^{-2}$；边界 $y=0$ 同理。故最大值为 $4e^{-2}$，所以
$$
k\in[4e^{-2},+\infty).
$$

### 第 14 题

**答案：** $-1$

记
$$
u_n(x)=\frac{n!}{n^n}e^{-nx}.
$$
由比值判别法，
$$
\lim_{n\to\infty}\left|\frac{u_{n+1}(x)}{u_n(x)}\right|
=\lim_{n\to\infty}\left(\frac{n}{n+1}\right)^n e^{-x}
=e^{-(x+1)}.
$$
当 $e^{-(x+1)}<1$，即 $x>-1$ 时级数收敛；当 $x<-1$ 时发散。

当 $x=-1$ 时，由 Stirling 公式
$$
\frac{n!}{n^n}e^n\sim\sqrt{2\pi n},
$$
通项不趋于 $0$，级数发散。因此收敛域为 $(-1,+\infty)$，故 $a=-1$。

### 第 15 题

**答案：** $-E$

令 $C=E-A$。则
$$
E-C^{-1}=(C-E)C^{-1}=-AC^{-1}.
$$
原方程化为
$$
-AC^{-1}B=A.
$$
由于 $A$ 可逆，左乘 $A^{-1}$ 得
$$
-C^{-1}B=E,
$$
所以
$$
B=-C=A-E.
$$
因此
$$
B-A=-E.
$$

### 第 16 题

**答案：** $\dfrac{5}{8}$

由题设
$$
P(AB)=0,\qquad P(AC)=0,\qquad P(BC)=P(B)P(C)=\frac{1}{9}.
$$
又因为 $A$ 与 $B,C$ 分别互不相容，所以 $ABC=\varnothing$。于是
$$
P(B\cup C)=\frac{1}{3}+\frac{1}{3}-\frac{1}{9}=\frac{5}{9},
$$
$$
P(A\cup B\cup C)=\frac{1}{3}+\frac{1}{3}+\frac{1}{3}-\frac{1}{9}=\frac{8}{9}.
$$
故
$$
P(B\cup C\mid A\cup B\cup C)=\frac{5/9}{8/9}=\frac{5}{8}.
$$

### 第 17 题

**答案：** $y=2x$ 是曲线 $y=y(x)$ 的唯一斜渐近线。

方程的积分因子为
$$
e^{\int \frac{1}{2\sqrt{x}}\,dx}=e^{\sqrt{x}}.
$$
于是
$$
\left(ye^{\sqrt{x}}\right)'=(2+\sqrt{x})e^{\sqrt{x}}.
$$
直接验证可得通解为
$$
y=2x+Ce^{-\sqrt{x}}.
$$
由 $y(1)=3$ 得
$$
3=2+Ce^{-1},\qquad C=e.
$$
故
$$
y=2x+e^{1-\sqrt{x}}.
$$
当 $x\to+\infty$ 时，$e^{1-\sqrt{x}}\to0$，所以
$$
y-2x\to0.
$$
因此曲线的斜渐近线为 $y=2x$；由于解在 $x>0$ 上定义且只有这一端趋于无穷，故它也是唯一渐近线。

### 第 18 题

**答案：** $I=2\pi-2$。

将被积函数拆开：
$$
\frac{(x-y)^2}{x^2+y^2}
=1-\frac{2xy}{x^2+y^2}.
$$
区域面积为
$$
|D|=\int_0^2\left(\sqrt{4-y^2}-y+2\right)dy=\pi+2.
$$

令 $x=r\cos\theta,\ y=r\sin\theta$。区域可表示为
$$
0\le\theta\le\frac{\pi}{2},\ 0\le r\le2;
\qquad
\frac{\pi}{2}\le\theta\le\pi,\ 0\le r\le\frac{2}{\sin\theta-\cos\theta}.
$$
记
$$
J=\iint_D\frac{2xy}{x^2+y^2}\,dxdy.
$$
则
$$
J=\int_0^{\pi/2}\int_0^2 2\sin\theta\cos\theta\,r\,dr\,d\theta
+\int_{\pi/2}^{\pi}\int_0^{2/(\sin\theta-\cos\theta)}
2\sin\theta\cos\theta\,r\,dr\,d\theta.
$$
第一项为 $2$；第二项令 $t=\tan\theta$ 计算得 $2-\pi$。因此
$$
J=4-\pi.
$$
所以
$$
I=|D|-J=(\pi+2)-(4-\pi)=2\pi-2.
$$

### 第 19 题

**答案：** $I=0$。

设
$$
P=yz^2-\cos z,\qquad Q=2xz^2,\qquad R=2xyz+x\sin z.
$$
则
$$
\nabla\times(P,Q,R)=(-2xz,0,z^2).
$$
由 Stokes 公式，
$$
I=\iint_\Sigma(\nabla\times\mathbf F)\cdot \mathbf n\,dS.
$$
将曲面写成
$$
z=\sqrt{1-4x^2-y^2},
$$
其上侧法向量面积元为
$$
(-z_x,-z_y,1)\,dxdy=\left(\frac{4x}{z},\frac{y}{z},1\right)dxdy.
$$
于是
$$
(\nabla\times\mathbf F)\cdot(-z_x,-z_y,1)
=-8x^2+z^2
=1-12x^2-y^2.
$$
投影区域为
$$
D=\{(x,y)\mid 4x^2+y^2\le1,\ x\ge0,\ y\ge0\}.
$$
作变换 $u=2x,\ v=y$，则 $dxdy=\frac{1}{2}\,dudv$，区域化为第一象限单位四分之一圆。故
$$
I=\frac{1}{2}\iint_{u^2+v^2\le1,\ u,v\ge0}(1-3u^2-v^2)\,dudv.
$$
在四分之一单位圆上
$$
\iint 1\,dudv=\frac{\pi}{4},\qquad
\iint u^2\,dudv=\iint v^2\,dudv=\frac{\pi}{16}.
$$
因此
$$
I=\frac{1}{2}\left(\frac{\pi}{4}-3\cdot\frac{\pi}{16}-\frac{\pi}{16}\right)=0.
$$

### 第 20 题

**答案：** 证明见解析。

先证充分性。若 $f''(x)\ge0$，则 $f$ 为凸函数。对任意 $x\in[a,b]$，由凸性，
$$
f\left(\frac{x+(a+b-x)}{2}\right)
\le \frac{f(x)+f(a+b-x)}{2}.
$$
左边即 $f\left(\frac{a+b}{2}\right)$。两边在 $[a,b]$ 上积分，得
$$
(b-a)f\left(\frac{a+b}{2}\right)
\le \frac{1}{2}\int_a^b f(x)\,dx+\frac{1}{2}\int_a^b f(a+b-x)\,dx.
$$
后一积分作代换 $u=a+b-x$，等于 $\int_a^b f(u)\,du$，故
$$
f\left(\frac{a+b}{2}\right)
\le \frac{1}{b-a}\int_a^b f(x)\,dx.
$$

再证必要性。任取 $x_0$，令 $a=x_0-h,\ b=x_0+h$，其中 $h>0$。由题设，
$$
f(x_0)\le \frac{1}{2h}\int_{x_0-h}^{x_0+h}f(x)\,dx.
$$
由 Taylor 展开，
$$
f(x_0+t)=f(x_0)+f'(x_0)t+\frac{1}{2}f''(x_0)t^2+o(t^2).
$$
在 $t\in[-h,h]$ 上取平均，奇次项积分为 $0$，得到
$$
\frac{1}{2h}\int_{x_0-h}^{x_0+h}f(x)\,dx
=f(x_0)+\frac{f''(x_0)}{6}h^2+o(h^2).
$$
代入不等式并令 $h\to0^+$，得 $f''(x_0)\ge0$。由于 $x_0$ 任意，故 $f''(x)\ge0$。

### 第 21 题

**答案：** (I)
$$
A=\begin{pmatrix}
1&2&3\\
2&4&6\\
3&6&9
\end{pmatrix}.
$$

(II) 可取
$$
Q=\begin{pmatrix}
\frac{1}{\sqrt{14}}&-\frac{2}{\sqrt{5}}&-\frac{3}{\sqrt{70}}\\
\frac{2}{\sqrt{14}}& \frac{1}{\sqrt{5}}&-\frac{6}{\sqrt{70}}\\
\frac{3}{\sqrt{14}}&0&\frac{5}{\sqrt{70}}
\end{pmatrix},
$$
标准形为
$$
14y_1^2.
$$

(III)
$$
x=k_1(-2,1,0)^T+k_2(-3,-6,5)^T,\qquad k_1,k_2\in\mathbb R.
$$

由题意
$$
f=x_1^2+4x_2^2+9x_3^2+4x_1x_2+6x_1x_3+12x_2x_3,
$$
故对应矩阵为
$$
A=\begin{pmatrix}
1&2&3\\
2&4&6\\
3&6&9
\end{pmatrix}.
$$

矩阵 $A$ 的特征值为 $14,0,0$。当 $\lambda=14$ 时，可取特征向量
$$
\alpha_1=(1,2,3)^T.
$$
当 $\lambda=0$ 时，解 $Ax=0$，可取两个线性无关特征向量
$$
\alpha_2=(-2,1,0)^T,\qquad \alpha_3=(-3,0,1)^T.
$$
将 $\alpha_2,\alpha_3$ 正交化，取
$$
\xi_2=(-2,1,0)^T,\qquad \xi_3=(-3,-6,5)^T.
$$
单位化得
$$
\gamma_1=\frac{1}{\sqrt{14}}(1,2,3)^T,\quad
\gamma_2=\frac{1}{\sqrt{5}}(-2,1,0)^T,\quad
\gamma_3=\frac{1}{\sqrt{70}}(-3,-6,5)^T.
$$
令 $Q=(\gamma_1,\gamma_2,\gamma_3)$，即
$$
Q=\begin{pmatrix}
\frac{1}{\sqrt{14}}&-\frac{2}{\sqrt{5}}&-\frac{3}{\sqrt{70}}\\
\frac{2}{\sqrt{14}}& \frac{1}{\sqrt{5}}&-\frac{6}{\sqrt{70}}\\
\frac{3}{\sqrt{14}}&0&\frac{5}{\sqrt{70}}
\end{pmatrix}.
$$
则经正交变换 $x=Qy$，二次型化为
$$
f=14y_1^2.
$$

由 $f=0$ 得 $y_1=0$，所以
$$
x=y_2\gamma_2+y_3\gamma_3.
$$
等价地，可写成
$$
x=k_1(-2,1,0)^T+k_2(-3,-6,5)^T,\qquad k_1,k_2\in\mathbb R.
$$

### 第 22 题

**答案：** 最大似然估计量为
$$
\hat\theta=\frac{2\sum_{i=1}^nX_i+\sum_{j=1}^mY_j}{2(n+m)}.
$$
且
$$
D(\hat\theta)=\frac{\theta^2}{n+m}.
$$

因为 $X$ 的均值为 $\theta$，$Y$ 的均值为 $2\theta$，故密度分别为
$$
f_X(x)=\frac{1}{\theta} e^{-x/\theta},\quad x>0,
$$
$$
f_Y(y)=\frac{1}{2\theta}e^{-y/(2\theta)},\quad y>0.
$$
样本相互独立，所以似然函数为
$$
L(\theta)=\frac{1}{2^m\theta^{n+m}}
\exp\left[-\frac{2\sum_{i=1}^nX_i+\sum_{j=1}^mY_j}{2\theta}\right].
$$
取对数：
$$
\ln L(\theta)=-m\ln2-(n+m)\ln\theta
-\frac{2\sum_{i=1}^nX_i+\sum_{j=1}^mY_j}{2\theta}.
$$
令导数为 $0$：
$$
\frac{d}{d\theta}\ln L(\theta)
=-\frac{n+m}{\theta}
+\frac{2\sum_{i=1}^nX_i+\sum_{j=1}^mY_j}{2\theta^2}=0,
$$
得
$$
\hat\theta=\frac{2\sum_{i=1}^nX_i+\sum_{j=1}^mY_j}{2(n+m)}.
$$

又
$$
D(X_i)=\theta^2,\qquad D(Y_j)=4\theta^2.
$$
因此
$$
D(\hat\theta)
=\frac{1}{4(n+m)^2}
D\left(2\sum_{i=1}^nX_i+\sum_{j=1}^mY_j\right)
$$
$$
=\frac{1}{4(n+m)^2}\left(4n\theta^2+4m\theta^2\right)
=\frac{\theta^2}{n+m}.
$$
