import fitz  # PyMuPDF
import json
import os
import re
from tqdm import tqdm

PDF_PATH = r"E:\llm_with_rag\data\book.pdf"
OUTPUT_PATH = r"E:\llm_with_rag\data\parsed\prml_pages.json"

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = text.replace('\u00a0', ' ')
    return text.strip()

def extract_pdf():
    doc = fitz.open(PDF_PATH)
    all_pages = []

    for page_num in tqdm(range(len(doc)), desc="Extracting PRML pages"):
        page = doc[page_num]
        text = page.get_text("text")

        if not text.strip():
            continue

        text = clean_text(text)

        # Heuristic: detect math-heavy pages
        math_density = sum(text.count(sym) for sym in ["=", "∑", "∫", "θ", "λ", "μ", "σ"])

        page_data = {
            "page": page_num + 1,
            "text": text,
            "math_density": math_density
        }

        all_pages.append(page_data)

    return all_pages

def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    pages = extract_pdf()

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(pages, f, indent=2)

    print(f"\n✅ Extraction complete")
    print(f"📄 Pages processed: {len(pages)}")
    print(f"💾 Saved to: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
