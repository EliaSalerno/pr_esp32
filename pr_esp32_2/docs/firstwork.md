# Guida introduttiva: MicroPython su ESP32

Guida passo-passo per configurare l'ambiente di sviluppo e iniziare a programmare una scheda ESP32 con MicroPython. Pensata per lezioni scolastiche, su sistema operativo Windows con Anaconda.

---

## 1. Cos'è MicroPython

MicroPython è un'implementazione di Python 3 ottimizzata per girare su microcontrollori con poca memoria e potenza di calcolo limitata, come l'ESP32. Permette di scrivere codice Python "vero" per controllare pin, sensori, motori, display e connettersi al WiFi, senza dover imparare C/C++.

**Cosa serve prima di iniziare:**
- Una scheda ESP32 (qualsiasi variante: ESP32, ESP32-S3, ESP32-C3...)
- Un cavo USB dati (non solo di ricarica!)
- Un PC con Anaconda/Miniconda installato
- Connessione internet per scaricare firmware e pacchetti

---

## 2. Preparare l'ambiente su Anaconda Prompt

Creiamo un ambiente Python dedicato, per non mescolare pacchetti con altri progetti.

```bash
conda create -n esp32 python=3.11
conda activate esp32
```

Installiamo gli strumenti necessari **via pip** (più affidabile rispetto ai canali conda per questi pacchetti):

```bash
python -m pip install esptool mpremote
```

- **esptool**: serve per scrivere (flashare) il firmware MicroPython sulla scheda
- **mpremote**: strumento ufficiale per comunicare con la scheda, trasferire file ed eseguire script

Verifica che l'installazione sia andata a buon fine:

```bash
esptool version
mpremote --help
```

> ⚠️ **Nota per la classe**: se conda restituisce errori `HTTP 403 Forbidden`, è dovuto a restrizioni recenti sui canali Anaconda a pagamento. La soluzione è usare `pip install` invece di `conda install`, come mostrato sopra.

---

## 3. Trovare la porta seriale della scheda

1. Collega l'ESP32 al PC via USB
2. Apri **Gestione dispositivi** di Windows
3. Cerca sotto **Porte (COM e LPT)** una voce tipo `Silicon Labs CP210x` o `CH340` seguita da un numero di porta, es. `COM3`

Questa porta (`COM3`, `COM4`, ecc.) andrà usata in tutti i comandi successivi — sostituiscila con quella reale della vostra scheda.

---

## 4. Scaricare e installare il firmware MicroPython

1. Vai su [micropython.org/download](https://micropython.org/download)
2. Scegli la scheda corretta (es. "ESP32" generico, oppure la variante specifica S3/C3 se in uso)
3. Scarica il file `.bin` più recente

Cancella la memoria flash della scheda e carica il firmware:

```bash
esptool --port COM3 erase_flash
esptool --port COM3 --baud 460800 write_flash -z 0x1000 firmware.bin
```

Al termine, l'output dovrebbe confermare `Hash of data verified`. Se il flash fallisce con un cavo USB scadente, riprova con `--baud 115200` (più lento ma più stabile).

---

## 5. Primo collegamento alla scheda

Collegati alla REPL (il terminale interattivo di MicroPython):

```bash
mpremote connect COM3
```

Dovresti vedere un banner tipo:

```
MicroPython v1.2x on ... ; ESP32 module
Type "help()" for more information.
>>>
```

Da qui puoi scrivere comandi Python interattivamente. Per uscire, premi **Ctrl+]** oppure chiudi il terminale.

**Comandi utili nella REPL:**
- **Ctrl+C**: interrompe uno script in esecuzione
- **Ctrl+D**: fa un soft reset della scheda

> ⚠️ **Regola importante**: solo un programma alla volta può usare la porta seriale. Se hai VS Code, Thonny o un altro terminale aperto sulla stessa porta, `mpremote` non riuscirà a connettersi e darà errori come `could not enter raw repl`. Chiudi sempre le altre connessioni prima.

---

## 6. Scrivere ed eseguire uno script

Invece di digitare codice direttamente nella REPL (rischioso: copia-incolla di più righe può causare errori di indentazione o crash), è più affidabile scrivere il codice in un file sul PC e poi trasferirlo.

**Esempio — `blink.py`** (fa lampeggiare il LED integrato, se presente sul pin 2):

```python
from machine import Pin
import time

led = Pin(2, Pin.OUT)

while True:
    led.value(not led.value())
    time.sleep(0.5)
```

