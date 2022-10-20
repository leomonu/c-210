import socket
from  threading import Thread
import time
IP_ADDRESS = '127.0.0.1'
PORT = 8080
SERVER = None
clients = {}

BUFFER_SIZE = 4096

def disconnectclient(msg,client,client_name):
    global clients
    enterClientName=msg[11:].strip()

    if(enterClientName in clients):
        clients[enterClientName]["connected_with"]=""
        clients[client_name]["connected_with"]=""
        other_client_sockets=clients[enterClientName]["clients"]
        greeting=f"Hello {enterClientName} ur are successfully disconnected with {client_name}"
        other_client_sockets.send(greeting.encode())

        msg=f"Your successfully disconnected with {enterClientName}"
        client.send(msg.encode())


def connectclient(msg,client,client_name):
    global clients

    entered_client_name = msg[8:].strip()
    if(entered_client_name in clients):
        if(not clients[client_name]["connected_with"]):
            clients[entered_client_name]["connected_with"] = client_name
            clients[client_name]["connected_with"]  = entered_client_name

            other_client_socket = clients[entered_client_name]["client"]

            greet_message = f"Hello, {entered_client_name} {client_name} connected with you !!!"
            other_client_socket.send(greet_message.encode())

            msg = f"You are successfully connected with {entered_client_name}"
            client.send(msg.encode())
        else:
            other_client_name = clients[client_name]["connected_with"]
            msg = f"You are already connected with {other_client_name}"
            client.send(msg.encode())


def handleShowList(client):
    global clients
    counter = 0
    for c in clients:
        counter+=1
    
    client_addr=clients[c]["address"][0]
    connected_with=client[c]["connected_with"]
    msg=""
    if connected_with:
        msg=f"{counter},{c},{client_addr},Connected With{connected_with},tiul,\n"
    
    else :
        msg=f"{counter},{c},{client_addr},Available,tiul,\n"
    
    client.send(msg.encode('utf-8'))
    time.sleep(1)





def handleMessges(client, message, client_name):
    if(message == 'show list'):
        handleShowList(client)
    elif message[:7] == "connect":
        connectclient(message,client,client_name)
    elif message[:10] == "disconnect":
        disconnectclient(message,client,client_name)
    



def handleClient(client, client_name):
    global clients
    global BUFFER_SIZE
    global SERVER


    banner1 = "Welcome, You are now connected to Server!\nClick on Refresh to see all available users.\nSelect the user and click on Connect to start chatting."
    client.send(banner1.encode())

    while True:
        try:
            BUFFER_SIZE = clients[client_name]["file_size"]
            chunk = client.recv(BUFFER_SIZE)
            message = chunk.decode().strip().lower()
            if(message):
                handleMessges(client, message, client_name)
            else:
                removeClient(client_name)
        except:
            pass

def removeClient():
    pass


def acceptConnections():
    global SERVER
    global clients

    while True:
        client, addr = SERVER.accept()
        print(client,addr)

        client_name = client.recv(4096).decode().lower()
        clients[client_name] = {
                "client"         : client,
                "address"        : addr,
                "connected_with" : "",
                "file_name"      : "",
                "file_size"      : 4096
            }

        print(f"Connection established with {client_name} : {addr}")

        thread = Thread(target = handleClient, args=(client,client_name,))
        thread.start()

def setup():
    print("\n\t\t\t\t\t\tIP MESSENGER\n")


    global PORT
    global IP_ADDRESS
    global SERVER


    SERVER  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.bind((IP_ADDRESS, PORT))


    SERVER.listen(100)

    print("\t\t\t\tSERVER IS WAITING FOR INCOMMING CONNECTIONS...")
    print("\n")

    acceptConnections()



setup_thread = Thread(target=setup)          
setup_thread.start()