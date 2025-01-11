import curses
import time

from model.database import Database
from model.task import Task
from view.console_view import draw_table, error_screen, get_task_name


class TaskManager:
    def __init__(self, stdscr: curses.window, db_url="sqlite:///tasks.db"):
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, 236)
        curses.init_pair(2, curses.COLOR_WHITE, 233)
        curses.init_pair(3, curses.COLOR_WHITE, 245)
        curses.init_pair(4, 233, curses.COLOR_WHITE)
        
        self.database = Database(db_url)
        self.stdscr = stdscr
        self.tasks = self.database.fetch_all_tasks()
        self.show_finished = False
        self.active_field = 0
        

    def run(self):
        self.stdscr.nodelay(True)
        curses.curs_set(0)
        while True:
            draw_table(self.stdscr, self.tasks, self.active_field)
            a = self.stdscr.getch()
            if a == ord("e"):
                self.add_task()
            elif a == ord("s"):
                self.stop_resume_task()
            elif a == ord("d"):
                self.delete_task()
            elif a == ord("r"):
                self.update_task_name()
            elif a == ord("x"):
                self.finish_task()
            elif a == ord("f"):
                self.switch_tasks()
            elif a == curses.KEY_UP:
                self.active_field -= 1
                if self.active_field < 0:
                    self.active_field = len(self.tasks) - 1
            elif a == curses.KEY_DOWN:
                self.active_field += 1
                if self.active_field >= len(self.tasks):
                    self.active_field = 0
            elif a == ord("q"):
                break
            time.sleep(0.01)

    def finish_task(self):
        task_name = get_task_name(self.stdscr)
        if task := self.database.get_task_by_name(task_name):
            task.finish()
            self.database.update_task(task_name, task)
            self.__update_tasks_list()
        else:
            error_screen(self.stdscr, "Задача с данным именем не обнаружена")

    def switch_tasks(self):
        self.show_finished = not self.show_finished
        self.__update_tasks_list()

    def add_task(self):
        task_name = get_task_name(self.stdscr)
        new_task = Task(task_name)
        if self.database.add_task(new_task):
            self.__update_tasks_list()
        else:
            error_screen(self.stdscr, "Задача с данным именем уже существует")

    def stop_resume_task(self):
        task_name = get_task_name(self.stdscr)
        if task := self.database.get_task_by_name(task_name):
            if task.finished:
                error_screen(self.stdscr, "Задача уже завершена, начните новую")
            else:
                if task.running:
                    task.stop()
                else:
                    task.resume()
                self.database.update_task(task_name, task)
                self.__update_tasks_list()
        else:
            error_screen(self.stdscr, "Задача с данным именем не обнаружена")

    def delete_task(self):
        task_name = get_task_name(self.stdscr)
        if self.database.delete_task(task_name):
            self.__update_tasks_list()
        else:
            error_screen(self.stdscr, "Задача с данным именем не обнаружена")

    def update_task_name(self):
        task_name = get_task_name(self.stdscr)

        if task := self.database.get_task_by_name(task_name):
            new_name = get_task_name(self.stdscr)
            task.name = new_name
            if self.database.update_task(task_name, task):
                self.__update_tasks_list()
            else:
                error_screen(self.stdscr, "Задача с данным именем уже существует")
        else:
            error_screen(self.stdscr, "Задача с данным именем не обнаружена")

    def __update_tasks_list(self):
        self.tasks = self.database.fetch_all_tasks(self.show_finished)
