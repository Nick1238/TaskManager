import curses
import time
from enum import Enum

from model.database import Database
from model.task import Task
from view.console_view import (confirmation, draw_table, error_screen,
                               get_task_name, init_colors)


class Commands(Enum):
    ADD_TASK = "eE"
    SWITCH_TASKS = "fF"
    STOP_RESUME = "sS"
    DELETE_TASK = "dD"
    RENAME_TASK = "rR"
    FINISH_TASK = "xX"
    QUIT = "qQ"

    @classmethod
    def match_command(cls, key):
        """
        Сопоставляет нажатую клавишу с командой.

        :param key: Код нажатой клавиши.
        :return: Соответствующая команда или None, если команда не найдена.
        """
        if isinstance(key, int) and key >= 0:
            try:
                char = chr(key)
            except ValueError:
                return None
            for command in cls:
                if char in command.value:
                    return command
        return None


class TaskManager:
    def __init__(self, stdscr: curses.window, db_url="sqlite:///tasks.db"):
        """
        Инициализация менеджера задач. Создается подключение к базе данных и настраивается
        начальное состояние интерфейса.

        :param stdscr: Объект окна curses для рисования интерфейса.
        :param db_url: URL базы данных для подключения (по умолчанию используется SQLite).
        """
        self.__database = Database(db_url)
        self.__stdscr = stdscr
        self.__tasks = self.__database.fetch_all_tasks()
        self.__active_field = 0
        self.__show_finished = False
        self.__stdscr.nodelay(True)
        init_colors()

    def run(self):
        """
        Основной цикл программы, который обновляет интерфейс и обрабатывает команды.
        """
        commands_map = {
            Commands.ADD_TASK: self.add_task,
            Commands.SWITCH_TASKS: self.switch_tasks,
            Commands.STOP_RESUME: self.stop_resume_task,
            Commands.DELETE_TASK: self.delete_task,
            Commands.RENAME_TASK: self.update_task_name,
            Commands.FINISH_TASK: self.finish_task,
        }

        while True:
            draw_table(
                self.__stdscr, self.__tasks, self.__active_field, self.__show_finished
            )
            key = self.__stdscr.getch()
            command = Commands.match_command(key)

            if command == Commands.QUIT:
                break

            if command in commands_map:
                commands_map[command]()
            elif key == curses.KEY_UP:
                self.navigate_up()
            elif key == curses.KEY_DOWN:
                self.navigate_down()
            time.sleep(0.01)

    def finish_task(self):
        """
        Завершает текущую задачу, если она активна.

        Запрашивает подтверждение на завершение задачи, обновляет её статус в базе данных.
        """
        if not self.__tasks:
            return
        task = self.__tasks[self.__active_field]
        if confirmation(self.__stdscr, "завершить", task.name):
            task.finish()
            self.__database.update_task(task.name, task)
            self.__update_tasks_list()

    def switch_tasks(self):
        """
        Переключает отображение между активными и завершенными задачами.

        Этот метод меняет фильтр для отображаемых задач (показывает или скрывает завершенные).
        """
        self.__show_finished = not self.__show_finished
        self.__active_field = 0
        self.__update_tasks_list()

    def add_task(self):
        """
        Добавляем новую задачу.

        Ожидает ввода имени задачи, добавляет задачу в базу данных и обновляет список задач.
        """
        task_name = get_task_name(self.__stdscr)
        if task_name == "":
            error_screen(self.__stdscr, "Пустой ввод или ошибка кодировки")
            return
        new_task = Task(task_name)
        if self.__database.add_task(new_task):
            self.__update_tasks_list()
        else:
            error_screen(self.__stdscr, "Задача с данным именем уже существует")

    def stop_resume_task(self):
        """
        Останавливаем или возобновляем задачу.

        Этот метод либо останавливает текущую задачу, если она запущена, либо возобновляет её.
        """
        if not self.__tasks:
            return
        task = self.__tasks[self.__active_field]
        if task.finished:
            error_screen(self.__stdscr, "Задача уже завершена, начните новую")
        else:
            if task.running:
                task.stop()
            else:
                task.resume()
            self.__database.update_task(task.name, task)
            self.__update_tasks_list()

    def delete_task(self):
        """
        Удаляем текущую задачу.

        Этот метод запрашивает подтверждение на удаление и удаляет задачу из базы данных.
        """
        if not self.__tasks:
            return
        task = self.__tasks[self.__active_field]
        if confirmation(self.__stdscr, "удалить", task.name):
            if self.__database.delete_task(task.name):
                self.__update_tasks_list()
            else:
                error_screen(self.__stdscr, "Ошибка базы данных")

    def update_task_name(self):
        """
        Переименовываем задачу.

        Запрашивает новое имя задачи и обновляет её в базе данных.
        """
        if not self.__tasks:
            return
        task = self.__tasks[self.__active_field]
        if confirmation(self.__stdscr, "переименовать", task.name):
            new_name = get_task_name(self.__stdscr)
            if new_name == "":
                error_screen(self.__stdscr, "Пустой ввод или ошибка кодировки")
                return
            task_name = task.name
            task.name = new_name
            if self.__database.update_task(task_name, task):
                self.__update_tasks_list()
            else:
                task.name = task_name
                error_screen(self.__stdscr, "Задача с данным именем уже существует")

    def navigate_up(self):
        """
        Навигация вверх по списку задач.
        """
        self.__active_field -= 1
        if self.__active_field < 0:
            self.__active_field = len(self.__tasks) - 1

    def navigate_down(self):
        """
        Навигация вниз по списку задач.
        """
        self.__active_field += 1
        if self.__active_field >= len(self.__tasks):
            self.__active_field = 0

    def __update_tasks_list(self):
        """
        Обновление списка задач.

        Этот метод получает все задачи из базы данных и обновляет отображаемый список.
        Если активное поле выходит за пределы списка, оно корректируется.
        """
        self.__tasks = self.__database.fetch_all_tasks(self.__show_finished)
        if len(self.__tasks) <= self.__active_field:
            self.__active_field = max(len(self.__tasks) - 1, 0)
