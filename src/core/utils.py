import os

from pybricks.media.ev3dev import Font
from pybricks.parameters import Button


def get_hostname() -> str:
    """
    Retorna o hostname do dispositivo. Feito pensando em verificar o nome do BRICK.
    """
    stream = os.popen("hostname")  # nosec
    return stream.read().split()[0]


def ev3_print(
    *args,
    ev3=None,
    clear=False,
    font="Lucida",
    size=16,
    bold=False,
    x=0,
    y=0,
    background=None,
    end="\n",
    **kwargs,
):
    """
    Função para logs.
    Imprime os valores tanto na tela do EV3 (caso disponível) quanto na do terminal.
    A opção 'clear' controla se a tela do EV3 é limpada a cada novo print.
    """

    if ev3 is not None:
        if clear:
            ev3.screen.clear()

        # ev3.screen.set_font(Font(font, size, bold))

        if x != 0 or y != 0 or background != None:
            ev3.screen.draw_text(x, y, str(*args), background_color=background)
        else:
            ev3.screen.print(*args, **kwargs, end=end)
    print(*args, **kwargs)


def wait_button_pressed(ev3, button: Button = Button.CENTER, beep=True):
    """
    Trava execução até que o botão especificado seja pressionado.
    Pode receber uma lista de botões. Retorna qual botão foi ativado primeiro.
    """
    if beep:
        ev3.speaker.beep(800)

    while True:

        if isinstance(button, list):
            for btn in button:
                if btn in ev3.buttons.pressed():
                    return btn

        elif button in ev3.buttons.pressed():
            return button
