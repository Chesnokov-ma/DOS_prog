import pandas as pd
import sys
from math import e
from simple_arange_withstep import simpleArangeWithStep


class HeatCapacityCalculator:
    """ Загрузить файл с gem """
    def __init__(self, src_file='src/gem.txt'):
        try:
            self.__df = pd.read_csv(src_file, names=['E', 'g'], sep='\t')
        except FileNotFoundError:
            sys.exit(f'файл {src_file} еще не создан')

    """ Расчитать теплоескость для M = 0 и вывести в файл """
    def CalculateDemo(self, file_name='src/c.txt', k=1, T_start=0.0001, T_end=0.3, T_step=0.0001, T_size=100):

        # if T_step is None and T_size is not None:

        output_c_file = open(f'{file_name}', 'w')
        # PE_E_file = open('pe/pe.txt', 'w')

        df_m0 = self.__df
        t_lst = simpleArangeWithStep(start=T_start, end=T_end, step=T_step, round_val=4)
        # print(len(t_lst))

        g = df_m0['g'].tolist()
        E = df_m0['E'].tolist()
        counter = 0

        # with open('m0_ge.dat', 'w') as dem_file:
        #     for i in range(len(g)):
        #         # print(f'{g[i]}\t{E[i]}')
        #         dem_file.write(f'{E[i]}\t{g[i]}\n')

        for T in t_lst[0:]:     # цикл по температуре
            Z = 0   # статсумма
            for i in range(len(E))[:]:
                Z += g[i] * e ** (-1 * ((E[i] + 0.17998) / T))
                # print(g[i] * e ** (-1 * ((E[i] + 0.17998) / T)))

            # print(f'T={T}\tZ={Z}')

            PE = []     # массив вероятностей

            for i in range(len(E))[:]:
                PE.append((g[i] * e ** (-1 * ((E[i] + 0.17998) / T))) / Z)

            # with open(f'pe/pe{counter}.txt', 'w') as PE_E_file:
            #     for i in range(len(PE)):
            #         PE_E_file.write(f'{round(E[i], 5)}\t{round(PE[i], 5)}\n')

            # print(f'T={T}\tsum PE={sum(PE)}')

            delta_E2 = 0
            delta_E = 0     # <E> = sum(P(Ei) * Ei)
            for i in range(len(E)):
                delta_E += PE[i] * E[i]
                delta_E2 += PE[i] * (E[i] ** 2)
                # print(f'{E[i]}\t{PE[i] * E[i]}')

            #     # теплоемкость
            C = (delta_E2 - (delta_E ** 2)) / (T ** 2)
            print(f'T={T} => C={C}')
            output_c_file.write(f'{T}\t{round(C, 5)}\n')

            counter += 1

        output_c_file.close()


Cap = HeatCapacityCalculator('src/gE_con.txt')
Cap.CalculateDemo('src/c.txt')

pass
