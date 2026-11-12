
from app.services.chunker import chunk_text
from app.services.embedder import generate_embeddings
from app.services.vector_store import add_document_to_index, search
from app.services.llm import generate_answer


# 1. PROCESS AND INDEX DOCUMENT

def index_document(document_id: str, text: str) -> dict:
    """
    Process and add a document to the shared FAISS index.

    Pipeline:
    Text -> Chunks -> Embeddings -> FAISS Index
    """

    if not document_id:
        raise ValueError("Document ID cannot be empty.")

    if not text or not text.strip():
        raise ValueError("Document text cannot be empty.")

    # Step 1: Split document text into chunks
    chunks = chunk_text(text)

    if not chunks:
        raise ValueError("No meaningful text chunks were generated.")

    # Step 2: Generate embeddings
    embeddings = generate_embeddings(chunks)

    if not embeddings:
        raise ValueError("Could not generate document embeddings.")

    # Step 3: Add document to shared FAISS index
    add_document_to_index(
        document_id=document_id,
        chunks=chunks,
        embeddings=embeddings
    )

    return {
        "document_id": document_id,
        "chunks_created": len(chunks),
        "embedding_dimension": len(embeddings[0]),
        "status": "indexed"
    }


# 2. ANSWER USER QUESTION

def ask_question(
    question: str,
    top_k: int = 5,
    document_ids: list[str] | None = None
) -> dict:
    """
    Retrieve relevant chunks across all indexed documents
    and generate an answer using the configured LLM.

    If document_ids are supplied, search only those documents.
    """

    if not question or not question.strip():
        raise ValueError("Question cannot be empty.")

    # Step 1: Generate question embedding
    query_embedding = generate_embeddings([question])[0]

    # Step 2: Retrieve relevant chunks
    retrieved_results = search(
        query_embedding=query_embedding,
        top_k=top_k,
        document_ids=document_ids
    )

    if not retrieved_results:
        return {
            "answer": "I could not find relevant information in the indexed documents.",
            "sources": []
        }

    # Step 3: Extract retrieved text
    context_chunks = [
        result["chunk"]
        for result in retrieved_results
    ]

    # Step 4: Generate answer using Coforge LLM
    answer = generate_answer(
        question,
        context_chunks
    )

    return {
        "answer": answer,
        "sources": retrieved_results
    }