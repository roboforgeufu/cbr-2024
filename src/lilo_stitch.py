#!/usr/bin/env pybricks-micropython

from core.omni_robot import OmniRobot
from core.utils import get_hostname
from core.decision_color_sensor import DecisionColorSensor

from pybricks.parameters import Port
from pybricks.ev3devices import ColorSensor


def lilo_main(lilo: OmniRobot):
    # lilo.bluetooth.start()

    #
    # Localização inicial
    #

    while True:
        #
        # Coleta de passageiros
        #

        #
        # Pathfinding e movimentação (obstáculos)
        #

        #
        # Desembarque de passageiros
        #

        #
        # Retorno a zona de embarque
        #
        pass


def stitch_main(stitch: OmniRobot):
    stitch.bluetooth.start()

    #
    # Localização inicial
    #

    while True:
        #
        # Coleta de passageiros
        #

        #
        # Pathfinding e movimentação (obstáculos)
        #

        #
        # Desembarque de passageiros
        #

        #
        # Retorno a zona de embarque
        #
        pass


def main(hostname):
    if hostname == "lilo":
        lilo_main(
            OmniRobot(
                motor_front_left=Port.B,
                motor_front_right=Port.C,
                motor_back_left=Port.A,
                motor_back_right=Port.D,
                color_front_left=DecisionColorSensor(ColorSensor(Port.S3), ...),
                color_front_right=DecisionColorSensor(ColorSensor(Port.S2), ...),
                color_back_left=DecisionColorSensor(ColorSensor(Port.S1), ...),
                color_back_right=DecisionColorSensor(ColorSensor(Port.S4), ...),
                server_name="lilo",
            )
        )
    elif hostname == "stitch":
        stitch_main(
            OmniRobot(
                server_name="lilo",
            )
        )


if __name__ == "__main__":
    main(get_hostname())
