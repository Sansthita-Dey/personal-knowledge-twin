import os
import faiss
import pickle
import numpy as np
from utils.embedder import get_embedding

PROJECT_PATH = "."
CODE_EXTENSIONS = [".py"]

INDEX_FILE = "code_index.faiss"
CHUNKS_FILE = "code_chunks.pkl"

EXCLUDED_FOLDERS = {".venv", "__pycache__", ".git"}


def collect_code():

    code_blocks = []

    for root, dirs, files in os.walk(PROJECT_PATH):

        # remove excluded directories
        dirs[:] = [d for d in dirs if d not in EXCLUDED_FOLDERS]

        for file in files:

            if any(file.endswith(ext) for ext in CODE_EXTENSIONS):

                path = os.path.join(root, file)

                try:
                    with open(path, "r", encoding="utf-8") as f:

                        code = f.read()

                        if len(code.strip()) > 0:
                            code_blocks.append(code)

                except:
                    continue

    return code_blocks


code_blocks = collect_code()

print(f"Indexing {len(code_blocks)} project code files...")

embeddings = []

valid_chunks = []

for code in code_blocks:

    try:
        emb = get_embedding(code[:2000])

        embeddings.append(emb)

        valid_chunks.append(code)

    except:
        continue


embeddings = np.array(embeddings).astype("float32")

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embeddings)

faiss.write_index(index, INDEX_FILE)

with open(CHUNKS_FILE, "wb") as f:
    pickle.dump(valid_chunks, f)

print("Code index built successfully.")