import numpy
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3

print("Loading data...")
conn = sqlite3.connect('../db/switrs.sqlite')

#Import sqlite as dataframe using pd
query = (
        "SELECT latitude, longitude "
        "FROM collisions "
        "WHERE latitude IS NOT NULL AND longitude IS NOT NULL"
)

df = pd.read_sql_query(query, conn)

#Close the connection
conn.close()

# Generate a depth map for the data with interpolation for smoothing
def generate_depth_map(df, resolution):
    # Create a grid of points
    x_start = df['longitude'].min()
    y_start = df['latitude'].min()
    x_end = df['longitude'].max()
    y_end = df['latitude'].max()

    print("Generating depth map...")
    #1. Create a depth map with the resolution specified
    print("Creating depth map...")
    depth_map = numpy.zeros((int((x_end - x_start)/resolution), int((y_end - y_start)/resolution)))
    for index, row in df.iterrows():
        x_index = int((row['longitude'] - x_start)/resolution)
        y_index = int((row['latitude'] - y_start)/resolution)
        # Only increment the depth map if the point is within the bounds
        if x_index < depth_map.shape[0] and y_index < depth_map.shape[1]:
            depth_map[x_index][y_index] += 1
    
    #2. Interpolate the depth map by averaging the surrounding points
    print("Interpolating depth map...")
    for i in range(depth_map.shape[0]):
        for j in range(depth_map.shape[1]):
            depth_map[i][j] = numpy.average(depth_map[max(0, i-1):min(depth_map.shape[0], i+2), max(0, j-1):min(depth_map.shape[1], j+2)])

    #3. Return the depth map
    return depth_map

# TEST FUNCTION
# Render the depth map as an image
def render_depth_map(depth_map):
    print("Rendering depth map...")
    plt.imshow(depth_map, cmap='hot', extent=[0, depth_map.shape[1], depth_map.shape[0], 0], vmin=0.0, vmax=20.0)
    plt.show()

    '''
    #Normalize the depth map to 0-255
    depth_map = numpy.interp(depth_map, (depth_map.min(), depth_map.max()), (0, 255))

    plt.imshow(depth_map, cmap='gray')
    plt.show()
    '''
if __name__ == '__main__':
    render_depth_map(generate_depth_map(df, 0.001))
