# test_relationships.py
from sqlalchemy.orm import Session
from database import SessionLocal
from models.user import User
from models.subreddit import Subreddit

def test_create_user_and_subreddit():
    db: Session = SessionLocal()
    try:
        user = User(username="john_doe")
        db.add(user)
        db.commit()
        db.refresh(user)

        subreddit = Subreddit(name="testsub", created_by=user.id)
        db.add(subreddit)
        db.commit()
        db.refresh(subreddit)

        # Check relationship
        print("User:", user.username)
        print("Subreddits:", [s.name for s in user.subreddits])  # Should include "testsub"
    finally:
        db.close()

if __name__ == "__main__":
    test_create_user_and_subreddit()
