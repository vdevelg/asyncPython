import socket
import sys


# socket == domain:port
# Создание сокета с протоколом сетевого уровня IPv4 и
# протоколом транспортного уровня TCP:
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_address = (sys.argv[1], int(sys.argv[2])) # IP and port
server_socket.bind(server_address)
server_socket.listen()

while True:

    print('Before .accept()')

    client_socket, client_address = server_socket.accept() # !!!БЛОКИРУЮЩАЯ ОПЕРАЦИЯ!!!
    print('Connected with: ', client_address)

    while True:

        print('Before .recv()')

        request = client_socket.recv(4 * 1024) # !!!БЛОКИРУЮЩАЯ ОПЕРАЦИЯ!!!
        print(request)
        if not request:
            break
        elif request == b'\r\n':
            print('Continue')
            continue
        else:
            response = 'Hello, world!\r\n'
            # БЛОКИРУЮЩАЯ ОПЕРАЦИЯ, если буфер отправки будет полон:
            client_socket.send(response.encode())

    client_socket.close()
    print('Disconnected from the client')
