import numpy
import pandas as pd
import sqlite3
import matplotlib
from mpl_toolkits.basemap import Basemap
import tkinter as tk

matplotlib.use('TkAgg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)

from sklearn.cluster import DBSCAN

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

#Close the connection
conn.close()

#Dummy data within california with 30 points in 2 clear clusters
df = pd.DataFrame({
    'latitude': [34.56, 34.57, 34.58, 34.59, 34.60, 34.61, 34.62, 34.63, 34.64, 34.65, 34.66, 34.67, 34.68, 34.69, 34.70, 34.71, 34.72, 34.73, 34.74, 34.75, 34.76, 34.77, 34.78, 34.79, 34.80, 34.81, 34.82, 34.83, 34.84, 34.85],
    'longitude': [-118.56, -118.57, -118.58, -118.59, -118.60, -118.61, -118.62, -118.63, -118.64, -118.65, -118.66, -118.67, -118.68, -118.69, -118.70, -118.71, -118.72, -118.73, -118.74, -118.75, -118.76, -118.77, -118.78, -118.79, -118.80, -118.81, -118.82, -118.83, -118.84, -118.85]
})

db = DBSCAN(eps=0.01, min_samples=10).fit(df)
print(db)

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        #Create a window
        self.title("Switrs")
        self.geometry("800x600")

        #Split the window into two panels
        self.left_panel = tk.Frame(self)
        self.right_panel = tk.Frame(self)

        #Create a figure in the left panel
        fig = Figure(figsize=(6, 4), dpi=100)

        #Create a subplot to left panel
        self.canvas = FigureCanvasTkAgg(fig, master=self.left_panel)
        NavigationToolbar2Tk(self.canvas, self.left_panel)

        #Create a subplot
        ax = fig.add_subplot(111)

        #Create the map
        basemap = Basemap(
            projection='gall',
            llcrnrlon = -126,   # lower-left corner longitude
            llcrnrlat = 32,     # lower-left corner latitude
            urcrnrlon = -113,   # upper-right corner longitude
            urcrnrlat = 43,     # upper-right corner latitude
            ax=ax
        )

        #Draw the map
        basemap.drawcoastlines()
        basemap.drawcountries()
        basemap.drawstates()

        #Plot the points
        x, y = basemap(df['longitude'].values, df['latitude'].values)
        ax.plot(x, y, 'k.', markersize=1.5)

        #Add a label for the listbox
        self.label = tk.Label(self.right_panel, text="Clusters")
        self.label.pack()

        #Create a listbox in the right panel
        self.listbox = tk.Listbox(self.right_panel, width=50, height=30)

        #Add the clusters to the listbox
        for cluster in set(db.labels_):
            self.listbox.insert(tk.END, cluster)

        #Render the listbox
        self.listbox.pack()

        #Render the panels
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

        print("Done")
    
if __name__ == '__main__':
    app = App()
    app.mainloop()


