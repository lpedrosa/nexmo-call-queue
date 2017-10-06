try:
    from Queue import Empty, Full, Queue
except ImportError:
    from queue import Empty, Full, Queue


class QueueServiceError(Exception):
    """Base class for QueueService errors."""
    pass


class QueueFullError(QueueServiceError):
    """Raised when the queue service cannot queue a call"""
    def __init__(self, message):
        super(QueueFullError, self).__init__(message)
        self.message = message


class QueueService(object):

    def __init__(self, max_calls=10):
        self._current_size = 0
        self._queue = Queue(maxsize=max_calls)

    def put(self, call):
        """Put a call in the queue.

        Returns the amount of calls queued so far (including this call).

        Raises `QueueFullError` if the queue limit has been reached.

        """
        try:
            self._queue.put(call, block=False)
            self._current_size += 1
        except Full:
            raise QueueFullError('call queue is full')

        return self._current_size

    def get(self):
        """Remove a call from the queue.

        Returns the queued call instance or None if there are no calls queued.

        """
        try:
            call = self._queue.get(block=False)
            self._current_size -= 1
        except Empty:
            return None

        return call
