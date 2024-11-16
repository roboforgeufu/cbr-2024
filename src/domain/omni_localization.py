from core.omni_robot import OmniRobot

from domain.localization import wall_colors, wall_colors_check
from core.omni_robot import Direction
from pybricks.parameters import Color

from core.utils import PIDControl

import constants as const


def forward_avoiding_places(
    robot: OmniRobot,
    direction=Direction.FRONT,
    speed=45,
    check_obstacle=False,
    max_distance=None,
    should_stop_transmission=True,
):
    """
    Vai pra frente desviando de estabelecimentos. Caso check_obstacle seja True, o robô para ao ver um obstáculo, e retorna True.

    O parâmetro max_distance é opcional e serve para definir uma distância máxima que o robô deve andar.
    """

    robot.ev3_print("Forward avoiding places")
    left_sensor, right_sensor = robot.get_sensors_towards_direction(direction)

    if direction == Direction.FRONT:
        robot.bluetooth.message("ULTRA_FRONT")
    else:
        robot.bluetooth.message("ULTRA_BACK")

    seeing_obstacle = (
        lambda: check_obstacle
        and (robot.bluetooth.message(should_wait=False) or 2550)
        < const.OBSTACLE_DISTANCE
    )

    pid = [PIDControl(const.PID_WALK_VALUES) for _ in range(3)]
    initials = [motor.angle() for motor in robot.get_all_motors()]
    while (
        (
            left_sensor.color() not in wall_colors
            or right_sensor.color() not in wall_colors
        )
        and not seeing_obstacle()
        and (
            max_distance is None
            or abs(robot.motor_front_left.angle() - initials[0])
            < robot.cm_to_motor_degrees(max_distance)
        )
    ):
        # robot.ev3_print(left_sensor.color(), right_sensor.color())
        if (
            left_sensor.color() in wall_colors
            and right_sensor.color() not in wall_colors
        ):
            # Ajuste à direita
            robot.line_follower(
                left_sensor,
                speed=speed,
                loop_condition_function=lambda: left_sensor.color() != Color.WHITE
                and right_sensor.color() == Color.WHITE,
                pid=const.LINE_FOLLOWER_AVOIDING_PLACES,
                error_function=lambda: left_sensor.rgb()[2]
                - const.OMNI_LINE_FOLLOWER_BLUE_TARGET,
                side="L",
            )
            robot.stop()
            initials = [motor.angle() for motor in robot.get_all_motors()]
            if right_sensor.color() in wall_colors:
                break

        elif (
            right_sensor.color() in wall_colors
            and left_sensor.color() not in wall_colors
        ):
            # Ajuste à esquerda
            robot.line_follower(
                right_sensor,
                speed=speed,
                loop_condition_function=lambda: right_sensor.color() != Color.WHITE
                and left_sensor.color() == Color.WHITE,
                # and abs(robot.motor_front_right.angle() - initial_angle) < MAX_ANGLE,
                pid=const.LINE_FOLLOWER_AVOIDING_PLACES,
                error_function=lambda: right_sensor.rgb()[2]
                - const.OMNI_LINE_FOLLOWER_BLUE_TARGET,
                side="R",
            )
            robot.stop()
            initials = [motor.angle() for motor in robot.get_all_motors()]
            if left_sensor.color() in wall_colors:
                break

        robot.loopless_pid_walk(pid, direction=direction, vel=speed, initials=initials)
    robot.stop()
    has_seen_obstacle = seeing_obstacle()
    if has_seen_obstacle:
        distance = (robot.bluetooth.message()) / 10
        robot.pid_walk(
            abs(const.OBSTACLE_ALIGN_DISTANCE - distance),
            speed=40,
            direction=(
                Direction.BACK
                if const.OBSTACLE_ALIGN_DISTANCE - distance > 0
                else Direction.FRONT
            ),
        )
        robot.ev3.speaker.beep()
        if Color.BLUE in [left_sensor.color(), right_sensor.color()]:
            has_seen_obstacle = False
            robot.ev3.speaker.beep(100)

        # Ré de volta
        robot.pid_walk(
            abs(const.OBSTACLE_ALIGN_DISTANCE - distance),
            speed=40,
            direction=(
                Direction.BACK
                if const.OBSTACLE_ALIGN_DISTANCE - distance <= 0
                else Direction.FRONT
            ),
        )

    if should_stop_transmission:
        robot.bluetooth.message("STOP")
    robot.ev3_print("Seen obst:", has_seen_obstacle)
    return has_seen_obstacle


def omni_blue_routine(robot: OmniRobot):
    robot.ev3_print("Blue routine")
    robot.pid_walk(10, speed=40, direction=Direction.BACK)
    robot.pid_turn(-90)

    forward_avoiding_places(robot, direction=Direction.BACK)

    robot.pid_walk(3, speed=40)
    robot.ev3_print("End Blue routine")
    return 31


