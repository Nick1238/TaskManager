from curses import window, wrapper

from controller.task_manager import TaskManager


def main(stdscr: window):
    manager = TaskManager(stdscr)
    manager.run()


if __name__ == "__main__":
    wrapper(main)
