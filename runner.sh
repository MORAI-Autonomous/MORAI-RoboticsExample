#!/bin/bash
exit_commands() {
  tmux kill-session -t rb
  tmux kill-session -t loam
  tmux kill-session -t ogm
  tmux kill-session -t auto
  exit
}

trap 'exit_commands' SIGINT
gedit ./config.yaml
source ~/catkin_ws/devel/setup.bash
tmux new -d -s rb 'source ~/catkin_ws/devel/setup.bash && roslaunch rosbridge_server rosbridge_websocket.launch; exec bash'
sleep 2
python3 src/MORAI-RoboticsExample/EgoCtrl/scripts/lib/launcher.py

mapping=$(niet example.mapping config.yaml)
echo "Mapping mode is ${mapping} mode."
mapping=${mapping,,}
if [[ $mapping == 3d ]]; then
  echo "Run 3D SLAM (LeGO-LOAM)"
  tmux new -d -s loam 'source ~/catkin_ws/devel/setup.bash && roslaunch lego_loam run.launch; exec bash'
  rviz='Off'
elif [[ $mapping == 2d ]]; then
  echo "Run 2D SLAM (Google Cartographer)"
  tmux new -d -s ogm 'source ~/catkin_ws/devel/setup.bash && roslaunch ogm_cartographer run.launch; exec bash'
  rviz='Off'
else
  echo "No-mapping"
  rviz='On'
fi

moving=$(niet example.moving config.yaml)
echo "Moving mode is ${moving} mode."
moving=${moving,,}
if [[ $moving == cruise ]]; then
  roslaunch ego_ctrl ego_ctrl.launch mode:=$moving
elif [[ $moving == auto ]]; then
  roslaunch ego_ctrl ego_ctrl.launch mode:=$moving
  sleep 2
  tmux new -d -s auto "source ~/catkin_ws/devel/setup.bash && roslaunch morai_standard morai_standard.launch rviz:=$rviz; exec bash"
  
else
  roslaunch ego_ctrl ego_ctrl.launch mode:=$moving
fi
echo -n "Press any key or Ctrl+C to stop"
read
roslaunch ego_ctrl ego_ctrl.launch mode:=keyboard
echo "See you!"

tmux kill-session -t rb
tmux kill-session -t loam
tmux kill-session -t ogm
tmux kill-session -t auto