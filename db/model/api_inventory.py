from email.policy import default
from sqlalchemy import (
    Integer,
    Column,
    String,
    func,
    DateTime,
    ForeignKey,
    Enum,
    Boolean,
)
from sqlalchemy.orm import relationship
from db.database import Base
import enum


class AddedByEnum(enum.Enum):
    CRAWLER = "crawler"
    USER = "user"


class APIInventory(Base):
    __tablename__ = "api_inventory"

    id = Column(Integer, primary_key=True)
    # In case of crawled APIs, spec may not be present
    spec_id = Column(String(40), ForeignKey("api_spec.spec_id"), nullable=True)
    # TODO: Is the user the owner ? Need this notion when deleting API. Think RBAC
    user_id = Column(
        String, ForeignKey("user.user_id")
    )  # User who discovered the api(crawler or actual user)
    added_by = Column(Enum(AddedByEnum), nullable=False)
    api_path = Column(String(120), nullable=False)
    http_method = Column(String(20), nullable=False)
    found_in_file = Column(String(40), nullable=True)
    # Add additional remarks to be displayed
    message = Column(String(60), nullable=True)
    time_created = Column(DateTime, default=func.now(), nullable=False)
    time_updated = Column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False
    )
    user = relationship("User", backref="apis")
    spec = relationship("APISpec", backref="apis")

    def __init__(
        self,
        spec_id,
        user_id,
        added_by,
        api_path,
        http_method,
        found_in_file,
        message=None,
    ):
        self.spec_id = spec_id
        self.user_id = user_id
        self.added_by = added_by
        self.api_path = api_path
        self.http_method = http_method
        self.found_in_file = found_in_file
        if message:
            self.message = message
