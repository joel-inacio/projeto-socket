# Cliente: lampada
import socket

HOST = "127.0.0.1"
PORTA = 5000
ID = "lampada1"  

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((HOST, PORTA))
cliente.sendall((ID + ";TIPO;lampada\n").encode())

print("Lampada", ID, "conectada")
print("desligada")

arquivo = cliente.makefile("r")
for linha in arquivo:
    partes = linha.strip().split(";")
    comando = partes[1]
    if comando == "LIGAR":
        print("ligada")
    elif comando == "DESLIGAR":
        print("desligada")

print("Conexao encerrada pelo servidor")
