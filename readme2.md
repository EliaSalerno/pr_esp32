# readme2 — Argomenti trattati nel repository `pr_esp32`

Questo documento dettaglia tutti gli argomenti tecnici e didattici trattati nel repository, che raccoglie materiale di riferimento per lo sviluppo **IoT su ESP32 con MicroPython**. Il progetto è pensato per un contesto scolastico (lezioni su sistema operativo Windows con Anaconda/Miniconda).

---

## 1. Panoramica del repository

Il repository è organizzato in cartelle per fasi di apprendimento progressive:

| Cartella | Contenuto | Argomento principale |
|----------|-----------|----------------------|
| `intro/` | `ESP32_Specifiche_tecniche_e_periferiche_con_micropython.md`, `ESP32_MicroPython_IoT_Essentials.pdf` | Teoria hardware e specifiche tecniche ESP32 |
| `configure/` | `configure.md`, `wifi-connessione-manuale.md`, `wifi-connessione-automatica.md` | Configurazione ambiente di sviluppo e WiFi |
| `step1/` | `general_board_control.md`, `wifi_config.py` | Controllo della scheda e configurazione di rete |
| `step2/` | `blink.py` | Primo programma: lampeggio del LED |
| `step3/` | `web_server.py`, `microdot/` | Web server con Microdot |
| `img/` | screenshot e guide visive | Supporto visuale (driver, Thonny, Miniconda, protocolli) |

Le guide principali trasversali sono:
- `README.md` — introduzione riassuntiva del progetto
- `firstwork.md` — guida passo-passo completa per iniziare con MicroPython su ESP32

---

## 2. Introduzione teorica (cartella `intro/`)

### 2.1 Perché ESP32 con MicroPython

L'ESP32 è descritto come lo **standard de facto per l'IoT industriale**. L'uso di MicroPython è una scelta strategica: l'astrazione di alto livello mitiga la complessità dello sviluppo bare-metal, pur mantenendo un controllo granulare sulle risorse hardware grazie ai moduli `machine` ed `esp`.

### 2.2 Specifiche tecniche hardware

Guida approfondita (`ESP32_Specifiche_tecniche_e_periferiche_con_micropython.md`) che copre:

**1. Architettura centrale e gestione del calcolo**
- **Dual-core a 240 MHz**, frequenza gestibile via `machine.freq()`
- Ottimizzazione: `esp.osdebug(None)` per silenziare i log di sistema
- Gestione della **flash** (`esp.flash_read/write/erase`) e longevità del dispositivo: attenzione al wear leveling (tipicamente ~100.000 cicli di scrittura)

**2. Comunicazione seriale UART**
- 3 controller UART hardware
- **GPIO matrix**: mappaggio flessibile dei segnali TX/RX
- Tabella dei pin predefiniti (UART0 → REPL, UART1 → conflitto flash SPI, UART2 → uso generale)

**3. Segnali analogici e PWM**
- **16 canali PWM** fino a 40 MHz (con tradeoff risoluzione/duty cycle)
- **ADC dual-block**: ADC2 condiviso con il modulo WiFi
- **DAC** 8-bit su pin 25/26

**4. Infrastruttura bus I2C e SPI**
- 2 controller I2C e 2 controller SPI per sensori e periferiche ad alta frequenza

**5. Gestione dell'energia e persistenza degli stati**
- **Deep-Sleep** avanzato
- Risveglio tramite **RTC** e **Pad Hold**
- Distinzione tra pin RTC (pull-up/down nativi) e pin standard (richiedono `hold=True` e `esp32.gpio_deep_sleep_hold(True)`)
- Efficienza energetica: disabilitare i pull-up non necessari prima dello sleep

**6. Tabella di riferimento pin**

| Periferica | Pin | Note |
|------------|-----|------|
| GPIO utilizzabili | 0–19, 21–23, 25–27, 32–39 | Range totale |
| Pin solo input | 34–39 | Privi di pull-up/down interni |
| Pin critici (Flash) | 6–11, 16, 17 | Da evitare, legati alla SPI interna |
| ADC Block 1 | 32–39 | Utilizzabile con WiFi attivo |
| ADC Block 2 | 0, 2, 4, 12–15, 25–27 | Conflitto con WiFi |
| DAC | 25, 26 | Output analogico 8-bit |

### 2.3 Materiale PDF

- `ESP32_MicroPython_IoT_Essentials.pdf` — approfondimento sulle essenzialità di MicroPython per applicazioni IoT.

---

## 3. Configurazione dell'ambiente (cartella `configure/`)

### 3.1 Installazione dei driver (`configure.md`)

Procedura in fasi per preparare la scheda ESP32:

