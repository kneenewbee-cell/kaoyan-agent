# Math 2 1997 Answers

资料类型：考研数学二答案解析
年份：1997
科目：数学二
范围：试卷 III
校对状态：已按答案页图像清洗并与题面同步。

## 答案速查

| 题号 | 题型 | 答案 |
|---|---|---|
| 1 | 填空题 | $e^{-1/2}$ |
| 2 | 填空题 | $-\dfrac{3}{2}$ |
| 3 | 填空题 | $2\arcsin\dfrac{\sqrt{x}}{2}+C$ |
| 4 | 填空题 | $\dfrac{\pi}{8}$ |
| 5 | 填空题 | $3$ |
| 6 | 选择题 | $C$ |
| 7 | 选择题 | $B$ |
| 8 | 选择题 | $B$ |
| 9 | 选择题 | $A$ |
| 10 | 选择题 | $D$ |
| 11 | 解答题 | $1$ |
| 12 | 解答题 | $\dfrac{(1+t^2)(y^2-e^t)}{2(1-ty)}$ |
| 13 | 解答题 | $e^{2x}\tan x+C$ |
| 14 | 解答题 | $x^3+x^2y-xy^2=C$ |
| 15 | 解答题 | $y''-y'-2y=(1-2x)e^x$ |
| 16 | 解答题 | $\begin{pmatrix}0&2&1\\0&0&0\\0&0&0\end{pmatrix}$ |
| 17 | 解答题 | 当 $\lambda\neq 1,-\dfrac45$ 时有唯一解；当 $\lambda=-\dfrac45$ 时无解；当 $\lambda=1$ 时有无穷多解，通解为
$$
x_1=1,\quad x_2=-1+k,\quad x_3=k\qquad(k\in\mathbb R).
$$
 |
| 18 | 解答题 | $x\pm \sqrt3\,y=2$ |
| 19 | 解答题 | $f(x)=\dfrac a2x^3+(4-a)x$，当 $a=-5$ 时体积最小。 |
| 20 | 证明题 | 当 $x\ne 0$ 时，
$$
\varphi'(x)=\frac{x f(x)-\int_0^x f(u)\,du}{x^2};
$$
且
$$
\varphi'(0)=A,
$$
并且 $\varphi'(x)$ 在 $x=0$ 处连续。 |
| 21 | 证明题 | 设
$$
g(x)=x-\frac{\pi}{2}\sin x,
$$
则它在 $\left(0,\dfrac{\pi}{2}\right)$ 内有唯一极小点
$$
x_0=\arccos\frac{2}{\pi},
$$
极小值
$$
k_0=g(x_0)=\arccos\frac{2}{\pi}-\frac12\sqrt{\pi^2-4}<0.
$$
因此：

- 当 $k\ge 0$ 或 $k<k_0$ 时，无根；
- 当 $k=k_0$ 时，有且仅有一根；
- 当 $k_0<k<0$ 时，有两根。 |

## 详细解析

### 第 1 题

- 答案?$e^{-1/2}$

由连续性可得
$$
a=\lim_{x\to 0}(\cos x)^{x^{-2}}.
$$
取对数，
$$
\ln a=\lim_{x\to 0}\frac{\ln(\cos x)}{x^2}.
$$
利用 $\ln(\cos x)\sim-\dfrac{x^2}{2}$，得
$$
\ln a=-\frac12,
$$
故
$$
a=e^{-1/2}=\frac{1}{\sqrt e}.
$$

### 第 2 题

- 答案：$-\dfrac{3}{2}$

