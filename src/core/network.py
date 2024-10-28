#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick  # type: ignore
from pybricks.messaging import BluetoothMailboxClient, BluetoothMailboxServer, TextMailbox  # type: ignore
from pybricks.tools import wait

import socket

from core.encoding import encoder, decoder
from core.utils import get_hostname

"""
Módulo central de comunicação do EV3.

Devem estar nesse módulo:
    - Classe 'Network', com métodos e atributos para a comunicação entre dois dispositivos (bricks ou computadores)

Não devem estar nesse módulo:
    - Código específico de algum problema/desafio
    - Métodos de codificação
"""


class Wifi:

    #
    #   Conexão WIFI Ev3 com computador
    #

    def __init__(self, ev3=EV3Brick()):

        self.ev3 = ev3
        self.wifi = socket.socket()

    def start(self):

        # Inicia a conexão WIFI (Servidor)
        port = 12345
        self.wifi.bind(("", port))
        self.wifi.listen(5)
        self.client, self.addr = self.wifi.accept()
        self.ev3.speaker.beep()
        wait(500)

    def message(self, message=None):

        # Envia ou recebe um pacote do computador
        if message != None:
            self.client.send(message.encode())  # Codifica mensagem em bytes

        else:
            recv_message = self.client.recv(
                1024
            ).decode()  # Decodifica bytes em mensagem
            return recv_message

    def end(self):

        # Encerra conexão com o computador
        message = "end"
        self.client.send(message.encode())
        self.client.close()
        wait(500)


class Bluetooth:

    #
    # Conexão bluetooth EV3 com EV3
    #

    def __init__(self, ev3: EV3Brick, server_name="ev3server"):

        self.ev3 = ev3
        self.is_server = get_hostname()
        self.server_name = server_name

        if self.is_server:
            self.bluetooth = BluetoothMailboxServer()
        else:
            self.bluetooth = BluetoothMailboxClient()

    def start(self):

        # Inicia a conexão bluetooth (Servidor ou cliente)
        if self.is_server:
            # Inicia o servidor
            self.bluetooth.wait_for_connection()
            return "SERVER START!"

        else:
            # Inicia o cliente
            self.bluetooth.connect("ev3server")
            return "CLIENT START!"

    def message(
        self, message=None, channel="Main", delay=0
    ):  # Envia ou recebe uma mensagem (no canal principal por padrão)

        # Método de comunicação do Ev3 que envia ou recebe apenas strings
        mbox = TextMailbox(channel, self.bluetooth)

        if message != None:

            # Se tiver alguma mensagem como argumento, envia a mensagem
            encoded_message = encoder(message)
            wait(delay)  # Codifica mensagem em formato personalizado (string)
            mbox.send(encoded_message)
            return "Mensagem enviada!"

        else:

            # Se não tiver mensagem como argumento, retorna uma mensagem recebida e o assunto (canal)
            mbox.wait()
            recv_message = decoder(
                mbox.read()
            )  # Decodifica string personalizado em mensagem
            return recv_message

    def end(self):

        self.bluetooth.close()
