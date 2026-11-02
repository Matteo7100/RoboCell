# Verifiche prima di Gazebo

Le modifiche sono nella [PR #1](https://github.com/Matteo7100/RoboCell/pull/1),
ramo codex/verification-tcp. Comprendono il test isolato del timeout e la
definizione nominale del TCP, senza nuovi movimenti o modifiche alla scena.

## Cosa e stato implementato

- timeout_probe: deadline steady di 2 s, una sola notifica False e altri 3 s
  senza notifiche duplicate. Distrugge solo la propria subscription; non
  interrompe il publisher della demo e non chiama servizi MoveIt o action.
- robot_reference: confronta i modelli esportati da MoveIt e dal publisher TF,
  legge la catena SRDF e riporta la convenzione TCP selezionata.
- tcp_probe: controlla geometria e mesh della pinza, acquisisce un campione
  nuovo, confronta FK e TF al suo esatto timestamp e calcola il TCP.
  Attende al massimo 8 s. Non pianifica e non comanda il robot.
- panda_tcp: definizione del punto e conversioni PoseStamped TCP/mano, con
  copia del messaggio e mantenimento di frame e timestamp.
- tcp_geometry: composizione/inversa delle trasformazioni e quaternion xyzw.

## Punto e assi scelti

Il riferimento virtuale vision_sort_tcp ha origine (0, 0, 0.1034) m rispetto
a panda_hand e quaternion (0, 0, 0, 1): assi identici alla mano.
Y e la direzione di apertura/chiusura; +Z va verso le estremita delle dita.
Le origini delle dita sono a z=0.0584 m; il TCP si trova quindi 45 mm oltre
tali origini, sulla mezzeria fra le dita nella zona dei polpastrelli.

E una convenzione geometrica nominale esplicita. Non viene dichiarato un link
TCP preesistente, una calibrazione reale o una presa fisica verificata.
La pinza ha aperture simmetriche solo quando il mimic tra le dita e rispettato.
Il probe verifica le ipotesi del modello e la mesh collisionale installata.

Fonte della convenzione: [franka_robot.xacro](https://github.com/frankarobotics/franka_ros/blob/ddd2fffd9de44b02ad15b4bbb2bfa2cec4d60d98/franka_description/robots/common/franka_robot.xacro).
Mesh esaminata: [finger.stl](https://github.com/moveit/moveit_resources/blob/ros2/panda_description/meshes/collision/finger.stl),
Git blob 3b87289fea8128bcec3e0b4d174b169124e8e444, 32 triangoli.
Il parametro TCP nominale del sorgente Franka e usato come riferimento
geometrico; il progetto continua a usare ROS 2 Jazzy.

Le conversioni sono:
~~~
T_base_tcp  = T_base_hand * T_hand_tcp
T_base_hand = T_base_tcp  * inverse(T_hand_tcp)
~~~
L'offset viene ruotato con la mano. Con un TCP verso il basso a z=0.02 m,
panda_hand deve essere a z=0.1234 m, non a z=0.02 m.
Il planner esistente continua a controllare panda_hand. Per i futuri target
TCP si usa tcp_target_to_hand; per una posa raggiunta della mano si usa
hand_pose_to_tcp. Il frame virtuale non va richiesto a FK come link URDF.

## Installare il ramo in un nuovo workspace WSL

Lasciare la demo Panda gia aperta. Eseguire tutti i blocchi seguenti nello
stesso nuovo terminale WSL, mantenendo le variabili. Il workspace ha un nome
nuovo; non vengono sovrascritti i sorgenti precedenti.

~~~bash
source /opt/ros/jazzy/setup.bash
ROBOCELL_WS=$(mktemp -d /home/matteo/robocell_verify.XXXXXX)
mkdir "$ROBOCELL_WS/src"
ROBOCELL_REPO="$ROBOCELL_WS/src/RoboCell"
git clone --branch codex/verification-tcp --single-branch https://github.com/Matteo7100/RoboCell.git "$ROBOCELL_REPO"
cd "$ROBOCELL_WS"
colcon build --symlink-install --packages-select vision_sort_lab --allow-overriding vision_sort_lab
source "$ROBOCELL_WS/install/setup.bash"
git -C "$ROBOCELL_REPO" log -1 --oneline
python3 -c "import vision_sort_lab.pose_verifier as m; print(m.__file__)"
~~~

Il percorso importato deve appartenere al nuovo workspace o alla sua sorgente
tramite symlink, non al vecchio vision_sort_ws.
Se la demo non e aperta, avviarla da un altro terminale:
~~~bash
source /opt/ros/jazzy/setup.bash
ros2 launch moveit_resources_panda_moveit_config demo.launch.py
~~~

## 1. Test unitari e timeout senza movimento

~~~bash
python3 -m unittest discover -s "$ROBOCELL_REPO/vision_sort_lab/test" -p '*_unit.py' -v
ros2 run vision_sort_lab timeout_probe
echo $?
~~~

Attesi: Ran 42 tests / OK; dopo circa cinque secondi TIMEOUT PASS con
notifiche=1, risultato=False, durata intorno a 2 s, osservazione_successiva=3 s
e FK=0, validita=0, movimenti=0. Il log ERROR Timeout scaduto e intenzionale.
Il processo chiude senza traceback e con codice zero.

## 2. Confronto dei modelli e TCP nominale

~~~bash
ros2 run vision_sort_lab robot_reference --move-group "$ROBOCELL_REPO/docs/robot_reference/move_group.urdf" --semantic "$ROBOCELL_REPO/docs/robot_reference/move_group.srdf" --state-publisher "$ROBOCELL_REPO/docs/robot_reference/robot_state_publisher.params.yaml" --nominal-panda-tcp
ros2 run vision_sort_lab tcp_probe --model "$ROBOCELL_REPO/docs/robot_reference/robot_state_publisher.params.yaml"
echo $?
~~~

Il report deve contenere kinematics_match=true, chain_tip=panda_link8,
tcp_definition.frame=vision_sort_tcp e xyz_m=[0,0,0.1034].
Si usano i due XML acquisiti direttamente: il primo move_group.params.yaml
vuoto resta soltanto una traccia diagnostica e non e usato nella verifica.

Con la demo attiva, il probe deve riportare TCP PASS, stamp aggiornato,
FK-TF entro 1 mm e 0.001 rad, posizione del TCP in panda_link0 e movimenti=0.
Queste tolleranze confrontano FK e TF, non sostituiscono i vincoli di posa
del planner. Il codice finale deve essere zero.

Se mancano stati nuovi, TF allo stesso istante o servizio FK, il probe conclude
con TCP FAIL dopo 8 s e codice nonzero. Mesh o geometria diverse fanno fallire
il controllo preliminare con una causa esplicita.

## Vedere il TCP in RViz

Facoltativo, nello stesso terminale configurato:
~~~bash
ros2 run vision_sort_lab tcp_probe --model "$ROBOCELL_REPO/docs/robot_reference/robot_state_publisher.params.yaml" --show
~~~

Dopo TCP PASS il processo rimane attivo. In RViz aggiungere il display TF e
abilitare vision_sort_tcp; usando Fixed Frame panda_link0 si vede l'origine
fra le dita, nella regione dei polpastrelli. Il robot non viene mosso.
Ctrl+C chiude il processo che pubblica il riferimento virtuale.

## Prove automatiche e limiti

Suite finale [GitHub Actions](https://github.com/Matteo7100/RoboCell/actions/runs/41496585807)
riuscita sul codice d081a28dbd9d503547128e4e4e44896a6c4ccd8f: build, 42 test
unitari e 4 ROS passati; confronto modelli e mesh installata riusciti.
Timeout osservato 2.001 s; il probe sintetico ha FK-TF=0 e TCP z=0.4966 m per
una mano rivolta in basso a z=0.6 m. Queste coordinate appartengono al test,
non sono la posa richiesta al Panda della WSL.

42 test unitari sono eseguibili anche senza ROS tramite unittest.
I test ROS richiedono rclpy e usano un container Jazzy nel workflow:
- timer reale PoseVerifier: scadenza, risultato unico e cleanup;
- probe TCP con FK/TF sintetici, compreso arrivo ritardato di TF;
- rifiuto di un frame FK errato;
- scadenza del probe senza stati;
- confronto dei modelli caricati e hash della mesh Panda installata.

I test sintetici verificano il software e il middleware; l'output del probe
sul Panda della WSL resta il controllo specifico dell'installazione dell'utente.
Non vengono ripetute prove della scena o eseguite nuove traiettorie.
I linter del template ROS non sono inclusi in questa suite mirata.

Dopo l'esito positivo dei due comandi finali in WSL si puo iniziare a collegare
Gazebo Harmonic. Il TCP andra mantenuto coerente nel modello usato dal simulatore.
