# Cliente: sensor de presenca
import socket

HOST = "127.0.0.1"
PORTA = 5000
ID = "presenca1"

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((HOST, PORTA))
cliente.sendall((ID + ";TIPO;presenca\n").encode())

print("Sensor de presenca", ID, "conectado. Digite 'sair' para encerrar.")

while True:
    texto = input("Digite 1 para simular presenca: ").strip()
    if texto == "sair":
        break
    if texto == "1":
        cliente.sendall((ID + ";PRESENCA;1\n").encode())
    else:
        print("Valor invalido! Digite 1.")

cliente.close()
