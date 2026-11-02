# RoboCell / Vision Sort Lab

Pacchetto didattico ROS 2 Jazzy per il Panda con MoveIt. Il pacchetto ROS e
`vision_sort_lab`; la repository contiene la cartella completa del pacchetto,
non `build`, `install` o `log` del workspace.

La pipeline positiva di pianificazione, controllo endpoint, ExecuteTrajectory
e verifica su un campione aggiornato e gia stata osservata nella demo mock.
La fase successiva chiude il ramo di timeout e definisce il TCP prima di
iniziare Gazebo Harmonic.

Le modifiche preparate il 2 novembre 2026 includono:

- `timeout_probe`: test ROS isolato, senza ricevere stati e senza movimenti;
- 36 test unitari per PoseVerifier, trasformazioni e confronto dei modelli;
- `tcp_geometry`: conversione completa tra TCP e link della mano;
- `robot_reference`: confronto offline dei modelli realmente caricati.

Stato: 36 test unitari passati su Python 3.12 Windows. Aggiunto un job GitHub
Actions per eseguire anche il timer reale in ROS Jazzy, ancora da confermare.
Il TCP specifico del Panda non e ancora definito: il dump ricevuto da
robot_state_publisher e completo, ma quello di move_group e vuoto.
Non e stato comandato un nuovo movimento.

Le istruzioni riproducibili sono in [docs/VERIFICA-TIMEOUT-TCP.md](docs/VERIFICA-TIMEOUT-TCP.md).
La guida generale e [GUIDA-PROGETTO.md](GUIDA-PROGETTO.md); la mappa sintetica
e [PERCORSO.md](PERCORSO.md).
