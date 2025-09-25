# app/schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# ===================== USERS =====================
class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None


class UserOut(UserBase):
    id: str


# ===================== POSTS =====================
class PostBase(BaseModel):
    content: str


class PostCreate(PostBase):
    username: str   # author username


class PostUpdate(BaseModel):
    content: Optional[str] = None


class PostOut(PostBase):
    id: str
    created_at: datetime
    author: str


# ===================== COMMENTS =====================
class CommentBase(BaseModel):
    content: str


class CommentCreate(CommentBase):
    username: str
    post_id: str


class CommentUpdate(BaseModel):
    content: Optional[str] = None


class CommentOut(CommentBase):
    id: str
    created_at: datetime
    author: str
    post_id: str


# ===================== FOLLOW =====================
class FollowCreate(BaseModel):
    follower: str     # username of follower
    following: str    # username of user being followed


class FollowOut(BaseModel):
    follower: str
    following: str
