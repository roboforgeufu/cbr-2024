#!/usr/bin/env pybricks-micropython

from pybricks.ev3devices import ColorSensor, InfraredSensor, Motor, UltrasonicSensor  # type: ignore
from pybricks.hubs import EV3Brick  # type: ignore
from pybricks.parameters import Button, Color, Port, Stop  # type: ignore
from pybricks.iodevices import Ev3devSensor  # type: ignore

from pybricks.tools import DataLog, wait  # type: ignore

from decision_trees.sandy_lego_ev3_color_3 import sandy_lego_ev3_color_p3_decision_tree
from decision_trees.sandy_lego_ev3_color_4 import sandy_lego_ev3_color_p4_decision_tree
from decision_trees.lilo_lego_ev3_color_1 import lilo_lego_ev3_color_p1_decision_tree
from decision_trees.lilo_lego_ev3_color_2 import lilo_lego_ev3_color_p2_decision_tree
from decision_trees.lilo_lego_ev3_color_3 import lilo_lego_ev3_color_p3_decision_tree
from decision_trees.lilo_lego_ev3_color_4 import lilo_lego_ev3_color_p4_decision_tree
from decision_trees.ht_nxt_color_v2_2 import ht_nxt_color_v2_p2_decision_tree


from core.utils import ev3_print, get_hostname

brick_name_to_sensors_and_functions = {
    "lilo": [
        ("S1", ColorSensor, Port.S1, lilo_lego_ev3_color_p1_decision_tree),
        ("S2", ColorSensor, Port.S2, lilo_lego_ev3_color_p2_decision_tree),
        ("S3", ColorSensor, Port.S3, lilo_lego_ev3_color_p3_decision_tree),
        ("S4", ColorSensor, Port.S4, lilo_lego_ev3_color_p4_decision_tree),
    ],
    "stitch": ["S4", Ev3devSensor, Port.S4, ht_nxt_color_v2_p2_decision_tree],
    "sandy": [
        ("S3", ColorSensor, Port.S3, sandy_lego_ev3_color_p3_decision_tree),
        ("S4", ColorSensor, Port.S4, sandy_lego_ev3_color_p4_decision_tree),
    ],
    "junior": ["S2", ColorSensor, Port.S2, ...],
}


def test_calibration():

    brick = EV3Brick()
    sensor_info = brick_name_to_sensors_and_functions[get_hostname()]

    sensors = []
    for _, s_class, s_port, _ in sensor_info:
        sensors.append(s_class(s_port))

    while True:
        for (s_name, s_class, s_port, s_function), sensor in zip(sensor_info, sensors):
            if "ht-nxt" in s_name:
                ev3_print(s_port, "-", s_function(*sensor.read("NORM")), ev3=brick)
            else:
                ev3_print(s_port, "-", s_function(*sensor.rgb()), ev3=brick)

        wait(100)
        brick.screen.clear()


if __name__ == "__main__":
    test_calibration()
