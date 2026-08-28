# Installazione

Per effettuare una corretta configurazione del dispositivo esp32:

 - per iniziare è necessario installare sul pc i driver:  [Download driver per esp32](www.micropython.org/download/);
 - per essere sicuri di aver effettuato l'installazione dei driver senza problemi, premere "windows + x" e 
   selezionare la voce "Gestione dispositivi": se l'installazione è andata a buon fine allora si vedrà una 
   voce dedicata sulla porta usata (ad esempio a me in corrispondenza della COM5 vedo "Silicon Labs CP210x
   USB to UART Bridge");
 <details>
  <summary>ulteriore conferma la si può ottenere con **Arduino IDE**, oppure con putty.</summary>

   ![Putty](./img/putty.bmp)
 <p>Dopo aver effettuato la connessione, provare a premere il tasto reset sulla board e vedere se sul terminale succede qualcosa;</p>
 </details>
 <details>
  <summary>in alternativa usare thonny</summary>

   ![Thonny](./img/thonny.bmp)
 <p>Digitando sulla parte indicata dalla freccia, si apre un menù a tendina che vi permette una serie di opzioni selezionabili per l'interprete.</p>

   ![Thonny configurazione](./img/thonny2.bmp)
 </details>

```

 Attenzione:
 Se durante il tentativo di configurazione il dispositivo resta nascosto o non reperibile probabilmente si sta usando un cavo errato che non permette lo scambio di informazioni tra l'esp e il pc, ma solo il caricamento di una batteria.

```