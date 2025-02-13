#!/usr/bin/env pybricks-micropython
from pybricks.parameters import Button # type: ignore
from core.robot import Robot

r = Robot()

def screen(*options, selected=None, error:str=None, clear=False):
    lines = len(options)
    if clear: r.ev3.screen.clear()
    for line in range(lines-1):
        r.ev3_draw(options[line], background=selected==line, line=line)
    if error is not None: r.ev3_draw(*error, line=lines)

def menu(options: list, headers: list):
    while True:
        if isinstance(options, list):
        
