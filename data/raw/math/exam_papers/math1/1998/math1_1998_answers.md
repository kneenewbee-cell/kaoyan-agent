# Math 1 1998 Answers

资料类型：考研数学一答案解析
年份：1998
科目：数学一
范围：试卷 I
来源：D:\百度网盘\高数资料\【02】1987-2022年数学一真题详解答案（PDF）\1998考研数学一真题解析.pdf
校对状态：已按题干和答案页图像重新清洗，去除 OCR 碎行、串题内容和非本题页脚

## 答案速查

| 题号 | 题型 | 答案 |
|---|---|---|
| 1 | 填空题 | $-\dfrac{1}{4}$ |
| 2 | 填空题 | $y f''(xy)+\varphi'(x+y)+y\varphi''(x+y)$ |
| 3 | 填空题 | $12a$ |
| 4 | 填空题 | $\left(\dfrac{\det A}{\lambda}\right)^2+1$ |
| 5 | 填空题 | $\dfrac{1}{4}$ |
| 6 | 选择题 | A |
| 7 | 选择题 | B |
| 8 | 选择题 | D |
| 9 | 选择题 | A |
| 10 | 选择题 | C |
| 11 | 解答题 | $l_0:\begin{cases}x-y+2z-1=0,\\ x-3y-2z+1=0,\end{cases}$；旋转曲面为 $4x^2-17y^2+4z^2+2y-1=0$ |
| 12 | 解答题 | $\lambda=-1,\quad u(x,y)=-\arctan\dfrac{y}{x^2}+C$ |
| 13 | 解答题 | $\displaystyle y=-\frac{m}{k}v-\frac{m(mg-B\rho)}{k^2}\ln\frac{mg-B\rho-kv}{mg-B\rho}$ |
| 14 | 解答题 | $-\dfrac{\pi}{2}a^3$ |
| 15 | 解答题 | $\dfrac{2}{\pi}$ |
| 16 | 解答题 | 收敛 |
| 17 | 解答题 | 见解析；存在性成立，且在附加条件下 $x_0$ 唯一 |
| 18 | 解答题 | $a=3,\ b=1$；$P=\begin{pmatrix}\frac{1}{\sqrt2}&\frac{1}{\sqrt3}&\frac{1}{\sqrt6}\\0&-\frac{1}{\sqrt3}&\frac{2}{\sqrt6}\\-\frac{1}{\sqrt2}&\frac{1}{\sqrt3}&\frac{1}{\sqrt6}\end{pmatrix}$ |
| 19 | 解答题 | 见解析 |
| 20 | 解答题 | $\displaystyle \boldsymbol y=k_1\boldsymbol\xi_1+\cdots+k_n\boldsymbol\xi_n$，其中 $\boldsymbol\xi_i=(a_{i1},a_{i2},\ldots,a_{i,2n})^T$ |
| 21 | 解答题 | $1-\dfrac{2}{\pi}$ |
| 22 | 解答题 | $n$ 至少取 $35$ |
| 23 | 解答题 | 不拒绝 $H_0$；在显著性水平 $0.05$ 下，可以认为总体平均成绩为 $70$ 分 |

## 详细解析

### 第 1 题
- 答案：$-\dfrac{1}{4}$

用泰勒展开
$$
\sqrt{1+x}=1+\frac{1}{2}x-\frac{1}{8}x^2+o(x^2),
$$
$$
\sqrt{1-x}=1-\frac{1}{2}x-\frac{1}{8}x^2+o(x^2).
$$

相加后一次项抵消：
$$
\sqrt{1+x}+\sqrt{1-x}-2
=-\frac{1}{4}x^2+o(x^2).
$$

因此
$$
\lim_{x\to0}
\frac{\sqrt{1+x}+\sqrt{1-x}-2}{x^2}
=-\frac{1}{4}.
$$

### 第 2 题
- 答案：$y f''(xy)+\varphi'(x+y)+y\varphi''(x+y)$

