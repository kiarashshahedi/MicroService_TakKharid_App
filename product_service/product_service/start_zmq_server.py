from products.zmq_handlers import ProductServiceZMQServer

if __name__ == "__main__":
    zmq_server = ProductServiceZMQServer()
    zmq_server.run()
