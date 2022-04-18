# Ключи-значения для интервалов из жадных данных
import pandas as pd
import sys


class GreedIntervalSplit:
    def __init__(self, N, dots_num, to_file=True):
        try:
            df = pd.read_csv(f'src/MinMax_{N}.dat', names=['m', 'E'], sep='\t')
        except FileNotFoundError:
            sys.exit(f'файл MinMax_{N}.dat не найден')

        f_keys = open('src/greed_keys.txt', 'w')

        m_lst = df['m'][int(df.shape[0] / 2):].to_list()
        Emin_lst = df['E'][:int(df.shape[0] / 2)].to_list()
        Emax_lst = df['E'][int(df.shape[0] / 2):].to_list()

        min_max = pd.DataFrame(columns=['m', 'Emin', 'Emax'], data={'m': m_lst, 'Emin': Emin_lst, 'Emax': Emax_lst})
        min_max = min_max.query('m >= 0')[::-1]
        del m_lst, Emin_lst, Emax_lst, df

        self.__intervals = []

        for index, row in min_max.query(f'm != {N}').iterrows():
            step = (row['Emax'] - row['Emin']) / dots_num  # шаг
            tmp_lst = []
            for i in range(0, dots_num):
                tmp_lst.append(row['Emin'] + step * i)
                f_keys.write('{0:.7f} '.format(row['Emin'] + step * i))   # ключи-энергии интервалов
            self.__intervals.append(tmp_lst)
            f_keys.write('\n')

        f_keys.close()

    @property
    def interval(self):
        return self.__intervals
