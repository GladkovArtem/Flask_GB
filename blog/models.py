from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from blog.database import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(255))
    username = Column(String(80), unique=True, nullable=False)
    password = Column(String(255))
    is_staff = Column(Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"<User #{self.id} {self.username!r}>"


class Articles(db.Model, UserMixin):
    __tablename__ = 'articles'

    title = Column(String(255), primary_key=True)
    text = Column(String)
    # author = relationship('User')
