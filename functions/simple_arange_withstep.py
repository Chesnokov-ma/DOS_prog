"""
    Возвращает список [start:end:step] с округлением до round_val
    Так как все остальные на удивление возвращают что-то типо
    0.59999999999999999994
"""


def simpleArangeWithStep(start, end, step, round_val=2):
    ret_lst = []
    value = start

    while value < end:
        value = round(value, round_val)
        ret_lst.append(value)
        value += step

    return ret_lst
