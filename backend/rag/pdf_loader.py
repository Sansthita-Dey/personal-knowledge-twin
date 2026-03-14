import os
from PyPDF2 import PdfReader

def load_pdfs(folder_path):

    texts = []

    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):

            reader = PdfReader(os.path.join(folder_path, file))

            for page in reader.pages:
                text = page.extract_text()

                if text:
                    texts.append(text)

    return texts