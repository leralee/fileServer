import socket

# Устанавливаем соединение
HOST = 'localhost'
PORT = 9090
while True:
    # Подключаемся к серверу
    sock = socket.socket()
    sock.connect((HOST, PORT))
    # Получаем команду
    request = input('Введите команду: ')

    # Отправляем запрос
    sock.send(request.encode())

    # Если запрос - exit, выходим из клиента
    if request == "exit":
        break

    # Получаем ответ
    response = sock.recv(8192).decode()

    # Если ответа нет
    if not response:
        print("No data was received")
    else:
        # Печатаем ответ
        print(response)

    # Закрываем сокет
    sock.close()
