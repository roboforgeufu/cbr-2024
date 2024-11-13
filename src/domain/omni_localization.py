from core.omni_robot import OmniRobot

from domain.localization import wall_colors, wall_colors_check
from core.omni_robot import Direction
from pybricks.parameters import Color

from core.utils import PIDControl

import constants as const


def omni_blue_routine(robot: OmniRobot):
    robot.ev3_print("Blue routine")
    robot.pid_turn(-90)

    pid = [PIDControl(const.PID_WALK_VALUES) for _ in range(3)]
    robot.reset_wheels_angle()
    while (
        robot.color_back_left.color() != Color.RED
        and robot.color_back_right.color() != Color.RED
    ):
        robot.loopless_pid_walk(pid, direction=Direction.BACK)
    robot.off_motors()
    robot.pid_walk(2, speed=40)
    return 31


def omni_red_routine(robot: OmniRobot):
    robot.ev3_print("Red routine")
    robot.pid_walk(30, speed=40, direction=Direction.BACK)
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
    robot.pid_walk(1, speed=30)

    if (
        wall_colors_check(
            robot.color_front_left.color(), robot.color_front_right.color()
        )
        == "BLUE"
    ):
        return omni_blue_routine(robot)
    elif (
        wall_colors_check(
            robot.color_front_left.color(), robot.color_front_right.color()
        )
        == "BLACK"
    ):
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
    robot.pid_walk(2, speed=40)

    if (
        robot.color_front_left.color() == Color.RED
        and robot.color_front_right.color() == Color.RED
    ):
        return omni_red_routine(robot)
    if (
        robot.color_front_left.color() == Color.BLACK
        and robot.color_front_right.color() == Color.BLACK
    ):
        return omni_black_routine(robot)
    if (
        robot.color_front_left.color() == Color.BLUE
        and robot.color_front_right.color() == Color.BLUE
    ):
        return omni_blue_routine(robot)


def omni_black_routine(robot: OmniRobot):
    robot.ev3_print("Black routine")
    robot.pid_turn(180)

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

        has_seen_obstacle, walked_percentage = robot.pid_walk(
            30, obstacle_function=obstacle_function
        )
        robot.ev3_print("Walked percentage:", walked_percentage)

        if has_seen_obstacle:
            robot.ev3_print("Obstacle detected!")

            robot.pid_walk(2, speed=30, direction=Direction.BACK)
            robot.align(speed=30)
            robot.pid_walk(1, speed=30)

        color_str = wall_colors_check(
            robot.color_front_left.color(), robot.color_front_right.color()
        )
        robot.ev3_print("Color detected:", color_str)

        if color_str == "BLUE":
            return omni_blue_routine(robot)
        elif color_str == "RED":
            return omni_red_routine(robot)

        colors_checkpoints_list.append(color_str)

        robot.pid_walk(cm=30 * walked_percentage, speed=60, direction=Direction.BACK)
        robot.pid_turn(90)

    robot.bluetooth.message("STOP")

    robot.ev3_print("Cores detectadas nos quatro lados:", colors_checkpoints_list)
    robot.pid_turn(colors_checkpoints_list.index("WHITE") * 90)
    return omni_all_white_routine(robot)
