from sqlalchemy import Integer, Column, String, func, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.db.database import Base


class ApiSpec(Base):
    __tablename__ = "api_spec"

    id = Column(Integer, primary_key=True)
    spec_id = Column(String(40), nullable=False, unique=True)
    user_id = Column(
        String, ForeignKey("user.user_id", ondelete="CASCADE")
    )  # Who added the spec(crawler or actual user)
    collection_name = Column(String(40), nullable=False)
    file_name = Column(String(40), nullable=False)
    data_dir = Column(String(120), nullable=False)
    time_created = Column(DateTime, default=func.now(), nullable=False)
    time_updated = Column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False
    )
    # Strict one to one relationship from spec to validate
    validate_result = relationship("ApiValidate", backref="spec", uselist=False)
    user = relationship("User", backref="specs")

    def __init__(self, spec_id, user_id, collection_name, file_name, data_dir):
        self.spec_id = spec_id
        self.user_id = user_id
        self.collection_name = collection_name
        self.file_name = file_name
        self.data_dir = data_dir
