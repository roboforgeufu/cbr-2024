from core.omni_robot import OmniRobot
import constants as const
from pybricks.parameters import Color

from domain.path_control import (
    walls_of_vertices,
    possible_obstacles_vertices,
    possible_directions,
    wall_colors,
    get_side_directions,
)


def omni_turn_to_direction(robot: OmniRobot, target_direction):
    """Considerando a orientação atual do robô, faz uma curva para colocá-lo na orientação desejada (retorna True caso seja necessário o robô se mover ao contrário, False se não)"""
    if robot.orientation is None:
        raise ValueError("É esperado que o robô conheça sua orientação.")

    current_position_index = possible_directions.index(robot.orientation)
    target_position_index = possible_directions.index(target_direction)

    turn_times = current_position_index - target_position_index

    robot.ev3_print("turn_times:", turn_times)

    turn_times_sign = 1 if turn_times == 0 else turn_times / abs(turn_times)
    if abs(turn_times) == 3:
        turn_times = 1 * -turn_times_sign

    robot.pid_turn(-90 * turn_times)
    robot.orientation = target_direction


def omni_path_control(robot: OmniRobot, path: list, directions: list):
    """
    Rotina pro robô OMNIDIRECIONAL seguir o caminho traçado, seguindo o conjunto de direções determinado.
    """
    position_index = 0

    for idx, (direction, distance) in enumerate(directions):
        robot.ev3_print("Current position:", path[position_index])
        robot.ev3_print("STEP:", direction, distance)
        turn_to_direction(robot, direction)

        if idx == len(directions) - 1:
            # nao anda a ultima distancia, pra nao entrar no estabelecimento
            break

        # Confere se a próxima movimentação é na mesma direção que a atual.
        should_stop = True
        if idx + 1 < len(directions) and directions[idx + 1][0] == direction:
            # Caso seja, o robô não desliga os motores entre as movimentações.
            should_stop = False

        obstacle_function = (
            lambda: robot.color_left.color() in wall_colors
            or robot.color_right.color() in wall_colors
        )
        has_seen_obstacle, walked_perc = robot.pid_walk(
            distance,
            off_motors=should_stop,
            obstacle_function=obstacle_function,
        )
        while has_seen_obstacle:
            robot.off_motors()
            if robot.color_left.color() in wall_colors:
                # Alinhamento à esquerda
                robot.ev3_print("à esquerda")
                robot.pid_turn(20)
                has_seen_obstacle, walked_perc = robot.pid_walk(
                    cm=distance * (1 - walked_perc),
                    off_motors=should_stop,
                    obstacle_function=obstacle_function,
                )
            elif robot.color_right.color() in wall_colors:
                # Alinhamento à direita
                robot.ev3_print("à direita")
                robot.pid_turn(-20)
                has_seen_obstacle, walked_perc = robot.pid_walk(
                    cm=distance * (1 - walked_perc),
                    off_motors=should_stop,
                    obstacle_function=obstacle_function,
                )

        position_index += 1

        new_position = path[position_index]
        if robot.orientation in walls_of_vertices[new_position]:
            # O robô está de frente pra uma parede, aproveita pra alinhar a frente
            robot.off_motors()
            robot.align()
            robot.pid_walk(const.ROBOT_SIZE_HALF, speed=-60)
