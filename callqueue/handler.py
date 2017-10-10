import logging

from callqueue.database import DatabaseError
from callqueue.queueservice import QueueFullError


class WorkflowManager(object):

    def __init__(self, database, queue_service, logger=None):
        self._database = database
        self._queue = queue_service
        self._logger = logger or logging.getLogger(__name__)

    def greet_caller(self, caller):
        call_id = caller['call_id']

        try:
            self._database.store_call(caller)
        except DatabaseError:
            self._logger.exception('failed to store call {}'.format(call_id))
            return self._failure_ncco()

        try:
            queue_position = self._queue.put(call_id)
        except QueueFullError:
            # this is okay
            self._logger.warning('failed to queue call {}'.format(call_id))
            try:
                self._database.delete_call(call_id)
            except DatabaseError:
                self._logger.warning('failed to delete call {}'.format(call_id))
            return self._failure_ncco()

        return self._greet_ncco(queue_position)

    def _greet_ncco(self, queue_position):
        return [{
            'action': 'talk', 
            'text': 'You are position number {} in queue'.format(queue_position)
        },{
            'action': 'stream',
            'streamUrl': 'someurl',
            'loop': '0'
        }]

    def _failure_ncco(self):
        return [{'action': 'hangup'}]

    def transfer_agent(self, agent, caller):
        # make call to agent
        # issue transfer of caller to agent's conversation
        pass
