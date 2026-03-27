
import util as u

import mysql.connector
import datetime

debug = True
conexao = ''
if debug:
    conexao = mysql.connector.connect(host='localhost', database='tkd', user="root", password='')
else:
    conexao = mysql.connector.connect(host='localhost', database='tk', user="root", password='')
cursor = ''

if(conexao.is_connected):
    print('conexão bem sucedida')
    cursor = conexao.cursor(dictionary=True)

def criar_ciclo():# cria um ciclo
    ciclo = {}
    r = input("Digite o nome do ciclo: ")
    ciclo['nome'] = r
    r = input("Desejar digitar o tempo em decimal ou hh:mm:ss :[d][h]\nR: ")
    if r == 'd':
        hora = float(input("Digite a hora a ser mostrada: "))
        ciclo['tempo total'] = u.objetoHorasParaStringHoras(u.horaParaHorasBonita(hora))
        ciclo['tempo total decimal'] = hora
    elif r == 'h':
        hora = u.criarHora()
        ciclo['tempo total'] = u.objetoHorasParaStringHoras(hora)
        ciclo['tempo total decimal'] = u.lessDecimalBadHour(u.converteParaDecimalFeio(hora),hora)
    else:
        print('digite uma entrada valida')
    print(ciclo)
    insert = f"INSERT INTO ciclo(nome, tempoTotal, tempoTotalDecimal) values('{ciclo['nome']}', '{ciclo['tempo total']}', '{ciclo['tempo total decimal']}')"
    print(insert)
    cursor.execute(insert)
    conexao.commit()

def criar_atividade():# cria uma atividade
    atividade = {}
    r = input('Digite o nome da atividade: ')
    atividade['Nome'] = r
    insert = f"INSERT INTO atividade(nome) VALUES ('{atividade['Nome']}')"
    cursor.execute(insert)
    conexao.commit()

def listAny(table, complement='', fields='*'):# cria uma lista em base numa consulta select
    select = f'SELECT {fields} FROM {table} {complement};'
    #print(select)
    result = cursor.execute(select)
    lista = cursor.fetchall()

    for i in lista:
        for key in i.keys():
            if(key == 'tempoTotal'):
                i[key] = u.objetoHorasParaStringHoras(u.horaParaHorasBonita(i['tempoTotalDecimal']))

    return lista

def adicionarAtividadeACiclo(ciclo):#relaciona um atividade com um ciclo(cadastra ela no ciclo)
    #vc pode adicionar a mesma atividade num ciclo n vezes isso é um problema
    list = listAny('atividade')
    print(imprimirMenu(list))
    r = input('teste')
    insert = f"INSERT INTO ciclo_atividade(codigoAtividade, codigoCiclo, gp, porcentagemTempoTotal) VALUES ({list[int(r)]['codigo']}, {ciclo['codigo']}, 'na', 0)"
    cursor.execute(insert)
    conexao.commit()

def apagarAtividadeCiclo(ciclo):#apaga uma atividade de um ciclo
    #vc pode adicionar a mesma atividade num ciclo n vezes isso é um problema
    list = listAny('ciclo_atividade', complement=f"INNER JOIN atividade on codigoAtividade=atividade.codigo where codigoCiclo = {ciclo['codigo']}", 
    fields='ciclo_atividade.codigo, codigoAtividade, atividade.nome, gp, porcentagemTempoTotal')
    print(imprimirMenu(list))
    r = input('escolha qual apagar: ')
    delete = f"DELETE FROM ciclo_atividade WHERE codigo={list[int(r)]['codigo']}"
    cursor.execute(delete)
    conexao.commit()

def selectItens(itens):#faz multi-seleção de itens de uma lista
    choosed = []
    choosing = True
    while choosing:
        showList(choosed)
        r = input('[1] - adicionar item\n[2] - remover item\n[3] - terminar seleção\nR: ')
        if r=='1':
            print(imprimirMenu(itens))
            r = input('R: ')
            choosed.append(itens[int(r)])
            del itens[int(r)]
        elif r=='2':
            if len(choosed) > 0:
                print(imprimirMenu(choosed))
                r=input('R: ')
                itens.append(choosed[int(r)])
                del choosed[int(r)]
        elif r=='3':
            return {'choosed': choosed,'unchoosed': itens}

