from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from model.task_model import Base, TaskModel
from model.task import Task

class Database:
    def __init__(self, db_url="sqlite:///tasks.db"):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def add_task(self, task: Task):
        with self.Session() as session:
            task_model = TaskModel.from_task(task)
            session.add(task_model)
            try:
                session.commit()
            except IntegrityError:
                pass

    def update_task(self, task_name: str, task: Task) -> bool:
        with self.Session() as session:
            if task_model := session.query(TaskModel).filter_by(name=task_name).first():
                updates = {
                    "name": task.name,
                    "start_time": task.start_time,
                    "total_time": task.total_time,
                    "running": task.running,
                    "finished": task.finished
                }
                for key, value in updates.items():
                    setattr(task_model, key, value)
                try:
                    session.commit()
                    return True
                except IntegrityError:
                    pass
            return False

    def delete_task(self, task_name):
        with self.Session() as session:
            task_model = session.query(TaskModel).filter_by(name=task_name).first()
            if task_model:
                session.delete(task_model)
                session.commit()
                return True
            else:
                return False

    def fetch_all_tasks(self, finished=False):
        with self.Session() as session:
            task_models = session.query(TaskModel).order_by(TaskModel.running.desc()).filter_by(finished=finished)
            return [task_model.to_task() for task_model in task_models]
    
    

    def get_task_by_name(self, task_name):
        with self.Session() as session:
            task_model = session.query(TaskModel).filter_by(name=task_name).first()
            if task_model:
                return task_model.to_task()
            return None
