
def table(names, lista):
    if len(lista) != 0:
        ncols = len(lista[0])
        nrows = len(lista)
        mat = []
        for i in range(ncols):
            mat.append([])
            for j in range(nrows):
                mat[i].append(str(lista[j][i]))
        lens = []
        for i in range(ncols):
            lens.append(max(len(max(mat[i], key=len)), len(names[i])))

        for i in range(ncols):
            print('+' + (lens[i]+2)*'-', end='')
        print('+')

        for i in range(ncols):
            print('| %s ' % (names[i] + (lens[i]-len(names[i]))*' '), end='')
        print('|')

        for i in range(ncols):
            print('+' + (lens[i]+2)*'-', end='')
        print('+')

        for i in range(nrows):
            for j in range(ncols):
                print('| %s ' % (mat[j][i] + (lens[j]-len(mat[j][i]))*' '), end='')
            print('|')

        for i in range(ncols):
            print('+' + (lens[i]+2)*'-', end='')
        print('+')
    else:
        print('Tabela Vazia!')
