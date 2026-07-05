# 2015 年数学二答案解析

资料类型：考研数学二答案解析
年份：2015
科目：数学二
整理状态：答案与解析按答案册清洗，并与题面同步。

## 答案速查

| 题号 | 题型 | 答案 |
|---|---|---|
| 1 | 选择题 | D |
| 2 | 选择题 | B |
| 3 | 选择题 | A |
| 4 | 选择题 | C |
| 5 | 选择题 | D |
| 6 | 选择题 | B |
| 7 | 选择题 | D |
| 8 | 选择题 | A |
| 9 | 填空题 | 48 |
| 10 | 填空题 | $n(n-1)(\ln 2)^{n-2}$ |
| 11 | 填空题 | 2 |
| 12 | 填空题 | $e^{-2x}+2e^x$ |
| 13 | 填空题 | $-\dfrac13(dx+2dy)$ |
| 14 | 填空题 | 21 |
| 15 | 解答题 | $a=-1,\ b=-\dfrac12,\ k=-\dfrac13$ |
| 16 | 解答题 | $A=\dfrac{8}{\pi}$ |
| 17 | 解答题 | 极小值为 $-1$，在点 $(0,-1)$ 处取得 |
| 18 | 解答题 | $\dfrac{\pi}{4}-\dfrac{2}{5}$ |
| 19 | 解答题 | 2 个 |
| 20 | 解答题 | 30 min |
| 21 | 证明题 | $a<x_0<b$ |
| 22 | 解答题 | （1）$a=0$；（2）$X=\begin{pmatrix}3&1&-2\\1&1&-1\\2&1&-1\end{pmatrix}$ |
| 23 | 解答题 | （1）$a=4,\ b=5$；（2）可取 $P=\begin{pmatrix}2&-3&-1\\1&0&-1\\0&1&1\end{pmatrix}$，$P^{-1}AP=\operatorname{diag}(1,1,5)$ |

## 详细解析

### 第 1 题

- 答案：D

对 (D)，有
$$
\int xe^{-x}\,dx=-(x+1)e^{-x}+C,
$$
因此
$$
\int_2^{+\infty}\frac{x}{e^x}\,dx
=\left[-(x+1)e^{-x}\right]_2^{+\infty}
=3e^{-2},
$$
所以收敛。

其余三项分别与
$\int x^{-1/2}\,dx$、
$\int \dfrac{\ln x}{x}\,dx$、
$\int \dfrac{1}{x\ln x}\,dx$
同型，均发散。

### 第 2 题

- 答案：B

当 $x\ne 0$ 时，
$$
f(x)=\exp\!\left(\lim_{t\to 0}\frac{\sin t}{x}\cdot \frac{x^2}{t}\right)
=e^x.
$$
因而 $x=0$ 是唯一可能的间断点。

又
$$
\lim_{x\to 0}f(x)=\lim_{x\to 0}e^x=1,
$$
只需补定义 $f(0)=1$ 就可使其连续，所以它在 $x=0$ 处有可去间断点。

### 第 3 题

- 答案：A

对 $x<0$，有 $f'(x)=0$，故 $f'_-(0)=0$。

对 $x>0$，
$$
f'(x)=\alpha x^{\alpha-1}\cos\!\left(\frac{1}{x^\beta}\right)
+\beta x^{\alpha-\beta-1}\sin\!\left(\frac{1}{x^\beta}\right).
$$
要使 $f'(x)$ 在 $x=0$ 处连续，需 $\lim\limits_{x\to 0^+}f'(x)=0$，
从而必须有
$$
\alpha-1>0,\qquad \alpha-\beta-1>0.
$$
尤其有 $\alpha-\beta>0$，故选 A。

### 第 4 题

- 答案：C

拐点对应于 $f''(x)$ 变号的点。由图像可见，$f''(x)$ 恰有两处变号，
因此曲线 $y=f(x)$ 有两个拐点，故选 C。

### 第 5 题

- 答案：D

令
$$
u=x+y,\qquad v=\frac{y}{x},
$$
解得
$$
x=\frac{u}{1+v},\qquad y=\frac{uv}{1+v}.
$$
于是
$$
f(u,v)=x^2-y^2
=\left(\frac{u}{1+v}\right)^2-\left(\frac{uv}{1+v}\right)^2
=\frac{u^2(1-v)}{1+v}.
$$
因而
$$
\frac{\partial f}{\partial u}=\frac{2u(1-v)}{1+v},\qquad
\frac{\partial f}{\partial v}=-\frac{2u^2}{(1+v)^2}.
$$
在 $(u,v)=(1,1)$ 处有
$$
\left.\frac{\partial f}{\partial u}\right|_{(1,1)}=0,\qquad
\left.\frac{\partial f}{\partial v}\right|_{(1,1)}=-\frac12.
$$
故选 D。

