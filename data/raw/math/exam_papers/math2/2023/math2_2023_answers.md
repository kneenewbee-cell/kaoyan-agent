# 2023 年数学二答案解析

资料类型：考研数学二答案解析
年份：2023
科目：数学二
整理状态：仅保留答案合集中的数学二页面（第 3、4 页），并结合题面补全简洁解析。

**答案页图 3**

![2023 数学二答案页 3](images/answer_pages/page-3.png)

**答案页图 4**

![2023 数学二答案页 4](images/answer_pages/page-4.png)

## 答案速查

| 题号 | 题型 | 答案 |
|---|---|---|
| 1 | 选择题 | B |
| 2 | 选择题 | D |
| 3 | 选择题 | B |
| 4 | 选择题 | C |
| 5 | 选择题 | C |
| 6 | 选择题 | A |
| 7 | 选择题 | C |
| 8 | 选择题 | D |
| 9 | 选择题 | B |
| 10 | 选择题 | D |
| 11 | 填空题 | $-2$ |
| 12 | 填空题 | $\sqrt{3}+\dfrac{4\pi}{3}$ |
| 13 | 填空题 | $-\dfrac{3}{2}$ |
| 14 | 填空题 | $-\dfrac{11}{9}$ |
| 15 | 填空题 | $\dfrac{1}{2}$ |
| 16 | 填空题 | $8$ |
| 17 | 解答题 | (1) $y(x)=x(2-\ln x)$； (2) 当点为 $\left(e^{3/2},\dfrac12e^{3/2}\right)$ 时面积最小，最小面积为 $e^3$。 |
| 18 | 解答题 | 极小值为 $f(-e,k\pi)=-\dfrac{e^2}{2}$，其中 $k$ 为偶整数；无极大值。 |
| 19 | 解答题 | (1) 面积为 $\ln(\sqrt2+1)$； (2) 旋转体体积为 $\pi\left(1-\dfrac{\pi}{4}\right)$。 |
| 20 | 解答题 | $\dfrac{\pi\ln 2}{8\sqrt3}$ |
| 21 | 证明题 | 结论成立。 |
| 22 | 解答题 | (1) $A=\begin{pmatrix}1&1&1\\2&-1&1\\0&1&-1\end{pmatrix}$； (2) 可取 $P=\begin{pmatrix}4&0&-1\\3&-1&0\\1&1&2\end{pmatrix},\qquad \Lambda=\operatorname{diag}(2,-2,-1).$ |

## 详细解析

### 第 1 题

- 答案：B

当 $x\to\infty$ 时，$\ln\left(e+\dfrac{1}{x-1}\right)=1+\dfrac{1}{e(x-1)}+o\left(\dfrac1x\right)$，故
$$
y=x+\frac{x}{e(x-1)}+o(1)=x+\frac1e+o(1).
$$
所以斜渐近线为 $y=x+\dfrac1e$。

### 第 2 题

- 答案：D

左段原函数可取 $\ln(\sqrt{1+x^2}+x)+C$，右段原函数可取 $(x+1)\sin x+\cos x$。又 $F(0^+)=1$，故左段常数应取 $1$，于是选 $D$。

### 第 3 题

- 答案：B

由 $0<\sin t<t\ (t>0)$ 知 $x_n\downarrow0$，且 $x_n-\sin x_n\sim \dfrac{x_n^3}{6}$，所以 $x_n$ 只按幂次速度趋于零。另一方面
$$
y_n=\left(\frac12\right)^{2^{n-1}},
$$
按双指数速度趋于零，因此 $\dfrac{y_n}{x_n}\to0$，故选 $B$。

### 第 4 题

- 答案：C

全部解在整个实轴上有界时，特征根只能是共轭纯虚根 $\pm i\omega\ (\omega\ne0)$，故 $a=0$，$b=\omega^2>0$，所以选 $C$。

### 第 5 题

- 答案：C

当 $t<0$ 时 $f(x)=-x\sin x$；当 $t\ge0$ 时 $f(x)=\dfrac{x}{3}\sin\dfrac{x}{3}$。由此可算得 $f'(0^-)=f'(0^+)=0$，故 $f'$ 在 $0$ 处连续；但 $f''(0^-)=2$，$f''(0^+)=\dfrac23$，故 $f''(0)$ 不存在，选 $C$。

### 第 6 题

- 答案：A

令 $u=\ln x$，则
$$
f(\alpha)=\int_{\ln2}^{+\infty}u^{-\alpha-1}\,du=\frac{(\ln2)^{-\alpha}}{\alpha}\quad(\alpha>0).
$$
对 $\ln f(\alpha)$ 求导得极值条件 $-\ln(\ln2)-\dfrac1\alpha=0$，故
$$
\alpha_0=-\frac1{\ln(\ln2)}.
$$