化简得
$$
y=\frac12\ln(1-x)-\frac12\ln(1+x^2).
$$
逐次求导并代入 $x=0$，可得
$$
y'''(0)=-\frac32.
$$

### 第 3 题

- 答案：$2\arcsin\dfrac{\sqrt{x}}{2}+C$

令
$$
x=4\sin^2\theta,
$$
则
$$
dx=8\sin\theta\cos\theta\,d\theta,\qquad
\sqrt{x(4-x)}=4\sin\theta\cos\theta.
$$
原式化为
$$
\int 2\,d\theta=2\theta+C=2\arcsin\frac{\sqrt{x}}{2}+C.
$$

### 第 4 题

- 答案：$\dfrac{\pi}{8}$

配方得
$$
x^2+4x+8=(x+2)^2+2^2.
$$
因此
$$
\int_0^{+\infty}\frac{dx}{x^2+4x+8}
=\frac12\int_0^{+\infty}\frac{dx}{\left(\frac{x+2}{2}\right)^2+1}
=\frac12\left[\arctan\frac{x+2}{2}\right]_0^{+\infty}
=\frac{\pi}{8}.
$$

### 第 5 题

- 答案：$3$

由秩为 $2$ 可知三向量线性相关。取三阶子式
$$
\begin{vmatrix}
1&2&0\\
2&0&-4\\
-1&t&5
\end{vmatrix}=0,
$$
化简得
$$
3-t=0,
$$
故
$$
t=3.
$$

### 第 6 题

- 答案：$C$

由
$$
\tan x=x+\frac{x^3}{3}+o(x^3),
$$
得
$$
e^{\tan x}-e^x=e^x\bigl(e^{\tan x-x}-1\bigr)\sim \tan x-x\sim \frac{x^3}{3}.
$$
故它与 $x^3$ 同阶，应选 $C$。

### 第 7 题

- 答案?$B$

$f'(x)<0$ 表明 $f(x)$ 单调递减，因此右端点矩形面积小于曲边梯形面积：
$$
S_2<S_1.
$$
又 $f''(x)>0$ 表明曲线为凸函数，连接端点的弦在曲线上方，所以梯形面积大于曲边梯形面积：
$$
S_1<S_3.
$$
综上
$$
S_2<S_1<S_3,
$$
故选 B。

### 第 8 题

- 答案：$B$

由 $f'(x_0)=0$ 代入题设，得
$$
x_0f''(x_0)=1-e^{-x_0}.
$$
右端与 $x_0$ 同号，故
$$
f''(x_0)>0.
$$
所以 $x_0$ 为极小值点，应选 $B$。

### 第 9 题

- 答案：$A$

被积函数 $e^{\sin t}\sin t$ 是以 $2\pi$ 为周期的函数，所以
$$
F(x)
$$
与起点 $x$ 无关，是常数。又
$$
\int_0^{2\pi}e^{\sin t}\sin t\,dt>0,
$$
故 $F(x)$ 为正常数，应选 $A$。

### 第 10 题

- 答案：$D$

当 $x<0$ 时，$f(x)=x^2>0$，故
$$
g(f(x))=x^2+2.
$$
当 $x\ge 0$ 时，$f(x)=-x\le 0$，故
$$
g(f(x))=2-(-x)=x+2.
$$
因此应选 $D$。

### 第 11 题

- 答案：$1$

分子、分母同除以 $x$，并注意 $x\to-\infty$ 时 $|x|=-x$。于是
$$
\sqrt{4x^2+x-1}=-x\sqrt{4+\frac1x-\frac1{x^2}},\qquad
\sqrt{x^2+\sin x}=-x\sqrt{1+\frac{\sin x}{x^2}}.
$$
从而原极限化为
$$
\frac{\sqrt{4+\frac1x-\frac1{x^2}}-1-\frac1x}{\sqrt{1+\frac{\sin x}{x^2}}}\to 1.
$$

### 第 12 题

- 答案：$\dfrac{(1+t^2)(y^2-e^t)}{2(1-ty)}$

对参数 $t$ 求导，
$$
\frac{dx}{dt}=\frac{1}{1+t^2}.
$$
对方程 $2y-ty^2+e^t=5$ 两边求导，得
$$
2\frac{dy}{dt}-y^2-2ty\frac{dy}{dt}+e^t=0,
$$
即
$$
\frac{dy}{dt}=\frac{y^2-e^t}{2(1-ty)}.
$$
因此
$$
\frac{dy}{dx}=\frac{dy/dt}{dx/dt}
=\frac{(1+t^2)(y^2-e^t)}{2(1-ty)}.
$$

### 第 13 题

- 答案：$e^{2x}\tan x+C$

注意到
$$
(\tan x+1)^2=\tan^2x+2\tan x+1=\sec^2x+2\tan x.
$$
而
$$
\frac{d}{dx}\bigl(e^{2x}\tan x\bigr)=2e^{2x}\tan x+e^{2x}\sec^2x
=e^{2x}(\tan x+1)^2.
$$
故原积分为
$$
e^{2x}\tan x+C.
$$

### 第 14 题

- 答案：$x^3+x^2y-xy^2=C$

方程为齐次微分方程。令
$$
y=ux,\qquad dy=u\,dx+x\,du,
$$
代入并整理后可分离变量，积分可得
$$
x^3+x^2y-xy^2=C.
$$
直接检验其微分恰与原方程对应。

### 第 15 题

- 答案：$y''-y'-2y=(1-2x)e^x$

由
$$
y_1-y_3=e^{-x},\qquad y_3-y_2=e^{2x}
$$
知相应齐次方程有两个线性无关解 $e^{-x},e^{2x}$，其特征方程为
$$
(r+1)(r-2)=0,
$$
故齐次部分为
$$
y''-y'-2y=0.
$$
再取非齐次方程的一个特解 $y=xe^x$，代入得
$$
y''-y'-2y=(1-2x)e^x.
$$
故所求方程为
$$
y''-y'-2y=(1-2x)e^x.
$$

### 第 16 题

- 答案：$\begin{pmatrix}0&2&1\\0&0&0\\0&0&0\end{pmatrix}$

由
$$
A^2-AB=E
$$
得
$$
A(A-B)=E.
$$
因为 $A$ 可逆，所以
$$
A-B=A^{-1},\qquad B=A-A^{-1}.
$$
算得
$$
A^{-1}=
\begin{pmatrix}
1&-1&-2\\
0&1&1\\
0&0&-1
\end{pmatrix},
$$
从而
$$
B=
\begin{pmatrix}
0&2&1\\
0&0&0\\
0&0&0
\end{pmatrix}.
$$

### 第 17 题

- 答案：当 $\lambda\neq 1,-\dfrac45$ 时有唯一解；当 $\lambda=-\dfrac45$ 时无解；当 $\lambda=1$ 时有无穷多解，通解为
$$
x_1=1,\quad x_2=-1+k,\quad x_3=k\qquad(k\in\mathbb R).
$$


对增广矩阵作初等行变换，系数矩阵行列式为
$$
|A|=(\lambda-1)(5\lambda+4).
$$
因此：

当
$$
\lambda\neq 1,-\frac45
$$
时，系数矩阵可逆，方程组有唯一解。

当
$$
\lambda=-\frac45
$$
时，化简后出现矛盾方程，故无解。

当
$$
\lambda=1
$$
时，秩小于未知量个数，故有无穷多解。化简后可取
$$
x_3=k,
$$
得到
$$
x_1=1,\qquad x_2=-1+k,\qquad x_3=k.
$$

### 第 18 题

- 答案：$x\pm \sqrt3\,y=2$

设从 $M_0$ 到 $M$ 的弧长为
$$
s=\int_0^\theta\sqrt{r^2+\left(\frac{dr}{d\theta}\right)^2}\,d\theta,
$$
扇形面积为
$$
\frac12\int_0^\theta r^2\,d\theta.
$$
由题设
$$
\frac12\int_0^\theta r^2\,d\theta=\frac12 s.
$$
两边对 $\theta$ 求导，得
$$
r^2=\sqrt{r^2+\left(\frac{dr}{d\theta}\right)^2}.
$$
整理并积分，可得
$$
\arccos\frac1r=\pm\theta+\frac{\pi}{3}.
$$
再由 $M_0(2,0)$ 代入，化为直角坐标式即
$$
x\pm\sqrt3\,y=2.
$$

### 第 19 题

- 答案：$f(x)=\dfrac a2x^3+(4-a)x$，当 $a=-5$ 时体积最小。

由方程
$$
xf'(x)-f(x)=\frac{3a}{2}x^2
$$
化为
$$
\left(\frac{f(x)}{x}\right)'=\frac{3a}{2}.
$$
积分得
$$
f(x)=\frac a2x^3+Cx.
$$
再由面积条件
$$
\int_0^1 f(x)\,dx=2
$$
求得
$$
C=4-a.
$$
所以
$$
f(x)=\frac a2x^3+(4-a)x.
$$
将其代入旋转体体积公式
$$
V=\pi\int_0^1 f(x)^2\,dx
$$
得到关于 $a$ 的二次函数，求极小值得
$$
a=-5.
$$

### 第 20 题

- 答案：当 $x\ne 0$ 时，
$$
\varphi'(x)=\frac{x f(x)-\int_0^x f(u)\,du}{x^2};
$$
且
$$
\varphi'(0)=A,
$$
并且 $\varphi'(x)$ 在 $x=0$ 处连续。

当 $x\ne 0$ 时，令 $u=xt$，则
$$
\varphi(x)=\int_0^1 f(xt)\,dt=\frac1x\int_0^x f(u)\,du.
$$
故
$$
\varphi'(x)=\frac{x f(x)-\int_0^x f(u)\,du}{x^2}\qquad(x\ne 0).
$$
又由
$$
\lim_{x\to 0}\frac{f(x)}{x}=A
$$
可得 $f(0)=0$，进而由导数定义算得
$$
\varphi'(0)=A.
$$
再比较
$$
\lim_{x\to 0}\varphi'(x)=A=\varphi'(0),
$$
故 $\varphi'(x)$ 在 $x=0$ 处连续。

### 第 21 题

- 答案：设
$$
g(x)=x-\frac{\pi}{2}\sin x,
$$
则它在 $\left(0,\dfrac{\pi}{2}\right)$ 内有唯一极小点
$$
x_0=\arccos\frac{2}{\pi},
$$
极小值
$$
k_0=g(x_0)=\arccos\frac{2}{\pi}-\frac12\sqrt{\pi^2-4}<0.
$$
因此：

- 当 $k\ge 0$ 或 $k<k_0$ 时，无根；
- 当 $k=k_0$ 时，有且仅有一根；
- 当 $k_0<k<0$ 时，有两根。

令
$$
g(x)=x-\frac{\pi}{2}\sin x.
$$
则
$$
g'(x)=1-\frac{\pi}{2}\cos x.
$$
由 $g'(x)=0$ 得唯一驻点
$$
x_0=\arccos\frac{2}{\pi}.
$$
并且
$$
g''(x)=\frac{\pi}{2}\sin x>0\qquad\left(0<x<\frac{\pi}{2}\right),
$$
故 $x_0$ 为唯一极小点。其极小值为
$$
k_0=g(x_0)=\arccos\frac{2}{\pi}-\frac12\sqrt{\pi^2-4}<0.
$$
又有
$$
\lim_{x\to 0^+}g(x)=0,\qquad g\!\left(\frac{\pi}{2}\right)=0.
$$
于是可得：

- 当 $k\ge 0$ 或 $k<k_0$ 时，直线 $y=k$ 与曲线 $y=g(x)$ 无交点；
- 当 $k=k_0$ 时，恰与极小点相切，故有一根；
- 当 $k_0<k<0$ 时，有两个交点，故有两根。
