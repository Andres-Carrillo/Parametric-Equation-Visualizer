import time

class Timer:
    def __init__(self):
        self.start_time = time.perf_counter()
        self.last_time = self.start_time
        self.delta = 0.0
 

    def elapsed_time(self):
        current_time = time.perf_counter()
        elapsed = current_time - self.start_time

        return elapsed   

    def delta_time(self):
        current_time = time.perf_counter()
        self.delta = current_time - self.last_time
        self.last_time = current_time

        return self.delta
    
    def reset(self):
        self.start_time = time.perf_counter()

    @staticmethod
    def sleep(seconds: float):
        time.sleep(seconds)