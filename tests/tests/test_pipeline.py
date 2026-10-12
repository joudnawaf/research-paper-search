
import unittest
import psycopg

from src.ingestion.fetch_papers import parse_feed
from src.processing.pipeline import process_paper
from tests.test_fetch_papers import SAMPLE_XML


class TestPipeline(unittest.TestCase):

    def test_process_paper_stores_chunks_and_embeddings(self):
        paper = parse_feed(SAMPLE_XML)[0]
        chunk_count = process_paper(paper)

        self.assertGreater(chunk_count, 0)

        with psycopg.connect(
            "host=localhost port=5434 dbname=research_papers user=jude"
        ) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT content, embedding
                    FROM paper_chunks
                    WHERE arxiv_id = %s AND version = %s
                    ORDER BY chunk_index
                    """,
                    (paper.arxiv_id, paper.version),
                )
                rows = cur.fetchall()

        self.assertEqual(len(rows), chunk_count)
        self.assertTrue(rows[0][0])
        self.assertIsNotNone(rows[0][1])


if __name__ == "__main__":
    unittest.main()
