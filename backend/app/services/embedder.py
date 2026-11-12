
from sentence_transformers import SentenceTransformer
import numpy as np

# Load the embedding model only once
MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


def generate_embeddings(chunks: list[str]) -> list[list[float]]:
    """
    Convert text chunks into numerical vectors.

    Args:
        chunks: List of text chunks.

    Returns:
        List of embedding vectors.
    """

    if not chunks:
        return []

    if not all(isinstance(chunk, str) and chunk.strip() for chunk in chunks):
        raise ValueError("All chunks must be non-empty strings.")

    embeddings = model.encode(
        chunks,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=False
    )

    # FAISS works efficiently with float32 vectors
    embeddings = np.asarray(embeddings, dtype=np.float32)

    return embeddings.tolist()
