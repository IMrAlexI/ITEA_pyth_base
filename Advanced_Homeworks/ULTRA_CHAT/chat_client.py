from threading import Thread
from socket import AF_INET, SOCK_STREAM, socket
from tkinter import *


HOST = input('Введите значение хоста(просто пустое поле для значения по умолчанию): ')
PORT = input('Введите знаяение порта(просто пустое поле для значения по умолчанию): ')

if not HOST:
    HOST = "192.168.111.1"
if not PORT:
    PORT = 2552
else:
    PORT = int(PORT)

BUFFER_SIZE = 1024
ADDRESS = (HOST, PORT)

socket_for_client = socket(AF_INET, SOCK_STREAM)
socket_for_client.connect(ADDRESS)


def messages_reciever():
    while True:
        try:
            message = socket_for_client.recv(BUFFER_SIZE).decode('utf8')
            messages_list.insert(END, message)
        except OSError('<--пользователь покинул чат('):
            break


def messages_sender(event = None):
    message = current_message.get()
    current_message.set('')
    socket_for_client.send(bytes(message, 'utf8'))
    if message == '/выход':
        socket_for_client.close()
        GUI_closing_after_sender()


def GUI_closing(event = None):
    current_message.set("/выход")
    messages_sender()
    GUI_closing_after_sender()


def GUI_closing_after_sender():
    MAIN_APP_FRAME.destroy()
    from sys import exit
    exit(0)

#Непесредственно весь интерфейс
# Главное окно
MAIN_APP_FRAME = Tk()
MAIN_APP_FRAME.title('Факс - чат для избранных')
# Блок для ввода/вывода сообщений
SHOW_MESSAGES_FRAME = Frame(MAIN_APP_FRAME)
# текстовая строка
current_message = StringVar()
current_message.set("Текст сообщения необходимо вводить в эту строку...")
# Ползунок
SCROLLBAR = Scrollbar(SHOW_MESSAGES_FRAME)
# Окно вывода
messages_list = Listbox(SHOW_MESSAGES_FRAME,height = 30, width = 110, yscrollcommand = SCROLLBAR.set, bg = "black", fg = "violet")
# Привязка єлементов к позициям в блоке
SCROLLBAR.pack(side = RIGHT, fill = Y)
messages_list.pack(side = LEFT, fill = BOTH)
# Сборка блока
SHOW_MESSAGES_FRAME.pack()

# Сторока ввода: действия
TEXT_INPUT_FIELD = Entry(MAIN_APP_FRAME, textvariable = current_message, width = 102, bg = "black", fg = "violet")
TEXT_INPUT_FIELD.bind('<Control-Return>', messages_sender)
TEXT_INPUT_FIELD.pack(side = 'left', fill = Y)
# Кнопка отправки
SEND_BUTTON = Button(MAIN_APP_FRAME, text = 'Отправить', command = messages_sender, bg = "black", fg = "violet")
SEND_BUTTON.pack(side = 'right')

# Закрытые интерфейса при закрытии приложения
MAIN_APP_FRAME.protocol("WM_DELETE_WINDOW", GUI_closing)

# Запуск потока интерфейса
receiver_thread = Thread(target=messages_reciever)
receiver_thread.start()
mainloop()


# способ ввода сетевых данных непосредственно из командной строки
if __name__ == '__main__':
    import sys
    BUFFER_SIZE = 1024
    args = sys.argv[1:]
    HOST, PORT, *_ = args
    ADDRESS = (HOST, PORT)

    socket_for_client = socket(AF_INET, SOCK_STREAM)
    socket_for_client.connect(ADDRESS)
    receiver_thread = Thread(target=messages_reciever)
    receiver_thread.start()
    mainloop()
