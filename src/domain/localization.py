from core.robot import Robot
from pybricks.parameters import Port
from pybricks.ev3devices import ColorSensor

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


def origin_alignment_routine(sandy: Robot, angle = 60):
    sandy.pid_turn(angle=angle)
    sandy.reset_wheels_angle()
    pid = PIDControl(const.PID_WALK_VALUES)
    while sandy.color_left.color() == Color.WHITE:
        sandy.loopless_pid_walk(pid)
    sandy.stop()


# Chega de frente no azul e faz a rotina do azul
def blue_routine(robot: Robot):
    print(robot.color_left.color(), robot.color_right.color())
    robot.pid_walk(cm = const.LINE_TO_CELL_CENTER_DISTANCE, speed = -40)
    robot.pid_turn(-90)
    pid_control = PIDControl(const.PID_WALK_VALUES)
    robot.reset_wheels_angle()
    while ( 
        robot.color_right.color() != Color.RED
        and robot.color_left.color != Color.RED
    ):
        robot.loopless_pid_walk(pid_control, speed=40)
    robot.pid_walk(cm=2, speed=-30)
    robot.align(speed=30)
    robot.pid_turn(90)
    robot.align(40)

    origin_alignment_routine(robot, 90)
    return "V5"  # Verificar se a virada está com o sinal correto


def black_routine(robot: Robot):
    robot.pid_turn(180)
    pid_control = PIDControl(const.PID_WALK_VALUES)

    """
    INÍCIO DA TRATATIVA DE OBSTÁCULO
    
    """
    print("Início da tratativa do preto")

    if robot.ultra_feet.distance() < 160: # Anda próximo o suficiente para identificar
        robot.reset_wheels_angle()
        robot.pid_walk(cm=30, speed=-50) # Volta para o vértice anterior
        # Verificar se está virando à esquerda
        robot.pid_turn(90) 
        
        # Anda para frente para acessar a borda diametralmente oposta
        obstacle_function = lambda: (
            robot.color_left.color() != Color.WHITE
            or robot.color_right.color() != Color.WHITE
        )

        has_seen_obstacle, walked_perc = robot.pid_walk(
            95, 40,
            obstacle_function=obstacle_function,
        )

        if has_seen_obstacle:
            robot.pid_walk(2, -20)
            robot.align(speed=30)
            robot.pid_walk(2,20)

        # Pega o valor da borda lida quando interrompeu 
        cor = wall_colors_check(robot.color_left.color(), robot.color_right.color())
        robot.ev3_print(robot.color_left.color(), robot.color_right.color())

        # Talvez encaixar uma tratativa aqui ainda

        # Verifica se é o vermelho perto e corrige para o longe (se caminhou menos da metade do mapa)
        if cor == "RED":
            if  walked_perc < 0.5:
                robot.reset_wheels_angle()
                robot.pid_walk(150, -40)
            robot.align()
            robot.pid_walk(cm=30, speed=-40) # Anda 30cm para trás para acessar a rua
            robot.turn(-90) # Acessa a rua virando para a "direita agora"

        # Seguir reto até o azul (não sei se é necessário tratar o preto de novo)
        obstacle_function = lambda: (
            robot.color_left.color() != Color.WHITE
            or robot.color_right.color() != Color.WHITE
        )

        has_seen_obstacle, walked_perc = robot.pid_walk(
            95, 40,
            obstacle_function=obstacle_function,
        )

        if has_seen_obstacle:
            robot.pid_walk(2, -20)
            robot.align(speed=30)
            robot.pid_walk(2,20)

        cor = wall_colors_check(robot.color_left.color(), robot.color_right.color())
        robot.ev3_print(robot.color_left.color(), robot.color_right.color())
        # Ativa a blue_routine
        if cor == "BLUE":
            return blue_routine(robot)
        
    """
    FIM DA TRATATIVA, INÍCIO DA ROTINA NORMAL
    """

    robot.reset_wheels_angle() # Resetar ângulo para o PID funcionar corretamente
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
        robot.loopless_pid_walk(pid_control, speed=40)
    robot.stop()

    robot.pid_walk(cm=2, speed=-30)
    robot.align()

    return blue_routine(robot)

def color_multicheck(robot: Robot, times = 1, distance = 2, cor = Color.BLUE):

    for i in range(times):
        if robot.color_left.color() != Color.WHITE:
            robot.pid_walk(distance, speed = 40)
            if robot.color_left.color() == cor:
                return True
        elif robot.color_right.color() != Color.WHITE:
            robot.pid_walk(distance, speed = -40)
            if robot.color_right.color() == cor:
                return True
    return False

