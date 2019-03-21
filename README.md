#Thunderbird

## Dependencies
```
Ros-kinetc
Mavros Mavlink
Firmware

```



## offb_py
```
roscore

```

For real flight:
```

rosrun mavros mavros_node _fcu_url:=/dev/ttyUSB0:57600 _gcs_url:=udp://@172.16.254.1 
```


For simulation in gazebo:
```
cd src/Firmware
make px4_sitl_default gazebo
```

In new terminal:
```
roslaunch mavros px4.launch fcu_url:="udp://:14540@127.0.0.1:14557"

```

Run test program in new terminal
```
cd extra_ws
catkin_make
source devel/setup.bash
rosrun offb_py test_traj.py
```
 

