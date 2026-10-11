
import unittest
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

from src.ingestion.fetch_papers import parse_feed, validate_paper

SAMPLE_XML = b"""<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom"
      xmlns:arxiv="http://arxiv.org/schemas/atom">
  <entry>
    <id>https://arxiv.org/abs/2401.00001v2</id>
    <title>  Testing   Research Paper Parsing  </title>
    <summary>
      This paper tests our parser.
      It contains multiple lines.
    </summary>
    <published>2024-01-10T12:00:00Z</published>
    <updated>2024-02-15T09:30:00Z</updated>
    <author>
      <name>Alex Smith</name>
    </author>
    <author>
      <name>Jamie Lee</name>
    </author>
    <arxiv:primary_category term="cs.AI"/>
    <category term="cs.AI"/>
    <category term="cs.CL"/>
    <link href="https://arxiv.org/pdf/2401.00001" title="pdf"/>
  </entry>
</feed>
"""


class TestParseFeed(unittest.TestCase):

    def test_parses_paper_metadata(self):
        papers = parse_feed(SAMPLE_XML)

        self.assertEqual(len(papers), 1)

        paper = papers[0]

        self.assertEqual(paper.arxiv_id, "2401.00001")
        self.assertEqual(paper.version, 2)
        self.assertEqual(paper.title, "Testing Research Paper Parsing")
        self.assertEqual(
            paper.summary,
            "This paper tests our parser. It contains multiple lines."
        )
        self.assertEqual(paper.authors, ["Alex Smith", "Jamie Lee"])
        self.assertEqual(paper.primary_category, "cs.AI")
        self.assertEqual(paper.categories, ["cs.AI", "cs.CL"])
        self.assertEqual(
            paper.published,
            datetime(2024, 1, 10, 12, 0, tzinfo=timezone.utc)
        )
        self.assertEqual(
            paper.updated,
            datetime(2024, 2, 15, 9, 30, tzinfo=timezone.utc)
        )
        self.assertEqual(
            paper.pdf_url,
            "https://arxiv.org/pdf/2401.00001"
        )


    def test_empty_feed_returns_empty_list(self):
        empty_xml = b"""
        <feed xmlns="http://www.w3.org/2005/Atom">
        </feed>
        """

        papers = parse_feed(empty_xml)

        self.assertEqual(papers, [])

        
    def test_malformed_xml_raises_error(self):
        with self.assertRaises(ET.ParseError):
            parse_feed(b"<feed><entry>")

    
    def test_valid_paper_has_no_errors(self):
        paper = parse_feed(SAMPLE_XML)[0]

        errors = validate_paper(paper)

        self.assertEqual(errors, [])

    def test_missing_title_is_detected(self):
        paper = parse_feed(SAMPLE_XML)[0]
        paper = paper.__class__(
            arxiv_id=paper.arxiv_id,
            version=paper.version,
            title="",
            summary=paper.summary,
            authors=paper.authors,
            primary_category=paper.primary_category,
            categories=paper.categories,
            published=paper.published,
            updated=paper.updated,
            pdf_url=paper.pdf_url,
        )

        errors = validate_paper(paper)

        self.assertIn("Missing title", errors)

 

if __name__ == "__main__":
    unittest.main()
