from groq import Groq
from app.services.document_processor import collection, embedding_model
from app.core.config import settings

client = Groq(api_key=settings.GROQ_API_KEY)


def query_policies(question: str, n_results: int = 8) -> dict:
    """
    Full RAG pipeline:
    1. Embed the question
    2. Find relevant chunks from ChromaDB
    3. Build a prompt with those chunks as context
    4. Get an answer from LLaMA via Groq
    """

    # Step 1: Embed the question
    question_embedding = embedding_model.encode(question).tolist()

    # Step 2: Search ChromaDB for the most relevant chunks
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=n_results,
        include=["documents", "metadatas", "distances"]
    )

    chunks = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    if not chunks:
        return {
            "answer": "No relevant policy documents found to answer your question.",
            "sources": []
        }

    # Step 3: Build context from retrieved chunks
    context = "\n\n---\n\n".join([
        f"[From: {meta['original_name']}]\n{chunk}"
        for chunk, meta in zip(chunks, metadatas)
    ])

    # Step 4: Build the prompt
    prompt = f"""You are a compliance assistant for a company. Answer the employee's question based strictly on the policy documents below.

    Important instructions:
    - Read ALL provided policy sections carefully before answering
    - If the answer is implied or can be inferred from the policy, explain it clearly
    - "Commuting" includes rides like Uber, Lyft, or driving from home to the office
    - If something is listed as non-reimbursable, clearly state that
    - Only say you cannot find information if the topic is truly not covered at all

    POLICY DOCUMENTS:
    {context}

    EMPLOYEE QUESTION:
    {question}

    ANSWER:"""

    # Step 5: Call Groq + LLaMA
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,  # low temperature = more factual, less creative
        max_tokens=1000,
    )

    answer = response.choices[0].message.content

    # Build sources list so the user knows where the answer came from
    sources = [
        {
            "document_name": meta["original_name"],
            "chunk_index": meta["chunk_index"],
            "relevance_score": round(1 - distance, 3)  # convert distance to similarity score
        }
        for meta, distance in zip(metadatas, distances)
    ]

    return {
        "answer": answer,
        "sources": sources
    }