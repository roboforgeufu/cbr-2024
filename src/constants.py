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

# Dimensões do robô
WHEEL_DIAMETER = 5.5
WHEEL_DIST = 16.2
WHEEL_LENGTH = WHEEL_DIAMETER * math.pi

ROBOT_SIZE = 23
ROBOT_SIZE_HALF = ROBOT_SIZE / 2

