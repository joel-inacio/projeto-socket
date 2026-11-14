# Cliente: termometro (sensor de temperatura)
import socket

HOST = "127.0.0.1"
PORTA = 5000
ID = "termometro1"

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((HOST, PORTA))
cliente.sendall((ID + ";TIPO;termometro\n").encode())

print("Termometro", ID, "conectado. Digite 'sair' para encerrar.")

while True:
    texto = input("Temperatura do ambiente: ").strip().replace(",", ".")
    if texto == "sair":
        break
    try:
        float(texto)   # so para verificar se e um numero
    except ValueError:
        print("Digite um numero valido!")
        continue
    cliente.sendall((ID + ";TEMPERATURA;" + texto + "\n").encode())

cliente.close()
