import socket
from select import select
# "select" working whith objects that contained method .fileno()


to_monitor = []

# Socket is domain and port.
# It works on protocols of media layers.
# The following protocols are sets here:
# 3 Network layer - IP protocol (addressing by domain)
# 4 Transport layer - TCP protocol (addressing by port)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_address = ('localhost', 5000)
server_socket.bind(server_address)
server_socket.listen()


def accept_connection(server_socket):
    client_socket, client_address = server_socket.accept()
    print('Connection from', client_address)

    to_monitor.append(client_socket)


def send_message(client_socket):
    request = client_socket.recv(4096)
    print(request)

    if request:
        response = 'Hello, world!\n'
        client_socket.send(response.encode())
    else:
        client_socket.close()


def event_loop():
    while True:
        ready_to_read, _, _ = select(to_monitor, [], []) # read, write, arrors

        for sock in ready_to_read:
            if sock is server_socket:
                accept_connection(sock)
            else:
                send_message(sock)



if __name__ == "__main__":
    to_monitor.append(server_socket)
    event_loop()
