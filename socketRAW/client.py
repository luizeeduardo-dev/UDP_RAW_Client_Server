import utils
import socket

# Luiz Eduardo Dias dos Santos - 20180171629

# Endereço IP e porta do servidor
SERVER_IP = "15.228.191.109"
SOURCE_IP = "192.168.1.105"
SERVER_PORT = 50000
SOURCE_PORT = 0

def main():
    # Criar um socket UDP
    socket_raw = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
    protocol = socket.IPPROTO_UDP.to_bytes(1, byteorder='big')


    while True:
        utils.display_menu()
        escolha = input("Opção: ")
        if escolha == "4":
            print("até logo!")
            break

        if escolha in ["1", "2", "3"]:
            tipo = int(escolha) - 1  # Tipo começa em 0, então subtraímos 1
        else:
            print("Opção inválida.")
            continue

        message = utils.criar_mensagem_requisicao(tipo)
        header_size  = 8 + len(message)
        checksum = 0
        
        # Cria o cabeçalho UDP
        udp_header = utils.criar_header_udp(SERVER_PORT, header_size, checksum)
        segment = udp_header + message
        
        # Cria um pseudo-cabeçalho para o cálculo do checksum
        pseudo_header = utils.create_pseudo_header(protocol, SOURCE_IP, SERVER_IP, header_size)
        checksum = utils.cheksum(pseudo_header + segment)  # Calcula o checksum do segmento

        # Atualiza o cabeçalho UDP com o checksum calculado
        udp_header = utils.criar_header_udp(SERVER_PORT, header_size, checksum)

        destination_address = (SERVER_IP, SERVER_PORT)        # Endereço do servidor
        socket_raw.sendto(segment, destination_address)
        resposta, _ = socket_raw.recvfrom(2040)    # Recebe a resposta do servidor
        payload = resposta[28:]
        
        utils.processar_resposta(payload)  # Decodifica a resposta de acordo com o tipo da requisição

if __name__ == "__main__":
    main()