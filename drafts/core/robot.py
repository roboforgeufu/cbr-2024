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
from pybricks.media.ev3dev import SoundFile, ImageFile, Font  # type: ignore

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

    def __init__(
        self,
        wheel_diameter=5.5,
        wheel_distance=11.25,
        r_wheel=None,
        l_wheel=None,
    ):

        # Ev3
        self.ev3 = EV3Brick()
        self.watch = StopWatch()

        # Rodas
        self.wheel_diameter = wheel_diameter
        self.wheel_distance = wheel_distance
        self.r_wheel = r_wheel
        self.l_wheel = l_wheel

    def real_angle_to_motor_degrees(self, angle):

        # Converte graus reais para graus correspondentes na roda
        return angle * (self.wheel_diameter / self.wheel_distance)

    def set_wheels_angle(self, angle):

        # Zera o ângulo das rodas
        self.r_wheel.reset_angle(angle)
        self.l_wheel.reset_angle(angle)

    def hold_wheels(self):

        # Interrompe e trava as rodas
        self.r_wheel.hold()
        self.l_wheel.hold()

    def wheels_angle(self):

        # Retorna a média do ângulo das duas rodas
        return (self.l_wheel.angle() + self.l_wheel.angle()) / 2

    def abs_wheels_angle(self):

        # Retorna a média do módulo do ângulo das duas rodas
        return (abs(self.r_wheel.angle()) + abs(self.l_wheel.angle())) / 2

    def walk(self, dc=100, angle=None, pid=False):

        # Movimenta o robô
        if pid:
            pass

        else:
            if angle != None:
                self.set_wheels_angle(0)
                while abs(angle) >= abs_wheels_angle():
                    self.r_wheel.dc(dc)
                    self.l_wheel.dc(dc)
                self.hold_wheels()
            else:
                self.r_wheel.dc(dc)
                self.l_wheel.dc(dc)

    def turn(self, angle, pid=False, dc=100):

        # Gira o robô em graus
        self.set_wheels_angle(0)

        motor_degrees = self.real_angle_to_motor_degrees(angle)
        error = self.abs_wheels_angle()

        if pid:
            # Curva usando PID
            side = angle / abs(angle)
            pass

        else:
            # Curva normal
            while error < motor_degrees:
                error = self.abs_wheels_angle()
                self.r_wheel.run(dc)
                self.l_wheel.run(-dc)

    def wait_button(self, button=[]):
        if not isinstance(button, list):
            button = [button]
        while True:
            if self.ev3.buttons.pressed() == button:
                continue
            else:
                break

    def ev3_print(self, *args, clear=False, font='Lucida', size=16, bold=False, **kwargs):
        """Imprime na tela do robô e no terminal do PC ao mesmo tempo. A opção `clear` controla se a tela do EV3 é limpada a cada novo print."""
        if clear: self.ev3.screen.clear()
        self.ev3.screen.set_font(Font(font, size, bold))
        self.ev3.screen.print(*args, **kwargs)
        print(*args, **kwargs)
