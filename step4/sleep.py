import machine
import esp32

pin = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP)

esp32.wake_on_ext0(pin=pin, level=esp32.WAKEUP_ALL_LOW)

print("Vado in deep sleep, premi il pulsante su GPIO4 per svegliarmi")
machine.deepsleep()