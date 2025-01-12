import curses
import time


def init_colors():
    """
    Инициализация цветов для выделения различных элементов интерфейса.
    """
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, 236)
    curses.init_pair(2, curses.COLOR_WHITE, 233)
    curses.init_pair(3, 26, curses.COLOR_WHITE)
    curses.init_pair(4, 233, curses.COLOR_WHITE)
    curses.init_pair(5, 248, 236)
    curses.init_pair(6, 248, 233)
    curses.init_pair(7, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.curs_set(0)


def error_screen(stdscr: curses.window, message: str):
    """
    Отображает экран с ошибкой и задерживает на 2 секунды перед возвратом.

    :param stdscr: Объект окна curses
    :param message: Сообщение об ошибке для отображения
    """
    stdscr.clear()
    stdscr.addstr(3, 1, message)
    stdscr.border()
    stdscr.refresh()
    time.sleep(2)


def confirmation(stdscr: curses.window, action: str, task_name: str) -> bool:
    """
    Отображает окно подтверждения для выполнения действия с задачей.

    :param stdscr: Объект окна curses
    :param action: Действие, которое нужно подтвердить (например, "удалить")
    :param task_name: Имя задачи, с которой нужно выполнить действие
    :return: True, если пользователь подтвердил действие, False в противном случае
    """
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
    """
    Получение имени задачи от пользователя через ввод с клавиатуры.

    :param stdscr: Объект окна curses
    :param message: Сообщение, которое будет выведено пользователю
    :return: Введенное имя задачи
    """
    curses.echo()
    curses.curs_set(1)
    stdscr.clear()
    stdscr.nodelay(False)
    stdscr.addstr(3, 1, message)
    stdscr.border(0)
    try:
        task_name = stdscr.getstr(4, 1, 40).decode("utf-8")
    except UnicodeDecodeError:
        task_name = ""
    curses.curs_set(0)
    stdscr.nodelay(True)
    curses.noecho()
    return task_name


def draw_table(stdscr: curses.window, tasks: list, active_field, finished):
    """
    Отображает таблицу с задачами на экране.

    :param stdscr: Объект окна curses
    :param tasks: Список задач для отображения
    :param active_field: Индекс активной задачи
    :param finished: Флаг, указывающий, показывать ли завершенные задачи
    """
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    max_rows = h - 2
    max_columns = w - 2
    if max_columns < 60 or max_rows < 3:
        stdscr.addstr(0, 0, "Недостаточный размер окна", curses.A_BOLD)
        stdscr.refresh()
        return
    draw_header(stdscr, max_columns, finished)
    for i, task in enumerate(tasks):
        row = i + 3
        if row > max_rows:
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


def draw_header(stdscr: curses.window, max_columns: int, finished: bool):
    """
    Рисует заголовок таблицы.

    :param stdscr: Объект окна curses
    :param max_columns: Максимальное количество колонок в окне
    :param finished: Флаг, указывающий, показывать ли завершенные задачи
    """
    if finished:
        header = "Завершенные задачи"
    else:
        header = "Текущие задачи"
    stdscr.addstr(1, 1, header.ljust(max_columns), curses.A_BOLD | curses.color_pair(3))
    stdscr.addstr(2, 1, "Задача".ljust(41), curses.A_BOLD | curses.color_pair(2))
    stdscr.addstr(
        2, 42, "Время выполнения".ljust(18), curses.A_BOLD | curses.color_pair(2)
    )
    stdscr.addstr(
        2, 60, "Активна".ljust(max_columns - 59), curses.A_BOLD | curses.color_pair(2)
    )


def format_elapsed_time(seconds):
    """
    Форматирует время в читаемый вид (секунды, минуты, часы, дни).

    :param seconds: Время в секундах
    :return: Строка с отформатированным временем
    """
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
    """
    Рисует подсказки по управлению внизу экрана.

    :param stdscr: Объект окна curses
    """
    h, w = stdscr.getmaxyx()
    if h > 8:
        for i in range(1, w - 1):
            stdscr.addch(h - 4, i, "─")
        stdscr.addstr(
            h - 3,
            1,
            "'e'-добавить 's'-пауза/продолжить 'd'-удалить 'r'-переименовать"[
                : w - 2
            ].ljust(w - 2),
        )
        stdscr.addstr(
            h - 2,
            1,
            "'↑↓'-выбор 'x'-завершить 'f'-текущие/завершенные 'q'-выход ".ljust(w - 2),
        )
