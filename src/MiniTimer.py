import time
from functools import wraps


class MiniTimer:
    """
    A simple timer class for measuring elapsed time in nanoseconds.

    This class provides methods to start a timer, get the elapsed time since the timer was started,
    and get the current time in nanoseconds. It is mostly used for timeout checks: for measuring
    the execution time of a function, prefer the :func:`measure_time` decorator, which keeps its
    timestamp local to the call and is therefore safe for nested or concurrent measurements.
    """

    def __init__(self) -> None:
        """
        Initializes a new MiniTimer instance with the start time set to 0.
        """
        self._time_ = 0

    def start_time(self):
        """
        Starts or restarts the timer by recording the current monotonic time in nanoseconds.
        """
        self._time_ = time.perf_counter_ns()

    def get_elapsed_time(self) -> int:
        """
        Calculates and returns the elapsed time in nanoseconds since the timer was started.

        Returns:
            int: The elapsed time in nanoseconds.
        """
        return time.perf_counter_ns() - self._time_

    def get_ellapsed_time(self) -> int:
        """
        Backward-compatible alias of :meth:`get_elapsed_time` (historical misspelling).
        """
        return self.get_elapsed_time()

    def get_time(self) -> int:
        """
        Returns the current monotonic clock reading in nanoseconds.

        Returns:
            int: The current time in nanoseconds.
        """
        return time.perf_counter_ns()


def measure_time(target, key, accumulate=False):
    """
    Decorator factory that measures the execution time of a function in nanoseconds
    and stores the result in a dictionary.

    The timestamp is kept in a local variable for the duration of the call, instead of
    being stored on a shared timer object. This makes measurements independent from each
    other, so nested or repeated calls cannot overwrite one another.

    :param target: Either the name of an instance attribute holding the target dictionary
                   (the wrapped function is then expected to be a method), or a callable
                   receiving the same arguments as the wrapped function and returning the
                   target dictionary.
    :type target: str | callable
    :param key: Key under which the elapsed time is stored.
    :type key: str
    :param accumulate: If True, add the elapsed time to the existing value instead of
                       replacing it. Useful when timing several runs of the same function.
    :type accumulate: bool
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter_ns()
            try:
                return func(*args, **kwargs)
            finally:
                elapsed = time.perf_counter_ns() - start
                store = getattr(args[0], target) if isinstance(target, str) else target(*args, **kwargs)
                if accumulate:
                    store[key] = store.get(key, 0) + elapsed
                else:
                    store[key] = elapsed

        return wrapper

    return decorator
