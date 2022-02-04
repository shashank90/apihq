import enum
from sqlalchemy import Integer, Column, String, func, DateTime, ForeignKey, Enum
from db.database import Base


class AuditStatusEnum(enum.Enum):
    INITIATED = "initiated"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ERROR = "error"


class APIAudit(Base):
    __tablename__ = "api_audit"

    id = Column(Integer, primary_key=True)
    spec_id = Column(String(40), ForeignKey("api_spec.spec_id", ondelete="CASCADE"))
    user_id = Column(String, ForeignKey("user.user_id"))  # Who initiated the audit
    score = Column(Integer, nullable=False, default=10)
    status = Column(Enum(AuditStatusEnum), nullable=False)
    time_created = Column(DateTime, default=func.now(), nullable=False)
    time_updated = Column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False
    )

    def __init__(self, spec_id, user_id, score, status):
        self.spec_id = spec_id
        self.user_id = user_id
        self.score = score
        self.status = status
