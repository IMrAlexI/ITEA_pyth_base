import os
from threading import Timer

def epic_exit():
    timeout = 5
    t = Timer(timeout, os._exit, [1])
    t.start()
    try:
        print("\n   ---Спасибо за то, что пользуетесь именно этим калькулятором!---")
        case = "\n   Введите что-то, если хотите продожить использовать приложение! У вас есть %d секунд...\n" % timeout
        answer = input(case)
    finally:
        t.cancel()
