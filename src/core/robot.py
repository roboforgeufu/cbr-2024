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
from core.utils import ev3_print, wait_button_pressed
from core.decision_color_sensor import DecisionColorSensor
from pybricks.parameters import Button
from core.utils import PIDValues
import constants as const

import math


"""
Módulo central pra controle do Robô.

Devem estar nesse módulo:
    - Classe 'Robot' e 'OmniRobot', com métodos e atributos para controle geral no robô
    - Estruturas de dados auxiliares aplicáveis a "qualquer" tipo de robô

Não devem estar nesse módulo:
    - Código específico de algum problema/desafio ou comunicação.
"""

#
# Robô com duas rodas
#


class Robot:

    # Classe que representa um robô genérico

    def __init__(
        self,
        wheel_diameter,
        wheel_distance,
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
        debug=True,
    ):

        # Ev3
        self.ev3 = EV3Brick()

        self.stopwatch = StopWatch()

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
        # TODO

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

    def set_wheels_angle(self, angle):

        # Zera o ângulo das rodas
        self.r_wheel.reset_angle(angle)
        self.l_wheel.reset_angle(angle)

    def off_motors(self):
        """Desliga motores de locomoção."""
        self.motor_l.dc(0)
        self.motor_r.dc(0)
        self.motor_l.hold()
        self.motor_r.hold()
        self.motor_l.dc(0)
        self.motor_r.dc(0)

    def wheels_angle(self):

        # Retorna a média do ângulo das duas rodas
        return (self.l_wheel.angle() + self.l_wheel.angle()) / 2

    def abs_wheels_angle(self):

        # Retorna a média do módulo do ângulo das duas rodas
        return (abs(self.r_wheel.angle()) + abs(self.l_wheel.angle())) / 2

    def walk(self, dc=100, angle=None, pid=False):
        # TODO: passar valor em centímetros

        # Movimenta o robô
        if pid:
            pass

        else:
            if angle != None:
                self.set_wheels_angle(0)
                while abs(angle) >= self.abs_wheels_angle():
                    self.r_wheel.dc(dc)
                    self.l_wheel.dc(dc)
                self.hold_wheels()
            else:
                self.r_wheel.dc(dc)
                self.l_wheel.dc(dc)

    def pid_walk(
        self,
        cm,
        speed=60,
        obstacle_function=None,
        off_motors=True,
    ):
        """Anda em linha reta com controle PID entre os motores."""
        degrees = self.cm_to_motor_degrees(cm)

        elapsed_time = 0
        i_share = 0
        error = 0
        motor_angle_average = 0
        initial_left_angle = self.motor_l.angle()
        initial_right_angle = self.motor_r.angle()
        self.stopwatch.reset()

        has_seen_obstacle = False
        while abs(motor_angle_average) < abs(degrees):
            if obstacle_function is not None and obstacle_function():
                has_seen_obstacle = True
                break

            motor_angle_average = (
                (self.motor_l.angle() - initial_left_angle)
                + (self.motor_r.angle() - initial_right_angle)
            ) / 2

            elapsed_time, i_share, error = self.loopless_pid_walk(
                elapsed_time,
                i_share,
                error,
                vel=speed,
                initial_left_angle=initial_left_angle,
                initial_right_angle=initial_right_angle,
            )

        if off_motors:
            self.off_motors()
        return has_seen_obstacle

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
        error = (self.motor_r.angle() - initial_right_angle) - (
            self.motor_l.angle() - initial_left_angle
        )
        p_share = error * pid.kp

        if abs(error) < 3:
            i_share = i_share + (error * pid.ki)

        wait(1)
        elapsed_time = self.stopwatch.time()

        d_share = ((error - prev_error) * pid.kd) / (elapsed_time - prev_elapsed_time)

        pid_correction = p_share + i_share + d_share
        self.motor_r.dc(vel - pid_correction)
        self.motor_l.dc(vel + pid_correction)

        return (elapsed_time, i_share, error)

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
        self.off_motors()
        # self.ev3_print(n, "| END:", self.motor_l.angle(), self.motor_r.angle())

    def wait_button(self, button=Button.CENTER):
        return wait_button_pressed(ev3=self.ev3, button=button)

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

    def walk_while_same_reflection(self, speed=200):
        """Retorna o tempo passado andando até chegar na cor diferente"""
        ...

    def align(
        self,
        pid: PIDValues = PIDValues(kp=1, ki=0.015, kd=1.5),
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
                left_speed = 75

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
                right_speed = 75

            self.motor_l.dc(left_speed)
            self.motor_r.dc(right_speed)

            self.ev3_print(left_error, left_error_i, right_error, right_error_i)
            if (
                has_seen_left
                and has_seen_right
                and abs(left_error) <= 7
                and abs(right_error) <= 7
            ):
                break
        self.off_motors()


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
                while abs(angle) >= self.abs_wheels_angle():
                    self.vertical_run(duty)

            elif direction == "horizontal":
                while abs(angle) >= self.abs_wheels_angle():
                    self.horizontal_run(duty, side)

        else:

            if direction == "vertical":
                self.vertical_run(duty)

            elif direction == "horizontal":
                self.horizontal_run(duty, side)

    def turn(self, duty=100, angle=0, pid=False):

        if angle > 0:
            angle = self.real_angle_to_motor_degrees(angle)
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