先对 $y$ 求偏导：
$$
z_y=\frac{1}{x} f'(xy)\cdot x+\varphi(x+y)+y\varphi'(x+y)
=f'(xy)+\varphi(x+y)+y\varphi'(x+y).
$$

再对 $x$ 求偏导：
$$
z_{xy}
=y f''(xy)+\varphi'(x+y)+y\varphi''(x+y).
$$

由于 $f,\varphi$ 有二阶连续导数，混合偏导存在且顺序可交换。

### 第 3 题
- 答案：$12a$

椭圆 $l$ 关于两坐标轴均对称，$ds$ 在对称变换下不变，而 $2xy$ 关于 $x$、$y$ 都是奇对称项，所以
$$
\oint_l 2xy\,ds=0.
$$

在椭圆
$$
\frac{x^2}{4}+\frac{y^2}{3}=1
$$
上有
$$
3x^2+4y^2=12.
$$

故
$$
\oint_l(2xy+3x^2+4y^2)\,ds
=\oint_l12\,ds
=12a.
$$

### 第 4 题
- 答案：$\left(\dfrac{\det A}{\lambda}\right)^2+1$

设 $\boldsymbol{\xi}$ 是 $A$ 属于特征值 $\lambda$ 的非零特征向量，则
$$
A\boldsymbol{\xi}=\lambda\boldsymbol{\xi}.
$$

由于 $\det A\ne0$，故 $\lambda\ne0$，且
$$
A^*A=(\det A)E.
$$

两边左乘 $A^*$：
$$
A^*A\boldsymbol{\xi}=(\det A)\boldsymbol{\xi}
=\lambda A^*\boldsymbol{\xi}.
$$

于是
$$
A^*\boldsymbol{\xi}=\frac{\det A}{\lambda}\boldsymbol{\xi}.
$$

再作用一次 $A^*$：
$$
(A^*)^2\boldsymbol{\xi}
=\left(\frac{\det A}{\lambda}\right)^2\boldsymbol{\xi}.
$$

因此
$$
\bigl((A^*)^2+E\bigr)\boldsymbol{\xi}
=\left[\left(\frac{\det A}{\lambda}\right)^2+1\right]\boldsymbol{\xi},
$$
所以所给矩阵必有特征值
$$
\left(\frac{\det A}{\lambda}\right)^2+1.
$$

### 第 5 题
- 答案：$\dfrac{1}{4}$

区域
$$
D=\{(x,y)\mid 1\le x\le e^2,\ 0\le y\le 1/x\}
$$
的面积为
$$
S_D=\int_1^{e^2}\frac{1}{x}\,dx=2.
$$

均匀分布下联合密度为
$$
f(x,y)=\frac{1}{S_D}=\frac{1}{2},\qquad (x,y)\in D.
$$

当 $1\le x\le e^2$ 时，
$$
f_X(x)=\int_0^{1/x}\frac{1}{2}\,dy=\frac{1}{2x}.
$$

故
$$
f_X(2)=\frac{1}{4}.
$$

### 第 6 题
- 答案：A

令
$$
u=x^2-t^2,\qquad du=-2t\,dt.
$$

当 $t=0$ 时 $u=x^2$，当 $t=x$ 时 $u=0$，因此
$$
\int_0^x t f(x^2-t^2)\,dt
=\frac{1}{2}\int_0^{x^2}f(u)\,du.
$$

求导得
$$
\frac{d}{dx}\int_0^x t f(x^2-t^2)\,dt
=\frac{1}{2} f(x^2)\cdot2x
=xf(x^2).
$$

选 A。

### 第 7 题
- 答案：B

绝对值项
$$
|x^3-x|=|x(x-1)(x+1)|
$$
可能在 $x=-1,0,1$ 处造成不可导。

又
$$
x^2-x-2=(x-2)(x+1).
$$

在 $x=-1$ 处，外面的因子也有零点，使尖点被抵消，左右导数相等，因此可导。

在 $x=0$ 处，$x^2-x-2=-2\ne0$，绝对值的尖点不能抵消，不可导。

