import zmq
import json
from django.conf import settings
from django.core.wsgi import get_wsgi_application

# Initialize Django environment
application = get_wsgi_application()

from users.models import MyUser

def seller_validation_server():
    context = zmq.Context()
    socket = context.socket(zmq.REP)  # Reply socket
    socket.bind("tcp://*:5555")  # Listen on port 5555

    print("Seller validation server started...")

    while True:
        message = socket.recv_json()
        print("Received request:", message)

        user_id = message.get("user_id")
        try:
            user = MyUser.objects.get(id=user_id, is_seller=True)
            response = {"is_valid": True, "details": {"username": user.username}}
        except MyUser.DoesNotExist:
            response = {"is_valid": False, "details": {}}

        socket.send_json(response)

if __name__ == "__main__":
    seller_validation_server()
