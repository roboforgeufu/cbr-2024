#!/usr/bin/env pybricks-micropython

from pybricks.ev3devices import ColorSensor, InfraredSensor, Motor, UltrasonicSensor
from pybricks.hubs import EV3Brick
from pybricks.iodevices import Ev3devSensor
from pybricks.parameters import Button, Color, Port, Stop
from pybricks.tools import DataLog, wait
from pybricks.media.ev3dev import Font


from core.utils import ev3_print, wait_button_pressed

ALL_COLORS = [
    "BLUE",
    "RED",
    "GREEN",
    "BROWN",
    "BLACK",
    "YELLOW",
    "WHITE",
    "None",
]

ALL_PORTS = [
    Port.S1,
    Port.S2,
    Port.S3,
    Port.S4,
]

brick = EV3Brick()


def get_sensor_driver_name(sensor):
    driver_name_path = (
        "/sys/class/lego-sensor/sensor" + str(sensor.sensor_index) + "/driver_name"
    )

    with open(driver_name_path, "r") as d:
        contents = d.read()
        return contents.strip()


def detect_color_sensors():
    """
    Retorna a lista de sensores de cor conectados.
    Formato:
    [
        (sensor: ColorSensor | Ev3devSensor, driver_name: str, port_index: int),
    ]
    """

    driver_name_path = "/sys/class/lego-sensor/sensor"
    sensors = []

    for port in ALL_PORTS:
        try:
            sensor = Ev3devSensor(port)
        except OSError:
            continue

        driver_name = get_sensor_driver_name(sensor)
        if driver_name == "lego-ev3-color":
            sensors.append((ColorSensor(port), driver_name, sensor.port_index + 1))
        elif driver_name == "ht-nxt-color-v2":
            sensors.append((sensor, driver_name, sensor.port_index + 1))

    return sensors


def main():
    brick.screen.set_font(Font("Lucida", 12, False))

    all_sensors = detect_color_sensors()
    for sensor, s_name, s_port in all_sensors:
        ev3_print(s_name, str(s_port), "? ^ ou v", ev3=brick)
        y_n = wait_button_pressed(button=[Button.UP, Button.DOWN], ev3=brick)
        wait(500)
        if y_n == Button.DOWN:
            continue

        for color in ALL_COLORS:
            ev3_print("> " + str(color) + "? ^ ou v", ev3=brick)
            y_n = wait_button_pressed(button=[Button.UP, Button.DOWN], ev3=brick)
            wait(500)
            if y_n == Button.DOWN:
                continue

            logger = DataLog(
                name="calib_" + s_name + "_" + str(s_port) + "_" + str(color),
                timestamp=True,
                extension="csv",
            )
            ev3_print("PROX:", color, ev3=brick)
            wait_button_pressed(ev3=brick)
            ev3_print("LENDO...", ev3=brick)

            for _ in range(100):
                if s_name == "lego-ev3-color":
                    # Sensor do RGB
                    logger.log(*sensor.rgb())
                else:
                    # Hi Technic (valores normalizados)
                    logger.log(*sensor.read("NORM"))

                wait(100)

            ev3_print("DONE:", color, ev3=brick)


if __name__ == "__main__":
    main()
