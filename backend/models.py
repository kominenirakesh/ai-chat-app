from sqlalchemy import Column, Integer, String, Text, ForeignKey
from database import Base


class Thread(Base):
    __tablename__ = "threads"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    thread_id = Column(Integer, ForeignKey("threads.id"))
    role = Column(String)
    content = Column(Text)


class Memory(Base):
    __tablename__ = "memory"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)