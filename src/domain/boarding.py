import constants as const
from core.robot import Robot

from pybricks.parameters import Color  # type: ignore
from domain.star_platinum import star_platinum
from domain.pathfinding import main
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
    backwards_distance = robot.line_grabber(time = 3000)
    robot.pid_walk(cm = backwards_distance, speed =-40)
    robot.reset_wheels_angle()
    pid = PIDControl(const.LINE_FOLLOWER_VALUES)
    target = 20
    while robot.infra_side.distance() >= 30:
        robot.line_follower(target, "L", pid, 60)
    while robot.infra_side.distance() < 30:
        robot.line_follower(target, "L", pid, 60)
    robot.pid_turn(-90)
    star_platinum(robot, "DOWN")
    star_platinum(robot, "OPEN")
    robot.align(30)
    robot.pid_walk(8, 40)
    star_platinum(robot, "CLOSE")
    vertice = star_platinum(robot, "PASSENGER INFO")
    if len(vertice) == 0:
        star_platinum(robot, "OPEN")
        robot.pid_walk(10, -40)
        robot.align()
        robot.pid_turn(-90)
        return passenger_boarding(robot)
    star_platinum(robot, "UP")
    robot.pid_walk(10, -40)
    robot.align(speed = 40)
    robot.pid_walk(4,-30)
    robot.pid_turn(90)
    
    pid = PIDControl(const.LINE_FOLLOWER_VALUES)
    while robot.color_right.color() != Color.RED:
        robot.line_follower(target, "L", pid, 60)
    robot.pid_walk(cm=5, speed=-40)
    robot.pid_turn(90)
    robot.pid_walk(cm=2, speed=-40)
    robot.align()
    robot.pid_walk(cm=13.5, speed=-60)
    robot.pid_turn(-90)
    robot.align()
    robot.pid_walk(cm=13.5, speed=-60)
    robot.orientation = "S"

    return vertice

def passenger_unboarding(robot: Robot):
    """
    Rotina de desembarque de passageiro
    """
    
    robot.align(speed=35)
    robot.pid_walk(1.5, 30)
    
    if robot.color_right.color() == Color.YELLOW:
        while robot.color_left.color() != Color.YELLOW:
            robot.pid_walk(12, -30)
            robot.pid_turn(-30)    
            
            robot.pid_walk(7)
            robot.align(speed=40)
            robot.pid_walk(1.5, 35)    
    
    elif robot.color_left.color() == Color.YELLOW:
        while robot.color_right.color() != Color.YELLOW:
            robot.pid_walk(12, -30)
            robot.pid_turn(30)    
            
            robot.pid_walk(7)
            robot.align(speed=40)
            robot.pid_walk(1.5, 35)
    
    robot.pid_walk(15, -35)
    robot.ev3.speaker.beep()
    robot.pid_walk(27, 35)
    star_platinum(robot, 'DOWN')
    star_platinum(robot, 'OPEN')
    
    robot.pid_walk(15, -40)
    robot.align(speed=35)
    robot.pid_walk(11, -40)
      
                
def omni_passenger_unboarding(omni: OmniRobot):
    """
    Rotina de desembarque de passageiro
    """
    if omni.moving_direction_sign == -1:
        omni.pid_turn(180)
        omni.moving_direction_sign = 1

    omni.align(pid=PIDValues(kp = 1, ki = 0.0015, kd = 0.45))
    omni.stop()

    omni.pid_walk(1.5, 35)
    
    print(omni.color_front_left.color(), omni.color_front_right.color())
    
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
    omni.pid_walk(20)

    omni.ev3.speaker.beep()
    
    omni.pid_walk(10, 40)
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
        omni.loopless_pid_walk(
            pid_controls, 35, direction=Direction.BACK, initials=initial_angles
        )

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
