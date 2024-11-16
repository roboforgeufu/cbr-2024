import constants as const
from core.robot import Robot

from pybricks.parameters import Color  # type: ignore
from domain.star_platinum import star_platinum
from domain.pathfinding import main
from core.utils import PIDValues, PIDControl
import constants as const
from core.omni_robot import OmniRobot, Direction
import math

from domain.omni_localization import forward_avoiding_places

boarding_vertices = [(31, 32), (24, 25), (18, 19), (11, 12), (5, 6)]


def passenger_boarding(robot: Robot):
    """
    Rotina de encontrar um passageiro, pega-lo e detectar faixa etária e cor.

    Retorna uma tupla como ("CHILD", Color.BLUE) ou ("ADULT", Color.GREEN)
    """
    robot.ev3_print("Passenger boarding")

    # backwards_distance = robot.line_grabber(time = 3000)
    # robot.pid_walk(cm = backwards_distance, speed =-40)
    robot.reset_wheels_angle()
    pid = PIDControl(const.LINE_FOLLOWER_VALUES)
    target = 20
    # procura um cilindro
    robot.line_follower(
        sensor = robot.color_left,
        loop_condition_function= lambda: robot.infra_side.distance() >= 40,
        speed = 40,
        side = "L",
    )
    # passa do cilindro
    robot.line_follower(
        sensor = robot.color_left,
        loop_condition_function= lambda: robot.infra_side.distance() >= 40,
        speed = 40,
        side = "L",
    )
    # corrige a distancia do cilindro
    robot.pid_walk(10, 40)
    # aponta para o cilindro
    robot.pid_turn(-90)
    star_platinum(robot, "CLOSE")
    star_platinum(robot, "DOWN")
    star_platinum(robot, "OPEN")
    robot.align(30)
    robot.pid_walk(7, 40)
    # pega o cilindro e define as informações
    star_platinum(robot, "CLOSE")
    vertice = star_platinum(robot, "PASSENGER INFO")
    # tratativa de leitura da cor branca e nenhum cilindro
    if len(vertice) == 0:
        star_platinum(robot, "UP")
        star_platinum(robot, "OPEN")
        robot.pid_walk(10, -40)
        robot.align(speed=30)
        robot.pid_turn(90)
        return passenger_boarding(robot)
    # pega o cilindro
    star_platinum(robot, "UP")
    robot.pid_walk(10, -40)
    robot.align(speed=30)
    # Alinha de novo
    robot.pid_walk(2,-30)
    robot.pid_turn(90)

    # segue a linha até V31
    robot.line_follower(
        sensor = robot.color_left,
        loop_condition_function= lambda: robot.color_right.color() != Color.RED,
        speed = 40,
        side = "L",
    )
    # alinha com o azul
    robot.pid_walk(10, -30)
    robot.pid_turn(-90)
    robot.pid_walk(5, -30)
    robot.align(speed=30)
    robot.pid_walk(cm = const.LINE_TO_CELL_CENTER_DISTANCE, speed = -30)
    # alinha com o vermelho
    robot.pid_turn(90)
    robot.align(speed=30)
    robot.pid_walk(cm = const.LINE_TO_CELL_CENTER_DISTANCE, speed = -30)
    robot.orientation = "S"
    
    return vertice


def passenger_unboarding(robot: Robot):
    """
    Rotina de desembarque de passageiro
    """

    robot.ev3_print("Entrou no vértice")

    robot.align(speed=30, pid=PIDValues(kp=0.8, ki=0.005, kd=1))
    robot.pid_walk(1.75, 40)

    if robot.color_right.color() == Color.YELLOW:
        while robot.color_left.color() != Color.YELLOW:
            robot.ev3_print(robot.color_left.color())
            robot.pid_walk(12, -30)
            robot.pid_turn(15)

            robot.pid_walk(7, 35)
            robot.align(speed=30, pid=PIDValues(kp=0.8, ki=0.005, kd=1))
            robot.pid_walk(2, 35)

    elif robot.color_left.color() == Color.YELLOW:
        while robot.color_right.color() != Color.YELLOW:
            robot.ev3_print(robot.color_right.color())
            robot.pid_walk(12, -30)
            robot.pid_turn(-15)

            robot.pid_walk(7, 35)
            robot.align(speed=30, pid=PIDValues(kp=0.8, ki=0.005, kd=1))
            robot.pid_walk(2, 35)

    robot.pid_walk(15, -35)
    robot.ev3.speaker.beep()
    robot.pid_walk(21, 35)
    star_platinum(robot, "DOWN")
    star_platinum(robot, "OPEN")

    robot.pid_walk(15, -40)
    robot.align(speed=30, pid=PIDValues(kp=0.8, ki=0.005, kd=1))
    robot.pid_walk(11, -40)


