import pdfplumber
import chromadb
from chromadb.config import Settings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from pathlib import Path

# Load the embedding model once at startup — this is the model that converts text to vectors
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Set up ChromaDB — runs locally, stores data in a folder called chroma_db
chroma_client = chromadb.PersistentClient(
    path="./chroma_db",
    settings=Settings(anonymized_telemetry=False)
)

# Get or create a collection — think of this like a table in ChromaDB
collection = chroma_client.get_or_create_collection(
    name="policy_documents",
    metadata={"hnsw:space": "cosine"}  # cosine similarity for semantic search
)

# Text splitter — breaks text into overlapping chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,       # each chunk is ~500 characters
    chunk_overlap=200,     # chunks overlap by 50 characters so context isn't lost at boundaries
    length_function=len,
)


def extract_text_from_pdf(file_path: str) -> str:
    """Extract all text from a PDF file."""
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()


def chunk_and_embed_document(document_id: int, file_path: str, original_name: str) -> int:
    """
    Full pipeline:
    1. Extract text from PDF
    2. Split into chunks
    3. Embed each chunk
    4. Store in ChromaDB
    Returns the number of chunks stored.
    """
    # Step 1: Extract text
    raw_text = extract_text_from_pdf(file_path)

    if not raw_text:
        raise ValueError("No text could be extracted from this PDF")

    # Step 2: Split into chunks
    chunks = text_splitter.split_text(raw_text)

    # Step 3: Embed each chunk — convert text to vectors
    embeddings = embedding_model.encode(chunks).tolist()

    # Step 4: Store in ChromaDB
    # Each chunk needs a unique ID, the embedding, the text, and metadata
    collection.add(
        ids=[f"doc_{document_id}_chunk_{i}" for i, _ in enumerate(chunks)],
        embeddings=embeddings,
        documents=chunks,
        metadatas=[{
            "document_id": document_id,
            "original_name": original_name,
            "chunk_index": i
        } for i, _ in enumerate(chunks)]
    )

    return len(chunks)


def delete_document_chunks(document_id: int):
    """Remove all chunks for a document from ChromaDB."""
    results = collection.get(where={"document_id": document_id})
    if results["ids"]:
        collection.delete(ids=results["ids"])