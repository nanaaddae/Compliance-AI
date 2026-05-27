from pydantic import BaseModel


class QueryRequest(BaseModel):
    question: str


class SourceResponse(BaseModel):
    document_name: str
    chunk_index: int
    relevance_score: float


class QueryResponse(BaseModel):
    question: str
    answer: str
    sources: list[SourceResponse]