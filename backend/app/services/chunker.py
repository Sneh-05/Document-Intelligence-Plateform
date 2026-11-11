def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100) -> list[str]:
    """
    Splits text into fixed-size chunks with overlap.

    Args:
        text: The raw text to chunk.
        chunk_size: Number of characters per chunk.
        overlap: Number of characters to repeat from the previous chunk.

    Returns:
        A list of text chunks.
    """
    if not text or not text.strip():
        return []

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)

        # Move forward by chunk_size minus overlap
        start += chunk_size - overlap

    return chunks

