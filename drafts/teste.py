#!/usr/bin/env pybricks-micropython

from core.network import Bluetooth
from core.robot import Robot
from core.utils import get_hostname
from pybricks.ev3devices import (
    Motor,
    TouchSensor,
    ColorSensor,  # type: ignore
    InfraredSensor,
    UltrasonicSensor,
    GyroSensor,
)
from pybricks.iodevices import Ev3devSensor  # type: ignore
from pybricks.parameters import Port, Stop, Direction, Button, Color  # type: ignore

robot = Robot()
is_server = get_hostname() == "ev3server"

if is_server:
    hitech = Ev3devSensor(Port.S1)
bt = Bluetooth(is_server)

robot.ev3.speaker.beep()
bt.start()
robot.ev3.speaker.beep()

while True:
    if is_server:
        color = hitech.read("NORM")
        bt.message(color)
    else:
        color = bt.message()
        robot.ev3_print(color, clear=True, font='Lucida', size=18, bold=True)