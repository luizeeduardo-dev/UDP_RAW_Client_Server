import datetime
import random
import socket

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

# Cria uma mensagem de requisição com base no tipo
def criar_mensagem_requisicao(tipo):
    byte_req_tipo = 0x00
    byte_req_tipo |= tipo
    bytes_identificador = id_random().to_bytes(2, 'big')  # 16 bits para identificador
    mensagem = bytes([byte_req_tipo]) + bytes_identificador
    return mensagem

# Gera um número aleatório para o identificador
def id_random():
    id = random.randint(1,65535)
    return id

# Cria um pseudo-cabeçalho para o cálculo do checksum UDP
def create_pseudo_header(protocol, source_ip, server_ip, header_size):
    source_ip = bytes(map(int, source_ip.split('.')))
    server_ip = bytes(map(int, server_ip.split('.')))
    zero = 0b00000000
    header_size = header_size.to_bytes(2, byteorder='big')
    pseudo_header = source_ip + server_ip + bytes([zero, protocol[0], header_size[0], header_size[1]])
    return pseudo_header

# Cria o cabeçalho UDP
def criar_header_udp(server_port, header_size, checksum):
    source_port = define_source_port().to_bytes(2, byteorder='big')
    server_port = server_port.to_bytes(2, byteorder='big')
    header_size = header_size.to_bytes(2, byteorder='big')
    checksum = checksum.to_bytes(2, byteorder='big')
    header = bytes([source_port[0], source_port[1], server_port[0],server_port[1],header_size[0],header_size[1], checksum[0], checksum[1]])
    return header

# Obtém uma porta de origem disponível
def define_source_port():
    sock = socket.socket()
    sock.bind(('', 0))
    return sock.getsockname()[1]

# Calcula o checksum de uma lista de bytes
def cheksum(bytes_list):
    list_size = len(bytes_list)
    if list_size % 2 == 0:                  
       pass
    else:
        bytes_list = bytes_list + bytes([0])  
    list_size = len(bytes_list)            
    index = 0
    cheksum = 0
    for i in range(int(list_size/4)):
        cheksum = sum_word_16bits(cheksum, sum_word_16bits(bytes_list[index] << 8 | bytes_list[index + 1],bytes_list[index + 2] << 8 | bytes_list[index + 3]))
        index += 4
    return ~cheksum & 0xFFFF  # Faz a inversão dos bits

def sum_word_16bits(word1, word2):
    result = word1 + word2
    while result.bit_length() > 16:
        carry = result >> 16
        result &= 0xFFFF
        result += carry
    return result

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
