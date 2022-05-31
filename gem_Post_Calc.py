import pandas as pd
pd.set_option('mode.chained_assignment', None)

from sys import exit as sys_exit

'''
    Пост операции с gem для низкоэнергетических зон
'''

# найти верхунюю и нижнюю границы стабильности *
# провести прямую линию
# посчиать теплоемкость


class gemPost:
    def __init__(self, src_file='src/gem.txt'):
        df = pd.read_csv(src_file, names=['g', 'E', 'M'], sep='\t')     # скачать gem, чтобы рисовать поверх
        self.__df = df
        self.__borders = {}

        M_lst = df['M'].unique()        # все уникальные m
        self.__M_lst = M_lst

        for m in M_lst[:]:
            df_m = df.query(f'M == {m}').reset_index(drop=True)
            stable_lst = [0, ]

            for i in range(1, len(df_m['g'][:-1])):                 # расчет стабильных и нестабильных зон
                if df_m['g'][i - 1] == 0 or df_m['g'][i + 1] == 0:
                    # print(f'{i}: {df_m["E"][i - 1]} - unstable')
                    stable_lst.append(0)
                else:
                    # print(f'{i}: {df_m["E"][i - 1]} - stable')
                    stable_lst.append(1)

            stable_lst.append(0)
            df_m['is_stable'] = stable_lst
            del stable_lst

            step = 10               # сколько интервалов в одной зоне
            self.__step = step

            zone_lst = []
            cur_zone = 0
            for i in range(len(df_m['E'])):
                if i % step == 0:
                    cur_zone += 1
                zone_lst.append(cur_zone)

            df_m['zone'] = zone_lst
            del zone_lst
            del cur_zone

            is_zone_stable_lst = []
            for z in df_m['zone'].unique():
                if sum(df_m.query(f'zone == {z}')['is_stable'].tolist()) < step - 4:       # если большенство g в зоне
                    is_zone_stable_lst.append(0)                                           # рандомятся нормально
                else:                                                                      # зона "безопасная"
                    is_zone_stable_lst.append(1)

            self.__zone_col_size = len(is_zone_stable_lst)

            defined_as_borders = []

            for i in range(4, len(is_zone_stable_lst) - 4):
                is_border, diff_val_count = False, 0
                for j in range(i - 1, i + 1):
                    if is_zone_stable_lst[i] != is_zone_stable_lst[j]:
                        diff_val_count += 1
                if diff_val_count != 0:
                    is_border = True
                    defined_as_borders.append(i)
                # print(f'{i} => {is_zone_stable_lst[i]} => {is_border}')

            # print(is_zone_stable_lst)
            # print(defined_as_borders)

            top_v, bot_v = [], []
            for val in defined_as_borders:
                if val <= int(len(is_zone_stable_lst) / 2):
                    top_v.append(val)
                else:
                    bot_v.append(val)
            del defined_as_borders

            ret_zero = False        # если заходим в зоны, где и так все прекрасно рандомится
            top_border, bot_border = 0, 0                       # то заканчивает наш цырк

            try:
                top_border = max(top_v) + 1
                bot_border = min(bot_v) - 1
            except ValueError:
                ret_zero = True

            if not ret_zero:
                self.__borders[m] = (top_border, bot_border)  # упаковываем
            else:
                tmp_lst = []
                for key in self.__borders:
                    tmp_lst.append(key)
                for key in tmp_lst[::-1]:
                    if key != 0:
                        self.__borders[-key] = self.__borders[key]
                break
            # границы найдены

            # print(f'm = {m}\t\t{top_border}\t{bot_border}', end='\n\n')

            pass

    def fix_low_E_zone(self):                           # рисуем поверх пустых низкоэнергетических зон свой курс рубля
        final_m_changed = []
        f = open('src/gem.txt', 'w')
        ind = 0
        Nm_dict = {}

        with open('src/k.txt', 'r') as fk:              # скачиваем Nm для расчета новых g после исправления низкоэн зон
            for line in fk:
                try:
                    Nm_dict[ind] = int(line.replace('\n', ''))
                except:
                    sys_exit('Ну и фикси теперь')
                ind += 2

        for m, bord in self.__borders.items():
            df_m = self.__df.query(f'M == {m}').reset_index(drop=True)
            df_m.is_copy = False

            # print(f'{0}\t{bord[0] * self.__step}')
            # print(f'{len(df_m["E"].tolist()) - 1}\t{bord[1] * self.__step + self.__step - 1}')

            top_ind = bord[0] * self.__step
            bot_ind = bord[1] * self.__step + self.__step - 1       # много кода

            if df_m["g"][top_ind] == 0:
                while df_m["g"][top_ind] == 0:
                    top_ind -= 1

            if df_m["g"][bot_ind] == 0:
                while df_m["g"][bot_ind] == 0:
                    bot_ind += 1

            # снова обрезаем незначительную область близко к M
            if df_m["g"][top_ind] < 100 or df_m["g"][bot_ind] < 100:
                pass
            else:
                # df_m["E"][len(df_m["E"].tolist()) - 1]
                g_top = df_m["g"][top_ind]
                g_bot = df_m["g"][bot_ind]

                split_top = top_ind
                split_bot = (len(df_m["E"].tolist()) - 1) - bot_ind

                step_val_top = (g_top - 2) / split_top
                step_val_bot = (g_bot - 2) / split_bot

                df_m['g'][0] = 2
                for i in range(1, top_ind):
                    df_m['g'][i] = int(2 + i * step_val_top)
                    # print(f'{int(2 + i * step_val_top)}, ', end='')
                # print()

                df_m['g'][len(df_m["E"].tolist()) - 1] = 2
                for i in range(bot_ind, len(df_m["E"].tolist()) - 1):
                    back_ind = len(df_m["E"].tolist()) - i
                    df_m['g'][i] = int(2 + back_ind * step_val_top)
                    # print(f'{int(2 + back_ind * step_val_bot)}, ', end='')
                # print()

                # print(f'2\t{g_top}\t({split_top}) => {int(step_val_top)}')
                # print(f'2\t{g_bot}\t({split_bot}) => {int(step_val_bot)}')
                #
                # print(f'm={m}\tb={bord}', end="\n\n")

                # изменить площадь под графиком, чтобы она была равна биномиальному коэф (S = Nm)
                k = Nm_dict[abs(m)] / df_m['g'].sum()
                for i in range(len(df_m['g'].tolist())):
                    df_m['g'] *= k

                # print(f'm={m} => {k}')

                for index, row in df_m.iterrows():      # вывести/сохранить в файл gem
                    f.write(f'{int(row["g"])}\t{round(row["E"], 5)}\t{int(row["M"])}\n')
                final_m_changed.append(m)     # сохранить, какие m изменились

        for m in self.__M_lst:
            if m not in final_m_changed:
                for index, row in self.__df.query(f'M == {m}').iterrows():
                    f.write(f'{int(row["g"])}\t{round(row["E"], 5)}\t{int(row["M"])}\n')
        f.close()

    @property
    def borders(self):
        return self.__borders


post = gemPost()
post.fix_low_E_zone()