
from app.services.chunker import chunk_text
from app.services.embedder import generate_embeddings
from app.services.vector_store import build_index, search
from app.services.llm import generate_answer



# 1. PROCESS AND INDEX DOCUMENT


def index_document(text: str) -> dict:
    """
    Process document text and build its FAISS index.

    Pipeline:
    Text -> Chunks -> Embeddings -> FAISS Index
    """

    if not text or not text.strip():
        raise ValueError("Document text cannot be empty.")

    # Step 1: Split text into chunks
    chunks = chunk_text(text)

    if not chunks:
        raise ValueError("No meaningful text chunks were generated.")

    # Step 2: Generate embeddings for chunks
    embeddings = generate_embeddings(chunks)

    if not embeddings:
        raise ValueError("Could not generate document embeddings.")

    # Step 3: Build FAISS index
    build_index(chunks, embeddings)

    return {
        "chunks_created": len(chunks),
        "embedding_dimension": len(embeddings[0]),
        "status": "indexed"
    }



# 2. ANSWER USER QUESTION


def ask_question(
    question: str,
    top_k: int = 5
) -> dict:
    """
    Retrieve relevant document chunks and generate
    an answer using the configured LLM.
    """

    if not question or not question.strip():
        raise ValueError("Question cannot be empty.")

    # Step 1: Generate embedding for the question
    query_embedding = generate_embeddings([question])[0]

    # Step 2: Retrieve relevant chunks from FAISS
    retrieved_results = search(
        query_embedding,
        top_k=top_k
    )

    if not retrieved_results:
        return {
            "answer": "I could not find relevant information in the document.",
            "sources": []
        }

    # Step 3: Extract text from retrieved results
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
