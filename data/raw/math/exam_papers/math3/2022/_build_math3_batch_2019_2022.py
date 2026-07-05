from __future__ import annotations

import json
from pathlib import Path

import fitz
from rapidocr_onnxruntime import RapidOCR


ROOT = Path(__file__).resolve().parents[1]
PDF_QUESTION = {
    2022: Path(r"D:\百度网盘\高数资料\【01】1987-2022考研数学三真题（PDF）\2022年考研数学三真题.pdf"),
    2021: Path(r"D:\百度网盘\高数资料\【01】1987-2022考研数学三真题（PDF）\2021年考研数学三真题.pdf"),
    2020: Path(r"D:\百度网盘\高数资料\【01】1987-2022考研数学三真题（PDF）\2020年考研数学三真题.pdf"),
    2019: Path(r"D:\百度网盘\高数资料\【01】1987-2022考研数学三真题（PDF）\2019年考研数学三真题.pdf"),
}
PDF_ANSWER = {
    2022: Path(r"D:\百度网盘\高数资料\【02】1987-2022考研数学三答案解析（PDF）\2022年考研数学三答案.pdf"),
    2021: Path(r"D:\百度网盘\高数资料\【02】1987-2022考研数学三答案解析（PDF）\2021年数学三真题（速查版）.pdf"),
    2020: Path(r"D:\百度网盘\高数资料\【02】1987-2022考研数学三答案解析（PDF）\2020年数学三真题答案解析.pdf"),
    2019: Path(r"D:\百度网盘\高数资料\【02】1987-2022考研数学三答案解析（PDF）\2019年数学三真题答案解析.pdf"),
}


def render_pdf(pdf_path: Path, out_dir: Path, scale: float = 2.0) -> list[dict]:
    out_dir.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(pdf_path)
    meta = []
    for idx, page in enumerate(doc, start=1):
        pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=False)
        png_path = out_dir / f"page-{idx:02d}.png"
        pix.save(png_path)
        text = page.get_text("text")
        meta.append(
            {
                "page": idx,
                "png": png_path.name,
                "text_preview": " ".join(text.split())[:400],
                "char_count": len(text),
            }
        )
    return meta


def extract_text(pdf_path: Path) -> str:
    doc = fitz.open(pdf_path)
    chunks = []
    for idx, page in enumerate(doc, start=1):
        chunks.append(f"===== PAGE {idx:02d} =====\n")
        chunks.append(page.get_text("text"))
        chunks.append("\n")
    return "".join(chunks)


def ocr_png_dir(png_dir: Path) -> str:
    engine = RapidOCR()
    chunks = []
    for png_path in sorted(png_dir.glob("page-*.png")):
        chunks.append(f"===== {png_path.name} =====\n")
        result, _ = engine(str(png_path))
        if result:
            for item in result:
                chunks.append(item[1] + "\n")
        chunks.append("\n")
    return "".join(chunks)


def main() -> None:
    summary = []
    for year in (2022, 2021, 2020, 2019):
        year_dir = ROOT / str(year)
        images_dir = year_dir / "images"
        source_meta = render_pdf(PDF_QUESTION[year], images_dir / "source_pages")
        answer_meta = render_pdf(PDF_ANSWER[year], images_dir / "answer_pages")
        (year_dir / "_ocr_questions.txt").write_text(extract_text(PDF_QUESTION[year]), encoding="utf-8")
        (year_dir / "_ocr_answers.txt").write_text(extract_text(PDF_ANSWER[year]), encoding="utf-8")
        (year_dir / "_rapidocr_questions.txt").write_text(
            ocr_png_dir(images_dir / "source_pages"),
            encoding="utf-8",
        )
        (year_dir / "_rapidocr_answers.txt").write_text(
            ocr_png_dir(images_dir / "answer_pages"),
            encoding="utf-8",
        )
        (year_dir / "_render_manifest.json").write_text(
            json.dumps(
                {
                    "year": year,
                    "question_pdf": str(PDF_QUESTION[year]),
                    "answer_pdf": str(PDF_ANSWER[year]),
                    "source_pages": source_meta,
                    "answer_pages": answer_meta,
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
        summary.append(
            {
                "year": year,
                "source_pages": len(source_meta),
                "answer_pages": len(answer_meta),
            }
        )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