### 第 7 题

- 答案：C

由
$$
f'(x)=e^x(x^2+2x+a)=e^x[(x+1)^2+a-1]
$$
知无极值点需 $a\ge1$；又
$$
f''(x)=e^x(x^2+4x+a+2)=e^x[(x+2)^2+a-2]
$$
有拐点需 $a<2$。综上 $1\le a<2$，选 $C$。

### 第 8 题

- 答案：D

设 $M=\begin{pmatrix}A&E\\O&B\end{pmatrix}$，则
$$
M^{-1}=\begin{pmatrix}A^{-1}&-A^{-1}B^{-1}\\O&B^{-1}\end{pmatrix}.
$$
由 $M^*=|M|M^{-1}=|A||B|M^{-1}$ 得
$$
M^*=\begin{pmatrix}|B|A^*&-A^*B^*\\O&|A|B^*\end{pmatrix},
$$
故选 $D$。

### 第 9 题

- 答案：B

该二次型对应对称矩阵恰有一个正惯性指数和一个负惯性指数，秩为 $2$，故其规范形为 $y_1^2-y_2^2$，选 $B$。

### 第 10 题

- 答案：D

设 $\gamma=s\alpha_1+t\alpha_2=u\beta_1+v\beta_2$，按分量联立可得公共表示空间是一条直线，其方向向量为 $(1,5,8)^T$，故选 $D$。

### 第 11 题

- 答案：$-2$

展开得 $f(x)=(a+1)x+\left(b-\dfrac12\right)x^2+o(x^2)$，$g(x)=\dfrac32x^2+o(x^2)$。故 $a=-1$，$b=2$，于是 $ab=-2$。

### 第 12 题

- 答案：$\sqrt{3}+\dfrac{4\pi}{3}$

