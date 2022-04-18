from greed_int import GreedIntervalSplit
from gE_int import gemCalculator

if __name__ == '__main__':
    N = 40                              # размер системы
    dots_num = 1000                     # кол-во интервалов (точек на графике gem)

    GreedIntervalSplit(N, dots_num)     # вычислить интервалы и сложить в файл
    gemCalculator(N)                    # вычислить gem и сложить в файл
