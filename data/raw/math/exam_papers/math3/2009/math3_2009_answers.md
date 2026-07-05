# 2009 年考研数学三答案与解析

## 第 1 题

### 标准答案

C

### 解析

使函数无意义的点来自 $\sin(\pi x)=0$，即所有整数点 $x=k$。

要成为可去间断点，还需要分子同时为 $0$。由
$$
x-x^3=x(1-x^2)=0
$$
得到候选点只有 $x=0,\pm1$。

在这三个点处，用洛必达法则可得
$$
\lim_{x\to0}\frac{x-x^3}{\sin(\pi x)}=\frac{1}{\pi},\quad
\lim_{x\to1}\frac{x-x^3}{\sin(\pi x)}=\frac{2}{\pi},\quad
\lim_{x\to-1}\frac{x-x^3}{\sin(\pi x)}=\frac{2}{\pi}.
$$

因而可去间断点共有 $3$ 个，选 C。

## 第 2 题

### 标准答案

A

### 解析

由泰勒展开，
$$
\sin(ax)=ax-\frac{a^3x^3}{6}+o(x^3),
$$
所以
$$
f(x)=x-\sin(ax)=(1-a)x+\frac{a^3x^3}{6}+o(x^3).
$$

又有
$$
\ln(1-bx)=-bx+o(x),
$$
因而
$$
g(x)=x^2\ln(1-bx)=-bx^3+o(x^3).
$$

若 $f(x)$ 与 $g(x)$ 等价，则 $f(x)$ 也必须是三阶无穷小，故先有 $1-a=0$，即 $a=1$。
此时
$$
f(x)\sim\frac{x^3}{6},\qquad g(x)\sim-bx^3.
$$
再由等价关系得 $-b=\frac16$，所以 $b=-\frac16$。

故选 A。

## 第 3 题

### 标准答案

A

### 解析

设
$$
h(x)=\int_1^x\frac{\sin t}{t}\,dt-\ln x
    =\int_1^x\frac{\sin t-1}{t}\,dt.
$$

对一切 $t>0$ 都有 $\sin t\le1$，且除个别点外严格小于 $1$，所以
$$
\frac{\sin t-1}{t}\le0.
$$

当 $x>1$ 时，上式从 $1$ 积到 $x$，故 $h(x)<0$；
当 $0<x<1$ 时，
$$
h(x)=-\int_x^1\frac{\sin t-1}{t}\,dt>0.
$$

因而不等式成立当且仅当 $0<x<1$，选 A。

## 第 4 题

### 标准答案

D

### 解析

由 $F'(x)=f(x)$ 且 $F(0)=0$，可直接根据题图判断 $F$ 的单调性与形状：

1. 在 $[-1,0]$ 上，$f(x)>0$，所以 $F(x)$ 单调递增；但因为
   $$
   F(x)=\int_0^x f(t)\,dt=-\int_x^0 f(t)\,dt<0,
   $$
   因此图像位于 $x$ 轴下方并向上升到原点。
2. 在 $(0,1)$ 上，$f(x)<0$，故 $F(x)$ 继续减小。
3. 在 $(1,2)$ 上，$f(x)>0$，故 $F(x)$ 转为增大。
4. 在 $[2,3]$ 上，$f(x)=0$，所以 $F(x)$ 保持常数。

同时 $F(x)$ 必连续，因此只有 D 与这些特征完全一致。

## 第 5 题

### 标准答案

B

### 解析

记
$$
M=\begin{pmatrix}
O & A \\
B & O
\end{pmatrix}.
$$

先求行列式：
$$
|M|=\left|\begin{pmatrix} O & A \\ B & O \end{pmatrix}\right|
=|{-AB}|=|A||B|=2\times3=6.
$$
因此 $M$ 可逆。

对这种分块矩阵有
$$
M^{-1}=\begin{pmatrix}
O & B^{-1} \\
A^{-1} & O
\end{pmatrix}.
$$

