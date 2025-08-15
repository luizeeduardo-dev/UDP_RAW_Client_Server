# Projeto Redes: Cliente-Servidor UDP RAW 
Este é um projeto desenvolvido como parte da disciplina de Redes de Computadores I, oferecida pelo Centro de Informática da Universidade Federal da Paraíba.

## Descrição
O projeto consiste na implementação de dois clientes (um utilizando socket UDP e outro utilizando socket RAW) para uma aplicação cliente/servidor que encaminha requisições para um servidor executando os protocolos UDP/IP no endereço IP 15.228.191.109 e porta 50000. Cada cliente solicita ao usuário uma das seguintes opções de requisição:

1. Data e hora atual
2. Mensagem motivacional para o fim do semestre
3. Quantidade de respostas emitidas pelo servidor até o momento
4. Sair
Após receber a escolha do usuário, o cliente formata e envia a requisição para o servidor, que retorna uma resposta no mesmo formato. O cliente então exibe a resposta ao usuário de forma legível.

## Requisitos
Python 3.x

## Execução
1. Clone o repositório para o seu ambiente local.
2. Navegue até o diretório do projeto.
3. Execute o cliente UDP com o seguinte comando:
```
python client.py
```
Siga as instruções exibidas no terminal para interagir com o cliente.

## Autor
Luiz Eduardo Dias dos Santos - 20180171629
