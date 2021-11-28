import socket
import threading

host = '127.0.0.1'
porta = 6060

apelido = input('Escolha um apelido: ')

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, porta))

def receberMsgServidor():
    while True:
        try:
            mensagemRecebida = sock.recv(1024).decode('utf-8')
            if mensagemRecebida == 'APELIDO':
                sock.send(apelido.encode('utf-8'))
            else:
                print(mensagemRecebida)
        except Exception as e:
            print(f"Ops, parece que ocorreu algum problema :c ({e})\r\n")
            sock.close()
            break;

def enviarMsg():
    while True:
        mensagem = input("")
        sock.send(mensagem.encode('utf-8'))

threadReceber = threading.Thread(target=receberMsgServidor)
threadReceber.start()

threadEnviar = threading.Thread(target=enviarMsg)
threadEnviar.start()