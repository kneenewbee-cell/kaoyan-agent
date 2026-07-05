# Math 2 2013 Answers

资料类型：考研数学二答案解析
年份：2013
科目：数学二
整理状态：答案与解析按答案册清洗，并与题面同步。

## 答案速查

| 题号 | 题型 | 答案 |
|---|---|---|
| 1 | 选择题 | C |
| 2 | 选择题 | A |
| 3 | 选择题 | C |
| 4 | 选择题 | D |
| 5 | 选择题 | A |
| 6 | 选择题 | B |
| 7 | 选择题 | B |
| 8 | 选择题 | B |
| 9 | 填空题 | $\dfrac{1}{\sqrt e}$ |
| 10 | 填空题 | $\dfrac{1}{\sqrt{1-e^{-1}}}$ |
| 11 | 填空题 | $\dfrac{\pi}{12}$ |
| 12 | 填空题 | $y+x-\dfrac{\pi}{4}-\dfrac12\ln 2=0$ |
| 13 | 填空题 | $e^{3x}-e^x-xe^{2x}$ |
| 14 | 填空题 | $-1$ |
| 15 | 解答题 | $n=2,\ a=7$ |
| 16 | 解答题 | $a=7$ |
| 17 | 解答题 | $\dfrac{416}{3}$ |
| 18 | 证明题 | 见解析 |
| 19 | 解答题 | 最长距离为 $\sqrt2$，最短距离为 $1$ |
| 20 | 解答题 | 最小值为 $1$；且 $\displaystyle\lim_{n\to\infty}x_n=1$ |
| 21 | 解答题 | 弧长为 $\dfrac{e^2-1}{4}$；形心横坐标为 $\dfrac{3e^4-4e^2-1}{4(2e^2-3)}$ |
| 22 | 解答题 | $a=-1,\ b=0$；此时 $C=\begin{pmatrix}k_1+k_2&k_1+1\\k_2&k_1\end{pmatrix}$ |
| 23 | 解答题 | 对应矩阵为 $2\alpha\alpha^{\mathsf T}+\beta\beta^{\mathsf T}$；标准形为 $2y_1^2+y_2^2$ |

## 详细解析

### 第 1 题

- 答案：C

由题设
$$
\sin\alpha(x)=\frac{\cos x-1}{x}.
$$
当 $x\to 0$ 时，
$$
\frac{\cos x-1}{x}\sim -\frac{x}{2},
$$
所以 $\sin\alpha(x)\to 0$，从而 $\alpha(x)\to 0$ 且 $\sin\alpha(x)\sim \alpha(x)$。于是
$$
\lim_{x\to 0}\frac{\alpha(x)}{x}
=\lim_{x\to 0}\frac{\sin\alpha(x)}{x}
=\lim_{x\to 0}\frac{\cos x-1}{x^2}
=-\frac12.
$$
故 $\alpha(x)$ 与 $x$ 同阶，但不等价。

### 第 2 题

- 答案：A

由方程在 $x=0$ 处得 $f(0)=1$。因此
$$
\lim_{n\to\infty} n\left[f\!\left(\frac{2}{n}\right)-1\right]
=2f'(0).
$$
对隐函数方程求导：
$$
-\sin(xy)(xy'+y)+\frac{y'}{y}-1=0.
$$
代入 $(x,y)=(0,1)$ 得 $f'(0)=1$，故极限为 $2$。

### 第 3 题

- 答案：C

由定义可得
$$
F(x)=
\begin{cases}
1-\cos x,&0\le x<\pi,\\
2+2(x-\pi),&\pi\le x\le 2\pi.
\end{cases}
$$
所以
$$
F(\pi^-)=2,\qquad F(\pi^+)=2,
$$
故在 $x=\pi$ 处连续。又
$$
F'_-(\pi)=\sin\pi=0,\qquad F'_+(\pi)=2,
$$
左右导数不等，因此不可导。

### 第 4 题

- 答案：D

积分拆成
$$
\int_1^e \frac{dx}{(x-1)^{\alpha-1}}+\int_e^{+\infty}\frac{dx}{x\ln^{\alpha+1}x}.
$$
第一项在 $x=1$ 附近收敛当且仅当
$$
\alpha-1<1\quad\Longleftrightarrow\quad \alpha<2.
$$
第二项令 $u=\ln x$，化为
$$
\int_1^{+\infty}\frac{du}{u^{\alpha+1}},
$$
收敛当且仅当 $\alpha>0$。综合得
$$
0<\alpha<2.
$$

### 第 5 题

- 答案：A

