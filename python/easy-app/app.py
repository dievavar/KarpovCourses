from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import psycopg2
import psycopg2.extras

app = FastAPI()

class PostResponse(BaseModel):
    id: int
    text: str
    topic: str

    class Config:
        orm_mode = True

def get_db():
    conn = psycopg2.connect(
        "postgresql://robot-startml-ro:pheiph0hahj1Vaif@postgres.lab.karpov.courses:6432/startml",
        cursor_factory=psycopg2.extras.RealDictCursor
    )
    try:
        yield conn
    finally:
        conn.close()

@app.get("/post/{id}", response_model=PostResponse)
def get_post(id: int, db=Depends(get_db)) -> PostResponse:
    with db.cursor() as cursor:
        cursor.execute(
            """
            SELECT id, text, topic
            FROM "post"
            WHERE id = %s
            """,
            (id,)
        )
        result = cursor.fetchone()

    if not result:
        raise HTTPException(status_code=404, detail="post not found")
    return PostResponse(**result)