# Math 1 2003 Answers

资料类型：考研数学一答案解析
年份：2003
科目：数学一
范围：试卷 I
来源：D:\百度网盘\高数资料\【02】1987-2022年数学一真题详解答案（PDF）\2003考研数学一真题解析.pdf
校对状态：已按答案页图像和题干重新整理，去除识别碎行、串题内容和非本题页脚。

## 答案速查

| 题号 | 题型 | 答案 |
|---|---|---|
| 1 | 填空题 | $\dfrac{1}{\sqrt{e}}$ |
| 2 | 填空题 | $2x+4y-z=5$ |
| 3 | 填空题 | $1$ |
| 4 | 填空题 | $\begin{pmatrix}2&3\\-1&-2\end{pmatrix}$ |
| 5 | 填空题 | $\dfrac{1}{4}$ |
| 6 | 填空题 | $(39.51,\ 40.49)$ |
| 7 | 选择题 | C |
| 8 | 选择题 | D |
| 9 | 选择题 | A |
| 10 | 选择题 | D |
| 11 | 选择题 | B |
| 12 | 选择题 | C |
| 13 | 解答题 | $A=\dfrac{e}{2}-1$；$\displaystyle V=\dfrac{\pi}{6}(5e^2-12e+3)$ |
| 14 | 解答题 | $\displaystyle \arctan\frac{1-2x}{1+2x}=\frac{\pi}{4}-2\sum_{n=0}^{\infty}\frac{(-1)^n4^n}{2n+1}x^{2n+1}$；$\displaystyle \sum_{n=0}^{\infty}\frac{(-1)^n}{2n+1}=\frac{\pi}{4}$ |
| 15 | 解答题 | 结论成立 |
| 16 | 解答题 | (1) $a\sqrt{1+r+r^2}$；(2) $\displaystyle \frac{a}{\sqrt{1-r}}$ |
| 17 | 解答题 | $y''-y=\sin x$；$y=e^x-e^{-x}-\dfrac{1}{2}\sin x$ |
| 18 | 解答题 | $F(t)$ 在 $(0,+\infty)$ 内严格单调增加；且 $F(t)>\dfrac{2}{\pi}G(t)$ |
| 19 | 解答题 | 特征值为 $9,9,3$；$\lambda=9$ 的特征向量为 $k_1(1,-1,0)^T+k_2(-1,-1,1)^T$；$\lambda=3$ 的特征向量为 $k(0,1,1)^T$ |
| 20 | 解答题 | 三直线交于一点的充分必要条件为 $a+b+c=0$ |
| 21 | 解答题 | (1) $E(X)=\dfrac{3}{2}$；(2) 概率为 $\dfrac{1}{4}$ |
| 22 | 解答题 | $F(x)=0\ (x\le\theta),\ F(x)=1-e^{-2(x-\theta)}\ (x>\theta)$；$\hat\theta$ 非无偏 |

## 详细解析

### 第 1 题
- 答案：$\dfrac{1}{\sqrt{e}}$

设原式为 $L$。取对数，有
$$
\ln L=\lim_{x\to0}\frac{\ln(\cos x)}{\ln(1+x^2)}.
$$

当 $x\to0$ 时，
$$
\ln(\cos x)\sim \cos x-1\sim -\frac{x^2}{2},
\qquad
\ln(1+x^2)\sim x^2.
$$

所以
$$
\ln L=-\frac{1}{2}.
$$

因此
$$
L=e^{-1/2}=\frac{1}{\sqrt{e}}.
$$

### 第 2 题
- 答案：$2x+4y-z=5$

已知平面 $2x+4y-z=0$ 的法向量为
$$
\boldsymbol n=(2,4,-1).
$$

曲面
$$
z=x^2+y^2
$$
在点 $(x_0,y_0,z_0)$ 处的法向量可取为
$$
(2x_0,2y_0,-1).
$$

切平面与已知平面平行，所以
$$
(2x_0,2y_0,-1)=(2,4,-1),
$$
得
$$
x_0=1,\qquad y_0=2,\qquad z_0=1^2+2^2=5.
$$

