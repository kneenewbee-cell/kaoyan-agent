# Math 1 1990 Answers

资料类型：考研数学一答案解析
年份：1990
科目：数学一
范围：试卷 I
来源：D:\百度网盘\高数资料\【02】1987-2022年数学一真题详解答案（PDF）\1990考研数一真题解析.pdf
校对状态：已按题干、原卷页和答案页图像重新清洗，去除 OCR 碎行、串题内容和非本题知识点页脚

## 答案速查

| 题号 | 题型 | 答案 |
|---|---|---|
| 1 | 填空题 | $x-3y-z+4=0$ |
| 2 | 填空题 | $e^{2a}$ |
| 3 | 填空题 | $1$ |
| 4 | 填空题 | $\dfrac{1}{2}(1-e^{-4})$ |
| 5 | 填空题 | $2$ |
| 6 | 选择题 | A |
| 7 | 选择题 | A |
| 8 | 选择题 | C |
| 9 | 选择题 | D |
| 10 | 选择题 | B |
| 11 | 解答题 | $\dfrac{1}{3}\ln 2$ |
| 12 | 解答题 | $-2f_{11}+(2\sin x-y\cos x)f_{12}+y\sin x\cos x\,f_{22}+\cos x\,f_2$ |
| 13 | 解答题 | $y=(C_1+C_2x)e^{-2x}+\dfrac{1}{2}x^2e^{-2x}$ |
| 14 | 解答题 | 收敛域为 $(-1,1)$，和函数为 $S(x)=\dfrac{1+x}{(1-x)^2}$ |
| 15 | 解答题 | $12\pi$ |
| 16 | 解答题 | 见解析 |
| 17 | 解答题 | $A=\begin{pmatrix}1&0&0&0\\-2&1&0&0\\1&-2&1&0\\0&1&-2&1\end{pmatrix}$ |
| 18 | 解答题 | 取 $x=Py$，其中 $P=\begin{pmatrix}\dfrac{2}{\sqrt5}&-\dfrac{2}{3\sqrt5}&\dfrac{1}{3}\\[2pt]\dfrac{1}{\sqrt5}&\dfrac{4}{3\sqrt5}&-\dfrac{2}{3}\\[2pt]0&\dfrac{5}{3\sqrt5}&\dfrac{2}{3}\end{pmatrix}$，则 $f=9y_3^2$ |
| 19 | 解答题 | $2(\pi-1)$ |
| 20 | 填空题 | $F(x)=\begin{cases}\dfrac{1}{2}e^x,&x<0,\\[2pt]1-\dfrac{1}{2}e^{-x},&x\ge0,\end{cases}$ |
| 21 | 填空题 | $0.3$ |
| 22 | 填空题 | $4$ |
| 23 | 解答题 | $f_X(x)=\begin{cases}2x,&0<x<1,\\0,&\text{其他},\end{cases}\quad D(Z)=\dfrac{2}{9}$ |

## 详细解析

### 第 1 题

- 答案：$x-3y-z+4=0$

直线的方向向量为

$$
\boldsymbol{l}=(-1,3,1).
$$

所求平面与该直线垂直，所以平面的法向量可取

$$
\boldsymbol{n}=(-1,3,1).
$$

又平面过点 $M(1,2,-1)$，因此平面方程为

$$
-(x-1)+3(y-2)+(z+1)=0.
$$

整理得

$$
x-3y-z+4=0.
$$

### 第 2 题

- 答案：$e^{2a}$

将底数改写为

$$
\frac{x+a}{x-a}=1+\frac{2a}{x-a}.
$$

于是

$$
\left(\frac{x+a}{x-a}\right)^x
=\left(1+\frac{2a}{x-a}\right)^x.
$$

取对数：

$$
x\ln\left(1+\frac{2a}{x-a}\right).
$$

当 $x\to\infty$ 时，

$$
x\ln\left(1+\frac{2a}{x-a}\right)
\sim x\cdot \frac{2a}{x-a}\to 2a.
$$

所以原极限为

$$
e^{2a}.
$$

### 第 3 题

- 答案：$1$

由题设

