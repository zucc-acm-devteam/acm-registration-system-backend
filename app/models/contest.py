from sqlalchemy import Column, Integer, String
from app.models.base import Base, db


class Contest(Base):
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(100), nullable=False)
    limit = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False, default=0)
    registration_status = Column(Integer, nullable=False, default=0)

    def keys(self):
        return ['id', 'name', 'limit', 'status', 'registration_status']

    @staticmethod
    def create_contest(name, limit):
        with db.auto_commit():
            contest = Contest()
            contest.name = name
            contest.limit = limit
            contest.status = 0
            contest.registration_status = 0
            db.session.add(contest)
        return contest

    @classmethod
    def delete_contest(cls, id_):
        contest = cls.get_by_id(id_)
        with db.auto_commit():
            db.session.delete(contest)
