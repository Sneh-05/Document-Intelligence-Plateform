from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Literal
from fastapi import UploadFile, File
from fastapi import HTTPException
from uuid import uuid4

import os


app = FastAPI()


@app.get("/")      #root endpoint
def home():
    return {
        "message": "Welcome to NEXOR",
        "project": "Document Intelligence Platform",
        "status": "Running"
    }

@app.get("/health")           #a way to check whether their backend application is running
def health_check():
    return {
        "status": "healthy",
        "application": "NEXOR"
    }

@app.get("/documents")       #this endpoint will retrieve actual document records from our database
def get_documents():
    return {
        "documents": []
    }

class DocumentCreate(BaseModel):  #This pydantic model defines what the API accepts. 
    title: str = Field(min_length=3, max_length=100)  #Adds validation rules
    file_type: Literal["pdf", "docx", "txt"]

class DocumentResponse(BaseModel): #This pydantic model defines what the API returns.
    id: int
    title: str
    file_type: str
    status: str


documents = []

@app.post("/documents",response_model=DocumentResponse,status_code=201)
def create_document(document: DocumentCreate):

    new_document = {
        "id": len(documents) + 1,
        "title": document.title,
        "file_type": document.file_type,
        "status": "uploaded",
        "internal_note": "This is a private backend field"  #will not be seen in the output 
    }

    documents.append(new_document)
    return new_document


UPLOAD_DIR = "../uploaded_documents"

os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


@app.post("/upload", status_code=201)
async def upload_document(file: UploadFile = File(...)):

    # 1. Validate filename
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is missing"
        )

    # 2. Extract and validate extension
    safe_filename = os.path.basename(
        file.filename.replace("\\", "/")
    )

    _, extension = os.path.splitext(safe_filename) #Separates the filename and extension.

    extension = extension.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=415,
            detail="Only PDF, DOCX and TXT files are allowed"
        )

    # 3. Generate unique filename
    stored_filename = f"{uuid4().hex}{extension}"

    file_path = os.path.join(
        UPLOAD_DIR,
        stored_filename
    )

    # 4. Save file in chunks and validate size
    file_size = 0
    chunk_size = 1024 * 1024  # 1 MB

    try:
        with open(file_path, "wb") as buffer:

            while True:

                chunk = await file.read(chunk_size)

                if not chunk:
                    break

                file_size += len(chunk)

                if file_size > MAX_FILE_SIZE:
                    raise HTTPException(
                        status_code=413,
                        detail="File size exceeds the 10 MB limit"
                    )

                buffer.write(chunk)

        # 5. Reject empty files
        if file_size == 0:
            raise HTTPException(
                status_code=400,
                detail="Empty files are not allowed"
            )

    except Exception:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise

    finally:
        await file.close()

    return {
        "filename": safe_filename,
        "stored_filename": stored_filename,
        "file_size": file_size,
        "message": "File uploaded successfully"
    }
