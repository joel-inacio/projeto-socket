# Cliente: ar condicionado
import socket

HOST = "127.0.0.1"
PORTA = 5000
ID = "ar1"

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((HOST, PORTA))
cliente.sendall((ID + ";TIPO;ar\n").encode())

print("Ar condicionado", ID, "conectado")
print("desligado")

arquivo = cliente.makefile("r")
for linha in arquivo:
    partes = linha.strip().split(";")
    comando = partes[1]
    if comando == "LIGAR":
        temperatura = partes[2]
        print("ligado com temperatura", temperatura, "graus")
    elif comando == "DESLIGAR":
        print("desligado")

print("Conexao encerrada pelo servidor")
