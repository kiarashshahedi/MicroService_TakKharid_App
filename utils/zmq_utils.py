import zmq

def create_socket(socket_type, address, bind=True):
    context = zmq.Context()
    socket = context.socket(socket_type)
    if bind:
        socket.bind(address)
    else:
        socket.connect(address)
    return socket
