from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from app.models.base import Base, db


class Team(Base):
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(100), nullable=False)
    contest_id = Column(ForeignKey('contest.id'))
    contest = relationship("app.models.contest.Contest", foreign_keys=[contest_id])
    create_username = Column(ForeignKey('user.username'))
    create_user = relationship("app.models.user.User", foreign_keys=[create_username])
    _password = Column('password', String(100), nullable=False)
    status = Column(Integer, nullable=False, default=0)

    def keys(self):
        return ['id', 'name', 'contest_id', 'create_username']

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    def check_password(self, raw):
        if not self._password:
            return False
        return check_password_hash(self._password, raw)

    @staticmethod
    def create_team(name, contest_id, create_username, password):
        with db.auto_commit():
            team = Team()
            team.name = name
            team.contest_id = contest_id
            team.create_username = create_username
            team.password = password
            team.status = 0
            db.session.add(team)
        return team
