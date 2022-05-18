from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy import Column, Integer, String, DateTime, create_engine, select
from datetime import datetime
from flask_login import UserMixin
import os

Base = declarative_base()

if path := os.getenv("database"):
    DATABASE_PATH = path
else:
    DATABASE_PATH = "sqlite:///data_db.sqlite3"


ENGINE = create_engine(DATABASE_PATH, future=True)
db_session = sessionmaker(bind=ENGINE)


class Website(Base):
    __tablename__ = "websites"
    id = Column(Integer, primary_key=True)
    domain = Column(String(255), unique=True)
    created = Column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return self.domain


class PageVisit(Base):
    __tablename__ = "page_visits"

    id = Column(Integer, primary_key=True)
    page = Column(String(255))
    referer = Column(String(255))
    loadtime = Column(Integer)
    ip = Column(String(255))
    country = Column(String(255))
    countryCode = Column(String(10))
    state = Column(String(255))
    city = Column(String(255))
    time = Column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.id=},{self.page}"


class FormSubmit(Base):
    __tablename__ = "form_submit"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    page = Column(String(255))
    time = Column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.name} : {self.name}"


class User(Base, UserMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True)
    password = Column(String(255))

    def __repr__(self) -> str:

        return self.username
