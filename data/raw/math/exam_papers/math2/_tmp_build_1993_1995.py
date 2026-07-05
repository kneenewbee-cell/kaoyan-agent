from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent
YEAR = 1994
YEAR_DIR = ROOT / str(YEAR)


@dataclass
class Question:
    number: int
    question_type: str
    score: int
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
    topic_lines = [f"  - {topic}" for topic in q.topics]
    asset_lines = [f"  - {asset}" for asset in q.assets]
    image_lines = [f"![题图](../{asset})" for asset in q.assets]
    lines = [
        "---",
        f"question_id: {qid}",
        f"exam_id: kaoyan_math2_{YEAR}",
        "exam_type: math2",
        f"year: {YEAR}",
        f"question_number: {q.number}",
        f"question_type: {q.question_type}",
        f"score: {q.score}",
        "module: 高等数学",
        "topics:",
        *topic_lines,
        "difficulty: unknown",
        "review_status: reviewed",
        "answer_status: available",
        "explanation_status: available",
        f"source_file: math2_{YEAR}_questions.md",
        f"answer_source_file: math2_{YEAR}_answers.md",
        "assets:",
        *asset_lines,
        "---",
        "",
        f"# {YEAR} 数学二第 {q.number} 题",
        "",
        "## 题目",
        "",
        q.stem,
        "",
        *image_lines,
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
        "整理状态：已按原卷页面图像校对并转写。",
        "",
    ]
    for q in questions:
        lines.extend(
            [
                f"## 第 {q.number} 题",
                f"- 题型：{qtype_label(q.question_type)}",
                f"- 分值：{q.score}",
                "- 模块：高等数学",
                f"- 考点：{'、'.join(q.topics)}",
                "",
                q.stem,
                "",
            ]
        )
        for asset in q.assets:
            lines.extend([f"![{YEAR} 数学二题图]({asset})", ""])
    return "\n".join(lines).rstrip() + "\n"


