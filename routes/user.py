from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from models import User 
from database import get_db  
router = APIRouter()

@router.get("/get-username-by-id/{user_id}")
def get_username_by_id(user_id: str, db: Session = Depends(get_db)):
    """Get username, given user id."""
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        return {"user": user.username}
    raise HTTPException(status_code=404, detail="User not found")