故切平面为
$$
2(x-1)+4(y-2)-(z-5)=0,
$$
即
$$
2x+4y-z=5.
$$

### 第 3 题
- 答案：$1$

函数 $x^2$ 为偶函数，其余弦级数中
$$
a_n=\frac{2}{\pi}\int_0^\pi x^2\cos nx\,dx
\qquad(n\ge1).
$$

因此
$$
a_2=\frac{2}{\pi}\int_0^\pi x^2\cos2x\,dx.
$$

分部积分：
$$
\int_0^\pi x^2\cos2x\,dx
=\left.\frac{x^2\sin2x}{2}\right|_0^\pi
-\int_0^\pi x\sin2x\,dx.
$$

继续分部积分得
$$
\int_0^\pi x\sin2x\,dx
=\left.-\frac{x\cos2x}{2}\right|_0^\pi
+\int_0^\pi\frac{\cos2x}{2}\,dx
=-\frac{\pi}{2}.
$$

所以
$$
\int_0^\pi x^2\cos2x\,dx=\frac{\pi}{2},
$$
从而
$$
a_2=\frac{2}{\pi}\cdot\frac{\pi}{2}=1.
$$

### 第 4 题
- 答案：$\begin{pmatrix}2&3\\-1&-2\end{pmatrix}$

从基 $\alpha_1,\alpha_2$ 到基 $\beta_1,\beta_2$ 的过渡矩阵 $P$ 满足
$$
[\beta_1,\beta_2]=[\alpha_1,\alpha_2]P.
$$

其中
$$
[\alpha_1,\alpha_2]=
\begin{pmatrix}
1&1\\
0&-1
\end{pmatrix},
\qquad
[\beta_1,\beta_2]=
\begin{pmatrix}
1&1\\
1&2
\end{pmatrix}.
$$

所以
$$
P=[\alpha_1,\alpha_2]^{-1}[\beta_1,\beta_2]
=
\begin{pmatrix}
1&1\\
0&-1
\end{pmatrix}^{-1}
\begin{pmatrix}
1&1\\
1&2
\end{pmatrix}
=
\begin{pmatrix}
2&3\\
-1&-2
\end{pmatrix}.
$$

### 第 5 题
- 答案：$\dfrac{1}{4}$

事件 $X+Y\le1$ 与密度支撑
$$
0\le x\le y\le1
$$
共同限制下，有
$$
0\le x\le\frac{1}{2},\qquad x\le y\le1-x.
$$

因此
$$
P\{X+Y\le1\}
=\int_0^{1/2}\int_x^{1-x}6x\,dy\,dx.
$$

计算得
$$
\int_0^{1/2}6x(1-2x)\,dx
=\left(3x^2-4x^3\right)\bigg|_0^{1/2}
=\frac{3}{4}-\frac{1}{2}
=\frac{1}{4}.
$$

### 第 6 题
- 答案：$(39.51,\ 40.49)$

总体 $X\sim N(\mu,1)$，样本量 $n=16$，样本均值 $\bar X=40$。

方差已知时，均值 $\mu$ 的 $1-\alpha=0.95$ 置信区间为
$$
\left(\bar x-u_{\alpha/2}\frac{\sigma}{\sqrt{n}},
\bar x+u_{\alpha/2}\frac{\sigma}{\sqrt{n}}\right).
$$

由题给 $\Phi(1.96)=0.975$，得
$$
u_{\alpha/2}=1.96.
$$

代入 $\sigma=1,\ n=16,\ \bar x=40$：
$$
40\pm 1.96\cdot\frac{1}{4}
=40\pm0.49.
$$

所以置信区间为
$$
(39.51,\ 40.49).
$$

### 第 7 题
- 答案：C

由 $f'(x)$ 的图像判断 $f(x)$ 的极值点：一阶导数由正变负时为极大值点，由负变正时为极小值点。

图中 $f'(x)$ 与 $x$ 轴有三个交点。按从左到右看，第一个交点处 $f'$ 由正变负，为极大值点；第二、第三个交点处 $f'$ 均由负变正，为极小值点。

另外，$x=0$ 处导函数不存在；从图像看，左侧 $f'(x)>0$，右侧 $f'(x)<0$，所以 $x=0$ 也是极大值点。

