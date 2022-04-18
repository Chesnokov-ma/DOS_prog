from math import factorial


def Nm_generate(N, f):  # вручную сгенерировать список Nm
    Nm = []; m = 20
    for _ in range(int(N / 2)):
        tmp = (factorial(N) / (factorial(m) * factorial(N - m)))
        print(f'M = {m}; Nm = {tmp}')
        f.write(f'{int(tmp)}\n')
        Nm.append(tmp)
        m += 1
    del N, m
    return Nm
