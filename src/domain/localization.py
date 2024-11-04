from core.robot import Robot
from pybricks.parameters import Port
from pybricks.ev3devices import ColorSensor

import constants as const
from pybricks.parameters import Color
from core.decision_color_sensor import DecisionColorSensor
from time import time, sleep


# TODO substituir as condições pelo tratamento de cores
# TODO testar o robô para criar logs que permitam diferenciar os vértices
# TODO descobrir se usaremos árvore de decisão ou apenas condicionais
# TODO incrementar os resultados de diferenciação na função adivinhar vértice
# TODO conectar com o restante do código

wall_colors = [Color.BLACK, Color.BLUE, Color.RED, Color.YELLOW, Color.BROWN]

cor_laterais_vertices = [
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
    robot.turn(180)
    return "V31"
   
def red_routine(robot:Robot):
    robot

def fill_list(
    robot: Robot
):
    lista = []
    for _ in range(4):
        while robot.color_sensor.color() == "Color.WHITE" and :
            robot.walk()
        if robot.color_sensor.color() == "Color.BLUE":
            blue_routine(robot)
        else:
            lista.append(read_color())
            fim = robot.watch()
            robot.hold_wheels()
            print(lista)
        return lista 


def interprets_list(lista):
    for vertice_info in laterais_vertices:
        vertice_id = vertice_info[0][0]
        combinacoes = vertice_info[1:]
        if lista in combinacoes:
            return "V{}".format(vertice_id)
    return None


resultado = interprets_list(
    ["YELLOW", "RED", "YELLOW", "RED"]
)  # retorna apenas o 1º id, fazer alteração para ter um tempo de cada movimentação


def localization_routine(robot: Robot):

    log_data = []  
    while True:
        robot.pid_turn(90)
        start_time = time()
        
        while robot.color_left.color() == Color.WHITE and robot.color_right.color() == Color.WHITE:
            robot.walk()
        robot.pid_walk(speed=80,cm=1)
        detected_color = (
            robot.color_left.color() if robot.color_left.color() != Color.WHITE 
            else robot.color_right.color()
        )
        time_spent = time() - start_time
        log_data.append(detected_color)
        log_data.append(time_spent)

        if detected_color in wall_colors:
            break
    robot.walk(-100)
    sleep(time_spent)
    robot.off_motors()  
    return log_data

    
        

    