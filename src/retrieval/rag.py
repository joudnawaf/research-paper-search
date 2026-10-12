
import ollama

from src.retrieval.semantic_search import search_papers


def answer_question(question: str, limit: int = 3) -> dict:
    if not question.strip():
        raise ValueError("Question must not be empty")

    papers = search_papers(question, limit=limit)

    if not papers:
        return {
            "answer": "I couldn't find relevant research papers for this question.",
            "sources": [],
        }


    context = ""

    print("\nRETRIEVED PAPERS:")

    for paper in papers:
        print(f"\n{paper['title']} (arXiv:{paper['arxiv_id']})")
        print(paper["content"])

        context += (

            f"\nPaper: {paper['title']}\n"
            f"arXiv ID: {paper['arxiv_id']}\n"
            f"Excerpt: {paper['content']}\n"
        )

    response = ollama.chat(
        model="qwen2.5:3b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a research assistant answering questions using "
                    "retrieved research-paper excerpts.\n\n"
                    "Follow these rules:\n"
                    "1. Use only information explicitly supported by the excerpts.\n"
                    "2. Do not invent facts or make unsupported assumptions.\n"
                    "3. Cite each important claim using the format "
                    "[arXiv:1234.56789].\n"
                    "4. If the excerpts are insufficient, clearly say so.\n"
                    "5. If papers disagree, explain the difference and cite "
                    "each relevant paper.\n"
                    "6. Distinguish what a paper states from your own conclusions."
                    "7. Do not present recommendations or implications as findings "
                    "from a paper unless the excerpts explicitly support them.\n"
                    "8. When making an inference, label it clearly as an inference "
                    "rather than a reported finding."
                ),
            },
            {
                "role": "user",
                "content": f"Question: {question}\n\nResearch excerpts:\n{context}",
            },
        ],
    )

    return {
        "answer": response["message"]["content"],
        "sources": [
            {
                "arxiv_id": paper["arxiv_id"],
                "title": paper["title"],
                "similarity": paper["similarity"],
            }
            for paper in papers
        ],
    }
