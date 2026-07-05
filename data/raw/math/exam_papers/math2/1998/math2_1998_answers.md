# Math 2 1998 Answers

资料类型：考研数学二答案解析
年份：1998
科目：数学二
范围：试卷 III
校对状态：已按答案页图像清洗并与题面同步。

## 答案速查

| 题号 | 题型 | 答案 |
|---|---|---|
| 1 | 填空题 | $-\dfrac{1}{4}$ |
| 2 | 填空题 | $\dfrac{37}{12}$ |
| 3 | 填空题 | $-\cot x\ln(\sin x)-\cot x-x+C$ |
| 4 | 填空题 | $x f(x^2)$ |
| 5 | 填空题 | $y=x+\dfrac{1}{e}$ |
| 6 | 选择题 | $D$ |
| 7 | 选择题 | $C$ |
| 8 | 选择题 | $A$ |
| 9 | 选择题 | $C$ |
| 10 | 选择题 | $B$ |
| 11 | 解答题 | 间断点为
$$
\frac{\pi}{4},\ \frac{3\pi}{4},\ \frac{5\pi}{4},\ \frac{7\pi}{4}.
$$
其中 $\dfrac{\pi}{4},\dfrac{5\pi}{4}$ 为第二类间断点，$\dfrac{3\pi}{4},\dfrac{7\pi}{4}$ 为可去间断点。 |
| 12 | 解答题 | $a=1,\ b=0,\ c=\dfrac12$ |
| 13 | 解答题 | $y=\dfrac{C_1\cos 2x+C_2\sin 2x+\frac15 e^x}{\cos x}$ |
| 14 | 解答题 | $\dfrac{\pi}{2}+\ln(2+\sqrt3)$ |
| 15 | 解答题 | 微分方程为
$$
mv\frac{dv}{dy}=mg-B\rho-kv,
$$
且
$$
y=-\frac{m}{k}v-\frac{m(mg-B\rho)}{k^2}\ln\!\left(\frac{mg-B\rho-kv}{mg-B\rho}\right).
$$
 |
| 16 | 证明题 | 存在唯一的 $x_0\in(0,1)$ 使
$$
x_0f(x_0)=\int_{x_0}^{1}f(x)\,dx.
$$
 |
| 17 | 解答题 | $\dfrac{(11\sqrt5-1)\pi}{6}$ |
| 18 | 解答题 | 曲线方程为
$$
y=-\ln\cos\left(x-\frac{\pi}{4}\right)+1+\ln2,\qquad -\frac{\pi}{4}<x<\frac{3\pi}{4}.
$$
其极大值为
$$
1+\ln2
$$
（在 $x=\frac{\pi}{4}$ 处取得），无极小值。 |
| 19 | 证明题 | 见解析。 |
| 20 | 解答题 | $
A=
\begin{pmatrix}
1&0&0&0\\
-2&1&0&0\\
1&-2&1&0\\
0&1&-2&1
\end{pmatrix}
$ |
| 21 | 解答题 | 当 $b\ne2$ 时不能表示；

当 $b=2,a\ne1$ 时，
$$
\beta=\alpha_1-2\alpha_2;
$$

当 $b=2,a=1$ 时，有无穷多种表示，
$$
\beta=(2k+1)\alpha_1+(-k-2)\alpha_2+k\alpha_3\qquad(k\in\mathbb R).
$$
 |

## 详细解析

### 第 1 题

- 答案：$-\dfrac{1}{4}$

对分子作泰勒展开：
$$
\sqrt{1+x}=1+\frac{x}{2}-\frac{x^2}{8}+o(x^2),\qquad
\sqrt{1-x}=1-\frac{x}{2}-\frac{x^2}{8}+o(x^2).
$$
故
$$
\sqrt{1+x}+\sqrt{1-x}-2=-\frac{x^2}{4}+o(x^2),
$$
从而原极限为
$$
-\frac14.
$$

### 第 2 题

- 答案：$\dfrac{37}{12}$

因
$$
y=-x(x-2)(x+1),
$$
与 $x$ 轴交于 $x=-1,0,2$。在 $[-1,0]$ 上函数为负，在 $[0,2]$ 上函数为正，因此
$$
A=-\int_{-1}^{0}(-x^3+x^2+2x)\,dx+\int_{0}^{2}(-x^3+x^2+2x)\,dx.
$$
计算得
$$
A=\frac14+\frac{17}{6}=\frac{37}{12}.
$$

### 第 3 题

- 答案：$-\cot x\ln(\sin x)-\cot x-x+C$

