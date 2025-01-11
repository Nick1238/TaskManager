import curses
import time


def error_screen(stdscr: curses.window, message: str):
    stdscr.clear()
    stdscr.addstr(3, 1, message)
    stdscr.border()
    stdscr.refresh()
    time.sleep(2)


def confirmation(stdscr: curses.window, action: str, task_name: str):
    stdscr.clear()
    stdscr.nodelay(False)
    stdscr.addstr(3, 1, f"Вы действительно хотите {action} задачу?")
    stdscr.addstr(4, 5, task_name, curses.color_pair(7) | curses.A_BOLD)
    stdscr.addstr(5, 1, "нажите Enter для подтверждения")
    stdscr.addstr(6, 1, "Любая другая кнопка - отмена")
    stdscr.border()
    stdscr.refresh()
    ch = stdscr.getch()
    stdscr.nodelay(True)
    return ch == ord("\n")


def get_task_name(stdscr: curses.window, message: str = "Введите имя задачи: "):
    curses.echo()
    curses.curs_set(1)
    stdscr.clear()
    stdscr.nodelay(False)
    stdscr.addstr(3, 1, message)
    stdscr.border(0)
    task_name = stdscr.getstr(4, 1, 40).decode("utf-8")
    curses.curs_set(0)
    stdscr.nodelay(True)
    curses.noecho()
    return task_name


def draw_table(stdscr: curses.window, tasks: list, active_field):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    max_rows = h - 2
    max_columns = w - 2
    if max_columns < 60 or max_rows < 1:
        stdscr.addstr(0, 0, "Недостаточный размер экрана", curses.A_BOLD)
        stdscr.refresh()
        return
    if tasks:
        if tasks[0].finished:
            header = "Завершенные задачи"
        else:
            header = "Текущие задачи"
        stdscr.addstr(
            1, 1, header.ljust(max_columns), curses.A_BOLD | curses.color_pair(3)
        )
        stdscr.addstr(2, 1, "Задача".ljust(41), curses.A_BOLD | curses.color_pair(2))
        stdscr.addstr(
            2, 42, "Время выполнения".ljust(18), curses.A_BOLD | curses.color_pair(2)
        )
        stdscr.addstr(
            2,
            60,
            "Активна".ljust(max_columns - 59),
            curses.A_BOLD | curses.color_pair(2),
        )
    else:
        stdscr.addstr(
            1,
            1,
            "Нет задач для отслеживания, добавьте задачи с помощью кнопки 'e'".ljust(
                max_columns
            ),
            curses.A_BOLD | curses.color_pair(3),
        )
    for i, task in enumerate(tasks):
        row = i + 3
        if row >= max_rows:
            break
        col_pair = i % 2 + (5, 1)[task.running] if i != active_field else 4
        stdscr.addstr(row, 1, task.name.ljust(41), curses.color_pair(col_pair))
        stdscr.addstr(
            row,
            42,
            format_elapsed_time(task.elapsed_time()).ljust(18),
            curses.color_pair(col_pair),
        )
        stdscr.addstr(
            row,
            60,
            ("Да" if task.running else "Нет").ljust(max_columns - 59),
            curses.color_pair(col_pair),
        )
    stdscr.border()
    print_help(stdscr)
    stdscr.refresh()


def format_elapsed_time(seconds):
    if seconds < 60:
        return f"{int(seconds)}сек"
    minutes, seconds = divmod(seconds, 60)
    if minutes < 60:
        return f"{int(minutes)}мин {int(seconds)}сек"
    hours, minutes = divmod(minutes, 60)
    if hours < 24:
        return f"{int(hours)}ч {int(minutes)}мин {int(seconds)}сек"
    days, hours = divmod(hours, 24)
    return f"{int(days)}д {int(hours)}ч {int(minutes)}мин"


def print_help(stdscr: curses.window):
    h, w = stdscr.getmaxyx()
    if h > 6:
        for i in range(1, w - 1):
            stdscr.addch(h - 4, i, "─")
        stdscr.addstr(
            h - 3,
            1,
            "'e'-добавить 's'-пауза/продолжить 'd'-удалить 'r'-переименовать"[: w - 2],
        )
        stdscr.addstr(h - 2, 1, "'x'-завершить 'f'-текущие/завершенные 'q'-выход ")
