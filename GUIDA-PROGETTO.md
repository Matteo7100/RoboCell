# Vision Sort Lab — guida e diario del progetto

Ultimo aggiornamento: 2 novembre 2026.

Questa è la guida principale del progetto. Viene aggiornata durante il lavoro con obiettivi, motivazioni, comandi, snippet dei file studiati o scritti, risultati e problemi risolti. `PERCORSO.md` rimane la mappa sintetica dei traguardi.

### Dove sono i file

| Ambiente | Percorso | Uso |
|---|---|---|
| Windows | `C:\Users\matte\Documents\Codex\2026-10-05\vor\outputs\vision-sort-lab\GUIDA-PROGETTO.md` | Questa guida |
| Windows | `C:\Users\matte\Documents\Codex\2026-10-05\vor\outputs\vision-sort-lab\PERCORSO.md` | Mappa sintetica |
| Ubuntu WSL 2 | `/home/matteo/vision_sort_ws` | Workspace ROS 2 |
| Ubuntu WSL 2 | `/home/matteo/vision_sort_ws/src/vision_sort_lab` | Pacchetto ROS Python |
| Ubuntu WSL 2 | `/home/matteo/vision_sort_ws/src/vision_sort_lab/vision_sort_lab` | Moduli `joint_monitor.py`, `motion_commander.py`, `motion_builders.py` e `motion_errors.py` |

La guida è un documento Windows. I comandi `bash` in questa guida sono invece destinati al terminale Ubuntu WSL. Non occorre spostare la guida in Ubuntu per consultarla o aggiornarla.

### Stato attuale e punti di consultazione

- **Completato:** ambiente ROS, demo Panda, movimenti da RViz e monitor Python dei giunti.
- **Completato:** primo movimento comandato da `motion_commander`, con pianificazione, accettazione del goal, feedback e risultato finale.
- **Completato nel caso positivo:** verifica automatica dei sette giunti entro `0.01` rad, su un campione successivo al risultato dell'esecuzione.
- **Completato:** prima separazione dei builder in `motion_builders.py`, con movimento e verifica riusciti dopo il refactoring.
- **Completato:** timeout della verifica con timer periodico, prova controllata del timeout e ripristino del percorso positivo.
- **Completato:** primo test negativo di pianificazione con gruppo inesistente, codice `99999` e ripristino confermati dall'utente.
- **Completato:** secondo test negativo con vincoli incompatibili sul primo giunto e ripristino del percorso positivo confermati dall'utente.
- **Completato:** descrizione dei codici in `motion_errors.py`, import nel commander, log con nome e numero, prova negativa e ripristino confermati dall'utente.
- **Completato:** test locali dei rami eccezione e goal rifiutato di `on_execution_goal_response`, seguiti da prova Panda positiva con log allegato.
- **Completato:** script con cinque test locali riusciti; `on_execution_result` e descrizione di `CONTROL_FAILED` ricevuti e rivisti.
- **Osservato e ripristinato:** risultato negativo dell'action reale, `STATUS_ABORTED` e `CONTROL_FAILED`; successiva esecuzione positiva e ritorno al target normale confermati (17.11).
- **Osservato e ripristinato:** verifica articolare negativa su campione aggiornato, primo giunto fuori tolleranza; ritorno al target normale, verifica positiva e assenza di timeout confermati dal log (17.11).
- **Completato localmente:** richiesta e risposta di cancellazione; tre nuovi test ricevuti e rivisti, otto messaggi `OK` confermati dall'output dell'utente (17.8).
- **Osservato nella demo:** richiesta di cancellazione dopo `0.301` s; risposta a fine esecuzione con `ERROR_GOAL_TERMINATED (3)` e lista vuota. Movimento completato e verifica positiva; arresto tramite cancellazione non ottenuto (17.10).
- **Installazione osservata:** `moveit_ros_move_group` da `/opt/ros/jazzy`, pacchetto Ubuntu `2.12.4-1noble.20260915.202214` (17.11).
- **Completato localmente:** Matteo conferma che, dopo le correzioni, tutti gli undici test passano: limite, codice escluso e recupero riuscito del piano simulato (18.8). I codici specifici del retry non sono stati osservati dal servizio reale.
- **Limite del servizio verificato nel sorgente 2.12.4:** `GetMotionPlan` sostituisce con `FAILURE (99999)` il codice quando `generatePlan` restituisce falso. La politica del retry non include quel codice generico; non promettere una ripetizione nella demo per quei fallimenti (18.9).
- **Completato:** parametro del target da terminale confermato dall'utente; log del movimento verso `0.8` rad con verifica positiva allegato (19.4). Conferma generale delle prove, senza altri due log o costruttore allegati.
- **Completato:** `scene_inspector.py` ricevuto e rivisto; richiesta reale a GetPlanningScene riuscita, `Numero oggetti: 0` (20.7). Import Node corretto nel codice. Risoluzione degli avvisi Pylance non esplicitamente confermata.
- **Punto corrente (2 novembre):** percorso completo positivo confermato in 35.13. Matteo incarica l'assistente di completare verifiche e TCP, riprendendo il codice da Gazebo. Ricevuta e letta Matteo7100/RoboCell al commit d0a779fb13b6f9faf677d2486586d5b6dc2f7c91. Copia locale in RoboCell: timeout_probe, trasformazioni TCP/mano, report del modello e 36 test unitari passati (39). Creazione del ramo remoto rifiutata con 403; gh locale non autenticato. Richiesti accesso per la pubblicazione e dump della descrizione robot attiva. Test del timer ROS e TCP specifico ancora da completare; nessuna modifica remota o nuovo movimento.
- **Ancora da verificare o realizzare:** manipolazione da pose note, presa fisica in Gazebo, visione e recupero al livello del compito; la cancellazione efficace nella demo resta un limite distinto documentato.

Per ritrovare rapidamente il materiale:

| Sezione | Contenuto |
|---|---|
| 4–5 | Installazione e demo Panda |
| 6.8–6.11 | Monitor dei giunti, problemi risolti e codice completo di riferimento |
| 7.1–7.5 | Architettura del comando, interfacce e dipendenze |
| 7.6 | `motion_commander.py` completo e commentato |
| 7.7–7.11 | Spiegazione delle funzioni, Future e callback |
| 7.12–7.13 | Comandi, output verificato e diagnosi |
| 7.14–7.16 | Limiti attuali, Python/C++ e continuità nella nuova chat |
| 8–10 | Decisioni, diario e fonti |
| 11 | Verifica dei giunti: esercizi, revisioni, controllo temporale e checkpoint operativo |
| 12 | Timeout della verifica, prova controllata e ripristino confermati |
| 13 | Punto di ripresa: revisione di `on_plan_response` e fallimento di pianificazione |
| 14 | Punto di ripresa attuale: risposta al goal di esecuzione e fallimenti dell'action |
| 15 | Consegna attuale: log e test del risultato finale dell'esecuzione |
| 16 | Consegna attuale: ultima prova di fallimento, verifica articolare negativa e ripristino |
| 17 | Richiesta e risposta di cancellazione, test locali, prova nella demo e ripristino |
| 18 | Consegna attuale: un solo nuovo tentativo di pianificazione e test del recupero |
| 19 | Consegna attuale: target del primo giunto configurabile all'avvio tramite parametro ROS |
| 20 | Consegna attuale: leggere gli oggetti di collisione con un nodo separato |
| 21 | Consegna attuale: costruire il messaggio CollisionObject del piano di lavoro |
| 27–29 | Roadmap, chiusura della scena e passaggio alla fase 6 |
| 30 | Fase 6: link terminale, riferimento della pinza e lettura della posa tramite TF2 |
| 31 | Primo piano di posa riuscito: builder, revisione e checkpoint con 10 punti |
| 32 | Verifica del punto finale: cinematica diretta, vincoli e checkpoint positivo in 32.7 |
| 33 | Ripresa dal listato allegato e chiarimenti didattici; proposta iniziale interna al planner, superata da 34 |
| 34 | MotionExecution: percorso positivo e correzione del log confermati in 34.17 |
| 35 | PoseVerifier: primo risultato reale positivo su campione aggiornato in 35.13; timeout controllato ancora da verificare |
| 36 | Passaggio alla nuova chat: stato, prossimo test isolato del timeout e testo di ripresa |
| 37 | Roadmap dettagliata: timeout, TCP, pipeline riutilizzabile, prima manipolazione e fasi successive |
| 38 | Incarico all'assistente per verifiche/TCP; collaborazione GitHub, sorgenti e comandi di verifica WSL |

## 1. Come lavoriamo

Matteo scrive il codice attraverso esercizi guidati. L'assistente spiega il problema, propone un passo limitato, rivede la soluzione e aiuta a interpretare gli errori. Le nuove API vengono spiegate prima di essere usate nell'esercizio. Gli snippet servono a studiare i componenti o a chiarire il passo corrente; una soluzione completa viene fornita quando richiesta.

**Preferenza aggiornata il 14 ottobre 2026:** Matteo chiede consegne un po' più lunghe per ridurre il tempo perso fra le risposte. Raggruppare spiegazioni delle nuove API, implementazione, comandi e criteri di verifica in un blocco coerente; chiedere codice e risultati al termine del blocco, evitando revisioni intermedie per ogni singola riga. Il codice continua a essere scritto da Matteo, con esercizi di portata gestibile.

**Preferenza precisata il 28 ottobre 2026:** essere piu espliciti nel metodo di costruzione delle nuove funzioni/classi. Prima della consegna distinguere le classi da definire, quelle gia esistenti e gli oggetti delle librerie da istanziare. Per ogni metodo spiegare responsabilita, firma e provenienza degli argomenti, attributi letti/modificati, valore restituito, ordine dei controlli e collegamento con il chiamante. Mostrare come ricavare questi passaggi dal problema, lasciando a Matteo la scrittura del corpo Python. Un semplice rinvio a MotionCommander non basta: indicare esattamente quale schema riusare e come adattarlo a PosePlanner. Mantenere un blocco completo di implementazione e verifica, senza chiedere una revisione per ogni riga.

**Organizzazione del codice, richiesta il 28 ottobre 2026:** per funzionalita nuove preferire un nuovo file quando emerge una responsabilita coerente, mantenendo piccole le integrazioni nei file esistenti. Ampliare funzioni esistenti quando e il loro compito naturale; valutare esplicitamente la separazione per chiarezza. Il criterio e una responsabilita per componente, non un file per ogni funzione. La nuova esecuzione viene quindi sviluppata in un modulo separato (34); pianificazione e verifiche gia funzionanti non vengono riscritte per questa scelta.

**Eccezione richiesta il 2 novembre 2026:** Matteo chiede che l'assistente scriva il codice necessario da on_fk_response compreso in poi nel nuovo PoseVerifier. Per questo blocco l'assistente fornisce le callback FK e validita, destroy e i collegamenti al planner; la parte precedente resta quella scritta dall'utente. La richiesta autorizza il codice di completamento e non richiede di riscrivere l'intera classe.

**Incarico aggiornato il 2 novembre 2026:** Matteo delega all'assistente i prossimi due blocchi completi, fine delle verifiche e definizione del TCP. L'assistente puo implementare e modificare i file necessari entro questo ambito, con prove e documentazione; Matteo riprendera la scrittura quando iniziera l'integrazione Gazebo. Fino ad allora eseguira in WSL i comandi di verifica forniti in questa chat. Viene proposta una repository GitHub condivisa per lavorare sulle versioni correnti, senza dipendere dall'accesso diretto ai file WSL. Questa autorizzazione supera la precedente modalita di scrittura guidata per i due blocchi indicati.

Ogni passo distingue tre informazioni:

- **Eseguito e confermato:** verificato tramite output o conferma dell'utente.
- **Da eseguire:** istruzioni del prossimo esercizio.
- **Esempio di lettura:** frammento che spiega un concetto; non è un file completo da avviare.

Non consideriamo una funzionalità completata solo perché il comando è stato suggerito o il file è stato scritto. Per ogni passo registriamo un risultato osservabile.

Il 12 ottobre Matteo ha chiesto esplicitamente di riunire nella guida gli aggiornamenti e gli snippet della chat. Il codice completo riportato qui è materiale di riferimento ricostruito dai tentativi e dalle correzioni discussi, non un nuovo progetto sviluppato al posto dell'utente. I file Ubuntu non sono stati modificati durante questo aggiornamento della documentazione. Alla ripresa del 13 ottobre Matteo ha richiesto di aggiornare la guida a ogni checkpoint: registriamo la revisione del codice e l'esito delle prove, distinguendo ciò che è confermato da ciò che resta da eseguire.

## 2. Cosa vogliamo costruire

Una cella virtuale in cui un braccio osserva tre oggetti rossi o blu, li afferra e li deposita in due contenitori. La sequenza completa è:

**osservare → individuare → scegliere la presa → pianificare → eseguire → verificare → recuperare se necessario.**

Nella prima versione gli oggetti sono separati, appoggiati su un piano noto e dentro un'area raggiungibile. La presa è inizialmente dall'alto. Questi vincoli permettono di affrontare un problema alla volta e di capire dove nasce un eventuale errore.

La prima verifica del movimento utilizza pose note. Quando aggiungeremo la visione, il comando al robot utilizzerà coordinate ricavate dalla telecamera; le pose note del simulatore serviranno a misurare l'errore e non a sostituire la percezione.

### Perché questo progetto

Il progetto collega la precedente esperienza di Matteo con ROS, navigazione, controllo di manipolatori e SayCan a una pipeline di manipolazione completa. I nuovi aspetti principali sono il passaggio dalle immagini alle coordinate del robot, la pianificazione con collisioni, la verifica del compito e il recupero dagli errori.

Java potrà gestire ordini, interfaccia e report. Un PLC potrà coordinare nastro o stazioni. Il primo traguardo riguarda la pipeline robotica, prima di integrare questi componenti.

## 3. Architettura e motivazioni

| Componente | Ruolo | Perché lo usiamo |
|---|---|---|
| Ubuntu 24.04 in WSL 2 | Ambiente Linux sul PC Windows | Offre una base adatta ai pacchetti ROS scelti |
| ROS 2 Jazzy | Comunicazione fra nodi e strumenti | Separa percezione, pianificazione ed esecuzione in componenti verificabili |
| RViz | Visualizzazione e ispezione | Permette di controllare robot, frame, stati e traiettorie |
| MoveIt 2 | Cinematica e pianificazione | Trasforma un obiettivo in una traiettoria, considerando il modello del robot e le collisioni |
| Gazebo Harmonic | Simulazione del processo fisico e dei sensori | Permetterà di osservare contatti, oggetti, pinza e immagini sintetiche |
| Python/rclpy | Nodi attuali di monitoraggio e comando | Consente di apprendere ROS 2, servizi, action e callback |
| Python/OpenCV | Prima percezione futura | Consente di iniziare con segmentazione del colore su immagini semplici |
| C++/rclcpp | Componenti futuri, quando utili | Offre controllo delle risorse e accesso alle API C++; non è richiesto per proseguire |

Ubuntu 24.04, ROS 2 Jazzy e Gazebo Harmonic sono un abbinamento documentato. I tutorial online `main` possono riferirsi a Rolling e usare un robot diverso: i nomi dei gruppi e dei pacchetti vanno verificati per la configurazione che installiamo.

### Tre livelli da distinguere

1. **Visualizzazione:** vedere una geometria o un'animazione in RViz.
2. **Pianificazione ed esecuzione tramite hardware simulato:** calcolare una traiettoria, inviarla al controllore e ricevere stati dei giunti aggiornati.
3. **Simulazione fisica:** verificare contatti, presa, gravità e movimento degli oggetti in Gazebo.

L'esercizio corrente riguarda il secondo livello. Il movimento del braccio nella demo non dimostra che una pinza riesca a sollevare un oggetto.

### Python, ROS 2 e MoveIt 2 sono livelli differenti

Python è il linguaggio del nostro codice; `rclpy` è la libreria client ROS 2 usata dai nostri nodi. ROS 2 mette a disposizione comunicazione e strumenti. MoveIt 2 fornisce le funzionalità robotiche a cui il nodo invia le richieste.

`joint_monitor` e `motion_commander` sono già nodi ROS 2. Usare Python non significa lavorare fuori da ROS 2. Nodi Python e C++ possono convivere nello stesso sistema tramite le stesse interfacce.

## 4. Esercizio 0 — ambiente ROS

**Stato: completato, confermato dall'utente.**

### 4.1 Diagnosi iniziale

Comandi eseguiti in Ubuntu:

```bash
lsb_release -ds
ls /opt/ros
printenv DISPLAY WAYLAND_DISPLAY
```

Output iniziale comunicato dall'utente:

```text
Ubuntu 24.04.1 LTS
ls: cannot access '/opt/ros': No such file or directory
:0
wayland-0
```

Interpretazione: Ubuntu è della versione adatta; ROS non era rilevato nella posizione standard; le variabili della sessione grafica WSLg erano presenti. La grafica andava ancora provata avviando un'applicazione. Il messaggio `No LSB modules are available` non impediva l'esercizio.

### 4.2 Preparazione del sistema

Procedura fornita durante l'installazione:

```bash
export LANG=C.UTF-8
export LC_ALL=C.UTF-8

sudo apt update
sudo apt upgrade
sudo apt install software-properties-common curl ca-certificates
sudo add-apt-repository universe
```

Le prime due righe configurano UTF-8 nella sessione corrente. `apt update` aggiorna gli indici dei pacchetti; `apt upgrade` aggiorna quelli installati. `universe` abilita una componente dei repository Ubuntu richiesta dalle dipendenze.

### 4.3 Configurazione del repository ROS

Il pacchetto ufficiale `ros2-apt-source` configura repository e chiavi. Per Ubuntu Noble è stata proposta la release 1.3.0, verificata durante la preparazione delle istruzioni.

```bash
curl -fL -o /tmp/ros2-apt-source.deb \
  https://github.com/ros-infrastructure/ros-apt-source/releases/download/1.3.0/ros2-apt-source_1.3.0.noble_all.deb

sudo dpkg -i /tmp/ros2-apt-source.deb
sudo apt update
```

`curl -fL` segue i reindirizzamenti e termina con errore se il server restituisce un errore HTTP. `dpkg -i` installa il pacchetto di configurazione scaricato. I pacchetti ROS successivi vengono gestiti tramite APT.

### 4.4 Installazione Desktop e ambiente

```bash
sudo apt install ros-jazzy-desktop
source /opt/ros/jazzy/setup.bash
echo "$ROS_DISTRO"
```

La distribuzione Desktop include RViz e i programmi dimostrativi. `source` carica nel terminale le variabili necessarie a trovare pacchetti e comandi ROS. L'output atteso dell'ultima riga è `jazzy`.

Per ora eseguiamo `source` in ciascun terminale ROS. Questo rende esplicita la distribuzione che stiamo utilizzando, prima di introdurre automatismi nella configurazione della shell.

### 4.5 Verifica della comunicazione

Primo terminale Ubuntu:

```bash
source /opt/ros/jazzy/setup.bash
ros2 run demo_nodes_cpp talker
```

Secondo terminale Ubuntu:

```bash
source /opt/ros/jazzy/setup.bash
ros2 run demo_nodes_py listener
```

Il talker pubblica messaggi e il listener li riceve. Questo esercizio introduce nodi, topic e comunicazione fra programmi C++ e Python. `Ctrl+C` interrompe ciascun programma.

### 4.6 Verifica della grafica

```bash
rviz2
```

L'utente ha confermato che la procedura funziona: comunicazione e apertura di RViz sono riuscite. Non abbiamo ancora registrato le versioni esatte dei pacchetti installati.

## 5. Esercizio 1 — primo movimento con MoveIt e Panda

**Stato: demo utilizzata e movimento osservato, confermato dall'utente; simulazione fisica della presa ancora da verificare.**

### 5.1 Obiettivo

Caricare il robot in RViz, definire una posa obiettivo vicina allo stato iniziale, pianificare una traiettoria e inviarla ai controllori della demo. Osservare la differenza fra posa obiettivo, anteprima della traiettoria e stato corrente del robot.

### 5.2 Scelta del robot

Per questo esercizio utilizziamo la configurazione didattica Panda di `moveit_resources`: il braccio ha sette giunti e una pinza parallela. Un braccio a sette giunti è ridondante rispetto a una posa cartesiana completa dell'organo terminale; possono esistere più configurazioni articolari compatibili con la stessa posa, entro limiti e vincoli.

Questa configurazione permette di iniziare con un modello esistente. L'integrazione in Gazebo e la futura scelta del modello per hardware reale richiedono verifiche ulteriori. La configurazione del repository è pensata per esempi e test di MoveIt.

### 5.3 Installazione dei pacchetti precompilati

Eseguire nel terminale Ubuntu:

```bash
sudo apt update
sudo apt install ros-jazzy-moveit ros-jazzy-moveit-resources-panda-moveit-config
source /opt/ros/jazzy/setup.bash
```

`ros-jazzy-moveit` installa lo stack MoveIt. Il secondo pacchetto contiene la configurazione Panda e porta con sé le dipendenze dichiarate, inclusa la descrizione del robot. Usiamo i pacchetti APT per concentrarci sul primo comportamento osservabile; un workspace con il nostro codice verrà introdotto nell'esercizio successivo.

Verificare che ROS trovi il pacchetto:

```bash
ros2 pkg prefix --share moveit_resources_panda_moveit_config
```

Il risultato deve essere il percorso della cartella `share` del pacchetto. Se APT non trova un pacchetto o ROS non lo individua, registrare l'errore e risolverlo prima del launch.

### 5.4 Avvio della demo

Chiudere la precedente finestra RViz generica, quindi avviare:

```bash
ros2 launch moveit_resources_panda_moveit_config demo.launch.py
```

La demo avvia più componenti: descrizione e trasformazioni del robot, server MoveIt `move_group`, RViz e controllori con hardware simulato. Il terminale deve rimanere aperto durante la prova. Il codice installato può differire dal ramo upstream consultato: in caso di errore si studia la versione locale.

### 5.5 Primo esperimento in RViz

1. Individuare il pannello **MotionPlanning**. Se il display manca, aggiungerlo da **Displays → Add → MotionPlanning**. Se necessario, aggiungere il pannello dal menu **Panels → Add New Panel**.
2. Selezionare il gruppo **panda_arm**. Il gruppo **hand** riguarda la pinza; i tutorial di altri robot possono usare nomi differenti.
3. Usare lo stato corrente come stato iniziale. Nel pannello **Displays**, espandere **MotionPlanning → Planning Request** tramite le freccette accanto ai nomi e spuntare **Query Goal State**. Per questa prima prova lasciare **Query Start State** disattivato, così si interagisce soltanto con l'obiettivo. Nella barra degli strumenti in alto selezionare **Interact**; se manca, premere **+**, scegliere **Interact** e confermare. Vicino alla pinza compare il marker con frecce e anelli: trascinare una freccia per cambiare la posizione oppure un anello per cambiare l'orientazione. Il trascinamento dello sfondo ruota la vista, non il marker.
4. Spostare l'obiettivo di pochi centimetri, circa 5 cm, lasciando inizialmente invariata l'orientazione. Evitare di cambiare contemporaneamente posizione, orientazione e stato iniziale: sarebbe più difficile diagnosticare un fallimento.
5. Premere **Plan** e osservare la traiettoria mostrata come anteprima.
6. Dopo una pianificazione riuscita, premere **Execute**. Osservare lo stato del robot aggiornato dai controllori della demo.

Se si cambia l'obiettivo, occorre pianificare di nuovo prima di eseguire. Un marker spostato rappresenta una richiesta; non significa che il robot abbia già eseguito un movimento. Le animazioni della traiettoria in RViz possono sembrare un movimento del robot anche prima di Execute: la verifica dello stato corrente chiarisce la differenza.

### 5.6 Verifica dal terminale

Con la demo in esecuzione, aprire un secondo terminale Ubuntu:

```bash
source /opt/ros/jazzy/setup.bash
ros2 node list
ros2 topic list
ros2 topic echo /joint_states --once
```

La prima riga di ispezione elenca i nodi. La seconda mostra i topic. L'ultima legge un messaggio degli stati articolari e termina. Nel messaggio, `name` identifica i giunti e `position` contiene le rispettive posizioni, in radianti per i giunti rotativi e metri per quelli prismatici. Non assumere che l'ordine dei giunti sia quello immaginato: associa sempre nomi e valori.

Ripetere la lettura prima e dopo Execute per verificare che lo stato sia cambiato. La presenza di nomi o valori non attesi si interpreta leggendo il modello installato.

### 5.7 File che studiamo: il launch

Individuare la cartella del pacchetto senza assumere un percorso fisso:

```bash
panda_share_dir="$(ros2 pkg prefix --share moveit_resources_panda_moveit_config)"
less "$panda_share_dir/launch/demo.launch.py"
```

In `less`, premere `q` per uscire. La lettura è parte dell'esercizio: i file installati rimangono invariati. Quando scriveremo la nostra configurazione, lavoreremo in un pacchetto del progetto.

Questo estratto del sorgente upstream mostra come il launch definisce il server MoveIt:

```python
move_group_node = Node(
    package="moveit_ros_move_group",
    executable="move_group",
    output="screen",
    parameters=[moveit_config.to_dict()],
    arguments=["--ros-args", "--log-level", "info"],
)
```

**Esempio di lettura, non file completo.** `Node` è un'azione del sistema di launch: specifica quale eseguibile avviare, da quale pacchetto e con quali parametri. `moveit_config` è costruito in precedenza nel launch. Il server mette a disposizione i servizi e le azioni di pianificazione ed esecuzione; RViz è l'interfaccia con cui li utilizziamo in questo esercizio.

Fonte del frammento: [demo.launch.py di moveit_resources](https://github.com/moveit/moveit_resources/blob/ros2/panda_moveit_config/launch/demo.launch.py), consultato il 7 ottobre 2026. La versione installata va controllata prima di trasferire modifiche da un tutorial.

### 5.8 File che studiamo: il gruppo di pianificazione

```bash
less "$panda_share_dir/config/panda.srdf"
```

Questo breve estratto definisce il gruppo del braccio:

```xml
<group name="panda_arm">
  <chain base_link="panda_link0" tip_link="panda_link8"/>
</group>
```

**Esempio di lettura.** L'SRDF aggiunge informazioni semantiche alla descrizione del robot: qui il gruppo indica la catena su cui pianificare. I nomi dei link devono corrispondere a quelli della descrizione URDF. Il frame di punta della catena non va automaticamente considerato uguale al punto di presa fra le dita: studieremo la trasformazione verso il riferimento della pinza prima di comandare una presa.

Fonte del frammento: [panda.srdf di moveit_resources](https://github.com/moveit/moveit_resources/blob/ros2/panda_moveit_config/config/panda.srdf).

### 5.9 Piccolo esercizio di ragionamento

Dopo il primo movimento, annotare:

- Cosa è cambiato quando è stato spostato il marker?
- Che cosa ha fatto Plan e che cosa ha fatto Execute?
- Quali giunti hanno cambiato posizione nel messaggio `/joint_states`?
- Perché una posa dell'organo terminale può corrispondere a più configurazioni del braccio?

Poi provare una seconda posa vicina, cambiando solo l'orientazione. Registrare se la pianificazione riesce e se il percorso differisce. Non è necessario ottenere lo stesso percorso a ogni richiesta: alcuni pianificatori utilizzano campionamento.

### 5.10 Criteri di completamento

- Il Panda compare in RViz e il gruppo `panda_arm` è disponibile.
- Un obiettivo vicino produce una traiettoria pianificata.
- Execute termina e lo stato corrente del braccio raggiunge l'obiettivo nella demo.
- Gli stati dei giunti sono leggibili e coerenti con l'esecuzione.
- Matteo distingue l'anteprima dalla traiettoria eseguita e dalla futura simulazione fisica.

**Risultato dell'esercizio: demo operativa; l'utente ha confermato la prova di movimento e l'osservazione dei giunti tramite il proprio nodo.**

## 6. Esercizio 2 — workspace, pacchetto e nodo

**Stato 2A: creazione, build e visibilità del pacchetto confermate dall'output dell'utente. Modifiche alle descrizioni non ispezionate. Stato 2B: nodo scritto e avviato dall'utente; ricezione e osservazione del movimento confermate.**

Dopo il chiarimento sui marker in RViz, l'utente ha costruito e avviato il monitor dei giunti e ha confermato il funzionamento della prova di movimento.

### 6.1 Obiettivo e motivazione

Creare il pacchetto `vision_sort_lab` nel workspace Ubuntu `~/vision_sort_ws`. Nel passo 2B Matteo scriverà un nodo `joint_monitor` che riceve `/joint_states`: servirà a osservare i valori con cui, in seguito, confronteremo movimento richiesto e stato ricevuto. Il nodo iniziale leggerà dati; non comanderà il robot.

Python permette di concentrarsi su messaggi e callback usando un linguaggio già familiare. Questo primo pacchetto usa `ament_python`; un successivo componente C++ potrà essere un pacchetto distinto nello stesso workspace.

Un **workspace** raccoglie pacchetti e risultati della build; un **pacchetto ROS** organizza codice, dipendenze e metadati; un **nodo** è un componente avviato che partecipa alla comunicazione ROS. Creare il pacchetto non crea automaticamente un nodo in esecuzione.

Il workspace viene creato nel filesystem Linux, sotto la home di Matteo. La guida resta nel percorso Windows già condiviso. `~` indica la home dell'utente Ubuntu; i comandi seguenti vanno eseguiti in Ubuntu, non in PowerShell.

### 6.2 Preparare gli strumenti e creare il pacchetto

In un nuovo terminale Ubuntu:

```bash
source /opt/ros/jazzy/setup.bash
sudo apt update
sudo apt install python3-colcon-common-extensions

mkdir -p ~/vision_sort_ws/src
cd ~/vision_sort_ws/src

ros2 pkg create vision_sort_lab \
  --build-type ament_python \
  --license Apache-2.0 \
  --dependencies rclpy sensor_msgs
```

`colcon` gestisce la build del workspace. `mkdir -p` crea le cartelle necessarie. Il comando `ros2 pkg create` genera la struttura iniziale; `ament_python` seleziona il tipo di pacchetto. `rclpy` è la libreria client ROS per Python; `sensor_msgs` contiene il tipo di messaggio `JointState` che useremo. La licenza dichiarata per il pacchetto didattico è Apache-2.0.

Non utilizziamo `--node-name`: il primo nodo sarà scritto da Matteo nel passo 2B. Se il pacchetto esiste già, non cancellarlo né ricrearlo per ripetere l'esercizio: controllare i file presenti.

### 6.3 Leggere e modificare i primi file

```bash
cd ~/vision_sort_ws/src/vision_sort_lab
ls
cat package.xml
cat setup.py
cat setup.cfg
```

Struttura principale attesa (il generatore può aggiungere altri file):

```text
vision_sort_ws/
└── src/
    └── vision_sort_lab/          # pacchetto ROS
        ├── package.xml          # metadati e dipendenze ROS
        ├── setup.py             # installazione del codice Python
        ├── setup.cfg            # percorso degli eseguibili installati
        ├── resource/
        │   └── vision_sort_lab  # marker per l'indice dei pacchetti ROS
        ├── vision_sort_lab/     # package Python: qui scriveremo il nodo
        │   └── __init__.py
        └── test/                # controlli generati dal template
```

Le due cartelle `vision_sort_lab` hanno ruoli diversi: quella esterna contiene il pacchetto ROS; quella interna è il package Python importabile.

Aprire i file con l'editor preferito. Una possibilità dal terminale è:

```bash
nano package.xml
```

In `nano`, `Ctrl+O` e Invio salvano; `Ctrl+X` chiude. Nel file sostituire soltanto il testo della descrizione, mantenendo il resto:

```xml
<description>Guided robotic vision sorting and recovery project</description>
```

Poi aprire `setup.py`:

```bash
nano setup.py
```

Modificare la relativa voce, lasciando invariato il resto della chiamata a `setup`:

```python
description='Guided robotic vision sorting and recovery project',
```

Questi sono **snippet da inserire nei file generati**, non file completi. Manteniamo coerenti i metadati ROS e Python. In `package.xml` individuare le dipendenze `rclpy` e `sensor_msgs` generate dal comando precedente; non aggiungerle una seconda volta. Studiare anche `console_scripts` in `setup.py`: nel passo 2B collegheremo un nome eseguibile alla funzione `main` del nodo.

### 6.4 Prima build e registrazione nell'ambiente

Nel terminale usato per creare il pacchetto:

```bash
cd ~/vision_sort_ws
colcon build --symlink-install --packages-select vision_sort_lab
```

La build prepara l'installazione anche se il codice è Python. `--packages-select` limita il lavoro al nostro pacchetto; `--symlink-install` usa collegamenti dove supportati, agevolando lo sviluppo. Le modifiche ai metadati e agli entry point richiedono comunque una nuova build.

Dopo una build riuscita, aprire **un altro terminale Ubuntu**:

```bash
source /opt/ros/jazzy/setup.bash
source ~/vision_sort_ws/install/local_setup.bash
ros2 pkg prefix vision_sort_lab
```

Il primo `source` carica ROS installato tramite APT (underlay); il secondo aggiunge il nostro workspace (overlay). Il percorso restituito dovrebbe trovarsi sotto `~/vision_sort_ws/install`. I `source` valgono solo per il terminale corrente. Per le build future usare un terminale con il solo ambiente base ROS, senza caricare prima l'overlay che si sta ricostruendo.

Dopo la build compaiono `build/`, `install/` e `log/`: contengono risultati intermedi, installazione e log. I file che scriviamo restano in `src/`.

### 6.5 Consegna e criterio di completamento

Comunicare il riepilogo finale di `colcon build` e l'output di `ros2 pkg prefix vision_sort_lab`. Spiegare inoltre perché dichiariamo `sensor_msgs` pur non avendo ancora scritto il nodo e quale delle due cartelle omonime ospiterà il file `joint_monitor.py`.

Il passo è completato quando la build riesce, ROS trova il pacchetto nel workspace e le due descrizioni sono coerenti. Non è ancora una verifica della ricezione di messaggi: questa sarà la prova del passo 2B.

### 6.6 Risultato del passo 2A

Output comunicato da Matteo:

```text
Starting >>> vision_sort_lab
Finished <<< vision_sort_lab [1.50s]

Summary: 1 package finished [1.75s]
```

Il comando `ros2 pkg prefix vision_sort_lab` ha restituito:

```text
/home/matteo/vision_sort_ws/install/vision_sort_lab
```

La build è riuscita e l'ambiente del secondo terminale trova il pacchetto installato nel workspace corretto. Il fatto che il prompt di quel terminale sia in `/mnt/c/Users/matte` non cambia la ricerca dei pacchetti: dipende dall'ambiente caricato tramite `source`, non dalla directory corrente.

### 6.7 Passo 2B — scrivere joint_monitor.py

Questa sezione conserva la consegna iniziale e lo scheletro con TODO. Il passo è stato completato: correzioni e risultato sono in 6.8–6.9; il listato completo di riferimento è in 6.11.

**Obiettivo:** ricevere `/joint_states`, associare nomi e posizioni, conservare l'ultimo stato e mostrare `panda_joint1` in radianti al massimo una volta al secondo. Il monitor riceve dati dalla demo: non misura un robot fisico.

Una **subscription** collega un nodo a un topic. La **callback** è una funzione chiamata dall'executor quando il messaggio viene elaborato. `rclpy.spin` permette all'executor di gestire questi eventi: non occorre scrivere un ciclo che legga manualmente il topic.

#### Preparare il flusso di dati

Se la demo è stata chiusa, avviarla in un terminale Ubuntu:

```bash
source /opt/ros/jazzy/setup.bash
ros2 launch moveit_resources_panda_moveit_config demo.launch.py
```

In un altro terminale:

```bash
source /opt/ros/jazzy/setup.bash
ros2 topic info /joint_states --verbose
ros2 interface show sensor_msgs/msg/JointState
ros2 topic echo /joint_states --once
```

Controllare che il topic sia presente, il tipo sia `sensor_msgs/msg/JointState`, esista almeno un publisher e un messaggio contenga `panda_joint1`. Il comando `--verbose` mostra anche i profili QoS degli endpoint. Se non arrivano dati, risolvere prima questo problema.

In `JointState`, `name[i]` corrisponde a `position[i]`. La posizione di un giunto rotativo è in radianti, quella di un giunto prismatico in metri. I campi posizione, velocità e sforzo possono essere vuoti; quando valorizzati devono avere dimensione coerente con i nomi. Il monitor di questo esercizio richiede posizioni disponibili: se mancano, salta il messaggio.

Per la subscription usiamo `qos_profile_sensor_data`, un profilo best effort per i dati dei sensori. È adatto a questa lettura dello stato, ma non garantisce di ricevere ogni campione. Limitare i log a una riga al secondo non imposta la frequenza del publisher né quella della callback.

#### Creare il file e completare lo scheletro

```bash
cd ~/vision_sort_ws/src/vision_sort_lab/vision_sort_lab
nano joint_monitor.py
```

Il percorso previsto è `/home/matteo/vision_sort_ws/src/vision_sort_lab/vision_sort_lab/joint_monitor.py`.

**Scheletro didattico incompleto:** Matteo sostituisce i TODO. Con `None` e `pass` non viene creata alcuna subscription e non vengono elaborati dati. Non è una soluzione funzionante già verificata.

```python
import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import JointState


class JointMonitor(Node):
    def __init__(self):
        super().__init__('joint_monitor')
        self.joint_positions = {}
        # TODO 1: sostituire None con la creazione della subscription.
        self.subscription = None

    def joint_state_callback(self, msg: JointState):
        # TODO 2: controllare il messaggio e aggiornare joint_positions.
        # TODO 3: mostrare panda_joint1 con un log limitato a 1 Hz.
        pass


def main(args=None):
    rclpy.init(args=args)
    monitor = JointMonitor()
    try:
        rclpy.spin(monitor)
    except KeyboardInterrupt:
        pass
    finally:
        monitor.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
```

Il costruttore crea il nodo e prepara la subscription. `self.joint_positions` memorizza lo stato per nome. Il `main` inizializza ROS, mantiene il nodo attivo e libera le risorse quando termina. Il blocco finale consente anche l'avvio diretto del modulo Python; in seguito useremo l'eseguibile registrato con ROS.

**TODO 1:** chiamare `self.create_subscription` con questi quattro argomenti, in ordine: `JointState`, `'/joint_states'`, `self.joint_state_callback`, `qos_profile_sensor_data`. Passare la funzione callback senza parentesi: la funzione deve essere eseguita quando arriva il messaggio, non durante la creazione della subscription.

**TODO 2:** se `msg.position` è vuoto, ritornare senza elaborarlo. Se le lunghezze di `msg.name` e `msg.position` differiscono, emettere un warning e ritornare. Altrimenti associare nomi e posizioni in un dizionario e assegnarlo a `self.joint_positions`. Indizio Python: `zip` abbina elementi corrispondenti; il controllo delle lunghezze evita che tronchi silenziosamente dati incoerenti. Il dizionario rappresenta i giunti contenuti nell'ultimo messaggio valido, non una fusione di campioni di tempi diversi.

**TODO 3:** controllare che `panda_joint1` sia presente; poi mostrarne il valore con tre decimali e l'unità `rad`. Un messaggio che non contiene il giunto selezionato può essere saltato. Per il log usare `self.get_logger().info(testo, throttle_duration_sec=1.0)`. Aggiornare il dizionario a ogni messaggio valido, anche quando il log viene saltato dal filtro.

#### Revisione prima dell'avvio

Matteo invia il contenuto del file completato e, se il topic non si comporta come previsto, l'output di `ros2 topic info /joint_states --verbose`. L'assistente rivede prima subscription, callback, gestione dei dati e log.

Nel passo seguente aggiungeremo l'entry point in `setup.py`, rifaremo la build e avvieremo il nodo con `ros2 run`. La verifica sarà osservare il valore aggiornarsi durante un movimento eseguito del Panda, distinguendo l'anteprima della pianificazione dal movimento del controllore.

#### Concetti da spiegare

- Perché `self.joint_state_callback` viene passato senza `()`?
- Perché non possiamo assumere che `msg.position[0]` corrisponda sempre a `panda_joint1`?
- Che differenza c'è tra frequenza di ricezione e frequenza dei log?

### 6.8 Revisione del nodo e chiarimento dello scheletro

Gli import caricano librerie e tipi: non generano la callback del nostro programma. `JointMonitor` eredita da `Node` i metodi ROS, come `create_subscription` e `get_logger`. `super().__init__('joint_monitor')` inizializza la parte ROS dell'oggetto. `self` indica l'istanza corrente; `msg: JointState` descrive il tipo previsto del parametro e non costruisce un messaggio.

Nel `main`, `rclpy.init` inizializza ROS, `JointMonitor()` costruisce il nodo e `rclpy.spin` elabora gli eventi, chiamando la callback quando un messaggio viene elaborato. Alla chiusura, `finally` libera il nodo e termina il contesto ROS.

Il primo tentativo di Matteo aveva una subscription corretta. Abbiamo poi corretto:

- **Sintassi della stringa:** la chiamata a `print` conteneva una stringa non chiusa. Scrivere una chiamata al logger fra virgolette la rende testo, non codice da eseguire.
- **Chiamata al metodo:** `self.get_logger()` restituisce il logger su cui chiamare `warning` e `info`. Alla subscription passiamo invece `self.joint_state_callback` senza parentesi, per registrare la funzione da chiamare in futuro.
- **Nomi:** il campo del messaggio è `msg.position`; il nostro attributo è `self.joint_positions`. `msg.positions` non esiste; `self.joint_position` creerebbe un attributo diverso da quello inizializzato.
- **Dati:** `zip` produce coppie; `dict(zip(msg.name, msg.position))` costruisce la mappa per nome. Controllare prima le lunghezze evita un troncamento silenzioso.
- **Iterazione:** `len(msg.name)` restituisce un intero e non è direttamente iterabile. Per cercare un giunto nel dizionario basta controllare la sua chiave.
- **Blocchi Python:** il `TabError` è stato risolto usando spazi coerenti. Python delimita i blocchi tramite indentazione; le graffe attorno a `warning` e `return` erano da eliminare. Le graffe delle f-string restano corrette.
- **Uscita dalla callback:** basta `return`, senza un codice numerico. Il `pass` dello scheletro era un segnaposto e può essere eliminato dopo l'implementazione.

La callback corretta studiata insieme è:

```python
    def joint_state_callback(self, msg: JointState):
        if not msg.position:
            return

        if len(msg.name) != len(msg.position):
            self.get_logger().warning(
                'Nomi e posizioni hanno lunghezze diverse'
            )
            return

        self.joint_positions = dict(zip(msg.name, msg.position))

        if 'panda_joint1' in self.joint_positions:
            valore = self.joint_positions['panda_joint1']
            testo = f'panda_joint1 = {valore:.3f} rad'
            self.get_logger().info(testo, throttle_duration_sec=1.0)
```

Il metodo rimane dentro la classe: quattro spazi prima di `def`, otto per il corpo del metodo e dodici per il corpo degli `if`. Il costruttore registra una sola callback: il riferimento passato a `create_subscription` e la definizione del metodo sono due parti della stessa connessione, non due callback da scegliere.

### 6.9 Registrazione, build e risultato verificato

In `setup.py` è stata indicata questa registrazione nella sezione `entry_points` esistente, senza duplicarla:

```python
entry_points={
    'console_scripts': [
        'joint_monitor = vision_sort_lab.joint_monitor:main',
    ],
},
```

Prima di `=` c'è il nome del comando; dopo c'è il modulo Python e, dopo `:`, la funzione da avviare. Il `main` dello scheletro deve rimanere nel modulo.

Matteo ha confermato il superamento di `python3 -m py_compile`. Questo verifica la sintassi, non gli attributi ROS o il comportamento della callback. Dopo la build e l'avvio con `ros2 run`, ha fornito log del nodo circa una volta al secondo:

```text
[INFO] [1791497142.883920156] [joint_monitor]: panda_joint1 = 0.000 rad
[INFO] [1791497143.884354014] [joint_monitor]: panda_joint1 = 0.000 rad
```

Un valore costante di un singolo giunto può indicare un robot fermo oppure un movimento degli altri giunti. Per osservare lo stato completo abbiamo sostituito temporaneamente la sola riga del testo con:

```python
testo = str(self.joint_positions)
```

Il logger mantiene il filtro di un secondo. Il dizionario viene aggiornato a ogni messaggio valido, anche quando la stampa viene saltata. Dopo il riavvio del monitor e la prova con Plan ed Execute, Matteo ha confermato che i cambiamenti dei giunti sono osservabili.

**Risultato: nodo scritto dall'utente, avvio riuscito e osservazione del movimento confermata.** Le verifiche sono state eseguite da Matteo nel proprio ambiente; l'assistente ha rivisto il codice incollato e gli output. La demo usa controllori simulati: la fisica della presa in Gazebo resta da verificare.

La programmazione del primo movimento è stata completata nella sezione 7. La prossima fase immediata sarà la verifica automatica della configurazione raggiunta; seguiranno gestione degli errori, scena, simulazione fisica, prelievo, telecamera e smistamento.

### 6.10 Comandi Bash per ripetere la demo e le verifiche

I comandi seguenti vanno eseguiti in **Ubuntu WSL**, con ROS, MoveIt e il pacchetto del progetto già installati. La guida resta nel suo percorso Windows. I terminali sono separati perché demo e monitor sono processi che devono restare attivi contemporaneamente.

#### Terminale 1 — Panda e RViz

```bash
source /opt/ros/jazzy/setup.bash
ros2 launch moveit_resources_panda_moveit_config demo.launch.py
```

Lasciare il terminale aperto. La demo apre già RViz. Selezionare `panda_arm`, usare lo stato corrente come partenza, abilitare **Displays → MotionPlanning → Planning Request → Query Goal State**, scegliere **Interact**, spostare il marker e premere **Plan → Execute**. Questi passaggi sono manuali: l'anteprima non modifica lo stato corrente del robot.

#### Terminale 2 — monitor dei giunti

```bash
source /opt/ros/jazzy/setup.bash
source ~/vision_sort_ws/install/local_setup.bash
ros2 run vision_sort_lab joint_monitor
```

Lasciare il processo attivo e osservare i valori durante il movimento eseguito. I comandi `source` valgono soltanto per il terminale corrente.

#### Terminale 3 — ispezione

```bash
source /opt/ros/jazzy/setup.bash
source ~/vision_sort_ws/install/local_setup.bash

# Pacchetto ed eseguibile
ros2 pkg prefix vision_sort_lab
ros2 pkg executables vision_sort_lab

# Nodi
ros2 node list
ros2 node info /joint_monitor

# Topic, profili QoS e definizione del messaggio
ros2 topic list
ros2 topic info /joint_states --verbose
ros2 interface show sensor_msgs/msg/JointState

# Ricevere un messaggio e terminare
ros2 topic echo /joint_states --once
```

Il prefisso atteso è `/home/matteo/vision_sort_ws/install/vision_sort_lab`; la lista degli eseguibili deve contenere `vision_sort_lab joint_monitor`.

#### Dopo modifiche — sintassi e build

Aprire un nuovo terminale dedicato alla build, caricando soltanto ROS di base, senza caricare prima l'overlay che si sta ricostruendo:

```bash
source /opt/ros/jazzy/setup.bash

python3 -m py_compile \
  ~/vision_sort_ws/src/vision_sort_lab/vision_sort_lab/joint_monitor.py
```

Solo se il controllo termina senza errori, proseguire:

```bash
cd ~/vision_sort_ws
colcon build --symlink-install --packages-select vision_sort_lab
```

Dopo la build, avviare il monitor in un altro terminale usando i comandi del terminale 2. Con `--symlink-install`, una modifica al modulo Python normalmente viene letta al riavvio del nodo; modifiche a entry point e metadati richiedono una nuova build.

#### Apertura e lettura dei file

```bash
nano ~/vision_sort_ws/src/vision_sort_lab/vision_sort_lab/joint_monitor.py
nano ~/vision_sort_ws/src/vision_sort_lab/setup.py
nano ~/vision_sort_ws/src/vision_sort_lab/package.xml

# Mostrare il codice senza il troncamento delle righe di nano
cat ~/vision_sort_ws/src/vision_sort_lab/vision_sort_lab/joint_monitor.py
```

In nano: `Ctrl+O` e Invio per salvare, `Ctrl+X` per uscire. Usare spazi per l'indentazione Python.

#### Arresto e ripetizione

Premere `Ctrl+C` nel terminale del monitor e in quello della demo. Per ripetere la prova, rilanciare i comandi dei terminali 1 e 2. Non serve reinstallare i pacchetti o rifare la build a ogni avvio.

### 6.11 joint_monitor.py completo di riferimento

Il listato seguente riunisce lo scheletro e la callback corretta studiati nella sezione 6. Mostra `panda_joint1` a circa 1 Hz; per stampare l'intero dizionario si può sostituire la costruzione di `testo` con `testo = str(self.joint_positions)`, come nella prova eseguita da Matteo.

**Codice completo di riferimento ricostruito dalla revisione, non copia del file attuale in WSL.** Il comportamento di ricezione e osservazione del movimento è stato verificato dall'utente. Il `main` conserva la gestione della chiusura anche se la creazione del nodo non termina.

```python
import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import JointState


class JointMonitor(Node):
    def __init__(self):
        super().__init__('joint_monitor')
        self.joint_positions = {}

        # Registra il metodo; sarà l'executor a chiamarlo sui messaggi ricevuti.
        self.subscription = self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_state_callback,
            qos_profile_sensor_data,
        )

    def joint_state_callback(self, msg: JointState):
        if not msg.position:
            return

        if len(msg.name) != len(msg.position):
            self.get_logger().warning(
                'Nomi e posizioni hanno lunghezze diverse'
            )
            return

        # Associa le posizioni ai nomi; non assume un ordine fisso.
        self.joint_positions = dict(zip(msg.name, msg.position))

        if 'panda_joint1' in self.joint_positions:
            valore = self.joint_positions['panda_joint1']
            testo = f'panda_joint1 = {valore:.3f} rad'
            self.get_logger().info(testo, throttle_duration_sec=1.0)


def main(args=None):
    rclpy.init(args=args)
    monitor = None

    try:
        monitor = JointMonitor()
        rclpy.spin(monitor)
    except KeyboardInterrupt:
        pass
    finally:
        if monitor is not None:
            monitor.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
```

Il dizionario appartiene a questo nodo. `motion_commander` non accede automaticamente a `self.joint_positions` di un altro processo: la futura verifica dovrà ricevere i messaggi tramite una propria subscription o un'interfaccia progettata appositamente.

## 7. Esercizio 3 — movimento programmato con MoveIt 2

**Stato: completato e verificato da Matteo nella demo RViz con hardware mock/simulato.** Il nodo ha pianificato ed eseguito un movimento verso `ready`; sono stati osservati accettazione, feedback, risultato positivo e movimento del Panda.

### 7.1 Obiettivo e architettura

Passare dal comando manuale tramite RViz a un nostro programma, comprendendo la separazione fra pianificazione, esecuzione e risultato.

```text
motion_commander, scritto in Python con rclpy
  |
  +-- servizio /plan_kinematic_path --> move_group
  |       richiesta: stato iniziale, gruppo e obiettivo
  |       risposta: codice MoveIt e traiettoria
  |
  +-- action /execute_trajectory --> move_group --> controllori della demo
          goal: traiettoria già calcolata
          risposta iniziale: accettazione o rifiuto
          feedback: stato dell'operazione
          risultato finale: stato ROS e codice MoveIt

/joint_states --> joint_monitor
                  osservazione delle posizioni dei giunti
```

Il nodo Python organizza il compito. Il pianificatore è configurato nella demo, mentre i controllori eseguono la traiettoria sul modello simulato. Non pubblichiamo manualmente posizioni sul topic `/joint_states` e non sostituiamo i controllori.

**Criteri raggiunti:** una richiesta di pianificazione produce una traiettoria valida; questa viene inviata all'action; il server accetta il goal; il nodo riceve feedback e risultato finale; Matteo osserva il movimento.

### 7.2 Scoprire servizi, action e messaggi

Con la demo avviata, eseguire in un terminale Ubuntu:

```bash
source /opt/ros/jazzy/setup.bash
source /home/matteo/vision_sort_ws/install/setup.bash

ros2 service list -t
ros2 action list -t
ros2 interface show moveit_msgs/srv/GetMotionPlan
ros2 interface show moveit_msgs/action/ExecuteTrajectory
```

Interfacce individuate e confermate dall'utente:

| Nome | Tipo | Ruolo |
|---|---|---|
| `/plan_kinematic_path` | `moveit_msgs/srv/GetMotionPlan` | Calcolare una traiettoria |
| `/execute_trajectory` | `moveit_msgs/action/ExecuteTrajectory` | Eseguire una traiettoria |
| `/joint_states` | `sensor_msgs/msg/JointState` | Ricevere gli stati articolari |

Nel servizio, `---` separa richiesta e risposta. Nell'action i due separatori dividono goal, risultato e feedback. Per studiare i messaggi interni:

```bash
ros2 interface show moveit_msgs/msg/MotionPlanRequest
ros2 interface show moveit_msgs/msg/MotionPlanResponse
ros2 interface show moveit_msgs/msg/Constraints
ros2 interface show moveit_msgs/msg/JointConstraint
ros2 interface show moveit_msgs/msg/MoveItErrorCodes
ros2 interface show action_msgs/msg/GoalStatus
```

Il comando locale mostra i campi della versione installata. Gli esempi online possono avere campi aggiuntivi o differenze: non si modifica il codice affidandosi soltanto al ramo `main`.

### 7.3 Perché un servizio e un'action

Un servizio descrive un'interazione richiesta–risposta. Nel nostro esercizio chiediamo un piano e attendiamo la risposta senza richiedere feedback intermedi del calcolo.

Un'action gestisce un obiettivo nel tempo, distinguendo accettazione, feedback e risultato finale, con un meccanismo per richiedere la cancellazione. Questo è utile per seguire l'esecuzione.

La scelta riguarda l'interazione, non la presenza di hardware. Anche il calcolo di un piano può essere esposto come action: MoveIt offre `MoveGroup` con l'opzione `plan_only`. Il servizio scelto qui mantiene esplicita la separazione fra i due passi. Fonte: [modello delle action ROS 2](https://design.ros2.org/articles/actions.html).

La sola richiesta `GetMotionPlan` non muove il robot. Un piano riuscito non garantisce che la successiva esecuzione riesca.

Il feedback di un'action non garantisce tempi di risposta deterministici e non costituisce da solo una protezione dell'hardware. Una richiesta di cancellazione deve essere elaborata dal server. Nel progetto attuale cancellazione e recupero non sono ancora implementati.

### 7.4 Ricavare l'obiettivo dall'SRDF

La configurazione `ready` è stata letta dalla configurazione locale, non scelta con valori arbitrari:

```bash
ros2 param get /move_group robot_description_semantic
```

Nel contenuto restituito, Matteo ha individuato:

```xml
<group_state group="panda_arm" name="ready">
  <joint name="panda_joint1" value="0"/>
  <joint name="panda_joint2" value="-0.785"/>
  <joint name="panda_joint3" value="0"/>
  <joint name="panda_joint4" value="-2.356"/>
  <joint name="panda_joint5" value="0"/>
  <joint name="panda_joint6" value="1.571"/>
  <joint name="panda_joint7" value="0.785"/>
</group_state>
```

Le posizioni dei sette giunti rotativi sono in radianti. Nel dizionario Python gli zeri sono scritti come `0.0`: i campi delle posizioni sono in virgola mobile e i messaggi Python ROS applicano controlli sui tipi.

Sono presenti anche gli stati nominati `extended` e `transport`. La loro presenza nell'SRDF non è una verifica della raggiungibilità o dell'assenza di collisioni nella scena corrente: ogni richiesta deve passare dalla pianificazione.

`goal.name = 'joint_goal'` è un'etichetta del messaggio `Constraints`. Non carica uno stato nominato dell'SRDF. Il nostro programma usa esplicitamente il dizionario delle posizioni di `ready`.

### 7.5 File, dipendenze ed entry point

Il modulo studiato è:

```text
/home/matteo/vision_sort_ws/src/vision_sort_lab/vision_sort_lab/motion_commander.py
```

In `package.xml` mantenere le dipendenze già presenti. Aggiungere, solo se assenti:

```xml
<exec_depend>moveit_msgs</exec_depend>
<exec_depend>action_msgs</exec_depend>
```

`rclpy` è usato da entrambi i nodi; `sensor_msgs` dal monitor; `moveit_msgs` contiene le interfacce MoveIt; `action_msgs` contiene `GoalStatus`. Non servono gli import QoS del monitor nel nodo di comando, che per ora non ha una subscription a `/joint_states`.

Dentro la chiamata `setup(...)` di `setup.py`, la sezione esistente deve contenere entrambi gli eseguibili:

```python
entry_points={
    'console_scripts': [
        'joint_monitor = vision_sort_lab.joint_monitor:main',
        'motion_commander = vision_sort_lab.motion_commander:main',
    ],
},
```

Questo è un frammento di configurazione da inserire nella chiamata `setup`, non uno script Python indipendente. Non duplicare `entry_points`. Il nome a sinistra diventa il comando per `ros2 run`; il modulo e `main` a destra indicano cosa avviare.

### 7.6 motion_commander.py completo e commentato

**Listato completo di riferimento, ricostruito dai tentativi e dalle correzioni discussi nella chat.** La prova ROS ha verificato il percorso positivo del codice scritto da Matteo. Questo listato riunisce i pezzi con rientri, nomi e gestione delle eccezioni uniformati; non è stato copiato dal file Ubuntu né rieseguito contro ROS durante l'aggiornamento della guida. Gli attributi dei Future e del goal handle sono inizializzati a `None` per rendere leggibile lo stato iniziale.

**Comportamento all'avvio:** appena le interfacce sono disponibili, il nodo richiede un piano verso `ready` e, se il piano riesce, ne richiede automaticamente l'esecuzione nella demo. Il nodo resta poi in `spin` fino alla chiusura; non ripete il movimento in un ciclo.

```python
import rclpy
from action_msgs.msg import GoalStatus
from moveit_msgs.action import ExecuteTrajectory
from moveit_msgs.msg import Constraints, JointConstraint, MoveItErrorCodes
from moveit_msgs.srv import GetMotionPlan
from rclpy.action import ActionClient
from rclpy.node import Node


class MotionCommander(Node):
    def __init__(self):
        super().__init__('motion_commander')

        self.plan_client = self.create_client(
            GetMotionPlan,
            '/plan_kinematic_path',
        )
        self.execute_client = ActionClient(
            self,
            ExecuteTrajectory,
            '/execute_trajectory',
        )

        # Nessun piano o goal attivo è ancora stato ottenuto.
        self.planned_trajectory = None
        self.plan_future = None
        self.execute_goal_future = None
        self.execute_goal_handle = None
        self.execute_result_future = None

        # True significa disponibile: ripetiamo l'attesa quando è False.
        while rclpy.ok() and not self.plan_client.wait_for_service(
            timeout_sec=1.0
        ):
            self.get_logger().info(
                'In attesa del servizio di pianificazione…'
            )

        if not rclpy.ok():
            return
        self.get_logger().info('Servizio di pianificazione disponibile')

        while rclpy.ok() and not self.execute_client.wait_for_server(
            timeout_sec=1.0
        ):
            self.get_logger().info(
                "In attesa dell'action di esecuzione…"
            )

        if not rclpy.ok():
            return
        self.get_logger().info('Action di esecuzione disponibile')

        # Valori ricavati dallo stato ready dell'SRDF locale.
        self.target_positions = {
            'panda_joint1': 0.0,
            'panda_joint2': -0.785,
            'panda_joint3': 0.0,
            'panda_joint4': -2.356,
            'panda_joint5': 0.0,
            'panda_joint6': 1.571,
            'panda_joint7': 0.785,
        }

        # Invia una richiesta. La risposta verrà elaborata durante spin().
        self.request_plan(self.target_positions)

    def build_goal_constraints(self, target_positions):
        goal = Constraints()
        goal.name = 'joint_goal'

        for joint_name, position in target_positions.items():
            # Ogni giunto deve avere un proprio oggetto vincolo.
            constraint = JointConstraint()
            constraint.joint_name = joint_name
            constraint.position = position
            constraint.tolerance_above = 0.01
            constraint.tolerance_below = 0.01
            constraint.weight = 1.0
            goal.joint_constraints.append(constraint)

        return goal

    def build_plan_request(self, target_positions):
        # Crea il contenitore del servizio: non invia ancora nulla.
        request = GetMotionPlan.Request()

        # Riferimento al messaggio interno, non una copia.
        plan = request.motion_plan_request
        plan.group_name = 'panda_arm'
        plan.num_planning_attempts = 1
        plan.allowed_planning_time = 5.0
        plan.max_velocity_scaling_factor = 0.2
        plan.max_acceleration_scaling_factor = 0.2

        # Aggiornamento parziale, senza posizioni iniziali alternative:
        # MoveIt usa lo stato corrente che sta monitorando.
        plan.start_state.is_diff = True

        # Una sola regione obiettivo, con sette vincoli simultanei.
        plan.goal_constraints = [
            self.build_goal_constraints(target_positions)
        ]
        return request

    def request_plan(self, target_positions):
        request = self.build_plan_request(target_positions)
        self.plan_future = self.plan_client.call_async(request)
        self.get_logger().info('Richiesta di pianificazione inviata')

        # Passa il metodo senza (): verrà chiamato sul Future completato.
        self.plan_future.add_done_callback(self.on_plan_response)

    def on_plan_response(self, future):
        try:
            response = future.result()
        except Exception as exc:
            self.get_logger().error(
                f'Errore nel recupero della risposta: {exc}'
            )
            return

        result = response.motion_plan_response
        if result.error_code.val == MoveItErrorCodes.SUCCESS:
            self.planned_trajectory = result.trajectory
            self.get_logger().info(
                f'Pianificazione riuscita in '
                f'{result.planning_time:.3f} secondi'
            )
            num_points = len(result.trajectory.joint_trajectory.points)
            self.get_logger().info(
                f'La traiettoria contiene {num_points} punti'
            )

            # Il piano è arrivato: ora possiamo costruire il goal.
            self.request_execution()
        else:
            self.planned_trajectory = None
            self.get_logger().error(
                f'Pianificazione fallita, codice MoveIt: '
                f'{result.error_code.val}'
            )

    def build_execution_goal(self):
        if self.planned_trajectory is None:
            self.get_logger().error(
                'Nessuna traiettoria disponibile per l’esecuzione'
            )
            return None

        if not self.planned_trajectory.joint_trajectory.points:
            self.get_logger().error(
                'La traiettoria non contiene punti da eseguire'
            )
            return None

        goal = ExecuteTrajectory.Goal()
        goal.trajectory = self.planned_trajectory
        return goal

    def request_execution(self):
        goal = self.build_execution_goal()
        if goal is None:
            return

        # Il Future riguarda l'accettazione; il feedback ha un'altra callback.
        self.execute_goal_future = self.execute_client.send_goal_async(
            goal,
            feedback_callback=self.on_execution_feedback,
        )
        self.execute_goal_future.add_done_callback(
            self.on_execution_goal_response
        )
        self.get_logger().info('Goal di esecuzione inviato')

    def on_execution_goal_response(self, future):
        try:
            goal_handle = future.result()
        except Exception as exc:
            self.get_logger().error(
                f'Errore nella risposta al goal di esecuzione: {exc}'
            )
            return

        if not goal_handle.accepted:
            self.get_logger().error('Goal di esecuzione rifiutato')
            return

        self.execute_goal_handle = goal_handle
        self.get_logger().info('Goal di esecuzione accettato')

        # Richiede l'esito del goal già accettato, non un nuovo movimento.
        self.execute_result_future = goal_handle.get_result_async()
        self.execute_result_future.add_done_callback(
            self.on_execution_result
        )

    def on_execution_feedback(self, feedback_msg):
        state = feedback_msg.feedback.state
        self.get_logger().info(f'Stato esecuzione: {state}')

    def on_execution_result(self, future):
        try:
            response = future.result()
        except Exception as exc:
            self.get_logger().error(
                f'Errore nel recupero del risultato di esecuzione: {exc}'
            )
            return

        # Lo stato ROS e il codice MoveIt sono informazioni differenti.
        status = response.status
        error_code = response.result.error_code.val

        if (
            status == GoalStatus.STATUS_SUCCEEDED
            and error_code == MoveItErrorCodes.SUCCESS
        ):
            self.get_logger().info(
                'Esecuzione completata con successo'
            )
        else:
            self.get_logger().error(
                f'Esecuzione non riuscita: status ROS={status}, '
                f'codice MoveIt={error_code}'
            )


def main(args=None):
    rclpy.init(args=args)
    commander = None

    try:
        # Anche le attese nel costruttore sono dentro il try.
        commander = MotionCommander()
        rclpy.spin(commander)
    except KeyboardInterrupt:
        pass
    finally:
        if commander is not None:
            commander.destroy_node()
        # Si chiude il contesto anche se il costruttore non è terminato.
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
```

### 7.7 Costruttore, attese e main

`super().__init__('motion_commander')` inizializza il nodo ROS. `create_client` crea il client del servizio; `ActionClient(self, tipo, nome)` crea quello dell'action associandolo esplicitamente al nodo.

`wait_for_service(timeout_sec=1.0)` e `wait_for_server(timeout_sec=1.0)` verificano la disponibilità dell'interfaccia. Ritornano `True` quando è disponibile, `False` allo scadere del tentativo. Nel ciclo occorre quindi `not`. `rclpy.ok()` permette di uscire se il contesto viene chiuso.

Il secondo non è un timeout globale: ogni tentativo dura fino a circa un secondo e il ciclo può ripetersi finché ROS resta attivo. La disponibilità del servizio non garantisce che un obiettivo sia pianificabile; la disponibilità dell'action non garantisce che il goal sarà accettato.

In questo primo nodo le attese sono nel costruttore perché non deve ancora elaborare altri dati durante quella fase. Con subscription, verifiche e sequenze più articolate studieremo inizializzazione e attese senza bloccare le altre attività.

Il `main` inizializza ROS, costruisce il nodo ed entra in `rclpy.spin`, che consente all'executor di elaborare risposte e callback. `commander = None` distingue il caso in cui il costruttore non termina. La costruzione va dentro il `try` per gestire Ctrl+C anche durante l'attesa. `try_shutdown` deve stare fuori dall'`if commander is not None`.

Chiudere il nodo o il contesto ROS non è un'implementazione della cancellazione del goal. Il nostro codice non invia una richiesta di arresto tramite l'action quando si preme Ctrl+C; la futura cancellazione avrà un percorso esplicito.

### 7.8 Costruire dati: vincoli e richiesta di piano

`build_goal_constraints(target_positions)` crea un contenitore `Constraints` e un `JointConstraint` distinto per ogni giunto. Il ciclo `for joint_name, position in target_positions.items()` legge coppie nome–posizione. `append` aggiunge ciascun vincolo alla lista.

Tutti i vincoli nello stesso contenitore devono essere soddisfatti insieme. Con `position = 0.5` e tolleranze `0.01`, il giunto deve arrivare nell'intervallo `[0.49, 0.51]` radianti. `weight` esprime l'importanza relativa del vincolo; non è un guadagno del controllore.

Queste sono **tolleranze dell'obiettivo di pianificazione**. Non impostano automaticamente le tolleranze del controllore durante l'esecuzione e non svolgono il confronto finale con `/joint_states`. La prossima verifica dovrà definire il proprio criterio.

`build_plan_request` crea il messaggio esterno e recupera il messaggio interno:

```python
request = GetMotionPlan.Request()
plan = request.motion_plan_request
```

`GetMotionPlan.Request()` costruisce un oggetto; non effettua una chiamata ROS. `request` è una variabile locale. Scrivere `self.request` conserverebbe invece l'oggetto come attributo del nodo: sarebbe valido, ma richiederebbe usare quel nome coerentemente. Il nostro metodo restituisce l'oggetto, quindi non ha bisogno di conservarlo in `self`.

`plan` è un riferimento al messaggio interno, non una copia. Modificare `plan.group_name` modifica il campo interno di `request`. Il nome `plan` qui non rappresenta ancora una traiettoria calcolata.

| Campo | Valore scelto | Interpretazione |
|---|---|---|
| `group_name` | `panda_arm` | Gruppo articolare |
| `num_planning_attempts` | `1` | Tentativi richiesti |
| `allowed_planning_time` | `5.0` | Tempo concesso al calcolo, non durata del movimento |
| `max_velocity_scaling_factor` | `0.2` | Scala i limiti massimi di velocità |
| `max_acceleration_scaling_factor` | `0.2` | Scala i limiti massimi di accelerazione |
| `start_state.is_diff` | `True` | Stato iniziale come aggiornamento parziale |
| `goal_constraints` | Lista con un contenitore | Una regione obiettivo |

Lo stato iniziale non contiene posizioni alternative: `move_group` usa lo stato corrente monitorato nella demo. `is_diff` indica un aggiornamento parziale; non è una subscription e non sostituisce il monitor dello stato di MoveIt.

I fattori di scala sono nell'intervallo `(0, 1]`. `0.2` non impone una velocità costante. `0.0` non significa “fermo”: secondo la definizione del messaggio viene trattato come valore non valido e ricondotto al valore predefinito. Fonte: [MotionPlanRequest](https://github.com/moveit/moveit_msgs/blob/ros2/msg/MotionPlanRequest.msg).

`goal_constraints` è una lista di regioni alternative: ne basta una soddisfatta. Noi inseriamo un solo contenitore con tutti i sette vincoli, non sette contenitori alternativi:

```python
plan.goal_constraints = [
    self.build_goal_constraints(target_positions)
]
```

### 7.9 Richiesta asincrona e risposta di pianificazione

`request_plan` costruisce il messaggio e lo invia con `call_async`. La chiamata restituisce un `Future` e il programma prosegue. Non restituisce immediatamente il piano, non aspetta il termine del calcolo e non significa che il nostro codice abbia creato un nuovo thread.

```python
self.plan_future = self.plan_client.call_async(request)
self.plan_future.add_done_callback(self.on_plan_response)
```

`add_done_callback` registra cosa fare al completamento del Future. Passiamo `self.on_plan_response` senza parentesi; scrivere `self.on_plan_response(...)` eseguirebbe subito il metodo. Alla callback viene passato il Future; `self` è già associato all'istanza. Se il Future è già completo al momento della registrazione, la callback viene comunque gestita.

Quando `on_plan_response` viene chiamato, il Future è completato. `future.result()` recupera il risultato oppure solleva l'eccezione memorizzata. Non è una nuova richiesta a MoveIt. In `rclpy` non va usato come attesa bloccante prima del completamento: può restituire `None` se il risultato non è ancora disponibile. Fonte: [Future in rclpy Jazzy](https://github.com/ros2/rclpy/blob/jazzy/rclpy/rclpy/task.py).

```text
request_plan() invia la richiesta
  -> il costruttore termina
  -> main() entra in spin()
  -> la risposta viene elaborata
  -> il Future si completa
  -> on_plan_response(future) legge il risultato
```

#### try/except, exc e return

```python
try:
    response = future.result()
except Exception as exc:
    self.get_logger().error(f'Errore: {exc}')
    return
```

Python prova la riga nel `try`. Se solleva un'eccezione compatibile, passa al blocco `except` e rende l'oggetto eccezione disponibile con il nome `exc`. Non viene “inviata una exc”. La f-string inserisce nel messaggio la sua descrizione.

`return` termina questa callback, non tutto il nodo. Senza il `return`, il codice potrebbe proseguire senza una `response` valida. Se non c'è eccezione, l'`except` viene saltato.

Il risultato robotico è una verifica distinta:

```python
result = response.motion_plan_response
if result.error_code.val == MoveItErrorCodes.SUCCESS:
    self.planned_trajectory = result.trajectory
```

Una pianificazione fallita normalmente arriva come risposta valida con un codice MoveIt negativo: non fa scattare automaticamente l'`except`. Il confronto col codice positivo è necessario prima di conservare ed eseguire il piano. Il numero di punti si ottiene da `len(result.trajectory.joint_trajectory.points)`.

`self.request_execution()` è chiamato soltanto nel ramo di successo, dopo aver ottenuto la traiettoria. Chiamarlo nel costruttore, subito dopo `request_plan`, anticiperebbe la risposta asincrona.

### 7.10 Costruire e inviare il goal di esecuzione

`build_execution_goal` controlla che `self.planned_trajectory` non sia `None` e che la lista dei punti non sia vuota. In caso di errore restituisce `None`; altrimenti crea `ExecuteTrajectory.Goal()`, assegna la traiettoria e **restituisce il goal**.

```python
goal = ExecuteTrajectory.Goal()
goal.trajectory = self.planned_trajectory
return goal
```

Qui passa la traiettoria già calcolata, non il dizionario obiettivo. Creare il goal non muove il robot; inviarlo all'action può avviare l'esecuzione appena viene accettato.

`request_execution` chiama `self.build_execution_goal()`. Senza `self.` Python cercherebbe una funzione separata con quel nome. Il controllo `if goal is None: return` impedisce di inviare un valore mancante.

```python
self.execute_goal_future = self.execute_client.send_goal_async(
    goal,
    feedback_callback=self.on_execution_feedback,
)
```

Questo Future contiene la risposta di accettazione o rifiuto del goal, non il risultato finale. Il parametro `feedback_callback` registra invece il metodo che elabora i feedback. Fonte: [ActionClient in rclpy Jazzy](https://github.com/ros2/rclpy/blob/jazzy/rclpy/rclpy/action/client.py).

### 7.11 Accettazione, feedback e risultato finale

`on_execution_goal_response` recupera un `ClientGoalHandle` con `future.result()` e controlla `goal_handle.accepted`. Il goal handle identifica il goal e fornisce operazioni per seguirlo. Un goal rifiutato non deve passare al percorso di esecuzione riuscita.

Se accettato, lo conserviamo in `self.execute_goal_handle` e richiediamo il risultato:

```python
self.execute_result_future = goal_handle.get_result_async()
self.execute_result_future.add_done_callback(self.on_execution_result)
```

`get_result_async` richiede l'esito dello stesso goal. Non pianifica e non avvia un secondo movimento. Il suo Future si completa quando il risultato è disponibile.

`on_execution_feedback` riceve un contenitore che include il feedback specifico dell'action:

```python
state = feedback_msg.feedback.state
```

`state` è una stringa sullo stato interno dell'operazione. Nel nostro log compare `MONITOR`. Non contiene automaticamente angoli, distanze dagli ostacoli, percentuale completata o errore di inseguimento: i dati dei giunti arrivano tramite `/joint_states`.

`on_execution_result` recupera due livelli di informazione:

| Espressione | Significato |
|---|---|
| `response.status` | Stato finale dell'action ROS |
| `response.result.error_code.val` | Codice di risultato MoveIt |

`GoalStatus.STATUS_SUCCEEDED` vale `4`; `STATUS_CANCELED` vale `5`; `STATUS_ABORTED` vale `6`. `MoveItErrorCodes.SUCCESS` vale `1`. Sono codici di sistemi differenti, perciò si confrontano con le rispettive costanti, non fra loro.

Il successo richiede entrambi i confronti positivi. Nel ramo negativo il nostro nodo registra stato e codice: non riprova, non cancella e non ripianifica automaticamente.

Per orientarsi nei messaggi:

| Oggetto | Cosa contiene |
|---|---|
| `request` | Richiesta da inviare al servizio |
| `plan` in `build_plan_request` | Messaggio interno della richiesta |
| `self.plan_future` | Esito futuro della chiamata al servizio |
| `response.motion_plan_response` | Risultato della pianificazione |
| `self.planned_trajectory` | Traiettoria ottenuta |
| `goal` | Messaggio per richiedere l'esecuzione |
| `self.execute_goal_future` | Risposta di accettazione o rifiuto |
| `self.execute_goal_handle` | Riferimento al goal accettato |
| `self.execute_result_future` | Risultato finale futuro |
| `feedback_msg.feedback` | Feedback specifico di MoveIt |

L'arrivo dei feedback è asincrono: frequenza e interleaving dei log dipendono dal server e dall'elaborazione degli eventi. I callback di feedback non sostituiscono il controllo del risultato finale.

### 7.12 Comandi per build, avvio e prima prova

I comandi di questa sezione vanno eseguiti in **Ubuntu WSL**, perché il codice ROS si trova nel workspace Linux. Il documento che contiene questi comandi resta su Windows.

#### Terminale per sintassi e build

Usare un nuovo terminale con il solo ambiente base ROS:

```bash
source /opt/ros/jazzy/setup.bash
python3 -m py_compile \
  /home/matteo/vision_sort_ws/src/vision_sort_lab/vision_sort_lab/joint_monitor.py \
  /home/matteo/vision_sort_ws/src/vision_sort_lab/vision_sort_lab/motion_commander.py
```

Se il controllo sintattico termina senza errori:

```bash
cd /home/matteo/vision_sort_ws
colcon build --packages-select vision_sort_lab --symlink-install
```

`py_compile` verifica la sintassi, non il successo delle chiamate ROS. Procedere alla build soltanto se termina senza errori; procedere all'avvio soltanto se la build riesce.

#### Terminale 1 — demo

```bash
source /opt/ros/jazzy/setup.bash
ros2 launch moveit_resources_panda_moveit_config demo.launch.py
```

#### Terminale 2 — monitor

```bash
source /opt/ros/jazzy/setup.bash
source /home/matteo/vision_sort_ws/install/setup.bash
ros2 run vision_sort_lab joint_monitor
```

Per osservare tutti i giunti durante la prova, usare la variante del testo descritta in 6.9.

#### Terminale 3 — comando del movimento

```bash
source /opt/ros/jazzy/setup.bash
source /home/matteo/vision_sort_ws/install/setup.bash
ros2 run vision_sort_lab motion_commander
```

Prima dell'avvio, si può portare il robot da RViz in una configurazione valida diversa da `ready` tramite Plan & Execute. Il nostro nodo poi pianifica nuovamente dallo stato corrente. Se è già in `ready`, il movimento può essere minimo.

Durante la prova lasciare al nostro nodo la sequenza di comando. Cambiare lo stato da RViz dopo il calcolo del piano può rendere il piano incoerente con la partenza effettiva.

Il nodo rimane attivo dopo il risultato finale. Per ripetere l'esercizio chiuderlo e rilanciarlo; per applicare modifiche Python occorre almeno salvare e riavviare il processo. Metadati ed entry point richiedono build e caricamento dell'ambiente aggiornato.

#### Output effettivamente comunicato da Matteo

```text
[INFO] [1791829005.041921337] [motion_commander]: Servizio di pianificazione disponibile
[INFO] [1791829005.042465832] [motion_commander]: Action di esecuzione disponibile
[INFO] [1791829005.043006776] [motion_commander]: Richiesta di pianificazione inviata
[INFO] [1791829005.076750092] [motion_commander]: Pianificazione riuscita in 0.015 secondi
[INFO] [1791829005.077350168] [motion_commander]: La traiettoria contiene 63 punti
[INFO] [1791829005.078405881] [motion_commander]: Goal di esecuzione inviato
[INFO] [1791829005.079427936] [motion_commander]: Goal di esecuzione accettato
[INFO] [1791829005.080154992] [motion_commander]: Stato esecuzione: MONITOR
[INFO] [1791829012.067300678] [motion_commander]: Stato esecuzione: Solution was found and executed.
[INFO] [1791829012.067781022] [motion_commander]: Esecuzione completata con successo
```

Matteo ha confermato di aver osservato il movimento eseguito correttamente. Il tempo di pianificazione riportato è `0.015` s; l'intervallo fra accettazione e risultato osservato è circa `6.99` s. Quest'ultimo è un intervallo tra log, non una misura esatta del tempo di movimento del controllore.

I `63` punti sono campioni della traiettoria, non `63` callback o `63` movimenti separati. Nella prima prova di sola pianificazione erano stati ottenuti `4` punti: stato iniziale e condizioni della richiesta possono produrre traiettorie diverse.

### 7.13 Errori incontrati e diagnosi

| Sintomo o errore | Causa discussa | Correzione |
|---|---|---|
| “In attesa” ripetuto quando il servizio è disponibile | Ciclo con `while wait_for_service(...)` | Ripetere quando il risultato è falso: `while rclpy.ok() and not ...` |
| “Disponibile” stampato dopo la chiusura | Uscita dal ciclo anche per shutdown | Controllare `rclpy.ok()` prima del log e dell'invio |
| `AttributeError` su `request.group_name` | Campo assegnato sul messaggio esterno | Usare `request.motion_plan_request` |
| `request` non definita | Creata `self.request` ma letto `request` | Usare coerentemente un nome locale o un attributo |
| `self.plan` non definito | Uso di un attributo mai creato | Definire `plan = request.motion_plan_request` e usare `plan` |
| Traiettoria apparentemente non conservata | Refuso `planned_trajectroy` | Usare ovunque `planned_trajectory` |
| Numero di punti non visibile | Calcolo di `num_points` senza log | Aggiungere `get_logger().info(...)` |
| Solo “Servizio di pianificazione disponibile” | Non raggiunto il metodo di invio o processo/file non aggiornato | Controllare chiamata, rientri, salvataggio e riavvio |
| `build_execution_goal` non trovato | Chiamata senza `self.` | `self.build_execution_goal()` |
| Goal mancante nonostante la costruzione | Assente `return goal` | Restituire il messaggio creato |
| Nuovo errore durante l'`except` | `exc` usata senza `as exc` | `except Exception as exc:` |
| Nessuna indicazione di un'eccezione | `except: return` silenzioso | Registrare l'eccezione e uscire |
| `/n` visibile nel testo | Sequenza errata | Usare `\n` o un messaggio su una riga |
| Metodo non disponibile sulla classe | `def` fuori da `MotionCommander` | Allineare tutti i metodi della classe |
| Ctrl+C durante l'attesa non gestito dal blocco | Costruzione del nodo prima del `try` | Mettere anche il costruttore nel `try` |
| Contesto ROS non chiuso se il costruttore viene interrotto | `try_shutdown` dentro l'`if` sul nodo | Chiamarlo comunque nel `finally` |

#### Diagnosi del caso “vedo soltanto il servizio disponibile”

Matteo ha osservato inizialmente solo quel messaggio. Abbiamo aggiunto come prima riga di `request_plan`:

```python
self.get_logger().info('Entrato nel metodo request_plan')
```

Se il messaggio non compare, il metodo non è raggiunto oppure il processo non usa il file aggiornato. Se compare ma manca il log successivo, controllare `build_plan_request` e il traceback. Dopo la revisione e il riavvio sono comparsi invio, risposta riuscita e numero di punti. Non è stata isolata una causa unica fra chiamata mancante e versione avviata: la prova ha verificato il percorso corretto.

Per individuare quale installazione viene usata:

```bash
source /opt/ros/jazzy/setup.bash
source /home/matteo/vision_sort_ws/install/setup.bash
ros2 pkg prefix vision_sort_lab
ros2 pkg executables vision_sort_lab
python3 -c "import vision_sort_lab.motion_commander as m; print(m.__file__)"
```

L'eseguibile deve includere `vision_sort_lab motion_commander` e il modulo importato deve appartenere all'installazione del workspace previsto. Con i symlink il percorso può apparire sotto `install` pur rimandando al sorgente.

Alcuni codici MoveIt utili per la diagnosi:

| Costante | Valore | Significato |
|---|---|---|
| `SUCCESS` | `1` | Successo |
| `PLANNING_FAILED` | `-1` | Nessuna soluzione di pianificazione |
| `CONTROL_FAILED` | `-4` | Esecuzione/controllo fallito |
| `TIMED_OUT` | `-6` | Tempo scaduto |
| `START_STATE_IN_COLLISION` | `-10` | Stato iniziale in collisione |
| `GOAL_IN_COLLISION` | `-12` | Obiettivo in collisione |
| `INVALID_GROUP_NAME` | `-15` | Gruppo non valido |
| `ROBOT_STATE_STALE` | `-23` | Stato del robot non aggiornato |

Usare anche il terminale della demo per leggere il motivo dettagliato. Non introdurre tentativi ripetuti senza aver capito e aggiornato lo stato.

### 7.14 Limiti attuali e prossimo esercizio

**Verificato nella demo:** collegamento, pianificazione, invio della traiettoria, accettazione, feedback, risultato positivo e movimento osservato.

**Ancora aperto:**

- Confronto automatico fra posizioni raggiunte e obiettivo.
- Controllo della freschezza dei messaggi `/joint_states`.
- Timeout complessivi delle attese e delle operazioni asincrone.
- Prove sistematiche di fallimento, goal rifiutato ed eccezioni nel sistema ROS.
- Cancellazione, ripianificazione e numero finito di tentativi.
- Sequenze con più obiettivi, pinza, collision objects e gestione della scena.
- Gazebo, visione e verifica fisica di presa/deposito.

Il listato è un nodo didattico a singola richiesta, non una macchina a stati completa. Gli `except` gestiscono il recupero del risultato dai Future; non costituiscono gestione esaustiva di ogni errore immediato di costruzione o invio. Non bisogna chiamare ad hoc più richieste contemporanee sul nodo: la gestione dei goal concorrenti non è stata progettata.

#### Verificare la configurazione raggiunta

Il prossimo esercizio userà le posizioni di `/joint_states`, riutilizzando i concetti di `joint_monitor`. Per ciascuno dei sette giunti Panda:

```python
errore = abs(posizione_letta - posizione_obiettivo)
entro_tolleranza = errore <= tolleranza
```

Questo è **un frammento concettuale**, non una funzionalità già implementata. Prima di dichiarare la verifica positiva serviranno tutti i giunti richiesti, dati sufficientemente recenti e un criterio temporale dopo la conclusione del movimento. Un giunto mancante non deve essere considerato corretto.

L'action positiva sarà un ingresso del processo di verifica; il confronto con gli stati ricevuti sarà un ulteriore controllo. La tolleranza della verifica va scelta e dichiarata separatamente dai vincoli di pianificazione e dalle tolleranze del controllore.

#### Cancellazione e recupero, in seguito

La futura cancellazione userà il goal handle per chiedere al server di interrompere il goal. Il completamento della richiesta di cancellazione e il risultato finale dell'action saranno verificati separatamente. Prima di ripianificare servirà acquisire lo stato aggiornato, perché il robot può essersi fermato lungo il percorso.

Non basta cancellare un Future Python per arrestare il robot. Non introduciamo qui un'implementazione anticipata: questa fase sarà un esercizio dedicato.

### 7.15 Python e C++: decisione per il progetto

`motion_commander` è già un nodo ROS 2, anche se scritto in Python. Per proseguire non serve convertirlo a C++.

C++ può essere utile quando il nodo esegue calcoli pesanti, richiede controllo accurato delle risorse o deve usare direttamente una libreria C++. Il compilatore intercetta molti errori di nomi e tipi prima dell'avvio. MoveIt mette a disposizione `MoveGroupInterface` per impostare obiettivi, pianificare ed eseguire tramite metodi dedicati.

Python permette modifiche più rapide e concentra lo studio sulle interfacce. Nel nostro nodo il lavoro di pianificazione e controllo è svolto da altri componenti: riscrivere il client non implica accelerare il pianificatore o il movimento.

C++ richiede più attenzione a compilazione, tipi e gestione degli oggetti. Il tempo reale richiede anche una progettazione del sistema e del codice adeguata; il linguaggio da solo non lo garantisce.

**Decisione:** continuare in Python con `rclpy`. Aggiungere eventuali nodi C++ solo per esigenze concrete o per un esercizio mirato, mantenendo l'interoperabilità ROS 2.

Fonti: [MoveGroupInterface](https://moveit.picknik.ai/main/doc/examples/move_group_interface/move_group_interface_tutorial.html) e [concetti di tempo reale in ROS 2 Jazzy](https://github.com/ros2/ros2_documentation/blob/jazzy/source/Tutorials/Demos/Real-Time-Programming.rst).

### 7.16 Riprendere in una nuova chat

Titolo della chat che raccoglie questa fase: **Vision Sort Lab — Primo movimento Panda con ROS 2 e MoveIt 2**.

Messaggio sintetico di continuità, da copiare se serve:

```text
Progetto: Vision Sort Lab.
Obiettivo: cella robotica simulata per smistare oggetti mediante visione,
manipolazione e recupero degli errori. Per ora nessun hardware.

Metodo: scrivo personalmente il codice, con piccoli esercizi guidati,
spiegazioni dei concetti e revisione dei tentativi. Non generare
automaticamente l'intero progetto.

Ambiente: Ubuntu 24.04 su WSL 2, ROS 2 Jazzy, MoveIt 2, Panda nella demo
RViz con hardware mock/simulato. Gazebo deve ancora essere realizzato.
Continuiamo in Python/rclpy: i nostri programmi sono già nodi ROS 2.

Workspace Ubuntu: /home/matteo/vision_sort_ws.
Pacchetto: vision_sort_lab.
Nodi: joint_monitor.py e motion_commander.py.
Modulo di supporto: motion_builders.py.

Completato e verificato: demo Panda, movimenti da RViz, subscription
a /joint_states, dizionario nome giunto -> posizione, log circa 1 Hz,
build e ros2 run; primo movimento dal nostro programma verso ready.
motion_commander usa GetMotionPlan su /plan_kinematic_path e
ExecuteTrajectory su /execute_trajectory, con Future, callback,
accettazione del goal, feedback e risultato finale.
Sono inoltre verificati: confronto automatico dei sette giunti entro
0.01 rad su un campione successivo al risultato dell'esecuzione;
separazione dei builder in motion_builders.py; timeout della verifica
di 2.0 s con timer ogni 0.1 s, prova controllata e ripristino.
Il timeout è stato provato sospendendo il confronto articolare;
non è stata interrotta realmente la pubblicazione di /joint_states.

Gestione dei fallimenti di pianificazione verificata nei casi seguenti (13).
Il metodo attuale on_plan_response(self, future) è stato ricevuto
e rivisto: il ramo con codice diverso da SUCCESS non invia l'esecuzione.
La prima prova negativa con gruppo inesistente ha restituito 99999;
comportamento richiesto e ripristino confermati dall'utente (13.4).
Anche il test con vincoli incompatibili per panda_joint1 e la rimozione
del blocco TEST sono confermati, con ritorno al percorso positivo (13.7).
Il codice numerico di questo secondo test non è stato comunicato.
La funzione describe_moveit_error(code) in motion_errors.py, l'import
nel commander e il nuovo log con nome e numero sono verificati (13.15).
Matteo preferisce mantenerla esterna per semplificare il commander.
Gruppo panda_arm ripristinato e percorso positivo confermato.
on_execution_goal_response(self, future) ricevuto il 14 ottobre:
controllo dell'accettazione e richiesta del risultato corretti.
Matteo conferma le correzioni a except e al livello del log (14.3).
Consegne ora più lunghe: spiegazione, implementazione e verifica insieme.
Script /home/matteo/vision_sort_ws/check_goal_response.py individuato:
test locali eccezione e rifiuto riusciti, secondo l'output riferito.
Prova Panda allegata: 4 punti, piano in 0.018 s, verifica positiva
su campione successivo al risultato, nessun timeout (14.7).
Cinque test locali riusciti, con script completo e on_execution_result
ricevuti e rivisti: confronto con and e log negativo corretti (15.2).
Restano due prove principali nel blocco corrente: errore reale dell'action
con controllore inesistente e verifica articolare negativa (15.3).
Log del fallimento reale ricevuto: status ROS=6, CONTROL_FAILED(-4) (15.5).
Consegna attuale: rimuovere il controllore di test; nel ramo positivo
del risultato alterare temporaneamente solo il riferimento della verifica,
poi osservare esito negativo e ripristinare il percorso positivo (16.1).
Verifica negativa osservata: stamp aggiornato, errore joint1=0.499512 (16.2).
Matteo preferisce mantenere la gestione dell'action e la cancellazione
nel commander: le proposte di estrazione 17.2–17.3 sono superate (17.4).
request_cancel ricevuto e rivisto: controllo None, invio asincrono e
callback corretti; sostituire il testo provvisorio del log (17.5).
on_cancel_response corretto ricevuto e rivisto il 15 ottobre (17.7).
Il 21 ottobre Matteo invia i tre test di cancellazione e l'output:
tutti gli otto test locali riusciti; codice rivisto e corretto (17.8).
Il promemoria di aggiornare lo script è soddisfatto.
Prova temporizzata nella demo ricevuta e rivista (17.10): richiesta
dopo 0.301 s, risposta solo a fine movimento con codice 3, nessun arresto.
Esecuzione e verifica verso joint1=0.8 riuscite, nessun timeout nel log.
Ripristino al target 0.0 riuscito, log con sette giunti entro tolleranza,
nessuna cancellazione o timeout nel log successivo di oltre tre secondi (17.11).
Prefisso /opt/ros/jazzy, pacchetto 2.12.4-1noble.20260915.202214.
Prossimo esercizio: massimo un retry di piano per due codici ammessi,
con tre test locali (18). Callback ricevuta e rivista in 18.5.
Test ricevuti e corretti: Matteo conferma tutti gli undici riusciti (18.8).
Retry testato localmente: il servizio 2.12.4 può mascherare gli errori
specifici con FAILURE (99999), escluso dalla politica (18.9).
Parametro target da terminale confermato funzionante dall'utente (19.4).
Log della prova 0.8 ricevuto: sette giunti entro tolleranza, nessun timeout.
Prossimo blocco: scene_inspector.py separato, GetPlanningScene con
WORLD_OBJECT_NAMES per leggere gli ID degli oggetti già noti a MoveIt (20).
Supporto agli avvisi VS Code/Pylance documentato in 20.4–20.6;
risoluzione non esplicitamente confermata, inspector comunque eseguito.
SceneInspector ricevuto: import corretto, client e callback corretti,
GetPlanningScene restituisce zero oggetti (20.7). Pylance non confermato.
Ora piccole correzioni log/pulizia e scene_builders.py con tavolo (21).
Il 23 ottobre Matteo richiede una nuova chat dedicata alla scena (21.5).
Ripartire dalle sezioni 20.7 e 21, senza considerare già scritto il builder.
Matteo chiede di chiarire cambio di argomento e mancata cancellazione:
spiegazione e verifica del sorgente tag 2.12.4 documentate in 18.4.
Cancellazione efficace resta aperta; il retry del piano non la risolve.

Guida Windows:
C:\Users\matte\Documents\Codex\2026-10-05\vor\outputs\vision-sort-lab\GUIDA-PROGETTO.md
La guida e il workspace Ubuntu sono distinti.
Piccoli esercizi in Python/rclpy, nuove API spiegate prima dell'uso.
Spiegazioni e comandi in chat; guida aggiornata a ogni checkpoint.
```

## 8. Registro delle decisioni

| Decisione | Motivazione | Stato |
|---|---|---|
| Metodo guidato | L'obiettivo è apprendere scrivendo e verificando il codice | Confermato dall'utente |
| Smistamento con due colori e tre oggetti | Limita la percezione iniziale mantenendo un ciclo completo | Obiettivo della prima versione |
| Ubuntu 24.04, ROS 2 Jazzy, Gazebo Harmonic | Abbinamento compatibile e documentato | Ubuntu e ROS operativi; Gazebo da verificare |
| Prima movimento da posa nota, poi visione | Separa errori di movimento da errori di percezione | Percorso definito |
| Panda delle risorse MoveIt per il primo esercizio | Consente di studiare una configurazione esistente | Demo operativa, confermata dall'utente |
| Primo esercizio tramite pacchetti precompilati | Riduce il lavoro di build iniziale e facilita la prima verifica | Demo utilizzata dall'utente |
| Nodi Python con rclpy | Permettono di apprendere le interfacce ROS 2; C++ resta opzionale | Monitor e comando operativo verificati |
| Servizio GetMotionPlan e action ExecuteTrajectory | Rendono esplicita la separazione fra calcolo, accettazione e risultato | Primo movimento programmato verificato |
| Obiettivo ready ricavato dall'SRDF locale | Usa valori definiti nella configurazione Panda installata | Sette vincoli articolari implementati |
| Verifica degli stati dopo il movimento | Aggiunge un controllo sulle posizioni oltre al risultato dell'action | Prossimo esercizio |
| Verifica della presa e del deposito | Evita di confondere il comando con il risultato fisico | Da implementare nelle fasi successive |

## 9. Diario e problemi risolti

### 7 ottobre 2026 — ambiente iniziale

**Problema:** dal contesto dell'assistente, l'enumerazione di WSL restituiva accesso negato.

**Ragionamento:** questo errore non dimostrava che Ubuntu mancasse. L'utente ha eseguito i comandi nel proprio terminale WSL e fornito l'output.

**Risultato:** Ubuntu 24.04.1 e variabili grafiche identificate; procedura ROS proposta e completata dall'utente. Talker/listener e RViz confermati funzionanti.

### 7 ottobre 2026 — preparazione dell'esercizio MoveIt

**Attività:** verificati il pacchetto Panda per Jazzy, il launch upstream e i gruppi nell'SRDF. Preparati comandi e prove per l'utente.

**Risultato:** guida disponibile. Nessuna pianificazione Panda o simulazione fisica ancora confermata sul PC.

### 8 ottobre 2026 — preparazione del pacchetto ROS

**Attività:** l'utente ha chiesto di proseguire. Preparato il passo 2A per creare il workspace Ubuntu e il pacchetto Python, leggere i file generati e modificare le descrizioni. Il nodo di lettura dei giunti è il passo 2B.

**Motivazione:** rendere comprensibile l'organizzazione del codice prima di introdurre subscription e callback; lasciare a Matteo la scrittura del nodo.

**Risultato:** istruzioni aggiunte alla guida. Creazione, modifiche e build in WSL non ancora eseguite o confermate dall'utente.

### 8 ottobre 2026 — build del pacchetto riuscita

**Evidenza:** Matteo ha fornito il riepilogo `Summary: 1 package finished [1.75s]` e il prefisso `/home/matteo/vision_sort_ws/install/vision_sort_lab`.

**Risultato:** build e riconoscimento del pacchetto confermati. Le modifiche ai metadati non sono state ispezionate. Preparato il passo 2B con uno scheletro da completare: nessun nodo originale eseguito ancora.

### 9 ottobre 2026 — nodo e movimento verificati

**Evidenza:** Matteo ha superato il controllo sintattico, ha fornito i log di `joint_monitor` e ha confermato il funzionamento dopo la visualizzazione dell'intero dizionario e la prova del movimento.

**Risultato:** completata la prima osservazione dello stato del robot tramite un nodo scritto dall'utente. Registrate le correzioni di sintassi, nomi, dati e indentazione; aggiunti entry point e comandi Bash per ripetere avvio, ispezione e build a fine sezione 6.

**Problema di accesso alla guida:** i comandi dell'assistente nella sandbox fallivano nel launcher MXC con errore di autenticazione 1326, anche usando il percorso Windows. La lettura dello stesso file fuori dalla sandbox è riuscita. La guida rimane nel percorso Windows originale; non è stata trasferita in WSL.

### 9–12 ottobre 2026 — primo movimento dal programma

**Obiettivo:** comandare il Panda dal nodo Python comprendendo pianificazione, esecuzione e feedback.

**File interessato:** `motion_commander.py` nel pacchetto Ubuntu `vision_sort_lab`; aggiornati gli entry point e le dipendenze necessarie alla procedura.

**Percorso:** client di pianificazione, vincoli per `ready` ricavati dall'SRDF, Future e callback, costruzione del goal, invio dell'action, accettazione, feedback e risultato finale.

**Problemi affrontati:** condizione di attesa invertita; campi del messaggio esterno e interno; differenza fra attributi `self` e variabili locali; refuso nel nome della traiettoria; chiamata senza `self`; `return goal` mancante; gestione delle eccezioni e indentazione. Il caso con il solo messaggio di servizio disponibile è stato diagnosticato con un log all'ingresso di `request_plan`.

**Evidenza:** Matteo ha fornito prima il risultato di pianificazione positiva con `4` punti, poi il log completo riportato in 7.12 con `63` punti, accettazione, feedback e risultato finale positivo. Ha confermato il movimento osservato in RViz.

**Risultato:** primo movimento programmato completato nella demo mock. Il confronto automatico delle posizioni, le prove sistematiche dei fallimenti e la cancellazione restano da implementare. Chiarito che Python/rclpy è già ROS 2; proseguimento in Python confermato.

### 12 ottobre 2026 — consolidamento della guida

**Richiesta:** Matteo ha autorizzato l'aggiornamento della guida con spiegazioni chiare e tutti gli snippet necessari prima del passaggio a una nuova chat.

**Attività:** lettura e modifica del documento direttamente nel workspace Windows; aggiunti percorsi distinti Windows/Ubuntu, listati completi di riferimento, spiegazioni delle funzioni, comandi, diagnosi, risultati e messaggio di continuità. La mappa `PERCORSO.md` è stata allineata ai traguardi confermati.

**Limite:** i listati della guida sono ricostruzioni documentali del codice condiviso e corretto in chat. Non è stato letto o modificato il sorgente Ubuntu e non è stata eseguita una nuova prova ROS. Le prove operative citate restano quelle fornite da Matteo.

**Controlli del materiale di riferimento:** i 20 snippet Python della guida sono stati verificati sintatticamente. I due listati completi sono stati controllati anche con sostituti in memoria delle interfacce ROS: 15 scenari comprendenti struttura della richiesta, percorso positivo, piano fallito, traiettoria vuota, goal rifiutato, eccezioni nelle callback, esiti finali discordanti e chiusura del nodo. Questi controlli documentali non verificano middleware, controllori o comportamento del robot e non rendono completati i futuri esercizi sui fallimenti reali.

### Formato delle prossime registrazioni

Ogni nuova voce conterrà: data, obiettivo, file interessati, snippet scritto o modificato, comandi eseguiti, motivazione, output significativo, risultato e limite ancora aperto. Gli output completi saranno inclusi quando necessari a capire il problema; i risultati di routine saranno riassunti.

## 10. Riferimenti tecnici

- [Installazione ROS 2 Jazzy: sorgente della documentazione ufficiale](https://github.com/ros2/ros2_documentation/blob/jazzy/source/Installation/Ubuntu-Install-Debs.rst).
- [Configurazione dei repository APT ROS](https://github.com/ros2/ros2_documentation/blob/jazzy/source/Installation/_Apt-Repositories.rst).
- [Release ros-apt-source 1.3.0](https://github.com/ros-infrastructure/ros-apt-source/releases/tag/1.3.0).
- [MoveIt: primo utilizzo in RViz](https://moveit.picknik.ai/main/doc/tutorials/quickstart_in_rviz/quickstart_in_rviz_tutorial.html). Il tutorial corrente usa Kinova; i concetti sono applicabili, ma i nomi del nostro robot vengono dalla configurazione Panda.
- [Indice ROS del pacchetto Panda](https://index.ros.org/p/moveit_resources_panda_moveit_config/).
- [Repository moveit_resources](https://github.com/moveit/moveit_resources).
- [Abbinamenti ROS e Gazebo](https://gazebosim.org/docs/latest/ros_installation/).
- [Creazione di un pacchetto: sorgente ufficiale ROS 2 Jazzy](https://github.com/ros2/ros2_documentation/blob/jazzy/source/Tutorials/Beginner-Client-Libraries/Creating-Your-First-ROS2-Package.rst).
- [Publisher e subscriber Python: sorgente ufficiale ROS 2 Jazzy](https://github.com/ros2/ros2_documentation/blob/jazzy/source/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Publisher-And-Subscriber.rst).
- [Definizione ufficiale di JointState per Jazzy](https://github.com/ros2/common_interfaces/blob/jazzy/sensor_msgs/msg/JointState.msg).
- [API create_subscription nel sorgente rclpy Jazzy](https://github.com/ros2/rclpy/blob/jazzy/rclpy/rclpy/node.py).
- [Profili QoS in rclpy Jazzy](https://github.com/ros2/rclpy/blob/jazzy/rclpy/rclpy/qos.py).
- [Filtri dei log in rclpy Jazzy](https://github.com/ros2/rclpy/blob/jazzy/rclpy/rclpy/impl/rcutils_logger.py).
- [Architettura di move_group](https://moveit.picknik.ai/main/doc/concepts/move_group.html).
- [Servizio GetMotionPlan](https://github.com/moveit/moveit_msgs/blob/ros2/srv/GetMotionPlan.srv).
- [MotionPlanRequest](https://github.com/moveit/moveit_msgs/blob/ros2/msg/MotionPlanRequest.msg).
- [MotionPlanResponse](https://github.com/moveit/moveit_msgs/blob/ros2/msg/MotionPlanResponse.msg).
- [RobotState](https://github.com/moveit/moveit_msgs/blob/ros2/msg/RobotState.msg).
- [Constraints](https://github.com/moveit/moveit_msgs/blob/ros2/msg/Constraints.msg).
- [JointConstraint](https://github.com/moveit/moveit_msgs/blob/ros2/msg/JointConstraint.msg).
- [ExecuteTrajectory](https://github.com/moveit/moveit_msgs/blob/ros2/action/ExecuteTrajectory.action).
- [MoveItErrorCodes](https://github.com/moveit/moveit_msgs/blob/ros2/msg/MoveItErrorCodes.msg).
- [GoalStatus per Jazzy](https://github.com/ros2/rcl_interfaces/blob/jazzy/action_msgs/msg/GoalStatus.msg).
- [Future e add_done_callback in rclpy Jazzy](https://github.com/ros2/rclpy/blob/jazzy/rclpy/rclpy/task.py).
- [Client dei servizi in rclpy Jazzy](https://github.com/ros2/rclpy/blob/jazzy/rclpy/rclpy/client.py).
- [ActionClient e ClientGoalHandle in rclpy Jazzy](https://github.com/ros2/rclpy/blob/jazzy/rclpy/rclpy/action/client.py).
- [Progettazione delle action ROS 2](https://design.ros2.org/articles/actions.html).
- [MoveGroup e opzione plan_only](https://github.com/moveit/moveit_msgs/blob/ros2/msg/PlanningOptions.msg).
- [MoveGroupInterface C++](https://moveit.picknik.ai/main/doc/examples/move_group_interface/move_group_interface_tutorial.html).
- [Programmazione in tempo reale in ROS 2 Jazzy](https://github.com/ros2/ros2_documentation/blob/jazzy/source/Tutorials/Demos/Real-Time-Programming.rst).

Le fonti aggiunte per il movimento programmato sono state consultate durante la fase di sviluppo e il consolidamento del 12 ottobre 2026. I messaggi `moveit_msgs` upstream sono un riferimento; `ros2 interface show` della versione installata resta la verifica dei campi disponibili nel proprio ambiente.

## 11. Esercizio 4 — preparare la verifica delle posizioni raggiunte

### 11.1 Obiettivo e stato

**Consegna del 12 ottobre 2026: da svolgere.** Il checkpoint di pianificazione ed esecuzione di `motion_commander` è confermato dal riepilogo dell'utente: circa `0.015` secondi per pianificare, `63` punti, circa `7` secondi di esecuzione, feedback `MONITOR` e risultato finale positivo. Il confronto automatico delle posizioni non è ancora implementato e verificato.

Il progetto prosegue in Python con `rclpy`, senza una riscrittura in C++. Matteo scrive il codice attraverso piccoli esercizi. L'assistente spiega le API e rivede i tentativi. Questo aggiornamento aggiunge una consegna alla guida Windows; non modifica i sorgenti Ubuntu.

Per verificare la configurazione finale serviranno le posizioni di tutti e sette i giunti, lo stesso obiettivo usato per pianificare e una tolleranza definita. Il confronto sarà `abs(posizione - obiettivo) <= tolleranza` per ciascun giunto. Un giunto mancante significa dati insufficienti. Studieremo anche la freschezza del campione: il risultato positivo dell'action non garantisce che il dizionario locale contenga già lo stato finale.

### 11.2 Primo piccolo passo — ricezione nel commander

Il dizionario di `joint_monitor` appartiene a quel nodo. `motion_commander` deve ricevere `/joint_states` tramite una propria subscription per conservare lo stato nella propria memoria.

API e dati da comprendere prima di usarli:

- `self.create_subscription(tipo, topic, callback, qos)` registra una callback per i messaggi del topic e restituisce la subscription. Usare `JointState`, `'/joint_states'`, `self.on_joint_states` e `qos_profile_sensor_data`, in questo ordine. Passare la callback senza parentesi.
- `qos_profile_sensor_data` è lo stesso profilo best effort già usato nel monitor.
- In `JointState`, `name[i]` identifica il giunto associato a `position[i]`. Per i giunti rotativi del braccio la posizione è in radianti. Le posizioni possono essere vuote; se presenti, devono avere la stessa lunghezza dei nomi.
- `msg.header.stamp` indica il tempo di registrazione del campione, con i campi `sec` e `nanosec`, secondo l'orologio del publisher. Per ora lo conserviamo; la verifica temporale sarà un esercizio successivo. Non confrontarlo con l'orologio Windows.

Fonti: [create_subscription nel sorgente ufficiale rclpy Jazzy](https://github.com/ros2/rclpy/blob/jazzy/rclpy/rclpy/node.py), [JointState per Jazzy](https://github.com/ros2/common_interfaces/blob/jazzy/sensor_msgs/msg/JointState.msg) e [profili QoS di rclpy Jazzy](https://github.com/ros2/rclpy/blob/jazzy/rclpy/rclpy/qos.py).

Matteo aggiunge gli import di `JointState` da `sensor_msgs.msg` e di `qos_profile_sensor_data` da `rclpy.qos`.

Nel costruttore, dopo l'inizializzazione ROS del nodo e prima della richiesta di pianificazione:

1. Inizializzare `self.joint_positions` con un dizionario vuoto e `self.last_joint_state_stamp` con `None`.
2. Creare la subscription con i quattro argomenti spiegati sopra e conservarla in `self.joint_state_subscription`.

Scrivere `on_joint_states(self, msg)` con questi compiti:

1. Ritornare se `msg.position` è vuoto. Se nomi e posizioni hanno lunghezze diverse, emettere un warning e ritornare.
2. Sostituire `self.joint_positions` con `dict(zip(msg.name, msg.position))` e conservare `msg.header.stamp` in `self.last_joint_state_stamp`.
3. Mostrare temporaneamente il dizionario con `self.get_logger().info`, usando `throttle_duration_sec=1.0`. Aggiornare entrambi gli attributi a ogni messaggio valido, anche quando il log viene saltato dal filtro.

Il dizionario rappresenta un singolo messaggio: non usare `update` per fondere campioni di tempi diversi. Se arrivano messaggi parziali, li esamineremo prima di scegliere una diversa strategia. In questo passo la callback raccoglie dati; non decide ancora se l'obiettivo sia raggiunto.

### 11.3 Comandi e consegna per la revisione

Eseguire in **Ubuntu WSL**:

```bash
nano /home/matteo/vision_sort_ws/src/vision_sort_lab/vision_sort_lab/motion_commander.py
```

Per mostrare il file:

```bash
cat /home/matteo/vision_sort_ws/src/vision_sort_lab/vision_sort_lab/motion_commander.py
```

Prima dell'avvio, inviare in chat gli import, il costruttore e la nuova callback per la revisione. Non occorre riscrivere il nodo completo.

**Criterio del primo passo:** dopo revisione e avvio, osservare i sette giunti del braccio in log prodotti da `motion_commander`, aggiornati durante il movimento. Nessuna nuova prova ROS è stata eseguita dall'assistente in questo aggiornamento.

**Passi successivi:** calcolo degli errori e tolleranza; collegamento della verifica al risultato dell'action; attesa di dati aggiornati con un limite temporale, evitando attese bloccanti nelle callback. Seguiranno prove dei fallimenti, cancellazione e recupero.

### 11.4 Revisione del primo tentativo — 12 ottobre 2026

**Stato: frammento esaminato; correzioni da applicare e ricezione nel commander ancora da verificare.** Matteo ha inviato gli import, la callback `on_joint_state` e il costruttore. Gli import ROS, i quattro argomenti della subscription e il riferimento `self.on_joint_state` sono coerenti. Il nome al singolare va bene: deve corrispondere al metodo definito.

La callback controllava inizialmente `self.joint_positions` e `self.last_joint_state_stamp`, anziché il messaggio appena ricevuto. Questi attributi conservano il campione precedente; prima del primo campione sono volutamente vuoti anche quando il nuovo messaggio contiene posizioni valide. Inoltre mancava `:` dopo il primo `if` e il ramo non terminava con `return`.

Correzione minima da applicare al solo blocco iniziale, dentro la callback:

```python
if not msg.position:
    return
```

Il controllo delle lunghezze, `dict(zip(msg.name, msg.position))`, la conservazione di `msg.header.stamp` e il filtro del log a un secondo sono corretti nel frammento. Il log mostrava soltanto `panda_joint3`; per osservare i sette giunti in questo checkpoint, sostituire temporaneamente il blocco di visualizzazione del singolo giunto con:

```python
testo = str(self.joint_positions)
self.get_logger().info(testo, throttle_duration_sec=1.0)
```

Nel file reale `__init__` e `on_joint_state` devono essere metodi della classe `MotionCommander(Node)`, indentati di quattro spazi; il frammento inviato non mostra la dichiarazione della classe, quindi la sua presenza non è stata verificata. `self.target_positions` è già conservato nel costruttore e potrà essere usato dal successivo confronto.

Dopo le correzioni, controllare la sintassi in **Ubuntu WSL**:

```bash
python3 -m py_compile /home/matteo/vision_sort_ws/src/vision_sort_lab/vision_sort_lab/motion_commander.py
```

Il controllo verifica la sintassi; la ricezione ROS richiede una successiva prova con il nodo avviato. Prima di procedere al confronto con l'obiettivo, inviare la callback corretta e l'esito del comando. Nessuna prova di build o esecuzione di questa modifica è stata ancora confermata.

### 11.5 Checkpoint — ricezione nel commander confermata

**12 ottobre 2026: completato tramite callback corretta e log forniti dall'utente.** La callback controlla `msg.position`, scarta messaggi con lunghezze incoerenti, sostituisce il dizionario, conserva `msg.header.stamp` e limita il log a circa 1 Hz.

I log allegati provengono da `motion_commander` e contengono tutti e sette i giunti del braccio, oltre ai due giunti delle dita. Il campione iniziale contiene la configurazione ready; dopo l'esecuzione le posizioni cambiano e vengono ripetutamente ricevute. La pianificazione dura `0.015` secondi, questa traiettoria contiene `5` punti, il goal viene accettato e l'esecuzione termina con successo. Fra accettazione e risultato trascorrono circa `0.39` secondi. Questi dati appartengono alla nuova prova e non sostituiscono quelli della precedente traiettoria di 63 punti.

Errori assoluti calcolati dall'assistente sui valori del campione stampato dopo il risultato, rispetto all'obiettivo ready già definito:

| Giunto | Errore assoluto (rad, arrotondato) |
|---|---:|
| `panda_joint1` | 0.001249 |
| `panda_joint2` | 0.009157 |
| `panda_joint3` | 0.007943 |
| `panda_joint4` | 0.006798 |
| `panda_joint5` | 0.002532 |
| `panda_joint6` | 0.006437 |
| `panda_joint7` | 0.000101 |

Tutti i valori osservati rientrano in `0.01` rad. Questo è un controllo dei log da parte dell'assistente: il confronto automatico nel nodo non è ancora implementato. La conservazione dello stamp è presente nel codice inviato; i log non mostrano gli stamp e non ne dimostrano la freschezza. Il tempo del log indica quando è stata eseguita la stampa, non quando il publisher ha registrato il campione.

### 11.6 Prossimo piccolo esercizio — confronto numerico

**Da svolgere:** scrivere soltanto `check_target_reached(self)`, senza chiamarlo ancora dalla callback dei giunti o dalle callback dell'action. La funzione valuterà il campione attualmente memorizzato; il collegamento alla conclusione dell'esecuzione e la verifica temporale verranno affrontati dopo la revisione.

Definire nel costruttore `self.goal_tolerance = 0.01` (radianti). Questa è la tolleranza scelta per la nostra verifica, distinta come responsabilità dalle tolleranze dei `JointConstraint`, anche se ora ha lo stesso valore.

Prima di implementare, comprendere queste operazioni Python:

- `self.target_positions.items()` permette di iterare su coppie `(nome, obiettivo)`; usare i sette giunti dell'obiettivo, non tutti i giunti ricevuti, che includono anche le dita.
- `abs(posizione - obiettivo)` misura l'errore assoluto: uno scostamento positivo o negativo della stessa ampiezza conta allo stesso modo.
- Un risultato `None` indica dati insufficienti; `False` indica che il campione completo non rispetta la tolleranza; `True` indica che tutti e sette i giunti la rispettano. Non confondere `None` con un giunto fuori tolleranza.

Consegna del metodo:

1. Controllare che ogni nome dell'obiettivo sia presente in `self.joint_positions`; se manca, emettere un warning con quel nome e restituire `None`.
2. Per tutti e sette i giunti calcolare l'errore assoluto e registrarlo con nome e unità rad, ad esempio con sei decimali.
3. Restituire `True` solo se ogni errore è `<= self.goal_tolerance`, altrimenti `False`. È possibile usare una variabile booleana inizialmente vera e renderla falsa quando un confronto non è soddisfatto, continuando il ciclo per mostrare tutti gli errori.

Matteo invia il solo metodo e la riga di inizializzazione della tolleranza. Nessuna nuova API ROS è necessaria in questo passo. La ricezione dello stato è verificata; la verifica automatica finale, la gestione dei fallimenti, la cancellazione e il recupero rimangono aperti.

### 11.7 Revisione del confronto — primo tentativo

**12 ottobre 2026: codice ricevuto e rivisto; confronto ancora da correggere e verificare.** L'iterazione su `self.target_positions.items()` è corretta e il risultato `None` è appropriato quando manca un giunto richiesto.

Correzioni individuate:

- `self.joint_positions` è un dizionario, non un messaggio `JointState`: non ha un attributo `.name`. La presenza si controlla con `if name not in self.joint_positions:`. Il warning deve indicare quale nome manca.
- L'assegnamento con `=` dentro l'espressione della f-string inviata non è sintassi valida. Calcolare prima l'errore in una riga separata, poi formattarlo nel log.
- Usare `error = abs(self.joint_positions[name] - objective)`. La semplice sottrazione produce anche errori negativi: per esempio `-0.2 <= 0.01` è vero, ma lo scostamento assoluto è fuori tolleranza.
- La variabile `check` deve partire da `True` e diventare `False` se anche un solo giunto non soddisfa il confronto `error <= self.goal_tolerance`. Non riportarla a `True` quando un giunto successivo è corretto; continuare il ciclo per mostrare tutti gli errori. La versione inviata rendeva vera la variabile quando un singolo giunto rientrava nella tolleranza, senza rappresentare il controllo di tutti e sette.
- Il log deve indicare il giunto e l'unità: ad esempio `f'{name}: errore = {error:.6f} rad'`.
- Aggiungere `return check` dopo il ciclo `for`, alla stessa indentazione del `for`. Senza un return finale il metodo restituisce implicitamente `None` anche dopo aver elaborato tutti i giunti.

Matteo applica le correzioni e invia nuovamente il solo metodo. Verificare anche la presenza di `self.goal_tolerance = 0.01` nel costruttore. Non è ancora stata eseguita una prova di questo metodo né collegato il confronto all'action.

**Secondo tentativo, 12 ottobre 2026:** corretti l'inizializzazione di `check` a `True`, il warning con il nome del giunto, il calcolo con `abs` e il log separato. Restano tre modifiche: togliere `.name` dal controllo di presenza nel dizionario; usare la variabile `error` nel confronto, perché `error_tolerance` non è definita nel metodo inviato; aggiungere `return check` dopo il ciclo, alla stessa indentazione del `for`. Per i valori finiti osservati nella demo, `if error > self.goal_tolerance:` individua lo scostamento fuori tolleranza. Il metodo non è ancora confermato funzionante e non è stato collegato all'action.

**Organizzazione del codice:** Matteo ha chiesto di discutere una divisione del commander in moduli dopo questo esercizio. È stato concordato di completare prima la verifica, poi valutare un piccolo refactoring guidato, iniziando eventualmente dalle funzioni che costruiscono richieste e vincoli e mantenendo il coordinamento ROS nel nodo.

**Terzo tentativo, 12 ottobre 2026:** confronto con `error` e `return check` dopo il ciclo ora corretti. Il ciclo è stato cambiato in `for name in self.target_positions.items()`: ogni elemento di `items()` è una coppia, per esempio `('panda_joint2', -0.785)`, quindi `name` riceverebbe l'intera coppia e `objective` non verrebbe definita. Ripristinare `for name, objective in self.target_positions.items():`. Il controllo di presenza contiene ancora `.name`: usare `if name not in self.joint_positions:`, perché `self.joint_positions` è il dizionario costruito dalla callback. Il resto del metodo inviato può rimanere invariato. Il confronto non è ancora stato provato in esecuzione.

### 11.8 Metodo di confronto corretto — revisione completata

**12 ottobre 2026: versione corretta ricevuta da Matteo; revisione del metodo completata.** La prova del risultato restituito dal nodo e il collegamento temporale con l'esecuzione restano da svolgere. Per le posizioni finite della demo e l'obiettivo ready di sette giunti, il metodo distingue dati insufficienti, almeno un giunto fuori tolleranza e tutti i giunti entro tolleranza.

Versione scritta dall'utente, da mantenere dentro la classe del nodo:

```python
    def check_target_reached(self):
        check = True
        for name, objective in self.target_positions.items():
            if name not in self.joint_positions:
                self.get_logger().warning(
                    f"Target position of joint {name} not in Joint position"
                )
                return None
            error = abs(self.joint_positions[name] - objective)
            self.get_logger().info(
                f'{name}: errore = {error:.6f} rad'
            )
            if error > self.goal_tolerance:
                check = False
        return check
```

Il valore `self.goal_tolerance = 0.01` deve essere presente nel costruttore. Un errore uguale alla tolleranza è accettato. L'errore viene confrontato prima di qualsiasi arrotondamento: `:.6f` riguarda soltanto la visualizzazione.

Il metodo esamina il dizionario attuale e non stabilisce da solo quando il campione sia stato registrato. Il prossimo passo richiede il codice attuale di `on_execution_result` per progettare la verifica su dati aggiornati dopo il risultato positivo, senza attese bloccanti. La sola chiamata al metodo non dimostra ancora la verifica finale dell'esecuzione. La divisione del commander in moduli resta concordata dopo la verifica di questo esercizio.

### 11.9 Punto di ripresa concordato — fine sessione

**12 ottobre 2026:** Matteo conclude la sessione dopo aver completato la scrittura e la revisione di `check_target_reached`. Nessuna nuova prova in esecuzione del confronto è stata fornita. Il metodo è corretto per i dati finiti della demo, ma non è ancora collegato alla verifica finale del movimento.

Alla prossima richiesta di aggiornamento, fornire in chat un riepilogo chiaro di quanto è stato fatto e dei prossimi passi:

- **Verificato:** demo Panda in RViz con hardware mock; monitor `/joint_states`; pianificazione ed esecuzione tramite `motion_commander`, accettazione, feedback e risultato; subscription propria del commander con tutti e sette i giunti e log circa 1 Hz.
- **Scritto e rivisto:** conservazione dello stamp e `check_target_reached`, con errore assoluto per ogni giunto e risultati `None`, `False`, `True`. Tolleranza di verifica prevista: `0.01` rad; la sua inizializzazione nel costruttore deve essere presente.
- **Prossimo passo tecnico:** ricevere il codice attuale di `on_execution_result`, spiegare e costruire il collegamento della verifica a dati aggiornati dopo l'esecuzione, quindi osservare il risultato del confronto nel nodo. Fallimenti, cancellazione, recupero e simulazione fisica Gazebo rimangono fasi successive.
- **Promemoria esplicito richiesto da Matteo:** ricordare di valutare se dividere `motion_commander.py`, ormai lungo, in moduli semplici. Discutere questa scelta nel riepilogo prima di proseguire con altro codice; la divisione è una possibilità da valutare insieme, non una modifica già autorizzata da eseguire automaticamente.

Continuare con piccoli esercizi in Python/rclpy, lasciando a Matteo la scrittura del codice. La richiesta di riepilogo riguarda la prossima conversazione e non prevede una notifica programmata.

### 11.10 Collegamento al risultato — preparare l'attesa della verifica

**13 ottobre 2026: ricevuto e rivisto `on_execution_result` attuale.** Matteo recupera il risultato dal Future con gestione dell'eccezione, legge `response.status` e `response.result.error_code.val`, e riconosce il successo solo quando coincidono `GoalStatus.STATUS_SUCCEEDED` e `MoveItErrorCodes.SUCCESS`. Questo controllo è coerente con il comportamento verificato. La verifica articolare non viene ancora chiamata.

**Nuovo piccolo esercizio, da svolgere:** nel ramo di successo registrare il momento in cui il nodo elabora il risultato e attivare la richiesta di verifica. La callback deve poi terminare per permettere all'executor di elaborare altri messaggi dei giunti.

Spiegazione delle API prima dell'uso:

- `self.get_clock()` restituisce l'orologio del nodo.
- `.now()` legge un istante e restituisce un oggetto `rclpy.time.Time`.
- `.nanoseconds` è una proprietà che restituisce il numero totale di nanosecondi dall'epoca dell'orologio, non soltanto la frazione di secondo. Non si scrivono parentesi dopo la proprietà.
- L'espressione completa è `self.get_clock().now().nanoseconds`.

Fonti: [Clock.now di rclpy Jazzy](https://github.com/ros2/rclpy/blob/jazzy/rclpy/rclpy/clock.py) e [Time.nanoseconds di rclpy Jazzy](https://github.com/ros2/rclpy/blob/jazzy/rclpy/rclpy/time.py).

Nel costruttore, prima della richiesta di pianificazione, inizializzare:

```python
self.verification_pending = False
self.verification_start_ns = None
```

Nel ramo di successo di `on_execution_result`, dopo il log già presente, Matteo aggiunge due assegnamenti: salvare l'istante attuale in `self.verification_start_ns`, poi impostare `self.verification_pending = True`. I rami di errore non attivano la verifica. Il flag significa verifica richiesta e ancora da effettuare, non obiettivo già verificato.

In questo passo non chiamare ancora `check_target_reached` e non introdurre un ciclo di attesa nella callback. Inviare le inizializzazioni e il ramo di successo modificato per la revisione.

**Passo successivo:** usare la callback dei giunti per verificare il tempo del campione e la presenza dei sette giunti, quindi chiamare il confronto. Prima di confrontare numericamente lo stamp del publisher con l'orologio del commander, verificare che entrambi usino lo stesso riferimento temporale e una configurazione coerente di `use_sim_time`. Memorizzare l'istante di attivazione non dimostra ancora la freschezza. Successivamente introdurre un limite temporale all'attesa. Nessuna nuova prova ROS è stata eseguita o confermata con queste modifiche.

### 11.11 Attivazione della verifica — ramo corretto

**13 ottobre 2026: modifica ricevuta e rivista.** Nel ramo di successo Matteo assegna prima `self.get_clock().now().nanoseconds` a `self.verification_start_ns`, poi imposta `self.verification_pending = True`. L'ordine e il posizionamento sono corretti. Le inizializzazioni nel costruttore non sono state mostrate in questa consegna; devono precedere la richiesta di pianificazione. Nessuna prova di esecuzione di questa nuova versione è stata ancora fornita.

Prima di usare lo stamp dei giunti come filtro temporale, individuare il publisher di `/joint_states` e leggere la configurazione temporale del commander. `use_sim_time = False` fa usare al normale orologio ROS il tempo di sistema; con `True` il nodo usa il tempo ROS pubblicato su `/clock`. Il confronto numerico richiede un riferimento temporale comune.

Con demo e commander attivi, in un altro terminale **Ubuntu WSL**:

```bash
source /opt/ros/jazzy/setup.bash
ros2 topic info /joint_states --verbose
ros2 param get /motion_commander use_sim_time
```

`topic info --verbose` permette di individuare nome e namespace del publisher. `param get` legge il parametro indicato senza modificarlo. Matteo invia entrambi gli output; sulla base del nome effettivo del publisher verrà indicato il comando per leggere anche il suo `use_sim_time`. I parametri del commander e del publisher, insieme al comportamento dello stamp, saranno la base per il prossimo esercizio nella callback dei giunti.

Fonti: [Orologi e tempo ROS 2](https://design.ros2.org/articles/clock_and_time.html), [ros2 param get per Jazzy](https://github.com/ros2/ros2cli/blob/jazzy/ros2param/ros2param/verb/get.py) e [ros2 topic info per Jazzy](https://github.com/ros2/ros2cli/blob/jazzy/ros2topic/ros2topic/verb/info.py).

### 11.12 Topic ripristinato e publisher individuato

**13 ottobre 2026: evidenza fornita da Matteo.** Dopo un primo controllo che mostrava soltanto `/parameter_events` e `/rosout`, `/joint_states` è ora visibile come `sensor_msgs/msg/JointState`, con un publisher: `/joint_state_broadcaster`. L'output contiene due subscriber della demo (`robot_state_publisher` e il nodo privato di MoveIt); nello snapshot non compare `motion_commander`.

Per leggere il parametro del commander occorre che il nodo sia in esecuzione. Avviarlo in un terminale Ubuntu WSL, mantenendo attiva la demo:

```bash
source /opt/ros/jazzy/setup.bash
source /home/matteo/vision_sort_ws/install/local_setup.bash
ros2 run vision_sort_lab motion_commander
```

Poi, nel terminale di ispezione già configurato per ROS:

```bash
ros2 param get /motion_commander use_sim_time
ros2 param get /joint_state_broadcaster use_sim_time
ros2 param get /controller_manager use_sim_time
```

La lettura di `controller_manager` completa il controllo del ciclo dei controllori: nel sorgente Jazzy upstream il broadcaster assegna allo stamp il tempo ricevuto nel metodo `update`. La configurazione installata verrà valutata in base agli output reali e agli stamp prima di considerare valida la comparazione temporale. Non sono ancora stati ricevuti i valori dei tre parametri.

Fonte del comportamento dello stamp: [joint_state_broadcaster Jazzy](https://github.com/ros-controls/ros2_controllers/blob/jazzy/joint_state_broadcaster/src/joint_state_broadcaster.cpp).

### 11.13 Configurazione temporale confermata e filtro sul campione

**13 ottobre 2026: parametri letti dall'utente.** `/motion_commander`, `/joint_state_broadcaster` e `/controller_manager` riportano tutti `use_sim_time = False`. La configurazione è coerente per la demo locale senza tempo simulato. Il comportamento effettivo degli stamp sarà osservato nella prova del nuovo filtro; nessuna comparazione temporale è ancora stata eseguita dal codice fornito.

**Prossimo esercizio, da svolgere:** estendere la sola callback `on_joint_state`, dopo l'aggiornamento del dizionario e dello stamp. Le posizioni devono continuare ad aggiornarsi anche quando non è richiesta una verifica.

Lo stamp del messaggio è diviso in secondi (`sec`) e frazione di secondo in nanosecondi (`nanosec`). Convertirlo nello stesso formato numerico di `verification_start_ns` con:

```python
stamp_ns = msg.header.stamp.sec * 1_000_000_000 + msg.header.stamp.nanosec
```

Per esempio, 12 secondi e 300 milioni di nanosecondi corrispondono a `12_300_000_000` nanosecondi totali. Gli underscore rendono leggibili le cifre e non cambiano il valore dell'intero.

Fonte dei campi: [builtin_interfaces/Time per Jazzy](https://github.com/ros2/rcl_interfaces/blob/jazzy/builtin_interfaces/msg/Time.msg).

Consegna guidata:

1. Dopo gli aggiornamenti già esistenti, ritornare se `self.verification_pending` è falso.
2. Calcolare `stamp_ns`. Mostrare temporaneamente `stamp_ns` e `self.verification_start_ns` in un log limitato a 1 Hz, per verificare il riferimento temporale nei dati reali.
3. Ritornare se `stamp_ns <= self.verification_start_ns`: questo esercizio richiede un campione registrato strettamente dopo l'istante in cui il nodo ha elaborato il risultato positivo. Una callback successiva non garantisce da sola che il campione sia successivo: il messaggio potrebbe essere rimasto in coda.
4. Chiamare `self.check_target_reached()` e conservarne il risultato in una variabile locale.
5. Se il risultato è `None`, ritornare mantenendo la verifica attiva: il campione non contiene tutti i giunti richiesti. Se è `True`, loggare la verifica positiva. Se è `False`, loggare che la configurazione non rispetta la tolleranza.
6. Per entrambi i risultati booleani, impostare `self.verification_pending = False`, così la verifica viene conclusa sul primo campione completo ammesso dal filtro e non ripetuta a ogni messaggio.

Distinguere esplicitamente `result is None` e `result is True`: la sola condizione `if result` non distingue dati insufficienti da un confronto negativo. Non introdurre attese bloccanti nella callback. Inviare la callback modificata per la revisione prima dell'avvio.

La prova successiva dovrà mostrare il successo dell'action, uno stamp ammesso dal filtro, gli errori dei sette giunti e un solo esito della verifica. Il limite temporale all'attesa resta da implementare; dopo il checkpoint operativo rivalutare la divisione del commander in moduli, come richiesto da Matteo.

### 11.14 Callback di verifica rivista — pronta per la prova

**13 ottobre 2026: callback ricevuta da Matteo e rivista.** La sequenza aggiorna dizionario e stamp, controlla `verification_pending`, converte lo stamp in nanosecondi, scarta i campioni con tempo `<= verification_start_ns` e chiama il confronto. `None` mantiene l'attesa; i risultati booleani producono un esito e disattivano il flag. Questa logica è corretta per il passo corrente. Non è ancora stata fornita una prova del risultato in esecuzione.

Nel frammento il log del dizionario è dopo la disattivazione del flag: viene eseguito soltanto alla conclusione della verifica. Per preservare il monitoraggio circa 1 Hz, spostare quel blocco subito dopo l'aggiornamento di `self.last_joint_state_stamp`, prima del controllo del flag. Gli attributi vengono già aggiornati correttamente a ogni messaggio valido.

`if self.verification_pending == False:` è valido; la forma `if not self.verification_pending:` è una semplificazione facoltativa. Il log dei due istanti può usare etichette `stamp_ns` e `start_ns` per facilitarne la lettura. Essendo limitato a 1 Hz, questo log diagnostico può saltare campioni: non dedurre dal solo primo log che sia quello usato nel confronto.

Prova guidata, da eseguire dall'utente in **Ubuntu WSL** mantenendo attiva la demo Panda e fermando con Ctrl+C il commander precedente. In un terminale dedicato alla build, con ROS di base:

```bash
source /opt/ros/jazzy/setup.bash
python3 -m py_compile /home/matteo/vision_sort_ws/src/vision_sort_lab/vision_sort_lab/motion_commander.py
```

Se il controllo sintattico termina senza errori:

```bash
cd /home/matteo/vision_sort_ws
colcon build --symlink-install --packages-select vision_sort_lab
```

Nel terminale del commander, dopo la build:

```bash
source /opt/ros/jazzy/setup.bash
source /home/matteo/vision_sort_ws/install/local_setup.bash
ros2 run vision_sort_lab motion_commander
```

Inviare i log dal risultato dell'action fino all'esito della verifica. Controllare che il confronto dei sette giunti produca un solo esito e che i log degli errori non si ripetano mentre continuano i messaggi di stato. Un esito fuori tolleranza richiede di esaminare gli errori, non di allargare subito la tolleranza. Attesa con limite temporale e refactoring rimangono passi successivi.

### 11.15 Checkpoint — verifica automatica riuscita

**13 ottobre 2026: completato il caso positivo, confermato dai log forniti da Matteo.** Pianificazione riuscita in `0.020` secondi, traiettoria di `4` punti, goal accettato ed esecuzione completata con successo. La callback dei giunti ha poi eseguito il confronto e prodotto `Configurazione raggiunta entro la tolleranza`.

Nel log temporale:

```text
stamp_ns = 1791897757348868798
verification_start_ns = 1791897757342782273
differenza = 6086525 ns = 6.086525 ms
```

Il campione è stato registrato dopo l'istante di attivazione della verifica. La differenza riguarda gli stamp, non la latenza con cui la callback viene elaborata.

| Giunto | Errore riportato (rad) |
|---|---:|
| `panda_joint1` | 0.008719 |
| `panda_joint2` | 0.008466 |
| `panda_joint3` | 0.001703 |
| `panda_joint4` | 0.006172 |
| `panda_joint5` | 0.005665 |
| `panda_joint6` | 0.004951 |
| `panda_joint7` | 0.001035 |

Tutti gli errori sono inferiori a `0.01` rad; il maggiore riportato è quello di `panda_joint1`. Nei log forniti compare un solo esito della verifica. L'implementazione rivista disattiva il flag dopo questo risultato. Non sono ancora stati provati sistematicamente giunti mancanti, configurazione fuori tolleranza, stamp non ammessi o interruzione della pubblicazione.

La sequenza operativa verificata è ora: richiesta di piano → piano riuscito → goal accettato → esecuzione riuscita → campione aggiornato → confronto dei sette giunti. Restano il limite temporale alla verifica, i casi negativi, la cancellazione e il recupero. Questa prova riguarda hardware mock in RViz; non dimostra la presa fisica di un oggetto.

### 11.16 Riprendere dalla divisione del commander

**Promemoria richiesto dall'utente:** ora che la verifica positiva funziona, valutare una piccola divisione del file prima di aggiungere altro codice per l'attesa.

Prima separazione proposta: lasciare comunicazione ROS e callback in `motion_commander.py`; spostare la costruzione dei vincoli e delle richieste in un modulo Python `motion_builders.py`, nella stessa cartella dei moduli del pacchetto Ubuntu. Il modulo di supporto conterrà funzioni che ricevono dati e restituiscono messaggi. Non sono ancora stati creati o modificati sorgenti Ubuntu per questa divisione.

Prossima consegna: Matteo invia le versioni attuali di `build_goal_constraints` e `build_plan_request`, così l'estrazione guidata si basa sul codice effettivo. Gli import e il passaggio dai metodi alle funzioni saranno spiegati prima dell'esercizio. Dopo il refactoring si dovrà ripetere la prova del movimento con verifica, quindi aggiungere il limite temporale all'attesa.

### 11.17 Primo refactoring guidato — costruzione dei messaggi

**13 ottobre 2026: ricevuti i due metodi attuali.** `build_goal_constraints` costruisce i vincoli usando soltanto `target_positions`. `build_plan_request` costruisce la richiesta e usa `self` soltanto per chiamare il primo metodo. Sono quindi adatti a essere trasformati in funzioni di un modulo di supporto, senza dipendere dall'istanza del nodo.

**Esercizio da svolgere da Matteo:** creare in Ubuntu il modulo `/home/matteo/vision_sort_ws/src/vision_sort_lab/vision_sort_lab/motion_builders.py` e spostare lì i due metodi, trasformandoli in funzioni. Non sono stati modificati sorgenti Ubuntu dall'assistente.

Un modulo Python è un file `.py` importabile. Un metodo della classe riceve l'istanza come `self`; una funzione esterna riceve esplicitamente i dati necessari. Queste due funzioni ricevono `target_positions` e restituiscono messaggi. Costruire i messaggi non invia richieste al robot.

Aprire il nuovo modulo in **Ubuntu WSL**:

```bash
nano /home/matteo/vision_sort_ws/src/vision_sort_lab/vision_sort_lab/motion_builders.py
```

Import necessari nel nuovo file:

```python
from moveit_msgs.msg import Constraints, JointConstraint
from moveit_msgs.srv import GetMotionPlan
```

Modifiche da applicare ai corpi esistenti, mantenendo gli stessi valori dei parametri:

- Definire `build_goal_constraints(target_positions)` e `build_plan_request(target_positions)`, togliendo `self` dalle firme.
- Scrivere ciascun `def` a inizio riga, con il corpo indentato di quattro spazi e il corpo del `for` di otto.
- Nel builder della richiesta sostituire `self.build_goal_constraints(target_positions)` con `build_goal_constraints(target_positions)`.
- Correggere il commento finale: la richiesta restituita contiene già l'obiettivo, perché `goal_constraints` è stato assegnato. La richiesta non è stata ancora inviata.

Nel commander importare la funzione esterna:

```python
from vision_sort_lab.motion_builders import build_plan_request
```

`vision_sort_lab` è il package Python; `motion_builders` è il nuovo modulo senza l'estensione `.py`; `build_plan_request` è il nome della funzione importata. L'import rende disponibile quel nome; la funzione viene eseguita quando è chiamata.

Nel metodo `request_plan` del nodo, sostituire la chiamata `self.build_plan_request(target_positions)` con `build_plan_request(target_positions)`. Rimuovere dalla classe i due vecchi metodi spostati. Gli import `Constraints` e `JointConstraint` possono essere rimossi dal commander se erano usati soltanto nei due metodi; `GetMotionPlan` deve restare perché serve a creare il client del servizio. Il nuovo modulo fa parte dello stesso package Python e non è un eseguibile ROS: non aggiungere un nuovo entry point in `setup.py`.

**Consegna per la revisione:** inviare il contenuto di `motion_builders.py`, gli import aggiornati di `motion_commander.py` e il metodo `request_plan`. Dopo la revisione, eseguire il controllo sintattico sui due moduli, la build e la stessa prova del movimento con verifica dei giunti. Il refactoring non è ancora stato completato o verificato.

### 11.18 Refactoring ricevuto e rivisto — prova da eseguire

**13 ottobre 2026:** Matteo ha inviato il nuovo `request_plan`, gli import del commander e le funzioni esterne del builder. La chiamata importata `build_plan_request(target_positions)` è corretta; la richiesta chiama `build_goal_constraints(target_positions)` senza `self`. I parametri e l'obiettivo sono preservati. Il refactoring è corretto nei frammenti esaminati; il funzionamento dopo la separazione non è ancora stato provato.

È valido definire `build_plan_request` prima di `build_goal_constraints`: il secondo nome viene cercato quando la prima funzione è chiamata, dopo il caricamento del modulo. Nel frammento i corpi delle funzioni esterne hanno otto spazi: Python lo accetta se l'indentazione è coerente; per lo stile concordato usare quattro spazi nel corpo e otto nel ciclo.

Il commander conserva l'import di `GetMotionPlan` per il client. Rimuovere l'import di `Constraints, JointConstraint` se non è usato altrove nel nodo e verificare che i due metodi spostati siano stati rimossi dalla classe. Il nuovo file importa questi tipi direttamente e non dipende dal commander.

Riferimento compatto del modulo scritto dall'utente, con indentazione a quattro spazi e gli stessi valori:

```python
from moveit_msgs.msg import Constraints, JointConstraint
from moveit_msgs.srv import GetMotionPlan


def build_plan_request(target_positions):
    request = GetMotionPlan.Request()
    plan = request.motion_plan_request
    plan.group_name = "panda_arm"
    plan.num_planning_attempts = 1
    plan.allowed_planning_time = 5.0
    plan.max_velocity_scaling_factor = 0.2
    plan.max_acceleration_scaling_factor = 0.2
    plan.start_state.is_diff = True
    plan.goal_constraints = [build_goal_constraints(target_positions)]
    return request


def build_goal_constraints(target_positions):
    goal = Constraints()
    goal.name = "joint_goal"
    for joint_name, position in target_positions.items():
        constraint = JointConstraint()
        constraint.joint_name = joint_name
        constraint.position = position
        constraint.tolerance_above = 0.01
        constraint.tolerance_below = 0.01
        constraint.weight = 1.0
        goal.joint_constraints.append(constraint)
    return goal
```

Il modulo è `/home/matteo/vision_sort_ws/src/vision_sort_lab/vision_sort_lab/motion_builders.py`. Non è una classe e non contiene un nodo da avviare separatamente. Nel commander il metodo scritto dall'utente continua a creare il Future e registrare la callback:

```python
    def request_plan(self, target_positions):
        request = build_plan_request(target_positions)
        self.get_logger().info("Richiesta di pianificazione inviata")
        self.plan_future = self.plan_client.call_async(request)
        self.plan_future.add_done_callback(self.on_plan_response)
```

**Prova da svolgere in Ubuntu WSL:** mantenere la demo attiva e fermare il precedente commander. In un terminale dedicato alla build:

```bash
source /opt/ros/jazzy/setup.bash
python3 -m py_compile \
  /home/matteo/vision_sort_ws/src/vision_sort_lab/vision_sort_lab/motion_builders.py \
  /home/matteo/vision_sort_ws/src/vision_sort_lab/vision_sort_lab/motion_commander.py
```

Se non ci sono errori:

```bash
cd /home/matteo/vision_sort_ws
colcon build --symlink-install --packages-select vision_sort_lab
```

Dopo la build, nel terminale del nodo:

```bash
source /opt/ros/jazzy/setup.bash
source /home/matteo/vision_sort_ws/install/local_setup.bash
ros2 run vision_sort_lab motion_commander
```

Inviare l'output dell'avvio: pianificazione, esecuzione e verifica dei sette giunti devono funzionare anche dopo l'estrazione. Un errore di importazione va esaminato prima di modificare la logica del movimento. Il checkpoint rimane la prova operativa; nessun sorgente Ubuntu è stato modificato dall'assistente.

### 11.19 Checkpoint — prova dopo il refactoring riuscita

**13 ottobre 2026: confermato dall'output allegato da Matteo.** Il nodo parte, pianifica in `0.013` secondi una traiettoria di `62` punti, invia il goal e ne riceve l'accettazione. L'esecuzione termina con successo dopo circa `4.55` secondi dall'accettazione. Seguono i sette errori e un unico esito positivo della verifica.

```text
stamp_ns = 1791899018158003139
verification_start_ns = 1791899018150571010
differenza = 7432129 ns = 7.432129 ms
```

Errori riportati, in ordine da `panda_joint1` a `panda_joint7`: `0.004055`, `0.000945`, `0.004206`, `0.007676`, `0.002212`, `0.006765`, `0.000834` rad. Sono tutti sotto `0.01` rad; il maggiore è quello di `panda_joint4`.

Il log finale è `Configurazione raggiunta entro la tolleranza`. Nei secondi successivi continuano i log del dizionario circa a 1 Hz, senza ripetere gli errori e l'esito della verifica. Questo conferma anche il monitoraggio continuo dopo lo spostamento del log.

Il refactoring è verificato nel percorso positivo. La prova parte da valori di `panda_joint2` e `panda_joint4` vicini a zero e mostra un movimento più ampio verso ready rispetto alla precedente prova di pochi punti. Parametri del builder e criteri di verifica restano quelli già scelti. Il limite temporale e i casi negativi rimangono da implementare e verificare.

## 12. Esercizio 5 — limite all'attesa della verifica

### 12.1 Perché serve un timer

**Consegna del 13 ottobre 2026: da svolgere.** Se dopo il risultato positivo non arriva un campione aggiornato con tutti i giunti, `verification_pending` rimane vero. Serve un controllo periodico indipendente dalla subscription: deve funzionare anche se `/joint_states` smette di arrivare.

Un timer registra una callback periodica nell'executor, che la elabora durante `rclpy.spin`. Non occorre un ciclo di attesa nella callback del risultato o dei giunti. `self.create_timer(periodo_in_secondi, callback)` restituisce il timer; passare il riferimento al metodo senza `()`.

Fonte: [Node.create_timer di rclpy Jazzy](https://github.com/ros2/rclpy/blob/jazzy/rclpy/rclpy/node.py).

### 12.2 Piccolo esercizio guidato

Nel costruttore, dopo l'inizializzazione del flag e dell'istante della verifica e prima della richiesta di pianificazione:

1. Definire `self.verification_timeout_sec = 2.0`.
2. Creare un timer con periodo `0.1` secondi e callback `self.check_verification_timeout`, conservandolo in `self.verification_timer`.

Il periodo è la frequenza richiesta per il controllo; i due secondi sono il limite dell'attesa dei dati dopo il risultato positivo. Non sono un limite alla durata del movimento. L'executor può elaborare il timer in ritardo: non è una garanzia di scadenza esatta.

Matteo scrive `check_verification_timeout(self)` con questi compiti:

1. Ritornare subito se `self.verification_pending` è falso.
2. Leggere `self.get_clock().now().nanoseconds` e sottrarre `self.verification_start_ns`.
3. Dividere la differenza per `1_000_000_000` per ottenere la durata trascorsa in secondi.
4. Se la durata è `>= self.verification_timeout_sec`, emettere un errore che indichi il timeout della verifica e impostare `self.verification_pending = False`.

Il metodo non riceve un messaggio o un Future: soltanto `self`. Il timer rimane periodico; quando il flag è falso il controllo termina subito. Questo consente di evitare ripetizioni del timeout e di mantenere il controllo disponibile per richieste future.

Per questo esercizio si usa l'orologio del nodo, come nel riferimento di attivazione; nella demo è stato verificato `use_sim_time = False`. Quando verrà introdotto il tempo simulato di Gazebo, riesaminare il riferimento del timeout per gestire anche pause e salti del clock: il timer predefinito segue il clock del nodo.

**Consegna:** inviare le righe aggiunte nel costruttore e il nuovo metodo. Nessun timer di timeout è ancora stato scritto o provato dall'assistente nel workspace Ubuntu. Dopo la revisione serviranno una prova positiva e una prova controllata di timeout.

### 12.3 Revisione del primo tentativo del timeout

**13 ottobre 2026: codice ricevuto e rivisto, correzioni ancora da applicare.** Il controllo iniziale del flag, la lettura dell'orologio, la sottrazione dell'istante di attivazione e la conversione in secondi sono corretti. Anche il periodo `0.1` e il riferimento alla callback passato senza parentesi sono corretti.

Nel confronto la soglia va letta come `self.verification_timeout_sec`: il costruttore l'ha definita come attributo dell'istanza, non come variabile locale o globale del metodo. Il nome senza `self` nel frammento non è definito e, quando quel ramo viene elaborato, provoca un errore di risoluzione del nome.

Dopo il log di timeout occorre assegnare `self.verification_pending = False`. L'assegnamento `verification_pending = False` crea invece una variabile locale e lascia attivo il flag del nodo, quindi non impedisce le successive segnalazioni del timer.

Le inizializzazioni `self.verification_timeout_sec = 2.0` e `self.verification_timer = self.create_timer(0.1, self.check_verification_timeout)` devono essere entrambe dentro `__init__`, alla stessa indentazione degli altri attributi e dopo l'inizializzazione del flag e dell'istante. La diversa indentazione delle due righe incollate richiede di controllarne la posizione nel file reale.

Matteo applica le due correzioni a `self` e invia nuovamente il metodo. Il controllo sintattico da solo non verifica la corretta risoluzione dei nomi in un ramo non eseguito; dopo la revisione servirà anche una prova controllata del timeout. Nessuna prova del timeout è stata ancora fornita.

### 12.4 Correzioni confermate dall'utente e piano di prova

**13 ottobre 2026:** Matteo riferisce di aver applicato le correzioni a `self.verification_timeout_sec` e `self.verification_pending`. Il metodo aggiornato non è stato nuovamente incollato; la conferma riguarda le modifiche effettuate, non ancora il comportamento del timeout.

Mantenere attiva la demo e fermare il precedente commander. In un terminale Ubuntu dedicato alla build, con ROS di base:

```bash
source /opt/ros/jazzy/setup.bash
python3 -m py_compile /home/matteo/vision_sort_ws/src/vision_sort_lab/vision_sort_lab/motion_commander.py
```

Se il controllo termina senza errori:

```bash
cd /home/matteo/vision_sort_ws
colcon build --symlink-install --packages-select vision_sort_lab
```

Nel terminale del nodo:

```bash
source /opt/ros/jazzy/setup.bash
source /home/matteo/vision_sort_ws/install/local_setup.bash
ros2 run vision_sort_lab motion_commander
```

**Prova normale:** deve terminare con la verifica positiva. Lasciare il nodo attivo per almeno altri tre secondi: il timer non deve segnalare un timeout dopo una verifica già conclusa.

**Prova controllata del ramo di timeout:** fermare il commander. In `on_joint_state`, dopo gli aggiornamenti del dizionario e dello stamp e dopo il log continuo del dizionario, ma prima del normale controllo del flag, aggiungere temporaneamente:

```python
if self.verification_pending:  # SOLO TEST: sospende la verifica articolare
    return
```

Le due righe devono appartenere al corpo della callback, con indentazione coerente. Mantengono la ricezione e il monitoraggio, ma impediscono al confronto dei giunti di concludere la verifica quando il flag è attivo. Il timer è una callback distinta e deve continuare a essere elaborato dall'executor. Non modificare l'istante di attivazione né il publisher.

Ripetere controllo sintattico, build e riavvio. Dopo il risultato positivo dell'action, attendere almeno tre secondi. Deve comparire circa due secondi dopo l'attivazione un solo log di timeout (`time expired, verification not executed`, nel testo scelto dall'utente), mentre continuano i log del dizionario. La verifica positiva non deve comparire in questa prova. Il test controlla il ramo del timer e la disattivazione del flag; un'interruzione reale della pubblicazione non è ancora stata provata.

**Ripristino:** rimuovere entrambe le righe marcate SOLO TEST, ripetere controllo sintattico, build e riavvio, e confermare nuovamente la verifica positiva senza timeout nei tre secondi successivi. Inviare i log delle prove e confermare la rimozione del blocco temporaneo. Le prove sono ancora da eseguire dall'utente; nessun sorgente Ubuntu è stato modificato dall'assistente.

### 12.5 Prova controllata — timeout osservato

**13 ottobre 2026: output ricevuto da Matteo.** Con il blocco SOLO TEST presente nella callback dei giunti, la pianificazione riesce in `0.014` secondi con `4` punti. Il goal viene accettato e l'esecuzione termina con successo.

```text
1791901524.105793214 — Esecuzione completata con successo
1791901526.203130995 — time expired, verification not executed
```

Fra i timestamp dei due log trascorrono `2.097337781` secondi, coerenti con la soglia di due secondi e il controllo periodico ogni decimo di secondo. L'istante interno di attivazione viene registrato appena dopo il primo log; questa differenza misura l'intervallo fra le stampe.

I log intermedi del dizionario mostrano che i giunti continuano ad arrivare mentre la verifica articolare è sospesa. Il ramo di timeout è quindi stato effettivamente esercitato. Il frammento termina al primo errore: non documenta ancora l'assenza di ripetizioni nei secondi successivi.

**Per chiudere il checkpoint:** lasciare il nodo attivo per almeno altri tre secondi e confermare che il timeout non si ripeta. Poi fermare il commander, rimuovere solo le due righe del blocco SOLO TEST, ripetere controllo sintattico/build/avvio e osservare la verifica positiva senza timeout nei tre secondi successivi. Il ripristino non è ancora stato confermato. Il test resta una sospensione controllata della verifica; non è stata interrotta realmente la pubblicazione di `/joint_states`.

### 12.6 Checkpoint — timeout e ripristino confermati

**13 ottobre 2026:** Matteo conferma che tutte le verifiche richieste funzionano. Il timeout controllato è stato osservato nei log precedenti; la sua mancata ripetizione, la rimozione del blocco SOLO TEST e il ritorno alla verifica positiva senza timeout sono confermati dall'utente, senza ulteriori log allegati.

Il limite all'attesa della verifica è completato per la demo corrente: soglia di `2.0` secondi, controllo ogni `0.1` secondi, segnalazione e disattivazione del flag alla scadenza. La richiesta di pianificazione e l'action non ricevono un limite globale da questo timer. La ripresa automatica dopo un errore e la cancellazione restano da sviluppare. L'interruzione reale della pubblicazione non è stata provata: il timeout è stato esercitato sospendendo temporaneamente il confronto articolare.

## 13. Esercizio 6 — fallimento di pianificazione

### 13.1 Primo passo — revisione del ramo di errore

**Consegna del 13 ottobre 2026: da svolgere.** Prima di introdurre un obiettivo che non produce un piano, Matteo invia il metodo attuale `on_plan_response(self, future)`. La revisione deve verificare la distinzione fra eccezione nel recupero della risposta, codice MoveIt diverso da `SUCCESS` e piano utilizzabile.

Il test successivo dovrà produrre una pianificazione non riuscita e mostrare il codice restituito. In quel caso il nodo non deve inviare un goal di esecuzione e non deve attivare la verifica post-esecuzione. Nessun obiettivo di prova è stato ancora scelto o modificato e nessun fallimento di pianificazione è stato ancora testato sistematicamente.

Proseguire con un solo caso controllato alla volta, ripristinando l'obiettivo valido dopo la prova. Recupero automatico e cancellazione saranno fasi successive, dopo aver verificato e compreso i rami di fallimento.

ciao da matteo

### 13.2 Checkpoint — callback ricevuta e rivista

**13 ottobre 2026: revisione completata sul frammento inviato da Matteo; prova negativa ancora da eseguire.** Il metodo attuale è:

```python
    def on_plan_response(self, future):
        try:
            response = future.result()
        except Exception as exc:
            self.get_logger().error(
                f"Errore nel recupero della risposta: {exc}"
            )
            return

        result = response.motion_plan_response

        if result.error_code.val == MoveItErrorCodes.SUCCESS:
            self.planned_trajectory = result.trajectory
            self.get_logger().info(
                f"Pianificazione riuscita in {result.planning_time:.3f} secondi"
            )
            num_points = len(result.trajectory.joint_trajectory.points)
            self.get_logger().info(
                f"La traiettoria contiene {num_points} punti"
            )
            self.request_execution()
        else:
            self.planned_trajectory = None
            self.get_logger().error(
                f"Error number {result.error_code.val}"
            )
```

Il `try/except` gestisce un'eccezione nel recupero dal Future e termina la callback tramite `return`. Una risposta del servizio con un codice MoveIt non riuscito segue invece il ramo `else`: elimina la traiettoria disponibile, registra il codice e non chiama `request_execution`. Il ramo positivo conserva la traiettoria e richiede l'esecuzione. Questa callback non attiva la verifica articolare; l'attivazione avviene dopo il risultato positivo dell'action.

Il confronto con `MoveItErrorCodes.SUCCESS` è corretto: `val` contiene il codice numerico, `SUCCESS` vale `1`, e non tutti i fallimenti sono negativi (`FAILURE` vale `99999`). `None` indica al nostro codice che non è disponibile una traiettoria; non è una richiesta di cancellazione a ROS. Fonti: [Future.result in rclpy Jazzy](https://github.com/ros2/rclpy/blob/jazzy/rclpy/rclpy/task.py), [MoveItErrorCodes](https://github.com/moveit/moveit_msgs/blob/ros2/msg/MoveItErrorCodes.msg).

Per il nodo attuale, con una singola richiesta all'avvio e `planned_trajectory` inizializzata a `None`, non serve aggiungere un reset nell'`except` per svolgere questa prova. Il controllo della lista dei punti vuota è già documentato in `build_execution_goal` (sezione 7.10); `request_execution` deve continuare a fermarsi quando quel builder restituisce `None`. Questi due metodi non sono stati nuovamente incollati durante questa revisione. Il testo `Error number` può essere reso più esplicito in seguito, ma non impedisce il test.

### 13.3 Primo test negativo — gruppo inesistente

**Consegna del 13 ottobre 2026: da svolgere da Matteo.** Non introduciamo nuove API: usiamo il campo `group_name` già presente in `build_plan_request`. Il campo sceglie il gruppo di giunti su cui MoveIt deve pianificare; nella demo il gruppo del braccio è `panda_arm`, definito nell'SRDF. Un nome inesistente rende la richiesta non valida e permette di esercitare il ramo con codice diverso da `SUCCESS`.

Questa prima prova verifica il rifiuto della richiesta per un gruppo non valido. Non verifica ancora il caso di un obiettivo valido per cui il pianificatore non trova una traiettoria.

Mantenere la demo attiva e fermare il commander. Nel file Ubuntu `/home/matteo/vision_sort_ws/src/vision_sort_lab/vision_sort_lab/motion_builders.py`, dentro `build_plan_request`, sostituire temporaneamente la sola assegnazione del gruppo con:

```python
    plan.group_name = "gruppo_inesistente_test"  # SOLO TEST
```

Lasciare invariati l'obiettivo, il metodo appena rivisto e la logica di verifica. Nel terminale Ubuntu dedicato alla build:

```bash
source /opt/ros/jazzy/setup.bash
cd /home/matteo/vision_sort_ws
python3 -m py_compile src/vision_sort_lab/vision_sort_lab/motion_builders.py
```

Se il controllo termina senza errori:

```bash
colcon build --symlink-install --packages-select vision_sort_lab
```

Nel terminale del nodo:

```bash
source /opt/ros/jazzy/setup.bash
source /home/matteo/vision_sort_ws/install/local_setup.bash
ros2 run vision_sort_lab motion_commander
```

**Risultati da osservare:** richiesta di pianificazione inviata, log `Error number ...` con codice diverso da `1`, nessun log `Goal di esecuzione inviato`, nessun risultato o verifica post-esecuzione. Attendere almeno tre secondi dopo l'errore: il timer della verifica non deve produrre un timeout e il monitoraggio dei giunti deve continuare.

Registrare il numero effettivamente restituito, senza vincolare la prova a `-15`. Il messaggio definisce `INVALID_GROUP_NAME = -15`, ma il sorgente upstream del servizio nel ramo Jazzy può sostituire l'errore con `FAILURE = 99999` quando la pipeline fallisce. La versione installata non è stata ispezionata in questa revisione. Fonte: [servizio GetMotionPlan in MoveIt 2 Jazzy](https://github.com/moveit/moveit2/blob/jazzy/moveit_ros/move_group/src/default_capabilities/plan_service_capability.cpp).

**Ripristino:** fermare il commander, rimettere `plan.group_name = "panda_arm"` e rimuovere il commento SOLO TEST. Ripetere controllo sintattico, build e avvio; confermare pianificazione, esecuzione e verifica positive senza timeout nei tre secondi successivi. Inviare l'output della prova negativa e del ripristino. La prova e il ripristino non sono ancora stati eseguiti o confermati; nessun sorgente Ubuntu è stato modificato dall'assistente.

### 13.4 Checkpoint — primo test negativo e ripristino confermati

**13 ottobre 2026:** Matteo riferisce «funziona tutto» e indica il codice restituito `99999`. Il codice è stato comunicato direttamente dall'utente; non sono stati allegati nuovi log. La conferma riguarda la prova negativa e il ripristino richiesti nella sezione 13.3, inclusa l'assenza di invio dell'esecuzione e di verifica/timeout dopo il fallimento, e il ritorno al percorso positivo con `panda_arm`.

`99999` corrisponde a `MoveItErrorCodes.FAILURE`: è coerente con il comportamento del servizio Jazzy descritto in 13.3. Non identifica da solo la causa specifica; in questa prova la causa introdotta era il nome di gruppo inesistente. Il ramo `else` della callback è quindi verificato per questo caso. Un obiettivo con vincoli incompatibili non è ancora stato provato; recupero e cancellazione restano da realizzare.

### 13.5 Prossimo piccolo esercizio — obiettivo con vincoli incompatibili

**Consegna del 13 ottobre 2026: da svolgere e poi rivedere prima dell'avvio ROS.** Mantenere il gruppo valido `panda_arm` e l'obiettivo `ready` ripristinato. Preparare un test in `build_goal_constraints(target_positions)`, nel modulo Ubuntu `motion_builders.py`, aggiungendo un secondo vincolo sul primo giunto, nello stesso oggetto `goal`.

Non introduciamo nuove API. `JointConstraint()` crea un messaggio distinto, come già avviene nel ciclo; `goal.joint_constraints.append(...)` aggiunge quel messaggio alla lista dei vincoli. Tutti i vincoli di un singolo messaggio `Constraints` devono essere soddisfatti insieme. La lista `goal_constraints` della richiesta contiene invece regioni obiettivo alternative: aggiungere un secondo `Constraints` separato non realizza questa contraddizione. Fonti: [Constraints.msg](https://github.com/moveit/moveit_msgs/blob/ros2/msg/Constraints.msg), [MotionPlanRequest.msg](https://github.com/moveit/moveit_msgs/blob/ros2/msg/MotionPlanRequest.msg).

Nel nostro obiettivo `ready`, il vincolo già costruito per `panda_joint1` richiede `0.0` rad con tolleranze `0.01` sopra e sotto: intervallo `[-0.01, 0.01]`. Un secondo vincolo sullo stesso giunto a `0.5` rad, con le stesse tolleranze, richiede `[0.49, 0.51]`. Gli intervalli non si intersecano; nessuna configurazione può soddisfarli entrambi. Il test riguarda un obiettivo deliberatamente incompatibile, non la probabilità di trovare un percorso verso un obiettivo raggiungibile.

**Matteo scrive il blocco temporaneo:** dopo il ciclo `for`, fuori dal ciclo e prima di `return goal`, creare un nuovo messaggio chiamato `extra_constraint`. Assegnargli `joint_name = "panda_joint1"`, `position = 0.5`, `tolerance_above = 0.01`, `tolerance_below = 0.01` e `weight = 1.0`. Aggiungerlo a `goal.joint_constraints` usando `append`. Segnare inizio e fine del blocco con commenti SOLO TEST per poterlo rimuovere dopo la prova. Non riutilizzare l'oggetto `constraint` rimasto dal ciclo: è già presente nella lista e modificarlo cambierebbe il vincolo dell'ultimo giunto.

**Consegna per la revisione:** inviare la funzione `build_goal_constraints` aggiornata. Il controllo della posizione del blocco e dell'oggetto aggiunto precede la prova. La funzione aggiornata non è ancora stata ricevuta e nessun sorgente Ubuntu è stato modificato dall'assistente. Dopo la revisione si daranno i comandi di prova e ripristino; il caso negativo dovrà ancora mostrare un codice diverso da `SUCCESS`, nessun goal di esecuzione e nessuna attivazione della verifica.

### 13.6 Checkpoint di revisione — vincolo aggiunto correttamente, prova da eseguire

**13 ottobre 2026: funzione ricevuta e rivista.** Matteo ha creato un nuovo `JointConstraint`, fuori dal ciclo `for` e prima di `return goal`, con nome, posizione, tolleranze e peso richiesti. Lo ha aggiunto alla stessa lista `goal.joint_constraints`, conservando i sette vincoli iniziali. Il blocco temporaneo è identificato dal commento `# -----TEST-----`. Non occorrono correzioni funzionali nel frammento.

Funzione scritta dall'utente:

```python
def build_goal_constraints(target_positions):
    goal = Constraints()
    goal.name = "joint_goal"

    for joint_name, position in target_positions.items():
        constraint = JointConstraint()
        constraint.joint_name = joint_name
        constraint.position = position
        constraint.tolerance_above = 0.01
        constraint.tolerance_below = 0.01
        constraint.weight = 1.0
        goal.joint_constraints.append(constraint)

    # -----TEST-----
    extra_constraint = JointConstraint()
    extra_constraint.joint_name = "panda_joint1"
    extra_constraint.position = 0.5
    extra_constraint.tolerance_above = 0.01
    extra_constraint.tolerance_below = 0.01
    extra_constraint.weight = 1.0

    goal.joint_constraints.append(extra_constraint)

    return goal
```

Con l'obiettivo `ready` ripristinato, la lista contiene otto vincoli per sette giunti: due riguardano `panda_joint1` e richiedono intervalli disgiunti. Avere lo stesso nome di giunto due volte nella lista non sostituisce il primo messaggio: `append` conserva entrambi gli oggetti. La prova deve mantenere `plan.group_name = "panda_arm"` per isolare il problema dell'obiettivo.

**Prova da svolgere in Ubuntu WSL:** mantenere la demo attiva e fermare il precedente commander. Nel terminale della build:

```bash
source /opt/ros/jazzy/setup.bash
cd /home/matteo/vision_sort_ws
python3 -m py_compile src/vision_sort_lab/vision_sort_lab/motion_builders.py
```

Se il controllo termina senza errori:

```bash
colcon build --symlink-install --packages-select vision_sort_lab
```

Se la build riesce, nel terminale del nodo:

```bash
source /opt/ros/jazzy/setup.bash
source /home/matteo/vision_sort_ws/install/local_setup.bash
ros2 run vision_sort_lab motion_commander
```

Attendere la risposta del servizio e registrare il codice effettivo: deve essere diverso da `SUCCESS`. Non devono comparire `Goal di esecuzione inviato`, risultato dell'action o verifica articolare. Lasciare il nodo attivo almeno tre secondi dopo il log di errore: il monitoraggio deve continuare senza timeout della verifica. Se il terminale della demo mostra diagnostiche sui vincoli o sul campionamento dell'obiettivo, conservare anche quelle poche righe per interpretare la causa insieme al codice del client.

**Ripristino dopo la prova:** fermare il commander e rimuovere l'intero blocco dal commento `# -----TEST-----` fino a `goal.joint_constraints.append(extra_constraint)` incluso. Conservare `return goal` e il ciclo originale. Ripetere controllo sintattico, build e avvio; confermare pianificazione, esecuzione e verifica positive, senza timeout nei tre secondi successivi. Inviare l'output negativo e quello del ripristino. La revisione è completata; la prova ROS e il ripristino di questo secondo test non sono ancora confermati. Nessun sorgente Ubuntu è stato modificato dall'assistente.

### 13.7 Checkpoint — vincoli incompatibili e ripristino confermati

**13 ottobre 2026:** Matteo conferma «FUNZIONA TUTTO» e chiede di procedere. La conferma riguarda la prova e il ripristino della sezione 13.6: pianificazione non riuscita con il gruppo valido e due vincoli incompatibili, assenza di invio del goal e di verifica/timeout dopo l'errore, monitoraggio ancora attivo, rimozione del blocco TEST e ritorno al percorso positivo. Non sono stati allegati nuovi log né comunicato il codice numerico del secondo test: non lo deduciamo dal `99999` del test precedente.

Il ramo di fallimento della callback è ora verificato nei due casi controllati. Il nodo si ferma prima dell'esecuzione e resta in ascolto; non esegue ancora un recupero automatico. Non sono ancora provati rifiuto del goal, fallimento dell'esecuzione o cancellazione.

### 13.8 Prossimo piccolo esercizio — descrivere i codici MoveIt

**Proposta iniziale del 13 ottobre 2026; collocazione aggiornata nella sezione 13.9 su richiesta di Matteo.** Prima di passare ai fallimenti dell'action, rendere leggibili i codici nei log. La proposta iniziale era un metodo `describe_moveit_error(self, code)` nella classe `MotionCommander`; la consegna attuale è una funzione esterna senza `self`. Riceve il numero e restituisce una stringa. Il collegamento alla callback verrà effettuato dopo la revisione.

Nuova API Python, spiegata prima dell'uso: `dizionario.get(chiave, valore_predefinito)` restituisce il valore associato alla chiave, oppure il valore predefinito se la chiave manca. L'accesso `dizionario[chiave]` richiede invece che la chiave esista. Qui il valore predefinito permette di descrivere anche codici non elencati senza provocare un `KeyError`; nel log conserveremo sempre anche il numero originale.

**Esempio di lettura, non il metodo completo da copiare:**

```python
nomi = {1: "SUCCESS"}
nomi.get(1, "UNKNOWN")    # restituisce "SUCCESS"
nomi.get(123, "UNKNOWN")  # restituisce "UNKNOWN"
```

Matteo costruisce nel metodo un dizionario locale `names`, usando come chiavi le costanti `MoveItErrorCodes.SUCCESS`, `FAILURE`, `PLANNING_FAILED`, `INVALID_GROUP_NAME`, `INVALID_GOAL_CONSTRAINTS`, `TIMED_OUT` e come valori le stringhe con i rispettivi nomi. Le chiavi sono i numeri rappresentati dalle costanti, non stringhe. Restituire il nome usando `get`, con `"UNKNOWN"` come valore predefinito. `MoveItErrorCodes` è già importato nel commander; non serve un nuovo import. Fonte delle costanti: [MoveItErrorCodes.msg](https://github.com/moveit/moveit_msgs/blob/ros2/msg/MoveItErrorCodes.msg).

La stringa `FAILURE` rende il codice `99999` riconoscibile, ma non ricostruisce la causa specifica che il servizio ha eventualmente sostituito con quel codice generico. Il log numerico rimane necessario. **Consegna attuale:** seguire la sezione 13.9 e inviare il modulo con la funzione esterna per la revisione. La funzione e il collegamento ai log non sono ancora implementati o verificati; nessun sorgente Ubuntu è stato modificato dall'assistente.

### 13.9 Decisione — funzione esterna per mantenere semplice il commander

**13 ottobre 2026:** Matteo preferisce collocare la descrizione dei codici in un file separato e importarla nel commander. La funzione dipende solo dal codice ricevuto e dalle costanti MoveIt: è adatta a un modulo di supporto, come i builder già separati. Non serve una nuova classe.

La consegna attuale sostituisce il metodo proposto in 13.8. Matteo crea in Ubuntu `/home/matteo/vision_sort_ws/src/vision_sort_lab/vision_sort_lab/motion_errors.py`. Nel nuovo modulo importa direttamente la dipendenza:

```python
from moveit_msgs.msg import MoveItErrorCodes
```

Definisce a inizio riga `describe_moveit_error(code)`, senza `self`, e scrive il dizionario e il ritorno con `get` richiesti in 13.8. Il modulo deve importare ciò che usa: l'import presente nel commander non rende automaticamente disponibile `MoveItErrorCodes` nel nuovo file.

In Python usiamo `import` per rendere disponibile una funzione di un altro modulo. Nel commander l'import sarà:

```python
from vision_sort_lab.motion_errors import describe_moveit_error
```

`vision_sort_lab` è il package Python, `motion_errors` è il modulo senza estensione `.py`, `describe_moveit_error` è la funzione. Dopo l'import la chiamata sarà, ad esempio:

```python
error_name = describe_moveit_error(result.error_code.val)
```

La chiamata non usa `self`: è una funzione esterna, non un metodo del nodo. Nel commander mantenere l'import di `MoveItErrorCodes`, perché serve ancora nei confronti con `SUCCESS`. Non aggiungere un entry point in `setup.py`: il nuovo modulo non è un eseguibile ROS. **Prossimo passo:** Matteo invia `motion_errors.py` per la revisione; l'import e il collegamento al log saranno verificati dopo. Il file non è ancora stato ricevuto, e nessun sorgente Ubuntu è stato creato o modificato dall'assistente.

### 13.10 Revisione del primo tentativo — dizionario e ritorno

**13 ottobre 2026: primo frammento ricevuto, correzioni da applicare da Matteo.** L'import `from moveit_msgs.msg import MoveItErrorCodes` e la firma della funzione esterna `describe_moveit_error(code)` sono corretti. Il corpo tenta di usare `names = dict{ ... }` con coppie come `SUCCESS = "SUCCESS"`, e manca il ritorno del risultato.

Tre correzioni:

- Per un dizionario scritto con le graffe usare `names = { ... }`, senza `dict` prima della graffa. Le coppie interne si scrivono `chiave: valore`, con i due punti; `=` è usato nell'assegnazione esterna a `names`.
- L'import rende disponibile il nome della classe `MoveItErrorCodes`, non nomi isolati come `SUCCESS`. Ogni chiave deve quindi essere qualificata: ad esempio `MoveItErrorCodes.SUCCESS`. Il valore resta la stringa `"SUCCESS"`. Ripetere per tutte e sei le costanti richieste.
- Dopo la chiusura del dizionario, dentro il corpo della funzione, restituire il risultato di `names.get(code, "UNKNOWN")` usando `return`. Definire soltanto il dizionario non restituisce la descrizione; una funzione che termina senza `return` esplicito restituisce `None`.

**Esempio di lettura limitato a una coppia, da completare con le altre:**

```python
    names = {
        MoveItErrorCodes.SUCCESS: "SUCCESS",
        # aggiungere qui le altre cinque coppie
    }
```

La riga finale richiesta è:

```python
    return names.get(code, "UNKNOWN")
```

`code` è il numero ricevuto dalla funzione e viene cercato fra le chiavi numeriche del dizionario. Conservare l'indentazione di quattro spazi nel corpo della funzione e otto per le coppie interne. **Prossimo passo:** Matteo invia nuovamente il modulo corretto prima dell'integrazione nel commander. Il primo frammento non è sintatticamente valido; la revisione non costituisce una prova del modulo corretto. Nessun sorgente Ubuntu è stato modificato dall'assistente.

### 13.11 Checkpoint di revisione — descrizione dei codici corretta

**13 ottobre 2026: funzione corretta ricevuta e rivista.** Il dizionario usa le sei costanti numeriche qualificate e le stringhe dei nomi; `return names.get(code, "UNKNOWN")` restituisce la descrizione, anche quando il numero non è elencato. Il frammento è corretto. Gli spazi prima di alcuni due punti e l'indentazione più ampia delle coppie non ne alterano il funzionamento; il riferimento sotto uniforma soltanto lo stile.

Modulo scritto dall'utente, con formattazione uniforme:

```python
from moveit_msgs.msg import MoveItErrorCodes


def describe_moveit_error(code):
    names = {
        MoveItErrorCodes.SUCCESS: "SUCCESS",
        MoveItErrorCodes.FAILURE: "FAILURE",
        MoveItErrorCodes.PLANNING_FAILED: "PLANNING_FAILED",
        MoveItErrorCodes.INVALID_GROUP_NAME: "INVALID_GROUP_NAME",
        MoveItErrorCodes.INVALID_GOAL_CONSTRAINTS: "INVALID_GOAL_CONSTRAINTS",
        MoveItErrorCodes.TIMED_OUT: "TIMED_OUT",
    }
    return names.get(code, "UNKNOWN")
```

La revisione del frammento è completata; importazione del modulo nell'ambiente ROS e uso nel log non sono ancora verificati. Nessun sorgente Ubuntu è stato modificato dall'assistente.

### 13.12 Prossimo piccolo esercizio — collegamento al log

**Consegna del 13 ottobre 2026: da svolgere da Matteo.** Nel commander aggiungere, fra gli import a inizio file:

```python
from vision_sort_lab.motion_errors import describe_moveit_error
```

Nel solo ramo `else` di `on_plan_response`, conservare `self.planned_trajectory = None`. Salvare `result.error_code.val` in una variabile locale `error_code`, chiamare `describe_moveit_error(error_code)` e salvare la stringa in `error_name`. Modificare il log di errore perché mostri entrambi, nel formato `Pianificazione fallita: NOME (NUMERO)`. La funzione importata si chiama senza `self`; non introdurre nuove chiamate di pianificazione o esecuzione.

Esempio dell'output desiderato per il codice `99999`:

```text
Pianificazione fallita: FAILURE (99999)
```

Il dizionario rende leggibile il codice, senza ricostruire la causa specifica di un errore generico. **Consegna:** inviare l'import aggiunto e il ramo `else` aggiornato. Dopo la revisione servirà verificare l'importazione e il nuovo log con una prova controllata già nota e il relativo ripristino. Il collegamento non è ancora ricevuto o provato; la revisione non è un nuovo test ROS.

### 13.13 Checkpoint di revisione — log collegato alla funzione esterna

**13 ottobre 2026: callback aggiornata ricevuta e rivista.** Nel ramo negativo Matteo conserva l'invalidazione della traiettoria, legge il numero, chiama la funzione esterna senza `self` e registra nome e numero:

```python
        else:
            self.planned_trajectory = None
            error_code = result.error_code.val
            error_name = describe_moveit_error(error_code)
            self.get_logger().error(
                f"Pianificazione fallita: {error_name} {error_code}"
            )
```

Il ramo è corretto e non richiede l'esecuzione. L'assenza delle parentesi attorno al numero è soltanto una scelta di formattazione. Il ramo positivo e il recupero dal Future sono preservati nel frammento. L'import non è stato incollato: la sua presenza nel file reale non è confermata dalla revisione. Il funzionamento dopo l'integrazione resta da provare; nessun sorgente Ubuntu è stato modificato dall'assistente.

### 13.14 Prova da eseguire — importazione e nuovo log

**Consegna del 13 ottobre 2026: da svolgere da Matteo.** Nel commander verificare la presenza dell'import:

```python
from vision_sort_lab.motion_errors import describe_moveit_error
```

Mantenere la demo attiva e fermare il commander. In `motion_builders.py`, ripetere soltanto il test del gruppo inesistente, con `plan.group_name = "gruppo_inesistente_test"` e commento SOLO TEST. Il blocco con il vincolo extra deve rimanere rimosso, come confermato al checkpoint 13.7.

Nel terminale Ubuntu della build:

```bash
source /opt/ros/jazzy/setup.bash
cd /home/matteo/vision_sort_ws
python3 -m py_compile \
  src/vision_sort_lab/vision_sort_lab/motion_errors.py \
  src/vision_sort_lab/vision_sort_lab/motion_commander.py \
  src/vision_sort_lab/vision_sort_lab/motion_builders.py
```

Se il controllo termina senza errori:

```bash
colcon build --symlink-install --packages-select vision_sort_lab
```

Se la build riesce, nel terminale del nodo:

```bash
source /opt/ros/jazzy/setup.bash
source /home/matteo/vision_sort_ws/install/local_setup.bash
ros2 run vision_sort_lab motion_commander
```

La precedente prova del gruppo inesistente ha restituito `99999`; con quel codice il log aggiornato sarà `Pianificazione fallita: FAILURE 99999`. Registrare comunque il testo effettivo. Non devono comparire errori di importazione o risoluzione del nome, né `Goal di esecuzione inviato`. Attendere almeno altri tre secondi: monitoraggio attivo e nessuna verifica o timeout post-esecuzione.

**Ripristino:** fermare il commander, rimettere il gruppo `panda_arm` togliendo il commento SOLO TEST; conservare modulo, import e nuovo log. Ripetere controllo sintattico, build e avvio per confermare pianificazione, esecuzione e verifica positive senza timeout nei tre secondi successivi. Inviare il nuovo log negativo e confermare il ripristino. La prova dell'integrazione e il ripristino dopo questo test non sono ancora confermati.

### 13.15 Checkpoint — modulo degli errori, nuovo log e ripristino verificati

**13 ottobre 2026:** Matteo conferma «funziona tutto» e chiede di procedere. La conferma riguarda la prova della sezione 13.14: importazione della funzione esterna, log del fallimento con nome e numero, nessun invio del goal o attivazione della verifica nel caso negativo, monitoraggio attivo e ripristino di `panda_arm` con pianificazione, esecuzione e verifica positive. Non sono stati allegati ulteriori log; registriamo la conferma dell'utente senza ricostruire un nuovo output osservato.

`motion_errors.py` fa ora parte dei moduli verificati del package. La funzione non richiede un metodo aggiuntivo nella classe del commander. Il caso `UNKNOWN` è previsto dal codice rivisto, ma non è stato provato separatamente con un codice non elencato. I casi controllati di fallimento della pianificazione e il nuovo log sono verificati; non costituiscono una copertura completa degli errori del servizio. Recupero automatico, rifiuto del goal, fallimento dell'esecuzione e cancellazione restano da sviluppare o provare.

## 14. Esercizio 7 — fallimenti dell'action di esecuzione

### 14.1 Primo passo — revisione della risposta al goal

**Consegna del 13 ottobre 2026: in attesa del frammento attuale.** Matteo invia il metodo completo `on_execution_goal_response(self, future)` del proprio commander. Prima di scegliere una prova negativa, la revisione deve controllare recupero del goal handle dal Future, gestione dell'eccezione, ramo del goal rifiutato e richiesta del risultato finale soltanto dopo l'accettazione.

Il piano riuscito, l'accettazione del goal e il successo finale dell'esecuzione sono passaggi distinti. `goal_handle.accepted` indica se il server ha accettato il goal; `get_result_async()` richiede separatamente il risultato di quel goal. Queste API sono già presenti nel riferimento studiato in 7.11: non introduciamo una nuova API in questa consegna. Fonte: [ClientGoalHandle e ActionClient in rclpy Jazzy](https://github.com/ros2/rclpy/blob/jazzy/rclpy/rclpy/action/client.py).

La callback non deve attivare la verifica dei giunti al momento dell'accettazione; l'attivazione rimane legata al risultato positivo dell'esecuzione. Il metodo attuale non è ancora stato inviato in questa fase; il riferimento di 7.6 non viene assunto come copia aggiornata del file Ubuntu. Nessuna prova negativa dell'action è stata scelta o eseguita e nessun sorgente Ubuntu è stato modificato dall'assistente.

### 14.2 Revisione del primo frammento — eccezione senza nome

**14 ottobre 2026: metodo attuale ricevuto e rivisto; correzioni da applicare da Matteo.** Il commento sul Future già completato all'ingresso della callback è corretto. Il metodo recupera il goal handle, controlla `accepted`, termina subito nel caso rifiutato e, solo dopo l'accettazione, conserva il handle e registra la callback del risultato. La verifica dei giunti non viene attivata prematuramente.

Nel ramo dell'eccezione, il frammento usa:

```python
        except:
            self.get_logger().error(
                f"Errore nella risposta al goal di esecuzione: {exc}"
            )
            return
```

`except:` non assegna l'eccezione a un nome. Nel frammento `exc` non è definito: se `future.result()` solleva un'eccezione, la valutazione della f-string provoca un `NameError` invece di registrare l'errore originale. Il percorso positivo può funzionare senza mostrare il difetto, perché non entra in quel ramo.

**Prima correzione:** usare la stessa forma già studiata in `on_plan_response`:

```python
        except Exception as exc:
```

`Exception` indica la famiglia di eccezioni da gestire; `as exc` associa l'oggetto eccezione al nome usato nel log. Conservare il log e il `return` già presenti. Non serve un nuovo import.

**Seconda modifica diagnostica:** nel ramo `if not goal_handle.accepted`, usare `self.get_logger().error` invece di `info` per il messaggio `Goal di esecuzione rifiutato`. Il controllo e il `return` sono già corretti; cambiare il livello del log non cambia il comportamento del nodo.

**Consegna:** Matteo applica le due modifiche e invia il metodo aggiornato. Non occorre riscrivere il ramo accettato o spostarlo in un nuovo modulo. Le correzioni non sono ancora ricevute o provate. Il ramo dell'eccezione e quello del rifiuto non sono stati verificati in esecuzione; il solo controllo sintattico non rileva l'uso di `exc` non definito nel ramo non eseguito. Nessun sorgente Ubuntu è stato modificato dall'assistente.

### 14.3 Checkpoint — correzioni riferite e consegne più ampie

**14 ottobre 2026:** Matteo riferisce «ho sistemato», in risposta alle due modifiche richieste in 14.2. Registriamo la conferma di modifica, non una prova dei rami negativi: il metodo aggiornato non è stato nuovamente incollato e non sono stati forniti output del test. Matteo richiede di raggruppare più lavoro in ogni messaggio; la preferenza è ora riportata nella sezione 1.

### 14.4 Consegna completa — test locali della callback e prova positiva

**14 ottobre 2026: da svolgere da Matteo, con una sola restituzione finale di codice e risultati.** Scrivere uno script separato `/home/matteo/vision_sort_ws/check_goal_response.py` per eseguire la callback reale con dati di prova, senza istanziare il nodo. Nel sorgente upstream MoveIt Jazzy il server `ExecuteTrajectory` restituisce `ACCEPT_AND_EXECUTE` alla ricezione del goal: una traiettoria errata non è una prova affidabile del ramo di rifiuto. La versione installata non è stata letta. Questi test verificano la logica del client, non dimostrano un rifiuto reale del server. Fonte: [execute_trajectory_action_capability.cpp, Jazzy](https://github.com/moveit/moveit2/blob/jazzy/moveit_ros/move_group/src/default_capabilities/execute_trajectory_action_capability.cpp).

**API da conoscere prima dell'esercizio:**

- `Future()` da `rclpy.task` crea un Future; `set_exception(RuntimeError("errore di prova"))` lo completa con un'eccezione che `result()` solleverà. `set_result(oggetto)` lo completa con quell'oggetto come risultato. Usare queste operazioni solo sui Future creati nello script di prova. Fonte: [Future, rclpy Jazzy](https://github.com/ros2/rclpy/blob/jazzy/rclpy/rclpy/task.py).
- `Mock()` da `unittest.mock`, incluso in Python, crea un oggetto di prova che registra le chiamate ai propri metodi e genera gli attributi richiesti. `assert_called_once()` controlla una sola chiamata; `assert_not_called()` controlla zero chiamate. Ad esempio `probe.get_logger().error.assert_called_once()` verifica il log d'errore. Fonte: [unittest.mock](https://docs.python.org/3/library/unittest.mock.html).
- `assert condizione` interrompe lo script con `AssertionError` quando la condizione è falsa. Serve a trasformare uno stato inatteso in un fallimento visibile.
- `MotionCommander.on_execution_goal_response(probe, future)` chiama il metodo della classe passando esplicitamente `probe` come `self`. Non costruisce un `MotionCommander` e quindi non esegue il costruttore che invia il movimento. Il probe offre solo gli attributi usati nei rami del test. Il `main()` del commander deve restare protetto da `if __name__ == "__main__":`, come nel riferimento.

**Materiale di supporto per preparare lo script, non soluzione dei due test:**

```python
from unittest.mock import Mock
from rclpy.task import Future
from vision_sort_lab.motion_commander import MotionCommander


def make_probe():
    probe = Mock()
    probe.execute_goal_handle = None
    probe.execute_result_future = None
    probe.verification_pending = False
    return probe
```

Matteo scrive due funzioni e le chiama alla fine dello script:

1. `test_response_exception()`: creare probe e Future nuovi; completare il Future con `RuntimeError("errore di prova")` tramite `set_exception`; chiamare la callback reale; verificare un solo log di errore e nessun log info, `execute_goal_handle` e `execute_result_future` ancora `None`, `verification_pending` ancora falso. Stampare `OK: eccezione` soltanto dopo tutti i controlli.
2. `test_goal_rejected()`: creare probe e Future nuovi; creare `goal_handle = Mock()` e impostare `goal_handle.accepted = False`; completare il Future con il goal handle tramite `set_result`; chiamare la callback reale; verificare un solo log di errore, nessun log info e nessuna chiamata a `goal_handle.get_result_async`; verificare gli stessi tre attributi del probe. Stampare `OK: rifiuto` soltanto dopo tutti i controlli.

Entrambi i test usano Future già completati, coerentemente con l'ingresso nella callback. Non copiare l'implementazione della callback nello script: importare ed eseguire quella del package. Non creare `MotionCommander()`, non inviare goal, non chiamare `rclpy.spin`. Il logger è sostituito dal Mock, quindi i suoi messaggi non sono stampati; le conferme `OK` sono stampate dallo script.

**Verifica:** fermare il commander attivo. Nel terminale della build:

```bash
source /opt/ros/jazzy/setup.bash
cd /home/matteo/vision_sort_ws
python3 -m py_compile check_goal_response.py src/vision_sort_lab/vision_sort_lab/motion_commander.py
```

Se non ci sono errori:

```bash
colcon build --symlink-install --packages-select vision_sort_lab
```

Se la build riesce, in un terminale per le prove:

```bash
source /opt/ros/jazzy/setup.bash
source /home/matteo/vision_sort_ws/install/local_setup.bash
python3 /home/matteo/vision_sort_ws/check_goal_response.py
```

Attesi i due messaggi `OK` senza traceback. Se il test fallisce, conservare il traceback prima di proseguire. Se entrambi passano, con demo attiva, gruppo `panda_arm` e tutti i blocchi temporanei rimossi, eseguire `ros2 run vision_sort_lab motion_commander`: confermare accettazione, risultato positivo, verifica articolare e nessun timeout nei tre secondi successivi. Questa prova normale verifica l'integrazione reale dopo le correzioni; non attiva un caso negativo sul server.

**Consegna finale del blocco:** script scritto, output dei due test e conferma o log della prova positiva. Nessuna implementazione o prova del nuovo script è ancora confermata; nessun sorgente Ubuntu è stato modificato dall'assistente.

### 14.5 Revisione dello script — completare controlli, stampe e avvio

**14 ottobre 2026: primo script ricevuto e rivisto, senza output di esecuzione.** Gli import, il probe, i due Future, il goal handle con `accepted = False`, la chiamata al metodo reale e i controlli delle chiamate ai Mock sono corretti. Nel test di rifiuto è correttamente controllata anche l'assenza di chiamate a `get_result_async`. Restano tre completamenti, da applicare e verificare nello stesso blocco di lavoro.

**Controlli dello stato:** in entrambe le funzioni, dopo la callback e prima della conferma finale, aggiungere:

```python
    assert probe.execute_goal_handle is None
    assert probe.execute_result_future is None
    assert probe.verification_pending is False
```

Questi controlli verificano che il ramo negativo non conservi un goal, non avvii l'attesa del risultato e non attivi la verifica articolare.

**Conferme visibili:** il frammento usa `probe.get_logger.info(...)`. Mancano le parentesi per chiamare `get_logger`, ma anche usando `probe.get_logger().info(...)` si chiamerebbe soltanto il Mock, senza stampare. I controlli dei log devono restare riferiti al logger Mock della callback; le conferme dello script vanno stampate con `print`:

```python
    print("OK: eccezione")
```

nel primo test, e:

```python
    print("OK: rifiuto")
```

nel secondo. Rimuovere tutte le chiamate a `probe.get_logger.info`, incluse quelle ripetute nel secondo test. Stampare ciascuna conferma una sola volta e solo dopo tutti i controlli; aggiungere `info` al logger del test dopo i controlli altererebbe anche la cronologia delle chiamate che stiamo misurando.

**Esecuzione delle funzioni:** il frammento definisce i test ma non li chiama. Aggiungere a fondo file, fuori dalle funzioni:

```python
if __name__ == "__main__":
    test_response_exception()
    test_goal_rejected()
```

Il blocco esegue entrambi i test quando lo script viene avviato direttamente. I test sono normali funzioni: scrivere soltanto `def` non ne esegue il corpo.

**Completare ed eseguire senza una revisione intermedia:** dopo le correzioni ripetere il controllo sintattico dello script e del commander, la build e l'avvio dello script con i comandi della sezione 14.4. Attesi esattamente `OK: eccezione` e `OK: rifiuto`, senza traceback. Se i test passano, con demo attiva e percorso positivo ripristinato, eseguire il commander e confermare accettazione, esecuzione e verifica positive senza timeout nei tre secondi successivi. Inviare insieme script aggiornato, output dei test ed esito Panda; in caso di errore inviare il traceback. I completamenti non sono ancora ricevuti o verificati, e nessun sorgente Ubuntu è stato modificato dall'assistente.

### 14.6 Diagnosi — script non trovato nella cartella corrente

**14 ottobre 2026: errore di percorso ricevuto da Matteo.** Dal prompt `~/vision_sort_ws`, il comando `python3 -m py_compile check_goal_response.py src/vision_sort_lab/vision_sort_lab/motion_commander.py` restituisce `[Errno 2] No such file or directory: 'check_goal_response.py'`. Il percorso relativo dello script viene risolto come `/home/matteo/vision_sort_ws/check_goal_response.py`, dove il comando non trova il file. Non è un errore ROS o un esito negativo dei test: il controllo si ferma prima di esaminare lo script.

**Passo da svolgere in Ubuntu:** individuare il file salvato cercandolo nel workspace:

```bash
find /home/matteo/vision_sort_ws -type f -name 'check_goal_response.py'
```

Se compare un percorso, usare quel percorso completo come primo argomento del controllo sintattico e nel comando `python3` che esegue lo script. Il file può rimanere dove Matteo lo ha salvato; non serve spostarlo per questa prova. Se non compare nulla, verificare nome e percorso nell'editor e salvare lo script completo nella posizione concordata `/home/matteo/vision_sort_ws/check_goal_response.py`. Non creare un file vuoto soltanto per superare il controllo.

Dopo aver risolto il percorso, completare controllo sintattico, build e prove della sezione 14.4, sostituendo il percorso dello script nei comandi se necessario. Il percorso effettivo non è ancora stato comunicato, e nessuna esecuzione dei test è confermata. Nessun file Ubuntu è stato spostato, creato o modificato dall'assistente.

### 14.7 Checkpoint — due test locali e prova Panda riusciti

**14 ottobre 2026:** Matteo riferisce l'output `OK: eccezione` e `OK: rifiuto`, quindi allega il log della prova normale con Panda. Il problema di percorso è risolto; il file indicato dall'utente è `\\wsl.localhost\Ubuntu\home\matteo\vision_sort_ws\check_goal_response.py`, corrispondente a `/home/matteo/vision_sort_ws/check_goal_response.py`. Gli strumenti dell'assistente non riescono a leggere il percorso WSL indicato né il commander nello stesso workspace: non viene confusa questa limitazione con l'assenza del file nell'ambiente dell'utente. Il sorgente finale dello script non è stato nuovamente letto; i test riusciti sono confermati dall'output riferito.

La prova reale allegata mostra piano in `0.018` secondi, `4` punti, goal inviato e accettato, feedback `MONITOR`, risultato positivo e verifica dei sette giunti. Fra accettazione (`1791994965.606448338`) e risultato positivo (`1791994965.945099570`) trascorrono `0.338651232` secondi. È una prova vicina all'obiettivo ready, non una misura della durata di un percorso ampio.

```text
stamp_ns = 1791994965953002668
verification_start_ns = 1791994965945145841
differenza = 7856827 ns = 7.856827 ms
```

Errori da `panda_joint1` a `panda_joint7`: `0.007532`, `0.006944`, `0.005892`, `0.003048`, `0.000709`, `0.008355`, `0.009543` rad. Sono tutti sotto `0.01` rad; il maggiore è quello di `panda_joint7`. La verifica positiva compare una volta. Il monitoraggio prosegue fino a circa `3.64` secondi dopo quell'esito senza timeout nel log allegato.

Il percorso accettato fino alla verifica è già osservato nella prova reale: non aggiungiamo ora un ulteriore test locale dell'accettazione. Il prossimo blocco riguarda il risultato finale dell'action. I test locali del rifiuto non dimostrano un rifiuto effettivo da parte del server MoveIt; nessun fallimento reale dell'esecuzione è ancora stato introdotto.

## 15. Esercizio 8 — risultato negativo dell'esecuzione

### 15.1 Consegna completa — log leggibile e tre casi di risultato

**14 ottobre 2026: da svolgere da Matteo, con codice e output restituiti insieme a fine blocco.** Nel modulo `motion_errors.py` aggiungere al dizionario la coppia `MoveItErrorCodes.CONTROL_FAILED: "CONTROL_FAILED"`. Nel ramo negativo di `on_execution_result` usare la funzione esterna già importata per registrare stato ROS, nome del codice MoveIt e numero. Per un risultato abortito con errore di controllo il formato desiderato è `Esecuzione non riuscita: status ROS=6, codice MoveIt=CONTROL_FAILED (-4)`.

Preservare la condizione positiva esistente: `status == GoalStatus.STATUS_SUCCEEDED` **e** `error_code == MoveItErrorCodes.SUCCESS`. Preservare l'attivazione della verifica e la lettura dell'istante soltanto nel ramo positivo. Nel ramo negativo non attivare la verifica. Il risultato dell'esecuzione contiene due livelli: `response.status` è lo stato finale ROS, `response.result.error_code.val` è il codice MoveIt. Fonti: [GoalStatus Jazzy](https://github.com/ros2/rcl_interfaces/blob/jazzy/action_msgs/msg/GoalStatus.msg), [MoveItErrorCodes](https://github.com/moveit/moveit_msgs/blob/ros2/msg/MoveItErrorCodes.msg).

Nello stesso script di test, importare `GoalStatus` da `action_msgs.msg` e `MoveItErrorCodes` da `moveit_msgs.msg`. Aggiungere a `make_probe` l'inizializzazione `probe.verification_start_ns = None`.

Il Mock può rappresentare anche il contenitore del risultato. **Esempio di preparazione dei dati, non soluzione del test completo:**

```python
response = Mock()
response.status = GoalStatus.STATUS_ABORTED
response.result.error_code.val = MoveItErrorCodes.CONTROL_FAILED
future = Future()
future.set_result(response)
```

Il Future contiene ora una risposta finale, non un goal handle. Si passa alla callback reale con `MotionCommander.on_execution_result(probe, future)`. I Mock generano gli attributi intermedi `result` ed `error_code` mentre vi si accede, come già spiegato in 14.4.

Matteo scrive una funzione `test_execution_case(status, moveit_code, label)` che prepara probe, risposta e Future, chiama la callback e verifica un solo log d'errore, nessun log info, `verification_pending is False` e `verification_start_ns is None`. Stampare `OK: {label}` dopo tutti i controlli. Chiamare la funzione per queste tre combinazioni nel blocco finale, conservando anche i due test del goal già riusciti:

| Stato ROS | Codice MoveIt | Etichetta |
|---|---|---|
| `GoalStatus.STATUS_ABORTED` | `MoveItErrorCodes.CONTROL_FAILED` | `esecuzione abortita` |
| `GoalStatus.STATUS_SUCCEEDED` | `MoveItErrorCodes.CONTROL_FAILED` | `errore MoveIt` |
| `GoalStatus.STATUS_ABORTED` | `MoveItErrorCodes.SUCCESS` | `errore ROS` |

Le ultime due risposte sono volutamente incoerenti: verificano che entrambi i confronti siano richiesti per dichiarare successo. Questa è una prova locale della logica del client e non un errore effettivamente provocato nel controllore Panda.

**Verifica:** con commander fermo, nel terminale della build:

```bash
source /opt/ros/jazzy/setup.bash
cd /home/matteo/vision_sort_ws
python3 -m py_compile check_goal_response.py src/vision_sort_lab/vision_sort_lab/motion_commander.py src/vision_sort_lab/vision_sort_lab/motion_errors.py
```

Se non ci sono errori, eseguire la build già usata: `colcon build --symlink-install --packages-select vision_sort_lab`. Dopo la build, nel terminale delle prove, caricare ROS e `install/local_setup.bash`, poi eseguire `python3 /home/matteo/vision_sort_ws/check_goal_response.py`. Attesi cinque messaggi `OK` senza traceback. La prova normale Panda è già documentata in 14.7; questo blocco si concentra sul nuovo log e sui casi negativi della callback.

**Consegna finale:** `on_execution_result` aggiornato, funzione di test e chiamate ai tre casi, output completo. In caso di errore includere il traceback. La callback attuale non è stata letta tramite WSL; la consegna è basata sui frammenti già discussi nella guida. L'integrazione del nuovo log e i tre nuovi test non sono ancora confermati; nessun sorgente Ubuntu è stato modificato dall'assistente.

### 15.2 Checkpoint — cinque test riusciti e codice ricevuto

**14 ottobre 2026:** Matteo allega l'output completo:

```text
OK: eccezione
OK: rifiuto
OK: esecuzione abortita
OK: errore MoveIt
OK: errore ROS
```

Seguono il modulo degli errori con `CONTROL_FAILED`, lo script completo e `on_execution_result`. I frammenti sono corretti: i test del goal verificano assenza di handle e attesa del risultato nei rami negativi; i tre casi finali controllano log d'errore, nessun log info, flag di verifica falso e istante non impostato. Le tre chiamate usano le combinazioni richieste. La callback recupera il risultato con `except Exception as exc`, richiede entrambi i codici positivi con `and`, legge l'istante e attiva la verifica soltanto nel ramo positivo. Nel ramo negativo chiama `describe_moveit_error(error_code)` e registra stato ROS, nome e numero.

Formato effettivo del log scritto dall'utente:

```python
error_name = describe_moveit_error(error_code)
self.get_logger().error(
    f"Esecuzione non riuscita: status ROS={status}, codice MoveIt={error_name}({error_code})"
)
```

Lo spazio prima della parentesi non è necessario al funzionamento. La stringa fra triple apici nel ramo `else` è materiale esplicativo e non altera il flusso. Non occorrono correzioni funzionali nei frammenti ricevuti. I test locali sono completati, sulla base del codice e dell'output dell'utente. La prova Panda positiva rimane quella allegata in 14.7; nessun fallimento reale dell'esecuzione è ancora stato provocato. Nessun sorgente Ubuntu è stato modificato dall'assistente.

### 15.3 Portata del blocco — due prove principali ancora da fare

**14 ottobre 2026:** Matteo chiede quanti casi di fallimento restino. Per completare il blocco didattico corrente scegliamo due prove principali, senza estendere il lavoro a tutti i codici MoveIt:

1. **Risultato negativo dell'action reale:** mantenere un piano valido e specificare temporaneamente un controllore inesistente nel goal `ExecuteTrajectory`. Osservare accettazione, risultato negativo, nessuna verifica articolare, poi ripristinare il percorso positivo.
2. **Verifica articolare negativa:** provare il ramo che riceve un campione aggiornato ma rileva almeno un giunto fuori tolleranza. La prova positiva e il timeout della verifica sono già verificati; questa prova completa il terzo esito principale del confronto. Modalità controllata da spiegare nel relativo esercizio.

Dopo queste due prove, passare alla cancellazione e a un primo recupero controllato. Questo elenco definisce la portata didattica attuale, non una copertura esaustiva di guasti o timeout di un sistema destinato all'hardware.

**Ricerca per il prossimo esercizio:** il goal `ExecuteTrajectory` espone `controller_names` come lista di stringhe. Nel sorgente upstream Jazzy, una lista vuota lascia la selezione automatica al gestore; un nome specificato ma sconosciuto fa fallire la configurazione della traiettoria. Il server dell'action può accettare il goal e poi terminarlo con `CONTROL_FAILED` e stato abortito. Il caso scelto prova un errore nella preparazione dell'esecuzione, non un guasto del motore mentre il robot è in movimento. Fonti: [ExecuteTrajectory.action](https://github.com/moveit/moveit_msgs/blob/ros2/action/ExecuteTrajectory.action), [TrajectoryExecutionManager Jazzy](https://github.com/moveit/moveit2/blob/jazzy/moveit_ros/planning/trajectory_execution_manager/src/trajectory_execution_manager.cpp), [server ExecuteTrajectory Jazzy](https://github.com/moveit/moveit2/blob/jazzy/moveit_ros/move_group/src/default_capabilities/execute_trajectory_action_capability.cpp).

La versione installata non è stata letta. L'assegnazione temporanea a `goal.controller_names`, i comandi e il ripristino saranno spiegati nella prossima consegna completa prima dell'uso. Nessuna delle due nuove prove è ancora eseguita o confermata.

### 15.4 Consegna completa — action reale con controllore inesistente

**14 ottobre 2026: da svolgere da Matteo.** Il test mantiene valido il piano e rende non valida la scelta del controllore nel goal. Il campo `controller_names` di `ExecuteTrajectory.Goal` è una lista di stringhe con i nomi dei controllori richiesti. Quando la lista è vuota, MoveIt seleziona automaticamente quelli adatti alla traiettoria; con un nome sconosciuto specificato, il gestore Jazzy fallisce la preparazione dell'esecuzione. Il server può accettare il goal e poi terminarlo come abortito con codice `CONTROL_FAILED`. È il caso reale scelto per provare il ramo negativo della callback; non è un guasto del motore durante un movimento. Fonti delle API e del comportamento: sezione 15.3.

**Preparazione:** mantenere la demo Panda attiva e fermare il precedente commander. Conservare gruppo `panda_arm`, obiettivo `ready` e i vincoli originali. Nel metodo `build_execution_goal`, dentro il commander, dopo l'assegnazione della traiettoria e prima di `return goal`, aggiungere alla stessa indentazione:

```python
        goal.controller_names = ["controller_inesistente_test"]  # SOLO TEST
```

Le parentesi quadre indicano una lista con una stringa. Non assegnare una singola stringa direttamente al campo; il messaggio richiede una sequenza di nomi. Il goal continua a contenere la traiettoria pianificata. Creare il goal non invia nulla; l'invio avviene in `request_execution`, già presente.

Nel terminale Ubuntu della build:

```bash
source /opt/ros/jazzy/setup.bash
cd /home/matteo/vision_sort_ws
python3 -m py_compile src/vision_sort_lab/vision_sort_lab/motion_commander.py
```

Se il controllo termina senza errori:

```bash
colcon build --symlink-install --packages-select vision_sort_lab
```

Se la build riesce, nel terminale del nodo:

```bash
source /opt/ros/jazzy/setup.bash
source /home/matteo/vision_sort_ws/install/local_setup.bash
ros2 run vision_sort_lab motion_commander
```

**Osservabili del test negativo:** pianificazione riuscita, goal di esecuzione inviato, goal accettato, risultato negativo. Con il codice discusso e il comportamento upstream Jazzy l'esito atteso è:

```text
Esecuzione non riuscita: status ROS=6, codice MoveIt=CONTROL_FAILED(-4)
```

Lo stato `6` indica `STATUS_ABORTED`; `-4` indica `CONTROL_FAILED`. Registrare comunque i valori effettivi. Nel terminale della demo è attesa una diagnostica che nomini il controllore sconosciuto. Il fallimento avviene durante la preparazione, prima dell'invio della traiettoria a un controllore valido. Dopo il risultato attendere almeno tre secondi: il dizionario dei giunti deve continuare a essere mostrato; non devono comparire successo dell'esecuzione, verifica articolare positiva o timeout della verifica. La verifica non deve partire solo perché il goal è stato accettato.

**Ripristino:** fermare il commander, rimuovere la sola riga con `goal.controller_names` e il commento SOLO TEST. Il goal appena creato torna ad avere la lista predefinita vuota, quindi MoveIt seleziona automaticamente i controllori. Conservare il nuovo log e il modulo degli errori. Ripetere controllo sintattico, build e avvio; confermare pianificazione, esecuzione e verifica positive senza timeout nei tre secondi successivi.

**Consegna finale del blocco:** output del commander nel caso negativo, righe della demo relative al controllore sconosciuto, conferma o log del ripristino. Se l'esito differisce, inviare il log effettivo prima di cambiare ulteriormente il codice. Il test reale e il ripristino non sono ancora eseguiti o confermati; la versione installata sarà verificata dal comportamento osservato. Nessun sorgente Ubuntu è stato modificato dall'assistente.

### 15.5 Checkpoint — risultato negativo dell'action reale osservato

**14 ottobre 2026:** Matteo allega:

```text
[ERROR] [1792011539.118153552] [motion_commander]: Esecuzione non riuscita: status ROS=6, codice MoveIt=CONTROL_FAILED(-4)
```

Il log conferma il risultato negativo reale atteso e l'uso del nome del codice nel ramo d'errore: `STATUS_ABORTED` e `CONTROL_FAILED`. Il frammento non include le diagnostiche della demo, i secondi successivi o il ripristino. Non registriamo quindi ancora assenza di verifica/timeout dopo il fallimento o ritorno al percorso positivo come nuovi fatti osservati. Il ripristino del campo temporaneo viene incluso esplicitamente nella consegna successiva, per permettere l'esecuzione riuscita necessaria al test della verifica.

## 16. Esercizio 9 — verifica articolare negativa

### 16.1 Consegna completa — riferimento di confronto alterato dopo l'esecuzione

**14 ottobre 2026: da svolgere da Matteo.** È l'ultima prova principale del blocco sui fallimenti. Il robot esegue il normale obiettivo `ready`; dopo il risultato positivo si modifica temporaneamente il riferimento usato dal confronto, per ottenere un errore deterministico su un campione aggiornato. Il test esercita il ramo negativo della verifica; non rappresenta un errore fisico del robot.

**Preparazione:** mantenere la demo attiva e fermare il commander. Rimuovere dal metodo `build_execution_goal` la riga `goal.controller_names = ["controller_inesistente_test"]` e il commento SOLO TEST. Il goal torna alla selezione automatica dei controllori. Conservare gruppo `panda_arm`, obiettivo `ready`, vincoli originali e tolleranza di verifica `0.01` rad.

Nel solo ramo positivo di `on_execution_result`, dopo il log `Esecuzione completata con successo` e **prima** della lettura dell'istante e dell'attivazione del flag, aggiungere:

```python
            self.target_positions["panda_joint1"] += 0.5  # SOLO TEST: riferimento verifica
```

Per il valore numerico del dizionario, `+= 0.5` legge il valore, aggiunge mezzo radiante e lo riassegna alla stessa chiave. Il target ready del primo giunto era `0.0`, quindi il riferimento di confronto diventa `0.5`. Non mettere la riga nel costruttore o nel builder: lì cambierebbe l'obiettivo inviato al pianificatore. Nel punto scelto l'esecuzione è già terminata; non viene inviata una nuova richiesta di movimento. Non metterla nella callback dei giunti: lì si ripeterebbe a ogni messaggio. Fonte della sintassi: [assegnamenti aumentati Python](https://docs.python.org/3/reference/simple_stmts.html#augmented-assignment-statements).

Conservare subito dopo, nel ramo positivo:

```python
            self.verification_start_ns = self.get_clock().now().nanoseconds
            self.verification_pending = True
```

Il filtro temporale e la subscription restano quelli già verificati. Il primo campione ammesso viene confrontato con un riferimento intenzionalmente diverso. Si attende un errore circa `0.5` rad per `panda_joint1`, maggiore della tolleranza, e quindi un solo esito negativo della verifica. Non cambiare i dati pubblicati su `/joint_states` né il metodo di confronto.

**Verifica in Ubuntu:** nel terminale della build:

```bash
source /opt/ros/jazzy/setup.bash
cd /home/matteo/vision_sort_ws
python3 -m py_compile src/vision_sort_lab/vision_sort_lab/motion_commander.py
```

Se non ci sono errori:

```bash
colcon build --symlink-install --packages-select vision_sort_lab
```

Se la build riesce, nel terminale del nodo:

```bash
source /opt/ros/jazzy/setup.bash
source /home/matteo/vision_sort_ws/install/local_setup.bash
ros2 run vision_sort_lab motion_commander
```

**Osservabili:** pianificazione riuscita, goal accettato ed esecuzione positiva; campione con stamp successivo all'istante della verifica; errori articolari, con primo giunto fuori tolleranza; un solo esito negativo della verifica. Lasciare il nodo attivo almeno tre secondi: monitoraggio continuo, nessuna ripetizione dell'esito negativo e nessun timeout. Il flag deve essere disattivato dopo un confronto concluso con `False`, come dopo `True`.

**Ripristino finale:** fermare il commander e rimuovere la riga con `+= 0.5` e il commento di test. Riavviare il nodo dopo controllo sintattico e build: il costruttore ricrea il dizionario originale, quindi non occorre sottrarre manualmente `0.5` a un'istanza già in esecuzione. Confermare di nuovo esecuzione e verifica positive, senza timeout nei tre secondi successivi. La riga del controllore inesistente deve rimanere rimossa.

**Consegna finale del blocco:** log dal risultato positivo dell'action all'esito negativo della verifica, inclusi i due istanti e gli errori dei giunti, e output o conferma del ripristino positivo. Se compare ancora `CONTROL_FAILED`, controllare innanzitutto la rimozione del precedente controllore di test. Se l'esito negativo si ripete o appare un timeout, allegare anche quei log. La prova e il ripristino non sono ancora eseguiti o confermati; nessun sorgente Ubuntu è stato modificato dall'assistente.

### 16.2 Checkpoint — confronto fuori tolleranza su dati aggiornati

**14 ottobre 2026:** Matteo allega il risultato positivo dell'esecuzione, i due istanti, i sette errori e `Configurazione fuori tolleranza`.

```text
stamp_ns = 1792012019037938172
verification_start_ns = 1792012019030180641
differenza = 7757531 ns = 7.757531 ms
panda_joint1: errore = 0.499512 rad
```

Gli altri sei errori sono `0.006653`, `0.000697`, `0.006738`, `0.008217`, `0.001232`, `0.006069` rad: tutti entro `0.01`. Il primo giunto è invece fuori tolleranza, come previsto dal riferimento alterato. Il log distingue correttamente successo dell'esecuzione e fallimento della verifica. L'esecuzione positiva conferma anche che il precedente errore di esecuzione non persiste in questa prova.

Il frammento termina all'esito negativo: non documenta ancora i tre secondi successivi o il ripristino del riferimento. Le due prove principali di fallimento sono state osservate; la chiusura del blocco richiede ancora il ripristino positivo e l'assenza di ripetizioni/timeout. Questi controlli sono inclusi nella consegna seguente.

## 17. Esercizio 10 — richiesta di cancellazione

### 17.1 Consegna completa — due metodi e test locali

**Consegna del 14 ottobre 2026, nuovamente attuale per la scelta esplicita riportata in 17.4.** Prima fermare il commander e rimuovere la riga `self.target_positions["panda_joint1"] += 0.5` e il commento SOLO TEST. Conservare rimossa anche la riga del controllore inesistente. Il ripristino sarà verificato nella prova positiva al termine del blocco. La prova negativa deve inoltre produrre un solo esito, come richiesto in 16.1. I nuovi metodi vengono implementati direttamente in `MotionCommander`.

Poi implementare nel commander, senza collegare ancora un timer o una chiamata automatica, `request_cancel(self)` e `on_cancel_response(self, future)`. Inizializzare `self.cancel_future = None` nel costruttore prima della prima richiesta di piano. La richiesta verrà inviata attraverso il goal handle già conservato, non cancellando il Future dell'esecuzione.

**Nuove API, prima dell'uso:** `self.execute_goal_handle.cancel_goal_async()` richiede la cancellazione di quel goal e restituisce un Future della risposta alla richiesta. La risposta contiene `return_code` e `goals_canceling`, la lista dei goal passati allo stato di cancellazione in corso. `CancelGoal.Response.ERROR_NONE` è la costante `0`; con accettazione la lista non è vuota. Importare `CancelGoal` da `action_msgs.srv` per il confronto. Il completamento di questa risposta non è il risultato finale dell'action. Fonti: [ClientGoalHandle Jazzy](https://github.com/ros2/rclpy/blob/jazzy/rclpy/rclpy/action/client.py), [CancelGoal.srv Jazzy](https://github.com/ros2/rcl_interfaces/blob/jazzy/action_msgs/srv/CancelGoal.srv).

**Matteo scrive i metodi:**

- `request_cancel`: se il goal handle è `None`, registrare l'errore e ritornare; altrimenti chiamare `cancel_goal_async`, conservare il Future in `self.cancel_future`, registrare `self.on_cancel_response` con `add_done_callback`, e mostrare il log di richiesta inviata. Conservare il Future del risultato finale già in uso; non attivare la verifica.
- `on_cancel_response`: recuperare la risposta con `try/except Exception as exc` e `return` nell'errore. Se `return_code` è `ERROR_NONE` e la lista `goals_canceling` non è vuota, registrare `Richiesta di cancellazione accettata`. Altrimenti registrare un errore con codice e numero di goal nella lista. Non registrare `Robot fermato` o `Cancellazione completata` in questa callback: non sono fatti provati dalla risposta.

**Tre test locali nello script esistente:** aggiungere `cancel_future = None` in `make_probe` e importare `CancelGoal`. Prima dell'uso spiegare `mock_metodo.return_value = oggetto`: imposta ciò che quel metodo di prova restituisce quando viene chiamato. `assert_called_once_with(argomento)` verifica una singola chiamata con quell'argomento.

1. Richiesta: goal handle Mock, suo `cancel_goal_async.return_value` impostato a un Future ancora pendente. Chiamare `MotionCommander.request_cancel(probe)`; verificare una chiamata al metodo del handle e che `probe.cancel_future` sia proprio quel Future. Verificare nessuna chiamata iniziale a `probe.on_cancel_response`; completare poi il Future con una risposta di prova e verificare `probe.on_cancel_response.assert_called_once_with(future)`. Qui la callback della risposta è un Mock: il test verifica il collegamento; i due test seguenti ne verificano il corpo reale.
2. Risposta accettata: Future completato con risposta Mock, `return_code = CancelGoal.Response.ERROR_NONE`, `goals_canceling = [Mock()]`. Chiamare il metodo reale `MotionCommander.on_cancel_response(probe, future)`; verificare un log info, nessun log error e flag di verifica falso.
3. Risposta rifiutata: risposta Mock con `return_code = CancelGoal.Response.ERROR_REJECTED`, `goals_canceling = []`; verificare un log error, nessun log info e flag falso.

Ogni test usa un probe nuovo. Stampare `OK` solo dopo gli assert, chiamare i tre test nel blocco finale dello script e conservare i cinque già riusciti. Attesi otto messaggi `OK`. Completare controllo sintattico dei due file, build e avvio dello script con i comandi già usati. Le due nuove funzioni non sono ancora chiamate dal flusso reale, quindi non viene richiesta alcuna cancellazione alla demo in questo blocco.

**Consegna finale:** i due metodi, i tre test e gli otto output, insieme alla conferma del ripristino positivo. Dopo la revisione si programmerà l'attivazione su un movimento sufficientemente lungo e si leggeranno risposta, risultato finale e stati dei giunti. Nel sorgente upstream Jazzy il callback di cancellazione di ExecuteTrajectory accetta la richiesta senza chiamare direttamente lo stop del gestore; la versione installata non è stata ispezionata. Non dedurre quindi l'arresto dal solo messaggio di accettazione. Fonte: [server ExecuteTrajectory Jazzy](https://github.com/moveit/moveit2/blob/jazzy/moveit_ros/move_group/src/default_capabilities/execute_trajectory_action_capability.cpp).

Nessuna implementazione o prova dei nuovi metodi è ancora confermata, e nessun sorgente Ubuntu è stato modificato dall'assistente.

### 17.2 Proposta superata da 17.4 — separare la gestione dell'action

**14 ottobre 2026:** Matteo chiede nuovamente se il commander si stia appesantendo. La classe raccoglie pianificazione, comunicazione con l'action e verifica dei giunti. Prima di aggiungere ulteriori metodi di cancellazione, l'assistente propone una separazione per responsabilità, mantenendo un solo nodo ROS. Non basta spostare i `def` in funzioni che ricevono l'intero commander: rimarrebbero dipendenti da tutto il suo stato.

La direzione aggiornata è un modulo `/home/matteo/vision_sort_ws/src/vision_sort_lab/vision_sort_lab/motion_execution.py` con una normale classe Python di supporto `MotionExecution`, che riceve il nodo e il riferimento alla callback del risultato. Il componente possiede il client `ExecuteTrajectory`, il goal handle e i Future relativi a invio, risultato e cancellazione. Gestisce invio della traiettoria, accettazione, feedback e in seguito richiesta/risposta di cancellazione. Il risultato finale viene inoltrato alla callback del commander; `on_execution_result` resta nel commander perché decide se attivare la verifica.

Il commander conserva il ruolo di nodo ROS, client della pianificazione, obiettivo e traiettoria pianificata, subscription dei giunti, confronto, filtro temporale e timeout della verifica. I builder e la descrizione dei codici restano nei moduli già separati. La classe di supporto non eredita da `Node`, non ha un proprio `spin` e non richiede un nuovo entry point ROS.

**Ordine del lavoro:** prima rimuovere i blocchi temporanei e confermare il percorso positivo; poi estrarre la gestione dell'action già esistente, senza introdurre contemporaneamente la cancellazione. Adattare i due test della risposta al goal al nuovo componente; i tre test di `on_execution_result` restano riferiti al commander. Ripetere la prova Panda dopo l'estrazione. Aggiungere quindi la cancellazione nel componente, riusando le API e i criteri della sezione 17.1. Se Matteo ha già scritto i due metodi, saranno trasferiti in quella fase.

Questo è l'orientamento architetturale e l'ordine della prossima consegna, non un modulo già implementato. La classe, il collegamento fra componenti e gli aggiornamenti dei test saranno spiegati prima dell'esercizio. Non sono stati creati file Python dall'assistente né confermati refactoring o nuove prove.

### 17.3 Consegna superata da 17.4 — estrazione di MotionExecution

**14 ottobre 2026:** Matteo chiede di procedere. Scrive personalmente il nuovo modulo e le modifiche descritte sotto. Prima rimuovere il riferimento di verifica alterato e il controllore di test, poi confermare la prova positiva con i comandi usuali; ripetere la prova dopo il refactoring. Non aggiungere la cancellazione in questa estrazione: la sezione 17.1 verrà ripresa nel nuovo componente.

**Concetti prima dell'uso:** `MotionExecution` è una normale classe Python. Nel suo costruttore `self` è il componente; `node` è il commander già creato. `self.node = node` conserva un riferimento a quel nodo. Il logger si raggiunge quindi con `self.node.get_logger()`. L'`ActionClient` deve ricevere `self.node`, che è un nodo ROS, come primo argomento. Fonte: [ActionClient Jazzy](https://github.com/ros2/rclpy/blob/jazzy/rclpy/rclpy/action/client.py).

`result_callback` è il riferimento a una funzione/metodo da chiamare al completamento del risultato. Dal commander si passa `self.on_execution_result` senza parentesi: il metodo è già associato all'istanza del commander. Il componente conserva il riferimento in `self.result_callback` e lo registra sul Future del risultato. Non legge il codice finale né attiva la verifica: questi compiti restano in `on_execution_result` del commander.

**Nuovo modulo:** `/home/matteo/vision_sort_ws/src/vision_sort_lab/vision_sort_lab/motion_execution.py`. Importare `ExecuteTrajectory` da `moveit_msgs.action` e `ActionClient` da `rclpy.action`. Definire `class MotionExecution:` senza ereditare da `Node`, con costruttore `__init__(self, node, result_callback)`. Inizializzare `self.node`, `self.result_callback`, l'ActionClient `/execute_trajectory` e i tre attributi `execute_goal_future`, `execute_goal_handle`, `execute_result_future` a `None`. Il costruttore crea il client ma non invia un goal.

**Riferimento del costruttore, non soluzione del componente completo:**

```python
class MotionExecution:
    def __init__(self, node, result_callback):
        self.node = node
        self.result_callback = result_callback
        self.execute_client = ActionClient(
            self.node, ExecuteTrajectory, "/execute_trajectory"
        )
        self.execute_goal_future = None
        self.execute_goal_handle = None
        self.execute_result_future = None
```

Matteo copia dal proprio commander quattro metodi nella nuova classe, mantenendo le protezioni e i log:

| Metodo | Modifica richiesta |
|---|---|
| `build_execution_goal(self, trajectory)` | Riceve esplicitamente la traiettoria. Sostituire i riferimenti a `self.planned_trajectory` con `trajectory`, preservando controlli `None` e punti vuoti. |
| `request_execution(self, trajectory)` | Chiama `self.build_execution_goal(trajectory)`; conserva invio asincrono e callback di accettazione. |
| `on_execution_goal_response(self, future)` | Preserva eccezione e rifiuto; nel ramo accettato registra `self.result_callback` sul Future del risultato, al posto di `self.on_execution_result`. |
| `on_execution_feedback(self, feedback_msg)` | Preserva la lettura del feedback e il log. |

In tutti i metodi spostati sostituire `self.get_logger()` con `self.node.get_logger()`. I tre attributi dell'esecuzione restano sulla classe di supporto con gli stessi nomi. Non copiare `on_execution_result`: resta nel commander con controllo ROS/MoveIt, timestamp e flag. Aggiungere `wait_for_server(self, timeout_sec=1.0)` che restituisce `self.execute_client.wait_for_server(timeout_sec=timeout_sec)`; questo piccolo metodo permette al commander di attendere senza accedere direttamente al client interno.

**Collegamento nel commander:** importare:

```python
from vision_sort_lab.motion_execution import MotionExecution
```

Sostituire la creazione diretta del client dell'action con:

```python
self.execution = MotionExecution(self, self.on_execution_result)
```

Qui il primo `self` è il nodo commander. Nel ciclo di attesa dell'action usare `self.execution.wait_for_server(timeout_sec=1.0)`, conservando `rclpy.ok`, log e ritorni esistenti. Nel ramo positivo di `on_plan_response`, dopo aver conservato il piano, chiamare `self.execution.request_execution(self.planned_trajectory)` al posto di `self.request_execution()`.

Dopo aver copiato e adattato i metodi, rimuovere dalla classe del commander le quattro definizioni spostate e le inizializzazioni dei tre attributi `execute_*`. Conservare `planned_trajectory`, `plan_future` e gli attributi della verifica. Gli import di `ExecuteTrajectory` e `ActionClient` possono essere rimossi dal commander se non usati altrove; conservare `GoalStatus`, `MoveItErrorCodes` e `describe_moveit_error`. Non aggiungere un entry point in `setup.py` o un secondo `spin`. Se metodi di cancellazione sono già stati scritti, conservarne il testo per il blocco successivo, quando saranno adattati al componente.

**Adattamento dei test:** mantenere `make_probe` e i tre casi di `on_execution_result` esistenti. Importare anche `MotionExecution` nello script e creare un secondo helper:

```python
def make_execution_probe():
    probe = Mock()
    probe.node = Mock()
    probe.result_callback = Mock()
    probe.execute_goal_future = None
    probe.execute_goal_handle = None
    probe.execute_result_future = None
    return probe
```

Nei soli due test di eccezione e goal rifiutato usare questo helper e chiamare `MotionExecution.on_execution_goal_response(probe, future)`. I controlli del logger diventano `probe.node.get_logger().error.assert_called_once()` e `probe.node.get_logger().info.assert_not_called()`. Conservare gli assert su handle e Future del risultato ancora `None` e, nel caso rifiutato, su `goal_handle.get_result_async` non chiamato. Sostituire gli assert sui flag della verifica con `probe.result_callback.assert_not_called()`: il componente non possiede quei flag e non deve inoltrare un risultato nei due casi negativi.

**Verifica dopo l'estrazione:** fermare il commander. Nel terminale della build:

```bash
source /opt/ros/jazzy/setup.bash
cd /home/matteo/vision_sort_ws
python3 -m py_compile src/vision_sort_lab/vision_sort_lab/motion_execution.py src/vision_sort_lab/vision_sort_lab/motion_commander.py check_goal_response.py
```

Se non ci sono errori, eseguire `colcon build --symlink-install --packages-select vision_sort_lab`. Dopo la build, nel terminale delle prove, caricare ROS e `install/local_setup.bash`, eseguire lo script e osservare gli stessi cinque messaggi `OK`. Quindi con demo attiva eseguire il commander: piano, accettazione, feedback, risultato positivo e verifica dei sette giunti devono funzionare come prima, con monitoraggio e tre secondi senza timeout. Questo verifica anche che il callback del risultato venga inoltrato correttamente al commander.

**Consegna finale:** nuovo modulo completo, import/costruttore e ramo positivo della risposta al piano modificati, due test adattati, output dei cinque test e prova Panda. In caso di errore includere il traceback. Nessun codice Ubuntu è stato modificato dall'assistente; l'estrazione e il ripristino non sono ancora ricevuti o verificati.

### 17.4 Scelta attuale — conservare l'action nel commander

**14 ottobre 2026:** Matteo richiede esplicitamente «preferisco tenere tutto in motion commander. procediamo cosi». La gestione dell'action, i suoi attributi e le nuove callback di cancellazione rimangono nella classe esistente. La proposta e la consegna di estrazione delle sezioni 17.2–17.3 sono superate. Non creare `MotionExecution` e non adattare i cinque test esistenti a quella classe. I builder e il modulo degli errori già verificati non richiedono modifiche per questa scelta.

La consegna operativa torna a 17.1: due metodi nel commander e tre test locali nel medesimo script. Inizializzare soltanto il nuovo attributo `self.cancel_future = None` dentro `__init__`, prima della prima `request_plan`; non è necessario aggiungere ora altre inizializzazioni dei Future. Conservare l'import di `CancelGoal` per il confronto della risposta. Non collegare ancora i metodi a un timer o al flusso reale: la prima verifica è locale.

I tre test devono usare ogni volta un probe nuovo. Il primo verifica la richiesta e il collegamento della callback con un Future pendente e la proprietà Mock `return_value`; gli altri due invocano direttamente il corpo reale di `on_cancel_response` con risposta accettata e rifiutata. Conservare i cinque test già riusciti: attesi otto messaggi `OK`. Il test della risposta accettata indica l'accettazione della richiesta, non il completamento dell'arresto.

Prima di concludere il blocco, confermare anche il ripristino della verifica normale: riga `+= 0.5` e controllore inesistente rimossi, esecuzione e verifica positive, monitoraggio senza timeout nei tre secondi successivi. Dopo la revisione di metodi, test e output si programmerà la prova reale della cancellazione. Non sono state fornite nuove implementazioni o prove e nessun sorgente Ubuntu è stato modificato dall'assistente.

### 17.5 Revisione di request_cancel — testo del log da completare

**14 ottobre 2026: metodo ricevuto e rivisto.** Matteo controlla `self.execute_goal_handle is None`, registra un errore e termina; altrimenti chiama `cancel_goal_async`, conserva il Future, registra `on_cancel_response` e mostra il log di richiesta inviata. Il flusso è corretto nei limiti dell'esercizio. Il ramo `else` dopo il `return` è valido e può rimanere; non occorre ristrutturare il metodo.

Nel ramo senza handle il logger è già usato correttamente. Sostituire il testo provvisorio `"dimmi come registrare questo errore"` con:

```python
            self.get_logger().error(
                "Impossibile richiedere la cancellazione: nessun goal di esecuzione disponibile"
            )
```

È un controllo dello stato del nodo: non è stata sollevata un'eccezione e non serve usare `exc` o un `try/except` in quel ramo. Il messaggio descrive l'assenza del goal handle; non sostiene che la sola presenza di un handle significhi movimento ancora attivo, perché un handle può rimanere disponibile anche dopo un risultato finale.

**Proseguire nello stesso blocco:** applicare il testo e completare `on_cancel_response` e i tre test di 17.1, senza richiedere una nuova revisione per il solo log. Nella risposta controllare sia `return_code == CancelGoal.Response.ERROR_NONE` sia la lista `goals_canceling` non vuota, conservando `try/except` e `return`. In caso negativo mostrare codice e `len(response.goals_canceling)`. Concludere con gli otto messaggi `OK` e la conferma del ripristino Panda positivo. La callback della risposta, i tre test di cancellazione e nuove prove non sono ancora stati forniti; nessun sorgente Ubuntu è stato modificato dall'assistente.

### 17.6 Revisione del primo on_cancel_response — campi e condizione

**15 ottobre 2026: callback ricevuta e rivista; correzioni da applicare da Matteo.** Il `try/except Exception as exc` e il `return` nel ramo di eccezione sono impostati correttamente. Il frammento assegna però l'intera risposta al nome `goals_canceling`, usa `iself` nel logger, verifica una condizione invertita e legge nomi non definiti nei log.

**Risposta e campi:** `future.result()` restituisce il contenitore del servizio `CancelGoal`, con `return_code` numerico e lista `goals_canceling`. Usare `response = future.result()` nel `try`, poi ricavare:

```python
        return_code = response.return_code
        num_goals = len(response.goals_canceling)
```

`num_goals` è un conteggio, non il numero identificativo del goal. I nomi `error_code` e `goal` usati nella f-string ricevuta non sono definiti nel metodo. Le variabili locali appena ricavate devono essere usate nel log.

**Accettazione:** occorrono codice `CancelGoal.Response.ERROR_NONE` e lista non vuota. La condizione proposta nel frammento `not goals_canceling and self.error_name is not "ERROR_NONE"` non esprime questo controllo: il nome indica attualmente il contenitore intero; `not` richiederebbe invece una lista vuota; il codice va confrontato con una costante numerica, non con una stringa o una descrizione MoveIt. Il servizio di cancellazione ha codici distinti da `MoveItErrorCodes`. Fonte: [CancelGoal.srv Jazzy](https://github.com/ros2/rcl_interfaces/blob/jazzy/action_msgs/srv/CancelGoal.srv).

Condizione corretta, espressa usando i valori appena ricavati:

```python
        if return_code == CancelGoal.Response.ERROR_NONE and num_goals > 0:
```

`==` confronta i valori; `is` e `is not` confrontano l'identità degli oggetti, come nel controllo `is None`. Non usarli per confrontare questo codice con una stringa. `self.error_name` non serve: la risposta contiene direttamente il codice numerico.

**Logger dell'eccezione:** correggere `iself` in `self` e includere `exc` in una f-string, con testo relativo al recupero della risposta, ad esempio `Errore nel recupero della risposta di cancellazione: {exc}`. La richiesta è già stata inviata quando viene elaborata questa callback.

**Logger del ramo negativo:** mostrare `return_code` e `num_goals`, ad esempio:

```python
            self.get_logger().error(
                f"Richiesta di cancellazione non accettata: codice={return_code}, "
                f"goal in cancellazione={num_goals}"
            )
```

Nel ramo positivo mantenere `Richiesta di cancellazione accettata`. Conservare la verifica articolare invariata. **Consegna unica:** applicare tutte le correzioni, completare i tre test locali di 17.1 e inviare metodo corretto, test e output degli otto casi, oltre al ripristino positivo richiesto. I nuovi test di cancellazione non sono ancora stati forniti o eseguiti dall'assistente; nessun sorgente Ubuntu è stato modificato dall'assistente.

### 17.7 Checkpoint e promemoria di ripresa — callback corretta, test ancora da iniziare

**15 ottobre 2026:** Matteo invia la callback corretta e conclude la sessione per andare a dormire. Il recupero della risposta, il logger dell'eccezione, le variabili locali, il confronto numerico con `CancelGoal.Response.ERROR_NONE` e il controllo del numero di goal sono corretti nel frammento. Il ramo positivo registra soltanto l'accettazione della richiesta; non dichiara l'arresto. Nessun output dei nuovi test è stato fornito.

Metodo scritto dall'utente:

```python
    def on_cancel_response(self, future):
        try:
            response = future.result()
        except Exception as exc:
            self.get_logger().error(
                f"Errore nel recupero della risposta di cancellazione: {exc}"
            )
            return
        return_code = response.return_code
        num_goals = len(response.goals_canceling)

        if return_code == CancelGoal.Response.ERROR_NONE and num_goals > 0:
            self.get_logger().info(
                "Richiesta di cancellazione accettata"
            )
        else:
            self.get_logger().error(
                f"Richiesta di cancellazione non accettata: codice={return_code}, "
                f"goal in cancellazione={num_goals}"
            )
```

**Promemoria esplicitamente richiesto per la prossima conversazione:** Matteo deve ancora **iniziare ad aggiornare** `/home/matteo/vision_sort_ws/check_goal_response.py` per i test della cancellazione. Aprire la prossima ripresa ricordando questo punto, prima di assegnare altro lavoro. La richiesta riguarda la ripresa della conversazione.

Nel prossimo blocco riprendere le istruzioni di 17.1 e 17.4: aggiungere `CancelGoal` agli import dello script e `cancel_future = None` in `make_probe`; scrivere i tre test di richiesta/collegamento, risposta accettata e risposta rifiutata; conservare i cinque test già riusciti e chiamare tutti i casi nel blocco finale. Dopo controllo sintattico e build, eseguire lo script: attesi otto messaggi `OK`. Poi confermare il ripristino Panda positivo, senza i due blocchi temporanei e senza timeout nei tre secondi successivi.

**Stato preciso:** callback rivista, tre nuovi test non ancora iniziati, test di cancellazione e arresto reale non verificati. Il ripristino positivo dopo il test del riferimento alterato resta da confermare. Conservare action e cancellazione in `MotionCommander` e le consegne più lunghe concordate. Nessun sorgente Ubuntu è stato modificato dall'assistente.

### 17.8 Checkpoint — otto test locali riusciti

**21 ottobre 2026:** Matteo invia il codice dei tre nuovi test e l'output dello script `/home/matteo/vision_sort_ws/check_goal_response.py`:

```text
OK: eccezione
OK: rifiuto
OK: esecuzione abortita
OK: errore MoveIt
OK: errore ROS
OK: cancel request
OK: cancel request accepted
OK: cancel request rejected
```

Il codice ricevuto è corretto per i tre casi concordati:

- `test_cancel_request`: chiama il vero `MotionCommander.request_cancel` sul probe; verifica un solo invio e che `cancel_future` sia proprio il Future predisposto. La callback del probe non viene chiamata prima del completamento; dopo `set_result` riceve proprio quel Future una volta.
- `test_cancel_accepted`: chiama il vero `on_cancel_response` con `ERROR_NONE` e lista non vuota; verifica un log informativo, nessun errore e verifica articolare inattiva.
- `test_cancel_rejected`: chiama il vero `on_cancel_response` con `ERROR_REJECTED` e lista vuota; verifica un errore, nessun log informativo e verifica articolare inattiva.

Nel primo test `probe.on_cancel_response` è un Mock: si verifica il collegamento della callback. Gli altri due esercitano il corpo della callback reale. La prova usa Future completati localmente, senza inviare richieste al server MoveIt. Il promemoria di iniziare l'aggiornamento dello script è ora soddisfatto. I rami senza goal ed eccezione della risposta di cancellazione non sono fra questi tre test; non sono richiesti nuovi test in questo checkpoint.

**Limiti confermati:** nessun log di cancellazione nella demo ancora ricevuto; ripristino positivo dopo il riferimento alterato ancora da confermare. Nessun sorgente Ubuntu è stato modificato dall'assistente.

### 17.9 Consegna — richiesta temporizzata nella demo

**Da eseguire, 21 ottobre 2026.** Matteo scrive le modifiche; action e cancellazione restano nel commander. Il blocco comprende ripristino positivo, prova osservata e rimozione della strumentazione temporanea.

1. Prima ripristinare il target normale e rimuovere sia `goal.controller_names = ["controller_inesistente_test"]` sia la modifica `self.target_positions["panda_joint1"] += 0.5`, se ancora presenti. Fare build e avvio: attendere esecuzione e verifica positive e altri tre secondi senza timeout. Terminare il commander prima del successivo avvio.
2. Per la sola prova, cambiare il target iniziale di `panda_joint1` da `0.0` a `0.8`, lasciando gli altri sei valori normali. Partire dalla configurazione normale appena verificata, per avere un movimento distinguibile dal comando a posizione già raggiunta.
3. Nuova API prima dell'uso: `Timer.cancel()` disattiva le successive chiamate periodiche di quel timer. Non cancella il goal del robot; quello resta compito di `request_cancel()`. Il timer di `create_timer` è periodico: renderlo monouso disattivandolo all'inizio della propria callback. Fonte: [Timer Jazzy](https://github.com/ros2/rclpy/blob/jazzy/rclpy/rclpy/timer.py).
4. Aggiungere un metodo temporaneo `cancel_once(self)` che prima esegue `self.cancel_test_timer.cancel()` e poi `self.request_cancel()`. Alla fine del ramo accettato di `on_execution_goal_response`, dopo la registrazione di `on_execution_result`, creare `self.cancel_test_timer = self.create_timer(0.3, self.cancel_once)`. Contrassegnare metodo e riga con `SOLO TEST`. Non usare `sleep`, non creare il timer prima del goal handle e non cambiare il timer della verifica.
5. Ripetere controllo sintattico, build e gli otto test locali; poi avviare una sola prova nella demo e raccogliere richiesta, risposta, risultato finale ed eventuale verifica. Osservare anche il movimento in RViz. Il ritardo di 0.3 secondi è nominale e dipende dall'esecuzione delle callback.
6. Togliere il timer temporaneo e `cancel_once`, ripristinare il target di joint1 a `0.0`; conservare `request_cancel` e `on_cancel_response`. Fare build e un nuovo avvio, attendendo verifica positiva e tre secondi senza timeout.

Comandi nel workspace Ubuntu, ripetendo build dopo ogni modifica prima di avviare il nodo:

```bash
cd /home/matteo/vision_sort_ws
python3 -m py_compile check_goal_response.py src/vision_sort_lab/vision_sort_lab/motion_commander.py
colcon build --packages-select vision_sort_lab --symlink-install
source install/setup.bash
python3 /home/matteo/vision_sort_ws/check_goal_response.py
ros2 run vision_sort_lab motion_commander
```

**Interpretazione prima della prova:** una richiesta accettata non dimostra l'arresto. Nel sorgente upstream Jazzy consultato il callback di cancellazione di ExecuteTrajectory restituisce `ACCEPT` senza chiamare direttamente lo stop; il comportamento della versione installata va osservato. Non promettere `STATUS_CANCELED`. Un risultato di esecuzione positivo dopo la richiesta indica che il server ha dichiarato conclusa l'esecuzione con successo; un errore va letto con stato ROS e codice MoveIt. Il codice `CancelGoal` pari a `3` significa goal già terminato. Fonti: [ExecuteTrajectory Jazzy](https://github.com/moveit/moveit2/blob/jazzy/moveit_ros/move_group/src/default_capabilities/execute_trajectory_action_capability.cpp), [CancelGoal Jazzy](https://github.com/ros2/rcl_interfaces/blob/jazzy/action_msgs/srv/CancelGoal.srv).

Se la cancellazione viene accettata ma il movimento termina normalmente, registrare il risultato senza cambiare a tentativi le callback client. Consegna: metodo temporaneo e punto di inserimento del timer, log completi della prova e conferma del ripristino positivo. Non aggiungere ancora recupero automatico o ripianificazione.

### 17.10 Checkpoint — richiesta inviata durante il movimento, risposta con goal già terminato

**21 ottobre 2026:** Matteo invia `cancel_once`, il metodo aggiornato di risposta al goal e un log della demo allegato alla chat. Entrambi i frammenti sono corretti per la prova assegnata:

```python
    # SOLO TEST
    def cancel_once(self):
        self.cancel_test_timer.cancel()
        self.request_cancel()
```

Il timer di `0.3` secondi è creato alla fine del ramo accettato, dopo aver salvato il goal handle e registrato `on_execution_result`. Nel log compare una sola richiesta di cancellazione.

Cronologia tratta dall'output ricevuto; tempi relativi al log di accettazione:

| Tempo ROS nel log | Tempo relativo | Evento |
|---|---|---|
| `1792584925.012426338` | `0.000` s | Goal accettato |
| `1792584925.313510695` | `0.301` s | Richiesta di cancellazione inviata |
| `1792584925.975824838` | `0.963` s | Joint1 a `0.291466` rad |
| `1792584926.975972914` | `1.964` s | Joint1 a `0.721844` rad |
| `1792584927.487353083` | `2.475` s | Cancellazione non accettata: codice `3`, lista vuota |
| `1792584927.487887543` | `2.475` s | Esecuzione completata con successo |
| `1792584927.499725654` | `2.487` s | Configurazione entro tolleranza |

**Significato:** `3` appartiene a `CancelGoal`, non a `MoveItErrorCodes`; è `CancelGoal.Response.ERROR_GOAL_TERMINATED`, quindi al momento della gestione della richiesta il goal era già in uno stato terminale. La richiesta è stata inviata dal client durante il movimento, non dopo la sua conclusione. I successivi campioni confermano che il movimento è proseguito fino a `panda_joint1 = 0.8038588506` rad. Non è stata ottenuta una cancellazione efficace. Fonte: [CancelGoal.srv Jazzy](https://github.com/ros2/rcl_interfaces/blob/jazzy/action_msgs/srv/CancelGoal.srv).

**Interpretazione del server, da distinguere dai fatti osservati:** il comportamento è compatibile con il sorgente upstream Jazzy, che esegue e attende la traiettoria nella callback del goal, nel medesimo gruppo a esecuzione mutuamente esclusiva usato dall'action. La richiesta di cancellazione può essere elaborata soltanto dopo il completamento. Inoltre, il callback di cancellazione upstream restituisce `ACCEPT` senza collegare lo stop. La corrispondenza esatta con il binario installato non è ancora verificata; non attribuire una patch o versione specifica al sistema dell'utente. Non cambiare il timer a tentativi e non presumere che più thread nel solo client risolvano il problema del server. Fonte: [ExecuteTrajectory Jazzy](https://github.com/moveit/moveit2/blob/jazzy/moveit_ros/move_group/src/default_capabilities/execute_trajectory_action_capability.cpp).

**Percorso positivo osservato:** piano in `0.012` s con `26` punti; verifica su campione successivo di `6.925532` ms al risultato, tutti i sette errori inferiori a `0.01` rad, massimo `0.009181` rad. Il log prosegue per oltre dieci secondi senza ripetizioni della verifica o timeout, con posizioni stabili. Questo conferma il percorso positivo con il target di prova a `0.8`; non conferma ancora il ritorno al target normale a `0.0` né la rimozione del codice temporaneo.

**Prossimo blocco:** rimuovere il metodo temporaneo e la riga che crea il timer, conservare richiesta e risposta di cancellazione, riportare joint1 a `0.0`. Ripetere controllo sintattico, build, otto test e avvio con i comandi di 17.9. Attendere verifica positiva e tre secondi senza timeout. Raccogliere inoltre:

```bash
ros2 pkg prefix moveit_ros_move_group
dpkg-query -W ros-jazzy-moveit-ros-move-group
```

Il primo comando mostra il prefisso del pacchetto selezionato dall'ambiente ROS; il secondo la versione del pacchetto binario Ubuntu, se installato. Un prefisso di overlay richiede di distinguere quella build dal pacchetto Ubuntu. Restituire log del ripristino e output dei due comandi. Nessuna modifica al server MoveIt o nuovo esercizio di recupero automatico è ancora assegnato. Nessun sorgente Ubuntu è stato modificato dall'assistente.

### 17.11 Checkpoint — ripristino normale e versione installata

**21 ottobre 2026:** Matteo invia un nuovo log della demo e l'output dei comandi di identificazione. Il pacchetto selezionato da ROS ha prefisso `/opt/ros/jazzy`; `dpkg-query` riporta `ros-jazzy-moveit-ros-move-group 2.12.4-1noble.20260915.202214`. Il precedente comando con prefisso `1.` non era stato eseguito perché la shell interpretava la numerazione come nome del comando; il successivo comando senza numerazione è riuscito. Non sono richieste correzioni all'installazione per quell'errore di copia.

**Ripristino osservato:** joint1 parte da circa `0.790801` rad e arriva a `0.007474947` rad. Piano in `0.012` s, `25` punti; goal accettato ed esecuzione dichiarata riuscita. La verifica usa un campione successivo di `7.245009` ms al riferimento temporale del risultato; tutti i sette errori sono inferiori a `0.01` rad, massimo `0.009032` rad sul quarto giunto. Configurazione dichiarata raggiunta alle `1792585577.519569217`, con log di monitoraggio fino a `1792585581.086144309`: oltre tre secondi senza ulteriori verifiche, richieste di cancellazione o timeout.

Il ritorno al percorso normale è confermato dal comportamento. Non è stato ricevuto un nuovo listato completo da cui attestare la rimozione fisica del metodo temporaneo, né un nuovo output degli otto test in questo messaggio. Gli otto test precedentemente riusciti restano l'ultimo risultato locale documentato. La prova del limite di cancellazione resta associata all'installazione riportata; non è stata dimostrata una corrispondenza riga per riga fra il binario e il sorgente upstream.

**Decisione didattica:** passare al recupero da un fallimento di pianificazione. La cancellazione efficace rimane aperta; non modificare MoveIt né cambiare action in questo blocco. Nessun sorgente Ubuntu è stato modificato dall'assistente.

## 18. Esercizio 11 — un solo nuovo tentativo di pianificazione

**Consegna del 21 ottobre 2026, da scrivere da Matteo e ancora da verificare.** Primo recupero automatico limitato al caso in cui la pianificazione restituisca un errore ammesso. Non applicarlo all'esecuzione fallita o alla verifica fuori tolleranza. Non introdurre timer o nuove API ROS: riutilizzare `request_plan(self.target_positions)`, Future, callback e Mock già studiati.

**Politica scelta per l'esercizio:** massimo due richieste complessive per l'operazione corrente, ossia richiesta iniziale più un solo nuovo tentativo. Ammettere il nuovo tentativo esclusivamente per `MoveItErrorCodes.PLANNING_FAILED` e `MoveItErrorCodes.TIMED_OUT`; questi codici non garantiscono che il secondo tentativo riesca. Altri codici, compreso `FAILURE (99999)`, non attivano recupero automatico. Non correggere di nascosto obiettivi, gruppo, vincoli o controllori.

### 18.1 Modifiche al commander

- Nel costruttore, prima della richiesta iniziale, inizializzare `self.plan_retry_count = 0` e `self.max_plan_retries = 1`. Il contatore rappresenta i nuovi tentativi, non la richiesta iniziale.
- In `on_plan_response`, conservare il ramo positivo e il recupero dell'eccezione. Nel ramo del codice MoveIt negativo conservare `self.planned_trajectory = None` e il log con nome e numero.
- Dopo quel log, verificare entrambe le condizioni: codice appartenente ai due ammessi e `plan_retry_count < max_plan_retries`. La forma `code in (A, B)` verifica se il valore coincide con una delle due costanti.
- Soltanto in quel caso incrementare il contatore prima di inviare una nuova richiesta; registrare un warning, ad esempio `Nuovo tentativo di pianificazione 1/1`, e chiamare `self.request_plan(self.target_positions)`.
- Se le condizioni non sono soddisfatte, terminare la callback senza pianificare o eseguire. Non chiamare direttamente `on_plan_response` e non usare cicli o attese bloccanti.

Non azzerare il contatore dentro `request_plan` o a ogni risposta: altrimenti il limite non funzionerebbe. Il nodo attuale avvia una singola operazione nel costruttore; la gestione del reset per future operazioni separate sarà definita quando verrà aggiunta un'interfaccia per comandi multipli.

### 18.2 Tre test locali del recupero

Conservare gli otto test riusciti in `/home/matteo/vision_sort_ws/check_goal_response.py`. Estendere `make_probe` con contatore e limite come nel nodo e un dizionario `target_positions`. In questi test `probe.request_plan` e `probe.request_execution` rimangono Mock: nessuna richiesta al server. Ogni risposta di pianificazione finta va inserita in un Future nuovo, poi passata al vero `MotionCommander.on_plan_response(probe, future)`.

1. **Limite rispettato:** partire da un probe nuovo, assegnando a `planned_trajectory` un oggetto non nullo. Fornire una risposta `TIMED_OUT`: verificare contatore `1`, traiettoria `None`, una chiamata `request_plan` con `probe.target_positions`, nessuna esecuzione. Sullo stesso probe fornire un secondo Future con un'altra risposta `TIMED_OUT`: il contatore resta `1` e la chiamata di nuova pianificazione resta una sola. Stampare `OK: limite retry piano`.
2. **Codice escluso:** su probe nuovo fornire una risposta `FAILURE`. Verificare contatore `0`, traiettoria `None`, nessuna chiamata a `request_plan` o `request_execution`. Stampare `OK: errore senza retry`.
3. **Recupero riuscito:** su probe nuovo fornire prima `PLANNING_FAILED`, poi una risposta `SUCCESS`. Nel secondo risultato preparare `planning_time = 0.01` e `trajectory.joint_trajectory.points = [Mock()]`, affinché il log esistente possa formattare il tempo e leggere `len(points)`. L'esecuzione rimane finta tramite `probe.request_execution`. Verificare una sola ripianificazione, una sola chiamata a `request_execution` e che `planned_trajectory` sia lo stesso oggetto `trajectory` della risposta positiva. Stampare `OK: recupero piano`.

Preparazione di una risposta finta, usando gli strumenti già noti:

```python
response = Mock()
response.motion_plan_response.error_code.val = MoveItErrorCodes.TIMED_OUT
future = Future()
future.set_result(response)
MotionCommander.on_plan_response(probe, future)
```

Nel test del limite non creare un probe nuovo tra le due risposte, poiché si verifica lo stato della stessa operazione. Non completare due volte lo stesso Future. Conservare i controlli del contatore anche dopo il secondo errore; non è necessario imporre il numero totale di log di tutti i rami.

### 18.3 Verifica e consegna

Eseguire controllo sintattico, build, caricamento dell'ambiente e script con i comandi di 17.9. Attesi gli otto messaggi precedenti più i tre nuovi, totale undici. La prova del recupero in questo blocco è locale e controllata; non falsificare la risposta di un piano reale nel nodo. Un avvio normale della demo può confermare il percorso positivo, ma non dimostra da solo che il nuovo tentativo sia stato esercitato.

Consegna unica: `on_plan_response` aggiornato, inizializzazioni aggiunte, tre test nuovi e output degli undici casi. Nessuna implementazione o prova di questo esercizio è ancora confermata.

### 18.4 Chiarimento — recupero del piano distinto dalla cancellazione

**21 ottobre 2026:** Matteo chiede se il nuovo esercizio ripeta la cancellazione e vuole approfondire perché la prova precedente non abbia fermato il robot. L'assistente riconosce che il passaggio al tema del recupero non era stato spiegato abbastanza. Questo messaggio è un approfondimento concettuale: nessun nuovo codice o test di recupero è stato ricevuto.

**Due operazioni diverse:** pianificare significa chiedere una traiettoria; eseguire significa chiedere di percorrerla. La cancellazione inviata tramite `execute_goal_handle` riguarda il goal di esecuzione già in corso. L'esercizio 18 riguarda invece un esito negativo di `on_plan_response`: ripresentare al massimo una volta lo stesso obiettivo al servizio di pianificazione per i soli codici ammessi, prima di avviare l'esecuzione di quel movimento. Non cancella il goal precedente, non lo reinvia e non ripara il comportamento di cancellazione del server.

**Verifica più precisa della causa:** consultato ora il tag ufficiale MoveIt `2.12.4`, corrispondente alla versione upstream del pacchetto Ubuntu indicato dall'utente. Nel file `execute_trajectory_action_capability.cpp`:

- `initialize` crea un gruppo `MutuallyExclusive` per il server dell'action;
- la callback del goal accettato chiama direttamente `executePathCallback`, che esegue `executePath`;
- `executePath` avvia il gestore di esecuzione e attende con `waitForExecution`, trattenendo la callback fino alla fine;
- il risultato viene dichiarato riuscito o abortito e la callback termina;
- il callback configurato per la cancellazione restituisce solo `ACCEPT`; il metodo separato `preemptExecuteTrajectoryCallback`, che chiamerebbe `stopExecution(true)`, non è collegato lì.

Fonte della versione precisa: [ExecuteTrajectory MoveIt 2.12.4](https://github.com/moveit/moveit2/blob/2.12.4/moveit_ros/move_group/src/default_capabilities/execute_trajectory_action_capability.cpp). I gruppi mutuamente esclusivi impediscono l'esecuzione contemporanea delle proprie callback anche con più thread: [documentazione ufficiale ROS 2 Jazzy](https://github.com/ros2/ros2_documentation/blob/jazzy/source/How-To-Guides/Using-callback-groups.rst).

**Ricostruzione compatibile con l'output:** il client invia la cancellazione dopo circa `0.301` s; il server sta ancora attendendo il completamento della traiettoria nella callback del goal. La gestione della cancellazione resta in attesa; quando può avvenire, il goal è già terminato e la risposta è `ERROR_GOAL_TERMINATED (3)`, lista vuota. Il log del client non misura l'istante esatto di arrivo della richiesta sul server. Il ritardo di elaborazione è una spiegazione supportata dal sorgente e coerente con i tempi, non una traccia interna registrata nel server installato. Non è stato verificato riga per riga il contenuto del binario Ubuntu o di sue eventuali patch.

Il framework ROS controlla i goal cancellabili prima di invocare il callback di cancellazione dell'applicazione: con il goal già terminale, il codice `3` può essere restituito senza passare dal callback MoveIt che esprime `ACCEPT`. Fonti: [server rclcpp_action Jazzy](https://github.com/ros2/rclcpp/blob/jazzy/rclcpp_action/src/server.cpp), [CancelGoal Jazzy](https://github.com/ros2/rcl_interfaces/blob/jazzy/action_msgs/srv/CancelGoal.srv).

**Conseguenze didattiche:** `cancel_goal_async` rende asincrona la richiesta del client, ma non rende automaticamente interrompibile il lavoro del server. Ripetere la richiesta, anticipare ancora il timer o aggiungere thread al solo commander non risolve questa struttura del server. I Mock provano il comportamento client nei casi simulati; non provano che il server reale accetti e attui l'arresto. Per ottenere un arresto effettivo occorrerebbe affrontare il percorso di esecuzione/cancellazione lato server o scegliere un'interfaccia appropriata, con spiegazione e prova specifiche. Nessuna di queste modifiche viene assegnata in questo chiarimento. L'esercizio 18 conserva il proprio scopo separato e resta da realizzare.

### 18.5 Revisione — callback del nuovo tentativo ricevuta

**21 ottobre 2026:** Matteo invia `on_plan_response` aggiornato. Nel frammento sono corretti il mantenimento del ramo positivo, l'azzeramento della traiettoria dopo un codice negativo, il log con nome e numero, la selezione dei soli `PLANNING_FAILED` e `TIMED_OUT`, il confronto del contatore con il limite e la chiamata a `request_plan(self.target_positions)` dopo l'incremento previsto. L'eccezione resta gestita come prima, senza nuovo tentativo.

**Correzione necessaria:** `self.plan_retry_count++` non è sintassi Python valida. Matteo deve sostituirla con:

```python
                self.plan_retry_count += 1
```

`+= 1` incrementa il valore dell'attributo di uno; in questo caso equivale a `self.plan_retry_count = self.plan_retry_count + 1`. Il warning successivo mostrerà quindi `1/1`. Alla seconda risposta negativa dello stesso piano il confronto `1 < 1` è falso e non parte una terza richiesta complessiva.

**Consegna nello stesso blocco:** applicare la correzione; verificare che `plan_retry_count = 0` e `max_plan_retries = 1` siano inizializzati prima della richiesta iniziale e non azzerati in `request_plan`; completare i tre test di 18.2. Eseguire controllo sintattico, build e script; inviare inizializzazioni, test e undici messaggi `OK`. Non richiedere un nuovo passaggio in chat per la sola riga corretta.

**Stato verificato:** revisione del solo frammento; inizializzazioni non inviate, tre nuovi test e loro esecuzione non ancora ricevuti. Nessun sorgente Ubuntu è stato modificato e nessun test è stato eseguito dall'assistente.

### 18.6 Spiegazione operativa dei tre test del piano

**21 ottobre 2026:** Matteo chiede una consegna più esplicita per i test locali. Si chiarisce che viene eseguito il vero corpo di `MotionCommander.on_plan_response`, usando il probe come `self`; i metodi `request_plan` e `request_execution` del probe rimangono Mock. La chiamata a `request_plan` viene registrata, ma non produce una risposta né richiama autonomamente la callback. Per simulare l'esito del secondo tentativo il test deve costruire e passare manualmente un secondo Future completato.

In `/home/matteo/vision_sort_ws/check_goal_response.py`, conservare gli attributi già presenti in `make_probe` e aggiungere:

```python
    probe.plan_retry_count = 0
    probe.max_plan_retries = 1
    probe.target_positions = {"panda_joint1": 0.0}
    probe.planned_trajectory = None
```

Qui il dizionario serve solo a verificare l'argomento della chiamata al Mock; non viene inviato a MoveIt.

Primo test svolto come esempio guidato; Matteo scrive il codice nello script:

```python
def test_plan_retry_limit():
    probe = make_probe()
    probe.planned_trajectory = Mock()

    response1 = Mock()
    response1.motion_plan_response.error_code.val = MoveItErrorCodes.TIMED_OUT
    future1 = Future()
    future1.set_result(response1)
    MotionCommander.on_plan_response(probe, future1)

    assert probe.plan_retry_count == 1
    assert probe.planned_trajectory is None
    probe.request_plan.assert_called_once_with(probe.target_positions)
    probe.request_execution.assert_not_called()

    response2 = Mock()
    response2.motion_plan_response.error_code.val = MoveItErrorCodes.TIMED_OUT
    future2 = Future()
    future2.set_result(response2)
    MotionCommander.on_plan_response(probe, future2)

    assert probe.plan_retry_count == 1
    assert probe.planned_trajectory is None
    probe.request_plan.assert_called_once_with(probe.target_positions)
    probe.request_execution.assert_not_called()

    print("OK: limite retry piano")
```

Il secondo `assert_called_once_with` deve ancora passare: la prima risposta ha richiesto un nuovo piano, la seconda non ne ha richiesto un altro. Non azzerare i Mock o il contatore fra le due risposte. La traiettoria non nulla iniziale serve a verificare che il ramo di fallimento la elimini.

**Secondo test, `test_plan_no_retry`:** partire da un probe nuovo; creare una sola risposta con `response.motion_plan_response.error_code.val = MoveItErrorCodes.FAILURE`, inserirla in un Future completato e chiamare il vero metodo. Verificare contatore `0`, traiettoria `None`, `probe.request_plan.assert_not_called()` e `probe.request_execution.assert_not_called()`. Stampare `OK: errore senza retry`. Questo codice non appartiene ai due ammessi per il nuovo tentativo.

**Terzo test, `test_plan_retry_success`:** partire da un probe nuovo, simulare `PLANNING_FAILED` con lo stesso schema del primo test; verificare contatore `1`, una ripianificazione, nessuna esecuzione. Preparare poi una risposta positiva sullo stesso probe:

```python
    success_response = Mock()
    result = success_response.motion_plan_response
    result.error_code.val = MoveItErrorCodes.SUCCESS
    result.planning_time = 0.01
    result.trajectory.joint_trajectory.points = [Mock()]
```

Inserire `success_response` in un Future nuovo, completarlo e chiamare il vero metodo. Tempo numerico e lista sono necessari perché il ramo positivo formatta `planning_time` con `.3f` e chiama `len(points)`. Verificare infine:

```python
    assert probe.plan_retry_count == 1
    assert probe.planned_trajectory is result.trajectory
    probe.request_plan.assert_called_once_with(probe.target_positions)
    probe.request_execution.assert_called_once()
```

Stampare `OK: recupero piano`. Il controllo con `is` verifica che sia stato conservato lo stesso oggetto traiettoria della risposta positiva. Nessuna esecuzione reale avviene, poiché `probe.request_execution` è un Mock.

Nel blocco `if __name__ == "__main__":` mantenere gli otto test esistenti e aggiungere le chiamate a `test_plan_retry_limit()`, `test_plan_no_retry()` e `test_plan_retry_success()`. Completare correzione `+= 1`, inizializzazioni nel nodo, controllo sintattico, build e script come da 18.3. Attesi undici messaggi `OK`. Questo approfondimento non conferma alcuna nuova implementazione o esecuzione.

### 18.7 Revisione — dieci OK, preparazione incompleta nel test del recupero

**21 ottobre 2026:** Matteo invia i tre test e un output con gli otto casi precedenti, `OK: limite retry piano`, `OK: errore senza retry`, poi `AssertionError` su `probe.plan_retry_count == 1` nel test del recupero. `test_plan_retry_limit` è corretto e l'output ne conferma l'esito nell'ambiente dell'utente. La revisione del recupero e dell'indipendenza dei test evidenzia questi punti:

- In `test_plan_no_retry`, il frammento usa `response` senza crearla nella funzione. Aggiungere `response = Mock()` prima di impostarne il codice. L'output riferisce che il test è passato, ma il frammento non è autonomo: potrebbe risolvere un nome globale già presente oppure non coincidere interamente con il file eseguito. Non dedurre che le variabili locali di altri test siano condivise.
- In `test_plan_retry_success`, dopo il probe nuovo viene assegnato un codice a `response`, ma non viene creato/completato il primo Future né chiamata la callback prima degli assert. Il contatore del probe parte da `0` e solo il vero corpo della callback lo incrementa. Impostare un campo del Mock non esegue la callback.
- Anche il nome `future` usato per il successo non viene creato nella funzione. Predisporre un Future nuovo per ognuna delle due risposte; un Future completato non va riutilizzato con un secondo `set_result`.

Correzione guidata della prima parte di `test_plan_retry_success`, subito dopo `probe = make_probe()` e prima degli assert:

```python
    response = Mock()
    response.motion_plan_response.error_code.val = MoveItErrorCodes.PLANNING_FAILED
    future1 = Future()
    future1.set_result(response)
    MotionCommander.on_plan_response(probe, future1)
```

Mantenere i controlli del contatore, della traiettoria nulla e dell'unica ripianificazione; verificare anche `probe.request_execution.assert_not_called()` prima di simulare il successo. Conservare la preparazione di `success_response`, tempo e lista dei punti. Sostituire poi le due righe che usano `future` con:

```python
    future2 = Future()
    future2.set_result(success_response)
    MotionCommander.on_plan_response(probe, future2)
```

Gli assert finali del recupero sono corretti una volta eseguite entrambe le callback sullo stesso probe. Il ciclo dei test è preparare dati, chiamare il metodo da verificare, controllare effetti; questa sequenza va ripetuta per la seconda risposta. Nessun codice del commander deve essere cambiato sulla base di questo assert del test.

**Da eseguire:** correggere entrambi i test nello script, salvare e rilanciare `python3 /home/matteo/vision_sort_ws/check_goal_response.py`; attesi undici messaggi `OK`. Se si modifica solo lo script esterno al package, non serve rifare la build ROS. L'assistente ha rivisto il codice e aggiornato la guida, senza modificare i sorgenti Ubuntu o eseguire i test.

### 18.8 Checkpoint — undici test locali confermati

**21 ottobre 2026:** Matteo riferisce «andato tutto apposto. continuimo» dopo la consegna delle correzioni e dell'esecuzione dello script. La conferma viene registrata come riuscita degli undici test richiesti, compresi limite di un solo nuovo tentativo, errore escluso e recupero con seconda risposta positiva. Non è stato allegato un nuovo output completo né il codice finale corretto; l'esito è confermato dall'utente. Nessun test è stato eseguito dall'assistente.

Il recupero è verificato sulle risposte simulate nella callback. Non è stata osservata una sequenza reale in cui il servizio abbia restituito prima `PLANNING_FAILED` o `TIMED_OUT` e poi `SUCCESS`. La cancellazione efficace resta un tema distinto e aperto.

### 18.9 Limite del servizio reale e scelta del prossimo blocco

**21 ottobre 2026:** prima di assegnare una prova negativa del retry nella demo, l'assistente controlla il sorgente del tag esatto `2.12.4` di `plan_service_capability.cpp`. Quando `planning_pipeline->generatePlan(...)` restituisce falso, il servizio imposta `mp_res.error_code.val = MoveItErrorCodes::FAILURE` prima di copiare la risposta al client. Anche pipeline non disponibile ed eccezioni producono `FAILURE`. Fonte: [GetMotionPlan MoveIt 2.12.4](https://github.com/moveit/moveit2/blob/2.12.4/moveit_ros/move_group/src/default_capabilities/plan_service_capability.cpp).

Questa implementazione può quindi nascondere al commander i codici specifici ammessi dalla politica. Il comportamento è coerente con il `99999` già osservato. Non estendere automaticamente il retry a tutti i `FAILURE`, perché quel codice include anche errori persistenti di configurazione. Non falsificare il codice della risposta reale per far passare una prova. Non presentare gli undici test locali come dimostrazione di un retry reale della demo. La corrispondenza binaria del pacchetto Ubuntu non è stata ispezionata, ma il sorgente della stessa versione chiarisce perché non conviene assegnare un errore specifico come risultato garantito della prova.

La prova di fallimento del planner annunciata inizialmente in commentary viene pertanto sostituita, prima di assegnarla, da un esercizio sul target configurabile. Il controllo del limite e il recupero con codici specifici restano verificati localmente. Conservare il codice scritto; non modificare il server in questo blocco.

## 19. Esercizio 12 — scegliere il target con un parametro ROS

**Consegna del 21 ottobre 2026, da realizzare da Matteo.** Rendere configurabile all'avvio il target di `panda_joint1`, lasciando gli altri sei valori come nella configurazione normale. Obiettivo pratico: avviare il movimento verso `0.8` e poi verso `0.0` senza modificare e ricostruire il codice fra i due avvii. Ogni processo continua a gestire una sola operazione, con un nuovo contatore del retry inizializzato nel costruttore.

### 19.1 Nuove API prima dell'uso

`self.declare_parameter("target_joint1", 0.0)` dichiara il parametro del nodo e il valore predefinito. Il tipo è ricavato dal default: `0.0` è un numero decimale, quindi tipo ROS double. Un valore fornito all'avvio viene usato al posto del default. La dichiarazione deve avvenire dopo `super().__init__(...)` e prima della lettura del parametro. Fonte: [parametri Python in ROS 2 Jazzy](https://github.com/ros2/ros2_documentation/blob/jazzy/source/Tutorials/Beginner-Client-Libraries/Using-Parameters-In-A-Class-Python.rst).

`self.get_parameter("target_joint1")` restituisce un oggetto `Parameter`; la proprietà `.value` ne legge il valore Python, qui un float. Il valore viene letto una volta nel costruttore e inserito in `self.target_positions`. Fonte: [Parameter in rclpy Jazzy](https://github.com/ros2/rclpy/blob/jazzy/rclpy/rclpy/parameter.py).

Il comando `--ros-args -p target_joint1:=0.8` fornisce il valore al nuovo processo. `--ros-args` introduce gli argomenti ROS, `-p` assegna un parametro, `:=` separa nome e valore. Fonte: [argomenti ROS da terminale](https://github.com/ros2/ros2_documentation/blob/jazzy/source/How-To-Guides/Node-arguments.rst).

### 19.2 Modifica da scrivere

1. Nel costruttore di `/home/matteo/vision_sort_ws/src/vision_sort_lab/vision_sort_lab/motion_commander.py`, dopo l'inizializzazione del nodo e prima del dizionario dei target, dichiarare `target_joint1` con default `0.0`.
2. Nel dizionario sostituire soltanto il valore di `panda_joint1` con `self.get_parameter("target_joint1").value`. Conservare gli altri sei target, il builder e la verifica.
3. Dopo la costruzione del dizionario e prima della richiesta iniziale, aggiungere un log con il valore effettivo scelto per joint1, formattato in radianti con tre decimali. Per esempio, il testo atteso è `Obiettivo panda_joint1: 0.800 rad` quando si passa `0.8`.

Pianificazione e confronto finale devono usare lo stesso `self.target_positions`: il valore da terminale deve cambiare entrambi. Il parametro non è una richiesta di movimento dinamica. In questo esercizio avviare un nuovo processo per ogni comando; non introdurre callback di modifica dei parametri o `ros2 param set`.

### 19.3 Verifica nella demo

Mantenere la demo Panda attiva e terminare il precedente commander. Una sola build dopo la modifica:

```bash
cd /home/matteo/vision_sort_ws
python3 -m py_compile src/vision_sort_lab/vision_sort_lab/motion_commander.py
colcon build --packages-select vision_sort_lab --symlink-install
source install/setup.bash
```

Eseguire separatamente, attendendo esecuzione e verifica e terminando ogni commander con Ctrl+C prima del successivo:

```bash
ros2 run vision_sort_lab motion_commander
```

Atteso target joint1 `0.000` rad e verifica positiva. Poi:

```bash
ros2 run vision_sort_lab motion_commander --ros-args -p target_joint1:=0.8
```

Atteso target `0.800` rad, movimento ed esito della verifica sui sette giunti. Infine tornare al default senza modificare il file:

```bash
ros2 run vision_sort_lab motion_commander
```

Atteso ritorno verso `0.000` rad e verifica positiva. Attendere tre secondi dopo ogni verifica per osservare l'assenza di timeout. Le posizioni misurate possono differire dal target entro la tolleranza `0.01` rad già scelta. Non sono necessari nuovi test con Mock per questa piccola configurazione; le tre prove osservano default, override e ripartenza con default.

**Consegna unica:** frammento del costruttore modificato e log delle tre esecuzioni, includendo target scelto ed esito della verifica. Nessuna nuova implementazione o prova del parametro ancora ricevuta. Nessun sorgente Ubuntu è stato modificato dall'assistente.

### 19.4 Checkpoint — target da terminale riuscito

**21 ottobre 2026:** Matteo allega il log della prova con target da terminale e conferma «funziona tutto correttamente». L'output documenta il movimento del primo giunto da circa `0.008339` a `0.8037175513` rad e la verifica positiva rispetto al target `0.8`.

Piano in `0.028` s, `26` punti; goal accettato ed esecuzione riuscita. Verifica con errori dei sette giunti tutti inferiori a `0.01` rad: joint1 `0.003718`, massimo `0.009936` sul settimo giunto. Il campione usato è successivo di `6.711683` ms al riferimento del risultato. La verifica positiva compare a `1792591303.402834690` e il monitoraggio prosegue fino a `1792591306.897814365`, oltre tre secondi senza timeout o ripetizioni della verifica.

**Distinzione delle evidenze:** l'utente conferma il funzionamento generale dell'esercizio; l'allegato contiene soltanto la prova verso `0.8`, senza gli altri due log della sequenza e senza il costruttore modificato. Non compare il log del target esplicito richiesto nella consegna. Questo non impedisce di proseguire: comportamento e confronto finale della prova allegata sono coerenti con il target indicato dall'utente. Non considerare il listato finale del costruttore rivisto né inventare output non forniti. Nessun sorgente Ubuntu è stato modificato dall'assistente.

**Prossima fase:** iniziare la scena di smistamento attraverso una lettura della scena di collisione di MoveIt. Un nuovo nodo separato evita ulteriori responsabilità nel commander e può essere riutilizzato per controllare le successive aggiunte.

## 20. Esercizio 13 — leggere gli oggetti della scena di MoveIt

**Consegna del 21 ottobre 2026, da realizzare da Matteo.** Creare `/home/matteo/vision_sort_ws/src/vision_sort_lab/vision_sort_lab/scene_inspector.py`. Il nodo non invia movimenti o modifiche della scena: effettua una richiesta per conoscere gli identificativi degli oggetti di collisione già presenti nel mondo di MoveIt. Questa lettura servirà in seguito a verificare l'inserimento di tavolo e oggetti, prima della simulazione fisica.

### 20.1 Nuove interfacce prima dell'uso

- `GetPlanningScene`, da `moveit_msgs.srv`, è un servizio per leggere parti della scena. La richiesta contiene `components`; la risposta contiene `scene`. Fonte: [GetPlanningScene.srv](https://github.com/moveit/moveit_msgs/blob/ros2/srv/GetPlanningScene.srv).
- `PlanningSceneComponents`, da `moveit_msgs.msg`, contiene costanti che selezionano le parti richieste. `WORLD_OBJECT_NAMES` seleziona gli identificativi degli oggetti del mondo. Fonte: [PlanningSceneComponents.msg](https://github.com/moveit/moveit_msgs/blob/ros2/msg/PlanningSceneComponents.msg).
- L'assegnazione `request.components.components = PlanningSceneComponents.WORLD_OBJECT_NAMES` è corretta: il primo `components` è il messaggio contenuto nella richiesta; il secondo è il campo numerico di selezione contenuto in quel messaggio. Non serve studiare combinazioni di bit in questo esercizio.
- La lista restituita è `response.scene.world.collision_objects`; ogni elemento ha un campo `.id`. Il robot e gli oggetti collegati al robot non sono gli oggetti del mondo selezionati da questa richiesta. Fonti: [PlanningSceneWorld.msg](https://github.com/moveit/moveit_msgs/blob/ros2/msg/PlanningSceneWorld.msg), [CollisionObject.msg](https://github.com/moveit/moveit_msgs/blob/ros2/msg/CollisionObject.msg).

`create_client`, `wait_for_service`, `call_async`, Future e `add_done_callback` sono già stati studiati: riutilizzare lo stesso schema del commander.

### 20.2 Struttura da scrivere

Import necessari: `rclpy`, `Node` da `rclpy.node`, `GetPlanningScene` e `PlanningSceneComponents` come sopra.

Creare una classe `SceneInspector(Node)` con nome del nodo `scene_inspector` e tre metodi:

1. `__init__`: inizializzare il nodo, creare `self.scene_client` per `GetPlanningScene` sul servizio `/get_planning_scene`, attendere la disponibilità come già fatto per il servizio del piano, poi chiamare una volta `self.request_scene()`.
2. `request_scene`: creare `GetPlanningScene.Request()`, selezionare `WORLD_OBJECT_NAMES`, inviare con `self.scene_client.call_async(request)`, conservare il risultato in `self.scene_future` e registrare `self.on_scene_response` come callback. Aggiungere un log di richiesta inviata.
3. `on_scene_response(self, future)`: recuperare la risposta con `try/except Exception as exc` e log con `exc`; ritornare in caso di errore. Salvare localmente la lista `response.scene.world.collision_objects`, stamparne il numero e, tramite un ciclo, stampare l'`id` di ogni oggetto. Una lista vuota è un risultato valido: log informativo, non errore.

Completare `main` con inizializzazione ROS, costruzione di `SceneInspector`, `spin` e pulizia come nei nodi già scritti; proteggere con `if __name__ == "__main__":`. La richiesta parte una sola volta. Il nodo può restare in spin fino a Ctrl+C; non aggiungere timer o chiamare shutdown dalla callback.

In `/home/matteo/vision_sort_ws/src/vision_sort_lab/setup.py`, conservare gli entry point esistenti e aggiungere alla lista `console_scripts`:

```python
'scene_inspector = vision_sort_lab.scene_inspector:main',
```

Il pacchetto usa già `rclpy` e `moveit_msgs`: non è richiesto un nuovo pacchetto Python o un nuovo workspace. Non modificare `motion_commander.py` in questo blocco.

### 20.3 Verifica e consegna

Lasciare la demo Panda attiva e terminare il commander precedente. Verificare prima il tipo del servizio nell'ambiente ROS già caricato:

```bash
ros2 service type /get_planning_scene
```

Atteso `moveit_msgs/srv/GetPlanningScene`. Se non è disponibile, controllare che la demo sia attiva; non attribuire l'assenza del servizio a un errore del nuovo nodo.

Dopo aver scritto il file e l'entry point:

```bash
cd /home/matteo/vision_sort_ws
python3 -m py_compile src/vision_sort_lab/vision_sort_lab/scene_inspector.py
colcon build --packages-select vision_sort_lab --symlink-install
source install/setup.bash
ros2 run vision_sort_lab scene_inspector
```

Risultato atteso: servizio disponibile, richiesta inviata, numero degli oggetti del mondo ed eventuali ID. Il numero può essere zero e dipende dalla scena corrente; non fissare nomi attesi o aggiungere oggetti per far apparire un risultato. Non sono necessari test Mock per questo primo client di sola lettura.

**Consegna unica:** file `scene_inspector.py`, nuova riga dell'entry point e output dell'avvio. Dopo la revisione si passerà ad aggiungere una prima geometria alla scena e a verificarne la presenza con questo strumento. Nessun codice del nuovo nodo o risultato di questa prova è ancora stato ricevuto; nessun sorgente Ubuntu è stato modificato dall'assistente.

### 20.4 Supporto editor — sottolineature gialle dopo l'estensione Python

**21 ottobre 2026:** Matteo riferisce di aver installato l'estensione Python raccomandata per VS Code e selezionato l'interprete; ora vede molte sottolineature gialle. Non sono ancora stati forniti messaggi diagnostici, percorso dell'interprete o conferma della connessione WSL. Non attribuire tutti gli avvisi a un problema di import o considerare il progetto danneggiato senza leggere i messaggi.

**Spiegazione:** l'estensione Python può attivare Pylance, che analizza il codice senza eseguirlo. Gli avvisi possono indicare import non trovati nell'ambiente dell'editor, problemi reali come nomi non definiti o altri controlli. Il fatto che ROS esegua il nodo non garantisce che l'editor abbia gli stessi percorsi dei moduli. Fonti: [editing Python in VS Code](https://code.visualstudio.com/docs/python/editing), [diagnosi degli import Pylance](https://github.com/microsoft/pylance-release/blob/main/docs/howto/unresolved-imports.md).

**Informazioni richieste:** copiare il testo completo di uno o due avvisi passando il mouse sulla sottolineatura, indicare il percorso dell'interprete selezionato e se compare `WSL: Ubuntu` nell'indicatore remoto. La richiesta è stata presentata anche mediante domanda asincrona; nessuna risposta ricevuta al momento di questo aggiornamento.

**Primi controlli proposti, non ancora eseguiti o confermati:**

1. Aprire il workspace Ubuntu tramite la connessione WSL di VS Code, con Python/Pylance disponibili sul lato WSL. Un interprete Windows non è quello del progetto ROS in Ubuntu. Fonti: [VS Code con WSL](https://code.visualstudio.com/docs/remote/wsl), [Pylance in ambienti remoti](https://github.com/microsoft/pylance-release/blob/main/docs/howto/remote-development.md).
2. Dal terminale Ubuntu caricare l'ambiente e aprire il workspace:

```bash
cd /home/matteo/vision_sort_ws
source /opt/ros/jazzy/setup.bash
source install/setup.bash
code .
```

3. Verificare l'interprete del terminale e i percorsi effettivi dei moduli:

```bash
python3 -c "import sys, rclpy, moveit_msgs; print(sys.executable); print(rclpy.__file__); print(moveit_msgs.__file__)"
```

4. Nella finestra WSL selezionare tramite `Python: Select Interpreter` lo stesso interprete indicato dal comando. Se gli import funzionano nel terminale e Pylance continua a segnalarli, esaminare i percorsi di ricerca statici; `python.analysis.extraPaths` permette di aggiungere le radici effettive dei moduli. Non assegnare percorsi ROS indovinati prima di vedere l'output. Non confondere il caricamento dell'ambiente nel solo terminale con una riconfigurazione garantita del language server già attivo. Fonte: [risoluzione degli import Pylance](https://github.com/microsoft/pylance-release/blob/main/docs/howto/unresolved-imports.md).

Non reinstallare ROS, non installare copie pip dei pacchetti già funzionanti e non disabilitare genericamente gli avvisi per risolvere questa segnalazione non ancora diagnosticata. Nessuna impostazione di VS Code o sorgente Ubuntu è stato modificato dall'assistente. L'esercizio sulla scena resta il prossimo passo tecnico dopo il chiarimento dell'editor.

### 20.5 Avvisi ricevuti — controllo dell'import di PlanningSceneComponents

**21 ottobre 2026:** Matteo conferma indicatore `WSL: Ubuntu` e interprete `/usr/bin/python3`. Riporta due messaggi Pylance: `"PlanningSceneComponents" is not accessed` e `Import "PlanningSceneComponents" could not be resolved`, con `reportMissingImports`. La riga effettiva di import non è stata allegata.

**Distinzione:** `is not accessed` segnala un nome importato ma non ancora usato; durante la scrittura del nuovo nodo è normale finché non viene usata la costante nella richiesta. `reportMissingImports` segnala invece che Pylance non trova il modulo indicato. Dal nome riportato si sospetta un import del tipo `import PlanningSceneComponents`, ma questa resta un'ipotesi da confrontare con la riga del file.

Import corretti per l'esercizio:

```python
from moveit_msgs.msg import PlanningSceneComponents
from moveit_msgs.srv import GetPlanningScene
```

`moveit_msgs.msg` è il modulo dal quale importare il tipo di messaggio; `PlanningSceneComponents` non è il nome di un pacchetto Python autonomo. Usare poi il tipo con:

```python
request = GetPlanningScene.Request()
request.components.components = PlanningSceneComponents.WORLD_OBJECT_NAMES
```

Questo utilizzo elimina la causa dell'avviso sul nome inutilizzato. Fonte del messaggio e della costante: [PlanningSceneComponents.msg](https://github.com/moveit/moveit_msgs/blob/ros2/msg/PlanningSceneComponents.msg).

**Verifica mirata, se necessaria, nell'ambiente Ubuntu con ROS caricato:**

```bash
source /opt/ros/jazzy/setup.bash
python3 -c "from moveit_msgs.msg import PlanningSceneComponents; print(PlanningSceneComponents.WORLD_OBJECT_NAMES)"
```

Atteso `8`. Se l'import corretto funziona nel terminale ma resta segnalato nell'editor, passare al controllo dei percorsi Pylance descritto in 20.4. Richiedere in quel caso la riga effettiva dell'import e il nuovo messaggio prima di modificare le impostazioni. Nessuna risoluzione ancora confermata dall'utente; nessun sorgente o configurazione modificato dall'assistente.

### 20.6 Screenshot — import corretti di MoveIt, import Node da correggere

**21 ottobre 2026:** Matteo allega lo screenshot di `scene_inspector.py`. Sono visibili:

```python
import rclpy
import Node
from moveit_msgs.msg import PlanningSceneComponents
from moveit_msgs.srv import GetPlanningScene

request = GetPlanningScene.Request()
request.components.components = PlanningSceneComponents.WORLD_OBJECT_NAMES
```

Gli import dei messaggi e del servizio MoveIt sono già corretti e la costante viene usata. La precedente ipotesi di un import diretto `import PlanningSceneComponents` non è confermata dallo screenshot e non va riproposta come causa. Il codice mostrato è un frammento in costruzione, non il nodo completo.

**Errore effettivo nel frammento:** sostituire `import Node` con `from rclpy.node import Node`. `Node` è la classe base importata dal modulo `rclpy.node`. Potrà restare segnalata come inutilizzata finché non viene definita `SceneInspector(Node)`.

**Problema di risoluzione da verificare:** sono sottolineati anche `rclpy`, `moveit_msgs.msg` e `moveit_msgs.srv`. Con WSL e interprete già confermati, il caso è coerente con percorsi ROS non visibili all'analisi statica. Prima verificare nel terminale Ubuntu caricato:

```bash
cd /home/matteo/vision_sort_ws
source /opt/ros/jazzy/setup.bash
source install/setup.bash
python3 -c "from rclpy.node import Node; from moveit_msgs.msg import PlanningSceneComponents; from moveit_msgs.srv import GetPlanningScene; print(PlanningSceneComponents.WORLD_OBJECT_NAMES)"
```

Atteso `8`. Se fallisce, raccogliere il traceback e non considerare sufficiente una modifica ai percorsi dell'editor. Se riesce, generare una proposta JSON dai percorsi effettivi dell'ambiente:

```bash
python3 -c "import json, sys; print(json.dumps({'python.analysis.extraPaths': [p for p in sys.path if p.startswith('/opt/ros/jazzy/')] + ['/home/matteo/vision_sort_ws/src/vision_sort_lab']}, indent=2))"
```

`sys.path` elenca i percorsi di ricerca di Python; il comando seleziona quelli ROS e aggiunge la radice del package del progetto, poi li stampa come impostazione JSON. Nella finestra VS Code del workspace Ubuntu aprire `Preferences: Open Workspace Settings (JSON)` e integrare la proprietà `python.analysis.extraPaths` stampata, conservando le altre impostazioni e unendo eventuali percorsi già presenti. Se il file è vuoto, utilizzare l'intero oggetto JSON. Ricaricare con `Developer: Reload Window` e controllare gli avvisi rimasti. Fonte: [configurazione e diagnosi degli import Pylance](https://github.com/microsoft/pylance-release/blob/main/docs/howto/unresolved-imports.md).

Questo percorso di correzione è proposto prima di ulteriori scambi per ottenere una configurazione basata sui percorsi reali senza indovinarli. Gli avvisi su nomi ancora inutilizzati vanno distinti dagli import non risolti; non promettere che ogni sottolineatura scompaia. Nessuna esecuzione del comando, modifica delle impostazioni o risoluzione è ancora confermata. Nessun file Ubuntu è stato modificato dall'assistente.

### 20.7 Checkpoint — inspector scritto e prima risposta reale

**21 ottobre 2026:** Matteo invia il nodo completo `SceneInspector` e poi l'output dell'avvio: servizio disponibile, richiesta inviata e `Numero oggetti: 0`. La creazione del client, l'attesa condizionata a `rclpy.ok()`, l'invio con `call_async`, il Future conservato, la callback e il recupero di `response.scene.world.collision_objects` sono corretti. Gli import di `Node`, `PlanningSceneComponents` e `GetPlanningScene` sono ora corretti nel listato. Non sono stati forniti nuovi dettagli sulla configurazione Pylance o la scomparsa delle sottolineature.

**Significato del risultato:** la richiesta reale dei nomi degli oggetti del mondo è riuscita. La lista vuota è valida: non contiene il robot stesso o la griglia di visualizzazione di RViz. Non equivale a un errore del servizio né prova che la scena del robot non esista. Fonte dei componenti selezionati: [PlanningSceneComponents.msg](https://github.com/moveit/moveit_msgs/blob/ros2/msg/PlanningSceneComponents.msg).

**Piccole revisioni da applicare nello stesso blocco successivo:**

- Il servizio legge la scena, non pianifica una scena. Cambiare i testi dei log in `Servizio di lettura della scena disponibile`, `In attesa del servizio di lettura della scena…` e `Richiesta di lettura della scena inviata`.
- Il ciclo con indici è valido; preferire la forma diretta e il logger ROS, per mantenere nome del nodo, livello e timestamp:

```python
        for obj in objects:
            self.get_logger().info(f"Oggetto: {obj.id}")
```

- Il corpo di `if rclpy.ok():` nel costruttore è sovraindentato ma coerente e quindi valido; allinearlo allo stile consueto, con quattro spazi aggiuntivi rispetto all'`if`.
- In `main`, `rclpy.try_shutdown()` è attualmente dentro `if scene is not None`. Spostarlo fuori: se il costruttore solleva un'eccezione, l'assegnazione a `scene` non termina, ma il contesto inizializzato va comunque chiuso.

```python
    finally:
        if scene is not None:
            scene.destroy_node()
        rclpy.try_shutdown()
```

Il risultato osservato conferma il client di lettura, senza ancora verificare un ID non vuoto, una modifica della scena o collisioni. Nessun nuovo test automatico è richiesto per le correzioni di stile e pulizia. Non occorre un passaggio in chat per ciascuna correzione. Il codice finale dopo queste revisioni resta da ricevere; nessun sorgente Ubuntu è stato modificato dall'assistente.

## 21. Esercizio 14 — costruire il piano di lavoro come CollisionObject

**Consegna del 21 ottobre 2026, da scrivere da Matteo.** Creare `/home/matteo/vision_sort_ws/src/vision_sort_lab/vision_sort_lab/scene_builders.py` con una funzione senza nodo `build_table_object()`. Il risultato è un messaggio che descrive un piano di lavoro rettangolare. In questo blocco viene costruito il messaggio; il successivo invio con ApplyPlanningScene e la verifica della presenza saranno affrontati dopo la revisione geometrica. Non modificare il commander.

### 21.1 Nuove API e convenzioni prima dell'uso

- `CollisionObject`, da `moveit_msgs.msg`, contiene l'ID, il frame di riferimento, la posa generale, le geometrie, le pose delle geometrie e l'operazione. Usare `CollisionObject.ADD` per l'aggiunta futura; un nuovo ADD con lo stesso ID sostituisce quell'oggetto, non crea un secondo ID. Fonte: [CollisionObject nella versione 2.5.0 dei messaggi](https://github.com/moveit/moveit_msgs/blob/2.5.0/msg/CollisionObject.msg).
- `SolidPrimitive`, da `shape_msgs.msg`, descrive una geometria semplice. Per una scatola usare `.type = SolidPrimitive.BOX` e `.dimensions = [lunghezza_x, lunghezza_y, altezza_z]`, in metri. La scatola è centrata nella propria origine: l'altezza si estende per metà sopra e metà sotto il centro. Fonte: [SolidPrimitive Jazzy](https://github.com/ros2/common_interfaces/blob/jazzy/shape_msgs/msg/SolidPrimitive.msg).
- `Pose`, da `geometry_msgs.msg`, contiene `position` e `orientation`. Per orientamento identità assegnare `orientation.w = 1.0`, con x/y/z della rotazione a zero. Il quaternion di default a quattro zeri non è un orientamento valido.
- `table.header.frame_id = "panda_link0"` rende esplicito il frame delle coordinate. In questo esercizio tenere la posa generale `table.pose` identità (`table.pose.orientation.w = 1.0`, traslazione zero) e specificare il centro della scatola nella sua voce di `primitive_poses`. Le pose delle primitive sono relative alla posa generale dell'oggetto.

### 21.2 Geometria e funzione da scrivere

La funzione deve creare un `CollisionObject` nuovo e restituirlo, con:

| Campo | Valore |
|---|---|
| ID | `work_table` |
| Frame | `panda_link0` |
| Operazione | `CollisionObject.ADD` |
| Posa generale | Identità |
| Tipo primitiva | `SolidPrimitive.BOX` |
| Dimensioni XYZ | `[0.8, 0.8, 0.1]` metri |
| Centro della primitiva XYZ | `(0.6, 0.0, -0.05)` metri |
| Orientamento della primitiva | Identità |

Geometria conseguente: piano superiore a `z = 0.0`, inferiore a `z = -0.1`; estensione X da `0.2` a `1.0`, Y da `-0.4` a `0.4`, nel frame scelto. Il riferimento è la base Panda, non l'origine di una futura scena Gazebo. Le dimensioni sono quelle di una prima superficie di lavoro per la scena di pianificazione, da valutare in RViz dopo l'aggiunta.

Passi della funzione: creare `table`, assegnarne campi base e posa generale; creare una primitiva e una `Pose` per il suo centro; aggiungere la primitiva a `table.primitives` e la posa a `table.primitive_poses`; infine `return table`. Le due liste devono contenere un elemento ciascuna, nello stesso ordine. Non aggiungere `main`, un entry point o richieste ROS a questo modulo di builder.

Se non già presenti, dichiarare nel `package.xml` del pacchetto le dipendenze runtime dirette `geometry_msgs` e `shape_msgs`, conservando le dichiarazioni esistenti. Per un package Python possono essere espresse come:

```xml
<exec_depend>geometry_msgs</exec_depend>
<exec_depend>shape_msgs</exec_depend>
```

Non duplicare dipendenze già dichiarate con `depend` o `exec_depend`.

### 21.3 Verifica e consegna

Applicare anche le piccole correzioni dell'inspector di 20.7. Poi:

```bash
cd /home/matteo/vision_sort_ws
python3 -m py_compile src/vision_sort_lab/vision_sort_lab/scene_builders.py src/vision_sort_lab/vision_sort_lab/scene_inspector.py
colcon build --packages-select vision_sort_lab --symlink-install
source install/setup.bash
python3 -c "from vision_sort_lab.scene_builders import build_table_object; print(build_table_object())"
```

L'ultima istruzione costruisce e stampa il messaggio; non invia modifiche a MoveIt. Il numero di oggetti sul server resta quindi quello precedente. Inviare la funzione e l'output della stampa per rivedere frame, dimensioni, posa e corrispondenza delle liste. Dopo la revisione, applicare il messaggio tramite un servizio dedicato e usare l'inspector per verificare `work_table`. Nessun builder del tavolo o invio della scena è ancora stato ricevuto o verificato.

### 21.4 Chiarimento — pulizia del contesto anche nel commander

**21 ottobre 2026:** Matteo chiede se lo spostamento di `rclpy.try_shutdown()` fuori dal controllo sull'esistenza del nodo vada applicato anche a `motion_commander`, che usa lo stesso schema di `main`. Sì: conservare `destroy_node()` nel ramo che controlla il riferimento non nullo al nodo, mentre `rclpy.try_shutdown()` deve essere nel `finally` ma fuori da quell'`if`. Usare il nome della variabile già presente nel singolo `main`.

Motivo: dopo `rclpy.init()`, il costruttore del nodo può sollevare un'eccezione prima che l'assegnazione alla variabile termini. Se la variabile è stata inizializzata a `None`, non esiste un riferimento da distruggere, ma il contesto ROS deve comunque essere chiuso. La stessa correzione si applica ai due entry point senza modificare pianificazione, action o verifica.

Indicazione fornita; applicazione nei due file ancora da confermare. Nessun nuovo test automatico richiesto e nessun sorgente Ubuntu modificato dall'assistente. La consegna corrente rimane il builder geometrico del piano di lavoro.

### 21.5 Passaggio a una nuova chat — fase della scena di smistamento

**23 ottobre 2026:** Matteo osserva che la costruzione della scena è una fase diversa dalla gestione dei fallimenti e richiede un messaggio da copiare in una nuova chat. Chiede anche un titolo per questa chat nel formato `Vision Sort Lab — fase 4: ...`. L'assistente prepara il testo di passaggio e suggerisce `Vision Sort Lab — fase 4: gestione dei fallimenti e recupero` per la chat attuale, e `Vision Sort Lab — fase 5: scena di smistamento e collisioni` per quella nuova. Titoli proposti, non applicati mediante strumenti; nessuna nuova chat creata.

**Stato da trasferire:** Python/rclpy su ROS 2 Jazzy in Ubuntu WSL; workspace `/home/matteo/vision_sort_ws`, pacchetto `/home/matteo/vision_sort_ws/src/vision_sort_lab`. Panda nella demo MoveIt/RViz, non ancora simulazione fisica in Gazebo. Pianificazione, esecuzione, verifica dei sette giunti e parametro del primo giunto già verificati; undici test locali dei rami di fallimento e recupero confermati. I limiti del servizio del piano e della cancellazione nella versione 2.12.4 sono documentati; la cancellazione efficace non va dichiarata completata.

**Punto concreto della nuova fase:** `scene_inspector.py` scritto dall'utente e provato con `GetPlanningScene`, `WORLD_OBJECT_NAMES`, esito `Numero oggetti: 0`. Il builder del tavolo è soltanto assegnato, non ancora ricevuto o eseguito. Riprendere la funzione `build_table_object()` senza nodo nel nuovo `scene_builders.py`, con i dati geometrici esatti di 21.2. Spiegare prima le nuove API e la distinzione fra frame, posa dell'oggetto e posa della primitiva. Prima costruzione e stampa, poi invio con `ApplyPlanningScene` e verifica tramite inspector; non saltare alla simulazione fisica.

**Correzioni pendenti:** terminologia di lettura della scena nei log; logger nel ciclo degli oggetti; pulizia con `try_shutdown()` fuori dal controllo del nodo in entrambi i main. Non è stata fornita conferma dell'applicazione; non richiedere un passaggio in chat per ciascuna riga. Pylance rimane un tema di supporto non confermato, senza bloccare automaticamente la fase della scena.

**Metodo da conservare:** Matteo scrive personalmente il codice, consegne di ampiezza gestibile ma sufficientemente lunghe, nuove API spiegate prima dell'uso, revisione e verifica alla fine del blocco. Aggiornare questa guida a ogni checkpoint. Distinguere sempre implementazioni ricevute, prove confermate e consegne ancora da eseguire. L'assistente non ha modificato i sorgenti Ubuntu.

### 21.6 Checkpoint - prima consegna del builder e revisione

**23 ottobre 2026:** Matteo chiede frammenti espliciti di sintassi per le nuove API, mantenendo a proprio carico la composizione della funzione. Spiegati creazione di SolidPrimitive, selezione di BOX, dimensioni, Pose e inserimento con append nelle due liste corrispondenti.

Ricevuta e rivista la funzione build_table_object(): ID work_table, frame panda_link0, operazione ADD, posa generale identita, BOX di dimensioni [0.8, 0.8, 0.1], centro (0.6, 0.0, -0.05), orientamento della primitiva identita e corrispondenza delle due liste risultano corretti dalla lettura del frammento.

**Correzione assegnata:** manca return table alla fine della funzione, alla stessa indentazione dei due append. Senza return Python restituisce implicitamente None. Gli import non sono inclusi nel frammento: verificare nel modulo CollisionObject da moveit_msgs.msg, SolidPrimitive da shape_msgs.msg e Pose da geometry_msgs.msg.

**Da verificare:** applicazione del return, import, controllo sintattico, build e stampa del messaggio secondo 21.3. Nessun output di esecuzione ricevuto e nessuna applicazione della scena effettuata. Le correzioni dell'inspector e dei due main restano da confermare. Nessun sorgente Ubuntu modificato dall'assistente.

### 21.7 Checkpoint - prima stampa del builder: None

**23 ottobre 2026:** Matteo esegue il comando di import e stampa di build_table_object() e riporta None. Il comando completa import e chiamata, ma non restituisce il CollisionObject atteso. Costruzione e stampa del tavolo non sono ancora verificate.

**Diagnosi da confermare:** nella funzione effettivamente caricata manca un return table raggiunto sul percorso eseguito, oppure viene importata una copia non aggiornata. Verificare che return table sia salvato alla fine della funzione, con quattro spazi di indentazione come i due append. Se gia presente nel sorgente, stampare scene_builders.__file__ e inspect.getsource(scene_builders.build_table_object) per identificare percorso e codice realmente importati prima di altre modifiche.

Prossimo risultato atteso: stampa del CollisionObject completo. Nessun invio ad ApplyPlanningScene effettuato; correzioni dell'inspector e dei main ancora da confermare. Nessun sorgente Ubuntu modificato dall'assistente.

### 21.8 Checkpoint - builder del tavolo verificato tramite stampa

**23 ottobre 2026:** Matteo ripete il comando di import e stampa e fornisce il CollisionObject completo. Confermati: frame panda_link0, ID work_table, posa generale con posizione nulla e quaternion (0, 0, 0, 1), una BOX (type=1) di dimensioni [0.8, 0.8, 0.1], una posa della primitiva con centro (0.6, 0.0, -0.05) e quaternion identita. Il campo operation compare come b'\x00', rappresentazione Python del byte zero corrispondente ad ADD. Le altre liste geometriche sono vuote, come atteso.

La funzione ora restituisce il messaggio: il precedente None e superato dalla nuova prova. Non sono stati forniti output separati di py_compile o build; non dichiararli verificati. Il comando eseguito costruisce dati locali e non invia il tavolo a MoveIt. Le correzioni dell'inspector e dei main restano da confermare.

**Preferenza didattica da mantenere:** spiegare le nuove API e fornire la sintassi di base con frammenti mirati; Matteo scrive e collega personalmente il codice del nodo.

## 22. Esercizio 15 - applicare il tavolo alla scena e verificarne la presenza

**Consegna del 23 ottobre 2026, da implementare e verificare.** Creare /home/matteo/vision_sort_ws/src/vision_sort_lab/vision_sort_lab/scene_loader.py con un nodo separato SceneLoader. Il builder rimane nel suo modulo; il loader invia una sola richiesta per avvio. Nessun movimento del robot richiesto.

### 22.1 API nuove e sintassi essenziale

ApplyPlanningScene, da moveit_msgs.srv, riceve una richiesta con campo scene (PlanningScene) e restituisce success (bool). Il servizio da cercare nella demo e /apply_planning_scene. Prima di implementare, verificarlo e leggere le interfacce installate:

```bash
ros2 service type /apply_planning_scene
ros2 interface show moveit_msgs/srv/ApplyPlanningScene
ros2 interface show moveit_msgs/msg/PlanningScene
```

PlanningScene e il contenitore della scena; il tavolo va nella lista scene.world.collision_objects. is_diff=True seleziona un aggiornamento parziale. Anche robot_state.is_diff=True indica che lo stato del robot contenuto nel messaggio e parziale; qui lo lasciamo vuoto senza richiedere una sostituzione dello stato o degli oggetti collegati al robot. Questi campi sono distinti da CollisionObject.ADD, che seleziona l'operazione sul singolo oggetto. Lo schema e usato anche dal metodo applyCollisionObject di MoveIt: https://moveit.picknik.ai/main/api/html/planning__scene__interface_8cpp_source.html .

Frammento per il corpo del metodo di invio, non nodo completo:

```python
request = ApplyPlanningScene.Request()
request.scene.is_diff = True
request.scene.robot_state.is_diff = True
request.scene.world.collision_objects.append(build_table_object())
```

request.scene e gia creato dal costruttore della richiesta: non serve costruire separatamente un PlanningScene. build_table_object() restituisce un singolo CollisionObject, quindi append lo inserisce nella lista.

### 22.2 Struttura del nodo da scrivere

Import: rclpy, Node da rclpy.node, ApplyPlanningScene da moveit_msgs.srv e build_table_object da vision_sort_lab.scene_builders.

1. __init__: inizializzare SceneLoader con nome scene_loader; creare self.scene_client di tipo ApplyPlanningScene su /apply_planning_scene; attendere il servizio con wait_for_service e rclpy.ok() come nell'inspector; se il contesto e ancora valido chiamare una volta self.apply_scene().
2. apply_scene: costruire la richiesta con i quattro comandi di 22.1, inviarla con call_async, conservare il Future in self.scene_future e registrare self.on_scene_response con add_done_callback. Log di richiesta inviata.
3. on_scene_response: recuperare future.result() in try/except; in caso di eccezione registrare il problema e ritornare. Controllare response.success: log informativo se True, log di errore se False. Avere ricevuto una risposta non equivale automaticamente a successo.
4. main: inizializzazione ROS, riferimento al nodo inizializzato a None, costruzione, spin e pulizia nel finally. destroy_node dentro il controllo sul riferimento, try_shutdown fuori. Restare in spin fino a Ctrl+C; nessun timer o invio ripetuto.

Aggiungere a console_scripts in setup.py, conservando gli entry point presenti:

```python
'scene_loader = vision_sort_lab.scene_loader:main',
```

Nessuna nuova dipendenza rispetto a quelle gia necessarie al builder e all'inspector.

### 22.3 Verifica e consegna

Demo Panda attiva. In un terminale build dedicato:

```bash
source /opt/ros/jazzy/setup.bash
cd /home/matteo/vision_sort_ws
python3 -m py_compile src/vision_sort_lab/vision_sort_lab/scene_loader.py
colcon build --packages-select vision_sort_lab --symlink-install
```

In un altro terminale:

```bash
source /opt/ros/jazzy/setup.bash
source /home/matteo/vision_sort_ws/install/local_setup.bash
ros2 run vision_sort_lab scene_loader
```

Dopo il log con success=True, fermare il loader con Ctrl+C e avviare l'inspector nello stesso terminale. Se l'inspector era gia attivo, riavviarlo: fa una sola richiesta per avvio.

```bash
ros2 run vision_sort_lab scene_inspector
```

Criteri: risposta positiva di ApplyPlanningScene e ID work_table presente nell'output dell'inspector. Se la scena era ancora vuota, atteso Numero oggetti: 1; il criterio essenziale e la presenza dell'ID. Osservare inoltre il tavolo in RViz; distinguere la visualizzazione dalla verifica dell'ID e dalla futura verifica delle collisioni. WORLD_OBJECT_NAMES non conferma dimensioni e pose memorizzate: una lettura della geometria sara un eventuale passo successivo.

Inviare codice scene_loader.py, entry point e log di loader e inspector; riferire se il tavolo e visibile in RViz. I dati della scena appartengono al processo MoveIt corrente: dopo il riavvio della demo puo essere necessario reinviarli. Nessuna di queste nuove prove e ancora confermata.

### 22.4 Checkpoint - loader ricevuto e funzionamento confermato

**24 ottobre 2026:** Matteo consegna SceneLoader completo e dichiara tutto funzionante. Revisione: client ApplyPlanningScene corretto, attesa condizionata a rclpy.ok(), richiesta diff con robot_state diff, append del tavolo, Future conservato, registrazione di on_apply_scene_response, gestione eccezioni e controllo response.success corretti. Il main del loader ha try_shutdown fuori dall'if sul nodo, come richiesto.

La callback ha nome distinto da quella dell'inspector per scelta di leggibilita; metodi con lo stesso nome in classi diverse sarebbero comunque validi. Piccole revisioni suggerite nello stesso blocco successivo: ridurre a quattro spazi aggiuntivi l'indentazione del corpo dell'if rclpy.ok() (attualmente valida ma eccessiva) e collocare il log di richiesta inviata dopo call_async. Non richiedono nuovi test automatici.

**Livello di evidenza:** codice ricevuto e funzionamento confermato dall'utente. Non allegati log del servizio o dell'inspector, entry point o immagine RViz; non inventare numero di oggetti, ID osservati o visualizzazione verificata separatamente. Correzioni dell'inspector e del main del commander ancora non confermate dai rispettivi sorgenti. Nessun sorgente Ubuntu modificato dall'assistente.

## 23. Esercizio 16 - tre cubi colorati sul tavolo

**Consegna del 24 ottobre 2026, da implementare e verificare.** Estendere scene_builders.py e scene_loader.py. Si resta nella scena di pianificazione MoveIt/RViz. I colori sono metadati per la visualizzazione; non sono ancora misure di una telecamera o classi riconosciute da un algoritmo.

### 23.1 Builder parametrico della scatola

Scrivere una funzione senza nodo:

```python
def build_box_object(object_id, dimensions, center):
```

Restituisce un nuovo CollisionObject, usando lo schema del tavolo: frame panda_link0, operazione ADD, posa generale identita, una BOX e una posa della primitiva con centro assegnato e orientamento identita. Usare object_id al posto dell'ID fisso, list(dimensions) per la lista delle dimensioni e i tre elementi di center per la posizione. Esempi di sintassi:

```python
obj.id = object_id
box.dimensions = list(dimensions)
box_pose.position.x = center[0]
```

center[0], center[1], center[2] sono X, Y, Z. Ogni chiamata deve creare nuovi messaggi; nessuna istanza condivisa fra i tre cubi. Conservare per ora build_table_object gia verificato.

### 23.2 Lista degli oggetti e geometria

Scrivere build_sorting_objects(), che restituisce una lista di tre CollisionObject costruiti tramite il nuovo helper. Tutti hanno dimensioni [0.04, 0.04, 0.04], in metri e float.

| ID | Centro XYZ in panda_link0 | Colore RGB |
|---|---|---|
| piece_red_1 | (0.45, -0.20, 0.02) | (1.0, 0.0, 0.0) |
| piece_blue_1 | (0.55, 0.0, 0.02) | (0.0, 0.0, 1.0) |
| piece_red_2 | (0.45, 0.20, 0.02) | (1.0, 0.0, 0.0) |

Il fondo di ciascun cubo e z=0.02-0.04/2=0.0, coincidente con il piano superiore del tavolo. I cubi sono separati e interni al piano; raggiungibilita e traiettorie di presa saranno verificate con la pianificazione in seguito.

Per costruire una lista si puo iniziare con objects = [], poi objects.append(build_box_object(...)) per ciascun pezzo e return objects. Sono tre CollisionObject con ID distinti, non tre primitive nello stesso CollisionObject: potranno essere manipolati indipendentemente.

### 23.3 Nuova API ObjectColor

Leggere le interfacce della versione installata:

```bash
ros2 interface show moveit_msgs/msg/ObjectColor
ros2 interface show std_msgs/msg/ColorRGBA
```

Importare ObjectColor da moveit_msgs.msg. Il messaggio associa id a color, che ha campi r, g, b e a in [0.0, 1.0]. Alpha 1.0 rende il colore opaco; non lasciare alpha a zero. Non serve importare ColorRGBA se si assegnano i campi del messaggio interno gia costruito.

Scrivere build_object_color(object_id, r, g, b), che crea un nuovo ObjectColor, assegna id e componenti RGB, imposta alpha=1.0 e restituisce il messaggio. Frammento esplicativo:

```python
color = ObjectColor()
color.id = object_id
color.color.r = r
color.color.a = 1.0
```

Il colore viene inserito in PlanningScene.object_colors, separatamente dalle geometrie. Il collegamento avviene per ID, non per indice. Fonti: https://docs.ros.org/en/humble/p/moveit_msgs/msg/ObjectColor.html e https://moveit.picknik.ai/main/api/html/classplanning__scene_1_1PlanningScene.html ; verificare la definizione locale Jazzy con ros2 interface show.

### 23.4 Integrazione nel loader

Importare i nuovi builder nel loader. Dopo l'append del tavolo inserire i tre pezzi con:

```python
request.scene.world.collision_objects.extend(build_sorting_objects())
```

extend aggiunge separatamente tutti gli elementi di una lista; append aggiungerebbe l'intera lista come un singolo elemento, incompatibile con CollisionObject[].

Aggiungere i tre colori in request.scene.object_colors, usando build_object_color con gli ID e RGB della tabella. Esempio per il primo:

```python
request.scene.object_colors.append(
    build_object_color('piece_red_1', 1.0, 0.0, 0.0)
)
```

Tavolo, pezzi e colori viaggiano nella stessa richiesta. Conservare is_diff e robot_state.is_diff a True. Nessun nuovo nodo o entry point richiesto.

### 23.5 Verifica e consegna

Prima dell'invio, stampare gli ID prodotti dal builder:

```bash
python3 -c "from vision_sort_lab.scene_builders import build_sorting_objects; print([obj.id for obj in build_sorting_objects()])"
```

In un terminale build con ROS base caricato:

```bash
cd /home/matteo/vision_sort_ws
python3 -m py_compile src/vision_sort_lab/vision_sort_lab/scene_builders.py src/vision_sort_lab/vision_sort_lab/scene_loader.py
colcon build --packages-select vision_sort_lab --symlink-install
```

In un terminale runtime caricare ROS base e install/local_setup.bash, con demo attiva, eseguire scene_loader e dopo il risultato fermarlo; avviare scene_inspector. Attesi work_table e i tre ID, quattro oggetti se non esistono oggetti estranei. Verificare in RViz tre cubi sopra il tavolo, due rossi e uno blu. Eventuali collisioni con lo stato corrente del robot o differenze di visualizzazione vanno osservate, non escluse in anticipo.

Ripetere loader e inspector nella stessa demo: con gli stessi ID e ADD gli oggetti vengono sostituiti, non duplicati; attesi gli stessi quattro ID. Questa prova ripristina le pose iniziali dei pezzi, comportamento da ricordare prima delle future prese.

Inviare i tre nuovi builder, apply_scene aggiornato e log di loader e inspector; descrivere il risultato in RViz. Nessuna implementazione o prova di questo blocco e ancora ricevuta.

### 23.6 Chiarimento - la BOX del builder e il ripiano del tavolo

**24 ottobre 2026:** Matteo ripropone build_table_object e chiede perche la scatola inserita non venga visualizzata. Chiarimento: table e il contenitore CollisionObject con ID work_table; box e la sua unica geometria. Il risultato atteso e un solo ripiano rettangolare 0.8 x 0.8 x 0.1 m, non un tavolo piu una scatola separata. Il nome della variabile box non crea un oggetto con ID autonomo. Non ci sono gambe nel modello corrente.

Il codice mostrato mantiene dimensioni, pose e return corretti. Distinguere l'assenza di una scatola aggiuntiva (coerente con il modello) dall'eventuale assenza dell'intero ripiano in RViz. La domanda non fornisce immagine o log sufficienti a confermare quale caso si presenti: se manca anche il ripiano, controllare prima l'ID work_table tramite una nuova esecuzione dell'inspector, poi la visualizzazione. Non dichiarare risolta o verificata la visibilita.

L'esercizio dei tre cubi colorati rimane assegnato; nessuna sua implementazione ricevuta. Nessun sorgente Ubuntu modificato dall'assistente.

### 23.7 Checkpoint - builder dei cubi e colori ricevuti, correzioni assegnate

**24 ottobre 2026:** Matteo consegna gli import del loader, il frammento apply_scene e i builder completi. Geometrie, coordinate, ID e RGB dei tre pezzi corrispondono alla consegna. Il loader usa correttamente append per il tavolo, extend per la lista dei pezzi e object_colors per i colori; il log e ora dopo call_async.

**Correzioni necessarie:** aggiungere return new_box a build_box_object, return objects a build_sorting_objects e return color a build_object_color. Ogni return deve essere alla fine della propria funzione, con quattro spazi di indentazione. Senza return gli helper restituiscono None: il builder della lista non fornisce una sequenza a extend; se si corregge solo quel return, i suoi elementi restano None senza il return del builder della scatola. Anche il builder del colore deve restituire ObjectColor.

Negli import mostrati del loader manca build_object_color: aggiungerlo da vision_sort_lab.scene_builders. ObjectColor importato in scene_builders non importa automaticamente la funzione helper nel namespace del loader. Il frammento apply_scene e mostrato isolato: ricordare che nel file deve rimanere un metodo di SceneLoader, con la def indentata di quattro spazi e il corpo di otto; non dichiarare una perdita effettiva della classe senza il file completo.

**Verifica assegnata:** dopo le correzioni, controllo sintattico e build, poi stampa degli ID da build_sorting_objects e stampa di un risultato di build_object_color. Attesi tre ID corretti e un ObjectColor con alpha 1.0. Infine loader e nuova richiesta dell'inspector, verifica dei quattro ID e dei colori in RViz, piu ripetizione con gli stessi ID. Nessun output di questi test ancora ricevuto; non considerare completato il blocco. Nessun sorgente Ubuntu modificato dall'assistente.

### 23.8 Checkpoint - tre cubi colorati confermati funzionanti

**24 ottobre 2026:** dopo la revisione di 23.7, Matteo conferma che tutto funziona correttamente e chiede di proseguire. Registrata conferma complessiva del blocco: builder dei pezzi e colori, caricamento e verifica previsti dall'esercizio. Nessun nuovo codice corretto, log o screenshot allegato: il dettaglio dei singoli output e della ripetizione con gli stessi ID non e documentato separatamente. Non richiedere nuove prove del blocco senza una ragione concreta; procedere ai contenitori. Il dubbio precedente sulla BOX del tavolo e stato chiarito concettualmente; nessuna diagnosi aggiuntiva di RViz richiesta dall'utente.

## 24. Esercizio 17 - due contenitori aperti con geometrie composte

**Consegna del 24 ottobre 2026, da scrivere e verificare.** Aggiungere due contenitori di smistamento alla stessa scena MoveIt. Ogni contenitore e un solo CollisionObject composto da cinque BOX: fondo e quattro pareti. Il modello ha un volume interno libero e nessuna copertura superiore. Due nuove funzioni di builder e un helper per aggiungere primitive; nessun nuovo nodo.

### 24.1 Riferimenti e geometria

Usare ora la posa generale per collocare il contenitore nel frame panda_link0. L'origine locale del contenitore e al centro della faccia inferiore del fondo: la posizione Z=0 lo appoggia geometricamente sul tavolo. Tutte le primitive hanno posa locale rispetto al contenitore. Nessuna rotazione: entrambe le orientazioni sono identita e le posizioni si sommano.

| ID | Posizione dell'origine del contenitore XYZ | Colore RGB |
|---|---|---|
| bin_red | (0.75, -0.22, 0.0) | (1.0, 0.0, 0.0) |
| bin_blue | (0.75, 0.22, 0.0) | (0.0, 0.0, 1.0) |

Dimensioni esterne XY 0.18 x 0.18 m; fondo spesso 0.01 m; altezza complessiva 0.08 m; pareti spesse 0.01 m e alte 0.07 m, sopra il fondo. Tutte le coordinate della tabella seguente sono locali al contenitore:

| Parte | Dimensioni XYZ | Centro XYZ locale |
|---|---|---|
| Fondo | [0.18, 0.18, 0.01] | (0.0, 0.0, 0.005) |
| Parete X negativa | [0.01, 0.18, 0.07] | (-0.085, 0.0, 0.045) |
| Parete X positiva | [0.01, 0.18, 0.07] | (0.085, 0.0, 0.045) |
| Parete Y negativa | [0.16, 0.01, 0.07] | (0.0, -0.085, 0.045) |
| Parete Y positiva | [0.16, 0.01, 0.07] | (0.0, 0.085, 0.045) |

Il fondo va da Z=0 a Z=0.01; le pareti da Z=0.01 a Z=0.08. Lo spazio interno XY e 0.16 x 0.16 m. Le pareti Y sono lunghe 0.16 per inserirsi fra le due pareti X senza sovrapposizioni di volume agli angoli. I contenitori restano dentro il piano di lavoro; nessuna raggiungibilita di presa o deposito ancora verificata.

Esempio di composizione: la parete X positiva di bin_red ha centro nel frame panda_link0 pari a (0.835, -0.22, 0.045), somma dell'origine del contenitore e del centro locale. Non aggiungere la traslazione globale anche alle primitive. L'ID del contenitore non crea automaticamente un frame TF.

### 24.2 Helper che modifica un messaggio esistente

In scene_builders.py scrivere:

```python
def add_box_primitive(collision_object, dimensions, center):
```

Creare una nuova SolidPrimitive BOX e una nuova Pose locale, assegnare dimensioni, centro e orientamento identita come nei builder gia scritti, poi:

```python
collision_object.primitives.append(box)
collision_object.primitive_poses.append(box_pose)
```

Questo helper modifica direttamente il CollisionObject ricevuto. Non deve creare un nuovo CollisionObject, assegnare un ID o restituire un nuovo oggetto. La chiamata e una istruzione autonoma; il ritorno implicito None e intenzionale e non va aggiunto alla lista. Il confronto con build_box_object chiarisce la differenza fra costruire/restituire e modificare un oggetto esistente.

### 24.3 Builder del contenitore e lista delle destinazioni

Scrivere build_bin_object(object_id, position). Creare un CollisionObject nuovo, impostare ID, frame panda_link0 e operazione ADD. Assegnare position alla posa generale e quaternion identita:

```python
container.pose.position.x = position[0]
container.pose.position.y = position[1]
container.pose.position.z = position[2]
container.pose.orientation.w = 1.0
```

Chiamare add_box_primitive cinque volte con la geometria della tabella. Esempio per il fondo:

```python
add_box_primitive(container, [0.18, 0.18, 0.01], (0.0, 0.0, 0.005))
```

Restituire container. Le due liste devono avere cinque elementi ciascuna; ogni coppia geometria/posa deve mantenere lo stesso indice. Si possono usare cinque chiamate esplicite oppure un ciclo su una lista di specifiche.

Scrivere build_sorting_bins(), che restituisce una lista con i due risultati di build_bin_object, secondo gli ID e le posizioni di 24.1. Conservare i builder di tavolo e pezzi gia funzionanti.

### 24.4 Integrazione e verifiche

Importare build_sorting_bins nel loader. Dopo tavolo e cubi aggiungere:

```python
request.scene.world.collision_objects.extend(build_sorting_bins())
```

Aggiungere a object_colors i due colori tramite build_object_color, usando esattamente bin_red e bin_blue. Il colore del CollisionObject si applica all'intero contenitore, non separatamente per indice alle pareti. Conservare una sola richiesta diff con gli oggetti correnti.

Controllo locale dopo build e caricamento ambiente runtime:

```bash
python3 -c "from vision_sort_lab.scene_builders import build_sorting_bins; print([(obj.id, len(obj.primitives), len(obj.primitive_poses)) for obj in build_sorting_bins()])"
```

Atteso [('bin_red', 5, 5), ('bin_blue', 5, 5)]. Eseguire controllo sintattico e build come nel blocco precedente. Con demo attiva eseguire loader, poi una nuova richiesta dell'inspector. Attesi sei ID se non ci sono oggetti estranei: work_table, i tre piece e i due bin. In RViz verificare due contenitori aperti dall'alto, con fondo sul piano e nessuna sovrapposizione con i cubi. L'inspector con WORLD_OBJECT_NAMES controlla solo gli ID: il numero di primitive nel server non e verificato da quella richiesta. La stampa locale e la visualizzazione sono verifiche distinte.

Consegna: i tre nuovi helper/builder, integrazione in apply_scene, output della stampa locale e dell'inspector, descrizione o screenshot RViz. L'interno geometricamente libero non garantisce ancora accesso della pinza o riuscita del deposito; seguira la verifica di pose e collisioni tramite pianificazione. Nessuna implementazione o prova del blocco 24 ancora ricevuta. Nessun sorgente Ubuntu modificato dall'assistente.

### 24.5 Alternativa discussa - contenitore importato da URDF o mesh

**24 ottobre 2026:** prima di consegnare il contenitore composto da primitive, Matteo propone di importare un modello URDF o un altro file. Nessun contenitore del blocco 24 e stato scritto o verificato nella conversazione.

Chiarimento: un file mesh (ad esempio STL o DAE) descrive la superficie triangolata; un URDF descrive link, joint, visual e collision e puo riferirsi a mesh esterne. Nel percorso attuale ApplyPlanningScene riceve un PlanningScene con CollisionObject, non un percorso URDF: un'importazione URDF richiede estrazione/conversione della geometria oppure integrazione nel modello robotico. Visualizzare un URDF separato in RViz non inserisce automaticamente i suoi ostacoli nel mondo di MoveIt.

Alternativa coerente con l'architettura attuale: caricare una mesh di contenitore aperto e convertirla in shape_msgs/Mesh, poi inserirla in CollisionObject.meshes con la relativa mesh_poses. Frame, ID, posa generale, colori, loader e inspector restano applicabili. Non assegnare direttamente una stringa con il percorso a meshes: quel campo richiede messaggi geometrici. Prima dell'implementazione spiegare caricamento del file, scala/unita, origine, vertici e triangoli e verificare eventuali dipendenze nell'ambiente WSL.

La geometria per le collisioni deve preservare l'apertura e lo spazio interno: un semplice volume pieno o un involucro convesso dell'intero contenitore impedirebbe l'ingresso della pinza nella pianificazione. Mesh visuale e collisione possono essere differenti; una rappresentazione a cinque primitive resta un'opzione semplice ed efficiente per questo oggetto regolare.

**Stato:** opzioni spiegate; nessun asset selezionato, scaricato o creato, nessuna dipendenza installata e nessuna sostituzione dell'esercizio implementata. L'import di mesh e la proposta piu diretta qualora Matteo scelga di usare un modello esterno; URDF resta utile se si vuole studiare o riusare una descrizione strutturata. Nessun sorgente Ubuntu modificato dall'assistente.

### 24.6 Vincolo confermato - stessa geometria per visualizzazione e collisioni

**24 ottobre 2026:** Matteo chiede di evitare complicazioni dovute a differenze fra modello visuale e modello di collisione. Per i contenitori importati mantenere una sola mesh per oggetto, caricata nel CollisionObject della scena MoveIt e visualizzata tramite il display della stessa scena in RViz. Non introdurre un modello URDF visuale separato o un marker con geometria indipendente per questi contenitori.

La stessa mesh descrive la geometria visibile e quella sottoposta ai controlli di collisione. Rimangono da verificare il file scelto, scala, origine, apertura interna e una successiva prova di collisione: vedere il modello non prova da solo la correttezza di una traiettoria. La futura sincronizzazione con Gazebo e un tema distinto e non viene introdotta in questo blocco.

Nessun asset ancora scelto o importato, nessun nuovo codice ricevuto. Questo vincolo orienta il prossimo esercizio di importazione della mesh; non dichiarare gia verificato il suo comportamento nelle collisioni. Nessun sorgente Ubuntu modificato dall'assistente.

### 24.7 Decisione - procedere con un file mesh

**24 ottobre 2026:** Matteo accetta il percorso mesh. La consegna a cinque primitive di 24.1-24.4 viene sostituita dalla lettura di un file STL e successiva integrazione in un CollisionObject. Non considerare scritti add_box_primitive, build_bin_object o build_sorting_bins del precedente esercizio. Il vincolo di 24.6 rimane: stessa mesh per visualizzazione della scena e collisioni.

## 25. Esercizio 17 aggiornato - leggere uno STL e convertirlo in Mesh ROS

**Consegna del 24 ottobre 2026, da scrivere da Matteo.** Prima lettura del file e conversione in shape_msgs/Mesh, senza invio al server. L'integrazione dei due contenitori nel loader seguira la revisione della conversione. Non riscrivere i nodi e non aggiungere URDF o marker separati.

### 25.1 Asset preparato e verifiche realmente eseguite

L'assistente prepara un modello originale semplice per il progetto, non scaricato da terzi, nel file Windows:

C:\Users\matte\Documents\Codex\2026-10-05\vor\outputs\vision-sort-lab\assets\meshes\open_bin.stl

Formato STL ASCII, singola superficie triangolata del materiale del contenitore, 28 triangoli e 16 posizioni di vertici distinte. Dimensioni espresse numericamente in metri; STL non dichiara una propria unita. Origine al centro della faccia inferiore del fondo.

| Proprieta | Valore |
|---|---|
| Dimensioni esterne XYZ | [0.18, 0.18, 0.08] m |
| Bounds minimi | [-0.09, -0.09, 0.0] |
| Bounds massimi | [0.09, 0.09, 0.08] |
| Spessore fondo e pareti | 0.01 m |
| Vano interno XY | 0.16 x 0.16 m |
| Piano interno del fondo | z = 0.01 m |
| SHA-256 | 6a7b2e2ca266cf0e8bbe4b7d2e4b876650d7104352fd8d252366cc9d743ec5bf |

**Verifiche locali dell'assistente:** riletto lo STL dopo la scrittura; bounds e numero dei triangoli corretti, triangoli non degeneri, ogni spigolo geometrico condiviso da due facce con orientamenti opposti, volume del materiale 0.0008 m3. Un raggio verticale nel vano incontra solo fondo a z=0.01 e faccia inferiore a z=0, senza un coperchio; un raggio orizzontale nel vano incontra parete interna a x=0.08 ed esterna a x=0.09. Anteprima 3D renderizzata e ispezionata. Superficie chiusa del materiale non significa che il vano sia chiuso: il bordo collega pareti interne ed esterne e lascia aperto l'accesso superiore.

Queste sono verifiche del file, non una prova di collisione nel MoveIt dell'utente. Nessuna esecuzione ROS della mesh, copia in WSL o installazione di dipendenze confermata.

### 25.2 Preparazione in Ubuntu WSL

Usare numpy-stl tramite il pacchetto APT python3-stl, presente in Ubuntu Noble 24.04 (2.9.0-2build4), senza installazioni pip globali o nuovo ambiente virtuale. Fonte verificata: https://packages.ubuntu.com/noble/amd64/python3-stl . Le API base Mesh.from_file, vectors, min_ e max_ sono descritte anche nella documentazione ufficiale: https://numpy-stl.readthedocs.io/en/latest/getting-started/quickstart.html e https://numpy-stl.readthedocs.io/en/latest/guide/properties.html . La documentazione latest puo riferirsi a versioni successive: non introdurre metodi aggiuntivi non controllati nella versione locale.

```bash
sudo apt update
sudo apt install python3-stl
mkdir -p /home/matteo/vision_sort_ws/src/vision_sort_lab/meshes
cp /mnt/c/Users/matte/Documents/Codex/2026-10-05/vor/outputs/vision-sort-lab/assets/meshes/open_bin.stl /home/matteo/vision_sort_ws/src/vision_sort_lab/meshes/
source /opt/ros/jazzy/setup.bash
cd /home/matteo/vision_sort_ws/src/vision_sort_lab
python3 -c "from stl import mesh; m = mesh.Mesh.from_file('meshes/open_bin.stl'); print('Triangoli:', len(m.vectors)); print('Min:', m.min_); print('Max:', m.max_); print('Dimensioni:', m.max_ - m.min_)"
```

Attesi 28 triangoli, bounds e dimensioni di 25.1 con possibili arrotondamenti float32. Nessuna scalatura o traslazione dei vertici necessaria per questo asset. Installazione, copia e comandi sono assegnati a Matteo, non eseguiti nel suo Ubuntu dall'assistente.

### 25.3 Nuove API prima della funzione

Creare /home/matteo/vision_sort_ws/src/vision_sort_lab/vision_sort_lab/mesh_builders.py. Import:

```python
from stl import mesh as stl_mesh
from geometry_msgs.msg import Point
from shape_msgs.msg import Mesh, MeshTriangle
```

stl_mesh e un alias per distinguere la libreria STL dal messaggio ROS Mesh. Lettura del file:

```python
source = stl_mesh.Mesh.from_file(str(file_path))
```

source.vectors e una sequenza di triangoli; ogni triangolo contiene tre vertici e ogni vertice tre coordinate XYZ. Il messaggio ROS Mesh contiene vertices (lista di Point) e triangles (lista di MeshTriangle). MeshTriangle.vertex_indices contiene tre indici nella lista vertices: non coordinate. Leggere nell'ambiente locale:

```bash
ros2 interface show shape_msgs/msg/Mesh
ros2 interface show shape_msgs/msg/MeshTriangle
```

Per il primo import usare tre nuovi Point per ciascun triangolo, conservando l'ordine originale dei vertici. Nessuna deduplicazione richiesta: 28 triangoli producono 84 voci vertices. La ripetizione di coordinate non cambia la geometria rappresentata.

### 25.4 Funzione da scrivere

Scrivere load_stl_mesh(file_path), funzione senza nodo che restituisce un Mesh ROS.

1. Leggere lo STL in source e creare result = Mesh().
2. Iterare su source.vectors. Per ogni triangolo salvare start = len(result.vertices) prima di aggiungere i tre punti.
3. Iterare sui suoi tre vertici. Creare un Point nuovo ogni volta; assegnare x/y/z convertendo con float, quindi aggiungere il punto a result.vertices.
4. Dopo i tre punti, creare un MeshTriangle nuovo e impostare vertex_indices = [start, start + 1, start + 2]. Aggiungerlo a result.triangles.
5. Dopo il ciclo esterno, return result.

Frammenti di sintassi da comporre personalmente:

```python
for triangle_vertices in source.vectors:
    start = len(result.vertices)
    # Qui il ciclo sui tre vertici e la costruzione del triangolo.
```

```python
point = Point()
point.x = float(xyz[0])
point.y = float(xyz[1])
point.z = float(xyz[2])
result.vertices.append(point)
```

```python
triangle = MeshTriangle()
triangle.vertex_indices = [start, start + 1, start + 2]
result.triangles.append(triangle)
```

float converte i numeri NumPy nel tipo Python adatto ai campi ROS float64. start e un indice intero ottenuto da len. Il triangolo deve essere aggiunto dopo il ciclo sui tre vertici e dentro il ciclo sui triangoli. Non ricalcolare o invertire l'ordine dei vertici e non usare convex_hull, bounding box o altre sostituzioni geometriche.

### 25.5 Verifica e checkpoint atteso

Terminale build con ROS base caricato:

```bash
cd /home/matteo/vision_sort_ws
python3 -m py_compile src/vision_sort_lab/vision_sort_lab/mesh_builders.py
colcon build --packages-select vision_sort_lab --symlink-install
```

Terminale runtime:

```bash
source /opt/ros/jazzy/setup.bash
source /home/matteo/vision_sort_ws/install/local_setup.bash
python3 -c "from vision_sort_lab.mesh_builders import load_stl_mesh; m = load_stl_mesh('/home/matteo/vision_sort_ws/src/vision_sort_lab/meshes/open_bin.stl'); print('Vertici:', len(m.vertices)); print('Triangoli:', len(m.triangles)); print('Primo triangolo:', list(m.triangles[0].vertex_indices)); print('Ultimo triangolo:', list(m.triangles[-1].vertex_indices))"
```

Attesi Vertici: 84, Triangoli: 28, primo [0, 1, 2], ultimo [81, 82, 83]. Nessun main, nodo o entry point per mesh_builders. Il percorso assoluto al sorgente e temporaneo per questa verifica: installazione della mesh nei data_files di setup.py, risoluzione tramite ament_index_python e dichiarazione della dipendenza esterna con chiave rosdep verificata saranno affrontate nel blocco di integrazione; non presentare ancora il package come autonomamente distribuibile.

Consegna unica: mesh_builders.py, output di lettura dello STL e output della conversione. Nessun invio della mesh con ApplyPlanningScene ancora assegnato in questo blocco e nessun comportamento di collisione verificato in MoveIt. Il codice ROS continua a essere scritto personalmente da Matteo; l'assistente ha preparato esclusivamente l'asset geometrico e la documentazione.

### 25.6 Checkpoint - conversione STL in Mesh ricevuta e verificata

**24 ottobre 2026:** Matteo consegna load_stl_mesh completa e l'output: Vertici: 84, Triangoli: 28, Ultimo triangolo: [81, 82, 83]. Revisione positiva: import e alias corretti, lettura con Mesh.from_file, nuovo Point per ciascun vertice con conversioni float, start calcolato prima dei tre punti, nuovo MeshTriangle per faccia con indici corretti, append e return result dopo il ciclo esterno.

La conversione del file usato nella prova in un messaggio ROS e confermata dall'output. Non allegati output separati di bounds, installazione APT o build; non dichiararli osservati. La mesh non e ancora stata inviata a MoveIt e non sono state verificate collisioni del modello importato.

## 26. Esercizio 18 - installare lo STL e caricare due contenitori mesh

**Consegna del 24 ottobre 2026, da implementare e verificare.** Integrare la funzione di conversione gia verificata con scene_builders e scene_loader. Un solo STL utilizzato per due CollisionObject con ID e pose differenti. Il file contiene geometria locale, mentre il messaggio contiene la collocazione nel frame robot.

### 26.1 Installazione della risorsa e nuova API di ricerca

In setup.py, nella lista data_files gia presente, aggiungere la tupla:

```python
('share/vision_sort_lab/meshes', ['meshes/open_bin.stl']),
```

Il primo elemento e la destinazione relativa al prefisso di installazione; il secondo e la lista di file relativi alla radice del pacchetto, dove si trova setup.py. Conservare le righe di installazione del resource marker e package.xml e gli entry point esistenti. Non aggiungere una seconda proprieta data_files.

Nel loader importare:

```python
from pathlib import Path
from ament_index_python.packages import get_package_share_directory
```

get_package_share_directory cerca nell'indice dei pacchetti ROS caricati e restituisce il percorso della directory share/vision_sort_lab del package installato. Path e la classe della libreria standard per rappresentare percorsi; l'operatore / compone le loro parti. Nel metodo apply_scene:

```python
mesh_path = (
    Path(get_package_share_directory('vision_sort_lab'))
    / 'meshes'
    / 'open_bin.stl'
)
```

Con l'installazione isolata corrente il percorso atteso e /home/matteo/vision_sort_ws/install/vision_sort_lab/share/vision_sort_lab/meshes/open_bin.stl. La funzione evita di fissare quel prefisso nel codice. Fonte API Jazzy: https://docs.ros.org/en/jazzy/p/ament_index_python/ ; overview del pacchetto: https://index.ros.org/p/ament_index_python/ .

Aggiungere in package.xml, solo se assente:

```xml
<exec_depend>ament_index_python</exec_depend>
```

Conservare geometry_msgs e shape_msgs gia necessari ai builder. L'import stl e gia riuscito nella prova, ma il metodo di installazione non e documentato separatamente. python3-stl e il prerequisito APT documentato in 25.2. La ricerca della chiave rosdep corrispondente non ha fornito una mappatura autorevole verificata: non aggiungere chiavi ipotetiche al manifest o sostituirle con un'installazione pip globale. L'installazione automatica di quella dipendenza tramite rosdep resta un punto di confezionamento da chiudere; non blocca la prova nel sistema corrente dove il modulo e disponibile.

### 26.2 Builder di un contenitore mesh

In scene_builders.py importare load_stl_mesh da vision_sort_lab.mesh_builders e scrivere:

```python
def build_bin_object(object_id, position, mesh_path):
```

Creare un CollisionObject nuovo (es. container), assegnare ID, frame panda_link0 e ADD. Impostare posa generale con position e quaternion identita. Il file ha origine al centro della faccia inferiore del fondo, percio Z=0 appoggia il fondo sul tavolo.

La geometria va nei campi meshes e mesh_poses:

```python
container.meshes.append(load_stl_mesh(mesh_path))
mesh_pose = Pose()
mesh_pose.orientation.w = 1.0
container.mesh_poses.append(mesh_pose)
```

Il frammento mostra la nuova parte specifica delle mesh; completare personalmente campi base, assegnazione della posa generale e return container. mesh_pose ha posizione nulla e orientamento identita: non ripetere qui la traslazione globale. La lista primitives rimane vuota. Criteri locali: una mesh, una posa della mesh, 28 triangoli.

### 26.3 Integrazione nella richiesta esistente

Importare build_bin_object nel loader. In apply_scene ricavare mesh_path con 26.1 e conservare gli inserimenti di tavolo e cubi. Aggiungere i due contenitori, ciascuno tramite append. Esempio per il rosso:

```python
request.scene.world.collision_objects.append(
    build_bin_object('bin_red', (0.75, -0.22, 0.0), mesh_path)
)
```

Creare allo stesso modo bin_blue in (0.75, 0.22, 0.0). Aggiungere a object_colors i due messaggi prodotti dal builder dei colori gia verificato: bin_red rosso e bin_blue blu, alpha=1.0. Una sola richiesta con sei CollisionObject se non ci sono altri oggetti. Non e necessario scrivere build_sorting_bins o add_box_primitive della vecchia consegna.

### 26.4 Verifica e consegna

Terminale build dedicato:

```bash
source /opt/ros/jazzy/setup.bash
cd /home/matteo/vision_sort_ws
python3 -m py_compile src/vision_sort_lab/setup.py src/vision_sort_lab/vision_sort_lab/scene_builders.py src/vision_sort_lab/vision_sort_lab/scene_loader.py
colcon build --packages-select vision_sort_lab --symlink-install
```

Nel terminale runtime, caricare ROS e overlay e verificare il percorso installato:

```bash
source /opt/ros/jazzy/setup.bash
source /home/matteo/vision_sort_ws/install/local_setup.bash
python3 -c "from pathlib import Path; from ament_index_python.packages import get_package_share_directory; p = Path(get_package_share_directory('vision_sort_lab')) / 'meshes' / 'open_bin.stl'; print(p); print('Esiste:', p.is_file())"
```

Atteso percorso nel prefisso installato e Esiste: True. Se non e presente, controllare data_files e build: non ripiegare sul percorso assoluto del sorgente per aggirare una risorsa non installata.

Con demo attiva eseguire scene_loader, attendere risposta positiva, fermarlo con Ctrl+C e avviare una nuova istanza di scene_inspector. Attesi work_table, piece_red_1, piece_blue_1, piece_red_2, bin_red e bin_blue, sei oggetti se non ne esistono altri. In RViz attesi due contenitori aperti, rosso e blu, appoggiati sul tavolo, senza sovrapporsi ai pezzi. Stessa mesh memorizzata nella scena per visualizzazione e collisioni; nessun modello visuale separato.

Consegna unica: build_bin_object, apply_scene aggiornato, nuova tupla data_files e dipendenza ament_index_python, output del percorso e log di loader/inspector, descrizione o screenshot RViz. Questa prova confermera caricamento e visualizzazione, non ancora una verifica di collisione della pinza dentro e contro le pareti. Quella prova verra affrontata dopo la revisione della scena. Nessuna implementazione o prova del blocco 26 ancora ricevuta. Nessun sorgente Ubuntu modificato dall'assistente.

## 27. Recap e ordine delle prossime fasi

**24 ottobre 2026:** Matteo chiede se chiudere la sezione della scena e iniziare una nuova chat, e se il passo successivo debba riguardare la manipolazione autonoma o la computer vision. La risposta distingue lo stato confermato dalla roadmap: tavolo e tre cubi confermati, conversione STL verificata; per l'ultimo blocco 26 non sono ancora stati consegnati codice o un esito esplicito del caricamento dei due contenitori. Il messaggio perfetto procediamo non viene trasformato in log di sei oggetti o in una prova delle collisioni.

### 27.1 Criterio di chiusura della scena

Concludere in questa chat l'integrazione del blocco 26, se non gia eseguita: STL trovato nelle risorse installate, ApplyPlanningScene riuscito, sei ID presenti e due contenitori aperti correttamente collocati in RViz. Aggiungere una verifica esplicita che MoveIt consideri le collisioni delle mesh; la sola visualizzazione non basta. Non sono richiesti nuovi elementi geometrici, dettagli estetici o un modello visuale separato.

Il controllo dettagliato della raggiungibilita dei punti di presa e deposito appartiene alla fase successiva: non renderlo un requisito illimitato per chiudere la modellazione della scena. La simulazione fisica non fa parte della fase attuale.

### 27.2 Fase successiva consigliata - manipolazione da pose note

Dopo la chiusura della scena, aprire una nuova chat con titolo proposto Vision Sort Lab - fase 6: manipolazione da pose note. Nessuna nuova chat creata o rinominata dall'assistente.

Obiettivo: passare dagli obiettivi articolari gia usati a pose cartesiane della pinza, iniziando da un solo cubo. Studiare posizione e orientamento della pinza, frame e link terminale, pre-presa e avvicinamento, apertura e chiusura della pinza, sollevamento, trasporto e deposito con pianificazione delle collisioni. Gestire l'oggetto nella scena come libero, collegato alla pinza durante il trasporto e nuovamente libero dopo il rilascio. L'eventuale collegamento ideale in MoveIt e dichiarato e non dimostra una presa fisica.

Le pose note dei builder permettono di verificare la manipolazione senza aggiungere incertezze percettive. Il commander gia pianifica ed esegue autonomamente richieste articolari: il nuovo lavoro e la generazione e orchestrazione delle richieste di manipolazione rispetto agli oggetti.

### 27.3 Sequenza consigliata dopo la prima manipolazione

1. Stabilizzare il ciclo di manipolazione di un oggetto da posa nota in MoveIt, poi estenderlo ai tre pezzi.
2. Integrare Gazebo per contatti, gravita, presa fisica e stato degli oggetti; mantenere coerente la scena del pianificatore con il simulatore. Preparare poi una telecamera simulata.
3. Introdurre computer vision: immagini, segmentazione rosso/blu, posizione degli oggetti e trasformazione nel frame robot. Sostituire l'ingresso a pose note con misure percettive, mantenendo la logica di manipolazione gia verificata. Confrontare con ground truth per misurare l'errore.
4. Integrare smistamento, verifica del deposito, recupero da presa o percezione fallite e prove ripetibili. La robustezza della cancellazione reale resta un limite distinto gia documentato.

Questa e una roadmap proposta per il progetto, non una dichiarazione di implementazioni completate. Il prossimo esercizio concreto resta la chiusura delle verifiche della scena; la computer vision seguira la manipolazione da pose note e la preparazione dell'ambiente sensoriale. Mappa PERCORSO.md aggiornata per rimuovere indicazioni correnti rimaste ferme al 12 ottobre.

### 26.5 Checkpoint - sei oggetti presenti sul server MoveIt

**24 ottobre 2026:** Matteo invia l'output completo di scene_inspector: servizio disponibile, richiesta riuscita, Numero oggetti: 6 e ID bin_blue, bin_red, piece_blue_1, piece_red_1, piece_red_2, work_table. La presenza di tutti gli ID attesi e ora confermata da risposta reale del server, inclusi i due contenitori.

Il log conferma anche la terminologia corretta di lettura della scena nell'inspector. Non allegati build_bin_object, modifiche ai metadati, output del percorso installato o immagine RViz: non inferirli dal solo elenco dei nomi. La richiesta WORLD_OBJECT_NAMES non verifica tipo e triangoli delle geometrie, pose o collisioni. Le prove di mesh e collisione vengono chiuse con il blocco 28. Nessun sorgente Ubuntu modificato dall'assistente.

## 28. Esercizio 19 - lettura delle mesh e prova controllata delle collisioni

**Consegna del 24 ottobre 2026, ancora da eseguire.** Ultimo blocco di validazione della scena prima del passaggio alla manipolazione da pose note. Riutilizzare inspector e loader; nessun nuovo nodo necessario. Lasciare la demo attiva e il commander fermo: si interrogano stati e si modifica temporaneamente la posa di un contenitore nella scena, senza esecuzioni di traiettorie.

### 28.1 Leggere la geometria dal server

Nella richiesta dell'inspector combinare le due maschere con OR bit a bit:

```python
request.components.components = (
    PlanningSceneComponents.WORLD_OBJECT_NAMES
    | PlanningSceneComponents.WORLD_OBJECT_GEOMETRY
)
```

Le costanti sono flag selezionabili: | combina le selezioni; or e un operatore logico e non le combina. Verificare le definizioni della versione installata con ros2 interface show moveit_msgs/msg/PlanningSceneComponents.

Nel ciclo degli oggetti aggiungere un log con ID, numero di primitives e meshes. Esempio:

```python
self.get_logger().info(
    f'{obj.id}: primitive={len(obj.primitives)}, mesh={len(obj.meshes)}'
)
```

Per ciascuna mesh loggare anche len(mesh.triangles). Attesi una mesh da 28 triangoli e zero primitive per ogni contenitore; una primitiva per tavolo e ciascun cubo. Non imporre 84 vertici nel messaggio riletto, poiche il server puo ricostruire la rappresentazione geometrica. Nessuna modifica della scena tramite l'inspector.

### 28.2 Nuova API GetStateValidity

Verificare nell'ambiente ROS:

```bash
ros2 service type /check_state_validity
ros2 interface show moveit_msgs/srv/GetStateValidity
ros2 interface show moveit_msgs/msg/ContactInformation
```

Tipo atteso moveit_msgs/srv/GetStateValidity. La richiesta ha robot_state, group_name e constraints. La risposta include valid e contacts. robot_state.is_diff=True con campi articolari vuoti viene applicato allo stato corrente monitorato dal server; group_name vuoto seleziona l'intero robot, compresi base e pinza. Non vengono inviati goal o movimenti. Con constraints vuoti non introduciamo nuovi vincoli espliciti.

Fonte della semantica del servizio: https://moveit.picknik.ai/main/api/html/state__validation__service__capability_8cpp_source.html ; il server copia lo stato corrente, applica il RobotState ricevuto e restituisce l'esito con i contatti. Per le interfacce usare la versione locale Jazzy. Ogni contatto ha contact_body_1 e contact_body_2; non assumere un ordine fisso.

Comando di interrogazione corrente:

```bash
ros2 service call /check_state_validity moveit_msgs/srv/GetStateValidity "{robot_state: {is_diff: true}, group_name: ''}"
```

La chiamata legge la scena corrente sul server. Il fatto che un contenitore si sovrapponga ad altri oggetti del mondo non e la collisione cercata: serve un contatto fra il robot e la mesh.

### 28.3 Tre prove: normale, collisione, ripristino

1. Con la scena normale caricata, interrogare GetStateValidity. Atteso valid=True. Se e False, leggere i contatti e diagnosticare prima di alterare la scena per la prova negativa.
2. Nel loader modificare temporaneamente solo la posizione passata a build_bin_object per bin_red da (0.75, -0.22, 0.0) a (0.0, 0.0, 0.02). ID, mesh e frame restano quelli del builder (panda_link0). La posizione di prova colloca il fondo nella zona della base robot; deve produrre un'intersezione con un corpo del robot, da confermare tramite contacts, non per sola aspettativa geometrica.
3. Riavviare il loader aggiornato e attendere il risultato di ApplyPlanningScene. Ripetere GetStateValidity: atteso valid=False con un contatto il cui contact_body_1 o contact_body_2 sia bin_red e l'altro un link Panda. Se manca quel contatto, non dichiarare provata la collisione della mesh; inviare la risposta per adattare la posa di prova alla geometria effettiva del robot.
4. Ripristinare comunque il valore originale (0.75, -0.22, 0.0), salvare, riavviare il loader e interrogare di nuovo: atteso valid=True, con la medesima configurazione del robot della prima prova. La verifica finale chiude il ripristino, non basta correggere soltanto il sorgente.

Dopo modifiche eseguire py_compile dei moduli toccati e build del package, caricando l'overlay nel terminale runtime. Con symlink-install le modifiche Python normalmente sono lette al riavvio, ma la stessa procedura di build rimane utilizzabile. Non modificare matrice delle collisioni ammesse, controllori o pianificatore per ottenere il risultato desiderato.

Consegna unica: modifiche all'inspector, output dei conteggi geometrici e tre risposte del servizio (normale, collisione con bin_red, ripristino). Una prova robot-contro-mesh non dimostra ancora la raggiungibilita della pinza dentro il contenitore o il deposito: quei controlli appartengono alla prossima fase. Nessuna di queste prove e ancora confermata; nessuna scena reale o sorgente Ubuntu modificato dall'assistente.

### 28.4 Checkpoint - collisione reale del contenitore rilevata da MoveIt

**24 ottobre 2026:** Matteo invia la risposta GetStateValidity con bin_red posizionato alla base del Panda. Esito osservato: valid=False; contacts contiene contact_body_1='bin_red' (WORLD_OBJECT, tipo 1) e contact_body_2='panda_link0' (ROBOT_LINK, tipo 0). Il contatto e riportato nel frame world, con posizione circa (-0.071675, -0.075621, 0.057520) m e depth=0.0375203523 m. Sono presenti cost_sources e constraint_result vuoto.

**Conclusione verificata:** la collisione fra il contenitore caricato nella scena e la base del robot viene effettivamente rilevata. Il test negativo ha il contatto specifico richiesto; non si tratta soltanto di una risposta genericamente non valida. I cost_sources non sono necessari alla valutazione di questo esercizio; depth e un dato geometrico del collision checker, non una misura di deformazione fisica.

**Da completare:** ripristinare nel loader la posizione originale di bin_red (0.75, -0.22, 0.0), salvare, riavviare il loader aggiornato e interrogare nuovamente GetStateValidity. Attesi valid=True e assenza di contatti, senza cambiare la configurazione del robot fra le prove. Non basta il ripristino del sorgente: serve applicare di nuovo la scena e verificare il server.

Non ancora ricevuti l'output della prova normale iniziale, la risposta dopo ripristino o i conteggi geometrici dell'inspector richiesti in 28.1. La prova negativa non conferma quei risultati. Non introdurre ulteriori prove negative se il ripristino e le verifiche pendenti riescono. Nessun sorgente Ubuntu o scena del server modificati dall'assistente.

### 28.5 Checkpoint finale - ripristino e verifiche confermati

**24 ottobre 2026:** Matteo dichiara di avere ripristinato tutto e ottenuto tutti i risultati richiesti. La conferma chiude il ripristino della posa normale di bin_red con riapplicazione della scena, esito valido e assenza di contatti, e il riepilogo geometrico richiesto in 28.1. Sono conferme dell'utente, senza nuovi log o sorgenti allegati; non presentarle come ulteriori esecuzioni osservate direttamente dall'assistente.

**Fase 5 completata nel suo ambito:** scena di pianificazione con tavolo, tre cubi e due contenitori mesh; sei ID letti dal server; geometrie e conteggi confermati; collisione negativa bin_red-panda_link0 documentata dal log in 28.4; ripristino e verifiche finali confermati da Matteo. Non ripetere le stesse prove di chiusura senza nuovi cambiamenti o problemi concreti.

La validazione della scena non comprende ancora raggiungibilita delle pose di presa, ciclo di manipolazione, presa fisica in Gazebo o percezione da immagini. Questi sono gli obiettivi delle fasi successive.

## 29. Passaggio alla fase 6 - manipolazione da pose note

**24 ottobre 2026:** alla conferma del checkpoint 28.5 si conclude la chat della fase 5. Titolo consigliato della nuova chat: Vision Sort Lab - fase 6: manipolazione da pose note. L'assistente prepara il testo di passaggio; non crea o rinomina chat.

### 29.1 Stato da trasferire

- Metodo: Matteo scrive personalmente Python/rclpy; spiegare le API prima dell'uso e fornire la sintassi di base con frammenti mirati. Consegnare blocchi comprensivi di implementazione e verifica; aggiornare la guida a ogni checkpoint.
- Ambiente: ROS 2 Jazzy in Ubuntu WSL, workspace /home/matteo/vision_sort_ws, Panda nella demo MoveIt/RViz; nessuna simulazione fisica Gazebo ancora integrata.
- Gia verificati: pianificazione/esecuzione, verifica dei sette giunti su dati aggiornati, timeout, parametro del primo giunto e undici test locali. Limiti della cancellazione reale e del servizio di pianificazione documentati nelle sezioni 17-18.
- Scena completata: work_table, piece_red_1, piece_blue_1, piece_red_2, bin_red, bin_blue. Builder geometrici separati dai nodi; scena inviata da scene_loader con ApplyPlanningScene e letta da scene_inspector con GetPlanningScene, nomi e geometrie.
- Tavolo: BOX [0.8, 0.8, 0.1], centro (0.6, 0.0, -0.05) nel frame panda_link0, superficie superiore z=0.
- Cubi: lato 0.04 m, centri piece_red_1=(0.45,-0.20,0.02), piece_blue_1=(0.55,0.0,0.02), piece_red_2=(0.45,0.20,0.02).
- Contenitori: stesso open_bin.stl usato come geometria visibile e di collisione; esterno [0.18,0.18,0.08], vano interno XY 0.16 x 0.16 m, fondo spesso 0.01 m, origine al centro della faccia inferiore. Pose normali bin_red=(0.75,-0.22,0.0), bin_blue=(0.75,0.22,0.0), orientamenti identita.
- mesh_builders.load_stl_mesh scritto dall'utente e verificato: 84 voci vertices, 28 triangoli, ultimo [81,82,83]. La risorsa e prevista nei data_files di setup.py e ricercata tramite ament_index_python; python3-stl e il prerequisito APT documentato. Non inventare la chiave rosdep ancora non verificata o il testo finale dei metadati non allegati.
- Verifica collisioni: GetStateValidity con stato diff vuoto e gruppo vuoto; spostamento temporaneo di bin_red alla base ha dato valid=False e contatto bin_red-panda_link0. Ripristino e risultati finali confermati dall'utente. La scena normale e quella da conservare.

### 29.2 Primo blocco della nuova fase

Iniziare da un solo oggetto, piece_red_1, e da pose note. Primo obiettivo didattico: identificare il link di riferimento effettivo della pinza/TCP e leggerne la posa corrente; spiegare la differenza fra target articolare e posa cartesiana, posizione e orientamento. Non assumere arbitrariamente che panda_hand, panda_link8 o un eventuale frame di presa siano intercambiabili. Verificare nomi e trasformazioni nella configurazione locale prima di fissare pose numeriche di presa.

Poi assegnare un primo obiettivo cartesiano e verificarne la pianificazione, prima di comporre avvicinamento e presa. Le API nuove verranno spiegate nella nuova chat prima della consegna: nessun codice di manipolazione e ancora stato scritto o verificato. Conservare la gestione dei risultati e dei fallimenti gia studiata senza riscrivere l'intero progetto.

La progressione resta: avvicinamento, comando pinza, gestione dell'oggetto libero/collegato nella scena, sollevamento, trasporto, deposito e distacco. Un aggancio ideale in MoveIt verra dichiarato e non varra come prova di presa fisica. Dopo il ciclo da pose note seguiranno Gazebo e quindi computer vision, come nella roadmap di sezione 27.

### 29.3 Testo di passaggio preparato

Riprendiamo Vision Sort Lab nella fase 6, manipolazione da pose note. Leggi prima GUIDA-PROGETTO.md nel percorso Windows del progetto, in particolare le sezioni 27-29. La fase 5 della scena e conclusa: sei oggetti caricati, contenitori mesh verificati, collisione bin_red-panda_link0 rilevata da GetStateValidity e ripristino normale con verifiche finali confermato. Non ripetere quelle prove salvo nuovi problemi.

Scrivo personalmente Python/rclpy: spiega prima le API nuove, mostra la sintassi di base e assegna blocchi che includano implementazione e verifica. Aggiorna la guida a ogni checkpoint. L'ambiente e ROS 2 Jazzy su Ubuntu WSL, workspace /home/matteo/vision_sort_ws, Panda nella demo MoveIt/RViz; Gazebo e computer vision arriveranno dopo.

Iniziamo da piece_red_1: prima identificazione del link pinza/TCP e lettura della posa corrente, poi primo obiettivo cartesiano e pianificazione. Non considerare gia realizzati presa, collegamento dell'oggetto, trasporto o deposito. Pianificazione/esecuzione articolare, verifica dei sette giunti, timeout e undici test locali sono gia acquisiti; i limiti della cancellazione reale restano documentati. Conserva il vincolo di usare la stessa mesh per visualizzazione della scena e collisioni.

## 30. Esercizio 20 - riferimento della pinza e posa corrente con TF2

**24 ottobre 2026: fase 6 ripresa.** Lette le sezioni 27–29. Il checkpoint 28.5 resta acquisito: nessuna ripetizione delle prove della fase 5. Primo oggetto del futuro ciclo: `piece_red_1`, centro `(0.45, -0.20, 0.02)` m in `panda_link0`, lato `0.04` m, faccia superiore a `z=0.04` m. In questo blocco si legge il robot; non si sceglie ancora una posa di presa.

### 30.1 Checkpoint documentale - configurazione locale letta

L'assistente ha letto, senza modificarli, i seguenti file nell'Ubuntu WSL dell'utente:

- `/opt/ros/jazzy/share/moveit_resources_panda_moveit_config/config/panda.srdf`;
- `/opt/ros/jazzy/share/moveit_resources_panda_moveit_config/config/panda.urdf.xacro`;
- `/opt/ros/jazzy/share/moveit_resources_panda_moveit_config/config/kinematics.yaml`;
- `/opt/ros/jazzy/share/moveit_resources_panda_description/urdf/panda.urdf` e `panda.urdf.xacro`;
- `setup.py` e `package.xml` in `/home/matteo/vision_sort_ws/src/vision_sort_lab`.

Risultati effettivamente letti:

| Riferimento | Evidenza e significato |
|---|---|
| `panda_link0` | Base della catena `panda_arm`; stesso frame dei nostri oggetti della scena |
| `panda_link8` | Tip della catena nel SRDF; parent link dell'end effector `hand` |
| `panda_hand` | Link della pinza, collegato a `panda_link8` dal giunto fisso `panda_hand_joint` |
| Trasformazione link8 → hand | `xyz="0 0 0"`, `rpy="0 0 -0.785398163397"`: stessa origine, assi ruotati di -45 gradi attorno a Z |
| TCP distinto | Nessun link/frame TCP dedicato definito negli URDF/Xacro letti; non inventare nomi come `panda_hand_tcp` |
| Cinematica | `panda_arm` usa `kdl_kinematics_plugin/KDLKinematicsPlugin`, risoluzione `0.005`, timeout `0.05` |

L'Xacro della configurazione include quello della descrizione letto. Queste sono evidenze dei file installati, non una lettura del parametro `robot_description` del processo attivo o una misura TF runtime. Le verifiche 30.3 confermeranno i riferimenti pubblicati dalla demo.

Il TCP (Tool Center Point) e il riferimento operativo scelto per il compito, ad esempio un punto fra le dita. L'origine di `panda_hand` non diventa automaticamente il centro di presa. Per questo esercizio leggiamo `panda_hand`; prima di una presa dovremo stabilire il punto operativo e il suo offset rispetto al link. Non introdurre ora nuovi link o broadcaster statici.

Metadati letti: gli entry point correnti sono `joint_monitor`, `motion_commander`, `scene_inspector`, `scene_loader`; `tf2_ros_py` non e ancora dichiarato in `package.xml`. Sono presenti la risorsa `meshes/open_bin.stl` nei `data_files` e `ament_index_python` nelle dipendenze runtime. La stessa mesh dei contenitori resta usata per scena visibile e collisioni.

### 30.2 Concetti e nuove API, prima della consegna

Il target articolare specifica i sette valori dei giunti. Un target di posa specifica posizione e orientamento di un riferimento terminale rispetto a un frame noto; il pianificatore dovra trovare giunti compatibili. Una posa cartesiana obiettivo non impone da sola una traiettoria rettilinea della pinza: il percorso cartesiano sara un argomento distinto.

La posa comprende posizione `(x, y, z)` in metri e orientamento. In ROS l'orientamento viene comunemente espresso con un quaternion `(x, y, z, w)` normalizzato: quattro componenti che rappresentano una rotazione, non quattro angoli. L'identita `(0, 0, 0, 1)` significa assi allineati al frame di riferimento, non genericamente pinza rivolta verso il basso. `q` e `-q` rappresentano la stessa rotazione.

TF2 gestisce le trasformazioni fra frame. `robot_state_publisher` pubblica quelle del robot dal modello e dagli stati dei giunti; la posa letta e quindi ricavata dal modello e dagli stati pubblicati, non misurata da una telecamera. Gli ID degli oggetti MoveIt, incluso `piece_red_1`, non creano automaticamente frame TF.

Nuove classi:

- `Buffer`: conserva le trasformazioni ricevute e permette di interrogare la catena fra frame.
- `TransformListener`: sottoscrive `/tf` e `/tf_static` e alimenta il buffer. Mantenerlo come attributo del nodo.
- `Time()` di `rclpy.time`: valore temporale zero; nel lookup TF richiede l'ultima trasformazione disponibile lungo la catena, non necessariamente un campione recente.
- `TransformException`: famiglia di errori TF, ad esempio frame assente, catena scollegata o trasformazione non disponibile all'istante richiesto.

Import mirati da integrare nel nodo scritto da Matteo:

```python
from rclpy.time import Time
from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener
```

Nel costruttore, dopo `super().__init__`, il buffer e il listener vengono conservati nel nodo. Un timer gia noto effettua i tentativi dopo l'avvio dello spin:

```python
self.tf_buffer = Buffer()
self.tf_listener = TransformListener(self.tf_buffer, self)
self.pose_timer = self.create_timer(1.0, self.read_pose)
```

`lookup_transform(target_frame, source_frame, time)` restituisce un `geometry_msgs/msg/TransformStamped`. Il primo argomento e il frame in cui esprimere il risultato; il secondo e quello di cui leggere la posa. Esempio di interrogazione nella callback, con `self.tool_frame` letto da un parametro ROS gia studiato:

```python
try:
    transform = self.tf_buffer.lookup_transform(
        'panda_link0', self.tool_frame, Time()
    )
except TransformException as exc:
    self.get_logger().info(f'TF non ancora disponibile: {exc}')
    return
```

Il significato e: posa di `self.tool_frame` espressa in `panda_link0`. Non invertire gli argomenti. Il lookup compone automaticamente i passaggi intermedi. Il buffer puo essere vuoto nei primi tentativi: lasciare che la callback ritorni e che il timer ritenti. Il timeout predefinito e zero; non aggiungere attese bloccanti o `sleep` nella callback del nostro executor a singolo thread.

Campi del risultato, da usare dopo il blocco `try/except`:

```python
position = transform.transform.translation
orientation = transform.transform.rotation
stamp = transform.header.stamp
```

`position` espone `x`, `y`, `z`; `orientation` espone `x`, `y`, `z`, `w`; `stamp` espone `sec` e `nanosec`. Il risultato include anche `header.frame_id` (riferimento) e `child_frame_id` (frame osservato). Per stampare i nanosecondi con nove cifre: `f'{stamp.sec}.{stamp.nanosec:09d}'`. Non confondere `TransformStamped.transform.translation/rotation` con i campi di `PoseStamped.pose.position/orientation`, che studieremo quando serviranno.

### 30.3 Consegna unica - implementazione e verifica

**Ancora da eseguire da Matteo.** Lasciare la demo aperta, il commander fermo e la scena normale. L'assistente non ha scritto il nodo o modificato la scena.

1. In un terminale Ubuntu con ROS e overlay caricati, interrogare la trasformazione fissa, quindi interrompere con `Ctrl+C` e interrogare la posa della pinza nella base:

   ```bash
   source /opt/ros/jazzy/setup.bash
   source /home/matteo/vision_sort_ws/install/setup.bash
   ros2 run tf2_ros tf2_echo panda_link8 panda_hand
   ```

   Atteso dalla configurazione letta: traslazione circa zero e RPY circa `(0, 0, -0.785398)` rad. Il quaternion equivalente e circa `(0, 0, -0.382683, 0.923880)`, oppure il suo opposto. Per la trasformazione puramente fissa lo stamp puo essere zero.

   ```bash
   ros2 run tf2_ros tf2_echo panda_link0 panda_hand
   ```

   Questo comando legge la posa di `panda_hand` espressa in `panda_link0`; non comanda il robot. Non imponiamo una posa numerica della pinza: dipende dai giunti correnti. Eventuali avvisi di attesa iniziali devono lasciare posto a un risultato. Se la trasformazione fissa contraddice i file letti, fermarsi alla lettura e riportare l'esito per chiarire il modello attivo.

2. Scrivere `/home/matteo/vision_sort_ws/src/vision_sort_lab/vision_sort_lab/tool_pose_reader.py`, classe `ToolPoseReader(Node)`. Usare il ciclo `main`/spin/chiusura gia appreso. Dichiarare `tool_frame` con default `panda_hand`; creare buffer, listener e timer a un secondo. Nella callback gestire gli errori TF come sopra e loggare a ogni successo frame, posizione con almeno quattro decimali, quaternion, stamp e norma del quaternion, attesa circa `1.0`. Per la norma basta la radice di `x*x + y*y + z*z + w*w`. Nessun servizio di movimento o modifica della scena.

3. Integrare i metadati esistenti, senza duplicare le sezioni. In `package.xml` aggiungere la dipendenza diretta Python:

   ```xml
   <exec_depend>tf2_ros_py</exec_depend>
   ```

   `tf2_ros` e il modulo importato, `tf2_ros_py` il pacchetto ROS della libreria Python; `tf2_ros` e anche il pacchetto del comando CLI `tf2_echo`. Non installare pacchetti omonimi con pip. Aggiungere alla lista `console_scripts` di `setup.py`:

   ```python
   'tool_pose_reader = vision_sort_lab.tool_pose_reader:main',
   ```

4. Controllare sintassi, costruire e avviare il proprio nodo:

   ```bash
   cd /home/matteo/vision_sort_ws
   python3 -m py_compile src/vision_sort_lab/vision_sort_lab/tool_pose_reader.py
   colcon build --symlink-install --packages-select vision_sort_lab
   source install/setup.bash
   ros2 run vision_sort_lab tool_pose_reader
   ```

   Con il robot fermo confrontare posizione e orientamento con il precedente `tf2_echo panda_link0 panda_hand`: attesi valori coincidenti entro gli arrotondamenti. Per i quaternion accettare anche il segno globale opposto. Nella catena dalla base alla pinza gli stamp devono aggiornarsi mentre arrivano gli stati del robot; una posizione costante da sola non dimostra dati aggiornati. In questo blocco non si implementa ancora un filtro temporale per l'esecuzione. Dopo `Ctrl+C`, riavviare con il parametro gia studiato:

   ```bash
   ros2 run vision_sort_lab tool_pose_reader --ros-args -p tool_frame:=panda_link8
   ```

   A parita di stato del robot, posizione uguale alla lettura di `panda_hand`, orientamento diverso secondo la trasformazione fissa; non aspettarsi di sottrarre semplicemente 45 gradi a una componente del quaternion.

Consegna per la revisione: `tool_pose_reader.py`, una lettura di ciascuno dei due comandi `tf2_echo`, due righe consecutive del nodo per `panda_hand` e una per `panda_link8`, oltre all'esito della build. Le letture e l'implementazione non sono ancora confermate.

### 30.4 Passo successivo e fonti

Dopo la verifica della posa, introdurre un primo goal cartesiano vicino alla posa corrente, conservando inizialmente l'orientamento e richiedendo solo pianificazione. Spiegare prima le nuove interfacce e i vincoli di posizione/orientamento, riusando il percorso di pianificazione gia studiato. Una posa cartesiana non equivale a un percorso rettilineo. Poi definire il riferimento operativo e la pre-presa di `piece_red_1`; non usare il centro del cubo come posizione dell'origine di `panda_hand` senza considerare gli offset e le geometrie. Presa, collegamento, trasporto e deposito restano da implementare.

API controllate sulle fonti ufficiali del ramo Jazzy; le pagine HTML docs.ros.org erano protette da un controllo di accesso, quindi sono stati consultati i sorgenti ufficiali corrispondenti:

- [Tutorial ROS 2 Jazzy: listener Python](https://raw.githubusercontent.com/ros2/ros2_documentation/jazzy/source/Tutorials/Intermediate/Tf2/Writing-A-Tf2-Listener-Py.rst).
- [Buffer Python Jazzy: ordine dei frame, Time zero e timeout](https://github.com/ros2/geometry2/blob/jazzy/tf2_ros_py/tf2_ros/buffer.py).
- [TransformListener Python Jazzy: sottoscrizioni TF](https://github.com/ros2/geometry2/blob/jazzy/tf2_ros_py/tf2_ros/transform_listener.py).
- [tf2_echo Jazzy: ordine e stampa delle trasformazioni](https://github.com/ros2/geometry2/blob/jazzy/tf2_ros/src/tf2_echo.cpp).

### 30.5 Chiarimento - costruire ToolPoseReader collegandolo alle classi gia studiate

**26 ottobre 2026:** Matteo chiede una spiegazione piu esplicita della costruzione della classe e riferimenti alle classi gia costruite. Il blocco 30.3 resta da implementare e verificare; questa e una precisazione didattica, non un risultato di esecuzione. Nessun file Python Ubuntu modificato dall'assistente.

Riferimenti concreti nella guida:

| Parte di ToolPoseReader | Riferimento gia studiato |
|---|---|
| `class ToolPoseReader(Node)` e `super().__init__` | `JointMonitor` (6.11), `MotionCommander` (7.6), `SceneInspector` (20.2) |
| Parametro stringa `tool_frame` | Parametro `target_joint1` di `MotionCommander` (19.1–19.2): stessa dichiarazione e lettura, con nome e tipo diversi |
| `self.pose_timer` e `self.read_pose` | `self.verification_timer` e `self.check_verification_timeout` di `MotionCommander` (12.2–12.3) |
| Estrarre campi e scrivere log | `JointMonitor.joint_state_callback` (6.11) e `SceneInspector.on_scene_response` (20.2) |
| `main`, spin e pulizia | `main` di `JointMonitor` (6.11) o di `MotionCommander` (7.6) |

La classe eredita direttamente da `Node`; gli altri nodi sono esempi da cui riprendere gli schemi. `ToolPoseReader` e il nome della classe Python; `'tool_pose_reader'` e il nome dato al nodo ROS, scelto uguale al nome dell'eseguibile registrato. Il costruttore viene eseguito quando `main` crea l'istanza. `self` rappresenta quell'istanza; gli attributi con `self.` conservano valori utilizzabili anche dagli altri suoi metodi.

Import per i frammenti seguenti:

```python
import math
import rclpy
from rclpy.node import Node
from rclpy.time import Time
from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener
```

Primo frammento: struttura della classe e costruttore, con callback ancora da completare. E materiale da integrare personalmente, non un file completo gia installato:

```python
class ToolPoseReader(Node):
    def __init__(self):
        super().__init__('tool_pose_reader')

        self.declare_parameter('tool_frame', 'panda_hand')
        self.tool_frame = self.get_parameter('tool_frame').value

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        self.pose_timer = self.create_timer(1.0, self.read_pose)

    def read_pose(self):
        # TODO: lookup TF, estrazione dati e log.
        pass
```

Come nel commander, il parametro viene dichiarato dopo `super().__init__` e letto una volta nel costruttore. Il default stringa determina il tipo stringa; `.value` restituisce qui una stringa Python. Il parametro ROS `tool_frame` e l'attributo Python `self.tool_frame` sono due elementi distinti: in questo blocco non implementiamo aggiornamenti dinamici del parametro.

`Buffer()` crea il contenitore delle trasformazioni; `TransformListener(self.tf_buffer, self)` collega il listener a quel contenitore e al nodo corrente. Il secondo argomento e il nodo stesso, come `self` passato all'`ActionClient` nel `MotionCommander`. Il listener gestisce le sottoscrizioni TF. L'executor le elabora durante lo spin e il buffer viene alimentato con le trasformazioni ricevute.

Il timer riprende esattamente lo schema del timeout: periodo `1.0` secondi e callback `self.read_pose`, passata senza parentesi. `self.read_pose()` eseguirebbe il metodo subito e passerebbe il suo valore di ritorno a `create_timer`. La periodicita e nominale, non una garanzia di esecuzione al secondo esatto.

Firme delle callback da distinguere:

- `JointMonitor.joint_state_callback(self, msg)`: l'executor passa il messaggio ricevuto dalla subscription.
- `SceneInspector.on_scene_response(self, future)`: il completamento del Future attiva la callback e le passa quel Future.
- `MotionCommander.check_verification_timeout(self)` e `ToolPoseReader.read_pose(self)`: il timer non passa un messaggio o un Future; il metodo usa gli attributi del nodo.

Secondo frammento: sostituire il metodo con `pass` mantenendo `read_pose` alla stessa indentazione di `__init__`. Dopo il lookup riuscito, estrarre i dati e calcolare la norma:

```python
def read_pose(self):
    try:
        transform = self.tf_buffer.lookup_transform(
            'panda_link0', self.tool_frame, Time()
        )
    except TransformException as exc:
        self.get_logger().info(f'TF non ancora disponibile: {exc}')
        return

    position = transform.transform.translation
    orientation = transform.transform.rotation
    stamp = transform.header.stamp

    quaternion_norm = math.sqrt(
        orientation.x ** 2 + orientation.y ** 2
        + orientation.z ** 2 + orientation.w ** 2
    )

    # TODO: costruire il testo del log e stamparlo con get_logger().info().
```

Il frammento del metodo e mostrato a partire dalla sua prima colonna per facilitarne la lettura; nel file deve essere dentro la classe, indentato di quattro spazi. Il `return` del ramo errore termina solo quel tentativo; il timer rimane attivo e l'executor potra riprovare. Le variabili `transform`, `position`, `orientation`, `stamp` e `quaternion_norm` possono restare locali: vengono usate subito dalla stessa callback. Il prefisso `self.` e necessario per lo stato da condividere fra costruttore e callback, come frame e buffer.

La radice quadrata e la funzione standard Python `math.sqrt`; `** 2` eleva al quadrato. La norma e calcolata su tutte e quattro le componenti e deve essere circa uno. `translation` e `rotation` sono i campi effettivi del messaggio TF: non usare `pose.position` su questo tipo di risultato.

Per costruire il log, riprendere il meccanismo delle f-string e di `get_logger().info` gia usato da `JointMonitor`. Esempio mirato per frame e posizione:

```python
self.get_logger().info(
    f'{transform.header.frame_id} -> {transform.child_frame_id}: '
    f'pos=({position.x:.4f}, {position.y:.4f}, {position.z:.4f}) m'
)
```

Da completare personalmente nello stesso testo con quaternion `(x,y,z,w)`, timestamp `f'{stamp.sec}.{stamp.nanosec:09d}'` e norma `f'{quaternion_norm:.6f}'`. Le stringhe adiacenti dentro le parentesi vengono concatenate. Il formato `.4f` stampa quattro cifre dopo il punto; `09d` stampa un intero con nove cifre, aggiungendo zeri a sinistra.

`main` rimane fuori dalla classe, senza indentazione. Riprendere quello di `JointMonitor` in 6.11: costruire `reader = ToolPoseReader()`, usare `rclpy.spin(reader)`, chiamare `reader.destroy_node()` nel `finally` quando l'istanza esiste e chiudere il contesto con `rclpy.try_shutdown()`. Conservare il controllo `if __name__ == '__main__': main()`. Lo spin consente all'executor di elaborare sia le sottoscrizioni del listener sia il timer; il costruttore prepara gli oggetti, il timer effettua le letture periodiche.

Consegna mantenuta come unico blocco: completare classe, log e `main`, integrare i metadati e svolgere le verifiche di 30.3. Inviare il codice e i risultati insieme. Nessuna nuova prova di movimento richiesta e nessuna lettura TF runtime ancora ricevuta.

### 30.6 Chiarimento - campi di TransformStamped e significato della posa

**26 ottobre 2026:** Matteo chiede di spiegare le proprieta di `transform` nelle tre assegnazioni a `position`, `orientation` e `stamp`. Sono stati controllati i messaggi ufficiali ROS 2 Jazzy. Nessun nuovo codice o output runtime ricevuto; la consegna 30.3 resta da completare.

Nel codice `transform` e il nome della variabile Python a cui assegniamo il risultato di `lookup_transform`. Il tipo dell'oggetto restituito e `geometry_msgs/msg/TransformStamped`. Contiene questi campi annidati:

```text
transform                         TransformStamped (variabile locale)
├── header                        Header
│   ├── frame_id                   string
│   └── stamp                     builtin_interfaces/Time
│       ├── sec                   intero
│       └── nanosec               intero
├── child_frame_id                string
└── transform                     Transform
    ├── translation               Vector3
    │   ├── x                     float
    │   ├── y                     float
    │   └── z                     float
    └── rotation                  Quaternion
        ├── x                     float
        ├── y                     float
        ├── z                     float
        └── w                     float
```

In `transform.transform.translation`, il primo `transform` e il nome scelto da noi; il secondo e il campo `transform` definito dal tipo ROS. Il punto permette di accedere a un attributo dell'oggetto alla sua sinistra. E lo stesso meccanismo usato in `SceneInspector` con `response.scene.world.collision_objects` (20.2), dove si attraversano messaggi contenuti in altri messaggi. Per distinguere visivamente nome e campo si potrebbe chiamare la variabile `tf_msg`, ottenendo `tf_msg.transform.translation`; nel codice attuale si puo conservare il nome gia scelto.

Per la chiamata:

```python
transform = self.tf_buffer.lookup_transform(
    'panda_link0', self.tool_frame, Time()
)
```

con `self.tool_frame == 'panda_hand'`, il risultato ha come riferimento `header.frame_id == 'panda_link0'` e come frame osservato `child_frame_id == 'panda_hand'`.

- `transform.transform.translation` descrive la posizione dell'origine di `panda_hand` espressa negli assi di `panda_link0`, in metri. Il campo `x` e la coordinata lungo X della base, e analogamente per Y e Z; non e uno spostamento da inviare al robot.
- `transform.transform.rotation` descrive l'orientamento degli assi di `panda_hand` rispetto alla base, come quaternion `(x,y,z,w)`. Queste quattro componenti sono adimensionali e la loro norma deve essere circa uno. I campi `x,y,z` del quaternion non sono coordinate di posizione. L'identita `(0,0,0,1)` esprime assi allineati al riferimento.
- `transform.header.stamp` e l'istante associato alla trasformazione restituita. `sec` contiene la parte in secondi; `nanosec` la frazione in nanosecondi. Per esprimerlo come secondi decimali: `stamp.sec + stamp.nanosec / 1_000_000_000`. Lo stamp non indica l'istante in cui viene scritto il log. Con trasformazioni puramente statiche puo essere zero; per la catena dinamica base-pinza si osserva l'aggiornamento dei dati.

Le tre assegnazioni:

```python
position = transform.transform.translation
orientation = transform.transform.rotation
stamp = transform.header.stamp
```

creano nomi locali per i sotto-oggetti del messaggio. Non calcolano nuove coordinate e non effettuano copie: `position.x` accede allo stesso campo di `transform.transform.translation.x`. `position` rimane un `Vector3`, `orientation` un `Quaternion` e `stamp` un messaggio `builtin_interfaces/Time`. In questo esercizio usiamo quei nomi per leggere e stampare i campi.

Distinguere inoltre `Time()` usato come argomento del lookup, che e un oggetto `rclpy.time.Time`, dal messaggio temporale `header.stamp`. Nel lookup il valore temporale zero richiede l'ultima trasformazione disponibile; non garantisce da solo che il dato sia recente.

Come verifica della struttura si puo usare il comando ROS gia studiato:

```bash
ros2 interface show geometry_msgs/msg/TransformStamped
```

Mostra il tipo e i campi del messaggio; non legge una posa dalla demo. Il comando e proposto per consultazione, non e stato eseguito in questo chiarimento. Nessuna modifica dei file Python Ubuntu o della scena.

Fonti ufficiali Jazzy consultate: [TransformStamped](https://github.com/ros2/common_interfaces/blob/jazzy/geometry_msgs/msg/TransformStamped.msg), [Transform](https://github.com/ros2/common_interfaces/blob/jazzy/geometry_msgs/msg/Transform.msg), [Header](https://github.com/ros2/common_interfaces/blob/jazzy/std_msgs/msg/Header.msg), [Quaternion](https://github.com/ros2/common_interfaces/blob/jazzy/geometry_msgs/msg/Quaternion.msg).

### 30.7 Checkpoint - reader scritto e lettura TF riuscita

Matteo ha inviato ToolPoseReader completo: parametro tool_frame, Buffer, TransformListener, timer a un secondo, lookup non bloccante con TransformException, estrazione dei campi e norma del quaternion. Le prime sette letture allegate mostrano posa stabile e stamp aggiornati. La classe e stata rivista; non sono stati modificati sorgenti Ubuntu dall'assistente.

**27 ottobre 2026:** durante il riavvio e comparso un TypeError nel log: il separatore `|` era stato scritto fuori dalle stringhe. La correzione spiegata consiste nell'inserirlo dentro le f-string, concatenate automaticamente fra parentesi. L'avviso iniziale TF non disponibile era gestito dall'except; il crash avveniva nella stampa di una lettura successiva. Matteo allega poi una nuova lettura riuscita:

```text
panda_link0 -> panda_hand
pos=(0.3070, -0.0000, 0.5903) m
quaternion=(0.9999999801832394, 0.00019908169372384601,
            -3.6082248300317592e-16, 3.463743181164603e-12)
timestamp=1793112392.100725477
norma=1.000000
```

La lettura della pinza nella base e confermata. Non sono stati allegati i confronti tf2_echo o l'override panda_link8; non presentarli come eseguiti. Il primo piano usa lo stesso panda_hand gia letto. Il reader osserva lo stato corrente; SceneInspector legge invece gli oggetti della scena e non e lo strumento per confrontare questa posa.

## 31. Primo obiettivo di posa - pianificazione riuscita

### 31.1 Implementazione discussa e rivista

Obiettivo didattico: acquisire la posa corrente di panda_hand in panda_link0 e costruire un PoseStamped con stessa X/Y, Z aumentata di 0.03 m e quaternion copiato. Si tratta di una prima prova vicina allo stato corrente, non della pre-presa di piece_red_1.

Matteo ha inviato i due builder aggiunti a motion_builders.py:

- `build_pose_goal_constraints(target, link_name)`: un Constraints contenente PositionConstraint e OrientationConstraint per lo stesso link. Posizione entro una sfera di raggio 0.005 m, offset del punto nullo; orientamento con ROTATION_VECTOR e tolleranze di 0.05 rad sulle tre componenti dell'errore. I due vincoli stanno nello stesso goal e devono essere entrambi soddisfatti.
- `build_pose_plan_request(target, link_name)`: GetMotionPlan, gruppo panda_arm, un tentativo, 5.0 s, scaling velocita/accelerazione 0.2, stato iniziale diff e il solo goal di posa. I builder ricevuti sono corretti per il blocco.

Il nodo PosePlanner riprende buffer/listener da ToolPoseReader e client/Future/callback da MotionCommander. Un timer controlla service_is_ready senza attese bloccanti, acquisisce TF e invia una sola richiesta; dopo l'invio imposta plan_requested e disattiva il timer. Questo e diverso dal ciclo wait_for_service usato nel costruttore del commander: il controllo periodico lascia all'executor il tempo di elaborare le callback TF.

Revisione del nodo ricevuto: mancava l'inizializzazione di self.tool_frame; erano rimasti dal commander request_execution e il blocco retry con attributi/metodi non definiti nella nuova classe. Sono state indicate l'inizializzazione a panda_hand, la coerenza del link fra lettura e builder, la rimozione di quelle chiamate e il controllo della traiettoria non vuota. La callback proposta conserva solo il piano e ne stampa esito, tempo e punti. Il main ricevuto protegge correttamente anche la costruzione del nodo con try/finally. Il listato finale completo dopo le correzioni non e stato nuovamente allegato.

### 31.2 Checkpoint - risultato reale del servizio

**27 ottobre 2026:** Matteo allega il log di pose_planner e conferma il funzionamento:

```text
Servizio di pianificazione disponibile
Target panda_hand in panda_link0:
  pos=(0.3070, -0.0000, 0.6203) m
  q=(1.000000, 0.000199, -0.000000, 0.000000)
Pianificazione riuscita: SUCCESS (1) | tempo=0.018 s | punti=10
```

**Verificato dal log:** target coerente con la lettura del reader, Z aumentata di 0.03 m, quaternion coincidente entro gli arrotondamenti, risposta positiva e traiettoria non vuota. E il primo piano di posa riuscito documentato nel progetto. Il log contiene un solo invio/risultato mostrato; non misura autonomamente i tre secondi aggiuntivi richiesti nella consegna.

Questa prova conferma il piano restituito da MoveIt. Non documenta esecuzione o posa raggiunta. I goal finali non impongono da soli una traiettoria cartesiana rettilinea o orientamento costante durante tutto il percorso. Non e ancora stata verificata esplicitamente la posa corrispondente all'ultimo punto articolare del piano.

### 31.3 Punto di ripresa

Prossimo blocco: ricavare dal piano i nomi dei giunti e le posizioni dell'ultimo punto, calcolarne la posa di panda_hand nel frame base e confrontarla con il target usando le tolleranze gia definite. Spiegare le nuove API prima di assegnare l'implementazione. Dopo questa verifica, integrare esecuzione e controllo della posa raggiunta riutilizzando la gestione dell'action gia studiata.

Restano successivi: riferimento operativo/TCP di presa, pre-presa di piece_red_1, avvicinamento, pinza, oggetto collegato nella scena, sollevamento, trasporto e deposito. La scena normale e la stessa mesh dei contenitori per visualizzazione e collisioni restano il riferimento. Nessuna ripetizione delle prove della fase 5 richiesta e nessun file Python Ubuntu modificato dall'assistente.

## 32. Esercizio 22 - verificare il punto finale del piano prima dell'esecuzione

**Consegna del 27 ottobre 2026; implementazione rivista e prova positiva ricevuta il 28 ottobre (32.7).** Estendere PosePlanner: ultimo stato articolare del piano → posa prevista tramite GetPositionFK → confronto della posizione → valutazione dei vincoli con GetStateValidity. Nessuna esecuzione in questo esercizio. Matteo scrive il codice; l'assistente aggiorna soltanto la documentazione.

### 32.1 Perche usare cinematica diretta e vincoli

ToolPoseReader interroga TF sullo stato pubblicato del robot, che in questa prova resta fermo. Per conoscere la posa prevista alla fine del piano dobbiamo invece usare i valori articolari dell'ultimo punto. La cinematica diretta (FK, Forward Kinematics) calcola la posa di un link da una configurazione dei giunti, usando il modello robotico. Non e una misura di posa raggiunta e non verifica da sola collisioni o goal.

GetStateValidity e gia stato studiato nella fase 5. Ora gli inviamo il nuovo stato finale e i vincoli del piano per valutare quel goal, senza spostare oggetti o ripetere la prova negativa dei contenitori. Questa scelta conserva esattamente la semantica di ROTATION_VECTOR con tre tolleranze di 0.05 rad: una singola soglia sull'angolo totale del quaternion non e equivalente a tre soglie sulle componenti dell'errore.

### 32.2 Nuova API GetPositionFK e dati della traiettoria

Verificare nell'ambiente Ubuntu:

```bash
ros2 service type /compute_fk
ros2 interface show moveit_msgs/srv/GetPositionFK
ros2 interface show moveit_msgs/msg/RobotState
```

Tipo atteso moveit_msgs/srv/GetPositionFK. Il servizio e definito dal MoveIt ufficiale come compute_fk; il nome del servizio locale resta da confermare dal comando.

| Richiesta FK | Uso nel blocco |
|---|---|
| header.frame_id | panda_link0: riferimento delle pose restituite |
| fk_link_names | Lista con il solo self.tool_frame, attualmente panda_hand |
| robot_state.joint_state.name | Nomi presi dalla traiettoria |
| robot_state.joint_state.position | Posizioni dell'ultimo punto, nello stesso ordine dei nomi |
| robot_state.is_diff | True: stato parziale, con i sette giunti del braccio esplicitamente assegnati |

La risposta ha error_code, fk_link_names e pose_stamped, una lista di PoseStamped. La lista dei link identifica la posa corrispondente a ciascun elemento. Per una richiesta a un solo link attendiamo esattamente una posa e il nome richiesto. Il servizio 2.12.4 parte dallo stato monitorato e applica i giunti ricevuti; tutti i sette giunti del braccio devono quindi essere presenti. Gli altri valori del robot restano quelli del server. Il timestamp della posa FK e quello del calcolo sul server, non il tempo futuro di arrivo del robot.

La traiettoria articolare si legge cosi:

```python
trajectory = self.planned_trajectory.joint_trajectory
last_point = trajectory.points[-1]
joint_names = list(trajectory.joint_names)
joint_positions = list(last_point.positions)
```

`[-1]` seleziona l'ultimo elemento di una lista o sequenza Python. joint_names e joint_positions devono avere la stessa lunghezza e lo stesso ordine: l'elemento i delle posizioni appartiene al nome i. Come nel JointMonitor conta l'associazione nome-valore; qui i due elenchi della traiettoria la forniscono gia. Non ordinare i nomi separatamente dalle posizioni. Controllare lista non vuota, lunghezze coerenti e presenza una sola volta dei sette nomi panda_joint1…panda_joint7 prima di inviare FK.

### 32.3 Conservare il target del piano e preparare i client

Import aggiuntivi in pose_planner.py:

```python
import math
from moveit_msgs.srv import GetPositionFK, GetStateValidity
```

Conservare gli import esistenti, incluso GetMotionPlan. Nessuna nuova dipendenza esterna: math e deepcopy appartengono alla libreria standard, i servizi a moveit_msgs.

Nel costruttore, dopo gli altri client e prima della creazione del timer:

```python
self.fk_client = self.create_client(GetPositionFK, '/compute_fk')
self.validity_client = self.create_client(
    GetStateValidity, '/check_state_validity'
)
self.fk_future = None
self.validity_future = None
self.target_pose = None
self.target_constraints = None
self.endpoint_state = None
self.endpoint_position_ok = False
self.endpoint_verified = False
```

In try_plan controllare con service_is_ready tutti e tre i client prima di inviare il piano; se ne manca uno ritornare e lasciare ritentare il timer. Usare lo stesso schema non bloccante gia studiato, senza attese dentro le callback.

Subito dopo build_pose_plan_request e prima di call_async conservare i dati dell'operazione:

```python
self.target_pose = deepcopy(target)
self.target_constraints = deepcopy(
    request.motion_plan_request.goal_constraints[0]
)
```

E lo stesso principio di self.target_positions nel MotionCommander: la risposta e la verifica devono usare il riferimento dell'operazione corrente. Le copie conservano il target numerico completo e i vincoli realmente inviati. Non ricostruire il target da TF nella callback e non usare i valori arrotondati stampati nel log.

### 32.4 Tre nuovi metodi nella classe PosePlanner

**1. request_endpoint_fk(self).** Chiamarlo nel ramo positivo di on_plan_response, soltanto dopo SUCCESS, controllo punti non vuoti e assegnazione di self.planned_trajectory. Non aggiungere nuovi timer.

Leggere e verificare i dati finali come in 32.2, quindi costruire la richiesta:

```python
request = GetPositionFK.Request()
request.header.frame_id = self.target_pose.header.frame_id
request.fk_link_names = [self.tool_frame]
request.robot_state.is_diff = True
request.robot_state.joint_state.name = joint_names
request.robot_state.joint_state.position = joint_positions

self.endpoint_state = deepcopy(request.robot_state)
self.fk_future = self.fk_client.call_async(request)
self.fk_future.add_done_callback(self.on_fk_response)
```

I messaggi annidati esistono gia dopo GetPositionFK.Request(): non occorre costruire separatamente JointState. Endpoint_state conserva lo stato ipotetico del piano che invieremo anche al secondo servizio.

**2. on_fk_response(self, future).** Riprendere il recupero della risposta con try/except e describe_moveit_error come in on_plan_response. Se il codice non e SUCCESS, loggare nome/numero e ritornare. Controllare inoltre:

- un elemento in fk_link_names e uno in pose_stamped;
- nome restituito uguale a self.tool_frame;
- header.frame_id della posa uguale al frame del target.

Un risultato con struttura inattesa deve produrre un errore e interrompere la verifica. Altrimenti leggere la posa e confrontare:

```python
predicted = response.pose_stamped[0]
actual_position = predicted.pose.position
target_position = self.target_pose.pose.position

dx = actual_position.x - target_position.x
dy = actual_position.y - target_position.y
dz = actual_position.z - target_position.z
position_error = math.sqrt(dx ** 2 + dy ** 2 + dz ** 2)
self.endpoint_position_ok = position_error <= 0.005
```

Il nome actual_position indica qui la posizione calcolata da FK per quello stato, non una misura fisica. La distanza euclidea corrisponde al raggio della sfera obiettivo. Stampare posa/quaternion previsti, dx/dy/dz e distanza in metri o millimetri con unita esplicite. La posizione finale puo differire dal centro target entro 5 mm.

Nella stessa callback, dopo aver ottenuto e loggato la posa, chiedere la valutazione dei vincoli dello stato finale:

```python
request = GetStateValidity.Request()
request.robot_state = deepcopy(self.endpoint_state)
request.group_name = ''
request.constraints = deepcopy(self.target_constraints)

self.validity_future = self.validity_client.call_async(request)
self.validity_future.add_done_callback(self.on_endpoint_validity_response)
```

Il gruppo vuoto usa l'intero robot, come nella verifica della scena. Il servizio valuta collisioni e vincoli sullo stato fornito, senza applicarlo al robot. La sfera e il vincolo di orientamento sono quelli del goal salvato.

**3. on_endpoint_validity_response(self, future).** Recuperare la risposta con try/except. Questo servizio usa valid, contacts e constraint_result, non error_code. Ogni elemento di constraint_result ha result, booleano relativo al vincolo. Per i nostri due vincoli attendiamo due elementi e due True. Loggare almeno valid, risultati dei vincoli e numero dei contatti.

Impostare endpoint_verified a True soltanto se valid e True, i due risultati dei vincoli sono True e endpoint_position_ok e True. Per controllare gli elementi si puo usare `all(item.result for item in response.constraint_result)`, dopo averne verificato la lunghezza: all restituisce True se tutti i valori sono veri. In caso di lista inattesa, eccezione o esito negativo lasciare endpoint_verified=False e loggare un errore. Nessuna chiamata di esecuzione in questo blocco.

Questa valutazione riutilizza la semantica del pianificatore per il confronto di orientamento. Non sottrarre le componenti dei quaternion come se fossero angoli, e non sostituire le tre tolleranze da 0.05 rad con un unico angolo totale da 0.05 rad.

### 32.5 Verifica e consegna

Lasciare demo e scena normale attive, robot fermo, commander terminato. Dopo le modifiche:

```bash
cd /home/matteo/vision_sort_ws
python3 -m py_compile src/vision_sort_lab/vision_sort_lab/pose_planner.py
colcon build --symlink-install --packages-select vision_sort_lab
source install/setup.bash
ros2 run vision_sort_lab pose_planner
```

Attesi in sequenza: target → piano SUCCESS con punti → FK SUCCESS sullo stato finale → posa prevista vicina al target con distanza <=0.005 m → stato finale valid=True, due vincoli True e nessun contatto → endpoint_verified=True. Il nuovo piano puo avere numero di punti e durata di calcolo diversi da quello gia documentato. ToolPoseReader continua a osservare il robot fermo nella posa attuale, mentre FK restituisce la posa ipotetica finale. Nessuna esecuzione o animazione richiesta.

Consegna unica: righe di inizializzazione e conservazione target, collegamento nel ramo positivo, tre metodi e log completo della nuova sequenza. Non modificare tolleranze o scena per nascondere una discrepanza: se c'e, inviare i dati. Nessuna prova negativa aggiuntiva assegnata. Solo dopo questo checkpoint si affrontera l'esecuzione. Prima revisione dei metodi in 32.6; risultato positivo ricevuto in 32.7. Il listato completo dopo le correzioni non e stato nuovamente allegato.

### 32.6 Revisione dei tre metodi ricevuti - 28 ottobre 2026

Matteo ha inviato request_endpoint_fk, on_fk_response e on_endpoint_validity_response. La costruzione delle due richieste, la conservazione di endpoint_state, il confronto euclideo e la combinazione dei due risultati dei vincoli seguono la consegna. Il listato presenta ancora errori; nessun risultato FK o validita e stato allegato.

Correzioni spiegate con frammenti mirati, lasciando a Matteo la modifica dei sorgenti Ubuntu:

- JointTrajectory non contiene joint_positions: confrontare le variabili locali joint_positions e joint_names. Prima di points[-1] verificare che i punti esistano. Verificare anche sette nomi attesi presenti una sola volta, mantenendo l'ordine originale nomi/posizioni.
- GetPositionFK.Response contiene direttamente error_code, fk_link_names e pose_stamped. Eliminare response.motion_plan_response, copiato dalla callback di GetMotionPlan. In caso di errore riferire il fallimento FK, non un nuovo fallimento di pianificazione.
- Dopo il controllo delle due lunghezze, assegnare returned_link = response.fk_link_names[0] e predicted = response.pose_stamped[0] prima di usarli. returned_link e predicted sono nomi locali scelti nel codice, non campi ROS.
- pose_stamped e una lista: il frame si legge con predicted.header.frame_id, cioe response.pose_stamped[0].header.frame_id. Confrontare quel frame con self.target_pose.header.frame_id prima di sottrarre coordinate.
- In GetStateValidity usare response.valid: response e una variabile locale e valid e il nome del campo booleano. self.response.valide usa sia un attributo del nodo non definito sia un nome di campo errato. Un esito valid=False e una risposta ordinaria, distinta da un'eccezione di future.result(). Nel log dell'eccezione includere exc.
- La f-string con {} vuoto e un errore di sintassi che impedisce l'avvio. Il numero dei contatti e len(response.contacts); la verifica finale e self.endpoint_verified. Preferire get_logger a print e mostrare i booleani [item.result for item in results]. Segnalare il fallimento finale con livello error.
- Aggiungere il log della posa FK, quaternion, dx/dy/dz e distanza con unita; il calcolo ricevuto non li stampava. Inizializzare a False i flag della verifica quando inizia la richiesta FK.

Riferimenti didattici: MotionCommander fornisce lo schema Future/callback ma ogni servizio ha una risposta diversa; JointMonitor insegna l'associazione nome-valore; SceneInspector gia usa GetStateValidity; ToolPoseReader legge la posa corrente, mentre qui FK calcola quella prevista dallo stato finale del piano.

Prossima verifica: correggere il modulo, controllare la sintassi e seguire i comandi di 32.5. Inviare la sequenza completa target/piano/FK/validita. Nessuna esecuzione del piano di posa ancora assegnata. Aggiornata solo la documentazione Windows; nessun sorgente Python Ubuntu modificato dall'assistente.

### 32.7 Checkpoint - verifica del punto finale riuscita

**28 ottobre 2026:** Matteo allega la nuova esecuzione di pose_planner. Alla prima callback pianificazione e FK sono disponibili, mentre il terzo servizio non e ancora pronto; il timer riprova un secondo dopo e la sequenza prosegue normalmente. Non e un errore di pianificazione.

```text
Target panda_hand in panda_link0:
  pos=(0.3070, -0.0000, 0.6203) m
  q=(1.000000, 0.000199, -0.000000, 0.000000)
Pianificazione riuscita: SUCCESS (1) | tempo=0.014 s | punti=9
Posa FK in panda_link0:
  pos=(0.3071, -0.0009, 0.6251) m
  q=(0.999522, 0.021804, 0.011561, -0.018599)
Errore posizione: dx=0.108, dy=-0.852, dz=4.823 mm
  distanza=4.899 mm | entro 5 mm=True
Lo stato finale supera la verifica di validita
Validita dello stato: True | Vincoli: [True, True]
  Numero di contatti: 0 | Verifica endpoint: True
```

**Confermato dal log:** richiesta di pianificazione riuscita, calcolo della posa prevista, distanza entro il raggio di 5 mm e valutazione positiva dei due vincoli originali sullo stato finale senza contatti riportati. La distanza e vicina al bordo della sfera ma rispetta la tolleranza assegnata: non e richiesto arrivare esattamente al centro. Il quaternion FK differisce dal target e il vincolo di orientamento risulta comunque soddisfatto, secondo le tre tolleranze ROTATION_VECTOR configurate. Non dedurre la validita dell'orientamento dalla sola somiglianza dei numeri del quaternion.

Il log mostra una sola sequenza di piano/FK/validita. Non documenta un'attesa aggiuntiva misurata o il listato completo aggiornato. La posa FK resta una previsione dallo stato articolare del piano: nessuna esecuzione del piano di posa o verifica della posa raggiunta e stata documentata. L'esercizio 22 e completato nel caso positivo.

**Punto di ripresa:** integrare l'esecuzione della traiettoria gia verificata, riprendendo ActionClient ed ExecuteTrajectory di MotionCommander, con un solo invio dopo endpoint_verified=True; poi verificare lo stato raggiunto su dati aggiornati e con timeout. Spiegare il collegamento fra i metodi prima della consegna. Conservare il target originale: non ricalcolarlo dalla nuova TF dopo il movimento. Il target didattico Z +0.03 m precede ancora la pre-presa di piece_red_1. Nessuna ripetizione della fase 5, nessuna modifica delle tolleranze o della geometria richiesta. Nessun sorgente Python Ubuntu modificato dall'assistente.

Fonti ufficiali: [GetPositionFK](https://github.com/moveit/moveit_msgs/blob/ros2/srv/GetPositionFK.srv), [RobotState](https://github.com/moveit/moveit_msgs/blob/ros2/msg/RobotState.msg), [JointTrajectory Jazzy](https://github.com/ros2/common_interfaces/blob/jazzy/trajectory_msgs/msg/JointTrajectory.msg), [servizio FK MoveIt 2.12.4](https://github.com/moveit/moveit2/blob/2.12.4/moveit_ros/move_group/src/default_capabilities/kinematics_service_capability.cpp), [GetStateValidity](https://github.com/moveit/moveit_msgs/blob/ros2/srv/GetStateValidity.srv), [valutazione stato e vincoli 2.12.4](https://github.com/moveit/moveit2/blob/2.12.4/moveit_ros/move_group/src/default_capabilities/state_validation_service_capability.cpp). Interfacce MoveIt consultate sul ramo ros2, sorgenti server sul tag 2.12.4; usare ros2 interface show per confrontare i campi installati.

## 33. Esercizio 23 - eseguire il piano di posa verificato

**Proposta iniziale superata dalla sezione 34 per l'organizzazione del codice.** La richiesta successiva di Matteo porta a costruire l'action in un nuovo modulo di supporto. Le istruzioni di 33.3-33.5 e 33.7 che collocano i cinque metodi dentro PosePlanner rimangono come storico e non sono piu la consegna da implementare. API, risultati gia osservati e principi di verifica restano il riferimento. La direzione della verifica successiva in 33.6 resta valida.

### 33.1 Checkpoint documentale - allegato completo letto

**28 ottobre 2026:** letti la guida, il punto 32.7 e il file `pose_planner(1).py` allegato alla conversazione precedente. L'allegato contiene la classe PosePlanner completa, con i tre client, i target conservati, i controlli dei sette giunti, FK, confronto entro 5 mm e callback di validita. Le correzioni di 32.6 risultano presenti. Il flusso termina al log di `endpoint_verified`: non contiene ancora ActionClient, invio ExecuteTrajectory o verifica della posa raggiunta.

Il punto da estendere e il ramo positivo di `on_endpoint_validity_response`, dopo il calcolo di `endpoint_verified`. `on_plan_response` continua a chiamare soltanto `request_endpoint_fk`. I risultati di piano/FK/validita gia documentati restano completati: non e assegnata una nuova campagna di quelle prove o della fase 5. Durante la nuova prova di esecuzione i controlli esistenti restano prerequisiti automatici.

Il riferimento per l'action e MotionCommander documentato in 7.6 e aggiornato nelle sezioni 14-15; non e stato letto un nuovo file Ubuntu del commander. La ricezione degli stati verra ripresa da JointMonitor/MotionCommander nel blocco successivo. L'assistente modifica solo questa guida; Matteo scrive tutto il codice Python.

### 33.2 API prima dell'implementazione

| Simbolo o API | Significato nel blocco |
|---|---|
| `ActionClient`, da `rclpy.action` | Client conservato come attributo del nodo; riceve nodo, tipo ExecuteTrajectory e nome `/execute_trajectory` |
| `ExecuteTrajectory`, da `moveit_msgs.action` | Tipo dell'action; `Goal()` costruisce il messaggio con la traiettoria |
| `GoalStatus`, da `action_msgs.msg` | Costanti degli stati ROS dell'action |
| `server_is_ready()` | Booleano immediato di disponibilita del server |
| `send_goal_async(goal, feedback_callback=...)` | Invia il goal; il Future riguarda accettazione o rifiuto |
| `goal_handle.accepted` | Indica accettazione, senza certificare il movimento completato |
| `goal_handle.get_result_async()` | Richiede il risultato del goal accettato; restituisce un secondo Future |
| `feedback_msg.feedback.state` | Stringa di stato del server, non posa raggiunta o percentuale |
| `response.status` | Stato ROS nel contenitore restituito dal Future del risultato |
| `response.result.error_code.val` | Codice MoveIt nel risultato interno |

Il goal riceve l'intero RobotTrajectory gia conservato in `planned_trajectory`, inclusi i tempi: non ricostruire una traiettoria dal solo punto finale. Lasciare `controller_names` vuoto, come nella prova normale del commander. Il successo richiede contemporaneamente `GoalStatus.STATUS_SUCCEEDED` e `MoveItErrorCodes.SUCCESS`. Riprendere `describe_moveit_error` per stampare nome e numero del codice insieme allo stato ROS.

PosePlanner riceve TF durante lo spin: mantenere i controlli periodici non bloccanti. Le attese nel costruttore del vecchio commander non vanno trasferite. Anche l'attesa del risultato deve usare la versione asincrona, lasciando libere le callback.

Fonti ufficiali consultate per questa consegna: [ExecuteTrajectory.action](https://github.com/moveit/moveit_msgs/blob/ros2/action/ExecuteTrajectory.action), [ActionClient Jazzy](https://github.com/ros2/rclpy/blob/jazzy/rclpy/rclpy/action/client.py), [GoalStatus Jazzy](https://github.com/ros2/rcl_interfaces/blob/jazzy/action_msgs/msg/GoalStatus.msg), [server ExecuteTrajectory 2.12.4](https://github.com/moveit/moveit2/blob/2.12.4/moveit_ros/move_group/src/default_capabilities/execute_trajectory_action_capability.cpp). I messaggi MoveIt sono consultati sul ramo ros2, rclpy sul ramo jazzy e il server sul tag 2.12.4 gia registrato nel progetto.

### 33.3 Preparazione da scrivere nel nodo

**Da implementare da Matteo.** Aggiungere i tre import indicati in 33.2. Nel costruttore, prima della creazione del timer di pianificazione:

- creare `self.execute_client` per ExecuteTrajectory su `/execute_trajectory`;
- inizializzare `self.execute_goal_future`, `self.execute_goal_handle` e `self.execute_result_future` a None;
- inizializzare `self.execution_requested` e `self.execution_succeeded` a False.

I tre attributi Future/handle conservano oggetti diversi. `execution_requested` serve a impedire un secondo invio nella stessa operazione; `execution_succeeded` registra solo l'esito dell'action. Nessuno dei due significa posa raggiunta verificata.

In `try_plan`, aggiungere il controllo `execute_client.server_is_ready()` accanto a quelli dei servizi e prima del lookup TF e della richiesta di piano. Se falso, loggare l'attesa e ritornare; il timer esistente riprova. Nessuna modifica ai builder, al target, ai vincoli o al main e necessaria per questo blocco.

### 33.4 Cinque metodi da riprendere da MotionCommander

1. **`build_execution_goal(self)`.** Verificare che endpoint_verified sia True, che planned_trajectory esista e che contenga punti. In caso contrario errore e ritorno None. Altrimenti creare ExecuteTrajectory.Goal, assegnarne trajectory e restituire il goal. Questo metodo costruisce soltanto dati.
2. **`request_execution(self)`.** Ritornare se execution_requested e gia True. Ottenere il goal dal builder e fermarsi se None. Ricontrollare server_is_ready prima dell'invio: se ora falso, segnalare che l'invio non e avvenuto e ritornare. Questo blocco non introduce ripetizioni automatiche. Impostare execution_requested immediatamente prima dell'unico tentativo di send_goal_async; conservare il Future e registrarvi on_execution_goal_response. Passare on_execution_feedback come feedback_callback. Gestire e loggare anche un'eccezione immediata dell'invio, senza ritentare implicitamente.
3. **`on_execution_goal_response(self, future)`.** Recuperare l'handle con try/except. In caso di eccezione o goal rifiutato, errore e ritorno. Soltanto dopo accepted=True conservare l'handle, loggare l'accettazione, chiedere get_result_async e collegare on_execution_result al secondo Future.
4. **`on_execution_feedback(self, feedback_msg)`.** Leggere e loggare feedback_msg.feedback.state come nel commander. La prova non richiede un particolare numero di messaggi di feedback.
5. **`on_execution_result(self, future)`.** Recuperare la risposta con try/except; leggere i due livelli del risultato e stamparli. Impostare execution_succeeded=True soltanto se entrambi i controlli di successo passano. Eccezione o risultato negativo lasciano il flag falso e producono un errore leggibile. Per questo checkpoint il log positivo indica soltanto l'esecuzione completata: la verifica della posa sara aggiunta dopo la revisione.

Collegare `request_execution()` al ramo `if self.endpoint_verified` di `on_endpoint_validity_response`, dopo il log positivo gia presente. Non chiamarlo da on_plan_response o on_fk_response. Lasciare execution_requested=True dopo un tentativo, anche se rifiutato o fallito, per impedire nuovi invii involontari. Non importare nel nuovo nodo il movimento verso ready, il retry di pianificazione, la cancellazione o il confronto articolare del commander.

Sequenza da ottenere: target originale conservato → piano → endpoint verificato → un solo goal → accettazione → risultato. Il controllo del piano resta quello gia funzionante.

### 33.5 Nuova verifica - un'esecuzione nella demo

Demo e scena normale attive, altri nodi che comandano movimenti terminati; lasciare il robot fermo mentre viene prodotto e controllato il piano. Questa versione, appena endpoint_verified e True, inviera automaticamente la traiettoria. Non avviare piu istanze del planner.

In Ubuntu WSL, dopo aver scritto le modifiche:

```bash
source /opt/ros/jazzy/setup.bash
cd /home/matteo/vision_sort_ws
python3 -m py_compile src/vision_sort_lab/vision_sort_lab/pose_planner.py
colcon build --symlink-install --packages-select vision_sort_lab
source install/setup.bash
ros2 run vision_sort_lab pose_planner
```

Eseguire i comandi successivi solo se quello precedente riesce. Attesi: normale controllo endpoint positivo, un solo log di invio, goal accettato e risultato con stato ROS 4 e codice MoveIt SUCCESS (1). Osservare il movimento del robot in RViz. Lasciare il nodo attivo altri tre secondi e controllare che non invii un secondo goal. Un successivo riavvio e una nuova operazione: il target viene costruito dalla nuova posa corrente, ancora con Z aumentata di 0.03 m.

Non sono assegnati test negativi del controllore o della scena gia conclusi. Il nuovo log di successo dell'action non prova ancora il rispetto del goal di posa. Conservare i valori stampati del target; la nuova pianificazione puo avere endpoint, durata e numero di punti diversi dalla precedente.

**Consegna unica:** import e inizializzazioni aggiunti, controllo del server in try_plan, ramo positivo di on_endpoint_validity_response, cinque metodi e log completo fino al risultato. Includere conferma dell'assenza di un secondo invio nei tre secondi successivi. Codice e risultato ancora da ricevere: nessuna esecuzione di posa e dichiarata completata da questo aggiornamento.

### 33.6 Blocco successivo - posa raggiunta su dati aggiornati e timeout

Dopo la revisione e il risultato del blocco 33, spiegare e assegnare insieme implementazione e verifica della posa raggiunta. Riferimenti: ricezione e associazione nome-valore di JointMonitor/MotionCommander; istante e filtro sul campione delle sezioni 11.10-11.14; timer indipendente della sezione 12; FK e vincoli gia studiati in PosePlanner.

Direzione tecnica concordata per il prossimo esercizio:

- soltanto dopo i due esiti positivi dell'action, registrare l'istante di inizio verifica e attivare l'attesa;
- acquisire un nuovo JointState completo per i sette giunti, con stamp sorgente strettamente successivo all'istante registrato; una callback ricevuta dopo il risultato puo ancora contenere un messaggio vecchio;
- conservare separatamente quello stato e il suo stamp; calcolarne la posa con FK e valutarne i vincoli originali con GetStateValidity. Non riusare endpoint_state, che contiene la previsione del piano, e non richiamare le callback endpoint ora collegate all'esecuzione;
- conservare target_pose e target_constraints originali per il confronto. Il timestamp del calcolo FK non sostituisce lo stamp del campione dei giunti;
- mantenere le tolleranze originali: distanza entro 0.005 m e le tre componenti ROTATION_VECTOR entro 0.05 rad, valutate dai vincoli MoveIt. Un singolo limite sull'angolo totale del quaternion non e equivalente;
- usare un controllo periodico ogni 0.1 s con limite di 2.0 s per l'intera verifica dopo il risultato, comprese le risposte dei servizi. Al massimo una catena di verifica in corso; nessun invio ripetuto a ogni callback dei giunti. Disattivare l'attesa dopo un unico esito e ignorare risposte tardive dopo la scadenza;
- definire esplicitamente prima dell'uso la politica per un campione fuori tolleranza e il riferimento temporale. La demo precedente usava use_sim_time=False; quel risultato e storico. Per Gazebo, timer e durata dovranno gestire pause/salti del tempo simulato. Non sottrarre timestamp ROS e tempi monotoni fra loro.

ToolPoseReader rimane il riferimento per leggere TF a scopo di osservazione. `Time()` richiede soltanto l'ultima trasformazione disponibile: non ne garantisce la freschezza. Per la verifica completa si propone il nuovo snapshot dei giunti, cosi da riutilizzare esattamente i vincoli di orientamento gia costruiti. Nella demo la posa deriva dal modello e dagli stati pubblicati, non da un sensore fisico indipendente.

Il precedente endpoint era a 4.899 mm dal centro della sfera di 5 mm: il risultato positivo dell'action puo quindi essere seguito da una verifica di posa negativa. Registrare la discrepanza senza allargare le tolleranze. La pre-presa di piece_red_1 resta successiva a esecuzione e verifica della posa.

**Stato:** ripresa documentata e blocco ExecuteTrajectory assegnato; implementazione, prova dell'action e verifica della posa raggiunta ancora da svolgere da Matteo. Nessun file Python modificato dall'assistente.

### 33.7 Chiarimento didattico - come costruire i metodi prima di scriverli

**28 ottobre 2026:** Matteo chiede una spiegazione piu esplicita del metodo di costruzione di nuove funzioni/classi. La consegna 33.3-33.5 resta attiva; questo chiarimento ne esplicita il progetto. Nessun nuovo codice o risultato di esecuzione ricevuto.

#### Quali classi e quali oggetti servono

In questo esercizio si estende la classe PosePlanner gia scritta. I cinque metodi vanno nel corpo di quella classe, allo stesso livello di try_plan e on_plan_response; non dentro __init__ o dentro un'altra callback. MotionCommander e il riferimento da leggere: non occorre crearne un'istanza, avviarlo o usarlo come classe base.

ActionClient e una classe fornita da rclpy: si importa e se ne crea un oggetto nel costruttore. Il suo costruttore riceve, nell'ordine, il nodo corrente, il tipo ExecuteTrajectory e il nome dell'action. L'attributo execute_client conserva quell'oggetto per usarlo nelle callback successive. ExecuteTrajectory.Goal e la classe del messaggio da istanziare nel builder. GoalStatus fornisce le costanti da usare nel confronto; non occorre costruirne un oggetto in questo blocco.

Lo schema gia usato in PosePlanner e lo stesso: il client GetMotionPlan e conservato nel nodo, mentre il messaggio della singola richiesta e costruito quando serve. Un client e riutilizzabile; un goal rappresenta i dati di una singola richiesta di esecuzione.

`self` identifica l'istanza corrente di PosePlanner. Quando un metodo e chiamato attraverso l'istanza, Python passa self automaticamente. Gli attributi con self conservano dati fra callback; i nomi locali, come goal, goal_handle e response, sono definiti nel singolo metodo. Il nome scelto per una variabile locale non crea un campo ROS: i campi trajectory, accepted, status ed error_code vengono invece dalle interfacce.

#### Schema da applicare a ogni nuovo metodo

Prima del corpo Python rispondere a queste domande, in questo ordine:

1. Quale singola responsabilita ha il metodo?
2. Chi lo chiama e quando? Quali argomenti gli passa?
3. Quali dati gia disponibili deve leggere?
4. Quali condizioni impediscono di proseguire? Quali controlli devono venire prima degli accessi ai dati?
5. Che cosa costruisce, restituisce o modifica nel nodo?
6. Quale passaggio avvia dopo di se e con quale risultato osservabile?

Una funzione che costruisce dati deve restituirli al chiamante. Un metodo che avvia un'operazione asincrona conserva il Future e registra chi elaborera la risposta. Una callback elabora l'evento ricevuto e decide se il flusso puo proseguire. Questa distinzione determina i corpi dei nostri cinque metodi.

#### Contratto dei cinque metodi

| Metodo | Chi lo chiama / argomenti | Legge | Produce o modifica |
|---|---|---|---|
| build_execution_goal(self) | request_execution, senza argomenti espliciti | endpoint_verified e planned_trajectory | Restituisce un Goal pronto oppure None; nessun invio |
| request_execution(self) | Ramo endpoint positivo, senza argomenti espliciti | execution_requested, builder e disponibilita client | Marca il tentativo, invia, conserva execute_goal_future, registra le callback |
| on_execution_goal_response(self, future) | rclpy al completamento del Future dell'invio | Il risultato del Future: goal handle | Se accettato conserva handle e Future del risultato, registra on_execution_result |
| on_execution_feedback(self, feedback_msg) | rclpy alla ricezione del feedback | feedback_msg.feedback.state | Log dello stato, senza modificare l'esito |
| on_execution_result(self, future) | rclpy al completamento del Future del risultato | status ROS e risultato MoveIt | Log finale; execution_succeeded vero soltanto con entrambi gli esiti positivi |

I due parametri chiamati future appartengono a metodi differenti e contengono risultati diversi. Il primo produce un handle; il secondo produce un contenitore con status e result. Il nome locale uguale non rende uguale il contenuto.

#### Costruire build_execution_goal passo per passo

Responsabilita: trasformare la traiettoria gia verificata nel messaggio richiesto dall'action. La firma riceve solo self perche i dati sono gia negli attributi del nodo.

1. Controllare endpoint_verified. Se falso, loggare il motivo e uscire restituendo None.
2. Controllare che planned_trajectory non sia None. Questo controllo deve precedere l'accesso a joint_trajectory: un oggetto assente non ha quel campo.
3. Controllare che joint_trajectory.points contenga elementi. Il riferimento e la traiettoria completa conservata nel nodo.
4. Creare una variabile locale goal contenente una nuova istanza di ExecuteTrajectory.Goal. La chiamata alla classe costruisce il messaggio e rende disponibili i suoi campi.
5. Nel campo trajectory del messaggio mettere planned_trajectory. Non estrarre solo l'ultimo punto e non ricostruire il target.
6. Restituire goal: request_execution ricevera quell'oggetto e potra inviarlo.

I tre controlli sono uscite anticipate. La costruzione finale si raggiunge solo se tutti sono passati. Il builder non deve alterare execution_requested, chiedere un piano, inviare il goal o registrare callback. Per questo e possibile capire dal suo valore restituito se la preparazione e riuscita.

#### Costruire request_execution e collegare le callback

Responsabilita: effettuare un solo tentativo di invio del goal pronto. Seguire l'ordine: guardia contro il duplicato, chiamata al builder, controllo del valore restituito, controllo del server, attivazione del flag, invio asincrono, conservazione Future e registrazione callback. Il valore del builder e locale; il Future e conservato con self perche rappresenta un'operazione in corso.

In send_goal_async si passano il goal e il riferimento al metodo on_execution_feedback come feedback_callback. Sul Future restituito si usa add_done_callback con il riferimento a on_execution_goal_response. Si passa il metodo senza parentesi: verra chiamato da rclpy, che fornira l'argomento. Scrivere le parentesi provocherebbe invece una chiamata immediata, prima che sia disponibile la risposta, e mancherebbe l'argomento atteso.

`future.result()` dentro una callback registrata con add_done_callback legge un Future gia completato. Il try/except serve a gestire il caso in cui il Future contenga un'eccezione. Questo e lo schema gia usato in on_plan_response; cambia il tipo di oggetto contenuto.

In on_execution_goal_response, il percorso positivo e: ottenere goal_handle, controllare accepted, conservare l'handle nel nodo, chiamare get_result_async su quell'handle, conservare execute_result_future e registrarvi on_execution_result. La richiesta del risultato riguarda lo stesso goal e non invia un secondo movimento. Un rifiuto o un'eccezione devono terminare la callback prima di questo percorso.

In on_execution_result, recuperare il contenitore response dal Future. Da response leggere status; dal suo campo result leggere error_code.val. Usare un solo ramo positivo che richieda entrambi i successi con and. Il ramo negativo riporta lo stato ROS e il codice MoveIt descritto dalla funzione esistente. L'attivazione della verifica della posa sara aggiunta soltanto nel ramo positivo al prossimo checkpoint.

I nomi on_execution_goal_response e on_execution_result sono nomi scelti nel progetto: ROS non li riconosce automaticamente. A renderli callback sono i collegamenti espliciti appena descritti. Analogamente, request_execution viene eseguito soltanto perche lo chiamiamo dal ramo positivo di on_endpoint_validity_response.

#### Ordine di scrittura e verifica del blocco

Scrivere prima import e attributi, poi builder, callback del risultato, callback del feedback, callback dell'accettazione e infine request_execution. Questo ordine aiuta a progettare ogni passaggio avendo gia definito quello che richiamera; non e un requisito sull'ordine dei metodi nel file. Tenere on_endpoint_validity_response come ultimo collegamento da aggiungere al flusso.

Dopo avere completato tutte le parti, usare la verifica unica di 33.5 e consegnare codice e log insieme. Per la revisione seguire il flusso operativo: endpoint positivo → request_execution → build_execution_goal → Future dell'invio → callback accettazione → Future del risultato → callback risultato. Il feedback puo arrivare nel frattempo. Il criterio rimane un solo invio e un risultato dell'action correttamente interpretato. Nessun corpo Python scritto dall'assistente.

## 34. Consegna aggiornata - costruire MotionExecution in un nuovo file

### 34.1 Decisione e motivazione

**28 ottobre 2026:** Matteo preferisce costruire le funzionalita nuove in un nuovo file quando questo rende il codice piu chiaro. La separazione dell'esecuzione e sensata: PosePlanner ha gia TF, target, pianificazione e tre passaggi di verifica dell'endpoint. L'action aggiunge un insieme autonomo di dati persistenti: client, Future dell'invio, goal handle, Future del risultato e callback. Questo insieme giustifica una classe di supporto con una responsabilita precisa.

Nuovo file da creare personalmente in Ubuntu: `/home/matteo/vision_sort_ws/src/vision_sort_lab/vision_sort_lab/motion_execution.py`, classe MotionExecution. E una normale classe Python, senza ereditarieta da Node. PosePlanner rimane l'unico nodo ROS ed e il coordinatore dell'operazione. Il nome riprende la proposta storica di 17.2-17.3, mai confermata come realizzata: quella proposta era stata annullata per MotionCommander in 17.4. La richiesta attuale introduce una nuova decisione per PosePlanner; non richiede modifiche al commander.

Non basta trasferire funzioni in un file facendo leggere a tutte l'intero stato del planner. Il componente riceve la traiettoria come argomento e restituisce un esito mediante callback. Il nodo ricevuto nel costruttore serve a creare il client e usare il logger, non a leggere target_pose, endpoint_verified o planned_trajectory. Se Matteo ha gia iniziato i metodi della consegna precedente, riusarli spostandoli e adattandone ingressi e attributi.

### 34.2 Confine fra i due componenti

| PosePlanner conserva | MotionExecution possiede |
|---|---|
| Node, TF e timer di pianificazione | ActionClient ExecuteTrajectory |
| Target originale, vincoli e traiettoria del piano | Preparazione del messaggio Goal dalla traiettoria ricevuta |
| Client del piano, FK e validita endpoint gia funzionanti | Future dell'invio, goal handle e Future del risultato |
| Decisione di eseguire soltanto dopo endpoint_verified | Invio, accettazione/rifiuto, feedback e risultato dell'action |
| Ricezione dell'esito e futuro avvio della verifica della posa raggiunta | Log dettagliati dell'action e interpretazione congiunta di stato ROS e codice MoveIt |
| Esito complessivo del compito | Guardia contro un secondo tentativo e notifica unica dell'esito |

Per questo blocco il componente ammette un solo tentativo d'invio nella sua vita, coerentemente con la singola operazione del nodo attuale. Il flag execution_requested appartiene al componente e non va duplicato nel planner. Un futuro uso in sequenze di movimenti richiedera una politica esplicita di riarmo, da introdurre quando servira. Nessun reset o nuovo invio automatico ora.

### 34.3 Costruzione della nuova classe e composizione

La firma del costruttore e `__init__(self, node, result_callback)`. Non si chiama super().__init__ di Node perche questa classe non e un nodo.

- self e l'oggetto MotionExecution che si sta costruendo.
- node e il nodo ROS gia esistente, cioe l'istanza PosePlanner che crea il componente.
- result_callback e un metodo del planner passato senza parentesi; il componente lo conserva e lo richiamera al completamento dell'action.

Conservare node in `self.node` e result_callback in `self.result_callback`. Creare `self.execute_client` passando ad ActionClient, nell'ordine, il nodo ricevuto, il tipo ExecuteTrajectory e `/execute_trajectory`. Per il logger usare `self.node.get_logger()`: MotionExecution non eredita get_logger.

Inizializzare nel componente execute_goal_future, execute_goal_handle ed execute_result_future a None; execution_requested e completion_reported a False. I primi tre conservano l'operazione asincrona; il primo flag protegge dal secondo tentativo, il secondo dalla seconda notifica terminale. In PosePlanner resta soltanto execution_succeeded, inizialmente falso, come esito ricevuto dall'esterno.

Import necessari nel nuovo modulo: ActionClient da rclpy.action, ExecuteTrajectory da moveit_msgs.action, GoalStatus da action_msgs.msg, MoveItErrorCodes da moveit_msgs.msg e describe_moveit_error dal modulo gia costruito. Nel planner si importa MotionExecution dal nuovo modulo. Gli import dell'action appartengono al nuovo file.

### 34.4 Interfaccia esplicita e significato dei risultati

| Metodo | Ingresso | Uscita / effetto |
|---|---|---|
| is_ready(self) | Nessun argomento oltre self | Booleano di server_is_ready, senza attese |
| build_execution_goal(self, trajectory) | RobotTrajectory ricevuto dal planner | Goal pronto oppure None se dati assenti/vuoti |
| request_execution(self, trajectory) | RobotTrajectory ricevuto dal planner | True se send_goal_async ha restituito il Future dell'invio; False se il percorso si interrompe prima. Non e l'esito del movimento |
| on_execution_goal_response(self, future) | Future dell'invio | Handle accettato e attesa del risultato, oppure esito negativo |
| on_execution_feedback(self, feedback_msg) | Feedback dell'action | Log di feedback_msg.feedback.state |
| on_execution_result(self, future) | Future del risultato finale | Interpretazione di status ROS e codice MoveIt, quindi notifica dell'esito |
| _finish(self, succeeded) | Booleano terminale calcolato dal componente | Invoca result_callback una sola volta |
| destroy(self) | Nessun argomento oltre self | Distrugge l'ActionClient prima della chiusura del nodo |

I due canali hanno tempi diversi. Il booleano immediato di request_execution dice soltanto se e partita la richiesta asincrona. La callback successiva comunica l'esito dell'action: True solo con STATUS_SUCCEEDED e MoveIt SUCCESS; False con rifiuto, eccezione del Future o risultato finale negativo.

Se non e stato ottenuto un Future dell'invio, request_execution restituisce False e logga il motivo, senza una notifica di completamento. Una chiamata duplicata restituisce False e non genera una seconda notifica. Questo evita di comunicare due fallimenti per la stessa interruzione. Dopo il tentativo d'invio, execution_requested resta True anche se l'invio solleva subito un'eccezione: nessuna ripetizione implicita.

La callback esterna sara `on_execution_finished(self, succeeded)` in PosePlanner. Non e una nuova API ROS: e un normale metodo Python chiamato dal componente, con un booleano. Il Future e l'handle rimangono interni a MotionExecution.

### 34.5 Ragionamento e ordine dei corpi da scrivere

**Traccia operativa ampliata il 28 ottobre 2026, su richiesta di Matteo: iniziare la scrittura di tutti i metodi con passaggi espliciti.** Tutte le firme sotto appartengono alla classe MotionExecution. Il corpo di ciascun metodo va indentato rispetto al def; ogni def e allo stesso livello del costruttore. Matteo scrive il codice: questa e una traccia ordinata, non un listato implementato dall'assistente.

Prima dei metodi: scrivere gli import di 34.3, poi dichiarare la classe MotionExecution senza la base Node. Nel modulo non servono main, init ROS o spin. Gli oggetti necessari saranno creati quando PosePlanner istanziera la classe. Usare i nomi di attributo indicati qui per poter confrontare la consegna senza ambiguita.

**0. Costruttore: `__init__(self, node, result_callback)`.**

1. Conservare i due argomenti negli attributi self.node e self.result_callback. Il callback deve essere conservato come oggetto richiamabile: non eseguirlo qui.
2. Creare self.execute_client usando ActionClient con node, ExecuteTrajectory e il nome `/execute_trajectory`.
3. Inizializzare self.execute_goal_future, self.execute_goal_handle e self.execute_result_future a None: nessuna operazione e ancora stata avviata.
4. Inizializzare self.execution_requested e self.completion_reported a False.
5. Terminare il costruttore senza attese, richieste o notifiche. Non assegnare una traiettoria e non accedere ai dati del planner.

Il client usa il nodo ricevuto. Dentro la nuova classe self identifica MotionExecution: il riferimento al nodo ROS e self.node, distinto da self.

**1. Disponibilita: `is_ready(self)`.**

1. Chiamare server_is_ready sul proprio execute_client: produce subito True o False.
2. Restituire quel booleano al chiamante. Una chiamata senza return farebbe restituire None al metodo, perdendo il risultato.

Il metodo non modifica attributi, non stampa a ogni interrogazione e non avvia il movimento. Il log periodico dell'attesa rimane nel try_plan del planner.

**2. Costruzione del messaggio: `build_execution_goal(self, trajectory)`.**

1. Se trajectory e None, loggare l'assenza di traiettoria attraverso self.node.get_logger() e restituire None.
2. Dopo il primo controllo, verificare trajectory.joint_trajectory.points. Se la sequenza e vuota, loggare l'errore e restituire None. L'ordine evita di accedere ai campi di un oggetto assente.
3. Creare una variabile locale goal contenente un nuovo ExecuteTrajectory.Goal.
4. Assegnare l'argomento trajectory al campo trajectory dell'oggetto goal, conservando tutti i punti e i tempi. Il primo e un parametro Python; il secondo e un campo del messaggio ROS.
5. Lasciare controller_names al valore predefinito vuoto e restituire goal.

Il planner ha gia deciso se l'endpoint e verificato: non leggere endpoint_verified o planned_trajectory dal nodo. Il builder non modifica i flag dell'action e non invia il messaggio.

**3. Notifica unica: `_finish(self, succeeded)`.**

1. Se self.completion_reported e gia True, terminare subito con un semplice return.
2. Altrimenti impostare self.completion_reported a True prima di chiamare codice esterno.
3. Richiamare self.result_callback passando succeeded come unico argomento esplicito.

Il callback conservato e gia associato all'istanza PosePlanner: Python gestisce il suo self. Non passare manualmente il planner come argomento aggiuntivo. Il metodo non restituisce un esito da interpretare: lo consegna al callback. Il prefisso underscore indica per convenzione un metodo interno. Nessun altro metodo deve chiamare direttamente result_callback.

**4. Risultato finale: `on_execution_result(self, future)`.**

1. In un try limitato al recupero, ottenere response da future.result(). Il Future e gia completato quando questa callback viene invocata.
2. Nell'except conservare il nome dell'eccezione, loggarlo, chiamare _finish con False e terminare con return. Il percorso normale deve rimanere fuori dall'except.
3. Dopo il try/except leggere status da response.status ed error_code da response.result.error_code.val. response e un contenitore: il campo result contiene il risultato specifico di MoveIt.
4. Ottenere error_name tramite describe_moveit_error(error_code), la funzione gia scritta.
5. Calcolare il booleano locale succeeded con due confronti collegati da and: status uguale a GoalStatus.STATUS_SUCCEEDED ed error_code uguale a MoveItErrorCodes.SUCCESS.
6. Stampare stato ROS, nome e numero del codice; livello info se succeeded e vero, error altrimenti.
7. Dopo il log chiamare _finish con succeeded, una sola volta per questo percorso.

Tenere il try stretto: un errore nel metodo del planner richiamato da _finish non deve essere descritto come un errore nel recupero del Future. Non richiamare direttamente result_callback e non iniziare qui la verifica della posa.

**5. Feedback: `on_execution_feedback(self, feedback_msg)`.**

1. Leggere la stringa feedback_msg.feedback.state e conservarla, se utile, in una variabile locale state.
2. Loggarla tramite il logger del nodo, indicando che e uno stato dell'esecuzione.

Questa callback riceve un messaggio, non un Future: niente future.result(). Non modificare execution_requested o completion_reported e non chiamare _finish. Un messaggio di feedback non conclude il goal.

**6. Accettazione: `on_execution_goal_response(self, future)`.**

1. Recuperare il goal_handle da future.result() dentro un try limitato a quella lettura.
2. Nell'except: log con exc, _finish(False) e return.
3. Controllare goal_handle.accepted. Se falso: log di rifiuto, _finish(False) e return. Non chiedere il risultato di un goal rifiutato.
4. Conservare l'handle accettato in self.execute_goal_handle e loggare l'accettazione.
5. In un secondo try chiedere get_result_async sull'handle e conservarne il valore in self.execute_result_future.
6. Nell'except di questa seconda operazione: log dell'impossibilita di richiedere il risultato, _finish(False) e return. Questo errore non dimostra l'arresto del robot.
7. Dopo il secondo try collegare on_execution_result al Future appena conservato, con add_done_callback. Passare il riferimento self.on_execution_result senza parentesi.

Il primo Future produce un handle; il secondo produrra il contenitore status/result. Chiedere il risultato riguarda lo stesso goal, non un nuovo invio. Un risultato non ottenuto e un esito non confermato dal componente, distinto dalla certezza che il robot sia fermo.

**7. Invio: `request_execution(self, trajectory)`.**

1. Se self.execution_requested e gia True, segnalare il tentativo duplicato e restituire False. Non chiamare _finish: la prima operazione conserva il proprio percorso di risultato.
2. Chiamare il proprio build_execution_goal con trajectory e conservare localmente il valore restituito in goal.
3. Se goal e None, restituire False: il builder ha gia loggato la causa.
4. Controllare il proprio is_ready. Se falso, loggare che il server non e disponibile e restituire False. Nessuna attesa dentro questo metodo.
5. Impostare self.execution_requested a True, immediatamente prima del tentativo di invio. Dopo questo punto il flag non viene ripristinato neppure in caso di eccezione.
6. In un try chiamare send_goal_async sul client, passando goal e il riferimento self.on_execution_feedback come feedback_callback. Conservare il Future in self.execute_goal_future.
7. Se l'invio solleva subito un'eccezione, loggarla e restituire False. Qui non esiste un Future di cui attendere il completamento e non si chiama _finish.
8. Dopo il try collegare self.on_execution_goal_response al Future tramite add_done_callback. Passare il metodo senza parentesi.
9. Loggare che il goal e stato inviato e restituire True.

False significa che questa chiamata non ha avviato un nuovo invio asincrono; True significa Future dell'invio ottenuto e callback collegata. Non usare il valore immediato per dichiarare il movimento riuscito. Gli errori asincroni passano invece da _finish e dalla callback esterna. Tenere le registrazioni delle callback fuori dal try dell'invio per non attribuire eventuali errori del codice richiamato al tentativo di invio.

**8. Chiusura: `destroy(self)`.**

1. Chiamare destroy sull'ActionClient conservato in self.execute_client.
2. Lasciare la distruzione del nodo al chiamante.

L'API del client ne libera le risorse e lo rimuove dal nodo. Usarla una volta nella chiusura. Non distruggere qui self.node e non chiamare rclpy.try_shutdown dal componente.

Questo e un ordine didattico di scrittura, non un vincolo sull'ordine dei metodi nel file. Il codice dei callback puo riprendere MotionCommander, adattando logger, attributi e notifica al nuovo proprietario dello stato. Usare _finish per tutti e soli gli esiti asincroni, is_ready per la disponibilita e build_execution_goal per preparare il messaggio: ogni metodo ha un ruolo riconoscibile.

### 34.6 Piccole integrazioni in PosePlanner

1. Aggiungere al planner l'import di MotionExecution dal modulo vision_sort_lab.motion_execution. Nel costruttore, prima del timer, inizializzare self.execution_succeeded a False. Poi costruire MotionExecution e conservarlo in self.motion_execution: il primo argomento e self, il secondo e self.on_execution_finished senza parentesi. La firma del metodo puo essere definita piu in basso nel file: Python ha gia creato la classe quando il costruttore viene eseguito.
2. In try_plan, prima del lookup TF, controllare `self.motion_execution.is_ready()`. Se falso loggare l'attesa e ritornare, lasciando riprovare il timer. Non creare un secondo ActionClient nel planner.
3. Nel ramo endpoint positivo di on_endpoint_validity_response, dopo il log positivo gia presente, chiamare request_execution sul componente con self.planned_trajectory. Conservare il booleano immediato in una variabile locale submitted; se falso segnalare che questo passaggio non ha avviato un nuovo invio. Non chiamare manualmente on_execution_finished con submitted: sono due informazioni diverse. Il gate endpoint_verified resta qui.
4. Scrivere `on_execution_finished(self, succeeded)` come nuovo metodo del planner, allo stesso livello degli altri. Riceve il booleano passato da MotionExecution. Prima salvarlo in self.execution_succeeded; poi usare un if sul booleano per loggare esito ricevuto positivo o negativo. Non usare future.result(), response o goal_handle: non sono argomenti di questo metodo. Solo nel ramo succeeded=True verra aggiunto in seguito l'avvio della verifica della posa. Per ora il log dice che l'esito positivo dell'action e arrivato al planner, senza dichiarare posa raggiunta verificata.
5. Nel finally di main, dentro il controllo gia presente che pose_planner non sia None, chiamare destroy sul suo attributo motion_execution prima della chiamata gia presente a destroy_node; conservare rclpy.try_shutdown. Il componente usa ancora il nodo per liberare il client, per questo l'ordine e importante.

Non occorrono un nuovo main, rclpy.init, spin, entry point o processo per motion_execution.py. Il modulo viene importato dal nodo gia avviabile con ros2 run. Le cinque callback/metodi dell'action proposti in 33 non vanno aggiunti al planner. Target, builder di posa, FK e validita endpoint conservano il flusso gia funzionante.

### 34.7 Implementazione e verifica da consegnare insieme

Scrivere il nuovo file e completare le piccole integrazioni nel planner come un unico blocco. Prima dell'avvio controllare a lettura che il nuovo modulo non acceda agli attributi del piano/endpoint del nodo e che PosePlanner non gestisca i Future dell'action. Questi sono i due confini che rendono utile la separazione.

Demo e scena normale attive, altri nodi che comandano movimenti terminati. Il lancio inviera automaticamente il piano dopo la verifica endpoint positiva. In Ubuntu WSL:

```bash
source /opt/ros/jazzy/setup.bash
cd /home/matteo/vision_sort_ws
python3 -m py_compile src/vision_sort_lab/vision_sort_lab/motion_execution.py src/vision_sort_lab/vision_sort_lab/pose_planner.py
colcon build --symlink-install --packages-select vision_sort_lab
source install/setup.bash
ros2 run vision_sort_lab pose_planner
```

Proseguire solo se il comando precedente riesce. Attesi: normale controllo endpoint positivo, un solo invio, goal accettato, risultato ROS 4 e MoveIt SUCCESS (1), ricezione di succeeded=True nel planner. Lasciare il nodo attivo altri tre secondi: nessun secondo invio o seconda notifica terminale. La disponibilita del feedback non impone un particolare numero di messaggi. Terminare con Ctrl+C e osservare la chiusura senza traceback.

Consegna unica: nuovo modulo completo, parti modificate di PosePlanner/main, esito della build e log completo dell'esecuzione, inclusa conferma dei tre secondi senza duplicazioni. Nessuna ripetizione delle prove della fase 5 o della campagna di piano/FK/validita endpoint. Quei controlli continuano a comparire come prerequisiti automatici della nuova esecuzione.

### 34.8 Stato e passo successivo

Confermata soltanto la decisione documentale e assegnata l'implementazione nel nuovo file: nessun nuovo codice o log ricevuto. L'assistente ha aggiornato la guida e non ha creato o modificato file Python.

Dopo il checkpoint dell'action, valutare un secondo componente dedicato alla verifica della posa raggiunta: nuovo campione JointState, FK, vincoli originali e timeout complessivo secondo 33.6. Il nuovo componente si avviera dal ramo positivo di on_execution_finished. Non caricare MotionExecution delle verifiche di posa e non riscrivere ora l'endpoint gia verificato.

Le API dell'action e del client restano quelle documentate in 33.2; la nuova separazione e una scelta di organizzazione del codice, non un nuovo protocollo ROS. Riferimenti: [ActionClient Jazzy, incluse le API di distruzione](https://github.com/ros2/rclpy/blob/jazzy/rclpy/rclpy/action/client.py), [ExecuteTrajectory](https://github.com/moveit/moveit_msgs/blob/ros2/action/ExecuteTrajectory.action).

### 34.9 Checkpoint didattico - avvio della scrittura guidata

**28 ottobre 2026:** Matteo conferma che la spiegazione della separazione e chiara e chiede di iniziare, con una guida piu esplicita alla scrittura di tutte le funzioni. Ampliata 34.5 con firma, dati, ordine delle istruzioni, condizioni di uscita e delimitazione dei try/except per ciascun metodo; precisati nomi e integrazione nel planner in 34.3 e 34.6. La consegna e un unico blocco nuovo modulo + integrazione + verifica di 34.7, con revisione alla fine. Nessun codice scritto dall'assistente e nessun nuovo file o risultato di esecuzione ancora ricevuto dall'utente. Il checkpoint 32.7 resta concluso.

### 34.10 Primo avvio - TypeError nel costruttore di MotionExecution

**31 ottobre 2026:** Matteo invia il traceback di `ros2 run vision_sort_lab pose_planner`. L'entry point carica PosePlanner e il suo costruttore arriva alla creazione di MotionExecution. Nel modulo motion_execution.py, riga 13 del file eseguito, compare `super().__init__('motion_execution')`; Python solleva `TypeError: object.__init__() takes exactly one argument (the instance to initialize)`.

Il traceback dimostra che il modulo viene trovato e il componente viene istanziato; l'avvio si interrompe durante il suo costruttore. Non documenta ancora l'invio dell'action o un risultato di esecuzione. I nuovi listati completi non sono stati allegati e non sono stati letti dall'assistente.

Diagnosi: la chiamata super con il nome del nodo appartiene allo schema usato nelle classi che ereditano da Node, come PosePlanner o MotionCommander. MotionExecution e invece una normale classe Python, che riceve un nodo gia esistente. Nella gerarchia indicata dall'errore, il costruttore raggiunto e object.__init__, che non accetta il nome passato come argomento aggiuntivo.

Correzione da applicare personalmente nel sorgente `/home/matteo/vision_sort_ws/src/vision_sort_lab/vision_sort_lab/motion_execution.py`: rimuovere la riga `super().__init__('motion_execution')`. Conservare la classe senza base Node e il costruttore con self, node e result_callback; conservare self.node, self.result_callback e il client costruito usando il nodo ricevuto. Non modificare i file generati in build o install anche se il traceback li cita.

Proseguire in Ubuntu, un comando alla volta e solo se il precedente riesce:

```bash
cd /home/matteo/vision_sort_ws
python3 -m py_compile src/vision_sort_lab/vision_sort_lab/motion_execution.py
colcon build --symlink-install --packages-select vision_sort_lab
source install/setup.bash
ros2 run vision_sort_lab pose_planner
```

La verifica decisiva e il nuovo avvio: py_compile da solo non rileva questa incompatibilita del costruttore. Demo e scena normale devono restare attive come previsto dalla consegna, perche dopo la correzione il nodo potra proseguire verso l'esecuzione automatica. Inviare il nuovo log completo o l'eventuale prossimo traceback. Non attribuire alla correzione un esito positivo prima di riceverlo. Aggiornata soltanto la guida; nessun sorgente Python modificato dall'assistente.

### 34.11 Avvio successivo - argomenti mancanti di ActionClient

**31 ottobre 2026:** Matteo invia il log della build riuscita di vision_sort_lab (un pacchetto completato) e un nuovo traceback. L'ultimo avvio non si ferma piu sulla chiamata super documentata in 34.10: raggiunge la riga 15 del costruttore di MotionExecution, dove compare `self.execute_client = ActionClient()`. Python segnala i tre argomenti posizionali obbligatori mancanti: node, action_type e action_name. Un messaggio successivo ripropone lo stesso nuovo errore; non e un ulteriore risultato di esecuzione dell'action.

La classe ActionClient deve sapere quale nodo ROS la utilizza, quale tipo di action gestisce e quale nome contattare. Nel nostro costruttore il nodo e gia disponibile nel parametro node. Correzione puntuale da applicare personalmente nel sorgente motion_execution.py:

```python
self.execute_client = ActionClient(
    node,
    ExecuteTrajectory,
    '/execute_trajectory',
)
```

Questo frammento chiarisce la singola chiamata alla libreria, senza sostituire l'implementazione della classe scritta da Matteo. Il primo argomento e il nodo ricevuto, non il self di MotionExecution, che e una normale classe Python. Se self.node e gia stato inizializzato dal parametro node, anche quel riferimento identifica lo stesso nodo; mantenere comunque l'attributo per il logger e gli altri metodi. ExecuteTrajectory e il tipo importato da moveit_msgs.action, senza istanziarlo in questa chiamata. Il terzo argomento e il nome dell'action gia usata nel commander.

Modificare il file sotto src, poi ripetere build, caricamento install/setup.bash e avvio di pose_planner come in 34.10, con demo e scena normale attive. La build riuscita gia osservata non dimostra la correttezza delle chiamate eseguite nel costruttore. Richiesti il nuovo log e il costruttore completo di MotionExecution per controllarne insieme le inizializzazioni. L'esecuzione della traiettoria e la verifica della posa raggiunta restano da confermare. Aggiornata soltanto la guida; nessun file Python modificato dall'assistente.

### 34.12 Endpoint positivo e due NameError nei riferimenti agli oggetti

**31 ottobre 2026:** ricevuto un nuovo log completo fino al traceback. Il nodo entra nello spin e termina positivamente i controlli gia costruiti:

- target panda_hand in panda_link0, posizione (0.3070, -0.0000, 0.6203) m;
- piano SUCCESS, 0.017 s, 9 punti;
- FK posizione (0.3073, -0.0027, 0.6171) m;
- errore dx=0.277, dy=-2.677, dz=-3.124 mm; distanza=4.123 mm, entro 5 mm;
- valid=True, vincoli [True, True], zero contatti ed endpoint_verified=True.

Il nuovo avvio supera quindi i precedenti errori del costruttore. Il traceback mostra il passaggio da on_endpoint_validity_response a self.motion_execution.request_execution(self.planned_trajectory): il collegamento fra planner e componente viene raggiunto. Non e ancora documentato un goal inviato o un risultato dell'action.

**Primo errore:** nella riga 128 del modulo motion_execution.py eseguito compare `goal = build_execution_goal(trajectory)`. Python cerca un nome locale o globale che non trova. Il builder e un metodo della stessa istanza MotionExecution: nella chiamata occorre self. Correzione puntuale da applicare nel sorgente:

```python
goal = self.build_execution_goal(trajectory)
```

Self permette di trovare il metodo sull'oggetto; Python fornisce automaticamente quell'istanza al suo primo parametro. L'unico argomento esplicito rimane trajectory.

**Secondo errore, durante la chiusura:** nel finally del main di pose_planner.py compare `motion_execution.destroy()`. Nel main non esiste una variabile locale motion_execution: il componente e conservato come attributo del nodo pose_planner. Correzione puntuale, dentro il controllo gia previsto che pose_planner non sia None:

```python
pose_planner.motion_execution.destroy()
```

Conservare dopo questa chiamata pose_planner.destroy_node e la chiusura del contesto gia prevista. Il secondo NameError nasce nella pulizia avviata dopo il primo errore; va corretto separatamente. Nel main si parte dalla variabile pose_planner, mentre dentro un metodo della classe si usa self.

Modificare entrambi i sorgenti sotto src, poi completare build, caricamento overlay e nuovo avvio come nel blocco 34.7. Nessuna nuova campagna di prove endpoint o della fase 5 assegnata. Richiesti il nuovo log e anche request_execution e main completi per una revisione congiunta dei riferimenti. Il listato aggiornato completo di MotionExecution non e ancora stato ricevuto. Il log conferma i prerequisiti della nuova esecuzione, non il movimento o la posa raggiunta. Aggiornata soltanto la guida; nessun sorgente Python modificato dall'assistente.

### 34.13 Nome del builder duplicato e distruzione del client sull'istanza

**31 ottobre 2026:** nuovo log con piano SUCCESS (0.016 s, 9 punti), FK a distanza 3.440 mm dal target, valid=True, vincoli [True, True], zero contatti ed endpoint_verified=True. Il flusso raggiunge ancora request_execution ma si ferma prima dell'invio documentato.

Nella riga 128 del modulo eseguito e comparso `goal = self.build_execution_goalbuild_execution_goal(trajectory)`: il nome del metodo e stato concatenato due volte. Il conseguente AttributeError riguarda esattamente quel nome inesistente. Sostituire tutta la riga nel sorgente motion_execution.py con:

```python
goal = self.build_execution_goal(trajectory)
```

La chiamata corretta a pose_planner.motion_execution.destroy nel main viene ora raggiunta: il precedente NameError di quel riferimento non compare. Il nuovo errore di chiusura e interno a MotionExecution.destroy, che contiene `ActionClient.destroy()`. ActionClient e la classe, mentre l'oggetto da distruggere e l'istanza conservata in self.execute_client. Sostituire quella chiamata con:

```python
self.execute_client.destroy()
```

Chiamando il metodo attraverso l'istanza, Python fornisce automaticamente il parametro self al metodo della libreria. La chiamata sulla classe senza alcuna istanza produce invece il TypeError osservato. Questa correzione riguarda il corpo di destroy nel componente; il riferimento pose_planner.motion_execution.destroy nel main rimane quello previsto.

Applicare le due sostituzioni nel file sotto src, poi build, caricamento overlay e nuovo avvio secondo 34.7. Richiesto nuovamente il file motion_execution.py completo insieme al prossimo log per poter rivedere i riferimenti nelle parti non visibili nei traceback. La prova dell'action e la verifica della posa raggiunta restano aperte. Nessuna ripetizione delle prove della fase 5 assegnata. Aggiornata soltanto la guida; nessun file Python modificato dall'assistente.

### 34.14 Future sbagliato nel collegamento della risposta al goal

**31 ottobre 2026:** nuovo log con piano SUCCESS (0.013 s, 8 punti), FK posizione (0.3052, 0.0030, 0.6198) m, dx=-1.793, dy=2.983, dz=-0.472 mm, distanza 3.512 mm. Validita True, due vincoli True, zero contatti ed endpoint_verified=True. L'ultimo traceback raggiunge la riga 152 di request_execution e mostra `self.execute_result_future.add_done_callback(self.on_execution_goal_response)`. execute_result_future e ancora None, per cui il suo accesso ad add_done_callback genera AttributeError. Il precedente errore nel nome del builder non compare e non compare un secondo traceback di pulizia; il sorgente completo non e ancora stato ricevuto.

Il Future del risultato finale viene creato solo dopo il recupero dell'handle accettato, con get_result_async. Per ricevere l'accettazione occorre invece il Future restituito da send_goal_async. Correzione puntuale nel sorgente di request_execution:

```python
self.execute_goal_future.add_done_callback(
    self.on_execution_goal_response
)
```

Verificare nello stesso metodo che il valore restituito da send_goal_async sia effettivamente assegnato a self.execute_goal_future. Mantenere self.execute_result_future inizializzato a None fino al passaggio che chiede il risultato sull'handle accettato.

| Operazione | Future da conservare | Callback da registrarvi |
|---|---|---|
| send_goal_async | execute_goal_future | on_execution_goal_response |
| get_result_async sull'handle accettato | execute_result_future | on_execution_result |

L'errore avviene durante la registrazione della callback: il log non dimostra che la richiesta non sia partita. Se send_goal_async ha gia restituito il primo Future, il server puo aver ricevuto il goal prima del crash. Non dichiarare mancato movimento, accettazione o successo senza i relativi dati; prima di un eventuale nuovo avvio lasciare terminare un movimento gia in corso e mantenere la condizione robot fermo prevista per la pianificazione.

Richiesto il modulo motion_execution.py completo per controllare in un unico passaggio assegnazioni, callback e rami negativi, oltre al traceback. Si puo mostrarlo dal terminale Ubuntu con `cat /home/matteo/vision_sort_ws/src/vision_sort_lab/vision_sort_lab/motion_execution.py`. Nessuna modifica dei sorgenti Python eseguita dall'assistente. La verifica della posa raggiunta resta il blocco successivo all'action; il nuovo log documenta soltanto i prerequisiti positivi e l'errore nel collegamento.

### 34.15 Checkpoint - prima esecuzione di posa riuscita e log da rivedere

**1 novembre 2026:** Matteo invia il primo log che raggiunge il risultato positivo di ExecuteTrajectory dopo le correzioni. L'attesa iniziale del servizio e seguita dal normale tentativo del timer e dalla disponibilita dei servizi. Il nuovo target e conservato per questa operazione:

```text
Target panda_hand in panda_link0:
  pos=(0.3086, -0.0039, 0.6841) m
  q=(0.999111, 0.029469, 0.024673, -0.017340)
Pianificazione riuscita: SUCCESS (1) | tempo=0.013 s | punti=10
Posa FK in panda_link0:
  pos=(0.3041, -0.0057, 0.6848) m
  q=(0.997982, 0.046101, 0.006219, -0.043231)
Errore posizione: dx=-4.483, dy=-1.736, dz=0.660 mm
  distanza=4.852 mm | entro 5 mm=True
Validita dello stato: True | Vincoli: [True, True]
  Numero di contatti: 0 | Verifica endpoint: True
Il goal e stato inviato
Stato dell'esecuzione: MONITOR
Goal accettato
Stato dell'esecuzione: Solution was found and executed.
Esito dell'esecuzione positivo: statusROS = 4 - error = SUCCESS(1)
Esecuzione conclusa con successo
```

**Confermato dal log:** prerequisiti endpoint positivi, invio del goal, accettazione, ricezione del feedback e risultato finale con entrambi gli esiti richiesti. Il messaggio conclusivo e coerente con la notifica positiva prevista verso il planner. L'integrazione dell'action ha ora un primo percorso positivo osservato. Il frammento contiene un solo invio e un solo messaggio conclusivo mostrati, nessun traceback; non documenta autonomamente i tre secondi successivi, la chiusura con Ctrl+C o il sorgente completo aggiornato.

**Anomalia separata da rivedere:** fra il log di invio e il feedback MONITOR compare un log di livello ERROR con lo stesso messaggio endpoint positivo (valid=True, due vincoli True, zero contatti, endpoint_verified=True). La riga compare dopo l'invio e prima del risultato positivo: non e un codice di fallimento dell'action. Il log da solo non permette di stabilire il ramo che l'ha emessa.

Richiesti i metodi aggiornati on_endpoint_validity_response di PosePlanner e request_execution di MotionExecution. Controllare insieme: a quale if e associato ogni else; eventuale log d'errore rimasto fuori dal ramo negativo; valore restituito da request_execution nel percorso in cui l'invio e avviato. Una mancata restituzione esplicita di True produce None, che nel controllo `if not submitted` viene trattato come falso valore e puo attivare un errore ingiustificato. Sono ipotesi di revisione, non una diagnosi accertata sul sorgente non ancora ricevuto.

Per chiudere il checkpoint, verificare sulla stessa istanza l'assenza di un secondo invio/notifica nei tre secondi dopo il risultato e la chiusura con Ctrl+C senza traceback. Non serve riavviare il planner per questa osservazione se e ancora attivo. Dopo la revisione del codice, correggere soltanto il ramo o il ritorno effettivamente errato e completarne la verifica. Nessuna nuova prova della fase 5 assegnata.

**Limite del risultato:** i 4.852 mm si riferiscono alla posa FK prevista dal piano. Non e ancora stato mostrato un campione aggiornato successivo all'action con cui verificare posizione e orientamento raggiunti. L'action riuscita non sostituisce quel confronto. Il blocco successivo resta il nuovo componente di verifica con campione sorgente aggiornato, target/vincoli originali e timeout complessivo (33.6 e 34.8).

Aggiornata soltanto la guida con il checkpoint positivo e le verifiche ancora aperte; nessun file Python modificato dall'assistente.

### 34.16 Revisione dei due metodi - causa del log incoerente individuata

**1 novembre 2026:** Matteo incolla i metodi on_endpoint_validity_response di PosePlanner e request_execution di MotionExecution. I due corpi sono stati letti; i nuovi file completi non sono ancora stati allegati.

**request_execution:** il frammento segue il contratto previsto: controlli su tentativo gia effettuato, goal e server, flag prima dell'invio, send_goal_async conservato in execute_goal_future, registrazione della risposta al goal su quel Future, log di invio e return True. Le uscite immediate restituiscono False. Non e necessaria una modifica a questo metodo per il log incoerente. L'ipotesi di return True mancante e esclusa dal codice ricevuto.

**on_endpoint_validity_response:** il controllo della risposta, i due vincoli e il calcolo di endpoint_verified sono coerenti con il blocco precedente. Il problema e nel blocco finale: if not submitted e allo stesso livello di if self.endpoint_verified, quindi l'else successivo appartiene al controllo di submitted.

Con endpoint positivo e submitted=True, il percorso entra nell'else di if not submitted e stampa il messaggio endpoint positivo come ERROR, spiegando esattamente il log di 34.15. Inoltre, con endpoint negativo, submitted non sarebbe assegnato e il successivo if not submitted causerebbe UnboundLocalError. Questo secondo ramo e un difetto identificato dalla lettura del codice, non un errore osservato nella demo.

Correzione mirata del blocco gia scritto da Matteo: rientrare if not submitted e il suo log dentro il ramo endpoint positivo; lasciare l'else esterno associato a if self.endpoint_verified. Lo schema corretto del solo blocco finale e:

```python
if self.endpoint_verified:
    self.get_logger().info(message)
    submitted = self.motion_execution.request_execution(
        self.planned_trajectory
    )
    if not submitted:
        self.get_logger().error(
            "Non è stato avviato un nuovo invio della traiettoria"
        )
else:
    self.get_logger().error(message)
```

Nel file reale mantenere l'indentazione del metodo: il controllo if not submitted e allineato alla riga submitted; l'else e allineato a if self.endpoint_verified. Questo e un riassetto del frammento ricevuto, non la scrittura di un nuovo metodo al posto dell'utente.

Verifica assegnata dopo la correzione: build/overlay e un nuovo log di esecuzione positivo privo dell'ERROR endpoint incoerente; osservare tre secondi dopo il risultato senza secondo invio o seconda notifica, poi chiudere con Ctrl+C senza traceback. Non e assegnata una nuova prova negativa di validita o della fase 5. L'azione ha gia un percorso positivo documentato; resta la verifica della modifica di controllo del flusso. La posa raggiunta con dati aggiornati e timeout e ancora il passo successivo. Aggiornata soltanto la guida, nessun file Python modificato dall'assistente.

### 34.17 Checkpoint - esecuzione riuscita senza il log incoerente

**1 novembre 2026:** Matteo allega il nuovo log e conferma «funziona. procediamo». Il target di panda_hand in panda_link0 e (0.3041, -0.0057, 0.7148) m, quaternion (0.997982, 0.046101, 0.006219, -0.043231). Piano SUCCESS in 0.024 s con 10 punti. FK dell'endpoint: (0.3068, -0.0078, 0.7164) m, quaternion (0.997415, 0.065377, 0.020750, -0.021419), distanza 3.817 mm, valid=True, due vincoli True e zero contatti.

Seguono un log di invio, feedback MONITOR, goal accettato, feedback di esecuzione completata e risultato ROS 4 / MoveIt SUCCESS (1), con messaggio conclusivo positivo. Il precedente ERROR che ripeteva i valori endpoint positivi non compare e il frammento non contiene traceback. Confermato il percorso positivo dell'integrazione dopo il riallineamento di 34.16. La conferma generale dell'utente non viene trasformata in log separati dei tre secondi o della chiusura; i listati completi correnti non sono stati allegati. Si procede al blocco successivo, senza richiedere una ripetizione delle prove concluse.

Il nuovo target Z=0.7148 m e coerente con il comportamento gia costruito: ogni avvio ricava la posa corrente e aggiunge 0.03 m alla quota della pinza. Non e richiesto il ritorno automatico a ready. La FK registrata continua a rappresentare il piano, non una verifica su un campione successivo a questa esecuzione.

## 35. Esercizio 24 - verificare la posa raggiunta su dati aggiornati

**Consegna iniziale del 1 novembre 2026; aggiornamento del 2 novembre in 35.9:** Matteo scrive la parte iniziale, mentre richiede all'assistente il completamento da on_fk_response compreso in poi. Nuovo modulo `/home/matteo/vision_sort_ws/src/vision_sort_lab/vision_sort_lab/pose_verifier.py`, classe Python di supporto PoseVerifier. PosePlanner conserva coordinamento, target e controlli endpoint; MotionExecution conserva l'action. PoseVerifier riceve un nuovo campione articolare dopo il risultato positivo, ne calcola la posa, valuta i vincoli originali e comunica l'esito una sola volta entro una scadenza complessiva. Nessun nuovo nodo o entry point.

### 35.1 Cosa rappresentano le figure di RViz

Matteo riferisce una figura arancione in ready e una bianca spostata verso l'alto. Nessuno screenshot o elenco corrente dei display ricevuto: la loro identita va confermata nelle proprieta, non dedotta soltanto dal colore.

Nel plugin MoveIt 2.12.4 il Goal State Color predefinito e arancione (250, 128, 0). Query Goal State mostra lo stato obiettivo della richiesta interattiva del pannello, che puo restare su ready mentre un nodo esterno esegue un'altra traiettoria. Il robot della scena/stato corrente puo apparire bianco con i materiali Panda; anche una traiettoria visualizzata puo sovrapporre altre geometrie.

Per identificarli senza muovere il robot: in Displays → MotionPlanning → Planning Request togliere Query Goal State. Se scompare l'arancione, e il goal interattivo. Se necessario disattivare anche Query Start State e, in Planned Path, Show Robot Visual / Show Robot Collision per nascondere l'anteprima. Mantenere visibile il robot della scena o il display RobotModel. Le spunte modificano la visualizzazione, non comandano il robot.

Nella demo il robot corrente deve aggiornarsi con gli stati dei giunti; l'organo terminale raggiunge una posizione circa 3 cm piu alta per ogni avvio riuscito, entro i vincoli assegnati. Il robot arancione puo restare in ready senza contraddizione. RViz e un visualizzatore; qui osserviamo gli stati pubblicati dall'hardware simulato, non una presa fisica. La verifica numerica del nuovo componente risolvera il confronto con il goal originale.

Fonti verificate: [proprieta MotionPlanning 2.12.4](https://github.com/moveit/moveit2/blob/2.12.4/moveit_ros/visualization/motion_planning_rviz_plugin/src/motion_planning_display.cpp), [visualizzazione della traiettoria 2.12.4](https://github.com/moveit/moveit2/blob/2.12.4/moveit_ros/visualization/rviz_plugin_render_tools/src/trajectory_visualization.cpp).

### 35.2 Metodo e riferimenti gia costruiti

Riutilizziamo la ricezione JointState e il filtro temporale di JointMonitor/MotionCommander, e le API GetPositionFK/GetStateValidity gia studiate in PosePlanner. Cambiano i dati: lo stato inviato ai servizi deriva da un messaggio aggiornato, non da planned_trajectory o endpoint_state. Le callback del nuovo componente sono indipendenti da quelle endpoint, che ora terminano con l'invio dell'action.

La verifica controlla la distanza entro 0.005 m e i due vincoli originali, inclusa l'orientazione ROTATION_VECTOR con tre tolleranze di 0.05 rad. Non sostituire il vincolo di orientamento con un unico limite sull'angolo del quaternion. Il successo dell'action e il successo della verifica restano due esiti distinti.

Politica per questo blocco: usare il primo singolo messaggio completo, finito e ammesso dal filtro temporale. Se il suo stato risulta fuori goal, terminare con esito negativo; non riprovare campioni finche uno passa. Campioni vecchi o incompleti vengono ignorati in attesa di uno utilizzabile, entro il timeout. Nessuna fusione di posizioni provenienti da messaggi registrati a tempi diversi.

### 35.3 API prima della scrittura: messaggi e due riferimenti temporali

| API o dato | Uso |
|---|---|
| JointState, sensor_msgs.msg | name[i] identifica position[i]; header.stamp e il tempo di registrazione |
| qos_profile_sensor_data, rclpy.qos | Profilo best effort gia usato da JointMonitor |
| node.create_subscription | Riceve tipo, topic, callback e QoS; conservare l'oggetto subscription |
| node.get_clock().now().nanoseconds | Riferimento ROS da confrontare con lo stamp del publisher |
| Clock, rclpy.clock | Costruisce un orologio separato per misurare la durata |
| ClockType.STEADY_TIME, rclpy.clock_type | Orologio monotono per il timeout |
| node.create_timer, parametro clock | Timer di 0.1 s che usa lo stesso clock steady della scadenza |
| Timer.cancel / Timer.reset | Disattiva il controllo / lo avvia quando inizia la verifica |
| math.isfinite | Verifica che una posizione non sia NaN o infinita |

L'orologio ROS e il clock steady non sono numericamente confrontabili fra loro. Conservare due istanti separati: verification_start_ns per la freschezza, start_steady_ns per la durata. Il timeout di 2.0 s deve proseguire anche se il tempo simulato e fermo; per questo anche il timer usa il clock steady. Nessun sleep, attesa bloccante o spin annidato nelle callback.

Prima del confronto, con il nodo e la demo attivi, leggere `use_sim_time` di /pose_planner, /joint_state_broadcaster e /controller_manager. Il risultato storico del 13 ottobre era False per gli ultimi due e il commander; la nuova verifica usa invece il clock di PosePlanner. Nella demo corrente attendiamo tutti False. Se i riferimenti differiscono, riportare i valori prima di interpretare gli stamp.

Import da scrivere all'inizio del nuovo file:

```python
from copy import deepcopy
import math

from moveit_msgs.msg import MoveItErrorCodes
from moveit_msgs.srv import GetPositionFK, GetStateValidity
from rclpy.clock import Clock
from rclpy.clock_type import ClockType
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import JointState

from vision_sort_lab.motion_errors import describe_moveit_error
```

Fonti: [JointState Jazzy](https://github.com/ros2/common_interfaces/blob/jazzy/sensor_msgs/msg/JointState.msg), [Clock Jazzy](https://github.com/ros2/rclpy/blob/jazzy/rclpy/rclpy/clock.py), [ClockType](https://github.com/ros2/rclpy/blob/jazzy/rclpy/rclpy/clock_type.py), [Node e timer/subscription/client Jazzy](https://github.com/ros2/rclpy/blob/jazzy/rclpy/rclpy/node.py). Le interfacce FK/validita e il server 2.12.4 restano quelli documentati in 32.

### 35.4 Costruire la classe: dati persistenti e interfaccia

Classe PoseVerifier senza base Node. Costruttore `__init__(self, node, result_callback)`: conservare self.node e self.result_callback, come in MotionExecution. Non chiamare super con un nome di nodo. La callback esterna ricevera un booleano: True soltanto se la verifica completa passa, False per campione fuori goal, errore o timeout. Il dettaglio viene loggato dal componente.

Preparare questi attributi prima di subscription e timer:

| Attributi | Valore iniziale |
|---|---|
| target_pose, target_constraints, tool_frame | None |
| sampled_state, sample_stamp_ns | None |
| fk_future, validity_future | None |
| verification_start_ns, start_steady_ns | None |
| verification_started, verification_pending, sample_captured, position_ok | False |
| timeout_sec | 2.0 |
| expected_joint_names | Sequenza ordinata panda_joint1 fino a panda_joint7 |

Creare i client FK su /compute_fk e validita su /check_state_validity e conservarli nel componente. Sono le sue risorse, indipendenti dai client usati dal planner per l'endpoint. Creare self.steady_clock con Clock e parametro clock_type uguale a ClockType.STEADY_TIME. Creare self.joint_subscription tramite il nodo, con JointState, /joint_states, self.on_joint_state e qos_profile_sensor_data. Creare self.verification_timer con periodo 0.1 s, callback self.check_timeout e parametro nominato clock=self.steady_clock; cancellarlo subito con cancel. Lo riattiveremo con reset soltanto dopo l'action riuscita.

Per questo esercizio una sola verifica per istanza: verification_started impedisce un secondo start, mentre verification_pending indica che l'operazione e ancora aperta. sample_captured impedisce di avviare piu catene FK/validita mentre arrivano altri messaggi. Tutti i metodi ROS e il logger si usano attraverso self.node.

### 35.5 Metodi da scrivere, nell'ordine di costruzione

**1. `_finish(self, succeeded, message)`.** Se verification_pending e falso, ritornare: l'esito e gia stato consegnato o la verifica non e iniziata. Altrimenti impostarlo a False, cancellare il timer, loggare message con livello info o error secondo succeeded e richiamare self.result_callback passando soltanto succeeded. Prima si chiude lo stato interno, poi si richiama il planner. Questo e il punto unico di notifica; non ripristinare verification_started.

**2. `check_timeout(self)`.** Questo metodo e anche la callback del timer, ma restituisce un booleano utilizzabile dalle altre callback. Se la verifica non e pending, restituire False. Leggere lo steady_clock attuale e calcolare (now_steady_ns - start_steady_ns) / 1_000_000_000. Se la durata e >= timeout_sec, chiamare _finish(False, messaggio di timeout) e restituire True. Altrimenti restituire False. Il limite parte una sola volta e comprende attesa del campione, FK e validita; non azzerarlo quando arriva il campione o una risposta.

**3. `start(self, target_pose, target_constraints, tool_frame)`.** Rifiutare con log e False se verification_started e gia vero o se target/vincoli mancano o i frame/link sono vuoti. Conservare copie profonde di target e vincoli e il nome del link, senza ricostruire il target da TF. Leggere verification_start_ns dal clock ROS del nodo e start_steady_ns dal proprio clock steady. Impostare verification_started e verification_pending a True; sample_captured e position_ok restano False. Riattivare il timer con reset, loggare inizio e riferimento ROS e restituire True. Il True immediato significa verifica avviata, non posa verificata.

**4. `on_joint_state(self, msg)`.**

1. Ritornare se verification_pending e falso o sample_captured e gia vero. Poi chiamare check_timeout e ritornare se restituisce True.
2. Calcolare stamp_ns con sec * 1_000_000_000 + nanosec. Ignorare il messaggio se stamp_ns <= verification_start_ns o se e maggiore del tempo ROS corrente letto nella callback. Un arrivo dopo l'action non basta a dimostrare uno stamp successivo.
3. Richiedere lunghezze name/position coerenti, nomi non duplicati e presenza di tutti i sette giunti attesi. Associare nomi e posizioni del medesimo messaggio. Richiedere valori finiti per i sette giunti. Con dati insufficienti ritornare mantenendo il timer attivo.
4. Se i client del nuovo componente non sono ancora pronti, ritornare e attendere un altro campione entro la stessa scadenza; usare service_is_ready, senza attese.
5. Costruire GetPositionFK.Request: header.frame_id dal target originale, fk_link_names con tool_frame, robot_state.is_diff=True. Inserire nel joint_state i sette nomi attesi e le corrispondenti posizioni ricavate dalla mappa; copiare anche lo stamp originale del messaggio. Conservare sampled_state come copia del robot_state, sample_stamp_ns e impostare sample_captured=True.
6. Loggare stamp del campione, riferimento e differenza positiva. Chiamare FK con call_async conservando self.fk_future; gestire un'eccezione immediata con _finish(False, messaggio). Dopo il try registrare self.on_fk_response sul Future. Non leggere planned_trajectory o endpoint_state dal planner.

**5. `on_fk_response(self, future)`.** Ritornare se la verifica non e pending, se future non e self.fk_future o se check_timeout termina l'attesa. Recuperare la risposta in un try limitato a future.result; in caso di eccezione terminare con _finish(False, messaggio). Richiedere SUCCESS, un solo link e una sola posa, link corretto e frame uguale a quello del target; anomalie terminano la verifica. Riprendere il confronto euclideo gia scritto per l'endpoint, ora sulla posa ottenuta dal campione aggiornato: loggare posa, quaternion, dx/dy/dz e distanza; conservare position_ok con soglia 0.005 m. Costruire GetStateValidity.Request usando deepcopy(sampled_state), gruppo vuoto e deepcopy(target_constraints). Non usare lo stato del piano. Inviare con call_async conservando validity_future, gestire l'eccezione immediata e registrare on_validity_response dopo il try. Il timer resta attivo. Il timestamp della risposta FK e quello del calcolo, non il tempo del campione: mantenere la prova di freschezza su sample_stamp_ns.

**6. `on_validity_response(self, future)`.** Ritornare se non pending, se future non e validity_future o se check_timeout conclude l'attesa. Recuperare response con try/except. Loggare valid, i risultati dei vincoli e il numero di contatti. Richiedere esattamente due constraint_result e che siano entrambi True, come nel controllo endpoint. Calcolare succeeded con response.valid, constraints_ok e position_ok tutti veri. Ricontrollare check_timeout prima della notifica terminale; se non scaduto chiamare _finish con succeeded e un messaggio che descriva il rispetto o il mancato rispetto della posa richiesta. Non inviare altre richieste o un nuovo movimento con campione fuori tolleranza. I callback tardivi dopo timeout troveranno pending=False e verranno ignorati.

**7. `destroy(self)`.** Disattivare verification_pending, cancellare il timer e distruggere le risorse create attraverso il nodo: node.destroy_subscription(joint_subscription), node.destroy_timer(verification_timer), node.destroy_client(fk_client) e node.destroy_client(validity_client). Non distruggere il nodo da questo componente e non notificare un nuovo esito durante la chiusura.

Le firme dei callback dei servizi ricevono un Future; on_joint_state riceve invece un messaggio, e check_timeout non riceve altri argomenti oltre self. Le callback si registrano senza parentesi. Tutte le comunicazioni sono asincrone e il timer continua a essere elaborato mentre si attendono le risposte.

### 35.6 Collegamenti limitati a PosePlanner

1. Importare PoseVerifier dal nuovo modulo. Nel costruttore, prima dei timer, inizializzare self.pose_verified=False e conservare self.pose_verifier creato passando self e il riferimento self.on_pose_verification_finished senza parentesi.
2. In on_execution_finished conservare l'esito dell'action come gia previsto. Soltanto nel ramo succeeded=True avviare self.pose_verifier.start con target_pose, target_constraints e tool_frame originali. Se lo start restituisce False, loggare che la verifica non e stata avviata; non trasformare quel valore nel risultato della posa.
3. Aggiungere `on_pose_verification_finished(self, succeeded)`: salvare il booleano in self.pose_verified e loggare l'esito della verifica. Il True di questa callback e il punto in cui possiamo dichiarare il goal di posa verificato sui dati aggiornati. Non richiede Future o handle.
4. Nel finally del main distruggere prima pose_planner.pose_verifier, poi il componente motion_execution, poi il nodo, conservando la chiusura del contesto. Nessun nuovo entry point e nessuna modifica ai controlli endpoint gia riusciti.

### 35.7 Verifica e consegna del blocco

Prima di interpretare gli stamp, con nodo/demo attivi leggere:

```bash
ros2 param get /pose_planner use_sim_time
ros2 param get /joint_state_broadcaster use_sim_time
ros2 param get /controller_manager use_sim_time
```

Per la demo corrente sono attesi tutti False; se differiscono, inviare i valori. Non confrontare stamp di clock differenti. Il timeout steady rimane distinto da questo controllo.

Scrivere il modulo completo e le piccole integrazioni, poi in Ubuntu WSL, un comando alla volta e solo se il precedente riesce:

```bash
source /opt/ros/jazzy/setup.bash
cd /home/matteo/vision_sort_ws
python3 -m py_compile src/vision_sort_lab/vision_sort_lab/pose_verifier.py src/vision_sort_lab/vision_sort_lab/pose_planner.py
colcon build --symlink-install --packages-select vision_sort_lab
source install/setup.bash
ros2 run vision_sort_lab pose_planner
```

Attesi: percorso dell'action gia funzionante → inizio verifica soltanto dopo il risultato positivo → stamp campione strettamente successivo al riferimento ROS → nuova FK del campione → confronto numerico e valutazione dei vincoli → una sola notifica di successo o fallimento entro il limite. Una posa fuori tolleranza e un risultato da esaminare, non un motivo per allargare la sfera o cambiare orientamento.

Consegna unica: pose_verifier.py, i collegamenti aggiunti a PosePlanner/main, valori use_sim_time e log completo fino al nuovo esito. Poi tenere il nodo attivo tre secondi per controllare l'assenza di altre notifiche o timeout dopo un esito gia concluso. Il caso di timeout del nuovo componente verra verificato in modo controllato dopo la revisione del primo codice, evitando di modificare il publisher della demo o ripetere le prove di collisione della fase 5.

### 35.8 Stato della consegna

Confermata l'esecuzione del piano di posa e corretta l'anomalia di log in 34.17. Assegnata la costruzione del nuovo componente di verifica; nessun suo codice o risultato ancora ricevuto. L'identificazione delle figure RViz tramite le spunte e suggerita, non osservata dall'assistente. Aggiornata solo la documentazione Windows; nessun file Python scritto o modificato dall'assistente.

### 35.9 Completamento richiesto all'assistente - callback FK, validita e integrazione

**2 novembre 2026:** Matteo chiede esplicitamente «voglio che scriva tu quello che serve da on_fk_response compreso in poi». L'assistente prepara i tre metodi finali di PoseVerifier e le due callback di PosePlanner, rispettando i nomi del contratto di 35.4-35.6. La parte gia scritta dall'utente non e stata allegata. Il tentativo di leggere `\\wsl.localhost\Ubuntu\home\matteo\vision_sort_ws\src\vision_sort_lab\vision_sort_lab\pose_verifier.py` fallisce per percorso non disponibile negli strumenti: questo non dimostra che il file manchi nell'ambiente Ubuntu dell'utente.

Frammenti salvati nel workspace Windows:

- [Metodi finali di PoseVerifier](supporto/pose_verifier_metodi_finali.txt): on_fk_response, on_validity_response e destroy, gia indentati come metodi di classe.
- [Callback del planner](supporto/pose_planner_callback_verifica.txt): on_execution_finished e on_pose_verification_finished, gia indentate come metodi di classe.
- [Verifica locale dei frammenti](supporto/test_pose_verifier_metodi_finali.py): 24 test con risposte/Future simulati, senza ROS e senza movimento del robot.

I file .txt sono blocchi da incollare nelle classi esistenti, non nuovi moduli ROS da installare. Non e stato scritto un nuovo file pose_verifier.py sostitutivo, ne sono stati modificati i sorgenti in WSL.

**Contratto necessario con la parte iniziale:** devono essere presenti self.node, verification_pending, fk_future, validity_future, target_pose, target_constraints, tool_frame, sampled_state, sample_stamp_ns, verification_start_ns, position_ok e le risorse create nel costruttore. _finish deve ricevere (succeeded, message) e chiudere/notificare una sola volta; check_timeout deve restituire True quando termina l'attesa per scadenza, False altrimenti. La richiesta FK deve conservare il Future in self.fk_future e registrarvi self.on_fk_response. Gli import sono quelli di 35.3.

La callback FK controlla verifica ancora attiva, identita del Future e deadline; gestisce eccezioni o risposta vuota, codice MoveIt, dimensioni, link e frame. Richiede il campione conservato e stamp successivo all'inizio, rifiuta valori di posa non finiti e confronta la distanza entro 5 mm. Chiede poi la validita usando copie dello stato campionato e dei vincoli originali. La callback di validita richiede valid, esattamente due vincoli veri e posizione entro tolleranza; ricontrolla la deadline prima del risultato terminale. Le risposte tardive o non appartenenti al Future atteso vengono ignorate.

**Collegamenti da completare in pose_planner.py:** importare PoseVerifier e inizializzare il componente prima dei timer:

```python
from vision_sort_lab.pose_verifier import PoseVerifier
```

Nel costruttore della classe:

```python
self.pose_verified = False
self.pose_verifier = PoseVerifier(
    self,
    self.on_pose_verification_finished,
)
```

Usare le due callback fornite nel secondo frammento. Il ramo positivo dell'action avvia start con target_pose, target_constraints e tool_frame originali. L'esito immediato di start non viene usato come successo della posa. Nel finally del main l'ordine rimane:

```python
finally:
    if pose_planner is not None:
        pose_planner.pose_verifier.destroy()
        pose_planner.motion_execution.destroy()
        pose_planner.destroy_node()
    rclpy.try_shutdown()
```

**Verifica locale osservata dall'assistente:** eseguito `python supporto/test_pose_verifier_metodi_finali.py`, 24 test riusciti. Coperti percorso positivo, copie dello stato campionato/vincoli, soglia di posizione, vincoli negativi o mancanti, frame/link/struttura errati, posa non finita, stato mancante/vecchio, eccezioni e risposte vuote, Future estranei, deadline prima della FK o della richiesta di validita e prima dell'esito, risposte tardive, notifica unica, cleanup e collegamenti al planner. I test sostituiscono i client, _finish e check_timeout con oggetti di prova: non verificano il clock steady reale, la subscription reale o il codice iniziale scritto dall'utente.

**Da verificare in ROS:** integrare i frammenti, completare i comandi di 35.7 e inviare il modulo risultante con log della nuova verifica. Restano aperti il campione reale aggiornato, l'esito finale della posa e il timeout controllato sul componente completo. Nessuna ripetizione delle prove della fase 5 e nessuna modifica dei vincoli/tolleranze. La modifica documentale e i frammenti forniti sono confermati; l'integrazione in WSL non e ancora osservata.

### 35.10 Revisione dell'allegato completo - istanti iniziali e acquisizione del campione

**2 novembre 2026:** Matteo allega l'intero pose_verifier.py come Testo incollato.txt. Il file e stato letto, inclusa la parte iniziale scritta personalmente dall'utente. Il primo log mostra ancora l'action riuscita, poi un NameError nel controllo `if not tool_framreturn` di start. Matteo corregge il nome in tool_frame e invia il successivo log: servizi pronti, piano SUCCESS (0.023 s, 10 punti), endpoint entro 2.707 mm, valid=True e due vincoli True, goal inviato/accettato e risultato ROS 4 / MoveIt SUCCESS (1). Compare «verifica avviata», poi la subscription raggiunge check_timeout e solleva TypeError nella sottrazione fra now intero e start_steady_ns=None. Non e ancora stata osservata una posa calcolata dal nuovo campione aggiornato.

**Causa dell'errore corrente:** start contiene `starting_time_ROS = self.verification_start_ns` e `starting_time_steady = self.start_steady_ns`. Queste righe leggono attributi ancora None e li copiano in variabili locali inutilizzate; non registrano nessun istante. La direzione dell'assegnazione va invertita e i valori vanno letti dai due clock:

```python
self.verification_start_ns = self.node.get_clock().now().nanoseconds
self.start_steady_ns = self.steady_clock.now().nanoseconds
```

La revisione completa individua e corregge insieme gli altri problemi nella parte iniziale, per evitare prove del robot interrotte una riga alla volta:

- _finish deve usare il parametro succeeded, non self.node.succeeded, che non e un attributo previsto del nodo.
- check_timeout deve considerare scaduto anche il limite esatto, usando durata >= timeout_sec.
- start deve conservare copie profonde del target e dei vincoli, mantenendo il nome tool_frame corretto.
- on_joint_state deve terminare quando check_timeout restituisce True; ignorare il ritorno farebbe proseguire una verifica appena conclusa.
- math.isfinite deve essere applicato ai valori numerici di joint_positions, non alla lista di stringhe joint_names; un campione non finito va scartato.
- validity_client e un client di servizio: usare service_is_ready, come per fk_client. server_is_ready appartiene invece al client dell'action.
- sampled_state viene conservato come copia del robot_state. sample_stamp_ns deve contenere l'intero stamp_ns gia calcolato; il messaggio Time copiato resta invece nel campo header.stamp della richiesta ROS.
- Alla fine di on_joint_state mancavano completamente call_async della richiesta FK, conservazione del Future e registrazione di on_fk_response. Senza queste istruzioni la verifica catturerebbe il campione ma non avvierebbe il calcolo.

**Copia revisionata:** [pose_verifier_revisionato.py](supporto/pose_verifier_revisionato.py). E il file allegato dall'utente con correzioni mirate nella parte iniziale e completamento dell'invio FK; non e una riprogettazione della classe. I metodi on_fk_response, on_validity_response e destroy gia integrati dall'utente rimangono invariati; l'identita e stata controllata confrontandone gli AST. Disponibile anche il [confronto delle modifiche](supporto/pose_verifier_revisionato.diff). L'allegato originale non e stato modificato e il file WSL non e stato sovrascritto dall'assistente.

**Verifica locale osservata:** [test_pose_verifier_revisionato.py](supporto/test_pose_verifier_revisionato.py), 15 test riusciti. Viene eseguita la classe completa della copia revisionata usando tipi, client, timer e clock di prova. Coperti registrazione corretta dei due tempi, copie dei target, percorso messaggio fresco → FK → validita → callback, stamp intero, campioni vecchi/futuri/incompleti/non finiti, prontezza dei servizi, una sola catena FK, errore immediato di invio, scadenza esatta a due secondi anche senza avanzamento ROS, timeout durante FK o validita e risposte tardive, scelta del logger dal parametro succeeded, notifica unica e pulizia. Questi nuovi test verificano anche i metodi iniziali reali della copia, senza sostituire _finish/check_timeout come nei 24 test del solo completamento di 35.9. Non e una prova con i servizi ROS reali o con il tempo del sistema della demo.

**Prossimo passo:** applicare la copia revisionata al sorgente Ubuntu, poi controllo sintattico, build, overlay e nuovo avvio come in 35.7. Per copiare il file dal workspace Windows, se /mnt/c e disponibile come nel percorso gia usato per gli asset:

```bash
cp /mnt/c/Users/matte/Documents/Codex/2026-10-05/vor/outputs/vision-sort-lab/supporto/pose_verifier_revisionato.py /home/matteo/vision_sort_ws/src/vision_sort_lab/vision_sort_lab/pose_verifier.py
```

Inviare il nuovo log completo fino alla verifica della posa. Restano da confermare runtime ROS, origine temporale coerente degli stamp e timeout controllato nel componente reale. La scena, le tolleranze e la pianificazione endpoint gia verificate non ricevono nuove prove. La correzione di tool_frame riferita dall'utente e registrata come applicata; le altre correzioni sono presenti nella copia locale e attendono conferma nell'ambiente Ubuntu.

### 35.11 Istanti iniziali corretti - controllo di finitezza sulla lista sbagliata

**2 novembre 2026:** Matteo invia il nuovo start e un altro log. Nel metodo ricevuto tool_frame e corretto e vengono assegnati verification_start_ns dal clock ROS e start_steady_ns dal clock steady. Rimangono due variabili locali starting_time_ROS e starting_time_steady che leggono gli stessi valori ma non vengono usate; possono essere rimosse. Il target e i vincoli nel frammento sono ancora assegnati per riferimento: la copia revisionata di 35.10 usa deepcopy.

Il nuovo log mostra piano SUCCESS (0.024 s, 11 punti), target (0.3168, -0.0028, 0.7399) m, endpoint FK entro 2.797 mm, valid=True e due vincoli True. L'action termina con ROS 4 / MoveIt SUCCESS (1) e la verifica parte. La callback dei giunti supera il precedente problema dell'istante None e si arresta su `math.isfinite(joint_names)` con TypeError: must be real number, not list.

math.isfinite accetta un singolo numero; joint_names e una lista di nomi. La verifica richiesta riguarda invece ogni valore della lista joint_positions. Sostituzione puntuale dopo la costruzione delle due liste:

```python
if not all(math.isfinite(value) for value in joint_positions):
    return
```

La funzione all richiede che tutti i controlli siano veri; il return scarta un campione con NaN o valori infiniti mantenendo l'attesa entro il timeout. Le verifiche precedenti assicurano gia che ci siano i sette nomi e le relative posizioni.

La sostituzione e gia presente in supporto/pose_verifier_revisionato.py, insieme alle correzioni di _finish, timeout, prontezza del servizio, stamp intero e invio della richiesta FK che erano emerse dalla revisione integrale dell'allegato. Per la prossima prova usare la copia completa o applicare tutte le modifiche del diff di 35.10: il nuovo traceback dimostra che almeno il controllo math.isfinite nel file in esecuzione e ancora quello originario. Non dichiarare applicate le correzioni non mostrate dall'utente.

Nessuna ulteriore modifica al file revisionato e nessuna nuova esecuzione dei test locali, gia passati senza cambiamenti in 35.10. Aggiornata la guida con la nuova evidenza; l'esito della posa su campione aggiornato resta ancora da ricevere.

### 35.12 Ramo di timeout raggiunto - riferimento errato al parametro succeeded

**2 novembre 2026:** nuovo log con target (0.3234, -0.0019, 0.8271) m, piano SUCCESS (0.016 s, 11 punti), endpoint FK entro 4.685 mm, valid=True e due vincoli True. L'action e ancora accettata e conclusa con ROS 4 / MoveIt SUCCESS (1); segue «verifica avviata». Il timer raggiunge check_timeout, che chiama _finish(False, 'Timeout scaduto'). Nel corpo di _finish e ancora presente `if self.node.succeeded is True`, che solleva AttributeError: PosePlanner non ha l'attributo succeeded.

La condizione deve leggere il parametro locale succeeded ricevuto da _finish. In questa chiamata il valore e False perche proviene dal timeout. Correzione puntuale:

```python
if succeeded:
```

Non creare un nuovo attributo succeeded nel planner per risolvere il nome: la scelta del log dipende dall'esito passato al metodo. Il file supporto/pose_verifier_revisionato.py contiene gia questa correzione. Il traceback mostra quindi che il corpo in esecuzione conserva almeno una riga della versione precedente; non permette di stabilire se dipenda da correzioni manuali parziali, copia, build o overlay.

Il timeout e un fatto distinto dall'errore del logger: il ramo di scadenza viene raggiunto, ma la procedura di conclusione si interrompe prima della result_callback. Non e una prova riuscita del timeout controllato. Nel frammento non compaiono i nuovi log di campione acquisito o FK della posa raggiunta, per cui non si conclude ancora se manchino campioni ammessi, invio FK o risposte. La revisione completa dell'allegato aveva individuato anche l'invio FK mancante; occorre verificare il file effettivamente caricato prima di dedurre una causa del timeout.

Prossimo passo richiesto prima di un altro movimento: applicare il file revisionato, build e overlay come in 35.10, poi ispezionare l'import senza istanziare nodi:

```bash
python3 -c "import inspect; from vision_sort_lab.pose_verifier import PoseVerifier; print(inspect.getfile(PoseVerifier)); print(inspect.getsource(PoseVerifier._finish))"
```

Il comando mostra percorso e corpo del metodo importato e non avvia il planner. Atteso if succeeded senza self.node.succeeded. Richiesto quell'output; non assegnato un altro lancio di movimento per verificare semplicemente il riferimento Python. Nessuna modifica al file revisionato locale, gia verificato in 35.10. Aggiornata la guida; integrazione ROS della verifica e causa concreta del timeout ancora da confermare.

### 35.13 Checkpoint - posa raggiunta verificata su un campione aggiornato

**2 novembre 2026:** Matteo allega il primo log completo positivo della sequenza pianificazione → esecuzione → verifica su nuovi stati articolari. Il target e (0.3238, -0.0032, 0.9213) m in panda_link0 per panda_hand, quaternion (0.996498, 0.051528, 0.061775, -0.022820). Piano SUCCESS in 0.014 s con 17 punti; endpoint previsto entro 2.914 mm, valid=True, due vincoli True e zero contatti. Il goal viene inviato e accettato; feedback MONITOR, esecuzione completata e IDLE; risultato ROS 4 / MoveIt SUCCESS (1).

Dopo il risultato positivo il nuovo verificatore produce:

```text
verifica avviata
Campione aggiornato acquisito:
  stamp_ns=1793638217584865605
  riferimento_ns=1793638217578727494
Posa raggiunta da FK in panda_link0:
  pos=(0.3222, -0.0009, 0.9221) m
  q=(0.996039, 0.037060, 0.079106, -0.016608)
Campione verificato:
  dx=-1.538, dy=2.345, dz=0.792 mm
  distanza=2.914 mm | entro 5 mm=True
Validita posa raggiunta: True | Vincoli: [True, True]
  Numero di contatti: 0 | Posizione entro 5 mm: True
Posa raggiunta verificata sui dati aggiornati
Verifica della posa conclusa con successo
```

Lo stamp del campione supera il riferimento di **6_138_111 ns = 6.138111 ms**. Questo e il confronto dei timestamp di registrazione e attivazione, non una misura della latenza di trasporto. La notifica positiva del verificatore e stampata circa 10.931 ms dopo quel riferimento ROS; non sostituisce una misura del clock steady interno. Il percorso positivo si conclude entro il limite previsto e non compare un traceback.

**Confermato dal log:** la richiesta FK del campione aggiornato e il successivo GetStateValidity raggiungono il risultato, i vincoli originali risultano soddisfatti e il planner riceve l'esito positivo. La posa prevista e quella ricavata dal campione concordano alle cifre mostrate. Le correzioni necessarie non sono piu bloccanti nel percorso osservato. Il sorgente corrente non e stato nuovamente allegato e non si presume che coincida in ogni dettaglio con la copia locale di 35.10. I valori use_sim_time correnti non sono stati forniti separatamente; il log mostra il confronto temporale numerico ammesso dal filtro.

Il frammento mostra un solo ciclo e una sola notifica conclusiva; non viene trasformato in una prova separata dei tre secondi successivi o della chiusura. Il robot e ancora quello della demo con hardware simulato: questa e verifica dello stato pubblicato e del modello, non presa fisica o percezione indipendente.

**Rimane aperto il test del timeout del componente reale.** In 35.12 il ramo di scadenza era stato raggiunto ma la notifica falliva; i 15 test locali di 35.10 usano risorse di prova. Prima della pre-presa completare quindi un test controllato in ROS con un'istanza isolata di PoseVerifier che non riceve un campione, senza inviare una nuova traiettoria. Non ripetere per questo le prove di pianificazione, endpoint o collisione della fase 5.

## 36. Passaggio alla nuova chat - timeout del verificatore e successiva pre-presa

### 36.1 Stato da portare nella nuova chat

**2 novembre 2026:** Matteo chiede di procedere e se sia opportuno aprire una nuova chat. E un punto di passaggio utile: il percorso positivo della prima operazione di posa e completo. La risposta consiglia una nuova chat con questa guida e le versioni correnti dei moduli; non viene creata automaticamente una nuova conversazione.

Classi e responsabilita attuali:

- PosePlanner: nodo ROS, lettura TF, target Z +0.03 m, pianificazione e verifica dell'endpoint; coordina gli altri componenti.
- MotionExecution, modulo motion_execution.py: classe di supporto con ExecuteTrajectory, accettazione, feedback e risultato; percorso positivo confermato.
- PoseVerifier, modulo pose_verifier.py: campione aggiornato dopo il risultato, FK, validita dei vincoli originali, deadline di 2 s sul clock steady e notifica unica; percorso positivo reale confermato in 35.13.
- ToolPoseReader e JointMonitor restano riferimenti didattici; motion_builders e motion_errors restano moduli separati.

Ambiente: Ubuntu 24.04 WSL, ROS 2 Jazzy, demo Panda/MoveIt con hardware simulato; MoveIt server osservato 2.12.4. Scena di sei oggetti gia conclusa: work_table, piece_red_1, piece_blue_1, piece_red_2, bin_red e bin_blue, con stessa mesh per collisioni e visualizzazione dei contenitori. Nessuna ripetizione delle prove della fase 5.

Preferenze: spiegare le API prima dell'uso e guidare esplicitamente firma, attributi, ordine dei controlli e verifica. Favorire componenti nuovi in file separati quando hanno una responsabilita autonoma. Matteo scrive personalmente il codice guidato, salvo richieste esplicite di far scrivere blocchi all'assistente, come in 35.9. Aggiornare la guida a ogni checkpoint e distinguere codice fornito, risultati locali e risultati reali.

### 36.2 Primo blocco della prossima chat - timeout senza movimento

Preparare un test ROS isolato del PoseVerifier corrente, senza avviare PosePlanner/MotionExecution e senza inviare ExecuteTrajectory. L'istanza di prova deve essere attivata con riferimenti validi e privata in modo controllato della possibilita di acquisire un campione; non interrompere il publisher della demo o modificare la scena.

Criteri di completamento:

1. Il clock steady della verifica porta alla scadenza dopo circa 2 s; il periodo di controllo e 0.1 s e non e una garanzia di scadenza esatta.
2. _finish conclude senza eccezioni, cancella il timer e consegna esattamente un risultato False.
3. Nei tre secondi successivi non compaiono altre notifiche o timeout ripetuti.
4. Nessuna richiesta FK/validita viene avviata se il campione non e stato acquisito; nessun movimento o comando al controllore.
5. Pulizia delle risorse e chiusura senza traceback. La classe di produzione non deve rimanere con una modifica temporanea di test.

Partire dalla revisione del codice attuale allegato. E possibile disattivare soltanto la subscription dell'istanza isolata prima dello spin, lasciando indipendente il timer steady; spiegare prima eventuali API aggiuntive del piccolo nodo di prova. Progettare un blocco unico con implementazione e output richiesto. La prova e ancora da svolgere: il positivo di 35.13 non dimostra questo ramo.

Dopo questo checkpoint: definire il riferimento operativo/TCP della pinza e il primo target di pre-presa di piece_red_1 usando pose note. Restano successivi avvicinamento, comando pinza, gestione dell'oggetto collegato nella scena, sollevamento, trasporto e deposito. Gazebo e visione non sono il prossimo blocco immediato.

### 36.3 Testo di ripresa da copiare

```text
Riprendiamo ROS 2 Vision Sort Lab, fase 6.

Leggi prima:
C:\Users\matte\Documents\Codex\2026-10-05\vor\outputs\vision-sort-lab\GUIDA-PROGETTO.md

Riparti dal checkpoint 35.13 e dalla sezione 36.
Sono riusciti pianificazione di posa, verifica endpoint, ExecuteTrajectory
tramite MotionExecution e verifica della posa raggiunta tramite PoseVerifier.
Il campione supera il riferimento di 6.138111 ms; la posa raggiunta e entro
2.914 mm, valid=True, due vincoli True, zero contatti. Il planner riceve
l'esito positivo.

Primo nuovo blocco: test controllato del timeout reale di PoseVerifier,
con una sola notifica negativa e chiusura pulita, senza comandare nuovi
movimenti. Dopo questo passiamo al riferimento operativo/TCP e alla
pre-presa di piece_red_1 da posa nota.

Non ripetere le prove della fase 5 o il percorso positivo gia concluso.
Spiega prima le API, guidami esplicitamente nella scrittura e raggruppa
implementazione e verifica. Preferisci file separati per nuove responsabilita.
Scrivo il codice guidato, salvo quando chiedo esplicitamente di scriverlo tu.
Aggiorna la guida a ogni checkpoint.
```

Allegare nella nuova chat le versioni correnti di pose_planner.py, pose_verifier.py e motion_execution.py dal workspace Ubuntu. Le copie di supporto Windows restano materiale di riferimento e non sostituiscono la lettura delle versioni effettivamente eseguite. Se necessario per il target di pre-presa, aggiungere poi motion_builders.py. La guida e PERCORSO.md sono stati aggiornati; nessun sorgente Python modificato per questo passaggio.

## 37. Roadmap dettagliata dopo la prima posa verificata

**2 novembre 2026:** Matteo chiede il dettaglio dei prossimi passi. Le sezioni 37.1-37.12 raccolgono la roadmap iniziale e i blocchi funzionali; il momento proposto per l'ingresso in Gazebo viene poi anticipato in 37.13. Non sono esercizi gia eseguiti o quote di presa gia validate. Il prossimo blocco operativo resta il test di timeout di 36.2. I nuovi componenti saranno definiti in file separati quando emergera la relativa responsabilita; i nomi futuri non sono interfacce gia installate. Ogni blocco verra assegnato con API, implementazione e verifica.

### 37.1 Timeout del verificatore, senza un altro movimento

Usare un'istanza isolata di PoseVerifier a cui si impedisce in modo controllato di acquisire un campione. Il timer steady rimane attivo; non si istanzia MotionExecution e non si comanda il braccio. Verificare scadenza intorno a 2 s, una sola callback False, nessuna eccezione e nessuna notifica aggiuntiva nei tre secondi successivi. Chiudere pulitamente il nodo di prova. Questo completa il ramo negativo temporale della verifica; il percorso positivo gia concluso non deve essere rifatto come prerequisito.

### 37.2 Definire il punto operativo della pinza

Riprendere i dati del modello gia letti in 30.1 e controllare la geometria delle dita e i riferimenti necessari al compito. Stabilire un TCP, cioe il punto operativo fra le dita, e la sua trasformazione rispetto al link reale panda_hand. Nei file letti non risultava un TCP dedicato: non presumere l'esistenza di un nuovo link. Se e sufficiente, usare un offset esplicito invece di modificare la descrizione del robot.

Codice coinvolto: helper geometrici/builder e letture TF/FK gia studiate. L'offset e la convenzione degli assi verranno resi espliciti; un target riferito al TCP va tradotto correttamente per il link controllato. Verifica conclusiva: indicare in modo univoco quale punto e quale orientamento stiamo comandando e confrontarne la collocazione con il modello. L'origine di panda_hand non viene posta arbitrariamente nel centro del cubo.

### 37.3 Costruire le pose del primo cubo

Primo oggetto: piece_red_1, centro noto (0.45, -0.20, 0.02) m in panda_link0, lato 0.04 m e faccia superiore a z=0.04 m, come gia documentato. Da questi dati ricavare orientamento di presa dall'alto, posa di pre-presa sopra l'oggetto, posa di presa e quota di sollevamento. Le distanze operative verranno scelte dopo la definizione del TCP e le verifiche geometriche, non copiate come coordinate di panda_hand.

Preparare funzioni che costruiscono PoseStamped senza muovere il robot. Prima verificare frame, quaternion e relazione geometrica fra pose; poi pianificabilita e collisioni delle nuove pose. Lo scopo e passare dall'esperimento Z +0.03 m a obiettivi espliciti legati all'oggetto. I controlli specifici per queste nuove pose non sono una ripetizione delle prove concluse della scena.

### 37.4 Rendere riutilizzabile la pipeline di movimento

L'attuale esercizio e avviato una volta dal timer, con flag di pianificazione, esecuzione e verifica validi per una singola operazione. Una sequenza di manipolazione richiede piu movimenti nello stesso processo. Ampliare i metodi esistenti per ricevere un target esplicito e riportare un esito complessivo, distinguendo richiesta di piano, esito dell'action e verifica del goal.

Progettare un riarmo controllato di MotionExecution e PoseVerifier quando l'operazione precedente e terminata; non azzerare indiscriminatamente i flag durante le callback. Conservare copie dei riferimenti della nuova operazione, rifiutare richieste sovrapposte e ignorare eventuali risposte tardive appartenenti alla precedente. Definire il comportamento dopo errore o timeout prima di consentire una nuova richiesta.

Verifica conclusiva: richieste successive ammesse solo quando la pipeline e libera, esito singolo per operazione e assenza di riuso di target/campioni/Future precedenti. Prima di concatenare molte pose, usare poche operazioni controllate e il codice corrente allegato. Non ricreare nodi, client o subscription a ogni messaggio di stato.

### 37.5 Comando indipendente della pinza

Individuare nella demo i controller e le action effettivamente disponibili, con relativi tipi e giunti. Solo dopo scegliere l'interfaccia e spiegare il significato dei suoi argomenti; non presumere un nome di action o una funzione hardware Franka non verificata. Controllare la relazione fra posizione del singolo dito e apertura totale e i limiti del modello.

Costruire un componente dedicato alla pinza in un nuovo modulo: apertura, chiusura, gestione dell'esito e confronto con gli stati pubblicati. Verifica iniziale senza oggetto afferrato: dita che raggiungono aperture richieste e un solo esito per comando. L'apertura scelta per avvicinarsi al cubo deve lasciare spazio alla larghezza di 4 cm entro i limiti della pinza. Nella demo mock la chiusura non prova contatto o forza di presa.

### 37.6 Raggiungere la pre-presa

Aprire la pinza e usare il target esplicito sopra piece_red_1. Riutilizzare pianificazione, verifica endpoint, MotionExecution e PoseVerifier per raggiungerlo. Il criterio e il TCP nella posizione/orientamento di pre-presa e il rispetto delle collisioni nella nuova geometria, con la pinza pronta ad avvicinarsi. Il cubo resta libero nella scena.

### 37.7 Avvicinamento controllato alla presa

Il goal di posa attuale vincola la destinazione ma non rende rettilineo tutto il percorso. Per il tratto locale pre-presa → presa studiare GetCartesianPath: punti intermedi, passo di campionamento, collisioni, vincoli, error_code e fraction della soluzione. Esigere un segmento completo e una traiettoria utilizzabile con tempi coerenti; una soluzione parziale va esaminata prima di eseguirla.

Prevedere e limitare i contatti intenzionali tra oggetto e dita nelle fasi appropriate, senza disabilitare globalmente le collisioni. Verifica: avvicinamento nella direzione stabilita, orientamento conforme, nessun contatto indesiderato con tavolo o altri oggetti e posa finale verificata. La scelta precisa dei vincoli e dei permessi di contatto verra implementata nel blocco dedicato.

Fonte dell'interfaccia da studiare: [GetCartesianPath](https://github.com/moveit/moveit_msgs/blob/ros2/srv/GetCartesianPath.srv), da confrontare con quella installata prima dell'uso.

### 37.8 Chiudere la pinza e collegare l'oggetto nella scena

Raggiunta la posa di presa, comandare la chiusura e verificarne l'esito riportato. Poi gestire piece_red_1 come oggetto collegato al link reale della pinza mediante AttachedCollisionObject, con posa relativa coerente e touch_links limitati ai link necessari. La trasformazione di collegamento deve conservare la posa del cubo nel passaggio da libero a collegato.

Estendere SceneInspector per distinguere oggetti liberi e collegati. Criterio: un solo oggetto con quell'ID, collegato al link corretto, assente dall'elenco degli oggetti liberi e rappresentato nelle collisioni del robot. Nella demo si tratta di un aggancio ideale dichiarato: non e prova di presa fisica, attrito o contatto.

Fonte: [AttachedCollisionObject](https://github.com/moveit/moveit_msgs/blob/ros2/msg/AttachedCollisionObject.msg). I touch_links indicano i link che l'oggetto collegato puo toccare; non sostituiscono una politica dei contatti per tutti gli oggetti liberi della scena.

### 37.9 Sollevare e trasportare il cubo

Prima sollevare con un breve tratto controllato che liberi il cubo dal tavolo; poi pianificare il trasporto verso una posa sopra bin_red. Durante il trasporto il pianificatore deve considerare anche l'ingombro del cubo collegato. Ogni tratto viene eseguito e verificato prima del successivo.

Criteri: cubo solidale alla pinza nella scena, assenza di collisioni indesiderate, arrivo sopra il contenitore e posizione/orientamento verificati. Le quote dipendono da TCP, cubo, fondo e pareti del contenitore e vanno calcolate e controllate; non sono fissate da questa roadmap.

### 37.10 Deposito, rilascio e arretramento

Definire la posa di deposito nel vano di bin_red considerando dimensioni del pezzo e del fondo. Raggiungerla, aprire la pinza, scollegare l'oggetto e riportarlo come oggetto libero con posa coerente. Poi allontanare la pinza dal contenitore lungo un tratto controllato.

Verificare oggetto non piu collegato, posa mondiale nel contenitore previsto e mano libera nella posa di arretramento. In questa fase mock la posa dell'oggetto libero viene gestita esplicitamente: la gravita o l'assestamento nel contenitore non sono ancora simulati. La sola apertura della pinza non e la verifica del deposito.

### 37.11 Coordinatore del ciclo e tre oggetti

Riunire i blocchi validati in un coordinatore a stati in un modulo dedicato. Stati indicativi: apri → pre-presa → avvicina → chiudi → collega → solleva → trasporta → deposita → apri → scollega → arretra. Il prossimo stato parte solo dopo l'esito richiesto dal precedente; un errore produce uno stato terminale leggibile con causa e stato noto dell'oggetto.

Iniziare con un ciclo completo di piece_red_1. Poi usare i tre ID e l'associazione nota rosso → bin_red, blu → bin_blue. Non introdurre ancora la percezione per scegliere il colore: il compito usa i dati noti. Il recupero non deve rilasciare automaticamente un oggetto trasportato o dichiarare presa/deposito in base al solo successo di una action.

Criterio: ciclo completo senza interventi tra le fasi per un oggetto, poi corretta distribuzione dei tre oggetti, aggiornamento coerente della scena e log dell'esito di ogni fase.

### 37.12 Fasi successive: fisica, visione e robustezza del compito

1. **Gazebo:** integrare robot, controllori e oggetti con contatti e gravita; sincronizzare la scena MoveIt con lo stato del simulatore. Verificare presa fisica e oggetto realmente sollevato. La strategia di aggancio ideale non deve essere confusa con questa nuova prova.
2. **Visione:** aggiungere una camera simulata, verificare i suoi riferimenti/calibrazione, ricavare colore e posa dalle immagini e trasformare il risultato nel frame del robot. Le misure percettive sostituiranno le pose note mantenendo l'orchestrazione gia validata. Misurare l'errore rispetto alla ground truth del simulatore.
3. **Recupero e metriche:** verificare esistenza e posizione del pezzo dopo le azioni, riconoscere presa o deposito falliti, progettare recuperi limitati e registrare successi, tempi ed errori su prove ripetibili. I limiti della cancellazione nella demo gia documentati restano separati e non vengono considerati risolti dalla nuova roadmap.

**Stato:** pianificati i prossimi blocchi su richiesta dell'utente. Nessun nuovo movimento, componente Python, controller o test e stato eseguito per questa descrizione. La prova operativa immediata resta soltanto 37.1 / 36.2.

### 37.13 Quando iniziare Gazebo - proposta di anticipazione

**2 novembre 2026:** Matteo domanda «ma quando facciamo il salto a Gazebo?». La roadmap iniziale collocava l'integrazione fisica dopo il ciclo completo di uno e poi tre oggetti in MoveIt. L'assistente propone di anticipare il passaggio: non e necessario completare tutto il ciclo mock prima di iniziare a lavorare con la fisica.

Sequenza consigliata da questo punto:

1. Chiudere il timeout reale isolato di PoseVerifier, senza altro movimento.
2. Definire riferimento operativo/TCP e verificare la descrizione del robot che useremo coerentemente con MoveIt e Gazebo. Non richiedere gia il ciclo completo di pre-presa, aggancio ideale e deposito.
3. Iniziare l'integrazione Gazebo: controllare installazione/versioni, caricare il Panda e collegare i controller al simulatore. Primo checkpoint: una traiettoria comandata dal percorso MoveIt/Python eseguita dal robot simulato, con stati aggiornati e verifica finale.
4. Aggiungere tavolo e un cubo fisico, allineare lo stato del simulatore e la scena MoveIt, quindi sviluppare pre-presa, pinza, presa e deposito nell'ambiente fisico. Il collegamento dell'oggetto nella scena del pianificatore non deve produrre artificialmente una presa fisica riuscita nel simulatore.
5. Completare un oggetto, poi i tre; visione e recupero seguono come previsto.

Le funzioni descritte in 37.3-37.11 restano necessarie, ma possono essere costruite progressivamente dopo l'ingresso in Gazebo. Il riuso controllato della pipeline e il coordinatore rimangono necessari per le sequenze; non serve completarli prima di caricare il robot e provarne il primo movimento fisico simulato. Non e una stima di giorni o di numero di chat: i primi due punti sono i checkpoint che precedono l'inizio dell'integrazione.

Stack di riferimento confermato dalla documentazione ufficiale: Ubuntu 24.04 / ROS 2 Jazzy con Gazebo Harmonic; gz_ros2_control collega ros2_control al modello Gazebo. La configurazione Panda concreta e la disponibilita locale dei pacchetti vanno ancora controllate; non si presume che la demo mock attuale sia gia pronta per Gazebo. I componenti Python potranno essere riutilizzati attraverso le interfacce ROS mantenute coerenti, adattando configurazione, controller e riferimenti temporali.

Fonti consultate: [abbinamento ROS/Gazebo](https://gazebosim.org/docs/harmonic/ros_installation/), [gz_ros2_control per Jazzy](https://control.ros.org/jazzy/doc/gz_ros2_control/doc/index.html). Nessun pacchetto installato e nessuna configurazione robot modificata per questa proposta. Il prossimo esercizio resta il timeout; prima di assegnare un lungo ciclo mock, riprendere questa proposta di anticipazione con l'utente.

## 38. Collaborazione GitHub per completare verifiche e TCP

### 38.1 Richiesta e ambito autorizzato

**2 novembre 2026:** Matteo chiede che l'assistente esegua i due prossimi passi, chiusura delle verifiche e definizione del TCP, riprendendo personalmente il lavoro da quando inizieremo a collegare Gazebo. Propone di creare una repository GitHub accessibile all'assistente e richiede in questa chat l'elenco esatto dei comandi terminale necessari a verificare il risultato in WSL.

L'ambito comprende correzioni necessarie, test del timeout, definizione geometrica del TCP, helper/configurazione e verifiche del riferimento operativo. Non include iniziare installazioni o integrazione Gazebo al posto dell'utente. Non e una richiesta di creare una nuova chat o di spostare il lavoro altrove.

### 38.2 Accesso verificato e limite del collegamento

Il tool GitHub get_profile conferma l'account collegato Matteo7100. Sono disponibili strumenti per leggere file, creare branch, aggiornare contenuti, commit e pull request. L'URL successivamente comunicato e https://github.com/Matteo7100/RoboCell: lettura verificata, ma creazione del ramo rifiutata con 403 Resource not accessible by integration. I metadati del proprietario riportano push=true: questo non dimostra che il token del collegamento abbia accesso di scrittura. Anche gh locale risulta non autenticato. Dettagli e lavoro locale in sezione 39.

GitHub puo fungere da sorgente condivisa: l'assistente legge le versioni effettive e pubblica modifiche su un ramo dedicato, con commit e descrizione dei test. Questo non conferisce accesso al processo ROS, alla GUI RViz o alla WSL dell'utente. I test eseguibili localmente o in un ambiente automatico restano distinti dalle verifiche ROS eseguite dall'utente con i comandi forniti. Nessuna verifica reale verra marcata completata per il solo fatto che il codice e stato scritto o pubblicato.

Per la domanda di accesso e workflow e stata applicata la skill OpenAI Docs e consultata la [documentazione ufficiale Codex Cloud](https://learn.chatgpt.com/docs/cloud), che descrive selezione delle repository, preparazione dell'ambiente, test e pubblicazione tramite commit/PR. Il workflow concreto di questa chat usa il collegamento GitHub disponibile; non richiede automaticamente una nuova chat cloud.

### 38.3 Contenuto da mettere nella repository

Struttura consigliata: repository con radice nel workspace ~/vision_sort_ws, sorgenti sotto src/vision_sort_lab e documentazione sotto docs. Includere il pacchetto completo aggiornato: moduli Python, package.xml, setup.py/setup.cfg, risorse e mesh usate dal progetto, eventuali configurazioni/launch e test. Escludere build/, install/, log/, cache Python e ambienti virtuali. Pubblicare sorgenti coerenti, non i file generati citati nei traceback.

Portare anche GUIDA-PROGETTO.md e PERCORSO.md, indicando che la versione piu recente di questa fase e quella del 2 novembre con il presente incarico. Una volta disponibile la repository, verificare se workspace o pacchetto sono gia versionati prima di inizializzare un nuovo repository o cambiare remoti. I comandi del primo caricamento andranno adattati all'URL e allo stato locale, senza assumere che esista gia un ramo o un remoto specifico.

Per definire il TCP serve la descrizione del robot effettivamente caricata, inclusi riferimenti e geometrie delle dita. Preparazione in Ubuntu WSL con la demo Panda attiva:

```bash
source /opt/ros/jazzy/setup.bash
source /home/matteo/vision_sort_ws/install/setup.bash
mkdir -p /home/matteo/vision_sort_ws/docs/robot_reference
ros2 param dump /move_group > /home/matteo/vision_sort_ws/docs/robot_reference/move_group.params.yaml
ros2 param dump /robot_state_publisher > /home/matteo/vision_sort_ws/docs/robot_reference/robot_state_publisher.params.yaml
```

I file devono contenere gli output validi delle richieste, non messaggi di nodo assente. I dump permettono di confrontare la descrizione usata da MoveIt con quella del publisher TF. Se il modello rimanda a geometrie esterne necessarie a scegliere il punto fra le dita, l'assistente specifichera i soli asset/configurazioni ulteriori da aggiungere dopo la lettura; non verra inventato un offset numerico.

### 38.4 Lavoro che svolgera l'assistente

1. Leggere i sorgenti correnti e verificare il collegamento della repository. Lavorare su un ramo dedicato, con modifiche reviewabili e versioni identificabili tramite commit.
2. Chiudere le verifiche del PoseVerifier: percorso positivo gia osservato, timeout isolato ROS senza nuovo movimento, notifica negativa unica, assenza di callback tardive/duplicate e cleanup. Implementare quanto necessario e aggiungere test appropriati.
3. Ricavare e documentare il TCP dal modello effettivo: convenzione del punto e degli assi, trasformazione rispetto al link reale e coerenza geometrica. Implementare helper/configurazione e controlli per TF/FK e conversione dei target. Non aggiungere un frame/link non supportato come se fosse gia nel modello.
4. Aggiornare guida e istruzioni di prova e pubblicare le modifiche. Se viene creata una PR, allegarla alla chat. Non dichiarare eseguiti test che richiedono la WSL senza averne ricevuto l'output.

### 38.5 Comandi da consegnare qui dopo l'implementazione

L'elenco finale dovra usare branch, percorsi ed eseguibili realmente creati e comprendere:

- acquisizione del commit in WSL e controllo della versione importata;
- build del pacchetto e caricamento overlay;
- test automatici e lettura dei risultati;
- comando isolato per il timeout, con risultato False unico e conclusione pulita;
- comandi per la verifica del TCP rispetto al modello e ai dati TF/FK aggiornati;
- output attesi, criteri di successo e dati da riportare in caso di errore.

I nomi dei nuovi comandi non vengono presentati come gia disponibili prima di essere implementati. Le istruzioni iniziali sopra preparano la repository e il modello; non sono la dichiarazione che i due blocchi sono gia conclusi.

**Stato aggiornato:** URL ricevuto e sorgenti letti; il lavoro locale e iniziato come descritto in sezione 39. Nessun file remoto modificato e nessun comando ROS eseguito per conto dell'utente. L'utente eseguira i comandi di verifica e tornera a scrivere il codice da Gazebo.

## 39. RoboCell letta: implementazione locale di timeout e geometria TCP

### 39.1 Sorgenti effettivi e accesso alla repository

Repository comunicata: https://github.com/Matteo7100/RoboCell.
Branch letto: main; commit d0a779fb13b6f9faf677d2486586d5b6dc2f7c91;
tree cc1e6e47209696d7003f461824b686b123af3926.
La radice contiene vision_sort_lab/ come cartella completa del pacchetto, non
src/vision_sort_lab. Nessun AGENTS.md o descrizione URDF/SRDF e presente nel tree
letto. I sorgenti remoti sono stati acquisiti nella sottocartella locale RoboCell.

La lettura dei file e riuscita. Il tentativo di creare codex/verification-tcp
dal commit letto ha ricevuto GitHub 403 Resource not accessible by integration.
Nessun branch, commit o PR remoto e stato creato. gh auth status conferma che
il terminale Windows non ha account GitHub autenticati. Non si e tentato di
scrivere direttamente su main per aggirare il problema.

E stato richiesto a Matteo di completare in PowerShell:

```powershell
gh auth login --hostname github.com --git-protocol https --web
```

La procedura interattiva deve essere completata personalmente nel browser.
Non inviare password, token o codici in chat. Non e una nuova richiesta di
autorizzazione alle modifiche: l'incarico e gia approvato; manca l'accesso
tecnico necessario alla loro pubblicazione.

### 39.2 Modifiche locali pronte

- PoseVerifier: scadenza inclusiva >= 2 s, rimozione di due variabili locali
  inutilizzate; cleanup che accetta la subscription gia rimossa nell'istanza
  isolata di prova. La subscription del normale planner resta invariata.
- timeout_probe.py: nodo isolato; rimuove solo la propria subscription prima
  dello spin. Avvia PoseVerifier senza campioni, attende la notifica False,
  osserva altri 3 s e verifica notifica unica, timer cancellato, nessun campione
  e nessuna richiesta FK/validita. Watchdog indipendente per non attendere
  indefinitamente. Cleanup in finally, nessuna action o classe di esecuzione.
- tcp_geometry.py: trasformazioni rigide, quaternion ROS xyzw normalizzati,
  composizione/inversa, conversioni mano-TCP e parsing di catene URDF fisse.
  Nessun offset Panda presunto. Catene mobili o link assenti sono rifiutati.
- robot_reference.py: lettura offline dei due dump, confronto della cinematica,
  controllo della catena SRDF panda_arm, report di mano/dita e candidati TCP
  esistenti. La selezione di un TCP richiede un nome esplicito e una catena
  fissa esistente; il report non prova la geometria dei polpastrelli.
- setup.py: aggiunti gli eseguibili timeout_probe e robot_reference.
- package.xml: dipendenza python3-yaml per leggere i dump.
- Test, README, .gitignore e RoboCell/docs/VERIFICA-TIMEOUT-TCP.md aggiunti.

Non e stato modificato il controllo del movimento in PosePlanner/MotionExecution
e non sono state ripetute le prove della scena o le prove positive nella demo.

### 39.3 Verifiche locali effettivamente eseguite

Python 3.12 Windows, unittest: **36 test passati**.

- 19 test sulla classe PoseVerifier importata integralmente con sostituti ROS
  limitati al caricamento del modulo: clock ROS/steady distinti, timeout alla
  soglia esatta, campioni vecchi/futuri/incompleti/non finiti, servizi non pronti,
  errori di invio, risposte tardive o estranee, notifica singola e cleanup.
- 11 test geometrici: offset ruotato, mano verso il basso, orientamento TCP
  distinto dalla mano, ordine RPY, inversa/andata-ritorno, numeri invalidi,
  parsing di catene fisse e rifiuto di frame inventati o mobili.
- 6 test di confronto dei modelli con XML sintetico: accordo, divergenza,
  TCP esplicito/assente e dump mancanti/ambigui.

La compilazione sintattica di tutti i moduli e test e riuscita. ROS/rclpy non
e disponibile nell'ambiente Windows: test_timeout_ros.py e timeout_probe non
sono stati eseguiti sul middleware reale. pytest non e installato qui; i test
unitari sono eseguibili con unittest, senza tale dipendenza. Non si dichiarano
passati i linter ROS del template o la presa fisica.

### 39.4 Comandi WSL per il timeout gia implementato

Eseguire nello stesso terminale WSL; il workspace nuovo evita di sovrascrivere
i sorgenti originali. Il probe non richiede la demo e non comanda movimenti.

```bash
source /opt/ros/jazzy/setup.bash
ROBOCELL_VERIFY_WS=$(mktemp -d /home/matteo/robocell_verify.XXXXXX)
mkdir "$ROBOCELL_VERIFY_WS/src"
cp -a "/mnt/c/Users/matte/Documents/Codex/2026-10-05/vor/outputs/vision-sort-lab/RoboCell/vision_sort_lab" "$ROBOCELL_VERIFY_WS/src/"
cd "$ROBOCELL_VERIFY_WS"
colcon build --symlink-install --packages-select vision_sort_lab
source "$ROBOCELL_VERIFY_WS/install/setup.bash"
python3 -c "import vision_sort_lab.pose_verifier as m; print(m.__file__)"
python3 -m unittest discover -s "$ROBOCELL_VERIFY_WS/src/vision_sort_lab/test" -p '*_unit.py' -v
ros2 run vision_sort_lab timeout_probe
echo $?
```

Import dal workspace nuovo, Ran 36 tests / OK, TIMEOUT PASS con notifiche=1,
risultato=False e FK/validita/movimenti=0, nessun traceback e codice finale 0.
Il log ERROR Timeout scaduto e intenzionale: e il risultato negativo atteso
dal verificatore. Il test complessivo dura circa cinque secondi.

### 39.5 Dati ancora necessari per completare il TCP

Richiesti i dump /move_group e /robot_state_publisher effettivamente attivi,
da pubblicare in docs/robot_reference. I comandi di acquisizione sono in 38.3;
e stato indicato anche /home/matteo/robot_reference come cartella comoda fuori
dal workspace. Nessuno dei due file risultava presente nella repository al
controllo corrente. Le descrizioni lette in passato non bastano per attribuire
al robot attivo un offset o un frame TCP non verificato.

Rimangono: leggere il modello, scegliere punto e assi con motivazione geometrica,
completare configurazione e controllo TCP su dati aggiornati TF/FK, pubblicare
le modifiche e dare qui i comandi finali corrispondenti. Solo dopo questi
checkpoint si inizia a collegare Gazebo con Matteo alla scrittura del codice.

**Stato:** implementazione locale verificata per i blocchi indipendenti dai dati
del robot; entrambi i passi complessivi non sono ancora dichiarati conclusi.
In attesa dell'accesso di pubblicazione e dei dump. GUIDA e PERCORSO aggiornati.

### 39.6 Accesso completato e primi dati del robot ricevuti

Matteo conferma l'accesso GitHub. Verifica effettiva riuscita con gh api user:
account Matteo7100. Creato il ramo codex/verification-tcp dal commit
770a596c5a9f3fce723ea12a6ace41ea08dd7ddf; le modifiche saranno basate sul main
aggiornato, preservando i caricamenti successivi dell'utente.

I dump sono ora in docs/robot_reference dopo gli spostamenti del main al commit
6a7eef02456f16a80bb059047d39b71c15786042. Il dump robot_state_publisher contiene
il modello completo; quello move_group contiene soltanto ros__parameters: {}.
Non permette quindi ancora il confronto tra il robot di MoveIt e il publisher TF.

Dati osservati dal modello del publisher: panda_link8->panda_hand fisso con
traslazione nulla e yaw -0.785398163397; entrambe le dita hanno origine z=0.0584 m,
assi opposti Y, corsa del singolo dito 0..0.04 m e seconda dita mimic della prima.
Nessun link TCP dedicato e presente. Le mesh delle dita rimandano al pacchetto
moveit_resources_panda_description sotto /opt/ros/jazzy.

Richiesta acquisizione diretta dei parametri XML robot_description e
robot_description_semantic di /move_group con ros2 param get --hide-type, da
caricare come move_group.urdf e move_group.srdf. Conferma «fatto» ricevuta;
alla prima rilettura nativa GitHub i due file non risultavano ancora presenti.

Aggiunto un workflow GitHub Actions con container ufficiale
ros:jazzy-ros-base-noble: build, test unitari e test del timer rclpy reale senza
robot, controllori o servizi MoveIt. L'esito resta da osservare dopo il push.
Questo permette di verificare autonomamente il ramo temporale su ROS Linux;
la prova WSL specifica dell'utente rimane distinta.
