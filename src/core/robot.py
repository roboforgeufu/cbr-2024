#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick  # type: ignore
from pybricks.ev3devices import (  # type: ignore
    Motor,
    TouchSensor,
    ColorSensor,
    InfraredSensor,
    UltrasonicSensor,
    GyroSensor,
)
from pybricks.parameters import Port, Stop, Direction, Button, Color  # type: ignore
from pybricks.tools import wait, StopWatch, DataLog  # type: ignore
from pybricks.robotics import DriveBase  # type: ignore
from pybricks.media.ev3dev import SoundFile, ImageFile, Font  # type: ignore
from core.utils import ev3_print, ev3_draw, wait_button_pressed, get_hostname
from core.decision_color_sensor import DecisionColorSensor
from pybricks.parameters import Button  # type: ignore
from core.utils import PIDValues, PIDControl
from core.network import Bluetooth
import constants as const

import math


"""
Módulo central pra controle do Robô.

Devem estar nesse módulo:
    - Classe 'Robot', com métodos e atributos para controle geral no robô
    - Estruturas de dados auxiliares aplicáveis a "qualquer" tipo de robô

Não devem estar nesse módulo:
    - Código específico de algum problema/desafio ou comunicação.
"""

#
# Robô com duas rodas
#


class Robot:
    """Classe que representa um robô de 2 rodas"""

    def __init__(
        self,
        wheel_diameter=None,
        wheel_distance=None,
        motor_r: Port = None,
        motor_l: Port = None,
        motor_elevate_claw: Port = None,
        motor_open_claw: Port = None,
        infra_side: Port = None,
        ultra_feet: Port = None,
        ultra_head: Port = None,
        color_left: DecisionColorSensor = None,
        color_right: DecisionColorSensor = None,
        color_claw: DecisionColorSensor = None,
        server_name: str = None,
        debug=True,
    ):

        # Ev3
        self.ev3 = EV3Brick()
        self.stopwatch = StopWatch()
        self.name = get_hostname() 

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
            self.color_claw = color_claw
        if ultra_head is not None:
            self.ultra_head = UltrasonicSensor(ultra_head)
        if ultra_feet is not None:
            self.ultra_feet = UltrasonicSensor(ultra_feet)
        if color_left is not None:
            self.color_left = color_left
        if color_right is not None:
            self.color_right = color_right
        if infra_side is not None:
            self.infra_side = InfraredSensor(infra_side)

        # Comunicação bluetooth
        if server_name:
            self.bluetooth = Bluetooth(ev3=self.ev3, server_name=server_name)

        self.debug = debug

        # Orientação (N, S, L, O, ou None caso o robô ainda não tenha se encontrado)
        self.orientation = None

        # Fator de correção de curvas
        self.turn_correction = 0.9

        # Printa a voltagem e corrente atual da bateria:
        self.ev3_print("Bat. V:", self.ev3.battery.voltage(), "mV")
        self.ev3_print("Bat. C:", self.ev3.battery.current(), "mA")

    def robot_axis_to_motor_degrees(self, axis_degrees: float):
        """
        Grau relativo ao eixo do robô -> grau nas rodas (motores) do robô

        Considera um possível fator de correção
        """
        return (
            axis_degrees
            * (self.wheel_distance / self.wheel_diameter)
            * self.turn_correction
        )

    def cm_to_motor_degrees(self, cm: float):
        """Distância em centímetros -> grau nas rodas (motores) do robô"""
        return cm * (360 / (math.pi * self.wheel_diameter))

    def motor_degrees_to_cm(self, degrees: float):
        """Grau nas rodas (motores) do robô -> Distância em centímetros"""
        return degrees * ((math.pi * self.wheel_diameter) / 360)

    def reset_wheels_angle(self, angle=0):
        """Reseta o ângulo das rodas"""
        self.motor_r.reset_angle(angle)
        self.motor_l.reset_angle(angle)

    def stop(self):
        """Desliga motores de locomoção."""
        self.motor_l.dc(0)
        self.motor_r.dc(0)
        self.motor_l.hold()
        self.motor_r.hold()
        self.motor_l.dc(0)
        self.motor_r.dc(0)

    def wheels_angle(self):

        # Retorna a média do ângulo das duas rodas
        return (self.motor_r.angle() + self.motor_l.angle()) / 2

    def abs_wheels_angle(self):

        # Retorna a média do módulo do ângulo das duas rodas
        return (abs(self.motor_r.angle()) + abs(self.motor_l.angle())) / 2

    def pid_walk(
        self,
        cm,
        speed=60,
        pid: PIDValues = const.PID_WALK_VALUES,
        obstacle_function=None,
        off_motors=True,
    ):
        """
        Anda em linha reta com controle PID entre os motores.

        Retorna se viu obstáculos e quantos porcento do movimento foi realizado até a saída da função.

        Exemplos:
            False, 0.7
            True, 1
        """
        degrees = self.cm_to_motor_degrees(cm)
        if degrees == 0:
            return

        motor_angle_average = 0
        initial_left_angle = self.motor_l.angle()
        initial_right_angle = self.motor_r.angle()
        pid_c = PIDControl(pid)

        has_seen_obstacle = False
        while abs(motor_angle_average) < abs(degrees):
            if obstacle_function is not None and obstacle_function():
                has_seen_obstacle = True
                break

            motor_angle_average = (
                (self.motor_l.angle() - initial_left_angle)
                + (self.motor_r.angle() - initial_right_angle)
            ) / 2

            self.loopless_pid_walk(
                pid_control=pid_c,
                speed=speed,
                initial_left_angle=initial_left_angle,
                initial_right_angle=initial_right_angle,
            )

        if off_motors:
            self.stop()
        return has_seen_obstacle, abs(motor_angle_average) / abs(degrees)

    def loopless_pid_walk(
        self,
        pid_control: PIDControl,
        speed=60,
        initial_left_angle=0,
        initial_right_angle=0,
    ):
        """
        Controle PID entre os motores sem um loop específico.
        Feita pra ser colocada dentro de um loop em outra função, passando os
        novos parâmetros (prev_elapsed_time, i_share, prev_error) devidamente
        inicializados a cada iteração.
        """
        correction = pid_control.compute(
            lambda: (self.motor_r.angle() - initial_right_angle)
            - (self.motor_l.angle() - initial_left_angle)
        )
        self.motor_r.dc(speed - correction)
        self.motor_l.dc(speed + correction)

    def pid_turn(self, angle, pid: PIDValues = const.PID_TURN_VALUES):
        """
        Curva com controle PID.
        - Angulo relativo ao eixo do robô.
        - Angulo negativo: curva p / esquerda
        - Angulo positivo: curva p / direita
        """
        # self.ev3_print(self.pid_turn.__name__)

        motor_degrees = self.robot_axis_to_motor_degrees(angle)

        initial_angle_l = self.motor_l.angle()
        initial_angle_r = self.motor_r.angle()

        target_angle_r = initial_angle_r - motor_degrees
        target_angle_l = initial_angle_l + motor_degrees

        # self.ev3_print("INICIAL:", initial_angle_l, initial_angle_r)
        # self.ev3_print("TARGET:", target_angle_l, target_angle_r)

        left_error = target_angle_l - self.motor_l.angle()
        right_error = target_angle_r - self.motor_r.angle()

        left_error_i = 0
        right_error_i = 0

        left_prev_error = left_error
        right_prev_error = right_error

        n = 0
        while (
            int(abs(self.motor_l.angle() - target_angle_l))
            > const.PID_TURN_ACCEPTABLE_DEGREE_DIFF
            or int(abs(self.motor_r.angle() - target_angle_r))
            > const.PID_TURN_ACCEPTABLE_DEGREE_DIFF
        ):
            n += 1
            left_error = target_angle_l - self.motor_l.angle()
            right_error = target_angle_r - self.motor_r.angle()

            if abs(left_error) < 30:
                left_error_i += left_error
            if abs(right_error) < 30:
                right_error_i += right_error

            left_error_d = left_prev_error - left_error
            right_error_d = right_prev_error - right_error

            left_prev_error = left_error
            right_prev_error = right_error

            left_pid_speed = (
                pid.kp * left_error + pid.ki * left_error_i + pid.kd * left_error_d
            )
            right_pid_speed = (
                pid.kp * right_error + pid.ki * right_error_i + pid.kd * right_error_d
            )
            # self.ev3_print(
            #     self.motor_l.angle(),
            #     self.motor_r.angle(),
            #     "|",
            #     left_error,
            #     left_error_i,
            #     left_error_d,
            #     left_pid_speed,
            # )

            # Limitante de velocidade
            left_speed_sign = -1 if left_pid_speed < 0 else 1
            left_pid_speed = min(75, abs(left_pid_speed)) * left_speed_sign
            right_speed_sign = -1 if right_pid_speed < 0 else 1
            right_pid_speed = min(75, abs(right_pid_speed)) * right_speed_sign

            self.motor_l.dc(left_pid_speed)
            self.motor_r.dc(right_pid_speed)

            left_wheel_angle_distance = self.motor_l.angle() - initial_angle_l
            right_wheel_angle_distance = self.motor_r.angle() - initial_angle_r

            # self.ev3_print("C:", self.motor_l.speed(), self.motor_r.speed())
            if (
                abs(self.motor_l.speed()) < const.PID_TURN_MIN_SPEED
                and abs(self.motor_r.speed()) < const.PID_TURN_MIN_SPEED
                and abs(left_wheel_angle_distance) > const.MIN_DEGREES_CURVE_THRESHOLD
                and abs(right_wheel_angle_distance) > const.MIN_DEGREES_CURVE_THRESHOLD
            ):
                break
        self.stop()
        # self.ev3_print(n, "| END:", self.motor_l.angle(), self.motor_r.angle())

    def line_follower(self, target: int, side: str, pid: PIDControl, speed: int = 50):
        pid = PIDControl(const.LINE_FOLLOWER_VALUES)
        if side == "R":
            sensor = self.color_right
            side = 1
        elif side == "L":
            sensor = self.color_left
            side = -1
        else:
            raise ValueError("Apenas 'R' ou 'L'")

        correction = pid.compute(lambda: sensor.reflection() - target)

        self.motor_l.dc(speed + correction * side)
        self.motor_r.dc(speed - correction * side)

    def wait_button(self, button=Button.CENTER, beep=600):
        return wait_button_pressed(ev3=self.ev3, button=button, beep=beep)

    def ev3_print(
        self,
        *args,
        clear=False,
        end="\n",
        font="Lucida",
        size=16,
        bold=False,
        **kwargs,
    ):
        ev3_print(
            *args,
            ev3=self.ev3,
            clear=clear,
            end=end,
            font=font,
            size=size,
            bold=bold,
            **kwargs,
        )

    def ev3_draw(
        self,
        *args,
        x=0,
        y=0,
        background=False,
        line=0,
        clear=False,
        font="Lucida",
        size=16,
        bold=False,
        **kwargs,
    ):
        ev3_draw(
            *args,
            ev3=self.ev3,
            x=x,
            y=y,
            background=background,
            line=line,
            clear=clear,
            font=font,
            size=size,
            bold=bold,
            **kwargs,
        )

    def align(
        self,
        speed=75,
        pid: PIDValues = PIDValues(kp=1, ki=0.02, kd=2),
        direction_sign=1,
    ):
        initial_color_left = self.color_left.color()
        initial_reflection_left = self.color_left.rgb()[2]

        initial_color_right = self.color_right.color()
        initial_reflection_right = self.color_right.rgb()[2]

        has_seen_left, has_seen_right = False, False

        left_error = 0
        left_error_i = 0
        left_prev_error = 0

        right_error = 0
        right_error_i = 0
        right_prev_error = 0

        while True:
            if not has_seen_left and self.color_left.color() != initial_color_left:
                has_seen_left = True
                left_target = (self.color_left.rgb()[2] + initial_reflection_left) / 2

            if not has_seen_right and self.color_right.color() != initial_color_right:
                has_seen_right = True
                right_target = (
                    self.color_right.rgb()[2] + initial_reflection_right
                ) / 2

            if has_seen_left:
                # PID motor esquerdo
                left_error = self.color_left.rgb()[2] - left_target
                left_error_i += left_error
                left_error_d = left_error - left_prev_error
                left_prev_error = left_error
                left_pid_speed = (
                    pid.kp * left_error + pid.ki * left_error_i + pid.kd * left_error_d
                )
                # Limitante de velocidade
                left_speed_sign = -1 if left_pid_speed < 0 else 1
                left_pid_speed = min(75, abs(left_pid_speed)) * left_speed_sign

                left_speed = left_pid_speed * direction_sign
            else:
                left_speed = speed

            if has_seen_right:
                # PID motor direito
                right_error = self.color_right.rgb()[2] - right_target
                right_error_i += right_error
                right_error_d = right_error - right_prev_error
                right_prev_error = right_error
                right_pid_speed = (
                    pid.kp * right_error
                    + pid.ki * right_error_i
                    + pid.kd * right_error_d
                )
                # Limitante de velocidade
                right_speed_sign = -1 if right_pid_speed < 0 else 1
                right_pid_speed = min(75, abs(right_pid_speed)) * right_speed_sign

                right_speed = right_pid_speed * direction_sign
            else:
                right_speed = speed

            self.motor_l.dc(left_speed)
            self.motor_r.dc(right_speed)

            # self.ev3_print(left_error, left_error_i, right_error, right_error_i)
            if (
                has_seen_left
                and has_seen_right
                and abs(left_error) <= 7
                and abs(right_error) <= 7
            ):
                break
        self.stop()

    def line_grabber(self, time, speed=20, multiplier = 1.5):
        color_reads = []
        num_reads = 10
        wrong_read_perc = 0.5
        color_count_perc = 0.5
        self.stopwatch.reset() 
        self.reset_wheels_angle()

        while True:
            color_reads.append(self.color_left.color())
            if len(color_reads) == num_reads:
                color_count_perc = color_reads.count(Color.BLUE) / num_reads
                wrong_read_perc = 1 - color_count_perc
                color_reads.clear()

            self.motor_l.dc(speed * color_count_perc * multiplier)
            self.motor_r.dc(speed * wrong_read_perc * multiplier)

            motor_mean = (self.motor_l.angle() + self.motor_r.angle()) / 2

            if self.stopwatch.time() > time:
                self.stop()
                return self.motor_degrees_to_cm(motor_mean)