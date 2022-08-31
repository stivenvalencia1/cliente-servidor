import time
import os
import zmq
import json

'''
" ": se esta enviando el archivo
0: Archivo recibido
1: Ya existe el archivo
'''
def leer_json(file_name):
    with open(file_name) as f:
        data = json.load(f)
    return data

def escribir_json(data, file_name):
    with open("server_data.json", "w") as newf:
        json.dump(data, newf, indent=3)

def iniciar_server():
    if os.path.exists("server_data.json"):
        data = leer_json("server_data.json")
        return data
    else:
        data = {}
        escribir_json(data, "server_data.json")
        return data




context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    #  Wait for next request from client
    #se lee el archivo que contiene los hash de documentos almacenados en server
    data_server = iniciar_server()
    info_file = socket.recv_multipart()
