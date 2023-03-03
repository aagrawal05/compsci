import numpy
import pandas as pd
import sqlite3
import matplotlib
from mpl_toolkits.basemap import Basemap
import tkinter as tk
import analysis as an

matplotlib.use('TkAgg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)

# Create a connection to the database
print("Connecting to database...")
conn = sqlite3.connect('../db/switrs.sqlite')

#Import sqlite as dataframe using pd
query = (
        "SELECT latitude, longitude "
        "FROM collisions "
        "WHERE latitude IS NOT NULL AND longitude IS NOT NULL"
)

df = pd.read_sql_query(query, conn)

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        #Create a window
        self.title("Switrs")
        self.geometry("1000x800")

        #Split the window into two panels
        self.left_panel = tk.Frame(self)
        self.right_panel = tk.Frame(self)

        #Create a figure in the left panel
        self.fig = Figure(figsize=(6, 4), dpi=100)

        #Create a subplot to left panel
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.left_panel)
        NavigationToolbar2Tk(self.canvas, self.left_panel)

        #Create a subplot
        ax = self.fig.add_subplot(211)
        ax2 = self.fig.add_subplot(212, projection='3d')
        
        #TODO: Make the 3D plot zoom match the 2D plot zoom
        #Need to figure out how to get the current extent of the 2D plot in lat/long
        #Then convert that to x/y and set the 3D plot extent to that
        
        #Create the map
        self.basemap = Basemap(
            projection='gall',
            llcrnrlon = -126,   # lower-left corner longitude
            llcrnrlat = 32,     # lower-left corner latitude
            urcrnrlon = -113,   # upper-right corner longitude
            urcrnrlat = 43,     # upper-right corner latitude
            ax=ax
        )

        #Draw the map
        self.basemap.drawcoastlines()
        self.basemap.drawcountries()
        self.basemap.drawstates()
        self.basemap.bluemarble()

        #Plot the points
        x, y = self.basemap(df['longitude'].values, df['latitude'].values)
        #Black dots
        ax.plot(x, y, '.', color='k', markersize=1.5)

        #Plot the 3D points
        an.plot_3d(an.generate_depth_map(df, 0.05), ax2)
        ax2.set_xlabel('Longitude')
        ax2.set_ylabel('Latitude')
        ax2.set_zlabel('Number of Collisions')
        
        #Add a panel for the longitude query range feature
        self.longitude_query_panel = tk.Frame(self.right_panel)
        self.longitude_query_panel.pack(side=tk.TOP, fill=tk.X)
        
        #Add a text field for the longitude query range feature
        self.longitude_query_label = tk.Label(self.longitude_query_panel, text="Longitude Range")
        self.longitude_query_label.pack()
        self.min_longitude = tk.Entry(self.longitude_query_panel)
        self.min_longitude.pack(side=tk.LEFT)
        self.max_longitude = tk.Entry(self.longitude_query_panel)
        self.max_longitude.pack(side=tk.RIGHT)

        #Add a panel for the latitude query range feature
        self.latitude_query_panel = tk.Frame(self.right_panel)
        self.latitude_query_panel.pack(side=tk.TOP, fill=tk.X)
        
        #Add a text field for the latitude query range feature
        self.latitude_query_label = tk.Label(self.latitude_query_panel, text="Latitude Range")
        self.latitude_query_label.pack()
        self.min_latitude = tk.Entry(self.latitude_query_panel)
        self.min_latitude.pack(side=tk.LEFT)
        self.max_latitude = tk.Entry(self.latitude_query_panel)
        self.max_latitude.pack(side=tk.RIGHT)

        #Add a button to query the database
        self.query_button = tk.Button(self.right_panel, text="Query", command=self.query)
        self.query_button.pack()

        #Add a label for the listbox
        self.label = tk.Label(self.right_panel, text="Clusters")
        self.label.pack()

        #Create a listbox in the right panel
        self.listbox = tk.Listbox(self.right_panel, width=50, height=30)

        #Render the listbox
        self.listbox.pack()
        self.listbox.bind('<Double-Button-1>', self.listbox_double_click)

        #Create a panel for the add point text boxes
        self.add_point_panel = tk.Frame(self.right_panel)
        self.add_point_panel.pack()
        self.add_point_label = tk.Label(self.add_point_panel, text="Enter longitude and latitude to add a point")
        self.add_point_label.pack()

        #Add two text fields to enter the coordinates
        self.latitude = tk.Entry(self.add_point_panel)
        self.latitude.pack(side=tk.LEFT)
        self.longitude = tk.Entry(self.add_point_panel)
        self.longitude.pack(side=tk.RIGHT)

        #Create a button to add a point
        self.add_point_button = tk.Button(self.right_panel, text="Add Point", command=self.add_point)
        self.add_point_button.pack()

        #Create a button to cluster the data in the current view
        self.button = tk.Button(self.right_panel, text="Cluster", command=self.cluster)
        self.button.pack()

        #Render the panels
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

    def cluster(self):
        #Clear the listbox
        self.listbox.delete(0, tk.END)

        #Get the current extent of the map
        xmin, xmax = self.fig.axes[0].get_xlim()
        ymin, ymax = self.fig.axes[0].get_ylim()
        
        #Convert the extent to lat/long
        xmin, ymin = self.basemap(xmin, ymin, inverse=True)
        xmax, ymax = self.basemap(xmax, ymax, inverse=True)

        #Get the current view of the map
        view = df[(df['latitude'] >= ymin) & (df['latitude'] <= ymax) & (df['longitude'] >= xmin) & (df['longitude'] <= xmax)]

        #Cluster the data
        centroids, clusters = an.cluster(view)
        
        if (centroids is None or clusters is None):
            return
        
        #Add the centroids to the listbox
        for centroid in centroids:
            self.listbox.insert(tk.END, "Collision at {}, {}".format(round(centroid[0], 4), round(centroid[1], 4)))

        #self.fig.axes[0].clear()
        #Clusters format (longitude, latitude, cluster)
        #Plot the clusters with a different color for each cluster and the centroid of the cluster
        # A list of random colors with length equal to the number of clusters
        colors = [matplotlib.colors.rgb2hex(numpy.random.rand(3)) for i in range(len(centroids))]
        for index, row in clusters.iterrows():
            x, y = self.basemap(row['longitude'], row['latitude'])
            self.fig.axes[0].plot(x, y, '.', color=colors[int(row['cluster'])], markersize=1.5)

        for cluster in centroids:
            x, y = self.basemap(centroid[0], centroid[1])
            self.fig.axes[0].plot(x, y, 'r*', markersize=100)

        self.canvas.draw()

    def listbox_double_click(self, event):
        # Zoom to the selected cluster
        centroid = self.listbox.get(self.listbox.curselection())
        centroid = centroid.split("at ")[1]
        centroid = centroid.split(", ")
        centroid = [float(centroid[0]), float(centroid[1])]
        # Set extent of `self.fig.axes[0]` to the centroid with a 0.1 degree buffer
        print(centroid)
        centroid = self.basemap(centroid[0], centroid[1])
        print(centroid)
        self.fig.axes[0].set_xlim(centroid[0] - 0.1, centroid[0] + 0.1)
        self.fig.axes[0].set_ylim(centroid[1] - 0.1, centroid[1] + 0.1)
        self.canvas.draw()

    def add_point(self):
        #Read the latitude and longitude from the text boxes
        latitude = float(self.latitude.get())
        longitude = float(self.longitude.get())
        #Ensure the latitude and longitude are valid
        #TODO: Add toast message
        if (latitude < -90 or latitude > 90 or longitude < -180 or longitude > 180):
            return
        #Add the point to the dataframe
        df.loc[len(df)] = [latitude, longitude]
        #Plot the point on the map
        x, y = self.basemap(longitude, latitude)
        self.fig.axes[0].plot(x, y, 'k.', markersize=1.5)
        #Query insert the point into the database
        conn.cursor.execute("INSERT INTO collisions (latitude, longitude) VALUES (%s, %s)", (latitude, longitude))
        conn.conn.commit()
        #Redraw the map
        self.canvas.draw()

    def query(self):
        #Get min and max latitude and longitude from the text boxes
        min_latitude = float(self.min_latitude.get())
        max_latitude = float(self.max_latitude.get())
        min_longitude = float(self.min_longitude.get())
        max_longitude = float(self.max_longitude.get())
        #Ensure the min and max latitude and longitude are valid
        if (min_latitude < -90 or min_latitude > 90 or max_latitude < -90 or max_latitude > 90 or min_longitude < -180 or min_longitude > 180 or max_longitude < -180 or max_longitude > 180):
            return

        #Get the data from the df
        data = df[(df['latitude'] >= min_latitude) & (df['latitude'] <= max_latitude) & (df['longitude'] >= min_longitude) & (df['longitude'] <= max_longitude)]
        
        #Redraw the map
        self.fig.axes[0].clear()
        self.basemap.drawcoastlines()
        self.basemap.drawcountries()
        self.basemap.drawstates()
        self.basemap.bluemarble()

        #Plot the data on the map
        x, y = self.basemap(data['longitude'].values, data['latitude'].values)
        self.fig.axes[0].plot(x, y, 'k.', markersize=1.5)

        self.fig.axes[1].clear()
        an.plot_3d(an.generate_depth_map(df, 0.05), self.fig.axes[1])
        self.fig.axes[1].set_xlabel('Longitude')
        self.fig.axes[1].set_ylabel('Latitude')
        self.fig.axes[1].set_zlabel('Number of Collisions')

        self.canvas.draw()



if __name__ == '__main__':
    app = App()
    app.mainloop()
    conn.close()


