import enum
from sqlalchemy import Integer, Column, String, func, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from backend.db.database import Base


class RunStatusEnum(enum.Enum):
    INITIATED = "initiated"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ERROR = "error"


RSEnum = Enum(RunStatusEnum, inherit_schema=True)


class ApiRun(Base):
    __tablename__ = "api_run"

    id = Column(Integer, primary_key=True)
    run_id = Column(String(40))
    api_id = Column(String(40), ForeignKey("api_inventory.api_id", ondelete="CASCADE"))
    http_method = Column(String(20), nullable=True)
    user_id = Column(String, ForeignKey("user.user_id"))  # Who initiated the run
    score = Column(Integer, nullable=True)
    status = Column(RSEnum, nullable=False)
    message = Column(String(160), nullable=True)
    time_created = Column(DateTime, default=func.now(), nullable=False)
    time_updated = Column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False
    )
    # Many to one relationship from run to api
    api = relationship("ApiInventory", backref="runs")

    def __init__(self, run_id, api_id, user_id, status, http_method=None):
        self.api_id = api_id
        self.user_id = user_id
        self.run_id = run_id
        self.status = status
        self.http_method = http_method
