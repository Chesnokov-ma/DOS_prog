# убрать M из данных (сколько всего g соотвтетсвует каждому E) для подхода с интервалами
# не идеальный вариант, но должно сильно повысить точность относительно того, что есть
# или не должно...

import pandas as pd
import sys


def gEconnect_interval(intervals, file_name='src/gem.txt', out_name='src/gE_con.txt', glob_sum_true=None):
    out = open(out_name, 'w')
    try:
        df = pd.read_csv(file_name, names=['g', 'E', 'M'], sep='\t')
        print("Глобальная сумма (до) = ", df['g'].sum())
        df = df.drop(df[df.g == 0].index)
    except FileNotFoundError:
        sys.exit(f'файл {file_name} еще не создан')

    main_interval = intervals[0]
    for i in range(len(main_interval)):
        main_interval[i] = round(main_interval[i], 5)

    df = df.sort_values(by=['E']).reset_index(drop=True)

    if glob_sum_true is not None:
        print("Потеря точности по g = ", df['g'].sum() / glob_sum_true)

    # за основу брать 0-й интервал (M = 0)
    # -> если энергия принадлежит интервалу
    # -> ее g уходит в него
    # -> в итоговом df по энергиям из первого столца

    cur_E = df['E'].tolist()[0]
    loc_sum = 0
    glob_sum = 0

    E_lst, g_lst = [], []

    for index, row in df.iterrows():
        if round(cur_E, 5) == round(row['E'], 5):
            loc_sum += int(row['g'])
        else:
            # print(f'{cur_E}\t{int(loc_sum)}')
            E_lst.append(cur_E); g_lst.append(loc_sum)
            glob_sum += loc_sum

            cur_E = round(row['E'], 5)
            loc_sum = row['g']

    i_E = 0

    gE_dict = dict.fromkeys(main_interval, 0)

    for i in range(len(main_interval) - 1):
        for j in range(len(E_lst)):
            if main_interval[i] < E_lst[j] <= main_interval[i + 1]:
                gE_dict[main_interval[i]] += g_lst[j]

    glob_sum = 0
    for key, value in gE_dict.items():
        out.write(f'{round(key, 5)}\t{int(value)}\n')
        glob_sum += value

    print("Глобальная сумма (после) = ", glob_sum)
    if glob_sum_true is not None:
        print("Потеря точности после расчета = ", glob_sum / df['g'].sum())
        print("Итог: ", glob_sum / glob_sum_true)
    print("\n")

    pass