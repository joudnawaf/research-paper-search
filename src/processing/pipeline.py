
import psycopg

from src.ingestion.fetch_papers import Paper
from src.processing.chunking import chunk_text
from src.processing.embeddings import generate_embeddings
from src.ingestion.db_connection import get_connection_string




def process_paper(paper: Paper) -> int:
    chunks = chunk_text(f"{paper.title}\n\n{paper.summary}")

    if not chunks:
        return 0

    vectors = generate_embeddings([chunk.content for chunk in chunks])

    with psycopg.connect(get_connection_string()) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM paper_chunks
                WHERE arxiv_id = %s AND version = %s
                """,
                (paper.arxiv_id, paper.version),
            )

            for chunk, vector in zip(chunks, vectors):
                cur.execute(
                    """
                    INSERT INTO paper_chunks (
                        arxiv_id, version, chunk_index, content, embedding
                    )
                    VALUES (%s, %s, %s, %s, %s::vector)
                    """,
                    (
                        paper.arxiv_id,
                        paper.version,
                        chunk.chunk_index,
                        chunk.content,
                        str(vector),
                    ),
                )

    return len(chunks)
