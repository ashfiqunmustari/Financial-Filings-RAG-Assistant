import requests
from pathlib import Path
CIK = "0000789019"  # Microsoft
HEADERS = {
    "User-Agent": "Financial-RAG/1.0 asfiqunishaa@gmail.com"
}

SAVE_DIR = Path("data/raw")
SAVE_DIR.mkdir(parents=True, exist_ok=True)

# Get submission metadata
url = f"https://data.sec.gov/submissions/CIK{CIK}.json"
response = requests.get(url, headers=HEADERS)
response.raise_for_status()
data = response.json()
recent = data["filings"]["recent"]
forms = recent["form"]
accessions = recent["accessionNumber"]
documents = recent["primaryDocument"]
tenk = None
for form, accession, document in zip(forms, accessions, documents):
    if form == "10-K":
        tenk = {
            "accession": accession,
            "document": document
        }
        break

if tenk is None:
    raise Exception("No 10-K found.")
print("Latest 10-K found:")
print(tenk)
accession_no_dash = tenk["accession"].replace("-", "")

filing_url = (
    f"https://www.sec.gov/Archives/edgar/data/"
    f"{int(CIK)}/"
    f"{accession_no_dash}/"
    f"{tenk['document']}"
)

print(f"Downloading:\n{filing_url}")

filing = requests.get(
    filing_url,
    headers=HEADERS
)

filing.raise_for_status()

output_file = SAVE_DIR / "microsoft_10k.html"

output_file.write_text(
    filing.text,
    encoding="utf-8"
)

print(f"\nSaved to:\n{output_file}")