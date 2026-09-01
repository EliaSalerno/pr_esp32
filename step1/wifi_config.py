# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

import network
import time

def connect_wifi(ssid, password, timeout=15):
    wlan = network.WLAN(network.STA_IF)
    
    if wlan.isconnected():
        print("Era connesso:", wlan.ifconfig())
        return wlan

    wlan.active(False)
    time.sleep(1)
    wlan.active(True)
    time.sleep(1)
    
    print(f"Connessione a {ssid}...")
    wlan.connect(ssid, password)
    
    start = time.time()
    while not wlan.isconnected():
        if time.time() - start > timeout:
            print("Timeout: connessione fallita")
            return wlan
        time.sleep(0.5)
        print(".", end="")
    
    print("\nConnesso!")
    print("Config di rete:", wlan.ifconfig())
    return wlan

if __name__ == "__main__":
    SSID = "TP-Link_4CF8"
    PASSWORD = "74610693"
    connect_wifi(SSID, PASSWORD)