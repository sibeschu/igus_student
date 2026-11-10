- [Igus Student](#Igus-Student)
  - [Workspace herunterladen](#0-workspace-herunterladen)
  - [Workspace vorbereiten](#1-workspace-vorbereiten)
  - [Roboter und MoveIt starten](#2-roboter-und-moveit-starten)
    - [Simulation](#simulation)
    - [Echter Roboter](#echter-roboter)
  - [Erste Schritte](#erste-schritte)
    - [Wo schreibe ich Code?](#wo-schreibe-ich-code)
  - [Grundlegende Funktionen](#grundlegende-funktionen)
    - [`move_and_wait(x, y, z, roll, pitch, yaw)`](#move_and_waitx-y-z-roll-pitch-yaw)
    - [`igus.move_ee_vertical(node-node-delta_z-float--01)`](#igusmove_ee_verticalnode-node-delta_z-float--01)
  - [Kamera und Punktwolken](#kamera-und-punktwolken)
    - [Nodes](#nodes)
    - [Topics](#topics)
  - [Startposition](#startposition)
  - [Fehlerbehebung](#fehlerbehebung)
    - [Problem: NOT-AUS](#problem-not-aus)
    - [Problem: "move_group server not available"](#problem-move_group-server-not-available)
    - [Problem: Roboter bewegt sich nicht](#problem-roboter-bewegt-sich-nicht)
    - [Problem: Timeout beim Warten auf Bewegung](#problem-timeout-beim-warten-auf-bewegung)
  - [Koordinatensystem](#koordinatensystem)
    - [Kartesische Koordinaten (X, Y, Z)](#kartesische-koordinaten-x-y-z)
    - [Orientierung (Roll, Pitch, Yaw)](#orientierung-roll-pitch-yaw)
  - [Misc](#Misc)
    - [Kamera installieren / inbetriebnehmen](#kamera-installieren--inbetriebnehmen)

# Igus Student

### 0. Workspace herunterladen

```bash
git clone https://github.com/sibeschu/igus_student.git
```

### 1. Workspace vorbereiten

```bash
# In das Workspace-Verzeichnis navigieren
cd ~/igus_student

# Den Workspace bauen
colcon build --symlink-install

# --symlink-install erzeugt einen symbolischen Link zu den src-Dateien
# ohne --symlink-install muss man nach jeder Änderung erneut über colcon build bauen

# Workspace aktivieren
source install/setup.bash
```

### 2. Roboter und MoveIt starten

Bevor du dein Programm startest, musst du den Roboter und MoveIt starten:

#### Simulation

```bash
# Terminal 1: Robotersimulation starten
ros2 launch igus_rebel_moveit_config igus_rebel_simulated.launch.py

# Terminal 2: Dein Student-Programm
ros2 run igus_student student_control
```

#### Echter Roboter

```bash
# Terminal 1: Roboter verbinden
ros2 launch igus_rebel rebel.launch.py

# Terminal 2: Motion planner starten
ros2 launch igus_rebel_moveit_config igus_rebel_motion_planner.launch.py use_gui:=true

# Terminal 3: Dein selbstgeschriebenes Programm starten
ros2 run igus_student student_control
```

## Erste Schritte

### Wo schreibe ich Code?

```bash
igus_student
└── src
    ├── igus_student
    │   ├── igus_student
    │   │   └── student_control.py # <── Einstieg hier
    ├── igus_student_msgs
    └── igus_rebel_ros2
```


## Grundlegende Funktionen

### `move_and_wait(x, y, z, roll, pitch, yaw)`
```python 
move_and_wait(x, y, z, roll, pitch, yaw)
```

Bewegt den Roboter zu einer bestimmten Position und wartet, bis er dort angekommen ist.

**Parameter:**
- `x, y, z` (float): Kartesische Koordinaten in Metern (relativ zur Basis)
- `roll, pitch, yaw` (float): Orientierung in Radiant (Euler-Winkel)

**Beispiel:**
```python
# Roboter zu Position (0.4, 0.2, 0.3) mit Orientierung (~π, 0, 0) bewegen
_robot.move_and_wait(0.4, 0.2, 0.3, 3.14, 0.0, 0.0)
```

### `igus.move_ee_vertical(node: Node, delta_z: float = 0.1)`
```python
igus.move_ee_vertical(node: Node, delta_z: float = 0.1)
```

Bewegt den Roboter 0.1m in z-Richtung.

**Parameter:**
- `node` (Node): Node des zu steuernden Objektes.
- `delta_z` (float): Distanz in Meter, welche in Z-Richtung verfahren werden soll.

**Beispiel:**
```python
# Roboter um 0.1m nach oben fahren
igus.move_ee_vertical(_robot, delta_z=0.1)
```

## Kamera und Punktwolken

### Nodes
```bash
# Node mit Blob-Detektor
ros2 run igus_student puck_opencv

# Node nimmt detektierte Punkte und überführt 2D zu 3D Punkten
ros2 run igus_student puck_2d_to_3d

```

### Topics

Verfügbare Topics sind : 

```bash
/puck_2d_coords
/puck_3d_markers
/puck_3d_points
/puck_3d_points_world
/puck_debug_image
```

Die Punkte in /puck_3d_points in der eigenen Node zu subscriben (siehe Dokumentation ROS2 Jazzy) und mittels dieser Punkte später eine Pfadplanung zu machen. Dabei können diese beliebig weggespeichert werden, da die Pucks sich im Idealfall ja nicht bewegen werden.

Siehe "subscriber_example.py". Gerne kann vergleichbare Funktionalität auch in student_control.py übernommen werden, um den Überblick zu behalten.

[Writing a simple .py publisher and subscriber](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Publisher-And-Subscriber.html)

[Beispiele für Subscriber Nodes](https://github.com/ros2/examples/tree/jazzy/rclpy/topics)

Wie man eigene msg-Typen (Interfaces) anlegt. (Nicht erforderlich für Einführung Robotik)
[Custom ROS2 Interfaces](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Custom-ROS2-Interfaces.html)

## Startposition 

"Sorting" Position kann in src/igus_rebel_ros2/src/igus_rebel_moveit_config/config/igus_rebel2.srdf geändert werden. In dieser Datei einfach nach "sorting" suchen. Die Joint Positionen werden in RAD angegeben.

# Troubleshooting

### Problem: Dependencies fehlen (z.B. ros-gz-sim not found)
**Lösung**: 
```bash
cd igus_student
rosdep install --from-paths src -y --ignore-src
```

### Problem: Not-Aus


### Problem: "move_group server not available"

**Lösung:** Stelle sicher, dass der Motion planner läuft:
```bash
ros2 launch igus_rebel_moveit_config igus_rebel_motion_planner.launch.py use_gui:=true
```

### Problem: Roboter bewegt sich nicht

**Lösung:**
Überprüfe, ob die Zielposition im Arbeitsbereich des Roboters liegt.
**Lösung:** Überprüfe ob der Not-Aus Schalter betätigt ist. Falls ja, Not-Aus zurücksetzen und `rebel.launch.py` neustarten.

### Problem: Timeout beim Warten auf Bewegung

Dies kann auftreten wenn der Roboter die Zielposition nicht erreichen kann. Mögliche Ursachen:
- Position ist außerhalb des Arbeitsbereichs
- Roboter kann die Orientierung des Endeffektors nicht erreichen
- Kollision mit Hindernis erkannt

## Koordinatensystem

### Kartesische Koordinaten (X, Y, Z)

- **X-Achse:** Vorwärts/Rückwärts (in Meter)
- **Y-Achse:** Links/Rechts (in Meter)
- **Z-Achse:** Oben/Unten (in Meter)

### Orientierung (Roll, Pitch, Yaw)

Die Orientierung wird mit Euler-Winkeln in Radiant definiert:
- **Roll:** Rotation um die X-Achse
- **Pitch:** Rotation um die Y-Achse
- **Yaw:** Rotation um die Z-Achse

**Wichtige Konstanten:**
```python
import math

pi = math.pi
# Roll = π (180°) bedeutet: Roboter zeigt nach unten
# Roll = 0, Pitch = 0, Yaw = 0: Roboter zeigt nach oben
```

## Misc

### Kamera installieren / inbetriebnehmen

```bash
sudo apt install ros-jazzy-librealsense2*

sudo apt install ros-jazzy-realsense2-*

```