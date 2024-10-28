#!/usr/bin/env pybricks-micropython

"""
Módulo para centralização dos processos e gerência da estratégia geral.

Podem estar nesse módulo coisas como:
    - Código que controla a ordem que as rotinas serão executadas
    - Código para controle de fluxo geral do robô
    - Chamadas a rotinas mais específicas
    - Instanciação de estruturas de dados, classes, etc.
    - Códigos específicos de comunicação com o EV3 ou gerência de recursos de sistemas
        operacionais no geral
    - Várias funções "main" alternativas, inclusive para testes ou calibragem de
        motores/sensores

Não devem estar nesse módulo:
    - Definição de constantes ou variáveis globais
    - Chamadas de função fora de escopo da main do módulo
    - Execução de código manipulando motores ou sensores diretamente

OBS:. As direções são determinadas a partir do POV do robô
"""

from core.robot import Robot
from core.utils import get_hostname
from pybricks.parameters import Port

import constants as const


def sandy_main(sandy: Robot):
    # 
    # Localização inicial
    # 

    while True:
        # 
        # Coleta de passageiros
        #
         
        # 
        # Pathfinding e movimentação (obstáculos)
        # 

        # 
        # Desembarque de passageiros
        # 

        # 
        # Retorno a zona de embarque
        # 
        ...


def junior_main(junior: Robot):
    # 
    # Localização inicial
    # 

    while True:
        # 
        # Coleta de passageiros
        #
         
        # 
        # Pathfinding e movimentação (obstáculos)
        # 

        # 
        # Desembarque de passageiros
        # 

        # 
        # Retorno a zona de embarque
        # 
        ...

        
def main():
    if get_hostname() == "sandy":
        sandy_main(
            Robot(
                wheel_diameter=const.WHEEL_DIAMETER,wheel_distance=const.WHEEL_DIST,
                motor_r=Port.B,
                motor_l=Port.C,
                infra_side=Port.S1,
                ultra_feet=Port.S2,
                color_right=Port.S3,
                color_left=Port.S4
            )
        )
    else:
        junior_main(
            Robot(
                motor_elevate_claw=Port.C,
                motor_open_claw=Port.B,
                color_claw=Port.S1,
                ultra_head=Port.S2
            )
        )

