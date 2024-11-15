from core.omni_robot import OmniRobot

from domain.localization import wall_colors, wall_colors_check
from core.omni_robot import Direction
from pybricks.parameters import Color

from core.utils import PIDControl

import constants as const


def forward_avoiding_places(robot: OmniRobot, direction=Direction.FRONT, speed=45):
    robot.ev3_print("Forward avoiding places")
    left_sensor, right_sensor = robot.get_sensors_towards_direction(direction)

    pid = [PIDControl(const.PID_WALK_VALUES) for _ in range(3)]
    robot.reset_wheels_angle()
    while (
        robot.color_back_left.color() != Color.RED
        and robot.color_back_right.color() != Color.RED
    ):
        # robot.ev3_print(left_sensor.color(), right_sensor.color())
        if (
            left_sensor.color() in wall_colors
            and right_sensor.color() not in wall_colors
        ):
            # Ajuste à direita
            initial_angle = robot.motor_front_left.angle()
            # MAX_ANGLE = robot.cm_to_motor_degrees(2)
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
            robot.reset_wheels_angle()
            if right_sensor.color() in wall_colors:
                break
            # else:
            #     robot.ev3_print("MAX ANGLE CASE")
            #     robot.wait_button()

        elif (
            right_sensor.color() in wall_colors
            and left_sensor.color() not in wall_colors
        ):
            # Ajuste à esquerda
            initial_angle = robot.motor_front_right.angle()
            # MAX_ANGLE = robot.cm_to_motor_degrees(2)
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
            robot.reset_wheels_angle()
            if left_sensor.color() in wall_colors:
                break
            # else:
            #     robot.ev3_print("MAX ANGLE CASE")
            #     robot.wait_button()

        robot.loopless_pid_walk(pid, direction=direction, vel=speed)
    robot.stop()
    robot.ev3_print("End of forward avoiding places")


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

    pid = [PIDControl(const.PID_WALK_VALUES) for _ in range(3)]
    robot.reset_wheels_angle()
    while (
        robot.color_front_left.color() not in wall_colors
        or robot.color_front_right.color() not in wall_colors
    ):
        robot.ev3_print(robot.color_front_left.color(), robot.color_front_right.color())
        if (
            robot.color_front_left.color() in (Color.BLACK, Color.YELLOW)
            and robot.color_front_right.color() == Color.WHITE
        ):
            # Curva à direita
            robot.pid_turn(20)
            robot.reset_wheels_angle()
        elif (
            robot.color_front_right.color() in (Color.BLACK, Color.YELLOW)
            and robot.color_front_left.color() == Color.WHITE
        ):
            # Curva à esquerda
            robot.pid_turn(-20)
            robot.reset_wheels_angle()
        robot.loopless_pid_walk(pid)
    robot.off_motors()

    robot.pid_walk(2, speed=40, direction=Direction.BACK)
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


def omni_all_white_routine(robot: OmniRobot):
    robot.ev3_print("White routine")
    pid = [PIDControl(const.PID_WALK_VALUES) for _ in range(3)]
    robot.reset_wheels_angle()
    while (
        robot.color_front_left.color() not in wall_colors
        or robot.color_front_right.color() not in wall_colors
    ):
        if (
            robot.color_front_left.color() in (Color.BLACK, Color.YELLOW)
            and robot.color_front_right.color() == Color.WHITE
        ):
            # Curva à direita
            robot.pid_turn(20)
            robot.reset_wheels_angle()
        elif (
            robot.color_front_left.color() in (Color.BLACK, Color.YELLOW)
            and robot.color_front_right.color() == Color.WHITE
        ):
            # Curva à esquerda
            robot.pid_turn(-20)
            robot.reset_wheels_angle()
        robot.loopless_pid_walk(pid)
    robot.off_motors()

    robot.pid_walk(2, speed=40, direction=Direction.BACK)
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

    pid = [PIDControl(const.PID_WALK_VALUES) for _ in range(3)]
    robot.reset_wheels_angle()
    while (
        robot.color_front_left.color() not in wall_colors
        or robot.color_front_right.color() not in wall_colors
    ):
        if (
            robot.color_front_left.color() in (Color.BLACK, Color.YELLOW)
            and robot.color_front_right.color() == Color.WHITE
        ):
            # Curva à direita
            robot.pid_turn(20)
            robot.reset_wheels_angle()
        elif (
            robot.color_front_right.color() in (Color.BLACK, Color.YELLOW)
            and robot.color_front_left.color() == Color.WHITE
        ):
            # Curva à esquerda
            robot.pid_turn(-20)
            robot.reset_wheels_angle()
        robot.loopless_pid_walk(pid)
    robot.off_motors()

    robot.pid_walk(2, speed=40, direction=Direction.BACK)
    robot.align()

    return omni_blue_routine(robot)


def localization_routine(robot: OmniRobot):
    robot.ev3_print("Localization")

    colors_checkpoints_list = []

    robot.bluetooth.message("ULTRA_FRONT")
    robot.bluetooth.message()
    for n in range(4):
        robot.ev3_print("Checkpoint", n + 1)
        obstacle_function = lambda: (
            robot.color_front_left.color() in wall_colors
            or robot.color_front_right.color() in wall_colors
            or (robot.bluetooth.message(should_wait=False) or 2550)
            < const.OBSTACLE_DISTANCE
        )

        SEARCHING_DISTANCE = 25
        has_seen_obstacle, walked_percentage = robot.pid_walk(
            SEARCHING_DISTANCE, obstacle_function=obstacle_function
        )
        robot.ev3_print("Walked percentage:", walked_percentage)

        if has_seen_obstacle:
            robot.ev3_print("Obstacle detected!")

            robot.pid_walk(2, speed=30, direction=Direction.BACK)
            robot.align(speed=30)
            robot.pid_walk(const.DIST_COLOR_AFTER_ALIGN, speed=30)

        color_str = wall_colors_check(
            robot.color_front_left.color(), robot.color_front_right.color()
        )
        robot.ev3_print("Color detected:", color_str)

        if color_str == "BLUE":
            return omni_blue_routine(robot)
        elif color_str == "RED":
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

    robot.bluetooth.message("STOP")

    robot.ev3_print("Cores detectadas nos quatro lados:", colors_checkpoints_list)
    robot.pid_turn(colors_checkpoints_list.index("WHITE") * 90)
    return omni_all_white_routine(robot)
