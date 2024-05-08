import socket
import random

SERVER_IP = "15.228.191.109"
SERVER_PORT = 50000

def main():
    # Criar um socket UDP
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        # Solicitar a escolha do usuário
        print("Escolha uma opção:")
        print("1. Data e hora atual")
        print("2. Mensagem motivacional para o fim do semestre")
        print("3. Quantidade de respostas emitidas pelo servidor até o momento")
        print("4. Sair")
        escolha = input("Opção: ")

        if escolha == "4":
            break

        identificador = random.randint(1,65535)

        if escolha == "1":
            tipo = 0b00000000
        elif escolha == "2":
            tipo = 0b00000001
        elif escolha == "3":
            tipo = 0b00000010
        else:
            print("Opção inválida.")
            continue

        # Criar a mensagem de requisição
        mensagem = criar_mensagem_requisicao(tipo, random.randint(1, 65535))

        # Enviar a mensagem de requisição para o servidor
        udp_socket.sendto(mensagem, (SERVER_IP, SERVER_PORT))

        # Receber a resposta do servidor
        resposta, _ = udp_socket.recvfrom(1024)

        processar_resposta(resposta)

        # Processar e exibir a resposta
        print(resposta)

    # Fechar o socket UDP
    udp_socket.close()

# Função para criar a mensagem de requisição
def criar_mensagem_requisicao(tipo, identificador):

    byte_req_tipo = 0b00000000
    byte_req_tipo |= tipo
    bytes_identificador = identificador.to_bytes(2, 'big')  # 16 bits para identificador
    mensagem = bytes([byte_req_tipo]) + bytes_identificador
    return mensagem

def processar_resposta(resposta):
    # Extrair o tipo de resposta
    tipo_resposta = resposta[0] & 0b00001111

    if tipo_resposta == 0x00:  # Resposta de data e hora
        data_hora = resposta[3:].decode()
        print(f"Resposta do servidor: {data_hora}")

    elif tipo_resposta == 0b00010001:  # Resposta de mensagem motivacional
        mensagem = resposta[4:].decode()
        print(f"Resposta do servidor: {mensagem}")

    elif tipo_resposta == 0b00010010:  # Resposta de quantidade de respostas emitidas
        quantidade = int.from_bytes(resposta[4:], byteorder='big')
        print(f"Resposta do servidor: {quantidade}")

    else:
        print("Resposta inválida do servidor.")


if __name__ == "__main__":
    main()