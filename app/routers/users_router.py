from fastapi import APIRouter, HTTPException, Depends
from neo4j import GraphDatabase
from app.schemas import UserCreate, UserOut
from app.database import get_driver
from pydantic import BaseModel

router = APIRouter(prefix="/users", tags=["Users"])

# Helper function: convert Neo4j node -> dict
def node_to_dict(node):
    # Neo4j returns a Node object, which can be converted to dict via .items()
    return dict(node)

# CREATE user
@router.post("/", response_model=UserOut)
async def create_user(user: UserCreate, driver=Depends(get_driver)):
    with driver.session() as s:
        # Check if username already exists
        exists = s.run(
            "MATCH (u:User {username: $username}) RETURN u",
            username=user.username
        ).single()
        if exists:
            raise HTTPException(status_code=409, detail="Username already exists")
        result = s.run(
            """
            CREATE (u:User {id: randomUUID(), username: $username, email: $email})
            RETURN u
            """,
            username=user.username,
            email=user.email
        )
        record = result.single()
        if not record:
            raise HTTPException(status_code=400, detail="User not created")
        node = record["u"]
        return node_to_dict(node)

# READ user
@router.get("/{username}", response_model=UserOut)
async def get_user(username: str, driver=Depends(get_driver)):
    with driver.session() as s:
        result = s.run("MATCH (u:User {username: $username}) RETURN u", username=username)
        record = result.single()
        if not record:
            raise HTTPException(status_code=404, detail="User not found")
        node = record["u"]
        return node_to_dict(node)

# UPDATE user
class UserUpdate(BaseModel):
    email: str

@router.put("/{username}", response_model=UserOut)
async def update_user(username: str, user: UserUpdate, driver=Depends(get_driver)):
    with driver.session() as s:
        # Check if user exists
        exists = s.run(
            "MATCH (u:User {username: $username}) RETURN u",
            username=username
        ).single()
        if not exists:
            raise HTTPException(status_code=404, detail="User not found")
        result = s.run(
            "MATCH (u:User {username: $username}) SET u.email = $email RETURN u",
            username=username,
            email=user.email
        )
        record = result.single()
        node = record["u"]
        return node_to_dict(node)

# DELETE user
@router.delete("/{username}", response_model=dict)
async def delete_user(username: str, driver=Depends(get_driver)):
    with driver.session() as s:
        # Check if user exists
        result = s.run(
            "MATCH (u:User {username: $username}) RETURN u",
            username=username
        )
        record = result.single()
        if not record:
            raise HTTPException(status_code=404, detail="User not found")
        # Delete user
        s.run(
            "MATCH (u:User {username: $username}) DETACH DELETE u",
            username=username
        )
        return {"message": f"User {username} deleted"}