from fastapi import Depends, FastAPI, APIRouter, HTTPException, status, Query
from typing import List
from models import User, Subreddit
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from utils.security import get_current_user 
from models import Post 
from models import UserSubreddit
from schemas.subreddit import SubredditCreate, SubredditUpdateStatus, SubredditUpdateDescription, SubredditResponse, FollowSubreddit
from database import get_db

router = APIRouter()

@router.get("/get-all")
def get_subreddit_posts(db: Session = Depends(get_db)):
    """Retrieve all subreddits"""
    subreddits = db.query(Subreddit).all()
    if not subreddits:
        raise HTTPException(status_code=404, detail="Subreddits not found")

    return {"subreddits": subreddits}

@router.get("/display-all")
def get_subreddit_posts(db: Session = Depends(get_db)):
    """Retrieve all subreddits' names and posts"""
    subreddits = db.query(Subreddit).all()
    if not subreddits:
        raise HTTPException(status_code=404, detail="Subreddits not found")
        return
    subreddit_names=[]

    for subreddit in subreddits:
        subreddit_names.append(subreddit.name)
    return {"subreddit names": subreddit_names}

@router.post("/follow")
def toggle_follow(
    request: FollowSubreddit,
    db: Session = Depends(get_db), 
    user: User = Depends(get_current_user)
):
    membership = db.query(UserSubreddit).filter(
        UserSubreddit.user_id == user.id, 
        UserSubreddit.subreddit_id == request.subreddit_id
    ).first()

    subreddit_status = db.query(Subreddit).filter(Subreddit.id==request.subreddit_id).first()

    if membership:
        if membership.role == "moderator":
            return HTTPException(status_code=403, detail="Moderators cannot unfollow the subreddit.")
        else:
            db.delete(membership)
            db.commit()
            return {"message": "Unfollowed", "status": "Non-member"}
    else:
            new_follow = UserSubreddit(user_id=user.id, subreddit_id=request.subreddit_id, role="member")
            db.add(new_follow)
            db.commit()
            return {"message": "Followed", "status": "member"}
        # else:
        #     new_follow = UserSubreddit(user_id=user.id, subreddit_id=request.subreddit_id, role="pending")
        #     db.add(new_follow)
        #     db.commit()
        #     return {"message": "Followed", "status": "pending"}

@router.get("/membership-status/{subreddit_id}")
def get_membership_status(
    subreddit_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)  
):
    is_member = db.query(UserSubreddit).filter(
        UserSubreddit.user_id == user.id,
        UserSubreddit.subreddit_id == subreddit_id
    ).first()
    
    return {"status": is_member.role if is_member else "Non-member"}

@router.get("/top-six-reddits-most-recent-posts-joined")
def get_most_recent_post_joined(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)  
):
    """
    Retrieve the most recent posts from the top six subreddits the user has joined.
    """
    # subreddit_ids = []
    posts = []

    if user:
        #user's joined subreddits (both private and public)
        joined_subreddits = (
            db.query(Subreddit.id)
            .join(UserSubreddit, UserSubreddit.subreddit_id == Subreddit.id)
            .filter(UserSubreddit.user_id == user.id)
            .all()
        )

        if not joined_subreddits:
            return {
                    "message": "User has not joined any subreddits. Showing recommended public subreddits.",
                    "posts": []
            }

        # subreddit_hits = (
        #     db.query(
        #         Subreddit.id
        #     )
        #     .join(Post, Post.subreddit_id == Subreddit.id)
        #     .filter(Subreddit.id.in_([sub.id for sub in joined_subreddits]))
        #     .group_by(Subreddit.id)
        #     .order_by(func.sum(Post.upvotes + Post.downvotes).desc())
        #     .limit(6)
        #     .all()
        # )

        # subreddit_ids = [sub.id for sub in subreddit_hits]

        # if not subreddit_ids:
        #     raise HTTPException(status_code=404, detail="No posts found in the user's joined subreddits")
        empty_joined = []
        for subreddit in joined_subreddits:
            post = (
                db.query(Post)
                .filter(Post.subreddit_id == subreddit.id)
                .order_by(Post.created_at.desc())
                .first()
            )
            if post:
                posts.append(post)
                print(post.content)
            else: empty_joined.append(subreddit.id)

        if not posts:
            raise HTTPException(status_code=404, detail="No posts found for the selected subreddits")

    return {"posts": posts, "empty_joined": empty_joined}


