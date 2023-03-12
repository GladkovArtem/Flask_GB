from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Boolean, LargeBinary
from sqlalchemy.orm import relationship
from blog.database import db
from blog.security import flask_bcrypt


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(120), unique=False, nullable=False, default="", server_default="")
    last_name = Column(String(120), unique=False, nullable=False, default="", server_default="")
    email = Column(String(255), nullable=False, default="", server_default="")
    username = Column(String(80), unique=True, nullable=False)
    is_staff = Column(Boolean, nullable=False, default=False)
    password_ = Column(LargeBinary, nullable=True)

    @property
    def password(self):
        return self.password_

    @password.setter
    def password(self, value):
        self.password_ = flask_bcrypt.generate_password_hash(value)

    def validate_password(self, password) -> bool:
        return flask_bcrypt.check_password_hash(self.password_, password)

    def __repr__(self):
        return f"<User #{self.id} {self.username!r}>"


class Articles(db.Model, UserMixin):
    __tablename__ = 'articles'

    title = Column(String(255), primary_key=True)
    text = Column(String)
    # author = relationship('User')