在 $x=1$ 处，$x^2-x-2=-2\ne0$，同样不可导。

所以不可导点共有 $2$ 个，选 B。

### 第 8 题
- 答案：D

由增量式
$$
\Delta y=\frac{y\,\Delta x}{1+x^2}+\alpha,
$$
且 $\alpha$ 是 $\Delta x$ 的高阶无穷小，得
$$
\frac{dy}{dx}=\frac{y}{1+x^2}.
$$

分离变量：
$$
\frac{dy}{y}=\frac{dx}{1+x^2}.
$$

积分得
$$
\ln|y|=\arctan x+C,
$$
即
$$
y=Ce^{\arctan x}.
$$

由 $y(0)=\pi$ 得 $C=\pi$。因此
$$
y(1)=\pi e^{\arctan1}
=\pi e^{\pi/4}.
$$

选 D。

### 第 9 题
- 答案：A

两条直线的方向向量分别为
$$
\boldsymbol v_1=(a_1-a_2,b_1-b_2,c_1-c_2),
$$
$$
\boldsymbol v_2=(a_2-a_3,b_2-b_3,c_2-c_3).
$$

题设矩阵
$$
\begin{pmatrix}
a_1&b_1&c_1\\
a_2&b_2&c_2\\
a_3&b_3&c_3
\end{pmatrix}
$$
满秩，经过行初等变换可知 $\boldsymbol v_1,\boldsymbol v_2$ 线性无关，所以两直线不平行。

由第一条直线参数式可得其过点
$$
(a_3,b_3,c_3)+\boldsymbol v_1
=(a_1-a_2+a_3,\ b_1-b_2+b_3,\ c_1-c_2+c_3).
$$

由第二条直线参数式取相应参数，也可得到同一点，因此两直线相交于一点。

选 A。

### 第 10 题
- 答案：C

由
$$
P(B\mid A)=P(B\mid\overline A)
$$
得
$$
\frac{P(AB)}{P(A)}
=
\frac{P(\overline A B)}{P(\overline A)}
=
\frac{P(B)-P(AB)}{1-P(A)}.
$$

整理：
$$
P(AB)[1-P(A)]
=P(A)[P(B)-P(AB)].
$$

于是
$$
P(AB)=P(A)P(B).
$$

即事件 $A$ 与 $B$ 独立，选 C。

### 第 11 题
- 答案：$l_0:\begin{cases}x-y+2z-1=0,\\ x-3y-2z+1=0,\end{cases}$；旋转曲面为 $4x^2-17y^2+4z^2+2y-1=0$

直线 $l$ 可写为
$$
x=1+t,\qquad y=t,\qquad z=1-t.
$$

代入平面 $\pi:x-y+2z-1=0$，得
$$
(1+t)-t+2(1-t)-1=0,
$$
故 $t=1$，交点为
$$
N_1(2,1,0).
$$

过 $l$ 上点 $M_0(1,0,1)$ 作平面 $\pi$ 的垂线，其方向为平面法向量 $(1,-1,2)$：
$$
x=1+s,\quad y=-s,\quad z=1+2s.
$$

代入平面得 $s=-1/3$，交点为
$$
N_2\left(\frac{2}{3},\frac{1}{3},\frac{1}{3}\right).
$$

因此投影线 $l_0$ 过 $N_1,N_2$，可写为
$$
\frac{x-2}{4}=\frac{y-1}{2}=\frac{z}{-1},
$$
等价于
$$
l_0:\begin{cases}
x-y+2z-1=0,\\
x-3y-2z+1=0.
\end{cases}
$$

由 $l_0$ 可得
$$
x=2y,\qquad z=-\frac{1}{2}(y-1).
$$

绕 $y$ 轴旋转时，半径满足
$$
x^2+z^2=(2y)^2+\left[-\frac{1}{2}(y-1)\right]^2.
$$

整理得旋转曲面方程
$$
4x^2-17y^2+4z^2+2y-1=0.
$$

