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
from pybricks.parameters import Port
from pybricks.ev3devices import ColorSensor

from core.robot import Robot
from core.utils import get_hostname
from core.decision_color_sensor import DecisionColorSensor

import constants as const
from domain.localization import localization_routine
from domain.pathfinding import Graph, map_matrix, get_target_for_passenger
from domain.boarding import passenger_boarding, passenger_unboarding
from domain.path_control import path_control
from decision_trees.ht_nxt_color_v2_2 import ht_nxt_color_v2_p2_decision_tree
from decision_trees.lego_ev3_color_1 import levo_ev3_color_1_decision_tree


def sandy_main(sandy: Robot):
    # Inicialização mapa
    map_graph = Graph(map_matrix)

    #
    # Localização inicial
    #
    localization_routine(sandy)

    while True:
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
        path_control(sandy, directions)

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
        path_control(sandy, directions)


def junior_main(junior: Robot):
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
        ...


def main():
    if get_hostname() == "sandy":
        sandy_main(
            Robot(
                wheel_diameter=const.WHEEL_DIAMETER,
                wheel_distance=const.WHEEL_DIST,
                motor_r=Port.B,
                motor_l=Port.C,
                infra_side=Port.S1,
                ultra_feet=Port.S2,
                color_right=DecisionColorSensor(
                    ColorSensor(Port.S3), levo_ev3_color_1_decision_tree
                ),
                color_left=DecisionColorSensor(
                    ColorSensor(Port.S4), levo_ev3_color_1_decision_tree
                ),
            )
        )
    else:
        junior_main(
            Robot(
                motor_elevate_claw=Port.C,
                motor_open_claw=Port.B,
                color_claw=DecisionColorSensor(
                    ColorSensor(Port.S1), levo_ev3_color_1_decision_tree
                ),
                ultra_head=Port.S2,
            )
        )
