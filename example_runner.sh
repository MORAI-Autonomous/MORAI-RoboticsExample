#!/bin/bash
gnome-terminal -- sh -c 'roslaunch rosbridge_server rosbridge_websocket.launch; exec bash'
sleep 2
python3 src/MORAI-EXAMPLE/EgoCtrl/scripts/lib/launcher.py

mapping=$(niet example.mapping example_config.yaml)
echo "Mapping mode is ${mapping} mode."
mapping=${mapping,,}
if [[ $mapping == 3d ]]; then
  echo "Run LeGO-LOAM"
  gnome-terminal -- sh -c 'roslaunch lego_loam run.launch; exec bash'
  rviz='Off'
elif [[ $mapping == 2d ]]; then
  echo "Run 2D Grid-mapping"
  gnome-terminal -- sh -c 'roslaunch ogm run.launch; exec bash'
  rviz='Off'
else
  echo "No-mapping"
  rviz='On'
fi

moving=$(niet example.moving example_config.yaml)
echo "Moving mode is ${moving} mode."
moving=${moving,,}
if [[ $moving == cruise ]]; then
  roslaunch ego_ctrl ego_ctrl.launch mode:=$moving
elif [[ $moving == auto ]]; then
  roslaunch ego_ctrl ego_ctrl.launch mode:=$moving
  sleep 2
  gnome-terminal -- sh -c "roslaunch morai_standard morai_standard.launch rviz:=$rviz; exec bash"
  
else
  roslaunch ego_ctrl ego_ctrl.launch mode:=$moving
fi
echo -n "Press any key to stop"
read
roslaunch ego_ctrl ego_ctrl.launch mode:=keyboard
echo "See you!"
lm_ps=$(ps -ef | grep "roslaunch lidar2d_mapping run.launch; exec bash$")
lm_cmd=$(echo ${lm_ps} | cut -d " " -f2 )
if [ -n "${lm_cmd}" ]
then
        result=$(kill -9 ${lm_cmd})
        echo process is killed.
else
        echo running process not found.
fi
ad_ps=$(ps -ef | grep "roslaunch morai_standard morai_standard.launch rviz:=$rviz; exec bash$")
ad_cmd=$(echo ${ad_ps} | cut -d " " -f2 )
if [ -n "${ad_cmd}" ]
then
        result=$(kill -9 ${ad_cmd})
        echo process is killed.
else
        echo running process not found.
fi
rb_ps=$(ps -ef | grep 'roslaunch rosbridge_server rosbridge_websocket.launch; exec bash$')
rb_cmd=$(echo ${rb_ps} | cut -d " " -f2 )
if [ -n "${rb_cmd}" ]
then
        result=$(kill -9 ${rb_cmd})
        echo process is killed.
else
        echo running process not found.
fi
ll_ps=$(ps -ef | grep 'roslaunch lego_loam run.launch; exec bash')
ll_cmd=$(echo ${ll_ps} | cut -d " " -f2 )
if [ -n "${ll_cmd}" ]
then
        result=$(kill -9 ${ll_cmd})
        echo process is killed.
else
        echo running process not found.
fi