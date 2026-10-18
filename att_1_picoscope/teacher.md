# Guida Docente: Analisi della Trasmissione Seriale con ESP32 e Picoscope

## 1. Ripasso Teorico: La Trasmissione Seriale (UART)

La comunicazione **UART (Universal Asynchronous Receiver-Transmitter)** è un protocollo asincrono, il che significa che non c'è un cavo di clock condiviso: mittente e destinatario devono preventivamente concordare la velocità di trasmissione, detta **Baud Rate** (es. 9600 bit/s).

Il pacchetto dati standard (8-N-1) per un singolo carattere è composto da:
1. **Bit di Start:** Un livello logico basso (`0` / 0V) che segnala l'inizio della trasmissione.
2. **Data Bits (Payload):** Solitamente 8 bit, trasmessi partendo dal **meno significativo** (**LSB first**).
3. **Bit di Stop:** Uno o più livelli logici alti (`1` / 3.3V) che chiudono il pacchetto.

Se consideriamo la lettera **"a"** minuscola, il suo valore ASCII in decimale è `97`, che in binario si scrive **`01100001`**. Poiché si trasmette prima l'LSB, la sequenza fisica effettiva dei bit dati sul filo sarà:
$$\text{Start (0)} \rightarrow \mathbf{1 \rightarrow 0 \rightarrow 0 \rightarrow 0 \rightarrow 0 \rightarrow 1 \rightarrow 1 \rightarrow 0} \rightarrow \text{Stop (1)}$$

---

## 2. Teoria sull'ESP32 per l'Attività

Per comprendere e realizzare questa esperienza con l'ESP32, è necessario conoscere tre concetti chiave:
* **Logica a 3.3V:** I pin dell'ESP32 operano tra 0V e 3.3V. Sono perfettamente compatibili con le sonde di un Picoscope, ma bisogna evitare tensioni a 5V per non danneggiare i pin.
* **Matrice dei pin (GPIO Matrix):** L'ESP32 possiede interfacce UART hardware che non sono vincolate a pin fissi, ma possono essere mappate via software su quasi tutti i pin digitali GPIO (es. TX su GPIO 17 e RX su GPIO 16).
* **MicroPython:** Permette di interagire con l'hardware in modo immediato tramite REPL o script leggeri, sfruttando la classe `machine.UART`.

---

## 3. Descrizione dell'Attività di Laboratorio

### Obiettivo
Osservare i livelli fisici di tensione di un carattere trasmesso via seriale da un ESP32 tramite un oscilloscopio (Picoscope), calcolare i tempi di bit (durata di un singolo impulso) in base al Baud Rate, e replicare la ricezione dei dati collegando due ESP32 tra loro.

### Materiale Utile
* N. 2 Schede di sviluppo ESP32.
* N. 1 Picoscope (o oscilloscopio digitale) con sonda 1X/10X.
* Cavi Dupont per i collegamenti.
* PC con Thonny IDE (o ambiente MicroPython installato).

---

### Fase 1: Trasmissione continua e analisi con Picoscope

In questa fase configuriamo un ESP32 affinché invii ripetutamente la lettera *"a"* a un Baud Rate noto (es. 9600 baud).

#### Rappresentazione Hardware (Fase 1)
```text
+-------------------+                      +-------------------------+
|                   |--- (TX: GPIO 17) --->| Sonda Picoscope (Ch A)  |
|      ESP32        |                      +-------------------------+
|   (Trasmettitore) |--- (GND) ----------->| GND Picoscope           |
+-------------------+                      +-------------------------+

```

#### Codice MicroPython (ESP32 - Trasmettitore)

```python
import time
from machine import UART, Pin

# Inizializzazione della UART 1 impostando i pin TX (es. GPIO 17) e RX (es. GPIO 16)
# Baud rate impostato a 9600
uart = UART(1, baudrate=9600, tx=Pin(17), rx=Pin(16))

print("Trasmissione avviata...")

while True:
    uart.write("a")  # Invia il carattere 'a' continuamente
    time.sleep_ms(
        500
    )  # Pausa di mezzo secondo tra un invio e l'altro per stabilizzare l'oscilloscopio

```

#### Analisi dei tempi sul Picoscope

Impostando la base dei tempi del Picoscope (es. a $100\,\mu\text{s}/\text{div}$), i ragazzi noteranno che:

1. Con un Baud Rate di $9600\,\text{baud}$, la durata di un singolo bit ($T_{\text{bit}}$) è pari a:

$$T_{\text{bit}} = \frac{1}{\text{Baud Rate}} = \frac{1}{9600} \approx 104.17\,\mu\text{s}$$


2. Osservando il treno d'impulsi della lettera *"a"* (`01100001` LSB first), gli studenti misureranno graficamente sul display del Picoscope la corrispondenza temporale dei singoli bit e verificheranno sperimentalmente la teoria.

---

### Fase 2: Comunicazione tra due ESP32 usando i tempi ricavati

Una volta compresi i tempi e la struttura del pacchetto, passiamo alla comunicazione diretta tra microcontrollori. Colleghiamo il pin TX del primo ESP32 al pin RX del secondo ESP32.

#### Rappresentazione Hardware (Fase 2)

```text
+-------------------+                               +-------------------+
|      ESP32 A      |                               |      ESP32 B      |
|   (Trasmittente)  |                               |    (Ricevente)    |
|                   |                               |                   |
|           TX (17) |------------------------------>| RX (16)           |
|              GND  |--------------------------------| GND              |
+-------------------+                               +-------------------+

```

#### Codice MicroPython (ESP32 B - Ricevitore)

Il secondo ESP32 rimarrà in ascolto sulla stessa porta UART, leggendo il byte in arrivo e stampandolo sulla console (REPL).

```python
import time
from machine import UART, Pin

# Configurazione UART speculare sul secondo ESP32
uart_rx = UART(1, baudrate=9600, tx=Pin(17), rx=Pin(16))

print("In attesa di dati dal primo ESP32...")

while True:
    # Controlla se ci sono dati nel buffer di ricezione
    if uart_rx.any():
        dato = uart_rx.read(1)  # Legge 1 byte
        print(f"Ricevuto in formato byte: {dato}")

        # Decodifica il byte in carattere stringa
        carattere = dato.decode("utf-8")
        print(f"Carattere decodificato: {carattere}")

    time.sleep_ms(10)

```

---

### Spunto di verifica per il docente:

*Se aumentassimo il Baud Rate a 115200, come cambierebbe visivamente la forma d'onda sul Picoscope rispetto a quella osservata a 9600 baud?*