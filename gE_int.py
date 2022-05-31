import pandas as pd
import time
from functions.Nm_generate import Nm_generate


class gemCalculator:
    def __init__(self, N, E_last_val='-0.09758'):
        start_time = time.time()
        Nm = []
        with open('src/k.txt', 'r') as kf:
            for line in kf:
                try:
                    Nm.append(int(line))
                except:
                    Nm = Nm_generate(N, f=kf)
                    # sys.exit('Файл k.txt - проблема')
        del kf, line

        f_out = open('src/gem.txt', 'w')  # очистить файл
        del f_out

        # with open('src/gem.txt', 'w'):
        #     pass

        M = []
        for file_m in list(range(N))[::2]:
            M.append(file_m)
        count = 0

        with open('src/greed_keys.txt', 'r') as f:  # энергии-ключи из жадных данных
            for line in f:
                keys = line.replace('\n', '').split(' ')
                keys = [float(i) for i in keys if len(i) > 0]

                E_lst = []
                with open(f"MK_data_100/E_m{M[count]}.dat", 'r') as fe:  # для M = 0
                    for line in fe:
                        E_lst.append(float(line))
                    del line
                E_lst.sort()

                val_ind_saved = []  # индексы E соответствующие ключу (своему интервалу)
                val_len_saved_G = []  # g в каждом интервале
                tmp = []
                start_ind = 0

                # поиск индексов энергий для каждого интервала
                for i in range(1, len(keys)):
                    tmp = []
                    for e in E_lst[start_ind:]:
                        if keys[i - 1] <= e < keys[i]:
                            tmp.append(e)
                            start_ind += 1
                        elif e > keys[i]:
                            break
                    val_ind_saved.append(tmp) if len(tmp) > 0 else val_ind_saved.append([])

                for elem in val_ind_saved:
                    val_len_saved_G.append(len(elem))

                len_g = sum(val_len_saved_G)

                with open('src/gem.txt', 'a') as f_out:
                    for i in range(len(val_len_saved_G)):
                        f_out.write(f'{int(val_len_saved_G[i] * (Nm[count] / len_g))}\t{keys[i]}\t{M[count]}\n')

                count += 1

        with open('src/gem.txt', 'a') as f:  # дозаписать N = M с единсвенной точкой
            f.write('1\t-0.09758\t40\n')
            # f.write('1\t{E_last_val}\t{N}\n')

        full_gem = pd.read_csv("src/gem.txt", names=['g', 'E', 'M'], sep='\t')  # отзеркалить график
        full_gem = full_gem.loc[full_gem['M'] != 0]
        full_gem = full_gem.iloc[::-1]

        full_g = full_gem['g'].to_list()
        full_E = full_gem['E'].to_list()
        full_M = full_gem['M'].to_list()

        with open('src/gem.txt', 'a') as f:
            for i in range(0, len(full_E)):
                f.write(f'{full_g[i]}\t{full_E[i]}\t{-full_M[i]}\n')
        del full_gem, full_g, full_E, full_M

        print(f'gem для {N} частиц посчитан')
        print(f'Потребовалось: {round(time.time() - start_time, 2)} сек')