### 第 12 题
- 答案：$\lambda=-1,\quad u(x,y)=-\arctan\dfrac{y}{x^2}+C$

设
$$
P=2xy(x^4+y^2)^\lambda,\qquad
Q=-x^2(x^4+y^2)^\lambda.
$$

在右半平面 $x>0$ 上，向量场为某函数的梯度等价于
$$
\frac{\partial P}{\partial y}=\frac{\partial Q}{\partial x}.
$$

计算可得
$$
\frac{\partial Q}{\partial x}
=-2x(x^4+y^2)^\lambda
-4\lambda x^5(x^4+y^2)^{\lambda-1},
$$
$$
\frac{\partial P}{\partial y}
=2x(x^4+y^2)^\lambda
+4\lambda xy^2(x^4+y^2)^{\lambda-1}.
$$

令二者相等，整理得
$$
4x(x^4+y^2)^\lambda(\lambda+1)=0.
$$

因 $x>0$，故
$$
\lambda=-1.
$$

于是
$$
du=\frac{2xy}{x^4+y^2}\,dx-\frac{x^2}{x^4+y^2}\,dy.
$$

取从 $(1,0)$ 到 $(x,y)$ 的折线路径，先沿 $x$ 轴再沿竖线，得
$$
u(x,y)=\int_0^y\frac{-x^2}{x^4+s^2}\,ds+C.
$$

积分得
$$
u(x,y)=-\arctan\frac{y}{x^2}+C.
$$

### 第 13 题
- 答案：$\displaystyle y=-\frac{m}{k}v-\frac{m(mg-B\rho)}{k^2}\ln\frac{mg-B\rho-kv}{mg-B\rho}$

取铅直向下为正方向。仪器受重力 $mg$、浮力 $B\rho$ 和阻力 $kv$，其中阻力方向向上，所以
$$
m\frac{d^2y}{dt^2}=mg-B\rho-kv,
\qquad y(0)=0,\quad v(0)=0.
$$

又
$$
v=\frac{dy}{dt},\qquad
\frac{d^2y}{dt^2}=\frac{dv}{dt}
=\frac{dv}{dy}\frac{dy}{dt}
=v\frac{dv}{dy}.
$$

代入得
$$
mv\frac{dv}{dy}=mg-B\rho-kv.
$$

故
$$
dy=\frac{mv}{mg-B\rho-kv}\,dv.
$$

两边从 $0$ 到 $v$ 积分：
$$
y=\int_0^v\frac{ms}{mg-B\rho-ks}\,ds.
$$

计算得
$$
y=-\frac{m}{k}v-\frac{m(mg-B\rho)}{k^2}
\ln\frac{mg-B\rho-kv}{mg-B\rho}.
$$

### 第 14 题
- 答案：$-\dfrac{\pi}{2}a^3$

在半球面
$$
x^2+y^2+z^2=a^2
$$
上有
$$
\sqrt{x^2+y^2+z^2}=a.
$$

下半球面写为
$$
z=-\sqrt{a^2-x^2-y^2},
$$
其上侧对应图形曲面的上侧取向。设投影区域
$$
D:x^2+y^2\le a^2.
$$

对上侧图形曲面有
$$
dy\,dz=-z_x\,dx\,dy,
\qquad dx\,dy=dx\,dy.
$$

于是积分化为
$$
I=\iint_D\left[-x z_x+\frac{(z+a)^2}{a}\right]dx\,dy.
$$

其中
$$
z_x=\frac{x}{\sqrt{a^2-x^2-y^2}},
\qquad
z+a=a-\sqrt{a^2-x^2-y^2}.
$$

转为极坐标后，
$$
I=-\int_0^{2\pi}\int_0^a
\frac{r^2\cos^2\theta}{\sqrt{a^2-r^2}}\,r\,dr\,d\theta
\frac{1}{a}\int_0^{2\pi}\int_0^a
\left(a-\sqrt{a^2-r^2}\right)^2r\,dr\,d\theta.
$$

