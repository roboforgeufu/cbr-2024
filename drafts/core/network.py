#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick # type: ignore
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, # type: ignore
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.messaging import (BluetoothMailboxClient, BluetoothMailboxServer, TextMailbox) # type: ignore
from pybricks.parameters import Port, Stop, Direction, Button, Color # type: ignore
from pybricks.tools import wait, StopWatch, DataLog # type: ignore
from pybricks.robotics import DriveBase # type: ignore
from pybricks.media.ev3dev import SoundFile, ImageFile # type: ignore

import socket

from encoding import encoder, decoder
"""
Módulo central de comunicação.

Devem estar nesse módulo:
    - Classe 'Network', com métodos e atributos para a comunicação entre dois dispositivos (bricks ou computadores)

Não devem estar nesse módulo:
    - Código específico de algum problema/desafio
    - Métodos de codificação
"""

class Network:
    
    def __init__(self, ev3):

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
        message = enconding.encoder(message)
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

    def bluetooth_message(self, connection, message=None, channel="Main"): # Envia ou recebe uma mensagem
                                                                           # (No canal principal por padrão)
        # Função do Ev3 que envia ou recebe apenas strings
        mbox = TextMailbox(connection, channel)

        if message==None:

        # Se não tiver mensagem como argumento, retorna uma mensagem recebida e o assunto (canal)
            mbox.wait()
            message_tuple = decoder(mbox.read())
            return recv_message
        
        else:
            
            # Se tiver mensagem como argumento, envia a mensagem
            encoded_message = encoder(message)
            mbox.send(encoded_message)


    def bluetooth_end(self, is_server=False):

        # Encerra a conexão
        if is_server:
            self.server.close()
        
        else:
            self.client.close()