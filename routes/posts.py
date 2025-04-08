from fastapi import Depends, APIRouter, HTTPException, File, UploadFile, Body, Form
from typing import List, Optional
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from models import Post
from schemas.post import PostResponse
from utils.security import get_current_user
from models import User
import uuid
import os

from database import get_db

router = APIRouter()

IMAGEDIR = "images/"

@router.get("/my-posts")
def get_all_my_posts(user: User = Depends(get_current_user), db: Session = Depends(get_db), response_model=List[PostResponse]):
    """Get all posts of the authenticated user."""
    try:
        posts = db.query(Post).filter(Post.user_id == user.id).all()
        return posts
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.delete("/delete-post/{post_id}")
async def delete_post(
    post_id: str,  
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    try:
        db.delete(post)
        db.commit()
        return JSONResponse(content={"detail": "Post deleted successfully."})
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred while deleting the post")


@router.get("/{post_id}")
async def get_my_posts(post_id:str, db: Session = Depends(get_db)):
    """Get the requested post."""
    post = db.query(Post).filter(Post.id == post_id).first()
    print("RETURNING: ", post)
    return {"post": post}

@router.post("/create-post")
async def create_post(
    user: User = Depends(get_current_user),
    title: str = Form(...),
    content: Optional[str] = Form(None),
    subreddit_id: str = Form(...),
    files: List[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
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
        user_id=user.id,
        image_url=",".join(image_urls) if image_urls else None,
        subreddit_id=subreddit_id,
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


