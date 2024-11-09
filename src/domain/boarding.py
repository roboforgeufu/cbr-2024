import constants as const
from core.robot import Robot
from core.network import Bluetooth
from pybricks.parameters import Color  # type: ignore
from domain.star_platinum import star_platinum
from core.utils import PIDValues, PIDControl
import constants as const
from core.omni_robot import OmniRobot, Direction
import math


boarding_vertices = [(31, 32), (24, 25), (18, 19), (11, 12), (5, 6)]


def passenger_boarding(robot: Robot):
    """
    Rotina de encontrar um passageiro, pega-lo e detectar faixa etária e cor.

    Retorna uma tupla como ("CHILD", Color.BLUE) ou ("ADULT", Color.GREEN)
    """
    pid = PIDControl(PIDValues(kp=1.8, kd=0.03, ki=0))
    target = 20
    while robot.infra_side.distance() >= 30:
        robot.line_follower(target, "L", pid, 60)
    while robot.infra_side.distance() < 30:
        robot.line_follower(target, "L", pid, 60)
    robot.pid_turn(-90)
    star_platinum(robot, "DOWN")
    star_platinum(robot, "OPEN")
    robot.align(30)
    robot.pid_walk(10, 30)
    star_platinum(robot, "CLOSE")
    star_platinum(robot, "PASSENGER INFO")
    passenger = robot.bluetooth.message()
    robot.ev3_print(passenger)


def smart_walk(robot: Robot):
    """O que será a movimentação no início e
    envia mensagens de abrir e fechar a garra"""


def passenger_read_color_and_type(robot: Robot):
    """Retorna cor e se é adulto ou criança -> ("CHILD", Color.BLUE)"""


def passenger_read_type(robot: Robot):
    """Retorna se é adulto ou criança"""


def passenger_traject(robot: Robot):
    """Chama funções de movimentação depois
    de ver quais vértices são o início e o fim"""


def passenger_unboarding(robot: Robot):
    """
    Rotina de desembarque de passageiro
    """


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

    omni.line_follow(
        sensor=omni.color_front_right,
        loop_condition_function=condition_function,
    )
    passenger_color = omni.bluetooth.message(should_wait=False)
    omni.ev3_print("PASSENGER:", passenger_color)

    t = 0
    i = [0, 0, 0]
    e = [0, 0, 0]
    initial_angles = [motor.angle() for motor in omni.get_all_motors()]
    while omni.bluetooth.message(should_wait=False) is None:
        t, i, e = omni.loopless_pid_walk(
            t,
            i,
            e,
            20,
            direction=Direction.BACK,
            initial_front_left_angle=initial_angles[0],
            initial_front_right_angle=initial_angles[1],
            initial_back_left_angle=initial_angles[2],
            initial_back_right_angle=initial_angles[3],
        )
    omni.off_motors()
    t = 0
    i = [0, 0, 0]
    e = [0, 0, 0]
    initial_angles = [motor.angle() for motor in omni.get_all_motors()]
    while omni.bluetooth.message(should_wait=False) is not None:
        t, i, e = omni.loopless_pid_walk(
            t,
            i,
            e,
            20,
            initial_front_left_angle=initial_angles[0],
            initial_front_right_angle=initial_angles[1],
            initial_back_left_angle=initial_angles[2],
            initial_back_right_angle=initial_angles[3],
        )
    omni.off_motors()
    omni.bluetooth.message("STOP")

    final_angle_left = omni.motor_front_left.angle()

    walked_cm = omni.motor_degrees_to_cm(abs(final_angle_left - initial_angle_left))
    walked_cells = walked_cm / 30
    omni.ev3_print("walked:", walked_cm)
    omni.ev3_print("wkd cells:", walked_cells)
    vertice = boarding_vertices[int(math.floor(walked_cells))]
    omni.ev3_print("vertice:", vertice)

    omni.pid_walk(cm=2, direction=Direction.BACK)
    omni.off_motors()
    omni.pid_walk(cm=5, direction=Direction.LEFT)
    omni.pid_turn(90)
    omni.align(speed=50)
    omni.pid_walk(cm=6, direction=Direction.FRONT, speed=35)

    omni.bluetooth.message("CLAW_CLOSE")
    omni.bluetooth.message()

    omni.bluetooth.message("CLAW_HIGH")
    omni.bluetooth.message()

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

    # Retorna ao centro do vértice
    back_to_vertice_distance = walked_cells - int(math.floor(walked_cells))

    correction = 4  # valor em cm, pode ser necessário recalibrar.
    backwards_distance = (
        back_to_vertice_distance * 30 * const.OMNI_WALK_DISTANCE_CORRECTION
    ) - (correction * (math.floor(walked_cells) + 1))
    omni.ev3_print("BACK_DIST:", backwards_distance)

    omni.pid_walk(
        cm=abs(backwards_distance),
        direction=Direction.BACK if backwards_distance >= 0 else Direction.FRONT,
        obstacle_function=lambda: omni.color_back_left.color() != Color.WHITE
        or omni.color_back_right.color() != Color.WHITE
        or omni.color_front_left.color() != Color.WHITE
        or omni.color_front_right.color() != Color.WHITE,
    )
    if (
        omni.color_back_left.color() != Color.WHITE
        or omni.color_back_right.color() != Color.WHITE
    ):
        omni.pid_walk(cm=2, direction=Direction.FRONT)
    elif (
        omni.color_front_left.color() != Color.WHITE
        or omni.color_front_right.color() != Color.WHITE
    ):
        omni.pid_walk(cm=2, direction=Direction.BACK)
    omni.align(Direction.RIGHT)
    omni.pid_walk(cm=8, direction=Direction.LEFT)

    return ((adult_or_child, passenger_color), vertice)
