import socket
import selectors
import sys

# функция по умолчанию в операционной системе
# для отслеживания изменения объектов, 
# имеющих файловый дескриптор
selector = selectors.DefaultSelector()


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # связывание сокета с IP-адресом и портом,
    # которые передаются в аргументах командной строки при вызове скрипта
    server_address = (sys.argv[1], int(sys.argv[2]))
    server_socket.bind(server_address)
    server_socket.listen()
    # регистрация объекта, имеющего файловый дексриптор (сокета),
    # для начала отслеживания его изменений
    selector.register(fileobj=server_socket,
                      events=selectors.EVENT_READ,
                      data=accept_connection) # в data можно передать любой объект Python, 
                                              # в данном случае это объект функции


def accept_connection(server_socket):
    client_socket, client_address = server_socket.accept()
    print('Connected with:', client_address)
    selector.register(fileobj=client_socket,
                      events=selectors.EVENT_READ,
                      data=send_message) # в data можно передать любой объект Python, 
                                         # в данном случае это объект функции


def send_message(client_socket):
    request = client_socket.recv(4096)
    print(request)
    print(client_socket)

    if request == b'stop_server':
        exit()
    elif request == b'\r\n' or not request:
        selector.unregister(client_socket)
        client_socket.close()
    else:
        response = 'Hello, world!'
        client_socket.send(response.encode())


def event_loop():
    while True:
        # .select() возвращает список кортежей (key, events),
        # для изменившихся объектов с файловым дескриптором (сокетов)
        events = selector.select()
        # key - это объект SelectorKey типа named_tuple (из модуля collections)
        # он имеет следующие поля: key.fileobj, key.events, key.data,
        # соответствующие параметрам, переданным при регистрации сокетов

        for key, _ in events:
            # callback присваивается объект функции,
            # связаный с сокетом на этапе его регистрации
            callback = key.data
            callback(key.fileobj)



if __name__ == "__main__":
    start_server()
    event_loop()