**FASE 1 — Driver USB**
- Verifica via **Gestione dispositivi** che il driver sia installato correttamente
- Riconoscimento del chip (es. **Silicon Labs CP210x USB to UART Bridge** su una porta COM)
- Conferma dell'installazione tramite **Arduino IDE**, **Putty** o **Thonny**
- Avvertenza: un cavo sbagliato (solo ricarica, non dati) impedisce il riconoscimento della scheda

**FASE 2 — Firmware MicroPython**
- Installazione di **Miniconda/Anaconda**
- Creazione di un ambiente virtuale dedicato (`conda create`)
- Installazione di `esptool` (via conda-forge o preferibilmente via pip)
- Cancellazione della flash ed **erasing** + **write_flash** del firmware MicroPython scaricato da micropython.org

**FASE 3 — Limitazioni della REPL e script `wifi_config.py`**
- Perché scrivere codice in un file `.py` invece di incollarlo nella REPL (problemi di indentazione, caratteri sporchi, chiusure inattese della connessione)
- Copia ed esecuzione del file sulla scheda con `mpremote`

### 3.2 Connessione WiFi manuale (`wifi-connessione-manuale.md`)

Collegamento "a comando", senza connessione automatica all'avvio:

- Requisito: `wifi_config.py` presente sulla scheda
- **Metodo 1 (consigliato)**: comando singolo `mpremote connect COMx exec "import wifi_config; wifi_config.connect_wifi(...)"`
- **Metodo 2**: dalla REPL interattiva
- Verifica dello stato (`isconnected()`, `ifconfig()`)
- Nota sugli import ripetuti nella stessa sessione (cache dei moduli Python)
- Tabella di risoluzione problemi (`could not read file`, `OSError: Wifi Internal State Error`, `could not enter raw repl`, IP a `0.0.0.0`)

### 3.3 Connessione WiFi automatica (`wifi-connessione-automatica.md`)

Connessione automatica ad ogni accensione/reset tramite **`boot.py`**:

- Comportamento di avvio MicroPython: `boot.py` (configurazione di basso livello) → `main.py` (applicazione)
- **Differenza chiave**: in `boot.py` non serve il blocco `if __name__ == "__main__":`, le credenziali e la chiamata a `connect_wifi(...)` vengono eseguiti linearmente
- Copia del file come `:boot.py` sulla scheda
- Verifica con reset fisico (pulsante EN/RST) e output atteso
- Controllo dell'IP senza rientrare in REPL (`exec`)
- Backup ed eliminazione di un `boot.py` esistente
- Combinazione con un `main.py` applicativo separato
- Tabella problemi comuni (nome file non `boot.py`, stack WiFi non stabilizzato, REPL "intrappolata" dal boot)

---

## 4. Step 1 — Controllo della scheda e WiFi (cartella `step1/`)

- `general_board_control.md` — file **placeholder attualmente vuoto** (argomento previsto: controllo generale della board)
- `wifi_config.py` — script di connessione WiFi riutilizzabile:

```python
import network
import time

def connect_wifi(ssid, password, timeout=15):
    wlan = network.WLAN(network.STA_IF)

    if wlan.isconnected():
        print("Già connesso:", wlan.ifconfig())
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
    SSID = "..."
    PASSWORD = "..."
    connect_wifi(SSID, PASSWORD)
```

