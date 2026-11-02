# Vision Sort Lab - percorso guidato

Ultimo aggiornamento: 2 novembre 2026.

Guida principale con esercizi, codice discusso e risultati: [GUIDA-PROGETTO.md](GUIDA-PROGETTO.md). Il recap delle prossime fasi si trova nella sezione 27.

## Obiettivo

Smistare tre oggetti rossi o blu in due contenitori con un braccio Panda: percepire, scegliere la presa, pianificare, eseguire, verificare il deposito e gestire i fallimenti.

Matteo scrive personalmente il codice Python/rclpy, salvo richieste esplicite di completamento all'assistente. L'incarico del 2 novembre per verifiche e TCP e concluso con test automatici e conferma WSL (guida 40.7); Matteo riprende ora la scrittura dall'integrazione Gazebo. Le nuove API vengono spiegate prima degli esercizi e le nuove responsabilita vengono separate in moduli quando migliora la chiarezza. La guida viene aggiornata a ogni checkpoint.

## Ambiente corrente

- ROS 2 Jazzy su Ubuntu 24.04 in WSL.
- Workspace: /home/matteo/vision_sort_ws.
- Workspace verificato per il codice GitHub: /home/matteo/robocell_verify.V8qcfk, checkout src/RoboCell; il workspace originario e conservato.
- Panda nella demo MoveIt/RViz con controllori simulati; Gazebo non ancora integrato.
- Documentazione e asset geometrici nella cartella Windows del progetto.

## Risultati confermati

- Ambiente ROS, demo Panda e monitor dei giunti.
- Pianificazione ed esecuzione dal commander Python.
- Verifica dei sette giunti su campioni aggiornati, tolleranza e timeout.
- Parametro del target articolare da terminale.
- Undici test locali dei rami di fallimento e recupero. Limiti della cancellazione reale e dei codici del servizio documentati: non dichiarare efficace l'arresto nella demo.
- Lettura e aggiornamento della scena con GetPlanningScene e ApplyPlanningScene.
- Lettura TF della pinza e primo piano di posa a Z +0.03 m: SUCCESS (1), 0.018 s, 10 punti (guida 30.7–31.2).
- Verifica del punto finale del piano tramite FK e vincoli riuscita (32.7).
- ExecuteTrajectory nel componente separato MotionExecution: invio, accettazione, feedback e risultato ROS 4 / MoveIt SUCCESS (1) confermati (34.17).
- PoseVerifier: campione registrato 6.138111 ms dopo il riferimento, FK della posa raggiunta entro 2.914 mm dal target, valid=True, due vincoli True, zero contatti e notifica positiva al planner (35.13). Timeout isolato reale poi riuscito in ROS Jazzy CI: 2.001 s, una notifica False, altri 3 s senza duplicati (40).
- Tavolo e tre cubi colorati confermati funzionanti dall'utente.
- File open_bin.stl preparato e verificato geometricamente dall'assistente; conversione in Mesh ROS scritta da Matteo e verificata con 84 vertici, 28 triangoli e ultimo triangolo [81, 82, 83].

## Punto corrente - fase 6, prima posa eseguita e verificata

Fase 5 conclusa al checkpoint 28.5; non ripetere quelle prove senza nuovi problemi. Il percorso positivo della fase 6 arriva fino alla verifica della posa raggiunta dopo ExecuteTrajectory (35.13). Entrambi i passi delegati sono conclusi: 42 test unitari e 4 ROS in CI; TIMEOUT PASS, confronto modelli e TCP PASS con codice 0 nella WSL di Matteo (40.6-40.7). TCP corrente in panda_link0=(0.307020,0,0.486870) m, FK/TF concordi alla precisione del log, nessun movimento per queste prove. PR #1 unita su main. Prossimo blocco: integrazione Gazebo con Matteo nuovamente alla scrittura del codice. Presa e manipolazione non ancora implementate.

