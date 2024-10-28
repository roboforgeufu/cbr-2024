from pybricks.ev3devices import ColorSensor


class DecisionColorSensor:
    """
    Encapsula o sensor de cor numa classe que parametriza
    a determinação de cores através de uma árvore de decisão
    """

    def __init__(self, sensor_instance, decision_tree) -> None:
        self.raw_sensor = sensor_instance
        self.decision_tree = decision_tree

    def color(self):
        if isinstance(self.raw_sensor, ColorSensor):
            return self.decision_tree(*self.raw_sensor.rgb())
        else:
            return self.decision_tree(*self.raw_sensor.read("NORM"))

    def reflection(self):
        if isinstance(self.raw_sensor, ColorSensor):
            return self.raw_sensor.reflection()
        else:
            return self.raw_sensor.read("NORM")[3]

    def rgb(self):
        if isinstance(self.raw_sensor, ColorSensor):
            return self.raw_sensor.rgb()
        else:
            return self.raw_sensor.read("NORM")
