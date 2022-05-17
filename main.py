from greed_int import GreedIntervalSplit
from gE_int import gemCalculator
from heat_capacity import HeatCapacityCalculator
from gE_connect import gEconnect
from gE_int_con import gEconnect_interval

import os.path

if __name__ == '__main__':
    N = 40                              # размер системы
    dots_num = 1000                     # кол-во интервалов (точек на графике gem минус 1)

    intervals = GreedIntervalSplit(N, dots_num).intervals     # вычислить интервалы и сложить в файл
    print('Данные разбиты на интервалы')

    gemCalculator(N)                    # вычислить gem и сложить в файл
    print('DOS рассчитан')

    glob_sum = 2 ** N
    print("\nТочная глобальная сумма g = ", glob_sum)

    # gEconnect('src/gem.txt', 'src/gE_con.txt)            # избавления от столбца M (соединение g и E в одну таблицу)
    # получается более неточный, но в общем похожий на полный перебор график

    gEconnect_interval(intervals, glob_sum_true=glob_sum)

    Cap = HeatCapacityCalculator('src/gE_con.txt')
    Cap.CalculateCap('src/c.txt')

