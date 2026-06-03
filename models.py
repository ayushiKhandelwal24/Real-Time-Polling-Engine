from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Poll(Base):
    __tablename__ = "polls"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)  # Length fixed here

    choices = relationship("Choice", back_populates="poll", cascade="all, delete-orphan", lazy="selectin")

class Choice(Base):
    __tablename__ = "choices"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(255), nullable=False)   # Length fixed here
    votes = Column(Integer, default=0)
    poll_id = Column(Integer, ForeignKey("polls.id", ondelete="CASCADE"))

    poll = relationship("Poll", back_populates="choices")