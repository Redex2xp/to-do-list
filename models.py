from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    is_done = Column(Boolean, default=False)

    def __repr__(self):
        return f"<Task(title='{self.title}', done={self.is_done})>"
