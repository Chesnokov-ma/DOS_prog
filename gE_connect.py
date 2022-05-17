# убрать M из данных (сколько всего g соотвтетсвует каждому E)
import pandas as pd
import sys


def gEconnect(file_name='src/gem_true.txt', out_name='src/gE_con_true.txt'):
    # file_name = 'src/dos_true.dat'

    out = open(out_name, 'w')
    try:
        # df = pd.read_csv(file_name, names=['E', 'M', 'g'], sep=' ')
        df = pd.read_csv(file_name, names=['g', 'E', 'M'], sep='\t')
    except FileNotFoundError:
        sys.exit(f'файл {file_name} еще не создан')

    df = df.sort_values(by=['E']).reset_index(drop=True)
    cur_E = df['E'].tolist()[0]
    loc_sum = 0
    glob_sum = 0

    for index, row in df.iterrows():
        if round(cur_E, 5) == round(row['E'], 5):
            loc_sum += int(row['g'])
        else:
            out.write(f'{round(cur_E, 5)}\t{int(loc_sum)}\n')
            # print(f'{cur_E}\t{int(loc_sum)}')
            glob_sum += loc_sum

            cur_E = round(row['E'], 5)
            loc_sum = row['g']


    # print("Glob sum = ", glob_sum)

    out.close()