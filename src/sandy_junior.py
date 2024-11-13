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
from domain.localization import (
    localization_routine,
    wall_colors_check,
    color_lateral_vertices,
)
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

from domain.localization import walk_until_non_white
from core.robot import Robot


def sandy_main(sandy: Robot):
    localization_routine(sandy)

    # next_vertice = passenger_boarding()


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
    return current_position


def test_sandy_main(sandy: Robot):
    # inicia a comunicacao bluetooth
    # sandy.bluetooth.start()

    #
    # localização inicial
    #

    localization_routine(sandy)
    ## rotina de localização inicial

    map_graph = Graph(map_matrix)
    origin_vertex = 31
    localization_vertex = 5
    ## loop    
    while True:
        #
        # embarque de passageiro
        #
        targets = passenger_boarding(sandy)

        #
        # calculo de rota e controle de caminho
        #
        current_position = move_to_target(sandy, map_graph, origin_vertex, targets)

        #
        # desembarque de passageiro
        #


        #
        # retorno para a origem
        #
        move_to_target(sandy, map_graph, current_position, list(localization_vertex))



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
