from dronekit import connect, VehicleMode, Command, LocationGlobalRelative
import time
import math


# Connect to the Vehicle
print("----Connecting to vehicle----")
vehicle = connect('udp:127.0.0.1:14550', wait_ready=True)

# Navigation parameters (in cm/s)
WPNAV_ACCEL = 250  # cm/s²
WPNAV_SPEED = 1000  # cm/s (10 m/s)
TAKEOFF_ALT = 10   # m


def get_distance_metres(aLocation1, aLocation2):
    """
    Returns the ground distance in metres between two LocationGlobal objects.
    """

    dlat = aLocation2.lat - aLocation1.lat
    dlong = aLocation2.lon - aLocation1.lon
    return math.sqrt((dlat * dlat) + (dlong * dlong)) * 1.113195e5  # Approximate distance in meters


def estimate_time_to_waypoint(distance, speed):
    """
    Calculate the instantaneous time required to reach the next waypoint
    using the current speed of the vehicle.
    """
    # instantaneous time required
    estimated_time_seconds = distance / speed  # Time (seconds)
    
    return estimated_time_seconds


def arm_and_takeoff(target_altitude):
    """
    Arms vehicle and flies to the target altitude.
    """
    print("Basic pre-arm checks")
    while not vehicle.is_armable:
        print("Waiting for vehicle to initialise...")
        time.sleep(1)
    
    print("\n----Arming motors----")
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True
    
    while not vehicle.armed:
        print("Waiting for arming")
        time.sleep(1)
    
    print("\n----Taking off----")
    vehicle.simple_takeoff(target_altitude)
    
    while True:
        current_alt = vehicle.location.global_relative_frame.alt
        print(f"[Altitude]: {current_alt:.2f} m")
        if current_alt >= target_altitude * 0.95:
            print(f"Reached target altitude of {TAKEOFF_ALT} m")
            break
        time.sleep(1)


def import_mission(filename):
    """
    Import mission from file and upload to vehicle
    """
    print(f"\n----Configuring Mission----")
    print(f"Reading mission from file: {filename}")
    cmds = vehicle.commands
    cmds.clear()
    
    with open(filename) as f:
        lines = f.readlines()
        
    # Skip first line (header)
    mission_items = [line.strip() for line in lines[1:]]
    
    for i, line in enumerate(mission_items):
        line_split = line.strip().split('\t')
        if len(line_split) == 12:
            lat = float(line_split[8])
            lon = float(line_split[9])
            alt = float(line_split[10])
            
            cmd = Command(0, 0, 0,
                        int(line_split[2]),    # frame
                        int(line_split[3]),    # command
                        0, 0,                  # current, autocontinue
                        float(line_split[4]),  # param1
                        float(line_split[5]),  # param2
                        float(line_split[6]),  # param3
                        float(line_split[7]),  # param4
                        lat, lon, alt)
            cmds.add(cmd)
    
    cmds.upload()
    print(f"Uploaded {len(mission_items) - 1} waypoints") # excluding the first row which represents the home location (not any waypoint)
    return len(mission_items)


def main():
    try:
        # Step 1: Takeoff
        arm_and_takeoff(TAKEOFF_ALT) 
      
        # Step 2: Import mission
        waypoint_count = import_mission('mission.txt')
        
        # Reset mission
        vehicle.commands.next = 0
        
        # Start mission
        print("\n---Starting Mission----")
        vehicle.mode = VehicleMode("AUTO")

        # Monitor mission progress
        last_waypoint = 0

        while True:
            current_wp = vehicle.commands.next            

            if (current_wp - last_waypoint) == 1:

                # Get the next waypoint's location
                next_waypoint = vehicle.commands[current_wp]
                current_location = vehicle.location.global_relative_frame

                next_location = LocationGlobalRelative(next_waypoint.x, next_waypoint.y, next_waypoint.z)
                distance = get_distance_metres(current_location, next_location)
                current_speed = abs(vehicle.groundspeed) 
                estimated_time = estimate_time_to_waypoint(distance, current_speed)

                print(f"[Navigating to waypoint {current_wp}]: estimated distance= {distance:.2f} m, estimated time= {estimated_time:.2f} s")
            
            if (current_wp - last_waypoint) == 2:
                print(f"Reached waypoint {current_wp-1}\n")
                last_waypoint += 1

                if current_wp == (waypoint_count - 1):
                    # Navigation to last waypoint is already started\
                    # print(f"[Navigating to waypoint {current_wp}]:")
                    break


            time.sleep(1)
        
        # Land at final waypoint
        print(f"\n----Landing at the final waypoint {current_wp}----")
        vehicle.mode = VehicleMode("LAND")
        
        # Monitor landing
        while vehicle.armed:
            current_alt = vehicle.location.global_relative_frame.alt
            print(f"[Landing]: Current altitude= {current_alt:.2f} m")
            if current_alt <= 0.1:
                break
            time.sleep(1)
        
        print("Landed successfully!")
        
    except KeyboardInterrupt:
        print("\nMission cancelled by user!")
        vehicle.mode = VehicleMode("LAND")
        print("Emergency landing initiated!.")
        
    finally:
        print("\n----Closing vehicle connection----")
        vehicle.close()


if __name__ == '__main__':
    main()
