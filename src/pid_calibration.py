#!/usr/bin/env pybricks-micropython
from pybricks.parameters import Port, Button  # type: ignore
from pybricks.ev3devices import ColorSensor  # type: ignore
from pybricks.tools import wait  # type: ignore
from pybricks.hubs import EV3Brick  # type: ignore

from core.robot import Robot
from core.utils import get_hostname, PIDControl, PIDValues
from core.decision_color_sensor import DecisionColorSensor
from core.display import screen, calibration_menu

import constants as const
from domain.localization import localization_routine
from domain.pathfinding import Graph, map_matrix, get_target_for_passenger
from domain.boarding import passenger_boarding, passenger_unboarding
from domain.path_control import path_control
from decision_trees.ht_nxt_color_v2_2 import ht_nxt_color_v2_p2_decision_tree
from decision_trees.lego_ev3_color_1 import levo_ev3_color_1_decision_tree
from decision_trees.sandy_lego_ev3_color_3 import sandy_lego_ev3_color_p3_decision_tree
from decision_trees.sandy_lego_ev3_color_4 import sandy_lego_ev3_color_p4_decision_tree

import json

robot = Robot(
    wheel_diameter=const.WHEEL_DIAMETER,
    wheel_distance=const.WHEEL_DIST,
    motor_r=Port.B,
    motor_l=Port.C,
    infra_side=Port.S1,
    ultra_feet=Port.S2,
    color_right=DecisionColorSensor(
        ColorSensor(Port.S3), sandy_lego_ev3_color_p3_decision_tree
    ),
    color_left=DecisionColorSensor(
        ColorSensor(Port.S4), sandy_lego_ev3_color_p4_decision_tree
    ),
)

def main():

    header = ["KP", "KI", "KD"]
    file_name = "pid_const.json"

    while True:

        selected_options, showed_data = calibration_menu(file_name, header, robot, clear=True)
        selected_function, kp, ki, kd = selected_options

        values = [kp, ki, kd]

        screen(showed_data, "RUNNING", selected=None, clear=True, robot=robot)

        while robot.ev3.buttons.pressed() == []:
            if selected_function == "align":
                robot.align(pid = PIDValues(kp, ki, kd))
            elif selected_function == "walk":
                robot.pid_walk(100, pid = PIDValues(kp, ki, kd))
            elif selected_function == "turn":
                robot.pid_turn(90, pid = PIDValues(kp, ki, kd))
            elif selected_function == "line_follower":
                robot.line_follower(50, side = "R", pid = PIDControl(PIDValues(kp, ki, kd)))

        robot.stop()

        screen(showed_data, "Save parameters?", selected=None, clear=True, robot=robot)

        button = robot.wait_button([Button.UP, Button.DOWN, Button.CENTER, Button.LEFT, Button.RIGHT])
        
        if button == Button.CENTER:
            screen(showed_data, "Saved!", selected=None, clear=True, robot=robot)
            with open(file_name, "r") as file:
                data = json.load(file)
            data[robot.name][selected_function] = values
            print(data)
            with open(file_name, "w") as file:
                json.dump(data, file, indent=4)
                
            robot.wait_button([Button.UP, Button.DOWN, Button.CENTER, Button.LEFT, Button.RIGHT])
        else:
            screen(showed_data, "Not saved!", selected=None, clear=True, robot=robot)

main()