from sqlalchemy import Column, Integer, String
from app.models.base import Base, db


class Contest(Base):
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(100), nullable=False)
    limit = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False, default=0)

    def keys(self):
        return ['id', 'name', 'limit', 'status']

    @staticmethod
    def get_contest_by_id(id_):
        return Contest.query.get(id_)

    @staticmethod
    def create_contest(name, limit, status):
        with db.auto_commit():
            contest = Contest()
            contest.name = name
            contest.limit = limit
            contest.status = status
