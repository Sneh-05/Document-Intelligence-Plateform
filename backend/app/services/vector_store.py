
import faiss
import numpy as np

# In-memory storage for the MVP
_chunks: list[str] = []
_index: faiss.IndexFlatIP | None = None


def build_index(
    chunks: list[str],
    embeddings: list[list[float]]
) -> None:
    """
    Build a FAISS index using text chunks and their embeddings.
    """

    global _chunks, _index

    if not chunks or not embeddings:
        raise ValueError("Chunks and embeddings cannot be empty.")

    if len(chunks) != len(embeddings):
        raise ValueError("Number of chunks must match number of embeddings.")

    vectors = np.asarray(embeddings, dtype=np.float32)

    if vectors.ndim != 2:
        raise ValueError("Embeddings must be a 2D array.")

    if vectors.shape[0] != len(chunks) or vectors.shape[1] == 0:
        raise ValueError("Invalid embedding dimensions.")

    if not np.isfinite(vectors).all():
        raise ValueError("Embeddings contain invalid numerical values.")

    # Create FAISS inner-product index
    dimension = vectors.shape[1]

    new_index = faiss.IndexFlatIP(dimension)
    new_index.add(vectors)

    _chunks = chunks.copy()
    _index = new_index


def search(
    query_embedding: list[float],
    top_k: int = 5
) -> list[dict]:
    """
    Search for the most relevant chunks.

    Returns:
        List of dictionaries containing chunk and similarity score.
    """

    if _index is None:
        raise ValueError("FAISS index has not been built.")

    if top_k <= 0:
        raise ValueError("top_k must be greater than zero.")

    query_vector = np.asarray(query_embedding, dtype=np.float32)

    if query_vector.ndim != 1:
        raise ValueError("Query embedding must be a 1D vector.")

    if query_vector.shape[0] != _index.d:
        raise ValueError("Query embedding dimension does not match index.")

    if not np.isfinite(query_vector).all():
        raise ValueError("Query embedding contains invalid values.")

    query_vector = query_vector.reshape(1, -1)

    actual_k = min(top_k, len(_chunks))

    scores, indices = _index.search(query_vector, actual_k)

    results = []

    for score, idx in zip(scores[0], indices[0]):

        if idx == -1:
            continue

        results.append({
            "chunk": _chunks[idx],
            "score": float(score)
        })

    return results
