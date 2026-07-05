from __future__ import annotations

from pathlib import Path

from rapidocr_onnxruntime import RapidOCR


ROOT = Path(__file__).resolve().parents[1]
YEAR_DIR = ROOT / "data" / "raw" / "math" / "exam_papers" / "math3" / "2023"


def ocr_dir(subdir: str, out_name: str) -> None:
    engine = RapidOCR()
    out_parts: list[str] = []
    for image in sorted((YEAR_DIR / "images" / subdir).glob("*.png")):
        result, _ = engine(str(image))
        out_parts.append(f"\n\n===== {image.name} =====\n")
        if not result:
            continue
        for item in result:
            out_parts.append(item[1])
    (YEAR_DIR / out_name).write_text("\n".join(out_parts), encoding="utf-8", newline="\n")


def main() -> None:
    ocr_dir("source_pages", "_ocr_source.txt")
    ocr_dir("answer_pages", "_ocr_answers.txt")
    ocr_dir("eol_pages", "_ocr_eol.txt")


if __name__ == "__main__":
    main()
