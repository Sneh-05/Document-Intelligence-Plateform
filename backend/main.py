
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel, Field
from typing import Literal
from uuid import uuid4
from app.document_processor import extract_text

import os


app = FastAPI(
    title="NEXOR - Document Intelligence Platform",
    description="Upload and process documents using AI-powered document intelligence.",
    version="1.0.0"
)


# -------------------- HOME AND HEALTH ROUTES --------------------

@app.get("/")
def home():
    return {
        "message": "Welcome to NEXOR",
        "project": "Document Intelligence Platform",
        "status": "Running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": "NEXOR"
    }


# -------------------- DOCUMENT METADATA --------------------

@app.get("/documents")
def get_documents():
    return {
        "documents": []
    }


class DocumentCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    file_type: Literal["pdf", "docx", "txt"]


class DocumentResponse(BaseModel):
    id: int
    title: str
    file_type: str
    status: str


documents = []


@app.post(
    "/documents",
    response_model=DocumentResponse,
    status_code=201
)
def create_document(document: DocumentCreate):

    new_document = {
        "id": len(documents) + 1,
        "title": document.title,
        "file_type": document.file_type,
        "status": "uploaded",
        "internal_note": "This is a private backend field"
    }

    documents.append(new_document)

    return new_document


# -------------------- FILE UPLOAD CONFIGURATION --------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

UPLOAD_DIR = os.path.join(BASE_DIR, "uploaded_documents")

os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


# -------------------- DOCUMENT UPLOAD AND PROCESSING --------------------

@app.post("/upload", status_code=201)
async def upload_document(file: UploadFile = File(...)):

    # 1. Validate filename
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is missing"
        )

    safe_filename = os.path.basename(
        file.filename.replace("\\", "/")
    )

    _, extension = os.path.splitext(safe_filename)

    extension = extension.lower()

    # 2. Validate file extension
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=415,
            detail="Only PDF, DOCX and TXT files are allowed"
        )

    # 3. Generate a unique filename
    stored_filename = f"{uuid4().hex}{extension}"

    file_path = os.path.join(UPLOAD_DIR, stored_filename)

    file_size = 0
    chunk_size = 1024 * 1024  # 1 MB

    try:

        # 4. Save the uploaded file in chunks
        with open(file_path, "wb") as buffer:

            while True:

                chunk = await file.read(chunk_size)

                if not chunk:
                    break

                file_size += len(chunk)

                # 5. Validate maximum file size
                if file_size > MAX_FILE_SIZE:
                    raise HTTPException(
                        status_code=413,
                        detail="File size exceeds the 10 MB limit"
                    )

                buffer.write(chunk)

        # 6. Reject empty files
        if file_size == 0:
            raise HTTPException(
                status_code=400,
                detail="Empty files are not allowed"
            )

        # 7. Extract text from the saved document
        extracted_text = extract_text(file_path)

    except HTTPException:

        # Remove partially uploaded or invalid files
        if os.path.exists(file_path):
            os.remove(file_path)

        raise

    except ValueError as error:

        if os.path.exists(file_path):
            os.remove(file_path)

        raise HTTPException(
            status_code=422,
            detail=str(error)
        ) from error

    except RuntimeError:

        if os.path.exists(file_path):
            os.remove(file_path)

        raise HTTPException(
            status_code=422,
            detail="The document could not be processed. Please check whether it is valid."
        )

    except Exception as error:

        if os.path.exists(file_path):
            os.remove(file_path)

        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while uploading or processing the document."
        ) from error

    finally:
        await file.close()

    # 8. Return upload and extraction information
    return {
        "filename": safe_filename,
        "stored_filename": stored_filename,
        "file_size": file_size,
        "extracted_text_length": len(extracted_text),
        "status": "processed",
        "message": "Document uploaded and text extracted successfully"
    }