分别计算得第一部分为 $-\dfrac{2}{3}\pi a^3$，第二部分为 $\dfrac{1}{6}\pi a^3$。
因此
$$
I=-\frac{2}{3}\pi a^3+\frac{1}{6}\pi a^3
=-\frac{\pi}{2}a^3.
$$

### 第 15 题
- 答案：$\dfrac{2}{\pi}$

记第 $i$ 项的分子为
$$
\sin\frac{i\pi}{n},\qquad i=1,2,\ldots,n.
$$

因为 $0\le \sin\dfrac{i\pi}{n}$，且
$$
n< n+\frac{1}{i}\le n+1,
$$
所以
$$
\sum_{i=1}^n\frac{\sin(i\pi/n)}{n+1}
\le
\sum_{i=1}^n\frac{\sin(i\pi/n)}{n+1/i}
\le
\sum_{i=1}^n\frac{\sin(i\pi/n)}{n}.
$$

左右两端的极限相同。右端为黎曼和：
$$
\lim_{n\to\infty}\frac{1}{n}\sum_{i=1}^n\sin\frac{i\pi}{n}
=\int_0^1\sin(\pi x)\,dx
=\frac{2}{\pi}.
$$

左端比右端只差因子 $n/(n+1)\to1$，故极限也为 $2/\pi$。
由夹逼定理，原极限为
$$
\frac{2}{\pi}.
$$

### 第 16 题
- 答案：收敛

正项数列 $\{a_n\}$ 单调减少且有下界 $0$，故极限存在，设
$$
\lim_{n\to\infty}a_n=a\ge0.
$$

若 $a=0$，则由交错级数判别法，
$$
\sum_{n=1}^\infty(-1)^n a_n
$$
应收敛，这与题设发散矛盾。因此
$$
a>0.
$$

因为 $a_n\ge a$，所以
$$
0<\frac{1}{a_n+1}\le\frac{1}{a+1}<1.
$$

于是
$$
0<\left(\frac{1}{a_n+1}\right)^n
\le
\left(\frac{1}{a+1}\right)^n.
$$

右端为收敛的等比级数，故由比较判别法，
$$
\sum_{n=1}^{\infty}\left(\frac{1}{a_n+1}\right)^n
$$
收敛。

### 第 17 题
- 答案：见解析；存在性成立，且在附加条件下 $x_0$ 唯一

题意中的面积等式可写为
$$
x_0 f(x_0)=\int_{x_0}^{1}f(x)\,dx.
$$

令
$$
\varphi(x)=xf(x)-\int_x^1 f(t)\,dt.
$$

为证明存在零点，取
$$
\Phi(x)=\int_0^x\varphi(t)\,dt.
$$
则
$$
\Phi(0)=0.
$$

又
$$
\Phi(1)=\int_0^1xf(x)\,dx-\int_0^1\int_x^1 f(t)\,dt\,dx.
$$

对第二项交换积分次序：
$$
\int_0^1\int_x^1 f(t)\,dt\,dx
=\int_0^1 t f(t)\,dt.
$$

故
$$
\Phi(1)=0.
$$

由 Rolle 定理，存在 $x_0\in(0,1)$，使
$$
\Phi'(x_0)=\varphi(x_0)=0.
$$
即
$$
x_0 f(x_0)=\int_{x_0}^{1}f(x)\,dx.
$$

再证唯一性。在附加条件下，
$$
\varphi'(x)=xf'(x)+f(x)+f(x)
=xf'(x)+2f(x)>0.
$$

因此 $\varphi(x)$ 在 $(0,1)$ 内严格单调递增，零点至多一个。结合已证存在性，$x_0$ 唯一。

### 第 18 题
- 答案：$a=3,\ b=1$；$P=\begin{pmatrix}\frac{1}{\sqrt2}&\frac{1}{\sqrt3}&\frac{1}{\sqrt6}\\0&-\frac{1}{\sqrt3}&\frac{2}{\sqrt6}\\-\frac{1}{\sqrt2}&\frac{1}{\sqrt3}&\frac{1}{\sqrt6}\end{pmatrix}$

