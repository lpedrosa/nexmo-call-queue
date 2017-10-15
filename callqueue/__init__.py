from flask import Flask, jsonify, request, logging

from callqueue.domain import parse_call
from callqueue.handler import WorkflowManager
from callqueue.database import InMemoryDatabase
from callqueue.queueservice import QueueService


app = Flask(__name__)
manager = WorkflowManager(InMemoryDatabase(), QueueService(), logger=logging.create_logger(app))


@app.route('/')
def index():
    return 'Hello World!'


@app.route('/queue', methods=['POST'])
def queue_call():
    body = request.json
    caller = parse_call(body)
    response = manager.greet_caller(caller)
    return jsonify(response)