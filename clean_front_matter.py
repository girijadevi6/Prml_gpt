import json
import re

INPUT_PATH = r"E:\llm_with_rag\data\chunks\prml_chunks.json"
OUTPUT_PATH = r"E:\llm_with_rag\data\chunks\prml_chunks_clean.json"

FRONT_MATTER_PATTERNS = [
    r"isbn",
    r"library of congress",
    r"springer",
    r"all rights reserved",
    r"printed in",
    r"series editors",
    r"preface",
    r"acknowledg",
    r"dedicated to",
    r"http://",
    r"www\."
]

def is_front_matter(chunk):
    text = chunk["text"].lower()

    # Rule 1: early pages
    if chunk["page_end"] < 10:
        return True

    # Rule 2: keyword match
    for pattern in FRONT_MATTER_PATTERNS:
        if re.search(pattern, text):
            return True

    return False

def main():
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    clean_chunks = []
    removed = 0

    for chunk in chunks:
        if is_front_matter(chunk):
            removed += 1
            continue
        clean_chunks.append(chunk)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(clean_chunks, f, indent=2)

    print("✅ Front matter removal complete")
    print(f"🗑️ Chunks removed: {removed}")
    print(f"📦 Clean chunks remaining: {len(clean_chunks)}")
    print(f"💾 Saved to: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
