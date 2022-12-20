import zmq
from flask import jsonify

from services.listener import pub_socket


def payment_process(request_sale, payment_method):
    payment_validation(request_sale)
    publish_payment(request_sale, payment_method)

def payment_validation(request_sale):
    if request_sale['is_paid']:
        return jsonify({
            'error': 'Sale is already paid'
        }), 400

def publish_payment(request_sale, payment_method):
    if payment_method == 'credit_card':
        pub_socket.send_string('credit_card', zmq.SNDMORE)
        pub_socket.send_json(request_sale)
    elif payment_method == 'debit_card':
        pub_socket.send_string('debit_card', zmq.SNDMORE)
        pub_socket.send_json(request_sale)