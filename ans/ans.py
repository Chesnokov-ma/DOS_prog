import pandas as pd
pd.set_option('mode.chained_assignment', None)


df = pd.read_csv('../src/gem_t_int.txt', names=['g', 'E', 'M'], sep='\t')

M_lst = [0]

for m in M_lst:
    df_m = df.query(f'M == {m}').reset_index(drop=True)
    dif_lst = [0]

    for i in range(1, len(df_m['g'].tolist())):
        if df_m['g'][i] == 0 or df_m['g'][i - 1] == 0:
            dif_lst.append(0)
        else:
            if df_m['g'][i] > df_m['g'][i - 1]:
                dif_lst.append(df_m['g'][i] / df_m['g'][i - 1])
            elif df_m['g'][i] < df_m['g'][i - 1]:
                dif_lst.append(df_m['g'][i - 1] / df_m['g'][i])
            else:
                dif_lst.append(1)

    df_m['dif'] = dif_lst
    df_m.to_csv()



pass