### 第 6 题

- 答案：B

改用极坐标
$$
x=r\cos\theta,\qquad y=r\sin\theta.
$$
由直线边界得
$$
\theta=\frac{\pi}{4},\qquad \theta=\frac{\pi}{3}.
$$
由双曲线边界
$$
2xy=1,\qquad 4xy=1
$$
分别得到
$$
r=\frac{1}{\sqrt{\sin2\theta}},\qquad
r=\frac{1}{\sqrt{2\sin2\theta}}.
$$
因而
$$
D=\left\{(r,\theta)\ \middle|\ \frac{\pi}{4}\le\theta\le\frac{\pi}{3},
\ \frac{1}{\sqrt{2\sin2\theta}}\le r\le\frac{1}{\sqrt{\sin2\theta}}\right\}.
$$
再乘雅可比 $r$，故选 B。

### 第 7 题

- 答案：D

对增广矩阵作初等变换：
$$
(A,b)\sim
\begin{pmatrix}
1&1&1&1\\
0&1&a-1&d-1\\
0&0&(a-1)(a-2)&(d-1)(d-2)
\end{pmatrix}.
$$
要使方程组有无穷多解，必须满足
$$
r(A)=r(A,b)<3.
$$
这等价于
$$
(a-1)(a-2)=0,\qquad (d-1)(d-2)=0,
$$
即 $a\in\{1,2\}$ 且 $d\in\{1,2\}$。
故选 D。

### 第 8 题

- 答案：A

由 $x=Py$，可知
$$
f=x^{\mathsf T}Ax=y^{\mathsf T}(P^{\mathsf T}AP)y
=2y_1^2+y_2^2-y_3^2,
$$
因而
$$
P^{\mathsf T}AP=
\begin{pmatrix}
2&0&0\\
0&1&0\\
0&0&-1
\end{pmatrix}.
$$
又
$$
Q=PC,\qquad
C=
\begin{pmatrix}
1&0&0\\
0&0&1\\
0&-1&0
\end{pmatrix},
$$
所以
$$
Q^{\mathsf T}AQ=C^{\mathsf T}(P^{\mathsf T}AP)C=
\begin{pmatrix}
2&0&0\\
0&-1&0\\
0&0&1
\end{pmatrix}.
$$
因此新标准形为
$$
2y_1^2-y_2^2+y_3^2,
$$
故选 A。

### 第 9 题

- 答案：48

由参数方程求导，
$$
\frac{dy}{dx}=\frac{dy/dt}{dx/dt}
=\frac{3+3t^2}{1/(1+t^2)}=3(1+t^2)^2.
$$
再对 $x$ 求导：
$$
\frac{d^2y}{dx^2}
=\frac{d[3(1+t^2)^2]/dt}{dx/dt}
=\frac{12t(1+t^2)}{1/(1+t^2)}
=12t(1+t^2)^2.
$$
代入 $t=1$，得
$$
\left.\frac{d^2y}{dx^2}\right|_{t=1}=48.
$$

### 第 10 题

- 答案：$n(n-1)(\ln 2)^{n-2}$

由莱布尼茨公式，
$$
f^{(n)}(0)=\sum_{k=0}^n\binom{n}{k}(x^2)^{(k)}(2^x)^{(n-k)}\Big|_{x=0}.
$$
只有 $k=2$ 项不为零，因此
$$
f^{(n)}(0)=\binom{n}{2}\cdot 2\cdot (\ln 2)^{n-2}
=n(n-1)(\ln 2)^{n-2}.
$$

### 第 11 题

- 答案：2

将 $x$ 看作积分号外的因子，有
$$
\varphi(x)=x\int_0^{x^2}f(t)\,dt.
$$
故
$$
\varphi'(x)=\int_0^{x^2}f(t)\,dt+2x^2f(x^2).
$$
代入 $x=1$，得
$$
\varphi(1)=\int_0^1f(t)\,dt=1,
$$
又
$$
\varphi'(1)=1+2f(1)=5,
$$
所以 $f(1)=2$。

### 第 12 题

- 答案：$e^{-2x}+2e^x$

