from view.console_view import *
from curses import wrapper, window
from model.database import Database
import time
from controller.task_manager import TaskManager

def main(stdscr: window):
    stdscr.nodelay(True)
    manager = TaskManager(stdscr)
    manager.run()


if __name__ == "__main__":
    wrapper(main)