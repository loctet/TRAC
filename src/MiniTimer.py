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


def measure_time(store_attr, key):
    """
    Decorator factory for methods: measures the execution time of the method in
    nanoseconds and stores it in ``getattr(self, store_attr)[key]``.

    The start timestamp is a local variable of each call, not shared timer state, so nested
    or repeated measurements cannot overwrite one another. The dictionary is looked up after
    the call, so the method can replace it (for example to reset its times) while it runs.
    The time is recorded even if the method raises an exception.

    Example::

        @measure_time("infos", "non_determinism")
        def n_det_check(self, ...):
            ...

    :param store_attr: Name of the instance attribute holding the target dictionary.
    :type store_attr: str
    :param key: Key under which the elapsed time is stored.
    :type key: str
    """

    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            start = time.perf_counter_ns()
            try:
                return func(self, *args, **kwargs)
            finally:
                getattr(self, store_attr)[key] = time.perf_counter_ns() - start

        return wrapper

    return decorator
