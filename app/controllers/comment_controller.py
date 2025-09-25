# app/controllers/comment_controller.py
import uuid
from datetime import datetime

async def create_comment(session, user_id: str, post_id: str, content: str):
    comment_id = str(uuid.uuid4())
    created_at = datetime.utcnow().isoformat()

    await session.run(
        """
        MATCH (u:User {id:$uid}), (p:Post {id:$pid})
        CREATE (c:Comment {id:$cid, content:$content, created_at:$created_at})
        CREATE (u)-[:WROTE]->(c)
        CREATE (c)-[:ON]->(p)
        """,
        uid=user_id, pid=post_id, cid=comment_id, content=content, created_at=created_at
    )
    return {"id": comment_id, "content": content, "created_at": created_at, "author": user_id, "post_id": post_id}

async def list_comments(session, post_id: str):
    result = await session.run(
        """
        MATCH (u:User)-[:WROTE]->(c:Comment)-[:ON]->(p:Post {id:$pid})
        RETURN c.id AS id, c.content AS content, c.created_at AS created_at, 
               u.username AS author, p.id AS post_id
        """,
        pid=post_id
    )
    return [record async for record in result]

async def update_comment(session, comment_id: str, content: str):
    result = await session.run(
        """
        MATCH (c:Comment {id:$cid})
        SET c.content = coalesce($content, c.content)
        RETURN c.id AS id, c.content AS content, c.created_at AS created_at
        """,
        cid=comment_id, content=content
    )
    return await result.single()

async def delete_comment(session, comment_id: str):
    await session.run("MATCH (c:Comment {id:$cid}) DETACH DELETE c", cid=comment_id)
    return {"message": f"Comment {comment_id} deleted"}
