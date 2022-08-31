import zmq
import os
import hashlib

'''
0: Voy a enviar un primer mensaje
1: El archivo que envie ya existe
2: estoy enviando un archivo
'''
def identificar_cliente() -> str:
    name_client=input("Identificate, Nombre: ")
    return name_client

def md5Hash(filename: str) -> str:
    md5_hash = hashlib.md5()
    with open(filename,"rb") as f:
        # Read and update hash in chunks of 1K
        for byte_block in iter(lambda: f.read(1024),b""):
            md5_hash.update(byte_block)
        return md5_hash.hexdigest()

def leer_archivo():
    name_file = input("Ingresa el nombre del archivo a enviar: ")
    if os.path.exists(name_file):
        size_file = os.path.getsize(name_file)
        md5_hash = md5Hash(name_file)
        info_file = [md5_hash, name_file, size_file]
        return info_file
    else:
        return 0

def codificar_lista(lista: list) -> list:
    lista_aux=[]
    for element in lista:
        lista_aux.append(str(element).encode())
    return lista_aux


context = zmq.Context()
#  Socket to talk to server
print("Connecting to server...")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

name_client = identificar_cliente()

info_file = leer_archivo()

if info_file:
    info_file_code = codificar_lista(info_file)
    info_file_code.append(name_client.encode())
    print(info_file, info_file_code)

    with open(info_file[1], "rb") as f:
        contenido = f.read(4096)
        info_file_code.append(contenido)
        info_file_code.append("0".encode())
        while contenido:
            socket.send_multipart(info_file_code)
            mensaje = socket.recv().decode()
            if mensaje == "1":
                print("Ya existe un archivo con el contenido enviado")
                break
            elif mensaje == "2":
                print("El archivo se está enviando...")
                contenido = f.read(4096)
                info_file_code[4] = contenido
                info_file_code[5] = "2".encode()
            elif mensaje == "3":
                print("Se ha enviado todo el contenido ")
                break


    """socket.send_multipart()
    #se recibe la respuesta del server para saber si existe el archivo o no
    message = socket.recv().decode()
    if message == "1":
        print(f"Received reply result: Ya cuenta con un archivo con ese nombre")
    elif message == "0":
        print(f"Received reply result: Archivo recibido")
    elif message == " ":
        print("...")
        with open (name_file,"rb") as f:
            contenido = f.read(1024)
            while contenido:
                socket.send_multipart([bytes(name_client.encode()), bytes(name_file.encode()), contenido, bytes(str(size_file).encode()), bytes(dm5_hash.encode())])
                contenido=f.read(1024)
                message = socket.recv()
                if message.decode() == "0":
                    print(f"Received reply result: Archivo recibido")
                    break
                elif message.decode() == "1" :
                    print(f"Received reply result: Ya cuenta con un archivo con ese nombre")
                    break
        f.close()"""

else:
    print("Archivo no encontrado, por favor revise el nombre del archivo")
