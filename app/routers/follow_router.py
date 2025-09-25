from fastapi import APIRouter, Depends, HTTPException
from ..database import get_driver
from ..schemas import FollowCreate

router = APIRouter(prefix="/follow", tags=["Follow"])

# FOLLOW a user
@router.post("/", response_model=dict)
async def follow_user(follow: FollowCreate, driver=Depends(get_driver)):
    with driver.session() as s:
        result = s.run(
            """
            MATCH (a:User {username: $follower}), (b:User {username: $following})
            MERGE (a)-[:FOLLOWS]->(b)
            RETURN a.username AS follower, b.username AS following
            """,
            follower=follow.follower,
            following=follow.following
        )
        record = result.single()
        if not record:
            raise HTTPException(status_code=400, detail="Follow action failed")
        return {"message": f"{record['follower']} now follows {record['following']}"}

# GET followers of a user
@router.get("/{username}/followers", response_model=dict)
async def get_followers(username: str, driver=Depends(get_driver)):
    with driver.session() as s:
        results = s.run(
            """
            MATCH (u:User {username: $username})<-[:FOLLOWS]-(f:User)
            RETURN f.username AS follower
            """,
            username=username
        )
        followers = [r["follower"] for r in results]
        return {"followers": followers}

# GET following of a user
@router.get("/{username}/following", response_model=dict)
async def get_following(username: str, driver=Depends(get_driver)):
    with driver.session() as s:
        results = s.run(
            """
            MATCH (u:User {username: $username})-[:FOLLOWS]->(f:User)
            RETURN f.username AS following
            """,
            username=username
        )
        following = [r["following"] for r in results]
        return {"following": following}
