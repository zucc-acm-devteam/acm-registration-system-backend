import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, desc
from sqlalchemy.orm import relationship

from app.models.base import Base, db


class Mail(Base):
    id = Column(Integer, primary_key=True)
    username = Column(String(100), ForeignKey('user.username'))
    user = relationship("app.models.user.User", foreign_keys=[username])
    recipient = Column(String(100), nullable=False)
    code = Column(Integer, nullable=False)
    create_time = Column(DateTime, nullable=False)

    @staticmethod
    def create_log(username, recipient, code):
        with db.auto_commit():
            mail = Mail()
            mail.username = username
            mail.recipient = recipient
            mail.code = code
            mail.create_time = datetime.datetime.now()
            db.session.add(mail)

    @staticmethod
    def check_code(username, code):
        mail = Mail.query.filter_by(username=username).order_by(desc(Mail.create_time)).first()
        if not mail:
            return False
        return mail.code == code
