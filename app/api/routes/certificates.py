from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.certificate import Certificate

router = APIRouter(
    prefix="/api/certificates",
    tags=["Certificates"],
)


@router.get("/{certificate_id}")
def download_certificate(
    certificate_id: str,
    db: Session = Depends(get_db),
):
    certificate = (
        db.query(Certificate)
        .filter(Certificate.id == certificate_id)
        .first()
    )

    if not certificate:
        raise HTTPException(
            status_code=404,
            detail="Certificate not found",
        )

    if certificate.status != "SUCCESS":
        raise HTTPException(
            status_code=400,
            detail="Certificate was not generated successfully",
        )

    if not certificate.file_path:
        raise HTTPException(
            status_code=404,
            detail="Certificate file path is missing",
        )

    file_path = Path(certificate.file_path)

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Certificate file not found",
        )

    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename=f"{certificate.recipient_name}_certificate.pdf",
    )