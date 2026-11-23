"""
NEXOR - Backend API Client Module
Consolidates all FastAPI endpoints and communications into a clean, typed interface.
"""

import os
import time
from typing import Any, Dict, List, Optional
import requests


BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")


def check_backend() -> Dict[str, Any]:
    """Check health, connectivity, and latency of the FastAPI backend."""
    start_time = time.time()
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=4)
        latency = (time.time() - start_time) * 1000
        if response.status_code == 200:
            data = response.json()
            return {
                "online": True,
                "latency_ms": round(latency, 1),
                "application": data.get("application", "NEXOR"),
                "database": data.get("database", "connected"),
                "status": data.get("status", "healthy")
            }
    except requests.RequestException:
        pass

    return {
        "online": False,
        "latency_ms": 0,
        "application": "NEXOR",
        "database": "disconnected",
        "status": "offline"
    }


def get_documents() -> List[Dict[str, Any]]:
    """Fetch all document records from the backend database."""
    try:
        response = requests.get(f"{BACKEND_URL}/documents", timeout=10)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list):
            return data
        if isinstance(data, dict):
            return data.get("documents", [])
        return []
    except requests.RequestException:
        return []


def get_document_id(doc: Dict[str, Any]) -> Any:
    """Helper to extract document ID from document metadata dict."""
    return doc.get("document_id", doc.get("id"))


def get_document_name(doc: Dict[str, Any]) -> str:
    """Helper to extract readable document name."""
    return (
        doc.get("title")
        or doc.get("filename")
        or doc.get("file_name")
        or "Untitled Document"
    )


def format_file_size(size_bytes: Optional[int]) -> str:
    """Format file size in bytes to human-readable string."""
    if size_bytes is None or size_bytes < 0:
        return "N/A"
    if size_bytes < 1024:
        return f"{size_bytes} B"
    if size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    return f"{size_bytes / (1024 * 1024):.2f} MB"


def upload_and_index(file) -> Dict[str, Any]:
    """
    Step 1: Upload document to /upload (extracts text and stores file).
    Step 2: Index extracted text to /documents/{id}/index (FAISS vector store).
    """
    try:
        file_bytes = file.getvalue()
        files = {
            "file": (
                file.name,
                file_bytes,
                file.type or "application/octet-stream"
            )
        }

        # Step 1: Upload and extract
        upload_resp = requests.post(
            f"{BACKEND_URL}/upload",
            files=files,
            timeout=120
        )
        upload_resp.raise_for_status()
        upload_data = upload_resp.json()

        document_id = upload_data.get("document_id")
        extracted_text = upload_data.get("extracted_text", "")
        file_size = upload_data.get("file_size", len(file_bytes))

        if document_id is None:
            raise ValueError("Backend did not return a valid document ID.")

        if not extracted_text or not extracted_text.strip():
            raise ValueError("No readable text could be extracted from this document.")

        # Step 2: Index text into FAISS
        index_resp = requests.post(
            f"{BACKEND_URL}/documents/{document_id}/index",
            json={"text": extracted_text},
            timeout=180
        )
        index_resp.raise_for_status()
        index_data = index_resp.json()

        return {
            "success": True,
            "document_id": document_id,
            "filename": file.name,
            "file_size": file_size,
            "extracted_text_length": len(extracted_text),
            "chunks_created": index_data.get("chunks_created", 0),
            "embedding_dimension": index_data.get("embedding_dimension", 0),
            "message": index_data.get("message", "Document uploaded and indexed successfully.")
        }

    except requests.HTTPError as error:
        detail = "Backend request failed."
        if error.response is not None:
            try:
                detail = error.response.json().get("detail", error.response.text)
            except Exception:
                detail = error.response.text
        return {"success": False, "filename": file.name, "error": detail}

    except Exception as error:
        return {"success": False, "filename": file.name, "error": str(error)}


def delete_document_api(document_id: Any) -> Dict[str, Any]:
    """Delete document from disk, SQLite, and FAISS index."""
    try:
        response = requests.delete(
            f"{BACKEND_URL}/documents/{document_id}",
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        return {
            "success": True,
            "message": data.get("message", "Document deleted successfully.")
        }
    except requests.HTTPError as error:
        message = "Unable to delete document."
        if error.response is not None:
            try:
                message = error.response.json().get("detail", error.response.text)
            except Exception:
                message = error.response.text
        return {"success": False, "message": message}
    except requests.RequestException as error:
        return {"success": False, "message": str(error)}


def ask_question(query: str, selected_documents: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    """Query documents using the RAG pipeline."""
    payload: Dict[str, Any] = {"query": query.strip()}

    if selected_documents:
        doc_ids = [
            get_document_id(doc)
            for doc in selected_documents
            if get_document_id(doc) is not None
        ]
        if len(doc_ids) == 1:
            payload["document_id"] = doc_ids[0]
        elif len(doc_ids) > 1:
            payload["document_ids"] = doc_ids

    try:
        response = requests.post(
            f"{BACKEND_URL}/query",
            json=payload,
            timeout=180
        )
        response.raise_for_status()
        data = response.json()
        return {
            "success": True,
            "answer": data.get("answer", "No answer generated."),
            "sources": data.get("sources", []),
            "searched_document_ids": data.get("searched_document_ids", "All documents"),
            "question": query
        }
    except requests.HTTPError as error:
        detail = "Failed to generate answer."
        if error.response is not None:
            try:
                detail = error.response.json().get("detail", error.response.text)
            except Exception:
                detail = error.response.text
        return {
            "success": False,
            "error": detail,
            "answer": None,
            "sources": []
        }
    except requests.RequestException as error:
        return {
            "success": False,
            "error": f"Backend connection error: {error}",
            "answer": None,
            "sources": []
        }
