import zmq

from db import session, Sale

BROKER_IP = 'localhost'
BROKER_PUB_PORT = 5500
BROKER_SUB_PORT = 5501
context = zmq.Context()

pub_socket = context.socket(zmq.PUB)
pub_socket.connect(f'tcp://{BROKER_IP}:{BROKER_PUB_PORT}')

sub_socket = context.socket(zmq.SUB)
sub_socket.connect(f'tcp://{BROKER_IP}:{BROKER_SUB_PORT}')
sub_socket.subscribe('payment')

def listener():
    while True:
        print('Waiting for payment')
        string_message = sub_socket.recv_string()
        message = sub_socket.recv_json()
        print('Payment received: ', message)
        try:
            session.query(Sale).filter(Sale.id == message['client_id']).update({'is_paid': True})
            session.commit()
        except Exception as e:
            print(e)
            session.rollback()

if __name__ == '__main__':
    listener()