import time
import os
import zmq
import json

'''
0: primer mensaje de un cliente.
1: Ya existe el archivo.
2: estoy recibiendo un archivo.
3: he recibido un archivo completo.
'''
def leer_json(file_name):
    with open(file_name) as f:
        data = json.load(f)
    return data

def escribir_json(data, file_name):
    with open(file_name, "w") as newf:
        json.dump(data, newf, indent=3)

def iniciar_server():
    if os.path.exists("server_data.json"):
        data = leer_json("server_data.json")
        print("Data Loaded")
        return data
    else:
        data = {}
        escribir_json(data, "server_data.json")
        print("Data Loaded")
        return data




context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    #  Wait for next request from client
    #se lee el archivo que contiene los hash de documentos almacenados en server
    data_server = iniciar_server()
    info_file = socket.recv_multipart()
    print("recibieno alguna info")
    md5hash = info_file[0].decode()
    file_name = info_file[1].decode()
    file_size = info_file[2].decode()
    client = info_file[3].decode()
    content = info_file[4]
    status = info_file[5].decode()
    if status == "0":
        if md5hash in data_server.keys():
            if client in data_server[md5hash].keys():
                socket.send_string("1")
            else:
                data_server[md5hash].update({client: file_name})
                escribir_json(data_server, "server_data.json")
                socket.send_string("3")
        else:
            data_server.update({md5hash: {client: file_name}})
            escribir_json(data_server, "server_data.json")
            socket.send_string("2")
    elif status == "2":
        if os.path.exists(md5hash):
            if os.path.getsize(md5hash) < int(file_size):
                with open(md5hash, "ab") as f:
                    f.write(content)
                    f.close()
                socket.send_string("2")
            else:
                socket.send_string("3")
        else:
            with open(md5hash, "ab") as f:
                f.write(content)
                f.close()
            socket.send_string("2")

