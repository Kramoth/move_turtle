# move_turtle

## Installation
Pour installer ce package, dans le dossier source de votre catkin workspace faire un clone du package:
On supposera que votre catkin workspace s'appelle catkin_ws et se situe dans votre home, remplacer par le bon chemin suivant l'oragnisation de vos dossiers.

```sh
cd catkin_ws/src
git clone https://www.github.com/kramoth/move_pose.git
```

Puis compiler et sourcer le setup.bash
```sh
catkin build
source ~/catkin_ws/devel/setup.bash
```

# Utilisation

### Avec rosrun
Dans un terminal lancer le serveur ROS
```sh
roscore
```

Dans un second terminal, lancer le simulateur le turtlesim

```sh
rosrun turtlesim turtlesim_node
```

Dans un troisieme terminal 
```sh
source ~/catkin_ws/devel/setup.bash
rosrun move_turtle move_square.py /cmd_vel:=/turtle1/cmd_vel /pose:=/turtle1/pose _linear_speed:=4.0 _angular_speed:=0.5
```
Vous remarquerez que le carre decrit par la tortue derive, cela est du au fait que l'algorithme realise une commande par dead reckoning. Pour limiter l'effet de drift de la tortue il faudrait utiliser la pose de la tortue et mettre cette information dans une boucle de retro action pour realiser une regulation.

### Avec roslaunch

Dans un terminal:
```sh
source ~/catkin_ws/devel/setup.bash
roslaunch move_turtle square.launch
```
