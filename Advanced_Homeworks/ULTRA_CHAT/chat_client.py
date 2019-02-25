from threading import Thread
from socket import AF_INET, SOCK_STREAM, socket
from tkinter import *

# TODO: СКРОЛЛЫ ПОД МЫШЬ*ПОФИКСИТЬ(проблем со скролом у людей оказадось очень много, они интерактивны, однако не хотят перемещать ничего, хотя при использовании перемещения по тексту стрелками скролл меняет положение)
# Оптимизация роботы(некий уровень) -- готово
# Розветвление функционала -- готово
# Улучшение в плане запуска клиента -- готово: теперь ввод в консоли при старте клиента либо подключение к дефолтному из самого кода
# Поток запускается корректно -- готово: раньше запускался один поток дважды, что влекло за собой ошибки при работе с аргументами из-за асинхронности
# Более понятное начало работы с интерфейсом чата - готово
# Добавил ползунок для горизонтальной плоскости, а то длинные сообщения ведь тоже бывают(возможны изменения на другое решение)


def messages_reciever():
    while True:
        try:
            message = socket_for_client.recv(BUFFER_SIZE).decode('utf8')
            messages_list.insert(END, message)
        except:
            GUI_closing_after_sender()
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
current_message.set("Ввод имени и сообщений(в последующем) производить в этой строке ...")
# Ползунок
HOR_SCROLLBAR = Scrollbar(SHOW_MESSAGES_FRAME, orient = "horizontal")
VER_SCROLLBAR = Scrollbar(SHOW_MESSAGES_FRAME, orient = "vertical")
# Окно вывода
messages_list = Listbox(SHOW_MESSAGES_FRAME,height = 30, width = 110, xscrollcommand = HOR_SCROLLBAR.set,\
    yscrollcommand = VER_SCROLLBAR.set, bg = "black", fg = "violet")
# Привязка єлементов к позициям в блоке
HOR_SCROLLBAR.pack(side = BOTTOM, fill = X)
VER_SCROLLBAR.pack(side = RIGHT, fill = Y)
messages_list.pack(side = LEFT, fill = BOTH)
# Сборка блока
SHOW_MESSAGES_FRAME.pack()

# Сторока ввода: действия
TEXT_INPUT_FIELD = Entry(MAIN_APP_FRAME, textvariable = current_message, width = 102, bg = "black", fg = "violet", insertbackground = "yellow")
TEXT_INPUT_FIELD.bind('<Control-Return>', messages_sender)
TEXT_INPUT_FIELD.pack(side = 'left', fill = Y)
# Кнопка отправки
SEND_BUTTON = Button(MAIN_APP_FRAME, text = 'Отправить', command = messages_sender, bg = "black", fg = "violet")
SEND_BUTTON.pack(side = 'right')

# Закрытые интерфейса при закрытии приложения
MAIN_APP_FRAME.protocol("WM_DELETE_WINDOW", GUI_closing)


# +способ ввода сетевых данных непосредственно из командной строки
if __name__ == '__main__':
    import sys
    BUFFER_SIZE = 1024
    try:
        args = sys.argv[1:]
        HOST = ""
        PORT = ""
        HOST, PORT, *_ = args
    except:
        if not HOST:
            HOST = "192.168.111.1"
        if not PORT:
            PORT = "2552"
    finally:
        print(HOST, "_____", PORT)
        ADDRESS = (HOST, int(PORT))
        socket_for_client = socket(AF_INET, SOCK_STREAM)
        socket_for_client.connect(ADDRESS)
        receiver_thread = Thread(target=messages_reciever)
        receiver_thread.start()
        mainloop()
