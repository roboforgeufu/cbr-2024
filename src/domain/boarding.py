import constants as const
from core.robot import Robot
from core.network import Bluetooth
from pybricks.parameters import Color # type: ignore

def passenger_boarding(robot: Robot):
    """
    Rotina de encontrar um passageiro, pega-lo e detectar faixa etária e cor.

    Retorna uma tupla como ("CHILD", Color.BLUE) ou ("ADULT", Color.GREEN)
    """
    while robot.infra_side.distance <= 50:
        robot.walk(100)
    robot.motor_open_claw.run_until_stalled(-80)
    robot.turn(-90)


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


def passenger_boarding(robot: Robot):
    """
    Rotina de embarque de passageiro
    """


def passenger_unboarding(robot: Robot):
    """
    Rotina de desembarque de passageiro
    """
