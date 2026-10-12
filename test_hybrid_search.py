
from src.retrieval.hybrid_search import hybrid_search

query = "AI safety benchmarks and harmful refusals"

results = hybrid_search(query, limit=5)

print("\n=== Hybrid Search ===")

for rank, paper in enumerate(results, start=1):
    print(f"\n{rank}. {paper['title']}")
    print(f"arXiv ID: {paper['arxiv_id']}")
    print(f"Hybrid score: {paper['hybrid_score']:.4f}")
    print(f"Semantic rank: {paper['semantic_rank']}")
    print(f"Keyword rank: {paper['keyword_rank']}")
