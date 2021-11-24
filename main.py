from mysql.connector import Error, connect
from mysql.connector.connection import MySQLConnection
from table import table
from getpass import getpass

def safe_input(prompt, good_vals):
    qnt = None
    while qnt not in good_vals:
        try:
            qnt = int(input(prompt))
        except:
            print('Erro na entrada')
    return qnt


server = MySQLConnection()

good = False
while not good:
    usr = input("Nome de usuario: ")
    pwd = getpass("Senha: ")
    try:
        server.connect( # Conectar ao servidor
            host = 'financeiro-aero.mysql.uhserver.com',
            port = '3306',
            user = usr,
            password = pwd,
            database = 'financeiro_aero'
        )
        good = True
    except:
        print("Erro na conexão!")
        good = False

cursor = server.cursor()

while True:

    ## Menu
    print('1 - Ver Inventario')
    print('2 - Modificar Inventario')
    print('3 - Adicionar item')
    print('4 - Adicionar local')
    print('5 - Ver Log')
    print('6 - Sair')
    opt = safe_input('Escolher opcao: ', [1, 2, 3, 4, 5, 6])
    if opt == 1: # Ver inventário
        try:
            cursor.execute("select Itens.Nome, Locais.Nome, Inventario.Qnt, Inventario.UltimoMov from Inventario join Itens on Itens.ID = Inventario.ItemID join Locais on Locais.ID = Inventario.LocalID")
            table(['Item', 'Local', 'Quantidade', 'Ult. Mov.'], cursor.fetchall())
        except Error as e:
            print(e)
    if opt == 2: # Modificar Inventario
        print('1 - Mover Itens')
        print('2 - Adicionar Itens')
        print('3 - Remover Itens')
        print('4 - Voltar')
        opt1 = safe_input('Escolher opcao: ', [1, 2, 3, 4])
        if opt1 == 1: # Mover itens do inventario
            try:
                cursor.execute("select Inventario.ID, Itens.Nome, Locais.Nome, Inventario.Qnt, Inventario.UltimoMov from Inventario join Itens on Itens.ID = Inventario.ItemID join Locais on Locais.ID = Inventario.LocalID")
                itens = cursor.fetchall()
                table(['ID', 'Local', 'Item', 'Quantidade', 'Ult. Mov.'], itens)
                origemID = safe_input('Escolher origem: ', [ent[0] for ent in itens])

                # Coletar dados da entrada de origem
                cursor.execute("select ID, ItemID, Qnt, LocalID from Inventario")
                entradas = cursor.fetchall()
                origem = [entrada for entrada in entradas if entrada[0] == int(origemID)][0]

                cursor.execute("select ID, Nome from Locais")
                locais = cursor.fetchall()
                table(['ID', 'Nome'], [local for local in locais if local[0] != origem[3]])
                localID = safe_input('Escolher local final (ID): ', [ent[0] for ent in locais])

                qnt = safe_input('Escolher quantidade a mover (<= %d): ' % origem[2], range(origem[2] + 1))

                # Se já existe entrada do item no local, atualizar, se não, criar entrada
                novo = True
                for entrada in entradas:
                    if localID == entrada[3]:
                        if origem[1] == entrada[1]:
                            cursor.execute('update Inventario set Qnt = %d where ID = %d' % (entrada[2] + qnt, entrada[0]))
                            novo = False
                if novo:
                    cursor.execute('insert into Inventario(LocalID, ItemID, Qnt, UltimoMov) values (%d, %d, %d, NOW())' % (localID, origem[1], qnt))
                
                # Se a quantidade de itens final da entrada for nula, deletar, se não, atualizar
                if origem[2] != qnt:
                    cursor.execute('update Inventario set Qnt = %d where ID = %d' % (origem[2] - qnt, origem[0]))
                else:
                    cursor.execute('delete from Inventario where ID = %d' % origem[0])
                
                # Atualizar Log
                cursor.execute('insert into Log(LocalID, ItemID, Delta, Quando) values(%d, %d, %d, NOW())' % (  localID, origem[1],  qnt))
                cursor.execute('insert into Log(LocalID, ItemID, Delta, Quando) values(%d, %d, %d, NOW())' % (origem[3], origem[1], -qnt))
                server.commit()
                print("Sucesso!")
            except Error as e:
                print(e)

        if opt1 == 2: # Adicionar itens
            try:
                cursor.execute("select ID, ItemID, Qnt, LocalID from Inventario")
                entradas = cursor.fetchall()

                cursor.execute("select ID, Nome from Itens")
                itens = cursor.fetchall()
                table(['ID', 'Nome'], itens)
                itemID = safe_input('Escolher item: ', [end[0] for end in itens])

                cursor.execute("select ID, Nome from Locais")
                locais = cursor.fetchall()
                table(['ID', 'Nome'], locais)
                localID = safe_input('Escolher item: ', [end[0] for end in locais])

                print('Quantidade: ', end='')
                qnt = int(input())
                
                # Se já existe entrada do item no local, atualizar, se não, criar entrada
                novo = True
                for entrada in entradas:
                    if localID == entrada[3]:
                        if itemID == entrada[1]:
                            cursor.execute('update Inventario set Qnt = %d where ID = %d' % (entrada[2] + qnt, entrada[0]))
                            novo = False
                if novo:
                    cursor.execute('insert into Inventario(LocalID, ItemID, Qnt, UltimoMov) values (%d, %d, %d, NOW())' % (localID, itemID, qnt))
                
                # Atualizar Log
                cursor.execute('insert into Log(LocalID, ItemID, Delta, Quando) values(%d, %d, %d, NOW())' % (localID, itemID, qnt))
                server.commit()
                print("Sucesso!")
            except Error as e:
                print(e)

        if opt1 == 3: # Remover itens
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
                
                # Se a quantidade de itens final da entrada for nula, deletar, se não, atualizar
                if origem[2] != qnt:
                    cursor.execute('update Inventario set Qnt = %d where ID = %d' % (origem[2] - qnt, origem[0]))
                else:
                    cursor.execute('delete from Inventario where ID = %d' % origem[0])
                
                # Atualizar Log
                cursor.execute('insert into Log(LocalID, ItemID, Delta, Quando) values(%d, %d, %d, NOW())' % (origem[3], origem[1], -qnt))
                server.commit()
                print("Sucesso!")
            except Error as e:
                print(e)
            
    if opt == 3: # Adicionar item
        try:
            print('Nome do item: ', end='')
            nome = input()
            cursor.execute('insert into Itens(Nome) values("%s")' % nome)
            server.commit()
            print('Sucesso!')
        except Error as e:
            print(e)

    if opt == 4: # Adicionar local
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

    if opt == 5: # Ver Log
        cursor.execute('select Locais.Nome, Itens.Nome, Log.Delta, Log.Quando from Log join Locais on Locais.ID = Log.LocalID join Itens on Itens.ID = Log.ItemID')
        table(['Local', 'Item', 'Delta', 'Quando'], cursor.fetchall())

    if opt == 6: # Sair
        break
