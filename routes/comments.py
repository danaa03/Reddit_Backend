from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from models import Comment 
from schemas.comment import CommentCreate, CommentUpdate, CommentResponse
from database import get_db
from utils.security import get_current_user

router = APIRouter()

@router.post("/create-comment", response_model=CommentResponse)
def create_comment(
    comment: CommentCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    new_comment = Comment(
        content=comment.content,
        post_id=comment.post_id,
        parent_comment_id=comment.parent_comment_id,
        user_id=user.id
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

@router.get("/post/{post_id}", response_model=List[CommentResponse])
def get_comments_by_post(post_id: str, db: Session = Depends(get_db)):
    comments = db.query(Comment).filter(Comment.post_id == post_id).order_by(Comment.created_at.desc()).all()
    return comments

@router.put("/{comment_id}", response_model=CommentResponse)
def update_comment(
    comment_id: str,
    updated_data: CommentUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()

    if not comment:
        raise HTTPException(status_code=404, detail="comment not found")
    if comment.user_id != user.id:
        raise HTTPException(status_code=403, detail="not authorized")

    comment.content = updated_data.content
    db.commit()
    db.refresh(comment)
    return comment


@router.delete("/{comment_id}")
def delete_comment(
    comment_id: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()

    if not comment:
        raise HTTPException(status_code=404, detail="comment not found")
    if comment.user_id != user.id:
        raise HTTPException(status_code=403, detail="not authorized")

    db.delete(comment)
    db.commit()
    return {"message": "Comment deleted successfully"}