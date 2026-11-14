import socket
import time
import random

s = socket.socket()
s.connect(("127.0.0.1", 9999))

tipo = input("Tipo (termometro, presenca, tomada, ar, lampada): ")
comodo = input("Comodo (sala, quarto1, quarto2): ")
meu_id = tipo + ":" + comodo

s.send((meu_id + "|REGISTRO|-").encode())

if tipo == "termometro":
    while True:
        temp = input("Temperatura: ")
        s.send((meu_id + "|TEMP|" + temp).encode())

if tipo == "presenca":
    while True:
        input("Digite 1 para simular presenca: ")
        s.send((meu_id + "|PRESENCA|1").encode())

if tipo == "tomada":
    while True:
        time.sleep(120)  # 2 minutos
        consumo = random.randint(1, 15)
        print("Consumo enviado:", consumo)
        s.send((meu_id + "|CONSUMO|" + str(consumo)).encode())

if tipo == "lampada":
    print("desligada")
    while True:
        msg = s.recv(1024).decode()
        if msg.split("|")[1] == "LIGAR":
            print("ligada")
        else:
            print("desligada")

if tipo == "ar":
    print("desligado")
    while True:
        msg = s.recv(1024).decode()
        if msg.split("|")[1] == "LIGAR":
            print("ligado com temperatura", msg.split("|")[2], "graus")
        else:
            print("desligado")