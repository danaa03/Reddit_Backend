from fastapi import FastAPI, Depends
from database import get_db
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.sql import text
from sqlalchemy.orm import Session
from fastapi.openapi.utils import get_openapi
from routes import auth
from routes import subreddit
from routes import admin
from routes import images
from routes import posts
from routes import comments
from routes import votes
from routes import user
import uvicorn

app = FastAPI(title="Reddit Clone API", description="API for a Reddit clone", version="0.1")

origins = [
    "http://localhost:3000", 
    "http://127.0.0.1:3000",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# security_scheme = {
#     "BearerAuth": {
#         "type":"http",
#         "scheme":"bearer",
#         "bearerFormat":"JWT"
#     }
# }

# def custom_openapi():
#     if app.openapi_schema:
#         return app.openapi_schema
#     openapi_schema = get_openapi (
#         title = "Reddit API",
#         version="1.0.0",
#         description="Reddit Clone",
#         routes=app.routes,
#     )
#     openapi_schema["components"]["securitySchemas"] = security_scheme
#     openapi_schema["security"] = [{"BearerAuth": []}]
#     app.openapi_schema = openapi_schema
#     return app.openapi_schema
# app.openapi_schema= custom_openapi



app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(subreddit.router, prefix="/subreddit", tags=["SubReddit"])
app.include_router(posts.router, prefix="/posts", tags=["Posts"])
app.include_router(comments.router, prefix="/comments", tags=["Comments"])
app.include_router(user.router, prefix="/user", tags=["User"])
app.include_router(votes.router, prefix="/votes", tags=["Votes"])
app.include_router(images.router, prefix="/images", tags=["Images"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])

@app.get("/ping")
def ping(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"message": "Database connected!"}
    except Exception as e:
        return {"error": f"Database connection failed: {str(e)}"}

@app.get("/")
def read_root():
    return {"message": "Welcome to the Reddit Clone API"}

if __name__ == "__main__":
    uvicorn.run("app.api:app", host="0.0.0.0", port=8000, reload=True)
