class DatabaseError(Exception):
    """Base class for database errors"""
    pass


class Database(object):

    def store_call(self, call):
        raise NotImplementedError


class InMemoryDatabase(Database):

    def __init__(self):
        self._db = {}

    def store_call(self, call):
        call_id = call['call_id']

        if call_id in self._db:
            raise DatabaseError('call {} already stored'.format(call_id))

        self._db[call_id] = call
