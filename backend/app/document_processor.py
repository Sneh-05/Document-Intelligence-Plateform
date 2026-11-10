import fitz
from docx import Document
from pathlib import Path


def extract_text(file_path: str) -> str:
    path = Path(file_path)
    extension = path.suffix.lower()

    if extension == ".pdf":
        pdf = fitz.open(file_path)
        text = ""

        for page in pdf:
            text += page.get_text()

        pdf.close()
        return text

    elif extension == ".docx":
        doc = Document(file_path)
        text = ""

        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"

        return text

    else:
        raise ValueError("Unsupported file format")