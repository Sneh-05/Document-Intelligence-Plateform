import pymupdf
from docx import Document
from pathlib import Path


def extract_text(file_path: str) -> str:
    """
    Extract text from PDF, DOCX, and TXT documents.

    Args:
        file_path: Path of the uploaded document.

    Returns:
        Extracted text as a string.

    Raises:
        FileNotFoundError: If the document does not exist.
        ValueError: If the file format is unsupported or no text is extracted.
        RuntimeError: If the document is corrupted or cannot be read.
    """

    path = Path(file_path)

    # 1. Check whether the file exists
    if not path.exists() or not path.is_file():
        raise FileNotFoundError(f"Document not found: {file_path}")

    # 2. Identify the file extension
    extension = path.suffix.lower()

    # 3. Extract text from PDF
    if extension == ".pdf":
        try:
            text_parts = []

            # Context manager automatically closes the PDF
            with pymupdf.open(path) as pdf:
                for page in pdf:
                    page_text = page.get_text()
                    if page_text.strip():
                        text_parts.append(page_text)

            extracted_text = "\n".join(text_parts)

        except Exception as error:
            raise RuntimeError(
                f"Unable to read PDF document: {error}"
            ) from error

    # 4. Extract text from DOCX
    elif extension == ".docx":
        try:
            doc = Document(path)
            text_parts = []

            # Extract text from paragraphs
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    text_parts.append(paragraph.text)

            # Extract text from tables
            for table in doc.tables:
                for row in table.rows:
                    row_text = " | ".join(
                        cell.text.strip() for cell in row.cells
                    )

                    if row_text.strip():
                        text_parts.append(row_text)

            extracted_text = "\n".join(text_parts)

        except Exception as error:
            raise RuntimeError(
                f"Unable to read DOCX document: {error}"
            ) from error

    # 5. Extract text from TXT
    elif extension == ".txt":
        try:
            extracted_text = path.read_text(
                encoding="utf-8",
                errors="replace"
            )

        except OSError as error:
            raise RuntimeError(
                f"Unable to read TXT document: {error}"
            ) from error

    # 6. Reject unsupported file formats
    else:
        raise ValueError(
            "Unsupported file format. Only PDF, DOCX and TXT are allowed."
        )

    # 7. Check whether any meaningful text was extracted
    if not extracted_text.strip():
        raise ValueError(
            "No extractable text found in the document."
        )

    return extracted_text
