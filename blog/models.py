from datetime import datetime
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Boolean, LargeBinary, ForeignKey, Text, DateTime, func, Table
from sqlalchemy.orm import relationship
from blog.database import db
from blog.security import flask_bcrypt


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(120), unique=False, nullable=False, default="", server_default="")
    last_name = Column(String(120), unique=False, nullable=False, default="", server_default="")
    email = Column(String(255), nullable=False, default="", server_default="")
    username = Column(String(80), unique=True, nullable=False)
    is_staff = Column(Boolean, nullable=False, default=False)
    password_ = Column(LargeBinary, nullable=True)
    author = relationship("Author", uselist=False, back_populates="user")

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


article_tag_association_table = Table(
    "article_tag_association",
    db.metadata,
    Column("article_id", Integer, ForeignKey("articles.id"), nullable=False),
    Column("tag_id", Integer, ForeignKey("tag.id"), nullable=False),
    )


class Articles(db.Model, UserMixin):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False, default="", server_default="")
    body = Column(Text, nullable=False, default="", server_default="")
    dt_created = Column(DateTime, default=datetime.utcnow, server_default=func.now())
    dt_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    author_id = Column(Integer, ForeignKey("author.id"))
    author = relationship("Author", back_populates="article")

    tags = relationship(
        "Tag",
        secondary=article_tag_association_table,
        back_populates="articles",
    )

    def __str__(self):
        return self.title


class Author(db.Model):
    __tablename__ = 'author'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="author")
    article = relationship("Articles", back_populates="author")

    def __str__(self):
        return self.user.username


class Tag(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False, default="", server_default="")

    articles = relationship(
        "Articles",
        secondary=article_tag_association_table,
        back_populates="tags",
    )

    def __str__(self):
        return self.name
