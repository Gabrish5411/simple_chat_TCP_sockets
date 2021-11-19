import socket
import threading

nombre = input("Ingresa tu nombre de usuario: ")
if nombre == 'admin':
    clave = input("Ingresar clave admin: ")

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Connect to a host
cliente.connect(('127.0.0.1',60000))

thread_estado = False

def recibir():
    while True:
        global thread_estado
        if thread_estado:
            break    
        try:
            message = cliente.recv(1024).decode('ascii')
            if message == 'NOMBRE':
                cliente.send(nombre.encode('ascii'))
                message2 = cliente.recv(1024).decode('ascii')
                if message2 == 'CLAVE':
                    cliente.send(clave.encode('ascii'))
                    if cliente.recv(1024).decode('ascii') == 'REFUSE':
                        print("Clave incorrecta. No se pudo establecer la conexion")
                        thread_estado = True
            elif message == 'CONECTADOS\n':
                message2 = cliente.recv(1024).decode('ascii')
                print("Los usuarios conectados son los siguientes", message2)
                destino = input("")
                cliente.send(destino.encode('ascii'))
                mensaje_priv = input("")
                cliente.send(mensaje_priv.encode('ascii'))

            elif message == 'INVITAR A: \n':
                message2 = cliente.recv(1024).decode('ascii')
                print("Los usuarios conectados son los siguientes", message2)
                print("Ahora selecciona el nick del grupo (1 palabra)")
                conjunto = input("")
                cliente.send(conjunto.encode('ascii'))
                nick = input("")
                cliente.send(nick.encode('ascii'))
            
            elif message == 'MENSAJE A GRUPO: \n':
                cliente.recv(1024).decode('ascii') #Nombres grupos
                cliente.send(message2.encode('ascii')) #grupo destino
                print("Escribe el mensaje que deseas enviar")
                message2 = input("")
                cliente.send(message2.encode('ascii'))
                

            else:
                print(message)
        except:
            print('Error en la conexion')
            cliente.close()
            break





        
def escribir():
    while True:
        if thread_estado:
            break
        message = f'{nombre}: {input("")}'
        if message[len(nombre)+2:].startswith('/'):
            if nombre == 'admin':
                if message[len(nombre)+2:].startswith('/kick'):
                    cliente.send(f'KICK {message[len(nombre)+2+6:]}'.encode('ascii'))
            else:
                print("No posees credenciales de administrador")
        else:
            cliente.send(message.encode('ascii'))

recieve_thread = threading.Thread(target=recibir)
recieve_thread.start()
write_thread = threading.Thread(target=escribir)
write_thread.start()