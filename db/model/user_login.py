from sqlalchemy import Integer, Column, String, func, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from db.database import Base


class Login(Base):
    __tablename__ = "login"

    id = Column(Integer, primary_key=True)
    user_id = Column(String, ForeignKey("user.user_id"))  # Who initiated validate
    ip_address = Column(String(40), nullable=True)
    # This is login timestamp
    time_created = Column(DateTime, default=func.now(), nullable=False)
    time_updated = Column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False
    )

    user = relationship("User", backref="logins")

    def __init__(self, user_id, ip_addr):
        self.user_id = user_id
        self.ip_address = ip_addr
