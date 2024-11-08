#!/usr/bin/env pybricks-micropython

"""
Módulo para centralização dos processos e gerência da estratégia geral.

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
from pybricks.parameters import Port, Button, Stop  # type: ignore
from pybricks.ev3devices import ColorSensor  # type: ignore
from pybricks.tools import wait  # type: ignore

from core.robot import Robot
from core.utils import get_hostname
from core.decision_color_sensor import DecisionColorSensor
import domain.star_platinum as star_platinum

import constants as const
from domain.localization import localization_routine
from domain.pathfinding import Graph, map_matrix, get_target_for_passenger
from domain.path_control import path_control
from domain.boarding import passenger_unboarding, passenger_boarding
from decision_trees.ht_nxt_color_v2_2 import ht_nxt_color_v2_p2_decision_tree
from decision_trees.lego_ev3_color_1 import levo_ev3_color_1_decision_tree
from decision_trees.sandy_lego_ev3_color_3 import sandy_lego_ev3_color_p3_decision_tree
from decision_trees.sandy_lego_ev3_color_4 import sandy_lego_ev3_color_p4_decision_tree

from domain.localization import read_color, catch_color_routine, walk_until_non_white
from core.robot import Robot


def sandy_main(sandy: Robot):
    """
    Faz o robô andar até detectar uma cor diferente de branco, então armazena a cor detectada.
    Ainda não está estruturado como deveria no arquivo localization.py
    """
    lista = []
    sandy.reset_wheels_angle()

    walk_until_non_white(sandy)
   
    sandy.off_motors()
   
    detected_color = sandy.color_left.color()  
    lista.append(detected_color)
    
    angle = (sandy.motor_l.angle() + sandy.motor_r.angle()) / 2
    distance = sandy.motor_degrees_to_cm(angle)
    
    sandy.pid_walk(cm=distance, speed=-60)
    

    sandy.reset_wheels_angle()

    sandy.pid_turn(90)
   
    walk_until_non_white(sandy)
   
    sandy.off_motors()
   
    detected_color = sandy.color_left.color()  
    lista.append(detected_color)
    
    angle = (sandy.motor_l.angle() + sandy.motor_r.angle()) / 2
    distance = sandy.motor_degrees_to_cm(angle)
    
    sandy.pid_walk(cm=distance, speed=-60)

    sandy.ev3_print(lista)

    # Inicialização mapa
    #map_graph = Graph(map_matrix)

    #
    # Localização inicial
    #
    #localization_routine(sandy)

    """while True:
        #
        # Coleta de passageiros
        #
        passenger_info = passenger_boarding(sandy)

        #
        # Pathfinding e movimentação (obstáculos)
        #
        target = get_target_for_passenger(passenger_info)
        if isinstance(target, tuple):
            # Caso do parque, calcula a menor distância até lá
            paths = []
            for target_item in target:
                paths.append(map_graph.dijkstra(5, target_item))
            paths.sort(key=lambda x: x[1])
            path, distance, directions = paths[0]
        else:
            path, distance, directions = map_graph.dijkstra(5, target)
        path_control(sandy, path, directions)

        #
        # Desembarque de passageiros
        #
        passenger_unboarding(sandy)

        #
        # Retorno a zona de embarque
        #
        path, _, directions = map_graph.dijkstra(
            path[-2]  # A penultima posição do caminho (antes do vértice de entrega)
        )
        path_control(sandy, path, directions)
"""

def junior_main(junior: Robot):
    junior.bluetooth.start()

    # Levanta garra inicialmente
    junior.motor_elevate_claw.run_until_stalled(200, Stop.HOLD, 70)
    junior.motor_elevate_claw.hold()
    star_platinum.main(junior)
    


def test_navigation_main(sandy: Robot):
    # sandy.bluetooth.start()
    while True:
        sandy.pid_walk(20, speed=80)

    map_graph = Graph(map_matrix)

    sandy.ev3_print("Press initial robot orientation:")
    pressed = sandy.wait_button([Button.UP, Button.LEFT, Button.RIGHT, Button.DOWN])
    button_to_direction = {
        Button.UP: "N",
        Button.LEFT: "O",
        Button.RIGHT: "L",
        Button.DOWN: "S",
    }
    sandy.orientation = button_to_direction[pressed]

    map_graph.mark_obstacle("V10")
    map_graph.mark_obstacle("V21")
    path, _, directions = map_graph.dijkstra(5, 26)

    path_control(sandy, path, directions)

    sandy.wait_button()
    path, _, directions = map_graph.dijkstra(27, 6)
    path_control(sandy, path, directions)


def test_calibrate_align_pid(robot: Robot):
    while True:
        robot.wait_button()
        robot.align()


def test_passenger_boarding(sandy: Robot):
    sandy.bluetooth.start()
    passenger_boarding(sandy)


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
                    ColorSensor(Port.S2), levo_ev3_color_1_decision_tree
                ),
                ultra_head=Port.S1,
                server_name="sandy",
            )
        )


if __name__ == "__main__":
    main(get_hostname())