$$
f(x)=
\begin{cases}
1,&|x|\le 1,\\
0,&|x|>1.
\end{cases}
$$

当 $|x|\le 1$ 时，$f(x)=1$，故

$$
f[f(x)]=f(1)=1.
$$

当 $|x|>1$ 时，$f(x)=0$，故

$$
f[f(x)]=f(0)=1.
$$

两种情况都得到

$$
f[f(x)]=1.
$$

### 第 4 题

- 答案：$\dfrac{1}{2}(1-e^{-4})$

积分区域为

$$
D=\{(x,y)\mid 0\le x\le 2,\ x\le y\le 2\}.
$$

交换积分次序后，区域可写为

$$
0\le y\le 2,\quad 0\le x\le y.
$$

因此

$$
\int_0^2 dx\int_x^2 e^{-y^2}\,dy
=\int_0^2 dy\int_0^y e^{-y^2}\,dx
=\int_0^2 y e^{-y^2}\,dy.
$$

令 $u=-y^2$，则 $du=-2y\,dy$，所以

$$
\int_0^2 y e^{-y^2}\,dy
=-\frac{1}{2} e^{-y^2}\Big|_0^2
=\frac{1}{2}(1-e^{-4}).
$$

### 第 5 题

- 答案：$2$

把四个向量作为矩阵的行：

$$
A=
\begin{pmatrix}
1&2&3&4\\
2&3&4&5\\
3&4&5&6\\
4&5&6&7
\end{pmatrix}.
$$

作初等行变换：

$$
\begin{pmatrix}
1&2&3&4\\
2&3&4&5\\
3&4&5&6\\
4&5&6&7
\end{pmatrix}
\longrightarrow
\begin{pmatrix}
1&2&3&4\\
0&-1&-2&-3\\
0&-2&-4&-6\\
0&-3&-6&-9
\end{pmatrix}
\longrightarrow
\begin{pmatrix}
1&2&3&4\\
0&1&2&3\\
0&0&0&0\\
0&0&0&0
\end{pmatrix}.
$$

阶梯形矩阵中有两个非零行，故向量组的秩为

$$
r=2.
$$

### 第 6 题

- 答案：A

由变限积分求导公式，

$$
\frac{d}{dx}\int_{\alpha(x)}^{\beta(x)} f(t)\,dt
=f(\beta(x))\beta'(x)-f(\alpha(x))\alpha'(x).
$$

本题中

$$
\alpha(x)=x,\qquad \beta(x)=e^{-x}.
$$

因此

$$
F'(x)=f(e^{-x})(-e^{-x})-f(x)\cdot 1
=-e^{-x}f(e^{-x})-f(x).
$$

故选 A。

### 第 7 题

- 答案：A

记 $y=f(x)$。由题设

$$
y'=y^2.
$$

逐次求导：

