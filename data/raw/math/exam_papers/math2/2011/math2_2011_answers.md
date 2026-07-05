# Math 2 2011 Answers

资料类型：考研数学二答案解析
年份：2011
科目：数学二
整理状态：答案与解析按清洗后的正式题卡整理。

## 答案速查

| 题号 | 题型 | 答案 |
|---|---|---|
| 1 | choice | C |
| 2 | choice | B |
| 3 | choice | C |
| 4 | choice | C |
| 5 | choice | A |
| 6 | choice | B |
| 7 | choice | D |
| 8 | choice | D |
| 9 | fill_blank | $\sqrt2$ |
| 10 | fill_blank | $e^{-x}\sin x$ |
| 11 | fill_blank | $\ln(1+\sqrt2)$ |
| 12 | fill_blank | $\dfrac{1}{\lambda}$ |
| 13 | fill_blank | $\dfrac{7}{12}$ |
| 14 | fill_blank | $2$ |
| 15 | solution | $1<\alpha<3$ |
| 16 | solution | 极大值为 $1$（在点 $(-1,1)$ 处），极小值为 $-\dfrac13$（在点 $\left(\dfrac53,-\dfrac13\right)$ 处）；当 $x<\dfrac13$ 时曲线凹向下，当 $x>\dfrac13$ 时曲线凹向上；拐点为 $\left(\dfrac13,\dfrac13\right)$。 |
| 17 | solution | $f_u(1,1)+f_{uu}(1,1)+f_{uv}(1,1)$ |
| 18 | solution | $\displaystyle y=\arcsin\!\left(\frac{e^x}{\sqrt2}\right)-\frac\pi4$ |
| 19 | solution | 结论成立，数列 $\{a_n\}$ 收敛。 |
| 20 | solution | (I) $V=\dfrac{9\pi}{4}$；  
(II) $W=3375\pi g$。 |
| 21 | solution | $I=a$ |
| 22 | solution | (I) $a=5$；  
(II)
$$
\beta_1=2\alpha_1+4\alpha_2-\alpha_3,\qquad
\beta_2=\alpha_1+2\alpha_2,\qquad
\beta_3=5\alpha_1+10\alpha_2-2\alpha_3.
$$ |
| 23 | solution | (I) 特征值为 $-1,0,1$，对应特征向量可分别取
$$
(1,0,-1)^T,\ (0,1,0)^T,\ (1,0,1)^T.
$$
(II)
$$
A=
\begin{pmatrix}
0&0&1\\
0&0&0\\
1&0&0
\end{pmatrix}.
$$ |

## 详细解析

### 第 1 题
- 答案：C

由展开式
$$
\sin x=x-\frac{x^3}{6}+o(x^3),\qquad \sin3x=3x-\frac{(3x)^3}{6}+o(x^3)
$$
可得
$$
3\sin x-\sin3x
=3\left(x-\frac{x^3}{6}\right)-\left(3x-\frac{27x^3}{6}\right)+o(x^3)
=4x^3+o(x^3).
$$
故 $k=3,\ c=4$。

### 第 2 题
- 答案：B

因为 $f$ 在 $0$ 处可导，且 $f(0)=0$，所以
$$
f(x)=f'(0)x+o(x),\qquad f(x^3)=f'(0)x^3+o(x^3).
$$
于是
$$
x^2f(x)-2f(x^3)=f'(0)x^3-2f'(0)x^3+o(x^3)=-f'(0)x^3+o(x^3).
$$
因此极限为 $-f'(0)$。

### 第 3 题
- 答案：C

在定义域内
$$
f'(x)=\frac{1}{x-1}+\frac{1}{x-2}+\frac{1}{x-3}.
$$
令 $f'(x)=0$，化简得
$$
3x^2-12x+11=0.
$$
其判别式为 $12>0$，有两个不等实根，并且都落在函数定义域内，所以驻点有 $2$ 个。

### 第 4 题
- 答案：C

