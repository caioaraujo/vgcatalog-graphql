from sqlalchemy import Column, Integer, String, Boolean, UniqueConstraint

from app.db.database import Base


class Game(Base):
    __tablename__ = "games"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    released_year = Column(Integer)
    platform = Column(String)
    genre = Column(String)
    allow_multiplayer = Column(Boolean, default=False)

    __table_args__ = (UniqueConstraint("name", "platform", name="uk_name_platform"),)
