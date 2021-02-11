import mysql.connector
from mysql.connector import Error

def table(names, lista):
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

server = mysql.connector.connect(
    host = 'localhost',
    user = 'rubem',
    password = '123',
    database = 'inventario'
)

cursor = server.cursor()

while True:
    print('1 - Ver itens')
    print('2 - Mover item')
    print('3 - Adicionar item')
    print('4 - Adicionar local')
    print('5 - Sair')
    print('Escolha: ', end='')
    opt = input()
    if opt == '1':
        try:
            cursor.execute("select Itens.Nome, Locais.Nome, Itens.UltimoMov from Locais join Itens on Itens.LocalID = Locais.ID")
            table(['Item', 'Local', 'Ultimo Mov.'], cursor.fetchall())
        except Error as e:
            print(e)
    if opt == '2': # Mover item
        itens = []
        locais = []
        try:
            cursor.execute("select Itens.ID, Itens.Nome, Locais.Nome from Itens join Locais on Itens.LocalID = Locais.ID")
            itens = cursor.fetchall()
            cursor.execute("select ID, Nome from Locais")
            locais = cursor.fetchall()
        except Error as e:
            print(e)
        finally:
            table(['ID', 'Nome', 'Loc. Atual'], itens)
            ids = []
            for item in itens:
                ids.append(item[0])
            idItem = 0
            while idItem not in ids:
                print('Escolher item: ', end = '')
                try:
                    idItem = int(input())
                except:
                    print('Valor invalido')
            
            table(['ID', 'Nome'], locais)
            ids = []
            for local in locais:
                ids.append(local[0])
            idLocal = 0
            while idLocal not in ids:
                print('Escolher local: ', end = '')
                try:
                    idLocal = int(input())
                except:
                    print('Valor invalido')
            try:
                cursor.execute('update Itens set LocalID = %d, UltimoMov = NOW() where ID = %d' % (idLocal, idItem))
                server.commit()
                print('Sucesso!')
            except Error as e:
                print(e)
            
    if opt == '3': # Adicionar item
        try:
            print('Nome do item: ', end='')
            nome = input()
            cursor.execute("select ID, Nome from Locais")
            print('ID\tNome')
            ids = []
            for local in cursor.fetchall():
                print('%d\t%s' % (local[0], local[1]))
                ids.append(local[0])
            idLocal = 0
            while idLocal not in ids:
                print('Escolher local: ', end = '')
                try:
                    idLocal = int(input())
                except:
                    print('Valor invalido')
            cursor.execute('insert into Itens(Nome, UltimoMov, LocalID) values("%s", NOW(), %d)' %(nome, idLocal))
            server.commit()
            print('Sucesso!')
        except Error as e:
            print(e)
    if opt == '4': # Adicionar local
        print("Nao implementado")
    if opt == '5': # Sair
        break
