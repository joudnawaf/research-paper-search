
from src.retrieval.semantic_search import search_papers


query = input("What do you want to research? ")

threshold = input("Minimum similarity (default 0.30): ").strip()

if threshold:
    min_similarity = float(threshold)
else:
    min_similarity = 0.30

results = search_papers(
    query,
    limit=5,
    min_similarity=min_similarity,
)

if not results:
    print("No matching papers found.")
else:
    for i, paper in enumerate(results, start=1):
        print(f"\n{i}. {paper['title']}")
        print(f"   arXiv ID: {paper['arxiv_id']}")
        print(f"   Similarity: {paper['similarity']:.3f}")
        print(f"   Text: {paper['content'][:300]}")