伴随矩阵满足 $M^*=|M|M^{-1}$，于是
$$
M^*=6\begin{pmatrix}
O & B^{-1} \\
A^{-1} & O
\end{pmatrix}
=
\begin{pmatrix}
O & 6B^{-1} \\
6A^{-1} & O
\end{pmatrix}.
$$

又因为 $B^*=|B|B^{-1}=3B^{-1}$，$A^*=|A|A^{-1}=2A^{-1}$，故
$$
6B^{-1}=2B^*,\qquad 6A^{-1}=3A^*.
$$

所以
$$
M^*=
\begin{pmatrix}
O & 2B^* \\
3A^* & O
\end{pmatrix},
$$
选 B。

## 第 6 题

### 标准答案

A

### 解析

令
$$
E=\begin{pmatrix}
1 & 0 & 0 \\
1 & 1 & 0 \\
0 & 0 & 1
\end{pmatrix},
$$
则它的三列分别是 $(1,1,0)^T,(0,1,0)^T,(0,0,1)^T$，因此
$$
Q=PE.
$$

于是
$$
Q^TAQ=(PE)^TA(PE)=E^T(P^TAP)E.
$$

将
$$
P^TAP=\operatorname{diag}(1,1,2)
$$
代入，得到
$$
Q^TAQ
=E^T\begin{pmatrix}
1 & 0 & 0 \\
0 & 1 & 0 \\
0 & 0 & 2
\end{pmatrix}E
=
\begin{pmatrix}
2 & 1 & 0 \\
1 & 1 & 0 \\
0 & 0 & 2
\end{pmatrix}.
$$

所以选 A。

## 第 7 题

### 标准答案

D

### 解析

互不相容意味着
$$
A\cap B=\varnothing,
$$
所以
$$
P(AB)=0.
$$

由德摩根律，
$$
\overline{A}\cup\overline{B}=\overline{A\cap B}=\overline{\varnothing}=\Omega,
$$
因而
$$
P(\overline{A}\cup\overline{B})=1.
$$

其余选项都不必然成立，因此正确答案是 D。

## 第 8 题

### 标准答案

B

### 解析

记标准正态分布函数为 $\Phi(z)$。由全概率公式与独立性，
$$
F_Z(z)=P(XY\le z)
=\frac12P(X\cdot0\le z)+\frac12P(X\le z).
$$

当 $z<0$ 时，$P(0\le z)=0$，因此
$$
F_Z(z)=\frac12\Phi(z).
$$

当 $z\ge0$ 时，$P(0\le z)=1$，因此
$$
F_Z(z)=\frac12+\frac12\Phi(z).
$$

在 $z=0$ 处有跳跃：
$$
F_Z(0)-F_Z(0^-)=\frac12.
$$

所以分布函数只有一个间断点，选 B。

## 第 9 题

### 标准答案

$\frac{3e}{2}$

### 解析

当 $x\to0$ 时，
$$
\cos x=1-\frac{x^2}{2}+o(x^2),
$$
所以
$$
e^{\cos x}=e^{1-\frac{x^2}{2}+o(x^2)}
=e\left(1-\frac{x^2}{2}+o(x^2)\right).
$$
因而
$$
e-e^{\cos x}=\frac{e}{2}x^2+o(x^2).
$$

又
$$
\sqrt[3]{1+x^2}-1=\frac13x^2+o(x^2).
$$

所以极限为
$$
\lim_{x\to0}\frac{\frac{e}{2}x^2+o(x^2)}{\frac13x^2+o(x^2)}
=\frac{e/2}{1/3}
=\frac{3e}{2}.
$$

## 第 10 题

### 标准答案

$2\ln 2+1$

### 解析

先取对数：
$$
\ln z=x\ln(x+e^y).
$$

两边对 $x$ 求偏导，得
$$
\frac{1}{z}\frac{\partial z}{\partial x}
=\ln(x+e^y)+\frac{x}{x+e^y}.
$$
所以
$$
\frac{\partial z}{\partial x}
=(x+e^y)^x\left[\ln(x+e^y)+\frac{x}{x+e^y}\right].
$$

