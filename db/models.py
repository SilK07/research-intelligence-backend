from sqlalchemy import Column, Integer, String, PrimaryKeyConstraint
from db.base import Base

class documents(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)