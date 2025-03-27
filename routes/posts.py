from fastapi import Depends, APIRouter, HTTPException, File, UploadFile, Body, Form
from typing import List, Optional
from sqlalchemy.orm import Session
from models import Post
from utils.security import get_current_user
from models import User
import uuid
import os

from database import get_db

router = APIRouter()

IMAGEDIR = "images/"

@router.get("/my-posts")
def get_my_posts(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get all posts of the authenticated user."""
    posts = db.query(Post).filter(Post.user_id == user.id).all()
    return {"user": user.username, "posts": posts}

# @router.post("/upload-image")
# async def upload_image(files: List[UploadFile] = File(None)):
#     attachments = []
#     try:
#         for file in files:
#             file.filename = f"{uuid.uuid4()}.jpg"
#             contents = await file.read()

#             if not os.path.exists(f"{IMAGEDIR}"):  
#                 os.makedirs(f"{IMAGEDIR}") 
#             with open(f"{IMAGEDIR}{file.filename}", "wb") as f:
#                 f.write(contents)
        
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
#     return {"filenames": files}

@router.post("/create-post")
async def create_post(
    title: str = Form(...),
    content: Optional[str] = Form(None),
    subreddit_id: str = Form(...),
    files: List[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    user_id = "6d81a0f3-f183-4b75-8b39-e166612e29db"
    """Create a new post."""
    image_urls = []
    contents = []
    if files:
        try:
            for file in files:
                _, ext = os.path.splitext(file.filename)
                file.filename = f"{uuid.uuid4()}{ext}"
                contents = await file.read()

                if not os.path.exists(f"{IMAGEDIR}"):  
                    os.makedirs(f"{IMAGEDIR}") 
                with open(f"{IMAGEDIR}{file.filename}", "wb") as f:
                    f.write(contents)
                image_urls.append(file.filename)
                print(image_urls)
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    new_post = Post(
        title=title,
        content=content,
        user_id=user_id,
        image_url=",".join(image_urls) if image_urls else None,
        subreddit_id=subreddit_id,
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


