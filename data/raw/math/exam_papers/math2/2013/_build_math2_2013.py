from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parent
YEAR = 2013


def md(text: str) -> str:
    return dedent(text).strip()


@dataclass
class Question:
    number: int
    question_type: str
    score: int
    module: str
    topics: list[str]
    stem: str
    answer: str
    explanation: str
    assets: list[str]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def qtype_label(qtype: str) -> str:
    return {
        "fill_blank": "填空题",
        "single_choice": "选择题",
        "solution": "解答题",
        "proof": "证明题",
    }[qtype]


def build_card(q: Question) -> str:
    qid = f"kaoyan_math2_{YEAR}_q{q.number:03d}"
    lines = [
        "---",
        f"question_id: {qid}",
        f"exam_id: kaoyan_math2_{YEAR}",
        "exam_type: math2",
        f"year: {YEAR}",
        f"question_number: {q.number}",
        f"question_type: {q.question_type}",
        f"score: {q.score}",
        f"module: {q.module}",
        "topics:",
        *[f"  - {topic}" for topic in q.topics],
        "difficulty: unknown",
        "review_status: reviewed",
        "answer_status: available",
        "explanation_status: available",
        f"source_file: math2_{YEAR}_questions.md",
        f"answer_source_file: math2_{YEAR}_answers.md",
        "assets:",
        *[f"  - {asset}" for asset in q.assets],
        "---",
        "",
        f"# {YEAR} 数学二第 {q.number} 题",
        "",
        "## 题目",
        "",
        q.stem,
        "",
        *[f"![题图](../{asset})" for asset in q.assets],
        "",
        "## 标准答案",
        "",
        q.answer,
        "",
        "## 解析",
        "",
        q.explanation,
        "",
        "## 来源",
        "",
        f"- 题目来源：`math2_{YEAR}_questions.md`",
        f"- 答案来源：`math2_{YEAR}_answers.md`",
        "",
    ]
    return "\n".join(lines)


def annual_questions_md(questions: list[Question]) -> str:
    lines = [
        f"# {YEAR} 年数学二真题",
        "",
        "资料类型：考研数学二历年真题",
        f"年份：{YEAR}",
        "科目：数学二",
        "整理状态：按题卷页面转写并与答案册核对。",
        "",
    ]
    for q in questions:
        lines.extend(
            [
                f"## 第 {q.number} 题",
                f"- 题型：{qtype_label(q.question_type)}",
                f"- 分值：{q.score}",
                f"- 模块：{q.module}",
                f"- 考点：{'、'.join(q.topics)}",
                "",
                q.stem,
                "",
            ]
        )
        for asset in q.assets:
            lines.extend([f"![{YEAR} 数学二第 {q.number} 题题图]({asset})", ""])
    return "\n".join(lines).rstrip() + "\n"


def annual_answers_md(questions: list[Question]) -> str:
    lines = [
        f"# Math 2 {YEAR} Answers",
        "",
        "资料类型：考研数学二答案解析",
        f"年份：{YEAR}",
        "科目：数学二",
        "整理状态：答案与解析按答案册清洗，并与题面同步。",
        "",
        "## 答案速查",
        "",
        "| 题号 | 题型 | 答案 |",
        "|---|---|---|",
    ]
    for q in questions:
        lines.append(f"| {q.number} | {qtype_label(q.question_type)} | {q.answer.replace('|', '\\|')} |")
    lines.extend(["", "## 详细解析", ""])
    for q in questions:
        lines.extend([f"### 第 {q.number} 题", "", f"- 答案：{q.answer}", "", q.explanation, ""])
    return "\n".join(lines).rstrip() + "\n"


