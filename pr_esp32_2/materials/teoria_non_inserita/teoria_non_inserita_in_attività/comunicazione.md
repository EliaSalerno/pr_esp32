# Guida: Utilizzo del Wi-Fi sull'ESP32 per la trasmissione di pacchetti

Per utilizzare il Wi-Fi dell'ESP32 e trasmettere pacchetti verso altri ESP32 o verso un Raspberry Pi, hai a disposizione diverse modalità a seconda che tu voglia una comunicazione **diretta (senza router)** o **infrastrutturata (tramite una rete Wi-Fi o un Access Point)**.

---

## 1. ESP32 con altri ESP32: Comunicazione Diretta (ESP-NOW)

Se vuoi che due o più ESP32 scambino pacchetti tra loro in modo rapidissimo e **senza bisogno di un router Wi-Fi**, la tecnologia ideale è **ESP-NOW**.

* **Cos'è:** È un protocollo di comunicazione wireless sviluppato da Espressif (i produttori dell'ESP32) che permette una trasmissione dati a bassissima latenza basata sugli indirizzi MAC.
* **Come funziona:** 
  * Non c'è bisogno di fare il "pairing" a una rete Wi-Fi o inserire password.
  * Un ESP32 invia un pacchetto (di dimensioni ridotte, fino a 250 byte) specificando l'indirizzo MAC del destinatario.
  * È ideale per sensori distribuiti, domotica o comandi in tempo reale tra schede.

---

## 2. ESP32 con Raspberry Pi: Reti Wi-Fi e Protocolli Standard

Quando devi far comunicare un ESP32 con un Raspberry Pi, solitamente si sfrutta la rete Wi-Fi di casa/laboratorio (oppure il Raspberry Pi può creare un proprio Hotspot Wi-Fi a cui l'ESP32 si collega). 

Poiché il Raspberry Pi è un vero e proprio computer (spesso con Linux), la comunicazione avviene tramite i normali protocolli di rete TCP/IP. I metodi più usati sono:

### A. Protocollo MQTT (Il più consigliato per l'IoT)
* **Come funziona:** Si basa su un modello **Publish/Subscribe**. 
  * Il Raspberry Pi ospita un **Broker MQTT** (ad esempio il software gratuito *Mosquitto*).
  * L'ESP32 si connette al Wi-Fi e invia ("pubblica") i pacchetti di dati a un determinato "canale" (es. `casa/sensore/temperatura`).
  * Il Raspberry Pi si iscrive a quello stesso canale e riceve i dati in tempo reale.
* **Vantaggi:** Estremamente leggero, consuma poca banda, gestisce la riconnessione automatica ed è perfetto per gestire più ESP32 contemporaneamente.

### B. Socket TCP / UDP (Per pacchetti personalizzati)
* **Come funziona:** Si aprono socket di rete direttamente a livello di programmazione.
  * *UDP:* L'ESP32 spara pacchetti di dati nell'aria verso l'IP del Raspberry Pi (veloce, ma senza certezza di consegna).
  * *TCP:* Viene aperta una connessione affidabile "uno a uno" con scambio dati bidirezionale sicuro (es. l'ESP32 fa da client web o da piccolo server HTTP).

---

## 3. Schema riassuntivo dei contesti d'uso

| Destinatario | Metodo consigliato | Vantaggio principale |
| :--- | :--- | :--- |
| **ESP32 ⇄ ESP32** | **ESP-NOW** | Velocissimo, nessuna rete Wi-Fi richiesta, ideale per peer-to-peer. |
| **ESP32 ⇄ Raspberry Pi** | **MQTT (su Wi-Fi)** | Perfetto per gestire più dispositivi, scalabile e facile da integrare con dashboard sul Raspberry Pi. |
| **ESP32 ⇄ Raspberry Pi** | **Socket TCP/UDP** | Controllo totale e diretto dei pacchetti di basso livello. |
