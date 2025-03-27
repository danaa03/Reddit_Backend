from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Vote, Post, Comment
from schemas.vote import VoteCreate
from database import get_db
from utils.security import get_current_user

router = APIRouter()

@router.post("/add-vote") #will add AND remove vote
def vote(vote: VoteCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    #either post_id or comment_id will have a value, other one will be None
    existing_vote = db.query(Vote).filter_by(
        user_id=user.id,
        post_id=vote.post_id,
        comment_id=vote.comment_id
    ).first()

    #removing vote-> if vote type same at that comment/post
    if existing_vote:
        if vote.post_id:
            post = db.query(Post).filter(Post.id==vote.post_id).first()
            if not post:
                raise HTTPException(status_code=404, detail="Post not found")
        
            if vote.vote_type == "upvote":
                post.upvotes -= 1
            else:
                post.downvotes -= 1

        elif vote.comment_id:
            comment = db.query(Comment).filter(Comment.id==vote.comment_id).first()
            if not comment:
                raise HTTPException(status_code=404, detail="Comment not found")
            else:
                if vote.vote_type == "upvote":
                    comment.upvotes -= 1
                else:
                    comment.downvotes -= 1 
        if existing_vote.vote_type == vote.vote_type:
            db.delete(existing_vote)
            db.commit()
            return {"message": "vote removed successfully"}
        #upvote or downvote
        else:
            existing_vote.vote_type = vote.vote_type
    else:
        if vote.post_id:
            post = db.query(Post).filter(Post.id==vote.post_id).first()
            if not post:
                raise HTTPException(status_code=404, detail="Post not found")
            else:
                if vote.vote_type == "upvote":
                    post.upvotes += 1
                else:
                    post.downvotes += 1
        elif vote.comment_id:
            comment = db.query(Comment).filter(Comment.id==vote.comment_id).first()
            if not comment:
                raise HTTPException(status_code=404, detail="Comment not found")
            else:
                if vote.vote_type == "upvote":
                    comment.upvotes += 1
                else:
                    comment.downvotes += 1 
        new_vote = Vote(
            user_id=user.id,
            post_id=vote.post_id,
            comment_id=vote.comment_id,
            vote_type=vote.vote_type
        )
        db.add(new_vote)
    db.commit()
    return {"message": "voted successfully"}
