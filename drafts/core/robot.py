#!/usr/bin/env pybricks-micropython
from pybricks.ev3devices import ColorSensor  # type: ignore
from pybricks.ev3devices import (
    GyroSensor,
    InfraredSensor,
    Motor,
    TouchSensor,
    UltrasonicSensor,
)
from pybricks.hubs import EV3Brick  # type: ignore
from pybricks.media.ev3dev import Font, ImageFile, SoundFile  # type: ignore
from pybricks.parameters import Button, Color, Direction, Port, Stop  # type: ignore
from pybricks.robotics import DriveBase  # type: ignore
from pybricks.tools import DataLog, StopWatch, wait  # type: ignore

"""
Módulo central pra controle do Robô.

Devem estar nesse módulo:
    - Classe 'Robot' e 'OmniRobot', com métodos e atributos para controle geral no robô
    - Estruturas de dados auxiliares aplicáveis a "qualquer" tipo de robô

Não devem estar nesse módulo:
    - Código específico de algum problema/desafio ou comunicação.
"""

# TODO: colocar pid no walk e turn

#
# Robô com duas rodas
#


class Robot:

    # Classe que representa um robô genérico

    def __init__(
        self,
        motor_r: Port = None,
        motor_l: Port = None,
        motor_elevate_claw: Port = None,
        motor_open_claw: Port = None,
        infra_side: Port = None,
        ultra_feet: Port = None,
        ultra_head: Port = None,
        color_left: Port = None,
        color_right: Port = None,
        color_claw: Port = None,
        debug=True,
    ):

        # Ev3
        self.ev3 = EV3Brick()
        self.watch = StopWatch()

        # Rodas
        self.wheel_diameter = wheel_diameter
        self.wheel_distance = wheel_distance
        
        # Motores
        if motor_r is not None:
            self.motor_r = Motor(motor_r)
        if motor_l is not None:
            self.motor_l = Motor(motor_l)
        if motor_open_claw is not None:
            self.motor_open_claw = Motor(motor_open_claw)
        if motor_elevate_claw is not None:
            self.motor_elevate_claw = Motor(motor_elevate_claw)

        # Sensores
        if color_claw is not None:
            self.color_claw = ColorSensor(color_claw)
        if ultra_head is not None:
            self.ultra_head = UltrasonicSensor(ultra_head)
        if ultra_feet is not None:
            self.ultra_feet = UltrasonicSensor(ultra_feet)
        if color_left is not None:
            self.color_left = ColorSensor(color_left)
        if color_right is not None:
            self.color_right = ColorSensor(color_right)
        if infra_side is not None:
            self.infra_side = InfraredSensor(infra_side)

        # Comunicação bluetooth

        self.debug = debug
        

    def ev3_print(self, *args, clear=False, always: bool = False, **kwargs):
        """
        Métodos para logs.
        """
        if self.debug or always:
            if clear:
                wait(10)
                self.ev3.screen.clear()
            self.ev3.screen.print(*args, **kwargs)
            print(*args, **kwargs)

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

    def walk(self, speed=100, angle=None, pid=False):

        # Movimenta o robô
        if pid:
            pass

        else:
            if angle != None:
                self.set_wheels_angle(0)
                while angle >= self.wheels_angle():
                    self.r_wheel.run(speed)
                    self.l_wheel.run(speed)
                self.hold_wheels()
            else:
                self.r_wheel.run(speed)
                self.l_wheel.run(speed)

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

    def ev3_print(
        self,
        *args,
        clear=False,
        font="Lucida",
        size=16,
        bold=False,
        x=0,
        y=0,
        background=None,
        end="\n"
    ):
        # Imprime na tela do robô e no terminal do PC ao mesmo tempo
        # A opção 'clear' controla se a tela do EV3 é limpada a cada novo print
        if clear:
            self.ev3.screen.clear()
        self.ev3.screen.set_font(Font(font, size, bold))
        if x != 0 or y != 0 or background != None:
            self.ev3.screen.draw_text(x, y, str(*args), background_color=background)
        else:
            self.ev3.screen.print(*args, end=end)
        print(*args)
    


#
# Robô de quatro rodas omnidirecionais
#


class OmniRobot:

    # Classe que representa um robô genérico

    def __init__(
        self,
        wheel_diameter=5.5,
        wheel_length=10,
        wheel_width=10,
        wheel_1=None,
        wheel_2=None,
        wheel_3=None,
        wheel_4=None,
    ):

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
        radius = (self.wheel_length**2 + self.wheel_length**2) ** (1 / 2)
        return angle * radius / self.wheel_distance

    def wheels_angle(self):

        return (
            self.wheel_1.angle()
            + self.wheel_2.angle()
            + self.wheel_3.angle()
            + self.wheel_4.angle()
        ) / 4

    def abs_wheels_angle(self):

        return (
            abs(self.wheel_1.angle())
            + abs(self.wheel_2.angle())
            + abs(self.wheel_3.angle())
            + abs(self.wheel_4.angle())
        ) / 4

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

    def walk(self, duty, angle=0, direction="vertical", pid=False):

        side = abs(duty) / duty

        if angle != 0:

            side *= abs(angle) / angle

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
            while abs(angle) > self.abs_wheels_angle():
                self.wheel_1.dc(duty)
                self.wheel_2.dc(-duty)
                self.wheel_3.dc(duty)
                self.wheel_4.dc(-duty)
        else:
            self.wheel_1.dc(duty)
            self.wheel_2.dc(-duty)
            self.wheel_3.dc(duty)
            self.wheel_4.dc(-duty)

    def wait_button(self, button=[]):
        if not isinstance(button, list):
            button = [button]
        while True:
            if self.ev3.buttons.pressed() == button:
                continue
            else:
                break

    def ev3_print(
        self,
        *args,
        clear=False,
        font="Lucida",
        size=16,
        bold=False,
        x=0,
        y=0,
        background=None,
        end="\n"
    ):
        """Imprime na tela do robô e no terminal do PC ao mesmo tempo. A opção `clear` controla se a tela do EV3 é limpada a cada novo print."""
        if clear:
            self.ev3.screen.clear()
        self.ev3.screen.set_font(Font(font, size, bold))
        if x != 0 or y != 0 or background != None:
            self.ev3.screen.draw_text(x, y, str(*args), background_color=background)
        else:
            self.ev3.screen.print(*args, end=end)
        print(*args)