在 $(1,0)$ 处，$e^y=1$，$z=2$，于是
$$
\left.\frac{\partial z}{\partial x}\right|_{(1,0)}
=2\left(\ln2+\frac12\right)
=2\ln2+1.
$$

## 第 11 题

### 标准答案

$\frac{1}{e}$

### 解析

记
$$
a_n=\frac{e^n-(-1)^n}{n^2}.
$$
因为
$$
\lim_{n\to\infty}\sqrt[n]{|a_n|}
=\lim_{n\to\infty}\sqrt[n]{\frac{|e^n-(-1)^n|}{n^2}}
=e,
$$
所以幂级数的收敛半径为
$$
R=\frac{1}{\limsup\sqrt[n]{|a_n|}}=\frac1e.
$$

## 第 12 题

### 标准答案

$8000$

### 解析

收益函数为
$$
R(p)=pQ(p).
$$
价格弹性定义为
$$
\varepsilon_p=-\frac{p}{Q}\frac{dQ}{dp}=0.2,
$$
因而
$$
pQ'(p)=-0.2Q.
$$

于是
$$
R'(p)=Q+pQ'=Q-0.2Q=0.8Q.
$$

当 $Q=10000$ 时，
$$
R'(p)=0.8\times10000=8000.
$$
所以价格每增加 $1$ 元，收益增加 $8000$ 元。

## 第 13 题

### 标准答案

$2$

### 解析

相似矩阵有相同的特征值，因此矩阵 $\alpha\beta^T$ 的特征值为 $3,0,0$。

矩阵的迹等于特征值之和，也等于对角元之和。对秩一矩阵 $\alpha\beta^T$ 有
$$
\operatorname{tr}(\alpha\beta^T)=\beta^T\alpha
=(1,0,k)\begin{pmatrix}1\\1\\1\end{pmatrix}=1+k.
$$

另一方面，
$$
\operatorname{tr}(\alpha\beta^T)=3+0+0=3.
$$

所以 $1+k=3$，从而 $k=2$。

## 第 14 题

### 标准答案

$np^2$

### 解析

对二项分布总体 $B(n,p)$，
$$
E(\overline{X})=E(X_1)=np.
$$

样本方差 $S^2$ 是总体方差的无偏估计，因此
$$
E(S^2)=\operatorname{Var}(X_1)=np(1-p).
$$

所以
$$
ET=E(\overline{X})-E(S^2)=np-np(1-p)=np^2.
$$

## 第 15 题

### 标准答案

唯一驻点为 $\left(0,e^{-1}\right)$，该点取得极小值
$$
f\left(0,e^{-1}\right)=-\frac1e.
$$
函数无极大值。

### 解析

定义域为 $y>0$。

一阶偏导数为
$$
f_x=2x(2+y^2),\qquad f_y=2x^2y+\ln y+1.
$$
由 $f_x=0$ 得 $x=0$；代入 $f_y=0$ 得
$$
\ln y+1=0\quad\Rightarrow\quad y=e^{-1}.
$$
因而唯一驻点是 $\left(0,e^{-1}\right)$。

二阶偏导数为
$$
f_{xx}=4+2y^2,\qquad f_{xy}=4xy,\qquad f_{yy}=2x^2+\frac1y.
$$
在驻点处，
$$
f_{xx}=4+\frac{2}{e^2}>0,\qquad
f_{xy}=0,\qquad
f_{yy}=e>0,
$$
因此 Hessian 正定，故该驻点是极小值点。

又因为
$$
x^2(2+y^2)\ge0,
$$
而函数 $y\ln y$ 在 $y>0$ 上的最小值为 $-\frac1e$（在 $y=e^{-1}$ 处取得），故
$$
f(x,y)\ge -\frac1e.
$$
所以这不仅是局部极小值，还是全局最小值：
$$
f\left(0,e^{-1}\right)=-\frac1e.
$$

由于 $x^2(2+y^2)\to+\infty$ 可取到任意大值，函数不存在极大值。

## 第 16 题

### 标准答案

