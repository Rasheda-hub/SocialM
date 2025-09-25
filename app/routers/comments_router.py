# app/routers/comments_router.py
from fastapi import APIRouter, Depends
from ..database import get_session
from ..schemas import CommentCreate, CommentUpdate
from ..controllers import comment_controller

router = APIRouter(prefix="/comments", tags=["Comments"])

@router.post("/")
async def create_comment(user_id: str, post_id: str, comment: CommentCreate, session=Depends(get_session)):
    return await comment_controller.create_comment(session, user_id, post_id, comment.content)

@router.get("/{post_id}")
async def list_comments(post_id: str, session=Depends(get_session)):
    return await comment_controller.list_comments(session, post_id)

@router.put("/{comment_id}")
async def update_comment(comment_id: str, comment: CommentUpdate, session=Depends(get_session)):
    return await comment_controller.update_comment(session, comment_id, comment.content)

@router.delete("/{comment_id}")
async def delete_comment(comment_id: str, session=Depends(get_session)):
    return await comment_controller.delete_comment(session, comment_id)
