#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick # type: ignore
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, # type: ignore
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.messaging import (BluetoothMailboxClient, BluetoothMailboxServer, TextMailbox) # type: ignore
from pybricks.parameters import Port, Stop, Direction, Button, Color # type: ignore
from pybricks.tools import wait, StopWatch, DataLog # type: ignore
from pybricks.robotics import DriveBase # type: ignore
from pybricks.media.ev3dev import SoundFile, ImageFile # type: ignore

from core.network import Network

ev3 = EV3Brick

def check_server():
    while True:
        if ev3.buttons.pressed() != None:
            if ev3.buttons.pressed() != ev3.buttons.pressed([Button.CENTER]):
                return True
                break
            else:
                return False
                break
        else:
            ev3.screen.clear()
            ev3.screen.print('FOR SERVER PRESS CENTER')

is_server = check_server()

network = Network(EV3Brick, is_server)

status = network.bluetooth_start()

ev3.screen.print(status)
    