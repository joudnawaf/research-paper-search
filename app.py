
import streamlit as st

st.set_page_config(
    page_title="Research Paper Explorer",
    page_icon="📚",
    layout="wide",
)

st.title("📚 Research Paper Explorer")
st.write("Search academic papers and ask questions about research.")

from src.retrieval.semantic_search import search_papers
from src.retrieval.hybrid_search import hybrid_search
from src.retrieval.rag import answer_question

search_tab, ask_tab = st.tabs(["🔎 Search Papers", "💬 Ask a Question"])

with search_tab:
    st.subheader("Find research papers")

    query = st.text_input(
        "Search query",
        placeholder="AI safety and agent evaluation",
    )

    method = st.radio(
        "Search method",
        ["Semantic", "Hybrid"],
        horizontal=True,
    )

    limit = st.slider("Number of results", 1, 10, 5)

    if st.button("Search"):
        if not query.strip():
            st.warning("Please enter a search query.")
        else:
            try:
                with st.spinner("Searching papers..."):
                    if method == "Semantic":
                        results = search_papers(query, limit=limit)
                    else:
                        results = hybrid_search(query, limit=limit)

                if not results:
                    st.info("No relevant papers found.")

                for paper in results:
                    with st.container(border=True):
                        st.markdown(f"### {paper['title']}")
                        st.write(f"**arXiv ID:** {paper['arxiv_id']}")

                        if paper.get("summary"):
                            st.write(paper["summary"])

                        if paper.get("similarity") is not None:
                            st.caption(
                                f"Semantic similarity: {paper['similarity']:.3f}"
                            )

                        if paper.get("hybrid_score") is not None:
                            st.caption(
                                f"Hybrid score: {paper['hybrid_score']:.4f}"
                            )

                        st.markdown(
                            f"[Read paper on arXiv](https://arxiv.org/abs/{paper['arxiv_id']})"
                        )

            except Exception as error:
                st.error(f"Search failed: {error}")

with ask_tab:
    st.subheader("Ask a research question")

    question = st.text_area(
        "Your question",
        placeholder="What challenges exist in evaluating AI agent safety?",
    )

    if st.button("Generate Answer"):
        if not question.strip():
            st.warning("Please enter a question.")
        else:
            try:
                with st.spinner("Retrieving papers and generating an answer..."):
                    result = answer_question(question)

                st.markdown("### Answer")
                st.write(result["answer"])

                st.markdown("### Sources")
                if result["sources"]:
                    for source in result["sources"]:
                        st.markdown(
                            f"- [{source['title']}]"
                            f"(https://arxiv.org/abs/{source['arxiv_id']})"
                        )
                else:
                    st.info("No sources were retrieved.")

            except Exception as error:
                st.error(f"Could not generate an answer: {error}")
