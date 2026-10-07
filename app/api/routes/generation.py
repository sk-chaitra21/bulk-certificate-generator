from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.certificate import Certificate
from app.models.generation_job import GenerationJob
from app.schemas.generation import GenerationRequest
from app.services.certificate_service import generate_certificate

router = APIRouter(
    prefix="/api/generation-jobs",
    tags=["Generation Jobs"],
)


@router.post("/")
def create_generation_job(
    request: GenerationRequest,
    db: Session = Depends(get_db),
):
    job = GenerationJob(
        total_count=len(request.recipients),
        status="PROCESSING",
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    success_count = 0
    failure_count = 0

    for recipient in request.recipients:
        certificate = Certificate(
            job_id=job.id,
            recipient_name=recipient.name,
            recipient_email=recipient.email,
            event_name=request.event_name,
            status="PROCESSING",
        )

        db.add(certificate)
        db.commit()
        db.refresh(certificate)

        try:
            file_path = generate_certificate(
                certificate_id=certificate.id,
                recipient_name=recipient.name,
                event_name=recipient.event_name if hasattr(recipient, "event_name") else request.event_name,
                issue_date=str(request.issue_date),
            )

            certificate.status = "SUCCESS"
            certificate.file_path = file_path
            success_count += 1

        except Exception as error:
            certificate.status = "FAILED"
            certificate.error_message = str(error)
            failure_count += 1

        db.commit()

    job.success_count = success_count
    job.failure_count = failure_count

    if failure_count == 0:
        job.status = "COMPLETED"
    elif success_count > 0:
        job.status = "PARTIAL"
    else:
        job.status = "FAILED"

    db.commit()
    db.refresh(job)

    return {
        "job_id": job.id,
        "status": job.status,
        "total_count": job.total_count,
        "success_count": job.success_count,
        "failure_count": job.failure_count,
    }


@router.get("/{job_id}")
def get_generation_job(
    job_id: str,
    db: Session = Depends(get_db),
):
    job = (
        db.query(GenerationJob)
        .filter(GenerationJob.id == job_id)
        .first()
    )

    if not job:
        return {
            "error": "Generation job not found"
        }

    return {
        "job_id": job.id,
        "status": job.status,
        "total_count": job.total_count,
        "success_count": job.success_count,
        "failure_count": job.failure_count,
        "created_at": job.created_at,
    }


@router.get("/{job_id}/certificates")
def get_job_certificates(
    job_id: str,
    db: Session = Depends(get_db),
):
    job = (
        db.query(GenerationJob)
        .filter(GenerationJob.id == job_id)
        .first()
    )

    if not job:
        return {
            "error": "Generation job not found"
        }

    certificates = (
        db.query(Certificate)
        .filter(Certificate.job_id == job_id)
        .all()
    )

    return {
        "job_id": job_id,
        "certificates": [
            {
                "certificate_id": certificate.id,
                "recipient_name": certificate.recipient_name,
                "recipient_email": certificate.recipient_email,
                "status": certificate.status,
                "download_url": (
                    f"/api/certificates/{certificate.id}"
                    if certificate.status == "SUCCESS"
                    else None
                ),
                "error": certificate.error_message,
            }
            for certificate in certificates
        ],
    }