La guida conserva la costruzione di MotionExecution in 34 e di PoseVerifier in 35. Il positivo reale del 2 novembre e in 35.13. La PR https://github.com/Matteo7100/RoboCell/pull/1 e unita su main al commit ee0129113b8d70896b625c869dd93637c2558936. Codice d081a28dbd9d503547128e4e4e44896a6c4ccd8f verificato da GitHub Actions; prove WSL confermate in 40.6-40.7. Il TCP virtuale vision_sort_tcp e a (0,0,0.1034) m da panda_hand, con gli stessi assi. Istruzioni riproducibili in guida 40 e RoboCell/docs/VERIFICA-TIMEOUT-TCP.md.

Per i contenitori si usa la stessa mesh nella scena MoveIt per visualizzazione e collisioni. La precedente proposta con cinque primitive non e la consegna attiva.

I chiarimenti in 30.5–30.6 spiegano ToolPoseReader e TransformStamped; il reader e il risultato reale del planner sono registrati in 30.7–31. Non allegati confronti tf2_echo o override panda_link8; la pianificazione riuscita riguarda panda_hand.

La chiusura di questa fase riguarda la scena di pianificazione. Raggiungibilita di presa/deposito e simulazione fisica saranno affrontate nelle fasi successive.

## Prossime fasi

Proposta di sequenza aggiornata dopo la domanda sul passaggio a Gazebo (37.13):

1. Timeout isolato di PoseVerifier senza movimenti: concluso su ROS Jazzy in CI e WSL.
2. TCP nominale e modello MoveIt/TF: conclusi anche sul Panda della WSL; mantenere il riferimento coerente in Gazebo.
3. Gazebo Harmonic: caricamento del Panda, controller e primo movimento comandato da MoveIt con verifica degli stati.
4. Tavolo/cubo fisico e scena coerente; pose esplicite, pinza, pre-presa e presa con contatti.
5. Pipeline riutilizzabile e coordinatore: un ciclo completo di trasporto/deposito, poi tre oggetti.
6. Visione, recupero e metriche.

I dettagli funzionali di 37.3-37.11 restano validi, ma non sono tutti prerequisiti per iniziare Gazebo. Questi sono obiettivi futuri, non risultati acquisiti. Un oggetto collegato idealmente nella scena MoveIt non dimostra una presa fisica.

| Ordine | Fase | Risultato da verificare |
|---|---|---|
| 1 | Scena di pianificazione completata | Sei oggetti, mesh e prova di collisione con ripristino; checkpoint 28.5 |
| 2 | Base MoveIt e preparazione al simulatore | Posa pianificata/eseguita/verificata, timeout, riferimento operativo e modello coerente |
| 3 | Integrazione Gazebo e manipolazione da pose note | Robot e controller, primo movimento, contatti/gravita, presa e deposito di un oggetto, poi tre; scena del pianificatore coerente |
| 4 | Computer vision | Colore e posa ricavati dalle immagini e trasformati nel frame robot, errore misurato rispetto alla ground truth |
| 5 | Smistamento completo e recupero | Depositi verificati, gestione dei fallimenti e prove ripetibili con metriche |

La prima manipolazione usa coordinate note per isolare la pianificazione dalle incertezze della percezione. Un aggancio ideale nella scena MoveIt va dichiarato e non vale come presa fisica. La visione sostituira poi l'ingresso a pose note mantenendo la logica di manipolazione verificata.

## Organizzazione delle chat

- Fase 5, scena di smistamento e collisioni, conclusa al checkpoint 28.5.
- Chat corrente: fase 6, prima posa pianificata, eseguita e verificata su dati aggiornati; checkpoint positivo 35.13.
- Lavoro delegato proseguito in questa chat: verifiche/TCP pubblicati nella PR #1, comandi WSL in sezione 40; prossimo sviluppo Gazebo dopo la conferma locale. Nessuna nuova chat creata.
- Conservare stato, file, prove eseguite e prossimo esercizio, mantenendo il metodo guidato.

## Riferimenti

- [MoveIt](https://moveit.picknik.ai/main/index.html)
- [ROS 2 Jazzy](https://docs.ros.org/en/jazzy/)
- [Gazebo e abbinamenti ROS](https://gazebosim.org/docs/latest/ros_installation/)
