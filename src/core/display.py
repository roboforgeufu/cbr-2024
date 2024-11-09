#!/usr/bin/env pybricks-micropython
from pybricks.parameters import Button  # type: ignore
from pybricks.tools import wait  # type: ignore
from core.robot import Robot


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


def menu(
    parameters: list,
    headers: list,
    functions: list,
    robot: Robot,
    ki_line=None,
    delay=50,
    clear=False,
):
    selected = 0
    function_number = 0
    info = None
    enter = False
    enter_pressed = False
    if clear:
        robot.ev3.screen.clear()

    while True:

        showed_function = functions[function_number]
        extra_lines = [showed_function, "Start"]
        options = parameters + extra_lines
        showed_options = [
            str(x) + ": " + "{:.3g}".format(y) for x, y in zip(headers, parameters)
        ] + extra_lines
        functions_line = len(parameters)
        start_line = len(showed_options) - 1

        screen(showed_options, selected=selected, clear=True, robot=robot, info=info)

        info = None
        button = robot.wait_button(
            [Button.UP, Button.DOWN, Button.CENTER, Button.LEFT, Button.RIGHT]
        )

        if button == Button.CENTER:
            if selected == start_line:
                screen(
                    showed_options,
                    "RUNNING",
                    selected=None,
                    clear=True,
                    robot=robot,
                )
                break
            elif selected != functions_line:
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
            info = "Detailed edit"
            if button == Button.UP:
                if selected == ki_line:
                    parameters[selected] += 0.001
                else:
                    parameters[selected] += 0.01

            elif button == Button.DOWN:
                if selected == ki_line:
                    parameters[selected] -= 0.001
                else:
                    parameters[selected] -= 0.01
                if parameters[selected] < 0:
                    parameters[selected] = 0
                    info = "Maior que zero!"

        if selected == functions_line:

            if button == Button.RIGHT:
                function_number += 1
            elif button == Button.LEFT:
                function_number -= 1

            if function_number < 0:
                function_number = len(functions) - 1

            if function_number > len(functions) - 1:
                function_number = 0

        else:
            if button == Button.RIGHT:
                if enter:
                    detailed = 0.1
                else:
                    detailed = 1
                if selected == ki_line:
                    parameters[selected] += 0.1 * detailed
                else:
                    parameters[selected] += 1 * detailed

            elif button == Button.LEFT:
                if selected == ki_line:
                    parameters[selected] -= 0.1 * detailed
                else:
                    parameters[selected] -= 1 * detailed
                if parameters[selected] < 0:
                    parameters[selected] = 0
                    info = "Maior que zero!"

        if enter_pressed: 
            wait(2*delay)
            enter_pressed = False
        wait(delay)

    return options
