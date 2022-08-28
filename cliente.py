import zmq
import os

'''
0: Archivo recibido
1: Ya existe el archivo
'''

context = zmq.Context()

#  Socket to talk to server
print("Connecting to server...")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")


name_client=input("Identificate, Nombre: ")
name_file=input("Nombre de archivo a enviar: ")

if os.path.exists(name_file):
    print("Enviando archivo")
    size_file = os.path.getsize(name_file)
    print("Tamaño de archivo: "+str(size_file)+" bytes")
    with open (name_file,"rb") as f:
        contenido = f.read(1024)
        while contenido:
            socket.send_multipart([bytes(name_client.encode()), bytes(name_file.encode()), contenido, bytes(str(size_file).encode())])
            contenido=f.read(1024)
            message = socket.recv()
            if message.decode() == "0":
                print(f"Received reply result: Archivo recibido")
                break
            elif message.decode() == "1" :
                print(f"Received reply result: Ya cuenta con un archivo con ese nombre")
                break
    f.close()
else:
    print("Archivo no encontrado, por favor revise el nombre del archivo")