from core.omni_robot import OmniRobot, Direction
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
    """Considerando a orientação atual do robô, faz uma curva para colocá-lo na orientação desejada. Inverte o sentido do robô ao invés de uma curva de 180 graus."""
    if robot.orientation is None:
        raise ValueError("É esperado que o robô conheça sua orientação.")

    current_position_index = possible_directions.index(robot.orientation)
    target_position_index = possible_directions.index(target_direction)

    turn_times = current_position_index - target_position_index

    turn_times_sign = 1 if turn_times == 0 else turn_times / abs(turn_times)
    if abs(turn_times) == 3:
        turn_times = 1 * -turn_times_sign

    if abs(turn_times) == 2:
        robot.moving_direction_sign *= -1
        turn_times = 0

    if turn_times != 0:
        robot.pid_turn(-90 * turn_times)
    robot.orientation = target_direction


def omni_path_control(robot: OmniRobot, path: list, directions: list):
    """
    Rotina pro robô OMNIDIRECIONAL seguir o caminho traçado, seguindo o conjunto de direções determinado.
    """
    position_index = 0

    for idx, (direction, distance) in enumerate(directions):
        distance *= const.OMNI_WALK_DISTANCE_CORRECTION

        robot.ev3_print("Current position:", path[position_index])
        robot.ev3_print("STEP:", direction)
        omni_turn_to_direction(robot, direction)

        if idx == len(directions) - 1:
            # nao anda a ultima distancia, pra nao entrar no estabelecimento
            robot.off_motors()
            break

        # Confere se a próxima movimentação é na mesma direção que a atual, pra não desligar os motores entre elas.
        should_stop = True
        if idx + 1 < len(directions) and directions[idx + 1][0] == direction:
            # Caso seja, o robô não desliga os motores entre as movimentações.
            should_stop = False

        omni_direction = (
            Direction.FRONT if robot.moving_direction_sign == 1 else Direction.BACK
        )
        sensor_left, sensor_right = robot.get_sensors_towards_direction(omni_direction)
        obstacle_function = (
            lambda: sensor_left.color() in wall_colors
            or sensor_right.color() in wall_colors
        )

        has_seen_obstacle, walked_perc = robot.pid_walk(
            distance,
            off_motors=should_stop,
            obstacle_function=obstacle_function,
            direction=omni_direction,
        )
        while has_seen_obstacle:
            robot.off_motors()
            robot.ev3_print("SEEN OBSTACLE:", sensor_left.color(), sensor_right.color())
            right_direction, left_direction = get_side_directions(robot.orientation)
            relative_right = Direction.get_relative_direction(omni_direction, 2)
            relative_left = Direction.get_relative_direction(omni_direction, -2)
            if sensor_left.color() in wall_colors:
                # Desvio à esquerda
                robot.ev3_print("à esquerda:", walked_perc)

                if (
                    left_direction in walls_of_vertices[path[position_index]]
                    and walked_perc < const.OMNI_SIDE_ALING_PERCENTAGE
                ) or (
                    position_index + 1 < len(path)
                    and left_direction in walls_of_vertices[path[position_index + 1]]
                    and walked_perc > const.OMNI_SIDE_ALING_PERCENTAGE
                ):
                    # Se tiver parede à esquerda, e se tiver concluído mais de 50% da distancia, alinha na parede
                    robot.pid_walk(cm=2, direction=relative_right)
                    robot.align(relative_left)
                    robot.pid_walk(cm=const.ROBOT_SIZE_HALF, direction=relative_right)
                else:
                    robot.pid_turn(20)

                has_seen_obstacle, walked_perc = robot.pid_walk(
                    cm=distance * (1 - walked_perc),
                    off_motors=should_stop,
                    obstacle_function=obstacle_function,
                    direction=omni_direction,
                )
            elif sensor_right.color() in wall_colors:
                # Desvio à direita
                robot.ev3_print("à direita:", walked_perc)

                if (
                    right_direction in walls_of_vertices[path[position_index]]
                    and walked_perc < const.OMNI_SIDE_ALING_PERCENTAGE
                ) or (
                    position_index + 1 < len(path)
                    and right_direction in walls_of_vertices[path[position_index + 1]]
                    and walked_perc > const.OMNI_SIDE_ALING_PERCENTAGE
                ):
                    # Se tiver parede à esquerda, e se tiver concluído mais de 50% da distancia, alinha na parede
                    robot.pid_walk(cm=2, direction=relative_left)
                    robot.align(relative_right)
                    robot.pid_walk(cm=const.ROBOT_SIZE_HALF, direction=relative_right)
                else:
                    robot.pid_turn(-20)

                has_seen_obstacle, walked_perc = robot.pid_walk(
                    cm=distance * (1 - walked_perc),
                    off_motors=should_stop,
                    obstacle_function=obstacle_function,
                    direction=omni_direction,
                )

        position_index += 1

        new_position = path[position_index]
        if robot.orientation in walls_of_vertices[new_position]:
            # O robô está de frente pra uma parede, aproveita pra alinhar a frente
            robot.off_motors()
            robot.align(omni_direction)
            robot.pid_walk(const.ROBOT_SIZE_HALF, speed=-60, direction=omni_direction)
