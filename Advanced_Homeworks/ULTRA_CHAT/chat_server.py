# Let's get it started!)
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


##______________________________________________________________________________________________________________
## TODO: Лог чата для восстановки истории -- работало, но не так как хотелось, а теперь крашит всю программу, я не могу разобраться, не понимаю
# "помощь" -- готово
# изменение системных команд
# /*готово проверку имени пользователя на не плагиат других готово*/
# возможно личку(уже возможно, просто использовать какой-то другой порт, колхоз, но работает ведь)
##______________________________________________________________________________________________________________


# Assigning main "objects"
clients_dict = {}
addresses_dict = {}

HOST = "192.168.111.1"
PORT = 2552
BUFFER_SIZE = 1024
ADDRESS = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDRESS)

def connections_accepter():
# Func that accepting all of incoming client connections
    while True:
        client, client_address = SERVER.accept()
        print(client_address, " успешно подключён к серверу!")
        client.send(bytes\
        ("Вы были успешно подключены! Введите в строку отправки желаемое имя пользователя.",'utf8'))
        addresses_dict[client] = client_address
        Thread(target = client_activity, args = (client,)).start()

# обработка пользовательского ввода на сервере
def client_activity(client):
# переменная с помощью пользователю в освоении
    help = ['Для отправки сообщения помимо кнопки можно использовать "Ctrl(Command)+Enter".',
            # 'Для получения истории(предидущих сообщений в чате) отправьте сообщение "/хроника".',
            'Для выхода из приложения чата можно также отправить сообщение "/выход".']
# Получение имени пользователя с проверкой на уникальность и неиспользование технических конструкций чата
    client_name = client.recv(BUFFER_SIZE).decode('utf8')
    if client_name in clients_dict.values() or client_name.startswith('/') or client_name.startswith('[Хроника]') :
        client.send(bytes("Такое имя уже занято или недопустимо(1-й '/' или [Хроника]).", 'utf8'))
        client_activity(client)
# стандартный сценарий работы с пользователем
    else:
        clients_dict[client] = client_name
        WELCOME_MESSAGE = "Добро пожаловать в чат " + client_name + '! Введите "/помощь" для вывода справки.'
        client.send(bytes(WELCOME_MESSAGE, 'utf8'))
        message = bytes(client_name + " присоединился к нам!", 'utf8')
        messages_poster(message)
        while True:
            # print(clients_dict)
            message = client.recv(BUFFER_SIZE)
# Тут идёт проверка на команду выхода из чата и приложения чата пользователем с последующей обработкой
            if message == bytes('/выход', 'utf8'):
                # print(type(client_name))
                # print(type(message))
                # print(message)
                message = bytes(client_name + " покинул нас(в плане чата XD)!", 'utf8')
                client.close()
                del clients_dict[client]
                messages_poster(message)
                break
# Тут идёт проверка на команду запроса истории чата пользователем с последующей обработкой
            # elif message == bytes("/хроника", "utf8"):
            #     log_to_user(client)
# Тут идёт проверка на команду запроса справки/помощи пользователем с последующей обработкой
            elif message == bytes("/помощь", "utf8"):
                for tip in help:
                    client.send(bytes(tip + "\n", 'utf8'))
            else:
                messages_poster(message, client_name + ': ')

#пока выключу это
# def log_to_user(client):
#     client.send(bytes('У сообщений из "хроники" перед именем пользователя будет надпись "Хроника>>>"', 'utf8'))
#     log_file = open("chat_log.txt", "r")
#     log_list = [line.split("\nnewline_marker") for line in log_file]
#     for line in log_list:
#         send_line = str(line)
#         print(type(line))
#         client.send(bytes('Хроника>>>' + send_line, 'utf8'))
#     del log_list
#     log_file.close()


def messages_poster(message, nicknamer="system: "):
    try:
        for socket in clients_dict:
            socket.send(bytes(nicknamer, 'utf8') + message)
            log_file = open("chat_log.txt", "a")
            log_file.write(nicknamer + message.decode('utf8') + "\nnewline_marker")
            log_file.close()
    except: pass

if __name__ == "__main__":
    SERVER.listen(11)
    print("Ожидание подключения пользователей...")
    CLIENT_ACCEPTION_THREAD = Thread(target=connections_accepter)
    CLIENT_ACCEPTION_THREAD.start()
    CLIENT_ACCEPTION_THREAD.join()
    LOG_TO_CLIENT_THREAD = Thread(target=client_activity)
    LOG_TO_CLIENT_THREAD.start()
    LOG_TO_CLIENT_THREAD.join()
    SERVER.close()