一个原函数为
$$
x\ln\left(1+\sqrt{\frac{1+x}{x}}\right)
+\frac12\ln\!\bigl(\sqrt{x}+\sqrt{1+x}\bigr)
-\frac12\bigl(\sqrt{x(1+x)}-x\bigr)+C.
$$

### 解析

令
$$
t=\sqrt{\frac{1+x}{x}}\quad(t>1),
$$
则
$$
x=\frac{1}{t^2-1},\qquad dx=-\frac{2t}{(t^2-1)^2}\,dt.
$$

原积分化为
$$
I=-\int \frac{2t\ln(1+t)}{(t^2-1)^2}\,dt.
$$

对它做分部积分，可取
$$
u=\ln(1+t),\qquad dv=-\frac{2t}{(t^2-1)^2}\,dt,
$$
则
$$
du=\frac{dt}{1+t},\qquad v=\frac{1}{t^2-1}.
$$
于是
$$
I=\frac{\ln(1+t)}{t^2-1}-\int\frac{dt}{(1+t)(t^2-1)}.
$$

而
$$
\frac{1}{(1+t)(t^2-1)}
=\frac{1}{(t-1)(t+1)^2}
=\frac{1}{4(t-1)}-\frac{1}{4(t+1)}-\frac{1}{2(t+1)^2}.
$$
所以
$$
I=\frac{\ln(1+t)}{t^2-1}
-\frac14\ln(t-1)+\frac14\ln(t+1)-\frac{1}{2(t+1)}+C.
$$

再代回 $t=\sqrt{\frac{1+x}{x}}$，并利用
$$
\frac{t+1}{t-1}=\bigl(\sqrt{1+x}+\sqrt{x}\bigr)^2,
\qquad
\frac{1}{t+1}=\sqrt{x(1+x)}-x,
$$
整理得
$$
I=
x\ln\left(1+\sqrt{\frac{1+x}{x}}\right)
+\frac12\ln\!\bigl(\sqrt{x}+\sqrt{1+x}\bigr)
-\frac12\bigl(\sqrt{x(1+x)}-x\bigr)+C.
$$

## 第 17 题

### 标准答案

$-\dfrac{8}{3}$

### 解析

用极坐标变换
$$
x=r\cos\theta,\qquad y=r\sin\theta.
$$

圆域条件
$$
(x-1)^2+(y-1)^2\le2
$$
化为
$$
r^2-2r(\cos\theta+\sin\theta)\le0
\quad\Rightarrow\quad
0\le r\le2(\cos\theta+\sin\theta).
$$

又由 $y\ge x$ 得
$$
\sin\theta\ge\cos\theta
\quad\Rightarrow\quad
\theta\in\left[\frac\pi4,\frac{5\pi}4\right].
$$
同时为了使上界非负，还需 $\cos\theta+\sin\theta\ge0$，因此最终
$$
\theta\in\left[\frac\pi4,\frac{3\pi}4\right].
$$

于是
$$
\iint_D(x-y)\,dx\,dy
=\int_{\pi/4}^{3\pi/4}\int_0^{2(\cos\theta+\sin\theta)}
r(\cos\theta-\sin\theta)\cdot r\,dr\,d\theta.
$$

先对 $r$ 积分：
$$
=\frac13\int_{\pi/4}^{3\pi/4}
\bigl[2(\cos\theta+\sin\theta)\bigr]^3(\cos\theta-\sin\theta)\,d\theta.
$$

设 $u=\sin\theta+\cos\theta$，则
$$
du=(\cos\theta-\sin\theta)\,d\theta.
$$
积分变为
$$
\frac83\int_{\sqrt2}^{0}u^3\,du
=\frac83\left[\frac{u^4}{4}\right]_{\sqrt2}^{0}
=-\frac83.
$$

所以原积分为
$$
-\frac83.
$$

## 第 18 题

### 标准答案

（A）结论成立，可由罗尔定理推出拉格朗日中值定理。

（B）结论成立，且
$$
f'_+(0)=A.
$$

### 解析

**（A）证明拉格朗日中值定理**

