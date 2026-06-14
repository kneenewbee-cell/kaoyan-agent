import sys
import fitz

doc = fitz.open(r"e:\桌面\s41746-024-01339-7.pdf")
start = int(sys.argv[1]) if len(sys.argv) > 1 else 1
end = int(sys.argv[2]) if len(sys.argv) > 2 else len(doc)
for i in range(start, end + 1):
    page = doc[i - 1]
    text = page.get_text()
    print(f"===== PAGE {i} LEN {len(text)} =====")
    print(text)
