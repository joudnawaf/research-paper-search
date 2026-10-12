
from src.retrieval.hybrid_search import hybrid_search
from src.retrieval.semantic_search import search_papers, keyword_search


queries = {
    "large language models and reasoning": {
        "relevant": {"2610.12410"},
    },
    "AI safety and detecting deceptive behavior": {
        "relevant": {"2610.12445", "2610.12409", "2610.12463"},
    },
    "robot learning and self-improving robots": {
        "relevant": {"2610.12424"},
    },
    "generative modeling of complex systems": {
        "relevant": {"2610.12449"},
    },
    "human object interaction and scene understanding": {
        "relevant": {"2610.12416"},
    },
    "AI agents and collaboration": {
        "relevant": {"2610.12436", "2610.12452"},
    },
    "AI time horizons and statistical estimation": {
        "relevant": {"2610.12466"},
    },
    "robotics in complex real world environments": {
        "relevant": {"2610.12424"},
    },
    "AI safety benchmarks and harmful refusals": {
        "relevant": {"2610.12409"},
    },
}


def reciprocal_rank(results, relevant_ids):
    for rank, paper in enumerate(results, start=1):
        if paper["arxiv_id"] in relevant_ids:
            return 1 / rank
    return 0.0


def evaluate_results(results, relevant_ids):
    result_ids = {paper["arxiv_id"] for paper in results}

    recall = len(result_ids & relevant_ids) / len(relevant_ids)

    precision = (
        len(result_ids & relevant_ids) / len(result_ids)
        if result_ids
        else 0.0
    )

    mrr = reciprocal_rank(results, relevant_ids)

    return recall, precision, mrr


def print_metrics(name, recalls, precisions, mrr_scores):
    print(
        f"Mean {name} Recall@5: "
        f"{sum(recalls) / len(recalls):.2f}"
    )
    print(
        f"Mean {name} Precision@5: "
        f"{sum(precisions) / len(precisions):.2f}"
    )
    print(
        f"Mean {name} MRR@5: "
        f"{sum(mrr_scores) / len(mrr_scores):.2f}"
    )


semantic_030_recalls = []
semantic_030_precisions = []
semantic_030_mrr_scores = []

print("\n=== Semantic Search ===")

for threshold in (0.30, 0.40, 0.50):
    recalls = []
    precisions = []
    mrr_scores = []

    print(f"\n--- Threshold: {threshold:.2f} ---")

    for query, info in queries.items():
        relevant = info["relevant"]

        results = search_papers(
            query, limit=5, min_similarity=threshold
        )

        recall, precision, mrr = evaluate_results(results, relevant)

        recalls.append(recall)
        precisions.append(precision)
        mrr_scores.append(mrr)

        if threshold == 0.30:
            semantic_030_recalls.append(recall)
            semantic_030_precisions.append(precision)
            semantic_030_mrr_scores.append(mrr)

        print(f"\nQuery: {query}")
        print(f"Recall@5: {recall:.2f}")
        print(f"Precision@5: {precision:.2f}")
        print(f"MRR@5: {mrr:.2f}")

    print(
        f"\nMean Semantic Recall@5 at {threshold:.2f}: "
        f"{sum(recalls) / len(recalls):.2f}"
    )
    print(
        f"Mean Semantic Precision@5 at {threshold:.2f}: "
        f"{sum(precisions) / len(precisions):.2f}"
    )
    print(
        f"Mean Semantic MRR@5 at {threshold:.2f}: "
        f"{sum(mrr_scores) / len(mrr_scores):.2f}"
    )


keyword_recalls = []
keyword_precisions = []
keyword_mrr_scores = []

print("\n=== Keyword Search ===")

for query, info in queries.items():
    relevant = info["relevant"]
    results = keyword_search(query, limit=5)

    recall, precision, mrr = evaluate_results(results, relevant)

    keyword_recalls.append(recall)
    keyword_precisions.append(precision)
    keyword_mrr_scores.append(mrr)

    print(f"\nQuery: {query}")
    print(f"Recall@5: {recall:.2f}")
    print(f"Precision@5: {precision:.2f}")
    print(f"MRR@5: {mrr:.2f}")

print()
print_metrics(
    "Keyword",
    keyword_recalls,
    keyword_precisions,
    keyword_mrr_scores,
)


hybrid_recalls = []
hybrid_precisions = []
hybrid_mrr_scores = []

print("\n=== Hybrid Search ===")

for query, info in queries.items():
    relevant = info["relevant"]
    results = hybrid_search(query, limit=5)

    recall, precision, mrr = evaluate_results(results, relevant)

    hybrid_recalls.append(recall)
    hybrid_precisions.append(precision)
    hybrid_mrr_scores.append(mrr)

    print(f"\nQuery: {query}")
    print(f"Recall@5: {recall:.2f}")
    print(f"Precision@5: {precision:.2f}")
    print(f"MRR@5: {mrr:.2f}")

print()
print_metrics(
    "Hybrid",
    hybrid_recalls,
    hybrid_precisions,
    hybrid_mrr_scores,
)


print("\n=== Final Comparison ===")
print(
    f"{'Method':<20} {'Recall@5':<12} "
    f"{'Precision@5':<14} {'MRR@5':<10}"
)
print("-" * 56)

print(
    f"{'Semantic (0.30)':<20} "
    f"{sum(semantic_030_recalls) / len(semantic_030_recalls):<12.2f} "
    f"{sum(semantic_030_precisions) / len(semantic_030_precisions):<14.2f} "
    f"{sum(semantic_030_mrr_scores) / len(semantic_030_mrr_scores):.2f}"
)

print(
    f"{'Keyword':<20} "
    f"{sum(keyword_recalls) / len(keyword_recalls):<12.2f} "
    f"{sum(keyword_precisions) / len(keyword_precisions):<14.2f} "
    f"{sum(keyword_mrr_scores) / len(keyword_mrr_scores):.2f}"
)

print(
    f"{'Hybrid':<20} "
    f"{sum(hybrid_recalls) / len(hybrid_recalls):<12.2f} "
    f"{sum(hybrid_precisions) / len(hybrid_precisions):<14.2f} "
    f"{sum(hybrid_mrr_scores) / len(hybrid_mrr_scores):.2f}"
)
