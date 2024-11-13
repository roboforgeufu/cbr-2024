#!/usr/bin/env pybricks-micropython

"""
Módulo para centralização dos processos e gerência da estratégia geral.
3
Podem estar nesse módulo coisas como:
    - Código que controla a ordem que as rotinas serão executadas
    - Código para controle de fluxo geral do robô
    - Chamadas a rotinas mais específicas
    - Instanciação de estruturas de dados, classes, etc.
    - Códigos específicos de comunicação com o EV3 ou gerência de recursos de sistemas
        operacionais no geral
    - Várias funções "main" alternativas, inclusive para testes ou calibragem de
        motores/sensores

Não devem estar nesse módulo:
    - Definição de constantes ou variáveis globais
    - Chamadas de função fora de escopo da main do módulo
    - Execução de código manipulando motores ou sensores diretamente

OBS:. As direções são determinadas a partir do POV do robô
"""
from pybricks.parameters import Port, Button, Stop, Color  # type: ignore
from pybricks.ev3devices import ColorSensor  # type: ignore
from pybricks.tools import wait  # type: ignore

from core.robot import Robot
from core.utils import get_hostname
from core.decision_color_sensor import DecisionColorSensor
import domain.star_platinum as star_platinum


import constants as const
from domain.localization import localization_routine, wall_colors_check, color_lateral_vertices
from domain.pathfinding import Graph, map_matrix, get_target_for_passenger
from domain.path_control import path_control
from domain.boarding import passenger_unboarding, passenger_boarding
from domain.localization import localization_routine
from domain.pathfinding import Graph, map_matrix, get_target_for_passenger
from domain.path_control import path_control
from domain.boarding import passenger_unboarding, passenger_boarding

if const.MAP_COLOR_CALIBRATION == "OFICIAL":
    from decision_trees.oficial.sandy_lego_ev3_color_3 import (
        sandy_lego_ev3_color_p3_decision_tree,
    )
    from decision_trees.oficial.sandy_lego_ev3_color_4 import (
        sandy_lego_ev3_color_p4_decision_tree,
    )
    from decision_trees.oficial.junior_lego_ev3_color_2 import (
        junior_lego_ev3_color_p2_decision_tree,
    )
elif const.MAP_COLOR_CALIBRATION == "HOME":
    from decision_trees.home.sandy_lego_ev3_color_3 import (
        sandy_lego_ev3_color_p3_decision_tree,
    )
    from decision_trees.home.sandy_lego_ev3_color_4 import (
        sandy_lego_ev3_color_p4_decision_tree,
    )
    from decision_trees.home.junior_lego_ev3_color_2 import (
        junior_lego_ev3_color_p2_decision_tree,
    )

from domain.localization import catch_color_routine, walk_until_non_white
from core.robot import Robot


# def sandy_main(sandy: Robot):
#     """
#     Faz o robô andar até detectar uma cor diferente de branco, então armazena a cor detectada.
#     Ainda não está estruturado como deveria no arquivo localization.py
#     """
#     lista = []

#     obstacle_function = lambda: (
#         sandy.color_left.color() != Color.WHITE
#         or sandy.color_right.color() != Color.WHITE
#     )

#     sandy.reset_wheels_angle()

#     has_seen_obstacle, _ = sandy.pid_walk(
#         30,
#         obstacle_function=obstacle_function,
#     )

#     if has_seen_obstacle:
#         sandy.align()
    
#     cor = wall_colors_check(sandy)
    
#     lista.append(cor)

#     rotation = sandy.wheels_angle()
#     distance = sandy.motor_degrees_to_cm(rotation)

#     sandy.pid_walk(cm=distance, speed=-60)
#     sandy.pid_turn(90)

#     print("Cores detectadas nos quatro lados:", lista)

#     # vertice_inicial = color_lateral_vertices
#     # TODO: Acessar dicionário
    
#     # next_vertice = passenger_boarding()
    

def junior_main(junior: Robot):
    junior.bluetooth.start()

    # Levanta garra inicialmente
    junior.motor_elevate_claw.run_until_stalled(300, Stop.HOLD, 90)
    junior.motor_elevate_claw.hold()
    star_platinum.main(junior)


def move_to_target(
    sandy: Robot, map_graph: Graph, initial_position: int, targets: list
):
    completed = False
    current_position_idx = -1
    while not completed:
        if current_position_idx == -1:
            current_position = initial_position

        path, _, directions = map_graph.find_best_path(current_position, targets)
        sandy.ev3_print("Path:", path)
        sandy.ev3_print("Directions:", directions)
        completed, current_position_idx = path_control(sandy, path, directions)
        if not completed:
            map_graph.mark_obstacle("V{}".format(path[current_position_idx + 1]))
            sandy.ev3_print(
                "Obstacle detected at V{}".format(path[current_position_idx + 1])
            )
            current_position = path[current_position_idx]


def test_path_control(sandy: Robot):
    sandy.ev3_print("Press initial robot orientation:")
    pressed = sandy.wait_button([Button.UP, Button.LEFT, Button.RIGHT, Button.DOWN])
    button_to_direction = {
        Button.UP: "N",
        Button.LEFT: "O",
        Button.RIGHT: "L",
        Button.DOWN: "S",
    }
    sandy.orientation = button_to_direction[pressed]
    sandy.ev3_print(pressed)
    map_graph = Graph(map_matrix)
    initial_position = 1
    targets = [26]
    sandy.ev3_print("Press button to start:")
    sandy.wait_button()
    move_to_target(sandy, map_graph, initial_position, targets)


def test_calibrate_align_pid(robot: Robot):
    while True:
        robot.wait_button()
        robot.align()


def test_passenger_boarding(sandy: Robot):
    sandy.bluetooth.start()
    passenger_info = passenger_boarding(sandy)


def sandy_main(sandy: Robot):
    # inicia a comunicacao bluetooth
    # sandy.bluetooth.start()

    #
    # localização inicial
    #

    localization_routine(sandy)
    ## rotina de localização inicial

    ## loop    

    #
    # embarque de passageiro
    #
    # passenger_boarding(sandy)   


    #
    # calculo de rota e controle de caminho
    #

    #
    # retorno para a origem
    #

def main(hostname):
    if hostname == "sandy":
        sandy_main(
            Robot(
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
                server_name="sandy",
            )
        )
    else:
        junior_main(
            Robot(
                wheel_diameter=const.WHEEL_DIAMETER,
                wheel_distance=const.WHEEL_DIST,
                motor_elevate_claw=Port.C,
                motor_open_claw=Port.B,
                color_claw=DecisionColorSensor(
                    ColorSensor(Port.S2), junior_lego_ev3_color_p2_decision_tree
                ),
                ultra_head=Port.S1,
                server_name="sandy",
            )
        )


if __name__ == "__main__":
    main(get_hostname())
