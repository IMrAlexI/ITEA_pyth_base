from time import perf_counter


class callstat:
    """
    Декоратор, подсчитывающий количество вызовов и
    среднюю длительность вызова задекорированной функции.

    Пример использования:

    @callstat
    def add(a, b):
        return a + b

    >>> add.call_count
    0
    >>> add(1, 2)
    3
    >>> add.call_count
    1

    Подсказки по реализации: функторы, @property
    Для измерения времени выполнения - perf_counter, см. импорт.
    """
    def __init__(self, func):
        self.func = func
        self.__call_count = 0

    def __call__(self, *args, **kwargs):
        self.__call_count += 1
        result = self.func(*args, **kwargs)
        print("Функция была вызвана {} раз(-а)".format(self.__call_count))
        return result
    @property
    def call_count(self):
        return self.__call_count
