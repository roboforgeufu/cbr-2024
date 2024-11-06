import os

from pybricks.media.ev3dev import Font  # type: ignore
from pybricks.parameters import Button, Color  # type: ignore
from pybricks.tools import StopWatch, wait  # type: ignore


class PIDValues:
    """Variáveis de controle PID."""

    def __init__(
        self,
        kp: float = 0,
        ki: float = 0,
        kd: float = 0,
        target=None,
    ) -> None:
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.target = target

    def set_values(self, error_function):
        self._elapsed_time = 0
        self._i_share = 0
        self._prev_error = 0
        self._error_function = error_function
        self.stopwatch = StopWatch()

    def loopless_pid(
        self,
    ):
        error = self._error_function()
        p_share = error * self.kp

        self._i_share = self._i_share + (error * self.ki)

        wait(1)
        elapsed_time = self.stopwatch.time()

        d_share = ((error - self._prev_error) * self.kd) / (
            elapsed_time - self._elapsed_time
        )

        pid_correction = p_share + self._i_share + d_share

        self._elapsed_time = elapsed_time
        self._prev_error = error

        return pid_correction


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

        ev3.screen.print(*args, **kwargs, end=end)

    print(*args, **kwargs)


def ev3_draw(
    *args,
    ev3=None,
    x=0,
    y=0,
    background=False,
    line=0,
    spacing=22,
    clear=False,
    font="Lucida",
    size=16,
    bold=False,
):
    if ev3 is not None:
        if clear:
            ev3.screen.clear()
        if background:
            background_color = Color.BLACK
            text_color = Color.WHITE
        else:
            background_color = Color.WHITE
            text_color = Color.BLACK

        ev3.screen.draw_text(
            x,
            y + line * spacing,
            str(*args),
            text_color=text_color,
            background_color=background_color,
        )
    print(*args)


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
