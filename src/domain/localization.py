from core.robot import Robot
from pybricks.parameters import Port
from pybricks.ev3devices import ColorSensor
from pybricks.tools import wait

import constants as const
from pybricks.parameters import Color
from time import time, sleep
from core.utils import PIDControl

#TODO tratar obstáculos nas routines
#TODO refazer tratativa do alinhamento

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

def localization_routine(robot: Robot):
    """
    Faz o robô andar até detectar uma cor diferente de branco, então armazena a cor detectada.
    Ainda não está estruturado como deveria no arquivo localization.py
    """
    lista = []
    street_obstacle = False
    street_side = 1
    # checa as cores das 4 direções inciais do robo
    for n in range(4):
        print("{}ª iteração!".format(n+1))
        cor = "WHITE"
        obstacle_function = lambda: (
            wall_colors_check(robot.color_left.color(),
            robot.color_right.color()) != "WHITE"
            or robot.ultra_feet.distance() < const.SANDY_OBSTACLE_DISTANCE
        )
        has_seen_obstacle, walked_perc, _ = robot.pid_walk(
            cm = 20, 
            speed = const.ROBOT_SPEED,
            obstacle_function=obstacle_function,
        )
        # caso veja alguma cor, alinhe
        if has_seen_obstacle and wall_colors_check(robot.color_left.color(), robot.color_right.color()) != "WHITE":
            print("Viu cor")
            robot.ev3_print(robot.color_left.color(), robot.color_right.color())
            robot.pid_walk(cm = 5, speed =-30)
            print("Alinhando")
            robot.align(speed = 30)
            robot.pid_walk(cm = 2, speed = 30)
            # guarda a cor lida
            cor = wall_colors_check(robot.color_left.color(), robot.color_right.color())
        
        elif has_seen_obstacle and robot.ultra_feet.distance() < const.SANDY_OBSTACLE_DISTANCE:
            robot.ev3_print("Obstacle", robot.ultra_feet.distance())
            robot.ev3.speaker.beep()
            cor = "BLACK"

        if cor == "BLUE":
            robot.ev3_print("Starting blue routine")
            return blue_routine(robot)
        elif cor == "RED":
            robot.ev3_print("Starting red routine")
            return red_routine(robot, street_obstacle, street_side)
        
        robot.pid_walk(cm=20 * walked_perc, speed=-const.ROBOT_SPEED)
        robot.ev3_print(robot.color_left.color(), robot.color_right.color(), wall_colors_check(robot.color_left.color(), robot.color_right.color()))
        robot.pid_turn(90)

        lista.append(cor)

    robot.ev3_print("Cores detectadas nos quatro lados:", lista)
    robot.pid_turn(lista.index("WHITE") * 90)
    return all_white_routine(robot, street_obstacle, street_side)


