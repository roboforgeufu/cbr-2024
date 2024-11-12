#!/usr/bin/env pybricks-micropython
from core.robot import Robot
from pybricks.parameters import Stop, Color # type: ignore


def passenger_info(robot: Robot):
    passenger_lookup_table = {
        "CHILD": {
            Color.GREEN: [0, 13, 26],
            Color.BLUE: [4],
            Color.BROWN: [30],
            Color.WHITE: []
        },
        "ADULT": {
            Color.GREEN: [17],
            Color.BLUE: [28],
            Color.BROWN: [2],
            Color.RED: [15],
            Color.WHITE: []
        },
    }
    color = robot.color_claw.color()
    if robot.ultra_head.distance() <= 100:
        height = "ADULT"
    else: height = "CHILD"

    return passenger_lookup_table[height][color]


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
        if request == "UP":
            robot.ev3_print("Executing")
            lift_claw(robot)
        elif request == "DOWN":
            robot.ev3_print("Executing")
            lift_claw(robot, -1)
        elif request == "OPEN":
            robot.ev3_print("Executing")
            open_claw(robot, -1)
        elif request == "CLOSE":
            robot.ev3_print("Executing")
            open_claw(robot)
        elif request == "PASSENGER INFO":
            info = passenger_info(robot)
            robot.bluetooth.message(info)
        robot.ev3_print("Done!")
        robot.bluetooth.message("Done!")


def star_platinum(robot: Robot, order: str):
    robot.ev3_print("Sending request", clear=True)
    robot.ev3_print(order)
    robot.bluetooth.message(order)
    robot.ev3_print(robot.bluetooth.message(should_wait=True))
