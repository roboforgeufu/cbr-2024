#!/usr/bin/env pybricks-micropython

"""
Módulo central de codificação.

Devem estar nesse módulo:
    - Métodos de codificação e decodificação de mensagens, com comentários e exemplos.

Não devem estar nesse módulo:
    - Código específico de algum problema/desafio
"""
from pybricks.parameters import Color


def encoder(decoded_message):

    # Codifica a mensagem em uma string, indicando o tipo no começo para facilitar os logs e a decodificação.
    # Admite os tipos int, float, string, dict, list, tuple e set (Conjuntos podem ser recursivos e sempre retornam como tuplas)

    if isinstance(decoded_message, str):
        tipo = "Str"
        encoded_message = tipo + ": " + decoded_message

    elif isinstance(decoded_message, bool):
        tipo = "Bool"
        encoded_message = tipo + ": " + str(decoded_message)

    elif isinstance(decoded_message, (int)):
        tipo = "Int"
        encoded_message = tipo + ": " + str(decoded_message)

    elif isinstance(decoded_message, (float)):
        tipo = "Float"
        encoded_message = tipo + ": " + str(decoded_message)

    elif isinstance(decoded_message, (dict)):
        tipo = "Dict"
        encoded_message = tipo + ": " + str(decoded_message)

    elif isinstance(decoded_message, (list, tuple, set)):
        tipo = "List"
        encoded_elements = []
        for element in decoded_message:
            # Codifica cada elemento recursivamente
            encoded_elements.append(encoder(element))
        encoded_message = tipo + ": " + ",".join(encoded_elements)

    elif decoded_message is None or isinstance(decoded_message, Color):
        tipo = "Color"
        encoded_message = tipo + ": " + str(decoded_message)

    return "(" + encoded_message + ")"


def decoder(encoded_message):

    # Decodifica a mensagem no tipo especificado no começo da string

    if encoded_message is None:
        return None

    # Remove parênteses e divide o tipo da mensagem
    stripped_message = encoded_message.strip("()")
    tipo, string_message = stripped_message.split(": ", 1)

    if tipo == "Str":
        decoded_message = string_message

    elif tipo == "Bool":
        decoded_message = string_message == "True"

    elif tipo == "Int":
        decoded_message = int(string_message)

    elif tipo == "Float":
        decoded_message = float(string_message)

    elif tipo == "Dict" or tipo == "Color":
        decoded_message = eval(string_message)

    elif tipo == "List":

        # Divide os elementos da lista considerando elementos aninhados
        list_message = []
        current_element = ""
        depth = 0

        for char in string_message:
            if char == "(":
                depth += 1
            elif char == ")":
                depth -= 1

            # Se estamos fora de parênteses e encontramos uma vírgula, finalizamos o elemento
            if char == "," and depth == 0:
                list_message.append(current_element.strip())
                current_element = ""
            else:
                current_element += char

        # Adiciona o último elemento se houver
        if current_element:
            list_message.append(current_element.strip())

        decoded_list = []

        for parsed_message in list_message:
            # Decodifica cada elemento da lista recursivamente
            decoded_list.append(decoder(parsed_message))

        decoded_message = tuple(
            decoded_list
        )  # Retornando em tupla para preservar compatibilidade

    return decoded_message
