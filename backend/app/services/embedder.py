from sentence_transformers import SentenceTransformer

# Load the model once at module level (not inside the function)
# This avoids reloading the model on every call, which is expensive
model = SentenceTransformer("all-MiniLM-L6-v2")

def generate_embeddings(chunks: list[str]) -> list[list[float]]:
    """
    Converts a list of text chunks into embedding vectors.

    Args:
        chunks: List of text strings to embed.

    Returns:
        List of embedding vectors (each is a list of floats).
    """
    if not chunks:
        return []

    embeddings = model.encode(chunks, convert_to_numpy=True)
    return embeddings.tolist()
