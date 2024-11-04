#!/usr/bin/env pybricks-micropython
from core.robot import Robot
from pybricks.parameters import Port # type: ignore

r = Robot(motor_elevate_claw=Port.C, motor_open_claw=Port.B, ultra_head=Port.S1)