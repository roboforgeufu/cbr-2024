#!/usr/bin/env pybricks-micropython

from pybricks.ev3devices import ColorSensor, InfraredSensor, Motor, UltrasonicSensor #type: ignore
from pybricks.hubs import EV3Brick #type: ignore
from pybricks.iodevices import Ev3devSensor #type: ignore
from pybricks.parameters import Button, Color, Port, Stop #type: ignore
from pybricks.tools import StopWatch, DataLog, wait #type: ignore
from pybricks.media.ev3dev import Font #type: ignore

from core.robot import Robot

def turn_calibration(robot: Robot, calibration_sensor: ColorSensor, speed = 30):
    turn_repetitions = 10
    robot.stopwatch = StopWatch

    v = robot.ev3.battery.voltage() / 1000
    i = robot.ev3.battery.current() / 1000

    current_electric_power = v * i 

    read_degrees_ninety = []
    elapsed_time_ninety = []
    calculated_degrees_ninety = (robot.robot_axis_to_motor_degrees(90) / robot.turn_correction)

    for i in range(turn_repetitions):
        robot.reset_wheels_angle()
        robot.stopwatch.reset()
        robot.wait_button()
        while calibration_sensor.color() != Color.BLACK:
            robot.motor_l.dc(speed)
            robot.motor_r.dc(-speed)
        robot.stop()
        robot.stop()
        elapsed_time_ninety.append(robot.stopwatch.time())
        read_degrees_ninety.append(robot.motor_l.angle())
        read_degrees_ninety.append(robot.motor_r.angle())
        wait(100)

    read_degrees_one_eighty = []
    elapsed_time_one_eighty = []
    calculated_degrees_one_eighty = (robot.robot_axis_to_motor_degrees(180) / robot.turn_correction)

    for i in range(turn_repetitions):
        robot.reset_wheels_angle()
        robot.stopwatch.reset()
        robot.wait_button()
        while calibration_sensor.color() != Color.BLACK:
            robot.motor_l.dc(speed)
            robot.motor_r.dc(-speed)
        robot.stop()
        robot.stop()
        elapsed_time_one_eighty.append(robot.stopwatch.time())
        read_degrees_one_eighty.append(robot.motor_l.angle())
        read_degrees_one_eighty.append(robot.motor_r.angle())
        wait(100)

    turn_ninety_correction_factor = (sum(read_degrees_ninety)/(2 * turn_repetitions)) / calculated_degrees_ninety
    turn_one_eighty_correction_factor = (sum(read_degrees_one_eighty)/(2 * turn_repetitions)) / calculated_degrees_one_eighty
    angular_velocity_ninety = 90 / (sum(elapsed_time_ninety)/turn_repetitions)
    angular_velocity_one_eighty = 180 / (sum( elapsed_time_one_eighty)/turn_repetitions)

    print("Voltage: {} V, Current: {} A, Power: {} W".format(v, i, current_electric_power))
    print("FC(90º): {}, FC(180º): {}".format(turn_ninety_correction_factor, turn_one_eighty_correction_factor))
    print("W(90º): {} degrees/seconds, W(180): {} degrees/seconds".format(angular_velocity_ninety, angular_velocity_one_eighty))

    angular_coeficient = (turn_one_eighty_correction_factor - turn_ninety_correction_factor) / 90
    linear_coeficient = turn_ninety_correction_factor / (angular_coeficient * 90)

    print("Line equation: y = {}x + {}".format(angular_coeficient, linear_coeficient))