from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List, Optional

from database import SessionLocal
from schema import UserGet, PostGet, FeedGet
from table_feed import Feed
from table_post import Post
from table_user import User

app = FastAPI()

def get_db():
    with SessionLocal() as db:
        return db

@app.get("/user/{id}", response_model=UserGet)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return user

@app.get("/post/{id}", response_model=PostGet)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="post not found")
    return post

@app.get("/user/{id}/feed", response_model=List[FeedGet])
def get_user_feed(id: int, limit: int = 10, db: Session = Depends(get_db)):
    feed_actions = db.query(Feed).filter(Feed.user_id == id).order_by(Feed.time.desc()).limit(limit).all()
    if not feed_actions:
        raise HTTPException(status_code=404, detail="user not found")
    return feed_actions

@app.get("/post/{id}/feed", response_model=List[FeedGet])
def get_post_feed(id: int, limit: int = 10, db: Session = Depends(get_db)):
    feed_actions = db.query(Feed).filter(Feed.post_id == id).order_by(Feed.time.desc()).limit(limit).all()
    if not feed_actions:
        raise HTTPException(status_code=404, detail="post not found")
    return feed_actions

# Этот endpoint должен вернуть топ limit постов по количеству лайков.
@app.get("/post/recommendations/", response_model=List[PostGet])
def get_post_feed(id: int=0, limit: int = 10, db: Session = Depends(get_db)):
    top_posts = db.query(
        Post.id,
        Post.text,
        Post.topic,
        func.count(Feed.post_id).label('likes_count')
    ).join(
        Feed, Feed.post_id == Post.id
    ).filter(
        Feed.action == 'like'
    ).group_by(
        Post.id
    ).order_by(
        func.count(Feed.post_id).desc()
    ).limit(limit).all()
    if not top_posts:
        raise HTTPException(status_code=404, detail="post not found")
    return top_posts
