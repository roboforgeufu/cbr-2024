#!/usr/bin/env pybricks-micropython
from core.robot import Robot
from pybricks.parameters import Port # type: ignore

def color_check(robot: Robot):
    color=robot.color_claw.color()
    return color

def height_check(robot: Robot):
    adult=robot.ultra_head.distance()<=100 
    return adult

def lift_claw(robot: Robot, side=1):
    robot.motor_elevate_claw.run_target(40*side,200)
    robot.motor_elevate_claw.hold()

def open_claw(robot: Robot, side=1):
    robot.motor_open_claw.run_target(69*side,200)

def main(robot: Robot):
    while True:
        request = robot.bluetooth.message()
        if request == "SUPLEX":
            lift_claw(robot)
        elif request == "HAMMER":
            lift_claw(robot,-1)
        elif request == "DROP":
            open_claw(robot)
        elif request == "GRAB":
            open_claw(robot, -1)
        elif request == "PASSENGER INFO":
            color = color_check()
            adult = height_check()
            robot.bluetooth.message(adult,str(color))

def star_platinum(robot: Robot, order: str):
    robot.bluetooth.message()