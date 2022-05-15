from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime


Base = declarative_base()


class Websites(Base):
    __tablename__ = "websites"
    id = Column(Integer, primary_key=True)
    domain = Column(String(255))
    created = Column(DateTime, default=datetime.utcnow)


class Data(Base):
    __tablename__ = "data"
    id = Column(Integer, primary_key=True)

    # other columns
    

class PageVisits(Base):
    id = Column(Integer, primary_key=True)
    page = Column(String(255))
    referer = Column(String(255))
    loadtime = Column(Integer)
    browser = Column(String(355))
    device_type = Column(String(255))
    device_os = Column(String(255))
    country = Column(String(255))
    state = Column(String(255))
    city = Column(String(255))


