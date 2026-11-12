
def chunk_text(
    text: str,
    chunk_size: int = 500,
    overlap: int = 100
) -> list[str]:
    """
    Split document text into smaller overlapping chunks.

    Args:
        text: Extracted document text.
        chunk_size: Maximum approximate characters per chunk.
        overlap: Number of characters shared between consecutive chunks.

    Returns:
        A list of text chunks.
    """

    # Validate chunk configuration
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")

    if overlap < 0:
        raise ValueError("overlap cannot be negative")

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    # Handle empty input
    if not text or not text.strip():
        return []

    text = text.strip()

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:

        end = min(start + chunk_size, text_length)

        # Try to break at a word boundary
        if end < text_length:
            boundary = text.rfind(" ", start, end)

            # Avoid creating extremely small chunks
            if boundary > start + (chunk_size // 2):
                end = boundary

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        # Stop when the complete text has been processed
        if end >= text_length:
            break

        # Move forward while maintaining overlap
        start = end - overlap

    return chunks