令
$$
u=\ln(\sin x),\qquad dv=\csc^2x\,dx,
$$
则
$$
du=\cot x\,dx,\qquad v=-\cot x.
$$
所以
$$
\int \frac{\ln(\sin x)}{\sin^2 x}\,dx
=-\cot x\ln(\sin x)+\int \cot^2x\,dx.
$$
又
$$
\cot^2x=\csc^2x-1,
$$
故原式为
$$
-\cot x\ln(\sin x)-\cot x-x+C.
$$

### 第 4 题

- 答案?$x f(x^2)$

令
$$
u=x^2-t^2,\qquad du=-2t\,dt.
$$
则
$$
\int_0^x t\,f(x^2-t^2)\,dt=\frac12\int_0^{x^2}f(u)\,du.
$$
对 $x$ 求导，得
$$
\frac{d}{dx}\int_0^x t\,f(x^2-t^2)\,dt
=\frac12f(x^2)\cdot 2x=xf(x^2).
$$

### 第 5 题

- 答案：$y=x+\dfrac{1}{e}$

当 $x\to+\infty$ 时，
$$
\ln\left(e+\frac1x\right)=1+\ln\left(1+\frac{1}{ex}\right),
$$
故
$$
y-x=x\ln\left(1+\frac{1}{ex}\right)\to \frac1e.
$$
因此斜渐近线为
$$
y=x+\frac1e.
$$

### 第 6 题

- 答案：$D$

若
$$
\frac1{x_n}\to 0,
$$
则 $x_n$ 的绝对值趋于无穷大。由
$$
x_ny_n\to 0
$$
可写为
$$
y_n=\frac{x_ny_n}{x_n},
$$
分子趋于 $0$，分母绝对值趋于无穷大，从而 $y_n\to 0$。故选 $D$。

### 第 7 题

- 答案：$C$

$|x^3-x|$ 的可能不可导点在
$$
x=-1,0,1.
$$
其中
$$
x^2-x-2=(x-2)(x+1),
$$
在 $x=-1$ 处恰为 $0$，可消去尖点；而在 $x=0,1$ 处前因子非零，所以仍不可导。故共有 $2$ 个不可导点，选 $C$。

### 第 8 题

- 答案：$A$

