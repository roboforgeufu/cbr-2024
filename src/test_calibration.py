#!/usr/bin/env pybricks-micropython

from pybricks.ev3devices import ColorSensor, InfraredSensor, Motor, UltrasonicSensor
from pybricks.hubs import EV3Brick
from pybricks.parameters import Button, Color, Port, Stop
from pybricks.iodevices import Ev3devSensor

from pybricks.tools import DataLog, wait

from decision_trees.ht_nxt_color_v2 import hitechnic_decision_tree
from core.utils import ev3_print


def test_calibration():
    brick = EV3Brick()
    sensor = Ev3devSensor(Port.S2)

    while True:
        ev3_print("S:", hitechnic_decision_tree(*sensor.read("NORM")), ev3=brick)

        wait(100)
        brick.screen.clear()


if __name__ == "__main__":
    test_calibration()
