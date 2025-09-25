# app/controllers/user_controller.py
import uuid

async def create_user(session, user_data):
    user_id = str(uuid.uuid4())
    result = await session.run(
        "CREATE (u:User {id:$id, username:$username, email:$email}) "
        "RETURN u.id AS id, u.username AS username, u.email AS email",
        id=user_id, username=user_data.username, email=user_data.email
    )
    return await result.single()

async def list_users(session):
    result = await session.run(
        "MATCH (u:User) RETURN u.id AS id, u.username AS username, u.email AS email"
    )
    return [record async for record in result]

async def get_user(session, user_id: str):
    result = await session.run(
        "MATCH (u:User {id:$id}) RETURN u.id AS id, u.username AS username, u.email AS email",
        id=user_id
    )
    return await result.single()

async def update_user(session, user_id: str, data):
    query = """
    MATCH (u:User {id:$id})
    SET u.username = coalesce($username, u.username),
        u.email = coalesce($email, u.email)
    RETURN u.id AS id, u.username AS username, u.email AS email
    """
    result = await session.run(query, id=user_id, username=data.username, email=data.email)
    return await result.single()

async def delete_user(session, user_id: str):
    await session.run("MATCH (u:User {id:$id}) DETACH DELETE u", id=user_id)
    return {"message": f"User {user_id} deleted"}
