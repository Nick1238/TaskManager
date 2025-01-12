from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from model.task import Task
from model.task_model import Base, TaskModel


class Database:
    def __init__(self, db_url="sqlite:///tasks.db"):
        """
        Инициализация базы данных. Создается соединение с указанным URL базы данных,
        если база данных не существует, она будет создана.
        
        :param db_url: URL базы данных (по умолчанию используется SQLite база данных)
        """
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def add_task(self, task: Task):
        """
        Добавляет задачу в базу данных.

        :param task: Объект задачи, который нужно добавить в базу данных.
        :return: True, если задача успешно добавлена, иначе False.
        """
        with self.Session() as session:
            task_model = TaskModel.from_task(task)
            session.add(task_model)
            try:
                session.commit()
                return True
            except IntegrityError:
                pass
        return False

    def update_task(self, task_name: str, task: Task) -> bool:
        """
        Обновляет данные задачи по имени.

        :param task_name: Название задачи, которую нужно обновить.
        :param task: Новый объект задачи, содержащий обновленные данные.
        :return: True, если задача успешно обновлена, иначе False.
        """
        with self.Session() as session:
            if task_model := session.query(TaskModel).filter_by(name=task_name).first():
                updates = {
                    "name": task.name,
                    "start_time": task.start_time,
                    "total_time": task.total_time,
                    "running": task.running,
                    "finished": task.finished,
                }
                for key, value in updates.items():
                    setattr(task_model, key, value)
                try:
                    session.commit()
                    return True
                except IntegrityError:
                    pass
        return False

    def delete_task(self, task_name: str) -> bool:
        """
        Удаляет задачу из базы данных по её имени.

        :param task_name: Название задачи, которую нужно удалить.
        :return: True, если задача успешно удалена, иначе False.
        """
        with self.Session() as session:
            task_model = session.query(TaskModel).filter_by(name=task_name).first()
            if task_model:
                session.delete(task_model)
                session.commit()
                return True
            else:
                return False

    def fetch_all_tasks(self, finished=False) -> list[Task]:
        """
        Получает все задачи из базы данных, с фильтром по завершенности.

        :param finished: Флаг, определяющий, нужно ли получать только завершенные задачи (по умолчанию False).
        :return: Список объектов Task, которые соответствуют фильтру.
        """
        with self.Session() as session:
            task_models = (
                session.query(TaskModel)
                .order_by(TaskModel.running.desc())
                .filter_by(finished=finished)
            )
            return [task_model.to_task() for task_model in task_models]

    def get_task_by_name(self, task_name: str) -> Task | None:
        """
        Получает задачу по её имени.

        :param task_name: Название задачи.
        :return: Объект Task, если задача найдена, иначе None.
        """
        with self.Session() as session:
            task_model = session.query(TaskModel).filter_by(name=task_name).first()
            if task_model:
                return task_model.to_task()
            return None
