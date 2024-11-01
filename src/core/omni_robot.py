"""
Robô de quatro rodas omnidirecionais
"""

from pybricks.hubs import EV3Brick
from pybricks.tools import StopWatch
from pybricks.parameters import Port

from core.utils import wait_button_pressed, ev3_print, PIDValues
from core.network import Bluetooth
from core.decision_color_sensor import DecisionColorSensor
from pybricks.ev3devices import Motor

import math


class OmniRobot:
    """Classe que representa um robô de 4 rodas omnidirecionais"""

    def __init__(
        self,
        wheel_diameter=5.5,
        wheel_length=10,
        wheel_width=10,
        motor_front_left: Port = None,
        motor_front_right: Port = None,
        motor_back_left: Port = None,
        motor_back_right: Port = None,
        color_front_left: DecisionColorSensor = None,
        color_front_right: DecisionColorSensor = None,
        color_back_left: DecisionColorSensor = None,
        color_back_right: DecisionColorSensor = None,
        server_name: str = None,
        debug=True,
    ):

        # Ev3
        self.ev3 = EV3Brick()
        self.watch = StopWatch()

        # Rodas
        self.wheel_diameter = wheel_diameter
        self.wheel_length = wheel_length
        self.wheel_width = wheel_width

        # Motores
        if motor_front_left is not None:
            self.motor_front_left = Motor(motor_front_left)
        if motor_front_right is not None:
            self.motor_front_right = Motor(motor_front_right)
        if motor_back_left is not None:
            self.motor_back_left = Motor(motor_back_left)
        if motor_back_right is not None:
            self.motor_back_right = Motor(motor_back_right)

        # Sensores
        if color_front_left is not None:
            self.color_front_left = color_front_left
        if color_front_right is not None:
            self.color_front_right = color_front_right
        if color_back_left is not None:
            self.color_back_left = color_back_left
        if color_back_right is not None:
            self.color_back_right = color_back_right

        # Comunicação bluetooth
        if server_name:
            self.bluetooth = Bluetooth

        self.debug = debug

        # Orientação (N, S, L, O, ou None caso o robô ainda não tenha se encontrado)
        self.orientation = None

        # Printa a voltagem e corrente atual da bateria:
        self.ev3_print("Bat. V:", self.ev3.battery.voltage(), "mV")
        self.ev3_print("Bat. C:", self.ev3.battery.current(), "mA")

    def robot_axis_to_motor_degrees(self, angle):
        """
        Grau relativo ao eixo do robô -> grau nas rodas (motores) do robô

        Considera um possível fator de correção
        """
        # Converte graus reais para graus correspondentes na roda
        radius = (self.wheel_length**2 + self.wheel_length**2) ** (1 / 2)
        return angle * radius / self.wheel_distance

    def cm_to_motor_degrees(self, cm: float):
        """Distância em centímetros -> grau nas rodas (motores) do robô"""
        return cm * (360 / (math.pi * self.wheel_diameter))

    def abs_wheels_angle(self):

        return (
            abs(self.motor_front_left.angle())
            + abs(self.motor_front_right.angle())
            + abs(self.motor_back_left.angle())
            + abs(self.motor_back_right.angle())
        ) / 4

    def reset_wheels_angle(self, angle=0):
        """Reseta o ângulo das rodas"""
        self.motor_front_left.reset_angle(angle)
        self.motor_front_right.reset_angle(angle)
        self.motor_back_left.reset_angle(angle)
        self.motor_back_right.reset_angle(angle)

    def off_motors(self):
        """Desliga motores de locomoção."""
        self.motor_front_left.dc(0)
        self.motor_front_right.dc(0)
        self.motor_back_left.dc(0)
        self.motor_back_right.dc(0)

        self.motor_front_left.hold()
        self.motor_front_right.hold()
        self.motor_back_left.hold()
        self.motor_back_right.hold()

        self.motor_front_left.dc(0)
        self.motor_front_right.dc(0)
        self.motor_back_left.dc(0)
        self.motor_back_right.dc(0)

    def pid_walk(self, cm, speed=60, obstacle_function=None, off_motors=None):
        """
        Anda em linha reta com controle PID entre os motores.

        Retorna se viu obstáculos e quantos porcento do movimento foi realizado até a saída da função.

        Exemplos:
            False, 0.7
            True, 1
        """
        # TODO

    def loopless_pid_walk(
        self,
        prev_elapsed_time=0,
        i_share=0,
        prev_error=0,
        vel=60,
        pid: PIDValues = PIDValues(
            kp=3,
            ki=0.2,
            kd=8,
        ),
        initial_left_angle=0,
        initial_right_angle=0,
    ):
        """
        Controle PID entre os motores sem um loop específico.
        Feita pra ser colocada dentro de um loop em outra função, passando os
        novos parâmetros (prev_elapsed_time, i_share, prev_error) devidamente
        inicializados a cada iteração.
        """
        # TODO

    def pid_turn(
        self,
        angle,
        pid: PIDValues = PIDValues(
            kp=0.8,
            ki=0.01,
            kd=0.4,
        ),
    ):
        """
        Curva com controle PID.
        - Angulo relativo ao eixo do robô.
        - Angulo negativo: curva p / esquerda
        - Angulo positivo: curva p / direita
        - Modos(mode):
            - 1: usa o valor dado como ângulo ao redor do eixo do robô
            - 2: usa o valor dado como ângulo no eixo das rodas
        """

    def wait_button(self, button=[]):
        wait_button_pressed(ev3=self.ev3, button=button)

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
        end="\n",
        **kwargs,
    ):
        ev3_print(
            *args,
            ev3=self.ev3,
            clear=clear,
            font=font,
            size=size,
            bold=bold,
            x=x,
            y=y,
            background=background,
            end=end,
            **kwargs,
        )

    def align(
        self,
        pid: PIDValues = PIDValues(kp=1, ki=0.015, kd=1.5),
        direction_sign=1,
    ): ...
