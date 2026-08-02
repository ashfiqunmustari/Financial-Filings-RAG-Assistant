from pathlib import Path
import re
import trafilatura

INPUT_FILE = Path("data/raw/microsoft_10k.html")
OUTPUT_DIR = Path("data/processed")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "microsoft_10k.txt"
html = INPUT_FILE.read_text(
    encoding="utf-8",
    errors="ignore"
)

text = trafilatura.extract(
    html,
    include_comments=False,
    include_tables=False,
    favor_precision=True
)

if text is None:
    raise Exception("Text extraction failed.")

text = text.replace("\r", "")
start = text.find("UNITED STATES")
if start != -1:
    text = text[start:]
filtered_lines = []
for line in text.split("\n"):
    line = line.strip()
    if not line:
        continue
    if re.match(r"^ITEM\s+\d+[A-Z]?\.", line, re.IGNORECASE):
        filtered_lines.append(line)
        continue

    if (
        line.isupper()
        and len(re.findall(r"[A-Za-z]{2,}", line)) >= 2
    ):
        filtered_lines.append(line)
        continue

    if (
        len(line) < 80
        and line == line.title()
        and len(re.findall(r"[A-Za-z]{2,}", line)) >= 2
    ):
        filtered_lines.append(line)
        continue

    word_count = len(re.findall(r"[A-Za-z]{2,}", line))

    if word_count >= 3:
        filtered_lines.append(line)

text = "\n".join(filtered_lines)
text = re.sub(r"\n{3,}", "\n\n", text)

OUTPUT_FILE.write_text(
    text,
    encoding="utf-8"
)
print(f"Saved to {OUTPUT_FILE}")
print(f"Characters: {len(text):,}")
print(f"Lines kept: {len(filtered_lines):,}")