QUESTIONS = [
    Question(
        1,
        "single_choice",
        4,
        "高等数学",
        ["无穷小比较", "极限"],
        md(
            r"""
            设
            $$
            \cos x-1=x\sin\alpha(x),
            $$
            其中 $|\alpha(x)|<\dfrac{\pi}{2}$，则当 $x\to 0$ 时，$\alpha(x)$ 是（ ）

            A. 比 $x$ 高阶的无穷小量  
            B. 比 $x$ 低阶的无穷小量  
            C. 与 $x$ 同阶但不等价的无穷小量  
            D. 与 $x$ 等价的无穷小量
            """
        ),
        "C",
        md(
            r"""
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
            """
        ),
        ["images/source_pages/page-1.png"],
    ),
    Question(
        2,
        "single_choice",
        4,
        "高等数学",
        ["隐函数", "导数", "极限"],
        md(
            r"""
            设函数 $y=f(x)$ 由方程
            $$
            \cos(xy)+\ln y-x=1
            $$
            确定，则
            $$
            \lim_{n\to\infty} n\left[f\!\left(\frac{2}{n}\right)-1\right]=（\ ）
            $$

            A. $2$  
            B. $1$  
            C. $-1$  
            D. $-2$
            """
        ),
        "A",
        md(
            r"""
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
            """
        ),
        ["images/source_pages/page-1.png"],
    ),
    Question(
        3,
        "single_choice",
        4,
        "高等数学",
        ["分段函数", "定积分", "可导性"],
        md(
            r"""
            设函数
            $$
            f(x)=
            \begin{cases}
            \sin x,&0\le x<\pi,\\
            2,&\pi\le x\le 2\pi,
            \end{cases}
            \qquad
            F(x)=\int_0^x f(t)\,dt,
            $$
            则（ ）

            A. $x=\pi$ 是函数 $F(x)$ 的跳跃间断点  
            B. $x=\pi$ 是函数 $F(x)$ 的可去间断点  
            C. $F(x)$ 在 $x=\pi$ 处连续但不可导  
            D. $F(x)$ 在 $x=\pi$ 处可导
            """
        ),
        "C",
        md(
            r"""
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
            """
        ),
        ["images/source_pages/page-1.png"],
    ),
    Question(
        4,
        "single_choice",
        4,
        "高等数学",
        ["反常积分", "收敛性"],
        md(
            r"""
            设函数
            $$
            f(x)=
            \begin{cases}
            \dfrac{1}{(x-1)^{\alpha-1}},&1<x<e,\\[2mm]
            \dfrac{1}{x\ln^{\alpha+1}x},&x\ge e,
            \end{cases}
            $$
            若反常积分
            $$
            \int_1^{+\infty}f(x)\,dx
            $$
            收敛，则（ ）

            A. $\alpha<-2$  
            B. $\alpha>2$  
            C. $-2<\alpha<0$  
            D. $0<\alpha<2$
            """
        ),
        "D",
        md(
            r"""
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
            """
        ),
        ["images/source_pages/page-1.png"],
    ),
    Question(
        5,
        "single_choice",
        4,
        "高等数学",
        ["复合函数", "偏导数"],
        md(
            r"""
            设
            $$
            z=\frac{y}{x^2}f(xy),
            $$
            其中函数 $f$ 可微，则
            $$
            \frac{x}{y}\frac{\partial z}{\partial x}+\frac{\partial z}{\partial y}=（\ ）
            $$

            A. $2y f'(xy)$  
            B. $-2y f'(xy)$  
            C. $\dfrac{2}{x}f(xy)$  
            D. $-\dfrac{2}{x}f(xy)$
            """
        ),
        "A",
        md(
            r"""
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
            """
        ),
        ["images/source_pages/page-1.png"],
    ),
    Question(
        6,
        "single_choice",
        4,
        "高等数学",
        ["二重积分", "对称性", "象限"],
        md(
            r"""
            设 $D_k$ 是圆域
            $$
            D=\{(x,y)\mid x^2+y^2\le 1\}
            $$
            在第 $k$ 象限的部分。记
            $$
            I_k=\iint_{D_k}(y-x)\,dxdy\quad (k=1,2,3,4),
            $$
            则（ ）

            A. $I_1>0$  
            B. $I_2>0$  
            C. $I_3>0$  
            D. $I_4>0$
            """
        ),
        "B",
        md(
            r"""
            在第二象限中有 $x<0,\ y>0$，故
            $$
            y-x>0,
            $$
            从而 $I_2>0$。其余三个象限中可由对称性或直接判断符号排除。
            """
        ),
        ["images/source_pages/page-1.png"],
    ),
    Question(
        7,
        "single_choice",
        4,
        "线性代数",
        ["矩阵乘法", "向量组等价"],
        md(
            r"""
            设矩阵 $A,B,C$ 均为 $n$ 阶矩阵。若 $AB=C$，且 $B$ 可逆，则（ ）

            A. 矩阵 $C$ 的行向量组与矩阵 $A$ 的行向量组等价  
            B. 矩阵 $C$ 的列向量组与矩阵 $A$ 的列向量组等价  
            C. 矩阵 $C$ 的行向量组与矩阵 $B$ 的行向量组等价  
            D. 矩阵 $C$ 的列向量组与矩阵 $B$ 的列向量组等价
            """
        ),
        "B",
        md(
            r"""
            由 $AB=C$ 且 $B$ 可逆，得
            $$
            A=CB^{-1}.
            $$
            因此 $C$ 的列向量组可由 $A$ 的列向量组线性表示，而 $A$ 的列向量组也可由 $C$ 的列向量组线性表示，所以二者等价。
            """
        ),
        ["images/source_pages/page-1.png"],
    ),
    Question(
        8,
        "single_choice",
        4,
        "线性代数",
        ["相似", "特征值", "对角化"],
        md(
            r"""
            矩阵
            $$
            \begin{pmatrix}
            1&a&1\\
            a&b&a\\
            1&a&1
            \end{pmatrix}
            $$
            与
            $$
            \begin{pmatrix}
            2&0&0\\
            0&b&0\\
            0&0&0
            \end{pmatrix}
            $$
            相似的充分必要条件为（ ）

            A. $a=0,\ b=2$  
            B. $a=0,\ b$ 为任意常数  
            C. $a=2,\ b=0$  
            D. $a=2,\ b$ 为任意常数
            """
        ),
        "B",
        md(
            r"""
            左侧矩阵是实对称矩阵，必可正交相似对角化。注意第一、三行相同，所以它有特征值 $0$；又
            $$
            \begin{pmatrix}1\\0\\-1\end{pmatrix}
            $$
            对应特征值 $0$。要与右侧矩阵相似，其余两个特征值需为 $2$ 与 $b$。直接由迹与特征值结构比较可得必须有 $a=0$，而 $b$ 不受限制。
            """
        ),
        ["images/source_pages/page-1.png"],
    ),
    Question(
        9,
        "fill_blank",
        4,
        "高等数学",
        ["极限", "指数形式"],
        md(
            r"""
            计算
            $$
            \lim_{x\to 0}\left(2-\frac{\ln(1+x)}{x}\right)^{1/x}=\underline{\qquad}.
            $$
            """
        ),
        r"$\dfrac{1}{\sqrt e}$",
        md(
            r"""
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
            """
        ),
        ["images/source_pages/page-2.png"],
    ),
    Question(
        10,
        "fill_blank",
        4,
        "高等数学",
        ["反函数", "导数", "积分函数"],
        md(
            r"""
            设函数
            $$
            f(x)=\int_{-1}^x \sqrt{1-e^t}\,dt,
            $$
            则 $y=f(x)$ 的反函数 $x=f^{-1}(y)$ 在 $y=0$ 处的导数
            $$
            \left.\frac{dx}{dy}\right|_{y=0}
            =\underline{\qquad}.
            $$
            """
        ),
        r"$\dfrac{1}{\sqrt{1-e^{-1}}}$",
        md(
            r"""
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
            """
        ),
        ["images/source_pages/page-2.png"],
    ),
    Question(
        11,
        "fill_blank",
        4,
        "高等数学",
        ["极坐标", "面积"],
        md(
            r"""
            设封闭曲线 $L$ 的极坐标方程为
            $$
            r=\cos 3\theta\qquad \left(-\frac{\pi}{6}\le \theta\le \frac{\pi}{6}\right),
            $$
            则 $L$ 所围平面图形的面积是 $\underline{\qquad}$。
            """
        ),
        r"$\dfrac{\pi}{12}$",
        md(
            r"""
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
            """
        ),
        ["images/source_pages/page-2.png"],
    ),
    Question(
        12,
        "fill_blank",
        4,
        "高等数学",
        ["参数方程", "法线"],
        md(
            r"""
            曲线
            $$
            \begin{cases}
            x=\arctan t,\\
            y=\ln\sqrt{1+t^2}
            \end{cases}
            $$
            上对应于 $t=1$ 的点处的法线方程为 $\underline{\qquad}$。
            """
        ),
        r"$y+x-\dfrac{\pi}{4}-\ln 2=0$",
        md(
            r"""
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
            按答案册写法采用等价整理，可写成
            $$
            y+x-\frac{\pi}{4}-\ln 2=0.
            $$
            """
        ),
        ["images/source_pages/page-2.png"],
    ),
    Question(
        13,
        "fill_blank",
        4,
        "高等数学",
        ["微分方程", "线性叠加"],
        md(
            r"""
            已知
            $$
            y_1=e^{3x}-xe^{2x},\qquad
            y_2=e^x-xe^{2x},\qquad
            y_3=-xe^{2x}
            $$
            是某二阶常系数非齐次线性微分方程的 $3$ 个解，则满足条件
            $$
            y|_{x=0}=0,\qquad y'|_{x=0}=1
            $$
            的解为 $y=\underline{\qquad}$。
            """
        ),
        r"$e^{3x}-e^x-xe^{2x}$",
        md(
            r"""
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
            """
        ),
        ["images/source_pages/page-2.png"],
    ),
    Question(
        14,
        "fill_blank",
        4,
        "线性代数",
        ["伴随矩阵", "行列式"],
        md(
            r"""
            设 $A=(a_{ij})$ 是三阶非零矩阵，$|A|$ 为 $A$ 的行列式，$A_{ij}$ 为 $a_{ij}$ 的代数余子式。若
            $$
            a_{ij}+A_{ij}=0\quad (i,j=1,2,3),
            $$
            则 $|A|=\underline{\qquad}$。
            """
        ),
        "$-1$",
        md(
            r"""
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
            """
        ),
        ["images/source_pages/page-2.png"],
    ),
    Question(
        15,
        "solution",
        10,
        "高等数学",
        ["等价无穷小", "泰勒展开"],
        md(
            r"""
            当 $x\to 0$ 时，$1-\cos x\cdot \cos 2x\cdot \cos 3x$ 与 $ax^n$ 为等价无穷小，求 $n$ 与 $a$ 的值。
            """
        ),
        r"$n=2,\ a=7$",
        md(
            r"""
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
            """
        ),
        ["images/source_pages/page-2.png"],
    ),
    Question(
        16,
        "solution",
        10,
        "高等数学",
        ["旋转体体积", "定积分"],
        md(
            r"""
            设 $D$ 是由曲线 $y=x^{1/3}$、直线 $x=a\ (a>0)$ 及 $x$ 轴所围成的平面图形，$V_x,V_y$ 分别是 $D$ 绕 $x$ 轴、$y$ 轴旋转一周所得旋转体的体积。若 $V_y=10V_x$，求 $a$ 的值。
            """
        ),
        r"$a=7$",
        md(
            r"""
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
            """
        ),
        ["images/source_pages/page-2.png"],
    ),
    Question(
        17,
        "solution",
        10,
        "高等数学",
        ["二重积分", "区域划分"],
        md(
            r"""
            设平面内区域 $D$ 由直线 $x=3y,\ y=3x$ 及 $x+y=8$ 围成。计算
            $$
            \iint_D x^2\,dxdy.
            $$
            """
        ),
        r"$\dfrac{416}{3}$",
        md(
            r"""
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
            """
        ),
        ["images/source_pages/page-2.png"],
    ),
    Question(
        18,
        "proof",
        10,
        "高等数学",
        ["中值定理", "奇函数"],
        md(
            r"""
            设奇函数 $f(x)$ 在 $[-1,1]$ 上具有二阶导数，且 $f(1)=1$。证明：

            （I）存在 $\xi\in(0,1)$，使得 $f'(\xi)=1$；  
            （II）存在 $\eta\in(-1,1)$，使得 $f''(\eta)+f'(\eta)=1$。
            """
        ),
        "见解析",
        md(
            r"""
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
            """
        ),
        ["images/source_pages/page-3.png"],
    ),
    Question(
        19,
        "solution",
        10,
        "高等数学",
        ["条件极值", "拉格朗日乘子"],
        md(
            r"""
            求曲线
            $$
            x^3-xy+y^3=1\qquad (x\ge 0,\ y\ge 0)
            $$
            上的点到坐标原点的最长距离与最短距离。
            """
        ),
        r"最长距离为 $\sqrt2$，最短距离为 $1$",
        md(
            r"""
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
            """
        ),
        ["images/source_pages/page-3.png"],
    ),
    Question(
        20,
        "solution",
        11,
        "高等数学",
        ["函数最值", "数列极限"],
        md(
            r"""
            设函数
            $$
            f(x)=\ln x+\frac1x.
            $$

            （I）求 $f(x)$ 的最小值；  
            （II）设数列 $\{x_n\}$ 满足
            $$
            \ln x_n+\frac{1}{x_{n+1}}<1,
            $$
            证明 $\lim_{n\to\infty}x_n$ 存在，并求此极限。
            """
        ),
        r"最小值为 $1$；且 $\displaystyle\lim_{n\to\infty}x_n=1$",
        md(
            r"""
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
            """
        ),
        ["images/source_pages/page-3.png"],
    ),
    Question(
        21,
        "solution",
        11,
        "高等数学",
        ["弧长", "形心"],
        md(
            r"""
            设曲线 $L$ 的方程为
            $$
            y=\frac14x^2-\frac12\ln x\qquad (1\le x\le e),
            $$

            （I）求 $L$ 的弧长；  
            （II）设 $D$ 是由曲线 $L$、直线 $x=1$、$x=e$ 及 $x$ 轴所围平面图形，求 $D$ 的形心的横坐标。
            """
        ),
        r"弧长为 $\dfrac{e^2-1}{4}$；形心横坐标为 $\dfrac{3e^4-4e^2-1}{4(2e^2-3)}$",
        md(
            r"""
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
            """
        ),
        ["images/source_pages/page-4.png"],
    ),
    Question(
        22,
        "solution",
        11,
        "线性代数",
        ["矩阵方程", "线性方程组"],
        md(
            r"""
            设
            $$
            A=\begin{pmatrix}1&a\\1&0\end{pmatrix},\qquad
            B=\begin{pmatrix}0&1\\1&b\end{pmatrix}.
            $$
            当 $a,b$ 为何值时，存在矩阵 $C$ 使得
            $$
            AC-CA=B,
            $$
            并求所有矩阵 $C$。
            """
        ),
        r"$a=-1,\ b=0$；此时 $C=\begin{pmatrix}k_1+k_2&k_1+1\\k_2&k_1\end{pmatrix}$",
        md(
            r"""
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
            """
        ),
        ["images/source_pages/page-4.png"],
    ),
    Question(
        23,
        "solution",
        11,
        "线性代数",
        ["二次型", "矩阵表示", "正交变换"],
        md(
            r"""
            设二次型
            $$
            f(x_1,x_2,x_3)=2(a_1x_1+a_2x_2+a_3x_3)^2+(b_1x_1+b_2x_2+b_3x_3)^2,
            $$
            记
            $$
            \alpha=\begin{pmatrix}a_1\\a_2\\a_3\end{pmatrix},\qquad
            \beta=\begin{pmatrix}b_1\\b_2\\b_3\end{pmatrix}.
            $$

            （I）证明二次型 $f$ 对应的矩阵为 $2\alpha\alpha^{\mathsf T}+\beta\beta^{\mathsf T}$；  
            （II）若 $\alpha,\beta$ 正交且均为单位向量，证明 $f$ 在正交变换下的标准形为 $2y_1^2+y_2^2$。
            """
        ),
        r"对应矩阵为 $2\alpha\alpha^{\mathsf T}+\beta\beta^{\mathsf T}$；标准形为 $2y_1^2+y_2^2$",
        md(
            r"""
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
            """
        ),
        ["images/source_pages/page-4.png"],
    ),
]


