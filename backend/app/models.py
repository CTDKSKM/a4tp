from sqlalchemy import Column, Integer, String, Float

from .database import Base


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    img = Column(String)
    category = Column(String, index=True)
    title = Column(String, index=True)
    published_at = Column(String, nullable=True)
    running_time = Column(String, nullable=True)
    rating = Column(Integer, nullable=True)
    comment = Column(String)
