import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable

def plot_map(geofile, intensities, save_image, title):
    fig, ax = plt.subplots(1, 1)
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.1)
    print(title)
    data = gpd.read_file(geofile)
    data["intensities"] = intensities
    data.plot(column="intensities", ax=ax, legend=True, cmap="RdYlGn_r", cax=cax, legend_kwds={'label': "Intensities in Percentage"})
    plt.title(title,fontsize=30)
    plt.savefig(save_image)
    plt.clf()

geofile = "../nepal-map-governance/NEPAL_DISTRICTS_WGS.shp"
intensities = list(range(77))
save_image = "gapanapa.png"
title = "Nepal Gaupalika"

plot_map(geofile, intensities, save_image, title)