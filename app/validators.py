from fastapi import UploadFile, HTTPException, status
from PyPDF2 import PdfReader
from app.config import MAX_FILE_SIZE_MB, MAX_PAGES, ALLOWED_CONTENT_TYPE


def validate_pdf(file: UploadFile):
    if file.content_type != ALLOWED_CONTENT_TYPE:
        raise HTTPException( status_code=422, detail={"error_code": "INVALID_FILE_TYPE", "message": "Only PDF allowed"} )

    file.file.seek(0, 2)
    size_mb = file.file.tell() / (1024 * 1024)
    file.file.seek(0)

    if size_mb > MAX_FILE_SIZE_MB:
        raise HTTPException( status_code=413, detail={"error_code": "FILE_TOO_LARGE", "message": "File too large"} )

    reader = PdfReader(file.file)
    if len(reader.pages) > MAX_PAGES:
        raise HTTPException( status_code=422, detail={"error_code": "TOO_MANY_PAGES", "message": "Too many pages"} )
    file.file.seek(0)