对应齐次方程的特征方程为
$$
r^2-\lambda^2=0,
$$
特征根为 $\pm\lambda$。右端 $e^{\lambda x},e^{-\lambda x}$ 都与齐次解共振，各需乘以 $x$，故特解应取
$$
y_p=x(ae^{\lambda x}+be^{-\lambda x}).
$$

### 第 5 题
- 答案：A

在 $(0,0)$ 附近作二阶展开：
$$
z=f(x)g(y)=f(0)g(0)+\frac12 f''(0)g(0)x^2+\frac12 f(0)g''(0)y^2+o(x^2+y^2).
$$
要使 $(0,0)$ 成为极小值点，二次项系数应都为正。由于 $f(0)>0,g(0)<0$，故应有
$$
f''(0)g(0)>0\Rightarrow f''(0)<0,
$$
$$
f(0)g''(0)>0\Rightarrow g''(0)>0.
$$

### 第 6 题
- 答案：B

在 $0<x<\dfrac\pi4$ 上，有
$$
0<\sin x<\cos x<1.
$$
取对数后得
$$
\ln(\sin x)<\ln(\cos x)<0,
$$
积分可知 $I<K<0$。又
$$
J=\int_0^{\pi/4}[\ln(\cos x)-\ln(\sin x)]dx=K-I>0.
$$
故
$$
I<K<J.
$$

### 第 7 题
- 答案：D

将第 $2$ 列加到第 $1$ 列，等价于右乘矩阵 $P_1$，故
$$
B=AP_1.
$$
再交换 $B$ 的第 $2,3$ 行得到单位矩阵，等价于左乘 $P_2$，即
$$
P_2B=I.
$$
代入得
$$
P_2AP_1=I\Rightarrow A=P_2^{-1}P_1^{-1}=P_2P_1^{-1}.
$$

### 第 8 题
- 答案：D

由 $Ax=0$ 的基础解系为 $(1,0,1,0)^T$，知
$$
\alpha_1+\alpha_3=0,
$$
故 $r(A)=3$。于是 $r(A^*)=1$，从而 $A^*x=0$ 的解空间维数为 $3$。  
又由恒等式
$$
A^*A=O
$$
知 $A$ 的列向量都属于 $A^*x=0$ 的解空间，因此该解空间就是 $A$ 的列空间。由于 $\alpha_3=-\alpha_1$，列空间的一组基可取 $\alpha_2,\alpha_3,\alpha_4$。

### 第 9 题
- 答案：$\sqrt2$

设极限为 $L$，取对数：
$$
\ln L=\lim_{x\to0}\frac{1}{x}\ln\left(\frac{1+2^x}{2}\right).
$$
由 $2^x=e^{x\ln2}=1+x\ln2+o(x)$，得
$$
\frac{1+2^x}{2}=1+\frac{x\ln2}{2}+o(x).
$$
因此
$$
\ln L=\frac{\ln2}{2},
$$
从而
$$
L=e^{(\ln2)/2}=\sqrt2.
$$

### 第 10 题
- 答案：$e^{-x}\sin x$

乘以积分因子 $e^x$，得
$$
(e^xy)'=\cos x.
$$
积分可得
$$
e^xy=\sin x+C.
$$
由 $y(0)=0$ 知 $C=0$，故
$$
y=e^{-x}\sin x.
$$

### 第 11 题
- 答案：$\ln(1+\sqrt2)$

