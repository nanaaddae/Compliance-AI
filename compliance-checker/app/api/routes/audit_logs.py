from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import datetime
from typing import Optional
from app.db.database import get_db
from app.models.audit_log import AuditLog
from app.models.user import User
from app.schemas.audit_log import AuditLogResponse, AuditLogListResponse
from app.core.dependencies import get_current_user, require_executive

router = APIRouter(prefix="/audit-logs", tags=["Audit Logs"])


@router.get("/", response_model=AuditLogListResponse)
def list_audit_logs(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    keyword: Optional[str] = Query(None),
    user_id: Optional[int] = Query(None),
    date_from: Optional[datetime] = Query(None),
    date_to: Optional[datetime] = Query(None),
    db: Session = Depends(get_db),
    _: User = Depends(require_executive),
):
    query = db.query(AuditLog)

    if keyword:
        query = query.filter(
            or_(
                AuditLog.question.ilike(f"%{keyword}%"),
                AuditLog.answer.ilike(f"%{keyword}%")
            )
        )
    if user_id:
        query = query.filter(AuditLog.user_id == user_id)
    if date_from:
        query = query.filter(AuditLog.created_at >= date_from)
    if date_to:
        query = query.filter(AuditLog.created_at <= date_to)

    total = query.count()
    logs = query.order_by(AuditLog.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return AuditLogListResponse(total=total, logs=logs)


@router.get("/me", response_model=AuditLogListResponse)
def my_audit_logs(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    keyword: Optional[str] = Query(None),
    date_from: Optional[datetime] = Query(None),
    date_to: Optional[datetime] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(AuditLog).filter(AuditLog.user_id == current_user.id)

    if keyword:
        query = query.filter(
            or_(
                AuditLog.question.ilike(f"%{keyword}%"),
                AuditLog.answer.ilike(f"%{keyword}%")
            )
        )
    if date_from:
        query = query.filter(AuditLog.created_at >= date_from)
    if date_to:
        query = query.filter(AuditLog.created_at <= date_to)

    total = query.count()
    logs = query.order_by(AuditLog.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return AuditLogListResponse(total=total, logs=logs)