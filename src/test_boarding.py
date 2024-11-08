#!/usr/bin/env pybricks-micropython
from pybricks.parameters import Port, Button # type: ignore
from pybricks.ev3devices import ColorSensor # type: ignore
from pybricks.tools import wait # type: ignore

from core.robot import Robot
from core.utils import get_hostname
from core.decision_color_sensor import DecisionColorSensor

import constants as const
from domain.localization import localization_routine
from domain.pathfinding import Graph, map_matrix, get_target_for_passenger
from domain.boarding import passenger_boarding, passenger_unboarding
from domain.path_control import path_control
from decision_trees.ht_nxt_color_v2_2 import ht_nxt_color_v2_p2_decision_tree
from decision_trees.lego_ev3_color_1 import levo_ev3_color_1_decision_tree
from decision_trees.sandy_lego_ev3_color_3 import lego_ev3_color_p3_decision_tree
from decision_trees.sandy_lego_ev3_color_4 import lego_ev3_color_p4_decision_tree

passenger_boarding(Robot(
                wheel_diameter=const.WHEEL_DIAMETER,
                wheel_distance=const.WHEEL_DIST,
                motor_r=Port.B,
                motor_l=Port.C,
                infra_side=Port.S1,
                ultra_feet=Port.S2,
                color_right=DecisionColorSensor(
                    ColorSensor(Port.S3), lego_ev3_color_p3_decision_tree
                ),
                color_left=DecisionColorSensor(
                    ColorSensor(Port.S4), lego_ev3_color_p4_decision_tree
                ),
            )
)