$$
y''=2yy'=2y^3,\qquad
y'''=6y^2y'=3!y^4.
$$

由此猜想

$$
y^{(n)}=n!y^{n+1}.
$$

用数学归纳法验证：若 $y^{(k)}=k!y^{k+1}$，则

$$
y^{(k+1)}
=\frac{d}{dx}\left(k!y^{k+1}\right)
=k!(k+1)y^k y'
=(k+1)!y^{k+2}.
$$

所以

$$
f^{(n)}(x)=n![f(x)]^{n+1}.
$$

故选 A。

### 第 8 题

- 答案：C

将级数分成两部分：

$$
\sum_{n=1}^{\infty}\frac{\sin n\alpha}{n^2}
-\sum_{n=1}^{\infty}\frac{1}{\sqrt n}.
$$

由于

$$
\left|\frac{\sin n\alpha}{n^2}\right|\le \frac{1}{n^2},
$$

所以

$$
\sum_{n=1}^{\infty}\frac{\sin n\alpha}{n^2}
$$

绝对收敛。

而

$$
\sum_{n=1}^{\infty}\frac{1}{\sqrt n}
$$

是 $p=\dfrac{1}{2}$ 的 $p$ 级数，发散。收敛级数与发散级数之差仍发散，因此原级数发散。

故选 C。

### 第 9 题

- 答案：D

由

$$
\lim_{x\to 0}\frac{f(x)}{1-\cos x}=2>0
$$

可知，当 $x$ 充分接近 $0$ 且 $x\ne 0$ 时，

$$
\frac{f(x)}{1-\cos x}>0.
$$

又 $1-\cos x>0$，所以

$$
f(x)>0=f(0)
$$

在 $0$ 的去心邻域内成立。因此 $f(x)$ 在 $x=0$ 处取得极小值。

故选 D。

### 第 10 题

- 答案：B

非齐次方程组 $Ax=b$ 的通解等于对应齐次方程组的通解加上一个非齐次方程组的特解。

因为 $\beta_1,\beta_2$ 都是 $Ax=b$ 的解，所以

$$
A\left(\frac{\beta_1+\beta_2}{2}\right)
=\frac{1}{2}(A\beta_1+A\beta_2)
=b,
$$

即 $\dfrac{\beta_1+\beta_2}{2}$ 是一个特解。

又 $\alpha_1,\alpha_2$ 是齐次方程组的基础解系，故 $\alpha_1$ 与 $\alpha_1-\alpha_2$ 也是齐次方程组的一组基础解系。

因此通解可写为

$$
k_1\alpha_1+k_2(\alpha_1-\alpha_2)+\frac{\beta_1+\beta_2}{2}.
$$

故选 B。

### 第 11 题

- 答案：$\dfrac{1}{3}\ln 2$

注意

$$
\frac{1}{(2-x)^2}\,dx=d\left(\frac{1}{2-x}\right).
$$

因此用分部积分：

$$
\begin{aligned}
\int_0^1\frac{\ln(1+x)}{(2-x)^2}\,dx
&=\int_0^1\ln(1+x)\,d\left(\frac{1}{2-x}\right)\\
&=\left.\frac{\ln(1+x)}{2-x}\right|_0^1
-\int_0^1\frac{1}{(2-x)(1+x)}\,dx.
\end{aligned}
$$

又

$$
\frac{1}{(2-x)(1+x)}
=\frac{1}{3}\left(\frac{1}{2-x}+\frac{1}{1+x}\right).
$$

所以

$$
\begin{aligned}
\int_0^1\frac{\ln(1+x)}{(2-x)^2}\,dx
&=\ln 2-\frac{1}{3}\int_0^1
\left(\frac{1}{2-x}+\frac{1}{1+x}\right)\,dx\\
&=\ln2-\frac{1}{3}\left[-\ln(2-x)+\ln(1+x)\right]_0^1\\
&=\ln2-\frac{2}{3}\ln2\\
&=\frac{1}{3}\ln2.
\end{aligned}
$$

### 第 12 题

- 答案：$-2f_{11}+(2\sin x-y\cos x)f_{12}+y\sin x\cos x\,f_{22}+\cos x\,f_2$

以下各偏导数均在

$$
(u,v)=(2x-y,\ y\sin x)
$$

处取值。先对 $y$ 求偏导：

$$
\frac{\partial z}{\partial y}
=-f_1+\sin x\,f_2.
$$

再对 $x$ 求偏导。由链式法则，

$$
\frac{\partial f_1}{\partial x}
=2f_{11}+y\cos x\,f_{12},
$$

且

$$
\frac{\partial f_2}{\partial x}
=2f_{12}+y\cos x\,f_{22}.
$$

因此

$$
\begin{aligned}
\frac{\partial^2z}{\partial x\partial y}
&=-\left(2f_{11}+y\cos x\,f_{12}\right)
+\cos x\,f_2
+\sin x\left(2f_{12}+y\cos x\,f_{22}\right)\\
&=-2f_{11}+(2\sin x-y\cos x)f_{12}
+y\sin x\cos x\,f_{22}+\cos x\,f_2.
\end{aligned}
$$

### 第 13 题

- 答案：$y=(C_1+C_2x)e^{-2x}+\dfrac{1}{2}x^2e^{-2x}$

对应齐次方程为

$$
y''+4y'+4y=0.
$$

其特征方程为

$$
r^2+4r+4=(r+2)^2=0,
$$

故齐次通解为

$$
y_h=(C_1+C_2x)e^{-2x}.
$$

由于非齐次项为 $e^{-2x}$，且 $-2$ 是二重特征根，取特解

$$
y_p=ax^2e^{-2x}.
$$

代入方程得 $a=\dfrac{1}{2}$。所以通解为

$$
y=(C_1+C_2x)e^{-2x}+\frac{1}{2}x^2e^{-2x}.
$$

### 第 14 题

- 答案：收敛域为 $(-1,1)$，和函数为 $S(x)=\dfrac{1+x}{(1-x)^2}$

设

$$
S(x)=\sum_{n=0}^{\infty}(2n+1)x^n.
$$

由比值法，

$$
\lim_{n\to\infty}
\left|\frac{(2n+3)x^{n+1}}{(2n+1)x^n}\right|
=|x|.
$$

故当 $|x|<1$ 时收敛，当 $|x|>1$ 时发散。

端点处：

$$
x=1:\ \sum_{n=0}^{\infty}(2n+1)
$$

发散；

$$
x=-1:\ \sum_{n=0}^{\infty}(2n+1)(-1)^n
$$

通项不趋于 $0$，也发散。所以收敛域为 $(-1,1)$。

当 $|x|<1$ 时，

$$
\sum_{n=0}^{\infty}x^n=\frac{1}{1-x},
$$

且

$$
\sum_{n=0}^{\infty}n x^n
=x\left(\sum_{n=0}^{\infty}x^n\right)'
=\frac{x}{(1-x)^2}.
$$

于是

$$
S(x)=2\sum_{n=0}^{\infty}n x^n+\sum_{n=0}^{\infty}x^n
=\frac{2x}{(1-x)^2}+\frac{1}{1-x}
=\frac{1+x}{(1-x)^2}.
$$

### 第 15 题

- 答案：$12\pi$

原卷中曲面积分为

$$
I=\iint_{\Sigma} yz\,dz\,dx+2\,dx\,dy.
$$

按第二型曲面积分记号，取

$$
P=0,\qquad Q=yz,\qquad R=2.
$$

则

$$
\frac{\partial P}{\partial x}
+\frac{\partial Q}{\partial y}
+\frac{\partial R}{\partial z}
=z.
$$

用圆盘

$$
\Sigma_1:\ z=0,\quad x^2+y^2\le 4
$$

补成上半球体的闭曲面。闭曲面取外侧方向时，$\Sigma_1$ 的法向量向下，所以

$$
\iint_{\Sigma_1} yz\,dz\,dx+2\,dx\,dy
=-\iint_{x^2+y^2\le 4}2\,dx\,dy
=-8\pi.
$$

由高斯公式，

$$
I+\left(-8\pi\right)
=\iiint_{\Omega}z\,dV.
$$

上半球体 $\Omega$ 中，按先 $z$ 后 $x,y$ 积分：

$$
\iiint_{\Omega}z\,dV
=\int_0^2 z\cdot \pi(4-z^2)\,dz
=4\pi.
$$

因此

$$
I=4\pi+8\pi=12\pi.
$$

### 第 16 题

- 答案：见解析

因为 $f(x)$ 不恒为常数，且 $f(a)=f(b)$，所以存在 $x_0\in(a,b)$，使

$$
f(x_0)\ne f(a).
$$

若

$$
f(x_0)>f(a),
$$

则在区间 $[a,x_0]$ 上应用拉格朗日中值定理，存在 $\xi\in(a,x_0)$，使

$$
f'(\xi)=\frac{f(x_0)-f(a)}{x_0-a}>0.
$$

若

$$
f(x_0)<f(a)=f(b),
$$

则在区间 $[x_0,b]$ 上应用拉格朗日中值定理，存在 $\xi\in(x_0,b)$，使

$$
f'(\xi)=\frac{f(b)-f(x_0)}{b-x_0}>0.
$$

两种情况都能在 $(a,b)$ 内找到一点 $\xi$，使 $f'(\xi)>0$。

### 第 17 题

- 答案：$A=\begin{pmatrix}1&0&0&0\\-2&1&0&0\\1&-2&1&0\\0&1&-2&1\end{pmatrix}$

由矩阵转置与逆矩阵性质，

$$
(E-C^{-1}B)^TC^T
=\left[C(E-C^{-1}B)\right]^T
=(C-B)^T.
$$

原式

$$
A(E-C^{-1}B)^TC^T=E
$$

化为

$$
A(C-B)^T=E.
$$

因此

$$
A=\left[(C-B)^T\right]^{-1}
=\left[(C-B)^{-1}\right]^T.
$$

计算

$$
C-B=
\begin{pmatrix}
1&2&3&4\\
0&1&2&3\\
0&0&1&2\\
0&0&0&1
\end{pmatrix}.
$$

其逆矩阵为

$$
(C-B)^{-1}=
\begin{pmatrix}
1&-2&1&0\\
0&1&-2&1\\
0&0&1&-2\\
0&0&0&1
\end{pmatrix}.
$$

所以

$$
A=\left[(C-B)^{-1}\right]^T
=
\begin{pmatrix}
1&0&0&0\\
-2&1&0&0\\
1&-2&1&0\\
0&1&-2&1
\end{pmatrix}.
$$

### 第 18 题

- 答案：取 $x=Py$，其中 $P=\begin{pmatrix}\dfrac{2}{\sqrt5}&-\dfrac{2}{3\sqrt5}&\dfrac{1}{3}\\[2pt]\dfrac{1}{\sqrt5}&\dfrac{4}{3\sqrt5}&-\dfrac{2}{3}\\[2pt]0&\dfrac{5}{3\sqrt5}&\dfrac{2}{3}\end{pmatrix}$，则 $f=9y_3^2$

二次型对应的对称矩阵为

$$
A=
\begin{pmatrix}
1&-2&2\\
-2&4&-4\\
2&-4&4
\end{pmatrix}.
$$

注意到

$$
A=
\begin{pmatrix}1\\-2\\2\end{pmatrix}
\begin{pmatrix}1&-2&2\end{pmatrix}.
$$

因此 $A$ 的非零特征值为

$$
1^2+(-2)^2+2^2=9,
$$

其余两个特征值为 $0$。属于特征值 $9$ 的单位特征向量可取

$$
\boldsymbol{p}_3=\frac{1}{3}(1,-2,2)^T.
$$

在与 $(1,-2,2)^T$ 正交的平面内，取两个正交单位向量

$$
\boldsymbol{p}_1=\left(\frac{2}{\sqrt5},\frac{1}{\sqrt5},0\right)^T,
\qquad
\boldsymbol{p}_2=\left(-\frac{2}{3\sqrt5},\frac{4}{3\sqrt5},\frac{5}{3\sqrt5}\right)^T.
$$

令

$$
P=(\boldsymbol{p}_1,\boldsymbol{p}_2,\boldsymbol{p}_3)
=
\begin{pmatrix}
\dfrac{2}{\sqrt5}&-\dfrac{2}{3\sqrt5}&\dfrac{1}{3}\\[2pt]
\dfrac{1}{\sqrt5}&\dfrac{4}{3\sqrt5}&-\dfrac{2}{3}\\[2pt]
0&\dfrac{5}{3\sqrt5}&\dfrac{2}{3}
\end{pmatrix}.
$$

则 $P$ 为正交矩阵，且

$$
P^TAP=\operatorname{diag}(0,0,9).
$$

作正交变换 $x=Py$，二次型化为标准形

$$
f=9y_3^2.
$$

由于零特征值对应的特征子空间是二维的，前两个正交单位向量的选取不唯一；上式给出其中一种正交变换。

### 第 19 题

- 答案：$2(\pi-1)$

设质点坐标为 $P(x,y)$。力的大小为

$$
|\boldsymbol F|=\sqrt{x^2+y^2}.
$$

与 $\overrightarrow{OP}=(x,y)$ 垂直且与 $y$ 轴正向夹角小于 $\dfrac{\pi}{2}$ 的方向可取 $(-y,x)$，其长度也为 $\sqrt{x^2+y^2}$。因此

$$
\boldsymbol F=(-y,x).
$$

所作功为

$$
W=\int_{\widehat{AB}} -y\,dx+x\,dy.
$$

用线段 $\overline{BA}$ 补成正向闭曲线。直线 $AB$ 的方程为 $y=x+1$。沿 $\overline{BA}$，$x$ 从 $3$ 到 $1$，故

$$
\int_{\overline{BA}} -y\,dx+x\,dy
=\int_3^1[-(x+1)+x]\,dx=2.
$$

闭曲线围成的区域是半径 $\sqrt2$ 的半圆，面积为

$$
S=\frac{1}{2}(\sqrt2)^2\pi=\pi.
$$

由格林公式，

$$
\oint -y\,dx+x\,dy
=\iint 2\,dx\,dy
=2S=2\pi.
$$

于是

$$
W+2=2\pi,
$$

所以

$$
W=2(\pi-1).
$$

### 第 20 题

- 答案：$F(x)=\begin{cases}\dfrac{1}{2}e^x,&x<0,\\[2pt]1-\dfrac{1}{2}e^{-x},&x\ge0,\end{cases}$

分布函数定义为

$$
F(x)=\int_{-\infty}^{x}f(t)\,dt.
$$

当 $x<0$ 时，$|t|=-t$，所以

$$
F(x)=\int_{-\infty}^{x}\frac{1}{2}e^t\,dt
=\frac{1}{2}e^x.
$$

当 $x\ge 0$ 时，

$$
\begin{aligned}
F(x)
&=\int_{-\infty}^{0}\frac{1}{2}e^t\,dt
+\int_0^x\frac{1}{2}e^{-t}\,dt\\
&=\frac{1}{2}+\frac{1}{2}(1-e^{-x})\\
&=1-\frac{1}{2}e^{-x}.
\end{aligned}
$$

因此

$$
F(x)=
\begin{cases}
\dfrac{1}{2}e^x,&x<0,\\[2pt]
1-\dfrac{1}{2}e^{-x},&x\ge0.
\end{cases}
$$

### 第 21 题

- 答案：$0.3$

由加法公式，

$$
P(A\cup B)=P(A)+P(B)-P(AB).
$$

代入已知数据：

$$
0.6=0.4+0.3-P(AB),
$$

得

$$
P(AB)=0.1.
$$

所求为

$$
P(A\overline B)=P(A)-P(AB)=0.4-0.1=0.3.
$$

### 第 22 题

- 答案：$4$

若 $X$ 服从参数为 $2$ 的泊松分布，则

$$
E(X)=2.
$$

由期望的线性性质，

$$
E(Z)=E(3X-2)=3E(X)-2=3\cdot 2-2=4.
$$

### 第 23 题

- 答案：$f_X(x)=\begin{cases}2x,&0<x<1,\\0,&\text{其他},\end{cases}\quad D(Z)=\dfrac{2}{9}$

区域

$$
D:\ 0<x<1,\quad |y|<x
$$

的面积为

$$
S_D=\int_0^1 2x\,dx=1.
$$

因为 $(X,Y)$ 在 $D$ 上服从均匀分布，所以联合密度为

$$
f(x,y)=
\begin{cases}
1,&(x,y)\in D,\\
0,&(x,y)\notin D.
\end{cases}
$$

于是 $X$ 的边缘密度为

$$
f_X(x)=\int_{-\infty}^{+\infty}f(x,y)\,dy
=
\begin{cases}
\displaystyle\int_{-x}^{x}1\,dy=2x,&0<x<1,\\[4pt]
0,&\text{其他}.
\end{cases}
$$

计算 $X$ 的期望和二阶矩：

$$
E(X)=\int_0^1 x\cdot 2x\,dx=\frac{2}{3},
$$

$$
E(X^2)=\int_0^1 x^2\cdot 2x\,dx=\frac{1}{2}.
$$

所以

$$
D(X)=E(X^2)-[E(X)]^2
=\frac{1}{2}-\frac{4}{9}
=\frac{1}{18}.
$$

又

$$
Z=2X+1,
$$

故

$$
D(Z)=4D(X)=\frac{2}{9}.
$$
