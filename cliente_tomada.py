# Cliente: tomada (mede o consumo e envia de 2 em 2 minutos)
import socket
import random
import time

HOST = "127.0.0.1"
PORTA = 5000
ID = "tomada1"       
INTERVALO = 120       

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((HOST, PORTA))
cliente.sendall((ID + ";TIPO;tomada\n").encode())

print("Tomada", ID, "conectada. Enviando consumo a cada", INTERVALO, "segundos.")

while True:
    consumo = round(random.uniform(0.1, 10), 2)   # corrente em amperes
    cliente.sendall((ID + ";CONSUMO;" + str(consumo) + "\n").encode())
    print("Consumo enviado:", consumo, "A")
    time.sleep(INTERVALO)
