from fastapi import Depends, FastAPI, APIRouter, HTTPException, status
from models import User, Subreddit
from sqlalchemy.orm import Session
from utils.security import get_current_user 
from models import Post 
from models import UserSubreddit
from schemas.subreddit import SubredditCreate, SubredditUpdateStatus, SubredditUpdateDescription
from schemas.userSubreddit import UserSubredditBase
from database import get_db

router = APIRouter()

@router.get("/{subreddit_name}")
def get_subreddit_posts(subreddit_name: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Retrieve all posts from a specific subreddit, but user must be authenticated."""
    subreddit = db.query(Subreddit).filter(Subreddit.name == subreddit_name).first()
    if not subreddit:
        raise HTTPException(status_code=404, detail="Subreddit not found")

    posts = db.query(Post).filter(Post.subreddit_id == subreddit.id).all()
    return {"subreddit": subreddit_name, "posts": posts}

#CRUD OPERATIONS FOR SUBREDDIT
@router.post("/create-subreddit")
def create_subreddit(
    subreddit_data: SubredditCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    existing_subreddit = db.query(Subreddit).filter(Subreddit.name == subreddit_data.name).first()
    if existing_subreddit:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Subreddit already exists")
    
    new_subreddit = Subreddit(
        name=subreddit_data.name,
        description=subreddit_data.description,
        created_by=user.id
    )

    db.add(new_subreddit)
    db.commit() #generates id
    db.refresh(new_subreddit)

    relation = UserSubreddit(
        user_id = user.id,
        subreddit_id = new_subreddit.id,
        role = "moderator"
    )

    db.add(relation)
    db.commit()
    db.refresh(relation)

    return new_subreddit

#UPDATE ROUTES
@router.post("/change-subreddit-status")
def change_subreddit_status(
    subreddit_status: SubredditUpdateStatus,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Change subreddit status -> public or private."""
    #check if the current logged in user is related to the subreddit
    relation = db.query(UserSubreddit).filter(UserSubreddit.user_id == user.id, UserSubreddit.subreddit_id == subreddit_status.subreddit_id).first()
    if not relation:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not a part of the subreddit")
    #yes, check if the user is a moderator of the subreddit
    if relation.role != "moderator":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not a moderator of the subreddit")
    #yes, update subreddit status
    subreddit = db.query(Subreddit).filter(Subreddit.id == subreddit_status.subreddit_id).first()
    if not subreddit:
        raise HTTPException(status_code=404, detail="Subreddit not found")
    subreddit.status = subreddit_status.status
    db.commit()
    db.refresh(subreddit)
    return subreddit
    
@router.post("/change-subreddit-description")
def change_subreddit_description(
    subreddit_description: SubredditUpdateDescription,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    #check if the current logged in user is related to the subreddit -> is a mod or not?
    relation = db.query(UserSubreddit).filter(UserSubreddit.user_id == user.id, UserSubreddit.subreddit_id == subreddit_description.subreddit_id, UserSubreddit.role == "moderator").first()
    if not relation:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not a moderator of the subreddit")
    #yes, update subreddit desc
    subreddit = db.query(Subreddit).filter(Subreddit.id == subreddit_description.subreddit_id).first()
    if not subreddit:
        raise HTTPException(status_code=404, detail="Subreddit not found")
    subreddit.description = subreddit_description.description
    db.commit()
    db.refresh(subreddit)
    return subreddit
    

    