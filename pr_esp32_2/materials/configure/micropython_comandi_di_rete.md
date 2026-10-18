# ESP32 + MicroPython: comandi di rete con `mpremote`

Guida rapida per leggere il MAC address e gestire/ispezionare la rete di una scheda ESP32 usando `mpremote` (ad esempio dal prompt di Anaconda).

---

## 1. Installazione e connessione

```bash
pip install mpremote
```

Elenco delle porte seriali/schede rilevate:

```bash
mpremote devs
```

Connessione automatica (la prima scheda trovata) o a una porta specifica:

```bash
mpremote                      # apre il REPL sulla prima scheda
mpremote connect COM3         # Windows
mpremote connect /dev/ttyUSB0 # Linux
mpremote connect /dev/cu.usbserial-0001  # macOS
```

> Il comando `connect` può essere concatenato con gli altri: `mpremote connect COM3 exec "..."`.

### Nota sul quoting

- **Windows (Anaconda Prompt / PowerShell / cmd):** virgolette doppie all'esterno, singole all'interno.
- **Linux / macOS:** va bene anche il contrario, ma tieni la stessa convenzione per semplicità.
- Per codice lungo, meglio salvare uno script `.py` ed eseguirlo con `mpremote run script.py`.

---

## 2. MAC address

### MAC dell'interfaccia Wi-Fi station (formato leggibile)

```bash
mpremote exec "import network, ubinascii; print(ubinascii.hexlify(network.WLAN(network.STA_IF).config('mac'), ':').decode())"
```

Output di esempio: `a4:cf:12:34:56:78`

### MAC in formato byte grezzo

```bash
mpremote exec "import network; print(network.WLAN().config('mac'))"
```

Output di esempio: `b'\xa4\xcf\x124Vx'`

### MAC dell'Access Point

```bash
mpremote exec "import network, ubinascii; print(ubinascii.hexlify(network.WLAN(network.AP_IF).config('mac'), ':').decode())"
```

Il MAC dell'AP è diverso da quello della station (di solito l'ultimo byte è incrementato).

### MAC Bluetooth (BLE)

```bash
mpremote exec "import bluetooth; ble = bluetooth.BLE(); ble.active(True); print(ble.config('mac'))"
```

Restituisce una tupla `(tipo_indirizzo, indirizzo_in_bytes)`. Richiede MicroPython recente (1.20+) e firmware con BLE abilitato.

### ID univoco del chip

```bash
mpremote exec "import machine, ubinascii; print(ubinascii.hexlify(machine.unique_id()).decode())"
```

Su ESP32 coincide in genere con il MAC della station (senza i due punti).

---

## 3. Stato dell'interfaccia Wi-Fi

### Attivare l'interfaccia station

```bash
mpremote exec "import network; w = network.WLAN(network.STA_IF); w.active(True); print(w.active())"
```

> Alcune chiamate (come `scan` o `config('mac')` su certi firmware) richiedono l'interfaccia attiva. Se ricevi errori, attivala prima.

### Verificare se è connessa

```bash
mpremote exec "import network; print(network.WLAN(network.STA_IF).isconnected())"
```

### Codice di stato della connessione

```bash
mpremote exec "import network; print(network.WLAN(network.STA_IF).status())"
```

Valori utili: `network.STAT_IDLE`, `STAT_CONNECTING`, `STAT_GOT_IP`, `STAT_WRONG_PASSWORD`, `STAT_NO_AP_FOUND`, `STAT_CONNECT_FAIL`.

### Potenza del segnale (RSSI) della rete a cui sei connesso

```bash
mpremote exec "import network; print(network.WLAN(network.STA_IF).status('rssi'))"
```

Valore in dBm (es. `-55` è ottimo, `-85` è debole). Supportato solo su alcuni port/versioni.

---

## 4. Indirizzo IP, netmask, gateway, DNS

```bash
mpremote exec "import network; print(network.WLAN(network.STA_IF).ifconfig())"
```

Restituisce una tupla: `(ip, netmask, gateway, dns)`

Esempio: `('192.168.1.45', '255.255.255.0', '192.168.1.1', '192.168.1.1')`

### Impostare un IP statico

```bash
mpremote exec "import network; w = network.WLAN(network.STA_IF); w.ifconfig(('192.168.1.50','255.255.255.0','192.168.1.1','8.8.8.8'))"
```

---

## 5. Connessione a una rete Wi-Fi

```bash
mpremote exec "import network, time; w = network.WLAN(network.STA_IF); w.active(True); w.connect('NOME_SSID', 'PASSWORD'); time.sleep(5); print(w.isconnected(), w.ifconfig())"
```

Meglio ancora, con attesa a ciclo (script `connetti.py`):

```python
import network, time

w = network.WLAN(network.STA_IF)
w.active(True)
w.connect("NOME_SSID", "PASSWORD")

t = 0
while not w.isconnected() and t < 15:
    time.sleep(1)
    t += 1

print("Connesso:", w.isconnected())
print("Config:", w.ifconfig())
```

```bash
mpremote run connetti.py
```

### Disconnettersi

```bash
mpremote exec "import network; network.WLAN(network.STA_IF).disconnect()"
```

### Spegnere il Wi-Fi

```bash
mpremote exec "import network; network.WLAN(network.STA_IF).active(False)"
```

