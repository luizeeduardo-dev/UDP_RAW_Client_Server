import utils
import socket

# Luiz Eduardo Dias dos Santos - 20180171629

# Endereço IP e porta do servidor
SERVER_IP = "15.228.191.109"
SERVER_PORT = 50000

def main():
    # Criar um socket UDP
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

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

        mensagem = utils.criar_mensagem_requisicao(tipo)

        # Enviar a mensagem de requisição para o servidor
        udp_socket.sendto(mensagem, (SERVER_IP, SERVER_PORT))

        # Receber a resposta do servidor
        resposta, _ = udp_socket.recvfrom(1024)

        utils.processar_resposta(resposta)

    udp_socket.close()

if __name__ == "__main__":
    main()
