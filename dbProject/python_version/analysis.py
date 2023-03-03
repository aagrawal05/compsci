import numpy
import matplotlib.pyplot as plt
import scipy.cluster
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

def cluster(df):
    print("Clustering...")
    # If not an empty dataframe
    if df.empty:
        return None, None

    # Find a good number of clusters
    # Use the elbow method
    # https://en.wikipedia.org/wiki/Elbow_method_(clustering)
    print("Finding number of clusters...")
    #1. Create a list of the number of clusters to test
    num_clusters = [2, 3, 4, 5, 6, 7, 8, 9, 10]
    #2. Create a list of the SSE for each number of clusters
    sse = []
    for num in num_clusters:
        #3. For each number of clusters, run kmeans and calculate the SSE
        #4. Add the SSE to the list
        sse.append(scipy.cluster.vq.kmeans2(df, num)[1].sum())
    # Find the number of clusters that minimizes the SSE
    #1. Find the index of the minimum SSE
    min_index = sse.index(min(sse))
    #2. Return the number of clusters that corresponds to the minimum SSE
    k = num_clusters[min_index]

    # Perform k-means clustering on the data
    # Return the centroids
    print("Clustering...")
    centroids, _ = scipy.cluster.vq.kmeans2(df, k)
    #return a dataframe with all the points and their cluster
    clustered_df = pd.DataFrame({
        'latitude': df['latitude'],
        'longitude': df['longitude'],
        'cluster': _
    })
    return centroids, clustered_df

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
    
    #3. Return the depth map
    return depth_map

def plot_3d(depth_map, ax):
    # Create a meshgrid for the depth map
    x_start = df['longitude'].min()
    y_start = df['latitude'].min()
    x_end = df['longitude'].max()
    y_end = df['latitude'].max()
    x = numpy.linspace(x_start, x_end, depth_map.shape[1])
    y = numpy.linspace(y_start, y_end, depth_map.shape[0])
    X, Y = numpy.meshgrid(x, y)

    ax.plot_surface(X, Y, depth_map, cmap='viridis', linewidth=0)

# TEST FUNCTION
# Render the depth map as an image
def render_depth_map(depth_map):
    # plot this graph in 3D by fitting a 3D polynomial function to the data
    # Then plot the 3D polynomial function as a surface

    # Create a meshgrid for the depth map
    x_start = df['longitude'].min()
    y_start = df['latitude'].min()
    x_end = df['longitude'].max()
    y_end = df['latitude'].max()
    x = numpy.linspace(x_start, x_end, depth_map.shape[1])
    y = numpy.linspace(y_start, y_end, depth_map.shape[0])
    X, Y = numpy.meshgrid(x, y)

    print("Plotting...")
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, depth_map, linewidth=0) #cmap='viridis', linewidth=0)
    plt.show()

if __name__ == '__main__':
    render_depth_map(generate_depth_map(df, 0.05))
