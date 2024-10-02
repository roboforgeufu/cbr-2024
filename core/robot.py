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
from pybricks.tools import wait, StopWatch, DataLog  # type: ignore
from pybricks.robotics import DriveBase  # type: ignore
from pybricks.media.ev3dev import SoundFile, ImageFile  # type: ignore

"""
Módulo central pra controle do Robô.

Devem estar nesse módulo:
    - Classe 'Robot', com métodos e atributos para controle geral no robô
    - Estruturas de dados auxiliares aplicáveis a "qualquer" tipo de robô

Não devem estar nesse módulo:
    - Código específico de algum problema/desafio
"""

# TODO: colocar pid no walk e turn


class Robot:
    # Classe que representa um robô genérico

    def _init_(self, wheel_diameter, wheel_distance, r_wheel, l_wheel):

        # Ev3
        self.ev3 = EV3Brick()
        self.watch = StopWatch()

        # Rodas
        self.wheel_diameter = wheel_diameter
        self.wheel_distance = wheel_distance
        self.r_wheel = Motor(r_wheel)
        self.l_wheel = Motor(l_wheel)

    def real_degrees_to_motor_angle(self, degrees):
        # Converte graus reais para graus correspondentes na roda
        return degrees * (self.wheel_distance / self.wheel_diameter)

    def reset_wheels_angle(self):
        # Zera o ângulo das rodas
        self.r_wheel.reset_angle(0)
        self.l_wheel.reset_angle(0)

    def turn(self, angle, pid=False, dc=100):
        # Gira o robô em graus

        self.reset_wheels_angle()

        motor_degrees = self.real_degrees_to_motor_angle(angle)
        error = (abs(self.r_wheel) + abs(self.l_wheel)) / 2

        if pid:
            # Curva usando PID
            side = angle / abs(angle)

        else:
            # Curva normal
            while error < motor_degrees:
                error = (abs(self.r_wheel) + abs(self.l_wheel)) / 2
                self.r_wheel.run(dc)
                self.l_wheel.run(-dc)
