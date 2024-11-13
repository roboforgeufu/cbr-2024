from core.robot import Robot
from pybricks.parameters import Port
from pybricks.ev3devices import ColorSensor

import constants as const
from pybricks.parameters import Color
from time import time, sleep
from core.utils import PIDControl


# TODO testar a rotina de ler os 30cm para os 3 lados
# TODO pensar em uma rotina para quando houver obstáculo
# TODO completar a lógica com as quebras apenas no vermelho e azul
# TODO criar rotinas para o preto e amarelo


wall_colors = [Color.BLACK, Color.BLUE, Color.RED, Color.YELLOW, Color.BROWN]

color_lateral_vertices = [
    [
        [1],
        [
            ["RED", "YELLOW", "WHITE", "YELLOW"],  # Rotação 0
            ["YELLOW", "WHITE", "YELLOW", "RED"],  # Rotação 1
            ["WHITE", "YELLOW", "RED", "YELLOW"],  # Rotação 2
            ["YELLOW", "RED", "YELLOW", "WHITE"],  # Rotação 3
        ],
    ],
    [
        [3],
        [
            ["RED", "YELLOW", "WHITE", "BLACK"],  # Rotação 0
            ["YELLOW", "WHITE", "BLACK", "RED"],  # Rotação 1
            ["WHITE", "BLACK", "RED", "YELLOW"],  # Rotação 2
            ["BLACK", "RED", "YELLOW", "WHITE"],  # Rotação 3
        ],
    ],
    [
        [5],
        [
            ["RED", "BLUE", "WHITE", "BLACK"],  # Rotação 0
            ["BLUE", "WHITE", "BLACK", "RED"],  # Rotação 1
            ["WHITE", "BLACK", "RED", "BLUE"],  # Rotação 2
            ["BLACK", "RED", "BLUE", "WHITE"],  # Rotação 3
        ],
    ],
    [
        [7],
        [
            ["WHITE", "WHITE", "WHITE", "BLACK"],  # Rotação 0
            ["WHITE", "WHITE", "BLACK", "WHITE"],  # Rotação 1
            ["WHITE", "BLACK", "WHITE", "WHITE"],  # Rotação 2
            ["BLACK", "WHITE", "WHITE", "WHITE"],  # Rotação 3
        ],
    ],
    [
        [8],
        [
            ["YELLOW", "WHITE", "BLACK", "WHITE"],  # Rotação 0
            ["WHITE", "BLACK", "WHITE", "YELLOW"],  # Rotação 1
            ["BLACK", "WHITE", "YELLOW", "WHITE"],  # Rotação 2
            ["WHITE", "YELLOW", "WHITE", "BLACK"],  # Rotação 3
        ],
    ],
    [
        [9],
        [
            ["WHITE", "WHITE", "WHITE", "WHITE"],  # Rotação 0
            ["WHITE", "WHITE", "WHITE", "WHITE"],  # Rotação 1
            ["WHITE", "WHITE", "WHITE", "WHITE"],  # Rotação 2
            ["WHITE", "WHITE", "WHITE", "WHITE"],  # Rotação 3
        ],
    ],
    [
        [10],
        [
            ["YELLOW", "WHITE", "YELLOW", "WHITE"],  # Rotação 0
            ["WHITE", "YELLOW", "WHITE", "YELLOW"],  # Rotação 1
            ["YELLOW", "WHITE", "YELLOW", "WHITE"],  # Rotação 2
            ["WHITE", "YELLOW", "WHITE", "YELLOW"],  # Rotação 3
        ],
    ],
    [
        [11],
        [
            ["WHITE", "BLUE", "WHITE", "WHITE"],  # Rotação 0
            ["BLUE", "WHITE", "WHITE", "WHITE"],  # Rotação 1
            ["WHITE", "WHITE", "WHITE", "BLUE"],  # Rotação 2
            ["WHITE", "WHITE", "BLUE", "WHITE"],  # Rotação 3
        ],
    ],
    [
        [14],
        [
            ["WHITE", "YELLOW", "WHITE", "YELLOW"],  # Rotação 0
            ["YELLOW", "WHITE", "YELLOW", "WHITE"],  # Rotação 1
            ["WHITE", "YELLOW", "WHITE", "YELLOW"],  # Rotação 2
            ["YELLOW", "WHITE", "YELLOW", "WHITE"],  # Rotação 3
        ],
    ],
    [
        [16],
        [
            ["WHITE", "BLACK", "WHITE", "YELLOW"],  # Rotação 0
            ["BLACK", "WHITE", "YELLOW", "WHITE"],  # Rotação 1
            ["WHITE", "YELLOW", "WHITE", "BLACK"],  # Rotação 2
            ["YELLOW", "WHITE", "BLACK", "WHITE"],  # Rotação 3
        ],
    ],
    [
        [18],
        [
            ["WHITE", "BLUE", "WHITE", "BLACK"],  # Rotação 0
            ["BLUE", "WHITE", "BLACK", "WHITE"],  # Rotação 1
            ["WHITE", "BLACK", "WHITE", "BLUE"],  # Rotação 2
            ["BLACK", "WHITE", "BLUE", "WHITE"],  # Rotação 3
        ],
    ],
    [
        [20],
        [
            ["WHITE", "WHITE", "WHITE", "BLACK"],  # Rotação 0
            ["WHITE", "WHITE", "BLACK", "WHITE"],  # Rotação 1
            ["WHITE", "BLACK", "WHITE", "WHITE"],  # Rotação 2
            ["BLACK", "WHITE", "WHITE", "WHITE"],  # Rotação 3
        ],
    ],
    [
        [21],
        [
            ["WHITE", "BLACK", "WHITE", "YELLOW"],  # Rotação 0
            ["BLACK", "WHITE", "YELLOW", "WHITE"],  # Rotação 1
            ["WHITE", "YELLOW", "WHITE", "BLACK"],  # Rotação 2
            ["YELLOW", "WHITE", "BLACK", "WHITE"],  # Rotação 3
        ],
    ],
    [
        [22],
        [
            ["WHITE", "WHITE", "WHITE", "WHITE"],  # Rotação 0
            ["WHITE", "WHITE", "WHITE", "WHITE"],  # Rotação 1
            ["WHITE", "WHITE", "WHITE", "WHITE"],  # Rotação 2
            ["WHITE", "WHITE", "WHITE", "WHITE"],  # Rotação 3
        ],
    ],
    [
        [23],
        [
            ["YELLOW", "WHITE", "YELLOW", "WHITE"],  # Rotação 0
            ["WHITE", "YELLOW", "WHITE", "YELLOW"],  # Rotação 1
            ["YELLOW", "WHITE", "YELLOW", "WHITE"],  # Rotação 2
            ["WHITE", "YELLOW", "WHITE", "YELLOW"],  # Rotação 3
        ],
    ],
    [
        [24],
        [
            ["WHITE", "BLUE", "WHITE", "WHITE"],  # Rotação 0
            ["BLUE", "WHITE", "WHITE", "WHITE"],  # Rotação 1
            ["WHITE", "WHITE", "WHITE", "BLUE"],  # Rotação 2
            ["WHITE", "WHITE", "BLUE", "WHITE"],  # Rotação 3
        ],
    ],
    [
        [27],
        [
            ["YELLOW", "RED", "BLACK", "RED"],  # Rotação 0
            ["RED", "BLACK", "RED", "YELLOW"],  # Rotação 1
            ["BLACK", "RED", "YELLOW", "RED"],  # Rotação 2
            ["RED", "YELLOW", "RED", "BLACK"],  # Rotação 3
        ],
    ],
    [
        [29],
        [
            ["WHITE", "BLACK", "RED", "YELLOW"],  # Rotação 0
            ["BLACK", "RED", "YELLOW", "WHITE"],  # Rotação 1
            ["RED", "YELLOW", "WHITE", "BLACK"],  # Rotação 2
            ["YELLOW", "WHITE", "BLACK", "RED"],  # Rotação 3
        ],
    ],
    [
        [31],
        [
            ["WHITE", "BLUE", "RED", "YELLOW"],  # Rotação 0
            ["BLUE", "RED", "YELLOW", "WHITE"],  # Rotação 1
            ["RED", "YELLOW", "WHITE", "BLUE"],  # Rotação 2
            ["YELLOW", "WHITE", "BLUE", "RED"],  # Rotação 3
        ],
    ],
]


