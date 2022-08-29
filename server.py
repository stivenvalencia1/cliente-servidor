import time
import os
import zmq
import json

'''
" ": se esta enviando el archivo
0: Archivo recibido
1: Ya existe el archivo
'''

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    #  Wait for next request from client
    #se lee el archivo que contiene los hash de documentos almacenados en server
    with open("files.json") as files:
        data = json.load(files)
    #ser recibe el mensaje del cliente con el hash del archivo
    info = socket.recv_multipart()
    md5_hash = info[0].decode()
    name_client = info[1].decode()
    name_file = info[2].decode()
    #se verifica que la llave exista en el diccionario
    if md5_hash in data.keys() :
        if name_client in data[md5_hash].keys():
            socket.send_string("1")
        else:
            data[md5_hash].update({name_client: name_file})
            with open("files.json", "w") as newfiles:
                json.dump(data, newfiles, indent=4)
            socket.send_string("0")
    else:
        socket.send_string(" ")
        #se recibe la informacion que va usar el cliente para crear el archivo por primera vez
        message = socket.recv_multipart()
        name_client1 = message[0].decode()
        name_file1 = message[1].decode()
        size_file1 = message[3].decode()
        dm5_hash1 = message[4].decode()

        with open(dm5_hash1,"ab") as f:
            f.write(message[2])
            f.close()

        while os.path.getsize(dm5_hash1) < int(size_file1):
            socket.send_string(" ")
            message = socket.recv_multipart()
            name_client1 = message[0].decode()
            name_file1 = message[1].decode()
            size_file1 = message[3].decode()
            dm5_hash1 = message[4].decode()

            with open(dm5_hash1,"ab") as f:
                f.write(message[2])
                f.close()

        socket.send_string("0")
        with open("files.json") as files1:
            data1 = json.load(files1)
        #data1[dm5_hash1]
        data1[dm5_hash1]={name_client1: name_file1}
        with open("files.json", "w") as newfiles:
            json.dump(data1, newfiles, indent=4)
        print(name_client+": Archivo recibido")
