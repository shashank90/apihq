import enum
from sqlalchemy import Integer, Column, String, func, DateTime, ForeignKey, Enum
from db.database import Base


class ValidateStatusEnum(enum.Enum):
    LINT_ERROR = "lint_error"
    FIX_VALIDATION_ERROR = "fix_validation_error"
    RUN_API = "run_api"


VSEnum = Enum(ValidateStatusEnum, inherit_schema=True)


class ApiValidate(Base):
    __tablename__ = "api_validate"

    id = Column(Integer, primary_key=True)
    spec_id = Column(String(40), ForeignKey("api_spec.spec_id", ondelete="CASCADE"))
    user_id = Column(String, ForeignKey("user.user_id"))  # Who initiated validate
    score = Column(Integer, nullable=True)
    status = Column(VSEnum, nullable=False)
    message = Column(String(160), nullable=True)
    time_created = Column(DateTime, default=func.now(), nullable=False)
    time_updated = Column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False
    )

    def __init__(self, spec_id, user_id, status):
        self.spec_id = spec_id
        self.user_id = user_id
        self.status = status
