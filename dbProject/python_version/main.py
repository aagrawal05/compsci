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

#Example anomaly data
anomalies = pd.DataFrame({
    'latitude': [
        34.0522,
        34.0522,
        34.0522,
    ],
    'longitude': [
        -118.2437,
        -118.2437,
        -118.2437,
    ]
})

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
        self.label = tk.Label(self.right_panel, text="Anomalies")
        self.label.pack()

        #Create a listbox in the right panel
        self.listbox = tk.Listbox(self.right_panel, width=50, height=30)

        #Set the listbox to contain all the positions of the anomalies
        for index, row in anomalies.iterrows():
            self.listbox.insert(tk.END, "Collision at {}, {}".format(row['latitude'], row['longitude']))

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


