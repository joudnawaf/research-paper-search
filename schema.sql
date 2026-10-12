
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS papers (
    arxiv_id TEXT NOT NULL,
    version INTEGER NOT NULL,
    title TEXT NOT NULL,
    summary TEXT NOT NULL,
    authors TEXT[] NOT NULL,
    primary_category TEXT,
    categories TEXT[] NOT NULL DEFAULT '{}'::text[],
    published TIMESTAMPTZ NOT NULL,
    updated TIMESTAMPTZ NOT NULL,
    pdf_url TEXT,
    PRIMARY KEY (arxiv_id, version)
);

CREATE TABLE IF NOT EXISTS paper_chunks (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    arxiv_id TEXT NOT NULL,
    version INTEGER NOT NULL,
    chunk_index INTEGER NOT NULL,
    content TEXT NOT NULL,
    embedding VECTOR(384),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT paper_chunks_arxiv_id_version_chunk_index_key
        UNIQUE (arxiv_id, version, chunk_index),
    CONSTRAINT paper_chunks_paper_fk
        FOREIGN KEY (arxiv_id, version)
        REFERENCES papers (arxiv_id, version)
        ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS paper_chunks_embedding_idx
ON paper_chunks
USING hnsw (embedding vector_cosine_ops);
