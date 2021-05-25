import socket
import os
import glob


# Функция обработки запроса
def process(req):
    if req == 'pwd':
        return os.getcwd()
    # Команда ls
    elif req == 'ls':
        # Собрать в списке все файлы и каталоги
        files = []
        for filename in glob.iglob('**', recursive=True):
            files = files + [filename]
        # И вернуть список
        return '; '.join(files)
    else:
        reqs = req.split(" ")
        if len(reqs) != 2:
            if len(reqs) < 2:
                return 'bad request'
            # Если команда rename, переименовываем
            elif reqs[0] == 'rename':
                os.rename(reqs[1].replace('..', ''), reqs[2].replace('..', ''))
                return 'Изменения файла успешно сохранены'
            else:
                return 'bad request'
        # Если команда mkdir, создаем каталог
        elif reqs[0] == 'mkdir':
            os.mkdir(reqs[1].replace('..', ''))
            return 'Директория создана'
        # Если команда rmdir, удаляем каталог
        elif reqs[0] == 'rmdir':
            os.rmdir(reqs[1].replace('..', ''))
            return 'Директория удалена'
        # Если команда rmfile, удаляем файл
        elif reqs[0] == 'rmfile':
            os.remove(reqs[1].replace('..' , ''))
            return 'Файл удален'
        # Если команда download, читаем требуемый файл
        elif reqs[0] == 'cut':
            ref = req.split(" ")[1].replace('..', '')
            myfile = open(ref, "r")
            data = myfile.read()
            myfile.close()

            datasize = len(data)
            request = str(datasize) + " " + data
            return request
        else:
            return 'bad request'


# Номер порта
PORT = 9090

# Переходим в нужный каталог
os.chdir("DATA")

# Вечный цикл
while True:
    # Создаем сокет
    print("Создаем новый сокет")
    sock = socket.socket()
    sock.bind(('' , PORT))
    sock.listen()

    while True:
        print('Слушаем порт' , PORT)
        # Если кто-то подключился, выводим это
        conn , addr = sock.accept()
        print(addr)
        # Получаем команду
        request = conn.recv(8192).decode()
        print(request)

        # Если это выход, выходим и мы
        if request == "exit":
            break

        # Обработать запрос
        response = process(request)
        # Отправить ответ обратно
        conn.send(response.encode())

    # Если команда выход, закрыть сокет
    sock.close()
