import pytest

from callqueue.queueservice import QueueService, QueueFullError


@pytest.fixture
def unbounded_service():
    return QueueService()


@pytest.fixture
def full_service():
    service = QueueService(max_calls=1)
    service.put('something')

    return service


def test_put_call(unbounded_service):
    call = 'a call'
    res = unbounded_service.put(call)

    assert res == 1


def test_get_call(unbounded_service):
    service = QueueService()
    call = 'call 1'
    call2 = 'call 2'

    service.put(call)
    service.put(call2)

    assert service.get() == call
    assert service.get() == call2


def test_limited_queue():
    limited_service = QueueService(max_calls=1)
    call = 'a call'

    limited_service.put(call)

    with pytest.raises(QueueFullError):
        limited_service.put(call)


def test_full_queue(full_service):
    call = 'a call'

    with pytest.raises(QueueFullError):
        full_service.put(call)