# app/schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional

# ---- USERS ----
class UserCreate(BaseModel):
    username: str
    email: EmailStr

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None

class UserOut(BaseModel):
    id: str
    username: str
    email: EmailStr

# ---- POSTS ----
class PostCreate(BaseModel):
    content: str

class PostUpdate(BaseModel):
    content: Optional[str] = None

class PostOut(BaseModel):
    id: str
    content: str
    created_at: str
    author: str

# ---- COMMENTS ----
class CommentCreate(BaseModel):
    content: str

class CommentUpdate(BaseModel):
    content: Optional[str] = None

class CommentOut(BaseModel):
    id: str
    content: str
    created_at: str
    author: str
    post_id: str
