# ESP32: connessione WiFi automatica al riavvio

Guida per far sì che l'ESP32 si connetta da solo alla rete WiFi ogni volta che si accende o viene resettato, senza bisogno di lanciare comandi manualmente.

---

## Come funziona l'avvio automatico su MicroPython

Ad ogni accensione o reset, MicroPython esegue automaticamente, in ordine:
1. **`boot.py`** — pensato per configurazioni di basso livello (WiFi, impostazioni hardware)
2. **`main.py`** — pensato per il programma applicativo vero e proprio

Per la connessione WiFi automatica, il file va salvato come **`boot.py`**.

---

## 1. Contenuto dello script

Usa lo stesso script di connessione già testato, con le credenziali già inserite direttamente nel file (dato che nessuno lo lancerà a mano):

**`wifi_config.py`** (da rinominare in `boot.py` in fase di copia):

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

# Esecuzione automatica all'avvio (nessun blocco if __name__)
SSID = "NOME_RETE"
PASSWORD = "PASSWORD_RETE"
connect_wifi(SSID, PASSWORD)
```

> ⚠️ Differenza importante rispetto alla versione "manuale": qui **non c'è** il blocco `if __name__ == "__main__":`. In `boot.py` non serve, perché tutto il file viene eseguito linearmente all'avvio — comprese le ultime due righe che chiamano `connect_wifi(...)` direttamente.

---

## 2. Copiare il file come `boot.py` sulla scheda

```bash
mpremote connect COM5 fs cp wifi_config.py :boot.py
```

Nota il nome di destinazione `:boot.py` — anche se sul PC il file si chiama `wifi_config.py`, sulla scheda deve chiamarsi esattamente `boot.py` per essere eseguito automaticamente.

---

## 3. Verifica che funzioni

Fai un reset fisico della scheda (pulsante **EN/RST**), poi collegati subito alla REPL per vedere l'output del boot:

```bash
mpremote connect COM5
```

Dovresti vedere apparire automaticamente:
```
Connessione a NOME_RETE...
....
Connesso!
Config di rete: ('192.168.1.xx', '255.255.255.0', '192.168.1.1', '192.168.1.1')
```

---

## 4. Verificare l'IP in qualsiasi momento, senza rientrare in REPL

```bash
mpremote connect COM5 exec "import network; print(network.WLAN(network.STA_IF).ifconfig())"
```

---

## 5. Attenzione: `boot.py` esiste già?

Se sulla scheda è già presente un file `boot.py` (ad esempio quello di default del firmware), il comando `fs cp` lo **sovrascrive senza avviso**. Se vuoi conservarne una copia prima di sovrascrivere:

```bash
mpremote connect COM5 fs cp :boot.py boot_backup.py
```

(questo copia il `boot.py` esistente sulla scheda in un file locale sul PC, come backup)

---

## 6. Disattivare la connessione automatica

Se in futuro vuoi tornare alla modalità manuale (niente connessione all'avvio), basta eliminare o rinominare `boot.py` sulla scheda:

```bash
mpremote connect COM5 fs rm :boot.py
```

---

## 7. Combinare con un programma applicativo (`main.py`)

Una volta che il WiFi si connette automaticamente via `boot.py`, puoi aggiungere un `main.py` separato con la logica dell'applicazione (es. un web server), che partirà subito dopo:

```bash
mpremote connect COM5 fs cp web_server.py :main.py
```

In questo modo `boot.py` gestisce solo la connessione di rete, e `main.py` il comportamento dell'applicazione — mantenendo il codice più organizzato.

---

## Problemi comuni

| Problema | Causa | Soluzione |
|---|---|---|
| La scheda non si connette all'avvio | Il file non si chiama esattamente `boot.py` sulla scheda | Verifica con `mpremote connect COM5 fs ls` |
| `OSError: Wifi Internal State Error` all'avvio | Stack WiFi non ancora stabilizzato | Verifica che i due `time.sleep(1)` siano presenti nello script |
| Non riesci più a bloccare lo script per modificarlo | `boot.py` riparte ad ogni reset, "intrappolando" la REPL | Premi Ctrl+C rapidamente non appena vedi il banner MicroPython, oppure tieni premuto **BOOT** durante il reset per saltare l'esecuzione |
| La scheda si connette ma poi non fa nulla | Manca un `main.py` con la logica applicativa | `boot.py` gestisce solo la rete: aggiungi un `main.py` separato per il resto del programma |