def omni_passenger_unboarding(omni: OmniRobot):
    """
    Rotina de desembarque de passageiro
    """
    if omni.moving_direction_sign == -1:
        omni.pid_turn(180)
        omni.moving_direction_sign = 1

    omni.align(pid=PIDValues(kp=1, ki=0.0015, kd=0.45))
    omni.stop()

    omni.pid_walk(1.5, 35)

    pid_controls = [PIDControl(const.PID_WALK_VALUES) for _ in range(3)]
    initial_angles = [motor.angle() for motor in omni.get_all_motors()]
    if omni.color_front_left.color() == Color.YELLOW:
        while omni.color_front_right.color() != Color.YELLOW:
            omni.loopless_pid_walk(
                pid_controls, 40, direction=Direction.LEFT, initials=initial_angles
            )
    elif omni.color_front_right.color() == Color.YELLOW:
        while omni.color_front_left.color() != Color.YELLOW:
            omni.loopless_pid_walk(
                pid_controls, 40, direction=Direction.RIGHT, initials=initial_angles
            )

    omni.align(direction=Direction.BACK)
    omni.pid_walk(25, 40)

    omni.ev3.speaker.beep()

    omni.bluetooth.message("CLAW_LOW")
    omni.bluetooth.message()

    omni.bluetooth.message("CLAW_OPEN")
    omni.bluetooth.message()

    omni.pid_walk(25, 40, direction=Direction.BACK)
    omni.stop()


def omni_manouver_to_get_passenger(omni: OmniRobot):
    if omni.moving_direction_sign == -1:
        omni.pid_turn(90)
    else:
        omni.pid_turn(-90)


def omni_passenger_boarding(omni: OmniRobot):
    omni.bluetooth.message("CLAW_MID")
    omni.bluetooth.message()

    omni.bluetooth.message("CLAW_OPEN")
    omni.bluetooth.message()

    omni.align(direction=Direction.RIGHT, speed=50)

    omni.bluetooth.message("COLOR_SIDE")

    initial_angle_left = omni.motor_front_left.angle()

    def condition_function():
        color = omni.bluetooth.message(should_wait=False)
        return color is None or color == Color.WHITE

    omni.line_follower(
        sensor=omni.color_front_right,
        loop_condition_function=condition_function,
    )
    passenger_color = omni.bluetooth.message(should_wait=False)
    omni.ev3_print("PASSENGER:", passenger_color)

    pid_controls = [PIDControl(const.PID_WALK_VALUES) for _ in range(3)]
    initial_angles = [motor.angle() for motor in omni.get_all_motors()]
    while omni.bluetooth.message(should_wait=False) is None:
        omni.loopless_pid_walk(
            pid_controls, 35, direction=Direction.BACK, initials=initial_angles
        )
    omni.stop()

    for pid in pid_controls:
        pid.reset()
    initial_angles = [motor.angle() for motor in omni.get_all_motors()]
    while omni.bluetooth.message(should_wait=False) is not None:
        if passenger_color is None:
            passenger_color = omni.bluetooth.message(should_wait=False)
        omni.loopless_pid_walk(
            pid_controls, 35, direction=Direction.BACK, initials=initial_angles
        )
    omni.ev3_print("PASSENGER:", passenger_color)

    omni.stop()
    omni.bluetooth.message("STOP")

    final_angle_left = omni.motor_front_left.angle()

    walked_cm = omni.motor_degrees_to_cm(abs(final_angle_left - initial_angle_left))
    walked_cells = walked_cm / 30
    omni.ev3_print("walked:", walked_cm)
    omni.ev3_print("wkd cells:", walked_cells)
    vertice = boarding_vertices[int(math.floor(walked_cells))]
    omni.ev3_print("vertice:", vertice)

    omni.pid_walk(cm=3, direction=Direction.FRONT)
    omni.stop()
    omni.pid_walk(cm=5, direction=Direction.LEFT)
    omni.pid_turn(90)
    omni.align(speed=50)

    omni.pid_walk(cm=4, direction=Direction.FRONT, speed=35)

    omni.bluetooth.message("CLAW_CLOSE")
    omni.bluetooth.message()
    omni.ev3_print("CLAW_CLOSE")

    omni.bluetooth.message("CLAW_HIGH")
    omni.bluetooth.message()
    omni.ev3_print("CLAW_HIGH")

    # Média de 3 leituras
    omni.bluetooth.message("ULTRA_FRONT")
    distances = []
    for _ in range(3):
        distances.append(omni.bluetooth.message())
    omni.bluetooth.message("STOP")
    distance_front = sum(distances) / len(distances)

    omni.ev3_print("P. DIST.:", distance_front, distances)

    adult_or_child = (
        "ADULT" if passenger_color == Color.RED or distance_front < 100 else "CHILD"
    )

    omni.pid_walk(cm=8, direction=Direction.BACK)
    omni.pid_turn(-90)

    # Média de 3 leituras
    omni.bluetooth.message("ULTRA_FRONT")
    for _ in range(3):
        distances.append(omni.bluetooth.message())
    omni.bluetooth.message("STOP")
    distance_front = sum(distances) / len(distances)

    omni.ev3_print("P. DIST.:", distance_front, distances)

    forward_avoiding_places(omni, direction=Direction.BACK)

    omni.pid_walk(cm=3)

    return ((adult_or_child, passenger_color), boarding_vertices[0])
