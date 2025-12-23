import json
import os
import pickle
import faiss
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
import numpy as np

CHUNKS_PATH = r"E:\llm_with_rag\data\chunks\prml_chunks_clean.json"
VECTOR_DIR = r"E:\llm_with_rag\data\vectorstore"

def main():
    os.makedirs(VECTOR_DIR, exist_ok=True)

    print("🔹 Loading chunks...")
    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    texts = [c["text"] for c in chunks]

    print("🔹 Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    print("🔹 Creating embeddings...")
    embeddings = model.encode(
        texts,
        batch_size=32,
        show_progress_bar=True,
        normalize_embeddings=True
    )

    embeddings = np.array(embeddings).astype("float32")

    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)  # cosine similarity
    index.add(embeddings)

    print("🔹 Saving FAISS index...")
    faiss.write_index(index, os.path.join(VECTOR_DIR, "faiss.index"))

    print("🔹 Saving metadata...")
    with open(os.path.join(VECTOR_DIR, "metadata.pkl"), "wb") as f:
        pickle.dump(chunks, f)

    print("\n✅ FAISS vector store created successfully")
    print(f"📦 Total vectors: {index.ntotal}")
    print(f"📁 Saved in: {VECTOR_DIR}")

if __name__ == "__main__":
    main()
