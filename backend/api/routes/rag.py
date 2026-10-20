from pathlib import Path
from backend.services.rag_service import rag_service
from fastapi import APIRouter, UploadFile, File

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/upload")
async def rag_service_route(file: UploadFile = File(...)):

    file_path = UPLOAD_DIR / file.filename

    # Save uploaded file
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    print("Uploaded file:", file.filename)
    print("Saved path:", file_path)
    print("File exists:", file_path.exists())

    # Give the actual path to RAG
    return rag_service(str(file_path))