---

## 6. Scansione delle reti Wi-Fi

```bash
mpremote exec "import network; w = network.WLAN(network.STA_IF); w.active(True); [print(r) for r in w.scan()]"
```

Ogni risultato è una tupla:

```
(ssid, bssid, canale, rssi, authmode, hidden)
```

Versione più leggibile:

```bash
mpremote exec "import network, ubinascii; w = network.WLAN(network.STA_IF); w.active(True); [print(r[0].decode(), '|', ubinascii.hexlify(r[1], ':').decode(), '| ch', r[2], '|', r[3], 'dBm') for r in w.scan()]"
```

Valori di `authmode`: `0` open, `1` WEP, `2` WPA-PSK, `3` WPA2-PSK, `4` WPA/WPA2-PSK.

---

## 7. Hostname

Leggere (versioni recenti di MicroPython):

```bash
mpremote exec "import network; print(network.hostname())"
```

Impostare:

```bash
mpremote exec "import network; network.hostname('esp32-lab')"
```

> L'hostname va impostato **prima** di connettersi alla rete. Su versioni più vecchie si usa `w.config(dhcp_hostname='esp32-lab')`.

---

## 8. Modalità Access Point

Creare un AP:

```bash
mpremote exec "import network; ap = network.WLAN(network.AP_IF); ap.active(True); ap.config(essid='ESP32-AP', password='12345678', authmode=network.AUTH_WPA2_PSK); print(ap.ifconfig())"
```

Il tipico IP dell'AP è `192.168.4.1`.

Vedere la configurazione dell'AP:

```bash
mpremote exec "import network; ap = network.WLAN(network.AP_IF); print(ap.config('essid'), ap.config('channel'), ap.ifconfig())"
```

Elencare i client connessi all'AP:

```bash
mpremote exec "import network; print(network.WLAN(network.AP_IF).status('stations'))"
```

Spegnere l'AP:

```bash
mpremote exec "import network; network.WLAN(network.AP_IF).active(False)"
```

---

## 9. Test di rete

MicroPython **non ha un comando `ping`** integrato. Ecco le alternative.

### Risoluzione DNS

```bash
mpremote exec "import socket; print(socket.getaddrinfo('google.com', 80)[0][-1])"
```

### Test di connessione TCP

```bash
mpremote exec "import socket; s = socket.socket(); s.settimeout(5); s.connect(('example.com', 80)); print('OK'); s.close()"
```

### Richiesta HTTP

Prima installa la libreria `requests` (una sola volta, serve rete sulla scheda):

```bash
mpremote mip install requests
```

Poi:

```bash
mpremote exec "import requests; r = requests.get('http://example.com'); print(r.status_code); r.close()"
```

### Sincronizzare l'ora via NTP

```bash
mpremote exec "import ntptime; ntptime.settime(); import time; print(time.localtime())"
```

L'ora è in UTC. Richiede la scheda connessa a Internet.

---

## 10. Altre opzioni di rete

### Potenza di trasmissione

```bash
mpremote exec "import network; w = network.WLAN(network.STA_IF); w.active(True); print(w.config('txpower'))"
```

### Risparmio energetico Wi-Fi

```bash
mpremote exec "import network; w = network.WLAN(network.STA_IF); w.active(True); w.config(pm=network.WLAN.PM_NONE)"
```

Valori: `PM_NONE`, `PM_PERFORMANCE`, `PM_POWERSAVE`. Con `PM_NONE` la latenza è minore ma il consumo aumenta.

---

## 11. Comandi `mpremote` utili in generale

| Comando | Descrizione |
|---|---|
| `mpremote devs` | Elenca le porte seriali disponibili |
| `mpremote connect <porta>` | Si connette a una porta specifica |
| `mpremote` | Apre il REPL interattivo (esci con `Ctrl+]`) |
| `mpremote exec "<codice>"` | Esegue una riga di codice Python sulla scheda |
| `mpremote run script.py` | Esegue un file locale sulla scheda senza copiarlo |
| `mpremote fs ls` | Elenca i file sulla scheda |
| `mpremote fs cp file.py :` | Copia un file dal PC alla scheda |
| `mpremote fs cp :file.py .` | Copia un file dalla scheda al PC |
| `mpremote fs rm :file.py` | Cancella un file sulla scheda |
| `mpremote mip install <pacchetto>` | Installa un pacchetto sulla scheda |
| `mpremote reset` | Reset software della scheda |
| `mpremote soft-reset` | Soft reset dell'interprete |

Si possono concatenare più comandi con `+`:

```bash
mpremote connect COM3 fs cp main.py : + reset
```

---

## 12. Risoluzione dei problemi

- **`could not open port` / porta occupata:** chiudi Thonny, Arduino IDE, PuTTY o qualsiasi altro programma che usa la seriale.
- **Scheda non rilevata:** controlla il cavo USB (deve essere dati, non solo ricarica) e il driver CP210x/CH340.
- **`OSError: Wifi Internal Error`:** spesso l'interfaccia non è attiva, usa `w.active(True)`.
- **Il comando non restituisce nulla:** `exec` mostra solo ciò che viene stampato con `print()`.
- **Errori di quoting su Windows:** passa a uno script `.py` ed eseguilo con `mpremote run`.
