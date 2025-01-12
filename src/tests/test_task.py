from datetime import datetime

import pytest

from model.task import Task


@pytest.fixture
def test_task():
    """Фикстура для создания задачи Test Task."""
    return Task(
        name="Test Task",
        start_time=datetime.now(),
        total_time=0.0,
        running=True,
        finished=False
    )

def test_task_initialization(test_task):
    """Тестирование инициализации задачи"""
    task = test_task
    assert task.name == "Test Task"
    assert isinstance(task.start_time, datetime)
    assert task.total_time == 0.0
    assert task.running is True
    assert task.finished is False

def test_task_stop(test_task):
    """Тестирование остановки задачи"""
    task = test_task
    task.stop()
    assert task.running is False
    assert task.total_time > 0  # Время должно быть добавлено

def test_task_resume(test_task):
    """Тестирование возобновления задачи"""
    task = test_task
    task.stop()
    prev_total_time = task.total_time
    task.resume()
    assert task.running is True
    assert task.total_time == prev_total_time

def test_task_finish(test_task):
    """Тестирование завершения задачи"""
    task = test_task
    task.finish()
    assert task.finished is True
    assert task.running is False
    assert task.total_time > 0

def test_elapsed_time_running(test_task):
    """Тестирование расчета времени выполнения для запущенной задачи"""
    task = test_task
    initial_time = task.elapsed_time()
    assert initial_time > 0

def test_elapsed_time_stopped(test_task):
    """Тестирование расчета времени выполнения для остановленной задачи"""
    task = test_task
    task.stop()
    elapsed_time = task.elapsed_time()
    assert elapsed_time == task.total_time

def test_task_resume_after_stop(test_task):
    """Тестирование возобновления задачи после остановки"""
    task = test_task
    task.stop()
    total_time_before_resume = task.total_time
    task.resume()
    assert task.running is True
    assert task.total_time == total_time_before_resume

def test_task_elapsed_time_increase(test_task):
    """Тестирование увеличения времени выполнения задачи"""
    task = test_task
    initial_time = task.elapsed_time()
    task.stop()
    final_time = task.elapsed_time()
    assert final_time >= initial_time