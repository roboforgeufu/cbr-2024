#!/usr/bin/env pybricks-micropython
from pybricks.parameters import Button  # type: ignore
from pybricks.tools import wait  # type: ignore
from core.robot import Robot

import json


def screen(
    lines: list, *extralines, selected=None, clear=False, info=None, robot: Robot
):
    lines += list(extralines)
    lines_len = len(lines)

    if clear:
        robot.ev3.screen.clear()
    for line in range(lines_len):
        robot.ev3_draw(str(lines[line]), background=selected == line, line=line)
    if info is not None:
        robot.ev3_draw(info, line=lines_len)


def calibration_menu(
    file_name: str,
    headers: list,
    robot: Robot,
    delay=50,
    selected_function=0,
    clear=False,
):
    with open(file_name, "r") as file:
        data = json.load(file)

    functions = list(data[robot.name].keys())
    ki_line = 2
    selected_function = selected_function
    enter = False
    enter_pressed = False
    reset = False
    functions_line = 0
    parameters = data[robot.name][functions[selected_function]]
    selected = 0
    detailed = 1

    if clear:
        robot.ev3.screen.clear()

    while True:

        if reset:
            with open(file_name, "r") as file:
                data = json.load(file)
            reset = False
        parameters = data[robot.name][functions[selected_function]]
        options = [functions[selected_function]] + parameters + ["Start"] + ["Reset"]
        reset_line = len(options) - 2
        start_line = len(options) - 1

        showed_data = [(functions[selected_function])]+ [x + ": " + "{:.3g}".format(y) for x, y in zip(headers, parameters)]
        showed_options = (
            showed_data
            + ["Reset"]
            + ["Start"]
        )

        screen(showed_options, selected=selected, clear=True, robot=robot)

        button = robot.wait_button(
            [Button.UP, Button.DOWN, Button.CENTER, Button.LEFT, Button.RIGHT]
        )

        if button == Button.CENTER:
            if selected == start_line:
                wait(delay*4)
                break
            elif selected == reset_line:
                reset = True
            elif selected > functions_line:
                if enter:
                    enter = False
                elif not enter:
                    enter = True
                enter_pressed = True

        if not enter:
            if button == Button.UP:
                selected -= 1
                if selected < 0:
                    selected = start_line

            elif button == Button.DOWN:
                selected += 1
                if selected > start_line:
                    selected = 0
        else:
            if button == Button.UP:
                if selected == ki_line:
                    parameters[selected - 1] += 0.001
                else:
                    parameters[selected - 1] += 0.01

            elif button == Button.DOWN:
                if selected == ki_line:
                    parameters[selected - 1] -= 0.001
                else:
                    parameters[selected - 1] -= 0.01
                if parameters[selected - 1] < 0:
                    parameters[selected - 1] = round(0, 0)

        if selected == functions_line:

            if button == Button.RIGHT:
                selected_function += 1
            elif button == Button.LEFT:
                selected_function -= 1

            if selected_function < 0:
                selected_function = len(functions) - 1

            if selected_function > len(functions) - 1:
                selected_function = 0

        else:
            if button == Button.RIGHT:
                if enter:
                    detailed = 0.1
                else:
                    detailed = 1
                if selected == ki_line:
                    parameters[selected - 1] += 0.1 * detailed
                else:
                    parameters[selected - 1] += 1 * detailed

            elif button == Button.LEFT:
                if selected == ki_line:
                    parameters[selected - 1] -= 0.1 * detailed
                else:
                    parameters[selected - 1] -= 1 * detailed
                if parameters[selected - 1] < 0:
                    parameters[selected - 1] = round(0, 0)

        if enter_pressed:
            wait(2 * delay)
            enter_pressed = False
        wait(delay)

    print(options[:4], showed_data)

    return options[:4], showed_data
