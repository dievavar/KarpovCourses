from database import Base, SessionLocal
from sqlalchemy import Column, Integer, String
from sqlalchemy import func

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    age = Column(Integer)
    city = Column(String)
    country = Column(String)
    exp_group = Column(Integer)
    gender = Column(Integer)
    os = Column(String)
    source = Column(String)

 # отберите всех пользователей, у которых экспериментальная группа равна 3, сгруппируйте их по парам (country, os)
# и выведите эти пары (country, os, count(*)),
# отсортированные по убыванию COUNT(*) и имеющие COUNT(*) > 100

if __name__ == "__main__":
    session = SessionLocal()
    result = (
            session.query(
                User.country,
                User.os,
                func.count().label('count')
            )
            .filter(User.exp_group == 3)
            .group_by(User.country, User.os)
            .having(func.count() > 100)
            .order_by(func.count().desc())
            .all()
    )
    result_list = [(row.country, row.os, row.count) for row in result]
    print(result_list)