def omni_red_routine(robot: OmniRobot):

    robot.ev3_print("Red routine")
    robot.pid_walk(35, speed=40, direction=Direction.BACK)
    robot.pid_turn(90)

    turn_sign = 1
    has_seen_obstacle = forward_avoiding_places(
        robot, check_obstacle=True, should_stop_transmission=False
    )
    while has_seen_obstacle:
        distance = (robot.bluetooth.message()) / 10
        robot.ev3_print("ultra:", distance)

        # Correção pra "trocar de rua"
        robot.pid_walk(20 - distance, speed=40, direction=Direction.BACK)
        robot.pid_turn(90 * turn_sign)
        turn_sign *= -1

        has_seen_obstacle = forward_avoiding_places(
            robot,
            check_obstacle=True,
            max_distance=60,
            should_stop_transmission=False,
        )
        if has_seen_obstacle:
            turn_sign *= -1
            continue

        robot.pid_turn(90 * turn_sign)
        has_seen_obstacle = forward_avoiding_places(
            robot, check_obstacle=True, should_stop_transmission=False
        )
    robot.bluetooth.message("STOP")

    robot.pid_walk(3, speed=40, direction=Direction.BACK)
    robot.align()
    robot.pid_walk(const.DIST_COLOR_AFTER_ALIGN, speed=30)

    color = wall_colors_check(
        robot.color_front_left.color(), robot.color_front_right.color()
    )
    robot.ev3_print("Color detected:", color)
    if color == "BLUE":
        robot.ev3_print("BLUE detected")
        return omni_blue_routine(robot)
    elif color == "BLACK":
        robot.ev3_print("BLACK detected")
        return omni_black_routine(robot)
    elif color == "RED":
        robot.ev3_print("RED detected")
        return omni_red_routine(robot)


def omni_all_white_routine(robot: OmniRobot):
    robot.ev3_print("White routine")

    # Detectar obstáculo e virar à esquerda
    while True:
        has_seen_obstacle = forward_avoiding_places(
            robot, check_obstacle=True, should_stop_transmission=False
        )
        if has_seen_obstacle:
            distance = (robot.bluetooth.message()) / 10
            robot.pid_walk(20 - distance, speed=40, direction=Direction.BACK)
            robot.pid_turn(-90)
        else:
            break
    robot.bluetooth.message("STOP")

    robot.pid_walk(3, speed=40, direction=Direction.BACK)
    robot.align()
    robot.pid_walk(const.DIST_COLOR_AFTER_ALIGN, speed=40)

    color_seen = wall_colors_check(
        robot.color_front_left.color(), robot.color_front_right.color()
    )
    if color_seen == "RED":
        robot.ev3_print("RED detected")
        return omni_red_routine(robot)
    if color_seen == "BLACK":
        robot.ev3_print("BLACK detected")
        return omni_black_routine(robot)
    if color_seen == "BLUE":
        robot.ev3_print("BLUE detected")
        return omni_blue_routine(robot)


def omni_black_routine(robot: OmniRobot):
    robot.pid_walk(5, speed=40, direction=Direction.BACK)
    robot.ev3_print("Black routine")
    robot.pid_turn(180)
    robot.align(direction=Direction.BACK)

    turn_sign = 1
    has_seen_obstacle = forward_avoiding_places(
        robot, check_obstacle=True, should_stop_transmission=False
    )
    while has_seen_obstacle:
        distance = (robot.bluetooth.message()) / 10

        # Correção pra "trocar de rua"
        robot.pid_walk(20 - distance, speed=40, direction=Direction.BACK)
        robot.pid_turn(90 * turn_sign)
        turn_sign *= -1

        has_seen_obstacle = forward_avoiding_places(
            robot, check_obstacle=True, max_distance=60
        )
        if has_seen_obstacle:
            turn_sign *= -1
            continue

        robot.pid_turn(90 * turn_sign)
        has_seen_obstacle = forward_avoiding_places(
            robot, check_obstacle=True, should_stop_transmission=False
        )
    robot.bluetooth.message("STOP")

    robot.pid_walk(3, speed=40, direction=Direction.BACK)
    robot.align()

    return omni_blue_routine(robot)


def localization_routine(robot: OmniRobot):
    robot.ev3_print("Localization")

    colors_checkpoints_list = []

    robot.bluetooth.message("ULTRA_FRONT")
    robot.bluetooth.message()
    for n in range(4):
        robot.ev3_print("Checkpoint", n + 1)

        def obstacle_function():
            # robot.ev3_print(
            #     robot.color_front_left.color(), robot.color_front_right.color()
            # )
            return (
                robot.color_front_left.color() in wall_colors
                or robot.color_front_right.color() in wall_colors
            )

        SEARCHING_DISTANCE = 25
        has_seen_obstacle, walked_percentage = robot.pid_walk(
            SEARCHING_DISTANCE, obstacle_function=obstacle_function
        )
        robot.ev3_print("Walked percentage:", walked_percentage)
        robot.stop()

        if has_seen_obstacle:
            robot.ev3_print("Obstacle detected!")

            # Linha a frente
            robot.pid_walk(3, speed=30, direction=Direction.BACK)
            robot.align(speed=30)
            robot.pid_walk(const.DIST_COLOR_AFTER_ALIGN, speed=30)

        color_str = wall_colors_check(
            robot.color_front_left.color(), robot.color_front_right.color()
        )
        robot.ev3_print("Color detected:", color_str)

        if color_str == "BLUE":
            robot.bluetooth.message("STOP")
            return omni_blue_routine(robot)
        elif color_str == "RED":
            robot.bluetooth.message("STOP")
            return omni_red_routine(robot)

        colors_checkpoints_list.append(color_str)

        robot.pid_walk(
            cm=SEARCHING_DISTANCE * walked_percentage,
            speed=60,
            direction=Direction.BACK,
        )
        robot.stop()

        # robot.wait_button()
        robot.reset_wheels_angle()
        robot.pid_turn(90)
        # robot.wait_button()

    robot.bluetooth.message("STOP")

    robot.ev3_print("Cores detectadas nos quatro lados:", colors_checkpoints_list)
    robot.pid_turn(colors_checkpoints_list.index("WHITE") * 90)
    return omni_all_white_routine(robot)
