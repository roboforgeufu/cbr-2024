#!/usr/bin/env pybricks-micropython

from pybricks.ev3devices import (
    Motor,
    TouchSensor,
    ColorSensor, # type: ignore
    InfraredSensor,
    UltrasonicSensor,
    GyroSensor,
)
from pybricks.parameters import Port, Stop, Direction, Button, Color  # type: ignore

from core.robot import Robot

robot = Robot(
    wheel_diameter = 10.5,
    wheel_distance = 5.5,
    l_wheel = Motor(Port.B),
    r_wheel = Motor(Port.C),
)

def main():

    robot.turn(90)
    print(robot.abs_wheels_angle())
    while True:
        robot.walk()

main()