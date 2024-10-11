from sqlalchemy import Column, UUID, String, Integer, DateTime
from sqlalchemy.sql import func

from database import Base


class BlacklistEmail(Base):
    __tablename__ = "blacklist_emails"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True, index=True)
    app_uuid = Column(UUID)
    blocked_reason = Column(String(255))
    ip = Column(String(40))

    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    updateAt = Column(DateTime(timezone=True), onupdate=func.now())
