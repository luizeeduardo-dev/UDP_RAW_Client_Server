import socket
import random
import struct
import sys

# Endereço IP e porta do servidor
SERVER_IP = "15.228.191.109"
SOURCE_IP = "192.168.1.105"
SERVER_PORT = 50000

# Função para calcular o checksum UDP
def calcular_checksum(pseudo_cabecalho, cabecalho_udp, payload):
    # Concatenar o pseudo cabeçalho, cabeçalho UDP e payload
    udp_segment = pseudo_cabecalho + cabecalho_udp + payload
    
    # Se o comprimento for ímpar, adicionar um byte zero ao final
    if len(udp_segment) % 2 == 1:
        udp_segment += b'\x00'

    # Calcular a soma de 16 bits
    soma = 0
    for i in range(0, len(udp_segment), 2):
        soma += (udp_segment[i] << 8) + udp_segment[i + 1]

    # Wraparound de carry-out
    soma = (soma & 0xFFFF) + (soma >> 16)
    soma += (soma >> 16)

    # Calcular o complemento de 1
    checksum = ~soma & 0xFFFF

    return checksum

# Função para criar o cabeçalho UDP
def criar_cabecalho_udp(origem_porta, destino_porta, comprimento, checksum):
    return struct.pack('!HHHH', origem_porta, destino_porta, comprimento, checksum)

# Função para criar a mensagem de requisição com cabeçalho UDP
def criar_mensagem_requisicao(tipo, identificador):
    origem_porta = 0xE713
    destino_porta = SERVER_PORT
    comprimento = 0x000B
    checksum = 0x0000  # Inicialmente, o checksum é zero

    # Pseudo cabeçalho IP
    pseudo_cabecalho = socket.inet_aton("192.168.1.105") + socket.inet_aton(SERVER_IP) + 0x0011 + struct.pack('!H', comprimento)

    cabecalho_udp = criar_cabecalho_udp(origem_porta, destino_porta, comprimento, checksum)

    # Criar a mensagem de requisição
    mensagem = cabecalho_udp + bytes([tipo]) + identificador.to_bytes(2, 'big')

    # Calcular o checksum UDP
    checksum = calcular_checksum(pseudo_cabecalho, cabecalho_udp, mensagem)
    cabecalho_udp = criar_cabecalho_udp(origem_porta, destino_porta, comprimento, checksum)

    # Atualizar o cabeçalho UDP com o checksum correto
    mensagem = cabecalho_udp + bytes([tipo]) + identificador.to_bytes(2, 'big')

    return mensagem

# Função para processar e exibir a resposta do servidor
def processar_resposta(resposta):
    # Extrair o tipo de resposta
    tipo_resposta = resposta[8] & 0b00001111

    if tipo_resposta == 0x00:  # Resposta de data e hora
        data_hora = resposta[11:].decode()
        print(f"\n{data_hora}")

    elif tipo_resposta == 0x01:  # Resposta de mensagem motivacional
        mensagem = resposta[12:].decode()
        print(f"\n{mensagem}\n")

    elif tipo_resposta == 0x02:  # Resposta de quantidade de respostas emitidas
        quantidade = int.from_bytes(resposta[12:], byteorder='big')
        print(f"\n{quantidade}\n")

    else:
        print("Resposta inválida do servidor.")

# Função principal do cliente
def main():
    # Criar um socket RAW com protocolo IPPROTO_UDP
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)

    while True:
        # Solicitar a escolha do usuário
        print("Escolha uma opção:")
        print("1. Data e hora atual")
        print("2. Mensagem motivacional para o fim do semestre")
        print("3. Quantidade de respostas emitidas pelo servidor até o momento")
        print("4. Sair\n")
        escolha = input("Opção: ")

        if escolha == "4":
            break

        identificador = random.randint(1, 65535)

        if escolha == "1":
            tipo = 0x00
        elif escolha == "2":
            tipo = 0x01
        elif escolha == "3":
            tipo = 0x02
        else:
            print("Opção inválida.")
            continue

        # Criar a mensagem de requisição com cabeçalho UDP
        mensagem = criar_mensagem_requisicao(tipo, identificador)

        # Enviar a mensagem de requisição para o servidor
        udp_socket.sendto(mensagem, (SERVER_IP, SERVER_PORT))

        # Receber a resposta do servidor
        resposta, _ = udp_socket.recvfrom(1024)

        # Processar e exibir a resposta
        processar_resposta(resposta)

    # Fechar o socket RAW
    udp_socket.close()

if __name__ == "__main__":
    main()
