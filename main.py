import mysql.connector
from mysql.connector import Error

## Coisas a adicionar:
# Remover Itens
# Quantidades

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
    host = 'sql10.freemysqlhosting.net',
    port = '3306',
    user = 'sql10393418',
    password = 'BJwg6iCman',
    database = 'sql10393418'
)

cursor = server.cursor()

while True:
    print('1 - Ver Inventario')
    print('2 - Modificar Inventario')
    print('3 - Adicionar item')
    print('4 - Adicionar local')
    print('5 - Ver Log')
    print('6 - Sair')
    print('Escolha: ', end='')
    opt = input()
    if opt == '1':
        try:
            cursor.execute("select Itens.Nome, Locais.Nome, Inventario.Qnt, Inventario.UltimoMov from Inventario join Itens on Itens.ID = Inventario.ItemID join Locais on Locais.ID = Inventario.LocalID")
            table(['Item', 'Local', 'Quantidade', 'Ult. Mov.'], cursor.fetchall())
        except Error as e:
            print(e)
    if opt == '2': # Modificar Inventario
        print('1 - Mover Itens')
        print('2 - Adicionar Itens')
        print('3 - Remover Itens')
        print('Escolher opcao: ', end = '')
        opt1 = input()
        if opt1 == '1':
            try:
                cursor.execute("select Inventario.ID, Itens.Nome, Locais.Nome, Inventario.Qnt, Inventario.UltimoMov from Inventario join Itens on Itens.ID = Inventario.ItemID join Locais on Locais.ID = Inventario.LocalID")
                table(['ID', 'Local', 'Item', 'Quantidade', 'Ult. Mov.'], cursor.fetchall())
                print('Escolher origem: ', end = '')
                origemID = input()

                cursor.execute("select ID, ItemID, Qnt, LocalID from Inventario")
                entradas = cursor.fetchall()
                origem = [entrada for entrada in entradas if entrada[0] == int(origemID)][0]

                cursor.execute("select ID, Nome from Locais")
                table(['ID', 'Nome'], [local for local in cursor.fetchall() if local[0] != origem[3]])
                print('Escolher local final (ID): ', end='')
                localID = int(input())
                print('Escolher quantidade a mover (<= %d): ' % origem[2], end = '')
                qnt = int(input())
                novo = True
                for entrada in entradas:
                    if localID == entrada[3]:
                        if origem[1] == entrada[1]:
                            cursor.execute('update Inventario set Qnt = %d where ID = %d' % (entrada[2] + qnt, entrada[0]))
                            novo = False
                if novo:
                    cursor.execute('insert into Inventario(LocalID, ItemID, Qnt, UltimoMov) values (%d, %d, %d, NOW())' % (localID, origem[1], qnt))
                if origem[2] != qnt:
                    cursor.execute('update Inventario set Qnt = %d where ID = %d' % (origem[2] - qnt, origem[0]))
                else:
                    cursor.execute('delete from Inventario where ID = %d' % origem[0])
                
                cursor.execute('insert into Log(LocalID, ItemID, Delta, Quando) values(%d, %d, %d, NOW())' % (  localID, origem[1],  qnt))
                cursor.execute('insert into Log(LocalID, ItemID, Delta, Quando) values(%d, %d, %d, NOW())' % (origem[3], origem[1], -qnt))
                server.commit()
                print("Sucesso!")
            except Error as e:
                print(e)
        if opt1 == '2':
            try:
                cursor.execute("select ID, ItemID, Qnt, LocalID from Inventario")
                entradas = cursor.fetchall()

                cursor.execute("select ID, Nome from Itens")
                table(['ID', 'Nome'], cursor.fetchall())
                print('Escolher item: ', end='')
                itemID = int(input())

                cursor.execute("select ID, Nome from Locais")
                table(['ID', 'Nome'], cursor.fetchall())
                print('Escolher local: ', end='')
                localID = int(input())

                print('Quantidade: ', end='')
                qnt = int(input())

                novo = True
                for entrada in entradas:
                    if localID == entrada[3]:
                        if itemID == entrada[1]:
                            cursor.execute('update Inventario set Qnt = %d where ID = %d' % (entrada[2] + qnt, entrada[0]))
                            novo = False
                if novo:
                    cursor.execute('insert into Inventario(LocalID, ItemID, Qnt, UltimoMov) values (%d, %d, %d, NOW())' % (localID, itemID, qnt))
                
                cursor.execute('insert into Log(LocalID, ItemID, Delta, Quando) values(%d, %d, %d, NOW())' % (localID, itemID, qnt))
                server.commit()
                print("Sucesso!")
            except Error as e:
                print(e)
        if opt1 == '3':
            try:
                cursor.execute("select Inventario.ID, Itens.Nome, Locais.Nome, Inventario.Qnt, Inventario.UltimoMov from Inventario join Itens on Itens.ID = Inventario.ItemID join Locais on Locais.ID = Inventario.LocalID")
                table(['ID', 'Local', 'Item', 'Quantidade', 'Ult. Mov.'], cursor.fetchall())
                print('Escolher origem: ', end = '')
                origemID = input()

                cursor.execute("select ID, ItemID, Qnt, LocalID from Inventario")
                entradas = cursor.fetchall()
                origem = [entrada for entrada in entradas if entrada[0] == int(origemID)][0]

                print("Quantidade a remover (< %d): " % origem[2])
                qnt = int(input())
                
                if origem[2] != qnt:
                    cursor.execute('update Inventario set Qnt = %d where ID = %d' % (origem[2] - qnt, origem[0]))
                else:
                    cursor.execute('delete from Inventario where ID = %d' % origem[0])
                cursor.execute('insert into Log(LocalID, ItemID, Delta, Quando) values(%d, %d, %d, NOW())' % (origem[3], origem[1], -qnt))
                server.commit()
                print("Sucesso!")
            except Error as e:
                print(e)

            
    if opt == '3': # Adicionar item
        try:
            print('Nome do item: ', end='')
            nome = input()
            cursor.execute('insert into Itens(Nome) values("%s")' % nome)
            server.commit()
            print('Sucesso!')
        except Error as e:
            print(e)
    if opt == '4': # Adicionar local
        try:
            print('Nome do local: ', end='')
            nome = input()
            print('Endereco: ', end='')
            endereco = input()
            cursor.execute('insert into Locais(Nome, Endereco) values("%s", "%s")' % (nome, endereco))
            server.commit()
            print('Sucesso!')
        except Error as e:
            print(e)
    if opt == '5': # Ver Log
        cursor.execute('select Locais.Nome, Itens.Nome, Log.Delta, Log.Quando from Log join Locais on Locais.ID = Log.LocalID join Itens on Itens.ID = Log.ItemID')
        table(['Local', 'Item', 'Delta', 'Quando'], cursor.fetchall())
    if opt == '6': # Sair
        break
