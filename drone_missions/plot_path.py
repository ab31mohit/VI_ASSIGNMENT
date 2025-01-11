import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Function to extract lat, lon, and alt from mission.txt
def extract_coordinates(filename):
    latitudes = []
    longitudes = []
    altitudes = []

    with open(filename, 'r') as file:
        lines = file.readlines()

        # Skip the first line (header)
        for line in lines[1:]:
            parts = line.strip().split('\t')  # Split by tab delimiter

            if len(parts) == 12:
                lat = float(parts[8])
                lon = float(parts[9])
                alt = float(parts[10])

                latitudes.append(lat)
                longitudes.append(lon)
                altitudes.append(alt)

    return latitudes, longitudes, altitudes

# Plotting the data
def plot_3d_path(latitudes, longitudes, altitudes):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Plotting the path with a thicker line
    ax.plot(longitudes, latitudes, altitudes, color='blue', linewidth=2.5, label='Path')

    # Plotting the waypoints with larger points
    ax.scatter(longitudes, latitudes, altitudes, c='black', marker='o', s=50, label='Waypoints')

    # Mark start and end points with larger squares
    ax.scatter(longitudes[0], latitudes[0], altitudes[0], c='green', marker='s', s=50, label='Start')
    ax.scatter(longitudes[-1], latitudes[-1], altitudes[-1], c='red', marker='s', s=50, label='End')

    # Adding labels for each waypoint
    for i, (lat, lon, alt) in enumerate(zip(latitudes, longitudes, altitudes)):
        if i == 0:
            ax.text(lon, lat, alt + 0.5, 'HOME', color='purple', fontsize=8)
        else:
            ax.text(lon, lat, alt + 0.5, f'WP{i}', color='purple', fontsize=9)

    # Adding labels and title
    ax.set_xlabel('Longitude (deg)')
    ax.set_ylabel('Latitude (deg)')
    ax.set_zlabel('Altitude (m)')
    ax.set_title('3D Flight Path with Waypoint Labels', fontsize=20)
    ax.legend()
    plt.savefig("3d_path_mission.png")
    plt.show()

# Main script
if __name__ == "__main__":
    # Replace with the path to your mission.txt file
    mission_file = 'mission.txt'

    # Extract data
    lats, lons, alts = extract_coordinates(mission_file)

    # Plot the 3D path
    plot_3d_path(lats, lons, alts)
