import time
from Domain.interfaces.command import ICommand

class TimedCommandDecorator(ICommand):
    def __init__(self, decorated_command: ICommand):
        self._decorated = decorated_command

    def execute(self):
        start_time = time.perf_counter()
        result = self._decorated.execute()
        elapsed = time.perf_counter() - start_time
        print(f"Command executed in {elapsed:.4f} seconds")
        return result