# Math 2 2004 Answers

资料类型：考研数学二答案解析
年份：2004
科目：数学二
整理状态：答案与解析按答案册清洗整理。

## 答案速查

| 题号 | 题型 | 答案 |
|---|---|---|
| 1 | 填空题 | $0$ |
| 2 | 填空题 | $(-\infty,1)$ |
| 3 | 填空题 | $\dfrac{\pi}{2}$ |
| 4 | 填空题 | $2$ |
| 5 | 填空题 | $y=x^3+\dfrac15\sqrt{x}$ |
| 6 | 填空题 | $\dfrac19$ |
| 7 | 选择题 | B |
| 8 | 选择题 | C |
| 9 | 选择题 | B |
| 10 | 选择题 | C |
| 11 | 选择题 | A |
| 12 | 选择题 | D |
| 13 | 选择题 | D |
| 14 | 选择题 | A |
| 15 | 解答题 | $-\dfrac16$ |
| 16 | 解答题 | 在 $[-2,0)$ 上，$f(x)=k(x+2)x(x+4)$；且当 $k=-\dfrac12$ 时，$f(x)$ 在 $x=0$ 处可导。 |
| 17 | 解答题 | 周期为 $\pi$；值域为 $\left[2-\sqrt2,\sqrt2\right]$。 |
| 18 | 解答题 | $\dfrac{S(t)}{V(t)}=2$；$\displaystyle\lim_{t\to+\infty}\dfrac{S(t)}{F(t)}=1$。 |
| 19 | 证明题 | 见解析 |
| 20 | 解答题 | $1.05\text{ km}$ |
| 21 | 解答题 | 设 $u=x^2-y^2,\ v=e^{xy}$，则
$$
z=f(u,v).
$$
有
$$
z_x=2x\,f_u+y e^{xy}f_v,
\qquad
z_y=-2y\,f_u+x e^{xy}f_v.
$$
进一步，
$$
z_{xy}
=-4xy\,f_{uu}+2x^2e^{xy}f_{uv}-2y^2e^{xy}f_{uv}+e^{xy}f_v+xye^{xy}f_v+x y e^{2xy}f_{vv}.
$$
（其中 $f_u,f_v,f_{uu},f_{uv},f_{vv}$ 均取在 $(u,v)=(x^2-y^2,e^{xy})$ 处。） |
| 22 | 解答题 | $a=0$ 或 $a=-10$；对应通解见解析。 |
| 23 | 解答题 | $a=-2$ 或 $a=-\dfrac23$；当 $a=-2$ 时可相似对角化，当 $a=-\dfrac23$ 时不可相似对角化。 |

## 详细解析

### 第 1 题

- 答案：$0$

当 $x=0$ 时，显然 $f(0)=0$。当 $x\neq 0$ 时，
$$
f(x)=\lim_{n\to\infty}\frac{(n-1)x}{nx^2+1}
=\lim_{n\to\infty}\frac{1-\frac1n}{x+\frac{1}{nx}}=\frac1x.
$$
因而
$$
f(x)=\begin{cases}
0,&x=0,\\[2mm]
\dfrac1x,&x\ne 0.
\end{cases}
$$
由 $\lim_{x\to 0}f(x)$ 不存在可知，$x=0$ 是间断点。

### 第 2 题

- 答案：$(-\infty,1)$

由参数方程可得
$$
\frac{dy}{dx}=\frac{dy/dt}{dx/dt}=\frac{3t^2-3}{3t^2+3}=\frac{t^2-1}{t^2+1}.
$$
再求二阶导数：
$$
\frac{d^2y}{dx^2}
=\frac{d}{dt}\!\left(\frac{t^2-1}{t^2+1}\right)\Big/\frac{dx}{dt}
=\frac{4t}{3(t^2+1)^3}.
$$
向上凸对应 $\dfrac{d^2y}{dx^2}<0$，故 $t<0$。又
$$
x=t^3+3t+1
$$
单调递增，且 $t=0$ 时 $x=1$，所以 $t<0$ 等价于 $x<1$。

### 第 3 题

- 答案：$\dfrac{\pi}{2}$

令 $x=\sec t$，则
$$
dx=\sec t\tan t\,dt,\qquad \sqrt{x^2-1}=\tan t.
$$
当 $x=1$ 时 $t=0$，当 $x\to+\infty$ 时 $t\to \dfrac{\pi}{2}$，故
$$
\int_1^{+\infty}\frac{dx}{x\sqrt{x^2-1}}
=\int_0^{\pi/2}dt
=\frac{\pi}{2}.
$$

