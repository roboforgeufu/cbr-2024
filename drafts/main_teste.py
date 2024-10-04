#!/usr/bin/env pybricks-micropython

from pybricks.ev3devices import (
    Motor,
    TouchSensor,
    ColorSensor, 
    
    InfraredSensor,
    UltrasonicSensor,
    GyroSensor,
)

from core.robot import Robot

robot = Robot(
    wheel_diameter = 10.5
    wheel_distance = 5.5
    l_wheel = Motor(Port.B)
    r_wheel = Motor(Port.C)
)

def main():

    robot.turn(90)
    robot.walk()

main()