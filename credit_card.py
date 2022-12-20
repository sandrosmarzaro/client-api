import threading

import zmq

TOPIC = "credit_card"
BROKER_IP = "localhost"
BROKER_PUB_PORT = 5500
BROKER_SUB_PORT = 5501
context = zmq.Context()

pub_socket = context.socket(zmq.PUB)
pub_socket.connect(f"tcp://{BROKER_IP}:{BROKER_SUB_PORT}")

sub_socket = context.socket(zmq.SUB)
sub_socket.connect(f"tcp://{BROKER_IP}:{BROKER_SUB_PORT}")
sub_socket.subscribe(TOPIC)

def listener():
    while True:
        string_message = sub_socket.recv_string()
        message = sub_socket.recv_json()
        pub_socket.send_string('payment', zmq.SNDMORE)
        pub_socket.send_json({"sale_id": message["sale_id"], "is_paid": True})


if __name__ == '__main__':
    threading.Thread(target=listener).start()
