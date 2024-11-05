#!/usr/bin/env pybricks-micropython

from core.omni_robot import OmniRobot, Direction
from core.utils import get_hostname
from core.decision_color_sensor import DecisionColorSensor

from pybricks.parameters import Port, Button
from pybricks.ev3devices import ColorSensor
from pybricks.iodevices import Ev3devSensor

from decision_trees.lilo_lego_ev3_color_1 import lilo_lego_ev3_color_p1_decision_tree
from decision_trees.lilo_lego_ev3_color_2 import lilo_lego_ev3_color_p2_decision_tree
from decision_trees.lilo_lego_ev3_color_3 import lilo_lego_ev3_color_p3_decision_tree
from decision_trees.lilo_lego_ev3_color_4 import lilo_lego_ev3_color_p4_decision_tree
from decision_trees.ht_nxt_color_v2_2 import ht_nxt_color_v2_p2_decision_tree

from domain.pathfinding import Graph, map_matrix, get_target_for_passenger

from domain.ohana import (
    open_claw,
    close_claw,
    lower_claw,
    raise_claw,
    mid_claw,
    transmit_signal,
)

from domain.omni_path_control import omni_path_control


def lilo_main(lilo: OmniRobot):
    lilo.bluetooth.start()

    # Inicialização do mapa
    map_graph = Graph(map_matrix)

    #
    # Localização inicial
    #

    while True:
        #
        # Coleta de passageiros
        #

        #
        # Pathfinding e movimentação (obstáculos)
        #

        #
        # Desembarque de passageiros
        #

        #
        # Retorno a zona de embarque
        #
        pass


def test_navigation_lilo(lilo: OmniRobot):
    # lilo.bluetooth.start()
    map_graph = Graph(map_matrix)

    lilo.ev3_print("Press initial robot orientation:")
    pressed = lilo.wait_button([Button.UP, Button.LEFT, Button.RIGHT, Button.DOWN])
    button_to_direction = {
        Button.UP: "N",
        Button.LEFT: "O",
        Button.RIGHT: "L",
        Button.DOWN: "S",
    }
    lilo.orientation = button_to_direction[pressed]

    map_graph.mark_obstacle("V10")
    map_graph.mark_obstacle("V21")
    path, _, directions = map_graph.dijkstra(5, 26)
    omni_path_control(lilo, path, directions)

    lilo.wait_button()
    path, _, directions = map_graph.dijkstra(27, 6)
    omni_path_control(lilo, path, directions)


def test_bt_lilo(lilo: OmniRobot):
    lilo.bluetooth.start()
    while True:
        lilo.ev3_print("Press request button:")
        pressed = lilo.wait_button(
            [Button.UP, Button.LEFT, Button.RIGHT, Button.DOWN, Button.CENTER]
        )
        button_to_request = {
            Button.UP: "CLAW_HIGH",
            Button.LEFT: "CLAW_OPEN",
            Button.RIGHT: "CLAW_CLOSE",
            Button.DOWN: "CLAW_LOW",
            Button.CENTER: "CLAW_MID",
        }
        lilo.ev3_print(pressed)
        lilo.bluetooth.message(button_to_request[pressed])

        # while Button.CENTER not in lilo.ev3.buttons.pressed():
        #     lilo.ev3_print(lilo.bluetooth.message(should_wait=False))

        # lilo.bluetooth.message("STOP")


def stitch_main(stitch: OmniRobot):
    stitch.start_claw(0, 90, -330, 0)
    stitch.bluetooth.start()

    while True:
        request = stitch.bluetooth.message()
        stitch.ev3_print(request)
        if request == "ULTRA_SIDE":
            transmit_signal(stitch, stitch.ultra_side.distance)
        elif request == "ULTRA_BACK":
            transmit_signal(stitch, stitch.ultra_back.distance)
        elif request == "ULTRA_FRONT":
            transmit_signal(stitch, stitch.ultra_front.distance)
        elif request == "COLOR_SIDE":
            transmit_signal(stitch, stitch.color_side.color)
        elif request == "CLAW_LOW":
            lower_claw(stitch)
        elif request == "CLAW_HIGH":
            raise_claw(stitch)
        elif request == "CLAW_MID":
            mid_claw(stitch)
        elif request == "CLAW_OPEN":
            open_claw(stitch)
        elif request == "CLAW_CLOSE":
            close_claw(stitch)


def main(hostname):
    if hostname == "lilo":
        test_navigation_lilo(
            OmniRobot(
                motor_front_left=Port.B,
                motor_front_right=Port.C,
                motor_back_left=Port.A,
                motor_back_right=Port.D,
                color_front_left=DecisionColorSensor(
                    ColorSensor(Port.S3), lilo_lego_ev3_color_p3_decision_tree
                ),
                color_front_right=DecisionColorSensor(
                    ColorSensor(Port.S2), lilo_lego_ev3_color_p2_decision_tree
                ),
                color_back_left=DecisionColorSensor(
                    ColorSensor(Port.S1), lilo_lego_ev3_color_p1_decision_tree
                ),
                color_back_right=DecisionColorSensor(
                    ColorSensor(Port.S4), lilo_lego_ev3_color_p4_decision_tree
                ),
                server_name="lilo",
            )
        )
    elif hostname == "stitch":
        stitch_main(
            OmniRobot(
                color_side=DecisionColorSensor(
                    Ev3devSensor(Port.S4), ht_nxt_color_v2_p2_decision_tree
                ),
                ultra_front=Port.S2,
                ultra_back=Port.S1,
                ultra_side=Port.S3,
                motor_claw_lift=Port.C,
                motor_claw_gripper=Port.B,
                server_name="lilo",
            )
        )


if __name__ == "__main__":
    main(get_hostname())
