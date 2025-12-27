from sqlalchemy import Column, Integer, String, Boolean
from .db import Base

class Channel(Base):
    __tablename__ = "channels"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)

class File(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True)
    file_id = Column(String)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    tg_id = Column(Integer, unique=True)
    received = Column(Boolean, default=False)
