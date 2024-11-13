from core.robot import Robot
from pybricks.parameters import Port
from pybricks.ev3devices import ColorSensor

import constants as const
from pybricks.parameters import Color
from time import time, sleep

#TODO testar a rotina de ler os 30cm para os 3 lados
#TODO pensar em uma rotina para quando houver obstáculo
#TODO completar a lógica com as quebras apenas no vermelho e azul
#TODO criar rotinas para o preto e amarelo


wall_colors = [Color.BLACK, Color.BLUE, Color.RED, Color.YELLOW, Color.BROWN]

color_lateral_vertices = [
    [
        [1],
        [
            ["RED", "YELLOW", "WHITE", "YELLOW"],           # Rotação 0
            ["YELLOW", "WHITE", "YELLOW", "RED"],           # Rotação 1
            ["WHITE", "YELLOW", "RED", "YELLOW"],           # Rotação 2
            ["YELLOW", "RED", "YELLOW", "WHITE"],           # Rotação 3
        ]
    ],
    [
        [3],
        [
            ["RED", "YELLOW", "WHITE", "BLACK"],           # Rotação 0
            ["YELLOW", "WHITE", "BLACK", "RED"],           # Rotação 1
            ["WHITE", "BLACK", "RED", "YELLOW"],           # Rotação 2
            ["BLACK", "RED", "YELLOW", "WHITE"],           # Rotação 3
        ]
    ],
    [
        [5],
        [
            ["RED", "BLUE", "WHITE", "BLACK"],             # Rotação 0
            ["BLUE", "WHITE", "BLACK", "RED"],             # Rotação 1
            ["WHITE", "BLACK", "RED", "BLUE"],             # Rotação 2
            ["BLACK", "RED", "BLUE", "WHITE"],             # Rotação 3
        ]
    ],
    [
        [7],
        [
            ["WHITE", "WHITE", "WHITE", "BLACK"],          # Rotação 0
            ["WHITE", "WHITE", "BLACK", "WHITE"],          # Rotação 1
            ["WHITE", "BLACK", "WHITE", "WHITE"],          # Rotação 2
            ["BLACK", "WHITE", "WHITE", "WHITE"],          # Rotação 3
        ]
    ],
    [
        [8],
        [
            ["YELLOW", "WHITE", "BLACK", "WHITE"],         # Rotação 0
            ["WHITE", "BLACK", "WHITE", "YELLOW"],         # Rotação 1
            ["BLACK", "WHITE", "YELLOW", "WHITE"],         # Rotação 2
            ["WHITE", "YELLOW", "WHITE", "BLACK"],         # Rotação 3
        ]
    ],
    [
        [9],
        [
            ["WHITE", "WHITE", "WHITE", "WHITE"],          # Rotação 0
            ["WHITE", "WHITE", "WHITE", "WHITE"],          # Rotação 1
            ["WHITE", "WHITE", "WHITE", "WHITE"],          # Rotação 2
            ["WHITE", "WHITE", "WHITE", "WHITE"],          # Rotação 3
        ]
    ],
    [
        [10],
        [
            ["YELLOW", "WHITE", "YELLOW", "WHITE"],        # Rotação 0
            ["WHITE", "YELLOW", "WHITE", "YELLOW"],        # Rotação 1
            ["YELLOW", "WHITE", "YELLOW", "WHITE"],        # Rotação 2
            ["WHITE", "YELLOW", "WHITE", "YELLOW"],        # Rotação 3
        ]
    ],
    [
        [11],
        [
            ["WHITE", "BLUE", "WHITE", "WHITE"],           # Rotação 0
            ["BLUE", "WHITE", "WHITE", "WHITE"],           # Rotação 1
            ["WHITE", "WHITE", "WHITE", "BLUE"],           # Rotação 2
            ["WHITE", "WHITE", "BLUE", "WHITE"],           # Rotação 3
        ]
    ],
    [
        [14],
        [
            ["WHITE", "YELLOW", "WHITE", "YELLOW"],        # Rotação 0
            ["YELLOW", "WHITE", "YELLOW", "WHITE"],        # Rotação 1
            ["WHITE", "YELLOW", "WHITE", "YELLOW"],        # Rotação 2
            ["YELLOW", "WHITE", "YELLOW", "WHITE"],        # Rotação 3
        ]
    ],
    [
        [16],
        [
            ["WHITE", "BLACK", "WHITE", "YELLOW"],         # Rotação 0
            ["BLACK", "WHITE", "YELLOW", "WHITE"],         # Rotação 1
            ["WHITE", "YELLOW", "WHITE", "BLACK"],         # Rotação 2
            ["YELLOW", "WHITE", "BLACK", "WHITE"],         # Rotação 3
        ]
    ],
    [
        [18],
        [
            ["WHITE", "BLUE", "WHITE", "BLACK"],           # Rotação 0
            ["BLUE", "WHITE", "BLACK", "WHITE"],           # Rotação 1
            ["WHITE", "BLACK", "WHITE", "BLUE"],           # Rotação 2
            ["BLACK", "WHITE", "BLUE", "WHITE"],           # Rotação 3
        ]
    ],
    [
        [20],
        [
            ["WHITE", "WHITE", "WHITE", "BLACK"],          # Rotação 0
            ["WHITE", "WHITE", "BLACK", "WHITE"],          # Rotação 1
            ["WHITE", "BLACK", "WHITE", "WHITE"],          # Rotação 2
            ["BLACK", "WHITE", "WHITE", "WHITE"],          # Rotação 3
        ]
    ],
    [
        [21],
        [
            ["WHITE", "BLACK", "WHITE", "YELLOW"],         # Rotação 0
            ["BLACK", "WHITE", "YELLOW", "WHITE"],         # Rotação 1
            ["WHITE", "YELLOW", "WHITE", "BLACK"],         # Rotação 2
            ["YELLOW", "WHITE", "BLACK", "WHITE"],         # Rotação 3
        ]
    ],
    [
        [22],
        [
            ["WHITE", "WHITE", "WHITE", "WHITE"],          # Rotação 0
            ["WHITE", "WHITE", "WHITE", "WHITE"],          # Rotação 1
            ["WHITE", "WHITE", "WHITE", "WHITE"],          # Rotação 2
            ["WHITE", "WHITE", "WHITE", "WHITE"],          # Rotação 3
        ]
    ],
    [
        [23],
        [
            ["YELLOW", "WHITE", "YELLOW", "WHITE"],        # Rotação 0
            ["WHITE", "YELLOW", "WHITE", "YELLOW"],        # Rotação 1
            ["YELLOW", "WHITE", "YELLOW", "WHITE"],        # Rotação 2
            ["WHITE", "YELLOW", "WHITE", "YELLOW"],        # Rotação 3
        ]
    ],
    [
        [24],
        [
            ["WHITE", "BLUE", "WHITE", "WHITE"],           # Rotação 0
            ["BLUE", "WHITE", "WHITE", "WHITE"],           # Rotação 1
            ["WHITE", "WHITE", "WHITE", "BLUE"],           # Rotação 2
            ["WHITE", "WHITE", "BLUE", "WHITE"],           # Rotação 3
        ]
    ],
    [
        [27],
        [
            ["YELLOW", "RED", "BLACK", "RED"],             # Rotação 0
            ["RED", "BLACK", "RED", "YELLOW"],             # Rotação 1
            ["BLACK", "RED", "YELLOW", "RED"],             # Rotação 2
            ["RED", "YELLOW", "RED", "BLACK"],             # Rotação 3
        ]
    ],
    [
        [29],
        [
            ["WHITE", "BLACK", "RED", "YELLOW"],           # Rotação 0
            ["BLACK", "RED", "YELLOW", "WHITE"],           # Rotação 1
            ["RED", "YELLOW", "WHITE", "BLACK"],           # Rotação 2
            ["YELLOW", "WHITE", "BLACK", "RED"],           # Rotação 3
        ]
    ],
    [
        [31],
        [
            ["WHITE", "BLUE", "RED", "YELLOW"],            # Rotação 0
            ["BLUE", "RED", "YELLOW", "WHITE"],            # Rotação 1
            ["RED", "YELLOW", "WHITE", "BLUE"],            # Rotação 2
            ["YELLOW", "WHITE", "BLUE", "RED"],            # Rotação 3
        ]
    ],
]


