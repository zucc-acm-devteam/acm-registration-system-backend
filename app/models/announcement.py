from sqlalchemy import Column, Integer, ForeignKey, Text, or_
from sqlalchemy.orm import relationship
from app.models.base import Base, db


class Announcement(Base):
    id = Column(Integer, autoincrement=True, primary_key=True)
    contest_id = Column(ForeignKey('contest.id'))
    contest = relationship("app.models.contest.Contest", foreign_keys=[contest_id])
    type = Column(Integer, nullable=False)
    content = Column(Text)

    def keys(self):
        return ['id', 'contest_id', 'type', 'content']

    @staticmethod
    def create_announcement(contest_id, type_, content):
        with db.auto_commit():
            announcement = Announcement()
            announcement.contest_id = contest_id
            announcement.type = type_
            announcement.content = content
            db.session.add(announcement)
        return announcement

    @classmethod
    def search(cls, **kwargs):
        res = cls.query
        for key, value in kwargs.items():
            if value is not None and hasattr(cls, key):
                try:
                    value = int(value)
                except ValueError:
                    pass
                if isinstance(value, int):
                    if key == 'contest_id':
                        res = res.filter(or_(getattr(cls, key) == value, getattr(cls, key).is_(None)))
                    else:
                        res = res.filter(getattr(cls, key) == value)
                else:
                    res = res.filter(getattr(cls, key).like(value))

        data = {
            'count': res.count()
        }
        page = int(kwargs.get('page', 1))
        page_size = int(kwargs.get('page_size', 20))
        res = res.offset((page - 1) * page_size).limit(page_size)
        res = res.all()
        data['data'] = res
        return data
