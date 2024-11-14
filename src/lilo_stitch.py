#!/usr/bin/env pybricks-micropython

from core.omni_robot import OmniRobot, Direction
from core.utils import get_hostname, PIDValues
from core.decision_color_sensor import DecisionColorSensor

from pybricks.parameters import Port, Button, Color
from pybricks.ev3devices import ColorSensor
from pybricks.iodevices import Ev3devSensor
from pybricks.tools import wait
import constants as const

if const.MAP_COLOR_CALIBRATION == "OFICIAL":
    from decision_trees.oficial.lilo_lego_ev3_color_1 import (
        lilo_lego_ev3_color_p1_decision_tree,
    )
    from decision_trees.oficial.lilo_lego_ev3_color_2 import (
        lilo_lego_ev3_color_p2_decision_tree,
    )
    from decision_trees.oficial.lilo_lego_ev3_color_3 import (
        lilo_lego_ev3_color_p3_decision_tree,
    )
    from decision_trees.oficial.lilo_lego_ev3_color_4 import (
        lilo_lego_ev3_color_p4_decision_tree,
    )
    from decision_trees.oficial.stitch_ht_nxt_color_v2_4 import (
        stitch_ht_nxt_color_v2_p4_decision_tree,
    )
elif const.MAP_COLOR_CALIBRATION == "HOME":
    from decision_trees.home.lilo_lego_ev3_color_1 import (
        lilo_lego_ev3_color_p1_decision_tree,
    )
    from decision_trees.home.lilo_lego_ev3_color_2 import (
        lilo_lego_ev3_color_p2_decision_tree,
    )
    from decision_trees.home.lilo_lego_ev3_color_3 import (
        lilo_lego_ev3_color_p3_decision_tree,
    )
    from decision_trees.home.lilo_lego_ev3_color_4 import (
        lilo_lego_ev3_color_p4_decision_tree,
    )
    from decision_trees.home.stitch_ht_nxt_color_v2_4 import (
        stitch_ht_nxt_color_v2_p4_decision_tree,
    )
elif const.MAP_COLOR_CALIBRATION == "TEST":
    from decision_trees.test.lilo_lego_ev3_color_1 import (
        lilo_lego_ev3_color_p1_decision_tree,
    )
    from decision_trees.test.lilo_lego_ev3_color_2 import (
        lilo_lego_ev3_color_p2_decision_tree,
    )
    from decision_trees.test.lilo_lego_ev3_color_3 import (
        lilo_lego_ev3_color_p3_decision_tree,
    )
    from decision_trees.test.lilo_lego_ev3_color_4 import (
        lilo_lego_ev3_color_p4_decision_tree,
    )
    from decision_trees.test.stitch_ht_nxt_color_v2_4 import (
        stitch_ht_nxt_color_v2_p4_decision_tree,
    )

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
from domain.boarding import (
    omni_passenger_boarding,
    omni_passenger_unboarding,
    omni_manouver_to_get_passenger,
)
from domain.omni_localization import localization_routine


def lilo_main(lilo: OmniRobot):
    lilo.ev3_print(lilo.bluetooth.start())
    wait(100)

    # Inicialização do mapa
    map_graph = Graph(map_matrix)

    #
    # Localização inicial
    #
    localization_routine(lilo)
    lilo.orientation = "N"  # TODO: deixar na lógica de localização

    while True:
        #
        # Coleta de passageiros
        #
        passenger_info, boarding_position = omni_passenger_boarding(lilo)
        lilo.ev3_print("P.i.:", passenger_info)

        #
        # Pathfinding e movimentação (obstáculos)
        #
        target = get_target_for_passenger(*passenger_info)
        delivered_position = move_from_position_to_targets(
            lilo, map_graph, boarding_position[0], target
        )

        #
        # Desembarque de passageiros
        #
        omni_passenger_unboarding(lilo)

        #
        # Retorno a zona de embarque
        #
        move_from_position_to_targets(
            lilo, map_graph, delivered_position, [boarding_position[1]]
        )
        omni_manouver_to_get_passenger(lilo)


def move_from_position_to_targets(
    lilo: OmniRobot, map_graph: Graph, initial_position: int, targets: list
):
    """Integra pathfinding e path control para mover o robô de uma posição inicial para uma posição alvo, recalculando rotas quando necessário.
    Retorna a posição final do robô.
    """

    completed = False
    current_position_idx = -1
    while not completed:
        if current_position_idx == -1:
            current_position = initial_position

        path, _, directions = map_graph.find_best_path(current_position, targets)
        lilo.ev3_print("Path:", path)
        lilo.ev3_print("Directions:", directions)
        completed, current_position_idx = omni_path_control(lilo, path, directions)
        if not completed:
            # Marca obstáculo e tenta denovo
            map_graph.mark_obstacle("V{}".format(path[current_position_idx + 1]))
            current_position = path[current_position_idx]
            lilo.ev3_print(
                "Obstacle detected at V{}".format(path[current_position_idx + 1])
            )
            lilo.ev3_print("Recalculating path...")
            for _ in range(2):
                lilo.ev3.speaker.beep(700)
                lilo.ev3.speaker.beep(900)
    lilo.ev3_print("Finished in path[{}]".format(current_position_idx))
    return path[current_position_idx]


def test_navigation_lilo(lilo: OmniRobot):

    forward_avoiding_places(lilo, speed=60)

    return

    lilo.bluetooth.start()

    passenger_info = omni_passenger_boarding(lilo)

    return

    map_graph = Graph(map_matrix)

    lilo.orientation = "N"
    initial_position = 5
    target_position = 26

    current_position = move_from_position_to_target(
        lilo, map_graph, initial_position, target_position
    )
    lilo.wait_button()
    move_from_position_to_target(lilo, map_graph, current_position, initial_position)


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
    open_claw(stitch)
    # stitch.start_claw()
    stitch.bluetooth.start()

    while True:
        request = stitch.bluetooth.message()
        stitch.ev3_print(request)
        if request == "ULTRA_FRONT":
            transmit_signal(stitch, stitch.ultra_front.distance)
        elif request == "ULTRA_BACK":
            transmit_signal(stitch, stitch.ultra_back.distance)
        elif request == "ULTRA_CLAW":
            transmit_signal(stitch, stitch.ultra_claw.distance)
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
        stitch.bluetooth.message(None, force_send=True)
        stitch.ev3_print("Request finished")
        # stitch.ev3_print(stitch.ultra_claw.distance(), stitch.ultra_front.distance())


def test_unboarding(robot: OmniRobot):
    robot.bluetooth.start()
    
    wait(100)
    
    robot.bluetooth.message("CLAW_CLOSE")
    robot.bluetooth.message()

    robot.bluetooth.message("CLAW_HIGH")
    robot.bluetooth.message()
    
    omni_passenger_unboarding(robot)
    


def main(hostname):
    if hostname == "lilo":
        lilo_main(
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
                    Ev3devSensor(Port.S4), stitch_ht_nxt_color_v2_p4_decision_tree
                ),
                ultra_claw=Port.S2,
                ultra_back=Port.S1,
                ultra_front=Port.S3,
                motor_claw_lift=Port.C,
                motor_claw_gripper=Port.B,
                server_name="lilo",
            )
        )


if __name__ == "__main__":
    main(get_hostname())