**Trasferisci il file sulla scheda:**

```bash
mpremote connect COM3 fs cp blink.py :blink.py
```

**Eseguilo:**

```bash
mpremote connect COM3 run blink.py
```

---

## 7. Configurare il WiFi

Script pronto per connettere l'ESP32 a una rete WiFi (**deve essere una rete a 2.4GHz** — l'ESP32 non supporta il 5GHz).

**`wifi_config.py`:**

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
    time.sleep(1)  # dà tempo all'interfaccia di stabilizzarsi

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
    SSID = "NOME_RETE"
    PASSWORD = "PASSWORD_RETE"
    connect_wifi(SSID, PASSWORD)
```

Copia ed esegui:

```bash
mpremote connect COM3 fs cp wifi_config.py :wifi_config.py
mpremote connect COM3 run wifi_config.py
```

**Se compare l'errore `OSError: Wifi Internal State Error`:**
- Fai un reset fisico della scheda (pulsante EN/RST) e riprova
- Verifica che i due `time.sleep(1)` siano presenti nello script (danno tempo allo stack WiFi di stabilizzarsi)

**Rendere la connessione automatica all'avvio:**
Se rinomini il file in `boot.py`, MicroPython lo eseguirà automaticamente ogni volta che la scheda si accende:

```bash
mpremote connect COM3 fs cp wifi_config.py :boot.py
```

> 🔒 **Nota didattica**: evitate di scrivere password reali negli esempi mostrati in classe o condivisi online.

---

## 8. Un piccolo web server con Microdot

Flask **non funziona** su MicroPython (richiede CPython completo). L'alternativa leggera è **Microdot**, con una sintassi molto simile.

**Installazione manuale (consigliata, non richiede WiFi durante l'installazione):**

```bash
pip download microdot --no-deps -d .
```

oppure clonando il repository:

```bash
git clone https://github.com/miguelgrinberg/microdot.git
```

Copia il file `microdot.py` (dentro `src/microdot/`) sulla scheda:

```bash
mpremote connect COM3 fs cp microdot.py :microdot.py
```

**Esempio minimo — `web_server.py`:**

```python
from microdot import Microdot
import wifi_config  # riusa lo script di connessione già scritto

wifi_config.connect_wifi("NOME_RETE", "PASSWORD_RETE")

app = Microdot()

@app.route('/')
def index(request):
    return 'Ciao dalla ESP32!'

app.run(port=80)
```

Dopo l'esecuzione, lo script stampa l'indirizzo IP assegnato alla scheda (visibile nell'output di `wlan.ifconfig()`): apri quell'indirizzo dal browser di un dispositivo collegato alla stessa rete WiFi.

---

## 9. Comandi mpremote più usati — riepilogo

| Comando | Cosa fa |
|---|---|
| `mpremote connect COM3` | Apre la REPL interattiva |
| `mpremote connect COM3 fs cp file.py :file.py` | Copia un file dal PC alla scheda |
| `mpremote connect COM3 fs ls` | Elenca i file presenti sulla scheda |
| `mpremote connect COM3 run file.py` | Esegue uno script senza salvarlo permanentemente |
| `mpremote connect COM3 exec "import file"` | Esegue un file già presente sulla scheda |
| `mpremote connect COM3 fs rm file.py` | Elimina un file dalla scheda |

---

## 10. Problemi comuni e soluzioni rapide

| Problema | Causa probabile | Soluzione |
|---|---|---|
| `CondaHTTPError 403` | Restrizioni sui canali Anaconda a pagamento | Usa `pip install` invece di `conda install` |
| `could not enter raw repl` | Porta seriale occupata da un altro programma | Chiudi VS Code/Thonny/altri terminali sulla stessa porta |
| `OSError: Wifi Internal State Error` | Stack WiFi non stabilizzato | Aggiungi `time.sleep(1)` dopo `wlan.active(True)`, fai reset fisico |
| La scheda non risponde / solo simboli strani | Firmware non flashato correttamente | Riflasha con `esptool erase_flash` poi `write_flash` |
| `mip install` fallisce per un pacchetto | Il pacchetto non è nell'indice ufficiale o manca il WiFi | Installa manualmente il file `.py` con `mpremote fs cp` |

---

## Risorse utili

- Documentazione ufficiale MicroPython: https://docs.micropython.org
- Download firmware: https://micropython.org/download
- Repository Microdot: https://github.com/miguelgrinberg/microdot
