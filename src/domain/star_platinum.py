#!/usr/bin/env pybricks-micropython
from core.robot import Robot
from pybricks.parameters import Stop # type: ignore


def passenger_read_color_and_type(robot: Robot):
    color = robot.color_claw.color()
    adult = robot.ultra_head.distance() <= 100
    return adult, color


def lift_claw(robot: Robot, side=1):
    robot.motor_elevate_claw.run_until_stalled(200 * side, Stop.HOLD, 40)
    robot.motor_elevate_claw.hold()


def open_claw(robot: Robot, side=1):
    robot.motor_open_claw.run_until_stalled(100 * side, Stop.HOLD, 50)


def main(robot: Robot):
    while True:
        robot.ev3_print("Waiting request")
        request = robot.bluetooth.message(should_wait=True)
        robot.ev3_print(request, clear=True)
        if request == "SUPLEX":
            lift_claw(robot)
        elif request == "DOWN":
            robot.ev3_print("Executing")
            lift_claw(robot, -1)
        elif request == "OPEN":
            open_claw(robot, -1)
        elif request == "CLOSE":
            open_claw(robot)
        elif request == "PASSENGER INFO":
            adult, color = passenger_read_color_and_type(robot)
            robot.bluetooth.message((adult, str(color)))
        robot.ev3_print("Done!")
        robot.bluetooth.message("Done!")


def star_platinum(robot: Robot, order: str):
    robot.ev3_print("Sending request", clear=True)
    robot.ev3_print(order)
    robot.bluetooth.message(order)
    robot.ev3_print(robot.bluetooth.message(should_wait=True))
