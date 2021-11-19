import threading
from _thread import *
import socket

host = "127.0.0.1"
port = 60000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clientes = [] #Direcciones de los usuarios que se conectan
nombres = [] #Nombre de los usuarios que se conectan

grupo_clientes = []
grupo_nombres = []
nicks_grupos = []

def echar_cliente(usuario):
	if usuario in nombres:
		posicion_nombre = nombres.index(usuario)
		echar_a_cliente = clientes[posicion_nombre]
		clientes.remove(echar_a_cliente)
		echar_a_cliente.send('Fuiste echado del servidor por el admin'.encode('ascii'))
		echar_a_cliente.close()
		nombres.remove(usuario)
		aTodos(f'{usuario} fue echado del servidor por el admin'.encode('ascii'))




def aTodos(mnsj):
    for cliente in clientes:
        cliente.send(mnsj)


def handle(cliente): #Handelea los mensajes enviados a traves del servidor
    while True:
        try:
            msj = mensaje = cliente.recv(1024)  
            if msj.decode('ascii').startswith('KICK'):
                if nombres[clientes.index(cliente)] == 'admin':
                    echar = msj.decode('ascii')[5:]
                    echar_cliente(echar)
                else:
                    cliente.send('Comando no realizado'.encode('ascii'))
            elif msj.decode('ascii')[-4::] == "SHOW":
                todos = ""
                for miembro in nombres:
                    todos+=miembro
                cliente.send('CONECTADOS\n'.encode('ascii'))
                cliente.send(todos.encode('ascii'))
                destino = cliente.recv(1024).decode('ascii').split(" ")
                dir_destino = nombres.index(destino[1])
                mensaje_priv = cliente.recv(1024).decode('ascii')
                clientes[dir_destino].send(mensaje_priv.encode('ascii'))

            elif msj.decode('ascii')[-11::] == "CREATEGROUP":
                todos = ""
                for miembro in nombres:
                    todos+=miembro
                cliente.send('INVITAR A: \n'.encode('ascii'))
                cliente.send(todos.encode('ascii'))

                l_dirs = []
                integrantes = cliente.recv(1024).decode('ascii').split(" ") #Se mandan los que se quiere invitar al grupo separados por un espacio
                integrantes.pop(0) #Borro el Matias: que se guardaba en la lista
                integrantes.append(nombres[clientes.index(cliente)]) #agrego al cliente que ide crear el grupo
                print(integrantes)
                grupo_nombres.append(integrantes)
                for i in integrantes:    
                    l_dirs.append(clientes[nombres.index(i)])
                grupo_clientes.append(l_dirs)
                nick = cliente.recv(1024).decode('ascii').split(" ")
                nicks_grupos.append(nick[1])

            elif msj.decode('ascii')[-8::] == "MSGGROUP":
                cliente.send('MENSAJE A GRUPO: \n'.encode('ascii'))
                todos_grupos = ""
                for i in nicks_grupos:
                    todos_grupos+=i
                cliente.send(todos_grupos.encode('ascii'))
                name = cliente.recv(1024).decode('ascii').split(" ") #agarro nombre del grupo al que le quiere hablar
                pos = nicks_grupos.index(name[1])
                if cliente not in grupo_clientes[pos]: #caso de que usuario quiera escribir en un grupo en el que no esta
                    print("Acceso a grupo denegado")
                    continue
                mensaje_group = cliente.recv(1024).decode('ascii') #mensaje por mandar a integrantes del grupo
                for direcciones in grupo_clientes[pos]:
                    direcciones.send(mensaje_group.encode('ascii'))

            else:	
                aTodos(mensaje)   #Se deberia elegir si mandarlo a todos?
        except:
            if cliente in clientes:
                index = clientes.index(cliente)
                cliente.remove(cliente)
                cliente.close
                nombre = nombres[index]
                aTodos(f'{nombre} ha abandonado el chat'.encode('ascii'))
                nombres.remove(nombre)
				#for i in range(len(clientes)):
				#	if clientes[i] == cliente:
				#		del clientes[i]
				#		aTodos((str(nombres[i])+" acaba de salir del chat").encode('ascii'))
				#		del nombres[i]
                break

def recibir(): #Se encarga de la conexión con el cliente
    while True:
        cliente, direccion = server.accept()
        print(f"Conectado con", direccion)
        cliente.send('NOMBRE'.encode('ascii'))
        nombre = cliente.recv(1024).decode('ascii')
        if nombre == 'admin':
            cliente.send('CLAVE'.encode('ascii'))
            password = cliente.recv(1024).decode('ascii')
            if password != 'sistemas':
                cliente.send('REFUSE'.encode('ascii'))
                cliente.close()
                continue

        nombres.append(nombre)
        clientes.append(cliente)

        
        aTodos(f'{nombre} se ha unido al chat'.encode('ascii'))
        cliente.send('Conectado al servidor con exito'.encode('ascii'))


        thread = threading.Thread(target=handle, args=(cliente,))
        thread.start()





print('Server is Listening ...')
recibir()