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

# Troca a cor lida pelo sensor para o nome sem o prefixo 'Color.'
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

# Chega de frente no azul e faz a rotina do azul
def blue_routine(robot: Robot):  
    robot.pid_turn(90)
    while read_color(robot.color_right.color()) != "RED" and read_color(robot.color_left.color) != "RED":
        robot.pid_walk()
    robot.pid_turn(180)
    return "V31"
   
def black_routine(robot:Robot):
    robot.align()
    robot.pid_turn(180)
    while read_color(robot.color_left.color()) == "WHITE" and read_color(robot.color_right.color()) == "WHITE":
        robot.pid_walk()

def red_routine(robot:Robot):
    robot.pid_walk(cm=-30)
    robot.pid_turn(90)
    while read_color(robot.color_left.color()) == "WHITE" and read_color(robot.color_right.color()) == "WHITE":
        robot.pid_walk()
    if read_color(robot.color_left.color()) == "BLACK" or read_color(robot.color.right.color()) == "BLACK":
        robot.align()
        black_routine()
    if read_color(robot.color_left.color()) == "BLUE" or read_color(robot.color_right.color()) == "BLUE":
        robot.align()
        blue_routine(robot)
        return True
    return False

def all_white_routine(robot:Robot):
    while read_color(robot.color_left.color()) != "WHITE" or read_color(robot.color_rigth.color()) != "WHITE":
        robot.pid_walk()
    if read_color(robot.color_left.color()) == "RED" and read_color(robot.color_right()) == "RED":
        red_routine()
    if read_color(robot.color_left.color()) == "BLACK" and read_color(robot.color_right()) == "BLACK":
        black_routine()
    if read_color(robot.color_left.color()) == "BLUE" and read_color(robot.color_right()) == "BLUE":
        blue_routine()
    
def catch_color_routine(lista,robot:Robot):
    distance, angle = 0,0
    robot.motor_l.reset_angle()
    robot.motor_l.reset_angle()
    while read_color(robot.color_left.color()) == "WHITE" or read_color(robot.color_rigth.color()) == "WHITE" and distance < 30.5:
        angle += (robot.motor_l.angle()+robot.motor_r.angle()/2)
        distance = robot.motor_degrees_to_cm(angle)
        robot.pid_walk()
    if read_color.color_left.color() != "WHITE":
        color = read_color(robot.color_left.color())
        lista.append(color)
    robot.pid_walk(-distance)

def fill_list(robot: Robot):
    lista = []
    for _ in range(3):
        catch_color_routine(lista, robot)
        if read_color(robot.color_left()) == "BLUE":
            blue_routine(robot)
            break
        robot.pid_turn(90)
    else:
        catch_color_routine(lista, robot)
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
    resultado = fill_list(robot)
    print(resultado)