import math
from decimal import Decimal

def horaParaHorasBonita(horasFeia):
    segundos = horasFeia * 3600
    return formatHMS(segundos)

def formatHMS(segundos):#recebe tempo em segundos, e o converte em um objeto hora formatada

    return {
        'hora': int(segundos/3600),
        'minuto':int((segundos/60)%60),
        'segundo': int(segundos%60)
    }

def stringHoraToObject(horaString):
        hora = {}
        object = horaString.split(":")
        hora["hora"] = int(object[0])
        hora["minuto"] = int(object[1])
        hora["segundo"] = int(object[2])
        return hora

def criarHora():
    horaString = input("Digite a hora(ex: 12:30:20): ")

    return stringHoraToObject(horaString)

def diffHoras(hora, hora1):#recebe dois objetos hora formata, converte em segundos, realiza a subtração, e chama uma função para converter o resultado para objeto hora formatada
    segundos = (hora["hora"] * 60 + hora["minuto"]) * 60 + hora["segundo"]
    segundos1 = (hora1["hora"] * 60 + hora1["minuto"]) * 60 + hora1["segundo"]

    r = abs(segundos - segundos1)

    return formatHMS(r)

def sumHoras(hora, hora1):# possivel erro em horários perto do fim do dia
    segundos = (hora["hora"] * 60 + hora["minuto"]) * 60 + hora["segundo"]
    segundos1 = (hora1["hora"] * 60 + hora1["minuto"]) * 60 + hora1["segundo"]

    r = abs(segundos + segundos1)

    return objetoHorasParaStringHoras(formatHMS(r))

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
    numero = str(hora)
    if(len(numero.split('.')[1]) < 3):
        pass
        #return hora
    casas = 1
    while horaParaHorasBonita(math.ceil(hora * (10 * 10**(casas-1))) / (10 * 10**(casas-1))) != target:
        casas += 1
        #print(hora * (10 * 10**(casas-1)))
        rounded = math.ceil(hora * (10 * 10**(casas-1))) / (10 * 10**(casas-1))
        #print(f"{(rounded)} - {objetoHorasParaStringHoras(horaParaHorasBonita(rounded))}")
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

def testeFormatHMS():
    multiplicador100 = 10 ** 1
    for i in range(0,25 * multiplicador100):
        #print(f'{i/multiplicador100} - {((i/multiplicador100) * 3600)}')
        print(horaParaHorasBonita(i/multiplicador100))