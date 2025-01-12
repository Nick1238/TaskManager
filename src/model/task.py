from datetime import datetime


class Task:
    def __init__(
        self, name, start_time=None, total_time=0.0, running=True, finished=False
    ):
        self.name = name
        self.__start_time = start_time or datetime.now()
        self.__total_time = total_time
        self.__running = running
        self.__finished = finished

    @property
    def start_time(self):
        return self.__start_time

    @property
    def total_time(self):
        return self.__total_time

    @property
    def running(self):
        return self.__running

    @property
    def finished(self):
        return self.__finished

    def stop(self):
        if self.__running:
            elapsed = (datetime.now() - self.__start_time).total_seconds()
            self.__total_time += elapsed
            self.__running = False

    def finish(self):
        self.__finished = True
        self.stop()

    def resume(self):
        if not self.__running:
            self.__start_time = datetime.now()
            self.__running = True

    def elapsed_time(self):
        if self.__running:
            elapsed = (datetime.now() - self.__start_time).total_seconds()
        else:
            elapsed = 0.0
        return self.__total_time + elapsed

    def __str__(self):
        status = "Running" if self.__running else "Stopped"
        elapsed = self.elapsed_time()
        return (
            f"Task: {self.name}, Status: {status}, Time Elapsed: {elapsed:.2f} seconds"
        )
