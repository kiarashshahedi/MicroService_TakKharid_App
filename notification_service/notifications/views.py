from utils.zmq_utils import create_socket
import zmq

def run_notification_service():
    socket = create_socket(zmq.REP, "tcp://127.0.0.1:5555")
    while True:
        message = socket.recv_json()
        mobile = message.get("mobile")
        otp = message.get("otp")
        # Simulate sending OTP via SMS
        print(f"Sending OTP {otp} to mobile {mobile}")
        socket.send_json({"status": "sent"})
