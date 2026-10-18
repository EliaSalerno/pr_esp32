# Dispensa Teorica: Comunicazione Wireless con ESP32 e Raspberry Pi

## 1. Introduzione alle Reti Wireless nei Microcontrollori
A differenza della comunicazione seriale cablata ( UART), le reti wireless permettono lo scambio di dati nello spazio sfruttando onde elettromagnetiche (frequenza tipica dei 2.4 GHz per il Wi-Fi e il Bluetooth). 

Nei sistemi IoT (Internet of Things), l'**ESP32** rappresenta una scelta eccellente grazie al suo modulo Wi-Fi e Bluetooth integrato. Tuttavia, la scelta del protocollo di trasmissione dipende strettamente dall'architettura della rete e dalla destinazione dei dati (da microcontrollore a microcontrollore, oppure verso un computer/server come il Raspberry Pi).

---

## 2. Comunicazione Peer-to-Peer senza Router: ESP-NOW
**ESP-NOW** è un protocollo di comunicazione wireless proprietario sviluppato da Espressif Systems.

* **Caratteristiche principali:**
  * **Connectionless (Senza connessione):** Non richiede il processo di "handshaking" o l'associazione a un Access Point (router Wi-Fi).
  * **Basato su Indirizzi MAC:** Ogni pacchetto viene inviato direttamente utilizzando l'indirizzo MAC fisico del dispositivo destinatario.
  * **Bassa Latenza:** Essendo molto vicino al livello link dello stack di rete, i tempi di trasmissione e risposta sono estremamente ridotti.
  * **Limitazioni:** La dimensione massima di un singolo pacchetto payload è limitata a **250 byte**.
* **Contesto d'uso ideale:** Sistemi di controllo remoto, reti di sensori locali (es. domotica casalinga) in cui due o più ESP32 devono parlarsi direttamente senza infrastrutture di rete esterne.

---

## 3. Livello di Trasporto: Socket TCP vs UDP (ESP32 ⇄ Raspberry Pi)
Quando l'ESP32 dialoga con un computer più potente come il **Raspberry Pi** attraverso una rete Wi-Fi tradizionale, la comunicazione si basa sul modello client-server sfruttando i protocolli del livello di trasporto IP:

### A. UDP (User Datagram Protocol)
* **Orientato ai datagrammi:** I pacchetti (datagrammi) vengono inviati dal mittente al destinatario senza verificare se quest'ultimo sia pronto a riceverli.
* **Non affidabile:** Non garantisce l'ordinamento dei pacchetti né la loro effettiva consegna (se un pacchetto si perde sulla rete, non viene richiesto il reinvio).
* **Vantaggi:** Estremamente veloce e a bassissimo overhead. Ideale per streaming di dati in tempo reale dove la perdita occasionale di un campione non compromette il sistema.

### B. TCP (Transmission Control Protocol)
* **Orientato alla connessione:** Prima di scambiare dati, stabilisce una connessione affidabile tramite un processo di handshaking (*three-way handshake*).
* **Affidabile:** Garantisce che ogni pacchetto arrivi a destinazione integro e nel corretto ordine (gestisce la ritrasmissione in caso di errori).
* **Vantaggi:** Sicurezza e integrità totale dei dati trasmessi.

---

## 4. Protocolli Applicativi IoT: Il Modello MQTT
Per far comunicare in modo ordinato ed efficiente uno o più ESP32 con un Raspberry Pi (che solitamente funge da stazione centrale o server), il protocollo standard industriale è **MQTT (Message Queuing Telemetry Transport)**.

* **Architettura Publish/Subscribe:**
  Invece di una connessione diretta uno-a-uno, i dispositivi comunicano attraverso un componente centrale chiamato **Broker MQTT** (spesso installato sul Raspberry Pi tramite software come *Mosquitto*).
  * **Publisher (Mittente):** L'ESP32 pubblica un messaggio associato a un "argomento" testuale (chiamato **Topic**, es. `laboratorio/banco1/temperatura`).
  * **Subscriber (Ricevente):** Il Raspberry Pi si iscrive (effettua la *subscription*) a quel Topic e riceve istantaneamente tutti i dati pubblicati.
* **Vantaggi nell'IoT:**
  * **Leggerezza:** Header dei pacchetti estremamente ridotti, ideale per reti instabili o a banda stretta.
  * **Disoupling (Disaccoppiamento):** Mittente e ricevente non devono conoscersi direttamente né essere attivi nello stesso istante; è il broker a gestire la consegna.

---

## 5. Tabella di Sintesi e Confronto

| Protocollo | Tipo di Rete | Destinatari Tipici | Caratteristica Principale |
| :--- | :--- | :--- | :--- |
| **ESP-NOW** | Wireless Diretta (No Router) | ESP32 ⇄ ESP32 | Velocissimo, basato su MAC, nessun router richiesto. |
| **UDP** | Wi-Fi / IP | ESP32 ⇄ Raspberry Pi | Veloce, leggero, senza garanzia di consegna dei pacchetti. |
| **TCP** | Wi-Fi / IP | ESP32 ⇄ Raspberry Pi | Connessione affidabile, orientata alla sessione e all'integrità. |
| **MQTT** | Applicativo su IP (Wi-Fi) | ESP32 ⇄ Raspberry Pi | Modello Publish/Subscribe gestito da un Broker centrale. |
