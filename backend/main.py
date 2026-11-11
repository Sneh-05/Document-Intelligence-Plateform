from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Literal
from contextlib import asynccontextmanager

from app.database.database import init_db, insert_document, get_all_documents, get_document_by_id
from app.services.embedder import generate_embeddings
from app.services.vector_store import build_index, search
from app.services.llm import generate_answer

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Runs once when the server starts — creates the DB table if it doesn't exist
    init_db()
    print("Database initialized.")
    yield

app = FastAPI(lifespan=lifespan)

# ─── Health & Root ───────────────────────────────────────────────────────────

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

# ─── Pydantic Schemas ─────────────────────────────────────────────────────────

class DocumentCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    file_type: Literal["pdf", "docx", "txt"]

class DocumentResponse(BaseModel):
    id: int
    title: str
    file_type: str
    status: str

class QueryRequest(BaseModel):
    document_id: int
    query: str = Field(min_length=5)

class QueryResponse(BaseModel):
    document_id: int
    query: str
    answer: str

# ─── Document Endpoints ───────────────────────────────────────────────────────

@app.get("/documents")
def get_documents():
    documents = get_all_documents()
    return {"documents": documents}

@app.get("/documents/{document_id}", response_model=DocumentResponse)
def get_document(document_id: int):
    document = get_document_by_id(document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document

@app.post("/documents", response_model=DocumentResponse, status_code=201)
def create_document(document: DocumentCreate):
    new_document = insert_document(
        title=document.title,
        file_type=document.file_type
    )
    return new_document

# ─── Query Endpoint (RAG Pipeline) ────────────────────────────────────────────

# In-memory store for document chunks/embeddings (keyed by document_id)
# This will be replaced by persistent storage in a later step
_document_chunks: dict[int, list[str]] = {}

@app.post("/documents/{document_id}/index")
def index_document(document_id: int, payload: dict):
    """
    Accepts extracted text for a document, chunks and indexes it.
    Expects: { "text": "full document text here" }
    This endpoint will be replaced once file upload is implemented.
    """
    document = get_document_by_id(document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    from app.services.chunker import chunk_text
    from app.database.database import update_document_status

    text = payload.get("text", "")
    if not text.strip():
        raise HTTPException(status_code=400, detail="No text provided")

    chunks = chunk_text(text)
    embeddings = generate_embeddings(chunks)
    build_index(chunks, embeddings)

    _document_chunks[document_id] = chunks
    update_document_status(document_id, "processed")

    return {
        "document_id": document_id,
        "chunks_created": len(chunks),
        "status": "indexed"
    }

@app.post("/query", response_model=QueryResponse)
def query_document(request: QueryRequest):
    """
    Accepts a question, retrieves relevant chunks from FAISS,
    and returns a Gemini-generated answer.
    """
    document = get_document_by_id(request.document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    if document["status"] != "processed":
        raise HTTPException(
            status_code=400,
            detail="Document has not been indexed yet. POST to /documents/{id}/index first."
        )

    query_embedding = generate_embeddings([request.query])[0]
    results = search(query_embedding, top_k=5)
    context_chunks = [r["chunk"] for r in results]

    answer = generate_answer(request.query, context_chunks)

    return {
        "document_id": request.document_id,
        "query": request.query,
        "answer": answer
    }
