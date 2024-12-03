import zmq
import logging
import json

logger = logging.getLogger(__name__)

class ZMQHandler:
    def __init__(self, zmq_url="tcp://127.0.0.1:5555"):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.zmq_url = zmq_url
        self.socket.connect(self.zmq_url)
        logger.info(f"Connected to ZeroMQ at {self.zmq_url}")

    def send_message(self, data):
        try:
            self.socket.send_json(data)
            logger.info(f"Sent: {data}")
            response = self.socket.recv_json()
            logger.info(f"Received: {response}")
            return response
        except Exception as e:
            logger.error(f"ZeroMQ Error: {e}")
            return {"error": "Communication failed"}
