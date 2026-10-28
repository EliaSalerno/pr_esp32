import time
from machine import UART, Pin

uart=UART(1,baudrat=9600,tx=Pin(17),