def all_white_routine(robot: Robot, street_obstacle, street_side):
    pid_control = PIDControl(const.PID_WALK_VALUES)
    pid_control.reset()
    robot.reset_wheels_angle()
    # Rotina para quando não identifica o obstáculo
    while True:
        robot.loopless_pid_walk(pid_control, speed=const.ROBOT_SPEED)
        if wall_colors_check(robot.color_left.color(), robot.color_right.color()) != "WHITE":
            robot.reset_wheels_angle()
            robot.pid_walk(2, -30)
            hard_limit_reached, motor_degree_correction, motor = robot.align(hard_limit = 180)
            # se passar a rotacao do motor passar de um padrao pre estabelecido 
            if hard_limit_reached:
                    print("Correção:", motor, motor_degree_correction)
                    # o robô sabe que é estabelecimento
                    robot.stop()
                    robot.ev3_print("Estabelecimento")
                    robot.reset_wheels_angle()
                    # corrige o movimento
                    if motor == "RIGHT":
                        robot.stop()
                        robot.ev3_print("Corrigindo motor direito")
                        robot.one_wheel_turn("R", motor_degree_correction*1.25)
                        robot.pid_walk(cm=5, speed=40)
                        pid_control.reset()
                        robot.reset_wheels_angle()
                    else:
                        robot.stop()
                        robot.ev3_print("Corrigindo motor esquerdo")
                        motor_degree_correction *= -1
                        robot.one_wheel_turn("L", motor_degree_correction*1.25)
                        robot.pid_walk(cm=5, speed=40)
                        pid_control.reset()
                        robot.reset_wheels_angle()
            else:
                robot.pid_walk(2, 30)
                if wall_colors_check(
                    robot.color_left.color(), robot.color_right.color()
                ) == "BLUE":
                    # caso encontre o azul passa para a prox rotina
                    robot.stop()
                    robot.ev3_print("Embarque")
                    return blue_routine(robot)
                
                elif wall_colors_check(
                    robot.color_left.color(), robot.color_right.color()
                ) == "RED":
                    # caso encontre o azul passa para a prox rotina
                    robot.stop()
                    robot.ev3_print("Vermelho")
                    return red_routine(robot)
                else:
                    # caso encontre algo diferente de azul
                    # parque
                    robot.ev3_print("Parque")
                    robot.pid_walk(cm=const.LINE_TO_CELL_CENTER_DISTANCE, speed=-40)
                    robot.pid_turn(90)
                    robot.pid_turn(90)
                    if street_obstacle:
                        robot.pid_walk(cm = const.CELL_DISTANCE, speed=const.ROBOT_SPEED)
                        robot.pid_turn(90 * street_side)
                    pid_control.reset()
                    robot.reset_wheels_angle()
        elif robot.ultra_feet.distance() <= const.SANDY_OBSTACLE_DISTANCE:
            print("Obstacle")
            robot.pid_walk(const.OBSTACLE_DISTANCE_TO_CELL, -40)
            robot.pid_turn(90)
            robot.pid_walk(const.CELL_DISTANCE * 2, const.ROBOT_SPEED)
            robot.pid_turn(-90)
            robot.reset_wheels_angle()
            


def red_routine(robot: Robot, street_obstacle, street_side):
    robot.ev3_print("Início da red routine")
    robot.pid_walk(cm=const.LINE_TO_CELL_CENTER_DISTANCE + const.CELL_DISTANCE, speed=-40)
    print("Ativou o pid walk")
    robot.pid_turn(90)
    print("Gira 90")

    # """
    # RED ROUTINE SEM TRATATIVA DE OBSTÁCULO
    # """

    pid_control = PIDControl(const.PID_WALK_VALUES)
    pid_control.reset()
    robot.reset_wheels_angle()
    # Rotina para quando não identifica o obstáculo
    street_side = 1
    while True:
        robot.loopless_pid_walk(pid_control, speed=const.ROBOT_SPEED)
        if wall_colors_check(robot.color_left.color(), robot.color_right.color()) != "WHITE":
            robot.reset_wheels_angle()
            robot.pid_walk(2, -30)
            hard_limit_reached, motor_degree_correction, motor = robot.align(hard_limit = 180)
            # se passar a rotacao do motor passar de um padrao pre estabelecido 
            if hard_limit_reached:
                    print("Correção:", motor, motor_degree_correction)
                    # o robô sabe que é estabelecimento
                    robot.stop()
                    robot.ev3_print("Estabelecimento")
                    robot.reset_wheels_angle()
                    # corrige o movimento
                    if motor == "RIGHT":
                        robot.stop()
                        robot.ev3_print("Corrigindo motor direito")
                        robot.one_wheel_turn("R", motor_degree_correction*1.30)
                        robot.pid_walk(cm=5, speed=40)
                        pid_control.reset()
                        robot.reset_wheels_angle()
                    else:
                        robot.stop()
                        robot.ev3_print("Corrigindo motor esquerdo")
                        robot.one_wheel_turn("L", -motor_degree_correction*1.30)
                        robot.pid_walk(cm=5, speed=40)
                        pid_control.reset()
                        robot.reset_wheels_angle()
            else:
                robot.pid_walk(2, 30)
                if wall_colors_check(
                    robot.color_left.color(), robot.color_right.color()
                ) == "BLUE":
                    # caso encontre o azul passa para a prox rotina
                    print("Viu azul")
                    robot.stop()
                    robot.ev3_print("Embarque")
                    return blue_routine(robot)
                
                else:
                    # caso encontre algo diferente de azul
                    # parque
                    print("Não leu azul nem branco")
                    robot.ev3_print("Parque")
                    robot.pid_walk(cm=const.LINE_TO_CELL_CENTER_DISTANCE, speed=-const.ROBOT_SPEED)
                    robot.pid_turn(90)
                    robot.pid_turn(90)
                    pid_control.reset()
                    robot.reset_wheels_angle()
                    street_side *= -1

        elif robot.ultra_feet.distance() <= const.SANDY_OBSTACLE_DISTANCE:
            print("Obstacle")
            # Volta ao ver o obstáculo
            robot.pid_walk(const.OBSTACLE_DISTANCE_TO_CELL + 6, -const.ROBOT_SPEED)
            # Curva pra cima
            robot.pid_turn(90 * street_side)
            # Atravessa para a outra rua, a menos que veja outro obstáculo
            obstacle_function = lambda: (
            robot.ultra_feet.distance() < const.SANDY_OBSTACLE_DISTANCE
            )
            has_seen_obstacle, walked_perc, _ = robot.pid_walk(
            cm = const.CELL_DISTANCE * 2, 
            speed = const.ROBOT_SPEED,
            obstacle_function=obstacle_function,
            )
            if has_seen_obstacle:
                # Volta em direção ao parque
                robot.pid_walk(const.CELL_DISTANCE * 2 * walked_perc, -const.ROBOT_SPEED)
                robot.pid_turn(90 * street_side)
                street_side *= -1
                street_obstacle = True
                return all_white_routine(robot, street_obstacle, street_side)
            
            robot.reset_wheels_angle()
            street_side *= -1


