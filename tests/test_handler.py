import pytest

from callqueue.database import Database, DatabaseError, InMemoryDatabase
from callqueue.handler import CallerManager
from callqueue.queueservice import QueueService


@pytest.fixture
def caller_manager():
    database = InMemoryDatabase()
    queue_service = QueueService()
    return CallerManager(database, queue_service)


class FailingDatabase(Database):
    def store_call(self, call):
        raise DatabaseError('boom!')


@pytest.fixture
def db_failing_manager():
    database = FailingDatabase()
    queue_service = QueueService()
    return CallerManager(database, queue_service)


@pytest.fixture
def queue_full_manager():
    database = InMemoryDatabase()
    full_queue = QueueService(max_calls=1)
    full_queue.put('cid')
    return CallerManager(database, full_queue)


def test_greet_caller(caller_manager):
    caller = {'call_id': 'cid'}
    expected_queue_pos = '1'

    ncco = caller_manager.greet_caller(caller)

    assert ncco[0]['action'] == 'talk'
    assert expected_queue_pos in ncco[0]['text']
    assert ncco[1]['action'] == 'stream'


def test_greet_caller_db_failure(db_failing_manager):
    caller = {'call_id': 'cid'}

    ncco = db_failing_manager.greet_caller(caller)

    assert ncco[0]['action'] == 'hangup'


def test_greet_caller_queue_full(queue_full_manager):
    caller = {'call_id': 'cid'}

    ncco = queue_full_manager.greet_caller(caller)

    assert ncco[0]['action'] == 'hangup'