由题意知
$$
y(0)=3,\qquad y'(0)=0.
$$
特征方程为
$$
\lambda^2+\lambda-2=0,
$$
解得 $\lambda_1=1,\ \lambda_2=-2$。
因而通解为
$$
y=C_1e^x+C_2e^{-2x}.
$$
代入初值条件
$$
C_1+C_2=3,\qquad C_1-2C_2=0,
$$
解得 $C_1=2,\ C_2=1$，所以
$$
y=2e^x+e^{-2x}.
$$

### 第 13 题

- 答案：$-\dfrac13(dx+2dy)$

当 $x=0,\ y=0$ 时，由
$$
e^{x+2y+3z}+xyz=1
$$
得 $z=0$。

对原式分别对 $x,y$ 求偏导，得到
$$
(3e^{x+2y+3z}+xy)\frac{\partial z}{\partial x}=-yz-e^{x+2y+3z},
$$
$$
(3e^{x+2y+3z}+xy)\frac{\partial z}{\partial y}=-xz-2e^{x+2y+3z}.
$$
代入 $(0,0,0)$，得
$$
\left.\frac{\partial z}{\partial x}\right|_{(0,0)}=-\frac13,\qquad
\left.\frac{\partial z}{\partial y}\right|_{(0,0)}=-\frac23.
$$
因而
$$
dz\big|_{(0,0)}=-\frac13\,dx-\frac23\,dy
=-\frac13(dx+2dy).
$$

### 第 14 题

- 答案：21

由矩阵多项式的特征值对应关系，$A$ 的特征值 $2,-2,1$
经变换 $\lambda^2-\lambda+1$ 后，
$B$ 的特征值分别为
$$
2^2-2+1=3,\qquad (-2)^2-(-2)+1=7,\qquad 1^2-1+1=1.
$$
故
$$
|B|=3\cdot 7\cdot 1=21.
$$

### 第 15 题

- 答案：$a=-1,\ b=-\dfrac12,\ k=-\dfrac13$

由
$$
\ln(1+x)=x-\frac{x^2}{2}+\frac{x^3}{3}+o(x^3),\qquad
\sin x=x-\frac{x^3}{6}+o(x^3),
$$
得
$$
f(x)=x+a\left(x-\frac{x^2}{2}+\frac{x^3}{3}\right)+bx\left(x-\frac{x^3}{6}\right)+o(x^3).
$$
整理为
$$
f(x)=(1+a)x+\left(b-\frac{a}{2}\right)x^2+\frac{a}{3}x^3+o(x^3).
$$
因 $f(x)\sim g(x)=kx^3$，必须满足
$$
1+a=0,\qquad b-\frac{a}{2}=0,\qquad \frac{a}{3}=k.
$$
解得
$$
a=-1,\qquad b=-\frac12,\qquad k=-\frac13.
$$

### 第 16 题

- 答案：$A=\dfrac{8}{\pi}$

绕 $x$ 轴旋转时，
$$
V_1=\pi\int_0^{\pi/2}(A\sin x)^2\,dx
=\pi A^2\int_0^{\pi/2}\sin^2x\,dx
=\pi A^2\cdot \frac{\pi}{4}
=\frac{\pi^2A^2}{4}.
$$
绕 $y$ 轴旋转时，用柱壳法：
$$
V_2=2\pi\int_0^{\pi/2}x(A\sin x)\,dx.
$$
分部积分可得
$$
\int_0^{\pi/2}x\sin x\,dx=1,
$$
因而
$$
V_2=2\pi A.
$$
由 $V_1=V_2$ 得
$$
\frac{\pi^2A^2}{4}=2\pi A.
$$
因 $A>0$，解得
$$
A=\frac{8}{\pi}.
$$

### 第 17 题

- 答案：极小值为 $-1$，在点 $(0,-1)$ 处取得

先由
$$
f''_{xy}(x,y)=2(y+1)e^x
$$
对 $y$ 积分，得
$$
f'_x(x,y)=(y^2+2y)e^x+\varphi(x).
$$
再由 $f'_x(x,0)=(x+1)e^x$，得
$$
\varphi(x)=(x+1)e^x.
$$
因而
$$
f'_x(x,y)=(y^2+2y)e^x+(x+1)e^x.
$$
再对 $x$ 积分，
$$
f(x,y)=(y^2+2y)e^x+xe^x+C(y).
$$
由 $f(0,y)=y^2+2y$ 得 $C(y)=0$，所以
$$
f(x,y)=e^x(x+y^2+2y).
$$

求驻点：由
$$
f_x=e^x(x+y^2+2y+1),\qquad
f_y=2(y+1)e^x,
$$
得 $y=-1$，代回得 $x=0$，故唯一驻点为 $(0,-1)$。

