
import unittest

from src.processing.embeddings import generate_embeddings


class TestEmbeddings(unittest.TestCase):

    def test_generates_384_dimensions(self):
        vectors = generate_embeddings(["Machine learning research papers"])
        self.assertEqual(len(vectors), 1)
        self.assertEqual(len(vectors[0]), 384)

    def test_empty_input_returns_empty_list(self):
        self.assertEqual(generate_embeddings([]), [])

    def test_blank_text_raises_error(self):
        with self.assertRaises(ValueError):
            generate_embeddings(["   "])


if __name__ == "__main__":
    unittest.main()
