from fastapi import File, UploadFile, APIRouter, HTTPException
from typing import List
import uuid
import os

IMAGEDIR = "images/"

router = APIRouter()

@router.post("/upload-image")
async def upload_image(files: List[UploadFile] = File(...)):
    contents = []
    if files:
        print("images uploaded...fk")
    try:
        for file in files:
            file.filename = f"{uuid.uuid4()}.jpg"
            contents = await file.read()

            if not os.path.exists(f"{IMAGEDIR}"):  
                os.makedirs(f"{IMAGEDIR}") 
            with open(f"{IMAGEDIR}{file.filename}", "wb") as f:
                f.write(contents)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    return {"filenames": files}