from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os

IMAGEDIR = "images/"
router = APIRouter()

@router.get("/{file_path}")
async def return_image(file_path: str):
    print(os.path.exists(os.path.join(IMAGEDIR, file_path)))
    full_path = os.path.join(IMAGEDIR, file_path)
    if not os.path.exists(full_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(full_path)