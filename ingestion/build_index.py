import json
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

INPUT_FILE = Path("data/processed/chunks.json")
OUTPUT_DIR = Path("data/faiss")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

INDEX_FILE = OUTPUT_DIR / "faiss.index"
METADATA_FILE = OUTPUT_DIR / "metadata.json"

print("Loading chunks...")

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    chunks = json.load(f)

texts = [chunk["text"] for chunk in chunks]

print(f"Loaded {len(texts)} chunks")

print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

print("Generating embeddings...")

embeddings = model.encode(
    texts,
    batch_size=32,
    show_progress_bar=True,
    convert_to_numpy=True
)

embeddings = embeddings.astype(np.float32)

dimension = embeddings.shape[1]

print(f"Embedding dimension: {dimension}")
print("Building FAISS index...")
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)
faiss.write_index(
    index,
    str(INDEX_FILE)
)
with open(
    METADATA_FILE,
    "w",
    encoding="utf-8"
) as f:
    json.dump(
        chunks,
        f,
        indent=2,
        ensure_ascii=False
    )
print(f"Vectors indexed : {index.ntotal}")
print(f"Saved index     : {INDEX_FILE}")
print(f"Saved metadata  : {METADATA_FILE}")