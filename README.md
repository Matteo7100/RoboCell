# RoboCell / Vision Sort Lab

Cella di smistamento simulata per il braccio Panda, sviluppata con ROS 2 Jazzy, MoveIt 2 e Gazebo Harmonic. Il pacchetto ROS 2 si chiama `vision_sort_lab`.

## Percezione RGB-D

La camera osserva il tavolo dall’alto. Il probe individua i pezzi rossi e misura lunghezza e larghezza sulla faccia superiore. Quando il bordo inferiore è compatibile con il piano d’appoggio, il probe stima anche l’altezza e il centro volumetrico nel frame `world`. Se l’appoggio è nascosto e il piano osservato è incompatibile con il bordo, segnala `MISURA_INCERTA`.

Le prove in Gazebo comprendono un cubo sul tavolo, un parallelepipedo ruotato e un cubo su un rialzo nascosto. Nel test del parallelepipedo da 80 × 40 × 30 mm a 120°, il probe ha misurato 79,98 × 39,98 × 30,00 mm e uno yaw di 119,98°. Il prossimo esperimento riguarda il contrasto del canale V tra la faccia superiore e i fianchi visibili.

### Avvio del probe

Per una workspace già compilata, carica in entrambi i terminali l’ambiente ROS 2 Jazzy e l’overlay della workspace. Dalla radice della repository, avvia Gazebo nel primo terminale.

```bash
ros2 launch "$PWD/vision_sort_lab/launch/panda_gazebo_rgb.launch.py"
```

Nel secondo terminale, con la simulazione in esecuzione, acquisisci un’osservazione RGB-D.

```bash
ros2 run vision_sort_lab red_image_probe --ros-args -p use_sim_time:=true
```

Il punto di ingresso è [red_image_probe.py](vision_sort_lab/vision_sort_lab/red_image_probe.py). Il nodo, la proiezione dei pixel in 3D, la stima dei piani e il calcolo della geometria sono nel [sottopacchetto perception](vision_sort_lab/vision_sort_lab/perception/).

## Guide e verifiche

- La guida raccoglie esercizi e risultati delle verifiche sul Panda. [Guida al progetto](GUIDA-PROGETTO.md)
- La mappa del percorso descrive le tappe di sviluppo a partire da MoveIt. [Percorso guidato](PERCORSO.md)
- Le verifiche del timeout e del TCP confrontano cinematica diretta e TF. Il TCP nominale è a 0,1034 m lungo l’asse Z di `panda_hand`. La verifica storica in CI comprende 42 test unitari e 4 test ROS. [Procedura](docs/VERIFICA-TIMEOUT-TCP.md) · [Risultati CI](https://github.com/Matteo7100/RoboCell/actions/runs/41496585807)
