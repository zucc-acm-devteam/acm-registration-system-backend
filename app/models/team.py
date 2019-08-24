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

    def keys(self):
        return ['id', 'name', 'contest_id', 'create_username']

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    @staticmethod
    def get_team_by_id(id_):
        return Team.query.get(id_)

    def check_password(self, raw):
        if not self._password:
            return False
        return check_password_hash(self._password, raw)

    @staticmethod
    def create_team(name, contest_id, create_username):
        with db.auto_commit():
            team = Team()
            team.name = name
            team.contest_id = contest_id
            team.create_username = create_username
            db.session.add(team)
