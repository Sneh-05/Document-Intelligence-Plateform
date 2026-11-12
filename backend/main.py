
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel, Field
from typing import Literal
from uuid import uuid4
from pathlib import Path

from app.services.vector_store import remove_document_from_index
from app.document_processor import extract_text
from app.services.rag_pipeline import index_document, ask_question

from app.database.database import (
    init_db,
    insert_document,
    get_all_documents,
    get_document_by_id,
    update_document_status,
    delete_document
)

import os



# APPLICATION CONFIGURATION


app = FastAPI(
    title="NEXOR - Document Intelligence Platform",
    description="Upload, process and query documents using AI-powered RAG.",
    version="1.0.0"
)

# Initialize SQLite database
init_db()



# REQUEST AND RESPONSE SCHEMAS


class DocumentCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    file_type: Literal["pdf", "docx", "txt"]


class DocumentResponse(BaseModel):
    id: int
    title: str
    file_type: str
    status: str


class IndexRequest(BaseModel):
    text: str = Field(min_length=1)


class QueryRequest(BaseModel):
    query: str = Field(min_length=1, max_length=2000)
    document_id: int | None = None
    document_ids: list[int] | None = None



# HOME AND HEALTH ROUTES


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
        "application": "NEXOR",
        "database": "connected"
    }


# DOCUMENT METADATA ROUTES


@app.get("/documents")
def get_documents():

    all_documents = get_all_documents()

    public_documents = [
        {
            "id": doc["id"],
            "title": doc["title"],
            "file_type": doc["file_type"],
            "status": doc["status"],
            "created_at": doc["created_at"]
        }
        for doc in all_documents
    ]

    return {
        "documents": public_documents
    }


@app.delete("/documents/{document_id}")
def delete_uploaded_document(document_id: int):

    # Step 1: Find the document in SQLite
    document = get_document_by_id(document_id)

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )

    try:
        # Step 2: Validate and delete the physical file
        file_path = document.get("file_path")

        if file_path:
            upload_directory = Path(UPLOAD_DIR).resolve()
            stored_file = Path(file_path).resolve()

            # Prevent deletion outside the upload directory
            if not stored_file.is_relative_to(upload_directory):
                raise HTTPException(
                    status_code=400,
                    detail="Invalid document file path."
                )

            if stored_file.exists():
                stored_file.unlink()

        # Step 3: Remove document chunks and embeddings from FAISS
        remove_document_from_index(str(document_id))

        # Step 4: Delete document metadata from SQLite
        deleted_document = delete_document(document_id)

        if deleted_document is None:
            raise HTTPException(
                status_code=404,
                detail="Document not found."
            )

        return {
            "document_id": document_id,
            "filename": document["title"],
            "status": "deleted",
            "message": "Document and its indexed data deleted successfully."
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while deleting the document."
        ) from error

@app.post(
    "/documents",
    response_model=DocumentResponse,
    status_code=201
)
def create_document(document: DocumentCreate):

    try:
        new_document = insert_document(
            title=document.title,
            file_type=document.file_type
        )

        return new_document

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail="Could not register document."
        ) from error


# DOCUMENT INDEXING ROUTE


@app.post("/documents/{document_id}/index")
def index_uploaded_document(
    document_id: int,
    request: IndexRequest
):

    document = get_document_by_id(document_id)

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )

    try:
        result = index_document(
            document_id=str(document_id),
            text=request.text
        )

        update_document_status(
            document_id,
            "processed"
        )

        return {
            "document_id": document_id,
            "chunks_created": result["chunks_created"],
            "embedding_dimension": result["embedding_dimension"],
            "status": "indexed",
            "message": "Document indexed successfully."
        }

    except ValueError as error:

        update_document_status(document_id, "failed")

        raise HTTPException(
            status_code=422,
            detail=str(error)
        ) from error

    except Exception as error:

        update_document_status(document_id, "failed")

        raise HTTPException(
            status_code=500,
            detail="Document indexing failed."
        ) from error



# MULTI-DOCUMENT QUESTION-ANSWERING ROUTE


