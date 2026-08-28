# ESP32 - MicroPython IoT Essentials

## Introduzione

L'ESP32 si è consolidato come lo standard de facto per l'IoT industriale, offrendo un equilibrio senza precedenti tra potenza computazionale e versatilità di interfacciamento. Questo progetto raccoglie materiale tecnico di riferimento per lo sviluppo embedded basato su ESP32 con MicroPython.

### Perché ESP32 con MicroPython?

L'impiego di MicroPython non è una semplice scelta di comodità, ma una decisione strategica: l'astrazione di alto livello permette di mitigare la complessità dello sviluppo bare-metal, pur mantenendo un controllo granulare sulle risorse hardware tramite i moduli `machine` ed `esp`.

#### Caratteristiche chiave

- **Dual-core a 240 MHz** - Frequenza gestibile via `machine.freq()` per bilanciare throughput e consumo energetico
- **3 controller UART** - GPIO matrix per il mappaggio flessibile dei segnali TX/RX
- **16 canali PWM** - Fino a 40 MHz con tradeoff risoluzione/duty cycle
- **2 controller I2C e 2 SPI** - Infrastruttura bus per sensori e periferiche ad alte prestazioni
- **ADC dual-block** - Attenzione: ADC2 condiviso con il modulo WiFi
- **Deep-Sleep avanzato** - Gestione granulare del risveglio via RTC e Pad Hold

## Contenuti del progetto

| File | Descrizione |
|------|-------------|
| `ESP32_Specifiche_tecniche_e_periferiche_con_micropython.md` | Guida tecnica completa: architettura CPU, UART, PWM/ADC, bus I2C/SPI, gestione energia e tabella di riferimento pin |
| `ESP32_MicroPython_IoT_Essentials.pdf` | Materiale di approfondimento sulle essenzialità MicroPython per IoT |
| `img/Guida_tecnica_hardware_e_protocolli.png` | Rappresentazione visiva dei protocolli e dell'hardware |

## Riferimento rapido pin

| Periferica | Pin | Note |
|------------|-----|------|
| GPIO utilizzabili | 0-19, 21-23, 25-27, 32-39 | Range totale |
| Pin solo input | 34-39 | Privi di pull-up/down interni |
| Pin critici (Flash) | 6-11, 16, 17 | Da evitare, legati alla SPI interna |
| ADC Block 1 | 32-39 | Utilizzabile con WiFi attivo |
| ADC Block 2 | 0, 2, 4, 12-15, 25-27 | Conflitto con WiFi |
| DAC | 25, 26 | Output analogico 8-bit |

## Licenza

Materiale didattico di riferimento.