# Chega de frente no azul e faz a rotina do azul
def blue_routine(robot: Robot):
    robot.pid_turn(90)
    pid_control = PIDControl(const.PID_WALK_VALUES)
    robot.reset_wheels_angle()
    while (
        robot.color_right.color() != "Color.RED"
        and robot.color_left.color != "Color.RED"
    ):
        robot.loopless_pid_walk(pid_control)
    robot.pid_walk(cm=2, speed=-40)
    robot.align()

    robot.pid_turn(180)
    return "V31"  # Verificar se a virada está com o sinal correto


def black_routine(robot: Robot):
    robot.pid_turn(180)
    pid_control = const.PID_WALK_VALUES

    while (
        robot.color_left.color() == "Color.WHITE"
        or robot.color_right.color() == "Color.WHITE"
    ):
        if (
            robot.color_left.color() in (Color.BLACK, Color.YELLOW)
            and robot.color_right.color() == Color.WHITE
        ):
            # Curva à direita
            robot.pid_turn(20)
        elif (
            robot.color_right.color() in (Color.BLACK, Color.YELLOW)
            and robot.color_left.color() == Color.WHITE
        ):
            # Curva à esquerda
            robot.pid_turn(-20)
        robot.loopless_pid_walk(pid_control)
    robot.stop()

    robot.pid_walk(cm=2, speed=-40)
    robot.align()

    return blue_routine(robot)


