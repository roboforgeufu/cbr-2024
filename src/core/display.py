#!/usr/bin/env pybricks-micropython
from pybricks.parameters import Button  # type: ignore
from pybricks.tools import wait  # type: ignore
from core.robot import Robot


def screen(lines: list, *extralines, selected=None, clear=False, error=None, robot: Robot):
    lines += list(extralines)
    lines_len = len(lines)
    if clear:
        robot.ev3.screen.clear()
    for line in range(lines_len - 1):
        robot.ev3_draw(str(lines[line]), background=selected == line, line=line)
    if error is not None: robot.ev3_draw(error, line=lines_len)


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
    error = None
    if clear:
        robot.ev3.screen.clear()

    while True:
        if parameters[selected] is not None:
            if selected == ki_line:
                parameters[selected] = round(parameters[selected], 3)
            else:
                parameters[selected] = round(parameters[selected], 2)
            if parameters[selected] < 0:
                error = "Maior que zero!"
                parameters[selected] = 0
                clear = True
        values = parameters + functions[function_number] + "Start"
        options = [str(x) + " " + str(y) for x, y in zip(headers, values)]
        showed_function = functions[function_number]
        functions_line = len(values) - 1
        start_line = len(options)

        screen(options, "Start", selected=selected, clear=clear, robot=robot, error=error)

        error = None
        clear = False
        button = robot.wait_button(
            [Button.UP, Button.DOWN, Button.CENTER, Button.LEFT, Button.RIGHT]
        )

        if button == Button.UP:
            selected -= 1
            if selected < 0:
                selected = start_line
            clear = True

        elif button == Button.DOWN:
            selected += 1
            if selected > start_line:
                selected = 0
            clear = True

        if values[selected] is not None:
            if button == Button.RIGHT:
                if selected == functions_line:
                    function_number += 1
                    clear = True
                    if function_number > len(functions) - 1:
                        function_number = 0
                else:
                    if selected == ki_line:
                        values[selected] += 0.001
                    else:
                        values[selected] += 0.01

            elif button == Button.LEFT:
                if selected == functions_line:
                    function_number -= 1
                    clear = True
                    if function_number < 0:
                        function_number = len(functions) - 1
                else:
                    if selected == ki_line:
                        values[selected] -= 0.001
                    else:
                        values[selected] -= 0.01

        elif button == Button.CENTER and selected == start_line:
            screen(options, "Start", "RUNNING", selected=None, clear=True, robot=robot)
            break

        print(values[selected])

        wait(delay)

    return values, showed_function, options
