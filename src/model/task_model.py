from datetime import datetime

from sqlalchemy import Boolean, Column, Float, String
from sqlalchemy.ext.declarative import declarative_base

from model.task import Task

Base = declarative_base()


class TaskModel(Base):
    __tablename__ = "tasks"
    name = Column(String, primary_key=True)
    start_time = Column(String)
    total_time = Column(Float, default=0.0)
    running = Column(Boolean, default=True)
    finished = Column(Boolean, default=False)

    @staticmethod
    def from_task(task: Task):
        return TaskModel(
            name=task.name,
            start_time=task.start_time.isoformat(),
            total_time=task.total_time,
            running=task.running,
            finished=task.finished,
        )

    def to_task(self) -> Task:
        return Task(
            name=self.name,
            start_time=datetime.fromisoformat(self.start_time),
            total_time=self.total_time,
            running=self.running,
            finished=self.finished,
        )