def putNewPor(escolhido):#coloca novas porcentagens em mais de um item
    certo = True
    sum1 = 0
    for i in escolhido['unchoosed']:
        sum1 += i['porcentagemTempoTotal']

    while certo:
        print(imprimirMenu(escolhido['choosed']))
        r = input('digite os novos valores separados por ;: ')
        values = r.split(';')
        if len(values) != len(escolhido['choosed']):
            return 'erro'
        sum2 = 0
        for i,item in enumerate(escolhido['choosed']):
            item['porcentagemTempoTotal'] = float(values[i])
            sum2 += item['porcentagemTempoTotal']
        print(sum1 + sum2)
        if(sum1 + sum2 <= 1.00):
            certo = False
            return escolhido['choosed']
        showList(escolhido['choosed'])

def newGp(escolhido):# coloca gp em mais de um itens
    print(imprimirMenu(escolhido['choosed']))
    r = input('digite os novos valores separados por ;: ')
    values = r.split(';')
    if len(values) != len(escolhido['choosed']):
        return 'erro'
    for i,item in enumerate(escolhido['choosed']):
        item['gp'] = values[i]
    return escolhido['choosed']

def mudarGp(ciclo):#mudar gp de atividade em um ciclo
    list = listAny('ciclo_atividade',complement=f'INNER JOIN atividade on codigoAtividade=atividade.codigo where codigoCiclo={ciclo['codigo']}',fields='ciclo_atividade.codigo, codigoAtividade, atividade.nome, gp, porcentagemTempoTotal')
    escolhidos = selectItens(list)
    toUpdate = newGp(escolhidos)
    for i in toUpdate:
        update = f"update ciclo_atividade SET gp = '{i['gp']}' where codigo={i['codigo']}"
        print(update)
        cursor.execute(update)

    conexao.commit()

def mudarPorcentagem(ciclo):#mudar porcentagens em um ciclo
    list = listAny('ciclo_atividade',complement=f'INNER JOIN atividade on codigoAtividade=atividade.codigo where codigoCiclo={ciclo['codigo']}',fields='ciclo_atividade.codigo, codigoAtividade, atividade.nome, gp, porcentagemTempoTotal')
    escolhidos = selectItens(list)
    toUpdate = putNewPor(escolhidos)
    for i in toUpdate:
        update = f"update ciclo_atividade SET porcentagemTempoTotal = {i['porcentagemTempoTotal']} where codigo={i['codigo']}"
        cursor.execute(update)

    conexao.commit()


