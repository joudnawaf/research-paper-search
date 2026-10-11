
import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

from src.ingestion.fetch_papers import Paper


def save_papers(papers: list[Paper], path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    records = []

    for paper in papers:
        record = asdict(paper)
        record["published"] = paper.published.isoformat()
        record["updated"] = paper.updated.isoformat()
        records.append(record)

    path.write_text(
        json.dumps(records, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def load_papers(path: str | Path) -> list[Paper]:
    path = Path(path)
    records = json.loads(path.read_text(encoding="utf-8"))

    papers = []

    for record in records:
        record["published"] = datetime.fromisoformat(record["published"])
        record["updated"] = datetime.fromisoformat(record["updated"])
        papers.append(Paper(**record))

    return papers
