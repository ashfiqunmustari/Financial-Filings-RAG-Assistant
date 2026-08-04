import json
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

INDEX_FILE = Path("data/faiss/faiss.index")
METADATA_FILE = Path("data/faiss/metadata.json")

TOP_K = 3
RELEVANCE_THRESHOLD = 1.5

print("Loading FAISS index...")
index = faiss.read_index(str(INDEX_FILE))

print("Loading metadata...")
with open(METADATA_FILE, "r", encoding="utf-8") as f:
    chunks = json.load(f)

print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")


def retrieve(question, top_k=TOP_K):

    query_embedding = model.encode(
        [question],
        convert_to_numpy=True
    ).astype(np.float32)

    distances, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for distance, idx in zip(
        distances[0],
        indices[0]
    ):

        chunk = chunks[idx]

        results.append({
            "chunk_id": chunk["chunk_id"],
            "distance": float(distance),
            "company": chunk["company"],
            "section": chunk["section"],
            "text": chunk["text"]
        })
    results = [r for r in results if r["distance"] < RELEVANCE_THRESHOLD]
    return results


if __name__ == "__main__":

    while True:

        question = input("\nAsk a question (or type 'exit'): ")

        if question.lower() == "exit":
            break

        print("\nSearching...\n")

        results = retrieve(question)

        for rank, result in enumerate(results, start=1):

            print("=" * 80)
            print(f"Result #{rank}")
            print(f"Company   : {result['company']}")
            print(f"Section   : {result['section']}")
            print(f"Chunk ID  : {result['chunk_id']}")
            print(f"Distance  : {result['distance']:.4f}")
            print()

            preview = result["text"][:500]
            print(preview)

            if len(result["text"]) > 500:
                print("...")