有
$$
y'=\tan x,
$$
故弧长
$$
s=\int_0^{\pi/4}\sqrt{1+(y')^2}\,dx=\int_0^{\pi/4}\sec x\,dx.
$$
积分得
$$
s=\left.\ln|\sec x+\tan x|\right|_0^{\pi/4}=\ln(1+\sqrt2).
$$

### 第 12 题
- 答案：$\dfrac{1}{\lambda}$

由定义可知
$$
\int_{-\infty}^{+\infty}xf(x)\,dx=\int_0^{+\infty}x\lambda e^{-\lambda x}\,dx.
$$
分部积分或利用指数分布的期望公式，得
$$
\int_0^{+\infty}x\lambda e^{-\lambda x}\,dx=\frac{1}{\lambda}.
$$

### 第 13 题
- 答案：$\dfrac{7}{12}$

圆可写成
$$
x^2+(y-1)^2=1.
$$
区域由 $x=0$、$y=x$ 和上半圆弧围成，可取积分次序
$$
0\le x\le1,\qquad x\le y\le1+\sqrt{1-x^2}.
$$
因此
$$
\iint_D xy\,d\sigma
=\int_0^1\int_x^{1+\sqrt{1-x^2}}xy\,dy\,dx
=\int_0^1 x\left(1+\sqrt{1-x^2}-x^2\right)dx
=\frac14+\frac13=\frac{7}{12}.
$$

### 第 14 题
- 答案：$2$

对应矩阵为
$$
A=\begin{pmatrix}
1&1&1\\
1&3&1\\
1&1&1
\end{pmatrix}.
$$
其顺序主子式为
$$
\Delta_1=1>0,\qquad \Delta_2=2>0,\qquad \Delta_3=0.
$$
再注意到矩阵秩为 $2$，且非零特征值均为正，因此二次型有两个正平方项、一个零平方项，故正惯性指数为 $2$。

### 第 15 题
- 答案：$1<\alpha<3$

先看 $x\to0^+$。由
$$
\ln(1+t^2)\sim t^2
$$
得
$$
\int_0^x\ln(1+t^2)dt\sim\int_0^x t^2dt=\frac{x^3}{3}.
$$
故
$$
F(x)\sim\frac{x^3/3}{x^\alpha}=\frac13x^{3-\alpha},
$$
要使极限为 $0$，需
$$
3-\alpha>0\Rightarrow \alpha<3.
$$
再看 $x\to+\infty$。当 $t$ 大时，$\ln(1+t^2)\sim2\ln t$，从而
$$
\int_0^x\ln(1+t^2)dt\sim 2x\ln x.
$$
因此
$$
F(x)\sim 2x^{1-\alpha}\ln x.
$$
要使其趋于 $0$，需
$$
\alpha>1.
$$
综上
$$
1<\alpha<3.
$$

### 第 16 题
- 答案：极大值为 $1$（在点 $(-1,1)$ 处），极小值为 $-\dfrac13$（在点 $\left(\dfrac53,-\dfrac13\right)$ 处）；当 $x<\dfrac13$ 时曲线凹向下，当 $x>\dfrac13$ 时曲线凹向上；拐点为 $\left(\dfrac13,\dfrac13\right)$。

有
$$
\frac{dx}{dt}=t^2+1>0,
$$
故 $x$ 关于 $t$ 单调增加。于是
$$
\frac{dy}{dx}=\frac{dy/dt}{dx/dt}=\frac{t^2-1}{t^2+1}.
$$
令 $\dfrac{dy}{dx}=0$，得 $t=\pm1$。代入参数方程：
$$
t=-1\Rightarrow (x,y)=(-1,1),
$$
$$
t=1\Rightarrow \left(x,y\right)=\left(\frac53,-\frac13\right).
$$
又
$$
\frac{d^2y}{dx^2}=\frac{\dfrac{d}{dt}\left(\dfrac{t^2-1}{t^2+1}\right)}{dx/dt}
=\frac{4t}{(t^2+1)^3}.
$$
故当 $t<0$ 时 $\dfrac{d^2y}{dx^2}<0$，曲线凹向下；当 $t>0$ 时 $\dfrac{d^2y}{dx^2}>0$，曲线凹向上。  
由 $t=0$ 时
$$
x=y=\frac13,
$$
知拐点为 $\left(\dfrac13,\dfrac13\right)$。

### 第 17 题
- 答案：$f_u(1,1)+f_{uu}(1,1)+f_{uv}(1,1)$

记
$$
u=xy,\qquad v=yg(x),
$$
则
$$
z=f(u,v).
$$
先对 $x$ 求偏导：
$$
z_x=f_u\,u_x+f_v\,v_x=yf_u+y g'(x)f_v.
$$
再对 $y$ 求偏导：
$$
z_{xy}=f_u+y(xf_{uu}+g(x)f_{uv})+g'(x)f_v+y g'(x)(x f_{uv}+g(x)f_{vv}).
$$
由于 $g$ 在 $x=1$ 处取极值且可导，所以
$$
g(1)=1,\qquad g'(1)=0.
$$
在 $(x,y)=(1,1)$ 处代入，且此时 $(u,v)=(1,1)$，得到
$$
z_{xy}(1,1)=f_u(1,1)+f_{uu}(1,1)+f_{uv}(1,1).
$$

### 第 18 题
- 答案：$\displaystyle y=\arcsin\!\left(\frac{e^x}{\sqrt2}\right)-\frac\pi4$

设
$$
p=y'.
$$
因为切线倾角 $\alpha=\arctan p$，故
$$
\frac{d\alpha}{dx}=\frac{p'}{1+p^2}.
$$
题设给出
$$
\frac{p'}{1+p^2}=p,
$$
即
$$
p'=p(1+p^2).
$$
又曲线与直线 $y=x$ 相切于原点，所以
$$
y(0)=0,\qquad p(0)=1.
$$
分离变量：
$$
\int\frac{dp}{p(1+p^2)}=\int dx.
$$
积分得
$$
\ln p-\frac12\ln(1+p^2)=x+C.
$$
由 $p(0)=1$ 可得 $C=-\dfrac12\ln2$，化简得
$$
\frac{p}{\sqrt{1+p^2}}=\frac{e^x}{\sqrt2}.
$$
故
$$
p=y'=\frac{e^x}{\sqrt{2-e^{2x}}}.
$$
于是
$$
y=\int \frac{e^x}{\sqrt{2-e^{2x}}}\,dx
=\arcsin\left(\frac{e^x}{\sqrt2}\right)+C_1.
$$
再由 $y(0)=0$ 得
$$
C_1=-\frac\pi4.
$$

### 第 19 题
- 答案：结论成立，数列 $\{a_n\}$ 收敛。

(I) 由函数 $\dfrac1x$ 在区间 $[n,n+1]$ 上单调递减，
$$
\frac1{n+1}<\int_n^{n+1}\frac{1}{x}\,dx<\frac1n.
$$
而
$$
\int_n^{n+1}\frac1x\,dx=\ln\left(1+\frac1n\right),
$$
故结论成立。  
(II) 考察差分：
$$
a_{n+1}-a_n=\frac1{n+1}-\ln\left(1+\frac1n\right).
$$
由 (I) 知
$$
\frac1{n+1}-\ln\left(1+\frac1n\right)<0,
$$
故 $\{a_n\}$ 单调递减。又由
$$
\ln n=\sum_{k=1}^{n-1}\ln\left(1+\frac1k\right)<\sum_{k=1}^{n-1}\frac1k,
$$
得
$$
a_n=\left(1+\frac12+\cdots+\frac1{n-1}\right)-\ln n+\frac1n>0.
$$
因此 $\{a_n\}$ 有下界且单调递减，所以收敛。

### 第 20 题
- 答案：(I) $V=\dfrac{9\pi}{4}$；  
(II) $W=3375\pi g$。

旋转半径满足
$$
r^2=
\begin{cases}
1-y^2,&-1\le y\le \dfrac12,\\
2y-y^2,&\dfrac12\le y\le2.
\end{cases}
$$
(I) 容积
$$
V=\pi\int_{-1}^{1/2}(1-y^2)dy+\pi\int_{1/2}^{2}(2y-y^2)dy
=\frac{9\pi}{4}.
$$
(II) 把高度为 $y$ 处的薄层水抽到顶部 $y=2$，需提升距离 $2-y$。故做功
$$
W=10^3 g\pi\int_{-1}^{1/2}(2-y)(1-y^2)dy
+10^3 g\pi\int_{1/2}^{2}(2-y)(2y-y^2)dy.
$$
计算得
$$
\int_{-1}^{1/2}(2-y)(1-y^2)dy+\int_{1/2}^{2}(2-y)(2y-y^2)dy=\frac{27}{8},
$$
所以
$$
W=10^3g\pi\cdot\frac{27}{8}=3375\pi g.
$$

### 第 21 题
- 答案：$I=a$

对 $x$ 分部积分：
$$
I=\int_0^1 y\,dy\int_0^1 x f_{xy}(x,y)\,dx
=\int_0^1 y\left([xf_y(x,y)]_0^1-\int_0^1 f_y(x,y)dx\right)dy.
$$
由于 $f(1,y)=0$，所以 $f_y(1,y)=0$，故
$$
I=-\int_0^1 y\,dy\int_0^1 f_y(x,y)dx.
$$
交换积分次序并对 $y$ 再分部积分：
$$
I=-\int_0^1 dx\int_0^1 y f_y(x,y)dy
=-\int_0^1 dx\left([yf(x,y)]_0^1-\int_0^1 f(x,y)dy\right).
$$
又因 $f(x,1)=0$，于是
$$
I=\int_0^1dx\int_0^1 f(x,y)dy=\iint_D f(x,y)dxdy=a.
$$

### 第 22 题
- 答案：(I) $a=5$；  
(II)
$$
\beta_1=2\alpha_1+4\alpha_2-\alpha_3,\qquad
\beta_2=\alpha_1+2\alpha_2,\qquad
\beta_3=5\alpha_1+10\alpha_2-2\alpha_3.
$$

(I) 若 $\beta_1,\beta_2,\beta_3$ 线性无关，则它们张成 $\mathbb R^3$，任意三维向量组都能由它们线性表示，这与题意矛盾。因此
$$
\det(\beta_1,\beta_2,\beta_3)=0.
$$
计算
$$
\det
\begin{pmatrix}
1&1&3\\
1&2&4\\
1&3&a
\end{pmatrix}
=a-5,
$$
故
$$
a=5.
$$
(II) 设
$$
(\alpha_1,\alpha_2,\alpha_3)
=
\begin{pmatrix}
1&0&1\\
0&1&3\\
1&1&5
\end{pmatrix}.
$$
分别解线性方程组
$$
c_1\alpha_1+c_2\alpha_2+c_3\alpha_3=\beta_i
$$
即可得到
$$
\beta_1=2\alpha_1+4\alpha_2-\alpha_3,
$$
$$
\beta_2=\alpha_1+2\alpha_2,
$$
$$
\beta_3=5\alpha_1+10\alpha_2-2\alpha_3.
$$

### 第 23 题
- 答案：(I) 特征值为 $-1,0,1$，对应特征向量可分别取
$$
(1,0,-1)^T,\ (0,1,0)^T,\ (1,0,1)^T.
$$
(II)
$$
A=
\begin{pmatrix}
0&0&1\\
0&0&0\\
1&0&0
\end{pmatrix}.
$$

设
$$
u_1=(1,0,-1)^T,\qquad u_2=(1,0,1)^T.
$$
由题设矩阵等式知
$$
Au_1=-u_1,\qquad Au_2=u_2,
$$
故 $-1,1$ 是 $A$ 的两个特征值，特征向量分别为 $u_1,u_2$。  
又因 $r(A)=2$，所以 $0$ 也是特征值。由于 $A$ 为实对称矩阵，不同特征值对应的特征向量互相正交，故与 $u_1,u_2$ 都正交的特征向量可取
$$
u_3=(0,1,0)^T.
$$
于是
$$
A=P\operatorname{diag}(-1,0,1)P^{-1},
$$
其中 $P$ 的列向量取为 $u_1,u_3,u_2$。也可直接利用谱分解：
$$
A=-\frac{u_1u_1^T}{u_1^Tu_1}+\frac{u_2u_2^T}{u_2^Tu_2}.
$$
计算得
$$
A=
\begin{pmatrix}
0&0&1\\
0&0&0\\
1&0&0
\end{pmatrix}.
$$