### 第 4 题

- 答案：$2$

设
$$
F(x,y,z)=z-e^{2x-3z}-2y=0.
$$
则
$$
F_x=-2e^{2x-3z},\quad F_y=-2,\quad F_z=1+3e^{2x-3z}.
$$
因此
$$
z_x=-\frac{F_x}{F_z}=\frac{2e^{2x-3z}}{1+3e^{2x-3z}},\qquad
z_y=-\frac{F_y}{F_z}=\frac{2}{1+3e^{2x-3z}}.
$$
从而
$$
3z_x+z_y=\frac{6e^{2x-3z}+2}{1+3e^{2x-3z}}=2.
$$

### 第 5 题

- 答案：$y=x^3+\dfrac15\sqrt{x}$

原方程可化为
$$
\frac{dy}{dx}-\frac{1}{2x}y=\frac{x^2}{2}.
$$
先求齐次方程，得
$$
y_h=C\sqrt{x}.
$$
设特解为 $y_p=ax^3$，代入得 $a=1$，故通解为
$$
y=x^3+C\sqrt{x}.
$$
由条件 $y(1)=\dfrac65$ 可得 $C=\dfrac15$，故特解为
$$
y=x^3+\frac15\sqrt{x}.
$$

### 第 6 题

- 答案：$\dfrac19$

设 $C=BA^*$，则题设化为
$$
AC=2C+E,
$$
即
$$
(A-2E)C=E.
$$
由于
$$
A-2E=\begin{pmatrix}
0&1&0\\
1&0&0\\
0&0&-1
\end{pmatrix}
$$
可逆，且其行列式为 $1$，故 $|C|=1$。又
$$
C=BA^* \quad\Rightarrow\quad |C|=|B|\cdot|A^*|.
$$
由 $|A|=3$ 且 $A$ 为 $3$ 阶矩阵，知
$$
|A^*|=|A|^{2}=9.
$$
因而
$$
|B|=\frac{|C|}{|A^*|}=\frac19.
$$

### 第 7 题

- 答案：B

当 $x\to 0^+$ 时，
$$
\alpha\sim\int_0^x1\,dt=x.
$$
对 $\beta$ 令 $u=\sqrt t$，得
$$
\beta=2\int_0^x u\tan u\,du\sim 2\int_0^x u^2\,du=\frac23x^3.
$$
而
$$
\gamma\sim\int_0^{\sqrt x}t^3\,dt=\frac14x^2.
$$
所以
$$
\alpha\gg \gamma\gg \beta,
$$
即排列为 $\alpha,\gamma,\beta$。

### 第 8 题

- 答案：C

在 $x<0$ 时，
$$
f(x)=x^2-x;
$$
在 $0\le x\le 1$ 时，
$$
f(x)=x-x^2.
$$
因为 $f(0)=0$ 且其邻域内 $f(x)\ge 0$，所以 $x=0$ 为极小值点。又
$$
f''(x)=\begin{cases}
2,&x<0,\\
-2,&0<x<1,
\end{cases}
$$
凹凸性在 $x=0$ 左右发生改变，因此 $(0,0)$ 是拐点。

### 第 9 题

- 答案：B

设所求极限为 $L$，则
$$
L=\lim_{n\to\infty}\frac{2}{n}\sum_{k=1}^n\ln\left(1+\frac{k}{n}\right).
$$
这是函数 $\ln(1+x)$ 在 $[0,1]$ 上的黎曼和，因此
$$
L=2\int_0^1\ln(1+x)\,dx
=2\int_1^2\ln x\,dx.
$$
故选 B。

### 第 10 题

- 答案：C

由 $f'(0)>0$，根据导数定义，存在 $\delta>0$，当 $0<|x|<\delta$ 时有
$$
\frac{f(x)-f(0)}{x}>0.
$$
因而对 $x\in(0,\delta)$，有 $f(x)-f(0)>0$，即 $f(x)>f(0)$。故 C 正确。

### 第 11 题

- 答案：A

对多项式项 $x^2+1$，特解可设为 $ax^2+bx+c$。齐次方程
$$
y''+y=0
$$
的解为 $\sin x,\cos x$，右端含有共振项 $\sin x$，故对应特解应补乘 $x$，设为
$$
x(A\sin x+B\cos x).
$$
合并得应选 A。

### 第 12 题

