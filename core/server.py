#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick # type: ignore
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, # type: ignore
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.messaging import (BluetoothMailboxClient, BluetoothMailboxServer, # type: ignore
                                NumericMailbox, TextMailbox, LogicMailbox)
from pybricks.parameters import Port, Stop, Direction, Button, Color # type: ignore
from pybricks.tools import wait, StopWatch, DataLog # type: ignore
from pybricks.robotics import DriveBase # type: ignore
from pybricks.media.ev3dev import SoundFile, ImageFile # type: ignore

import socket

class Server:
    
    def _init_(self, ev3):

        self.ev3 = ev3
        self.server = BluetoothMailboxServer()
        self.client = BluetoothMailboxClient()

    #
    #   Conexão WIFI Ev3 com computador (Debug)
    #

    def wifi_start(self):

        # Inicia a conexão wifi (Servidor)
        client_connection = socket.socket()
        port = 12345
        client_connection.bind(("", port))
        client_connection.listen(5)
        print("Waiting for connection...")
        self.ev3.speaker.beep()
        self.ev3.screen.print("Waiting for connection")
        self.ev3.screen.print("    with computer...")
        client, addr = client_connection.accept()
        self.ev3.screen.clear()
        self.ev3.screen.print("Connection successful!")
        self.ev3.speaker.beep()
        wait(500)

        return client, addr
    
    def wifi_message(self, client, message):

        # Envia e recebe um pacote para o cliente
        message = ",".join(map(str, message))
        client.send(message.encode())
        recv_message = str(client.recv(1024).decode())

        return recv_message
    
    def wifi_end(self, client):

        message = "end"
        client.send(message.encode())
        self.ev3.screen.clear()
        self.ev3.screen.print("Server: ")
        self.ev3.screen.print(str(client.recv(1024).decode()))
        client.close()
        wait(700)
        self.ev3.screen.clear()
        self.ev3.screen.print("Connection ended!")
        wait(1000)

    #
    # Conexão bluetooth EV3 com EV3
    #

    def bluetooth_start(self, is_server=False):
        
        # Inicia a conexão bluetooth (Servidor ou cliente)
        if is_server:
            # Inicia o servidor
            self.server.wait_for_connection(5)

        else:
            # Inicia o cliente
            self.client.connect()

    def bluetooth_message(self,connection,message=None,channel="Main"): # Envia ou recebe uma mensagem (No canal principal por padrão)

        # Checa o tipo da mensagem
        if isinstance(message,(float,int)): mbox = NumericMailbox(channel,connection) 
        elif isinstance(message,str): mbox = TextMailbox(channel,connection)
        elif isinstance(message,bool): mbox = LogicMailbox(channel,connection)
        elif isinstance(message,(list,tuple)):
            # Converte a lista em uma string
            message = ",".join(map(str, message))
            mbox = TextMailbox("Mailbox", connection)
            
        if message==None:

        # Se não tiver mensagem como argumento, retorna uma mensagem recebida e o assunto (canal)
            mbox.wait()
            return mbox.read(), channel
        
        else:

            # Se tiver mensagem como argumento, envia uma mensagem
            mbox.send(message)


    def bluetooth_end(self, is_server=False):

        # Encerra a conexão
        if is_server:
            self.server.close()
        
        else:
            self.client.close()