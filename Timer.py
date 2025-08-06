import time


class Timer:
    """
    Says when a certain amount of time has passed
    """
    def __init__(self, duration=-1):
        """
        :param duration: the duration of the timer. Puts a negative number for infinity
        """
        if duration < 0:
            self.__time_end = -1
        else:
            self.__time_end = time.time() + duration

    def is_finished(self) -> bool:
        return (not self.__time_end < 0) and time.time() > self.__time_end

    def increment_timer(self, incrementation):
        self.__time_end += incrementation

    def set_duration(self, duration):
        """ Reset the timer with the new_duration. It forgets the past duration. """
        if duration < 0:
            self.__time_end = -1
        else:
            self.__time_end = time.time() + duration

    def time_remaining(self) -> float:
        """ The time remaining before the end.
        If the end is already past, this function will return a negative number """
        return self.__time_end - time.time()