def iniciarSessao(ciclo, listAtividade):
    #checar se não tem uma sessão com status executando
    sessoes = listAny('sessao', complement=f"where status='executando'")
    novaSessao = {}
    novaSessao['status'] = 'executando'
    if len(sessoes) > 0:
        r = input('Já existe uma sessão em execução,1=deseja criar mesmo assim em pausa ou 2=não criar[1][2]:')
        if r == '1':
            novaSessao['status'] = 'pausada'
        elif r == '2':
            return
    
    novaSessao['nome'] = input('Escreva o nome da sessão: ')
    sessoes = listAny('sessao', complement=f"where status='finalizada' and codigoCiclo={ciclo['codigo']} order by fimData desc limit 1")
    showList(sessoes)
    insert = ''
    if len(sessoes) <= 0:
    #fazer o insert
        insert = f"INSERT INTO sessao(codigoCiclo, nome, nome_ciclo, status, inicioData, tempoTotal, tempoTotalDecimal, filled) VALUES ({ciclo['codigo']}, '{novaSessao['nome']}', '{ciclo['nome']}', '{novaSessao['status']}','{datetime.date.today()}', '{ciclo['tempoTotal']}', {ciclo['tempoTotalDecimal']}, 'unready')"
    else:
        insert = f"INSERT INTO sessao(codigoCiclo, nome, nome_ciclo, status, inicioData, tempoTotal, tempoTotalDecimal, filled, ultimaSessao) VALUES ({ciclo['codigo']}, '{novaSessao['nome']}', '{ciclo['nome']}', '{novaSessao['status']}','{datetime.date.today()}', '{ciclo['tempoTotal']}', {ciclo['tempoTotalDecimal']}, 'unready', {sessoes[0]['codigo']})"
    print(insert)
    cursor.execute(insert)
    conexao.commit()
    sessao = listAny('sessao',complement="where filled = 'unready'")[0]
    insertAtividades = 'INSERT INTO sessao_atividade(nomeAtividade, codigoAtividade, codigoSessao, tempoAFazer, tempoAFazerDecimal, porcentagemTempoTotal, gp) VALUES '
    for pos, i in enumerate(listAtividade):
        insertAtividades += f"('{i['nome']}', {i['codigoAtividade']}, {sessao['codigo']}, '{i['tempo a fazer']}', {i['tempo a fazer decimal']}, {i['porcentagemTempoTotal']}, '{i['gp']}')"
        if pos < len(listAtividade) - 1:
            insertAtividades += ',\n'
        else:
            insertAtividades += ';'
    update = f"UPDATE sessao SET filled = 'ready' where codigo={sessao['codigo']}"
    cursor.execute(insertAtividades)
    cursor.execute(update)
    conexao.commit()
    
    #fazer o registro representando o andiatamento só fazer isso se tiver sessao anterior
    if sessao['ultimaSessao'] is not None:
        registroAndiantado(sessao)
    #se tiver mandar a opção de não criar ou criar em status pausado
    #considerar ultima sessao uma sessao finalizada do mesmo ciclo

