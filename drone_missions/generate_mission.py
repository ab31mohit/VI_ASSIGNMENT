#!/usr/bin/env python
"""
Script to generate a mission file for waypoints in QGC format with correct frame type
"""

DEFAULT_SITL_LAT = -35.363262
DEFAULT_SITL_LONG = 149.165237
TAKEOFF_ALT = 10  # meters
OFFSET = 0.001  # This will create visible distances on the map

def generate_mission_file():
    """
    Creates a mission file with waypoints in the QGC format.
    Does not include the takeoff, only waypoints and landing.
    Using MAV_FRAME_GLOBAL_RELATIVE_ALT (frame type 3) for relative altitudes.
    """
    
    # Create list of 16 waypoints
    # They are effectively 15 waypoints, last waypoint is added to land the drone at semilast the waypoint.
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
    ]
    
    # Create mission file content
    mission_items = []
    
    # Add HOME location as first waypoint with frame type 0 (Home location)
    mission_items.append("0\t1\t0\t16\t0\t0\t0\t0\t{}\t{}\t0\t1".format(
        DEFAULT_SITL_LAT, DEFAULT_SITL_LONG))

    # Add all waypoints with frame type 3 (MAV_FRAME_GLOBAL_RELATIVE_ALT)
    for i, wp in enumerate(waypoints, start=1):
        # Format: INDEX CURRENT_WP COORD_FRAME COMMAND PARAM1 PARAM2 PARAM3 PARAM4 LAT LON ALT AUTOCONTINUE
        mission_items.append("{}\t0\t3\t16\t0\t0\t0\t0\t{}\t{}\t{}\t1".format(
            i, wp["lat"], wp["lon"], wp["alt"]))
    
    # Add a landing waypoint at the end with frame type 3
    mission_items.append("{}\t0\t3\t21\t0\t0\t0\t0\t{}\t{}\t0\t1".format(
        len(waypoints) + 1, DEFAULT_SITL_LAT - (2 * OFFSET), DEFAULT_SITL_LONG))
    
    # Write to file
    with open('mission.txt', 'w') as f:
        f.write("QGC WPL 110\n")  # Header required by QGC
        f.write("\n".join(mission_items))
    
    print(f"Mission file generated with {len(mission_items)} commands")
    print("File saved as 'mission.txt'")
    print("\nMission structure:")
    print("- Waypoint 0: Home position (absolute frame)")
    print(f"- Waypoints 1-{len(waypoints)}: Square navigation at {TAKEOFF_ALT}m (relative frame)")
    print("- Final waypoint: Landing position")

if __name__ == '__main__':
    generate_mission_file()
