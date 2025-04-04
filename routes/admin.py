from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from fastapi.responses import JSONResponse
from typing import List
from schemas.user import UserResponse  
from schemas.post import PostResponse 
from schemas.subreddit import SubredditResponse 
from database import get_db
from utils.security import get_current_admin
from models.user import User
from models.post import Post
from models.subreddit import Subreddit
from models.comment import Comment
# from models.user_subreddit import UserSubreddit

router = APIRouter()

@router.get("/stats/user-count")
async def get_user_count(current_user: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    try:
        user_count = db.query(User).count()
        return {"user_count": user_count}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error fetching user count")
    
@router.get("/stats/active-posts-count")
async def get_post_count(current_user: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    """
    Get the count of posts with a total number of upvotes, downvotes, and comments greater than zero.
    """
    try:
        comment_count_subquery = (
            db.query(Comment.post_id, func.count(Comment.id).label("comment_count"))
            .group_by(Comment.post_id)
            .subquery()
        )

        post_count = (
            db.query(Post)
            .outerjoin(comment_count_subquery, Post.id == comment_count_subquery.c.post_id)
            .filter(
                (Post.upvotes + Post.downvotes + func.coalesce(comment_count_subquery.c.comment_count, 0)) > 0
            )
            .count()
        )

        return {"post_count": post_count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching post count: {str(e)}")

@router.get("/stats/subreddit-count")
async def get_subreddits_with_posts_count(
    current_user: User = Depends(get_current_admin), 
    db: Session = Depends(get_db)
):
    """
    Get the count of subreddits that have at least one post.
    """
    try:
        subreddit_count = (
            db.query(Subreddit.id)
            .join(Post, Post.subreddit_id == Subreddit.id)
            .group_by(Subreddit.id)
            .having(func.count(Post.id) > 0)
            .count()
        )

        return {"subreddit_count": subreddit_count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching subreddits count: {str(e)}")

@router.get("/users", response_model=List[UserResponse])
async def get_users(current_user: User = Depends(get_current_admin), 
                    db: Session = Depends(get_db)):
    try:
        users = db.query(User).filter(User.role != "admin").all()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error fetching users")
    
@router.get("/posts", response_model=List[PostResponse])
async def get_posts(current_user: User = Depends(get_current_admin), 
                    db: Session = Depends(get_db)):
    try:
        posts = db.query(Post).all()
        return posts
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error fetching posts")

@router.get("/subreddits", response_model=List[SubredditResponse])
async def get_subreddits(current_user: User = Depends(get_current_admin), 
                    db: Session = Depends(get_db)):
    try:
        subreddits = db.query(Subreddit).all()
        return subreddits
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error fetching subreddits")

@router.delete("/delete-user/{user_username}")
async def delete_user(
    user_username: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    user = db.query(User).filter(User.username == user_username).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.role == "admin":
        raise HTTPException(status_code=403, detail="Cannot delete admin users")

    try:
        db.delete(user)
        db.commit()
        return JSONResponse(content={"detail": "User deleted successfully."})
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred while deleting the user")

@router.delete("/delete-post/{post_id}")
async def delete_post(
    post_id: str,  
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
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

@router.delete("/delete-subreddit/{subreddit_id}")
async def delete_subreddit(
    subreddit_id: str,  
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    print(f"Attempting to delete subreddit with ID: {subreddit_id}")
    try:
        subreddit = db.query(Subreddit).filter(Subreddit.id == subreddit_id).first()

        if not subreddit:
            raise HTTPException(status_code=404, detail="Subreddit not found")

        db.delete(subreddit)
        db.commit()
        return JSONResponse(content={"detail": "Subreddit deleted successfully."})
    
    except Exception as e:
        print(f"Error during deletion: {str(e)}") 
        db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred while deleting the subreddit")
