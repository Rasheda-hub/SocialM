# app/routers/follow_router.py
from fastapi import APIRouter, Depends
from ..database import get_session
from ..controllers import follow_controller

router = APIRouter(prefix="/follows", tags=["Follows"])

@router.post("/{follower_id}/{followee_id}")
async def follow_user(follower_id: str, followee_id: str, session=Depends(get_session)):
    return await follow_controller.follow_user(session, follower_id, followee_id)

@router.delete("/{follower_id}/{followee_id}")
async def unfollow_user(follower_id: str, followee_id: str, session=Depends(get_session)):
    return await follow_controller.unfollow_user(session, follower_id, followee_id)

@router.get("/{user_id}/followers")
async def list_followers(user_id: str, session=Depends(get_session)):
    return await follow_controller.list_followers(session, user_id)

@router.get("/{user_id}/following")
async def list_following(user_id: str, session=Depends(get_session)):
    return await follow_controller.list_following(session, user_id)
