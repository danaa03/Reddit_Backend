from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Vote, Post, Comment
from schemas.vote import VoteCreate
from database import get_db
from utils.security import get_current_user


router = APIRouter()
@router.post("/add-vote")  # will add AND remove vote
def vote(vote: VoteCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    existing_vote = db.query(Vote).filter_by(
        user_id=user.id,
        post_id=vote.post_id,
        comment_id=vote.comment_id
    ).first()

    target = None

    if vote.post_id:
        target = db.query(Post).filter(Post.id == vote.post_id).first()
    elif vote.comment_id:
        target = db.query(Comment).filter(Comment.id == vote.comment_id).first()

    if not target:
        raise HTTPException(status_code=404, detail="Post or Comment not found")

    if existing_vote:
        #if vote type of existing vote and new vote same -> decrement existing vote_type's count
        if existing_vote.vote_type == vote.vote_type:
            if vote.vote_type == "upvote":
                target.upvotes -= 1
            else:
                target.downvotes -= 1

            db.delete(existing_vote)
            db.commit()
            return {"message": "vote removed successfully"}

        #if vote type of existing vote different -> increment new vote_type's count AND decrement opposite vote_type's count
        else:
            if existing_vote.vote_type == "upvote":
                target.upvotes -= 1
                target.downvotes += 1
            else:
                target.downvotes -= 1
                target.upvotes += 1

            existing_vote.vote_type = vote.vote_type

    #->vote doesnt already exist: simply increment
    else:
        if vote.vote_type == "upvote":
            target.upvotes += 1
        else:
            target.downvotes += 1

        new_vote = Vote(
            user_id=user.id,
            post_id=vote.post_id,
            comment_id=vote.comment_id,
            vote_type=vote.vote_type
        )
        db.add(new_vote)

    db.commit()
    return {"message": "voted successfully"}
