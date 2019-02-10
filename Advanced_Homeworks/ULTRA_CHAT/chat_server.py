# Let's get it started!)
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


##______________________________________________________________________________________________________________
## TODO: Лог чата для восстановки истории,
 # /*готово проверку имени пользователя на не плагиат других готово*/
 # возможно личку!!!
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


def client_activity(client):
# Func that is processing client's requests(messages)
    client_name = client.recv(BUFFER_SIZE).decode('utf8')
    if client_name in clients_dict.values():
        client.send(bytes("Такое имя пользователя уже занято, попробуйте другой вариант.", 'utf8'))
        client_activity(client)
    else:
        clients_dict[client] = client_name
        WELCOME_MESSAGE = "Добро пожаловать в чат " + client_name + "! Введите '/выход' для выхода из чата."
        client.send(bytes(WELCOME_MESSAGE, 'utf8'))
        message = bytes(client_name + " присоединился к нам!", 'utf8')
        messages_poster(message)
        while True:
            # print(clients_dict)
            message = client.recv(BUFFER_SIZE)
            if message != bytes('/выход', 'utf8'):
                # print(type(client_name))
                # print(type(message))
                # print(message)
                messages_poster(message, client_name + ': ')
            else:
                message = bytes(client_name + " покинул нас(в плане чата XD)!", 'utf8')
                client.close()
                del clients_dict[client]
                messages_poster(message)
                break


def messages_poster(message, nicknamer="system: "):
    try:
        for socket in clients_dict:
            socket.send(bytes(nicknamer, 'utf8') + message)
    except: pass

if __name__ == "__main__":
    SERVER.listen(11)
    print("Ожидание подключения пользователей...")
    CLIENT_ACCEPTION_THREAD = Thread(target=connections_accepter)
    CLIENT_ACCEPTION_THREAD.start()
    CLIENT_ACCEPTION_THREAD.join()
    SERVER.close()
