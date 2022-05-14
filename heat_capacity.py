import pandas as pd
import sys
from math import e
from simple_arange_withstep import simpleArangeWithStep


class HeatCapacityCalculator:
    """ Загрузить файл с gem """
    def __init__(self, src_file='src/gem.txt'):
        try:
            self.__df = pd.read_csv(src_file, names=['g', 'E', 'M'], sep='\t')
        except FileNotFoundError:
            sys.exit(f'файл {src_file} еще не создан')

    """ Расчитать теплоескость для M = 0 и вывести в файл """
    def CalculateDemo(self, file_name='src/c.txt', k=1, T_start=-5.0, T_end=5.0, T_step=0.11):
        # не брать числа на подобие T_step=0.1 ==> (T = 0) ==> деление на ноль

        output_c_file = open(f'{file_name}', 'w')
        df_m0 = self.__df.query('M == 0')   # gem для M=0
        t_lst = simpleArangeWithStep(start=T_start, end=T_end, step=T_step, round_val=4)

        g = df_m0['g'].tolist()
        E = df_m0['E'].tolist()

        for T in t_lst[:]:     # цикл по температуре
            Z = 0   # статсумма
            for i in range(len(g)):
                Z += g[i] * (e ** -(E[i] / k*T))

            PE = []     # массив вероятностей
            for i in range(len(E)):
                PE.append((g[i] * (e ** -(E[i] / k*T))) / Z)

            delta_E = 0     # <E> = sum(P(Ei) * Ei)
            delta_E2 = 0
            for i in range(len(E)):
                delta_E += PE[i] * E[i]
                delta_E2 += (PE[i] * E[i]) ** 2

            # теплоемкость
            C = (delta_E2 - (delta_E ** 2)) / k * (T ** 2)
            print(f'T={T} => C={C}')
            output_c_file.write(f'{T}\t{C}\n')

        output_c_file.close()


        pass


Cap = HeatCapacityCalculator()
Cap.CalculateDemo()

pass
