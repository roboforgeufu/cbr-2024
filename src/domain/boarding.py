import constants as const
from core.network import Bluetooth

def passenger_boarding(robot: Robot): # type: ignore
    """
    Rotina de encontrar um passageiro, pega-lo e detectar faixa etária e cor.

    Retorna uma tupla como ("CHILD", Color.BLUE) ou ("ADULT", Color.GREEN)
    """
    while robot.infra_side.distance <= 50:
        robot.walk(100)
    robot.motor_open_claw.run_until_stalled(-80)
    robot.turn(-90)


def passenger_unboarding(robot: Robot): # type: ignore
    """
    Rotina de desembarque de passageiro
    """
