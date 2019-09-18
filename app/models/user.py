from sqlalchemy import Column, Integer, String, SmallInteger
from werkzeug.security import generate_password_hash, check_password_hash

from app.libs.error_code import AuthFailed
from app.models.base import Base, db


class User(Base):
    username = Column(String(100), primary_key=True)
    _password = Column('password', String(100), nullable=False)
    nickname = Column(String(100))
    gender = Column(SmallInteger)
    college = Column(String(100))
    profession = Column(String(100))
    class_ = Column('class', String(100))
    phone = Column(String(11))
    qq = Column(String(100))
    remark = Column(String(10000))
    permission = Column(Integer, nullable=False, default=0)

    fields = ['username', 'nickname', 'permission']

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    @staticmethod
    def register(username, password, permission=0):
        with db.auto_commit():
            user = User()
            user.username = username
            user.password = password
            user.permission = permission
            db.session.add(user)

    @property
    def scope(self):
        if self.permission == 0 or self.permission == 1:
            return 'IncompleteUserScope'
        elif self.permission == 2:
            return 'UserScope'
        elif self.permission == -1:
            return 'AdminScope'
        else:  # 未激活用户
            return 'IncompleteUserScope'

    @classmethod
    def verify(cls, username, password):
        user = cls.get_by_id(username)
        if not user.check_password(password):
            raise AuthFailed('username or password wrong')
        return {'uid': user.username}

    def check_password(self, raw):
        if not self._password:
            return False
        return check_password_hash(self._password, raw)