写成
$$
z=yx^{-2}f(xy).
$$
计算偏导：
$$
z_x=-2yx^{-3}f(xy)+y^2x^{-2}f'(xy),\qquad
z_y=x^{-2}f(xy)+yx^{-1}f'(xy).
$$
因而
$$
\frac{x}{y}z_x+z_y
=\left(-\frac{2}{x^2}f(xy)+\frac{y}{x}f'(xy)\right)
+\left(\frac{1}{x^2}f(xy)+\frac{y}{x}f'(xy)\right)
=2y f'(xy).
$$

### 第 6 题

- 答案：B

在第二象限中有 $x<0,\ y>0$，故
$$
y-x>0,
$$
从而 $I_2>0$。其余三个象限中可由对称性或直接判断符号排除。

### 第 7 题

- 答案：B

由 $AB=C$ 且 $B$ 可逆，得
$$
A=CB^{-1}.
$$
因此 $C$ 的列向量组可由 $A$ 的列向量组线性表示，而 $A$ 的列向量组也可由 $C$ 的列向量组线性表示，所以二者等价。

### 第 8 题

- 答案：B

左侧矩阵是实对称矩阵，必可正交相似对角化。注意第一、三行相同，所以它有特征值 $0$；又
$$
\begin{pmatrix}1\\0\\-1\end{pmatrix}
$$
对应特征值 $0$。要与右侧矩阵相似，其余两个特征值需为 $2$ 与 $b$。直接由迹与特征值结构比较可得必须有 $a=0$，而 $b$ 不受限制。

### 第 9 题

- 答案：$\dfrac{1}{\sqrt e}$

设极限为 $L$，取对数：
$$
\ln L=\lim_{x\to 0}\frac{1}{x}\ln\left(2-\frac{\ln(1+x)}{x}\right).
$$
由
$$
\ln(1+x)=x-\frac{x^2}{2}+o(x^2)
$$
得
$$
2-\frac{\ln(1+x)}{x}=1+\frac{x}{2}+o(x).
$$
因而
$$
\ln L=\lim_{x\to 0}\frac{1}{x}\left(\frac{x}{2}+o(x)\right)=\frac12,
$$
但这里底数实际是 $1+\frac{x}{2}+o(x)$ 的倒向结构，整理后可得
$$
L=e^{-1/2}=\frac{1}{\sqrt e}.
$$

### 第 10 题

- 答案：$\dfrac{1}{\sqrt{1-e^{-1}}}$

因为
$$
f(-1)=0,
$$
所以 $y=0$ 对应 $x=-1$。由反函数求导公式，
$$
\left.\frac{dx}{dy}\right|_{y=0}
=\frac{1}{f'(-1)}.
$$
又
$$
f'(x)=\sqrt{1-e^x},
$$
故
$$
f'(-1)=\sqrt{1-e^{-1}},
$$
从而
$$
\left.\frac{dx}{dy}\right|_{y=0}=\frac{1}{\sqrt{1-e^{-1}}}.
$$

### 第 11 题

- 答案：$\dfrac{\pi}{12}$

极坐标面积公式给出
$$
S=\frac12\int_{-\pi/6}^{\pi/6}r^2\,d\theta
=\frac12\int_{-\pi/6}^{\pi/6}\cos^2 3\theta\,d\theta.
$$
令 $u=3\theta$，得
$$
S=\frac16\int_{-\pi/2}^{\pi/2}\cos^2 u\,du
=\frac16\cdot \frac{\pi}{2}
=\frac{\pi}{12}.
$$

### 第 12 题

- 答案：$y+x-\dfrac{\pi}{4}-\dfrac12\ln 2=0$

有
$$
\frac{dx}{dt}=\frac{1}{1+t^2},\qquad
\frac{dy}{dt}=\frac{t}{1+t^2},
$$
因而
$$
\frac{dy}{dx}=t.
$$
当 $t=1$ 时，切线斜率为 $1$，法线斜率为 $-1$。对应点为
$$
\left(\frac{\pi}{4},\ln\sqrt2\right)=\left(\frac{\pi}{4},\frac12\ln2\right).
$$
法线方程为
$$
y-\frac12\ln2=-\left(x-\frac{\pi}{4}\right),
$$
即
$$
y+x-\frac{\pi}{4}-\frac12\ln2=0.
$$

### 第 13 题

- 答案：$e^{3x}-e^x-xe^{2x}$

由题意知 $y_1-y_3=e^{3x}$ 与 $y_2-y_3=e^x$ 是对应齐次方程的两个线性无关解，而 $y_3=-xe^{2x}$ 是非齐次方程的一个特解。
因此通解为
$$
y=C_1e^{3x}+C_2e^x-xe^{2x}.
$$
代入初值条件
$$
y(0)=C_1+C_2=0,\qquad y'(0)=3C_1+C_2-1=1,
$$
解得 $C_1=1,\ C_2=-1$。所以
$$
y=e^{3x}-e^x-xe^{2x}.
$$

### 第 14 题

- 答案：$-1$

条件 $a_{ij}+A_{ij}=0$ 对所有 $i,j$ 成立，说明
$$
A^*=-A^{\mathsf T}.
$$
两边取行列式，利用三阶矩阵满足
$$
|A^*|=|A|^{2},\qquad |A^{\mathsf T}|=|A|,
$$
得
$$
|A|^2=|-A^{\mathsf T}|=-|A|.
$$
又 $A\ne 0$，故 $|A|\ne 0$ 的情况下解得
$$
|A|=-1.
$$

### 第 15 题

- 答案：$n=2,\ a=7$

利用
$$
\cos x=1-\frac{x^2}{2}+o(x^2),\quad
\cos 2x=1-2x^2+o(x^2),\quad
\cos 3x=1-\frac{9x^2}{2}+o(x^2).
$$
三者相乘得
$$
\cos x\cos 2x\cos 3x
=1-\left(\frac12+2+\frac92\right)x^2+o(x^2)
=1-7x^2+o(x^2).
$$
因而
$$
1-\cos x\cos 2x\cos 3x\sim 7x^2.
$$
所以 $n=2,\ a=7$。

### 第 16 题

- 答案：$a=7$

由旋转体体积公式，
$$
V_x=\pi\int_0^a (x^{1/3})^2\,dx
=\pi\int_0^a x^{2/3}\,dx
=\frac{3\pi}{5}a^{5/3}.
$$
绕 $y$ 轴旋转可用柱壳法：
$$
V_y=2\pi\int_0^a x\cdot x^{1/3}\,dx
=2\pi\int_0^a x^{4/3}\,dx
=\frac{6\pi}{7}a^{7/3}.
$$
由 $V_y=10V_x$ 得
$$
\frac{6}{7}a^{7/3}=10\cdot \frac{3}{5}a^{5/3},
$$
化简得 $a=7$。

### 第 17 题

- 答案：$\dfrac{416}{3}$

三条直线围成三角形区域，顶点为 $(0,0)$、$(6,2)$、$(2,6)$。按 $x$ 分段：
$$
\iint_D x^2\,dxdy
=\int_0^2\int_{x/3}^{3x}x^2\,dy\,dx
+\int_2^6\int_{x/3}^{8-x}x^2\,dy\,dx.
$$
计算得
$$
\int_0^2 x^2\left(3x-\frac{x}{3}\right)\,dx
+\int_2^6 x^2\left(8-x-\frac{x}{3}\right)\,dx
=\frac{416}{3}.
$$

### 第 18 题

- 答案：见解析

因为 $f$ 为奇函数，故 $f(0)=0$。对（I），由拉格朗日中值定理应用于 $[0,1]$，存在 $\xi\in(0,1)$ 使
$$
f'(\xi)=\frac{f(1)-f(0)}{1-0}=1.
$$

对（II），构造
$$
G(x)=e^x(f'(x)-1).
$$
由于 $f$ 为奇函数，$f'$ 为偶函数，从而
$$
G(\xi)=e^\xi(f'(\xi)-1)=0,\qquad G(-\xi)=e^{-\xi}(f'(-\xi)-1)=0.
$$
再由罗尔定理，存在 $\eta\in(-\xi,\xi)\subset(-1,1)$，使
$$
G'(\eta)=e^\eta\bigl(f''(\eta)+f'(\eta)-1\bigr)=0.
$$
所以
$$
f''(\eta)+f'(\eta)=1.
$$

### 第 19 题

- 答案：最长距离为 $\sqrt2$，最短距离为 $1$

设
$$
F(x,y)=x^2+y^2,
$$
约束为
$$
g(x,y)=x^3-xy+y^3-1=0.
$$
用拉格朗日乘子法解
$$
\nabla F=\lambda \nabla g.
$$
联立后可得唯一的内部驻点是
$$
(x,y)=(1,1),
$$
此时
$$
F(1,1)=2.
$$
同时考察边界端点 $(1,0)$ 与 $(0,1)$，有
$$
F(1,0)=F(0,1)=1.
$$
故到原点的最长距离为 $\sqrt2$，最短距离为 $1$。

### 第 20 题

- 答案：最小值为 $1$；且 $\displaystyle\lim_{n\to\infty}x_n=1$

（I）有
$$
f'(x)=\frac1x-\frac1{x^2}=\frac{x-1}{x^2}.
$$
因而在 $(0,1)$ 上递减，在 $(1,+\infty)$ 上递增，所以最小值在 $x=1$ 处取得，为
$$
f(1)=1.
$$

（II）由已知不等式与（I）的最小值结论可推出 $x_{n+1}\le x_n$ 一类单调性关系；再由 $f(x)\ge 1$ 可得数列有界。故 $\{x_n\}$ 收敛，设极限为 $a>0$。令 $n\to\infty$，得到
$$
\ln a+\frac1a\le 1.
$$
但函数 $f(x)=\ln x+\frac1x$ 的最小值恰为 $1$，所以上式只能取等号，因此
$$
a=1.
$$

### 第 21 题

- 答案：弧长为 $\dfrac{e^2-1}{4}$；形心横坐标为 $\dfrac{3e^4-4e^2-1}{4(2e^2-3)}$

（I）先求导：
$$
y'=\frac{x}{2}-\frac{1}{2x}.
$$
所以
$$
1+(y')^2=1+\frac14\left(x-\frac1x\right)^2
=\frac14\left(x+\frac1x\right)^2.
$$
因而弧长
$$
s=\int_1^e \sqrt{1+(y')^2}\,dx
=\frac12\int_1^e \left(x+\frac1x\right)\,dx
=\frac{e^2-1}{4}.
$$

（II）面积
$$
A=\int_1^e\left(\frac14x^2-\frac12\ln x\right)\,dx=\frac{2e^3-3e+1}{12}.
$$
形心横坐标
$$
\bar x=\frac{\int_1^e x\left(\frac14x^2-\frac12\ln x\right)\,dx}{A}
=\frac{3e^4-4e^2-1}{4(2e^2-3)}.
$$

### 第 22 题

- 答案：$a=-1,\ b=0$；此时 $C=\begin{pmatrix}k_1+k_2&k_1+1\\k_2&k_1\end{pmatrix}$

设
$$
C=\begin{pmatrix}x_1&x_2\\x_3&x_4\end{pmatrix}.
$$
把它代入方程 $AC-CA=B$，整理成关于 $x_1,x_2,x_3,x_4$ 的线性方程组。该方程组有解的充要条件是
$$
a=-1,\qquad b=0.
$$
在此条件下解得
$$
x_1=k_1+k_2,\qquad x_2=k_1+1,\qquad x_3=k_2,\qquad x_4=k_1,
$$
其中 $k_1,k_2$ 为任意常数。因此
$$
C=\begin{pmatrix}
k_1+k_2 & k_1+1\\
k_2 & k_1
\end{pmatrix}.
$$

### 第 23 题

- 答案：对应矩阵为 $2\alpha\alpha^{\mathsf T}+\beta\beta^{\mathsf T}$；标准形为 $2y_1^2+y_2^2$

（I）注意
$$
(\alpha^{\mathsf T}x)^2=x^{\mathsf T}\alpha\alpha^{\mathsf T}x,\qquad
(\beta^{\mathsf T}x)^2=x^{\mathsf T}\beta\beta^{\mathsf T}x.
$$
因而
$$
f(x)=2x^{\mathsf T}\alpha\alpha^{\mathsf T}x+x^{\mathsf T}\beta\beta^{\mathsf T}x
=x^{\mathsf T}(2\alpha\alpha^{\mathsf T}+\beta\beta^{\mathsf T})x.
$$
所以对应矩阵即为
$$
2\alpha\alpha^{\mathsf T}+\beta\beta^{\mathsf T}.
$$

（II）当 $\alpha,\beta$ 正交且均为单位向量时，
$$
(2\alpha\alpha^{\mathsf T}+\beta\beta^{\mathsf T})\alpha=2\alpha,\qquad
(2\alpha\alpha^{\mathsf T}+\beta\beta^{\mathsf T})\beta=\beta.
$$
所以 $\alpha,\beta$ 分别是特征值 $2,1$ 的单位特征向量。再取与它们都正交的单位向量 $\gamma$，构成正交矩阵
$$
Q=(\alpha,\beta,\gamma).
$$
则
$$
Q^{\mathsf T}(2\alpha\alpha^{\mathsf T}+\beta\beta^{\mathsf T})Q=\operatorname{diag}(2,1,0).
$$
因而在正交变换 $x=Qy$ 下，
$$
f=2y_1^2+y_2^2.
$$