# Chega de frente no azul e faz a rotina do azul
def blue_routine(robot: Robot):  
    robot.pid_turn(90)
    while robot.color_right.color() != "Color.RED" and robot.color_left.color != "Color.RED":
        robot.walk()
    robot.pid_turn(180)
    return "V31"
   
def black_routine(robot:Robot):
    robot.align()
    robot.pid_turn(180)
    while robot.color_left.color() == "Color.WHITE" and robot.color_right.color() == "Color.WHITE":
        robot.walk()

def red_routine(robot:Robot):
    robot.walk(cm=-30)
    robot.pid_turn(90)
    while robot.color_left.color() == "Color.WHITE" and robot.color_right.color() == "Color.WHITE":
        robot.walk()
    if robot.color_left.color() == "Color.BLACK" or robot.color.right.color() == "Color.BLACK":
        robot.align()
        black_routine()
    if robot.color_left.color() == "Color.BLUE" or robot.color_right.color() == "Color.BLUE":
        robot.align()
        blue_routine(robot)
        return True
    return False

def all_white_routine(robot:Robot):
    while robot.color_left.color() != "Color.WHITE" or robot.color_right.color() != "Color.WHITE":
        robot.walk()
    if robot.color_left.color() == "Color.RED" and robot.color_right.color() == "Color.RED":
        red_routine()
    if robot.color_left.color() == "Color.BLACK" and robot.color_right.color() == "Color.BLACK":
        black_routine()
    if robot.color_left.color() == "Color.BLUE" and robot.color_right.color() == "Color.BLUE":
        blue_routine()
    
def walk_until_non_white(robot: Robot, speed=60):
    """
    Faz o robô andar uma distância de 30 cm ou até que os sensores detectem algo diferente de branco.
    """
    print(robot.color_right.color())
    
    stop_condition = lambda: (
        robot.color_left.color() != "Color.WHITE" or robot.color_right.color() != "Color.WHITE"
    )

    has_detected_non_white, _ = robot.pid_walk(
        cm=32,
        speed=speed,
        off_motors=True,   
        obstacle_function=stop_condition,
    )


def wall_colors_check(robot: Robot):

    if robot.color_left.color() == Color.YELLOW or robot.color_right.color() == Color.YELLOW: color = "Yellow"
    elif robot.color_left.color() == Color.BLACK or robot.color_right.color() == Color.BLACK: color = "Black"
    elif robot.color_left.color() == Color.RED or robot.color_right.color() == Color.RED: color = "Red"
    elif robot.color_left.color() == Color.BLUE or robot.color_right.color() == Color.BLUE: color = "Blue"
    return color

def catch_color_routine(lista, robot: Robot):
    """
    Copiar e colar quando o sandy main der certo aqui
    """
    return lista


def interprets_list(lista):
    vertices = []
    for i in range(len(color_lateral_vertices)):
        vertice_id, combinacoes = color_lateral_vertices[i][0], color_lateral_vertices[i][1]
        for item in combinacoes:
            if lista == item and "V"+str(vertice_id[0]) not in vertices:
                vertices.append("V"+str(vertice_id[0]))
    return vertices

def localization_routine(robot: Robot):
    