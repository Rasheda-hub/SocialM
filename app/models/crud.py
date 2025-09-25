from neo4j import GraphDatabase

class CRUD:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    # ---------------- USER ----------------
    def create_user(self, name, email):
        query = """
        CREATE (u:User {name: $name, email: $email})
        RETURN u
        """
        with self.driver.session() as session:
            result = session.run(query, name=name, email=email)
            record = result.single()
            return dict(record["u"])

    # ---------------- POST ----------------
    def create_post(self, user_email, content):
        query = """
        MATCH (u:User {email: $email})
        CREATE (u)-[:POSTED]->(p:Post {content: $content, post_id: randomUUID()})
        RETURN p, u
        """
        with self.driver.session() as session:
            record = session.run(query, email=user_email, content=content).single()
            return {"post": dict(record["p"]), "author": dict(record["u"])}

    def get_post(self, post_id):
        query = """
        MATCH (u:User)-[:POSTED]->(p:Post {post_id: $post_id})
        OPTIONAL MATCH (c:Comment)-[:COMMENTED_ON]->(p)
        OPTIONAL MATCH (c)<-[:WROTE]-(commenter:User)
        RETURN p, u, collect({comment: c, commenter: commenter}) as comments
        """
        with self.driver.session() as session:
            record = session.run(query, post_id=post_id).single()
            if not record:
                return None
            post = dict(record["p"])
            author = dict(record["u"])
            comments = []
            for c in record["comments"]:
                if c["comment"] and c["commenter"]:
                    comments.append({
                        "comment": dict(c["comment"]),
                        "commenter": dict(c["commenter"])
                    })
            return {"post": post, "author": author, "comments": comments}

    # ---------------- COMMENT ----------------
    def add_comment(self, user_email, post_id, content):
        query = """
        MATCH (u:User {email: $email}), (p:Post {post_id: $post_id})
        CREATE (u)-[:WROTE]->(c:Comment {comment_id: randomUUID(), content: $content})
        CREATE (c)-[:COMMENTED_ON]->(p)
        RETURN c, u, p
        """
        with self.driver.session() as session:
            record = session.run(query, email=user_email, post_id=post_id, content=content).single()
            return {
                "comment": dict(record["c"]),
                "commenter": dict(record["u"]),
                "on_post": dict(record["p"])
            }

    # ---------------- FOLLOW ----------------
    def follow_user(self, follower_email, followee_email):
        query = """
        MATCH (a:User {email: $follower}), (b:User {email: $followee})
        CREATE (a)-[:FOLLOWS]->(b)
        RETURN a, b
        """
        with self.driver.session() as session:
            record = session.run(query, follower=follower_email, followee=followee_email).single()
            return {"follower": dict(record["a"]), "followee": dict(record["b"])}
