from core.robot import Robot
from pybricks.parameters import Port
from pybricks.ev3devices import ColorSensor

import constants as const
from pybricks.parameters import Color
from core.decision_color_sensor import DecisionColorSensor


# TODO substituir as condições pelo tratamento de cores
# TODO testar o robô para criar logs que permitam diferenciar os vértices
# TODO descobrir se usaremos árvore de decisão ou apenas condicionais
# TODO incrementar os resultados de diferenciação na função adivinhar vértice
# TODO conectar com o restante do código

""" 
Abaixo estão as combinações e os vértices em que elas aparecem.

    ['YELLOW', 'RED', 'YELLOW', 'RED']: [1, 14],
    ['RED', 'YELLOW', 'RED', 'YELLOW']: [1, 14],
    ['BLACK', 'RED', 'YELLOW', 'RED']: [3, 16, 27, 29]
    ['RED', 'YELLOW', 'RED', 'BLACK']: [3, 16, 27, 29]
    ['YELLOW', 'RED', 'BLACK', 'RED']: [3, 16, 27, 29]
    ['RED', 'BLACK', 'RED', 'YELLOW']: [3, 16, 27, 29]
    ['BLACK', 'RED', 'BLUE', 'RED']: [5, 9, 11, 18, 20, 22, 24]
    ['RED', 'BLUE', 'RED', 'BLACK']: [5, 9, 11, 18, 20, 22, 24]
    ['BLUE', 'RED', 'BLACK', 'RED']: [5, 9, 11, 18, 20, 22, 24]
    ['RED', 'BLACK', 'RED', 'BLUE']: [5, 9, 11, 18, 20, 22, 24]
    ['BLACK', 'RED', 'BLUE', 'YELLOW']: [7]
    ['RED', 'BLUE', 'YELLOW', 'BLACK']: [7]
    ['BLUE', 'YELLOW', 'BLACK', 'RED']: [7]
    ['YELLOW', 'BLACK', 'RED', 'BLUE']: [7]
    ['BLACK', 'BLACK', 'BLUE', 'YELLOW']: [8]
    ['BLACK', 'BLUE', 'YELLOW', 'BLACK']: [8]
    ['BLUE', 'YELLOW', 'BLACK', 'BLACK']: [8]
    ['YELLOW', 'BLACK', 'BLACK', 'BLUE']: [8]
    ['BLACK', 'YELLOW', 'BLUE', 'YELLOW']: [10, 23]
    ['YELLOW', 'BLUE', 'YELLOW', 'BLACK']: [10, 23]
    ['BLUE', 'YELLOW', 'BLACK', 'YELLOW']: [10, 23]
    ['YELLOW', 'BLACK', 'YELLOW', 'BLUE']: [10, 23]
    ['BLACK', 'YELLOW', 'BLUE', 'BLACK']: [21]
    ['YELLOW', 'BLUE', 'BLACK', 'BLACK']: [21]
    ['BLUE', 'BLACK', 'BLACK', 'YELLOW']: [21]
    ['BLACK', 'BLACK', 'YELLOW', 'BLUE']: [21]
    ['YELLOW', 'RED', 'BLUE', 'RED']: [31]
    ['RED', 'BLUE', 'RED', 'YELLOW']: [31]
    ['BLUE', 'RED', 'YELLOW', 'RED']: [31]
    ['RED', 'YELLOW', 'RED', 'BLUE']: [31]
"""

