import socket
import threading

host = '127.0.0.1'
porta = 6060

apelido = input('Escolha um apelido: ')

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, porta))

def mostrarMenuComandos():
    print('\r\n1 - Conversar com alguem\r\n2 - Voltar\r\n')

def controlarInputMenuComandos(opcaoEscolhida):
    if (opcaoEscolhida == '1'):
        return input("\r\nApelido a procurar: ")
    elif (opcaoEscolhida == '2'):
        return 'Voltar'
    else:
        retorno = 'Opcao invalida!'
        print(retorno)
        return retorno

def receberMsgServidor():
    while True:
        try:
            mensagemRecebida = sock.recv(1024).decode('utf-8')
            if mensagemRecebida == 'APELIDO':
                sock.send(apelido.encode('utf-8'))
            elif (mensagemRecebida == "USER-NOT-FOUND"):
                print("Usuario nao encontrado!")
            elif ("USER-FOUND" in mensagemRecebida):
                index =  mensagemRecebida.split(":",1)[1]
                print(f"Usuario encontrado!")
                msgEnviar = input("Digite sua mensagem: ")
                sock.send(f"MENSAGEM-A-USUARIO:{index}:{msgEnviar}".encode('utf-8'))
            elif (mensagemRecebida != ''):
                print(mensagemRecebida)
        except Exception as e:
            print(f"Ops, parece que ocorreu algum problema :c ({e})\r\n")
            sock.close()
            break;

def enviarMsg():
    while True:
        mensagem = input("")
        if (mensagem == '/COMANDOS'):
            mostrarMenuComandos()
            opcaoEscolhida = input("")
            retorno = controlarInputMenuComandos(opcaoEscolhida)

            if (retorno == 'Opcao invalida!' or retorno == 'Voltar'):
                continue
            else:
                sock.send(("SEND-CONEXAO-USUARIO:"+retorno).encode('utf-8'))
                continue

        sock.send(mensagem.encode('utf-8'))

threadReceber = threading.Thread(target=receberMsgServidor)
threadReceber.start()

threadEnviar = threading.Thread(target=enviarMsg)
threadEnviar.start()
