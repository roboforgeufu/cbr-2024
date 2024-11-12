from core.robot import Robot
import constants as const
from pybricks.parameters import Color


walls_of_vertices = {
    1: ["N", "L", "O"],
    3: ["N", "L", "O"],
    5: ["N", "L", "O"],
    7: ["O"],
    8: ["N", "S"],
    9: [],
    10: ["N", "S"],
    11: ["L"],
    14: ["L", "O"],
    16: ["L", "O"],
    18: ["L", "O"],
    20: ["O"],
    21: ["N", "S"],
    22: [],
    23: ["N", "S"],
    24: ["L"],
    27: ["L", "O", "S"],
    29: ["L", "O", "S"],
    31: ["L", "O", "S"],
}

possible_obstacles_vertices = [1, 3, 8, 10, 14, 16, 21, 23, 27, 29]
possible_directions = ["N", "L", "S", "O"]  # sentido horário


wall_colors = [Color.BLACK, Color.BLUE, Color.RED, Color.YELLOW, Color.BROWN]


def get_side_directions(robot_orientation: str):
    """Considerando a orientação atual do robô, retorna as direções laterais a ele.
    A primeira posição será a direção à direita do robô, a segunda posição será a direção à esquerda do robô
    Exemplos:
        Se o robô aponta para o Norte, as laterais são Leste e Oeste.
        Se o robô aponta para o Leste, as laterais são Sul e Norte.
    """
    orientation_idx = possible_directions.index(robot_orientation)
    return [
        possible_directions[(orientation_idx + 1) % 4],
        possible_directions[(orientation_idx - 1) % 4],
    ]


def get_relative_orientation(orientation: str, offset: int):
    """Retorna a orientação relativa à orientação passada, considerando um offset.
    Exemplos:
        get_relative_orientation("N", 1) == "L"
        get_relative_orientation("N", -1) == "O"
    """
    return possible_directions[(possible_directions.index(orientation) + offset) % 4]


def turn_to_direction(robot: Robot, target_direction):
    """Considerando a orientação atual do robô, faz uma curva para colocá-lo na orientação desejada"""
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


def path_control(robot: Robot, path: list, directions: list):
    """
    Rotina pro robô seguir o caminho traçado, seguindo o conjunto de direções determinado.
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
            or robot.ultra_feet.distance() < const.OBSTACLE_DISTANCE
        )
        has_seen_obstacle, walked_perc = robot.pid_walk(
            distance,
            off_motors=should_stop,
            obstacle_function=obstacle_function,
        )
        while has_seen_obstacle:
            robot.stop()
            if robot.ultra_feet.distance() < const.OBSTACLE_DISTANCE:
                robot.ev3_print("obstáculo à frente")
                has_seen_obstacle, walked_perc = robot.pid_walk(
                    cm=distance * (1 - walked_perc),
                    off_motors=should_stop,
                    obstacle_function=obstacle_function,
                )
                return False, position_index
            elif robot.color_left.color() in wall_colors:
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
            robot.stop()
            robot.align()
            robot.pid_walk(const.ROBOT_SIZE_HALF, speed=-60)

        if idx == len(path) - 1:
            robot.off_motors()
            return True, position_index