构造辅助函数
$$
\varphi(x)=f(x)-f(a)-\frac{f(b)-f(a)}{b-a}(x-a).
$$
则 $\varphi(x)$ 在 $[a,b]$ 上连续、在 $(a,b)$ 内可导，且
$$
\varphi(a)=0,\qquad \varphi(b)=f(b)-f(a)-\frac{f(b)-f(a)}{b-a}(b-a)=0.
$$
因而由罗尔定理，存在 $\xi\in(a,b)$ 使得
$$
\varphi'(\xi)=0.
$$
又
$$
\varphi'(x)=f'(x)-\frac{f(b)-f(a)}{b-a},
$$
所以
$$
f'(\xi)=\frac{f(b)-f(a)}{b-a},
$$
即
$$
f(b)-f(a)=f'(\xi)(b-a).
$$

**（B）证明右导数存在且等于 $A$**

任取 $x\in(0,\delta)$。函数 $f$ 在 $[0,x]$ 上连续、在 $(0,x)$ 上可导，因此由（A）的结论，存在 $\xi_x\in(0,x)$ 使得
$$
\frac{f(x)-f(0)}{x}=f'(\xi_x).
$$

当 $x\to0^+$ 时，$\xi_x\in(0,x)$，故也有 $\xi_x\to0^+$。于是
$$
\lim_{x\to0^+}\frac{f(x)-f(0)}{x}
=\lim_{x\to0^+}f'(\xi_x)
=A.
$$

左边正是右导数 $f'_+(0)$ 的定义，因此 $f'_+(0)$ 存在，且
$$
f'_+(0)=A.
$$

## 第 19 题

### 标准答案

曲线满足
$$
2y+\frac{1}{\sqrt y}=3x,\qquad y>0.
$$

### 解析

设
$$
S(t)=\int_1^t f(x)\,dx,\qquad
V(t)=\pi\int_1^t f(x)^2\,dx.
$$

题意给出
$$
V(t)=\pi t\,S(t),
$$
即
$$
\int_1^t f(x)^2\,dx=t\int_1^t f(x)\,dx.
$$

对 $t$ 求导，得
$$
f(t)^2=\int_1^t f(x)\,dx+t f(t). \tag{1}
$$

再对 (1) 求导：
$$
2f(t)f'(t)=f(t)+f(t)+t f'(t),
$$
即
$$
(2f(t)-t)f'(t)=2f(t). \tag{2}
$$

令 $y=f(t)$，把 $t$ 看成 $y$ 的函数，则由 (2)
$$
\frac{dt}{dy}=1-\frac{t}{2y},
$$
即
$$
\frac{dt}{dy}+\frac{1}{2y}t=1.
$$

这是关于 $t(y)$ 的一阶线性方程。积分因子为 $\sqrt y$，故
$$
\frac{d}{dy}\bigl(t\sqrt y\bigr)=\sqrt y.
$$
积分得
$$
t\sqrt y=\frac23y^{3/2}+C,
$$
从而
$$
t=\frac23y+C y^{-1/2}. \tag{3}
$$

由 (1) 在 $t=1$ 时可得
$$
f(1)^2=f(1).
$$
又因 $f(1)>0$，故 $f(1)=1$。把点 $(t,y)=(1,1)$ 代入 (3) 得
$$
1=\frac23+C \quad\Rightarrow\quad C=\frac13.
$$

因此
$$
t=\frac23y+\frac{1}{3\sqrt y}.
$$
把 $t$ 改写成 $x$，得到曲线方程
$$
2y+\frac{1}{\sqrt y}=3x,\qquad y>0.
$$

## 第 20 题

### 标准答案

（A）
$$
\xi_2=\begin{pmatrix}0\\0\\1\end{pmatrix}+k\begin{pmatrix}1\\-1\\2\end{pmatrix},
\qquad
\xi_3=\begin{pmatrix}-\frac12\\0\\0\end{pmatrix}
+s\begin{pmatrix}-1\\1\\0\end{pmatrix}
+t\begin{pmatrix}0\\0\\1\end{pmatrix},
$$
其中 $k,s,t\in\mathbb R$。