由可微定义知
$$
y'(x)=\frac{y}{1+x^2}.
$$
分离变量积分得
$$
\frac{y'}{y}=\frac{1}{1+x^2}\quad\Longrightarrow\quad
\ln y=\arctan x+C.
$$
由 $y(0)=\pi$ 得 $C=\ln\pi$，故
$$
y=\pi e^{\arctan x}.
$$
于是
$$
y(1)=\pi e^{\pi/4}.
$$
选 $A$。

### 第 9 题

- 答案：$C$

由 $f(a)$ 为极大值，在 $a$ 的邻域内有
$$
f(x)\le f(a).
$$
于是对固定的邻域内 $x\ne a$，
$$
\lim_{t\to a}\frac{f(t)-f(x)}{(t-x)^2}
=\frac{f(a)-f(x)}{(a-x)^2}\ge 0.
$$
故选 $C$。

### 第 10 题

- 答案：$B$

伴随矩阵的每个元素都是 $n-1$ 阶子式。矩阵整体乘以 $k$ 后，每个 $n-1$ 阶子式都会被乘上
$$
k^{n-1}.
$$
因此
$$
(kA)^*=k^{n-1}A^*.
$$
故选 $B$。

### 第 11 题

- 答案：间断点为
$$
\frac{\pi}{4},\ \frac{3\pi}{4},\ \frac{5\pi}{4},\ \frac{7\pi}{4}.
$$
其中 $\dfrac{\pi}{4},\dfrac{5\pi}{4}$ 为第二类间断点，$\dfrac{3\pi}{4},\dfrac{7\pi}{4}$ 为可去间断点。

间断点来自
$$
\tan\left(x-\frac{\pi}{4}\right)
$$
无定义或为零的位置，故候选点为
$$
\frac{\pi}{4},\ \frac{3\pi}{4},\ \frac{5\pi}{4},\ \frac{7\pi}{4}.
$$
分别考察左右极限，可得在
$$
\frac{\pi}{4},\ \frac{5\pi}{4}
$$
处分母趋于 $0$ 且函数发散，为第二类间断点；在
$$
\frac{3\pi}{4},\ \frac{7\pi}{4}
$$
处极限存在但原式无定义，为可去间断点。

### 第 12 题

- 答案：$a=1,\ b=0,\ c=\dfrac12$

要使极限存在且非零，分母在 $x\to0$ 时必须趋于 $0$，故只能有
$$
b=0.
$$
于是原式为
$$
\lim_{x\to0}\frac{ax-\sin x}{\int_0^x \frac{\ln(1+t^3)}{t}\,dt}.
$$
分子展开为
$$
ax-\sin x=(a-1)x+\frac{x^3}{6}+o(x^3),
$$
分母中
$$
\frac{\ln(1+t^3)}{t}=t^2+o(t^2),
$$
故积分后为
$$
\int_0^x \frac{\ln(1+t^3)}{t}\,dt=\frac{x^3}{3}+o(x^3).
$$
为使极限有限非零，需 $a=1$，从而
$$
c=\lim_{x\to0}\frac{x^3/6}{x^3/3}=\frac12.
$$

### 第 13 题

- 答案：$y=\dfrac{C_1\cos 2x+C_2\sin 2x+\frac15 e^x}{\cos x}$

代入
$$
y=\frac{u}{\cos x}
$$
并整理，可化为
$$
u''+4u=e^x.
$$
其对应齐次方程
$$
u''+4u=0
$$
通解为
$$
u_h=C_1\cos2x+C_2\sin2x.
$$
设特解为 $u_p=Ae^x$，代入得
$$
5A=1,\qquad A=\frac15.
$$
故
$$
u=C_1\cos2x+C_2\sin2x+\frac15e^x,
$$
从而
$$
y=\frac{C_1\cos 2x+C_2\sin 2x+\frac15 e^x}{\cos x}.
$$

### 第 14 题

- 答案：$\dfrac{\pi}{2}+\ln(2+\sqrt3)$

在区间 $\left[\frac12,1\right]$ 上有
$$
|x-x^2|=x-x^2,
$$
在区间 $\left[1,\frac32\right]$ 上有
$$
|x-x^2|=x^2-x.
$$
于是原积分拆为两段：
$$
\int_{1/2}^{1}\frac{dx}{\sqrt{x-x^2}}
+
\int_{1}^{3/2}\frac{dx}{\sqrt{x^2-x}}.
$$
前一段用 $x=\dfrac{1+\sin t}{2}$，后一段用 $2x-1=\sec t$，计算得
$$
\frac{\pi}{2}+\ln(2+\sqrt3).
$$

### 第 15 题

- 答案：微分方程为
$$
mv\frac{dv}{dy}=mg-B\rho-kv,
$$
且
$$
y=-\frac{m}{k}v-\frac{m(mg-B\rho)}{k^2}\ln\!\left(\frac{mg-B\rho-kv}{mg-B\rho}\right).
$$


取竖直向下为正方向。由牛顿第二定律，
$$
m\frac{dv}{dt}=mg-B\rho-kv.
$$
又
$$
\frac{dy}{dt}=v,\qquad \frac{dv}{dt}=v\frac{dv}{dy},
$$
故得到所求微分方程
$$
mv\frac{dv}{dy}=mg-B\rho-kv.
$$
分离变量后有
$$
dy=\frac{mv}{mg-B\rho-kv}\,dv.
$$
利用初始条件 $y=0,\ v=0$ 积分，得
$$
y=-\frac{m}{k}v-\frac{m(mg-B\rho)}{k^2}\ln\!\left(\frac{mg-B\rho-kv}{mg-B\rho}\right).
$$

### 第 16 题

- 答案：存在唯一的 $x_0\in(0,1)$ 使
$$
x_0f(x_0)=\int_{x_0}^{1}f(x)\,dx.
$$


令
$$
\varphi(x)=xf(x)-\int_x^1 f(t)\,dt.
$$
则
$$
\varphi(0)=-\int_0^1f(t)\,dt\le 0,\qquad \varphi(1)=f(1)\ge 0.
$$
由连续性知存在
$$
x_0\in(0,1)
$$
使 $\varphi(x_0)=0$，即
$$
x_0f(x_0)=\int_{x_0}^{1}f(x)\,dx.
$$
这正是题意。

再求导：
$$
\varphi'(x)=f(x)+xf'(x)+f(x)=2f(x)+xf'(x).
$$
由已知
$$
f'(x)>-\frac{2f(x)}{x}
$$
得
$$
\varphi'(x)>0.
$$
故 $\varphi(x)$ 在 $(0,1)$ 内严格单调递增，因此零点唯一。

### 第 17 题

- 答案：$\dfrac{(11\sqrt5-1)\pi}{6}$

设切点为 $(x_0,y_0)$，则
$$
y_0=\sqrt{x_0-1},\qquad y'=\frac{1}{2\sqrt{x-1}}.
$$
切线过原点，代入切线方程可得
$$
x_0=2,\qquad y_0=1,
$$
故切线为
$$
y=\frac{x}{2}.
$$

曲线段 $x\in[1,2]$ 绕 $x$ 轴旋转的面积为
$$
S_1=2\pi\int_1^2 y\sqrt{1+(y')^2}\,dx
=\frac{(5\sqrt5-1)\pi}{6}.
$$
线段 $y=\dfrac{x}{2},\ x\in[0,2]$ 旋转所得面积为
$$
S_2=2\pi\int_0^2 \frac{x}{2}\sqrt{1+\left(\frac12\right)^2}\,dx
=\pi\sqrt5.
$$
故总表面积为
$$
S=S_1+S_2=\frac{(11\sqrt5-1)\pi}{6}.
$$

### 第 18 题

- 答案：曲线方程为
$$
y=-\ln\cos\left(x-\frac{\pi}{4}\right)+1+\ln2,\qquad -\frac{\pi}{4}<x<\frac{3\pi}{4}.
$$
其极大值为
$$
1+\ln2
$$
（在 $x=\frac{\pi}{4}$ 处取得），无极小值。

由曲率公式与“向上凸”条件得
$$
\frac{y''}{(1+y'^2)^{3/2}}=\frac{1}{\sqrt{1+y'^2}},
$$
即
$$
y''=1+y'^2.
$$
令 $p=y'$，则
$$
p'=1+p^2.
$$
积分得
$$
\arctan p=x+C_1.
$$
由点 $(0,1)$ 处切线为 $y=x+1$，知
$$
y'(0)=1,
$$
故
$$
p=\tan\left(x+\frac{\pi}{4}\right).
$$
再积分并由 $y(0)=1$ 定常数，得
$$
y=-\ln\cos\left(x-\frac{\pi}{4}\right)+1+\ln2.
$$
当
$$
x=\frac{\pi}{4}
$$
时取极大值
$$
1+\ln2,
$$
且在定义区间内无极小值。

### 第 19 题

- 答案：见解析。

(1) 令
$$
\phi(x)=x^2-(1+x)\ln^2(1+x).
$$
逐次求导可证
$$
\phi'(x)>0\qquad(0<x<1),
$$
又 $\phi(0)=0$，故
$$
\phi(x)>0,
$$
即
$$
(1+x)\ln^2(1+x)<x^2.
$$

(2) 令
$$
g(x)=\frac{1}{\ln(1+x)}-\frac{1}{x}.
$$
计算导数可知 $g(x)$ 在 $(0,1)$ 上单调递减，因此
$$
g(1)<g(x)<\lim_{x\to0^+}g(x).
$$
由
$$
g(1)=\frac1{\ln2}-1,\qquad \lim_{x\to0^+}g(x)=\frac12,
$$
得
$$
\frac1{\ln2}-1<\frac{1}{\ln(1+x)}-\frac1x<\frac12.
$$

### 第 20 题

- 答案：$
A=
\begin{pmatrix}
1&0&0&0\\
-2&1&0&0\\
1&-2&1&0\\
0&1&-2&1
\end{pmatrix}
$

由原式左乘 $C$，得
$$
(2C-B)A^T=E.
$$
所以
$$
A^T=(2C-B)^{-1}.
$$
先算
$$
2C-B=
\begin{pmatrix}
1&2&3&4\\
0&1&2&3\\
0&0&1&2\\
0&0&0&1
\end{pmatrix}.
$$
其逆矩阵为
$$
(2C-B)^{-1}=
\begin{pmatrix}
1&-2&1&0\\
0&1&-2&1\\
0&0&1&-2\\
0&0&0&1
\end{pmatrix}.
$$
故
$$
A=
\begin{pmatrix}
1&0&0&0\\
-2&1&0&0\\
1&-2&1&0\\
0&1&-2&1
\end{pmatrix}.
$$

### 第 21 题

- 答案：当 $b\ne2$ 时不能表示；

当 $b=2,a\ne1$ 时，
$$
\beta=\alpha_1-2\alpha_2;
$$

当 $b=2,a=1$ 时，有无穷多种表示，
$$
\beta=(2k+1)\alpha_1+(-k-2)\alpha_2+k\alpha_3\qquad(k\in\mathbb R).
$$


设
$$
x_1\alpha_1+x_2\alpha_2+x_3\alpha_3=\beta,
$$
化为非齐次线性方程组。对其增广矩阵作初等变换，可得：

- 当 $b\ne2$ 时，增广矩阵出现矛盾行，因此无解，$\beta$ 不能由 $\alpha_1,\alpha_2,\alpha_3$ 线性表示；
- 当 $b=2,\ a\ne1$ 时，方程组有唯一解
$$
x_1=1,\quad x_2=-2,\quad x_3=0,
$$
故
$$
\beta=\alpha_1-2\alpha_2;
$$
- 当 $b=2,\ a=1$ 时，方程组有无穷多解。令自由参数为 $k$，可得
$$
x_1=2k+1,\qquad x_2=-k-2,\qquad x_3=k.
$$
所以
$$
\beta=(2k+1)\alpha_1+(-k-2)\alpha_2+k\alpha_3.
$$
