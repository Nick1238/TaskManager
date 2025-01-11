from datetime import datetime
from model.task import Task
from model.database import Database
import curses
import time

def error_screen(stdscr: curses.window, message: str):
    stdscr.clear()
    stdscr.addstr(3, 1, message)
    stdscr.border()
    stdscr.refresh()
    time.sleep(2)
    

def user_input(stdscr: curses.window):
    pass


def get_task_name(stdscr: curses.window):
    curses.echo() 
    stdscr.clear()
    stdscr.nodelay(False)

    stdscr.addstr(3, 1, "Введите имя задачи: ")
    stdscr.border()
    stdscr.refresh()
    task_name = stdscr.getstr(4, 1, 40).decode('utf-8')  # Считываем строку, максимум 40 символов


    curses.noecho()
    stdscr.nodelay(True)
    return task_name


def draw_table(stdscr: curses.window, tasks: list[Task]):
    stdscr.clear()
    h, w = stdscr.getmaxyx()  # Получаем размеры окна
    max_rows = h - 2  # Оставляем место для заголовков
    max_columns = w - 2  # Оставляем место для рамки
    if w < 40:
        stdscr.addstr(0, 0, "Недостаточный размер экрана", curses.A_BOLD)
        stdscr.refresh()
        return

    stdscr.addstr(1, 1, "Задача", curses.A_BOLD)
    stdscr.addstr(1, 20, "Время выполнения", curses.A_BOLD)
    stdscr.addstr(1, 40, "Активна ли", curses.A_BOLD)
    # stdscr.addstr(0, 55, "Важность", curses.A_BOLD)
    
    stdscr.border()
    
    # Выводим данные задач в таблице
    for i, task in enumerate(tasks):
        row = i + 2  # Строки начинаются с 2, чтобы не перезаписать заголовки

        if row >= max_rows:
            break  # Прекращаем вывод, если вышли за пределы экрана

        stdscr.addstr(row, 1, task.name[:15].ljust(15))  # Название задачи (до 15 символов)
        stdscr.addstr(row, 20, f"{task.elapsed_time():.0f} сек".ljust(15))  # Время выполнения
        stdscr.addstr(row, 40, "Да" if task.running else "Нет", curses.A_BOLD)  # Статус
    
    stdscr.refresh()