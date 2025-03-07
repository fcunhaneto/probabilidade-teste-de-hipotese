import pandas as pd
import numpy as np


def quant(dataframe, coluna: str, amplitude: float, vmin=None, vmax=None):
    """

    :param dataframe: pandas dataframe
    :param coluna: nome da coluna
    :param amplitude: distancia entre as classes
    :param vmin: valor minimo
    :param vmax: valor máximo
    :return: pandas dataframe
    """

    if vmin is None:
        limite_vmin = np.floor(dataframe[coluna].min())
    else:
        limite_vmin = vmin

    if vmax is None:
        limite_vmax = np.ceil(dataframe[coluna].max())
    else:
        limite_vmax = vmax

    classes = []
    classes_str = []
    limite_inferior = limite_vmin

    while limite_inferior <= limite_vmax:
        classes.append([limite_inferior, limite_inferior + amplitude])

        if amplitude == 1:
            classes_str.append(limite_inferior)
        else:
            classes_str.append(f'[{limite_inferior: .2f}, {limite_inferior + amplitude: .2f})', )


        limite_inferior = limite_inferior + amplitude

    total = dataframe[coluna].count()
    valores_classes = []
    valores_frequencia = []
    valores_frequencia_acumulada = []
    acumulado = 0
    i = 0
    for c in classes:

        filtro = dataframe[coluna].loc[(dataframe[coluna] >= c[0]) & (dataframe[coluna] < c[1])]
        total_classe = filtro.count()

        valores_classes.append(total_classe)
        valores_frequencia.append(total_classe/total)
        acumulado = acumulado + filtro.count()

        if valores_classes[i] != 0:
            valores_frequencia_acumulada.append(acumulado/total)
        else:
            # print('Entrou')
            valores_frequencia_acumulada.append(0)

        i = i + 1

    tabela = pd.DataFrame({coluna: classes_str, 'ni': valores_classes, 'fi': valores_frequencia, 'fi.ac': valores_frequencia_acumulada})

    return tabela


def qual(dataframe, coluna: str):
    """

    :param dataframe: pandas dataframe
    :param coluna: nome da coluna
    :return: pandas dataframe
    """

    x = dataframe[coluna].to_numpy()
    y, t = np.unique(x, return_counts=True)
    tabela = pd.DataFrame({coluna: y, 'ni': t})

    tabela['fi'] = tabela['ni'] / tabela['ni'].sum()
    tabela['fi'] = tabela['fi'].round(2)

    return tabela


if __name__ == '__main__':
    df = pd.read_csv('data/questionario.csv')
    print(df.head(), '\n\n')

    frq = quant(df, 'Alt', 0.05, 1.45, 1.85)
    print(frq, '\n\n')

    frq = qual(df, 'Tole')
    print(frq, '\n\n')

    frq = quant(df, 'Idade', 1)
    print(frq, '\n\n')
