from core.omni_robot import OmniRobot, Direction
import constants as const
from pybricks.parameters import Color

from domain.path_control import (
    walls_of_vertices,
    possible_obstacles_vertices,
    possible_directions,
    wall_colors,
    get_side_directions,
    get_relative_orientation,
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
    return turn_times


def get_obstacle_sensor_msg_and_distance(robot: OmniRobot):
    if robot.moving_direction_sign == 1:
        return "ULTRA_FRONT", const.OMNI_OBSTACLE_FRONT_DISTANCE
    return "ULTRA_BACK", const.OMNI_OBSTACLE_BACK_DISTANCE


def omni_path_control(robot: OmniRobot, path: list, directions: list):
    """
    Rotina pro robô OMNIDIRECIONAL seguir o caminho traçado, seguindo o conjunto de direções determinado.

    Retorna um booleano que representa se conseguiu terminar o caminho e o índice da posição em que terminou (se a frente de obstáculo o obstáculo está na próxima posição, se a frente de estabelecimento o estabelecimento está na próxima posição).
    Exemplo:
        True, 23 # O robô conseguiu terminar o caminho e está a frente da posição de índice 23
        False, 24 # O robô não conseguiu terminar o caminho por detectar um obstáculo e está na posição de índice 24

    """
    position_index = 0

    needs_align = 0
    for idx, (direction, distance) in enumerate(directions):
        distance *= const.OMNI_WALK_DISTANCE_CORRECTION

        robot.ev3_print("Current position:", path[position_index])
        robot.ev3_print("STEP:", direction)
        robot.ev3_print("Needs align:", needs_align)
        turn_times = omni_turn_to_direction(robot, direction)

        if turn_times != 0:
            needs_align += 1

        omni_direction = (
            Direction.FRONT if robot.moving_direction_sign == 1 else Direction.BACK
        )
        if (
            get_relative_orientation(robot.orientation, 2)
            in walls_of_vertices[path[position_index]]
        ):
            # O robô está de costas pra uma parede, aproveita pra alinhar atrás
            robot.ev3_print("WALL BACKWARDS")
            robot.off_motors()
            robot.align(Direction.get_relative_direction(omni_direction, 4))
            needs_align = 0
            robot.pid_walk(
                const.ROBOT_SIZE_HALF,
                speed=60,
                direction=omni_direction,
                off_motors=False,
            )

        if idx == len(directions) - 1:
            # nao anda a ultima distancia, pra nao entrar no estabelecimento
            robot.off_motors()
            return True, position_index

        # Confere se a próxima movimentação é na mesma direção que a atual, pra não desligar os motores entre elas.
        should_stop = True
        if idx + 1 < len(directions) and directions[idx + 1][0] == direction:
            # Caso seja, o robô não desliga os motores entre as movimentações.
            should_stop = False

        sensor_left, sensor_right = robot.get_sensors_towards_direction(omni_direction)

        sensor_msg, obstacle_distance = get_obstacle_sensor_msg_and_distance(robot)

        robot.bluetooth.message(sensor_msg)
        obstacle_function = (
            lambda: sensor_left.color() in wall_colors
            or sensor_right.color() in wall_colors
            or (
                (
                    robot.bluetooth.message(should_wait=False) or 2550
                )  # tratativa pra não comparar com None
                <= obstacle_distance
            )
        )

        has_seen_obstacle, walked_perc = robot.pid_walk(
            distance,
            off_motors=should_stop,
            obstacle_function=obstacle_function,
            direction=omni_direction,
        )
        while has_seen_obstacle:
            robot.off_motors()
            robot.ev3_print("Obs.:", sensor_left.color(), sensor_right.color())
            right_direction, left_direction = get_side_directions(robot.orientation)
            relative_right = Direction.get_relative_direction(omni_direction, 2)
            relative_left = Direction.get_relative_direction(omni_direction, -2)

            if (
                position_index + 1 < len(path)
                and path[position_index + 1] in possible_obstacles_vertices
                and robot.bluetooth.message(should_wait=False) <= obstacle_distance
            ):
                # Obstáculo à frente
                robot.bluetooth.message("STOP")
                robot.ev3_print("à frente:", walked_perc)
                robot.pid_walk(
                    distance * walked_perc,
                    direction=Direction.get_relative_direction(omni_direction, 4),
                )
                return (False, position_index)
            elif (
                sensor_left.color() in wall_colors
                and sensor_right.color() in wall_colors
            ):
                # Os dois sensores leram parede; apenas continua
                robot.ev3_print("BOTH SIDES")
                robot.ev3.speaker.beep(100)
                if walked_perc >= 0.8:
                    oposite_direction = Direction.get_relative_direction(
                        omni_direction, 4
                    )
                    robot.pid_walk(2, direction=oposite_direction)
                    has_seen_obstacle = False
                else:
                    robot.ev3_print("Walked perc:", walked_perc)
                    robot.wait_button()
            elif sensor_left.color() in wall_colors:
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
                    needs_align = 0
                    robot.pid_walk(cm=const.ROBOT_SIZE_HALF, direction=relative_right)
                else:
                    robot.pid_turn(20)
                    needs_align += 1

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
                    # Se tiver parede à direita, e se tiver concluído mais de 50% da distancia, alinha na parede
                    robot.pid_walk(cm=2, direction=relative_left)
                    robot.align(relative_right)
                    needs_align = 0
                    robot.pid_walk(cm=const.ROBOT_SIZE_HALF, direction=relative_left)
                else:
                    robot.pid_turn(-20)
                    needs_align += 1

                has_seen_obstacle, walked_perc = robot.pid_walk(
                    cm=distance * (1 - walked_perc),
                    off_motors=should_stop,
                    obstacle_function=obstacle_function,
                    direction=omni_direction,
                )
            else:
                break

        robot.bluetooth.message("STOP")

        position_index += 1

        new_position = path[position_index]
        if robot.orientation in walls_of_vertices[new_position]:
            # O robô está de frente pra uma parede, aproveita pra alinhar a frente
            robot.ev3_print("WALL IN FRONT")
            robot.off_motors()
            robot.align(omni_direction)
            needs_align = 0
            robot.pid_walk(const.ROBOT_SIZE_HALF, speed=-60, direction=omni_direction)
        elif needs_align >= 1:
            for i, side_orientation in enumerate(
                get_side_directions(robot.orientation)
            ):
                if side_orientation in walls_of_vertices[new_position]:
                    robot.off_motors()
                    robot.pid_walk(
                        5, direction=Direction.get_relative_direction(omni_direction, 4)
                    )
                    align_direction = Direction.get_relative_direction(
                        omni_direction,
                        # pra direita (i = 0), deve ser 2
                        # pra esquerda (i = 1), deve ser 6
                        2 + i * 4,
                    )
                    oposite_direction = Direction.get_relative_direction(
                        align_direction, 4
                    )
                    robot.align(direction=align_direction)
                    robot.pid_walk(const.ROBOT_SIZE_HALF, direction=oposite_direction)
                    needs_align = 0
                    break
