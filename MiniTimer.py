import time

class MiniTimer:
    """
    A simple timer class for measuring elapsed time in nanoseconds.
    
    This class provides methods to start a timer, get the elapsed time since the timer was started,
    and get the current time in nanoseconds.
    """

    def __init__(self) -> None:
        """
        Initializes a new MiniTimer instance with the start time set to 0.
        """
        self._time_ = 0
    
    def start_time(self):
        """
        Starts or restarts the timer by recording the current time in nanoseconds.
        """
        self._time_ = time.time_ns()

    def get_ellapsed_time(self) -> int:
        """
        Calculates and returns the elapsed time in nanoseconds since the timer was started.
        
        Returns:
            int: The elapsed time in nanoseconds.
        """
        return time.time_ns() - self._time_
    
    def get_time(self) -> int:
        """
        Returns the current time in nanoseconds.
        
        Returns:
            int: The current time in nanoseconds.
        """
        return time.time_ns()