def blue_routine(robot: Robot):
    # começa com os sensores em cima do azul
    print(robot.color_left.color(), robot.color_right.color())
    robot.pid_walk(cm = const.LINE_TO_CELL_CENTER_DISTANCE, speed = -40)
    robot.align(40)
    robot.pid_walk(cm = const.LINE_TO_CELL_CENTER_DISTANCE, speed = -40)
    robot.pid_turn(-90)
    # indo em direcao ao vermelho
    pid_control = PIDControl(const.PID_WALK_VALUES)
    robot.reset_wheels_angle()
    while ( 
        robot.color_right.color() != Color.RED
        and robot.color_left.color != Color.RED
    ):
        robot.loopless_pid_walk(pid_control, speed=40)
        if wall_colors_check(robot.color_left.color(), robot.color_right.color()) =="BLUE":
            robot.pid_walk(5, -40)
            robot.pid_turn(-20)
            robot.ev3_print(wall_colors_check(robot.color_left.color(), robot.color_right.color()))
            robot.reset_wheels_angle()
        if wall_colors_check(robot.color_left.color(), robot.color_right.color()) =="BLACK":
            robot.pid_walk(5, -40)
            robot.pid_turn(20)
            robot.ev3_print(wall_colors_check(robot.color_left.color(), robot.color_right.color()))
            robot.reset_wheels_angle()

    # alinha com o vermelho
    robot.pid_walk(cm=3, speed=-30)
    print("Andou 2cm")
    robot.align(30)
    print("Alinhou")
    robot.pid_walk(cm = const.LINE_TO_CELL_CENTER_DISTANCE-5, speed = -30)
    origin_alignment_routine(robot)

    return "V5"  # Verificar se a virada está com o sinal correto


def origin_alignment_routine(sandy: Robot):
    # alinhar com o azul
    sandy.pid_turn(90)
    sandy.align(30)
    print("Alinhou")
    # posiciona o sensor em cima da linha para seguir
    sandy.pid_walk(2, -30)
    sandy.pid_turn(90)
    sandy.pid_walk(6, -30)
    sandy.reset_wheels_angle()
    sandy.stop()


def wall_colors_check(left_color, right_color):
    color_str = "WHITE"
    if Color.YELLOW in (left_color, right_color):
        color_str = "YELLOW"
    if Color.BLACK in (left_color, right_color):
        color_str = "BLACK"
    if Color.RED in (left_color, right_color):
        color_str = "RED"
    if Color.BLUE in (left_color, right_color):
        color_str = "BLUE"
    return color_str


def walk_until_non_white(robot: Robot, speed=60):
   
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


"""def interprets_list(lista):
    vertices = []
    for i in range(len(color_lateral_vertices)):
        vertice_id, combinacoes = (
            color_lateral_vertices[i][0],
            color_lateral_vertices[i][1],
        )
        for item in combinacoes:
            if lista == item and "V" + str(vertice_id[0]) not in vertices:
                vertices.append("V" + str(vertice_id[0]))
    return vertices"""
