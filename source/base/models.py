from flask_login import UserMixin # 管理用户会话的模块
from sqlalchemy import Column, Integer, String
from database import Base

#  orm对象经历的状态transient, pending, and persistent.
class User(Base, UserMixin): # 继承UserMixin简便地实现用户类,配合flask-login使用

    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    username = Column(String(120))
    email = Column(String(120))
    password = Column(String(30))

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]
            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)
