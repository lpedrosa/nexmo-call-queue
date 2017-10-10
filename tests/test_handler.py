import pytest

from callqueue.database import Database, DatabaseError, InMemoryDatabase
from callqueue.handler import WorkflowManager, CallStates
from callqueue.queueservice import QueueService


@pytest.fixture
def database():
    database = InMemoryDatabase()
    return database


@pytest.fixture
def workflow_manager(database):
    queue_service = QueueService()
    return WorkflowManager(database, queue_service)


@pytest.fixture
def db_failing_manager():
    class FailingDatabase(Database):
        def store_call(self, call):
            raise DatabaseError('boom!')
    database = FailingDatabase()
    queue_service = QueueService()
    return WorkflowManager(database, queue_service)


@pytest.fixture
def queue_full_manager(database):
    full_queue = QueueService(max_calls=1)
    full_queue.put('cid')
    return WorkflowManager(database, full_queue)

##############################
# greet_caller tests
##############################

def test_greet_and_queue_when_everything_is_okay(workflow_manager):
    caller = {'call_id': 'cid'}
    expected_queue_pos = '1'

    ncco = workflow_manager.greet_caller(caller)

    assert ncco[0]['action'] == 'talk'
    assert expected_queue_pos in ncco[0]['text']
    assert ncco[1]['action'] == 'stream'


def test_greet_hangup_when_db_failure(db_failing_manager):
    caller = {'call_id': 'cid'}

    ncco = db_failing_manager.greet_caller(caller)

    assert ncco[0]['action'] == 'hangup'


def test_greet_hangup_when_queue_full(queue_full_manager):
    caller = {'call_id': 'cid'}

    ncco = queue_full_manager.greet_caller(caller)

    assert ncco[0]['action'] == 'hangup'


def test_dont_store_call_when_queue_full(queue_full_manager, database):
    caller = {'call_id': 'cid'}

    queue_full_manager.greet_caller(caller)

    assert database.retrieve_call(caller['call_id']) == None


##############################
# resolve_state tests
##############################

@pytest.mark.parametrize('state', CallStates.final)
def test_delete_call_when_is_final_state(workflow_manager, database, state):
    caller = {'call_id': 'cid'}

    workflow_manager.greet_caller(caller)
    workflow_manager.resolve_state(caller['call_id'], state)

    assert database.retrieve_call(caller['call_id']) == None
