
from src.retrieval.rag import answer_question

result = answer_question(
    "What was the exact sample size and statistical significance "
    "What exact percentage improvement in benchmark accuracy did the authors report, and what was the p-value?"
)

print("\nANSWER:\n")
print(result["answer"])

print("\nSOURCES:\n")
for source in result["sources"]:
    print(f"- {source['title']} (arXiv:{source['arxiv_id']})")
