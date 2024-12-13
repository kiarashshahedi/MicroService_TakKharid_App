import zmq
import json
from django.conf import settings


class ZMQHandler:
    def __init__(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)  # Publisher socket
        self.socket.bind(f"tcp://*:{settings.ZMQ_PORT}")

    def send_message(self, topic, data):
        message = json.dumps({'topic': topic, 'data': data})
        self.socket.send_string(f"{topic} {message}")


zmq_handler = ZMQHandler()
