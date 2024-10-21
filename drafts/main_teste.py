#!/usr/bin/env pybricks-micropython

from core.robot import Robot
from pybricks.ev3devices import ColorSensor  # type: ignore
from pybricks.ev3devices import (
    GyroSensor,
    InfraredSensor,
    Motor,
    TouchSensor,
    UltrasonicSensor,
)
from pybricks.iodevices import Ev3devSensor
from pybricks.parameters import Button, Color, Direction, Port, Stop  # type: ignore

robot = Robot(
    wheel_diameter=10.5,
    wheel_distance=5.5,
    l_wheel=Motor(Port.B),
    r_wheel=Motor(Port.C),
)


def main():
    hitechnic = Ev3devSensor(Port.S1)
    flag = True
    while True:
                color = hitechnic.read("NORM")
        if sum(color[:3]) != 0:
            robot.ev3.speaker.beep()
            robot.ev3_print(color, clear=True)

            flag = True

        if sum(color[:3]) == 0 and flag:
            robot.ev3_print("======", clear=True)
            flag = False

        robot.walk(150)


main()
