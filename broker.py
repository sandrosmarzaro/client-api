import zmq


def main():
    context = None
    frontend_socket = None
    backend_socket = None

    try:
        context = zmq.Context(1)

        frontend_socket = context.socket(zmq.SUB)
        frontend_socket.bind("tcp://*:5500")
        frontend_socket.subscribe("")

        backend_socket = context.socket(zmq.PUB)
        backend_socket.bind("tcp://*:5501")

        zmq.device(zmq.FORWARDER, frontend_socket, backend_socket)
    except Exception as e:
        print(e)
    finally:
        frontend_socket.close()
        backend_socket.close()
        context.term()


if __name__ == "__main__":
    main()