import pytest

from callqueue.queue import QueueService, QueueFullError


def test_put_call():
    queue_service = QueueService()
    call = 'a call'

    res = queue_service.put(call)

    assert res == 1

def test_full_queue():
    queue_service = QueueService(max_calls=0)
    call = 'a call'

    with pytest.raises(QueueFullError):
        queue_service.put(call)
