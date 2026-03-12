import os
from pypdf import PdfReader


def chunk_text(text, chunk_size=200, overlap=40):
    words = text.split()
    chunks = []

    step = chunk_size - overlap

    for i in range(0, len(words), step):
        chunk_words = words[i:i + chunk_size]
        chunk = " ".join(chunk_words)

        if chunk.strip():
            chunks.append(chunk)

    return chunks


def load_notes(folder="notes", chunk_size=200):

    documents = []

    for filename in os.listdir(folder):
        filepath = os.path.join(folder, filename)

        if not os.path.isfile(filepath):
            continue

        ext = filename.lower().split(".")[-1]
        text = ""

        # ---------- TXT / MD / PY ----------
        if ext in ["txt", "md", "py"]:
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()

        # ---------- PDF ----------
        elif ext == "pdf":
            reader = PdfReader(filepath)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

        if text:
            text = text.replace("\n", " ").strip()

            chunks = chunk_text(text, chunk_size=chunk_size)

            documents.extend(chunks)

    return documents