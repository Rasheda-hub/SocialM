# app/controllers/follow_controller.py

async def follow_user(session, follower_id: str, followee_id: str):
    await session.run(
        """
        MATCH (a:User {id:$fid}), (b:User {id:$foid})
        MERGE (a)-[:FOLLOWS]->(b)
        """,
        fid=follower_id, foid=followee_id
    )
    return {"message": f"User {follower_id} now follows {followee_id}"}

async def unfollow_user(session, follower_id: str, followee_id: str):
    await session.run(
        """
        MATCH (a:User {id:$fid})-[r:FOLLOWS]->(b:User {id:$foid})
        DELETE r
        """,
        fid=follower_id, foid=followee_id
    )
    return {"message": f"User {follower_id} unfollowed {followee_id}"}

async def list_followers(session, user_id: str):
    result = await session.run(
        """
        MATCH (f:User)-[:FOLLOWS]->(u:User {id:$uid})
        RETURN f.id AS id, f.username AS username, f.email AS email
        """,
        uid=user_id
    )
    return [record async for record in result]

async def list_following(session, user_id: str):
    result = await session.run(
        """
        MATCH (u:User {id:$uid})-[:FOLLOWS]->(f:User)
        RETURN f.id AS id, f.username AS username, f.email AS email
        """,
        uid=user_id
    )
    return [record async for record in result]
