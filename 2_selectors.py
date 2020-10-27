import socket
import selectors


selector = selectors.DefaultSelector()


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_address = ('localhost', 5000)
    server_socket.bind(server_address)
    server_socket.listen()

    selector.register(fileobj=server_socket,
                      events=selectors.EVENT_READ,
                      data=accept_connection)


def accept_connection(server_socket):
    client_socket, client_address = server_socket.accept()
    print('Connection from', client_address)
    selector.register(fileobj=client_socket,
                      events=selectors.EVENT_READ,
                      data=send_message)


def send_message(client_socket):
    request = client_socket.recv(4096)
    print(request)
    print(client_socket)

    if request == b'stop_server\r\n':
        exit()
    elif request == b'\r\n' or not request:
        selector.unregister(client_socket)
        client_socket.close()
    else:
        response = 'Hello, world!\r\n'
        client_socket.send(response.encode())


def event_loop():
    while True:
        events = selector.select() # method returns (key, events)
        # "key" have folowing methods:
        # key.fileobj(), key.events(), key.data()

        for key, _ in events:
            callback = key.data
            callback(key.fileobj)



if __name__ == "__main__":
    start_server()
    event_loop()
