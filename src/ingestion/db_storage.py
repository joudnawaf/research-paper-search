
import psycopg
from src.ingestion.db_connection import get_connection_string
from src.ingestion.fetch_papers import Paper


def save_papers_to_db(papers: list[Paper]) -> None:
    with psycopg.connect(get_connection_string()) as conn:
        with conn.cursor() as cur:
            cur.executemany(
                """
                INSERT INTO papers (
                    arxiv_id, version, title, summary, authors,
                    primary_category, categories, published, updated, pdf_url
                )
                VALUES (
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s
                )
                ON CONFLICT (arxiv_id, version) DO UPDATE SET
                    title = EXCLUDED.title,
                    summary = EXCLUDED.summary,
                    authors = EXCLUDED.authors,
                    primary_category = EXCLUDED.primary_category,
                    categories = EXCLUDED.categories,
                    published = EXCLUDED.published,
                    updated = EXCLUDED.updated,
                    pdf_url = EXCLUDED.pdf_url
                """,
                [
                    (
                        p.arxiv_id,
                        p.version,
                        p.title,
                        p.summary,
                        p.authors,
                        p.primary_category,
                        p.categories,
                        p.published,
                        p.updated,
                        p.pdf_url,
                    )
                    for p in papers
                ],
            )
