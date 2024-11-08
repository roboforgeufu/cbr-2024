#!/usr/bin/env pybricks-micropython
from pybricks.parameters import Port, Button  # type: ignore
from pybricks.ev3devices import ColorSensor  # type: ignore
from pybricks.tools import wait  # type: ignore
from pybricks.hubs import EV3Brick  # type: ignore

from core.robot import Robot
from core.utils import get_hostname, PIDControl, PIDValues
from core.decision_color_sensor import DecisionColorSensor

import constants as const
from domain.localization import localization_routine
from domain.pathfinding import Graph, map_matrix, get_target_for_passenger
from domain.boarding import passenger_boarding, passenger_unboarding
from domain.path_control import path_control
from decision_trees.ht_nxt_color_v2_2 import ht_nxt_color_v2_p2_decision_tree
from decision_trees.lego_ev3_color_1 import levo_ev3_color_1_decision_tree
from decision_trees.sandy_lego_ev3_color_3 import lego_ev3_color_p3_decision_tree
from decision_trees.sandy_lego_ev3_color_4 import lego_ev3_color_p4_decision_tree

r = Robot(
    wheel_diameter=const.WHEEL_DIAMETER,
    wheel_distance=const.WHEEL_DIST,
    motor_r=Port.B,
    motor_l=Port.C,
    infra_side=Port.S1,
    ultra_feet=Port.S2,
    color_right=DecisionColorSensor(
        ColorSensor(Port.S3), lego_ev3_color_p3_decision_tree
    ),
    color_left=DecisionColorSensor(
        ColorSensor(Port.S4), lego_ev3_color_p4_decision_tree
    ),
)

'''def display(pid, functions, i, j):
    if i == 0:
        r.ev3_print("KP: " + str(round(pid[0], 1)), background=True)
        r.ev3_print("KD: " + str(round(pid[1], 1)), line=1)
        r.ev3_print("KI: " + str(round(pid[2], 2)), line=2)
        r.ev3_print(functions[j], line=3)
    elif i == 1:
        r.ev3_print("KP: " + str(round(pid[0], 1)), draw = True)
        r.ev3_print("KD: " + str(round(pid[1], 1)), line=1, background=True)
        r.ev3_print("KI: " + str(round(pid[2], 2)), line=2)
        r.ev3_print(functions[j], line=3)
    elif i == 2:
        r.ev3_print("KP: " + str(round(pid[0], 1)), draw = True)
        r.ev3_print("KD: " + str(round(pid[1], 1)), line=1)
        r.ev3_print("KI: " + str(round(pid[2], 2)), line=2, background=True)
        r.ev3_print(functions[j], line=3)
    elif i == 3:
        r.ev3_print("KP: " + str(round(pid[0], 1)), draw = True)
        r.ev3_print("KD: " + str(round(pid[1], 1)), line=1)
        r.ev3_print("KI: " + str(round(pid[2], 2)), line=2)
        r.ev3_print(functions[j], line=3, background=True)
    else:
        r.ev3_print("KP: " + str(round(pid[0], 1)), draw = True)
        r.ev3_print("KD: " + str(round(pid[1], 1)), line=1)
        r.ev3_print("KI: " + str(round(pid[2], 2)), line=2)
        r.ev3_print(functions[j], line=3)'''

ev3 = EV3Brick()

BEEP = 0

def display(*options, selected=None, error:str=None, clear=False):
    lines = len(options)
    if clear: r.ev3.screen.clear()
    for line in range(lines-1):
        r.ev3_draw(options[line], background=selected==line, line=line)
    if error is not None: r.ev3_draw(*error, line=lines)


def main():
    values = [0, 0, 0]
    header = ["KP:", "KD:", "KI:"]
    while True:
        error = False
        functions = ["align", "walk", "turn", "line_follower"]
        selected = 0
        while selected < len(header):

            options = [str(x) + ' ' + str(y) for x, y in zip(header, values)]

            display(options, selected = selected, error = "Maior que zero", clear=clear)

            clear = False

            button = r.wait_button(
                [Button.UP, Button.DOWN, Button.LEFT, Button.RIGHT, Button.CENTER],
                beep=BEEP,
            )
            if button == Button.UP:
                values[selected] += 0.1
            elif button == Button.DOWN:
                values[selected] -= 0.1
            elif button == Button.RIGHT:
                values[selected] += 1
            elif button == Button.LEFT:
                values[selected] -= 1
            elif button == Button.CENTER:
                selected += 1
                clear = True
            
            if error:
                error = False
                clear = True

            if values[selected] < 0:
                values[selected] = 0
                error = True

            wait(100)

        r.ev3.screen.clear()
        function = 0


        while True:
            display(options, selected = None, clear=True)
            r.ev3_draw(functions[function], background=True, line=3)
            button = r.wait_button(
                [Button.LEFT, Button.RIGHT, Button.CENTER], beep=BEEP
            )

            if button == Button.RIGHT or button == Button.DOWN:
                function += 1
            elif button == Button.LEFT or button == Button.UP:
                function -= 1
            else:
                wait(100)
                break

            if function == len(functions):
                function = 0
            elif function < 0:
                function = len(functions) - 1

        ev3.screen.clear()
        wait(2000)

        display(options, selected = None)
        r.ev3_draw(functions[function], background=False, line=3)

        kp, kd, ki = values

        pid = PIDControl(PIDValues(kp, ki, kd))

        if functions[function] == "align":
            r.align(pid = pid)
        elif functions[function] == "walk":
            r.pid_walk(100, pid = pid)
        elif functions[function] == "turn":
            r.pid_turn(90, pid = pid)
        elif functions[function] == "line_follower":
            r.line_follower(50, side = "R", pid = pid)


main()