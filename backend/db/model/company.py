from sqlalchemy import Integer, Column, String, func, DateTime

from backend.db.database import Base


class Company(Base):
    __tablename__ = "company"
    id = Column(Integer, primary_key=True)
    name = Column(String(40), nullable=False)
    time_created = Column(DateTime, default=func.now(), nullable=False)
    time_updated = Column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False
    )

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Company('{self.name}')"
