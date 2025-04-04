from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from schemas.auth import TokenResponse
from utils.security import verify_password, create_access_token, hash_password
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from schemas.user import UserCreate, UserResponse
from models.user import User
from database import get_db
import os
from utils.security import get_current_user

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.username).first()
    if not user or not verify_password(request.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.email, "role": user.role})
     # Log the token and its payload to ensure it's formatted correctly
    print(f"Generated token: {token}")  # Log the whole token
    try:
        decoded_token = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
        print(f"Decoded token: {decoded_token}")  # Log the decoded payload
    except JWTError as e:
        print(f"Error decoding token: {e}")
    
    return {"access_token": token, "token_type": "bearer"}


@router.post("/signup", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    print(user.dict())
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
    
    return {"username": user.username, "email": user.email}

@router.get("/me", response_model=UserResponse)
def get_profile(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/logout")
def logout():
    return {"message": "Successfully logged out. Please discard the token on the client side."}
