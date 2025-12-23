import json
import os
import re
from tqdm import tqdm

INPUT_PATH = r"E:\llm_with_rag\data\parsed\prml_pages.json"
OUTPUT_PATH = r"E:\llm_with_rag\data\chunks\prml_chunks.json"

MAX_WORDS = 450   # safe for math + context
OVERLAP = 80      # prevents context loss

def split_into_chunks(text, max_words, overlap):
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = start + max_words
        chunk_words = words[start:end]
        chunks.append(" ".join(chunk_words))
        start += max_words - overlap

    return chunks

def main():
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        pages = json.load(f)

    chunks = []
    chunk_id = 0

    buffer_text = ""
    buffer_pages = []
    buffer_math = 0

    for page in tqdm(pages, desc="Creating math-aware chunks"):
        buffer_text += " " + page["text"]
        buffer_pages.append(page["page"])
        buffer_math += page["math_density"]

        # create chunk if math-heavy or long enough
        if buffer_math > 80 or len(buffer_text.split()) > MAX_WORDS:
            split_chunks = split_into_chunks(buffer_text, MAX_WORDS, OVERLAP)

            for c in split_chunks:
                chunks.append({
                    "chunk_id": chunk_id,
                    "text": c,
                    "page_start": buffer_pages[0],
                    "page_end": buffer_pages[-1],
                    "math_density": buffer_math
                })
                chunk_id += 1

            buffer_text = ""
            buffer_pages = []
            buffer_math = 0

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2)

    print(f"\n✅ Chunking complete")
    print(f"📦 Total chunks: {len(chunks)}")
    print(f"💾 Saved to: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