（B）对任意这样的 $\xi_2,\xi_3$，向量组 $\xi_1,\xi_2,\xi_3$ 都线性无关。

### 解析

**（A）求 $\xi_2$ 与 $\xi_3$**

先解方程 $A\xi_2=\xi_1$。注意到
$$
A\begin{pmatrix}0\\0\\1\end{pmatrix}
=
\begin{pmatrix}-1\\1\\-2\end{pmatrix}
=\xi_1,
$$
所以 $\begin{pmatrix}0\\0\\1\end{pmatrix}$ 是一个特解。

再解齐次方程 $A\xi=0$。行变换可得它的基础解系为
$$
\begin{pmatrix}1\\-1\\2\end{pmatrix}.
$$
因而
$$
\xi_2=\begin{pmatrix}0\\0\\1\end{pmatrix}
+k\begin{pmatrix}1\\-1\\2\end{pmatrix},\qquad k\in\mathbb R.
$$

再求 $A^2$：
$$
A^2=
\begin{pmatrix}
2 & 2 & 0 \\
-2 & -2 & 0 \\
4 & 4 & 0
\end{pmatrix}.
$$
注意到
$$
A^2\begin{pmatrix}-\frac12\\0\\0\end{pmatrix}
=
\begin{pmatrix}-1\\1\\-2\end{pmatrix}
=\xi_1,
$$
所以 $\begin{pmatrix}-\frac12\\0\\0\end{pmatrix}$ 是一个特解。

解齐次方程 $A^2\xi=0$，可得基础解系为
$$
\begin{pmatrix}-1\\1\\0\end{pmatrix},
\qquad
\begin{pmatrix}0\\0\\1\end{pmatrix}.
$$
故
$$
\xi_3=\begin{pmatrix}-\frac12\\0\\0\end{pmatrix}
+s\begin{pmatrix}-1\\1\\0\end{pmatrix}
+t\begin{pmatrix}0\\0\\1\end{pmatrix},
\qquad s,t\in\mathbb R.
$$

**（B）证明线性无关**

设
$$
\xi_2=\begin{pmatrix}k\\-k\\1+2k\end{pmatrix},\qquad
\xi_3=\begin{pmatrix}-s-\frac12\\ s\\ t\end{pmatrix}.
$$
则以 $\xi_1,\xi_2,\xi_3$ 为列向量组成矩阵
$$
M=\begin{pmatrix}
-1 & k & -s-\frac12 \\
1 & -k & s \\
-2 & 1+2k & t
\end{pmatrix}.
$$

直接计算行列式：
$$
|M|=-\frac12\ne0.
$$

因此无论参数 $k,s,t$ 取何值，$\xi_1,\xi_2,\xi_3$ 始终线性无关。

## 第 21 题

### 标准答案

（A）特征值为
$$
a,\quad a-2,\quad a+1.
$$

（B）$a=2$。

### 解析

二次型对应的对称矩阵为
$$
A=\begin{pmatrix}
a & 0 & 1 \\
0 & a & -1 \\
1 & -1 & a-1
\end{pmatrix}.
$$

**（A）求特征值**

其特征多项式为
$$
|\lambda I-A|
=
\begin{vmatrix}
\lambda-a & 0 & -1 \\
0 & \lambda-a & 1 \\
-1 & 1 & \lambda-a+1
\end{vmatrix}.
$$
计算得
$$
|\lambda I-A|
=(\lambda-a)(\lambda-a+2)(\lambda-a-1).
$$

所以特征值为
$$
\lambda_1=a,\qquad \lambda_2=a-2,\qquad \lambda_3=a+1.
$$

**（B）由规范形求 $a$**

规范形为 $y_1^2+y_2^2$，说明该二次型有两个正惯性指标、一个零惯性指标，因此三个特征值中恰有两个为正、一个为零。

分别令三个特征值为零：

