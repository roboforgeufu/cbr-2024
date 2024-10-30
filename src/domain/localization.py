from core.robot import Robot
from pybricks.parameters import Color

# TODO substituir as condições pelo tratamento de cores
# TODO testar o robô para criar logs que permitam diferenciar os vértices
# TODO descobrir se usaremos árvore de decisão ou apenas condicionais
# TODO incrementar os resultados de diferenciação na função adivinhar vértice
# TODO conectar com o restante do código

""" 
Abaixo estão as combinações e os vértices em que elas aparecem.

    ['AM', 'VM', 'AM', 'VM']: [1, 14],
    ['VM', 'AM', 'VM', 'AM']: [1, 14],
    ['PR', 'VM', 'AM', 'VM']: [3, 16, 27, 29]
    ['VM', 'AM', 'VM', 'PR']: [3, 16, 27, 29]
    ['AM', 'VM', 'PR', 'VM']: [3, 16, 27, 29]
    ['VM', 'PR', 'VM', 'AM']: [3, 16, 27, 29]
    ['PR', 'VM', 'AZ', 'VM']: [5, 9, 11, 18, 20, 22, 24]
    ['VM', 'AZ', 'VM', 'PR']: [5, 9, 11, 18, 20, 22, 24]
    ['AZ', 'VM', 'PR', 'VM']: [5, 9, 11, 18, 20, 22, 24]
    ['VM', 'PR', 'VM', 'AZ']: [5, 9, 11, 18, 20, 22, 24]
    ['PR', 'VM', 'AZ', 'AM']: [7]
    ['VM', 'AZ', 'AM', 'PR']: [7]
    ['AZ', 'AM', 'PR', 'VM']: [7]
    ['AM', 'PR', 'VM', 'AZ']: [7]
    ['PR', 'PR', 'AZ', 'AM']: [8]
    ['PR', 'AZ', 'AM', 'PR']: [8]
    ['AZ', 'AM', 'PR', 'PR']: [8]
    ['AM', 'PR', 'PR', 'AZ']: [8]
    ['PR', 'AM', 'AZ', 'AM']: [10, 23]
    ['AM', 'AZ', 'AM', 'PR']: [10, 23]
    ['AZ', 'AM', 'PR', 'AM']: [10, 23]
    ['AM', 'PR', 'AM', 'AZ']: [10, 23]
    ['PR', 'AM', 'AZ', 'PR']: [21]
    ['AM', 'AZ', 'PR', 'PR']: [21]
    ['AZ', 'PR', 'PR', 'AM']: [21]
    ['PR', 'PR', 'AM', 'AZ']: [21]
    ['AM', 'VM', 'AZ', 'VM']: [31]
    ['VM', 'AZ', 'VM', 'AM']: [31]
    ['AZ', 'VM', 'AM', 'VM']: [31]
    ['VM', 'AM', 'VM', 'AZ']: [31]
"""

