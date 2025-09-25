# app/main.py
from fastapi import FastAPI
from app.routers import users_router, posts_router, comments_router, follow_router

app = FastAPI(title="Social Media API with FastAPI + Neo4j")

app.include_router(users_router.router)
app.include_router(posts_router.router)
app.include_router(comments_router.router)
app.include_router(follow_router.router)
