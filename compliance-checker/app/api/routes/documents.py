from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session
from pathlib import Path
import shutil
import uuid

from app.db.database import get_db
from app.models.document import Document
from app.models.user import User
from app.schemas.document import DocumentResponse, DocumentListResponse
from app.core.dependencies import get_current_user, require_compliance_officer
from app.services.document_processor import chunk_and_embed_document, delete_document_chunks

router = APIRouter(prefix="/documents", tags=["Documents"])

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/upload", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
def upload_document(
    file: UploadFile = File(...),
    description: str = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_compliance_officer),
):
    """Compliance officers only — upload a policy PDF."""

    # Validate file type
    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are supported"
        )

    # Save file to disk with a unique name to avoid collisions
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = UPLOAD_DIR / unique_filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Save document record to database
    document = Document(
        filename=unique_filename,
        original_name=file.filename,
        description=description,
        uploaded_by=current_user.id,
    )
    db.add(document)
    db.commit()
    db.refresh(document)

    # Process PDF — extract, chunk, embed, store in ChromaDB
    try:
        chunk_count = chunk_and_embed_document(
            document_id=document.id,
            file_path=str(file_path),
            original_name=file.filename,
        )
        print(f"Document {document.id} processed: {chunk_count} chunks stored")
    except Exception as e:
        # If processing fails, clean up and roll back
        db.delete(document)
        db.commit()
        file_path.unlink(missing_ok=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process document: {str(e)}"
        )

    return document


@router.get("/", response_model=DocumentListResponse)
def list_documents(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """Any authenticated user can see available policy documents."""
    documents = db.query(Document).filter(Document.is_active == True).all()
    return DocumentListResponse(total=len(documents), documents=documents)


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_compliance_officer),
):
    """Compliance officers only — delete a document."""
    document = db.query(Document).filter(Document.id == document_id).first()

    if not document:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")

    # Remove from ChromaDB
    delete_document_chunks(document_id)

    # Remove file from disk
    file_path = UPLOAD_DIR / document.filename
    file_path.unlink(missing_ok=True)

    # Remove from database
    db.delete(document)
    db.commit()