def red_routine(robot: Robot):
    robot.pid_walk(cm=30, speed=-50)
    robot.pid_turn(90)

    # """
    # INÍCIO DA TRATATIVA DE OBSTÁCULO
    
    # """
    # print("Início da tratativa do vermelho")
    # if robot.ultra_feet.distance() < 160: # Anda próximo o suficiente para identificar
    #     robot.reset_wheels_angle()
    #     robot.pid_walk(cm=30, speed=-50) # Volta para o vértice anterior
    #     # Verificar se está virando à esquerda
    #     robot.pid_turn(90) 
        
    #     # Anda para frente para acessar a borda diametralmente oposta
    #     obstacle_function = lambda: (
    #         robot.color_left.color() != Color.WHITE
    #         or robot.color_right.color() != Color.WHITE
    #     )

    #     has_seen_obstacle, walked_perc = robot.pid_walk(
    #         95, 40,
    #         obstacle_function=obstacle_function,
    #     )

    #     if has_seen_obstacle:
    #         robot.pid_walk(2, -20)
    #         robot.align(speed=30)
    #         robot.pid_walk(2,20)

    #     # Pega o valor da borda lida quando interrompeu 
    #     cor = wall_colors_check(robot.color_left.color(), robot.color_right.color())
    #     robot.ev3_print(robot.color_left.color(), robot.color_right.color())

    #     # Talvez encaixar uma tratativa aqui ainda

    #     # Verifica se é o vermelho perto e corrige para o longe (se caminhou menos da metade do mapa)
    #     if cor == "RED":
    #         if  walked_perc < 0.5:
    #             robot.reset_wheels_angle()
    #             robot.pid_walk(150, -40)
    #         robot.align()
    #         robot.pid_walk(cm=30, speed=-40) # Anda 30cm para trás para acessar a rua
    #         robot.turn(-90) # Acessa a rua virando para a "direita agora"

    #     # Seguir reto até o azul (não sei se é necessário tratar o preto de novo)
    #     obstacle_function = lambda: (
    #         robot.color_left.color() != Color.WHITE
    #         or robot.color_right.color() != Color.WHITE
    #     )

    #     has_seen_obstacle, walked_perc = robot.pid_walk(
    #         95, 40,
    #         obstacle_function=obstacle_function,
    #     )

    #     if has_seen_obstacle:
    #         robot.pid_walk(2, -20)
    #         robot.align(speed=30)
    #         robot.pid_walk(2,20)

    #     cor = wall_colors_check(robot.color_left.color(), robot.color_right.color())
    #     robot.ev3_print(robot.color_left.color(), robot.color_right.color())
    #     # Ativa a blue_routine
    #     if cor == "BLUE":
    #         return blue_routine(robot)
        
    # """
    # FIM DA TRATATIVA, INÍCIO DA ROTINA NORMAL
    # """

    pid_control = PIDControl(const.PID_WALK_VALUES)
    # Rotina para quando não identifica o obstáculo
    while True:
        robot.loopless_pid_walk(pid_control, speed=50)
        # caso encontre o azul passa para a prox rotina
        if wall_colors_check(
            robot.color_left.color(), robot.color_right.color()
        ) == "BLUE":
            robot.stop()
            robot.ev3_print("Embarque")
            return blue_routine(robot)
        # caso encontre algo diferente de azul
        elif (
            robot.color_left.color(), robot.color_right.color()
        ) not in ("BLUE", "WHITE"):
            # tentar alinhar com a linha encontrada
            robot.stop()
            robot.reset_wheels_angle()
            hard_limit_reached, motor_degree_correction, motor = robot.align(hard_limit = 200)

            # se passar a rotacao do motor passar de um padrao pre estabelecido 
            if hard_limit_reached:
                # o robo sabe que eh estabelecimento
                robot.stop()
                robot.ev3_print("Estabelecimento")
                robot.reset_wheels_angle()
                # corrige o movimento
                if motor == "RIGHT":
                    robot.stop()
                    robot.ev3_print("Corrigindo motor direito")
                    robot.one_wheel_turn("R", motor_degree_correction)
                    robot.pid_walk(cm=5, speed=40)
                    pid_control.reset()
                    robot.reset_wheels_angle()
                else:
                    robot.stop()
                    robot.ev3_print("Corrigindo motor esquerdo")
                    robot.one_wheel_turn("L", motor_degree_correction)
                    robot.pid_walk(cm=5, speed=40)
                    pid_control.reset()
                    robot.reset_wheels_angle()
            
            else:
                # embarque ou parque
                robot.stop()
                robot.pid_walk(cm=3, speed=40)
                if wall_colors_check(
                    robot.color_left.color(), robot.color_right.color()
                ) == "BLUE":
                    robot.ev3_print("Embarque")
                    robot.stop()
                    return blue_routine(robot)
                else:
                    robot.ev3_print("Parque")
                    robot.pid_walk(cm=const.LINE_TO_CELL_CENTER_DISTANCE, speed=-40)
                    robot.pid_turn(180)
                    pid_control.reset()
                    robot.reset_wheels_angle()
                


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
    robot.pid_walk(cm=2, speed=50)

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
            30, 40,
            obstacle_function=obstacle_function,
        )

        if has_seen_obstacle:
            robot.pid_walk(2, -20)
            robot.align(speed=30)
            robot.pid_walk(2,20)

        cor = wall_colors_check(robot.color_left.color(), robot.color_right.color())
        robot.ev3_print(robot.color_left.color(), robot.color_right.color())
        
        lista.append(cor)
        
        if cor == "BLUE":
            robot.ev3_print("Starting blue routine")
            return blue_routine(robot)
        elif cor == "RED":
            robot.ev3_print("Starting red routine")
            return red_routine(robot)


        robot.pid_walk(cm=30 * walked_perc, speed=-40)
        robot.pid_turn(90)

    robot.ev3_print("Cores detectadas nos quatro lados:", lista)
    robot.pid_turn(lista.index("WHITE") * 90)
    return all_white_routine(robot)