- 答案：D

由
$$
x^2+y^2\le 2y
$$
可知该区域是圆 $x^2+(y-1)^2\le 1$。在极坐标下，
$$
r^2\le 2r\sin\theta \quad\Rightarrow\quad 0\le r\le 2\sin\theta,\quad 0\le \theta\le \pi.
$$
又
$$
xy=r^2\sin\theta\cos\theta,\qquad dxdy=r\,dr\,d\theta.
$$
因此应选 D。

### 第 13 题

- 答案：D

交换第 $1$、$2$ 列相当于右乘
$$
S=\begin{pmatrix}
0&1&0\\
1&0&0\\
0&0&1
\end{pmatrix}.
$$
再把第 $2$ 列加到第 $3$ 列，相当于右乘
$$
T=\begin{pmatrix}
1&0&0\\
0&1&1\\
0&0&1
\end{pmatrix}.
$$
所以
$$
C=AST=A(ST),
$$
从而
$$
Q=ST=\begin{pmatrix}
0&1&1\\
1&0&0\\
0&0&1
\end{pmatrix}.
$$

### 第 14 题

- 答案：A

由 $AB=0$ 且 $B\ne 0$，知 $B$ 至少有一个非零列向量 $\beta$ 满足
$$
A\beta=0.
$$
于是齐次方程组 $Ax=0$ 有非零解，故 $A$ 的列向量组线性相关。

另一方面，由 $A\ne 0$，取 $A$ 的一个非零行向量组合作为系数，可得
$$
\alpha^\mathrm{T}B=0
$$
有非零系数解，因此 $B$ 的行向量组线性相关。故选 A。

### 第 15 题

- 答案：$-\dfrac16$

设
$$
L=\lim_{x\to0}\frac{\left(\frac{2+\cos x}{3}\right)^x-1}{x^3}.
$$
先取对数化简指数：
$$
\left(\frac{2+\cos x}{3}\right)^x
=\exp\!\left(x\ln\frac{2+\cos x}{3}\right).
$$
因此关键在于求
$$
\lim_{x\to0}\frac{1}{x^2}\ln\frac{2+\cos x}{3}.
$$
由 $\cos x=1-\dfrac{x^2}{2}+o(x^2)$，得
$$
\frac{2+\cos x}{3}=1-\frac{x^2}{6}+o(x^2),
$$
从而
$$
\ln\frac{2+\cos x}{3}=-\frac{x^2}{6}+o(x^2).
$$
所以
$$
x\ln\frac{2+\cos x}{3}=-\frac{x^3}{6}+o(x^3),
$$
进而
$$
\left(\frac{2+\cos x}{3}\right)^x-1=-\frac{x^3}{6}+o(x^3).
$$
故
$$
L=-\frac16.
$$

### 第 16 题

- 答案：在 $[-2,0)$ 上，$f(x)=k(x+2)x(x+4)$；且当 $k=-\dfrac12$ 时，$f(x)$ 在 $x=0$ 处可导。

因为当 $-2\le x<0$ 时，$x+2\in[0,2)$，由题设递推关系
$$
f(x)=kf(x+2)=k(x+2)\bigl((x+2)^2-4\bigr)
=k(x+2)x(x+4).
$$
这就得到
$$
f(x)=k(x+2)x(x+4),\qquad -2\le x<0.
$$

再讨论 $x=0$ 处可导性。右导数为
$$
f'_+(0)=\left[x(x^2-4)\right]'_{x=0}=-4.
$$
左导数由上式得
$$
f'_-(0)=\left[k(x+2)x(x+4)\right]'_{x=0}=8k.
$$
可导要求左右导数相等，故
$$
8k=-4\quad\Rightarrow\quad k=-\frac12.
$$

### 第 17 题

- 答案：周期为 $\pi$；值域为 $\left[2-\sqrt2,\sqrt2\right]$。

由 $|\sin(t+\pi)|=|\sin t|$，有
$$
f(x+\pi)=\int_{x+\pi}^{x+\frac{3\pi}{2}}|\sin t|\,dt.
$$
令 $u=t-\pi$，则
$$
f(x+\pi)=\int_x^{x+\frac{\pi}{2}}|\sin(u+\pi)|\,du
=\int_x^{x+\frac{\pi}{2}}|\sin u|\,du=f(x),
$$
故 $f(x)$ 以 $\pi$ 为周期。

