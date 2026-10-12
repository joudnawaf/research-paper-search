
import psycopg

from src.processing.embeddings import generate_embeddings

CONNECTION_STRING = (
    "host=localhost port=5434 "
    "dbname=research_papers user=jude"
)


def search_papers(
    query: str, limit: int = 5, min_similarity: float = 0.30
) -> list[dict]:
    if not query.strip():
        raise ValueError("Query must not be empty")

    if limit <= 0:
        raise ValueError("Limit must be positive")

    vector = generate_embeddings([query])[0]

    with psycopg.connect(CONNECTION_STRING) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    arxiv_id,
                    title,
                    chunk_index,
                    content,
                    similarity
                FROM (
                    SELECT
                        p.arxiv_id,
                        p.title,
                        c.chunk_index,
                        c.content,
                        1 - (c.embedding <=> %s::vector) AS similarity,
                        ROW_NUMBER() OVER (
                            PARTITION BY p.arxiv_id
                            ORDER BY c.embedding <=> %s::vector
                        ) AS paper_rank
                    FROM paper_chunks AS c
                    JOIN papers AS p
                      ON p.arxiv_id = c.arxiv_id
                     AND p.version = c.version
                    WHERE c.embedding IS NOT NULL
                ) AS ranked_chunks
                WHERE paper_rank = 1
                AND similarity >= %s
                ORDER BY similarity DESC
                LIMIT %s
                """,
                (str(vector), str(vector), min_similarity, limit),
            )

            rows = cur.fetchall()

    return [
        {
            "arxiv_id": row[0],
            "title": row[1],
            "chunk_index": row[2],
            "content": row[3],
            "similarity": float(row[4]),
        }
        for row in rows
    ]



def keyword_search(query: str, limit: int = 5) -> list[dict]:
    if not query.strip():
        raise ValueError("Query must not be empty")

    if limit <= 0:
        raise ValueError("Limit must be positive")

    with psycopg.connect(CONNECTION_STRING) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    arxiv_id,
                    title,
                    chunk_index,
                    content,
                    score
                FROM (
                    SELECT
                        p.arxiv_id,
                        p.title,
                        c.chunk_index,
                        c.content,
                        ts_rank(
                            to_tsvector('english', c.content),
                            to_tsquery('english', replace(%s, ' ', ' | '))
                        ) AS score,
                        ROW_NUMBER() OVER (
                            PARTITION BY p.arxiv_id
                            ORDER BY ts_rank(
                                to_tsvector('english', c.content),
                                to_tsquery('english', replace(%s, ' ', ' | '))
                            ) DESC
                        ) AS paper_rank
                    FROM paper_chunks AS c
                    JOIN papers AS p
                      ON p.arxiv_id = c.arxiv_id
                     AND p.version = c.version
                    WHERE to_tsvector('english', c.content)
                          @@ to_tsquery('english', replace(%s, ' ', ' | '))
                ) AS ranked_chunks
                WHERE paper_rank = 1
                ORDER BY score DESC
                LIMIT %s
                """,
                (query, query, query, limit),
            )

            rows = cur.fetchall()

    return [
        {
            "arxiv_id": row[0],
            "title": row[1],
            "chunk_index": row[2],
            "content": row[3],
            "similarity": float(row[4]),
        }
        for row in rows
    ]
