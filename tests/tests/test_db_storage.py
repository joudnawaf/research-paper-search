
import unittest
import psycopg

from src.ingestion.fetch_papers import parse_feed
from src.ingestion.db_connection import get_connection_string
from src.ingestion.db_storage import save_papers_to_db
from tests.test_fetch_papers import SAMPLE_XML


class TestDatabaseStorage(unittest.TestCase):

    def test_save_paper_to_database(self):
        papers = parse_feed(SAMPLE_XML)
        save_papers_to_db(papers)

        with psycopg.connect(get_connection_string()) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT title FROM papers WHERE arxiv_id = %s AND version = %s",
                    ("2401.00001", 2),
                )
                result = cur.fetchone()

        self.assertIsNotNone(result)
        self.assertEqual(result[0], papers[0].title)


if __name__ == "__main__":
    unittest.main()
