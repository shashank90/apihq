import enum
from sqlalchemy import Integer, Column, String, func, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from backend.db.database import Base


class UserApiRunLimit(Base):
    __tablename__ = "user_api_run_limit"

    id = Column(Integer, primary_key=True)
    user_id = Column(String, ForeignKey("user.user_id"))  # Who initiated validate
    limit = Column(Integer, nullable=False)
    # This is login timestamp
    time_created = Column(DateTime, default=func.now(), nullable=False)
    time_updated = Column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False
    )
    user = relationship("User", backref="api_run_limit", uselist=False)

    def __init__(self, user_id, limit):
        self.user_id = user_id
        self.limit = limit
