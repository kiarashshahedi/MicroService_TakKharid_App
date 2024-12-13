import zmq

class ZeroMQClient:
    def __init__(self, server_address):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect(server_address)

    def send_request(self, message):
        self.socket.send_json(message)
        response = self.socket.recv_json()
        return response

class ZeroMQServer:
    def __init__(self, bind_address):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind(bind_address)

    def listen(self, handler):
        while True:
            message = self.socket.recv_json()
            response = handler(message)
            self.socket.send_json(response)
