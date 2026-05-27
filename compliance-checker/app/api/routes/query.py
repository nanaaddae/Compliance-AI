from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.query import QueryRequest, QueryResponse
from app.services.query_service import query_policies
from app.core.dependencies import require_employee
from app.models.user import User
from app.models.audit_log import AuditLog
from app.services.document_processor import collection
from app.db.database import get_db

router = APIRouter(prefix="/query", tags=["Query"])


@router.post("/", response_model=QueryResponse)
def query_compliance(
    payload: QueryRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_employee),
):
    """Any authenticated user can ask compliance questions."""

    if not payload.question.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Question cannot be empty"
        )

    if collection.count() == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No policy documents have been uploaded yet"
        )

    result = query_policies(payload.question)

    # Save to audit log
    log = AuditLog(
        user_id=current_user.id,
        question=payload.question,
        answer=result["answer"],
        sources=result["sources"],
    )
    db.add(log)
    db.commit()

    return QueryResponse(
        question=payload.question,
        answer=result["answer"],
        sources=result["sources"]
    )