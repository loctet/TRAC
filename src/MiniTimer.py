import time

class MiniTimer :
    def __init__(self) -> None:
        self._time_ = 0
    
    def start_time(self):
        self._time_ = time.time_ns()

    def get_ellapsed_time(self) :
        return time.time_ns() - self._time_
    
    def get_time(self):
        return time.time_ns()
  