laterais_vertices = [
    [
        [1],
        ["AM", "VM", "AM", "VM"],
        ["VM", "AM", "VM", "AM"],
        ["AM", "VM", "AM", "VM"],
        ["VM", "AM", "VM", "AM"],
    ],
    [
        [3],
        ["PR", "VM", "AM", "VM"],
        ["VM", "AM", "VM", "PR"],
        ["AM", "VM", "PR", "VM"],
        ["VM", "PR", "VM", "AM"],
    ],
    [
        [5],
        ["PR", "VM", "AZ", "VM"],
        ["VM", "AZ", "VM", "PR"],
        ["AZ", "VM", "PR", "VM"],
        ["VM", "PR", "VM", "AZ"],
    ],
    [
        [7],
        ["PR", "VM", "AZ", "AM"],
        ["VM", "AZ", "AM", "PR"],
        ["AZ", "AM", "PR", "VM"],
        ["AM", "PR", "VM", "AZ"],
    ],
    [
        [8],
        ["PR", "PR", "AZ", "AM"],
        ["PR", "AZ", "AM", "PR"],
        ["AZ", "AM", "PR", "PR"],
        ["AM", "PR", "PR", "AZ"],
    ],
    [
        [9],
        ["PR", "VM", "AZ", "VM"],
        ["VM", "AZ", "VM", "PR"],
        ["AZ", "VM", "PR", "VM"],
        ["VM", "PR", "VM", "AZ"],
    ],
    [
        [10],
        ["PR", "AM", "AZ", "AM"],
        ["AM", "AZ", "AM", "PR"],
        ["AZ", "AM", "PR", "AM"],
        ["AM", "PR", "AM", "AZ"],
    ],
    [
        [11],
        ["PR", "VM", "AZ", "VM"],
        ["VM", "AZ", "VM", "PR"],
        ["AZ", "VM", "PR", "VM"],
        ["VM", "PR", "VM", "AZ"],
    ],
    [
        [14],
        ["AM", "VM", "AM", "VM"],
        ["VM", "AM", "VM", "AM"],
        ["AM", "VM", "AM", "VM"],
        ["VM", "AM", "VM", "AM"],
    ],
    [
        [16],
        ["AM", "VM", "PR", "VM"],
        ["VM", "PR", "VM", "AM"],
        ["PR", "VM", "AM", "VM"],
        ["VM", "AM", "VM", "PR"],
    ],
    [
        [18],
        ["PR", "VM", "AZ", "VM"],
        ["VM", "AZ", "VM", "PR"],
        ["AZ", "VM", "PR", "VM"],
        ["VM", "PR", "VM", "AZ"],
    ],
    [
        [20],
        ["PR", "VM", "AZ", "VM"],
        ["VM", "AZ", "VM", "PR"],
        ["AZ", "VM", "PR", "VM"],
        ["VM", "PR", "VM", "AZ"],
    ],
    [
        [21],
        ["PR", "AM", "AZ", "PR"],
        ["AM", "AZ", "PR", "PR"],
        ["AZ", "PR", "PR", "AM"],
        ["PR", "PR", "AM", "AZ"],
    ],
    [
        [22],
        ["PR", "VM", "AZ", "VM"],
        ["VM", "AZ", "VM", "PR"],
        ["AZ", "VM", "PR", "VM"],
        ["VM", "PR", "VM", "AZ"],
    ],
    [
        [23],
        ["PR", "AM", "AZ", "AM"],
        ["AM", "AZ", "AM", "PR"],
        ["AZ", "AM", "PR", "AM"],
        ["AM", "PR", "AM", "AZ"],
    ],
    [
        [24],
        ["PR", "VM", "AZ", "VM"],
        ["VM", "AZ", "VM", "PR"],
        ["AZ", "VM", "PR", "VM"],
        ["VM", "PR", "VM", "AZ"],
    ],
    [
        [27],
        ["AM", "VM", "PR", "VM"],
        ["VM", "PR", "VM", "AM"],
        ["PR", "VM", "AM", "VM"],
        ["VM", "AM", "VM", "PR"],
    ],
    [
        [29],
        ["AM", "VM", "PR", "VM"],
        ["VM", "PR", "VM", "AM"],
        ["PR", "VM", "AM", "VM"],
        ["VM", "AM", "VM", "PR"],
    ],
    [
        [31],
        ["AM", "VM", "AZ", "VM"],
        ["VM", "AZ", "VM", "AM"],
        ["AZ", "VM", "AM", "VM"],
        ["VM", "AM", "VM", "AZ"],
    ],
]


def ler_cor(color):
    if color == "Color.RED":
        return "VM"
    elif color == "Color.YELLOW":
        return "AM"
    elif color == "Color.BLUE":
        return "AZ"
    elif color == "Color.BLACK":
        return "PR"
    else:
        return None


def rotina_azul(robot: Robot):  # chega de frente no azul
    robot.turn(90)
    while robot.color_sensor.color() != Color.RED:
        robot.walk()
    robot.turn(90)
    while robot.color_sensor.color() == "Color.WHITE":
        robot.walk()
    if robot.color_sensor.color() == "Color.YELLOW":
        return "V31"
    return "V5"


def preenche_lista(
    robot: Robot,
):  # vai andar para as 4 orientações e guardar a cor e medir o tempo para diferenciar o vértice
    inicio = robot.watch()
    lista = []
    while robot.color_sensor.color() == "Color.WHITE":
        robot.walk()
        if robot.color_sensor.color() == "Color.BLUE":
            rotina_azul()
        else:
            lista.append(ler_cor())
            fim = robot.watch()

            robot.hold_wheels()
            robot.turn(90)
        return lista  # vai ficar no formato tipo ["VM",947,"AM",345,"VM",358,"PR",347] depois de chamar 4 vezes na main


def interpreta_lista(lista):
    for vertice_info in laterais_vertices:
        vertice_id = vertice_info[0][0]
        combinacoes = vertice_info[1:]
        if lista in combinacoes:
            return "V{}".format(vertice_id)
    return None


resultado = interpreta_lista(
    ["AM", "VM", "AM", "VM"]
)  # retorna apenas o 1º id, fazer alteração para ter um tempo de cada movimentação


def localization_routine(robot: Robot):
    """
    Rotina de localização inicial do robô.
    Termina na origem: posição fixa pra iniciar a rotina de coleta de passageiros.
    """
    ...
