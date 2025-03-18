from database import Base, engine
from models.user import User
from models.subreddit import Subreddit
from models.post import Post
from models.comment import Comment
from models.vote import Vote
from models.message import DirectMessage
from models.notification import Notification
from models.user_subreddit import UserSubreddit

# Print tables registered in Base
print("Registered Tables:", Base.metadata.tables.keys())