由 $y'=\sqrt{3-x^2}$，弧长为
$$
L=\int_{-\sqrt3}^{\sqrt3}\sqrt{1+y'^2}\,dx=\int_{-\sqrt3}^{\sqrt3}\sqrt{4-x^2}\,dx=\sqrt3+\frac{4\pi}{3}.
$$

### 第 13 题

- 答案：$-\dfrac{3}{2}$

由 $(1,1)$ 代入得对应 $z=0$。设 $F=e^z+xz-2x+y$，先求 $z_x=\dfrac{2-z}{e^z+x}$，在 $(1,1,0)$ 处有 $z_x=1$。再对方程两次求偏导可得 $(e^z+x)z_{xx}+(e^z z_x+1)z_x+z_x=0$，代入得 $2z_{xx}+3=0$，故 $z_{xx}=-\dfrac32$。

### 第 14 题

- 答案：$-\dfrac{11}{9}$

当 $x=1$ 时解得 $y=1$。对方程求导得 $9x^2=(5y^4+6y^2)y'$，故在 $(1,1)$ 处 $y'=\dfrac9{11}$。法线斜率为其负倒数，故为 $-\dfrac{11}{9}$。

### 第 15 题

- 答案：$\dfrac{1}{2}$

利用 $f(x+2)=f(x)+x$ 作平移，可得
$$
\int_1^3f(x)dx=\int_{-1}^1f(u)du.
$$
再由 $\int_0^2f(x)dx=0$ 消去中间项，最终得到 $\int_1^3f(x)dx=\dfrac12$。

### 第 16 题

- 答案：$8$

先由 $a^3-3a+2=4$ 得 $(a-2)(a+1)^2=0$，故 $a=2$ 或 $a=-1$。再用方程组可解条件分别求得 $b=-4$ 或 $b=\dfrac72$。代入
$$
a^3-ab-2a+b
$$
两种情形都得 $8$。

### 第 17 题

- 答案：(1) $y(x)=x(2-\ln x)$；

(2) 当点为 $\left(e^{3/2},\dfrac12e^{3/2}\right)$ 时面积最小，最小面积为 $e^3$。

设切线斜率为 $y'$，则切线在 $y$ 轴上的截距为 $y-xy'$。由题意有 $y-xy'=x$，即
$$
y'-\frac{1}{x}y=-1.
$$
解得 $y=x(C-\ln x)$。再由 $(e^2,0)$ 得 $C=2$，故 $y=x(2-\ln x)$。又切线与坐标轴围成三角形面积
$$
S=\frac{x^2}{2(\ln x-1)}
$$
在 $x>e$ 上取极小。令 $t=\ln x$，解得最优点 $t=\dfrac32$，于是
$$
\left(x,y\right)=\left(e^{3/2},\frac12e^{3/2}\right),\qquad S_{\min}=e^3.
$$

### 第 18 题

- 答案：极小值为 $f(-e,k\pi)=-\dfrac{e^2}{2}$，其中 $k$ 为偶整数；无极大值。

由 $f_x=e^{\cos y}+x$、$f_y=-xe^{\cos y}\sin y$，驻点满足 $x=-e^{\cos y}$ 且 $\sin y=0$，即 $y=k\pi$。当 $k$ 为偶数时驻点为 $(-e,2m\pi)$，此时 Hessian 判别为极小点，极小值为 $-\dfrac{e^2}{2}$；当 $k$ 为奇数时为鞍点，所以无极大值。

### 第 19 题

- 答案：(1) 面积为 $\ln(\sqrt2+1)$；

(2) 旋转体体积为 $\pi\left(1-\dfrac{\pi}{4}\right)$。

(1) 面积为
$$
\int_1^{+\infty}\frac{1}{x\sqrt{1+x^2}}dx.
$$
作 $x=\tan\theta$ 可得结果 $\ln(\sqrt2+1)$。

(2) 体积为
$$
\pi\int_1^{+\infty}\frac{1}{x^2(1+x^2)}dx
=\pi\int_1^{+\infty}\left(\frac1{x^2}-\frac1{1+x^2}\right)dx,
$$
故结果为 $\pi\left(1-\dfrac\pi4\right)$。

### 第 20 题

- 答案：$\dfrac{\pi\ln 2}{8\sqrt3}$

令 $t=\dfrac{y}{x}$，则 $y=tx$，且 $0\le t\le\sqrt3$。区域条件化为
$$
1\le x^2(1+t^2-t)\le2,
$$
故对固定 $t$，
$$
\sqrt{\frac1{1+t^2-t}}\le x\le \sqrt{\frac2{1+t^2-t}}.
$$
又 Jacobian 为 $x$，所以
$$
I=\int_0^{\sqrt3}\int_{\sqrt{1/(1+t^2-t)}}^{\sqrt{2/(1+t^2-t)}}\frac{1}{x(3+t^2)}dxdt
=\frac{\ln2}{2}\int_0^{\sqrt3}\frac{dt}{3+t^2}
=\frac{\pi\ln2}{8\sqrt3}.
$$

### 第 21 题

- 答案：结论成立。

(1) 在 $0$ 处对 $f(a),f(-a)$ 作 Taylor 展开：
$$
f(a)=f(0)+af'(0)+\frac{a^2}{2}f''(\xi_1),\qquad
f(-a)=f(0)-af'(0)+\frac{a^2}{2}f''(\xi_2).
$$
由 $f(0)=0$ 相加得
$$
\frac{f(a)+f(-a)}{a^2}=\frac{f''(\xi_1)+f''(\xi_2)}{2}.
$$
因 $f''$ 连续，故由介值定理存在 $\xi\in(-a,a)$ 使上式右端等于 $f''(\xi)$。

(2) 设 $x_0\in(-a,a)$ 为极值点，则 $f'(x_0)=0$。在 $x_0$ 处分别展开 $f(a),f(-a)$，相减得
$$
f(a)-f(-a)=\frac{(a-x_0)^2}{2}f''(\eta_1)-\frac{(a+x_0)^2}{2}f''(\eta_2).
$$
令 $M=\max_{[-a,a]}|f''(x)|$，则
$$
|f(a)-f(-a)|\le\frac{(a-x_0)^2+(a+x_0)^2}{2}M\le2a^2M.
$$
所以
$$
M\ge\frac{1}{2a^2}|f(a)-f(-a)|.
$$
由连续性，存在 $\eta\in(-a,a)$ 使 $|f''(\eta)|=M$，结论成立。

### 第 22 题

- 答案：(1) $A=\begin{pmatrix}1&1&1\\2&-1&1\\0&1&-1\end{pmatrix}$；

(2) 可取
$$
P=\begin{pmatrix}4&0&-1\\3&-1&0\\1&1&2\end{pmatrix},\qquad
\Lambda=\operatorname{diag}(2,-2,-1).
$$

由线性变换对标准基的作用直接得到
$$
A=\begin{pmatrix}1&1&1\\2&-1&1\\0&1&-1\end{pmatrix}.
$$
再算得特征多项式为 $(\lambda-2)(\lambda+2)(\lambda+1)$，对应可取特征向量 $(4,3,1)^T,(0,-1,1)^T,(-1,0,2)^T$。以它们为列组成
$$
P=\begin{pmatrix}4&0&-1\\3&-1&0\\1&1&2\end{pmatrix},
$$
则 $P^{-1}AP=\operatorname{diag}(2,-2,-1)$。
