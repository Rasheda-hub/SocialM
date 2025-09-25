from fastapi import APIRouter, Depends, HTTPException
from ..database import get_db
from ..schemas import PostCreate, PostOut

router = APIRouter(prefix="/posts", tags=["Posts"])

# Helper: convert Neo4j node -> dict
def node_to_dict(node):
    return {k: v for k, v in dict(node).items()}

# CREATE post
@router.post("/", response_model=PostOut)
async def create_post(post: PostCreate, session=Depends(get_db)):
    with session as s:
        result = s.run(
            """
            MATCH (u:User {username: $username})
            CREATE (u)-[:POSTED]->(p:Post {
                id: randomUUID(),
                content: $content,
                created_at: datetime(),
                author: $username
            })
            RETURN p
            """,
            username=post.username,   # <-- make sure PostCreate includes username
            content=post.content
        )
        record = result.single()
        if not record:
            raise HTTPException(status_code=400, detail="Post not created")

        node = record["p"]
        return {
            "id": node["id"],
            "content": node["content"],
            "created_at": str(node["created_at"]),
            "author": node["author"]
        }


# READ post
@router.get("/{post_id}", response_model=PostOut)
async def get_post(post_id: str, session=Depends(get_db)):
    result = session.run(
        "MATCH (p:Post {id: $post_id}) RETURN p",
        post_id=post_id
    )
    record = result.single()
    if not record:
        raise HTTPException(status_code=404, detail="Post not found")

    node = record["p"]
    return {
        "id": node["id"],
        "content": node["content"],
        "created_at": str(node["created_at"]),
        "author": node["author"]
    }


# UPDATE post
@router.put("/{post_id}", response_model=PostOut)
async def update_post(post_id: str, content: str, driver=Depends(get_db)):
    with driver.session() as s:
        result = s.run(
            "MATCH (p:Post {id: $post_id}) SET p.content = $content RETURN p",
            post_id=post_id,
            content=content
        )
        record = result.single()
        if not record:
            raise HTTPException(status_code=404, detail="Post not found")
        node = record["p"]
        return node_to_dict(node)

# DELETE post
@router.delete("/{post_id}", response_model=dict)
async def delete_post(post_id: str, driver=Depends(get_db)):
    with driver.session() as s:
        result = s.run(
            "MATCH (p:Post {id: $post_id}) DETACH DELETE p RETURN COUNT(p) as count",
            post_id=post_id
        )
        record = result.single()
        if record["count"] == 0:
            raise HTTPException(status_code=404, detail="Post not found")
        return {"message": f"Post {post_id} deleted"}
