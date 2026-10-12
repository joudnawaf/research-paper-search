
import os

import psycopg
from dotenv import load_dotenv
load_dotenv()

def get_connection_string() -> str:
    return os.getenv(
        "DATABASE_URL",
        "host=localhost port=5434 dbname=research_papers user=jude",
    )


def test_connection():
    with psycopg.connect(get_connection_string()) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT current_database(), version();")
            result = cur.fetchone()
            print("Database:", result[0])
            print("PostgreSQL:", result[1].split(",")[0])


if __name__ == "__main__":
    test_connection()
