from datetime import datetime


class Task:
    def __init__(
        self, name, start_time=None, total_time=0.0, running=True, finished=False
    ):
        self.name = name
        self.start_time = start_time or datetime.now()
        self.total_time = total_time
        self.running = running
        self.finished = finished

    def stop(self):
        if self.running:
            elapsed = (datetime.now() - self.start_time).total_seconds()
            self.total_time += elapsed
            self.running = False

    def finish(self):
        self.finished = True
        self.stop()

    def resume(self):
        if not self.running:
            self.start_time = datetime.now()
            self.running = True

    def elapsed_time(self):
        if self.running:
            elapsed = (datetime.now() - self.start_time).total_seconds()
        else:
            elapsed = 0.0
        return self.total_time + elapsed

    def __str__(self):
        status = "Running" if self.running else "Stopped"
        elapsed = self.elapsed_time()
        return (
            f"Task: {self.name}, Status: {status}, Time Elapsed: {elapsed:.2f} seconds"
        )
