import math as m


def add(first_num, second_num):
    return first_num + second_num

def sub(first_num, second_num):
    return first_num - second_num

def mul(first_num, second_num):
    return first_num * second_num

def div(first_num, second_num):
    try:
        return first_num / second_num
    except ZeroDivisionError:
        print("\n   Ошибка деления на ноль! Результатом является бесконечно большое число!")


def pow(pow_num, pow_value):
    return pow_num ** pow_value

def root(root_num, root_value):
    try:
        return root_num ** (1 / root_value)
    except ZeroDivisionError:
        print("\n   Нельзя вычислить корень 0 степени из числа!")
        #нужна ошибка корня из отрицателього числа

def geom_sin(geom_num):
    return m.sin(m.radians(geom_num))

def geom_cos(geom_num):
    return m.cos(m.radians(geom_num))

def geom_tg(geom_num):
    return m.tan(m.radians(geom_num))

def geom_ctg(geom_num):
    return m.atan(m.radians(geom_num))
