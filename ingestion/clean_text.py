from pathlib import Path
from bs4 import BeautifulSoup
import re

RAW_FILE = Path("data/raw/microsoft_10k.html")
OUTPUT_DIR = Path("data/processed")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "microsoft_10k.txt"
html = RAW_FILE.read_text(encoding="utf-8", errors="ignore")
soup = BeautifulSoup(html, "html.parser")

for tag in soup(["script", "style", "noscript", "svg"]):
    tag.decompose()
text = soup.get_text(separator="\n")
text = re.sub(r"\n\s*\n+", "\n\n", text)
text = re.sub(r"[ \t]+", " ", text)

OUTPUT_FILE.write_text(text.strip(), encoding="utf-8")
print(f"Saved cleaned text to: {OUTPUT_FILE}")
print(f"Total characters: {len(text):,}")