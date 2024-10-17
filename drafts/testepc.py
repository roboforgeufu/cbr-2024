import socket
import msvcrt
from core.encoding import encoder

# Conecta WIFI
wifi = socket.socket()
# IPaddress = (input("Digite endereço IP: "))
IPaddress = (("192.168.137.97"))
wifi.connect((IPaddress, 12345))

key = b'A'
while True:
    key = msvcrt.getch().decode('utf-8')  # Captura a tecla pressionada
    if ord(key) == 8: # Backspace
        wifi.send("backspace".encode())
    elif ord(key) == 13:
        wifi.send("enter".encode())
    else:
        wifi.send(key.encode())
        print(key)

    
