import actions as act

def input_std_math(flag):

    operation = {
    "+" : act.add,
    "-" : act.sub,
    "*" : act.mul,
    "/" : act.div
                }

    while flag:
        try:
            first_num = float(input("   Введите число >>> "))
            oper = input("   Введите операцию >>> ")
            oper = oper.replace(" ", "")
            second_num = float(input("   Введите число >>> "))
        except ValueError:
            print("\n   Вы ввели число некоректно, повторите ввод!")
            continue
        else:
            flag = 0
        return operation[oper](first_num, second_num)

def input_geom_math(flag):
    operation = {
        "sin" : act.geom_sin,
        "cos" : act.geom_cos,
        "tg" : act.geom_tg,
        "ctg" : act.geom_ctg
    }
    while flag:
        try:
            oper = input("   Введите операцию(sin, cos, tg, ctg) >>> ")
            oper = oper.replace(" ", "")
            geom_num = float(input("   Введите обрабатываемое число >>> "))
        except ValueError:
            print("\n   Вы выполнили ввод некоректно, повторите ввод!")
            continue
        else:
            flag = 0
        return operation[oper](geom_num)

def input_pow_math(flag):
    while flag:
        try:
            pow_num = float(input("   Введите число >>>"))
            pow_value = float(input("   Введите числовое значение степени >>>"))
        except ValueError:
            print("   Вы ввели число некоректно, повторите ввод!")
            continue
        else:
            flag = 0
            return act.pow(pow_num, pow_value)

def input_root_math(flag):
    while flag:
        try:
            root_num = float(input("   Введите число >>>"))
            root_value = float(input("   Введите числовое значение корня >>>"))
        except ValueError:
            print("   Вы ввели число некоректно, повторите ввод!")
            continue
        else:
            flag = 0
        return act.root(root_num, root_value)
