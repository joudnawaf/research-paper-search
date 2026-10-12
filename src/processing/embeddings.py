
from functools import lru_cache

from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


@lru_cache(maxsize=1)
def load_model():
    return SentenceTransformer(MODEL_NAME)


def generate_embeddings(texts: list[str], model=None) -> list[list[float]]:
    if not texts:
      return []

    if any(not text.strip() for text in texts):
        raise ValueError("Texts must not contain empty strings")

    if model is None:
        model = load_model()

    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
    )

    return embeddings.tolist()
