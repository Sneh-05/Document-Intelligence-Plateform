
import faiss
import numpy as np


# In-memory storage for multiple documents
_chunks: list[str] = []
_document_ids: list[str] = []
_vectors: np.ndarray | None = None
_index: faiss.IndexFlatIP | None = None


def _rebuild_index() -> None:
    """Rebuild FAISS index using all currently stored vectors."""

    global _index

    if _vectors is None or len(_chunks) == 0:
        _index = None
        return

    dimension = _vectors.shape[1]

    _index = faiss.IndexFlatIP(dimension)
    _index.add(_vectors)


def add_document_to_index(
    document_id: str,
    chunks: list[str],
    embeddings: list[list[float]]
) -> None:
    """
    Add a document's chunks and embeddings to the existing FAISS index.

    If the document is already indexed, its previous vectors are replaced.
    """

    global _chunks, _document_ids, _vectors

    if not document_id:
        raise ValueError("Document ID cannot be empty.")

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

    if _vectors is not None and vectors.shape[1] != _vectors.shape[1]:
        raise ValueError("Embedding dimensions do not match existing index.")

    # Remove previous entries belonging to this document.
    keep_indices = [
        i for i, existing_id in enumerate(_document_ids)
        if existing_id != document_id
    ]

    if _vectors is not None:
        _vectors = _vectors[keep_indices]

    _chunks = [_chunks[i] for i in keep_indices]
    _document_ids = [_document_ids[i] for i in keep_indices]

    # Add new document data.
    _chunks.extend(chunks)
    _document_ids.extend([document_id] * len(chunks))

    if _vectors is None or len(_vectors) == 0:
        _vectors = vectors.copy()
    else:
        _vectors = np.vstack((_vectors, vectors))

    _rebuild_index()


def remove_document_from_index(document_id: str) -> bool:
    """
    Remove all chunks and embeddings belonging to a document.

    Returns True if the document was present in the index,
    otherwise returns False.
    """

    global _chunks, _document_ids, _vectors

    document_id = str(document_id)

    if document_id not in _document_ids:
        return False

    # Keep only entries belonging to other documents.
    keep_indices = [
        i for i, existing_id in enumerate(_document_ids)
        if existing_id != document_id
    ]

    _chunks = [_chunks[i] for i in keep_indices]
    _document_ids = [_document_ids[i] for i in keep_indices]

    if _vectors is not None:
        _vectors = _vectors[keep_indices]

    # If no documents remain, reset the vector storage.
    if not _chunks:
        _vectors = None

    # Rebuild FAISS with the remaining documents.
    _rebuild_index()

    return True


def build_index(
    chunks: list[str],
    embeddings: list[list[float]]
) -> None:
    """
    Backward-compatible wrapper for existing single-document calls.

    New code should use add_document_to_index().
    """

    add_document_to_index("default", chunks, embeddings)


def search(
    query_embedding: list[float],
    top_k: int = 5,
    document_ids: list[str] | None = None
) -> list[dict]:
    """
    Search for relevant chunks across indexed documents.

    Optionally restrict the search to selected document IDs.
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

    # Search all indexed vectors so document filtering
    # does not accidentally miss relevant results.
    scores, indices = _index.search(
        query_vector,
        _index.ntotal
    )

    allowed_ids = set(document_ids) if document_ids is not None else None

    results = []

    for score, idx in zip(scores[0], indices[0]):

        if idx == -1:
            continue

        current_document_id = _document_ids[idx]

        if allowed_ids is not None and current_document_id not in allowed_ids:
            continue

        results.append({
            "document_id": current_document_id,
            "chunk": _chunks[idx],
            "score": float(score)
        })

        if len(results) >= top_k:
            break

    return results
