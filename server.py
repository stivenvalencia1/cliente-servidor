import time
import os
import zmq

'''
0: Archivo recibido
1: Ya existe el archivo
'''

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    #  Wait for next request from client
    message = socket.recv_multipart()
    name_client=message[0].decode()
    name_file=message[1].decode()
    if os.path.exists(name_client+"/"+name_file) and os.path.getsize(name_client+"/"+name_file) == int(message[3].decode()):
            socket.send_string("1")
    else:
        if os.path.exists(name_client):
            f=open(name_client+"/"+name_file,"ab")
        else:
            os.mkdir(name_client)
            f=open(name_client+"/"+name_file,"ab")
        f.write(message[2])
        f.close()
        if os.path.getsize(name_client+"/"+name_file) == int(message[3].decode()):
            socket.send_string("0")
            print(name_client+": Archivo recibido")
        else:
            socket.send_string(" ")
