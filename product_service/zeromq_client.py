import zmq

def validate_seller(user_id):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)  # Request socket
    socket.connect("tcp://user_service:5555")  # Connect to User Service's ZeroMQ server

    # Send validation request
    socket.send_json({"user_id": user_id})

    # Receive response
    response = socket.recv_json()
    return response
