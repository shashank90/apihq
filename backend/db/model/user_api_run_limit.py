import enum
from sqlalchemy import Integer, Column, String, func, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.db.database import Base
from backend.utils.constants import DEFAULT_API_RUN_LIMIT


class UserApiRunLimit(Base):
    __tablename__ = "user_api_run_limit"

    id = Column(Integer, primary_key=True)
    user_id = Column(String, ForeignKey("user.user_id"))
    api_run_count = Column(Integer, default=0)
    limit = Column(Integer, default=DEFAULT_API_RUN_LIMIT)
    # This is login timestamp
    time_created = Column(DateTime, default=func.now(), nullable=False)
    time_updated = Column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False
    )
    user = relationship("User", backref="api_run_limit", uselist=False)

    def __init__(self, user_id, limit):
        self.user_id = user_id
        self.limit = limit
