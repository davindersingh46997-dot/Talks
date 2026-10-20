import unittest
from unittest.mock import patch
from types import SimpleNamespace

from backend.rag.crag import retrieve_with_correction
from backend.core.research import search_web_documents


def document(text: str, source: str = "test"):
    return SimpleNamespace(page_content=text, metadata={"source": source})


class CRAGTests(unittest.TestCase):
    def test_relevant_local_evidence_stops_correction(self):
        retrieved_queries = []
        rewrite_calls = []
        web_calls = []
        evidence = document("The answer is in the local file.")

        result = retrieve_with_correction(
            "What is the answer?",
            retrieve=lambda query: retrieved_queries.append(query) or [evidence],
            grade=lambda query, item: True,
            rewrite=lambda query: rewrite_calls.append(query) or "rewritten",
            web_search=lambda query: web_calls.append(query) or [],
        )

        self.assertEqual(result, [evidence])
        self.assertEqual(retrieved_queries, ["What is the answer?"])
        self.assertEqual(rewrite_calls, [])
        self.assertEqual(web_calls, [])

    def test_rewrites_once_and_retries_local_retrieval(self):
        retrieved_queries = []
        evidence = document("Relevant result after the rewritten query.")

        def retrieve(query):
            retrieved_queries.append(query)
            return [document("Unrelated chunk.")] if len(retrieved_queries) == 1 else [evidence]

        result = retrieve_with_correction(
            "Original question",
            retrieve=retrieve,
            grade=lambda query, item: item is evidence,
            rewrite=lambda query: "more specific query",
            web_search=lambda query: self.fail("web fallback should not run"),
        )

        self.assertEqual(result, [evidence])
        self.assertEqual(retrieved_queries, ["Original question", "more specific query"])

    def test_uses_web_after_one_failed_local_retry(self):
        retrieved_queries = []
        web_queries = []
        evidence = document("Relevant web result.", source="https://example.test")

        def retrieve(query):
            retrieved_queries.append(query)
            return [document("Unrelated local chunk.")]

        result = retrieve_with_correction(
            "Original question",
            retrieve=retrieve,
            grade=lambda query, item: item is evidence,
            rewrite=lambda query: "rewritten question",
            web_search=lambda query: web_queries.append(query) or [evidence],
        )

        self.assertEqual(result, [evidence])
        self.assertEqual(retrieved_queries, ["Original question", "rewritten question"])
        self.assertEqual(web_queries, ["rewritten question"])

    def test_returns_empty_when_sources_and_grader_fail(self):
        retrieve_calls = []
        web_calls = []

        def retrieve(query):
            retrieve_calls.append(query)
            return [document("Untrusted evidence")]

        def grader(query, item):
            raise RuntimeError("grader unavailable")

        result = retrieve_with_correction(
            "Question",
            retrieve=retrieve,
            grade=grader,
            rewrite=lambda query: "rewritten",
            web_search=lambda query: web_calls.append(query) or [document("Web result")],
        )

        self.assertEqual(result, [])
        self.assertEqual(retrieve_calls, ["Question", "rewritten"])
        self.assertEqual(web_calls, ["rewritten"])

    def test_empty_query_does_not_call_dependencies(self):
        result = retrieve_with_correction(
            "  ",
            retrieve=lambda query: self.fail("retrieval should not run"),
            web_search=lambda query: self.fail("web search should not run"),
        )

        self.assertEqual(result, [])

    def test_empty_corpus_retries_then_returns_empty_if_web_search_fails(self):
        retrieve_queries = []
        web_queries = []

        def retrieve(query):
            retrieve_queries.append(query)
            return []

        def web_search(query):
            web_queries.append(query)
            raise RuntimeError("Tavily unavailable")

        result = retrieve_with_correction(
            "Question",
            retrieve=retrieve,
            grade=lambda query, item: False,
            rewrite=lambda query: "rewritten question",
            web_search=web_search,
        )

        self.assertEqual(result, [])
        self.assertEqual(retrieve_queries, ["Question", "rewritten question"])
        self.assertEqual(web_queries, ["rewritten question"])

    def test_tavily_without_key_returns_no_web_documents(self):
        with patch.dict("os.environ", {"TAVILY_API_KEY": ""}):
            self.assertEqual(search_web_documents("test query"), [])


if __name__ == "__main__":
    unittest.main()