二次型对应的实对称矩阵为
$$
A=\begin{pmatrix}
1&b&1\\
b&a&1\\
1&1&1
\end{pmatrix}.
$$

题设正交变换后标准形为
$$
\eta^2+4\zeta^2=4,
$$
因此 $A$ 的特征值为
$$
0,\ 1,\ 4.
$$

由迹相等，
$$
1+a+1=0+1+4,
$$
得
$$
a=3.
$$

又由行列式相等，
$$
\det A=0.
$$
此时可得
$$
\det A=-(b-1)^2,
$$
故
$$
b=1.
$$

于是
$$
A=\begin{pmatrix}
1&1&1\\
1&3&1\\
1&1&1
\end{pmatrix}.
$$

分别求属于特征值 $0,1,4$ 的单位特征向量：
$$
\boldsymbol\eta_1=\frac{1}{\sqrt2}(1,0,-1)^T,
$$
$$
\boldsymbol\eta_2=\frac{1}{\sqrt3}(1,-1,1)^T,
$$
$$
\boldsymbol\eta_3=\frac{1}{\sqrt6}(1,2,1)^T.
$$

把它们按标准形中 $0,1,4$ 的顺序作为列向量，得
$$
P=
\begin{pmatrix}
\frac{1}{\sqrt2}&\frac{1}{\sqrt3}&\frac{1}{\sqrt6}\\
0&-\frac{1}{\sqrt3}&\frac{2}{\sqrt6}\\
-\frac{1}{\sqrt2}&\frac{1}{\sqrt3}&\frac{1}{\sqrt6}
\end{pmatrix}.
$$

### 第 19 题
- 答案：见解析

设存在常数
$$
\lambda_0,\lambda_1,\ldots,\lambda_{k-1}
$$
使
$$
\lambda_0\boldsymbol{\alpha}
+\lambda_1A\boldsymbol{\alpha}
+\cdots+
\lambda_{k-1}A^{k-1}\boldsymbol{\alpha}
=0.
$$

两边左乘 $A^{k-1}$，得
$$
\lambda_0A^{k-1}\boldsymbol{\alpha}
+\lambda_1A^k\boldsymbol{\alpha}
+\cdots+
\lambda_{k-1}A^{2k-2}\boldsymbol{\alpha}
=0.
$$

由题设 $A^k\boldsymbol{\alpha}=0$，可知
$$
A^{k+1}\boldsymbol{\alpha}=\cdots=A^{2k-2}\boldsymbol{\alpha}=0.
$$

所以上式化为
$$
\lambda_0A^{k-1}\boldsymbol{\alpha}=0.
$$

又 $A^{k-1}\boldsymbol{\alpha}\ne0$，故
$$
\lambda_0=0.
$$

代回原式，再左乘 $A^{k-2}$，同理可得
$$
\lambda_1=0.
$$

依次进行，得到
$$
\lambda_0=\lambda_1=\cdots=\lambda_{k-1}=0.
$$

因此
$$
\boldsymbol{\alpha},A\boldsymbol{\alpha},\ldots,A^{k-1}\boldsymbol{\alpha}
$$
线性无关。

### 第 20 题
- 答案：$\displaystyle \boldsymbol y=k_1\boldsymbol\xi_1+\cdots+k_n\boldsymbol\xi_n$，其中 $\boldsymbol\xi_i=(a_{i1},a_{i2},\ldots,a_{i,2n})^T$

设方程组 (I) 的系数矩阵为
$$
A_{n\times 2n},
$$
方程组 (II) 的系数矩阵为
$$
B_{n\times 2n}.
$$

题设中 $B$ 的每一行转置后都是 $AX=0$ 的基础解系向量，因此
$$
AB^T=0.
$$

由于 (I) 的基础解系含 $n$ 个向量，
$$
n=2n-r(A),
$$
故
$$
r(A)=n.
$$
所以 $A$ 的 $n$ 个行向量线性无关。

