# VECROS_INTERN_ASSIGNMENT
Robotics Intern Assignment solution for Problem statements 1 & 2.


## Pre-requisites for PS-2
- Ubuntu-22.04 LTS Desktop
- ArduPilot-SITL
- Python3.10

## Setup instructions for PS-2
I'm using ArduPilot SITL to simulate the drone environment and Dronekit to send commands to the drone which is based on MAVLink (Pymavlink).

- Clone ardupilot repo 
```
cd ~
git clone https://github.com/ArduPilot/ardupilot.git
```
- Install dependencies for your system
```
cd ~/ardupilot
Tools/environment_install/install-prereqs-ubuntu.sh -y
```

- Checkout to latest Copter Build & update the modules
```
cd ~/ardupilot
. ~/.profile
git checkout Copter-4.5
git submodule update --init --recursive
```

- Run the SITL (Making sure you are in ArduCopter direc)
```
cd ~/ardupilot/ArduCopter
sim_vehicle.py -v ArduCopter
```
***NOTE:***
- In case you fine errors like `sim_vehicle.py : command not found`, then run this command :
```
echo "export PATH=$PATH:$HOME/ardupilot/Tools/autotest:$HOME/.local/bin" >> ~/.bashrc
```

- Allowing multiple UDP out ports for SITL:    

    - By default the Copter-4.5 build out only 1 udp port for conneciton.
    
    - You can check this by running this command:    
        ```
        sim_vehicle.py -v ArduCopter
        ```
        and if see the selected content of the log data, you can see there is only 1 --out udp port

        <div align="center">
        <img src="drone_missions/media/sitl_default_copter4.5.png" alt="Turn windows features on or off" />
        </div>
    
    - You can use this out port to connect direcltly to the SITL using Pymavlink(low level) script.
    
    - But to connect your dronekit library, you need add one more udp out port.
    
    - To do this, go to `ardupilot/Tools/autotest/sime_vehicle.py` and comment line no. *883* from this    

        ```python
        ports = [14550 + 10 * i]
        ``` 
        and use this inplace of that
        ```python
        ports = [p + 10 * i for p in [14550, 14551]]
        ```
    - Now if you run the sitl, you will see 2 --out udp ports

        <div align="center">
        <img src="drone_missions/media/sitl_copter4.5_for_dronekit.png" alt="Turn windows features on or off" />
        </div>


## Running PS-2 solution

- Clone this repo in your system:
```
cd ~
git clone https://github.com/ab31mohit/VECROS_INTERN_ASSIGNMENT.git
```
- Start the SITL (with MAVProxy console & map) in terminal:
```
sim_vehicle.py -v ArduCopter --console --map
```
Wait until the log data on MAVProxy console shows `EKF is using GPS` or soemthing similar.    

Btw you can change the default SITL map location to anything you want to (make sure that location has enough open space). Follow this line for more info - [change default sitl location](https://ardupilot.org/dev/docs/using-sitl-for-ardupilot-testing.html#setting-vehicle-start-location:~:text=Setting%20vehicle%20start,locations.txt%0Afile).

- Now run the script to upload First mission (of 15 waypoints) to drone in another terminal:
```
cd ~/VECROS_INTERN_ASSIGNMENT/drone_missions/
python3 mission1.py
```