laterais_vertices = [
    [
        [1],
        ["YELLOW", "RED", "YELLOW", "RED"],
        ["RED", "YELLOW", "RED", "YELLOW"],
        ["YELLOW", "RED", "YELLOW", "RED"],
        ["RED", "YELLOW", "RED", "YELLOW"],
    ],
    [
        [3],
        ["BLACK", "RED", "YELLOW", "RED"],
        ["RED", "YELLOW", "RED", "BLACK"],
        ["YELLOW", "RED", "BLACK", "RED"],
        ["RED", "BLACK", "RED", "YELLOW"],
    ],
    [
        [5],
        ["BLACK", "RED", "BLUE", "RED"],
        ["RED", "BLUE", "RED", "BLACK"],
        ["BLUE", "RED", "BLACK", "RED"],
        ["RED", "BLACK", "RED", "BLUE"],
    ],
    [
        [7],
        ["BLACK", "RED", "BLUE", "YELLOW"],
        ["RED", "BLUE", "YELLOW", "BLACK"],
        ["BLUE", "YELLOW", "BLACK", "RED"],
        ["YELLOW", "BLACK", "RED", "BLUE"],
    ],
    [
        [8],
        ["BLACK", "BLACK", "BLUE", "YELLOW"],
        ["BLACK", "BLUE", "YELLOW", "BLACK"],
        ["BLUE", "YELLOW", "BLACK", "BLACK"],
        ["YELLOW", "BLACK", "BLACK", "BLUE"],
    ],
    [
        [9],
        ["BLACK", "RED", "BLUE", "RED"],
        ["RED", "BLUE", "RED", "BLACK"],
        ["BLUE", "RED", "BLACK", "RED"],
        ["RED", "BLACK", "RED", "BLUE"],
    ],
    [
        [10],
        ["BLACK", "YELLOW", "BLUE", "YELLOW"],
        ["YELLOW", "BLUE", "YELLOW", "BLACK"],
        ["BLUE", "YELLOW", "BLACK", "YELLOW"],
        ["YELLOW", "BLACK", "YELLOW", "BLUE"],
    ],
    [
        [11],
        ["BLACK", "RED", "BLUE", "RED"],
        ["RED", "BLUE", "RED", "BLACK"],
        ["BLUE", "RED", "BLACK", "RED"],
        ["RED", "BLACK", "RED", "BLUE"],
    ],
    [
        [14],
        ["YELLOW", "RED", "YELLOW", "RED"],
        ["RED", "YELLOW", "RED", "YELLOW"],
        ["YELLOW", "RED", "YELLOW", "RED"],
        ["RED", "YELLOW", "RED", "YELLOW"],
    ],
    [
        [16],
        ["YELLOW", "RED", "BLACK", "RED"],
        ["RED", "BLACK", "RED", "YELLOW"],
        ["BLACK", "RED", "YELLOW", "RED"],
        ["RED", "YELLOW", "RED", "BLACK"],
    ],
    [
        [18],
        ["BLACK", "RED", "BLUE", "RED"],
        ["RED", "BLUE", "RED", "BLACK"],
        ["BLUE", "RED", "BLACK", "RED"],
        ["RED", "BLACK", "RED", "BLUE"],
    ],
    [
        [20],
        ["BLACK", "RED", "BLUE", "RED"],
        ["RED", "BLUE", "RED", "BLACK"],
        ["BLUE", "RED", "BLACK", "RED"],
        ["RED", "BLACK", "RED", "BLUE"],
    ],
    [
        [21],
        ["BLACK", "YELLOW", "BLUE", "BLACK"],
        ["YELLOW", "BLUE", "BLACK", "BLACK"],
        ["BLUE", "BLACK", "BLACK", "YELLOW"],
        ["BLACK", "BLACK", "YELLOW", "BLUE"],
    ],
    [
        [22],
        ["BLACK", "RED", "BLUE", "RED"],
        ["RED", "BLUE", "RED", "BLACK"],
        ["BLUE", "RED", "BLACK", "RED"],
        ["RED", "BLACK", "RED", "BLUE"],
    ],
    [
        [23],
        ["BLACK", "YELLOW", "BLUE", "YELLOW"],
        ["YELLOW", "BLUE", "YELLOW", "BLACK"],
        ["BLUE", "YELLOW", "BLACK", "YELLOW"],
        ["YELLOW", "BLACK", "YELLOW", "BLUE"],
    ],
    [
        [24],
        ["BLACK", "RED", "BLUE", "RED"],
        ["RED", "BLUE", "RED", "BLACK"],
        ["BLUE", "RED", "BLACK", "RED"],
        ["RED", "BLACK", "RED", "BLUE"],
    ],
    [
        [27],
        ["YELLOW", "RED", "BLACK", "RED"],
        ["RED", "BLACK", "RED", "YELLOW"],
        ["BLACK", "RED", "YELLOW", "RED"],
        ["RED", "YELLOW", "RED", "BLACK"],
    ],
    [
        [29],
        ["YELLOW", "RED", "BLACK", "RED"],
        ["RED", "BLACK", "RED", "YELLOW"],
        ["BLACK", "RED", "YELLOW", "RED"],
        ["RED", "YELLOW", "RED", "BLACK"],
    ],
    [
        [31],
        ["YELLOW", "RED", "BLUE", "RED"],
        ["RED", "BLUE", "RED", "YELLOW"],
        ["BLUE", "RED", "YELLOW", "RED"],
        ["RED", "YELLOW", "RED", "BLUE"],
    ],
]


def read_color(color):
    if color == "Color.RED":
        return "RED"
    elif color == "Color.YELLOW":
        return "YELLOW"
    elif color == "Color.BLUE":
        return "BLUE"
    elif color == "Color.BLACK":
        return "BLACK"
    else:
        return None


def blue_routine(robot: Robot):  # chega de frente no azul
    robot.turn(90)
    while robot.color_right.color() != "Color.RED" and robot.color_left.color != "Color.RED":
        robot.walk()
    robot.turn(90)
    while robot.color_left.color() == "Color.WHITE" and robot.color_right == "Color.WHITE":
        robot.walk()
    if robot.color_left.color() == "Color.YELLOW" and robot.color_right == "Color.YELLOW":
        return "V31"
    return "V5"


def fill_list(
    robot: Robot
):
    ini = robot.watch()
    lista = []
    while robot.color_sensor.color() == "Color.WHITE":
        robot.walk()
        if robot.color_sensor.color() == "Color.BLUE":
            blue_routine(robot)
        else:
            lista.append(read_color())
            fim = robot.watch()
            lista.append(fim-ini)
            robot.hold_wheels()
            robot.turn(90)
        return lista 


def interprets_list(lista):
    for vertice_info in laterais_vertices:
        vertice_id = vertice_info[0][0]
        combinacoes = vertice_info[1:]
        if lista in combinacoes:
            return f"V{vertice_id}"
    return None


resultado = interprets_list(
    ["YELLOW", "RED", "YELLOW", "RED"]
)  # retorna apenas o 1º id, fazer alteração para ter um tempo de cada movimentação
print(resultado)


def localization_routine(robot: Robot):
    """
    Rotina de localização inicial do robô.
    Termina na origem: posição fixa pra iniciar a rotina de coleta de passageiros.
    """
    fill_list(robot)
    robot.hold_wheels()
