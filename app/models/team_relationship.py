from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base, db


class TeamRelationship(Base):
    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(ForeignKey('user.username'))
    team_id = Column(ForeignKey('team.id'))
    team = relationship("app.models.team.Team", foreign_keys=[team_id])

    def keys(self):
        return ['id', 'username', 'team_id']

    @staticmethod
    def create_team_relationship(username, team_id):
        with db.auto_commit():
            team_relationship = TeamRelationship()
            team_relationship.username = username
            team_relationship.team_id = team_id
            db.session.add(team_relationship)
        return team_relationship

    @classmethod
    def delete_team_relationship(cls, id_):
        with db.auto_commit():
            team_relationship = cls.get_by_id(id_)
            db.session.delete(team_relationship)
