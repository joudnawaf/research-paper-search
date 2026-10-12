
from src.ingestion.fetch_papers import fetch_papers, validate_paper
from src.ingestion.db_storage import save_papers_to_db
from src.processing.pipeline import process_paper


def main():
    print("Fetching 10 AI research papers from arXiv...")

    papers = fetch_papers(
        search_query="cat:cs.AI",
        max_results=10,
        page_size=10,
    )

    if not papers:
        print("No papers returned. Check the API error or try again later.")
        return

    valid_papers = []
    for paper in papers:
        errors = validate_paper(paper)
        if errors:
            print(f"Skipping {paper.arxiv_id}: {errors}")
        else:
            valid_papers.append(paper)

    print(f"Fetched {len(papers)} papers; {len(valid_papers)} passed validation.")

    save_papers_to_db(valid_papers)

    for paper in valid_papers:
        count = process_paper(paper)
        print(f"Stored {paper.arxiv_id}: {paper.title} ({count} chunks)")

    print("Ingestion finished.")


if __name__ == "__main__":
    main()
