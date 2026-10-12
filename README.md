# Research Paper Search Engine (RAG Pipeline)

A research-paper search engine that retrieves academic papers from arXiv, indexes them using vector embeddings, and answers research questions using Retrieval-Augmented Generation (RAG).

## Features

- **Paper ingestion:** Fetches recent papers from arXiv.
- **Text processing:** Splits paper content into smaller chunks.
- **Vector embeddings:** Uses `sentence-transformers/all-MiniLM-L6-v2` to generate embeddings.
- **Vector storage:** Stores paper metadata and embeddings in PostgreSQL with pgvector.
- **Semantic search:** Retrieves papers based on meaning.
- **Keyword search:** Finds papers using keyword matching.
- **Hybrid search:** Combines semantic and keyword search rankings.
- **RAG question answering:** Generates answers from retrieved excerpts and includes arXiv citations.
- **Search evaluation:** Evaluates retrieval using Recall@5, Precision@5, and Mean Reciprocal Rank (MRR).
- **Automated ingestion:** Uses Apache Airflow to schedule the ingestion pipeline.
- **Data transformations:** Uses dbt to build and test analytical models.
- **Web interface:** Uses Streamlit for interactive paper search and question answering.

## Technology Stack

- Python
- PostgreSQL
- pgvector
- Sentence Transformers
- Ollama (`qwen2.5:3b`)
- Streamlit
- Apache Airflow
- dbt
- pytest

## Architecture

1. Fetch paper metadata and text from arXiv.
2. Validate the retrieved data.
3. Split paper text into chunks.
4. Generate vector embeddings for the chunks.
5. Store paper metadata and embeddings in PostgreSQL.
6. Retrieve relevant papers using semantic or hybrid search.
7. Pass retrieved excerpts to the language model.
8. Generate an answer with citations to the source papers.
9. Display search results and answers in the Streamlit interface.

## Setup

### 1. Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd research-paper-search
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure PostgreSQL

Install PostgreSQL and pgvector, create a database named `research_papers`, and configure the connection settings used by the project.

The current local development configuration uses:

- Host: `localhost`
- Port: `5434`
- Database: `research_papers`

Ensure that PostgreSQL is running and that the required database tables and pgvector extension have been created before running the pipeline.

### 5. Configure Ollama

Install Ollama and pull the language model:

```bash
ollama pull qwen2.5:3b
```

Ensure Ollama is running before using the question-answering feature.

## Running the Application

Start the Streamlit interface from the project root:

```bash
python -m streamlit run app.py
```

Open the local URL displayed in the terminal, usually `http://localhost:8501`.

### Search Papers

Choose semantic or hybrid search, enter a query, and view the retrieved papers and their arXiv links.

### Ask a Question

Enter a research question to retrieve relevant excerpts and generate an answer with citations to the source papers.

## Running Ingestion

Fetch and process papers using:

```bash
python ingest_papers.py
```

## Running Tests

Run the automated test suite:

```bash
python -m pytest -q
```

The test suite previously completed with **21 passing tests** in the local development environment.

## Search Evaluation

The project evaluates retrieval using:

- **Recall@5:** The proportion of relevant papers retrieved in the top five results.
- **Precision@5:** The proportion of the top five results that are relevant.
- **MRR@5:** How highly the first relevant result is ranked.

In the current preliminary evaluation, using nine manually labeled queries, the recorded results were:

| Method | Recall@5 | Precision@5 | MRR@5 |
|---|---:|---:|---:|
| Semantic search (threshold 0.30) | 1.00 | 0.83 | 1.00 |
| Keyword search | 0.96 | 0.27 | 1.00 |
| Hybrid search | 1.00 | 0.29 | 1.00 |

These results are preliminary because the evaluation set is small and relevance labels were assigned manually. They should not be interpreted as a comprehensive benchmark.

## Limitations

- The indexed collection contains only a subset of arXiv research papers, rather than the entire arXiv corpus.
- Search quality depends on the indexed documents, chunking, and retrieval settings.
- Evaluation currently uses a small set of manually labeled queries.
- Generated answers depend on the quality and coverage of the retrieved excerpts.
- Citations identify the retrieved papers, but individual claims should be checked against the original papers.
- The local Airflow schedule requires the machine, scheduler, and database to be running.

## Future Improvements

- Expand the indexed paper collection.
- Increase the size and diversity of the search evaluation dataset.
- Improve retrieval ranking and relevance evaluation.
- Add richer paper metadata and filtering.
- Improve the user interface and source-excerpt display.
- Deploy the application and ingestion pipeline to a hosted environment.

## License

Add a license appropriate for your project before distributing it publicly.