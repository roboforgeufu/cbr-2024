import os

def get_hostname() -> str:
        """
        Retorna o hostname do dispositivo. Feito pensando em verificar o nome do BRICK.
        """
        stream = os.popen("hostname")  # nosec
        return stream.read().split()[0]