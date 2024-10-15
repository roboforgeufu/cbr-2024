#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick  # type: ignore
from pybricks.ev3devices import (
    Motor,
    TouchSensor,
    ColorSensor,  # type: ignore
    InfraredSensor,
    UltrasonicSensor,
    GyroSensor,
)
from pybricks.parameters import Port, Stop, Direction, Button, Color  # type: ignore

"""
Módulo central pra controle do Robô usando quatro rodas omnidirecionais

Devem estar nesse módulo:
    - Classe 'OmniRobot', com métodos e atributos para controle geral no robô
    - Estruturas de dados auxiliares aplicáveis a "qualquer" tipo de robô omnidirecional

Não devem estar nesse módulo:
    - Código específico de algum problema/desafio
"""

class OmniRobot:

    # Classe que representa um robô genérico

    def __init__(self, wheel_diameter, wheel_distance, wheel_1, wheel_2, wheel_3, wheel_4):
        
        # Ev3
        self.ev3 = EV3Brick()
        self.watch = StopWatch()

        # Rodas
        self.wheel_diameter = wheel_diameter
        self.wheel_length = wheel_length
        self.wheel_width = wheel_width
        self.wheel_1 = wheel_1
        self.wheel_2 = wheel_2
        self.wheel_3 = wheel_3
        self.wheel_4 = wheel_4

    def real_angle_to_motor_degrees(self, angle):

        # Converte graus reais para graus correspondentes na roda
        radius = (self.wheel_length ** 2 + self.wheel_length ** 2) ** (1/2)
        return angle * radius / self.wheel_distance

    def wheels_angle()

        return (self.wheel_1.angle() + self.wheel_2.angle() + self.wheel_3.angle() + self.wheel_4.angle())/4

    def abs_wheels_angle():

        return (abs(self.wheel_1.angle()) + abs(self.wheel_2.angle()) + abs(self.wheel_3.angle()) + abs(self.wheel_4.angle()))/4

    def set_wheels_angle(self, angle):

        # Zera o ângulo das rodas
        self.wheel_1.reset_angle(angle)
        self.wheel_2.reset_angle(angle)
        self.wheel_3.reset_angle(angle)
        self.wheel_4.reset_angle(angle)

    def vertical_run(self, duty):

        self.wheel_1.dc(duty)
        self.wheel_2.dc(duty)
        self.wheel_3.dc(duty)
        self.wheel_4.dc(duty)

    def horizontal_run(self, duty, side):

        if side == 1:
            self.wheel_1.dc(duty)
            self.wheel_2.dc(-duty)
            self.wheel_3.dc(-duty)
            self.wheel_4.dc(duty)
        else:
            self.wheel_1.dc(-duty)
            self.wheel_2.dc(duty)
            self.wheel_3.dc(duty)
            self.wheel_4.dc(-duty)


    def walk(self, duty, angle=0, direction="vertical", pid=False)

        side = abs(duty)/duty
        
        if angle != 0:

            side *= abs(angle)/angle

            self.set_wheels_angle(0)

            if direction == "vertical":
                while abs(angle) >= abs_wheels_angle():
                    vertical_run(duty)

            elif direction == "horizontal":
                while abs(angle) >= abs_wheels_angle():
                    horizontal_run(duty, side)

        else:

            if direction == "vertical":
                vertical_run(duty)

            elif direction == "horizontal":
                horizontal_run(duty, side)


        def turn(self, duty=100, angle=0, pid=False):

            if angle > 0:
                angle = real_angle_to_motor_degrees(angle)
                while abs angle > self.abs_wheels_angle():
                    self.wheel_1.dc(duty)
                    self.wheel_2.dc(-duty)
                    self.wheel_3.dc(duty)
                    self.wheel_4.dc(-duty)
            else:
                self.wheel_1.dc(duty)
                self.wheel_2.dc(-duty)
                self.wheel_3.dc(duty)
                self.wheel_4.dc(-duty)