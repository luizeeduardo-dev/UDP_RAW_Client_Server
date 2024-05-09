import datetime
import random

def display_menu():
    print("Qual requisição deseja realizar:")
    print("1. Data e hora atual")
    print("2. Mensagem motivacional para o fim do semestre")
    print("3. Quantidade de respostas emitidas pelo servidor até o momento")
    print("4. Sair\n")


# Converter para o fuso horário de Brasília (GMT-3)
def converter_horario_gmt(data_hora):
    data_hora_gmt = datetime.datetime.strptime(data_hora, "%a %b %d %H:%M:%S %Y")
    data_hora_gmt3 = datetime.timezone(datetime.timedelta(hours=-3))
    data_hora_brasilia = data_hora_gmt.replace(tzinfo=datetime.timezone.utc).astimezone(data_hora_gmt3)
    return data_hora_brasilia.strftime("%a %d-%m-%Y %H:%M:%S")

def processar_resposta(resposta):
    # Extrair o tipo de resposta
    tipo_resposta = resposta[0] & 0b00001111

    if tipo_resposta == 0x00:           # Resposta de data e hora
        data_hora = resposta[4:28].decode()
        local_data_hora = converter_horario_gmt(data_hora)
        print(f"\n{local_data_hora} (Horário de Brasília)\n")

    elif tipo_resposta == 0x01:         # Resposta de mensagem motivacional
        mensagem = resposta[4:].decode()
        print(f"\n{mensagem}\n")

    elif tipo_resposta == 0x02:         # Resposta de quantidade de respostas emitidas
        quantidade = int.from_bytes(resposta[4:], byteorder='big')
        print(f"\n{quantidade}\n")

    else:
        print("Resposta inválida do servidor.")
        
def criar_mensagem_requisicao(tipo):
    byte_req_tipo = 0x00
    byte_req_tipo |= tipo
    bytes_identificador = id_random().to_bytes(2, 'big')  # 16 bits para identificador
    mensagem = bytes([byte_req_tipo]) + bytes_identificador
    return mensagem

def id_random():
    id = random.randint(1,65535)
    return id