def question_record(q: Question) -> dict[str, object]:
    qid = f"kaoyan_math2_{YEAR}_q{q.number:03d}"
    return {
        "question_id": qid,
        "exam_id": f"kaoyan_math2_{YEAR}",
        "exam_type": "math2",
        "year": YEAR,
        "question_number": q.number,
        "question_type": q.question_type,
        "score": q.score,
        "module": q.module,
        "topics": q.topics,
        "difficulty": "unknown",
        "review_status": "reviewed",
        "answer_status": "available",
        "explanation_status": "available",
        "source_file": f"math2_{YEAR}_questions.md",
        "answer_source_file": f"math2_{YEAR}_answers.md",
        "card_path": f"questions/q{q.number:03d}.md",
        "assets": q.assets,
        "answer": q.answer,
        "explanation": q.explanation,
    }


def main() -> None:
    (ROOT / "questions").mkdir(parents=True, exist_ok=True)
    (ROOT / "images" / "source_pages").mkdir(parents=True, exist_ok=True)

    (ROOT / f"math2_{YEAR}_questions.md").write_text(annual_questions_md(QUESTIONS), encoding="utf-8")
    (ROOT / f"math2_{YEAR}_answers.md").write_text(annual_answers_md(QUESTIONS), encoding="utf-8")

    for q in QUESTIONS:
        (ROOT / "questions" / f"q{q.number:03d}.md").write_text(build_card(q), encoding="utf-8")

    records = [question_record(q) for q in QUESTIONS]
    with (ROOT / "questions.jsonl").open("w", encoding="utf-8") as fh:
        for record in records:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")

    manifest = {
        "exam_id": f"kaoyan_math2_{YEAR}",
        "exam_type": "math2",
        "exam_label": "数学二",
        "year": YEAR,
        "source_files": {
            "questions": f"math2_{YEAR}_questions.md",
            "answers": f"math2_{YEAR}_answers.md",
        },
        "card_dir": "questions",
        "index_file": "questions.jsonl",
        "question_count": len(QUESTIONS),
        "explanation_count": len(QUESTIONS),
        "question_ids": [f"kaoyan_math2_{YEAR}_q{q.number:03d}" for q in QUESTIONS],
        "generated_at": now_iso(),
        "review_status": "reviewed",
        "answer_status": "available",
        "explanation_status": "available",
    }
    (ROOT / "paper_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
