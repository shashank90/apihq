from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from backend.db.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    user_id = Column(String(50), unique=True, nullable=False)
    name = Column(String(50), nullable=False)
    email = Column(String(60), unique=True, nullable=False)
    password = Column(String(120), nullable=False)
    company_name = Column(String(60), nullable=True)
    time_created = Column(DateTime, default=func.now(), nullable=False)
    time_updated = Column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False
    )

    def __init__(self, user_id, name, email, password, company_name=None):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password
        self.company_name = company_name

    def __repr__(self):
        return f"{self.email}"
