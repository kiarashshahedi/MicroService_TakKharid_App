import zmq
import logging
import json

logger = logging.getLogger(__name__)

class ProductServiceZMQServer:
    def __init__(self, zmq_url="tcp://127.0.0.1:5555"):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.zmq_url = zmq_url
        self.socket.bind(self.zmq_url)
        logger.info(f"ZeroMQ Server running at {self.zmq_url}")

    def run(self):
        while True:
            try:
                message = self.socket.recv_json()
                logger.info(f"Received: {message}")
                response = self.process_message(message)
                self.socket.send_json(response)
            except Exception as e:
                logger.error(f"Error processing message: {e}")
                self.socket.send_json({"error": "Failed to process request"})

    def process_message(self, message):
        # Simulated product data or other logic
        if message.get("action") == "get_product_details":
            product_id = message.get("product_id")
            return {"product_id": product_id, "name": "Sample Product", "price": 100}
        return {"error": "Invalid action"}
