from datetime import datetime

import pytest

from model.database import Database
from model.task import Task


@pytest.fixture
def db():
    """Фикстура для создания нового сеанса базы данных для каждого теста."""
    database = Database(db_url="sqlite:///:memory:")
    yield database


@pytest.fixture
def sample_task():
    """Фикстура для создания тестовой задачи."""
    return Task(
        name="Test Task",
        start_time=datetime.now(),
        total_time=0.0,
        running=False,
        finished=False
    )


def test_add_task(db, sample_task):
    """Тест добавления задачи в базу данных."""
    result = db.add_task(sample_task)
    assert result is True

    task_from_db = db.get_task_by_name(sample_task.name)
    assert task_from_db is not None
    assert task_from_db.name == sample_task.name


def test_add_duplicate_task(db, sample_task):
    """Тест добавления задачи с дублирующимся именем (ошибка целостности)."""
    db.add_task(sample_task)
    result = db.add_task(sample_task)
    assert result is False

def test_update_non_existent_task(db):
    """Тест обновления задачи, которая не существует."""
    non_existent_task = Task(
        name="Non Existent Task",
        start_time=datetime.now(),
        total_time=0.0,
        running=False,
        finished=False
    )
    result = db.update_task("Non Existent Task", non_existent_task)
    assert result is False


def test_delete_task(db, sample_task):
    """Тест удаления существующей задачи."""
    db.add_task(sample_task)
    result = db.delete_task(sample_task.name)
    assert result is True

    task_from_db = db.get_task_by_name(sample_task.name)
    assert task_from_db is None


def test_delete_non_existent_task(db):
    """Тест удаления задачи, которая не существует."""
    result = db.delete_task("Non Existent Task")
    assert result is False


def test_fetch_all_tasks(db, sample_task):
    """Тест получения всех задач."""
    db.add_task(sample_task)

    tasks = db.fetch_all_tasks()
    assert len(tasks) == 1
    assert tasks[0].name == sample_task.name

def test_get_task_by_name(db, sample_task):
    """Тест получения задачи по имени."""
    db.add_task(sample_task)
    
    task_from_db = db.get_task_by_name(sample_task.name)
    assert task_from_db is not None
    assert task_from_db.name == sample_task.name


def test_get_task_by_non_existent_name(db):
    """Тест получения задачи по несуществующему имени."""
    task_from_db = db.get_task_by_name("Non Existent Task")
    assert task_from_db is None
