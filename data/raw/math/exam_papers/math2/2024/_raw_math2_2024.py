from __future__ import annotations

from textwrap import dedent


def md(text: str) -> str:
    return dedent(text).strip()


QUESTIONS = [
    {
        "number": 1,
        "question_type": "single_choice",
        "score": 5,
        "module": "高等数学",
        "topics": ["间断点", "极限", "分段函数"],
        "source_pages": [1],
        "answer_pages": [1],
        "stem": md(
            r"""
            函数
            $$
            f(x)=|x|^{\frac{1}{(1-x)(x-2)}}
            $$
            的第一类间断点的个数是

            (A) 3

            (B) 2

            (C) 1

            (D) 0
            """
        ),
        "answer": "C",
        "explanation": md(
            r"""
            无定义点为 $x=1,\ x=2$。

            对于 $x=1$，
            $$
            \lim_{x\to 1}|x|^{\frac{1}{(1-x)(x-2)}}
            =e^{\lim_{x\to 1}\frac{\ln|x|}{(1-x)(x-2)}}
            =e,
            $$
            故 $x=1$ 是可去间断点。

            对于 $x=2$，
            $$
            \lim_{x\to 2}|x|^{\frac{1}{(1-x)(x-2)}}=+\infty,
            $$
            故 $x=2$ 是第二类间断点。

            另外，$x=0$ 是分段点，且
            $$
            \lim_{x\to 0}|x|^{\frac{1}{(1-x)(x-2)}}
            =e^{\lim_{x\to 0}\frac{\ln|x|}{(1-x)(x-2)}}=+\infty,
            $$
            故 $x=0$ 也是第二类间断点。于是只有一个第一类间断点，选 $C$。
            """
        ),
    },
    {
        "number": 2,
        "question_type": "single_choice",
        "score": 5,
        "module": "高等数学",
        "topics": ["参数方程", "导数", "极限"],
        "source_pages": [1],
        "answer_pages": [1, 2],
        "stem": md(
            r"""
            已知函数 $y=f(x)$ 由参数方程
            $$
            \begin{cases}
            x=1+t^3,\\
            y=e^{t^2}
            \end{cases}
            $$
            确定，则
            $$
            \lim_{x\to+\infty}x\left[f\left(2+\frac{2}{x}\right)-f(2)\right]=
            $$

            (A) $2e$

            (B) $\dfrac{4e}{3}$

            (C) $\dfrac{2e}{3}$

            (D) $\dfrac{e}{3}$
            """
        ),
        "answer": "B",
        "explanation": md(
            r"""
            原式
            $$
            =\lim_{x\to+\infty}\frac{f\left(2+\frac{2}{x}\right)-f(2)}{\frac{2}{x}}\cdot 2
            =2f'_+(2).
            $$
            当 $x=2$ 时有 $1+t^3=2$，故 $t=1$。由参数方程求导，
            $$
            f'(x)=\frac{dy/dt}{dx/dt}=\frac{2te^{t^2}}{3t^2}=\frac{2e^{t^2}}{3t}.
            $$
            于是
            $$
            f'_+(2)=\left.\frac{2e^{t^2}}{3t}\right|_{t=1}=\frac{2e}{3},
            $$
            所以原式等于
            $$
            2f'_+(2)=\frac{4e}{3}.
            $$
            选 $B$。
            """
        ),
    },
    {
        "number": 3,
        "question_type": "single_choice",
        "score": 5,
        "module": "高等数学",
        "topics": ["积分定义函数", "奇偶性", "复合函数"],
        "source_pages": [1],
        "answer_pages": [2],
        "stem": md(
            r"""
            已知
            $$
            f(x)=\int_0^{\sin x}\sin t^3\,dt,\qquad
            g(x)=\int_0^x f(t)\,dt,
            $$
            则

            (A) $f(x)$ 为奇函数，$g(x)$ 为奇函数

            (B) $f(x)$ 为奇函数，$g(x)$ 为偶函数

            (C) $f(x)$ 为偶函数，$g(x)$ 为偶函数

            (D) $f(x)$ 为偶函数，$g(x)$ 为奇函数
            """
        ),
        "answer": "D",
        "explanation": md(
            r"""
            由变上限积分求导，
            $$
            f'(x)=\sin\bigl((\sin x)^3\bigr)\cos x.
            $$
            其中 $\sin\bigl((\sin x)^3\bigr)$ 为奇函数，$\cos x$ 为偶函数，所以 $f'(x)$ 为奇函数。
            又 $f(0)=0$，故 $f(x)$ 为偶函数。

            再看
            $$
            g(x)=\int_0^x f(t)\,dt,
            $$
            因为 $f(t)$ 为偶函数，所以 $g(x)$ 为奇函数。选 $D$。
            """
        ),
    },
    {
        "number": 4,
        "question_type": "single_choice",
        "score": 5,
        "module": "高等数学",
        "topics": ["数列", "收敛发散", "构造反例"],
        "source_pages": [1],
        "answer_pages": [2],
        "stem": md(
            r"""
            已知数列 $\{a_n\}(a_n\ne 0)$，若 $\{a_n\}$ 发散，则

            (A) $\left\{a_n+\dfrac{1}{a_n}\right\}$ 发散

            (B) $\left\{a_n-\dfrac{1}{a_n}\right\}$ 发散

            (C) $\left\{e^{a_n}+\dfrac{1}{e^{a_n}}\right\}$ 发散

            (D) $\left\{e^{a_n}-\dfrac{1}{e^{a_n}}\right\}$ 发散
            """
        ),
        "answer": "D",
        "explanation": md(
            r"""
            选项 $A$：取 $a_n=2,\frac12,2,\frac12,\dots$，则
            $$
            a_n+\frac{1}{a_n}\equiv 2+\frac12,
            $$
            收敛，故 $A$ 错。

            选项 $B$：取 $a_n=1,-1,1,-1,\dots$，则
            $$
            a_n-\frac{1}{a_n}\equiv 0,
            $$
            收敛，故 $B$ 错。

            选项 $C$：取 $a_n=\ln2,-\ln2,\ln2,-\ln2,\dots$，则
            $$
            e^{a_n}+\frac{1}{e^{a_n}}\equiv 2+\frac12,
            $$
            收敛，故 $C$ 错。

            选项 $D$：函数
            $$
            \varphi(x)=e^x-e^{-x}
            $$
            严格单调递增。若 $\{e^{a_n}-e^{-a_n}\}$ 收敛，由反函数存在可知 $\{a_n\}$ 必收敛，与题设矛盾，故 $D$ 正确。
            """
        ),
    },
    {
        "number": 5,
        "question_type": "single_choice",
        "score": 5,
        "module": "高等数学",
        "topics": ["多元函数", "可微性", "偏导数连续性"],
        "source_pages": [1],
        "answer_pages": [3],
        "stem": md(
            r"""
            已知函数
            $$
            f(x,y)=
            \begin{cases}
            (x^2+y^2)\sin\dfrac{1}{xy},&xy\ne 0,\\
            0,&xy=0,
            \end{cases}
            $$
            则在点 $(0,0)$ 处

            (A) $\dfrac{\partial f(x,y)}{\partial x}$ 连续，$f(x,y)$ 可微

            (B) $\dfrac{\partial f(x,y)}{\partial x}$ 连续，$f(x,y)$ 不可微

            (C) $\dfrac{\partial f(x,y)}{\partial x}$ 不连续，$f(x,y)$ 可微

            (D) $\dfrac{\partial f(x,y)}{\partial x}$ 不连续，$f(x,y)$ 不可微
            """
        ),
        "answer": "C",
        "explanation": md(
            r"""
            先证可微。因为
            $$
            \left|\frac{f(x,y)-f(0,0)-0\cdot x-0\cdot y}{\sqrt{x^2+y^2}}\right|
            =\frac{|(x^2+y^2)\sin\frac{1}{xy}|}{\sqrt{x^2+y^2}}
            \le \sqrt{x^2+y^2}\to 0,
            $$
            故 $f(x,y)$ 在 $(0,0)$ 处可微。

            再看偏导。对 $xy\ne0$，
            $$
            \frac{\partial f}{\partial x}
            =2x\sin\frac{1}{xy}+(x^2+y^2)\cos\frac{1}{xy}\left(-\frac{1}{x^2y}\right),
            $$
            而当 $xy=0$ 时，$\dfrac{\partial f}{\partial x}=0$。

            取沿不同路径趋于 $(0,0)$，上式中含有
            $$
            \frac{x^2+y^2}{x^2y}\cos\frac{1}{xy}
            $$
            的振荡项，其极限不存在，故 $\dfrac{\partial f}{\partial x}$ 在 $(0,0)$ 处不连续。选 $C$。
            """
        ),
    },
    {
        "number": 6,
        "question_type": "single_choice",
        "score": 5,
        "module": "高等数学",
        "topics": ["二重积分", "交换积分次序", "积分区域"],
        "source_pages": [1],
        "answer_pages": [3, 4],
        "stem": md(
            r"""
            设 $f(x,y)$ 是连续函数，则
            $$
            \int_{\pi/6}^{\pi/2}dx\int_{\sin x}^{1}f(x,y)\,dy=
            $$

            (A) $\displaystyle \int_{1/2}^{1}dy\int_{\pi/6}^{\arcsin y}f(x,y)\,dx$

            (B) $\displaystyle \int_{1/2}^{1}dy\int_{\arcsin y}^{\pi/2}f(x,y)\,dx$

            (C) $\displaystyle \int_{0}^{1/2}dy\int_{\pi/6}^{\arcsin y}f(x,y)\,dx$

            (D) $\displaystyle \int_{0}^{1/2}dy\int_{\arcsin y}^{\pi/2}f(x,y)\,dx$
            """
        ),
        "answer": "A",
        "explanation": md(
            r"""
            原积分区域为
            $$
            D=\{(x,y)\mid \pi/6\le x\le \pi/2,\ \sin x\le y\le 1\}.
            $$
            因为在区间 $\left[\pi/6,\pi/2\right]$ 上，$\sin x$ 单调递增，且
            $$
            \sin\frac{\pi}{6}=\frac12,\qquad \sin\frac{\pi}{2}=1,
            $$
            故换序后可写为
            $$
            D=\left\{(x,y)\mid \frac12\le y\le 1,\ \frac{\pi}{6}\le x\le \arcsin y\right\}.
            $$
            所以
            $$
            \int_{\pi/6}^{\pi/2}dx\int_{\sin x}^{1}f(x,y)\,dy
            =\int_{1/2}^{1}dy\int_{\pi/6}^{\arcsin y}f(x,y)\,dx.
            $$
            选 $A$。
            """
        ),
    },
    {
        "number": 7,
        "question_type": "single_choice",
        "score": 5,
        "module": "高等数学",
        "topics": ["反常积分", "比较判别法", "命题判断"],
        "source_pages": [1],
        "answer_pages": [4],
        "stem": md(
            r"""
            设非负函数 $f(x)$ 在 $[0,+\infty)$ 上连续，给定以下三个命题：

            (1) 若 $\displaystyle \int_0^{+\infty}f^2(x)\,dx$ 收敛，则 $\displaystyle \int_0^{+\infty}f(x)\,dx$ 收敛；

            (2) 若存在 $p>1$，使极限 $\displaystyle \lim_{x\to+\infty}x^pf(x)$ 存在，则 $\displaystyle \int_0^{+\infty}f(x)\,dx$ 收敛；

            (3) 若 $\displaystyle \int_0^{+\infty}f(x)\,dx$ 收敛，则存在 $p>1$，使极限 $\displaystyle \lim_{x\to+\infty}x^pf(x)$ 存在。

            其中正确的个数是

            (A) 0

            (B) 1

            (C) 2

            (D) 3
            """
        ),
        "answer": "B",
        "explanation": md(
            r"""
            (1) 不正确。取
            $$
            f(x)=\frac{1}{x+1},
            $$
            则
            $$
            \int_0^{+\infty}\frac{1}{(x+1)^2}\,dx
            $$
            收敛，但
            $$
            \int_0^{+\infty}\frac{1}{x+1}\,dx
            $$
            发散。

            (2) 正确。若 $x^pf(x)\to L$ 且 $p>1$，则 $f(x)$ 与 $\dfrac{1}{x^p}$ 可作极限比较，从而
            $$
            \int_0^{+\infty}f(x)\,dx
            $$
            收敛。

            (3) 不正确。取
            $$
            f(x)=\frac{1}{(x+1)\ln^2(x+1)},
            $$
            则 $\int_0^{+\infty}f(x)\,dx$ 收敛，但对任意 $p>1$，
            $$
            \lim_{x\to+\infty}x^pf(x)=+\infty.
            $$
            故正确命题只有一个，选 $B$。
            """
        ),
    },
    {
        "number": 8,
        "question_type": "single_choice",
        "score": 5,
        "module": "线性代数",
        "topics": ["矩阵合同", "初等矩阵", "矩阵运算"],
        "source_pages": [1],
        "answer_pages": [5],
        "stem": md(
            r"""
            设 $A$ 为 $3$ 阶矩阵，
            $$
            P=\begin{pmatrix}
            1&0&0\\
            0&1&0\\
            1&0&1
            \end{pmatrix},
            $$
            若
            $$
            P^{\mathsf T}AP^2=
            \begin{pmatrix}
            a+2c&0&c\\
            0&b&0\\
            2c&0&c
            \end{pmatrix},
            $$
            则矩阵 $A$ 为

            (A) $\begin{pmatrix}c&0&0\\0&a&0\\0&0&b\end{pmatrix}$

            (B) $\begin{pmatrix}b&0&0\\0&c&0\\0&0&a\end{pmatrix}$

            (C) $\begin{pmatrix}a&0&0\\0&b&0\\0&0&c\end{pmatrix}$

            (D) $\begin{pmatrix}c&0&0\\0&b&0\\0&0&a\end{pmatrix}$
            """
        ),
        "answer": "C",
        "explanation": md(
            r"""
            记
            $$
            B=P^{\mathsf T}AP^2=
            \begin{pmatrix}
            a+2c&0&c\\
            0&b&0\\
            2c&0&c
            \end{pmatrix}.
            $$
            因为
            $$
            P=E_{31}(1),\qquad P^{-1}=E_{31}(-1),
            $$
            所以
            $$
            A=(P^{\mathsf T})^{-1}B(P^2)^{-1}
            =\bigl[E_{31}(-1)\bigr]^{\mathsf T}BE_{31}(-1)E_{31}(-1).
            $$
            直接计算可得
            $$
            A=
            \begin{pmatrix}
            a&0&0\\
            0&b&0\\
            0&0&c
            \end{pmatrix}.
            $$
            选 $C$。
            """
        ),
    },
    {
        "number": 9,
        "question_type": "single_choice",
        "score": 5,
        "module": "线性代数",
        "topics": ["伴随矩阵", "矩阵秩", "矩阵方程"],
        "source_pages": [1],
        "answer_pages": [5, 6],
        "stem": md(
            r"""
            设 $A$ 为 $4$ 阶矩阵，$A^*$ 为 $A$ 的伴随矩阵，若 $A(A-A^*)=O$，且 $A\ne A^*$，则 $r(A)$ 的可能取值为

            (A) 0 或 1

            (B) 1 或 3

            (C) 2 或 3

            (D) 1 或 2
            """
        ),
        "answer": "D",
        "explanation": md(
            r"""
            由题意
            $$
            A(A-A^*)=O,
            $$
            故
            $$
            r(A)+r(A-A^*)\le 4.
            $$
            又因为 $A\ne A^*$，所以 $A-A^*\ne O$，从而
            $$
            r(A-A^*)\ge 1,
            $$
            于是
            $$
            r(A)\le 3.
            $$

            另一方面，
            $$
            A(A-A^*)=A^2-AA^*=A^2-|A|E=0.
            $$
            若 $r(A)=3$，则 $A^*=0$，从而 $A^2=0$，这与 $r(A)=3$ 矛盾，所以 $r(A)\ne 3$。

            因而 $r(A)\le 2$。又由 $A\ne A^*$ 可知 $A\ne O$，所以
            $$
            r(A)\ge 1.
            $$
            故 $r(A)$ 只能取 $1$ 或 $2$，选 $D$。
            """
        ),
    },
    {
        "number": 10,
        "question_type": "single_choice",
        "score": 5,
        "module": "线性代数",
        "topics": ["特征值", "可对角化", "交换矩阵"],
        "source_pages": [1],
        "answer_pages": [6, 7],
        "stem": md(
            r"""
            设 $A,B$ 均为 $2$ 阶矩阵，且 $AB=BA$，则“$A$ 有两个不相等的特征值”是“$B$ 可对角化”的

            (A) 充要条件

            (B) 充分非必要条件

            (C) 必要非充分条件

            (D) 既非充分又非必要条件
            """
        ),
        "answer": "B",
        "explanation": md(
            r"""
            充分性：若 $A$ 有两个不相等的特征值，设为 $\lambda_1,\lambda_2$，则 $A$ 可相似对角化。取可逆矩阵 $P$，使
            $$
            P^{-1}AP=
            \begin{pmatrix}
            \lambda_1&0\\
            0&\lambda_2
            \end{pmatrix},
            \qquad \lambda_1\ne\lambda_2.
            $$
            由 $AB=BA$ 得
            $$
            P^{-1}BP
            \begin{pmatrix}
            \lambda_1&0\\
            0&\lambda_2
            \end{pmatrix}
            =
            \begin{pmatrix}
            \lambda_1&0\\
            0&\lambda_2
            \end{pmatrix}
            P^{-1}BP.
            $$
            设 $P^{-1}BP=\begin{pmatrix}b_1&b_2\\ b_3&b_4\end{pmatrix}$，比较元素可得 $b_2=b_3=0$，故 $P^{-1}BP$ 为对角矩阵，于是 $B$ 可对角化。

            必要性不成立。取
            $$
            A=E,\qquad B=E,
            $$
            则 $AB=BA$ 且 $B$ 可对角化，但 $A$ 不具有两个不相等的特征值。

            因此该条件是“$B$ 可对角化”的充分非必要条件，选 $B$。
            """
        ),
    },
    {
        "number": 11,
        "question_type": "fill_blank",
        "score": 5,
        "module": "高等数学",
        "topics": ["曲率", "曲率圆", "平面曲线"],
        "source_pages": [1, 2],
        "answer_pages": [7, 8],
        "stem": md(
            r"""
            曲线 $y^2=x$ 在点 $(0,0)$ 处的曲率圆方程为 ________ 。
            """
        ),
        "answer": r"$\left(x-\dfrac12\right)^2+y^2=\dfrac14$",
        "explanation": md(
            r"""
            将曲线改写为
            $$
            x=y^2.
            $$
            在点 $(0,0)$ 处有
            $$
            x'(y)=2y,\qquad x''(y)=2.
            $$
            曲率为
            $$
            k=\frac{|x''|}{\bigl(1+(x')^2\bigr)^{3/2}}=2,
            $$
            故曲率半径
            $$
            R=\frac{1}{k}=\frac12.
            $$
            由图形可知曲率圆圆心为 $\left(\dfrac12,0\right)$，因此曲率圆方程是
            $$
            \left(x-\frac12\right)^2+y^2=\frac14.
            $$
            """
        ),
    },
    {
        "number": 12,
        "question_type": "fill_blank",
        "score": 5,
        "module": "高等数学",
        "topics": ["多元函数极值", "二阶偏导数判别法"],
        "source_pages": [1, 2],
        "answer_pages": [8],
        "stem": md(
            r"""
            函数
            $$
            f(x,y)=2x^3-9x^2-6y^4+12x+24y
            $$
            的极值点是 ________ 。
            """
        ),
        "answer": r"$(1,1)$",
        "explanation": md(
            r"""
            由
            $$
            f'_x=6x^2-18x+12=0,\qquad f'_y=-24y^3+24=0,
            $$
            得驻点为 $(1,1)$ 与 $(2,1)$。

            再算二阶偏导：
            $$
            A=f''_{xx}=12x-18,\qquad B=f''_{xy}=0,\qquad C=f''_{yy}=-72y^2.
            $$
            在 $(1,1)$ 处，
            $$
            AC-B^2=432>0,\qquad A=-6<0,
            $$
            所以 $(1,1)$ 是极大值点。

            在 $(2,1)$ 处，
            $$
            AC-B^2=-432<0,
            $$
            不是极值点。故极值点为 $(1,1)$。
            """
        ),
    },
    {
        "number": 13,
        "question_type": "fill_blank",
        "score": 5,
        "module": "高等数学",
        "topics": ["微分方程", "变量代换", "初值问题"],
        "source_pages": [2],
        "answer_pages": [8, 9],
        "stem": md(
            r"""
            微分方程
            $$
            y'=\frac{1}{(x+y)^2}
            $$
            满足初始条件 $y(1)=0$ 的解为 ________ 。
            """
        ),
        "answer": r"$\arctan(x+y)=y+\dfrac{\pi}{4}$",
        "explanation": md(
            r"""
            将方程改写为
            $$
            \frac{dx}{dy}=(x+y)^2.
            $$
            令
            $$
            u=x+y,
            $$
            则
            $$
            \frac{dx}{dy}=\frac{du}{dy}-1.
            $$
            因而
            $$
            \frac{du}{dy}=u^2+1.
            $$
            分离变量得
            $$
            \int\frac{1}{u^2+1}\,du=\int dy,
            $$
            即
            $$
            \arctan u=y+c.
            $$
            代入初值 $x=1,\ y=0$，此时 $u=1$，得
            $$
            c=\frac{\pi}{4}.
            $$
            所以解为
            $$
            \arctan(x+y)=y+\frac{\pi}{4}.
            $$
            """
        ),
    },
    {
        "number": 14,
        "question_type": "fill_blank",
        "score": 5,
        "module": "高等数学",
        "topics": ["高阶导数", "莱布尼茨公式"],
        "source_pages": [2],
        "answer_pages": [9],
        "stem": md(
            r"""
            已知函数
            $$
            f(x)=x^2(e^x+1),
            $$
            则 $f^{(5)}(1)=$ ________ 。
            """
        ),
        "answer": r"$31e$",
        "explanation": md(
            r"""
            利用莱布尼茨公式，
            $$
            \bigl((e^x+1)x^2\bigr)^{(5)}
            =(e^x+1)^{(5)}x^2+5(e^x+1)^{(4)}(x^2)'+C_5^2(e^x+1)^{(3)}(x^2)''.
            $$
            因为 $x^2$ 的三阶以上导数为 $0$，故
            $$
            f^{(5)}(x)=e^x\cdot x^2+5e^x\cdot 2x+10e^x\cdot 2.
            $$
            代入 $x=1$ 得
            $$
            f^{(5)}(1)=e+10e+20e=31e.
            $$
            """
        ),
    },
    {
        "number": 15,
        "question_type": "fill_blank",
        "score": 5,
        "module": "高等数学",
        "topics": ["定积分应用", "平均值", "运动学"],
        "source_pages": [2],
        "answer_pages": [9],
        "stem": md(
            r"""
            某物体以速度
            $$
            v(t)=t+k\sin\pi t
            $$
            作直线运动，若它从 $t=0$ 到 $t=3$ 的时间段内平均速度是 $\dfrac52$，则 $k=$ ________ 。
            """
        ),
        "answer": r"$\dfrac{3\pi}{2}$",
        "explanation": md(
            r"""
            由平均速度公式，
            $$
            \frac{1}{3}\int_0^3(t+k\sin\pi t)\,dt=\frac52.
            $$
            所以
            $$
            \int_0^3(t+k\sin\pi t)\,dt=\frac{15}{2}.
            $$
            计算得
            $$
            \int_0^3 t\,dt=\frac92,\qquad
            \int_0^3 \sin\pi t\,dt=-\frac{1}{\pi}\cos\pi t\Big|_0^3=\frac{2}{\pi}.
            $$
            因此
            $$
            \frac92+\frac{2k}{\pi}=\frac{15}{2},
            $$
            解得
            $$
            k=\frac{3\pi}{2}.
            $$
            """
        ),
    },
    {
        "number": 16,
        "question_type": "fill_blank",
        "score": 5,
        "module": "线性代数",
        "topics": ["向量组", "线性相关", "秩"],
        "source_pages": [2],
        "answer_pages": [9, 10],
        "stem": md(
            r"""
            设向量
            $$
            \alpha_1=\begin{pmatrix}a\\1\\-1\\1\end{pmatrix},\quad
            \alpha_2=\begin{pmatrix}1\\1\\b\\a\end{pmatrix},\quad
            \alpha_3=\begin{pmatrix}1\\a\\-1\\1\end{pmatrix},
            $$
            若 $\alpha_1,\alpha_2,\alpha_3$ 线性相关，且其中任意两个向量均线性无关，则
            $$
            ab=
            $$
            ________ 。
            """
        ),
        "answer": r"$-4$",
        "explanation": md(
            r"""
            记
            $$
            A=(\alpha_1,\alpha_2,\alpha_3)
            =\begin{pmatrix}
            a&1&1\\
            1&1&a\\
            -1&b&-1\\
            1&a&1
            \end{pmatrix}.
            $$
            由题意知 $r(\alpha_1,\alpha_2,\alpha_3)\le 2$，且任意两向量线性无关，所以
            $$
            r(\alpha_i,\alpha_j)=2\quad(i\ne j).
            $$

            先化简可得
            $$
            \begin{pmatrix}
            1&1&a\\
            0&1&1+a\\
            0&b+1&a-1\\
            0&0&a+2
            \end{pmatrix}.
            $$
            若 $a=1$，则 $\alpha_1$ 与 $\alpha_3$ 相关，不合题意。

            当 $a\ne1$ 时，由线性相关得
            $$
            a+2=0,\qquad -b(a+1)-2=0.
            $$
            解得
            $$
            a=-2,\qquad b=2.
            $$
            故
            $$
            ab=-4.
            $$
            """
        ),
    },
    {
        "number": 17,
        "question_type": "solution",
        "score": 10,
        "module": "高等数学",
        "topics": ["二重积分", "变量代换", "雅可比行列式"],
        "source_pages": [2],
        "answer_pages": [10, 11],
        "stem": md(
            r"""
            设平面有界区域 $D$ 位于第一象限，由曲线 $xy=\dfrac13$，$xy=3$ 与直线 $y=\dfrac13x$，$y=3x$ 围成，计算
            $$
            \iint_D(1+x-y)\,dxdy.
            $$
            """
        ),
        "answer": r"$\dfrac{8}{3}\ln 3$",
        "explanation": md(
            r"""
            令
            $$
            u=xy,\qquad v=\frac{y}{x}.
            $$
            则
            $$
            x=\sqrt{\frac{u}{v}},\qquad y=\sqrt{uv}.
            $$
            雅可比行列式为
            $$
            J=\left|\frac{\partial(x,y)}{\partial(u,v)}\right|=\frac{1}{2v}.
            $$

            由边界条件知
            $$
            \frac13\le u\le 3,\qquad \frac13\le v\le 3.
            $$
            原积分化为
            $$
            \int_{1/3}^3du\int_{1/3}^3\left(1+\sqrt{\frac{u}{v}}-\sqrt{uv}\right)\frac{1}{2v}\,dv.
            $$
            计算后得
            $$
            \iint_D(1+x-y)\,dxdy=\frac{8}{3}\ln 3.
            $$
            """
        ),
    },
    {
        "number": 18,
        "question_type": "solution",
        "score": 10,
        "module": "高等数学",
        "topics": ["欧拉方程", "变量代换", "定积分"],
        "source_pages": [2],
        "answer_pages": [11, 12],
        "stem": md(
            r"""
            设 $y=y(x)$ 为微分方程
            $$
            x^2y''+xy'-9y=0
            $$
            满足条件 $\left.y\right|_{x=1}=2$，$\left.y'\right|_{x=1}=6$ 的解。

            (1) 利用变换 $x=e^t$ 将上述方程化为常系数线性方程，并求 $y(x)$；

            (2) 计算
            $$
            \int_1^2 y(x)\sqrt{4-x^2}\,dx.
            $$
            """
        ),
        "answer": md(
            r"""
            (1) $y(x)=2x^3$

            (2) $\dfrac{22\sqrt3}{5}$
            """
        ),
        "explanation": md(
            r"""
            令 $x=e^t$，则
            $$
            \frac{dy}{dx}=\frac{dy}{dt}\frac{dt}{dx}=\frac{1}{x}\frac{dy}{dt},
            $$
            进一步可得
            $$
            x^2y''+xy'-9y=0
            \Longrightarrow
            \frac{d^2y}{dt^2}-9y=0.
            $$
            故
            $$
            y=C_1e^{3t}+C_2e^{-3t}=C_1x^3+\frac{C_2}{x^3}.
            $$
            由条件
            $$
            y(1)=C_1+C_2=2,\qquad
            y'(1)=3C_1-3C_2=6,
            $$
            解得 $C_1=2,\ C_2=0$，所以
            $$
            y(x)=2x^3.
            $$

            于是
            $$
            \int_1^2y(x)\sqrt{4-x^2}\,dx
            =\int_1^2 2x^3\sqrt{4-x^2}\,dx.
            $$
            令 $x=2\sin t$，则
            $$
            dx=2\cos t\,dt,\qquad \sqrt{4-x^2}=2\cos t,
            $$
            积分限由 $x=1,2$ 变为 $t=\pi/6,\pi/2$。因此
            $$
            \int_1^2 2x^3\sqrt{4-x^2}\,dx
            =\int_{\pi/6}^{\pi/2}16\sin^3t\cdot 4\cos^2t\,dt.
            $$
            再令 $u=\cos t$，可得
            $$
            64\int_0^{\sqrt3/2}(u^2-u^4)\,du
            =64\left(\frac{u^3}{3}-\frac{u^5}{5}\right)\Big|_0^{\sqrt3/2}
            =\frac{22\sqrt3}{5}.
            $$
            """
        ),
    },
    {
        "number": 19,
        "question_type": "solution",
        "score": 10,
        "module": "高等数学",
        "topics": ["定积分应用", "旋转体体积", "最值"],
        "source_pages": [2],
        "answer_pages": [12, 13],
        "stem": md(
            r"""
            设 $t>0$，平面有界区域 $D$ 由曲线 $y=\sqrt{x}e^{-x}$ 与直线 $x=t$，$x=2t$ 及 $x$ 轴围成，$D$ 绕 $x$ 轴旋转一周所成旋转体的体积为 $V(t)$，求 $V(t)$ 的最大值。
            """
        ),
        "answer": r"$V(t)$ 在 $t=\ln 2$ 处取最大值，且 $V_{\max}=\dfrac{\pi}{16}\ln 2+\dfrac{3\pi}{64}$",
        "explanation": md(
            r"""
            由旋转体体积公式，
            $$
            V(t)=\int_t^{2t}\pi y^2(x)\,dx
            =\int_t^{2t}\pi xe^{-2x}\,dx
            =-\frac{\pi}{4}(2x+1)e^{-2x}\Big|_t^{2t}.
            $$
            故
            $$
            V(t)=-\frac{\pi}{4}\Bigl[(4t+1)e^{-4t}-(2t+1)e^{-2t}\Bigr]\qquad (t>0).
            $$

            求导得
            $$
            V'(t)=-\frac{\pi}{4}\bigl(-16te^{-4t}+4te^{-2t}\bigr).
            $$
            令 $V'(t)=0$，得
            $$
            t=\frac12\ln4=\ln2.
            $$
            并且当 $t\in(0,\ln2)$ 时 $V'(t)>0$，当 $t>\ln2$ 时 $V'(t)<0$，故 $t=\ln2$ 处取最大值。

            代入得
            $$
            V_{\max}=V(\ln2)=\frac{\pi}{16}\ln2+\frac{3\pi}{64}.
            $$
            """
        ),
    },
    {
        "number": 20,
        "question_type": "solution",
        "score": 12,
        "module": "高等数学",
        "topics": ["二阶偏导数", "链式法则", "偏微分方程"],
        "source_pages": [2],
        "answer_pages": [13, 14],
        "stem": md(
            r"""
            已知函数 $f(u,v)$ 具有 $2$ 阶连续偏导，且函数
            $$
            g(x,y)=f(2x+y,3x-y)
            $$
            满足
            $$
            \frac{\partial^2g}{\partial x^2}
            +\frac{\partial^2g}{\partial x\partial y}
            -6\frac{\partial^2g}{\partial y^2}=1.
            $$

            (1) 求 $\dfrac{\partial^2f}{\partial u\partial v}$；

            (2) 若 $\dfrac{\partial f(u,0)}{\partial u}=ue^{-u}$，且 $f(0,v)=\dfrac{1}{50}v^2-1$，求 $f(u,v)$ 的表达式。
            """
        ),
        "answer": md(
            r"""
            (1) $\displaystyle \frac{\partial^2f}{\partial u\partial v}=\frac{1}{25}$

            (2) $\displaystyle f(u,v)=-(u+1)e^{-u}+\frac{1}{25}uv+\frac{1}{50}v^2$
            """
        ),
        "explanation": md(
            r"""
            设
            $$
            u=2x+y,\qquad v=3x-y.
            $$
            则由链式法则
            $$
            g_x=2f_u+3f_v,\qquad g_y=f_u-f_v.
            $$
            进一步有
            $$
            g_{xx}=4f_{uu}+12f_{uv}+9f_{vv},
            $$
            $$
            g_{xy}=2f_{uu}+f_{uv}-3f_{vv},
            $$
            $$
            g_{yy}=f_{uu}-2f_{uv}+f_{vv}.
            $$
            代入条件得
            $$
            g_{xx}+g_{xy}-6g_{yy}=25f_{uv}=1,
            $$
            所以
            $$
            f_{uv}=\frac{1}{25}.
            $$

            对 $v$ 积分，
            $$
            f_u=\int \frac{1}{25}\,dv=\frac{1}{25}v+c_1(u).
            $$
            由
            $$
            f_u(u,0)=ue^{-u}
            $$
            得
            $$
            c_1(u)=ue^{-u},
            $$
            因而
            $$
            f_u=ue^{-u}+\frac{1}{25}v.
            $$
            再对 $u$ 积分，
            $$
            f(u,v)=\int\left(ue^{-u}+\frac{1}{25}v\right)\,du
            =-(u+1)e^{-u}+\frac{1}{25}uv+c_2(v).
            $$
            利用
            $$
            f(0,v)=\frac{1}{50}v^2-1
            $$
            可得
            $$
            c_2(v)=\frac{1}{50}v^2.
            $$
            故
            $$
            f(u,v)=-(u+1)e^{-u}+\frac{1}{25}uv+\frac{1}{50}v^2.
            $$
            """
        ),
    },
    {
        "number": 21,
        "question_type": "proof",
        "score": 12,
        "module": "高等数学",
        "topics": ["泰勒公式", "积分不等式", "估值证明"],
        "source_pages": [2],
        "answer_pages": [14, 15],
        "stem": md(
            r"""
            设函数 $f(x)$ 具有 $2$ 阶导数，且 $f'(0)=f'(1)$，$|f''(x)|\le 1$。证明：

            (1) 当 $x\in(0,1)$ 时，
            $$
            |f(x)-f(0)(1-x)-f(1)x|\le \frac{x(1-x)}{2};
            $$

            (2)
            $$
            \left|\int_0^1f(x)\,dx-\frac{f(0)+f(1)}{2}\right|\le \frac{1}{12}.
            $$
            """
        ),
        "answer": '结论成立：（1）当 $x\\in(0,1)$ 时，$\\left\\lvert f(x)-f(0)(1-x)-f(1)x\\right\\rvert\\le \\frac{x(1-x)}{2}$；（2）$\\left\\lvert\\int_0^1f(x)\\,dx-\\frac{f(0)+f(1)}{2}\\right\\rvert\\le \\frac{1}{12}$',
        "explanation": md(
            r"""
            由带拉格朗日余项的泰勒公式，
            $$
            f(x)=f(0)+f'(0)x+\frac{f''(\xi_1)}{2}x^2,\qquad \xi_1\in(0,x),
            $$
            以及
            $$
            f(x)=f(1)+f'(1)(x-1)+\frac{f''(\xi_2)}{2}(x-1)^2,\qquad \xi_2\in(x,1).
            $$
            将第一式乘以 $(1-x)$，第二式乘以 $x$，并利用 $f'(0)=f'(1)$，相加得
            $$
            f(x)-f(0)(1-x)-f(1)x
            =\frac{f''(\xi_1)}{2}x^2(1-x)+\frac{f''(\xi_2)}{2}(x-1)^2x.
            $$
            因为 $|f''(x)|\le1$，故
            $$
            |f(x)-f(0)(1-x)-f(1)x|
            \le \frac12x^2(1-x)+\frac12x(1-x)^2
            =\frac{x(1-x)}{2}.
            $$
            这就证明了 (1)。

            对 (1) 在 $[0,1]$ 上积分，
            $$
            \left|\int_0^1\bigl[f(x)-f(0)(1-x)-f(1)x\bigr]\,dx\right|
            \le \int_0^1\frac{x(1-x)}{2}\,dx=\frac{1}{12}.
            $$
            又
            $$
            \int_0^1f(0)(1-x)\,dx+\int_0^1f(1)x\,dx=\frac{f(0)+f(1)}{2},
            $$
            所以
            $$
            \left|\int_0^1f(x)\,dx-\frac{f(0)+f(1)}{2}\right|\le\frac{1}{12}.
            $$
            """
        ),
    },
    {
        "number": 22,
        "question_type": "solution",
        "score": 12,
        "module": "线性代数",
        "topics": ["二次型", "正交变换", "特征值特征向量"],
        "source_pages": [2],
        "answer_pages": [15, 16],
        "stem": md(
            r"""
            设矩阵
            $$
            A=\begin{pmatrix}
            0&1&a\\
            1&0&1
            \end{pmatrix},\qquad
            B=\begin{pmatrix}
            1&1\\
            1&1\\
            b&2
            \end{pmatrix},
            $$
            二次型 $f(x_1,x_2,x_3)=x^{\mathsf T}BAx$。已知方程组 $Ax=0$ 的解是 $B^{\mathsf T}x=0$ 的解，但两个方程组不同解。

            (1) 求 $a,b$ 的值；

            (2) 求正交矩阵 $x=Qy$ 将 $f(x_1,x_2,x_3)$ 化为标准形。
            """
        ),
        "answer": md(
            r"""
            (1) $a=1,\ b=2$

            (2) 标准形为 $6y_3^2$
            """
        ),
        "explanation": md(
            r"""
            由题意可知，$Ax=0$ 的解均为 $B^{\mathsf T}x=0$ 的解，因此
            $$
            r(A)=r\binom{A}{B^{\mathsf T}}.
            $$
            又因为 $A$ 为 $2\times3$ 矩阵，且两个方程组不同解，所以
            $$
            r(A)=2.
            $$
            将
            $$
            \binom{A}{B^{\mathsf T}}
            =
            \begin{pmatrix}
            0&1&a\\
            1&0&1\\
            1&1&b\\
            1&1&2
            \end{pmatrix}
            $$
            作初等行变换，可化为
            $$
            \begin{pmatrix}
            1&0&1\\
            0&1&a\\
            0&0&b-a-1\\
            0&0&1-a
            \end{pmatrix}.
            $$
            由秩等于 $2$，得
            $$
            1-a=0,\qquad b-a-1=0,
            $$
            即
            $$
            a=1,\qquad b=2.
            $$

            此时
            $$
            BA=
            \begin{pmatrix}
            1&1\\
            1&1\\
            2&2
            \end{pmatrix}
            \begin{pmatrix}
            0&1&1\\
            1&0&1
            \end{pmatrix}
            =
            \begin{pmatrix}
            1&1&2\\
            1&1&2\\
            2&2&4
            \end{pmatrix}
            =C.
            $$
            所以
            $$
            f=x^{\mathsf T}Cx.
            $$
            由 $r(C)=1$，知其特征值为
            $$
            \lambda_1=\lambda_2=0,\qquad \lambda_3=\operatorname{tr}(C)=6.
            $$
            当 $\lambda=0$ 时，可取两个线性无关特征向量
            $$
            \xi_1=(1,-1,0)^{\mathsf T},\qquad \xi_2=(1,1,-1)^{\mathsf T},
            $$
            单位化得
            $$
            \eta_1=\frac{1}{\sqrt2}(1,-1,0)^{\mathsf T},\qquad
            \eta_2=\frac{1}{\sqrt3}(1,1,-1)^{\mathsf T}.
            $$
            当 $\lambda=6$ 时，可取特征向量
            $$
            \xi_3=(1,1,2)^{\mathsf T},
            $$
            单位化得
            $$
            \eta_3=\frac{1}{\sqrt6}(1,1,2)^{\mathsf T}.
            $$
            取正交矩阵
            $$
            Q=(\eta_1,\eta_2,\eta_3)
            =
            \begin{pmatrix}
            \frac{1}{\sqrt2}&\frac{1}{\sqrt3}&\frac{1}{\sqrt6}\\
            -\frac{1}{\sqrt2}&\frac{1}{\sqrt3}&\frac{1}{\sqrt6}\\
            0&-\frac{1}{\sqrt3}&\frac{2}{\sqrt6}
            \end{pmatrix},
            $$
            则在变换 $x=Qy$ 下，
            $$
            f=x^{\mathsf T}Cx=6y_3^2.
            $$
            """
        ),
    },
]
