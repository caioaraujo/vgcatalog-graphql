import datetime

from sqlalchemy import Column, Integer, String, JSON, DateTime, Boolean

from app.infra.db.database import Base


class OutboxEvent(Base):
    __tablename__ = "outbox_event"

    id = Column(Integer, primary_key=True)
    event_type = Column(String, nullable=False)
    payload = Column(JSON, nullable=False)

    created_at = Column(DateTime, default=datetime.datetime.now(datetime.UTC))
    processed = Column(Boolean, default=False)