再求二阶偏导：
$$
f_{xx}=e^x(x+y^2+2y+2),\quad
f_{xy}=2(y+1)e^x,\quad
f_{yy}=2e^x.
$$
在 $(0,-1)$ 处有
$$
f_{xx}=1,\qquad f_{xy}=0,\qquad f_{yy}=2.
$$
因而
$$
f_{xx}f_{yy}-f_{xy}^2=2>0,\qquad f_{xx}>0,
$$
所以 $(0,-1)$ 是极小点。

极小值为
$$
f(0,-1)=-1.
$$

### 第 18 题

- 答案：$\dfrac{\pi}{4}-\dfrac{2}{5}$

由积分区域关于 $y$ 轴对称，且 $xy$ 关于 $y$ 轴为奇函数，
所以
$$
\iint_D xy\,dxdy=0.
$$
因而原积分化为
$$
\iint_D x^2\,dxdy.
$$
可写成
$$
2\int_0^1\int_{x^2}^{\sqrt{2-x^2}}x^2\,dydx
=2\int_0^1x^2\bigl(\sqrt{2-x^2}-x^2\bigr)\,dx.
$$
即
$$
2\int_0^1x^2\sqrt{2-x^2}\,dx-\frac{2}{5}.
$$
令 $x=\sqrt2\sin t$，则
$$
2\int_0^1x^2\sqrt{2-x^2}\,dx
=2\int_0^{\pi/4}2\sin^2t\cdot \sqrt2\cos t\cdot \sqrt2\cos t\,dt
=4\int_0^{\pi/4}\sin^2t\cos^2t\,dt.
$$
又
$$
4\sin^2t\cos^2t=\sin^22t,
$$
因而
$$
4\int_0^{\pi/4}\sin^2t\cos^2t\,dt
=\int_0^{\pi/4}\sin^22t\,dt
=\frac12\int_0^{\pi/2}\sin^2u\,du
=\frac{\pi}{4}.
$$
所以原积分为
$$
\frac{\pi}{4}-\frac{2}{5}.
$$

### 第 19 题

- 答案：2 个

由变上限积分求导，
$$
f'(x)=-\sqrt{1+x^2}+2x\sqrt{1+x^2}
=\sqrt{1+x^2}(2x-1).
$$
因此驻点为 $x=\dfrac12$，且
$$
f(x)\text{ 在 }(-\infty,\tfrac12)\text{ 上单调递减，在 }(\tfrac12,+\infty)\text{ 上单调递增。}
$$
所以 $f\!\left(\dfrac12\right)$ 是唯一极小值。

计算
$$
f\!\left(\frac12\right)
=\int_{1/2}^1\sqrt{1+t^2}\,dt+\int_1^{1/4}\sqrt{1+t}\,dt
=\int_{1/2}^1\sqrt{1+t^2}\,dt-\int_{1/4}^1\sqrt{1+t}\,dt.
$$
分拆为
$$
\int_{1/2}^1\sqrt{1+t^2}\,dt-\int_{1/2}^1\sqrt{1+t}\,dt-\int_{1/4}^{1/2}\sqrt{1+t}\,dt.
$$
在 $(1/2,1)$ 上有 $\sqrt{1+t^2}<\sqrt{1+t}$，故上式小于 $0$，所以
$$
f\!\left(\frac12\right)<0.
$$

另一方面，
$$
\lim_{x\to-\infty}f(x)=+\infty,
$$
且
$$
\lim_{x\to+\infty}f(x)=+\infty.
$$
因为函数在极小值点取负值，所以它在
$$
(-\infty,\tfrac12)\quad\text{和}\quad(\tfrac12,+\infty)
$$
上各有一个零点。

故零点个数为 $2$。

### 第 20 题

- 答案：30 min

设 $t$ 时刻物体温度为 $x(t)$，由牛顿冷却定律，
$$
\frac{dx}{dt}=-k(x-20)\qquad (k>0).
$$
解得
$$
x(t)=Ce^{-kt}+20.
$$
由 $x(0)=120$ 得 $C=100$，故
$$
x(t)=100e^{-kt}+20.
$$
又由 $x(1/2)=30$，得
$$
100e^{-k/2}+20=30
\quad\Longrightarrow\quad
e^{-k/2}=\frac{1}{10}
\quad\Longrightarrow\quad
k=2\ln 10.
$$
令 $x(t)=21$，则
$$
100e^{-2t\ln 10}+20=21
\quad\Longrightarrow\quad
e^{-2t\ln 10}=\frac{1}{100}
\quad\Longrightarrow\quad
t=1\text{ h}.
$$
因此从 $30\text{ min}$ 冷却到 $21^\circ\mathrm{C}$ 还需
$$
1\text{ h}-30\text{ min}=30\text{ min}.
$$

