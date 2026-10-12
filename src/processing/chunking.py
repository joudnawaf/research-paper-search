
from dataclasses import dataclass


@dataclass(frozen=True)
class TextChunk:
    chunk_index: int
    content: str


def chunk_text(
    text: str,
    chunk_size: int = 180,
    overlap: int = 30,
) -> list[TextChunk]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be non-negative and smaller than chunk_size")

    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = min(start + chunk_size, len(words))
        content = " ".join(words[start:end])

        chunks.append(
            TextChunk(
                chunk_index=len(chunks),
                content=content,
            )
        )

        if end == len(words):
            break

        start = end - overlap

    return chunks