1. 若 $a=0$，则特征值为 $0,-2,1$，不符合；
2. 若 $a=2$，则特征值为 $2,0,3$，符合；
3. 若 $a=-1$，则特征值为 $-1,-3,0$，不符合。

因此
$$
a=2.
$$

## 第 22 题

### 标准答案

（A）
$$
f_{Y\mid X}(y\mid x)=
\begin{cases}
\dfrac1x, & 0<y<x, \\
0, & \text{其他}.
\end{cases}
$$

（B）
$$
P\!\left(X\le1\mid Y\le1\right)=\frac{e-2}{e-1}.
$$

### 解析

**（A）求条件密度**

先求 $X$ 的边缘密度。对 $x>0$，
$$
f_X(x)=\int_0^x e^{-x}\,dy=xe^{-x}.
$$

因而
$$
f_{Y\mid X}(y\mid x)=\frac{f(x,y)}{f_X(x)}
=
\begin{cases}
\dfrac{e^{-x}}{xe^{-x}}=\dfrac1x, & 0<y<x, \\
0, & \text{其他}.
\end{cases}
$$

**（B）求条件概率**

由定义，
$$
P(X\le1\mid Y\le1)=\frac{P(X\le1,\ Y\le1)}{P(Y\le1)}.
$$

先算分子。由于当 $0<x\le1$ 时必有 $0<y<x\le1$，
$$
P(X\le1,\ Y\le1)
=\int_0^1\int_0^x e^{-x}\,dy\,dx
=\int_0^1 xe^{-x}\,dx
=1-\frac2e.
$$

再算分母。先求 $Y$ 的边缘密度：
$$
f_Y(y)=\int_y^\infty e^{-x}\,dx=e^{-y},\qquad y>0.
$$
因此
$$
P(Y\le1)=\int_0^1 e^{-y}\,dy=1-\frac1e.
$$

所以
$$
P(X\le1\mid Y\le1)
=\frac{1-\frac2e}{1-\frac1e}
=\frac{e-2}{e-1}.
$$

## 第 23 题

### 标准答案

（A）
$$
P(X=1\mid Z=0)=\frac49.
$$

（B）$(X,Y)$ 的分布表为

| $Y\backslash X$ | $0$ | $1$ | $2$ |
| --- | --- | --- | --- |
| $0$ | $\frac14$ | $\frac16$ | $\frac1{36}$ |
| $1$ | $\frac13$ | $\frac19$ | $0$ |
| $2$ | $\frac19$ | $0$ | $0$ |

### 解析

设每次取球中，红球、黑球、白球的概率分别为
$$
p_R=\frac16,\qquad p_B=\frac13,\qquad p_W=\frac12.
$$
因为是有放回抽样，两次取球相互独立。

**（A）求 $P(X=1\mid Z=0)$**

条件 $Z=0$ 表示两次都没有取到白球。此时样本空间压缩为“只看红球和黑球”，条件下的单次概率变为
$$
P(R\mid \text{非白})=\frac{1/6}{1/6+1/3}=\frac13,\qquad
P(B\mid \text{非白})=\frac23.
$$

因而在条件 $Z=0$ 下，两次取球相当于进行两次独立的“红/黑”试验，所以
$$
P(X=1\mid Z=0)=2\cdot\frac13\cdot\frac23=\frac49.
$$

**（B）求 $(X,Y)$ 的概率分布**

因为两次取球，所以 $X,Y$ 只能取满足 $i,j\ge0$ 且 $i+j\le2$ 的整数。并且
$$
P(X=i,Y=j)
=\frac{2!}{i!\,j!\,(2-i-j)!}
\left(\frac16\right)^i
\left(\frac13\right)^j
\left(\frac12\right)^{2-i-j}.
$$

逐项计算得：

| $Y\backslash X$ | $0$ | $1$ | $2$ |
| --- | --- | --- | --- |
| $0$ | $\frac14$ | $\frac16$ | $\frac1{36}$ |
| $1$ | $\frac13$ | $\frac19$ | $0$ |
| $2$ | $\frac19$ | $0$ | $0$ |

其余取值的概率都为 $0$。