### 第 21 题

- 答案：$a<x_0<b$

点 $(b,f(b))$ 处的切线方程为
$$
y-f(b)=f'(b)(x-b).
$$
令 $y=0$，得
$$
x_0=b-\frac{f(b)}{f'(b)}.
$$

因为 $f'(x)>0$，故 $f(x)$ 单调递增；又 $f(a)=0$ 且 $b>a$，所以
$$
f(b)>0.
$$
再由 $f'(b)>0$，立得
$$
x_0=b-\frac{f(b)}{f'(b)}<b.
$$

下证 $x_0>a$。由拉格朗日中值定理，存在 $\xi\in(a,b)$，使
$$
\frac{f(b)-f(a)}{b-a}=f'(\xi),
$$
即
$$
\frac{f(b)}{b-a}=f'(\xi).
$$
因而
$$
x_0-a=b-a-\frac{f(b)}{f'(b)}
=\frac{f(b)}{f'(\xi)}-\frac{f(b)}{f'(b)}
=f(b)\frac{f'(b)-f'(\xi)}{f'(b)f'(\xi)}.
$$
由 $f''(x)>0$，知 $f'(x)$ 单调递增，于是
$$
f'(b)>f'(\xi),
$$
从而
$$
x_0-a>0.
$$
即 $x_0>a$。

综上，
$$
a<x_0<b.
$$

### 第 22 题

- 答案：(1) $a=0$；

(2) $X=\begin{pmatrix}
3&1&-2\\
1&1&-1\\
2&1&-1
\end{pmatrix}$。

由 $A^3=O$ 可知 $A$ 为幂零矩阵，因此
$$
|A|=0.
$$
计算
$$
|A|=a^3,
$$
所以
$$
a=0.
$$

代入后，原方程化为
$$
X(E-A^2)-AX(E-A^2)=E,
$$
即
$$
(E-A)X(E-A^2)=E.
$$
因为 $A^3=O$，所以 $E-A$ 与 $E-A^2$ 都可逆，从而
$$
X=(E-A)^{-1}(E-A^2)^{-1}
=\bigl[(E-A^2)(E-A)\bigr]^{-1}
=(E-A^2-A)^{-1}.
$$
当 $a=0$ 时，
$$
A=\begin{pmatrix}
0&1&0\\
1&0&-1\\
0&1&0
\end{pmatrix},
\qquad
E-A^2-A=
\begin{pmatrix}
0&-1&1\\
-1&1&1\\
-1&-1&2
\end{pmatrix}.
$$
直接求逆得
$$
X=
\begin{pmatrix}
3&1&-2\\
1&1&-1\\
2&1&-1
\end{pmatrix}.
$$

将该 $X$ 代回
$X-XA^2-AX+AXA^2=E$
可验证等式成立。

### 第 23 题

- 答案：(1) $a=4,\ b=5$；

(2) 可取
$$
P=\begin{pmatrix}
2&-3&-1\\
1&0&-1\\
0&1&1
\end{pmatrix},
$$
此时
$$
P^{-1}AP=\operatorname{diag}(1,1,5).
$$

因为 $A\sim B$，故相似矩阵的迹、行列式相等。

由迹相等，
$$
\operatorname{tr}(A)=3+a,\qquad \operatorname{tr}(B)=1+b+1=b+2,
$$
得
$$
a-b=-1.
$$
再由行列式相等可解得
$$
a=4,\qquad b=5.
$$

将 $a=4$ 代入，记
$$
A=E+C,\qquad
C=\begin{pmatrix}
-1&2&-3\\
-1&2&-3\\
1&-2&3
\end{pmatrix}
=
\begin{pmatrix}
-1\\ -1\\ 1
\end{pmatrix}
(1,-2,3).
$$
因而 $C$ 的特征值为 $0,0,4$，从而 $A$ 的特征值为
$$
1,\ 1,\ 5.
$$

对应 $\lambda=1$，可取两个线性无关特征向量
$$
\xi_1=(2,1,0)^{\mathsf T},\qquad
\xi_2=(-3,0,1)^{\mathsf T}.
$$
对应 $\lambda=5$，可取特征向量
$$
\xi_3=(-1,-1,1)^{\mathsf T}.
$$
以它们为列向量组成
$$
P=\begin{pmatrix}
2&-3&-1\\
1&0&-1\\
0&1&1
\end{pmatrix},
$$
则
$$
P^{-1}AP=\operatorname{diag}(1,1,5).
$$