只需在 $[0,\pi]$ 上求值域。由变上限积分求导公式，
$$
f'(x)=\left|\sin\left(x+\frac{\pi}{2}\right)\right|-|\sin x|
=|\cos x|-|\sin x|.
$$
在 $[0,\pi]$ 上可解得驻点 $x=\dfrac{\pi}{4},\dfrac{3\pi}{4}$。
分别计算：
$$
f\!\left(\frac{\pi}{4}\right)=\sqrt2,\qquad
f\!\left(\frac{3\pi}{4}\right)=2-\sqrt2,
$$
且
$$
f(0)=f(\pi)=1.
$$
因而最大值为 $\sqrt2$，最小值为 $2-\sqrt2$，值域为
$$
\left[2-\sqrt2,\sqrt2\right].
$$

### 第 18 题

- 答案：$\dfrac{S(t)}{V(t)}=2$；$\displaystyle\lim_{t\to+\infty}\dfrac{S(t)}{F(t)}=1$。

记
$$
y=\frac{e^x+e^{-x}}{2}=\cosh x.
$$
则
$$
y'=\sinh x,\qquad 1+(y')^2=\cosh^2x=y^2.
$$
因而侧面积
$$
S(t)=2\pi\int_0^t y\sqrt{1+(y')^2}\,dx
=2\pi\int_0^t y^2\,dx.
$$
体积
$$
V(t)=\pi\int_0^t y^2\,dx.
$$
所以
$$
\frac{S(t)}{V(t)}=2.
$$

又底面积为
$$
F(t)=\pi y(t)^2=\pi\cosh^2 t.
$$
因而
$$
\frac{S(t)}{F(t)}
=\frac{2\int_0^t \cosh^2x\,dx}{\cosh^2 t}.
$$
当 $t\to+\infty$ 时，用主项估计 $\cosh^2x\sim \dfrac14e^{2x}$，于是
$$
2\int_0^t\cosh^2x\,dx\sim \frac14e^{2t},\qquad
\cosh^2t\sim \frac14e^{2t},
$$
故
$$
\lim_{t\to+\infty}\frac{S(t)}{F(t)}=1.
$$

### 第 19 题

- 答案：见解析

设
$$
g(x)=\ln^2x.
$$
因为 $g$ 在 $[a,b]$ 上连续、在 $(a,b)$ 内可导，由拉格朗日中值定理，存在 $\xi\in(a,b)$，使
$$
\ln^2b-\ln^2a=g'(\xi)(b-a)=\frac{2\ln\xi}{\xi}(b-a).
$$
于是只需证明
$$
\frac{2\ln\xi}{\xi}>\frac4{e^2}.
$$
令
$$
h(x)=\frac{2\ln x}{x}.
$$
则
$$
h'(x)=\frac{2(1-\ln x)}{x^2}.
$$
在区间 $(e,e^2)$ 上有 $1<\ln x<2$，所以 $h'(x)<0$，即 $h$ 在 $(e,e^2)$ 上单调递减。
又由于 $\xi\in(a,b)\subset(e,e^2)$，故
$$
h(\xi)>h(e^2)=\frac{2\ln(e^2)}{e^2}=\frac4{e^2}.
$$
从而
$$
\ln^2b-\ln^2a=\frac{2\ln\xi}{\xi}(b-a)>\frac4{e^2}(b-a).
$$
证毕。

### 第 20 题

- 答案：$1.05\text{ km}$

设飞机速度为 $v(t)$，位移为 $x(t)$。由牛顿第二定律，
$$
m\frac{dv}{dt}=-kv.
$$
分离变量并积分，得
$$
v(t)=v_0e^{-kt/m},
$$
其中 $m=9000,\ v_0=700\text{ km/h}$。

又
$$
\frac{dx}{dt}=v(t),
$$
所以从着陆到最终停下的总滑行距离为
$$
x_{\max}=\int_0^{+\infty}v_0e^{-kt/m}\,dt=\frac{mv_0}{k}.
$$
代入数据可得
$$
x_{\max}=1.05\text{ km}.
$$

### 第 21 题

- 答案：设 $u=x^2-y^2,\ v=e^{xy}$，则
$$
z=f(u,v).
$$
有
$$
z_x=2x\,f_u+y e^{xy}f_v,
\qquad
z_y=-2y\,f_u+x e^{xy}f_v.
$$
进一步，
$$
z_{xy}
=-4xy\,f_{uu}+2x^2e^{xy}f_{uv}-2y^2e^{xy}f_{uv}+e^{xy}f_v+xye^{xy}f_v+x y e^{2xy}f_{vv}.
$$
（其中 $f_u,f_v,f_{uu},f_{uv},f_{vv}$ 均取在 $(u,v)=(x^2-y^2,e^{xy})$ 处。）

设
$$
u=x^2-y^2,\qquad v=e^{xy},
$$
则
$$
u_x=2x,\ u_y=-2y,\ v_x=ye^{xy},\ v_y=xe^{xy}.
$$
因而
$$
z_x=f_u u_x+f_v v_x=2x\,f_u+y e^{xy}f_v,
$$
$$
z_y=f_u u_y+f_v v_y=-2y\,f_u+x e^{xy}f_v.
$$
再对 $z_x$ 关于 $y$ 求导，得
$$
z_{xy}
=2x(f_{uu}u_y+f_{uv}v_y)+e^{xy}f_v+y\!\left(f_{vu}u_y+f_{vv}v_y\right)e^{xy}+xy e^{xy}f_v.
$$
利用 $f_{uv}=f_{vu}$ 并代入各偏导，可整理为
$$
z_{xy}
=-4xy\,f_{uu}+(2x^2-2y^2)e^{xy}f_{uv}+(1+xy)e^{xy}f_v+xye^{2xy}f_{vv}.
$$

### 第 22 题

- 答案：$a=0$ 或 $a=-10$；对应通解见解析。

将方程组写成矩阵形式 $Ax=0$。注意到系数矩阵可写为
$$
A=aI+\begin{pmatrix}1\\2\\3\\4\end{pmatrix}(1,1,1,1).
$$
若记 $s=x_1+x_2+x_3+x_4$，则各方程统一写成
$$
ax_i+i\,s=0,\qquad i=1,2,3,4.
$$

要有非零解，必须使系数矩阵奇异。由矩阵行列式引理，
$$
\det A=a^4\left(1+\frac{1+2+3+4}{a}\right)=a^3(a+10).
$$
因而有非零解当且仅当
$$
a=0\quad\text{或}\quad a=-10.
$$

1. 当 $a=0$ 时，四个方程都化为
$$
x_1+x_2+x_3+x_4=0.
$$
取 $x_2,x_3,x_4$ 为自由变量，则
$$
x_1=-x_2-x_3-x_4.
$$
通解为
$$
x=c_1(-1,1,0,0)^\mathrm{T}+c_2(-1,0,1,0)^\mathrm{T}+c_3(-1,0,0,1)^\mathrm{T}.
$$

2. 当 $a=-10$ 时，由 $-10x_i+i\,s=0$ 得
$$
x_i=\frac{i}{10}s.
$$
于是
$$
x_1:x_2:x_3:x_4=1:2:3:4,
$$
通解为
$$
x=t(1,2,3,4)^\mathrm{T}.
$$

### 第 23 题

- 答案：$a=-2$ 或 $a=-\dfrac23$；当 $a=-2$ 时可相似对角化，当 $a=-\dfrac23$ 时不可相似对角化。

计算特征多项式：
$$
\det(\lambda E-A)=\lambda^3-10\lambda^2+(34+3a)\lambda-(36+6a).
$$
若其有二重根 $\lambda_0$，则 $\lambda_0$ 既满足特征方程，也满足导方程
$$
3\lambda^2-20\lambda+(34+3a)=0.
$$
消去 $a$ 后可得
$$
(\lambda_0-2)^2(\lambda_0-4)=0.
$$
因而二重根只能是 $\lambda_0=2$ 或 $\lambda_0=4$。

1. 当 $\lambda_0=2$ 时，代回得
$$
a=-2.
$$
此时
$$
\chi_A(\lambda)=(\lambda-2)^2(\lambda-6).
$$
又
$$
A-2E=\begin{pmatrix}
-1&2&-3\\
-1&2&-3\\
1&-2&3
\end{pmatrix}
$$
的秩为 $1$，故特征值 $2$ 的特征子空间维数为 $2$，等于其代数重数，所以 $A$ 可相似对角化。

2. 当 $\lambda_0=4$ 时，代回得
$$
a=-\frac23.
$$
此时
$$
\chi_A(\lambda)=(\lambda-4)^2(\lambda-2).
$$
检查 $A-4E$ 可知特征值 $4$ 只对应一个线性无关特征向量，其几何重数为 $1$，小于代数重数 $2$，因此 $A$ 不可相似对角化。
