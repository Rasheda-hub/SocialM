# app/routers/posts_router.py
from fastapi import APIRouter, Depends
from ..database import get_session
from ..schemas import PostCreate, PostUpdate
from ..controllers import post_controller

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.post("/")
async def create_post(author_id: str, post: PostCreate, session=Depends(get_session)):
    return await post_controller.create_post(session, author_id, post.content)

@router.get("/")
async def get_posts(session=Depends(get_session)):
    return await post_controller.list_posts(session)

@router.get("/{post_id}")
async def get_post(post_id: str, session=Depends(get_session)):
    return await post_controller.get_post(session, post_id)

@router.put("/{post_id}")
async def update_post(post_id: str, post: PostUpdate, session=Depends(get_session)):
    return await post_controller.update_post(session, post_id, post.content)

@router.delete("/{post_id}")
async def delete_post(post_id: str, session=Depends(get_session)):
    return await post_controller.delete_post(session, post_id)