def registroAndiantado(sessao):
    #encontrar atividades que estão em ambas sessoes, verificar os ultimos registros de cada atividade, e caso tenha ultrapassado o tempo a fazer fazer um registro novo daquele dia
    listaAtividades = listAny('sessao_atividade', complement=f'WHERE codigoSessao={sessao['codigo']}')
    #showList(listaAtividades)
    for atividade in listaAtividades:
        atividadeSessaoAN = listAny('sessao_atividade', complement=f'inner join registro on registro.codigo = ultimoRegistro left join registro as ra on registro.codigoRA = ra.codigo inner join sessao on codigoSessao = sessao.codigo where codigoSessao = {sessao['ultimaSessao']} and codigoAtividade={atividade['codigoAtividade']}', fields='registro.nomeAtividade, registro.inicio, registro.fim, registro.data, registro.codigoRA, ultimoRegistro, ra.tempoAFazerD, sessao.tempoTotalDecimal, porcentagemTempoTotal')
        if(len(atividadeSessaoAN) > 0):
            registroNovo = {}
            atividade['tempoAFazer'] = u.horaParaHorasBonita(atividade['tempoAFazerdecimal'])
            atividadeSessaoAN = atividadeSessaoAN[0]
            if(atividadeSessaoAN['tempoAFazerD'] is None):
                atividadeSessaoAN['tempoAFazerD'] = atividadeSessaoAN['tempoTotalDecimal'] * atividadeSessaoAN['porcentagemTempoTotal']
            atividadeSessaoAN['inicio'] = u.formatHMS(atividadeSessaoAN['inicio'].total_seconds())
            atividadeSessaoAN['fim'] = u.formatHMS(atividadeSessaoAN['fim'].total_seconds())
            registroNovo['inicio'] = u.sumHoras(atividadeSessaoAN['inicio'], u.horaParaHorasBonita(atividadeSessaoAN['tempoAFazerD']))
            tempoDecorrido = u.diffHoras(u.stringHoraToObject(registroNovo['inicio']), atividadeSessaoAN['fim'])
            res = f'{atividadeSessaoAN['data']}\n{atividade['nomeAtividade']} - {u.lessDecimalBadHour(atividade['tempoAFazerdecimal'], atividade['tempoAFazer'])}\n'
            ultrapassou = ''
            if u.converteParaDecimalFeio(tempoDecorrido) >  atividade['tempoAFazerdecimal']:#verifica se foi feito tempo a mais do que se devia
                registroNovo['tempoAFazer'] = '00:00:00'
                registroNovo['tempoAFazerD'] = 0.0
                tempoUltrapassado = u.diffHoras(tempoDecorrido, atividade['tempoAFazer'])
                ultrapassou = f'\ntempo ultrapassado: {u.objetoHorasParaStringHoras(tempoUltrapassado)} - {u.lessDecimalBadHour(u.converteParaDecimalFeio(tempoUltrapassado), tempoUltrapassado)}'
            else:    
                registroNovo['tempoAFazer'] = u.diffHoras(tempoDecorrido, atividade['tempoAFazer'])
                registroNovo['tempoAFazerD'] = u.converteParaDecimalFeio(registroNovo['tempoAFazer'])
                registroNovo['tempoAFazer'] = u.objetoHorasParaStringHoras(registroNovo['tempoAFazer'])

            registroNovo['fim'] = u.objetoHorasParaStringHoras(atividadeSessaoAN['fim'])
            res += f'{registroNovo['inicio']}\n{registroNovo["fim"]}\ntempo decorrido: {u.objetoHorasParaStringHoras(tempoDecorrido)}\ntempo: {registroNovo["tempoAFazer"]} - {u.lessDecimalBadHour(registroNovo['tempoAFazerD'],u.stringHoraToObject(registroNovo["tempoAFazer"]))}{ultrapassou}'
            print(res)

            insert = f"insert into registro(codigoSessaoAtividade, inicio, fim, data, nomeAtividade, tempoAFazer, tempoAFazerD, codigoRAnd) VALUES ({atividade['codigo']}, '{registroNovo['inicio']}','{registroNovo['fim']}','{atividadeSessaoAN['data']}', '{atividade['nomeAtividade']}', '{registroNovo['tempoAFazer']}', {registroNovo['tempoAFazerD']}, {atividadeSessaoAN['ultimoRegistro']})"
            update = f"UPDATE sessao_atividade set tempoAFazer = '{registroNovo['tempoAFazer']}', tempoAFazerdecimal = {registroNovo['tempoAFazerD']} where codigo={atividade['codigo']}"
            cursor.execute(insert)
            cursor.execute(update)
            conexao.commit()
            ultimoRegistro = listAny('registro', fields='codigo', complement=f"where codigoSessaoAtividade = {atividade['codigo']} order by data desc, inicio desc limit 1")[0]
            update = f"UPDATE sessao_atividade set ultimoRegistro = '{ultimoRegistro['codigo']}' where codigo={atividade['codigo']}"
            cursor.execute(update)
            conexao.commit()
            if len(listAny('sessao_atividade',complement=f"where codigoSessao = {atividade['codigoSessao']} and tempoAFazerdecimal > 0")) <= 0:# verifica se a sessão finalizou
                print('sessão terminada')
                update = f"UPDATE sessao set status = 'finalizada', fimData = '{datetime.date.today()}' where codigo={atividade['codigoSessao']}"
                cursor.execute(update)
                conexao.commit()
                #tempo a fazer se ultimo registro for none deve ser o tempo total da atividade
                #verificar se a atividade tá completa

def gerenciar(ciclo):
    print(ciclo)
    gerenciando = True
    while gerenciando:

        listaAtividadesCiclo = listAny('ciclo_atividade',complement=f'INNER JOIN atividade on codigoAtividade=atividade.codigo where codigoCiclo={ciclo['codigo']}',fields='ciclo_atividade.codigo, codigoAtividade, atividade.nome, gp, porcentagemTempoTotal')
        for i in listaAtividadesCiclo:
            i['tempo a fazer decimal'] = ciclo['tempoTotalDecimal'] * i['porcentagemTempoTotal']
            i['tempo a fazer'] = u.objetoHorasParaStringHoras(u.horaParaHorasBonita(i['tempo a fazer decimal']))
        showList(listaAtividadesCiclo)
        r = input('[1] - adicionar atividade\n[2] - remover atividade\n[3] - mudar porcentagens\n[4] - mudar gp\n[5] - voltar menu\nwhat u wanna du nigaz: ')

        if r == '1':
            adicionarAtividadeACiclo(ciclo)
        elif r == '2':
            apagarAtividadeCiclo(ciclo)
        elif r == '3':
            mudarPorcentagem(ciclo)
        elif r=='4':
            mudarGp(ciclo)
        elif r == '5':
            iniciarSessao(ciclo, listaAtividadesCiclo)
        elif r == '6':
            gerenciando = False

