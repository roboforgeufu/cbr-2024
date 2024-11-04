#!/usr/bin/env pybricks-micropython

from pybricks.tools import wait # type: ignore
from core.network import Wifi, Bluetooth
from core.robot import Robot
from core.encoding import encoder, decoder

# OBJETOS
robot = Robot(font=("Helvetica", 15, True))

# DEFINE SERVIDOR
is_server = robot.get_hostname() == "ev3server"

# INICIA
robot.ev3.speaker.beep()

print(robot.get_hostname())

wifi = Wifi()
bt = Bluetooth(is_server=is_server)

# ESPERANDO CONEXÃO WIFI
if is_server:

    robot.ev3_print("ESPERANDO WIFI")
    # robot.ev3_print("ESPERANDO WIFI")

    wifi.start()
    robot.ev3_print("WIFI\nINICIADO!", clear=True)

robot.ev3_print("ESPERANDO\nBLUETOOTH")
bluetooth_status = bt.start()

robot.ev3_print(bluetooth_status, clear=True)
wait(2000)
robot.ev3.screen.clear()
if is_server:
    char = ""
    message = ""
    while True:
        char = wifi.message()
        if char == "enter":
            break
        elif char == "backspace":
            robot.ev3_print(message, clear=True)
        elif char == "space":
            robot.ev3_print(" ", end="")
        else:
            robot.ev3_print(char, end="")
            message = message + char
    bt.message(message)
else:
    message = bt.message()
    robot.ev3_print(message)

print("Normal:" + str(message))
print("Codificado:" + str(encoder(message)))

while True:
    wait(10000)
