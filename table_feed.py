from sqlalchemy.orm import relationship

from database import Base
from table_post import Post
from table_user import User
from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP


class Feed(Base):
    __tablename__ = "feed_action"
    id = Column(Integer, primary_key=True)
    action = Column(String)
    time = Column(TIMESTAMP)
    user_id = Column(Integer, ForeignKey(User.id))
    user = relationship("User")
    post_id = Column(Integer, ForeignKey(Post.id))
    post = relationship("Post")