def imprimirMenu(list):
    res = ''
    for i,line in enumerate(list):
        res += f'[{i}] - '
        for pos, key in enumerate(line):
            if pos == len(line.keys()) - 1:
                res += f'{key}: {line[key]}\n'
            else:
                res += f'{key}: {line[key]} - '
    return res
def gerenciarCiclo():
    #listar os ciclos
    list = listAny('Ciclo')
    res = imprimirMenu(list)
    print(res)
    #input pra escolher ciclo
    r = input('R: ')
    gerenciar(list[int(r)])
    #sistema menu de ciclo

def showList(list):
    for line in list:
        res = ''
        for pos, key in enumerate(line):
            if pos == len(line.keys()) - 1:
                res += f'{key}: {line[key]}'
            else:
                res += f'{key}: {line[key]} - '
        print(res)

def registrar(atividade):
    if atividade['tempoAFazerdecimal'] <= 0:#verifica se a atividade esta cumprida e sai para o menu anterior caso +
        print('atividade terminada')
        return
    
    registro = {}#criar um dicionário para armazenar as informações do registro
    print(atividade['tempoAFazerdecimal'])
    atividade['tempoAFazer'] = u.stringHoraToObject(atividade['tempoAFazer'])
    print(atividade)
    #pega os marcos temporais
    naoPronto = True
    while naoPronto:
        print("marco-1")
        registro['inicio'] = u.criarHora()
        print("marco-2")
        registro['fim'] = u.criarHora()
        #calcula o tempo decorrido entre os dois marcos
        tempoDecorrido = u.diffHoras(registro['inicio'], registro['fim'])
        res = f'{atividade['nomeAtividade']} - {u.lessDecimalBadHour(atividade['tempoAFazerdecimal'], atividade['tempoAFazer'])}\n'
        ultrapassou = ''
        if u.converteParaDecimalFeio(tempoDecorrido) >  atividade['tempoAFazerdecimal']:#verifica se foi feito tempo a mais do que se devia
            registro['tempoAFazer'] = '00:00:00'
            registro['tempoAFazerD'] = 0.0
            tempoUltrapassado = u.diffHoras(tempoDecorrido, atividade['tempoAFazer'])
            ultrapassou = f'\ntempo ultrapassado: {u.objetoHorasParaStringHoras(tempoUltrapassado)} - {u.lessDecimalBadHour(u.converteParaDecimalFeio(tempoUltrapassado), tempoUltrapassado)}'
        else:    
            registro['tempoAFazer'] = u.diffHoras(tempoDecorrido, atividade['tempoAFazer'])
            registro['tempoAFazerD'] = u.converteParaDecimalFeio(registro['tempoAFazer'])
            registro['tempoAFazer'] = u.objetoHorasParaStringHoras(registro['tempoAFazer'])

        registro['inicio'] = u.objetoHorasParaStringHoras(registro['inicio'])
        registro['fim'] = u.objetoHorasParaStringHoras(registro['fim'])
        print(registro)
        res += f'{registro['inicio']}\n{registro["fim"]}\ntempo decorrido: {u.objetoHorasParaStringHoras(tempoDecorrido)}\ntempo: {registro["tempoAFazer"]} - {u.lessDecimalBadHour(registro['tempoAFazerD'],u.stringHoraToObject(registro["tempoAFazer"]))}{ultrapassou}'
        print(res)
        print('[b] - back')
        r = input('confirmar novo registro[s][n]: ')
        if r == 'b':
            return
        if r == 's':
            naoPronto = False
    # inserção no banco
    if atividade['ultimoRegistro'] is not None:
        insert = f"INSERT INTO registro(codigoSessaoAtividade, inicio, fim, data, nomeAtividade, tempoAFazer, tempoAFazerD, codigoRA) VALUES ({atividade['codigo']}, '{registro['inicio']}','{registro['fim']}','{datetime.date.today()}', '{atividade['nomeAtividade']}', '{registro['tempoAFazer']}', {registro['tempoAFazerD']}, {atividade['ultimoRegistro']})"
    else:
        insert = f"INSERT INTO registro(codigoSessaoAtividade, inicio, fim, data, nomeAtividade, tempoAFazer, tempoAFazerD) VALUES ({atividade['codigo']}, '{registro['inicio']}','{registro['fim']}','{datetime.date.today()}', '{atividade['nomeAtividade']}', '{registro['tempoAFazer']}', {registro['tempoAFazerD']})"

    update = f"UPDATE sessao_atividade set tempoAFazer = '{registro['tempoAFazer']}', tempoAFazerdecimal = {registro['tempoAFazerD']} where codigo={atividade['codigo']}"
    cursor.execute(insert)
    cursor.execute(update)
    conexao.commit()
    ultimoRegistro = listAny('registro', fields='codigo', complement=f"where codigoSessaoAtividade = {atividade['codigo']} order by data desc, inicio desc limit 1")[0]
    update = f"UPDATE sessao_atividade set ultimoRegistro = '{ultimoRegistro['codigo']}' where codigo={atividade['codigo']}"
    cursor.execute(update)
    conexao.commit()
    if len(listAny('sessao_atividade',complement=f"where codigoSessao = {atividade['codigoSessao']} and tempoAFazerdecimal > 0")) <= 0:# verifica se a sessão finalizou
        print('sessão terminada')
        update = f"UPDATE sessao set status = 'finalizada', fimData = '{datetime.date.today()}' where codigo={atividade['codigoSessao']}"
        cursor.execute(update)
        conexao.commit()
        #tempo a fazer se ultimo registro for none deve ser o tempo total da atividade
        #verificar se a atividade tá completa

