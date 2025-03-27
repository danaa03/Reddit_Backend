from pydantic import BaseModel, EmailStr
from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator
import re

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=20, pattern="^[a-zA-Z0-9_]+$")
    email: EmailStr
    password: str
    confirmPassword: str

    @field_validator("password")
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one digit.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError("Password must contain at least one special character.")
        return value
    
    @model_validator(mode="after")
    def validate_passwords_match(cls, values):
        if values.password != values.confirmPassword:
            raise ValueError("Passwords do not match.")
        return values


class UserResponse(BaseModel):
    username: str
    email: str
    access_token: str
    token_type: str

    class Config:
        from_attributes = True