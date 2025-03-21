from fastapi import APIRouter, Depends, HTTPException, status
from schemas.auth import LoginRequest, TokenResponse
from utils.security import verify_password, create_access_token, hash_password
from sqlalchemy.orm import Session
from schemas.user import UserCreate, UserResponse
from models.user import User
from database import get_db

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.email == request.email).first()
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if not verify_password(request.password, existing_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
    token = create_access_token({"sub": existing_user.email})

    return {"access_token": token, "token_type": "bearer"}


@router.post("/signup", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
   
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    new_user = User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token({"user_id": new_user.email})
    
    return {"username": user.username, "email": user.email, "access_token": token, "token_type": "bearer"}

@router.post("/logout")
def logout():
    return {"message": "Successfully logged out. Please discard the token on the client side."}