def gerenciarSessao():
    still = True
    while still:
        sessoes = listAny('sessao',fields='codigo, codigoCiclo, nome, nome_ciclo, status, inicioData, fimData, tempoTotalDecimal, tempoTotal, ultimaSessao')
        print(imprimirMenu(sessoes))
        print('[b] - back')
        r = input('R: ')
        
        if(r == 'b'):
            return
        sessaoEscolhida = sessoes[int(r)]
        if sessaoEscolhida['status'] == 'finalizada':
            print('essa sessão já está terminada')
            continue
        atividadesSessao = listAny('sessao_atividade',complement=f"where codigoSessao = {sessaoEscolhida['codigo']}")
        for i in atividadesSessao:
            if i['ultimoRegistro'] is None:
                i['tempoAFazerdecimal'] = sessaoEscolhida['tempoTotalDecimal'] * i['porcentagemTempoTotal']
            i['tempoAFazer'] = u.objetoHorasParaStringHoras(u.horaParaHorasBonita(i['tempoAFazerdecimal']))
        print('escolha uma atividade para realizar registro')
        print(imprimirMenu(atividadesSessao))
        print('[b] - back')
        r = input('R: ')
        if(r != 'b'):
            registrar(atividadesSessao[int(r)])

while True:
    
    r = input("[0] - criar ciclo\n[1] - Criar atividade\n[2] - listar ciclos\n[3] - gerenciar ciclo\n[4] - olhar sessões\n[5] - encerrar aplicação\nR: ")

    if r == "0":
        criar_ciclo()
    elif r == '1':
        criar_atividade()
    elif r == '2':
        showList(listAny('ciclo'))
    elif r == '3':
        gerenciarCiclo()
    elif r == '4':
        gerenciarSessao()
    elif r == "5":
        print('fechado')
        conexao.close()
        cursor.close()
        break
conexao.close()
cursor.close()