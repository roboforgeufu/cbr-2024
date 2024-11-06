import constants as const
from core.robot import Robot
from core.network import Bluetooth
from pybricks.parameters import Color  # type: ignore
from domain.star_platinum import star_platinum
from core.utils import PID


def passenger_boarding(robot: Robot):
    """
    Rotina de encontrar um passageiro, pega-lo e detectar faixa etária e cor.

    Retorna uma tupla como ("CHILD", Color.BLUE) ou ("ADULT", Color.GREEN)
    """
    i_share = 0
    elapsed_time = 0
    previous_error = 0
    while robot.infra_side.distance() >= 45:
        elapsed_time, i_share, previous_error = robot.loopless_pid_walk()
    while robot.infra_side.distance() < 45:
        elapsed_time, i_share, previous_error = robot.loopless_pid_walk(prev_elapsed_time=elapsed_time, i_share = i_share, prev_error=previous_error)
    robot.pid_turn(-90)
    star_platinum(robot, "DOWN")
    star_platinum(robot, "OPEN")
    robot.align(40)
    star_platinum(robot, "CLOSE")
    star_platinum(robot, "PASSENGER INFO")
    passenger = robot.bluetooth.message()
    robot.ev3_print(passenger)


def smart_walk(robot: Robot):
    """O que será a movimentação no início e
    envia mensagens de abrir e fechar a garra"""


def passenger_read_color_and_type(robot: Robot):
    """Retorna cor e se é adulto ou criança -> ("CHILD", Color.BLUE)"""


def passenger_read_type(robot: Robot):
    """Retorna se é adulto ou criança"""


def passenger_traject(robot: Robot):
    """Chama funções de movimentação depois
    de ver quais vértices são o início e o fim"""


def passenger_unboarding(robot: Robot):
    """
    Rotina de desembarque de passageiro
    """
