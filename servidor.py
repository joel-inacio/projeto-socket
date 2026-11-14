import socket
import threading
import time

clientes = {}    # clientes["ar:sala"] = conexao
presenca = {}    # presenca["sala"] = hora da ultima presenca


def cuidar(conexao):
    # primeira mensagem: "tipo:comodo|REGISTRO|-"
    texto = conexao.recv(1024).decode()
    nome = texto.split("|")[0]
    tipo = nome.split(":")[0]
    comodo = nome.split(":")[1]
    clientes[nome] = conexao
    print("Conectou:", nome)

    while True:
        texto = conexao.recv(1024).decode()
        if texto == "":
            break

        partes = texto.split("|")
        controle = partes[1]
        valor = partes[2]
        print(nome, "enviou:", controle, valor)

        if controle == "TEMP":
            if float(valor) > 28 and "ar:" + comodo in clientes:
                clientes["ar:" + comodo].send("servidor|LIGAR|22".encode())

        if controle == "PRESENCA":
            presenca[comodo] = time.time()
            if "lampada:" + comodo in clientes:
                clientes["lampada:" + comodo].send("servidor|LIGAR|-".encode())

        if controle == "CONSUMO":
            arquivo = open("consumo.txt", "a")
            arquivo.write(nome + " | " + valor + "\n")
            arquivo.close()

    del clientes[nome]
    conexao.close()


def verificar():
    while True:
        time.sleep(5)
        for comodo in list(presenca.keys()):
            # 600 segundos = 10 minutos
            if time.time() - presenca[comodo] > 600:
                if "lampada:" + comodo in clientes:
                    clientes["lampada:" + comodo].send("servidor|DESLIGAR|-".encode())
                del presenca[comodo]


servidor = socket.socket()
servidor.bind(("127.0.0.1", 9999))
servidor.listen()
print("Servidor iniciado")

threading.Thread(target=verificar, daemon=True).start()

while True:
    conexao, endereco = servidor.accept()
    threading.Thread(target=cuidar, args=(conexao,)).start()