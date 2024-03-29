from sqlalchemy import Column, Integer, ForeignKey, desc
from sqlalchemy.orm import relationship

from app.models.base import Base, db
from app.models.team import Team


class TeamRelationship(Base):
    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(ForeignKey('user.username'))
    user = relationship("app.models.user.User", foreign_keys=[username])
    team_id = Column(ForeignKey('team.id'))
    team = relationship("app.models.team.Team", foreign_keys=[team_id])

    fields = ['id', 'user', 'team']

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
        team_relationship = cls.get_by_id(id_)
        with db.auto_commit():
            db.session.delete(team_relationship)

    @classmethod
    def search(cls, **kwargs):
        res = cls.query
        for key, value in kwargs.items():
            if value is not None:
                try:
                    value = int(value)
                except ValueError:
                    pass
                if hasattr(cls, key):
                    if isinstance(value, int):
                        res = res.filter(getattr(cls, key) == value)
                    else:
                        res = res.filter(getattr(cls, key).like(value))
                elif key == 'contest_id':
                    res = res.join(Team).filter(Team.contest_id == value)

        data = {
            'count': res.count()
        }
        try:
            res = res.order_by(desc(cls.id))
        except AttributeError:
            pass
        page = int(kwargs.get('page', 1))
        page_size = int(kwargs.get('page_size', 20))
        res = res.offset((page - 1) * page_size).limit(page_size)
        res = res.all()
        data['data'] = res
        return data
