from database import Base, SessionLocal
from sqlalchemy import Column, Integer, String


class Post(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True)
    text = Column(String)
    topic = Column(String)


# Используя класс Post из предыдущего степа, отберите все посты с topic = "business",
# отсортируйте их по убыванию их id и возьмите первые 10 id.
# Сделайте это все через ORM и sqlalchemy и распечатайте результат в виде списка из чисел.
# Например, [5, 4, 3, 2, 1]
if __name__ == "__main__":
    session = SessionLocal()
    result = (
        session.query(Post)
        .filter(Post.topic == 'business')
        .order_by(Post.id.desc())
        .limit(10)
        .all()
    )
    topic_ids = [int(i.id) for i in result]
    print(topic_ids)



