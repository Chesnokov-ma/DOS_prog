from greed_int import GreedIntervalSplit
from gE_int import gemCalculator
from heat_capacity import HeatCapacityCalculator

if __name__ == '__main__':
    N = 40                              # размер системы
    dots_num = 1000                     # кол-во интервалов (точек на графике gem минус 1)

    GreedIntervalSplit(N, dots_num)     # вычислить интервалы и сложить в файл
    print('Данные разбиты на интервалы')

    gemCalculator(N)                    # вычислить gem и сложить в файл
    print('DOS рассчитан')


