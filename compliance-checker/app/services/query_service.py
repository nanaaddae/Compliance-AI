import os
import vecs
from groq import Groq
from fastapi import HTTPException
from app.core.config import settings
from huggingface_hub import InferenceClient

# Groq client
client = Groq(api_key=settings.GROQ_API_KEY)

# Hugging Face client (FIXED)
hf_client = InferenceClient(
    provider="hf-inference",
    api_key=settings.HUGGINGFACE_API_KEY,
)

MODEL_ID = "sentence-transformers/all-MiniLM-L6-v2"

DATABASE_URL = settings.DATABASE_URL

def get_query_embedding(text: str) -> list:

    if not settings.HUGGINGFACE_API_KEY:
        raise HTTPException(status_code=500, detail="Missing HF API key")

    try:
        embedding = hf_client.feature_extraction(
            text,
            model=MODEL_ID
        )

        if isinstance(embedding, list) and len(embedding) > 0:
            if isinstance(embedding[0], list):
                return embedding[0]

        return embedding

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Embedding error: {str(e)}")


def query_policies(question: str, n_results: int = 8) -> dict:

    if not DATABASE_URL:
        raise HTTPException(status_code=500, detail="DATABASE_URL missing")

    # Step 1: embed question
    question_embedding = get_query_embedding(question)

    # Step 2: vector search
    vx = vecs.create_client(DATABASE_URL)
    collection = vx.get_or_create_collection(
        name="policy_documents",
        dimension=384
    )

    results = collection.query(
        data=question_embedding,
        limit=n_results,
        measure="cosine_distance",
        include_metadata=True,
        include_value=True
    )

    if not results:
        return {
            "answer": "No relevant policy documents found.",
            "sources": []
        }

    chunks = []
    metadatas = []
    distances = []

    for record_id, distance, metadata in results:
        chunks.append(metadata.get("content", ""))
        metadatas.append(metadata)
        distances.append(distance)

    context = "\n\n---\n\n".join([
        f"[From: {meta.get('original_name', 'Unknown')}]\n{chunk}"
        for chunk, meta in zip(chunks, metadatas)
    ])

    prompt = f"""You are a compliance assistant. Answer strictly based on the policies below.

POLICIES:
{context}

QUESTION:
{question}

Answer clearly and cite reasoning from the policies."""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        max_tokens=1000,
    )

    answer = response.choices[0].message.content

    sources = [
        {
            "document_name": meta.get("original_name", "Unknown"),
            "chunk_index": meta.get("chunk_index", 0),
            "relevance_score": round(1 - distance, 3)
        }
        for meta, distance in zip(metadatas, distances)
    ]

    return {
        "answer": answer,
        "sources": sources
    }