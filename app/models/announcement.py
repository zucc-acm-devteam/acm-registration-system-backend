from sqlalchemy import Column, Integer, ForeignKey, Text
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