由 $AB^T=0$ 取转置，得
$$
BA^T=0.
$$
这说明 $A^T$ 的列向量，也就是 $A$ 的行向量转置，都是方程组
$$
BY=0
$$
的解。

又 $B^T$ 的列向量是 (I) 的基础解系，故线性无关，从而
$$
r(B)=n.
$$
于是 $BY=0$ 的解空间维数为
$$
2n-r(B)=n.
$$

恰好等于 $A$ 的行向量个数，因此 $A$ 的行向量转置构成 (II) 的一组基础解系。通解为
$$
\boldsymbol y=k_1\boldsymbol\xi_1+\cdots+k_n\boldsymbol\xi_n,
$$
其中
$$
\boldsymbol\xi_i=(a_{i1},a_{i2},\ldots,a_{i,2n})^T,
\qquad i=1,2,\ldots,n.
$$

### 第 21 题
- 答案：$1-\dfrac{2}{\pi}$

令
$$
Z=X-Y.
$$

由于 $X,Y$ 相互独立且
$$
X,Y\sim N\left(0,\frac{1}{2}\right),
$$
所以
$$
Z\sim N(0,1).
$$

于是
$$
D(|X-Y|)=D(|Z|)
=E(Z^2)-[E(|Z|)]^2.
$$

因为 $Z\sim N(0,1)$，
$$
E(Z^2)=1,
$$
且
$$
E|Z|
=2\int_0^\infty z\frac{1}{\sqrt{2\pi}}e^{-z^2/2}\,dz
=\sqrt{\frac{2}{\pi}}.
$$

因此
$$
D(|X-Y|)
=1-\left(\sqrt{\frac{2}{\pi}}\right)^2
=1-\frac{2}{\pi}.
$$

### 第 22 题
- 答案：$n$ 至少取 $35$

样本均值满足
$$
\overline X\sim N\left(3.4,\frac{6^2}{n}\right).
$$

要求
$$
P(1.4<\overline X<5.4)\ge0.95.
$$

等价于
$$
P(|\overline X-3.4|<2)\ge0.95.
$$

标准化：
$$
\frac{\overline X-3.4}{6/\sqrt n}\sim N(0,1),
$$
故
$$
P(|\overline X-3.4|<2)
=2\Phi\left(\frac{2\sqrt n}{6}\right)-1
=2\Phi\left(\frac{\sqrt n}{3}\right)-1.
$$

令其不小于 $0.95$，得
$$
\Phi\left(\frac{\sqrt n}{3}\right)\ge0.975.
$$

查表得
$$
\frac{\sqrt n}{3}\ge1.96.
$$

于是
$$
n\ge(1.96\cdot3)^2=34.5744.
$$

所以样本容量至少应取
$$
n=35.
$$

### 第 23 题
- 答案：不拒绝 $H_0$；在显著性水平 $0.05$ 下，可以认为总体平均成绩为 $70$ 分

设总体均值为 $\mu$。检验假设为
$$
H_0:\mu=70,\qquad H_1:\mu\ne70.
$$

总体方差未知，样本容量为 $36$，使用 $t$ 检验。统计量为
$$
T=\frac{\overline X-\mu_0}{S/\sqrt n}.
$$

在 $H_0$ 成立时，
$$
T\sim t(35).
$$

显著性水平为 $0.05$ 的双侧检验拒绝域为
$$
|T|\ge t_{0.975}(35).
$$

由附表
$$
t_{0.975}(35)=2.0301.
$$

代入
$$
\overline X=66.5,\qquad S=15,\qquad n=36,
$$
得
$$
|T|=\left|\frac{66.5-70}{15/\sqrt{36}}\right|
=1.4.
$$

因为
$$
1.4<2.0301,
$$
所以不拒绝原假设 $H_0$。在显著性水平 $0.05$ 下，可以认为这次考试总体考生的平均成绩为 $70$ 分。
