# app/controllers/post_controller.py
import uuid
from datetime import datetime

async def create_post(session, author_id, content):
    post_id = str(uuid.uuid4())
    created_at = datetime.utcnow().isoformat()

    await session.run(
        "MATCH (u:User {id:$uid}) "
        "CREATE (p:Post {id:$pid, content:$content, created_at:$created_at}) "
        "CREATE (u)-[:CREATED]->(p)",
        uid=author_id, pid=post_id, content=content, created_at=created_at
    )
    return {"id": post_id, "content": content, "created_at": created_at, "author": author_id}

async def list_posts(session):
    result = await session.run(
        "MATCH (u:User)-[:CREATED]->(p:Post) "
        "RETURN p.id AS id, p.content AS content, p.created_at AS created_at, u.username AS author"
    )
    return [record async for record in result]

async def get_post(session, post_id: str):
    result = await session.run(
        "MATCH (u:User)-[:CREATED]->(p:Post {id:$id}) "
        "RETURN p.id AS id, p.content AS content, p.created_at AS created_at, u.username AS author",
        id=post_id
    )
    return await result.single()

async def update_post(session, post_id: str, content: str):
    query = """
    MATCH (p:Post {id:$id})
    SET p.content = coalesce($content, p.content)
    RETURN p.id AS id, p.content AS content, p.created_at AS created_at
    """
    result = await session.run(query, id=post_id, content=content)
    return await result.single()

async def delete_post(session, post_id: str):
    await session.run("MATCH (p:Post {id:$id}) DETACH DELETE p", id=post_id)
    return {"message": f"Post {post_id} deleted"}
