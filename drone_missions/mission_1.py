from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
import math

# Connect to the Vehicle
print("Connecting to vehicle...")
vehicle = connect('udp:127.0.0.1:14550', wait_ready=True)

# Define DEFAULT_SITL coordinates 
# [can be cross-checked from `~/ardupilot/Tools/autotest/arducopter.py` file]
DEFAULT_SITL_LAT = -35.362938
DEFAULT_SITL_LONG = 149.165085
TAKEOFF_ALT = 10  # meters


# Define offset (0.001 degrees is approximately 111 meters)
OFFSET = 0.001  # This will create visible distances on the map

waypoints = [
    # First side of square (moving East)
    {"lat": DEFAULT_SITL_LAT, "lon": DEFAULT_SITL_LONG + OFFSET, "alt": TAKEOFF_ALT},
    {"lat": DEFAULT_SITL_LAT, "lon": DEFAULT_SITL_LONG + (2 * OFFSET), "alt": TAKEOFF_ALT},
    {"lat": DEFAULT_SITL_LAT, "lon": DEFAULT_SITL_LONG + (3 * OFFSET), "alt": TAKEOFF_ALT},
    {"lat": DEFAULT_SITL_LAT, "lon": DEFAULT_SITL_LONG + (4 * OFFSET), "alt": TAKEOFF_ALT},
    
    # Second side of square (moving North)
    {"lat": DEFAULT_SITL_LAT - OFFSET, "lon": DEFAULT_SITL_LONG + (4 * OFFSET), "alt": TAKEOFF_ALT},
    {"lat": DEFAULT_SITL_LAT - (2 * OFFSET), "lon": DEFAULT_SITL_LONG + (4 * OFFSET), "alt": TAKEOFF_ALT},
    {"lat": DEFAULT_SITL_LAT - (3 * OFFSET), "lon": DEFAULT_SITL_LONG + (4 * OFFSET), "alt": TAKEOFF_ALT},
    {"lat": DEFAULT_SITL_LAT - (4 * OFFSET), "lon": DEFAULT_SITL_LONG + (4 * OFFSET), "alt": TAKEOFF_ALT},
    
    # Third side of square (moving West)
    {"lat": DEFAULT_SITL_LAT - (4 * OFFSET), "lon": DEFAULT_SITL_LONG + (3 * OFFSET), "alt": TAKEOFF_ALT},
    {"lat": DEFAULT_SITL_LAT - (4 * OFFSET), "lon": DEFAULT_SITL_LONG + (2 * OFFSET), "alt": TAKEOFF_ALT},
    {"lat": DEFAULT_SITL_LAT - (4 * OFFSET), "lon": DEFAULT_SITL_LONG + OFFSET, "alt": TAKEOFF_ALT},
    {"lat": DEFAULT_SITL_LAT - (4 * OFFSET), "lon": DEFAULT_SITL_LONG, "alt": TAKEOFF_ALT},
    
    # Fourth side of square (moving South, back towards start)
    {"lat": DEFAULT_SITL_LAT - (3 * OFFSET), "lon": DEFAULT_SITL_LONG, "alt": TAKEOFF_ALT},
    {"lat": DEFAULT_SITL_LAT - (2 * OFFSET), "lon": DEFAULT_SITL_LONG, "alt": TAKEOFF_ALT},
    {"lat": DEFAULT_SITL_LAT - OFFSET, "lon": DEFAULT_SITL_LONG, "alt": TAKEOFF_ALT}
]

def arm_and_takeoff(target_altitude):
    """
    Arms vehicle and fly to target_altitude.
    """
    print("Basic pre-arm checks")
    while not vehicle.is_armable:
        print("Waiting for vehicle to initialise...")
        time.sleep(1)
    
    print("Arming motors")
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True
    
    while not vehicle.armed:
        print("Waiting for arming...")
        time.sleep(1)
    
    print("Taking off!")
    vehicle.simple_takeoff(target_altitude)
    
    # Wait until the vehicle reaches a safe height
    while True:
        current_alt = vehicle.location.global_relative_frame.alt
        print(f"Altitude: {current_alt:.2f}m")
        if current_alt >= target_altitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)

def get_distance_metres(aLocation1, aLocation2):
    """
    Returns the ground distance in metres between two LocationGlobal objects.
    """
    dlat = aLocation2.lat - aLocation1.lat
    dlong = aLocation2.lon - aLocation1.lon
    return math.sqrt((dlat*dlat) + (dlong*dlong)) * 1.113195e5

def goto_position_target_global_int(lat, lon, alt):
    """
    Send SET_POSITION_TARGET_GLOBAL_INT command to request the vehicle fly to a specified location.
    """
    target_location = LocationGlobalRelative(lat, lon, alt)
    vehicle.simple_goto(target_location)
    
    # Wait until the vehicle reaches the target location
    while True:
        current_location = vehicle.location.global_relative_frame
        distance = get_distance_metres(current_location, target_location)
        
        print(f"Distance to waypoint: {distance:.2f}m")
        if distance < 1:  # If we're within 1 meter of the target
            print("Reached target location")
            break
        time.sleep(5)

def main():
    try:
        print(f"Starting mission from DEFAULT_SITL (Lat: {DEFAULT_SITL_LAT}, Long: {DEFAULT_SITL_LONG})")
        print(f"Planning to visit {len(waypoints)} waypoints at {TAKEOFF_ALT}m altitude")
        
        # Step 1: Takeoff
        arm_and_takeoff(TAKEOFF_ALT)
        
        # Step 2: Visit all waypoints
        print("\nStarting waypoint navigation...")
        for i, waypoint in enumerate(waypoints, 1):
            print(f"\nNavigating to waypoint {i}/{len(waypoints)}")
            print(f"Target: Lat: {waypoint['lat']:.6f}, Long: {waypoint['lon']:.6f}, Alt: {waypoint['alt']}m")
            goto_position_target_global_int(
                waypoint["lat"],
                waypoint["lon"],
                waypoint["alt"]
            )
        
        # Step 3: Land
        print("\nMission complete. Initiating landing sequence...")
        vehicle.mode = VehicleMode("LAND")
        
        # Wait for landing to complete
        while vehicle.location.global_relative_frame.alt > 0.1:
            current_alt = vehicle.location.global_relative_frame.alt
            print(f"Landing... Current altitude: {current_alt:.2f}m")
            time.sleep(1)
        
        print("Landed successfully!")
        
    except KeyboardInterrupt:
        print("\nMission cancelled by user!")
        vehicle.mode = VehicleMode("LAND")
        print("Emergency landing initiated...")
        
    finally:
        # Close vehicle object
        print("Closing vehicle connection...")
        vehicle.close()

if __name__ == '__main__':
    main()