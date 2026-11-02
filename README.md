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
- 42 test unitari per PoseVerifier, trasformazioni e confronto dei modelli;
- `tcp_geometry`: conversione completa tra TCP e link della mano;
- `robot_reference`: confronto offline dei modelli realmente caricati.
- `panda_tcp`: riferimento nominale e conversioni dei target TCP/mano;
- `tcp_probe`: controllo FK/TF su un campione aggiornato e frame RViz opzionale.

Stato: 42 test unitari passati su Python 3.12 Windows. Il timeout reale ROS
Jazzy e gia riuscito in GitHub Actions: 2.001 s, una sola notifica False,
altri 3 s senza duplicati. La cinematica dei modelli caricati coincide.
Il TCP nominale e (0,0,0.1034) m da panda_hand, con gli stessi assi.
La suite ROS completa e passata: build, 42 test unitari, 4 test ROS, confronto
modelli e controllo della mesh. [Risultati CI](https://github.com/Matteo7100/RoboCell/actions/runs/41496585807).
La verifica specifica sul Panda in WSL usa i comandi documentati sotto.
Non e stato comandato un nuovo movimento.

Le istruzioni riproducibili sono in [docs/VERIFICA-TIMEOUT-TCP.md](docs/VERIFICA-TIMEOUT-TCP.md).
La guida generale e [GUIDA-PROGETTO.md](GUIDA-PROGETTO.md); la mappa sintetica
e [PERCORSO.md](PERCORSO.md).