def red_routine(robot: Robot):
    robot.pid_walk(cm=30, speed=-60)
    robot.pid_turn(90)
    pid_control = const.PID_WALK_VALUES

    # while wall_color_check() == "WHITE":

    while (
        robot.color_left.color() == Color.WHITE
        or robot.color_right.color() == Color.WHITE
    ):
        if (
            robot.color_left.color() in (Color.BLACK, Color.YELLOW)
            and robot.color_right.color() == Color.WHITE
        ):
            # Curva à direita
            robot.pid_turn(20)
            robot.reset_wheels_angle()
        elif (
            robot.color_right.color() in (Color.BLACK, Color.YELLOW)
            and robot.color_left.color() == Color.WHITE
        ):
            # Curva à esquerda
            robot.pid_turn(-20)
            robot.reset_wheels_angle()
        robot.loopless_pid_walk(pid_control)
    robot.stop()

    robot.pid_walk(cm=2, speed=-40)
    robot.align()
    robot.pid_walk(cm=2, speed=40)

    if wall_colors_check(robot.color_left.color(), robot.color_right.color()) == "BLUE":
        return blue_routine(robot)
    elif (
        wall_colors_check(robot.color_left.color(), robot.color_right.color())
        == "BLACK"
    ):
        return black_routine(robot)


def all_white_routine(robot: Robot):
    pid_control = const.PID_WALK_VALUES
    robot.reset_wheels_angle()
    while (
        robot.color_left.color() != Color.WHITE
        or robot.color_right.color() != Color.WHITE
    ):
        if (
            robot.color_left.color() in (Color.BLACK, Color.YELLOW)
            and robot.color_right.color() == Color.WHITE
        ):
            # Curva à direita
            robot.pid_turn(20)
            robot.reset_wheels_angle()
        elif (
            robot.color_right.color() in (Color.BLACK, Color.YELLOW)
            and robot.color_left.color() == Color.WHITE
        ):
            # Curva à esquerda
            robot.pid_turn(-20)
            robot.reset_wheels_angle()
        robot.loopless_pid_walk(pid_control)
    robot.stop()

    robot.pid_walk(cm=2, speed=-40)
    robot.align()
    robot.pid_walk(cm=2, speed=40)

    if robot.color_left.color() == Color.RED and robot.color_right.color() == Color.RED:
        return red_routine(robot)
    if (
        robot.color_left.color() == Color.BLACK
        and robot.color_right.color() == Color.BLACK
    ):
        return black_routine(robot)
    if (
        robot.color_left.color() == Color.BLUE
        and robot.color_right.color() == Color.BLUE
    ):
        return blue_routine(robot)


def walk_until_non_white(robot: Robot, speed=60):
    """
    Faz o robô andar uma distância de 30 cm ou até que os sensores detectem algo diferente de branco.
    """
    print(robot.color_right.color())

    stop_condition = lambda: (
        robot.color_left.color() != Color.WHITE
        or robot.color_right.color() != Color.WHITE
    )

    has_detected_non_white, _ = robot.pid_walk(
        cm=32,
        speed=speed,
        off_motors=True,
        obstacle_function=stop_condition,
    )


def wall_colors_check(left_color, right_color):
    if Color.YELLOW in (left_color, right_color):
        return "YELLOW"
    if Color.BLACK in (left_color, right_color):
        return "BLACK"
    if Color.RED in (left_color, right_color):
        return "RED"
    if Color.BLUE in (left_color, right_color):
        return "BLUE"
    return "WHITE"


def interprets_list(lista):
    vertices = []
    for i in range(len(color_lateral_vertices)):
        vertice_id, combinacoes = (
            color_lateral_vertices[i][0],
            color_lateral_vertices[i][1],
        )
        for item in combinacoes:
            if lista == item and "V" + str(vertice_id[0]) not in vertices:
                vertices.append("V" + str(vertice_id[0]))
    return vertices


def localization_routine(robot: Robot):
    """
    Faz o robô andar até detectar uma cor diferente de branco, então armazena a cor detectada.
    Ainda não está estruturado como deveria no arquivo localization.py
    """
    lista = []

    for n in range(4):
        obstacle_function = lambda: (
            robot.color_left.color() != Color.WHITE
            or robot.color_right.color() != Color.WHITE
        )

        has_seen_obstacle, walked_perc = robot.pid_walk(
            30,
            obstacle_function=obstacle_function,
        )

        if has_seen_obstacle:
            robot.pid_walk(2, -30)
            robot.align()

        cor = wall_colors_check(robot)

        if cor == "BLUE":
            return blue_routine(robot)
        elif cor == "RED":
            return red_routine(robot)

        lista.append(cor)

        robot.pid_walk(cm=30 * walked_perc, speed=-60)
        robot.pid_turn(90)

    robot.ev3_print("Cores detectadas nos quatro lados:", lista)
    robot.pid_turn(lista.index("WHITE") * 90)
    return all_white_routine(robot)