因此 $f(x)$ 有两个极小值点和两个极大值点，选 C。

### 第 8 题
- 答案：D

因为
$$
\lim_{n\to\infty}b_n=1,\qquad
\lim_{n\to\infty}c_n=\infty.
$$

若 $\lim b_nc_n$ 存在且为有限数 $A$，则
$$
c_n=\frac{b_nc_n}{b_n}\to A,
$$
这与 $c_n\to\infty$ 矛盾。

若从广义极限看，$b_nc_n\to\infty$，也不是有限极限。因此题中“极限不存在”应选 D。

其余选项可由反例排除。例如 $a_n=1/n,\ c_n=n-2$ 时，$a_nc_n\to1$，所以 C 不成立。

### 第 9 题
- 答案：A

由题设
$$
\frac{f(x,y)-xy}{(x^2+y^2)^2}\to1
$$
可写成
$$
f(x,y)=xy+\bigl(1+o(1)\bigr)(x^2+y^2)^2.
$$

又 $f$ 在 $(0,0)$ 连续，故 $f(0,0)=0$。

沿直线 $y=x$，当 $x\ne0$ 且充分小时，
$$
f(x,x)=x^2+\bigl(1+o(1)\bigr)4x^4>0.
$$

沿直线 $y=-x$，当 $x\ne0$ 且充分小时，
$$
f(x,-x)=-x^2+\bigl(1+o(1)\bigr)4x^4<0.
$$

在 $(0,0)$ 的任意小邻域内，函数值既有正也有负，而 $f(0,0)=0$，故 $(0,0)$ 不是极值点。选 A。

### 第 10 题
- 答案：D

若向量组 I 可由向量组 II 线性表示，则
$$
\operatorname{rank}(\text{I})\le \operatorname{rank}(\text{II})\le s.
$$

若 $r>s$ 且向量组 I 线性无关，则
$$
\operatorname{rank}(\text{I})=r>s,
$$
与上式矛盾。

所以当 $r>s$ 时，向量组 I 必线性相关。选 D。

### 第 11 题
- 答案：B

设齐次方程组 $A\boldsymbol x=0$ 的解空间为 $N(A)$。

若 $A\boldsymbol x=0$ 的解均是 $B\boldsymbol x=0$ 的解，即
$$
N(A)\subseteq N(B),
$$
则
$$
\dim N(A)\le \dim N(B).
$$

由秩-零度定理
$$
\dim N(A)=n-r(A),\qquad \dim N(B)=n-r(B),
$$
所以
$$
r(A)\ge r(B).
$$
故命题 ① 正确。

若两个方程组同解，则 $N(A)=N(B)$，从而零度相同，秩也相同，故命题 ③ 正确。

命题 ②、④ 均不成立，因为秩的大小或相等不能唯一决定解空间本身。例如
$$
A=\begin{pmatrix}1&0\\0&0\end{pmatrix},
\qquad
B=\begin{pmatrix}0&0\\0&1\end{pmatrix}
$$
秩相同，但解空间不同。

因此正确的是 ①③，选 B。

### 第 12 题
- 答案：C

若 $X\sim t(n)$，则可表示为
$$
X=\frac{U}{\sqrt{V/n}},
$$
其中
$$
U\sim N(0,1),\qquad V\sim\chi^2(n),
$$
且 $U,V$ 相互独立。

于是
$$
Y=\frac{1}{X^2}
=\frac{V/n}{U^2}.
$$

又 $U^2\sim\chi^2(1)$，因此
$$
Y=\frac{V/n}{U^2/1}\sim F(n,1).
$$

故选 C。

### 第 13 题
- 答案：$A=\dfrac{e}{2}-1$；$\displaystyle V=\dfrac{\pi}{6}(5e^2-12e+3)$

设切点为 $(x_0,\ln x_0)$。曲线 $y=\ln x$ 在该点的切线为
$$
y=\ln x_0+\frac{1}{x_0}(x-x_0).
$$

切线过原点，代入 $(0,0)$ 得
$$
\ln x_0-1=0,
$$
故 $x_0=e$，切线为
$$
y=\frac{x}{e}.
$$

