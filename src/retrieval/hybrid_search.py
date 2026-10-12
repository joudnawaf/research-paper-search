
from src.retrieval.semantic_search import search_papers, keyword_search


def hybrid_search(
    query: str,
    limit: int = 5,
    min_similarity: float = 0.30,
) -> list[dict]:
    if not query.strip():
        raise ValueError("Query must not be empty")

    if limit <= 0:
        raise ValueError("Limit must be positive")

    semantic_results = search_papers(
        query, limit=limit, min_similarity=min_similarity
    )
    keyword_results = keyword_search(query, limit=limit)

    combined = {}

    for rank, paper in enumerate(semantic_results, start=1):
        paper_id = paper["arxiv_id"]
        combined[paper_id] = {
            **paper,
            "hybrid_score": 1 / (60 + rank),
            "semantic_rank": rank,
            "keyword_rank": None,
        }

    for rank, paper in enumerate(keyword_results, start=1):
        paper_id = paper["arxiv_id"]

        if paper_id not in combined:
            combined[paper_id] = {
                **paper,
                "hybrid_score": 0.5 / (60 + rank),
                "semantic_rank": None,
                "keyword_rank": rank,
            }
        else:
            combined[paper_id]["hybrid_score"] += 0.5 / (60 + rank)
            combined[paper_id]["keyword_rank"] = rank

    ranked_results = sorted(
        combined.values(),
        key=lambda paper: paper["hybrid_score"],
        reverse=True,
    )

    return ranked_results[:limit]
