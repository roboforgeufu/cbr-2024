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

from core.encoding import encoder, decoder
"""
Módulo central de comunicação.

Devem estar nesse módulo:
    - Classe 'Network', com métodos e atributos para a comunicação entre dois dispositivos (bricks ou computadores)

Não devem estar nesse módulo:
    - Código específico de algum problema/desafio
    - Métodos de codificação
"""

class Network:
    
    def __init__(self, ev3 = EV3Brick(), is_server=False):

        self.ev3 = ev3
        self.is_server = is_server
        self.wifi = socket.socket()

        if self.is_server:
            self.bluetooth = BluetoothMailboxServer()
        else:
            self.bluetooth = BluetoothMailboxClient()

    #
    #   Conexão WIFI Ev3 com computador (Debug)
    #

    def wifi_start(self):

        # Inicia a conexão wifi (Servidor)
        port = 12345
        self.wifi.bind(("", port))
        self.wifi.listen(5)
        client, addr = self.wifi.accept()
        self.ev3.speaker.beep()
        wait(500)

        return client, addr
                            
    def wifi_message(self, client, message=None):
        
        # Envia ou recebe um pacote do cliente

        if message != None:
            client.send(message.encode()) # Codifica mensagem em bytes

        else:
            recv_message = client.recv(1024).decode() # Decodifica bytes em mensagem
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

    def bluetooth_start(self):
        
        # Inicia a conexão bluetooth (Servidor ou cliente)
        if self.is_server:
            # Inicia o servidor
            self.bluetooth.wait_for_connection()
            return "SERVER START!"       

        else:
            # Inicia o cliente
            self.bluetooth.connect("ev3server")
            return "CLIENT START!"

    def bluetooth_message(self, message=None, channel="Main"):  # Envia ou recebe uma mensagem (no canal principal por padrão)

        # Método de comunicação do Ev3 que envia ou recebe apenas strings
        mbox = TextMailbox(channel, self.bluetooth)

        if message!=None:

            # Se tiver alguma mensagem como argumento, envia a mensagem
            encoded_message = encoder(message) # Codifica mensagem em formato personalizado (string)
            mbox.send(encoded_message)
            return "Mensagem enviada!"

        else:
            
            # Se não tiver mensagem como argumento, retorna uma mensagem recebida e o assunto (canal)
            mbox.wait()
            recv_message = decoder(mbox.read()) # Decodifica string personalizado em mensagem
            return recv_message

    def bluetooth_end(self):
    
        self.bluetooth.close()