import socket

# socket == domain:port

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_address = ('localhost', 5000)
server_socket.bind(server_address)
server_socket.listen()

while True:

    print('Before .accept()') # БЛОКИРУЮЩИЙ МЕТОД

    client_socket, client_address = server_socket.accept()
    print('Connection from', client_address)

    while True:

        print('Before .recv()') # БЛОКИРУЮЩИЙ МЕТОД

        request = client_socket.recv(4096)
        print(request)
        if not request:
            break
        elif request == b'\r\n':
            print('Continue')
            continue
        else:
            response = 'Hello, world!\n'
            client_socket.send(response.encode())

    print('Outside innet while loop')
    client_socket.close()
