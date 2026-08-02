import json
import re
from pathlib import Path

INPUT_FILE = Path("data/processed/microsoft_10k.txt")
OUTPUT_FILE = Path("data/processed/chunks.json")

COMPANY = "Microsoft"
FILING_YEAR = 2026
FILING_TYPE = "10-K"

CHUNK_SIZE = 500
OVERLAP = 50
MIN_WORDS = 20

text = INPUT_FILE.read_text(encoding="utf-8")
lines = text.split("\n")

sections = []
current_section = "INTRODUCTION"
current_lines = []

item_pattern = re.compile(
    r"^ITEM\s+\d+[A-Z]?\.",
    re.IGNORECASE
)

for line in lines:
    if item_pattern.match(line):
        if current_lines:
            sections.append({
                "section": current_section,
                "text": "\n".join(current_lines)
            })
        current_section = line
        current_lines = []
    else:
        current_lines.append(line)

if current_lines:
    sections.append({
        "section": current_section,
        "text": "\n".join(current_lines)
    })

chunks = []
chunk_id = 0

for section in sections:
    words = section["text"].split()
    start = 0

    while start < len(words):
        end = min(start + CHUNK_SIZE, len(words))
        chunk_text = " ".join(words[start:end])
        word_count = len(chunk_text.split())

        if word_count >= MIN_WORDS:
            chunks.append({
                "chunk_id": chunk_id,
                "company": COMPANY,
                "filing_year": FILING_YEAR,
                "filing_type": FILING_TYPE,
                "section": section["section"],
                "text": chunk_text,
                "word_count": word_count
            })
            chunk_id += 1

        start += CHUNK_SIZE - OVERLAP

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:
    json.dump(
        chunks,
        f,
        indent=2,
        ensure_ascii=False
    )

word_counts = [chunk["word_count"] for chunk in chunks]

print(f"Sections found : {len(sections)}")
print(f"Chunks created : {len(chunks)}")
print(f"Min words      : {min(word_counts)}")
print(f"Max words      : {max(word_counts)}")
print(f"Average words  : {sum(word_counts) / len(word_counts):.1f}")
print(f"Saved to       : {OUTPUT_FILE}")