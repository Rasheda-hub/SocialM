from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db
from ..schemas import CommentCreate

router = APIRouter(prefix="/comments", tags=["Comments"])

# CREATE comment
@router.post("/", response_model=dict)
async def create_comment(comment: CommentCreate, session=Depends(get_db)):
    with session as s:
        result = s.run(
            """
            MATCH (u:User {username: $username}), (p:Post {id: $post_id})
            CREATE (u)-[:COMMENTED]->(c:Comment {
                id: randomUUID(),
                text: $text,
                created_at: datetime()
            })-[:ON]->(p)
            RETURN c, u.username AS username
            """,
            username=comment.username,
            post_id=comment.post_id,
            text=comment.text
        )
        record = result.single()
        if not record:
            raise HTTPException(status_code=400, detail="Comment not created")
        
        return {
            "message": "Comment added",
            "comment": {
                "id": record["c"]["id"],
                "text": record["c"]["text"],
                "username": record["username"],
                "created_at": record["c"]["created_at"]
            }
        }

# GET comments on a post
@router.get("/{post_id}", response_model=dict)
async def get_comments(post_id: str, session=Depends(get_db)):
    with session as s:
        results = s.run(
            """
            MATCH (u:User)-[:COMMENTED]->(c:Comment)-[:ON]->(p:Post {id: $post_id})
            RETURN c.id AS id, c.text AS text, c.created_at AS created_at, u.username AS username
            ORDER BY c.created_at ASC
            """,
            post_id=post_id
        )
        comments = [
            {
                "id": r["id"],
                "text": r["text"],
                "username": r["username"],
                "created_at": r["created_at"]
            }
            for r in results
        ]
        return {"comments": comments}