@router.get("/top-six-reddits-most-recent-posts-public")
def get_most_recent_post_public(
    db: Session = Depends(get_db) 
):
    """
    Retrieve the most recent posts from the top six public subreddits.
    """
    subreddit_ids = []
    posts = []

    public_subreddits = (
        db.query(
            Subreddit.id
        )
        .join(Post, Post.subreddit_id == Subreddit.id)
        .filter(Subreddit.status == "public")
        .group_by(Subreddit.id)
        .order_by(func.sum(Post.upvotes + Post.downvotes).desc())
        .limit(6)
        .all()
    )

    if not public_subreddits:
        raise HTTPException(status_code=404, detail="No public subreddits found")

    subreddit_ids = [sub.id for sub in public_subreddits]

    if not subreddit_ids:
        raise HTTPException(status_code=404, detail="No subreddits found")

    for subreddit_id in subreddit_ids:
        post = (
            db.query(Post)
            .filter(Post.subreddit_id == subreddit_id)
            .order_by(Post.created_at.desc())
            .first()
        )
        if post:
            posts.append(post)

    if not posts:
        raise HTTPException(status_code=404, detail="No posts found for the selected public subreddits")

    return {"posts": posts}



@router.get("/{subreddit_id}")
def get_subreddit_posts_by_id(subreddit_id: str, db: Session = Depends(get_db)):
    """Retrieve the latest 50 posts from a subreddit, ordered by creation time."""
    subreddit = db.query(Subreddit).filter(Subreddit.id == subreddit_id).first()
    if not subreddit:
        raise HTTPException(status_code=404, detail="Subreddit not found")

    posts = (
        db.query(Post)
        .filter(Post.subreddit_id == subreddit.id)
        .order_by(Post.created_at.desc())  
        .limit(50)
        .all()
    )

    return {"subreddit": subreddit_id, "posts": posts}


@router.post("/create-subreddit")
def create_subreddit(
    subreddit_data: SubredditCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    existing_subreddit = db.query(Subreddit).filter(Subreddit.name == subreddit_data.name).first()
    if existing_subreddit:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Subreddit already exists")
    
    new_subreddit = Subreddit(
        name='r/'+subreddit_data.name,
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
    
# @router.get("/search/{subreddit_name}")
# def get_subreddit(subreddit_name: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
#     """Retrieve all posts from a specific subreddit, but user must be authenticated."""
#     subreddit = db.query(Subreddit).filter(Subreddit.name == subreddit_name).first()
#     if not subreddit:
#         raise HTTPException(status_code=404, detail="Subreddit not found")

#     posts = db.query(Post).filter(Post.subreddit_id == subreddit.id).all()
#     return {"subreddit": subreddit_name, "posts": posts}

@router.get("/user-status")
def get_subreddit(subreddit_name: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Retrieve all posts from a specific subreddit, but user must be authenticated."""
    subreddit = db.query(Subreddit).filter(Subreddit.name == subreddit_name).first()
    if not subreddit:
        raise HTTPException(status_code=404, detail="Subreddit not found")

    posts = db.query(Post).filter(Post.subreddit_id == subreddit.id).all()
    return {"subreddit": subreddit_name, "posts": posts}

@router.get("/details-by-id/{id}")
def get_subreddit_name_by_id(id: str, db: Session = Depends(get_db)):
    """Retrieve the subreddit's name and status, given its id."""
    print('subreddit id received is: ', id)
    subreddit = db.query(Subreddit).filter(Subreddit.id == id).first()
    if not subreddit:
        raise HTTPException(status_code=404, detail="Subreddit not found")
    return {"name": subreddit.name, "status": subreddit.status}