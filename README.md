
# 📘 PRML Question Answering System (RAG)

## 📌 Project Overview

This project implements a **Retrieval-Augmented Question Answering (RAG) system** for the book **“Pattern Recognition and Machine Learning (PRML)”**.
The system allows users to ask natural-language questions related to PRML concepts and receive **context-aware, structured answers** derived directly from the book content.

The entire pipeline runs **locally**, without using any paid APIs or cloud-based large language models.

---

## 🧠 What We Did (Step-by-Step)

### 1️⃣ PDF Ingestion

The PRML textbook PDF was processed to extract text **page by page**.
This step converts the book into machine-readable text while preserving page structure for traceability.

---

### 2️⃣ Text Cleaning

Non-content sections such as:

* Preface
* Table of contents
* Index pages

were removed to ensure that only **relevant academic material** is used during question answering.

---

### 3️⃣ Text Chunking

The cleaned text was split into **small overlapping chunks**.
This improves:

* Retrieval accuracy
* Context relevance
* Model understanding

Each chunk represents a short, meaningful passage from the book.

---

### 4️⃣ Embedding Generation

Each text chunk was converted into a **dense vector representation** using a sentence-level embedding model.
These embeddings capture the **semantic meaning** of the text rather than just keywords.

---

### 5️⃣ Vector Storage with FAISS

All embeddings were stored in a **FAISS vector index**, enabling:

* Fast similarity search
* Efficient retrieval of the most relevant text chunks for a user query

---

### 6️⃣ Retrieval-Augmented Generation (RAG)

When a user asks a question:

1. The query is embedded
2. FAISS retrieves the most relevant chunks
3. Retrieved content is passed as **context** to a language model
4. The model generates an answer **strictly based on the retrieved text**

This prevents hallucination and ensures answers stay grounded in the PRML book.

---

### 7️⃣ Local Language Model Inference

A **lightweight local language model (GPT-2)** was used to generate answers.
Key benefits:

* No paid API usage
* Works fully offline
* CPU-friendly
* Suitable for academic demonstrations

---

### 8️⃣ Interactive Streamlit Interface

A user-friendly **Streamlit web application** was built with:

* Chat-style question input at the bottom
* Cleanly formatted answers
* Copy-friendly output
* Download options (PDF & Word)
* Optional display of retrieved source chunks

This makes the system easy to use for students and researchers.

---

## ✨ Key Features

* 📚 PRML-specific question answering
* 🔍 Context-aware retrieval using FAISS
* 🧠 Local inference (no OpenAI / paid APIs)
* 📄 Answer export (PDF & Word)
* 💬 Chat-like Streamlit UI
* 🎓 Academic-friendly, structured responses

---

## 🏗 Architecture Summary

```
PRML PDF
   ↓
Text Extraction
   ↓
Cleaning
   ↓
Chunking
   ↓
Embeddings
   ↓
FAISS Vector Store
   ↓
Query Retrieval
   ↓
Language Model
   ↓
Streamlit UI
```

---

## 🎯 Use Cases

* PRML exam preparation
* Concept clarification
* Quick reference for equations and explanations
* Academic demonstrations of RAG systems

---

## 📝 Notes

* The system is designed for **educational use**
* Easily extendable to larger models or other textbooks
* GPT-4 or other advanced models can be integrated later if desired


