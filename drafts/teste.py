#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick  # type: ignore
from pybricks.ev3devices import (
    Motor,
    TouchSensor,
    ColorSensor,  # type: ignore
    InfraredSensor,
    UltrasonicSensor,
    GyroSensor,
)
from pybricks.messaging import BluetoothMailboxClient, BluetoothMailboxServer, TextMailbox  # type: ignore
from pybricks.parameters import Port, Stop, Direction, Button, Color  # type: ignore
from pybricks.tools import wait, StopWatch, DataLog  # type: ignore
from pybricks.robotics import DriveBase  # type: ignore
from pybricks.media.ev3dev import SoundFile, ImageFile  # type: ignore

from core.network import Network
from core.robot import Robot
from core.encoding import encoder, decoder

# OBJETOS
ev3 = EV3Brick()
robot = Robot()

# DEFINE SERVIDOR
is_server = robot.get_hostname() == "ev3server"

# INICIA
ev3.speaker.beep()

print(robot.get_hostname())

net = Network(ev3, is_server)

# ESPERANDO CONEXÃO WIFI
if is_server:
    
    robot.ev3_print("ESPERANDO WIFI")

    client, addr = net.wifi_start()

    ev3.screen.clear()
    robot.ev3_print('WIFI\nINICIADO!')

robot.ev3_print("ESPERANDO BLUETOOTH")
bluetooth_status = net.bluetooth_start()

ev3.screen.clear()
robot.ev3_print(bluetooth_status)
wait(2000)
ev3.screen.clear()
if is_server:
    char = ''
    message = ''
    while char != "enter":
        char = net.wifi_message(client)
        if char == "backspace":
            ev3.screen.clear()
            robot.ev3_print(message)
        else:
            robot.ev3_print(char, end='')
            message = message + net.wifi_message(client)
    net.bluetooth_message(message)
else:
    message = net.bluetooth_message()
    robot.ev3_print(message)

print('Normal:' + str(message))
print('Codificado:' + str(encoder(message)))

while True: wait(10000)