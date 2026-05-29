import os
import pdfplumber
import vecs
from fastapi import HTTPException
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.core.config import settings
from huggingface_hub import InferenceClient

# Hugging Face client (FIXED)
client = InferenceClient(
    provider="hf-inference",
    api_key=settings.HUGGINGFACE_API_KEY,
)

MODEL_ID = "sentence-transformers/all-MiniLM-L6-v2"

DATABASE_URL = settings.DATABASE_URL

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
)


def get_embedding(text: str) -> list:
    """Generate embedding via Hugging Face (stable client version)."""

    if not settings.HUGGINGFACE_API_KEY:
        raise HTTPException(status_code=500, detail="Missing Hugging Face API key")

    try:
        embedding = client.feature_extraction(
            text,
            model=MODEL_ID
        )

        # ensure flat list
        if isinstance(embedding, list) and len(embedding) > 0:
            if isinstance(embedding[0], list):
                return embedding[0]

        return embedding

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Embedding error: {str(e)}")


def extract_text_from_pdf(file_path: str) -> str:
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()


def chunk_and_embed_document(document_id: int, file_path: str, original_name: str) -> int:

    raw_text = extract_text_from_pdf(file_path)
    if not raw_text:
        raise ValueError("No text extracted from PDF")

    chunks = text_splitter.split_text(raw_text)

    embeddings = []
    for chunk in chunks:
        embeddings.append(get_embedding(chunk))

    if not DATABASE_URL:
        raise HTTPException(status_code=500, detail="DATABASE_URL missing")

    vx = vecs.create_client(DATABASE_URL)
    collection = vx.get_or_create_collection(
        name="policy_documents",
        dimension=384
    )

    records = []
    for i, chunk in enumerate(chunks):
        records.append((
            f"doc_{document_id}_chunk_{i}",
            embeddings[i],
            {
                "document_id": document_id,
                "original_name": original_name,
                "chunk_index": i,
                "content": chunk
            }
        ))

    collection.upsert(records=records)
    collection.create_index()

    return len(chunks)


def delete_document_chunks(document_id: int):

    if not DATABASE_URL:
        return

    vx = vecs.create_client(DATABASE_URL)
    collection = vx.get_or_create_collection(
        name="policy_documents",
        dimension=384
    )

    collection.delete(filters={"document_id": {"$eq": document_id}})