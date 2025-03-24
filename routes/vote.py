from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Vote
from schemas import VoteCreate
from database import get_db
from utils.security import get_current_user

router = APIRouter()

@router.post("/vote")
def vote(vote: VoteCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    #either post_id or comment_id will have a value, other one will be None
    existing_vote = db.query(Vote).filter_by(
        user_id=user.id,
        post_id=vote.post_id,
        comment_id=vote.comment_id
    ).first()

    #removing vote-> if vote type same at that comment/post
    if existing_vote:
        if existing_vote.vote_type == vote.vote_type:
            db.delete(existing_vote)
            db.commit()
            return {"message": "vote removed successfully"}
        #upvote or downvote
        else:
            existing_vote.vote_type = vote.vote_type
    else:
        new_vote = Vote(
            user_id=user.id,
            post_id=vote.post_id,
            comment_id=vote.comment_id,
            vote_type=vote.vote_type
        )
        db.add(new_vote)

    db.commit()
    return {"message": "voted successfully"}
