# app/routers/users_router.py
from fastapi import APIRouter, Depends
from ..database import get_session
from ..schemas import UserCreate, UserUpdate
from ..controllers import user_controller

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/")
async def create_user(user: UserCreate, session=Depends(get_session)):
    return await user_controller.create_user(session, user)

@router.get("/")
async def get_users(session=Depends(get_session)):
    return await user_controller.list_users(session)

@router.get("/{user_id}")
async def get_user(user_id: str, session=Depends(get_session)):
    return await user_controller.get_user(session, user_id)

@router.put("/{user_id}")
async def update_user(user_id: str, user: UserUpdate, session=Depends(get_session)):
    return await user_controller.update_user(session, user_id, user)

@router.delete("/{user_id}")
async def delete_user(user_id: str, session=Depends(get_session)):
    return await user_controller.delete_user(session, user_id)
