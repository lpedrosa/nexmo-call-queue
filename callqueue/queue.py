class QueueServiceError(Exception):
    """Base class for QueueService exceptions."""
    pass

class QueueFullError(QueueServiceError):

    def __init__(self, message):
        super(QueueFullError, self).__init__(message)
        self.message = message

class QueueService(object):

    def __init__(self, max_calls=10):
        self._max_calls = max_calls

    def put(self, call):
        """Put a call in the queue.
        
        Returns the amount of calls queued (including this call).

        Raises QueueFullError if the queue limit has been reached.

        """
        pass

    def get(self):
        pass
