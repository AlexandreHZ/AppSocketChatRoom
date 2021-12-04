import socket
import threading

host = '127.0.0.1'
porta = 6060

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((host, porta))

servidor.listen()

clientes = []
apelidos = []

def fazerBroadcast(mensagem):
    for cliente in clientes:
        cliente.send(mensagem)

def enviarMsgACliente(mensagem, indexCliente):
    clientes[indexCliente].send(mensagem)

def receberMensagem(cliente):
    while True:
        indexCliente = clientes.index(cliente)
        try:
            mensagem = cliente.recv(1024).decode("utf-8")
            print(f"Cliente {apelidos[indexCliente]} enviou a mensagem ´{mensagem}´\r\n")

            if ("SEND-CONEXAO-USUARIO:" in mensagem):
                indexClienteAConectar = 99999
                msgDividida = mensagem.split(":")

                if (len(msgDividida) <= 1):
                    continue

                nomeUsuarioAConectar = msgDividida[1]
                for apelido in apelidos:
                    if (apelido == nomeUsuarioAConectar):
                        indexClienteAConectar = apelidos.index(apelido)
                        break

                if (indexClienteAConectar != 99999):
                    cliente.send(f"USER-FOUND:{indexClienteAConectar}".encode("utf-8"))
                else:
                    cliente.send("USER-NOT-FOUND".encode("utf-8"))
                continue

            if ("MENSAGEM-A-USUARIO:" in mensagem):
                msgDividida = mensagem.split(":")
                if (len(msgDividida) <= 1):
                    continue

                indexClienteAConectar = int(msgDividida[1])
                msgEnviarACliente = msgDividida[2]
                enviarMsgACliente((f"{apelidos[indexCliente]} por mensagem privada:{msgEnviarACliente}\r\n").encode("utf-8"), indexClienteAConectar)
                continue

            fazerBroadcast(f"{apelidos[indexCliente]}: {mensagem}\r\n".encode("utf-8"))
        except Exception as e:
            print(e)
            clientes.remove(cliente)
            cliente.close()
            apelido = apelidos[indexCliente]
            print(f'{apelido} desconectado!')
            fazerBroadcast(f'{apelido} saiu da sala!'.encode('utf-8'))
            apelidos.remove(apelido)
            break

def receberCliente():
    while True:
        cliente, endereco = servidor.accept()
        print(f"Conectado com {str(endereco)}!\r\n")

        cliente.send("APELIDO".encode('utf-8'))
        apelido = cliente.recv(1024).decode('utf-8')

        apelidos.append(apelido)
        clientes.append(cliente)

        print(f"Cliente conectado no servidor: {apelido}\r\n")
        fazerBroadcast(f"\r\n{apelido} conectado a sala!\r\n".encode("utf-8"))
        cliente.send('Conectado ao servidor!'.encode('utf-8'))

        thread = threading.Thread(target=receberMensagem, args=(cliente,))
        thread.start();

print(f"Servidor rodando na porta {porta} pelo host {host}\r\n")
receberCliente()