@app.post("/query")
def query_documents(request: QueryRequest):

    if (
        request.document_id is not None
        and request.document_ids is not None
    ):
        raise HTTPException(
            status_code=422,
            detail="Provide either document_id or document_ids, not both."
        )

    selected_ids = None

    if request.document_id is not None:
        selected_ids = [request.document_id]

    elif request.document_ids is not None:
        selected_ids = request.document_ids

    # Validate selected document IDs
    if selected_ids is not None:

        if not selected_ids:
            raise HTTPException(
                status_code=422,
                detail="At least one document ID is required."
            )

        if len(selected_ids) != len(set(selected_ids)):
            raise HTTPException(
                status_code=422,
                detail="Duplicate document IDs are not allowed."
            )

        for doc_id in selected_ids:

            document = get_document_by_id(doc_id)

            if document is None:
                raise HTTPException(
                    status_code=404,
                    detail=f"Document {doc_id} not found."
                )

            if document["status"] != "processed":
                raise HTTPException(
                    status_code=409,
                    detail=f"Document {doc_id} has not been indexed."
                )

    try:
        result = ask_question(
            question=request.query,
            document_ids=(
                [str(doc_id) for doc_id in selected_ids]
                if selected_ids is not None
                else None
            )
        )

        return {
            "question": request.query,
            "searched_document_ids": (
                selected_ids if selected_ids is not None
                else "all indexed documents"
            ),
            "answer": result["answer"],
            "sources": result["sources"]
        }

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        ) from error

    except RuntimeError as error:

        raise HTTPException(
            status_code=502,
            detail=str(error)
        ) from error

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while generating the answer."
        ) from error



# FILE UPLOAD CONFIGURATION


BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

UPLOAD_DIR = os.path.join(
    BASE_DIR,
    "uploaded_documents"
)

os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}

MAX_FILE_SIZE = 10 * 1024 * 1024



# DOCUMENT UPLOAD AND TEXT EXTRACTION


@app.post("/upload", status_code=201)
async def upload_document(file: UploadFile = File(...)):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is missing."
        )

    safe_filename = os.path.basename(
        file.filename.replace("\\", "/")
    )

    _, extension = os.path.splitext(safe_filename)
    extension = extension.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=415,
            detail="Only PDF, DOCX and TXT files are allowed."
        )

    stored_filename = f"{uuid4().hex}{extension}"

    file_path = os.path.join(
        UPLOAD_DIR,
        stored_filename
    )

    file_size = 0
    chunk_size = 1024 * 1024

    try:

        # Save uploaded file
        with open(file_path, "wb") as buffer:

            while True:

                chunk = await file.read(chunk_size)

                if not chunk:
                    break

                file_size += len(chunk)

                if file_size > MAX_FILE_SIZE:
                    raise HTTPException(
                        status_code=413,
                        detail="File size exceeds the 10 MB limit."
                    )

                buffer.write(chunk)

        if file_size == 0:
            raise HTTPException(
                status_code=400,
                detail="Empty files are not allowed."
            )

        # Extract document text
        extracted_text = extract_text(file_path)

        if not extracted_text or not extracted_text.strip():
            raise HTTPException(
                status_code=422,
                detail="No readable text found in the document."
            )

        # Store document metadata in SQLite
        new_document = insert_document(
            title=safe_filename,
            file_type=extension.lstrip("."),
            file_path=file_path
        )

    except HTTPException:

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

    except RuntimeError as error:

        if os.path.exists(file_path):
            os.remove(file_path)

        raise HTTPException(
            status_code=422,
            detail="The document could not be processed."
        ) from error

    except Exception as error:

        if os.path.exists(file_path):
            os.remove(file_path)

        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while uploading or processing the document."
        ) from error

    finally:
        await file.close()

    return {
        "document_id": new_document["id"],
        "filename": safe_filename,
        "stored_filename": stored_filename,
        "file_size": file_size,
        "extracted_text_length": len(extracted_text),
        "extracted_text": extracted_text,
        "status": "uploaded",
        "message": "Document uploaded, extracted and saved successfully."
    }
