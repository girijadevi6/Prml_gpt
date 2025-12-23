import os
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

VECTOR_DIR = r"E:\llm_with_rag\data\vectorstore"
TOP_K = 5  # number of chunks to retrieve

# -----------------------------
# Load FAISS + metadata
# -----------------------------
print("🔹 Loading FAISS index and metadata...")
index = faiss.read_index(os.path.join(VECTOR_DIR, "faiss.index"))
with open(os.path.join(VECTOR_DIR, "metadata.pkl"), "rb") as f:
    chunks = pickle.load(f)
print("✅ FAISS index and metadata loaded!")

# Load embeddings
embed_model = SentenceTransformer("all-MiniLM-L6-v2")
print("✅ Embedding model loaded!")

# Load GPT-2 small (CPU-friendly)
print("🔹 Loading LLM (GPT-2 small)...")
tokenizer = AutoTokenizer.from_pretrained("gpt2")
model = AutoModelForCausalLM.from_pretrained("gpt2")
generator = pipeline("text-generation", model=model, tokenizer=tokenizer, device=-1)
print("✅ LLM loaded!")

# -----------------------------
# Helper functions
# -----------------------------
def retrieve_chunks(question, top_k=TOP_K):
    q_vec = embed_model.encode([question], normalize_embeddings=True)
    q_vec = np.array(q_vec).astype("float32")
    D, I = index.search(q_vec, top_k)
    retrieved = [chunks[i] for i in I[0]]
    return retrieved

def generate_answer(question, top_k=TOP_K):
    retrieved = retrieve_chunks(question, top_k)
    if not retrieved:
        return "❌ No relevant text found in the dataset."

    answers = []
    for chunk in retrieved:
        # Truncate each chunk to GPT-2 max tokens
        encoded = tokenizer(chunk["text"], return_tensors="pt", truncation=True, max_length=1024)
        truncated_text = tokenizer.decode(encoded["input_ids"][0])

        prompt = (
            f"You are a helpful assistant. Use ONLY the following text to answer the question.\n"
            f"Include explanations and equations if present.\n\n"
            f"Context:\n{truncated_text}\n\n"
            f"Question: {question}\nAnswer:"
        )

        output = generator(
            prompt,
            max_new_tokens=150,
            do_sample=False,          # greedy decoding
            repetition_penalty=2.0,   # reduce repetition
            pad_token_id=tokenizer.eos_token_id
        )[0]["generated_text"]

        ans = output.split("Answer:")[-1].strip()
        answers.append(ans)

    # Combine all chunk answers
    full_answer = " ".join(answers)

    # Remove repeated lines
    lines = full_answer.split("\n")
    filtered_lines = []
    seen = set()
    for line in lines:
        if line.strip() and line not in seen:
            filtered_lines.append(line)
            seen.add(line)
    return "\n".join(filtered_lines)

def export_word(text, filename):
    doc = Document()
    doc.add_paragraph(text)
    doc.save(filename)
    print(f"📄 Saved Word: {filename}")

def export_pdf(text, filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    lines = text.split("\n")
    y = height - 40
    for line in lines:
        c.drawString(40, y, line)
        y -= 14
        if y < 40:
            c.showPage()
            y = height - 40
    c.save()
    print(f"📄 Saved PDF: {filename}")

# -----------------------------
# Interactive loop
# -----------------------------
def main():
    print("\n🧠 PRML QA System Ready! Type 'exit' to quit.")
    while True:
        query = input("\nEnter your question: ").strip()
        if query.lower() == "exit":
            break

        answer = generate_answer(query)
        print("\n" + "="*50)
        print("📝 Generated Answer:\n")
        print(answer)
        print("="*50)

        # Optional export
        export_choice = input("\nDo you want to export this answer? (yes/no): ").strip().lower()
        if export_choice == "yes":
            fmt = input("Enter format (word/pdf): ").strip().lower()
            fname = input("Enter filename (with extension): ").strip()
            if fmt == "word":
                export_word(answer, fname)
            elif fmt == "pdf":
                export_pdf(answer, fname)
            else:
                print("❌ Invalid format. Skipping export.")

if __name__ == "__main__":
    main()
