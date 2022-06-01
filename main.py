from greed_int import GreedIntervalSplit
from gE_int import gemCalculator
from heat_capacity import HeatCapacityCalculator
from gE_connect import gEconnect
from gE_int_con import gEconnect_interval
from gem_Post_Calc import gemPost
import time


if __name__ == '__main__':
    start_time = time.time()

    N = 40                              # размер системы
    dots_num = 1000                     # кол-во интервалов (точек на графике gem минус 1)

    intervals = GreedIntervalSplit(N, dots_num).intervals     # вычислить интервалы и сложить в файл
    print('Данные разбиты на интервалы')

    gemCalculator(N)                    # вычислить gem и сложить в файл
    print('DOS рассчитан')

    glob_sum = 2 ** N
    print("\nТочная глобальная сумма g = ", glob_sum)

    # post = gemPost()              # здесь что-то работает не так
    # post.fix_low_E_zone()         # линии на графике gem идут неверно через одну
    # print('Пост обработка завершена\n')      # возможно в расчете площади

    # gEconnect('src/gem.txt', 'src/gE_con.txt')            # избавления от столбца M (соединение g и E в одну таблицу)

    # тоже что и выше только в интервальном виде
    gEconnect_interval(intervals, glob_sum_true=glob_sum, file_name='src/gem.txt')
    Cap = HeatCapacityCalculator('src/gE_con.txt')
    Cap.CalculateCap('src/c.txt')

    print(f'\nПотребовалось всего: {round(time.time() - start_time, 2)} сек')


