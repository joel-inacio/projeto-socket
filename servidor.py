# Servidor central da Smart Home (TCP + threads)
import socket
import threading
import time
from datetime import datetime

HOST = "127.0.0.1"
PORTA = 5000
ARQUIVO_CONSUMO = "consumo.txt"
TEMPO_SEM_PRESENCA = 600   
TEMPERATURA_LIMITE = 28    
TEMPERATURA_AR = 22        

# guarda os dispositivos conectados: id -> [conexao, tipo]
dispositivos = {}
lock = threading.Lock()

# estado da casa
ultima_presenca = 0
lampadas_ligadas = False
ar_ligado = False


def enviar(conexao, comando, valor=""):
    # formato da mensagem: ID;COMANDO;VALOR
    mensagem = "SERVIDOR;" + comando + ";" + valor + "\n"
    try:
        conexao.sendall(mensagem.encode())
    except:
        pass


def enviar_para_tipo(tipo, comando, valor=""):
    # envia a mensagem para todos os dispositivos de um tipo
    with lock:
        for id_disp in dispositivos:
            conexao, tipo_disp = dispositivos[id_disp]
            if tipo_disp == tipo:
                enviar(conexao, comando, valor)


def ligar_lampadas():
    global lampadas_ligadas
    lampadas_ligadas = True
    enviar_para_tipo("lampada", "LIGAR")


def desligar_lampadas():
    global lampadas_ligadas
    lampadas_ligadas = False
    enviar_para_tipo("lampada", "DESLIGAR")


def ligar_ar():
    global ar_ligado
    ar_ligado = True
    enviar_para_tipo("ar", "LIGAR", str(TEMPERATURA_AR))


def desligar_ar():
    global ar_ligado
    ar_ligado = False
    enviar_para_tipo("ar", "DESLIGAR")


def salvar_consumo(id_disp, consumo):
    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    with open(ARQUIVO_CONSUMO, "a") as arquivo:
        arquivo.write(data_hora + " | " + id_disp + " | " + consumo + " A\n")


def atender_cliente(conexao, endereco):
    global ultima_presenca
    id_disp = None
    arquivo = conexao.makefile("r")  # permite ler linha por linha
    try:
        for linha in arquivo:
            partes = linha.strip().split(";")
            if len(partes) < 2:
                continue
            id_disp = partes[0]
            comando = partes[1]
            valor = ""
            if len(partes) > 2:
                valor = partes[2]

            if comando == "TIPO":
                with lock:
                    dispositivos[id_disp] = [conexao, valor]
                print("[+]", id_disp, "conectado (tipo:", valor + ")")
                # se ja estiver ligado, avisa o novo dispositivo
                if valor == "lampada" and lampadas_ligadas:
                    enviar(conexao, "LIGAR")
                if valor == "ar" and ar_ligado:
                    enviar(conexao, "LIGAR", str(TEMPERATURA_AR))

            elif comando == "PRESENCA":
                print("[presenca]", id_disp, "detectou pessoas")
                ultima_presenca = time.time()
                if not lampadas_ligadas:
                    ligar_lampadas()

            elif comando == "TEMPERATURA":
                print("[temperatura]", id_disp, "-", valor, "graus")
                try:
                    temperatura = float(valor)
                    if temperatura > TEMPERATURA_LIMITE and not ar_ligado:
                        print("Ambiente acima de", TEMPERATURA_LIMITE, "graus. Ligando o ar...")
                        ligar_ar()
                except ValueError:
                    print("Temperatura invalida:", valor)

            elif comando == "CONSUMO":
                print("[consumo]", id_disp, "-", valor, "A")
                salvar_consumo(id_disp, valor)
    except:
        pass

    # cliente desconectou
    if id_disp != None:
        with lock:
            if id_disp in dispositivos:
                del dispositivos[id_disp]
        print("[-]", id_disp, "desconectado")
    conexao.close()


def monitorar_presenca():
    # desliga as lampadas se ninguem aparecer por 10 minutos by Joel
    while True:
        time.sleep(5)
        if lampadas_ligadas and time.time() - ultima_presenca > TEMPO_SEM_PRESENCA:
            print("Sem presenca ha mais de 10 minutos. Desligando lampadas...")
            desligar_lampadas()


def console_servidor():
    # comandos digitados no servidor para controle manual by Joel
    print("Comandos: lampada on | lampada off | ar on | ar off | listar")
    while True:
        comando = input().strip().lower()
        if comando == "lampada on":
            ligar_lampadas()
        elif comando == "lampada off":
            desligar_lampadas()
        elif comando == "ar on":
            ligar_ar()
        elif comando == "ar off":
            desligar_ar()
        elif comando == "listar":
            for id_disp in dispositivos:
                print(id_disp, "-", dispositivos[id_disp][1])
        else:
            print("Comando desconhecido")


servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
servidor.bind((HOST, PORTA))
servidor.listen()
print("Servidor rodando em", HOST, "porta", PORTA)

threading.Thread(target=monitorar_presenca, daemon=True).start()
threading.Thread(target=console_servidor, daemon=True).start()

while True:
    conexao, endereco = servidor.accept()
    threading.Thread(target=atender_cliente, args=(conexao, endereco), daemon=True).start()
