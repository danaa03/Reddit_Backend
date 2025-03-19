from fastapi import FastAPI, Depends
from database import get_db
from sqlalchemy.sql import text
from sqlalchemy.orm import Session
from routes import auth

app = FastAPI(title="Reddit Clone API", description="API for a Reddit clone", version="0.1")
app.include_router(auth.router, prefix="/auth", tags=["Auth"])

@app.get("/ping")
def ping(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"message": "Database connected!"}
    except Exception as e:
        return {"error": f"Database connection failed: {str(e)}"}