def annual_answers_md(questions: list[Question]) -> str:
    lines = [
        f"# Math 2 {YEAR} Answers",
        "",
        "资料类型：考研数学二答案解析",
        f"年份：{YEAR}",
        "科目：数学二",
        "范围：试卷 III",
        "校对状态：已按答案页图像清洗并与题面同步。",
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
    Question(1, "fill_blank", 3, ["极限", "连续"], "若\n$$\nf(x)=\\begin{cases}\n\\dfrac{\\sin 2x+e^{2ax}-1}{x},&x\\ne 0,\\\\\na,&x=0,\n\\end{cases}\n$$\n在 $(-\\infty,+\\infty)$ 上连续，则 $a=\\underline{\\qquad}$。", "$-2$", "要使 $f(x)$ 在 $x=0$ 处连续，需有\n$$\na=\\lim_{x\\to 0}\\frac{\\sin 2x+e^{2ax}-1}{x}.\n$$\n由 $\\sin 2x\\sim 2x$，$e^{2ax}-1\\sim 2ax$，得\n$$\na=2+2a,\n$$\n故 $a=-2$。", ["images/source_pages/page-1.png"]),
    Question(2, "fill_blank", 3, ["参数方程", "二阶导数"], "设函数 $y=y(x)$ 由参数方程\n$$\n\\begin{cases}\nx=t-\\ln(1+t),\\\\\ny=t^3+t^2\n\\end{cases}\n$$\n所确定，则 $\\dfrac{d^2y}{dx^2}=\\underline{\\qquad}$。", "$\\dfrac{(t+1)(6t+5)}{t}$", "先求\n$$\n\\frac{dy}{dx}=\\frac{dy/dt}{dx/dt}=\\frac{3t^2+2t}{1-\\frac{1}{1+t}}=3t^2+5t+2.\n$$\n再对 $t$ 求导，得\n$$\n\\frac{d^2y}{dx^2}=\\frac{6t+5}{1-\\frac{1}{1+t}}=\\frac{(t+1)(6t+5)}{t}.\n$$", ["images/source_pages/page-1.png"]),
    Question(3, "fill_blank", 3, ["变上限积分", "复合函数"], "计算\n$$\n\\frac{d}{dx}\\left(\\int_0^{\\cos 3x}f(t)\\,dt\\right)=\\underline{\\qquad}.\n$$", "$-3\\sin 3x\\,f(\\cos 3x)$", "由变上限积分求导公式与链式法则，\n$$\n\\frac{d}{dx}\\left(\\int_0^{\\cos 3x}f(t)\\,dt\\right)=f(\\cos 3x)\\cdot(\\cos 3x)'=-3\\sin 3x\\,f(\\cos 3x).\n$$", ["images/source_pages/page-1.png"]),
    Question(4, "fill_blank", 3, ["不定积分", "分部积分"], "计算\n$$\n\\int x^3e^{x^2}\\,dx=\\underline{\\qquad}.\n$$", "$\\dfrac12(x^2-1)e^{x^2}+C$", "写成\n$$\n\\int x^3e^{x^2}\\,dx=\\frac12\\int x^2\\,d(e^{x^2}).\n$$\n作分部积分得\n$$\n\\frac12\\int x^2\\,d(e^{x^2})=\\frac12\\left[x^2e^{x^2}-\\int e^{x^2}\\,d(x^2)\\right]=\\frac12(x^2-1)e^{x^2}+C.\n$$", ["images/source_pages/page-1.png"]),
    Question(5, "fill_blank", 3, ["可分离变量方程", "微分方程"], "微分方程\n$$\ny\\,dx+(x^2-4x)\\,dy=0\n$$\n的通解为 $\\underline{\\qquad}$。", "$(x-4)y^4=Cx$", "原方程可写成\n$$\n\\frac{dx}{x(x-4)}+\\frac{dy}{y}=0.\n$$\n积分得\n$$\n\\frac14\\ln\\left|\\frac{x-4}{x}\\right|+\\ln|y|=C_1.\n$$\n化简为\n$$\n\\frac{x-4}{x}y^4=C,\n$$\n即\n$$\n(x-4)y^4=Cx.\n$$", ["images/source_pages/page-1.png"]),
    Question(6, "single_choice", 3, ["极限", "泰勒展开"], "设\n$$\n\\lim_{x\\to 0}\\frac{\\ln(1+x)-(ax+bx^2)}{x^2}=2,\n$$\n则（  ）\n\nA. $a=1,b=-\\dfrac52$\n\nB. $a=0,b=-2$\n\nC. $a=0,b=-\\dfrac52$\n\nD. $a=1,b=-2$", "A", "由 $\\ln(1+x)=x-\\dfrac{x^2}{2}+o(x^2)$，得\n$$\n\\ln(1+x)-(ax+bx^2)=(1-a)x-\\left(\\frac12+b\\right)x^2+o(x^2).\n$$\n由题设应有\n$$\n1-a=0,\\qquad -\\left(\\frac12+b\\right)=2.\n$$\n故 $a=1,b=-\\dfrac52$，选 A。", ["images/source_pages/page-1.png"]),
    Question(7, "single_choice", 3, ["分段函数", "可导性"], "设\n$$\nf(x)=\\begin{cases}\n\\dfrac23x^3,&x\\le 1,\\\\\nx^2,&x>1,\n\\end{cases}\n$$\n则 $f(x)$ 在点 $x=1$ 处的（  ）\n\nA. 左、右导数都存在\n\nB. 左导数存在，但右导数不存在\n\nC. 左导数不存在，但右导数存在\n\nD. 左、右导数都不存在", "B", "左侧函数可导，且\n$$\nf'_-(1)=\\left(\\frac23x^3\\right)'\\bigg|_{x=1}=2.\n$$\n又有\n$$\nf(1)=\\frac23,\\qquad \\lim_{x\\to1^+}f(x)=1\\ne f(1),\n$$\n故 $f$ 在 $x=1$ 右侧不连续，从而右导数不存在，选 B。", ["images/source_pages/page-1.png"]),
    Question(8, "single_choice", 3, ["微分方程", "极值"], "设 $y=f(x)$ 是满足微分方程\n$$\ny''+y'-e^{\\sin x}=0\n$$\n的解，且 $f'(x_0)=0$，则 $f(x)$ 在（  ）\n\nA. $x_0$ 的某个邻域内单调增加\n\nB. $x_0$ 的某个邻域内单调减少\n\nC. $x_0$ 处取得极小值\n\nD. $x_0$ 处取得极大值", "C", "在 $x=x_0$ 处有\n$$\nf''(x_0)+f'(x_0)=e^{\\sin x_0}.\n$$\n由 $f'(x_0)=0$ 得\n$$\nf''(x_0)=e^{\\sin x_0}>0.\n$$\n故 $x_0$ 是极小值点，选 C。", ["images/source_pages/page-1.png"]),
    Question(9, "single_choice", 3, ["渐近线", "极限"], "曲线\n$$\ny=e^{1/x^2}\\arctan\\frac{x^2+x+1}{(x-1)(x+2)}\n$$\n的渐近线有（  ）\n\nA. 1 条\n\nB. 2 条\n\nC. 3 条\n\nD. 4 条", "B", "当 $x\\to\\pm\\infty$ 时，$e^{1/x^2}\\to1$，且\n$$\n\\frac{x^2+x+1}{(x-1)(x+2)}\\to1,\n$$\n故有水平渐近线 $y=\\arctan1=\\dfrac\\pi4$。当 $x\\to0$ 时，\n$$\n\\arctan\\frac{x^2+x+1}{(x-1)(x+2)}\\to\\arctan\\left(-\\frac12\\right)<0,\n$$\n而 $e^{1/x^2}\\to+\\infty$，故 $y\\to-\\infty$，所以 $x=0$ 是铅直渐近线。$x=1,-2$ 处函数值有界，不是渐近线。故共 2 条，选 B。", ["images/source_pages/page-1.png"]),
    Question(10, "single_choice", 3, ["定积分", "奇偶性"], "设\n$$\nM=\\int_{-\\pi/2}^{\\pi/2}\\frac{\\sin x}{1+x^2}\\cos^4x\\,dx,\n$$\n$$\nN=\\int_{-\\pi/2}^{\\pi/2}(\\sin^3x+\\cos^4x)\\,dx,\n$$\n$$\nP=\\int_{-\\pi/2}^{\\pi/2}(x^2\\sin^3x-\\cos^4x)\\,dx,\n$$\n则有（  ）\n\nA. $N<P<M$\n\nB. $M<P<N$\n\nC. $N<M<P$\n\nD. $P<M<N$", "D", "被积函数 $\\dfrac{\\sin x}{1+x^2}\\cos^4x$ 为奇函数，故 $M=0$。又\n$$\nN=\\int_{-\\pi/2}^{\\pi/2}\\sin^3x\\,dx+\\int_{-\\pi/2}^{\\pi/2}\\cos^4x\\,dx=2\\int_0^{\\pi/2}\\cos^4x\\,dx>0,\n$$\n$$\nP=\\int_{-\\pi/2}^{\\pi/2}x^2\\sin^3x\\,dx-\\int_{-\\pi/2}^{\\pi/2}\\cos^4x\\,dx=-N<0.\n$$\n故 $P<M<N$，选 D。", ["images/source_pages/page-1.png"]),
    Question(11, "solution", 5, ["复合函数", "二阶导数"], "设 $y=f(x+y)$，其中 $f$ 具有二阶导数，且其一阶导数不等于 1，求 $\\dfrac{d^2y}{dx^2}$。", "$y''=\\dfrac{f''}{(1-f')^3}$", "对方程 $y=f(x+y)$ 两边对 $x$ 求导，得\n$$\ny'=f'(1+y').\n$$\n故\n$$\ny'=\\frac{f'}{1-f'}.\n$$\n再求导，有\n$$\ny''=f''(1+y')^2+f'y''.\n$$\n移项得\n$$\n(1-f')y''=f''(1+y')^2.\n$$\n而\n$$\n1+y'=1+\\frac{f'}{1-f'}=\\frac1{1-f'},\n$$\n所以\n$$\ny''=\\frac{f''}{(1-f')^3}.\n$$", ["images/source_pages/page-2.png"]),
    Question(12, "solution", 5, ["定积分", "换元积分"], "计算\n$$\n\\int_0^1x(1-x^4)^{3/2}\\,dx.\n$$", "$\\dfrac{3\\pi}{32}$", "令 $x^2=\\sin t$，则 $2x\\,dx=\\cos t\\,dt$。当 $x=0$ 时 $t=0$，当 $x=1$ 时 $t=\\dfrac\\pi2$，故\n$$\n\\int_0^1x(1-x^4)^{3/2}dx=\\frac12\\int_0^{\\pi/2}\\cos^4t\\,dt.\n$$\n又\n$$\n\\int_0^{\\pi/2}\\cos^4t\\,dt=\\frac{3\\pi}{16},\n$$\n故原积分为\n$$\n\\frac12\\cdot\\frac{3\\pi}{16}=\\frac{3\\pi}{32}.\n$$", ["images/source_pages/page-2.png"]),
    Question(13, "solution", 5, ["重要极限", "三角变换"], "计算极限\n$$\n\\lim_{n\\to\\infty}\\tan^n\\left(\\frac\\pi4+\\frac2n\\right).\n$$", "$e^4$", "利用\n$$\n\\tan\\left(\\frac\\pi4+u\\right)=\\frac{1+\\tan u}{1-\\tan u},\n$$\n取 $u=\\dfrac2n$，得\n$$\n\\tan^n\\left(\\frac\\pi4+\\frac2n\\right)=\\left(1+\\frac{2\\tan(2/n)}{1-\\tan(2/n)}\\right)^n.\n$$\n由 $\\tan(2/n)\\sim 2/n$ 可知\n$$\nn\\cdot\\frac{2\\tan(2/n)}{1-\\tan(2/n)}\\to4,\n$$\n于是由重要极限得原极限为 $e^4$。", ["images/source_pages/page-2.png"]),
    Question(14, "solution", 5, ["不定积分", "换元积分"], "计算\n$$\n\\int\\frac{dx}{\\sin 2x+2\\sin x}.\n$$", "$\\dfrac18\\left[\\ln(1-\\cos x)-\\ln(1+\\cos x)+\\dfrac{2}{1+\\cos x}\\right]+C$", "先化简分母：\n$$\n\\sin2x+2\\sin x=2\\sin x(1+\\cos x).\n$$\n令 $u=\\cos x$，则 $du=-\\sin x\\,dx$，原式化为\n$$\n-\\frac12\\int\\frac{du}{(1-u)(1+u)^2}.\n$$\n将被积函数分解为\n$$\n\\frac{1}{(1-u)(1+u)^2}=\\frac14\\cdot\\frac1{1-u}+\\frac14\\cdot\\frac1{1+u}+\\frac12\\cdot\\frac1{(1+u)^2}.\n$$\n逐项积分后得\n$$\n\\int\\frac{dx}{\\sin2x+2\\sin x}=\\frac18\\left[\\ln(1-u)-\\ln(1+u)+\\frac{2}{1+u}\\right]+C.\n$$\n代回 $u=\\cos x$ 即得。", ["images/source_pages/page-2.png"]),
    Question(15, "solution", 5, ["定积分", "不等式证明"], "如图，设曲线方程为 $y=x^2+\\dfrac12$，梯形 $OABC$ 的面积为 $D$，曲边梯形 $OABC$ 的面积为 $D_1$，点 $A$ 的坐标为 $(a,0)$，$a>0$。证明：\n$$\n\\frac{D}{D_1}<\\frac32.\n$$", "见解析。", "由图可知 $C=(0,\\tfrac12)$，$B=(a,a^2+\\tfrac12)$。故梯形面积\n$$\nD=\\frac{\\frac12+\\left(a^2+\\frac12\\right)}{2}\\cdot a=\\frac{a(1+a^2)}{2}.\n$$\n曲边梯形面积\n$$\nD_1=\\int_0^a\\left(x^2+\\frac12\\right)dx=\\frac{a^3}{3}+\\frac a2=\\frac{a(3+2a^2)}{6}.\n$$\n于是\n$$\n\\frac{D}{D_1}=\\frac{3(1+a^2)}{3+2a^2}=\\frac32\\cdot\\frac{1+a^2}{\\frac32+a^2}<\\frac32.\n$$", ["images/source_pages/page-2.png", "images/q015_diagram.png"]),
    Question(16, "solution", 9, ["方程根的个数", "导数应用"], "设当 $x>0$ 时，方程\n$$\nkx+\\frac1{x^2}=1\n$$\n有且仅有一个解，求 $k$ 的取值范围。", "$k\\le0$ 或 $k=\\dfrac{2\\sqrt3}{9}$", "方程可化为\n$$\nkx^3-x^2+1=0.\n$$\n记 $\\varphi(x)=kx^3-x^2+1$。则\n$$\n\\varphi'(x)=3kx^2-2x=x(3kx-2).\n$$\n当 $k\\le0$ 时，对一切 $x>0$ 有 $\\varphi'(x)<0$，故 $\\varphi$ 单调减少，且 $\\varphi(0)=1>0$，在 $x>0$ 上恰有一个零点。\n当 $k>0$ 时，$\\varphi$ 先减后增，极小值在 $x=\\dfrac{2}{3k}$ 处取得。要使正根唯一，必须有极小值为零，即\n$$\n\\varphi\\left(\\frac{2}{3k}\\right)=1-\\frac{4}{27k^2}=0.\n$$\n解得\n$$\nk=\\frac{2\\sqrt3}{9}.\n$$\n综上，\n$$\nk\\le0\\quad\\text{或}\\quad k=\\frac{2\\sqrt3}{9}.\n$$", ["images/source_pages/page-2.png"]),
    Question(17, "solution", 9, ["导数应用", "渐近线"], "设\n$$\ny=\\frac{x^3+4}{x^2},\n$$\n(1) 求函数的增减区间及极值；\n(2) 求函数图形的凹凸区间及拐点；\n(3) 求其渐近线；\n(4) 作出其图形。", "函数在 $(-\\infty,0)\\cup(2,+\\infty)$ 上单调增加，在 $(0,2)$ 上单调减少；在 $x=2$ 处取极小值 $3$；在 $(-\\infty,0)\\cup(0,+\\infty)$ 上均为凹，无拐点；渐近线为 $x=0$ 与 $y=x$。", "函数可化为\n$$\ny=x+\\frac{4}{x^2},\\qquad x\\ne0.\n$$\n故\n$$\ny'=1-\\frac8{x^3},\\qquad y''=\\frac{24}{x^4}>0.\n$$\n由 $y'=0$ 得驻点 $x=2$。于是函数在 $(-\\infty,0)$、$(2,+\\infty)$ 上单调增加，在 $(0,2)$ 上单调减少，且\n$$\ny(2)=2+\\frac44=3,\n$$\n所以在 $x=2$ 处取极小值 $3$。由于 $y''>0$ 对一切 $x\\ne0$ 成立，所以在 $(-\\infty,0)$ 与 $(0,+\\infty)$ 上均为凹，不存在拐点。\n又\n$$\n\\lim_{x\\to0}y=+\\infty,\n$$\n故 $x=0$ 为铅直渐近线；并且\n$$\n\\lim_{x\\to\\pm\\infty}\\frac{y}{x}=1,\\qquad \\lim_{x\\to\\pm\\infty}(y-x)=0,\n$$\n故斜渐近线为 $y=x$。据此可作出图形。", ["images/source_pages/page-2.png"]),
    Question(18, "solution", 9, ["二阶常系数非齐次方程"], "求微分方程\n$$\ny''+a^2y=\\sin x\n$$\n的通解，其中常数 $a>0$。", "$\\begin{cases}y=C_1\\cos ax+C_2\\sin ax+\\dfrac{\\sin x}{a^2-1},&a\\ne1,\\\\[4pt]y=C_1\\cos x+C_2\\sin x-\\dfrac{x}{2}\\cos x,&a=1.\\end{cases}$", "对应齐次方程 $y''+a^2y=0$ 的通解为\n$$\ny_h=C_1\\cos ax+C_2\\sin ax.\n$$\n当 $a\\ne1$ 时，设特解为 $y_p=A\\sin x+B\\cos x$，代入得\n$$\n(a^2-1)A=1,\\qquad (a^2-1)B=0,\n$$\n故\n$$\ny_p=\\frac{\\sin x}{a^2-1}.\n$$\n当 $a=1$ 时发生共振，设特解为\n$$\ny_p=x(A\\sin x+B\\cos x).\n$$\n代入方程得 $A=0,B=-\\dfrac12$，于是\n$$\ny_p=-\\frac{x}{2}\\cos x.\n$$\n故所求通解即为题中所示。", ["images/source_pages/page-2.png"]),
    Question(19, "solution", 9, ["定积分", "不等式证明"], "设 $f(x)$ 在 $[0,1]$ 上连续且递减，证明：当 $0<\\lambda<1$ 时，\n$$\n\\int_0^\\lambda f(x)\\,dx\\ge \\lambda\\int_0^1f(x)\\,dx.\n$$", "见解析。", "作代换 $x=\\lambda t$，则\n$$\n\\int_0^\\lambda f(x)\\,dx=\\lambda\\int_0^1f(\\lambda t)\\,dt.\n$$\n因此\n$$\n\\int_0^\\lambda f(x)\\,dx-\\lambda\\int_0^1f(x)\\,dx=\\lambda\\int_0^1\\bigl[f(\\lambda t)-f(t)\\bigr]dt.\n$$\n由于 $0<\\lambda<1$，对任意 $t\\in[0,1]$ 都有 $\\lambda t\\le t$，又 $f$ 递减，故\n$$\nf(\\lambda t)\\ge f(t).\n$$\n于是右端非负，从而\n$$\n\\int_0^\\lambda f(x)\\,dx\\ge \\lambda\\int_0^1f(x)\\,dx.\n$$", ["images/source_pages/page-2.png"]),
    Question(20, "solution", 9, ["旋转体体积", "定积分"], "求曲线\n$$\ny=3-|x^2-1|\n$$\n与 $x$ 轴围成的封闭图形绕直线 $y=3$ 旋转所得的旋转体体积。", "$\\dfrac{448\\pi}{15}$", "曲线关于 $y$ 轴对称，且与 $x$ 轴交于 $(-2,0)$、$(2,0)$。只算右半边即可。对 $0\\le x\\le2$，有\n$$\n3-y=|x^2-1|.\n$$\n以竖条作体积微元，得\n$$\ndV=\\pi\\left[3^2-(3-y)^2\\right]dx=\\pi\\left[9-(x^2-1)^2\\right]dx=\\pi(8+2x^2-x^4)dx.\n$$\n故总体积\n$$\nV=2\\pi\\int_0^2(8+2x^2-x^4)dx\n=2\\pi\\left[8x+\\frac23x^3-\\frac15x^5\\right]_0^2\n=\\frac{448\\pi}{15}.\n$$", ["images/source_pages/page-2.png"]),
]


