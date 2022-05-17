from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy import Column, Integer, String, DateTime, create_engine
from datetime import datetime


Base = declarative_base()

DATABASE_PATH = "sqlite:///data_db.sqlite3"
ENGINE = create_engine(DATABASE_PATH, future=True)
db_session = sessionmaker(bind=ENGINE)


class Websites(Base):
    __tablename__ = "websites"
    id = Column(Integer, primary_key=True)
    domain = Column(String(255), unique=True)
    created = Column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return self.domain

class PageVisits(Base):
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

class Login(Base):
    __tablename__ = "login_info"

    id = Column(Integer, primary_key=True)
    username = Column(String(255),unique=True)
    password = Column(String(255))

    def __repr__(self) -> str:
        return self.username
