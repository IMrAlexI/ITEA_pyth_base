""" Задание №2.
Переделать Задание №1 с созданием и использованием собственное исключение
WhitespaceError с атрибутами:
    position - позиция в строке
    symbol - какой именно непечатный символ
Функция main() демонстрирует работу вашей функции, должна красиво показывать
что именно вызвало исключение.
"""


from string import whitespace

text = """!My
name_is_Alex!"""

class WhitespaceError(Exception):
    def __init__(self, position, symbol):
        self.position = position
        self.symbol = symbol


def string_processing(text, *args, **kwargs):
    # блок вашего кода, который преобразовывает строку к новому виду,
    # которое сохроняете в переменной result
    result = "WOW " + text.upper() * 3 + " WOW"
    """
    Там, где у вас вызывается исключение,
    необходимо сохранить позицию и ошибочный символ в атрибуты исключения
    следующим блоком кода
    вызов_исключения WhitespaceError(ваща_переменна_позиции, ваша_переменная_символа)
    """
# Сказано - сделано
    for sym in text:
        if sym in whitespace:
            raise WhitespaceError(text.find(sym) + 1, repr(sym))
    return result


def main():
    """
    Вызываете свою функцию с тестовыми данными и красиво сообщаете о том, что произошло
    """
    try:
        result = string_processing(text, whitespace)
        print("Ваш текст для названия:", result)
    except WhitespaceError as e:
        print("Вы ввели исключённый символ, он находится под номером {}, а его репрезентация - {}".format(e.position, e.symbol))

if __name__ == "__main__":
    main()
