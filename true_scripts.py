""" Скрипты для работы с точными данными """
import pandas as pd
import sys
from heat_capacity import HeatCapacityCalculator


# Реформатировать согласно моему формату
def reformat_true_dos(file_name='src/dos_true.dat'):
    try:
        df = pd.read_csv(file_name, names=['E', 'M', 'g'], sep=' ')
    except FileNotFoundError:
        sys.exit(f'файл {file_name} еще не создан')

    with open('src/gem_true.txt', 'w') as f:
        g = df['g'].tolist()
        E = df['E'].tolist()
        M = df['M'].tolist()

        for i in range(len(g)):
            f.write(f'{g[i]}\t{round(E[i], 5)}\t{M[i]}\n')


# reformat_true_dos()
Cap = HeatCapacityCalculator(src_file='src/gem_true.txt')
Cap.CalculateDemo('src/c_true.txt')
