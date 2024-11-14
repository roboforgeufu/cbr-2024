"""
Centralização de definição de constantes.

Devem estar nesse módulo:
    - Definição de variáveis constantes (e que obviamente não devem ser alteradas em
        execução)
    - Comentários sobre o que significam as constantes
    - Constantes com nomes bem significativos

Não devem estar nesse módulo:
    - Qualquer tipo de código além de declaração de constantes
    - Variáveis globais utilizadas para controle de algoritmos (que sofrem alterações em
        execução)
"""

import math
import json
from core.utils import get_hostname

from core.utils import PIDValues


def load_json_file():
    with open("pid_const.json", "r") as file:
        data = json.load(file)
    return data


const_map = load_json_file()
hostname = get_hostname()

# Constantes PID

PID_WALK_VALUES = PIDValues.from_list(const_map[hostname]["pid_walk"])
PID_TURN_VALUES = PIDValues.from_list(const_map[hostname]["pid_turn"])
ALIGN_VALUES = PIDValues.from_list(const_map[hostname]["align"])
LINE_FOLLOWER_VALUES = PIDValues.from_list(const_map[hostname]["line_follower"])

# Dimensões do robô
WHEEL_DIAMETER = 6.8
WHEEL_DIST = 16.1
WHEEL_LENGTH = WHEEL_DIAMETER * math.pi

ROBOT_SIZE = 15  # considerando a distância dos sensores de cor da frente até a parte de trás do robô
ROBOT_SIZE_HALF = ROBOT_SIZE / 2

# Curvas com PID
PID_TURN_ACCEPTABLE_DEGREE_DIFF = 3
PID_TURN_MIN_SPEED = 5
MIN_DEGREES_CURVE_THRESHOLD = 30

# Comunicação Bluetooth
SERVER_NAME = "sandy"


# Distâncias
OMNI_WALK_DISTANCE_CORRECTION = 0.95

OMNI_SIDE_ALING_PERCENTAGE = 0.53


# Obstáculos
OBSTACLE_DISTANCE = 150

LINE_FOLLOW_TARGET_REFLECTION = 30


CELL_DISTANCE = 25
CELL_DISTANCE_TO_PARK = 20
CELL_DISTANCE_TO_BOARDING = 15


# Calibração de cor
MAP_COLOR_CALIBRATION = "OFICIAL"  # OFICIAL, HOME, TEST
