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
    return turn_times


def future_possible_alignment(initial_position_idx: int, path: list, directions: list, depth = 5):
    position = directions[initial_position_idx][0]
    
    for index in range(initial_position_idx, initial_position_idx + depth):
        if index >= len(path) - 1:  
            return False
        if directions[index][0] == position:
            continue
        
        print('future alignment', end=' ')
        print(position in walls_of_vertices[path[index]])
        
        return position in walls_of_vertices[path[index]]
    

def align_side(robot: Robot, side: str):
    print_str = "Align right" if side == "right" else "Align left"
    mult = 1 if side == "right" else -1
    robot.ev3_print(print_str)
    robot.pid_turn(mult * 90)
    robot.pid_walk(
        cm=5,
        speed=-40,
    )
    robot.align(speed=30)
    robot.pid_walk(
        (const.CELL_DISTANCE / 2),
        speed=-50,
    )
    robot.pid_turn(mult * (-90))


def path_control(robot: Robot, path: list, directions: list):
    """
    Rotina pro robô seguir o caminho traçado, seguindo o conjunto de direções determinado.
    """
    # inicia o idx da lista como 0 e a necessidade de alinhar
    position_index = 0
    needs_align = 0
    for idx, (direction, distance) in enumerate(directions):
        robot.ev3_print("Current position:", path[position_index])
        robot.ev3_print("Step:", direction, distance)

        # apos alinhar procura por possiveis alinhamentos
        if needs_align == 0:
            alignment_found = False
        # se houver possibilidade de alinhamentos faceis no futuro, nao alinhar
        if not alignment_found and future_possible_alignment(position_index, path, directions):
            needs_align = 0
            alignment_found = True

        # caso a orientacao do robo coincida com uma parede, alinhe
        if (robot.orientation in walls_of_vertices[path[position_index]]):
            robot.ev3_print("Align front")
            robot.stop()
            robot.align(speed=30)
            robot.pid_walk(
                const.ROBOT_SIZE_HALF,
                speed=-50,
            )
            needs_align = 0

        turn_times = turn_to_direction(robot, direction)
        if turn_times != 0:
            needs_align += 1
        
        # # caso a orientacao nao coincida alinha na prox parede disponivel
        # if (needs_align >= 2):
        #     if (
        #         get_relative_orientation(robot.orientation, 1)
        #         in walls_of_vertices[path[position_index]]
        #     ):
        #         align_side(robot, "right")
        #     elif (
        #         get_relative_orientation(robot.orientation, -1)
        #         in walls_of_vertices[path[position_index]]
        #     ):
        #         align_side(robot, "left")
        #     needs_align = 0

        if idx == len(directions) - 1:
            # nao anda a ultima distancia, pra nao entrar no estabelecimento
            return True, position_index

        # Confere se a próxima movimentação é na mesma direção que a atual.
        should_stop = True
        if idx + 1 < len(directions) and directions[idx + 1][0] == direction:
            # Caso seja, o robô não desliga os motores entre as movimentações.
            should_stop = False

        # procura obstaculos no caminho e trtar bater com um sensor em estabelecimento
        obstacle_function = (
            lambda: robot.color_left.color() in wall_colors
            or robot.color_right.color() in wall_colors
            or (robot.ultra_feet.distance() < const.OBSTACLE_DISTANCE
            and path[position_index + 1] in possible_obstacles_vertices)
        )
        has_seen_obstacle, walked_perc = robot.pid_walk(
            distance,
            40,
            off_motors=should_stop,
            obstacle_function=obstacle_function,
        )
        # caso veja um obstaculo volta a porcentagem do ultimo movimento e recalcula a rota
        while has_seen_obstacle:
            robot.stop()
            if (robot.ultra_feet.distance() < const.OBSTACLE_DISTANCE
                and path[position_index + 1] in possible_obstacles_vertices):
                robot.ev3_print("Obstacle")
                has_seen_obstacle, walked_perc = robot.pid_walk(
                    cm=distance * walked_perc,
                    speed = -60,
                    off_motors=should_stop,
                    obstacle_function=obstacle_function,
                )
                return False, position_index
            # bateu com o sensor direito em um estabelecimento
            elif robot.color_right.color() in wall_colors:
                # caso veja estabelecimento com o sensor direito segue a linha até ver branco 
                robot.line_follower(
                    sensor = robot.color_right,
                    speed = 40,
                    loop_condition_function = lambda: robot.color_right.color()
                    != Color.WHITE
                    and robot.color_left.color() == Color.WHITE,
                    error_function=lambda: robot.color_right.rgb()[2],
                    side="R",
                )
            elif robot.color_left.color() in wall_colors:
                # caso veja estabelecimento com o sensor esquerdo segue a linha até ver branco 
                robot.line_follower(
                    sensor = robot.color_left,
                    speed = 40,
                    loop_condition_function = lambda: robot.color_left.color()
                    != Color.WHITE
                    and robot.color_right.color() == Color.WHITE,
                    error_function=lambda: robot.color_left.rgb()[2],
                    side="L",
                )

        position_index += 1
