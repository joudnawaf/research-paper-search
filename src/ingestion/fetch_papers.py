"""Fetch recent arXiv papers and parse them into clean, typed records.

Extract (HTTP) and transform (XML parsing) are kept separate so the parser
can be unit tested without touching the network.
"""

from __future__ import annotations

import logging
import re
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime

BASE_URL = "https://export.arxiv.org/api/query"
NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "arxiv": "http://arxiv.org/schemas/atom",
}
REQUEST_DELAY_SECONDS = 3  # arXiv asks for at most ~1 request every 3 seconds
RETRYABLE_STATUS = {429, 500, 502, 503, 504}
VERSION_RE = re.compile(r"^(?P<id>.+)v(?P<version>\d+)$")

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class Paper:
    arxiv_id: str  # stable id without version, e.g. "2401.00001"
    version: int
    title: str
    summary: str
    authors: list[str]
    primary_category: str | None
    categories: list[str]
    published: datetime
    updated: datetime
    pdf_url: str | None


def _clean(text: str | None) -> str:
    """Collapse the newlines and runs of whitespace arXiv puts in text."""
    return " ".join((text or "").split())


def _parse_datetime(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _parse_entry(entry: ET.Element) -> Paper:
    raw_id = _clean(entry.findtext("atom:id", namespaces=NS))
    if "/api/errors" in raw_id:
        message = _clean(entry.findtext("atom:summary", namespaces=NS))
        raise ValueError(f"arXiv API error: {message}")

    arxiv_id = raw_id.split("/abs/", 1)[-1]
    version = 1
    match = VERSION_RE.match(arxiv_id)
    if match:
        arxiv_id, version = match["id"], int(match["version"])

    primary = entry.find("arxiv:primary_category", NS)
    pdf_url = next(
        (
            link.get("href")
            for link in entry.findall("atom:link", NS)
            if link.get("title") == "pdf"
        ),
        None,
    )

    return Paper(
        arxiv_id=arxiv_id,
        version=version,
        title=_clean(entry.findtext("atom:title", namespaces=NS)),
        summary=_clean(entry.findtext("atom:summary", namespaces=NS)),
        authors=[
            _clean(a.findtext("atom:name", namespaces=NS))
            for a in entry.findall("atom:author", NS)
        ],
        primary_category=primary.get("term") if primary is not None else None,
        categories=[c.get("term") for c in entry.findall("atom:category", NS)],
        published=_parse_datetime(entry.findtext("atom:published", namespaces=NS)),
        updated=_parse_datetime(entry.findtext("atom:updated", namespaces=NS)),
        pdf_url=pdf_url,
    )


def parse_feed(xml_bytes: bytes) -> list[Paper]:
    """Pure function: raw Atom XML in, list of Paper out. Easy to unit test."""
    root = ET.fromstring(xml_bytes)
    return [_parse_entry(entry) for entry in root.findall("atom:entry", NS)]


def validate_paper(paper: Paper) -> list[str]:
    """Return a list of validation problems; an empty list means valid."""
    errors = []

    if not paper.arxiv_id.strip():
        errors.append("Missing arXiv ID")

    if not paper.title.strip():
        errors.append("Missing title")

    if not paper.summary.strip():
        errors.append("Missing abstract")

    if not paper.authors:
        errors.append("Missing authors")

    if paper.published.tzinfo is None:
        errors.append("Publication date must include a timezone")

    if paper.updated.tzinfo is None:
        errors.append("Update date must include a timezone")

    return errors



def build_url(search_query: str, start: int, max_results: int) -> str:
    params = {
        "search_query": search_query,
        "start": start,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }
    return f"{BASE_URL}?{urllib.parse.urlencode(params)}"


def _http_get(url: str, retries: int = 4) -> bytes:
    """GET with exponential backoff on rate limits, server errors, timeouts."""
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "ResearchPaperSearch/0.1 (judenawaaf@gmail.com)"},
    )
    for attempt in range(1, retries + 1):
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return response.read()
        except urllib.error.HTTPError as exc:
            retryable, error = exc.code in RETRYABLE_STATUS, exc
        except (urllib.error.URLError, TimeoutError) as exc:
            retryable, error = True, exc

        if not retryable or attempt == retries:
            raise error
        wait = REQUEST_DELAY_SECONDS * 2**attempt
        log.warning("Request failed (%s); retry %d/%d in %ds", error, attempt, retries, wait)
        time.sleep(wait)
    raise RuntimeError("unreachable")


def fetch_papers(
    search_query: str = "cat:cs.AI",
    max_results: int = 100,
    page_size: int = 100,
    since: datetime | None = None,
) -> list[Paper]:
    """Fetch papers newest-first, paginating politely.

    `since` (timezone-aware) enables incremental loads: results are sorted
    newest-first, so we stop as soon as we reach a paper we already have.
    """
    papers: list[Paper] = []
    start = 0
    while start < max_results:
        size = min(page_size, max_results - start)
        batch = parse_feed(_http_get(build_url(search_query, start, size)))
        if not batch:
            break
        for paper in batch:
            if since and paper.published <= since:
                return papers
            papers.append(paper)
        start += len(batch)
        if len(batch) < size:
            break
        time.sleep(REQUEST_DELAY_SECONDS)
    return papers


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    for i, paper in enumerate(fetch_papers(max_results=5), start=1):
        print(f"\n{i}. {paper.title}")
        print(f"   ID: {paper.arxiv_id}v{paper.version}  ({paper.primary_category})")
        print(f"   Authors: {', '.join(paper.authors[:3])}")
        print(f"   Published: {paper.published:%Y-%m-%d}")
        print(f"   Abstract: {paper.summary[:250]}...")