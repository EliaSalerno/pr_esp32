# ESP32: forzare la connessione WiFi manualmente

Guida per collegare l'ESP32 al WiFi "a comando", senza che si connetta automaticamente all'avvio. Utile in fase di test o quando si vuole controllare esattamente quando la scheda si collega alla rete.

---

## Prerequisito

Il file `wifi_config.py` deve essere già presente sulla scheda. Verifica con:

```bash
mpremote connect COM5 fs ls
```

Se non compare nell'elenco, copialo prima:
```bash
mpremote connect COM5 fs cp wifi_config.py :wifi_config.py
```

---

## Contenuto di riferimento — `wifi_config.py`

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
```

> ⚠️ Con questo script salvato come `wifi_config.py` (**non** `boot.py` o `main.py`), la scheda **non** si connette da sola all'avvio: il blocco `if __name__ == "__main__":` scatta solo quando il file è eseguito come script principale, non quando viene importato.

---

## Metodo 1 — comando singolo da terminale (consigliato)

Il modo più rapido: import del modulo + chiamata esplicita della funzione, tutto in un comando.

```bash
mpremote connect COM5 exec "import wifi_config; wifi_config.connect_wifi('NOME_RETE', 'PASSWORD_RETE')"
```

Sostituisci `NOME_RETE` e `PASSWORD_RETE` con le credenziali reali. Vedrai l'output in tempo reale: i puntini di attesa, poi "Connesso!" con l'indirizzo IP assegnato.

---

## Metodo 2 — dalla REPL interattiva

Utile se vuoi eseguire più comandi in sequenza o controllare lo stato passo per passo.

**1. Entra nella REPL:**
```bash
mpremote connect COM5
```

**2. Digita (o incolla, con attenzione all'indentazione):**
```python
import wifi_config
wifi_config.connect_wifi('NOME_RETE', 'PASSWORD_RETE')
```

**3. Per uscire dalla REPL:** Ctrl+]

---

## Verificare lo stato della connessione in qualsiasi momento

```bash
mpremote connect COM5 exec "import network; wlan = network.WLAN(network.STA_IF); print('Connesso:', wlan.isconnected()); print('IP:', wlan.ifconfig())"
```

Se l'IP restituito è tutto a zero (`0.0.0.0`), la scheda non è connessa in quel momento.

---

## Nota importante: import ripetuti nella stessa sessione

Se hai già fatto `import wifi_config` in precedenza nella stessa sessione REPL (senza uscire), un secondo `import wifi_config` **non ri-esegue** il modulo (Python lo tiene in cache). Per rilanciare la connessione in quel caso, richiama direttamente la funzione senza reimportare:

```python
wifi_config.connect_wifi('NOME_RETE', 'PASSWORD_RETE')
```

oppure chiudi e riapri la connessione mpremote per ripartire da zero.

---

## Problemi comuni

| Errore | Causa | Soluzione |
|---|---|---|
| `mpremote: could not read file` | Stai usando `run` invece di `exec`, o il file non è sul PC nella cartella corrente | Usa `exec "import wifi_config; ..."` per eseguire il file già presente sulla scheda |
| `OSError: Wifi Internal State Error` | Stack WiFi non stabilizzato | Reset fisico della scheda (pulsante EN/RST), poi riprova |
| `could not enter raw repl` | Porta seriale occupata da un altro programma | Chiudi VS Code/Thonny/altri terminali sulla stessa porta seriale |
| IP a `0.0.0.0` dopo la connessione | Connessione fallita o non ancora completata | Rilancia lo script e controlla se compare "Connesso!" nell'output |
