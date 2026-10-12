
import unittest

from src.processing.chunking import chunk_text


class TestChunking(unittest.TestCase):

    def test_short_text_creates_one_chunk(self):
        chunks = chunk_text("Research papers help us learn.")
        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0].content, "Research papers help us learn.")

    def test_long_text_has_overlap(self):
        words = [f"word{i}" for i in range(250)]
        chunks = chunk_text(" ".join(words), chunk_size=100, overlap=20)

        self.assertEqual(len(chunks), 3)
        self.assertEqual(chunks[0].chunk_index, 0)
        self.assertEqual(chunks[1].chunk_index, 1)
        self.assertEqual(chunks[0].content.split()[-20:],
                         chunks[1].content.split()[:20])

    def test_invalid_overlap_raises_error(self):
        with self.assertRaises(ValueError):
            chunk_text("some text", chunk_size=10, overlap=10)


if __name__ == "__main__":
    unittest.main()
