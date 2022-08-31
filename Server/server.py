import time
import os
import zmq
import json

'''
" ": se esta enviando el archivo
0: Archivo recibido
1: Ya existe el archivo
'''

def iniciar_server():
    if os.path.exists("server_data.json"):
        with open("server_data.json") as f:
            data = json.load(f)
            print("data loaded")
        return data
    else:
        data = {}
        with open("server_data.json", "w") as newf:
            json.dump(data, newf, indent=3)
            print("data loaded")
        return data



context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    #  Wait for next request from client
    #se lee el archivo que contiene los hash de documentos almacenados en server
    data_server = iniciar_server()
    