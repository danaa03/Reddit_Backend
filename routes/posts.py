from fastapi import Depends, FastAPI, APIRouter
from sqlalchemy.orm import Session
from models import Post
from schemas.post import CreatePost
from utils.security import get_current_user

from models import User
from database import get_db

router = APIRouter()

posts = []

    # id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    # title = Column(String, nullable=False)
    # content = Column(Text, nullable=True)
    # image_url = Column(String, nullable=True)
    # user_id = Column(String, ForeignKey("users.id"), nullable=False)
    # subreddit_id = Column(String, ForeignKey("subreddits.id"), nullable=False)
    # upvotes = Column(Integer, default=0)
    # downvotes = Column(Integer, default=0)
    # created_at = Column(TIMESTAMP, default=datetime.utcnow)

@router.get("/my-posts")
def get_my_posts(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get all posts of the authenticated user."""
    posts = db.query(Post).filter(Post.user_id == user.id).all()
    return {"user": user.username, "posts": posts}

@router.post("/create-post")
def create_post(post: CreatePost, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Create a new post."""
    new_post = Post(
        title=post.title,
        content=post.content if hasattr(post, "content") else None,
        user_id=user.id,
        image_url=post.image_url if hasattr(post, "image_url") else None,
        subreddit_id=post.subreddit_id
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


