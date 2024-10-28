import socket
import msvcrt
from core.encoding import encoder

# Conecta WIFI
wifi = socket.socket()
# IPaddress = (input("Digite endereço IP: "))
IPaddress = (("192.168.137.49"))
wifi.connect((IPaddress, 12345))

while True:
    key = msvcrt.getch().decode('utf-8')  # Captura a tecla pressionada
    if ord(key) == 13:
        enter = ("enter").encode()
        wifi.send(enter)
    elif ord(key) == 32:
        space = ("space").encode()
        wifi.send(aaaspace)
    elif ord(key) == 8:
        backspace = ("backspace").encode()
        wifi.send(backspace)
    else:
        wifi.send(key.encode())
    print(key)

    
