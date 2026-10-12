
import psycopg


def test_connection():
    with psycopg.connect(
        "host=localhost port=5434 dbname=research_papers user=jude"
    ) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT current_database(), version();")
            result = cur.fetchone()
            print("Database:", result[0])
            print("PostgreSQL:", result[1].split(",")[0])


if __name__ == "__main__":
    test_connection()