用 $y$ 作积分变量。区域 $D$ 可写成
$$
0\le y\le1,\qquad ey\le x\le e^y.
$$

因此面积
$$
A=\int_0^1(e^y-ey)\,dy
=e-1-\frac{e}{2}
=\frac{e}{2}-1.
$$

绕直线 $x=e$ 旋转时，外半径为 $e-ey$，内半径为 $e-e^y$，故体积
$$
V=\pi\int_0^1\left[(e-ey)^2-(e-e^y)^2\right]dy.
$$

计算得
$$
V=\frac{\pi}{6}(5e^2-12e+3).
$$

### 第 14 题
- 答案：$\displaystyle \arctan\frac{1-2x}{1+2x}=\frac{\pi}{4}-2\sum_{n=0}^{\infty}\frac{(-1)^n4^n}{2n+1}x^{2n+1}$；$\displaystyle \sum_{n=0}^{\infty}\frac{(-1)^n}{2n+1}=\frac{\pi}{4}$

设
$$
f(x)=\arctan\frac{1-2x}{1+2x}.
$$

先求导：
$$
f'(x)
=\frac{\left(\frac{1-2x}{1+2x}\right)'}
{1+\left(\frac{1-2x}{1+2x}\right)^2}
=-\frac{2}{1+4x^2}.
$$

当 $|x|<\frac{1}{2}$ 时，
$$
\frac{1}{1+4x^2}
=\sum_{n=0}^{\infty}(-1)^n4^n x^{2n}.
$$

所以
$$
f'(x)=-2\sum_{n=0}^{\infty}(-1)^n4^n x^{2n}.
$$

逐项积分，并用
$$
f(0)=\arctan1=\frac{\pi}{4},
$$
得
$$
f(x)=\frac{\pi}{4}
-2\sum_{n=0}^{\infty}\frac{(-1)^n4^n}{2n+1}x^{2n+1}.
$$

在 $x=\frac{1}{2}$ 处，左边
$$
f\left(\frac{1}{2}\right)=\arctan0=0,
$$
而级数在该端点收敛，故代入 $x=\frac{1}{2}$：
$$
0=\frac{\pi}{4}-\sum_{n=0}^{\infty}\frac{(-1)^n}{2n+1}.
$$

因此
$$
\sum_{n=0}^{\infty}\frac{(-1)^n}{2n+1}=\frac{\pi}{4}.
$$

### 第 15 题
- 答案：结论成立

(1) 对
$$
\oint_L xe^{\sin y}\,dy-ye^{-\sin x}\,dx
$$
用格林公式，取
$$
P=-ye^{-\sin x},\qquad Q=xe^{\sin y}.
$$

则
$$
\frac{\partial Q}{\partial x}=e^{\sin y},
\qquad
\frac{\partial P}{\partial y}=-e^{-\sin x}.
$$

所以
$$
\oint_L xe^{\sin y}\,dy-ye^{-\sin x}\,dx
=\iint_D\left(e^{\sin y}+e^{-\sin x}\right)dxdy.
$$

同理
$$
\oint_L xe^{-\sin y}\,dy-ye^{\sin x}\,dx
=\iint_D\left(e^{-\sin y}+e^{\sin x}\right)dxdy.
$$

区域 $D=[0,\pi]\times[0,\pi]$ 关于 $x,y$ 对称，交换 $x,y$ 可知两二重积分相等，故 (1) 成立。

(2) 由 (1) 中结果，
$$
\oint_L xe^{\sin y}\,dy-ye^{-\sin x}\,dx
=\iint_D\left(e^{\sin y}+e^{-\sin x}\right)dxdy.
$$

利用对称性可写成
$$
\iint_D\left(e^{\sin x}+e^{-\sin x}\right)dxdy.
$$

对任意实数 $u$，
$$
e^u+e^{-u}\ge2.
$$

因此
$$
\oint_L xe^{\sin y}\,dy-ye^{-\sin x}\,dx
\ge \iint_D2\,dxdy
=2\pi^2.
$$

### 第 16 题
- 答案：(1) $a\sqrt{1+r+r^2}$；(2) $\displaystyle \frac{a}{\sqrt{1-r}}$

设第 $n$ 次击打后桩进入地下深度为 $x_n$，第 $n$ 次击打所作功为 $W_n$。土层阻力为 $kx$，故从深度 $u$ 到 $v$ 所作功为
$$
\int_u^v kx\,dx=\frac{k}{2}(v^2-u^2).
$$

第一次击打后 $x_1=a$，所以
$$
W_1=\int_0^a kx\,dx=\frac{k}{2}a^2.
$$

又题设
$$
W_2=rW_1,\qquad W_3=r^2W_1.
$$

前三次总功为
$$
W_1+W_2+W_3=(1+r+r^2)\frac{k}{2}a^2.
$$

这等于从 $0$ 打到 $x_3$ 的总功：
$$
\frac{k}{2}x_3^2=(1+r+r^2)\frac{k}{2}a^2.
$$

故
$$
x_3=a\sqrt{1+r+r^2}.
$$

若击打 $n$ 次，
$$
\frac{k}{2}x_n^2=(1+r+\cdots+r^{n-1})\frac{k}{2}a^2,
$$
所以
$$
x_n=a\sqrt{\frac{1-r^n}{1-r}}.
$$

令 $n\to\infty$，因 $0<r<1$，
$$
\lim_{n\to\infty}x_n=\frac{a}{\sqrt{1-r}}.
$$

### 第 17 题
- 答案：$y''-y=\sin x$；$y=e^x-e^{-x}-\dfrac{1}{2}\sin x$

反函数求导关系为
$$
\frac{dx}{dy}=\frac{1}{y'},
\qquad
\frac{d^2x}{dy^2}
=\frac{d}{dy}\left(\frac{1}{y'}\right)
=\frac{d}{dx}\left(\frac{1}{y'}\right)\frac{dx}{dy}
=-\frac{y''}{(y')^3}.
$$

代入原方程
$$
\frac{d^2x}{dy^2}+(y+\sin x)\left(\frac{dx}{dy}\right)^3=0
$$
得
$$
-\frac{y''}{(y')^3}+\frac{y+\sin x}{(y')^3}=0.
$$

由于 $y'\ne0$，故
$$
y''-y=\sin x.
$$

求该方程满足
$$
y(0)=0,\qquad y'(0)=\frac{3}{2}
$$
的解。齐次方程 $y''-y=0$ 的通解为
$$
C_1e^x+C_2e^{-x}.
$$

设特解为 $A\cos x+B\sin x$，代入得
$$
-2A\cos x-2B\sin x=\sin x,
$$
故
$$
A=0,\qquad B=-\frac{1}{2}.
$$

所以
$$
y=C_1e^x+C_2e^{-x}-\frac{1}{2}\sin x.
$$

由初始条件得
$$
C_1=1,\qquad C_2=-1.
$$

故
$$
y=e^x-e^{-x}-\frac{1}{2}\sin x.
$$

并且
$$
y'=e^x+e^{-x}-\frac{1}{2}\cos x>0,
$$
满足题设 $y'\ne0$。

### 第 18 题
- 答案：$F(t)$ 在 $(0,+\infty)$ 内严格单调增加；且 $F(t)>\dfrac{2}{\pi}G(t)$

先化简 $F(t),G(t)$。在球坐标与极坐标下，
$$
\iiint_{\Omega(t)}f(x^2+y^2+z^2)\,dv
=4\pi\int_0^t f(r^2)r^2\,dr,
$$
$$
\iint_{D(t)}f(x^2+y^2)\,d\sigma
=2\pi\int_0^t f(r^2)r\,dr.
$$

因此
$$
F(t)=
\frac{2\int_0^t f(r^2)r^2\,dr}
{\int_0^t f(r^2)r\,dr}.
$$

对 $F(t)$ 求导并整理：
$$
F'(t)=
\frac{2tf(t^2)\int_0^t f(r^2)r(t-r)\,dr}
{\left[\int_0^t f(r^2)r\,dr\right]^2}.
$$

因 $t>0,\ f>0,\ 0<r<t$ 时 $r(t-r)>0$，故
$$
F'(t)>0.
$$
所以 $F(t)$ 在 $(0,+\infty)$ 内严格单调增加。

再证不等式。因为
$$
\int_{-t}^{t}f(x^2)\,dx=2\int_0^t f(r^2)\,dr,
$$
所以
$$
G(t)=
\frac{2\pi\int_0^t f(r^2)r\,dr}
{2\int_0^t f(r^2)\,dr}
=
\frac{\pi\int_0^t f(r^2)r\,dr}
{\int_0^t f(r^2)\,dr}.
$$

令
$$
A(t)=\int_0^t f(r^2)r^2\,dr,\quad
B(t)=\int_0^t f(r^2)r\,dr,\quad
C(t)=\int_0^t f(r^2)\,dr.
$$

则
$$
F(t)-\frac{2}{\pi}G(t)
=\frac{2A(t)}{B(t)}-\frac{2B(t)}{C(t)}
=\frac{2(A(t)C(t)-B^2(t))}{B(t)C(t)}.
$$

只需证 $A(t)C(t)-B^2(t)>0$。设
$$
H(t)=A(t)C(t)-B^2(t).
$$

则 $H(0)=0$，且
$$
H'(t)=f(t^2)\int_0^t f(r^2)(t-r)^2\,dr>0
\qquad(t>0).
$$

故 $H(t)>0$，从而
$$
F(t)>\frac{2}{\pi}G(t).
$$

### 第 19 题
- 答案：特征值为 $9,9,3$；$\lambda=9$ 的特征向量为 $k_1(1,-1,0)^T+k_2(-1,-1,1)^T$；$\lambda=3$ 的特征向量为 $k(0,1,1)^T$

由计算或利用伴随矩阵性质可得
$$
A^*=
\begin{pmatrix}
5&-2&-2\\
-2&5&-2\\
-2&-2&5
\end{pmatrix},
\qquad
P^{-1}=
\begin{pmatrix}
0&1&-1\\
1&0&0\\
0&0&1
\end{pmatrix}.
$$

于是
$$
B=P^{-1}A^*P
=
\begin{pmatrix}
7&0&0\\
-2&5&-4\\
-2&-2&3
\end{pmatrix}.
$$

所以
$$
B+2E=
\begin{pmatrix}
9&0&0\\
-2&7&-4\\
-2&-2&5
\end{pmatrix}.
$$

其特征多项式为
$$
\det(\lambda E-(B+2E))=(\lambda-9)^2(\lambda-3).
$$

故特征值为
$$
\lambda_1=\lambda_2=9,\qquad \lambda_3=3.
$$

当 $\lambda=9$ 时，解
$$
(9E-(B+2E))x=0
$$
得一组基础特征向量
$$
(1,-1,0)^T,\qquad (-1,-1,1)^T.
$$

因此 $\lambda=9$ 的全部特征向量为
$$
k_1(1,-1,0)^T+k_2(-1,-1,1)^T,
$$
其中 $k_1,k_2$ 不全为 $0$。

当 $\lambda=3$ 时，解
$$
(3E-(B+2E))x=0
$$
得特征向量
$$
(0,1,1)^T.
$$

因此 $\lambda=3$ 的全部特征向量为
$$
k(0,1,1)^T,\qquad k\ne0.
$$

### 第 20 题
- 答案：三直线交于一点的充分必要条件为 $a+b+c=0$

三条直线交于一点，等价于线性方程组
$$
\begin{cases}
ax+2by=-3c,\\
bx+2cy=-3a,\\
cx+2ay=-3b
\end{cases}
$$
有唯一解，即系数矩阵与增广矩阵的秩均为 $2$。

先证必要性。若三直线交于一点，则增广矩阵
$$
\bar A=
\begin{pmatrix}
a&2b&-3c\\
b&2c&-3a\\
c&2a&-3b
\end{pmatrix}
$$
的秩小于 $3$，故 $\det(\bar A)=0$。

直接计算可得
$$
\det(\bar A)
=3(a+b+c)\left[(a-b)^2+(b-c)^2+(c-a)^2\right].
$$

由于三条直线互不相同，不能有 $a=b=c$；因此
$$
(a-b)^2+(b-c)^2+(c-a)^2\ne0.
$$

于是
$$
a+b+c=0.
$$

再证充分性。若 $a+b+c=0$，则上式给出 $\det(\bar A)=0$，故增广矩阵秩小于 $3$。

又由 $c=-(a+b)$，
$$
\begin{vmatrix}
a&2b\\
b&2c
\end{vmatrix}
=2(ac-b^2)
=-\left(a^2+b^2+(a+b)^2\right).
$$

在题设三条不同直线下，该二阶子式不为 $0$，故系数矩阵秩为 $2$。于是系数矩阵和增广矩阵秩均为 $2$，方程组有唯一解。

所以三条直线交于一点。

### 第 21 题
- 答案：(1) $E(X)=\dfrac{3}{2}$；(2) 概率为 $\dfrac{1}{4}$

从甲箱中取出 $3$ 件放入乙箱。令 $X$ 为乙箱中次品件数，也就是从甲箱抽出的次品件数。

甲箱中有 $3$ 件合格品、$3$ 件次品，共 $6$ 件。故
$$
P\{X=k\}
=\frac{\binom{3}{k}\binom{3}{3-k}}{\binom{6}{3}},
\qquad k=0,1,2,3.
$$

于是分布为
$$
\begin{array}{c|cccc}
X&0&1&2&3\\
\hline
P&\frac{1}{20}&\frac{9}{20}&\frac{9}{20}&\frac{1}{20}
\end{array}
$$

所以
$$
E(X)=0\cdot\frac{1}{20}
+1\cdot\frac{9}{20}
+2\cdot\frac{9}{20}
+3\cdot\frac{1}{20}
=\frac{3}{2}.
$$

从甲箱放入乙箱后，乙箱共有 $6$ 件产品，其中次品件数为 $X$。任取一件为次品的条件概率为 $X/6$，故全概率为
$$
E\left(\frac{X}{6}\right)
=\frac{1}{6}E(X)
=\frac{1}{6}\cdot\frac{3}{2}
=\frac{1}{4}.
$$

### 第 22 题
- 答案：$F(x)=0\ (x\le\theta),\ F(x)=1-e^{-2(x-\theta)}\ (x>\theta)$；$\hat\theta$ 非无偏

(1) 由密度函数
$$
f(x)=2e^{-2(x-\theta)},\qquad x>\theta,
$$
得总体分布函数
$$
F(x)=
\begin{cases}
0,&x\le\theta,\\
1-e^{-2(x-\theta)},&x>\theta.
\end{cases}
$$

(2) 统计量
$$
\hat\theta=\min\{X_1,\ldots,X_n\}.
$$

当 $x\le\theta$ 时，显然
$$
F_{\hat\theta}(x)=0.
$$

当 $x>\theta$ 时，
$$
F_{\hat\theta}(x)
=P\{\hat\theta\le x\}
=1-P\{X_1>x,\ldots,X_n>x\}.
$$

由于样本独立同分布，
$$
F_{\hat\theta}(x)
=1-[1-F(x)]^n
=1-e^{-2n(x-\theta)}.
$$

故
$$
F_{\hat\theta}(x)=
\begin{cases}
0,&x\le\theta,\\
1-e^{-2n(x-\theta)},&x>\theta.
\end{cases}
$$

(3) 对上式求导，得 $\hat\theta$ 的密度
$$
f_{\hat\theta}(x)=
\begin{cases}
0,&x\le\theta,\\
2n e^{-2n(x-\theta)},&x>\theta.
\end{cases}
$$

于是
$$
E(\hat\theta)
=\int_\theta^{+\infty}2nx e^{-2n(x-\theta)}\,dx.
$$

令 $u=x-\theta$，得
$$
E(\hat\theta)
=\theta+\int_0^{+\infty}2n u e^{-2nu}\,du
=\theta+\frac{1}{2n}.
$$

因为
$$
E(\hat\theta)\ne\theta,
$$
所以 $\hat\theta$ 作为 $\theta$ 的估计量不具有无偏性。