Punti didattici chiave:
- Rete obbligatoriamente **a 2.4 GHz** (l'ESP32 non supporta il 5 GHz)
- I due `time.sleep(1)` dopo `wlan.active()` danno tempo allo stack WiFi di stabilizzarsi
- Il blocco `if __name__ == "__main__":` evita la connessione quando il file viene importato

---

## 5. Step 2 — Primo programma: LED blink (cartella `step2/`)

`blink.py` — il classico "Hello World" dell'hardware: fa lampeggiare il LED integrato sul **pin 2** usando il modulo `machine.Pin` e `time`:

```python
from machine import Pin
import time

led = Pin(2, Pin.OUT)

while True:
    led.value(not led.value())
    time.sleep(0.5)
```

Concetti introdotti:
- Configurazione di un GPIO come `Pin.OUT`
- Ciclo infinito con toggle dello stato (`led.value(not led.value())`)
- Timing con `time.sleep()`

---

## 6. Step 3 — Web server con Microdot (cartella `step3/`)

### 6.1 `web_server.py`

Esempio minimale di applicazione web sulla scheda ESP32:

```python
from microdot import Microdot
import wifi_config

wifi_config.connect_wifi("SSID","password")

app = Microdot()

@app.route('/')
def index(request):
    return 'Ciao da esp32!'

app.run(port=80)
```

Concetti:
- **Perché Microdot** e non Flask: Flask non gira su MicroPython (richiede CPython completo); Microdot è l'alternativa leggera con sintassi molto simile
- Creazione di un'app `Microdot()`, definizione di rotte con `@app.route('/')`
- Avvio del server sulla porta 80 dopo la connessione WiFi
- Accesso dal browser tramite l'IP assegnato alla scheda

### 6.2 Installazione di Microdot

Metodi descritti:
- **Manuale (consigliata)**: `pip download microdot --no-deps -d .` oppure `git clone` del repository, poi copia di `microdot.py` sulla scheda con `mpremote fs cp`
- Il repository `microdot/` è incluso in `step3/` come libreria sorgente completa (framework con estensioni: ASGI, WSGI, auth, CORS, CSRF, login, sessione, SSE, WebSocket, multipart, template jinja/utemplate, static, streaming, etc.)

---

## 7. Guida introduttiva completa (`firstwork.md`)

Documento a uso delle lezioni, copre l'intero percorso:

1. **Cos'è MicroPython** e cosa serve (scheda, cavo dati, Anaconda, internet)
2. **Preparazione ambiente** con Anaconda Prompt (`conda create`, `pip install esptool mpremote`) — nota sugli errori `HTTP 403` dei canali Anaconda
3. **Trovare la porta seriale** (Gestione dispositivi: `Silicon Labs CP210x` o `CH340`)
4. **Scaricare e installare il firmware** (`esptool erase_flash`, `write_flash`)
5. **Primo collegamento** alla REPL (`mpremote connect`) e comandi utili (Ctrl+C, Ctrl+D, regola del "solo un programma alla volta sulla porta")
6. **Scrivere ed eseguire uno script** (trasferimento ed esecuzione di `blink.py`)
7. **Configurare il WiFi** (esecuzione di `wifi_config.py`, gestione errori, connessione automatica via `boot.py`)
8. **Piccolo web server con Microdot** (`web_server.py`)
9. **Riepilogo comandi mpremote** (tabella)
10. **Problemi comuni e soluzioni rapide** (tabella)

---

## 8. Riepilogo dei comandi `mpremote`

| Comando | Cosa fa |
|---|---|
| `mpremote connect COMx` | Apre la REPL interattiva |
| `mpremote connect COMx fs cp file.py :file.py` | Copia un file dal PC alla scheda |
| `mpremote connect COMx fs ls` | Elenca i file sulla scheda |
| `mpremote connect COMx fs rm file.py` | Elimina un file dalla scheda |
| `mpremote connect COMx run file.py` | Esegue uno script senza salvarlo in modo permanente |
| `mpremote connect COMx exec "import file"` | Esegue un file già presente sulla scheda |

Comandi `esptool`:
| Comando | Cosa fa |
|---|---|
| `esptool --port COMx erase_flash` | Cancella la memoria flash della scheda |
| `esptool --port COMx --baud 460800 write_flash -z 0x1000 firmware.bin` | Scrive il firmware MicroPython |

---

## 9. Problemi comuni e soluzioni

| Problema | Causa probabile | Soluzione |
|---|---|---|
| `CondaHTTPError 403` | Restrizioni sui canali Anaconda a pagamento | Usa `pip install` invece di `conda install` |
| `could not enter raw repl` | Porta seriale occupata da un altro programma | Chiudi VS Code/Thonny/altri terminali sulla stessa porta |
| `OSError: Wifi Internal State Error` | Stack WiFi non stabilizzato | Aggiungi `time.sleep(1)` dopo `wlan.active(True)`, fai reset fisico |
| La scheda non risponde / simboli strani | Firmware non flashato correttamente | Riflasha con `esptool erase_flash` poi `write_flash` |
| `mip install` fallisce | Pacchetto non nell'indice o manca il WiFi | Installa manualmente il file `.py` con `mpremote fs cp` |
| Scheda non riconosciuta | Cavo errato (solo ricarica) | Usa un cavo USB dati |
| IP a `0.0.0.0` | Connessione fallita o non completata | Rilancia lo script e verifica l'output "Connesso!" |

---

## 10. Nota di sicurezza (importante)

All'interno del repository sono presenti **credenziali WiFi reali** (SSID e password) in chiaro nei file:
- `step1/wifi_config.py`
- `step3/web_server.py`

**Raccomandazione:** queste credenziali non dovrebbero essere versionate/condivise. È buona pratica rimuoverle e sostituirle con placeholder, oppure leggerle da variabili d'ambiente o da file separati esclusi dal controllo di versione (vedi `.gitignore`).

> NOTA: questo documento descrive gli argomenti senza riportare le credenziali effettive.

---

## 11. Risorse utili

- Documentazione ufficiale MicroPython: https://docs.micropython.org
- Download firmware: https://micropython.org/download
- Repository Microdot: https://github.com/miguelgrinberg/microdot
- Download Miniconda: https://www.anaconda.com/download/success
