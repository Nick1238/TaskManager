from model.database import Database
from view.console_view import *
from curses import window

class TaskManager:

    def __init__(self, stdscr: window, db_url="sqlite:///tasks.db"):
        self.database = Database(db_url)
        self.stdscr = stdscr
        self.tasks = self.database.fetch_all_tasks()

    def run(self):
        while True:
            draw_table(self.stdscr, self.tasks)
            a = self.stdscr.getch()
            if a == ord('q'):
                self.add_task()
            elif a == ord('s'):
                self.stop_resume_task()
            elif a == ord('d'):
                self.delete_task()
            elif a == ord('r'):
                self.update_task_name()
            time.sleep(1)
            
    
    def add_task(self):
        task_name = get_task_name(self.stdscr)
        if not self.database.get_task_by_name(task_name):
            new_task = Task(task_name)
            self.database.add_task(new_task)
            self.tasks = self.database.fetch_all_tasks()
        else:
            error_screen(self.stdscr, "Задача с данным именем уже существует")


    def stop_resume_task(self):
        task_name = get_task_name(self.stdscr)
        if task := self.database.get_task_by_name(task_name):
            if task.running:
                task.stop()
            else:
                task.resume()
            self.database.update_task(task_name, task)
            self.tasks = self.database.fetch_all_tasks()
        else:
            error_screen(self.stdscr, "Задача с данным именем не обнаружена")

    def delete_task(self):
        task_name = get_task_name(self.stdscr)
        if self.database.delete_task(task_name):
            self.tasks = self.database.fetch_all_tasks()
        else:
            error_screen(self.stdscr, "Задача с данным именем не обнаружена")

    def update_task_name(self):
        task_name = get_task_name(self.stdscr)

        if task := self.database.get_task_by_name(task_name):
            new_name = get_task_name(self.stdscr)
            task.name = new_name
            if self.database.update_task(task_name, task):
                self.tasks = self.database.fetch_all_tasks()
            else:
                error_screen(self.stdscr, "Задача с данным именем уже существует")
        else:
            error_screen(self.stdscr, "Задача с данным именем не обнаружена")
        
    
    
    