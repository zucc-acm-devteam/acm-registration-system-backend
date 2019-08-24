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

    def keys(self):
        return ['username', 'nickname', 'gender', 'college', 'profession', 'class_',
                'phone', 'qq', 'remark', 'permission']

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    @staticmethod
    def get_user_by_username(username):
        return User.query.get(username)

    @staticmethod
    def register(username, password, permission=0):
        with db.auto_commit():
            user = User()
            user.username = username
            user.password = password
            user.permission = permission
            db.session.add(user)

    @classmethod
    def modify(cls, username, **kwargs):
        user = cls.get_user_by_username(username)
        with db.auto_commit():
            for key, value in kwargs.items():
                if hasattr(cls, key):
                    setattr(user, key, value)

    @classmethod
    def search(cls, **kwargs):
        res = User.query
        for key, value in kwargs.items():
            if value and hasattr(cls, key):
                if isinstance(value, int):
                    res = res.filter(getattr(cls, key) == value)
                else:
                    res = res.filter(getattr(cls, key).like(value))

        data = {
            'count': res.count()
        }
        page = kwargs.get('page', 1)
        page_size = kwargs.get('page_size', 20)
        res = res.offset((page - 1) * page_size).limit(page_size)
        res = res.all()
        data['data'] = res
        return data

    @property
    def scope(self):
        if self.permission == 1:  # 普通用户
            return 'UserScope'
        elif self.permission == -1:  # 管理员
            return 'AdminScope'
        else:  # 未激活用户
            return 'InactivateUserScope'

    @classmethod
    def verify(cls, username, password):
        user = cls.get_user_by_username(username)
        if not user.check_password(password):
            raise AuthFailed('username or password wrong')
        return {'uid': user.username}

    def check_password(self, raw):
        if not self._password:
            return False
        return check_password_hash(self._password, raw)