def main() -> None:
    (YEAR_DIR / "questions").mkdir(parents=True, exist_ok=True)
    qids = [f"kaoyan_math2_{YEAR}_q{q.number:03d}" for q in QUESTIONS]
    rows = []
    for q in QUESTIONS:
        card_rel = f"questions/q{q.number:03d}.md"
        (YEAR_DIR / card_rel).write_text(build_card(q), encoding="utf-8", newline="\n")
        rows.append(
            {
                "question_id": f"kaoyan_math2_{YEAR}_q{q.number:03d}",
                "exam_id": f"kaoyan_math2_{YEAR}",
                "exam_type": "math2",
                "year": YEAR,
                "question_number": q.number,
                "question_type": q.question_type,
                "score": q.score,
                "module": "高等数学",
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

    (YEAR_DIR / f"math2_{YEAR}_questions.md").write_text(annual_questions_md(QUESTIONS), encoding="utf-8", newline="\n")
    (YEAR_DIR / f"math2_{YEAR}_answers.md").write_text(annual_answers_md(QUESTIONS), encoding="utf-8", newline="\n")
    with (YEAR_DIR / "questions.jsonl").open("w", encoding="utf-8", newline="\n") as f:
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
        "paper_scope": "试卷 III only",
        "review_status": "reviewed",
        "answer_status": "available",
        "explanation_status": "available",
    }
    (YEAR_DIR / "paper_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
