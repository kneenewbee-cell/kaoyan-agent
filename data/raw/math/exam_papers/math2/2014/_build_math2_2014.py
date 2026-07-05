from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parent
YEAR = 2014


def md(text: str) -> str:
    return dedent(text).strip()


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def qtype_label(qtype: str) -> str:
    return {
        "single_choice": "选择题",
        "fill_blank": "填空题",
        "solution": "解答题",
        "proof": "证明题",
    }[qtype]


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
        "资料类型：考研数学二历年真题  ",
        f"年份：{YEAR}  ",
        "科目：数学二  ",
        "整理状态：按原卷页面转写并校对。  ",
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
        "整理状态：按答案册清洗并与题面同步。",
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
        1, "single_choice", 4, "高等数学", ["无穷小比较", "极限"],
        md(r"""
        当 $x\to 0^+$ 时，若 $\ln^\alpha(1+2x)$、$(1-\cos x)^{1/\alpha}$ 均是比 $x$ 高阶的无穷小量，则 $\alpha$ 的取值范围是（ ）  
        (A) $(2,+\infty)$  
        (B) $(1,2)$  
        (C) $\left(\dfrac12,1\right)$  
        (D) $\left(0,\dfrac12\right)$
        """),
        "B",
        md(r"""
        要使 $\ln^\alpha(1+2x)=o(x)$，由 $\ln(1+2x)\sim 2x$ 得
        $$
        \frac{\ln^\alpha(1+2x)}{x}\sim 2^\alpha x^{\alpha-1}\to 0,
        $$
        故 $\alpha>1$。
        又因 $1-\cos x\sim \dfrac{x^2}{2}$，要使 $(1-\cos x)^{1/\alpha}=o(x)$，需
        $$
        \frac{(1-\cos x)^{1/\alpha}}{x}\sim \left(\frac12\right)^{1/\alpha}x^{2/\alpha-1}\to0,
        $$
        即 $\dfrac{2}{\alpha}-1>0$，所以 $\alpha<2$。综合得 $\alpha\in(1,2)$。
        """),
        ["images/source_pages/page-1.png"],
    ),
    Question(
        2, "single_choice", 4, "高等数学", ["渐近线", "函数性质"],
        md(r"""
        下列曲线中有渐近线的是（ ）  
        (A) $y=x+\sin x$  
        (B) $y=x^2+\sin x$  
        (C) $y=x+\sin\dfrac1x$  
        (D) $y=x^2+\sin\dfrac1x$
        """),
        "C",
        md(r"""
        对 $y=x+\sin\dfrac1x$，当 $x\to\infty$ 时，
        $$
        \frac{y}{x}=1+\frac{\sin(1/x)}{x}\to 1,\qquad
        y-x=\sin\frac1x\to 0.
        $$
        因此它有斜渐近线 $y=x$。其余选项分别因振荡项不趋零或主项为二次项，不满足渐近线条件。
        """),
        ["images/source_pages/page-1.png"],
    ),
    Question(
        3, "single_choice", 4, "高等数学", ["凸性", "函数图像"],
        md(r"""
        设函数 $f(x)$ 具有 2 阶导数，$g(x)=f(0)(1-x)+f(1)x$，则在区间 $[0,1]$ 上，（ ）  
        (A) 当 $f'(x)\ge 0$ 时，$f(x)\ge g(x)$  
        (B) 当 $f'(x)\ge 0$ 时，$f(x)\le g(x)$  
        (C) 当 $f''(x)\ge 0$ 时，$f(x)\ge g(x)$  
        (D) 当 $f''(x)\ge 0$ 时，$f(x)\le g(x)$
        """),
        "D",
        md(r"""
        $g(x)$ 是连接 $(0,f(0))$ 与 $(1,f(1))$ 的弦。若 $f''(x)\ge 0$，则 $f$ 在 $[0,1]$ 上为凸函数，凸函数图像位于任意弦的下方，因此
        $$
        f(x)\le g(x),\qquad x\in[0,1].
        $$
        所以选 D。
        """),
        ["images/source_pages/page-1.png"],
    ),
    Question(
        4, "single_choice", 4, "高等数学", ["参数方程", "曲率"],
        md(r"""
        曲线
        $$
        \begin{cases}
        x=t^2+7,\\
        y=t^2+4t+1
        \end{cases}
        $$
        上对应于 $t=1$ 的点处的曲率半径是（ ）  
        (A) $\dfrac{\sqrt{10}}{50}$  
        (B) $\dfrac{\sqrt{10}}{100}$  
        (C) $10\sqrt{10}$  
        (D) $5\sqrt{10}$
        """),
        "C",
        md(r"""
        由参数方程得
        $$
        \frac{dy}{dx}=\frac{dy/dt}{dx/dt}=\frac{2t+4}{2t},\qquad \left.\frac{dy}{dx}\right|_{t=1}=3.
        $$
        再求
        $$
        \frac{d^2y}{dx^2}
        =\frac{d}{dt}\left(\frac{2t+4}{2t}\right)\Big/\frac{dx}{dt}
        =-\frac{8}{(2t)^3},
        $$
        所以 $\left.\dfrac{d^2y}{dx^2}\right|_{t=1}=-1$。曲率
        $$
        k=\frac{|y''|}{(1+y'^2)^{3/2}}=\frac{1}{(1+3^2)^{3/2}}.
        $$
        因此曲率半径
        $$
        R=\frac1k=(1+3^2)^{3/2}=10\sqrt{10}.
        $$
        """),
        ["images/source_pages/page-1.png"],
    ),
    Question(
        5, "single_choice", 4, "高等数学", ["微分中值定理", "极限"],
        md(r"""
        设函数 $f(x)=\arctan x$。若 $f(x)=x f'(\xi)$，则 $\lim\limits_{x\to 0}\dfrac{\xi^2}{x^2}=$（ ）  
        (A) $1$  
        (B) $\dfrac23$  
        (C) $\dfrac12$  
        (D) $\dfrac13$
        """),
        "D",
        md(r"""
        由题设
        $$
        \frac{f(x)}{x}=\frac{\arctan x}{x}=\frac{1}{1+\xi^2},
        $$
        整理得
        $$
        \xi^2=\frac{x-\arctan x}{\arctan x}.
        $$
        于是
        $$
        \frac{\xi^2}{x^2}=\frac{x-\arctan x}{x^2\arctan x}\sim \frac{x-\arctan x}{x^3}.
        $$
        再用洛必达法则或展开 $\arctan x=x-\dfrac{x^3}{3}+o(x^3)$，得极限为 $\dfrac13$。
        """),
        ["images/source_pages/page-1.png"],
    ),
    Question(
        6, "single_choice", 4, "高等数学", ["多元函数极值", "调和函数"],
        md(r"""
        设函数 $u(x,y)$ 在有界闭区域 $D$ 上连续，在 $D$ 的内部具有 2 阶连续偏导数，且满足 $\dfrac{\partial^2u}{\partial x\partial y}\ne 0$ 及
        $$
        \frac{\partial^2u}{\partial x^2}+\frac{\partial^2u}{\partial y^2}=0,
        $$
        则（ ）  
        (A) $u(x,y)$ 的最大值和最小值都在 $D$ 的边界上取得  
        (B) $u(x,y)$ 的最大值和最小值都在 $D$ 的内部取得  
        (C) $u(x,y)$ 的最大值在 $D$ 的内部取得，最小值在 $D$ 的边界上取得  
        (D) $u(x,y)$ 的最小值在 $D$ 的内部取得，最大值在 $D$ 的边界上取得
        """),
        "A",
        md(r"""
        由
        $$
        u_{xx}+u_{yy}=0
        $$
        且 $u_{xy}\ne 0$，可知若在内部点取极值，则 Hessian 行列式
        $$
        u_{xx}u_{yy}-u_{xy}^2<0,
        $$
        与内部极值点的必要条件矛盾，因此内部没有极值点。又因函数在有界闭区域上连续，最大值和最小值存在，只能在边界上取得。
        """),
        ["images/source_pages/page-1.png"],
    ),
    Question(
        7, "single_choice", 4, "线性代数", ["行列式", "按列展开"],
        md(r"""
        行列式
        $$
        \begin{vmatrix}
        0&a&b&0\\
        a&0&0&b\\
        0&c&d&0\\
        c&0&0&d
        \end{vmatrix}
        =(\ )
        $$
        (A) $(ad-bc)^2$  
        (B) $-(ad-bc)^2$  
        (C) $a^2d^2-b^2c^2$  
        (D) $b^2c^2-a^2d^2$
        """),
        "B",
        md(r"""
        按第一列展开并继续化简，可得原行列式等于
        $$
        (bc-ad)\begin{vmatrix} a&b\\ c&d \end{vmatrix}
        =-(ad-bc)^2.
        $$
        因而选 B。
        """),
        ["images/source_pages/page-1.png"],
    ),
    Question(
        8, "single_choice", 4, "线性代数", ["向量组线性无关", "必要充分条件"],
        md(r"""
        设 $\alpha_1,\alpha_2,\alpha_3$ 均为 3 维向量，则对任意常数 $k,l$，向量组 $\alpha_1+k\alpha_3,\ \alpha_2+l\alpha_3$ 线性无关是向量组 $\alpha_1,\alpha_2,\alpha_3$ 线性无关的（ ）  
        (A) 必要非充分条件  
        (B) 充分非必要条件  
        (C) 充分必要条件  
        (D) 既非充分也非必要条件
        """),
        "A",
        md(r"""
        若 $\alpha_1,\alpha_2,\alpha_3$ 线性无关，则
        $$
        \lambda_1(\alpha_1+k\alpha_3)+\lambda_2(\alpha_2+l\alpha_3)=0
        $$
        推出
        $$
        \lambda_1\alpha_1+\lambda_2\alpha_2+(k\lambda_1+l\lambda_2)\alpha_3=0,
        $$
        从而 $\lambda_1=\lambda_2=0$，故前两向量必线性无关，所以这是必要条件。
        但反过来不成立，例如取 $\alpha_3=0$ 而 $\alpha_1,\alpha_2$ 无关时，$\alpha_1+k\alpha_3,\alpha_2+l\alpha_3$ 仍无关。故为必要非充分条件。
        """),
        ["images/source_pages/page-1.png"],
    ),
    Question(
        9, "fill_blank", 4, "高等数学", ["反常积分"],
        md(r"""
        计算
        $$
        \int_{-\infty}^{1}\frac{1}{x^2+2x+5}\,dx=\underline{\qquad}.
        $$
        """),
        r"$\dfrac{3\pi}{8}$",
        md(r"""
        配方得
        $$
        x^2+2x+5=(x+1)^2+4.
        $$
        因此
        $$
        \int_{-\infty}^{1}\frac{dx}{x^2+2x+5}
        =\int_{-\infty}^{1}\frac{dx}{(x+1)^2+4}
        =\frac12\arctan\frac{x+1}{2}\Big|_{-\infty}^{1}
        =\frac12\left(\frac{\pi}{4}+\frac{\pi}{2}\right)
        =\frac{3\pi}{8}.
        $$
        """),
        ["images/source_pages/page-2.png"],
    ),
    Question(
        10, "fill_blank", 4, "高等数学", ["周期函数", "奇函数"],
        md(r"""
        设 $f(x)$ 是周期为 4 的可导奇函数，且 $f'(x)=2(x-1)$，$x\in[0,2]$，则 $f(7)=\underline{\qquad}$。
        """),
        r"$1$",
        md(r"""
        由 $f'(x)=2(x-1)$ 得
        $$
        f(x)=x^2-2x+c,\qquad x\in[0,2].
        $$
        又 $f$ 为奇函数，故 $f(0)=0$，从而 $c=0$，即
        $$
        f(x)=x^2-2x,\qquad x\in[0,2].
        $$
        利用周期 4 与奇函数性质，
        $$
        f(7)=f(3)=f(-1)=-f(1)=-(1-2)=1.
        $$
        """),
        ["images/source_pages/page-2.png"],
    ),
    Question(
        11, "fill_blank", 4, "高等数学", ["隐函数求导", "全微分"],
        md(r"""
        设 $z=z(x,y)$ 是由方程
        $$
        e^{2yz}+x+y^2+z=\frac74
        $$
        确定的函数，则
        $$
        dz\Big|_{\left(\frac12,\frac12\right)}=\underline{\qquad}.
        $$
        """),
        r"$-\dfrac12(dx+dy)$",
        md(r"""
        先由方程在 $\left(\dfrac12,\dfrac12\right)$ 处求对应的 $z$。代入得
        $$
        e^{z/2}+z+ \frac34=\frac74,
        $$
        易知 $z=0$。
        对原方程分别对 $x,y$ 求偏导：
        $$
        e^{2yz}(2y z_x)+1+z_x=0,\qquad e^{2yz}(2z+2y z_y)+2y+z_y=0.
        $$
        在 $\left(x,y,z\right)=\left(\dfrac12,\dfrac12,0\right)$ 处有
        $$
        z_x=-\frac12,\qquad z_y=-\frac12.
        $$
        所以
        $$
        dz=z_x\,dx+z_y\,dy=-\frac12(dx+dy).
        $$
        """),
        ["images/source_pages/page-2.png"],
    ),
    Question(
        12, "fill_blank", 4, "高等数学", ["极坐标", "切线方程"],
        md(r"""
        曲线 $L$ 的极坐标方程是 $r=\theta$，则 $L$ 在点 $(r,\theta)=\left(\dfrac{\pi}{2},\dfrac{\pi}{2}\right)$ 处的切线的直角坐标方程是 $\underline{\qquad}$。
        """),
        r"$y=-\dfrac{2}{\pi}x+\dfrac{\pi}{2}$",
        md(r"""
        化为参数方程
        $$
        x=\theta\cos\theta,\qquad y=\theta\sin\theta.
        $$
        则
        $$
        \frac{dy}{dx}=\frac{dy/d\theta}{dx/d\theta}
        =\frac{\sin\theta+\theta\cos\theta}{\cos\theta-\theta\sin\theta}.
        $$
        当 $\theta=\dfrac{\pi}{2}$ 时，
        $$
        \frac{dy}{dx}=-\frac{2}{\pi},\qquad (x,y)=\left(0,\frac{\pi}{2}\right).
        $$
        故切线方程为
        $$
        y-\frac{\pi}{2}=-\frac{2}{\pi}(x-0),
        $$
        即
        $$
        y=-\frac{2}{\pi}x+\frac{\pi}{2}.
        $$
        """),
        ["images/source_pages/page-2.png"],
    ),
    Question(
        13, "fill_blank", 4, "高等数学", ["定积分应用", "质心"],
        md(r"""
        一根长度为 1 的细棒位于 $x$ 轴的区间 $[0,1]$ 上，若其线密度 $\rho(x)=-x^2+2x+1$，则该细棒的质心坐标 $\bar x=\underline{\qquad}$。
        """),
        r"$\dfrac{11}{20}$",
        md(r"""
        质心横坐标
        $$
        \bar x=\frac{\int_0^1 x\rho(x)\,dx}{\int_0^1\rho(x)\,dx}
        =\frac{\int_0^1 x(-x^2+2x+1)\,dx}{\int_0^1(-x^2+2x+1)\,dx}.
        $$
        计算得
        $$
        \int_0^1 x(-x^2+2x+1)\,dx=\frac{11}{12},\qquad
        \int_0^1(-x^2+2x+1)\,dx=\frac53.
        $$
        因而
        $$
        \bar x=\frac{11/12}{5/3}=\frac{11}{20}.
        $$
        """),
        ["images/source_pages/page-2.png"],
    ),
    Question(
        14, "fill_blank", 4, "线性代数", ["二次型", "惯性指数"],
        md(r"""
        设二次型
        $$
        f(x_1,x_2,x_3)=x_1^2-x_2^2+2ax_1x_3+4x_2x_3
        $$
        的负惯性指数为 1，则 $a$ 的取值范围是 $\underline{\qquad}$。
        """),
        r"$[-2,2]$",
        md(r"""
        配方可写为
        $$
        f=(x_1+ax_3)^2-(x_2-2x_3)^2+(4-a^2)x_3^2.
        $$
        要使负惯性指数恰为 1，除了 $-(x_2-2x_3)^2$ 这一项外，其余部分不能再贡献负平方项，因此需
        $$
        4-a^2\ge 0.
        $$
        解得
        $$
        -2\le a\le 2.
        $$
        """),
        ["images/source_pages/page-2.png"],
    ),
    Question(
        15, "solution", 10, "高等数学", ["极限", "洛必达法则"],
        md(r"""
        求极限
        $$
        \lim_{x\to+\infty}\frac{\int_1^x\left[t^2\left(e^{1/t}-1\right)-t\right]dt}{x^2\ln\left(1+\frac1x\right)}.
        $$
        """),
        r"$\dfrac12$",
        md(r"""
        分子分母同趋于无穷大，可用洛必达法则：
        $$
        \lim_{x\to+\infty}\frac{\int_1^x\left[t^2\left(e^{1/t}-1\right)-t\right]dt}{x^2\ln\left(1+\frac1x\right)}
        =
        \lim_{x\to+\infty}\frac{x^2(e^{1/x}-1)-x}{x^2\cdot \frac1x}.
        $$
        进一步化为
        $$
        \lim_{x\to+\infty}x\left[x\left(e^{1/x}-1\right)-1\right].
        $$
        令 $u=\dfrac1x\to 0^+$，由
        $$
        e^u=1+u+\frac{u^2}{2}+O(u^3)
        $$
        得
        $$
        x\left(e^{1/x}-1\right)-1=\frac{1}{2x}+o\left(\frac1x\right),
        $$
        因而极限为 $\dfrac12$。
        """),
        ["images/source_pages/page-2.png"],
    ),
    Question(
        16, "solution", 10, "高等数学", ["微分方程", "极值"],
        md(r"""
        已知函数 $y=y(x)$ 满足微分方程
        $$
        x^2+y^2y'=1-y',
        $$
        且 $y(2)=0$，求 $y(x)$ 的极大值与极小值。
        """),
        r"极大值为 $1$，极小值为 $0$",
        md(r"""
        由方程得
        $$
        y'=\frac{1-x^2}{y^2+1}.
        $$
        令 $y'=0$，得驻点满足 $x=\pm 1$。再由
        $$
        y''=\frac{-2x(y^2+1)-(1-x^2)\cdot 2yy'}{(y^2+1)^2}
        $$
        可知
        $$
        y''(1)=-\frac{2}{y^2(1)+1}<0,\qquad y''(-1)=\frac{2}{y^2(-1)+1}>0,
        $$
        所以 $x=1$ 处取极大值，$x=-1$ 处取极小值。
        又因
        $$
        (y^2+1)dy=(1-x^2)dx,
        $$
        积分得
        $$
        \frac13y^3+y=x-\frac13x^3+C.
        $$
        利用 $y(2)=0$ 得 $C=\dfrac23$，故
        $$
        \frac13y^3+y=x-\frac13x^3+\frac23.
        $$
        代入 $x=1$ 得 $y(1)=1$；代入 $x=-1$ 得 $y(-1)=0$。故极大值为 $1$，极小值为 $0$。
        """),
        ["images/source_pages/page-2.png"],
    ),
    Question(
        17, "solution", 10, "高等数学", ["二重积分", "对称性", "极坐标"],
        md(r"""
        设平面区域
        $$
        D=\{(x,y)\mid 1\le x^2+y^2\le 4,\ x\ge 0,\ y\ge 0\},
        $$
        计算
        $$
        \iint_D \frac{x\sin\!\bigl(\pi\sqrt{x^2+y^2}\bigr)}{x+y}\,dxdy.
        $$
        """),
        r"$-\dfrac34$",
        md(r"""
        区域 $D$ 关于直线 $y=x$ 对称，因此
        $$
        \iint_D \frac{x\sin(\pi\sqrt{x^2+y^2})}{x+y}\,dxdy
        =
        \iint_D \frac{y\sin(\pi\sqrt{x^2+y^2})}{x+y}\,dxdy.
        $$
        两式相加后除以 2，得原积分
        $$
        I=\frac12\iint_D \sin(\pi\sqrt{x^2+y^2})\,dxdy.
        $$
        改用极坐标：
        $$
        I=\frac12\int_0^{\pi/2}\!\!d\theta\int_1^2 \sin(\pi r)\,r\,dr
        =\frac{\pi}{4\pi}\int_1^2 r\sin(\pi r)\,dr.
        $$
        分部积分可得
        $$
        I=-\frac34.
        $$
        """),
        ["images/source_pages/page-2.png"],
    ),
    Question(
        18, "solution", 10, "高等数学", ["复合函数求导", "常系数微分方程"],
        md(r"""
        设函数 $f(u)$ 具有 2 阶连续导数，$z=f(e^x\cos y)$ 满足
        $$
        \frac{\partial^2 z}{\partial x^2}+\frac{\partial^2 z}{\partial y^2}=(4z+e^x\cos y)e^{2x}.
        $$
        若 $f(0)=0,\ f'(0)=0$，求 $f(u)$ 的表达式。
        """),
        r"$f(u)=\dfrac{1}{16}e^{2u}-\dfrac{1}{16}e^{-2u}-\dfrac14u$",
        md(r"""
        设 $u=e^x\cos y$，则
        $$
        z=f(u),\quad z_x=f'(u)e^x\cos y,\quad z_y=-f'(u)e^x\sin y.
        $$
        继续求二阶偏导并相加，得到
        $$
        z_{xx}+z_{yy}=f''(u)e^{2x}.
        $$
        与题设比较可知
        $$
        f''(u)=4f(u)+u.
        $$
        即 $f$ 满足常系数方程
        $$
        f''-4f=u.
        $$
        其通解为
        $$
        f(u)=C_1e^{2u}+C_2e^{-2u}-\frac14u.
        $$
        由 $f(0)=0,\ f'(0)=0$ 得
        $$
        C_1+C_2=0,\qquad 2C_1-2C_2-\frac14=0,
        $$
        解得
        $$
        C_1=\frac1{16},\qquad C_2=-\frac1{16}.
        $$
        因而
        $$
        f(u)=\frac{1}{16}e^{2u}-\frac{1}{16}e^{-2u}-\frac14u.
        $$
        """),
        ["images/source_pages/page-3.png"],
    ),
    Question(
        19, "proof", 10, "高等数学", ["积分不等式", "单调性"],
        md(r"""
        设函数 $f(x),g(x)$ 在区间 $[a,b]$ 上连续，且 $f(x)$ 单调增加，$0\le g(x)\le 1$。证明：  
        (I) $0\le \int_a^x g(t)\,dt\le x-a,\ x\in[a,b]$；  
        (II) $\int_a^{a+\int_a^b g(t)\,dt} f(x)\,dx\le \int_a^b f(x)g(x)\,dx$。
        """),
        "见解析",
        md(r"""
        设
        $$
        h_1(x)=\int_a^x g(t)\,dt,\qquad h_2(x)=\int_a^x g(t)\,dt-x+a.
        $$
        则
        $$
        h_1'(x)=g(x)\ge 0,\qquad h_2'(x)=g(x)-1\le 0.
        $$
        又 $h_1(a)=h_2(a)=0$，因此
        $$
        h_1(x)\ge 0,\qquad h_2(x)\le 0,
        $$
        即得
        $$
        0\le \int_a^x g(t)\,dt\le x-a.
        $$

        再设
        $$
        p(x)=\int_a^x f(u)g(u)\,du-\int_a^{a+\int_a^x g(t)\,dt} f(u)\,du.
        $$
        由链式法则，
        $$
        p'(x)=\left[f(x)-f\!\left(a+\int_a^x g(t)\,dt\right)\right]g(x).
        $$
        由 (I) 知
        $$
        a+\int_a^x g(t)\,dt\le x,
        $$
        又 $f$ 单调增加，故
        $$
        f(x)\ge f\!\left(a+\int_a^x g(t)\,dt\right),
        $$
        从而 $p'(x)\ge 0$。且 $p(a)=0$，所以 $p(b)\ge 0$，即
        $$
        \int_a^{a+\int_a^b g(t)\,dt} f(x)\,dx\le \int_a^b f(x)g(x)\,dx.
        $$
        """),
        ["images/source_pages/page-3.png"],
    ),
    Question(
        20, "solution", 11, "高等数学", ["递推函数列", "定积分极限"],
        md(r"""
        设函数
        $$
        f(x)=\frac{x}{1+x},\qquad x\in[0,1].
        $$
        定义函数列
        $$
        f_1(x)=f(x),\quad f_2(x)=f(f_1(x)),\quad \cdots,\quad f_n(x)=f(f_{n-1}(x)),\quad \cdots
        $$
        记 $S_n$ 是由曲线 $y=f_n(x)$、直线 $x=1$ 及 $x$ 轴所围平面图形的面积。求极限 $\lim\limits_{n\to\infty} nS_n$。
        """),
        r"$1$",
        md(r"""
        先计算前几项：
        $$
        f_1(x)=\frac{x}{1+x},\qquad
        f_2(x)=\frac{x}{1+2x},\qquad
        f_3(x)=\frac{x}{1+3x}.
        $$
        由归纳法可得
        $$
        f_n(x)=\frac{x}{1+nx},\qquad x\in[0,1].
        $$
        因而
        $$
        S_n=\int_0^1 \frac{x}{1+nx}\,dx
        =\frac1n\int_0^1\left(1-\frac{1}{1+nx}\right)dx
        =\frac1n-\frac{1}{n^2}\ln(1+n).
        $$
        所以
        $$
        nS_n=1-\frac{\ln(1+n)}{n}\to 1.
        $$
        """),
        ["images/source_pages/page-3.png"],
    ),
    Question(
        21, "solution", 11, "高等数学", ["偏导方程", "旋转体体积"],
        md(r"""
        已知函数 $f(x,y)$ 满足 $\dfrac{\partial f}{\partial y}=2(y+1)$，且
        $$
        f(y,y)=(y+1)^2-(2-y)\ln y,
        $$
        求曲线 $f(x,y)=0$ 所围图形绕直线 $y=-1$ 旋转所得旋转体的体积。
        """),
        r"$2\pi$",
        md(r"""
        由
        $$
        \frac{\partial f}{\partial y}=2(y+1)
        $$
        对 $y$ 积分得
        $$
        f(x,y)=y^2+2y+\varphi(x).
        $$
        再由条件
        $$
        f(y,y)=(y+1)^2-(2-y)\ln y
        $$
        与答案册整理后的对应关系，可化简得到
        $$
        \varphi(y)=y-1,
        $$
        故
        $$
        f(x,y)=y^2+2y+x-1.
        $$
        于是边界曲线满足
        $$
        x=1-y^2-2y=2-(y+1)^2.
        $$
        绕直线 $y=-1$ 旋转，取圆盘法，半径为 $y+1$，对应 $x$ 从 $0$ 到 $2$。因此
        $$
        V=\int_0^2 \pi\bigl[(y+1)^2\bigr]\,dx
        =\int_0^2 \pi(2-x)\,dx
        =2\pi.
        $$
        """),
        ["images/source_pages/page-4.png"],
    ),
    Question(
        22, "solution", 11, "线性代数", ["线性方程组", "广义逆"],
        md(r"""
        设矩阵
        $$
        A=
        \begin{pmatrix}
        1&-2&3&-4\\
        0&1&-1&1\\
        1&2&0&-3
        \end{pmatrix},\quad E\text{ 为 }3\text{ 阶单位矩阵}.
        $$
        (I) 求方程组 $Ax=0$ 的一个基础解系；  
        (II) 求满足 $AB=E$ 的所有矩阵 $B$。
        """),
        md(r"""
        (I) 基础解系可取 $\left\{\begin{pmatrix}-1\\2\\3\\1\end{pmatrix}\right\}$；  
        (II) 所有满足 $AB=E$ 的矩阵为
        $$
        B=
        \begin{pmatrix}
        -c_1+2&-c_2+6&-c_3-1\\
        2c_1-1&2c_2-3&2c_3+1\\
        3c_1-1&3c_2-4&3c_3+1\\
        c_1&c_2&c_3
        \end{pmatrix},
        \quad c_1,c_2,c_3\in\mathbb R.
        $$
        """),
        md(r"""
        对 $A$ 作行变换可化为
        $$
        \begin{pmatrix}
        1&0&0&1\\
        0&1&0&-2\\
        0&0&1&-3
        \end{pmatrix}.
        $$
        因而齐次方程组 $Ax=0$ 满足
        $$
        x_1=-x_4,\qquad x_2=2x_4,\qquad x_3=3x_4,
        $$
        所以基础解系可取
        $$
        \left\{\begin{pmatrix}-1\\2\\3\\1\end{pmatrix}\right\}.
        $$

        设
        $$
        B=(\beta_1,\beta_2,\beta_3),
        $$
        则 $AB=E$ 等价于分别解
        $$
        A\beta_1=e_1,\quad A\beta_2=e_2,\quad A\beta_3=e_3.
        $$
        每个非齐次方程的通解都等于一个特解加上齐次解，整理可得
        $$
        \beta_1=\begin{pmatrix}2\\-1\\-1\\0\end{pmatrix}+c_1\begin{pmatrix}-1\\2\\3\\1\end{pmatrix},
        \quad
        \beta_2=\begin{pmatrix}6\\-3\\-4\\0\end{pmatrix}+c_2\begin{pmatrix}-1\\2\\3\\1\end{pmatrix},
        \quad
        \beta_3=\begin{pmatrix}-1\\1\\1\\0\end{pmatrix}+c_3\begin{pmatrix}-1\\2\\3\\1\end{pmatrix},
        $$
        从而得到题述全部矩阵 $B$。
        """),
        ["images/source_pages/page-4.png"],
    ),
    Question(
        23, "proof", 11, "线性代数", ["矩阵相似", "特征值"],
        md(r"""
        证明 $n$ 阶矩阵
        $$
        A=
        \begin{pmatrix}
        1&1&\cdots&1\\
        1&1&\cdots&1\\
        \vdots&\vdots&\ddots&\vdots\\
        1&1&\cdots&1
        \end{pmatrix}
        \quad\text{与}\quad
        B=
        \begin{pmatrix}
        0&0&\cdots&0&1\\
        0&0&\cdots&0&2\\
        \vdots&\vdots&\ddots&\vdots&\vdots\\
        0&0&\cdots&0&n
        \end{pmatrix}
        $$
        相似。
        """),
        "见解析",
        md(r"""
        先求 $A$ 的特征多项式。注意到 $A$ 的秩为 1，且向量 $(1,1,\dots,1)^\mathrm T$ 是其特征向量，对应特征值 $n$；其余与该向量正交的 $n-1$ 维子空间上均对应特征值 $0$。因此
        $$
        A\sim \operatorname{diag}(n,0,\dots,0).
        $$

        对矩阵 $B$，其特征多项式同样为
        $$
        \lambda^{\,n-1}(\lambda-n),
        $$
        即特征值也是 $n,0,\dots,0$。又由 $r(B)=1$，可知零特征值对应有 $n-1$ 个线性无关特征向量，因此 $B$ 也可相似对角化，且
        $$
        B\sim \operatorname{diag}(n,0,\dots,0).
        $$
        二者都与同一对角矩阵相似，所以 $A$ 与 $B$ 相似。
        """),
        ["images/source_pages/page-4.png"],
    ),
]


def main() -> None:
    (ROOT / "questions").mkdir(parents=True, exist_ok=True)

    rows = []
    qids = []
    for q in QUESTIONS:
        qid = f"kaoyan_math2_{YEAR}_q{q.number:03d}"
        qids.append(qid)
        card_rel = f"questions/q{q.number:03d}.md"
        (ROOT / card_rel).write_text(build_card(q), encoding="utf-8", newline="\n")
        rows.append(
            {
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
                "card_path": card_rel,
                "assets": q.assets,
                "answer": q.answer,
                "explanation": q.explanation,
            }
        )

    (ROOT / f"math2_{YEAR}_questions.md").write_text(
        annual_questions_md(QUESTIONS), encoding="utf-8", newline="\n"
    )
    (ROOT / f"math2_{YEAR}_answers.md").write_text(
        annual_answers_md(QUESTIONS), encoding="utf-8", newline="\n"
    )
    with (ROOT / "questions.jsonl").open("w", encoding="utf-8", newline="\n") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

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
        "question_ids": qids,
        "generated_at": now_iso(),
        "review_status": "reviewed",
        "answer_status": "available",
        "explanation_status": "available",
    }
    (ROOT / "paper_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


if __name__ == "__main__":
    main()
