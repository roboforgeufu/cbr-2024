#!/usr/bin/env pybricks-micropython

from pybricks.ev3devices import ColorSensor, InfraredSensor, Motor, UltrasonicSensor
from pybricks.hubs import EV3Brick
from pybricks.parameters import Button, Color, Port, Stop
from pybricks.iodevices import Ev3devSensor

from pybricks.tools import DataLog, wait

from decision_trees.lego_ev3_color_3 import lego_ev3_color_p3_decision_tree
from decision_trees.lego_ev3_color_4 import lego_ev3_color_p4_decision_tree

from core.utils import ev3_print


def test_calibration():
    brick = EV3Brick()
    sensor3 = ColorSensor(Port.S3)
    sensor4 = ColorSensor(Port.S4)

    while True:
        ev3_print("S3:", lego_ev3_color_p3_decision_tree(*sensor3.rgb()), ev3=brick)
        ev3_print("S4:", lego_ev3_color_p4_decision_tree(*sensor4.rgb()), ev3=brick)

        wait(100)
        brick.screen.clear()


if __name__ == "__main__":
    test_calibration()
