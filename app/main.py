from fastapi import FastAPI

from app.core.database import Base, engine
from app.models import Certificate, GenerationJob

from app.api.routes.generation import router as generation_router
from app.api.routes.certificates import router as certificate_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Bulk Certificate Generator API",
    version="1.0.0",
    description="Backend API for bulk certificate generation and tracking.",
)


app.include_router(generation_router)
app.include_router(certificate_router)


@app.get("/")
def root():
    return {
        "message": "Bulk Certificate Generator API is running"
    }
