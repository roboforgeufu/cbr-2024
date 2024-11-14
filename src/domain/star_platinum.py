#!/usr/bin/env pybricks-micropython
from core.robot import Robot
from pybricks.parameters import Stop, Color # type: ignore


def passenger_info(robot: Robot):
    passenger_lookup_table = {
        "CHILD": {
            Color.GREEN: [0, 13, 26],
            Color.BLUE: [4],
            Color.BROWN: [30],
            Color.WHITE: [],
            None: []
        },
        "ADULT": {
            Color.GREEN: [17],
            Color.BLUE: [28],
            Color.BROWN: [2],
            Color.RED: [15],
            Color.WHITE: [],
            None: []      
        },
    }
    color = robot.color_claw.color()
    if robot.ultra_head.distance() <= 100:
        height = "ADULT"
    else: height = "CHILD"

    return passenger_lookup_table[height][color]


def lift_claw(robot: Robot, side=1):
    robot.motor_elevate_claw.run_until_stalled(500 * side, Stop.HOLD)


def open_claw(robot: Robot, side=1):
    robot.motor_open_claw.run_until_stalled(500 * side, Stop.HOLD)


def main(robot: Robot):
    info = "None"
    while True:
        robot.ev3_print("Waiting request")
        request = robot.bluetooth.message(should_wait=True)
        robot.ev3_print(request, clear=True)
        if request == "UP":
            robot.ev3_print("Executing")
            lift_claw(robot)
            info = "Done!"
        elif request == "DOWN":
            robot.ev3_print("Executing")
            lift_claw(robot, -1)
            info = "Done!"
        elif request == "OPEN":
            robot.ev3_print("Executing")
            open_claw(robot, -1)
            info = "Done!"
        elif request == "CLOSE":
            robot.ev3_print("Executing")
            open_claw(robot)
            info = "Done!"
        elif request == "PASSENGER INFO":
            info = passenger_info(robot)
            
        robot.ev3_print(info)
        robot.bluetooth.message(info)


def star_platinum(robot: Robot, order: str):
    robot.ev3_print("Sending request", clear=True)
    robot.ev3_print(order)
    robot.bluetooth.message(order)
    info = robot.bluetooth.message(should_wait=True)
    robot.ev3_print(info)

    return info

