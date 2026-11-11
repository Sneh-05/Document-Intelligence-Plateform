import faiss
import numpy as np

# In-memory store to keep chunks paired with their index positions
_chunks: list[str] = []
_index: faiss.IndexFlatL2 | None = None

def build_index(chunks: list[str], embeddings: list[list[float]]) -> None:
    """
    Builds a FAISS index from the given chunks and their embeddings.

    Args:
        chunks: The original text chunks.
        embeddings: Corresponding embedding vectors.
    """
    global _chunks, _index

    vectors = np.array(embeddings, dtype=np.float32)
    dimension = vectors.shape[1]  # 384 for all-MiniLM-L6-v2

    _index = faiss.IndexFlatL2(dimension)  # L2 = Euclidean distance
    _index.add(vectors)
    _chunks = chunks

def search(query_embedding: list[float], top_k: int = 5) -> list[dict]:
    """
    Searches the FAISS index for the most similar chunks.

    Args:
        query_embedding: The embedding of the user's query.
        top_k: Number of top results to return.

    Returns:
        List of dicts with 'chunk' and 'score' keys.
    """
    if _index is None:
        raise ValueError("Index has not been built yet. Call build_index() first.")

    query_vector = np.array([query_embedding], dtype=np.float32)
    distances, indices = _index.search(query_vector, top_k)

    results = []
    for dist, idx in zip(distances[0], indices[0]):
        if idx == -1:  # FAISS returns -1 when there aren't enough results
            continue
        results.append({
            "chunk": _chunks[idx],
            "score": float(dist)  # lower score = more similar in L2
        })

    return results
