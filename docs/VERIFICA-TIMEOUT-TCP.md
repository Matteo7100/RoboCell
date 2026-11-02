# Verifiche prima di Gazebo

## Stato del checkpoint del 2 novembre 2026

Base letta da GitHub: `d0a779fb13b6f9faf677d2486586d5b6dc2f7c91`.
Le modifiche sono preparate sul ramo `codex/verification-tcp`, con successiva
pubblicazione tramite GitHub CLI. Il connettore iniziale aveva rifiutato la
creazione del ramo con 403. Un clone di `main` non contiene queste modifiche
finche la relativa PR non viene unita.

36 test unitari passati in locale. Sono usati clock e servizi sostitutivi nei
test di PoseVerifier; non e una prova del middleware ROS o del simulatore.
La compilazione sintattica di tutti i moduli e dei test e riuscita.
Il test reale ROS non e eseguibile in questo ambiente Windows. E aggiunto
un job GitHub Actions con il container ROS Jazzy e test_timeout_ros.py;
il suo esito verra registrato dopo la prima esecuzione.

## Eseguire la copia locale in WSL

Questo percorso permette gia di provare il timeout senza attendere il push.
Usare un solo terminale WSL per mantenere la variabile del nuovo workspace.
Il workspace temporaneo ha un nome nuovo: i sorgenti precedenti restano
disponibili. Non avviare PosePlanner per questo test. La demo puo rimanere
attiva, ma non e necessaria al timeout.

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
```

Il percorso importato deve appartenere al nuovo workspace o alla sua sorgente
tramite symlink. Non deve indicare il vecchio workspace `vision_sort_ws`.
I test unitari devono riportare `Ran 36 tests` e `OK`.

Il probe impiega circa cinque secondi: due di deadline e tre di osservazione.
Il log ERROR `Timeout scaduto` e l'esito negativo intenzionale della verifica.
L'esito positivo del **test** e:

```text
TIMEOUT PASS | notifiche=1 | risultato=False | durata=2.xxx s | osservazione_successiva=3 s | FK=0 | validita=0 | movimenti=0
```

Il processo deve chiudersi senza traceback e con codice zero. Dopo il comando
si puo controllare `echo $?`. Nessun servizio di MoveIt e nessuna action vengono
richiesti dal probe. Viene rimossa soltanto la subscription della sua istanza;
il publisher `/joint_states` della demo continua normalmente.

In un ambiente che dispone di pytest, il medesimo test ROS e anche disponibile
come `test/test_timeout_ros.py`. Non occorre eseguirlo di nuovo se il comando
`timeout_probe` e gia passato. I test di stile generati dal template ROS non
sono stati riscritti o dichiarati passati per questa modifica.

## Acquisire il modello effettivo

Con la demo Panda attiva, da un terminale che vede il suo grafo ROS:

```bash
source /opt/ros/jazzy/setup.bash
source /home/matteo/vision_sort_ws/install/setup.bash
mkdir -p /home/matteo/robot_reference
ros2 param dump /move_group > /home/matteo/robot_reference/move_group.params.yaml
ros2 param dump /robot_state_publisher > /home/matteo/robot_reference/robot_state_publisher.params.yaml
```

Pubblicare i due file in `docs/robot_reference` della repository. Nel terminale
del nuovo workspace, dopo aver acquisito i file, si puo gia produrre il report:

```bash
ros2 run vision_sort_lab robot_reference --move-group /home/matteo/robot_reference/move_group.params.yaml --state-publisher /home/matteo/robot_reference/robot_state_publisher.params.yaml
```

Il comando confronta nomi dei link, origini, assi, limiti e relazioni dei giunti,
legge il gruppo SRDF `panda_arm` e descrive riferimenti e geometrie delle dita.
Non prova l'uguaglianza delle mesh o la presa fisica. Non seleziona automaticamente
un link perche il suo nome contiene `tcp` e non sceglie un offset numerico.

Primo caricamento ricevuto al commit 770a596c5a9f3fce723ea12a6ace41ea08dd7ddf:
file in `robot_reference/docs`, dump robot_state_publisher completo, dump
move_group vuoto (`ros__parameters: {}`). Quest'ultimo non permette il confronto.
Per recuperare direttamente i due parametri con la demo attiva:

```bash
ros2 param get --hide-type /move_group robot_description > /home/matteo/robot_reference/move_group.urdf
ros2 param get --hide-type /move_group robot_description_semantic > /home/matteo/robot_reference/move_group.srdf
```

I file devono contenere XML valido. `None` o `Parameter not set` non sono un
modello utilizzabile e richiedono prima una verifica del nodo attivo.

`--tcp-link NOME` e accettato solo per un link gia esistente e collegato alla
mano da una catena fissa, da esaminare prima dell'adozione come punto di presa.

## Convenzione geometrica gia implementata

`T_A_B` e la posa del riferimento B espressa in A. La definizione del TCP sara
`T_hand_tcp`. Si usano metri e quaternion nell'ordine ROS `(x, y, z, w)`.

```text
T_base_tcp  = T_base_hand * T_hand_tcp
T_base_hand = T_base_tcp  * inverse(T_hand_tcp)
```

Gli assi e la traslazione del TCP saranno fissati dopo la lettura del modello.
I valori da 10 cm usati nei test sono esempi sintetici, non misure del Panda.
Il parser rifiuta frame assenti e catene contenenti giunti mobili. I test coprono
anche una mano rivolta in basso e orientamenti TCP diversi da quelli della mano.

Resta da completare: scelta documentata del punto fra le dita, configurazione
specifica e verifica TF/FK coerente sul robot corrente. I relativi comandi
saranno aggiunti quando il TCP e davvero implementato, prima di Gazebo.

Riferimenti API verificati: [timer rclpy Jazzy](https://github.com/ros2/rclpy/blob/jazzy/rclpy/rclpy/timer.py),
[gestione risorse Node Jazzy](https://github.com/ros2/rclpy/blob/jazzy/rclpy/rclpy/node.py),
[parser joint URDF](https://github.com/ros/urdfdom/blob/master/urdf_parser/src/joint.cpp).
