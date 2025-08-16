
import math

def horaParaHorasBonita(horasFeia):
    segundos = horasFeia * 3600
    return formatHMS(segundos)

def formatHMS(segundos):#recebe tempo em segundos, e o converte em um objeto hora formatada

    return {
        'hora': int(segundos/3600),
        'minuto':(int(segundos/60))%60,
        'segundo': int(segundos%60)
    }

def criarHora():
    hora = {}
    hora["hora"] = int(input("hora: "))
    hora["minuto"] = int(input("minuto: "))
    hora["segundo"] = int(input("segundo: "))

    return hora

def diffHoras(hora, hora1):#recebe dois objetos hora formata, converte em segundos, realiza a subtração, e chama uma função para converter o resultado para objeto hora formatada
    segundos = (hora["hora"] * 60 + hora["minuto"]) * 60 + hora["segundo"]
    segundos1 = (hora1["hora"] * 60 + hora1["minuto"]) * 60 + hora1["segundo"]

    r = abs(segundos - segundos1)

    return formatHMS(r)

def sumHoras(hora, hora1):# possivel erro em horários perto do fim do dia
    segundos = (hora["hora"] * 60 + hora["minuto"]) * 60 + hora["segundo"]
    segundos1 = (hora1["hora"] * 60 + hora1["minuto"]) * 60 + hora1["segundo"]

    r = abs(segundos + segundos1)

    return formatHMS(r)

# transforma o objeto de horas em formato h:s:m em uma string hh:mm:ss
def partHour(part):#faz zeropad de HH ou MM ou SS
    part = str(part)
    if len(part) < 2:
        part = '0' + part
    return part

def objetoHorasParaStringHoras(horas):
    res = f"{partHour(horas["hora"])}:{partHour(horas["minuto"])}:{partHour(horas["segundo"])}"
    return res

def lessDecimalBadHour(hora,target):#ver se dar para corte bits desnecessários no float do python. UwU
    casas = 1
    while horaParaHorasBonita(math.ceil(hora * (10 * 10**(casas-1))) / (10 * 10**(casas-1))) != target:
        casas += 1
        rounded = math.ceil(hora * (10 * 10**(casas-1))) / (10 * 10**(casas-1))
        print(f"{(rounded)} - {objetoHorasParaStringHoras(horaParaHorasBonita(rounded))}")
    else:
        return math.ceil(hora * (10 * 10**(casas-1))) / (10 * 10**(casas-1))

def converteParaDecimalFeio(hora):
    segundos = (hora["hora"] * 60 + hora["minuto"]) * 60 + hora["segundo"]
    resultado = segundos/3600
    return resultado

def subTotalTempo(tempo, feito):
    TempoFormatado = horaParaHorasBonita(tempo)
    resultado = diffHoras(TempoFormatado, feito)
    horaDecimal = converteParaDecimalFeio(resultado)
    res = lessDecimalBadHour(horaDecimal,resultado)
    saida = f'tempo: {objetoHorasParaStringHoras(resultado)} - {res}'
    return saida #{'hora':converteParaDecimalFeio(resultado),'horas bonita': resultado}

feito = ''

while True:
    print("====================TASK-MANAGER====================")
    r = input('[1] - converte horas em decimal(ex: 4.80) para horas em (h:m:s)\n[2] - calcula diferença entre marcos temporais\n[3] - Soma horas\n[4] - marca o tempo cumprido de atividade\n[5] - sair\nR: ')
    if r == '1':
        print('CONVERSOR-HORA-DECIMAL-HORA-NORMAL')
        hora = float(input("Digite a hora a ser mostrada: "))
        print(horaParaHorasBonita(hora))
    elif r == '2':
        print('DIFERENCA-ENTRE-MARCOS-TEMPORAIS')
        print("marco-1")
        hora1 = criarHora()
        print("marco-2")
        hora2 = criarHora()
        feito = diffHoras(hora1,hora2) 
        print(f"tempo decorrido: {objetoHorasParaStringHoras(feito)}")
        print('tempo utilizado para marcar tempo de atividade')
    elif r == '3':
        print("SOMA-TEMPO")
        print("marco-1")
        hora1 = criarHora()
        print("marco-2")
        hora2 = criarHora()
        result = sumHoras(hora1,hora2) 
        print(result)

    elif r == '4':
        if feito == '':
            print('calcule o tempo de atividade realizada em [2] para prosseguir')
            print(feito)
            continue

        print('Marca oq foi cumprido')
        tempo = float(input("Digite o tempo reservado(em decimal feio): "))
        print(f"tempo decorrido: {objetoHorasParaStringHoras(feito)}")
        print(subTotalTempo(tempo, feito))

    elif r == '5':
        break










