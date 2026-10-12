
from unittest.mock import patch

from src.retrieval.rag import answer_question


class TestRag:
    def test_empty_question_raises_error(self):
        try:
            answer_question("")
        except ValueError as error:
            assert str(error) == "Question must not be empty"
        else:
            assert False, "Expected ValueError"

    @patch("src.retrieval.rag.ollama.chat")
    @patch("src.retrieval.rag.search_papers")
    def test_answer_uses_retrieved_papers(self, mock_search, mock_chat):
        mock_search.return_value = [{
            "arxiv_id": "1234.56789",
            "title": "AI Safety Research",
            "chunk_index": 0,
            "content": "This paper discusses AI safety.",
            "similarity": 0.8,
        }]
        mock_chat.return_value = {
            "message": {
                "content": "AI safety is discussed in the paper [arXiv:1234.56789]."
            }
        }

        result = answer_question("What is AI safety?")

        assert "AI safety" in result["answer"]
        assert result["sources"][0]["arxiv_id"] == "1234.56789"
        mock_chat.assert_called_once()

    @patch("src.retrieval.rag.ollama.chat")
    @patch("src.retrieval.rag.search_papers")
    def test_answer_handles_insufficient_evidence(self, mock_search, mock_chat):
        mock_search.return_value = [{
            "arxiv_id": "1234.56789",
            "title": "Unrelated Paper",
            "chunk_index": 0,
            "content": "This paper discusses cooking recipes.",
            "similarity": 0.1,
        }]
        mock_chat.return_value = {
            "message": {
                "content": "The excerpts do not provide enough information to answer."
            }
        }

        result = answer_question(
            "What is the best treatment for a rare disease?"
        )

        assert "not provide enough information" in result["answer"]
        mock_chat.assert_called_once()

    @patch("src.retrieval.rag.ollama.chat")
    @patch("src.retrieval.rag.search_papers")
    def test_no_papers_returns_message_without_calling_model(
        self, mock_search, mock_chat
    ):
        mock_search.return_value = []

        result = answer_question("What is AI safety?")

        assert result["sources"] == []
        assert "couldn't find relevant" in result["answer"]
        mock_chat.assert_not_called()
